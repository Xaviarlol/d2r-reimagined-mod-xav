# Greater Affix Presentation Implementation

Date: 2026-05-20

## Decision

The follow-up spec proposed cloning every Greater affix `itemstatcost.txt` stat so each clone could use a colored display string. I did not implement that literally for live gameplay.

D2R gameplay systems commonly look up the original stat IDs directly. A cloned stat such as `greater_strength`, `greater_item_fastercastrate`, or `greater_fireresist` can be made to display like the original stat, but it is not guaranteed to feed Strength, FCR, resist, damage, or other engine calculations. That would risk creating Greater affixes that look powerful but do not actually work.

## First Implemented Approach

Instead, Greater affixes now use property wrappers in `properties.txt`:

- `greater_<property>` copies the source property exactly and applies the original gameplay stat.
- `greater_m_<property>` also copies the source property, but embeds the existing `item_greaterAffixMarker` display stat inside the property itself.

Each Greater affix row uses one `greater_m_` property and any remaining Greater properties use `greater_` wrappers. This keeps the original gameplay stat IDs intact while removing the separate `greater-affix-marker` mod slot from almost every Greater affix row.

## Known Exception

The `dmg-elem` property already uses all seven property function slots. Those six Greater elemental-damage rows still keep the separate `greater-affix-marker` mod slot because there is no safe free property function slot to embed it.

## Result

- Existing Greater affix behavior remains tied to original D2R stats.
- 903 of 909 Greater rows no longer spend a magicprefix/magicsuffix mod slot on the marker.
- The marker line remained the current visible chase signal.
- True per-stat coloring for core stats still needed a proven D2R data pattern that keeps original stat IDs active while overriding display per affix.

## Second Pass: Colored Greater Stat Rows

Eric clarified that the desired result is for the Greater stat lines themselves to be colored differently.

The second pass implements that literal presentation layer:

- Added `greater_<stat>` rows to `itemstatcost.txt` for every stat used by Greater affix properties.
- Added matching `GreaterAffix_*` strings to `item-modifiers.json`, wrapped with the same `ÿc8...ÿc3` color-control format used by existing colored modifier strings.
- Repointed Greater property wrappers to the `greater_<stat>` rows.
- Removed the visible `GREATER AFFIX:` marker from Greater affix rows and wrappers.

This makes Greater stat lines visually distinct. If any direct core stat clone proves not to feed the underlying gameplay stat correctly in-game, that specific family will need a targeted fallback.
