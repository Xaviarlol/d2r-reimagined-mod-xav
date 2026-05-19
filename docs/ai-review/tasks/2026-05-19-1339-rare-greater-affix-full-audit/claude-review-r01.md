---
schema: ai-review-result-v1
task_id: 2026-05-19-1339-rare-greater-affix-full-audit
round: 1
reviewer: claude
verdict: needs_fixes
critical: 0
high: 0
medium: 2
low: 3
requires_codex_changes: true
---

# Claude Review

## Verdict
Needs fixes

## Summary

`design_review` of the generated full rare-affix apex audit and the Greater Affix chance
model. I reviewed the audit (`rare-greater-affix-apex-audit-2026-05-19.md`), the chance
table, the probability-sanity TSV, and the generator script
(`scripts/audit_rare_affix_apexes.py`), and verified the generated numbers against the
artifacts.

**The framework is sound and the core math is correct.** The headline answer to Eric's
question — *"does this test prove the frequency math?"* — is **yes**:

- The frequency model is uniform `× 10` of every existing affix, with each Greater
  candidate's eligible weight set equal to the **pre-scale** apex weight. That makes Greater
  exactly `1 : 10` against the post-scale apex — the requested "10x rarer than apex."
- The probability-sanity TSV's `existing_only_relative_delta` column is **`0.0` for all 1795
  rows**. This is both mathematically guaranteed (uniform scaling cancels:
  `10f / 10T = f / T`) and numerically confirmed. So ordinary-affix proportions are preserved
  *exactly* when Greater rows are excluded.
- `with_greater_relative_delta` is the small uniform per-pool dilution (`-0.37%` to `-3.23%`),
  which is the unavoidable mass the new Greater rows take — exactly as Eric described.
- The coverage audit is mechanically generated from every `rare=1` group, so it cannot miss
  a group; the script's `itype`/`etype` + `itemtypes.txt` inheritance handling is correct.

It cannot be approved for implementation yet because of **two issues**:

- **MED-001** — `Greater Lamprey/Vampire` comes out **30x rarer**, not 10x, breaking the
  design's own stated invariant ("`10.0x rarer` for every candidate").
- **MED-002** — the chance table samples only **one item per candidate**, so the `10x`
  ratio is verified at one item type only; a candidate whose authored `itype` scope differs
  from its apex's scope (which is exactly what MED-001 is) can be silently wrong on
  non-sampled items.

Fix those, plus the Low items, and the model is ready to drive Phase 2 implementation.

## Review Questions

**Q1 — Does the coverage audit capture every rare-eligible affix group / apex family?**
Yes. `group_audit()` enumerates every `rare=1` row's group across `magicprefix.txt` and
`magicsuffix.txt`, so coverage is mechanically complete — every prefix group (44, 101–143,
200–227, 307) and suffix group (1–81, 200–307) is listed. No family can be missed.

**Q2 — Are any groups incorrectly deferred or marked optional?**
No. I checked every deferred/optional group: charged-skill (44), light/AR (112, 25), howl
(113), sockets (122), stack size (141), pierce (307), binary effects (ignore-ac 4, freeze 11,
noheal 20, knock 24), repair/indestruct (37, 39), proc skills (77/78/79), class-special (81),
and the utility "optional" groups (reduce-ac 5, res-pois-len 29, ease 30, cheap 63). All are
reasonable deferrals — binary effects, proc systems, sockets, and pure utility do not gain
from a Greater range. Nothing that should be a Phase 2 power chase is wrongly deferred.

**Q3 — Does the frequency model correctly make each Greater candidate 10x rarer than its
apex?**
Yes for every candidate **except one**. The mechanism is correct:
`synthetic_greater_rows()` sets each candidate's total Greater weight equal to the pre-scale
apex weight, and `proposed_freq()` scales all existing rows `× 10` — giving `apex_after :
greater = 10 : 1`. The chance table confirms `10.0x rarer` for ~60 candidates. The exception
is **`Greater Lamprey/Vampire`** at **`30.0x rarer`** (apex weight before `72`, Greater
weight `24`; `720 / 24 = 30`). See MED-001.

