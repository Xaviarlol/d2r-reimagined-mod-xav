# Rare Item Rework Design

Created: 2026-05-18.

Status: canonical design document. This file replaces the separate Greater Affix pilot document; the rare item work is one two-phase rework.

Goal: make rare items appear less often, but make the rares that do drop more exciting. The design should primarily reward elite base rares, affect exceptional base rares to a lesser degree, and leave normal base rares mostly unchanged.

Reference context:

- D2R Data Guide: https://eezstreet.github.io/d2rdoc/guides/getting-started.html
- Full local D2RDoc crawl notes: `docs/d2rdoc-reading-notes-2026-05-18.md`

## Current Implementation Status

- 2026-05-18: Applied the safer 2.5x rarity pass to both active and base `itemratio.txt`.
- Changed only the three `Uber=1` rare rows.
- Normal-base rare rows remain unchanged.
- `RareMin` was raised from `3200` to `8000` on the changed rows so high-MF/high-level cases are capped consistently with the new rarity target.
- Greater Affix marker plumbing exists:
  - `item_greaterAffixMarker` in `itemstatcost.txt`
  - `greater-affix-marker` in `properties.txt`
  - `GreaterAffixMarker` in `item-modifiers.json`
- Phase 1 affix level compression is not implemented yet.
- Phase 2 Greater Affix rows are not implemented yet.
- 2026-05-19: Added a full generated apex audit and draft Greater Affix chance report: `docs/rare-greater-affix-apex-audit-2026-05-19.md`.

## Current Data Constraints

- Global rare quality odds are controlled by `data/global/excel/itemratio.txt` and its base copy.
- `itemratio.txt` has rows for `Version`, `Uber`, and `Class Specific`. It does not have a separate `Ultra` / elite row.
- In the item base tables, `weapons.txt` and `armor.txt` distinguish base tiers with `normcode`, `ubercode`, and `ultracode`.
- Because `itemratio.txt` only has `Uber=0` and `Uber=1`, the exposed quality-ratio table can cleanly distinguish normal bases from non-normal bases, but not exceptional from elite.
- Rare affix count appears engine-side rather than TXT-side. Treat the rare cap as 6 affix records: up to 3 prefixes and 3 suffixes.
- Each affix row can carry up to 3 stat mods through `mod1`, `mod2`, and `mod3`, so rare power can be increased without changing the 6-affix cap.
- `magicprefix.txt` and `magicsuffix.txt` affix rows can be shared by magic and rare items. It is acceptable for Phase 1 to affect magic items too, so direct edits to shared `spawnable=1, rare=1` rows are allowed.

## Rare Quality Pass

Current active/base `itemratio.txt` values before the rarity pass:

| Row | Rare | RareDivisor | RareMin |
|---|---:|---:|---:|
| Classic normal non-class | 160 | 3 | 3200 |
| Classic exceptional/elite non-class | 96 | 3 | 3200 |
| Expansion normal non-class | 100 | 2 | 3200 |
| Expansion exceptional/elite non-class | 100 | 2 | 3200 |
| Expansion normal class-specific | 80 | 3 | 3200 |
| Expansion exceptional/elite class-specific | 80 | 3 | 3200 |

Implemented safer pass:

| Row | Current Rare | Implemented Rare | Current RareMin | Implemented RareMin | Intent |
|---|---:|---:|---:|---:|---|
| Classic exceptional/elite non-class | 96 | 240 | 3200 | 8000 | 2.5x rarer |
| Expansion exceptional/elite non-class | 100 | 250 | 3200 | 8000 | 2.5x rarer |
| Expansion exceptional/elite class-specific | 80 | 200 | 3200 | 8000 | 2.5x rarer |

Alternative if testing shows elite/exceptional rares are still too common:

| Row | Current Rare | Full 3x Rare | Current RareMin | Full 3x RareMin |
|---|---:|---:|---:|---:|
| Classic exceptional/elite non-class | 96 | 288 | 3200 | 9600 |
| Expansion exceptional/elite non-class | 100 | 300 | 3200 | 9600 |
| Expansion exceptional/elite class-specific | 80 | 240 | 3200 | 9600 |

## Rare Affix Mechanics

