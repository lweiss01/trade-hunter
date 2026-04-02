---
estimated_steps: 8
estimated_files: 1
skills_used: []
---

# T02: Refactor MarketStore to use SQLite backend

1. Refactor app/store.py MarketStore class to use SQLite backend
2. Replace deques/dicts with SQL queries
3. add_event(): INSERT INTO events, UPDATE markets, update detector window
4. get_recent_events(limit): SELECT FROM events ORDER BY timestamp DESC LIMIT
5. get_signals(limit): SELECT FROM signals ORDER BY detected_at DESC LIMIT
6. update_feed_status(): UPSERT INTO feed_health
7. Preserve existing method signatures - service.py should not need changes
8. Add connection pooling (sqlite3.connect with check_same_thread=False)

## Inputs

- `app/store.py`
- `app/db.py`
- `app/schema.sql`

## Expected Output

- `app/store.py`
- `tests/test_store_sqlite.py`

## Verification

python -m pytest tests/test_store_sqlite.py -k add_event -k get_recent

## Observability Impact

Query durations logged for slow queries (>100ms)
