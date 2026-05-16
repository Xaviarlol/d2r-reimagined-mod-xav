---
schema: ai-review-result-v1
task_id: 2026-05-16-1749-orb-rank-tiering-design
round: 1
reviewer: claude
verdict: needs_fixes
critical: 0
high: 1
medium: 2
low: 5
requires_codex_changes: true
---

# Claude Review

## Verdict
Needs fixes

## Summary

This is a **design review** (no code written yet) for ranked Orb of Conversion / Orb of Assemblage. The design is well-researched — it correctly identifies the 3-char item-code limit, picks free codes, uses the right cube qualifiers, provides real jewelry-pool counts, and flags its own riskiest assumption (the jewelry `lvl` mechanism). Most of it is implementable as written.

I verified the design's factual claims against the repo:
- **Codes `oc2` / `oc3` / `oa2` / `oa3` are all free** — confirmed unused in `misc.txt`, `weapons.txt`, `armor.txt`. ✓
- **`ooc` / `ooa` are loose (`maxstack=0`); `1oc` / `1oa` are the stacks (`maxstack=100`)** — matches the design's "Current State". ✓
- **`bas`/`exc`/`eli` rare qualifiers exist** — 4 cubemain rows use `armo,bas,rar` / `armo,exc,rar` / `weap,bas,rar` / `weap,exc,rar`. ✓
- **Quest boss TCs `Mephistoq` / `Diabloq` use `Picks=-2`** (guaranteed-drop mode), with Item1 currently pointing at the `Assemblage Orb` / `Conversion Orb` sub-TCs. Baal's quest TC drops `Corruption Orb`, a different item — correctly excluded from this design. ✓

The design is mostly sound, but it cannot be approved for implementation as-is because of **HIGH-001**: the boss quest-drop weighting (`6/2/1`) does not match Eric's explicit "1 in 3 / 1 in 6" probabilities. There are also two Medium items (jewelry `lvl` mechanism is unverified; active/base treasureclassex divergence needs an explicit decision) and several Low spec-completeness gaps. Fix HIGH-001 in the design doc, address the Mediums, then this is good to implement.

## Findings

### Critical
None.

### High

**HIGH-001 — Boss quest-drop weights `6/2/1` do not match Eric's "1 in 3 / 1 in 6" request**

- Design section: "Boss Quest-Drop Plan".
- Issue: The design proposes `Assemblage Orb Quest -> ooa weight 6, oa2 weight 2, oa3 weight 1` (and the same for Conversion). With weights `6/2/1` the distribution is **rank I = 66.7%, rank II = 22.2%, rank III = 11.1%**. Eric's request says: *"1 in 3 chance to drop Rank 2 instead of rank 1, 1 in 6 chance to drop rank 3 instead of rank 1."* "1 in 3 chance" is an absolute probability (P = 1/3), not a relative weight ratio. The distribution Eric described is **rank II = 1/3, rank III = 1/6, rank I = remaining 1/2** → weights **`3 / 2 / 1`** (3+2+1 = 6; 3/6 = 1/2, 2/6 = 1/3, 1/6 = 1/6).
- Why it matters: This is review priority #1 — judge against the original request. Eric deliberately used *different wording* for the two cases: generic drops are "roughly 3x / 6x rarer" (a rarity ratio → `6/2/1` is correct there) while the boss drop is "1 in 3 / 1 in 6 chance" (absolute odds → `3/2/1`). The design correctly used `6/2/1` for the generic `Jewelry Orbs` TC but incorrectly reused `6/2/1` for the boss selector. As designed, the boss would hand out rank II/III noticeably less often than Eric asked.
- Suggested fix: Change the boss selector TCs to `ooa 3 / oa2 2 / oa3 1` and `ooc 3 / oc2 2 / oc3 1`. Keep the generic `Jewelry Orbs` weighting at `6/2/1` (that one is correct). Implementation note: `Mephistoq` and `Diabloq` use `Picks=-2` (guaranteed drop, each Item slot is a fixed quantity). The chain stays two-level: `Mephistoq` (Picks=-2, Item1 → `Assemblage Orb Quest` qty 1) → `Assemblage Orb Quest` (Picks=1, weighted `3/2/1`). Only the Item1 reference on `Mephistoq`/`Diabloq` changes from `Assemblage Orb`/`Conversion Orb` to the new `*Quest` selector TC — preserve `Picks=-2`.
- Blocks approval: **Yes** — design must be corrected before implementation, or Eric must explicitly re-approve `6/2/1` if he actually meant a rarity ratio for the boss too.

