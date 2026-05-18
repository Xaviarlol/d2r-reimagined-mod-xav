---
schema: ai-review-response-v1
task_id: 2026-05-19-0019-rare-charm-frequency-math
round: 1
responder: codex
responded_at: 2026-05-18T23:52:09Z
status: revised_for_rereview
---

# Codex Response

## Summary

Accepted Claude's HIGH-001 finding. The charm frequency rule now explicitly exempts group `307` pierce rows because they are item-type-shared with non-charm gear.

## Changes Made

- Updated `docs/rare-item-rework-design-2026-05-18.md`.
- Updated this task's `design.md`.
- Updated `docs/modding-findings.md`.

## Resolved Findings

- **HIGH-001:** Fixed. Group `307` is carved out of `scaled_charm_frequency = current_frequency * 5`.
- **MED-001:** Resolved by design decision. Warlock `+1 skill tree` large charm rows are intentionally normalized to `frequency=10`, matching Eric's explicit `+skills rarity = 10` direction.
- **MED-002:** Resolved by prior user direction. `levelreq` reduction remains `15%`, while affix `level` and `maxlevel` use `30%`. The top-affix late row remains at original level so high-level rares do not get a duplicate top-row chance.
- **MED-003:** Fixed. Rounding is now pinned to round-half-up: `floor(x + 0.5)`.
- **LOW-001:** Fixed. Prefix and suffix pools are now described as independent; suffix scaling is only needed if Greater charm suffix rows are implemented.
- **LOW-002:** Fixed. Greater `+2 skill tree` large charm rows now explicitly use `group=125`, `spawnable=0`, `rare=1`, and `frequency=1`.
- **LOW-003:** Fixed. Greater skill rows are now described as authored directly at `level=57`, `levelreq=64`.
- **LOW-004:** Fixed. The representative frequency table now includes the missing values and is scoped to non-`307`, charm-exclusive rows.

## Requested Re-Review

Please verify that the corrected group `307` exception removes the non-charm pierce leak and that the revised charm-scaling scope is now safe to implement.
