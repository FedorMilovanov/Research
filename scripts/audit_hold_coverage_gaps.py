#!/usr/bin/env python3
"""Найти записи, где объект не приобретён полностью, но HOLD не выставлен.

Это зеркало обычного аудита HOLD. Обычно ищут лишние HOLD; здесь ищут
**отсутствующие**: строка реестра объявляет `accessState` уровня
`PARTIAL_OBJECT` / `CATALOG_ONLY` / `LINK_ONLY` / `NOT_ACQUIRED`, а массив
`holds` пуст. Такая запись выглядит полностью обеспеченной, хотя объекта нет.

Второй режим (`--promotion-gaps`) ищет обратную ошибку: запись продвигается в
публикацию (`publicationState = PROMOTE`) при том, что объект не приобретён
полностью или сама запись объявляет пробел в `limits` («not collated»,
«not verified», «не сличалось»). Так выглядит `SRC-PHOS-BASIL-DSS`: `PROMOTE`,
`holds: []`, а в `limits` написано, что греческий текст не сличался.

Скрипт печатает две величины, потому что они означают разное: сколько записей
**объявляют** объём осмотра (`limits`, `inspection_scope`, `inspection_level`,
`claim_limit`) и сколько **молчат** о нём. Молчащая запись — это дефект; объявившая
неполноту словами — это вопрос конвенции, а не обмана. Разбор: 
`docs/research/holds/UNDER_ACQUIRED_WITHOUT_HOLD_TRIAGE_2026-11-18.md`.

Скрипт ничего не правит: он только считает и раскладывает по файлам. Решение о
том, какой HOLD уместен, — за владельцем, потому что неверно выставленный HOLD
расщепляет источник так же, как правка `holds` без правки прозы.

    python3 scripts/audit_hold_coverage_gaps.py
    python3 scripts/audit_hold_coverage_gaps.py --summary
    python3 scripts/audit_hold_coverage_gaps.py --promotion-gaps
"""

from __future__ import annotations

import collections
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".github", "docs/research/holds"}

NOT_FULL = {"PARTIAL_OBJECT", "CATALOG_ONLY", "LINK_ONLY", "NOT_ACQUIRED"}

# Формулировки, которыми запись сама объявляет, что доказательство неполно.
GAP_MARKERS = (
    "not collated",
    "not verified",
    "not checked",
    "not inspected",
    "not read",
    "unverified",
    "not confirmed",
    "не сличал",
    "не сверял",
    "не проверял",
)
ACCESS_KEYS = ("accessState", "access_state")
HOLD_KEYS = ("holds", "hold", "activeHolds", "active_holds")

# Поля, которыми запись сама называет, что именно она осмотрела. Схемы разные:
# `SUNO_HYMNS` пишет `limits`, `1_PETER_BOT` — `inspection_scope`/`inspection_level`
# и `claim_limit`. Запись с таким полем не молчит о пробеле, она его описывает.
DECLARATION_KEYS = ("limits", "limit", "inspection_scope", "inspection_level", "claim_limit", "caveats", "qualifiers")


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
                declared = [
                    key for key in DECLARATION_KEYS if node.get(key) not in (None, "", [], {})
                ]
                out.append(
                    {
                        "id": str(ident),
                        "accessState": access,
                        "rightsState": str(node.get("rightsState") or node.get("rights_state") or ""),
                        "publicationState": str(
                            node.get("publicationState") or node.get("publication_state") or ""
                        ),
                        "path": path,
                        "declaredBy": declared,
                    }
                )
        for key, value in node.items():
            walk(value, path, out, node.get("id") or parent_id)
    elif isinstance(node, list):
        for value in node:
            walk(value, path, out, parent_id)


def limit_text(node: dict) -> str:
    parts = []
    for key in ("limits", "limit", "caveats", "qualifiers", "notes"):
        value = node.get(key)
        if isinstance(value, str):
            parts.append(value)
        elif isinstance(value, list):
            parts.extend(str(v) for v in value if isinstance(v, (str, int, float)))
    return " ".join(parts).lower()


def build_promotion_gaps() -> list[dict]:
    """Записи, продвигаемые в публикацию при объявленном пробеле в доказательствах."""
    rows: list[dict] = []
    for path in iter_json():
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError):
            continue
        rel = str(path.relative_to(ROOT))

        def walk_pg(node, parent_id: str | None) -> None:
            if isinstance(node, dict):
                pub = str(
                    node.get("publicationState") or node.get("publication_state") or ""
                ).strip().upper()
                if pub == "PROMOTE":
                    access = next(
                        (
                            str(node[k]).strip().upper()
                            for k in ACCESS_KEYS
                            if isinstance(node.get(k), str)
                        ),
                        "",
                    )
                    text = limit_text(node)
                    markers = sorted({m for m in GAP_MARKERS if m in text})
                    if access in NOT_FULL or markers:
                        rows.append(
                            {
                                "path": rel,
                                "id": str(
                                    node.get("id")
                                    or node.get("source_id")
                                    or parent_id
                                    or "(без id)"
                                ),
                                "accessState": access,
                                "holds": sorted(holds_of(node) or []),
                                "gapMarkers": markers,
                            }
                        )
                for key, value in node.items():
                    walk_pg(value, node.get("id") or parent_id)
            elif isinstance(node, list):
                for value in node:
                    walk_pg(value, parent_id)

        walk_pg(data, None)
    return rows


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
    if "--promotion-gaps" in argv:
        gaps = build_promotion_gaps()
        print(f"Записей PROMOTE с объявленным пробелом в доказательствах: {len(gaps)}")
        for row in gaps:
            marks = ", ".join(row["gapMarkers"]) or "—"
            holds = ", ".join(row["holds"]) or "нет"
            print(
                f"  {row['path']} | {row['id']} | access={row['accessState'] or '-'} | "
                f"holds={holds} | маркеры: {marks}"
            )
        return 0

    result = build()
    rows = result["rows"]
    declared = [r for r in rows if r["declaredBy"]]
    silent = [r for r in rows if not r["declaredBy"]]
    print(f"Записей «объект не приобретён, HOLD не выставлен»: {len(rows)}")
    print(f"  из них сами называют объём осмотра (limits/inspection_scope/claim_limit): {len(declared)}")
    print(f"  молчат о нём совсем: {len(silent)}")
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
        if silent:
            print("\nмолчащие записи:")
            for row in silent:
                print(f"  {row['path']} | {row['id']} | {row['accessState']}")
        print("\nполя, которыми записи объявляют объём осмотра:")
        seen = collections.Counter(k for r in declared for k in r["declaredBy"])
        for key, value in seen.most_common():
            print(f"  {key}: {value}")
        if result["unreadable"]:
            print(f"\nнечитаемых JSON: {len(result['unreadable'])}")
        return 0
    for row in rows:
        mark = "declared" if row["declaredBy"] else "SILENT"
        print(
            f"{row['path']} | {row['id']} | {row['accessState']} | rights={row['rightsState'] or '-'} | "
            f"pub={row['publicationState'] or '-'} | {mark}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
