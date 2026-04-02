---
estimated_steps: 9
estimated_files: 2
skills_used: []
---

# T02: Create signal card HTML template with enriched breakdown

1. Create app/templates/signal_card.html Jinja2 template
2. Card sections:
   - Header: market title, tier badge (color coded), timestamp
   - Volume section: delta, 1h baseline, 24h baseline, multiple (delta / baseline_1h)
   - Price section: 1m move, 5m move, 30m move, current yes_price
   - Source section: detector-driven or vendor-driven label, platform
   - Event timeline: table with last 5 events (timestamp, event_kind, yes_price, volume)
3. Add CSS for tier color coding (watch: gray, notable: yellow, high conviction: red)
4. Make card clickable to expand/collapse timeline

## Inputs

- `app/models.py`

## Expected Output

- `app/templates/signal_card.html`
- `app/static/css/signal_card.css`

## Verification

grep -q 'baseline_1h' app/templates/signal_card.html && grep -q 'price_move_1m' app/templates/signal_card.html
