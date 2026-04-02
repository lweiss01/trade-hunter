---
estimated_steps: 6
estimated_files: 1
skills_used: []
---

# T04: Add Discord delivery logging and error handling

1. Update app/notifiers.py to track delivery stats
2. Count: sent, failed, rate_limited (429 responses)
3. Log errors with details: status code, response body, signal_id
4. Add retry logic: if 429, wait retry-after seconds and retry once
5. Expose stats in /api/health endpoint: discord_notifier: {sent: N, failed: M, rate_limited: K}
6. Add pytest for error scenarios

## Inputs

- `app/notifiers.py`

## Expected Output

- `app/notifiers.py`
- `tests/test_discord_errors.py`

## Verification

python -m pytest tests/test_discord_errors.py && curl -s http://127.0.0.1:8765/api/health | jq -e '.discord_notifier'

## Observability Impact

Discord delivery stats: sent, failed, rate_limited
