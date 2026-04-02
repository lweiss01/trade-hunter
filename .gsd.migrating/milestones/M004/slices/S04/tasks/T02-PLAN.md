---
estimated_steps: 7
estimated_files: 2
skills_used: []
---

# T02: Add detector config persistence and caching

1. Add MarketStore methods:
   - get_detector_config() -> dict of settings
   - update_detector_config(settings: dict) -> save to DB, log to audit trail
   - reset_detector_config() -> restore defaults from config.py
2. Update SpikeDetector.__init__ to load config from store if available, else use defaults
3. Add config cache with 5-min TTL to avoid DB query per event
4. Write tests for config persistence and cache behavior

## Inputs

- `app/store.py`
- `app/detector.py`

## Expected Output

- `app/store.py`
- `app/detector.py`
- `tests/test_detector_config.py`

## Verification

python -m pytest tests/test_detector_config.py -k persistence -k cache
