# Holistic System Setup

This directory contains generated startup and sync helpers for Holistic.

Files:
- holistic / holistic.cmd: repo-local CLI fallback when `holistic` is not on PATH
- run-daemon.ps1 / run-daemon.sh: restore the portable state, then start the background daemon
- restore-state.ps1 / restore-state.sh: pull the portable Holistic state ref into the current worktree when safe
- sync-state.ps1 / sync-state.sh: mirror Holistic files into the portable state ref without pushing the working branch
- config in ../config.json defines the remote and portable state target

If the global `holistic` command is unavailable in this shell:
- Windows: `.\.holistic\system\holistic.cmd`
- macOS/Linux: `./.holistic/system/holistic`
