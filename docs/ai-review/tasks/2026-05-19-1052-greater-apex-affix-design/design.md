# Greater Apex Affix Design Review

## Context

The earlier Greater Affix table benchmarked `Greater Cruel` against ordinary `Cruel` (`dmg% 267-300`). That was incomplete because the current mod already has stronger apex rows in the same group:

- `Grandmaster's`: `dmg% 301-350` plus AR, Deadly Strike, Crushing Blow, or Open Wounds.
- Weapon `Wraithly1`: `dmg% 176-200`, ethereal, self-repair.

The design now says every Greater candidate must be benchmarked against the strongest existing row in its actual affix `group`, not only against the named vanilla-style family row.

## Revised Greater Cruel

Current apex rows in group `111`:

| Row | Current Payload | Frequency |
|---|---|---:|
| `Cruel` top | `dmg% 267-300` | 114 |
| `Grandmaster's` AR variant | `att 276-300`, `dmg% 301-350` | 4 |
| `Grandmaster's` Deadly Strike variant | `deadly 15-30`, `dmg% 301-350` | 2 |
| `Grandmaster's` Crushing Blow variant | `crush 15-30`, `dmg% 301-350` | 2 |
| `Grandmaster's` Open Wounds variant | `openwounds 94-100`, `dmg% 301-350` | 2 |
| Weapon `Wraithly1` | `dmg% 176-200`, `ethereal`, `rep-dur 10` | 4 |

Revised Greater Cruel:

| Technical Band | level | maxlevel | frequency | Payload |
|---|---:|---:|---:|---|
| Early | 50 | 65 | 1 | `dmg% 500`, `greater-affix-marker` |
| Mid | 66 | 80 | 2 | `dmg% 500`, `greater-affix-marker` |
| Late | 81 | blank | 3 | `dmg% 500`, `greater-affix-marker` |

Rationale:

- Fixed 500% weapon ED is intentionally above `Grandmaster's`.
- 500% ED also beats the rough ethereal damage baseline of Wraithly (`1.5 * 300% effective weapon multiplier = 450% equivalent baseline before other mods`).
- It uses one real stat plus the marker, so it fits safely within the three affix mod slots.
- Late band odds remain around 1 in 330 high-affix-level rare eligible weapons under the current pool simulation.

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
