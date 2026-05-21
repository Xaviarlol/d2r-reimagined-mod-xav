---
name: Eric — D2R modder
description: Eric runs a Diablo II Resurrected mod called XavReimagined. Repo paths, live folder, branch, launch args, TSV conventions.
type: user
originSessionId: 80430070-75f6-4d4b-afde-059a1f4801e5
---
Eric is the modder behind the Diablo II Resurrected mod **XavReimagined** (also called "D2R Reimagined").

**Paths:**
- Primary repo: `C:\Dropbox\AI projects\d2r\d2r-reimagined-fresh`
- Live game folder: `E:\Diablo II Resurrected\mods\XavReimagined\XavReimagined.mpq`
- Codex's working branch: `xav-custom`
- Main/PR branch: `next`
- Launch args: `-mod XavReimagined -txt`

**Data layout:**
- Active game data: `data/global/excel/`
- Base mirror: `data/global/excel/base/`
- Active and base TSV files typically need to stay in sync.

**TSV conventions:**
- Column count must match the header — empty columns are intentional, never strip trailing tabs or "normalize" casually.
- Do not use Excel to edit TSVs (it mangles them). Recommend script-based or AFJ Sheet Editor-safe edits.
- A clean row keeps the same column count as the header.

**Collaboration model:**
- Codex implements (writes data/code, publishes to live, commits, pushes).
- I review only — see the reviewer-role and ai-review-queue memories.
