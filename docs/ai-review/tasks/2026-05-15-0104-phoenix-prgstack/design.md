# Phoenix Strike Prgstack

## Context

The stack-style elemental charge-ups use `prgstack=1`:

```text
Fists of Fire      prgstack=1
Claws of Thunder   prgstack=1
Blades of Ice      prgstack=1
```

Phoenix Strike is displayed in-game as Phoenix Strike but stored internally as:

```text
Royal Strike
```

Before this change, `Royal Strike` had blank `prgstack`, so its charge release selected one payload rather than clearly opting into the stacked lower-charge behavior.

## Change

Set `Royal Strike` to:

```text
prgstack=1
```

Do this in both:

```text
data/global/excel/skills.txt
data/global/excel/base/skills.txt
```

## Non-Goals

- Do not change Phoenix/Royal Strike `srvdofunc` or progressive functions.
- Do not change `royalstrikemeteor`, `royalstrikechainlightning`, `royalstrikechaosice`, or `royalstrikemeteorfire`.
- Do not change Fists of Fire, Claws of Thunder, Blades of Ice, Cobra Strike, or finishing moves.
- Do not change Phoenix tooltip strings in this pass.

## Risk / Verification Note

This is a direct test of the `prgstack` flag on `Royal Strike`. It may still need in-game verification because `Royal Strike` uses `srvdofunc=34`, while Fists of Fire / Claws of Thunder / Blades of Ice use `srvdofunc=35`.

## Validation Plan

- Check active/base `skills.txt` both remain 322 columns.
- Check active/base `Royal Strike` rows match.
- Check only `Royal Strike` gains `prgstack=1`.
- Confirm Phoenix missile rows are untouched.
