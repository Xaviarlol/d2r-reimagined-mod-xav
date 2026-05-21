# Claude Review

## Verdict

APPROVED

## Summary

Staged rollback cleanly reverts commit 01a3b111: removes `item_salvageDummy` (itemstatcost id 488) and `salvageDummy` (properties id 486) from both active and base TSVs, and replaces the 106-line "DUMMY = roll 1-100 + per-bracket %" cube recipe block with 12 deterministic per-tier recipes that output `ooi` (1x normal, 2x exceptional, 3x elite) per Set/Unique × Armor/Weapon.

What I verified:
- **Active/base sync:** itemstatcost (489 rows, 52 cols), properties (487 rows, 38 cols), cubemain (15719 rows, 106 cols) all match between `data/global/excel/*.txt` and `data/global/excel/base/*.txt`. `badRows=0` on all six. `salvageDummy=False` confirmed in all six.
- **No orphan references:** removed itemstatcost row 488 was only referenced by (a) the property `salvageDummy` (also being removed) and (b) the cube recipes using `mod=15`/`mod=18` with id 488 (all being removed). No tooltip strings, no skill/missile cross-refs.
- **Last surviving rows are intact:** itemstatcost ends at id 487 (`ga_marker_aureole_vigor`); properties ends at id 485 (`ga_aureole_vigor`). No gap, no off-by-one.
- **Replacement recipes use only pre-existing item codes** (`ooi`, plus the unchanged `oc*`/`oa*`/`ooa`/`ooc` chains elsewhere in cubemain). Input filters (`"armo,bas,uni"`, `"weap,exc,set"`, etc.) match the pattern used by the surrounding ASSEMBLAGE recipes. Multi-output via repeated `ooi` columns is the standard D2R pattern.
- **Diff scope:** only touches the salvage block in cubemain plus the two trailing rows in itemstatcost/properties. No edits leak into adjacent recipes, no row-count drift in upstream/downstream cubemain entries.
- **Memory check:** my `feedback_d2r_spawnable_rare_only.md` and `user_eric_d2r_modder.md` notes flag this project as already pressing itemstatcost limits, which is consistent with row 488 (a new stat with encode/CsvBits values) being a plausible startup-crash trigger.

The rollback restores the deterministic pre-Reapply state (matches what existed between commits `dd15ba9f` and `01a3b111`). Committing and deploying via `scripts\install-local.ps1` is appropriate.

## Low-risk follow-ups (non-blocking)

1. **Confirm root cause empirically.** The supplied `LAST BLZ LOG TAIL` does not actually contain a startup-crash signature — it shows D2R reaching save-file creation and then failing on the BattleNet connect step (`Cannot Connect to Server`), which is unrelated. That log is from either a successful boot or a different run. After publishing the rollback, if D2R starts cleanly, the diagnosis is confirmed by construction. If it still crashes, the salvageDummy commit was not the culprit and you should bisect into the other recent affix work (`ebd57892` top-50 GA redesign, `e19e1336` marker strings, the `restore-greater-affix-frequencies` task work) before doing anything else.

2. **Capture a real crash log before any future re-attempt.** Next time you reproduce the startup CTD, grab the D2R log immediately and include the *crash-side* tail in the review prompt, not the post-startup tail. The current evidence chain rests on suspicion plus "the file with salvageDummy is the most recently touched risky surface", which is plausible but not proven.

3. **Orphan-stat risk on existing saves is theoretically present but practically tiny.** The `salvageDummy` stat was only applied transiently inside the cube transmute sequence (property 486 sets stat 488, follow-up recipes consume the dummy item via `useitem`). A fully-completed salvage cycle leaves no stat-488-bearing item behind. The only at-risk save would be one where a mid-transmute dummy item somehow survived in stash. Given you are the sole tester, this is almost certainly zero impact — but if a save fails to load after deploy, that's why.

4. **In-game smoke test after deploy:** salvage one of each of the eight categories (Set/Unique × Armor/Weapon × Norm/Exc/Elite, plus a Shield) and confirm the deterministic ooi output matches the recipe count (1/2/3 by tier). Cheap, covers the whole replacement block.

5. **If you re-attempt randomized salvage outputs later,** consider implementations that don't add a new `itemstatcost` row, since this project has already shown it sits near a hard limit there. Alternatives: weighted multi-output via existing stats, or a multi-step recipe chain that branches on existing flags (durability, ilvl) rather than a new dummy stat.

6. **Carry-over from prior review rounds (not part of this fix):** `Task folders:` block at `docs/ai-review/protocol.md` lines 106–110 still reads as current rather than legacy. Cosmetic; fold in whenever you next touch protocol.md.

Verdict: **APPROVED** — zero Critical, zero High. Safe to commit and deploy.
