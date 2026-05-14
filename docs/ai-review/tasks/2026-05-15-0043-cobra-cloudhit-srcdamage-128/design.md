# Cobra Cloudhit SrcDamage 128

## Context

Cobra Strike charge 2 currently uses a split path:

```text
server payload: cobrastrikecloudhit
client visual:  cobrastrikecloud
```

The old dangerous setup was source damage on a lingering cloud/collision missile. That could apply weapon damage repeatedly as the cloud collision checked targets.

The safer setup is to place source damage only on the dedicated one-shot server payload:

```text
cobrastrikecloudhit
```

## Change

Set source damage to 100% on the charge 2 server payload in active and base `missiles.txt`:

```text
cobrastrikecloudhit  SrcDamage=128
```

Keep the lingering visual cloud at zero source damage:

```text
cobrastrikecloud     SrcDamage=0
```

Keep charge 3 unchanged:

```text
cobrastrikenova      SrcDamage=128
```

Update `Eskillcobra2` from:

```text
Charge 2 - Poison Cloud: %d-%d over 6 sec
```

to:

```text
Charge 2 - Poison Cloud: %d-%d over 6 sec + 100%% weapon damage
```

## Non-Goals

- Do not change Cobra charge 1 damage or release behavior.
- Do not change Cobra charge 2 flat poison values, `HitShift`, `ELen`, range, or visual duration.
- Do not set source damage on `cobrastrikecloud`.
- Do not change Cobra charge 3 nova fields.
- Do not alter Phoenix Strike source-damage rows in this pass.

## Validation Plan

- Check active/base `missiles.txt` both remain 172 columns.
- Check active/base Cobra rows match.
- Check `cobrastrikecloudhit` has `SrcDamage=128`.
- Check `cobrastrikecloud` remains `SrcDamage=0`.
- Check `cobrastrikenova` remains `SrcDamage=128`.
- Parse `data/local/lng/strings/skills.json` as JSON.
