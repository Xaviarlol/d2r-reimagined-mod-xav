#!/usr/bin/env python3
"""Generate a rare-affix apex audit and draft Greater Affix chance table."""

from __future__ import annotations

import csv
from collections import defaultdict
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXCEL = ROOT / "data" / "global" / "excel"
OUT = ROOT / "docs" / "rare-greater-affix-apex-audit-2026-05-19.md"
CHANCE_TSV = ROOT / "docs" / "rare-greater-affix-chance-table-2026-05-19.tsv"
SANITY_TSV = ROOT / "docs" / "rare-greater-affix-probability-sanity-2026-05-19.tsv"
ALVL = 90
SLOTS = 3
FREQ_SCALE = 10


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f, delimiter="\t"))


ITEMTYPES = {r["Code"]: r for r in read_tsv(EXCEL / "itemtypes.txt") if r.get("Code")}


@lru_cache(maxsize=None)
def type_closure(code: str) -> frozenset[str]:
    if not code:
        return frozenset()
    row = ITEMTYPES.get(code)
    if not row:
        return frozenset({code})
    out = {code}
    for parent in (row.get("Equiv1", ""), row.get("Equiv2", "")):
        if parent:
            out.update(type_closure(parent))
    return frozenset(out)


def row_mods(row: dict[str, str]) -> list[str]:
    mods = []
    for n in range(1, 4):
        code = row.get(f"mod{n}code", "")
        if not code:
            continue
        param = row.get(f"mod{n}param", "")
        mn = row.get(f"mod{n}min", "")
        mx = row.get(f"mod{n}max", "")
        if param:
            mods.append(f"{code}({param}) {mn}-{mx}".strip())
        else:
            mods.append(f"{code} {mn}-{mx}".strip())
    return mods


def itypes(row: dict[str, str]) -> list[str]:
    return [row.get(f"itype{n}", "") for n in range(1, 8) if row.get(f"itype{n}", "")]


def etypes(row: dict[str, str]) -> list[str]:
    return [row.get(f"etype{n}", "") for n in range(1, 6) if row.get(f"etype{n}", "")]


def eligible(row: dict[str, str], item_type: str, alvl: int = ALVL) -> bool:
    if row.get("rare") != "1":
        return False
    level = int(row.get("level") or 0)
    maxlevel = int(row.get("maxlevel") or 0)
    if level > alvl:
        return False
    if maxlevel and alvl > maxlevel:
        return False
    closure = type_closure(item_type)
    include = itypes(row)
    exclude = etypes(row)
    if include and not any(t in closure for t in include):
        return False
    if any(t in closure for t in exclude):
        return False
    return True


def freq(row: dict[str, str]) -> int:
    return int(row.get("frequency") or 0)


def proposed_freq(row: dict[str, str]) -> int:
    if row.get("synthetic_greater") == "1":
        return int(row.get("frequency") or 0)
    return int(row.get("frequency") or 0) * FREQ_SCALE


def as_row(
    cid: str,
    name: str,
    side: str,
    group: int,
    level: int,
    maxlevel: int | None,
    frequency: int,
    include: list[str],
    exclude: list[str] | None = None,
) -> dict[str, str]:
    row = {
        "candidate_id": cid,
        "name": name,
        "side": side,
        "group": str(group),
        "level": str(level),
        "maxlevel": "" if maxlevel is None else str(maxlevel),
        "frequency": str(frequency),
        "rare": "1",
    }
    for idx, code in enumerate(include, start=1):
        row[f"itype{idx}"] = code
    for idx, code in enumerate(exclude or [], start=1):
        row[f"etype{idx}"] = code
    return row


def band_rows(cid: str, name: str, side: str, group: int, freq_late: int, include: list[str], exclude: list[str] | None = None) -> list[dict[str, str]]:
    return [
        as_row(cid, name, side, group, 50, 65, 1, include, exclude),
        as_row(cid, name, side, group, 66, 80, 2, include, exclude),
        as_row(cid, name, side, group, 81, None, freq_late, include, exclude),
    ]


