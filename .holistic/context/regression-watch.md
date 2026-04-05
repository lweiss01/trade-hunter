# Regression Watch

Use this before changing existing behavior. It is the short list of fixes and outcomes that future agents should preserve.

## RW001 — Topbar is full-width, ticker input must not overlap pills
- Fixed: topbar moved outside `.app-shell`, fixed at body level, `app-shell` padded down
- Risk: reverting the topbar position or removing the app-shell padding will reintroduce ticker-input / pill overlap
- Files: `app/static/index.html`, `app/static/dashboard.css`

## RW002 — Settings page is isolated from Dashboard/Markets
- Fixed: Settings is a separate page-view, not a panel layered on top of dashboard
- Risk: any change that puts settings content inside `#page-dashboard` or `#page-markets` violates this
- Files: `app/static/index.html`, `app/static/dashboard.js`

## RW003 — Signal cards keep a single left stripe (no double-border)
- Fixed: `.signal-card::before` provides the colored left stripe; the card border is neutral
- Risk: adding a colored `border-left` to `.signal-card` directly reintroduces the double-border look
- Files: `app/static/dashboard.css`

## RW004 — Live Trade Flow is view-only (no click/select behavior)
- Fixed: removed `tabindex`, `role="button"`, click/keydown handlers, and cursor/selected/focus CSS from `.flow-row`
- Risk: re-adding any of those will make the flow rows act as interactive controls again
- Files: `app/static/dashboard.js`, `app/static/dashboard.css`

## RW005 — Market Tape uses friendly titles from Kalshi API, not raw market IDs
- Fixed: `app/feeds/kalshi_pykalshi.py` caches titles from the Kalshi API; `MarketEvent.title` uses that cache
- Risk: removing `_title_cache` or reverting to `title=str(market_id)` restores the raw-ID display
- Files: `app/feeds/kalshi_pykalshi.py`

## RW006 — Category browser is labeled honestly (not "Category Search")
- Fixed: UI says "Category Browser", button says "Show series", results say "series found"
- Risk: reverting copy to "Search" / "Search results" is misleading — the backend does local filtering, not true search
- Files: `app/static/index.html`, `app/static/dashboard.js`

## RW007 — Dashboard Tuning Advisor has no Details or Apply buttons
- Fixed: details collapsible and apply button removed from dashboard panel; apply belongs in Settings
- Risk: re-adding those buttons to the dashboard panel violates the approved design
- Files: `app/static/dashboard.js`

## RW008 — Selected Signal Workbench is fully removed from the dashboard path
- Fixed: workbench section, JS state, and CSS removed; signal cards are plain triage items
- Risk: re-adding `selectedSignalWorkbenchEl` or workbench CSS reintroduces the oversized left-column behavior
- Files: `app/static/index.html`, `app/static/dashboard.js`, `app/static/dashboard.css`

## RW009 — Kalshi pill reflects actual feed health, not mode
- Fixed: pill reads `kalshi-pykalshi.running` + staleness from telemetry; shows OFFLINE/STALE/age
- Risk: reverting to `kalshi_last_event_at`-only logic means the pill will show "fresh" when the feed is stopped
- Files: `app/static/dashboard.js`

## RW010 — Application mode chip is in the metrics row, not the topbar
- Fixed: removed `#mode-badge` from topbar; mode now appears as a quiet chip at the end of the metrics strip
- Risk: re-adding a topbar mode pill will re-clutter the header with redundant/misleading info
- Files: `app/static/index.html`, `app/static/dashboard.js`, `app/static/dashboard.css`
