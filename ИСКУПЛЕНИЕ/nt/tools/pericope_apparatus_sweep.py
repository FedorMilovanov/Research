#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Прогон аппарата SBLGNT (S7) по всем перикопам §3.2 брифа.

Зачем
-----
S1 (py-sblgnt) печатает сиглы вариантов прямо в тексте (⸀ ⸂ ⸃), но не говорит,
в чём variant состоит. S7 говорит. Этот скрипт соединяет их: берёт каждую
перикопу из карточек 06_/07_/08_/10_, разворачивает диапазоны и списки и
печатает, какие записи <app> на неё приходятся.

Что скрипт НЕ делает
--------------------
Не решает, какое чтение верное, и не определяет объём искупления. Он отвечает
только на вопрос «где в корпусе об искуплении вообще есть textual variation».

Использование:
  python3 ИСКУПЛЕНИЕ/nt/tools/pericope_apparatus_sweep.py            # сводка
  python3 ИСКУПЛЕНИЕ/nt/tools/pericope_apparatus_sweep.py --full     # с чтениями
  python3 ИСКУПЛЕНИЕ/nt/tools/pericope_apparatus_sweep.py --sigla    # только стихи с сиглами в S1
"""
from __future__ import annotations

import glob
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sbl_apparatus import Apparatus  # noqa: E402

ROOT = Path(__file__).resolve().parents[1].parent  # ИСКУПЛЕНИЕ/

BOOKS = ["Мф", "Мк", "Лк", "Ин", "Деян", "Рим", "1 Кор", "2 Кор", "Гал", "Еф",
         "Флп", "Кол", "1 Фес", "2 Фес", "1 Тим", "2 Тим", "Тит", "Флм",
         "Евр", "Иак", "1 Пет", "2 Пет", "1 Ин", "2 Ин", "3 Ин", "Иуд", "Откр"]
BOOKRE = "|".join(sorted(BOOKS, key=len, reverse=True))
CARD_GLOBS = ["nt/06_*.md", "nt/07_*.md", "nt/08_*.md", "nt/10_*.md"]


def expand(text: str) -> set[str]:
    """Разворачивает ссылку в список стихов.

    Обязательны обе развёртки, иначе审计 врёт: карточки пишут и диапазонами
    («Ин 6:37–40»), и списками («Ин 10:11, 15, 26»). Без них первый прогон
    показывал десятки ложных «пропусков».
    """
    out: set[str] = set()
    for m in re.finditer(rf"(?<![\w])({BOOKRE})\s+(\d+):([\d]+)((?:[–,\s]+[\d]+)*)", text):
        book, ch, first, rest = m.group(1), m.group(2), int(m.group(3)), m.group(4)
        vs = [first]
        for part in re.split(r"[–,\s]+", rest.strip()):
            if part.isdigit():
                vs.append(int(part))
        for v in range(min(vs), max(vs) + 1):
            out.add(f"{book} {ch}:{v}")
    return out


def card_refs() -> set[str]:
    refs: set[str] = set()
    for g in CARD_GLOBS:
        for path in sorted(glob.glob(str(ROOT / g))):
            text = Path(path).read_text(encoding="utf-8")
            for m in re.finditer(r"(?m)^## ((?:0[678]|10)\.\d+ )(.+)$", text):
                refs |= expand(m.group(2))
    return refs


def sbl_sigla() -> set[str]:
    """Стихи, где S1 сам напечатал сиглу варианта (⸀ ⸁ ⸂ ⸃ ⸄ …)."""
    hits: set[str] = set()
    names = {"01": "Мф", "02": "Мк", "03": "Лк", "04": "Ин", "05": "Деян",
             "06": "Рим", "07": "1 Кор", "08": "2 Кор", "09": "Гал", "10": "Еф",
             "11": "Флп", "12": "Кол", "13": "1 Фес", "14": "2 Фес", "15": "1 Тим",
             "16": "2 Тим", "17": "Тит", "18": "Флм", "19": "Евр", "20": "Иак",
             "21": "1 Пет", "22": "2 Пет", "23": "1 Ин", "24": "2 Ин", "25": "3 Ин",
             "26": "Иуд", "27": "Откр"}
    for path in glob.glob(str(Path.home() / "nt-corpus/py-sblgnt*/pysblgnt/sblgnt/*.txt")):
        for line in Path(path).read_text(encoding="utf-8").splitlines():
            p = line.split()
            if len(p) < 8 or not p[0].isdigit():
                continue
            if any(c in p[4] for c in "⸀⸁⸂⸃⸄⸅⸆⸇"):
                c = p[0]
                b = names.get(c[0:2])
                if b:
                    hits.add(f"{b} {int(c[2:4])}:{int(c[4:6])}")
    return hits


def main(argv: list[str]) -> int:
    app = Apparatus()
    refs = card_refs()
    def order(r: str):
        # Имя книги может содержать пробел («1 Кор», «2 Пет»), поэтому r.split()[0]
        # не годится — оно вернёт «1». Берём по совпадению с BOOKS.
        for i, b in enumerate(sorted(BOOKS, key=len, reverse=True)):
            if r.startswith(b + " "):
                ch, v = r[len(b) + 1:].split(":")
                return (BOOKS.index(b), int(ch), int(v))
        return (len(BOOKS), 0, 0)

    withapp = sorted([r for r in refs if r in app.entries], key=order)
    total = sum(len(app.entries[r]) for r in withapp)
    print(f"стихов перикоп §3.2 (после разворачивания): {len(refs)}")
    print(f"с записью <app> в S7: {len(withapp)}; всего записей: {total}")
    print(f"БЕЗ textual variation: {len(refs) - len(withapp)} из {len(refs)}"
          f"  = {(len(refs) - len(withapp)) / len(refs) * 100:.1f}%")

    if "--sigla" in argv:
        sig = sbl_sigla()
        both = sorted(set(withapp) & sig)
        print(f"\nстихов с сиглой ⸀⸂⸃ прямо в S1: {len(sig)}"
              f"; из них на перикопах брифа: {len(both)}")
        for r in both:
            print(f"  {r}")
        return 0

    print()
    for r in withapp:
        items = app.entries[r]
        wits = sorted({w for it in items for rd in it["rdg"] for w in rd["wit"]})
        print(f"{r:12s} n={len(items):2d}  {'+'.join(wits)}")
        if "--full" in argv:
            for it in items:
                print(f"    lem: {it['lem']}")
                for rd in it["rdg"]:
                    print(f"       {'+'.join(rd['wit']):30s} {rd['text']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