### Medium

**MED-001 — Jewelry `lvl`-cap mechanism is unverified and is a single point of failure for the whole jewelry plan**

- Design section: "Jewelry Plan" (the design flags this itself at the "Important review question" line).
- Issue: The plan restricts rank I/II/III jewelry to lvl 40 / 70 / 99 by setting the cube recipe output `lvl`. This only works if cube output `lvl` sets the generated item's **ilvl before** unique/set selection, so that only uniques/sets with `lvl` (qlvl) ≤ the cap are eligible. If `lvl` instead only stamps a level on the item *after* the unique/set is already chosen, the cap does nothing and rank I could roll a level-99 unique amulet.
- Why it matters: D2's cube-generated unique/set selection picks from uniqueitems.txt / setitems.txt rows whose `lvl` ≤ the item ilvl. `cubemain.txt`'s `lvl` column is documented as "forces the item to spawn at a specific level" — which *should* mean it sets ilvl and therefore gates the pool. But "should" is not "verified", and the entire jewelry tiering depends on it. If it doesn't work, jewelry tiering needs a different lever (e.g., separate jewelry-specific output codes, or accepting that jewelry can't be tiered the same way).
- Suggested fix: Before committing the jewelry recipes, run a controlled test — one cube recipe `amu,rar + <orb> -> amu,uni` with `lvl=40`, transmute repeatedly, and confirm zero results are uniques whose qlvl > 40. Recommend **splitting the jewelry portion into its own implementation sub-step** gated on this verification, so the armor/weapon tiering (which uses the proven `bas/exc/eli` mechanism) can proceed independently.
- Blocks approval: Partial — the armor/weapon portion is fine; the jewelry portion should not be implemented until the `lvl` behavior is confirmed.

**MED-002 — Active/base `treasureclassex.txt` divergence must be resolved before adding ranked-orb TC entries**

- Design section: "Current State" (the paragraph noting base has `Jewelry Orbs Single` / `Jewelry Orbs Stack` while active does not).
- Issue: The design itself notes the active and base `treasureclassex.txt` have different shapes for the orb TCs. This is the same active/base divergence I flagged in task `2026-05-14-0046-orb-stack-conversion-recipes` (active "Infusion Orb" TC drops loose `ooi`, base drops the `1oi` stack). Adding ranked-orb TCs on top of an already-divergent pair of files risks compounding the drift — and the project convention is that active/base should be deliberately in sync or deliberately documented as different.
- Why it matters: If the new ranked-orb TC rows are added to one file's shape but not the other's, the two game modes (Reign of the Warlock = active, Classic/Expansion = base) will behave differently for orb drops, and future scripts/reviews can't tell intentional from accidental.
- Suggested fix: Before implementation, make an explicit decision: (a) normalize active and base to the same TC structure as part of this work, or (b) keep them intentionally different and document why in `docs/modding-findings.md`. Recommend (a) — pick one structure (loose-orb or stack-aware) and mirror it. Given the mod's primary mode is the active Reign of the Warlock files, follow the active pattern and bring base into line.
- Blocks approval: Partial — the design should state which path it's taking before the treasureclassex edits land.

### Low

**LOW-001 — Confirm the `9x ooc` recipe target with Eric (literal text says `oc2`, design assumes `oc3`)**

- Design section: "Orb Promotion Recipe Plan".
- Issue: Eric wrote `9xOOC = 1x OC2`; the design assumes a typo and implements `9x ooc -> oc3`. Codex's interpretation is almost certainly correct — taking the text literally (`9 ooc -> oc2`) would be a strictly-worse trap recipe than the `3 ooc -> oc2` recipe (a player would waste 6 orbs), so no rational player would use it, and `9 ooc -> oc3` keeps the economy consistent with `3 oc2 -> oc3`. I concur with `9x ooc -> oc3`.
- Why it matters: It deviates from the literal written request, so per protocol it needs Eric's explicit sign-off rather than a silent assumption.
- Suggested fix: Keep `9x ooc -> oc3` but get a one-line confirmation from Eric. Not a blocker.
- Blocks approval: No.

