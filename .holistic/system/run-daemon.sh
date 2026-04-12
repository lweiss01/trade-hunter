#!/usr/bin/env sh
cd 'D:\Projects\active\trade-hunter' || exit 1
'D:\Projects\active\trade-hunter\.holistic\system\restore-state.sh' || true
'C:\Program Files\nodejs\node.exe' 'C:\Users\lweis\AppData\Roaming\npm\node_modules\holistic\dist\daemon.js' --interval 30 --agent unknown
