# Phoenix Meteor Timing

## Context

Phoenix Strike is displayed in game as Phoenix Strike, but its `skills.txt` row is internally named:

```text
Royal Strike
```

Charge 1 releases the meteor chain through:

```text
royalstrikemeteorcenter
royalstrikemeteor
royalstrikemeteortail
```

Before this change, the Royal Strike meteor rows used a 60-frame pattern:

```text
royalstrikemeteorcenter Range=60 CltParam1=59
royalstrikemeteor       Range=60
royalstrikemeteortail   Range=60
```

That is about 2.4 seconds at 25 frames per second.

## Change

Match vanilla Meteor's 1.2-second timing:

```text
royalstrikemeteorcenter Range=30 CltParam1=29
royalstrikemeteor       Range=30
royalstrikemeteortail   Range=30
```

Do this in both:

```text
data/global/excel/missiles.txt
data/global/excel/base/missiles.txt
```

## Non-Goals

- Do not change Phoenix/Royal Strike skill-row functions, `prgstack`, damage formulas, or tooltips.
- Do not change `SrcDamage` on any Phoenix missile.
- Do not change `royalstrikemeteorfire`; burning ground remains excluded from source damage and timing changes.
- Do not change Cobra Strike, Fists of Fire, Claws of Thunder, Blades of Ice, or finishing moves.

## Risk / Verification Note

The change is intentionally limited to meteor fall timing. The center missile's `Range` controls the landing window, while `CltParam1` controls the visible fall frames. Keeping `CltParam1` one frame below `Range` mirrors vanilla Meteor and should keep visual impact and server timing aligned.

Because Phoenix now uses `prgstack=1`, this faster meteor can appear during 2-charge and 3-charge releases as well as a 1-charge release.

## Validation Plan

- Check active/base `missiles.txt` both remain 172 columns.
- Check active/base Royal Strike meteor rows match.
- Compare Royal Strike meteor timing against vanilla Meteor values.
- Confirm `royalstrikemeteorfire`, chain lightning, chaos ice, Cobra Strike, and skill rows are untouched.
- In game, build one Phoenix charge and release; the meteor should land in about 1.2 seconds.
