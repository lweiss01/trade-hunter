# S02: Spread and Divergence Monitoring

**Goal:** Track price divergence between equivalent contracts and alert when spread is actionable.
**Demo:** After this: Spread monitoring calculates yes-price gap between paired markets. Alerts trigger when spread exceeds threshold and persists for configured duration.

## Tasks
- [ ] **T01: Implement SpreadDetector with spread calculation and persistence tracking** — 1. Create app/spread_detector.py with SpreadDetector class
2. Initialize with market_pairs from store and config settings
3. Track spread windows: {pair_id: deque[(timestamp, spread)]}
4. On each event, find paired market and calculate spread
5. spread_cents = abs(yes_price_kalshi - yes_price_polymarket) * 100
6. spread_pct = spread_cents / avg(yes_price_kalshi, yes_price_polymarket)
7. Add to spread window deque
8. Check persistence: if all spreads in last N seconds > threshold, emit divergence signal
  - Estimate: 60m
  - Verify: python -m pytest tests/test_spread_detector.py -k spread_calc -k persistence
- [ ] **T02: Add spread detector configuration settings** — 1. Add to config.py Settings:
   - spread_threshold_pct (default 0.03 = 3%)
   - spread_min_duration_seconds (default 60)
   - spread_cooldown_seconds (default 300)
2. Update .env.example with new settings
3. SpreadDetector reads settings on init
4. Cooldown prevents re-alerting same pair within cooldown window
  - Estimate: 15m
  - Files: app/config.py, .env.example
  - Verify: grep -q 'spread_threshold_pct' app/config.py && grep -q 'SPREAD_THRESHOLD_PCT' .env.example
- [ ] **T03: Define DivergenceSignal model with spread context** — 1. Create DivergenceSignal dataclass extending SpikeSignal
2. Additional fields:
   - kalshi_event: MarketEvent
   - polymarket_event: MarketEvent
   - spread_cents: float
   - spread_pct: float
   - duration_seconds: float
3. Automatically set tier='cross-venue divergence'
4. Update to_dict() for serialization
  - Estimate: 20m
  - Files: app/models.py
  - Verify: python -c 'from app.models import DivergenceSignal; s = DivergenceSignal.__annotations__; assert "spread_pct" in s'
- [ ] **T04: Wire SpreadDetector into event processing pipeline** — 1. Wire SpreadDetector into service.py
2. On each MarketEvent, pass to both SpikeDetector and SpreadDetector
3. SpreadDetector emits DivergenceSignal when criteria met
4. Store DivergenceSignal in signals table (add divergence-specific columns if needed)
5. Expose divergence signals via /api/signals?type=divergence
6. Add divergence section to spike board view
  - Estimate: 30m
  - Files: app/service.py, app/server.py
  - Verify: curl -s http://127.0.0.1:8765/api/signals?type=divergence | jq -e '.[] | .tier == "cross-venue divergence"'
- [ ] **T05: Test spread detection end-to-end with diverging price scenarios** — 1. Seed market pairs, generate events with diverging prices
2. Example: Kalshi yes_price=0.55, Polymarket yes_price=0.60 (5% spread)
3. Generate events over 90 seconds with persistent spread > threshold
4. Verify divergence signal emitted after min_duration
5. Verify signal includes both events, spread_cents, spread_pct, duration
6. Test cooldown: generate another divergence within cooldown window, verify no duplicate signal
7. Test convergence: spread drops below threshold, verify no signal
8. Document results
  - Estimate: 30m
  - Verify: python -m pytest tests/test_spread_detector.py -k end_to_end -v
