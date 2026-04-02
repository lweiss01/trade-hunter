from __future__ import annotations

from collections import deque
from threading import Lock
from typing import Any

from .models import MarketEvent, SpikeSignal


class MarketStore:
    def __init__(self) -> None:
        self._lock = Lock()
        self._latest_by_market: dict[str, MarketEvent] = {}
        self._recent_events: deque[MarketEvent] = deque(maxlen=120)
        self._signals: deque[SpikeSignal] = deque(maxlen=100)
        self._feed_status: dict[str, dict[str, Any]] = {}

    def upsert_event(self, event: MarketEvent) -> None:
        with self._lock:
            self._latest_by_market[event.market_id] = event
            self._recent_events.appendleft(event)

    def record_signal(self, signal: SpikeSignal) -> None:
        with self._lock:
            self._signals.appendleft(signal)

    def update_feed_status(self, name: str, payload: dict[str, Any]) -> None:
        with self._lock:
            self._feed_status[name] = payload

    def dashboard_state(self) -> dict[str, Any]:
        with self._lock:
            markets = sorted(
                self._latest_by_market.values(),
                key=lambda item: item.timestamp,
                reverse=True,
            )
            activity = list(self._recent_events)
            live_events = sum(1 for item in activity if item.live)
            trade_events = sum(1 for item in activity if item.event_kind == "trade")
            source_counts: dict[str, int] = {}
            for item in activity:
                source_counts[item.source] = source_counts.get(item.source, 0) + 1
            return {
                "markets": [item.to_dict() for item in markets[:50]],
                "activity": [item.to_dict() for item in activity[:24]],
                "signals": [item.to_dict() for item in list(self._signals)[:25]],
                "feeds": dict(self._feed_status),
                "summary": {
                    "live_events": live_events,
                    "trade_events": trade_events,
                    "sources": source_counts,
                },
            }
