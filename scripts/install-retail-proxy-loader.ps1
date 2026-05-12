param(
    [string]$D2RPath = "E:\Diablo II Resurrected",
    [switch]$Force
)

$ErrorActionPreference = "Stop"

$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$BuildRoot = Join-Path $RepoRoot "retail-dll-experiment\build\x64\Release"
$ProxySource = Join-Path $BuildRoot "winmm.dll"
$ProxyTarget = Join-Path $D2RPath "winmm.dll"

if (-not (Test-Path -LiteralPath (Join-Path $D2RPath "D2R.exe"))) {
    throw "D2R.exe not found in: $D2RPath"
}

& (Join-Path $PSScriptRoot "build-retail-hook.ps1")

if (-not (Test-Path -LiteralPath $ProxySource)) {
    throw "Built proxy DLL not found: $ProxySource"
}

if ((Test-Path -LiteralPath $ProxyTarget) -and -not $Force) {
    throw "Refusing to overwrite existing winmm.dll without -Force: $ProxyTarget"
}

Copy-Item -LiteralPath $ProxySource -Destination $ProxyTarget -Force

Write-Host "Installed retail startup proxy:"
Write-Host "  $ProxyTarget"
Write-Host "Proxy log path after next D2R launch:"
Write-Host "  $(Join-Path $D2RPath 'xav-retail-proxy.log')"
