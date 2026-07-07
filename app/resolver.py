"""Kalshi settlement resolver (Phase 5).

Periodically polls the Kalshi public API for the settlement of markets that have
an unresolved signal in the eval log, and writes the resolution row so the signal
becomes scorable. Reads pending signals from the eval log itself (not the events
table) because event retention deletes rows long before some markets settle.

Never crashes the app: every network/parse failure degrades to "not resolved
yet" and is retried on the next pass.
"""
from __future__ import annotations

import json
import logging
import threading
import urllib.request
from typing import Any

from .eval import EvalLogger

log = logging.getLogger(__name__)

_KALSHI_MARKET_URL = "https://api.elections.kalshi.com/trade-api/v2/markets/{ticker}"
DEFAULT_POLL_SECONDS = 1800  # 30 minutes

# Kalshi market statuses that carry a final outcome. The elections API uses
# "finalized" for fully-settled markets and "determined" for markets whose
# outcome is decided but settlement is still processing — both expose a stable
# `result`. "settled" is included for forward-compat / other endpoints. Verified
# against the live API 2026-07-07: the resolver previously only accepted "settled"
# and so captured ZERO of ~85 resolved markets.
_RESOLVED_STATUSES = frozenset({"settled", "finalized", "determined"})


def fetch_market_outcome(ticker: str, *, timeout: float = 8.0) -> int | str | None:
    """Return 1 (YES), 0 (NO), "void", or None if not yet resolved / unreachable.

    A resolved market with no yes/no result (cancelled/voided) maps to "void".
    """
    url = _KALSHI_MARKET_URL.format(ticker=urllib.request.quote(str(ticker), safe=""))
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "trade-hunter/1.0"})
        with urllib.request.urlopen(req, timeout=timeout) as response:
            data = json.loads(response.read().decode("utf-8") or "{}")
    except Exception as exc:  # network error, 404, bad JSON — try again next pass
        log.debug("resolver: fetch failed for %s: %s", ticker, exc)
        return None

    market = data.get("market") if isinstance(data, dict) else None
    if not isinstance(market, dict):
        return None
    if str(market.get("status") or "").lower() not in _RESOLVED_STATUSES:
        return None
    result = str(market.get("result") or "").strip().lower()
    if result == "yes":
        return 1
    if result == "no":
        return 0
    return "void"  # resolved but not a clean yes/no → dropped by the scorer


class SettlementResolver:
    """Background thread that resolves pending eval-log signals against Kalshi."""

    def __init__(self, eval_logger: EvalLogger, *, poll_seconds: float = DEFAULT_POLL_SECONDS) -> None:
        self._eval = eval_logger
        self._poll_seconds = poll_seconds
        self._stop = threading.Event()
        self._thread: threading.Thread | None = None

    def start(self) -> None:
        self._stop.clear()
        self._thread = threading.Thread(target=self._loop, name="settlement-resolver", daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._stop.set()
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=2.0)
        self._thread = None

    def _loop(self) -> None:
        # Initial soak so startup isn't slowed by an immediate network sweep.
        if self._stop.wait(timeout=min(30.0, self._poll_seconds)):
            return
        while not self._stop.is_set():
            try:
                self.poll_once()
            except Exception as exc:  # a bad pass must never kill the thread
                log.warning("resolver: poll failed: %s", exc)
            self._stop.wait(timeout=self._poll_seconds)

    def poll_once(self) -> int:
        """One resolution sweep. Returns the number of markets resolved."""
        resolved = 0
        # De-dupe by market: multiple pending signals can share a ticker, but the
        # first-signal-per-market policy means there is at most one open per market.
        for sig in self._eval.log.pending_signals():
            if self._stop.is_set():
                break
            market_id = str(sig.get("market_id") or "")
            signal_event_id = sig.get("event_id")
            if not market_id or not signal_event_id:
                continue
            outcome = fetch_market_outcome(market_id)
            if outcome is None:
                continue
            try:
                self._eval.log.log_resolution(
                    signal_event_id=signal_event_id,
                    market_id=market_id,
                    outcome=outcome,
                )
                self._eval.mark_resolved(market_id)
                resolved += 1
                log.info("resolver: %s settled → %s", market_id, outcome)
            except Exception as exc:
                log.warning("resolver: failed to log resolution for %s: %s", market_id, exc)
        return resolved
