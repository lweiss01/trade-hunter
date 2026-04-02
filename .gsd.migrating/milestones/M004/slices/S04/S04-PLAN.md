# S04: Detector Tuning Dashboard

**Goal:** Allow user to adapt detector sensitivity to different market behaviors without editing code.
**Demo:** After this: Detector tuning dashboard shows current settings (baseline window, volume threshold, price threshold, cooldown) with sliders and input fields. Changes apply immediately and persist to config.

## Tasks
- [ ] **T01: Define detector_config schema with audit log** — 1. Add detector_config table to schema.sql:
   - id INTEGER PRIMARY KEY (single row)
   - spike_baseline_points INTEGER
   - spike_min_volume_delta REAL
   - spike_min_price_move REAL
   - spike_cooldown_seconds INTEGER
   - spike_score_threshold REAL
   - updated_at TIMESTAMP
2. Seed with current defaults from config.py
3. Add audit log table: detector_config_history (id, config_snapshot JSON, changed_by, changed_at)
  - Estimate: 25m
  - Files: app/schema.sql
  - Verify: python -c 'import app.db; conn = app.db.connect(":memory:"); cursor = conn.cursor(); cursor.execute("SELECT sql FROM sqlite_master WHERE name=\"detector_config\""); assert cursor.fetchone()'
- [ ] **T02: Add detector config persistence and caching** — 1. Add MarketStore methods:
   - get_detector_config() -> dict of settings
   - update_detector_config(settings: dict) -> save to DB, log to audit trail
   - reset_detector_config() -> restore defaults from config.py
2. Update SpikeDetector.__init__ to load config from store if available, else use defaults
3. Add config cache with 5-min TTL to avoid DB query per event
4. Write tests for config persistence and cache behavior
  - Estimate: 35m
  - Files: app/store.py, app/detector.py
  - Verify: python -m pytest tests/test_detector_config.py -k persistence -k cache
- [ ] **T03: Build detector tuning dashboard UI** — 1. Create app/templates/detector_tuning.html UI
2. Fetch current config from /api/detector/config
3. Render controls:
   - spike_baseline_points: slider (10-100) + input field
   - spike_min_volume_delta: slider (10-500) + input field
   - spike_min_price_move: slider (0.005-0.05, step 0.001) + input field (percentage)
   - spike_cooldown_seconds: slider (60-600) + input field
   - spike_score_threshold: slider (2.0-10.0, step 0.1) + input field
4. 'Save Changes' button POSTs to /api/detector/config
5. 'Reset to Defaults' button POSTs to /api/detector/config/reset
6. Show last updated timestamp
7. Show signal count last 1h/24h to gauge impact
  - Estimate: 60m
  - Verify: curl -s http://127.0.0.1:8765/dashboard/detector-tuning | grep -q 'detector tuning'
- [ ] **T04: Add detector tuning API endpoints** — 1. Add GET /api/detector/config endpoint -> returns current config
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
  - Estimate: 30m
  - Files: app/server.py
  - Verify: python -m pytest tests/test_detector_tuning_api.py && curl -s http://127.0.0.1:8765/api/detector/config | jq -e '.spike_baseline_points'
- [ ] **T05: Test detector tuning end-to-end with signal rate validation** — 1. Navigate to /dashboard/detector-tuning
2. Record baseline: note current signal count/hour
3. Adjust spike_min_volume_delta to 2x default
4. Save changes, generate test events
5. Verify fewer signals triggered (higher threshold)
6. Adjust spike_score_threshold lower
7. Verify more signals triggered
8. Test 'Reset to Defaults' - verify settings restored
9. Restart app, verify settings persist
10. Check audit log: verify config changes recorded
11. Document impact of each setting on signal rate
  - Estimate: 30m
  - Verify: test -f integration_test_results.md && grep -q 'detector tuning test' integration_test_results.md
