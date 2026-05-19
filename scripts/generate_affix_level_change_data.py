#!/usr/bin/env python3
"""Export proposed Phase 1 affix level and levelreq compression data."""

from __future__ import annotations

import csv
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXCEL = ROOT / "data" / "global" / "excel"
OUT = ROOT / "docs" / "affix-level-requirement-changes-2026-05-19.tsv"


def round_half_up(value: float) -> int:
    return math.floor(value + 0.5)


def parse_int(value: str) -> int | None:
    value = (value or "").strip()
    if value == "":
        return None
    try:
        return int(value)
    except ValueError:
        return None


def compressed_level(value: str, in_scope: bool) -> str:
    original = parse_int(value)
    if original is None:
        return value
    if not in_scope:
        return str(original)
    return str(max(1, round_half_up(original * 0.70)))


def compressed_maxlevel(value: str, new_level: str, in_scope: bool) -> str:
    original = parse_int(value)
    if original is None:
        return value
    if not in_scope:
        return str(original)
    new_level_int = parse_int(new_level) or 1
    return str(max(new_level_int, round_half_up(original * 0.70)))


def compressed_levelreq(value: str, in_scope: bool) -> str:
    original = parse_int(value)
    if original is None:
        return value
    if original == 0:
        return "0"
    if not in_scope:
        return str(original)
    return str(max(1, round_half_up(original * 0.85)))


def delta(original: str, proposed: str) -> str:
    old = parse_int(original)
    new = parse_int(proposed)
    if old is None or new is None:
        return ""
    return str(new - old)


def mods(row: dict[str, str]) -> str:
    parts: list[str] = []
    for idx in range(1, 4):
        code = row.get(f"mod{idx}code", "")
        if not code:
            continue
        param = row.get(f"mod{idx}param", "")
        mn = row.get(f"mod{idx}min", "")
        mx = row.get(f"mod{idx}max", "")
        if param:
            parts.append(f"{code}({param}) {mn}-{mx}".strip())
        else:
            parts.append(f"{code} {mn}-{mx}".strip())
    return "; ".join(parts)


def codes(row: dict[str, str], prefix: str, count: int) -> str:
    return ", ".join(row.get(f"{prefix}{idx}", "") for idx in range(1, count + 1) if row.get(f"{prefix}{idx}", ""))


def process_table(filename: str, side: str) -> list[dict[str, str]]:
    path = EXCEL / filename
    rows: list[dict[str, str]] = []
    with path.open(newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for line, row in enumerate(reader, start=2):
            in_scope = row.get("rare", "") == "1"
            new_level = compressed_level(row.get("level", ""), in_scope)
            new_maxlevel = compressed_maxlevel(row.get("maxlevel", ""), new_level, in_scope)
            new_levelreq = compressed_levelreq(row.get("levelreq", ""), in_scope)
            rows.append(
                {
                    "side": side,
                    "source_file": filename,
                    "line": str(line),
                    "name": row.get("name", ""),
                    "description": row.get("* Description", ""),
                    "spawnable": row.get("spawnable", ""),
                    "rare": row.get("rare", ""),
                    "phase1_scope": "yes" if in_scope else "no",
                    "group": row.get("group", ""),
                    "frequency": row.get("frequency", ""),
                    "level_before": row.get("level", ""),
                    "level_after": new_level,
                    "level_delta": delta(row.get("level", ""), new_level),
                    "maxlevel_before": row.get("maxlevel", ""),
                    "maxlevel_after": new_maxlevel,
                    "maxlevel_delta": delta(row.get("maxlevel", ""), new_maxlevel),
                    "levelreq_before": row.get("levelreq", ""),
                    "levelreq_after": new_levelreq,
                    "levelreq_delta": delta(row.get("levelreq", ""), new_levelreq),
                    "mods": mods(row),
                    "itypes": codes(row, "itype", 7),
                    "etypes": codes(row, "etype", 5),
                }
            )
    return rows


def main() -> None:
    rows = process_table("magicprefix.txt", "prefix") + process_table("magicsuffix.txt", "suffix")
    headers = [
        "side",
        "source_file",
        "line",
        "name",
        "description",
        "spawnable",
        "rare",
        "phase1_scope",
        "group",
        "frequency",
        "level_before",
        "level_after",
        "level_delta",
        "maxlevel_before",
        "maxlevel_after",
        "maxlevel_delta",
        "levelreq_before",
        "levelreq_after",
        "levelreq_delta",
        "mods",
        "itypes",
        "etypes",
    ]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers, delimiter="\t", extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
    print(OUT)


if __name__ == "__main__":
    main()