CANDIDATES = [
    {
        "id": "greater-grandmasters",
        "name": "Greater Grandmaster's",
        "side": "prefix",
        "sample": "axe",
        "apex": "Grandmaster's variants and Wraithly1 in group 111",
        "greater": "dmg% 451-500 plus AR / Deadly / Crushing / Open Wounds rider",
        "rows": [
            as_row("greater-grandmasters", "Greater Grandmaster's", "prefix", 111, 50, 65, 1, ["weap"], ["orb", "wand"]),
            as_row("greater-grandmasters", "Greater Grandmaster's", "prefix", 111, 66, 80, 2, ["weap"], ["orb", "wand"]),
            as_row("greater-grandmasters", "Greater Grandmaster's", "prefix", 111, 81, None, 4, ["weap"], ["orb", "wand"]),
        ],
    },
    {
        "id": "greater-godly",
        "name": "Greater Godly",
        "side": "prefix",
        "sample": "tors",
        "apex": "Godly, Invulnerable1, armor Wraithly1 in group 101",
        "greater": "ac% 250-300 plus red-dmg% 26-30",
        "rows": band_rows("greater-godly", "Greater Godly", "prefix", 101, 3, ["armo", "shld"]),
    },
    {
        "id": "greater-antimagic-prefix",
        "name": "Greater Antimagic",
        "side": "prefix",
        "sample": "shld",
        "apex": "Antimagic res-mag 16-20 in group 102",
        "greater": "res-mag 24-30",
        "rows": band_rows("greater-antimagic-prefix", "Greater Antimagic", "prefix", 102, 3, ["shld", "tors", "orb", "wand", "staf"]),
    },
    {
        "id": "greater-bloody",
        "name": "Greater Bloody",
        "side": "prefix",
        "sample": "jewl",
        "apex": "Bloody min+max damage rows in group 103",
        "greater": "dmg-min 9-12 plus dmg-max 18-24",
        "rows": band_rows("greater-bloody", "Greater Bloody", "prefix", 103, 3, ["jewl", "lcha"]),
    },
    {
        "id": "greater-serrated",
        "name": "Greater Serrated",
        "side": "prefix",
        "sample": "lcha",
        "apex": "Serrated large charm enhanced damage in group 104",
        "greater": "dmg% 30-35 on large charms",
        "rows": band_rows("greater-serrated", "Greater Serrated", "prefix", 104, 3, ["lcha"]),
    },
    {
        "id": "greater-gritty",
        "name": "Greater Gritty",
        "side": "prefix",
        "sample": "axe",
        "apex": "Gritty damage-per-level in group 105",
        "greater": "stronger dmg/lvl weapon scaling",
        "rows": band_rows("greater-gritty", "Greater Gritty", "prefix", 105, 3, ["weap"], ["orb", "wand"]),
    },
    {
        "id": "greater-vulpine",
        "name": "Greater Vulpine",
        "side": "prefix",
        "sample": "shld",
        "apex": "Vulpine damage-to-mana in group 107",
        "greater": "dmg-to-mana 16-20",
        "rows": band_rows("greater-vulpine", "Greater Vulpine", "prefix", 107, 3, ["shld", "amul", "orb", "staf"]),
    },
    {
        "id": "greater-platinum",
        "name": "Greater Platinum",
        "side": "prefix",
        "sample": "axe",
        "apex": "highest attack-rating rows in group 110",
        "greater": "att 351-450, item-scope split if needed",
        "rows": band_rows("greater-platinum", "Greater Platinum", "prefix", 110, 3, ["weap", "ring", "amul", "lcha"]),
    },
    {
        "id": "greater-lucky",
        "name": "Greater Lucky",
        "side": "prefix",
        "sample": "lcha",
        "apex": "Lucky mag% plus gold% in group 114",
        "greater": "mag% 30-35 plus gold% 60-70",
        "rows": band_rows("greater-lucky", "Greater Lucky", "prefix", 114, 3, ["lcha"]),
    },
    {
        "id": "greater-serpents",
        "name": "Greater Serpent's",
        "side": "prefix",
        "sample": "lcha",
        "apex": "Serpent's mana in group 115",
        "greater": "mana 70-85",
        "rows": band_rows("greater-serpents", "Greater Serpent's", "prefix", 115, 3, ["lcha"]),
    },
    {
        "id": "greater-shimmering",
        "name": "Greater Shimmering",
        "side": "prefix",
        "sample": "lcha",
        "apex": "Shimmering all resistance in group 116",
        "greater": "res-all 15-18",
        "rows": band_rows("greater-shimmering", "Greater Shimmering", "prefix", 116, 3, ["lcha"]),
    },
    {
        "id": "greater-single-resist-charm",
        "name": "Greater Ruby/Sapphire/Amber/Emerald",
        "side": "prefix",
        "sample": "lcha",
        "apex": "single-element large charm resist rows in groups 117-120",
        "greater": "single resist 34-40, one element per row",
        "rows": (
            band_rows("greater-single-resist-charm", "Greater Sapphire", "prefix", 117, 3, ["lcha"])
            + band_rows("greater-single-resist-charm", "Greater Ruby", "prefix", 118, 3, ["lcha"])
            + band_rows("greater-single-resist-charm", "Greater Amber", "prefix", 119, 3, ["lcha"])
            + band_rows("greater-single-resist-charm", "Greater Emerald", "prefix", 120, 3, ["lcha"])
        ),
    },
    {
        "id": "greater-aureolin",
        "name": "Greater Aureolin",
        "side": "prefix",
        "sample": "jewl",
        "apex": "Aureolin mana after kill in group 121",
        "greater": "mana-kill 4-5",
        "rows": band_rows("greater-aureolin", "Greater Aureolin", "prefix", 121, 3, ["jewl"]),
    },
    {
        "id": "greater-celestial",
        "name": "Greater Celestial",
        "side": "prefix",
        "sample": "axe",
        "apex": "Celestial demon AR/damage in group 123",
        "greater": "att-demon 451-550 plus dmg-demon 351-425",
        "rows": band_rows("greater-celestial", "Greater Celestial", "prefix", 123, 3, ["weap"], ["wand", "orb"]),
    },
    {
        "id": "greater-omniscient",
        "name": "Greater Omniscient",
        "side": "prefix",
        "sample": "amul",
        "apex": "Omniscient/Sage's allskills in group 125",
        "greater": "allskills +3 torso/amulet, +2 ring",
        "rows": band_rows("greater-omniscient", "Greater Omniscient", "prefix", 125, 1, ["tors", "amul", "ring"]),
    },
    {
        "id": "greater-class-skill",
        "name": "Greater class skill",
        "side": "prefix",
        "sample": "amul",
        "apex": "+2 class skill rows, including Warlock, in group 125",
        "greater": "+3 class skills on torso/amulet/circlet scopes",
        "rows": band_rows("greater-class-skill", "Greater class skill", "prefix", 125, 1, ["tors", "amul", "circ"]),
    },
    {
        "id": "greater-skilltab",
        "name": "Greater Skilltab",
        "side": "prefix",
        "sample": "amul",
        "apex": "+3 skilltab rows in group 125",
        "greater": "skilltab +4, one row per skill tree",
        "rows": band_rows("greater-skilltab", "Greater Skilltab", "prefix", 125, 3, ["amul", "circ"]),
    },
    {
        "id": "greater-avatar",
        "name": "Greater Avatar",
        "side": "prefix",
        "sample": "lcha",
        "apex": "Avatar elemental large charm row in group 137",
        "greater": "dmg-elem 35-45",
        "rows": band_rows("greater-avatar", "Greater Avatar", "prefix", 137, 3, ["lcha"]),
    },
    {
        "id": "greater-weapon-elemental-prefix",
        "name": "Greater Scorching/Shocking/Pestilent",
        "side": "prefix",
        "sample": "axe",
        "apex": "weapon elemental damage prefixes in groups 138-140",
        "greater": "one element per row, about 25-35% above current apex",
        "rows": (
            band_rows("greater-weapon-elemental-prefix", "Greater Scorching", "prefix", 138, 3, ["weap"])
            + band_rows("greater-weapon-elemental-prefix", "Greater Shocking", "prefix", 139, 3, ["weap"])
            + band_rows("greater-weapon-elemental-prefix", "Greater Pestilent", "prefix", 140, 3, ["weap"])
        ),
    },
    {
        "id": "greater-divine",
        "name": "Greater Divine",
        "side": "prefix",
        "sample": "axe",
        "apex": "Divine undead AR/damage in group 142",
        "greater": "att-undead 500-650 plus dmg-undead 400-500",
        "rows": band_rows("greater-divine", "Greater Divine", "prefix", 142, 3, ["weap"], ["wand", "orb"]),
    },
    {
        "id": "greater-hulking",
        "name": "Greater Hulking",
        "side": "prefix",
        "sample": "lcha",
        "apex": "Hulking normal damage large charm in group 143",
        "greater": "dmg-norm 70-85",
        "rows": band_rows("greater-hulking", "Greater Hulking", "prefix", 143, 3, ["lcha"]),
    },
    {
        "id": "greater-veracious",
        "name": "Greater Veracious",
        "side": "prefix",
        "sample": "glov",
        "apex": "Veracious attack% in group 200",
        "greater": "att% 40-50",
        "rows": band_rows("greater-veracious", "Greater Veracious", "prefix", 200, 3, ["weap", "glov"]),
    },
    {
        "id": "greater-gnostic",
        "name": "Greater Gnostic",
        "side": "prefix",
        "sample": "amul",
        "apex": "+5 random class skill rows in group 201",
        "greater": "skill-rand +6, one class band per row",
        "rows": band_rows("greater-gnostic", "Greater Gnostic", "prefix", 201, 1, ["amul", "circ", "belt", "ring"]),
    },
    {
        "id": "greater-crushing-fatal",
        "name": "Greater Crushing/Fatal",
        "side": "prefix",
        "sample": "glov",
        "apex": "Crushing and Fatal glove rows in group 202",
        "greater": "crush/deadly 24-30, separate rows in same group",
        "rows": band_rows("greater-crushing-fatal", "Greater Crushing/Fatal", "prefix", 202, 3, ["glov"]),
    },
    {
        "id": "greater-elemental-prefix",
        "name": "Greater Elemental",
        "side": "prefix",
        "sample": "axe",
        "apex": "Elemental1 mixed elemental weapon row in group 203",
        "greater": "dmg-elem above current range",
        "rows": band_rows("greater-elemental-prefix", "Greater Elemental", "prefix", 203, 3, ["weap"]),
    },
    {
        "id": "greater-sage-xp",
        "name": "Greater Sage",
        "side": "prefix",
        "sample": "amul",
        "apex": "Master Sage's addxp in group 204",
        "greater": "addxp 6",
        "rows": band_rows("greater-sage-xp", "Greater Sage", "prefix", 204, 3, ["amul", "ring", "circ", "weap", "armo", "shld"]),
    },
    {
        "id": "greater-savage",
        "name": "Greater Savage",
        "side": "prefix",
        "sample": "boot",
        "apex": "Savage kick damage in group 205",
        "greater": "kick 11-13",
        "rows": band_rows("greater-savage", "Greater Savage", "prefix", 205, 3, ["boot"]),
    },
    {
        "id": "greater-adamantine-wrought",
        "name": "Greater Adamantine-Wrought",
        "side": "prefix",
        "sample": "axe",
        "apex": "Adamantine-Wrought ED/defense plus durability in group 206",
        "greater": "weapon dmg% 110-130 or armor ac% 85-100 plus dur 80-100",
        "rows": band_rows("greater-adamantine-wrought", "Greater Adamantine-Wrought", "prefix", 206, 3, ["weap", "armo", "shld"], ["orb", "wand"]),
    },
    {
        "id": "greater-aureole",
        "name": "Greater Aureole",
        "side": "prefix",
        "sample": "tors",
        "apex": "Aureole aura rows in group 207",
        "greater": "higher aura level; needs per-aura balance",
        "rows": band_rows("greater-aureole", "Greater Aureole", "prefix", 207, 1, ["tors"]),
    },
    {
        "id": "greater-elemental-mastery",
        "name": "Greater Elemental Mastery",
        "side": "prefix",
        "sample": "wand",
        "apex": "extra-fire/cold/lightning/poison caster rows in group 209",
        "greater": "extra-* 14-16",
        "rows": band_rows("greater-elemental-mastery", "Greater Elemental Mastery", "prefix", 209, 2, ["wand", "orb", "staf"]),
    },
    {
        "id": "greater-elemental-pierce",
        "name": "Greater Elemental Pierce",
        "side": "prefix",
        "sample": "wand",
        "apex": "pierce-fire/cold/lightning/poison caster rows in group 209",
        "greater": "pierce-* 14-16",
        "rows": band_rows("greater-elemental-pierce", "Greater Elemental Pierce", "prefix", 209, 2, ["wand", "orb", "staf"]),
    },
    {
        "id": "greater-missile-prefix",
        "name": "Greater missile prefixes",
        "side": "prefix",
        "sample": "misl",
        "apex": "missile-only prefix groups 220-227",
        "greater": "stronger quiver/missile weapon stat family rows",
        "rows": (
            band_rows("greater-missile-prefix", "Greater missile prefix", "prefix", 220, 2, ["misl"])
            + band_rows("greater-missile-prefix", "Greater missile prefix", "prefix", 221, 2, ["misl"])
            + band_rows("greater-missile-prefix", "Greater missile prefix", "prefix", 222, 2, ["misl"])
            + band_rows("greater-missile-prefix", "Greater missile prefix", "prefix", 223, 2, ["misl"])
            + band_rows("greater-missile-prefix", "Greater missile prefix", "prefix", 224, 2, ["misl"])
            + band_rows("greater-missile-prefix", "Greater missile prefix", "prefix", 225, 2, ["misl"])
            + band_rows("greater-missile-prefix", "Greater missile prefix", "prefix", 226, 2, ["misl"])
            + band_rows("greater-missile-prefix", "Greater missile prefix", "prefix", 227, 2, ["misl"])
        ),
    },
    {
        "id": "greater-anima",
        "name": "Greater Anima",
        "side": "suffix",
        "sample": "tors",
        "apex": "Anima flat damage reduction in group 1",
        "greater": "red-dmg 18-24",
        "rows": band_rows("greater-anima", "Greater Anima", "suffix", 1, 3, ["tors", "shld", "circ"]),
    },
    {
        "id": "greater-negation",
        "name": "Greater Negation",
        "side": "suffix",
        "sample": "shld",
        "apex": "Negation res-mag 14-20 in group 2",
        "greater": "res-mag 24-30",
        "rows": band_rows("greater-negation", "Greater Negation", "suffix", 2, 3, ["shld", "orb", "circ", "tors"]),
    },
    {
        "id": "greater-coalescence",
        "name": "Greater Coalescence",
        "side": "suffix",
        "sample": "ring",
        "apex": "elemental absorb percent rows in group 3",
        "greater": "abs-fire/ltng/cold% 28-35, one element per row",
        "rows": band_rows("greater-coalescence", "Greater Coalescence", "suffix", 3, 3, ["weap", "amul", "ring", "shld"]),
    },
    {
        "id": "greater-thorns",
        "name": "Greater Thorns",
        "side": "suffix",
        "sample": "tors",
        "apex": "Thorns flat/level retaliation in group 6",
        "greater": "stronger thorns/lvl",
        "rows": band_rows("greater-thorns", "Greater Thorns", "suffix", 6, 3, ["tors", "shld"]),
    },
    {
        "id": "greater-quickness",
        "name": "Greater Quickness",
        "side": "suffix",
        "sample": "axe",
        "apex": "Quickness IAS in group 7",
        "greater": "swing3 50",
        "rows": band_rows("greater-quickness", "Greater Quickness", "suffix", 7, 3, ["mele"], ["wand", "staf", "orb"]),
    },
    {
        "id": "greater-deflecting",
        "name": "Greater Deflecting",
        "side": "suffix",
        "sample": "shld",
        "apex": "Deflecting block rows in group 8",
        "greater": "block 35-40 plus block2 40",
        "rows": band_rows("greater-deflecting", "Greater Deflecting", "suffix", 8, 3, ["shld"]),
    },
    {
        "id": "greater-magus",
        "name": "Greater Magus",
        "side": "suffix",
        "sample": "orb",
        "apex": "Magus FCR in group 9",
        "greater": "cast3 25",
        "rows": band_rows("greater-magus", "Greater Magus", "suffix", 9, 3, ["rod", "orb", "circ"], ["scep"]),
    },
    {
        "id": "greater-jewelry-elemental-suffix",
        "name": "Greater jewelry elemental damage",
        "side": "suffix",
        "sample": "amul",
        "apex": "Glacier/Burning/Storms/Blight jewelry elemental rows in groups 10,12,13,16",
        "greater": "about 25-35% above current apex, one element per row",
        "rows": (
            band_rows("greater-jewelry-elemental-suffix", "Greater jewelry elemental damage", "suffix", 10, 2, ["belt", "amul"])
            + band_rows("greater-jewelry-elemental-suffix", "Greater jewelry elemental damage", "suffix", 12, 2, ["glov", "ring", "amul"])
            + band_rows("greater-jewelry-elemental-suffix", "Greater jewelry elemental damage", "suffix", 13, 2, ["boot", "ring", "amul"])
            + band_rows("greater-jewelry-elemental-suffix", "Greater jewelry elemental damage", "suffix", 16, 2, ["ring", "amul"])
        ),
    },
    {
        "id": "greater-evisceration",
        "name": "Greater Evisceration",
        "side": "suffix",
        "sample": "axe",
        "apex": "Evisceration max damage in group 14",
        "greater": "dmg-max 150-165",
        "rows": band_rows("greater-evisceration", "Greater Evisceration", "suffix", 14, 3, ["weap"], ["wand", "staf", "orb"]),
    },
    {
        "id": "greater-transcendence",
        "name": "Greater Transcendence",
        "side": "suffix",
        "sample": "axe",
        "apex": "Transcendence min damage in group 15",
        "greater": "dmg-min 75-85",
        "rows": band_rows("greater-transcendence", "Greater Transcendence", "suffix", 15, 3, ["weap"], ["orb", "wand"]),
    },
    {
        "id": "greater-perfection",
        "name": "Greater Perfection",
        "side": "suffix",
        "sample": "boot",
        "apex": "Perfection dexterity in group 17",
        "greater": "dex 36-40",
        "rows": band_rows("greater-perfection", "Greater Perfection", "suffix", 17, 3, ["tors", "boot"], ["glov"]),
    },
    {
        "id": "greater-balance",
        "name": "Greater Balance",
        "side": "suffix",
        "sample": "lcha",
        "apex": "Balance FHR on large charms in group 18",
        "greater": "balance3 13-15",
        "rows": band_rows("greater-balance", "Greater Balance", "suffix", 18, 3, ["lcha"]),
    },
    {
        "id": "greater-regeneration",
        "name": "Greater Regeneration",
        "side": "suffix",
        "sample": "boot",
        "apex": "Regeneration life regen in group 19",
        "greater": "regen 6-8",
        "rows": band_rows("greater-regeneration", "Greater Regeneration", "suffix", 19, 3, ["tors", "weap", "boot"], ["scep"]),
    },
    {
        "id": "greater-wealth",
        "name": "Greater Wealth",
        "side": "suffix",
        "sample": "belt",
        "apex": "Wealth gold find in group 21",
        "greater": "gold% 100-120",
        "rows": band_rows("greater-wealth", "Greater Wealth", "suffix", 21, 3, ["boot", "glov", "belt", "amul", "circ"]),
    },
    {
        "id": "greater-prosperity",
        "name": "Greater Prosperity",
        "side": "suffix",
        "sample": "jewl",
        "apex": "Prosperity magic find in group 22",
        "greater": "mag% 26-30",
        "rows": band_rows("greater-prosperity", "Greater Prosperity", "suffix", 22, 3, ["jewl"]),
    },
    {
        "id": "greater-enlightenment",
        "name": "Greater Enlightenment",
        "side": "suffix",
        "sample": "amul",
        "apex": "Energy rows in group 23",
        "greater": "enr 36-40, scope split if needed",
        "rows": band_rows("greater-enlightenment", "Greater Enlightenment", "suffix", 23, 3, ["amul", "orb", "circ", "wand", "staf", "ring", "jewl"]),
    },
    {
        "id": "greater-vita",
        "name": "Greater Vita",
        "side": "suffix",
        "sample": "lcha",
        "apex": "Vita life on large charms in group 26",
        "greater": "hp 80-95",
        "rows": band_rows("greater-vita", "Greater Vita", "suffix", 26, 3, ["lcha"]),
    },
    {
        "id": "greater-leech",
        "name": "Greater Lamprey/Vampire",
        "side": "suffix",
        "sample": "ring",
        "apex": "single leech rows in groups 27 and 28",
        "greater": "lifesteal/manasteal above current top, scope split",
        "rows": (
            band_rows("greater-leech", "Greater Lamprey", "suffix", 27, 3, ["amul"])
            + band_rows("greater-leech", "Greater Vampire", "suffix", 28, 3, ["ring"])
        ),
    },
    {
        "id": "greater-titan",
        "name": "Greater Titan",
        "side": "suffix",
        "sample": "ring",
        "apex": "strength/dex/vit/enr rows in group 31",
        "greater": "primary stat 26-30 or equivalent scope split",
        "rows": band_rows("greater-titan", "Greater Titan", "suffix", 31, 3, ["ring", "scep", "mace", "tors"]),
    },
    {
        "id": "greater-inertia",
        "name": "Greater Inertia",
        "side": "suffix",
        "sample": "lcha",
        "apex": "Inertia FRW large charm in group 35",
        "greater": "move3 13-15",
        "rows": band_rows("greater-inertia", "Greater Inertia", "suffix", 35, 3, ["lcha"]),
    },
    {
        "id": "greater-elephant",
        "name": "Greater Elephant",
        "side": "suffix",
        "sample": "ring",
        "apex": "Elephant hp/lvl and mana/lvl in group 41",
        "greater": "stronger hp/lvl plus mana/lvl",
        "rows": band_rows("greater-elephant", "Greater Elephant", "suffix", 41, 3, ["ring", "amul"]),
    },
    {
        "id": "greater-zodiac",
        "name": "Greater Zodiac",
        "side": "suffix",
        "sample": "amul",
        "apex": "Zodiac all-stats in group 42",
        "greater": "all-stats 38-45",
        "rows": band_rows("greater-zodiac", "Greater Zodiac", "suffix", 42, 3, ["amul", "ring", "circ", "orb", "staf", "wand"]),
    },
    {
        "id": "greater-elements",
        "name": "Greater Elements",
        "side": "suffix",
        "sample": "shld",
        "apex": "Elements res/lvl row in group 43",
        "greater": "stronger multi-res per level",
        "rows": band_rows("greater-elements", "Greater Elements", "suffix", 43, 3, ["circ", "shld"]),
    },
    {
        "id": "greater-lich",
        "name": "Greater Lich",
        "side": "suffix",
        "sample": "ring",
        "apex": "Lich dual leech in group 60",
        "greater": "manasteal 10-12 plus lifesteal 13-15",
        "rows": band_rows("greater-lich", "Greater Lich", "suffix", 60, 3, ["ring", "amul"]),
    },
    {
        "id": "greater-guarding",
        "name": "Greater Guarding",
        "side": "suffix",
        "sample": "ring",
        "apex": "Guarding flat defense on jewelry in group 61",
        "greater": "ac 60-90",
        "rows": band_rows("greater-guarding", "Greater Guarding", "suffix", 61, 3, ["ring", "amul"]),
    },
    {
        "id": "greater-paralysis",
        "name": "Greater Paralysis",
        "side": "suffix",
        "sample": "axe",
        "apex": "Paralysis slow target in group 64",
        "greater": "slow 28-33",
        "rows": band_rows("greater-paralysis", "Greater Paralysis", "suffix", 64, 2, ["weap"]),
    },
    {
        "id": "greater-blindness",
        "name": "Greater Blindness",
        "side": "suffix",
        "sample": "axe",
        "apex": "Blindness hit blinds target in group 65",
        "greater": "stupidity 4",
        "rows": band_rows("greater-blindness", "Greater Blindness", "suffix", 65, 2, ["weap"]),
    },
    {
        "id": "greater-reanimation",
        "name": "Greater Reanimation",
        "side": "suffix",
        "sample": "glov",
        "apex": "Reanimation in group 66",
        "greater": "higher reanimate chance/level",
        "rows": band_rows("greater-reanimation", "Greater Reanimation", "suffix", 66, 2, ["weap", "glov", "amul"]),
    },
    {
        "id": "greater-four-seasons",
        "name": "Greater Four Seasons",
        "side": "suffix",
        "sample": "shld",
        "apex": "Four Seasons max all resist in group 67",
        "greater": "res-all-max 7-8",
        "rows": band_rows("greater-four-seasons", "Greater Four Seasons", "suffix", 67, 1, ["armo", "shld", "ring", "amul"]),
    },
    {
        "id": "greater-draining",
        "name": "Greater Draining",
        "side": "suffix",
        "sample": "axe",
        "apex": "Siphoning heal per hit in group 80",
        "greater": "healperhit 14-16",
        "rows": band_rows("greater-draining", "Greater Draining", "suffix", 80, 3, ["mele", "amaz"]),
    },
    {
        "id": "greater-missile-suffix",
        "name": "Greater missile suffixes",
        "side": "suffix",
        "sample": "misl",
        "apex": "missile-only suffix groups 200-206",
        "greater": "stronger quiver/missile weapon suffix rows",
        "rows": (
            band_rows("greater-missile-suffix", "Greater missile suffix", "suffix", 200, 2, ["misl"])
            + band_rows("greater-missile-suffix", "Greater missile suffix", "suffix", 201, 2, ["misl"])
            + band_rows("greater-missile-suffix", "Greater missile suffix", "suffix", 202, 2, ["misl"])
            + band_rows("greater-missile-suffix", "Greater missile suffix", "suffix", 203, 2, ["misl"])
            + band_rows("greater-missile-suffix", "Greater missile suffix", "suffix", 204, 2, ["misl"])
            + band_rows("greater-missile-suffix", "Greater missile suffix", "suffix", 205, 2, ["misl"])
            + band_rows("greater-missile-suffix", "Greater missile suffix", "suffix", 206, 1, ["misl"])
        ),
    },
]


