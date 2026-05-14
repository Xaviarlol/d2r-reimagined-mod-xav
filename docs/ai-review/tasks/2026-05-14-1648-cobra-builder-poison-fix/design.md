# Cobra Builder-Hit Poison Fix

## Problem

Eric reported that Cobra Strike is applying poison on the first Cobra hit, before the charge 1 finisher release.

The main `Cobra Strike` row currently carries direct poison fields:

```text
EType=pois
EMin/EMax curve = 8.. / 14..
ELen=50
```

Because `AssDoProgressiveAttack` performs a real melee attack while building charges, these direct skill damage fields can poison the charge-building hit itself.

## Earlier Test Fix

Clear direct poison damage from the main `Cobra Strike` skill row so the builder hit no longer has a skill-row poison payload:

```text
EType=
EMin/EMax/ELen=
```

Then route all three released charge payloads through the existing `cobrastrikenova` missile path:

```text
srvprgfunc1=36
srvprgfunc2=36
srvprgfunc3=36
srvmissilea=cobrastrikenova
srvmissileb=cobrastrikenova
srvmissilec=cobrastrikenova
```

This initial workaround removed the premature builder-hit poison, but playtesting showed charge 1 also behaved like an AoE nova.

The follow-up changes charge 1 to a dedicated single-target missile release:

```text
srvprgfunc1=40
srvmissilea=cobrastrikehit
cltprgfunc1=14
cltmissilea=cobrastrikehit
```

`cobrastrikehit` is appended to `missiles.txt` with the Cobra poison curve, `ELen=50`, and `SrcDamage=128`. The main skill row still leaves direct poison fields blank.

## Charge 1 Revert

Eric confirmed the charge 2 cloud now works, but the dedicated charge 1 helper missile made charge 1 behave like the charge 2 AoE. The latest fix reverts charge 1 to the original single-target poison finisher model:

```text
srvprgfunc1=
srvmissilea=
cltprgfunc1=
cltmissilea=
EType=pois
EMin/EMax curve = 8.. / 14..
EDmgSymPerCalc=skill('Tiger Strike'.blvl)*par8
ELen=50
```

The appended `cobrastrikehit` missile was removed from active and base `missiles.txt`.

## Charge 2 Visual Follow-up

Eric confirmed charge 2 now works mechanically, but the poison cloud animation was not showing. The server-side charge 2 payload stays on `cobrastrikenova` so the poison behavior remains unchanged:

```text
srvmissileb=cobrastrikenova
```

Only the charge 2 client missile was changed from the tiny `poisonpuff` to the existing cloud visual:

```text
prgcalc2=par1+((lvl-1)/6)
cltmissileb=cobrastrikecloud
```

`prgcalc2` must stay populated because `cltprgfunc2=9` uses it for the visual disc/cloud radius. This should make the poison cloud visible without reintroducing `cobrastrikecloud` as a server damage/collision missile.

## Validation

- Active and base `skills.txt` both remain 322 columns.
- No malformed rows in active or base `skills.txt`.
- Active/base Cobra Strike rows were updated symmetrically.
- Active/base `missiles.txt` both remain 172 columns.
- `cobrastrikehit` is no longer present or referenced.
- `cobrastrikenova` damage rows in `missiles.txt` were left unchanged.
- Charge 2 server missile remains `cobrastrikenova`; charge 2 client missile is now `cobrastrikecloud`.