Rare affix quality is controlled by `magicprefix.txt` and `magicsuffix.txt`.

Important columns:

- `spawnable`: whether the affix can appear in the general magic affix pool.
- `rare`: whether the affix can appear on rares.
- `level`: minimum affix level gate.
- `maxlevel`: maximum affix level gate; useful for non-overlapping bands. Existing rows keep their original `maxlevel` in Phase 1 so weaker affixes do not expire earlier.
- `levelreq`: item equip requirement impact, not roll chance.
- `frequency`: weighted likelihood once the affix is eligible.
- `group`: mutual-exclusion family. Affixes in the same group cannot stack together on the same item.
- `itype*` / `etype*`: included and excluded item types.
- `mod1*`, `mod2*`, `mod3*`: stat payload.

Frequency is a weight, not an inverse-rarity value. Higher frequency means more common among eligible affixes.

Current rare-eligible affix counts:

| File | Rare-eligible | Rare-only (`spawnable=0`, `rare=1`) |
|---|---:|---:|
| `magicprefix.txt` | 918 | 38 |
| `magicsuffix.txt` | 726 | 57 |

## Two-Phase Rework

### Phase 1: Proportional Rare Affix Level Compression

Phase 1 lowers the effective level gate of all rare-eligible affixes, not just the best affixes. The goal is to let lower-level rare items roll a broader, more exciting affix pool while preserving the internal order of each affix family.

Use a consistent compression formula:

```text
compressed_level = max(1, round_half_up(original_level * 0.70))
```

Use round-half-up for all compression math:

```text
round_half_up(x) = floor(x + 0.5)
```

Existing rows keep their original `maxlevel`:

```text
phase1_maxlevel = original_maxlevel
```

If the original `maxlevel` is blank, leave it blank. This avoids making high-level rares cleaner by prematurely removing weaker affixes from the eligible pool.

Lower affix equip requirements by 15% at the same time:

```text
compressed_levelreq = max(1, round_half_up(original_levelreq * 0.85))
```

If the original `levelreq` is blank or `0`, leave it blank or `0`.

Important proportionality rules:

- Apply the same formula to the whole rare-eligible affix ladder.
- Do not lower only the best affix while leaving the second-best affix above it.
- Within each family, stronger affixes must remain at the same or higher level than weaker affixes.
- If compression collapses two adjacent tiers to the same level and that creates confusion, nudge the stronger tier up by 1 level.
- Apply the 15% `levelreq` reduction broadly so earlier affix access does not feel artificially locked behind the old requirements.
- Keep `levelreq` proportional too. Stronger affixes should generally still require the same or higher character level than weaker affixes in the same family.
- Directly edit shared affix rows unless there is a specific reason to create rare-only rows. Magic items can participate in the same earlier-affix progression.
- Do not directly scale rows that are shared across unrelated item families when the change is meant to affect only one family. The important known exception is charm frequency scaling for group `307`.

### Phase 1 Top-Affix Split

Only the top normal affix in each target family gets an early/late frequency split.

Top-affix split rule:

```text
top_early_level = compressed_level(original_top_level)
top_early_maxlevel = original_top_level - 1
top_early_frequency = max(1, round_half_up(original_top_frequency / 2))
top_late_level = original_top_level
top_late_maxlevel = blank or original
top_late_frequency = original_top_frequency
```

This means:

- Lower and mid affixes move down proportionally.
- The best affix can appear earlier, but is 2x rarer before the old gate.
- High-level rares do not get an extra chance to roll the best affix because the early row expires before the late row starts.

Example: current weapon enhanced-damage rows include `Cruel 234-266%` at level 69 and `Cruel 267-300%` at level 74. After compression, the lower Cruel row moves to level 48, while the top Cruel early row starts at level 52. The lower affix remains lower level than the stronger affix.

### Phase 2: Greater Affixes

Phase 2 adds Greater Affixes to each target affix family as a separate chase layer.

Greater Affix policy:

