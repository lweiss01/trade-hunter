# Project History

This archive is the durable memory of what agents changed, why they changed it, and what the project impact was. Review it before revisiting a feature area.

---

## Session: M007 Dashboard Parity — April 2026
- Agent: GSD (Claude Code)
- Status: in-progress (dashboard done, Markets + Settings remaining)
- When: 2026-04-05
- Goal: Bring the Trade Hunter UI to visible parity with `design-proposal.html`

### What was done

**Feed health / status**
- `app/feeds/kalshi_pykalshi.py`: added `_title_cache`; market titles now come from the Kalshi API instead of raw IDs
- `app/static/dashboard.js` `renderFeeds()`: Kalshi pill now uses `feeds["kalshi-pykalshi"].running` + staleness to show `OFFLINE` / `STALE` / `Xm ago` — mode no longer implies feed health
- `app/static/dashboard.js` `renderModeUI()`: removed topbar mode badge update (badge element removed from HTML)

**Application mode indicator**
- Removed `<div class="topbar-status"><span id="mode-badge">` from `app/static/index.html`
- Added `Application mode: Live/Simulation/Offline` chip at the end of the metrics strip in `renderMetrics()`
- New CSS classes: `.mode-live`, `.mode-sim`, `.mode-off`, `.metric-chip-label-mode`, `.metric-chip-val-mode`

**Topbar proportions**
- Reduced topbar height 56px → 52px
- Tightened nav tabs, pills, settings icon, ticker form vertical padding
- Brand name: tighter letter-spacing, slightly lighter weight
- Brand tagline: reduced size, no `text-transform: uppercase`

**Brand / logo**
- Replaced `app/static/trade-hunter-logo4.png` with cleaner version (less chrome/glare)
- Switched icon from `box-shadow` ring to `filter: drop-shadow` teal glow

**Metrics row**
- Reduced chip padding, gap, type scale
- Corrected metric-label color to `--text-muted`

**Panel headers**
- Reduced `panel-head` padding and gap
- Tightened `signals-controls` gap, `signals-label` size, `signal-sort`/`signal-toggle` height/padding

**Topic filter chips**
- Reduced chip height, gap, padding, font size
- Switched inactive border to `--border-mid`; count opacity reduced

**Panel body / empty states**
- Reduced padding on `.panel-body-signals` and `.panel-body-tuning`
- Added explicit `.empty` padding/font-size rule matching proposal

**Right column density**
- Market Tape: reduced `thead th` padding, `tbody td` padding, `mkt-title`/`mkt-id`/`mkt-cell` sizes
- Live Trade Flow: reduced `flow-list` padding, `flow-row` gap/padding/font-size, all flow span sizes

**Footer**
- Restructured to proposal layout: version + copy on left, plain Roadmap/Changelog links right, outlined User Guide pill right
- New elements: `.site-footer-left`, `.site-footer-links`, `.site-footer-copy`
- Footer links `font-size: 0.68rem` (smaller than before, matching version badge)

**Backend**
- `app/service.py`: `search_kalshi_by_category()` now fetches broader open-events set and filters locally; alias handling for sports/elections/macro/geopolitics/crypto
- `app/analyst.py`: `_persist_tuning_snapshot()` appends advisor snapshots to `docs/TUNING-BACKLOG.md` with sequential TB-XXX IDs

### Commits this session (most recent first)
```
c69b029  Footer: reduce Roadmap/Changelog link font size
4aa2a3d  Footer: align utility links with proposal layout
0099109  Right column: tighten flow and tape row density
8a309bf  Panels: tighten empty-state body spacing
df0fd4d  Signals: tighten topic filter chips toward proposal
db711cf  Panels: tighten header bar spacing toward proposal
4f0bff4  Brand: refresh header logo and icon treatment
98524d2  Metrics: tighten status chip spacing toward proposal
d17959f  Topbar: tighten header proportions toward proposal
7021090  Mode indicator: move application mode into metrics row
0e4dde9  Topbar: make Kalshi pill reflect feed health
56a7d9a  Metrics row: shorten window sublabels
bce7d7d  Live Trade Flow: align empty-state inset with Market Tape
e6ed48f  Dashboard: tighten empty-state copy
622882a  Dashboard: remove selected-signal workbench path
8721106  Tuning Advisor: compress dashboard panel to proposal style
a9b4776  Recent Signals: compress cards to proposal-style triage view
903fcd4  Tuning Advisor: use approved next-steps empty copy
3a0d48a  Markets panel: honest category-browser copy and aligned helper text
73e1f84  Category search: filter Kalshi results locally by query
8bb0283  Markets page: restore proposal layout and controls
```

### Why it mattered
The dashboard was visually diverging from the proposal in ways that made it feel unpolished and misleading (e.g. green LIVE badge when the feed was stopped, oversized panels, clickable flow rows). This pass closes most of the visible gap against `design-proposal.html`.

### Regression risks
See `regression-watch.md` for the full list of preserved fixes (RW001–RW010).

---

## What remains

### Markets page parity
- Tracked ticker table: verify column widths, status chip, remove button sizing, title wrapping
- Category browser: input/button proportion, result row spacing, shortcut chips
- Overall spacing, panel structure, and responsive behavior

### Settings page parity
- Panel grouping: settings currently renders flat; proposal groups into logical sections
- Control sizing: toggles, selects, inputs need to match proposal scale
- Section headers and descriptions need proposal typography treatment
- Save bar positioning and button styles

### Dashboard final composition pass
- Left/right column vertical balance when panels have content vs. are empty
- Minor remaining spacing gaps (e.g. panel-body gap when signals are present)
- CSS legacy/duplicate rules cleanup

### Tuning Backlog
- Real TB-IDs should appear in the dashboard advisor panel from fresh advisor runs
- Currently blocked until a new advisor snapshot is generated after enough signals accumulate
