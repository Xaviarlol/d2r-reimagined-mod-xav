# AI Review Protocol

This file is the durable coordination contract between Eric, Codex, Claude, and any Codex subagents working on this Diablo II Resurrected mod repository.

If a conversation restarts, read this file before starting risky design or code/data work.

## Paths

Primary repository:

```text
C:\Dropbox\AI projects\d2r\d2r-reimagined-fresh
```

Main working branch:

```text
xav-custom
```

Live game folder:

```text
E:\Diablo II Resurrected\mods\XavReimagined\XavReimagined.mpq
```

Launch arguments:

```text
-mod XavReimagined -txt
```

Review queue root:

```text
C:\Dropbox\AI projects\d2r\d2r-reimagined-fresh\docs\ai-review
```

Task folders:

```text
docs\ai-review\tasks\<task-id>\
```

## Purpose

Codex is the primary implementer. Claude is an independent reviewer. The review loop exists to catch design mistakes, data-table risks, tooltip/gameplay mismatches, unsafe TSV edits, and cases where a change technically modifies files but misses Eric's gameplay intent.

For small obvious edits, Codex may skip the queue. For skill changes, missile changes, cube recipes, itemization passes, treasure classes, TSV-wide changes, live-publish-sensitive work, or anything with tooltip/gameplay mismatch risk, use this queue.

## Roles

Eric:

- Provides gameplay/design requests.
- Can override the review loop.
- Decides ambiguous product/design tradeoffs.

Codex:

- Writes designs, patches, code, data changes, docs, commits, pushes, and live publishes when appropriate.
- Creates review tasks for Claude.
- Includes Eric's original request verbatim in every task.
- Reads Claude reviews, writes Codex responses, and either fixes issues or explains why findings are rejected.
- Marks consensus reached.

Claude:

- Reviews only.
- Does not edit gameplay/data/code files.
- Does not publish to the live game folder.
- Does not commit or push.
- Writes structured Markdown reviews into task folders.

Codex subagents:

- Follow this same protocol when assigned design/code/data work that needs review.
- Do not bypass Claude for risky work.
- Do not publish, push, or touch the live game folder unless the parent Codex agent explicitly assigns that responsibility.

## Folder Layout

Each task lives in its own folder:

```text
docs\ai-review\tasks\<task-id>\
  request.md
  design.md              optional
  diff.patch             optional
  claude-review-r01.md   written by Claude
  codex-response-r01.md  written by Codex
  claude-review-r02.md   later rounds as needed
  codex-response-r02.md
  claude.lock            temporary lock file
```

Completed or obsolete tasks may be moved to:

```text
docs\ai-review\archive\
```

## Task Statuses

Use these `request.md` frontmatter statuses:

```text
draft
ready_for_claude
claude_in_progress
claude_reviewed
codex_in_progress
consensus_reached
blocked_needs_user
cancelled
```

Normal code review loop:

```text
ready_for_claude
claude_in_progress
claude_reviewed
codex_in_progress
ready_for_claude
...
consensus_reached
```

Claude never marks a task `consensus_reached`. Codex does that after reading Claude's latest review and writing a Codex response.

## Consensus

Consensus is reached when:

- Claude's latest verdict is `approved` or `approved_with_notes`.
- There are zero Critical findings.
- There are zero High findings.
- Codex has either implemented or explicitly rejected remaining findings in `codex-response-rXX.md`.

If `max_rounds` is reached and serious issues remain, Codex should mark the task `blocked_needs_user` and ask Eric to decide.

## Request File Format

`request.md` must include YAML frontmatter:

```yaml
---
schema: ai-review-task-v1
id: 2026-05-14-example-task
status: ready_for_claude
phase: design_review
round: 1
max_rounds: 3
created_by: codex
created_at: 2026-05-14T12:34:56Z
updated_at: 2026-05-14T12:34:56Z
repo: C:\Dropbox\AI projects\d2r\d2r-reimagined-fresh
branch: xav-custom
base_ref: HEAD
head_ref:
original_user_request_included: true
live_publish_allowed: false
last_review:
last_verdict:
claimed_by:
claimed_at:
reviewed_at:
---
```

Timestamps are ISO 8601 UTC:

```text
2026-05-14T12:34:56Z
```

Every `request.md` must include Eric's original request exactly:

````markdown
## Original User Request

```text
<Eric's original request copied verbatim>
```
````

Claude validates both the flag and this section. If the section is missing or empty, Claude marks the task `blocked_needs_user`.

## Request Body Template

Use this body shape:

````markdown
# Review Request

## Original User Request

```text
<Eric's original request copied verbatim>
```

## Goal

Short description of what Codex is trying to accomplish.

## Phase

design_review | code_review | re_review

## Scope

- Files expected to change
- Systems affected
- Known constraints

## Design Or Diff

Point to `design.md`, `diff.patch`, commits, or both.

## Review Questions

1. Does this match Eric's request?
2. What are the likely D2R modding risks?
3. Are active/base files synchronized where needed?
4. Are TSV structures safe?
5. Are tooltip and gameplay values likely consistent?
6. Is this safe to publish/playtest?
````

## Claude Lock File

Claude uses `claude.lock` to avoid duplicate automated reviews.

Lock content:

