---
estimated_steps: 5
estimated_files: 1
skills_used: []
---

# T03: Add market pairing queries to store API

1. Add MarketStore method: get_paired_markets() returns list of (kalshi_market, polymarket_market) tuples
2. For each pair, fetch latest events from both markets
3. Add MarketStore method: get_pair_by_market_id(market_id) returns paired market if exists
4. Add route /api/paired-markets returning JSON list of pairs with latest events
5. Write unit tests for pairing queries

## Inputs

- `app/store.py`
- `app/schema.sql`

## Expected Output

- `app/store.py`
- `tests/test_market_pairs.py`

## Verification

python -m pytest tests/test_market_pairs.py -k get_paired
