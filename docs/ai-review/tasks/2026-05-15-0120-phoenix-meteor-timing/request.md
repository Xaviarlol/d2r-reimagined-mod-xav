---
schema: ai-review-task-v1
id: 2026-05-15-0120-phoenix-meteor-timing
status: ready_for_review
phase: code_review
round: 0
max_rounds: 3
created_by: codex
created_at: 2026-05-15T01:20:00+02:00
updated_at: 2026-05-15T01:20:00+02:00
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
make it 1.2 sec
```

## Prior Context

Eric confirmed Phoenix Strike `prgstack=1` works and asked whether the charge 1 meteor landing delay can be managed. The local data showed Phoenix Strike is stored as `Royal Strike`, and its charge 1 release uses the `royalstrikemeteorcenter` missile chain.

## Goal

Change Phoenix Strike charge 1 meteor landing timing to approximately 1.2 seconds.

The mod should match vanilla Meteor timing:

- `royalstrikemeteorcenter` `Range=30`
- `royalstrikemeteorcenter` `CltParam1=29`
- `royalstrikemeteor` `Range=30`
- `royalstrikemeteortail` `Range=30`

At D2R's 25 frames per second, 30 frames is approximately 1.2 seconds.

## Phase

code_review

## Scope

- `data/global/excel/missiles.txt`
- `data/global/excel/base/missiles.txt`
- `docs/modding-findings.md`

## Design Or Diff

See `design.md`.

## Review Questions

1. Are the three Royal Strike meteor missile rows the correct rows for Phoenix charge 1 landing timing?
2. Is matching vanilla Meteor's `30`/`29` frame pattern appropriate for the requested 1.2-second landing?
3. Do active/base `missiles.txt` remain synchronized and TSV-safe?
4. Does this avoid changing Phoenix damage, source damage, burning ground, Cobra Strike, and other charge-up skills?
