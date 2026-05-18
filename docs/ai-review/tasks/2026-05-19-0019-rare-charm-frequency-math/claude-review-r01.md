---
schema: ai-review-result-v1
task_id: 2026-05-19-0019-rare-charm-frequency-math
round: 1
reviewer: claude
verdict: needs_fixes
critical: 0
high: 1
medium: 3
low: 4
requires_codex_changes: true
---

# Claude Review

## Verdict
Needs fixes

## Summary

This is a **design review** of the rare-item rework, focused on the charm frequency
normalization math. Eric's explicit ask: *"It is very important the math is correct here."*

**Headline: the arithmetic is correct, and the core approach is sound.** I verified every
number in `design.md` and the canonical design against the live data in
`data/global/excel/magicprefix.txt` and `magicsuffix.txt`. The proportional-scaling logic
(`× 5`) is mathematically valid and provably preserves charm affix odds. There is **one
genuine defect** — not in the arithmetic, but in the *scope* of the "scale ALL charm affixes"
rule — plus two design decisions that need Eric's explicit sign-off and one unpinned
convention.

What I verified against the files:

- **Skill-tree rows: 21 original-class `+1 skill tree` `lcha` prefix rows at `frequency=2`
  (skilltab params 0–20) + 3 Warlock rows at `frequency=1` (params 21/22/23).** Confirmed
  exactly. All 24 are `lcha`-exclusive, `group=125`, `level=50`, `levelreq=42`. Current skill
  frequency `(21×2)+(3×1)=45` ✓.
- **Level-90 `lcha` prefix pool: 65 rows, total frequency 279.** Independently reproduced —
  all 78 `lcha` prefix rows in the level band, minus 13 `rare=0` rows = 65; 404 − 125 = 279.
  The audit's eligibility rule (`rare=1` rows within the level band) is the correct rare-item
  rule. ✓
- **Level-90 `lcha` suffix pool: 15 rows, total frequency 88, zero skill rows.** Confirmed
  exactly. ✓
- **Scaled totals: 1410 / 240 / 24 / 1434, shares 16.74% / 1.67%.** All arithmetic correct
  (see Q5).
- **Only `skilltab` carries skills on charms** — no `oskill` / `allskills` / `skill` charm
  rows exist. The design's scope (skilltab only) is complete. ✓
- **Critical finding:** a full scan of both files shows **`group=307` is the *only* group
  whose charm-eligible rows also carry non-charm itypes** (`ring`, `amul`, `glov`, `boot`,
  `belt`, `helm`). Every other charm affix row is charm-itype-exclusive. This makes the flat
  `× 5` safe everywhere *except* group 307 — see HIGH-001.

The design cannot move to implementation as-is because **HIGH-001**: applying
`scaled_charm_frequency = current_frequency * 5` literally to `group=307` would multiply the
pierce-affix odds on rings, amulets, gloves, boots, belts, and helms by 5×, because those
group-307 rows are itype-shared with non-charm equipment. Fix the rule's scope, get Eric's
decisions on the Warlock normalization (MED-001) and the `levelreq` −15% (MED-002), pin the
rounding convention (MED-003), then this is good to implement.

## Review Questions

**Q1 — Does the proposal preserve proportions when normal `+1 skill tree` rows go to
`frequency=10` and Greater `+2 skill tree` rows use `frequency=1`?**
Yes, in the meaningful sense, with two caveats. Uniform `× 5` of *every* existing charm row
exactly preserves the relative weighting among all existing affixes (proof in Q6). Setting
normal skill rows to 10 *is* exactly `× 5` of their current `frequency=2`, so they stay in
proportion with everything else. Greater rows at `frequency=1` are new content: they dilute
every affix's *absolute share* uniformly but do not change any *ratio* between two existing
affixes — so they do not break proportionality in the sense Eric means. The two caveats:
(a) the Warlock rows are not `× 5`'d, they are set to 10 (= `× 10`) — see Q3/MED-001;
(b) the "scale ALL charm affixes" rule must not be applied verbatim to `group=307` — see
Q7/HIGH-001.

**Q2 — Is multiplying all charm affix frequencies by 5 correct, given original skill rows are
`frequency=2`?**
Yes. `10 / 2 = 5`. D2 `frequency` is a positive integer and the Greater floor is `1`; to
express the desired 10:1 normal:Greater ratio while keeping skill rows proportional to the
rest of the pool, every existing charm row must be `× 5` so the skill rows land exactly on
10. `× 5` of any integer is an integer, so the scaling step introduces **zero rounding
error** (unlike the `× 0.70` level compression). `× 5` is the unique minimal integer
multiplier that works. Correct — provided `group=307` is carved out (Q7).

