---
schema: ai-review-result-v1
task_id: 2026-05-19-2146-rare-affix-final-preimplementation-review
round: 1
reviewer: claude
verdict: needs_fixes
critical: 0
high: 0
medium: 2
low: 2
requires_codex_changes: true
---

# Claude Review

## Verdict
Needs fixes

## Summary

Final pre-implementation review of the two-phase rare-affix overhaul. The framework is
sound, the prior round-1 findings on the `1339` audit task are well addressed, and the
**core math is correct and proven**. The package is close to implementation-ready, but two
real items need to land before Codex edits `magicprefix.txt` / `magicsuffix.txt`.

What I verified:

- **MED-001 from `1339` (`Greater Lamprey/Vampire` 30x bug) is fixed** — the chance table
  now shows `Greater weight 72`, `apex weight after 720`, `10.0x rarer`. ✓
- **MED-002 from `1339` (single-item sampling) is addressed** — the new
  `rare-greater-affix-scope-validation-2026-05-19.tsv` has **1430 candidate × item-type
  checks, every one at `ratio_delta_from_10x = 0.0`**. So "Greater is exactly 10x rarer"
  is verified per scope, not just per sample item. ✓
- **`LOW-001` whole-file scaling** is now explicit in the design (line 359). ✓
- **`LOW-002` group-blocked-3-slot model** is now labelled an approximation (line 363). ✓
- **Phase 1 `maxlevel` preservation is correctly implemented** — every one of the 1940 rows
  in `affix-level-requirement-changes-2026-05-19.tsv` shows `maxlevel_delta = 0` (verified
  by direct scan of the TSV). The generator script (`generate_affix_level_change_data.py`)
  preserves `maxlevel` and applies `× 0.70` to `level` and `× 0.85` to `levelreq` using the
  pinned `round_half_up = floor(x + 0.5)` rule. Sample rounds check out (Cruel `69→48`,
  Cruel `74→52`, Grandmaster's `84→59`, Grandmaster's `86→60`; levelreqs `63→54`, `69→59`,
  `88→75`).
- **Phase 1 scoping** — compression is applied only to `rare=1` rows (1644 in scope, 296
  magic-only out of scope); Phase 2's `× 10` frequency scaling separately applies to all
  rows including `rare=0`. That combination preserves both the rare and the magic pools
  proportionally where they overlap, and is consistent with Eric's stated intent.

Two real items remain:

- **MED-001 — Greater rows have no explicit `levelreq`.** Codex flagged this in the task
  request. It is a hard pre-implementation blocker: without `levelreq`, a `dmg% 451-500`
  Greater Grandmaster's row contributes nothing to the item's equip-level, so a Greater
  weapon could be wielded far below the character level its power demands.
- **MED-002 — The "early/mid/late Greater bands vs single late row" decision** (Codex's
  Q3) needs Eric's explicit call. Eric's earlier explicit design *was* the 3-band structure
  ("Early 50-65 freq 1, Mid 66-80 freq 2, Late 81+ freq 3"); his later "all new affixes don't
  have a `maxlevel`" reads as ambiguous about whether that overrules the early/mid
  `maxlevel`-gated bands. The design currently still shows the 3-band structure.

Plus two Lows around the top-affix split preview and per-element row expansion. Fix the two
Mediums, decide the bands, and this is ready to go.

## Review Questions

**Q1 — Does the two-phase plan preserve rare affix proportions correctly for existing
affixes?**
Yes, in the meaningful sense:
- **At high ilvls (~90):** `maxlevel` preservation means the eligible pool at ilvl 90 is the
  same set of affixes as before (low-tier affixes still expire at their original
  `maxlevel`); Phase 2 scales every frequency `× 10` uniformly; Greater rows add only the
  uniform per-pool dilution proven by `existing_only_relative_delta = 0`. Relative
  proportions at endgame ilvls are essentially identical.
