---
name: D2R modding reference resources
description: External resources for D2R data files, property/skill/missile codes, mod design intent. Use when reviewing changes that touch unfamiliar TSVs or property codes.
type: reference
originSessionId: 80430070-75f6-4d4b-afde-059a1f4801e5
---
External resources for D2R modding lookups. These don't change often, but the content does — always WebFetch when consulting, don't recall from this memory.

## 1. eezstreet d2rdoc — authoritative D2R data file reference

- Base: `https://eezstreet.github.io/d2rdoc/`
- Per-file page pattern: `https://eezstreet.github.io/d2rdoc/files/<filename>.html`
- Source repo: `https://github.com/eezstreet/d2rdoc` (markdown sources in `contrib/guides/`, data in `data/files/*.js`)
- **Use when:** verifying that a property code like `half-freeze`, `dmg-pois`, `light-thorns`, `mana-kill`, `att-undead` exists and behaves as expected; checking TSV column meanings; investigating skill/missile fields; understanding cube/treasure class formats.

Key per-file pages (replace `<name>` in the URL pattern; the .js suffix in the list below = .html on the site):

- **Item content:** setitems, sets, uniqueitems, runes, magicprefix, magicsuffix, rareprefix, raresuffix, automagic, uniqueprefix, uniquesuffix, uniqueappellation
- **Property/stat system:** properties, propertygroups, itemstatcost (THE canonical list of stat codes used in `prop1..prop9`/`aprop*` columns), shareditemmods
- **Base items:** itemtypes, itemuicategories, armor, weapons, misc, gems, belts, books, shareditems, qualityitems, lowqualityitems, runeworduicategories, gamble
- **Skills & missiles:** skills, skilldesc, skillcalc, missiles, misscalc, states, overlay
- **Loot & recipes:** treasureclassex, cubemain, itemratio
- **Monsters:** monstats, monstats2, monlvl, monumod, monpreset, monequip, montype, monprop, monai, monpet, monplace, monseq, monsounds, hireling, hirelingdesc, npc, superuniques, wanderingmon
- **World/levels:** levels, lvlmaze, lvlprest, lvlsub, lvltypes, lvlwarp, levelgroups, desecratedzones, actinfo, objects, objgroup, objmode, objpreset, shrines
- **Character:** charstats, experience, playerclass, plrmode, plrtype
- **Misc/system:** inventory, storepage, sounds, soundenviron, colors, events, difficultylevels, hitclass, monmode, compcode, composit, automap, enums (constants)

The site is JS-rendered — `WebFetch` of `index.html` only shows the landing page. Always fetch the specific `/files/<name>.html` page you need.

## 2. D2R Reimagined wiki — mod-specific design intent

- Base: `https://wiki.d2r-reimagined.com/`
- Wiki.js SPA. Known URL patterns:
  - `/en/<Topic>` — e.g., `/en/ClassChanges`, `/en/Installs`, `/en/new_player_guide`
  - `/en/Items/<Sub>` — e.g., `/en/Items/Charms`, `/en/Items/LootTable`, `/en/Items/Orbs`, `/en/Items/Runes`
  - `/en/recipes/<Sub>` — e.g., `/en/recipes/Crafting`, `/en/recipes/CubeRecipes`, `/en/recipes/ItemEnchants`
- **Use when:** I need to understand the *intent* of a mod-specific change — e.g., what role charms play in this mod, the design philosophy behind a class redesign, what cube recipes the mod has added, how loot tables differ from vanilla.
- **Don't use for:** vanilla D2R technical docs (use eezstreet instead).
- WebFetch only sees the page shell; for body content use `curl -s -L -A "Mozilla/5.0" <url>` and parse the response.

## 3. D2R Reimagined public source on GitHub

