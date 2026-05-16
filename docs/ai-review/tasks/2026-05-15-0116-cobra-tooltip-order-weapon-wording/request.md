---
schema: ai-review-task-v1
id: 2026-05-15-0116-cobra-tooltip-order-weapon-wording
status: consensus_reached
phase: code_review
round: 1
max_rounds: 3
created_by: codex
created_at: 2026-05-15T01:16:00+02:00
updated_at: 2026-05-16T16:45:16+02:00
repo: C:\Users\ericb\Dropbox\AI projects\d2r\d2r-reimagined-fresh
branch: xav-custom
base_ref: HEAD
head_ref:
original_user_request_included: true
live_publish_allowed: true
last_review:
last_verdict: approved
claimed_by:
claimed_at:
reviewed_at:
approval_source: user_override
approved_at: 2026-05-16T16:45:16+02:00
review_suspended_by: eric
review_suspended_at: 2026-05-16T16:45:16+02:00
review_suspend_reason: External AI review loop suspended by user request; current queue marked approved.
---


# Review Request

## Original User Request

```text
btw the tooltips need some consistency around weapon damage, AND the charges are in the wrong order (other charge up skills have charge 1 at top and 3 at bottom of the charge section)
```

## Prior Context

Cobra Strike currently has 100% weapon/source damage on all three charge release paths:

- Charge 1 uses the Cobra skill row with `SrcDam=128`
- Charge 2 uses `cobrastrikecloudhit` with `SrcDamage=128`
- Charge 3 uses `cobrastrikenova` with `SrcDamage=128`

The detailed tooltip was rendering charge 3 above charge 2 above charge 1. The other Assassin charge-up skills author their `skilldesc.txt` detailed charge lines in reverse slot order so the game renders charge 1 at the top and charge 3 at the bottom.

## Goal

1. Reorder Cobra Strike's detailed tooltip charge section so it renders:
   - Charge 1
   - Charge 2
   - Charge 3
2. Make Cobra Strike's English weapon-damage wording consistent by using `100%% weapon damage` for all three detailed charge lines.
3. Update the Cobra short/long English descriptions so they mention 100% weapon damage consistently.

## Phase

code_review

## Scope

- `data/global/excel/skilldesc.txt`
- `data/global/excel/base/skilldesc.txt`
- `data/local/lng/strings/skills.json`
- `docs/modding-findings.md`

## Design Or Diff

See `design.md` and `diff.patch`.

## Review Questions

1. Does the `skilldesc.txt` Cobra charge section now match the rendering order used by the other charge-up skills?
2. Are the Cobra charge formulas preserved while only moving their display slots?
3. Is the `100%% weapon damage` wording correct and properly escaped for JSON tooltip rendering?
4. Do active/base `skilldesc.txt` remain synchronized and TSV-safe?

## User Approval / Review Suspension

On 2026-05-16T16:45:16+02:00, Eric instructed Codex to suspend the external Claude review loop for now and mark the current review queue approved. This task is closed as `consensus_reached` by user override. Any future risky gameplay/data work can open a new task if the review process resumes.
