param(
    [string]$D2RPath = "E:\Diablo II Resurrected",
    [string]$ModName = "XavReimaginedExperimental",
    [switch]$Inject,
    [int]$InjectDelaySeconds = 8
)

$ErrorActionPreference = "Stop"

$D2RExe = Join-Path $D2RPath "D2R.exe"
if (-not (Test-Path -LiteralPath $D2RExe)) {
    throw "D2R.exe not found: $D2RExe"
}

$ModRoot = Join-Path $D2RPath "mods\$ModName"
$MpqRoot = Join-Path $ModRoot "$ModName.mpq"
if (-not (Test-Path -LiteralPath $MpqRoot)) {
    throw "Experimental mod is not installed yet: $MpqRoot"
}

$Existing = Get-Process -Name "D2R" -ErrorAction SilentlyContinue
if ($Existing) {
    throw "D2R is already running. Close it before launching the experimental copy."
}

$Arguments = "-mod $ModName -txt"
Write-Host "Launching:"
Write-Host "  $D2RExe $Arguments"

$Process = Start-Process -FilePath $D2RExe -ArgumentList $Arguments -WorkingDirectory $D2RPath -PassThru

if ($Inject) {
    Start-Sleep -Seconds $InjectDelaySeconds

    $ToolsRoot = Join-Path $ModRoot "tools"
    $Injector = Join-Path $ToolsRoot "xav-retail-injector.exe"
    $Hook = Join-Path $ToolsRoot "xav-retail-hook.dll"

    if (-not (Test-Path -LiteralPath $Injector)) {
        throw "Injector not found: $Injector"
    }
    if (-not (Test-Path -LiteralPath $Hook)) {
        throw "Hook DLL not found: $Hook"
    }

    & $Injector $Process.Id $Hook
    if ($LASTEXITCODE -ne 0) {
        throw "Injector failed with exit code $LASTEXITCODE"
    }

    Write-Host "Hook log:"
    Write-Host "  $(Join-Path $ToolsRoot 'xav-retail-hook.log')"
}
