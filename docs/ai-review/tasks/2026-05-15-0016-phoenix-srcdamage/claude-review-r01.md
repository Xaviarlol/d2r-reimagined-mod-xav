---
schema: ai-review-result-v1
task_id: 2026-05-15-0016-phoenix-srcdamage
round: 1
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

Tightly scoped, single-purpose change. Eric's request — "please set them to srcdam 128 (except burning ground)" — referring to Phoenix Strike's three charge-release missiles (which internally use the `Royal Strike` skill row). Codex committed `607656ac Apply Phoenix Strike source damage` and the result matches the request exactly.

Current state in [data/global/excel/missiles.txt](data/global/excel/missiles.txt) (and identical in base):

| Missile | EType | SrcDamage | HitShift | Role | Change? |
|---|---|---|---|---|---|
| `royalstrikemeteor` | fire | **128** | 8 | Charge 1 release payload | ✓ set to 128 |
| `royalstrikechainlightning` | ltng | **128** | 8 | Charge 2 release payload | ✓ set to 128 |
| `royalstrikechaosice` | cold | **128** | 8 | Charge 3 release payload | ✓ set to 128 |
| `royalstrikemeteorfire` | fire | (blank) | 3 | Burning ground lingering field | ✓ correctly unchanged |
| `royalstrikemeteorcenter` | (blank) | (blank) | 8 | Meteor spawn/targeting carrier | ✓ correctly unchanged |

The exclusion of `royalstrikemeteorfire` is the right call: HitShift=3 + EType=fire + a long lingering ground field means each tick from a unit standing in the burn would re-apply 100% weapon damage, which is the same class of exploitable repeated-collision pattern the project already flagged in `docs/modding-findings.md` for cobrastrikecloud and the fistsoffirefirewall. Leaving SrcDamage blank keeps the burn at its existing weapon-independent fire ticks.

`royalstrikemeteorcenter` is the meteor's targeting/spawn-position marker, not a damage missile — correctly left alone.

No other Phoenix/Royal Strike fields touched (skill row, damage curves, HitShift, ELen, synergies, tooltip strings). No collateral changes to Fists of Fire, Claws of Thunder, Blades of Ice, or Cobra. The task scope and the diff scope match exactly.

Both files retain 172 header columns, 916 rows. Active/base copies of all 5 inspected rows are byte-identical. `docs/modding-findings.md` got a small note update; everything else is just the three single-cell `SrcDamage=128` edits.

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

- Original user request reviewed: **Yes** — "please set them to srcdam 128 (except burning ground)". The fix sets exactly three missile rows to `SrcDamage=128` and leaves the burning-ground row alone. Matches verbatim.
- Git diff / design reviewed: **Yes**. Commit `607656ac` touches `data/global/excel/missiles.txt` (6 lines), `data/global/excel/base/missiles.txt` (6 lines), and `docs/modding-findings.md` (3 lines), plus the new review-task folder. The 6 lines in each missiles.txt = the 3 changed rows × 2 (one `-` and one `+` line each). No other gameplay rows altered.
- TSV column counts checked: **Yes**.
  - [data/global/excel/missiles.txt](data/global/excel/missiles.txt): 172 cols, 916 rows. The 5 Royal Strike rows all 172 cols.
  - [data/global/excel/base/missiles.txt](data/global/excel/base/missiles.txt): 172 cols, 916 rows. Same.
- Active/base sync checked: **Yes**. All 5 inspected Royal Strike rows are byte-identical between active and base (after CR normalize).
- Tooltip vs gameplay consistency considered: **N/A**. Phoenix Strike's tooltips don't currently include a "+ X% weapon damage" rider, and Codex's non-goals explicitly excluded touching tooltip strings. Possible future tooltip work: now that the three charges actually transfer 100% weapon damage, the `Eskillphoenix1/2/3` strings could optionally be updated to mention it (same precedent as the Fists of Fire tooltip rider). Out of scope for this task.
- Live publish risk considered: **Yes**. `live_publish_allowed: false`, so the patch is for code review only — not authorized to publish to the live folder yet. Safe to commit; no save-format risk, no row-index shifts, no new missile IDs.
- Docs checked: **Yes**. [docs/modding-findings.md](docs/modding-findings.md) updated with a short Phoenix Strike note. Consistent with the new state.
- Scope discipline: **Yes**. Confirmed `Royal Strike` skill row in `skills.txt` is untouched (already had `SrcDam=128`). No Fists of Fire, Claws of Thunder, Blades of Ice, or Cobra Strike rows changed in this commit.

## Codex Action Items

None.

## Suggested Follow-up Tests

1. **Charge 1 (meteor) weapon-scaling test** — build 1 Phoenix Strike charge and release with a finisher. The target hit by the meteor's impact should now take fire damage roughly equal to weapon damage + the missile's base fire EMin/EMax (previously the meteor only delivered its raw EMin/EMax fire). Compare the hit's HP swing pre-patch vs. post-patch to confirm weapon damage now scales the meteor.
2. **Charge 2 (chain lightning) weapon-scaling test** — same idea with charge 2: the lightning chain should deal noticeably more damage per arc since each arc now carries 100% weapon damage on top of the base lightning curve.
3. **Charge 3 (chaos ice) weapon-scaling test** — same with charge 3, but verify against an enemy that's NOT cold-immune. Confirm the cold damage transfer is correctly added.
4. **Burning ground regression test** — stand a dummy on `royalstrikemeteorfire`'s burn patch. Confirm the per-tick fire damage is the *same* as before the patch (i.e. small, no weapon-damage explosion). This is the safety net for "don't apply SrcDamage to lingering ground fires."
5. **Tooltip render** — open Phoenix Strike's skill tooltip and confirm the three charge lines still render correctly. No change expected since strings weren't touched, but a sanity check is cheap.
6. **Synergy + weapon damage stacking** — equip a high-damage weapon and Tiger Strike-style synergies; verify the per-charge fire/lightning/cold damage scales with weapon damage as expected (linear with weapon's avg damage × 1.0).
