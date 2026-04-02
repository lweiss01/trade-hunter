---
estimated_steps: 6
estimated_files: 1
skills_used: []
---

# T01: Build live spike board view with recent signals

1. Create app/templates/spike_board.html - main dashboard view
2. Query 20 most recent signals ORDER BY detected_at DESC
3. Render as grid/list with tier color badges, market title, timestamp, score
4. Click signal opens signal card (reuse from S01)
5. Auto-refresh every 30 seconds (or WebSocket live update)
6. Add route /dashboard/spike-board in server.py

## Inputs

- `app/templates/signal_card.html`

## Expected Output

- `app/templates/spike_board.html`
- `app/server.py`

## Verification

curl -s http://127.0.0.1:8765/dashboard/spike-board | grep -q 'most recent signals'
