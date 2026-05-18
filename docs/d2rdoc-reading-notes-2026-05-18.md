# D2RDoc Reading Notes

Created: 2026-05-18.

Source: https://eezstreet.github.io/d2rdoc/

## Crawl Scope

Read the D2RDoc sitemap current on 2026-05-18:

- 100 HTML pages total.
- 3 root pages: `index.html`, `about.html`, `changelog.html`.
- 91 `files/*.html` data-file reference pages.
- 2 guide pages: `guides/getting-started.html`, `guides/desecratedzones.html`.
- 4 standalone docs: `docs/bbe-calc.html`, `docs/game-mode-split.html`, `docs/genericpetai.html`, `docs/itemratio-calc.html`.
- Also checked `data/community-notes.js` because file-reference pages load important community caveats from that script.

Generated file-reference pages were read through their HTML/no-script content and backing data scripts where needed. This matters for shared append-file definitions such as item affix fields used by `magicprefix.txt`, `magicsuffix.txt`, and `automagic.txt`.

## General Modding Workflow

`guides/getting-started.html` reinforces the loose-file workflow we already use:

- D2R supports modded art assets, data tables, and UI layout JSON.
- Particle effects, animation editing, level editing, and code editing are limited or unsupported by ordinary loose-file modding.
- A mod lives under `mods/<ModName>/<ModName>.mpq`.
- `modinfo.json` needs at least `name` and `savepath`.
- Launch with `-mod <ModName> -txt`.
- Main data tables are tab-delimited `.txt` files under `data/global/excel`.
- String edits usually live under `data/local/lng/strings`.
- Excel can save these files incorrectly; keep using TSV-aware scripts/editors instead.

## Game Mode Split

`docs/game-mode-split.html` is directly relevant to this repo:

- Classic/Expansion modes use files in `data/global/excel/base/`.
- Reign of the Warlock uses files in `data/global/excel/`.
- There is no inheritance between the split copies.
- Some files are shared and always use the non-base path; D2RDoc explicitly calls out `sounds.txt` and `soundenviron.txt`.

Project implication: continue mirroring active/base files only when both modes should receive the same gameplay data. Do not assume base values inherit from active values.

## Item Quality And Rare Rarity

Important pages:

- `files/itemratio.html`
- `docs/itemratio-calc.html`
- `files/treasureclassex.html`

Item quality roll order is:

```text
Unique -> Set -> Rare -> Magic -> High Quality -> Normal -> Low Quality
```

The item-ratio probability is a divisor. Lower values mean better odds; higher `Rare` / `RareMin` values make rares harder to roll.

Base probability:

```text
Probability = ( Quality - ( mlvl - ilvl ) / Divisor ) * 128
```

Magic find then reduces the divisor. Unique/Set/Rare use diminishing returns above the threshold; D2RDoc lists the quality-specific diminishing return constants as:

```text
Unique = 250
Set = 500
Rare = 600
```

The `Min` field then caps how low the divisor can go after MF. Treasure-class quality modifiers are applied after the minimum comparison:

```text
Probability = Probability - Probability * TreasureClass / 1024
```

Finally, the game rolls 0 through `Probability`; success is the 0-128 band. The important design consequence is that `RareMin` matters a lot in high-MF/high-level cases because it prevents odds from improving past the cap.

`itemratio.txt` `Uber=1` means exceptional or elite base items. It does not split exceptional from elite. The rare-item overhaul therefore cannot make only elite rares rarer through `itemratio.txt`; elite-specific feeling needs to come from affix level/availability and base-level distribution.

## Affix Pool Mechanics

Important pages/scripts:

- `files/magicprefix.html`
- `files/magicsuffix.html`
- `data/files/shareditemmods.js`
- `files/properties.html`
- `files/itemstatcost.html`
- `files/itemtypes.html`

`magicprefix.txt`, `magicsuffix.txt`, and `automagic.txt` share the item-mod structure.

For Greater Affixes:

- `spawnable=0` means the affix is not part of normal magic-affix randomization.
- `rare=1` allows the affix to appear on rare items.
- `level` is the minimum item level required for the affix to spawn.
- `maxlevel` is the maximum item level band for that row.
- `levelreq` is the character level required to equip the resulting item.
- `frequency` is a weight, not a rarity value. Higher frequency means more common among eligible affixes.
- `group` prevents more than one affix from the same family spawning on one item. Empty group defaults to group 0.
- Affix rows can carry up to three property payloads through `mod1`, `mod2`, and `mod3`.
- `itype#` and `etype#` include/exclude item types and rely on `itemtypes.txt` hierarchy.

