---
schema: ai-review-result-v1
task_id: 2026-05-14-2356-cobra-charge-balance
round: 1
reviewer: claude
verdict: approved_with_notes
critical: 0
high: 0
medium: 0
low: 3
requires_codex_changes: false
---

# Claude Review

## Verdict
Approved with notes

## Summary

Comprehensive Cobra Strike rebalance against Eric's three explicit asks:

1. **"Increase charge 1 damage by about 50%"** — ✓ Met. Skill row poison curves scaled by 1.5×:
   - `EMin`: `8 / 4 / 5 / 6 / 10 / 14` → `12 / 6 / 8 / 9 / 15 / 21` (each entry × 1.5)
   - `EMax`: `14 / 6 / 7 / 10 / 13 / 19` → `21 / 9 / 11 / 15 / 20 / 29` (each entry × 1.5, rounded up where fractional)
   - `ELen=50`, `SrcDam=128`, charge-1 hooks (`srvprgfunc1`/`srvmissilea`/`cltprgfunc1`/`cltmissilea`) still blank, so the charge-1 release continues to hit a single target via the skill row's direct poison. Skilldesc charge-1 formulas updated to match.
2. **"Reduce charge 2's poison cloud damage by 50%, but make the duration of the cloud 6 seconds"** — ✓ Met (close-to-50%). Charge 2 is now routed through a new dedicated `cobrastrikecloudhit` server missile so it can be tuned independently from charge 3:
   - `cobrastrikecloudhit`: copy of `cobrastrikenova` with `SrcDamage=64` (50% weapon damage transfer), `HitShift=3` (≈ 3.125% damage scale instead of 4 = 6.25%), `EMin=3 / 1 / 2 / 2 / 3 / 5`, `EMax=5 / 2 / 2 / 3 / 4 / 6`, `ELen=150` (6 sec at 25 fps), `Skill` column empty so the missile uses its own values.
   - `srvmissileb=cobrastrikecloudhit` on the Cobra Strike skill row.
   - Tooltip formula at level 1 drops from `8×50/16 = 25` to `3×150/32 ≈ 14.06` total displayed damage — a ~44% reduction (close to the asked 50%; small interpretation choice that prioritizes total payload over per-second damage).
   - Visual cloud (`cltmissileb=cobrastrikecloud`) has `Range` extended from `60` to `150` frames to match the 6-second window.
3. **"Charge 3 no change"** — ✓ Met. `srvmissilec=cobrastrikenova` and `cltmissilec=cobrastrikenova` unchanged; the existing `cobrastrikenova` missile row and Cobra Strike Nova helper skill row are byte-identical to the previous state; charge-3 tooltip formula unchanged.

All four TSV files (active + base for `skills.txt`, `skilldesc.txt`, `missiles.txt`) keep their header column counts (322, 120, 172). Active/base copies of the changed Cobra Strike rows and the `cobrastrikecloudhit` row are byte-identical after CR normalization. `data/hd/missiles/missiles.json` adds the `cobrastrikecloudhit: poison_nova` HD mapping so the new missile renders correctly. `data/local/lng/strings/skills.json` updates `Eskillcobra2` to `"Charge 2 - Poison Cloud: %d-%d over 6 sec + 50%% weapon damage"` — the `50%%` correctly escapes the percent to avoid the printf glitch we fixed for Fists of Fire in the previous task.

The math, the file structure, and the active/base sync are all clean. Three low-severity notes follow.

## Findings

### Critical
None.

### High
None.

### Medium
None.

### Low

**LOW-001 — Charge 2 "50% damage reduction" landed at ~44%, not exactly 50%**

- File: [data/global/excel/missiles.txt:cobrastrikecloudhit](data/global/excel/missiles.txt) and corresponding skilldesc charge-2 formula in [data/global/excel/skilldesc.txt](data/global/excel/skilldesc.txt).
- Issue: At skill level 1, the tooltip-displayed charge-2 poison drops from `8 × 50 / 16 = 25` to `3 × 150 / 32 ≈ 14.06`. That's ~56% of the old value, i.e. a 44% reduction. Eric asked for a 50% reduction. The picked `EMin=3` (rather than something like `EMin=3` and a `HitShift=3` combo producing exactly half) is the source of the slight skew.
- Why it matters: Cosmetic / tuning. Eric likely won't notice the 6 percentage-point difference in-game, and the per-second damage drops far more aggressively (from `12.5/sec` to `~2.3/sec` — ~81% lower DPS) since the duration tripled. If Eric is satisfied with the practical feel, this is fine; if Eric wants exactly half total payload, drop `EMin` to `~2.5` (round to `2` or `3` with an offset). Defensible either way.
- Suggested fix: Optional. If targeting an exact 50% reduction at lvl 1: set `EMin` rate to `~2.67` (impossible integer); a closer integer fit would be `EMin=2 / EMinLev1=1 / EMinLev2=1 / EMinLev3=2 / EMinLev4=2 / EMinLev5=4` to land at `12.5` total at lvl 1.
- Blocks approval: No.

