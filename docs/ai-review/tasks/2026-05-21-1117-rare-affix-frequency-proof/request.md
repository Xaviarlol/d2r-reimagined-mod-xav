---
schema: ai-review-task-v1
id: 2026-05-21-1117-rare-affix-frequency-proof
status: ready_for_claude
phase: code_review
round: 1
max_rounds: 2
created_by: codex
created_at: 2026-05-21T11:17:22Z
updated_at: 2026-05-21T11:17:22Z
repo: C:\Dropbox\AI projects\d2r\d2r-reimagined-fresh
branch: xav-custom
base_ref: ebd578928fa2517095edb5a29692f6b97b1b5b0b
head_ref: a779c55a530b0e9fd6c0a7b4d15ef87623898850
original_user_request_included: true
live_publish_allowed: false
last_review:
last_verdict:
last_response:
claimed_by:
claimed_at:
reviewed_at:
---

# Review Request

## Original User Request

```text
did you adjust the frequency for everything? Then you need to run that simulation of before and after chance the affix will appear vs vanilla file

send to claude for review
```

## Goal

Review the rare-affix frequency simulation and the small follow-up fix it found.

## Phase

code_review

## Scope

Commit under review:

- `a779c55a530b0e9fd6c0a7b4d15ef87623898850` - `Verify rare affix frequency math`

Base:

- `ebd578928fa2517095edb5a29692f6b97b1b5b0b` - top-50 Greater Affix implementation before this frequency proof/fix

Changed files in scope:

- `data/global/excel/magicsuffix.txt`
- `data/global/excel/base/magicsuffix.txt`
- `scripts/implement_rare_affix_rework.py`
- `docs/affix-chance-simulation-summary-2026-05-21.md`
- `docs/affix-chance-simulation-2026-05-21.tsv`

The prior task's `claude-review-r03.md` and `codex-response-r03.md` were committed in the same Git commit for workflow bookkeeping, but they are not the review target here.

## Design Or Diff

Review:

- `implementation-summary.md`
- `diff.patch`
- `docs/affix-chance-simulation-summary-2026-05-21.md`
- `docs/affix-chance-simulation-2026-05-21.tsv`
- `scripts/implement_rare_affix_rework.py`

## Review Questions

1. Is the simulation methodology valid for the requested frequency sanity check?
2. Does the simulation correctly compare current non-Greater affix odds against the pre-rare-rework baseline?
3. Is the level-1 split fix correct?
4. Are active/base suffix files still synchronized and TSV-safe?
5. Does the result prove that non-Greater endgame affix proportions are preserved after the frequency scaling?
6. Are the low/mid-level deltas correctly explained as an expected result of the intentional 30% affix-level compression?
7. Is this safe to keep as part of the Greater Affix implementation before any live publish?
