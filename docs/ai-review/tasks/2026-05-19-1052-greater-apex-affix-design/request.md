---
schema: ai-review-task-v1
id: 2026-05-19-1052-greater-apex-affix-design
status: ready_for_claude
phase: design_review
round: 1
max_rounds: 3
created_by: codex
created_at: 2026-05-19T10:52:11Z
updated_at: 2026-05-19T10:52:11Z
repo: C:\Dropbox\AI projects\d2r\d2r-reimagined-fresh
branch: xav-custom
base_ref: b750dd00
head_ref: xav-custom
original_user_request_included: true
live_publish_allowed: false
last_review:
last_verdict:
---

# Review Request

## Original User Request

```text
ok so youll need to update the greater affixes to be better than grandmasters and any other apex affixes you missed before
```

## Goal

Review the revised Greater Affix candidate design. The important correction is that Greater Affixes must beat the strongest existing modded apex row in their affix group, not only the familiar vanilla-style top row.

## Scope

- Canonical design: `docs/rare-item-rework-design-2026-05-18.md`
- Findings summary: `docs/modding-findings.md`
- This task summary: `docs/ai-review/tasks/2026-05-19-1052-greater-apex-affix-design/design.md`
- No game-data TXT implementation yet.

## Review Questions

1. Does the new Greater Cruel target, fixed `dmg% 500`, correctly benchmark against `Grandmaster's` and weapon `Wraithly1` in group `111`?
2. Are the newly added apex baselines complete enough for the next implementation pass: `Grandmaster's`, weapon/armor `Wraithly1`, `Invulnerable1`, magic resistance rows, elemental absorb Coalescence rows, and +skills rows?
3. Does `Greater Godly` with `ac% 250-300` plus `red-dmg% 26-30` correctly beat both `Godly` and `Invulnerable1` without being obviously absurd?
4. Are the +skills Greater candidates safe as design candidates, or should any be deferred from Phase 2?
5. Are any other existing apex affixes still missing from the candidate list?
