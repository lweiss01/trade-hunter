# GitHub Copilot Adapter

## Product North Star

Open repo, start working, Holistic quietly keeps continuity alive.

Use this adapter to move toward that outcome: less manual setup, less re-briefing, and more continuity preserved by default.

## Tool-Specific Notes

- Copilot should pick up repo guidance from `.github/copilot-instructions.md` alongside the shared Holistic docs.
- Keep Holistic as the continuity layer and Copilot instructions as the tool-specific behavior layer.

## Startup Contract

1. Read `HOLISTIC.md`.
2. Review `project-history.md`, `regression-watch.md`, and `zero-touch.md` for durable memory before editing related code.
3. If the Holistic daemon is installed, treat passive session capture as already active.
4. Use the repo-local Holistic helper when you need an explicit recap or recovery flow.
5. Recap the current state for the user in the first 30 seconds.
6. Ask: continue as planned, tweak the plan, or start something new.

### Startup Notes For GitHub Copilot

- Review `.github/copilot-instructions.md` after the Holistic recap so Copilot gets both continuity and local coding rules.

Use the repo-local Holistic helper in this repo: Windows `.\.holistic\system\holistic.cmd resume --agent copilot`; macOS/Linux `./.holistic/system/holistic resume --agent copilot`.

## Checkpoint Contract

Use the repo-local Holistic helper for checkpoints in this repo when:

- the task focus changes
- you are about to compact or clear context
- you finish a meaningful chunk of work
- you fix or alter behavior that could regress later

Include impact notes and regression risks when they matter.

### Checkpoint Notes For GitHub Copilot

- Checkpoint after multi-file edits so Copilot sessions do not lose why a change set exists.

Use the repo-local Holistic helper in this repo: Windows `.\.holistic\system\holistic.cmd checkpoint --reason "<what changed>"`; macOS/Linux `./.holistic/system/holistic checkpoint --reason "<what changed>"`.

## Handoff Contract

- Preferred: map your session-end workflow to the repo-local Holistic helper with `handoff`
- Fallback: ask the user to run the repo-local Holistic helper with `handoff` before leaving the session

### Handoff Notes For GitHub Copilot

- End with a real handoff instead of relying on editor chat history surviving between Copilot sessions.

Use the repo-local Holistic helper in this repo: Windows `.\.holistic\system\holistic.cmd handoff`; macOS/Linux `./.holistic/system/holistic handoff`.

## Before ending this session

Run:
```
holistic handoff --summary "..." --next "..."
```
This keeps repo memory current for the next agent.
