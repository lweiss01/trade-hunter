---
estimated_steps: 11
estimated_files: 1
skills_used: []
---

# T02: Implement rich embed format in DiscordNotifier

1. Update app/notifiers.py DiscordNotifier.send() method
2. Build embed object:
   - title: market title
   - description: tier + reason (one-liner)
   - color: tier-based (watch: 0x808080, notable: 0xFFA500, high conviction: 0xFF0000, divergence: 0x800080)
   - fields: [{name: 'Volume Delta', value: '+XXX vs baseline YYY'}, {name: 'Price Move', value: 'X.X%'}, {name: 'Score', value: 'X.XX'}]
   - url: link to dashboard signal detail page
   - footer: {text: 'Source: pykalshi | Platform: kalshi', icon_url: (optional)}
   - timestamp: detected_at as ISO 8601
3. Send as POST with {embeds: [embed]} instead of plain text
4. Handle errors: log failed delivery, retry once on 429 rate limit

## Inputs

- `app/notifiers.py`
- `app/models.py`

## Expected Output

- `app/notifiers.py`
- `tests/test_discord_notifier.py`

## Verification

python -m pytest tests/test_discord_notifier.py -k rich_embed
