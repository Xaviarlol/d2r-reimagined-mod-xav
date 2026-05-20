---
schema: ai-review-task-v1
id: 2026-05-20-0024-rare-affix-implementation-code-review
status: ready_for_claude
phase: code_review
round: 1
max_rounds: 3
created_by: codex
created_at: 2026-05-20T00:24:00Z
updated_at: 2026-05-20T00:24:00Z
repo: C:\Dropbox\AI projects\d2r\d2r-reimagined-fresh
branch: xav-custom
base_ref: 103603327bda35f29f01431f15b49e11e363f077
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
/goal ok go ahead with the implementation. Both phases
```

## Context

Codex implemented the approved two-phase rare affix rework after Claude approved the final pre-implementation design in:

`docs/ai-review/tasks/2026-05-19-2146-rare-affix-final-preimplementation-review/claude-review-r02.md`

The implementation should match the approved design:

1. Phase 1 lowers `level` by 30% and `levelreq` by 15% for rare-enabled affixes while preserving original `maxlevel`.
2. Apex rows receive an early/late split:
   - existing row becomes early, with compressed level/reqlevel, `maxlevel = original level - 1`, and half frequency before global scaling
   - late duplicate starts at the original apex level, no maxlevel, compressed reqlevel, and original frequency before global scaling
3. Existing/non-Greater affix frequencies are multiplied by 10.
4. Greater affix rows are added in 3 bands:
   - Early: level 50, maxlevel 65, frequency `round_half_up(source_freq / 3)`, min 1
   - Mid: level 66, maxlevel 80, frequency `round_half_up(source_freq * 2 / 3)`, min 1
   - Late: level 81, no maxlevel, frequency `source_freq`
5. Greater `levelreq` copies the source apex `levelreq` after the 15% reduction.
6. Greater rows use `spawnable=0`, `rare=1`, same group/scope as the source apex, and `greater-affix-marker` where a mod slot exists.
7. Active and base TXT copies should match.

## Files To Review

- `data/global/excel/magicprefix.txt`
- `data/global/excel/magicsuffix.txt`
- `data/global/excel/base/magicprefix.txt`
- `data/global/excel/base/magicsuffix.txt`
- `scripts/implement_rare_affix_rework.py`
- `docs/rare-affix-implementation-summary-2026-05-20.tsv`
- `docs/rare-item-rework-design-2026-05-18.md`
- `docs/modding-findings.md`
- `docs/session-handoff-2026-05-18.md`

## Codex Validation Already Run

Codex ran a structural validation against the current implementation and the approved TSV artifacts:

```text
validation_summary
('data/global/excel/magicprefix.txt', 1117, 1797, 170, 510, {('50', '65'): 170, ('66', '80'): 170, ('81', ''): 170})
('data/global/excel/magicsuffix.txt', 823, 1355, 133, 399, {('50', '65'): 133, ('66', '80'): 133, ('81', ''): 133})
expected_greater_band_counts {('prefix', 'early'): 170, ('prefix', 'mid'): 170, ('prefix', 'late'): 170, ('suffix', 'early'): 133, ('suffix', 'mid'): 133, ('suffix', 'late'): 133}
actual_greater_band_counts {('prefix', 'early'): 170, ('prefix', 'mid'): 170, ('prefix', 'late'): 170, ('suffix', 'early'): 133, ('suffix', 'mid'): 133, ('suffix', 'late'): 133}
errors 0
```

The implementation summary currently reports:

```text
file	original_rows	output_rows	rare_rows_compressed	source_rows_split	greater_rows_added	active_rows	base_rows	columns	width_errors	missing_greater_level	missing_greater_levelreq	missing_greater_group
magicprefix.txt	1117	1797	918	170	510	1797	1797	40	0	0	0	0
magicsuffix.txt	823	1355	726	133	399	1355	1355	40	0	0	0	0
```

## Review Questions

1. Does the TXT implementation match the approved phase 1 and phase 2 design?
2. Are active/base files synchronized correctly?
3. Are the Greater bands, frequencies, levelreq values, and maxlevel boundaries correct?
4. Did the implementation accidentally alter existing affix proportions beyond the intended global 10x scaling and apex split?
5. Are there any table-shape, column-count, row-order, or D2R data risks before Codex commits/pushes this implementation?
