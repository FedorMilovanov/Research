#!/usr/bin/env python3
"""Проверка пар «Docs-объект + коммит» для тринадцати зеркал «ИСКУПЛЕНИЕ».

Зачем: сверка 2026-11-18 (`ИСКУПЛЕНИЕ/evidence/DOC_MIRRORS_EXPORT_TAILS_2026-11-18.md`)
установила для каждого зеркала коммит, чей текст в нём лежит. Пока это знание
живёт только в прозе, следующий круг снова начнёт угадывать по имени объекта и
по `modifiedTime`. Здесь оно лежит в `docs/research/data/drive-mirror-pairs.json` и
проверяется без сети: всё, что нужно, есть в Git.

Что проверяется (структурные ошибки — ненулевой код):

1. реестр разбирается, `schema` тот, зеркал ровно тринадцать, id не повторяются;
2. у каждой записи есть файл по указанному пути;
3. `revision` резолвится в коммит, коммит содержит этот путь и является предком
   `HEAD` (иначе пара «объект + коммит» указывает в другую историю);
4. записанные `bytes_now`/`md5_now` совпадают с деревом на дату съёма.

Что печатается как сведения, а не приговор: сколько ревизий файла прошло после
названного коммита и на сколько байт вырос файл. Это число и есть отставание
зеркала, и оно обязано расти — падать из-за него нельзя.

    python3 -B scripts/check_drive_mirror_pairs.py
    python3 -B scripts/check_drive_mirror_pairs.py --check
    python3 -B scripts/check_drive_mirror_pairs.py --summary   # одна строка

`07_` записан без `revision`: его текст не попадал в Git ни разу, и это
установлено, а не пропущено (`RIGHTS_MIRROR_07_STOP_POINT_2026-11-18.md`).
"""

from __future__ import annotations

import hashlib
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "docs" / "research" / "data" / "drive-mirror-pairs.json"
EXPECTED_MIRRORS = 13


def git(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True)


def load() -> tuple[dict, list[str]]:
    errors: list[str] = []
    if not REGISTRY.exists():
        return {}, [f"нет реестра {REGISTRY.relative_to(ROOT)}"]
    try:
        data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return {}, [f"реестр не разбирается: {exc}"]

    if data.get("schema") != 1:
        errors.append(f"schema={data.get('schema')!r}, ожидался 1")
    mirrors = data.get("mirrors") or []
    if len(mirrors) != EXPECTED_MIRRORS:
        errors.append(f"зеркал {len(mirrors)}, ожидалось {EXPECTED_MIRRORS}")

    seen_mirror: set[str] = set()
    seen_id: set[str] = set()
    for entry in mirrors:
        tag = entry.get("mirror") or "?"
        if tag in seen_mirror:
            errors.append(f"{tag}: зеркало записано дважды")
        seen_mirror.add(tag)
        drive_id = entry.get("drive_id") or ""
        if not drive_id:
            errors.append(f"{tag}: пустой drive_id")
        elif drive_id in seen_id:
            errors.append(f"{tag}: drive_id повторяется ({drive_id})")
        seen_id.add(drive_id)
        if entry.get("kind") not in {"docs", "file"}:
            errors.append(f"{tag}: kind={entry.get('kind')!r}, ожидалось docs или file")
    return data, errors


def check_entry(entry: dict) -> tuple[list[str], dict]:
    """Структурные ошибки записи и сведения о её дрейфе."""
    tag = entry.get("mirror", "?")
    errors: list[str] = []
    info: dict = {"mirror": tag, "revision": entry.get("revision") or "—"}

    path = ROOT / (entry.get("path") or "")
    if not path.exists():
        errors.append(f"{tag}: нет файла {entry.get('path')}")
        return errors, info

    current = path.read_bytes()
    info["bytes_now"] = len(current)
    info["bytes_at_check"] = entry.get("bytes_now")
    info["grew_since_check"] = len(current) - int(entry.get("bytes_now") or len(current))
    if hashlib.md5(current).hexdigest() != entry.get("md5_now"):
        info["md5_drift"] = True

    revision = entry.get("revision")
    if not revision:
        info["behind"] = "—"
        info["revision_bytes"] = None
        return errors, info

    rev = git("rev-parse", "--verify", f"{revision}^{{commit}}")
    if rev.returncode != 0:
        errors.append(f"{tag}: коммит {revision} не найден")
        return errors, info
    full = rev.stdout.strip()
    info["revision"] = full[:8]

    blob = git("rev-parse", "--verify", f"{full}:{entry['path']}")
    if blob.returncode != 0:
        errors.append(f"{tag}: коммит {full[:8]} не содержит {entry['path']}")
        return errors, info

    ancestor = git("merge-base", "--is-ancestor", full, "HEAD")
    if ancestor.returncode != 0:
        errors.append(f"{tag}: коммит {full[:8]} не предок HEAD")

    if entry.get("kind") == "file":
        md5 = hashlib.md5(git("cat-file", "blob", f"{full}:{entry['path']}").stdout.encode()).hexdigest()
        info["blob_md5"] = md5
        info["byte_identical"] = md5 == entry.get("md5_now")

    info["revision_bytes"] = int(git("cat-file", "-s", f"{full}:{entry['path']}").stdout.strip() or 0)

    after = git("rev-list", "--count", f"{full}..HEAD", "--", entry["path"])
    info["behind"] = int(after.stdout.strip() or 0) if after.returncode == 0 else "?"
    return errors, info


def main(argv: list[str]) -> int:
    data, errors = load()
    mode_check = "--check" in argv
    mode_summary = "--summary" in argv

    infos: list[dict] = []
    if data:
        for entry in data.get("mirrors", []):
            entry_errors, info = check_entry(entry)
            errors.extend(entry_errors)
            infos.append(info)

    if mode_summary:
        behind = [i["behind"] for i in infos if isinstance(i.get("behind"), int)]
        stale = sum(1 for i in infos if isinstance(i.get("behind"), int) and i["behind"] > 0)
        print(
            f"DRIVE MIRROR PAIRS: {len(infos)} записей, названных коммитов "
            f"{sum(1 for i in infos if i['revision'] != '—')}, "
            f"отстают {stale} (максимум {max(behind) if behind else 0} ревизий), "
            f"структурных ошибок {len(errors)}"
        )
        return 1 if errors else 0

    if not mode_check or errors:
        print(f"{'зеркало':<8} {'ревизия':<10} {'позади':>7} {'было B':>8} {'стало B':>8}  примечание")
        for info in infos:
            tag = info["mirror"]
            note = ""
            if info.get("byte_identical"):
                note = "md5 блоба равен зеркалу"
            elif info.get("md5_drift"):
                note = "файл изменился после съёма"
            elif isinstance(info.get("behind"), int) and info["behind"] == 0:
                note = "файл не менялся после ревизии"
            print(
                f"{tag:<8} {info['revision']:<10} {str(info.get('behind', '—')):>7} "
                f"{str(info.get('bytes_at_check', '—')):>8} {str(info.get('bytes_now', '—')):>8}  {note}"
            )

    for error in errors:
        print(f"[FAIL] {error}", file=sys.stderr)
    if errors:
        return 1
    if mode_check:
        print(f"DRIVE MIRROR PAIRS: OK ({len(infos)} записей, структурных ошибок нет)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
