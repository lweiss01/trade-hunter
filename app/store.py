from __future__ import annotations

import json
import sqlite3
from datetime import UTC, datetime
from threading import Lock, local
from typing import Any

from . import db
from .models import MarketEvent, SpikeSignal


class MarketStore:
    """SQLite-backed event and signal store with thread-safe operations."""
    
    def __init__(self, db_path: str | None = None) -> None:
        self._lock = Lock()
        self._db_path = db_path
        self._thread_local = local()
    
    def _get_connection(self) -> sqlite3.Connection:
        """Get connection, preferring injected test connection when present."""
        injected_conn = getattr(self, "_conn", None)
        if injected_conn is not None:
            return injected_conn

        if not hasattr(self._thread_local, "conn"):
            self._thread_local.conn = db.connect(self._db_path) if self._db_path else db.connect()
        return self._thread_local.conn
    
    def upsert_event(self, event: MarketEvent) -> None:
        """Insert event and update market metadata."""
        with self._lock:
            cursor = self._get_connection().cursor()
            
            # Insert event
            cursor.execute("""
                INSERT INTO events (
                    source, platform, market_id, title, event_kind,
                    yes_price, no_price, volume, volume_kind,
                    trade_size, trade_side, liquidity, live, topic,
                    market_url, timestamp, metadata_json
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                event.source,
                event.platform,
                event.market_id,
                event.title,
                event.event_kind,
                event.yes_price,
                event.no_price,
                event.volume,
                event.volume_kind,
                event.trade_size,
                event.trade_side,
                event.liquidity,
                1 if event.live else 0,
                event.topic,
                event.market_url,
                event.timestamp.isoformat(),
                json.dumps(event.metadata) if event.metadata else None,
            ))
            
            # Upsert market metadata
            cursor.execute("""
                INSERT INTO markets (market_id, platform, title, last_event_at, total_events, last_yes_price, last_volume, updated_at)
                VALUES (?, ?, ?, ?, 1, ?, ?, ?)
                ON CONFLICT(market_id) DO UPDATE SET
                    platform = excluded.platform,
                    title = excluded.title,
                    last_event_at = excluded.last_event_at,
                    total_events = total_events + 1,
                    last_yes_price = excluded.last_yes_price,
                    last_volume = excluded.last_volume,
                    updated_at = excluded.updated_at
            """, (
                event.market_id,
                event.platform,
                event.title,
                event.timestamp.isoformat(),
                event.yes_price,
                event.volume,
                datetime.now(UTC).isoformat(),
            ))
            
            self._get_connection().commit()
    
    def record_signal(self, signal: SpikeSignal) -> None:
        """Insert spike signal with optional event link."""
        with self._lock:
            cursor = self._get_connection().cursor()
            
            # Try to find the event_id for this signal's event
            event_id = None
            cursor.execute("""
                SELECT id FROM events
                WHERE market_id = ? AND timestamp = ?
                ORDER BY id DESC LIMIT 1
            """, (signal.event.market_id, signal.event.timestamp.isoformat()))
            row = cursor.fetchone()
            if row:
                event_id = row["id"]
            
            cursor.execute("""
                INSERT INTO signals (
                    market_id, score, volume_delta, price_move,
                    baseline_volume_delta, reason, tier, topic,
                    source_label, detected_at, event_id,
                    baseline_1h, baseline_24h,
                    price_move_1m, price_move_5m, price_move_30m,
                    leading_events_json
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                signal.event.market_id,
                signal.score,
                signal.volume_delta,
                signal.price_move,
                signal.baseline_volume_delta,
                signal.reason,
                signal.tier,
                signal.topic,
                signal.source_label,
                signal.detected_at.isoformat(),
                event_id,
                signal.baseline_1h,
                signal.baseline_24h,
                signal.price_move_1m,
                signal.price_move_5m,
                signal.price_move_30m,
                json.dumps([event.to_dict() for event in signal.leading_events]),
            ))
            self._get_connection().commit()
    
    def update_feed_status(self, name: str, payload: dict[str, Any]) -> None:
        """Upsert feed health status."""
        with self._lock:
            cursor = self._get_connection().cursor()
            cursor.execute("""
                INSERT INTO feed_health (feed_name, running, detail, last_event_at, error_count, reconnects, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(feed_name) DO UPDATE SET
                    running = excluded.running,
                    detail = excluded.detail,
                    last_event_at = excluded.last_event_at,
                    error_count = excluded.error_count,
                    reconnects = excluded.reconnects,
                    updated_at = excluded.updated_at
            """, (
                name,
                1 if payload.get("running") else 0,
                payload.get("detail"),
                payload.get("last_event_at"),
                payload.get("error_count", 0),
                payload.get("reconnects", 0),
                datetime.now(UTC).isoformat(),
            ))
            self._get_connection().commit()
    
    def recent_events(self, market_id: str | None = None, limit: int = 30) -> list:
        """Return recent MarketEvent objects, optionally filtered by market_id."""
        from .models import MarketEvent
        with self._lock:
            cursor = self._get_connection().cursor()
            if market_id:
                cursor.execute(
                    "SELECT * FROM events WHERE market_id = ? ORDER BY timestamp DESC LIMIT ?",
                    (market_id, limit),
                )
            else:
                cursor.execute(
                    "SELECT * FROM events ORDER BY timestamp DESC LIMIT ?",
                    (limit,),
                )
            rows = cursor.fetchall()
        return [self._row_to_market_event(row) for row in rows]

    def dashboard_state(self) -> dict[str, Any]:
        """Return dashboard data from SQLite."""
        with self._lock:
            cursor = self._get_connection().cursor()
            
            # Get latest event per market (top 50)
            cursor.execute("""
                SELECT e.* FROM events e
                INNER JOIN (
                    SELECT market_id, MAX(timestamp) as max_ts
                    FROM events
                    GROUP BY market_id
                ) latest ON e.market_id = latest.market_id AND e.timestamp = latest.max_ts
                ORDER BY e.timestamp DESC, e.id DESC
                LIMIT 200
            """)
            markets = self._dedupe_events([self._row_to_market_event(row) for row in cursor.fetchall()])[:50]
            
            # Get recent events (return 24 for activity after dedupe)
            cursor.execute("""
                SELECT * FROM events
                ORDER BY timestamp DESC, id DESC
                LIMIT 300
            """)
            all_recent = self._dedupe_events([self._row_to_market_event(row) for row in cursor.fetchall()])
            activity = all_recent[:24]
            
            # Get recent signals (top 25)
            cursor.execute("""
                SELECT s.* FROM signals s
                ORDER BY s.detected_at DESC, s.id DESC
                LIMIT 25
            """)
            signals = []
            for row in cursor.fetchall():
                # For each signal, fetch its associated event if event_id exists
                event_id = row["event_id"]
                if event_id:
                    cursor.execute("SELECT * FROM events WHERE id = ?", (event_id,))
                    event_row = cursor.fetchone()
                    if event_row:
                        event = self._row_to_market_event(event_row)
                    else:
                        # Event deleted or missing - skip signal
                        continue
                else:
                    # No event_id - create minimal event from signal data
                    event = MarketEvent(
                        source="unknown",
                        platform="unknown",
                        market_id=row["market_id"],
                        title=row["market_id"],
                        timestamp=datetime.fromisoformat(row["detected_at"]),
                    )
                
                signal = SpikeSignal(
                    event=event,
                    score=row["score"],
                    volume_delta=row["volume_delta"],
                    price_move=row["price_move"],
                    baseline_volume_delta=row["baseline_volume_delta"],
                    reason=row["reason"],
                    tier=row["tier"],
                    topic=row["topic"],
                    source_label=row["source_label"],
                    detected_at=datetime.fromisoformat(row["detected_at"]),
                    baseline_1h=row["baseline_1h"],
                    baseline_24h=row["baseline_24h"],
                    price_move_1m=row["price_move_1m"],
                    price_move_5m=row["price_move_5m"],
                    price_move_30m=row["price_move_30m"],
                    leading_events=[
                        self._dict_to_market_event(item)
                        for item in json.loads(row["leading_events_json"] or "[]")
                    ],
                )
                signals.append(signal)
            
            # Get feed health
            cursor.execute("SELECT * FROM feed_health")
            feeds = {}
            for row in cursor.fetchall():
                feeds[row["feed_name"]] = {
                    "running": bool(row["running"]),
                    "detail": row["detail"],
                    "last_event_at": row["last_event_at"],
                    "error_count": row["error_count"],
                    "reconnects": row["reconnects"],
                }
            
            # Compute summary stats from activity
            live_events = sum(1 for e in all_recent if e.live)
            trade_events = sum(1 for e in all_recent if e.event_kind == "trade")
            source_counts: dict[str, int] = {}
            for e in all_recent:
                source_counts[e.source] = source_counts.get(e.source, 0) + 1
            
            return {
                "markets": [e.to_dict() for e in markets],
                "activity": [e.to_dict() for e in activity],
                "signals": [s.to_dict() for s in signals],
                "feeds": feeds,
                "summary": {
                    "live_events": live_events,
                    "trade_events": trade_events,
                    "sources": source_counts,
                },
            }
    
    def _dedupe_events(self, events: list[MarketEvent]) -> list[MarketEvent]:
        """Remove duplicate events while preserving recency order."""
        deduped: list[MarketEvent] = []
        seen: set[tuple[Any, ...]] = set()

        for event in events:
            key = (
                event.source,
                event.platform,
                event.market_id,
                event.event_kind,
                event.timestamp.isoformat(),
                event.trade_size,
                event.yes_price,
                event.volume,
            )
            if key in seen:
                continue
            seen.add(key)
            deduped.append(event)

        return deduped

    def _dict_to_market_event(self, payload: dict[str, Any]) -> MarketEvent:
        """Convert a serialized event dict back into a MarketEvent."""
        return MarketEvent(
            source=str(payload.get("source") or "unknown"),
            platform=str(payload.get("platform") or "unknown"),
            market_id=str(payload.get("market_id") or "unknown"),
            title=str(payload.get("title") or payload.get("market_id") or "unknown"),
            event_kind=str(payload.get("event_kind") or "quote"),
            yes_price=payload.get("yes_price"),
            no_price=payload.get("no_price"),
            volume=payload.get("volume"),
            volume_kind=str(payload.get("volume_kind") or "cumulative"),
            trade_size=payload.get("trade_size"),
            trade_side=payload.get("trade_side"),
            liquidity=payload.get("liquidity"),
            live=bool(payload.get("live", True)),
            topic=payload.get("topic"),
            market_url=payload.get("market_url"),
            timestamp=datetime.fromisoformat(str(payload.get("timestamp"))),
            metadata=payload.get("metadata") or {},
        )

    def _row_to_market_event(self, row: sqlite3.Row, offset: int = 0) -> MarketEvent:
        """Convert database row to MarketEvent, optionally with column offset."""
        keys = row.keys()
        
        def get(name: str, default=None):
            # Try with offset first, then without
            if offset > 0:
                try:
                    idx = keys.index(name, offset)
                    return row[idx]
                except (ValueError, IndexError):
                    pass
            try:
                return row[name]
            except (KeyError, IndexError):
                return default
        
        metadata = get("metadata_json")
        return MarketEvent(
            source=get("source"),
            platform=get("platform"),
            market_id=get("market_id"),
            title=get("title"),
            event_kind=get("event_kind"),
            yes_price=get("yes_price"),
            no_price=get("no_price"),
            volume=get("volume"),
            volume_kind=get("volume_kind", "cumulative"),
            trade_size=get("trade_size"),
            trade_side=get("trade_side"),
            liquidity=get("liquidity"),
            live=bool(get("live", 1)),
            topic=get("topic"),
            market_url=get("market_url"),
            timestamp=datetime.fromisoformat(get("timestamp")),
            metadata=json.loads(metadata) if metadata else {},
        )
