---
schema: ai-review-task-v1
id: 2026-05-19-1339-rare-greater-affix-full-audit
status: cancelled
phase: re_review
round: 2
max_rounds: 3
created_by: codex
created_at: 2026-05-19T13:39:54Z
updated_at: 2026-05-19T21:46:38Z
repo: C:\Dropbox\AI projects\d2r\d2r-reimagined-fresh
branch: xav-custom
base_ref: 49de242a
head_ref: xav-custom
original_user_request_included: true
live_publish_allowed: false
last_review: claude-review-r01.md
last_verdict: needs_fixes
---

# Review Request

## Superseded

This narrower review request is superseded by `docs/ai-review/tasks/2026-05-19-2146-rare-affix-final-preimplementation-review/request.md`, which consolidates the rare-affix math, maxlevel policy, and pre-implementation checks into one final Claude pass.

## Original User Request

```text
/goal go through all affixes and make ure you capture every apex affix for each family and then draft a full list of greater affixes with their effective chance to spawn on an item

/goal you didnt do what I said then. I said to make greater affixes 10x rarer than their current apex. You need to redo all the frequency math. Afterwards, compare the before and after probability (using the simple total affixes available divided by freq for each affix before and after our overhaul). The % chance should be virtually identitcal for all affixes before and after the changes. This will be a good sanity check to ensure the main objective of not changing the proportion of rarity for everything except greater affixes. Do you agree that this test will prove your frequency math?
```

## Goal

Review the full rare-affix apex audit and draft Greater Affix chance model before implementation.

## Scope

- Generated audit and chance table: `docs/rare-greater-affix-apex-audit-2026-05-19.md`
- Generated chance TSV: `docs/rare-greater-affix-chance-table-2026-05-19.tsv`
- Generated row-level sanity TSV: `docs/rare-greater-affix-probability-sanity-2026-05-19.tsv`
- Generated per-item-type scope validation TSV: `docs/rare-greater-affix-scope-validation-2026-05-19.tsv`
- Generator script: `scripts/audit_rare_affix_apexes.py`
- Canonical design link update: `docs/rare-item-rework-design-2026-05-18.md`
- Findings link update: `docs/modding-findings.md`
- No game-data TXT implementation yet.
- Round 1 response: `codex-response-r01.md`

## Review Questions

1. Does the generated coverage audit capture every rare-eligible affix group that should be considered an apex family?
2. Are any groups incorrectly deferred or marked optional when they should receive a Phase 2 Greater candidate?
3. Does the revised frequency model correctly make each Greater candidate 10x rarer than its current apex row(s) in the final scaled table?
4. Does the probability sanity TSV prove that existing affixes keep identical relative proportions when Greater rows are excluded, and only lose the unavoidable absolute probability mass taken by the new Greater rows?
5. Does the chance model make correct use of `itype*` / `etype*`, item type inheritance, current affix pools, candidate synthetic rows, same-group blocking, and the apex-vs-Greater comparison columns?
6. Are the effective chances in the Greater table reasonable enough for a first design draft, especially high-impact rows like `Greater Grandmaster's`, `Greater Godly`, +skills, max resist, speed, leech, and charm affixes?
7. Which proposed Greater families need to be split more carefully by item scope or element before implementation?
