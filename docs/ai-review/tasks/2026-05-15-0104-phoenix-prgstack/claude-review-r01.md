---
schema: ai-review-result-v1
task_id: 2026-05-15-0104-phoenix-prgstack
round: 1
reviewer: claude
verdict: approved_with_notes
critical: 0
high: 0
medium: 1
low: 1
requires_codex_changes: false
---

# Claude Review

## Verdict
Approved with notes

## Summary

Single-cell toggle: set `prgstack = 1` on the `Royal Strike` row in both [data/global/excel/skills.txt](data/global/excel/skills.txt) and [data/global/excel/base/skills.txt](data/global/excel/base/skills.txt). Internal name `Royal Strike` is correct — that's Phoenix Strike's skills.txt row identifier (display name is "Phoenix Strike" via the `Skillname<id>` localization indirection).

Per the eezstreet skills.js docs, `prgstack` controls how progressive functions fire when charges release:

- `prgstack=0`: only `srvprgfunc<N>` (where N = current charge count) fires.
- `prgstack=1`: **all** `srvprgfunc1`/`srvprgfunc2`/`srvprgfunc3` fire, scaled by current charge count.

So with `prgstack=1`, a Royal Strike charge-3 release now fires `srvprgfunc1=40` (meteor) + `srvprgfunc2=143` (chain lightning) + `srvprgfunc3=41` (chaos ice). A 2-charge release fires both 1 and 2. A 1-charge release still just fires srvprgfunc1. This matches Eric's intent ("a 3-charge Phoenix Strike finisher should also release lower charge payloads").

This brings Royal Strike in line with the other stack-style charge-ups in this mod:

| Skill | `prgstack` | `srvdofunc` |
|---|---|---|
| Fists of Fire | 1 | 35 |
| Claws of Thunder | 1 | 35 |
| Blades of Ice | 1 | 35 |
| **Royal Strike (Phoenix Strike)** | **1** (was blank) | **34** |
| Cobra Strike | (blank) | 34 |

Everything checks out structurally — see MED-001 for the only real concern (mismatched `srvdofunc`).

## Findings

### Critical
None.

### High
None.

### Medium

**MED-001 — `prgstack=1` behavior is unverified on `srvdofunc=34` skills**

