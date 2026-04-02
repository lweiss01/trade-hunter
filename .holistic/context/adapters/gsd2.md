# GSD2 Adapter

## Product North Star

Open repo, start working, Holistic quietly keeps continuity alive.

Use this adapter to move toward that outcome: less manual setup, less re-briefing, and more continuity preserved by default.

## Tool-Specific Notes

- GSD2 should be treated as a distinct workflow surface, not an alias of GSD.
- Use Holistic as the shared continuity layer across GSD2 sessions and across non-GSD2 agents touching the same repo.

## Startup Contract

1. Read `HOLISTIC.md`.
2. Review `project-history.md`, `regression-watch.md`, and `zero-touch.md` for durable memory before editing related code.
3. If the Holistic daemon is installed, treat passive session capture as already active.
4. Use the repo-local Holistic helper when you need an explicit recap or recovery flow.
5. Recap the current state for the user in the first 30 seconds.
6. Ask: continue as planned, tweak the plan, or start something new.

### Startup Notes For GSD2

- Load Holistic context first, then reconcile it with any GSD2-native state or workflow entrypoint.

Use the repo-local Holistic helper in this repo: Windows `.\.holistic\system\holistic.cmd resume --agent gsd2`; macOS/Linux `./.holistic/system/holistic resume --agent gsd2`.

## Checkpoint Contract

Use the repo-local Holistic helper for checkpoints in this repo when:

- the task focus changes
- you are about to compact or clear context
- you finish a meaningful chunk of work
- you fix or alter behavior that could regress later

Include impact notes and regression risks when they matter.

### Checkpoint Notes For GSD2

- Checkpoint when GSD2 changes execution mode, task boundary, or planned next step.

Use the repo-local Holistic helper in this repo: Windows `.\.holistic\system\holistic.cmd checkpoint --reason "<what changed>"`; macOS/Linux `./.holistic/system/holistic checkpoint --reason "<what changed>"`.

## Handoff Contract

- Preferred: map your session-end workflow to the repo-local Holistic helper with `handoff`
- Fallback: ask the user to run the repo-local Holistic helper with `handoff` before leaving the session

### Handoff Notes For GSD2

- Write handoffs for the next agent, not just for the next GSD2 runtime instance.

Use the repo-local Holistic helper in this repo: Windows `.\.holistic\system\holistic.cmd handoff`; macOS/Linux `./.holistic/system/holistic handoff`.

## Before ending this session

Run:
```
holistic handoff --summary "..." --next "..."
```
This keeps repo memory current for the next agent.
