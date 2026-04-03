#!/usr/bin/env python3
"""Test script to verify pykalshi WebSocket connection and message schema."""

import asyncio
import logging
import sys
from datetime import datetime

# Configure logging with UTF-8 encoding for Windows console compatibility
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('output.log', mode='w', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
log = logging.getLogger(__name__)

# Windows console compatibility
OK = "[OK]"
FAIL = "[FAIL]"
WARN = "[WARN]"


async def run_connection_test():
    """
    Connect to Kalshi WebSocket, subscribe to one test market, and observe message schemas.
    
    This test validates:
    - pykalshi imports successfully
    - WebSocket connection can be established
    - Subscription to a market works
    - Messages arrive with expected structure
    """
    try:
        from pykalshi import Feed, KalshiClient
        log.info(f"{OK} pykalshi imported successfully")
    except ImportError as e:
        log.error(f"{FAIL} Failed to import pykalshi: {e}")
        log.error("  Install with: py -m pip install -e .[integrations]")
        return False

    # Use a popular market that's likely to have activity
    # KXBTC is a Bitcoin market that typically has volume
    test_market = "KXBTC-26DEC31"
    
    try:
        log.info("Creating KalshiClient...")
        client = KalshiClient()
        log.info(f"{OK} KalshiClient created")
        
        log.info(f"Connecting to Kalshi WebSocket feed...")
        async with Feed(client) as feed:
            log.info(f"{OK} Connected to Kalshi WebSocket")
            
            log.info(f"Subscribing to ticker: {test_market}")
            await feed.subscribe_ticker(test_market)
            log.info(f"{OK} Subscribed to ticker updates for {test_market}")
            
            log.info(f"Subscribing to trades: {test_market}")
            await feed.subscribe_trades(test_market)
            log.info(f"{OK} Subscribed to trade updates for {test_market}")
            
            log.info("Waiting for messages (max 30 seconds)...")
            message_count = 0
            max_messages = 5
            
            try:
                async with asyncio.timeout(30):
                    async for message in feed:
                        message_count += 1
                        message_type = type(message).__name__
                        
                        log.info(f"\n--- Message {message_count} ({message_type}) ---")
                        
                        # Document all available attributes
                        attrs = {k: v for k, v in vars(message).items() if not k.startswith('_')}
                        for key, value in sorted(attrs.items()):
                            log.info(f"  {key}: {value!r}")
                        
                        # Extract key fields for MarketEvent normalization
                        market_id = getattr(message, 'market_ticker', None) or getattr(message, 'ticker', None)
                        price_cents = getattr(message, 'price', None)
                        volume = getattr(message, 'volume', None)
                        size = getattr(message, 'size', None)
                        count = getattr(message, 'count', None)
                        side = getattr(message, 'side', None)
                        
                        log.info(f"\nExtracted fields:")
                        log.info(f"  market_id: {market_id}")
                        log.info(f"  price_cents: {price_cents}")
                        log.info(f"  volume: {volume}")
                        log.info(f"  size: {size}")
                        log.info(f"  count: {count}")
                        log.info(f"  side: {side}")
                        
                        if message_count >= max_messages:
                            log.info(f"\n{OK} Received {message_count} messages, test complete")
                            break
                            
            except TimeoutError:
                if message_count == 0:
                    log.warning(f"{WARN} No messages received within 30 seconds")
                    log.warning(f"  This might indicate:")
                    log.warning(f"  - Market {test_market} has no current activity")
                    log.warning(f"  - Authentication issues (check KALSHI_API_KEY_ID and KALSHI_PRIVATE_KEY_PATH)")
                    log.warning(f"  - Network connectivity issues")
                    return False
                else:
                    log.info(f"{OK} Timeout reached after receiving {message_count} messages")
        
        log.info("\n" + "="*60)
        log.info(f"{OK} Connection test PASSED")
        log.info(f"  - Successfully connected to Kalshi WebSocket")
        log.info(f"  - Subscribed to {test_market}")
        log.info(f"  - Received {message_count} message(s)")
        log.info("="*60)
        return True
        
    except ValueError as e:
        if "API key ID required" in str(e):
            log.error(f"\n{FAIL} Missing credentials")
            log.error(f"  {e}")
            log.error(f"\nTo test with real credentials:")
            log.error(f"  1. Set KALSHI_API_KEY_ID environment variable")
            log.error(f"  2. Set KALSHI_PRIVATE_KEY_PATH to your key file")
            log.error(f"  3. Re-run this test")
            log.error(f"\nWithout credentials, we've verified:")
            log.error(f"  {OK} pykalshi library is installed")
            log.error(f"  {OK} Import succeeds")
            log.error(f"  {OK} Client initialization validates credentials")
            return False
        else:
            log.error(f"\n{FAIL} Connection test FAILED: {e}")
            log.exception("Full traceback:")
            return False
        
    except Exception as e:
        log.error(f"\n{FAIL} Connection test FAILED: {e}")
        log.exception("Full traceback:")
        return False


def main():
    """Run the connection test."""
    log.info("Starting Kalshi WebSocket connection test...")
    log.info(f"Timestamp: {datetime.now().isoformat()}")
    
    success = asyncio.run(run_connection_test())
    
    if success:
        log.info("\nTest completed successfully!")
        sys.exit(0)
    else:
        log.error("\nTest failed. See output.log for details.")
        sys.exit(1)


if __name__ == "__main__":
    main()
