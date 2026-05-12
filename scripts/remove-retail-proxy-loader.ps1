param(
    [string]$D2RPath = "E:\Diablo II Resurrected"
)

$ErrorActionPreference = "Stop"

$ProxyTarget = Join-Path $D2RPath "winmm.dll"
$ProxyLog = Join-Path $D2RPath "xav-retail-proxy.log"

if (Test-Path -LiteralPath $ProxyTarget) {
    Remove-Item -LiteralPath $ProxyTarget -Force -ErrorAction Stop
}

if (Test-Path -LiteralPath $ProxyLog) {
    Remove-Item -LiteralPath $ProxyLog -Force -ErrorAction Stop
}

if (Test-Path -LiteralPath $ProxyTarget) {
    throw "Retail startup proxy still exists after removal attempt: $ProxyTarget"
}

Write-Host "Removed retail startup proxy files from:"
Write-Host "  $D2RPath"
