# Greater Affix And Rare Frequency Rework

Created: 2026-05-18.

Status: design only, not implemented.

This replaces the earlier "add a handful of Greater rows" pilot. Eric clarified that the real rare rework is broader: top affixes, not only Greater Affixes, should be able to appear earlier, but lower-level rares should see them much less often.

## Corrected Model

There should be one player-facing Greater Affix per category, such as `Greater Cruel`.

To make that one Greater category rarer or more common by item level, implement multiple technical rows with the same player-facing idea and same stat payload:

| Technical Band | level | maxlevel | frequency |
|---|---:|---:|---:|
| Early | 50 | 65 | 1 |
| Mid | 66 | 80 | 2 |
| Late | 81 | 100 or blank | 3 |

Example:

| Row Name | level | maxlevel | frequency | Mods |
|---|---:|---:|---:|---|
| Greater Cruel | 50 | 65 | 1 | `dmg% 350-400` |
| Greater Cruel | 66 | 80 | 2 | `dmg% 350-400` |
| Greater Cruel | 81 | 100 or blank | 3 | `dmg% 350-400` |

All three technical rows use the same `group` as normal Cruel so only one enhanced-damage family prefix can appear on a rare item.

## Frequency Ratio Rule

Frequency is a weight. If two affixes are eligible for the same item, relative rarity is approximately:

```text
affix A relative odds = frequency A / frequency B
```

The exact final chance also depends on the total eligible prefix/suffix pool for that item type and item level, but direct frequency ratios are still the right first-order balancing tool.

For `Greater Cruel`, Eric's target is:

- Late Greater Cruel should be about 10x rarer than normal Cruel.
- Early Greater Cruel should be about 30x rarer than normal Cruel.

With Greater Cruel frequencies `1 / 2 / 3`, this implies normal late Cruel should be around `30` frequency:

| Comparison | Greater Freq | Normal Cruel Freq | Relative Rarity |
|---|---:|---:|---:|
| Early Greater vs normal Cruel | 1 | 30 | 30x rarer |
| Mid Greater vs normal Cruel | 2 | 30 | 15x rarer |
| Late Greater vs normal Cruel | 3 | 30 | 10x rarer |

This means the current file cannot just add `Greater Cruel` at `1 / 2 / 3` and call it done:

- Current normal `Cruel` is `frequency=114`.
- If normal Cruel stays at `114`, late Greater Cruel at `3` is about `38x` rarer than Cruel, not `10x`.
- Early Greater Cruel at `1` would be about `114x` rarer than Cruel.

So the rework needs frequency normalization, not only new Greater rows.

## Are We Wrong To Reweight Existing Frequencies?

No. The user's concern is correct.

Any ordinary affix with `frequency=1` and overlapping eligibility would be as common as an early Greater row. That is not what we want unless that ordinary row is also intended to be chase-tier. Many existing `frequency=1` rows are not necessarily designed as true Greater-grade chase affixes, so they need audit and likely reweighting.

Likewise, ordinary junk/filler affixes may need higher frequency so they continue to dilute powerful rows, especially at lower item levels.

Important nuance: not every current row moves in the same direction.

- Very high-frequency rows like current `Cruel` at `114` may need to come down if Greater rows are fixed at `1 / 2 / 3` and the target ratio is only 10x at the late band.
- Current `frequency=1` ordinary rows probably need to go up, often to at least `3`, unless they are intentionally chase-tier.
- Junk/filler rows generally need to stay high or become higher, especially in early bands.

## Two Ways To Make Early Top Affixes Rare

### 1. Explicit banded rows

Create early/mid/late technical rows for each important affix family.

Example for normal Cruel and Greater Cruel:

| Player-Facing Affix | level | maxlevel | frequency | Mods |
|---|---:|---:|---:|---|
| Cruel | 50 | 65 | 10 | `dmg% 267-300` |
| Cruel | 66 | 80 | 20 | `dmg% 267-300` |
| Cruel | 81 | blank | 30 | `dmg% 267-300` |
| Greater Cruel | 50 | 65 | 1 | `dmg% 350-400` |
| Greater Cruel | 66 | 80 | 2 | `dmg% 350-400` |
| Greater Cruel | 81 | blank | 3 | `dmg% 350-400` |

This makes Cruel itself rarer on lower-level rares while preserving a clean 10:1 normal-to-Greater ratio inside each band.

Compared to the late normal Cruel baseline frequency of `30`, early Greater Cruel is still `30x` rarer, mid Greater Cruel is `15x` rarer, and late Greater Cruel is `10x` rarer.

This is the most explicit and easiest-to-audit approach.

### 2. Pool shaping through broader low-level eligibility

Make the lower-level affix pool larger by allowing many ordinary and junk affixes to remain eligible at lower levels, then retire or reduce some of that junk at higher levels with `maxlevel`.

This can make early top affixes rarer because the denominator is larger:

```text
Greater chance ~= Greater frequency / total eligible frequency
```

This approach is useful as a supporting lever, but it is harder to reason about because total eligible weight changes by item type, prefix/suffix side, and item level.

Recommended direction: use explicit banded rows for high-value affix families, then use pool shaping only to tune the overall feel after the main families are in place.

