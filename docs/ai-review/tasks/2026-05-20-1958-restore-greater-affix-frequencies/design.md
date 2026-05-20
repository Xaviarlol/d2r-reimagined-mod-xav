# Greater Affix Frequency Restore Plan

## Context

The live/repo affix files are currently in an intentional high-frequency test state:

- All non-Greater affix rows were compressed to `frequency=1`.
- All Greater Affix rows were boosted to `frequency=999999`.
- This was done so Eric could prove Greater Affixes spawn and test the gold marker tooltip line.

The next step, after Eric finishes testing, is to restore the intended rare-affix frequency weights while keeping the later fixes that made Greater Affixes visible and identifiable.

## Clean Restore Anchor

Use the frequency column from commit `00337b07` (`Implement rare affix rework`) as the canonical source.

Validation already performed by Codex:

- `00337b07` and `6e2d5a87` have identical `frequency` columns for both `magicprefix.txt` and `magicsuffix.txt`.
- `6e2d5a87` is the last clearly pre-temporary-boost checkpoint in the visible history.
- Current row counts still match the clean source:
  - `magicprefix.txt`: 1797 rows.
  - `magicsuffix.txt`: 1355 rows.

Do not checkout whole files from either old commit. Whole-file checkout would risk reverting later good changes, especially:

- Greater `spawnable=1`.
- Embedded marker property wrappers such as `greater_m_ac%`.
- The safe gold `GreaterAffixMarker` string.

## Planned Implementation

For each of these four files:

- `data/global/excel/magicprefix.txt`
- `data/global/excel/base/magicprefix.txt`
- `data/global/excel/magicsuffix.txt`
- `data/global/excel/base/magicsuffix.txt`

Perform a column-only restore:

1. Read the current file.
2. Read the matching source file from `00337b07`.
3. Assert the header contains `frequency`.
4. Assert row counts match.
5. Assert row names match by row index well enough to catch drift.
6. Copy only the source `frequency` value into the current row.
7. Preserve every other current column value.
8. Write the TSV with original column order and trailing empty fields preserved.
9. Apply the same result to active and `base` copies.
10. Verify active/base copies are identical after restore.

## Expected Frequency Restoration

### `magicprefix.txt`

Current test distribution:

| frequency | rows |
|---:|---:|
| 1 | 1287 |
| 999999 | 510 |

Restored intended distribution:

| frequency | rows |
|---:|---:|
| 1 | 221 |
| 2 | 116 |
| 3 | 59 |
| 4 | 53 |
| 5 | 14 |
| 6 | 20 |
| 7 | 1 |
| 8 | 16 |
| 9 | 1 |
| 10 | 388 |
| 12 | 2 |
| 14 | 1 |
| 16 | 1 |
| 20 | 374 |
| 24 | 1 |
| 30 | 64 |
| 37 | 1 |
| 40 | 127 |
| 50 | 10 |
| 60 | 88 |
| 70 | 1 |
| 73 | 1 |
| 80 | 75 |
| 90 | 10 |
| 100 | 17 |
| 110 | 1 |
| 120 | 51 |
| 140 | 5 |
| 160 | 2 |
| 240 | 49 |
| 260 | 2 |
| 550 | 1 |
| 1100 | 11 |
| 1140 | 4 |
| 1500 | 9 |

Rows whose `frequency` changes back: 1797.

### `magicsuffix.txt`

Current test distribution:

| frequency | rows |
|---:|---:|
| 1 | 956 |
| 999999 | 399 |

Restored intended distribution:

| frequency | rows |
|---:|---:|
| 1 | 24 |
| 2 | 20 |
| 3 | 13 |
| 4 | 32 |
| 6 | 7 |
| 8 | 42 |
| 10 | 278 |
| 11 | 2 |
| 12 | 39 |
| 16 | 55 |
| 20 | 26 |
| 21 | 2 |
| 24 | 35 |
| 25 | 1 |
| 28 | 4 |
| 29 | 1 |
| 30 | 28 |
| 32 | 40 |
| 36 | 15 |
| 40 | 23 |
| 48 | 40 |
| 50 | 10 |
| 51 | 1 |
| 56 | 4 |
| 59 | 1 |
| 60 | 60 |
| 64 | 1 |
| 72 | 2 |
| 76 | 1 |
| 80 | 2 |
| 84 | 4 |
| 88 | 1 |
| 90 | 12 |
| 96 | 2 |
| 100 | 26 |
| 120 | 119 |
| 144 | 1 |
| 160 | 2 |
| 180 | 15 |
| 200 | 7 |
| 240 | 108 |
| 300 | 3 |
| 320 | 6 |
| 360 | 81 |
| 380 | 1 |
| 420 | 4 |
| 440 | 1 |
| 480 | 106 |
| 600 | 11 |
| 640 | 3 |
| 720 | 7 |
| 760 | 1 |
| 840 | 8 |
| 880 | 1 |
| 960 | 5 |
| 1120 | 1 |
| 1280 | 1 |
| 1440 | 1 |
| 1600 | 1 |
| 1680 | 1 |
| 1760 | 1 |
| 1920 | 5 |

Rows whose `frequency` changes back: 1355.

## Validation After Implementation

Before commit/publish:

1. Count TSV columns for every row in all four edited files.
2. Compare active/base files and confirm byte-identical pairs:
   - `magicprefix.txt` == `base/magicprefix.txt`
   - `magicsuffix.txt` == `base/magicsuffix.txt`
3. Confirm no current `frequency=999999` remains in prefix/suffix files.
4. Confirm Greater rows still have `spawnable=1` and `rare=1`.
5. Confirm `properties.txt` still has `greater_m_` wrappers with embedded `item_greaterAffixMarker`.
6. Commit and push.
7. Publish to the live folder only after Eric says to restore/publish.

## Known Non-Goals

- Do not change Greater Affix levels, `maxlevel`, `levelreq`, groups, mod columns, or marker properties.
- Do not change magic/rare affix generation rules.
- Do not alter `itemstatcost.txt` or localization strings.
- Do not remove the gold `GREATER AFFIX:` marker.
