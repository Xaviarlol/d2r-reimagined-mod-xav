"""Audit current Greater Affix rows and generate chance tables.

The chance model is intentionally simple and explicit:
- affix level is fixed at 90 for the published chance columns;
- chance is per eligible prefix/suffix selection roll, not per full rare item;
- item scopes are resolved through itemtypes.txt ancestry and actual base-item
  type codes from weapons/armor/misc.

This is meant to catch data oversights and produce a readable table for design
review. It is not a full drop simulator.
"""

from __future__ import annotations

import csv
import json
import math
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXCEL = ROOT / "data" / "global" / "excel"
DOCS = ROOT / "docs"

ALVL = 90
OUT_TABLE = DOCS / "greater-affix-final-table-2026-05-22.tsv"
OUT_REPORT = DOCS / "greater-affix-quality-pass-2026-05-22.md"

MOD_SLOTS = ("mod1", "mod2", "mod3")
BASE_ITEM_FILES = ("weapons.txt", "armor.txt", "misc.txt")
LOCALES_FILE = ROOT / "data" / "local" / "lng" / "strings" / "item-nameaffixes.json"


@dataclass(frozen=True)
class Mod:
    code: str
    param: str
    min: str
    max: str


@dataclass
class Variant:
    side: str
    name: str
    description: str
    group: str
    levelreq: str
    classspecific: str
    class_: str
    classlevelreq: str
    transformcolor: str
    itypes: tuple[str, ...]
    etypes: tuple[str, ...]
    mods: tuple[Mod, ...]
    rows: list[dict[str, str]]


def read_tsv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    header = lines[0].split("\t")
    rows = []
    for line_no, line in enumerate(lines[1:], start=2):
        parts = line.split("\t")
        if len(parts) < len(header):
            parts += [""] * (len(header) - len(parts))
        if len(parts) != len(header):
            raise ValueError(f"{path}:{line_no}: {len(parts)} columns, expected {len(header)}")
        row = dict(zip(header, parts))
        row["_line"] = str(line_no)
        rows.append(row)
    return header, rows


def mod_list(row: dict[str, str]) -> tuple[Mod, ...]:
    mods = []
    for slot in MOD_SLOTS:
        code = row.get(f"{slot}code", "")
        if code:
            mods.append(
                Mod(
                    code,
                    row.get(f"{slot}param", ""),
                    row.get(f"{slot}min", ""),
                    row.get(f"{slot}max", ""),
                )
            )
    return tuple(mods)


def type_list(row: dict[str, str], prefix: str, count: int) -> tuple[str, ...]:
    return tuple(row.get(f"{prefix}{idx}", "") for idx in range(1, count + 1) if row.get(f"{prefix}{idx}", ""))


def is_greater_row(row: dict[str, str]) -> bool:
    if "Greater" in row.get("name", ""):
        return True
    if "Greater" in row.get("* Description", ""):
        return True
    return False


def row_eligible(row: dict[str, str], alvl: int) -> bool:
    if row.get("spawnable") != "1" or row.get("rare") != "1":
        return False
    level = int(row.get("level") or 0)
    maxlevel = int(row["maxlevel"]) if row.get("maxlevel") else None
    return level <= alvl and (maxlevel is None or alvl <= maxlevel)


def itemtype_maps() -> tuple[dict[str, dict[str, str]], dict[str, set[str]]]:
    _, rows = read_tsv(EXCEL / "itemtypes.txt")
    by_code = {row["Code"]: row for row in rows if row.get("Code")}

    def ancestors(code: str, seen: set[str] | None = None) -> set[str]:
        seen = set() if seen is None else seen
        if not code or code in seen:
            return seen
        seen.add(code)
        row = by_code.get(code)
        if row:
            ancestors(row.get("Equiv1", ""), seen)
            ancestors(row.get("Equiv2", ""), seen)
        return seen

    return by_code, {code: ancestors(code) for code in by_code}


