---
schema: ai-review-result-v1
task_id: 2026-05-21-0144-top50-greater-affix-redesign
round: 3
reviewer: claude
verdict: approved_with_notes
critical: 0
high: 0
medium: 2
low: 3
requires_codex_changes: false
---

# Claude Review

## Verdict

Approved with notes

## Summary

`code_review` of the top-50 Greater Affix redesign implementation. **All structural
validation gates pass cleanly: Greater row counts (201 prefix + 54 suffix = 255 ≈
50 logical families × per-tier emission), `itemstatcost.txt` max ID 487 with strict
sequential IDs 0..487, active/base byte-identical on all 4 file pairs, TSV column
widths match headers on all 4 files (0 bad rows), `spawnable=1 rare=1` on every
Greater row, level bands exactly 85/85/85 split across early/mid/late, no
`greater_m_*`/`greater_item_*`/`item_greaterAffixMarker`/`greater-affix-marker`
references remain anywhere, all 50 family markers defined and referenced, all 6 aura
params correctly resolve to verified Paladin skill IDs (98/114/115/120/122/123 with
no 126/Bash leftover).** The implementation faithfully executes the approved design.

The two MEDIUM notes are UX / cleanup items, not correctness bugs.

What I verified independently against the implementation files:

- **Row counts match summary:** 201 prefix Greater + 54 suffix Greater = 255 rows.
  All 255 are split evenly into 85 × 3 bands (early `level=50 maxlevel=65`, mid
  `level=66 maxlevel=80`, late `level=81 maxlevel=blank`). No `level<50` leftovers.
- **`itemstatcost.txt`:** 488 rows, max `*ID` = 487, strict sequential 0..487 with
  no gaps. Comfortably under the 510 ceiling, matches the design's ≤487 target.
- **Active/base sync:** `diff -q` returns empty for all 4 pairs (magicprefix,
  magicsuffix, itemstatcost, properties).
- **TSV shape:** magicprefix 40 cols × 1488 rows, magicsuffix 40 × 1010, itemstatcost
  52 × 488, properties 38 × 486. 0 rows with wrong column count in any file.
- **Cleanup verified:** Zero matches for `greater_m_|greater_item_|item_greaterAffixMarker|greater-affix-marker`
  in any of the 4 files.
- **Property cross-references:** 53 `ga_*` properties defined (50 family markers
  named `ga_<family>` + 3 hybrid wrappers `ga_h_*`). Every `ga_*` code referenced
  in `mod1code/mod2code/mod3code` exists as a property definition (empty
  set-difference). Every property's `stat<N>` reference resolves to a stat in
  `itemstatcost.txt`. No dangling references introduced by this diff.
- **Aura params (all 6 correct, no 126/Bash leftover):**

  | Greater family | mod2param (verified vs skills.txt) |
  |---|---:|
  | Greater Aureole Might | 98 ✓ |
  | Greater Aureole Holy Freeze | 114 ✓ |
  | Greater Aureole Vigor | 115 ✓ |
  | Greater Aureole Meditation | 120 ✓ |
  | Greater Aureole Fanaticism | 122 ✓ |
  | Greater Aureole Conviction | 123 ✓ |

  Aura level fixed at 4 (mod2min=4 mod2max=4). The pattern is two-slot: mod1 carries
  the per-family marker property (`ga_aureole_might` etc.), mod2 carries the raw
  `aura` gameplay stat with the resolved skill ID. Clean split.
- **Frequency formula spot-check (8 surviving families):**

  | Family | Late freq | Expected (`apex/10`) | Match |
  |---|---:|---:|---|
  | of Greater Quickness | 60 | 60 | ✓ |
  | of the Greater Magus | 60 | 60 | ✓ |
  | of Greater Evisceration | 88 | 88 | ✓ |
  | Greater Grandmaster's (att variant) | 4 | 4 | ✓ |
  | Greater Chromatic | 6 | 6 | ✓ |
  | of the Greater Elements | 24 | 24 | ✓ |
  | of the Greater Lich | 12 | 12 | ✓ |
  | of Greater Equilibrium | 48 | 48 | ✓ |
- **Phase 1 preservation verified by row-count invariance:** Non-Greater rows are
  byte-for-byte unchanged from `6dca8854`. Prefix non-Greater rows = 1287 in both
  current and pre-diff state; suffix = 956 in both. Phase 1 levels/levelreqs are
  preserved by construction since non-Greater rows weren't touched.
- **Sage's group-125-only check:** All 6 emitted Greater Sage's rows are in group
  125 (allskills). Zero group-204 (addxp) rows. Per design.
