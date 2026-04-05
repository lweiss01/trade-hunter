# HOLISTIC

<!-- ═══════════════════════════════════════════════════════════════════════
     AGENT INSTRUCTIONS - READ THIS ENTIRE FILE BEFORE DOING ANYTHING ELSE
     ═══════════════════════════════════════════════════════════════════════

  1. Read this file top-to-bottom.
  2. Read AGENTS.md for the setup steps specific to your agent.
  3. Summarise to the user: what was last worked on, what's planned next.
  4. Ask: "What would you like to work on - continue recent work, or start something new?"
  5. Open the session with the repo-local Holistic helper for this repo.

  ⚠️  If you are about to edit a file listed under KNOWN FIXES, STOP and
     read that fix entry carefully before proceeding.
  ════════════════════════════════════════════════════════════════════════ -->

## Start Here

This repo uses Holistic for cross-agent handoffs. The source of truth is the repo itself: handoff docs, history, and regression memory should be committed and synced so any device can continue. Read this file first, then review the long-term history docs and zero-touch architecture note, then use the adapter doc for your app. The Holistic daemon is optional and only improves passive capture on devices where it is installed.

Use the repo-local Holistic helper in this repo: Windows `.\.holistic\system\holistic.cmd resume --agent <your-agent-name>`; macOS/Linux `./.holistic/system/holistic resume --agent <your-agent-name>`.

## Product North Star

Open repo, start working, Holistic quietly keeps continuity alive.

That is the intended end state for this project. Prefer changes that reduce ceremony, keep continuity durable, and make Holistic fade further into the background of normal work.

## Current Objective

**M007 Dashboard UI Redesign — Markets + Settings parity remaining**

Dashboard parity against `design-proposal.html` is substantially complete. Next work is the Markets page parity pass, then the Settings page parity pass, then a final dashboard composition cleanup.

## Latest Work Status

Dashboard parity committed and pushed to `origin/main` at `c69b029`. 21 commits this session. Dev server runs on `:8765` — may need restart (check `bg_shell list` or run `python -m app`).

## What Was Tried

### Dashboard parity — completed this session
- Kalshi pill now shows real feed health (OFFLINE/STALE/Xm ago), not mode
- Application mode moved from topbar badge to quiet metrics-row chip
- Topbar height reduced 56→52px; nav tabs, pills, forms all tightened
- Brand block: new cleaner logo (less chrome), softer teal drop-shadow icon
- Metrics row chips tightened (padding, gap, type scale)
- Panel headers slimmed (padding, sort/toggle controls)
- Topic filter chips aligned to proposal (height, gap, border)
- Panel body/empty-state spacing reduced
- Right column denser: flow rows and tape table rows both tightened
- Footer restructured: left/right layout, version chip, plain links, outlined User Guide

## What To Try Next

1. **Markets page parity pass** — compare running Markets tab vs. `design-proposal.html` markets section: tracked-ticker table, category browser, shortcut chips, spacing
2. **Settings page parity pass** — compare running Settings vs. `design-proposal.html` settings section: panel grouping, control sizing, section headers, save bar
3. **Dashboard final composition pass** — left/right vertical balance, remaining minor gaps, CSS legacy cleanup

## Active Plan

See `.holistic/context/current-plan.md` for the full step-by-step.

## Overall Impact So Far

The dashboard now closely matches `design-proposal.html`. All structural, spacing, and typography changes are committed. Feed status is truthful. Markets and Settings need the same treatment.

## Regression Watch

See `.holistic/context/regression-watch.md` for the full list (RW001–RW010). Key items:
- Topbar full-width, ticker input must not overlap pills (RW001)
- Settings isolated from Dashboard/Markets (RW002)
- Signal cards: single left stripe only (RW003)
- Live Trade Flow: view-only, no click behavior (RW004)
- Kalshi pill: actual feed health, not mode (RW009)
- Application mode chip in metrics row, not topbar (RW010)

## Key Assumptions

- User's acceptance bar: "if it doesn't look JUST LIKE the design-proposal, IT'S NOT RIGHT"
- Work at task granularity — complete, verify, commit, then move to next item
- Do not bundle unrelated fixes in the same commit

