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

**Continue recent repo work**

Continue work around .bg-shell/manifest.json, .gitattributes, .pytest_cache/v/cache/nodeids

## Latest Work Status

Detected branch switch; review the new branch context.

## What Was Tried

- Nothing recorded yet.

## What To Try Next

- Ask the user what they'd like to work on.

## Active Plan

- Review the most recently changed files
- Continue the current implementation thread

## Overall Impact So Far

- Nothing recorded yet.

## Regression Watch

- Review the regression watch document before changing related behavior.

## Key Assumptions

- None recorded.

## Blockers

- None.

## Changed Files In Current Session

- .antigravity_session/implementation.md
- .antigravity_session/planning/trade-hunter-ui-revision-checklist.md
- .antigravity_session/task.md
- .antigravity_session/walkthrough.md
- .beads/beads.db
- .beads/beads.db-shm
- .beads/beads.db-wal
- .beads/daemon-error
- .beads/daemon.lock
- .beads/daemon.log
- .bg-shell/manifest.json
- .cursorrules
- .env
- .github/copilot-instructions.md
- .gitignore
- .gsd-id
- .gsd/PROJECT.md
- .gsd/REQUIREMENTS.md
- .gsd/STATE.md
- .gsd/activity/003-execute-task-M008-S01-T01.jsonl
- .gsd/activity/004-execute-task-M008-S01-T01.jsonl
- .gsd/activity/005-execute-task-M008-S01-T01.jsonl
- .gsd/activity/006-execute-task-M008-S01-T01.jsonl
- .gsd/activity/007-execute-task-M008-S01-T01.jsonl
- .gsd/doctor-history.jsonl
- .gsd/event-log.jsonl
- .gsd/gsd.db
- .gsd/gsd.db-shm
- .gsd/gsd.db-wal
- .gsd/journal/2026-04-07.jsonl
- .gsd/metrics.json
- .gsd/milestones/M002/M002-ROADMAP.md
- .gsd/milestones/M002/M002-SUMMARY.md
- .gsd/milestones/M002/slices/S01/S01-PLAN.md
- .gsd/milestones/M002/slices/S01/S01-SUMMARY.md
- .gsd/milestones/M002/slices/S01/S01-UAT.md
- .gsd/milestones/M002/slices/S01/tasks/T01-SUMMARY.md
- .gsd/milestones/M002/slices/S01/tasks/T02-SUMMARY.md
- .gsd/milestones/M002/slices/S01/tasks/T03-SUMMARY.md
- .gsd/milestones/M002/slices/S01/tasks/T04-SUMMARY.md
- .gsd/milestones/M002/slices/S02/S02-PLAN.md
- .gsd/milestones/M002/slices/S02/S02-SUMMARY.md
- .gsd/milestones/M002/slices/S02/S02-UAT.md
- .gsd/milestones/M002/slices/S02/tasks/T01-SUMMARY.md
- .gsd/milestones/M002/slices/S02/tasks/T02-SUMMARY.md
- .gsd/milestones/M002/slices/S02/tasks/T03-SUMMARY.md
- .gsd/milestones/M002/slices/S02/tasks/T04-SUMMARY.md
- .gsd/milestones/M002/slices/S03/S03-PLAN.md
- .gsd/milestones/M002/slices/S03/S03-SUMMARY.md
- .gsd/milestones/M002/slices/S03/S03-UAT.md
- .gsd/milestones/M002/slices/S03/tasks/T01-SUMMARY.md
- .gsd/milestones/M002/slices/S03/tasks/T02-SUMMARY.md
- .gsd/milestones/M002/slices/S03/tasks/T03-SUMMARY.md
- .gsd/milestones/M002/slices/S03/tasks/T04-SUMMARY.md
- .gsd/milestones/M002/slices/S03/tasks/T05-SUMMARY.md
- .gsd/milestones/M003/M003-ROADMAP.md
- .gsd/milestones/M003/M003-SUMMARY.md
- .gsd/milestones/M003/slices/S01/S01-PLAN.md
- .gsd/milestones/M003/slices/S01/S01-SUMMARY.md
- .gsd/milestones/M003/slices/S01/S01-UAT.md
- .gsd/milestones/M003/slices/S01/tasks/T01-SUMMARY.md
- .gsd/milestones/M003/slices/S01/tasks/T02-SUMMARY.md
- .gsd/milestones/M003/slices/S01/tasks/T03-SUMMARY.md
- .gsd/milestones/M003/slices/S01/tasks/T04-SUMMARY.md
- .gsd/milestones/M003/slices/S01/tasks/T05-SUMMARY.md
- .gsd/milestones/M003/slices/S02/S02-PLAN.md
- .gsd/milestones/M003/slices/S02/S02-SUMMARY.md
- .gsd/milestones/M003/slices/S02/S02-UAT.md
- .gsd/milestones/M003/slices/S02/tasks/T01-SUMMARY.md
- .gsd/milestones/M003/slices/S02/tasks/T02-SUMMARY.md
- .gsd/milestones/M003/slices/S02/tasks/T03-SUMMARY.md
- .gsd/milestones/M003/slices/S02/tasks/T04-SUMMARY.md
- .gsd/milestones/M003/slices/S02/tasks/T05-SUMMARY.md
- .gsd/milestones/M003/slices/S03/S03-PLAN.md
- .gsd/milestones/M003/slices/S03/S03-SUMMARY.md
- .gsd/milestones/M003/slices/S03/S03-UAT.md
- .gsd/milestones/M003/slices/S03/tasks/T01-SUMMARY.md
- .gsd/milestones/M003/slices/S03/tasks/T02-SUMMARY.md
- .gsd/milestones/M003/slices/S03/tasks/T03-SUMMARY.md
- .gsd/milestones/M003/slices/S03/tasks/T04-SUMMARY.md
- .gsd/milestones/M003/slices/S03/tasks/T05-SUMMARY.md
- .gsd/milestones/M004/M004-ROADMAP.md
- .gsd/milestones/M004/M004-SUMMARY.md
- .gsd/milestones/M004/slices/S01/S01-PLAN.md
- .gsd/milestones/M004/slices/S01/S01-SUMMARY.md
- .gsd/milestones/M004/slices/S01/S01-UAT.md
- .gsd/milestones/M004/slices/S01/tasks/T01-SUMMARY.md
- .gsd/milestones/M004/slices/S01/tasks/T02-SUMMARY.md
- .gsd/milestones/M004/slices/S01/tasks/T03-SUMMARY.md
- .gsd/milestones/M004/slices/S01/tasks/T04-SUMMARY.md
- .gsd/milestones/M004/slices/S01/tasks/T05-SUMMARY.md
- .gsd/milestones/M004/slices/S02/S02-PLAN.md
- .gsd/milestones/M004/slices/S02/S02-SUMMARY.md
- .gsd/milestones/M004/slices/S02/S02-UAT.md
- .gsd/milestones/M004/slices/S02/tasks/T01-SUMMARY.md
- .gsd/milestones/M004/slices/S02/tasks/T02-SUMMARY.md
- .gsd/milestones/M004/slices/S02/tasks/T03-SUMMARY.md
- .gsd/milestones/M004/slices/S02/tasks/T04-SUMMARY.md
- .gsd/milestones/M004/slices/S02/tasks/T05-SUMMARY.md
- .gsd/milestones/M004/slices/S03/S03-PLAN.md
- .gsd/milestones/M004/slices/S04/S04-PLAN.md
- .gsd/milestones/M004/slices/S04/S04-SUMMARY.md
- .gsd/milestones/M004/slices/S04/S04-UAT.md
- .gsd/milestones/M004/slices/S04/tasks/T01-SUMMARY.md
- .gsd/milestones/M004/slices/S04/tasks/T02-SUMMARY.md
- .gsd/milestones/M004/slices/S04/tasks/T03-SUMMARY.md
- .gsd/milestones/M004/slices/S04/tasks/T04-SUMMARY.md
- .gsd/milestones/M004/slices/S04/tasks/T05-SUMMARY.md
- .gsd/milestones/M005/M005-ROADMAP.md
- .gsd/milestones/M005/M005-SUMMARY.md
- .gsd/milestones/M005/slices/S01/S01-PLAN.md
- .gsd/milestones/M005/slices/S02/S02-PLAN.md
- .gsd/milestones/M005/slices/S03/S03-PLAN.md
- .gsd/milestones/M005/slices/S04/S04-PLAN.md
- .gsd/milestones/M006/M006-ROADMAP.md
- .gsd/milestones/M006/M006-SUMMARY.md
- .gsd/milestones/M006/slices/S01/S01-PLAN.md
- .gsd/milestones/M006/slices/S01/tasks/T01-SUMMARY.md
- .gsd/milestones/M006/slices/S01/tasks/T02-SUMMARY.md
- .gsd/milestones/M006/slices/S01/tasks/T03-SUMMARY.md
- .gsd/milestones/M006/slices/S01/tasks/T04-SUMMARY.md
- .gsd/milestones/M006/slices/S02/S02-PLAN.md
- .gsd/milestones/M006/slices/S02/tasks/T01-SUMMARY.md
- .gsd/milestones/M006/slices/S02/tasks/T02-SUMMARY.md
- .gsd/milestones/M006/slices/S02/tasks/T03-SUMMARY.md
- .gsd/milestones/M006/slices/S02/tasks/T04-SUMMARY.md
- .gsd/milestones/M006/slices/S03/S03-PLAN.md
- .gsd/milestones/M006/slices/S03/tasks/T01-SUMMARY.md
- .gsd/milestones/M006/slices/S03/tasks/T02-SUMMARY.md
- .gsd/milestones/M006/slices/S03/tasks/T03-SUMMARY.md
- .gsd/milestones/M006/slices/S04/S04-PLAN.md
- .gsd/milestones/M006/slices/S04/tasks/T01-SUMMARY.md
- .gsd/milestones/M006/slices/S04/tasks/T02-SUMMARY.md
- .gsd/milestones/M006/slices/S04/tasks/T03-SUMMARY.md
- .gsd/milestones/M006/slices/S04/tasks/T04-SUMMARY.md
- .gsd/milestones/M006/slices/S05/S05-PLAN.md
- .gsd/milestones/M007/M007-ROADMAP.md
- .gsd/milestones/M007/M007-SUMMARY.md
- .gsd/milestones/M007/slices/S01/S01-PLAN.md
- .gsd/milestones/M007/slices/S02/S02-PLAN.md
- .gsd/milestones/M007/slices/S03/S03-PLAN.md
- .gsd/milestones/M007/slices/S03/tasks/T01-SUMMARY.md
- .gsd/milestones/M007/slices/S03/tasks/T02-SUMMARY.md
- .gsd/milestones/M007/slices/S03/tasks/T03-SUMMARY.md
- .gsd/milestones/M007/slices/S03/tasks/T04-SUMMARY.md
- .gsd/milestones/M007/slices/S04/S04-PLAN.md
- .gsd/milestones/M007/slices/S04/tasks/T01-SUMMARY.md
- .gsd/milestones/M007/slices/S04/tasks/T02-SUMMARY.md
- .gsd/milestones/M007/slices/S04/tasks/T03-SUMMARY.md
- .gsd/milestones/M007/slices/S04/tasks/T04-SUMMARY.md
- .gsd/milestones/M007/slices/S05/S05-PLAN.md
- .gsd/milestones/M007/slices/S05/tasks/T01-SUMMARY.md
- .gsd/milestones/M007/slices/S05/tasks/T02-SUMMARY.md
- .gsd/milestones/M007/slices/S05/tasks/T03-SUMMARY.md
- .gsd/milestones/M007/slices/S05/tasks/T04-SUMMARY.md
- .gsd/milestones/M007/slices/S06/S06-PLAN.md
- .gsd/milestones/M007/slices/S07/S07-PLAN.md
- .gsd/milestones/M007/slices/S08/S08-PLAN.md
- .gsd/milestones/M007/slices/S08/tasks/T01-SUMMARY.md
- .gsd/milestones/M007/slices/S08/tasks/T02-SUMMARY.md
- .gsd/milestones/M007/slices/S08/tasks/T03-SUMMARY.md
- .gsd/milestones/M007/slices/S08/tasks/T04-SUMMARY.md
- .gsd/milestones/M007/slices/S09/S09-PLAN.md
- .gsd/milestones/M007/slices/S09/tasks/T01-SUMMARY.md
- .gsd/milestones/M007/slices/S09/tasks/T02-SUMMARY.md
- .gsd/milestones/M007/slices/S09/tasks/T03-SUMMARY.md
- .gsd/milestones/M007/slices/S09/tasks/T04-SUMMARY.md
- .gsd/milestones/M007/slices/S10/S10-PLAN.md
- .gsd/milestones/M007/slices/S10/tasks/T01-SUMMARY.md
- .gsd/milestones/M007/slices/S10/tasks/T02-SUMMARY.md
- .gsd/milestones/M007/slices/S10/tasks/T03-SUMMARY.md
- .gsd/milestones/M007/slices/S10/tasks/T04-SUMMARY.md
- .gsd/milestones/M007/slices/S11/S11-PLAN.md
- .gsd/milestones/M007/slices/S12/S12-PLAN.md
- .gsd/milestones/M007/slices/S13/S13-PLAN.md
- .gsd/milestones/M007/slices/S14/S14-PLAN.md
- .gsd/milestones/M007/slices/S14/tasks/T01-SUMMARY.md
- .gsd/milestones/M007/slices/S14/tasks/T02-SUMMARY.md
- .gsd/milestones/M007/slices/S14/tasks/T03-SUMMARY.md
- .gsd/milestones/M007/slices/S14/tasks/T04-SUMMARY.md
- .gsd/milestones/M007/slices/S15/S15-PLAN.md
- .gsd/milestones/M007/slices/S16/S16-PLAN.md
- .gsd/milestones/M007/slices/S17/S17-PLAN.md
- .gsd/milestones/M007/slices/S18/S18-PLAN.md
- .gsd/milestones/M007/slices/S19/S19-PLAN.md
- .gsd/milestones/M007/slices/S20/S20-PLAN.md
- .gsd/milestones/M007/slices/S21/S21-PLAN.md
- .gsd/milestones/M007/slices/S21/tasks/T01-SUMMARY.md
- .gsd/milestones/M007/slices/S21/tasks/T02-SUMMARY.md
- .gsd/milestones/M007/slices/S21/tasks/T03-SUMMARY.md
- .gsd/milestones/M007/slices/S21/tasks/T04-SUMMARY.md
- .gsd/milestones/M008/M008-ROADMAP.md
- .gsd/milestones/M008/slices/S01/S01-PLAN.md
- .gsd/milestones/M008/slices/S02/S02-PLAN.md
- .gsd/milestones/M009/M009-ROADMAP.md
- .gsd/milestones/M009/slices/S01/S01-PLAN.md
- .gsd/milestones/M009/slices/S01/tasks/T01-PLAN.md
- .gsd/milestones/M009/slices/S01/tasks/T02-PLAN.md
- .gsd/milestones/M009/slices/S02/S02-PLAN.md
- .gsd/milestones/M009/slices/S03/S03-PLAN.md
- .gsd/milestones/M010/M010-CONTEXT.md
- .gsd/milestones/M010/M010-ROADMAP.md
- .gsd/milestones/M011/M011-CONTEXT.md
- .gsd/milestones/M011/M011-ROADMAP.md
- .gsd/milestones/M012/M012-CONTEXT.md
- .gsd/milestones/M012/M012-ROADMAP.md
- .gsd/milestones/M013/M013-CONTEXT.md
- .gsd/milestones/M013/M013-ROADMAP.md
- .gsd/notifications.jsonl
- .gsd/runtime/paused-session.json
- .gsd/runtime/units/execute-task-M001-S01-T01.json
- .gsd/runtime/units/execute-task-M001-S01-T02.json
- .gsd/runtime/units/execute-task-M001-S01-T03.json
- .gsd/runtime/units/execute-task-M008-S01-T01.json
- .gsd/state-manifest.json
- .pytest_cache/v/cache/nodeids
- .windsurfrules
- FINAL_SESSION_SUMMARY.md
- README.md
- ROADMAP.md
- SESSION_SUMMARY.md
- USER_GUIDE.md
- app/__main__.py
- app/analyst.py
- app/config.py
- app/detector.py
- app/server.py
- app/service.py
- app/static/dashboard.css
- app/static/dashboard.js
- app/static/index.html
- app/store.py
- docs/TUNING-BACKLOG.md
- fix_detector.py
- main.py
- test_defensive_logging.py
- test_kalshi_connection.py
- trade-hunter
- trade-hunter-ui-revision-checklist.md
- trade-hunter.cmd
- trade_hunter.db
- trade_hunter.db-shm
- trade_hunter.db-wal
- update_readme.py
- update_user_guide.py

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

- Last updated: 2026-04-05T22:08:05.323Z
- Last handoff: None yet.
- Pending sessions remembered: 0
