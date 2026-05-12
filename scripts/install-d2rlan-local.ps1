param(
    [Parameter(Mandatory = $true)]
    [string]$D2RLANPath,
    [string]$ModName = "XavReimaginedLAN",
    [switch]$AllowMissingD2RExe
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

if (-not (Test-Path -LiteralPath $D2RLANPath)) {
    throw "D2RLAN path not found: $D2RLANPath"
}

$ResolvedInput = (Resolve-Path -LiteralPath $D2RLANPath).Path
$CandidateD2R = Join-Path $ResolvedInput "D2R"
$CandidateLauncher = Join-Path $ResolvedInput "Launcher\D2RLAN.exe"

if (Test-Path -LiteralPath (Join-Path $ResolvedInput "D2R.exe")) {
    $D2RPath = $ResolvedInput
}
elseif (Test-Path -LiteralPath (Join-Path $CandidateD2R "D2R.exe")) {
    $D2RPath = (Resolve-Path -LiteralPath $CandidateD2R).Path
}
elseif ($AllowMissingD2RExe -and (Test-Path -LiteralPath $CandidateLauncher)) {
    $D2RPath = $CandidateD2R
    New-Item -ItemType Directory -Force -Path $D2RPath | Out-Null
}
elseif ($AllowMissingD2RExe -and ((Split-Path -Leaf $ResolvedInput) -ieq "D2R")) {
    $D2RPath = $ResolvedInput
    New-Item -ItemType Directory -Force -Path $D2RPath | Out-Null
}
else {
    throw "Could not find D2R.exe. Pass either the D2RLAN root folder or its nested D2R folder, or use -AllowMissingD2RExe to stage files before installing Base TCP files."
}

$ModsRoot = Join-Path $D2RPath "Mods"
$ModRoot = Join-Path $ModsRoot $ModName
$MpqRoot = Join-Path $ModRoot "$ModName.mpq"
$DestData = Join-Path $MpqRoot "data"

$ExpectedPrefix = Join-Path $D2RPath "Mods\$ModName\$ModName.mpq"
$TargetFullPath = [System.IO.Path]::GetFullPath($DestData)

if (-not $TargetFullPath.StartsWith([System.IO.Path]::GetFullPath($ExpectedPrefix), [System.StringComparison]::OrdinalIgnoreCase)) {
    throw "Refusing to copy outside the expected D2RLAN mod folder: $TargetFullPath"
}

New-Item -ItemType Directory -Force -Path $MpqRoot | Out-Null

Write-Host "Installing $ModName to D2RLAN:"
Write-Host "  $MpqRoot"

robocopy $SourceData $DestData /MIR /E /IS /IT
$RoboCopyExitCode = $LASTEXITCODE

if ($RoboCopyExitCode -ge 8) {
    throw "robocopy failed with exit code $RoboCopyExitCode"
}

Copy-Item -LiteralPath $SourceModInfo -Destination (Join-Path $MpqRoot "modinfo.json") -Force

Write-Host ""
Write-Host "Done."
Write-Host "D2RLAN should launch this side mod as:"
Write-Host "  -mod $ModName -txt"
