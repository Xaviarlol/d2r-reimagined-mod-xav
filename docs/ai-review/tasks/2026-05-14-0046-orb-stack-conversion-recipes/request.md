---
schema: ai-review-task-v1
id: 2026-05-14-0046-orb-stack-conversion-recipes
status: consensus_reached
phase: re_review
round: 2
max_rounds: 3
created_by: codex
created_at: 2026-05-14T00:46:09Z
updated_at: 2026-05-16T16:45:16+02:00
repo: C:\Users\ericb\Dropbox\AI projects\d2r\d2r-reimagined-fresh
branch: xav-custom
base_ref: HEAD
head_ref:
original_user_request_included: true
live_publish_allowed: true
last_review: claude-review-r02.md
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
while waiting for review, can you check the recipe that does 15 orb of infusion + p topaz, it doesnt seem to work?
```

## Additional User Clarification

```text
what is the max cube recipe input size? Just set it to that amount of ooi and remove the orb of assemlage recipe
```

```text
if you are doing 11 + topaz then keep the 11 + emerald for orb os assemblage.
```

```text
the issue with the cube recipes is you have the wrong item code for the gems. gmt and gme
```

## Goal

Fix the Orb of Infusion conversion recipes so they are usable with loose `ooi` items inside the Horadric Cube's 12-slot capacity and match the mod's player-facing Topaz/Emerald item codes.

## Phase

re_review

## Scope

- `data/global/excel/cubemain.txt`
- `data/global/excel/base/cubemain.txt`
- Horadric Cube recipes for Orb of Infusion conversion into Orb of Conversion and Orb of Assemblage.
- Removal of obsolete Infusion Orb stack/unstack cube recipes so this task uses loose `ooi` only.
- Local publish to `C:\Program Files (x86)\Diablo II Resurrected\mods\XavReimagined\XavReimagined.mpq` is allowed for playtesting.

## Design Or Diff

See `design.md`, `diff.patch`, `codex-response-r01.md`, and `codex-response-r02.md`.

## Review Questions

1. Does the revised 11-loose-orb approach match Eric's latest clarification?
2. Are the active/base `cubemain.txt` recipe rows synchronized?
3. Are the TSV structures safe and column counts preserved?
4. Is `numinputs=12` with `input 1="ooi,qty=11"` plus `gmt`/`gme` the right way to represent the cube's practical maximum loose-item recipe?
5. Is removing the Infusion Orb stack/unstack recipe family consistent with the loose-only workflow?
6. Is this safe to commit and publish for playtesting?

## Suggested Follow-up Tests

- Verify active/base `cubemain.txt` both have 106 columns and no malformed rows.
- Verify `11x ooi + Topaz (gmt)` outputs `ooc`.
- Verify `11x ooi + Emerald (gme)` outputs `ooa`.
- Verify `10x ooi + Topaz (gmt)` does not match.
- Verify the old impossible `15x ooi + perfect gem` recipes no longer exist.
- Verify Infusion Orb stack/unstack cube recipes no longer exist, while other orb stack recipes are untouched.

## User Approval / Review Suspension

On 2026-05-16T16:45:16+02:00, Eric instructed Codex to suspend the external Claude review loop for now and mark the current review queue approved. This task is closed as `consensus_reached` by user override. Any future risky gameplay/data work can open a new task if the review process resumes.