GROUP_ACTIONS = {
    ("prefix", "44"): "Defer: charged-skill affixes are technical and not a clean Greater range.",
    ("prefix", "112"): "Defer: light radius plus small AR is not a meaningful chase family.",
    ("prefix", "113"): "Defer: howl-on-hit utility needs a separate crowd-control affix review.",
    ("prefix", "122"): "Defer: sockets dominate item identity and need a separate socket-affix review.",
    ("prefix", "141"): "Defer: stack-size utility, not a rare-power target.",
    ("prefix", "307"): "Defer/exempt: special rare-only pierce rows with mixed charm/non-charm scopes.",
    ("suffix", "4"): "Defer: ignore target defense is binary.",
    ("suffix", "5"): "Optional: reduce target defense can be Greater later, but is not a first-pass chase family.",
    ("suffix", "11"): "Defer: half-freeze/cannot-freeze are binary.",
    ("suffix", "20"): "Defer: prevent monster heal is binary.",
    ("suffix", "24"): "Defer: knockback is binary.",
    ("suffix", "25"): "Defer: light radius plus small AR is not a meaningful chase family.",
    ("suffix", "29"): "Optional: poison length reduction is utility-only.",
    ("suffix", "30"): "Optional: requirements reduction is strong utility but needs item-scope balance.",
    ("suffix", "37"): "Defer: repair rate needs durability-system review.",
    ("suffix", "39"): "Defer: indestructible/repair quantity is utility-binary.",
    ("suffix", "44"): "Defer: charged-skill affixes are technical.",
    ("suffix", "63"): "Optional utility: vendor price reduction can be revisited after combat affixes.",
    ("suffix", "77"): "Defer: get-hit proc affixes need proc-specific balance.",
    ("suffix", "78"): "Defer: on-hit proc affixes need proc-specific balance.",
    ("suffix", "79"): "Defer: level-up/death proc affixes are event proc systems.",
    ("suffix", "81"): "Defer: class-special mechanics, not broad Greater rows.",
    ("suffix", "307"): "Defer/exempt: special rare-only pierce rows with mixed charm/non-charm scopes.",
}


