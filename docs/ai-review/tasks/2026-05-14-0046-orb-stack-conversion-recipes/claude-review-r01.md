---
schema: ai-review-result-v1
task_id: 2026-05-14-0046-orb-stack-conversion-recipes
round: 1
reviewer: claude
verdict: needs_fixes
critical: 0
high: 1
medium: 0
low: 3
requires_codex_changes: true
---

# Claude Review

## Verdict
Needs fixes

## Summary

Eric reported that the recipe `15 Orb of Infusion + Perfect Topaz` doesn't work. Codex correctly diagnosed the cause — the old recipe asked for `ooi,qty=15` + a gem, which is 16 cube slots vs. the cube's 12-slot capacity — and replaced it with 172 new recipes (86 each for Topaz→Conversion and Emerald→Assemblage) that take a single stackable `1oi` (Orb of Infusion Stack, `maxstack=100`) plus the gem and use `op=18 / param=70 / value=<N>` to match exact stack quantities from 15 through 100. For stacks larger than 15, the recipes return a `usetype,qty=<N-15>` leftover stack alongside the converted orb. Structurally the patch is clean (106 cols per row, active/base symmetric, qty math checks out, qty cap matches `1oi.maxstack=100`).

**However, in active mode (Reign of the Warlock — the mode the primary `data/global/excel/` files serve) there is no player path to obtain a `1oi` stack.** The only sources of Orbs of Infusion in active mode produce `ooi` (loose, `maxstack=0`):
- Salvage recipes (rows 231–242 of `cubemain.txt`) → output `ooi`.
- Active `treasureclassex.txt` "Infusion Orb" TC (row 8) → drops `ooi`.

No cube recipe converts `ooi → 1oi`, and `ooi` is unstackable. So in active mode the new recipes are **unreachable** — Eric is in the same stuck state he was in before the patch (he has `ooi` orbs from salvage; the new recipes refuse them). Only base-mode players (Classic/Expansion) currently have access to `1oi`, because base `treasureclassex.txt` row 12 has a second "Infusion Orb" TC that drops `1oi`.

The patch fixes the bug **only in base/Classic mode**. In the active/Warlock mode (the mode the mod is built around), it replaces a broken recipe with another unreachable one. Before merging, the missing `ooi → 1oi` path needs to be added — or Eric should confirm he's actually testing in base mode.

## Findings

### Critical
None.

### High

**HIGH-001 — New recipes are unreachable in active (Reign of the Warlock) mode: no `ooi → 1oi` conversion path**

- Files: [data/global/excel/cubemain.txt](data/global/excel/cubemain.txt), [data/global/excel/misc.txt](data/global/excel/misc.txt) row for `ooi` and `1oi`, [data/global/excel/treasureclassex.txt:8](data/global/excel/treasureclassex.txt:8) ("Infusion Orb" TC in active).
- Issue: All 172 new recipes require `1oi` (stackable Orb of Infusion Stack) as input 1. In active mode (`data/global/excel/`), the only source of Infusion Orbs is `ooi` (loose, `maxstack=0`), via salvage recipes and the "Infusion Orb" treasure class. There is no cube recipe converting `ooi → 1oi`, and `ooi` cannot auto-stack (`maxstack=0`). Grep across `data/` confirms zero references to `1oi` in active mode that produce it: only the new patch recipes and the misc.txt definition. The base files (`data/global/excel/base/treasureclassex.txt:12`) have a separate "Infusion Orb" TC that drops `1oi`, so base/Classic/Expansion players can use the new recipes, but active/Warlock players cannot.
- Why it matters: Eric's stated problem — "15 orb of infusion + p topaz doesnt seem to work" — is presumed to be a real complaint from someone playing the mod, most likely in the showcase Reign of the Warlock mode. The patch replaces the broken 16-slot recipe with a recipe that requires an input Eric has no way to obtain in that mode. Net effect for an active-mode player: **same stuck state, just for a different reason.**
- Suggested fix (pick one):
  1. **Add an `ooi → 1oi` cube recipe.** Simplest is a single recipe with `numinputs=1`, `input 1="ooi"`, `output="1oi,qty=1"`, no op gate. Then players cube each loose orb individually to build up a stack. Add a second variant taking multiple `ooi` if desired. The same recipe should be present in both active and base files.
  2. **Update the salvage recipes (cubemain rows 231–242) to output `1oi` instead of `ooi`,** so players never accumulate loose orbs in the first place. This also requires the existing `ooi` items in player saves to be handled (either dropped from drops/recipes too, or eventually phased out).
  3. **Update active `treasureclassex.txt` to drop `1oi`** like base does (and/or add an active counterpart to base row 12). This still leaves the `ooi` from salvage stranded — option 1 or 2 is needed alongside.
