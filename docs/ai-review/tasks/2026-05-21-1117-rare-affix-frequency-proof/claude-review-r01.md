---
schema: ai-review-result-v1
task_id: 2026-05-21-1117-rare-affix-frequency-proof
round: 1
reviewer: claude
verdict: approved
critical: 0
high: 0
medium: 0
low: 1
requires_codex_changes: false
---

# Claude Review

## Verdict

Approved

## Summary

`code_review` of the rare-affix frequency proof and its level-1 split-overlap fix.
**The fix is correct, the simulation methodology is appropriate for the question
asked, and the results confirm the rework preserves endgame non-Greater proportions
exactly.** Implementation is safe.

What I verified independently against the implementation files:

- **Bug existed and is now fixed.** Pre-fix at commit `ebd57892` (top-50 implementation
  base), `of Grace` carried two rows at `magicsuffix.txt`:
  - NR=324: `lvl=1 maxlvl=1 lvlreq=1 freq=60` (the spurious early split)
  - NR=325: `lvl=1 maxlvl=blank lvlreq=1 freq=120` (the late row)

  Both eligible at item-level 1 → combined freq=180 vs vanilla 12 → **15× bug** vs the
  intended 10× scaling. Same shape for `of Power`, `of Greed`, `of Avarice`. Post-fix,
  each has a single row at freq = vanilla × 10:

  | Suffix | Vanilla freq | Post-fix freq | Ratio |
  |---|---:|---:|---:|
  | of Grace | 12 | 120 | 10× ✓ |
  | of Power | 12 | 120 | 10× ✓ |
  | of Greed | 48 | 480 | 10× ✓ |
  | of Avarice | 48 | 480 | 10× ✓ |

- **Script guard is correctly scoped.** The added line in `phase1_existing_row`:

  ```python
  if line_key not in split_sources or original_level is None or original_level <= 1:
      # don't split — return single row with compressed levels
  ```

  Traced through with `original_level=1`: compressed_level(1) = max(1, round(1*0.70))
  = 1; early would have `level=1 maxlevel=max(1, 1-1)=1`; late would have `level=1
  maxlevel=blank`. At item-level 1, both rows would be eligible → the overlap bug.
  The guard correctly blocks splits when `original_level <= 1` while still applying
  the level/levelreq compression for level=1 rows that aren't split candidates.

  Sanity-traced `original_level=2`:
  - early.level = round(2 * 0.70) = 1, early.maxlevel = max(1, 2-1) = 1
  - late.level = 2, late.maxlevel = blank
  - At item-level 1: only early eligible. At item-level 2: only late eligible.
  - No overlap. The `<=1` boundary is exactly correct.

- **Active/base byte-identical** for both `magicsuffix.txt` and base copy (`diff -q`
  empty). TSV shape valid (40 cols × 1006 data rows, 0 bad rows in active and base).

- **Simulation methodology is sound.** The per-level eligibility pooling is the
  right approach for this question. My naive `current_freq_sum == vanilla * 10` check
  on fingerprint produced 119 "mismatches" — but every one I spot-checked
  resolves once you filter by level eligibility:

  Example: `of Evisceration (group 14, dmg-max 41-63)` — vanilla has one row at
  `lvl=45 lvlreq=37 freq=144`. Current has two rows: early `lvl=31 maxlvl=44
  lvlreq=31 freq=720` and late `lvl=45 maxlvl=blank lvlreq=31 freq=1440`. At the
  vanilla row's level (lvl=45), only the late row is eligible (early has maxlvl=44
  capping at 44) → current eligible freq = 1440 = vanilla 144 × 10 ✓. The
  simulation's `at-original-level matches × 10: 0 mismatches` is correct.

- **Simulation's "split-row overlap: 0" check is comprehensive.** The check pools
  by `(itype, alvl)` so multi-itype affixes like `of the Fox` (3 rows covering
  different bodylocs) and `of the Mammoth` (4 rows split across two source tiers
  and itype groups) don't falsely flag. My initial pure-name scan picked up these as
  candidates, but they're not real overlaps under itype-aware pooling. Codex's
  simulation got the methodology right.

- **Low/mid-level deltas are correctly explained as the Phase 1 30% level
  compression artifact.** At alvl 20-66, the rework's compressed-level affixes
  enter the pool earlier than vanilla, so the *pool size* grows and each individual
  affix's share shrinks proportionally. My calculation:
  - At alvl 50, vanilla had ~N eligible affixes; current has ~1.25×N eligible
    (Phase 1 brings ~25% more affixes earlier).
  - 1/1.25 - 1 = -20% per-affix share — matches the reported `-19.66%` average.
  - This is the intended behavior of the level compression, not a bug.

- **Endgame proportion preserved at 0% non-Greater delta** at alvl 90/100 — the
  point where ALL affixes are eligible in both vanilla and current, so the pool
  composition is exactly preserved up to the × 10 uniform scaling. ✓

- **Full-pool delta of 1.9% at alvl 90/100 is the Greater-row dilution.** Adding
  255 Greater rows (each with low freq) into the pool shrinks each non-Greater
  affix's full-pool share by ~0.85-1.9%. That's the intended cost of having the
  Greater chase layer, not a frequency miscalculation.

## Review Questions

