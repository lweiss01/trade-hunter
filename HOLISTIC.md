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

**Milestone Audit & Whale Detection Planning**

Audit existing GSD milestones (M002-M008) to align the stale state with recent progress and determine the remaining work. Begin planning for Whale Detection (R002) to identify large-size position entries.

## Latest Work Status

Dashboard parity work complete. Analyst rationale and threshold notes restored to signal cards. Project docs updated to reflect completion of UI work and new Whale Detection requirement (R002).

## What Was Tried

- Restored analyst rationale and threshold notes to dashboard signal cards.
- Verified dashboard automatic refresh picks up analyst updates.
- Recorded new Whale Detection requirement (R002) in REQUIREMENTS.md.
- Updated PROJECT.md to reflect UI parity completion and set next focus.

## What To Try Next

- **Milestone Audit**: Review ROADMAP.md and slice plans for M002-M008. Many tasks in these milestones have already been implemented (e.g., tuning advisor, settings persistence) but are not marked as complete in GSD artifacts.
- **Whale Detection Design**: Define the logic for "whale" detection—should it be a fixed notional floor ($5k+), a standard deviation from market mean, or a percentage of open interest?
- **CSS cleanup**: Prune unused/duplicate styles in `dashboard.css`.

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

- .bg-shell/manifest.json
- .env
- app/server.py
- app/static/dashboard.js
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

- Last updated: 2026-04-05T20:23:59.949Z
- Last handoff: None yet.
- Pending sessions remembered: 0
