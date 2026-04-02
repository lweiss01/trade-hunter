---
estimated_steps: 8
estimated_files: 2
skills_used: []
---

# T03: Update signal card to display tier explanation and color coding

1. Update signal_card.html template to show tier_explanation below tier badge
2. Add tooltip on tier badge with full criteria explanation
3. Color coding:
   - watch: #808080 (gray)
   - notable: #FFA500 (orange/yellow)
   - high conviction flow: #FF0000 (red)
   - cross-venue divergence: #800080 (purple)
4. Test rendering with each tier

## Inputs

- `app/templates/signal_card.html`
- `app/models.py`

## Expected Output

- `app/templates/signal_card.html`
- `app/static/css/signal_card.css`

## Verification

grep -q 'tier_explanation' app/templates/signal_card.html && grep -c '#FF0000\|#FFA500\|#808080\|#800080' app/static/css/signal_card.css | test $(cat) -ge 4
