---
estimated_steps: 9
estimated_files: 1
skills_used: []
---

# T04: Build paired markets dashboard view

1. Create app/templates/paired_markets.html view
2. Query paired markets from /api/paired-markets
3. Render as two-column layout:
   - Left: Kalshi market with latest yes_price, volume, last event timestamp
   - Right: Polymarket market with same fields
   - Center: spread indicator (price difference)
4. Click either market opens unified event timeline
5. Unified timeline shows events from both venues with venue labels
6. Add route /dashboard/paired-markets in server.py

## Inputs

- `app/store.py`

## Expected Output

- `app/templates/paired_markets.html`
- `app/server.py`

## Verification

curl -s http://127.0.0.1:8765/dashboard/paired-markets | grep -q 'paired markets'
