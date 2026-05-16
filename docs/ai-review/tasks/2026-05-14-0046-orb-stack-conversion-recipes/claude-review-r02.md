---
schema: ai-review-result-v1
task_id: 2026-05-14-0046-orb-stack-conversion-recipes
round: 2
reviewer: claude
verdict: approved_with_notes
critical: 0
high: 0
medium: 0
low: 2
requires_codex_changes: false
---

# Claude Review

## Verdict
Approved with notes

## Summary

Round-2 patch (committed as `685d3be8 Fix Cobra, Fists of Fire, and orb recipes`) is clean and fixes the user's stated problem two ways: (1) the cube slot overflow that originally broke the 15-orb recipe is gone, and (2) the gem item codes now match the mod's player-facing Topaz/Emerald (`gmt`/`gme`) instead of the vanilla Perfect Topaz/Emerald (`gpy`/`gpg`) that aren't in this mod's gem progression.

Final state of the two relevant cube recipes in [data/global/excel/cubemain.txt](data/global/excel/cubemain.txt) and [data/global/excel/base/cubemain.txt](data/global/excel/base/cubemain.txt):

```
ORB CONVERSION  - 11 Orbs of Infusion + Topaz   → Orb of Conversion   (numinputs=12, input1="ooi,qty=11", input2=gmt, output=ooc)
ORB ASSEMBLAGE  - 11 Orbs of Infusion + Emerald → Orb of Assemblage   (numinputs=12, input1="ooi,qty=11", input2=gme, output=ooa)
```

Matches Eric's clarification ("11 + topaz" + "keep the 11 + emerald for orb os assemblage" + "wrong item code for the gems. gmt and gme").

All round-1 HIGH-001 / LOW-001 / LOW-002 findings are resolved:
- The unreachable-`1oi` problem is no longer relevant — the recipes consume loose `ooi` directly, which is what players already have from salvage and active-mode drops.
- The misleading design.md wording is rewritten.

The round-1 LOW-003 ("hardcoded qty cap at 100 tied to `1oi.maxstack`") is moot because the patch no longer references `1oi` at all.

Side effect worth flagging (not blocking): the commit also **removed all `ORB STACK - Stacked Infusion Orb...`** recipes (the loose-to-stack family for `1oi`). The `1oi` item still exists in [data/global/excel/misc.txt](data/global/excel/misc.txt) row 248 (`Orb of Infusion Stack, maxstack=100`) and still drops via base mode's "Infusion Orb" TC at [data/global/excel/base/treasureclassex.txt:12](data/global/excel/base/treasureclassex.txt:12) — see LOW-001. The active mode's "Infusion Orb" TC drops loose `ooi`, so active-mode players are fully covered by the new recipes.

Live folder cubemain.txt mtime (2026-05-14 03:18:34, 3,659,558 bytes) is older and larger than the repo copy (2026-05-14 23:15:58, 3,614,297 bytes) — the live state reflects round-1's qty=15..100 recipe set rather than the committed round-2 state. Eric needs to re-publish before in-game testing (see LOW-002). `live_publish_allowed: true` per the request frontmatter, so re-publishing is authorized.

## Findings

### Critical
None.

### High
None.

### Medium
None.

### Low

**LOW-001 — `1oi` (Orb of Infusion Stack) is now an orphan item in cube usage**