**Q4 — Does the probability sanity TSV prove proportions are preserved?**
Yes — this is the strongest part of the package. `existing_only_relative_delta` is `0.0` for
**all 1795 rows** (verified by direct scan of the TSV). Because every existing row and the
whole pool are scaled by the same factor 10, each affix's relative share is algebraically
unchanged; the TSV confirms there is not even floating-point noise. The
`with_greater_relative_delta` column correctly isolates the unavoidable absolute dilution
from adding Greater rows (uniform within each pool, `-G / (10T + G)`). Eric's proposed test
is valid and it passes — the math is proven.

**Q5 — Does the chance model correctly use `itype`/`etype`, inheritance, pools, group
blocking, and apex-vs-Greater comparison?**
Mostly yes. `type_closure()` correctly walks `itemtypes.txt` `Equiv1`/`Equiv2` inheritance;
`eligible()` correctly gates on `rare=1`, `level`/`maxlevel`, and `itype`/`etype` against the
closure. Pool building and the `× 10` scaling are correct. Two caveats: (a) the
apex-vs-Greater comparison is only sampled at one item per candidate — see MED-002; (b) the
"if 3 same-side slots" figure is exact for its *model* but the model is a simplification of
D2's real draw-with-rejection algorithm — see LOW-002.

**Q6 — Are the effective chances reasonable for a first draft?**
Yes, for a draft. The high-impact rows are sane starting points: `Greater Grandmaster's`
(`dmg% 451-500`) and `Greater Godly` (`ac% 250-300` + `red-dmg% 26-30`) carry over from the
prior apex-design review; max-resist `Greater Four Seasons` (`res-all-max 7-8`) is a modest
bump and is appropriately rare; speed rows (`swing3 50`, `cast3 25`) are breakpoint-sensitive
but fine to draft; leech rows are reasonable. `design.md` explicitly says payloads are a
tunable draft, which is the right posture. The one structural concern is that the per-slot
odds at level 90 are small (mostly `<1%`), and the audit's own question — should late Greater
frequency be `1` not `3` — is worth deciding before implementation.

**Q7 — Which Greater families need splitting by item scope or element?**
Several, and the audit aggregates them and flags it:
- **Missile groups** — `Greater missile prefixes` lumps 8 groups (220–227); `Greater missile
  suffixes` lumps 7 (200–206). These need splitting, and there is a prior question of
  whether quivers/missiles should receive Greater affixes at all.
- **Multi-element** — `Greater Ruby/Sapphire/Amber/Emerald` (resist groups 117–120),
  `Greater Scorching/Shocking/Pestilent` (138–140), `Greater jewelry elemental damage`
  (10/12/13/16), and `Greater Elemental Mastery` + `Greater Elemental Pierce` (both group
  209) must become one row per element.
- **`group 125`** — three candidates (`Greater Skilltab`, `Greater class skill`,
  `Greater Omniscient`) share group 125, and skilltab itself is per-class/per-tree; this
  needs careful scope rows (and should be reconciled with the separate charm `+2 skill tree`
  task `2026-05-19-0019`).
- **`Greater Titan`** (str/dex/vit/enr, group 31) and `Greater Lamprey/Vampire` (lifesteal +
  manasteal, groups 27/28) — the audit notes "scope split"; for Lamprey/Vampire that scope
  mismatch is also the cause of MED-001.

## Findings

### Critical
None.

### High
None.

### Medium

**MED-001 — `Greater Lamprey/Vampire` is 30x rarer than apex, not 10x**

- Where: chance table row `Greater Lamprey/Vampire` (suffix, groups 27/28, sample `ring`).
- Issue: the row shows `Greater vs apex after = 30.0x rarer` — apex weight before `72`,
  apex after `720`, Greater weight `24`; `720 / 24 = 30`. The design's stated invariant is
  "`10.0x rarer` for every candidate with a valid apex baseline." For 10x, the Greater weight
  on the sampled `ring` should be `72`, not `24`.
- Root cause: this is the only candidate that aggregates two groups (27 lifesteal + 28
  manasteal) **and** the candidate's hand-authored `itype` scope is narrower than the actual
  leech apex rows' scope. `apex_weight_before` counts every ring-eligible apex row (`72`),
  but only `24` of the synthesised Greater weight is ring-eligible — so `cand_weight` and the
  apex it is measured against are computed over different item-type scopes.
