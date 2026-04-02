# AGENTS

<!-- ═══════════════════════════════════════════════════════════════════
     AGENT AUTO-START INSTRUCTIONS
     ═══════════════════════════════════════════════════════════════════

  YOU ARE READING THIS FILE AUTOMATICALLY AT SESSION START. GOOD.
  Now do the following BEFORE responding to the user or doing any work:

  1. Read HOLISTIC.md in full.
  2. Summarise to the user: what was last worked on, what's planned next,
     and flag any KNOWN FIXES they should be aware of.
  3. Ask: "What would you like to work on - continue recent work, or start something new?"
  4. Open the session with the repo-local Holistic helper for this repo.

  DO NOT skip step 1. HOLISTIC.md is the source of truth.
  ══════════════════════════════════════════════════════════════════ -->

## Holistic Protocol

### Product North Star

Open repo, start working, Holistic quietly keeps continuity alive.

Agents should treat that as the ultimate UX target. Prefer decisions that reduce manual ceremony while making checkpoint, resume, handoff, and regression-awareness more automatic and more reliable.

Every agent working in this repo should:

1. Read [HOLISTIC.md](./HOLISTIC.md) first.
2. Review [Project History](./.holistic/context/project-history.md), [Regression Watch](./.holistic/context/regression-watch.md), and [Zero-Touch Architecture](./.holistic/context/zero-touch.md) before changing behavior that may already have been fixed.
3. Read the app-specific adapter in `.holistic/context/adapters/`.
4. If the Holistic daemon is installed, assume passive capture is already running in the background.
5. Use the repo-local Holistic helper for explicit recap or recovery flows in this repo.
6. Recap the current state for the user and ask whether to continue, tweak the plan, or start something new.
7. Record a checkpoint when focus changes, before likely context compaction, and before handoff.

Use the repo-local Holistic helper in this repo: Windows `.\.holistic\system\holistic.cmd resume --agent <your-agent-name>`; macOS/Linux `./.holistic/system/holistic resume --agent <your-agent-name>`.

## Handoff Commands

-  the repo-local Holistic helper in this repo: Windows `.\.holistic\system\holistic.cmd checkpoint --reason "<why>"`; macOS/Linux `./.holistic/system/holistic checkpoint --reason "<why>"`.
-  the repo-local Holistic helper in this repo: Windows `.\.holistic\system\holistic.cmd checkpoint --fixed "<bug>" --fix-files "<file>" --fix-risk "<what would reintroduce it>"`; macOS/Linux `./.holistic/system/holistic checkpoint --fixed "<bug>" --fix-files "<file>" --fix-risk "<what would reintroduce it>"`.
- `holistic set-phase --phase "<id>" --name "<name>" --goal "<goal>"`
- `holistic complete-phase --phase "<id>" --next-phase "<id>" --next-name "<name>" --next-goal "<goal>"`
-  the repo-local Holistic helper in this repo: Windows `.\.holistic\system\holistic.cmd handoff`; macOS/Linux `./.holistic/system/holistic handoff`.
-  the repo-local Holistic helper in this repo: Windows `.\.holistic\system\holistic.cmd start-new --goal "<goal>"`; macOS/Linux `./.holistic/system/holistic start-new --goal "<goal>"`.
-  the repo-local Holistic helper in this repo: Windows `.\.holistic\system\holistic.cmd watch`; macOS/Linux `./.holistic/system/holistic watch`.

## Before Ending a Session

## Before ending this session

Run:
```
holistic handoff --summary "..." --next "..."
```
This keeps repo memory current for the next agent.

## Adding a New Agent Adapter

To add instructions for a new agent, create a file at:

`.holistic/context/adapters/<agent-name>.md`

Copy any existing adapter as a template and customise the agent name and startup steps.
Do not edit Holistic source files to register agents - adapters are data, not code.

## Landing the Plane (Session Completion)

**When ending a work session**, you MUST complete ALL steps below. Work is NOT complete until `git push` succeeds.

**MANDATORY WORKFLOW:**

1. **File issues for remaining work** - Create issues for anything that needs follow-up
2. **Run quality gates** (if code changed) - Tests, linters, builds
3. **Update issue status** - Close finished work, update in-progress items
4. **PUSH TO REMOTE** - This is MANDATORY:
   ```bash
   git pull --rebase
   bd sync
   git push
   git status  # MUST show "up to date with origin"
   ```
5. **Clean up** - Clear stashes, prune remote branches
6. **Verify** - All changes committed AND pushed
7. **Hand off** - Provide context for next session

**CRITICAL RULES:**
- Work is NOT complete until `git push` succeeds
- NEVER stop before pushing - that leaves work stranded locally
- NEVER say "ready to push when you are" - YOU must push
- If push fails, resolve and retry until it succeeds
