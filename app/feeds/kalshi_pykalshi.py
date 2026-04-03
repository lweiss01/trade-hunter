from __future__ import annotations

import asyncio
import logging
import threading
from datetime import UTC, datetime

from ..config import Settings
from ..models import MarketEvent
from .base import FeedAdapter

log = logging.getLogger(__name__)


class KalshiPykalshiFeed(FeedAdapter):
    name = "kalshi-pykalshi"

    def __init__(self, settings: Settings, emit, publish_status) -> None:
        super().__init__(emit, publish_status)
        self.settings = settings
        self._thread: threading.Thread | None = None
        self._stop = threading.Event()
        self._last_event_at: datetime | None = None
        self._error_count = 0
        self._reconnects = 0

    def start(self) -> None:
        self._thread = threading.Thread(target=self._run_loop, name="kalshi-feed", daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._stop.set()
        self.publish_status(
            self.name,
            {
                "running": False,
                "detail": "stopped",
                "last_event_at": self._last_event_at.isoformat() if self._last_event_at else None,
                "error_count": self._error_count,
                "reconnects": self._reconnects,
            },
        )

    def _run_loop(self) -> None:
        try:
            asyncio.run(self._run())
        except ImportError:
            self._error_count += 1
            self.publish_status(
                self.name,
                {
                    "running": False,
                    "detail": "pykalshi is not installed. Run: py -m pip install .[integrations]",
                    "last_event_at": self._last_event_at.isoformat() if self._last_event_at else None,
                    "error_count": self._error_count,
                    "reconnects": self._reconnects,
                },
            )
        except Exception as exc:
            self._error_count += 1
            self.publish_status(
                self.name,
                {
                    "running": False,
                    "detail": f"error: {exc}",
                    "last_event_at": self._last_event_at.isoformat() if self._last_event_at else None,
                    "error_count": self._error_count,
                    "reconnects": self._reconnects,
                },
            )

    async def _run(self) -> None:
        from pykalshi import Feed, KalshiClient

        if not self.settings.kalshi_markets:
            self.publish_status(
                self.name,
                {
                    "running": False,
                    "detail": "no KALSHI_MARKETS configured",
                    "last_event_at": self._last_event_at.isoformat() if self._last_event_at else None,
                    "error_count": self._error_count,
                    "reconnects": self._reconnects,
                },
            )
            return

        client = KalshiClient()
        self.publish_status(
            self.name,
            {
                "running": True,
                "detail": f"subscribed to {len(self.settings.kalshi_markets)} markets",
                "last_event_at": self._last_event_at.isoformat() if self._last_event_at else None,
                "error_count": self._error_count,
                "reconnects": self._reconnects,
            },
        )
        async with Feed(client) as feed:
            for ticker in self.settings.kalshi_markets:
                await feed.subscribe_ticker(ticker)
                await feed.subscribe_trades(ticker)

            async for message in feed:
                if self._stop.is_set():
                    break

                try:
                    self._process_message(message)
                    self._last_event_at = datetime.now(UTC)
                except Exception as exc:
                    # Log unexpected schema without crashing feed
                    log.error(
                        f"Failed to process message type {type(message).__name__}: {exc}",
                        extra={
                            "message_type": type(message).__name__,
                            "message_attrs": dir(message),
                            "message_repr": repr(message),
                        },
                    )

    def _process_message(self, message) -> None:
        """Extract fields defensively and emit MarketEvent."""
        market_id = getattr(message, "market_ticker", None) or getattr(message, "ticker", None)
        if not market_id:
            log.debug(f"Skipping message with no market_id: {type(message).__name__}")
            return

        message_type = type(message).__name__
        event_kind = "trade" if "trade" in message_type.lower() else "quote"
        
        # Extract price - Kalshi sends prices in cents
        price_cents = getattr(message, "price", None)
        yes_price = (float(price_cents) / 100.0) if price_cents is not None else None
        
        # Extract volume/size - handle both ticker and trade message schemas
        count = getattr(message, "count", None)
        size = getattr(message, "volume", None) or getattr(message, "size", None)
        volume_delta = size if size is not None else count
        trade_side = getattr(message, "side", None)

        event = MarketEvent(
            source="pykalshi",
            platform="kalshi",
            market_id=str(market_id),
            title=str(market_id),
            event_kind=event_kind,
            yes_price=yes_price,
            volume=float(volume_delta) if volume_delta is not None else None,
            volume_kind="delta" if volume_delta is not None else "cumulative",
            trade_size=float(size) if size is not None else None,
            trade_side=str(trade_side) if trade_side is not None else None,
            live=True,
            timestamp=datetime.now(UTC),
            metadata={"message_type": message_type},
        )
        self.emit(event)
