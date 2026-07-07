"""
Signal analyst — uses Claude to interpret spike signals in the context of
prediction market flow and surface high-confidence actionable reads.
"""
from __future__ import annotations

import json
import logging
import os
import pathlib
import re
import threading
import time
from collections import OrderedDict
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any, Callable

log = logging.getLogger(__name__)

MAX_SIGNAL_ANALYST_CACHE = 500
DEFAULT_PROVIDER_COOLDOWN_MINUTES = 60
# Minimum seconds between tuning-advisor runs. Each run costs LLM calls
# (advisor + governor) and appends a snapshot to the tuning backlog; without a
# floor, the 3s dashboard poll re-triggers on every newly analysed signal.
DEFAULT_TUNING_ADVISOR_INTERVAL_SECONDS = 3600.0
_RULE_SIM_WORD_TOKENS_RE = re.compile(r"[a-z0-9_]+")
_RULE_SIM_JACCARD_THRESHOLD = 0.55  # >55% word overlap = likely clash



def _summarize_provider_error(provider: str, exc: Exception) -> str:
    """Map provider exceptions to short, user-facing guidance."""
    text = str(exc).lower()
    if "credit balance" in text or "billing" in text or "insufficient" in text or "purchase credits" in text:
        return "check billing credits"
    if "401" in text or "unauthorized" in text or "invalid api key" in text or "authentication" in text:
        return "API key invalid or expired"
    if "403" in text or "forbidden" in text:
        return "API access denied"
    if "429" in text or "rate limit" in text:
        return "rate limited — try again shortly"
    if "no module named" in text and provider == "anthropic":
        return "anthropic client unavailable in this build"
    return "request failed — check API key and account status"


class AIProviderManager:
    """Manages AI provider health, ordering, and cooling down failing ones."""

    def __init__(self, cooldown_mins: int = DEFAULT_PROVIDER_COOLDOWN_MINUTES):
        self.cooldown_mins = cooldown_mins
        self._health: dict[str, datetime | None] = {}  # None = healthy, datetime = fail timestamp
        self._last_errors: dict[str, str] = {}
        self._lock = threading.Lock()

    def report_failure(self, name: str, error: Exception | str | None = None) -> None:
        """Mark a provider as failing for the cooldown period."""
        summary = _summarize_provider_error(name, error) if isinstance(error, Exception) else (
            str(error).strip() if error else "request failed"
        )
        with self._lock:
            self._health[name] = datetime.now(UTC)
            self._last_errors[name] = summary
            log.warning("provider[%s]: demoted (cooldown starts now) — %s", name, summary)

    def report_success(self, name: str) -> None:
        """Clear any failure for a provider."""
        with self._lock:
            if self._health.get(name):
                self._health[name] = None
                log.info("provider[%s]: restored to healthy", name)
            self._last_errors.pop(name, None)

    def get_ordered_providers(self, requested: list[tuple[str, Callable]]) -> list[tuple[str, Callable]]:
        """Return requested providers sorted by health (healthy first, others by cooldown age)."""
        now = datetime.now(UTC)
        with self._lock:
            # Partition: (healthy_list, cooling_down_list)
            healthy = []
            cooling = []

            for name, call in requested:
                fail_time = self._health.get(name)
                if fail_time:
                    # check if cooldown expired
                    age_mins = (now - fail_time).total_seconds() / 60
                    if age_mins >= self.cooldown_mins:
                        # auto-restore
                        self._health[name] = None
                        healthy.append((name, call))
                    else:
                        cooling.append((name, call, fail_time))
                else:
                    healthy.append((name, call))

            # sort cooling by rarest/oldest failure first (optional, but keep it stable)
            cooling.sort(key=lambda x: x[2])
            ordered = healthy + [(c[0], c[1]) for c in cooling]
            return ordered

    def health_status(self, provider_names: list[str]) -> dict[str, Any]:
        """Return analyst health for dashboard surfacing."""
        if not provider_names:
            return {"healthy": True, "failing": False, "message": None, "providers": []}

        with self._lock:
            provider_notes = [
                f"{name}: {self._last_errors[name]}"
                for name in provider_names
                if name in self._last_errors
            ]
            all_recently_failed = bool(provider_notes) and len(provider_notes) == len(provider_names)

        if not all_recently_failed:
            return {"healthy": True, "failing": False, "message": None, "providers": provider_notes}

        detail = "; ".join(provider_notes)
        message = (
            "AI analyst cannot reach any configured provider. "
            f"{detail}. Update API keys or billing in your .env, then restart the app."
        )
        return {
            "healthy": False,
            "failing": True,
            "message": message,
            "providers": provider_notes,
        }


@dataclass
class AnalystRead:
    signal_id: str                    # market_id + detected_at
    noise_or_signal: str              # "noise" | "signal" | "uncertain"
    direction: str                    # "yes" | "no" | "unclear"
    confidence: str                   # "low" | "medium" | "high"
    rationale: str                    # one-paragraph plain-English read
    threshold_note: str               # detector tuning suggestion if any
    probability_yes: float | None = None  # agent's P(resolves YES) in [0,1]
    generated_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def to_dict(self) -> dict[str, Any]:
        return {
            "noise_or_signal": self.noise_or_signal,
            "direction": self.direction,
            "confidence": self.confidence,
            "rationale": self.rationale,
            "threshold_note": self.threshold_note,
            "probability_yes": self.probability_yes,
            "generated_at": self.generated_at.isoformat(),
        }


def _coerce_probability(value: Any) -> float | None:
    """Coerce the model's probability_yes to a float in [0.0, 1.0].

    Returns None on anything unusable (missing, non-numeric, out of range) so a
    bad model response never poisons the eval log — the scorer simply skips
    signals without a usable agent probability."""
    if value is None:
        return None
    try:
        p = float(value)
    except (TypeError, ValueError):
        return None
    if p != p or p < 0.0 or p > 1.0:  # NaN or out of range
        return None
    return p


def _normalize_trade_side(trade_side: Any) -> str | None:
    """Map platform side vocabulary to yes/no. Mirrors the detector's rule:
    Kalshi uses yes/no, PolyAlertHub uses buy/sell."""
    side = str(trade_side or "").strip().lower()
    if side in {"yes", "buy"}:
        return "yes"
    if side in {"no", "sell"}:
        return "no"
    return None


