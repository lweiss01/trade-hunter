---
estimated_steps: 7
estimated_files: 1
skills_used: []
---

# T02: Build market detail view with full event timeline

1. Create app/templates/market_detail.html
2. Accept market_id as URL param: /dashboard/market/<market_id>
3. Query all events for market ORDER BY timestamp ASC
4. Render timeline table: timestamp, event_kind, yes_price, volume, trade_size
5. Add simple price/volume chart (use Chart.js or similar)
6. Show market metadata: platform, title, topic, live status
7. Link back to spike board

## Inputs

- `app/models.py`

## Expected Output

- `app/templates/market_detail.html`
- `app/server.py`

## Verification

curl -s http://127.0.0.1:8765/dashboard/market/TEST_MKT | grep -q 'event timeline'