def base_item_types(type_rows: dict[str, dict[str, str]]) -> set[str]:
    codes: set[str] = set()
    for file_name in BASE_ITEM_FILES:
        _, rows = read_tsv(EXCEL / file_name)
        for row in rows:
            if row.get("spawnable") != "1":
                continue
            for col in ("type", "type2"):
                code = row.get(col, "")
                if code and type_rows.get(code, {}).get("Rare") == "1":
                    codes.add(code)
    return codes


def item_matches(row: dict[str, str], sample_type: str, ancestors: dict[str, set[str]]) -> bool:
    lineage = ancestors.get(sample_type, {sample_type})
    include = type_list(row, "itype", 7)
    exclude = type_list(row, "etype", 5)
    if include and not any(code in lineage for code in include):
        return False
    if exclude and any(code in lineage for code in exclude):
        return False
    return True


def pool(rows: list[dict[str, str]], sample_type: str, ancestors: dict[str, set[str]], alvl: int) -> list[dict[str, str]]:
    return [row for row in rows if row_eligible(row, alvl) and item_matches(row, sample_type, ancestors)]


def format_mod(mod: Mod) -> str:
    bits = [mod.code]
    if mod.param:
        bits.append(f"param={mod.param}")
    if mod.min or mod.max:
        bits.append(f"{mod.min or ''}-{mod.max or ''}")
    return " ".join(bits)


def stats_text(mods: tuple[Mod, ...]) -> str:
    return "; ".join(format_mod(mod) for mod in mods)


def band_name(row: dict[str, str]) -> str:
    level = row.get("level", "")
    maxlevel = row.get("maxlevel", "")
    if level == "50" and maxlevel == "65":
        return "early"
    if level == "66" and maxlevel == "80":
        return "mid"
    if level == "81" and maxlevel == "":
        return "late"
    return f"L{level}-{maxlevel or '+'}"


def band_summary(rows: list[dict[str, str]]) -> str:
    ordered = sorted(rows, key=lambda r: int(r.get("level") or 0))
    return "; ".join(
        f"{band_name(row)} L{row.get('level')}-{row.get('maxlevel') or '+'} freq {row.get('frequency')} line {row.get('_line')}"
        for row in ordered
    )