APEX_RULES = {
    "greater-grandmasters": {"names": {"Grandmaster's", "Wraithly1"}},
    "greater-godly": {"names": {"Godly", "Wraithly1", "Invulnerable1"}, "max_level": True},
    "greater-antimagic-prefix": {"names": {"Antimagic"}, "mod_codes_any": {"res-mag"}},
    "greater-omniscient": {"mod_codes_any": {"allskills"}, "max_mod_value_code": "allskills"},
    "greater-class-skill": {"mod_codes_any": {"ama", "pal", "nec", "sor", "bar", "dru", "ass", "war"}, "mod_value": 2},
    "greater-skilltab": {"mod_codes_any": {"skilltab"}, "mod_value": 3},
    "greater-gnostic": {"mod_codes_any": {"skill-rand"}, "mod_param": "5"},
    "greater-elemental-mastery": {"mod_code_prefixes": {"extra-"}, "max_level": True},
    "greater-elemental-pierce": {"mod_code_prefixes": {"pierce-"}, "max_level": True},
    "greater-coalescence": {"mod_codes_any": {"abs-fire%", "abs-ltng%", "abs-cold%"}, "max_level": True},
    "greater-draining": {"names": {"of Siphoning"}},
}


def load_affixes() -> dict[str, list[dict[str, str]]]:
    out = {}
    for side, fname in (("prefix", "magicprefix.txt"), ("suffix", "magicsuffix.txt")):
        rows = []
        for idx, row in enumerate(read_tsv(EXCEL / fname), start=2):
            row["side"] = side
            row["line"] = str(idx)
            rows.append(row)
        out[side] = rows
    return out


