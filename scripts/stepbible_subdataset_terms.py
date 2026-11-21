#!/usr/bin/env python3
"""Права по подкаталогам STEPBible: что говорит сам архив, а не репозиторий целиком.

Зачем: очередь кандидатов записывает права STEPBible как «dataset-specific;
verify each subdataset». Пока это одна строка, проверить её нельзя: неизвестно,
сколько подкаталогов, чем они различаются и где условия меняются. Архив
зафиксирован коммитом и SHA-256, значит вопрос сводится к разбору имён и
единственного README, а не к веб-поиску.

Скрипт не решает права. Он перечисляет, что заявлено внутри архива, и оставляет
решение владельцу: лицензия в имени файла — утверждение распространителя,
а не разрешение на публикацию.

    # генерация (нужен архив, скачанный по закреплённому URL)
    curl -sSLo /tmp/stepbible.zip https://codeload.github.com/STEPBible/STEPBible-Data/zip/b86d26cdb1f51729e73b5b4eb7f7ccadc5dfba39
    python3 scripts/stepbible_subdataset_terms.py --zip /tmp/stepbible.zip --write

    # гейт: сверка записанного JSON без сети и без архива
    python3 scripts/stepbible_subdataset_terms.py --check
"""

from __future__ import annotations

import argparse
import collections
import hashlib
import json
import pathlib
import re
import sys
import zipfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT_JSON = ROOT / "data" / "stepbible-subdataset-terms-2026-11-18.json"
REPRO_JSON = ROOT / "data" / "official-core-datasets-reproducibility-2026-11-18.json"

# Закреплённый вход: коммит неподвижен, размер и SHA-256 сняты 2026-11-18.
PIN = {
    "repository": "STEPBible/STEPBible-Data",
    "commit": "b86d26cdb1f51729e73b5b4eb7f7ccadc5dfba39",
    "url": "https://codeload.github.com/STEPBible/STEPBible-Data/zip/b86d26cdb1f51729e73b5b4eb7f7ccadc5dfba39",
    "bytes": 100920275,
    "sha256": "6845fa9660c62301a0eec38c009ca34ef82647a9737529d8c56ac45d35182df0",
}

# Токены лицензий, которые STEPBible пишет прямо в имя файла.
TOKEN_RE = re.compile(r"CC[ -]BY(?:[ -]SA|[ -]NC)?", re.IGNORECASE)

# Подкаталоги, о которых нужно сказать отдельно: там условия отличаются от
# базового CC BY 4.0, заявленного в README.
NOTES = {
    "Tagged-Bibles/TTESV": (
        "CC BY-NC: некоммерческая лицензия на разметку ESV. Сам текст ESV — "
        "© Crossway, и разметка не даёт прав на текст; для проекта это "
        "ограничение на использование, а не на хранение."
    ),
    "Tagged-Bibles/Arabic Bibles": (
        "CC BY-SA: share-alike. Производные разметки обязаны распространяться "
        "на тех же условиях — единственный share-alike подкаталог в архиве."
    ),
    "Lexicons": (
        "Содержит TFLSJ (полный LSJ) и TBESG (на основе Abbott-Smith): README "
        "говорит, что «much of the data is based on other publically licenced "
        "sources». CC BY 4.0 заявлен на форматирование и разметку; права на "
        "исходные словари этим не подтверждены."
    ),
}


def digest(path: pathlib.Path) -> tuple[int, str]:
    h = hashlib.sha256()
    total = 0
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
            total += len(chunk)
    return total, h.hexdigest()


def readme_claim(zf: zipfile.ZipFile, root: str) -> dict:
    raw = zf.read(f"{root}/README.md").decode("utf-8", "replace")
    first = raw.splitlines()[0].strip()
    has_cc_by = "CC BY 4.0" in first or "CC BY 4.0" in raw
    credit = re.search(r"Credit it\*{0,2}\s*to\s+\"([^\"]+)\"", raw)
    return {
        "firstLine": first,
        "claimsCcBy40": bool(has_cc_by),
        "creditRequested": credit.group(1) if credit else None,
        "derivativeCaveat": "Much of the data is based on other publically licenced sources"
        if "publically licenced sources" in raw
        else None,
    }


