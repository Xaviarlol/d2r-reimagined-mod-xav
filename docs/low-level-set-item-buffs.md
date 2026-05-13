# Low-Level Set Item Buffs

Generated 2026-05-14. Fourth additive pass after comparing low-level set items against low-level unique item power.

Scope: low-level D2R Reimagined set items, mainly level requirement 25 or below, whose visible affix package was short or weak. Hidden `oskill_hide` plumbing is omitted from display summaries and was preserved in both TSV copies.

Fourth-pass rule: add power instead of swapping it sideways. The prior practical baseline from the pre-flavor pass was restored where it had been replaced, and the newer flavorful affixes were retained in extra visible slots when space allowed. Low-level uniques in this mod commonly carry strong packages very early, including 70-150% enhanced damage, crushing blow, open wounds, leech, sockets, movement, cast speed, regen, resists, skill hooks, and flat elemental/magic damage on caster weapons, so these set pieces should now feel closer to that baseline while still depending on set completion for their larger bonuses.

Validation: active and base `setitems.txt` were updated symmetrically, with all rows keeping the expected TSV column count.

| Item | Set | Req | Base | Final Visible Affixes |
|---|---:|---:|---|---|
| Arctic Binding | Arctic Gear | 2 | Light Belt | res-cold 40; ac 30; mana 40; half-freeze 1 |
| Arctic Horn | Arctic Gear | 2 | Short War Bow | att% 20; dmg% 90; dmg-cold(75) 12-24; pierce 20 |
| Arctic Mitts | Arctic Gear | 2 | Light Gauntlets | hp 20; swing1 10; dex 10-15; dmg-cold(75) 3-6 |
| Berserker's Hatchet | Berserker's Arsenal | 3 | Double Axe | att% 30; manasteal 5; openwounds 35; dmg% 90; crush 10 |
| Berserker's Hauberk | Berserker's Arsenal | 3 | Splint Mail | red-mag 2; bar 1; hp 45; balance1 20; thorns 8 |
| Berserker's Headgear | Berserker's Arsenal | 3 | Helm | ac 15; res-fire 25; balance1 20; howl 15 |
| Hsarus' Iron Fist | Hsarus' Defense | 3 | Buckler | red-dmg% 10; str 10; dmg% 25; block1 20; crush 8 |
| Hsarus' Iron Heel | Hsarus' Defense | 3 | Chain Boots | res-fire 25; move2 20; balance1 20; stam 30 |
| Hsarus' Iron Stay | Hsarus' Defense | 3 | Belt | res-cold 20; hp 20; mana 20; regen-stam 75; red-dmg 2 |
| Cleglaw's Claw | Cleglaw's Brace | 4 | Small Shield | ac 17; res-pois-len 75; block1 20; thorns 6 |
| Infernal Cranium | Infernal Tools | 5 | Cap | res-all 10; dmg-to-mana 20; regen-mana 35; dmg-fire 4-8 |
| Infernal Sign | Infernal Tools | 5 | Heavy Belt | ac 25; hp 20; res-fire 30; light-thorns 8 |
| Infernal Torch | Infernal Tools | 5 | Grim Wand | dmg-min 8; nec 1; cast1 20; regen-mana 35; mana-kill 4 |
| Death's Hand | Death's Disguise | 6 | Leather Gloves | res-pois 50; res-pois-len 75; swing1 20; noheal 1 |
| Death's Touch | Death's Disguise | 6 | War Sword | dmg% 85; lifesteal 4; deadly 25; dmg-cold(75) 15-30 |
| Sigon's Gage | Sigon's Complete Steel | 6 | Gauntlets | str 10; att 20; swing1 20; crush 10 |
| Sigon's Sabot | Sigon's Complete Steel | 6 | Greaves | move2 20; res-cold 40; balance1 20; stam 30 |
| Sigon's Shelter | Sigon's Complete Steel | 6 | Gothic Plate | ac% 25; res-ltng 30; hp 45; red-dmg 3 |
| Sigon's Visor | Sigon's Complete Steel | 6 | Great Helm | mana 30; ac 25; balance1 20; light 2 |
| Sigon's Wrap | Sigon's Complete Steel | 6 | Plated Belt | res-fire 20; hp 20; res-ltng 30; dmg-to-mana 15 |
| Bane's Authority | Bane's Garments | 8 | Light Belt | cast1 10; hp 20; mana 40; dmg-to-mana 15 |
| Bane's Wraithskin | Bane's Garments | 8 | Hard Leather Armor | ac 50; res-mag 30; red-mag 7; half-freeze 1 |
| Isenhart's Case | Isenhart's Armory | 8 | Breast Plate | ac 40; red-mag 5; res-mag 10; hp 45; red-dmg 3 |
| Isenhart's Horns | Isenhart's Armory | 8 | Full Helm | dex 10-15; red-dmg 5; dmg% 25; balance1 20; att-demon 75 |
| Isenhart's Lightbrand | Isenhart's Armory | 8 | Broad Sword | dmg-min 10-20; swing2 20; dmg-max 20-40; dmg% 95; dmg-ltng 1-30 |
| Isenhart's Parry | Isenhart's Armory | 8 | Gothic Shield | ac 40; light-thorns 30; thorns 30; block 15; red-dmg 3 |
| Civerb's Cudgel | Civerb's Vestments | 9 | Grand Scepter | att 75; dmg-max 20-35; dmg% 95; dmg-undead 100 |
| Civerb's Icon | Civerb's Vestments | 9 | Amulet | regen-mana 40; regen2 4; mana/lvl(16); res-ltng 30; light 2 |
| Civerb's Ward | Civerb's Vestments | 9 | Large Shield | ac 25; block 15; block1 15; res-all 15; red-dmg 3 |
| Corgina's Slippers | Corgina's Element | 9 | Boots | move2 20; balance2 20; mana 40; abs-cold% 3 |
| Grimlock's Belt | Grimlock's Grave | 9 | Belt | hp 20-25; balance1 15; res-cold 30; half-freeze 1 |
| Jakira's Leather Jerkin | Midnight Calling | 9 | Studded Leather Armor | ac 35-50; dex 15; str 15; balance1 20; ac-miss 30 |
| Jakira's Braces | Midnight Calling | 10 | Chain Gloves | swing1 10; ac% 75; hp 25-35; deadly 25; openwounds 20 |
| Janis' Gloves | Forgotten Treasures | 10 | Heavy Gloves | ac 20-30; swing2 20; dex 10-15; mag% 20 |
| Luther's Cord | Forgotten Treasures | 10 | Heavy Belt | ac 20-30; regen 2-5; res-all 15; gold% 50 |
| Sheena's Band | Sheena's Grace | 10 | Light Belt | hp% 5-10; mana 5-10; regen-mana 35; balance1 15 |
| The Raven's Talons | The Raven's Nest | 10 | Leather Gloves | cast2 5-10; res-all 5-10; all-stats 5-10; mana-kill 5; dmg-cold(50) 4-8 |
| Cathan's Mesh | Cathan's Traps | 11 | Chain Mail | ac 15; ease -50; res-fire 30; red-mag 3 |
| Cathan's Rule | Cathan's Traps | 11 | Battle Staff | fireskill 1; fire-max 10; cast1 20; mana 40; dmg% 75; mana-kill 3; dmg-fire 8-16 |
| Cathan's Seal | Cathan's Traps | 11 | Ring | lifesteal 6; red-dmg 2; hp 45; dmg-fire 4-8 |
| Cathan's Sigil | Cathan's Traps | 11 | Amulet | balance1 10; light-thorns 5; res-ltng 30; dmg-to-mana 20 |
| Cathan's Visage | Cathan's Traps | 11 | Mask | mana 20; res-cold 25; regen-mana 35; dmg-fire 5-10 |
| Grimlock's Shroud | Grimlock's Grave | 11 | Quilted Armor | red-dmg% 10; gethit-skill(Frost Nova) 15-2; res-cold 30; half-freeze 1 |
| Angelic Halo | Angelic Raiment | 12 | Ring | regen 6; hp 20; att 75; att-undead 75 |
| Angelic Mantle | Angelic Raiment | 12 | Ring Mail | red-dmg 3; ac% 40; res-ltng 30; light-thorns 10 |
| Angelic Wings | Angelic Raiment | 12 | Amulet | light 3; dmg-to-mana 20; cast1 20; move1 10 |
| Greyhawk's Viser | Greyhawk's Mantle | 13 | Full Helm | ac 20-30; manasteal 3-5; res-cold 30; dmg-cold(75) 4-8 |
| Corgina's Ward | Corgina's Element | 14 | Large Shield | ac 20-30; block 15-25; res-all 15; abs-ltng% 3 |
| Ferrit's Paw | Silent Runnings | 14 | Heavy Gloves | swing2 20; lifesteal 4-6; openwounds 35; knock 1 |
| Sheena's Elven Mail | Sheena's Grace | 14 | Scale Mail | ac(0) 100-150; dex 15; move1 25; balance1 15 |
| Vidala's Ambush | Vidala's Rig | 14 | Leather Armor | ac 50; dex 10-15; noheal 1; move1 25; pierce 25 |
| Vidala's Barb | Vidala's Rig | 14 | Long Battle Bow | ltng-min 1; ltng-max 20-40; swing1 25; att% 50; dmg% 95; pierce 25 |
| Vidala's Fetlock | Vidala's Rig | 14 | Light Plated Boots | move3 30; dmg-fire 10-20; dex 10-15; regen-stam 50 |
| Vidala's Snare | Vidala's Rig | 14 | Amulet | hp 15-30; res-cold 20; freeze 1; mag% 35; slow 10 |
| Animal Kinship | Nature's Grove | 15 | Antlers | ac 30-40; dru 1; res-pois 30; skill(Raven) 1 |
| Arcanna's Deathwand | Arcanna's Tricks | 15 | War Staff | sor 1; deadly 25; cast1 20; dmg% 85; dmg-mag 15-30 |
| Arcanna's Flesh | Arcanna's Tricks | 15 | Light Plate | light 2; red-dmg 3; mana 40; res-all 15; dmg-to-mana 20; mag% 25 |
| Arcanna's Head | Arcanna's Tricks | 15 | Skull Cap | regen 4; thorns 2; cast1 20; mana-kill 3 |
| Arcanna's Sign | Arcanna's Tricks | 15 | Amulet | mana 15; regen-mana 20; enr 15; mag% 20 |
| Beast Collar | Silent Runnings | 15 | Bone Helm | dmg% 20-30; dmg-mag 20-30; att% 50; howl 20 |
| Corgina's Orb | Corgina's Element | 15 | Sacred Globe | sor 1; mana-kill 2-4; cast1 20; regen-mana 35; extra-ltng 10; dmg-ltng 1-40 |
| Iratha's Coil | Iratha's Finery | 15 | Crown | res-fire 30; res-ltng 30; res-cold 30; res-pois-max 5 |
| Iratha's Collar | Iratha's Finery | 15 | Amulet | res-pois 30; res-pois-len 75; res-all 15; dmg-pois(75) 8-16 |
| Iratha's Cord | Iratha's Finery | 15 | Heavy Belt | ac 25; dmg-min 5; res-pois 30; dmg-pois(75) 6-12 |
| Iratha's Cuff | Iratha's Finery | 15 | Light Gauntlets | res-cold 30; half-freeze 1; res-ltng 30; dmg-pois(75) 8-16 |
| Xavier's Greaves | Forgotten Treasures | 15 | Light Plate Greaves | ac% 80-110; move2 30; balance1 20; crush 10 |
| Grimlock's Skull | Grimlock's Grave | 16 | Zombie Head | block 25-30; block1 20; res-pois 30; thorns 8 |
| Grimlock's Wand | Grimlock's Grave | 15 | Bone Wand | nec 1; mana 33; cast1 20; dmg-mag 15-30 |
| Milabrega's Diadem | Milabrega's Regalia | 17 | Crown | hp 15; mana 15; regen-mana 35; light 3 |
| Milabrega's Orb | Milabrega's Regalia | 17 | Kite Shield | mag% 20; ac 25; block1 20; light-thorns 10 |
| Milabrega's Robe | Milabrega's Regalia | 17 | Ancient Armor | thorns 3; red-dmg 2; res-all 15; balance1 20; light-thorns 10 |
| Milabrega's Rod | Milabrega's Regalia | 17 | War Scepter | pal 1; dmg% 100; light 2; res-ltng 30; dmg-undead 100 |
| Dragon's Flank | Silent Runnings | 18 | Bone Shield | ac% 65-90; red-dmg% 5-10; block 15; dmg-fire 6-12 |
| Greyhawk's Wing | Greyhawk's Mantle | 19 | Plate Mail | ac 75-100; res-ltng 15-20; balance1 20; move1 10 |
| Tancred's Crowbill | Tancred's Battlegear | 20 | Military Pick | att 75; dmg% 125; deadly 25; openwounds 25 |
| Tancred's Hobnails | Tancred's Battlegear | 20 | Boots | regen-stam 25; dex 10; move1 25; crush 10 |
| Tancred's Skull | Tancred's Battlegear | 20 | Bone Helm | dmg% 10; att 40; balance1 20; deadly 10 |
| Tancred's Weird | Tancred's Battlegear | 20 | Amulet | red-dmg 2; red-mag 1; res-all 15; att 75; stupidity 1 |
| Aviendha's Gift | Dragon Reborn | 21 | Heavy Boots | ac 25-35; dex 10; move2 25; regen-stam 50 |
| Shattering Fist | Talonrage's Fury | 21 | Gauntlets | ac 20-30; crush 10; openwounds 35; knock 1 |
| Holy Boots of Amaunator | Amaunator's Peace | 22 | Greaves | ac/lvl(8); move2 20; res-fire 30; heal-kill 3 |
| Jeweled Circlet | Snowmane's Jewelry | 22 | Circlet | str 15; vit 15; mana 40; mag% 25 |
| Sander's Paragon | Sander's Folly | 25 | Cap | mag% 35; thorns 8; ac/lvl(8); balance1 20; stupidity 1 |
