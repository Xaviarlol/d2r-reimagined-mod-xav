param(
    [Parameter(Mandatory = $true)]
    [string]$D2RLANPath,
    [string]$ModName = "XavLANProbe",
    [string]$D2CompareBuild = "69270",
    [switch]$KeepD2RHUDInjection
)

$ErrorActionPreference = "Stop"

$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$ProbeRoot = Join-Path $RepoRoot "d2rlan-probe"
$ProbeMemoryOverrides = Join-Path $ProbeRoot "memory_overrides.json"

function Resolve-D2RPath {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Path
    )

    if (-not (Test-Path -LiteralPath $Path)) {
        throw "D2RLAN path not found: $Path"
    }

    $ResolvedInput = (Resolve-Path -LiteralPath $Path).Path
    $CandidateD2R = Join-Path $ResolvedInput "D2R"

    if (Test-Path -LiteralPath (Join-Path $ResolvedInput "D2R.exe")) {
        return $ResolvedInput
    }

    if (Test-Path -LiteralPath (Join-Path $CandidateD2R "D2R.exe")) {
        return (Resolve-Path -LiteralPath $CandidateD2R).Path
    }

    throw "Could not find D2R.exe. Pass either the D2RLAN root folder or its nested D2R folder."
}

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

function Disable-D2RHUDInjection {
    param(
        [Parameter(Mandatory = $true)]
        [string]$LauncherRoot
    )

    $LoaderPath = Join-Path $LauncherRoot "D2RHUD-Loader.exe"
    $BackupPath = Join-Path $LauncherRoot "D2RHUD-Loader.original.exe"
    $TempPath = Join-Path $LauncherRoot "_D2RHUD-Loader.noop.exe"

    if ((Test-Path -LiteralPath $LoaderPath) -and -not (Test-Path -LiteralPath $BackupPath)) {
        Copy-Item -LiteralPath $LoaderPath -Destination $BackupPath -Force
        Write-Host "Backed up original D2RHUD loader:"
        Write-Host "  $BackupPath"
    }

    if (Test-Path -LiteralPath $TempPath) {
        Remove-Item -LiteralPath $TempPath -Force
    }

    $ClassName = "NoopD2RHUDLoader_" + ([Guid]::NewGuid().ToString("N"))
    $Code = @"
public static class $ClassName
{
    public static int Main(string[] args)
    {
        return 0;
    }
}
"@

    Add-Type -TypeDefinition $Code -OutputAssembly $TempPath -OutputType ConsoleApplication
    Move-Item -LiteralPath $TempPath -Destination $LoaderPath -Force
    Write-Host "Disabled D2RHUD injection with a no-op loader."
}

function Write-Tsv {
    param(
        [Parameter(Mandatory = $true)]
        [string]$SourcePath,
        [Parameter(Mandatory = $true)]
        [string]$DestinationPath,
        [scriptblock]$RowMutator
    )

    $Lines = [System.IO.File]::ReadAllLines($SourcePath)

    if ($Lines.Count -eq 0) {
        throw "Source TSV is empty: $SourcePath"
    }

    $Header = $Lines[0].Split([char]9)
    $Column = @{}

    for ($Index = 0; $Index -lt $Header.Count; $Index++) {
        $Column[$Header[$Index]] = $Index
    }

    $Output = [System.Collections.Generic.List[string]]::new()
    $Output.Add($Lines[0])

    for ($LineIndex = 1; $LineIndex -lt $Lines.Count; $LineIndex++) {
        $Cells = $Lines[$LineIndex].Split([char]9)

        if ($Cells.Count -lt $Header.Count) {
            $Expanded = New-Object string[] $Header.Count
            [Array]::Copy($Cells, $Expanded, $Cells.Count)

            for ($CellIndex = $Cells.Count; $CellIndex -lt $Header.Count; $CellIndex++) {
                $Expanded[$CellIndex] = ""
            }

            $Cells = $Expanded
        }

        if ($RowMutator) {
            & $RowMutator $Cells $Column
        }

        $Output.Add(($Cells -join "`t"))
    }

    New-Item -ItemType Directory -Force -Path (Split-Path -Parent $DestinationPath) | Out-Null
    [System.IO.File]::WriteAllLines($DestinationPath, $Output, [System.Text.Encoding]::ASCII)
}

function Copy-D2RTextTable {
    param(
        [Parameter(Mandatory = $true)]
        [string]$SourcePath,
        [Parameter(Mandatory = $true)]
        [string]$DestinationPath
    )

    Write-Tsv -SourcePath $SourcePath -DestinationPath $DestinationPath
}

