---
estimated_steps: 11
estimated_files: 1
skills_used: []
---

# T05: Test watchlist filtering end-to-end with multiple scenarios

1. Seed default watchlists: python app/seed_watchlists.py
2. Create 'Crypto' watchlist, set active
3. Generate test signals:
   - Crypto signal (BTC market, topic=crypto) -> should match
   - Macro signal (CPI market, topic=macro) -> should suppress
   - Election signal (president market, topic=elections) -> should suppress
4. Verify only crypto signal appears in dashboard
5. Switch to 'All Markets' (no active watchlist), verify all signals shown
6. Test keyword matching: create watchlist with keywords=['trump'], verify only matching signals appear
7. Test min_volume_surge filter
8. Document filter effectiveness and UX feedback

## Inputs

- `app/templates/watchlists.html`
- `seed_watchlists.json`

## Expected Output

- `integration_test_results.md`

## Verification

test -f integration_test_results.md && grep -q 'watchlist filter test' integration_test_results.md
