# Claude Review

## Verdict

APPROVED — with two Medium notes worth fixing before this becomes load-bearing.

## Summary

Codex implemented a wrapper-based persistent review history that meets Eric's intent: every Codex-triggered Claude review now runs through `scripts/invoke-claude-review.ps1`, which writes the prompt, raw JSON, rendered review, metadata, mirrored session jsonl, and mirrored project memory under `docs/ai-review/claude-cli-history/`. Native Claude Code sessions correctly remain local — only the per-run mirror is repo-side. The wrapper enforces read-only review via `--tools Read,Glob,Grep` and `--permission-mode dontAsk`, and it does **not** copy credentials, cache directories, or telemetry. The slug computed by `Get-ClaudeProjectSlug` (`C--Dropbox-AI-projects-d2r-d2r-reimagined-fresh`) matches the real `.claude/projects/` directory layout, which I can confirm from my own memory dir path. AGENTS.md and protocol.md both correctly steer to the wrapper as the canonical entry point and demote the raw `claude` invocation to a debugging fallback.

## Findings

### High

None.

### Medium

- **MEDIUM-001 — `2>&1` merge can break JSON parse on a "success" run**
  - File: `scripts/invoke-claude-review.ps1` line 70
  - Issue: `& claude @claudeArgs 2>&1` captures stderr into the same stream as stdout. If `claude` emits any non-fatal stderr line on a successful run (deprecation warnings, auto-update notices, transient network warnings, etc.), `$raw` will contain non-JSON noise mixed with the JSON. `result.json` still gets written (good), but `ConvertFrom-Json` on line 79 will throw, no `review.md` is produced, and the caller sees a parse error rather than a clean review. Exit code 0 + parse failure currently masquerades as a script bug rather than a CLI warning.
  - Why it matters: Once this is the canonical pre-commit gate, a single one-off stderr line silently blocks reviews in a confusing way.
  - Suggested fix: Either (a) capture stderr separately, e.g. `& claude @claudeArgs 2> (Join-Path $runDir 'stderr.log')`, and only parse stdout; or (b) keep the merge but try the JSON parse defensively and, on failure, extract the largest balanced `{...}` substring before giving up.
  - Blocks approval: no (per the protocol's CLI consensus rule only Critical/High block)

- **MEDIUM-002 — Mirrored session.jsonl and memory/*.md may contain sensitive prior-conversation content that will land in git**
  - Files: `scripts/invoke-claude-review.ps1` lines 89–102; `docs/ai-review/claude-cli-history/README.md`
  - Issue: `<session-id>.jsonl` is the full Claude Code conversation transcript including every tool input/output the assistant saw in that session — file contents read, paths inspected, prompts containing diffs, etc. Mirroring it into the repo is intentional per Eric's request, but the README and protocol.md don't warn that this snapshot becomes a permanent, publicly-committable artifact. Same applies to `memory/*.md`, which today contains user profile, feedback, and project memories. None of *my* current memory files contain secrets, but a future memory write of "API token = …" or a future review that reads a `.env` file into a tool result would silently propagate to the repo and any GitHub push.
  - Why it matters: Eric asked for persistence; he hasn't necessarily signed off on indiscriminate inclusion of any sensitive content that ever appears in Claude's local state. A warning in the README plus a pre-commit reminder in protocol.md is cheap insurance.
  - Suggested fix: Add to `docs/ai-review/claude-cli-history/README.md`: "Session transcripts and memory mirrors are committed to the repo. Before pushing, sanity-check the latest run's `session.jsonl` and `memory/*.md` for content you do not want in version control (tokens, private file contents, etc.). The wrapper deliberately does not auto-redact." Optional: also add a `-NoMirror` switch to the wrapper for one-off sensitive reviews.
  - Blocks approval: no

### Low

- **LOW-001 — Very large prompts may hit Windows process-arg length limit**
  - File: `scripts/invoke-claude-review.ps1` line 66
  - Issue: `-p $promptText` passes the entire prompt as a single command-line argument. Diff-heavy reviews can easily push past Windows' practical process-argument ceiling (~32K chars). The wrapper currently doesn't have a fallback to stdin.
  - Suggested fix: If `claude` accepts a prompt via stdin (e.g., `claude … -p -` or piped input), gate on `$promptText.Length` and switch to stdin past ~30000 chars. Optional, can be deferred until it bites.
  - Blocks approval: no

- **LOW-002 — Sub-second timestamp collisions**
  - File: `scripts/invoke-claude-review.ps1` lines 43–45
  - Issue: `yyyyMMddTHHmmssZ` has second-level resolution. Two reviews fired in the same second produce the same `runDir` and the second `New-Item -Force` quietly reuses the first. Realistically only an issue if someone scripts a fan-out.
  - Suggested fix: Append `-{0:D4} -f (Get-Random -Maximum 10000)` or the process ID.
  - Blocks approval: no

- **LOW-003 — Memory mirror keeps only the latest snapshot**
  - File: `scripts/invoke-claude-review.ps1` lines 97–102
  - Issue: Each run overwrites `docs/ai-review/claude-cli-history/memory/*.md`. The `runs/<timestamp>/` dir captures `session.jsonl` per run, but not memory. Future "what did Claude know at the time of review X" investigations will be lossy.
  - Suggested fix: Also copy memory snapshot under `runs/<timestamp>/memory/` (cheap, small files).
  - Blocks approval: no

- **LOW-004 — Memory copy is non-recursive**
  - File: `scripts/invoke-claude-review.ps1` line 99
  - Issue: `Get-ChildItem -LiteralPath $localMemoryDir -File -Filter '*.md'` only sees top-level `*.md`. My memory dir is currently flat, so this works today, but if memories are ever organized into subfolders the mirror silently drops them.
  - Suggested fix: Add `-Recurse` and preserve subdir structure with a small `Resolve-Path` walk; or document the flat-only assumption.
  - Blocks approval: no

- **LOW-005 — No `claude` PATH check / no fallback to documented absolute path**
  - File: `scripts/invoke-claude-review.ps1` line 70
  - Issue: Script calls `& claude` directly. Protocol.md documents `C:\Users\ericb\.local\bin\claude.exe` as the canonical location. If a future Codex shell loses PATH, the script errors out generically.
  - Suggested fix: Add a `[string]$ClaudeExe = 'claude'` parameter and `& $ClaudeExe @claudeArgs`, with a `Get-Command` probe up front that falls back to the documented path.
  - Blocks approval: no

- **LOW-006 — No guard / metadata field when `result.result` is missing**
  - File: `scripts/invoke-claude-review.ps1` lines 80–82
  - Issue: If Claude returns a JSON envelope with no `.result` (unusual but possible — e.g., a thinking-only response or future format change), no `review.md` is written and `metadata.json.verdict_recorded_by_claude` stays `$null` with no other signal. Caller relying on `ReviewPath` will get a path that doesn't exist.
  - Suggested fix: Write a stub `review.md` ("No `.result` field in CLI output — see result.json") and set a `result_present = $false` flag in metadata.
  - Blocks approval: no

- **LOW-007 — Wording: "latest mirrored session transcript"**
  - File: `docs/ai-review/claude-cli-history/README.md` line 18
  - Issue: The README phrasing implies only one file lives in `sessions/`, but the wrapper writes one jsonl per distinct session id. Over time `sessions/` will accumulate multiple files.
  - Suggested fix: Rephrase to "mirrored session transcript per session id". Trivially small.
  - Blocks approval: no

## Validation Checks

- Original user request reviewed: yes
- Git diff or design reviewed: working-tree state of all four in-scope files reviewed; supplied diff was again truncated at `-p <review`, but the live files are intact
- TSV column counts checked: n/a (no TSV touched)
- Active/base sync checked: n/a
- Tooltip vs gameplay consistency considered: n/a
- Live publish risk considered: yes — script does not touch live folder; protocol publish rule unchanged
- Docs checked: yes (AGENTS.md, protocol.md, claude-cli-history/README.md)
- Read-only review constraint preserved: yes — `--tools Read,Glob,Grep` + `--permission-mode dontAsk` and confirmed against this session's tool surface
- Credentials/cache/telemetry exclusion: yes — only `<session-id>.jsonl` and `memory/*.md` are copied; no `.credentials*`, no cache dirs, no statsig
- Claude project slug correctness: yes — `Get-ClaudeProjectSlug` output matches the real `C--Dropbox-AI-projects-d2r-d2r-reimagined-fresh` directory

## Codex Action Items

1. (Recommended before this becomes load-bearing) MEDIUM-001: split stderr from stdout in the wrapper so a stray warning doesn't break the JSON parse.
2. (Recommended) MEDIUM-002: add a one-paragraph "what's in here / what to sanity-check before pushing" warning to `docs/ai-review/claude-cli-history/README.md` and a one-line nudge in protocol.md near the existing "make sure history files are included in version control" sentence.
3. Optional cleanup: any of LOW-001 through LOW-007 as you encounter the corresponding pain.
4. Record this verdict (APPROVED, MEDIUM notes left intentional) and the reviewer session id in the commit summary, per the existing protocol rule at protocol.md line 68.

## Suggested Follow-up Tests

- Run the wrapper end-to-end against a synthetic small prompt and verify all of: `runs/<ts>/prompt.md`, `runs/<ts>/result.json`, `runs/<ts>/review.md`, `runs/<ts>/metadata.json`, `runs/<ts>/session.jsonl`, `sessions/<session-id>.jsonl`, `memory/*.md`, and `latest-run.json` exist and contain expected content.
- Force a non-zero exit (e.g., bad model name) and confirm `result.json` is still saved and the wrapper throws with a clear message.
- Force a non-JSON stderr line on a success path (run with a flag the CLI deprecates) to confirm/demonstrate MEDIUM-001 in practice.
- After commit, `git log -- docs/ai-review/claude-cli-history/` to verify history is actually tracked and not gitignored anywhere upstream.

Verdict: **APPROVED** — zero Critical, zero High. Codex is clear to commit. Strongly suggest folding in MEDIUM-001 and MEDIUM-002 in a follow-up; both are quick changes and meaningfully harden the new mechanism.
