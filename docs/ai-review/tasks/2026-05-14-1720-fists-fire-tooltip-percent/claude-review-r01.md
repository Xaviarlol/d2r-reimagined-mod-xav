---
schema: ai-review-result-v1
task_id: 2026-05-14-1720-fists-fire-tooltip-percent
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

Tight, single-purpose fix. Two strings in `data/local/lng/strings/skills.json` had raw `%` characters in literal text (`100% weapon damage as fire`), which D2R's printf-style tooltip renderer was interpreting as a format specifier and rendering as garbage numeric text. Escaping them to `100%%` is the canonical fix and now displays correctly.

Verified against the current repo (commit `685d3be8`):

- [data/local/lng/strings/skills.json](data/local/lng/strings/skills.json) `Eskillfistsoffire1` enUS = `"Charge 1 - Fire Damage: %d-%d + 100%% weapon damage as fire"` ✓
- [data/local/lng/strings/skills.json](data/local/lng/strings/skills.json) `Eskillfistsoffire2` enUS = `"Charge 2 - Fire Damage Radius: %d yards + 100%% weapon damage as fire"` ✓

Gameplay-side claim ("+ 100% weapon damage as fire") is consistent with the Fists of Fire skills.txt row:

- `prgdam = 4` (`ModifyProgressiveElementalConvert`) — per eezstreet skills.js docs: "Convert calc1% of the physical damage dealt to the skill's elemental damage."
- `calc1 = 100` — so 100% of the source physical damage is converted into the skill's elemental damage (fire).
- `SrcDam = 128` — transfers 100% of weapon damage onto the skill.
- `EType = fire`, `EMin = 6`, `EMax = 10` (the flat fire component layered on top).

Combined effect: the charge releases deal `100%` of weapon damage as fire (per `SrcDam × prgdam/calc1`) plus the flat 6–10 fire baseline. The tooltip "+ 100% weapon damage as fire" annotation is therefore accurate. The other AI agent who added the weapon-damage path did configure the gameplay correctly; the only remaining issue was the printf escape, which this patch fixes.

Active and base copies of [data/global/excel/skills.txt](data/global/excel/skills.txt) hold byte-identical Fists of Fire rows. Active and base [data/global/excel/skilldesc.txt](data/global/excel/skilldesc.txt) still have 120 columns each with the FoF row at 120 columns and no malformed rows. JSON parses cleanly. No tooltip vs gameplay disagreement on this row after the escape.

Patch also updates [docs/modding-findings.md](docs/modding-findings.md) with a note that literal `%` in skills.json must be escaped to `%%`. This is good institutional knowledge to keep; it's the same class of issue as the Cobra Strike "over 4 sec" tooltip miss from last week.

## Findings

### Critical
None.

### High
None.

### Medium
None.

### Low

**LOW-001 — Non-English Fists of Fire tooltip strings do not mention the weapon-damage scaling**

- File: [data/local/lng/strings/skills.json](data/local/lng/strings/skills.json) `Eskillfistsoffire1` and `Eskillfistsoffire2` entries.
- Issue: Only the `enUS` text contains "+ 100% weapon damage as fire". All 12 other localizations (`zhTW`, `deDE`, `esES`, `frFR`, `itIT`, `koKR`, `plPL`, `esMX`, `jaJP`, `ptBR`, `ruRU`, `zhCN`) stop at the fire damage / radius line (e.g., German charge 1 reads `Ladung 1 - Feuerschaden: %d-%d` with no weapon-damage suffix). So non-English players see the base values but not the weapon-damage rider.
- Why it matters: Cosmetic / informational only. The gameplay still applies the weapon damage as fire regardless of which localization is loaded — only the tooltip text is incomplete. Same class of problem as the existing non-English `Skillsd266`/`Skillld266` Cobra Strike drift.
- Suggested fix: When a translator pass happens, mirror the "+ 100% weapon damage as fire" rider into the 12 non-English entries (with their own `100%%` escape). Out of scope for this task. Not a publish blocker.
- Blocks approval: No.

## Validation Checks

- Original user request reviewed: **Yes** — "fix fist of fire tooltip and double check the formulas, another AI agent added weapon damage to charge 1 and 2." Both halves addressed:
  - Tooltip: `100% → 100%%` (this patch).
  - Formula double-check: `prgdam=4` + `calc1=100` + `SrcDam=128` together produce a "100% of weapon damage as fire" effect — matches the tooltip claim.
- Git diff / design reviewed: **Yes**. diff.patch reviewed against [data/local/lng/strings/skills.json](data/local/lng/strings/skills.json) current state; the two enUS strings show the `%%` escape exactly as the diff lists.
- TSV column counts checked: **Yes**.
  - [data/global/excel/skills.txt](data/global/excel/skills.txt): 322 cols, 492 rows, 0 deviating rows. FoF row also 322 cols.
  - [data/global/excel/base/skills.txt](data/global/excel/base/skills.txt): same.
  - [data/global/excel/skilldesc.txt](data/global/excel/skilldesc.txt): 120 cols, FoF row 120 cols.
  - [data/global/excel/base/skilldesc.txt](data/global/excel/base/skilldesc.txt): same.
- Active/base sync checked: **Yes**. Fists of Fire rows are byte-identical between active and base skills.txt (CR-normalized diff returns no differences).
- Tooltip vs gameplay consistency considered: **Yes**. `prgdam=4` + `calc1=100` + `SrcDam=128` does deliver the "+ 100% weapon damage as fire" rider claimed by the tooltip text. The base fire damage component (`EMin=6, EMax=10`) is displayed via the `%d-%d` placeholder. Per-charge tooltip formulas in [data/global/excel/skilldesc.txt](data/global/excel/skilldesc.txt) for FoF were not touched by this patch and are unchanged from prior state.
- Live publish risk considered: **Yes**. `live_publish_allowed: true`. Pure tooltip-text and docs change — zero gameplay or save-state risk. Safe to publish.
- Docs checked: **Yes**. [docs/modding-findings.md](docs/modding-findings.md) updated with the percent-escape note and unrelated Cobra Strike status updates (the Cobra-side notes overlap with the cobra-builder-poison-fix task; both are in the same commit `685d3be8`).
- Cross-file scan: searched all `enUS` skill strings for `[0-9]+% [a-z]` patterns (unescaped percent followed by a word). **Zero matches.** No other skill tooltips share the same defect.

## Codex Action Items

None required.

## Suggested Follow-up Tests

1. **Tooltip render check** — in-game, open the Fists of Fire skill tooltip in the skill tree. Confirm charge 1 line reads `Charge 1 - Fire Damage: 6-10 + 100% weapon damage as fire` (or whatever level-scaled `%d-%d` produces) without garbled trailing characters or numeric garbage.
2. **Charge 2 tooltip** — confirm charge 2 reads `Charge 2 - Fire Damage Radius: 4 yards + 100% weapon damage as fire` (or similar) cleanly.
3. **Charge 3 tooltip** — confirm charge 3 (`Eskillfistsoffire3`) renders unchanged — its text doesn't contain literal `%` so it should already be fine.
4. **In-game damage check** — equip a weapon with a clear physical damage range, hit a stationary target with FoF charges 1 and 2, and verify the dealt fire damage matches `weapon damage × ~100%` plus the small 6–10 flat baseline (within rounding / synergy modifiers).
5. **Non-English smoke test** — optional, if Eric or another tester uses a non-English client, confirm the tooltip still parses (no formatter crash) even though it lacks the weapon-damage rider text. The format string in those languages has no `%`-followed-by-letter pattern, so they should render fine, just incomplete.
