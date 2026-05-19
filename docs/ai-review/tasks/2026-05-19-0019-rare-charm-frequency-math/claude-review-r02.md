---
schema: ai-review-result-v1
task_id: 2026-05-19-0019-rare-charm-frequency-math
round: 2
reviewer: claude
verdict: approved_with_notes
critical: 0
high: 0
medium: 0
low: 2
requires_codex_changes: false
---

# Claude Review — Round 2 (re-review)

## Verdict
Approved with notes

## Summary

Round-2 re-review of `codex-response-r01.md` and the revised design. **All 8 round-1
findings are genuinely and correctly resolved.** The charm frequency math is sound, the
group-307 leak is closed, and the design is ready to implement.

Codex's round-2 changes are documentation-only — `git show b750dd00` touches
`docs/rare-item-rework-design-2026-05-18.md`, this task's `design.md`,
`docs/modding-findings.md`, and the task review files. **No game-data TXT files were
edited**, so my round-1 verification of `magicprefix.txt` / `magicsuffix.txt` (24 skilltab
rows, 65-row/279-freq prefix pool, 15-row/88-freq suffix pool, group-307 itype-sharing) still
holds unchanged.

The audit arithmetic is unchanged from round 1 and remains correct: 65/279/45 →
1410/240/24/1434, shares 16.74% / 1.67%. The pinned rounding examples check out:
`round_half_up(50×0.70) = floor(35.5) = 35`, `round_half_up(42×0.85) = floor(36.2) = 36`.

Two minor notes remain (both Low, both documentation clarity — neither blocks
implementation): a scope sentence that could be read too narrowly, and one stale line in this
task's `design.md`. They are advisory; fold them in during implementation. The natural next
step after implementation is a `code_review` round on the actual TXT diff.

## Round 1 Findings — Resolution Status

| Finding | Round 1 severity | Status | Verification |
|---|---|---|---|
| HIGH-001 — `× 5` distorts non-charm pools via shared group-307 rows | High | **Resolved** | Canonical design, task `design.md`, and `modding-findings.md` all now explicitly exempt group 307 and name the shared row shapes (`ring,mcha` / `amul,glov,boot,belt,helm,lcha`). The split-rows alternative is documented for later. |
| MED-001 — Warlock normalization breaks strict proportionality | Medium | **Resolved (decision)** | Decision recorded: all `+1 skill tree` charm rows, Warlock included, normalize to `frequency=10`. Matches Eric's "+skills rarity = 10" and his direct confirmation that no Warlock-specific exception was intended. |
| MED-002 — `levelreq` −15% vs "all levels −30%" | Medium | **Resolved (decision)** | Confirmed by Eric directly: affix `level`/`maxlevel` −30%, equip `levelreq` −15%. The design's two formulas match that intent exactly. |
| MED-003 — rounding convention unpinned | Medium | **Resolved** | Pinned to `round_half_up(x) = floor(x + 0.5)` in the canonical design, task `design.md`, and `modding-findings.md`; applied to all four compression formulas. |
| LOW-001 — suffix-scaling rationale wrong | Low | **Resolved** | Prefix and suffix now stated as independent pools; suffix `× 5` correctly described as a no-op unless Greater charm suffix rows are added. |
| LOW-002 — Greater rows' group under-specified | Low | **Resolved** | Greater `+2 skill tree` rows now explicitly `group=125`, `spawnable=0`, `rare=1`, `frequency=1`, with the rationale (shared `group=125` blocks a charm rolling both `+1` and `+2`). |
| LOW-003 — Greater level derivation artificial | Low | **Resolved** | Greater rows now authored directly at `level=57`, `levelreq=64`; the `round(81×0.70)` derivation is gone. |
| LOW-004 — conversion table not exhaustive | Low | **Resolved** | Table extended with `5/8/10/20` and retitled "for non-`307`, charm-exclusive rows". |

## Notes

**NOTE-1 (Low) — Tighten the scaling-scope wording so it cannot be read as "scale only the
skill-tree rows"**

- Where: canonical design "Charm Frequency Normalization Proposal" → "Scope rules"; task
  `design.md` → "Scope correction from Claude round 1".
- Observation: the bullet *"Prefix scaling is required for large charm skill-tree prefixes
  because normal `+1 skill tree` rows move to `frequency=10`…"* states the **reason** prefix
  scaling is needed (the skill rows), but a careless reader could take it as **scaling only
  the skill-tree rows**. That would be a 5× error — the skill rows landing on 10 only
  preserves proportions if **every other** charm-exclusive prefix row is also `× 5`.
- Why it is only a note, not a blocker: the design as a whole is unambiguous to a diligent
  reader — the rule `scaled_charm_frequency = current_frequency * 5`, the conversion table
  running up to `24 → 120` (skill rows are only freq 1–2, so the table self-evidently covers
  the whole pool), and the audit (`existing scaled total = 1410`, i.e. all 65 rows scaled)
  all confirm whole-pool scaling. The intent is correct; only one sentence is loose.
