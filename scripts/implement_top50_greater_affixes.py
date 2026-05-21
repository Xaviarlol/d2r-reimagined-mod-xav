"""Implement the reviewed top-50 Greater Affix redesign.

This script intentionally rebuilds Greater rows from the current post-Phase-1 data
rather than restoring old files wholesale. It removes the broad Greater experiment,
keeps the reviewed 50 logical families, converts gameplay stats back to normal
properties, and adds one colored marker stat per logical family.
"""

from __future__ import annotations

import json
import math
import re
import shutil
from collections import OrderedDict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXCEL = ROOT / "data" / "global" / "excel"
BASE = EXCEL / "base"
STRINGS = ROOT / "data" / "local" / "lng" / "strings" / "item-modifiers.json"

PREFIX = EXCEL / "magicprefix.txt"
SUFFIX = EXCEL / "magicsuffix.txt"
PROPERTIES = EXCEL / "properties.txt"
ITEMSTATCOST = EXCEL / "itemstatcost.txt"

MOD_SLOTS = ("mod1", "mod2", "mod3")
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


FAMILIES = OrderedDict(
    [
        ("grandmasters", "Grandmaster's"),
        ("wraithly_weapon", "Wraithly Weapon"),
        ("wraithly_armor", "Wraithly Armor"),
        ("godly", "Godly"),
        ("jewelers", "Jeweler's"),
        ("visionary", "Visionary"),
        ("gritty", "Gritty"),
        ("evisceration", "Evisceration"),
        ("transcendence_damage", "Transcendence Damage"),
        ("quickness", "Quickness"),
        ("alacrity", "Alacrity"),
        ("fervor", "Fervor"),
        ("deflecting", "Deflecting"),
        ("chromatic", "Chromatic"),
        ("scintillating", "Scintillating"),
        ("four_seasons", "Four Seasons"),
        ("elements", "Elements"),
        ("magus", "Magus"),
        ("apprentice", "Apprentice"),
        ("equilibrium", "Equilibrium"),
        ("traveling_speed", "Traveling / Speed"),
        ("omniscient", "Omniscient"),
        ("sages", "Sage's"),
        ("arch_angels", "Arch-Angel's"),
        ("witch_hunters", "Witch-hunter's"),
        ("valkyries", "Valkyrie's"),
        ("priests", "Priest's"),
        ("berserkers", "Berserker's"),
        ("necromancers", "Necromancer's"),
        ("hierophants", "Hierophant's"),
        ("arch_devils", "Arch-Devil's"),
        ("cunning", "Cunning"),
        ("rose_branded", "Rose Branded"),
        ("pyromaniacs_damage", "Pyromaniac's Damage"),
        ("pyromaniacs_pierce", "Pyromaniac's Pierce"),
        ("zeuss_damage", "Zeus's Damage"),
        ("zeuss_pierce", "Zeus's Pierce"),
        ("frost_wyrms_damage", "Frost Wyrm's Damage"),
        ("frost_wyrms_pierce", "Frost Wyrm's Pierce"),
        ("manticores_damage", "Manticore's Damage"),
        ("manticores_pierce", "Manticore's Pierce"),
        ("lich", "Lich"),
        ("transcendence_amp", "Transcendence Amp"),
        ("transcendence_lower_resist", "Transcendence Lower Resist"),
        ("aureole_might", "Aureole Might"),
        ("aureole_fanaticism", "Aureole Fanaticism"),
        ("aureole_conviction", "Aureole Conviction"),
        ("aureole_holy_freeze", "Aureole Holy Freeze"),
        ("aureole_meditation", "Aureole Meditation"),
        ("aureole_vigor", "Aureole Vigor"),
    ]
)

AURA_SOURCES = OrderedDict(
    [
        ("aureole_might", ("Might", "98")),
        ("aureole_fanaticism", ("Fanaticism", "122")),
        ("aureole_conviction", ("Conviction", "123")),
        ("aureole_holy_freeze", ("Holy Freeze", "114")),
        ("aureole_meditation", ("Meditation", "120")),
        ("aureole_vigor", ("Vigor", "115")),
    ]
)