def pool_for(affixes: dict[str, list[dict[str, str]]], side: str, item_type: str, synthetic: list[dict[str, str]]) -> list[dict[str, str]]:
    rows = [r for r in affixes[side] if eligible(r, item_type)]
    rows.extend(r for r in synthetic if r["side"] == side and eligible(r, item_type))
    return rows


def current_pool_for(affixes: dict[str, list[dict[str, str]]], side: str, item_type: str) -> list[dict[str, str]]:
    return [r for r in affixes[side] if eligible(r, item_type)]


def candidate_groups(candidate: dict[str, object]) -> set[str]:
    return {r["group"] for r in candidate["rows"]}


def mod_entries(row: dict[str, str]) -> list[tuple[str, str, str, str]]:
    return [
        (row.get(f"mod{n}code", ""), row.get(f"mod{n}param", ""), row.get(f"mod{n}min", ""), row.get(f"mod{n}max", ""))
        for n in range(1, 4)
        if row.get(f"mod{n}code", "")
    ]


def row_matches_apex_rule(row: dict[str, str], rule: dict[str, object]) -> bool:
    entries = mod_entries(row)
    codes = {code for code, _, _, _ in entries}
    if "names" in rule and row.get("name") not in rule["names"]:
        return False
    if "mod_codes_any" in rule and codes.isdisjoint(rule["mod_codes_any"]):
        return False
    if "mod_code_prefixes" in rule:
        prefixes = tuple(rule["mod_code_prefixes"])
        if not any(code.startswith(prefixes) for code in codes):
            return False
    if "mod_param" in rule and not any(param == rule["mod_param"] for _, param, _, _ in entries):
        return False
    if "mod_value" in rule:
        target = str(rule["mod_value"])
        if not any(mn == target and mx == target for _, _, mn, mx in entries):
            return False
    return True


