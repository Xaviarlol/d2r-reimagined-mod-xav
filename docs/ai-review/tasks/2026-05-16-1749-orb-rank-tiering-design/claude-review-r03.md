---
schema: ai-review-result-v1
task_id: 2026-05-16-1749-orb-rank-tiering-design
round: 3
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

Round 3 (final round) re-review of the ranked Conversion/Assemblage orb design. The round-2 design was already approved; this round covers a small addendum:

1. **New user requirement** — Eric noted rank II/III orbs need stackable slots in the D2R v3 advanced stash. Codex added an `AdvancedStashStackable=1` requirement for the new loose `oc2`/`oc3`/`oa2`/`oa3` rows.
2. **Folded-in round-2 lows** — LOW-201 (rank-I rename) and LOW-202 (loose-orb promotion / `1oc`/`1oa` unstack note) were incorporated into the design body.

Both verified correct against the live repo:

- **AdvancedStashStackable** — Confirmed `ooc`, `ooa`, `ooi` (the loose rank-I orbs) each have `AdvancedStashStackable=1` (column 175) and `maxstack=0`. The old explicit stack items `1oc`/`1oa`/`1oi` have `maxstack=100` and a blank `AdvancedStashStackable`. The design's instruction — set `AdvancedStashStackable=1` on the new loose rank II/III rows — is correct and matches the rank-I pattern. Since the new rows are copied from `ooc`/`ooa` (which already carry the flag), the flag is preserved automatically; the design making it explicit is good belt-and-suspenders. Design lines 80, 310, validation step 3 (line 331), and in-game test 11 (line 351) all cover it consistently.
- **LOW-201** — Design Code Scheme section (lines 60-65) now states `ooc -> Orb of Conversion I` and `ooa -> Orb of Assemblage I`, citing the round-2 finding. Item codes stay `ooc`/`ooa` (save-safe); only display names change.
- **LOW-202** — Design line 312 documents that promotion recipes consume loose `ooc`/`ooa` and that `1oc`/`1oa` stack holders use existing unstack recipes first; direct stack-item promotion is out of scope. Line 310 also clarifies advanced-stash stacking is independent of the old explicit stack-item system.

No conflict introduced: `AdvancedStashStackable` is a stash storage/display feature and is orthogonal to cube recipes. The existing `11x ooi` cube recipe already operates on `ooi` (which has `AdvancedStashStackable=1`), proving the flag and loose-item `qty=N` cube recipes coexist fine — so `oc2`/`oc3` with the flag will work identically with the `3x`/`9x` promotion recipes.

All prior-round findings (round 1: 1 High + 2 Medium + 5 Low; round 2: 2 Low) are resolved. No new issues. The design is complete and approved for implementation.

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

- Original user request reviewed: **Yes** — original request, both early follow-ups, the `9x ooc` confirmation, and the new "stash stacking" follow-up. The design now satisfies all of them, including the v3 advanced-stash requirement.
- Git diff or design reviewed: **Yes** — `design.md` round-3 revision and `codex-response-r02.md` reviewed. `phase: re_review`, round 3 of 3. Still design-only; no implementation/diff yet.
- TSV column counts checked: **N/A this round** — no TSV edits yet. `misc.txt` is 176 columns; new rows copied from `ooc`/`ooa` will inherit 176 columns. Column-count verification belongs to the eventual `code_review` round (design validation step 1 commits to it).
- Active/base sync checked: **Yes (decision level)** — round-2 decision to normalize active/base `treasureclassex.txt` to the active loose-orb structure stands. New `misc.txt` rows must be added to both active and base. Byte-level sync check is for the `code_review` round.
- Tooltip vs gameplay consistency considered: **Yes** — rank-I display names gain the "I"; rank II/III descriptions state the required base tier; `spelldesc=2` + `spelldescstr`/`spelldescstr2` plumbing verified against live `ooc`/`ooa` rows in the round-2 review.
- Live publish risk considered: **Yes** — `live_publish_allowed: false`; design-only. `AdvancedStashStackable=1` on new rows is a storage/UI flag with no save-corruption risk; new misc rows append at end-of-file (no index displacement).
- Docs checked: **Yes** — `docs/modding-findings.md` remains in the files-to-change list. Recommend the implementation records the `AdvancedStashStackable` vs old `stackable=1` distinction (loose orbs use the former; explicit `1oc`/`1oa`-style rows use the latter) since it's a useful D2R v3 modding note.

