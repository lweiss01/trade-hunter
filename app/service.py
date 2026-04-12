from __future__ import annotations

import logging
import os
import threading
import time
from datetime import UTC, datetime, timedelta
from typing import Any

log = logging.getLogger(__name__)

from .config import Settings, persist_detector_thresholds, persist_kalshi_markets
from .detector import SpikeDetector
from .feeds.kalshi_pykalshi import KalshiPykalshiFeed
from .feeds.simulated import SimulatedFeed
from .models import MarketEvent
from .notifiers import DiscordWebhookNotifier
from .retention import cleanup_old_events
from .store import MarketStore
from .analyst import SignalAnalyst, TuningAdvisor


LIVE_FRESHNESS_WINDOW_MINUTES = 10


class TradeHunterService:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.store = MarketStore()
        self.detector = SpikeDetector(settings)
        self.notifier = DiscordWebhookNotifier(
            settings.discord_webhook_url,
            settings.discord_webhook_routes,
            alert_mode=_normalize_discord_alert_mode(getattr(settings, "discord_alert_mode", "all")),
            analyst_followup=bool(getattr(settings, "discord_analyst_followup", True)),
            analyst_min_confidence=_normalize_analyst_confidence(getattr(settings, "discord_analyst_min_confidence", "medium")),
        )
        self.feeds = []
        self._cleanup_thread: threading.Thread | None = None
        self._cleanup_stop = threading.Event()
        self._last_cleanup: dict[str, Any] | None = None
        self._kalshi_lock = threading.Lock()
        self._analyst_followups_sent: set[str] = set()
        self._analyst_followups_lock = threading.Lock()
        self._whale_baselines: dict[str, dict[str, float]] = {}

        # Optional signal analyst (Anthropic primary, Perplexity fallback)
        from .config import _load_env_file, ROOT
        _load_env_file(ROOT / ".env")
        anthropic_key = os.environ.get("ANTHROPIC_API_KEY") or ""
        perplexity_key = os.environ.get("PERPLEXITY_API_KEY") or ""
        if anthropic_key or perplexity_key:
            from .analyst import AIProviderManager
            provider_manager = AIProviderManager()
            self._analyst: SignalAnalyst | None = SignalAnalyst(
                anthropic_key=anthropic_key,
                perplexity_key=perplexity_key,
                provider_manager=provider_manager,
            )
            self._tuning_advisor: TuningAdvisor | None = TuningAdvisor(
                anthropic_key=anthropic_key,
                perplexity_key=perplexity_key,
                provider_manager=provider_manager,
            )
        else:
            self._analyst = None
            self._tuning_advisor = None
            log.info("signal analyst disabled (no API keys configured)")

        # Enforce exactly one operating mode: live OR simulation.
        # SECURITY HARDENING: Commercial Edition only for live feeds (M017)
        if not self.settings.is_commercial:
            if self.settings.enable_kalshi:
                log.warning("LIVE FEEDS BLOCKED: Kalshi feed is only available in the Commercial Edition. Defaulting to Simulation.")
            self.settings = Settings(**{**self.settings.__dict__, "enable_kalshi": False, "enable_simulation": True})

        self._active_mode = "none"
        if self.settings.enable_kalshi:
            self._active_mode = "live"
            self.feeds.append(
                KalshiPykalshiFeed(self.settings, self.ingest_event, self.store.update_feed_status)
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
        """Background thread that updates baselines hourly and runs retention daily."""
        loops = 0
        while not self._cleanup_stop.is_set():
            # Hourly: update statistical baselines
            try:
                self._whale_baselines = self.store.update_statistical_baselines()
            except Exception as e:
                log.error(f"[baselines] Update failed: {e}")

            # Daily (every 24 hours): retention cleanup
            if loops % 24 == 0:
                try:
                    result = cleanup_old_events(None, self.settings.retention_days)
                    self._last_cleanup = result
                    if not self.settings.quiet_mode:
                        print(f"[retention] Deleted {result['events_deleted']} events, {result['signals_deleted']} signals (retention: {result['retention_days']} days)")
                except Exception as e:
                    if not self.settings.quiet_mode:
                        print(f"[retention] Cleanup failed: {e}")
            
            loops += 1
            # Wait 1 hour (or until stop signal)
            self._cleanup_stop.wait(timeout=3600)
    
    def get_cleanup_status(self) -> dict[str, Any] | None:
        """Get last cleanup execution result."""
        return self._last_cleanup

    def ingest_event(self, event: MarketEvent) -> bool:
        self.store.upsert_event(event)
        market_baselines = self._whale_baselines.get(event.market_id)
        signal = self.detector.process(event, market_baselines)
        if not signal:
            return False
        self.store.record_signal(signal)
        signal_dict = signal.to_dict()
        if self.notifier.should_send_detector_alert():
            self.notifier.notify(signal)
        # Enqueue analyst interpretation (non-blocking background thread)
        if self._analyst:
            recent_flow = [e.to_dict() for e in self.store.recent_events(market_id=event.market_id, limit=30)]
            self._analyst.enqueue(
                signal_dict,
                recent_flow,
                on_complete=self._handle_analyst_complete,
            )
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

    def _handle_analyst_complete(self, signal: dict[str, Any], analyst: dict[str, Any]) -> None:
        signal_id = _signal_id(signal)
        with self._analyst_followups_lock:
            if signal_id in self._analyst_followups_sent:
                return
        if self.notifier.should_send_analyst_followup() or self.notifier.should_send_analyst_signal_only(analyst):
            if self.notifier.notify_analyst_followup(signal, analyst):
                with self._analyst_followups_lock:
                    self._analyst_followups_sent.add(signal_id)

    def get_kalshi_markets(self) -> list[str]:
        return list(self.settings.kalshi_markets)

    def get_dead_kalshi_markets(self) -> list[str]:
        for feed in self.feeds:
            if isinstance(feed, KalshiPykalshiFeed):
                return feed.dead_tickers()
        return []

    def search_kalshi_by_category(self, category: str, limit: int = 20) -> list[dict]:
        """Resolve a category label to open Kalshi event tickers via the public API.

        Returns a list of dicts with keys: event_ticker, series_ticker, title, category, open_markets.
        Each entry's series_ticker can be added to KALSHI_MARKETS for auto-resolution.

        Kalshi's public /events endpoint does not reliably honor the category query param,
        so we fetch a broader open-events window and filter locally.
        """
        import json as _json
        import urllib.request as _ureq

        base = "https://api.elections.kalshi.com/trade-api/v2"
        results: list[dict] = []
        query = str(category or "").strip().lower()

        try:
            fetch_limit = max(limit * 10, 100)
            req = _ureq.Request(
                f"{base}/events?status=open&limit={fetch_limit}",
                headers={"User-Agent": "trade-hunter/1.0"},
            )
            data = _json.load(_ureq.urlopen(req, timeout=8))
            events = data.get("events") or []

            def _event_matches(ev: dict[str, Any]) -> bool:
                if not query:
                    return True
                haystacks = [
                    str(ev.get("category") or "").lower(),
                    str(ev.get("title") or "").lower(),
                    str(ev.get("event_ticker") or ev.get("ticker") or "").lower(),
                ]
                aliases = {
                    "crypto": ["crypto", "bitcoin", "btc", "ethereum", "eth", "solana", "xrp", "doge"],
                    "macro": ["macro", "economy", "economic", "inflation", "recession", "gdp", "rates", "oil", "tariff"],
                    "geopolitics": ["geopolitics", "world", "war", "israel", "ukraine", "russia", "china", "iran"],
                    "sports": ["sports", "nba", "nfl", "mlb", "nhl", "f1", "golf", "soccer", "tennis"],
                    "elections": ["elections", "election", "president", "prime minister", "vote", "senate", "house"],
                }
                terms = aliases.get(query, [query])

                def _matches_term(text: str, term: str) -> bool:
                    if len(term) <= 3:
                        normalized = ''.join(ch if ch.isalnum() else ' ' for ch in text)
                        return term in normalized.split()
                    return term in text

                return any(_matches_term(text, term) for term in terms for text in haystacks)

            matched_events = [ev for ev in events if _event_matches(ev)]

            for ev in matched_events[:limit]:
                ticker = ev.get("event_ticker") or ev.get("ticker") or ""
                if not ticker:
                    continue
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
        if not self.settings.is_commercial:
            raise ValueError("Commercial Edition Required: Manual market tracking is disabled in the public simulation build.")

        normalized = ticker.strip().upper()
        if not normalized:
            raise ValueError("ticker is required")
        
        # Security Hardening: Validate ticker format (M014)
        import re
        if not re.match(r"^[A-Z0-9-]{1,64}$", normalized):
            raise ValueError("Invalid ticker format: tickers must be alphanumeric/dashes and <= 64 chars")

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
                # If the feed has a live refresher, trigger it for a zero-downtime update.
                # Otherwise, fall back to a hard restart.
                if hasattr(feed, "refresh_tickers"):
                    log.info("triggering live ticker refresh for %s", feed.name)
                    feed.refresh_tickers()
                else:
                    log.info("performing hard restart for feed %s", feed.name)
                    feed.stop()
                    time.sleep(0.1)
                    feed.start()
                break

    def get_tuning_backlog(self) -> dict:
        """Parse docs/TUNING-BACKLOG.md into structured data for the Settings panel."""
        import pathlib, re
        backlog_path = pathlib.Path(__file__).parent.parent / "docs" / "TUNING-BACKLOG.md"
        if not backlog_path.exists():
            return {"snapshots": [], "applied_count": 0, "planned_count": 0}

        text = backlog_path.read_text(encoding="utf-8")
        snapshots: list[dict] = []
        current_snapshot: dict | None = None
        current_items: list[dict] = []

        for line in text.splitlines():
            # Snapshot header: ## 2026-04-03 — Advisor snapshot A
            snap_m = re.match(r'^## (.+)', line)
            if snap_m:
                if current_snapshot is not None:
                    current_snapshot["items"] = current_items
                    snapshots.append(current_snapshot)
                current_snapshot = {"label": snap_m.group(1).strip(), "summary": "", "items": []}
                current_items = []
                continue

            if current_snapshot is None:
                continue

            # Summary line after ### Summary
            if line.startswith("### Summary"):
                continue

            # Item line: - [x] **TB-001** `applied` — rule text
            item_m = re.match(
                r'^\s*-\s+\[([ xX])\]\s+\*\*([\w-]+)\*\*\s+`(\w+)`\s+[—–-]+\s*(.*)',
                line
            )
            if item_m:
                checked, item_id, status, rule = item_m.groups()
                current_items.append({
                    "id": item_id,
                    "status": status,
                    "rule": rule.strip(),
                    "detail": "",
                    "note": "",
                })
                continue

            # Shorter item line (no status): - [ ] **TB-042** `planned` — rule
            item_m2 = re.match(r'^\s*-\s+\[([ xX])\]\s+\*\*([\w-]+)\*\*\s+`(\w+)`\s+(.*)', line)
            if item_m2 and not current_items or (item_m2 and current_items and item_m2.group(2) != current_items[-1]["id"]):
                checked, item_id, status, rule = item_m2.groups()
                # strip leading em-dash if present
                rule = re.sub(r'^[—–-]+\s*', '', rule).strip()
                current_items.append({
                    "id": item_id,
                    "status": status,
                    "rule": rule,
                    "detail": "",
                    "note": "",
                })
                continue

            # Continuation lines for current item
            if current_items:
                detail_m = re.match(r'^\s+-\s+Rule:\s*(.*)', line)
                if detail_m:
                    current_items[-1]["detail"] = detail_m.group(1).strip()
                    continue
                note_m = re.match(r'^\s+-\s+Notes?:\s*(.*)', line)
                if note_m:
                    current_items[-1]["note"] = note_m.group(1).strip()
                    continue

            # Snapshot summary (free text after header, before first item)
            if not current_items and current_snapshot and line.strip() and not line.startswith("#") and not line.startswith("-") and not line.startswith("`"):
                if current_snapshot["summary"]:
                    current_snapshot["summary"] += " " + line.strip()
                else:
                    current_snapshot["summary"] = line.strip()

        if current_snapshot is not None:
            current_snapshot["items"] = current_items
            snapshots.append(current_snapshot)

        # Filter out non-item snapshots (preamble, etc.)
        snapshots = [s for s in snapshots if s["items"]]

        all_items = [item for s in snapshots for item in s["items"]]
        applied_count = sum(1 for i in all_items if i["status"] == "applied")
        planned_count = sum(1 for i in all_items if i["status"] == "planned")

        return {
            "snapshots": snapshots,
            "applied_count": applied_count,
            "planned_count": planned_count,
        }

    def mark_tuning_item_applied(self, tb_id: str) -> None:
        """Flip the checkbox for a planned TB item in TUNING-BACKLOG.md to applied."""
        import pathlib, re
        backlog_path = pathlib.Path(__file__).parent.parent / "docs" / "TUNING-BACKLOG.md"
        if not backlog_path.exists():
            raise ValueError("TUNING-BACKLOG.md not found")
        text = backlog_path.read_text(encoding="utf-8")
        # Match: - [ ] **TB-042** `planned` — ...
        pattern = re.compile(
            r'^(\s*-\s+)\[ \](\s+\*\*' + re.escape(tb_id) + r'\*\*\s+)`planned`',
            re.MULTILINE,
        )
        if not pattern.search(text):
            raise ValueError(f"{tb_id} not found as a planned item")
        updated = pattern.sub(r'\1[x]\2`applied`', text)
        backlog_path.write_text(updated, encoding="utf-8")
        log.info("tuning backlog: marked %s as applied", tb_id)

    def apply_tuning_suggestions(self) -> dict[str, float]:
        if not self._tuning_advisor:
            raise ValueError("tuning advisor unavailable")

        tuning = self._tuning_advisor.get()
        if not tuning:
            raise ValueError("no tuning suggestions available")

        suggested = dict(tuning.get("suggested_thresholds") or {})
        if not suggested:
            raise ValueError("no structured threshold suggestions to apply")

        allowed = {"min_volume_delta", "min_price_move", "score_threshold"}
        unknown = sorted(set(suggested) - allowed)
        if unknown:
            raise ValueError(f"unsupported suggested thresholds: {', '.join(unknown)}")

        applied: dict[str, float] = {}
        if "min_volume_delta" in suggested:
            value = float(suggested["min_volume_delta"])
            object.__setattr__(self.settings, "spike_min_volume_delta", value)
            applied["min_volume_delta"] = value
        if "min_price_move" in suggested:
            value = float(suggested["min_price_move"])
            object.__setattr__(self.settings, "spike_min_price_move", value)
            applied["min_price_move"] = value
        if "score_threshold" in suggested:
            value = float(suggested["score_threshold"])
            object.__setattr__(self.settings, "spike_score_threshold", value)
            applied["score_threshold"] = value

        persist_detector_thresholds(
            min_volume_delta=applied.get("min_volume_delta"),
            min_price_move=applied.get("min_price_move"),
            score_threshold=applied.get("score_threshold"),
        )
        return applied

    def dashboard_state(self, is_admin: bool = False) -> dict[str, Any]:
        """Return dashboard data from SQLite."""
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

        dead_kalshi_markets = self.get_dead_kalshi_markets()

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

        # Kick and attach the second-pass tuning advisor.
        # suggested_thresholds inside tuning_advisor are SUGGESTED values only —
        # they are never auto-applied. Active thresholds live exclusively in config.applied_thresholds.
        if self._tuning_advisor:
            self._tuning_advisor.maybe_enqueue(state.get("signals", []))
            tuning = self._tuning_advisor.get()
            if tuning:
                state["tuning_advisor"] = {**tuning, "status": "suggested"}
            elif self._tuning_advisor.pending():
                state["tuning_advisor"] = {"pending": True, "status": "pending"}

        state["config"] = {
            "host": self.settings.host,
            "port": self.settings.port,
            "simulation": self.settings.enable_simulation,
            "kalshi": self.settings.enable_kalshi,
            "active_mode": self._active_mode,
            "kalshi_markets": self.settings.kalshi_markets,
            "dead_kalshi_markets": dead_kalshi_markets,
            "discord_routes": sorted(self.settings.discord_webhook_routes.keys()),
            "is_admin": is_admin,
            "is_commercial": self.settings.is_commercial,
            # applied_thresholds — these are the live detector settings, not suggestions
            "applied_thresholds": {
                "min_volume_delta": self.settings.spike_min_volume_delta,
                "min_price_move": self.settings.spike_min_price_move,
                "score_threshold": self.settings.spike_score_threshold,
            },
            # Keep flat keys for backward compat
            "spike_min_volume_delta": self.settings.spike_min_volume_delta,
            "spike_min_price_move": self.settings.spike_min_price_move,
            "spike_score_threshold": self.settings.spike_score_threshold,
        }
        return state


def _signal_id(signal: dict[str, Any]) -> str:
    event = signal.get("event") or {}
    return f"{event.get('market_id', 'unknown')}@{signal.get('detected_at', '')}"


def _normalize_discord_alert_mode(value: Any) -> str:
    normalized = str(value or "all").strip().lower()
    return normalized if normalized in {"all", "detector-only", "analyst-signals-only"} else "all"


def _normalize_analyst_confidence(value: Any) -> str:
    normalized = str(value or "medium").strip().lower()
    return normalized if normalized in {"low", "medium", "high"} else "medium"


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