def max_level_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    grouped = defaultdict(list)
    for row in rows:
        grouped[row.get("group") or "blank"].append(row)
    out = []
    for group_rows in grouped.values():
        max_level = max(int(row.get("level") or 0) for row in group_rows)
        out.extend(row for row in group_rows if int(row.get("level") or 0) == max_level)
    return out


def max_mod_value_rows(rows: list[dict[str, str]], code: str) -> list[dict[str, str]]:
    scored = []
    for row in rows:
        values = []
        for mod_code, _, mn, mx in mod_entries(row):
            if mod_code == code:
                for raw in (mn, mx):
                    if raw.lstrip("-").isdigit():
                        values.append(int(raw))
        if values:
            scored.append((max(values), row))
    if not scored:
        return rows
    max_value = max(score for score, _ in scored)
    return [row for score, row in scored if score == max_value]


def apex_rows_for(affixes: dict[str, list[dict[str, str]]], candidate: dict[str, object]) -> list[dict[str, str]]:
    groups = candidate_groups(candidate)
    rows = [
        row
        for row in affixes[candidate["side"]]
        if eligible(row, candidate["sample"]) and (row.get("group") or "blank") in groups
    ]
    rule = APEX_RULES.get(candidate["id"])
    if rule:
        rows = [row for row in rows if row_matches_apex_rule(row, rule)]
        if rule.get("max_level"):
            rows = max_level_rows(rows)
        if "max_mod_value_code" in rule:
            rows = max_mod_value_rows(rows, rule["max_mod_value_code"])
    else:
        rows = max_level_rows(rows)
    return rows


def synthetic_greater_rows(affixes: dict[str, list[dict[str, str]]]) -> list[dict[str, str]]:
    synthetic = []
    for candidate in CANDIDATES:
        apex_by_group: dict[str, int] = defaultdict(int)
        for row in apex_rows_for(affixes, candidate):
            apex_by_group[row.get("group") or "blank"] += freq(row)
        for group, target_weight in apex_by_group.items():
            if target_weight <= 0:
                continue
            eligible_templates = [
                row
                for row in candidate["rows"]
                if (row.get("group") or "blank") == group and eligible(row, candidate["sample"])
            ]
            if not eligible_templates:
                eligible_templates = [row for row in candidate["rows"] if (row.get("group") or "blank") == group]
            if not eligible_templates:
                continue
            base = target_weight // len(eligible_templates)
            remainder = target_weight % len(eligible_templates)
            for idx, template in enumerate(eligible_templates):
                row = dict(template)
                row["frequency"] = str(base + (1 if idx < remainder else 0))
                if int(row["frequency"]) <= 0:
                    continue
                row["synthetic_greater"] = "1"
                synthetic.append(row)
    return synthetic


def group_weights(pool: list[dict[str, str]], is_target, weight_fn=freq) -> dict[str, tuple[int, int]]:
    weights: dict[str, list[int]] = defaultdict(lambda: [0, 0])
    for row in pool:
        g = row.get("group") or "blank"
        f = weight_fn(row)
        weights[g][0] += f
        if is_target(row):
            weights[g][1] += f
    return {g: (vals[0], vals[1]) for g, vals in weights.items()}


def exact_groupblocked_chance(weights: dict[str, tuple[int, int]], slots: int = SLOTS) -> float:
    groups = tuple(sorted((g, w, c) for g, (w, c) in weights.items() if w > 0))

    @lru_cache(maxsize=None)
    def rec(state: tuple[tuple[str, int, int], ...], remaining: int) -> float:
        if remaining <= 0 or not state:
            return 0.0
        total = sum(w for _, w, _ in state)
        if total <= 0:
            return 0.0
        chance = 0.0
        for idx, (g, w, c) in enumerate(state):
            if c:
                chance += c / total
            non_target_weight = w - c
            if non_target_weight > 0:
                next_state = state[:idx] + state[idx + 1 :]
                chance += (non_target_weight / total) * rec(next_state, remaining - 1)
        return chance

    return rec(groups, slots)


