---
estimated_steps: 14
estimated_files: 1
skills_used: []
---

# T03: Build watchlist management UI

1. Create app/templates/watchlists.html management UI
2. List all watchlists with:
   - Name, active badge, filter summary, created_at
   - Edit/Delete buttons
3. 'Create Watchlist' button opens form:
   - Name input
   - Platform checkboxes (Kalshi, Polymarket, both)
   - Topic checkboxes (crypto, elections, macro, sports, geopolitics, general)
   - Min volume surge slider (1.0 - 5.0x)
   - Min liquidity input (optional)
   - Keywords textarea (comma-separated)
4. Edit form pre-populates with existing filters
5. 'Set Active' button to activate watchlist
6. Add route /dashboard/watchlists

## Inputs

- None specified.

## Expected Output

- `app/templates/watchlists.html`
- `app/server.py`

## Verification

curl -s http://127.0.0.1:8765/dashboard/watchlists | grep -q 'watchlists'
