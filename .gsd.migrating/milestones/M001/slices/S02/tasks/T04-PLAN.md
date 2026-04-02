---
estimated_steps: 4
estimated_files: 2
skills_used: []
---

# T04: Wire PolyAlertHub relay into feed health tracking

1. Update store.py to track 'polyalerthub' feed health status
2. In endpoint handler: call store.update_feed_status('polyalerthub', {running: True, last_event_at: now, detail: 'relay endpoint active'})
3. On error, update feed status with error detail
4. Dashboard should show 'polyalerthub' in feed status panel

## Inputs

- `app/store.py`
- `app/server.py`

## Expected Output

- `app/store.py`
- `app/server.py`

## Verification

curl -X POST http://127.0.0.1:8765/api/alerts/polyalerthub -H 'Content-Type: application/json' -d @tests/fixtures/sample_polyalerthub_payload.json && curl -s http://127.0.0.1:8765/api/health | jq -e '.feeds.polyalerthub.running == true'