- Repo: `https://github.com/D2R-Reimagined/d2r-reimagined-mod`
- Default branch for PRs: `next`
- Releases: tagged on `next`; latest is v3.0.9 as of May 2026 (advance the version when verifying)
- Eric's fork/local works on branch `xav-custom`; PRs target `next` (the same `next` branch Eric calls "main branch" in his project notes).
- Top-level layout: `data/`, `lint/`, `scripts/`, plus `modinfo.json`.
- Companion: a launcher project also under the `D2R-Reimagined` org.
- Nexus: `https://www.nexusmods.com/diablo2resurrected/mods/503`
- **Use when:** I need to confirm whether a change exists in the public source vs. Eric's local; check open issues/PRs on the public repo (`gh` CLI is **not** installed in this environment — use `curl https://api.github.com/repos/D2R-Reimagined/d2r-reimagined-mod/...` for read-only API queries).

## 4. Holy Grail spreadsheet (NOT a modding reference)

- URL: `https://docs.google.com/spreadsheets/d/1Lg4pez86LkdcB933I4kE6IWUMWDqh2BD15Y-4mzY0w4/`
- Read-only, requires Google auth to view. Public scrape only sees summary headers.
- This is an **item-collection checklist** for players doing Holy Grail runs on the mod — not a property/stat/skill reference. Don't try to use it for review lookups. Tabs are organized by item type (Sets, Armor, Belts/Boots/Gloves, Helms, Shields, Misc, Axes, Bows & Crossbows, Claws, Maces, Polearms & Spears, Staves/Wands, Swords, Throwing).

## Practical fetch tips

- The shell is PowerShell (Windows). Use `curl -s -L -A "Mozilla/5.0" <url>` for raw HTML; `WebFetch` for AI-summarized content.
- `gh` CLI not available. For GitHub data, use the API directly: `curl https://api.github.com/repos/<owner>/<repo>/contents/<path>`.
- Most JS-rendered SPAs (eezstreet `index.html`, the wiki landing) return only the shell on raw fetch; go to the specific content URL instead.
- The eezstreet `/files/<name>.html` pages are JS-rendered, but the underlying data is in `https://raw.githubusercontent.com/eezstreet/d2rdoc/master/data/files/<name>.js` — fetch the raw JS file when WebFetch summaries get truncated. The structure is a JSON-ish array with `"name"` + `"description"` per field. `grep -B1 -A3 '"name"'` gives a clean field list.
- WebFetch sometimes refuses to "reproduce" a long markdown file. Switch to `curl -s` + `head`/`grep` to get raw content.

## Non-obvious facts that affect review decisions

These are not derivable from re-reading the repo — keep handy.

**Game Mode Split (the real reason for active/base):**
- `data/global/excel/` (active) = used by **"Reign of the Warlock"** game mode in v3.0+.
- `data/global/excel/base/` (base) = used by **Classic** and **Expansion** game modes.
- A few files (`sounds.txt`, `soundenviron.txt`) always come from `/excel/` regardless of mode.
- **Indices must match across modes** to prevent save-corruption when characters traverse modes. Renaming or reordering rows in one but not the other is unsafe.
- When reviewing: a change to active only is fine if it's mode-specific. A change that should affect all modes needs both copies updated. Eric's project conventions reflect this; this is the underlying reason.

**Frame timing:** D2's internal clock is **25 frames per second**. `ELen 25` = 1 sec. `ELen 50` = 2 sec. `ELen 100` = 4 sec. This applies to poison/cold/freeze/stun durations in skills.txt and missiles.txt.

**SrcDam vs SrcDamage (skills.txt vs missiles.txt):**
- Both encode weapon damage as **128ths** — `128` = 100%, `64` = 50%, `0` or `-1` = no weapon damage transferred.
- skills.txt `SrcDam`: weapon damage transferred to direct-damage skills (melee, simple ranged).
- missiles.txt `SrcDamage`: weapon damage transferred to the missile's hit damage.

