# Design Notes

## Intent

For testing, normalize Cobra Strike's three charge payloads so the flat poison component is no longer a confounding variable.

## Proposed Data Behavior

- Charge 1: 100% weapon damage plus the same flat poison curve as charge 3, over 2 seconds.
- Charge 2: 100% weapon damage plus the same flat poison curve as charge 3, over 2 seconds.
- Charge 3: unchanged functional nova behavior, but its helper skill row is normalized to the same flat poison curve as the missile/tooltip.

## Data Changes

- `data/global/excel/skills.txt`
  - `Cobra Strike`: set poison flat rate curve to the existing `cobrastrikenova` missile / charge-3 tooltip curve.
  - `Cobra Strike`: set `ELen` from `100` to `50`, making charge 1/2 poison total display over 2 seconds instead of 4.
  - `Cobra Strike`: keep `SrcDam` at `128` for 100% weapon damage.
  - `Cobra Strike Nova`: normalize helper skill flat poison curve to the same curve.
- `data/global/excel/base/skills.txt`
  - Mirrored changes.
- `data/global/excel/skilldesc.txt`
  - Charge 1, charge 2, and charge 3 tooltip formulas all use the same flat poison calculation.
- `data/global/excel/base/skilldesc.txt`
  - Mirrored changes.

## Explicit Non-Changes

- `data/global/excel/missiles.txt` was not changed because `cobrastrikenova` already uses the target 2-second flat poison curve and `SrcDamage 128`.
- Radius behavior was not changed.
- Tiger Strike synergy remained unchanged.
- No live publish has been done for this review round.

## Validation Already Run

- TSV column counts checked for active/base `skills.txt`, `skilldesc.txt`, and `missiles.txt`.
- Diff generated at `diff.patch`.