- **Hybrid wrappers (3 defined, 9 references):**

  | Hybrid | Func/stat composition | Used by | Justification |
  |---|---|---|---|
  | `ga_h_wraithly_weapon_dmg` | func7 + marker | 3 Greater Wraithly Weapon rows | 3 source mods (ED+Eth+Repair) |
  | `ga_h_wraithly_armor_ac` | item_armor_percent + marker | 3 Greater Wraithly Armor rows | 3 source mods (AC%+Eth+Repair) |
  | `ga_h_elements_res_cold_lvl` | item_resist_cold_perlevel + marker | 3 of the Greater Elements rows | Expanded to 3 mods (cold+fire+ltng per-lvl, see LOW-002) |

- **Pre-existing dangling refs (Codex correctly out-of-scoped):** 12 references to
  `Breaching-Affix1`/`Gelid-Affix1`/`Incendiary-Affix1`/`Magnetic-Affix1`/
  `Mystical-Affix1`/`Virulent-Affix1` (and the `-Affix2` versions) in group 307
  rows of `magicprefix.txt`. I confirmed each exists at `6dca8854` (pre-diff state),
  so they predate this implementation. See LOW-003.

## Review Questions

**Q1 — Implementation matches approved design?** Yes. The per-source-variant
emission policy (HIGH-001 from r01) produces 255 Greater rows from 50 logical
families — examples: Greater Arch-Angel's emits 9 rows across 3 source lvlreq tiers
(36, 57, 64), Greater Sage's emits 6 rows across 2 lvlreq tiers (43, 68), Greater
Aureole emits 18 rows (6 auras × 3 bands). All match the Round 2 clarification spec.

**Q2 — Broad/old Greater rows and `greater_m_*` wrappers safely removed?** Yes.
- 510 old prefix Greater rows removed, 201 new added (`-510 +201` diff).
- 399 old suffix Greater rows removed, 54 new added (`-399 +54`).
- Zero `greater_m_*` / `greater_item_*` / `item_greaterAffixMarker` references
  remain in any of the 4 modified TXT files.
- 72 old `greater_*` itemstatcost rows removed; IDs renumbered sequentially 0..487.