**Skill ↔ missile damage inheritance — THE rule (from Phrozen Keep Missiles.txt guide):**
- Missiles.txt column **`Skill`** (column 108 in this mod's missiles.txt) controls inheritance.
- **If `Skill` is set** to a skill ID/name, the missile **pulls all of these fields from the linked skill row, ignoring the missile-row values**: `ResultFlags, HitFlags, HitShift, HitClass, SrcDamage (called SrcDam in skills.txt), MinDam, MinLevDam1-5, MaxDam, MaxLevDam1-5, DmgSymPerCalc, EType, EMin, EMinLev1-5, EMax, EMaxLev1-5, EDmgSymPerCalc, ELen, ELenLev1-3, ELenSymPerCalc`.
- **If `Skill` is empty**, the missile uses its OWN values for those fields.
- **Always check the missile's `Skill` column before reasoning about whose damage values apply.**
- For Cobra Strike specifically: `cobrastrikenova` missile has `Skill = empty` → missile's own E* drives charge 3 damage. The `Cobra Strike Nova` helper skill row (id 490) E* fields are **dead code for nova damage** in this configuration. (Resolves the MED-001 question from the 2026-05-14 review — charge 3 is *not* nerfed by the patch; old and new effective damage both = missile's `8/14` over 50 frames.)

**SrcDamage signal values (missiles.txt):**
- `128` = 100% weapon damage transferred.
- `0` or `-1` = no weapon damage transferred (e.g., pure ele clouds).

