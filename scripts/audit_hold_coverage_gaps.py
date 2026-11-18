#!/usr/bin/env python3
"""Найти записи, где объект не приобретён полностью, но HOLD не выставлен.

Это зеркало обычного аудита HOLD. Обычно ищут лишние HOLD; здесь ищут
**отсутствующие**: строка реестра объявляет `accessState` уровня
`PARTIAL_OBJECT` / `CATALOG_ONLY` / `LINK_ONLY` / `NOT_ACQUIRED`, а массив
`holds` пуст. Такая запись выглядит полностью обеспеченной, хотя объекта нет.

Скрипт ничего не правит: он только считает и раскладывает по файлам. Решение о
том, какой HOLD уместен, — за владельцем, потому что неверно выставленный HOLD
расщепляет источник так же, как правка `holds` без правки прозы.

    python3 scripts/audit_hold_coverage_gaps.py
    python3 scripts/audit_hold_coverage_gaps.py --summary
"""

from __future__ import annotations

import collections
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".github", "docs/research/holds"}

NOT_FULL = {"PARTIAL_OBJECT", "CATALOG_ONLY", "LINK_ONLY", "NOT_ACQUIRED"}
ACCESS_KEYS = ("accessState", "access_state")
HOLD_KEYS = ("holds", "hold", "activeHolds", "active_holds")


def iter_json() -> list[pathlib.Path]:
    files = []
    for path in ROOT.rglob("*.json"):
        rel = path.relative_to(ROOT)
        if any(part in SKIP_DIRS for part in rel.parts):
            continue
        if rel.parts and rel.parts[0] in SKIP_DIRS:
            continue
        files.append(path)
    return sorted(files)


def holds_of(node: dict) -> set[str] | None:
    for key in HOLD_KEYS:
        if key in node:
            value = node[key]
            if isinstance(value, list):
                return {str(v) for v in value if str(v).strip()}
            if isinstance(value, str):
                return {value} if value.strip() else set()
    return None


def walk(node, path: str, out: list[dict], parent_id: str | None = None) -> None:
    if isinstance(node, dict):
        access = None
        for key in ACCESS_KEYS:
            if isinstance(node.get(key), str):
                access = node[key].strip().upper()
                break
        if access in NOT_FULL:
            holds = holds_of(node)
            if holds is not None and not holds:
                ident = (
                    node.get("id")
                    or node.get("source_id")
                    or node.get("sourceId")
                    or node.get("objectId")
                    or node.get("recordId")
                    or parent_id
                    or "(без id)"
                )
                out.append(
                    {
                        "id": str(ident),
                        "accessState": access,
                        "rightsState": str(node.get("rightsState") or node.get("rights_state") or ""),
                        "publicationState": str(
                            node.get("publicationState") or node.get("publication_state") or ""
                        ),
                        "path": path,
                    }
                )
        for key, value in node.items():
            walk(value, path, out, node.get("id") or parent_id)
    elif isinstance(node, list):
        for value in node:
            walk(value, path, out, parent_id)


def build() -> dict:
    rows: list[dict] = []
    unreadable: list[str] = []
    for path in iter_json():
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError):
            unreadable.append(str(path.relative_to(ROOT)))
            continue
        walk(data, str(path.relative_to(ROOT)), rows)

    by_file = collections.Counter(r["path"] for r in rows)
    by_access = collections.Counter(r["accessState"] for r in rows)
    by_rights = collections.Counter(r["rightsState"] or "(не задано)" for r in rows)
    by_publication = collections.Counter(r["publicationState"] or "(не задано)" for r in rows)
    return {
        "rows": rows,
        "unreadable": unreadable,
        "byFile": dict(by_file.most_common()),
        "byAccess": dict(by_access.most_common()),
        "byRights": dict(by_rights.most_common()),
        "byPublication": dict(by_publication.most_common()),
    }


def main(argv: list[str]) -> int:
    result = build()
    rows = result["rows"]
    print(f"Записей «объект не приобретён, HOLD не выставлен»: {len(rows)}")
    print(f"Файлов с такими записями: {len(result['byFile'])}")
    if "--summary" in argv:
        print("\nпо accessState:")
        for key, value in result["byAccess"].items():
            print(f"  {key}: {value}")
        print("\nпо rightsState:")
        for key, value in result["byRights"].items():
            print(f"  {key}: {value}")
        print("\nпо publicationState:")
        for key, value in result["byPublication"].items():
            print(f"  {key}: {value}")
        print("\nпо файлам:")
        for key, value in result["byFile"].items():
            print(f"  {value:4d}  {key}")
        if result["unreadable"]:
            print(f"\nнечитаемых JSON: {len(result['unreadable'])}")
        return 0
    for row in rows:
        print(
            f"{row['path']} | {row['id']} | {row['accessState']} | rights={row['rightsState'] or '-'} | "
            f"pub={row['publicationState'] or '-'}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
