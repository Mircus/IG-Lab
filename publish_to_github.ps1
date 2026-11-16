# Safe, non-forcing PowerShell upload of an extracted IG-Lab repository.
# Requires Git and a PRE-EXISTING empty/compatible GitHub repo at Mircus/IG-Lab.
$ErrorActionPreference = 'Stop'
$expected = 'https://github.com/Mircus/IG-Lab.git'
if (-not (Get-Command git -ErrorAction SilentlyContinue)) { throw 'Git is not installed or not on PATH.' }
if (-not (Test-Path 'pyproject.toml') -or -not (Test-Path 'src/iglab')) { throw 'Run inside the EXTRACTED IG-Lab folder, not next to the ZIP.' }
if (-not (Test-Path '.git')) { git init; if ($LASTEXITCODE -ne 0) { throw 'git init failed' } }
git branch -M main
$origin = (git remote get-url origin 2>$null)
if ($LASTEXITCODE -ne 0) { git remote add origin $expected }
elseif ($origin -ne $expected -and $origin -ne 'git@github.com:Mircus/IG-Lab.git') { throw "Existing origin is '$origin', not the expected IG-Lab. No changes made to origin." }
git add .
if ($LASTEXITCODE -ne 0) { throw 'git add failed' }
$pending = git status --porcelain
if ($pending) {
  git commit -m 'Initial IG-Lab research release: Fisher geometry, Chentsov proof, tests'
  if ($LASTEXITCODE -ne 0) { throw 'git commit failed (check user.name and user.email)' }
}
git push -u origin main
if ($LASTEXITCODE -ne 0) { throw 'Push failed. The existing remote was not modified; no force-push attempted.' }
Write-Host 'IG-Lab pushed to GitHub main.'
