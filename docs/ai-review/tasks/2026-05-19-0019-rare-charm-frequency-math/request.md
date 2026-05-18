---
schema: ai-review-task-v1
id: 2026-05-19-0019-rare-charm-frequency-math
status: ready_for_claude
phase: design_review
round: 2
max_rounds: 3
created_by: codex
created_at: 2026-05-18T22:19:05Z
updated_at: 2026-05-18T23:52:09Z
repo: C:\Dropbox\AI projects\d2r\d2r-reimagined-fresh
branch: xav-custom
base_ref: d4390941
head_ref: xav-custom
original_user_request_included: true
live_publish_allowed: false
last_review: claude-review-r01.md
last_verdict: needs_fixes
last_response: codex-response-r01.md
---

# Review Request

## Original User Request

```text
keep everything consistent, the levels should all be reduced by 30%. Regarding things like charms, you will indeed need to make +skills rarity = 10, and the greater affix freq 1. This means you will need to scale ALL charm affixes freq accordingly, so the proportions are exactly the same. Give me proposal for charms for example, how you will scale frequency. So I guess if there for a level 90 charm there are 20 possible affixes with a total freq of say 100, then you need to scale everything accordingly to maintain the same ratios

ok, put all of this up for review for claude. It is very important the math is correct here
```

## Goal

Review the rare-item rework design math, especially the charm frequency normalization proposal and the treatment of Greater Affixes.

## Phase

design_review

## Scope

- Canonical rare item rework design document.
- Phase 1 affix level compression and level requirement compression rules.
- Phase 2 Greater Affix candidate ranges and frequency policy.
- Large charm `+1 skill tree` and proposed `+2 Greater skill tree` rarity math.
- No active game data implementation yet for this specific review task.

## Design Or Diff

- Main design: `docs/rare-item-rework-design-2026-05-18.md`
- Math summary for this review: `docs/ai-review/tasks/2026-05-19-0019-rare-charm-frequency-math/design.md`
- Relevant commits:
  - `d4390941` documented Greater Affix candidates and tighter ranges.
  - `1cf4fe13` documented charm Greater Affix scaling.

## Review Questions

1. Does the charm frequency proposal correctly preserve proportions when normal large charm `+1 skill tree` rows are raised to `frequency=10` and Greater `+2 skill tree` rows use `frequency=1`?
2. Is multiplying all existing charm affix frequencies by `5` the correct normalization if original class large charm skill rows are currently `frequency=2`?
3. Is the proposed exception for Warlock `+1 skill tree` large charm rows, currently `frequency=1` but proposed as `frequency=10`, mathematically and design-wise consistent?
4. Does the level compression rule stay consistent with Eric's intent that all levels are reduced by 30%?
5. Are the stated level 90 large charm prefix-pool totals correct: current total `279`, current skill frequency `45`, scaled existing total `1410`, normal skill frequency `240`, Greater skill frequency `24`, final total `1434`, normal skill share `16.74%`, Greater skill share `1.67%`?
6. Are there hidden D2R affix-selection mechanics that make this proportional-frequency reasoning incomplete or misleading?
7. Should small/medium charm rare-only pierce rows in group `307` also be scaled under this charm rule, or should they be excluded because they are special-purpose rare-only rows?
8. Should the design distinguish prefix and suffix pools explicitly for charm scaling?
9. Is this design ready to implement, or should Codex revise the math before editing `magicprefix.txt` / `magicsuffix.txt`?
