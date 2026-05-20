#!/usr/bin/env python3
"""Apply the two-phase rare affix rework to magicprefix/magicsuffix tables."""

from __future__ import annotations

import csv
import math
import shutil
from collections import OrderedDict
from copy import deepcopy
from pathlib import Path

import audit_rare_affix_apexes as audit

ROOT = Path(__file__).resolve().parents[1]
EXCEL = ROOT / "data" / "global" / "excel"
REPORT = ROOT / "docs" / "rare-affix-implementation-summary-2026-05-20.tsv"
FREQ_SCALE = 10
GREATER_BANDS = (
    ("early", 50, 65, 1 / 3),
    ("mid", 66, 80, 2 / 3),
    ("late", 81, None, 1.0),
)
CLASS_SKILL_CODES = {"ama", "pal", "nec", "sor", "bar", "dru", "ass", "war"}


def round_half_up(value: float) -> int:
    return math.floor(value + 0.5)


def parse_int(value: str) -> int | None:
    value = (value or "").strip()
    if not value:
        return None
    try:
        return int(value)
    except ValueError:
        return None


def compressed_level(value: str) -> str:
    original = parse_int(value)
    if original is None:
        return value
    return str(max(1, round_half_up(original * 0.70)))


def compressed_levelreq(value: str) -> str:
    original = parse_int(value)
    if original is None:
        return value
    if original == 0:
        return "0"
    return str(max(1, round_half_up(original * 0.85)))


def scaled_frequency(value: str) -> str:
    original = parse_int(value)
    if original is None:
        return value
    return str(original * FREQ_SCALE)


def half_frequency(value: str) -> str:
    original = parse_int(value)
    if original is None:
        return value
    return str(max(1, round_half_up(original / 2)))


def band_frequency(value: str, multiplier: float) -> str:
    original = parse_int(value)
    if original is None:
        return value
    return str(max(1, round_half_up(original * multiplier)))


def read_table(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f, delimiter="\t")
        return list(reader.fieldnames or []), list(reader)


