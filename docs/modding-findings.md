# D2R Modding Findings

Living notes for discoveries made while testing XavReimagined. Treat this as practical project knowledge, not a full D2R data-file reference.

Updated: 2026-05-14.

## Workflow Notes

- The active gameplay tables live under `data/global/excel/`.
- The mirror/reference tables live under `data/global/excel/base/`.
- When changing a table that has a `base/` counterpart, update both unless there is a deliberate reason not to. We already hit this with `setitems.txt`: gameplay was correct in the active file, but `base/setitems.txt` drifted and could have confused future scripts.
- Publish to the live game with `scripts/install-local.ps1`.
- Current live target is `C:\Program Files (x86)\Diablo II Resurrected\mods\XavReimagined\XavReimagined.mpq`.
- Current launch args are `-mod XavReimagined -txt -enablerespec`.
- After gameplay/data changes are validated, commit and push them to `origin/xav-custom`; keep the relevant docs/review notes in the same commit.

## Tooltips Vs Mechanics

- Skill tooltips are largely controlled by `skilldesc.txt` and string JSON files.
- Skill behavior is controlled by `skills.txt`, `missiles.txt`, and related data rows.
- These can absolutely disagree. A tooltip can show a value that is not the exact runtime behavior if the formula is wrong, if the missile applies damage differently, or if the skill row itself is carrying hidden damage.
- Cobra Strike showed this clearly: when the main charge-up skill row itself carries poison `EType` / `EMin` / `EMax`, the first Cobra builder hit can apply that poison before any finisher release happens.
- Literal percent signs in string JSON must be escaped as `%%`. A raw `%` inside tooltip text can be interpreted as another printf placeholder and render garbage numeric text, as happened with Fists of Fire's "100% weapon damage as fire" note.

## Cube Recipe Item Codes

- In `cubemain.txt`, `qty=N` on a loose item code such as `ooi,qty=11` is valid for matching multiple loose cube inputs of that item.
- This mod's player-facing Topaz and Emerald item codes are `gmt` and `gme`.
- Vanilla perfect gem codes such as `gpy` and `gpg` may still exist in `misc.txt`, but they are not the Topaz/Emerald items used by the mod's active cube recipes.

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
- For Cobra Strike, weapon scaling felt good after flat poison was reduced to nearly nothing and `SrcDamage=128` was used, but source damage is risky on lingering DOT/cloud-style collision missiles. Current Cobra charge 2 keeps `SrcDamage=128` only on the dedicated one-shot `cobrastrikecloudhit` server payload; the lingering visual cloud row stays at `SrcDamage=0`.
- Active Tiger Strike charges did not appear to multiply Cobra Strike's source-damage release in testing. Hard-point synergy from `EDmgSymPerCalc = skill('Tiger Strike'.blvl)*10` still applies.

## Cobra Strike Current Model

Current design direction:

- Charge 1: restored to the original direct single-target poison finisher model. `srvprgfunc1`, `srvmissilea`, `cltprgfunc1`, and `cltmissilea` stay blank, while the main skill row carries `EType=pois` and its poison curve. Current charge 1 poison rate is roughly 50% higher than the earlier equalized test curve, with `ELen=50`.
- Charge 2: currently routed through the dedicated `cobrastrikecloudhit` server missile so charge 2 can be balanced independently from charge 3.
- Charge 2 uses `cltprgfunc2=9`, `prgcalc2=par1+((lvl-1)/6)`, and `cltmissileb=cobrastrikecloud` as the client-only poison cloud visual. The client cloud visual now uses `Range=150`, which is 6 seconds at 25 frames per second.
- Charge 3: poison nova missile, `SrcDamage=128`, plus flat poison over 2 seconds. Its missile range is intentionally modest and grows slowly.
- Flat poison should stay moderate on DOT/cloud-style effects because source damage can create unclear repeated-hit scaling when it is attached to a lingering collision cloud.
- Current playtest note: charge 2 cloud visuals work when `cltmissileb=cobrastrikecloud` and `prgcalc2` stays populated. Charge 1 must not use the helper missile path, because that made it behave like the charge 2 AoE.

