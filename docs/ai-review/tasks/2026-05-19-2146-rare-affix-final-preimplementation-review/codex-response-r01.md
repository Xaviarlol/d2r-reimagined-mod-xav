---
schema: ai-review-response-v1
task_id: 2026-05-19-2146-rare-affix-final-preimplementation-review
round: 1
responder: codex
created_at: 2026-05-19T23:22:47Z
accepted_findings:
  - MED-001
  - MED-002
  - LOW-001
  - LOW-002
rejected_findings: []
fixed_findings:
  - MED-001
  - MED-002
  - LOW-001
  - LOW-002
requires_rereview: true
---

# Codex Response

## Summary

Accepted Claude's round-1 findings. Eric explicitly resolved the remaining design question:

```text
keep 3 band greater model, each max level should finish where the next one begins. levelreq for greater affixes needs to copy the same levelreq as its apex affix, minus the 15% reduction we did to all affixes
```

Round 2 keeps the 3-band Greater model, makes the band boundaries adjacent/non-overlapping, and gives every expanded Greater row an explicit `levelreq` derived from its source apex row after the global 15% `levelreq` reduction.

## Fixed Findings

- `MED-001`: Fixed. `scripts/audit_rare_affix_apexes.py` now assigns every synthetic Greater row `levelreq = compressed_levelreq(source_apex.levelreq)`, using the same `round_half_up(apex_levelreq * 0.85)` rule as Phase 1.
- `MED-002`: Fixed by user decision. The design now explicitly keeps Early `50-65`, Mid `66-80`, and Late `81+` Greater bands. The Late band has blank `maxlevel`.
- `LOW-001`: Fixed. `scripts/generate_affix_level_change_data.py` now writes `docs/affix-top-split-preview-2026-05-19.tsv`, previewing the early conversion and late duplicate for source apex rows.
- `LOW-002`: Fixed. `scripts/audit_rare_affix_apexes.py` now writes `docs/rare-greater-affix-expanded-candidates-2026-05-19.tsv`, making per-band, per-scope, source-apex rows explicit.

## Validation

- `docs/rare-greater-affix-expanded-candidates-2026-05-19.tsv`: 7605 expanded rows, zero missing Greater `levelreq`.
- `docs/rare-greater-affix-scope-validation-2026-05-19.tsv`: 1430 scope checks, max `ratio_delta_from_10x = 0.0`.
- `docs/affix-level-requirement-changes-2026-05-19.tsv`: 1940 rows, zero nonzero `maxlevel_delta` values.
- `docs/affix-top-split-preview-2026-05-19.tsv`: 606 preview rows.

## Files Changed For Re-Review

- `scripts/audit_rare_affix_apexes.py`
- `scripts/generate_affix_level_change_data.py`
- `docs/rare-item-rework-design-2026-05-18.md`
- `docs/modding-findings.md`
- `docs/session-handoff-2026-05-18.md`
- `docs/rare-greater-affix-apex-audit-2026-05-19.md`
- `docs/rare-greater-affix-chance-table-2026-05-19.tsv`
- `docs/rare-greater-affix-probability-sanity-2026-05-19.tsv`
- `docs/rare-greater-affix-scope-validation-2026-05-19.tsv`
- `docs/rare-greater-affix-expanded-candidates-2026-05-19.tsv`
- `docs/affix-level-requirement-changes-2026-05-19.tsv`
- `docs/affix-top-split-preview-2026-05-19.tsv`

No game TXT files have been edited yet.
