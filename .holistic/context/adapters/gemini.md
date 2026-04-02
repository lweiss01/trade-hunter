# Gemini Adapter

## Product North Star

Open repo, start working, Holistic quietly keeps continuity alive.

Use this adapter to move toward that outcome: less manual setup, less re-briefing, and more continuity preserved by default.

## Tool-Specific Notes

- Gemini should use repo-visible docs first: `HOLISTIC.md`, `GEMINI.md`, and the Holistic context folder.
- Treat `GEMINI.md` as the app-local companion to the shared Holistic memory.

## Startup Contract

1. Read `HOLISTIC.md`.
2. Review `project-history.md`, `regression-watch.md`, and `zero-touch.md` for durable memory before editing related code.
3. If the Holistic daemon is installed, treat passive session capture as already active.
4. Use the repo-local Holistic helper when you need an explicit recap or recovery flow.
5. Recap the current state for the user in the first 30 seconds.
6. Ask: continue as planned, tweak the plan, or start something new.

### Startup Notes For Gemini

- Open with the shared Holistic recap, then align Gemini-specific behavior from `GEMINI.md`.

Use the repo-local Holistic helper in this repo: Windows `.\.holistic\system\holistic.cmd resume --agent gemini`; macOS/Linux `./.holistic/system/holistic resume --agent gemini`.

## Checkpoint Contract

Use the repo-local Holistic helper for checkpoints in this repo when:

- the task focus changes
- you are about to compact or clear context
- you finish a meaningful chunk of work
- you fix or alter behavior that could regress later

Include impact notes and regression risks when they matter.

### Checkpoint Notes For Gemini

- Checkpoint when Gemini is about to pivot from research to edits or from one subsystem to another.

Use the repo-local Holistic helper in this repo: Windows `.\.holistic\system\holistic.cmd checkpoint --reason "<what changed>"`; macOS/Linux `./.holistic/system/holistic checkpoint --reason "<what changed>"`.

## Handoff Contract

- Preferred: map your session-end workflow to the repo-local Holistic helper with `handoff`
- Fallback: ask the user to run the repo-local Holistic helper with `handoff` before leaving the session

### Handoff Notes For Gemini

- Use the handoff to leave a crisp resume point for the next non-Gemini agent too, not just Gemini.

Use the repo-local Holistic helper in this repo: Windows `.\.holistic\system\holistic.cmd handoff`; macOS/Linux `./.holistic/system/holistic handoff`.

## Before ending this session

Run:
```
holistic handoff --summary "..." --next "..."
```
This keeps repo memory current for the next agent.
