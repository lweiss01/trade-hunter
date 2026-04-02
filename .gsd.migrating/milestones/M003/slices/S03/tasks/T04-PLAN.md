---
estimated_steps: 10
estimated_files: 2
skills_used: []
---

# T04: Update signal card to display liquidity context

1. Update signal_card.html to show liquidity section
2. Fetch liquidity metrics from store:
   - recent_trade_count = store.get_recent_trade_count(market_id, 30)
   - bid_ask_spread_pct = store.calculate_bid_ask_spread(market_id)
   - slippage = estimate_slippage(...) from latest event metadata
3. Render:
   - 'Bid/ask spread: X.X%' (or 'N/A')
   - 'Recent trades (30m): N' (or '0')
   - 'Est. slippage ($100): $X.XX' (or 'Insufficient data')
4. Gray out or show warning icon if liquidity is poor (spread > 5% or trades < 5)

## Inputs

- `app/templates/signal_card.html`
- `app/liquidity.py`

## Expected Output

- `app/templates/signal_card.html`
- `app/server.py`

## Verification

grep -q 'Bid/ask spread' app/templates/signal_card.html && grep -q 'Recent trades' app/templates/signal_card.html
