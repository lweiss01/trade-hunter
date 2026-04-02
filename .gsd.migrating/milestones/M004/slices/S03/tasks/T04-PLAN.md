---
estimated_steps: 7
estimated_files: 2
skills_used: []
---

# T04: Wire watchlist filters into detector signal emission

1. Update detector signal emission to check active watchlist
2. Before emitting signal:
   - active_watchlist = store.get_active_watchlist()
   - if active_watchlist and not matches_watchlist(signal, active_watchlist): suppress signal
3. Log suppressed signals: {signal_id, watchlist_id, reason: 'filtered'}
4. Expose suppression stats in /api/health: watchlist_stats: {signals_matched: N, signals_suppressed: M}
5. Add toggle: WATCHLIST_MODE in config (strict: suppress non-matching, permissive: show all, flag non-matching)

## Inputs

- `app/detector.py`
- `app/store.py`

## Expected Output

- `app/detector.py`
- `app/config.py`

## Verification

python -m pytest tests/test_watchlist_integration.py -k filter -k suppress

## Observability Impact

Watchlist filter stats: signals_matched, signals_suppressed