- Why it matters: this task's whole purpose is "redo the frequency math and prove it is
  right." A visible 30x outlier means the leech Greater would be 3x rarer than intended (or
  the scope is wrong), and it is a concrete instance of MED-002.
- Suggested fix: make the `Greater Lamprey/Vampire` candidate's `itype`/`etype` scope match
  the leech apex rows it upgrades (split into lifesteal and manasteal, and per item scope as
  needed), so `cand_weight == apex_weight_before` on every shared item type. Re-run and
  confirm `10.0x`.
- Blocks approval: Yes.

**MED-002 — Single-item sampling cannot verify the 10x ratio across item scopes**

- Where: `chance_rows()` — one `sample` item per candidate; `synthetic_greater_rows()` scope.
- Issue: the `10x` ratio and the per-slot odds are computed at exactly one item type per
  candidate. The ratio is `apex_weight_after / cand_weight`, and both terms are filtered by
  `eligible(row, sample)`. If a candidate's authored Greater `itype` scope does not exactly
  match its apex rows' `itype` coverage, the ratio is wrong on every item type the sample did
  not happen to land on. `Greater Lamprey/Vampire` was caught only because `ring` exposed it;
  a mismatch on a candidate sampled at a "safe" item type would pass silently at `10.0x`.
- Why it matters: the audit presents `10.0x rarer` as a proven invariant. It is currently
  proven only at one sample point per candidate.
- Suggested fix: for each candidate, assert that the Greater rows' eligible item-type set
  equals the apex rows' eligible item-type set (or compute and report the ratio across all
  eligible item types, not just one sample). Add that check to the generator so the audit
  fails loudly if any candidate is not exactly `10x` everywhere it should be.
- Blocks approval: Yes — without it, "every candidate is 10x" is unverified.

### Low

**LOW-001 — The `× 10` scaling must be applied to the whole affix file, including
`rare=0` rows, or magic-item proportions shift**

- Where: implementation guidance implied by the model; `proposed_freq()` scales any row, but
  the audit only reasons about `rare=1` rows.
- Issue: `magicprefix.txt` / `magicsuffix.txt` also contain `rare=0` magic-only rows. If
  implementation scales only the rare-eligible rows `× 10`, then on **magic** items the
  rare=1 rows become 10x heavier than the rare=0 rows and the magic-item affix distribution
  is distorted. The sanity proof only covers the rare pool.
- Suggested fix: state explicitly that every row in both files is scaled `× 10` (rare and
  non-rare alike). Uniform whole-file scaling preserves both the rare and the magic pools.
- Blocks approval: No.

**LOW-002 — The "if 3 same-side slots" figure is exact for a simplified model only**

- Where: `exact_groupblocked_chance()`.
- Issue: the function is exact for the model "3 draws, each picks a distinct group weighted
  by group weight, success if any within-group pick is the target." D2's actual rare-affix
  generation is weighted pick **with rejection** on group collision, and the affix count is
  itself random. The recursion is internally correct, but the column should not be labelled
  "exact" without qualification.
- Suggested fix: relabel as an approximate/upper-bound illustration (the design text already
  notes real odds are lower with fewer slots — extend that caveat to the model itself). This
  does not affect the core 10x or proportionality results, which are pure weight ratios.
- Blocks approval: No.

**LOW-003 — Multi-group / multi-element candidates must be split before implementation**

- Where: missile candidates (groups 220–227, 200–206), multi-element resist/damage/caster
  candidates, `group 125` skill candidates, `Greater Titan` — see Q7.
- Issue: the chance table aggregates these into single rows for readability; they cannot be
  implemented as single rows (one element per row, per-scope rows). The audit acknowledges
  this in its own review questions.
- Suggested fix: before the Phase 2 TXT pass, expand each aggregated candidate into its
  real per-element / per-scope row set and re-confirm `10x` for each. Also decide whether
  missile/quiver affixes should get a Greater layer at all.
- Blocks approval: No (acknowledged future work) — but it is a prerequisite for the
  implementation pass.

## Responses To The Audit's Own Review Questions

