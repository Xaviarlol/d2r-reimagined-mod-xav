# Rare Greater Affix Apex Audit

Generated: 2026-05-19.

Purpose: scan the live rare-eligible affix tables, identify every affix group that contains apex rows, and draft a complete Greater Affix candidate list with spawn odds that can be reviewed before implementation.

## Method And Assumptions

- Source tables: `data/global/excel/magicprefix.txt`, `data/global/excel/magicsuffix.txt`, and `data/global/excel/itemtypes.txt`.
- Chance model uses affix level `90` and the current live affix pools.
- The script adds drafted Greater rows synthetically; no game TXT files are changed by this report.
- `Per affix slot` is candidate frequency divided by all eligible same-side affix frequency for the sample item after adding all drafted Greater rows.
- `If 3 same-side slots` is an exact group-blocked probability for a rare item that receives `3` prefix slots or `3` suffix slots. Real rares may receive fewer same-side slots, so actual per-item odds are lower when the item rolls fewer affixes.
- Item-type eligibility uses `itype*` / `etype*` plus `itemtypes.txt` inheritance.
- Multi-element or multi-scope candidates are aggregated in the chance table. Per-element odds are lower when a row represents several separate element variants.
- Rows marked defer/optional are still captured in the audit so we do not forget them, but they are not first-pass Greater candidates.

## Draft Greater Affix Chance Table

