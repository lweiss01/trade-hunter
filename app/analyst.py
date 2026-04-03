"""
Signal analyst — uses Claude to interpret spike signals in the context of
prediction market flow and surface high-confidence actionable reads.
"""
from __future__ import annotations

import logging
import os
import threading
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

log = logging.getLogger(__name__)


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

    prompt = f"""You are a prediction market analyst. A spike detector has flagged unusual activity on a Kalshi market.

MARKET
  ID: {market_id}
  Question (title): {title}
  Current yes price: {f'{yes_price:.3f} ({yes_price*100:.1f}% implied probability)' if yes_price is not None else 'unknown'}

SPIKE DETAILS
  Score: {score} (tier: {tier})
  Volume delta: {volume_delta:,.0f} vs baseline {baseline:,.0f} ({f'{volume_delta/baseline:.1f}x' if baseline else 'n/a'} baseline)
  Price move: {f'{price_move*100:.1f}%' if price_move is not None else 'n/a'}
  Detector reason: {reason}

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
    generated_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def to_dict(self) -> dict[str, Any]:
        return {
            "summary": self.summary,
            "global_recommendation": self.global_recommendation,
            "recommendations": self.recommendations,
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
        self._cache: dict[str, dict[str, Any]] = {}
        self._lock = threading.Lock()
        self._in_flight: set[str] = set()

        providers = []
        if anthropic_key:
            providers.append(f"anthropic/{anthropic_model}")
        if perplexity_key:
            providers.append(f"perplexity/{perplexity_model}")
        log.info("signal analyst ready, providers: %s", " → ".join(providers) or "none")

    def enqueue(self, signal: dict[str, Any], recent_flow: list[dict[str, Any]]) -> None:
        """Fire-and-forget: analyze signal in background thread."""
        event = signal.get("event") or {}
        signal_id = f"{event.get('market_id', 'unknown')}@{signal.get('detected_at', '')}"

        with self._lock:
            if signal_id in self._cache or signal_id in self._in_flight:
                return
            self._in_flight.add(signal_id)

        t = threading.Thread(
            target=self._run,
            args=(signal_id, signal, list(recent_flow)),
            daemon=True,
            name=f"analyst-{signal_id[:30]}",
        )
        t.start()

    def _run(self, signal_id: str, signal: dict, flow: list) -> None:
        try:
            result = analyze_signal(
                signal, flow,
                anthropic_key=self._anthropic_key,
                perplexity_key=self._perplexity_key,
                anthropic_model=self._anthropic_model,
                perplexity_model=self._perplexity_model,
            )
            if result:
                with self._lock:
                    self._cache[signal_id] = result.to_dict()
        finally:
            with self._lock:
                self._in_flight.discard(signal_id)

    def get(self, signal: dict[str, Any]) -> dict[str, Any] | None:
        event = signal.get("event") or {}
        signal_id = f"{event.get('market_id', 'unknown')}@{signal.get('detected_at', '')}"
        with self._lock:
            return self._cache.get(signal_id)

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

RECENT SIGNALS
{chr(10).join(lines)}

Return JSON only, no markdown:
{{
  "summary": "<1-2 sentence summary of the current false-positive pattern>",
  "global_recommendation": "<single best next threshold or rule change>",
  "recommendations": [
    "<short concrete tweak 1>",
    "<short concrete tweak 2>",
    "<short concrete tweak 3>"
  ]
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
            return TuningAdvice(
                summary=str(data.get("summary", "")),
                global_recommendation=str(data.get("global_recommendation", "")),
                recommendations=[str(x) for x in recs[:5]],
            )
        except Exception as exc:
            log.warning("tuning-advisor[%s]: failed: %s", provider_name, exc)
            last_error = exc
            continue

    if last_error:
        log.warning("tuning-advisor: all providers failed, last error: %s", last_error)
    return None


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
                with self._lock:
                    self._cache = result.to_dict()
        finally:
            with self._lock:
                self._in_flight = False

    def get(self) -> dict[str, Any] | None:
        with self._lock:
            return dict(self._cache) if self._cache else None

    def pending(self) -> bool:
        with self._lock:
            return self._in_flight