function Write-ProbeSkillsTable {
    param(
        [Parameter(Mandatory = $true)]
        [string]$SourcePath,
        [Parameter(Mandatory = $true)]
        [string]$DestinationPath
    )

    $ZeroManaSkills = @{}

    @(
        "Tiger Strike",
        "Fists of Fire",
        "Cobra Strike",
        "Claws of Thunder",
        "Blades of Ice",
        "Royal Strike",
        "Dragon Talon",
        "Dragon Claw",
        "Dragon Tail",
        "Dragon Flight",
        "Quickness",
        "Fade",
        "Blade Shield",
        "Venom"
    ) | ForEach-Object { $ZeroManaSkills[$_] = $true }

    $LongBuffs = @{
        "Quickness" = @{ Start = "Param5"; PerLevel = "Param6" }
        "Fade" = @{ Start = "Param5"; PerLevel = "Param6" }
        "Blade Shield" = @{ Start = "Param1"; PerLevel = "Param2" }
        "Venom" = @{ Start = "Param1"; PerLevel = "Param2" }
    }

    $UpdatedSkills = @{}

    Write-Tsv -SourcePath $SourcePath -DestinationPath $DestinationPath -RowMutator {
        param($Cells, $Column)

        $SkillName = $Cells[$Column["skill"]]

        if ($ZeroManaSkills.ContainsKey($SkillName)) {
            $Cells[$Column["mana"]] = "0"
            $Cells[$Column["lvlmana"]] = "0"
            $UpdatedSkills[$SkillName] = $true
        }

        if ($LongBuffs.ContainsKey($SkillName)) {
            $StartColumn = $LongBuffs[$SkillName].Start
            $PerLevelColumn = $LongBuffs[$SkillName].PerLevel
            $Cells[$Column[$StartColumn]] = "45000"
            $Cells[$Column[$PerLevelColumn]] = "0"
        }
    }

    $MissingSkills = @($ZeroManaSkills.Keys | Where-Object { -not $UpdatedSkills.ContainsKey($_) } | Sort-Object)

    if ($MissingSkills.Count -gt 0) {
        throw "Did not find expected skills in $SourcePath`: $($MissingSkills -join ', ')"
    }
}

function Write-ProbeUserSettings {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Path,
        [Parameter(Mandatory = $true)]
        [string]$ModName,
        [string]$TemplatePath
    )

    if ($TemplatePath -and (Test-Path -LiteralPath $TemplatePath)) {
        $Settings = Get-Content -Raw -LiteralPath $TemplatePath | ConvertFrom-Json
    }
    else {
        $Settings = [pscustomobject]@{}
    }

    $Values = [ordered]@{
        InfiniteRespec = $true
        ResetMaps = $false
        AudioLanguage = 0
        TextLanguage = 0
        UiTheme = 1
        AutoBackups = 1
        HdrFix = $true
        DirectTxt = $false
        CurrentD2RArgs = "-mod $ModName -txt -enablerespec"
        Cheats = $false
        CheatsActive = $true
        FilterUpdates = $false
        HUDDebug = $false
        LANOffline = $true
        CloseMinimized = $false
    }

    foreach ($Name in $Values.Keys) {
        $Settings | Add-Member -NotePropertyName $Name -NotePropertyValue $Values[$Name] -Force
    }

    $Settings | ConvertTo-Json -Compress -Depth 20 | Set-Content -LiteralPath $Path -Encoding UTF8
}

if (-not (Test-Path -LiteralPath $ProbeMemoryOverrides)) {
    throw "Probe memory override file not found: $ProbeMemoryOverrides"
}

$D2RPath = Resolve-D2RPath -Path $D2RLANPath
$D2RLANRoot = Split-Path -Parent $D2RPath
$LauncherRoot = Join-Path $D2RLANRoot "Launcher"
$D2CompareTxtRoot = Join-Path $D2RLANRoot "_DocsTools\D2Compare\D2TXTCompare\TXT\$D2CompareBuild"
$TcpMpqRoot = Join-Path $D2RPath "Mods\TCP\TCP.mpq"
$ModRoot = Join-Path $D2RPath "Mods\$ModName"
$MpqRoot = Join-Path $ModRoot "$ModName.mpq"
$DestData = Join-Path $MpqRoot "data"

if (-not (Test-Path -LiteralPath $D2CompareTxtRoot)) {
    throw "D2Compare text table build not found: $D2CompareTxtRoot"
}

if (-not (Test-Path -LiteralPath $TcpMpqRoot)) {
    throw "TCP mod must be installed before building the D2RLAN probe: $TcpMpqRoot"
}

$ExpectedPrefix = Join-Path $D2RPath "Mods\$ModName\$ModName.mpq"
$TargetFullPath = [System.IO.Path]::GetFullPath($MpqRoot)

if (-not $TargetFullPath.StartsWith([System.IO.Path]::GetFullPath($ExpectedPrefix), [System.StringComparison]::OrdinalIgnoreCase)) {
    throw "Refusing to write outside the expected D2RLAN probe folder: $TargetFullPath"
}

