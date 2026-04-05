# Current Plan

## Goal

Complete M007 visible parity against `design-proposal.html` — dashboard is substantially done; remaining work is the **Markets page** and **Settings page** parity passes, followed by a final dashboard composition cleanup.

## Latest Status

Dashboard parity is in good shape. All major structural and spacing work is committed and pushed. The topbar, brand block, metrics row, panel headers, topic chips, signal/tuning panel bodies, right-column table density, and footer now match the proposal closely.

## What's Done This Session
- Feed health: Kalshi pill truthful (OFFLINE/STALE/Xm ago)
- Application mode: moved from topbar pill to quiet metrics-row chip
- Topbar: proportions tightened (height, nav tabs, pills, ticker form)
- Brand: new cleaner logo, softer icon treatment, tighter typography
- Metrics row: chips tightened
- Panel headers: padding and controls slimmed
- Topic filter chips: aligned to proposal
- Panel bodies / empty states: tighter spacing
- Right column: denser flow rows and tape table
- Footer: restructured to proposal left/right layout, smaller plain links

## Planned Next Steps

### 1. Markets page parity pass (next)
Compare `design-proposal.html` Markets section against the live Markets page at `http://127.0.0.1:8765/` (click Markets tab). Work through:
- Tracked ticker table: column widths, status chip size, `×` remove button size, title wrapping behavior
- Category browser: input/button proportions, shortcut chips, result row spacing
- Overall panel structure and section spacing
Accept bar: screenshot the running Markets page and compare directly to the proposal HTML.

### 2. Settings page parity pass
Compare `design-proposal.html` Settings section against the live Settings page (gear icon). Work through:
- Panel grouping (proposal groups settings into logical card sections)
- Control sizing: toggles, selects, text inputs
- Section headers/descriptions typography
- Save bar and button styles

### 3. Dashboard final composition pass
- Left/right column vertical balance with content vs. empty
- Remaining minor spacing gaps
- CSS legacy/duplicate rule cleanup in `dashboard.css`

## Key Constraints to Preserve
- No ticker-input overlap in topbar (RW001)
- Settings isolated from Dashboard/Markets (RW002)
- Signal cards: single left stripe only (RW003)
- Live Trade Flow: view-only, no click behavior (RW004)
- Market titles from Kalshi API cache (RW005)
- Category browser labeled honestly (RW006)
- Dashboard Tuning Advisor: no Details or Apply buttons (RW007)
- Selected Signal Workbench: fully removed (RW008)
- Kalshi pill: actual feed health, not mode (RW009)
- Application mode chip in metrics row, not topbar (RW010)

## Dev Server
- Running on `:8765`
- To restart: `python -m app` (or via `trade-hunter.cmd`)
- Background process ID varies per session — check with `bg_shell list`

## Key Files
- `app/static/index.html` — page structure, footer, nav
- `app/static/dashboard.css` — all styles
- `app/static/dashboard.js` — all render logic
- `design-proposal.html` — the acceptance bar for all visual work
- `app/feeds/kalshi_pykalshi.py` — feed health, title cache
- `app/service.py` — category search backend
- `app/analyst.py` — tuning advisor, TB persistence
- `docs/TUNING-BACKLOG.md` — persisted advisor snapshots

## Project Impact
Every commit this session brings the UI closer to the exact proposal layout. The user's acceptance standard is explicit: "if it doesn't look JUST LIKE the design-proposal, IT'S NOT RIGHT." The dashboard is now very close. Markets and Settings need the same treatment.
