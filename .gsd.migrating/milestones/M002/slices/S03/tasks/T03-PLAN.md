---
estimated_steps: 10
estimated_files: 1
skills_used: []
---

# T03: Build alert history view with filters and pagination

1. Create app/templates/alert_history.html
2. Query signals with filters:
   - tier (dropdown: all, watch, notable, high conviction, divergence)
   - topic (dropdown: all, crypto, elections, macro, sports, geopolitics, general)
   - platform (dropdown: all, kalshi, polymarket)
   - date range (start_date, end_date inputs)
3. Paginate results (20 per page)
4. Render as table: timestamp, market, tier badge, score, volume_delta, price_move
5. Click row opens signal card
6. Add route /dashboard/history in server.py

## Inputs

- `app/models.py`

## Expected Output

- `app/templates/alert_history.html`
- `app/server.py`

## Verification

curl -s 'http://127.0.0.1:8765/dashboard/history?tier=notable' | grep -q 'alert history'
