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


def analyze_signal(
    signal: dict[str, Any],
    recent_flow: list[dict[str, Any]],
    api_key: str,
    model: str = "claude-haiku-4-5",
) -> AnalystRead | None:
    """Synchronous signal analysis. Call from a background thread."""
    try:
        import anthropic
        client = anthropic.Anthropic(api_key=api_key)
        prompt = _build_prompt(signal, recent_flow)

        msg = client.messages.create(
            model=model,
            max_tokens=512,
            messages=[{"role": "user", "content": prompt}],
        )
        raw = msg.content[0].text.strip()

        import json
        # Claude sometimes wraps JSON in markdown fences — strip them
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        raw = raw.strip()
        log.debug("analyst raw response: %s", raw[:200])
        data = json.loads(raw)

        event = signal.get("event") or {}
        signal_id = f"{event.get('market_id', 'unknown')}@{signal.get('detected_at', '')}"

        return AnalystRead(
            signal_id=signal_id,
            noise_or_signal=str(data.get("noise_or_signal", "uncertain")),
            direction=str(data.get("direction", "unclear")),
            confidence=str(data.get("confidence", "low")),
            rationale=str(data.get("rationale", "")),
            threshold_note=str(data.get("threshold_note", "none")),
        )
    except Exception as exc:
        log.warning("analyst: failed to analyze signal: %s | raw=%r", exc, locals().get('raw', '')[:200])
        return None


class SignalAnalyst:
    """Background analyst that enriches signals with LLM reads.

    Analysis runs in a daemon thread so it never blocks ingestion.
    Results are stored in a local cache keyed by signal_id and fetched
    by the dashboard via the state response.
    """

    def __init__(self, api_key: str, model: str = "claude-haiku-4-5") -> None:
        self._api_key = api_key
        self._model = model
        self._cache: dict[str, dict[str, Any]] = {}
        self._lock = threading.Lock()
        self._in_flight: set[str] = set()

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
            result = analyze_signal(signal, flow, self._api_key, self._model)
            if result:
                with self._lock:
                    self._cache[signal_id] = result.to_dict()
                log.info(
                    "analyst: %s → %s/%s/%s",
                    signal_id[:40], result.noise_or_signal,
                    result.direction, result.confidence,
                )
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
