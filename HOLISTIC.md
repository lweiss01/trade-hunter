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

M010: Cross-Platform Whale Flow (Polymarket & Kalshi)

## Latest Work Status

Detected branch switch; review the new branch context.

## What Was Tried

- Nothing recorded yet.

## What To Try Next

- M010: Cross-Platform Whale Flow (Polymarket & Kalshi)

## Active Plan

- Read HOLISTIC.md
- M010: Cross-Platform Whale Flow (Polymarket & Kalshi)

## Overall Impact So Far

- Nothing recorded yet.

## Regression Watch

- Review the regression watch document before changing related behavior.

## Key Assumptions

- None recorded.

## Blockers

- None.

## Changed Files In Current Session

- .cursorrules
- .github/copilot-instructions.md
- .windsurfrules
- README.md
- ROADMAP.md
- USER_GUIDE.md
- app/__main__.py
- app/analyst.py
- app/config.py
- app/edition.py
- app/feeds/kalshi_pykalshi.py
- app/server.py
- app/service.py
- app/static/dashboard.css
- app/static/dashboard.js
- app/static/index.html
- docs/TUNING-BACKLOG.md
- scratch/patch_dashboard.py
- scratch/recover_tickers.py
- scratch/test_rotation.py
- scripts/distribute.py
- scripts/run_checks.py
- tests/test_security_hardening.py
- trade-hunter.cmd
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

- Last updated: 2026-04-12T19:03:31.476Z
- Last handoff: Completed comprehensive security hardening pass (M014-M016). Implemented Admin and Ingest token auth, CSRF protection, .env injection prevention, safe port-kill, and automated security regression tests (97/97 passing).
- Pending sessions remembered: 0
