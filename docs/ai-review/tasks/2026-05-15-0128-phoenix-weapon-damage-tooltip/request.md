---
schema: ai-review-task-v1
id: 2026-05-15-0128-phoenix-weapon-damage-tooltip
status: ready_for_review
phase: code_review
round: 0
max_rounds: 3
created_by: codex
created_at: 2026-05-15T01:28:00+02:00
updated_at: 2026-05-15T01:28:00+02:00
repo: C:\Users\ericb\Dropbox\AI projects\d2r\d2r-reimagined-fresh
branch: xav-custom
base_ref: HEAD
head_ref:
original_user_request_included: true
live_publish_allowed: true
---

# Review Request

## Original User Request

```text
did you forget to update the tooltoip for phoenix strike that it now uses 100% weapon damage
```

## Prior Context

Phoenix Strike is internally named `Royal Strike`. Earlier changes set `SrcDamage=128` on the three direct Phoenix release payload missiles:

- `royalstrikemeteor`
- `royalstrikechainlightning`
- `royalstrikechaosice`

The lingering burning-ground missile `royalstrikemeteorfire` remains intentionally excluded from source damage.

## Goal

Update the English Phoenix Strike tooltip strings so they disclose the 100% weapon-damage component on the three direct charge releases.

## Phase

code_review

## Scope

- `data/local/lng/strings/skills.json`
- `docs/modding-findings.md`

## Design Or Diff

See `design.md`.

## Review Questions

1. Do the Phoenix tooltip strings now mention 100% weapon damage where the corresponding payload missiles have `SrcDamage=128`?
2. Does the wording avoid implying that `royalstrikemeteorfire` burning ground adds weapon damage?
3. Are the JSON changes valid and limited to Phoenix English tooltip strings?
4. Does this avoid changing gameplay formulas or missile data?
