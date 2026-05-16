# Upstream Next Sync - 2026-05-16

Merged upstream `next` through:

```text
c9074f7c KOR translation: Blinded by Faith (#1237)
b2a147f3 fix bk tribal guardian visual (#1242)
35310e7c Golem Damage and Chasm Break Lag Updates (#1232)
```

## Upstream Changes

- Necromancer golem and Revive scaling were updated in `skills.txt`, `skilldesc.txt`, `monstats.txt`, and `skills.json`.
- Chasm Break, Carnage, and Shield Throw missile behavior were updated in `missiles.txt`.
- Several melee skills gained Sorceress item-type support for oskill use.
- Bul-Kathos Tribal Guardian's HD set visual now points at the flamberge asset.
- Korean `Blinded by Faith` item-name text was updated.

## Merge Resolution

Git reported content conflicts only in:

```text
data/global/excel/skills.txt
data/global/excel/base/skills.txt
```

The conflict was an adjacent-row TSV hunk conflict, not a same-cell gameplay conflict. Resolution used a column-aware merge:

- Preserve Xav custom Assassin, Phoenix, Fists of Fire, Paladin aura, charm, and mercenary skill edits.
- Apply upstream Necromancer golem, Revive, Paladin shield throw, and oskill item-type edits.
- Keep active and `base/` TSV copies synchronized.

## Post-Merge Checks

- No conflict markers remain.
- Active/base `skills.txt`, `missiles.txt`, `skilldesc.txt`, and `monstats.txt` all parse with consistent column counts.
- Cobra Strike, Phoenix Strike/Royal Strike, and Fists of Fire custom values were spot-checked after the merge.
