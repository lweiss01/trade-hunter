---
estimated_steps: 5
estimated_files: 1
skills_used: []
---

# T03: Add API endpoint and route for signal detail view

1. Add GET /api/signals/<signal_id> endpoint in server.py
2. Query signal from database with enriched fields
3. Return JSON with all context: baselines, price moves, leading events
4. Add /dashboard/signal/<signal_id> route that renders signal_card.html
5. Link signal cards from live spike board and alert history

## Inputs

- `app/server.py`
- `app/templates/signal_card.html`

## Expected Output

- `app/server.py`

## Verification

curl -s http://127.0.0.1:8765/api/signals/1 | jq -e '.baseline_1h'
