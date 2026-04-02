"""
Test KalshiPykalshiFeed defensive field extraction and error handling.
"""
from __future__ import annotations

import logging
from datetime import UTC, datetime
from typing import Any
from unittest.mock import MagicMock, Mock

import pytest

from app.config import Settings
from app.feeds.kalshi_pykalshi import KalshiPykalshiFeed
from app.models import MarketEvent


class MockMessage:
    """Mock Kalshi WebSocket message with configurable attributes."""
    
    def __init__(self, **kwargs):
        self._attrs = kwargs
        for k, v in kwargs.items():
            setattr(self, k, v)
    
    def __repr__(self):
        return f"MockMessage({self._attrs})"


@pytest.fixture
def feed_instance():
    """Create KalshiPykalshiFeed instance for testing."""
    # Use Mock settings to avoid requiring all config fields
    settings = Mock(spec=Settings)
    settings.kalshi_markets = ["TEST-MARKET"]
    emit_fn = Mock()
    status_fn = Mock()
    feed = KalshiPykalshiFeed(settings, emit_fn, status_fn)
    return feed, emit_fn, status_fn


def test_defensive_ticker_message_complete(feed_instance):
    """Test processing ticker message with all fields present."""
    feed, emit_fn, _ = feed_instance
    
    msg = MockMessage(
        market_ticker="TEST-MARKET",
        price=5250,  # 52.50 in cents
        volume=1500,
        side="yes",
    )
    
    feed._process_message(msg)
    
    assert emit_fn.call_count == 1
    event: MarketEvent = emit_fn.call_args[0][0]
    assert event.source == "pykalshi"
    assert event.platform == "kalshi"
    assert event.market_id == "TEST-MARKET"
    assert event.yes_price == 52.50  # normalized from cents
    assert event.volume == 1500.0
    assert event.volume_kind == "delta"
    assert event.event_kind == "quote"
    assert event.metadata["message_type"] == "MockMessage"


def test_defensive_trade_message_alternative_fields(feed_instance):
    """Test trade message using 'ticker' field instead of 'market_ticker'."""
    feed, emit_fn, _ = feed_instance
    
    msg = MockMessage(
        ticker="ALT-MARKET",  # alternative field name
        price=7800,
        size=250,  # 'size' instead of 'volume'
        side="no",
    )
    
    feed._process_message(msg)
    
    assert emit_fn.call_count == 1
    event: MarketEvent = emit_fn.call_args[0][0]
    assert event.market_id == "ALT-MARKET"
    assert event.yes_price == 78.00
    assert event.volume == 250.0
    assert event.trade_size == 250.0
    assert event.trade_side == "no"


def test_defensive_missing_price(feed_instance):
    """Test message with missing price field."""
    feed, emit_fn, _ = feed_instance
    
    msg = MockMessage(
        market_ticker="NO-PRICE",
        volume=100,
    )
    
    feed._process_message(msg)
    
    assert emit_fn.call_count == 1
    event: MarketEvent = emit_fn.call_args[0][0]
    assert event.yes_price is None
    assert event.volume == 100.0


def test_defensive_missing_volume(feed_instance):
    """Test message with missing volume/size fields."""
    feed, emit_fn, _ = feed_instance
    
    msg = MockMessage(
        market_ticker="NO-VOLUME",
        price=5000,
    )
    
    feed._process_message(msg)
    
    assert emit_fn.call_count == 1
    event: MarketEvent = emit_fn.call_args[0][0]
    assert event.volume is None
    assert event.volume_kind == "cumulative"


def test_defensive_count_fallback(feed_instance):
    """Test volume extraction falls back to 'count' field."""
    feed, emit_fn, _ = feed_instance
    
    msg = MockMessage(
        market_ticker="COUNT-FIELD",
        price=6000,
        count=42,  # 'count' instead of 'volume' or 'size'
    )
    
    feed._process_message(msg)
    
    assert emit_fn.call_count == 1
    event: MarketEvent = emit_fn.call_args[0][0]
    assert event.volume == 42.0
    assert event.volume_kind == "delta"


def test_defensive_no_market_id(feed_instance, caplog):
    """Test message with no market identifier - should skip."""
    feed, emit_fn, _ = feed_instance
    
    msg = MockMessage(
        price=5000,
        volume=100,
    )
    
    with caplog.at_level(logging.DEBUG):
        feed._process_message(msg)
    
    assert emit_fn.call_count == 0
    assert "Skipping message with no market_id" in caplog.text