def _scoped_rule_texts(
    signal: dict[str, Any],
    ruleset_store: Any | None,
    limit: int,
) -> list[str]:
    """Return applied-rule texts relevant to this signal's topic/tier.

    Defensive by design: any missing store or lookup error yields an empty list,
    so a ruleset problem can never break signal analysis. Empty result → the
    analyst prompt is byte-identical to pre-ruleset behavior.
    """
    if ruleset_store is None:
        return []
    event = signal.get("event") or {}
    topic = signal.get("topic") or event.get("topic")
    tier = signal.get("tier")
    try:
        return [r.text for r in ruleset_store.rules_for_scope(topic=topic, tier=tier, limit=limit)]
    except Exception as exc:  # pragma: no cover - safety net
        log.warning("ruleset lookup failed, proceeding without rules: %s", exc)
        return []


def _build_prompt(
    signal: dict[str, Any],
    recent_flow: list[dict[str, Any]],
    ruleset_rules: list[str] | None = None,
) -> str:
    event = signal.get("event") or {}
    market_id = event.get("market_id", "unknown")
    title = event.get("title", market_id)
    yes_price = event.get("yes_price")
    volume_delta = signal.get("volume_delta")
    baseline = signal.get("baseline_volume_delta")
    price_move = signal.get("price_move")
    score = signal.get("score")
    tier = signal.get("tier", "watch")
    reason = signal.get("reason", "")
    baseline_1h = signal.get("baseline_1h")
    baseline_24h = signal.get("baseline_24h")
    price_move_1m = signal.get("price_move_1m")
    price_move_5m = signal.get("price_move_5m")
    price_move_30m = signal.get("price_move_30m")
    leading_events = signal.get("leading_events") or []

    # Recent flow for this market, oldest → newest. The store returns events
    # newest-first, so sort by timestamp before slicing; otherwise the trend
    # delta and price history read backwards.
    market_flow = sorted(
        (e for e in recent_flow if e.get("market_id") == market_id),
        key=lambda e: str(e.get("timestamp") or ""),
    )[-20:]
    prices = [e.get("yes_price") for e in market_flow if e.get("yes_price") is not None]
    trades = [e for e in market_flow if e.get("event_kind") == "trade"]
    # Normalize side vocabulary: Kalshi uses yes/no, PolyAlertHub uses buy/sell.
    # Counting only literal "yes"/"no" silently dropped every buy/sell trade.
    trade_sides = [_normalize_trade_side(t.get("trade_side")) for t in trades]
    yes_trades = sum(1 for s in trade_sides if s == "yes")
    no_trades = sum(1 for s in trade_sides if s == "no")
    price_trend = ""
    if len(prices) >= 2:
        delta = prices[-1] - prices[0]
        price_trend = f"trending {'up' if delta > 0 else 'down'} {abs(delta):.3f} over last {len(prices)} ticks"

    def fmt_number(value: Any, decimals: int = 0) -> str:
        if value is None:
            return "n/a"
        return f"{float(value):,.{decimals}f}"

    def fmt_pct(value: Any) -> str:
        if value is None:
            return "n/a"
        return f"{float(value) * 100:.1f}%"

    leading_lines = []
    for lead in leading_events[-5:]:
        lead_side = lead.get("trade_side") or "-"
        leading_lines.append(
            f"    - {lead.get('event_kind', 'event')} @ {lead.get('timestamp', 'unknown time')} "
            f"price={fmt_number(lead.get('yes_price'), 3)} vol={fmt_number(lead.get('volume'), 0)} side={lead_side}"
        )
    leading_summary = "\n".join(leading_lines) if leading_lines else "    - none"

    # Applied tuning rules relevant to this signal's topic/tier (Phase 2).
    # When the ruleset is empty, this block is omitted entirely so the prompt is
    # byte-identical to the pre-ruleset behavior (zero regression).
    ruleset_block = ""
    if ruleset_rules:
        rule_lines = "\n".join(f"  - {r}" for r in ruleset_rules)
        ruleset_block = (
            "\n\nAPPLIED TUNING RULES (learned from prior analysis — apply these when judging)\n"
            f"{rule_lines}\n"
        )

    prompt = f"""You are a prediction market analyst. A spike detector has flagged unusual activity on a Kalshi market.

MARKET
  ID: {market_id}
  Question (title): {title}
  Current yes price: {f'{yes_price:.3f} ({yes_price*100:.1f}% implied probability)' if yes_price is not None else 'unknown'}

SPIKE DETAILS
  Score: {score} (tier: {tier})
  Volume delta: {volume_delta:,.0f} vs baseline {baseline:,.0f} ({f'{volume_delta/baseline:.1f}x' if baseline else 'n/a'} baseline)
  Price move: {fmt_pct(price_move)}
  Detector reason: {reason}

ENRICHED DETECTOR CONTEXT
  1h baseline delta: {fmt_number(baseline_1h, 0)}
  24h baseline delta: {fmt_number(baseline_24h, 0)}
  Price moves: 1m={fmt_pct(price_move_1m)}, 5m={fmt_pct(price_move_5m)}, 30m={fmt_pct(price_move_30m)}
  Leading events before spike:
{leading_summary}

RECENT FLOW ({len(market_flow)} events)
  Price history: {', '.join(f'{p:.3f}' for p in prices[-10:]) if prices else 'none'}
  Price trend: {price_trend or 'insufficient data'}
  Recent trades: {len(trades)} total — {yes_trades} yes-side, {no_trades} no-side
{ruleset_block}
YOUR TASK
Interpret this signal for a trader who wants to decide whether this yes/no question is worth acting on.

Return your analysis as a JSON object with exactly these fields:
{{
  "noise_or_signal": "noise" | "signal" | "uncertain",
  "direction": "yes" | "no" | "unclear",
  "confidence": "low" | "medium" | "high",
  "probability_yes": <number between 0 and 1: your best estimate of the probability this market resolves YES, given everything above; this is scored against the market's own implied probability, so only diverge from the current price when the flow gives you a real reason to>,
  "rationale": "<2-3 sentence plain-English interpretation: what the flow suggests, whether the move looks informed or mechanical, and what the current price implies about the market's conviction>",
  "threshold_note": "<one sentence: if this looks like noise, what detector threshold change would reduce false positives for this type of market — or 'none' if the signal looks real>"
}}

Return only the JSON object. No markdown, no preamble.
"""
    return prompt


def _parse_json_response(raw: str) -> dict:
    """Strip markdown fences and parse JSON from LLM response."""
    raw = raw.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip()
    # Strip trailing citation markers like [1][2] added by Perplexity
    import re
    raw = re.sub(r"\[\d+\]", "", raw).strip()
    return __import__("json").loads(raw)


