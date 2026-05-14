---
schema: ai-review-result-v1
task_id: 2026-05-14-0030-cobra-equal-poison-test
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

Eric asked for a test build where Cobra Strike charge 1, charge 2, and charge 3 all deal the **same flat poison damage**, over the **same 2-second duration**, all using **100% weapon damage**.

Codex's patch:
- **Cobra Strike** row (skills.txt id 265): poison curve set to `EMin/EMax` `8/14` with per-level adders `4/5/6/10/14` / `6/7/10/13/19`, and `ELen` changed from `100` → `50` frames. `SrcDam 128` (100% weapon damage) preserved.
- **Cobra Strike Nova** helper row (skills.txt id 490): poison curve set to the same `8/14` curve. `ELen 50` preserved.
- **skilldesc.txt** cobra strike row: charge 1, 2, 3 tooltip formulas all use the new `8/14` curve with `*50/16` (2-second display).
- All four edits mirrored across `active` and `base` copies.

This matches the original request as stated: the three charges now share one poison curve, one 2-second duration, and the 100% weapon damage path is intact (Cobra Strike row keeps `SrcDam 128`; `cobrastrikenova` missile in [data/global/excel/missiles.txt:915](data/global/excel/missiles.txt:915) already has `SrcDamage 128`, `ELen 50`, and the matching `8/14` poison curve, so charge 3 routes through it correctly).

One semantic caveat is worth flagging before publish: the chosen `8/14` curve matches what the **prior tooltip** showed for charge 3, **not** what the prior helper-skill row had (which was `10/18`). Depending on whether the helper-skill curve or the missile curve was actually being applied to charge 3 damage in the old build, charge 3's effective damage may have decreased slightly — see MED-001.

## Findings

### Critical
None.

### High
None.

### Medium

**MED-001 — Possible (small) effective reduction to charge 3 poison damage**

- File: [data/global/excel/skills.txt](data/global/excel/skills.txt) (Cobra Strike Nova row, id 490) and the missile at [data/global/excel/missiles.txt:915](data/global/excel/missiles.txt:915).
- Issue: Before this patch, three different `pois` curves existed for charge 3:
  - Cobra Strike Nova **helper skill** row: `EMin 10 / EMax 18` with adders `5,6,8,12,18 / 7,9,12,16,24`.
  - `cobrastrikenova` **missile** row: `EMin 8 / EMax 14` with adders `4,5,6,10,14 / 6,7,10,13,19` (already at the new target).
  - skilldesc tooltip charge 3: `8/14` (matched the missile).
  
  The patch aligns the helper skill row to `8/14`, matching the missile and tooltip. **If the helper-skill row was being applied to in-game charge 3 damage**, this is a small effective nerf to charge 3 (from `10/18` → `8/14`). **If only the missile drove the damage** (which is the more common D2 behavior for skills that fire a missile), then charge 3's effective damage was already `8/14` and is unchanged.
- Why it matters: Eric's amendment says "make all of them 2 sec and **same damage**" — they presumably want equalization without unintentional nerfs to the previously-strongest charge. If Codex hasn't already verified which curve drives charge 3 damage in-game, this is worth a quick test before publishing for testing.
- Suggested fix: No data change needed; just confirm in-game that pre-patch charge 3 poison damage was already showing `8/14`-curve values (i.e., the missile was the source), or accept the small reduction as intentional. If charge 3 was actually firing at `10/18` and Eric prefers the higher numbers, raise the shared curve to `10/18` (and update both the Cobra Strike row, the Cobra Strike Nova helper, the missile, and the three tooltip formulas).
- Blocks approval: No.

### Low

**LOW-001 — Design.md wording slightly misleading**

- File: [docs/ai-review/tasks/2026-05-14-0030-cobra-equal-poison-test/design.md:16](docs/ai-review/tasks/2026-05-14-0030-cobra-equal-poison-test/design.md:16)
- Issue: Says `Cobra Strike: set poison flat rate curve to the current nova curve.` But the chosen `8/14` curve is the previous **tooltip / missile** curve, not the previous **Cobra Strike Nova helper-skill** curve (which was `10/18`).
- Why it matters: Minor — the result is fine, but the phrasing makes it harder to verify intent vs. data later. Future re-reviewers may assume Codex meant `10/18`.
- Suggested fix: Reword to e.g., "set poison flat rate curve to the existing `cobrastrikenova` missile / charge-3 tooltip curve (`EMin 8 / EMax 14`)."
- Blocks approval: No.

**LOW-002 — Pre-existing LF vs CRLF mismatch between active and base files**

- Files: [data/global/excel/skills.txt](data/global/excel/skills.txt) and [data/global/excel/base/skills.txt](data/global/excel/base/skills.txt); same for skilldesc pair.
- Issue: Active files use CRLF line endings; base files use LF. After stripping CRs, the content is byte-identical (active/base **content** is in sync), but `diff active base` shows the entire file as different, which is noise that masks real differences. `git` warns "LF will be replaced by CRLF" on every commit touching base/.
- Why it matters: Not Codex's bug for this task — pre-existing repo state (probably stems from `core.autocrlf` interacting with `.gitattributes` only filtering one path). It does, however, make active/base sync verification harder for any reviewer, and would hide a real desync if one were introduced.
- Suggested fix: Out of scope for this task. Recommend filing a separate housekeeping task to normalize line endings (or `.gitattributes` rules) so both copies stay byte-identical.
- Blocks approval: No.

