# Rare Item Rework Design

Created: 2026-05-18.

Goal: make rare items appear less often, but make the rares that do drop more exciting. The design should primarily reward elite base rares, affect exceptional base rares to a lesser degree, and leave normal base rares mostly unchanged.

Reference context: the D2R Data Guide is useful for the overall loose-file modding workflow and reinforces the current `-mod XavReimagined -txt` style workflow: https://eezstreet.github.io/d2rdoc/guides/getting-started.html

## Current Data Constraints

- Global rare quality odds are controlled by `data/global/excel/itemratio.txt` and its base copy.
- `itemratio.txt` has rows for `Version`, `Uber`, and `Class Specific`. It does not have a separate `Ultra` / elite row.
- In the item base tables, `weapons.txt` and `armor.txt` distinguish base tiers with `normcode`, `ubercode`, and `ultracode`.
- Because `itemratio.txt` only has `Uber=0` and `Uber=1`, the exposed quality-ratio table can cleanly distinguish normal bases from non-normal bases, but not exceptional from elite.
- Current spawnable base counts:
  - Weapons: 103 normal, 97 exceptional, 97 elite.
  - Armor: 73 normal, 72 exceptional, 72 elite.
- Current spawnable base level ranges:
  - Normal weapons: level 1-34, average 15.6.
  - Exceptional weapons: level 28-55, average 40.8.
  - Elite weapons: level 52-86, average 71.4.
  - Normal armor: level 1-52, average 15.8.
  - Exceptional armor: level 24-70, average 44.6.
  - Elite armor: level 54-85, average 72.9.
- Rare affix count appears engine-side rather than TXT-side. Treat the rare cap as 6 affix records: up to 3 prefixes and 3 suffixes.
- Each affix row can carry up to 3 stat mods through `mod1`, `mod2`, and `mod3`, so rare power can be increased without changing the 6-affix cap.

## Current Rare Quality Values

Current active/base `itemratio.txt` values:

| Row | Rare | RareDivisor | RareMin |
|---|---:|---:|---:|
| Classic normal non-class | 160 | 3 | 3200 |
| Classic exceptional/elite non-class | 96 | 3 | 3200 |
| Expansion normal non-class | 100 | 2 | 3200 |
| Expansion exceptional/elite non-class | 100 | 2 | 3200 |
| Expansion normal class-specific | 80 | 3 | 3200 |
| Expansion exceptional/elite class-specific | 80 | 3 | 3200 |

Higher `Rare` and `RareMin` values make rare quality harder to roll.

## Recommended Rarity Pass

Do not change the `Uber=0` rows. This leaves normal base rare rates unchanged.

Change only the `Uber=1` rows. This affects exceptional and elite together, which is the closest clean TXT-level approximation for "elite primarily, exceptional somewhat."

Recommended first implementation:

| Row | Current Rare | Proposed Rare | Current RareMin | Proposed RareMin | Effective Intent |
|---|---:|---:|---:|---:|---|
| Classic exceptional/elite non-class | 96 | 240 | 3200 | 8000 | 2.5x rarer |
| Expansion exceptional/elite non-class | 100 | 250 | 3200 | 8000 | 2.5x rarer |
| Expansion exceptional/elite class-specific | 80 | 200 | 3200 | 8000 | 2.5x rarer |

Alternative if we want the full headline number immediately:

| Row | Current Rare | Full 3x Rare | Current RareMin | Full 3x RareMin |
|---|---:|---:|---:|---:|
| Classic exceptional/elite non-class | 96 | 288 | 3200 | 9600 |
| Expansion exceptional/elite non-class | 100 | 300 | 3200 | 9600 |
| Expansion exceptional/elite class-specific | 80 | 240 | 3200 | 9600 |

Recommendation: start at 2.5x for the shared exceptional/elite quality roll, then make elite rares feel substantially better through affix availability. If elite rares still feel too common after testing, move to the full 3x values.

## Affix Pool Strategy

Rare affix quality is controlled by `magicprefix.txt` and `magicsuffix.txt`.

Important columns:

- `spawnable`: whether the affix can appear in the general magic affix pool.
- `rare`: whether the affix can appear on rares.
- `level`: affix level gate.
- `levelreq`: item requirement impact.
- `frequency`: weighted likelihood once the affix is eligible.
- `group`: mutual-exclusion family. Affixes in the same group cannot stack together on the same item.
- `itype*` / `etype*`: included and excluded item types.
- `mod1*`, `mod2*`, `mod3*`: stat payload.

