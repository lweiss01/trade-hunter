# M004: 

## Vision
Make the app useful during real decision-making. By the end of this milestone, signals include actionable workflow prompts, Discord notifications are scannable and rich, watchlists reduce noise, and detector tuning is self-service.

## Slice Overview
| ID | Slice | Risk | Depends | Done | After this |
|----|-------|------|---------|------|------------|
| S01 | Research Checklist on Alerts | low | — | ⬜ | Signal cards show research checklist with prompts: What changed? Cross-platform? News? Liquidity sufficient? Nearing resolution? What invalidates the trade? |
| S02 | Discord Embed Improvements | low | — | ⬜ | Discord embeds use rich format with color coding (red: high conviction, yellow: notable, gray: watch), category labels, market URLs, and acknowledge/snooze action links. |
| S03 | Personal Watchlists and Filters | medium | S02 | ⬜ | Watchlist UI allows creating named watchlists (e.g. 'Macro', 'Crypto', 'Elections') with filters by platform, category, topic, min liquidity, min volume surge, keyword lists. |
| S04 | Detector Tuning Dashboard | low | S03 | ⬜ | Detector tuning dashboard shows current settings (baseline window, volume threshold, price threshold, cooldown) with sliders and input fields. Changes apply immediately and persist to config. |
