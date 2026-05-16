# Ranked Conversion and Assemblage Orbs

## Current State

Current item codes:

```text
ooc  Orb of Conversion
ooa  Orb of Assemblage
1oc  Orb of Conversion Stack
1oa  Orb of Assemblage Stack
```

Current conversion recipes:

```text
amu,rar  + ooc -> amu,uni
armo,rar + ooc -> usetype,uni
rin,rar  + ooc -> rin,uni
weap,rar + ooc -> usetype,uni

amu,rar  + ooa -> amu,set
armo,rar + ooa -> usetype,set
rin,rar  + ooa -> rin,set
weap,rar + ooa -> usetype,set
```

Current active treasure classes:

```text
Infusion Orb    -> ooi
Assemblage Orb  -> ooa
Conversion Orb  -> ooc
Jewelry Orbs    -> Infusion Orb weight 3, Assemblage Orb weight 1, Conversion Orb weight 1
Mephistoq       -> Assemblage Orb + Mephistoq Item
Diabloq         -> Conversion Orb + Diabloq Item
Baalq           -> Corruption Orb + Baalq Item
```

`data/global/excel/base/treasureclassex.txt` currently has a more stack-aware shape with `Jewelry Orbs Single`, `Jewelry Orbs Stack`, and stack item outputs. The active file does not use that same split. Claude should check whether implementation should preserve active behavior, mirror active/base exactly, or intentionally keep base as a richer reference file.

## Code Scheme

Observed item-code max length is 3 characters in `misc.txt`, `weapons.txt`, and `armor.txt`. Use three-character codes rather than `ooaii`/`ooaiii`.

Proposed single-orb codes:

```text
ooc  Orb of Conversion I
oc2  Orb of Conversion II
oc3  Orb of Conversion III

ooa  Orb of Assemblage I
oa2  Orb of Assemblage II
oa3  Orb of Assemblage III
```

Rank I keeps the existing item codes exactly, per Eric's request. The visible name for rank I should probably gain the roman numeral so the player can distinguish it from rank II/III, but this is a player-facing compatibility question.

## Item Definition Plan

Add four new rows to active and base `misc.txt`, copied from the existing unstacked `ooc`/`ooa` rows:

```text
Orb of Conversion II   code=oc2  namestr=oc2
Orb of Conversion III  code=oc3  namestr=oc3
Orb of Assemblage II   code=oa2  namestr=oa2
Orb of Assemblage III  code=oa3  namestr=oa3
```

Keep inventory/flippy art, size, rarity, type, and item-category behavior the same as rank I unless Claude identifies a reason to differentiate.

Add strings in `data/local/lng/strings/item-names.json`:

```text
ooc  -> Orb of Conversion I
oc2  -> Orb of Conversion II
oc3  -> Orb of Conversion III
ooa  -> Orb of Assemblage I
oa2  -> Orb of Assemblage II
oa3  -> Orb of Assemblage III
```

Descriptions should state the required base tier:

```text
Conversion I: Cube with a normal rare item to convert it to Unique.
Conversion II: Cube with an exceptional rare item to convert it to Unique.
Conversion III: Cube with an elite rare item to convert it to Unique.

Assemblage I: Cube with a normal rare item to convert it to Set.
Assemblage II: Cube with an exceptional rare item to convert it to Set.
Assemblage III: Cube with an elite rare item to convert it to Set.
```

## Cube Recipe Plan

Use `bas`, `exc`, and `eli` to restrict base tier. These qualifiers are already used by the rare/set/unique upgrade recipes:

```text
"armo,bas,rar"
"armo,exc,rar"
"weap,bas,rar"
"weap,exc,rar"
```

Proposed armor/weapon recipes:

```text
CONVERSION I ARMOR   "armo,bas,rar" + ooc -> usetype,uni
CONVERSION II ARMOR  "armo,exc,rar" + oc2 -> usetype,uni
CONVERSION III ARMOR "armo,eli,rar" + oc3 -> usetype,uni

CONVERSION I WEAPON   "weap,bas,rar" + ooc -> usetype,uni
CONVERSION II WEAPON  "weap,exc,rar" + oc2 -> usetype,uni
CONVERSION III WEAPON "weap,eli,rar" + oc3 -> usetype,uni

ASSEMBLAGE I ARMOR   "armo,bas,rar" + ooa -> usetype,set
ASSEMBLAGE II ARMOR  "armo,exc,rar" + oa2 -> usetype,set
ASSEMBLAGE III ARMOR "armo,eli,rar" + oa3 -> usetype,set

ASSEMBLAGE I WEAPON   "weap,bas,rar" + ooa -> usetype,set
ASSEMBLAGE II WEAPON  "weap,exc,rar" + oa2 -> usetype,set
ASSEMBLAGE III WEAPON "weap,eli,rar" + oa3 -> usetype,set
```

The existing all-tier `armo,rar` and `weap,rar` recipes should be replaced or disabled so rank I cannot affect exceptional/elite items.

## Jewelry Plan

Current recipes also support rare amulets and rings:

```text
amu,rar + ooc -> amu,uni
rin,rar + ooc -> rin,uni
amu,rar + ooa -> amu,set
rin,rar + ooa -> rin,set
```

Rings and amulets do not have normal/exceptional/elite base tiers in the same sense as armor/weapons. Eric proposed using output item-level caps instead:

```text
Rank I   -> up to level 40 jewelry outcomes
Rank II  -> up to level 70 jewelry outcomes
Rank III -> full/high-level jewelry outcomes
```

