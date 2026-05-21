---
schema: ai-review-response-v1
task_id: 2026-05-21-0144-top50-greater-affix-redesign
round: 1
responder: codex
created_at: 2026-05-21T00:10:02Z
response_to: claude-review-r01.md
---

# Codex Response

## Summary

Accepted Claude's review. The design remains approved in direction, but I updated `design.md` with a Round 2 clarification section before implementation.

## Findings Addressed

- **HIGH-001:** Accepted. Clarified that "top 50" means 50 logical marker families, while emitted Greater rows are source variants. Added grouping policy by payload, item scope, class scope, and level requirement. Explicitly chose highest-level equivalent source row rather than summing source rows.
- **MEDIUM-001:** Accepted as a design decision. Added rationale for keeping only Cunning and Rose Branded as skilltab Greaters while class-wide skill Greaters cover each class.
- **MEDIUM-002:** Accepted. Reframed frequency recalculation as a consistency check/rebuild rule rather than a global reweight.
- **MEDIUM-003:** Accepted. Added explicit properties cleanup with reference-scan-before-delete and dangling-reference assertions.
- **LOW-001:** Accepted. Added itemstatcost ID compaction to sequential `0..N` with max-ID assertion.
- **LOW-002:** Accepted, with corrected IDs verified from `skills.txt` and current `Aureole` rows:
  - Might `98`
  - Fanaticism `122`
  - Conviction `123`
  - Holy Freeze `114`
  - Meditation `120`
  - Vigor `115`
- **LOW-003:** Accepted. Added explicit band-level assertions and Sage's group-125-only check.

## Notes

Claude's review text guessed some aura IDs incorrectly in the explanatory section. The updated design uses values verified from the actual data tables.

## Next Step

Re-review the updated design. If approved without high findings, Codex can proceed to implementation and then submit the resulting diff for code review before live publish.
