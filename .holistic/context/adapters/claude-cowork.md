# Claude/Cowork Adapter

## Product North Star

Open repo, start working, Holistic quietly keeps continuity alive.

Use this adapter to move toward that outcome: less manual setup, less re-briefing, and more continuity preserved by default.

## Tool-Specific Notes

- Claude/Cowork can use Holistic through MCP-style tool calls when available.
- When MCP is active, prefer Holistic tools over free-form summaries for startup and session close.

## Startup Contract

1. Read `HOLISTIC.md`.
2. Review `project-history.md`, `regression-watch.md`, and `zero-touch.md` for durable memory before editing related code.
3. If the Holistic daemon is installed, treat passive session capture as already active.
4. Use the repo-local Holistic helper when you need an explicit recap or recovery flow.
5. Recap the current state for the user in the first 30 seconds.
6. Ask: continue as planned, tweak the plan, or start something new.

### Startup Notes For Claude/Cowork

- Use `holistic_resume` or the mapped startup hook instead of manually reconstructing prior work.
- Let the initial recap shape the first answer before editing code.

Use the repo-local Holistic helper in this repo: Windows `.\.holistic\system\holistic.cmd resume --agent claude`; macOS/Linux `./.holistic/system/holistic resume --agent claude`.

## Checkpoint Contract

Use the repo-local Holistic helper for checkpoints in this repo when:

- the task focus changes
- you are about to compact or clear context
- you finish a meaningful chunk of work
- you fix or alter behavior that could regress later

Include impact notes and regression risks when they matter.

### Checkpoint Notes For Claude/Cowork

- Checkpoint after meaningful implementation slices, especially before asking Claude to branch into analysis-heavy discussion.

Use the repo-local Holistic helper in this repo: Windows `.\.holistic\system\holistic.cmd checkpoint --reason "<what changed>"`; macOS/Linux `./.holistic/system/holistic checkpoint --reason "<what changed>"`.

## Handoff Contract

- Preferred: map your session-end workflow to the repo-local Holistic helper with `handoff`
- Fallback: ask the user to run the repo-local Holistic helper with `handoff` before leaving the session

### Handoff Notes For Claude/Cowork

- Prefer `holistic_handoff` when the tool is available so the handoff fields stay structured.

Use the repo-local Holistic helper in this repo: Windows `.\.holistic\system\holistic.cmd handoff`; macOS/Linux `./.holistic/system/holistic handoff`.

## Before ending this session

Call `holistic_handoff` with a summary of what you did and what should happen next. This keeps repo memory current for the next agent.
