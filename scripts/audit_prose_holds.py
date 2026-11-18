#!/usr/bin/env python3
"""Найти записи, которые называют HOLD **словами**, но не выставляют его полем.

Зачем это нужно. Два инструмента учёта читают разные вещи:

- `render_hold_inventory.py` считает структурные HOLD — массивы `holds` в JSON и
  токены `RIGHTS_HOLD` / `PUBLICATION_HOLD` / … в markdown;
- `audit_hold_coverage_gaps.py` ищет обратную ошибку — объект не приобретён, а
  `holds` пуст.

Ни один из них не видит третьего случая: запись, у которой массив `holds` пуст или
отсутствует, а сам HOLD назван в прозе — в поле `rights`, `rightsNote`, `limits`,
`downloadAccess`, `notes`. Пример из `docs/research/reformation/acquisition-manifest-v1.json`:
`"rights": "… Not reconciled: RIGHTS_UNKNOWN, RIGHTS_HOLD and PUBLICATION_HOLD on
archival JPEG reuse."` — HOLD объявлен, но ни в инвентаре, ни в HOLD-дефицитах такой
записи нет.

Скрипт отвечает только на вопрос «сколько таких записей и где они», и ничего не
утверждает о том, правильно ли они устроены. Часть из них — законная конвенция: в
`SUNO_HYMNS/data/claim-ledger-v1.json` токен `LOCATOR_HOLD` описывает состояние
**довода**, а не объекта, и полю `holds` там взяться неоткуда. Поэтому вывод — это
размер класса и его раскладка, а не список ошибок.

Периметр тот же, что у аудита HOLD-дефицитов: все JSON репозитория, кроме `.git`,
`.github`, `node_modules`, `__pycache__` и `docs/research/holds` (документы о HOLD не
должны считаться записями о HOLD).

    python3 scripts/audit_prose_holds.py
    python3 scripts/audit_prose_holds.py --summary
    python3 scripts/audit_prose_holds.py --list

Fail-open: скрипт ничего не правит и возвращает 0, даже если записи нашлись. Это
измерение, а не приговор.
"""

from __future__ import annotations

import collections
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".github", "docs/research/holds"}
HOLD_KEYS = ("holds", "hold", "activeHolds", "active_holds")

# Токены HOLD, которые в этом репозитории пишут капсом. Поиск идёт по границе слова,
# чтобы `RIGHTS_HOLD` не совпал с `RIGHTS_HOLDING` и подобным.
HOLD_TOKENS = re.compile(
    r"\b(RIGHTS_HOLD|PUBLICATION_HOLD|EVIDENCE_HOLD|ARCHIVE_HOLD|LOCATOR_HOLD|STORAGE_HOLD|ACQUISITION_HOLD)\b"
)

# Поля, в которых конвенция разрешает объяснять состояние словами.
TEXT_KEYS = (
    "rights",
    "rightsNote",
    "rightsProse",
    "rightsBasis",
    "notes",
    "note",
    "limits",
    "limit",
    "caveats",
    "qualifiers",
    "description",
    "downloadAccess",
    "intendedNextStep",
    "publicationNote",
    "holdNote",
    "why",
)


def iter_json() -> list[pathlib.Path]:
    files = []
    for path in ROOT.rglob("*.json"):
        rel = path.relative_to(ROOT)
        if any(part in SKIP_DIRS for part in rel.parts):
            continue
        files.append(path)
    return sorted(files)


def holds_of(node: dict) -> set[str] | None:
    """Структурные HOLD записи: None — поля нет вовсе, пустое множество — массив пуст."""
    for key in HOLD_KEYS:
        if key in node:
            value = node[key]
            if isinstance(value, list):
                return {str(v) for v in value if str(v).strip()}
            if isinstance(value, str):
                return {value} if value.strip() else set()
    return None


def prose_tokens(node: dict) -> set[str]:
    found: set[str] = set()
    for key in TEXT_KEYS:
        value = node.get(key)
        if isinstance(value, str):
            found |= set(HOLD_TOKENS.findall(value))
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, str):
                    found |= set(HOLD_TOKENS.findall(item))
    return found


def collect() -> list[dict]:
    rows: list[dict] = []

    def walk(node, path: str, parent_id: str | None) -> None:
        if isinstance(node, dict):
            tokens = prose_tokens(node)
            if tokens:
                structured = holds_of(node)
                if not structured:  # None (поля нет) или пустой массив
                    ident = (
                        node.get("id")
                        or node.get("source_id")
                        or node.get("sourceId")
                        or node.get("recordId")
                        or parent_id
                        or "(без id)"
                    )
                    rows.append(
                        {
                            "path": path,
                            "id": str(ident),
                            "tokens": sorted(tokens),
                            "holdsKeyPresent": structured is not None,
                            "accessState": str(node.get("accessState") or ""),
                            "publicationState": str(node.get("publicationState") or ""),
                        }
                    )
            for key, value in node.items():
                walk(value, path, node.get("id") or parent_id)
        elif isinstance(node, list):
            for value in node:
                walk(value, path, parent_id)

    for path in iter_json():
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError, OSError):
            continue
        walk(data, str(path.relative_to(ROOT)), None)
    return rows


def main(argv: list[str]) -> int:
    rows = collect()
    by_file = collections.Counter(r["path"] for r in rows)
    by_token = collections.Counter(t for r in rows for t in r["tokens"])
    with_key = sum(1 for r in rows if r["holdsKeyPresent"])

    print(
        "Записей, называющих HOLD в прозе при пустых или отсутствующих holds: "
        f"{len(rows)}"
    )
    print(
        f"  из них с полем holds (и оно пустое): {with_key}; вовсе без поля: {len(rows) - with_key}"
    )
    print("  это не список ошибок: часть токенов описывает состояние довода, а не объекта")

    if "--summary" in argv or "--list" in argv:
        print("\nпо файлам:")
        for key, value in by_file.most_common():
            print(f"  {value:4d}  {key}")
        print("\nпо токенам:")
        for key, value in by_token.most_common():
            print(f"  {value:4d}  {key}")

    if "--list" in argv:
        print("\nпо записям:")
        for row in rows:
            print(
                f"  {row['path']} | {row['id']} | {','.join(row['tokens'])} | "
                f"access={row['accessState'] or '-'} | pub={row['publicationState'] or '-'}"
            )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
