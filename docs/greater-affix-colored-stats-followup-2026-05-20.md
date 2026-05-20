# Greater Affix Colored Stats — Follow-up Spec

Created: 2026-05-20. Status: design draft for Codex to implement.

## Goal

Color the Greater affix stat line itself (e.g. `+451-500% Enhanced Damage`) in a non-default
color (orange / gold / purple — TBD by Eric) so the player can identify a Greater roll at a
glance, **without** consuming one of the 3 magicprefix/magicsuffix mod slots for a
`greater-affix-marker` row.

This replaces (or supplements — see Open Questions) the current marker approach.

## How D2R colors stat lines

The color of an affix's display line is controlled by the **stat's display string** in
`data/local/lng/strings/item-modifiers.json`, not by the magicprefix/magicsuffix row.

Reference example already present in this mod — `+1 Bone Spear Projectiles` shown in gold on
a rare Grim Wand. Its display key is `extraspear`:

```text
"Key":  "extraspear"
"enUS": "ÿc4%+d Bone Spear Projectilesÿc3"
```

Where:

- `ÿ` is the byte `0xff` (the color-control prefix).
- `ÿc4` switches subsequent text to **color 4 (gold)**.
- `ÿc3` at the end resets back to **color 3 (blue / default magic)** so it doesn't bleed
  into other tooltip lines.

D2R color codes (commonly used):

| Code | Color |
|---|---|
| `ÿc0` | white |
| `ÿc1` | red |
| `ÿc2` | bright green (set) |
| `ÿc3` | blue (default magic) |
| `ÿc4` | gold (unique) |
| `ÿc8` | orange |
| `ÿc9` | yellow (rare item name) |
| `ÿc;` | purple |

## The catch — and why we need custom stats

The display key is per-**stat**, not per-affix-row. If we color `dmg%`'s display string in
`item-modifiers.json` (e.g. wrap it in `ÿc8...ÿc3`), then **every** item using `dmg%`
(rare swords, magic shields, runewords, uniques, jewels) gets the orange `dmg%` line — not
just the Greater versions. That breaks the visual distinction.

To color only the Greater roll, we need a stat that is unique to Greater affixes.

## Implementation plan

For every stat used on a Greater affix row, create a `greater_<stat>` duplicate that
behaves identically but has its own display string in `item-modifiers.json`.

### Per stat, three edits

1. **`data/global/excel/itemstatcost.txt`** — add a new row that mirrors the source stat
   exactly (same `Send Other`, `Signed`, `Send Bits`, `Send Param Bits`, `UpdateAnimRate`,
   `Saved`, `CSvSigned`, `CSvBits`, `CSvParam`, `fCallback`, `fMin`, `MinAccr`, `Encode`,
   `Max`, `MaxAccr`, `op`, `op param`, `op base`, `op stat1-3`, `direct`, `maxstat`,
   `itemspecific`, `damagerelated`, `itemevent`, `itemeventfunc`, `descpriority`,
   `descfunc`, `descval`, `descstr2`, `dgrp`, `dgrpfunc`, `dgrpval`, `dgrpstrpos`,
   `dgrpstrneg`, `dgrpstr2`, `stuff` — i.e. all behavior columns), but with:
   - `Stat` = `greater_<source_stat>` (e.g. `greater_dmg%`, `greater_att`, `greater_allskills`)
   - `descstrpos` and `descstrneg` pointing at a **new** key (e.g. `strModGreaterDmgPercent`)
