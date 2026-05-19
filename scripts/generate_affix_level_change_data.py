#!/usr/bin/env python3
"""Export proposed Phase 1 affix level and levelreq compression data."""

from __future__ import annotations

import csv
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXCEL = ROOT / "data" / "global" / "excel"
OUT = ROOT / "docs" / "affix-level-requirement-changes-2026-05-19.tsv"
TOP_SPLIT_OUT = ROOT / "docs" / "affix-top-split-preview-2026-05-19.tsv"


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


def preserved_maxlevel(value: str) -> str:
    original = parse_int(value)
    if original is None:
        return value
    return str(original)


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
            new_maxlevel = preserved_maxlevel(row.get("maxlevel", ""))
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
    write_top_split_preview()
    print(OUT)


def write_top_split_preview() -> None:
    import audit_rare_affix_apexes as audit

    affixes = audit.load_affixes()
    seen: set[tuple[str, str]] = set()
    preview_rows: list[dict[str, str]] = []
    for candidate in audit.CANDIDATES:
        for item_type in sorted(audit.ITEMTYPES):
            scoped_candidate = dict(candidate)
            scoped_candidate["sample"] = item_type
            for row in audit.apex_rows_for(affixes, scoped_candidate):
                key = (candidate["side"], row["line"])
                if key in seen:
                    continue
                seen.add(key)
                original_level = row.get("level", "")
                original_levelreq = row.get("levelreq", "")
                original_frequency = row.get("frequency", "")
                early_frequency = ""
                original_freq_int = parse_int(original_frequency)
                if original_freq_int is not None:
                    early_frequency = str(max(1, round_half_up(original_freq_int / 2)))
                early_level = compressed_level(original_level, True)
                early_maxlevel = ""
                original_level_int = parse_int(original_level)
                if original_level_int is not None:
                    early_maxlevel = str(max(1, original_level_int - 1))
                compressed_req = compressed_levelreq(original_levelreq, True)
                base = {
                    "side": candidate["side"],
                    "source_file": "magicprefix.txt" if candidate["side"] == "prefix" else "magicsuffix.txt",
                    "source_line": row["line"],
                    "candidate_id": candidate["id"],
                    "candidate": candidate["name"],
                    "name": row.get("name", ""),
                    "group": row.get("group", ""),
                    "mods": mods(row),
                    "itypes": codes(row, "itype", 7),
                    "etypes": codes(row, "etype", 5),
                    "level_before": original_level,
                    "levelreq_before": original_levelreq,
                    "maxlevel_before": row.get("maxlevel", ""),
                    "frequency_before": original_frequency,
                }
                preview_rows.append({
                    **base,
                    "operation": "convert_existing_to_early",
                    "level_after": early_level,
                    "levelreq_after": compressed_req,
                    "maxlevel_after": early_maxlevel,
                    "frequency_after": early_frequency,
                })
                preview_rows.append({
                    **base,
                    "operation": "add_late_duplicate",
                    "level_after": original_level,
                    "levelreq_after": compressed_req,
                    "maxlevel_after": row.get("maxlevel", ""),
                    "frequency_after": original_frequency,
                })
    headers = [
        "side",
        "source_file",
        "source_line",
        "candidate_id",
        "candidate",
        "operation",
        "name",
        "group",
        "level_before",
        "level_after",
        "levelreq_before",
        "levelreq_after",
        "maxlevel_before",
        "maxlevel_after",
        "frequency_before",
        "frequency_after",
        "mods",
        "itypes",
        "etypes",
    ]
    with TOP_SPLIT_OUT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers, delimiter="\t", extrasaction="ignore")
        writer.writeheader()
        writer.writerows(preview_rows)


if __name__ == "__main__":
    main()
