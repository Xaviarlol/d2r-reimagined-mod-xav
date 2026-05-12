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

function Set-D2RLANSetting {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Path,
        [Parameter(Mandatory = $true)]
        [string]$Name,
        [Parameter(Mandatory = $true)]
        [string]$Value
    )

    [xml]$Config = Get-Content -Raw -LiteralPath $Path
    $Settings = $Config.SelectSingleNode("/configuration/userSettings/D2RLAN.Properties.Settings")

    if (-not $Settings) {
        throw "D2RLAN settings section not found: $Path"
    }

    $Setting = $Config.SelectSingleNode("/configuration/userSettings/D2RLAN.Properties.Settings/setting[@name='$Name']")

    if (-not $Setting) {
        $Setting = $Config.CreateElement("setting")
        $Setting.SetAttribute("name", $Name)
        $Setting.SetAttribute("serializeAs", "String")
        $ValueNode = $Config.CreateElement("value")
        [void]$Setting.AppendChild($ValueNode)
        [void]$Settings.AppendChild($Setting)
    }

    @($Setting.SelectNodes("value")) | ForEach-Object {
        [void]$Setting.RemoveChild($_)
    }

    $ValueElement = $Config.CreateElement("value")
    $ValueElement.InnerText = $Value
    [void]$Setting.AppendChild($ValueElement)
    $Config.Save($Path)
}

function Get-D2RLANSetting {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Path,
        [Parameter(Mandatory = $true)]
        [string]$Name
    )

    [xml]$Config = Get-Content -Raw -LiteralPath $Path
    $ValueElement = $Config.SelectSingleNode("/configuration/userSettings/D2RLAN.Properties.Settings/setting[@name='$Name']/value")

    if ($ValueElement) {
        return $ValueElement.InnerText
    }

    return $null
}

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

$LauncherConfig = Join-Path (Split-Path -Parent $D2RPath) "Launcher\D2RLAN.dll.config"

if (Test-Path -LiteralPath $LauncherConfig) {
    $InstallPathSetting = $D2RPath

    if (-not $InstallPathSetting.EndsWith([System.IO.Path]::DirectorySeparatorChar)) {
        $InstallPathSetting += [System.IO.Path]::DirectorySeparatorChar
    }

    Set-D2RLANSetting -Path $LauncherConfig -Name "SelectedMod" -Value $ModName
    Set-D2RLANSetting -Path $LauncherConfig -Name "InstallPath" -Value $InstallPathSetting
    Write-Host "Updated launcher defaults:"
    Write-Host "  SelectedMod = $ModName"

    $UserConfigRoot = Join-Path $env:LOCALAPPDATA "D2RLAN"

    if (Test-Path -LiteralPath $UserConfigRoot) {
        Get-ChildItem -Path $UserConfigRoot -Recurse -Filter "user.config" -ErrorAction SilentlyContinue | ForEach-Object {
            try {
                $SavedInstallPath = Get-D2RLANSetting -Path $_.FullName -Name "InstallPath"

                if ($SavedInstallPath -eq $InstallPathSetting) {
                    Set-D2RLANSetting -Path $_.FullName -Name "SelectedMod" -Value $ModName
                    Write-Host "Updated saved launcher selection:"
                    Write-Host "  $($_.FullName)"
                }
            }
            catch {
                Write-Warning "Could not update saved launcher settings: $($_.FullName)"
            }
        }
    }
}

Write-Host ""
Write-Host "Done."
Write-Host "D2RLAN should launch this side mod as:"
Write-Host "  -mod $ModName -txt"