**LOW-002 — `cobrastrikecloud` client visual still carries server-side damage fields**

- File: [data/global/excel/missiles.txt:cobrastrikecloud](data/global/excel/missiles.txt) and base copy.
- Issue: The Cobra Strike row now uses `cobrastrikecloud` only as the **client** visual (`cltmissileb=cobrastrikecloud`). But the missile row itself still has `SrcDamage=128`, `HitShift=4`, `EType=pois`, `EMin=1 / EMax=2` and its own poison curve in [data/global/excel/missiles.txt](data/global/excel/missiles.txt). Since the server doesn't spawn it as a damage missile here, those server-side fields don't apply during charge 2. But the values remain alongside the missile definition and could be a footgun if anyone later sets `srvmissileb=cobrastrikecloud` again — they'd reintroduce the original "lingering collision cloud applying ticked damage" issue that was the reason for moving to `cobrastrikecloudhit` in the first place.
- Why it matters: Defensive cleanup. Not a current bug; the design.md already calls this out ("`cobrastrikecloud` should not be reintroduced as the charge 2 server missile without retesting repeated collision damage; it is currently only the charge 2 client visual"), but the data still allows that reintroduction trivially.
- Suggested fix (optional cleanup): set `cobrastrikecloud.SrcDamage` to `-1` and clear `EMin/EMax/ELen`. The missile would then be visually identical but couldn't reintroduce damage even if accidentally re-referenced server-side. Not blocking — the docs note is the immediate safeguard.
- Blocks approval: No.

**LOW-003 — `Eskillcobra2` string is enUS-only; non-English players see the fallback**

- File: [data/local/lng/strings/skills.json](data/local/lng/strings/skills.json) `Eskillcobra2` entry.
- Issue: Pre-existing state — `Eskillcobra2` only has `enUS`; no `deDE`/`esES`/`frFR`/`itIT`/`koKR`/`plPL`/`esMX`/`jaJP`/`ptBR`/`ruRU`/`zhCN`/`zhTW` entries. Other Cobra strings (`Skillname266` / `Skillld266`) do have all 13 languages. Non-English clients will fall back to enUS for this line — which is mechanically correct since the patch already updated enUS. The same gap applies to `Eskillcobra1` and `Eskillcobra3`.
- Why it matters: Localization completeness only. Not introduced by this patch — flagged in last task's review too. Worth noting since the patch is editing this exact line.
- Suggested fix: When a translator pass happens, add localized copies of `Eskillcobra1/2/3` (including the new `over 6 sec + 50%% weapon damage` rider in their own escape syntax). Out of scope.
- Blocks approval: No.

## Validation Checks

- Original user request reviewed: **Yes** — all three asks (charge 1 +50%, charge 2 -50% over 6 sec, charge 3 unchanged) confirmed against the diff and current repo state.
- Git diff / design reviewed: **Yes**. diff.patch matches commit `54a0cdff Rebalance Cobra Strike charges`. design.md accurately describes the change.
- TSV column counts checked: **Yes**.
  - [data/global/excel/skills.txt](data/global/excel/skills.txt): 322 cols, 492 rows. Cobra Strike row: 322 cols.
  - [data/global/excel/base/skills.txt](data/global/excel/base/skills.txt): 322 cols, 492 rows. Cobra Strike row: 322 cols.
  - [data/global/excel/skilldesc.txt](data/global/excel/skilldesc.txt): 120 cols, 295 rows. cobra strike row: 120 cols.
  - [data/global/excel/base/skilldesc.txt](data/global/excel/base/skilldesc.txt): 120 cols, 295 rows. cobra strike row: 120 cols.
  - [data/global/excel/missiles.txt](data/global/excel/missiles.txt): 172 cols, 916 rows. New `cobrastrikecloudhit` row: 172 cols.
  - [data/global/excel/base/missiles.txt](data/global/excel/base/missiles.txt): 172 cols, 916 rows. New `cobrastrikecloudhit` row: 172 cols.
