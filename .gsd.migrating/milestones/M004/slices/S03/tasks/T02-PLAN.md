---
estimated_steps: 11
estimated_files: 1
skills_used: []
---

# T02: Add watchlist CRUD and filter matching to store

1. Add MarketStore methods:
   - create_watchlist(name, filters) -> watchlist_id
   - update_watchlist(id, name, filters)
   - delete_watchlist(id)
   - get_watchlists() -> list of watchlists
   - set_active_watchlist(id) -> deactivate others, activate this one
   - get_active_watchlist() -> current active watchlist or None
2. Add watchlist filter matching:
   - matches_watchlist(signal, watchlist) -> bool
   - Check each filter: platform, topics, min_volume_surge, keywords (case-insensitive substring match in title/market_id)
3. Write unit tests for filter matching edge cases

## Inputs

- `app/store.py`

## Expected Output

- `app/store.py`
- `tests/test_watchlist_filters.py`

## Verification

python -m pytest tests/test_watchlist_filters.py -k matches -k create