**Q3 — Is the Warlock `+1 skill tree` exception (currently `frequency=1`, proposed `10`)
consistent?**
Mathematically it is trivial — it is just "set to 10." But it is **not proportional
scaling**: pure proportional scaling would give `1 × 5 = 5`. Raising it to 10 changes the
Warlock-vs-original-class skiller weight ratio from 1:2 to 1:1, so it *does* break
"proportions exactly the same" for those 3 rows specifically. It is, however, consistent with
Eric's explicit "+skills rarity = 10" (a flat target). **Eric's two instructions conflict**
("scale so proportions are exactly the same" vs "make +skills = 10"); he must explicitly
choose. Recommendation: accept the normalization — all class skill-tree charms being equally
common is the cleaner outcome and honors the more specific instruction — but record it as a
deliberate rebalance, not as proportion-preserving. The design already surfaces this honestly.
→ MED-001.

**Q4 — Does the level compression stay consistent with "all levels reduced by 30%"?**
Partially. The affix `level` (`× 0.70`) and `maxlevel` (`× 0.70`) compressions *are* −30% ✓.
But two things deviate from a literal "all levels −30%": (a) `levelreq` is reduced only 15%
(`× 0.85`); (b) the Phase 1 Top-Affix Split keeps the top affix's *late* row at its
**original, uncompressed** `level` (`top_late_level = original_top_level`). Both are
deliberate, defensible choices, but neither matches the literal instruction. Eric should
explicitly confirm the −15% `levelreq` and the top-late-row exception. → MED-002.

**Q5 — Are the stated level-90 prefix-pool numbers correct?**
**Yes — all confirmed against `magicprefix.txt`:**

| Quantity | Stated | Verified |
|---|---|---|
| Eligible `lcha` prefix rows @ ilvl 90 | 65 | ✓ (78 in level band − 13 `rare=0` = 65) |
| Current total frequency | 279 | ✓ (404 − 125 = 279) |
| Current skill frequency | 45 | ✓ (21×2 + 3×1) |
| Current skill share | 16.13% | ✓ (45/279 = 16.1290%) |
| Scaled existing total | 1410 | ✓ (234 non-skill ×5 = 1170; +21×10=210; +3×10=30) |
| Normal skill frequency | 240 | ✓ (210 + 30) |
| Greater skill frequency | 24 | ✓ (24 rows × 1) |
| Final total with Greater | 1434 | ✓ (1410 + 24) |
| Normal skill share | 16.74% | ✓ (240/1434 = 16.7364%) |
| Greater skill share | 1.67% | ✓ (24/1434 = 1.6736%) |

The audit methodology is sound: the `rare=1` filter reproduces 65/279 exactly, which is the
correct affix pool for rare items.

**Q6 — Are there hidden D2R mechanics that make this reasoning incomplete?**
The proportional reasoning is **complete and correct for the charm pools**, with one genuine
gap. Proof that uniform `× K` is a no-op:

```text
For any eligible row-subset S, P(pick row r) = freq(r) / SUM_{s in S} freq(s).
Multiply every frequency by K:
  P'(r) = K*freq(r) / SUM K*freq(s) = K*freq(r) / (K * SUM freq(s)) = P(r).
Identical. This holds for ANY subset S, so it holds at every draw regardless of
which `group`s are already locked and regardless of how many prefixes/suffixes
the item rolls. Therefore uniform scaling leaves the entire joint distribution
of affix outcomes unchanged.
```

This survives every D2 affix mechanic that matters: `group` mutual-exclusion (it only changes
*which* subset `S` is — the cancellation works for any `S`), the up-to-3-prefix /
3-suffix multi-draw, and the magic-vs-rare split. Affix *count* is engine-side and
independent of `frequency` (canonical design line 33), so scaling never changes how many
affixes a charm rolls. **The one requirement: `K` must be applied to every row a charm can
draw — and a scaled row must not also appear in a non-charm pool.** The only incomplete spot
is exactly that: itype-sharing. A full scan confirms it affects **only `group=307`**. → see
HIGH-001 and Q7.

**Q7 — Should `group=307` rare-only pierce rows be scaled `× 5`?**
**No — not as the rule is currently written.** Each pierce affix in group 307 is implemented
as ~5 rows split by item type (because a row has only 7 itype slots). For example
`Virulent` (pierce-pois) prefix rows:

