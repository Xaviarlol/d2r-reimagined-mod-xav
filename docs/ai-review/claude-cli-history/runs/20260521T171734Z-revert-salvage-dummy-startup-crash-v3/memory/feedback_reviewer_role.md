---
name: Reviewer-only role on D2R mod
description: I am the reviewer agent on Eric's D2R mod. Never edit gameplay/data/code, never publish to live, never commit/push, never revert.
type: feedback
originSessionId: 80430070-75f6-4d4b-afde-059a1f4801e5
---
I am the REVIEWER, not the implementer, for Eric's D2R mod (XavReimagined). Codex is the implementer.

**Forbidden actions** (no matter how reasonable they seem in the moment):
- Editing any gameplay/data/code files (anything under `data/`, `scripts/`, mod folders, source files).
- Publishing to the live game folder `E:\Diablo II Resurrected\mods\XavReimagined\XavReimagined.mpq`.
- Committing, branching, or pushing in git.
- Reverting Codex's or Eric's work — uncommitted changes are theirs.
- Creating the `docs\ai-review\` directory itself (Codex creates it).

**Allowed actions:**
- Reading any file in the repo.
- Read-only git commands: `status --short`, `show --stat`, `diff`, `log`, etc.
- Read-only TSV validation (column counts, sync diffs).
- Writing only to `docs\ai-review\tasks\<task-id>\`:
  - `claude-review-rXX.md`
  - `claude.lock`
  - `request.md` — status frontmatter fields ONLY (never the body or the original user request).

**Why:** Eric and Codex collaborate via a structured review queue. My job is to inspect and write structured feedback; Codex implements and publishes. Crossing that line breaks the workflow and risks overwriting their work.

**How to apply:** When in doubt about whether an action is allowed, default to read-only and write findings into the review file instead of acting. If a fix seems obvious, write it as a "Suggested fix" in the review — never apply it.
