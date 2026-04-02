#!/bin/sh
# HOLISTIC-MANAGED auto-checkpoint debounce script
STATE_FILE="$PWD/.holistic/state.json"
HOLISTIC_CMD="$PWD/.holistic/system/holistic"
THRESHOLD=900  # 15 minutes in seconds

if [ ! -f "$STATE_FILE" ]; then exit 0; fi

LAST=$(node -e "try{const s=JSON.parse(require('fs').readFileSync('$STATE_FILE','utf8'));process.stdout.write(s.lastAutoCheckpoint||'')}catch(e){}")
if [ -z "$LAST" ]; then
  "$HOLISTIC_CMD" checkpoint --reason "auto periodic snapshot" 2>/dev/null || true
  exit 0
fi

NOW=$(date +%s)
LAST_S=$(node -e "process.stdout.write(String(Math.floor(new Date('$LAST').getTime()/1000)))")
DIFF=$((NOW - LAST_S))
if [ "$DIFF" -ge "$THRESHOLD" ]; then
  "$HOLISTIC_CMD" checkpoint --reason "auto periodic snapshot" 2>/dev/null || true
fi
