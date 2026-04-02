---
estimated_steps: 8
estimated_files: 1
skills_used: []
---

# T05: Test end-to-end: persistence, restart recovery, retention policy

1. Start app with SQLite backend, add test events from multiple feeds
2. Verify events persisted: query database directly with sqlite3 CLI
3. Restart app, verify events still present
4. Verify detector windows restored: generate spike, verify cooldown prevents duplicate
5. Verify feed health status persists
6. Test retention policy: set RETENTION_DAYS=0, run cleanup, verify old events deleted
7. Monitor performance: measure event ingestion rate (events/sec), query latency
8. Document results in integration_test_results.md

## Inputs

- `app/store.py`
- `app/service.py`
- `app/retention.py`

## Expected Output

- `integration_test_results.md`

## Verification

bash -c 'python main.py & PID=$!; sleep 5; curl -X POST http://127.0.0.1:8765/api/events -H "Content-Type: application/json" -d @tests/fixtures/sample_event.json; kill $PID; python main.py & PID=$!; sleep 5; COUNT=$(curl -s http://127.0.0.1:8765/api/events | jq length); kill $PID; test $COUNT -gt 0'