- Files: [data/global/excel/misc.txt:248](data/global/excel/misc.txt) (item still defined, `maxstack=100`), [data/global/excel/base/treasureclassex.txt:12](data/global/excel/base/treasureclassex.txt:12) (still drops `1oi`).
- Issue: With the `ORB STACK - Stacked Infusion Orb qty=N + Infusion Orb` family removed, no cube recipe consumes `1oi` and no recipe produces it. The item still exists in misc.txt and still drops via base mode's "Infusion Orb" TC, so base/Classic/Expansion players will occasionally pick up an `Orb of Infusion Stack` they cannot use anywhere (no salvage path, no conversion path, no upgrade). Active/Warlock mode players never see `1oi` at all because active mode's "Infusion Orb" TC drops `ooi`.
- Why it matters: Cosmetic dead-loot rather than functional bug. Doesn't break the recipes Eric asked about. Worth a cleanup pass later.
- Suggested fix (any one):
  - Remove `1oi` from base mode's "Infusion Orb" TC and let base mode drop `ooi` like active does (one-line change in [data/global/excel/base/treasureclassex.txt](data/global/excel/base/treasureclassex.txt) — swap `1oi` for `ooi`).
  - OR keep `1oi` and add a single `1oi → ooi,qty=100`-style "unstack" recipe so a 1oi stack converts back to loose orbs (which then feed the 11-orb recipe).
  - OR set `1oi.disabled` to suppress drops entirely. (Not sure if that's a real misc.txt column — verify before applying.)
- Blocks approval: No.

**LOW-002 — Live folder out of sync with repo**

- Files: live `cubemain.txt` at `E:\Diablo II Resurrected\mods\XavReimagined\XavReimagined.mpq\data\global\excel\cubemain.txt`.
- Issue: Live file mtime `2026-05-14 03:18:34`, size 3,659,558 bytes (matches the round-1 qty=15..100 state, not the round-2 committed state at 3,614,297 bytes / `2026-05-14 23:15:58`).
- Why it matters: If Eric tests in-game now, they'll be testing the round-1 state (which has the recipes-needing-`1oi` problem), not the round-2 fix.
- Suggested fix: Re-publish the repo's `data/global/excel/cubemain.txt` and `data/global/excel/base/cubemain.txt` to the live folder before testing. `live_publish_allowed: true` makes this authorized for Codex/Eric (I do not publish myself — reviewer role).
- Blocks approval: No.

## Validation Checks

- Original user request reviewed: **Yes**. Three messages total:
  1. "the recipe that does 15 orb of infusion + p topaz, it doesnt seem to work" — fixed (cube slot overflow + gem code mismatch).
  2. "what is the max cube recipe input size? Just set it to that amount of ooi" — fixed at 11 ooi + 1 gem = 12 slots.
  3. "the issue with the cube recipes is you have the wrong item code for the gems. gmt and gme" — fixed (`gmt`/`gme` instead of `gpy`/`gpg`).
- Git diff / design reviewed: **Yes**. Commit `685d3be8`: 2 ORB rows added, 202 ORB rows removed (172 round-1 qty=15..100 series + 30 ORB STACK Infusion Orb stack/unstack rows). codex-response-r01.md and codex-response-r02.md both consulted.
- TSV column counts checked: **Yes**.
  - Active [data/global/excel/cubemain.txt](data/global/excel/cubemain.txt): header 106 cols, 15,677 rows, 0 deviating rows.
  - Base [data/global/excel/base/cubemain.txt](data/global/excel/base/cubemain.txt): header 106 cols, 15,677 rows, 0 deviating rows.
  - The 2 new ORB CONVERSION/ASSEMBLAGE rows in each file: 106 cols each.
- Active/base sync checked: **Yes**. Content-identical after CRLF normalization (`diff <(tr -d '\r' < active) <(tr -d '\r' < base)` returns no differences).
- Tooltip vs gameplay consistency considered: **N/A** for cube recipes (no skilldesc/skills.json paths involved).
- Live publish risk considered: **Yes**. `live_publish_allowed: true`, but the live folder hasn't actually been published yet for the round-2 state — flagged in LOW-002. No new save-compat or column-shape risks: row count changed but no row IDs/positions matter for cube lookups (recipes are matched by input pattern, not row index).
- Docs checked: **Yes**. design.md and both codex-response files reviewed; they accurately describe the committed state. `docs/modding-findings.md` was also touched in the commit but isn't in scope for this task.
- Item codes verified against [data/global/excel/misc.txt](data/global/excel/misc.txt):
  - `ooi` = "Orb of Infusion" (maxstack 0, loose) ✓
  - `gmt` = "Topaz" (the mod's gem) ✓
  - `gme` = "Emerald" (the mod's gem) ✓
  - `ooc` = "Orb of Conversion" ✓
  - `ooa` = "Orb of Assemblage" ✓
- Cross-recipe check: searched the file for any other recipe that uses `ooi` as input — found one pre-existing `CRAFT ITEM - 5x Infusion Orb & Mephisto's Animus & Baal's...` recipe at row 506 that is independent of this task and uses 5 loose `ooi` + 2 named items = 7 slots (well under cube capacity). Untouched by this patch and still valid.

## Codex Action Items

1. **Required for the user to actually test:** publish the updated `cubemain.txt` (active + base) to the live folder. `live_publish_allowed: true` covers this.
2. **Optional cleanup (LOW-001):** decide whether to keep `1oi` as a drop-only orphan, swap base mode's "Infusion Orb" TC to drop `ooi` like active mode does, or add a tiny unstack recipe. Worth a follow-up task but out of scope for this fix.

## Suggested Follow-up Tests

1. **Republish then in-game smoke test:** copy repo `cubemain.txt` (and base) to the live `.mpq` folder, launch with `-mod XavReimagined -txt`, then:
   - Salvage 11+ items to get loose `ooi` orbs in inventory.
   - Put 11 `ooi` + 1 `gmt` (Topaz) into the cube → transmute → expect `ooc` (Orb of Conversion).
   - Put 11 `ooi` + 1 `gme` (Emerald) into the cube → transmute → expect `ooa` (Orb of Assemblage).
2. **Negative test (10 orbs):** put 10 `ooi` + 1 `gmt` into the cube → transmute → no match, items returned.
3. **Negative test (wrong gem):** put 11 `ooi` + 1 `gpy` (Perfect Topaz, if you have one from old saves) → no match.
4. **Negative test (legacy recipe gone):** put 15 loose `ooi` + 1 gem (any) — won't fit anyway because 16 > 12 slots, but mentally confirm the old recipe row is gone (it is in the diff).
5. **Cross-mode test (base only):** start a character in Classic/Expansion mode and verify the new recipes work there too. If a `1oi` drops (the LOW-001 orphan), confirm it can be sold/dropped without crashing the game.
6. **Save compatibility:** load an existing character that has loose `ooi` in inventory pre-patch — the items should still be valid (`ooi` definition in `misc.txt` is unchanged), and the new recipe should consume them normally.