def build(zip_path: pathlib.Path) -> dict:
    size, sha = digest(zip_path)
    if size != PIN["bytes"] or sha != PIN["sha256"]:
        raise SystemExit(
            f"архив не совпал с закреплением: {size} B / {sha}\n"
            f"ожидалось {PIN['bytes']} B / {PIN['sha256']}"
        )

    zf = zipfile.ZipFile(zip_path)
    names = [n for n in zf.namelist() if not n.endswith("/")]
    root = names[0].split("/")[0]

    dirs: dict[str, dict] = collections.defaultdict(
        lambda: {"files": 0, "bytes": 0, "tokens": collections.Counter(), "untagged": []}
    )
    loose: list[dict] = []
    for name in names:
        rel = name[len(root) + 1 :]
        top = rel.split("/")[0]
        info = zf.getinfo(name)
        if "/" not in rel:
            # README.md и _config.yml — файлы репозитория, не наборы данных.
            loose.append(
                {"path": rel, "bytes": info.file_size, "tokens": sorted(TOKEN_RE.findall(rel))}
            )
            continue
        bucket = dirs[top]
        bucket["files"] += 1
        bucket["bytes"] += info.file_size
        found = TOKEN_RE.findall(rel)
        if found:
            for tok in found:
                bucket["tokens"][tok] += 1
        else:
            bucket["untagged"].append({"path": rel, "bytes": info.file_size})

    def norm(tok: str) -> str:
        """«CC-BY-NC» и «CC BY-NC» — один токен; «CC BY» и «CC-BY» — тоже."""
        t = re.sub(r"[\s-]+", " ", tok.upper()).strip()
        return t.replace(" ", "-")

    subdatasets = []
    for top in sorted(dirs):
        b = dirs[top]
        tokens = collections.Counter()
        for tok, n in b["tokens"].items():
            tokens[norm(tok)] += n
        entry = {
            "path": top,
            "files": b["files"],
            "bytes": b["bytes"],
            "declaredTerms": [{"token": t, "files": n} for t, n in sorted(tokens.items())],
            "filesWithoutTokenInName": b["untagged"],
            "note": NOTES.get(top),
        }
        # Более точные примечания для подкаталогов второго уровня.
        for key, note in NOTES.items():
            if "/" in key and top == key.split("/")[0] and any(
                f["path"].startswith(key) for f in b["untagged"]
            ):
                entry.setdefault("nestedNotes", []).append({"path": key, "note": note})
        subdatasets.append(entry)

    # Второй уровень: подкаталоги внутри Tagged-Bibles, где условия расходятся.
    nested = []
    for key in NOTES:
        if "/" not in key:
            continue
        prefix = f"{root}/{key}/"
        files = [n for n in names if n.startswith(prefix)]
        if not files:
            continue
        tokens = collections.Counter()
        for n in files:
            for tok in TOKEN_RE.findall(n):
                tokens[norm(tok)] += 1
        nested.append(
            {
                "path": key,
                "files": len(files),
                "bytes": sum(zf.getinfo(n).file_size for n in files),
                "declaredTerms": [{"token": t, "files": c} for t, c in sorted(tokens.items())],
                "note": NOTES[key],
            }
        )

    return {
        "role": "DERIVED_READ_ONLY_NOT_AUTHORITY",
        "pin": PIN,
        "readme": readme_claim(zf, root),
        "totals": {
            "files": len(names),
            "dataFiles": len(names) - len(loose),
            "bytesUncompressed": sum(zf.getinfo(n).file_size for n in names),
            "archiveBytes": PIN["bytes"],
            "topLevelEntries": len(subdatasets),
        },
        "subdatasets": subdatasets,
        "nestedSubdatasets": nested,
        "looseFiles": loose,
        "limits": [
            "Лицензия в имени файла — утверждение распространителя, а не решение владельца.",
            "Разметка и форматирование могут быть CC BY 4.0 при том, что исходный текст "
            "(ESV, LSJ, Abbott-Smith) имеет собственные права.",
            "Содержимое файлов не читалось: разобраны имена и README.",
            "Ни один HOLD этим не снимается; это материал для решения о правах.",
        ],
    }


def display_path(path: pathlib.Path) -> str:
    """Показать repo-relative путь, не упав на временном файле из теста."""
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def check() -> int:
    if not OUT_JSON.exists():
        print(f"нет {display_path(OUT_JSON)}", file=sys.stderr)
        return 1
    try:
        data = json.loads(OUT_JSON.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"{display_path(OUT_JSON)} не разбирается: {exc}", file=sys.stderr)
        return 1
    errors: list[str] = []

    pin = data.get("pin", {})
    if pin.get("sha256") != PIN["sha256"] or pin.get("commit") != PIN["commit"]:
        errors.append("закрепление в JSON не совпадает с PIN в скрипте")
    if pin.get("bytes") != PIN["bytes"]:
        errors.append("размер архива в JSON не совпадает с PIN")

    totals = data.get("totals", {})
    summed = sum(s["bytes"] for s in data.get("subdatasets", [])) + sum(
        f["bytes"] for f in data.get("looseFiles", [])
    )
    if totals.get("bytesUncompressed") != summed:
        errors.append(
            f"сумма подкаталогов и файлов {summed} != распакованного итога {totals.get('bytesUncompressed')}"
        )
    if totals.get("archiveBytes") != PIN["bytes"]:
        errors.append(f"размер архива в JSON {totals.get('archiveBytes')} != PIN {PIN['bytes']}")

    files = sum(s["files"] for s in data.get("subdatasets", [])) + len(data.get("looseFiles", []))
    if files != totals.get("files"):
        errors.append(f"сумма файлов {files} != итога {totals.get('files')}")

    if not data.get("readme", {}).get("claimsCcBy40"):
        errors.append("README не фиксирует заявленный CC BY 4.0")

    for entry in data.get("subdatasets", []):
        if not entry.get("declaredTerms") and not entry.get("filesWithoutTokenInName"):
            errors.append(f"{entry['path']}: ни токенов, ни неразмеченных файлов")

    if REPRO_JSON.exists():
        repro = json.loads(REPRO_JSON.read_text(encoding="utf-8"))
        items = repro.get("datasets") or repro.get("items") or []
        step = next((d for d in items if "STEPBible" in json.dumps(d, ensure_ascii=False)), None)
        if step and step.get("bytes") not in (None, PIN["bytes"]):
            errors.append(f"расхождение с official-core JSON: {step.get('bytes')}")

    if errors:
        for e in errors:
            print(f"FAIL: {e}", file=sys.stderr)
        return 1
    print("STEPBible subdataset terms: PASS (JSON согласован, закрепление совпадает)")
    return 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--zip", type=pathlib.Path, help="архив STEPBible, скачанный по PIN['url']")
    ap.add_argument("--write", action="store_true", help="записать JSON")
    ap.add_argument("--check", action="store_true", help="сверить записанный JSON без архива")
    args = ap.parse_args(argv)

    if args.check:
        return check()
    if not args.zip:
        ap.error("нужен --zip (для генерации) или --check")
    data = build(args.zip)
    text = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    if args.write:
        OUT_JSON.write_text(text, encoding="utf-8")
        print(f"записано: {OUT_JSON.relative_to(ROOT)}")
        return 0
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
