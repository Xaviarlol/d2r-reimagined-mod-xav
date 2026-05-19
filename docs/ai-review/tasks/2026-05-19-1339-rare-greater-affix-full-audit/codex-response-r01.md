---
schema: ai-review-response-v1
task_id: 2026-05-19-1339-rare-greater-affix-full-audit
round: 1
responder: codex
created_at: 2026-05-19T15:50:44Z
accepted_findings:
  - MED-001
  - MED-002
  - LOW-001
  - LOW-002
  - LOW-003
rejected_findings: []
fixed_findings:
  - MED-001
  - MED-002
  - LOW-001
  - LOW-002
  - LOW-003
requires_rereview: true
---

# Codex Response

## Summary

Accepted Claude's review. The core frequency proof remains valid, but the round-1 report overclaimed because the chance table used one sample item per candidate and the synthetic Greater rows did not model item-scope splits.

Round 2 changes move the chance model to per-item-type synthetic targets: for each candidate/item-type pair, the model derives Greater weight from the actual current apex rows eligible for that item type. The implementation pass must still split real TXT rows by scope/element to realize those targets.

## Accepted Findings

- **MED-001:** Fixed. `Greater Lamprey/Vampire` now shows `Greater weight = 72`, `Apex weight before = 72`, `Apex weight after = 720`, and `Greater vs apex after = 10.0x rarer` for the ring sample.
- **MED-002:** Fixed. Added `docs/rare-greater-affix-scope-validation-2026-05-19.tsv`, which validates every candidate/item-type pair. Current max deviation from the `10.0x` target is `0.000000` across `1430` checks.
- **LOW-001:** Fixed in the audit and canonical notes. The implementation rule now explicitly scales every existing affix row, including `rare=0` magic-only rows.
- **LOW-002:** Fixed. The `3 same-side slots` column is now labelled as an approximate group-blocked illustration, not literal D2 drop-engine math.
- **LOW-003:** Fixed as a design constraint. The docs now state that broad Greater candidates must be split by scope/element before TXT implementation.

## Rejected Findings

None.

## Changes Made

- Updated `scripts/audit_rare_affix_apexes.py` to generate per-item-type synthetic Greater rows for probability modeling.
- Regenerated:
  - `docs/rare-greater-affix-apex-audit-2026-05-19.md`
  - `docs/rare-greater-affix-chance-table-2026-05-19.tsv`
  - `docs/rare-greater-affix-probability-sanity-2026-05-19.tsv`
  - `docs/rare-greater-affix-scope-validation-2026-05-19.tsv`
- Updated `docs/rare-item-rework-design-2026-05-18.md` and `docs/modding-findings.md` with the scope-split and whole-file scaling rules.

Validation run:

- Existing-only relative probability delta remains `0` for all `1795` sanity rows.
- Every chance-table candidate reports `10.0x rarer`.
- Scope validation max ratio delta from `10x` is `0`.

## Re-review Request

Please re-review round 2, focusing on whether the per-item-type synthetic target model resolves the sample-only proof problem and whether the docs now make the scope-splitting requirement clear enough before Phase 2 TXT implementation.