- **At lower ilvls (e.g. 50):** Phase 1 deliberately expands the eligible pool (more
  formerly-high-tier affixes now reach down). Relative ratios *among* the previously-eligible
  affixes stay the same; their absolute share is diluted as new entrants join the pool.
  That dilution is the *purpose* of Phase 1 ("broader, more exciting affix pool at lower
  levels"), not a math defect.
The sanity proof (`existing_only_relative_delta = 0.0` across all 1795 rows) covers the
Phase 2 frequency reweighting. Phase 1's eligibility expansion is intentional and
documented.

**Q2 — Is preserving existing `maxlevel` correct?**
Yes — verified in the TSV (`maxlevel_delta = 0` for every one of the 1940 rows). The
intended exception is the new early-duplicate row added by the **top-affix split**
(`top_early_maxlevel = original_top_level - 1`). One caveat: the TSV preview shows top-affix
existing rows being level-compressed (e.g. `Grandmaster's 84→59`) without the split-row
additions, so the TSV is an incomplete Phase 1 preview — see LOW-001.

**Q3 — Should Greater rows have no `maxlevel`, or keep early/mid/late banding?**
**Recommendation: keep the 3-band structure.** Eric explicitly designed it in the original
request ("Early 50-65 freq 1, Mid 66-80 freq 2, Late 81+ freq 3, all `dmg% 350-400`") to
make Greater available on lower-ilvl rares but rarer. The most plausible read of his later
"all new affixes don't have a `maxlevel`" is that it refers to the **late** band — which
correctly has no `maxlevel` — and to existing-affix Phase 1 work, not to the structural
early/mid bands which use `maxlevel` as their gating mechanism. Collapsing to a single
`level=81 maxlevel=blank` row would make Greater a strict ilvl-81+ exclusive and remove
Eric's "available on lower-ilvl items but rarer" feature; that is a different design.
**Get Eric's explicit yes/no here** — see MED-002.

**Q4 — What `levelreq` policy should Greater rows use? Is the missing `levelreq` a
blocker?**
**Yes, it is a blocker.** Without an explicit `levelreq`, the affix contributes `0` to the
item's overall equip-level requirement, so a Greater Grandmaster's weapon (`dmg% 451-500`)
would only require the base item's own level — fundamentally wrong for a chase affix.
**Recommended policy: each Greater row's `levelreq` equals its `level`** (e.g. Early band
`level=50 → levelreq=50`; Mid `66 → 66`; Late `81 → 81`). This matches the convention used
by the strongest existing affixes (where `levelreq` is at or above `level`) and is the
simplest defensible default. Eric can shift the late-band `levelreq` up further (e.g. `85`
or `90`) if he wants Greater to require a higher equip level than its `level` gate, but `0`
is not acceptable.

**Q5 — Do the TSVs prove 10x per item-scope?**
Yes. `rare-greater-affix-scope-validation-2026-05-19.tsv` has **1430 candidate × item-type
checks, every one at `ratio_delta_from_10x = 0.0`**. The `existing_only_relative_delta`
column of the probability-sanity TSV is `0.0` for all 1795 rows. The two TSVs together
constitute a strong empirical proof that (a) existing-affix proportions are preserved
exactly under uniform `× 10`, and (b) every drafted Greater candidate is exactly 10x rarer
than its apex on every item type it can roll on.

**Q6 — Does the apex coverage miss any important top affix families?**
No glaring gaps. The coverage audit (lines 99–204 of the audit MD) is mechanically generated
from every `rare=1` group, so by construction no group is missed. Eric's specific call-outs
are all present:
- **Cross-scope rows** — handled in the scope-validation TSV.
- **Charms** — `Greater Avatar`, `Hulking`, `Lucky`, `Ruby/Sapphire/Amber/Emerald`,
  `Serpent's`, `Serrated`, `Shimmering`, `Balance`, `Inertia`, `Vita` all present.
- **Class skills** — `Greater Omniscient`, `Greater Skilltab`, `Greater class skill` all in
  group 125.
- **Damage reduction %** — `Greater Godly` carries `red-dmg% 26-30` (group 101 apex).
- **Ethereal / self-repair** — `Wraithly1` (weapon) is in `Greater Grandmaster's` baseline,
  armor `Wraithly1` is in `Greater Godly` baseline. A "Greater ethereal" affix is not
  drafted — reasonable, since ethereal is binary.
- **Weapon-only hybrid families** — `Greater Grandmaster's` (ED + rider),
  `Greater Adamantine-Wrought` (ED/AC + dur), `Greater Celestial` / `Divine` (anti-demon /
  anti-undead) all present.
The only structural gap is implementation-time row expansion for the aggregated multi-element
and multi-scope candidates — see LOW-002.

