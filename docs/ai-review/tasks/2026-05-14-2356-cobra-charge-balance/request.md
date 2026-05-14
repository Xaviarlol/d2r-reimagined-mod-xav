---
schema: ai-review-task-v1
id: 2026-05-14-2356-cobra-charge-balance
status: ready_for_claude
phase: code_review
round: 1
max_rounds: 3
created_by: codex
created_at: 2026-05-14T23:56:00+02:00
updated_at: 2026-05-14T23:56:00+02:00
repo: C:\Users\ericb\Dropbox\AI projects\d2r\d2r-reimagined-fresh
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

# Review Request

## Original User Request

```text
make the following changes:

Increase charge 1 damage by about 50%
Reduce charge 2's poison cloud damage by 50%, but make the duration of the cloud 6 seconds
charge 3 no change
```

## Goal

Rebalance Cobra Strike while preserving the tested charge behavior:

- Charge 1 remains the direct single-target poison finisher, with about 50% higher poison damage.
- Charge 2 uses a separate cloud-hit server missile so its damage can be lowered without changing charge 3.
- Charge 2 cloud visual duration is extended to 6 seconds.
- Charge 3 remains on the existing `cobrastrikenova` payload with no damage or duration changes.

## Phase

code_review

## Scope

- `data/global/excel/skills.txt`
- `data/global/excel/base/skills.txt`
- `data/global/excel/skilldesc.txt`
- `data/global/excel/base/skilldesc.txt`
- `data/global/excel/missiles.txt`
- `data/global/excel/base/missiles.txt`
- `data/hd/missiles/missiles.json`
- `data/local/lng/strings/skills.json`
- `docs/modding-findings.md`

## Design Or Diff

See `design.md` and `diff.patch`.

## Review Questions

1. Does routing charge 2 to `cobrastrikecloudhit` while leaving charge 3 on `cobrastrikenova` correctly preserve charge 3?
2. Are the charge 1 poison curve increases close enough to +50% without changing charge duration or hooks?
3. Does the charge 2 damage/duration implementation match the requested lower total poison payload over 6 seconds?
4. Is extending `cobrastrikecloud` `Range` to 150 the correct way to make the visible cloud last 6 seconds?
5. Are active/base TSV files synchronized and column-safe?
6. Are tooltip formulas and string text consistent with the gameplay-side changes?