- Active/base sync checked: **Yes**. Cobra Strike skill row, cobra strike skilldesc row, `cobrastrikecloud` missile row, and `cobrastrikecloudhit` missile row are byte-identical between active and base copies (CR-normalized).
- Tooltip vs gameplay consistency considered: **Yes**:
  - Charge 1 tooltip formula `(12+...)*50/16` matches skill row `EMin=12 / ELen=50` at default HitShift.
  - Charge 2 tooltip formula `(3+...)*150/32` matches missile `EMin=3 / ELen=150 / HitShift=3`.
  - Charge 3 tooltip formula `(8+...)*50/16` matches the unchanged `cobrastrikenova` missile values.
  - `Eskillcobra2` enUS text says "over 6 sec + 50%% weapon damage" — matches `ELen=150` (6 sec) and `SrcDamage=64` (50% weapon damage).
- Live publish risk considered: **Yes**. `live_publish_allowed: false` per request frontmatter — task explicitly does not authorize publishing yet. Safe to commit; recommended to wait for Eric's go-ahead before pushing to the live folder. No save-affecting changes — only existing skill/missile row values were tuned, plus one new missile row appended (id 914, new internal ID, no displacement of existing IDs).
- Docs checked: **Yes**. [docs/modding-findings.md](docs/modding-findings.md) updated with charge-2 cobrastrikecloudhit notes and the cloud `Range=150` value. The Cobra Strike model section accurately describes the new state.
- HD-side checked: **Yes**. [data/hd/missiles/missiles.json](data/hd/missiles/missiles.json) adds `"cobrastrikecloudhit": "poison_nova"` so the new server missile maps to a known HD visual entry. The `cobrastrikenova` mapping is untouched.
- Missile damage inheritance: **Yes**. `cobrastrikecloudhit.Skill` (col 108) is empty, so the missile uses its own `EMin/EMax/ELen/SrcDamage/HitShift` — not inherited from any skill row. Consistent with how `cobrastrikenova` works.

## Codex Action Items

None required to unblock. **Optional follow-ups**:

1. (Per LOW-001) If Eric wants the charge-2 reduction to be closer to exactly 50% of the old total payload, drop `cobrastrikecloudhit.EMin` slightly (current 3 → 2 with an adjusted Lev1-5 curve). Tooltip will reflect the change automatically once skilldesc formulas are re-tuned.
2. (Per LOW-002) Optional cleanup: clear `cobrastrikecloud`'s server-side `SrcDamage/EMin/EMax/ELen` since it's only a client visual now. Removes the "footgun if accidentally re-referenced server-side" risk.
3. (Per LOW-003) Localization of `Eskillcobra1/2/3` into the 12 non-English locales when a translator pass happens.

## Suggested Follow-up Tests

1. **Charge 1 power test** — pre-rebalance saves with skill points spent in Cobra Strike: build 1 charge against a stationary dummy, release with a finisher. Confirm the poison damage applied is visibly higher than before (roughly 1.5× the pre-rebalance value, e.g. ~37 displayed instead of ~25 at lvl 1).
2. **Charge 2 duration test** — build 2 charges, release. Watch the green poison cloud visual stay on screen for ~6 seconds (was ~2.4 seconds before). Confirm the poison status icon on a target hit by the cloud also persists ~6 seconds.
3. **Charge 2 damage test** — log a target's HP across the full cloud duration. Total damage taken should be approximately half of the pre-rebalance per-charge-2 release total. Per-second damage should be much lower (since the duration tripled).
4. **Charge 3 regression test** — build 3 charges, release. Confirm the nova fires with the same radius, damage, and visual as before. No drift expected since `cobrastrikenova` is byte-identical to the pre-rebalance state.
5. **Charge 2 vs charge 3 differentiation** — explicitly compare the two: a single target in melee range should take noticeably *less* damage from charge 2 than from charge 3 now (charge 2 has lower base poison, lower weapon damage transfer, and the same target only sits in the cloud once). Multi-target: charge 2 cloud lingers longer at the target's spot; charge 3 nova hits the wider radius once.
6. **Tooltip render** — open Cobra Strike's skill tree tooltip and confirm all three charge lines display values cleanly, with charge 2 reading "Charge 2 - Poison Cloud: 14-..." or similar with "over 6 sec + 50% weapon damage" trailing without garbled text.
7. **Save compatibility** — load an existing Assassin save that had charge-2 expectations baked in. Skills should re-resolve at next equip / town reload with the new values. No skill ID changes, so no save corruption expected.
8. **`cobrastrikecloud` accidental reintroduction guard** — *not* a test, but a reminder: if anyone later wants to reroute charge 2's server damage through `cobrastrikecloud`, recheck the repeated-collision issue documented in [docs/modding-findings.md](docs/modding-findings.md).