## Blockers

- Dev server showed a connection error at session end — may need restart
- TB-ID in dashboard advisor needs a fresh advisor snapshot (enough signals to trigger)

## Changed Files In Current Session

- .bg-shell/manifest.json
- .env
- .gsd/DECISIONS.md
- .gsd/KNOWLEDGE.md
- .gsd/PROJECT.md
- .gsd/REQUIREMENTS.md
- .gsd/STATE.md
- .gsd/audits/2026-04-05-002453-bring-the-app-ui-and-navigation-into-par.md
- .gsd/event-log.jsonl
- .gsd/gsd.db
- .gsd/gsd.db-shm
- .gsd/gsd.db-wal
- .gsd/milestones/M002/M002-ROADMAP.md
- .gsd/milestones/M003/M003-ROADMAP.md
- .gsd/milestones/M004/M004-ROADMAP.md
- .gsd/milestones/M005/M005-ROADMAP.md
- .gsd/milestones/M006/M006-ROADMAP.md
- .gsd/milestones/M007/M007-ROADMAP.md
- .gsd/milestones/M007/slices/S01/S01-PLAN.md
- .gsd/milestones/M007/slices/S02/S02-PLAN.md
- .gsd/milestones/M007/slices/S03/S03-PLAN.md
- .gsd/milestones/M007/slices/S03/tasks/T01-PLAN.md
- .gsd/milestones/M007/slices/S03/tasks/T02-PLAN.md
- .gsd/milestones/M007/slices/S03/tasks/T03-PLAN.md
- .gsd/milestones/M007/slices/S03/tasks/T04-PLAN.md
- .gsd/milestones/M007/slices/S04/S04-PLAN.md
- .gsd/milestones/M007/slices/S04/tasks/T01-PLAN.md
- .gsd/milestones/M007/slices/S04/tasks/T02-PLAN.md
- .gsd/milestones/M007/slices/S04/tasks/T03-PLAN.md
- .gsd/milestones/M007/slices/S04/tasks/T04-PLAN.md
- .gsd/milestones/M007/slices/S05/S05-PLAN.md
- .gsd/milestones/M007/slices/S05/tasks/T01-PLAN.md
- .gsd/milestones/M007/slices/S05/tasks/T02-PLAN.md
- .gsd/milestones/M007/slices/S05/tasks/T03-PLAN.md
- .gsd/milestones/M007/slices/S05/tasks/T04-PLAN.md
- .gsd/milestones/M007/slices/S06/S06-PLAN.md
- .gsd/milestones/M007/slices/S07/S07-PLAN.md
- .gsd/milestones/M007/slices/S08/S08-PLAN.md
- .gsd/milestones/M007/slices/S08/tasks/T01-PLAN.md
- .gsd/milestones/M007/slices/S08/tasks/T02-PLAN.md
- .gsd/milestones/M007/slices/S08/tasks/T03-PLAN.md
- .gsd/milestones/M007/slices/S08/tasks/T04-PLAN.md
- .gsd/milestones/M007/slices/S09/S09-PLAN.md
- .gsd/milestones/M007/slices/S09/tasks/T01-PLAN.md
- .gsd/milestones/M007/slices/S09/tasks/T02-PLAN.md
- .gsd/milestones/M007/slices/S09/tasks/T03-PLAN.md
- .gsd/milestones/M007/slices/S09/tasks/T04-PLAN.md
- .gsd/milestones/M007/slices/S10/S10-PLAN.md
- .gsd/milestones/M007/slices/S10/tasks/T01-PLAN.md
- .gsd/milestones/M007/slices/S10/tasks/T02-PLAN.md
- .gsd/milestones/M007/slices/S10/tasks/T03-PLAN.md
- .gsd/milestones/M007/slices/S10/tasks/T04-PLAN.md
- .gsd/milestones/M007/slices/S11/S11-PLAN.md
- .gsd/milestones/M007/slices/S12/S12-PLAN.md
- .gsd/milestones/M007/slices/S13/S13-PLAN.md
- .gsd/milestones/M007/slices/S14/S14-PLAN.md
- .gsd/milestones/M007/slices/S14/tasks/T01-PLAN.md
- .gsd/milestones/M007/slices/S14/tasks/T02-PLAN.md
- .gsd/milestones/M007/slices/S14/tasks/T03-PLAN.md
- .gsd/milestones/M007/slices/S14/tasks/T04-PLAN.md
- .gsd/milestones/M007/slices/S15/S15-PLAN.md
- .gsd/milestones/M007/slices/S16/S16-PLAN.md
- .gsd/milestones/M007/slices/S17/S17-PLAN.md
- .gsd/milestones/M007/slices/S18/S18-PLAN.md
- .gsd/milestones/M007/slices/S19/S19-PLAN.md
- .gsd/milestones/M007/slices/S20/S20-PLAN.md
- .gsd/milestones/M007/slices/S21/S21-PLAN.md
- .gsd/milestones/M007/slices/S21/tasks/T01-PLAN.md
- .gsd/milestones/M007/slices/S21/tasks/T02-PLAN.md
- .gsd/milestones/M007/slices/S21/tasks/T03-PLAN.md
- .gsd/milestones/M007/slices/S21/tasks/T04-PLAN.md
- .gsd/milestones/M008/M008-ROADMAP.md
- .gsd/milestones/M008/slices/S01/S01-PLAN.md
- .gsd/milestones/M008/slices/S01/tasks/T01-PLAN.md
- .gsd/milestones/M008/slices/S01/tasks/T02-PLAN.md
- .gsd/milestones/M008/slices/S01/tasks/T03-PLAN.md
- .gsd/milestones/M008/slices/S02/S02-PLAN.md
- .gsd/state-manifest.json
- README.md
- USER_GUIDE.md
- app/__main__.py
- app/config.py
- app/feeds/kalshi_pykalshi.py
- app/server.py
- app/service.py
- app/static/dashboard.css
- app/static/dashboard.js
- app/static/favicon-32x32.png
- app/static/favicon.svg
- app/static/index.html
- app/static/trade-hunter-logo4.png
- docs/index.html
- trade-hunter.cmd
- trade_hunter.db
- trade_hunter.db-shm
- trade_hunter.db-wal

