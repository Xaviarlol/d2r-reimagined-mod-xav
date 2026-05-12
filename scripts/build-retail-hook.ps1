param(
    [string]$Configuration = "Release"
)

$ErrorActionPreference = "Stop"

$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$SourceRoot = Join-Path $RepoRoot "retail-dll-experiment\src"
$BuildRoot = Join-Path $RepoRoot "retail-dll-experiment\build\x64\$Configuration"
$VsWhere = Join-Path ${env:ProgramFiles(x86)} "Microsoft Visual Studio\Installer\vswhere.exe"

if (-not (Test-Path -LiteralPath $VsWhere)) {
    throw "vswhere.exe not found. Install Visual Studio Build Tools with C++ support."
}

$VsInstall = & $VsWhere -latest -products * -requires Microsoft.VisualStudio.Component.VC.Tools.x86.x64 -property installationPath
if (-not $VsInstall) {
    throw "Visual Studio C++ Build Tools were not found."
}

$VsDevCmd = Join-Path $VsInstall "Common7\Tools\VsDevCmd.bat"
if (-not (Test-Path -LiteralPath $VsDevCmd)) {
    throw "VsDevCmd.bat not found: $VsDevCmd"
}

New-Item -ItemType Directory -Force -Path $BuildRoot | Out-Null

$HookSource = Join-Path $SourceRoot "xav_hook.cpp"
$InjectorSource = Join-Path $SourceRoot "xav_injector.cpp"
$HookDll = Join-Path $BuildRoot "xav-retail-hook.dll"
$InjectorExe = Join-Path $BuildRoot "xav-retail-injector.exe"
$BuildCmd = Join-Path $BuildRoot "build.cmd"

$CmdText = @"
@echo off
call "$VsDevCmd" -arch=x64 -host_arch=x64 -no_logo
if errorlevel 1 exit /b %errorlevel%
cl /nologo /std:c++17 /EHsc /O2 /LD "$HookSource" /Fe:"$HookDll" /Fo:"$BuildRoot\\" /link version.lib
if errorlevel 1 exit /b %errorlevel%
cl /nologo /std:c++17 /EHsc /O2 "$InjectorSource" /Fe:"$InjectorExe" /Fo:"$BuildRoot\\"
if errorlevel 1 exit /b %errorlevel%
"@

Set-Content -LiteralPath $BuildCmd -Value $CmdText -Encoding ASCII

& $env:ComSpec /d /c "`"$BuildCmd`""
if ($LASTEXITCODE -ne 0) {
    throw "Retail hook build failed with exit code $LASTEXITCODE"
}

Write-Host "Built:"
Write-Host "  $HookDll"
Write-Host "  $InjectorExe"
