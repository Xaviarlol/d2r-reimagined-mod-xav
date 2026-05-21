---
schema: ai-review-result-v1
task_id: 2026-05-21-0144-top50-greater-affix-redesign
round: 2
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

Round 2 of `design_review`. **All seven findings from r01 are concretely addressed in the
new "Round 2 Clarifications After Claude Review" section of `design.md`.** Codex's
response correctly identifies that my r01 explanatory aura-ID guesses were wrong and
replaces them with verified values; I re-verified those against `data/global/excel/skills.txt`
and they are correct (table below). The design is implementation-ready.

What I re-verified for this round:

- **Aura skill IDs against `skills.txt` (col 2 = `*Id`):**

  | Codex r2 claim | skills.txt entry | Match |
  |---|---|---|
  | Might = 98 | ID 98 = `Might`, charclass `pal` | ✓ |
  | Fanaticism = 122 | ID 122 = `Fanaticism`, `pal` | ✓ |
  | Conviction = 123 | ID 123 = `Conviction`, `pal` | ✓ |
  | Holy Freeze = 114 | ID 114 = `Holy Freeze`, `pal` | ✓ |
  | Meditation = 120 | ID 120 = `Meditation`, `pal` | ✓ |
  | Vigor = 115 | ID 115 = `Vigor`, `pal` | ✓ |

  6/6 correct. My r01 guesses (Might=113, Fanaticism=126) were wrong: 113 is
  Concentration and 126 is Bash (a Barbarian skill). Codex's verified-from-data
  approach caught this. Memory note relevance: this is the "don't assert engine
  behavior from documentation/memory without testing" lesson holding in real time —
  good catch by Codex.

- **Side observation: current Greater Aureole row is silently broken.** The existing
  Greater Aureole at `magicprefix.txt` lines 1718-1720 uses `mod1param=126`, which
  resolves to Bash (a Barbarian skill), not a Paladin aura. Whether the `aura` stat
  silently drops non-aura skill IDs or grants Bash-when-equipped is unclear, but the
  current state is wrong. The Round 2 redesign re-grounds all six aura params to
  valid Paladin aura IDs from `skills.txt` — fixing this latent bug as a side effect.
  Worth noting in the implementation commit message.

- **Per-tier emission policy (r01 HIGH-001) is now explicit.** New "Family Versus
  Emitted Row Policy" section states: "one 3-band Greater row set for every selected
  source variant" grouped by `(side, source affix name, payload fingerprint, item
  scope, class scope, level requirement tier)`. Concrete examples cover Arch-Angel's
  (multi-scope), Sage's (group 125 only), Traveling/Speed (both kept under one
  marker), Aureole (6 × 3 = 18 rows). This is the policy I recommended.

- **Frequency recalculation reframed (r01 MEDIUM-002).** New "Frequency Recalculation
  Meaning" section explicitly notes: "If this reproduces the current Greater frequency
  for a surviving family, that is expected." That's the right expectation-set.

- **Skilltab curation rationale documented (r01 MEDIUM-001).** New "Skilltab Curation
  Rationale" section: keep two specific skilltab Greaters (Cunning for trapper,
  Rose Branded for paladin combat) because class-wide skill Greaters already cover
  every class, and adding more skilltab Greaters would dilute the chase quality.
  Defensible.

- **Properties/itemstatcost cleanup procedure (r01 MEDIUM-003, LOW-001).** New
  "Property And ItemStatCost Cleanup" section adds the 7-step reference-scan-before-
  delete procedure, including `*ID` compaction to sequential `0..N` and the post-state
  max-ID assertion (target ≤487, ceiling 510). That's what I asked for.

- **Hybrid wrappers scoped (r01 Q6).** New "Hybrid Wrapper Families" section
  explicitly names Greater Wraithly Weapon and Greater Wraithly Armor as the only
  known hybrid-wrapper cases, with a fallback rule for implementation discovery
  ("if any other selected source variant needs three gameplay mods, use the same
  hybrid-wrapper approach rather than dropping a gameplay stat").

- **Validation strengthened (r01 LOW-003).** New "Additional Validation" section adds
  per-band level/maxlevel assertions (`early=50/65`, `mid=66/80`, `late=81/blank`),
  the Sage's group-125-only check, active/base byte-identical, and the launch-test
  gate before live publish.

## Review Questions

**Q1-Q8 from r01:** All answered satisfactorily by the r2 clarifications. No
remaining ambiguity.

**On the original r2 review questions (carried from r1 request.md):** All previously
flagged in r01 and now addressed.

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

- **Original user request reviewed:** Yes — *"create a plan to do them for review by
  claude. You will need to reweight all frequencies now that you are removing the
  other GA's..."*. The design correctly rebuilds from current rows (preserves Phase 1)
  rather than reverting to original files, and the freq reweight is reframed
  accurately as a consistency check that reproduces current values for surviving
  families. Eric's original ask is satisfied.
- **r01 findings re-checked:** All 7 addressed concretely in the new clarifications
  section. No remaining issues.
- **Independent data re-verification (r2 specific):** Aura skill IDs against
  `skills.txt` (6/6 correct), current Greater Aureole param=126 → Bash bug confirmed,
  current Aureole source rows contain all 6 chosen auras (98 Might, 114 Holy Freeze,
  115 Vigor, 120 Meditation, 122 Fanaticism, 123 Conviction at lines 602/610/611/
  613/614/615 respectively).
- **Diff scope:** No game-data TXT changes in this round (still design-only). The
  implementation will touch 8 listed files plus `item-modifiers.json` for the new
  marker strings.
- **Live publish risk:** `live_publish_allowed: false`. Design-only review. The
  design now explicitly gates live publish on a successful launch-test, which is
  the right discipline given the prior `44b2c3b0` crash.

## Codex Action Items

None for this round.

Proceed to implementation. The redesign is well-scoped: ~120-150 total Greater rows
across ~50 logical families, 50 new family marker stats, 6 verified paladin aura
IDs, atomic cleanup of the prior `greater_*` experiment, and a clear launch-test
gate before live publish.

Submit the implementation diff as a `code_review` round on this task (round 3 of
max 3) when ready.

## Suggested Follow-up Tests (for the `code_review` round)

Same as r01's list — those tests remain the right shape for the implementation diff:

1. Greater row count matches Round 2's per-source-variant policy (not necessarily 150).
2. No dangling property/stat references.
3. `itemstatcost.txt` `*ID` is sequential 0..N, max ≤487 target / ≤510 ceiling.
4. Active/base byte-identical for all four file pairs.
5. TSV row width matches header for every row.
6. `spawnable=1 rare=1` on every Greater row.
7. Level bands: early `level=50 maxlevel=65`, mid `level=66 maxlevel=80`, late
   `level=81 maxlevel=blank`.
8. Frequency spot-check: `late_freq = max(1, round(source_apex_freq/10))` on 5
   surviving families.
9. Marker presence: every Greater row carries exactly one per-family marker (either
   pure marker property or hybrid wrapper).
10. Aura param values are 98/114/115/120/122/123 — not the broken 126 from current
    state.
11. Game-launch test before publish: deploy to live, launch D2R, drop rares, confirm
    no crash and tooltip rendering.
