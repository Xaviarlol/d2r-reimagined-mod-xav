# Repository Agent Instructions

Before doing risky design, code, or data-table work in this repository, read:

```text
docs/ai-review/protocol.md
```

That file defines the coordination protocol between Eric, Codex, Claude CLI, and Codex subagents. It covers:

- when to run direct Claude CLI review
- how to include Eric's original request
- Claude's read-only reviewer role
- Codex response and consensus rules
- subagent responsibilities
- publishing and Git expectations

For small obvious edits, Claude review may be skipped. For skill changes, missile changes, cube recipes, itemization passes, treasure classes, TSV-wide changes, live-publish-sensitive work, or anything with tooltip/gameplay mismatch risk, run direct Claude CLI review before committing.
