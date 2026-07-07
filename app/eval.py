"""Analyst-accuracy evaluation logging (Phase 5).

Bridges the running app to the hash-chained ``signal_log.SignalLog``: when the
analyst produces a probability for a live Kalshi signal, freeze that view (agent
probability + the market's bid/ask at T) into the eval log. A separate resolver
(``app.resolver``) later writes settlement rows, and ``score.py`` joins the two.

Scope is deliberate and matches ``EVAL_PREREGISTRATION.md``:
  - Live Kalshi signals only. Simulation markets never settle, and the resolver
    only knows how to query Kalshi, so nothing else is scorable.
  - First unresolved signal per market only. The same market can spike many times
    before it settles; logging each one would over-weight noisy markets in the
    aggregate. Once a market has an open (unresolved) signal in the log it is not
    re-logged until it resolves.
"""
from __future__ import annotations

import logging
import threading
from typing import Any, Callable

from signal_log import SignalLog

log = logging.getLogger(__name__)

_CONFIDENCE_TO_FLOAT = {"low": 0.25, "medium": 0.5, "high": 0.75}
# Synthetic sources never reach a real Kalshi settlement, so logging them would
# leave permanently-pending rows (e.g. the smoke test's "smoke-btc"). Excluded.
_SYNTHETIC_SOURCES = {"simulation", "demo-button", "smoke-test", "test", "manual"}


def _to_cents(dollars: Any) -> int | None:
    """Convert a dollar price (0.0–1.0) to int cents (0–100), or None."""
    if dollars is None:
        return None
    try:
        cents = int(round(float(dollars) * 100))
    except (TypeError, ValueError):
        return None
    return max(0, min(100, cents))


def _log_ts(detected_at: Any) -> str | None:
    """Normalize an ISO signal timestamp to the log's canonical UTC format so
    status.py can age it. Returns None (log uses now) on unparseable input."""
    if not detected_at:
        return None
    from datetime import datetime, timezone

    try:
        dt = datetime.fromisoformat(str(detected_at).replace("Z", "+00:00"))
    except ValueError:
        return None
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


class EvalLogger:
    """Thread-safe front door to the eval log with the first-signal-per-market
    policy. Never raises to the caller — a logging failure must not disturb the
    analyst callback."""

    def __init__(self, log_path: Any, agent_version_fn: Callable[[], str]) -> None:
        self._log = SignalLog(log_path)
        self._agent_version_fn = agent_version_fn
        self._lock = threading.Lock()
        # Markets that already have an unresolved signal in the log (rebuilt from
        # disk so the policy survives restarts).
        self._open_markets: set[str] = self._log.pending_market_ids()

    @property
    def log(self) -> SignalLog:
        return self._log

    def maybe_log(self, signal: dict[str, Any], analyst: dict[str, Any]) -> str | None:
        """Log this signal if it is a live Kalshi signal with a probability and
        the market is not already open. Returns the event_id logged, or None."""
        try:
            event = signal.get("event") or {}
            if str(event.get("platform") or "").lower() != "kalshi":
                return None
            if not event.get("live"):
                return None
            if str(event.get("source") or "").lower() in _SYNTHETIC_SOURCES:
                return None
            probability = analyst.get("probability_yes")
            if probability is None:
                return None
            market_id = str(event.get("market_id") or "").strip()
            if not market_id:
                return None

            meta = event.get("metadata") or {}
            bid = _to_cents(meta.get("yes_bid"))
            ask = _to_cents(meta.get("yes_ask"))
            last = _to_cents(event.get("yes_price"))
            if bid is None and ask is None and last is None:
                # kalshi_price benchmark needs at least one market price at T.
                return None

            direction = str(analyst.get("direction") or "").lower()
            action = "buy_yes" if direction == "yes" else "buy_no" if direction == "no" else None
            confidence = _CONFIDENCE_TO_FLOAT.get(str(analyst.get("confidence") or "").lower())

            with self._lock:
                if market_id in self._open_markets:
                    return None
                event_id = self._log.log_signal(
                    market_id=market_id,
                    agent_prob=float(probability),
                    agent_action=action,
                    benchmark_type="kalshi_price",
                    market_yes_bid=bid,
                    market_yes_ask=ask,
                    market_yes_price=last,
                    market_title=str(event.get("title") or market_id),
                    category=(signal.get("topic") or event.get("topic")),
                    agent_confidence=confidence,
                    agent_version=self._agent_version_fn(),
                    ts_signal=_log_ts(signal.get("detected_at")),
                )
                self._open_markets.add(market_id)
                return event_id
        except Exception as exc:  # never break the analyst callback
            log.warning("eval log: failed to record signal: %s", exc)
            return None

    def mark_resolved(self, market_id: str) -> None:
        with self._lock:
            self._open_markets.discard(market_id)

    def status(self) -> dict[str, Any]:
        """Accrual snapshot for the dashboard (read-only)."""
        try:
            pairs = self._log.load_scored_pairs()
            pending = self._log.pending_signals()
            return {
                "enabled": True,
                "chain_ok": self._log.verify_chain(),
                "resolved_scorable": len(pairs),
                "pending": len(pending),
                "gates": {"first_read": 30, "publish": 100},
            }
        except Exception as exc:
            log.warning("eval log: status read failed: %s", exc)
            return {"enabled": True, "chain_ok": None, "resolved_scorable": 0, "pending": 0,
                    "gates": {"first_read": 30, "publish": 100}}
