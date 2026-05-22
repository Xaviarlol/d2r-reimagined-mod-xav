# Greater Affix Quality Pass

Generated from current live data files at affix level 90.

## Summary

- Greater variants audited: 85
- Greater row count: 255
- Missing Greater affix name strings: 0
- Missing property references in Greater rows: 0
- Functional generic marker/hybrid refs in Greater rows: 0
- Greater variants missing exact early/mid/late bands: 0
- Greater rows not spawnable rare: 0
- Duplicate same-payload overlap warnings: 11
- Per-affix-roll chance outliers >= 1% at alvl 90: 1
- Approx three-roll chance outliers >= 1% at alvl 90: 11

## Findings

- Duplicate same-payload overlap warnings:
  - prefix group 209: duplicate Greater payload `Greater Frost Wyrm's Damage` overlaps item types orb, staf, wand; scopes `wand,orb,staf` and `wand,orb,staf,helm` both apply.
  - prefix group 209: duplicate Greater payload `Greater Frost Wyrm's Pierce` overlaps item types orb, staf, wand; scopes `wand,orb,staf` and `wand,orb,staf,helm` both apply.
  - prefix group 101: duplicate Greater payload `Greater Godly` overlaps item types ashd, grim, head, shie, tors; scopes `armo,shld` and `tors,shld` both apply.
  - prefix group 209: duplicate Greater payload `Greater Manticore's Damage` overlaps item types staf, wand; scopes `wand,staf` and `wand,staf,helm` both apply.
  - prefix group 209: duplicate Greater payload `Greater Manticore's Pierce` overlaps item types staf, wand; scopes `wand,staf` and `wand,staf,helm` both apply.
  - prefix group 125: duplicate Greater payload `Greater Priest's` overlaps item types ashd; scopes `scep,ashd` and `swor,mace,hamm,shld` both apply.
  - prefix group 209: duplicate Greater payload `Greater Pyromaniac's Damage` overlaps item types orb, staf, wand; scopes `wand,orb,staf` and `wand,orb,staf,helm` both apply.
  - prefix group 209: duplicate Greater payload `Greater Pyromaniac's Pierce` overlaps item types orb, staf, wand; scopes `wand,orb,staf` and `wand,orb,staf,helm` both apply.
  - prefix group 209: duplicate Greater payload `Greater Zeus's Damage` overlaps item types orb, staf, wand; scopes `wand,orb,staf` and `wand,orb,staf,helm` both apply.
  - prefix group 209: duplicate Greater payload `Greater Zeus's Pierce` overlaps item types orb, staf, wand; scopes `wand,orb,staf` and `wand,orb,staf,helm` both apply.
  - suffix group 14: duplicate Greater payload `of Greater Evisceration` overlaps item types abow, ajav, aspe, axe, bow, club, h2h, h2h2, hamm, jave, knif, mace; scopes `weap` and `weap` both apply.
- High per-roll chance outliers:
  - prefix `Greater Godly` group 101 max 1.395231% on `boot` stats `ga_godly_ac% 300-300; ga_godly_red-dmg% 30-30`
- High approximate three-roll chance outliers:
  - prefix `Greater Godly` group 101 approx 4.127564% if the rare gets three same-side rolls; single-roll max 1.395231% on `boot` stats `ga_godly_ac% 300-300; ga_godly_red-dmg% 30-30`
  - suffix `of Greater Evisceration` group 14 approx 1.813101% if the rare gets three same-side rolls; single-roll max 0.608057% on `staf` stats `dmg-max 165-165`
  - suffix `of Greater Speed` group 35 approx 1.462500% if the rare gets three same-side rolls; single-roll max 0.489896% on `boot` stats `move3 15-15`
  - suffix `of Greater Traveling` group 35 approx 1.462500% if the rare gets three same-side rolls; single-roll max 0.489896% on `boot` stats `move3 15-15; stamdrain 117-117`
  - suffix `of the Greater Apprentice` group 9 approx 1.444407% if the rare gets three same-side rolls; single-roll max 0.483806% on `orb` stats `cast1 13-13`
  - suffix `of Greater Equilibrium` group 18 approx 1.349813% if the rare gets three same-side rolls; single-roll max 0.451977% on `belt` stats `balance2 26-26`
  - suffix `of Greater Alacrity` group 7 approx 1.328641% if the rare gets three same-side rolls; single-roll max 0.444856% on `glov` stats `swing2 26-26`
  - suffix `of Greater Deflecting` group 8 approx 1.264825% if the rare gets three same-side rolls; single-roll max 0.423398% on `grim,shie` stats `block 40-40; block2 40-40`
  - suffix `of the Greater Magus` group 9 approx 1.204645% if the rare gets three same-side rolls; single-roll max 0.403172% on `orb` stats `cast3 25-25`
  - suffix `of Greater Evisceration` group 14 approx 1.105240% if the rare gets three same-side rolls; single-roll max 0.369779% on `bow,xbow` stats `dmg-max 165-165`
  - suffix `of Greater Fervor` group 7 approx 1.096214% if the rare gets three same-side rolls; single-roll max 0.366748% on `cjwl,jewl` stats `swing1 20-20`
- Cosmetic stale description labels still mention `marker=ga_`:
  - 249 rows affected. This is internal/comment text, not a functional mod.

## Chance Model

- The table reports chance per eligible prefix/suffix selection roll, not full item drop odds.
- Full rare-item chance is lower or higher depending on how many affixes and how many prefix/suffix slots the rare receives.
- `approx_three_roll_max_pct` is the upper-bound style estimate if a rare receives three same-side rolls for the item type with the highest observed per-roll chance.
- Chance pool is evaluated at affix level 90; early and mid bands are shown for frequency documentation but are not active at alvl 90.

Detailed table: `greater-affix-final-table-2026-05-22.tsv`