**Missile damage does NOT require a hit/damage function — collision damage is built in:**
- `pSrvDoFunc=1` (`MissileDoArrow`) is the **standard damaging-projectile function**. Basic missiles (`arrow`, `bolt`, `firebolt`) all use `pSrvDoFunc=1` with NO `pSrvHitFunc` / `pSrvDmgFunc` and still deal damage. Collision detection + damage application are built into the standard processing.
- `pSrvHitFunc` / `pSrvDmgFunc` are for SPECIAL on-collision behavior (explosions, sub-missile rings, firewall periodic ticks) — NOT required for a missile to deal basic damage.
- Do NOT conclude "no hit function = no damage." A missile with `Collision=1` + `EType`/`EMin`/`EMax` set deals that damage on collision via the standard function.
- Two valid ways to build a damaging ground-fire field, both work:
  - **Firewall** (vanilla `meteorfire`): `pSrvDoFunc=5` (`srv-Firewall`) + `pSrvDmgFunc=3` (`DamageFireWall`) — periodic AoE, ticks units in its area on an internal cadence.
  - **Collision missile** (mod's `royalstrikemeteorfire`, `fistsoffirefirewall`): `pSrvDoFunc=1` + `Collision=1` — a lingering missile that damages units that collide with it. Confirmed in-game: it deals damage for its **entire** lifetime, including a skill-extended duration (e.g. `royalstrikemeteorfire`'s lifetime is set to Royal Strike's `Param3 + Param4*lvl` "Duration of ground fire" via the `HitMeteorCenter` function). The standard function does NOT cap the damage at the animation length.
- Phoenix Strike's meteor burn (`royalstrikemeteorfire`) is a fully functional collision-damage field — confirmed in-game, damages for its full ~`30+15*lvl`-frame duration.
- **CAUTION (lesson learned):** do NOT infer D2 *engine behavior* (damage windows, throttling, "visual-only", whether a field stacks) from missile/skill function IDs alone — that produced 3 wrong calls on `royalstrikemeteorfire` in one session. Function IDs and column values are reliable *data* facts; behavior conclusions are hypotheses to verify in-game, not findings to assert.

**HitShift damage scaling — 256ths-based:**
- HitShift is a damage divisor in 256ths. Value → fraction: `8 = 256/256 (100%)`, `7 = 128/256 (50%)`, `6 = 64/256 (25%)`, ..., `0 = 1/256 (0.39%)`.
- Same convention in both skills.txt and missiles.txt. Default for most skills is `8`.

**What `SrcDam`/`SrcDamage` actually carries (researched 2026-05-17):**
- `SrcDamage` transfers ONLY: (1) the source unit's **weapon physical damage** (the raw min-max already scaled by +%ED, +min/max dmg, str/dex), and (2) **Life Steal / Mana Steal** (leech is bundled into the "attack properties" and the missile-damage path has explicit `No Life Steal`/`No Mana Steal`/`No Stamina Steal` Hit Flags bits).
- `SrcDamage` does **NOT** carry on-hit attack procs to skill-fired (spell-type) missiles:
  - **Open Wounds** — attack-gated. Maxroll D2R: applied only to skills doing a "Melee or Ranged Attack with a physical component", NOT spell-cast missiles.
  - **Deadly Strike / Critical Strike** — attack-gated; doubles physical damage on weapon attacks only.
  - **Crushing Blow** — attack-gated weapon-strike mechanic.
  - **Venom / Envenom poison** — Venom adds poison to weapon attacks / attack skills; rides the attack path, not spell missiles. SrcDamage moves weapon *damage*, not the caster's poison-buff stat.
- The dividing line is **ATTACK vs SPELL**, not physical vs elemental. OW/CB/DS/Venom check "did a weapon attack land?". A bow's arrow carries them because the arrow IS the bow attack (skill `aitype` = ranged attack). A skill-released nova/cloud/meteor missile is a spell missile — its hit is not an "attack", so those procs never roll, even with `SrcDamage=128`.
- The `Hit Flags` enum (in `enums.js`, referenced by missiles.txt `HitFlags`) has 11 bits: `Do not add physical damage`, `Do not add any damage`, `No Life Steal`, `No Mana Steal`, `No Stamina Steal`, `Use Source Damage`, `Add Elemental Damage to Steals`, `No Triggered Events`, `Bypass Undead/Demons/Beasts`. Note there is NO Open Wounds / Crushing Blow / Deadly Strike flag — confirming those aren't part of the missile-damage routine.
- **Intra-skill consequence for charge-up skills:** a charge released via an *attack* function DOES roll OW/CB/DS + Venom; a charge released as a missile does NOT. Verified for current Cobra Strike: **charge 1** = `srvprgfunc1` empty → `srvdofunc=34 AssDoProgressiveAttack` ("attempt to attack the target unit") = a real attack → carries procs. **Charge 2** = `srvprgfunc2=36 ApplyClawsOfThunderLvl2` → fires `cobrastrikecloudhit` missile → spell missile → NO procs. **Charge 3** = `srvprgfunc3=36` → fires `cobrastrikenova` → NO procs. So Cobra splits 1-vs-2&3, not 1&2-vs-3. Phoenix Strike `royalstrike*` releases are missiles → no procs.
- Review implication: when Codex puts `SrcDamage=128` on a skill missile, read it as "weapon damage + leech", NOT "the player's full melee attack package". Flag any design that assumes a `SrcDamage` nova/release inherits a build's Open Wounds / Crushing Blow / Deadly Strike / Venom.

**`SrcDam`/`SrcDamage` and elemental damage (researched 2026-05-17):**
- Engine formula: `DmgTotal += DmgWeap * SrcDamage / 128`. `DmgWeap` is the weapon's **physical** damage.
- Whether the weapon's **elemental affixes** (`+X-Y fire/cold/etc damage` mods on the weapon item) transfer through `SrcDamage` to a spell missile is **not definitively documented** — the Phrozen Keep thread asking exactly this ended inconclusive (Nefarius recommended empirical testing). Best assessment: physical transfers reliably; weapon elemental affixes probably do NOT carry cleanly to a spell missile. Treat as "test before relying on it".
- **CRITICAL GOTCHA — use only `0` or `128`, never mid-range:** a `SrcDam`/`SrcDamage` value that is not `0` and not `128` does NOT just scale weapon damage — it also silently scales the skill/missile's **own** `EMin/EMax` elemental damage downward. Phrozen Keep moderator testing on Lightning Bolt confirmed: `SrcDam=96` one-shot the dummy, `SrcDam=1` took many hits, `SrcDam=0` one-shot again. So mid-range values corrupt the skill's intended elemental damage. Only `0` (no weapon damage) and `128` (100% weapon damage) are safe. When reviewing, flag any `SrcDam`/`SrcDamage` cell set to a value other than 0 or 128 (e.g. `64`) as a latent bug that shrinks that row's own elemental curve.

**BBE / Calc formula language** (used in `desccalca/b`, `calc1-10`, `srvprgfunc#`, `prgcalc#`, missile `Param#` calcs, etc.):
- Arithmetic: `+ - * / ^` with parentheses.
- Comparisons: `< <= > >= == !=`.
- Ternary: `(cond) ? (if_true) : (if_false)`.
- Logic shorthand: `*` works as AND (any 0 → 0), `+` works as OR (any non-zero → non-zero). 0 = false, non-zero = true.
- Identifiers in skill scope: `lvl` (skill level), `blvl` (base skill level), `par1..par20` (skill row params).
- Functions:
  - `min(a,b)`, `max(a,b)`, `rand(a,b)`
  - `skill('Skill Name'.identifier)` — lookup by unit's level
  - `miss('Missile Name'.identifier)` — lookup missile field
  - `stat('Stat Name'.accr|base|mod)` — stat from itemstatcost
  - `sklvl('Skill Name'.idToGetLevel.identifier)` — lookup at specific level
  - `sksrc('Skill Name'.identifier)` — by source unit's level
  - `cond('Condition Name', param)` — returns 0/1; conditions include `IsType`, `IsClass`, `Desecrated`, `Difficulty`, `MonsterTestElite`, `ItemIsType`, `ItemIsModType`.

**Skill tooltip text lives in THREE files that all have to stay in sync** (lesson from missing the Cobra Strike tooltip-duration fix in 2026-05-14-0030 review):

1. **`data/global/excel/skills.txt`** — gameplay values: `ELen`, `EMin`, `EMax`, `SrcDam`, etc.
2. **`data/global/excel/skilldesc.txt`** — formulas that compute the displayed numbers. Contains `*ELen/16` style constants embedded in the formula string, e.g. `(8+...)*50/16` for a 50-frame duration. **The "50" is a literal, not a reference to `ELen` — change `ELen` and the formula constant must change too.**
3. **`data/local/lng/strings/skills.json`** — the string templates that the tooltip uses, e.g. `"Charge 1 - Poison Damage: %d-%d over 2 sec + weapon damage"`. **The "2 sec" is hardcoded text — change the duration and this literal must change too.**

When reviewing a skill tuning change that touches `ELen`, damage curves, or any numeric value that appears in displayed text:
- Always grep `data/local/lng/strings/skills.json` for the relevant string keys (e.g., `Eskill<skillname>1/2/3`, `Skillsd<id>`, `Skillld<id>`, `StrSkill<Class><Skill><Charge#>`) and check for hardcoded numbers that match the OLD value.
- Check ALL languages (`enUS`, `deDE`, `esES`, `frFR`, `itIT`, `koKR`, `plPL`, `esMX`, `jaJP`, `ptBR`, `ruRU`, `zhCN`, `zhTW`) — the mod often updates `enUS` only, leaving stale vanilla-D2 text in the other 12.
- Specifically check for: literal `"X sec"` / `"X seconds"` / `"X yards"` / `"+X%"` / `"X to Y damage"` patterns in the string templates.
- If a skill swaps gameplay behavior (e.g., vanilla life-steal Cobra Strike → mod poison Cobra Strike), the `Skillsd<id>` / `Skillld<id>` long descriptions are also localized text that may still describe the vanilla behavior. Often only `enUS` was updated.

**Skilldesc charge-up display (lessons from Cobra Strike review):**
- `descline1..6` are core tooltip lines. `dsc2line1..5` are pinned lines AFTER core. `dsc3line1..7` are pinned lines AT BOTTOM. They render simultaneously, not for different charges.
- For charge-up skills, the **per-charge character-screen damage** display uses `p1dmelem/p1dmmin/p1dmmax`, `p2dmelem/p2dmmin/p2dmmax`, `p3dmelem/p3dmmin/p3dmmax`. These show the three charge tiers' damage.
- `descline#` numeric ID picks the line function. Common: 36, 40, 56, 74, 75, 76, 77. `75` is one of the elemental-damage line functions. The string in `desctexta#` is usually a localization key like `Skillname123` or `Eskillcobra1`.

**Item quality roll algorithm** (when reviewing TC / drop changes):
- Engine rolls Unique → Set → Rare → Magic → Superior → Normal → Low Quality in descending order. First success wins.
- Probability = `(Quality - (mlvl - ilvl) / Divisor) * 128` from `itemratio.txt`. Lower probability = better chance.
- Magic Find bonus over 110% gets diminishing returns; then `probability *= 100 / MF`.
- Final clamp: roll 0..probability; if ≤ 128, quality succeeds.

**TreasureClassEx mechanics (refined):**
- Drop probability for each item = `Prob# / (sum of NoDrop + Prob1..Prob10)`, not divided by 1024.
- `Picks > 0` (0..6): loop counter. Game runs the pick-drop routine `Picks` times. **Hard cap of 6** without code editing.
- `Picks < 0` (-1..-6): deterministic; each `Prob#` becomes a quantity rather than a probability. Example `Picks=-6, Item1=2, Item2=1, Item3=3` → always drops 2+1+3 = 6 items.
- `NoDrop` scales down with player count in multi-player games, reducing no-drop chance proportionally.
- `level` field within a `group`: monster picks the TC with the **nearest level** to its own (not just `level ≤ monster level`).
- Gotchas:
  - **Never move or rename the gold row** — game depends on it being in place.
  - TC ID pointers are **case-sensitive**.
  - Duplicate TC IDs: first occurrence wins, duplicates silently ignored.
  - Auto-TCs `armo3..armo99` and `weap3..weap99` are controlled by `ItemTypes.txt` `TreasureClass` column.

**Cubemain mechanics (refined):**
- Up to **7 inputs** (`input 1..input 7`) and up to 3 outputs (`output b`, `output c` are 2nd/3rd outputs).
- Input/output item specs combine **base code + quality params**:
  - Quality: `nor` (normal), `mag` (magic), `rar` (rare), `uni` (unique), `set` (set)
  - Other: `low` (low qual), `hiq` (superior), `nos` (no sockets), `sock=N` (N sockets), `bas`/`exc`/`eli` (base/exceptional/elite), `eth` (ethereal), `qty=N` (quantity needed)
- `op` column gates the recipe:
  - `1` = day of month; `2` = day of week
  - `3..14` = player stat conditions (Accr / Base / Bonus, with `<`/`>`/`=`/`≠` operators)
  - `15..26` = item stat conditions on input
  - `27..28` = quest difficulty conditions
- Output item level math:
  - `lvl` = forced item level for output
  - `plvl` = % of player level
  - `ilvl` = % of input 1's item level
  - `lvl` is also the base for the `plvl`/`ilvl` percentage calculations
- Up to **5 mod properties** on output (`mod 1..mod 5`), each with `chance` (percent), `param`, `min`, `max`.
- `usetype` / `useitem` decide whether output is a fresh base item or a copy of input 1's identity.
- `class` restricts the recipe to one character class.

**Item stat cost (itemstatcost.txt) basics:**
- `Send Bits` caps the stat's max raw value (network-side).
- `Saved` = does it persist in save files. Combined with `CSvBits`/`CSvParam` for save layout.
- `Encode` controls how min/max/duration are stored — especially relevant for poison and cold (duration encoded into the same value).
- `fCallback` = recompute character state when this stat changes.
- `descfunc/descval/descstrpos/descstrneg` build the tooltip line.
- `op`/`op param`/`op base`/`op stat#` chain stats together (e.g., "per-level" stats).

**Properties.txt as a translation layer:**
- Properties bridge between item rows (setitems/uniqueitems/magicprefix/etc.) and itemstatcost stats.
- Each property row has up to 7 (`func1..7` + `stat1..7` + `val1..7` + `set1..7`) effects.
- Common `func#` values: 1 = random between min/max; 2 = always max; 5/6 = set min/max damage; 9 = +N to specific skill; 10 = +N to skill tab; 11 = skill-on-attack.

**Wiki access workaround:**
- `wiki.d2r-reimagined.com` is a Wiki.js SPA. `WebFetch` only sees the page shell.
- Get internal page list via `curl -s -L -A "Mozilla/5.0" https://wiki.d2r-reimagined.com/en/<known-page>` and grep `href="/en/...` from raw HTML.
- Known top-level pages from seed crawl: `/en/ClassChanges`, `/en/Installs`, `/en/new_player_guide`, `/en/Items/{Charms,LootTable,Orbs,Runes}`, `/en/recipes/{Crafting,CubeRecipes,ItemEnchants}`. There are more — re-crawl from any page when needed.

**Sets.txt vs SetItems.txt:**
- `Sets.txt` defines the **set-piece-count** progressive bonuses. `PCode2a/2b` activate with 2+ items, `PCode3a/3b` with 3+, etc. `FCode1..8` activate only with the **full set** equipped.
- `SetItems.txt` defines per-item visible affixes (`prop1..9`) and the **green per-piece bonus chains** in `aprop1a..5b` columns.
- `add func` column on SetItems.txt controls how `aprop#` chains activate based on other equipped set pieces. (Sets.txt KB defers to a separate SetItems.txt guide for these details — fetch that if reviewing `add func` changes.)

**D2R-specific quirks:**
- Uses **CASC archives** (not MPQ as in classic D2). Files are extracted from CASC for modding.
- Resurrected (HD) graphics live in `data/global/hd/`; legacy graphics live in `data/global/` (without `/hd/`).
- The `-mod <name> -txt` launch args are required, and Vicarious Visions disabled the legacy `-direct` flag in D2R.

## Additional resource indexes (when going deeper)

**The Phrozen Keep — d2mods.info — canonical community archive.** Knowledge Base format: `https://d2mods.info/forum/kb/viewarticle?a=<id>`. Highest-value KB articles I've confirmed:
- `a=350` — Skills.txt file guide
- `a=370` — SkillDesc.txt file guide (Appendix B with 75 descline function IDs lives on the actual page; AI fetchers may not return it — view directly)
- `a=368` — TreasureClassEx.txt
- `a=349` — Sets.txt
- `a=284` — CubeMain.txt
- `a=477` — Getting Started with D2R modding
- Masterlist of all guides: `https://d2mods.info/forum/viewtopic.php?t=34455`
- Missiles.txt forum guide (not in KB format): `https://d2mods.info/forum/viewtopic.php?t=34583`
- Beginner's Guide PDF (full LoD reference, classic D2 but mechanics carry over): `https://phrozenkeep.blob.core.windows.net/public/files/resources/BeginnerGuide-v14.pdf`

**locbones D2R Data Guide** (alternative reference, color-coded format, marked WIP): `https://locbones.github.io/D2R_DataGuide/`. Covers ~60 files including D2R-specific ones like `ActInfo.txt`. Truncated coverage of some files at the time of last check.

**d2rmodding.com** — practical tutorials: `https://www.d2rmodding.com/guides`
- Video series: **HitchHiker's Guide to D2R Modding** (10 episodes, intro) and **The Catacombs** (24 episodes, advanced including splash, particles, custom warps, monsters, NPCs, drop odds, skill icons, passives, status icons, properties, breakpoints, hardcoded bypasses).
- Categories: Item (7), Monster (4), Skill (5), General (11), UI/Visual (7).

## Out-of-scope of eezstreet (don't expect to find docs here)

- The mod's custom **JSON state machines** (e.g., `paladin_state_machine.json` seen in recent commits) — these are repo-specific, not part of standard D2R modding. Read the JSON itself + any neighboring `.md` design docs in the repo.
- The mod's `scripts/` toolchain (Python/JS file-compare and install helpers).
- The launcher project (separate repo under `D2R-Reimagined` org).
- Particle effects, level editing, animation editing, code editing — not officially supported per the eezstreet getting-started guide.
