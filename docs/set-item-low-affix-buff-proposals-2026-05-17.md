# Set Item Low-Affix Buff Proposals

Generated 2026-05-17.

Scope: every spawnable, enabled row in `data/global/excel/setitems.txt` with 3 or fewer visible item-level affixes. Hidden plumbing such as `oskill_hide` is excluded from the count. Set completion and partial-set bonus columns (`aprop*`) are not counted, because this pass is about the item standing on its own before set bonuses.

Implementation status: approved buffs were applied to `data/global/excel/setitems.txt` and `data/global/excel/base/setitems.txt` on 2026-05-17, excluding the 13 items listed below. `Mystic Blades` also had its malformed `block1` / `dmg-mag` property slots repaired before the approved buffs were added.

Excluded from implementation:

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

Design target:

- Bring sparse set pieces closer to the mod's current unique-item density without erasing set identity.
- Prefer additive flavour buffs over replacing existing affixes.
- Keep low-level pieces modest and high-level pieces more complete.
- Avoid making single sparse pieces carry the whole set when their current affix is already very strong, such as sockets or `allskills`.

Implementation note:

- `Mystic Blades` appears to have a malformed item-property area: `prop3=block1`, `par3=30`, `min3=30`, `max3=dmg-mag`, then `prop4` is blank while `par4=25` and `min4=50`. Before implementing its proposed buff, repair that row so the likely intended `dmg-mag 25-50` lands in a valid property slot.

## Summary

| Current visible affix count | Item count |
|---:|---:|
| 1 | 6 |
| 2 | 44 |
| 3 | 56 |
| Total | 106 |

## Early And Low-Level Items

