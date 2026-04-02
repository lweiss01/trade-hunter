---
estimated_steps: 7
estimated_files: 2
skills_used: []
---

# T04: Implement retention policy with configurable threshold

1. Add RETENTION_DAYS to config.py Settings (default 7)
2. Create app/retention.py with cleanup_old_events(db_path, retention_days) function
3. DELETE FROM events WHERE timestamp < now - retention_days
4. DELETE FROM signals WHERE detected_at < now - retention_days
5. Add background thread in service.py that runs cleanup every 24 hours
6. Log: rows deleted, last run timestamp
7. Expose last_cleanup_at in /api/health

## Inputs

- `app/config.py`
- `app/service.py`

## Expected Output

- `app/retention.py`
- `app/config.py`
- `app/service.py`
- `tests/test_retention.py`

## Verification

python -m pytest tests/test_retention.py -k cleanup

## Observability Impact

Retention policy logs: rows_deleted, retention_days, last_run_at