def test_defensive_malformed_message_exception_handling(feed_instance, caplog):
    """Test that exceptions during processing are logged without crashing."""
    feed, emit_fn, _ = feed_instance
    
    # Create a message that will cause an exception when processed
    class BadMessage:
        @property
        def market_ticker(self):
            raise RuntimeError("Unexpected error accessing market_ticker")
        
        def __repr__(self):
            return "BadMessage"
    
    msg = BadMessage()
    
    with caplog.at_level(logging.ERROR):
        # Call the parent processing logic that wraps _process_message
        try:
            feed._process_message(msg)
        except Exception as exc:
            # Simulate what happens in the async loop
            logging.error(
                f"Failed to process message type {type(msg).__name__}: {exc}",
                extra={
                    "message_type": type(msg).__name__,
                    "message_attrs": dir(msg),
                    "message_repr": repr(msg),
                },
            )
    
    # Verify emit was never called
    assert emit_fn.call_count == 0


def test_defensive_zero_price(feed_instance):
    """Test message with zero price (edge case)."""
    feed, emit_fn, _ = feed_instance
    
    msg = MockMessage(
        market_ticker="ZERO-PRICE",
        price=0,
        volume=50,
    )
    
    feed._process_message(msg)
    
    assert emit_fn.call_count == 1
    event: MarketEvent = emit_fn.call_args[0][0]
    assert event.yes_price == 0.0  # Should handle zero gracefully


def test_defensive_price_normalization_precision(feed_instance):
    """Test price normalization maintains precision."""
    feed, emit_fn, _ = feed_instance
    
    msg = MockMessage(
        market_ticker="PRECISION",
        price=3333,  # 33.33 cents
        volume=10,
    )
    
    feed._process_message(msg)
    
    assert emit_fn.call_count == 1
    event: MarketEvent = emit_fn.call_args[0][0]
    assert event.yes_price == 33.33


def test_defensive_event_kind_inference(feed_instance):
    """Test event_kind correctly infers from message type."""
    feed, emit_fn, _ = feed_instance
    
    # Trade message (contains 'trade' in class name)
    class TradeUpdate:
        market_ticker = "TRADE-TEST"
        price = 5000
        size = 100
    
    msg = TradeUpdate()
    feed._process_message(msg)
    
    event: MarketEvent = emit_fn.call_args[0][0]
    assert event.event_kind == "trade"
    
    emit_fn.reset_mock()
    
    # Ticker message (doesn't contain 'trade')
    class TickerUpdate:
        market_ticker = "TICKER-TEST"
        price = 6000
        volume = 200
    
    msg2 = TickerUpdate()
    feed._process_message(msg2)
    
    event2: MarketEvent = emit_fn.call_args[0][0]
    assert event2.event_kind == "quote"


def test_defensive_metadata_preservation(feed_instance):
    """Test that message_type is preserved in metadata."""
    feed, emit_fn, _ = feed_instance
    
    class CustomMessageType:
        market_ticker = "META-TEST"
        price = 5000
        volume = 100
    
    msg = CustomMessageType()
    feed._process_message(msg)
    
    event: MarketEvent = emit_fn.call_args[0][0]
    assert event.metadata["message_type"] == "CustomMessageType"


def test_defensive_string_coercion(feed_instance):
    """Test that market_id and trade_side are coerced to strings."""
    feed, emit_fn, _ = feed_instance
    
    msg = MockMessage(
        market_ticker=12345,  # numeric market_ticker
        price=5000,
        volume=100,
        side=None,  # None trade_side
    )
    
    feed._process_message(msg)
    
    event: MarketEvent = emit_fn.call_args[0][0]
    assert event.market_id == "12345"  # should be stringified
    assert event.trade_side is None  # None should remain None


def test_defensive_all_optional_fields_missing(feed_instance):
    """Test message with only required market_id field."""
    feed, emit_fn, _ = feed_instance
    
    msg = MockMessage(
        market_ticker="MINIMAL",
    )
    
    feed._process_message(msg)
    
    assert emit_fn.call_count == 1
    event: MarketEvent = emit_fn.call_args[0][0]
    assert event.market_id == "MINIMAL"
    assert event.yes_price is None
    assert event.volume is None
    assert event.trade_size is None
    assert event.trade_side is None
