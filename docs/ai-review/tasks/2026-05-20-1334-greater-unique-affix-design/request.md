---
schema: ai-review-task-v1
id: 2026-05-20-1334-greater-unique-affix-design
status: ready_for_claude
phase: design_review
round: 1
max_rounds: 3
created_by: codex
created_at: 2026-05-20T13:34:35Z
updated_at: 2026-05-20T13:34:35Z
repo: C:\Dropbox\AI projects\d2r\d2r-reimagined-fresh
branch: xav-custom
base_ref: 34e764f2cac42eb9b2604d859fd9803fd8dcfdef
head_ref: xav-custom
original_user_request_included: true
live_publish_allowed: false
last_review:
last_verdict:
last_response:
---

# Review Request

## Original User Request

```text
do a design to create greater affixes for the top 5 unique items. One idea is you create copies of the same unique item, with the "enhanced" stats. Say it has 2 main affixes that we want to have a chance to be greater, we create 3 new unique item dupliates:
a) A version that has affix #1 as greater with relative rarity 10x rarer than the chance of getting the same item
b) A version that has affix #2 as greater with relative rarity 10x rarer than the chance of getting the same item
c) A version that has both affix #1 and #2 as greater with relative rarity 100x rarer than the chance of getting the same item
```

## Design To Review

`docs/greater-unique-affix-design-2026-05-20.md`

## Context

Codex drafted a five-item pilot for Greater unique variants:

- Harlequin Crest
- Arachnid Mesh
- Griffon's Eye
- Death's Web
- Windforce

The design uses duplicate `uniqueitems.txt` rows, a family-normalized rarity model, and the existing `greater-affix-marker` property where an open property slot exists.

## Review Questions

1. Does the family-normalized rarity model correctly preserve each target unique family's total chance against same-base sibling uniques?
2. Does the 100:10:10:1 internal weighting correctly express single-Greater variants being 10x rarer than the plain item and double-Greater being 100x rarer?
3. Are there D2R data-table risks with duplicate unique rows using the same base `code` and different `rarity` values?
4. Are the proposed stat packages reasonable for a first pilot?
5. Are there missing implementation details, especially around `*ID`, item-name string keys, marker property slots, or active/base synchronization?
