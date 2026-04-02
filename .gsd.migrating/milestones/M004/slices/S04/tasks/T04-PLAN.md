---
estimated_steps: 12
estimated_files: 1
skills_used: []
---

# T04: Add detector tuning API endpoints

1. Add GET /api/detector/config endpoint -> returns current config
2. Add POST /api/detector/config endpoint:
   - Accept JSON body with settings
   - Validate ranges (prevent nonsensical values)
   - Call store.update_detector_config(settings)
   - Invalidate detector config cache
   - Return updated config
3. Add POST /api/detector/config/reset endpoint:
   - Call store.reset_detector_config()
   - Invalidate cache
   - Return defaults
4. Add pytest for API validation and error handling

## Inputs

- `app/server.py`
- `app/store.py`

## Expected Output

- `app/server.py`
- `tests/test_detector_tuning_api.py`

## Verification

python -m pytest tests/test_detector_tuning_api.py && curl -s http://127.0.0.1:8765/api/detector/config | jq -e '.spike_baseline_points'