| Greater candidate | Side | Group | Sample item | Candidate weight | Pool weight | Per affix slot | If 3 same-side slots | Apex baseline | Draft greater payload |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Greater Gnostic | prefix | 201 | amul | 1 | 483 | 0.207% | 0.719% | +5 random class skill rows in group 201 | skill-rand +6, one class band per row |
| Greater Omniscient | prefix | 125 | amul | 1 | 483 | 0.207% | 0.398% | Omniscient/Sage's allskills in group 125 | allskills +3 torso/amulet, +2 ring |
| Greater Sage | prefix | 204 | amul | 3 | 483 | 0.621% | 2.401% | Master Sage's addxp in group 204 | addxp 6 |
| Greater Skilltab | prefix | 125 | amul | 3 | 483 | 0.621% | 1.194% | +3 skilltab rows in group 125 | skilltab +4, one row per skill tree |
| Greater class skill | prefix | 125 | amul | 1 | 483 | 0.207% | 0.398% | +2 class skill rows, including Warlock, in group 125 | +3 class skills on torso/amulet/circlet scopes |
| Greater Adamantine-Wrought | prefix | 206 | axe | 3 | 1275 | 0.235% | 1.578% | Adamantine-Wrought ED/defense plus durability in group 206 | weapon dmg% 110-130 or armor ac% 85-100 plus dur 80-100 |
| Greater Celestial | prefix | 123 | axe | 3 | 1275 | 0.235% | 1.652% | Celestial demon AR/damage in group 123 | att-demon 451-550 plus dmg-demon 351-425 |
| Greater Divine | prefix | 142 | axe | 3 | 1275 | 0.235% | 1.647% | Divine undead AR/damage in group 142 | att-undead 500-650 plus dmg-undead 400-500 |
| Greater Elemental | prefix | 203 | axe | 3 | 1275 | 0.235% | 1.647% | Elemental1 mixed elemental weapon row in group 203 | dmg-elem above current range |
| Greater Grandmaster's | prefix | 111 | axe | 4 | 1275 | 0.314% | 0.438% | Grandmaster's variants and Wraithly1 in group 111 | dmg% 451-500 plus AR / Deadly / Crushing / Open Wounds rider |
| Greater Gritty | prefix | 105 | axe | 3 | 1275 | 0.235% | 1.583% | Gritty damage-per-level in group 105 | stronger dmg/lvl weapon scaling |
| Greater Platinum | prefix | 110 | axe | 3 | 1275 | 0.235% | 1.533% | highest attack-rating rows in group 110 | att 351-450, item-scope split if needed |
| Greater Scorching/Shocking/Pestilent | prefix | 138, 139, 140 | axe | 9 | 1275 | 0.706% | 4.888% | weapon elemental damage prefixes in groups 138-140 | one element per row, about 25-35% above current apex |
| Greater Savage | prefix | 205 | boot | 3 | 789 | 0.380% | 3.570% | Savage kick damage in group 205 | kick 11-13 |
| Greater Crushing/Fatal | prefix | 202 | glov | 3 | 859 | 0.349% | 2.646% | Crushing and Fatal glove rows in group 202 | crush/deadly 24-30, separate rows in same group |
| Greater Veracious | prefix | 200 | glov | 3 | 859 | 0.349% | 2.685% | Veracious attack% in group 200 | att% 40-50 |
| Greater Aureolin | prefix | 121 | jewl | 3 | 166 | 1.807% | 5.784% | Aureolin mana after kill in group 121 | mana-kill 4-5 |
| Greater Bloody | prefix | 103 | jewl | 3 | 166 | 1.807% | 5.080% | Bloody min+max damage rows in group 103 | dmg-min 9-12 plus dmg-max 18-24 |
| Greater Avatar | prefix | 137 | lcha | 3 | 315 | 0.952% | 2.760% | Avatar elemental large charm row in group 137 | dmg-elem 35-45 |
| Greater Hulking | prefix | 143 | lcha | 3 | 315 | 0.952% | 2.996% | Hulking normal damage large charm in group 143 | dmg-norm 70-85 |
| Greater Lucky | prefix | 114 | lcha | 3 | 315 | 0.952% | 3.059% | Lucky mag% plus gold% in group 114 | mag% 30-35 plus gold% 60-70 |
| Greater Ruby/Sapphire/Amber/Emerald | prefix | 117, 118, 119, 120 | lcha | 12 | 315 | 3.810% | 11.364% | single-element large charm resist rows in groups 117-120 | single resist 34-40, one element per row |
| Greater Serpent's | prefix | 115 | lcha | 3 | 315 | 0.952% | 2.963% | Serpent's mana in group 115 | mana 70-85 |
| Greater Serrated | prefix | 104 | lcha | 3 | 315 | 0.952% | 3.028% | Serrated large charm enhanced damage in group 104 | dmg% 30-35 on large charms |
| Greater Shimmering | prefix | 116 | lcha | 3 | 315 | 0.952% | 2.996% | Shimmering all resistance in group 116 | res-all 15-18 |
| Greater missile prefixes | prefix | 220, 221, 222, 223, 224, 225, 226, 227 | miss | 16 | 1269 | 1.261% | 8.833% | missile-only prefix groups 220-227 | stronger quiver/missile weapon stat family rows |
| Greater Antimagic | prefix | 102 | shld | 3 | 870 | 0.345% | 2.660% | Antimagic res-mag 16-20 in group 102 | res-mag 24-30 |
| Greater Vulpine | prefix | 107 | shld | 3 | 870 | 0.345% | 2.867% | Vulpine damage-to-mana in group 107 | dmg-to-mana 16-20 |
| Greater Aureole | prefix | 207 | tors | 1 | 872 | 0.115% | 0.906% | Aureole aura rows in group 207 | higher aura level; needs per-aura balance |
| Greater Godly | prefix | 101 | tors | 3 | 872 | 0.344% | 0.453% | Godly, Invulnerable1, armor Wraithly1 in group 101 | ac% 250-300 plus red-dmg% 26-30 |
| Greater Elemental Mastery | prefix | 209 | wand | 2 | 395 | 0.506% | 1.416% | extra-fire/cold/lightning/poison caster rows in group 209 | extra-* 14-16 |
| Greater Elemental Pierce | prefix | 209 | wand | 2 | 395 | 0.506% | 1.416% | pierce-fire/cold/lightning/poison caster rows in group 209 | pierce-* 14-16 |
| Greater Enlightenment | suffix | 23 | amul | 3 | 3316 | 0.090% | 0.275% | Energy rows in group 23 | enr 36-40, scope split if needed |
| Greater Zodiac | suffix | 42 | amul | 3 | 3316 | 0.090% | 0.278% | Zodiac all-stats in group 42 | all-stats 38-45 |
| Greater jewelry elemental damage | suffix | 10, 12, 13, 16 | amul | 8 | 3316 | 0.241% | 0.739% | Glacier/Burning/Storms/Blight jewelry elemental rows in groups 10,12,13,16 | about 25-35% above current apex, one element per row |
| Greater Blindness | suffix | 65 | axe | 2 | 2739 | 0.073% | 0.251% | Blindness hit blinds target in group 65 | stupidity 4 |
| Greater Draining | suffix | 80 | axe | 3 | 2739 | 0.110% | 0.379% | Siphoning heal per hit in group 80 | healperhit 14-16 |
| Greater Evisceration | suffix | 14 | axe | 3 | 2739 | 0.110% | 0.251% | Evisceration max damage in group 14 | dmg-max 150-165 |
| Greater Paralysis | suffix | 64 | axe | 2 | 2739 | 0.073% | 0.245% | Paralysis slow target in group 64 | slow 28-33 |
| Greater Quickness | suffix | 7 | axe | 3 | 2739 | 0.110% | 0.339% | Quickness IAS in group 7 | swing3 50 |
| Greater Transcendence | suffix | 15 | axe | 3 | 2739 | 0.110% | 0.373% | Transcendence min damage in group 15 | dmg-min 75-85 |
| Greater Wealth | suffix | 21 | belt | 3 | 1062 | 0.282% | 0.930% | Wealth gold find in group 21 | gold% 100-120 |
| Greater Perfection | suffix | 17 | boot | 3 | 1041 | 0.288% | 0.900% | Perfection dexterity in group 17 | dex 36-40 |
| Greater Regeneration | suffix | 19 | boot | 3 | 1041 | 0.288% | 0.925% | Regeneration life regen in group 19 | regen 6-8 |
| Greater Reanimation | suffix | 66 | glov | 2 | 1117 | 0.179% | 0.573% | Reanimation in group 66 | higher reanimate chance/level |
| Greater Prosperity | suffix | 22 | jewl | 3 | 1310 | 0.229% | 0.724% | Prosperity magic find in group 22 | mag% 26-30 |
| Greater Balance | suffix | 18 | lcha | 3 | 97 | 3.093% | 12.431% | Balance FHR on large charms in group 18 | balance3 13-15 |
| Greater Inertia | suffix | 35 | lcha | 3 | 97 | 3.093% | 12.431% | Inertia FRW large charm in group 35 | move3 13-15 |
| Greater Vita | suffix | 26 | lcha | 3 | 97 | 3.093% | 12.431% | Vita life on large charms in group 26 | hp 80-95 |
| Greater missile suffixes | suffix | 200, 201, 202, 203, 204, 205, 206 | miss | 13 | 2431 | 0.535% | 1.890% | missile-only suffix groups 200-206 | stronger quiver/missile weapon suffix rows |
| Greater Magus | suffix | 9 | orb | 3 | 1552 | 0.193% | 0.588% | Magus FCR in group 9 | cast3 25 |
| Greater Coalescence | suffix | 3 | ring | 3 | 2706 | 0.111% | 0.318% | elemental absorb percent rows in group 3 | abs-fire/ltng/cold% 28-35, one element per row |
| Greater Elephant | suffix | 41 | ring | 3 | 2706 | 0.111% | 0.350% | Elephant hp/lvl and mana/lvl in group 41 | stronger hp/lvl plus mana/lvl |
| Greater Guarding | suffix | 61 | ring | 3 | 2706 | 0.111% | 0.328% | Guarding flat defense on jewelry in group 61 | ac 60-90 |
| Greater Lamprey/Vampire | suffix | 27, 28 | ring | 3 | 2706 | 0.111% | 0.343% | single leech rows in groups 27 and 28 | lifesteal/manasteal above current top, scope split |
| Greater Lich | suffix | 60 | ring | 3 | 2706 | 0.111% | 0.348% | Lich dual leech in group 60 | manasteal 10-12 plus lifesteal 13-15 |
| Greater Titan | suffix | 31 | ring | 3 | 2706 | 0.111% | 0.338% | strength/dex/vit/enr rows in group 31 | primary stat 26-30 or equivalent scope split |
| Greater Deflecting | suffix | 8 | shld | 3 | 1798 | 0.167% | 0.494% | Deflecting block rows in group 8 | block 35-40 plus block2 40 |
| Greater Elements | suffix | 43 | shld | 3 | 1798 | 0.167% | 0.508% | Elements res/lvl row in group 43 | stronger multi-res per level |
| Greater Four Seasons | suffix | 67 | shld | 1 | 1798 | 0.056% | 0.168% | Four Seasons max all resist in group 67 | res-all-max 7-8 |
| Greater Negation | suffix | 2 | shld | 3 | 1798 | 0.167% | 0.466% | Negation res-mag 14-20 in group 2 | res-mag 24-30 |
| Greater Anima | suffix | 1 | tors | 3 | 1518 | 0.198% | 0.612% | Anima flat damage reduction in group 1 | red-dmg 18-24 |
| Greater Thorns | suffix | 6 | tors | 3 | 1518 | 0.198% | 0.558% | Thorns flat/level retaliation in group 6 | stronger thorns/lvl |