| Item | Set | Req | Base | Before | Proposed after | Flavour |
|---|---|---:|---|---|---|---|
| Cleglaw's Tooth | Cleglaw's Brace | 4 | Long Sword | `att% 30; deadly 50; dmg% 90` | `att% 30; deadly 50; dmg% 90; +swing1 20; +openwounds 25` | Dirty duelist blade, fast cuts and bleeding pressure. |
| Cleglaw's Pincers | Cleglaw's Brace | 4 | Chain Gloves | `knock 1; slow 25` | `knock 1; slow 25; +crush 10; +att 50; +str 10` | Grappling gauntlets that shove, stagger, and overpower. |
| Tancred's Spine | Tancred's Battlegear | 20 | Full Plate Mail | `hp 40; str 15` | `hp 40; str 15; +ac% 100; +balance1 20; +red-dmg 4` | Heavy battlegear should feel like a sturdy spine, not just stat padding. |
| Sigon's Guard | Sigon's Complete Steel | 6 | Tower Shield | `allskills 1; block 20` | `allskills 1; block 20; +block1 20; +res-all 15; +red-dmg 3` | Classic knight shield, broader guard package. |
| Death's Guard | Death's Disguise | 6 | Sash | `ac 20; nofreeze 1` | `ac 20; nofreeze 1; +res-cold 40; +hp 25; +red-dmg 3` | Death's cold refusal made into a true defensive sash. |
| Arctic Furs | Arctic Gear | 2 | Quilted Armor | `ac% 275-325; res-all 10` | `ac% 275-325; res-all 10; +res-cold 35; +half-freeze 1; +hp 20` | Warm starter armor with a stronger cold-weather identity. |
| Rite of Passage | The Disciple | 29 | Demonhide Boots | `ac 25; move3 30; half-freeze 1` | `ac 25; move3 30; half-freeze 1; +regen-stam 75; +res-cold 35` | Pilgrim boots built for long, cold travel. |
| Bane's Oathmaker | Bane's Garments | 8 | Kriss | `move1 20; dmg/lvl(8); dmg% 80` | `move1 20; dmg/lvl(8); dmg% 80; +deadly 20; +mana-kill 3; +dmg-pois(75) 25-40` | Quick oath-dagger with a spiteful venom edge. |
| Jakira's Strike | Midnight Calling | 12 | Hatchet hands | `dmg% 120; lifesteal 5` | `dmg% 120; lifesteal 5; +ass 1; +swing1 20; +openwounds 25` | Assassin claws should reward aggressive, bloody tempo. |
| Jakira's Hood | Midnight Calling | 5 | Skull Cap | `ass 1; ac 15-25; mana 20-30` | `ass 1; ac 15-25; mana 20-30; +cast1 15; +res-all 10` | Midnight caller hood, more nimble and occult. |
| Peace Ring | Nature's Grove | 12 | Ring | `mana 40-50; hp 40-50` | `mana 40-50; hp 40-50; +regen 5; +regen-mana 40; +res-pois 25` | Grove calm through recovery and natural protection. |
| Balance of Power | Nature's Grove | 18 | Maul | `dmg% 140-200; swing1 15` | `dmg% 140-200; swing1 15; +crush 20; +att% 50; +dmg-norm 20-40` | The maul should land with balanced but serious force. |
| Calming Embrace | Nature's Grove | 7 | Hard Leather Armor | `ac% 80-120; skilltab(15) 1-3` | `ac% 80-120; skilltab(15) 1-3; +hp 30; +res-pois 30; +balance1 15` | Protective druidic hide with poison/nature resilience. |
| Corgina's Plate | Corgina's Element | 21 | Light Plate | `ac% 75-105; res-all 20` | `ac% 75-105; res-all 20; +mana 40; +cast1 10; +res-ltng 25` | Elemental caster armor, leaning into charged protection. |
| Sheena's Heartwood | Sheena's Grace | 15 | Stag Bow | `dmg-norm 15-30; openwounds 35-55; dmg% 95` | `dmg-norm 15-30; openwounds 35-55; dmg% 95; +swing1 20; +pierce 25` | Graceful bow, faster shots and cleaner penetration. |
| Sheena's Choker | Sheena's Grace | 12 | Amulet | `allskills 1` | `allskills 1; +dex 15; +mag% 25; +res-all 15` | Ranger charm with poise, luck, and a little protection. |
| Berserker's Howl | Talonrage's Fury | 18 | Assault Helmet | `bar 1; oskill(Terror) 1` | `bar 1; oskill(Terror) 1; +hp 40; +balance1 20; +dmg% 20` | Screaming helm for reckless front-line pressure. |
| Chaos Heart | Talonrage's Fury | 22 | Field Plate | `ac% 90-120; sock 2` | `ac% 90-120; sock 2; +bar 1; +res-fire 30; +hp 45` | Barbarian chaos armor, hot-blooded and socket friendly. |
| Warlord's Pike | Talonrage's Fury | 20 | Pike | `dmg% 110-140; rep-dur(5)` | `dmg% 110-140; rep-dur(5); +swing2 30; +att% 75; +dmg-norm 25-55` | Warlord reach weapon that actually keeps pace. |
| Greyhawk's Icebrand | Greyhawk's Mantle | 14 | Scepter | `dmg% 80-120; dmg-cold(100) 10-20` | `dmg% 80-120; dmg-cold(100) 10-20; +pal 1; +freeze 1; +dmg-cold(100) 25-50` | Paladin icebrand with a real chill theme. |
| Greyhawk's Deflector | Greyhawk's Mantle | 15 | Heraldic Shield | `sock 1-4; block 15` | `sock 1-4; block 15; +block1 25; +res-cold 35; +dmg-cold(75) 5-12` | Cold paladin shield that deflects and punishes. |
| Turtle's Shell | Silent Runnings | 23 | Full Plate Mail | `ac% 90-130; balance2 20` | `ac% 90-130; balance2 20; +red-dmg% 10; +hp 60; +res-all 15` | Slow shell armor should be meaningfully hard to crack. |
| Wolf Pelt | Silent Runnings | 14 | Heavy Belt | `hp 35-50; res-all 10-15` | `hp 35-50; res-all 10-15; +dru 1; +move1 10; +regen 5` | Wolfish belt with mobility and feral recovery. |
| Jeweled Belt | Snowmane's Jewelry | 22 | Plated Belt | `ac% 100-125; res-all 10-15` | `ac% 100-125; res-all 10-15; +mag% 35; +gold% 75; +all-stats 8` | Treasure belt should sparkle mechanically too. |
| Ruby Ring | Snowmane's Jewelry | 22 | Ring | `res-all 10-15; red-mag 6-8` | `res-all 10-15; red-mag 6-8; +res-fire 25; +hp 40; +dmg-fire 8-16` | Ruby accent: warmth, life, and small fire damage. |
| Diamond Necklace | Snowmane's Jewelry | 22 | Amulet | `res-all 15-20; mag% 20-30` | `res-all 15-20; mag% 20-30; +light 3; +all-stats 8; +mana 30` | Diamond clarity, utility, and clean magic-find flavour. |
| Winter's Heart | Four Seasons | 25 | Ancient Armor | `pierce-cold 10-15; extra-cold 10-15` | `pierce-cold 10-15; extra-cold 10-15; +res-cold 40; +abs-cold% 5; +dmg-cold(100) 30-60` | Winter armor should both amplify and endure cold. |
| Spring Dawning | Four Seasons | 22 | Great Helm | `pierce-ltng 10-15; extra-ltng 10-15` | `pierce-ltng 10-15; extra-ltng 10-15; +res-ltng 40; +abs-ltng% 5; +dmg-ltng 1-80` | Spring lightning, bright and volatile. |
| Summer Flame | Four Seasons | 21 | Greaves | `pierce-fire 10-15; extra-fire 10-15` | `pierce-fire 10-15; extra-fire 10-15; +res-fire 40; +abs-fire% 5; +dmg-fire 25-50` | Summer heat on both offense and defense. |
| Autumn's Decay | Four Seasons | 19 | Light Gauntlets | `pierce-pois 10-15; extra-pois 10-15` | `pierce-pois 10-15; extra-pois 10-15; +res-pois 40; +res-pois-len 50; +dmg-pois(100) 80-120` | Autumn rot, poison power, and poison discipline. |
| Fernandez' Plate | Forgotten Treasures | 15 | Breast Plate | `ac% 75-120; sock 3` | `ac% 75-120; sock 3; +mag% 35; +gold% 100; +res-all 15` | Treasure armor, lucky and practical. |
| Katriana's Mask | Forgotten Treasures | 15 | Mask | `ac% 60-100; sock 3` | `ac% 60-100; sock 3; +mag% 30; +all-stats 10; +light 2` | Relic mask with jewel utility and explorer flavour. |

