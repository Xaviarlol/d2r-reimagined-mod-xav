---
schema: ai-review-task-v1
id: 2026-05-15-0104-phoenix-prgstack
status: consensus_reached
phase: code_review
round: 1
max_rounds: 3
created_by: codex
created_at: 2026-05-15T01:04:00+02:00
updated_at: 2026-05-16T16:45:16+02:00
repo: C:\Users\ericb\Dropbox\AI projects\d2r\d2r-reimagined-fresh
branch: xav-custom
base_ref: HEAD
head_ref:
original_user_request_included: true
live_publish_allowed: true
last_review: claude-review-r01.md
last_verdict: approved
claimed_by: claude
claimed_at: 2026-05-14T22:09:41Z
reviewed_at: 2026-05-14T22:09:41Z
approval_source: user_override
approved_at: 2026-05-16T16:45:16+02:00
review_suspended_by: eric
review_suspended_at: 2026-05-16T16:45:16+02:00
review_suspend_reason: External AI review loop suspended by user request; current queue marked approved.
---


# Review Request

## Original User Request

```text
change phoenix strike to use prgstack also.
```

## Prior Context

Eric asked whether charge-up skills such as Fists of Fire / Claws of Thunder combine lower charge payloads into a 3-charge finisher. The local data shows those stack-style elemental skills use `prgstack=1`, while Phoenix Strike is internally named `Royal Strike` and previously had `prgstack` blank.

## Goal

Set Phoenix Strike / `Royal Strike` to use `prgstack=1` in active and base `skills.txt`.

Expected gameplay experiment:
- A 3-charge Phoenix Strike finisher should also release lower charge payloads.
- A 2-charge Phoenix Strike finisher should also release charge 1.

## Phase

code_review

## Scope

- `data/global/excel/skills.txt`
- `data/global/excel/base/skills.txt`
- `docs/modding-findings.md`

## Design Or Diff

See `design.md` and `diff.patch`.

## Review Questions

1. Is `Royal Strike` the correct internal row for Phoenix Strike?
2. Is setting `prgstack=1` the narrowest change to test stacked Phoenix charge releases?
3. Do active/base `skills.txt` remain synchronized and TSV-safe?
4. Does this avoid changing Cobra Strike, Fists of Fire, Claws of Thunder, Blades of Ice, and Phoenix missile payload rows?

## User Approval / Review Suspension

On 2026-05-16T16:45:16+02:00, Eric instructed Codex to suspend the external Claude review loop for now and mark the current review queue approved. This task is closed as `consensus_reached` by user override. Any future risky gameplay/data work can open a new task if the review process resumes.
