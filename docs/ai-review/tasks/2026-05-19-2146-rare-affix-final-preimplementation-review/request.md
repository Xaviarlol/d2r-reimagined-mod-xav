---
schema: ai-review-task-v1
id: 2026-05-19-2146-rare-affix-final-preimplementation-review
status: claude_reviewed
phase: re_review
round: 2
max_rounds: 3
created_by: codex
created_at: 2026-05-19T21:46:38Z
updated_at: 2026-05-20T00:14:28Z
repo: C:\Dropbox\AI projects\d2r\d2r-reimagined-fresh
branch: xav-custom
base_ref: 43e3acef
head_ref: xav-custom
original_user_request_included: true
live_publish_allowed: false
last_review: claude-review-r02.md
last_verdict: approved
last_response: codex-response-r01.md
claimed_by: claude
claimed_at: 2026-05-20T00:09:40Z
reviewed_at: 2026-05-20T00:14:28Z
---

# Review Request

## Original User Request

```text
regarding greater affixes:
There should only be 1 greater affix per category, for exampe Greater Cruel. But to make it rarer to be found on lower level rares, create 3 Greater Cruel affixes with varying frequency:
Early: Level 50-65. Freq=1
Mid: Level 66-80. Freq=2
Late: Level 81-100. Freq=3
All 3 of them will be dmg% 350-400

The late one should still be around 10x rarer than the normal Cruel normal affix, which means the early one would be 30x rarer. So you will have to reweight freq proportionaly for every affix I would think. Am I wrong? So anything with current freq=1 would need to be freq>1 otherwise they will be as common as greater. I would estimate they would need to be something like freq=3. And then normal junk affixes will all need their freq proportionally increased.

Dont forget that the lowering of higher level affixes appearing on lower level rares is for ALL affixes, not just greater. So you actually have quite a big reweighting task for freq. Update the documents with your new understand, and show before and after numbers for some examples, such as Before can only appear on level X, now can appear on level Y proposed. 

There are two ways to make them appear on lower level items but make it rarer if the item is lower level, 1) is how we did it with greater affixes, or 2) Make the total pool of available affixex bigger on lower level items which incude a lot of junk affixes but reduce them on higher level rares

so i think we should split this work in to 2 phases., 1. Stretch the level requirements of all affixes for rare items so that they can appear earlier, but with lower chance for better ones on lower level items 2) implement greater affixes to eavh affix family. For phase 1, we will scan all of the top affixes for each family and add a early and late frequency. Early = 2x rarer. Dont bother with the lower affixes. So best affixes have 2 splits and greater have 3

/goal go through all affixes and make ure you capture every apex affix for each family and then draft a full list of greater affixes with their effective chance to spawn on an item

/goal you didnt do what I said then. I said to make greater affixes 10x rarer than their current apex. You need to redo all the frequency math. Afterwards, compare the before and after probability (using the simple total affixes available divided by freq for each affix before and after our overhaul). The % chance should be virtually identitcal for all affixes before and after the changes. This will be a good sanity check to ensure the main objective of not changing the proportion of rarity for everything except greater affixes. Do you agree that this test will prove your frequency math?

I just realized that we probably dont want to be increasing MAX LEVEL, only level and reqlevel. Otherwise it actually makes it easier for rares overall to be better. What do you think?

yes, revert the maxlevel back to original in our plan.

are there any new affixes you added with missing level entries? Except maxlevel (since all new affixes are powerful they dont have a maxlevel)

ok a final review for claude and then we will implement

keep 3 band greater model, each max level should finish where the next one begins. levelreq for greater affixes needs to copy the same levelreq as its apex affix, minus the 15% reduction we did to all affixes
```

## Goal

Final pre-implementation review of the rare-affix overhaul before Codex edits `data/global/excel/magicprefix.txt`, `data/global/excel/magicsuffix.txt`, and their base copies.

This task supersedes:

- `docs/ai-review/tasks/2026-05-19-1339-rare-greater-affix-full-audit/request.md`
- `docs/ai-review/tasks/2026-05-19-1700-phase1-maxlevel-policy/request.md`

## Scope

Primary design and memory files:

- `docs/rare-item-rework-design-2026-05-18.md`
- `docs/modding-findings.md`
- `docs/session-handoff-2026-05-18.md`

Greater-affix audit and math files:

- `scripts/audit_rare_affix_apexes.py`
- `docs/rare-greater-affix-apex-audit-2026-05-19.md`
- `docs/rare-greater-affix-chance-table-2026-05-19.tsv`
- `docs/rare-greater-affix-probability-sanity-2026-05-19.tsv`
- `docs/rare-greater-affix-scope-validation-2026-05-19.tsv`
- `docs/rare-greater-affix-expanded-candidates-2026-05-19.tsv`

Phase 1 level/requirement comparison files:

- `scripts/generate_affix_level_change_data.py`
- `docs/affix-level-requirement-changes-2026-05-19.tsv`
- `docs/affix-top-split-preview-2026-05-19.tsv`
- Workbook outside repo for user viewing: `C:\Dropbox\AI projects\d2r\outputs\affix-level-requirement-changes\affix-level-requirement-changes-2026-05-19-maxlevel-preserved.xlsx`

Source data files for reference only in this review:

- `data/global/excel/magicprefix.txt`
- `data/global/excel/magicsuffix.txt`
- `data/global/excel/base/magicprefix.txt`
- `data/global/excel/base/magicsuffix.txt`

No game-data TXT implementation has been made for this rare-affix overhaul yet. No live publish is authorized by this task.

## Current Plan

Phase 1, existing affixes:

- Lower every existing affix `level` by 30%, preserving relative ordering across an affix family.
- Lower every existing affix `levelreq` by 15%.
- Preserve every existing row's `maxlevel`.
- Do not compress existing weak-affix `maxlevel` values, because that would shrink the weak-affix pool and make high-level rares cleaner than intended.
- For top normal affixes only, create an earlier duplicate row when needed. The early duplicate should be lower chance and should use `maxlevel = original_top_level - 1`; the original top row remains the late/high-level version.

Phase 2, Greater affixes:

- Add a Greater version for each confirmed apex family.
- Greater affixes should be approximately 10x rarer than the current apex affix for the same item scope.
- Keep the 3-band Greater model. Bands are adjacent and non-overlapping: Early `50-65`, Mid `66-80`, Late `81+`.
- The current audit scales existing affix frequencies by 10 and derives synthetic per-item-scope Greater weights from the apex rows, rather than assuming a single global `freq = 1` works everywhere.
- Greater frequency preserves the Early/Mid/Late `1 / 2 / 3` ratio but derives actual weights from the source apex: Early `round(F / 3)`, Mid `round(2F / 3)`, Late `F`, each minimum `1`.
- Greater `levelreq` copies the source apex `levelreq` after the same 15% reduction used by Phase 1.
- Existing affix proportions should remain effectively identical after the frequency scaling, excluding the unavoidable probability mass taken by new Greater rows.
- Whole-file frequency scaling includes `rare=0` rows too, because magic and rare rows share the same files and the user is fine with this affecting magic items.
- Group `307` rare-only elemental pierce remains special-purpose and should not be blindly charm-scaled because it shares rows across charms and non-charm gear.

Resolved design point:

- Eric explicitly chose the 3-band Greater model.
- Each band's `maxlevel` should finish immediately before the next band begins.
- Greater `levelreq` should copy the compressed source apex requirement, not the band level.

## Current Checks

- Existing active/base `magicprefix.txt` and `magicsuffix.txt` rows currently have zero missing `level` values and zero missing `levelreq` values.
- `docs/affix-level-requirement-changes-2026-05-19.tsv` currently has zero proposed `maxlevel` deltas for existing rows.
- `scripts/audit_rare_affix_apexes.py` now generates expanded 3-band Greater candidate rows with explicit `levelreq` values copied from the source apex after the global 15% reduction.
- `docs/rare-greater-affix-expanded-candidates-2026-05-19.tsv` currently has 7605 expanded rows and zero missing Greater `levelreq` values.
- `docs/rare-greater-affix-scope-validation-2026-05-19.tsv` currently has 1430 scope checks with max ratio delta 0 in the generated model.
- `docs/affix-top-split-preview-2026-05-19.tsv` previews the top-affix split rows: convert existing apex row to early plus add late duplicate.

## Round 2 Changes

- Added `codex-response-r01.md`.
- Accepted Claude's two Medium findings and both Low findings.
- Eric explicitly confirmed the 3-band Greater model.
- Greater bands are now documented as adjacent/non-overlapping: Early `50-65`, Mid `66-80`, Late `81+`.
- Greater frequency uses the source apex frequency while preserving the `1 / 2 / 3` ratio: Early `round(F / 3)`, Mid `round(2F / 3)`, Late `F`, with a minimum of `1`.
- Greater `levelreq` now copies the source apex `levelreq` after the 15% reduction. It does not copy the Greater band's `level`.
- The audit now writes `docs/rare-greater-affix-expanded-candidates-2026-05-19.tsv`.
- The phase 1 generator now writes `docs/affix-top-split-preview-2026-05-19.tsv`.
- `docs/rare-item-rework-design-2026-05-18.md`, `docs/modding-findings.md`, and `docs/session-handoff-2026-05-18.md` were updated to preserve this policy.

## Review Questions

1. Does the final two-phase plan preserve rare affix proportions correctly for existing affixes?
2. Is preserving existing `maxlevel` correct for Phase 1, with `maxlevel` only used on intentionally-created early duplicate top-affix rows?
3. Does the updated 3-band Greater policy satisfy the user's decision that each band should end where the next begins?
4. Does the updated Greater `levelreq` policy correctly copy the source apex `levelreq` after the 15% reduction?
5. Are the chance, probability sanity, and scope-validation TSVs sufficient evidence that Greater affixes are 10x rarer than their current apex rows for each item scope?
6. Does the current apex coverage miss any important top affix families, especially cross-scope rows, charms, class skills, damage reduction %, ethereal/self-repair, or weapon-only hybrid families?
7. Are there any implementation blockers before Codex edits `magicprefix.txt`, `magicsuffix.txt`, and the base copies?

## Requested Output

Please write `claude-review-r02.md` in this same task folder.

Use the usual review structure:

- Verdict: `approved`, `needs_fixes`, or `blocked_needs_user`
- Findings ordered by severity
- Specific file references and row/group examples where possible
- Direct recommendations for any math, scope, level, reqlevel, maxlevel, or frequency corrections needed before implementation
