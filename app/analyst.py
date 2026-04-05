"""
Signal analyst — uses Claude to interpret spike signals in the context of
prediction market flow and surface high-confidence actionable reads.
"""
from __future__ import annotations

import logging
import os
import pathlib
import re
import threading
from collections import OrderedDict
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any, Callable

log = logging.getLogger(__name__)

MAX_SIGNAL_ANALYST_CACHE = 500


@dataclass
class AnalystRead:
    signal_id: str                    # market_id + detected_at
    noise_or_signal: str              # "noise" | "signal" | "uncertain"
    direction: str                    # "yes" | "no" | "unclear"
    confidence: str                   # "low" | "medium" | "high"
    rationale: str                    # one-paragraph plain-English read
    threshold_note: str               # detector tuning suggestion if any
    generated_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def to_dict(self) -> dict[str, Any]:
        return {
            "noise_or_signal": self.noise_or_signal,
            "direction": self.direction,
            "confidence": self.confidence,
            "rationale": self.rationale,
            "threshold_note": self.threshold_note,
            "generated_at": self.generated_at.isoformat(),
        }


def _build_prompt(signal: dict[str, Any], recent_flow: list[dict[str, Any]]) -> str:
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

    # Recent flow for this market
    market_flow = [e for e in recent_flow if e.get("market_id") == market_id][-20:]
    prices = [e.get("yes_price") for e in market_flow if e.get("yes_price") is not None]
    trades = [e for e in market_flow if e.get("event_kind") == "trade"]
    yes_trades = sum(1 for t in trades if t.get("trade_side") == "yes")
    no_trades = sum(1 for t in trades if t.get("trade_side") == "no")
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

YOUR TASK
Interpret this signal for a trader who wants to decide whether this yes/no question is worth acting on.

