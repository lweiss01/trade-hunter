---
estimated_steps: 7
estimated_files: 1
skills_used: []
---

# T04: Test signal card rendering with real and edge-case data

1. Start app, generate test spike signal
2. Click signal from live spike board - verify card opens
3. Verify all fields populated: volume multiple, baselines, price moves, event timeline
4. Verify tier color coding matches tier (watch=gray, notable=yellow, high conviction=red)
5. Verify source label shows 'detector' for internal signals, 'polyalerthub' for vendor
6. Test edge cases: missing price data, missing volume data
7. Document visual issues and layout problems

## Inputs

- `app/templates/signal_card.html`
- `app/server.py`

## Expected Output

- `integration_test_results.md`

## Verification

curl -s http://127.0.0.1:8765/dashboard/signal/1 | grep -q 'volume multiple'