**Q7 — Implementation blockers?**
Three. The two Mediums (missing `levelreq`, bands decision) plus a coordination gap: the
existing Phase 1 TSV does not yet preview the top-affix split additions (the new late rows
and the early-row `maxlevel` / halved frequency adjustments). Codex should not edit
`magicprefix.txt` / `magicsuffix.txt` until those three are resolved.

## Findings

### Critical
None.

### High
None.

### Medium

**MED-001 — Greater synthetic templates have no explicit `levelreq`; this is a blocker**

- Where: `scripts/audit_rare_affix_apexes.py` — the synthetic Greater rows produced by
  `band_rows()` / `as_row()` carry `level`, `maxlevel`, `frequency`, `rare`, `itype*`,
  `etype*` but **no `levelreq`** field. Codex flagged this in the task request.
- Why it matters: an affix row with no `levelreq` contributes `0` to the item's overall
  equip-level. A Greater Grandmaster's weapon (`dmg% 451-500`) would then be wieldable as
  soon as the underlying weapon's own level requirement is met — a chase-tier affix with no
  power-floor on equip is bad design and an in-game balance break.
- Suggested fix: each Greater row's `levelreq = row.level` as the simplest defensible
  default (so an Early band `level=50` row has `levelreq=50`, a Late band `level=81` row
  has `levelreq=81`). If Eric wants Greater to require a *higher* equip level than its
  `level` gate, raise the Late-band `levelreq` (e.g. `85` or `90`); the principle of "equip
  req >= drop-level gate" still holds. Update both `as_row()` / `band_rows()` to set
  `levelreq` and regenerate the audit.
- Blocks approval: **Yes** — required before TXT edits.

**MED-002 — Greater bands vs single late row needs Eric's explicit decision**

- Where: design line 178 (3-band default shape); Phase 2 examples (`Greater Grandmaster's`
  7 rows across 3 bands at line 369–377; `Greater Zodiac` 3 rows at line 388–392); user
  guidance "all new affixes don't have a `maxlevel`".
- Why it matters: the 3-band structure depends on `maxlevel=65` and `maxlevel=80` on the
  early and mid bands to make them disappear at higher ilvls. If Eric's "no `maxlevel`"
  instruction applies to every Greater row, the early/mid bands collapse and Greater becomes
  a Late-only single row (ilvl 81+ exclusive). That is a real gameplay difference: in the
  3-band model, Greater is rare-but-possible on ilvl 50–80 rares; in the single-row model
  it can never appear below ilvl 81.
- Suggested fix: recommend keeping the 3-band structure (it's Eric's original explicit
  design, and his "no `maxlevel`" is most naturally read as referring to the late band /
  to Phase 1 existing-row work). But get Eric to confirm verbatim which model he wants
  before Codex commits to TXT rows.
- Blocks approval: **Yes** — Codex needs the answer to write the right rows.

### Low

**LOW-001 — Top-affix split additions are not previewed in the Phase 1 TSV**

- Where: `affix-level-requirement-changes-2026-05-19.tsv` shows every existing top-affix row
  level-compressed (e.g. `Grandmaster's 84→59`, `86→60`) with `maxlevel_delta=0`. The design
  (line 137–150, Implementation Strategy step 5) says the top-affix split adds an
  early-duplicate row with `maxlevel = original_top_level - 1` and half frequency, and the
  late row stays at the original level — none of which appears in the TSV.
- Why it matters: as previewed, Codex's TXT edits would compress the top row's level without
  adding the early/late split, removing the "top affix is half-rate before its original
  gate, full-rate at its original gate" feature.
- Suggested fix: extend `generate_affix_level_change_data.py` (or add a follow-up generator)
  to preview the top-affix split — show the late-row addition and the early-row's
  `maxlevel`/frequency adjustment for each apex family — so the implementation diff is fully
  visualised before TXT edits land.
- Blocks approval: No, but should land before implementation.

**LOW-002 — Multi-element / multi-scope Greater candidates are still aggregated in the
audit**

- Where: chance table — `Greater Ruby/Sapphire/Amber/Emerald` (4 elements, groups 117-120),
  `Greater Scorching/Shocking/Pestilent` (3 elements, 138-140), `Greater jewelry elemental
  damage` (4 groups), `Greater Elemental Mastery` / `Greater Elemental Pierce` (4 elements
  each in group 209), `Greater missile prefixes`/`suffixes` (8/7 groups), `Greater Titan`
  (str/dex/vit/enr in group 31), `Greater Crushing/Fatal` (crush + deadly in group 202).