- Blocks approval: **Yes.** This is the difference between "fixes Eric's problem" and "moves the broken thing one step over."

### Medium
None.

### Low

**LOW-001 — design.md misstates that the new pattern is "already present in cubemain.txt"**

- File: [docs/ai-review/tasks/2026-05-14-0046-orb-stack-conversion-recipes/design.md:19-23](docs/ai-review/tasks/2026-05-14-0046-orb-stack-conversion-recipes/design.md:19)
- Issue: Design says "Use the existing stack pattern already present in `cubemain.txt`" referencing `op=18, param=70, value=<qty>` and `output="usetype,qty=<remaining>"`. Pre-patch, no rows in `cubemain.txt` use `param=70`, no rows use the `usetype,qty=N` output pattern, and no rows take `1oi` as input. The 51 existing `op=18` rows all use `param=361` (`item_corrupted`) and check whether an item is corrupted, not stack quantity. The new pattern is *valid* D2R modding (per the Phrozen Keep CubeMain guide: op 18 = "item stat(param) ! value", which in the "Fail Item if" framing means "recipe passes when stat = value") but it is **new** to this codebase, not reused.
- Why it matters: Cosmetic — it makes the design less verifiable against the existing data, and a future re-reviewer may waste time looking for the supposed precedent.
- Suggested fix: Reword to "Adopt the standard D2R cube pattern (op=18 / param=70 = `quantity` stat from itemstatcost / value=<stack-size>) — newly introduced to this mod for the orb conversion recipes."
- Blocks approval: No.

**LOW-002 — design.md claims `ooi` "can already be stacked into `1oi`"**

- File: [docs/ai-review/tasks/2026-05-14-0046-orb-stack-conversion-recipes/design.md:32](docs/ai-review/tasks/2026-05-14-0046-orb-stack-conversion-recipes/design.md:32)
- Issue: Says "loose Orbs of Infusion can already be stacked into `1oi`; the conversion recipe then consumes exactly 15 from that stack." There is no such existing mechanism — see HIGH-001. The salvage recipes output `ooi` (maxstack 0), active treasure class drops `ooi`, and there is no `ooi → 1oi` cube recipe.
- Why it matters: This is the assumption that makes the design *seem* complete. Once corrected, the design's own logic surfaces the HIGH-001 gap.
- Suggested fix: Remove this sentence or rewrite once HIGH-001's missing conversion is in place. Then describe the full workflow including the salvage → loose → stack → conversion chain.
- Blocks approval: No (the underlying gap is High; this is just the docs).

**LOW-003 — Hardcoded qty cap at 100 is correct today but tied to a magic number**

- File: [data/global/excel/cubemain.txt](data/global/excel/cubemain.txt) new rows.
- Issue: The patch generates rows for `qty=15..100`. The cap of 100 matches `1oi.maxstack=100` in [data/global/excel/misc.txt](data/global/excel/misc.txt). If `maxstack` is ever raised, the patch will silently leave players unable to consume the top of an oversized stack — they'd have to manually split it down before cubing.
- Why it matters: Low priority; only matters if anyone touches `1oi.maxstack`.
- Suggested fix: When changing `1oi.maxstack`, regenerate the recipes to match. Optionally leave a brief comment in `design.md` or `misc.txt` row tying the two numbers together. Out of scope for this task.
- Blocks approval: No.

## Validation Checks

