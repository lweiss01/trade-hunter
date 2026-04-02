---
estimated_steps: 7
estimated_files: 2
skills_used: []
---

# T02: Add spread detector configuration settings

1. Add to config.py Settings:
   - spread_threshold_pct (default 0.03 = 3%)
   - spread_min_duration_seconds (default 60)
   - spread_cooldown_seconds (default 300)
2. Update .env.example with new settings
3. SpreadDetector reads settings on init
4. Cooldown prevents re-alerting same pair within cooldown window

## Inputs

- `app/config.py`

## Expected Output

- `app/config.py`
- `.env.example`

## Verification

grep -q 'spread_threshold_pct' app/config.py && grep -q 'SPREAD_THRESHOLD_PCT' .env.example
