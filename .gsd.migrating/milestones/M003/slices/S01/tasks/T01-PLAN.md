---
estimated_steps: 11
estimated_files: 1
skills_used: []
---

# T01: Define market_pairs schema and create seed data

1. Add market_pairs table to schema.sql:
   - id INTEGER PRIMARY KEY
   - kalshi_market_id TEXT NOT NULL
   - polymarket_market_id TEXT NOT NULL
   - category TEXT (e.g. 'elections', 'crypto', 'macro')
   - notes TEXT (optional)
   - created_at TIMESTAMP
   - UNIQUE(kalshi_market_id, polymarket_market_id)
2. Run migration to update database schema
3. Create seed data file: seed_market_pairs.json with 10+ pairs
4. Add seed script: app/seed_pairs.py to INSERT seed data

## Inputs

- `app/schema.sql`

## Expected Output

- `app/schema.sql`
- `seed_market_pairs.json`
- `app/seed_pairs.py`

## Verification

python -c 'import app.db; conn = app.db.connect(":memory:"); cursor = conn.cursor(); cursor.execute("SELECT sql FROM sqlite_master WHERE name=\"market_pairs\""); assert cursor.fetchone()' && test -f seed_market_pairs.json