PREFIX_DIRECT = {
    "Greater Wraithly Weapon": "wraithly_weapon",
    "Greater Wraithly Armor": "wraithly_armor",
    "Greater Jeweler's": "jewelers",
    "Greater Visionary": "visionary",
    "Greater Gritty": "gritty",
    "Greater Chromatic": "chromatic",
    "Greater Scintillating": "scintillating",
    "Greater Omniscient": "omniscient",
    "Greater Arch-Angel's": "arch_angels",
    "Greater Witch-hunter's": "witch_hunters",
    "Greater Valkyrie's": "valkyries",
    "Greater Priest's": "priests",
    "Greater Berserker's": "berserkers",
    "Greater Necromancer's": "necromancers",
    "Greater Hierophant's": "hierophants",
    "Greater Arch-Devil's": "arch_devils",
    "Greater Cunning": "cunning",
    "Greater Rose Branded": "rose_branded",
    "Greater Pyromaniac's Damage": "pyromaniacs_damage",
    "Greater Pyromaniac's Pierce": "pyromaniacs_pierce",
    "Greater Zeus's Damage": "zeuss_damage",
    "Greater Zeus's Pierce": "zeuss_pierce",
    "Greater Frost Wyrm's Damage": "frost_wyrms_damage",
    "Greater Frost Wyrm's Pierce": "frost_wyrms_pierce",
    "Greater Manticore's Damage": "manticores_damage",
    "Greater Manticore's Pierce": "manticores_pierce",
    "Greater Aureole Might": "aureole_might",
    "Greater Aureole Fanaticism": "aureole_fanaticism",
    "Greater Aureole Conviction": "aureole_conviction",
    "Greater Aureole Holy Freeze": "aureole_holy_freeze",
    "Greater Aureole Meditation": "aureole_meditation",
    "Greater Aureole Vigor": "aureole_vigor",
}

