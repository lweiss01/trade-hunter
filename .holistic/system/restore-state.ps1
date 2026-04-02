$ErrorActionPreference = 'Stop'
if (Get-Variable PSNativeCommandUseErrorActionPreference -ErrorAction SilentlyContinue) { $PSNativeCommandUseErrorActionPreference = $false }
$root = 'D:\Projects\active\trade-hunter'
$remote = 'origin'
$stateRef = 'refs/holistic/state'
$legacySeedRef = 'refs/heads/holistic/state'
$tracked = @('HOLISTIC.md', 'AGENTS.md', 'HISTORY.md', 'CLAUDE.md', 'GEMINI.md', '.cursorrules', '.windsurfrules', '.github/copilot-instructions.md', '.holistic')
$status = git -C $root status --porcelain -- $tracked 2>$null
if ($LASTEXITCODE -ne 0) { exit 0 }
if ($status) { Write-Host 'Holistic restore skipped because local Holistic files are dirty.'; exit 0 }
$restored = $false
try {
  git -C $root fetch --quiet $remote $stateRef *> $null
  if ($LASTEXITCODE -eq 0) {
    git -C $root checkout FETCH_HEAD -- $tracked 2>$null | Out-Null
    $restored = $true
  }
} catch {
  $restored = $false
}
if (-not $restored -and $legacySeedRef) {
  try {
    git -C $root fetch --quiet $remote $legacySeedRef *> $null
    if ($LASTEXITCODE -eq 0) {
      git -C $root checkout FETCH_HEAD -- $tracked 2>$null | Out-Null
      $restored = $true
    }
  } catch {
    $restored = $false
  }
}
if (-not $restored) { Write-Host 'Holistic restore skipped because remote portable state is unavailable.'; exit 0 }