## Pending Work Queue

- None.

## Long-Term Memory

- Project history: [.holistic/context/project-history.md](.holistic/context/project-history.md)
- Regression watch: [.holistic/context/regression-watch.md](.holistic/context/regression-watch.md)
- Zero-touch architecture: [.holistic/context/zero-touch.md](.holistic/context/zero-touch.md)
- Portable sync model: handoffs are intended to be committed and synced so any device with repo access can continue.

## Supporting Documents

- State file: [.holistic/state.json](.holistic/state.json)
- Current plan: [.holistic/context/current-plan.md](.holistic/context/current-plan.md)
- Session protocol: [.holistic/context/session-protocol.md](.holistic/context/session-protocol.md)
- Session archive: [.holistic/sessions](.holistic/sessions)
- Adapter docs:
- codex: [.holistic/context/adapters/codex.md](.holistic/context/adapters/codex.md)
- claude: [.holistic/context/adapters/claude-cowork.md](.holistic/context/adapters/claude-cowork.md)
- antigravity: [.holistic/context/adapters/antigravity.md](.holistic/context/adapters/antigravity.md)
- gemini: [.holistic/context/adapters/gemini.md](.holistic/context/adapters/gemini.md)
- copilot: [.holistic/context/adapters/copilot.md](.holistic/context/adapters/copilot.md)
- cursor: [.holistic/context/adapters/cursor.md](.holistic/context/adapters/cursor.md)
- goose: [.holistic/context/adapters/goose.md](.holistic/context/adapters/goose.md)
- gsd: [.holistic/context/adapters/gsd.md](.holistic/context/adapters/gsd.md)
- gsd2: [.holistic/context/adapters/gsd2.md](.holistic/context/adapters/gsd2.md)

## Historical Memory

- Last updated: 2026-04-04T17:48:58.031Z
- Last handoff: None yet.
- Pending sessions remembered: 0
