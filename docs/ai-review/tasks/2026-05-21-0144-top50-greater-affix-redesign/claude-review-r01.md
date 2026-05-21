---
schema: ai-review-result-v1
task_id: 2026-05-21-0144-top50-greater-affix-redesign
round: 1
reviewer: claude
verdict: approved_with_notes
critical: 0
high: 1
medium: 3
low: 3
requires_codex_changes: false
---

# Claude Review

## Verdict

Approved with notes

## Summary

`design_review` of the top-50 Greater Affix redesign plan after the `freq=999999` test
was reverted by `6dca8854`. **The overall direction is sound:** the one-marker-per-family
strategy materially reduces `itemstatcost.txt` ID pressure compared to the 72 cloned
`greater_*` stats currently sitting at IDs 439-510, the row-rebuild-from-current strategy
correctly preserves Phase 1 levels/levelreqs, and the targeted curation (Grandmaster's,
Wraithly, Godly, Aureole auras, class-skill prefixes, elemental damage/pierce, etc.) is
internally consistent with the "elite gamer" intent. The frequency formula `late = apex/10,
mid = late*2/3, early = late/3` already matches the current Greater frequencies for surviving
families exactly — I verified 11 families produce 0-row deltas against the current file.

What I verified independently against the repo:

- **Row counts match design's claims.** Current `magicprefix.txt` has 510 Greater rows,
  `magicsuffix.txt` has 399 Greater rows — 909 total, matching the design's "909 rows
  collapsed into ~303 families" figure (the audit's family TSV has 304 rows, 1-off from
  the design text but immaterial).
- **`itemstatcost.txt` pressure is real.** 511 data rows (lines 2-512), max `*ID` is 510,
  72 `greater_*` clones already exist (IDs 439-510), plus 1 `item_greaterAffixMarker` at
  ID 438. There is no headroom — the next ID would be 511, which the prior `44b2c3b0`
  experiment hit and crashed. Deleting the 73 prior-experiment stats and adding 50 family
  markers nets -23 IDs, taking the post-redesign max from 510 to ~487. Comfortable.
- **Active/base are byte-identical right now** for all four affected file pairs
  (magicprefix, magicsuffix, itemstatcost, properties). `diff -q` returns empty. The
  restore commit `6dca8854` kept this invariant.
- **Frequency formula is already correct.** Verified `apex_freq/10 → late_freq` for 11
  surviving families:

  | Family | Source apex | apex_freq | Formula late | Current late | Match |
  |---|---|---:|---:|---:|---|
  | of Quickness | suffix 420 | 600 | 60 | 60 | ✓ |
  | of the Magus | suffix 481 | 600 | 60 | 60 | ✓ |
  | of Alacrity | suffix 417 | 720 | 72 | 72 | ✓ |
  | of Speed | suffix 403 | 480 | 48 | 48 | ✓ |
  | of Equilibrium | suffix 410 | 480 | 48 | 48 | ✓ |
  | of Deflecting | suffix 477 | 760 | 76 | 76 | ✓ |
  | of the Elements | suffix 243 | 240 | 24 | 24 | ✓ |
  | of the Four Seasons2 | suffix 250 | 120 | 12 | 12 | ✓ |
  | of the Lich | suffix 158 | 120 | 12 | 12 | ✓ |
  | of Evisceration | suffix 24 | 880 | 88 | 88 | ✓ |
  | of Transcendence dmg-min | suffix 49 | 240 | 24 | 24 | ✓ |

- **Drift claims independently verified.** Prefix lines 1301-1303 currently named
  `Greater Grandmaster's` carry `mod1=greater_m_dmg% mod2=greater_ethereal
  mod3=greater_rep-dur` — a Wraithly1 payload pasted onto a Grandmaster's name. Confirmed.
  Lines 1307-1309 named `Greater Godly` carry the same Wraithly armor payload (`ac% +
  ethereal + rep-dur`). Confirmed. The redesign's family split (#1 Greater Grandmaster's
  for ED+AR, #2 Greater Wraithly Weapon for ED+Eth+Repair, #3 Greater Wraithly Armor for
  AC%+Eth+Repair, #4 Greater Godly for AC%+DR%) cleanly resolves both drifts.
