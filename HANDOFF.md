# Trade Hunter - Handoff Summary

**Date:** 2026-04-03  
**Current local branch:** `master`  
**Current focus:** live detector hardening + AI-assisted false-positive reduction  
**Next milestone:** `M005` — Detector Tuning Hardening and Guided Adjustment Application

---

## Current as-built state

Trade Hunter is no longer just a basic live feed + detector app. It now has:

- live Kalshi feed via `pykalshi`
- automatic ticker resolution for:
  - series slugs (`KXBTC15M`)
  - event tickers (`KXTOPCHEF-26DEC31`)
  - exact market tickers
- fan-out subscription for event tickers (all open sub-markets)
- SQLite persistence with thread-local connections
- 10-minute freshness filtering in live mode
- compact dashboard redesign with:
  - stronger live-mode pills
  - compact single-line flow rows
  - per-market sparklines
  - category search
- per-signal AI analyst
  - Anthropic Claude Haiku primary
  - Perplexity Sonar fallback
- tuning advisor (second-pass AI recommendations across recent labelled signals)
- durable tuning recommendation backlog in `docs/TUNING-BACKLOG.md`

---

## Verified current runtime behavior

Latest known clean server was restarted after killing stray app processes and resolving SQLite lock contention.

Key runtime behavior verified this session:
- `/api/state` returns:
  - `signals`
  - `tuning_advisor`
  - `telemetry`
  - current feed status
- per-signal analyst readouts are surfacing in the UI
- tuning advisor is generating recommendations from analysed signals
- Kalshi feed is resolving configured slugs into many live subscriptions
- false-positive tracking is now a first-class feature, not just chat history

---

## What was completed this session

### Live feed + detector/runtime hardening
- Fixed Kalshi message schema extraction:
  - `TickerMessage`
  - `TradeMessage`
- Added transport observability:
  - websocket frames
  - handled message counts
  - ticker/trade/lifecycle counters
- Added resolution logic for:
  - direct market ticker
  - series ticker
  - event ticker
- Added fan-out subscription behavior for event tickers
- Added expired/unresolved ticker reporting
- Hardened SQLite startup/connection behavior with:
  - busy timeout
  - WAL mode
  - `synchronous=NORMAL`
- Identified repeated crash source as stray `python -m app` processes causing DB locks

### Dashboard/UI improvements
- `MODE: LIVE` pill has stronger visual treatment
- simulation pill hidden entirely in live mode
- discord pill wording now reflects webhook state rather than vague running/idle state
- metric cards collapsed into compact metric strip
- flow rows compressed into one-line compact format
- added per-market sparkline history in the flow
- added latest-per-market clarification for signal toggle
- added category search panel

### AI signal interpretation
- Added `app/analyst.py`
- Added per-signal analyst:
  - `noise_or_signal`
  - `direction`
  - `confidence`
  - `rationale`
  - `threshold_note`
- Added provider fallback:
  - Anthropic primary
  - Perplexity fallback
- Verified live analyst output in the running app

### AI tuning recommendations
- Added tuning advisor second pass
- Tuning advisor analyzes recent analyst-labelled signals and returns:
  - summary
  - global recommendation
  - recommendation bullets
- Added durable backlog file:
  - `docs/TUNING-BACKLOG.md`
- Captured implemented vs planned tuning work there

### Planning / docs / roadmap
- Created new milestone plan: `M005`
- Updated `README.md`
- Updated `USER_GUIDE.md`
- Replaced stale `HANDOFF.md` with current summary

---

## What is intentionally NOT implemented yet

### Approved but deferred by user
The user explicitly approved the first detector tuning tweak, then explicitly chose to defer implementation to next session.

**Do not assume it is already live. It is NOT implemented yet.**

Deferred item:
- `TB-001` — add a **0.5% minimum absolute price-move gate** before a spike can be promoted to `notable`

This is the first concrete implementation item in `M005/S01`.

---

## Next recommended starting point

### Start here next session
Implement:
- `M005 / S01`
- `TB-001`

Specifically:
1. update `app/detector.py`
   - apply the approved gate only to `notable` promotion
   - do **not** change `watch` yet
2. add or update detector tests
3. run full `pytest -q`
4. verify live server still starts cleanly
5. update `docs/TUNING-BACKLOG.md`
   - mark `TB-001` as `applied`
6. then continue to:
   - `TB-007` / flow-direction coherence
   - eventual **Apply recommended tweak** UI workflow

---

## Durable backlog / planning sources

Use these as source of truth next session:

- `docs/TUNING-BACKLOG.md` — tuning recommendations and statuses
- `README.md` — current product overview
- `USER_GUIDE.md` — current operator guidance
- `HANDOFF.md` — this file
- `ROADMAP.md` / GSD milestone state — `M005`

---

## Important operational notes

### If the app is failing to start
First suspect **multiple stray app processes**.

On Windows:
```powershell
Get-CimInstance Win32_Process |
  Where-Object { $_.Name -eq "python.exe" -and $_.CommandLine -match "-m app" } |
  ForEach-Object { Stop-Process -Id $_.ProcessId -Force }
```
Then start one clean instance:
```powershell
py -m app
```

### SQLite lock hardening already added
`app/db.py` now uses:
- `timeout=30s`
- `PRAGMA busy_timeout = 30000`
- `PRAGMA journal_mode = WAL`
- `PRAGMA synchronous = NORMAL`

So if locking still appears, suspect multi-process contention first.

---

## Test status

Latest full-suite verification this session:
- **63 passed**

That is the current clean baseline.

---

## Local commits added this session

Not exhaustive by feature, but the meaningful recent commits include:
- `40f8b4c` — analyst fallback (Anthropic primary, Perplexity fallback)
- `4dcab00` — inline Claude analyst on signal cards
- `2beb2da` — compact metric strip
- `d4102f8` — live feed hardening, series/event resolution, compact UI, docs

There may also be additional uncommitted planning/doc changes from the very end of the session if this handoff is being read before the final local commit is made.

---

## Bottom line

The project is now in a much stronger place:
- live feed works
- UI is much cleaner
- signal interpretation is live
- tuning advice is live
- recommendations are durably tracked

The next session should begin by turning the **first approved tuning recommendation** into actual detector logic.
