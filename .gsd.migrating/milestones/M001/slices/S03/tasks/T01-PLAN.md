---
estimated_steps: 7
estimated_files: 3
skills_used: []
---

# T01: Define SQLite schema for events, signals, feed_health, markets

1. Create app/schema.sql with tables:
   - events: id, source, platform, market_id, title, event_kind, yes_price, no_price, volume, volume_kind, trade_size, trade_side, liquidity, live, topic, market_url, timestamp, metadata_json
   - signals: id, market_id, score, volume_delta, price_move, baseline_volume_delta, reason, tier, topic, source_label, detected_at, event_id (FK to events)
   - feed_health: feed_name (PK), running, detail, last_event_at, error_count, reconnects, updated_at
   - markets: market_id (PK), platform, title, last_event_at, total_events
2. Create app/db.py with connect() function and schema initialization
3. Add pytest fixture for test database

## Inputs

- None specified.

## Expected Output

- `app/schema.sql`
- `app/db.py`
- `tests/conftest.py`

## Verification

python -c 'import app.db; conn = app.db.connect(":memory:"); cursor = conn.cursor(); cursor.execute("SELECT name FROM sqlite_master WHERE type=\"table\""); tables = [r[0] for r in cursor.fetchall()]; assert set(tables) >= {"events", "signals", "feed_health", "markets"}'
