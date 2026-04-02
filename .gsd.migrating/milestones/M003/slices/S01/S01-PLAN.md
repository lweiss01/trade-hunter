# S01: Cross-Platform Market Matching

**Goal:** Create manual mapping table for equivalent contracts across Kalshi and Polymarket, and display paired markets in unified view.
**Demo:** After this: Market mapping table defines equivalent Kalshi and Polymarket contracts. Dashboard shows paired markets side by side with shared event page.

## Tasks
- [ ] **T01: Define market_pairs schema and create seed data** — 1. Add market_pairs table to schema.sql:
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
  - Estimate: 30m
  - Files: app/schema.sql
  - Verify: python -c 'import app.db; conn = app.db.connect(":memory:"); cursor = conn.cursor(); cursor.execute("SELECT sql FROM sqlite_master WHERE name=\"market_pairs\""); assert cursor.fetchone()' && test -f seed_market_pairs.json
- [ ] **T02: Curate 10+ equivalent market pairs manually** — 1. Research 10+ equivalent contracts on Kalshi and Polymarket
2. Focus on high-volume categories: elections (president, senate), crypto (BTC price levels), macro (CPI, Fed rates)
3. Document in seed_market_pairs.json:
   - kalshi_market_id: exact market ticker/ID from Kalshi
   - polymarket_market_id: exact market slug from Polymarket
   - category: elections/crypto/macro
   - notes: any important differences (resolution criteria, close date)
4. Verify market IDs are correct by checking actual market pages
  - Estimate: 45m
  - Files: seed_market_pairs.json
  - Verify: jq 'length >= 10' seed_market_pairs.json
- [ ] **T03: Add market pairing queries to store API** — 1. Add MarketStore method: get_paired_markets() returns list of (kalshi_market, polymarket_market) tuples
2. For each pair, fetch latest events from both markets
3. Add MarketStore method: get_pair_by_market_id(market_id) returns paired market if exists
4. Add route /api/paired-markets returning JSON list of pairs with latest events
5. Write unit tests for pairing queries
  - Estimate: 30m
  - Files: app/store.py
  - Verify: python -m pytest tests/test_market_pairs.py -k get_paired
- [ ] **T04: Build paired markets dashboard view** — 1. Create app/templates/paired_markets.html view
2. Query paired markets from /api/paired-markets
3. Render as two-column layout:
   - Left: Kalshi market with latest yes_price, volume, last event timestamp
   - Right: Polymarket market with same fields
   - Center: spread indicator (price difference)
4. Click either market opens unified event timeline
5. Unified timeline shows events from both venues with venue labels
6. Add route /dashboard/paired-markets in server.py
  - Estimate: 60m
  - Files: app/server.py
  - Verify: curl -s http://127.0.0.1:8765/dashboard/paired-markets | grep -q 'paired markets'
- [ ] **T05: Test paired markets view with real and edge-case data** — 1. Seed market pairs into database: python app/seed_pairs.py
2. Generate test events for both sides of at least 2 pairs
3. Navigate to /dashboard/paired-markets
4. Verify pairs displayed side by side with latest data
5. Click market - verify unified timeline shows events from both venues with labels
6. Verify spread calculation shown (price difference)
7. Test with missing data - one side has events, other doesn't
8. Document layout and usability issues
  - Estimate: 20m
  - Verify: curl -s http://127.0.0.1:8765/api/paired-markets | jq 'length >= 2'
