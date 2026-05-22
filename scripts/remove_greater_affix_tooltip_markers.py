"""Remove generic Greater Affix tooltip marker properties from active affixes.

The old marker approach stored a separate `ga_marker_*` itemstat on rolled items.
That is unsafe because saved items persist itemstatcost numeric IDs, so later ID
reuse can render unrelated saved stats as fake "Greater Affix" labels.

This cleanup keeps the real Greater Affix gameplay stats, keeps the existing
Greater Godly colored real stats, removes generic marker properties from active
prefix/suffix rows, and fills missing affix-name strings.
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXCEL = ROOT / "data" / "global" / "excel"
BASE = EXCEL / "base"

PREFIX = EXCEL / "magicprefix.txt"
SUFFIX = EXCEL / "magicsuffix.txt"
PROPERTIES = EXCEL / "properties.txt"
NAME_STRINGS = ROOT / "data" / "local" / "lng" / "strings" / "item-nameaffixes.json"

LOCALES = [
    "enUS",
    "zhTW",
    "deDE",
    "esES",
    "frFR",
    "itIT",
    "koKR",
    "plPL",
    "esMX",
    "jaJP",
    "ptBR",
    "ruRU",
    "zhCN",
]

MOD_SLOTS = ("mod1", "mod2", "mod3")

HYBRID_REPLACEMENTS = {
    "ga_h_wraithly_weapon_dmg": "dmg%",
    "ga_h_wraithly_armor_ac": "ac%",
    "ga_h_elements_res_cold_lvl": "res-cold/lvl",
}


def read_tsv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    header = lines[0].split("\t")
    rows: list[dict[str, str]] = []
    for line in lines[1:]:
        parts = line.split("\t")
        if len(parts) < len(header):
            parts += [""] * (len(header) - len(parts))
        if len(parts) != len(header):
            raise ValueError(f"{path}: row width {len(parts)} != {len(header)}")
        rows.append(dict(zip(header, parts)))
    return header, rows


def write_tsv(path: Path, header: list[str], rows: list[dict[str, str]]) -> None:
    out = ["\t".join(header)]
    for row in rows:
        out.append("\t".join(row.get(col, "") for col in header))
    path.write_text("\n".join(out) + "\n", encoding="utf-8")


def mod_list(row: dict[str, str]) -> list[tuple[str, str, str, str]]:
    mods = []
    for slot in MOD_SLOTS:
        code = row.get(f"{slot}code", "")
        if code:
            mods.append(
                (
                    code,
                    row.get(f"{slot}param", ""),
                    row.get(f"{slot}min", ""),
                    row.get(f"{slot}max", ""),
                )
            )
    return mods


def set_mods(row: dict[str, str], mods: list[tuple[str, str, str, str]]) -> None:
    if len(mods) > 3:
        raise ValueError(f"Too many mods for {row.get('name', '<unnamed>')}: {mods}")
    for slot in MOD_SLOTS:
        for suffix in ("code", "param", "min", "max"):
            row[f"{slot}{suffix}"] = ""
    for index, (code, param, min_value, max_value) in enumerate(mods, 1):
        row[f"mod{index}code"] = code
        row[f"mod{index}param"] = param
        row[f"mod{index}min"] = min_value
        row[f"mod{index}max"] = max_value


def marker_property_codes(properties: list[dict[str, str]]) -> set[str]:
    markers = set()
    for row in properties:
        stats = [row.get(f"stat{idx}", "") for idx in range(1, 8)]
        if any(stat.startswith("ga_marker_") for stat in stats):
            markers.add(row["code"])
    return markers


def remove_marker_mods(
    rows: list[dict[str, str]],
    marker_codes: set[str],
) -> tuple[int, int]:
    removed = 0
    replaced = 0
    for row in rows:
        new_mods = []
        changed = False
        for code, param, min_value, max_value in mod_list(row):
            replacement = HYBRID_REPLACEMENTS.get(code)
            if replacement:
                new_mods.append((replacement, param, min_value, max_value))
                replaced += 1
                changed = True
                continue
            if code in marker_codes:
                removed += 1
                changed = True
                continue
            new_mods.append((code, param, min_value, max_value))
        if changed:
            set_mods(row, new_mods)
    return removed, replaced


def strip_marker_properties(
    rows: list[dict[str, str]],
    marker_codes: set[str],
) -> list[dict[str, str]]:
    stripped = [
        row
        for row in rows
        if row["code"] not in marker_codes and row["code"] not in HYBRID_REPLACEMENTS
    ]
    for index, row in enumerate(stripped):
        row["*Id"] = str(index)
    return stripped


def greater_affix_names(rows: list[dict[str, str]]) -> set[str]:
    names = set()
    for row in rows:
        if "Greater" in row.get("name", "") or "Greater" in row.get("* Description", ""):
            names.add(row["name"])
    return names


def add_missing_name_strings(names: set[str]) -> int:
    data = json.loads(NAME_STRINGS.read_text(encoding="utf-8"))
    existing = {entry["Key"] for entry in data}
    next_id = max(int(entry.get("id", 0)) for entry in data) + 1
    added = 0
    for name in sorted(names):
        if name in existing:
            continue
        entry = {"id": next_id, "Key": name}
        for locale in LOCALES:
            entry[locale] = name
        data.append(entry)
        existing.add(name)
        next_id += 1
        added += 1
    NAME_STRINGS.write_text(json.dumps(data, ensure_ascii=False, indent=4) + "\n", encoding="utf-8")
    return added


def main() -> None:
    prefix_header, prefix_rows = read_tsv(PREFIX)
    suffix_header, suffix_rows = read_tsv(SUFFIX)
    prop_header, prop_rows = read_tsv(PROPERTIES)

    markers = marker_property_codes(prop_rows)
    removed_prefix, replaced_prefix = remove_marker_mods(prefix_rows, markers)
    removed_suffix, replaced_suffix = remove_marker_mods(suffix_rows, markers)
    prop_rows = strip_marker_properties(prop_rows, markers)

    greater_names = greater_affix_names(prefix_rows) | greater_affix_names(suffix_rows)
    added_strings = add_missing_name_strings(greater_names)

    write_tsv(PREFIX, prefix_header, prefix_rows)
    write_tsv(SUFFIX, suffix_header, suffix_rows)
    write_tsv(PROPERTIES, prop_header, prop_rows)

    for path in (PREFIX, SUFFIX, PROPERTIES):
        shutil.copy2(path, BASE / path.name)

    print(f"removed marker mods: prefix={removed_prefix}, suffix={removed_suffix}")
    print(f"replaced hybrid mods: prefix={replaced_prefix}, suffix={replaced_suffix}")
    print(f"removed marker properties: {len(markers)}")
    print(f"added affix name strings: {added_strings}")


if __name__ == "__main__":
    main()
