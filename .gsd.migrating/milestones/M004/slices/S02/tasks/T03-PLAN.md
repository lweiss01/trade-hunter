---
estimated_steps: 8
estimated_files: 1
skills_used: []
---

# T03: Add action button support (placeholder for future bot integration)

1. Add DISCORD_INCLUDE_ACTIONS to config (bool, default False)
2. If enabled, add 'components' to Discord message with action buttons
3. Buttons:
   - 'Acknowledge' (green button) - marks signal as reviewed
   - 'Snooze 1h' (gray button) - suppresses similar alerts for market
4. Note: Discord interactive components require bot integration (not simple webhook)
5. Document limitation: webhooks don't support buttons, need bot for actions
6. Implement as future enhancement placeholder, disabled by default

## Inputs

- `app/config.py`

## Expected Output

- `app/config.py`
- `docs/discord_actions.md`

## Verification

grep -q 'DISCORD_INCLUDE_ACTIONS' app/config.py && test -f docs/discord_actions.md
