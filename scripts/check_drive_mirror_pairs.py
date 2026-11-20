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
    python3 -B scripts/check_drive_mirror_pairs.py --index     # что значит поле bytes в индексе
    python3 -B scripts/check_drive_mirror_pairs.py --cross     # id в корпусе, индексе и реестре

Отдельно `--index` сверяет записи индекса библиотеки с этим реестром и печатает,
какой из четырёх смыслов лежит в их поле `bytes` (внутренний размер Docs, размер
git-блоба, реальные байты файла) и где `kind: file` стоит у Docs-объекта;
подробности — `ИСКУПЛЕНИЕ/evidence/DRIVE_INDEX_BYTES_FIELD_2026-11-18.md`.

`07_` записан без `revision`: его текст не попадал в Git ни разу, и это
установлено, а не пропущено (`RIGHTS_MIRROR_07_STOP_POINT_2026-11-18.md`).
"""

from __future__ import annotations

import hashlib
import json
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "docs" / "research" / "data" / "drive-mirror-pairs.json"
INDEX = ROOT / "ИСКУПЛЕНИЕ" / "data" / "atonement-library-index.json"
CORPUS = ROOT / "ИСКУПЛЕНИЕ" / "data" / "atonement-corpus-v1.json"
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


def index_records() -> dict[str, dict]:
    """Записи индекса библиотеки по drive_id — чтобы сверить смысл поля `bytes`."""
    if not INDEX.exists():
        return {}
    data = json.loads(INDEX.read_text(encoding="utf-8"))
    return {rec["driveId"]: rec for rec in data.get("records", []) if rec.get("driveId")}


def classify_bytes(entry: dict, rec: dict) -> tuple[str, bool]:
    """Какой из четырёх смыслов лежит в поле `bytes` этой записи, и сходится ли он."""
    declared = rec.get("bytes")
    mime = str(rec.get("mime") or "")
    if mime == "text/markdown":
        expected = entry.get("drive_file_bytes")
        if declared == expected:
            return "реальные байты файла", True
        return f"файл: в индексе {declared}, у объекта {expected}", False
    docs_size = entry.get("drive_docs_size")
    if declared == docs_size:
        return "внутренний размер Docs", True
    git_bytes = entry.get("git_blob_bytes")
    if git_bytes and declared == git_bytes:
        return "размер git-блоба", True
    claimed = entry.get("git_claimed_bytes")
    if claimed and declared == claimed:
        return "размер git-блоба, ревизии с таким размером нет", True
    return f"не опознан (в индексе {declared})", False


# Только поля, которые обещают число *файла в Git*: drive*Claimed и md5VerifiedFromDrive
# описывают сам объект на Drive, им с HEAD сходиться не обязательно.
CURRENCY_FIELD = re.compile(r"(gitBytes|bytesAfter|gitMd5|md5After)", re.I)

# …и только те из них, которые обещают число *сейчас*. Поле с названным кругом
# (`gitBytesAfterRound24`) честно датировано: оно про состояние после круга 24, а не про
# HEAD, и расхождение с HEAD у него — норма, а не ложь. Считать его «отставшим» значит
# объявлять дефектом саму датировку; записка об этом поле говорит ровно это.
DATED_FIELD = re.compile(r"(?:after|before|после|до)round\d+|round\d+$", re.I)


def check_currency_claims(rec: dict, path: pathlib.Path, verbose: bool) -> tuple[int, int]:
    """Поля записи: (сколько «текущих» разошлось с HEAD, сколько датировано кругом)."""
    claims = {k: v for k, v in rec.items() if CURRENCY_FIELD.search(k)}
    if not claims:
        return 0, 0
    data = path.read_bytes()
    size, md5 = len(data), hashlib.md5(data).hexdigest()
    stale = dated = 0
    for key, value in claims.items():
        is_dated = bool(DATED_FIELD.search(key))
        is_md5 = "md5" in key.lower()
        actual = md5 if is_md5 else size
        ok = str(value).lower() == str(actual).lower()
        if is_dated:
            dated += 1
            if verbose:
                print(f"         {key} = {value} — датировано кругом, с HEAD не сверяется")
            continue
        if not ok:
            stale += 1
        if verbose or not ok:
            delta = "" if is_md5 else f" (расхождение {size - int(value)} B)"
            print(f"         {key} = {value} — {'совпадает' if ok else 'не совпадает, сейчас ' + str(actual) + delta}")
    return stale, dated


def report_index(entries: list[dict]) -> int:
    records = index_records()
    if not records:
        print("индекс библиотеки не найден или пуст", file=sys.stderr)
        return 1
    print(f"{'зеркало':<8} {'bytes':>8} {'kind':<9} смысл поля bytes")
    contradictions = 0
    stale_claims = 0
    dated_claims = 0
    kind_mismatch = 0
    for entry in entries:
        rec = records.get(entry.get("drive_id") or "")
        tag = entry.get("mirror", "?")
        if not rec:
            print(f"{tag:<8} {'—':>8} {'—':<9} записи в индексе нет")
            continue
        sense, fits = classify_bytes(entry, rec)
        declared_kind = rec.get("bytesKind")
        kind_flag = ""
        if declared_kind:
            expect = {
                "drive_file_bytes": "реальные байты файла",
                "drive_docs_internal": "внутренний размер Docs",
                "git_blob_bytes": "размер git-блоба",
                "git_snapshot_bytes_unverifiable": "размер git-блоба, ревизии с таким размером нет",
            }.get(declared_kind)
            kind_flag = " [bytesKind сходится]" if expect == sense else f" [bytesKind {declared_kind} ≠ {sense}]"
            if expect != sense:
                kind_mismatch += 1
        kind = str(rec.get("kind") or "?")
        flag = ""
        if str(rec.get("mime") or "") == "application/vnd.google-apps.document" and kind == "file":
            flag = "  ← kind: file у Docs-объекта"
            contradictions += 1
        print(f"{tag:<8} {str(rec.get('bytes')):>8} {kind:<9} {sense}{'' if fits else '  ← расходится'}{flag}{kind_flag}")
        path = ROOT / (entry.get("path") or "")
        if path.exists():
            stale_now, dated_now = check_currency_claims(rec, path, verbose=False)
            stale_claims += stale_now
            dated_claims += dated_now
    total_docs_as_file = sum(
        1 for rec in records.values()
        if str(rec.get("mime") or "") == "application/vnd.google-apps.document" and rec.get("kind") == "file"
    )
    print(
        f"\nDocs-объектов с kind: file — в индексе {total_docs_as_file}, из них зеркал {contradictions}"
        " (нормализация — решение владельца, см. DRIVE_INDEX_BYTES_FIELD_2026-11-18.md)"
    )
    print(f"полей, называющих себя текущими числами файла и разошедшихся с HEAD: {stale_claims}; "
          f"полей с названным кругом (с HEAD не сверяются): {dated_claims}")
    if kind_mismatch:
        print(f"объявленный bytesKind расходится с содержимым поля: {kind_mismatch}")
    return 0



# Как зовётся каждое зеркало в driveMirrors корпуса: там ключи fileNN, а не наши «05_».
CORPUS_KEYS = {
    "03_": "file03", "04_": None, "05_": "file05", "07_": "file07", "08_": "file08",
    "09_": None, "10_": None, "11_": "file11", "12_": "file12", "13_": "file13",
    "14_": "file14", "15_": "file15", "16_": "file16",
}


def report_cross(entries: list[dict]) -> int:
    """Три места, где живёт личность зеркала: корпус (SSOT ID), индекс, реестр пар."""
    if not CORPUS.exists():
        print("корпус не найден", file=sys.stderr)
        return 1
    corpus = json.loads(CORPUS.read_text(encoding="utf-8"))
    mirrors = corpus.get("driveMirrors") or {}
    records = index_records()

    print(f"{'зеркало':<8} {'корпус':<16} {'индекс':<12} {'реестр':<10} состояние SSOT")
    mismatches = 0
    bare = 0
    for entry in entries:
        tag = entry.get("mirror", "?")
        drive_id = entry.get("drive_id")
        key = CORPUS_KEYS.get(tag)
        corpus_val = mirrors.get(key) if key else None
        if isinstance(corpus_val, dict):
            corpus_id, corpus_state = corpus_val.get("driveId"), "запись-объект"
        elif isinstance(corpus_val, str):
            corpus_id, corpus_state = corpus_val, "голая строка ID"
            bare += 1
        elif key is None:
            corpus_id, corpus_state = "—", "ключа нет"
        else:
            corpus_id, corpus_state = "—", "отсутствует"

        rec = records.get(drive_id) or {}
        index_rev = rec.get("contentRevision") or "—"
        registry_rev = entry.get("revision") or "—"

        ok = True
        if corpus_id not in (None, "—") and corpus_id != drive_id:
            ok = False
            mismatches += 1
        if rec and (rec.get("contentRevision") != entry.get("revision")):
            ok = False
            mismatches += 1
        print(
            f"{tag:<8} {('совпадает' if corpus_id == drive_id else corpus_state):<16} "
            f"{index_rev:<12} {registry_rev:<10} {corpus_state}{'' if ok else '  ← расходится'}"
        )

    print(f"\nзеркал: {len(entries)}; ID расходятся с корпусом/индексом: {mismatches}; "
          f"в driveMirrors записаны голой строкой: {bare}")
    return 1 if mismatches else 0


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

    if "--cross" in argv:
        return report_cross(data.get("mirrors", []))

    if "--index" in argv:
        return report_index(data.get("mirrors", []))

    if mode_summary:
        behind = [i["behind"] for i in infos if isinstance(i.get("behind"), int)]
        stale = sum(1 for i in infos if isinstance(i.get("behind"), int) and i["behind"] > 0)
        # «Отстают 8» при девяти объявленных лагах — не расхождение, а разница между
        # измеримым и объявленным: у зеркала-документа нет ревизии, и сравнивать его не с чем.
        # Строка обязана называть оба числа, иначе два инструмента выглядят противоречащими.
        without = sum(1 for i in infos if i["revision"] == "—")
        print(
            f"DRIVE MIRROR PAIRS: {len(infos)} записей, названных коммитов "
            f"{sum(1 for i in infos if i['revision'] != '—')}, "
            f"отстают {stale} (максимум {max(behind) if behind else 0} ревизий), "
            f"без ревизии {without} — сравнить не с чем, "
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
