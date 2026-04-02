---
estimated_steps: 8
estimated_files: 1
skills_used: []
---

# T05: Test paired markets view with real and edge-case data

1. Seed market pairs into database: python app/seed_pairs.py
2. Generate test events for both sides of at least 2 pairs
3. Navigate to /dashboard/paired-markets
4. Verify pairs displayed side by side with latest data
5. Click market - verify unified timeline shows events from both venues with labels
6. Verify spread calculation shown (price difference)
7. Test with missing data - one side has events, other doesn't
8. Document layout and usability issues

## Inputs

- `app/templates/paired_markets.html`
- `seed_market_pairs.json`

## Expected Output

- `integration_test_results.md`

## Verification

curl -s http://127.0.0.1:8765/api/paired-markets | jq 'length >= 2'