- **Audit `lvl=1` defects are real.** Confirmed `Greater Sage's` line 1700 has
  `lvl=1 lvlreq=39` — this row would roll on level-1 items and break the early-band
  level-50 gate. The redesign's "rebuild from current non-Greater rows" approach will
  naturally fix these since the source rows have correct levels.
- **Aura source has 16 distinct aura skill IDs.** `Aureole` rows currently use mod1param
  values 98-126 across 16 different paladin auras at varying lvl/lvlreq tiers. The
  current sole Greater Aureole row uses `aura/126/4-4`. The 6 chosen Greater auras
  (Might/Fanaticism/Conviction/Holy Freeze/Meditation/Vigor) each need their correct
  aura skill ID resolved from this source list — this isn't shown in the design.
- **Marker stat template exists.** Existing `item_greaterAffixMarker` (ID 438) uses
  `descpriority=999 descfunc=19 Save Bits=4` — the right shape to clone for the 50
  family markers. No new descfunc work required.

## Review Questions

**Q1 — Top-50 list matches "elite gamer" intent?**

Yes, with one ambiguity. The chosen families are the canonical chase rare slots:
Grandmaster's (ED+AR weapon), Godly (armor%), Jeweler's (4 sockets), Omniscient
(allskills), per-class skill prefixes, FCR/IAS/FRW/FHR rolls, dual-leech Lich, elemental
damage/pierce pairs, top-band damage suffixes, aura prefixes. The exclusions (light
radius, single-stat life/mana, Greater Bahamut/Mnemonic mana, Greater Whale, Greater
Sentinel/Paralysis, thorns, stamina) are exactly the "low-impact" group the design
intro names. Defensible curation.

Ambiguity: only 2 skilltab families (Cunning=traps, Rose Branded=paladin combat) are
kept. Other class skilltab affixes — bow tab, javelin tab, summon tab, fire/cold/lightning
mastery tabs, etc. — are dropped. Whether that's deliberate ("traps and zealot are the
only build-defining tabs") or an oversight needs Eric's read. Flagged as MEDIUM-001 below.

**Q2 — Rebuild from current non-Greater rows safer than full-file checkout?**

Yes, materially. A full-file checkout from any pre-Greater commit would revert:
- Phase 1 level reductions (level × 0.70) and levelreq reductions (× 0.85) — sampled
  current non-Greater rows still carry these reduced values.
- Phase 2 `×10` frequency rescale (e.g. Grandmaster's freq=20→200, of Quickness
  freq=300→600).
- Cruel/Jagged top-tier additions, Phoenix/Cobra column edits in non-affix files (not
  relevant here but the principle generalizes).

The "parse current → drop Greater rows → re-add 50 curated families" plan touches the
minimum surface area required.

**Q3 — One-marker-per-family safe under 511 cap?**

Yes. The math:
- Current itemstatcost: 511 data rows, IDs 0-510.
- Delete 72 `greater_*` clones (IDs 439-510) + 1 `item_greaterAffixMarker` (ID 438) = 73 removed.
- Add 50 new family markers.
- Net: -23 rows. New max ID ~487 (depending on renumbering — see LOW-001).

The descfunc/encoding template is already proven by `item_greaterAffixMarker`: `descfunc=19`,
`Save Bits=4`, `descpriority=999`. Clone that 50 times with new `descstrpos` keys and
unique `Stat` names. No risk of the v1 colored-stats failure mode (which copied `descfunc`
wrong for various source stats).

**Q4 — Frequency formula correct after Greater removal?**