2. **`data/local/lng/strings/item-modifiers.json`** — add a new entry with:
   - A unique `id` (allocate above the current max — see the strings-limits note below)
   - `Key` matching the new `descstrpos`/`descstrneg`
   - `enUS` value wrapping the **existing** source stat's display text in `ÿc8…ÿc3` (or
     whichever color Eric picks). Localize the other locales too, or copy the enUS string
     across them as a placeholder (current convention in this mod's recently-added strings).
3. **`data/global/excel/magicprefix.txt` and `magicsuffix.txt`** — on every Greater row
   that currently uses the source stat, swap the `modXcode` from the source stat to the
   `greater_<source_stat>` variant. Keep `modXparam`/`modXmin`/`modXmax` exactly as they
   were. Apply the change to both active (`data/global/excel/`) and base
   (`data/global/excel/base/`) copies.

### Enumerate the stat list first

Before editing, generate the full distinct stat list across all Greater rows:

- Filter: every row in `magicprefix.txt` / `magicsuffix.txt` where `spawnable=0`,
  `rare=1`, and at least one of `mod1code`/`mod2code`/`mod3code` is `greater-affix-marker`
  (the marker reliably identifies a Greater row added by this mod, separate from
  pre-existing rare-only rows like Hulking and group 307 pierce).
- Collect every non-empty `modXcode` value that is **not** `greater-affix-marker` itself.
- That set is the list of stats that need `greater_` duplicates.

Expected size: roughly 15–25 distinct stats. Likely candidates based on the design
(non-exhaustive): `att`, `dmg%`, `dmg-min`, `dmg-max`, `dmg-norm`, `ac%`, `red-dmg`,
`red-dmg%`, `allskills`, `skilltab`, `skill-rand`, `lifesteal`, `manasteal`, `hp`, `mana`,
`res-all`, `res-fire`, `res-cold`, `res-ltng`, `res-pois`, `res-mag`, `addxp`, `str`, `dex`,
`vit`, `enr`, `mag%`, `gold%`, `swing2`, `swing3`, `cast2`, `cast3`, `move3`, `balance3`,
`crush`, `deadly`, `openwounds`, `pierce-*`, `extra-*`, `abs-*%`, `aura`, `att-undead`,
`dmg-undead`, `att-demon`, `dmg-demon`, `dmg-elem`, etc. Codex should enumerate from the
actual data, not from this list.

### Open questions Eric needs to answer before implementation

1. **Which color?** `ÿc8` orange and `ÿc;` purple are the two most "chase" colors that don't
   collide with existing item-quality colors (gold = unique, green = set, white = runeword,
   blue = magic, yellow = rare name). Recommend `ÿc8` orange — already used by the
   `greater-affix-marker` line, so it stays visually consistent.
2. **Keep the marker mod slot or drop it?**
   - **Keep** (1 mod slot + colored stat): redundant signal but very clear.
   - **Drop** (0 mod slots, only colored stat): frees a property slot for actual stats —
     useful for rows that currently get the marker dropped due to 3-slot saturation (e.g.
     Wraithly1 variants of Greater Grandmaster's / Greater Godly carrying
     `dmg%`+`ethereal`+`rep-dur`). Recommend dropping the marker and relying on the
     colored stat.
3. **Double-Greater handling.** When a Greater pilot row gets implemented for unique items
   (per `docs/greater-unique-affix-design-2026-05-20.md`), it can have two boosted stats.
   With colored stats, double-Greater is visually obvious — both boosted stat lines are
   colored. No additional work needed.

## Affected files summary

For ~20 stats, the implementation touches:

- `data/global/excel/itemstatcost.txt` — append ~20 new rows.
- `data/local/lng/strings/item-modifiers.json` — append ~20 new entries.
- `data/global/excel/magicprefix.txt` and `data/global/excel/base/magicprefix.txt` — edit
  ~500 Greater rows' `modXcode` fields (one-column swap per row).
- `data/global/excel/magicsuffix.txt` and `data/global/excel/base/magicsuffix.txt` —
  similar, ~400 rows.
- (Optional, if dropping the marker) clear `greater-affix-marker` mod slots on every
  Greater row that currently carries it.

Script it. Manual edits across 900+ rows will introduce drift between active and base.

## Validation after implementation

1. **TSV integrity** — column counts unchanged (`itemstatcost.txt`,
   `magicprefix.txt`/`magicsuffix.txt`), active == base.
2. **Stat-uniqueness check** — every new `greater_<stat>` Stat name unique within
   `itemstatcost.txt`; every new `Key` unique within `item-modifiers.json`; every new `id`
   unique across the file.
3. **In-game smoke test** — drop a rare item, force-roll a Greater affix via the test rows
   already in place (the 5 families at `freq=999999`), confirm the Greater stat line
   renders in the chosen color and that non-Greater rolls of the same stat still render
   blue.

## Out of scope for this task

- Unique-item Greater coloring (`docs/greater-unique-affix-design-2026-05-20.md`) — that
  design will benefit from this mechanism but should be reviewed separately.
- Colored stat lines for non-Greater chase rows (e.g. coloring `Grandmaster's` itself
  gold) — possible by the same mechanism but a deliberate design choice that needs Eric's
  call.

## Note on strings limits

Adding ~20 new `item-modifiers.json` entries is well under any practical D2R limit. The
mod currently runs 442 entries in `item-modifiers.json`, 3 227 in `item-names.json`, 2 432
in `skills.json`, with the highest observed `id` in the 57 000 range. Classic D2 LoD had a
65 535 string-ID cap baked into its old `.tbl` format; D2R replaced that with JSON loading
which removed the hard cap. No documented D2R-specific ceiling has been hit in this mod or
others I'm aware of. ~20 more entries is a rounding error.
