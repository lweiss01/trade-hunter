from __future__ import annotations

import random
import threading
import time
from datetime import UTC, datetime

from ..models import MarketEvent
from .base import FeedAdapter


class SimulatedFeed(FeedAdapter):
    name = "simulation"

    def __init__(self, emit, publish_status) -> None:
        super().__init__(emit, publish_status)
        self._thread: threading.Thread | None = None
        self._stop = threading.Event()
        self._markets = {
            "pm-fed-cut": {
                "platform": "polymarket",
                "title": "Will the Fed cut rates in June?",
                "topic": "macro",
                "price": 0.44,
                "volume": 900.0,
            },
            "kalshi-btc-110k": {
                "platform": "kalshi",
                "title": "BTC above 110k by year end",
                "topic": "crypto",
                "price": 0.39,
                "volume": 600.0,
            },
            "pm-election-texas": {
                "platform": "polymarket",
                "title": "Will Texas vote Republican in 2028?",
                "topic": "elections",
                "price": 0.71,
                "volume": 1300.0,
            },
        }

    def start(self) -> None:
        self.publish_status(self.name, {"running": True, "detail": "simulated markets active"})
        self._thread = threading.Thread(target=self._run, name="simulated-feed", daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._stop.set()
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=1)
        self.publish_status(self.name, {"running": False, "detail": "stopped"})

    def _run(self) -> None:
        while not self._stop.is_set():
            market_id = random.choice(list(self._markets.keys()))
            market = self._markets[market_id]

            drift = random.uniform(-0.015, 0.015)
            spike = random.random() < 0.18
            volume_burst = random.uniform(130, 280) if spike else random.uniform(12, 55)
            price_jump = random.uniform(0.04, 0.1) if spike else 0.0

            market["price"] = min(max(market["price"] + drift + price_jump, 0.02), 0.98)
            market["volume"] += volume_burst

            event = MarketEvent(
                source="simulation",
                platform=market["platform"],
                market_id=market_id,
                title=market["title"],
                event_kind="trade",
                yes_price=round(market["price"], 4),
                no_price=round(1 - market["price"], 4),
                volume=round(market["volume"], 2),
                volume_kind="cumulative",
                trade_size=round(volume_burst, 2),
                live=False,
                topic=market["topic"],
                timestamp=datetime.now(UTC),
                metadata={"spike": spike},
            )
            self.emit(event)
            time.sleep(1.5)