Important current-value note:

- Cobra's charge-up skill row currently carries direct `EType` / `EMin` / `EMax` / `ELen` so charge 1 releases as a single-target poison finisher.
- `cobrastrikehit` was removed after testing because it made charge 1 behave like an AoE release.
- `cobrastrikecloudhit` is a charge 2-only copy of the nova-style server payload with lower poison values, `HitShift=3`, `SrcDamage=128`, and `ELen=150`. This is intended to add one 100% source/weapon damage payload while keeping the total charge 2 flat poison payload about half of the previous 2-second payload over 6 seconds.
- `cobrastrikenova` in `missiles.txt` remains the charge 3 payload with the previous poison curve, `HitShift=4`, `ELen=50`, and `SrcDamage=128`.
- `prgcalc2` must stay populated for `cltprgfunc2=9`; otherwise charge 2 can work mechanically while drawing no poison cloud visual.
- `cobrastrikecloud` should not be reintroduced as the charge 2 server missile without retesting repeated collision damage; it is currently only the charge 2 client visual.
- Charge 1, charge 2, and charge 3 tooltips can diverge because the tooltip is formula-driven and may not reflect whether a payload comes from the skill row or missile row unless `skilldesc.txt` is updated alongside gameplay fields.

## Poison Cloud Collision Behavior

Historical note from the removed Cobra charge 2 cloud experiment:

- Monsters do not simply stand in the cloud and take a normal periodic DOT.
- The monster must move through or across cloud collision areas.
- Damage is applied on collision/hit events as the monster crosses cloud pieces.
- With `SrcDamage=128`, weapon damage was applied through those collision events. Keep `SrcDamage=0` on the lingering `cobrastrikecloud` visual/collision row; put weapon damage only on the dedicated one-shot `cobrastrikecloudhit` server payload.
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
Range = 150
HitShift = 4
SrcDamage = 0
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
- Phoenix Strike/Royal Strike now has `prgstack=1` so it can be tested like the stack-style elemental charge-ups. The expected result is that a 3-charge finisher releases the lower charge payloads as well, but this still needs in-game verification because Royal Strike uses `srvdofunc=34` while Fists of Fire / Claws of Thunder / Blades of Ice use `srvdofunc=35`.
- Phoenix Strike's released elemental effects mostly come from missiles. The three direct release payloads are `royalstrikemeteor`, `royalstrikechainlightning`, and `royalstrikechaosice`; these should carry `SrcDamage=128` when Phoenix charges are intended to add 100% source/weapon damage.
- Do not put `SrcDamage` on `royalstrikemeteorfire` unless specifically testing repeated ground-fire collision/tick behavior; that is the lingering burning-ground payload and was intentionally excluded.
- Fists of Fire has `SrcDam=128` on the skill row. For charge 1/2 weapon scaling, use the skill row's progressive conversion lever: `prgdam=4` with `calc1=100`, described in the table as `% Weapon Damage dealt as Fire for progressive release`.
- Fists of Fire's charge 1/2 tooltip text hardcodes `100%% weapon damage as fire`; keep that string in sync if `calc1` changes from `100`.
- Avoid putting `SrcDamage` directly on `fistsoffirefirewall`; it is a lingering collision fire field and has the same class of repeated-hit risk as the old Cobra cloud experiment.
- Dragon Claw can feel strong with Fists of Fire because multiple charge-release payloads can happen across the two claw attacks. Poison is trickier because poison applications compete/refresh rather than simply stacking like separate fire hits.

## References Worth Keeping Handy

- D2RDoc: `https://eezstreet.github.io/d2rdoc/index.html`
- D2 Data File Guide: `https://wolfieeiflow.github.io/diabloiidatafileguide/`
- Phrozen Keep data-file discussions and guides: `https://d2mods.info/`
- Amazon Basin missile notes: `https://www.theamazonbasin.com/wiki/index.php/Missile`