def _analyze_via_openai_compatible(prompt: str, api_key: str, model: str, base_url: str) -> str:
    """Call an OpenAI-compatible chat endpoint and return raw response text."""
    import json as _json
    import urllib.request as _ureq
    payload = _json.dumps({
        "model": model,
        "max_tokens": 512,
        "messages": [{"role": "user", "content": prompt}],
    }).encode()
    req = _ureq.Request(
        f"{base_url}/chat/completions",
        data=payload,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
    )
    resp = _json.load(_ureq.urlopen(req, timeout=20))
    return resp["choices"][0]["message"]["content"]


def _analyze_via_anthropic(prompt: str, api_key: str, model: str) -> str:
    """Call Claude API and return raw response text."""
    import anthropic
    client = anthropic.Anthropic(api_key=api_key)
    msg = client.messages.create(
        model=model,
        max_tokens=512,
        messages=[{"role": "user", "content": prompt}],
    )
    return msg.content[0].text


def _analyze_via_perplexity(prompt: str, api_key: str, model: str) -> str:
    """Call Perplexity API (OpenAI-compatible) and return raw response text."""
    return _analyze_via_openai_compatible(prompt, api_key, model, "https://api.perplexity.ai")


def analyze_signal(
    signal: dict[str, Any],
    recent_flow: list[dict[str, Any]],
    anthropic_keys: list[str] | str | None = None,
    perplexity_keys: list[str] | str | None = None,
    openai_keys: list[str] | str | None = None,
    xai_keys: list[str] | str | None = None,
    gemini_keys: list[str] | str | None = None,
    anthropic_model: str = "claude-haiku-4-5",
    perplexity_model: str = "sonar",
    openai_model: str = "gpt-4o-mini",
    xai_model: str = "grok-2-1212",
    gemini_model: str = "gemini-2.5-flash",
    provider_manager: AIProviderManager | None = None,
    ruleset_store: Any | None = None,
    ruleset_limit: int = 40,
) -> AnalystRead | None:
    """Synchronous signal analysis with provider/key failover.

    Tries providers in the order suggested by the manager (usually Anthropic
    first). Within each provider, multiple keys are tried in order. When
    ``ruleset_store`` is provided, scope-relevant applied rules are injected into
    the prompt so the analyst judges against the learned ruleset (Phase 2).
    """
    def _as_list(value: list[str] | str | None) -> list[str]:
        if not value:
            return []
        return value if isinstance(value, list) else [value]

    anthropic_key_list = _as_list(anthropic_keys)
    perplexity_key_list = _as_list(perplexity_keys)
    openai_key_list = _as_list(openai_keys)
    xai_key_list = _as_list(xai_keys)
    gemini_key_list = _as_list(gemini_keys)

    rules = _scoped_rule_texts(signal, ruleset_store, ruleset_limit)
    prompt = _build_prompt(signal, recent_flow, rules)
    event = signal.get("event") or {}
    signal_id = f"{event.get('market_id', 'unknown')}@{signal.get('detected_at', '')}"

    providers: list[tuple[str, Callable[[], str]]] = []
    for idx, key in enumerate(anthropic_key_list):
        providers.append((f"anthropic-key-{idx+1}", lambda k=key: _analyze_via_anthropic(prompt, k, anthropic_model)))
    for idx, key in enumerate(perplexity_key_list):
        providers.append((f"perplexity-key-{idx+1}", lambda k=key: _analyze_via_perplexity(prompt, k, perplexity_model)))
    for idx, key in enumerate(openai_key_list):
        providers.append((f"openai-key-{idx+1}", lambda k=key: _analyze_via_openai_compatible(prompt, k, openai_model, "https://api.openai.com")))
    for idx, key in enumerate(xai_key_list):
        providers.append((f"xai-key-{idx+1}", lambda k=key: _analyze_via_openai_compatible(prompt, k, xai_model, "https://api.x.ai")))
    for idx, key in enumerate(gemini_key_list):
        providers.append((f"gemini-key-{idx+1}", lambda k=key: _analyze_via_openai_compatible(prompt, k, gemini_model, "https://generativelanguage.googleapis.com/v1beta/openai")))

    last_error = None
    ordered_providers = (
        provider_manager.get_ordered_providers(providers)
        if provider_manager else providers
    )

    for provider_name, call in ordered_providers:
        try:
            raw = call()
            log.debug("analyst[%s] raw: %s", provider_name, raw[:200])
            data = _parse_json_response(raw)
            log.info("analyst[%s]: %s → %s/%s/%s", provider_name, signal_id[:40],
                     data.get("noise_or_signal"), data.get("direction"), data.get("confidence"))

            if provider_manager:
                provider_manager.report_success(provider_name)

            return AnalystRead(
                signal_id=signal_id,
                noise_or_signal=str(data.get("noise_or_signal", "uncertain")),
                direction=str(data.get("direction", "unclear")),
                confidence=str(data.get("confidence", "low")),
                rationale=str(data.get("rationale", "")),
                threshold_note=str(data.get("threshold_note", "none")),
                probability_yes=_coerce_probability(data.get("probability_yes")),
            )
        except Exception as exc:
            log.warning("analyst[%s]: failed: %s", provider_name, exc)
            if provider_manager:
                provider_manager.report_failure(provider_name, exc)
            last_error = exc
            continue

    if last_error:
        log.warning("analyst: all providers/keys failed, last error: %s", last_error)
    return None


@dataclass
class TuningAdvice:
    summary: str
    global_recommendation: str
    recommendations: list[str]
    suggested_min_volume_delta: float | None = None
    suggested_min_price_move: float | None = None
    suggested_score_threshold: float | None = None
    proposed_rules: list[dict[str, Any]] = field(default_factory=list)
    conflict: bool = False
    conflict_reason: str | None = None
    generated_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def to_dict(self) -> dict[str, Any]:
        suggested: dict[str, float] = {}
        if self.suggested_min_volume_delta is not None:
            suggested["min_volume_delta"] = self.suggested_min_volume_delta
        if self.suggested_min_price_move is not None:
            suggested["min_price_move"] = self.suggested_min_price_move
        if self.suggested_score_threshold is not None:
            suggested["score_threshold"] = self.suggested_score_threshold
        return {
            "summary": self.summary,
            "global_recommendation": self.global_recommendation,
            "recommendations": self.recommendations,
            "suggested_thresholds": suggested,  # empty dict when no structured suggestion
            "proposed_rules": self.proposed_rules,  # [] when no structured rules
            "conflict": self.conflict,
            "conflict_reason": self.conflict_reason,
            "generated_at": self.generated_at.isoformat(),
        }


