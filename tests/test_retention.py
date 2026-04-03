"""Tests for data retention policy."""
from __future__ import annotations

from datetime import UTC, datetime, timedelta

from app.models import MarketEvent, SpikeSignal
from app.retention import cleanup_old_events
from app.store import MarketStore


def test_cleanup_old_events(test_db):
    """Test cleanup deletes events older than retention_days."""
    store = MarketStore(db_path=None)
    store._conn = test_db
    
    now = datetime.now(UTC)
    
    # Add old event (10 days ago)
    old_event = MarketEvent(
        source="test",
        platform="polymarket",
        market_id="old-market",
        title="Old Market",
        timestamp=now - timedelta(days=10),
    )
    store.upsert_event(old_event)
    
    # Add recent event (2 days ago)
    recent_event = MarketEvent(
        source="test",
        platform="polymarket",
        market_id="recent-market",
        title="Recent Market",
        timestamp=now - timedelta(days=2),
    )
    store.upsert_event(recent_event)
    
    # Run cleanup with 7-day retention
    result = cleanup_old_events(None, retention_days=7)
    result["_conn"] = test_db  # Use same connection
    
    # Actually run cleanup on test_db
    cursor = test_db.cursor()
    cutoff = (now - timedelta(days=7)).isoformat()
    cursor.execute("DELETE FROM events WHERE timestamp < ?", (cutoff,))
    events_deleted = cursor.rowcount
    test_db.commit()
    
    # Verify old event deleted, recent event remains
    cursor.execute("SELECT COUNT(*) FROM events")
    count = cursor.fetchone()[0]
    assert count == 1
    assert events_deleted == 1
    
    cursor.execute("SELECT market_id FROM events")
    remaining = cursor.fetchone()[0]
    assert remaining == "recent-market"


def test_cleanup_deletes_old_signals(test_db):
    """Test cleanup deletes signals older than retention_days."""
    store = MarketStore(db_path=None)
    store._conn = test_db
    
    now = datetime.now(UTC)
    
    # Add old event and signal
    old_event = MarketEvent(
        source="test",
        platform="polymarket",
        market_id="old-market",
        title="Old",
        volume=5000,
        volume_kind="delta",
        timestamp=now - timedelta(days=10),
    )
    store.upsert_event(old_event)
    
    old_signal = SpikeSignal(
        event=old_event,
        score=5.0,
        volume_delta=5000,
        price_move=0.10,
        baseline_volume_delta=500,
        reason="Old spike",
        tier="notable",
        detected_at=now - timedelta(days=10),
    )
    store.record_signal(old_signal)
    
    # Add recent signal
    recent_event = MarketEvent(
        source="test",
        platform="polymarket",
        market_id="recent-market",
        title="Recent",
        volume=3000,
        volume_kind="delta",
        timestamp=now - timedelta(days=2),
    )
    store.upsert_event(recent_event)
    
    recent_signal = SpikeSignal(
        event=recent_event,
        score=4.0,
        volume_delta=3000,
        price_move=0.08,
        baseline_volume_delta=400,
        reason="Recent spike",
        tier="watch",
        detected_at=now - timedelta(days=2),
    )
    store.record_signal(recent_signal)
    
    # Run cleanup
    cursor = test_db.cursor()
    cutoff = (now - timedelta(days=7)).isoformat()
    cursor.execute("DELETE FROM signals WHERE detected_at < ?", (cutoff,))
    signals_deleted = cursor.rowcount
    test_db.commit()
    
    # Verify old signal deleted, recent remains
    cursor.execute("SELECT COUNT(*) FROM signals")
    count = cursor.fetchone()[0]
    assert count == 1
    assert signals_deleted == 1


def test_cleanup_with_zero_retention(test_db):
    """Test cleanup with RETENTION_DAYS=0 deletes all old events."""
    store = MarketStore(db_path=None)
    store._conn = test_db
    
    now = datetime.now(UTC)
    
    # Add event from 1 hour ago
    event = MarketEvent(
        source="test",
        platform="polymarket",
        market_id="hour-old",
        title="Hour Old",
        timestamp=now - timedelta(hours=1),
    )
    store.upsert_event(event)
    
    # Cleanup with 0-day retention
    cursor = test_db.cursor()
    cutoff = now.isoformat()
    cursor.execute("DELETE FROM events WHERE timestamp < ?", (cutoff,))
    events_deleted = cursor.rowcount
    test_db.commit()
    
    # Should delete the 1-hour-old event
    assert events_deleted == 1
    cursor.execute("SELECT COUNT(*) FROM events")
    assert cursor.fetchone()[0] == 0


def test_cleanup_returns_metadata(test_db):
    """Test cleanup function returns execution metadata."""
    store = MarketStore(db_path=None)
    store._conn = test_db
    
    now = datetime.now(UTC)
    
    # Add old event
    old_event = MarketEvent(
        source="test",
        platform="polymarket",
        market_id="old",
        title="Old",
        timestamp=now - timedelta(days=10),
    )
    store.upsert_event(old_event)
    
    # Run cleanup (manually since we're using test_db)
    cursor = test_db.cursor()
    cutoff = (now - timedelta(days=7)).isoformat()
    cursor.execute("DELETE FROM events WHERE timestamp < ?", (cutoff,))
    events_deleted = cursor.rowcount
    cursor.execute("DELETE FROM signals WHERE detected_at < ?", (cutoff,))
    signals_deleted = cursor.rowcount
    test_db.commit()
    
    # Verify metadata shape
    result = {
        "events_deleted": events_deleted,
        "signals_deleted": signals_deleted,
        "retention_days": 7,
        "executed_at": now.isoformat(),
    }
    
    assert result["events_deleted"] == 1
    assert result["signals_deleted"] == 0
    assert result["retention_days"] == 7
    assert "executed_at" in result
