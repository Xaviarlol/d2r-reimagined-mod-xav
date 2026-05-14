# Cobra Tooltip Order And Weapon Wording

## Context

The game renders the detailed charge section in reverse slot order. Other Assassin charge-up skills place charge 3 in lower-numbered `descline` slots and charge 1 in a later slot so the tooltip displays:

```text
Charge 1
Charge 2
Charge 3
```

Cobra Strike was authored the other way around, so it rendered charge 3 first.

## Change

Move Cobra Strike's `skilldesc.txt` detailed charge slots without changing the formulas:

```text
descline5 -> Charge 1 poison damage
descline4 -> Charge 2 poison cloud damage
descline3 -> Charge 2 splash radius
descline2 -> Charge 3 nova poison damage
descline1 -> Charge 3 nova radius
descline6 -> Attack Rating, unchanged
```

Update English strings:

```text
Eskillcobra1: ... + 100%% weapon damage
Eskillcobra2: already ... + 100%% weapon damage
Eskillcobra3: ... + 100%% weapon damage
```

Also update the short and long Cobra English descriptions to mention `100%% weapon damage`.

## Non-Goals

- Do not change Cobra gameplay fields in `skills.txt` or `missiles.txt`.
- Do not change Cobra charge damage formulas.
- Do not change non-English localizations in this pass.
- Do not change Phoenix, Fists of Fire, Claws of Thunder, or Blades of Ice tooltips.

## Validation Plan

- Parse `data/local/lng/strings/skills.json` as JSON.
- Check active/base `skilldesc.txt` both remain 120 columns.
- Check active/base Cobra skilldesc rows match.
- Check Cobra detailed slot order is charge 3/radius3 in low slots and charge 1 in high slot, matching the reverse-render pattern.