Yes for surviving families — but the formula produces the *same* values currently in
the file, so the "recalculate" step is essentially a no-op for surviving rows. Removing
unrelated Greater families does NOT meaningfully change a surviving family's per-roll
probability, because D2's affix rolling is group-weighted within the affix group, not
pool-weighted across all Greater rows. (Greater Speed and Greater Quickness don't compete
with each other — they're in groups 35 and 7 respectively.) See MEDIUM-002 below for the
nuance.

**Q5 — Single apex row vs sum-equivalent for split families?**

**Use single apex row, picking the highest-band row of the highest-lvlreq tier.** Reasons:

1. D2 picks each affix slot by weighted-random within the eligible-for-this-itype pool,
   one row at a time. A Greater's "rarity vs apex" comparison is per-row, not summed.
2. The "10x rarer than apex" intent compares the Greater chase against the *best
   non-Greater roll of the same payload* — that's a single specific row.
3. Summing would conflate distinct payload tiers (of Evisceration's dmg-max 41-63 / 64-80
   / 81-100 / 101-120 are *different* affixes by D2 selection, not a unified pool).

When a family has an "early/late split at the same lvlreq" (e.g. of Evisceration line 23
lvl=59 freq=440 and line 24 lvl=85 freq=880 — both lvlreq 67 dmg-max 101-120), use the
LATE row's freq (880, not 440 and not the sum 1320). The current Greater Evisceration at
freq 88 reflects this — `880/10`.

**Q6 — Any selected family unsafe for too-many-mods + marker?**

Three families need the hybrid wrapper from design step 4:
- **#2 Greater Wraithly Weapon** (ED + Ethereal + Self-Repair = 3 gameplay mods)
- **#3 Greater Wraithly Armor** (AC% + Ethereal + Self-Repair = 3 gameplay mods)
- **#16 Greater Four Seasons** (currently single mod `res-all-max` so 1 mod free for
  marker — but verify if Eric wants additional payload).

All others fit comfortably (mostly 1-2 gameplay mods + 1 marker = ≤3 mod slots).
**#4 Greater Godly** (AC% + DR%) — 2 gameplay + 1 marker = 3 slots. Fine, no hybrid needed.

For the two Wraithly families, the hybrid wrapper should bundle the marker with the most
unconditional gameplay stat (the ED%/AC% one) — that way the marker still applies even
if the row rolls in a slot configuration where the optional `rep-dur` param is unused.

**Q7 — Aura Greater affixes safe and sensible?**

Yes, but the design owes the implementer six specific aura skill IDs. Pulling from the
current `Aureole` source rows in `magicprefix.txt`:

- Skill ID 113 — Might (verify by cross-checking with `data/global/excel/skills.txt`)
- Skill ID 126 — Fanaticism (the existing sole Greater Aureole uses 126, confirming this
  mapping)
- Skill ID 125 — Conviction
- Skill ID 119 — Holy Freeze
- Skill ID 123 — Meditation
- Skill ID 109 — Vigor

The implementer should look these up against `skills.txt` before committing — not from
my memory of D2 IDs. (Memory note: don't assert engine behavior from documentation
without verification — same lesson as the spawnable=0 incident.)

Aura level 4 is reasonable. It's:
- Higher than vanilla Aureole's `1-3` roll, so feels "Greater"
- Below runeword tiers (Doom's lvl 12 Holy Freeze, Faith's lvl 12-15 Fanaticism), so
  doesn't trivialize uniques/runewords
- Within reach of build relevance — lvl 4 Fanaticism is meaningfully more damage for a
  zealot than vanilla +2; lvl 4 Conviction is ~25% enemy resist reduction; lvl 4 Vigor is
  a solid FRW party buff

Alternative: tiered levels (early=3, mid=4, late=5) to differentiate bands beyond just
freq, but flat 4 is simpler and defensible. Eric's call.

**Q8 — Active/base sync and TSV validation covered?**

Yes. Plan step 8 lists active/base byte-match, row-width-match-header, ID count, no
dangling property references, and `spawnable=1`/`rare=1` checks. That's the full set.
One addition worth adding explicitly: see LOW-003 below on the lvl=1 leftover bug
prevention check.

## Findings

### Critical

None.

### High

**HIGH-001 — "Family" terminology conflates one-band-set with one-source-lvlreq-tier; row count is undefined**

