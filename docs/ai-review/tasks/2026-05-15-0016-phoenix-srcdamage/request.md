---
schema: ai-review-task-v1
id: 2026-05-15-0016-phoenix-srcdamage
status: ready_for_claude
phase: code_review
round: 1
max_rounds: 3
created_by: codex
created_at: 2026-05-15T00:16:00+02:00
updated_at: 2026-05-15T00:16:00+02:00
repo: C:\Users\ericb\Dropbox\AI projects\d2r\d2r-reimagined-fresh
branch: xav-custom
base_ref: HEAD
head_ref:
original_user_request_included: true
live_publish_allowed: false
last_review:
last_verdict:
claimed_by:
claimed_at:
reviewed_at:
---

# Review Request

## Original User Request

```text
please set them to srcdam 128 (except burning ground)
```

## Prior Context

Eric asked whether Phoenix Strike charges had source damage applied to all three charge releases except burning ground. The check found that Phoenix Strike's internal row is `Royal Strike`, and the release payload missiles had blank `SrcDamage` values.

## Goal

Apply `SrcDamage=128` to the three Phoenix/Royal Strike elemental release payload missiles:

- `royalstrikemeteor`
- `royalstrikechainlightning`
- `royalstrikechaosice`

Leave the lingering burning-ground missile `royalstrikemeteorfire` unchanged.

## Phase

code_review

## Scope

- `data/global/excel/missiles.txt`
- `data/global/excel/base/missiles.txt`
- `docs/modding-findings.md`

## Design Or Diff

See `design.md` and `diff.patch`.

## Review Questions

1. Are the three changed missile rows the correct Phoenix/Royal Strike charge payload rows?
2. Is leaving `royalstrikemeteorfire` with blank `SrcDamage` correct for the "except burning ground" requirement?
3. Are active/base `missiles.txt` synchronized and TSV-safe?
4. Does this avoid changing unrelated Fists of Fire, Claws of Thunder, Blades of Ice, or Cobra data?