SUFFIX_DIRECT = {
    "of Greater Quickness": "quickness",
    "of Greater Alacrity": "alacrity",
    "of Greater Fervor": "fervor",
    "of Greater Deflecting": "deflecting",
    "of the Greater Four Seasons2": "four_seasons",
    "of the Greater Elements": "elements",
    "of the Greater Magus": "magus",
    "of the Greater Apprentice": "apprentice",
    "of Greater Equilibrium": "equilibrium",
    "of Greater Traveling": "traveling_speed",
    "of Greater Speed": "traveling_speed",
    "of the Greater Lich": "lich",
    "of Greater Evisceration": "evisceration",
    "of Greater Transcendence Damage": "transcendence_damage",
    "of Greater Transcendence Amp": "transcendence_amp",
    "of Greater Transcendence Lower Resist": "transcendence_lower_resist",
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
            raise ValueError(f"{path}: row has {len(parts)} fields, expected {len(header)}: {line[:120]}")
        rows.append(dict(zip(header, parts)))
    return header, rows


def write_tsv(path: Path, header: list[str], rows: list[dict[str, str]]) -> None:
    out = ["\t".join(header)]
    for row in rows:
        values = [row.get(col, "") for col in header]
        if len(values) != len(header):
            raise AssertionError(path)
        out.append("\t".join(values))
    path.write_text("\n".join(out) + "\n", encoding="utf-8")


def is_greater_row(row: dict[str, str]) -> bool:
    if "Greater" in row.get("name", ""):
        return True
    if row.get("* Description", "").startswith("Greater "):
        return True
    for slot in MOD_SLOTS:
        code = row.get(f"{slot}code", "")
        if code == "greater-affix-marker" or code.startswith("greater"):
            return True
    return False


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


def has_mod(row: dict[str, str], code: str, param: str | None = None) -> bool:
    for mod_code, mod_param, _, _ in mod_list(row):
        if mod_code == code and (param is None or mod_param == param):
            return True
    return False


def classify_prefix(row: dict[str, str]) -> str | None:
    name = row["name"]
    mods = mod_list(row)
    codes = {m[0] for m in mods}
    if name == "Greater Grandmaster's":
        if "greater_ethereal" in codes or "greater_rep-dur" in codes:
            return "wraithly_weapon"
        return "grandmasters"
    if name == "Greater Godly":
        if "greater_ethereal" in codes or "greater_rep-dur" in codes:
            return "wraithly_armor"
        return "godly"
    if name == "Greater Sage's":
        return "sages" if row.get("group") == "125" else None
    if name == "Greater Pyromaniac's":
        if any(code.endswith("extra-fire") for code in codes):
            return "pyromaniacs_damage"
        if any(code.endswith("pierce-fire") for code in codes):
            return "pyromaniacs_pierce"
    if name == "Greater Zeus's":
        if any(code.endswith("extra-ltng") for code in codes):
            return "zeuss_damage"
        if any(code.endswith("pierce-ltng") for code in codes):
            return "zeuss_pierce"
    if name == "Greater Frost Wyrm's":
        if any(code.endswith("extra-cold") for code in codes):
            return "frost_wyrms_damage"
        if any(code.endswith("pierce-cold") for code in codes):
            return "frost_wyrms_pierce"
    if name == "Greater Manticore's":
        if any(code.endswith("extra-pois") for code in codes):
            return "manticores_damage"
        if any(code.endswith("pierce-pois") for code in codes):
            return "manticores_pierce"
    return PREFIX_DIRECT.get(name)


def classify_suffix(row: dict[str, str]) -> str | None:
    name = row["name"]
    if name == "of Greater Transcendence":
        if has_mod(row, "greater_m_dmg-min"):
            return "transcendence_damage"
        if has_mod(row, "greater_m_hit-skill", "Amplify Damage"):
            return "transcendence_amp"
        if has_mod(row, "greater_m_hit-skill", "Lower Resist"):
            return "transcendence_lower_resist"
        return None
    return SUFFIX_DIRECT.get(name)


def normalize_code(code: str, normal_codes: set[str]) -> str:
    if code == "greater-affix-marker":
        return ""
    candidates = []
    if code.startswith("greater_m_"):
        candidates.append(code.removeprefix("greater_m_"))
    if code.startswith("greater_"):
        candidates.append(code.removeprefix("greater_"))
    if code in normal_codes:
        return code
    for candidate in candidates:
        if candidate in normal_codes:
            return candidate
    raise ValueError(f"Could not map Greater property code {code!r} to a normal property")


def clear_mods(row: dict[str, str]) -> None:
    for slot in MOD_SLOTS:
        for suffix in ("code", "param", "min", "max"):
            row[f"{slot}{suffix}"] = ""


def set_mods(row: dict[str, str], mods: list[tuple[str, str, str, str]]) -> None:
    if len(mods) > 3:
        raise ValueError(f"Too many mods for {row['name']}: {mods}")
    clear_mods(row)
    for index, (code, param, min_value, max_value) in enumerate(mods, 1):
        row[f"mod{index}code"] = code
        row[f"mod{index}param"] = param
        row[f"mod{index}min"] = min_value
        row[f"mod{index}max"] = max_value


def band_from_level(level: str) -> str:
    if level == "50":
        return "early"
    if level == "66":
        return "mid"
    if level == "81":
        return "late"
    raise ValueError(f"Unexpected Greater band level {level}")


def marker_property(slug: str) -> str:
    return f"ga_{slug}"


def marker_stat(slug: str) -> str:
    return f"ga_marker_{slug}"


def marker_key(slug: str) -> str:
    return f"GreaterAffix_{slug}"


def hybrid_property(slug: str, normal_code: str) -> str:
    safe_code = re.sub(r"[^A-Za-z0-9]+", "_", normal_code).strip("_")
    return f"ga_h_{slug}_{safe_code}"


def make_hybrid_property(
    normal_property: dict[str, str],
    slug: str,
    normal_code: str,
    prop_header: list[str],
) -> dict[str, str]:
    row = dict(normal_property)
    row["code"] = hybrid_property(slug, normal_code)
    row["*Id"] = ""
    row["*Notes"] = f"Greater Affix hybrid marker for {FAMILIES[slug]}"
    stat = marker_stat(slug)
    for idx in range(1, 8):
        if not row.get(f"func{idx}", ""):
            row[f"func{idx}"] = "1"
            row[f"stat{idx}"] = stat
            row[f"set{idx}"] = ""
            row[f"val{idx}"] = ""
            return {col: row.get(col, "") for col in prop_header}
    raise ValueError(f"No free property function slot for hybrid {slug}/{normal_code}")


def make_marker_property(slug: str, prop_header: list[str]) -> dict[str, str]:
    row = {col: "" for col in prop_header}
    row["code"] = marker_property(slug)
    row["*Enabled"] = "1"
    row["func1"] = "1"
    row["stat1"] = marker_stat(slug)
    row["*Tooltip"] = f"Greater Affix marker: {FAMILIES[slug]}"
    row["*Notes"] = "top-50 Greater Affix marker"
    row["*eol"] = "0"
    return row


def make_marker_stat_row(slug: str, template: dict[str, str], header: list[str]) -> dict[str, str]:
    row = dict(template)
    row["Stat"] = marker_stat(slug)
    row["*ID"] = ""
    row["descstrpos"] = marker_key(slug)
    row["descstrneg"] = marker_key(slug)
    row["*eol"] = "0"
    return {col: row.get(col, "") for col in header}


def convert_existing_greater_row(
    row: dict[str, str],
    slug: str,
    normal_codes: set[str],
    normal_props: dict[str, dict[str, str]],
    prop_header: list[str],
    hybrid_props: dict[str, dict[str, str]],
) -> dict[str, str]:
    codes = [code for code, _, _, _ in mod_list(row)]
    if any(code.startswith("ga_") for code in codes) and not any(
        code.startswith("greater") or code == "greater-affix-marker" for code in codes
    ):
        return dict(row)

    converted = dict(row)
    converted["name"] = greater_row_name(converted["name"], slug)
    band = band_from_level(converted["level"])
    converted["* Description"] = f"Greater {FAMILIES[slug]} [{band}; marker={marker_property(slug)}]"

    actual_mods = []
    for code, param, min_value, max_value in mod_list(row):
        normal_code = normalize_code(code, normal_codes)
        if normal_code:
            actual_mods.append((normal_code, param, min_value, max_value))

    if len(actual_mods) <= 2:
        set_mods(converted, [(marker_property(slug), "", "1", "1"), *actual_mods])
        return converted

    if len(actual_mods) == 3:
        first_code, first_param, first_min, first_max = actual_mods[0]
        hybrid_code = hybrid_property(slug, first_code)
        if hybrid_code not in hybrid_props:
            hybrid_props[hybrid_code] = make_hybrid_property(normal_props[first_code], slug, first_code, prop_header)
        set_mods(converted, [(hybrid_code, first_param, first_min, first_max), *actual_mods[1:]])
        return converted

    raise ValueError(f"Unexpected mod count for {row['name']}: {actual_mods}")


def greater_row_name(current_name: str, slug: str) -> str:
    if slug.startswith("wraithly_"):
        return f"Greater {FAMILIES[slug]}"
    if slug.startswith("aureole_"):
        return f"Greater {FAMILIES[slug]}"
    if slug in {"pyromaniacs_damage", "pyromaniacs_pierce"}:
        return f"Greater {FAMILIES[slug]}"
    if slug in {"zeuss_damage", "zeuss_pierce"}:
        return f"Greater {FAMILIES[slug]}"
    if slug in {"frost_wyrms_damage", "frost_wyrms_pierce"}:
        return f"Greater {FAMILIES[slug]}"
    if slug in {"manticores_damage", "manticores_pierce"}:
        return f"Greater {FAMILIES[slug]}"
    if slug in {"transcendence_damage", "transcendence_amp", "transcendence_lower_resist"}:
        return f"of Greater {FAMILIES[slug]}"
    return current_name


def band_freq(apex_freq: str, band: str) -> str:
    freq = int(apex_freq)
    late = max(1, round(freq / 10))
    if band == "late":
        return str(late)
    if band == "mid":
        return str(max(1, round(late * 2 / 3)))
    if band == "early":
        return str(max(1, round(late / 3)))
    raise ValueError(band)


def make_banded_rows(
    source: dict[str, str],
    slug: str,
    name: str,
    description: str,
    mods: list[tuple[str, str, str, str]],
    normal_props: dict[str, dict[str, str]],
    prop_header: list[str],
    hybrid_props: dict[str, dict[str, str]],
) -> list[dict[str, str]]:
    rows = []
    for band, level, maxlevel in (("early", "50", "65"), ("mid", "66", "80"), ("late", "81", "")):
        row = dict(source)
        row["name"] = name
        row["* Description"] = f"Greater {description} [{band}; marker={marker_property(slug)}]"
        row["spawnable"] = "1"
        row["rare"] = "1"
        row["level"] = level
        row["maxlevel"] = maxlevel
        row["frequency"] = band_freq(source["frequency"], band)
        row["levelreq"] = source["levelreq"]
        row["classspecific"] = source.get("classspecific", "")
        row["class"] = source.get("class", "")
        row["classlevelreq"] = source.get("classlevelreq", "")
        if len(mods) <= 2:
            set_mods(row, [(marker_property(slug), "", "1", "1"), *mods])
        else:
            first_code, first_param, first_min, first_max = mods[0]
            hybrid_code = hybrid_property(slug, first_code)
            if hybrid_code not in hybrid_props:
                hybrid_props[hybrid_code] = make_hybrid_property(normal_props[first_code], slug, first_code, prop_header)
            set_mods(row, [(hybrid_code, first_param, first_min, first_max), *mods[1:]])
        rows.append(row)
    return rows


def source_rows_by_name(rows: list[dict[str, str]], name: str) -> list[dict[str, str]]:
    return [row for row in rows if row["name"] == name and not is_greater_row(row)]


def highest_source(rows: list[dict[str, str]], name: str, predicate) -> dict[str, str]:
    matches = [row for row in source_rows_by_name(rows, name) if predicate(row)]
    if not matches:
        raise ValueError(f"No source row found for {name}")
    return max(matches, key=lambda r: (int(r.get("level") or 0), int(r.get("frequency") or 0)))


def strip_old_greater_properties(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    return [
        row
        for row in rows
        if not (
            row["code"].startswith("greater")
            or (row["code"].startswith("ga_") and not row["code"].startswith("ga_h_"))
        )
    ]


def strip_old_greater_stats(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    return [
        row
        for row in rows
        if not (
            row["Stat"].startswith("greater_")
            or row["Stat"].startswith("item_greaterAffix")
            or row["Stat"].startswith("ga_marker_")
        )
    ]


def assign_ids(rows: list[dict[str, str]], id_col: str) -> None:
    for index, row in enumerate(rows):
        row[id_col] = str(index)


def append_marker_strings() -> None:
    data = json.loads(STRINGS.read_text(encoding="utf-8"))
    active_keys = {marker_key(slug) for slug in FAMILIES}
    data = [
        entry
        for entry in data
        if not entry.get("Key", "").startswith("GreaterAffix_") or entry.get("Key", "") in active_keys
    ]
    existing = {entry["Key"] for entry in data}
    max_id = max(int(entry.get("id", 0)) for entry in data)
    for slug, label in FAMILIES.items():
        key = marker_key(slug)
        text = f"\u00ffc8Greater Affix: {label}\u00ffc3"
        if key in existing:
            entry = next(entry for entry in data if entry["Key"] == key)
            for locale in LOCALES:
                entry[locale] = text
            continue
        max_id += 1
        entry = {"id": max_id, "Key": key}
        for locale in LOCALES:
            entry[locale] = text
        data.append(entry)
    STRINGS.write_text(json.dumps(data, ensure_ascii=False, indent=4) + "\n", encoding="utf-8")


def validate_affix_table(header: list[str], rows: list[dict[str, str]], side: str) -> None:
    seen_greater = 0
    for row in rows:
        if len([row.get(col, "") for col in header]) != len(header):
            raise AssertionError(f"{side}: bad width for {row.get('name')}")
        if is_greater_row(row):
            seen_greater += 1
            if row.get("spawnable") != "1" or row.get("rare") != "1":
                raise AssertionError(f"{side}: Greater row not spawnable rare: {row['name']}")
            if row.get("level") == "50" and row.get("maxlevel") != "65":
                raise AssertionError(f"{side}: bad early band {row['name']}")
            if row.get("level") == "66" and row.get("maxlevel") != "80":
                raise AssertionError(f"{side}: bad mid band {row['name']}")
            if row.get("level") == "81" and row.get("maxlevel") != "":
                raise AssertionError(f"{side}: bad late band {row['name']}")
            if row.get("level") not in {"50", "66", "81"}:
                raise AssertionError(f"{side}: unexpected Greater level {row['level']} for {row['name']}")
            markers = [row.get(f"{slot}code", "") for slot in MOD_SLOTS if row.get(f"{slot}code", "").startswith("ga_")]
            if len(markers) != 1:
                raise AssertionError(f"{side}: expected exactly one GA marker/hybrid for {row['name']}: {markers}")
    if seen_greater == 0:
        raise AssertionError(f"{side}: no Greater rows emitted")


def main() -> None:
    prefix_header, prefix_rows = read_tsv(PREFIX)
    suffix_header, suffix_rows = read_tsv(SUFFIX)
    prop_header, prop_rows = read_tsv(PROPERTIES)
    stat_header, stat_rows = read_tsv(ITEMSTATCOST)

    normal_prop_rows = strip_old_greater_properties(prop_rows)
    normal_props = {row["code"]: row for row in normal_prop_rows}
    normal_codes = set(normal_props)

    prefix_base = [row for row in prefix_rows if not is_greater_row(row)]
    suffix_base = [row for row in suffix_rows if not is_greater_row(row)]
    removed_prefix = [row for row in prefix_rows if is_greater_row(row)]
    removed_suffix = [row for row in suffix_rows if is_greater_row(row)]

    marker_props = [make_marker_property(slug, prop_header) for slug in FAMILIES]
    hybrid_props: dict[str, dict[str, str]] = {}

    new_prefix_rows: list[dict[str, str]] = []
    selected_counts = {slug: 0 for slug in FAMILIES}

    for row in removed_prefix:
        slug = classify_prefix(row)
        if not slug:
            continue
        converted = convert_existing_greater_row(row, slug, normal_codes, normal_props, prop_header, hybrid_props)
        new_prefix_rows.append(converted)
        selected_counts[slug] += 1

    # Generate selected families that were not present in the broad Greater experiment.
    if selected_counts["jewelers"] == 0:
        jeweler = highest_source(prefix_base, "Jeweler's", lambda r: r.get("mod1code") == "sock")
        new_prefix_rows.extend(
            make_banded_rows(
                jeweler,
                "jewelers",
                "Greater Jeweler's",
                "Jeweler's",
                [("sock", jeweler["mod1param"], jeweler["mod1min"], jeweler["mod1max"])],
                normal_props,
                prop_header,
                hybrid_props,
            )
        )
        selected_counts["jewelers"] += 3

    if selected_counts["visionary"] == 0:
        visionary = highest_source(prefix_base, "Visionary", lambda r: r.get("mod1code") == "att%/lvl")
        new_prefix_rows.extend(
            make_banded_rows(
                visionary,
                "visionary",
                "Greater Visionary",
                "Visionary",
                [("att%/lvl", "3", "", "")],
                normal_props,
                prop_header,
                hybrid_props,
            )
        )
        selected_counts["visionary"] += 3

    for slug, (aura_name, skill_id) in AURA_SOURCES.items():
        if selected_counts[slug] != 0:
            continue
        source = highest_source(
            prefix_base,
            "Aureole",
            lambda r, expected=skill_id: r.get("mod1code") == "aura" and r.get("mod1param") == expected,
        )
        new_prefix_rows.extend(
            make_banded_rows(
                source,
                slug,
                f"Greater {FAMILIES[slug]}",
                f"{aura_name} Aura",
                [("aura", skill_id, "4", "4")],
                normal_props,
                prop_header,
                hybrid_props,
            )
        )
        selected_counts[slug] += 3

    new_suffix_rows: list[dict[str, str]] = []
    for row in removed_suffix:
        slug = classify_suffix(row)
        if not slug:
            continue
        converted = convert_existing_greater_row(row, slug, normal_codes, normal_props, prop_header, hybrid_props)
        new_suffix_rows.append(converted)
        selected_counts[slug] += 1

    missing = [slug for slug, count in selected_counts.items() if count == 0]
    if missing:
        raise AssertionError(f"No rows emitted for selected Greater families: {missing}")

    final_prefix = prefix_base + new_prefix_rows
    final_suffix = suffix_base + new_suffix_rows

    # Rebuild properties and itemstatcost.
    final_props = normal_prop_rows + marker_props + list(hybrid_props.values())
    next_prop_id = 0
    for row in final_props:
        row["*Id"] = str(next_prop_id)
        next_prop_id += 1

    marker_template = next((row for row in stat_rows if row["Stat"] == "item_greaterAffixMarker"), None)
    if marker_template is None:
        marker_template = next(row for row in stat_rows if row["Stat"].startswith("ga_marker_"))
    final_stats = strip_old_greater_stats(stat_rows)
    final_stats += [make_marker_stat_row(slug, marker_template, stat_header) for slug in FAMILIES]
    assign_ids(final_stats, "*ID")

    referenced_props = set()
    for row in new_prefix_rows + new_suffix_rows:
        for slot in MOD_SLOTS:
            if row.get(f"{slot}code"):
                referenced_props.add(row[f"{slot}code"])
    missing_props = sorted(referenced_props - {row["code"] for row in final_props})
    if missing_props:
        raise AssertionError(f"Missing properties: {missing_props}")

    referenced_stats = set()
    for prop in marker_props + list(hybrid_props.values()):
        for idx in range(1, 8):
            stat = prop.get(f"stat{idx}", "")
            if stat:
                referenced_stats.add(stat)
    missing_stats = sorted(referenced_stats - {row["Stat"] for row in final_stats})
    if missing_stats:
        raise AssertionError(f"Missing itemstats: {missing_stats}")

    max_stat_id = max(int(row["*ID"]) for row in final_stats)
    if max_stat_id > 510:
        raise AssertionError(f"itemstatcost max ID {max_stat_id} exceeds 510")

    validate_affix_table(prefix_header, final_prefix, "prefix")
    validate_affix_table(suffix_header, final_suffix, "suffix")

    write_tsv(PREFIX, prefix_header, final_prefix)
    write_tsv(SUFFIX, suffix_header, final_suffix)
    write_tsv(PROPERTIES, prop_header, final_props)
    write_tsv(ITEMSTATCOST, stat_header, final_stats)

    for path in (PREFIX, SUFFIX, PROPERTIES, ITEMSTATCOST):
        shutil.copy2(path, BASE / path.name)

    append_marker_strings()

    print(f"prefix greater rows: {len(new_prefix_rows)}")
    print(f"suffix greater rows: {len(new_suffix_rows)}")
    print(f"logical families: {len(FAMILIES)}")
    print(f"hybrid properties: {len(hybrid_props)}")
    print(f"itemstatcost max ID: {max_stat_id}")


if __name__ == "__main__":
    main()