**LOW-002 — Verify `bas` qualifier matches normal-tier ONLY (not "any base item")**

- Design section: "Cube Recipe Plan".
- Issue: The entire armor/weapon tiering relies on `armo,bas,rar` matching *only* normal-tier rare items, so that rank I (`ooc`) can't convert exceptional/elite. If `bas` actually means "base item of any tier", rank I would over-match. The design assumes `bas` = normal tier; the 4 existing recipes that use `bas` strongly suggest it's correct, but it's worth an explicit confirmation against the existing rare-upgrade recipes' known behavior.
- Suggested fix: Confirm via the eezstreet CubeMain docs or by checking that the 4 existing `*,bas,rar` recipes are known to work on normal-tier items only. Cheap to verify; high impact if wrong.
- Blocks approval: No (but verify before implementation).

**LOW-003 — Orb description text mechanism not specified**

- Design section: "Item Definition Plan".
- Issue: The design specifies `item-names.json` for the orb *names* but only describes the *descriptions* ("Cube with a normal rare item to convert it to Unique.") in prose without saying where that text lives — which `misc.txt` field (e.g. a `spelldescstr` reference) and which string file.
- Suggested fix: Specify the description plumbing — the misc.txt column(s) that point to a description string, and the string-file entries to add. Copy the mechanism the existing `ooc`/`ooa` rows already use for their descriptions.
- Blocks approval: No.

**LOW-004 — New `misc.txt` rows need `normcode`/`ubercode`/`ultracode` set, not just `code`/`namestr`**

- Design section: "Item Definition Plan".
- Issue: The plan mentions setting `code` and `namestr` on the four new misc rows but not `normcode`/`ubercode`/`ultracode`. For a non-tiered item these three should all equal the new `code` (e.g. `oc2`). If they're left as the copied `ooc`/`ooa` values, the new orbs could misbehave in normal/nightmare/hell code resolution.
- Suggested fix: When copying the `ooc`/`ooa` rows, update `code`, `namestr`, `normcode`, `ubercode`, and `ultracode` all to the new code.
- Blocks approval: No.

**LOW-005 — Confirm `Jewelry Orbs` TC has no `NoDrop` weight before finalizing the drop-rate math**

- Design section: "Drop Weight Plan".
- Issue: The design's percentage math (rank I stays at its current share, II/III at 1/3 and 1/6) assumes `Jewelry Orbs` is a clean weighted pick with no `NoDrop`. My inspection of row 20 (`Jewelry Orbs`, Picks=1) didn't surface a populated `NoDrop`, which is consistent with the assumption — but the implementer should explicitly confirm `NoDrop` is blank/0. If `NoDrop` is present, the scaled weights must account for it or the rank-I share will shift.
- Suggested fix: Confirm `Jewelry Orbs.NoDrop` is blank during implementation; if not, include it in the ×6 scaling.
- Blocks approval: No.

## Validation Checks

- Original user request reviewed: **Yes** — original request + both follow-up clarifications (jewelry ilvl caps, promotion recipes). HIGH-001 and LOW-001 are the two places the design diverges from the literal request.
- Git diff or design reviewed: **Yes** — `design.md` reviewed in full. This is `phase: design_review`; no implementation exists yet, so there is no diff/patch to check. Design's factual claims were independently verified against the live repo data (see Summary).
- TSV column counts checked: **N/A this round** — no TSV edits yet. The design's "Validation Plan After Implementation" correctly commits to checking column counts on `misc.txt`, `cubemain.txt`, and `treasureclassex.txt` post-implementation; that will need a `code_review` round once Codex implements.
- Active/base sync checked: **Partially** — confirmed the design correctly identifies a pre-existing active/base `treasureclassex.txt` divergence (see MED-002). No new edits to sync-check yet.
- Tooltip vs gameplay consistency considered: **Yes** — the orb item descriptions must state the required base tier (normal/exc/elite for armor/weapons) and the jewelry behavior; design covers names via `item-names.json` but the description plumbing is under-specified (LOW-003). When implemented, the rank I orb's visible name should gain the "I" so players can distinguish ranks — the design raises this as an open question; recommend yes, rename to "Orb of Conversion I".
- Live publish risk considered: **Yes** — `live_publish_allowed: false`; this is design-only. No publish. When implemented: appending new rows to `misc.txt` (new item codes, new indices at end of file) is save-safe as long as existing row order/indices are not displaced. Replacing/disabling the old all-tier `armo,rar`/`weap,rar` recipes is the one behavior change existing players will notice (rank I orbs stop working on exc/elite).
- Docs checked: **Yes** — design lists `docs/modding-findings.md` in the files-to-change. Recommend the implementation also document: the `bas`/`exc`/`eli` qualifier semantics (LOW-002 outcome), the cube `lvl`-gates-unique-pool finding (MED-001 outcome), and the active/base treasureclassex decision (MED-002).

