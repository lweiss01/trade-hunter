# trade-hunter

## What this project is
Trade Hunter is a real-time prediction-market monitoring dashboard for a small retail trader. It ingests live Kalshi activity and external alerts, detects unusual market behavior, explains why a signal fired, and helps separate genuine repricing from noise without placing trades.

## Current state
M001 is complete: live Kalshi ingestion, PolyAlertHub relay support, SQLite persistence, and feed-health reporting are in place. Since then, the app has shipped transparent severity tiers (`watch` / `notable` / `high conviction flow`), real-time detector enrichment, inline AI signal analysis, structured tuning suggestions, a tuning advisor, the apply-tuning endpoint with `.env` threshold persistence, and the core false-positive hardening rules.

**M007 Dashboard UI Redesign is the active milestone.** The dashboard parity pass against `design-proposal.html` is substantially complete. The following changes have landed:

### Completed this session (dashboard parity)
- Truthful Kalshi pill: shows `KALSHI 0M AGO` / `KALSHI STALE` / `KALSHI OFFLINE` based on actual feed health, not just mode
- Application mode moved out of topbar pill into a quieter metrics-row chip (`Application mode: Live`)
- Topbar proportions tightened to proposal: height 56→52px, nav tabs, pills, ticker input all slimmed
- Brand block refreshed: new cleaner logo (less chrome), softer icon drop-shadow treatment, tighter letter-spacing
- Metrics row chips tightened: padding, gap, type scale all reduced
- Panel headers slimmed: padding, badge, sort/toggle controls all tighter
- Topic filter chips tightened: height, gap, border color, active state aligned to proposal
- Panel body/empty-state spacing reduced: signals/tuning panels sit tighter
- Right-column density improved: Live Trade Flow and Market Tape rows use smaller padding/type
- Footer restructured: version + copy on left, quieter plain text links right, `User Guide` stays as primary outlined action

### Still needed to reach full parity
- **Markets page**: tracked-ticker table, category browser, status chips, and spacing need a full parity pass against the proposal
- **Settings page**: panel grouping, control sizing, section headers, and spacing need a proposal-aligned pass
- **Dashboard composition final pass**: overall left/right column spacing balance, a few remaining minor gaps
- **CSS cleanup**: `dashboard.css` still carries some legacy/duplicate rule blocks that survived earlier rewrites

## Goals
A reliable decision-support tool that surfaces unusual prediction-market flow quickly, explains the evidence clearly, preserves history across restarts, and keeps false positives low. Informational only — no trades placed. Live and simulation modes mutually exclusive. Tuning changes explainable and safely applied. Operational behavior observable enough to debug feed, persistence, and detector regressions quickly.
