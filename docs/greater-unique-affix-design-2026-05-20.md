# Greater Unique Affix Design

Created: 2026-05-20.

Status: design draft for Claude review. No item table changes are implemented by this document.

## Goal

Create a "Greater affix" chase layer for selected unique items by duplicating the unique row with one or two enhanced signature stats.

The pilot should prove the system on five iconic endgame uniques:

- Harlequin Crest
- Arachnid Mesh
- Griffon's Eye
- Death's Web
- Windforce

The design intentionally starts with equipment uniques that have clear signature stats. Jewellery, charms, and jewels can use the same method later, but they are not part of this first pass.

## Core Mechanic

For each target unique, keep the normal unique row and add three duplicate rows with the same base item code:

| Variant | Meaning | Relative weight inside target family |
|---|---|---:|
| Plain | Existing item, unchanged stats | 100 |
| Greater A | Signature stat package A is enhanced | 10 |
| Greater B | Signature stat package B is enhanced | 10 |
| Greater A+B | Both signature packages are enhanced | 1 |

This makes each single-Greater version 10x rarer than the plain version, and the double-Greater version 100x rarer than the plain version.

## Important Rarity Detail

`uniqueitems.txt` uses `rarity` as a weight among eligible unique rows with the same base item `code`. These target bases already have sibling uniques. If we simply add three rows, the target unique family becomes more common compared with sibling uniques on the same base.

To avoid that, use a family-normalized weighting model.

For a target unique with original rarity `R`:

```text
Plain target rarity       = 100 * R
Greater A rarity          = 10 * R
Greater B rarity          = 10 * R
Greater A+B rarity        = 1 * R
Target family total       = 121 * R
Each non-target sibling   = 121 * original sibling rarity
```

This preserves the old chance that this unique family wins against sibling uniques with the same base code, while splitting that family internally into plain and Greater outcomes.

Example for Harlequin Crest:

| Row | Old rarity | New rarity |
|---|---:|---:|
| Harlequin Crest, plain | 1 | 100 |
| Harlequin Crest, Greater Skills | new | 10 |
| Harlequin Crest, Greater Vitality | new | 10 |
| Harlequin Crest, Double Greater | new | 1 |
| Bane's Dark Wisdom | 2 | 242 |

Old Harlequin-family share on Shako uniques:

```text
1 / (1 + 2) = 33.33%
```

New Harlequin-family share:

```text
121 / (121 + 242) = 33.33%
```

Within the Harlequin family:

```text
Plain = 100 / 121 = 82.64%
Greater Skills = 10 / 121 = 8.26%
Greater Vitality = 10 / 121 = 8.26%
Double Greater = 1 / 121 = 0.83%
```

This means a single-Greater variant is exactly 10x rarer than the new plain version, and the whole Harlequin family does not become more common than before.

## Implementation Rules

- Duplicate rows in `data/global/excel/uniqueitems.txt` and mirror to `data/global/excel/base/uniqueitems.txt`.
- Allocate new unique `*ID` values after the current max ID. Current max observed: `1478`, so the first implementation should use `1479+`.
- Keep `code`, `lvl`, `lvl req`, transforms, inventory art, sounds, cost fields, carry flags, and non-target properties copied from the source row.
- Use the same `index` display strategy for all variants of a source item. Recommended display string is `Greater <Item Name>`.
- Add string keys for every new `index` in `data/local/lng/strings/item-names.json`.
- Add `greater-affix-marker` to each Greater duplicate if there is an open property slot. This renders the existing marker string:

```text
** Greater Affix
```

- Do not add the marker to the plain source row.
- If a source row already uses all 12 property slots, do not implement that item until a marker strategy is chosen.
- Do not change quality odds in `itemratio.txt`.
- Do not change the base item tables.

## Pilot Items

### Harlequin Crest

Source row:

| Field | Value |
|---|---|
| `index` | `Harlequin Crest` |
| `code` | `uap` |
| base | Shako |
| current rarity | 1 |
| current `lvl` / `lvl req` | 58 / 62 |
| same-code siblings | `Bane's Dark Wisdom` rarity 2 |

Signature packages:

| Package | Current | Greater |
|---|---|---|
| A: Skills | `allskills 2` | `allskills 3` |
| B: Life/Mana scaling | `hp/lvl param 12`, `mana/lvl param 12` | `hp/lvl param 16`, `mana/lvl param 16` |

Generated rows:

| Row | Rarity | Stat changes |
|---|---:|---|
| Greater Harlequin Crest: Skills | 10 | A only |
| Greater Harlequin Crest: Vitality | 10 | B only |
| Greater Harlequin Crest: Perfected | 1 | A and B |

Sibling scaling:

| Sibling | Old rarity | New rarity |
|---|---:|---:|
| Bane's Dark Wisdom | 2 | 242 |

### Arachnid Mesh

Source row:

| Field | Value |
|---|---|
| `index` | `Arachnid Mesh` |
| `code` | `ulc` |
| base | Spiderweb Sash |
| current rarity | 1 |
| current `lvl` / `lvl req` | 61 / 80 |
| same-code siblings | `Duskwreath` rarity 2 |

