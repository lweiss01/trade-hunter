---
estimated_steps: 11
estimated_files: 1
skills_used: []
---

# T02: Add POST /api/alerts/polyalerthub endpoint with payload transformation

1. Add POST /api/alerts/polyalerthub route to app/server.py
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

## Inputs

- `app/server.py`
- `app/models.py`
- `tests/fixtures/sample_polyalerthub_payload.json`

## Expected Output

- `app/server.py`
- `tests/test_polyalerthub_endpoint.py`

## Verification

python -m pytest tests/test_polyalerthub_endpoint.py -k transform
