# Low-Level Set Item Buffs

Generated 2026-05-13. Third pass after flavor review.

Scope: low-level D2R Reimagined set items, mainly level requirement 25 or below, whose visible affix package was short and weak. Hidden `oskill_hide` plumbing is omitted from display summaries and was preserved in both TSV copies.

Third-pass rule: avoid simple increases to existing visible stats. Rows that were previously just bigger mana, resistance, hit recovery, block, enhanced damage, or similar numeric bumps were converted into flavor-forward affixes where sensible: cold/freeze hooks for Arctic and Grave items, poison/venom hooks for Iratha, radiant/undead hooks for Angelic/Civerb/Milabrega, and martial control such as crush, knockback, pierce, open wounds, or blind for weapon-facing sets.

| Item | Set | Req | Base | Third-Pass Change | Final Visible Affixes | Flavor Direction |
|---|---:|---:|---|---|---|---|
| Arctic Binding | Arctic Gear | 2 | Light Belt | prop3: mana -> half-freeze 1 | res-cold 40; ac 30; half-freeze 1 | Arctic identity: freeze mitigation instead of a mana pile. |
| Arctic Horn | Arctic Gear | 2 | Short War Bow | prop2: dmg% -> dmg% 50; prop5: empty slot -> pierce 20 | att% 20; dmg% 50; dmg-cold(75) 12-24; pierce 20 | Bow remains cold-themed, with pierce replacing raw ED inflation. |
| Arctic Mitts | Arctic Gear | 2 | Light Gauntlets | prop3: dex -> dmg-cold(75) 3-6 | hp 20; swing1 10; dmg-cold(75) 3-6 | Cold bite on attacks for the glove slot. |
| Berserker's Hatchet | Berserker's Arsenal | 3 | Double Axe | prop4: openwounds -> openwounds 25; prop6: empty slot -> crush 10 | att% 30; manasteal 5; openwounds 25; dmg% 90; crush 10 | Axe leans into savage wounds and crushing hits. |
| Berserker's Hauberk | Berserker's Arsenal | 3 | Splint Mail | prop3: hp -> thorns 8 | red-mag 2; bar 1; thorns 8; balance1 20 | Armor punishes attackers instead of just adding life. |
| Berserker's Headgear | Berserker's Arsenal | 3 | Helm | prop3: balance1 -> howl 15 | ac 15; res-fire 25; howl 15 | Fear-on-hit sells the berserker intimidation fantasy. |
| Hsarus' Iron Fist | Hsarus' Defense | 3 | Buckler | prop5: block1 -> crush 8 | red-dmg% 10; str 10; dmg% 25; crush 8 | Shield keeps the iron-fist fantasy through crushing melee impact. |
| Hsarus' Iron Heel | Hsarus' Defense | 3 | Chain Boots | prop3: balance1 -> stam 30 | res-fire 25; move2 20; stam 30 | Boots emphasize marching endurance. |
| Hsarus' Iron Stay | Hsarus' Defense | 3 | Belt | prop4: regen-stam -> red-dmg 2 | res-cold 20; hp 20; mana 20; red-dmg 2 | Belt becomes a physical brace. |
| Cleglaw's Claw | Cleglaw's Brace | 4 | Small Shield | prop4: block1 -> thorns 6 | ac 17; res-pois-len 75; thorns 6 | Shield gains claw-like retaliation. |
| Infernal Cranium | Infernal Tools | 5 | Cap | prop3: regen-mana -> dmg-fire 4-8 | res-all 10; dmg-to-mana 20; dmg-fire 4-8 | The skull now adds hellfire to attacks. |
| Infernal Sign | Infernal Tools | 5 | Heavy Belt | prop3: res-fire -> light-thorns 8 | ac 25; hp 20; light-thorns 8 | Belt mark burns attackers back. |
| Infernal Torch | Infernal Tools | 5 | Grim Wand | prop4: cast1 -> cast1 10; prop5: regen-mana -> mana-kill 4 | dmg-min 8; nec 1; cast1 10; mana-kill 4 | Caster sustain now comes from kills, not passive regen. |
| Death's Hand | Death's Disguise | 6 | Leather Gloves | prop3: swing1 -> noheal 1 | res-pois 50; res-pois-len 75; noheal 1 | Poison gloves now stop monster healing. |
| Death's Touch | Death's Disguise | 6 | War Sword | prop1: dmg% -> dmg% 25; prop4: deadly -> deadly 20; prop5: empty slot -> dmg-cold(75) 15-30 | dmg% 25; lifesteal 4; deadly 20; dmg-cold(75) 15-30 | Sword gets a cold death-touch rider rather than inflated ED. |
| Sigon's Gage | Sigon's Complete Steel | 6 | Gauntlets | prop3: swing1 -> crush 10 | str 10; att 20; crush 10 | Heavy steel gloves crush instead of merely swinging faster. |
| Sigon's Sabot | Sigon's Complete Steel | 6 | Greaves | prop3: balance1 -> stam 30 | move2 20; res-cold 40; stam 30 | Steel boots trade FHR for marching stamina. |
| Sigon's Shelter | Sigon's Complete Steel | 6 | Gothic Plate | prop3: hp -> red-dmg 3 | ac% 25; res-ltng 30; red-dmg 3 | Armor shelters through damage reduction. |
| Sigon's Visor | Sigon's Complete Steel | 6 | Great Helm | prop3: balance1 -> light 2 | mana 30; ac 25; light 2 | The visor gets a literal sight/light hook. |
| Sigon's Wrap | Sigon's Complete Steel | 6 | Plated Belt | prop3: res-ltng -> dmg-to-mana 15 | res-fire 20; hp 20; dmg-to-mana 15 | Belt turns incoming punishment into mana. |
| Bane's Authority | Bane's Garments | 8 | Light Belt | prop3: mana -> dmg-to-mana 15 | cast1 10; hp 20; dmg-to-mana 15 | Authority belt rewards taking hits as a caster. |
| Bane's Wraithskin | Bane's Garments | 8 | Hard Leather Armor | prop3: red-mag -> half-freeze 1 | ac 50; res-mag 30; half-freeze 1 | Ghostly armor resists freeze instead of adding numeric MDR. |
| Isenhart's Case | Isenhart's Armory | 8 | Breast Plate | prop4: hp -> red-dmg 3 | ac 40; red-mag 5; res-mag 10; red-dmg 3 | Chest armor protects with DR instead of flat life. |
| Isenhart's Horns | Isenhart's Armory | 8 | Full Helm | prop4: balance1 -> att-demon 75 | dex 10-15; red-dmg 5; dmg% 25; att-demon 75 | Horns become demon-hunting headgear. |
| Isenhart's Lightbrand | Isenhart's Armory | 8 | Broad Sword | prop5: dmg% -> dmg-ltng 1-30 | dmg-min 10-20; swing2 20; dmg-max 20-40; dmg-ltng 1-30 | Lightbrand now actually carries lightning damage. |
| Isenhart's Parry | Isenhart's Armory | 8 | Gothic Shield | prop5: block -> red-dmg 3 | ac 40; light-thorns 30; thorns 30; red-dmg 3 | Parry is represented as damage reduction. |
| Civerb's Cudgel | Civerb's Vestments | 9 | Grand Scepter | prop4: dmg% -> dmg-undead 100 | att 75; dmg-max 20-35; dmg-undead 100 | Holy scepter specializes into undead damage. |
| Civerb's Icon | Civerb's Vestments | 9 | Amulet | prop4: res-ltng -> light 2 | regen-mana 40; regen2 4; mana/lvl(16); light 2 | The icon glows rather than adding another resist. |
| Civerb's Ward | Civerb's Vestments | 9 | Large Shield | prop5: res-all -> red-dmg 3 | ac 25; block 15; block1 15; red-dmg 3 | Ward becomes a defensive damage reducer. |
| Corgina's Slippers | Corgina's Element | 9 | Boots | prop3: mana -> abs-cold% 3 | move2 20; balance2 20; abs-cold% 3 | Elemental boots gain cold absorb. |
| Grimlock's Belt | Grimlock's Grave | 9 | Belt | prop3: res-cold -> half-freeze 1 | hp 20-25; balance1 15; half-freeze 1 | Grave-cold belt halves freeze duration. |
| Jakira's Leather Jerkin | Midnight Calling | 9 | Studded Leather Armor | prop4: balance1 -> ac-miss 30 | ac 35-50; dex 15; str 15; ac-miss 30 | Midnight leather leans evasive against missiles. |
| Jakira's Braces | Midnight Calling | 10 | Chain Gloves | prop4: deadly -> openwounds 20 | swing1 10; ac% 75; hp 25-35; openwounds 20 | Braces cut and bleed rather than generic critting. |
| Janis' Gloves | Forgotten Treasures | 10 | Heavy Gloves | prop3: dex -> mag% 20 | ac 20-30; swing2 20; mag% 20 | Forgotten treasure slot gets magic find. |
| Luther's Cord | Forgotten Treasures | 10 | Heavy Belt | prop3: res-all -> gold% 50 | ac 20-30; regen 2-5; gold% 50 | Cord becomes the gold-hoarding part of the treasure set. |
| Sheena's Band | Sheena's Grace | 10 | Light Belt | prop3: regen-mana -> balance1 15 | hp% 5-10; mana 5-10; balance1 15 | Grace reads as recovery instead of mana regen. |
| The Raven's Talons | The Raven's Nest | 10 | Leather Gloves | prop4: mana-kill -> dmg-cold(50) 4-8 | cast2 5-10; res-all 5-10; all-stats 5-10; dmg-cold(50) 4-8 | Talons now carry a cold claw rider. |
| Cathan's Mesh | Cathan's Traps | 11 | Chain Mail | prop3: res-fire -> red-mag 3 | ac 15; ease -50; red-mag 3 | Mesh becomes light spell protection instead of another fire-resist bump. |
| Cathan's Rule | Cathan's Traps | 11 | Battle Staff | prop4: cast1 -> cast1 10; prop5: mana -> mana-kill 3; prop6: dmg% -> dmg-fire 8-16 | fireskill 1; fire-max 10; cast1 10; mana-kill 3; dmg-fire 8-16 | Fire staff gets fire damage and kill sustain. |
| Cathan's Seal | Cathan's Traps | 11 | Ring | prop3: hp -> dmg-fire 4-8 | lifesteal 6; red-dmg 2; dmg-fire 4-8 | Ring seal adds a fire damage rider. |
| Cathan's Sigil | Cathan's Traps | 11 | Amulet | prop3: res-ltng -> dmg-to-mana 20 | balance1 10; light-thorns 5; dmg-to-mana 20 | Sigil converts harm into mana for trap-caster play. |
| Cathan's Visage | Cathan's Traps | 11 | Mask | prop3: regen-mana -> dmg-fire 5-10 | mana 20; res-cold 25; dmg-fire 5-10 | Visage adds fire damage instead of mana regen. |
| Grimlock's Shroud | Grimlock's Grave | 11 | Quilted Armor | prop3: res-cold -> half-freeze 1 | red-dmg% 10; gethit-skill(Frost Nova) 15-2; half-freeze 1 | Shroud complements Frost Nova with half-freeze. |
| Angelic Halo | Angelic Raiment | 12 | Ring | prop3: att -> att-undead 75 | regen 6; hp 20; att-undead 75 | Halo targets undead rather than giving generic AR. |
| Angelic Mantle | Angelic Raiment | 12 | Ring Mail | prop3: res-ltng -> light-thorns 10 | red-dmg 3; ac% 40; light-thorns 10 | Mantle retaliates with radiant lightning damage. |
| Angelic Wings | Angelic Raiment | 12 | Amulet | prop3: cast1 -> move1 10 | light 3; dmg-to-mana 20; move1 10 | Wings add a small movement hook. |
| Greyhawk's Viser | Greyhawk's Mantle | 13 | Full Helm | prop3: res-cold -> dmg-cold(75) 4-8 | ac 20-30; manasteal 3-5; dmg-cold(75) 4-8 | Icy helm now adds cold damage. |
| Corgina's Ward | Corgina's Element | 14 | Large Shield | prop4: res-all -> abs-ltng% 3 | ac 20-30; block 15-25; abs-ltng% 3 | Elemental ward gets lightning absorb. |
| Ferrit's Paw | Silent Runnings | 14 | Heavy Gloves | prop3: openwounds -> knock 1 | swing2 20; lifesteal 4-6; knock 1 | Paw now knocks enemies back. |
| Sheena's Elven Mail | Sheena's Grace | 14 | Scale Mail | prop3: move1 -> balance1 15 | ac(0) 100-150; dex 15; balance1 15 | Elven grace becomes composed hit recovery. |
| Vidala's Ambush | Vidala's Rig | 14 | Leather Armor | prop4: move1 -> pierce 25 | ac 50; dex 10-15; noheal 1; pierce 25 | Ambush armor supports bow pierce. |
| Vidala's Barb | Vidala's Rig | 14 | Long Battle Bow | prop5: att% -> att% 40; prop6: dmg% -> pierce 25 | ltng-min 1; ltng-max 20-40; swing1 25; att% 40; pierce 25 | Lightning bow gets pierce instead of ED inflation. |
| Vidala's Fetlock | Vidala's Rig | 14 | Light Plated Boots | prop3: dex -> regen-stam 50 | move3 30; dmg-fire 10-20; regen-stam 50 | Boots emphasize long-chase stamina. |
| Vidala's Snare | Vidala's Rig | 14 | Amulet | prop4: mag% -> slow 10 | hp 15-30; res-cold 20; freeze 1; slow 10 | Snare amulet now actually slows targets. |
| Animal Kinship | Nature's Grove | 15 | Antlers | prop3: res-pois -> skill(Raven) 1 | ac 30-40; dru 1; skill(Raven) 1 | Druid pelt gains Raven to embody animal kinship. |
| Arcanna's Deathwand | Arcanna's Tricks | 15 | War Staff | prop4: cast1 -> cast1 10; prop5: dmg% -> dmg-mag 15-30 | sor 1; deadly 25; cast1 10; dmg-mag 15-30 | Staff adds magic damage rather than ED. |
| Arcanna's Flesh | Arcanna's Tricks | 15 | Light Plate | prop3: mana -> dmg-to-mana 20; prop4: res-all -> mag% 25 | light 2; red-dmg 3; dmg-to-mana 20; mag% 25 | Arcanna armor shifts to damage-to-mana and magic find tricks. |
| Arcanna's Head | Arcanna's Tricks | 15 | Skull Cap | prop3: cast1 -> mana-kill 3 | regen 4; thorns 2; mana-kill 3 | Skull cap gets mana on kill. |
| Arcanna's Sign | Arcanna's Tricks | 15 | Amulet | prop3: enr -> mag% 20 | mana 15; regen-mana 20; mag% 20 | Sign becomes a trickster magic-find amulet. |
| Beast Collar | Silent Runnings | 15 | Bone Helm | prop3: att% -> howl 20 | dmg% 20-30; dmg-mag 20-30; howl 20 | Collar intimidates on hit. |
| Corgina's Orb | Corgina's Element | 15 | Sacred Globe | prop4: cast1 -> cast1 10; prop5: regen-mana -> extra-ltng 10 | sor 1; mana-kill 2-4; cast1 10; extra-ltng 10 | Orb gets lightning skill damage for elemental identity. |
| Iratha's Coil | Iratha's Finery | 15 | Crown | prop3: res-cold -> res-pois-max 5 | res-fire 30; res-ltng 30; res-pois-max 5 | Crown deepens Iratha's poison-resist ceiling. |
| Iratha's Collar | Iratha's Finery | 15 | Amulet | prop3: res-all -> dmg-pois(75) 8-16 | res-pois 30; res-pois-len 75; dmg-pois(75) 8-16 | Collar becomes venomous rather than broadly resistant. |
| Iratha's Cord | Iratha's Finery | 15 | Heavy Belt | prop3: res-pois -> dmg-pois(75) 6-12 | ac 25; dmg-min 5; dmg-pois(75) 6-12 | Cord carries poison damage. |
| Iratha's Cuff | Iratha's Finery | 15 | Light Gauntlets | prop3: res-ltng -> dmg-pois(75) 8-16 | res-cold 30; half-freeze 1; dmg-pois(75) 8-16 | Cuff carries poison damage. |
| Xavier's Greaves | Forgotten Treasures | 15 | Light Plate Greaves | prop3: balance1 -> crush 10 | ac% 80-110; move2 30; crush 10 | Greaves hit hard enough to crush. |
| Grimlock's Skull | Grimlock's Grave | 16 | Zombie Head | prop4: res-pois -> thorns 8 | block 25-30; block1 20; thorns 8 | Zombie head gets bony retaliation. |
| Milabrega's Diadem | Milabrega's Regalia | 17 | Crown | prop3: regen-mana -> light 3 | hp 15; mana 15; light 3 | Regal diadem shines instead of regenerating mana. |
| Milabrega's Orb | Milabrega's Regalia | 17 | Kite Shield | prop4: block1 -> light-thorns 10 | mag% 20; ac 25; light-thorns 10 | Shield retaliates with holy light. |
| Milabrega's Robe | Milabrega's Regalia | 17 | Ancient Armor | prop3: res-all -> light-thorns 10 | thorns 3; red-dmg 2; light-thorns 10; balance1 20 | Robe keeps heavy-armor feel through radiant retaliation. |
| Milabrega's Rod | Milabrega's Regalia | 17 | War Scepter | prop2: dmg% -> dmg% 50; prop5: res-ltng -> dmg-undead 100 | pal 1; dmg% 50; light 2; dmg-undead 100 | Paladin rod returns to original ED and specializes vs undead. |
| Dragon's Flank | Silent Runnings | 18 | Bone Shield | prop4: block -> dmg-fire 6-12 | ac% 65-90; red-dmg% 5-10; dmg-fire 6-12 | Shield gets a small dragon-fire rider. |
| Greyhawk's Wing | Greyhawk's Mantle | 19 | Plate Mail | prop3: balance1 -> move1 10 | ac 75-100; res-ltng 15-20; move1 10 | Wing armor gets a light movement hook. |
| Tancred's Crowbill | Tancred's Battlegear | 20 | Military Pick | prop2: dmg% -> dmg% 80; prop4: deadly -> deadly 15; prop5: empty slot -> openwounds 25 | att 75; dmg% 80; deadly 15; openwounds 25 | Pick keeps original ED and gains bleeding flavor. |
| Tancred's Hobnails | Tancred's Battlegear | 20 | Boots | prop3: move1 -> crush 10 | regen-stam 25; dex 10; crush 10 | Hobnails crush instead of just running faster. |
| Tancred's Skull | Tancred's Battlegear | 20 | Bone Helm | prop3: balance1 -> deadly 10 | dmg% 10; att 40; deadly 10 | Battle helm gains deadly strike. |
| Tancred's Weird | Tancred's Battlegear | 20 | Amulet | prop3: res-all -> stupidity 1 | red-dmg 2; red-mag 1; stupidity 1; att 75 | Weird amulet blinds on hit. |
| Aviendha's Gift | Dragon Reborn | 21 | Heavy Boots | prop3: move2 -> regen-stam 50 | ac 25-35; dex 10; regen-stam 50 | Boots become desert-runner stamina gear. |
| Shattering Fist | Talonrage's Fury | 21 | Gauntlets | prop3: openwounds -> knock 1 | ac 20-30; crush 10; knock 1 | Gauntlets shatter enemies backward. |
| Holy Boots of Amaunator | Amaunator's Peace | 22 | Greaves | prop3: res-fire -> heal-kill 3 | ac/lvl(8); move2 20; heal-kill 3 | Sun-blessed boots heal after kills. |
| Jeweled Circlet | Snowmane's Jewelry | 22 | Circlet | prop3: mana -> mag% 25 | str 15; vit 15; mag% 25 | Jewelry slot gets magic find. |
| Sander's Paragon | Sander's Folly | 25 | Cap | prop4: balance1 -> stupidity 1 | mag% 35; thorns 8; ac/lvl(8); stupidity 1 | Folly cap blinds targets on hit. |

Ambiguous choices to revisit in playtesting: a few non-weapon armor pieces now carry attack riders such as `dmg-fire`, `dmg-cold`, `dmg-pois`, `stupidity`, or `howl`; these are valid item properties in the data and were chosen for flavor, but their practical value depends on how often the wearer attacks. `Animal Kinship` uses `skill(Raven)` because that pelt already targets Druids and the name strongly suggests a companion hook.
