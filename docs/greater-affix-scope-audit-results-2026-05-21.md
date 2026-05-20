# Greater Affix Scope Audit Results - 2026-05-21

## Result

The cross-slot scan did **not** find the feared weapon-only Greater affixes leaking onto jewels. It also did not find charm Greater rows bleeding into non-charm gear.

## Confirmed Safe

- No weapon-only Greater affix was allowed on jewels.
- Charm Greater rows were isolated to charm item types and did not mix with jewels, weapons, rings, armor, or regular gear.
- Class-skill Greater placements looked inherited from their original affix families, not a new Greater-only scope bug.

## Defects Or Suspect Rows Preserved For Redesign

These remain in the current tables and should be handled during the Greater affix redesign rather than hidden by the frequency restore.

- `magicprefix.txt` lines 1304-1306, `Greater Godly`: broad `armo, shld` scope and grants both Enhanced Defense and `%DR`; if this is meant to be pure Godly, remove `%DR`, otherwise narrow the scope.
- `magicprefix.txt` lines 1328-1330, `Greater Gritty`: duplicate `orb` exclusion in `etype`.
- `magicprefix.txt` line 1373, `Greater Serpent's`: early band still has `level=1`; likely copied from low-tier base row.
- `magicprefix.txt` line 1700, `Greater Sage's`: early band still has `level=1`; broad scope may be too generous.
- `magicsuffix.txt` line 976, `of the Greater Sentinel`: early band still has `level=1`; broad scope may be too generous.
- `magicsuffix.txt` line 1168, `of the Greater Whale`: early band still has `level=1`; likely copied from low-tier base row.
- `magicsuffix.txt` line 1291, `Greater Paralysis1`: early band still has `level=1`; likely copied from low-tier base row.

## Current Inventory Files

- `current-greater-affix-inventory-2026-05-21.tsv`: one row per current Greater affix table row, including raw exact mods and inferred apex row.
- `current-greater-affix-family-summary-2026-05-21.tsv`: collapsed family/payload view with early/mid/late bands grouped together.