- One player-facing Greater category per family, such as `Greater Grandmaster's`.
- Implemented as multiple technical rows with the same name idea, same stat payload, and same `group`.
- Rare-only: `spawnable=0`, `rare=1`.
- Same `group` as the normal family so Greater replaces normal, not stacks with normal.
- Default frequencies: early/mid/late = `1 / 2 / 3`.
- Default Greater bands are design targets, not hard rules; adjust by family if the compressed ladder suggests better gates.
- Greater stat ranges should be narrow chase rolls with a high floor.
- Benchmark every Greater family against the strongest existing row in that `group`, not merely the familiar vanilla-style top row. If a modded apex row exists, such as `Grandmaster's` in weapon damage group `111` or `Invulnerable1` in defense group `101`, the Greater row must clearly beat that apex.
- Add `greater-affix-marker` when the row has a spare mod slot.

Default Greater band shape:

| Technical Band | level | maxlevel | frequency |
|---|---:|---:|---:|
| Early | 50 | 65 | 1 |
| Mid | 66 | 80 | 2 |
| Late | 81 | blank | 3 |

Greater marker:

```text
modXcode = greater-affix-marker
modXmin = 1
modXmax = 1
```

This prints an orange/gold tooltip line using D2R color controls:

```text
** Greater Affix
```

Because each affix row only has `mod1`, `mod2`, and `mod3`, the marker is safest for Greater rows with no more than two real stat mods. Rows that already need all three real mod slots need either a combined property or no marker.

### Candidate Greater Affix Families

These are candidates, not implementation promises. The proposed Greater ranges are intentionally tighter than the first draft so a Greater roll feels consistently premium. The "Current Apex Row" column is the row a Greater candidate must beat.

