# Retail DLL Experiment

This is the retail-only experiment for D2R `3.1.x`. It does not use D2RLAN or the old TCP runtime.

The first stage is intentionally harmless:

- `XavReimaginedExperimental` is installed as a side mod next to `XavReimagined`.
- The DLL only writes a log line when injected.
- No gameplay memory is patched yet.

Use this only for offline single-player testing. Do not use injected DLLs on Battle.net.

## Build

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\build-retail-hook.ps1
```

## Install Side Mod And Tools

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\install-experimental-local.ps1 -D2RPath "E:\Diablo II Resurrected"
```

## Launch

Launch without injection:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\launch-experimental-retail.ps1 -D2RPath "E:\Diablo II Resurrected"
```

Launch and inject the no-op DLL:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\launch-experimental-retail.ps1 -D2RPath "E:\Diablo II Resurrected" -Inject
```

The DLL log is written beside the DLL in:

```text
E:\Diablo II Resurrected\mods\XavReimaginedExperimental\tools\xav-retail-hook.log
```
