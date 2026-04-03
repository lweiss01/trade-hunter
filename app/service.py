from __future__ import annotations

import logging
import os
import threading
import time
from datetime import UTC, datetime, timedelta
from typing import Any

log = logging.getLogger(__name__)

from .config import Settings, persist_kalshi_markets
from .detector import SpikeDetector
from .feeds.kalshi_pykalshi import KalshiPykalshiFeed
from .feeds.simulated import SimulatedFeed
from .models import MarketEvent
from .notifiers import DiscordWebhookNotifier
from .retention import cleanup_old_events
from .store import MarketStore
from .analyst import SignalAnalyst


LIVE_FRESHNESS_WINDOW_MINUTES = 10


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
        self._cleanup_thread: threading.Thread | None = None
        self._cleanup_stop = threading.Event()
        self._last_cleanup: dict[str, Any] | None = None
        self._kalshi_lock = threading.Lock()

        # Optional signal analyst (Anthropic primary, Perplexity fallback)
        from .config import _load_env_file, ROOT
        _load_env_file(ROOT / ".env")
        anthropic_key = os.environ.get("ANTHROPIC_API_KEY") or ""
        perplexity_key = os.environ.get("PERPLEXITY_API_KEY") or ""
        if anthropic_key or perplexity_key:
            self._analyst: SignalAnalyst | None = SignalAnalyst(
                anthropic_key=anthropic_key,
                perplexity_key=perplexity_key,
            )
        else:
            self._analyst = None
            log.info("signal analyst disabled (no API keys configured)")

        # Enforce exactly one operating mode: live OR simulation.
        self._active_mode = "none"
        if settings.enable_kalshi:
            self._active_mode = "live"
            self.feeds.append(
                KalshiPykalshiFeed(settings, self.ingest_event, self.store.update_feed_status)
            )
            self.store.update_feed_status(
                "simulation",
                {
                    "running": False,
                    "detail": "suppressed: live mode active",
                    "error_count": 0,
                    "reconnects": 0,
                },
            )
        elif settings.enable_simulation:
            self._active_mode = "simulation"
            self.feeds.append(SimulatedFeed(self.ingest_event, self.store.update_feed_status))
            self.store.update_feed_status(
                "kalshi-pykalshi",
                {
                    "running": False,
                    "detail": "suppressed: simulation mode active",
                    "error_count": 0,
                    "reconnects": 0,
                },
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
        
        # Start retention cleanup thread
        self._cleanup_stop.clear()
        self._cleanup_thread = threading.Thread(target=self._cleanup_loop, daemon=True)
        self._cleanup_thread.start()

    def stop(self) -> None:
        for feed in self.feeds:
            feed.stop()
        
        # Stop cleanup thread
        if self._cleanup_thread:
            self._cleanup_stop.set()
            self._cleanup_thread.join(timeout=2.0)
    
    def _cleanup_loop(self) -> None:
        """Background thread that runs retention cleanup every 24 hours."""
        while not self._cleanup_stop.is_set():
            try:
                result = cleanup_old_events(None, self.settings.retention_days)
                self._last_cleanup = result
                if not self.settings.quiet_mode:
                    print(f"[retention] Deleted {result['events_deleted']} events, {result['signals_deleted']} signals (retention: {result['retention_days']} days)")
            except Exception as e:
                if not self.settings.quiet_mode:
                    print(f"[retention] Cleanup failed: {e}")
            
            # Wait 24 hours (or until stop signal)
            self._cleanup_stop.wait(timeout=86400)
    
    def get_cleanup_status(self) -> dict[str, Any] | None:
        """Get last cleanup execution result."""
        return self._last_cleanup

    def ingest_event(self, event: MarketEvent) -> bool:
        self.store.upsert_event(event)
        signal = self.detector.process(event)
        if not signal:
            return False
        self.store.record_signal(signal)
        self.notifier.notify(signal)
        # Enqueue analyst interpretation (non-blocking background thread)
        if self._analyst:
            recent_flow = [e.to_dict() for e in self.store.recent_events(market_id=event.market_id, limit=30)]
            self._analyst.enqueue(signal.to_dict(), recent_flow)
        return True

    def ingest_payload(self, payload: Any, default_source: str = "manual") -> list[bool]:
        if isinstance(payload, list):
            return [self.ingest_payload(item, default_source=default_source)[0] for item in payload]

        metadata = dict(payload.get("metadata") or {})
        # Preserve alert_type in metadata if present
        if "alert_type" in payload:
            metadata["alert_type"] = payload["alert_type"]
        
        # Default platform to 'polymarket' for polyalerthub source, 'unknown' otherwise
        default_platform = "polymarket" if default_source == "polyalerthub" else "unknown"
        
        event = MarketEvent(
            source=str(payload.get("source") or default_source),
            platform=str(payload.get("platform") or default_platform),
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

    def get_kalshi_markets(self) -> list[str]:
        return list(self.settings.kalshi_markets)

    def search_kalshi_by_category(self, category: str, limit: int = 20) -> list[dict]:
        """Resolve a category label to open Kalshi event tickers via the public API.

        Returns a list of dicts with keys: event_ticker, series_ticker, title, category, open_markets.
        Each entry's series_ticker can be added to KALSHI_MARKETS for auto-resolution.
        """
        import json as _json
        import urllib.request as _ureq
        base = "https://api.elections.kalshi.com/trade-api/v2"
        results: list[dict] = []
        try:
            params = f"?status=open&limit={limit}"
            if category:
                params += f"&category={_ureq.quote(category, safe='')}"
            req = _ureq.Request(
                f"{base}/events{params}",
                headers={"User-Agent": "trade-hunter/1.0"},
            )
            data = _json.load(_ureq.urlopen(req, timeout=8))
            for ev in data.get("events") or []:
                ticker = ev.get("event_ticker") or ev.get("ticker") or ""
                if not ticker:
                    continue
                # Try to find associated series ticker via markets search
                series_ticker = None
                try:
                    mreq = _ureq.Request(
                        f"{base}/markets?event_ticker={_ureq.quote(ticker, safe='')}&status=open&limit=1",
                        headers={"User-Agent": "trade-hunter/1.0"},
                    )
                    mdata = _json.load(_ureq.urlopen(mreq, timeout=5))
                    markets = mdata.get("markets") or []
                    if markets:
                        series_ticker = markets[0].get("series_ticker") or markets[0].get("ticker")
                except Exception:
                    pass
                results.append({
                    "event_ticker": ticker,
                    "series_ticker": series_ticker or ticker,
                    "title": str(ev.get("title") or ""),
                    "category": str(ev.get("category") or ""),
                    "mutually_exclusive": bool(ev.get("mutually_exclusive")),
                })
        except Exception as exc:
            log.warning("kalshi category search failed for %r: %s", category, exc)
        return results

    def add_kalshi_market(self, ticker: str) -> list[str]:
        normalized = ticker.strip().upper()
        if not normalized:
            raise ValueError("ticker is required")

        with self._kalshi_lock:
            if normalized in self.settings.kalshi_markets:
                return list(self.settings.kalshi_markets)

            self.settings.kalshi_markets.append(normalized)
            persist_kalshi_markets(self.settings.kalshi_markets)
            self._restart_kalshi_feed_locked()
            return list(self.settings.kalshi_markets)

    def remove_kalshi_market(self, ticker: str) -> list[str]:
        normalized = ticker.strip().upper()
        if not normalized:
            raise ValueError("ticker is required")

        with self._kalshi_lock:
            self.settings.kalshi_markets[:] = [
                item for item in self.settings.kalshi_markets if item != normalized
            ]
            persist_kalshi_markets(self.settings.kalshi_markets)
            self._restart_kalshi_feed_locked()
            return list(self.settings.kalshi_markets)

    def _restart_kalshi_feed_locked(self) -> None:
        if not self.settings.enable_kalshi:
            return

        for feed in self.feeds:
            if isinstance(feed, KalshiPykalshiFeed):
                feed.stop()
                time.sleep(0.1)
                feed.start()
                break

    def dashboard_state(self) -> dict[str, Any]:
        state = self.store.dashboard_state()

        raw_activity = list(state.get("activity", []))
        raw_markets = list(state.get("markets", []))
        raw_signals = list(state.get("signals", []))
        latest_event_at = _latest_event_timestamp(raw_activity + raw_markets)
        latest_signal_at = _latest_signal_timestamp(raw_signals)

        if self._active_mode == "live":
            excluded = {"simulation", "demo-button", "smoke-test", "test"}
            state["activity"] = [e for e in state.get("activity", []) if e.get("source") not in excluded]
            state["markets"] = [e for e in state.get("markets", []) if e.get("source") not in excluded]
            state["signals"] = [
                s
                for s in state.get("signals", [])
                if (s.get("event") or {}).get("source") not in excluded
            ]

            fresh_cutoff = datetime.now(UTC) - timedelta(minutes=LIVE_FRESHNESS_WINDOW_MINUTES)
            state["activity"] = [
                e for e in state.get("activity", []) if _event_is_fresh(e, fresh_cutoff)
            ]
            state["markets"] = [
                e for e in state.get("markets", []) if _event_is_fresh(e, fresh_cutoff)
            ]
            state["signals"] = [
                s for s in state.get("signals", []) if _signal_is_fresh(s, fresh_cutoff)
            ]

        state["activity"] = _dedupe_event_dicts(state.get("activity", []))
        state["markets"] = _dedupe_event_dicts(state.get("markets", []))

        feeds = state.get("feeds", {})
        if self._active_mode == "live" and "simulation" in feeds:
            feeds["simulation"]["running"] = False
            feeds["simulation"]["detail"] = "suppressed: live mode active"
        if self._active_mode == "simulation" and "kalshi-pykalshi" in feeds:
            feeds["kalshi-pykalshi"]["running"] = False
            feeds["kalshi-pykalshi"]["detail"] = "suppressed: simulation mode active"

        activity = state.get("activity", [])
        sources: dict[str, int] = {}
        for event in activity:
            src = str(event.get("source") or "unknown")
            sources[src] = sources.get(src, 0) + 1

        state["summary"] = {
            "live_events": sum(1 for e in activity if e.get("live")),
            "trade_events": sum(1 for e in activity if e.get("event_kind") == "trade"),
            "sources": sources,
        }

        state["telemetry"] = {
            "freshness_window_minutes": LIVE_FRESHNESS_WINDOW_MINUTES if self._active_mode == "live" else None,
            "latest_event_at": latest_event_at,
            "latest_signal_at": latest_signal_at,
            "kalshi_last_event_at": (feeds.get("kalshi-pykalshi") or {}).get("last_event_at"),
            "subscribed_tickers": _safe_len(self.settings.kalshi_markets),
        }

        # Attach analyst reads to signals if available
        if self._analyst:
            enriched = []
            for sig in state.get("signals", []):
                read = self._analyst.get(sig)
                pending = self._analyst.pending(sig)
                sig = dict(sig)
                if read:
                    sig["analyst"] = read
                elif pending:
                    sig["analyst"] = {"pending": True}
                enriched.append(sig)
            state["signals"] = enriched

        state["config"] = {
            "host": self.settings.host,
            "port": self.settings.port,
            "simulation": self.settings.enable_simulation,
            "kalshi": self.settings.enable_kalshi,
            "active_mode": self._active_mode,
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


def _safe_len(value: Any) -> int:
    """Return len(value) when list-like, otherwise 0 for mock/unknown values."""
    try:
        length = len(value)
    except Exception:
        return 0
    return int(length) if isinstance(length, int) and length >= 0 else 0


def _latest_event_timestamp(events: list[dict[str, Any]]) -> str | None:
    latest: datetime | None = None
    for event in events:
        ts = event.get("timestamp")
        if not ts:
            continue
        try:
            dt = _parse_time(ts)
        except Exception:
            continue
        if latest is None or dt > latest:
            latest = dt
    return latest.isoformat() if latest else None


def _latest_signal_timestamp(signals: list[dict[str, Any]]) -> str | None:
    latest: datetime | None = None
    for signal in signals:
        ts = signal.get("detected_at")
        if not ts:
            continue
        try:
            dt = _parse_time(ts)
        except Exception:
            continue
        if latest is None or dt > latest:
            latest = dt
    return latest.isoformat() if latest else None


def _event_is_fresh(event: dict[str, Any], cutoff: datetime) -> bool:
    ts = event.get("timestamp")
    if not ts:
        return False
    try:
        dt = _parse_time(ts)
    except Exception:
        return False
    return dt >= cutoff


def _signal_is_fresh(signal: dict[str, Any], cutoff: datetime) -> bool:
    ts = signal.get("detected_at")
    if not ts:
        return False
    try:
        dt = _parse_time(ts)
    except Exception:
        return False
    return dt >= cutoff


def _dedupe_event_dicts(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Remove duplicate serialized events while preserving order."""
    seen: set[tuple[Any, ...]] = set()
    deduped: list[dict[str, Any]] = []

    for event in events:
        key = (
            event.get("source"),
            event.get("platform"),
            event.get("market_id"),
            event.get("event_kind"),
            event.get("timestamp"),
            event.get("trade_size"),
            event.get("yes_price"),
            event.get("volume"),
        )
        if key in seen:
            continue
        seen.add(key)
        deduped.append(event)

    return deduped


def _discord_detail(settings: Settings) -> str:
    routes = sorted(settings.discord_webhook_routes.keys())
    if settings.discord_webhook_url and routes:
        return f"default webhook + {len(routes)} topic routes ({', '.join(routes)})"
    if settings.discord_webhook_url:
        return "default webhook configured"
    if routes:
        return f"{len(routes)} topic routes configured ({', '.join(routes)})"
    return "webhook disabled"
