# Phoenix Strike SrcDamage

## Current Rows

Phoenix Strike is stored internally as `Royal Strike`.

The charge release missiles are:

```text
charge 1: royalstrikemeteor
charge 2: royalstrikechainlightning
charge 3: royalstrikechaosice
```

The charge 1 lingering fire patch is:

```text
royalstrikemeteorfire
```

## Change

Set `SrcDamage=128` on the three direct release payload missiles only:

```text
royalstrikemeteor          SrcDamage=128
royalstrikechainlightning  SrcDamage=128
royalstrikechaosice        SrcDamage=128
```

Do not set `SrcDamage` on `royalstrikemeteorfire`, because Eric explicitly excluded burning ground and lingering ground-fire rows can repeatedly collide or tick.

## Non-Goals

- Do not change `Royal Strike` skill-row `SrcDam`; it is already `128`.
- Do not change `royalstrikemeteorcenter`, which is the meteor targeting/spawn carrier.
- Do not alter damage curves, `HitShift`, `ELen`, synergies, or tooltip strings in this pass.
- Do not alter Fists of Fire, Claws of Thunder, Blades of Ice, or Cobra Strike rows.

## Validation Plan

- Check active/base `missiles.txt` both remain 172 columns.
- Check only the three requested payload rows gain `SrcDamage=128`.
- Check `royalstrikemeteorfire` remains blank for `SrcDamage`.
- Check active/base changed rows are identical.
