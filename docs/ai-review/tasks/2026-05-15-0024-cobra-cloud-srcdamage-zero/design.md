# Cobra Cloud SrcDamage Zero

## Context

Cobra Strike charge 2 currently uses a split path:

```text
server payload: cobrastrikecloudhit
client visual:  cobrastrikecloud
```

Charge 3 uses:

```text
server/client payload: cobrastrikenova
```

Eric flagged source damage as risky on DOT effects. The cloud behavior has already shown repeated-collision quirks, so the safest current interpretation is to remove source/weapon damage from the charge 2 cloud path entirely.

## Change

Set source damage to zero on both charge 2 cloud rows in active and base `missiles.txt`:

```text
cobrastrikecloud     SrcDamage=0
cobrastrikecloudhit  SrcDamage=0
```

Keep charge 3 unchanged:

```text
cobrastrikenova      SrcDamage=128
```

Update `Eskillcobra2` from:

```text
Charge 2 - Poison Cloud: %d-%d over 6 sec + 50%% weapon damage
```

to:

```text
Charge 2 - Poison Cloud: %d-%d over 6 sec
```

## Non-Goals

- Do not change Cobra charge 1 damage or release behavior.
- Do not change Cobra charge 2 flat poison values, `HitShift`, `ELen`, range, or visual duration.
- Do not change Cobra charge 3 nova fields.
- Do not alter Phoenix Strike source-damage rows in this pass.

## Validation Plan

- Check active/base `missiles.txt` both remain 172 columns.
- Check active/base Cobra cloud rows match.
- Check `cobrastrikecloud` and `cobrastrikecloudhit` have `SrcDamage=0`.
- Check `cobrastrikenova` remains `SrcDamage=128`.
- Parse `data/local/lng/strings/skills.json` as JSON.
