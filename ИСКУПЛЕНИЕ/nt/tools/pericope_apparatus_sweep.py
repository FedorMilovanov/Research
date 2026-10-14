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

import re
import sys
sys.dont_write_bytecode = True
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sbl_apparatus import Apparatus  # noqa: E402
from nt_sources import registry
from nt_refs import BOOKS, expand, card_refs, s1_verses

def sbl_sigla() -> set[str]:
    return {ref for ref, rows in s1_verses().items()
            if any(any(c in row[4] for c in "⸀⸁⸂⸃⸄⸅⸆⸇") for row in rows)}


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
    print(f"стихов, явно указанных в заголовках текстовых карточек: {len(refs)}")
    print(f"с записью <app> в S7: {len(withapp)}; всего записей: {total}")
    print(f"БЕЗ записи в выборочном аппарате S7 (не согласие всех): {len(refs) - len(withapp)} из {len(refs)}"
          f"  = {(len(refs) - len(withapp)) / len(refs) * 100:.1f}%")

    sig = sbl_sigla()
    s1_hits, s7_hits = sig & refs, set(withapp)
    only_s1, only_s7 = sorted(s1_hits - s7_hits), sorted(s7_hits - s1_hits)
    print(f"S1 sigla on selected verses: {len(s1_hits)}; S1-only={only_s1}; S7-only={only_s7}")
    if refs - s1_verses().keys():
        raise ValueError(f"card references absent from S1: {sorted(refs - s1_verses().keys())}")
    if "--check" in argv:
        expected = registry()["apparatusSweep"]
        actual = (len(refs), len(withapp), total, len(refs) - len(withapp))
        wanted = tuple(expected[k] for k in ("versesInCardHeadings", "versesWithApparatus", "appRecordsOnPericopes", "versesWithoutEncodedApp"))
        if actual != wanted or only_s1 != expected["s1OnlySigla"] or only_s7 != expected["s7OnlyApp"]:
            raise ValueError(f"apparatus sweep SSOT mismatch: {actual} != {wanted}")
        print("PASS: selected-verse census and S1/S7 locator cross-check match SSOT")
    if "--sigla" in argv:
        for ref in sorted(s1_hits):
            print(f"  {ref}")
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
    try:
        raise SystemExit(main(sys.argv[1:]))
    except (KeyError, OSError, ValueError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