| Candidate | Current Apex Row | Current Apex Range | Proposed Greater Range | Item Scope | Priority / Notes |
|---|---|---|---|---|---|
| Greater Grandmaster's | `Grandmaster's` / `Wraithly1` | `dmg% 301-350` plus AR/Deadly/Crushing/Open Wounds; Wraithly has ethereal+self-repair with `dmg% 176-200` | `dmg% 451-500` plus a stronger AR/Deadly/Crushing/Open Wounds rider | Weapons, excluding orbs/wands | High. Primary physical rare chase prefix. This is a true Greater version of Grandmaster's, not a plain ED-only row. |
| Greater Godly | `Godly` / `Invulnerable1` / armor `Wraithly1` | `ac% 201-225`; `Invulnerable1` has `ac% 81-100` plus `red-dmg% 21-25`; Wraithly has ethereal+self-repair with `ac% 81-100` | `ac% 250-300`, `red-dmg% 26-30` | Armor, shields | High. Must beat both raw defense and DR% apex rows in group `101`. Uses two real mods plus marker. |
| Greater Zodiac | `of the Zodiac` | `all-stats 21-30` | `all-stats 38-45` | Amulets, rings, circlets, caster weapons | High. Broad build-enabler suffix. |
| Greater Chromatic | `Chromatic` | `res-all 21-30` | `res-all 36-40` | Shields, amulets, circlets | High. Defensive all-res chase. |
| Greater Scintillating | `Scintillating` | `res-all 13-17` | `res-all 22-25` | Rings | High. Separate ring tuning because the base row is lower. |
| Greater Antimagic | `Antimagic` / `of Negation` | `res-mag 16-20` prefix; `res-mag 14-20` suffix | `res-mag 24-30` | Shields, torso, circlets, rods/orbs where eligible | Medium-high. Missed apex family for magic resistance; prefix and suffix rows need separate group-safe implementation. |
| Greater Evisceration | `of Evisceration` | `dmg-max 101-120` | `dmg-max 150-165` | Weapons | High. Flat damage weapon suffix. |
| Greater Transcendence | `of Transcendence` | `dmg-min 50-60` | `dmg-min 75-85` | Weapons | Medium-high. Strong but less broadly visible than max damage. |
| Greater Lich | `of the Lich` | `manasteal 8-9`, `lifesteal 10-12` | `manasteal 10-12`, `lifesteal 13-15` | Rings, amulets | High. Premium sustain roll. |
| Greater Four Seasons | `of the Four Seasons` | `res-all-max 4-6` | `res-all-max 7-8` | Armor, shields, rings, amulets | High impact. Keep very rare or defer until defensive balance pass. |
| Greater Coalescence | Fire/Lightning/Cold Coalescence | `abs-fire%` / `abs-ltng%` / `abs-cold% 16-25` | matching absorb `28-35` | Weapons, amulets, rings, shields | Medium-high. Missed apex absorb family; one element per row, same group `3`. |
| Greater Elemental Mastery | `Pyromaniac's` / `Frost Wyrm's` / `Zeus's` / `Manticore's` damage rows | `extra-* 10-12` | `extra-* 14-16` | Wands, orbs, staves | Medium. Caster damage chase, one element per row. |
| Greater Elemental Pierce | Elemental pierce rows | `pierce-* 10-12` | `pierce-* 14-16` | Wands, orbs, staves | Medium. Stronger than sheet damage suggests, tune carefully. |
| Greater Quickness | `of Quickness` | `swing3 40` | `swing3 50` | Melee weapons | Medium. Breakpoint-sensitive. |
| Greater Magus | `of the Magus` | `cast3 20` | `cast3 25` | Rods, orbs, circlets | Medium. Breakpoint-sensitive. |
| Greater Omniscient | `Omniscient` / `Sage's` | `allskills 2` on torso/amulet; `allskills 1` on ring | `allskills 3` for torso/amulet, `allskills 2` for ring | Torso, amulets, rings | High impact. Needs separate scope rows so rings do not jump to torso/amulet power. |
| Greater Skilltab | top `+3 skilltab` rows | `skilltab +3` | `skilltab +4` | Class-appropriate skilltab item scopes | High impact. Must share group `125` with normal skilltab rows. |
| Greater Gnostic | top `skill-rand` rows | random class skill `+5` | random class skill `+6` | Rings, amulets, circlets, belts | Very high variance. Include in skill-affix pass, not broad numeric pass. |
| Greater Perfection | `of Perfection` | `dex 20-30` | `dex 36-40` | Body armor, boots | Medium. Good for attack rating, block, and dex builds. |
| Greater Titan | `of the Titan` | `str 16-20` | `str 26-30` | Rings, scepters, maces, body armor | Medium. Requirement and damage utility. |
| Greater Deflecting | `of Deflecting` | `block 20-30`, `block2 30` | `block 35-40`, `block2 40` | Shields | Medium. Defensive build-defining suffix. |
| Greater Fatal | `Fatal` | `deadly 16-20` | `deadly 24-30` | Gloves | Medium. Melee damage chase. |
| Greater Crushing | `Crushing` | `crush 16-20` | `crush 24-30` | Gloves | Medium. Boss-kill power, tune carefully. |
| Greater Prosperity | `of Prosperity` | `mag% 16-20` | `mag% 26-30` | Jewels | Low-medium. Utility chase rather than combat power. |
| Greater Inertia | `of Inertia` | `move3 10` | `move3 13-15` | Large charms | Optional. Include only if rare charms are in scope. |
| Greater Balance | `of Balance` | `balance3 10` | `balance3 13-15` | Large charms | Optional. Include only if rare charms are in scope. |

Likely defer or skip for the first Greater pass:

- Binary effects such as `nofreeze`, `ignore-ac`, and knockback. They do not gain much from a Greater range.
- Socket affixes such as `Jeweler's`. Extra sockets can dominate item identity and should be evaluated separately.
- Skill affixes should be implemented in a dedicated skill-affix pass, even though they are now included as candidates above. `+6` random skill rows may be too swingy without separate probability review.
- Existing rare-only pierce rows in group `307`. They are already special-purpose rare rows and should not be mixed into the first broad Greater pass.

### Charm Frequency Normalization Proposal

Charms need a separate frequency-normalization rule because large charm `+1 skill tree` affixes currently have low raw frequencies. The target is:

- Normal large charm `+1 skill tree`: `frequency = 10`.
- Greater large charm `+2 skill tree`: `frequency = 1`.
- All existing charm-affix proportions should otherwise stay the same.
- All charm affix levels follow the same 30% level reduction used by the rest of Phase 1.

Current large charm skill rows:

| Row Type | Current Level | Current Level Req | Current Freq | Phase 1 Level | Phase 1 Level Req | Proposed Freq |
|---|---:|---:|---:|---:|---:|---:|
| Original class `+1 skill tree` rows | 50 | 42 | 2 | 35 | 36 | 10 |
| Warlock `+1 skill tree` rows | 50 | 42 | 1 | 35 | 36 | 10 |
| New Greater `+2 skill tree` rows | new row | new row | new | 57 | 64 | 1 |

Base scaling rule for existing charm rows:

```text
scaled_charm_frequency = current_frequency * 5
```

Scope rules:

- Apply this only to charm-exclusive rows, and only where the charm pool is being given new Greater rows or needs the `+1` skill-tree normalization.
- Prefix scaling is required for large charm skill-tree prefixes because normal `+1 skill tree` rows move to `frequency=10` and new Greater `+2 skill tree` rows enter at `frequency=1`.
- Suffix scaling is only required if Greater charm suffix rows such as `Greater Inertia` or `Greater Balance` are implemented. If no Greater charm suffix rows are added, suffix scaling is a mathematical no-op inside the suffix pool and can be skipped.
- Exempt all group `307` pierce rows from this scaling. Group `307` is implemented with mixed item-type rows such as `ring,mcha` and `amul,glov,boot,belt,helm,lcha`; scaling those rows in place would also multiply pierce odds on rings, amulets, gloves, boots, belts, and helms. If charm pierce ever needs proportional scaling, first split those rows into charm-only and non-charm-only copies.

The planned Warlock exception is deliberate: Warlock `+1 skill tree` large charm rows currently have `frequency=1`, but should be raised to `10` so all normal `+1 skill tree` charm rows share one consistent rarity. This intentionally changes the old Warlock-vs-original-class ratio rather than preserving it.

New Greater `+2 skill tree` large charm rows should be authored directly as `level=57`, `levelreq=64`, `frequency=1`, `spawnable=0`, `rare=1`, and `group=125`. The shared `group=125` prevents a charm from rolling both the normal `+1` and Greater `+2` skill-tree prefix in separate prefix slots.

Example: level 90 large charm prefix pool before Greater rows:

| Pool | Eligible Rows | Current Total Frequency | Current Skill Frequency | Current Skill Share |
|---|---:|---:|---:|---:|
| `lcha` prefixes at level 90 | 65 | 279 | 45 | 16.13% |

After normalization and adding one Greater row per skill tree:

| Pool | Existing Scaled Total | Normal Skill Frequency | Greater Skill Frequency | Total With Greater | Normal Skill Share | Greater Skill Share |
|---|---:|---:|---:|---:|---:|---:|
| `lcha` prefixes at level 90 | 1410 | 240 | 24 | 1434 | 16.74% | 1.67% |

This preserves the old large-charm affix feel while making Greater skill charms exactly 10x rarer than normal skill charms inside the skill-tree charm slice.

Representative charm frequency conversions for non-`307`, charm-exclusive rows:

| Current Freq | Scaled Existing Freq |
|---:|---:|
| 1 | 5 |
| 2 | 10 |
| 3 | 15 |
| 4 | 20 |
| 5 | 25 |
| 6 | 30 |
| 8 | 40 |
| 10 | 50 |
| 12 | 60 |
| 20 | 100 |
| 24 | 120 |

## Phase 1 Examples

These examples show the intended proportional level compression plus top-row split. They are design examples, not implemented data.

### Weapon Enhanced Damage

| Affix Row | Stats | Current Level | Current Freq | Phase 1 Effective Rare Availability |
|---|---|---:|---:|---|
| Cruel lower top row | `dmg% 234-266` | 69 / req 63 | 114 | level `48`, req `54`, freq `114` |
| Cruel true top row, early | `dmg% 267-300` | 74 / req 69 | 114 | level `52`, req `59`, maxlevel `73`, freq `57` |
| Cruel true top row, late | `dmg% 267-300` | 74 / req 69 | 114 | level `74`, req `59`, freq `114` |

### Armor / Shield Enhanced Defense

