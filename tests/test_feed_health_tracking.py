"""Tests for PolyAlertHub feed health tracking."""
from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from unittest.mock import Mock

from app.service import TradeHunterService


FIXTURES = Path(__file__).parent / "fixtures"


def _mock_settings():
    """Create a mock Settings object with all required attributes."""
    return Mock(
        enable_simulation=False,
        enable_kalshi=False,
        discord_webhook_url=None,
        discord_webhook_routes={},
        polyalerthub_token=None,
        spike_min_volume_delta=120.0,
        spike_min_price_move=0.03,
        spike_score_threshold=3.0,
        spike_baseline_points=24,
        spike_cooldown_seconds=300,
    )


def test_polyalerthub_feed_status_tracked():
    """Verify polyalerthub feed health status is tracked in store."""
    service = TradeHunterService(_mock_settings())
    
    # Manually update feed status (simulating what server.py does)
    service.store.update_feed_status(
        "polyalerthub",
        {
            "running": True,
            "last_event_at": datetime.now(UTC).isoformat(),
            "detail": "relay endpoint active",
            "error_count": 0,
        }
    )
    
    state = service.dashboard_state()
    
    assert "polyalerthub" in state["feeds"]
    feed_status = state["feeds"]["polyalerthub"]
    assert feed_status["running"] is True
    assert feed_status["detail"] == "relay endpoint active"
    assert feed_status["error_count"] == 0
    assert "last_event_at" in feed_status


def test_polyalerthub_feed_status_shows_error():
    """Verify feed status can track errors."""
    service = TradeHunterService(_mock_settings())
    
    service.store.update_feed_status(
        "polyalerthub",
        {
            "running": False,
            "detail": "error: connection failed",
            "error_count": 1,
        }
    )
    
    state = service.dashboard_state()
    feed_status = state["feeds"]["polyalerthub"]
    
    assert feed_status["running"] is False
    assert "error" in feed_status["detail"]
    assert feed_status["error_count"] == 1


def test_multiple_feed_statuses_tracked():
    """Verify store can track multiple feed statuses simultaneously."""
    service = TradeHunterService(_mock_settings())
    
    service.store.update_feed_status("polyalerthub", {"running": True, "detail": "active"})
    service.store.update_feed_status("simulation", {"running": True, "detail": "sim active"})
    service.store.update_feed_status("discord", {"running": False, "detail": "webhook disabled"})
    
    state = service.dashboard_state()
    
    assert len(state["feeds"]) == 3
    assert "polyalerthub" in state["feeds"]
    assert "simulation" in state["feeds"]
    assert "discord" in state["feeds"]


def test_feed_status_updates_overwrite():
    """Verify feed status updates replace previous status."""
    service = TradeHunterService(_mock_settings())
    
    service.store.update_feed_status("polyalerthub", {"running": False, "detail": "initial"})
    service.store.update_feed_status("polyalerthub", {"running": True, "detail": "updated"})
    
    state = service.dashboard_state()
    feed_status = state["feeds"]["polyalerthub"]
    
    assert feed_status["running"] is True
    assert feed_status["detail"] == "updated"
