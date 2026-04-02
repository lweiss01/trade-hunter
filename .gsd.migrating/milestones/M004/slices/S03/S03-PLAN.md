# S03: Personal Watchlists and Filters

**Goal:** Support personal watchlists and filters to reduce alert noise and focus on relevant markets.
**Demo:** After this: Watchlist UI allows creating named watchlists (e.g. 'Macro', 'Crypto', 'Elections') with filters by platform, category, topic, min liquidity, min volume surge, keyword lists.

## Tasks
- [ ] **T01: Define watchlists schema and create default templates** — 1. Add watchlists table to schema.sql:
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
  - Estimate: 30m
  - Files: app/schema.sql
  - Verify: python -c 'import app.db; conn = app.db.connect(":memory:"); cursor = conn.cursor(); cursor.execute("SELECT sql FROM sqlite_master WHERE name=\"watchlists\""); assert cursor.fetchone()' && jq 'length >= 3' seed_watchlists.json
- [ ] **T02: Add watchlist CRUD and filter matching to store** — 1. Add MarketStore methods:
   - create_watchlist(name, filters) -> watchlist_id
   - update_watchlist(id, name, filters)
   - delete_watchlist(id)
   - get_watchlists() -> list of watchlists
   - set_active_watchlist(id) -> deactivate others, activate this one
   - get_active_watchlist() -> current active watchlist or None
2. Add watchlist filter matching:
   - matches_watchlist(signal, watchlist) -> bool
   - Check each filter: platform, topics, min_volume_surge, keywords (case-insensitive substring match in title/market_id)
3. Write unit tests for filter matching edge cases
  - Estimate: 45m
  - Files: app/store.py
  - Verify: python -m pytest tests/test_watchlist_filters.py -k matches -k create
- [ ] **T03: Build watchlist management UI** — 1. Create app/templates/watchlists.html management UI
2. List all watchlists with:
   - Name, active badge, filter summary, created_at
   - Edit/Delete buttons
3. 'Create Watchlist' button opens form:
   - Name input
   - Platform checkboxes (Kalshi, Polymarket, both)
   - Topic checkboxes (crypto, elections, macro, sports, geopolitics, general)
   - Min volume surge slider (1.0 - 5.0x)
   - Min liquidity input (optional)
   - Keywords textarea (comma-separated)
4. Edit form pre-populates with existing filters
5. 'Set Active' button to activate watchlist
6. Add route /dashboard/watchlists
  - Estimate: 60m
  - Files: app/server.py
  - Verify: curl -s http://127.0.0.1:8765/dashboard/watchlists | grep -q 'watchlists'
- [ ] **T04: Wire watchlist filters into detector signal emission** — 1. Update detector signal emission to check active watchlist
2. Before emitting signal:
   - active_watchlist = store.get_active_watchlist()
   - if active_watchlist and not matches_watchlist(signal, active_watchlist): suppress signal
3. Log suppressed signals: {signal_id, watchlist_id, reason: 'filtered'}
4. Expose suppression stats in /api/health: watchlist_stats: {signals_matched: N, signals_suppressed: M}
5. Add toggle: WATCHLIST_MODE in config (strict: suppress non-matching, permissive: show all, flag non-matching)
  - Estimate: 30m
  - Files: app/detector.py, app/config.py
  - Verify: python -m pytest tests/test_watchlist_integration.py -k filter -k suppress
- [ ] **T05: Test watchlist filtering end-to-end with multiple scenarios** — 1. Seed default watchlists: python app/seed_watchlists.py
2. Create 'Crypto' watchlist, set active
3. Generate test signals:
   - Crypto signal (BTC market, topic=crypto) -> should match
   - Macro signal (CPI market, topic=macro) -> should suppress
   - Election signal (president market, topic=elections) -> should suppress
4. Verify only crypto signal appears in dashboard
5. Switch to 'All Markets' (no active watchlist), verify all signals shown
6. Test keyword matching: create watchlist with keywords=['trump'], verify only matching signals appear
7. Test min_volume_surge filter
8. Document filter effectiveness and UX feedback
  - Estimate: 30m
  - Verify: test -f integration_test_results.md && grep -q 'watchlist filter test' integration_test_results.md
