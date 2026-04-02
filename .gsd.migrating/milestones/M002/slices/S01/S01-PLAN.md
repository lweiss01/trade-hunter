# S01: Signal Explanation Cards

**Goal:** Add per-signal breakdown UI that explains why an alert fired with concrete numbers and context.
**Demo:** After this: Signal detail card shows volume delta vs 1-hour and 24-hour baseline, price move over 1 min/5 min/30 min, whether signal was detector-driven or vendor-driven, and last 5 events leading into spike.

## Tasks
- [ ] **T01: Enhance SpikeSignal with enriched context fields** — 1. Enhance SpikeSignal dataclass in models.py with:
   - baseline_1h, baseline_24h (replace single baseline)
   - price_move_1m, price_move_5m, price_move_30m
   - leading_events: list[MarketEvent] (last 5 before spike)
2. Update detector.py to calculate multiple baselines and price move windows
3. Update detector to capture leading events from market window
4. Update SpikeSignal.to_dict() to include new fields
  - Estimate: 45m
  - Files: app/models.py, app/detector.py
  - Verify: python -m pytest tests/test_signal_enrichment.py -k baseline -k price_move
- [ ] **T02: Create signal card HTML template with enriched breakdown** — 1. Create app/templates/signal_card.html Jinja2 template
2. Card sections:
   - Header: market title, tier badge (color coded), timestamp
   - Volume section: delta, 1h baseline, 24h baseline, multiple (delta / baseline_1h)
   - Price section: 1m move, 5m move, 30m move, current yes_price
   - Source section: detector-driven or vendor-driven label, platform
   - Event timeline: table with last 5 events (timestamp, event_kind, yes_price, volume)
3. Add CSS for tier color coding (watch: gray, notable: yellow, high conviction: red)
4. Make card clickable to expand/collapse timeline
  - Estimate: 60m
  - Verify: grep -q 'baseline_1h' app/templates/signal_card.html && grep -q 'price_move_1m' app/templates/signal_card.html
- [ ] **T03: Add API endpoint and route for signal detail view** — 1. Add GET /api/signals/<signal_id> endpoint in server.py
2. Query signal from database with enriched fields
3. Return JSON with all context: baselines, price moves, leading events
4. Add /dashboard/signal/<signal_id> route that renders signal_card.html
5. Link signal cards from live spike board and alert history
  - Estimate: 30m
  - Files: app/server.py
  - Verify: curl -s http://127.0.0.1:8765/api/signals/1 | jq -e '.baseline_1h'
- [ ] **T04: Test signal card rendering with real and edge-case data** — 1. Start app, generate test spike signal
2. Click signal from live spike board - verify card opens
3. Verify all fields populated: volume multiple, baselines, price moves, event timeline
4. Verify tier color coding matches tier (watch=gray, notable=yellow, high conviction=red)
5. Verify source label shows 'detector' for internal signals, 'polyalerthub' for vendor
6. Test edge cases: missing price data, missing volume data
7. Document visual issues and layout problems
  - Estimate: 20m
  - Verify: curl -s http://127.0.0.1:8765/dashboard/signal/1 | grep -q 'volume multiple'
