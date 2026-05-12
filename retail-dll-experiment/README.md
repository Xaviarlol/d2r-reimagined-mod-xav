# Retail DLL Experiment

This is the retail-only experiment for D2R `3.1.x`. It does not use D2RLAN or the old TCP runtime.

The first stage is intentionally harmless:

- `XavReimaginedExperimental` is installed as a side mod next to `XavReimagined`.
- The DLL only writes a log line when injected.
- No gameplay memory is patched yet.

Use this only for offline single-player testing. Do not use injected DLLs on Battle.net.

## Current Status

- The side mod installs and launches against retail D2R `3.1.92198`.
- The no-op DLL builds and loads in a normal local process.
- Retail D2R currently returns null from remote `LoadLibraryW` for this DLL and the prebuilt retail `D2RHud` DLL, while signed Windows DLLs load. That means remote injection is not the working retail path yet.
- Next likely path: startup/proxy loading or a closer reproduction of the current D2RLaunch runtime behavior.

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
