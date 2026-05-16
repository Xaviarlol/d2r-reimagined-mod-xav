---
schema: ai-review-task-v1
id: 2026-05-16-1541-all-belts-four-rows
status: ready_for_review
phase: code_review
round: 0
max_rounds: 3
created_by: codex
created_at: 2026-05-16T15:41:00+02:00
updated_at: 2026-05-16T15:41:00+02:00
repo: C:\Users\ericb\Dropbox\AI projects\d2r\d2r-reimagined-fresh
branch: xav-custom
base_ref: HEAD
head_ref:
original_user_request_included: true
live_publish_allowed: true
---

# Review Request

## Original User Request

```text
how do we make all belts have the 4 rows of potion slots
do it
```

## Prior Context

The project keeps active TSV data under `data/global/excel/` and mirrored reference data under `data/global/excel/base/`. For gameplay table changes, both copies should stay synchronized.

## Goal

Make every belt base provide four potion rows, including the low normal belt bases that previously had lower or inconsistent `belt` column values.

## Phase

code_review

## Scope

- `data/global/excel/armor.txt`
- `data/global/excel/base/armor.txt`
- `docs/modding-findings.md`

## Design Or Diff

See `design.md`.

## Review Questions

1. Do the four low normal belt base rows now use the same four-row belt tier as Plated Belt?
2. Are active and base `armor.txt` synchronized?
3. Does the change avoid touching unique/set item rows unnecessarily?
4. Is the new documentation accurate about the `armor.txt` `belt` column driving potion row capacity?
