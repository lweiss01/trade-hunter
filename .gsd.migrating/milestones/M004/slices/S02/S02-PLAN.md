# S02: Discord Embed Improvements

**Goal:** Improve Discord notification quality to make alerts more scannable and actionable without opening dashboard.
**Demo:** After this: Discord embeds use rich format with color coding (red: high conviction, yellow: notable, gray: watch), category labels, market URLs, and acknowledge/snooze action links.

## Tasks
- [ ] **T01: Research and document Discord rich embed format** — 1. Research Discord embed format: https://discord.com/developers/docs/resources/channel#embed-object
2. Document structure: title, description, fields, color, footer, timestamp, url
3. Create example embed JSON for each tier (watch, notable, high conviction, divergence)
4. Test with webhook: curl -X POST with embed payload
5. Verify rendering in Discord client (desktop/mobile)
  - Estimate: 30m
  - Verify: test -f docs/discord_embed_format.md && test -f tests/fixtures/discord_embed_examples.json
- [ ] **T02: Implement rich embed format in DiscordNotifier** — 1. Update app/notifiers.py DiscordNotifier.send() method
2. Build embed object:
   - title: market title
   - description: tier + reason (one-liner)
   - color: tier-based (watch: 0x808080, notable: 0xFFA500, high conviction: 0xFF0000, divergence: 0x800080)
   - fields: [{name: 'Volume Delta', value: '+XXX vs baseline YYY'}, {name: 'Price Move', value: 'X.X%'}, {name: 'Score', value: 'X.XX'}]
   - url: link to dashboard signal detail page
   - footer: {text: 'Source: pykalshi | Platform: kalshi', icon_url: (optional)}
   - timestamp: detected_at as ISO 8601
3. Send as POST with {embeds: [embed]} instead of plain text
4. Handle errors: log failed delivery, retry once on 429 rate limit
  - Estimate: 45m
  - Files: app/notifiers.py
  - Verify: python -m pytest tests/test_discord_notifier.py -k rich_embed
- [ ] **T03: Add action button support (placeholder for future bot integration)** — 1. Add DISCORD_INCLUDE_ACTIONS to config (bool, default False)
2. If enabled, add 'components' to Discord message with action buttons
3. Buttons:
   - 'Acknowledge' (green button) - marks signal as reviewed
   - 'Snooze 1h' (gray button) - suppresses similar alerts for market
4. Note: Discord interactive components require bot integration (not simple webhook)
5. Document limitation: webhooks don't support buttons, need bot for actions
6. Implement as future enhancement placeholder, disabled by default
  - Estimate: 20m
  - Files: app/config.py
  - Verify: grep -q 'DISCORD_INCLUDE_ACTIONS' app/config.py && test -f docs/discord_actions.md
- [ ] **T04: Add Discord delivery logging and error handling** — 1. Update app/notifiers.py to track delivery stats
2. Count: sent, failed, rate_limited (429 responses)
3. Log errors with details: status code, response body, signal_id
4. Add retry logic: if 429, wait retry-after seconds and retry once
5. Expose stats in /api/health endpoint: discord_notifier: {sent: N, failed: M, rate_limited: K}
6. Add pytest for error scenarios
  - Estimate: 25m
  - Files: app/notifiers.py
  - Verify: python -m pytest tests/test_discord_errors.py && curl -s http://127.0.0.1:8765/api/health | jq -e '.discord_notifier'
- [ ] **T05: Test Discord rich embeds end-to-end on real webhook** — 1. Set DISCORD_WEBHOOK_URL in .env to test webhook
2. Generate test signals for each tier (watch, notable, high conviction, divergence)
3. Verify embeds sent to Discord with correct:
   - Color coding
   - Field values (volume, price, score)
   - Market URL link
   - Footer with source/platform
   - Timestamp
4. Test mobile rendering (Discord mobile app)
5. Test error scenarios: invalid webhook URL, rate limit (send 10+ rapid signals)
6. Document visual quality and scannability feedback
  - Estimate: 30m
  - Verify: test -f integration_test_results.md && grep -q 'Discord embed test' integration_test_results.md