| Affix Row | Stats | Current Level | Current Freq | Phase 1 Effective Rare Availability |
|---|---|---:|---:|---|
| Godly lower top row | `ac% 167-200` | 79 / req 74 | 110 | level `55`, req `63`, freq `110` |
| Godly true top row, early | `ac% 201-225` | 86 / req 75 | 110 | level `60`, req `64`, maxlevel `85`, freq `55` |
| Godly true top row, late | `ac% 201-225` | 86 / req 75 | 110 | level `86`, req `64`, freq `110` |

### Jewelry / Caster All Attributes

| Affix Row | Stats | Current Level | Current Freq | Phase 1 Effective Rare Availability |
|---|---|---:|---:|---|
| of the Sky | `all-stats 5-10` | 20 / req 18 | 12 | level `14`, req `15`, freq `12` |
| of the Stars | `all-stats 11-15` | 44 / req 40 | 12 | level `31`, req `34`, freq `12` |
| of the Heavens | `all-stats 16-20` | 69 / req 64 | 12 | level `48`, req `54`, freq `12` |
| of the Zodiac, early | `all-stats 21-30` | 86 / req 83 | 12 | level `60`, req `71`, maxlevel `85`, freq `6` |
| of the Zodiac, late | `all-stats 21-30` | 86 / req 83 | 12 | level `86`, req `71`, freq `12` |

### Shield All Resist

| Affix Row | Stats | Current Level | Current Freq | Phase 1 Effective Rare Availability |
|---|---|---:|---:|---|
| Rainbow | `res-all 8-11` | 18 / req 13 | 10 | level `13`, req `11`, freq `10` |
| Scintillating | `res-all 12-15` | 28 / req 21 | 10 | level `20`, req `18`, freq `10` |
| Prismatic | `res-all 16-20` | 39 / req 31 | 8 | level `27`, req `26`, freq `8` |
| Chromatic, early | `res-all 21-30` | 50 / req 42 | 8 | level `35`, req `36`, maxlevel `49`, freq `4` |
| Chromatic, late | `res-all 21-30` | 50 / req 42 | 8 | level `50`, req `36`, freq `8` |

### Ring All Resist

| Affix Row | Stats | Current Level | Current Freq | Phase 1 Effective Rare Availability |
|---|---|---:|---:|---|
| Shimmering | `res-all 5-8` | 45 / req 37 | 6 | level `32`, req `31`, freq `6` |
| Rainbow | `res-all 9-12` | 56 / req 48 | 4 | level `39`, req `41`, freq `4` |
| Scintillating, early | `res-all 13-17` | 67 / req 59 | 4 | level `47`, req `50`, maxlevel `66`, freq `2` |
| Scintillating, late | `res-all 13-17` | 67 / req 59 | 4 | level `67`, req `50`, freq `4` |

## Phase 2 Examples

### Greater Frequency And Scope Rule

Greater Affix frequency math is now defined against the current modded apex rows for each item-type scope, not only a single sample item.

- Existing affix frequencies should be scaled across the whole affix file, including `rare=0` magic-only rows. Scaling only `rare=1` rows would preserve rare odds but distort magic-item affix odds.
- For each Greater family, the total Greater frequency eligible for a given item type should equal the current apex frequency for that same item type before the `x10` scale. After all existing rows are scaled by `10`, the Greater family is therefore exactly `10x` rarer than its apex for that item type.
- Broad families must be split by scope and element as needed. One technical row cannot always be exactly `10x` on every item type; leech rows are the clearest example because rings, amulets, circlets, gloves, and weapons have different apex weights.
- The generated audit now writes `docs/rare-greater-affix-scope-validation-2026-05-19.tsv`; implementation is not ready unless every candidate/item-type row in that file shows `greater_vs_apex_after = 10`.
- The `Greater if 3 same-side slots` column is an approximation for comparison, not a literal D2 drop-engine probability.

### Greater Grandmaster's

The real apex weapon-damage row is `Grandmaster's`, so the Greater affix should inherit that identity and keep the ED-plus-rider structure instead of being a plain enhanced-damage-only row.

