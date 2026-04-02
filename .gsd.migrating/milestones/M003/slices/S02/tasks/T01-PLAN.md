---
estimated_steps: 8
estimated_files: 2
skills_used: []
---

# T01: Implement SpreadDetector with spread calculation and persistence tracking

1. Create app/spread_detector.py with SpreadDetector class
2. Initialize with market_pairs from store and config settings
3. Track spread windows: {pair_id: deque[(timestamp, spread)]}
4. On each event, find paired market and calculate spread
5. spread_cents = abs(yes_price_kalshi - yes_price_polymarket) * 100
6. spread_pct = spread_cents / avg(yes_price_kalshi, yes_price_polymarket)
7. Add to spread window deque
8. Check persistence: if all spreads in last N seconds > threshold, emit divergence signal

## Inputs

- `app/models.py`
- `app/store.py`

## Expected Output

- `app/spread_detector.py`
- `tests/test_spread_detector.py`

## Verification

python -m pytest tests/test_spread_detector.py -k spread_calc -k persistence
