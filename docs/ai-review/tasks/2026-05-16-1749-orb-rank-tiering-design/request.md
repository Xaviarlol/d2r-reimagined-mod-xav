---
schema: ai-review-task-v1
id: 2026-05-16-1749-orb-rank-tiering-design
status: ready_for_claude
phase: design_review
round: 1
max_rounds: 3
created_by: codex
created_at: 2026-05-16T15:49:06Z
updated_at: 2026-05-16T16:01:50Z
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
lets prepare to introduce some changes to orbs. There will now be 3 types each of Orb of Assemblage and Orb of Converstion

Each orb will only work on their respective item base quality (eg. normal, exception, elite).
For example, Orb of Conversion I will only work on normal rare items and convert them to normal unique
Orb of Conversion II will only work on exceptional rare items and convert them to their exceptional unique
Orb of Conversion III will only work on elite rare items and covert them to their elite unqiue.

Same for Orb of Assemblage.

Rank 1 will have the same drop rate as the current orb of conversion / assemblage. Rank 2 will be roughly 3x rarer. Rank 3 will be roughly 6x rarer.

First time kill on bosses who drop them (baal, diablo I think?) will drop rank 1 as they currently do, but also have a chance to instead drop a rank 2 or rank 3 version (1 in 3 chance to drop Rank 2 instead of rank 1, 1 in 6 chance to drop rank 3 instead of rank 1. If that part is too hard, just let the bosses drop rank 1 as per normal (unchanged).
Keep the item codes for orb of assemblage and orb of conversion the same for rank 1. Add the new codes as ooaii for rank 2, and ooaiii for rank 3. If there is a character limit of 3, do oa2, oa3 etc.

This change will need to be reviewed by claude before implementing.
```

## Goal

Review the proposed design before Codex implements ranked Orb of Conversion and Orb of Assemblage behavior.

## Follow-up User Clarification

```text
regarding jewellery, can we restrict the output to plvl/ilvl? So for example rank 1 OOC can only make up to level 40, rank 2 to 70, rank 3 to 100?
```

## Follow-up Recipe Request

```text
also, please add to the design new recipe changes to support this change:
11x OOI + topaz = unchanged (OOC rank 1)
11x OOI + emerald = unchanged (OOA rank 1)
new recipe 3x OOC = 1x OC2
9xOOC = 1x OC2
3xOC2 = 1x OC3
Same pattern for assemblage version (OA2 and 3)
Update the reviewe package
```

## Phase

design_review

## Scope

- Item definitions for Orb of Conversion and Orb of Assemblage ranks.
- Cube recipes that convert rare items into unique or set items.
- Treasure classes that drop Conversion and Assemblage orbs.
- Item name/description strings.
- Documentation for new orb behavior and any D2R modding findings.

## Design Or Diff

See `design.md`. No gameplay/data implementation has been made yet.

## Review Questions

1. Does the proposed rank/tier behavior match Eric's request?
2. Are `bas`, `exc`, and `eli` cube input qualifiers the correct way to restrict normal, exceptional, and elite rare bases?
3. Is the proposed three-character code scheme safe and clear?
4. Does the proposed drop weighting preserve rank I's current relative drop rate while making rank II and III roughly 3x/6x rarer?
5. Is the proposed jewelry output-ilvl cap approach valid for limiting unique/set ring and amulet result pools?
6. Should rank II/III stack variants be added now, deferred, or avoided?
7. Are active/base files likely to need normalization around single-orb versus stacked-orb treasure classes?
8. Is the boss quest-drop tier-upgrade design safe enough to implement?
9. Is Codex's assumption that `9x OOC` / `9x OOA` should produce rank III correct, or should the user-written `9x OOC = 1x OC2` be treated literally?