class SignalAnalyst:
    """Background analyst that enriches signals with LLM reads.

    Tries providers in provider order first, with key-level failover inside each
    provider: Anthropic → Perplexity → OpenAI → Grok. Analysis runs in a daemon
    thread so it never blocks ingestion. Results are stored in a local cache
    keyed by signal_id.
    """

    def __init__(
        self,
        anthropic_keys: list[str] | str | None = None,
        perplexity_keys: list[str] | str | None = None,
        openai_keys: list[str] | str | None = None,
        xai_keys: list[str] | str | None = None,
        gemini_keys: list[str] | str | None = None,
        anthropic_key: str = "",
        perplexity_key: str = "",
        openai_key: str = "",
        xai_key: str = "",
        gemini_key: str = "",
        anthropic_model: str = "claude-haiku-4-5",
        perplexity_model: str = "sonar",
        openai_model: str = "gpt-4o-mini",
        xai_model: str = "grok-2-1212",
        gemini_model: str = "gemini-2.5-flash",
        provider_manager: AIProviderManager | None = None,
        ruleset_store: Any | None = None,
    ) -> None:
        def _coerce_keys(values):
            if not values:
                return []
            return values if isinstance(values, list) else [values]

        self._anthropic_keys = _coerce_keys(anthropic_keys) or ([anthropic_key] if anthropic_key else [])
        self._perplexity_keys = _coerce_keys(perplexity_keys) or ([perplexity_key] if perplexity_key else [])
        self._openai_keys = _coerce_keys(openai_keys) or ([openai_key] if openai_key else [])
        self._xai_keys = _coerce_keys(xai_keys) or ([xai_key] if xai_key else [])
        self._gemini_keys = _coerce_keys(gemini_keys) or ([gemini_key] if gemini_key else [])
        self._anthropic_model = anthropic_model
        self._perplexity_model = perplexity_model
        self._openai_model = openai_model
        self._xai_model = xai_model
        self._gemini_model = gemini_model
        self._provider_manager = provider_manager or AIProviderManager()
        self._ruleset_store = ruleset_store
        self._cache: OrderedDict[str, dict[str, Any]] = OrderedDict()
        self._lock = threading.Lock()
        self._in_flight: set[str] = set()

        self._providers_configured = []
        for name, keys in [
            ("anthropic", self._anthropic_keys),
            ("perplexity", self._perplexity_keys),
            ("openai", self._openai_keys),
            ("xai", self._xai_keys),
            ("gemini", self._gemini_keys),
        ]:
            for idx in range(len(keys)):
                self._providers_configured.append(f"{name}-key-{idx+1}")

        self._session_failing = False
        self._failure_message: str | None = None

        provider_bits = []
        if self._anthropic_keys:
            provider_bits.append(f"anthropic/{anthropic_model} x{len(self._anthropic_keys)}")
        if self._perplexity_keys:
            provider_bits.append(f"perplexity/{perplexity_model} x{len(self._perplexity_keys)}")
        if self._openai_keys:
            provider_bits.append(f"openai/{openai_model} x{len(self._openai_keys)}")
        if self._xai_keys:
            provider_bits.append(f"xai/{xai_model} x{len(self._xai_keys)}")
        if self._gemini_keys:
            provider_bits.append(f"gemini/{gemini_model} x{len(self._gemini_keys)}")
        log.info("signal analyst ready, providers: %s", ", ".join(provider_bits) or "none")

    def enqueue(
        self,
        signal: dict[str, Any],
        recent_flow: list[dict[str, Any]],
        on_complete: Callable[[dict[str, Any], dict[str, Any]], None] | None = None,
    ) -> None:
        """Fire-and-forget: analyze signal in background thread."""
        event = signal.get("event") or {}
        signal_id = f"{event.get('market_id', 'unknown')}@{signal.get('detected_at', '')}"

        with self._lock:
            if signal_id in self._cache or signal_id in self._in_flight:
                return
            self._in_flight.add(signal_id)

        t = threading.Thread(
            target=self._run,
            args=(signal_id, signal, list(recent_flow), on_complete),
            daemon=True,
            name=f"analyst-{signal_id[:30]}",
        )
        t.start()

    def _remember_result(self, signal_id: str, payload: dict[str, Any]) -> None:
        with self._lock:
            self._cache[signal_id] = payload
            self._cache.move_to_end(signal_id)
            while len(self._cache) > MAX_SIGNAL_ANALYST_CACHE:
                self._cache.popitem(last=False)

    def _run(
        self,
        signal_id: str,
        signal: dict,
        flow: list,
        on_complete: Callable[[dict[str, Any], dict[str, Any]], None] | None = None,
    ) -> None:
        try:
            result = analyze_signal(
                signal, flow,
                anthropic_keys=self._anthropic_keys,
                perplexity_keys=self._perplexity_keys,
                openai_keys=self._openai_keys,
                xai_keys=self._xai_keys,
                gemini_keys=self._gemini_keys,
                anthropic_model=self._anthropic_model,
                perplexity_model=self._perplexity_model,
                openai_model=self._openai_model,
                xai_model=self._xai_model,
                gemini_model=self._gemini_model,
                provider_manager=self._provider_manager,
                ruleset_store=self._ruleset_store,
            )
            if result:
                payload = result.to_dict()
                self._remember_result(signal_id, payload)
                with self._lock:
                    self._session_failing = False
                    self._failure_message = None
                if on_complete:
                    on_complete(signal, payload)
            else:
                health = self._provider_manager.health_status(self._providers_configured)
                with self._lock:
                    self._session_failing = bool(health.get("failing"))
                    self._failure_message = health.get("message")
        finally:
            with self._lock:
                self._in_flight.discard(signal_id)

    def status(self) -> dict[str, Any]:
        """Expose session-level analyst health for the dashboard."""
        with self._lock:
            failing = self._session_failing
            message = self._failure_message
        health = self._provider_manager.health_status(self._providers_configured)
        return {
            "enabled": bool(self._providers_configured),
            "failing": failing or bool(health.get("failing")),
            "message": message or health.get("message"),
            "providers": health.get("providers") or [],
        }

    def get(self, signal: dict[str, Any]) -> dict[str, Any] | None:
        event = signal.get("event") or {}
        signal_id = f"{event.get('market_id', 'unknown')}@{signal.get('detected_at', '')}"
        with self._lock:
            payload = self._cache.get(signal_id)
            if payload is None:
                return None
            self._cache.move_to_end(signal_id)
            return payload

    def pending(self, signal: dict[str, Any]) -> bool:
        event = signal.get("event") or {}
        signal_id = f"{event.get('market_id', 'unknown')}@{signal.get('detected_at', '')}"
        with self._lock:
            return signal_id in self._in_flight


