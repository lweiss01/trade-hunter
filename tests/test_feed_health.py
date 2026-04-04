"""Tests for feed health status reporting."""

from __future__ import annotations

import asyncio
from datetime import UTC, datetime
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.config import Settings
from app.feeds.kalshi_pykalshi import KalshiPykalshiFeed
from app.store import MarketStore


@pytest.fixture
def settings():
    return Settings(
        host="127.0.0.1",
        port=8765,
        enable_simulation=True,
        enable_kalshi=True,
        discord_webhook_url=None,
        discord_webhook_routes={},
        ingest_api_token=None,
        spike_min_volume_delta=120.0,
        spike_min_price_move=0.03,
        spike_score_threshold=3.0,
        spike_baseline_points=24,
        spike_cooldown_seconds=300,
        kalshi_markets=["TEST-MARKET"],
        kalshi_api_key_id=None,
        kalshi_private_key_path=None,
    )


@pytest.fixture
def store():
    return MarketStore()


@pytest.fixture
def mock_emit():
    return MagicMock()


@pytest.fixture
def mock_publish_status():
    return MagicMock()


@pytest.fixture
def feed(settings, mock_emit, mock_publish_status):
    return KalshiPykalshiFeed(settings, mock_emit, mock_publish_status)


def test_initial_state(feed):
    """Feed should initialize health tracking fields."""
    assert feed._last_event_at is None
    assert feed._error_count == 0
    assert feed._reconnects == 0


def test_stop_publishes_status(feed, mock_publish_status):
    """stop() should publish status with all health fields."""
    feed.stop()
    
    mock_publish_status.assert_called_once()
    name, payload = mock_publish_status.call_args[0]
    
    assert name == "kalshi-pykalshi"
    assert payload["running"] is False
    assert payload["detail"] == "stopped"
    assert payload["last_event_at"] is None
    assert payload["error_count"] == 0
    assert payload["reconnects"] == 0


def test_import_error_increments_error_count(feed, mock_publish_status):
    """ImportError should increment error_count and publish status."""
    with patch.object(feed, "_run", new=AsyncMock(side_effect=ImportError("no pykalshi"))):
        feed._run_loop()
    
    assert feed._error_count == 1
    
    mock_publish_status.assert_called_once()
    name, payload = mock_publish_status.call_args[0]
    
    assert name == "kalshi-pykalshi"
    assert payload["running"] is False
    assert "pykalshi is not installed" in payload["detail"]
    assert payload["error_count"] == 1


def test_generic_error_increments_error_count(feed, mock_publish_status):
    """Generic Exception should increment error_count and publish reconnect status once."""
    with patch.object(feed, "_run", new=AsyncMock(side_effect=ValueError("boom"))):
        with patch.object(feed, "_sleep_with_stop", new=AsyncMock(return_value=True)):
            feed._run_loop()

    assert feed._error_count == 1
    assert feed._reconnects == 1

    mock_publish_status.assert_called_once()
    name, payload = mock_publish_status.call_args[0]

    assert name == "kalshi-pykalshi"
    assert payload["running"] is False
    assert "error: boom (reconnecting in 5s)" == payload["detail"]
    assert payload["error_count"] == 1
    assert payload["reconnects"] == 1


@pytest.mark.asyncio
async def test_no_markets_configured(mock_emit, mock_publish_status):
    """Should publish status and exit when no markets configured."""
    settings = Settings(
        host="127.0.0.1",
        port=8765,
        enable_simulation=True,
        enable_kalshi=True,
        discord_webhook_url=None,
        discord_webhook_routes={},
        ingest_api_token=None,
        spike_min_volume_delta=120.0,
        spike_min_price_move=0.03,
        spike_score_threshold=3.0,
        spike_baseline_points=24,
        spike_cooldown_seconds=300,
        kalshi_markets=[],  # Empty markets
        kalshi_api_key_id=None,
        kalshi_private_key_path=None,
    )
    feed = KalshiPykalshiFeed(settings, mock_emit, mock_publish_status)
    
    await feed._run()
    
    mock_publish_status.assert_called_once()
    name, payload = mock_publish_status.call_args[0]
    
    assert name == "kalshi-pykalshi"
    assert payload["running"] is False
    assert payload["detail"] == "no KALSHI_MARKETS configured"


