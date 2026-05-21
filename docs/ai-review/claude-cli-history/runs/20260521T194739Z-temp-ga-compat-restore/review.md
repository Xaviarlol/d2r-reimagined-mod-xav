# Claude Review

## Verdict

APPROVED — no Critical/High blockers.

## Why this is safe as a rescue commit

The crash signature ("CTD after click-to-continue, fresh empty save folder fixes it") is the textbook save-deserialization failure mode for D2R rare items. To deserialize a rare item, the engine needs the affix row indices (magicprefix / magicsuffix) and the stat IDs (itemstatcost) to resolve to the *same row layout that produced the save*. Restoring all three table pairs to the commit-6dca8854 layout is exactly the minimum-correct compatibility surface for that workflow:

1. **Correct surface (Q1):** Yes. Saved rares store (a) affix row indices into magicprefix/magicsuffix and (b) stat IDs from itemstatcost (with Save Bits / Save Param Bits driving the bit-packing). Restoring all three to the pre-top-50 state aligns row indices, stat IDs, and bit allocations with what serialized the old saves.

2. **All three together is materially safer than partial (Q2):** Yes, and partial restoration would itself be a High risk:
   - Restoring only magicprefix/suffix without itemstatcost: affix rows would resolve, but the stat IDs they reference (and the bit-packing in the save stream) would still be the new layout → mis-decoded stat blocks, likely the same CTD.
   - Restoring only itemstatcost without magicprefix/suffix: affix row indices would still index into the new (shifted) affix tables → wrong/missing affixes, and the moment any rare with an out-of-range affix row hits the loader, you get the original CTD again.
   - Restoring all three pairs is the coherent set. Active/base hash match and column validation confirm it lands cleanly.

3. **Acceptable as temporary commit (Q4):** Yes, provided the commit message clearly tags it as a temporary rescue tied to a follow-up restore commit. After the user has loaded the save, deleted every rare with an old GA marker, and saved out, the cleaned save no longer contains any old GA affix indices and the top-50 layout can be restored without re-triggering the CTD. Items without GA markers are unaffected by the affix-range churn either way.

## Low-risk follow-ups (non-blocking)

1. **properties.txt was not restored (Q3).** If any of the restored old prefixes/suffixes have `mod1code` / `mod2code` values pointing at property names that no longer exist in the current properties.txt (e.g., pre-top-50 GA property aliases that were renamed during `ebd57892` / `bc40b5bf`), those mods will silently no-op when the items render. That's fine for the "load → identify → delete" workflow — the items will still load, the affix slot is still there, the user can still identify and dump them — but if you find the items render with suspiciously empty stat blocks or the engine logs property-lookup errors, restore properties.txt from 6dca8854 as well. It is not required for save *load* safety, only for full-fidelity *display* of the doomed items.

2. **Restoration-after-cleanup checklist.** Before the follow-up commit that puts the top-50 GA files back, confirm in-game that the affected stash/character has zero remaining rares (or at minimum zero rares whose magic prefix/suffix index lands above the post-top-50 row count, and zero with old GA marker stats). Otherwise the same CTD returns. A quick `Reset Stash` / character-by-character pass should be enough.

3. **Commit messaging.** Use a message that makes the temporary status loud, e.g. `Temporary: restore pre-top-50 GA compat tables to rescue old save — revert after cleanup`. The repo's recent history (`fc2779cb`, `0a2b6c77`, `01a3b111` etc.) already shows clear intent labels; matching that style helps the next bisect.

4. **Make sure the planned restore commit reverts exactly these six paths.** When you put the top-50 layout back, do it as a clean `git checkout <top-50-commit> -- <the six paths>` against the post-cleanup HEAD, so the restore commit's diff is the literal inverse of this rescue commit. That keeps `git log -p` on these tables readable and makes any future bisect deterministic.

5. **Do not push other unrelated changes in the same commit.** The session-start status had unrelated modifications in `docs/ai-review/tasks/...` request.md files and some untracked review artifacts. Keep this rescue commit scoped to the six TSVs only so the eventual revert is mechanical.

6. **Carry-over from prior reviews (not part of this fix):** `Task folders:` block at `docs/ai-review/protocol.md` lines 106–110 is still unlabeled as legacy. Cosmetic; fold in whenever you next touch protocol.md.

## Validation Checks

- Original user request reviewed: yes
- Git diff or design reviewed: diff stat reviewed; full content not opened, but the local validation reported (active/base hash match, column counts pass) is the right gate for a same-revision restore
- TSV column counts checked: confirmed by your validation script
- Active/base sync checked: yes (hash match reported across all three pairs)
- Tooltip vs gameplay consistency considered: yes — partial mismatch possible on missing properties.txt entries; non-blocking for rescue workflow
- Live publish risk considered: yes — deploy already done locally, which is the right ordering for a save-load rescue
- Docs checked: n/a for this change

Verdict: **APPROVED** — zero Critical, zero High. Safe to commit as a temporary rescue. Plan the inverse restore commit before you forget which files you touched.
