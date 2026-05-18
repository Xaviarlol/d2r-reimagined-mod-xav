# Greater Affix Pilot Proposal

Created: 2026-05-18.

This is the proposed first Greater Affix pass for the rare item rework. It is intentionally small and based on actual existing affix groups in `magicprefix.txt` / `magicsuffix.txt`.

Status: design only, not implemented.

## Goals

- Make elite rares feel more exciting after rare quality was made rarer.
- Add a small number of rare-only chase affixes rather than rewriting hundreds of rows.
- Keep Greater Affixes mutually exclusive with their normal affix families by reusing `group`.
- Use `level`, `maxlevel`, and `levelreq` to allow rare early spikes without low-level abuse.
- Keep socket affixes out of the first pilot.

## Ground Rules

Every Greater row should use:

```text
spawnable = 0
rare = 1
frequency = low relative weight
group = same group as normal family
```

Suggested banding:

| Band | level | maxlevel | levelreq | frequency |
|---|---:|---:|---:|---:|
| Early | 58-65 | 74 or 84 | 75-82 | 1 |
| Main | 75-84 | blank | 82-88 | 2-4 |
| Apex | 90+ | blank | 88-92 | 1 |

## Existing Affix Families Worth Targeting

### Weapon Damage Prefixes

Existing family:

- Group `111`.
- Normal high end includes `Cruel` at `267-300% Enhanced Damage`, `frequency=114`.
- Reimagined high end includes `Grandmaster's` at `301-350% Enhanced Damage` plus attack rating or secondary effects, usually `frequency=2-4`.
- Item scope is usually `itype1=weap`, with `etype1=orb`, `etype2=wand`.

Pilot rows:

| Row | Band | Mods | Intended Feel |
|---|---|---|---|
| Greater Cruel | Early | `dmg% 301-350` | Exceptional/early elite can rarely hit current top-tier damage |
| Greater Grandmaster's | Main | `dmg% 351-425`, `att 301-350` | True elite rare weapon spike |
| Apex Grandmaster's | Apex | `dmg% 426-500`, `att 351-450` | Extremely rare chase weapon prefix |

### Weapon Attack Speed Suffixes

Existing family:

- Group `7`.
- Weapon rows currently top out around `30% IAS` on melee weapons.
- Gloves and jewels also use group `7`, so item scoping should be precise.

Pilot rows:

| Row | Band | Item Scope | Mods | Intended Feel |
|---|---|---|---|---|
| Greater Alacrity | Main | `weap`, exclude `wand`, `orb` | `swing2 35-40` | Rare weapons can beat ordinary IAS |
| Apex Quickness | Apex | `weap`, exclude `wand`, `orb` | `swing2 45-50` | True chase IAS suffix |

### Armor And Shield Defense Prefixes

Existing family:

- Group `101`.
- Current normal high-frequency top includes `Godly` armor/shield defense at `201-225% Enhanced Defense`, `frequency=110`.
- Existing rare-friendly defense/reduction hybrid line tops at `Invulnerable1`: `ac% 81-100`, `red-dmg% 21-25`, `frequency=4`.

Pilot rows:

| Row | Band | Item Scope | Mods | Intended Feel |
|---|---|---|---|---|
| Greater Godly | Main | `armo`, `shld` | `ac% 226-275` | Cleaner high-defense chase |
| Apex Invulnerable | Apex | `tors`, `shld` | `ac% 151-200`, `red-dmg% 26-35` | Defensive rare armor/shield spike |

### Shield Blocking Suffixes

Existing family:

- Group `8`.
- `of Deflecting` gives `block 20-30` and `block2 30`.

Pilot rows:

| Row | Band | Item Scope | Mods | Intended Feel |
|---|---|---|---|---|
| Greater Deflecting | Main | `shld` | `block 31-40`, `block2 35-40` | Strong defensive shield suffix |

### Jewelry Resist Prefixes

Existing family:

- Group `116`.
- `Chromatic` gives `res-all 21-30` on shields and amulets/circlets.
- Rings have lower all-resist values, topping around `13-17`.

Pilot rows:

| Row | Band | Item Scope | Mods | Intended Feel |
|---|---|---|---|---|
| Greater Chromatic | Main | `amul`, `circ` | `res-all 31-40` | Strong but narrow jewelry resist spike |
| Apex Chromatic | Apex | `amul`, `circ` | `res-all 41-50` | Very rare defensive jewelry chase |
| Greater Rainbow | Main | `ring` | `res-all 18-25` | Ring-specific all-resist spike |

### Jewelry Stat Suffixes

Existing family:

- Group `42`.
- `of the Zodiac` gives `all-stats 21-30` on amulet/ring/circlet/orb/staff/wand.

Pilot rows:

| Row | Band | Item Scope | Mods | Intended Feel |
|---|---|---|---|---|
| Greater Zodiac | Main | `amul`, `ring`, `circ` | `all-stats 31-40` | Clear high-roll rare jewelry payoff |
| Apex Zodiac | Apex | `amul`, `ring`, `circ` | `all-stats 41-50` | Very rare stat-stack chase |

### Jewelry Dual Leech Suffixes

Existing family:

- Group `60`.
- `of the Lich` reaches `manasteal 8-9`, `lifesteal 10-12` on ring/amulet.

Pilot rows:

| Row | Band | Item Scope | Mods | Intended Feel |
|---|---|---|---|---|
| Greater Lich | Main | `ring`, `amul` | `manasteal 10-12`, `lifesteal 12-15` | Rare sustain jewelry |
| Apex Lich | Apex | `ring`, `amul` | `manasteal 13-15`, `lifesteal 16-20` | Very rare leech chase |

### Class Item Skill Prefixes

Existing family:

- Group `125`.
- Skill tabs can already roll `+3`.
- Class skills can roll `+2` on several item types.
- This family is very powerful and should be handled conservatively.

Pilot option:

| Row | Band | Item Scope | Mods | Intended Feel |
|---|---|---|---|---|
| Greater Class Mastery | Main | class-specific item types only | class skill `+3` | Makes elite class-specific rares exciting |

Recommended first implementation should either skip this until after the generic pilot, or add only class-item-specific rows. Do not add broad `+3 all skills` in the first pilot.

## First Implementation Recommendation

Start with these 14 rows:

- 3 weapon damage prefixes.
- 2 weapon IAS suffixes.
- 2 armor/shield defense prefixes.
- 1 shield blocking suffix.
- 3 jewelry resist prefixes.
- 2 jewelry stat suffixes.
- 1 jewelry dual-leech suffix: `Greater Lich` only.

Hold back for later:

- `Apex Lich`, because very high dual leech on jewelry may be too build-defining.
- Class-item skill Greater rows, because skill rows need a class-by-class item-type pass.
- Any socket affixes.

## Validation Checklist

Before implementation:

- Confirm each target property code exists in `properties.txt`.
- Confirm target `group` values match the intended normal family.
- Confirm item type codes exist in `itemtypes.txt`.

After implementation:

- Active/base `magicprefix.txt` and `magicsuffix.txt` remain synchronized.
- Column counts remain unchanged.
- Every Greater row has `spawnable=0`, `rare=1`, `frequency>0`, and non-empty `group`.
- No Greater row uses an item type that makes it appear on unintended bases.
- Install to live and use rare reroll/gamble recipes to inspect generated rares.