Signature packages:

| Package | Current | Greater |
|---|---|---|
| A: Skills | `allskills 1` | `allskills 2` |
| B: Casting | `cast2 20` | `cast2 30` |

Generated rows:

| Row | Rarity | Stat changes |
|---|---:|---|
| Greater Arachnid Mesh: Skills | 10 | A only |
| Greater Arachnid Mesh: Casting | 10 | B only |
| Greater Arachnid Mesh: Perfected | 1 | A and B |

Sibling scaling:

| Sibling | Old rarity | New rarity |
|---|---:|---:|
| Duskwreath | 2 | 242 |

### Griffon's Eye

Source row:

| Field | Value |
|---|---|
| `index` | `Griffon's Eye` |
| `code` | `ci3` |
| base | Diadem |
| current rarity | 1 |
| current `lvl` / `lvl req` | 84 / 76 |
| same-code siblings | `Blindsight` rarity 1, `Royal Diadem` rarity 3 |

Signature packages:

| Package | Current | Greater |
|---|---|---|
| A: Lightning skill damage | `extra-ltng 10-15` | `extra-ltng 20-25` |
| B: Enemy lightning resistance | `pierce-ltng 15-20` | `pierce-ltng 25-30` |

Generated rows:

| Row | Rarity | Stat changes |
|---|---:|---|
| Greater Griffon's Eye: Storm | 10 | A only |
| Greater Griffon's Eye: Pierce | 10 | B only |
| Greater Griffon's Eye: Perfected | 1 | A and B |

Sibling scaling:

| Sibling | Old rarity | New rarity |
|---|---:|---:|
| Blindsight | 1 | 121 |
| Royal Diadem | 3 | 363 |

### Death's Web

Source row:

| Field | Value |
|---|---|
| `index` | `Death's Web1` |
| `code` | `7gw` |
| base | Unearthed Wand |
| current rarity | 1 |
| current `lvl` / `lvl req` | 60 / 70 |
| same-code siblings | `Pull of Darkness` rarity 1 |

Signature packages:

| Package | Current | Greater |
|---|---|---|
| A: Enemy poison resistance | `pierce-pois 40-50` | `pierce-pois 55-65` |
| B: Necromancer skill package | `allskills 2`, `skilltab 7 1-2` | `allskills 3`, `skilltab 7 2-3` |

Generated rows:

| Row | Rarity | Stat changes |
|---|---:|---|
| Greater Death's Web: Venom | 10 | A only |
| Greater Death's Web: Necromancy | 10 | B only |
| Greater Death's Web: Perfected | 1 | A and B |

Sibling scaling:

| Sibling | Old rarity | New rarity |
|---|---:|---:|
| Pull of Darkness | 1 | 121 |

### Windforce

Source row:

| Field | Value |
|---|---|
| `index` | `Windforce` |
| `code` | `6lw` |
| base | Hydra Bow |
| current rarity | 1 |
| current `lvl` / `lvl req` | 80 / 85 |
| same-code siblings | `Gale Song` rarity 1, `Adamantine Bow` rarity 1 |

Signature packages:

| Package | Current | Greater |
|---|---|---|
| A: Enhanced damage | `dmg% 250-300` | `dmg% 350-400` |
| B: Attack speed | `swing2 30-45` | `swing2 50-60` |

Generated rows:

| Row | Rarity | Stat changes |
|---|---:|---|
| Greater Windforce: Force | 10 | A only |
| Greater Windforce: Gale | 10 | B only |
| Greater Windforce: Perfected | 1 | A and B |

Sibling scaling:

| Sibling | Old rarity | New rarity |
|---|---:|---:|
| Gale Song | 1 | 121 |
| Adamantine Bow | 1 | 121 |

## Expected Row Count

For the five-item pilot:

| Change type | Count |
|---|---:|
| New Greater duplicate unique rows | 15 |
| Existing sibling rows with rarity scaled | 10 |
| Existing source rows with rarity changed to plain weight | 5 |
| New item-name string keys | 15 |

## Open Questions For Review

1. Should the visible item name be `Greater <Item Name>` for all three variants, or should the display name remain the original item name and rely on the marker/stat lines?
2. Is the family-normalized rarity model preferred, or should the Greater variants add extra chance on top of the existing item instead?
3. Are the proposed stat bumps exciting enough without being too far beyond the current unique's identity?
4. Should double-Greater variants get a second `greater-affix-marker` line or a different string such as `** Double Greater Affix`?
5. Should this system eventually apply to jewellery and charms, or stay equipment-only?

## Recommended Next Step

Have Claude review the rarity math and the five proposed stat packages. If approved, implement the pilot with a script that:

1. Locates each source row by `index`.
2. Scales sibling rarity values by 121.
3. Rewrites the source row rarity to `100 * original_rarity`.
4. Appends three duplicate rows per source item.
5. Adds item-name string entries.
6. Mirrors active/base files.
7. Emits a TSV report of every changed and added row.