def _build_tuning_prompt(signals: list[dict[str, Any]]) -> str:
    lines = []
    for sig in signals[:20]:
        event = sig.get("event") or {}
        analyst = sig.get("analyst") or {}
        lines.append(
            f"- {event.get('market_id')} | tier={sig.get('tier')} score={sig.get('score')} "
            f"yes={event.get('yes_price')} volΔ={sig.get('volume_delta')} priceΔ={sig.get('price_move')} "
            f"analyst={analyst.get('noise_or_signal')}/{analyst.get('direction')}/{analyst.get('confidence')} "
            f"note={analyst.get('threshold_note', 'none')}"
        )

    return f"""You are a tuning advisor for a prediction-market spike detector.
You are looking across recent signals that already have analyst labels.
Your goal is to reduce false positives without muting genuinely informative flow.

CURRENT THRESHOLDS
- spike_min_volume_delta: minimum volume delta to trigger detection
- spike_min_price_move: minimum fractional price move (e.g. 0.03 = 3%)
- spike_score_threshold: minimum combined score to emit a signal

RECENT SIGNALS
{chr(10).join(lines)}

Return JSON only, no markdown. Include suggested_thresholds only when you have a concrete
numeric recommendation; omit a key (or set it to null) when you have no specific suggestion.

Also propose durable ANALYST RULES: natural-language judgment rules the signal analyst will
apply when labelling future signals (e.g. proportionality rules, follow-through requirements,
topic-specific cautions). These capture insights that go beyond the three numeric thresholds.
Each rule needs a `scope` so it only loads for relevant signals:
  - topic: one of all|crypto|macro|elections|sports|geopolitics|general
  - tier:  one of all|watch|notable|signal
Use topic/tier "all" unless the rule is clearly specific. Return [] when you have no durable
rule to add. Keep each rule text self-contained and unambiguous.
{{
  "summary": "<1-2 sentence summary of the current false-positive pattern>",
  "global_recommendation": "<single best next threshold or rule change>",
  "recommendations": [
    "<short concrete tweak 1>",
    "<short concrete tweak 2>",
    "<short concrete tweak 3>"
  ],
  "suggested_thresholds": {{
    "min_volume_delta": <float or null>,
    "min_price_move": <float or null>,
    "score_threshold": <float or null>
  }},
  "proposed_rules": [
    {{ "text": "<durable analyst judgment rule>", "scope": {{ "topic": "all", "tier": "all" }} }}
  ]
}}
"""


def _normalize_proposed_rules(raw: Any, *, limit: int = 5) -> list[dict[str, Any]]:
    """Coerce the LLM's ``proposed_rules`` into clean {text, scope} dicts.

    Tolerant of malformed output: skips items without usable text, clamps scope
    to the known topic/tier vocabulary (defaulting to 'all'), and caps the count.
    Never raises — bad structure yields an empty list.
    """
    from .ruleset import VALID_TOPICS, VALID_TIERS

    if not isinstance(raw, list):
        return []
    out: list[dict[str, Any]] = []
    for item in raw:
        if not isinstance(item, dict):
            continue
        text = str(item.get("text", "")).strip()
        if not text:
            continue
        scope_in = item.get("scope") if isinstance(item.get("scope"), dict) else {}
        topic = str(scope_in.get("topic", "all")).strip().lower()
        tier = str(scope_in.get("tier", "all")).strip().lower()
        out.append({
            "text": text,
            "scope": {
                "topic": topic if topic in VALID_TOPICS else "all",
                "tier": tier if tier in VALID_TIERS else "all",
            },
        })
        if len(out) >= limit:
            break
    return out


def analyze_tuning(
    signals: list[dict[str, Any]],
    anthropic_keys: list[str] | str | None = None,
    perplexity_keys: list[str] | str | None = None,
    openai_keys: list[str] | str | None = None,
    xai_keys: list[str] | str | None = None,
    gemini_keys: list[str] | str | None = None,
    anthropic_model: str = "claude-haiku-4-5",
    perplexity_model: str = "sonar",
    openai_model: str = "gpt-4o-mini",
    xai_model: str = "grok-2-1212",
    gemini_model: str = "gemini-2.5-flash",
    provider_manager: AIProviderManager | None = None,
) -> TuningAdvice | None:
    prompt = _build_tuning_prompt(signals)
    providers: list[tuple[str, Callable[[], str]]] = []

    def _as_list(value: list[str] | str | None) -> list[str]:
        if not value:
            return []
        return value if isinstance(value, list) else [value]

    for idx, key in enumerate(_as_list(anthropic_keys)):
        providers.append((f"anthropic-key-{idx+1}", lambda k=key: _analyze_via_anthropic(prompt, k, anthropic_model)))
    for idx, key in enumerate(_as_list(perplexity_keys)):
        providers.append((f"perplexity-key-{idx+1}", lambda k=key: _analyze_via_perplexity(prompt, k, perplexity_model)))
    for idx, key in enumerate(_as_list(openai_keys)):
        providers.append((f"openai-key-{idx+1}", lambda k=key: _analyze_via_openai_compatible(prompt, k, openai_model, "https://api.openai.com")))
    for idx, key in enumerate(_as_list(xai_keys)):
        providers.append((f"xai-key-{idx+1}", lambda k=key: _analyze_via_openai_compatible(prompt, k, xai_model, "https://api.x.ai")))
    for idx, key in enumerate(_as_list(gemini_keys)):
        providers.append((f"gemini-key-{idx+1}", lambda k=key: _analyze_via_openai_compatible(prompt, k, gemini_model, "https://generativelanguage.googleapis.com/v1beta/openai")))

    last_error = None
    ordered_providers = (
        provider_manager.get_ordered_providers(providers)
        if provider_manager else providers
    )

    for provider_name, call in ordered_providers:
        try:
            raw = call()
            data = _parse_json_response(raw)
            log.info("tuning-advisor[%s]: generated", provider_name)

            if provider_manager:
                provider_manager.report_success(provider_name)

            recs = data.get("recommendations") or []
            suggested = data.get("suggested_thresholds") or {}

            def _opt_float(key: str) -> float | None:
                v = suggested.get(key)
                try:
                    return float(v) if v is not None else None
                except (TypeError, ValueError):
                    return None

            return TuningAdvice(
                summary=str(data.get("summary", "")),
                global_recommendation=str(data.get("global_recommendation", "")),
                recommendations=[str(x) for x in recs[:5]],
                suggested_min_volume_delta=_opt_float("min_volume_delta"),
                suggested_min_price_move=_opt_float("min_price_move"),
                suggested_score_threshold=_opt_float("score_threshold"),
                proposed_rules=_normalize_proposed_rules(data.get("proposed_rules")),
            )
        except Exception as exc:
            log.warning("tuning-advisor[%s]: failed: %s", provider_name, exc)
            if provider_manager:
                provider_manager.report_failure(provider_name, exc)
            last_error = exc
            continue

    if last_error:
        log.warning("tuning-advisor: all providers failed, last error: %s", last_error)
    return None


