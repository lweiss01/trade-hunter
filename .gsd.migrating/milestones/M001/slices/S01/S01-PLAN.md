# S01: Kalshi Live WebSocket Stream

**Goal:** Connect to Kalshi WebSocket API using pykalshi, subscribe to configured markets, normalize ticker and trade messages into MarketEvent, and report feed health.
**Demo:** After this: Dashboard shows live Kalshi markets with ticker and trade updates. Feed status shows connection state, last event timestamp, and error count.

## Tasks
- [ ] **T01: Install pykalshi and test basic WebSocket connection** — 1. Add pykalshi to dependencies in pyproject.toml under [project.optional-dependencies.integrations]
2. Install locally: `py -m pip install -e .[integrations]`
3. Create test script test_kalshi_connection.py that connects to Kalshi WebSocket and subscribes to one test market
4. Verify connection succeeds and messages arrive
5. Document message schema variations observed
  - Estimate: 30m
  - Files: pyproject.toml, test_kalshi_connection.py
  - Verify: py test_kalshi_connection.py && grep -q 'Connected' output.log
- [ ] **T02: Enhance KalshiPykalshiFeed adapter with defensive field extraction** — 1. Update app/feeds/kalshi_pykalshi.py to handle missing/optional fields with .get() instead of direct access
2. Add try/except around message processing to log unexpected schemas without crashing
3. Normalize price from cents to decimal (price_cents / 100.0)
4. Handle both ticker and trade message types with different field names
5. Extract volume as delta when available, mark as volume_kind='delta'
6. Add metadata field for message_type to aid debugging
  - Estimate: 45m
  - Files: app/feeds/kalshi_pykalshi.py
  - Verify: python -m pytest tests/test_kalshi_feed.py -k defensive
- [ ] **T03: Wire feed health status reporting into KalshiPykalshiFeed** — 1. Call publish_status() on feed start with running=True, detail=f'subscribed to {count} markets'
2. Call publish_status() on stop with running=False
3. Call publish_status() on error with running=False, detail=error message
4. Track last_event_at timestamp - update on each message received
5. Track error_count and reconnects counters
6. Update store.py to persist feed_health status (add update_feed_status method if missing)
  - Estimate: 30m
  - Files: app/feeds/kalshi_pykalshi.py, app/store.py
  - Verify: python -m pytest tests/test_feed_health.py
- [ ] **T04: Add KALSHI_MARKETS env var configuration and subscription logic** — 1. Add KALSHI_MARKETS to config.py Settings dataclass (comma-separated list)
2. Update .env.example with KALSHI_MARKETS=TICKER1,TICKER2
3. Update KalshiPykalshiFeed to read settings.kalshi_markets and subscribe to each ticker
4. Add validation: if kalshi_markets is empty, publish_status with running=False, detail='no KALSHI_MARKETS configured'
5. Test with real market tickers
  - Estimate: 20m
  - Files: app/config.py, .env.example, app/feeds/kalshi_pykalshi.py
  - Verify: grep -q 'KALSHI_MARKETS' .env.example && python -c 'from app.config import Settings; s = Settings(); assert hasattr(s, "kalshi_markets")'
- [ ] **T05: Test end-to-end flow: Kalshi → MarketEvent → Store → Dashboard** — 1. Set KALSHI_MARKETS to one active market ticker in .env
2. Start app with Kalshi feed enabled
3. Verify events appear in store (check /api/markets endpoint)
4. Verify feed status shows running=True in dashboard
5. Stop feed, verify status updates to running=False
6. Test reconnection: kill WebSocket, verify adapter reconnects and increments reconnects counter
7. Document any unexpected behaviors
  - Estimate: 30m
  - Verify: curl -s http://127.0.0.1:8765/api/markets | jq -e '.[] | select(.source == "pykalshi")'