- Why it matters: these cannot be implemented as a single TXT row each — they need one row
  per element/per scope. The design acknowledges this (line 361) but the audit aggregates
  for readability. Implementation must expand each aggregated candidate into its real per-row
  set, and the 10x ratio must hold for each split row's actual scope.
- Suggested fix: before TXT edits, expand each aggregated candidate explicitly in the
  audit / chance table, and confirm via the scope-validation TSV that every split row is at
  exactly 10x.
- Blocks approval: No (acknowledged future work) — but is a prerequisite for the TXT pass.

## Codex Action Items

Before editing `magicprefix.txt` / `magicsuffix.txt`:

1. **(MED-001 — required)** Add explicit `levelreq` to every Greater row. Recommended
   default: `levelreq = row.level`. Regenerate the audit / TSVs and confirm levelreq
   monotonicity within each Greater family.
2. **(MED-002 — required)** Get Eric's explicit confirmation: keep the 3-band Greater
   structure (recommended) vs collapse to a single Late row per family. Document the
   decision in the design.
3. **(LOW-001)** Extend the Phase 1 preview TSV (or add a complementary one) that shows the
   top-affix split additions — the new late rows, and the existing top row's transition into
   the early row with `maxlevel = original_top_level - 1` and halved frequency.
4. **(LOW-002)** Expand aggregated multi-element / multi-scope Greater candidates into the
   real per-row sets in the audit, and re-run the scope-validation TSV against the expanded
   list.

Resubmit as round 2 once the two Mediums are resolved; the Lows can be folded in alongside.

## Validation Checks

- **Original user request reviewed:** Yes — every Eric instruction in the request is
  reflected in the plan (level −30%, levelreq −15%, maxlevel preserved, top-affix early/late
  split, Greater ~10× rarer than apex per-scope, whole-file frequency scale, sanity
  proof). The two Mediums above are exactly the items Eric himself flagged or that fell out
  of the round-1 review.
- **Round-1 findings re-checked:** All addressed — Lamprey/Vampire 30× fixed, scope-validation
  TSV produced and clean, whole-file scaling explicit, group-blocked model relabelled.
- **TSVs spot-checked numerically:** `maxlevel_delta = 0` for all 1940 rows;
  `existing_only_relative_delta = 0.0` for all 1795 rows; `ratio_delta_from_10x = 0.0` for
  all 1430 scope checks. Sample `level` and `levelreq` rounds match
  `round_half_up(x * 0.70)` / `round_half_up(x * 0.85)` precisely.
- **TSV column counts:** N/A this round — no TXT edits. A `code_review` round must check
  `magicprefix.txt` / `magicsuffix.txt` column counts and active/base parity once the rows
  land.
- **Live publish risk:** `live_publish_allowed: false`; design-only.

## Suggested Follow-up Tests (for the Phase 1 + Phase 2 code_review)

1. **`levelreq` correctness** — every new Greater row has a non-blank `levelreq`; the
   resulting item-level on a Greater rare matches expectations.
2. **`maxlevel` invariance** — every existing affix row's `maxlevel` matches its pre-Phase-1
   value; the only `maxlevel` deltas are on the new top-affix early-duplicate rows and
   intentionally blank on the new late rows.
3. **Top-affix split end-to-end** — at ilvl `original_top_level - 1`, only the early-duplicate
   row is eligible (half frequency); at ilvl `original_top_level`, only the late row is
   eligible (full frequency); no double counting.
4. **Greater 10x per scope** — every Greater row's eligible weight is `1/10` of its
   post-scale apex on each item type both can roll on.
5. **Whole-file scale** — every `magicprefix.txt` / `magicsuffix.txt` frequency was
   multiplied by 10 (`rare=0` and `rare=1` alike); active/base in sync; column counts
   intact.
6. **Greater group exclusivity** — a Greater roll excludes the normal family rows in the
   same group.
7. **In-game** — top affix chance at high ilvl is unchanged; broader affix variety on
   mid-ilvl rares; Greater feels like a rare chase; no broken low-level twink items.
