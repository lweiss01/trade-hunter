# S02: Confidence and Severity Tier Refinement

**Goal:** Refine tier assignment logic to match user intuition and prioritize signals during busy periods.
**Demo:** After this: Signals labeled as watch/notable/high conviction flow based on transparent composite scoring. High conviction requires score ≥ 6.0, price move ≥ 1.75x threshold, volume multiple ≥ 3.0.

## Tasks
- [ ] **T01: Implement refined tier assignment logic with composite criteria** — 1. Update detector.py::_tier() method with refined logic:
   - Cross-venue: if event.metadata.get('cross_venue') return 'cross-venue divergence'
   - High conviction: score >= 6.0 AND price_move >= 1.75 * threshold AND volume_multiple >= 3.0
   - Notable: score >= 4.0 OR (price_move >= 1.2 * threshold AND volume_multiple >= 2.4)
   - Watch: fallback for all other cases
2. Add _tier_explanation() method that returns human-readable reason
3. Update SpikeSignal to include tier_explanation field
4. Write unit tests for tier boundary cases
  - Estimate: 45m
  - Files: app/detector.py
  - Verify: python -m pytest tests/test_tier_refinement.py -v
- [ ] **T02: Add tier distribution logging and stats** — 1. Create tier_stats.py background task that runs every 24 hours
2. Query signals from last 24 hours grouped by tier
3. Calculate: count per tier, avg score per tier, avg volume_multiple per tier
4. Log stats with structured format: {tier: 'notable', count: 15, avg_score: 4.8, avg_volume_multiple: 2.7}
5. Expose in /api/health endpoint as tier_distribution object
6. Add pytest for stats calculation
  - Estimate: 30m
  - Verify: python -m pytest tests/test_tier_stats.py && curl -s http://127.0.0.1:8765/api/health | jq -e '.tier_distribution'
- [ ] **T03: Update signal card to display tier explanation and color coding** — 1. Update signal_card.html template to show tier_explanation below tier badge
2. Add tooltip on tier badge with full criteria explanation
3. Color coding:
   - watch: #808080 (gray)
   - notable: #FFA500 (orange/yellow)
   - high conviction flow: #FF0000 (red)
   - cross-venue divergence: #800080 (purple)
4. Test rendering with each tier
  - Estimate: 20m
  - Files: app/templates/signal_card.html, app/static/css/signal_card.css
  - Verify: grep -q 'tier_explanation' app/templates/signal_card.html && grep -c '#FF0000\|#FFA500\|#808080\|#800080' app/static/css/signal_card.css | test $(cat) -ge 4
- [ ] **T04: Validate tier assignments against 20+ edge cases** — 1. Generate 20+ test signals with varying score/volume/price combinations
2. For each tier boundary:
   - Just below threshold (should be lower tier)
   - Just above threshold (should be higher tier)
   - Well above threshold (should be higher tier)
3. Manually review tier assignments - verify conservative high conviction (no false positives)
4. Verify tier explanations are clear and accurate
5. Document any counterintuitive assignments
  - Estimate: 30m
  - Verify: python -m pytest tests/test_tier_refinement.py -k edge_cases -v
