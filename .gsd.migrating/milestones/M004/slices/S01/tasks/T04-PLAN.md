---
estimated_steps: 8
estimated_files: 2
skills_used: []
---

# T04: Add checklist completion tracking and stats

1. Create app/checklist_stats.py background task
2. Query all signals with non-null checklist_completed
3. Calculate:
   - Overall completion rate (avg items checked per signal)
   - Per-item completion rate (which prompts most/least often checked)
   - Time to first check (signal detected_at to first checklist update)
4. Log daily stats
5. Expose in /api/health endpoint

## Inputs

- `app/models.py`

## Expected Output

- `app/checklist_stats.py`
- `tests/test_checklist_stats.py`

## Verification

python -m pytest tests/test_checklist_stats.py && curl -s http://127.0.0.1:8765/api/health | jq -e '.checklist_stats'

## Observability Impact

Checklist stats: overall_completion_rate, per_item_rates, avg_time_to_first_check