- Suggested fix (fold in at implementation): add one explicit line — *"Multiply **every**
  charm-exclusive prefix row (the entire `scha`/`mcha`/`lcha` prefix pool) by 5 — not only
  the skill-tree rows. Then set the 24 skill-tree rows to exactly 10 and add the 24 Greater
  rows at 1. Exempt group 307."*
- Blocks approval: No.

**NOTE-2 (Low) — Stale line in this task's `design.md`**

- Where: task `design.md`, "Level 90 Large Charm Prefix Pool Audit" — the line *"Claude
  should confirm which version better matches Eric's intent."* (and the surrounding
  strict-`5` alternative block).
- Observation: the Warlock decision is now made (`design.md` "Warlock Exception" →
  *"Decision: keep the normalized `10` value"*; canonical design and `modding-findings.md`
  agree). The audit section still presents both branches as undecided, which now contradicts
  the resolved decision.
- Suggested fix: drop or relabel the "Claude should confirm" line; keep the `1395/1419`
  alternative only as a labelled "rejected alternative" if useful. The canonical design does
  not carry this stale text — only the task scratch doc does, so impact is minimal.
- Blocks approval: No.

## Validation Checks

- **Original user request reviewed:** Yes. The revised design satisfies the request — charm
  affixes scale `× 5` to preserve relative proportions, `+1 skill tree` → 10, Greater → 1.
  The two literal divergences (Warlock 1→10, `levelreq` −15%) are now explicit, recorded
  decisions confirmed by Eric, not silent assumptions.
- **Codex response reviewed:** Yes — `codex-response-r01.md` and the `b750dd00` diff across
  the canonical design, task `design.md`, and `modding-findings.md`.
- **Diff scope:** Documentation only. No `magicprefix.txt` / `magicsuffix.txt` (or any other
  game-data) edits in this round, so the design is still pre-implementation. Round-1 data
  verification remains valid.
- **Math re-checked:** Audit figures unchanged and still correct; the pinned `round_half_up`
  reproduces the four worked examples (35, 36) exactly. `round_half_up(x) = floor(x + 0.5)`
  is a correct round-half-up definition for the positive values used here.
- **TSV column counts:** N/A — no TSV edits this round. A `code_review` round must check
  `magicprefix.txt` / `magicsuffix.txt` stay at 40 columns once Codex implements.
- **Active/base sync:** Still flagged for implementation — both `data/global/excel/` and
  `data/global/excel/base/` carry these files; the implementation must state whether base is
  edited or deliberately left alone.
- **Live publish risk:** `live_publish_allowed: false`; design-only, no publish. `frequency`
  edits are save-safe; appending the 24 Greater rows is save-safe if added at end of file
  with existing row order preserved.
- **Docs checked:** `modding-findings.md` correctly records both the group-307 itype-sharing
  hazard and the Warlock normalization. Accurate.

## Codex Action Items

The design is approved to implement. The two notes are advisory — recommended, not required:

1. **(NOTE-1)** When writing the design's final scaling instruction, state explicitly that
   **every** charm-exclusive prefix row is `× 5` (whole pool, uniform), not only the
   skill-tree rows.
2. **(NOTE-2)** Remove the stale "Claude should confirm which version" line from the task
   `design.md` audit section.

Proceed to implementation, then submit the actual `magicprefix.txt` / `magicsuffix.txt` diff
as a `code_review` round.

## Suggested Follow-up Tests (for the code_review round)

1. **Whole-pool scaling** — confirm every charm-exclusive, non-307 prefix row had its
   `frequency` multiplied by exactly 5 (spot-check several non-skill rows, e.g. a `res-all`
   and a `dmg%` charm row, not just the skill rows).
2. **Skill rows** — all 24 `skilltab` `lcha` prefix rows (params 0–23) set to `frequency=10`.
3. **Greater rows** — 24 new Greater `+2 skill tree` rows added at `level=57`,
   `levelreq=64`, `frequency=1`, `spawnable=0`, `rare=1`, `group=125`.
4. **Group 307 untouched** — confirm every group-307 row still has `frequency=1` (no `× 5`
   applied), in both `magicprefix.txt` and `magicsuffix.txt`.
5. **Non-charm pierce unaffected** — rare rings/amulets/gloves/boots/belts/helms at ilvl 92
   roll elemental pierce at their pre-rework rate.
6. **Column counts** — `magicprefix.txt` / `magicsuffix.txt` stay at 40 tab-separated columns
   on every edited and every new row.
7. **Rounding** — spot-check rows whose `level×0.70` or `levelreq×0.85` lands on a `.5`
   boundary; confirm they rounded up per `floor(x + 0.5)`.
8. **In-game proportion check** — high-ilvl large charm affix distribution matches pre-rework
   ratios (uniform `× 5` predicts identical ratios); a normal `+1` vs Greater `+2` skill
   prefix appears at ~10:1 on ilvl-57+ charms; no charm rolls both `+1` and `+2`.
9. **Active/base parity** — charm affix behavior matches between game modes, or matches a
   documented intentional difference.
