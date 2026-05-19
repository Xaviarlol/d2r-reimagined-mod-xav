# Rare Greater Affix Full Audit Review

Codex generated a full apex audit rather than hand-maintaining the candidate list.

Primary artifact:

- `docs/rare-greater-affix-apex-audit-2026-05-19.md`

Generator:

- `scripts/audit_rare_affix_apexes.py`

Important details:

- The report scans live `magicprefix.txt` and `magicsuffix.txt`.
- It lists every rare-eligible affix group in the complete coverage audit.
- Each group is either covered by a drafted Greater candidate, marked optional, or explicitly deferred for reasons such as binary effects, proc/charged-skill systems, sockets, or special mixed-scope pierce rows.
- The chance table adds drafted Greater rows synthetically and calculates odds at affix level 90.
- `Per affix slot` is the raw eligible candidate weight divided by the same-side pool weight for a sample item.
- `If 3 same-side slots` is an exact group-blocked probability assuming the rare receives three prefix or suffix slots. Actual item odds are lower when the rare rolls fewer same-side affixes.
- Multi-element candidates are aggregated in the chance table, so per-element odds are lower than the combined row shown.

Please focus on correctness of the coverage and math. The proposed Greater payloads are a draft and can be tuned after the audit is agreed.