| Affix | level | maxlevel | frequency | Mods |
|---|---:|---:|---:|---|
| Greater Grandmaster's | 50 | 65 | 1 | `att 301-350`, `dmg% 451-500`, `greater-affix-marker` |
| Greater Grandmaster's | 66 | 80 | 1 | `att 301-350`, `dmg% 451-500`, `greater-affix-marker` |
| Greater Grandmaster's | 66 | 80 | 1 | `deadly 31-40`, `dmg% 451-500`, `greater-affix-marker` |
| Greater Grandmaster's | 81 | blank | 1 | `att 301-350`, `dmg% 451-500`, `greater-affix-marker` |
| Greater Grandmaster's | 81 | blank | 1 | `deadly 31-40`, `dmg% 451-500`, `greater-affix-marker` |
| Greater Grandmaster's | 81 | blank | 1 | `crush 31-40`, `dmg% 451-500`, `greater-affix-marker` |
| Greater Grandmaster's | 81 | blank | 1 | `openwounds 100`, `dmg% 451-500`, `greater-affix-marker` |

Target ratio:

- This family is intentionally benchmarked against `Grandmaster's`, not ordinary `Cruel`.
- The staged variant unlock keeps lower-level Greater rolls narrower while letting late rare weapons chase all four Grandmaster-style riders.
- Late total Greater Grandmaster's family frequency is `4`, so the category remains rarer than existing Grandmaster's total frequency `10` while each specific variant stays extremely rare.
- If the normal late row stays very high, such as current Cruel at `114`, then Greater remains much rarer than ordinary Cruel. That may be acceptable, but it should be intentional.

### Greater Zodiac

| Affix | level | maxlevel | frequency | Mods |
|---|---:|---:|---:|---|
| Greater Zodiac | 60 | 70 | 1 | `all-stats 38-45`, `greater-affix-marker` |
| Greater Zodiac | 71 | 85 | 2 | `all-stats 38-45`, `greater-affix-marker` |
| Greater Zodiac | 86 | blank | 3 | `all-stats 38-45`, `greater-affix-marker` |

This family shows why Phase 2 may need frequency normalization. Normal Zodiac is only `frequency=12`, so a late Greater row at `3` is only 4x rarer unless normal Zodiac is raised or Greater Zodiac is lowered.

## Implementation Strategy

1. Review the generated affix-family audit from `magicprefix.txt` and `magicsuffix.txt`: `docs/rare-greater-affix-apex-audit-2026-05-19.md`.
2. For every affix row, calculate compressed `level` and compressed `levelreq`; leave existing `maxlevel` unchanged.
3. Validate that each family remains monotonic: weaker affixes should not require a higher affix level or equip level than stronger affixes.
4. Apply Phase 1 compression directly to shared affix rows; it is acceptable for magic items to move earlier too.
5. Add the top-affix early/late split for each target family.
6. Validate TSV column counts and active/base parity.
7. Generate sample eligible-weight reports for representative item levels and item types.
8. Generate per-item-type Greater scope validation and confirm every candidate is exactly `10x` rarer than its apex within its implemented scope.
9. Publish and test Phase 1.
10. After Phase 1 testing, implement Phase 2 Greater rows with marker lines.
11. Re-run sample probability reports and tune family frequencies if Greater odds are too common or too rare.

## Validation Targets

For sample item levels 35, 50, 65, 80, and 90, calculate:

- Total eligible prefix/suffix weight for representative item types.
- Weight of each target family.
- Weight of the current top affix in that family.
- Whether compressed levels preserved family ordering.
- Whether compressed `levelreq` values preserved family ordering.
- Whether unchanged existing `maxlevel` values keep weaker affixes in the high-level pool as intended.
- Whether the top-affix early row expires before the late row starts.
- Whether high-level rares gained any unintended duplicate chance.

Representative item types:

- Rare weapon.
- Rare body armor.
- Rare shield.
- Rare ring.
- Rare amulet.
- Rare jewel.

## Testing Notes

The in-game test should focus on:

- Normal bases still producing ordinary rares at roughly previous rates.
- Exceptional rares dropping less often but not vanishing.
- Elite rares feeling meaningfully rarer.
- Earlier rares showing broader affix variety.
- Stronger affixes appearing earlier without becoming common.
- Top affix chance at high levels not increasing accidentally.
- Greater Affixes appearing rarely enough that they feel special once Phase 2 is implemented.
- No low-level item becoming absurd because an early-access top affix has too low a `levelreq`.
