# S02: PolyAlertHub Relay Endpoint

**Goal:** Accept PolyAlertHub alerts via relay endpoint, normalize schema into MarketEvent, validate signature/token if configured, and surface in unified dashboard.
**Demo:** After this: POST /api/alerts/polyalerthub accepts PolyAlertHub payloads, transforms them into MarketEvent, and persists to store. Dashboard shows polyalerthub events in activity stream.

## Tasks
- [ ] **T01: Document PolyAlertHub webhook payload schema** — 1. Research PolyAlertHub webhook payload schema (check docs or existing examples)
2. Document expected fields: market_id, title, platform, alert_type, price, volume, timestamp, etc.
3. Create sample_polyalerthub_payload.json with realistic test data
4. Define transformation rules: which fields map to MarketEvent attributes
  - Estimate: 20m
  - Verify: test -f docs/polyalerthub_payload_schema.md && test -f tests/fixtures/sample_polyalerthub_payload.json
- [ ] **T02: Add POST /api/alerts/polyalerthub endpoint with payload transformation** — 1. Add POST /api/alerts/polyalerthub route to app/server.py
2. Extract payload from request.json
3. Transform payload into MarketEvent:
   - source='polyalerthub'
   - platform from payload (default 'polymarket' if missing)
   - market_id, title from payload
   - yes_price, volume from payload (handle missing gracefully)
   - volume_kind='delta' (PolyAlertHub likely sends incremental)
4. Call store.add_event(event)
5. Return 200 OK with {"status": "received"}
6. Handle errors: 400 if payload missing required fields, 500 on store error
  - Estimate: 30m
  - Files: app/server.py
  - Verify: python -m pytest tests/test_polyalerthub_endpoint.py -k transform
- [ ] **T03: Add optional token validation for PolyAlertHub endpoint** — 1. Add POLYALERTHUB_TOKEN to config.py Settings (optional, default None)
2. Update .env.example with POLYALERTHUB_TOKEN=
3. In endpoint handler: if token configured, check request.headers.get('Authorization') == f'Bearer {token}'
4. Return 401 Unauthorized if token mismatch
5. Skip validation if token not configured
6. Log validation attempts (success/failure)
  - Estimate: 20m
  - Files: app/config.py, .env.example, app/server.py
  - Verify: python -m pytest tests/test_polyalerthub_auth.py
- [ ] **T04: Wire PolyAlertHub relay into feed health tracking** — 1. Update store.py to track 'polyalerthub' feed health status
2. In endpoint handler: call store.update_feed_status('polyalerthub', {running: True, last_event_at: now, detail: 'relay endpoint active'})
3. On error, update feed status with error detail
4. Dashboard should show 'polyalerthub' in feed status panel
  - Estimate: 15m
  - Files: app/store.py, app/server.py
  - Verify: curl -X POST http://127.0.0.1:8765/api/alerts/polyalerthub -H 'Content-Type: application/json' -d @tests/fixtures/sample_polyalerthub_payload.json && curl -s http://127.0.0.1:8765/api/health | jq -e '.feeds.polyalerthub.running == true'
- [ ] **T05: Test end-to-end flow: PolyAlertHub webhook → MarketEvent → Dashboard** — 1. Start app locally
2. POST sample payload to /api/alerts/polyalerthub using curl
3. Verify event appears in /api/markets with source='polyalerthub'
4. Verify dashboard activity stream shows the event
5. Test with missing optional fields - verify graceful handling
6. Test token validation (if configured) - verify 401 on bad token
7. Document any edge cases
  - Estimate: 20m
  - Verify: curl -X POST http://127.0.0.1:8765/api/alerts/polyalerthub -H 'Content-Type: application/json' -d @tests/fixtures/sample_polyalerthub_payload.json && curl -s http://127.0.0.1:8765/api/events | jq -e '.[] | select(.source == "polyalerthub")'