```yaml
schema: ai-review-lock-v1
task_id: <task-id>
reviewer: claude
reviewer_model:
created_at: 2026-05-14T12:34:56Z
```

Lock rules:

- If `claude.lock` is less than 2 hours old, Claude skips the task.
- If `claude.lock` is 2 hours old or older, Claude may replace it and note that in the review.
- Claude removes the lock after writing its review and updating `request.md`.

## Claude Startup Behavior

Claude should:

1. Scan `docs\ai-review\tasks\*\request.md`.
2. Find the oldest task with `status: ready_for_claude`.
3. Sort by `created_at`, then `id`, then file mtime as fallback.
4. Process one task at a time.
5. If no task is ready, say exactly:

```text
No pending review requests.
```

Missing queue root is treated as an empty queue.

## Claude Allowed Writes

Claude may write only:

```text
docs\ai-review\tasks\<task-id>\claude-review-rXX.md
docs\ai-review\tasks\<task-id>\request.md frontmatter status fields only
docs\ai-review\tasks\<task-id>\claude.lock
```

Claude must not write:

```text
data\
scripts\
E:\Diablo II Resurrected\
git branches or refs
source/game/mod files outside docs\ai-review\tasks\<task-id>
```

## Claude Review Format

Claude writes `claude-review-rXX.md`, where `XX` is the current round.

Frontmatter:

```yaml
---
schema: ai-review-result-v1
task_id: <task-id>
round: 1
reviewer: claude
verdict: needs_fixes
critical: 0
high: 1
medium: 2
low: 0
requires_codex_changes: true
---
```

Verdicts:

```text
approved
approved_with_notes
needs_fixes
high_risk_do_not_publish
blocked_needs_info
```

Body:

```markdown
# Claude Review

## Verdict

Approved | Approved with notes | Needs fixes | High risk / do not publish | Blocked / needs info

## Summary

Briefly summarize what Codex proposed or changed, and whether it matches Eric's original request.

## Findings

Group by Critical, High, Medium, Low.

Each finding includes:

- ID, such as HIGH-001
- File path
- Row/item/skill/line if applicable
- Issue
- Why it matters
- Suggested fix
- Whether it blocks approval

## Validation Checks

Say yes/no for:

- Original user request reviewed
- Git diff or design reviewed
- TSV column counts checked
- Active/base sync checked
- Tooltip vs gameplay consistency considered
- Live publish risk considered
- Docs checked

## Codex Action Items

Exact actions for Codex.

## Suggested Follow-up Tests

Practical script or in-game tests.
```

## Codex Response Format

Codex writes `codex-response-rXX.md` after reading Claude's review.

Frontmatter:

```yaml
---
schema: ai-review-response-v1
task_id: <task-id>
round: 1
responder: codex
created_at: 2026-05-14T12:34:56Z
accepted_findings:
rejected_findings:
fixed_findings:
requires_rereview: true
---
```

Body:

```markdown
# Codex Response

## Summary

Short summary of how Codex handled the review.

## Accepted Findings

List finding IDs and fixes.

## Rejected Findings

List finding IDs and reasons.

## Changes Made

Files changed and validation run.

## Re-review Request

Say whether another Claude round is needed and why.
```

After writing a Codex response:

- If re-review is needed, Codex increments `round`, updates `updated_at`, sets `status: ready_for_claude`, and updates `base_ref` / `head_ref` / `diff.patch` as needed.
- If consensus is reached, Codex sets `status: consensus_reached`.

## Design Review Versus Code Review

Use `phase: design_review` before implementation when the approach itself is uncertain.

Use `phase: code_review` after implementation when Claude should inspect a diff, commit, or patch.

Use `phase: re_review` when Codex has responded to Claude findings and wants Claude to check the new round.

For risky work, the preferred sequence is:

```text
design_review -> code_review -> consensus_reached -> publish if requested/allowed
```

## D2R Modding Review Priorities

Claude should focus on:

- Does the change match Eric's original gameplay request?
- Are TSV column counts valid?
- Are empty TSV columns and trailing tabs preserved?
- Are active and base files synchronized when appropriate?
- Are tooltip strings consistent with actual gameplay fields?
- Are skill, missile, item, cube, and treasure-class mechanics likely valid?
- Could the change crash startup?
- Could the change silently do nothing because the wrong field was edited?
- Could existing items need respawn/cube refresh to show new stats?
- Were docs updated when new modding knowledge was learned?

## Publishing Rule

Claude never publishes.

Codex publishes only when Eric asks or when the current workflow explicitly allows automatic publish. Documentation-only changes do not need live publish.

Publish script:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\install-local.ps1
```

After publishing data changes, Codex should verify live files when practical, for example with `Get-FileHash`.

## Git Rule

Eric wants every set of changes version controlled on GitHub.

Codex should commit and push completed changes unless Eric asks not to.

Claude does not commit or push.

## Subagent Rule

When Codex launches subagents:

- Tell them this protocol exists.
- Give them the task ID if one exists.
- Tell them not to edit review files outside their assigned task.
- Tell them not to publish or push unless explicitly assigned.
- Tell them not to bypass Claude review for risky changes.

If a subagent creates a patch for risky work, the parent Codex agent is responsible for creating or updating the Claude review task.
