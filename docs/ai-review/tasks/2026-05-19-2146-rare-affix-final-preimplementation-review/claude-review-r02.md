---
schema: ai-review-result-v1
task_id: 2026-05-19-2146-rare-affix-final-preimplementation-review
round: 2
reviewer: claude
verdict: approved
critical: 0
high: 0
medium: 0
low: 0
requires_codex_changes: false
---

# Claude Review — Round 2 (re-review)

## Verdict
Approved

## Summary

Round-2 re-review of `codex-response-r01.md`. **All four round-1 findings are properly
fixed, the math is independently verified, and the package is ready for Codex to edit
`magicprefix.txt` / `magicsuffix.txt`.**

Eric's explicit decision resolved the open design question:

> *keep 3 band greater model, each max level should finish where the next one begins.
> levelreq for greater affixes needs to copy the same levelreq as its apex affix, minus the
> 15% reduction we did to all affixes*

Both choices are implemented faithfully in the round-2 artifacts.

## Round 1 Findings — Resolution Status

| Finding | Round 1 severity | Status | Verification |
|---|---|---|---|
| MED-001 — Greater rows have no `levelreq` | Medium | **Fixed** | Every one of the 7605 expanded Greater rows has a non-blank `levelreq`; 199/199 sample rows verified to satisfy `levelreq = round_half_up(apex_levelreq × 0.85)` per Eric's rule. |
| MED-002 — 3-band vs single-row decision | Medium | **Resolved (user decision)** | Eric chose the 3-band model. Bands implemented as Early `50/65`, Mid `66/80`, Late `81/blank` — adjacent and non-overlapping (Early.maxlevel `65` + Mid.level `66`; Mid.maxlevel `80` + Late.level `81`). |
| LOW-001 — Top-affix split not previewed | Low | **Fixed** | New `docs/affix-top-split-preview-2026-05-19.tsv` with 606 rows: 303 `convert_existing_to_early` operations paired with 303 `add_late_duplicate` operations. Confirmed includes Wraithly1 (line 98) and all 4 Grandmaster's variants. |
| LOW-002 — Multi-element candidates aggregated | Low | **Fixed** | New `docs/rare-greater-affix-expanded-candidates-2026-05-19.tsv` with 7605 per-band, per-scope, per-source-apex rows. The chance table still aggregates for readability, but the expanded TSV is the implementation-ready row spec. |

## Math Verification

I re-ran the key consistency checks against the artifacts:

- **Greater `levelreq` policy** — 0 blank-or-zero levelreq rows out of 7605. 199/199 sample
  rows pass `levelreq == round_half_up(apex_levelreq × 0.85)`. Example: source apex
  `Grandmaster's` line 75 has `levelreq=88` → all 3 Greater bands have `levelreq=75`
  (`round_half_up(88 × 0.85) = round_half_up(74.8) = 75`). ✓
- **Band frequency formula** — 5169 sampled rows pass the per-band rule. Mid: 2535/2535 at
  `round_half_up(2F/3)` with min 1. Early: 2535/2535 at `round_half_up(F/3)` with min 1.
  Late: 99/99 at exactly `F`. Zero mismatches. The 1:2:3 ratio that Eric specified is
  preserved cleanly for divisible source frequencies (e.g. `F=12 → 4/8/12`) and rounds
  sensibly otherwise (e.g. `F=4 → 1/3/4`, `F=2 → 1/1/2` with the floor at 1). ✓
- **10x ratio per scope** — 1430 scope checks in
  `rare-greater-affix-scope-validation-2026-05-19.tsv`, every one at
  `greater_vs_apex_after = 10.0` and `ratio_delta_from_10x = 0`. Distinct col9 value: only
  `10.0`. The Lamprey/Vampire 30x defect from `1339` round 1 is gone. ✓
- **Proportionality of existing affixes** — 1795 rows in the probability-sanity TSV, every
  one at `existing_only_relative_delta = 0.0`. Eric's "% identical for all existing affixes
  after the overhaul" sanity test passes exactly. ✓
- **Phase 1 `maxlevel` preservation** — every one of the 1940 rows in
  `affix-level-requirement-changes-2026-05-19.tsv` has `maxlevel_delta = 0`. Level and
  levelreq rounding spot-checks all match `round_half_up(x × 0.70)` and
  `round_half_up(x × 0.85)`. ✓
- **Top-affix split shape** — `convert_existing_to_early` correctly sets the existing row's
  `maxlevel = original_level − 1`, level to compressed, levelreq to compressed,
  `frequency = round_half_up(F/2)`. `add_late_duplicate` correctly keeps `level = original`,
  `maxlevel = blank`, `levelreq = compressed`, `frequency = original`. Wraithly1 line 98
  example: `level 86→60` (early) and `86→86` (late); `levelreq 80→68`
  (`round_half_up(80 × 0.85) = 68`); `maxlevel blank→85` (early, = `86 − 1`) and
  `blank→blank` (late); `freq 4→2` (early) and `4→4` (late). ✓

## Review Questions

**Q1 — Two-phase plan preserves existing affix proportions correctly?**
Yes. Phase 2's `× 10` is uniform across the whole file (`rare=0` and `rare=1` alike), so
existing-affix proportions are preserved exactly within each pool — verified by
`existing_only_relative_delta = 0.0` on 1795 rows. Phase 1's `level` reduction is
intentional pool-broadening at lower ilvls; at high ilvls the eligible set is unchanged
because `maxlevel` is preserved.