def group_variants(side: str, rows: list[dict[str, str]]) -> list[Variant]:
    buckets: dict[tuple[object, ...], list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        if not is_greater_row(row):
            continue
        key = (
            row["name"],
            row["group"],
            row.get("levelreq", ""),
            row.get("classspecific", ""),
            row.get("class", ""),
            row.get("classlevelreq", ""),
            row.get("transformcolor", ""),
            type_list(row, "itype", 7),
            type_list(row, "etype", 5),
            mod_list(row),
        )
        buckets[key].append(row)

    variants = []
    for key, bucket in buckets.items():
        first = bucket[0]
        variants.append(
            Variant(
                side=side,
                name=first["name"],
                description=first.get("* Description", ""),
                group=first.get("group", ""),
                levelreq=first.get("levelreq", ""),
                classspecific=first.get("classspecific", ""),
                class_=first.get("class", ""),
                classlevelreq=first.get("classlevelreq", ""),
                transformcolor=first.get("transformcolor", ""),
                itypes=type_list(first, "itype", 7),
                etypes=type_list(first, "etype", 5),
                mods=mod_list(first),
                rows=sorted(bucket, key=lambda r: int(r.get("level") or 0)),
            )
        )
    return sorted(variants, key=lambda v: (v.side, v.name, v.group, v.itypes, stats_text(v.mods)))


def active_frequency(rows: list[dict[str, str]], alvl: int) -> int:
    return sum(int(row.get("frequency") or 0) for row in rows if row_eligible(row, alvl))


def chance_stats(
    variant: Variant,
    all_rows: list[dict[str, str]],
    sample_types: set[str],
    ancestors: dict[str, set[str]],
) -> dict[str, object]:
    eligible_samples = [sample for sample in sorted(sample_types) if any(item_matches(row, sample, ancestors) for row in variant.rows)]
    chances = []
    for sample in eligible_samples:
        selected_rows = [row for row in variant.rows if row_eligible(row, ALVL) and item_matches(row, sample, ancestors)]
        freq = sum(int(row.get("frequency") or 0) for row in selected_rows)
        if freq <= 0:
            continue
        total = sum(int(row.get("frequency") or 0) for row in pool(all_rows, sample, ancestors, ALVL))
        if total <= 0:
            continue
        pct = 100.0 * freq / total
        chances.append((pct, sample, freq, total))

    if not chances:
        return {
            "eligible_samples": "",
            "sample_count": 0,
            "freq_at_alvl90_min": "",
            "freq_at_alvl90_max": "",
            "pool_at_alvl90_min": "",
            "pool_at_alvl90_max": "",
            "chance_min": "",
            "chance_avg": "",
            "chance_max": "",
            "best_samples": "",
            "approx_three_roll_max": "",
        }

    chances.sort()
    chance_values = [chance for chance, _, _, _ in chances]
    max_chance = chances[-1][0]
    best_samples = [sample for chance, sample, _, _ in chances if math.isclose(chance, max_chance, rel_tol=0, abs_tol=1e-12)]
    return {
        "eligible_samples": ",".join(sample for _, sample, _, _ in chances),
        "sample_count": len(chances),
        "freq_at_alvl90_min": min(freq for _, _, freq, _ in chances),
        "freq_at_alvl90_max": max(freq for _, _, freq, _ in chances),
        "pool_at_alvl90_min": min(total for _, _, _, total in chances),
        "pool_at_alvl90_max": max(total for _, _, _, total in chances),
        "chance_min": min(chance_values),
        "chance_avg": sum(chance_values) / len(chance_values),
        "chance_max": max_chance,
        "best_samples": ",".join(best_samples[:10]),
        "approx_three_roll_max": 100.0 * (1.0 - (1.0 - max_chance / 100.0) ** 3),
    }


def missing_name_strings(variants: list[Variant]) -> list[str]:
    data = json.loads(LOCALES_FILE.read_text(encoding="utf-8"))
    keys = {entry["Key"] for entry in data}
    return sorted({variant.name for variant in variants if variant.name not in keys})


def overlap_issues(variants: list[Variant], sample_types: set[str], ancestors: dict[str, set[str]]) -> list[str]:
    issues = []
    for i, left in enumerate(variants):
        for right in variants[i + 1 :]:
            if left.side != right.side or left.group != right.group:
                continue
            left_samples = {
                sample
                for sample in sample_types
                if any(row_eligible(row, ALVL) and item_matches(row, sample, ancestors) for row in left.rows)
            }
            right_samples = {
                sample
                for sample in sample_types
                if any(row_eligible(row, ALVL) and item_matches(row, sample, ancestors) for row in right.rows)
            }
            shared = sorted(left_samples & right_samples)
            if not shared:
                continue
            same_payload = left.name == right.name and left.mods == right.mods
            if same_payload:
                issues.append(
                    f"{left.side} group {left.group}: duplicate Greater payload `{left.name}` overlaps item types "
                    f"{', '.join(shared[:12])}; scopes `{','.join(left.itypes)}` and `{','.join(right.itypes)}` both apply."
                )
    return issues


def quality_report(
    variants: list[Variant],
    prefix_rows: list[dict[str, str]],
    suffix_rows: list[dict[str, str]],
    prop_rows: list[dict[str, str]],
    table_rows: list[dict[str, object]],
    sample_types: set[str],
    ancestors: dict[str, set[str]],
) -> str:
    prop_codes = {row["code"] for row in prop_rows}
    missing_props = []
    marker_refs = []
    stale_marker_descriptions = []
    bad_bands = []
    bad_spawn = []

    for side, rows in (("prefix", prefix_rows), ("suffix", suffix_rows)):
        for row in rows:
            if not is_greater_row(row):
                continue
            if row.get("spawnable") != "1" or row.get("rare") != "1":
                bad_spawn.append(f"{side}:{row['_line']} {row['name']} spawnable={row.get('spawnable')} rare={row.get('rare')}")
            if "marker=ga_" in row.get("* Description", ""):
                stale_marker_descriptions.append(f"{side}:{row['_line']} {row['name']}")
            for mod in mod_list(row):
                if mod.code not in prop_codes:
                    missing_props.append(f"{side}:{row['_line']} {row['name']} -> {mod.code}")
                if mod.code.startswith("ga_h_") or (mod.code.startswith("ga_") and mod.code not in {"ga_godly_ac%", "ga_godly_red-dmg%"}):
                    marker_refs.append(f"{side}:{row['_line']} {row['name']} -> {mod.code}")

    for variant in variants:
        bands = {(row.get("level"), row.get("maxlevel")) for row in variant.rows}
        expected = {("50", "65"), ("66", "80"), ("81", "")}
        if bands != expected:
            bad_bands.append(f"{variant.side} {variant.name} group {variant.group} `{stats_text(variant.mods)}` bands={sorted(bands)}")

    high_chance = [
        row
        for row in table_rows
        if row["chance_max_pct_per_affix_roll_alvl90"] != ""
        and float(row["chance_max_pct_per_affix_roll_alvl90"]) >= 1.0
    ]
    high_chance = sorted(high_chance, key=lambda row: float(row["chance_max_pct_per_affix_roll_alvl90"]), reverse=True)
    high_three_roll = [
        row
        for row in table_rows
        if row["approx_three_roll_max_pct"] != ""
        and float(row["approx_three_roll_max_pct"]) >= 1.0
    ]
    high_three_roll = sorted(high_three_roll, key=lambda row: float(row["approx_three_roll_max_pct"]), reverse=True)

    overlaps = overlap_issues(variants, sample_types, ancestors)
    missing_strings = missing_name_strings(variants)

    lines = [
        "# Greater Affix Quality Pass",
        "",
        f"Generated from current live data files at affix level {ALVL}.",
        "",
        "## Summary",
        "",
        f"- Greater variants audited: {len(variants)}",
        f"- Greater row count: {sum(len(variant.rows) for variant in variants)}",
        f"- Missing Greater affix name strings: {len(missing_strings)}",
        f"- Missing property references in Greater rows: {len(missing_props)}",
        f"- Functional generic marker/hybrid refs in Greater rows: {len(marker_refs)}",
        f"- Greater variants missing exact early/mid/late bands: {len(bad_bands)}",
        f"- Greater rows not spawnable rare: {len(bad_spawn)}",
        f"- Duplicate same-payload overlap warnings: {len(overlaps)}",
        f"- Per-affix-roll chance outliers >= 1% at alvl {ALVL}: {len(high_chance)}",
        f"- Approx three-roll chance outliers >= 1% at alvl {ALVL}: {len(high_three_roll)}",
        "",
        "## Findings",
        "",
    ]

    if not any([missing_strings, missing_props, marker_refs, bad_bands, bad_spawn, overlaps, high_chance, stale_marker_descriptions]):
        lines.append("- No obvious oversights found by the automated checks.")
    if missing_strings:
        lines.append("- Missing name strings:")
        lines.extend(f"  - {item}" for item in missing_strings)
    if missing_props:
        lines.append("- Missing property references:")
        lines.extend(f"  - {item}" for item in missing_props[:50])
    if marker_refs:
        lines.append("- Functional marker/hybrid references still present:")
        lines.extend(f"  - {item}" for item in marker_refs[:50])
    if bad_bands:
        lines.append("- Band issues:")
        lines.extend(f"  - {item}" for item in bad_bands[:50])
    if bad_spawn:
        lines.append("- Spawnability issues:")
        lines.extend(f"  - {item}" for item in bad_spawn[:50])
    if overlaps:
        lines.append("- Duplicate same-payload overlap warnings:")
        lines.extend(f"  - {item}" for item in overlaps[:50])
    if high_chance:
        lines.append("- High per-roll chance outliers:")
        for row in high_chance[:25]:
            lines.append(
                f"  - {row['side']} `{row['affix_name']}` group {row['group']} "
                f"max {row['chance_max_pct_per_affix_roll_alvl90']}% on `{row['best_item_type_samples']}` "
                f"stats `{row['stats']}`"
            )
    if high_three_roll:
        lines.append("- High approximate three-roll chance outliers:")
        for row in high_three_roll[:25]:
            lines.append(
                f"  - {row['side']} `{row['affix_name']}` group {row['group']} "
                f"approx {row['approx_three_roll_max_pct']}% if the rare gets three same-side rolls; "
                f"single-roll max {row['chance_max_pct_per_affix_roll_alvl90']}% on `{row['best_item_type_samples']}` "
                f"stats `{row['stats']}`"
            )
    if stale_marker_descriptions:
        lines.append("- Cosmetic stale description labels still mention `marker=ga_`:")
        lines.append(f"  - {len(stale_marker_descriptions)} rows affected. This is internal/comment text, not a functional mod.")

    lines += [
        "",
        "## Chance Model",
        "",
        "- The table reports chance per eligible prefix/suffix selection roll, not full item drop odds.",
        "- Full rare-item chance is lower or higher depending on how many affixes and how many prefix/suffix slots the rare receives.",
        "- `approx_three_roll_max_pct` is the upper-bound style estimate if a rare receives three same-side rolls for the item type with the highest observed per-roll chance.",
        f"- Chance pool is evaluated at affix level {ALVL}; early and mid bands are shown for frequency documentation but are not active at alvl 90.",
        "",
        f"Detailed table: `{OUT_TABLE.name}`",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    _, prefix_rows = read_tsv(EXCEL / "magicprefix.txt")
    _, suffix_rows = read_tsv(EXCEL / "magicsuffix.txt")
    _, prop_rows = read_tsv(EXCEL / "properties.txt")
    type_rows, ancestors = itemtype_maps()
    sample_types = base_item_types(type_rows)

    variants = group_variants("prefix", prefix_rows) + group_variants("suffix", suffix_rows)
    all_side_rows = {"prefix": prefix_rows, "suffix": suffix_rows}

    output_rows: list[dict[str, object]] = []
    for idx, variant in enumerate(variants, start=1):
        chance = chance_stats(variant, all_side_rows[variant.side], sample_types, ancestors)
        row = {
            "id": f"GA{idx:03d}",
            "side": variant.side,
            "affix_name": variant.name,
            "group": variant.group,
            "levelreq": variant.levelreq,
            "bands_and_frequency": band_summary(variant.rows),
            "active_frequency_at_alvl90_min": chance["freq_at_alvl90_min"],
            "active_frequency_at_alvl90_max": chance["freq_at_alvl90_max"],
            "stats": stats_text(variant.mods),
            "transformcolor": variant.transformcolor,
            "itypes": ",".join(variant.itypes),
            "etypes": ",".join(variant.etypes),
            "eligible_item_type_count": chance["sample_count"],
            "eligible_item_types": chance["eligible_samples"],
            "eligible_pool_frequency_min": chance["pool_at_alvl90_min"],
            "eligible_pool_frequency_max": chance["pool_at_alvl90_max"],
            "chance_min_pct_per_affix_roll_alvl90": f"{chance['chance_min']:.6f}" if chance["chance_min"] != "" else "",
            "chance_avg_pct_per_affix_roll_alvl90": f"{chance['chance_avg']:.6f}" if chance["chance_avg"] != "" else "",
            "chance_max_pct_per_affix_roll_alvl90": f"{chance['chance_max']:.6f}" if chance["chance_max"] != "" else "",
            "approx_three_roll_max_pct": f"{chance['approx_three_roll_max']:.6f}" if chance["approx_three_roll_max"] != "" else "",
            "best_item_type_samples": chance["best_samples"],
            "source_lines": ",".join(row["_line"] for row in variant.rows),
        }
        output_rows.append(row)

    with OUT_TABLE.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(output_rows[0]), dialect="excel-tab")
        writer.writeheader()
        writer.writerows(output_rows)

    OUT_REPORT.write_text(
        quality_report(variants, prefix_rows, suffix_rows, prop_rows, output_rows, sample_types, ancestors),
        encoding="utf-8",
    )
    print(f"Wrote {OUT_TABLE}")
    print(f"Wrote {OUT_REPORT}")


if __name__ == "__main__":
    main()