if (Test-Path -LiteralPath $MpqRoot) {
    Remove-Item -LiteralPath $MpqRoot -Recurse -Force
}

New-Item -ItemType Directory -Force -Path $MpqRoot | Out-Null

Write-Host "Creating $ModName from the installed TCP mod:"
Write-Host "  $MpqRoot"

robocopy $TcpMpqRoot $MpqRoot /MIR /E /IS /IT
$RoboCopyExitCode = $LASTEXITCODE

if ($RoboCopyExitCode -ge 8) {
    throw "robocopy failed with exit code $RoboCopyExitCode"
}

$ExcelSource = $D2CompareTxtRoot
$ExcelDest = Join-Path $DestData "global\excel"
$BaseExcelDest = Join-Path $ExcelDest "base"

Write-ProbeSkillsTable -SourcePath (Join-Path $ExcelSource "skills.txt") -DestinationPath (Join-Path $ExcelDest "skills.txt")
Write-ProbeSkillsTable -SourcePath (Join-Path $ExcelSource "skills.txt") -DestinationPath (Join-Path $BaseExcelDest "skills.txt")
Copy-D2RTextTable -SourcePath (Join-Path $ExcelSource "charstats.txt") -DestinationPath (Join-Path $ExcelDest "charstats.txt")
Copy-D2RTextTable -SourcePath (Join-Path $ExcelSource "charstats.txt") -DestinationPath (Join-Path $BaseExcelDest "charstats.txt")
Copy-D2RTextTable -SourcePath (Join-Path $ExcelSource "armor.txt") -DestinationPath (Join-Path $ExcelDest "armor.txt")
Copy-D2RTextTable -SourcePath (Join-Path $ExcelSource "armor.txt") -DestinationPath (Join-Path $BaseExcelDest "armor.txt")

Set-Content -LiteralPath (Join-Path $DestData "global\dataversionbuild.txt") -Value $D2CompareBuild -Encoding ASCII

New-Item -ItemType Directory -Force -Path (Join-Path $DestData "D2RLAN") | Out-Null
Copy-Item -LiteralPath $ProbeMemoryOverrides -Destination (Join-Path $DestData "D2RLAN\memory_overrides.json") -Force

$ModInfo = [ordered]@{
    name = $ModName
    version = "0.1-d2rlan-probe"
    savepath = "$ModName/"
}

$ModInfo | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath (Join-Path $MpqRoot "modinfo.json") -Encoding UTF8
Write-ProbeUserSettings -Path (Join-Path $MpqRoot "MyUserSettings.json") -ModName $ModName -TemplatePath (Join-Path $TcpMpqRoot "MyUserSettings.json")

$LauncherConfig = Join-Path $LauncherRoot "D2RLAN.dll.config"

if (Test-Path -LiteralPath $LauncherConfig) {
    $InstallPathSetting = $D2RPath

    if (-not $InstallPathSetting.EndsWith([System.IO.Path]::DirectorySeparatorChar)) {
        $InstallPathSetting += [System.IO.Path]::DirectorySeparatorChar
    }

    Set-D2RLANSetting -Path $LauncherConfig -Name "SelectedMod" -Value $ModName
    Set-D2RLANSetting -Path $LauncherConfig -Name "InstallPath" -Value $InstallPathSetting
    Set-D2RLANSetting -Path $LauncherConfig -Name "LANOffline" -Value "True"
    Set-D2RLANSetting -Path $LauncherConfig -Name "HUDDebug" -Value "False"

    $UserConfigRoot = Join-Path $env:LOCALAPPDATA "D2RLAN"

    if (Test-Path -LiteralPath $UserConfigRoot) {
        Get-ChildItem -Path $UserConfigRoot -Recurse -Filter "user.config" -ErrorAction SilentlyContinue | ForEach-Object {
            try {
                $SavedInstallPath = Get-D2RLANSetting -Path $_.FullName -Name "InstallPath"

                if ($SavedInstallPath -eq $InstallPathSetting) {
                    Set-D2RLANSetting -Path $_.FullName -Name "SelectedMod" -Value $ModName
                    Set-D2RLANSetting -Path $_.FullName -Name "LANOffline" -Value "True"
                    Set-D2RLANSetting -Path $_.FullName -Name "HUDDebug" -Value "False"
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

if ((Test-Path -LiteralPath $LauncherRoot) -and -not $KeepD2RHUDInjection) {
    Disable-D2RHUDInjection -LauncherRoot $LauncherRoot
}

Write-Host ""
Write-Host "Done."
Write-Host "D2RLAN probe launch arguments:"
Write-Host "  -mod $ModName -txt -enablerespec"
Write-Host ""
Write-Host "If the launcher is already open, close and reopen it so the selected mod reloads."
