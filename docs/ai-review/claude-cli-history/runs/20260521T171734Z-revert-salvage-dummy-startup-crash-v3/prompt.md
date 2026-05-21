# Claude CLI Review Request

## Original User Request
ok so the gwme crashed again on startup

## Context
D2R crashed on startup after recent Greater Affix and salvage recipe work. The suspected risky regression is commit 01a3b111, which added item_salvageDummy ID 488 in itemstatcost, added a salvageDummy property, and rewrote salvage cube recipes to use that stat/property.
This project has already hit hard limits around itemstatcost and tooltip stat rows, so the immediate proposed fix is a staged no-commit revert of 01a3b111.

Please use the Read tool on these two files for the concrete evidence:
- Status/log/validation file: C:\Dropbox\AI projects\d2r\d2r-reimagined-fresh\docs\ai-review\claude-cli-history\review-inputs\20260521T171550Z-revert-salvage-dummy-startup-crash-status.txt
- Full staged diff file: C:\Dropbox\AI projects\d2r\d2r-reimagined-fresh\docs\ai-review\claude-cli-history\review-inputs\20260521T171550Z-revert-salvage-dummy-startup-crash.diff

## Review Request
Review the staged rollback for crash risk and D2R data-table consistency. Confirm whether committing and deploying this rollback is appropriate. Return APPROVED only if there are no critical/high issues. If approved, mention any low-risk follow-up separately.
