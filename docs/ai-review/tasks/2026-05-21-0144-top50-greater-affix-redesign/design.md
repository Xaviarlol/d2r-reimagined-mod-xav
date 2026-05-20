# Top 50 Greater Affix Redesign Plan

## Goal

Replace the current broad Greater Affix experiment with a focused set of 50 chase affix families. The new system should:

- Remove low-impact Greater affixes such as light radius, single stat rolls, minor life/mana, thorns, stamina, and ordinary single resist rolls.
- Keep only affixes that feel like trophy rare outcomes or build-defining discoveries.
- Stay below the D2R `itemstatcost.txt` hard limit by using one colored marker stat per kept Greater family.
- Recalculate Greater frequencies after deleting the unused Greater rows.
- Preserve the existing Phase 1 rare-affix level and requirement rework unless explicitly changed later.

## Current Problem

The current tables contain 909 Greater affix rows collapsed into about 303 payload families. The colored-stat experiment hit the apparent `itemstatcost.txt` hard limit at 511 IDs, so the current "clone every Greater stat" model is not viable.

There is also naming/payload drift. For example:

- Current `Greater Grandmaster's` rows at `magicprefix.txt` lines 1301-1303 are actually the normal `Wraithly1` family payload: Enhanced Damage, Ethereal, and Self Repair.
- Current `Greater Godly` armor rows include Wraithly-style armor payloads and a broad ED + DR% row that should be narrowed/renamed in the redesign.

The redesign should rebuild from clean source rows rather than trying to preserve these drifted names.

## Baseline Strategy

Use current `xav-custom` tables after commit `6dca8854` as the working state, but treat the non-Greater rows as the canonical baseline.

Do not check out the full pre-`00337b07` files wholesale, because that would undo the Phase 1 level/levelreq changes. Instead:

1. Parse current `magicprefix.txt` and `magicsuffix.txt`.
2. Remove all rows whose name/description/mod codes indicate they are Greater rows.
3. Keep all non-Greater rows exactly as currently present, including Phase 1 level/levelreq changes and existing non-Greater frequency weights.
4. Re-add only the selected 50 Greater families from the normal apex source rows listed below.
5. Mirror active files into `data/global/excel/base/`.

This gives us a clean "current rare rework plus curated Greater affixes" state.

## Tooltip / ItemStatCost Strategy

Do not clone every gameplay stat into a colored Greater variant.

Instead, for each of the 50 kept Greater families:

1. Add one inert marker stat in `itemstatcost.txt`, e.g. `item_greaterAffix_grandmasters`.
2. Add one property wrapper in `properties.txt`, e.g. `greater_affix_grandmasters`, that applies the inert marker stat.
3. Put that marker property in `mod1code` for the Greater affix row, then put actual gameplay stats in `mod2code` / `mod3code` where possible.
4. For affixes that already require three gameplay mods, use a dedicated property wrapper that applies the marker plus one gameplay stat, preserving the two remaining gameplay slots.
5. The marker stat displays one colored line such as:

```text
Greater Affix: Grandmaster's
```

This uses 50 marker itemstatcost rows instead of hundreds of cloned gameplay stats, and avoids the 511 ID crash path. The actual gameplay stat lines remain normal color unless a later smaller experiment proves per-stat coloring is safe.

## Frequency Model

For every selected Greater family, create three level bands:

| Band | Level | MaxLevel | Intended rarity |
|---|---:|---:|---|
| early | 50 | 65 | about 30x rarer than the apex row |
| mid | 66 | 80 | about 15x rarer than the apex row |
| late | 81 | blank | about 10x rarer than the apex row |

For each selected family:

1. Identify the matching normal apex row by side, group, item scope, and payload.
2. Use the current non-Greater apex row's late/high frequency as `apex_freq`.
3. Set:
   - `late_freq = max(1, round(apex_freq / 10))`
   - `mid_freq = max(1, round(late_freq * 2 / 3))`
   - `early_freq = max(1, round(late_freq / 3))`
4. Set `levelreq` to the current non-Greater apex `levelreq`.
5. Do not add `maxlevel` to the late band.

This preserves the older 1:2:3 Greater-band shape while recalculating only for the 50 kept families. Claude should specifically verify whether the formula should use the apex row's late frequency or the full same-family frequency sum where the source family has multiple high-tier rows.

## Selected 50 Families

