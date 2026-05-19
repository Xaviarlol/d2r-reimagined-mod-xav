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
- The revised chance table uses the user-requested 10x-apex target: existing affix frequencies are scaled by 10, and each Greater candidate's eligible total frequency is set equal to the current apex frequency it upgrades. That makes Greater exactly 10x rarer than that apex in the final scaled table.
- The chance table adds drafted Greater rows synthetically and calculates odds at affix level 90.
- `Greater per slot after` is the raw eligible candidate weight divided by the same-side pool weight for a sample item after the 10x existing-affix scale and Greater additions.
- `If 3 same-side slots` is an exact group-blocked probability assuming the rare receives three prefix or suffix slots. Actual item odds are lower when the rare rolls fewer same-side affixes.
- The chance table also shows the current apex row(s) counted for each candidate, apex weight, apex per-slot chance, apex 3-slot chance, and the resulting Greater-vs-apex rarity ratio. The target ratio should now be `10.0x rarer` for every candidate with a valid apex baseline.
- `docs/rare-greater-affix-probability-sanity-2026-05-19.tsv` compares every ordinary affix row before and after. The `existing_only_relative_delta` column should be zero, proving ordinary affix proportions are preserved when Greater rows are excluded. The `with_greater_relative_delta` column shows the unavoidable absolute chance reduction caused by adding new Greater rows.
- Multi-element candidates are aggregated in the chance table, so per-element odds are lower than the combined row shown.

Please focus on correctness of the coverage and math. The proposed Greater payloads are a draft and can be tuned after the audit is agreed.
