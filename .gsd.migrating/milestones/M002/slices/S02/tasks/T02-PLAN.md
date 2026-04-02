---
estimated_steps: 6
estimated_files: 2
skills_used: []
---

# T02: Add tier distribution logging and stats

1. Create tier_stats.py background task that runs every 24 hours
2. Query signals from last 24 hours grouped by tier
3. Calculate: count per tier, avg score per tier, avg volume_multiple per tier
4. Log stats with structured format: {tier: 'notable', count: 15, avg_score: 4.8, avg_volume_multiple: 2.7}
5. Expose in /api/health endpoint as tier_distribution object
6. Add pytest for stats calculation

## Inputs

- `app/detector.py`

## Expected Output

- `app/tier_stats.py`
- `tests/test_tier_stats.py`

## Verification

python -m pytest tests/test_tier_stats.py && curl -s http://127.0.0.1:8765/api/health | jq -e '.tier_distribution'

## Observability Impact

Tier distribution stats logged daily and exposed in /api/health
