# Claude Review (round 2 — repo-persisted history)

## Verdict

APPROVED

## Summary

Codex addressed both Medium findings from round 1 and folded in the related Low-item suggestions. The wrapper now writes stderr to its own `stderr.log` so `result.json` is parsed from stdout alone (MEDIUM-001). Both the README and protocol.md gained an explicit "sanity-check before pushing — not auto-redacted" warning for `session.jsonl` and `memory\*.md` (MEDIUM-002). The script also picked up a `-NoMirror` switch (which lines up with protocol.md line 70's "unless Eric explicitly asks not to store that review history"), a `-ClaudeExe` parameter, a per-run `memory\` snapshot under `runs\<ts>\memory\`, and richer metadata (`claude_exe`, `stderr_path`, `mirror_enabled`). The credentials/cache/telemetry exclusion still holds — only `<session-id>.jsonl` and `memory/*.md` are mirrored, gated by `-NoMirror`. Read-only enforcement via `--tools Read,Glob,Grep` and `--permission-mode dontAsk` is unchanged and still correctly matches this session's tool surface.

## Findings Status (round 1 → round 2)

- **MEDIUM-001 (stderr/stdout merge breaks JSON parse)** — Resolved. Lines 72–73: `2> $stderrPath` redirects stderr to `runs\<ts>\stderr.log`; `$raw` contains only stdout for `ConvertFrom-Json`. metadata records the stderr path.
- **MEDIUM-002 (sensitive content warning)** — Resolved. README line 25 and protocol.md line 70 both add an explicit pre-push sanity-check warning naming `session.jsonl` and `memory\*.md`.
- **LOW-003 (memory mirror loses history)** — Resolved. Lines 104–108 create `runs\<ts>\memory\` and copy each `*.md` into both the global mirror and the per-run snapshot. README line 18 documents this.
- **LOW-005 (no claude PATH/fallback control)** — Resolved. New `-ClaudeExe` param at line 13, used at line 73 and recorded in metadata at line 119.
- **LOW-007 ("latest mirrored session transcript" wording)** — Resolved. README line 19 now reads "mirrored session transcript for each session id".
- **LOW-006 (review.md not created/noted when result.result empty)** — Not addressed. Still optional; not blocking.
- **LOW-002 (sub-second timestamp collisions)** — Not addressed. Still optional; very low realistic probability.
- **LOW-004 (memory Get-ChildItem non-recursive)** — Not addressed. Still optional; memory dir is flat today.
- **LOW-001 (argument-length limit)** — Not addressed. Still optional.
- **LOW-003 from the prior protocol-only review (`Task folders:` under `## Paths` not labeled legacy)** — Still present at protocol.md lines 106–110. Out of scope for this round but worth noting.

## Remaining Notes (non-blocking)

### Low

- **LOW-008 — `-NoMirror` switch is not documented in the README**
  - File: `docs/ai-review/claude-cli-history/README.md`
  - Issue: protocol.md line 70 carves out an "unless Eric explicitly asks not to store" exception. The wrapper now supports that via `-NoMirror`, but the README's invocation example doesn't mention it. A future Codex hunting for the off-switch will have to read the script.
  - Suggested fix: One sentence after the invocation block: "Pass `-NoMirror` to skip the `session.jsonl` and `memory\*.md` mirror copies when Eric has explicitly asked not to store that review's context."
  - Blocks approval: no

- **LOW-009 — Empty `stderr.log` is still written and tracked**
  - File: `scripts/invoke-claude-review.ps1` line 73
  - Issue: PowerShell's `2> $stderrPath` creates the file even when there is no stderr output, so every successful run leaves a zero-byte `stderr.log` in `runs\<ts>\`. Harmless but it pollutes diffs and `git status`.
  - Suggested fix: After the invocation, `if ((Get-Item -LiteralPath $stderrPath).Length -eq 0) { Remove-Item -LiteralPath $stderrPath }`. Optional.
  - Blocks approval: no

- **LOW-010 — `claude_exe` metadata records the raw param, not the resolved binary**
  - File: `scripts/invoke-claude-review.ps1` lines 13, 119
  - Issue: If the default `'claude'` is used, metadata stores the string `claude` rather than the actual binary that ran (e.g., the documented `C:\Users\ericb\.local\bin\claude.exe`). Minor audit-trail gap.
  - Suggested fix: `$resolvedClaude = (Get-Command -Name $ClaudeExe -ErrorAction SilentlyContinue).Source` and record both `claude_exe_param` and `claude_exe_resolved`. Optional.
  - Blocks approval: no

- **LOW-011 — `verdict_recorded_by_claude` in metadata is always `$null`**
  - File: `scripts/invoke-claude-review.ps1` line 127
  - Issue: The field is reserved but never populated. Either parse `review.md` for the `## Verdict` line and fill it in, or remove the field until it has a writer. Right now it's dead weight in every metadata.json.
  - Suggested fix: Either grep the first non-empty line under `## Verdict` from `$result.result` and assign it, or drop the field.
  - Blocks approval: no

- **LOW-012 — Carry-over: `Task folders:` block at protocol.md lines 106–110 still reads as current**
  - File: `docs/ai-review/protocol.md`
  - Issue: Adjacent to the now-labeled "Legacy review queue root:" but itself unlabeled. Out of scope for this round but unchanged from prior review's LOW-003.
  - Blocks approval: no

## Validation Checks

- Original user request reviewed: yes
- Git diff or design reviewed: working-tree state of all four in-scope files reviewed; supplied diff was again truncated at `-p <review`, but the live files are intact
- TSV column counts checked: n/a (no TSV touched)
- Active/base sync checked: n/a
- Tooltip vs gameplay consistency considered: n/a
- Live publish risk considered: yes — script does not touch live folder
- Docs checked: yes (AGENTS.md, protocol.md, claude-cli-history/README.md)
- Read-only review constraint preserved: yes — `--tools Read,Glob,Grep` + `--permission-mode dontAsk` and confirmed against this session's tool surface
- Credentials/cache/telemetry exclusion: yes — only `<session-id>.jsonl` and `memory/*.md` are copied, gated by `-NoMirror`; no `.credentials*`, no cache dirs, no statsig
- Stderr isolated from JSON parse: yes — `2> $stderrPath` at line 73, `$raw` contains stdout only
- Sensitive-content warning surfaced to user: yes (README line 25, protocol.md line 70)
- Per-run memory snapshot exists: yes (`runs\<ts>\memory\*.md`)

## Codex Action Items

1. Optional cleanup: any subset of LOW-008 through LOW-011 if you want to fold them in before commit.
2. LOW-012 can stay for a follow-up; it's been outstanding through multiple rounds and is genuinely cosmetic.
3. Record this verdict (APPROVED, round 2) and the reviewer session id in the commit summary per protocol.md line 68, and make sure the new `docs\ai-review\claude-cli-history\...` files (including this very review's run directory once it lands) are committed per protocol.md line 70.

## Suggested Follow-up Tests

- Run the wrapper end-to-end with `-NoMirror` and confirm `sessions\` and `memory\` are untouched, while `runs\<ts>\prompt.md`, `result.json`, `review.md`, `metadata.json`, and `stderr.log` still appear and `metadata.mirror_enabled` is `false`.
- Run the wrapper with a deliberately bad `-ClaudeExe` (e.g., `-ClaudeExe claude-nonexistent`) and confirm a clean failure path (script throws, `result.json` may be empty, `stderr.log` captures the PowerShell command-not-found error).
- After a successful run, `git diff --stat docs/ai-review/claude-cli-history/` to confirm the new artifacts land where expected and nothing unexpected (e.g., a `.credentials*`) was copied.

Verdict: **APPROVED** — zero Critical, zero High, all prior Mediums resolved. Codex is clear to commit.