## Consensus Status

This round-3 verdict is **Approved** with **0 Critical / 0 High / 0 Medium / 0 Low**. Across all three rounds Codex accepted and fixed every finding (round 1: HIGH-001, MED-001, MED-002, LOW-002..005; round 2: LOW-201, LOW-202; round 3: stash-stacking addendum). **Consensus is reached on the design review.** This is `round 3 of max_rounds 3` and it lands cleanly at consensus — no `blocked_needs_info` escalation needed.

The design is approved to proceed to implementation. Codex marks the task complete; Claude does not.

**Next step:** the implementation should return as a fresh **`code_review`** task (new task id, or a new task with `phase: code_review`) so the actual `misc.txt` / `cubemain.txt` / `treasureclassex.txt` / `item-names.json` diff can be checked for column counts, active/base byte-sync, recipe correctness, the `AdvancedStashStackable` flag on the new rows, and the MED-001 jewelry `lvl`-gate verification.

## Codex Action Items

None — design fully approved. Implementation-phase reminders (carried from round 2, still apply):

1. Rank-I orbs renamed to "Orb of Conversion I" / "Orb of Assemblage I" in `item-names.json` (codes unchanged).
2. Set `AdvancedStashStackable=1` on the new `oc2`/`oc3`/`oa2`/`oa3` loose rows (automatic if copying the `ooc`/`ooa` rows — verify it survived the copy).
3. Honor the MED-001 gate: jewelry `lvl`-cap recipes stay out of the first publishable implementation until the cube-`lvl`-gates-unique-pool behavior is verified on a scratch test. Armor/weapon + orb-promotion + drop-weight + boss-selector can ship first.
4. All 8 current conversion recipes (amu/armo/rin/weap × ooc/ooa) accounted for — no stale all-tier `armo,rar`/`weap,rar` recipe left behind.
5. Submit the implementation as a `code_review` task/round.

## Suggested Follow-up Tests

Carried forward for the implementation `code_review` round:

1. **Code uniqueness** — re-confirm `oc2`/`oc3`/`oa2`/`oa3` still free at implementation time.
2. **Stash stacking** — confirm `oc2`/`oc3`/`oa2`/`oa3` stack in the D2R advanced stash stack area, matching `ooc`/`ooa`/`ooi`.
3. **Tier gating (armor/weapons)** — normal+I works / II,III no-match; exceptional+II works / I,III no-match; elite+III works / I,II no-match; for both Conversion and Assemblage.
4. **Old all-tier recipe removed** — exceptional rare armor + rank I `ooc` must not convert.
5. **Promotion recipes** — `3x ooc->oc2`, `9x ooc->oc3`, `3x oc2->oc3` and the three Assemblage equivalents; all fit the 12-slot cube; one output orb each. Confirm they still work with `AdvancedStashStackable=1` items (should — `11x ooi` precedent).
6. **Rank-I recipes unchanged** — `11x ooi + gmt -> ooc`, `11x ooi + gme -> ooa`.
7. **Generic drop weighting** — `Jewelry Orbs`: rank I ≈ 20% internal share each; II/III ≈ 6.7% / 3.3%.
8. **Boss quest drop** — first-kill Mephisto/Diablo: rank distribution ≈ 50% / 33% / 17%.
9. **Jewelry `lvl` gate (MED-001)** — verify cube output `lvl=40` excludes uniques/sets with qlvl > 40 before committing jewelry recipes.
10. **Active/base parity** — TSV byte-sync of `misc.txt`, `cubemain.txt`, `treasureclassex.txt`.
11. **Save safety** — pre-change character holding loose `ooc`/`ooa` still has working rank-I orbs after the update.