- Where: design "Selected 50 Families" table; Q5 in the design's own open questions.
- Issue: Several source families have multiple lvlreq tiers with the same payload, and
  the current Greater implementation creates one 3-band set *per source lvlreq tier*:
  - `Greater Sage's` (allskills) currently spans 2 lvlreq tiers (43, 68) → 6 rows.
  - `Greater Arch-Angel's` / Berserker's / Necromancer's / etc. each currently span 3
    lvlreq tiers (36, 57, 64) → 9 rows per class.
  - `Greater Speed/Traveling` is in the design as ONE entry (#21) but Speed is lvlreq 25
    and Traveling is lvlreq 48 — 2 source tiers, currently 6 Greater rows.
  - `Greater Apprentice` (lvlreq 3) and `Greater Magus` (lvlreq 18) are listed as
    SEPARATE entries (#18, #19), implying the design *does* think tier-by-tier in some
    cases — but inconsistently.
  - `Greater Aureole × 6 auras` similarly raises the question: 6 families or 6 × 3 bands
    = 18 rows?
- Impact: The "50 families" headline could mean 50 × 3 = 150 rows, or it could mean
  ~80-100 rows depending on tier handling. The implementation needs an explicit answer
  to "for a family with N source lvlreq tiers, do I emit 1 × 3 bands or N × 3 bands?"
  Without it, the implementer will guess and Eric will get either a thin Greater layer
  (one tier only, low-level rares can't roll the Greater) or a much-larger-than-50 row
  set.
- Recommendation:
  - State explicitly in the design: each "family" emits **one 3-band set per source
    lvlreq tier** that currently exists for the same payload. Implementer reads source
    rows, groups by `(group, mod1code, ...payload-fingerprint, lvlreq)`, and emits 3
    bands per group.
  - Update the design table to either expand the 50 entries to their tier-resolved row
    counts (e.g. "Greater Arch-Angel's (lvlreq 36 / 57 / 64) → 27 rows") OR explicitly
    note "row count varies by source tier count — see implementation."
  - For Greater Speed/Traveling (#21), decide whether to keep both lvlreq 25 and 48 (low
    + mid access) or only 48 (chase-only).
  - For the 6 Greater Aureole auras, confirm each is one family emitting 3 bands (18
    rows total, single lvlreq=41 tier matching current Aureole/126).
- Blocks approval: No, but should be answered in a v2 design or in an addendum before
  implementation.

### Medium

**MEDIUM-001 — Skilltab coverage is suspiciously narrow**

- Where: design entries #32 (Cunning, traps tab) and #33 (Rose Branded, paladin combat
  tab).
- Issue: Vanilla D2 has skilltab affixes for many class build paths — Druid summons,
  Necro summoning, Amazon bow/javelin/spear, Sorc fire/cold/lightning mastery, Barb
  combat/warcries/masteries, Paladin defensive/offensive auras, etc. Keeping only
  Cunning and Rose Branded picks the two most "trapper / zealot" trees and silently
  drops every other class's tab-skill Greater path. The current `Greater Skilltab` /
  `Greater Skill-rand` references (96 combined wrapper uses) suggest there's more
  Greater skilltab content currently in play than the design preserves.
- Impact: Druid/Necro/Sorc/Amazon/Barb builds that rely on a specific skill tab get no
  Greater chase affix in their build path. Could be deliberate ("the rest don't earn
  Greater treatment") or an oversight.
- Recommendation: Either add a one-line rationale to the design ("Cunning and Rose
  Branded are the only skilltab Greaters because [reason]"), OR expand to cover the
  remaining class build-defining tabs. If expanded, the family count goes from 50 to
  ~58 — still fits the ID budget comfortably.
- Blocks approval: No.

**MEDIUM-002 — Per-family freq stays the same; "recalculate" is misleading**

- Where: design "Frequency Model" section, implementation step 5.
- Issue: The formula `late = round(apex/10)` produces the *current* late-band frequency
  for every surviving family I checked (11 spot-checks, 100% match). Removing unrelated
  Greater families doesn't change a surviving family's per-roll probability, because
  D2's affix rolling is weighted-random *within* the affix group (group 7 = IAS, group
  125 = +skills, etc.), not across the full Greater pool. Removing Greater Bahamut's
  (group 115, mana) doesn't change Greater Quickness's (group 7, IAS) roll chance.
- Impact: The "recalculate frequencies" step will produce a no-op diff for the 50
  surviving families' frequency columns. The script work is harmless but the design's
  framing suggests rebalancing happens — it doesn't.
- Recommendation: Either (a) clarify in the design: "frequency recalculation is a
  *consistency check*, expected to be a no-op for surviving families' current values;
  it exists to catch drift between source apex changes and Greater band values," or
  (b) actually retune the formula (e.g. tighten to `apex/8` for the 50-family curated
  pool now that Greaters are scarce) and document the intent.
- Blocks approval: No.

**MEDIUM-003 — Removing 175 `greater_*` property wrappers needs explicit step**

- Where: design implementation step 7 ("Remove unused Greater marker/properties/
  itemstatcost rows from the prior experiment").
- Issue: `properties.txt` currently has 225 `greater_*` and `greater_m_*` wrappers
  (112 of each kind, roughly). The redesign needs at most 50 marker wrappers + a small
  set of hybrid wrappers for 3-mod families (Wraithly weapon, Wraithly armor, maybe
  Aureole-with-marker). That's ~52-55 wrappers. The other ~170 must be removed.
- Impact: Leaving unreferenced wrappers in `properties.txt` is harmless at runtime (D2
  only loads referenced properties), but they're noise. Worse: if some are *still*
  referenced by the Greater rows the redesign keeps (e.g. `greater_m_swing2` is
  currently used by Greater Alacrity), the removal script must check references before
  deletion.
- Recommendation: Add an explicit substep: "For each `greater_*` property in
  `properties.txt`, scan `magicprefix.txt` + `magicsuffix.txt` (post-redesign) for any
  reference; delete only the unreferenced ones; assert no dangling references remain in
  the post-state."
- Blocks approval: No.

### Low

**LOW-001 — `itemstatcost.txt` ID renumbering policy not specified**

- Where: design tooltip/itemstatcost strategy section, implementation step 6.
- Issue: D2's `itemstatcost.txt` expects sequential `*ID` values starting from 0. If
  73 rows (IDs 438-510) are deleted in the middle and new family markers are appended,
  the file ends up with a gap (438-510 missing) unless the implementation explicitly
  renumbers. The current Greater experiment apparently appended `greater_*` stats at
  IDs 439-510 in sequence, suggesting the engine handles append-without-gap fine — but
  delete-with-gap behavior is unverified.
- Impact: Worst case, the engine reads `Send Bits` and uses position-index rather than
  `*ID`, in which case gaps cause stat misalignment and items roll wrong stat IDs (real
  crash risk — items can carry stat IDs that don't decode). Best case, the engine uses
  `*ID` directly and gaps are inert.
- Recommendation: Implementation script should
  (a) compact `*ID` to sequential 0..N after the deletion+addition pass, and
  (b) include a launch-test before commit confirming no stat decoding errors. The
  existing test pattern from the v2 colored-stats spec applies.
- Blocks approval: No.

**LOW-002 — Aura skill IDs not specified in design**

- Where: design entries #45-#50, Q7.
- Issue: The 6 Greater Aureole families need specific paladin aura skill IDs as
  `mod1param` values. The design names the auras (Might / Fanaticism / Conviction /
  Holy Freeze / Meditation / Vigor) but not the param numbers. The current sole Greater
  Aureole row uses `mod1param=126` (presumably Fanaticism). The implementer needs to
  cross-reference `data/global/excel/skills.txt` to resolve each name → skill ID.
- Impact: Wrong param → wrong aura grants. E.g. if Might is ID 113 but the implementer
  guesses 110, the row grants the wrong aura with no compile-time error.
- Recommendation: Add the 6 param values to the design table, resolved by reading
  `skills.txt`:
  | Aura name | skill ID |
  |---|---:|
  | Might | (lookup) |
  | Fanaticism | 126 (confirmed by current Greater Aureole row) |
  | Conviction | (lookup) |
  | Holy Freeze | (lookup) |
  | Meditation | (lookup) |
  | Vigor | (lookup) |
  This is a 5-minute lookup that prevents implementation guesswork.
- Blocks approval: No.

**LOW-003 — Audit `lvl=1` cleanup needs explicit validation step**

- Where: design implementation step 8 (validation), `greater-affix-scope-audit-results-
  2026-05-21.md`.
- Issue: The audit flagged five Greater rows currently carrying `lvl=1` from copy-paste
  drift (Sage's line 1700, Sentinel suffix 976, Whale suffix 1168, Paralysis1 suffix
  1291, Serpent's prefix 1373). The redesign deletes ALL current Greater rows and
  rebuilds from non-Greater rows, so this is naturally fixed for the kept families and
  N/A for the dropped families (Sentinel, Whale, Paralysis, Serpent — all dropped). But
  Sage's IS kept (#23), and the audit row 1700 is in group 204 (the `addxp` variant) —
  which the design drops. Worth confirming the redesign emits Sage's only in group 125
  (allskills) and not group 204 (addxp).
- Impact: If the implementation accidentally pulls Sage's from group 204, it inherits
  the `lvl=1` bug AND the wrong payload (XP gain instead of +skills).
- Recommendation: Add to validation: "Every emitted Greater row has `level ≥ 50` for the
  early band, `level ≥ 66` for mid, `level ≥ 81` for late." Assertion catches both the
  lvl=1 leftover bug class AND any band misassignment.
- Blocks approval: No.

## Validation Checks

- **Original user request reviewed:** Yes — *"create a plan to do them for review by
  claude. You will need to reweight all frequencies now that you are removing the other
  GA's. You decide how to do it, but it might make sense to go back to the original
  prefix suffix files to revert the frequency and redo it with these new GA's."* The
  design correctly rejects the "go back to original" path in favor of rebuilding from
  current rows (preserves Phase 1) — that's a stronger plan than Eric's tentative
  suggestion, and the design states the reason clearly. Frequency reweighting is
  covered (with the MEDIUM-002 caveat that it's a no-op for surviving families).
- **Design reviewed:** `design.md` in full plus the supporting audit files
  (`greater-affix-scope-audit-results-2026-05-21.md`, `current-greater-affix-family-
  summary-2026-05-21.tsv`).
- **Independent data verification:** Row counts (510 prefix Greater + 399 suffix Greater
  = 909 ✓), `itemstatcost.txt` max ID (510, 72 `greater_*` clones present ✓), active/base
  byte-identical (4 file pairs, all empty diff ✓), frequency formula spot-checks (11
  families, all match ✓), drift verification (Grandmaster's 1301-1303 and Godly
  1307-1309 carry Wraithly payload, confirmed ✓), audit defects (Sage's lvl=1 line 1700
  confirmed ✓), aura source param range (16 distinct IDs 98-126 ✓), marker template
  template (`item_greaterAffixMarker` descfunc=19 ✓).
- **Diff scope:** No game-data TXT changes in this round (design-only). The eventual
  implementation will touch the 8 listed files (4 active + 4 base counterparts) plus
  potentially `item-modifiers.json` for the 50 new marker strings.
- **Live publish risk:** `live_publish_allowed: false`; design-only review. The
  implementation review (round 2 of this task or a follow-up task) should gate
  live-publish on Eric's go-ahead and the game-launch test in the v2 colored-stats spec
  ("deploy to live, launch D2R, drop a rare, confirm no crash").

## Codex Action Items

1. **(HIGH-001)** State per-tier emission policy explicitly. For each design entry,
   either expand to per-lvlreq-tier sub-entries or document "1 family = 3 bands
   regardless of source tier count, picking the highest lvlreq tier as source apex."
   Recommended: keep per-tier emission (current Greater behavior) for Sage's,
   Arch-Angel's, Berserker's, Necromancer's, Hierophant's, Valkyrie's, Witch-hunter's,
   Priest's, Arch-Devil's, Speed/Traveling, Wraithly1 (weapon vs armor), Pyromaniac's
   (lvlreq 47 vs 65 for damage and pierce), Zeus's / Frost Wyrm's / Manticore's
   (likewise). Final implementation row count will be ~120-150 Greater rows, not 150
   exactly.

2. **(MEDIUM-001)** Add one-line rationale for the skilltab curation, or expand
   coverage to other class build-defining tabs. If expanded, list them in the design
   table.

3. **(MEDIUM-002)** Reframe "recalculate frequencies" as a consistency check, or
   actually retune the formula. Either way, set expectation that the freq column
   diff for surviving families is mostly a no-op.

4. **(MEDIUM-003)** Add explicit substep for `properties.txt` wrapper cleanup with
   reference-scan-before-delete. Assert no dangling references in the post-state.

5. **(LOW-001)** Specify `itemstatcost.txt` ID renumbering policy. Recommended: compact
   to sequential 0..N after delete+add, launch-test before commit.

6. **(LOW-002)** Resolve and add the 6 aura skill IDs to the design table.

7. **(LOW-003)** Add `level ≥ 50/66/81` per-band assertion to validation step 8.

None of these block approval. Proceed to implementation when Eric is ready; submit a
`code_review` round on the actual diff afterwards. The v2 colored-stats spec's launch-
test discipline (deploy → game launch → drop a rare → confirm no crash → revert
atomically if it crashes) applies to this implementation too — the prior `44b2c3b0`
crash is the cautionary precedent.

## Suggested Follow-up Tests (for the `code_review` round on the implementation diff)

1. **Greater row count.** Post-implementation, `awk '$1 ~ /Greater/' magicprefix.txt
   magicsuffix.txt | wc -l` should match the design's declared count (after HIGH-001
   resolution).
2. **No dangling property references.** Every `greater_*` / `greater_m_*` /
   `item_greaterAffix_*` code referenced in magicprefix/suffix's mod1code/mod2code/
   mod3code must exist as either a property in `properties.txt` or a stat in
   `itemstatcost.txt`.
3. **No dangling itemstatcost references.** Every `Stat` name referenced by a property
   wrapper's `func1-7`/`stat1-7` columns must exist in `itemstatcost.txt`.
4. **`itemstatcost.txt` ID continuity.** `*ID` column is strictly sequential 0..N with
   no gaps.
5. **`itemstatcost.txt` ID ceiling.** `awk -F'\t' 'NR>1 && $2!="" {if($2+0 > max)
   max=$2+0} END{print max}'` must return ≤ 510. Ideal target ≤ 487.
6. **Active/base byte-identical** for all four file pairs (`diff -q` empty).
7. **TSV row width** equals header count for every row in all four files.
8. **`spawnable=1 rare=1` on every Greater row.** No `spawnable=0` slips through. The
   prior bug (saved as `feedback_d2r_spawnable_rare_only.md`) cost a full review cycle.
9. **Level/lvlreq bands.** Early band rows have `level=50, maxlevel=65`; mid have
   `level=66, maxlevel=80`; late have `level=81, maxlevel=""`. No `lvl=1` leftovers.
10. **Frequency spot-check.** Pick 5 surviving families and verify `late_freq =
    max(1, round(source_apex_freq/10))`.
11. **Marker presence.** Every Greater row has exactly one mod slot pointing to either
    a per-family marker property OR a hybrid wrapper that includes the marker.
12. **Game-launch test before publish.** Deploy to live, launch D2R, drop multiple
    rares across various item levels, confirm:
    - No crash on game load.
    - No crash on item drop.
    - Greater roll rate is materially lower than current "post-freq-restore" state
      (because most Greater families were deleted) — eyeball check, not strict count.
    - The "Greater Affix: <family>" tooltip line renders on a Greater roll.
