---
schema: ai-review-task-v1
id: 2026-05-14-1720-fists-fire-tooltip-percent
status: ready_for_claude
phase: code_review
round: 1
max_rounds: 3
created_by: codex
created_at: 2026-05-14T17:20:36Z
updated_at: 2026-05-14T17:20:36Z
repo: C:\Users\ericb\Dropbox\AI projects\d2r\d2r-reimagined-fresh
branch: xav-custom
base_ref: HEAD
head_ref:
original_user_request_included: true
live_publish_allowed: true
last_review:
last_verdict:
claimed_by:
claimed_at:
reviewed_at:
---

# Review Request

## Original User Request

```text
fix fist of fire tooltip and double check the formulas, another AI agent added weapon damage to charge 1 and 2.
```

## Goal

Fix the Fists of Fire tooltip garbage text caused by raw literal percent signs in the English charge 1/2 strings, and confirm the tooltip remains consistent with the current weapon-damage-as-fire gameplay formula.

## Phase

code_review

## Scope

- `data/local/lng/strings/skills.json`
- `docs/modding-findings.md`
- Formula review of `data/global/excel/skills.txt`, `data/global/excel/base/skills.txt`, `data/global/excel/skilldesc.txt`, and `data/global/excel/base/skilldesc.txt`
- Local publish to `C:\Program Files (x86)\Diablo II Resurrected\mods\XavReimagined\XavReimagined.mpq` is allowed for playtesting.

## Design Or Diff

See `design.md` and `diff.patch`.

## Review Questions

1. Is escaping `100%` as `100%%` the correct fix for the corrupted tooltip rendering?
2. Do the current Fists of Fire gameplay fields actually add 100% weapon damage as fire to charge 1 and charge 2 releases?
3. Are the `skilldesc.txt` formulas still consistent with the gameplay row?
4. Are JSON and TSV structures safe?
5. Is this safe to publish for playtesting?

## Suggested Follow-up Tests

- Open the Fists of Fire tooltip in game and verify charge 1 displays `+ 100% weapon damage as fire` without garbage numeric text.
- Verify charge 2 displays `+ 100% weapon damage as fire` without garbage numeric text.
- Verify charge 3 remains unchanged.
