# Codex Session Handoff

Created: 2026-05-18.

This handoff captures the current repo state and the design decisions from the latest Codex work so another session can continue without re-discovering the project context.

## Repo State

- Workspace: `C:\Dropbox\AI projects\d2r\d2r-reimagined-fresh`
- Branch: `xav-custom`
- Remote: `origin` / `https://github.com/Xaviarlol/d2r-reimagined-mod-xav.git`
- Current pushed HEAD before this handoff doc: `6a592bdf Add ranges to low-affix set buffs`
- Live mod install target used this session: `E:\Diablo II Resurrected\mods\XavReimagined\XavReimagined.mpq`
- Launch args from install script: `-mod XavReimagined -txt`

Before this handoff doc was created, `git status --short --branch` was clean:

```text
## xav-custom...origin/xav-custom
```

## Recent Commit Trail

Most recent relevant commits:

```text
6a592bdf Add ranges to low-affix set buffs
d0b7ee61 Document rare item rework design
9d6c0d8a Apply approved low-affix set item buffs
7bb2f229 Make set quality as rare as unique
cb99cb8d Add item quality ratio table
b52bfaf6 Propose buffs for low-affix set items
f6d162c3 Add ranked orb downgrade recipes
19546445 Add gamble cube recipes
8c1206ec Move ranked orb stash slots above grid
8ebd5d0a Fix ranked orb UI presentation
c77a78fb Implement ranked conversion assemblage orbs
5fbcc6f4 Close orb rank design review
```

## Live Install Status

The latest data changes from `6a592bdf` were installed to the live `XavReimagined` folder.

Validation performed after install:

- `data/global/excel/setitems.txt` live hash matched repo hash.
- `data/global/excel/base/setitems.txt` live hash matched repo hash.
- The install script copied the changed `setitems.txt` files and reported launch args `-mod XavReimagined -txt`.

## Item Quality Ratio Work

Files added and tracked:

- `data/global/excel/itemratio.txt`
- `data/global/excel/base/itemratio.txt`

Sets were made as rare as uniques in `itemratio.txt`:

- Every `Set` / `SetDivisor` / `SetMin` now mirrors the matching `Unique` / `UniqueDivisor` / `UniqueMin`.
- Before this, uniques were 2x to 3.2x rarer than sets by raw ratio column.
- Main expansion/global rows were 2.5x rarer for uniques than sets.

Important note for future rare-overhaul work:

- `itemratio.txt` `Uber=1` means exceptional or elite for item quality ratio purposes.
- It does not separate exceptional from elite.
- This is confusing because `weapons.txt` / `armor.txt` use `ubercode` for exceptional and `ultracode` for elite.
- Therefore, rarity changes in `itemratio.txt` can cleanly affect normal vs exceptional+elite, but not elite-only.

## Set Item Buff Pass

Design/proposal doc:

- `docs/set-item-low-affix-buff-proposals-2026-05-17.md`

Implementation:

- Applied approved low-affix set item buffs to 93 items.
- Updated both:
  - `data/global/excel/setitems.txt`
  - `data/global/excel/base/setitems.txt`
- Repaired malformed `Mystic Blades` item-property slots:
  - `block1 30` now occupies a valid property slot.
  - `dmg-mag 25-50` now occupies a valid property slot.

Explicitly excluded 13 items from the buff pass:

- Spin's Enigma
- Spin's Paradox
- Spin's Mystery
- Spin's Conundrum
- Spin's Perplexing Puzzle
- Incarnadine Elven Plate
- Lilarcors Crown
- Teleomortis' Gloves
- Citadel Belt
- Cryptic Claws
- Way of the Shadow
- Return to Hydrakal
- Onyx's Celestial Rage

Validation performed:

- Active/base `setitems.txt` hashes matched after buff pass.
- Every row had 102 columns.
- All 93 approved items contained their proposed additions.
- Excluded rows were exact matches to pre-change HEAD.
- No malformed item-property slots remained.

## Set Buff Range Pass

The user noticed most added affixes were fixed rolls like `deadly 25-25`. A follow-up range pass was implemented in commit `6a592bdf`.

Range-pass rules:

- Scope only the newly added set-buff affixes from the approved pass.
- Do not change unrelated pre-existing set stats.
- Keep the 13 excluded items untouched.
- Convert fixed numeric values into roll ranges.
- The previous fixed number generally became the upper bound.
- Widened ranges more aggressively than the first proposal.
- Added skill affixes now roll instead of staying fixed.
- Binary effects stayed fixed.

Stats changed:

- 209 newly added fixed values were converted to ranges per file.
- Active and base files were changed identically.
- After the pass, only four newly added fixed stats remained:
  - `Greyhawk's Icebrand`: `freeze 1`
  - `Arctic Furs`: `half-freeze 1`
  - `Featherfoot`: `half-freeze 1`
  - `Panda's Sash`: `half-freeze 1`

Examples:

- `Teachings of Brother Laz`: added `allskills` changed from `2-2` to `1-2`; added `cast2` changed from `20-20` to `10-20`.
- `Temptation's Death`: added `allskills` changed from `1-1` to `1-2`.
- `Greyhawk's Icebrand`: added `pal` changed from `1-1` to `1-2`; `freeze` stayed `1-1`.
- `Mystic Blades`: repaired `block1` changed from `30-30` to `18-30`; added `block` changed from `20-20` to `10-20`; added leech rolls changed to `3-5`.

Validation performed:

- Active/base `setitems.txt` both still have 102 columns per row.
- Active/base `setitems.txt` hashes match.
- The excluded 13 items are unchanged.
- Live install hashes matched repo hashes.

## Added Skill Buffs In Set Pass

These were the newly added skill affixes from the buff pass. After the range pass, these generally roll `1-2` unless otherwise constrained by the file.

All skills:

- `Teachings of Brother Laz`: `allskills`
- `Ser'Angreal Necklace`: `allskills`
- `Guiding Force`: `allskills`
- `Temptation's Death`: `allskills`

Amazon:

- `Trent's Caster`: `ama`

Assassin:

- `Jakira's Strike`: `ass`
- `Mask of Vashna`: `ass`

Barbarian:

- `Chaos Heart`: `bar`
- `Born Supremacy`: `bar`

Druid:

- `Wolf Pelt`: `dru`
- `Cry of the Wolf`: `dru`

Necromancer:

- `Dracolich`: `nec`
- `Lord Hades' Throne`: `nec`
- `Lich's Cranium`: `nec`
- `Unholy Desires`: `nec`
- `Dark Rituals`: `nec`
- `Wall of Modius`: `nec`

Paladin:

- `Greyhawk's Icebrand`: `pal`
- `Firecam Gilded Plate`: `pal`
- `Holy Sash of Amaunator`: `pal`
- `Sunspear Deflector`: `pal`

No new `skilltab` buffs were added in that pass.

## Rare Item Overhaul Design

Design doc:

- `docs/rare-item-rework-design-2026-05-18.md`

The rare overhaul has not been implemented yet. It is currently a design discussion.

User goals:

- Make rare quality items roughly 3x rarer.
- The change should primarily affect elite base rares.
- Exceptional base rares should be affected to a lesser extent.
- Normal base rares should mostly stay as-is.
- Rares should roll better affixes on average.
- All rare-eligible affixes should have their effective level gates lowered proportionally by about 30%, while preserving family order.
- Only the top normal affix in each family should get a true early/late frequency split.
- Top affixes should be able to appear earlier, but be less likely before their old gate.
- Introduce "Greater Affixes": rare affixes much stronger than standard affixes.

Important constraints found:

- Rare affix cap appears engine-side rather than TXT-side.
- Treat rare items as capped at 6 affix records: up to 3 prefixes and 3 suffixes.
- There is no obvious TXT knob for increasing that cap.
- Each affix can carry up to 3 stat mods through `mod1`, `mod2`, `mod3`, so power can be increased without raising the affix count.
- `itemratio.txt` cannot cleanly target elite separately from exceptional.

Current rare quality values in `itemratio.txt`:

| Row | Rare | RareDivisor | RareMin |
|---|---:|---:|---:|
| Classic normal non-class | 160 | 3 | 3200 |
| Classic exceptional/elite non-class | 96 | 3 | 3200 |
| Expansion normal non-class | 100 | 2 | 3200 |
| Expansion exceptional/elite non-class | 100 | 2 | 3200 |
| Expansion normal class-specific | 80 | 3 | 3200 |
| Expansion exceptional/elite class-specific | 80 | 3 | 3200 |

Initial design recommendation in the doc:

- Leave `Uber=0` rows unchanged.
- Change only `Uber=1` rows as a first approximation.
- Suggested safer start: 2.5x rarer for exceptional+elite, then make elite feel better through affix design.
- Full 3x alternative is also documented.

## Greater Affix Discussion Updates

The initial Greater Affix proposal said to use `frequency=1`, high level gates, rare-only rows, and narrow item types.

The user corrected the weighting approach:

- `frequency=1` is rarer than `frequency>1`.
- The right approach is to make ordinary/non-Greater affixes have higher frequency, and keep Greater Affixes low.
- Greater Affixes should be rare by relative dilution, not only by being `frequency=1`.

Current frequency audit:

`magicprefix.txt` rare-eligible rows:

- 918 total rare-eligible.
- 284 have `frequency=1`.
- 634 have `frequency>1`.
- Total rare-eligible prefix weight: 5987.
- All `frequency=1` prefixes together are about 4.74% of prefix weight.

`magicsuffix.txt` rare-eligible rows:

- 726 total rare-eligible.
- 248 have `frequency=1`.
- 478 have `frequency>1`.
- Total rare-eligible suffix weight: 15825.
- All `frequency=1` suffixes together are about 1.57% of suffix weight.

Updated Greater Affix design direction:

- Greater Affixes should generally use early/mid/late frequencies `1/2/3`.
- Ordinary desirable affixes should often be `frequency=4-12`.
- Common/filler affixes should often be `frequency=12-48+`.
- Some existing `frequency=1` proc/charged affixes may need review; not every `frequency=1` affix should be treated as chase-tier.
- Greater Affixes should use the same `group` as the normal affix family they upgrade, so normal and Greater versions do not stack.
- Greater Affixes with a spare mod slot should include `greater-affix-marker` so the tooltip shows `** Greater Affix`.

## Phase 1 Affix Level Compression

The user does not want rare affixes strictly gated by very high affix level, but also does not want the affix ladder distorted.

Important conclusion:

- `level` controls when an affix can spawn.
- `maxlevel` can cap an affix's spawn band.
- `levelreq` controls when the player can equip/use the item.
- `levelreq` can be higher than the affix/drop/item level.
- Directly editing a shared `spawnable=1, rare=1` row also affects magic items. Use rare-only early rows if the change must stay rare-only.

Current Phase 1 direction:

- Lower the effective rare availability gate for all rare-eligible affixes by about 30%.
- Formula: `compressed_level = max(1, round(original_level * 0.70))`.
- Compress `maxlevel` too when it exists.
- Preserve family ordering after compression. A lower Cruel row should not end up above the stronger Cruel row.
- Only the best normal affix in each family gets an early/late split.

Top affix split:

- early row: compressed level, `maxlevel = original_top_level - 1`, half frequency
- late row: original level, original frequency

This lets lower-level drops hit the top affix rarely, while high-level rares do not get an extra duplicate chance.

## Useful External Reference

The user pointed to the D2R Data Guide:

- https://eezstreet.github.io/d2rdoc/guides/getting-started.html

The guide is useful for the loose-file modding workflow and confirms the general `-mod <name> -txt` pattern.

For `itemratio.txt`, the d2rdoc source was useful for confirming the `Uber` field behavior:

- https://raw.githubusercontent.com/eezstreet/d2rdoc/master/data/files/itemratio.js

## Suggested Next Steps For The Next Session

1. If continuing the rare overhaul, do not start with bulk edits.
2. Treat `docs/rare-item-rework-design-2026-05-18.md` as the canonical rare rework design doc.
3. The 2.5x `Uber=1` rare rarity pass is already implemented; test before moving to 3x.
4. Generate a rare affix family audit before editing `magicprefix.txt` or `magicsuffix.txt`.
5. For Phase 1:
   - calculate compressed level and maxlevel values using the 70% formula
   - validate that each affix family remains ordered correctly
   - decide direct shared-row edits vs rare-only early rows
   - add the top-affix early/late split for each target family
6. For Phase 2 Greater Affix families:
   - identify the existing normal affix `group`
   - add early/mid/late Greater rows with frequencies `1/2/3`
   - include `greater-affix-marker` when a row has a spare mod slot
   - normalize family frequencies only if Greater odds are too common or too rare
7. Validate with TSV-aware scripts:
   - active/base files identical where expected
   - column counts unchanged
   - property codes exist in `properties.txt`
   - Greater rows have `spawnable=0`, `rare=1`, non-empty `group`, non-zero `frequency`
8. Install to live with:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\install-local.ps1 -D2RPath "E:\Diablo II Resurrected" -ModName "XavReimagined"
```

9. Hash-check live files against repo files after install.
10. Commit and push every completed implementation checkpoint to `origin/xav-custom`.

## Working Practices To Preserve

- Use GitHub for all changes.
- Keep docs updated with every meaningful modding discovery.
- Keep active and `/base/` copies in sync when both exist.
- Use TSV-aware editing; do not use Excel for these files.
- Validate column counts after every TXT edit.
- Install to live after gameplay data changes unless the user says not to.
- Do not revert unrelated user changes.