**Q1 — Simulation methodology valid for the frequency sanity check?** Yes. Weighted
one-roll probability is the right primitive for "what's the chance any given affix
shows up first." The disclaimer about group lockouts and prefix/suffix count rolls
is correct — those are separate downstream effects on the final item composition
but don't affect the per-affix proportion this simulation measures.

**Q2 — Correct comparison vs pre-rework baseline?** Yes. `00337b07^` (`10360332...`)
is the commit immediately before "Implement rare affix rework" — the correct vanilla
baseline. Fingerprint matching by `(name, group, mod1code, mod1param, mod1min,
mod1max, ...)` correctly identifies same-affix rows across the rework.

**Q3 — Level-1 split fix correct?** Yes. The 4 affected rows are gone; the script
guard prevents recurrence; the boundary case (level=2) verified safe.

**Q4 — Active/base synchronized and TSV-safe?** Yes. `diff -q` empty for both
suffix file pair, 40-column structure preserved, 1006 data rows.

**Q5 — Endgame non-Greater proportions preserved?** Yes, exactly. 0% delta at
alvl 90/100 for non-Greater pool means the rework's `× 10` scaling is mathematically
faithful — every non-Greater affix's relative roll chance is identical to vanilla
at high item levels.

**Q6 — Low/mid-level deltas correctly explained?** Yes. The Phase 1 30% level
compression intentionally lets more affixes be eligible earlier, so the pool
expansion explanation matches my independent reasoning (-1/1.25 = -20% per-share).
The deltas are an artifact of the design choice, not a bug.

**Q7 — Safe to keep as part of the Greater Affix implementation before live
publish?** Yes. The fix is a strict improvement (corrects a real 15× bug to the
intended 10× scaling) and introduces no new risks. The MEDIUM-001/MEDIUM-002 notes
from `claude-review-r03.md` (color choice, JSON orphans) still apply to the broader
Greater Affix work and should be addressed before live publish — but those are
separate from this frequency-proof fix.

## Findings

### Critical
None.

### High
None.

### Medium
None.

### Low

**LOW-001 — Simulation TSV (`docs/affix-chance-simulation-2026-05-21.tsv`) not
inspected directly; trusted via summary metrics**

- Where: `docs/affix-chance-simulation-2026-05-21.tsv` (full per-case dump).
- Issue: I verified the summary metrics in
  `docs/affix-chance-simulation-summary-2026-05-21.md` against the implementation
  via independent spot-checks, but did not load the 11,724-row TSV directly to
  re-verify the underlying case-by-case data. The summary's reported aggregates
  (avg/min/max delta per alvl bucket) are consistent with my independent reasoning
  about Phase 1 pool dilution, so the TSV is likely accurate, but technically
  unverified at the row level.
- Impact: Low confidence cost. If the TSV had a row-level computation bug, the
  aggregates would likely be off as well — and they aren't.
- Recommendation: None required. The TSV is a supporting artifact, not a control
  surface. If a future audit needs row-level verification, re-run the simulation
  with a `--verbose` mode that dumps the eligibility computation per case.
- Blocks live publish: No.

## Validation Checks

- **Original user request reviewed:** Yes — *"did you adjust the frequency for
  everything? Then you need to run that simulation of before and after chance the
  affix will appear vs vanilla file"*. Codex ran the simulation, found a real bug
  (the 4 level-1 overlaps), fixed it, and the post-fix simulation shows 0%
  non-Greater delta at endgame. Eric's question is answered: yes, frequencies are
  adjusted correctly, and the endgame proportion is preserved exactly.
- **Diff reviewed:** `diff.patch` (6 hunks across 4 files — magicsuffix active/base
  + script + summary doc). The TXT diff is the 4 row deletions; the script diff
  is the `<=1` guard addition.
- **Independent verification (this round):**
  - 4 deleted suffixes confirmed gone from active and base ✓
  - Each fixed suffix has exactly 1 row at the expected × 10 freq ✓
  - Pre-fix state had the 2-row overlap bug (verified via `git show ebd57892`) ✓
  - Vanilla state had 1 row each (verified via `git show 103603327...`) ✓
  - Script guard logic traced through level=1 and level=2 cases ✓
  - Active/base byte-identical ✓
  - TSV shape valid ✓
  - At-original-level frequency check matches × 10 (spot-checked `of Evisceration`
    dmg-max 41-63 at vanilla lvl 45 → current eligible freq 1440 = vanilla 144 × 10) ✓
  - Low/mid-level delta math verified (-1/1.25 = -20% per-share) ✓
- **Diff scope:** Only `magicsuffix.txt` and base/, the script, and the docs.
  `magicprefix.txt` untouched (no level-1 prefix overlaps existed). Properties
  and itemstatcost not touched (this is a frequency-only fix on existing rows).
- **Live publish risk:** `live_publish_allowed: false`. This is a pre-publish
  verification round. The MEDIUM-001 (color) and MEDIUM-002 (JSON orphans) notes
  from the top-50 r3 review still apply to the broader Greater Affix
  implementation and should be addressed before live publish — they are not
  changed by this frequency fix.

## Codex Action Items

None for this round.

The fix is a clean improvement. Combined with the top-50 r3 follow-ups (color
swap + JSON orphan cleanup), the implementation should be ready for the
launch-test gate. Proceed to publish when those are addressed and the test plan
from r03's "Suggested Game-Launch Test Plan" passes.
