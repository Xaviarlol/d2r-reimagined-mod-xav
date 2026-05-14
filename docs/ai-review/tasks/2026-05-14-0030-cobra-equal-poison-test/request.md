---
schema: ai-review-task-v1
id: 2026-05-14-0030-cobra-equal-poison-test
status: consensus_reached
phase: code_review
round: 1
max_rounds: 3
created_by: codex
created_at: 2026-05-14T00:30:14Z
updated_at: 2026-05-14T00:51:36Z
repo: C:\Dropbox\AI projects\d2r\d2r-reimagined-fresh
branch: xav-custom
base_ref: df5c0b9f
head_ref:
original_user_request_included: true
live_publish_allowed: false
last_review: claude-review-r01.md
last_verdict: approved_with_notes
claimed_by: claude
claimed_at: 2026-05-14T00:33:50Z
reviewed_at: 2026-05-14T00:51:36Z
---

# Review Request

## Original User Request

```text
Ok for the first task under the new workflow:

Cobra strike Charge 1 and especially charge 2 are much lower damage than poison nova. For testing, can you adjust the flat damage portion for all 3 charges to be the same, and all use 100% weapon damage?
```

Amendment:

```text
wait I think its because nova is 2 sec poison vs 4 sec of the others. Make all of them 2 sec and same damage
```

## Goal

Normalize Cobra Strike for testing so charge 1, charge 2, and charge 3 all have the same flat poison damage curve, the same 2-second poison duration, and 100% weapon damage contribution.

## Phase

code_review

## Scope

- `data/global/excel/skills.txt`
- `data/global/excel/base/skills.txt`
- `data/global/excel/skilldesc.txt`
- `data/global/excel/base/skilldesc.txt`

Systems affected:

- Assassin Cobra Strike charge-up behavior
- Cobra Strike tooltip display
- Active/base TSV synchronization

Known constraints:

- D2R poison tooltip formulas use rate fields multiplied by poison length and divided by 16.
- In this repo, 100% source weapon damage is represented by `SrcDam` / `SrcDamage` value `128`.
- `cobrastrikenova` in `missiles.txt` already has `ELen 50` and `SrcDamage 128`; this patch intentionally leaves missile radius/velocity unchanged.

## Design Or Diff

See:

- `design.md`
- `diff.patch`

The patch is currently uncommitted and has not been published to the live game folder.

## Review Questions

1. Does the patch actually make charge 1, charge 2, and charge 3 use the same flat poison damage curve?
2. Does the patch make charge 1 and charge 2 use 2-second poison duration instead of 4-second duration?
3. Is charge 3 still using 100% weapon damage through the correct missile/source damage path?
4. Are active and base files synchronized for the edited rows?
5. Are the tooltip formulas consistent with the gameplay data?
6. Are TSV column counts and empty columns safe?
7. Is this safe to publish for testing?
