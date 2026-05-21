---
schema: ai-review-task-v1
id: 2026-05-21-0144-top50-greater-affix-redesign
status: consensus_reached
phase: code_review
round: 3
max_rounds: 3
created_by: codex
created_at: 2026-05-20T23:44:29Z
updated_at: 2026-05-21T11:59:32Z
repo: C:\Dropbox\AI projects\d2r\d2r-reimagined-fresh
branch: xav-custom
base_ref: 6dca8854
head_ref: xav-custom
original_user_request_included: true
live_publish_allowed: false
last_review: claude-review-r03.md
last_verdict: approved_with_notes
last_response: codex-response-r03.md
claimed_by: claude
claimed_at: 2026-05-21T11:25:00Z
reviewed_at: 2026-05-21T11:45:00Z
---

# Review Request

## Original User Request

```text
ok, create a plan to do them for review by claude. You will need to reweight all frequencies now that you are removing the other GA's. You decide how to do it, but it might make sense to go back to the original prefix suffix files to revert the frequency and redo it with these new GA's. 
```

## Goal

Review the implementation of the approved top-50 Greater Affix redesign.

## Phase

code_review

## Scope

- Implementation affects:
  - `data/global/excel/magicprefix.txt`
  - `data/global/excel/base/magicprefix.txt`
  - `data/global/excel/magicsuffix.txt`
  - `data/global/excel/base/magicsuffix.txt`
  - `data/global/excel/properties.txt`
  - `data/global/excel/base/properties.txt`
  - `data/global/excel/itemstatcost.txt`
  - `data/global/excel/base/itemstatcost.txt`
- `data/local/lng/strings/item-modifiers.json`
- `scripts/implement_top50_greater_affixes.py`
- Existing Phase 1 rare-affix level and requirement changes should be preserved.
- The prior 511-ID itemstatcost crash path must be avoided.
- This is not live-published yet.

## Design Or Diff

Review:

- `implementation-summary.md`
- `diff.patch`
- `scripts/implement_top50_greater_affixes.py`
- `design.md`, especially the "Round 2 Clarifications After Claude Review" section

## Review Questions

1. Does the implementation match the approved top-50 design?
2. Are all broad/old Greater rows and `greater_m_` colored gameplay wrappers removed safely?
3. Do the 50 marker stats/properties stay under the `itemstatcost.txt` hard limit?
4. Are active/base files synchronized and TSV structures valid?
5. Are the selected aura IDs correct and is the old broken `mod1param=126` state gone?
6. Are the generated Greater rows correctly marked `spawnable=1`, `rare=1`, and banded as 50/65, 66/80, 81+?
7. Is the tooltip marker strategy likely safe to publish/playtest?
