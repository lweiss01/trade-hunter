---
estimated_steps: 12
estimated_files: 1
skills_used: []
---

# T01: Define watchlists schema and create default templates

1. Add watchlists table to schema.sql:
   - id INTEGER PRIMARY KEY
   - name TEXT NOT NULL UNIQUE
   - filters JSON (structure: {platform: 'kalshi', topics: ['crypto'], min_volume_surge: 2.0, keywords: ['btc', 'eth']})
   - active BOOLEAN (default false, only one active at a time)
   - created_at TIMESTAMP
2. Add watchlist_signals junction table:
   - watchlist_id, signal_id, matched_at
3. Create seed_watchlists.json with default templates:
   - Macro: topics=['macro'], keywords=['fed', 'cpi', 'inflation', 'rates']
   - Crypto: topics=['crypto'], keywords=['btc', 'eth', 'bitcoin', 'ethereum']
   - Elections: topics=['elections'], keywords=['president', 'senate', 'vote']

## Inputs

- `app/schema.sql`

## Expected Output

- `app/schema.sql`
- `seed_watchlists.json`

## Verification

python -c 'import app.db; conn = app.db.connect(":memory:"); cursor = conn.cursor(); cursor.execute("SELECT sql FROM sqlite_master WHERE name=\"watchlists\""); assert cursor.fetchone()' && jq 'length >= 3' seed_watchlists.json
