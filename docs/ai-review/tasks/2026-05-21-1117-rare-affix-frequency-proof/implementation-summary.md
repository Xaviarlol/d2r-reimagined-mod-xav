# Implementation Summary

## Scope

This follow-up reviewed the rare-affix frequency math after the top-50 Greater Affix implementation. It adds a before/after chance simulation and fixes one Phase 1 split edge case the simulation exposed.

Changed files:

- `data/global/excel/magicsuffix.txt`
- `data/global/excel/base/magicsuffix.txt`
- `scripts/implement_rare_affix_rework.py`
- `docs/affix-chance-simulation-summary-2026-05-21.md`
- `docs/affix-chance-simulation-2026-05-21.tsv`

## Baseline

The simulation baseline is `00337b07^` (`103603327bda35f29f01431f15b49e11e363f077`), the commit before `00337b07 Implement rare affix rework`.

## Method

The simulation uses weighted one-roll prefix/suffix probability:

```text
affix frequency / total eligible same-side affix pool
```

This is a frequency sanity check, not a full rare item generator with group lockouts and prefix/suffix count rolls.

The simulation reports:

- structural preservation of original affix fingerprints
- original-level frequency totals vs expected `vanilla frequency * 10`
- split-row overlap detection from levels 1-100
- same-level gameplay-pool deltas at alvl `20`, `35`, `50`, `66`, `81`, `90`, and `100`

## Bug Found And Fixed

The first simulation found four level-1 suffixes where Phase 1 had created overlapping early/late rows:

- `of Grace`
- `of Power`
- `of Greed`
- `of Avarice`

Because the original level was already `1`, the generated early copy had `level=1 maxlevel=1`, while the late copy also started at `level=1`. Both were eligible at level 1, making these affixes 15x baseline frequency instead of the intended 10x baseline frequency.

Fix:

- Removed the four overlapping early rows from active/base `magicsuffix.txt`.
- Updated `scripts/implement_rare_affix_rework.py` so original `level <= 1` rows are not split in future regenerations.

## Post-Fix Results

```text
Original spawnable rare affix fingerprints missing from current non-Greater rows: 0
Original-level current frequency mismatches vs expected vanilla frequency * 10: 0
Split-row overlap cases detected from levels 1-100: 0
Endgame sample max absolute non-Greater-only delta at alvl 90/100: 0.000000000000%
Endgame sample max absolute full-pool delta at alvl 90/100: 1.901975%
```

Interpretation:

- At alvl 90/100, non-Greater affix proportions are exactly preserved.
- The remaining full-pool endgame dilution is from adding eligible Greater rows.
- Low/mid-level deltas are expected because Phase 1 intentionally lowers affix levels by 30%, letting higher affixes enter earlier item-level pools.

## Additional Validation

Checked after the fix:

```text
data/global/excel/magicprefix.txt rows 1488 cols 40 bad_rows 0
data/global/excel/magicsuffix.txt rows 1006 cols 40 bad_rows 0
data/global/excel/properties.txt rows 486 cols 38 bad_rows 0
data/global/excel/itemstatcost.txt rows 488 cols 52 bad_rows 0
data/global/excel/base/magicprefix.txt rows 1488 cols 40 bad_rows 0
data/global/excel/base/magicsuffix.txt rows 1006 cols 40 bad_rows 0
data/global/excel/base/properties.txt rows 486 cols 38 bad_rows 0
data/global/excel/base/itemstatcost.txt rows 488 cols 52 bad_rows 0
```

Active/base prefix and suffix files are identical for the checked pairs.

## Publish Status

Not live-published. This review is requested before any deploy to `E:\Diablo II Resurrected`.