```text
[scha]                                -> small charm only      (charm-exclusive)
[ring, mcha]                          -> ring + medium charm    (SHARED)
[amul, glov, boot, belt, helm, lcha]  -> 5 non-charm + lg charm (SHARED)
[shld, weap]                          -> non-charm only
[tors]                                -> non-charm only
[lcha]                                -> large charm only       (charm-exclusive; pierce-pois/fire only)
```

Scaling the two **SHARED** rows `× 5` would multiply pierce-affix odds on rings, amulets,
gloves, boots, belts, and helms by 5× — those item types are not part of the charm rework.
Recommendation: **exempt `group=307` entirely from the charm `× 5`**, consistent with the
design's own treatment of 307 as "special-purpose rare rows" (canonical design line 222), and
document that charm pierce affixes are intentionally left at `frequency=1` (hence
proportionally rarer in the post-scaling pool — an accepted, documented deviation). If Eric
instead wants pierce proportionally preserved *on charms*, the shared rows must first be
**split** into charm-only and non-charm-only copies. The one thing that must not happen:
scaling the shared rows in place. → HIGH-001.

**Q8 — Should the design distinguish prefix and suffix pools explicitly?**
**Yes, explicitly.** Prefix and suffix are independent draws — a frequency in one pool has no
interaction with the other, and they need not even share the same scaling factor.
Consequences the design should state: (a) the `+1`/`+2` skill-tree normalization is entirely
a **prefix** operation — all 24 `skilltab` rows are in `magicprefix.txt`, and the 15-row
`lcha` suffix pool has **zero** skill rows (confirmed) — so the prefix `× 5` is mandatory and
load-bearing; (b) the suffix `× 5` is a pure **no-op** *unless* Greater suffix rows are added
to charms. The canonical design *does* list `Greater Inertia` and `Greater Balance` as
charm-suffix Greater candidates (lines 214–215), and `of Inertia` / `of Balance` are in the
15-row suffix pool — so the suffix scaling should be tied explicitly to whether those Greater
suffix rows are in scope. → LOW-001.

**Q9 — Is the design ready to implement?**
**Not yet.** The core math is correct and the approach is sound, but Codex should revise the
design before editing `magicprefix.txt` / `magicsuffix.txt`: fix HIGH-001 (carve `group=307`
out of the `× 5` rule), get Eric's decisions on MED-001 (Warlock normalization) and MED-002
(`levelreq` −15%), and pin the rounding convention (MED-003). With those resolved, the charm
scaling is good to implement.

## Findings

### Critical
None.

### High

**HIGH-001 — The flat `× 5` rule, applied to `group=307`, distorts non-charm item pools**

- Design section: "Proposed Existing Charm Frequency Scaling" (`design.md`); canonical design
  "Charm Frequency Normalization Proposal", rule `scaled_charm_frequency = current_frequency * 5`.
- Issue: The rule says "scale ALL charm affixes." `group=307` (rare-only elemental pierce,
  `level=92`, all `frequency=1`) is implemented as item-type-split rows, and a verified
  full-file scan shows **307 is the only group whose charm rows also carry non-charm itypes.**
  Two of the ~5 rows per pierce affix are shared: `[ring, mcha]` and
  `[amul, glov, boot, belt, helm, lcha]`. Editing those rows to `frequency=5` raises the
  pierce-affix weight 5× in the **ring, amulet, glove, boot, belt, and helm** rare pools —
  item types that are not in scope for this rework. With 6 pierce affixes that is up to +24
  weight injected into each of those non-charm pools.
- Why it matters: Eric's instruction is explicitly "scale ALL charm affixes freq" so the
  *charm* proportions stay the same. The shared rows mean a literal implementation silently
  rebalances six other item categories. The canonical design's guidance to "directly edit
  shared affix rows" (line 125) was written for the magic-vs-rare sharing axis — it does not
  account for itype-sharing across equipment slots, which is what 307 does.
- Suggested fix: Carve `group=307` out of the `× 5` rule. Recommended: **exempt 307 entirely**
  (leave all its rows at `frequency=1`), consistent with the design already classifying 307
  as "special-purpose rare rows" (canonical design line 222); document that charm pierce
  affixes are deliberately not proportionally scaled and are therefore rarer relative to
  other charm affixes in the post-scaling pool. Alternative, if pierce must stay proportional
  on charms: split each shared 307 row into a charm-only copy (`scha`/`mcha`/`lcha`, scaled
  `× 5`) and a non-charm copy (unscaled `frequency=1`). Do **not** scale the shared rows in
  place.