- File: [data/global/excel/skills.txt](data/global/excel/skills.txt) Royal Strike row.
- Issue: Codex's design.md explicitly flags this: "`Royal Strike` uses `srvdofunc=34`, while Fists of Fire / Claws of Thunder / Blades of Ice use `srvdofunc=35`." The eezstreet docs describe `prgstack` as a generic flag in the `srvprgfunc#` family, but I haven't found a citation confirming the flag is honored identically by both `AssDoProgressiveAttack` (id 34, Cobra/Royal) and the FoF/CoT/BoI charge-release function (id 35). If the behavior diverges, Royal Strike may release only one payload despite `prgstack=1`, or release multiple but at unexpected damage scaling. The skill row also has a different `srvprgfunc2=143` (FoF/CoT/BoI use lower-numbered functions for charge 2), so the per-function semantics may also matter.
- Why it matters: This is the experiment Eric asked for. The fix is the minimal correct change to test the hypothesis, but the in-game outcome is the actual answer. If `prgstack=1` doesn't fire all three charges, Eric will need either (a) a different mechanism to combine charge payloads, or (b) to switch Royal Strike's `srvdofunc` to 35 (which would be a larger refactor and might break the per-charge missile selection that's currently working).
- Suggested fix: No data fix needed. **In-game test required before declaring success.** Specifically, with Phoenix Strike base-1 leveled, build 3 charges and release; observe whether the meteor + chain lightning + chaos ice payloads all visibly fire (or just the chaos ice). If only chaos ice fires, the `srvdofunc=34 × prgstack=1` combination is not honored and Codex/Eric need a different approach.
- Blocks approval: No (this is an experimental test build; the data change is the right shape to probe the question).

### Low

**LOW-001 — Phoenix tooltip not updated, but charge releases may now behave very differently**

- File: [data/local/lng/strings/skills.json](data/local/lng/strings/skills.json) `Eskillphoenix1/2/3` and friends; also `Skillsd<id>` / `Skillld<id>` for Phoenix Strike.
- Issue: If `prgstack=1` *does* fire all three payloads on charge 3, players will see meteor + chain lightning + chaos ice simultaneously on charge 3, which is significantly more damage than the tooltip currently describes (probably still showing only "Charge 3 - Chaos Ice damage" or equivalent). The tooltip text won't match reality.
- Why it matters: Same class of tooltip-vs-gameplay drift we've already hit with Cobra Strike's "+ 50% / + 100% weapon damage" trailing text. Codex's `Non-Goals` explicitly excludes tooltip string changes in this pass, so this is informational only. Worth flagging for a follow-up task once Eric tests the gameplay and decides whether to keep `prgstack=1`.
- Suggested fix: Defer until in-game test confirms the behavior. If the stack-release works, update `Eskillphoenix1/2/3` (or whatever the Phoenix charge strings are) to describe the combined-release behavior, and consider escalating the Phoenix `Skillld<id>` long description.
- Blocks approval: No.

## Validation Checks

- Original user request reviewed: **Yes** — "change phoenix strike to use prgstack also." Single-cell change made on the correct internal row name (`Royal Strike`).
- Git diff / design reviewed: **Yes**. Working-tree state shows `prgstack=1` on Royal Strike in both active and base skills.txt. The change appears to be uncommitted right now (no new commit yet beyond `d6beaa37`), so this review is against working-tree state.
- TSV column counts checked: **Yes**.
  - [data/global/excel/skills.txt](data/global/excel/skills.txt): 322 cols, 492 rows.
  - [data/global/excel/base/skills.txt](data/global/excel/base/skills.txt): 322 cols, 492 rows.
- Active/base sync checked: **Yes**. Royal Strike rows are byte-identical between active and base (CR-normalized).
- Tooltip vs gameplay consistency considered: **Yes** — see LOW-001. Tooltips not touched, may drift if `prgstack=1` produces visible combined releases.
- Live publish risk considered: **Yes**. `live_publish_allowed: true`. Pure single-cell value change, no row indices shifted, zero save-format risk. Safe to publish for testing.
- Docs checked: **Yes**. design.md flags the `srvdofunc=34` vs `=35` mismatch (the MED-001 caveat) — good documentation hygiene.
- Scope discipline: **Yes**. Confirmed untouched:
  - `royalstrikemeteor`, `royalstrikechainlightning`, `royalstrikechaosice`, `royalstrikemeteorfire`, `royalstrikemeteorcenter` — all 5 missile rows unchanged (still `SrcDamage=128` on the 3 release payloads, blank on burning ground and meteor center).
  - Fists of Fire, Claws of Thunder, Blades of Ice, Cobra Strike skill rows — all untouched.
  - Phoenix tooltip strings — untouched (Non-Goal compliance ✓).

## Codex Action Items

None required to unblock. **Required for follow-up**:

1. **In-game verification (per MED-001):** with Phoenix Strike at base level 1, build 3 charges against a stationary target and release. Confirm:
   - Visual: all three release effects fire (meteor impact + chain lightning + chaos ice nova), OR only one fires.
   - Damage: total damage on hit reflects the combined payloads.
   - If only one fires, the `srvdofunc=34 × prgstack=1` pairing isn't honored as expected and you'll need a different approach.
2. **Follow-up tooltip pass (per LOW-001):** if the stacked release works, update `Eskillphoenix1/2/3` (or whatever the Phoenix charge strings are — easy to find by grepping skills.json for "phoenix" or by looking up the `Eskill...` references in skilldesc.txt's `royal strike` row) to mention the combined-release behavior.

## Suggested Follow-up Tests

1. **Three-charge release** — see MED-001 step. Most important test.
2. **Two-charge release** — build 2 charges, release. Expect meteor + chain lightning (charge 1 + charge 2), no chaos ice. If `prgstack=1` is honored, this should fire both. If charge 2 (chain lightning) fires alone, then `srvprgfunc1` isn't being added by `prgstack=1` in this configuration.
3. **One-charge release** — build 1 charge, release. Expect just meteor. This should behave identically with or without `prgstack` (only one srvprgfunc to fire), so it's a control test.
4. **Burning ground regression** — confirm `royalstrikemeteorfire` still spawns its post-meteor burn patch and ticks fire damage with no weapon-damage scaling (untouched by this patch).
5. **Damage scaling** — if all 3 payloads fire on a 3-charge release, confirm each payload still applies `SrcDamage=128` weapon-damage transfer (per the Phoenix Strike SrcDamage task from earlier today). Total weapon-damage hits per release on a single target could be 3× weapon damage in addition to the elemental damage.
6. **No regression on Cobra Strike** — confirm Cobra Strike still behaves as a single-payload-per-charge skill (its `prgstack` is still blank — untouched).
