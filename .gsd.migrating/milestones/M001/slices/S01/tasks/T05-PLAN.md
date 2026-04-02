---
estimated_steps: 7
estimated_files: 1
skills_used: []
---

# T05: Test end-to-end flow: Kalshi → MarketEvent → Store → Dashboard

1. Set KALSHI_MARKETS to one active market ticker in .env
2. Start app with Kalshi feed enabled
3. Verify events appear in store (check /api/markets endpoint)
4. Verify feed status shows running=True in dashboard
5. Stop feed, verify status updates to running=False
6. Test reconnection: kill WebSocket, verify adapter reconnects and increments reconnects counter
7. Document any unexpected behaviors

## Inputs

- `app/feeds/kalshi_pykalshi.py`
- `app/store.py`
- `app/server.py`

## Expected Output

- `integration_test_results.md`

## Verification

curl -s http://127.0.0.1:8765/api/markets | jq -e '.[] | select(.source == "pykalshi")'
