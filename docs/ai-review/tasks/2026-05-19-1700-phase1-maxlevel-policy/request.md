---
schema: ai-review-task-v1
id: 2026-05-19-1700-phase1-maxlevel-policy
status: ready_for_claude
phase: design_review
round: 1
max_rounds: 3
created_by: codex
created_at: 2026-05-19T16:59:58Z
updated_at: 2026-05-19T16:59:58Z
repo: C:\Dropbox\AI projects\d2r\d2r-reimagined-fresh
branch: xav-custom
base_ref: 89fe33fa
head_ref: xav-custom
original_user_request_included: true
live_publish_allowed: false
---

# Review Request

## Original User Request

```text
I just realized that we probably dont want to be increasing MAX LEVEL, only level and reqlevel. Otherwise it actually makes it easier for rares overall to be better. What do you think?

yes, revert the maxlevel back to original in our plan.
```

## Goal

Review the Phase 1 rare-affix policy correction: existing affix rows should keep their original `maxlevel`, while Phase 1 still lowers `level` by 30% and `levelreq` by 15%.

## Rationale

Compressing existing `maxlevel` would make weaker affixes expire earlier. That indirectly improves high-level rare quality by shrinking the weak-affix pool, which is not the intended Phase 1 behavior. Phase 1 should make stronger affixes accessible earlier without making high-level rares cleaner overall.

The only new/changed `maxlevel` values should be on intentionally-created early duplicate rows for top affixes, where `maxlevel = original_top_level - 1` prevents duplicate top-affix odds at high level.

## Scope

- Canonical design: `docs/rare-item-rework-design-2026-05-18.md`
- Findings/memory notes: `docs/modding-findings.md`
- Session handoff note: `docs/session-handoff-2026-05-18.md`
- Comparison generator: `scripts/generate_affix_level_change_data.py`
- Regenerated source table: `docs/affix-level-requirement-changes-2026-05-19.tsv`
- Updated workbook outside the repo: `C:\Dropbox\AI projects\d2r\outputs\affix-level-requirement-changes\affix-level-requirement-changes-2026-05-19-maxlevel-preserved.xlsx`

No game-data TXT files are changed and no live publish is needed.

## Review Questions

1. Does preserving existing `maxlevel` correctly avoid the unintended high-level rare quality buff?
2. Is it still correct for intentionally-created early top-affix duplicate rows to use `maxlevel = original_top_level - 1`?
3. Does the regenerated TSV show no proposed changes to existing `maxlevel` values?
4. Are the docs clear that Phase 1 changes existing rows' `level` and `levelreq`, not existing `maxlevel`?
