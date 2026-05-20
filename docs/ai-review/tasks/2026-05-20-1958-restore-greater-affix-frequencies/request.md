---
schema: ai-review-task-v1
id: 2026-05-20-1958-restore-greater-affix-frequencies
status: ready_for_claude
phase: design_review
round: 1
max_rounds: 2
created_by: codex
created_at: 2026-05-20T19:58:32Z
updated_at: 2026-05-20T19:58:32Z
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

# Review Request

## Original User Request

```text
prepare the restore, and send it to claude to verify
```

## Goal

Prepare a safe restore plan for the temporary Greater Affix frequency test, without applying or publishing the restore until Claude verifies the approach.

## Phase

design_review

## Scope

- Restore only the `frequency` column in:
  - `data/global/excel/magicprefix.txt`
  - `data/global/excel/base/magicprefix.txt`
  - `data/global/excel/magicsuffix.txt`
  - `data/global/excel/base/magicsuffix.txt`
- Preserve later non-frequency fixes:
  - Greater rows remain `spawnable=1`, `rare=1`.
  - Greater marker properties/wrappers from `088d75fa` remain intact.
  - Gold `GREATER AFFIX:` marker string remains intact.
- Do not live-publish until Eric confirms after review.

## Design Or Diff

See `design.md` in this task folder.

## Review Questions

1. Is `00337b07` / `6e2d5a87` the correct clean frequency source for restoring the intended rare-affix rework weights?
2. Is restoring only the `frequency` column safer than checking out entire old TSV files?
3. Does the plan preserve active/base sync?
4. Does the plan avoid undoing `spawnable=1` for Greater Affixes and the later marker-wrapper tooltip implementation?
5. Are the expected restored frequency distributions plausible for the final non-test state?
6. Is this safe to implement and publish after Eric finishes the current in-game test?