def chance_rows(affixes: dict[str, list[dict[str, str]]]) -> list[dict[str, str]]:
    synthetic = synthetic_greater_rows(affixes)
    rows = []
    for c in CANDIDATES:
        before_pool = current_pool_for(affixes, c["side"], c["sample"])
        after_pool = pool_for(affixes, c["side"], c["sample"], synthetic)
        before_total = sum(freq(r) for r in before_pool)
        after_regular_total = sum(proposed_freq(r) for r in after_pool if r.get("synthetic_greater") != "1")
        after_greater_total = sum(proposed_freq(r) for r in after_pool if r.get("synthetic_greater") == "1")
        after_total = after_regular_total + after_greater_total
        cand_weight = sum(proposed_freq(r) for r in after_pool if r.get("candidate_id") == c["id"])
        apex_rows = apex_rows_for(affixes, c)
        apex_lines = {row["line"] for row in apex_rows}
        apex_weight_before = sum(freq(r) for r in before_pool if r.get("line") in apex_lines)
        apex_weight_after = apex_weight_before * FREQ_SCALE
        slot = cand_weight / after_total if after_total else 0.0
        apex_slot_before = apex_weight_before / before_total if before_total else 0.0
        apex_slot_after = apex_weight_after / after_total if after_total else 0.0
        item = exact_groupblocked_chance(
            group_weights(after_pool, lambda row, cid=c["id"]: row.get("candidate_id") == cid, proposed_freq),
            SLOTS,
        )
        apex_item = exact_groupblocked_chance(
            group_weights(after_pool, lambda row, lines=apex_lines: row.get("line") in lines, proposed_freq),
            SLOTS,
        )
        if apex_weight_after and cand_weight:
            ratio = apex_weight_after / cand_weight
            ratio_text = f"{ratio:.1f}x rarer"
        elif cand_weight and not apex_weight_after:
            ratio_text = "no apex baseline"
        else:
            ratio_text = "n/a"
        ordinary_drift = (after_regular_total / after_total - 1.0) if after_total else 0.0
        old_relative_check_delta = 0.0 if before_total and after_regular_total else 0.0
        rows.append({
            **c,
            "before_pool_weight": before_total,
            "after_pool_weight": after_total,
            "after_regular_weight": after_regular_total,
            "after_greater_weight": after_greater_total,
            "candidate_weight": cand_weight,
            "apex_weight_before": apex_weight_before,
            "apex_weight_after": apex_weight_after,
            "slot_chance": slot,
            "item_chance": item,
            "apex_slot_chance_before": apex_slot_before,
            "apex_slot_chance_after": apex_slot_after,
            "apex_item_chance": apex_item,
            "greater_vs_apex": ratio_text,
            "ordinary_absolute_drift": ordinary_drift,
            "old_relative_check_delta": old_relative_check_delta,
            "apex_rows_counted": "; ".join(sorted({row["name"] for row in apex_rows})),
        })
    return rows


def probability_sanity_rows(affixes: dict[str, list[dict[str, str]]]) -> list[dict[str, object]]:
    synthetic = synthetic_greater_rows(affixes)
    scenarios = sorted({(candidate["side"], candidate["sample"]) for candidate in CANDIDATES})
    rows: list[dict[str, object]] = []
    for side, sample in scenarios:
        before_pool = current_pool_for(affixes, side, sample)
        after_pool = pool_for(affixes, side, sample, synthetic)
        before_total = sum(freq(row) for row in before_pool)
        after_regular_total = sum(proposed_freq(row) for row in after_pool if row.get("synthetic_greater") != "1")
        after_greater_total = sum(proposed_freq(row) for row in after_pool if row.get("synthetic_greater") == "1")
        after_total = after_regular_total + after_greater_total
        if not before_total or not after_total or not after_regular_total:
            continue
        for row in before_pool:
            before = freq(row) / before_total
            after_existing_only = proposed_freq(row) / after_regular_total
            after_with_greater = proposed_freq(row) / after_total
            rows.append({
                "side": side,
                "sample_item": sample,
                "line": row.get("line", ""),
                "group": row.get("group", ""),
                "name": row.get("name", ""),
                "mods": ", ".join(row_mods(row)),
                "current_freq": freq(row),
                "proposed_freq": proposed_freq(row),
                "current_pool_weight": before_total,
                "after_regular_weight": after_regular_total,
                "after_greater_weight": after_greater_total,
                "after_total_weight": after_total,
                "before_per_slot": before,
                "after_per_slot_existing_only": after_existing_only,
                "after_per_slot_with_greater": after_with_greater,
                "existing_only_relative_delta": after_existing_only / before - 1 if before else 0,
                "with_greater_relative_delta": after_with_greater / before - 1 if before else 0,
            })
    return rows


def group_audit(affixes: dict[str, list[dict[str, str]]]) -> list[dict[str, str]]:
    covered = defaultdict(list)
    for c in CANDIDATES:
        for r in c["rows"]:
            covered[(c["side"], r["group"])].append(c["name"])

    audit = []
    for side in ("prefix", "suffix"):
        groups = defaultdict(list)
        for row in affixes[side]:
            if row.get("rare") == "1":
                groups[row.get("group") or "blank"].append(row)
        for group, rows in sorted(groups.items(), key=lambda kv: (int(kv[0]) if kv[0].isdigit() else 9999, kv[0])):
            top_level = max(int(r.get("level") or 0) for r in rows)
            top_rows = sorted(rows, key=lambda r: (int(r.get("level") or 0), freq(r)), reverse=True)[:4]
            apex = "; ".join(
                f"{r['name']} L{r.get('level') or 0} F{r.get('frequency') or 0} ({', '.join(row_mods(r))})"
                for r in top_rows
            )
            mods = sorted({m.split()[0].split("(")[0] for r in rows for m in row_mods(r)})
            if (side, group) in covered:
                action = "Covered by " + ", ".join(sorted(set(covered[(side, group)])))
            else:
                action = GROUP_ACTIONS.get((side, group), "Needs manual decision before implementation.")
            audit.append({
                "side": side,
                "group": group,
                "rows": str(len(rows)),
                "top_level": str(top_level),
                "mods": ", ".join(mods[:8]),
                "apex": apex,
                "action": action,
            })
    return audit


def pct(x: float) -> str:
    return f"{x * 100:.3f}%"


def md_table(headers: list[str], rows: list[list[str]]) -> str:
    out = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    out.extend("| " + " | ".join(str(v).replace("\n", " ") for v in row) + " |" for row in rows)
    return "\n".join(out)