## Before And After Examples

These are design examples, not yet implemented values.

### Weapon Damage: Cruel / Greater Cruel

Current:

| Affix | level | maxlevel | frequency | Mods |
|---|---:|---:|---:|---|
| Cruel | 74 | blank | 114 | `dmg% 267-300` |
| Greater Cruel | none | none | none | Does not exist |

Proposed:

| Affix | level | maxlevel | frequency | Mods |
|---|---:|---:|---:|---|
| Cruel | 50 | 65 | 10 | `dmg% 267-300` |
| Cruel | 66 | 80 | 20 | `dmg% 267-300` |
| Cruel | 81 | blank | 30 | `dmg% 267-300` |
| Greater Cruel | 50 | 65 | 1 | `dmg% 350-400` |
| Greater Cruel | 66 | 80 | 2 | `dmg% 350-400` |
| Greater Cruel | 81 | blank | 3 | `dmg% 350-400` |

Meaning:

- Before, Cruel only appears at affix level 74+.
- After, Cruel can appear at affix level 50+, but is 3x more common late than early.
- Greater Cruel can also appear at 50+, but is much rarer.

### Armor Defense: Godly / Greater Godly

Current:

| Affix | level | maxlevel | frequency | Mods |
|---|---:|---:|---:|---|
| Godly | 86 | blank | 110 | `ac% 201-225` |
| Greater Godly | none | none | none | Does not exist |

Proposed:

| Affix | level | maxlevel | frequency | Mods |
|---|---:|---:|---:|---|
| Godly | 55 | 65 | 10 | `ac% 201-225` |
| Godly | 66 | 80 | 20 | `ac% 201-225` |
| Godly | 81 | blank | 30 | `ac% 201-225` |
| Greater Godly | 55 | 65 | 1 | `ac% 275-325` |
| Greater Godly | 66 | 80 | 2 | `ac% 275-325` |
| Greater Godly | 81 | blank | 3 | `ac% 275-325` |

Meaning:

- Before, top Godly armor defense waits until very high affix levels.
- After, exceptional and early elite armor can rarely spike into high defense.
- Greater Godly remains a true chase roll.

### Jewelry Stats: Zodiac / Greater Zodiac

Current:

| Affix | level | maxlevel | frequency | Mods |
|---|---:|---:|---:|---|
| of the Zodiac | 86 | blank | 12 | `all-stats 21-30` |
| Greater Zodiac | none | none | none | Does not exist |

Proposed:

| Affix | level | maxlevel | frequency | Mods |
|---|---:|---:|---:|---|
| of the Zodiac | 60 | 70 | 10 | `all-stats 21-30` |
| of the Zodiac | 71 | 85 | 20 | `all-stats 21-30` |
| of the Zodiac | 86 | blank | 30 | `all-stats 21-30` |
| Greater Zodiac | 60 | 70 | 1 | `all-stats 35-45` |
| Greater Zodiac | 71 | 85 | 2 | `all-stats 35-45` |
| Greater Zodiac | 86 | blank | 3 | `all-stats 35-45` |

Meaning:

- This is an example where the existing normal top affix frequency is only `12`.
- If late Greater is `3` and we want it about `10x` rarer than normal Zodiac, late normal Zodiac needs to rise toward `30`.
- This confirms that some existing low-frequency ordinary rows must be increased.

### Current Frequency=1 Rows

Example current rows include some `+3 skilltab` prefixes such as `Malevolent` and `Torrid` at `frequency=1`.

If these remain ordinary non-Greater affixes and overlap with Greater rows, they should probably not stay at `frequency=1`; otherwise they are weighted like early Greater Affixes.

Proposed rule:

- Audit every ordinary `frequency=1` rare-eligible row.
- If it is not intended to be chase-tier, raise it to at least `3`.
- If it is an obsolete or undesirable row, decide whether it should become filler with higher frequency, be banded, or be disabled for rares.

## Revised Implementation Strategy

Do not implement the old 14-row pilot as-is.

New sequence:

1. Audit rare-eligible prefix/suffix rows by family, item type, group, level, maxlevel, and frequency.
2. Pick a small set of high-value affix families for the first banded test:
   - Weapon enhanced damage.
   - Armor/shield enhanced defense.
   - Jewelry all stats.
   - Jewelry all resist.
3. For each family, design normal high-tier band rows and matching Greater band rows.
4. Reweight ordinary `frequency=1` rows that overlap the same item pools.
5. Keep junk/filler rows high enough to dilute early access.
6. Validate probability examples by calculating total eligible weight at sample item levels.
7. Only then edit `magicprefix.txt` / `magicsuffix.txt`.

## Validation Targets For First Implementation

For sample item levels 55, 70, and 85, calculate:

- Total eligible prefix/suffix weight for representative item types.
- Normal top affix weight.
- Greater affix weight.
- Greater affix chance relative to the normal family row.
- Greater affix chance relative to the total eligible pool.

Representative item types:

- Rare weapon.
- Rare body armor.
- Rare shield.
- Rare ring.
- Rare amulet.

The first implementation should include a generated probability report before live publish.
