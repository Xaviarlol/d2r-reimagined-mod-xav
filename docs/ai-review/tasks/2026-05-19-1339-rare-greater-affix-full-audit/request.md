---
schema: ai-review-task-v1
id: 2026-05-19-1339-rare-greater-affix-full-audit
status: ready_for_claude
phase: design_review
round: 1
max_rounds: 3
created_by: codex
created_at: 2026-05-19T13:39:54Z
updated_at: 2026-05-19T13:39:54Z
repo: C:\Dropbox\AI projects\d2r\d2r-reimagined-fresh
branch: xav-custom
base_ref: 7064bdae
head_ref: xav-custom
original_user_request_included: true
live_publish_allowed: false
last_review:
last_verdict:
---

# Review Request

## Original User Request

```text
/goal go through all affixes and make ure you capture every apex affix for each family and then draft a full list of greater affixes with their effective chance to spawn on an item
```

## Goal

Review the full rare-affix apex audit and draft Greater Affix chance model before implementation.

## Scope

- Generated audit and chance table: `docs/rare-greater-affix-apex-audit-2026-05-19.md`
- Generator script: `scripts/audit_rare_affix_apexes.py`
- Canonical design link update: `docs/rare-item-rework-design-2026-05-18.md`
- Findings link update: `docs/modding-findings.md`
- No game-data TXT implementation yet.

## Review Questions

1. Does the generated coverage audit capture every rare-eligible affix group that should be considered an apex family?
2. Are any groups incorrectly deferred or marked optional when they should receive a Phase 2 Greater candidate?
3. Does the chance model make correct use of `itype*` / `etype*`, item type inheritance, current affix pools, candidate synthetic rows, and same-group blocking?
4. Are the effective chances in the Greater table reasonable enough for a first design draft, especially high-impact rows like `Greater Grandmaster's`, `Greater Godly`, +skills, max resist, speed, leech, and charm affixes?
5. Which proposed Greater families need to be split more carefully by item scope or element before implementation?
