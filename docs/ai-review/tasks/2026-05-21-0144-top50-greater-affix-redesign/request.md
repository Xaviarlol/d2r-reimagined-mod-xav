---
schema: ai-review-task-v1
id: 2026-05-21-0144-top50-greater-affix-redesign
status: ready_for_claude
phase: design_review
round: 2
max_rounds: 3
created_by: codex
created_at: 2026-05-20T23:44:29Z
updated_at: 2026-05-21T00:10:02Z
repo: C:\Dropbox\AI projects\d2r\d2r-reimagined-fresh
branch: xav-custom
base_ref: 6dca8854
head_ref: xav-custom
original_user_request_included: true
live_publish_allowed: false
last_review: claude-review-r01.md
last_verdict: approved_with_notes
last_response: codex-response-r01.md
claimed_by:
claimed_at:
reviewed_at:
---

# Review Request

## Original User Request

```text
ok, create a plan to do them for review by claude. You will need to reweight all frequencies now that you are removing the other GA's. You decide how to do it, but it might make sense to go back to the original prefix suffix files to revert the frequency and redo it with these new GA's. 
```

## Goal

Review a plan to replace the current broad Greater Affix implementation with a focused top-50 Greater family system, including frequency reweighting and a safer colored-tooltip marker strategy.

## Phase

design_review

## Scope

- Future implementation will affect:
  - `data/global/excel/magicprefix.txt`
  - `data/global/excel/base/magicprefix.txt`
  - `data/global/excel/magicsuffix.txt`
  - `data/global/excel/base/magicsuffix.txt`
  - `data/global/excel/properties.txt`
  - `data/global/excel/base/properties.txt`
  - `data/global/excel/itemstatcost.txt`
  - `data/global/excel/base/itemstatcost.txt`
  - possibly localized strings for marker tooltip text
- This review is design-only; no gameplay files have been changed for this redesign yet.
- Existing Phase 1 rare-affix level and requirement changes should be preserved.
- The prior 511-ID itemstatcost crash path must be avoided.

## Design Or Diff

Review `design.md` in this task folder, especially the "Round 2 Clarifications After Claude Review" section. Codex also wrote `codex-response-r01.md`.

## Review Questions

1. Does the selected top-50 list match Eric's "elite gamer" intent and avoid low-impact Greater affixes?
2. Is the plan to rebuild from current non-Greater rows safer than checking out full old prefix/suffix files?
3. Is the one-marker-stat-per-family colored tooltip strategy safe under the 511 itemstatcost ID limit?
4. Does the proposed frequency model correctly reweight Greater affixes after most Greater rows are removed?
5. Should the frequency model use a single apex row or sum equivalent apex rows for split families?
6. Are any selected affixes technically unsafe because they need too many mods plus marker properties?
7. Are the aura Greater affixes, especially Might/Fanaticism/Conviction/Holy Freeze/Meditation/Vigor, safe and sensible?
8. Are active/base synchronization and TSV structure validation sufficiently covered?
