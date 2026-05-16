---
schema: ai-review-task-v1
id: 2026-05-15-0024-cobra-cloud-srcdamage-zero
status: consensus_reached
phase: code_review
round: 1
max_rounds: 3
created_by: codex
created_at: 2026-05-15T00:24:00+02:00
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
sourcedam is risky on dot effects. Please set it to 0 for now
```

## Prior Context

Eric asked why Cobra Strike charge 2's tooltip said `50% weapon damage` and whether the poison cloud source damage was `128` before the recent rebalance. The active rows showed:

- `cobrastrikecloudhit` at `SrcDamage=64`
- `cobrastrikecloud` at `SrcDamage=128`
- `cobrastrikenova` at `SrcDamage=128`

This request applies to the Cobra charge 2 poison cloud DOT path, not the Phoenix Strike source-damage change.

## Goal

Set Cobra Strike charge 2 cloud source damage to zero for now:
- `cobrastrikecloudhit` should use `SrcDamage=0`
- `cobrastrikecloud` should use `SrcDamage=0`
- `cobrastrikenova` should remain unchanged for charge 3

Update the charge 2 tooltip so it no longer advertises weapon damage.

## Phase

code_review

## Scope

- `data/global/excel/missiles.txt`
- `data/global/excel/base/missiles.txt`
- `data/local/lng/strings/skills.json`
- `docs/modding-findings.md`

## Design Or Diff

See `design.md` and `diff.patch`.

## Review Questions

1. Does this correctly zero only the Cobra charge 2 cloud-related source damage rows?
2. Is leaving `cobrastrikenova` at `SrcDamage=128` correct for the "charge 3 no change" context?
3. Is the charge 2 tooltip now consistent with the gameplay fields?
4. Are active/base `missiles.txt` synchronized and TSV-safe?

## User Approval / Review Suspension

On 2026-05-16T16:45:16+02:00, Eric instructed Codex to suspend the external Claude review loop for now and mark the current review queue approved. This task is closed as `consensus_reached` by user override. Any future risky gameplay/data work can open a new task if the review process resumes.
