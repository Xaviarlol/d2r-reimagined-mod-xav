# Low-Level Set Item Buffs

Generated 2026-05-13.

Scope: spawnable set items in D2R Reimagined with level requirement 25 or below that had short, low-impact visible affix lists. Hidden `oskill_hide` plumbing is intentionally omitted from the before/after text and was not removed.

Design rule: each selected item received one small thematic visible affix. I avoided changing set bonuses in this pass so the patch is easy to review and revert item-by-item.

| Item | Set | Req | Base | Added | Before | After | Rationale |
|---|---:|---:|---|---|---|---|---|
| Arctic Binding | Arctic Gear | 2 | Light Belt | mana 20 | res-cold 40; ac 30 | res-cold 40; ac 30; mana 20 | Keeps the cold-weather utility belt useful for early casters and bow builds. |
| Arctic Horn | Arctic Gear | 2 | Short War Bow | dmg-cold(75) 5-10 | att% 20; dmg% 50 | att% 20; dmg% 50; dmg-cold(75) 5-10 | Adds a small cold bite so the bow matches the Arctic theme. |
| Arctic Mitts | Arctic Gear | 2 | Light Gauntlets | dex 5-8 | hp 20; swing1 10 | hp 20; swing1 10; dex 5-8 | Adds light archer scaling without pushing raw damage too far. |
| Berserker's Hatchet | Berserker's Arsenal | 3 | Double Axe | openwounds 25 | att% 30; manasteal 5 | att% 30; manasteal 5; openwounds 25 | Leans into the reckless bleeding-axe fantasy. |
| Berserker's Hauberk | Berserker's Arsenal | 3 | Splint Mail | hp 30 | red-mag 2; bar 1 | red-mag 2; bar 1; hp 30 | Gives the low-level Barbarian chest some brawling durability. |
| Berserker's Headgear | Berserker's Arsenal | 3 | Helm | balance1 15 | ac 15; res-fire 25 | ac 15; res-fire 25; balance1 15 | Adds early hit recovery for a face-first melee set. |
| Hsarus' Iron Fist | Hsarus' Defense | 3 | Buckler | block1 10 | red-dmg% 10; str 10; dmg% 25 | red-dmg% 10; str 10; dmg% 25; block1 10 | Makes the buckler feel more like an aggressive defensive piece. |
| Hsarus' Iron Heel | Hsarus' Defense | 3 | Chain Boots | balance1 10 | res-fire 25; move2 20 | res-fire 25; move2 20; balance1 10 | Adds steadiness to the fast defensive boots. |
| Hsarus' Iron Stay | Hsarus' Defense | 3 | Belt | regen-stam 50 | res-cold 20; hp 20; mana 20 | res-cold 20; hp 20; mana 20; regen-stam 50 | Supports the marching/stamina flavor of Hsarus. |
| Cleglaw's Claw | Cleglaw's Brace | 4 | Small Shield | block1 15 | ac 17; res-pois-len 75 | ac 17; res-pois-len 75; block1 15 | Improves the shield side of Cleglaw's control set. |
| Infernal Cranium | Infernal Tools | 5 | Cap | regen-mana 20 | res-all 10; dmg-to-mana 20 | res-all 10; dmg-to-mana 20; regen-mana 20 | Adds low-level caster sustain to the necromantic helm. |
| Infernal Sign | Infernal Tools | 5 | Heavy Belt | res-fire 20 | ac 25; hp 20 | ac 25; hp 20; res-fire 20 | Matches the Infernal set theme and helps the belt compete. |
| Infernal Torch | Infernal Tools | 5 | Grim Wand | cast1 10 | dmg-min 8; nec 1 | dmg-min 8; nec 1; cast1 10 | Makes the wand feel like an actual starter caster weapon. |
| Death's Hand | Death's Disguise | 6 | Leather Gloves | swing1 10 | res-pois 50; res-pois-len 75 | res-pois 50; res-pois-len 75; swing1 10 | Adds a small tempo reward to the poison glove. |
| Death's Touch | Death's Disguise | 6 | War Sword | deadly 20 | dmg% 25; lifesteal 4 | dmg% 25; lifesteal 4; deadly 20 | Turns the sword into a sharper death-themed leveling weapon. |
| Sigon's Gage | Sigon's Complete Steel | 6 | Gauntlets | swing1 10 | str 10; att 20 | str 10; att 20; swing1 10 | Gives the gauntlets a little melee identity beyond stats. |
| Sigon's Sabot | Sigon's Complete Steel | 6 | Greaves | balance1 10 | move2 20; res-cold 40 | move2 20; res-cold 40; balance1 10 | Adds plated-footing stability to the boots. |
| Sigon's Shelter | Sigon's Complete Steel | 6 | Gothic Plate | hp 30 | ac% 25; res-ltng 30 | ac% 25; res-ltng 30; hp 30 | Adds survivability to a heavy early chest piece. |
| Sigon's Visor | Sigon's Complete Steel | 6 | Great Helm | balance1 10 | mana 30; ac 25 | mana 30; ac 25; balance1 10 | Adds some helmet-weight poise to a flat mana/defense piece. |
| Sigon's Wrap | Sigon's Complete Steel | 6 | Plated Belt | res-ltng 20 | res-fire 20; hp 20 | res-fire 20; hp 20; res-ltng 20 | Rounds out the defensive belt without changing its role. |
| Bane's Authority | Bane's Garments | 8 | Light Belt | mana 25 | cast1 10; hp 20 | cast1 10; hp 20; mana 25 | Supports the early spellcasting belt angle. |
| Bane's Wraithskin | Bane's Garments | 8 | Hard Leather Armor | red-mag 4 | ac 50; res-mag 30 | ac 50; res-mag 30; red-mag 4 | Reinforces the anti-magic shroud identity. |
| Isenhart's Case | Isenhart's Armory | 8 | Breast Plate | hp 30 | ac 40; red-mag 5; res-mag 10 | ac 40; red-mag 5; res-mag 10; hp 30 | Adds simple front-line durability to the breast plate. |
| Isenhart's Horns | Isenhart's Armory | 8 | Full Helm | balance1 15 | dex 10-15; red-dmg 5; dmg% 25 | dex 10-15; red-dmg 5; dmg% 25; balance1 15 | Makes the helm better for melee trading. |
| Isenhart's Lightbrand | Isenhart's Armory | 8 | Broad Sword | dmg% 40 | dmg-min 10-20; swing2 20; dmg-max 20-40 | dmg-min 10-20; swing2 20; dmg-max 20-40; dmg% 40 | Gives the sword enough enhanced damage to feel purposeful. |
| Isenhart's Parry | Isenhart's Armory | 8 | Gothic Shield | block 10 | ac 40; light-thorns 30; thorns 30 | ac 40; light-thorns 30; thorns 30; block 10 | Makes the shield better at actual parrying. |
| Civerb's Cudgel | Civerb's Vestments | 9 | Grand Scepter | dmg% 50 | att 75; dmg-max 20-35 | att 75; dmg-max 20-35; dmg% 50 | Improves the scepter's hit quality while keeping it blunt and simple. |
| Civerb's Icon | Civerb's Vestments | 9 | Amulet | res-ltng 25 | regen-mana 40; regen2 4; mana/lvl(16) | regen-mana 40; regen2 4; mana/lvl(16); res-ltng 25 | Adds a holy-protection angle to the amulet. |
| Civerb's Ward | Civerb's Vestments | 9 | Large Shield | res-all 10 | ac 25; block 15; block1 15 | ac 25; block 15; block1 15; res-all 10 | Makes the ward feel like broad early protection. |
| Corgina's Slippers | Corgina's Element | 9 | Boots | mana 20 | move2 20; balance2 20 | move2 20; balance2 20; mana 20 | Adds caster comfort to mobility boots. |
| Grimlock's Belt | Grimlock's Grave | 9 | Belt | res-cold 20 | hp 20-25; balance1 15 | hp 20-25; balance1 15; res-cold 20 | Adds grave-cold resistance to the defensive belt. |
| Jakira's Leather Jerkin | Midnight Calling | 9 | Studded Leather Armor | balance1 15 | ac 35-50; dex 15; str 15 | ac 35-50; dex 15; str 15; balance1 15 | Adds agile recovery to the Assassin armor. |
| Janis' Gloves | Forgotten Treasures | 10 | Heavy Gloves | dex 10 | ac 20-30; swing2 20 | ac 20-30; swing2 20; dex 10 | Adds hand-skill flavor to the attack-speed gloves. |
| Luther's Cord | Forgotten Treasures | 10 | Heavy Belt | res-all 10 | ac 20-30; regen 2-5 | ac 20-30; regen 2-5; res-all 10 | Turns a thin regen belt into a general-purpose leveling piece. |
| Jakira's Braces | Midnight Calling | 10 | Chain Gloves | deadly 15 | swing1 10; ac% 75; hp 25-35 | swing1 10; ac% 75; hp 25-35; deadly 15 | Adds precision lethality to the Assassin bracers. |
| Sheena's Band | Sheena's Grace | 10 | Light Belt | regen-mana 25 | hp% 5-10; mana 5-10 | hp% 5-10; mana 5-10; regen-mana 25 | Supports the Grace set's early resource sustain. |
| The Raven's Talons | The Raven's Nest | 10 | Leather Gloves | mana-kill 3 | cast2 5-10; res-all 5-10; all-stats 5-10 | cast2 5-10; res-all 5-10; all-stats 5-10; mana-kill 3 | Adds caster-on-kill sustain to the raven talon flavor. |
| Cathan's Mesh | Cathan's Traps | 11 | Chain Mail | res-fire 25 | ac 15; ease -50 | ac 15; ease -50; res-fire 25 | Adds fire protection to the fire-themed low caster set. |
| Cathan's Rule | Cathan's Traps | 11 | Battle Staff | cast1 10 | fireskill 1; fire-max 10 | fireskill 1; fire-max 10; cast1 10 | Makes the staff feel like a caster weapon instead of a fire stat stick. |
| Cathan's Seal | Cathan's Traps | 11 | Ring | hp 20 | lifesteal 6; red-dmg 2 | lifesteal 6; red-dmg 2; hp 20 | Adds blood-ring survivability to the leech ring. |
| Cathan's Sigil | Cathan's Traps | 11 | Amulet | res-ltng 25 | balance1 10; light-thorns 5 | balance1 10; light-thorns 5; res-ltng 25 | Builds on the crackling thorn/lightning identity. |
| Cathan's Visage | Cathan's Traps | 11 | Mask | regen-mana 20 | mana 20; res-cold 25 | mana 20; res-cold 25; regen-mana 20 | Makes the mask more comfortable for low-level casting. |
| Grimlock's Shroud | Grimlock's Grave | 11 | Quilted Armor | res-cold 25 | red-dmg% 10; gethit-skill(Frost Nova) 15-2 | red-dmg% 10; gethit-skill(Frost Nova) 15-2; res-cold 25 | Supports the Frost Nova retaliation flavor. |
| Angelic Halo | Angelic Raiment | 12 | Ring | att 50 | regen 6; hp 20 | regen 6; hp 20; att 50 | Restores some classic Angelic accuracy identity to the ring itself. |
| Angelic Mantle | Angelic Raiment | 12 | Ring Mail | res-ltng 20 | red-dmg 3; ac% 40 | red-dmg 3; ac% 40; res-ltng 20 | Adds a small angelic ward against lightning. |
| Angelic Wings | Angelic Raiment | 12 | Amulet | cast1 10 | light 3; dmg-to-mana 20 | light 3; dmg-to-mana 20; cast1 10 | Makes the amulet feel lighter and more magical. |
| Greyhawk's Viser | Greyhawk's Mantle | 13 | Full Helm | res-cold 20 | ac 20-30; manasteal 3-5 | ac 20-30; manasteal 3-5; res-cold 20 | Adds a hawk-like frost guard to the mana-steal helm. |
| Corgina's Ward | Corgina's Element | 14 | Large Shield | res-all 10 | ac 20-30; block 15-25 | ac 20-30; block 15-25; res-all 10 | Rounds the shield into a real elemental ward. |
| Sheena's Elven Mail | Sheena's Grace | 14 | Scale Mail | move1 15 | ac(0) 100-150; dex 15 | ac(0) 100-150; dex 15; move1 15 | Keeps the archer armor light on its feet. |
| Ferrit's Paw | Silent Runnings | 14 | Heavy Gloves | openwounds 20 | swing2 20; lifesteal 4-6 | swing2 20; lifesteal 4-6; openwounds 20 | Adds clawing bite to the lifesteal gloves. |
| Vidala's Ambush | Vidala's Rig | 14 | Leather Armor | move1 15 | ac 50; dex 10-15; noheal 1 | ac 50; dex 10-15; noheal 1; move1 15 | Makes the leather armor fit the ambush/ranger fantasy. |
| Vidala's Barb | Vidala's Rig | 14 | Long Battle Bow | att% 40 | ltng-min 1; ltng-max 20-40; swing1 25 | ltng-min 1; ltng-max 20-40; swing1 25; att% 40 | Improves the bow's reliability without spiking elemental damage. |
| Vidala's Fetlock | Vidala's Rig | 14 | Light Plated Boots | dex 10 | move3 30; dmg-fire 10-20 | move3 30; dmg-fire 10-20; dex 10 | Adds nimble archer scaling to the fire-step boots. |
| Vidala's Snare | Vidala's Rig | 14 | Amulet | mag% 20 | hp 15-30; res-cold 20; freeze 1 | hp 15-30; res-cold 20; freeze 1; mag% 20 | Adds treasure-hunter utility to the trapping amulet. |
| Arcanna's Deathwand | Arcanna's Tricks | 15 | War Staff | cast1 10 | sor 1; deadly 25 | sor 1; deadly 25; cast1 10 | Gives the staff a useful caster affix beside the odd Deadly Strike. |
| Arcanna's Flesh | Arcanna's Tricks | 15 | Light Plate | mana 25 | light 2; red-dmg 3 | light 2; red-dmg 3; mana 25 | Adds caster fuel to a very sparse armor. |
| Arcanna's Head | Arcanna's Tricks | 15 | Skull Cap | cast1 10 | regen 4; thorns 2 | regen 4; thorns 2; cast1 10 | Makes the skull cap support actual spell tempo. |
| Arcanna's Sign | Arcanna's Tricks | 15 | Amulet | enr 10 | mana 15; regen-mana 20 | mana 15; regen-mana 20; enr 10 | Adds arcane stat identity to the mana amulet. |
| Corgina's Orb | Corgina's Element | 15 | Sacred Globe | cast1 10 | sor 1; mana-kill 2-4 | sor 1; mana-kill 2-4; cast1 10 | Makes the orb a stronger starter Sorceress focus. |
| Xavier's Greaves | Forgotten Treasures | 15 | Light Plate Greaves | balance1 15 | ac% 80-110; move2 30 | ac% 80-110; move2 30; balance1 15 | Adds sturdy footwork to defensive greaves. |
| Iratha's Coil | Iratha's Finery | 15 | Crown | res-cold 20 | res-fire 30; res-ltng 30 | res-fire 30; res-ltng 30; res-cold 20 | Completes the elemental-resistance crown profile. |
| Iratha's Collar | Iratha's Finery | 15 | Amulet | res-all 10 | res-pois 30; res-pois-len 75 | res-pois 30; res-pois-len 75; res-all 10 | Makes the collar less poison-only and more broadly protective. |
| Iratha's Cord | Iratha's Finery | 15 | Heavy Belt | res-pois 20 | ac 25; dmg-min 5 | ac 25; dmg-min 5; res-pois 20 | Adds poison protection to the venom-themed belt. |
| Iratha's Cuff | Iratha's Finery | 15 | Light Gauntlets | res-ltng 20 | res-cold 30; half-freeze 1 | res-cold 30; half-freeze 1; res-ltng 20 | Broadens the elemental glove protection. |
| Animal Kinship | Nature's Grove | 15 | Antlers | res-pois 20 | ac 30-40; dru 1 | ac 30-40; dru 1; res-pois 20 | Adds natural resistance to the Druid pelt. |
| Beast Collar | Silent Runnings | 15 | Bone Helm | att% 30 | dmg% 20-30; dmg-mag 20-30 | dmg% 20-30; dmg-mag 20-30; att% 30 | Makes the beast helm better for hybrid physical/magic attacks. |
| Grimlock's Skull | Grimlock's Grave | 16 | Zombie Head | res-pois 20 | block 25-30; block1 20 | block 25-30; block1 20; res-pois 20 | Adds necromantic poison warding to the shrunken head. |
| Milabrega's Diadem | Milabrega's Regalia | 17 | Crown | regen-mana 25 | hp 15; mana 15 | hp 15; mana 15; regen-mana 25 | Adds priestly sustain to the crown. |
| Milabrega's Orb | Milabrega's Regalia | 17 | Kite Shield | block1 15 | mag% 20; ac 25 | mag% 20; ac 25; block1 15 | Makes the kite shield feel more like a shield, not just MF. |
| Milabrega's Robe | Milabrega's Regalia | 17 | Ancient Armor | res-all 10 | thorns 3; red-dmg 2 | thorns 3; red-dmg 2; res-all 10 | Gives the heavy robe a basic sacred ward. |
| Milabrega's Rod | Milabrega's Regalia | 17 | War Scepter | res-ltng 20 | pal 1; dmg% 50; light 2 | pal 1; dmg% 50; light 2; res-ltng 20 | Adds a holy lightning-protection note to the scepter. |
| Dragon's Flank | Silent Runnings | 18 | Bone Shield | block 10 | ac% 65-90; red-dmg% 5-10 | ac% 65-90; red-dmg% 5-10; block 10 | Makes the shield better at guarding the flank. |
| Greyhawk's Wing | Greyhawk's Mantle | 19 | Plate Mail | balance1 15 | ac 75-100; res-ltng 15-20 | ac 75-100; res-ltng 15-20; balance1 15 | Adds poise to the heavy lightning-resistant plate. |
| Tancred's Crowbill | Tancred's Battlegear | 20 | Military Pick | deadly 15 | att 75; dmg% 80 | att 75; dmg% 80; deadly 15 | Adds a hooked weapon payoff to the pick. |
| Tancred's Hobnails | Tancred's Battlegear | 20 | Boots | move1 20 | regen-stam 25; dex 10 | regen-stam 25; dex 10; move1 20 | Fixes the boots feeling like they forgot to be boots. |
| Tancred's Skull | Tancred's Battlegear | 20 | Bone Helm | balance1 15 | dmg% 10; att 40 | dmg% 10; att 40; balance1 15 | Adds front-line grit to the bone helm. |
| Tancred's Weird | Tancred's Battlegear | 20 | Amulet | res-all 10 | red-dmg 2; red-mag 1 | red-dmg 2; red-mag 1; res-all 10 | Makes the strange amulet a broader warding piece. |
| Aviendha's Gift | Dragon Reborn | 21 | Heavy Boots | move2 20 | ac 25-35; dex 10 | ac 25-35; dex 10; move2 20 | Makes the boots feel like an actual gift for traveling. |
| Shattering Fist | Talonrage's Fury | 21 | Gauntlets | openwounds 20 | ac 20-30; crush 10 | ac 20-30; crush 10; openwounds 20 | Adds a second melee payoff next to Crushing Blow. |
| Holy Boots of Amaunator | Amaunator's Peace | 22 | Greaves | res-fire 20 | ac/lvl(8); move2 20 | ac/lvl(8); move2 20; res-fire 20 | Adds sun-god fire protection to the holy boots. |
| Jeweled Circlet | Snowmane's Jewelry | 22 | Circlet | mana 25 | str 15; vit 15 | str 15; vit 15; mana 25 | Adds jewel-like caster utility to the stat circlet. |
| Sander's Paragon | Sander's Folly | 25 | Cap | balance1 15 | mag% 35; thorns 8; ac/lvl(8) | mag% 35; thorns 8; ac/lvl(8); balance1 15 | Adds practical recovery to an otherwise MF/thorns cap. |

Review notes:
- The pass is intentionally conservative: mostly +10-25 utility stats, small recovery, small resists, or one modest combat proc/stat.
- A few class-skill pieces were included when their other affixes were effectively dead for the item role, such as Arcanna's Deathwand and Infernal Torch.
- Follow-up tuning should test Normal Act 1-3 pacing and twinked level 2-20 starts, since these items mostly affect early game feel.
