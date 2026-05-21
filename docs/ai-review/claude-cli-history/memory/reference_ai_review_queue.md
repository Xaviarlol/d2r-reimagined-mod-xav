---
name: AI review queue protocol
description: How to process Eric's D2R mod review queue. Triggered by "Check pending review requests" (often scheduled). One task per run, structured review file output.
type: reference
originSessionId: 80430070-75f6-4d4b-afde-059a1f4801e5
---
When prompted with "Check pending review requests" (or similar), follow this protocol.

## Queue location

- Root: `C:\Dropbox\AI projects\d2r\d2r-reimagined-fresh\docs\ai-review`
- Tasks: `docs\ai-review\tasks\<task-id>\`
- If queue root does not exist: say exactly `No pending review requests.` and stop. Do not create it.

## Per-task files

- `request.md` (required, has frontmatter + `## Original User Request` heading with fenced block)
- `design.md` (optional)
- `diff.patch` (optional)
- `claude-review-rXX.md` (mine; XX is 2-digit zero-padded round number)
- `codex-response-rXX.md` (Codex's per-round response)
- `claude.lock` (mine, while in progress)

## Pick the next task

Scan `docs\ai-review\tasks\*\request.md` for `status: ready_for_claude`. Sort oldest first by:
1. `created_at` ascending (ISO 8601 UTC)
2. `id` lexicographic if `created_at` ties
3. `request.md` mtime if `created_at` is missing — note the fallback in the review

Process exactly one task per run. If none ready: `No pending review requests.`

## Lock skip rule

- `claude.lock` exists and is **< 2 hours old** → skip the task, even if it looks like my own prior lock.
- `claude.lock` exists and is **≥ 2 hours old** → treat as stale, replace it, and note "stale lock replaced" in the review.

## Required request.md frontmatter (validate)

```yaml
schema: ai-review-task-v1
id: <task-id>
status: ready_for_claude   # I update to claude_in_progress then claude_reviewed
phase: design_review | code_review | re_review
round: <number>
max_rounds: <number>
created_by: codex
created_at: <ISO 8601 UTC>
updated_at: <ISO 8601 UTC>
repo: C:\Dropbox\AI projects\d2r\d2r-reimagined-fresh
branch: xav-custom
base_ref: <commit or blank>
head_ref: <commit or blank>
original_user_request_included: true
live_publish_allowed: false
```

If `original_user_request_included: true` but the `## Original User Request` heading is missing or its fenced block is empty: set `status: blocked_needs_user`, write a short review explaining, and stop.

## Claim & write protocol

1. Check `claude.lock` per skip rule above.
2. Write `claude.lock`:
   ```yaml
   schema: ai-review-lock-v1
   task_id: <task-id>
   reviewer: claude
   reviewer_model: claude-opus-4-7
   created_at: <ISO 8601 UTC>
   ```
3. Update `request.md` frontmatter (status fields only):
   - `status: claude_in_progress`
   - `claimed_by: claude`
   - `claimed_at: <ISO 8601 UTC>`
4. Review against Eric's original request (under `## Original User Request`), not just Codex's summary. Read any `design.md`, `diff.patch`, and the actual repo state at `head_ref`.
5. Write `claude-review-rXX.md` where XX = current `round` value, zero-padded (round 1 → `claude-review-r01.md`).
6. Update `request.md` frontmatter:
   - `status: claude_reviewed`
   - `last_review: claude-review-rXX.md`
   - `last_verdict: <verdict>`
   - `reviewed_at: <ISO 8601 UTC>`
7. Delete `claude.lock`.

## Review file frontmatter

```yaml
schema: ai-review-result-v1
task_id: <task-id>
round: <number>
reviewer: claude
verdict: approved | approved_with_notes | needs_fixes | high_risk_do_not_publish | blocked_needs_info
critical: <count>
high: <count>
medium: <count>
low: <count>
requires_codex_changes: true | false
```

## Review body sections (in this exact order)

1. `# Claude Review`
2. `## Verdict` — display string: `Approved` | `Approved with notes` | `Needs fixes` | `High risk / do not publish` | `Blocked / needs info`
3. `## Summary` — what Codex proposed and whether it matches Eric's original request
4. `## Findings` grouped by severity headers `### Critical` / `### High` / `### Medium` / `### Low`. Each finding includes:
   - ID like `CRITICAL-001`, `HIGH-001`, etc.
   - File path (markdown link)
   - Row/item/skill/line if applicable
   - Issue
   - Why it matters
   - Suggested fix
   - Whether it blocks approval
5. `## Validation Checks` — yes/no list:
   - Original user request reviewed
   - Git diff or design reviewed
   - TSV column counts checked
   - Active/base sync checked
   - Tooltip vs gameplay consistency considered
   - Live publish risk considered
   - Docs checked
6. `## Codex Action Items` — the exact changes Codex should make
7. `## Suggested Follow-up Tests` — practical script or in-game tests

## Review priorities (judge against these)

1. Match Eric's original request, not just Codex's summary.
2. Does the design/code actually accomplish the stated gameplay goal?
3. If Eric asked for additive changes, are they really additive (no stat replacements)?
4. TSV column count matches header on every changed row.
5. Active/base file sync where relevant.
6. Tooltip/display values consistent with actual gameplay values.
7. D2R modding risks: skills, missiles, item generation, cube recipes, treasure classes, save compatibility, launch safety.
8. Docs updated when new modding knowledge is learned.

## Consensus

I never mark a task complete — Codex does that after reading my review.

Consensus reached when:
- Latest verdict is `Approved` or `Approved with notes`, AND
- 0 Critical findings, AND
- 0 High findings, AND
- Codex has either implemented or explicitly rejected remaining findings in `codex-response-rXX.md`.

If `max_rounds` reached and serious issues remain: `verdict: blocked_needs_info`, ask Eric/Codex to decide.

## Re-review

When a task returns with status flipped back to `ready_for_claude` and `round` incremented:
- Read the new `codex-response-rXX.md` for what changed since last round.
- Re-state any unresolved Critical/High findings from prior rounds if Codex didn't address them.

## Strict file-write boundary

Allowed writes during a task:
- `docs\ai-review\tasks\<task-id>\claude-review-rXX.md`
- `docs\ai-review\tasks\<task-id>\claude.lock`
- `docs\ai-review\tasks\<task-id>\request.md` (status frontmatter fields only — never the body, never the original user request, never other frontmatter fields)

Forbidden during a task:
- Any file under `data\`, `scripts\`, mod folders, or game/source code
- The live game folder
- Git operations beyond read-only (`status`, `show`, `diff`, `log`)
- Creating `docs\ai-review\` itself (Codex creates it)
- Any file outside `docs\ai-review\tasks\<task-id>\`