Current rare-eligible affix counts:

| File | Rare-eligible | Rare-only (`spawnable=0`, `rare=1`) |
|---|---:|---:|
| `magicprefix.txt` | 918 | 38 |
| `magicsuffix.txt` | 726 | 57 |

This means the existing mod already uses rare-only affixes. Greater Affixes should follow that pattern.

## Greater Affixes

Greater Affixes should be rare-only affix rows:

- `spawnable=0`
- `rare=1`
- `frequency=1` for the strongest versions, occasionally `2` or `3` for softer versions
- same `group` as the normal affix family they upgrade
- `level` usually 75, 82, or 90 depending on power
- `levelreq` should be high enough to avoid low-level twinking abuse
- same `itype*` / `etype*` as the source affix unless intentionally narrowed

Using the same `group` is important. A Greater enhanced-damage prefix should replace a normal enhanced-damage prefix in that roll family, not stack with it.

Greater Affixes will not automatically show a special "Greater Affix" label in game. Rare item names do not visibly expose magic affix row names the way blue magic items do. The player-facing signal is the stronger stat line itself unless we later add a separate UI/string convention.

## Early Access Top Affixes

To make top affixes possible on lower-level items, add rare-only early-access variants:

- Copy selected high-tier affix rows.
- Lower `level` enough that exceptional or early elite bases can roll them.
- Keep `frequency=1`.
- Keep `levelreq` close to the original top affix, or only modestly reduce it.
- Keep the same `group`.

This makes the affix possible without making it common.

Example policy:

| Variant Type | Affix Level | Frequency | Purpose |
|---|---:|---:|---|
| Early access top affix | 55-65 | 1 | Exceptional and early elite can very rarely spike |
| Elite Greater Affix | 75-84 | 1-2 | Most elite bases can access it |
| Apex Greater Affix | 90+ | 1 | Very high item-level chase affixes |

## Pilot Scope

Do not rewrite hundreds of affixes in the first pass. Start with a controlled pilot:

- 8 weapon prefix upgrades.
- 6 weapon suffix upgrades.
- 8 armor/shield prefix upgrades.
- 6 armor/shield suffix upgrades.
- 8 jewelry upgrades.
- 6 class-item upgrades.

Suggested categories:

- Weapons: enhanced damage, attack rating, IAS, deadly strike, elemental damage, magic damage, leech.
- Armor/shields: defense, block, faster hit recovery, resistances, damage reduction, life.
- Jewelry: skills, faster cast, leech, resistances, magic find, all stats.
- Class items: class skills, skill tabs, pierce/extra elemental packages, class-themed sustain.

Avoid sockets in the first Greater Affix pilot. Socket affixes have very high build value and can overwhelm item identity quickly.

## Implementation Steps

1. Update both `itemratio.txt` copies with the chosen `Uber=1` rare rarity multiplier.
2. Add new rare-only Greater Affix rows to both `magicprefix.txt` copies.
3. Add new rare-only Greater Affix rows to both `magicsuffix.txt` copies.
4. Keep active and base copies identical.
5. Validate TSV column counts.
6. Validate every new affix uses an existing property code.
7. Validate every Greater Affix has `spawnable=0`, `rare=1`, non-empty `group`, and non-zero `frequency`.
8. Validate no Greater Affix uses a group that allows unintended stacking with its normal family.
9. Install to live with `scripts/install-local.ps1`.
10. Test in game with high-level rare drops and cube rare-reroll recipes.

## Testing Notes

The in-game test should focus on:

- Normal bases still producing ordinary rares at roughly previous rates.
- Exceptional rares dropping less often but not vanishing.
- Elite rares feeling meaningfully rarer.
- Elite rare affixes noticeably improving.
- Greater Affixes appearing rarely enough that they feel special.
- No low-level item becoming absurd because an early-access top affix has too low a `levelreq`.

## Open Design Choice

Choose the first rarity multiplier before implementation:

- Safer start: 2.5x rarer for `Uber=1` rows.
- Stronger start: 3x rarer for `Uber=1` rows.

Because `itemratio.txt` cannot split exceptional from elite, the safer start is recommended unless testing shows elite rares are still too common.