def _persist_tuning_snapshot(payload: dict[str, Any]) -> tuple[str | None, dict[str, Any]]:
    """Append a new advisor snapshot to docs/TUNING-BACKLOG.md with real TB ids.
    Returns (first_tb_id, updated_payload_with_tb_ids)."""
    try:
        from .config import TUNING_BACKLOG_PATH
        existing = TUNING_BACKLOG_PATH.read_text(encoding="utf-8") if TUNING_BACKLOG_PATH.exists() else ""

        # Find current highest TB number so we assign the next ones sequentially.
        existing_ids = [int(m) for m in re.findall(r"TB-(\d+)", existing)]
        next_tb = max(existing_ids, default=0) + 1

        today = datetime.now(UTC).strftime("%Y-%m-%d")
        summary = payload.get("summary", "")
        global_rec = payload.get("global_recommendation", "")
        recs = payload.get("recommendations") or []
        suggested = payload.get("suggested_thresholds") or {}

        is_conflict = payload.get("conflict")
        conflict_reason = payload.get("conflict_reason")
        status_label = "rejected" if is_conflict else "planned"

        # Build recommendation bullet lines with sequential TB ids.
        rec_lines = []
        tb_ids = []
        for i, rec in enumerate(recs):
            tb = f"TB-{next_tb + i:03d}"
            tb_ids.append(tb)
            rec_line = f"- [ ] **{tb}** `{status_label}` — {rec}"
            if is_conflict:
                rec_line += f"\n  - **Governor rejection**: {conflict_reason}"
            rec_lines.append(rec_line)

        first_tb = tb_ids[0] if tb_ids else f"TB-{next_tb:03d}"
        next_tb += len(recs)

        # Build suggested threshold note if present.
        threshold_note = ""
        if suggested:
            parts = [f"`{k}` → `{v}`" for k, v in suggested.items() if v is not None]
            if parts:
                threshold_note = f"\n### Suggested thresholds\n" + ", ".join(parts) + "\n"

        snapshot_count = len(re.findall(r"^## \d{4}-\d{2}-\d{2}", existing, re.MULTILINE))
        label_ord = 65 + snapshot_count  # A=65
        snapshot_label = chr(label_ord) if label_ord <= 90 else str(snapshot_count + 1)

        block = f"""
## {today} — Advisor snapshot {snapshot_label}

### Summary
{summary}

### Next step
{global_rec}
{threshold_note}
### Recommendations

{chr(10).join(rec_lines)}

---
"""
        # Update header date and append block.
        updated = re.sub(r"Last updated: \d{4}-\d{2}-\d{2}", f"Last updated: {today}", existing, count=1)
        # Insert before the Applied changes section if present, otherwise append.
        applied_marker = "## Applied changes"
        if applied_marker in updated:
            updated = updated.replace(applied_marker, block + applied_marker, 1)
        else:
            updated = updated + block

        TUNING_BACKLOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        TUNING_BACKLOG_PATH.write_text(updated, encoding="utf-8")
        log.info("tuning advisor: persisted snapshot to %s (first=%s)", TUNING_BACKLOG_PATH, first_tb)
        return first_tb, {**payload, "tb_id": first_tb, "tb_ids": tb_ids}
    except Exception as exc:
        log.warning("tuning advisor: failed to persist snapshot: %s", exc)
        return None, payload


def _rule_similarity(a: str, b: str) -> float:
    """Jaccard similarity over lowered word tokens. 0 = disjoint, 1 = identical."""
    at = set(_RULE_SIM_WORD_TOKENS_RE.findall(a.lower()))
    bt = set(_RULE_SIM_WORD_TOKENS_RE.findall(b.lower()))
    if not at and not bt:
        return 0.0
    inter = len(at & bt)
    union = len(at | bt)
    return inter / union if union else 0.0