**LOW-003 — Tiger Strike synergy formula uses `par8` in skill row but `*10` literal in the missile row**

- File: [data/global/excel/skills.txt](data/global/excel/skills.txt) Cobra Strike Nova row vs. [data/global/excel/missiles.txt:915](data/global/excel/missiles.txt:915) cobrastrikenova row.
- Issue: The new Cobra Strike Nova helper row's `EDmgSymPerCalc` is `skill('Tiger Strike'.blvl)*par8`, where `par8 = 10`. The matching cobrastrikenova missile row uses the literal `skill('Tiger Strike'.blvl)*10`. Numerically equivalent **today** because `par8 = 10`, but if someone ever tunes the Tiger Strike synergy by changing `par8` on the skill row, the missile won't follow.
- Why it matters: Pre-existing inconsistency, not introduced by this patch. Worth a one-line note in the modding docs (the `low-level-set-item-buffs.md`-style debrief).
- Suggested fix: Out of scope. If you want to fix it later, change the missile's formula to `skill('Tiger Strike'.blvl)*par8` and confirm `par8` is read from the same source in the missile context (this requires double-checking against the eezstreet docs for missiles.txt before applying).
- Blocks approval: No.

## Validation Checks

- Original user request reviewed: **Yes**. Verified both the initial request and the amendment ("make all of them 2 sec and same damage").
- Git diff / design reviewed: **Yes**. diff.patch applied cleanly against the working tree (`git diff HEAD ... | diff - diff.patch` → exit 0).
- TSV column counts checked: **Yes**.
  - `data/global/excel/skills.txt`: header 322 cols, 492 rows, 0 deviating rows.
  - `data/global/excel/base/skills.txt`: header 322 cols, 492 rows, 0 deviating rows.
  - `data/global/excel/skilldesc.txt`: header 120 cols, 295 rows, 0 deviating rows.
  - `data/global/excel/base/skilldesc.txt`: header 120 cols, 295 rows, 0 deviating rows.
- Active/base sync checked: **Yes** — content-identical after CR normalization; line-ending mismatch flagged in LOW-002.
- Tooltip vs gameplay consistency considered: **Yes**. New skilldesc charges 1/2/3 all expand to `(8+...*4...*5...*6...*10...*14)*50/16` for `EMin` and `(14+...*6...*7...*10...*13...*19)*50/16` for `EMax`. This matches the new Cobra Strike row `EMin/EMax` and `ELen 50`, and matches the unchanged `cobrastrikenova` missile. Pre-existing tooltip/helper mismatch on charge 3 is now resolved.
- Live publish risk considered: **Yes**. `live_publish_allowed: false` per request frontmatter; live folder not inspected. Safe to publish for testing once MED-001 is settled, since no skill IDs, missile IDs, columns, row counts, or save-affecting fields were changed — purely tuning values on existing rows.
- Docs checked: **Yes** — design.md reviewed. Minor wording note in LOW-001. No mod-side docs (e.g., a `docs/cobra-strike-charges.md`) were needed for a test-only adjustment; if this curve is kept for a release rather than just testing, recommend adding a short note to the changelog.

## Codex Action Items

None required for approval. **Optional** before publishing for in-game test:

1. Settle MED-001: confirm with a quick in-game test (or by reading the eezstreet `missiles.txt` and `skills.txt` docs at `https://eezstreet.github.io/d2rdoc/files/missiles.html` and `.../skills.html`) whether the Cobra Strike Nova **helper skill** row's `EMin/EMax` is applied in gameplay, or only the missile's. The patch is safe either way, but Eric should know whether charge 3 effective damage is unchanged or slightly reduced.
2. Optional: reword design.md per LOW-001.

## Suggested Follow-up Tests

1. **Equal damage check** — on a fresh test character, level Cobra Strike to base level 1, no Tiger Strike, no +skills. Hit a stationary target with each charge in turn (1, 2, 3) and confirm the floating poison numbers (and total damage over 2 sec) are equal within the expected min/max range (`8/14` per frame × `50` frames / `256` ≈ `1.56 – 2.73` per frame DPS at clvl 1, roughly).
2. **Duration check** — verify the poison status icon on the target lasts the same 2-second duration after all three charges (no longer 4 sec on charges 1/2).
3. **Tooltip check** — open the Cobra Strike skill tooltip in the skill tree and confirm the displayed charge-1, charge-2, charge-3 poison damage values match (use a low-level test character to make differences obvious).
4. **Weapon-damage check** — wear a melee weapon with a known min/max physical damage range. Hit a target with each charge and confirm the dealt physical hit equals 100% weapon damage (i.e., the same as a normal attack of comparable type). Repeat with a different weapon to confirm the missile (charge 3) inherits the swap.
5. **Tiger Strike synergy** — level Tiger Strike to lvl 5, verify all three Cobra Strike charges' poison damage scale by exactly `+50%` (par8 = 10 × 5 levels = 50%) on both gameplay and tooltip.
6. **Active/base verification** — load the game with the active files (the published path), and separately verify a one-off run that loads base files (if you have a test profile that does so) gives the same skill behavior. (This will also surface the LOW-002 line-ending difference if anything in the loader is whitespace-sensitive.)
7. **Save compat smoke test** — load an existing Assassin save with points in Cobra Strike, town/save/reload, confirm no skill-tree corruption.