Proposed cube recipes:

```text
CONVERSION I AMULET   amu,rar + ooc -> amu,uni  lvl=40
CONVERSION II AMULET  amu,rar + oc2 -> amu,uni  lvl=70
CONVERSION III AMULET amu,rar + oc3 -> amu,uni  lvl=99

CONVERSION I RING   rin,rar + ooc -> rin,uni  lvl=40
CONVERSION II RING  rin,rar + oc2 -> rin,uni  lvl=70
CONVERSION III RING rin,rar + oc3 -> rin,uni  lvl=99

ASSEMBLAGE I AMULET   amu,rar + ooa -> amu,set  lvl=40
ASSEMBLAGE II AMULET  amu,rar + oa2 -> amu,set  lvl=70
ASSEMBLAGE III AMULET amu,rar + oa3 -> amu,set  lvl=99

ASSEMBLAGE I RING   rin,rar + ooa -> rin,set  lvl=40
ASSEMBLAGE II RING  rin,rar + oa2 -> rin,set  lvl=70
ASSEMBLAGE III RING rin,rar + oa3 -> rin,set  lvl=99
```

Use fixed `lvl` rather than `plvl` or `ilvl` unless Claude advises otherwise. Current conversion recipes use fixed `lvl=99`, and existing cube recipe `lvl` values in this repo top out at `99`, so rank III should use `99` as the practical "100/full pool" value.

Local jewelry-level counts with current data:

```text
Unique jewelry lvl <= 40: 19
Unique jewelry lvl <= 70: 36
Unique jewelry lvl <= 99: 49

Set jewelry lvl <= 40: 24
Set jewelry lvl <= 70: 36
Set jewelry lvl <= 99: 39
```

Important review question: confirm that cube output `lvl` controls the generated output item level before unique/set selection, so `amu,uni lvl=40` and `rin,set lvl=40` really exclude unique/set jewelry rows whose `lvl` is above 40. If it only changes the resulting item level after selection, this plan would not work.

## Drop Weight Plan

For generic drops, preserve rank I's current relative chance while making rank II and III additional lower-frequency outcomes.

Current active `Jewelry Orbs` weights:

```text
Infusion Orb    3
Assemblage Orb  1
Conversion Orb  1
```

Scale the current weights by 6, then add rank II at 1/3 of rank I and rank III at 1/6 of rank I:

```text
Infusion Orb       12
Assemblage Orb I    6
Assemblage Orb II   2
Assemblage Orb III  1
Conversion Orb I    6
Conversion Orb II   2
Conversion Orb III  1
```

This keeps each rank I weight at the same scaled value as before, while rank II is 3x rarer than rank I and rank III is 6x rarer than rank I. It does make Infusion less common within this TC because new outcomes have been added.

If Claude thinks "same drop rate" should mean "same share among all possible `Jewelry Orbs` results after adding the new ranks," then the alternative is a family selector with weights `6/2/1`, but that would reduce rank I's absolute share compared with the current rankless orb.

## Boss Quest-Drop Plan

Current quest bosses that directly drop these orbs:

```text
Mephistoq -> Assemblage Orb
Diabloq   -> Conversion Orb
Baalq     -> Corruption Orb
```

Eric said Baal/Diablo "I think"; local data shows Mephisto drops Assemblage, Diablo drops Conversion, and Baal drops Corruption.

Add boss-only tier selector treasure classes:

```text
Assemblage Orb Quest -> ooa weight 6, oa2 weight 2, oa3 weight 1
Conversion Orb Quest -> ooc weight 6, oc2 weight 2, oc3 weight 1
```

Point Mephistoq to `Assemblage Orb Quest` and Diabloq to `Conversion Orb Quest`. This gives rank II and III chances relative to rank I of roughly 1:3 and 1:6 without changing the fact that the quest boss reward slot drops an orb.

If this proves risky in review, leave quest bosses pointed at rank I only as Eric allowed.

## Stack Support

Do not add rank II/III stack variants in the first implementation unless Claude says stack parity is important. Full stack parity would require additional item codes and many stack/unstack recipes, probably:

```text
2oc / 3oc for Conversion II/III stacks
2oa / 3oa for Assemblage II/III stacks
```

That is a much larger recipe-table change than the gameplay request strictly requires. Ranks II/III are expected to be rarer, so single-item inventory handling may be acceptable initially.

## Expected Files To Change After Approval

```text
data/global/excel/misc.txt
data/global/excel/base/misc.txt
data/global/excel/cubemain.txt
data/global/excel/base/cubemain.txt
data/global/excel/treasureclassex.txt
data/global/excel/base/treasureclassex.txt
data/local/lng/strings/item-names.json
docs/modding-findings.md
```

## Validation Plan After Implementation

1. Parse active/base TSV files and confirm all edited rows have the expected column counts.
2. Confirm active/base `misc.txt` and `cubemain.txt` orb rows match.
3. Confirm old all-tier `armo,rar`/`weap,rar` recipes no longer let rank I convert exceptional or elite items.
4. In game, test:
   - Normal rare weapon/armor + rank I works.
   - Exceptional rare weapon/armor + rank I fails.
   - Exceptional rare weapon/armor + rank II works.
   - Elite rare weapon/armor + rank II fails.
   - Elite rare weapon/armor + rank III works.
   - Equivalent Assemblage tests for set output.
5. Test Mephisto and Diablo quest-drop behavior if quest selector TCs are implemented.
6. Run local install only after Claude approval and implementation.
