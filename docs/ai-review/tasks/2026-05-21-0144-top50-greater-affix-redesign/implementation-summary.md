# Implementation Summary

## Scope

Implemented the approved top-50 Greater Affix redesign.

Changed files:

- `data/global/excel/magicprefix.txt`
- `data/global/excel/base/magicprefix.txt`
- `data/global/excel/magicsuffix.txt`
- `data/global/excel/base/magicsuffix.txt`
- `data/global/excel/properties.txt`
- `data/global/excel/base/properties.txt`
- `data/global/excel/itemstatcost.txt`
- `data/global/excel/base/itemstatcost.txt`
- `data/local/lng/strings/item-modifiers.json`
- `scripts/implement_top50_greater_affixes.py`
- `scripts/implement_rare_affix_rework.py`
- `docs/affix-chance-simulation-summary-2026-05-21.md`
- `docs/affix-chance-simulation-2026-05-21.tsv`

## What Changed

- Removed the broad Greater Affix experiment from prefix/suffix tables.
- Kept the approved 50 logical Greater families.
- Emitted 201 prefix Greater rows and 54 suffix Greater rows from selected source variants.
- Converted gameplay stats back to normal gameplay property codes instead of `greater_m_` colored gameplay wrappers.
- Added 50 `ga_marker_*` itemstats, one per logical Greater family.
- Added 50 `ga_*` marker properties and 3 `ga_h_*` hybrid marker properties.
- Compacted `itemstatcost.txt` to sequential IDs with max ID `487`.
- Rebuilt Greater aura rows with verified Paladin aura params:
  - Might `98`
  - Holy Freeze `114`
  - Vigor `115`
  - Meditation `120`
  - Fanaticism `122`
  - Conviction `123`
- Added localized marker strings such as `GreaterAffix_grandmasters`, displayed as `Greater Affix: Grandmaster's`.
- Fixed a Phase 1 split edge case where four level-1 suffixes had overlapping early/late rows and therefore 15x baseline frequency instead of 10x:
  - `of Grace`
  - `of Power`
  - `of Greed`
  - `of Avarice`

## Validation Run

Script output:

```text
prefix greater rows: 201
suffix greater rows: 54
logical families: 50
hybrid properties: 0
itemstatcost max ID: 487
```

Independent checks:

```text
data/global/excel/magicprefix.txt rows 1488 cols 40 bad []
data/global/excel/magicsuffix.txt rows 1006 cols 40 bad []
data/global/excel/properties.txt rows 486 cols 38 bad []
data/global/excel/itemstatcost.txt rows 488 cols 52 bad []
magicprefix.txt active_base_identical True
magicsuffix.txt active_base_identical True
properties.txt active_base_identical True
itemstatcost.txt active_base_identical True

data/global/excel/magicprefix.txt 201 bad 0 []
data/global/excel/magicsuffix.txt 54 bad 0 []
ga properties 53 hybrid 3
stats max 487 sequential True markers 50
top50 marker strings 50 missing []
total keys 564 duplicate keys 0
```

Cleanup check:

```text
rg -n "greater_m_|greater-affix-marker|item_greaterAffixMarker|greater_item_|^greater_" data/global/excel/magicprefix.txt data/global/excel/magicsuffix.txt data/global/excel/properties.txt data/global/excel/itemstatcost.txt
```

No matches.

Frequency sanity simulation against the pre-rare-rework baseline (`00337b07^`) is recorded in:

- `docs/affix-chance-simulation-summary-2026-05-21.md`
- `docs/affix-chance-simulation-2026-05-21.tsv`

Key results:

```text
Original spawnable rare affix fingerprints missing from current non-Greater rows: 0
Original-level current frequency mismatches vs expected vanilla frequency * 10: 0
Split-row overlap cases detected from levels 1-100: 0
Endgame sample max absolute non-Greater-only delta at alvl 90/100: 0.000000000000%
Endgame sample max absolute full-pool delta at alvl 90/100: 1.901975%
```

The low/mid-level same-alvl deltas are expected because the Phase 1 design intentionally lowers affix levels by 30%, causing higher affixes to enter earlier item-level pools. At alvl 90/100, non-Greater affix proportions are exactly preserved; the remaining full-pool dilution is from adding eligible Greater rows.

## Known Existing Data Issue Not Changed

The implementation script originally found pre-existing group `307` rows referencing property codes such as `Breaching-Affix1`, `Gelid-Affix1`, and similar names that do not exist in `properties.txt`. Those rows predate this change and are outside the Greater Affix implementation, so validation is scoped to the new Greater rows and their new marker/hybrid properties.

## Publish Status

Not published to the live game folder. This should receive Claude `code_review` first, then publish only after approval or explicit override.
