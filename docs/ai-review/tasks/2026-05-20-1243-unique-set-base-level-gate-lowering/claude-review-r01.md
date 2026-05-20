---
schema: ai-review-result-v1
task_id: 2026-05-20-1243-unique-set-base-level-gate-lowering
round: 1
reviewer: claude
verdict: approved
critical: 0
high: 0
medium: 0
low: 0
requires_codex_changes: false
---

# Claude Review

## Verdict
Approved

## Summary

`code_review` of commit `34e764f2 "Lower unique set levels to base item gates"`. **The
implementation is byte-perfect and matches the intent exactly — clean approval with no
findings.**

I built an independent base-item code→level map from `weapons.txt` (525 codes) and
`armor.txt`, then ran row-by-row column-level checks against the active files (post-change)
and the base_ref (`81afcc70`, pre-change). Every claim Codex made in the validation summary
holds up under independent verification:

- **394 rows changed total** — 333 unique (matches Codex's `unique: changed 333`) + 61 set
  (matches `set: changed 61`).
- **100% of changes are lowerings** — 333 lowered, 0 raised in `uniqueitems.txt`; 61 lowered,
  0 raised in `setitems.txt`. Zero rows had `lvl_new >= lvl_old`.
- **0 non-`lvl` columns changed** — across all 394 changed rows, the *only* column that
  differs is the `lvl` column (col 12 in `uniqueitems.txt`, col 13 in `setitems.txt`).
  `lvl req`, `code`, every mod, every property — all untouched.
- **Every `proposed_lvl` in the applied TSV equals the base item's level** — 394/394 TSV
  rows verified against the code→level map; 0 base-level mismatches.
- **Completeness: zero misses** — there is not a single remaining weapon/armor unique or
  set in the active files where `lvl > base_level`. Every row that needed lowering got
  lowered.
- **Active/base byte-identical** — `diff -q` returns empty for both
  `uniqueitems.txt` and `setitems.txt`.
- **Restricted to weapon/armor ladder bases** — the applied-changes TSV's `category` × `tier`
  distribution is exactly:
  - armor / normal 90, exceptional 24, elite 65 (subtotal 179)
  - weapon / normal 67, exceptional 56, elite 92 (subtotal 215)
  - **Total 394; no jewelry/charm/jewel/misc rows changed.**
- **158 unique + 39 set rows correctly skipped** — these are the rows whose `code` is not
  in `weapons.txt` / `armor.txt` (rings, amulets, jewels, charms, quest items, sunder
  charms, etc.). The user's "no-ladder misc/jewellery/charm/jewel" exclusion is honored.

## Review Questions

**Q1 — Did Codex only lower `lvl` values and avoid raising any rows?**
Yes — verified absolute. 333 unique + 61 set = 394 row changes; every single one is a
strict lowering (`lvl_new < lvl_old`). Zero raises. Zero same-value writes. And the
only column touched in any changed row is the `lvl` column itself.

**Q2 — Was the change correctly restricted to weapon/armor rows with normal/exceptional/elite
ladders?**
Yes. All 394 changed rows have `category ∈ {armor, weapon}` and `tier ∈ {normal,
exceptional, elite}` per the applied-changes TSV. No jewelry, no charms, no jewels, no
quest items. The 158 unique + 39 set rows whose codes are not in `weapons.txt` / `armor.txt`
are correctly skipped.

**Q3 — Are active/base files synchronized?**
Yes. `diff -q data/global/excel/uniqueitems.txt data/global/excel/base/uniqueitems.txt`
returns empty (byte-identical), and same for `setitems.txt`. Both pairs are exactly
synchronized.

**Q4 — Any D2R data risks?**
No structural or save-safety risks. The change is the cleanest possible kind of edit:
single-column lowering on 394 of ~1900 total rows. Specifically:

- **Column counts unchanged** — 75 cols in `uniqueitems.txt`, 102 cols in `setitems.txt`.
- **Save safety** — characters with already-dropped unique/set items keep them; the `lvl`
  column only affects future drop eligibility, not stored item data.
- **Equip gate unchanged** — `lvl req` (the character-level requirement to wield) was not
  touched. A level-3 character finding a newly-eligible unique on a Leather Armor base
  still cannot equip it until their character level meets `lvl req`. Trading economy
  implication is mild and is the explicit intent of the change.
- **Affix/Greater system unaffected** — uniques/sets carry hard-coded properties, not
  rolled affixes, so this change has zero interaction with the Phase 1 / Phase 2 rare-affix
  rework that just shipped.
- **No tier/quality cascade impact** — `uniqueitems.txt` `lvl` is a gating filter, not a
  quality probability; lowering it doesn't change how often uniques drop relative to sets
  or rares, only which items in the unique pool are eligible at a given monster level.

The only player-visible effect is the intended one: a unique whose base item drops at low
monster levels (e.g. Vidala's Ambush on `lea` Leather Armor, base level 3) can now drop in
the same zones that drop the base, instead of being artificially gated higher.

## Findings

### Critical
None.

### High
None.

### Medium
None.

### Low
None.

## Validation Checks

- **Original user request reviewed:** Yes. *"only change ones that will result in lowering
  the level — do not change ones that are already the same or lower than the base item
  level."* The implementation does exactly that (394 lowerings, 0 raises, 0 no-op writes,
  0 already-correct rows touched).
- **Diff scope:** 4 TXT files (active + base for unique and set), the applied-changes TSV,
  and the queue request. No other code or data touched. `git diff --shortstat` is `788
  insertions / 788 deletions` — exactly `394 × 2` (one `-` and one `+` per changed row),
  confirming no rows were added or removed.
- **Independent re-verification:**
  - Code→level map built from `weapons.txt` (col 4 = `code`, col 32 = `level`) +
    `armor.txt` (col 20 = `code`, col 15 = `level`) — 525 entries.
  - 394/394 TSV `proposed_lvl` equal `base_level` from the map. ✓
  - Active vs base_ref column-level diff: only `lvl` (col 12 unique / col 13 set) differs
    on changed rows; zero other columns touched.
  - Completeness sweep: 0 remaining weapon/armor unique/set rows with `lvl > base_level`. ✓
- **Live publish risk:** `live_publish_allowed: false`; design-only review. The change is
  structurally safe to publish whenever Eric chooses.

## Suggested Follow-up Tests (in-game smoke checks before live publish)

Nothing strictly required, but a quick smoke pass is cheap insurance:

1. **Low-level unique drop** — kill early-Act-1 monsters that drop the relevant base items;
   over many runs confirm previously-gated uniques (e.g. Vidala's Ambush on Leather Armor,
   Hwanin's Blessing on its base) can now drop where their base drops.
2. **Equip gate intact** — pick up a newly-eligible unique with a low base level; confirm
   the tooltip still shows the original `lvl req` and the item cannot be equipped below
   that character level.
3. **High-level uniques unchanged** — uniques on high-base-level items (where `lvl` was
   already at or below `base_level`) should be untouched; verify a couple still drop at
   their original gates.
4. **Active/base parity** — the byte-identical check is structural; the game pulls from
   `data/global/excel/` for the active mod, so both Reign of the Warlock and the base mode
   behave consistently if anyone switches.