| # | Greater family | Source apex | Side | Main payload |
|---:|---|---|---|---|
| 1 | Greater Grandmaster's | Grandmaster's | Prefix | ED + Attack Rating |
| 2 | Greater Wraithly Weapon | Wraithly1 | Prefix | Weapon ED + Ethereal + Self Repair |
| 3 | Greater Wraithly Armor | Wraithly1 | Prefix | Armor ED + Ethereal + Self Repair |
| 4 | Greater Godly | Godly / Reinforced1 | Prefix | Armor or shield ED + Damage Reduction % |
| 5 | Greater Jeweler's | Jeweler's | Prefix | 4 sockets |
| 6 | Greater Visionary | Visionary | Prefix | Attack Rating % per level |
| 7 | Greater Gritty | Gritty | Prefix | Max Damage per level |
| 8 | Greater Evisceration | of Evisceration | Suffix | Huge Max Damage |
| 9 | Greater Transcendence Damage | of Transcendence | Suffix | Huge Min Damage |
| 10 | Greater Quickness | of Quickness | Suffix | High IAS |
| 11 | Greater Alacrity | of Alacrity | Suffix | IAS on weapons/gloves |
| 12 | Greater Fervor | of Fervor | Suffix | IAS jewel |
| 13 | Greater Deflecting | of Deflecting | Suffix | Block + Faster Block |
| 14 | Greater Chromatic | Chromatic | Prefix | All Resistances |
| 15 | Greater Scintillating | Scintillating | Prefix | All Resistances on compact slots |
| 16 | Greater Four Seasons | of the Four Seasons2 | Suffix | All Maximum Resistances |
| 17 | Greater Elements | of the Elements | Suffix | Scaling Cold/Fire/Lightning Resist |
| 18 | Greater Magus | of the Magus | Suffix | High Faster Cast Rate |
| 19 | Greater Apprentice | of the Apprentice | Suffix | Broad Faster Cast Rate |
| 20 | Greater Equilibrium | of Equilibrium | Suffix | High Faster Hit Recovery |
| 21 | Greater Traveling / Speed | of Traveling / of Speed | Suffix | Faster Run/Walk |
| 22 | Greater Omniscient | Omniscient | Prefix | +All Skills |
| 23 | Greater Sage's | Sage's | Prefix | +All Skills on alternate slots |
| 24 | Greater Arch-Angel's | Arch-Angel's | Prefix | Sorceress skills |
| 25 | Greater Witch-hunter's | Witch-hunter's | Prefix | Assassin skills |
| 26 | Greater Valkyrie's | Valkyrie's | Prefix | Amazon skills |
| 27 | Greater Priest's | Priest's | Prefix | Paladin skills |
| 28 | Greater Berserker's | Berserker's | Prefix | Barbarian skills |
| 29 | Greater Necromancer's | Necromancer's | Prefix | Necromancer skills |
| 30 | Greater Hierophant's | Hierophant's | Prefix | Druid skills |
| 31 | Greater Arch-Devil's | Arch-Devil's | Prefix | Warlock skills |
| 32 | Greater Cunning | Cunning | Prefix | Traps |
| 33 | Greater Rose Branded | Rose Branded | Prefix | Paladin Combat Skills |
| 34 | Greater Pyromaniac's Damage | Pyromaniac's | Prefix | Fire Skill Damage |
| 35 | Greater Pyromaniac's Pierce | Pyromaniac's2 | Prefix | Enemy Fire Resist Pierce |
| 36 | Greater Zeus's Damage | Zeus's | Prefix | Lightning Skill Damage |
| 37 | Greater Zeus's Pierce | Zeus's2 | Prefix | Enemy Lightning Resist Pierce |
| 38 | Greater Frost Wyrm's Damage | Frost Wyrm's | Prefix | Cold Skill Damage |
| 39 | Greater Frost Wyrm's Pierce | Frost Wyrm's2 | Prefix | Enemy Cold Resist Pierce |
| 40 | Greater Manticore's Damage | Manticore's | Prefix | Poison Skill Damage |
| 41 | Greater Manticore's Pierce | Manticore's2 | Prefix | Enemy Poison Resist Pierce |
| 42 | Greater Lich | of the Lich | Suffix | Dual leech |
| 43 | Greater Transcendence Amp | of Transcendence | Suffix | CTC Amplify Damage + Physical Pierce |
| 44 | Greater Transcendence Lower Resist | of Transcendence | Suffix | CTC Lower Resist + Elemental Pierce |
| 45 | Greater Aureole Might | Aureole | Prefix | Levelled Might aura |
| 46 | Greater Aureole Fanaticism | Aureole | Prefix | Levelled Fanaticism aura |
| 47 | Greater Aureole Conviction | Aureole | Prefix | Levelled Conviction aura |
| 48 | Greater Aureole Holy Freeze | Aureole | Prefix | Levelled Holy Freeze aura |
| 49 | Greater Aureole Meditation | Aureole | Prefix | Levelled Meditation aura |
| 50 | Greater Aureole Vigor | Aureole | Prefix | Levelled Vigor aura |

## Implementation Steps After Approval

1. Write a script, likely `scripts/implement_top50_greater_affixes.py`, that performs the transformation deterministically.
2. Load current active prefix/suffix tables.
3. Remove all current Greater rows.
4. Add the 50 selected Greater families as three rows each unless the source family must remain single-band for technical reasons.
5. Recalculate frequencies with the model above.
6. Add exactly 50 marker stats/properties for colored tooltip marker lines.
7. Remove unused Greater marker/properties/itemstatcost rows from the prior experiment.
8. Validate:
   - active/base prefix files match.
   - active/base suffix files match.
   - row widths match headers.
   - `itemstatcost.txt` row count stays safely under 511 IDs.
   - no removed Greater properties are still referenced.
   - all selected Greater rows have `spawnable=1`, `rare=1`, and a marker property.
9. Commit and push.
10. Publish to live game folder only after implementation review approval or Eric's explicit override.

## Open Questions For Claude

1. Is the one-marker-stat-per-family tooltip approach safer than cloning gameplay stats for color?
2. Does the proposed frequency formula correctly preserve the "late Greater is about 10x rarer than source apex" goal after deleting most Greater rows?
3. Should frequency use a single source apex row, or the sum of equivalent source apex rows where a family has split high-tier rows?
4. Are any of the 50 selected families technically unsafe because they require too many gameplay mods plus a marker?
5. Are the aura Greater affixes safe as rare prefixes, and should their aura levels be 4 fixed as currently proposed or a different value?
6. Are there selected families that should be merged, split, or replaced before implementation?
7. Does this preserve the Phase 1 rare-affix level/requirement work?
