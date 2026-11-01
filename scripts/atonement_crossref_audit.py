#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Проверка перекрёстных ссылок черновиков на подразделы корпуса.

Зачем этот файл существует. Каждый довод серии обязан стоять на локаторе: «пересказ по
`../15_` §A.4». Если такой раздел в целевом файле называется иначе или его нет, ссылка
ведёт в пустоту, и проверяющий, открыв файл, попадёт не туда — при этом сам текст
черновика может быть верным. Такие ошибки не видны ни сверке цитат, ни сверке
греческого: они ломают именно цепочку «утверждение → источник».

Что проверяется. Ссылка вида `../NN_ИМЯ.md` вместе с номером подраздела (§A.4, §1.2,
§6.3, §B.5) в той же строке. Скрипт открывает целевой файл в ИСКУПЛЕНИЕ/ (или в
docs/research/atonement/ по префиксу `../../`), собирает заголовки и их номера и
отвечает: есть ли такой номер. Ссылки на разделы с именами (§3.15, §9.41) проверяются
там, где у заголовка есть номер.

Чего скрипт не делает. Он не судит, тот ли раздел выбран по смыслу, — только существует
ли он. Ссылка на существующий, но не тот раздел остаётся его слепой зоной; ровно поэтому
в отчёте печатается заголовок найденного раздела, чтобы человек проверил смысл.

Команды:
  --check   код 1, если есть ссылки на отсутствующие номера;
  --json    записать отчёт.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

FILE_REF = re.compile(r"((?:\.\./)*)((?:[a-z]+/)?)([0-9]{2}_[A-Za-z0-9_\-]+\.md)")
SECTION = re.compile(r"§\s*([A-ZА-Я]?\.?\s?\d+(?:\.\d+)?)")
HEADING = re.compile(r"^#{1,6}\s+(.*)$")
HEAD_ID = re.compile(r"^\s*([A-ZА-Я]?\.?\d+(?:\.\d+)?)\.?(?:\s|$)|^\s*([A-ZА-Я])\.(\d+)")


def heading_ids(path: Path) -> dict[str, str]:
    """Номера подразделов файла: {'A.4': '### A.4 Комментарий…'}."""
    ids: dict[str, str] = {}
    if not path.exists():
        return ids
    for line in path.read_text(encoding="utf-8").splitlines():
        m = HEADING.match(line)
        if not m:
            continue
        text = m.group(1).strip()
        # «A.4 Комментарий…», «1.2 Что…», «6.3 Классы…», «A. Кальвин…»
        mm = re.match(r"^([A-ZА-Я])\.(\d+)\b", text)
        if mm:
            ids[f"{mm.group(1)}.{mm.group(2)}"] = text[:60]
            continue
        mm = re.match(r"^([A-ZА-Я])\.(?:\s|$)", text)
        if mm:
            ids[mm.group(1)] = text[:60]
            continue
        mm = re.match(r"^(\d+(?:\.\d+)*)\.?\s", text)
        if mm:
            ids[mm.group(1)] = text[:60]
    return ids


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--drafts", default="ИСКУПЛЕНИЕ/synthesis/drafts")
    ap.add_argument("--root", default="ИСКУПЛЕНИЕ")
    ap.add_argument("--docs", default="docs/research/atonement")
    ap.add_argument("--json", default=None)
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args(argv)

    cache: dict[Path, dict[str, str]] = {}
    rows = []
    for draft in sorted(Path(args.drafts).glob("*.md")):
        text = draft.read_text(encoding="utf-8")
        for lineno, line in enumerate(text.splitlines(), 1):
            filerefs = list(FILE_REF.finditer(line))
            if not filerefs:
                continue
            for sec in SECTION.finditer(line):
                sec_id = sec.group(1).replace(" ", "")
                # целевой файл — ближайшая ссылка слева от номера
                cand = [f for f in filerefs if f.end() <= sec.start()]
                if not cand:
                    continue
                # Конвенция `../` в черновиках смешана: местами это synthesis/,
                # местами корень корпуса. Поэтому пробуем несколько баз и честно
                # записываем, какая сработала; «файл не найден» и «раздел не найден» —
                # разные диагнозы и не должны сливаться.
                rel = cand[-1].group(1) + cand[-1].group(2) + cand[-1].group(3)
                bases = [
                    ("drafts", draft.parent),
                    ("synthesis", draft.parent.parent),
                    ("corpus", draft.parent.parent.parent),
                    ("docs", Path(args.docs)),
                ]
                target, used_base = None, None
                for name, base in bases:
                    t = Path(os.path.normpath(base / rel))
                    if t.exists():
                        target, used_base = t, name
                        break
                if target is None:
                    rows.append(
                        {
                            "draft": draft.name,
                            "line": lineno,
                            "target": os.path.normpath(draft.parent / rel),
                            "section": sec_id,
                            "exists": False,
                            "diagnosis": "FILE_NOT_FOUND",
                            "heading": "",
                            "nearest_ids": [],
                        }
                    )
                    continue
                if target not in cache:
                    cache[target] = heading_ids(target)
                ids = cache[target]
                found = sec_id in ids
                rows.append(
                    {
                        "draft": draft.name,
                        "line": lineno,
                        "target": str(target),
                        "base": used_base,
                        "section": sec_id,
                        "exists": found,
                        "diagnosis": "OK" if found else "SECTION_NOT_FOUND",
                        "heading": ids.get(sec_id, ""),
                        "nearest_ids": sorted(ids)[:14] if not found else [],
                    }
                )

    bad = [r for r in rows if not r["exists"]]
    by_diag: dict[str, int] = {}
    for r in rows:
        by_diag[r["diagnosis"]] = by_diag.get(r["diagnosis"], 0) + 1
    print(f"перекрёстных ссылок с номером подраздела: {len(rows)}")
    for k in sorted(by_diag):
        print(f"  {k}: {by_diag[k]}")
    for r in bad:
        print(f"\n[{r['diagnosis']}] {r['draft']}:{r['line']} §{r['section']} → {r['target']}")
        if r["nearest_ids"]:
            print(f"  в файле есть номера: {', '.join(r['nearest_ids'])}")

    if args.json:
        Path(args.json).write_text(
            json.dumps({"total": len(rows), "missing": bad, "all": rows},
                       ensure_ascii=False, indent=1),
            encoding="utf-8",
        )
    if args.check and bad:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
