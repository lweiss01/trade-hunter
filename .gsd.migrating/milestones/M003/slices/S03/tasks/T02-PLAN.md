---
estimated_steps: 7
estimated_files: 1
skills_used: []
---

# T02: Add liquidity metric queries to store

1. Add MarketStore method: get_recent_trade_count(market_id, minutes=30)
2. Query events WHERE market_id = ? AND event_kind = 'trade' AND timestamp > now - minutes
3. Return count of trades
4. Add method: calculate_bid_ask_spread(market_id)
5. Get latest event with bid/ask metadata
6. spread_pct = (ask_price - bid_price) / avg(bid_price, ask_price)
7. Return spread_pct or None if no data

## Inputs

- `app/store.py`

## Expected Output

- `app/store.py`
- `tests/test_liquidity_metrics.py`

## Verification

python -m pytest tests/test_liquidity_metrics.py -k recent_trade_count -k bid_ask_spread
