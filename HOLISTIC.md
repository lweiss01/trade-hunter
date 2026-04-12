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

**Resume from last handoff**

Initiate M017 (Distribution & Licensing) to automate the build-time separation of Public (Simulation) and Commercial (Live) editions using scripts/distribute.py.

## Latest Work Status

Hardened terminology and UI across the entire stack. Standardized the 4-tier signal hierarchy (WHALE CLUSTER, SIGNAL, NOTABLE, WATCH). Purged 'ghost' features and legacy 'Winston' references. Deployed official commercial landing page to GitHub Pages.

## What Was Tried

- Nothing recorded yet.

## What To Try Next

- Initiate M017 (Distribution & Licensing) to automate the build-time separation of Public (Simulation) and Commercial (Live) editions using scripts/distribute.py.

## Active Plan

- None yet - will be set once work begins.

## Overall Impact So Far

- Nothing recorded yet.

## Regression Watch

- Review the regression watch document before changing related behavior.

## Key Assumptions

- None recorded.

## Blockers

- Manual separation of Public vs Commercial source code (targeted by M017)
- None for current phase

## Changed Files In Current Session

- No repo changes detected for the active session.

## Pending Work Queue

- Continue recent repo work: Initiate M017 (Distribution & Licensing) to automate the build-time separation of Public (Simulation) and Commercial (Live) editions using scripts/distribute.py.

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

- Last updated: 2026-04-12T22:47:47.970Z
- Last handoff: Hardened terminology and UI across the entire stack. Standardized the 4-tier signal hierarchy (WHALE CLUSTER, SIGNAL, NOTABLE, WATCH). Purged 'ghost' features and legacy 'Winston' references. Deployed official commercial landing page to GitHub Pages.
- Pending sessions remembered: 1
