# Phoenix Weapon Damage Tooltip

## Context

Phoenix Strike is displayed in game as Phoenix Strike, but its `skills.txt` row is internally named:

```text
Royal Strike
```

The direct Phoenix release payloads now use:

```text
royalstrikemeteor             SrcDamage=128
royalstrikechainlightning     SrcDamage=128
royalstrikechaosice           SrcDamage=128
```

The lingering burning ground remains:

```text
royalstrikemeteorfire         SrcDamage=<blank>
```

## Change

Update the English Phoenix strings in `data/local/lng/strings/skills.json`:

```text
Skillsd281
Skillld281
Eskillphoenix1
Eskillphoenix2
Eskillphoenix3
```

The three `Eskillphoenix#` lines should mention:

```text
+ 100%% weapon damage
```

The long description should also make clear that burning ground does not add weapon damage.

## Non-Goals

- Do not change Phoenix gameplay data, missile source damage, timing, `prgstack`, or formulas.
- Do not add source damage to `royalstrikemeteorfire`.
- Do not change Cobra Strike, Fists of Fire, Claws of Thunder, Blades of Ice, or finishing moves.
- Do not rewrite non-English localization in this pass.

## Risk / Verification Note

This is a tooltip-only correction. It brings the visible English tooltip in line with the existing Phoenix source-damage state while preserving the important caveat that lingering burning ground is not weapon-scaled.

## Validation Plan

- Parse `skills.json` as JSON.
- Confirm the five Phoenix English strings have the expected wording.
- Confirm no Phoenix skill or missile gameplay rows changed.
- Deploy locally and inspect Phoenix Strike in game.