- Original user request reviewed: **Yes**. Eric's request: "while waiting for review, can you check the recipe that does 15 orb of infusion + p topaz, it doesnt seem to work?" The patch correctly identifies WHY it doesn't work (cube slot overflow). The remaining question is whether the *fix* lets Eric's actual cube usage succeed — see HIGH-001.
- Git diff / design reviewed: **Yes**. 172 new rows + 2 removed rows. Working tree matches diff.patch (verified by inspection).
- TSV column counts checked: **Yes**.
  - Header: 106 columns in both [data/global/excel/cubemain.txt](data/global/excel/cubemain.txt) and [data/global/excel/base/cubemain.txt](data/global/excel/base/cubemain.txt).
  - Row count: 16,047 in both files (matched).
  - Every new row: 106 columns (verified by `awk -F'\t' '{print NF}'` over the diff's `+` lines → all `106`).
- Active/base sync checked: **Yes**. The two diff hunks are content-identical (`diff` of the two TSV diff outputs returned only the file-path header difference). Both files now byte-mirror each other for the new rows.
- Tooltip vs gameplay consistency considered: **N/A** for this change — cube recipes don't have tooltip formulas; recipe names are descriptive only and the descriptions accurately state input quantities and output items.
- Live publish risk considered: **Yes**. `live_publish_allowed: false` per request frontmatter; live folder not inspected. **Do not publish until HIGH-001 is resolved** — publishing would make the bug for active-mode players strictly different but still present.
- Docs checked: **Yes**. design.md reviewed; see LOW-001 / LOW-002 for wording corrections that surface the HIGH-001 gap.

## Codex Action Items

1. **(Required to unblock approval)** Provide a player-accessible path from `ooi` (loose) to `1oi` (stack) in active mode. Recommended: add a single cube recipe `1 ooi → 1 1oi` (`numinputs=1`, `input 1="ooi"`, `output="1oi,qty=1"`, no op gate), mirrored in active and base. Then players who have stacks of leftover `1oi` can keep cubing in another `ooi` to grow the stack by 1 each time. (Auto-stacking-style merging into an existing stack via cube can also be done via `usetype` output magic, but the simplest robust thing is `ooi → 1oi,qty=1` and let D2's own stack-merge logic handle in-inventory consolidation.)
2. Fix design.md per LOW-001 and LOW-002 once HIGH-001's resolution is implemented.
3. Confirm with Eric which game mode he's actually playing — if Reign of the Warlock (active), the above is essential; if Classic/Expansion (base), the existing base `1oi` drop already covers the input path and HIGH-001 doesn't block, only LOW-001/LOW-002 do.

## Suggested Follow-up Tests

1. **End-to-end test in active mode:** start a fresh character in Reign of the Warlock, farm or `/give` (if console-enabled) until you have 15 `ooi` from salvage. Try to convert them into an Orb of Conversion via the new workflow. Pre-fix this should fail (no `1oi` source); post-fix this should succeed.
2. **qty=15 exact-match:** with a `1oi,qty=15` stack + `gpy` in the cube, transmute → confirm output is exactly one `ooc`, the stack is fully consumed, no leftover.
3. **qty=16 leftover:** with `1oi,qty=16` + `gpy` → confirm output is `1oi,qty=1` AND `ooc`.
4. **qty=100 leftover:** with `1oi,qty=100` + `gpy` → confirm output is `1oi,qty=85` AND `ooc`.
5. **Emerald path:** repeat 2–4 with `gpg` instead of `gpy` → confirm `ooa` outputs.
6. **Boundary: qty=14:** with `1oi,qty=14` + `gpy` → confirm no recipe matches (transmute fails / does nothing).
7. **Boundary: stack > 100:** if 1oi can ever exceed maxstack=100 via mods or other means, confirm what happens (will silently fail since no qty=101+ row exists; document if intentional).
8. **Active/base sync:** load a character in each game mode and verify the recipe is available in both.
9. **Save compat:** confirm a character holding pre-patch `ooi` orbs loads cleanly post-patch — they should still be valid items (`ooi` definition in misc.txt is unchanged), just not directly usable in the conversion recipes without the LOW-002-related fix.