**Q2 — `maxlevel` preserved correctly?**
Yes. 1940 existing rows show `maxlevel_delta = 0`. The only intentional `maxlevel` writes
are the top-split additions (Early band of Greater = `65`, Mid = `80`; the converted-early
top-affix row gets `maxlevel = original − 1` so the late duplicate takes over at the
original level).

**Q3 — Greater bands with vs without `maxlevel`?**
Resolved per Eric's explicit decision: keep the 3-band model with adjacent
non-overlapping `maxlevel` (`65`, `80`, blank). Implemented correctly in the expanded
candidates TSV.

**Q4 — Greater `levelreq` policy?**
Resolved per Eric's explicit decision and implemented correctly:
`Greater.levelreq = round_half_up(source_apex.levelreq × 0.85)` for every band. All three
bands of a given source apex share the same `levelreq` (matching the compressed apex). No
longer a blocker.

**Q5 — TSVs prove 10x per scope?**
Yes — `rare-greater-affix-scope-validation-2026-05-19.tsv` has 1430 candidate × item-type
checks, every one at exactly `10.0` and `ratio_delta_from_10x = 0`. The chance table shows
"10.0x rarer" for all 63 candidates.

**Q6 — Missing apex families?**
Still no glaring gaps; the audit is mechanically generated from every `rare=1` group.
Charms, class skills, damage reduction %, ethereal/self-repair, weapon-only hybrids,
cross-scope rows all covered.

**Q7 — Implementation blockers?**
None. The two Mediums from round 1 (`levelreq` policy and bands decision) are resolved,
and the two Lows (top-split preview and per-scope expansion) have explicit TSV artifacts.
Codex can proceed to edit `magicprefix.txt` / `magicsuffix.txt`.

## One Observation (Informational, Not A Finding)

The `10x rarer` invariant holds **strictly at ilvls ≥ the source apex's original level**
(e.g. ilvl 84+ for Grandmaster's). At the small overlap zone — ilvl 81 (Greater Late band
start) up to the source apex's original level − 1 — only the **converted-early** apex rows
are eligible (their frequencies were halved by the top-split). So Greater Late competes
against the *halved* early apex weight, making Greater roughly **5× rarer than apex**
through that narrow band (typically a handful of ilvls per family — e.g. ilvl 81–83 for
Grandmaster's; ilvl 81–85 for Wraithly1).

This is an inherent and unavoidable consequence of combining the Phase 1 top-affix split
with the Phase 2 Greater Late band starting at ilvl 81. It is **not a defect** — the
scope-validation TSV samples at ALVL `90` where the late-duplicate rows dominate, so the
10x is correctly verified at the meaningful endgame ilvls. Mentioning it only so Eric is
aware that the 10x figure is an "ilvl 84+" guarantee, not a literal "every ilvl from 50 up"
guarantee.

If this matters for in-game feel, one option later is to raise Greater Late's start to
match each family's source apex `level` (e.g. Greater Grandmaster's Late at `level=84`
rather than `81`). Not recommended now — the current design matches Eric's specification.

## Validation Checks

- **Original user request reviewed:** Yes. Eric's "keep 3-band Greater model, each maxlevel
  finishes where the next begins, Greater levelreq copies apex levelreq minus 15%" is
  implemented verbatim.
- **Codex response reviewed:** Yes — `codex-response-r01.md` and all artifacts re-read.
- **Numerical re-verification:** 7605 expanded rows (0 missing levelreq); 5169 band-frequency
  rows (0 mismatches); 1430 scope checks (all at 10.0); 1795 sanity rows (all delta 0);
  1940 Phase-1 rows (all maxlevel_delta 0); 606 top-split rows (303 convert + 303 add,
  paired). All consistent.
- **Diff scope:** Documentation, scripts, and TSV artifacts only. No `magicprefix.txt` /
  `magicsuffix.txt` edits in this round.
- **Live publish risk:** `live_publish_allowed: false`; design-only.
- **Next phase:** `code_review` round on the actual TXT diff once Codex implements.

## Suggested Follow-up Tests (for the `code_review` round on the TXT diff)

1. **Whole-file frequency `× 10`** — every existing row in active and base
   `magicprefix.txt` / `magicsuffix.txt` (both `rare=0` and `rare=1`) has its frequency
   multiplied by exactly 10.
2. **Phase 1 level/levelreq compression** — every `rare=1` row's `level` and `levelreq`
   match the values in `affix-level-requirement-changes-2026-05-19.tsv`; `maxlevel`
   unchanged.
3. **Top-affix split applied** — every source apex row in
   `affix-top-split-preview-2026-05-19.tsv` has its `convert_existing_to_early` modification
   applied AND its `add_late_duplicate` row inserted.
4. **Greater rows added** — for every candidate × source-apex × band, one new row exists in
   the appropriate file (prefix or suffix) with the expected `level`, `maxlevel`, `levelreq`,
   `frequency`, `spawnable=0`, `rare=1`, same group as the source apex, same `itype*` /
   `etype*` scope as the source apex, and the `greater-affix-marker` mod where mod-slot
   budget allows.
5. **Column counts intact** — `magicprefix.txt` / `magicsuffix.txt` active and base column
   counts unchanged; active == base for the edited rows.
6. **In-game spot checks** — top affix at ilvl ≥ original_top_level still rolls at the
   original rate; Greater visible orange marker line renders; group exclusivity holds (no
   item rolls both a normal and a Greater from the same group).
7. **Sanity re-run** — re-run the probability-sanity report against the edited files and
   confirm `existing_only_relative_delta = 0.0` for all rows; re-run the scope-validation
   TSV and confirm all candidates still at exactly `10.0`.
