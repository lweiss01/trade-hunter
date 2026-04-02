---
estimated_steps: 6
estimated_files: 1
skills_used: []
---

# T02: Enhance KalshiPykalshiFeed adapter with defensive field extraction

1. Update app/feeds/kalshi_pykalshi.py to handle missing/optional fields with .get() instead of direct access
2. Add try/except around message processing to log unexpected schemas without crashing
3. Normalize price from cents to decimal (price_cents / 100.0)
4. Handle both ticker and trade message types with different field names
5. Extract volume as delta when available, mark as volume_kind='delta'
6. Add metadata field for message_type to aid debugging

## Inputs

- `app/feeds/kalshi_pykalshi.py`
- `test_kalshi_connection.py`

## Expected Output

- `app/feeds/kalshi_pykalshi.py`
- `tests/test_kalshi_feed.py`

## Verification

python -m pytest tests/test_kalshi_feed.py -k defensive

## Observability Impact

Adapter logs unexpected message schemas with full payload for debugging
