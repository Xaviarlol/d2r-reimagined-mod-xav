# Cobra Charge Balance

## Current Constraint

Before this change, Cobra Strike charge 2 and charge 3 both use `cobrastrikenova` as their server missile:

```text
srvmissileb=cobrastrikenova
srvmissilec=cobrastrikenova
```

Because Eric requested no charge 3 change, charge 2 needs a separate server missile before its damage or duration can be adjusted safely.

## Charge 1

Charge 1 remains the restored direct single-target poison finisher:

```text
srvprgfunc1=
srvmissilea=
cltprgfunc1=
cltmissilea=
```

The poison duration remains 50 frames, while the poison rate curve is increased by roughly 50%:

```text
EMin curve: 8/4/5/6/10/14 -> 12/6/8/9/15/21
EMax curve: 14/6/7/10/13/19 -> 21/9/11/15/20/29
ELen: 50 unchanged
HitShift: 4 unchanged
SrcDam: 128 unchanged
```

The charge 1 tooltip formulas are updated to match.

## Charge 2

Charge 2 now uses a new dedicated server missile:

```text
srvmissileb=cobrastrikecloudhit
```

`cobrastrikecloudhit` is copied from `cobrastrikenova` so the server behavior remains the safer nova-style hit payload instead of reintroducing `cobrastrikecloud` as a damaging collision cloud.

To make charge 2 total poison payload about 50% lower while lasting 6 seconds:

```text
HitShift: 4 -> 3
SrcDamage: 128 -> 64
ELen: 50 -> 150
EMin curve: 8/4/5/6/10/14 -> 3/1/2/2/3/5
EMax curve: 14/6/7/10/13/19 -> 5/2/2/3/4/6
```

The lower hitshift plus roughly one-third raw poison rate offsets the 3x longer duration, resulting in approximately half the previous total flat poison payload over 6 seconds. `SrcDamage=64` similarly halves the source-damage contribution.

The charge 2 tooltip formulas now use `150/32`, matching `ELen=150` and `HitShift=3`, and the English string says `over 6 sec + 50%% weapon damage`.

## Charge 2 Visual Duration

The client-only `cobrastrikecloud` visual remains charge 2's client missile:

```text
cltmissileb=cobrastrikecloud
```

Its `Range` is extended from 60 to 150 frames, matching a 6 second cloud duration at 25 frames per second.

## Charge 3

Charge 3 remains unchanged:

```text
srvmissilec=cobrastrikenova
cltmissilec=cobrastrikenova
```

The existing `cobrastrikenova` missile row, `Cobra Strike Nova` helper skill row, and charge 3 tooltip formulas are left unchanged.

## Validation Plan

- Check active/base `skills.txt`, `skilldesc.txt`, and `missiles.txt` column counts.
- Check active/base Cobra rows are synchronized.
- Check `cobrastrikecloudhit` exists in active/base `missiles.txt` with the same column count as the header.
- Check charge 3 fields still point to `cobrastrikenova`.
- Parse `data/hd/missiles/missiles.json` and `data/local/lng/strings/skills.json`.
