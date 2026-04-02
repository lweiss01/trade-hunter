$ErrorActionPreference = 'Stop'
if (Get-Variable PSNativeCommandUseErrorActionPreference -ErrorAction SilentlyContinue) { $PSNativeCommandUseErrorActionPreference = $false }
$root = 'D:\Projects\active\trade-hunter'
$remote = 'origin'
$stateRef = 'refs/holistic/state'
$legacySeedRef = 'refs/heads/holistic/state'
if (-not $remote) { Write-Error 'holistic sync-state: ERROR: no remote configured. Re-run holistic init --remote <remote>.'; exit 1 }
$tmp = Join-Path $env:TEMP ('holistic-state-' + [guid]::NewGuid().ToString())
git -c core.hooksPath=NUL -C $root worktree add --force $tmp | Out-Null
try {
  Push-Location $tmp
  $remoteStateExists = $false
  $remoteLegacyExists = $false
  try {
    git -c core.hooksPath=NUL ls-remote --quiet --exit-code $remote $stateRef *> $null
    $remoteStateExists = ($LASTEXITCODE -eq 0)
  } catch {
    $remoteStateExists = $false
  }
  if (-not $remoteStateExists -and $legacySeedRef) {
    try {
      git -c core.hooksPath=NUL ls-remote --quiet --exit-code $remote $legacySeedRef *> $null
      $remoteLegacyExists = ($LASTEXITCODE -eq 0)
    } catch {
      $remoteLegacyExists = $false
    }
  }
  if ($remoteStateExists) {
    git -c core.hooksPath=NUL fetch --quiet $remote $stateRef *> $null
    git -c core.hooksPath=NUL switch --detach FETCH_HEAD | Out-Null
  } elseif ($remoteLegacyExists) {
    git -c core.hooksPath=NUL fetch --quiet $remote $legacySeedRef *> $null
    git -c core.hooksPath=NUL switch --detach FETCH_HEAD | Out-Null
  } else {
    git -c core.hooksPath=NUL switch --orphan holistic-sync-tmp | Out-Null
  }
  Get-ChildItem -Force | Where-Object { $_.Name -ne '.git' } | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
  Copy-Item -Path (Join-Path $root 'HOLISTIC.md') -Destination (Join-Path $tmp 'HOLISTIC.md') -Force
  Copy-Item -Path (Join-Path $root 'AGENTS.md') -Destination (Join-Path $tmp 'AGENTS.md') -Force
  Copy-Item -Path (Join-Path $root 'HISTORY.md') -Destination (Join-Path $tmp 'HISTORY.md') -Force
  Copy-Item -Path (Join-Path $root 'CLAUDE.md') -Destination (Join-Path $tmp 'CLAUDE.md') -Force
  Copy-Item -Path (Join-Path $root 'GEMINI.md') -Destination (Join-Path $tmp 'GEMINI.md') -Force
  Copy-Item -Path (Join-Path $root '.cursorrules') -Destination (Join-Path $tmp '.cursorrules') -Recurse -Force
  Copy-Item -Path (Join-Path $root '.windsurfrules') -Destination (Join-Path $tmp '.windsurfrules') -Recurse -Force
  New-Item -ItemType Directory -Path (Join-Path $tmp '.github') -Force | Out-Null
  Copy-Item -Path (Join-Path $root '.github\copilot-instructions.md') -Destination (Join-Path $tmp '.github\copilot-instructions.md') -Force
  Copy-Item -Path (Join-Path $root '.holistic') -Destination (Join-Path $tmp '.holistic') -Recurse -Force
  git -c core.hooksPath=NUL add 'HOLISTIC.md' 'AGENTS.md' 'HISTORY.md' 'CLAUDE.md' 'GEMINI.md' '.cursorrules' '.windsurfrules' '.github/copilot-instructions.md' '.holistic'
  git -c core.hooksPath=NUL diff --cached --quiet
  if ($LASTEXITCODE -ne 0) {
    git -c core.hooksPath=NUL commit -m 'chore(holistic): sync portable state' | Out-Null
  }
  git -c core.hooksPath=NUL push $remote HEAD:$stateRef
} finally {
  Pop-Location
  git -c core.hooksPath=NUL -C $root worktree remove --force $tmp | Out-Null
}