class TuningGovernor:
    """Validates tuning advisor tweaks against historical constraints to prevent regressions."""

    def __init__(
        self,
        anthropic_keys: list[str] | str | None = None,
        perplexity_keys: list[str] | str | None = None,
        openai_keys: list[str] | str | None = None,
        xai_keys: list[str] | str | None = None,
        gemini_keys: list[str] | str | None = None,
        anthropic_key: str = "",
        perplexity_key: str = "",
        openai_key: str = "",
        xai_key: str = "",
        gemini_key: str = "",
        anthropic_model: str = "claude-haiku-4-5",
        perplexity_model: str = "sonar",
        openai_model: str = "gpt-4o-mini",
        xai_model: str = "grok-2-1212",
        gemini_model: str = "gemini-2.5-flash",
        provider_manager: AIProviderManager | None = None,
        ruleset_store: Any | None = None,
    ) -> None:
        def _coerce_keys(values):
            if not values:
                return []
            return values if isinstance(values, list) else [values]

        self._anthropic_keys = _coerce_keys(anthropic_keys) or ([anthropic_key] if anthropic_key else [])
        self._perplexity_keys = _coerce_keys(perplexity_keys) or ([perplexity_key] if perplexity_key else [])
        self._openai_keys = _coerce_keys(openai_keys) or ([openai_key] if openai_key else [])
        self._xai_keys = _coerce_keys(xai_keys) or ([xai_key] if xai_key else [])
        self._gemini_keys = _coerce_keys(gemini_keys) or ([gemini_key] if gemini_key else [])
        self._anthropic_model = anthropic_model
        self._perplexity_model = perplexity_model
        self._openai_model = openai_model
        self._xai_model = xai_model
        self._gemini_model = gemini_model
        self._provider_manager = provider_manager or AIProviderManager()
        self._lock = threading.Lock()
        self._cached_hash = ""
        self._cached_condensed = "No historical constraints."
        self._ruleset_store = ruleset_store

    def _extract_and_condense(self) -> str:
        from .config import TUNING_BACKLOG_PATH
        if not TUNING_BACKLOG_PATH.exists():
            return "No historical constraints."

        text = TUNING_BACKLOG_PATH.read_text(encoding="utf-8")
        import hashlib
        current_hash = hashlib.md5(text.encode("utf-8")).hexdigest()

        with self._lock:
            if self._cached_hash == current_hash:
                return self._cached_condensed

        lines = text.splitlines()
        extracted = []
        capture = False
        for line in lines:
            if line.startswith("- [") and ("`applied`" in line or "`rejected`" in line):
                extracted.append(line.strip())
                capture = True
            elif capture and line.startswith("  -"):
                extracted.append(line.strip())
            elif line.strip() == "" or line.startswith("- ["):
                capture = False

        raw_text = "\n".join(extracted)
        if not raw_text.strip():
            condensed = "No historical constraints."
        else:
            prompt = (
                "You are the Tuning Governor. Extract and condense these historical applied and rejected "
                "tuning rules into a dense list of active constraints. Return ONLY a markdown bulleted list. Do NOT use JSON.\n\n"
                f"RAW:\n{raw_text}"
            )
            providers = []
            for idx, key in enumerate(self._anthropic_keys):
                providers.append((f"anthropic-key-{idx+1}", lambda p=prompt, k=key: _analyze_via_anthropic(p, k, self._anthropic_model)))
            for idx, key in enumerate(self._perplexity_keys):
                providers.append((f"perplexity-key-{idx+1}", lambda p=prompt, k=key: _analyze_via_perplexity(p, k, self._perplexity_model)))
            for idx, key in enumerate(self._openai_keys):
                providers.append((f"openai-key-{idx+1}", lambda p=prompt, k=key: _analyze_via_openai_compatible(p, k, self._openai_model, "https://api.openai.com")))
            for idx, key in enumerate(self._xai_keys):
                providers.append((f"xai-key-{idx+1}", lambda p=prompt, k=key: _analyze_via_openai_compatible(p, k, self._xai_model, "https://api.x.ai")))
            for idx, key in enumerate(self._gemini_keys):
                providers.append((f"gemini-key-{idx+1}", lambda p=prompt, k=key: _analyze_via_openai_compatible(p, k, self._gemini_model, "https://generativelanguage.googleapis.com/v1beta/openai")))

            ordered_providers = self._provider_manager.get_ordered_providers(providers)
            condensed = raw_text
            for name, call in ordered_providers:
                try:
                    res_raw = call()
                    res_text = res_raw.strip()
                    if "```" in res_text:
                        res_text = res_text.split("```")[1]
                        if res_text.startswith("markdown"):
                            res_text = res_text[8:].strip()
                        elif res_text.startswith("text"):
                            res_text = res_text[4:].strip()

                    if res_text:
                        condensed = res_text

                    self._provider_manager.report_success(name)
                    break
                except Exception as e:
                    log.warning("tuning-governor-condense[%s]: failed: %s", name, e)
                    self._provider_manager.report_failure(name, e)

        with self._lock:
            self._cached_hash = current_hash
            self._cached_condensed = condensed
        return condensed

    def _ruleset_conflicts(self, advice: TuningAdvice) -> tuple[bool, str | None]:
        store = self._ruleset_store
        if store is None:
            return False, None
        try:
            active = store.active_rules()
        except Exception:
            return False, None
        if not active:
            return False, None
        proposed = advice.to_dict().get("proposed_rules") or []
        for pr in proposed:
            text = (pr.get("text") if isinstance(pr, dict) else None) or ""
            if not text:
                continue
            for rule in active:
                sim = _rule_similarity(text, rule.text)
                if sim >= _RULE_SIM_JACCARD_THRESHOLD:
                    return True, (
                        f"Proposed rule conflicts with active rule {rule.id} "
                        f"(Jaccard={sim:.0%} over rule text). "
                        f"Active rule: \"{rule.text}\". "
                        f"If the new rule improves on it, supersede {rule.id} explicitly."
                    )
        return False, None

    def review(self, advice: TuningAdvice) -> tuple[bool, str | None]:
        rule_conflict, rule_reason = self._ruleset_conflicts(advice)
        if rule_conflict:
            return True, rule_reason

        condensed_rules = self._extract_and_condense()
        if condensed_rules == "No historical constraints.":
            return False, None

        prompt = f"""You are the Tuning Governor for a spike detector.
Your job is to prevent regressions by verifying that a proposed new tuning tweak does not conflict with historical constraints.

HISTORICAL CONSTRAINTS (Applied or explicitly Rejected previously):
{condensed_rules}

PROPOSED NEW TWEAK:
Summary: {advice.summary}
Recommendation: {advice.global_recommendation}
Suggested thresholds:
  min_volume_delta: {advice.suggested_min_volume_delta}
  min_price_move: {advice.suggested_min_price_move}
  score_threshold: {advice.suggested_score_threshold}

Does the proposed tweak conflict with the historical constraints? (e.g. relaxing a threshold that was explicitly tightened to fix noise).
Return ONLY JSON:
{{
  "conflict": true or false,
  "reason": "If conflict is true, explain exactly which TB-XXX rule is violated and why. Otherwise null."
}}"""
        providers = []
        for idx, key in enumerate(self._anthropic_keys):
            providers.append((f"anthropic-key-{idx+1}", lambda p=prompt, k=key: _analyze_via_anthropic(p, k, self._anthropic_model)))
        for idx, key in enumerate(self._perplexity_keys):
            providers.append((f"perplexity-key-{idx+1}", lambda p=prompt, k=key: _analyze_via_perplexity(p, k, self._perplexity_model)))
        for idx, key in enumerate(self._openai_keys):
            providers.append((f"openai-key-{idx+1}", lambda p=prompt, k=key: _analyze_via_openai_compatible(p, k, self._openai_model, "https://api.openai.com")))
        for idx, key in enumerate(self._xai_keys):
            providers.append((f"xai-key-{idx+1}", lambda p=prompt, k=key: _analyze_via_openai_compatible(p, k, self._xai_model, "https://api.x.ai")))
        for idx, key in enumerate(self._gemini_keys):
            providers.append((f"gemini-key-{idx+1}", lambda p=prompt, k=key: _analyze_via_openai_compatible(p, k, self._gemini_model, "https://generativelanguage.googleapis.com/v1beta/openai")))

        ordered_providers = self._provider_manager.get_ordered_providers(providers)
        for name, call in ordered_providers:
            try:
                raw_res = call()
                data = _parse_json_response(raw_res)
                log.info("tuning-governor[%s]: generated", name)

                self._provider_manager.report_success(name)

                is_conflict = bool(data.get("conflict"))
                reason = data.get("reason")
                return is_conflict, (str(reason) if reason else None)
            except Exception as e:
                log.warning("tuning-governor[%s]: failed: %s", name, e)
                self._provider_manager.report_failure(name, e)

        return False, None


