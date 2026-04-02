---
estimated_steps: 5
estimated_files: 2
skills_used: []
---

# T01: Research and document Discord rich embed format

1. Research Discord embed format: https://discord.com/developers/docs/resources/channel#embed-object
2. Document structure: title, description, fields, color, footer, timestamp, url
3. Create example embed JSON for each tier (watch, notable, high conviction, divergence)
4. Test with webhook: curl -X POST with embed payload
5. Verify rendering in Discord client (desktop/mobile)

## Inputs

- None specified.

## Expected Output

- `docs/discord_embed_format.md`
- `tests/fixtures/discord_embed_examples.json`

## Verification

test -f docs/discord_embed_format.md && test -f tests/fixtures/discord_embed_examples.json
