from __future__ import annotations

import asyncio
import json
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
        self._message_count = 0
        self._ticker_count = 0
        self._trade_count = 0
        self._lifecycle_count = 0
        self._other_count = 0
        self._api_mode = "unknown"
        self._valid_tickers: list[str] = []
        self._dead_tickers: list[str] = []

    def start(self) -> None:
        self._thread = threading.Thread(target=self._run_loop, name="kalshi-feed", daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._stop.set()
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=5)
        self._thread = None
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
        feed_ctx = Feed(client)

        if hasattr(feed_ctx, "__aenter__"):
            async with feed_ctx as feed:
                await self._consume_feed(feed)
        else:
            with feed_ctx as feed:
                await self._consume_feed(feed)

    async def _consume_feed(self, feed) -> None:
        # Validate configured tickers — warn clearly about expired/invalid ones.
        valid_tickers, dead_tickers = await self._validate_tickers()
        if dead_tickers:
            log.warning(
                "kalshi: %d ticker(s) not found on API (expired/invalid): %s",
                len(dead_tickers), ", ".join(dead_tickers),
            )
        self._valid_tickers = valid_tickers
        self._dead_tickers = dead_tickers
        if not valid_tickers:
            self.publish_status(
                self.name,
                {
                    "running": False,
                    "detail": f"all configured tickers are expired or invalid: {', '.join(dead_tickers)}",
                    "last_event_at": None,
                    "error_count": self._error_count,
                    "reconnects": self._reconnects,
                },
            )
            return

        for ticker in valid_tickers:
            if hasattr(feed, "subscribe_ticker") and hasattr(feed, "subscribe_trades"):
                await feed.subscribe_ticker(ticker)
                await feed.subscribe_trades(ticker)
            elif hasattr(feed, "subscribe"):
                feed.subscribe("ticker", market_ticker=ticker)
                feed.subscribe("trade", market_ticker=ticker)
            else:
                raise AttributeError("Feed does not support ticker/trade subscription APIs")

        # Subscribe to lifecycle on any one ticker as a dispatch-sanity probe (public, no-auth).
        if valid_tickers and hasattr(feed, "subscribe"):
            try:
                result = feed.subscribe("market_lifecycle_v2", market_ticker=valid_tickers[0])
                # Defensive: if test mocks return a coroutine, close it to avoid warnings.
                if asyncio.iscoroutine(result):
                    result.close()
            except Exception as exc:
                log.warning("market_lifecycle_v2 probe subscription failed: %s", exc)

        self.publish_status(
            self.name,
            {
                "running": True,
                "detail": f"subscribed to {len(valid_tickers)} markets ({len(dead_tickers)} series/expired skipped)",
                "last_event_at": self._last_event_at.isoformat() if self._last_event_at else None,
                "error_count": self._error_count,
                "reconnects": self._reconnects,
            },
        )

        if hasattr(feed, "__aiter__"):
            self._api_mode = "async-iterator"
            async for message in feed:
                if self._stop.is_set():
                    break
                self._handle_message(message)
        elif hasattr(feed, "start") and hasattr(feed, "stop"):
            self._api_mode = "callback-startstop"
            self.publish_status(self.name, self._status_payload(feed))
            # Callback-based feed API variant; register handlers and keep adapter alive until stop.
            self._register_callback_handlers(feed)
            feed.start()
            try:
                heartbeat_ticks = 0
                while not self._stop.is_set():
                    await asyncio.sleep(0.25)
                    heartbeat_ticks += 1
                    # Every 10 seconds, refresh status so staleness is explicit in dashboard.
                    if heartbeat_ticks % 40 == 0:
                        self.publish_status(self.name, self._status_payload(feed))
            finally:
                feed.stop()
        else:
            raise AttributeError("Feed does not support iterable or start/stop consumption APIs")

    async def _validate_tickers(self) -> tuple[list[str], list[str]]:
        """Resolve each configured ticker to one or more active market tickers.

        Series slugs resolve to the current open market.
        Event slugs (fan-out events) resolve to ALL open sub-markets.
        Specific tickers that 404 are dead.
        Returns (valid_resolved, dead) lists of concrete market tickers.
        """
        import urllib.request as ureq
        base = "https://api.elections.kalshi.com/trade-api/v2/markets"
        valid: list[str] = []
        dead: list[str] = []

        for ticker in self.settings.kalshi_markets:
            resolved = await self._resolve_all_tickers(ticker, base, ureq)
            if resolved:
                for t in resolved:
                    if t not in valid:
                        valid.append(t)
            else:
                dead.append(ticker)

        return valid, dead

    async def _resolve_all_tickers(self, ticker: str, base: str, ureq) -> list[str]:
        """Like _resolve_ticker but returns ALL matching open market tickers.

        Fan-out events (many sub-markets per event) return all sub-markets
        so the feed gets full coverage of the event.
        """
        import json as _json

        # 1. Direct market lookup.
        try:
            req = ureq.Request(f"{base}/{ticker}", headers={"User-Agent": "trade-hunter/1.0"})
            data = _json.load(ureq.urlopen(req, timeout=5))
            m = data.get("market", data)
            if m.get("status") == "active":
                return [m.get("ticker", ticker)]
            log.debug("kalshi ticker %s exists but status=%s — skipping", ticker, m.get("status"))
            return []
        except Exception:
            pass

        # 2. Series ticker search — returns one active market (the current window).
        try:
            url = f"{base}?series_ticker={ticker}&status=open&limit=5"
            req = ureq.Request(url, headers={"User-Agent": "trade-hunter/1.0"})
            data = _json.load(ureq.urlopen(req, timeout=5))
            markets = data.get("markets", [])
            if markets:
                tickers = [m.get("ticker") for m in markets if m.get("ticker")]
                log.info("kalshi: resolved series %s → %s", ticker, tickers)
                return tickers
        except Exception as exc:
            log.debug("kalshi series lookup failed for %s: %s", ticker, exc)

        # 3. Event ticker search — fan-out events, return all sub-markets.
        try:
            url = f"{base}?event_ticker={ticker}&status=open&limit=20"
            req = ureq.Request(url, headers={"User-Agent": "trade-hunter/1.0"})
            data = _json.load(ureq.urlopen(req, timeout=5))
            markets = data.get("markets", [])
            if markets:
                tickers = [m.get("ticker") for m in markets if m.get("ticker")]
                log.info("kalshi: resolved event %s → %d sub-markets: %s", ticker, len(tickers), tickers[:3])
                return tickers
        except Exception as exc:
            log.debug("kalshi event lookup failed for %s: %s", ticker, exc)

        return []

    async def _resolve_ticker(self, ticker: str, base: str, ureq) -> str | None:
        """Return the concrete market ticker for a given input.

        Resolution order:
        1. Direct market lookup (specific ticker like KXBTC15M-26APR030145-45)
        2. Series ticker search (series slug like KXBTC15M)
        3. Event ticker search (event slug like KXTOPCHEF-26DEC31 with sub-markets)

        Returns the first resolved ticker, or None if nothing active is found.
        """
        # 1. Direct market lookup.
        try:
            req = ureq.Request(f"{base}/{ticker}", headers={"User-Agent": "trade-hunter/1.0"})
            data = json.load(ureq.urlopen(req, timeout=5))
            m = data.get("market", data)
            if m.get("status") == "active":
                return m.get("ticker", ticker)
            log.debug("kalshi ticker %s exists but status=%s — skipping", ticker, m.get("status"))
            return None
        except Exception:
            pass

        # 2. Series ticker search.
        try:
            url = f"{base}?series_ticker={ticker}&status=open&limit=5"
            req = ureq.Request(url, headers={"User-Agent": "trade-hunter/1.0"})
            data = json.load(ureq.urlopen(req, timeout=5))
            markets = data.get("markets", [])
            if markets:
                resolved = markets[0].get("ticker")
                log.info("kalshi: resolved series %s → %s (%d open)", ticker, resolved, len(markets))
                return resolved
        except Exception as exc:
            log.debug("kalshi series lookup failed for %s: %s", ticker, exc)

        # 3. Event ticker search — covers KXTOPCHEF-26DEC31 style event slugs.
        try:
            url = f"{base}?event_ticker={ticker}&status=open&limit=5"
            req = ureq.Request(url, headers={"User-Agent": "trade-hunter/1.0"})
            data = json.load(ureq.urlopen(req, timeout=5))
            markets = data.get("markets", [])
            if markets:
                resolved = markets[0].get("ticker")
                log.info("kalshi: resolved event %s → %s (%d open sub-markets)", ticker, resolved, len(markets))
                return resolved
        except Exception as exc:
            log.debug("kalshi event lookup failed for %s: %s", ticker, exc)

        return None

    def _register_callback_handlers(self, feed) -> None:
        """Register ticker/trade + lifecycle probe callbacks."""
        if not hasattr(feed, "on"):
            raise AttributeError("Feed start/stop API requires an 'on' callback registration method")

        feed.on("ticker", self._on_ticker)
        feed.on("trade", self._on_trade)
        # Public no-auth channel — fires on market state changes.
        # Acts as a dispatch-sanity probe: if channel routing works we'll see counts here.
        feed.on("market_lifecycle_v2", self._on_lifecycle)
        log.info("kalshi feed callback handlers registered: ticker, trade, market_lifecycle_v2 (probe)")

    def _on_ticker(self, message) -> None:
        self._ticker_count += 1
        self._handle_message(message)

    def _on_trade(self, message) -> None:
        self._trade_count += 1
        self._handle_message(message)

    def _on_lifecycle(self, message) -> None:
        """Lifecycle probe — count events to confirm dispatch is working; don't emit."""
        self._lifecycle_count += 1
        log.debug("kalshi lifecycle: %s", repr(message))
        if self._lifecycle_count == 1:
            log.info("kalshi market_lifecycle_v2 dispatch confirmed (first event received)")


    def _status_payload(self, feed: object | None = None) -> dict[str, object]:
        mode = self._api_mode if self._api_mode != "unknown" else "pending"

        n_valid = len(self._valid_tickers)
        n_dead = len(self._dead_tickers)
        n_configured = len(self.settings.kalshi_markets) if hasattr(self.settings, 'kalshi_markets') else 0
        if n_valid > n_configured:
            sub_info = f"{n_valid} subscriptions ({n_configured} configured"
            if n_dead:
                sub_info += f", {n_dead} unresolved"
            sub_info += ")"
        else:
            sub_info = f"{n_valid} active" + (f", {n_dead} expired" if n_dead else "")

        transport_parts: list[str] = []
        if feed is not None:
            ws_msgs = getattr(feed, "messages_received", None)
            since_last = getattr(feed, "seconds_since_last_message", None)
            if isinstance(ws_msgs, int):
                transport_parts.append(f"ws_msgs:{ws_msgs}")
            if isinstance(since_last, (int, float)):
                transport_parts.append(f"since_last:{int(since_last)}s")

        transport_parts.append(f"ticker:{self._ticker_count} trade:{self._trade_count} lifecycle:{self._lifecycle_count} handled:{self._message_count}")
        transport = ", ".join(transport_parts)

        if self._ticker_count + self._trade_count > 0:
            detail = f"{sub_info} markets ({mode}, {transport})"
        elif self._lifecycle_count > 0:
            detail = f"{sub_info} markets ({mode}, dispatch OK, no ticker/trade yet, {transport})"
        else:
            detail = f"{sub_info} markets ({mode}, waiting for first message, {transport})"

        return {
            "running": True,
            "detail": detail,
            "last_event_at": self._last_event_at.isoformat() if self._last_event_at else None,
            "error_count": self._error_count,
            "reconnects": self._reconnects,
        }

    def _handle_message(self, message) -> None:
        """Process and record one feed message safely."""
        if self._stop.is_set():
            return

        try:
            self._process_message(message)
            self._message_count += 1
            self._last_event_at = datetime.now(UTC)
            self.publish_status(self.name, self._status_payload())
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
        """Extract fields from TickerMessage or TradeMessage and emit MarketEvent."""
        market_id = getattr(message, "market_ticker", None) or getattr(message, "ticker", None)
        if not market_id:
            log.debug("Skipping message with no market_id: %s", type(message).__name__)
            return

        message_type = type(message).__name__

        if message_type == "TradeMessage":
            event_kind = "trade"
            # TradeMessage: yes_price_dollars, count_fp, taker_side
            yes_price = getattr(message, "yes_price_dollars", None)
            count_fp = getattr(message, "count_fp", None)
            volume_delta = float(count_fp) if count_fp is not None else None
            trade_side = str(getattr(message, "taker_side", "") or "")
            trade_size = volume_delta
        elif message_type == "TickerMessage":
            event_kind = "quote"
            # TickerMessage: price_dollars (last), yes_bid_dollars, yes_ask_dollars, volume_fp
            yes_price = getattr(message, "yes_bid_dollars", None) or getattr(message, "price_dollars", None)
            volume_fp = getattr(message, "volume_fp", None)
            volume_delta = float(volume_fp) if volume_fp is not None else None
            trade_side = None
            trade_size = None
        else:
            log.debug("Skipping unhandled message type: %s", message_type)
            return

        event = MarketEvent(
            source="pykalshi",
            platform="kalshi",
            market_id=str(market_id),
            title=str(market_id),
            event_kind=event_kind,
            yes_price=float(yes_price) if yes_price is not None else None,
            volume=volume_delta,
            volume_kind="delta",
            trade_size=trade_size,
            trade_side=trade_side if trade_side else None,
            live=True,
            timestamp=datetime.now(UTC),
            metadata={"message_type": message_type},
        )
        self.emit(event)
