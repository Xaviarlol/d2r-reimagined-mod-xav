# Orb Conversion Recipe Fix

## Problem

The original recipes asked for 15 loose Orbs of Infusion plus a perfect gem:

```text
ORB CONVERSION - 15 Orbs of Infusion + Perfect Topaz = Orb of Conversion
numinputs=16
input 1="ooi,qty=15"
input 2=gpy
output=ooc
```

The Horadric Cube is a 4x3 grid, so the practical maximum input count is 12 separate item slots. Fifteen loose `ooi` items plus one perfect gem requires 16 slots and cannot be performed in game.

## Revised User Request

Eric asked to set the recipe to the maximum possible loose-orb input size. Since one slot must be occupied by the gem, the maximum loose Orb of Infusion count is 11.

Eric also clarified that if the Conversion recipe uses `11 ooi + Topaz`, the Assemblage recipe should remain as `11 ooi + Emerald`.

Follow-up playtesting found the remaining failure: these recipes used the vanilla perfect gem codes (`gpy` / `gpg`), but this mod's player-facing Topaz and Emerald items use `gmt` / `gme`.

## Proposed Fix

Replace the two impossible 15-orb recipes with cube-capacity-safe loose-orb recipes:

- `11 Orbs of Infusion + Topaz (gmt) -> Orb of Conversion`
- `11 Orbs of Infusion + Emerald (gme) -> Orb of Assemblage`

Both recipes use:

```text
numinputs=12
input 1="ooi,qty=11"
input 2=<mod gem code>
```

This keeps the user-facing workflow simple and supports existing loose `ooi` items already created by salvage recipes or held in saves.

## Why Not Use Stacked Orbs Here

Claude correctly flagged the prior stacked-orb proposal as risky because it changed the player workflow and depended on `1oi` stack accessibility. Eric's latest request chooses the simpler loose-orb fix instead. That means no new stack mechanics, no new conversion-to-stack recipes, and no changes to salvage outputs or treasure classes are needed for this task.

The tracked Infusion Orb stack/unstack recipe family was also removed from active and base `cubemain.txt` so the local files match the loose-only workflow. Other orb stack systems were left untouched.

## Validation Already Run

- Active/base `cubemain.txt` remain synchronized for these recipe rows.
- Active/base `cubemain.txt` column counts: 106 columns, no malformed rows.
- Conversion now uses `input 2=gmt`; Assemblage now uses `input 2=gme`.
- `git diff --check -- data/global/excel/cubemain.txt data/global/excel/base/cubemain.txt` flags the two new active-file CRLF TSV rows as trailing whitespace. The rows have no malformed trailing tabs after `*eol=0`; this appears to be the usual CRLF/diff-check friction for generated Excel TSV rows.
- Searched for the old `15 Orbs of Infusion` conversion/assemblage recipes and stacked conversion/assemblage recipes; none remain in the active or base conversion block.
- Searched for Infusion Orb stack/unstack recipe rows; none remain in active or base `cubemain.txt`.
