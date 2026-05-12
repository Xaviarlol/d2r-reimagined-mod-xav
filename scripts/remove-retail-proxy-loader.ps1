param(
    [string]$D2RPath = "E:\Diablo II Resurrected"
)

$ErrorActionPreference = "Stop"

$ProxyTarget = Join-Path $D2RPath "winmm.dll"
$ProxyLog = Join-Path $D2RPath "xav-retail-proxy.log"

Remove-Item -LiteralPath $ProxyTarget -Force -ErrorAction SilentlyContinue
Remove-Item -LiteralPath $ProxyLog -Force -ErrorAction SilentlyContinue

Write-Host "Removed retail startup proxy files from:"
Write-Host "  $D2RPath"
