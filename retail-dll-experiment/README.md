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
- Startup/proxy loading through an app-local `winmm.dll` is detected by retail D2R as unsupported software. Do not leave `winmm.dll` in the retail game folder.
- Next likely path: a non-retail test runtime or a closer reproduction of the current D2RLaunch runtime behavior that does not trip retail's unsupported-software check.

## Startup Proxy Test

Retail `D2R.exe` imports `D2R_loader.dll`, and that loader imports `WINMM.dll` only for `timeGetDevCaps`. The startup proxy test installs an app-local `winmm.dll` that forwards `timeGetDevCaps` to the real Windows DLL and writes a log when it loads.

This path reached D2R startup, but latest retail D2R reports error `0x1100` for the app-local `WINMM.dll`. Treat this as a failed approach unless testing outside the latest retail runtime.

Install:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\install-retail-proxy-loader.ps1 -D2RPath "E:\Diablo II Resurrected"
```

Remove:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\remove-retail-proxy-loader.ps1 -D2RPath "E:\Diablo II Resurrected"
```

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
