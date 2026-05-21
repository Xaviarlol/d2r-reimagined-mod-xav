# Claude Review Request: Temporary Greater Affix Compatibility Restore

We need a pre-commit review for a temporary rescue build in the D2R mod repo.

## User request
The game only crashed after click-to-continue. A fresh empty save folder fixed it, implying old save/stash data has rare items with old Greater Affix stat/affix IDs. The user asked to temporarily re-add the old affix files so they can load the old save, remove all rares that have the old Greater Affixes, then restore the new version.

## Implementation under review
Restore these six files from commit 6dca8854 (last pre-top-50 Greater Affix state):

- data/global/excel/itemstatcost.txt
- data/global/excel/base/itemstatcost.txt
- data/global/excel/magicprefix.txt
- data/global/excel/base/magicprefix.txt
- data/global/excel/magicsuffix.txt
- data/global/excel/base/magicsuffix.txt

This brings back the old 511-row Greater Affix layout and old full prefix/suffix set for save compatibility only.

## Local validation already run
- Active/base file hashes match for all three table pairs.
- TSV column validation passed for all six files.
- Deployed locally to E:\Diablo II Resurrected\mods\XavReimagined\XavReimagined.mpq.
- Old save folder was restored after the temporary rescue data was deployed.

## Git status for reviewed files
`	ext
 M data/global/excel/base/itemstatcost.txt  M data/global/excel/base/magicprefix.txt  M data/global/excel/base/magicsuffix.txt  M data/global/excel/itemstatcost.txt  M data/global/excel/magicprefix.txt  M data/global/excel/magicsuffix.txt
`

## Diff stat
`	ext
 data/global/excel/base/itemstatcost.txt | 123 +++---  data/global/excel/base/magicprefix.txt  | 711 +++++++++++++++++++++++---------  data/global/excel/base/magicsuffix.txt  | 457 +++++++++++++++++---  data/global/excel/itemstatcost.txt      | 123 +++---  data/global/excel/magicprefix.txt       | 711 +++++++++++++++++++++++---------  data/global/excel/magicsuffix.txt       | 457 +++++++++++++++++---  6 files changed, 1972 insertions(+), 610 deletions(-)
`

## Review focus
Please check for Critical/High issues only:

1. Does this restore the correct compatibility surface for old rare Greater Affix items?
2. Is restoring itemstatcost, magicprefix, and magicsuffix together safer than restoring only one of them?
3. Are there any additional files that must be restored for old saved rares to load safely?
4. Is this acceptable as a temporary rescue commit, assuming we will restore the current top-50 GA files after the user deletes the old rare items?

Return a concise verdict with any blockers. If no blockers, say APPROVED.
