---
schema: ai-review-task-v1
id: 2026-05-16-2115-orb-rank-implementation
status: ready_for_claude
phase: code_review
round: 1
max_rounds: 3
created_by: codex
created_at: 2026-05-16T21:15:00Z
updated_at: 2026-05-16T21:54:34Z
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

regarding jewellery, can we restrict the output to plvl/ilvl? So for example rank 1 OOC can only make up to level 40, rank 2 to 70, rank 3 to 100?

also, please add to the design new recipe changes to support this change:
11x OOI + topaz = unchanged (OOC rank 1)
11x OOI + emerald = unchanged (OOA rank 1)
new recipe 3x OOC = 1x OC2
9xOOC = 1x OC2
3xOC2 = 1x OC3
Same pattern for assemblage version (OA2 and 3)
Update the reviewe package

yes, 9x ooc = oc3 and 3x oc2 = oc3

while we wait for your review, I just realized we also have to make oc2 and oc3, oa2 and oa3 have a stackable area in the stash (stacking added in diablo 2R v3

claude review is complete

go ahead
```

## Goal

Review the implemented first pass of ranked Orb of Conversion / Orb of Assemblage behavior after the approved design review.

## Phase

code_review

## Scope

- Adds loose rank II/III orb item rows in active/base `misc.txt`.
- Renames rank I display strings to `Orb of Conversion I` / `Orb of Assemblage I` and adds rank II/III names/descriptions.
- Replaces armor/weapon conversion and assemblage recipes with normal/exceptional/elite tiered variants.
- Keeps amulet/ring conversion and assemblage recipes unchanged for now because jewelry `lvl` pool gating is still unverified.
- Adds orb promotion recipes:
  - `3x ooc -> oc2`
  - `9x ooc -> oc3`
  - `3x oc2 -> oc3`
  - `3x ooa -> oa2`
  - `9x ooa -> oa3`
  - `3x oa2 -> oa3`
- Adds rank II/III treasure classes, generic Jewelry Orbs weights, and boss quest selectors.
- Normalizes active/base orb treasure-class structure to loose orb codes rather than base-only normal/stack split rows.
- Adds HD item asset bindings for `oc2`, `oc3`, `oa2`, and `oa3`, reusing existing Conversion/Assemblage orb assets.
- Adds HD stash stack slot widgets for the new rank II/III orb codes in both keyboard/mouse and controller stash layouts, packed into existing top-row free space so they do not overlap the normal stash grid underneath.
- Fixes English string color-control prefixes to use the actual `0xff` character so the orange item names and gray descriptions render correctly.
- Updates `docs/modding-findings.md`.

## Design Or Diff

- Approved design review task: `docs/ai-review/tasks/2026-05-16-1749-orb-rank-tiering-design/`
- Implementation diff: `diff.patch`

## Known Implementation Gate

Jewelry rank tiering is intentionally not implemented in this patch. The old `amu`/`rin` conversion and assemblage recipes remain rank-I-only until we verify that cube output `lvl` gates the unique/set jewelry selection pool before output selection.

## Review Questions

1. Does the implementation match the approved non-jewelry scope and Eric's request?
2. Are `misc.txt`, `cubemain.txt`, and `treasureclassex.txt` active/base changes synchronized where needed?
3. Are TSV structures safe and free of malformed rows?
4. Are the `bas` / `exc` / `eli` recipe qualifiers and outputs correct for armor/weapons?
5. Are `AdvancedStashStackable=1`, HD stash slot widgets, HD item asset mappings, and string keys correct for `oc2`, `oc3`, `oa2`, and `oa3`?
6. Are the generic and boss quest treasure-class weights correct?
7. Are the follow-up live smoke-test fixes complete and safe to keep published?

## Local Validation Already Run

- Active/base TSV column-count validation:
  - `misc.txt`: 176 columns, 282 rows.
  - `cubemain.txt`: 106 columns, 15690 rows.
  - `treasureclassex.txt`: 39 columns, 1553 rows.
- Verified one copy of each new promotion recipe in active and base `cubemain.txt`.
- Verified no legacy active/base treasure-class rows remain for `Jewelry Orbs Single`, `Jewelry Orbs Stack`, or `* Orb (Normal)`.
- Verified one copy of each managed orb treasure class in active and base `treasureclassex.txt`.
- Parsed `item-names.json` and verified one copy of each new rank/name/description key with no duplicate string ids.
- Parsed `item-names.json`, `items.json`, and both HD stash layout JSON files.
- Verified `ooc`/`ooa`/rank II/III English orb names and descriptions begin with the actual `0xff` color-control character.
- Verified HD item asset mappings and HD stash slot widgets exist for `oc2`, `oc3`, `oa2`, and `oa3`.
- Verified the new rank II/III stash slot rectangles sit above the normal stash grid in both keyboard/mouse and controller layouts.
