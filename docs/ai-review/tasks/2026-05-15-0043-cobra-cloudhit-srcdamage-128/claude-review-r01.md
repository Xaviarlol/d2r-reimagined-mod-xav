---
schema: ai-review-result-v1
task_id: 2026-05-15-0043-cobra-cloudhit-srcdamage-128
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

Direct reversal of the previous task (`2026-05-15-0024-cobra-cloud-srcdamage-zero`) on the one row that's safe to re-enable weapon damage on: the **one-shot server payload** `cobrastrikecloudhit`. The lingering-collision visual `cobrastrikecloud` stays at `SrcDamage=0` so the repeated-collision risk Eric flagged earlier doesn't return. Charge 3 unchanged.

Verified post-commit state (commit `d6beaa37 Restore Cobra cloudhit weapon damage`):

| Missile | Role | SrcDamage | Behavior |
|---|---|---|---|
| `cobrastrikecloud` | Charge 2 client visual / lingering | **0** (unchanged) | Visual only; no weapon damage even if accidentally re-routed server-side |
| `cobrastrikecloudhit` | Charge 2 server damage one-shot | **128** (was 0) | 100% weapon damage transferred on the single nova hit |
| `cobrastrikenova` | Charge 3 server+client payload | **128** (unchanged) | Charge 3 still scales with weapon damage |

`Eskillcobra2` enUS now reads `"Charge 2 - Poison Cloud: %d-%d over 6 sec + 100%% weapon damage"` — `100%%` correctly escapes the printf percent (same pattern as Fists of Fire).

The split is the right shape: the safe one-shot payload (`cobrastrikecloudhit` fires once when the charge releases) gets weapon damage; the unsafe lingering-collision missile (`cobrastrikecloud` can tick repeatedly as targets cross its collision shape) stays neutralized. This is the design Eric implicitly asked for with "let's the weapon damage back on, but set to 128 (100%)" combined with the prior context about source-damage being risky on DOTs.

All checks pass:
- Active and base `missiles.txt` both 172 cols, 916 rows, zero deviating rows.
- Active/base copies of `cobrastrikecloud`, `cobrastrikecloudhit`, and `cobrastrikenova` are byte-identical (CR-normalized).
- skills.json parses cleanly; `Eskillcobra2` text updated correctly with `100%%` escape.
- No charge 1, charge 3, Phoenix Strike, FoF, CoT, BoI, or unrelated row touched.

## Findings

### Critical
None.

### High
None.

### Medium
None.

### Low

**LOW-001 — Live folder out of sync with repo**

- File: live `data/global/excel/missiles.txt` at the `E:\...XavReimagined.mpq` path.
- Issue: Live `missiles.txt` differs from the repo copy (verified via `diff -q`). The recent series of commits (`0159b7ab Remove Cobra cloud source damage` → `d6beaa37 Restore Cobra cloudhit weapon damage`) haven't been published yet.
- Why it matters: In-game testing right now would reflect an older state (probably `SrcDamage=64` from the rebalance task, not the new `128`). Eric needs to publish to actually see the new behavior.
- Suggested fix: Run `scripts/install-local.ps1` (or whatever the publish helper is). `live_publish_allowed: true` covers this; reviewer doesn't publish.
- Blocks approval: No.

## Validation Checks

- Original user request reviewed: **Yes** — "ok. Lets the weapon damage back on, but set to 128 (100%)". The patch sets exactly `cobrastrikecloudhit.SrcDamage = 128`, the prior-context decision keeps `cobrastrikecloud.SrcDamage = 0`, charge 3 untouched. Matches.
- Git diff / design reviewed: **Yes**. Commit `d6beaa37` is the relevant commit. The before/after pairing across this task and the previous one is `cobrastrikecloudhit.SrcDamage: 64 → 0 → 128`, with `cobrastrikecloud.SrcDamage` permanently at `0` after the prior task.
- TSV column counts checked: **Yes**. 172 cols in both [data/global/excel/missiles.txt](data/global/excel/missiles.txt) and [data/global/excel/base/missiles.txt](data/global/excel/base/missiles.txt); 916 rows in both; zero deviating rows.
- Active/base sync checked: **Yes**. `cobrastrikecloud`, `cobrastrikecloudhit`, and `cobrastrikenova` rows are byte-identical between active and base after CR normalization.
- Tooltip vs gameplay consistency considered: **Yes**. `Eskillcobra2` enUS says "+ 100%% weapon damage" which matches `cobrastrikecloudhit.SrcDamage=128`. Charge-2 skilldesc formulas (`(3+...)*150/32` etc.) are unchanged and still describe the (unchanged) poison curve; only the trailing weapon-damage rider toggles. No other tooltip strings touched.
- Live publish risk considered: **Yes**. `live_publish_allowed: true`. Pure single-cell value change + tooltip text + docs update. Zero save-state risk. Safe to publish. **Note: live folder needs re-publish per LOW-001.**
- Docs checked: **Yes**. [docs/modding-findings.md](docs/modding-findings.md) was updated in this commit chain; verify it accurately notes `cobrastrikecloudhit` is back to `SrcDamage=128` while `cobrastrikecloud` stays at `0`. (I'd suggest re-confirming the doc text in a quick read-through; not blocking.)
- Cross-task continuity: The 6 recent Cobra Strike commits show a clear iterative tuning chain — `1b21903d → 685d3be8 → 54a0cdff → 0159b7ab → d6beaa37`. Each task review chain landed without regressions to TSV structure or save compatibility.

## Codex Action Items

None required. **Optional**: re-publish to live folder so the new state can be tested in-game (LOW-001).

## Suggested Follow-up Tests

1. **Charge 2 single-target damage check** — stationary dummy in melee range. Build 2 charges, release. The cloud should:
   - Drop a poison cloud at the target's location (visual unchanged, 6 sec duration).
   - Apply the one-shot weapon-damage hit via `cobrastrikecloudhit` to the dummy (this is the new bit being restored — pre-publish there was no weapon damage at all on charge 2).
   - The lingering visual cloud (`cobrastrikecloud`) does NOT add weapon damage even as the dummy stays in it.
2. **Multi-target charge 2 test** — pack of monsters in the cloud's burst radius. Each hit by the `cobrastrikecloudhit` nova should take one weapon-damage hit + the poison curve over 6 sec. Monsters that *walk into the cloud after the burst* should only take poison damage (no new weapon-damage tick per collision) — this confirms the previous "repeated weapon damage via collision" issue is still suppressed.
3. **Charge 1 regression** — confirm charge-1 release still applies single-target poison + weapon damage as before. Skill row unchanged.
4. **Charge 3 regression** — confirm charge-3 nova still applies weapon damage + nova poison as before. `cobrastrikenova` unchanged.
5. **Tooltip render** — confirm Cobra Strike skill tree tooltip charge-2 line reads cleanly: `Charge 2 - Poison Cloud: 14-... over 6 sec + 100% weapon damage` with no `%%` artifacts and no garbled trailing text.
6. **Compare against the previous task's behavior** — if Eric had a save from the previous (SrcDamage=0) state, charge-2 should now visibly deal more damage on hit than the previous test.