## Midgame Items

| Item | Set | Req | Base | Before | Proposed after | Flavour |
|---|---|---:|---|---|---|---|
| Afterlife | Hades' Underworld | 34 | Demonhide Armor | `ac/lvl(32); skilltab(8) 1-3; res-ltng 25-40` | `ac/lvl(32); skilltab(8) 1-3; res-ltng 25-40; +cast2 20; +mana 60` | Underworld caster armor with more necromantic throughput. |
| Dracolich | Hades' Underworld | 36 | Sexton Trophy | `block 20-30; ac/lvl(16); res-fire 25-40` | `block 20-30; ac/lvl(16); res-fire 25-40; +nec 1; +dmg-fire 25-45` | Dragon-lich trophy, fire memory and necromancer focus. |
| The River Stix | Hades' Underworld | 32 | Demonhide Boots | `ac/lvl(8); move3 30; res-cold 25-40` | `ac/lvl(8); move3 30; res-cold 25-40; +res-pois 35; +regen-stam 75` | Crossing the Stix: cold, poison, and relentless travel. |
| Lord Hades' Throne | Hades' Underworld | 41 | Grand Crown | `ac% 100; balance2 20; res-pois 25-40` | `ac% 100; balance2 20; res-pois 25-40; +nec 2; +red-dmg% 10` | A death-lord crown should command and endure. |
| Fallen Angels | Darque's Cabal | 43 | Embossed Armor | `ac% 180-220; res-all 20-30; sock 1` | `ac% 180-220; res-all 20-30; sock 1; +cast2 20; +red-mag 10` | Cabal armor, dark casting and warding. |
| Savant Fury | Darque's Cabal | 42 | Executionor Sword | `dmg% 220-300; indestruct 1` | `dmg% 220-300; indestruct 1; +swing3 40; +dmg-mag 75-125; +manasteal 7` | Smart rage: fast, unbreakable, and arcane. |
| Dawn's Blessing | Darque's Cabal | 41 | Ancient Shield | `block 25-35; balance2 25; dmg% 35-50` | `block 25-35; balance2 25; dmg% 35-50; +res-all 25; +red-dmg% 10` | Dawn shield that blesses survival, not just bashing. |
| Cry of the Wolf | Red Havoc's Challenge | 35 | Tigulated Mail | `charged(Summon Fenris) 8-35; ac%/lvl(16); move2 20` | `charged(Summon Fenris) 8-35; ac%/lvl(16); move2 20; +dru 2; +balance2 20` | Wolf-call armor for a mobile shapeshifter/summoner. |
| Trent's Caster | Mishy's Avatar | 40 | Ceremonial Bow | `dmg% 170-210; swing2 20; sock 3` | `dmg% 170-210; swing2 20; sock 3; +ama 1; +pierce 35` | Amazon caster-bow hybrid, socketed and piercing. |
| Night's Caress | JBouley's Scion | 32 | Demonhide Gloves | `ac/lvl(16); swing2 20; dmg/lvl(8)` | `ac/lvl(16); swing2 20; dmg/lvl(8); +lifesteal 8; +openwounds 25` | Night touch, fast strikes that drain and bleed. |
| Mystic Blades | JBouley's Scion | 35 | Barbed Shield | `dmg% 50; swing2 25; malformed block1/dmg-mag slot` | `dmg% 50; swing2 25; repaired block1 30; repaired dmg-mag 25-50; +block 20; +lifesteal 5; +manasteal 5` | Bladed shield should be an offensive off-hand, but fix the row first. |
| Hell's Embrace | Forsaken Divinity | 45 | Mage Plate | `ac% 160-200; sock 4` | `ac% 160-200; sock 4; +res-fire 40; +abs-fire% 5; +red-dmg% 10` | Hell armor with fire resistance and punishment mitigation. |
| Death Knight's Demon Blade | Volf's Undead Legion | 37 | Battle Sword | `dmg% 160-220; dmg-norm 20-55; lifesteal 15` | `dmg% 160-220; dmg-norm 20-55; lifesteal 15; +dmg-undead 150; +deadly 25` | Death knight blade made specifically hateful to the dead. |
| Lich's Cranium | Volf's Undead Legion | 39 | Grim Helm | `mana 60-80; cast2 25; sock 1` | `mana 60-80; cast2 25; sock 1; +nec 2; +regen-mana 60` | Lich helm, stronger spell identity. |
| Skeleton Warrior's Corpse Plate | Volf's Undead Legion | 42 | Templar Plate | `ac% 80-120; ac/lvl(16); balance2 25` | `ac% 80-120; ac/lvl(16); balance2 25; +red-dmg% 12; +hp 80` | Undead soldier plate, less elegant and harder to kill. |
| Dagger of Vashna | Legacy of Vashna | 30 | Piognard | `dmg-norm 35-70; swing3 75; cast1 10` | `dmg-norm 35-70; swing3 75; cast1 10; +dmg-pois(75) 100-160; +deadly 25` | Assassin dagger, quick and poisoned with ritual precision. |
| Mask of Vashna | Legacy of Vashna | 37 | Death Mask | `ac% 100-115; move1 15; cast1 10` | `ac% 100-115; move1 15; cast1 10; +ass 1; +res-all 20` | Mask supports the mobile caster-assassin role. |
| Lancer's Reach | Salander's Tirade | 37 | Partizan | `dmg% 180-240; swing2 30` | `dmg% 180-240; swing2 30; +pierce 30; +deadly 25; +att% 75` | Polearm reach should reward clean long hits. |
| Salander's Visor | Salander's Tirade | 34 | Casque | `ac% 75-120; dmg-to-mana 10; mana-kill 3` | `ac% 75-120; dmg-to-mana 10; mana-kill 3; +swing2 20; +lifesteal 5` | Visor for a mana-fueled melee tirade. |
| Red Dragon Scale Mail | Jerik's Dragon Armor | 37 | Tigulated Mail | `ac/lvl(32); abs-fire% 35` | `ac/lvl(32); abs-fire% 35; +res-fire 60; +dmg-fire 20-40; +balance2 20` | Red dragon scale should be dramatically fire-proof. |
| Black Dragon Hide Shield | Jerik's Dragon Armor | 37 | Dragon Shield | `res-all 60; ac% 100` | `res-all 60; ac% 100; +block 25; +block1 25; +red-dmg% 10` | Dragon shield, broad resistance plus true guarding. |
| Char's Annulus of Obscurity | Narrow Path Between Light and Darkness | 51 | Ring | `light -1; pal 1; oskill(Sanctuary) 12-15` | `light -1; pal 1; oskill(Sanctuary) 12-15; +res-mag 25; +dmg-undead 150` | Dark paladin ring with anti-undead holy contrast. |
| Char's Blessed Reflection | Narrow Path Between Light and Darkness | 51 | Ring | `light 1; nec 1; oskill(Decrepify) 8-12` | `light 1; nec 1; oskill(Decrepify) 8-12; +red-dmg% 10; +res-all 15` | Light-touched necromancy, curse and protection. |
| Unholy Desires | Zhoulomcrist's Dread | 31 | War Hat | `mana 50; cast1 25; dmg-to-mana 15` | `mana 50; cast1 25; dmg-to-mana 15; +nec 1; +res-pois 35` | Dread caster hat with poison/necromancy alignment. |
| Tortured Soul Gauntlets | The Warlord of Blood | 29 | Gauntlets | `swing2 20; dmg% 30-50` | `swing2 20; dmg% 30-50; +openwounds 35; +crush 10; +lifesteal 5` | Bloody gauntlets should hurt, break, and feed. |
| Hell's Torment Greaves | The Warlord of Blood | 31 | Greaves | `move2 30; hit-skill(Life Tap) 18-1` | `move2 30; hit-skill(Life Tap) 18-1; +res-fire 35; +crush 10; +openwounds 25` | Torment boots for charging into melee sustain. |
| Dying Curses | Darque Necromancy | 30 | Demonhide Sash | `ac% 100-120; skilltab(6) 1; levelup-skill(Weaken) 100-40` | `ac% 100-120; skilltab(6) 1; levelup-skill(Weaken) 100-40; +cast1 20; +res-pois 30` | Curse belt with enough casting support to matter. |
| Dark Rituals | Darque Necromancy | 50 | Mage Plate | `ac 300-400; red-dmg% 10-15; balance3 30` | `ac 300-400; red-dmg% 10-15; balance3 30; +nec 2; +cast2 20` | Ritual armor should empower the necromancer directly. |
| Legacy in Blood | Darque Necromancy | 35 | Amulet | `allskills 1; swing1 10; mag% 50-75` | `allskills 1; swing1 10; mag% 50-75; +lifesteal 6; +openwounds 25` | Blood legacy needs a little actual blood magic. |
| Momentum Theft | Sines Psionics | 50 | Ghost Armor | `ac% 150-250; red-dmg 10-20; aura(Holy Freeze) 5-10` | `ac% 150-250; red-dmg 10-20; aura(Holy Freeze) 5-10; +move2 20; +res-cold 35` | Stealing momentum through chill and movement control. |
| Wall of Modius | Forbidden Lore | 16 | Bone Shield | `aura(103) 7-10; dmg-to-mana 15` | `aura(103) 7-10; dmg-to-mana 15; +nec 1; +block1 20; +res-mag 20` | Forbidden bone ward for a low-level necromancer. |
| Hannibal's Bending Knee | Hannibal's Demise | 45 | Battle Boots | `ac% 100-120; dex 15; gold% 300` | `ac% 100-120; dex 15; gold% 300; +move3 30; +crush 10` | Mercenary/plunder boots that still kick hard. |
| Panda's Sash | Panda's Polar Adventure | 35 | Sash | `res-all 10; vit 10; hp 50` | `res-all 10; vit 10; hp 50; +res-cold 35; +half-freeze 1` | Polar adventure sash, simple and cold-proof. |

