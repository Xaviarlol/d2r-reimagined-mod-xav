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

Round 2 decision: normalize active and base treasure classes to the active loose-orb structure as part of this work. The implementation should make active/base orb TC behavior match, using loose `ooi`/`ooa`/`ooc` and the new loose rank II/III codes. The legacy base-only `Jewelry Orbs Single` / `Jewelry Orbs Stack` split should be removed or fully de-referenced so future reviews do not have to interpret accidental drift.

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

Add four new rows to active and base `misc.txt`, copied from the existing unstacked `ooc`/`ooa` rows. For each new row, update all item-code identity columns, not only `code`:

```text
Orb of Conversion II   code=oc2  namestr=oc2  normcode=oc2  ubercode=oc2  ultracode=oc2
Orb of Conversion III  code=oc3  namestr=oc3  normcode=oc3  ubercode=oc3  ultracode=oc3
Orb of Assemblage II   code=oa2  namestr=oa2  normcode=oa2  ubercode=oa2  ultracode=oa2
Orb of Assemblage III  code=oa3  namestr=oa3  normcode=oa3  ubercode=oa3  ultracode=oa3
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

Description plumbing should mirror the current `ooc`/`ooa` rows:

```text
spelldesc=2
spelldescstr=<rank-specific description key>
spelldescstr2=<same rank-specific description key>
```

Add the description keys to `data/local/lng/strings/item-names.json`, alongside the existing `oocDescription` and `ooaDescription` entries. Rank I can either reuse the old keys with revised text or receive explicit `ooc1Description` / `ooa1Description` keys; implementation should prefer the smallest clear diff while making the visible item tooltip state the rank and allowed target tier.

## Cube Recipe Plan

Use `bas`, `exc`, and `eli` to restrict base tier. These qualifiers are already used by the rare/set/unique upgrade recipes:

```text
"armo,bas,rar"
"armo,exc,rar"
"weap,bas,rar"
"weap,exc,rar"
```

Local evidence supports `bas` as the normal-tier qualifier, not "any base item": current salvage rows use `bas`, `exc`, and `eli` to award 1/2/3 Orbs of Infusion by normal/exceptional/elite tier, and current upgrade rows use `bas,rar -> mod,exc` and `exc,rar -> mod,eli`.

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

## Orb Promotion Recipe Plan

Keep the current Infusion-to-rank-I recipes unchanged:

```text
11x ooi + gmt -> ooc
11x ooi + gme -> ooa
```

Add rank promotion recipes:

```text
3x ooc -> oc2
9x ooc -> oc3
3x oc2 -> oc3

3x ooa -> oa2
9x ooa -> oa3
3x oa2 -> oa3
```

Eric wrote `9xOOC = 1x OC2`; Codex assumes that was a typo and that the intended direct shortcut is `9x OOC = 1x OC3`, matching `3x OC2 = 1x OC3`. Claude should flag this if the implementation should instead follow the literal text.

Round 2 status: this still needs Eric's explicit one-line confirmation before implementation. The design keeps `9x OOC -> OC3` and `9x OOA -> OA3` because literal `9x OOC -> OC2` would be a trap recipe that consumes three times the inputs of `3x OOC -> OC2` for the same output.

Use loose-item `qty` syntax, matching the existing supported `ooi,qty=11` recipe:

```text
input 1="ooc,qty=3" -> output=oc2, numinputs=3
input 1="ooc,qty=9" -> output=oc3, numinputs=9
input 1="oc2,qty=3" -> output=oc3, numinputs=3

input 1="ooa,qty=3" -> output=oa2, numinputs=3
input 1="ooa,qty=9" -> output=oa3, numinputs=9
input 1="oa2,qty=3" -> output=oa3, numinputs=3
```

Do not change the existing `11x ooi + topaz/emerald` rank-I recipes except for display descriptions if needed.

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

Proposed cube recipes, gated behind verification:

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

Implementation gate: split jewelry into a separate sub-step. First add a temporary/local test recipe or use a scratch branch to verify that fixed cube output `lvl=40` prevents higher-level unique/set jewelry outcomes. Do not include the final jewelry rank recipes in a publishable implementation until that behavior is confirmed. Armor/weapon tiering may proceed independently because it uses the existing `bas`/`exc`/`eli` pattern.

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

`Jewelry Orbs.NoDrop` is currently `0` in active `treasureclassex.txt`, and `Jewelry Orbs Single` / `Jewelry Orbs Stack` also have `NoDrop=0` in base. The drop-rate math therefore does not need to preserve a NoDrop weight.

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
Assemblage Orb Quest -> ooa weight 3, oa2 weight 2, oa3 weight 1
Conversion Orb Quest -> ooc weight 3, oc2 weight 2, oc3 weight 1
```

Point Mephistoq to `Assemblage Orb Quest` and Diabloq to `Conversion Orb Quest`. With `Picks=1` inside the selector, this gives absolute quest-orb probabilities of rank I = 1/2, rank II = 1/3, and rank III = 1/6, matching Eric's boss-specific request. Preserve the boss rows' existing `Picks=-2`; only change their orb Item reference to the new selector TC.

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
4. Confirm active/base `treasureclassex.txt` use the same orb TC structure after normalization.
5. Confirm the existing `11x ooi + gmt/gme` recipes still produce `ooc` and `ooa`.
6. Confirm rank promotion recipes:
   - `3x ooc -> oc2`
   - `9x ooc -> oc3`
   - `3x oc2 -> oc3`
   - `3x ooa -> oa2`
   - `9x ooa -> oa3`
   - `3x oa2 -> oa3`
7. Verify jewelry `lvl` gating before enabling final jewelry rank recipes.
8. In game, test:
   - Normal rare weapon/armor + rank I works.
   - Exceptional rare weapon/armor + rank I fails.
   - Exceptional rare weapon/armor + rank II works.
   - Elite rare weapon/armor + rank II fails.
   - Elite rare weapon/armor + rank III works.
   - Equivalent Assemblage tests for set output.
9. Test Mephisto and Diablo quest-drop behavior if quest selector TCs are implemented.
10. Run local install only after Claude approval and implementation.
