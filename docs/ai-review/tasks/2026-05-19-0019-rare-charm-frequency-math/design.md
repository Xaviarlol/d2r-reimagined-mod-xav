# Rare Charm Frequency Math Review

## Context

Eric wants the rare item rework to stay mathematically consistent:

- All rare-eligible affix levels should be reduced by 30%.
- All rare-eligible affix level requirements should be reduced by 15%.
- Greater Affixes should be rare chase rows.
- Normal large charm `+1 skill tree` rows should be `frequency=10`.
- Greater large charm `+2 skill tree` rows should be `frequency=1`.
- If one class of charm affixes is reweighted, all charm affixes need proportional scaling so old ratios are preserved.

The canonical design is in:

```text
docs/rare-item-rework-design-2026-05-18.md
```

## Current Phase 1 Rules

Level compression:

```text
compressed_level = max(1, round(original_level * 0.70))
```

Max-level compression:

```text
compressed_maxlevel = max(compressed_level, round(original_maxlevel * 0.70))
```

Equip requirement compression:

```text
compressed_levelreq = max(1, round(original_levelreq * 0.85))
```

Blank or zero `levelreq` remains blank or zero.

## Current Large Charm Skill Rows

From `data/global/excel/magicprefix.txt`:

| Row Type | Item Type | Current Level | Current Level Req | Current Freq | Current Count |
|---|---|---:|---:|---:|---:|
| Original class `+1 skill tree` rows | `lcha` | 50 | 42 | 2 | 21 |
| Warlock `+1 skill tree` rows | `lcha` | 50 | 42 | 1 | 3 |

The 21 original class rows cover skilltab params `0` through `20`.

The 3 Warlock rows cover skilltab params `21` through `23`.

Current total normal large charm `+1 skill tree` frequency:

```text
(21 * 2) + (3 * 1) = 45
```

## Proposed Large Charm Skill Rows

The proposal intentionally normalizes all normal `+1 skill tree` large charm rows to the same rarity:

| Row Type | Item Type | Phase 1 Level | Phase 1 Level Req | Proposed Freq | Proposed Count |
|---|---|---:|---:|---:|---:|
| Original class `+1 skill tree` rows | `lcha` | 35 | 36 | 10 | 21 |
| Warlock `+1 skill tree` rows | `lcha` | 35 | 36 | 10 | 3 |
| New Greater `+2 skill tree` rows | `lcha` | 57 | 64 | 1 | 24 |

Level and requirement math:

```text
round(50 * 0.70) = 35
round(42 * 0.85) = 36
round(81 * 0.70) = 57
round(75 * 0.85) = 64
```

Proposed total normal large charm `+1 skill tree` frequency:

```text
24 * 10 = 240
```

Proposed Greater large charm `+2 skill tree` frequency:

```text
24 * 1 = 24
```

Inside the skill-tree charm slice, a specific Greater skill-tree row is intended to be exactly 10x rarer than the corresponding normal skill-tree row:

```text
normal skill tree row freq = 10
greater skill tree row freq = 1
```

## Proposed Existing Charm Frequency Scaling

Base scaling rule for existing charm rows:

```text
scaled_charm_frequency = current_frequency * 5
```

Reasoning:

- Existing original class `+1 skill tree` large charm rows are `frequency=2`.
- Target normal `+1 skill tree` charm frequency is `10`.
- Therefore the proportional multiplier is `10 / 2 = 5`.

Representative conversions:

| Current Freq | Scaled Existing Freq |
|---:|---:|
| 1 | 5 |
| 2 | 10 |
| 3 | 15 |
| 4 | 20 |
| 6 | 30 |
| 12 | 60 |
| 24 | 120 |

## Warlock Exception

Warlock `+1 skill tree` large charm rows currently have `frequency=1`.

Pure proportional scaling would make them:

```text
1 * 5 = 5
```

The proposal instead sets them to `10`, matching the original class skill-tree rows.

Claude should review whether this is acceptable. It changes the current Warlock-vs-original-class ratio, but makes all normal large charm skill trees consistent with Eric's direct statement that `+skills rarity = 10`.

## Level 90 Large Charm Prefix Pool Audit

Using rare-eligible `lcha` prefix rows at item level 90:

```text
eligible rows = 65
current total frequency = 279
current normal skill-tree frequency = 45
current normal skill-tree share = 45 / 279 = 16.1290322581%
```

After scaling existing rows and adding one Greater row per skill tree:

```text
existing scaled total = 1410
normal skill-tree frequency = 240
greater skill-tree frequency = 24
final total with greater = 1410 + 24 = 1434
normal skill-tree share = 240 / 1434 = 16.7364016736%
greater skill-tree share = 24 / 1434 = 1.6736401674%
```

The normal skill share changes slightly because Warlock rows are normalized from effective `5` to `10` and because new Greater rows are added to the pool.

If Warlock rows were strictly scaled to `5` instead of normalized to `10`, the math would be:

```text
existing scaled total = 1395
normal skill-tree frequency = 225
greater skill-tree frequency = 24
final total with greater = 1419
normal skill-tree share = 225 / 1419 = 15.8562367865%
greater skill-tree share = 24 / 1419 = 1.6913319239%
```

Claude should confirm which version better matches Eric's intent.

## Level 90 Large Charm Suffix Pool Audit

Using rare-eligible `lcha` suffix rows at item level 90:

```text
eligible rows = 15
current total frequency = 88
current skill-tree frequency = 0
scaled total = 440
```

The current proposal scales suffix charm rows by the same `*5` multiplier to keep prefix and suffix charm affix pools internally consistent.

## Level 92 Pierce Rows Caveat

At item level 92, small/medium/large charm rare-only pierce rows in group `307` become eligible.

Question for Claude:

- Should these group `307` rare-only pierce charm rows also use `*5` under the general charm scaling rule?
- Or should they be excluded because they are special-purpose rare-only chase rows and not part of the old general charm-affix balance?

## Requested Claude Verdict

Please review the math and design implications before implementation.

The highest-risk issue is whether scaling every existing charm frequency by `5` really preserves the intended affix odds once D2R separately selects prefix/suffix counts and groups. If the simplified pool-weight math is incomplete, please explain the missing mechanic and recommend a safer formula.
