# XavReimaginedLAN D2RLAN Experiment

This branch is a side experiment for testing D2RLAN/D2RHUD-style hardcode edits without touching the normal `XavReimagined` branch.

## What Changed

- Mod name: `XavReimaginedLAN`
- Save path: `XavReimaginedLAN/`
- Added `data/D2RLAN/memory_overrides.json`
- Added an experimental memory edit copied from ReMoDDeD/D2RLAN:
  - `Disable Run Penalty for Defense`
  - Addresses: `329F70`, `BCA5A0`
  - Original byte value: `3`
  - Patched byte value: `255`

## Why This Exists

Normal D2R `-mod ... -txt` files do not expose a table setting for the running defense penalty. ReMoDDeD handles it through D2RLAN memory edits, which are applied after launching the game.

## Important Limits

These memory offsets are version-specific. They are intended for the D2RLAN/TCP 2.4 environment used by ReMoDDeD, not necessarily the current retail D2R install.

Do not use this path on Battle.net.

## Install Helper

After D2RLAN is installed, copy this side mod into the D2RLAN D2R folder:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\install-d2rlan-local.ps1 -D2RLANPath "C:\Path\To\D2RLAN"
```

The script accepts either the D2RLAN root folder or the nested folder that contains `D2R.exe`.

If you have only extracted the D2RLAN launcher and have not downloaded the Base TCP files yet, you can stage the mod folder first:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\install-d2rlan-local.ps1 -D2RLANPath "C:\Path\To\D2RLAN" -AllowMissingD2RExe
```
