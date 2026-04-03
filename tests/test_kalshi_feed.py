"""
Test KalshiPykalshiFeed message processing against actual pykalshi message schemas.
TickerMessage fields: market_ticker, price_dollars, yes_bid_dollars, yes_ask_dollars, volume_fp
TradeMessage fields:  market_ticker, ticker, trade_id, count_fp, yes_price_dollars, no_price_dollars, taker_side
"""
from __future__ import annotations

import logging
from datetime import UTC, datetime
from unittest.mock import Mock

import pytest

from app.config import Settings
from app.feeds.kalshi_pykalshi import KalshiPykalshiFeed
from app.models import MarketEvent


class MockTickerMessage:
    """Matches pykalshi.feed.TickerMessage field names."""
    def __init__(self, market_ticker="TEST", yes_bid_dollars=None, price_dollars=None,
                 yes_ask_dollars=None, volume_fp=None, ts=None):
        self.market_ticker = market_ticker
        self.yes_bid_dollars = yes_bid_dollars
        self.price_dollars = price_dollars
        self.yes_ask_dollars = yes_ask_dollars
        self.volume_fp = volume_fp
        self.ts = ts

    # Make type name match what _process_message dispatches on
    class _Meta(type):
        @property
        def __name__(cls): return "TickerMessage"

    def __class_getitem__(cls, item): return cls


# Patch __class__.__name__ for dispatch
MockTickerMessage.__name__ = "TickerMessage"


class MockTradeMessage:
    """Matches pykalshi.feed.TradeMessage field names."""
    def __init__(self, market_ticker="TEST", ticker=None, trade_id=None,
                 count_fp=None, yes_price_dollars=None, no_price_dollars=None, taker_side=None, ts=None):
        self.market_ticker = market_ticker
        self.ticker = ticker or market_ticker
        self.trade_id = trade_id
        self.count_fp = count_fp
        self.yes_price_dollars = yes_price_dollars
        self.no_price_dollars = no_price_dollars
        self.taker_side = taker_side
        self.ts = ts


MockTradeMessage.__name__ = "TradeMessage"


@pytest.fixture
def feed_instance():
    settings = Mock(spec=Settings)
    settings.kalshi_markets = ["TEST-MARKET"]
    emit_fn = Mock()
    status_fn = Mock()
    feed = KalshiPykalshiFeed(settings, emit_fn, status_fn)
    return feed, emit_fn, status_fn


def test_ticker_message_complete(feed_instance):
    """TickerMessage with all fields emits a quote event."""
    feed, emit_fn, _ = feed_instance

    msg = MockTickerMessage(
        market_ticker="TEST-MARKET",
        yes_bid_dollars=0.52,
        yes_ask_dollars=0.54,
        price_dollars=0.53,
        volume_fp=1500.0,
    )

    feed._process_message(msg)

    assert emit_fn.call_count == 1
    event: MarketEvent = emit_fn.call_args[0][0]
    assert event.source == "pykalshi"
    assert event.platform == "kalshi"
    assert event.market_id == "TEST-MARKET"
    assert event.event_kind == "quote"
    assert event.yes_price == 0.52          # yes_bid preferred
    assert event.volume == 1500.0
    assert event.volume_kind == "delta"
    assert event.trade_side is None
    assert event.metadata["message_type"] == "TickerMessage"


def test_ticker_message_falls_back_to_price_dollars(feed_instance):
    """TickerMessage uses price_dollars when yes_bid_dollars is absent."""
    feed, emit_fn, _ = feed_instance

    msg = MockTickerMessage(market_ticker="TEST-MARKET", price_dollars=0.47, volume_fp=300.0)
    feed._process_message(msg)

    assert emit_fn.call_count == 1
    assert emit_fn.call_args[0][0].yes_price == 0.47


def test_ticker_message_missing_volume(feed_instance):
    """TickerMessage without volume_fp emits event with volume=None."""
    feed, emit_fn, _ = feed_instance

    msg = MockTickerMessage(market_ticker="NO-VOL", yes_bid_dollars=0.60)
    feed._process_message(msg)

    assert emit_fn.call_count == 1
    assert emit_fn.call_args[0][0].volume is None


def test_ticker_message_missing_price(feed_instance):
    """TickerMessage without any price fields emits event with yes_price=None."""
    feed, emit_fn, _ = feed_instance

    msg = MockTickerMessage(market_ticker="NO-PRICE", volume_fp=100.0)
    feed._process_message(msg)

    assert emit_fn.call_count == 1
    assert emit_fn.call_args[0][0].yes_price is None


def test_trade_message_complete(feed_instance):
    """TradeMessage with all fields emits a trade event."""
    feed, emit_fn, _ = feed_instance

    msg = MockTradeMessage(
        market_ticker="TEST-MARKET",
        count_fp=10.0,
        yes_price_dollars=0.55,
        taker_side="yes",
    )

    feed._process_message(msg)

    assert emit_fn.call_count == 1
    event: MarketEvent = emit_fn.call_args[0][0]
    assert event.event_kind == "trade"
    assert event.market_id == "TEST-MARKET"
    assert event.yes_price == 0.55
    assert event.volume == 10.0
    assert event.trade_size == 10.0
    assert event.trade_side == "yes"
    assert event.metadata["message_type"] == "TradeMessage"


def test_trade_message_missing_price(feed_instance):
    """TradeMessage without yes_price_dollars emits event with yes_price=None."""
    feed, emit_fn, _ = feed_instance

    msg = MockTradeMessage(market_ticker="TEST-MARKET", count_fp=5.0)
    feed._process_message(msg)

    assert emit_fn.call_count == 1
    assert emit_fn.call_args[0][0].yes_price is None


def test_trade_message_missing_count(feed_instance):
    """TradeMessage without count_fp emits event with volume=None."""
    feed, emit_fn, _ = feed_instance

    msg = MockTradeMessage(market_ticker="TEST-MARKET", yes_price_dollars=0.48)
    feed._process_message(msg)

    assert emit_fn.call_count == 1
    assert emit_fn.call_args[0][0].volume is None


def test_no_market_id_skipped(feed_instance, caplog):
    """Message with no market_ticker and no ticker is skipped."""
    feed, emit_fn, _ = feed_instance

    msg = MockTickerMessage(market_ticker=None)
    msg.market_ticker = None

    with caplog.at_level(logging.DEBUG):
        feed._process_message(msg)

    assert emit_fn.call_count == 0
    assert "no market_id" in caplog.text


def test_unknown_message_type_skipped(feed_instance, caplog):
    """Unknown type name is skipped gracefully."""
    feed, emit_fn, _ = feed_instance

    class WeirdMessage:
        market_ticker = "TEST"

    with caplog.at_level(logging.DEBUG):
        feed._process_message(WeirdMessage())

    assert emit_fn.call_count == 0


def test_zero_price_handled(feed_instance):
    """Zero yes_price_dollars is a valid value, not skipped."""
    feed, emit_fn, _ = feed_instance

    msg = MockTradeMessage(market_ticker="ZERO", yes_price_dollars=0.0, count_fp=10.0)
    feed._process_message(msg)

    assert emit_fn.call_count == 1
    assert emit_fn.call_args[0][0].yes_price == 0.0


def test_market_id_stringified(feed_instance):
    """Numeric market_ticker is coerced to string."""
    feed, emit_fn, _ = feed_instance

    msg = MockTickerMessage(market_ticker=12345, yes_bid_dollars=0.50)
    feed._process_message(msg)

    assert emit_fn.call_count == 1
    assert emit_fn.call_args[0][0].market_id == "12345"
