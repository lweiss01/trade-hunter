#!/usr/bin/env sh
ROOT='D:\Projects\active\trade-hunter'
REMOTE='origin'
STATE_REF='refs/holistic/state'
LEGACY_SEED_REF='refs/heads/holistic/state'
LOG_FILE="$(dirname "$0")/sync.log"
log_msg() { echo "$(date '+%Y-%m-%d %H:%M:%S') [RESTORE] $1" >> "$LOG_FILE"; }
if ! git -C "$ROOT" diff --quiet -- "HOLISTIC.md" "AGENTS.md" "HISTORY.md" "CLAUDE.md" "GEMINI.md" ".cursorrules" ".windsurfrules" ".github/copilot-instructions.md" ".holistic" 2>/dev/null; then
  echo 'Holistic restore skipped because local Holistic files are dirty.'
  exit 0
fi
RESTORED=false
if git -C "$ROOT" fetch "$REMOTE" "$STATE_REF" >> "$LOG_FILE" 2>&1; then
  if git -C "$ROOT" checkout FETCH_HEAD -- ${shellPathList(trackedPaths)} >> "$LOG_FILE" 2>&1; then
    RESTORED=true
    log_msg "Successfully restored state from $STATE_REF"
  fi
fi
if [ "$RESTORED" != "true" ] && [ -n "$LEGACY_SEED_REF" ]; then
  if git -C "$ROOT" fetch "$REMOTE" "$LEGACY_SEED_REF" >/dev/null 2>&1; then
    git -C "$ROOT" checkout FETCH_HEAD -- "HOLISTIC.md" "AGENTS.md" "HISTORY.md" "CLAUDE.md" "GEMINI.md" ".cursorrules" ".windsurfrules" ".github/copilot-instructions.md" ".holistic" >/dev/null 2>&1 || true
    RESTORED=true
  fi
fi
if [ "$RESTORED" != "true" ]; then
  echo 'Holistic restore skipped because remote portable state is unavailable.'
  exit 0
fi
