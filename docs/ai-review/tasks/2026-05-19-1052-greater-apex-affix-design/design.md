# Greater Apex Affix Design Review

## Context

The earlier Greater Affix table benchmarked the weapon-damage Greater row against ordinary `Cruel` (`dmg% 267-300`). That was incomplete because the current mod already has stronger apex rows in the same group:

- `Grandmaster's`: `dmg% 301-350` plus AR, Deadly Strike, Crushing Blow, or Open Wounds.
- Weapon `Wraithly1`: `dmg% 176-200`, ethereal, self-repair.

The design now says every Greater candidate must be benchmarked against the strongest existing row in its actual affix `group`, not only against the named vanilla-style family row.

## Revised Greater Grandmaster's

Current apex rows in group `111`:

| Row | Current Payload | Frequency |
|---|---|---:|
| `Cruel` top | `dmg% 267-300` | 114 |
| `Grandmaster's` AR variant | `att 276-300`, `dmg% 301-350` | 4 |
| `Grandmaster's` Deadly Strike variant | `deadly 15-30`, `dmg% 301-350` | 2 |
| `Grandmaster's` Crushing Blow variant | `crush 15-30`, `dmg% 301-350` | 2 |
| `Grandmaster's` Open Wounds variant | `openwounds 94-100`, `dmg% 301-350` | 2 |
| Weapon `Wraithly1` | `dmg% 176-200`, `ethereal`, `rep-dur 10` | 4 |

Revised Greater Grandmaster's:

| Technical Band | level | maxlevel | frequency | Payload |
|---|---:|---:|---:|---|
| Early AR | 50 | 65 | 1 | `att 301-350`, `dmg% 451-500`, `greater-affix-marker` |
| Mid AR | 66 | 80 | 1 | `att 301-350`, `dmg% 451-500`, `greater-affix-marker` |
| Mid Deadly | 66 | 80 | 1 | `deadly 31-40`, `dmg% 451-500`, `greater-affix-marker` |
| Late AR | 81 | blank | 1 | `att 301-350`, `dmg% 451-500`, `greater-affix-marker` |
| Late Deadly | 81 | blank | 1 | `deadly 31-40`, `dmg% 451-500`, `greater-affix-marker` |
| Late Crushing | 81 | blank | 1 | `crush 31-40`, `dmg% 451-500`, `greater-affix-marker` |
| Late Open Wounds | 81 | blank | 1 | `openwounds 100`, `dmg% 451-500`, `greater-affix-marker` |

Rationale:

- The player-facing category is `Greater Grandmaster's`, matching the existing apex family identity.
- The Greater version is not plain ED-only. It keeps the Grandmaster-style "ED plus premium rider" shape.
- Each row uses two real stats plus the marker, so it fits within the three affix mod slots.
- `dmg% 451-500` is above `Grandmaster's` and above the rough ethereal damage baseline of Wraithly (`1.5 * 300% effective weapon multiplier = 450% equivalent baseline before other mods`).
- Late total Greater Grandmaster's family frequency is `4`, still below existing Grandmaster's total frequency `10`; each specific rider variant remains very rare.
- Open Wounds is fixed at the current apparent cap/top-end value of `100`, with the extra power coming from the much higher ED.

## Newly Added Apex Families

The candidate table now includes or corrects:

| Candidate | Apex Baseline | Proposed Greater Payload |
|---|---|---|
| Greater Godly | `Godly`, `Invulnerable1`, armor `Wraithly1` | `ac% 250-300`, `red-dmg% 26-30` |
| Greater Antimagic | `Antimagic`, `of Negation` magic resistance rows | `res-mag 24-30` |
| Greater Coalescence | Fire/Lightning/Cold Coalescence absorb suffixes | matching absorb `28-35` |
| Greater Omniscient | `Omniscient`, `Sage's` | `allskills 3` on torso/amulet, `allskills 2` on rings |
| Greater Skilltab | top `+3 skilltab` rows | `skilltab +4` |
| Greater Gnostic | top random class skill `+5` rows | random class skill `+6` |

## Important Design Constraints

- Greater rows should use the same `group` as the normal family so Greater replaces normal rather than stacking with normal.
- Greater rows should remain rare-only: `spawnable=0`, `rare=1`.
- Skill affixes should likely be implemented in a dedicated skill-affix pass, even though they are now listed as candidates.
- Rows with two real stats plus `greater-affix-marker` fill all three mod slots. Rows needing three real stats cannot also use the marker unless we add a combined property.

## Requested Claude Verdict

Please review whether the revised Greater Affix candidate list now properly accounts for the real apex rows in the current mod data, and identify any remaining apex affixes that should be added before implementation.
