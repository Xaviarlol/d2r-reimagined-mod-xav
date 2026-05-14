---
schema: ai-review-task-v1
id: 2026-05-14-1648-cobra-builder-poison-fix
status: ready_for_claude
phase: code_review
round: 1
max_rounds: 3
created_by: codex
created_at: 2026-05-14T17:15:17Z
updated_at: 2026-05-14T21:11:08Z
repo: C:\Users\ericb\Dropbox\AI projects\d2r\d2r-reimagined-fresh
branch: xav-custom
base_ref: HEAD
head_ref:
original_user_request_included: true
live_publish_allowed: true
last_review:
last_verdict:
claimed_by:
claimed_at:
reviewed_at:
---

# Review Request

## Original User Request

```text
there is a bug with cobra strike. It is applying the poison damage to the first cobra hit, instead of charge 1 finisher
```

## Additional User Finding

```text
charge 2 of cobra strike works, but the animation of the poison cloud isnt showing

now charge 1 is doing the same aoe as charge 2

poison cloud now works, but revert charge 1 back to what it was before you started messing with it - it was a single target poison that simply applied poison damage to a single target finisher
```

## Goal

Keep Cobra Strike charge 1 as the original single-target poison finisher payload, keep the charge 2 poison cloud animation visible, and avoid the helper-missile approach that made charge 1 behave like the charge 2 AoE.

## Phase

code_review

## Scope

- `data/global/excel/skills.txt`
- `data/global/excel/base/skills.txt`
- `data/global/excel/missiles.txt`
- `data/global/excel/base/missiles.txt`
- `docs/modding-findings.md`
- Local publish to `C:\Program Files (x86)\Diablo II Resurrected\mods\XavReimagined\XavReimagined.mpq` is allowed for playtesting.

## Design Or Diff

See `design.md` and `diff.patch`.

## Review Questions

1. Is restoring the Cobra Strike skill-row poison fields while leaving charge 1 missile hooks blank the correct way to return charge 1 to the original single-target finisher behavior?
2. Is keeping `srvprgfunc2=36`, `srvmissileb=cobrastrikenova`, and `cltmissileb=cobrastrikecloud` safe for the working charge 2 cloud behavior?
3. Are active/base `skills.txt` synchronized and TSV-safe?
4. Is removing the unused `cobrastrikehit` missile row from active/base `missiles.txt` correct?
5. Are tooltips now at risk of overstating charge 1 or charge 2 behavior?
6. Is this safe to keep for playtesting, or should we try a narrower data change?

## Suggested Follow-up Tests

- With zero charges, use Cobra Strike once and verify the builder hit does not poison.
- Build one Cobra charge, release with a finisher, and verify poison occurs on release.
- Verify one-charge release does not damage nearby monsters as an AoE.
- Repeat for two and three charges.
- On the two-charge release, verify the poison cloud visual appears.
- Verify charge 3 still produces the expected nova.
- Verify Cobra tooltip does not crash or show blank damage.
