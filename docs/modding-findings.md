# D2R Modding Findings

Living notes for discoveries made while testing XavReimagined. Treat this as practical project knowledge, not a full D2R data-file reference.

Updated: 2026-05-17.

Latest handoff for continuing in another Codex session: `docs/session-handoff-2026-05-18.md`.

Full D2RDoc reading notes from the 2026-05-18 sitemap crawl: `docs/d2rdoc-reading-notes-2026-05-18.md`.

## Workflow Notes

- The active gameplay tables live under `data/global/excel/`.
- The mirror/reference tables live under `data/global/excel/base/`.
- When changing a table that has a `base/` counterpart, update both unless there is a deliberate reason not to. We already hit this with `setitems.txt`: gameplay was correct in the active file, but `base/setitems.txt` drifted and could have confused future scripts.
- Publish to the live game with `scripts/install-local.ps1`.
- Current live target is `E:\Diablo II Resurrected\mods\XavReimagined\XavReimagined.mpq`.
- Current launch args are `-mod XavReimagined -txt`.
- After gameplay/data changes are validated, commit and push them to `origin/xav-custom`; keep the relevant docs/review notes in the same commit.

## Tooltips Vs Mechanics

- Skill tooltips are largely controlled by `skilldesc.txt` and string JSON files.
- Skill behavior is controlled by `skills.txt`, `missiles.txt`, and related data rows.
- These can absolutely disagree. A tooltip can show a value that is not the exact runtime behavior if the formula is wrong, if the missile applies damage differently, or if the skill row itself is carrying hidden damage.
- Cobra Strike showed this clearly: when the main charge-up skill row itself carries poison `EType` / `EMin` / `EMax`, the first Cobra builder hit can apply that poison before any finisher release happens.
- Literal percent signs in string JSON must be escaped as `%%`. A raw `%` inside tooltip text can be interpreted as another printf placeholder and render garbage numeric text, as happened with Fists of Fire's "100% weapon damage as fire" note.

## Cube Recipe Item Codes

- In `cubemain.txt`, `qty=N` on a loose item code such as `ooi,qty=11` is valid for matching multiple loose cube inputs of that item.
- In `misc.txt`, D2R advanced stash stacking for loose special items uses `AdvancedStashStackable=1`. This is separate from the older explicit stack item rows that use `stackable=1`, such as `1oc` / `1oa`.
- Advanced stash support also needs explicit `AdvancedStashSlotWidget` entries in both HD stash layouts: `data/global/ui/layouts/bankexpansionlayouthd.json` and `data/global/ui/layouts/controller/bankexpansionlayouthd.json`. New loose stackable item codes will not get a visible stash slot from `AdvancedStashStackable=1` alone.
- In the HD Gems stash layout, the normal stash grid starts at `y=708` for keyboard/mouse and `y=598` in the controller layout. A full 98px stack slot row immediately above that can visually overlap the stash grid, so new stack widgets should be packed into unused positions in the existing top rows unless the grid/background is deliberately redesigned.
- New visible inventory item codes need HD asset bindings in `data/hd/items/items.json`; otherwise the item can exist but show the missing-icon placeholder.
- D2R string color control prefixes must be written with the actual `0xff` character, such as `0xff + "c8"` for orange power-orb names. If tooling mangles that byte to `?c8`, the tooltip will show the color code literally and the item will not render orange.
- This mod's player-facing Topaz and Emerald item codes are `gmt` and `gme`.
- Vanilla perfect gem codes such as `gpy` and `gpg` may still exist in `misc.txt`, but they are not the Topaz/Emerald items used by the mod's active cube recipes.
- Orb of Conversion / Assemblage rank II and III item codes use the 3-character-safe codes `oc2`, `oc3`, `oa2`, and `oa3`. The original rank I codes remain `ooc` and `ooa`, with only their visible names changed to include `I`.
- Current ranked orb implementation tiers armor and weapon recipes with `bas` / `exc` / `eli`. Jewelry conversion/assemblage recipes remain on the old rank-I behavior until we verify that cube output `lvl` gates the unique/set jewelry selection pool before the item is chosen.
- Generic Jewelry Orbs treasure-class weighting keeps rank I as the common baseline and adds rank II/III as rarer outcomes: Infusion `12`, Assemblage I/II/III `6/2/1`, Conversion I/II/III `6/2/1`.
- Ranked orb downgrade recipes return three loose lower-rank outputs using `output`, `output b`, and `output c`, rather than relying on `code,qty=3` for a single output. Current downgrades are `oc3 -> 3x oc2`, `oc2 -> 3x ooc`, `oa3 -> 3x oa2`, and `oa2 -> 3x ooa`.

