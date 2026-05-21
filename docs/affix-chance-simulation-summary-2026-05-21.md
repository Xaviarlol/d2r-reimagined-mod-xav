# Affix Chance Simulation - 2026-05-21

Baseline ref: `00337b07^` (`103603327bda35f29f01431f15b49e11e363f077`), the commit before `00337b07 Implement rare affix rework`.

Method: weighted one-roll prefix/suffix probability, `affix frequency / total eligible same-side pool`. This is the frequency sanity check, not a full rare item generator with group lockout and prefix/suffix count rolls.

## Structural Frequency Audit

- Original spawnable rare affix fingerprints missing from current non-Greater rows: 0
- Original-level current frequency mismatches vs expected `vanilla frequency * 10`: 0
- Split-row overlap cases detected from levels 1-100: 0

## Same-Level Gameplay Pool Simulation

These deltas include the intentional 30% affix-level compression. Low/mid-level rows can change because higher affixes enter the same item level earlier than vanilla. Endgame levels are the useful check for pure frequency preservation.

| alvl | cases | avg non-Greater delta % | max non-Greater delta % | min non-Greater delta % | avg full delta % | max full delta % | min full delta % |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 20 | 6484 | -19.235696 | 0.000000 | -35.606936 | -19.235696 | 0.000000 | -35.606936 |
| 35 | 9215 | -19.467133 | 0.000000 | -63.636364 | -19.467133 | 0.000000 | -63.636364 |
| 50 | 9758 | -19.657217 | 0.000000 | -45.341615 | -19.872315 | 0.000000 | -45.598417 |
| 66 | 10537 | -16.722978 | 0.000000 | -51.895425 | -17.169281 | 0.000000 | -52.368625 |
| 81 | 11169 | -3.166197 | 0.000000 | -9.311224 | -4.007021 | 0.000000 | -11.013767 |
| 90 | 11724 | 0.000000 | 0.000000 | 0.000000 | -0.852188 | 0.000000 | -1.901975 |
| 100 | 11724 | 0.000000 | 0.000000 | 0.000000 | -0.852188 | 0.000000 | -1.901975 |

Endgame sample max absolute non-Greater-only delta at alvl 81/90/100: 9.311224489796%
Endgame sample max absolute non-Greater-only delta at alvl 90/100: 0.000000000000%
Endgame sample max absolute full-pool delta at alvl 90/100: 1.901975%

## Largest Full-Pool Deltas

| side | item | alvl | affix | group | baseline % | after incl. Greater % | delta % | greater pool | full pool |
|---|---|---:|---|---:|---:|---:|---:|---:|---:|
| prefix | lcha | 35 | Fine | 110 | 33.333333 | 12.121212 | -63.636364 | 0 | 1980 |
| prefix | lcha | 35 | Fine | 110 | 16.666667 | 6.060606 | -63.636364 | 0 | 1980 |
| prefix | lcha | 35 | Forked | 103 | 16.666667 | 6.060606 | -63.636364 | 0 | 1980 |
| prefix | lcha | 35 | Snowflake | 137 | 33.333333 | 12.121212 | -63.636364 | 0 | 1980 |
| prefix | armo | 66 | Consecrated | 101 | 29.891304 | 14.237639 | -52.368625 | 76 | 7726 |
| prefix | armo | 66 | Saintly | 101 | 29.891304 | 14.237639 | -52.368625 | 76 | 7726 |
| prefix | armo | 66 | Paradox | 101 | 6.521739 | 3.106394 | -52.368625 | 76 | 7726 |
| prefix | armo | 66 | Paradox | 101 | 6.521739 | 3.106394 | -52.368625 | 76 | 7726 |
| prefix | armo | 66 | Ghostly | 101 | 1.086957 | 0.517732 | -52.368625 | 76 | 7726 |
| prefix | armo | 66 | Spectral1 | 101 | 1.086957 | 0.517732 | -52.368625 | 76 | 7726 |
| prefix | armo | 66 | Lapis | 117 | 2.173913 | 1.035465 | -52.368625 | 76 | 7726 |
| prefix | armo | 66 | Cobalt | 117 | 1.630435 | 0.776598 | -52.368625 | 76 | 7726 |

Full TSV: `docs\affix-chance-simulation-2026-05-21.tsv`
