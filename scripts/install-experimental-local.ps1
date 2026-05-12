param(
    [string]$D2RPath = "E:\Diablo II Resurrected",
    [string]$ModName = "XavReimaginedExperimental",
    [string]$Version = "3.0.9-xav.retail-experiment.1",
    [switch]$SkipTools
)

$ErrorActionPreference = "Stop"

$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$SourceData = Join-Path $RepoRoot "data"

if (-not (Test-Path -LiteralPath $SourceData)) {
    throw "Source data directory not found: $SourceData"
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

$ModInfo = [ordered]@{
    name = $ModName
    version = $Version
    savepath = "$ModName/"
}

$ModInfo | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $MpqRoot "modinfo.json") -Encoding UTF8

if (-not $SkipTools) {
    & (Join-Path $PSScriptRoot "build-retail-hook.ps1")

    $BuildRoot = Join-Path $RepoRoot "retail-dll-experiment\build\x64\Release"
    $ToolsRoot = Join-Path $ModRoot "tools"
    New-Item -ItemType Directory -Force -Path $ToolsRoot | Out-Null

    Copy-Item -LiteralPath (Join-Path $BuildRoot "xav-retail-hook.dll") -Destination $ToolsRoot -Force
    Copy-Item -LiteralPath (Join-Path $BuildRoot "xav-retail-injector.exe") -Destination $ToolsRoot -Force

    Write-Host "Installed experimental tools to:"
    Write-Host "  $ToolsRoot"
}

Write-Host ""
Write-Host "Done."
Write-Host "Launch arguments:"
Write-Host "  -mod $ModName -txt"