## Item Quality Ratios

- Global item quality roll tuning lives in `itemratio.txt`, now tracked in both `data/global/excel/` and `data/global/excel/base/`.
- Unique and set quality rolls are independently tunable through `Unique` / `UniqueDivisor` / `UniqueMin` and `Set` / `SetDivisor` / `SetMin`.
- Higher ratio values make that quality harder to roll. Sets now mirror uniques in every `itemratio.txt` row by matching `Set` / `SetDivisor` / `SetMin` to `Unique` / `UniqueDivisor` / `UniqueMin`.
- Before this change, uniques were 2x to 3.2x rarer than sets by raw ratio column, with the main expansion non-class rows at 2.5x.
- To make sets globally rarer than uniques later, raise the relevant `Set` values above the matching `Unique` values, and consider raising `SetMin` above `UniqueMin` so high-level or high-MF cases do not cap sets as generously.
- `itemratio.txt` can target normal vs exceptional/elite through `Uber=0` and `Uber=1`, but it does not expose a separate elite-only row. For the rare rework, elite-primary behavior should come from affix level/weighting, with `Uber=1` rarity changes affecting exceptional and elite together.

## Rare Affix Rework

- The canonical rare item rework design is in `docs/rare-item-rework-design-2026-05-18.md`. The separate Greater Affix pilot doc was merged into it.
- The generated all-group apex audit and draft Greater Affix chance report is `docs/rare-greater-affix-apex-audit-2026-05-19.md`. Regenerate it with `python scripts/audit_rare_affix_apexes.py` after changing the candidate list or affix tables.
- Rare affix count appears engine-side rather than TXT-side; treat rares as capped at 6 affix records, up to 3 prefixes and 3 suffixes.
- Greater Affixes should be implemented as rare-only rows in `magicprefix.txt` / `magicsuffix.txt` using `spawnable=0`, `rare=1`, low `frequency`, and the same `group` as the normal affix family they upgrade.
- D2RDoc confirms `frequency` is a weight. Higher values are more common among eligible affixes; Greater Affixes should be rare by low relative weight and by dilution against ordinary/filler affixes with higher frequencies.
- `level` controls minimum affix item level, `maxlevel` can create spawn bands, and `levelreq` controls equip requirement. This supports early-access rare-only Greater rows that can drop before they can be equipped.
- First rare rarity pass applied on 2026-05-18: both `itemratio.txt` copies now make only `Uber=1` rare rows 2.5x rarer. `Uber=0` normal-base rare rows are unchanged. Elite-specific power should come later through affix design because `itemratio.txt` cannot split exceptional from elite.
- Phase 1 lowers effective affix availability for affixes using the proportional formula `compressed_level = max(1, round_half_up(original_level * 0.70))`; rows with `maxlevel` should compress that gate too.
- Use round-half-up for rare affix compression: `round_half_up(x) = floor(x + 0.5)`.
- Phase 1 also lowers affix equip requirements by 15% with `compressed_levelreq = max(1, round_half_up(original_levelreq * 0.85))`, leaving blank/zero requirements blank/zero.
- Phase 1 only gives the best normal affix in each family a true early/late frequency split. The early top row starts at the compressed level, ends at `original_top_level - 1`, and uses half the late frequency.
- Preserve family ordering after compression. A weaker row such as lower Cruel must not end up requiring a higher level than the stronger Cruel row.
- Directly editing shared `spawnable=1, rare=1` affix rows also changes magic items. This is acceptable for the Phase 1 affix compression.
- Phase 2 adds Greater Affixes with multiple technical level bands. Example: `Greater Grandmaster's` starts at level `50`, gains broader rider variants across `50-65`, `66-80`, and `81+`, and stays rare by low per-row frequency.

## Set Item Buff Pass