Return your analysis as a JSON object with exactly these fields:
{{
  "noise_or_signal": "noise" | "signal" | "uncertain",
  "direction": "yes" | "no" | "unclear",
  "confidence": "low" | "medium" | "high",
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
    import json as _json
    import urllib.request as _ureq
    payload = _json.dumps({
        "model": model,
        "max_tokens": 512,
        "messages": [{"role": "user", "content": prompt}],
    }).encode()
    req = _ureq.Request(
        "https://api.perplexity.ai/chat/completions",
        data=payload,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
    )
    resp = _json.load(_ureq.urlopen(req, timeout=20))
    return resp["choices"][0]["message"]["content"]


def analyze_signal(
    signal: dict[str, Any],
    recent_flow: list[dict[str, Any]],
    anthropic_key: str = "",
    perplexity_key: str = "",
    anthropic_model: str = "claude-haiku-4-5",
    perplexity_model: str = "sonar",
) -> AnalystRead | None:
    """Synchronous signal analysis with provider fallback.

    Tries Anthropic first (if key present), falls back to Perplexity (if key present).
    Returns None only if both providers fail or both keys are absent.
    """
    prompt = _build_prompt(signal, recent_flow)
    event = signal.get("event") or {}
    signal_id = f"{event.get('market_id', 'unknown')}@{signal.get('detected_at', '')}"

    providers = []
    if anthropic_key:
        providers.append(("anthropic", lambda: _analyze_via_anthropic(prompt, anthropic_key, anthropic_model)))
    if perplexity_key:
        providers.append(("perplexity", lambda: _analyze_via_perplexity(prompt, perplexity_key, perplexity_model)))

    last_error = None
    for provider_name, call in providers:
        try:
            raw = call()
            log.debug("analyst[%s] raw: %s", provider_name, raw[:200])
            data = _parse_json_response(raw)
            log.info("analyst[%s]: %s → %s/%s/%s", provider_name, signal_id[:40],
                     data.get("noise_or_signal"), data.get("direction"), data.get("confidence"))
            return AnalystRead(
                signal_id=signal_id,
                noise_or_signal=str(data.get("noise_or_signal", "uncertain")),
                direction=str(data.get("direction", "unclear")),
                confidence=str(data.get("confidence", "low")),
                rationale=str(data.get("rationale", "")),
                threshold_note=str(data.get("threshold_note", "none")),
            )
        except Exception as exc:
            log.warning("analyst[%s]: failed: %s", provider_name, exc)
            last_error = exc
            continue

    if last_error:
        log.warning("analyst: all providers failed, last error: %s", last_error)
    return None


@dataclass
class TuningAdvice:
    summary: str
    global_recommendation: str
    recommendations: list[str]
    suggested_min_volume_delta: float | None = None
    suggested_min_price_move: float | None = None
    suggested_score_threshold: float | None = None
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
            "generated_at": self.generated_at.isoformat(),
        }


class SignalAnalyst:
    """Background analyst that enriches signals with LLM reads.

    Tries Anthropic first, falls back to Perplexity if Anthropic fails or is unavailable.
    Analysis runs in a daemon thread so it never blocks ingestion.
    Results are stored in a local cache keyed by signal_id.
    """

    def __init__(
        self,
        anthropic_key: str = "",
        perplexity_key: str = "",
        anthropic_model: str = "claude-haiku-4-5",
        perplexity_model: str = "sonar",
    ) -> None:
        self._anthropic_key = anthropic_key
        self._perplexity_key = perplexity_key
        self._anthropic_model = anthropic_model
        self._perplexity_model = perplexity_model
        self._cache: OrderedDict[str, dict[str, Any]] = OrderedDict()
        self._lock = threading.Lock()
        self._in_flight: set[str] = set()

        providers = []
        if anthropic_key:
            providers.append(f"anthropic/{anthropic_model}")
        if perplexity_key:
            providers.append(f"perplexity/{perplexity_model}")
        log.info("signal analyst ready, providers: %s", " → ".join(providers) or "none")

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
                anthropic_key=self._anthropic_key,
                perplexity_key=self._perplexity_key,
                anthropic_model=self._anthropic_model,
                perplexity_model=self._perplexity_model,
            )
            if result:
                payload = result.to_dict()
                self._remember_result(signal_id, payload)
                if on_complete:
                    on_complete(signal, payload)
        finally:
            with self._lock:
                self._in_flight.discard(signal_id)

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
numeric recommendation; omit a key (or set it to null) when you have no specific suggestion:
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
  }}
}}
"""


def analyze_tuning(
    signals: list[dict[str, Any]],
    anthropic_key: str = "",
    perplexity_key: str = "",
    anthropic_model: str = "claude-haiku-4-5",
    perplexity_model: str = "sonar",
) -> TuningAdvice | None:
    prompt = _build_tuning_prompt(signals)
    providers = []
    if anthropic_key:
        providers.append(("anthropic", lambda: _analyze_via_anthropic(prompt, anthropic_key, anthropic_model)))
    if perplexity_key:
        providers.append(("perplexity", lambda: _analyze_via_perplexity(prompt, perplexity_key, perplexity_model)))

    last_error = None
    for provider_name, call in providers:
        try:
            raw = call()
            data = _parse_json_response(raw)
            log.info("tuning-advisor[%s]: generated", provider_name)
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
            )
        except Exception as exc:
            log.warning("tuning-advisor[%s]: failed: %s", provider_name, exc)
            last_error = exc
            continue

    if last_error:
        log.warning("tuning-advisor: all providers failed, last error: %s", last_error)
    return None


def _persist_tuning_snapshot(payload: dict[str, Any]) -> tuple[str | None, dict[str, Any]]:
    """Append a new advisor snapshot to docs/TUNING-BACKLOG.md with real TB ids.
    Returns (first_tb_id, updated_payload_with_tb_ids)."""
    try:
        backlog_path = pathlib.Path(__file__).parent.parent / "docs" / "TUNING-BACKLOG.md"
        existing = backlog_path.read_text(encoding="utf-8") if backlog_path.exists() else ""

        # Find current highest TB number so we assign the next ones sequentially.
        existing_ids = [int(m) for m in re.findall(r"TB-(\d+)", existing)]
        next_tb = max(existing_ids, default=0) + 1

        today = datetime.now(UTC).strftime("%Y-%m-%d")
        summary = payload.get("summary", "")
        global_rec = payload.get("global_recommendation", "")
        recs = payload.get("recommendations") or []
        suggested = payload.get("suggested_thresholds") or {}

        # Build recommendation bullet lines with sequential TB ids.
        rec_lines = []
        tb_ids = []
        for i, rec in enumerate(recs):
            tb = f"TB-{next_tb + i:03d}"
            tb_ids.append(tb)
            rec_lines.append(f"- [ ] **{tb}** `planned` — {rec}")

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

        backlog_path.write_text(updated, encoding="utf-8")
        log.info("tuning advisor: persisted snapshot to %s (first=%s)", backlog_path, first_tb)
        return first_tb, {**payload, "tb_id": first_tb, "tb_ids": tb_ids}
    except Exception as exc:
        log.warning("tuning advisor: failed to persist snapshot: %s", exc)
        return None, payload


class TuningAdvisor:
    """Background second-pass advisor over analyst-labelled signals."""

    def __init__(
        self,
        anthropic_key: str = "",
        perplexity_key: str = "",
        anthropic_model: str = "claude-haiku-4-5",
        perplexity_model: str = "sonar",
    ) -> None:
        self._anthropic_key = anthropic_key
        self._perplexity_key = perplexity_key
        self._anthropic_model = anthropic_model
        self._perplexity_model = perplexity_model
        self._lock = threading.Lock()
        self._in_flight = False
        self._cache: dict[str, Any] | None = None
        self._last_signature = ""

    def maybe_enqueue(self, signals: list[dict[str, Any]]) -> None:
        analyzed = [s for s in signals if s.get("analyst") and not s.get("analyst", {}).get("pending")]
        if len(analyzed) < 2:
            return
        signature = "|".join(
            f"{(s.get('event') or {}).get('market_id')}@{s.get('detected_at')}:{(s.get('analyst') or {}).get('noise_or_signal')}"
            for s in analyzed[:12]
        )
        with self._lock:
            if self._in_flight or signature == self._last_signature:
                return
            self._in_flight = True
            self._last_signature = signature
        t = threading.Thread(target=self._run, args=(analyzed[:20],), daemon=True, name="tuning-advisor")
        t.start()

    def _run(self, signals: list[dict[str, Any]]) -> None:
        try:
            result = analyze_tuning(
                signals,
                anthropic_key=self._anthropic_key,
                perplexity_key=self._perplexity_key,
                anthropic_model=self._anthropic_model,
                perplexity_model=self._perplexity_model,
            )
            if result:
                payload = result.to_dict()
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
