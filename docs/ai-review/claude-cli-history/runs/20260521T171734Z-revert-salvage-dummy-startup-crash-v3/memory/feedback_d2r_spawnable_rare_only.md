---
name: feedback-d2r-spawnable-rare-only
description: "In this mod's engine, affixes with `spawnable=0` do NOT spawn on rare items even when `rare=1`. Stop citing the \"rare-only\" pattern as established behavior."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 43c36c4d-2664-4dbd-b7a5-02c4760ab2ec
---

In magicprefix.txt / magicsuffix.txt, an affix row with `spawnable=0 rare=1` does **not**
spawn on rare items in this mod's D2R engine — even at extreme frequencies. The entire
Greater Affix layer of the rare-affix rework was authored with `spawnable=0 rare=1` and
empirically rolls on nothing in-game.

**Why:** Eric tested directly. With `freq=999999, lvl=1` test rows that had `spawnable=0
rare=1`, no rare item dropped them across many drops. Flipping `spawnable=0 → 1` was the
fix. I had previously argued from "Hulking and group-307 pierce rows are spawn=0 rare=1 in
vanilla" theory without ever empirically verifying they actually spawn — exactly the
"asserting D2 engine behavior from documentation without testing" mistake the broader D2R
modding memory warns against.

**How to apply:**
- Never claim `spawnable=0 rare=1` is a valid "rare-only" pattern in this mod's engine.
- If a design proposes `spawnable=0` for a chase affix, flag it as a likely
  non-spawning bug and recommend `spawnable=1`.
- The Greater Affix rework's whole `spawnable=0 rare=1` design rule (which I reviewed and
  approved across three rounds) was wrong. If Eric asks for an after-action on it, this is
  what to surface.
- If a different "rare-only" mechanism actually exists in this engine, treat that as
  something to test, not assert.

Related context: [[reference_d2r_modding_resources]] has the broader "don't infer engine
behavior from function IDs or docs without testing" lesson.
