---
estimated_steps: 6
estimated_files: 2
skills_used: []
---

# T03: Wire feed health status reporting into KalshiPykalshiFeed

1. Call publish_status() on feed start with running=True, detail=f'subscribed to {count} markets'
2. Call publish_status() on stop with running=False
3. Call publish_status() on error with running=False, detail=error message
4. Track last_event_at timestamp - update on each message received
5. Track error_count and reconnects counters
6. Update store.py to persist feed_health status (add update_feed_status method if missing)

## Inputs

- `app/feeds/kalshi_pykalshi.py`
- `app/store.py`

## Expected Output

- `app/feeds/kalshi_pykalshi.py`
- `app/store.py`
- `tests/test_feed_health.py`

## Verification

python -m pytest tests/test_feed_health.py

## Observability Impact

Feed health status includes: running, detail, last_event_at, error_count, reconnects. Visible in dashboard /api/health endpoint
