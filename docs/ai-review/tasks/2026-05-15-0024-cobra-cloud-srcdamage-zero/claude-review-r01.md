---
schema: ai-review-result-v1
task_id: 2026-05-15-0024-cobra-cloud-srcdamage-zero
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

Targeted DOT-safety patch. Eric's note "sourcedam is risky on dot effects. Please set it to 0 for now" applies to Cobra Strike's charge-2 poison cloud path. The patch zeroes `SrcDamage` on both cloud-related missile rows, leaves the single-shot nova charge 3 alone, and updates the tooltip to drop the now-obsolete "+ 50% weapon damage" rider.

Verified working-tree state (uncommitted, ready for commit + publish):

| Missile | Role | SrcDamage | Other key fields |
|---|---|---|---|
| `cobrastrikecloud` | Charge 2 client visual | **0** (was 128) | HitShift=4, EMin=1, EMax=2, ELen=100 |
| `cobrastrikecloudhit` | Charge 2 server damage | **0** (was 64) | HitShift=3, EMin=3, EMax=5, ELen=150 |
| `cobrastrikenova` | Charge 3 server+client payload | **128** (unchanged) | HitShift=4, EMin=8, EMax=14, ELen=50 |

`Eskillcobra2` enUS updated from `"Charge 2 - Poison Cloud: %d-%d over 6 sec + 50%% weapon damage"` to `"Charge 2 - Poison Cloud: %d-%d over 6 sec"` — tooltip no longer advertises weapon damage that the gameplay no longer delivers.

The patch also tightens [docs/modding-findings.md](docs/modding-findings.md) with a "source damage is risky on DOT/cloud effects" note and updates the current-value table to reflect `SrcDamage=0` on cobrastrikecloudhit.

Scope discipline is good: nothing touched on Cobra charge 1, charge 3, Phoenix Strike, Fists of Fire, Claws of Thunder, or Blades of Ice.

The change also incidentally addresses my LOW-002 finding from the previous task (`cobra-charge-balance`): `cobrastrikecloud` previously had `SrcDamage=128` even though it was used only as a client visual — a footgun if anyone ever re-pointed `srvmissileb` at it. Now both that footgun and the active-server `cobrastrikecloudhit` are at `SrcDamage=0`, so re-routing wouldn't accidentally reintroduce repeated-tick weapon damage on the DOT cloud.

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

- Original user request reviewed: **Yes** — "sourcedam is risky on dot effects. Please set it to 0 for now." Both cloud rows (the active DOT damage source `cobrastrikecloudhit` and the visual-only `cobrastrikecloud`) are now at `SrcDamage=0`. Defensive zeroing of the visual is good practice.
- Git diff / design reviewed: **Yes**. Working tree has uncommitted changes to:
  - `data/global/excel/missiles.txt` — 2 rows updated.
  - `data/global/excel/base/missiles.txt` — same 2 rows updated.
  - `data/local/lng/strings/skills.json` — `Eskillcobra2` enUS string updated.
  - `docs/modding-findings.md` — 4 small text updates reflecting the new state.
  No row insertions/deletions; no column shifts.
- TSV column counts checked: **Yes**.
  - [data/global/excel/missiles.txt](data/global/excel/missiles.txt): 172 cols, 916 rows, 0 deviating rows.
  - [data/global/excel/base/missiles.txt](data/global/excel/base/missiles.txt): same.
- Active/base sync checked: **Yes**. `cobrastrikecloud`, `cobrastrikecloudhit`, and `cobrastrikenova` rows are byte-identical between active and base (CR-normalized diff returns 0 on all three).
- Tooltip vs gameplay consistency considered: **Yes**. Pre-patch had `Eskillcobra2` claiming "+ 50%% weapon damage" while the missile carried `SrcDamage=64` (50% transfer). Post-patch the missile carries `SrcDamage=0` and the tooltip is correctly reduced to just "Poison Cloud: %d-%d over 6 sec" with no weapon-damage claim. The charge-2 skilldesc damage formulas (`(3+...)*150/32`) are unchanged and still correct for the unchanged poison curve. Charge 1 (skill-row poison) and Charge 3 (`cobrastrikenova`) tooltips unaffected.
- Live publish risk considered: **Yes**. `live_publish_allowed: true`. No save-format risk, no row-index shifts. Pure tuning of two cell values plus a tooltip string. Safe to commit and publish.
- Docs checked: **Yes**. [docs/modding-findings.md](docs/modding-findings.md) updated:
  - Section "SrcDam / SrcDamage" reworded to note source-damage is risky on DOT/cloud paths.
  - "Cobra Strike Current Model" section reflects `SrcDamage=0` on cobrastrikecloudhit and reframes the "flat poison should stay moderate" advice around DOT scaling unclarity.
  - "Historical note from the removed Cobra charge 2 cloud experiment" updated to past-tense the SrcDamage=128 behavior.
  - "Current cobrastrikecloud row characteristics" table updated to `SrcDamage = 0`.

## Codex Action Items

None. Safe to commit and publish.

## Suggested Follow-up Tests

1. **Charge 2 cloud damage test** — stand a dummy in/around the charge-2 cloud after release. Total damage taken should be only the flat poison curve (`EMin=3..EMax=5` baseline scaled by `EDmgSymPerCalc` synergy over 6 sec). No extra weapon-damage tick per cloud collision.
2. **Charge 2 with high-damage weapon** — equip something hard-hitting and repeat. Confirm the cloud damage does NOT scale up with weapon damage anymore. Pre-patch a high-damage weapon would have accumulated repeated weapon-damage hits through the cloud's collision events.
3. **Charge 3 regression test** — build 3 charges, release, confirm the nova still deals weapon-damage + nova poison as before. `cobrastrikenova` still has `SrcDamage=128`, so charge 3 should still scale with weapon damage. This is the differentiation between charge 2 (DOT only, no weapon damage) and charge 3 (nova + weapon damage).
4. **Tooltip render** — open Cobra Strike skill tree tooltip, confirm charge-2 line reads `Charge 2 - Poison Cloud: 14-... over 6 sec` (or similar at higher levels) with no garbled trailing text and no "weapon damage" claim.
5. **Charge 1 unchanged check** — confirm charge-1 release still delivers single-target poison + weapon damage as before. Skill row `SrcDam=128` is untouched, so this path is intact.
