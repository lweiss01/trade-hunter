#!/usr/bin/env sh
cd 'D:\Projects\active\trade-hunter' || exit 1
'D:\Projects\active\trade-hunter\.holistic\system\restore-state.sh' || true
'C:\Program Files\nodejs\node.exe' --experimental-strip-types 'D:\Projects\active\holistic\src\daemon.ts' --interval 30 --agent unknown