def write_table(path: Path, headers: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers, delimiter="\t", extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def mod_codes(row: dict[str, str]) -> list[str]:
    return [row.get(f"mod{idx}code", "") for idx in range(1, 4)]


def set_mod(row: dict[str, str], idx: int, code: str, param: str = "", mn: str = "", mx: str = "") -> None:
    row[f"mod{idx}code"] = code
    row[f"mod{idx}param"] = param
    row[f"mod{idx}min"] = mn
    row[f"mod{idx}max"] = mx


def set_all_matching(row: dict[str, str], codes: set[str], mn: int | str, mx: int | str, param: str | None = None) -> None:
    for idx in range(1, 4):
        if row.get(f"mod{idx}code", "") in codes:
            if param is not None:
                row[f"mod{idx}param"] = param
            row[f"mod{idx}min"] = str(mn)
            row[f"mod{idx}max"] = str(mx)


def set_prefix_matching(row: dict[str, str], prefixes: tuple[str, ...], mn: int | str, mx: int | str) -> None:
    for idx in range(1, 4):
        if row.get(f"mod{idx}code", "").startswith(prefixes):
            row[f"mod{idx}min"] = str(mn)
            row[f"mod{idx}max"] = str(mx)


def first_empty_mod_slot(row: dict[str, str]) -> int | None:
    for idx in range(1, 4):
        if not row.get(f"mod{idx}code", ""):
            return idx
    return None


def ensure_mod(row: dict[str, str], code: str, param: str = "", mn: str = "", mx: str = "") -> None:
    for idx in range(1, 4):
        if row.get(f"mod{idx}code", "") == code:
            row[f"mod{idx}param"] = param
            row[f"mod{idx}min"] = mn
            row[f"mod{idx}max"] = mx
            return
    slot = first_empty_mod_slot(row)
    if slot is not None:
        set_mod(row, slot, code, param, mn, mx)


def add_marker(row: dict[str, str]) -> bool:
    if "greater-affix-marker" in mod_codes(row):
        return True
    slot = first_empty_mod_slot(row)
    if slot is None:
        return False
    set_mod(row, slot, "greater-affix-marker", "", "1", "1")
    return True


def boost_numeric(value: str, factor: float = 1.30) -> str:
    original = parse_int(value)
    if original is None:
        return value
    if original <= 0:
        return str(original)
    return str(max(original + 1, round_half_up(original * factor)))


def generic_boost(row: dict[str, str]) -> None:
    for idx in range(1, 4):
        code = row.get(f"mod{idx}code", "")
        if not code or code in {"ethereal", "greater-affix-marker"}:
            continue
        if code in {"aura", "skill-rand"}:
            param = parse_int(row.get(f"mod{idx}param", ""))
            if param is not None:
                row[f"mod{idx}param"] = str(param + 1)
            row[f"mod{idx}min"] = boost_numeric(row.get(f"mod{idx}min", ""), 1.15)
            row[f"mod{idx}max"] = boost_numeric(row.get(f"mod{idx}max", ""), 1.15)
            continue
        if code.endswith("/lvl") and parse_int(row.get(f"mod{idx}param", "")) is not None:
            row[f"mod{idx}param"] = boost_numeric(row.get(f"mod{idx}param", ""), 1.30)
            continue
        row[f"mod{idx}min"] = boost_numeric(row.get(f"mod{idx}min", ""))
        row[f"mod{idx}max"] = boost_numeric(row.get(f"mod{idx}max", ""))


def greater_suffix_name(name: str) -> str:
    if name.startswith("of the "):
        return "of the Greater " + name[len("of the ") :]
    if name.startswith("of "):
        return "of Greater " + name[len("of ") :]
    return "Greater " + name


def greater_name(source: dict[str, str], candidate: dict[str, object]) -> str:
    cid = str(candidate["id"])
    if cid in {"greater-grandmasters", "greater-godly"}:
        return str(candidate["name"])
    if source.get("side") == "suffix":
        return greater_suffix_name(source.get("name", ""))
    name = source.get("name", "")
    if name.endswith("1") or name.endswith("2"):
        name = name[:-1]
    return "Greater " + name


def transform_greater_mods(row: dict[str, str], candidate_id: str) -> None:
    generic_boost(row)

    if candidate_id == "greater-grandmasters":
        set_all_matching(row, {"dmg%"}, 451, 500)
        set_all_matching(row, {"att"}, 301, 350)
        set_all_matching(row, {"deadly", "crush"}, 31, 40)
        set_all_matching(row, {"openwounds"}, 100, 100)
    elif candidate_id == "greater-godly":
        set_all_matching(row, {"ac%"}, 250, 300)
        ensure_mod(row, "red-dmg%", "", "26", "30")
    elif candidate_id in {"greater-antimagic-prefix", "greater-negation"}:
        set_all_matching(row, {"res-mag"}, 24, 30)
    elif candidate_id == "greater-bloody":
        set_all_matching(row, {"dmg-min"}, 9, 12)
        set_all_matching(row, {"dmg-max"}, 18, 24)
    elif candidate_id == "greater-serrated":
        set_all_matching(row, {"dmg%"}, 30, 35)
    elif candidate_id == "greater-vulpine":
        set_all_matching(row, {"dmg-to-mana"}, 16, 20)
    elif candidate_id == "greater-platinum":
        set_all_matching(row, {"att"}, 351, 450)
    elif candidate_id == "greater-lucky":
        set_all_matching(row, {"mag%"}, 30, 35)
        set_all_matching(row, {"gold%"}, 60, 70)
    elif candidate_id == "greater-serpents":
        set_all_matching(row, {"mana"}, 70, 85)
    elif candidate_id == "greater-shimmering":
        for idx in range(1, 4):
            if row.get(f"mod{idx}code") == "res-all":
                mx = parse_int(row.get(f"mod{idx}max", "")) or 0
                if mx >= 30:
                    row[f"mod{idx}min"], row[f"mod{idx}max"] = "36", "40"
                elif mx >= 17:
                    row[f"mod{idx}min"], row[f"mod{idx}max"] = "22", "25"
                else:
                    row[f"mod{idx}min"], row[f"mod{idx}max"] = "15", "18"
    elif candidate_id == "greater-single-resist-charm":
        set_all_matching(row, {"res-cold", "res-fire", "res-ltng", "res-pois"}, 34, 40)
    elif candidate_id == "greater-aureolin":
        set_all_matching(row, {"mana-kill"}, 4, 5)
    elif candidate_id == "greater-celestial":
        set_all_matching(row, {"att-demon"}, 451, 550)
        set_all_matching(row, {"dmg-demon"}, 351, 425)
    elif candidate_id == "greater-divine":
        set_all_matching(row, {"att-undead"}, 500, 650)
        set_all_matching(row, {"dmg-undead"}, 400, 500)
    elif candidate_id == "greater-avatar":
        set_all_matching(row, {"dmg-elem"}, 35, 45)
    elif candidate_id == "greater-weapon-elemental-prefix":
        pass
    elif candidate_id == "greater-hulking":
        set_all_matching(row, {"dmg-norm"}, 70, 85)
    elif candidate_id == "greater-veracious":
        set_all_matching(row, {"att%"}, 40, 50)
    elif candidate_id == "greater-gnostic":
        for idx in range(1, 4):
            if row.get(f"mod{idx}code") == "skill-rand":
                row[f"mod{idx}param"] = "6"
    elif candidate_id == "greater-crushing-fatal":
        set_all_matching(row, {"crush", "deadly"}, 24, 30)
    elif candidate_id == "greater-sage-xp":
        set_all_matching(row, {"addxp"}, 6, 6)
    elif candidate_id == "greater-savage":
        set_all_matching(row, {"kick"}, 11, 13)
    elif candidate_id == "greater-adamantine-wrought":
        set_all_matching(row, {"dmg%"}, 110, 130)
        set_all_matching(row, {"ac%"}, 85, 100)
        set_all_matching(row, {"dur"}, 80, 100)
    elif candidate_id == "greater-aureole":
        set_all_matching(row, {"aura"}, 2, 4)
    elif candidate_id == "greater-elemental-mastery":
        set_prefix_matching(row, ("extra-",), 14, 16)
    elif candidate_id == "greater-elemental-pierce":
        set_prefix_matching(row, ("pierce-",), 14, 16)
    elif candidate_id == "greater-anima":
        set_all_matching(row, {"red-dmg"}, 18, 24)
    elif candidate_id == "greater-coalescence":
        set_all_matching(row, {"abs-fire%", "abs-ltng%", "abs-cold%"}, 28, 35)
    elif candidate_id == "greater-quickness":
        set_all_matching(row, {"swing3"}, 50, 50)
    elif candidate_id == "greater-deflecting":
        set_all_matching(row, {"block"}, 35, 40)
        set_all_matching(row, {"block2"}, 40, 40)
    elif candidate_id == "greater-magus":
        set_all_matching(row, {"cast3"}, 25, 25)
    elif candidate_id == "greater-evisceration":
        set_all_matching(row, {"dmg-max"}, 150, 165)
    elif candidate_id == "greater-transcendence":
        set_all_matching(row, {"dmg-min"}, 75, 85)
    elif candidate_id == "greater-perfection":
        set_all_matching(row, {"dex"}, 36, 40)
    elif candidate_id == "greater-balance":
        set_all_matching(row, {"balance3"}, 13, 15)
    elif candidate_id == "greater-regeneration":
        set_all_matching(row, {"regen"}, 6, 8)
    elif candidate_id == "greater-wealth":
        set_all_matching(row, {"gold%"}, 100, 120)
    elif candidate_id == "greater-prosperity":
        set_all_matching(row, {"mag%"}, 26, 30)
    elif candidate_id == "greater-enlightenment":
        set_all_matching(row, {"enr"}, 36, 40)
    elif candidate_id == "greater-vita":
        set_all_matching(row, {"hp"}, 80, 95)
    elif candidate_id == "greater-leech":
        set_all_matching(row, {"lifesteal", "manasteal"}, 10, 12)
    elif candidate_id == "greater-titan":
        set_all_matching(row, {"str", "dex", "vit", "enr"}, 26, 30)
        set_all_matching(row, {"str%", "dex%", "vit%", "enr%"}, 34, 40)
    elif candidate_id == "greater-inertia":
        set_all_matching(row, {"move3"}, 13, 15)
    elif candidate_id == "greater-elephant":
        for idx in range(1, 4):
            if row.get(f"mod{idx}code") == "hp/lvl":
                row[f"mod{idx}param"] = "6"
            elif row.get(f"mod{idx}code") == "mana/lvl":
                row[f"mod{idx}param"] = "3"
    elif candidate_id == "greater-zodiac":
        set_all_matching(row, {"all-stats"}, 38, 45)
    elif candidate_id == "greater-lich":
        set_all_matching(row, {"manasteal"}, 10, 12)
        set_all_matching(row, {"lifesteal"}, 13, 15)
    elif candidate_id == "greater-guarding":
        set_all_matching(row, {"ac"}, 60, 90)
    elif candidate_id == "greater-paralysis":
        set_all_matching(row, {"slow"}, 28, 33)
    elif candidate_id == "greater-blindness":
        set_all_matching(row, {"stupidity"}, 4, 4)
    elif candidate_id == "greater-four-seasons":
        set_all_matching(row, {"res-all-max"}, 7, 8)
    elif candidate_id == "greater-draining":
        set_all_matching(row, {"healperhit"}, 14, 16)

    for idx in range(1, 4):
        code = row.get(f"mod{idx}code", "")
        if code == "allskills":
            current = parse_int(row.get(f"mod{idx}max", "")) or 0
            value = 3 if current >= 2 else 2
            row[f"mod{idx}min"] = str(value)
            row[f"mod{idx}max"] = str(value)
        elif code == "skilltab":
            row[f"mod{idx}min"] = "4"
            row[f"mod{idx}max"] = "4"
        elif code in CLASS_SKILL_CODES:
            row[f"mod{idx}min"] = "3"
            row[f"mod{idx}max"] = "3"


def collect_sources() -> tuple[dict[tuple[str, int], list[dict[str, object]]], dict[str, list[dict[str, object]]]]:
    affixes = audit.load_affixes()
    by_line: dict[tuple[str, int], list[dict[str, object]]] = OrderedDict()
    by_side: dict[str, list[dict[str, object]]] = {"prefix": [], "suffix": []}
    seen_greater: set[tuple[str, str, int]] = set()

    for candidate in audit.CANDIDATES:
        for item_type in sorted(audit.ITEMTYPES):
            scoped = dict(candidate)
            scoped["sample"] = item_type
            for source in audit.apex_rows_for(affixes, scoped):
                line = int(source["line"])
                side = str(candidate["side"])
                line_key = (side, line)
                by_line.setdefault(line_key, [])

                greater_key = (str(candidate["id"]), side, line)
                if greater_key in seen_greater:
                    continue
                seen_greater.add(greater_key)
                item = {
                    "candidate": candidate,
                    "side": side,
                    "line": line,
                    "source": deepcopy(source),
                }
                by_line[line_key].append(item)
                by_side[side].append(item)
    return by_line, by_side


def phase1_existing_row(row: dict[str, str], line_key: tuple[str, int], split_sources: dict[tuple[str, int], list[dict[str, object]]]) -> list[dict[str, str]]:
    if row.get("rare") != "1":
        return [deepcopy(row)]

    if line_key not in split_sources:
        out = deepcopy(row)
        out["level"] = compressed_level(row.get("level", ""))
        out["levelreq"] = compressed_levelreq(row.get("levelreq", ""))
        return [out]

    original_level = parse_int(row.get("level", ""))
    early = deepcopy(row)
    early["level"] = compressed_level(row.get("level", ""))
    early["levelreq"] = compressed_levelreq(row.get("levelreq", ""))
    early["frequency"] = half_frequency(row.get("frequency", ""))
    if original_level is not None:
        early["maxlevel"] = str(max(1, original_level - 1))

    late = deepcopy(row)
    late["levelreq"] = compressed_levelreq(row.get("levelreq", ""))
    return [early, late]


def make_greater_row(source_item: dict[str, object], band: tuple[str, int, int | None, float]) -> dict[str, str]:
    band_name, level, maxlevel, multiplier = band
    source = deepcopy(source_item["source"])
    candidate = source_item["candidate"]

    source["name"] = greater_name(source, candidate)
    source["* Description"] = f"Greater {source.get('* Description', '')}".strip()
    source["spawnable"] = "0"
    source["rare"] = "1"
    source["level"] = str(level)
    source["maxlevel"] = "" if maxlevel is None else str(maxlevel)
    source["levelreq"] = compressed_levelreq(source.get("levelreq", ""))
    source["frequency"] = band_frequency(source.get("frequency", ""), multiplier)
    source["multiply"] = source.get("multiply", "0") or "0"
    source["add"] = source.get("add", "0") or "0"
    transform_greater_mods(source, str(candidate["id"]))
    marker_added = add_marker(source)
    source["* Description"] = f"{source['* Description']} [{band_name}; marker={'yes' if marker_added else 'no'}]"
    source.pop("side", None)
    source.pop("line", None)
    return source


def apply_to_table(filename: str, side: str, split_sources: dict[tuple[str, int], list[dict[str, object]]], greater_sources: list[dict[str, object]]) -> dict[str, int]:
    path = EXCEL / filename
    headers, rows = read_table(path)
    if any(row.get("name", "").startswith("Greater ") or row.get("name", "").startswith("of Greater ") or row.get("name", "").startswith("of the Greater ") for row in rows):
        raise RuntimeError(f"{filename} already appears to contain Greater rows")

    out: list[dict[str, str]] = []
    split_count = 0
    compressed_count = 0
    for idx, row in enumerate(rows, start=2):
        line_key = (side, idx)
        transformed = phase1_existing_row(row, line_key, split_sources)
        if row.get("rare") == "1":
            compressed_count += 1
        if len(transformed) == 2:
            split_count += 1
        out.extend(transformed)

    for row in out:
        row["frequency"] = scaled_frequency(row.get("frequency", ""))

    greater_rows = []
    for item in greater_sources:
        for band in GREATER_BANDS:
            greater_rows.append(make_greater_row(item, band))
    out.extend(greater_rows)

    write_table(path, headers, out)
    base_path = EXCEL / "base" / filename
    shutil.copyfile(path, base_path)
    return {
        "original_rows": len(rows),
        "output_rows": len(out),
        "rare_rows_compressed": compressed_count,
        "source_rows_split": split_count,
        "greater_rows_added": len(greater_rows),
    }


def validate_table(filename: str) -> dict[str, int]:
    active_headers, active_rows = read_table(EXCEL / filename)
    base_headers, base_rows = read_table(EXCEL / "base" / filename)
    if active_headers != base_headers:
        raise RuntimeError(f"{filename} active/base headers differ")
    if active_rows != base_rows:
        raise RuntimeError(f"{filename} active/base rows differ")
    width_errors = 0
    missing_greater_req = 0
    missing_greater_level = 0
    missing_greater_group = 0
    for row in active_rows:
        if len(row) != len(active_headers):
            width_errors += 1
        if row.get("name", "").startswith("Greater ") or row.get("name", "").startswith("of Greater ") or row.get("name", "").startswith("of the Greater "):
            if not row.get("levelreq", ""):
                missing_greater_req += 1
            if not row.get("level", ""):
                missing_greater_level += 1
            if not row.get("group", ""):
                missing_greater_group += 1
    return {
        "active_rows": len(active_rows),
        "base_rows": len(base_rows),
        "columns": len(active_headers),
        "width_errors": width_errors,
        "missing_greater_level": missing_greater_level,
        "missing_greater_levelreq": missing_greater_req,
        "missing_greater_group": missing_greater_group,
    }


def write_report(results: list[dict[str, str | int]]) -> None:
    headers = [
        "file",
        "original_rows",
        "output_rows",
        "rare_rows_compressed",
        "source_rows_split",
        "greater_rows_added",
        "active_rows",
        "base_rows",
        "columns",
        "width_errors",
        "missing_greater_level",
        "missing_greater_levelreq",
        "missing_greater_group",
    ]
    with REPORT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers, delimiter="\t", extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        writer.writerows(results)


def main() -> None:
    split_sources, greater_by_side = collect_sources()
    results: list[dict[str, str | int]] = []
    for side, filename in (("prefix", "magicprefix.txt"), ("suffix", "magicsuffix.txt")):
        result = {"file": filename}
        result.update(apply_to_table(filename, side, split_sources, greater_by_side[side]))
        result.update(validate_table(filename))
        results.append(result)
    write_report(results)
    print(REPORT)


if __name__ == "__main__":
    main()
