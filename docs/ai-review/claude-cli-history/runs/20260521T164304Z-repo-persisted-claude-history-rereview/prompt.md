Re-review the repo-persisted Claude review history change after Codex addressed your Medium findings.

Original user request:
`	ext
make the session history persistent by saving on the repo, rather than locally
`

Prior Claude findings addressed:
- MEDIUM-001: stderr is now written separately to stderr.log and stdout alone is parsed as JSON.
- MEDIUM-002: README and protocol now warn that session/memory mirrors are committed and must be sanity-checked before pushing.
- Also added per-run memory snapshots and a ClaudeExe parameter.

Current git status for reviewed files:
`	ext
 M AGENTS.md  M docs/ai-review/protocol.md ?? docs/ai-review/claude-cli-history/README.md ?? scripts/invoke-claude-review.ps1
`

Review scope:
- AGENTS.md
- docs/ai-review/protocol.md
- docs/ai-review/claude-cli-history/README.md
- scripts/invoke-claude-review.ps1

Review this diff only:
`diff
diff --git a/AGENTS.md b/AGENTS.md index 92e05a39..b66c7750 100644 --- a/AGENTS.md +++ b/AGENTS.md @@ -8,11 +8,11 @@ docs/ai-review/protocol.md    That file defines the coordination protocol between Eric, Codex, Claude CLI, and Codex subagents. It covers:   -- when to run direct Claude CLI review +- when to run repo-persisted direct Claude CLI review  - how to include Eric's original request  - Claude's read-only reviewer role  - Codex response and consensus rules  - subagent responsibilities  - publishing and Git expectations   -For small obvious edits, Claude review may be skipped. For skill changes, missile changes, cube recipes, itemization passes, treasure classes, TSV-wide changes, live-publish-sensitive work, or anything with tooltip/gameplay mismatch risk, run direct Claude CLI review before committing. +For small obvious edits, Claude review may be skipped. For skill changes, missile changes, cube recipes, itemization passes, treasure classes, TSV-wide changes, live-publish-sensitive work, or anything with tooltip/gameplay mismatch risk, run `scripts\invoke-claude-review.ps1` before committing so the review history is saved in the repo. diff --git a/docs/ai-review/protocol.md b/docs/ai-review/protocol.md index 20a5833d..619bd74e 100644 --- a/docs/ai-review/protocol.md +++ b/docs/ai-review/protocol.md @@ -27,6 +27,18 @@ Use the `opus` model alias so the CLI selects the latest Opus model available to    Recommended code-review invocation pattern:   +```powershell +powershell -ExecutionPolicy Bypass -File .\scripts\invoke-claude-review.ps1 -PromptPath <prompt.md> -ReviewName <short-name> +``` + +The wrapper stores prompts, raw results, rendered reviews, metadata, mirrored session transcripts, and mirrored Claude project memory under: + +```text +docs\ai-review\claude-cli-history\ +``` + +Use the raw `claude` command only when debugging the wrapper. The canonical raw command is: +  ```powershell  claude --model opus --name d2r-codex-reviewer --permission-mode dontAsk --tools Read,Glob,Grep -p "<review prompt>" --output-format json  ``` @@ -55,6 +67,8 @@ CLI consensus is reached only when:    Before committing, Codex should record the last Claude verdict and session/run id in its final work notes or commit summary.   +Before committing, Codex should also make sure the relevant `docs\ai-review\claude-cli-history\...` files for the review are included in version control unless Eric explicitly asks not to store that review history. Sanity-check the mirrored `session.jsonl` and `memory\*.md` files before pushing because they preserve review context exactly and are not auto-redacted. +  The older `docs\ai-review\tasks\...` queue format may still be useful for archived design records, but it is no longer the primary mechanism for new reviews unless Eric explicitly asks to use the file queue.    ## Paths
`

Return findings ordered by severity and final verdict APPROVED or NEEDS_CHANGES.