## High-Level And Endgame Items

| Item | Set | Req | Base | Before | Proposed after | Flavour |
|---|---|---:|---|---|---|---|
| Onyx's Celestial Rage | Onyx's Primal Rage | 79 | Guardian Crown | `bar 2; red-dmg% 15-20; all-stats 15-25` | `bar 2; red-dmg% 15-20; all-stats 15-25; +crush 15; +swing2 20` | Celestial barbarian rage should hit harder, not only endure. |
| Teachings of Brother Laz | Brother Laz' Calling | 81 | Corona | `ac% 100-150; res-all 20-30; sock 2` | `ac% 100-150; res-all 20-30; sock 2; +allskills 2; +cast2 20` | Endgame teaching crown with real universal power. |
| Spin's Enigma | The Mysterious Spin | 52 | Tiara | `allskills 1-2` | `allskills 1-2; +cast2 20; +mana 75; +res-all 20` | Sparse by design, but still a mysterious caster tiara. |
| Spin's Paradox | The Mysterious Spin | 51 | Scarab Husk | `allskills 2` | `allskills 2; +ac% 180; +balance3 30; +red-dmg% 15` | Paradox armor: huge skill power wrapped in survivability. |
| Spin's Mystery | The Mysterious Spin | 46 | Spiderweb Sash | `allskills 1` | `allskills 1; +cast2 20; +regen-mana 60; +hp% 10` | Mystery caster sash, efficient but not empty. |
| Spin's Conundrum | The Mysterious Spin | 59 | Aegis | `ease -80` | `ease -80; +block 40; +block2 40; +red-dmg% 15; +res-all 25` | The shield's trick is carrying an Aegis easily, then blocking like one. |
| Spin's Perplexing Puzzle | The Mysterious Spin | 50 | Eldritch Orb | `allskills 2` | `allskills 2; +cast3 30; +mana% 15; +extra-mag 15` | Puzzle orb for high-skill spellcasting. |
| Cryptic Claws | Phrozen Heart's Mysticism | 77 | Runic Talons | `dmg% 200-300; lifesteal 11; regen 6` | `dmg% 200-300; lifesteal 11; regen 6; +ass 2; +swing3 40` | Endgame assassin claws should be fast and class-defining. |
| Way of the Shadow | Phrozen Heart's Mysticism | 71 | Diamond Mail | `balance3 30; ac% 160-200; hp 75-100` | `balance3 30; ac% 160-200; hp 75-100; +ass 2; +res-all 25` | Shadow armor with assassin identity and defenses. |
| Dawns Mist | Phrozen Heart's Mysticism | 74 | Vampirebone gloves | `ac% 100-140; mana 40-50; res-all 10-15` | `ac% 100-140; mana 40-50; res-all 10-15; +swing2 20; +dmg-cold(100) 40-80` | Cold mist on martial gloves. |
| Featherfoot | Phrozen Heart's Mysticism | 73 | Wyrmhide Boots | `ac% 125-150; ac 100-200; move3 40` | `ac% 125-150; ac 100-200; move3 40; +res-cold 40; +half-freeze 1` | Fast winter boots that resist the cold they invoke. |
| Winter's Discord | Phrozen Heart's Mysticism | 75 | Vampirefang Belt | `ac% 100-120; gethit-skill(Frost Nova) 10-6; att% 20` | `ac% 100-120; gethit-skill(Frost Nova) 10-6; att% 20; +pierce-cold 15; +extra-cold 15` | Discord belt supports the cold nova theme offensively. |
| Sundered Heart | The Darkest Weaves | 76 | Lacquered Plate | `ac% 170-200; sock 4` | `ac% 170-200; sock 4; +red-dmg% 15; +res-all 30; +hp% 10` | Dark endgame plate, socketable but not naked defensively. |
| Soulreaver | The Darkest Weaves | 77 | Phase Blade | `dmg% 220-300; sock 6` | `dmg% 220-300; sock 6; +swing3 40; +deadly 35; +lifesteal 8` | A soul-reaving blade should be fast and hungry. |
| Throws of Hatred | The Darkest Weaves | 78 | Troll Nest | `ac% 170-210; block 30-50; sock 3` | `ac% 170-210; block 30-50; sock 3; +dmg% 80; +att% 75` | Hatred shield that can be built offensively. |
| Return to Hydrakal | Cedric's Jinx | 75 | Legendary Mallet | `dmg% 175-225; swing3 60; sock 2` | `dmg% 175-225; swing3 60; sock 2; +crush 25; +dmg-fire 80-160` | Legendary mallet with hydra-fire weight. |
| Warder's Vest | Dragon Reborn | 41 | Trellised Armor | `mag% 25-30; gold% 75; ac% 160-200` | `mag% 25-30; gold% 75; ac% 160-200; +res-all 25; +red-dmg% 10` | Warder armor keeps treasure flavour but adds real warding. |
| Ser'Angreal Necklace | Dragon Reborn | 67 | Amulet | `balance1 10; block 5-10; addxp 4-7` | `balance1 10; block 5-10; addxp 4-7; +allskills 1; +res-all 20` | A legendary necklace deserves a little broad power. |
| Heroes Stand | Soldier's Cairn | 35 | Linked Mail | `ac% 130-170; dmg% 50-75; balance3 30` | `ac% 130-170; dmg% 50-75; balance3 30; +hp 75; +res-all 20` | Soldier armor that lets heroes actually hold ground. |
| Warrior's Heroism | Soldier's Cairn | 55 | Dacian Falx | `dmg% 200-300; swing2 20; sock 1-4` | `dmg% 200-300; swing2 20; sock 1-4; +deadly 30; +att% 100` | Heroic two-hander, reliable and lethal. |
| Born Supremacy | Gweibret's Rule | 70 | Mithril Coil | `ac/lvl(13); hp% 25` | `ac/lvl(13); hp% 25; +bar 1; +red-dmg% 15; +balance3 30` | Ruling belt for a dominant front-liner. |
| Alyssa's Leafblighter | Alyssa's Archery | 44 | Long Siege Bow | `dmg% 180-220; swing2 20; sock 3` | `dmg% 180-220; swing2 20; sock 3; +pierce 35; +dmg-pois(100) 150-250` | Leafblighter bow, piercing and poisonous. |
| Guiding Force | Wrath of Vengeance | 71 | Vambraces | `cast2 20; mana/lvl(8); regen-mana 25` | `cast2 20; mana/lvl(8); regen-mana 25; +allskills 1; +res-ltng 35` | Vengeful caster gloves with guidance and storm flavour. |
| Firecam Gilded Plate | Kaldorn's Majesty | 63 | Ornate Plate | `ac% 150-180; res-all 30-50; balance2 20` | `ac% 150-180; res-all 30-50; balance2 20; +pal 1; +red-dmg% 15` | Gilded majesty plate, paladin-coded and stalwart. |
| Windspar Mask | Kaldorn's Majesty | 74 | Spired Helm | `red-dmg% 15-25; ac% 155-185; hp 40-50` | `red-dmg% 15-25; ac% 155-185; hp 40-50; +res-cold 35; +balance2 20` | Wind-spire helm, cold air and resilience. |
| Waterwyrd's Talon | Kaldorn's Majesty | 55 | War Gauntlets | `swing3 40; ac% 175-200` | `swing3 40; ac% 175-200; +dmg-cold(100) 50-100; +lifesteal 6; +openwounds 25` | Water-wyrd talons, fast and cutting cold. |
| Daystar Wrap | Kaldorn's Majesty | 58 | war Belt | `hp 175-200; mana 75-100` | `hp 175-200; mana 75-100; +regen 10; +regen-mana 60; +res-fire 35` | Daystar belt: vitality, mana, and solar warmth. |
| Incarnadine Elven Plate | Warlock's Exploration | 55 | Mage Plate | `war 2; sock 2; ac 300-500` | `war 2; sock 2; ac 300-500; +res-mag 25; +balance3 30` | Warlock exploration armor with magical protection. |
| Lilarcors Crown | Warlock's Exploration | 64 | Diadem | `allskills 2; ac% 100-150; res-all 15-20` | `allskills 2; ac% 100-150; res-all 15-20; +cast2 20; +mana 75` | Talking-sword energy, mental speed and mana. |
| Teleomortis' Gloves | Warlock's Exploration | 75 | Bramble Mitts | `war 1; ac 150-200; extra-mag 10` | `war 1; ac 150-200; extra-mag 10; +cast2 20; +mana-kill 5` | Warlock mitts that convert death into casting momentum. |
| Citadel Belt | Warlock's Exploration | 66 | Spiderweb Sash | `allskills 2; ac 125-175` | `allskills 2; ac 125-175; +red-dmg% 10; +res-all 20; +hp 100` | Citadel belt should feel like a fortress around the caster. |
| Holy Sash of Amaunator | Amaunator's Peace | 30 | Demonhide Sash | `ac% 190-230; vit 15-20; red-mag 10-15` | `ac% 190-230; vit 15-20; red-mag 10-15; +pal 1; +res-fire 30` | Sun-god sash with paladin and fire protection. |
| Belt of Temerity | Knight's Gallantry | 30 | Plated Belt | `ac% 100-120; res-pois 35-45` | `ac% 100-120; res-pois 35-45; +red-dmg 8; +res-pois-len 50; +hp 50` | Gallant belt, sturdy and poison-resistant. |
| Sunspear Deflector | Kai Lord's Valiance | 63 | Pavice | `ac% 175-200; block 100; block1 15` | `ac% 175-200; block 100; block1 15; +pal 1; +dmg-undead 150` | Sunspear shield, holy deflection and undead punishment. |
| Imperial Plate | Path of Bravery | 73 | Hellforge Plate | `dmg-demon 200; ac% 100-125; pierce-fire 20` | `dmg-demon 200; ac% 100-125; pierce-fire 20; +res-fire 40; +dmg-fire 60-120` | Imperial demon hunter plate, fire-brave. |
| Imperial Helm | Path of Bravery | 40 | Sallet | `ac% 125-150; red-dmg% 15; pierce-cold 20` | `ac% 125-150; red-dmg% 15; pierce-cold 20; +res-cold 40; +balance2 20` | Bravery helm against cold pressure. |
| Imperial Girdle | Path of Bravery | 75 | Colossus Girdle | `ac% 125-150; res-all 35-40; pierce-ltng 20` | `ac% 125-150; res-all 35-40; pierce-ltng 20; +res-ltng 40; +hp 100` | Imperial lightning ward and battle stamina. |
| Imperial Greaves | Path of Bravery | 77 | Myrmidon Greaves | `ac% 120-140; res-mag 20; pierce-pois 20` | `ac% 120-140; res-mag 20; pierce-pois 20; +res-pois 40; +move2 30` | Brave stride through venom and magic. |
| Demonic Chuckle | Corruption Coils | 45 | Ring | `hp 35-50; mana 25` | `hp 35-50; mana 25; +cast1 10; +res-pois 25; +dmg-pois(75) 50-75` | One corruption ring leans poisonous and spell-like. |
| Evil Humor | Corruption Coils | 45 | Ring | `hp 35-50; mana 25` | `hp 35-50; mana 25; +swing1 10; +res-fire 25; +dmg-fire 15-30` | The other ring gets a cruel melee/fire identity. |
| Temptation's Death | Corruption Coils | 45 | Amulet | `hp 50-75; mana 40` | `hp 50-75; mana 40; +allskills 1; +res-all 15; +lifesteal 4` | Tempting amulet, broad power at a cost-flavoured edge. |
