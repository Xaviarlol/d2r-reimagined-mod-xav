# All Belts Four Potion Rows

## Context

The relevant capacity tier is the `belt` column in `armor.txt`. `inventory.txt` controls equipment UI placement, but it is not the potion-row capacity source for belt bases.

Known current four-row normal-tier behavior comes from:

```text
Plated Belt    code=hbl    belt=3
```

Exceptional and elite belt bases already use:

```text
belt=6
```

## Change

Set the low normal belt bases to `belt=3` in both active and base armor tables:

```text
Sash          code=lbl    belt=3
Light Belt    code=vbl    belt=3
Belt          code=mbl    belt=3
Heavy Belt    code=tbl    belt=3
```

Leave these existing tiers unchanged:

```text
Plated Belt                 belt=3
Exceptional/elite belts     belt=6
```

## Non-Goals

- Do not edit `inventory.txt`; potion row capacity is not controlled there.
- Do not edit unique or set belt rows; they inherit behavior from the base item code.
- Do not alter belt dimensions, item graphics, vendor data, treasure classes, affixes, or recipes.

## Risk / Verification Note

This is a narrow data-table change. The main risk is misunderstanding the numeric `belt` tier mapping, so the change uses the already-working Plated Belt value rather than inventing a new value.

## Validation Plan

- Parse active and base `armor.txt` and confirm the edited belt rows have `belt=3`.
- Confirm active and base belt rows match.
- Deploy locally with `scripts/install-local.ps1`.
- In game, inspect Sash, Light Belt, Belt, Heavy Belt, and Plated Belt to confirm four potion rows.