## Codex Action Items

Before this design can move to implementation:

1. **(HIGH-001 — required)** Correct the boss quest-drop selector weights from `6/2/1` to `3/2/1` for both `Assemblage Orb Quest` and `Conversion Orb Quest`, so rank II = 1/3 and rank III = 1/6 of all quest-boss orb drops, matching Eric's "1 in 3 / 1 in 6". Keep the generic `Jewelry Orbs` weighting at `6/2/1` (that one is right). Note `Mephistoq`/`Diabloq` keep `Picks=-2`; only their Item1 reference changes.
2. **(MED-001 — required)** Either include a verification result that cube output `lvl` gates the unique/set jewelry selection pool, or split the jewelry recipes into a separate implementation step gated on that test. Do not implement the jewelry `lvl`-cap recipes until confirmed.
3. **(MED-002 — required)** State explicitly whether active and base `treasureclassex.txt` will be normalized to one structure or kept intentionally different (with a `modding-findings.md` note). Recommend normalizing.
4. **(LOW-001)** Get Eric's one-line confirmation that `9x ooc -> oc3` (not the literal `oc2`) is intended.
5. **(LOW-002 / LOW-004 / LOW-005)** Fold the three verification/spec-completeness items into the design: confirm `bas` = normal tier only; set `normcode`/`ubercode`/`ultracode` on new misc rows; confirm `Jewelry Orbs.NoDrop`.
6. **(LOW-003)** Specify the orb-description string plumbing (misc.txt field + string file), mirroring how `ooc`/`ooa` already do their descriptions.

Resubmit the revised design as round 2 for a quick re-review, then proceed to implementation + a `code_review` round on the actual diff.

## Suggested Follow-up Tests

These apply once the design is revised and implemented (a `code_review` round will cover the diff itself):

1. **Code uniqueness** — re-confirm `oc2`/`oc3`/`oa2`/`oa3` are still free at implementation time (nothing else claimed them in the interim).
2. **Tier gating, armor/weapons** — normal rare armor + rank I → works; + rank II/III → no recipe matches (cube does nothing). Exceptional rare + rank II → works; + rank I or III → nothing. Elite rare + rank III → works; + rank I or II → nothing. Repeat for weapons and for Assemblage (set output).
3. **Old all-tier recipe removed** — confirm an exceptional rare armor + rank I `ooc` no longer converts (the old `armo,rar` recipe must be gone/disabled).
4. **Jewelry lvl caps (MED-001)** — rank I amulet/ring conversions only roll uniques/sets with qlvl ≤ 40; rank II ≤ 70; rank III full pool. Transmute many times and check the output qlvl distribution.
5. **Promotion recipes** — `3x ooc -> oc2`, `9x ooc -> oc3`, `3x oc2 -> oc3`, and the three Assemblage equivalents. Confirm all fit the 12-slot cube (max input is 9 — fine) and produce exactly one output orb.
6. **Rank-I recipes unchanged** — `11x ooi + gmt -> ooc` and `11x ooi + gme -> ooa` still work.
7. **Generic drop weighting** — sample-farm the `Jewelry Orbs` source and confirm rank I conversion/assemblage keep their pre-change ~20% internal share and II/III land near 6.7% / 3.3%.
8. **Boss quest drop** — first-kill Mephisto and Diablo; over many test runs confirm the rank distribution is ~50% / 33% / 17% (rank I / II / III) per the corrected `3/2/1` weighting.
9. **Save safety** — load a pre-change character holding loose `ooc`/`ooa`; confirm they still exist and still work as rank I after the update (item code `ooc`/`ooa` unchanged).
10. **Active/base parity** — verify orb behavior matches in both game modes, or matches the documented intentional difference.
