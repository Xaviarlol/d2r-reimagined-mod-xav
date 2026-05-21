[CmdletBinding(DefaultParameterSetName = 'Path')]
param(
    [Parameter(Mandatory = $true, ParameterSetName = 'Path')]
    [string]$PromptPath,

    [Parameter(Mandatory = $true, ParameterSetName = 'Text')]
    [string]$Prompt,

    [string]$ReviewName = 'review',
    [string]$SessionId = 'da1ceeba-3d9c-44b1-a65f-fbcd0eb0950e',
    [string]$Model = 'opus',
    [string]$ReviewerName = 'd2r-codex-reviewer',
    [string]$ClaudeExe = 'claude',
    [switch]$NoMirror,
    [switch]$NoResume
)

$ErrorActionPreference = 'Stop'

function Get-SafeName {
    param([string]$Value)

    $safe = $Value -replace '[^A-Za-z0-9._-]+', '-'
    $safe = $safe.Trim('-')
    if ([string]::IsNullOrWhiteSpace($safe)) {
        return 'review'
    }
    return $safe.ToLowerInvariant()
}

function Get-ClaudeProjectSlug {
    param([string]$RepoRoot)

    return ($RepoRoot -replace ':', '-' -replace '[\\/ ]+', '-')
}

$repoRoot = Resolve-Path (Join-Path $PSScriptRoot '..')
$historyRoot = Join-Path $repoRoot 'docs\ai-review\claude-cli-history'
$runRoot = Join-Path $historyRoot 'runs'
$sessionMirrorRoot = Join-Path $historyRoot 'sessions'
$memoryMirrorRoot = Join-Path $historyRoot 'memory'

New-Item -ItemType Directory -Force -Path $historyRoot, $runRoot, $sessionMirrorRoot, $memoryMirrorRoot | Out-Null

$timestamp = (Get-Date).ToUniversalTime().ToString('yyyyMMddTHHmmssZ')
$safeReviewName = Get-SafeName $ReviewName
$runDir = Join-Path $runRoot "$timestamp-$safeReviewName"
New-Item -ItemType Directory -Force -Path $runDir | Out-Null

if ($PSCmdlet.ParameterSetName -eq 'Path') {
    $resolvedPromptPath = Resolve-Path $PromptPath
    $promptText = Get-Content -LiteralPath $resolvedPromptPath -Raw
    Copy-Item -LiteralPath $resolvedPromptPath -Destination (Join-Path $runDir 'prompt.md') -Force
} else {
    $promptText = $Prompt
    Set-Content -LiteralPath (Join-Path $runDir 'prompt.md') -Value $promptText -Encoding UTF8
}

$claudeArgs = @()
if ($NoResume) {
    $claudeArgs += @('--model', $Model, '--name', $ReviewerName)
} else {
    $claudeArgs += @('--resume', $SessionId, '--model', $Model)
}
$claudeArgs += @(
    '--permission-mode', 'dontAsk',
    '--tools', 'Read,Glob,Grep',
    '-p', $promptText,
    '--output-format', 'json'
)

$stderrPath = Join-Path $runDir 'stderr.log'
$rawLines = & $ClaudeExe @claudeArgs 2> $stderrPath
$exitCode = $LASTEXITCODE
$raw = ($rawLines | ForEach-Object { $_.ToString() }) -join [Environment]::NewLine
Set-Content -LiteralPath (Join-Path $runDir 'result.json') -Value $raw -Encoding UTF8

if ($exitCode -ne 0) {
    throw "claude exited with code $exitCode. Raw output saved to $runDir\result.json"
}

$result = $raw | ConvertFrom-Json
if ($result.result) {
    Set-Content -LiteralPath (Join-Path $runDir 'review.md') -Value $result.result -Encoding UTF8
}

$effectiveSessionId = $result.session_id
if ([string]::IsNullOrWhiteSpace($effectiveSessionId)) {
    $effectiveSessionId = $SessionId
}

$claudeProjectSlug = Get-ClaudeProjectSlug $repoRoot.Path
$claudeProjectDir = Join-Path $env:USERPROFILE ".claude\projects\$claudeProjectSlug"

if (-not $NoMirror) {
    $sessionJsonl = Join-Path $claudeProjectDir "$effectiveSessionId.jsonl"
    if (Test-Path -LiteralPath $sessionJsonl) {
        Copy-Item -LiteralPath $sessionJsonl -Destination (Join-Path $sessionMirrorRoot "$effectiveSessionId.jsonl") -Force
        Copy-Item -LiteralPath $sessionJsonl -Destination (Join-Path $runDir 'session.jsonl') -Force
    }

    $localMemoryDir = Join-Path $claudeProjectDir 'memory'
    if (Test-Path -LiteralPath $localMemoryDir) {
        $runMemoryDir = Join-Path $runDir 'memory'
        New-Item -ItemType Directory -Force -Path $runMemoryDir | Out-Null
        Get-ChildItem -LiteralPath $localMemoryDir -File -Filter '*.md' | ForEach-Object {
            Copy-Item -LiteralPath $_.FullName -Destination (Join-Path $memoryMirrorRoot $_.Name) -Force
            Copy-Item -LiteralPath $_.FullName -Destination (Join-Path $runMemoryDir $_.Name) -Force
        }
    }
}

$metadata = [ordered]@{
    schema = 'claude-cli-review-run-v1'
    created_at = (Get-Date).ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ssZ')
    review_name = $ReviewName
    model = $Model
    reviewer_name = $ReviewerName
    claude_exe = $ClaudeExe
    requested_session_id = $SessionId
    effective_session_id = $effectiveSessionId
    run_dir = $runDir
    claude_project_dir = $claudeProjectDir
    result_uuid = $result.uuid
    stderr_path = $stderrPath
    mirror_enabled = -not $NoMirror
    verdict_recorded_by_claude = $null
}

Set-Content -LiteralPath (Join-Path $runDir 'metadata.json') -Value ($metadata | ConvertTo-Json -Depth 5) -Encoding UTF8
Set-Content -LiteralPath (Join-Path $historyRoot 'latest-run.json') -Value ($metadata | ConvertTo-Json -Depth 5) -Encoding UTF8

[pscustomobject]@{
    RunDir = $runDir
    SessionId = $effectiveSessionId
    ResultUuid = $result.uuid
    ResultPath = Join-Path $runDir 'result.json'
    ReviewPath = Join-Path $runDir 'review.md'
}