**Q3 — 50 marker stats under the 511 ID limit?** Yes. New max ID is 487, leaving
24 headroom under the 510 ceiling. The 50 family markers occupy contiguous IDs
between 438-487 (per `itemstatcost.txt`'s post-compaction layout). No risk of
hitting the cap with this implementation.

**Q4 — Active/base sync and TSV structure valid?** Yes. `diff -q` empty for all
4 pairs; TSV column-width check passes on all 4 files; header column counts match
expected (40/40/52/38).

**Q5 — Aura IDs correct and broken `mod1param=126` state gone?** Yes. All 6 aura
families use verified Paladin skill IDs from `skills.txt`. Zero `mod1param=126`
references anywhere; zero references to Bash on a Greater Aureole row.

**Q6 — Greater rows marked correctly?** Yes. 100% of Greater rows have
`spawnable=1 rare=1`, and 100% banded as exactly `(50/65)`, `(66/80)`, or
`(81/blank)`. The lvl=1 leftover bug class is impossible by construction.

**Q7 — Tooltip marker strategy safe to publish/playtest?** Yes structurally, with
two visual UX flags before live publish — see MEDIUM-001 (color choice) and
MEDIUM-002 (orphan JSON entries) below.

## Findings

### Critical
None.

### High
None.

### Medium

**MEDIUM-001 — Marker color is gold (`ÿc4`), not the v2-spec-recommended orange (`ÿc8`)**

- Where: `data/local/lng/strings/item-modifiers.json`. All 50 new family markers
  (`GreaterAffix_grandmasters`, `GreaterAffix_wraithly_weapon`, ...
  `GreaterAffix_aureole_vigor`) use color code `ÿc4` (gold) in every locale.
- Issue: The v2 colored-stats followup spec (`docs/greater-affix-colored-stats-
  followup-2026-05-20.md`) explicitly says:

  > "Color choice: `ÿc8` (orange) recommended — visually consistent with the
  > existing `** Greater Affix` marker. Other options: `ÿc4` gold (collides with
  > unique-item color), `ÿc;` purple. Eric's call but orange has precedent in this
  > mod."

  In-game, `ÿc4` gold is the color D2 uses for unique item header lines. With 50
  Greater family markers on rare items all displaying gold, a rare with a Greater
  affix will have a gold ribbon line that looks visually identical to a unique
  item's header. On a quick tooltip scan, that gold line could read as "this is a
  unique" rather than "this is a Greater rare."
- Impact: Pure UX/readability concern, not a correctness bug. Items will still drop
  correctly and the marker will display. The risk is player confusion at-a-glance.
- Recommendation: Change the color code to `ÿc8` (orange) across all 50 markers
  in `item-modifiers.json`. This is a one-line global swap per locale entry, no
  data-side changes needed (the marker stat doesn't care about the color, only the
  string content). If Eric prefers gold, document the deviation from the v2 spec
  in the implementation summary so future redesigns don't second-guess.
- Blocks live publish: No, but worth resolving first.

**MEDIUM-002 — 72 orphan `GreaterAffix_*` entries remain in `item-modifiers.json`**

- Where: `data/local/lng/strings/item-modifiers.json` contains 122 keys starting
  with `GreaterAffix_`: 50 are the new family markers, the other 72 are dead
  strings from the prior `greater_*` clone experiment (e.g.
  `GreaterAffix_item_armor_percent_Modstr2v`,
  `GreaterAffix_passive_cold_pierce_Moditemenrescoldsk`).
- Issue: The 72 orphan entries' referencing stats (the `greater_*` clones) were
  removed from `itemstatcost.txt` by this implementation, so no stat references
  these strings any more. D2 only loads strings referenced by stats, so the
  orphans are harmless at runtime — but they're dead state in a hot-loaded
  localization file.
- Impact: ~72 extra JSON entries (estimated ~20-30 KB at 12 locales each). No
  runtime correctness impact. Inflates the localization file unnecessarily.
- Recommendation: Add an explicit JSON cleanup step to the implementation script
  (or a follow-up commit): for every JSON key matching `GreaterAffix_*` where the
  key is not one of the 50 active family markers, remove the entry. Validate by
  ensuring every remaining `GreaterAffix_*` key has a corresponding stat in
  `itemstatcost.txt` with that key in `descstrpos`/`descstrneg`/`descstr2`.
- Blocks live publish: No, but recommended cleanup before final commit.

### Low

**LOW-001 — Greater Aureole Might `levelreq=5` may be too low for a chase affix**

- Where: `data/global/excel/magicprefix.txt` rows 1472-1474 (Greater Aureole
  Might): `level=50/66/81 levelreq=5`.
- Issue: The source `Aureole` row at line 602 has `lvlreq=5` (Might at the
  low-level entry), so per the design's rule "set `levelreq` to the current
  non-Greater apex `levelreq`," Greater Aureole Might inherits `levelreq=5`. A
  player at level 5 can wear an item rolling Greater Aureole Might. Other Greater
  Aureoles span lvlreq 20-38, so Might is the outlier.
- Impact: Greater Might can be a level-5-accessible "chase" affix on lvl 50+
  items. Either intentional (early access to chase affixes for character growth)
  or a refinement candidate.
- Recommendation: Decide if Greater Might's levelreq should be raised to match
  the other aura tiers (e.g. 20-30) or kept at 5 as deliberate low-level
  accessibility. Apply consistently to all 6 aura families if changing.
- Blocks live publish: No.

**LOW-002 — Greater Elements expands source's 2-mod payload to 3 mods**

- Where: `data/global/excel/magicsuffix.txt` rows 2486-2488 (of the Greater
  Elements): `mod1=ga_h_elements_res_cold_lvl mod2=res-fire/lvl mod3=res-ltng/lvl`.
- Issue: The source `of the Elements` affix (suffix line 240-243) carries only
  cold and fire per-level resists — `mod1=res-cold/lvl mod2=res-fire/lvl`, no
  lightning. The Greater Elements implementation expands to all 3 elements
  (cold+fire+lightning per-level), which is per the design table ("Cold/Fire/
  Lightning Resist") but is a deliberate scope expansion beyond the source row.
- Impact: Greater Elements is stronger than a `× 1.X scaled` version of source
  Elements — it now covers a third element the source never did. The `ga_h_elements_res_cold_lvl`
  hybrid wrapper was necessitated by this 3-mod expansion (justifying the third
  hybrid Codex defined beyond the design's named pair).
- Recommendation: Confirm with Eric this expansion was intended. If yes, no
  action — and consider updating the design table to flag the scope expansion
  explicitly. If no, remove `mod3=res-ltng/lvl` and drop the hybrid in favor of
  the simple marker pattern.
- Blocks live publish: No.

**LOW-003 — 12 pre-existing dangling property refs in group 307 (not introduced)**

- Where: `data/global/excel/magicprefix.txt` group 307 rows reference
  `Breaching-Affix1/2`, `Gelid-Affix1/2`, `Incendiary-Affix1/2`,
  `Magnetic-Affix1/2`, `Mystical-Affix1/2`, `Virulent-Affix1/2` — none of which
  exist in `properties.txt`.
- Issue: These 12 dangling references existed at `6dca8854` before this
  implementation (verified via `git show`). Out of scope for this review but
  worth carrying forward as a separate cleanup task — they represent silently
  broken rows that may have been intentionally placeholder.
- Impact: D2 likely fails silently when it encounters a dangling property in a
  mod slot (the affix probably doesn't roll those mods). Not a crash risk but
  also not behaving as authored.
- Recommendation: File as a separate `bug_fix` review task. Either define the
  missing properties (if the elemental affix expansion was incomplete) or
  remove/rename the rows referencing them.
- Blocks live publish: No.

## Validation Checks

- **Original user request reviewed:** Yes — *"create a plan to do them for review
  by claude. You will need to reweight all frequencies now that you are removing
  the other GA's..."*. The implementation reweights via the formula consistently
  (verified 8/8 spot-checks match `late_freq = max(1, round(apex_freq/10))`).
  Eric's original ask is satisfied.
- **Diff reviewed:** `diff.patch` (6221 lines, 14 hunks across 9 game-data files
  + script + summary). The bulk of the diff is the magicprefix/suffix Greater row
  swap and the itemstatcost ID compaction.
- **Independent verification (this round, not just summary trust):**
  - Greater row counts: 201 prefix + 54 suffix (matches summary) ✓
  - Level bands: 85 early + 85 mid + 85 late = 255 (matches row count) ✓
  - itemstatcost max ID: 487, sequential 0..487, no gaps ✓
  - active/base diff-empty for 4 pairs ✓
  - TSV column-width on all 4 files: 0 bad rows ✓
  - Cleanup grep: 0 matches for old greater_m_/greater_item_/item_greaterAffixMarker ✓
  - Property cross-reference: every `ga_*` mod-column code defined as a property ✓
  - Aura param table: 6/6 IDs match `skills.txt` ✓
  - Non-Greater row count invariance vs `6dca8854` (1287 prefix, 956 suffix) ✓
  - Sage's group-125-only ✓
- **Live publish risk:** `live_publish_allowed: false`. The implementation is
  not yet on the live folder. Recommend MEDIUM-001 (color) and MEDIUM-002 (JSON
  cleanup) be addressed before live publish, but neither blocks. The launch-test
  discipline from r02 remains the hard gate: deploy, launch D2R, drop rares,
  confirm no crash, confirm marker tooltip line renders correctly before commit.

## Codex Action Items

1. **(MEDIUM-001)** Change marker color from `ÿc4` (gold) to `ÿc8` (orange)
   across all 50 family markers in all 12 locales of `item-modifiers.json`. One-
   line global swap, no data-file changes. OR: document the deliberate deviation
   from the v2 spec in the implementation summary if gold is preferred. Eric's
   call.
2. **(MEDIUM-002)** Add a JSON-orphan cleanup pass to remove the 72 dead
   `GreaterAffix_*` entries from `item-modifiers.json`. Validate by ensuring
   every remaining `GreaterAffix_*` key is in some stat's `descstrpos`/
   `descstrneg`/`descstr2` column in `itemstatcost.txt`.
3. **(LOW-001)** Decide Greater Aureole Might's `levelreq` — keep at 5 (source
   apex) or raise to match other aura tiers' typical 20+. Apply consistently.
4. **(LOW-002)** Confirm Greater Elements 3-mod expansion (cold+fire+ltng) was
   intended. If yes, no action. If no, drop `mod3=res-ltng/lvl` and the
   `ga_h_elements_res_cold_lvl` hybrid.
5. **(LOW-003)** File a separate `bug_fix` review task for the 12 pre-existing
   dangling refs in group 307. Out of scope for this implementation.

After MEDIUM-001 and MEDIUM-002 are addressed (or explicitly waived), proceed
with the launch-test gate before live publish.

## Suggested Game-Launch Test Plan

1. Deploy active TXT/JSON files to the live game folder (XavReimagined).
2. Launch D2R, enter a game, gamble or drop several rares at varied item levels
   (lvl 50, lvl 66, lvl 81+ for the band coverage).
3. Confirm:
   - No crash on game launch.
   - No crash on item generation or item pickup.
   - The "Greater Affix: <family>" tooltip line renders on a Greater roll, in
     the chosen color.
   - At least one Greater Aureole rolls with the correct aura on hover (Might,
     Fanaticism, etc.) and at level 4.
   - Multiple distinct Greater families roll across the test session (e.g.
     Quickness, Grandmaster's, Lich, Aureole).
4. If any crash: revert the entire implementation diff atomically (single
   `git revert`) and debug locally. Do not try to fix-forward on a crashed
   state — the prior `44b2c3b0` failure mode is the cautionary precedent.
5. After 30-minute test session with no crashes, commit and publish.
