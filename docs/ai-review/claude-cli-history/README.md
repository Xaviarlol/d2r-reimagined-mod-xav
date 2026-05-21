# Claude CLI Review History

This directory stores repo-persisted Claude CLI review history for the D2R mod workflow.

Native Claude Code sessions still live under the user's local Claude home directory, but Codex must not rely on that local state alone. Each review run should be invoked through:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\invoke-claude-review.ps1 -PromptPath <prompt.md> -ReviewName <short-name>
```

The wrapper saves:

- `runs\<timestamp>-<review-name>\prompt.md`
- `runs\<timestamp>-<review-name>\result.json`
- `runs\<timestamp>-<review-name>\review.md`
- `runs\<timestamp>-<review-name>\metadata.json`
- `runs\<timestamp>-<review-name>\session.jsonl` when Claude exposes the local session file
- `runs\<timestamp>-<review-name>\memory\*.md` as the per-run memory snapshot
- `sessions\<session-id>.jsonl` as the mirrored session transcript for each session id
- `memory\*.md` as mirrored Claude project memory
- `latest-run.json` as the latest run pointer

Do not store Claude credentials, caches, downloads, or telemetry in this directory.

Session transcripts and memory mirrors are intended to be committed to the repo. Before pushing, sanity-check the latest run's `session.jsonl` and `memory\*.md` for anything that should not be in version control, such as tokens, private file contents, or unrelated personal context. The wrapper deliberately does not auto-redact.

If the local Claude session cannot be resumed on a future machine, start a fresh Claude CLI review and point Claude at the mirrored files in this directory, especially `sessions\<session-id>.jsonl`, `memory\*.md`, and the latest `runs\...\review.md`.
