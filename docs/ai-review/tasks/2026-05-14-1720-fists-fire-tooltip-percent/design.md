# Fists of Fire Tooltip Percent Fix

## Problem

The English Fists of Fire charge 1 and charge 2 strings include a literal percent sign:

```text
100% weapon damage as fire
```

D2R tooltip strings use printf-style formatting. The raw `%` is interpreted as another formatter, producing garbage numeric text in game.

## Fix

Escape the literal percent sign in the English strings:

```text
100%% weapon damage as fire
```

This keeps the displayed output as `100% weapon damage as fire` while preventing the formatter from reading extra nonexistent arguments.

## Formula Check

The gameplay-side weapon damage addition is already present on `Fists of Fire`:

```text
prgdam=4
calc1=100
SrcDam=128
```

The row comment describes `calc1` as `% Weapon Damage dealt as Fire for progressive release`. `SrcDam=128` is the repo's known 100% source damage value.

The tooltip formulas remain:

- Charge 1 damage: `enma` / `exma`
- Charge 2 radius: `par1+((lvl-1)/6)`
- Charge 3 average fire damage: `m1eo*50/256` / `m1ey*50/256`

The `100%% weapon damage as fire` text is a static note matching `calc1=100`.

## Validation

- `data/local/lng/strings/skills.json` parses as JSON.
- Active/base `skills.txt` remain 322 columns with no malformed rows.
- Active/base `skilldesc.txt` remain 120 columns with no malformed rows.
