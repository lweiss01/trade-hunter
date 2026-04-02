---
estimated_steps: 7
estimated_files: 1
skills_used: []
---

# T05: Test end-to-end flow: PolyAlertHub webhook → MarketEvent → Dashboard

1. Start app locally
2. POST sample payload to /api/alerts/polyalerthub using curl
3. Verify event appears in /api/markets with source='polyalerthub'
4. Verify dashboard activity stream shows the event
5. Test with missing optional fields - verify graceful handling
6. Test token validation (if configured) - verify 401 on bad token
7. Document any edge cases

## Inputs

- `app/server.py`
- `tests/fixtures/sample_polyalerthub_payload.json`

## Expected Output

- `integration_test_results.md`

## Verification

curl -X POST http://127.0.0.1:8765/api/alerts/polyalerthub -H 'Content-Type: application/json' -d @tests/fixtures/sample_polyalerthub_payload.json && curl -s http://127.0.0.1:8765/api/events | jq -e '.[] | select(.source == "polyalerthub")'
