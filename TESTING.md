# Damage validation harness

This branch wires a passive **Training Dummy** monster into Cold Plains so
damage formulas can be ground-truthed against the engine. The companion
calculator (`d2r-reimagined-calc` repo) predicts per-skill damage from gear,
skill points, and target profile; the dummy lets you compare predictions
against the actual game.

## What the patch does

- **`data/global/excel/monstats.txt`** — adds `training_dummy` (hcIdx 773).
  100,000 HP across all difficulties, 0 AC, 0% resistances, 0 attack damage,
  AI=Idle, no regen, no on-hit elemental, no drops, no XP.
- **`data/global/excel/superuniques.txt`** — repoints Bishibosh's `Class`
  from `fallenshaman1` to `training_dummy`. Removes mods/group/treasure so the
  dummy spawns clean.
- **`data/global/excel/weapons.txt`** — flattens `sst` (Short Staff) to
  100/100 damage, 1h and 2h. Eliminates weapon roll variance for tests.

## Test protocol

1. Roll a fresh Assassin (offline, /players1).
2. Equip only the modified Short Staff. Strip everything else.
3. Walk to Cold Plains. Bishibosh's spawn point now has the Training Dummy.
4. Bring a clean inventory (no charms, no jewelry) so no random affixes
   confound the test.
5. Pick a skill. Assassin skills with allocated points appear in the calc
   when you replicate the same build there. Pin both numbers side by side.
6. Hit the dummy. Read the floating damage numbers.
7. Compare to the calculator's predicted range.

## What a passing test looks like

For a pure-physical attack with the flat 100 staff:
- Calc predicts: 100 × (1 + ED%/100) × skill multiplier
- Observed: floating number per swing should land in that exact range,
  with no variance from weapon roll.

For an elemental skill (e.g. Fire Trauma at slvl 1):
- Calc reads `EMin`/`EMax` from the missile, applies synergy from
  `EDmgSymPerCalc`, applies player's `+%fire skill damage`, applies enemy
  fire resistance (0 on the dummy).
- Observed should match within the missile's own min-max spread.

Any persistent gap is a bug in the calculator or a wrong assumption about
the formula.

## Cleanup

These changes are scoped to a feature branch (`claude/review-codebase-BPWDq`).
Don't merge into `next` unless you want the Cold Plains encounter
permanently replaced. The cleanest route to ship the calculator is
to keep this branch around for validation, run tests against it, then
discard the testing changes when the formula coverage is verified.

To revert locally:
```
git checkout next -- data/global/excel/monstats.txt \
                     data/global/excel/superuniques.txt \
                     data/global/excel/weapons.txt
```