- The low-affix set item proposal was implemented in both active and base `setitems.txt` on 2026-05-17 for 93 approved items. The 13 user-excluded items were left untouched for later whole-set review.
- `Mystic Blades` had its malformed item-property slots repaired so `block1 30` and `dmg-mag 25-50` occupy valid property slots before the approved item buffs.
- A follow-up range pass on 2026-05-18 converted newly added fixed numeric buff values into roll ranges. Added skill bonuses now roll, mostly `1-2`; binary effects such as `freeze` and `half-freeze` stayed fixed.

## Belt Potion Rows

- Belt potion row capacity is controlled by the `belt` column in `armor.txt`, not by the equipment-slot placement rows in `inventory.txt`.
- The low normal belt bases now use `belt=3`, matching the Plated Belt's known four-row tier: `Sash`, `Light Belt`, `Belt`, and `Heavy Belt`.
- `Plated Belt` already used `belt=3`; exceptional and elite belts stay at `belt=6`.
- Unique and set belts inherit this behavior from their base item code, so no unique/set item rows were needed for the all-belts-four-rows pass.

## Poison Damage Math

D2 poison and other frame-based damage uses raw data values, `HitShift`, and frame length.

Useful working formula:

```text
total damage = raw_rate * (2^HitShift / 256) * duration_frames
damage per second = raw_rate * (2^HitShift / 256) * 25
```

For `HitShift = 4`:

```text
2^4 / 256 = 16 / 256 = 1 / 16
DPS = raw_rate * 25 / 16
2 sec total = raw_rate * 50 / 16
4 sec total = raw_rate * 100 / 16
```

Practical implication: raw poison numbers in the table are not already final displayed damage. A raw value that looks tiny can become meaningful once duration and `HitShift` are applied, and a raw value that looks moderate can become enormous.

## SrcDamage

- `SrcDamage`/`SrcDam` appears to be source damage in 128ths.
- `128` means 100 percent source damage.
- Values above `128` are unsafe. D2RDoc marks this field as 8-bit, and our test with `512` caused broken-looking character sheet damage such as `0-1`.
- Use `128` as the practical max unless a specific row proves otherwise.
- For Cobra Strike, weapon scaling felt good after flat poison was reduced to nearly nothing and `SrcDamage=128` was used, but source damage is risky on lingering DOT/cloud-style collision missiles. Current Cobra charge 2 keeps `SrcDamage=128` only on the dedicated one-shot `cobrastrikecloudhit` server payload; the lingering visual cloud row stays at `SrcDamage=0`.
- Active Tiger Strike charges did not appear to multiply Cobra Strike's source-damage release in testing. Hard-point synergy from `EDmgSymPerCalc = skill('Tiger Strike'.blvl)*10` still applies.

## Cobra Strike Current Model

Current design direction:

- Charge 1: restored to the original direct single-target poison finisher model. `srvprgfunc1`, `srvmissilea`, `cltprgfunc1`, and `cltmissilea` stay blank, while the main skill row carries `EType=pois` and its poison curve. Current charge 1 poison rate is roughly 50% higher than the earlier equalized test curve, with `ELen=50`.
- Charge 2: currently routed through the dedicated `cobrastrikecloudhit` server missile so charge 2 can be balanced independently from charge 3.
- Charge 2 uses `cltprgfunc2=9`, `prgcalc2=par1+((lvl-1)/6)`, and `cltmissileb=cobrastrikecloud` as the client-only poison cloud visual. The client cloud visual now uses `Range=150`, which is 6 seconds at 25 frames per second.
- Charge 3: poison nova missile, `SrcDamage=128`, plus flat poison over 2 seconds. Its missile range is intentionally modest and grows slowly.
- Flat poison should stay moderate on DOT/cloud-style effects because source damage can create unclear repeated-hit scaling when it is attached to a lingering collision cloud.
- Current playtest note: charge 2 cloud visuals work when `cltmissileb=cobrastrikecloud` and `prgcalc2` stays populated. Charge 1 must not use the helper missile path, because that made it behave like the charge 2 AoE.

Important current-value note:

