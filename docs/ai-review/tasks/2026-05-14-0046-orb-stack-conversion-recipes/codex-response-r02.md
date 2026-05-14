---
schema: ai-review-response-v1
task_id: 2026-05-14-0046-orb-stack-conversion-recipes
round: 2
responder: codex
created_at: 2026-05-14T21:16:38Z
accepted_findings:
  - USER-GEM-CODE
fixed_findings:
  - USER-GEM-CODE
rejected_findings: []
requires_rereview: true
---

# Codex Response

## Summary

Eric identified the remaining recipe failure: the rows were structurally valid, but the gem item codes were wrong for this mod.

The mod's player-facing Topaz and Emerald items use:

- `gmt` for Topaz
- `gme` for Emerald

The previous rows used vanilla perfect gem codes:

- `gpy` for Perfect Topaz
- `gpg` for Perfect Emerald

## Changes Made

- `data/global/excel/cubemain.txt`
- `data/global/excel/base/cubemain.txt`

Updated the two Orb of Infusion conversion rows:

- `11 Orbs of Infusion + Topaz (gmt) -> Orb of Conversion`
- `11 Orbs of Infusion + Emerald (gme) -> Orb of Assemblage`

Both rows still use:

```text
numinputs=12
input 1="ooi,qty=11"
```

## Validation

- Active/base `cubemain.txt` remain synchronized.
- Both files have 106 columns on every row.
- No malformed rows were found.
- Local publish is allowed for playtesting.
