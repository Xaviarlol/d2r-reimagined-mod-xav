param(
    [string]$D2RPath = "C:\Program Files (x86)\Diablo II Resurrected",
    [string]$ModName = "XavReimagined"
)

$ErrorActionPreference = "Stop"

$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$SourceData = Join-Path $RepoRoot "data"
$SourceModInfo = Join-Path $RepoRoot "modinfo.json"

if (-not (Test-Path -LiteralPath $SourceData)) {
    throw "Source data directory not found: $SourceData"
}

if (-not (Test-Path -LiteralPath $SourceModInfo)) {
    throw "modinfo.json not found: $SourceModInfo"
}

if (-not (Test-Path -LiteralPath $D2RPath)) {
    throw "D2R install path not found: $D2RPath"
}

$ModsRoot = Join-Path $D2RPath "mods"
$ModRoot = Join-Path $ModsRoot $ModName
$MpqRoot = Join-Path $ModRoot "$ModName.mpq"
$DestData = Join-Path $MpqRoot "data"

$ResolvedD2R = (Resolve-Path -LiteralPath $D2RPath).Path
$ExpectedPrefix = Join-Path $ResolvedD2R "mods\$ModName\$ModName.mpq"
$TargetFullPath = [System.IO.Path]::GetFullPath($DestData)

if (-not $TargetFullPath.StartsWith([System.IO.Path]::GetFullPath($ExpectedPrefix), [System.StringComparison]::OrdinalIgnoreCase)) {
    throw "Refusing to copy outside the expected mod folder: $TargetFullPath"
}

New-Item -ItemType Directory -Force -Path $MpqRoot | Out-Null

Write-Host "Installing $ModName to:"
Write-Host "  $MpqRoot"

robocopy $SourceData $DestData /MIR /E /IS /IT
$RoboCopyExitCode = $LASTEXITCODE

if ($RoboCopyExitCode -ge 8) {
    throw "robocopy failed with exit code $RoboCopyExitCode"
}

Copy-Item -LiteralPath $SourceModInfo -Destination (Join-Path $MpqRoot "modinfo.json") -Force

Write-Host ""
Write-Host "Done."
Write-Host "Launch arguments:"
Write-Host "  -mod $ModName -txt"