def _advice_content_signature(payload: dict[str, Any]) -> str:
    """Stable fingerprint of a tuning snapshot's substance (ignores timestamps
    and TB ids) so repeated identical advice is not persisted twice."""
    content = {
        key: payload.get(key)
        for key in (
            "summary",
            "global_recommendation",
            "recommendations",
            "suggested_thresholds",
            "proposed_rules",
            "conflict",
        )
    }
    return json.dumps(content, sort_keys=True, default=str)


class TuningAdvisor:
    """Background second-pass advisor over analyst-labelled signals."""

    def __init__(
        self,
        anthropic_keys: list[str] | str | None = None,
        perplexity_keys: list[str] | str | None = None,
        openai_keys: list[str] | str | None = None,
        xai_keys: list[str] | str | None = None,
        gemini_keys: list[str] | str | None = None,
        anthropic_key: str = "",
        perplexity_key: str = "",
        openai_key: str = "",
        xai_key: str = "",
        gemini_key: str = "",
        anthropic_model: str = "claude-haiku-4-5",
        perplexity_model: str = "sonar",
        openai_model: str = "gpt-4o-mini",
        xai_model: str = "grok-2-1212",
        gemini_model: str = "gemini-2.5-flash",
        provider_manager: AIProviderManager | None = None,
        ruleset_store: Any | None = None,
        min_interval_seconds: float = DEFAULT_TUNING_ADVISOR_INTERVAL_SECONDS,
    ) -> None:
        def _coerce_keys(values):
            if not values:
                return []
            return values if isinstance(values, list) else [values]

        self._anthropic_keys = _coerce_keys(anthropic_keys) or ([anthropic_key] if anthropic_key else [])
        self._perplexity_keys = _coerce_keys(perplexity_keys) or ([perplexity_key] if perplexity_key else [])
        self._openai_keys = _coerce_keys(openai_keys) or ([openai_key] if openai_key else [])
        self._xai_keys = _coerce_keys(xai_keys) or ([xai_key] if xai_key else [])
        self._gemini_keys = _coerce_keys(gemini_keys) or ([gemini_key] if gemini_key else [])
        self._anthropic_model = anthropic_model
        self._perplexity_model = perplexity_model
        self._openai_model = openai_model
        self._xai_model = xai_model
        self._gemini_model = gemini_model
        self._provider_manager = provider_manager or AIProviderManager()
        self._lock = threading.Lock()
        self._in_flight = False
        self._cache: dict[str, Any] | None = None
        self._last_signature = ""
        self._min_interval_seconds = float(min_interval_seconds)
        self._last_run_at: float | None = None
        self._ruleset_store = ruleset_store
        self._governor = TuningGovernor(
            anthropic_keys=self._anthropic_keys,
            perplexity_keys=self._perplexity_keys,
            openai_keys=self._openai_keys,
            xai_keys=self._xai_keys,
            gemini_keys=self._gemini_keys,
            anthropic_model=anthropic_model,
            perplexity_model=perplexity_model,
            openai_model=openai_model,
            xai_model=xai_model,
            gemini_model=gemini_model,
            provider_manager=self._provider_manager,
            ruleset_store=self._ruleset_store,
        )

    def maybe_enqueue(self, signals: list[dict[str, Any]]) -> None:
        analyzed = [s for s in signals if s.get("analyst") and not s.get("analyst", {}).get("pending")]
        if len(analyzed) < 2:
            return
        signature = "|".join(
            f"{(s.get('event') or {}).get('market_id')}@{s.get('detected_at')}:{(s.get('analyst') or {}).get('noise_or_signal')}"
            for s in analyzed[:12]
        )
        now = time.monotonic()
        with self._lock:
            if self._in_flight or signature == self._last_signature:
                return
            if (
                self._last_run_at is not None
                and now - self._last_run_at < self._min_interval_seconds
            ):
                return
            self._in_flight = True
            self._last_signature = signature
            self._last_run_at = now
        t = threading.Thread(target=self._run, args=(analyzed[:20],), daemon=True, name="tuning-advisor")
        t.start()

    def _run(self, signals: list[dict[str, Any]]) -> None:
        try:
            result = analyze_tuning(
                signals,
                anthropic_keys=self._anthropic_keys,
                perplexity_keys=self._perplexity_keys,
                openai_keys=self._openai_keys,
                xai_keys=self._xai_keys,
                gemini_keys=self._gemini_keys,
                anthropic_model=self._anthropic_model,
                perplexity_model=self._perplexity_model,
                openai_model=self._openai_model,
                xai_model=self._xai_model,
                gemini_model=self._gemini_model,
                provider_manager=self._provider_manager,
            )
            if result:
                is_conflict, reason = self._governor.review(result)
                if is_conflict:
                    result.conflict = True
                    result.conflict_reason = reason

                payload = result.to_dict()
                with self._lock:
                    previous = self._cache
                if previous is not None and _advice_content_signature(previous) == _advice_content_signature(payload):
                    # Same substance as the last snapshot — refresh the cache
                    # timestamp but do not append a duplicate to the backlog.
                    log.info("tuning advisor: advice unchanged, skipping snapshot persist")
                    with self._lock:
                        self._cache = {**previous, "generated_at": payload["generated_at"]}
                else:
                    _tb_id, enriched = _persist_tuning_snapshot(payload)
                    with self._lock:
                        self._cache = enriched
        finally:
            with self._lock:
                self._in_flight = False

    def get(self) -> dict[str, Any] | None:
        with self._lock:
            return dict(self._cache) if self._cache else None

    def pending(self) -> bool:
        with self._lock:
            return self._in_flight
