---
schema: ai-review-result-v1
task_id: 2026-05-14-1648-cobra-builder-poison-fix
round: 1
reviewer: claude
verdict: approved_with_notes
critical: 0
high: 0
medium: 1
low: 3
requires_codex_changes: false
---

# Claude Review

## Verdict
Approved with notes

## Summary

This task is the third iteration in a chain of Cobra Strike charge-1 / charge-2 fixes. Eric's complete instruction set:

1. (Original bug) "Cobra Strike is applying poison to the first cobra hit, instead of the charge 1 finisher."
2. (After Codex's first fix) "Charge 2 of Cobra Strike works, but the animation of the poison cloud isn't showing."
3. (After Codex's second fix) "Now charge 1 is doing the same AoE as charge 2."
4. (Final direction) "Poison cloud now works, but revert charge 1 back to what it was before you started messing with it — it was a single target poison that simply applied poison damage to a single target finisher."

Codex's committed state (`685d3be8 Fix Cobra, Fists of Fire, and orb recipes`) lands these per the design.md:

- **Charge 1**: `srvprgfunc1` blanked, `srvmissilea` blank, `cltmissilea` blank → falls back to `srvdofunc=34` (`AssDoProgressiveAttack`) → single-target direct attack. The skill row keeps `EType=pois`, `EMin=8`, `EMax=14`, `ELen=50`, `SrcDam=128`. So the charge 1 release applies the skill row's poison curve directly to the target. ✓ Matches Eric's "single-target poison finisher" requirement.
- **Charge 2**: `srvprgfunc2=36` (`ApplyClawsOfThunderLvl2` — shoot missile array) + `srvmissileb=cobrastrikenova` (server payload). Client visual changed from `poisonpuff` to `cobrastrikecloud` so the cloud now shows. The server damage path goes through `cobrastrikenova`. ✓ Matches Eric's "cloud animation showing" requirement.
- **Charge 3**: `srvprgfunc3=36` + `srvmissilec=cobrastrikenova` unchanged (visual still nova).

The `cobrastrikehit` helper missile mentioned in the design.md "Earlier Test Fix" history was never committed — it existed only in WIP state, so no removal is needed at commit-time. `git log -S cobrastrikehit` confirms zero history references.

Active/base `skills.txt` are content-synced (`diff` after CR normalize returns 0). Active/base `missiles.txt` are also content-synced. Both files have correct header column counts (322 and 172 respectively) and zero deviating rows. The Cobra Strike row at commit `685d3be8` has 322 columns in both copies, content-identical.

The patch is structurally clean and matches what Eric requested *in the latest direction*. The one substantive open question is whether the original underlying complaint ("builder hit applies poison") is still possible in this state — see MED-001.

> Note: the current worktree's Cobra Strike row reflects an *additional* later commit (`54a0cdff Rebalance Cobra Strike charges`) which is the scope of a separate review task (`2026-05-14-2356-cobra-charge-balance`). The state I am reviewing for *this* task is the snapshot at `685d3be8` itself, not the current HEAD.

## Findings

### Critical
None.

### High
None.

### Medium

**MED-001 — The original "builder hit applies poison" condition may still be present**

- Files: [data/global/excel/skills.txt](data/global/excel/skills.txt) Cobra Strike row (id 265); skills.js docs for `srvdofunc 34 = AssDoProgressiveAttack` and `prgdam 4 = ModifyProgressiveElementalConvert`.
- Issue: The skill row still has `EType=pois`, `EMin=8`, `EMax=14`, `ELen=50`, `SrcDam=128`, plus `prgdam=4` ("Add the skill's elemental damage"). `srvdofunc=34` (`AssDoProgressiveAttack`) is what runs on every Cobra Strike swing — both the *builder* hits that accumulate charges and the *charge-1 release* hit that consumes a single charge. If `prgdam=4` applies the skill row's E* on every Cobra-skill swing (rather than only on the release-with-charges swing), then the builder hits will still apply poison to the target — which is Eric's original bug.
- Why it matters: The whole task started with that bug. The design.md describes the failure mode in its own "Problem" section: "Because `AssDoProgressiveAttack` performs a real melee attack while building charges, these direct skill damage fields can poison the charge-building hit itself." The fix routes charges 2/3 through `srvprgfunc#=36` so those don't depend on the skill-row E*, but charge 1 deliberately falls back to the skill-row E* exactly to keep the "single-target finisher" feel — which means whatever D2's engine does for charge 1 release also applies for the builder hit (same `srvdofunc`). Eric may have implicitly accepted this trade-off ("revert charge 1 back to what it was"), but it's worth confirming with a quick in-game test.
- Suggested fix (if Eric still wants the builder-hit fixed but charge 1 to remain single-target):
  - Test 1: build 1 cobra charge against a stationary dummy, observe whether the dummy is poisoned *before* the release swing. If poisoned at hit #1, the bug is back; if poisoned only at hit #2 (release), the underlying engine actually gates the E* on charge release, and this fix is complete.
  - If the bug recurs, options include moving the charge-1 payload to a single-target missile (different missile from `cobrastrikenova` so it doesn't AoE) and clearing the skill row E*. The earlier `cobrastrikehit` attempt did this but, per the design.md history, ended up behaving like charge 2 AoE — that suggests the WIP `cobrastrikehit` either had a Radius / hit-function it shouldn't have, or `srvprgfunc1=40` invoked AoE behavior. A correctly-tuned single-target helper missile with `Radius=0` (no AoE), `pSrvHitFunc` that just kills + damages on contact, and `SrcDamage=128` would be the path to test next.
- Blocks approval: No — Eric explicitly asked for this rollback, but worth raising as a follow-up confirmation.

### Low

**LOW-001 — Charges 2 and 3 are now mechanically identical (server payload)**

- File: [data/global/excel/skills.txt](data/global/excel/skills.txt) Cobra Strike row.
- Issue: At commit `685d3be8`, both `srvprgfunc2=36` and `srvprgfunc3=36`, both `srvmissileb=cobrastrikenova` and `srvmissilec=cobrastrikenova`, and both use the same `cobrastrikenova` server missile (same `EMin/EMax/ELen/SrcDamage/HitShift`). Server-side they deliver the same damage in the same shape. Only the client visual differs (`cobrastrikecloud` vs `cobrastrikenova`).
- Why it matters: If Eric expects charge 2 to feel mechanically different from charge 3 (different radius, different damage, different effect), this commit doesn't differentiate them — the only player-visible difference is the visual. The `prgcalc2 = par1+((lvl-1)/6)` field controls the *client visual* radius via `cltprgfunc2=9` but does not affect server damage. (The next commit `54a0cdff` — a separate task — appears to address this by introducing `cobrastrikecloudhit` as a distinct charge-2 server missile; that's reviewed in task `2026-05-14-2356-cobra-charge-balance`.)
- Suggested fix: None for this task — Eric's clarification was specifically about restoring charge 1 and getting the charge-2 cloud visible. Differentiation between charges 2 and 3 is out of scope here and is the subject of the follow-up rebalance task.
- Blocks approval: No.

**LOW-002 — design.md asserts a missiles.txt change that didn't land in the commit**

- File: [docs/ai-review/tasks/2026-05-14-1648-cobra-builder-poison-fix/design.md:65](docs/ai-review/tasks/2026-05-14-1648-cobra-builder-poison-fix/design.md:65) and [.../design.md:90](docs/ai-review/tasks/2026-05-14-1648-cobra-builder-poison-fix/design.md:90).
- Issue: The design.md says "The appended `cobrastrikehit` missile was removed from active and base `missiles.txt`." and "`cobrastrikehit` is no longer present or referenced." Both are true *in the working tree*, but `git show 685d3be8 -- data/global/excel/missiles.txt` returns empty — this commit didn't touch missiles.txt at all. The cobrastrikehit experiment never made it into a commit; it existed only as an uncommitted WIP. So there is no "removal" to verify against the diff — there's nothing to remove.
- Why it matters: Documentation hygiene only. If a future task needs to audit history to understand what was tried, it'll spend time looking for a commit that never existed.
- Suggested fix: Reword design.md to say "the `cobrastrikehit` experiment was not committed; the working tree was reverted before commit." Optional cleanup.
- Blocks approval: No.

**LOW-003 — `cobrastrikecloud` as client-only visual: verify no client hit-function side-effects**

- File: [data/global/excel/missiles.txt](data/global/excel/missiles.txt) `cobrastrikecloud` row.
- Issue: Setting `cltmissileb=cobrastrikecloud` while `srvmissileb=cobrastrikenova` is a known D2 pattern (client visual ≠ server damage source), but `cobrastrikecloud` is a full missile definition. If it has `pCltHitFunc` or `pCltDoFunc` values that trigger client-side effects (state overlays, sound, overlap detection), those still fire for the visual missile. In the previous Cobra Strike experiment (per the design.md and earlier modding-findings.md), `cobrastrikecloud` was flagged as a "lingering collision missile" that caused repeated-hit issues when used server-side. Used as client-side only, those server-side hit functions don't apply, but it's worth a quick sanity check that there's no client-side `CltSubMissile` chain that produces visible per-tick damage indicators on the player's screen (cosmetic, not real damage, but confusing).
- Suggested fix: Quick in-game smoke test of charge 2 against a single stationary dummy — confirm the cloud is visible, the dummy takes one set of poison damage, and there are no repeated visual hit indicators per tick.
- Blocks approval: No.

## Validation Checks

- Original user request reviewed: **Yes** — the full message chain in `request.md` (original bug + three follow-up clarifications) was considered, including the final "revert charge 1 back to what it was".
- Git diff / design reviewed: **Yes**. `diff.patch` reviewed against `git show 685d3be8` for skills.txt and base/skills.txt. The diff.patch and the committed change match (both show the same OLD → NEW line for the Cobra Strike row, with `srvprgfunc1`/`srvmissilea`/`cltmissilea` cleared, `cltmissileb=cobrastrikecloud`, and skill-row poison preserved).
- TSV column counts checked: **Yes**.
  - [data/global/excel/skills.txt](data/global/excel/skills.txt): 322 cols, 492 rows, 0 deviating rows at `685d3be8`.
  - [data/global/excel/base/skills.txt](data/global/excel/base/skills.txt): 322 cols, 492 rows, 0 deviating rows.
  - [data/global/excel/missiles.txt](data/global/excel/missiles.txt): 172 cols, 916 rows, 0 deviating rows.
  - [data/global/excel/base/missiles.txt](data/global/excel/base/missiles.txt): 172 cols, 916 rows, 0 deviating rows.
  - Cobra Strike row specifically: 322 cols in both active and base at `685d3be8`.
- Active/base sync checked: **Yes**. Content-identical after CR normalization on all four files.
- Tooltip vs gameplay consistency considered: **Yes**. `Skillsd266`/`Skillld266` long descriptions (in `data/local/lng/strings/skills.json`) still describe charge 1 as "adds weapon damage and poison" (correct for this fix). `Eskillcobra1/2/3` formulas still drive the `%d-%d` per-charge display and the literals say "over 2 sec" (correct). No new tooltip update was needed for this round.
- Live publish risk considered: **Yes**. `live_publish_allowed: true`. As a reviewer I do not publish. The fix is safe to publish; the only behavioral question is the MED-001 builder-hit poison check, which Eric can verify in-game post-publish.
- Docs checked: **Yes**. `docs/modding-findings.md` updated with the new Cobra Strike model and the percent-escape note for FoF tooltips. design.md and codex-response files reviewed; only LOW-002 wording note.

## Codex Action Items

None required to unblock. **Optional follow-ups**:

1. (Per MED-001) Eric should confirm in-game whether a Cobra Strike *builder* hit still applies poison to the target. If yes, this iteration only restored charge 1 *gameplay shape*, not the original bug fix. If no, the engine gates skill-row E* application on charge release and we're good.
2. (Per LOW-002) Reword design.md to remove the misleading "cobrastrikehit removed from missiles.txt" claim, since cobrastrikehit was never committed.
3. (Per LOW-003) Verify `cobrastrikecloud` as a client-only visual doesn't trigger any client-side hit side-effects.

## Suggested Follow-up Tests

1. **Builder-hit smoke test (MED-001):** new Assassin, level Cobra Strike to 1, no other skills. Find a stationary low-HP monster (e.g. Den of Evil fallens). Press Cobra Strike *once* against it — observe whether the green poison overlay appears immediately or only after a *second* swing (the charge 1 release).
2. **Charge 1 single-target test:** build 1 charge, release with a finisher (or by attacking another target while charges are active depending on the engine model). Confirm only the directly-hit target is poisoned, no AoE around it.
3. **Charge 2 cloud test:** build 2 charges, release. Confirm the green cloud visual appears (was missing before this fix) and that the dummy takes poison.
4. **Charge 2 single-cloud test:** confirm only one set of poison damage is applied per release — no repeated hits per cloud frame (rules out the cltmissileb=cobrastrikecloud client-side side-effect concern in LOW-003).
5. **Charge 3 unchanged test:** build 3 charges, release, confirm the nova still fires as before with no regression.
6. **Tooltip sanity check:** open Cobra Strike's skill tree tooltip, confirm all three charge lines display values and "over 2 sec" without rendering as garbled text.
7. **Active/base parity test:** if the mod can be loaded in base mode (Classic/Expansion) as well as active (Warlock), confirm behavior matches in both — the active and base `skills.txt` rows are byte-identical at `685d3be8`, so this should be redundant, but worth a smoke check.
