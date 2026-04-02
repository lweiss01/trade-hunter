---
estimated_steps: 8
estimated_files: 1
skills_used: []
---

# T02: Curate 10+ equivalent market pairs manually

1. Research 10+ equivalent contracts on Kalshi and Polymarket
2. Focus on high-volume categories: elections (president, senate), crypto (BTC price levels), macro (CPI, Fed rates)
3. Document in seed_market_pairs.json:
   - kalshi_market_id: exact market ticker/ID from Kalshi
   - polymarket_market_id: exact market slug from Polymarket
   - category: elections/crypto/macro
   - notes: any important differences (resolution criteria, close date)
4. Verify market IDs are correct by checking actual market pages

## Inputs

- None specified.

## Expected Output

- `seed_market_pairs.json`

## Verification

jq 'length >= 10' seed_market_pairs.json
