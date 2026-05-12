# D2RLAN Probe

`XavLANProbe` is a small D2RLAN-compatible side mod for testing memory edits against the TCP/D2RLAN `1.2.69270` runtime.

The full Reimagined data targets retail D2R `3.1.92198`, so it is not expected to load in this older executable. This probe starts from the installed `TCP` mod, overlays selected `1.2.69270` text tables from D2RLAN's bundled `D2Compare` tools, and applies only the lightweight Xav changes that are safe to test there.

Included changes:

- Assassin charge-ups and finishing moves cost `0` mana.
- Burst of Speed, Fade, Blade Shield, and Venom cost `0` mana.
- Burst of Speed, Fade, Blade Shield, and Venom last 30 minutes.
- D2RLAN-only memory overrides for running defense and corpse retrieval.

The probe intentionally keeps stock walk and run speeds so the running-defense patch can be tested directly.
