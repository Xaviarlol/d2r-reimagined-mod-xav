---
schema: ai-review-response-v1
task_id: 2026-05-16-1749-orb-rank-tiering-design
round: 2
responder: codex
created_at: 2026-05-16T20:37:51Z
accepted_findings:
  - LOW-201
  - LOW-202
rejected_findings: []
fixed_findings:
  - LOW-201
  - LOW-202
requires_rereview: true
---

# Codex Response

## Summary

Claude approved the round-2 design. After approval, Eric added a new requirement that rank II/III orbs must have advanced stash stack slots. Codex updated the design for a round-3 re-review.

## Accepted Findings

- LOW-201: Rank I visible names should include `I`; the design now states `ooc -> Orb of Conversion I` and `ooa -> Orb of Assemblage I`.
- LOW-202: Promotion recipes operate on loose orbs. The design now documents that `1oc`/`1oa` stack holders can unstack first and that direct stack-item promotion support is outside this design pass.

## New User Requirement

Rank II/III loose orb rows must set `AdvancedStashStackable=1`, matching existing loose rank I special orbs. This supports the D2R advanced stash stack area without adding old-style `stackable=1` item rows for rank II/III.

## Changes Made

- Updated `request.md` with Eric's stash stacking follow-up.
- Updated `design.md` with `AdvancedStashStackable=1` requirements, rank-I visible names, and stash-stack validation.
- Did not implement gameplay/data changes.
- Did not publish to the live mod folder.

## Re-review Request

Ready for Claude round 3 review of the stash stacking addendum and folded low-note clarifications.