- Also note (pre-existing data quirk, not caused by this rework, but relevant when touching
  307): the prefix file gives `Virulent`/`Incendiary` an extra `[lcha]`-only row while
  `Gelid`/`Magnetic`/`Mystical`/`Breaching` get an extra `[tors]`-only row instead — so large
  charms already roll pierce-pois/pierce-fire at double the weight of the other four pierce
  types. Worth a one-line note in the design so Codex does not "fix" it unintentionally.
- Blocks approval: **Yes** — the rule's scope must be corrected before the TXT edits land.

### Medium

**MED-001 — The Warlock `+1 skill tree` normalization breaks strict proportionality and needs
Eric's explicit decision**

- Design section: "Warlock Exception".
- Issue: Warlock skiller rows are currently `frequency=1`. Proportional scaling gives
  `1 × 5 = 5`; the proposal sets them to `10`. That changes the Warlock-vs-original-class
  skiller weight ratio from 1:2 to 1:1, which contradicts "scale ALL charm affixes so the
  proportions are exactly the same."
- Why it matters: Eric gave two instructions that cannot both hold — "proportions exactly the
  same" and "+skills rarity = 10." This is a genuine fork, not a math error. Per protocol,
  divergence from the literal request needs explicit sign-off.
- Suggested fix: Present both branches to Eric (the design already does — good): normalize to
  10 (all class skill-tree charms equally common; recommended, honors the specific "+skills =
  10" instruction) vs strict `× 5` to 5 (preserves the old Warlock-is-rarer ratio). Whichever
  Eric picks, document it as a deliberate decision. If "normalize to 10" is chosen, the
  audit's 1410 / 240 / 16.74% figures are the right ones; if "strict 5", use the design's
  alternative 1395 / 225 / 15.86%.
- Blocks approval: Decision required before implementation.

**MED-002 — `levelreq` −15% (and the top-affix late-row exception) deviate from "all levels
reduced by 30%"**

- Design section: "Current Phase 1 Rules"; canonical design "Phase 1" and "Phase 1
  Top-Affix Split".
- Issue: Eric wrote "the levels should all be reduced by 30%." The design reduces affix
  `level` and `maxlevel` by 30% ✓ but reduces `levelreq` by only 15% (`× 0.85`), and the
  Top-Affix Split keeps the top affix's late row at its **original** `level`
  (`top_late_level = original_top_level`). Both are reasonable design choices but are not a
  literal "all levels −30%."
- Why it matters: Two separate deviations from the literal request. The −15% `levelreq` in
  particular is a sizable, deliberate softening that Eric did not state.
- Suggested fix: Get Eric's explicit confirmation that (a) `levelreq` should drop 15% (not
  30%) and (b) the top affix's full-frequency gate intentionally stays at its original level.
  If Eric meant 30% across the board, change the `levelreq` formula to `× 0.70`.
- Blocks approval: Decision required before implementation.

**MED-003 — The rounding convention for the compression formulas is unpinned**

