---
schema: ai-review-task-v1
id: 2026-05-20-1243-unique-set-base-level-gate-lowering
status: ready_for_claude
phase: code_review
round: 1
max_rounds: 3
created_by: codex
created_at: 2026-05-20T12:44:32Z
updated_at: 2026-05-20T12:44:32Z
repo: C:\Dropbox\AI projects\d2r\d2r-reimagined-fresh
branch: xav-custom
base_ref: 81afcc70d19c6b05a9832c58b249949576613b7c
head_ref: xav-custom
original_user_request_included: true
live_publish_allowed: false
last_review:
last_verdict:
last_response:
---

# Review Request

## Original User Request

```text
only change ones that will result in lowering the level - do not change ones that are already the same or lower than the base item level
```

## Context

The prior proposal file listed every unique/set row whose `lvl` did not match the white base item's `level`:

`docs/unique-set-base-level-gate-proposal-2026-05-20.tsv`

Eric clarified that Codex should only apply rows where the unique/set `lvl` is higher than the base item level. Rows where the unique/set `lvl` is already equal to or lower than the base item level must not be changed.

## Files To Review

- `data/global/excel/uniqueitems.txt`
- `data/global/excel/base/uniqueitems.txt`
- `data/global/excel/setitems.txt`
- `data/global/excel/base/setitems.txt`
- `docs/unique-set-base-level-gate-applied-2026-05-20.tsv`

## Intended Behavior

For weapon/armor ladder bases only:

- If `unique/set lvl > white base item level`, set `unique/set lvl = white base item level`.
- If `unique/set lvl <= white base item level`, leave it unchanged.
- Exclude no-ladder misc/jewellery/charm/jewel style rows.
- Keep active and base copies synchronized.
- Do not change `lvl req`.

## Codex Validation Already Run

```text
unique: changed 333
set: changed 61
applied 394 {'set': 61, 'unique': 333}

validated_changes 394
errors 0
```

Validation checked:

- Every changed row only changed the `lvl` column.
- Every changed row was a lowering.
- No non-target row changed.
- Active/base copies are structurally equal after the rewrite.

## Review Questions

1. Did Codex only lower `lvl` values and avoid raising any rows?
2. Did Codex correctly restrict the change to weapon/armor rows with normal/exceptional/elite base ladders?
3. Are active/base files synchronized?
4. Are there any D2R data risks in setting unique/set drop `lvl` to the base item `level` for these rows?
