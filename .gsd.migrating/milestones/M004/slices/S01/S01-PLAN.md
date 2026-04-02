# S01: Research Checklist on Alerts

**Goal:** Add actionable workflow prompts to signal cards to reduce impulsive decisions and improve research consistency.
**Demo:** After this: Signal cards show research checklist with prompts: What changed? Cross-platform? News? Liquidity sufficient? Nearing resolution? What invalidates the trade?

## Tasks
- [ ] **T01: Add checklist_completed JSON field to signals schema** — 1. Add checklist_completed JSON column to signals table
2. Structure: {"what_changed": true, "cross_platform": false, "news": null, "liquidity": true, "resolution_timing": false, "what_invalidates": null}
3. Default to all null (not started)
4. Update schema migration
5. Add to SpikeSignal model as optional field
  - Estimate: 20m
  - Files: app/schema.sql, app/models.py
  - Verify: python -c 'import app.db; conn = app.db.connect(":memory:"); cursor = conn.cursor(); cursor.execute("SELECT sql FROM sqlite_master WHERE name=\"signals\""); sql = cursor.fetchone()[0]; assert "checklist_completed" in sql'
- [ ] **T02: Build research checklist UI component** — 1. Create checklist component in signal_card.html
2. Render 6 checkboxes with prompts:
   - What changed? (e.g. news, catalyst, whale activity)
   - Cross-platform check? (divergence, confirmation)
   - News search? (Twitter, headlines, market-specific)
   - Liquidity sufficient? (spread, depth, slippage)
   - Nearing resolution? (close date, catalyst timing)
   - What invalidates? (price level, time decay, news)
3. Each checkbox sends AJAX POST to /api/signals/<id>/checklist with updated state
4. Checkboxes persist across page reloads
5. Show completion percentage (e.g. '4/6 complete')
  - Estimate: 45m
  - Files: app/templates/signal_card.html
  - Verify: grep -c 'checkbox' app/templates/signal_card.html | test $(cat) -ge 6
- [ ] **T03: Add checklist update API endpoint** — 1. Add POST /api/signals/<signal_id>/checklist endpoint
2. Accept JSON body: {"item": "what_changed", "checked": true}
3. Update signals.checklist_completed JSON field
4. Return updated checklist state
5. Add GET /api/signals/<signal_id>/checklist to retrieve current state
6. Handle missing signal_id gracefully (404)
  - Estimate: 25m
  - Files: app/server.py
  - Verify: python -m pytest tests/test_checklist_api.py -k update -k get
- [ ] **T04: Add checklist completion tracking and stats** — 1. Create app/checklist_stats.py background task
2. Query all signals with non-null checklist_completed
3. Calculate:
   - Overall completion rate (avg items checked per signal)
   - Per-item completion rate (which prompts most/least often checked)
   - Time to first check (signal detected_at to first checklist update)
4. Log daily stats
5. Expose in /api/health endpoint
  - Estimate: 25m
  - Verify: python -m pytest tests/test_checklist_stats.py && curl -s http://127.0.0.1:8765/api/health | jq -e '.checklist_stats'
- [ ] **T05: Test checklist persistence and UI workflow** — 1. Generate test signal, open signal card
2. Check off checklist items in UI
3. Verify AJAX calls succeed and state persists
4. Reload page, verify checkboxes still checked
5. Navigate to alert history, verify completed items shown
6. Test all 6 prompts, verify completion percentage updates
7. Test edge case: signal with no checklist data (show all unchecked)
8. Document UX feedback
  - Estimate: 20m
  - Verify: test -f integration_test_results.md && grep -q 'checklist test' integration_test_results.md