- Design section: "Current Phase 1 Rules" — `round(...)` in three formulas.
- Issue: `round()` is ambiguous: round-half-up (Excel `ROUND`, most modders' expectation) vs
  round-half-to-even / banker's (Python 3 `round()`, some libraries). Applied across ~918
  rare-eligible prefix rows + ~726 suffix rows, exact `.5` boundary values *will* occur (e.g.
  any `levelreq` where `req × 0.85` lands on `k.5`), and the two conventions disagree there.
- Why it matters: Eric's emphasis is "the math must be correct." An unpinned rounding rule
  makes the broad compression non-deterministic and means an implementer and a verifier can
  legitimately disagree on a handful of rows. (Note: the charm `× 5` step itself is exact —
  this only affects the `× 0.70` / `× 0.85` level compression.)
- Suggested fix: State the convention explicitly in the design, e.g. "round half up
  (`floor(x + 0.5)`)". The four worked examples in `design.md` (35, 36, 57, 64) happen to
  have no `.5` ambiguity, so pinning the rule does not change them.
- Blocks approval: Should be pinned before the broad compression is implemented.

### Low

**LOW-001 — The suffix-scaling rationale ("keep prefix and suffix pools internally
consistent") is conceptually wrong**

- Design section: "Level 90 Large Charm Suffix Pool Audit".
- Issue: Prefix and suffix are independent draws; there is no "consistency between prefix and
  suffix pools" to maintain — a frequency in one has zero effect on the other. Scaling the
  suffix pool `× 5` when it has no skill rows and no Greater rows is a pure no-op.
- Why it matters: The arithmetic (88 → 440) is fine and harmless, but the stated reason is a
  non-concept and could mislead future edits.
- Suggested fix: Reframe — the suffix `× 5` is only *needed* if Greater suffix rows are added
  to charms (the canonical design lists `Greater Inertia` / `Greater Balance` charm-suffix
  candidates at lines 214–215). Tie the suffix scaling decision to that scope. If no Greater
  suffix rows are in scope, the suffix `× 5` can simply be skipped.
- Blocks approval: No.

**LOW-002 — Group and frequency of the new Greater charm rows are under-specified in the
charm section**

- Design section: "Proposed Large Charm Skill Rows".
- Issue: (a) The new Greater `+2 skill tree` rows must be `group=125` so a charm cannot roll
  both a `+1` and a `+2` skill-tree prefix in separate slots. The general Greater policy does
  state "same `group` as the normal family" (canonical design line 159), but the charm
  section does not restate it — easy to miss at implementation. (b) `Greater Inertia` /
  `Greater Balance` (if in scope) have no stated frequency: the general Greater band shape is
  `1/2/3` across three rows, but the charm Greater rows are single-band `frequency=1`.
- Suggested fix: State explicitly in the charm section that all 24 Greater `+2 skill tree`
  rows are `group=125`, `spawnable=0`, `rare=1`, `frequency=1`; and specify the frequency for
  any Greater charm-suffix rows.
- Blocks approval: No.

**LOW-003 — The Greater skill-row level is derived by "compressing" an invented baseline**

- Design section: "Proposed Large Charm Skill Rows" — `round(81 × 0.70) = 57`,
  `round(75 × 0.85) = 64`.
- Issue: The Greater `+2 skill tree` rows are brand-new; there is no existing row to
  "compress." `81` / `75` are invented baselines, so the `round(... × 0.70)` dressing is
  artificial — the rows should simply be authored at their intended final values.
- Suggested fix: State the Greater skill rows directly as `level=57`, `levelreq=64` (the
  values are reasonable). Drop the `round(81 × 0.70)` derivation or relabel `81`/`75` as
  "chosen design targets" rather than implying compression of an existing row.
- Blocks approval: No.

**LOW-004 — The "Representative charm frequency conversions" table is not exhaustive**

- Design section: "Proposed Existing Charm Frequency Scaling".
- Issue: The table lists current frequencies `1,2,3,4,6,12,24`. The actual charm data also
  contains `frequency` values `5` and `8` (prefix) and `5`, `10`, `20` (suffix). They are
  absent from the table.
- Why it matters: Minor — `× 5` of any integer is exact (`5→25`, `8→40`, `10→50`, `20→100`),
  so there is no rounding risk. But a non-exhaustive table could make an implementer hesitate
  on an unlisted value.
- Suggested fix: Either complete the table or state plainly "apply `× 5` to every existing
  charm `frequency`; the table is illustrative."
- Blocks approval: No.

## Validation Checks

- **Original user request reviewed:** Yes. The request asks for proportion-preserving charm
  scaling; the proposal achieves this for all non-307, non-Warlock rows. The two literal
  divergences (Warlock 1→10, `levelreq` −15%) are flagged as MED-001 / MED-002 for explicit
  sign-off, per protocol.
- **Design reviewed:** Yes — `request.md`, the task `design.md`, and
  `docs/rare-item-rework-design-2026-05-18.md` reviewed in full. This is
  `phase: design_review`; no implementation exists, so there is no diff/patch to check.
- **Data claims independently verified:** Yes — against
  `data/global/excel/magicprefix.txt` and `magicsuffix.txt` (active Reign-of-the-Warlock
  files). 24 skilltab rows (21×freq2 + 3×freq1), 65-row/279-freq level-90 prefix pool,
  15-row/88-freq suffix pool, all scaled totals and percentages, and the group-307
  itype-sharing all confirmed. The `rare=1` eligibility filter reproduces 65/279 exactly.
- **TSV column counts checked:** N/A this round — no TSV edits yet. Both files have 40
  columns; a `code_review` round must check column counts once Codex writes the edits.
- **Active/base sync checked:** Not applicable to the math, but flagged for implementation —
  both `data/global/excel/` (active) and `data/global/excel/base/` contain
  `magicprefix.txt` / `magicsuffix.txt`. The design audits the active file; the
  implementation must state whether base is also edited or deliberately left alone.
- **Tooltip vs gameplay consistency considered:** Greater rows use a `greater-affix-marker`
  mod for the orange tooltip line; the marker needs a free `modX` slot. The `skilltab` rows
  use only `mod1`, so the Greater `+2 skill tree` rows have two free slots — the marker fits.
  No tooltip risk for the charm skill rows specifically.
- **Live publish risk considered:** Yes — `live_publish_allowed: false`; design-only, no
  publish. When implemented: `frequency` edits are save-safe (no row add/remove, no index
  shift). Adding the 24 Greater rows appends new rows — safe as long as they go at end of
  file and existing row order is preserved.
- **Docs checked:** Yes. Recommend the implementation record, in `docs/modding-findings.md`:
  the group-307 itype-sharing finding (HIGH-001), and the decisions taken on MED-001 /
  MED-002 / MED-003.

## Codex Action Items

Before this design can move to implementation:

1. **(HIGH-001 — required)** Carve `group=307` out of the `scaled_charm_frequency =
   current_frequency * 5` rule. Recommended: exempt 307 entirely (leave at `frequency=1`) and
   document charm pierce as a deliberate non-scaled exception. If pierce must stay
   proportional on charms, split each shared 307 row into charm-only and non-charm-only
   copies first. Do not scale the shared rows in place.
2. **(MED-001 — required)** Get Eric's explicit decision on the Warlock skiller rows:
   normalize to 10 (recommended) vs strict `× 5` to 5. Lock the audit numbers to the chosen
   branch (1410/240/16.74% vs 1395/225/15.86%).
3. **(MED-002 — required)** Get Eric's explicit confirmation that `levelreq` drops 15% (not
   30%) and that the top-affix late row intentionally stays at its original `level`. If he
   meant 30% across the board, change the `levelreq` formula to `× 0.70`.
4. **(MED-003 — required)** Pin the rounding convention in the design (recommend round
   half up, `floor(x + 0.5)`).
5. **(LOW-001)** Reframe the suffix scaling: tie it to whether Greater suffix rows
   (`Greater Inertia` / `Greater Balance`) are in scope; drop the "prefix/suffix consistency"
   rationale.
6. **(LOW-002 / LOW-003 / LOW-004)** In the charm section: state the Greater `+2 skill tree`
   rows are `group=125`, `spawnable=0`, `rare=1`, `frequency=1`; author Greater levels
   directly (57/64) without the `round(81×0.70)` derivation; make the conversion table
   exhaustive or explicitly illustrative.

Resubmit the revised design as round 2 for a quick re-review, then proceed to implementation
plus a `code_review` round on the actual TXT diff.

## Suggested Follow-up Tests

These apply once the design is revised and implemented (a `code_review` round will cover the
diff itself):

1. **Column counts** — `magicprefix.txt` / `magicsuffix.txt` stay at 40 tab-separated
   columns on every edited and every new row.
2. **Charm proportion check (in-game)** — farm a high-ilvl large charm pool; confirm the
   relative frequency of, e.g., resist vs damage vs skill-tree prefixes is unchanged from
   pre-rework (uniform `× 5` predicts identical ratios).
3. **Skill-tree rarity** — confirm a normal `+1 skill tree` prefix and a Greater
   `+2 skill tree` prefix appear at a ~10:1 ratio on ilvl-57+ large charms.
4. **Greater/normal mutual exclusion** — confirm no large charm ever rolls a `+1` and a `+2`
   skill-tree prefix simultaneously (verifies the Greater rows are in `group=125`).
5. **Non-charm pierce unaffected** — confirm rare rings/amulets/gloves/boots/belts/helms at
   ilvl 92 roll elemental pierce at their pre-rework rate (verifies HIGH-001 was handled —
   the shared 307 rows were not scaled in place).
6. **Warlock skiller rate** — confirm Warlock skill-tree charms drop at the rate matching
   Eric's chosen MED-001 branch.
7. **Level compression spot-check** — pick rows whose `level × 0.70` or `levelreq × 0.85`
   lands on a `.5` boundary; confirm they rounded per the pinned MED-003 convention.
8. **Active/base parity** — confirm charm affix behavior matches between the two game modes,
   or matches a documented intentional difference.