- Cobra's charge-up skill row currently carries direct `EType` / `EMin` / `EMax` / `ELen` so charge 1 releases as a single-target poison finisher.
- `cobrastrikehit` was removed after testing because it made charge 1 behave like an AoE release.
- `cobrastrikecloudhit` is a charge 2-only copy of the nova-style server payload with lower poison values, `HitShift=3`, `SrcDamage=128`, and `ELen=150`. This is intended to add one 100% source/weapon damage payload while keeping the total charge 2 flat poison payload about half of the previous 2-second payload over 6 seconds.
- `cobrastrikenova` in `missiles.txt` remains the charge 3 payload with the previous poison curve, `HitShift=4`, `ELen=50`, and `SrcDamage=128`.
- `prgcalc2` must stay populated for `cltprgfunc2=9`; otherwise charge 2 can work mechanically while drawing no poison cloud visual.
- `cobrastrikecloud` should not be reintroduced as the charge 2 server missile without retesting repeated collision damage; it is currently only the charge 2 client visual.
- Charge 1, charge 2, and charge 3 tooltips can diverge because the tooltip is formula-driven and may not reflect whether a payload comes from the skill row or missile row unless `skilldesc.txt` is updated alongside gameplay fields.
- Cobra's detailed charge tooltip lines are authored in reverse slot order in `skilldesc.txt` so the game renders charge 1 at the top and charge 3 at the bottom, matching the other Assassin charge-up skills.

## Poison Cloud Collision Behavior

Historical note from the removed Cobra charge 2 cloud experiment:

- Monsters do not simply stand in the cloud and take a normal periodic DOT.
- The monster must move through or across cloud collision areas.
- Damage is applied on collision/hit events as the monster crosses cloud pieces.
- With `SrcDamage=128`, weapon damage was applied through those collision events. Keep `SrcDamage=0` on the lingering `cobrastrikecloud` visual/collision row; put weapon damage only on the dedicated one-shot `cobrastrikecloudhit` server payload.
- This means the cloud can behave more like repeated collision damage than a passive poison puddle.

Current `cobrastrikecloud` row characteristics:

```text
pSrvDoFunc = 3
CollideType = 3
LastCollide = 1
Collision = 1
ClientCol = 1
NextHit = blank
NextDelay = blank
Size = 2
Range = 150
HitShift = 4
SrcDamage = 0
EType = pois
ELen = 100
```

Interpretation:

- The game can check cloud collision very frequently, up to the 25 FPS engine cadence.
- `LastCollide=1` prevents the simplest "same missile hits the same target every frame forever" model.
- The actual hit rate is still not a clean DOT tick rate. It depends on monster movement, monster size, cloud layout, and whether the target enters new collision pieces.

## NextHit And NextDelay

Likely normalization lever for cloud balance:

```text
NextHit = 1
NextDelay = N
```

Because D2 runs at 25 frames per second:

| NextDelay | Max applications per target |
|---:|---:|
| 25 | 1.00/sec |
| 12 | 2.08/sec |
| 10 | 2.50/sec |
| 8 | 3.13/sec |
| 6 | 4.17/sec |
| 5 | 5.00/sec |

Test plan:

- Start with `NextHit=1`, `NextDelay=12` on `cobrastrikecloud`.
- Keep flat poison tiny.
- Compare weak weapon vs strong weapon while dragging the same monster type through the cloud.
- If damage becomes predictable, tune cloud around expected collision applications per second.

## Blade Fury Comparison

Blade Fury is a useful comparison because it feels collision/re-hit based in game.

In this mod, the active Blade Fury skill uses the Reimagined missile chain:

```text
Blade Fury skill -> ri_bladefury -> ri_bladefuryspread -> ri_bladefuryspread_2
```

The older-looking `bladefury1`, `bladefury2`, `bladefury3`, and `bladefragment*` rows still exist, but the active `skills.txt` row points at `ri_bladefury`.

Relevant active missile values:

| Missile | pSrvDoFunc | pSrvHitFunc | pSrvDmgFunc | LastCollide | NextHit | NextDelay | CollideKill | Pierce | Range | Size |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `ri_bladefury` | 1 | 20 | 1 | 1 | 1 | 1 | 1 | 1 | 25 | 1 |
| `ri_bladefuryspread` | 1 | 20 | 1 | 1 | blank | blank | 1 | blank | 12 | 1 |
| `ri_bladefuryspread_2` | 1 | blank | 1 | 1 | blank | blank | 1 | blank | 12 | 1 |

Interpretation:

- Blade Fury's first missile explicitly uses `NextHit=1`, `NextDelay=1`.
- `NextDelay=1` is only a one-frame cooldown, so it is not a meaningful damage throttle by itself. It mostly means "use the next-hit system, but allow very frequent hits."
- The follow-up spread missiles rely on `LastCollide=1` and `CollideKill=1`, not `NextDelay`.
- Copying Blade Fury's `NextDelay=1` onto a lingering poison cloud would probably not normalize much. For Cobra cloud testing, start much higher, such as `NextDelay=12` or `25`.

## Phoenix Strike And Fists Of Fire Notes

- The internal `skills.txt` row for Phoenix Strike is named `Royal Strike`, even though the game displays Phoenix Strike.
- Phoenix Strike/Royal Strike now has `prgstack=1` so it can be tested like the stack-style elemental charge-ups. The expected result is that a 3-charge finisher releases the lower charge payloads as well, but this still needs in-game verification because Royal Strike uses `srvdofunc=34` while Fists of Fire / Claws of Thunder / Blades of Ice use `srvdofunc=35`.
- Phoenix Strike's released elemental effects mostly come from missiles. The three direct release payloads are `royalstrikemeteor`, `royalstrikechainlightning`, and `royalstrikechaosice`; these should carry `SrcDamage=128` when Phoenix charges are intended to add 100% source/weapon damage.
- Do not put `SrcDamage` on `royalstrikemeteorfire` unless specifically testing repeated ground-fire collision/tick behavior; that is the lingering burning-ground payload and was intentionally excluded.
- Phoenix charge 1 meteor landing delay is controlled in `missiles.txt`, not the `Royal Strike` skill row. `royalstrikemeteorcenter` uses `Range=30` and `CltParam1=29`, matching vanilla Meteor's approximately 1.2-second landing. Keep `royalstrikemeteor` and `royalstrikemeteortail` `Range` values synchronized with the center timing.
- Phoenix Strike's English tooltip should mention `100%% weapon damage` on the three direct release charge lines. The long description should also say burning ground does not add weapon damage, because `royalstrikemeteorfire` remains excluded.
- Claws of Thunder uses the skill row `SrcDam=128` for the direct charge 1 release, while charge 2 and 3 use `clawsofthundernova` and `clawsofthunderbolt`. Those missile rows need `SrcDamage=128` when all three charges should add 100% weapon damage.
- Fists of Fire has `SrcDam=128` on the skill row. For charge 1/2 weapon scaling, use the skill row's progressive conversion lever: `prgdam=4` with `calc1=100`, described in the table as `% Weapon Damage dealt as Fire for progressive release`.
- Fists of Fire's charge 1/2 tooltip text hardcodes `100%% weapon damage as fire`; keep that string in sync if `calc1` changes from `100`.
- Avoid putting `SrcDamage` directly on `fistsoffirefirewall`; it is a lingering collision fire field and has the same class of repeated-hit risk as the old Cobra cloud experiment.
- Dragon Claw can feel strong with Fists of Fire because multiple charge-release payloads can happen across the two claw attacks. Poison is trickier because poison applications compete/refresh rather than simply stacking like separate fire hits.

## Gems Stash Orb Slots

Ranked orbs are grouped as a 2x3 block on the Gems tab in both keyboard/mouse and controller layouts:

| Row | Slots |
|---|---|
| Top | `ooa`, `oa2`, `oa3` |
| Bottom | `ooc`, `oc2`, `oc3` |

Keep those ranks adjacent when adding future orb UI slots; the normal stash grid starts below this area, so prefer reusing open space in the gem utility rows before moving the grid.

## Cube Gamble Recipes

The restored gamble recipes use the same two-step hidden-roll pattern as corruption, but they must not share the corruption dummy stat.

- `item_gambleDummy` is appended to `itemstatcost.txt` and mapped through `gambleDummy` in `properties.txt`.
- The cube `op/param` checks use the numeric `item_gambleDummy` stat ID, while the cube modifier uses the `gambleDummy` property code.
- The dummy recipe only runs when the hidden gamble roll is absent/zero, returns the original rare item plus catalyst outputs, and writes a 1-100 roll onto the item.
- The result recipes then resolve that same item with descending `op=15` thresholds, so row order matters.
- Basic rare item + magic jewel recipes are 5% unique, 5% set, 90% rare reroll.
- Improved weapon/armor recipes with Pul/Lem + magic jewel are 15% unique, 15% set, 70% rare reroll.
- The inherited design is a two-click cube flow: the first transmute stamps the hidden roll, and the second transmute consumes the catalyst and resolves the result.

