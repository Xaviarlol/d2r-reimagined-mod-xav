---
schema: ai-review-task-v1
id: 2026-05-15-0043-cobra-cloudhit-srcdamage-128
status: ready_for_claude
phase: code_review
round: 1
max_rounds: 3
created_by: codex
created_at: 2026-05-15T00:43:00+02:00
updated_at: 2026-05-15T00:43:00+02:00
repo: C:\Users\ericb\Dropbox\AI projects\d2r\d2r-reimagined-fresh
branch: xav-custom
base_ref: HEAD
head_ref:
original_user_request_included: true
live_publish_allowed: true
last_review:
last_verdict:
claimed_by:
claimed_at:
reviewed_at:
---

# Review Request

## Original User Request

```text
ok. Lets the weapon damage back on, but set to 128 (100%)
```

## Prior Context

Eric wants Cobra Strike charge 2 to regain weapon/source damage, but only in the safer shape that seemed to behave normally before it was temporarily removed. The old broken behavior came from attaching source damage to a lingering cloud/collision missile, which could pulse weapon damage many times per second.

The current intended split is:

- `cobrastrikecloudhit`: charge 2 server damage payload
- `cobrastrikecloud`: charge 2 client visual / lingering cloud row
- `cobrastrikenova`: charge 3 payload

## Goal

Set Cobra Strike charge 2's one-shot server payload to 100% source/weapon damage:

- `cobrastrikecloudhit` should use `SrcDamage=128`

Keep the lingering visual cloud row disabled for source damage:

- `cobrastrikecloud` should stay `SrcDamage=0`

Keep charge 3 unchanged:

- `cobrastrikenova` should stay `SrcDamage=128`

Update the charge 2 tooltip so it again advertises 100% weapon damage.

## Phase

code_review

## Scope

- `data/global/excel/missiles.txt`
- `data/global/excel/base/missiles.txt`
- `data/local/lng/strings/skills.json`
- `docs/modding-findings.md`

## Design Or Diff

See `design.md` and `diff.patch`.

## Review Questions

1. Does this restore 100% source damage only on `cobrastrikecloudhit`?
2. Does `cobrastrikecloud` remain at `SrcDamage=0`, avoiding the old repeated-collision weapon damage risk?
3. Is the tooltip consistent with the new gameplay fields?
4. Are active/base `missiles.txt` synchronized and TSV-safe?
