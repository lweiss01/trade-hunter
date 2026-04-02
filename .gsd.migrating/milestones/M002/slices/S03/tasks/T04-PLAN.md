---
estimated_steps: 9
estimated_files: 1
skills_used: []
---

# T04: Add navigation structure with tab bar/sidebar

1. Create app/templates/base.html with navigation structure
2. Add tab bar or sidebar with links:
   - Live Spike Board (default)
   - Alert History
   - Market Detail (hidden, accessed via click)
3. Highlight active tab
4. Update all view templates to extend base.html
5. Test navigation: click between views, verify URL updates, state preserved
6. Mobile-responsive (optional - can defer)

## Inputs

- `app/templates/spike_board.html`
- `app/templates/market_detail.html`
- `app/templates/alert_history.html`

## Expected Output

- `app/templates/base.html`

## Verification

grep -q 'nav' app/templates/base.html && grep -c 'href.*dashboard' app/templates/base.html | test $(cat) -ge 2
