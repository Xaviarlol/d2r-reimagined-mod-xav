# D2R Modding Findings

Living notes for discoveries made while testing XavReimagined. Treat this as practical project knowledge, not a full D2R data-file reference.

Updated: 2026-05-13.

## Workflow Notes

- The active gameplay tables live under `data/global/excel/`.
- The mirror/reference tables live under `data/global/excel/base/`.
- When changing a table that has a `base/` counterpart, update both unless there is a deliberate reason not to. We already hit this with `setitems.txt`: gameplay was correct in the active file, but `base/setitems.txt` drifted and could have confused future scripts.
- Publish to the live game with `scripts/install-local.ps1`.
- Current live target is `E:\Diablo II Resurrected\mods\XavReimagined\XavReimagined.mpq`.
- Current launch args are `-mod XavReimagined -txt`.

## Tooltips Vs Mechanics

- Skill tooltips are largely controlled by `skilldesc.txt` and string JSON files.
- Skill behavior is controlled by `skills.txt`, `missiles.txt`, and related data rows.
- These can absolutely disagree. A tooltip can show a value that is not the exact runtime behavior if the formula is wrong, if the missile applies damage differently, or if the skill row itself is carrying hidden damage.
- Cobra Strike showed this clearly: the skill row itself still had scaling poison damage, so the character sheet showed unexpectedly high no-charge damage even before charge releases mattered.

## Poison Damage Math

D2 poison and other frame-based damage uses raw data values, `HitShift`, and frame length.

Useful working formula:

```text
total damage = raw_rate * (2^HitShift / 256) * duration_frames
damage per second = raw_rate * (2^HitShift / 256) * 25
```

For `HitShift = 4`:

```text
2^4 / 256 = 16 / 256 = 1 / 16
DPS = raw_rate * 25 / 16
2 sec total = raw_rate * 50 / 16
4 sec total = raw_rate * 100 / 16
```

Practical implication: raw poison numbers in the table are not already final displayed damage. A raw value that looks tiny can become meaningful once duration and `HitShift` are applied, and a raw value that looks moderate can become enormous.

## SrcDamage

- `SrcDamage`/`SrcDam` appears to be source damage in 128ths.
- `128` means 100 percent source damage.
- Values above `128` are unsafe. D2RDoc marks this field as 8-bit, and our test with `512` caused broken-looking character sheet damage such as `0-1`.
- Use `128` as the practical max unless a specific row proves otherwise.
- For Cobra Strike, weapon scaling felt good after flat poison was reduced to nearly nothing and `SrcDamage=128` was used.
- Active Tiger Strike charges did not appear to multiply Cobra Strike's source-damage release in testing. Hard-point synergy from `EDmgSymPerCalc = skill('Tiger Strike'.blvl)*10` still applies.

## Cobra Strike Current Model

Current design direction:

- Charge 1: direct poison payload, can use `SrcDamage=128`.
- Charge 2: poison cloud, dangerous with `SrcDamage=128` because cloud collision can reapply source damage.
- Charge 3: poison nova, can use `SrcDamage=128` because it behaves more like a discrete release payload.
- Flat poison should stay low if source damage is the main scaling component.

Important current-value note:

- Cobra's charge-up skill row was reduced to `EMin=1`, `EMax=2`, all poison growth columns `0`, with `ELen=50` and `HitShift=4`, to stop no-charge Cobra Strike from showing hundreds of extra poison damage.

## Poison Cloud Collision Behavior

User testing found an important behavior for Cobra charge 2:

- Monsters do not simply stand in the cloud and take a normal periodic DOT.
- The monster must move through or across cloud collision areas.
- Damage is applied on collision/hit events as the monster crosses cloud pieces.
- With `SrcDamage=128`, weapon damage is applied through those collision events.
- This means the cloud can behave more like repeated collision damage than a passive poison puddle.

Current `cobrastrikecloud` row characteristics:

```text
pSrvDoFunc = 3
CollideType = 3
LastCollide = 1
Collision = 1
ClientCol = 1
NextHit = blank
NextDelay = blank
Size = 2
Range = 60
HitShift = 4
SrcDamage = 128
EType = pois
ELen = 100
```

Interpretation:

- The game can check cloud collision very frequently, up to the 25 FPS engine cadence.
- `LastCollide=1` prevents the simplest "same missile hits the same target every frame forever" model.
- The actual hit rate is still not a clean DOT tick rate. It depends on monster movement, monster size, cloud layout, and whether the target enters new collision pieces.

## NextHit And NextDelay

Likely normalization lever for cloud balance:

```text
NextHit = 1
NextDelay = N
```

Because D2 runs at 25 frames per second:

| NextDelay | Max applications per target |
|---:|---:|
| 25 | 1.00/sec |
| 12 | 2.08/sec |
| 10 | 2.50/sec |
| 8 | 3.13/sec |
| 6 | 4.17/sec |
| 5 | 5.00/sec |

Test plan:

- Start with `NextHit=1`, `NextDelay=12` on `cobrastrikecloud`.
- Keep flat poison tiny.
- Compare weak weapon vs strong weapon while dragging the same monster type through the cloud.
- If damage becomes predictable, tune cloud around expected collision applications per second.

## Blade Fury Comparison

Blade Fury is a useful comparison because it feels collision/re-hit based in game.

In this mod, the active Blade Fury skill uses the Reimagined missile chain:

```text
Blade Fury skill -> ri_bladefury -> ri_bladefuryspread -> ri_bladefuryspread_2
```

The older-looking `bladefury1`, `bladefury2`, `bladefury3`, and `bladefragment*` rows still exist, but the active `skills.txt` row points at `ri_bladefury`.

Relevant active missile values:

| Missile | pSrvDoFunc | pSrvHitFunc | pSrvDmgFunc | LastCollide | NextHit | NextDelay | CollideKill | Pierce | Range | Size |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `ri_bladefury` | 1 | 20 | 1 | 1 | 1 | 1 | 1 | 1 | 25 | 1 |
| `ri_bladefuryspread` | 1 | 20 | 1 | 1 | blank | blank | 1 | blank | 12 | 1 |
| `ri_bladefuryspread_2` | 1 | blank | 1 | 1 | blank | blank | 1 | blank | 12 | 1 |

Interpretation:

- Blade Fury's first missile explicitly uses `NextHit=1`, `NextDelay=1`.
- `NextDelay=1` is only a one-frame cooldown, so it is not a meaningful damage throttle by itself. It mostly means "use the next-hit system, but allow very frequent hits."
- The follow-up spread missiles rely on `LastCollide=1` and `CollideKill=1`, not `NextDelay`.
- Copying Blade Fury's `NextDelay=1` onto a lingering poison cloud would probably not normalize much. For Cobra cloud testing, start much higher, such as `NextDelay=12` or `25`.

## Phoenix Strike And Fists Of Fire Notes

- The internal `skills.txt` row for Phoenix Strike is named `Royal Strike`, even though the game displays Phoenix Strike.
- Phoenix Strike's released elemental effects mostly come from missiles and do not use `SrcDamage` on the released payloads the way we first hoped.
- Fists of Fire has `SrcDam=128` on the skill row, but its released fire effects do not appear to carry `SrcDamage` as their own missile source-damage payloads.
- Dragon Claw can feel strong with Fists of Fire because multiple charge-release payloads can happen across the two claw attacks. Poison is trickier because poison applications compete/refresh rather than simply stacking like separate fire hits.

## References Worth Keeping Handy

- D2RDoc: `https://eezstreet.github.io/d2rdoc/index.html`
- D2 Data File Guide: `https://wolfieeiflow.github.io/diabloiidatafileguide/`
- Phrozen Keep data-file discussions and guides: `https://d2mods.info/`
- Amazon Basin missile notes: `https://www.theamazonbasin.com/wiki/index.php/Missile`