@pytest.mark.asyncio
async def test_start_publishes_status(settings, mock_emit, mock_publish_status):
    """Should publish status on successful feed start."""
    feed = KalshiPykalshiFeed(settings, mock_emit, mock_publish_status)

    # Mock pykalshi Feed to yield zero messages then stop
    mock_feed_instance = AsyncMock()
    mock_feed_instance.__aenter__ = AsyncMock(return_value=mock_feed_instance)
    mock_feed_instance.__aexit__ = AsyncMock(return_value=None)
    mock_feed_instance.subscribe_ticker = AsyncMock()
    mock_feed_instance.subscribe_trades = AsyncMock()

    async def async_iter():
        if False:
            yield  # Empty generator

    mock_feed_instance.__aiter__ = lambda self: async_iter()

    async def mock_validate():
        return (["TEST-MARKET"], [])

    with patch("pykalshi.Feed", return_value=mock_feed_instance):
        with patch("pykalshi.KalshiClient"):
            with patch.object(feed, "_validate_tickers", side_effect=mock_validate):
                await feed._run()

    # Should publish status once on start
    mock_publish_status.assert_called_once()
    name, payload = mock_publish_status.call_args[0]

    assert name == "kalshi-pykalshi"
    assert payload["running"] is True
    assert payload["error_count"] == 0


@pytest.mark.asyncio
async def test_message_updates_last_event_at(settings, mock_emit, mock_publish_status):
    """Should update last_event_at timestamp on each message."""
    feed = KalshiPykalshiFeed(settings, mock_emit, mock_publish_status)

    # Mock message shaped like a real TickerMessage so _process_message emits
    mock_message = MagicMock()
    mock_message.market_ticker = "TEST-MARKET"
    mock_message.yes_bid_dollars = 0.52
    mock_message.price_dollars = 0.52
    mock_message.volume_fp = 100.0
    type(mock_message).__name__ = "TickerMessage"

    # Mock pykalshi Feed to yield one message
    mock_feed_instance = AsyncMock()
    mock_feed_instance.__aenter__ = AsyncMock(return_value=mock_feed_instance)
    mock_feed_instance.__aexit__ = AsyncMock(return_value=None)
    mock_feed_instance.subscribe_ticker = AsyncMock()
    mock_feed_instance.subscribe_trades = AsyncMock()

    async def async_iter():
        yield mock_message
        feed._stop.set()  # Stop after one message

    mock_feed_instance.__aiter__ = lambda self: async_iter()

    before = datetime.now(UTC)

    async def mock_validate():
        return (["TEST-MARKET"], [])

    with patch("pykalshi.Feed", return_value=mock_feed_instance):
        with patch("pykalshi.KalshiClient"):
            with patch.object(feed, "_validate_tickers", side_effect=mock_validate):
                await feed._run()

    after = datetime.now(UTC)

    # last_event_at should be updated
    assert feed._last_event_at is not None
    assert before <= feed._last_event_at <= after

    # emit should have been called
    mock_emit.assert_called_once()


@pytest.mark.asyncio
async def test_malformed_message_does_not_update_last_event_at(settings, mock_emit, mock_publish_status):
    """Should not update last_event_at when message processing raises."""
    feed = KalshiPykalshiFeed(settings, mock_emit, mock_publish_status)
    
    # Mock message that will cause _process_message to raise
    mock_message = MagicMock()
    
    # Mock pykalshi Feed to yield one malformed message
    mock_feed_instance = AsyncMock()
    mock_feed_instance.__aenter__ = AsyncMock(return_value=mock_feed_instance)
    mock_feed_instance.__aexit__ = AsyncMock(return_value=None)
    mock_feed_instance.subscribe_ticker = AsyncMock()
    mock_feed_instance.subscribe_trades = AsyncMock()
    
    async def async_iter():
        yield mock_message
        feed._stop.set()  # Stop after one message
    
    mock_feed_instance.__aiter__ = lambda self: async_iter()
    
    with patch("pykalshi.Feed", return_value=mock_feed_instance):
        with patch("pykalshi.KalshiClient"):
            with patch.object(feed, "_process_message", side_effect=ValueError("bad schema")):
                await feed._run()
    
    # last_event_at should NOT be updated
    assert feed._last_event_at is None
    
    # emit should not have been called
    mock_emit.assert_not_called()


def test_store_persists_feed_status(store):
    """MarketStore should persist feed status via update_feed_status."""
    store.update_feed_status("test-feed", {
        "running": True,
        "detail": "healthy",
        "last_event_at": "2024-01-01T00:00:00Z",
        "error_count": 0,
        "reconnects": 2,
    })
    
    state = store.dashboard_state()
    assert "feeds" in state
    assert "test-feed" in state["feeds"]
    
    feed_status = state["feeds"]["test-feed"]
    assert feed_status["running"] is True
    assert feed_status["detail"] == "healthy"
    assert feed_status["error_count"] == 0
    assert feed_status["reconnects"] == 2
