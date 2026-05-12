# XavReimagined Custom Workflow

This branch is for personal changes on top of D2R Reimagined.

## Branches

- `next` mirrors the official upstream `D2R-Reimagined/d2r-reimagined-mod` branch.
- `xav-custom` is the working branch for your edits.
- `backup-before-fresh-start-20260512` preserves the previous state of your GitHub repo before the fresh reset.

## Editing

Most gameplay edits live in `data/global/excel/*.txt`.

Common starting points:

- `armor.txt`, `weapons.txt`, `misc.txt`: item bases.
- `uniqueitems.txt`, `setitems.txt`, `sets.txt`: uniques and sets.
- `skills.txt`, `skilldesc.txt`: skill behavior and display data.
- `treasureclassex.txt`: drop tables.
- `cubemain.txt`: cube recipes.

## Installing Locally

From this repo:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\install-local.ps1
```

If Diablo II Resurrected is installed somewhere else:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\install-local.ps1 -D2RPath "D:\Games\Diablo II Resurrected"
```

Launch with:

```text
-mod XavReimagined -txt
```

## Updating From Upstream

```powershell
git fetch upstream
git switch next
git merge --ff-only upstream/next
git push origin next
git switch xav-custom
git rebase next
git push --force-with-lease origin xav-custom
```
