# HOLISTIC-MANAGED auto-checkpoint debounce script
$stateFile = Join-Path $PWD ".holistic\state.json"
$holisticCmd = Join-Path $PWD ".holistic\system\holistic.cmd"
$threshold = 900

if (-not (Test-Path $stateFile)) { exit 0 }

$state = Get-Content $stateFile -Raw | ConvertFrom-Json -ErrorAction SilentlyContinue
$last = $state.lastAutoCheckpoint
if (-not $last) {
    & $holisticCmd checkpoint --reason "auto periodic snapshot" 2>$null
    exit 0
}

$now = [DateTimeOffset]::UtcNow.ToUnixTimeSeconds()
$lastS = [DateTimeOffset]::Parse($last).ToUnixTimeSeconds()
$diff = $now - $lastS
if ($diff -ge $threshold) {
    & $holisticCmd checkpoint --reason "auto periodic snapshot" 2>$null
}
