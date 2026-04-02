---
estimated_steps: 11
estimated_files: 1
skills_used: []
---

# T02: Build research checklist UI component

1. Create checklist component in signal_card.html
2. Render 6 checkboxes with prompts:
   - What changed? (e.g. news, catalyst, whale activity)
   - Cross-platform check? (divergence, confirmation)
   - News search? (Twitter, headlines, market-specific)
   - Liquidity sufficient? (spread, depth, slippage)
   - Nearing resolution? (close date, catalyst timing)
   - What invalidates? (price level, time decay, news)
3. Each checkbox sends AJAX POST to /api/signals/<id>/checklist with updated state
4. Checkboxes persist across page reloads
5. Show completion percentage (e.g. '4/6 complete')

## Inputs

- `app/templates/signal_card.html`

## Expected Output

- `app/templates/signal_card.html`
- `app/static/js/checklist.js`

## Verification

grep -c 'checkbox' app/templates/signal_card.html | test $(cat) -ge 6