1. *Apex groups wrongly deferred?* No — see Q2.
2. *Groups needing scope split (125 skills, 209 caster, missiles)?* Yes — see Q7 / LOW-003.
3. *Should late Greater frequency be `1` not `3`?* For the highest-impact families
   (Grandmaster's, Godly, max-resist, +skills) a late frequency of `1` is the safer draft —
   the per-slot odds are already low and these should feel like true chase rows. Decide per
   family; the proportionality proof is unaffected by the choice.
4. *Do any Greater ranges exceed sane limits?* Nothing egregious in the draft. `openwounds`
   is correctly capped at `100`; `res-all-max 7-8` is the one to keep deliberately rare.
   Payloads are explicitly a tunable draft, so this is not blocking.

## Validation Checks

- **Original user request reviewed:** Yes. The model implements Eric's two instructions —
  Greater = 10x rarer than current apex, and a before/after proof that ordinary proportions
  are unchanged. The proof is valid (Q4). The one place the 10x target is not met is
  MED-001.
- **Design reviewed:** Yes — task `design.md`, the generated audit MD, the chance table, the
  sanity TSV, and `scripts/audit_rare_affix_apexes.py` (read in full for the math paths:
  `eligible`, `proposed_freq`, `synthetic_greater_rows`, `apex_rows_for`,
  `exact_groupblocked_chance`, `chance_rows`, `probability_sanity_rows`).
- **Data claims spot-checked:** `Greater Godly` apex weight `118` = Godly `110` + Wraithly1
  `4` + Invulnerable1 `4` (the three group-101 level-86 rows) — confirmed. `Greater
  Grandmaster's` apex `14` = Grandmaster's variants `10` + Wraithly1 `4` — confirmed. Sanity
  TSV `existing_only_relative_delta` = `0.0` across all 1795 rows — confirmed.
- **`phase: design_review`:** no game-data TXT changes; the generator only writes report
  docs. A `code_review` round must check `magicprefix.txt` / `magicsuffix.txt` column counts
  and active/base parity once Phase 2 is implemented.
- **Minor:** `chance_rows()` line `old_relative_check_delta = 0.0 if ... else 0.0` is a
  dead no-op; harmless, but the real proof lives in `probability_sanity_rows()` — consider
  removing the dead line to avoid implying a check that is not performed.
- **Live publish risk:** `live_publish_allowed: false`; report-only.

## Codex Action Items

1. **(MED-001 — required)** Fix `Greater Lamprey/Vampire` so it is `10x` rarer than its
   leech apex — align the candidate's `itype` scope with the apex rows, splitting
   lifesteal/manasteal and per-scope as needed.
2. **(MED-002 — required)** Add a generator assertion that each candidate's Greater rows
   cover exactly the same item-type set as its apex rows (or report the ratio across all
   eligible item types). The audit must fail loudly if any candidate is not `10x` everywhere.
3. **(LOW-001)** State that the `× 10` scaling applies to every row in both affix files,
   including `rare=0` rows, so the magic-item pool is preserved too.
4. **(LOW-002)** Relabel the group-blocked 3-slot column as approximate.
5. **(LOW-003)** Expand the aggregated multi-element / multi-scope / missile / group-125
   candidates into real per-row sets before the Phase 2 implementation pass, and decide
   whether missiles get a Greater layer at all.

Resubmit as round 2 for a quick re-review (the framework is sound; only the scope/10x
verification needs to land), then proceed to Phase 2 implementation and a `code_review`
round on the affix TXT diff.

## Suggested Follow-up Tests (Phase 2 code_review / in-game)

1. **10x check** — every Greater row's eligible weight is exactly `1/10` of its post-scale
   apex weight, on every item type both can roll on.
2. **Whole-file scale** — every `magicprefix.txt` / `magicsuffix.txt` row frequency was
   multiplied by 10 (rare and non-rare); column counts intact; active/base in sync.
3. **Proportion check** — re-run the sanity comparison post-implementation; ordinary-affix
   relative shares unchanged, Greater rows carry only the expected dilution.
4. **Group exclusivity** — a Greater roll excludes the normal family rows in the same group.
5. **In-game rarity** — Greater Affixes appear rare enough to feel like chase rows; the
   `** Greater Affix` marker line renders.
