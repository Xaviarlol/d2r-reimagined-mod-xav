---
schema: ai-review-result-v1
task_id: 2026-05-16-1749-orb-rank-tiering-design
round: 2
reviewer: claude
verdict: approved
critical: 0
high: 0
medium: 0
low: 2
requires_codex_changes: false
---

# Claude Review

## Verdict
Approved

## Summary

Round 2 re-review of the ranked Conversion/Assemblage orb design. Codex accepted all 8 round-1 findings (1 High, 2 Medium, 5 Low) and revised `design.md` accordingly. I verified every fix against the updated design and the live repo data. All resolved correctly — the design is approved to proceed to implementation.

**Round-1 findings — verification:**

- **HIGH-001 (boss weights)** — ✅ Fixed. Boss selector TCs now `ooa 3 / oa2 2 / oa3 1` and `ooc 3 / oc2 2 / oc3 1`. Design line 288 states the resulting probabilities as rank I = 1/2, rank II = 1/3, rank III = 1/6 — matching Eric's "1 in 3 / 1 in 6" exactly. The design also now explicitly says to preserve the `Mephistoq`/`Diabloq` `Picks=-2` and only swap the Item reference to the selector TC — which is the correct two-level structure.
- **MED-001 (jewelry `lvl` mechanism)** — ✅ Fixed. Jewelry recipes are now explicitly "gated behind verification" with an implementation gate (design line 237): verify on a scratch branch that cube output `lvl=40` actually prevents higher-qlvl unique/set jewelry before any publishable jewelry recipes land. Armor/weapon tiering may proceed independently. This is exactly the split I recommended.
- **MED-002 (active/base divergence)** — ✅ Fixed. Design line 42 "Round 2 decision: normalize active and base treasure classes to the active loose-orb structure" and de-reference the legacy base-only `Jewelry Orbs Single`/`Stack` split. Explicit decision made.
- **LOW-001 (`9x ooc` target)** — ✅ Resolved. Eric confirmed `9x ooc = oc3` / `3x oc2 = oc3` (per request.md "User Confirmation" and design line 166). Same pattern applied to Assemblage.
- **LOW-002 (`bas` = normal tier)** — ✅ Addressed. Design line 119 documents the evidence: the salvage recipes award 1/2/3 Orbs of Infusion split by `bas`/`exc`/`eli`. That's solid proof — if `bas` matched all tiers, the "1 orb" normal recipe would also catch exceptional/elite items and the 2/3-orb recipes would be unreachable. `bas` is normal-tier-exclusive.
- **LOW-003 (description plumbing)** — ✅ Fixed and verified accurate. Design specifies `spelldesc=2`, `spelldescstr`, `spelldescstr2`. I confirmed against the live `ooc`/`ooa` misc rows: both have `spelldesc=2`, `spelldescstr=oocDescription/ooaDescription`, `spelldescstr2` identical, and the `oocDescription`/`ooaDescription` keys exist in `item-names.json`.
- **LOW-004 (`normcode`/`ubercode`/`ultracode`)** — ✅ Fixed. Design line 64-71 now explicitly requires all five identity columns (`code`, `namestr`, `normcode`, `ubercode`, `ultracode`) set to the new code on each of the 4 new misc rows.
- **LOW-005 (`Jewelry Orbs.NoDrop`)** — ✅ Confirmed. Design line 267 states `Jewelry Orbs.NoDrop=0` in active, and the base `Jewelry Orbs Single/Stack` also `NoDrop=0`, so the weight math needs no NoDrop term.

No round-1 finding is unresolved. No new High/Medium issues found in the round-2 design. Two trivial Low notes follow — neither blocks the design; both are guidance for the implementation phase.

## Findings

### Critical
None.

### High
None.

### Medium
None.

### Low

**LOW-201 — Resolving the open "rank I rename" question (design line 60)**

- Design section: "Code Scheme".
- Issue: The design still flags as an open question whether rank I's visible name should become "Orb of Conversion I" / "Orb of Assemblage I". 
- Resolution: **Yes, rename rank I to include the "I".** This is safe — the item *code* stays `ooc`/`ooa` (so existing player inventories and saves are unaffected; codes are the save-relevant identity), and only the display string changes. Without the roman numeral, players can't distinguish a rank-I orb from rank II/III in their inventory. Pure cosmetic change, zero save risk.
- Suggested action: Update the `ooc`/`ooa` name strings in `item-names.json` to "Orb of Conversion I" / "Orb of Assemblage I".
- Blocks approval: No.

**LOW-202 — Promotion recipes consume loose `ooc`/`ooa`; players holding the `1oc`/`1oa` stack form would need to unstack first**

- Design section: "Orb Promotion Recipe Plan" / "Stack Support".
- Issue: The promotion recipes use loose-item `qty` syntax (`ooc,qty=3`, `ooc,qty=9`). The mod also has stackable forms `1oc`/`1oa` (`maxstack=100`). A player who has accumulated a `1oc` stack could not feed it directly into `3x ooc -> oc2` — the recipe matches loose `ooc`, not the `1oc` stack item.
- Why it matters: Minor / edge case. The common path is fine: drops and the `11x ooi + gmt` recipe produce loose `ooc`, which the promotion recipes accept. It only matters for players who deliberately stacked their orbs into `1oc`. The design defers rank II/III stacks (reasonable), so this is consistent.
- Suggested action: No change required for this design. Optionally, when implementing, decide whether an `1oc -> ooc` unstack path is worth adding, or just document in `modding-findings.md` that promotion works on loose orbs. Not a blocker.
- Blocks approval: No.

