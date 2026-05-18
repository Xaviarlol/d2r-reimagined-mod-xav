# Rare Item Rework Design

Created: 2026-05-18.

Goal: make rare items appear less often, but make the rares that do drop more exciting. The design should primarily reward elite base rares, affect exceptional base rares to a lesser degree, and leave normal base rares mostly unchanged.

Reference context: the D2R Data Guide is useful for the overall loose-file modding workflow and reinforces the current `-mod XavReimagined -txt` style workflow: https://eezstreet.github.io/d2rdoc/guides/getting-started.html

Full local reading notes from the D2RDoc sitemap crawl: `docs/d2rdoc-reading-notes-2026-05-18.md`.

Greater Affix and frequency rework proposal: `docs/rare-greater-affix-pilot-2026-05-18.md`.

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
- D2RDoc's item-ratio calculation confirms the quality values are divisors. Higher `Rare` / `RareMin` values make rare quality harder to roll, and `RareMin` is especially important in high-MF/high-level cases because it caps how favorable the final divisor can become.

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

Implementation status:

- 2026-05-18: Applied the safer 2.5x rarity pass to both active and base `itemratio.txt`.
- Changed only the three `Uber=1` rows.
- Normal-base rare rows remain unchanged.
- `RareMin` was raised from `3200` to `8000` on the changed rows so high-MF/high-level cases are capped consistently with the new rarity target.
- Greater Affix rows are not implemented yet.

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

## Greater Affixes And Frequency Rework

Greater Affixes should be rare-only affix rows:

- `spawnable=0`
- `rare=1`
- low relative `frequency`
- same `group` as the normal affix family they upgrade
- `level` usually 75, 82, or 90 depending on power
- `levelreq` should be high enough to avoid low-level twinking abuse
- same `itype*` / `etype*` as the source affix unless intentionally narrowed

Using the same `group` is important. A Greater enhanced-damage prefix should replace a normal enhanced-damage prefix in that roll family, not stack with it.

Greater Affixes will not automatically show a special "Greater Affix" label in game. Rare item names do not visibly expose magic affix row names the way blue magic items do. The player-facing signal is the stronger stat line itself unless we later add a separate UI/string convention.

Frequency is a weight, not an inverse-rarity value. Higher `frequency` means the affix appears more often once eligible. Greater Affixes should feel rare because their own weights are low and the ordinary/filler affix pool has enough weight to dilute them.

Corrected implementation model:

- There should be one player-facing Greater Affix per category, such as `Greater Cruel`.
- That one category may be represented by multiple technical rows with the same effect and same group.
- Example Greater banding: level `50-65` frequency `1`, level `66-80` frequency `2`, level `81+` frequency `3`.
- If late Greater is intended to be about 10x rarer than the normal version, the normal version's late frequency should be about 10x the late Greater frequency.
- Therefore, with late Greater frequency `3`, the matching normal affix should be around `30` frequency for that comparison.

Not every existing `frequency=1` row should be treated as a chase affix. Some old proc/charge/utility rows may simply be low-priority legacy rows. The pilot should audit each target family rather than assuming the current frequency layout already expresses item power cleanly.

This is now a broader affix-frequency rework, not only a Greater Affix insertion pass:

- Current high-frequency top rows, such as `Cruel` at `frequency=114`, may need normalization if Greater rows use `1 / 2 / 3` and the target late ratio is 10x.
- Current ordinary `frequency=1` rows likely need to be raised if they are not meant to be chase-tier.
- Junk/filler rows should remain high or be increased where needed to dilute powerful lower-level access.

## Early Access Top Affixes

To make top affixes possible on lower-level items, add banded technical rows for important normal and Greater affix families:

- Copy selected high-tier affix rows.
- Lower `level` enough that exceptional or early elite bases can roll them.
- Use lower frequency in early bands and higher frequency in later bands.
- Keep `levelreq` close to the original top affix, or only modestly reduce it.
- Keep the same `group`.
- Use `maxlevel` where useful to create clean early/main/apex bands.

This makes the affix possible without making it common.

Example policy:

| Variant Type | level | maxlevel | Frequency | Purpose |
|---|---:|---:|---:|---|
| Early normal top affix | 50-65 | 65 | 10 | Strong affix can appear early, but is uncommon |
| Mid normal top affix | 66-80 | 80 | 20 | Strong affix becomes more likely |
| Late normal top affix | 81+ | blank | 30 | Strong affix reaches intended top-end rate |
| Early Greater affix | 50-65 | 65 | 1 | Very rare early spike |
| Mid Greater affix | 66-80 | 80 | 2 | Still rare, but less punishing |
| Late Greater affix | 81+ | blank | 3 | About 10x rarer than late normal if normal is 30 |

This lets an exciting affix drop earlier without letting a low-level character immediately equip a wildly overpowered item.

There are two complementary ways to make early high-tier affixes rare:

1. Explicit banded rows as above. This is easier to reason about and should be used for premium families.
2. Pool shaping: make the lower-level eligible affix pool larger with more ordinary/junk weight, then reduce that junk on higher-level rares with `maxlevel`. This helps tune total odds but is harder to reason about because every item type has a different eligible pool.

## Pilot Scope

Do not implement the old simple Greater-only pilot. The first implementation should be a controlled banding and frequency test:

- Weapon enhanced damage: `Cruel` and `Greater Cruel`.
- Armor/shield enhanced defense: `Godly` and `Greater Godly`.
- Jewelry all stats: `of the Zodiac` and `Greater Zodiac`.
- Jewelry all resist: `Chromatic` / ring equivalent and Greater variants.

For each family, design both:

- Normal high-tier early/mid/late technical rows.
- Greater early/mid/late technical rows.

Avoid sockets in the first Greater Affix pilot. Socket affixes have very high build value and can overwhelm item identity quickly.

The detailed proposal and before/after examples are documented separately in `docs/rare-greater-affix-pilot-2026-05-18.md`.

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