def write_tsv(path: Path, rows: list[dict[str, object]], headers: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers, delimiter="\t", extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    affixes = load_affixes()
    chances = chance_rows(affixes)
    sanity = probability_sanity_rows(affixes)
    audit = group_audit(affixes)
    chance_headers = [
        "Greater candidate",
        "Side",
        "Group",
        "Sample item",
        "Greater weight",
        "Apex weight before",
        "Apex weight after",
        "Current pool weight",
        "After pool weight",
        "Greater per slot after",
        "Apex per slot before",
        "Apex per slot after",
        "Greater if 3 same-side slots",
        "Apex if 3 same-side slots after",
        "Greater vs apex after",
        "Ordinary affix absolute drift",
        "Apex rows counted",
        "Apex baseline",
        "Draft greater payload",
    ]
    chance_table_rows = [
        {
            "Greater candidate": c["name"],
            "Side": c["side"],
            "Group": ", ".join(sorted({r["group"] for r in c["rows"]}, key=lambda x: int(x) if x.isdigit() else 9999)),
            "Sample item": c["sample"],
            "Greater weight": c["candidate_weight"],
            "Apex weight before": c["apex_weight_before"],
            "Apex weight after": c["apex_weight_after"],
            "Current pool weight": c["before_pool_weight"],
            "After pool weight": c["after_pool_weight"],
            "Greater per slot after": pct(c["slot_chance"]),
            "Apex per slot before": pct(c["apex_slot_chance_before"]),
            "Apex per slot after": pct(c["apex_slot_chance_after"]),
            "Greater if 3 same-side slots": pct(c["item_chance"]),
            "Apex if 3 same-side slots after": pct(c["apex_item_chance"]),
            "Greater vs apex after": c["greater_vs_apex"],
            "Ordinary affix absolute drift": pct(c["ordinary_absolute_drift"]),
            "Apex rows counted": c["apex_rows_counted"],
            "Apex baseline": c["apex"],
            "Draft greater payload": c["greater"],
        }
        for c in sorted(chances, key=lambda c: (c["side"], c["sample"], c["name"]))
    ]
    write_tsv(CHANCE_TSV, chance_table_rows, chance_headers)
    sanity_headers = [
        "side",
        "sample_item",
        "line",
        "group",
        "name",
        "mods",
        "current_freq",
        "proposed_freq",
        "current_pool_weight",
        "after_regular_weight",
        "after_greater_weight",
        "after_total_weight",
        "before_per_slot",
        "after_per_slot_existing_only",
        "after_per_slot_with_greater",
        "existing_only_relative_delta",
        "with_greater_relative_delta",
    ]
    write_tsv(SANITY_TSV, sanity, sanity_headers)
    max_existing_only_delta = max((abs(float(row["existing_only_relative_delta"])) for row in sanity), default=0.0)
    max_with_greater_delta = max((abs(float(row["with_greater_relative_delta"])) for row in sanity), default=0.0)
    lines = [
        "# Rare Greater Affix Apex Audit",
        "",
        "Generated: 2026-05-19.",
        "",
        "Purpose: scan the live rare-eligible affix tables, identify every affix group that contains apex rows, and draft a complete Greater Affix candidate list with spawn odds that can be reviewed before implementation.",
        "",
        "## Method And Assumptions",
        "",
        f"- Source tables: `data/global/excel/magicprefix.txt`, `data/global/excel/magicsuffix.txt`, and `data/global/excel/itemtypes.txt`.",
        f"- Chance model uses affix level `{ALVL}` and the current live affix pools.",
        f"- The proposed frequency model scales existing affix frequencies by `{FREQ_SCALE}` and sets each Greater candidate's total eligible frequency equal to the current apex frequency it upgrades. That makes Greater exactly 10x rarer than the same apex row(s) in the final scaled table.",
        "- The script adds drafted Greater rows synthetically; no game TXT files are changed by this report.",
        "- `Greater per slot after` is the candidate's proposed Greater frequency divided by the final eligible same-side pool for the sample item.",
        f"- `If 3 same-side slots` is an exact group-blocked probability for a rare item that receives `{SLOTS}` prefix slots or `{SLOTS}` suffix slots. Real rares may receive fewer same-side slots, so actual per-item odds are lower when the item rolls fewer affixes.",
        "- The apex columns count the current best matching non-Greater row or rows for that candidate, before and after the uniform frequency scale.",
        "- Item-type eligibility uses `itype*` / `etype*` plus `itemtypes.txt` inheritance.",
        "- Multi-element or multi-scope candidates are aggregated in the chance table. Per-element odds are lower when a row represents several separate element variants.",
        "- Rows marked defer/optional are still captured in the audit so we do not forget them, but they are not first-pass Greater candidates.",
        "",
        "## Probability Sanity Check",
        "",
        f"- Existing-only relative probability delta after scaling old affixes by `{FREQ_SCALE}`: max `{max_existing_only_delta:.6%}`. This should be exactly zero apart from floating-point noise.",
        f"- Absolute ordinary-affix chance drift after adding Greater rows: max `{max_with_greater_delta:.3%}` across sampled item pools. This is the unavoidable probability mass taken by the new Greater rows.",
        f"- Full row-level sanity data is written to `{SANITY_TSV.relative_to(ROOT)}`.",
        "",
        "## Draft Greater Affix Chance Table",
        "",
        md_table(
            chance_headers,
            [
                [str(row[header]) for header in chance_headers]
                for row in chance_table_rows
            ],
        ),
        "",
        "## Complete Rare-Affix Group Coverage Audit",
        "",
        "This table is intentionally mechanical. It makes every rare-eligible prefix/suffix group visible, including groups we should defer.",
        "",
        md_table(
            ["Side", "Group", "Rows", "Top level", "Mod families", "Representative apex rows", "Greater-plan status"],
            [
                [
                    r["side"],
                    r["group"],
                    r["rows"],
                    r["top_level"],
                    r["mods"],
                    r["apex"],
                    r["action"],
                ]
                for r in audit
            ],
        ),
        "",
        "## Immediate Review Questions",
        "",
        "1. Are any apex groups incorrectly marked as deferred when they should receive a Greater candidate in Phase 2?",
        "2. Do any groups currently covered by one broad candidate need to be split by item scope, especially `group 125` skills, `group 209` caster damage/pierce, and missile-only groups?",
        "3. Are the listed odds rare enough for Phase 2, or should late Greater frequencies generally be `1` instead of `3` for high-impact affixes?",
        "4. Do any proposed Greater ranges exceed sane balance limits before implementation?",
        "",
    ]
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(OUT)


if __name__ == "__main__":
    main()
