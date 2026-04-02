# S03: SQLite Persistence Layer

**Goal:** Replace in-memory store with SQLite schema for events, signals, and feed health. Preserve detector behavior and market windows across restarts.
**Demo:** After this: App restart preserves event history and detector state. SQLite database contains events, signals, and feed health records with retention policy.

## Tasks
- [ ] **T01: Define SQLite schema for events, signals, feed_health, markets** — 1. Create app/schema.sql with tables:
   - events: id, source, platform, market_id, title, event_kind, yes_price, no_price, volume, volume_kind, trade_size, trade_side, liquidity, live, topic, market_url, timestamp, metadata_json
   - signals: id, market_id, score, volume_delta, price_move, baseline_volume_delta, reason, tier, topic, source_label, detected_at, event_id (FK to events)
   - feed_health: feed_name (PK), running, detail, last_event_at, error_count, reconnects, updated_at
   - markets: market_id (PK), platform, title, last_event_at, total_events
2. Create app/db.py with connect() function and schema initialization
3. Add pytest fixture for test database
  - Estimate: 45m
  - Verify: python -c 'import app.db; conn = app.db.connect(":memory:"); cursor = conn.cursor(); cursor.execute("SELECT name FROM sqlite_master WHERE type=\"table\""); tables = [r[0] for r in cursor.fetchall()]; assert set(tables) >= {"events", "signals", "feed_health", "markets"}'
- [ ] **T02: Refactor MarketStore to use SQLite backend** — 1. Refactor app/store.py MarketStore class to use SQLite backend
2. Replace deques/dicts with SQL queries
3. add_event(): INSERT INTO events, UPDATE markets, update detector window
4. get_recent_events(limit): SELECT FROM events ORDER BY timestamp DESC LIMIT
5. get_signals(limit): SELECT FROM signals ORDER BY detected_at DESC LIMIT
6. update_feed_status(): UPSERT INTO feed_health
7. Preserve existing method signatures - service.py should not need changes
8. Add connection pooling (sqlite3.connect with check_same_thread=False)
  - Estimate: 90m
  - Files: app/store.py
  - Verify: python -m pytest tests/test_store_sqlite.py -k add_event -k get_recent
- [ ] **T03: Verify detector baseline calculation behavior unchanged post-migration** — 1. Create test: generate same event sequence, run through in-memory detector and SQLite detector
2. Compare: volume_deltas deque contents, baseline calculations, signal triggers
3. Verify: detector._baseline() returns same values for both backends
4. Verify: detector._volume_delta() handles cumulative volume correctly
5. Document any differences - fail test if behavior diverges
6. Add regression test with known event sequence and expected baseline/signals
  - Estimate: 60m
  - Verify: python -m pytest tests/test_detector_migration.py -v
- [ ] **T04: Implement retention policy with configurable threshold** — 1. Add RETENTION_DAYS to config.py Settings (default 7)
2. Create app/retention.py with cleanup_old_events(db_path, retention_days) function
3. DELETE FROM events WHERE timestamp < now - retention_days
4. DELETE FROM signals WHERE detected_at < now - retention_days
5. Add background thread in service.py that runs cleanup every 24 hours
6. Log: rows deleted, last run timestamp
7. Expose last_cleanup_at in /api/health
  - Estimate: 30m
  - Files: app/config.py, app/service.py
  - Verify: python -m pytest tests/test_retention.py -k cleanup
- [ ] **T05: Test end-to-end: persistence, restart recovery, retention policy** — 1. Start app with SQLite backend, add test events from multiple feeds
2. Verify events persisted: query database directly with sqlite3 CLI
3. Restart app, verify events still present
4. Verify detector windows restored: generate spike, verify cooldown prevents duplicate
5. Verify feed health status persists
6. Test retention policy: set RETENTION_DAYS=0, run cleanup, verify old events deleted
7. Monitor performance: measure event ingestion rate (events/sec), query latency
8. Document results in integration_test_results.md
  - Estimate: 45m
  - Verify: bash -c 'python main.py & PID=$!; sleep 5; curl -X POST http://127.0.0.1:8765/api/events -H "Content-Type: application/json" -d @tests/fixtures/sample_event.json; kill $PID; python main.py & PID=$!; sleep 5; COUNT=$(curl -s http://127.0.0.1:8765/api/events | jq length); kill $PID; test $COUNT -gt 0'
