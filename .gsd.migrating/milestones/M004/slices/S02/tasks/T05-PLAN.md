---
estimated_steps: 11
estimated_files: 1
skills_used: []
---

# T05: Test Discord rich embeds end-to-end on real webhook

1. Set DISCORD_WEBHOOK_URL in .env to test webhook
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

## Inputs

- `app/notifiers.py`
- `tests/fixtures/`

## Expected Output

- `integration_test_results.md`

## Verification

test -f integration_test_results.md && grep -q 'Discord embed test' integration_test_results.md
