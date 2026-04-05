$ErrorActionPreference = 'Stop'
$node = 'C:\Program Files\nodejs\node.exe'
$daemon = 'D:\Projects\active\holistic\src\daemon.ts'
$working = 'D:\Projects\active\trade-hunter'
& 'D:\Projects\active\trade-hunter\.holistic\system\restore-state.ps1'
& $node --experimental-strip-types $daemon --interval 30 --agent unknown