## Validation Checks

- Original user request reviewed: **Yes** — original request + both follow-up clarifications + the round-2 "User Confirmation" (`9x ooc = oc3`). The design now matches all of Eric's stated intent, including the boss-specific "1 in 3 / 1 in 6" odds (HIGH-001 fix).
- Git diff or design reviewed: **Yes** — `design.md` round-2 revision and `codex-response-r01.md` both reviewed. `phase: re_review`, round 2. No implementation/diff yet — that's the next phase.
- TSV column counts checked: **N/A this round** — still design-only, no TSV edits. The design's "Validation Plan After Implementation" item 1 commits to column-count checks; that will be exercised in the eventual `code_review` round.
- Active/base sync checked: **Yes (decision level)** — MED-002 is resolved: the design now commits to normalizing active and base `treasureclassex.txt` to the active loose-orb structure. The actual byte-level sync will be checked in the `code_review` round.
- Tooltip vs gameplay consistency considered: **Yes** — description plumbing (`spelldesc=2` + `spelldescstr`/`spelldescstr2`) is specified and verified against the existing `ooc`/`ooa` rows. Orb descriptions will state the required base tier per rank. LOW-201 recommends the rank-I name also carry the "I" so the tooltip identity is unambiguous.
- Live publish risk considered: **Yes** — `live_publish_allowed: false`; design-only, no publish. For the eventual implementation: appending new misc rows (new codes, new end-of-file indices) is save-safe; the one behavior change existing players will notice is rank-I orbs no longer working on exceptional/elite items once the all-tier `armo,rar`/`weap,rar` recipes are replaced.
- Docs checked: **Yes** — `docs/modding-findings.md` is in the files-to-change list. Recommend the implementation records: the `bas`/`exc`/`eli` tier-qualifier semantics, the cube-`lvl`-gates-jewelry-pool verification result (MED-001 outcome), and the active/base treasureclassex normalization (MED-002).

## Consensus Status

This round-2 verdict is **Approved** with **0 Critical and 0 High**. Codex accepted and fixed all round-1 findings (per `codex-response-r01.md`). Per the consensus rule, the design-review stage has reached consensus — the design is approved to move to implementation. Codex marks the task complete; Claude does not.

Note this closes the *design_review* only. The actual implementation should come back as a fresh **`code_review`** task (or a new round on this task with `phase: code_review`) so the TSV/JSON diff can be checked for column counts, active/base byte-sync, recipe correctness, and the items in "Suggested Follow-up Tests" below.

## Codex Action Items

None required — design approved. **For the implementation phase**, carry forward:

1. Apply LOW-201: rename rank-I orbs to "Orb of Conversion I" / "Orb of Assemblage I" in `item-names.json`.
2. Honor the MED-001 gate: do NOT include the jewelry `lvl`-cap recipes in the first publishable implementation until the cube-`lvl`-gates-unique-pool behavior is verified on a scratch test. Armor/weapon + orb-promotion + drop-weight + boss-selector changes can all proceed in the first implementation.
3. Ensure all 8 current conversion recipes (amu/armo/rin/weap × ooc/ooa) are accounted for: armo/weap replaced by tiered versions, amu/rin replaced by the (gated) jewelry versions — no stale all-tier recipe left behind.
4. Submit the implementation as a `code_review` task/round.

## Suggested Follow-up Tests

Carried forward from round 1, to be run against the actual implementation:

1. **Code uniqueness** — re-confirm `oc2`/`oc3`/`oa2`/`oa3` are still free at implementation time.
2. **Tier gating (armor/weapons)** — normal rare + rank I works; + rank II/III no match. Exceptional + rank II works; + I or III no match. Elite + rank III works; + I or II no match. Both Conversion and Assemblage.
3. **Old all-tier recipe removed** — exceptional rare armor + rank I `ooc` must NOT convert.
4. **Promotion recipes** — `3x ooc->oc2`, `9x ooc->oc3`, `3x oc2->oc3` and the three Assemblage equivalents; all fit the 12-slot cube (max 9 inputs) and yield exactly one output orb.
5. **Rank-I recipes unchanged** — `11x ooi + gmt -> ooc`, `11x ooi + gme -> ooa` still work.
6. **Generic drop weighting** — `Jewelry Orbs` sample: rank I conversion/assemblage keep ~20% internal share each; II/III near 6.7% / 3.3%.
7. **Boss quest drop** — first-kill Mephisto/Diablo over many runs: rank distribution ≈ 50% / 33% / 17% (I/II/III).
8. **Jewelry `lvl` gate (MED-001 verification)** — the prerequisite test: confirm cube output `lvl=40` excludes uniques/sets with qlvl > 40 before the jewelry recipes are committed.
9. **Active/base parity** — TSV byte-sync of `misc.txt`, `cubemain.txt`, `treasureclassex.txt` after the normalization; same orb behavior in both game modes.
10. **Save safety** — a pre-change character holding loose `ooc`/`ooa` still has working rank-I orbs after the update.
