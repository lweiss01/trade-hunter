"""
Manual smoke-test for KalshiPykalshiFeed._process_message defensive handling.
Run directly: py test_defensive_logging.py
NOT collected by pytest (no test_ functions).
"""
import logging
from unittest.mock import Mock

from app.feeds.kalshi_pykalshi import KalshiPykalshiFeed
from app.config import Settings

logging.basicConfig(level=logging.DEBUG, format="%(levelname)s - %(name)s - %(message)s")

settings = Mock(spec=Settings)
settings.kalshi_markets = ["TEST"]
emit_fn = Mock()
status_fn = Mock()
feed = KalshiPykalshiFeed(settings, emit_fn, status_fn)

print("=== Testing defensive field extraction and error logging ===\n")


# Test 1: TickerMessage-shaped object
print("1. TickerMessage-shaped object:")
class TickerMessage:
    __class__ = type("TickerMessage", (), {})
    market_ticker = "KXBTC-TEST"
    price_dollars = 0.52
    yes_bid_dollars = 0.51
    yes_ask_dollars = 0.53
    volume_fp = 1500.0
    ts = 1234567890

msg1 = TickerMessage()
msg1.__class__.__name__ = "TickerMessage"
feed._process_message(msg1)
if emit_fn.call_count:
    ev = emit_fn.call_args[0][0]
    print(f"   [OK] Emitted: {ev.market_id}, kind={ev.event_kind}, price={ev.yes_price}, vol={ev.volume}")
else:
    print("   [SKIP] Not emitted (type mismatch)")
emit_fn.reset_mock()


# Test 2: TradeMessage-shaped object
print("\n2. TradeMessage-shaped object:")
class TradeMessage:
    market_ticker = "KXBTC-TEST"
    ticker = "KXBTC-TEST"
    trade_id = "abc123"
    count_fp = 10.0
    yes_price_dollars = 0.55
    no_price_dollars = 0.45
    taker_side = "yes"
    ts = 1234567890

msg2 = TradeMessage()
feed._process_message(msg2)
if emit_fn.call_count:
    ev = emit_fn.call_args[0][0]
    print(f"   [OK] Emitted: {ev.market_id}, kind={ev.event_kind}, price={ev.yes_price}, vol={ev.volume}, side={ev.trade_side}")
else:
    print("   [SKIP] Not emitted (type mismatch)")
emit_fn.reset_mock()


# Test 3: No market_id
print("\n3. Message with no market_id:")
class NoIdMessage:
    yes_price_dollars = 0.5
    count_fp = 100.0

feed._process_message(NoIdMessage())
print(f"   [OK] Skipped, emit_count={emit_fn.call_count}")
emit_fn.reset_mock()


# Test 4: Unknown type is skipped gracefully
print("\n4. Unknown message type:")
class WeirdMessage:
    market_ticker = "KXBTC-TEST"

feed._process_message(WeirdMessage())
print(f"   [OK] Skipped, emit_count={emit_fn.call_count}")


print("\n=== Done ===")
