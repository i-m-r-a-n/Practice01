# Downloads the STAGE II presentation package (130 files, 453 MB) into .\STAGE_II_Presentation and checks every SHA-256.
# Windows PowerShell:  cd <folder with this script and manifest.csv>;  powershell -ExecutionPolicy Bypass -File .\get_package_windows.ps1
$ErrorActionPreference = 'Continue'
Set-Location $PSScriptRoot
$out = Join-Path $PSScriptRoot 'STAGE_II_Presentation'
$bad = 0
foreach ($r in Import-Csv manifest.csv) {
  $f = Join-Path $out ($r.target -replace '/', '\')
  New-Item -ItemType Directory -Force -Path (Split-Path $f) | Out-Null
  if ((Test-Path $f) -and ((Get-FileHash $f -Algorithm SHA256).Hash.ToLower() -eq $r.sha256)) { continue }
  for ($t = 1; $t -le 3; $t++) {
    try { Invoke-WebRequest -Uri $r.url -OutFile $f -UseBasicParsing; break } catch { Start-Sleep -Seconds (2 * $t) }
  }
  if ((Test-Path $f) -and ((Get-FileHash $f -Algorithm SHA256).Hash.ToLower() -eq $r.sha256)) { "ok  $($r.target)" } else { "BAD $($r.target)"; $bad++ }
}
"Done: $bad bad file(s). If any, run the script again."
