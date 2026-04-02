---
estimated_steps: 8
estimated_files: 1
skills_used: []
---

# T05: Test spread detection end-to-end with diverging price scenarios

1. Seed market pairs, generate events with diverging prices
2. Example: Kalshi yes_price=0.55, Polymarket yes_price=0.60 (5% spread)
3. Generate events over 90 seconds with persistent spread > threshold
4. Verify divergence signal emitted after min_duration
5. Verify signal includes both events, spread_cents, spread_pct, duration
6. Test cooldown: generate another divergence within cooldown window, verify no duplicate signal
7. Test convergence: spread drops below threshold, verify no signal
8. Document results

## Inputs

- `app/spread_detector.py`
- `tests/fixtures/`

## Expected Output

- `integration_test_results.md`

## Verification

python -m pytest tests/test_spread_detector.py -k end_to_end -v
