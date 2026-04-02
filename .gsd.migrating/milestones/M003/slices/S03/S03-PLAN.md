# S03: Liquidity-Aware Interpretation

**Goal:** Add liquidity context to signal explanations to help distinguish actionable moves from thin-market noise.
**Demo:** After this: Signal cards show liquidity context: bid/ask spread (if available), recent trade count (last 30 min), estimated slippage for $100 position.

## Tasks
- [ ] **T01: Extend MarketEvent metadata with liquidity fields** — 1. Update MarketEvent metadata schema to include liquidity fields:
   - bid_price, ask_price (float, optional)
   - bid_size, ask_size (float, optional - contract count)
2. Update Kalshi adapter to extract bid/ask from ticker messages if available
3. Update PolyAlertHub adapter to extract liquidity fields from payload
4. Gracefully handle missing fields - set to None, don't crash
5. Update tests with liquidity metadata
  - Estimate: 30m
  - Files: app/models.py, app/feeds/kalshi_pykalshi.py
  - Verify: python -c 'from app.models import MarketEvent; e = MarketEvent(source="test", platform="test", market_id="TEST", title="Test", metadata={"bid_price": 0.50}); assert e.metadata.get("bid_price") == 0.50'
- [ ] **T02: Add liquidity metric queries to store** — 1. Add MarketStore method: get_recent_trade_count(market_id, minutes=30)
2. Query events WHERE market_id = ? AND event_kind = 'trade' AND timestamp > now - minutes
3. Return count of trades
4. Add method: calculate_bid_ask_spread(market_id)
5. Get latest event with bid/ask metadata
6. spread_pct = (ask_price - bid_price) / avg(bid_price, ask_price)
7. Return spread_pct or None if no data
  - Estimate: 30m
  - Files: app/store.py
  - Verify: python -m pytest tests/test_liquidity_metrics.py -k recent_trade_count -k bid_ask_spread
- [ ] **T03: Implement slippage estimation logic** — 1. Create app/liquidity.py with estimate_slippage(bid_price, ask_price, bid_size, ask_size, position_value)
2. For $100 position:
   - contracts_needed = position_value / avg_price
   - If buying (bid side): slippage = contracts_needed * (ask_price - mid_price)
   - If bid/ask size insufficient: increase slippage estimate (thin market penalty)
3. Return estimated slippage in dollars
4. Handle missing data: return None
5. Write unit tests with various liquidity scenarios
  - Estimate: 30m
  - Verify: python -m pytest tests/test_slippage.py -v
- [ ] **T04: Update signal card to display liquidity context** — 1. Update signal_card.html to show liquidity section
2. Fetch liquidity metrics from store:
   - recent_trade_count = store.get_recent_trade_count(market_id, 30)
   - bid_ask_spread_pct = store.calculate_bid_ask_spread(market_id)
   - slippage = estimate_slippage(...) from latest event metadata
3. Render:
   - 'Bid/ask spread: X.X%' (or 'N/A')
   - 'Recent trades (30m): N' (or '0')
   - 'Est. slippage ($100): $X.XX' (or 'Insufficient data')
4. Gray out or show warning icon if liquidity is poor (spread > 5% or trades < 5)
  - Estimate: 30m
  - Files: app/templates/signal_card.html, app/server.py
  - Verify: grep -q 'Bid/ask spread' app/templates/signal_card.html && grep -q 'Recent trades' app/templates/signal_card.html
- [ ] **T05: Test liquidity context display with varied scenarios** — 1. Generate test events with varying liquidity:
   - High liquidity: tight spread (1%), high trade count (50+)
   - Medium liquidity: moderate spread (3%), medium trades (10)
   - Low liquidity: wide spread (8%), few trades (2)
   - No data: missing bid/ask fields
2. For each scenario, verify signal card shows correct liquidity metrics
3. Verify slippage estimates reasonable (higher for thin markets)
4. Verify 'N/A' handling when data missing
5. Document threshold for 'actionable' vs 'thin market' liquidity
  - Estimate: 30m
  - Verify: test -f integration_test_results.md && grep -q 'liquidity test' integration_test_results.md
