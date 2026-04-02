# Session Protocol

## Product North Star

Open repo, start working, Holistic quietly keeps continuity alive.

The protocol below is the current operating model, not the final ideal. When improving Holistic, prefer changes that make more of this protocol happen automatically without weakening durable continuity.

## Startup

1. Read `HOLISTIC.md`.
2. Review `project-history.md`, `regression-watch.md`, and `zero-touch.md` for durable project memory and automation expectations.
3. If the Holistic daemon is installed, let it capture repo activity in the background.
4. Use the repo-local Holistic helper for explicit recap or recovery flows in this repo.
5. Recap the work state to the user.
6. Ask whether to continue as planned, tweak the plan, or start something new.

Use the repo-local Holistic helper in this repo: Windows `.\.holistic\system\holistic.cmd resume --agent <app>`; macOS/Linux `./.holistic/system/holistic resume --agent <app>`.

## During The Session

Use the repo-local Holistic helper for checkpoints in this repo:

- when the task focus changes
- before likely context compaction
- after meaningful progress
- when you fix something another agent might accidentally re-break later

Use the repo-local Holistic helper with `watch` if you want foreground background checkpoints while working manually.

Use the repo-local Holistic helper in this repo: Windows `.\.holistic\system\holistic.cmd checkpoint --reason "<what changed>"`; macOS/Linux `./.holistic/system/holistic checkpoint --reason "<what changed>"`.

## Handoff

1. Use the repo-local Holistic helper to run `handoff`.
2. Confirm or edit the drafted summary.
3. Make sure the next step, impact, and regression risks are accurate.
4. Let Holistic write the docs and prepare the handoff commit.
5. If you want the handoff docs committed, make that git commit explicitly.
6. Holistic sync helpers should mirror portable state to the dedicated portable state ref without pushing your working branch.
7. If you continue on another device, pull or restore the latest portable state before starting work.

Use the repo-local Holistic helper in this repo: Windows `.\.holistic\system\holistic.cmd handoff`; macOS/Linux `./.holistic/system/holistic handoff`.