## Complete Rare-Affix Group Coverage Audit

This table is intentionally mechanical. It makes every rare-eligible prefix/suffix group visible, including groups we should defer.

| Side | Group | Rows | Top level | Mod families | Representative apex rows | Greater-plan status |
| --- | --- | --- | --- | --- | --- | --- |
| prefix | 44 | 235 | 80 | charged | Charged1 L80 F1 (charged(31) 300-22); Charged1 L80 F1 (charged(34) 300-15); Charged1 L80 F1 (charged(35) 300-15); Charged1 L80 F1 (charged(62) 250-25) | Defer: charged-skill affixes are technical and not a clean Greater range. |
| prefix | 101 | 39 | 86 | ac, ac%, ac%/lvl, ac-miss, ac/lvl, ethereal, red-dmg%, rep-dur | Godly L86 F110 (ac% 201-225); Wraithly1 L86 F4 (ac% 81-100, ethereal 1-1, rep-dur(10) -); Invulnerable1 L86 F4 (ac% 81-100, red-dmg% 21-25); Stalwart L81 F3 (ac 118-139, ac-miss 66-78) | Covered by Greater Godly |
| prefix | 102 | 8 | 86 | red-mag, res-mag | Antimagic L86 F8 (res-mag 16-20); Null L69 F8 (res-mag 11-15); Blank L47 F8 (res-mag 6-10); Antimagic L28 F8 (red-mag 6-10) | Covered by Greater Antimagic |
| prefix | 103 | 10 | 86 | dmg-max, dmg-min | Bloody L86 F8 (dmg-min 6-8, dmg-max 13-15); Bloody L86 F3 (dmg-min 6-8, dmg-max 13-15); Sanguinary L60 F6 (dmg-min 4-5, dmg-max 6-12); Sanguinary L59 F8 (dmg-min 4-5, dmg-max 8-12) | Covered by Greater Bloody |
| prefix | 104 | 5 | 81 | dmg%, dmg-max | Serrated L81 F3 (dmg% 20-25); Vermillion L58 F8 (dmg-max 11-15); Forked L55 F6 (dmg% 10-15); Carmine L35 F8 (dmg-max 6-9) | Covered by Greater Serrated |
| prefix | 105 | 17 | 75 | att/lvl, dmg%, dmg/lvl | Gritty L75 F14 (dmg/lvl(16) -); Vicious L70 F24 (dmg% 26-40); Ruby L66 F10 (dmg% 31-40); Shouting L60 F2 (dmg/lvl(12) -) | Covered by Greater Gritty |
| prefix | 107 | 2 | 9 | dmg-to-mana | Vulpine L9 F6 (dmg-to-mana 7-12); Dun L7 F6 (dmg-to-mana 7-12) | Covered by Greater Vulpine |
| prefix | 110 | 19 | 81 | att, dmg-max | Steel L81 F6 (att 118-132); Steel L61 F6 (att 103-117); Sharp L61 F3 (att 49-76, dmg-max 7-10); Weird L44 F8 (att 301-450) | Covered by Greater Platinum |
| prefix | 111 | 96 | 88 | ac, addxp, att, att%/lvl, att/lvl, crush, deadly, dmg% | Master Sage's L88 F2 (addxp 3-3, dmg% 225-250); Wraithly1 L86 F4 (dmg% 176-200, ethereal 1-1, rep-dur(10) -); Grandmaster's L86 F2 (deadly 15-30, dmg% 301-350); Grandmaster's L86 F2 (crush 15-30, dmg% 301-350) | Covered by Greater Grandmaster's |
| prefix | 112 | 3 | 6 | att, light | Glowing L6 F2 (light 2-2); Glimmering L1 F2 (light 1-1); Bright L1 F2 (light 1-1, att 10-10) | Defer: light radius plus small AR is not a meaningful chase family. |
| prefix | 113 | 6 | 24 | howl | Wailing L24 F8 (howl 128-128); Wailing L20 F6 (howl 128-128); Howling L16 F8 (howl 64-64); Howling L16 F6 (howl 64-64) | Defer: howl-on-hit utility needs a separate crowd-control affix review. |
| prefix | 114 | 5 | 55 | gold%, mag% | Lucky L55 F6 (mag% 20-25, gold% 40-50); Lucky L38 F12 (mag% 15-20, gold% 30-40); Emerald L16 F8 (mag% 3-7); Fortuitous L12 F8 (mag% 11-15) | Covered by Greater Lucky |
| prefix | 115 | 17 | 85 | mana, mana/lvl | Serpent's L85 F3 (mana 53-59); Serpent's L81 F6 (mana 47-52); Serpent's L61 F6 (mana 40-46); Dragon's L52 F4 (mana 31-40) | Covered by Greater Serpent's |
| prefix | 116 | 18 | 81 | res-all | Shimmering L81 F3 (res-all 10-12); Scintillating L67 F4 (res-all 13-17); Shimmering L65 F3 (res-all 8-10); Rainbow L56 F4 (res-all 9-12) | Covered by Greater Shimmering |
| prefix | 117 | 16 | 60 | res-cold, res-fire, res-ltng, res-pois | Sapphire L60 F6 (res-cold 26-30); Cobalt L55 F4 (res-cold 21-30); Cobalt L45 F12 (res-cold 21-25); Lapis L35 F4 (res-cold 11-20) | Covered by Greater Ruby/Sapphire/Amber/Emerald |
| prefix | 118 | 7 | 60 | res-fire | Ruby L60 F6 (res-fire 26-30); Garnet L55 F2 (res-fire 21-30); Garnet L45 F12 (res-fire 21-25); Russet L35 F2 (res-fire 11-20) | Covered by Greater Ruby/Sapphire/Amber/Emerald |
| prefix | 119 | 8 | 60 | res-ltng | Amber L60 F6 (res-ltng 26-30); Coral L55 F2 (res-ltng 21-30); Coral L45 F12 (res-ltng 21-25); Ocher L35 F2 (res-ltng 11-20) | Covered by Greater Ruby/Sapphire/Amber/Emerald |
| prefix | 120 | 8 | 60 | res-pois | Emerald L60 F6 (res-pois 26-30); Jade L55 F2 (res-pois 21-30); Jade L45 F12 (res-pois 21-25); Viridian L35 F2 (res-pois 11-20) | Covered by Greater Ruby/Sapphire/Amber/Emerald |
| prefix | 121 | 3 | 22 | mana-kill | Aureolin L22 F8 (mana-kill 1-3); Victorious L17 F8 (mana-kill 2-5); Triumphant L3 F8 (mana-kill 1-1) | Covered by Greater Aureolin |
| prefix | 122 | 3 | 55 | sock | Jeweler's L55 F2 (sock(4) -); Artificer's L33 F4 (sock(3) -); Mechanist's L10 F6 (sock 1-2) | Defer: sockets dominate item identity and need a separate socket-affix review. |
| prefix | 123 | 7 | 55 | att-demon, dmg-demon | Celestial L55 F2 (att-demon 301-400, dmg-demon 201-300); Elysian L45 F2 (att-demon 201-300, dmg-demon 151-200); Astral L35 F2 (att-demon 151-200, dmg-demon 101-150); Diamond L26 F2 (att-demon 25-50, dmg-demon 25-40) | Covered by Greater Celestial |
| prefix | 125 | 167 | 90 | allskills, ama, ass, bar, dru, nec, pal, skilltab | Arch-Devil's L90 F2 (war 2-2); Valkyrie's L86 F4 (ama 2-2); Priest's L86 F4 (pal 2-2); Necromancer's L86 F4 (nec 2-2) | Covered by Greater Omniscient, Greater Skilltab, Greater class skill |
| prefix | 137 | 14 | 85 | cold-len, cold-max, cold-min, dmg-elem, dmg-pois, fire-max, fire-min, ltng-max | Avatar L85 F1 (dmg-elem 20-30); Boreal L81 F3 (cold-min 12-14, cold-max 20-25); Flaming L81 F3 (fire-min 10-15, fire-max 20-25); Shocking L81 F3 (ltng-min 10-15, ltng-max 20-25) | Covered by Greater Avatar |
| prefix | 138 | 5 | 77 | fire-max, fire-min | Scorching L77 F2 (fire-min 121-170, fire-max 181-240); Flaming L61 F2 (fire-min 81-120, fire-max 131-180); Smoking L47 F2 (fire-min 51-80, fire-max 91-130); Smoldering L35 F4 (fire-min 26-50, fire-max 61-90) | Covered by Greater Scorching/Shocking/Pestilent |
| prefix | 139 | 5 | 76 | ltng-max, ltng-min | Shocking L76 F2 (ltng-min 1-1, ltng-max 361-480); Arcing L60 F2 (ltng-min 1-1, ltng-max 261-360); Buzzing L46 F2 (ltng-min 1-1, ltng-max 181-260); Glowing L34 F4 (ltng-min 1-1, ltng-max 121-180) | Covered by Greater Scorching/Shocking/Pestilent |
| prefix | 140 | 5 | 50 | dmg-pois | Pestilent L50 F2 (dmg-pois(150) 470-470); Toxic L35 F2 (dmg-pois(125) 308-308); Corosive L20 F2 (dmg-pois(100) 205-205); Envenomed L10 F4 (dmg-pois(75) 41-41) | Covered by Greater Scorching/Shocking/Pestilent |
| prefix | 141 | 3 | 38 | stack | Dense L38 F8 (stack 81-120); Thin L17 F10 (stack 41-80); Compact L1 F12 (stack 20-40) | Defer: stack-size utility, not a rare-power target. |
| prefix | 142 | 6 | 45 | att-undead, dmg-undead | Divine L45 F2 (att-undead 326-450, dmg-undead 276-350); Hallowed L35 F2 (att-undead 251-325, dmg-undead 201-275); Sacred L25 F4 (att-undead 175-250, dmg-undead 126-200); Pearl L18 F2 (att-undead 25-50, dmg-undead 25-50) | Covered by Greater Divine |
| prefix | 143 | 2 | 85 | dmg-norm | Hulking L85 F6 (dmg-norm 40-60); Hulking L65 F6 (dmg-norm 20-40) | Covered by Greater Hulking |
| prefix | 200 | 5 | 85 | att% | Veracious1 L85 F2 (att% 25-35); Meticulous1 L70 F4 (att% 20-24); Fastidious1 L55 F4 (att% 15-19); Precise1 L40 F6 (att% 10-14) | Covered by Greater Veracious |
| prefix | 201 | 32 | 85 | skill-rand | Gnostics L85 F2 (skill-rand(5) 6-35); Gnostics L85 F2 (skill-rand(5) 96-125); Gnostics L85 F2 (skill-rand(5) 66-95); Gnostics L85 F2 (skill-rand(5) 36-65) | Covered by Greater Gnostic |
| prefix | 202 | 6 | 70 | crush, deadly | Crushing1 L70 F4 (crush 16-20); Fatal L70 F4 (deadly 16-20); Fracturing1 L45 F4 (crush 11-15); Lethal L45 F4 (deadly 11-15) | Covered by Greater Crushing/Fatal |
| prefix | 203 | 4 | 80 | dmg-elem | Elemental1 L80 F2 (dmg-elem(125) 64-200); Elemental1 L68 F2 (dmg-elem(100) 51-125); Elemental1 L49 F4 (dmg-elem(75) 21-50); Elemental1 L24 F4 (dmg-elem(50) 1-20) | Covered by Greater Elemental |
| prefix | 204 | 5 | 87 | addxp | Master Sage's L87 F2 (addxp 5-5); Sage's L74 F4 (addxp 4-4); Sage's L51 F6 (addxp 3-3); Loremaster's1 L33 F8 (addxp 2-2) | Covered by Greater Sage |
| prefix | 205 | 6 | 64 | kick | Savage L64 F4 (kick 9-10); Savage L51 F4 (kick 7-8); Brutal L39 F4 (kick 5-6); Brutal L28 F4 (kick 3-4) | Covered by Greater Savage |
| prefix | 206 | 16 | 87 | ac%, dmg%, dur | Adamantine-Wrought L87 F4 (dmg% 81-100, dur 60-75); Adamantine-Wrought L87 F4 (ac% 51-75, dur 60-75); Mithril-Wrought L73 F4 (dmg% 66-80, dur 46-59); Mithril-Wrought L73 F4 (ac% 41-50, dur 46-59) | Covered by Greater Adamantine-Wrought |
| prefix | 207 | 15 | 62 | aura | Aureole L62 F2 (aura(125) 1-3); Aureole L57 F2 (aura(123) 1-3); Aureole L53 F2 (aura(122) 1-3); Aureole L46 F2 (aura(120) 1-3) | Covered by Greater Aureole |
| prefix | 209 | 24 | 77 | extra-cold, extra-fire, extra-ltng, extra-pois, pierce-cold, pierce-fire, pierce-ltng, pierce-pois | Pyromaniac's2 L77 F2 (pierce-fire 10-12); Frost Wyrm's2 L77 F2 (pierce-cold 10-12); Zeus's2 L77 F2 (pierce-ltng 10-12); Manticore's2 L77 F2 (pierce-pois 10-12) | Covered by Greater Elemental Mastery, Greater Elemental Pierce |
| prefix | 220 | 6 | 80 | hp, mana | Sturdy L80 F3 (hp 30-40); Lizard's L80 F3 (mana 30-40); Sturdy L45 F6 (hp 15-25); Lizard's L45 F6 (mana 15-25) | Covered by Greater missile prefixes |
| prefix | 221 | 3 | 80 | att | Sharp L80 F3 (att 50-100); Sharp L45 F6 (att 20-30); Sharp L1 F9 (att 5-10) | Covered by Greater missile prefixes |
| prefix | 222 | 6 | 80 | dmg%, dmg-max, dmg-min | Jagged L80 F3 (dmg% 30-50); Jagged L80 F3 (dmg-min 10-20, dmg-max 20-30); Jagged L45 F6 (dmg% 20-30); Jagged L45 F6 (dmg-min 3-5, dmg-max 5-10) | Covered by Greater missile prefixes |
| prefix | 223 | 3 | 80 | fire-max, fire-min | Flaming L80 F3 (fire-min 10-20, fire-max 20-30); Flaming L45 F6 (fire-min 3-5, fire-max 5-10); Flaming L1 F9 (fire-min 1-3, fire-max 3-5) | Covered by Greater missile prefixes |
| prefix | 224 | 3 | 80 | cold-max, cold-min | Shivering L80 F3 (cold-min 10-20, cold-max 20-30); Shivering L45 F6 (cold-min 3-5, cold-max 5-10); Shivering L1 F9 (cold-min 1-3, cold-max 3-5) | Covered by Greater missile prefixes |
| prefix | 225 | 3 | 80 | ltng-max, ltng-min | Static L80 F3 (ltng-min 5-10, ltng-max 30-50); Static L45 F6 (ltng-min 1-5, ltng-max 10-20); Static L1 F9 (ltng-min 1-1, ltng-max 5-10) | Covered by Greater missile prefixes |
| prefix | 226 | 3 | 80 | dmg-pois | Corosive L80 F3 (dmg-pois(100) 300-600); Corosive L45 F6 (dmg-pois(100) 100-150); Corosive L1 F9 (dmg-pois(100) 30-50) | Covered by Greater missile prefixes |
| prefix | 227 | 3 | 80 | dmg-mag | Apprentice L80 F3 (dmg-mag 10-20); Apprentice L45 F6 (dmg-mag 5-10); Apprentice L1 F9 (dmg-mag 1-5) | Covered by Greater missile prefixes |
| prefix | 307 | 36 | 92 | Breaching-Affix1, Breaching-Affix2, Gelid-Affix1, Gelid-Affix2, Incendiary-Affix1, Incendiary-Affix2, Magnetic-Affix1, Magnetic-Affix2 | Virulent L92 F1 (pierce-pois(1) 1-1); Virulent L92 F1 (pierce-pois(1) 1-2); Virulent L92 F1 (pierce-pois(1) 1-3); Virulent L92 F1 (pierce-pois(1) 1-4) | Defer/exempt: special rare-only pierce rows with mixed charm/non-charm scopes. |
| suffix | 1 | 9 | 51 | red-dmg | of Anima L51 F48 (red-dmg 8-15); of Life Everlasting L45 F48 (red-dmg 10-25); of Life L41 F48 (red-dmg 6-7); of Life L35 F48 (red-dmg 6-10) | Covered by Greater Anima |
| suffix | 2 | 11 | 84 | red-mag, res-mag | of Negation L84 F48 (res-mag 14-20); of Guarding L66 F48 (res-mag 10-13); of Negation L42 F48 (red-mag 7-8); of the Sentinel L42 F48 (res-mag 6-9) | Covered by Greater Negation |
| suffix | 3 | 39 | 87 | abs-cold, abs-cold%, abs-fire, abs-fire%, abs-ltng, abs-ltng% | of Fire Coalescence1 L87 F12 (abs-fire% 16-25); of Lightning Coalescence1 L87 F12 (abs-ltng% 16-25); of Chilling Coalescence1 L87 F12 (abs-cold% 16-25); of Fire Coalescence1 L66 F12 (abs-fire% 8-15) | Covered by Greater Coalescence |
| suffix | 4 | 2 | 77 | ignore-ac | of Piercing L77 F24 (ignore-ac 1-1); of Piercing L25 F24 (ignore-ac 1-1) | Defer: ignore target defense is binary. |
| suffix | 5 | 2 | 16 | reduce-ac | of Bashing L16 F48 (reduce-ac 5-10); of Puncturing L6 F48 (reduce-ac 11-20) | Optional: reduce target defense can be Greater later, but is not a first-pass chase family. |
| suffix | 6 | 11 | 67 | thorns, thorns/lvl | of Thorns L67 F48 (thorns/lvl(12) -); of Swords L65 F24 (thorns 41-50); of Malice L60 F48 (thorns 8-15); of Swords L55 F36 (thorns 21-40) | Covered by Greater Thorns |
| suffix | 7 | 8 | 46 | swing1, swing2, swing3 | of Quickness L46 F60 (swing3 40-40); of Alacrity L43 F48 (swing2 20-20); of Fervor L39 F48 (swing1 15-15); of Fervor L39 F48 (swing1 15-15) | Covered by Greater Quickness |
| suffix | 8 | 2 | 11 | block, block2 | of Deflecting L11 F76 (block 20-30, block2 30-30); of Blocking L1 F84 (block 10-19, block2 15-15) | Covered by Greater Deflecting |
| suffix | 9 | 2 | 29 | cast1, cast3 | of the Magus L29 F60 (cast3 20-20); of the Apprentice L5 F72 (cast1 10-10) | Covered by Greater Magus |
| suffix | 10 | 21 | 85 | cold-len, cold-max, cold-min, dmg-pois, fire-max, fire-min, ltng-max, ltng-min | of the Glacier L85 F24 (cold-min 4-5, cold-max 16-25, cold-len 150-150); of Winter L81 F6 (cold-min 12-14, cold-max 20-25); of Incineration L81 F6 (fire-min 10-15, fire-max 20-25); of Storms L81 F6 (ltng-min 10-15, ltng-max 20-25) | Covered by Greater jewelry elemental damage |
| suffix | 11 | 2 | 77 | half-freeze, nofreeze | of Warmth L77 F24 (nofreeze 1-1); of Warmth L10 F48 (half-freeze 1-1) | Defer: half-freeze/cannot-freeze are binary. |
| suffix | 12 | 13 | 80 | fire-max, fire-min | of Burning L80 F24 (fire-min 11-25, fire-max 31-50); of Incineration L80 F12 (fire-min 75-100, fire-max 200-250); of Fire L65 F24 (fire-min 4-10, fire-max 11-30); of Incineration L60 F12 (fire-min 40-60, fire-max 170-200) | Covered by Greater jewelry elemental damage |
| suffix | 13 | 13 | 86 | ltng-max, ltng-min | of Storms L86 F24 (ltng-min 1-1, ltng-max 76-100); of Thunder L75 F24 (ltng-min 1-1, ltng-max 51-75); of Storms L75 F12 (ltng-min 1-20, ltng-max 300-350); of Lightning L65 F24 (ltng-min 1-1, ltng-max 24-50) | Covered by Greater jewelry elemental damage |
| suffix | 14 | 30 | 85 | dmg-max | of Evisceration L85 F88 (dmg-max 101-120); of Maiming L80 F36 (dmg-max 9-12); of Maiming L79 F48 (dmg-max 13-15); of Quality L77 F96 (dmg-max 8-10) | Covered by Greater Evisceration |
| suffix | 15 | 13 | 85 | dmg-min | of Transcendence L85 F24 (dmg-min 50-60); of Transcendence L82 F36 (dmg-min 30-40); of Performance L81 F32 (dmg-min 10-13); of Transcendence L76 F48 (dmg-min 15-20) | Covered by Greater Transcendence |
| suffix | 16 | 10 | 85 | dmg-pois | of Blight L85 F12 (dmg-pois(75) 377-377); of Anthrax L77 F24 (dmg-pois(50) 309-309); of Venom L65 F12 (dmg-pois(75) 266-266); of Blight L45 F24 (dmg-pois(75) 171-171) | Covered by Greater jewelry elemental damage |
| suffix | 17 | 21 | 80 | dex | of Perfection L80 F36 (dex 20-30); of Perfection L75 F36 (dex 16-20); of Nirvana L72 F36 (dex 21-30); of Precision L60 F36 (dex 10-15) | Covered by Greater Perfection |
| suffix | 18 | 6 | 81 | balance1, balance2, balance3 | of Balance L81 F6 (balance3 10-10); of Truth L44 F48 (balance1 7-7); of Stability L18 F48 (balance3 25-25); of Balance L10 F6 (balance3 5-5) | Covered by Greater Balance |
| suffix | 19 | 8 | 70 | regen | of Regeneration L70 F48 (regen 3-5); of Regrowth L55 F48 (regen 6-9); of Honor L47 F48 (regen 1-4); of Regeneration L40 F48 (regen 3-5) | Covered by Greater Regeneration |
| suffix | 20 | 2 | 44 | noheal | of Vileness L44 F36 (noheal 1-1); of Vileness L9 F36 (noheal 1-1) | Defer: prevent monster heal is binary. |
| suffix | 21 | 3 | 17 | gold% | of Wealth L17 F48 (gold% 41-80); of Greed L1 F48 (gold% 25-40); of Avarice L1 F48 (gold% 10-30) | Covered by Greater Wealth |
| suffix | 22 | 8 | 80 | mag% | of Prosperity L80 F12 (mag% 16-20); of Luck L53 F48 (mag% 36-50); of Prosperity L50 F24 (mag% 11-15); of Luck L36 F48 (mag% 26-35) | Covered by Greater Prosperity |
| suffix | 23 | 19 | 41 | enr | of Enlightenment L41 F36 (enr 21-30); of Wizardry L41 F36 (enr 16-20); of Knowledge L41 F36 (enr 7-9); of Wizardry L31 F36 (enr 16-20) | Covered by Greater Enlightenment |
| suffix | 24 | 1 | 8 | knock | of the Bear L8 F36 (knock 1-1) | Defer: knockback is binary. |
| suffix | 25 | 4 | 17 | att, att%, light | of the Sun L17 F12 (light 5-5, att% 5-5); of Radiance L15 F12 (light 3-3, att 30-30); of Light L6 F12 (light 1-1, att 15-15); of Light L1 F48 (light 1-1, att 10-10) | Defer: light radius plus small AR is not a meaningful chase family. |
| suffix | 26 | 23 | 88 | hp | of Vita L88 F6 (hp 60-70); of Vita L81 F6 (hp 50-60); of the Colosuss L75 F36 (hp 41-60); of the Mammoth L68 F36 (hp 31-40) | Covered by Greater Vita |
| suffix | 27 | 10 | 85 | lifesteal | of the Lamprey L85 F24 (lifesteal 6-6); of the Lamprey L77 F48 (lifesteal 7-8); of the Locust L57 F24 (lifesteal 4-5); of the Lamprey L55 F84 (lifesteal 8-9) | Covered by Greater Lamprey/Vampire |
| suffix | 28 | 10 | 86 | manasteal | of the Vampire L86 F24 (manasteal 6-8); of the Vampire L78 F48 (manasteal 7-8); of the Wraith L58 F48 (manasteal 5-6); of the Wraith L58 F24 (manasteal 4-5) | Covered by Greater Lamprey/Vampire |
| suffix | 29 | 4 | 44 | res-pois-len | of Defiance L44 F24 (res-pois-len 75-90); of Amelioration L25 F36 (res-pois-len 50-74); of Remedy L18 F36 (res-pois-len 25-49); of Remedy L1 F36 (res-pois-len 10-24) | Optional: poison length reduction is utility-only. |
| suffix | 30 | 3 | 25 | ease | of Simplicity L25 F24 (ease -30--30); of Ease L15 F36 (ease -20--20); of Freedom L1 F36 (ease -15--15) | Optional: requirements reduction is strong utility but needs item-scope balance. |
| suffix | 31 | 25 | 74 | dex, enr, str, vit | of the Titan L74 F36 (str 16-20); of Atlus L71 F36 (str 21-30); of Energy L61 F4 (enr 5-8); of the Giant L59 F36 (str 10-15) | Covered by Greater Titan |
| suffix | 35 | 7 | 81 | move1, move2, move3, stamdrain | of Inertia L81 F6 (move3 10-10); of Traveling L65 F48 (move3 30-30, stamdrain 80-90); of Acceleration L51 F48 (move3 40-40); of Speed L37 F48 (move3 30-30) | Covered by Greater Inertia |
| suffix | 37 | 2 | 20 | rep-dur | of Fast Repair L20 F12 (rep-dur(5) -); of Self-Repair L3 F36 (rep-dur(3) -) | Defer: repair rate needs durability-system review. |
| suffix | 39 | 3 | 50 | indestruct, rep-quant | of Ages L50 F12 (indestruct 1-1); of Propogation L24 F60 (rep-quant(25) -); of Replenishing L5 F72 (rep-quant(25) -) | Defer: indestructible/repair quantity is utility-binary. |
| suffix | 41 | 4 | 66 | hp/lvl, mana/lvl | of the Elephant L66 F24 (hp/lvl(4) -, mana/lvl(2) -); of the Elephant L37 F24 (hp/lvl(4) -, mana/lvl(2) -); of the Kraken L20 F12 (hp/lvl(6) -); of Memory L20 F12 (mana/lvl(6) -) | Covered by Greater Elephant |
| suffix | 42 | 19 | 86 | all-stats, dex%, dex/lvl, enr%, str%, str/lvl, vit% | of the Zodiac L86 F12 (all-stats 21-30); of Agility2 L75 F12 (dex% 21-30); of Power2 L75 F12 (str% 21-30); of Endurance2 L75 F12 (vit% 21-30) | Covered by Greater Zodiac |
| suffix | 43 | 11 | 77 | res-cold/lvl, res-fire/lvl, res-ltng/lvl, res-pois/lvl | of the Elements L77 F24 (res-cold/lvl(5) -, res-fire/lvl(5) -, res-ltng/lvl(5) -); of the Elements L44 F24 (res-cold/lvl(4) -, res-fire/lvl(4) -, res-ltng/lvl(4) -); of the Yeti L20 F12 (res-cold/lvl(6) -); of the Phoenix L20 F12 (res-fire/lvl(6) -) | Covered by Greater Elements |
| suffix | 44 | 8 | 72 | charged | of Apocalypse L72 F1 (charged(401) -20--1); of Rancor L36 F1 (charged(396) -20--4); of Apocalypse L36 F1 (charged(401) -60--3); of Lethargy L24 F1 (charged(393) -20--5) | Defer: charged-skill affixes are technical. |
| suffix | 60 | 3 | 87 | lifesteal, manasteal | of the Lich L87 F12 (manasteal 8-9, lifesteal 10-12); of the Lich L66 F12 (manasteal 6-7, lifesteal 8-9); of the Lich L44 F12 (manasteal 3-5, lifesteal 5-7) | Covered by Greater Lich |
| suffix | 61 | 3 | 51 | ac | of Guarding L51 F60 (ac 26-50); of Defense1 L33 F60 (ac 11-25); of Defense1 L12 F60 (ac 5-10) | Covered by Greater Guarding |
| suffix | 63 | 3 | 57 | cheap | of Charming1 L57 F6 (cheap 5-6); of Haggling1 L33 F8 (cheap 3-4); of Bartering1 L13 F12 (cheap 1-2) | Optional utility: vendor price reduction can be revisited after combat affixes. |
| suffix | 64 | 4 | 62 | slow | Paralysis1 L62 F24 (slow 21-25); Daze1 L46 F24 (slow 16-20); Stunning1 L32 F24 (slow 11-15); Startling L16 F24 (slow 5-10) | Covered by Greater Paralysis |
| suffix | 65 | 3 | 61 | stupidity | of Blindness1 L61 F12 (stupidity 3-3); of Blindness1 L44 F12 (stupidity 2-2); of Blindness1 L23 F12 (stupidity 1-1) | Covered by Greater Blindness |
| suffix | 66 | 1 | 51 | reanimate | of Reanimation1 L51 F12 (reanimate(5) 3-5) | Covered by Greater Reanimation |
| suffix | 67 | 10 | 87 | heal-kill, res-all-max, res-cold-max, res-fire-max, res-ltng-max, res-pois-max | of the Four Seasons2 L87 F12 (res-all-max 4-6); of the Soul2 L75 F24 (heal-kill 16-25); of the Four Seasons2 L68 F24 (res-all-max 1-3); of the Dragon's Spirit2 L55 F24 (heal-kill 9-15) | Covered by Greater Four Seasons |
| suffix | 77 | 145 | 80 | gethit-skill | of Hydras L80 F1 (gethit-skill(62) 12-19); of Frozen Orbs L80 F1 (gethit-skill(64) 4-22); of Revivification L80 F1 (gethit-skill(95) 7-10); of Lower Resistance L77 F1 (gethit-skill(91) 6-18) | Defer: get-hit proc affixes need proc-specific balance. |
| suffix | 78 | 62 | 80 | hit-skill | of Hydras L80 F1 (hit-skill(62) 2-21); of Lightning Fury L70 F1 (hit-skill(35) 9-15); of Meteors L62 F1 (hit-skill(56) 5-19); of Novas L60 F1 (hit-skill(48) 6-21) | Defer: on-hit proc affixes need proc-specific balance. |
| suffix | 79 | 24 | 55 | death-skill, levelup-skill | of Battle Orders L55 F4 (levelup-skill(Battle Orders) 100-39); of Hurricane L55 F4 (levelup-skill(Hurricane) 100-22); of Frozen Orbs L48 F2 (death-skill(Frozen Orb) 100-48); of Poison Novas L48 F2 (death-skill(Poison Nova) 100-48) | Defer: level-up/death proc affixes are event proc systems. |
| suffix | 80 | 4 | 20 | healperhit | of Draining L20 F8 (healperhit 1-3); of Funneling L20 F6 (healperhit 4-6); of Pumping L20 F4 (healperhit 7-9); of Siphoning L20 F2 (healperhit 10-12) | Covered by Greater Draining |
| suffix | 81 | 3 | 30 | charge-noconsume, extra_bonespears, extra_holybolt | of Splitting L30 F64 (extra_bonespears 1-1); of Splitting L30 F64 (extra_holybolt 1-1); of Mosaic L30 F64 (charge-noconsume 50-50) | Defer: class-special mechanics, not broad Greater rows. |
| suffix | 200 | 3 | 80 | swing1 | of the Swift L80 F3 (swing1 20-30); of the Swift L45 F6 (swing1 10-20); of the Swift L1 F9 (swing1 5-10) | Covered by Greater missile suffixes |
| suffix | 201 | 9 | 80 | deadly, openwounds, pierce | of Slaying L80 F3 (deadly 15-20); of Maiming L80 F3 (openwounds 15-20); of Piercing L80 F3 (pierce 20-30); of Slaying L45 F6 (deadly 10-15) | Covered by Greater missile suffixes |
| suffix | 202 | 3 | 80 | lifesteal | of the Vampire L80 F3 (lifesteal 5-10); of the Vampire L45 F6 (lifesteal 3-5); of the Vampire L1 F9 (lifesteal 2-3) | Covered by Greater missile suffixes |
| suffix | 203 | 3 | 80 | manasteal | of the Bat L80 F3 (manasteal 5-10); of the Bat L45 F6 (manasteal 3-5); of the Bat L1 F9 (manasteal 2-3) | Covered by Greater missile suffixes |
| suffix | 204 | 15 | 80 | res-all, res-cold, res-fire, res-ltng, res-pois | of Resistance L80 F3 (res-fire 20-30); of Resistance L80 F3 (res-cold 20-30); of Resistance L80 F3 (res-ltng 20-30); of Resistance L80 F3 (res-pois 20-30) | Covered by Greater missile suffixes |
| suffix | 205 | 3 | 50 | gold%, mag% | of Fortune L50 F3 (mag% 25-40, gold% 50-80); of Fortune L45 F6 (mag% 15-25, gold% 30-50); of Fortune L1 F9 (mag% 10-15, gold% 20-30) | Covered by Greater missile suffixes |
| suffix | 206 | 6 | 85 | hit-skill, pierce-dmg, pierce-elem, pierce-mag | of Transcendence L85 F1 (hit-skill(Lower Resist) 10-10, pierce-elem 10-15); of Transcendence L85 F1 (hit-skill(Amplify Damage) 10-10, pierce-dmg 10-15); of Transcendence L85 F1 (hit-skill(Weaken) 10-10, pierce-mag 10-15); of Transcendence L50 F3 (hit-skill(Lower Resist) 10-5) | Covered by Greater missile suffixes |
| suffix | 307 | 30 | 92 | pierce-cold, pierce-dmg, pierce-fire, pierce-ltng, pierce-mag, pierce-pois | of Acidity L92 F1 (pierce-pois(1) 1-1); of Acidity L92 F1 (pierce-pois(1) 1-2); of Acidity L92 F1 (pierce-pois(1) 1-3); of Acidity L92 F1 (pierce-pois(1) 1-4) | Defer/exempt: special rare-only pierce rows with mixed charm/non-charm scopes. |

## Immediate Review Questions

1. Are any apex groups incorrectly marked as deferred when they should receive a Greater candidate in Phase 2?
2. Do any groups currently covered by one broad candidate need to be split by item scope, especially `group 125` skills, `group 209` caster damage/pierce, and missile-only groups?
3. Are the listed odds rare enough for Phase 2, or should late Greater frequencies generally be `1` instead of `3` for high-impact affixes?
4. Do any proposed Greater ranges exceed sane balance limits before implementation?
