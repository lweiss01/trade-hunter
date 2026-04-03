"""Tests for SQLite-backed MarketStore."""
from __future__ import annotations

from datetime import UTC, datetime

import pytest

from app.models import MarketEvent, SpikeSignal
from app.store import MarketStore


def test_add_event_and_retrieve(test_db):
    """Test adding event and retrieving from dashboard_state."""
    store = MarketStore(db_path=None)
    store._conn = test_db  # Use test database
    
    event = MarketEvent(
        source="test",
        platform="polymarket",
        market_id="test-market-1",
        title="Test Market",
        yes_price=0.55,
        volume=1000,
        timestamp=datetime.now(UTC),
    )
    
    store.upsert_event(event)
    
    state = store.dashboard_state()
    
    assert len(state["markets"]) == 1
    assert state["markets"][0]["market_id"] == "test-market-1"
    assert state["markets"][0]["yes_price"] == 0.55


def test_get_recent_events(test_db):
    """Test retrieving recent events in correct order."""
    store = MarketStore(db_path=None)
    store._conn = test_db
    
    # Add 3 events
    for i in range(3):
        event = MarketEvent(
            source="test",
            platform="polymarket",
            market_id=f"market-{i}",
            title=f"Market {i}",
            timestamp=datetime.now(UTC),
        )
        store.upsert_event(event)
    
    state = store.dashboard_state()
    
    # Activity shows most recent first
    assert len(state["activity"]) == 3
    assert state["activity"][0]["market_id"] == "market-2"
    assert state["activity"][2]["market_id"] == "market-0"


def test_record_signal(test_db):
    """Test recording spike signal."""
    store = MarketStore(db_path=None)
    store._conn = test_db
    
    event = MarketEvent(
        source="test",
        platform="polymarket",
        market_id="spike-market",
        title="Spike Market",
        yes_price=0.45,
        volume=5000,
        volume_kind="delta",
        timestamp=datetime.now(UTC),
    )
    store.upsert_event(event)
    
    signal = SpikeSignal(
        event=event,
        score=5.2,
        volume_delta=4500,
        price_move=0.12,
        baseline_volume_delta=450,
        reason="Large volume spike",
        tier="alert",
        detected_at=datetime.now(UTC),
    )
    store.record_signal(signal)
    
    state = store.dashboard_state()
    
    assert len(state["signals"]) == 1
    assert state["signals"][0]["score"] == 5.2
    assert state["signals"][0]["reason"] == "Large volume spike"


def test_update_feed_status(test_db):
    """Test feed health status upsert."""
    store = MarketStore(db_path=None)
    store._conn = test_db
    
    status1 = {
        "running": True,
        "detail": "feed active",
        "last_event_at": datetime.now(UTC).isoformat(),
        "error_count": 0,
        "reconnects": 0,
    }
    store.update_feed_status("test-feed", status1)
    
    state = store.dashboard_state()
    assert "test-feed" in state["feeds"]
    assert state["feeds"]["test-feed"]["running"] is True
    assert state["feeds"]["test-feed"]["error_count"] == 0
    
    # Update same feed
    status2 = {
        "running": False,
        "detail": "feed stopped",
        "error_count": 1,
    }
    store.update_feed_status("test-feed", status2)
    
    state = store.dashboard_state()
    assert state["feeds"]["test-feed"]["running"] is False
    assert state["feeds"]["test-feed"]["error_count"] == 1


def test_market_metadata_upsert(test_db):
    """Test market metadata updates on repeated events."""
    store = MarketStore(db_path=None)
    store._conn = test_db
    
    event1 = MarketEvent(
        source="test",
        platform="polymarket",
        market_id="repeated-market",
        title="Market Title",
        yes_price=0.50,
        volume=100,
        timestamp=datetime.now(UTC),
    )
    store.upsert_event(event1)
    
    event2 = MarketEvent(
        source="test",
        platform="polymarket",
        market_id="repeated-market",
        title="Market Title",
        yes_price=0.60,
        volume=200,
        timestamp=datetime.now(UTC),
    )
    store.upsert_event(event2)
    
    # Query markets table directly
    cursor = test_db.cursor()
    cursor.execute("SELECT total_events, last_yes_price FROM markets WHERE market_id = ?", ("repeated-market",))
    row = cursor.fetchone()
    
    assert row["total_events"] == 2
    assert row["last_yes_price"] == 0.60


def test_metadata_json_preserved(test_db):
    """Test event metadata is serialized and deserialized correctly."""
    store = MarketStore(db_path=None)
    store._conn = test_db
    
    event = MarketEvent(
        source="test",
        platform="polymarket",
        market_id="meta-market",
        title="Metadata Test",
        metadata={"custom_field": "value", "nested": {"key": 123}},
        timestamp=datetime.now(UTC),
    )
    store.upsert_event(event)
    
    state = store.dashboard_state()
    retrieved = state["markets"][0]
    
    assert retrieved["metadata"]["custom_field"] == "value"
    assert retrieved["metadata"]["nested"]["key"] == 123


def test_dashboard_limits(test_db):
    """Test dashboard respects limits (50 markets, 24 activity)."""
    store = MarketStore(db_path=None)
    store._conn = test_db
    
    # Add 60 events to different markets
    for i in range(60):
        event = MarketEvent(
            source="test",
            platform="test",
            market_id=f"market-{i}",
            title=f"Market {i}",
            timestamp=datetime.now(UTC),
        )
        store.upsert_event(event)
    
    state = store.dashboard_state()
    
    assert len(state["markets"]) == 50  # Limit to 50
    assert len(state["activity"]) == 24  # Limit to 24


def test_source_counts_in_summary(test_db):
    """Test summary includes source counts."""
    store = MarketStore(db_path=None)
    store._conn = test_db
    
    for source in ["polyalerthub", "kalshi", "polyalerthub"]:
        event = MarketEvent(
            source=source,
            platform="test",
            market_id=f"market-{source}",
            title="Test",
            timestamp=datetime.now(UTC),
        )
        store.upsert_event(event)
    
    state = store.dashboard_state()
    
    assert state["summary"]["sources"]["polyalerthub"] == 2
    assert state["summary"]["sources"]["kalshi"] == 1
