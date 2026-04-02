# S03: Dashboard Information Architecture

**Goal:** Improve dashboard navigation and reduce cognitive load during active market periods.
**Demo:** After this: Dashboard has dedicated views: live spike board (most recent signals), market detail (full event timeline for a market), alert history (all signals with filters).

## Tasks
- [ ] **T01: Build live spike board view with recent signals** — 1. Create app/templates/spike_board.html - main dashboard view
2. Query 20 most recent signals ORDER BY detected_at DESC
3. Render as grid/list with tier color badges, market title, timestamp, score
4. Click signal opens signal card (reuse from S01)
5. Auto-refresh every 30 seconds (or WebSocket live update)
6. Add route /dashboard/spike-board in server.py
  - Estimate: 45m
  - Files: app/server.py
  - Verify: curl -s http://127.0.0.1:8765/dashboard/spike-board | grep -q 'most recent signals'
- [ ] **T02: Build market detail view with full event timeline** — 1. Create app/templates/market_detail.html
2. Accept market_id as URL param: /dashboard/market/<market_id>
3. Query all events for market ORDER BY timestamp ASC
4. Render timeline table: timestamp, event_kind, yes_price, volume, trade_size
5. Add simple price/volume chart (use Chart.js or similar)
6. Show market metadata: platform, title, topic, live status
7. Link back to spike board
  - Estimate: 60m
  - Files: app/server.py
  - Verify: curl -s http://127.0.0.1:8765/dashboard/market/TEST_MKT | grep -q 'event timeline'
- [ ] **T03: Build alert history view with filters and pagination** — 1. Create app/templates/alert_history.html
2. Query signals with filters:
   - tier (dropdown: all, watch, notable, high conviction, divergence)
   - topic (dropdown: all, crypto, elections, macro, sports, geopolitics, general)
   - platform (dropdown: all, kalshi, polymarket)
   - date range (start_date, end_date inputs)
3. Paginate results (20 per page)
4. Render as table: timestamp, market, tier badge, score, volume_delta, price_move
5. Click row opens signal card
6. Add route /dashboard/history in server.py
  - Estimate: 60m
  - Files: app/server.py
  - Verify: curl -s 'http://127.0.0.1:8765/dashboard/history?tier=notable' | grep -q 'alert history'
- [ ] **T04: Add navigation structure with tab bar/sidebar** — 1. Create app/templates/base.html with navigation structure
2. Add tab bar or sidebar with links:
   - Live Spike Board (default)
   - Alert History
   - Market Detail (hidden, accessed via click)
3. Highlight active tab
4. Update all view templates to extend base.html
5. Test navigation: click between views, verify URL updates, state preserved
6. Mobile-responsive (optional - can defer)
  - Estimate: 30m
  - Verify: grep -q 'nav' app/templates/base.html && grep -c 'href.*dashboard' app/templates/base.html | test $(cat) -ge 2
- [ ] **T05: Test dashboard navigation and user workflow** — 1. Start app, navigate to each view
2. Live spike board: verify 20 recent signals, tier colors correct, auto-refresh works
3. Click signal - verify card opens with full context
4. Click market title - verify market detail view shows full timeline
5. Alert history: test each filter (tier, topic, platform), verify results match
6. Test pagination: navigate pages, verify results correct
7. Test navigation: switch between views, verify no lost context
8. Time user workflow: find specific signal in history (<10 seconds target)
9. Document any UX issues
  - Estimate: 30m
  - Verify: test -f integration_test_results.md && grep -q 'navigation test' integration_test_results.md
