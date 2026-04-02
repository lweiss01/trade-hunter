from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from .config import Settings
from .detector import SpikeDetector
from .feeds.kalshi_pykalshi import KalshiPykalshiFeed
from .feeds.simulated import SimulatedFeed
from .models import MarketEvent
from .notifiers import DiscordWebhookNotifier
from .store import MarketStore


class TradeHunterService:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.store = MarketStore()
        self.detector = SpikeDetector(settings)
        self.notifier = DiscordWebhookNotifier(
            settings.discord_webhook_url,
            settings.discord_webhook_routes,
        )
        self.feeds = []

        if settings.enable_simulation:
            self.feeds.append(SimulatedFeed(self.ingest_event, self.store.update_feed_status))
        if settings.enable_kalshi:
            self.feeds.append(
                KalshiPykalshiFeed(settings, self.ingest_event, self.store.update_feed_status)
            )

        self.store.update_feed_status(
            "discord",
            {
                "running": self.notifier.enabled(),
                "detail": _discord_detail(settings),
            },
        )

    def start(self) -> None:
        for feed in self.feeds:
            feed.start()

    def stop(self) -> None:
        for feed in self.feeds:
            feed.stop()

    def ingest_event(self, event: MarketEvent) -> bool:
        self.store.upsert_event(event)
        signal = self.detector.process(event)
        if not signal:
            return False
        self.store.record_signal(signal)
        self.notifier.notify(signal)
        return True

    def ingest_payload(self, payload: Any, default_source: str = "manual") -> list[bool]:
        if isinstance(payload, list):
            return [self.ingest_payload(item, default_source=default_source)[0] for item in payload]

        metadata = dict(payload.get("metadata") or {})
        event = MarketEvent(
            source=str(payload.get("source") or default_source),
            platform=str(payload.get("platform") or "unknown"),
            market_id=str(payload.get("market_id") or payload.get("ticker") or "unknown-market"),
            title=str(
                payload.get("title")
                or payload.get("market_id")
                or payload.get("ticker")
                or "Untitled market"
            ),
            event_kind=str(
                payload.get("event_kind")
                or payload.get("kind")
                or metadata.get("event_kind")
                or ("trade" if payload.get("trade_size") or payload.get("size") else "quote")
            ),
            yes_price=_maybe_float(payload.get("yes_price") or payload.get("price")),
            no_price=_maybe_float(payload.get("no_price")),
            volume=_maybe_float(payload.get("volume") or payload.get("size") or payload.get("count")),
            volume_kind=str(payload.get("volume_kind") or "cumulative"),
            trade_size=_maybe_float(payload.get("trade_size") or payload.get("size")),
            trade_side=_maybe_text(payload.get("trade_side") or payload.get("side")),
            liquidity=_maybe_float(payload.get("liquidity")),
            live=_maybe_bool(
                payload.get("live"),
                default=default_source not in {"simulation", "demo-button", "smoke-test"},
            ),
            topic=_maybe_text(payload.get("topic") or payload.get("watchlist") or metadata.get("topic")),
            market_url=_maybe_text(payload.get("market_url") or metadata.get("market_url")),
            timestamp=_parse_time(payload.get("timestamp")),
            metadata=metadata,
        )
        return [self.ingest_event(event)]

    def dashboard_state(self) -> dict[str, Any]:
        state = self.store.dashboard_state()
        state["config"] = {
            "host": self.settings.host,
            "port": self.settings.port,
            "simulation": self.settings.enable_simulation,
            "kalshi": self.settings.enable_kalshi,
            "kalshi_markets": self.settings.kalshi_markets,
            "discord_routes": sorted(self.settings.discord_webhook_routes.keys()),
            "spike_min_volume_delta": self.settings.spike_min_volume_delta,
            "spike_min_price_move": self.settings.spike_min_price_move,
            "spike_score_threshold": self.settings.spike_score_threshold,
        }
        return state


def _maybe_float(value: Any) -> float | None:
    if value is None or value == "":
        return None
    return float(value)


def _maybe_text(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _maybe_bool(value: Any, default: bool) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes", "on"}


def _parse_time(value: Any) -> datetime:
    if not value:
        return datetime.now(UTC)
    if isinstance(value, datetime):
        return value.astimezone(UTC)
    text = str(value).replace("Z", "+00:00")
    return datetime.fromisoformat(text).astimezone(UTC)


def _discord_detail(settings: Settings) -> str:
    routes = sorted(settings.discord_webhook_routes.keys())
    if settings.discord_webhook_url and routes:
        return f"default webhook + {len(routes)} topic routes ({', '.join(routes)})"
    if settings.discord_webhook_url:
        return "default webhook configured"
    if routes:
        return f"{len(routes)} topic routes configured ({', '.join(routes)})"
    return "webhook disabled"