Current hidden IDs:

| Table | Code | ID |
|---|---|---:|
| `itemstatcost.txt` | `item_gambleDummy` | 437 |
| `properties.txt` | `gambleDummy` | 431 |

If these tables are regenerated from upstream, keep the gamble dummy appended rather than inserting it near `item_corruptedDummy`; inserting would shift later stat IDs and risk breaking existing numeric `param` checks.

## Rare Affix Rework Notes

The rare affix rework is now split into two phases.

Phase 1 is proportional rare affix level compression:

- Lower the effective availability gate for affixes by about 30%, using `round_half_up(original_level * 0.70)`.
- Compress `maxlevel` too when it exists.
- Lower affix `levelreq` by 15%, using `round_half_up(original_levelreq * 0.85)`.
- Keep the whole family ladder proportional so lower tiers do not end up gated above stronger tiers.
- Only the best normal affix in each target family gets a true early/late split.
- The top early row uses the compressed level, `maxlevel = original_top_level - 1`, and about half the late frequency.
- The top late row keeps the original level and original frequency, so high-level rares do not get an extra top-affix chance.

Phase 2 is the Greater Affix layer:

- Add one player-facing Greater category per family, implemented as three technical rows.
- Default Greater bands are early/mid/late with frequencies `1 / 2 / 3`.
- Greater rows stay rare-only, use the same family `group`, and should not stack with the normal family row.
- During Phase 2, scale every existing affix row frequency by the same factor, including `rare=0` magic-only rows. Scaling only rare rows would preserve rare odds but distort magic-item affix odds.
- Greater frequency should be calculated per item-type scope: the total Greater frequency eligible for an item type should equal the current apex frequency before the global scale, making Greater exactly `10x` rarer than that apex after the existing rows are scaled by `10`.
- Broad families must be split by scope/element as needed. One technical row cannot always be exactly `10x` on every item type; leech is the canonical warning case because weapon, ring, amulet, circlet, and glove scopes have different apex weights.
- The generated audit writes `docs/rare-greater-affix-scope-validation-2026-05-19.tsv`; every candidate/item-type row should show a `10x` Greater-vs-apex ratio before implementation.
- Greater rows with a spare mod slot should include `greater-affix-marker`. The marker is backed by `item_greaterAffixMarker` / `GreaterAffixMarker` and prints `** Greater Affix` in orange/gold using D2R color control codes.
- Greater rows must be benchmarked against the strongest existing modded apex row in their group, not just the vanilla-style family name. For weapon ED group `111`, `Grandmaster's` and `Wraithly1` are the real apex rows, so the Greater weapon-damage category is `Greater Grandmaster's`, not a plain enhanced-damage-only upgrade. Current design uses `dmg% 451-500` plus one Grandmaster-style rider such as AR, Deadly Strike, Crushing Blow, or Open Wounds.
- Missed apex families now tracked in the canonical design include `Invulnerable1` / armor `Wraithly1` for defensive group `101`, magic resistance (`Antimagic` / `of Negation`), Fire/Lightning/Cold Coalescence absorb suffixes, and the +skills families (`Omniscient`, `Sage's`, top `skilltab`, and top `skill-rand` rows).
- Charm frequency normalization must not scale group `307` pierce rows in place. Group `307` has charm rows shared with non-charm gear (`ring,mcha` and `amul,glov,boot,belt,helm,lcha`), so a blanket `*5` would also make pierce affixes 5x more common on rings, amulets, gloves, boots, belts, and helms. Exempt `307` unless the rows are first split into charm-only and non-charm-only copies.
- Large charm `+1 skill tree` rows should be normalized to `frequency=10` for all classes, including Warlock. This intentionally changes Warlock rows from their old `frequency=1` relationship so all normal skill-tree charms share one rarity.

## References Worth Keeping Handy

- D2RDoc: `https://eezstreet.github.io/d2rdoc/index.html`
- D2 Data File Guide: `https://wolfieeiflow.github.io/diabloiidatafileguide/`
- Phrozen Keep data-file discussions and guides: `https://d2mods.info/`
- Amazon Basin missile notes: `https://www.theamazonbasin.com/wiki/index.php/Missile`