Project implication: Greater Affixes should generally share the normal affix family's `group` so the Greater version replaces the normal version rather than stacking with it. Greater rows should be low frequency, while ordinary/filler rows can have higher frequencies to dilute Greater outcomes.

## Cube Recipes

Important page:

- `files/cubemain.html`

Key reminders:

- `enabled=1` is required for an in-game recipe.
- `numinputs` is the number of consumed cube inputs.
- `input 1` through `input 7` define required inputs.
- `output`, `output b`, and `output c` define multiple outputs.
- `op`, `param`, and `value` gates can make recipes conditional.
- Comment columns beginning with `*` are ignored by the game.

Current project-specific confirmation from testing and docs: `qty=N` on loose cube inputs such as `ooi,qty=11` is valid for matching multiple loose copies of an item, but it still must fit the cube's physical input capacity.

## Items And Item Types

Important pages:

- `files/weapons.html`
- `files/armor.html`
- `files/misc.html`
- `files/itemtypes.html`
- `files/uniqueitems.html`
- `files/setitems.html`
- `files/qualityitems.html`
- `files/lowqualityitems.html`

Useful reminders:

- `weapons.txt`, `armor.txt`, and `misc.txt` form the combined item structure.
- Item-type inclusion/exclusion in affixes, cube recipes, shops, and drops depends on `itemtypes.txt` codes and parent equivalence.
- `normcode`, `ubercode`, and `ultracode` distinguish normal, exceptional, and elite base families in weapon/armor tables.
- `uniqueitems.txt` row order defines unique IDs; avoid reordering.
- `setitems.txt` controls individual set item modifiers and set membership.
- `qualityitems.txt` controls superior/high-quality modifier groups.
- Community note: a row with `spawnable=1` can still be created through the Horadric Cube even when it is not intended as a random drop. Validate cube paths separately from random drop paths.

## Skills, Missiles, States, And Tooltips

Important pages:

- `files/skills.html`
- `files/missiles.html`
- `files/skilldesc.html`
- `files/states.html`
- `files/events.html`
- `files/overlay.html`
- `files/misscalc.html`
- `files/skillcalc.html`

Useful reminders:

- Skill row order determines skill IDs; avoid reordering.
- Missile row order determines missile IDs; avoid reordering.
- Skill behavior is split between server/client function fields, missile references, calc fields, states, and elemental damage fields.
- `skilldesc.txt` controls display and tooltip formulas, not gameplay.
- Tooltips can easily disagree with runtime mechanics unless `skills.txt`, `missiles.txt`, `skilldesc.txt`, and string JSON are changed together.
- Community note: `skills.txt` `auraeventfunc#` code 33 can crash if the associated skill's `ItemTarget` is set to 4.

## Monster, Treasure, Level, And Hireling Tables

Important pages:

- `files/treasureclassex.html`
- `files/monstats.html`
- `files/monstats2.html`
- `files/monlvl.html`
- `files/monprop.html`
- `files/monumod.html`
- `files/levels.html`
- `files/levelgroups.html`
- `files/hireling.html`
- `files/hirelingdesc.html`

Useful reminders:

- `treasureclassex.txt` controls linked item/drop groups and quality modifiers.
- `monstats.txt` / `monstats2.txt` split monster gameplay values from animation/display-related setup.
- `monlvl.txt` provides level-scaling baselines used by monsters across difficulties.
- Hireling behavior and display are split between `hireling.txt` and `hirelingdesc.txt`.
- Area/level changes tend to involve multiple linked files (`levels`, `lvltypes`, `lvlprest`, `lvlmaze`, `lvlsub`, `lvlwarp`, `levelgroups`), so they should be treated as higher risk than single-table item tweaks.

## UI And Stash Layout

Important pages:

- `files/inventory.html`
- `files/itemuicategories.html`
- `files/runeworduicategories.html`
- `files/storepage.html`
- `files/colors.html`

Community note relevant to our orb/stash work:

- `misc.txt` `AdvancedStashStackable` alone is not enough; visible stash support also needs the appropriate `bankexpansionlayouthd.json` layout edits.

## Practical Rules For This Repo

- Use D2RDoc as the field-reference baseline before changing unfamiliar columns.
- Keep active/base split behavior in mind on every data-file edit.
- Use TSV-aware scripts and column-count validation after every TXT edit.
- Do not reorder row-ID tables unless the goal explicitly requires it.
- For rare item work, update `itemratio.txt`, `magicprefix.txt`, `magicsuffix.txt`, and docs together in small checkpoints.
- For any tooltip-facing skill work, treat tooltip and mechanics as separate systems and validate both.
