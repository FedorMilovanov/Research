#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Критический аппарат SBLGNT (свидетель S7) — доступ по ссылкам.

Зачем
-----
До S7 карточки могли только констатировать расхождение S1 против трёх изданий TR
и ставить `LOCATOR_HOLD`: перечислить варианты было нечем. Здесь аппарат
читается напрямую.

Свидетель
---------
`jjmccollum/sblgnt-tei` — TEI-разметка текста и аппарата *SBL Greek New
Testament* (Holmes). Лицензия **CC BY 4.0**: сам SBLGNT перевыпущен под CC BY,
репозиторий унаследовал лицензию. Это НЕ CC BY-NC и не CC BY-SA, как у S5/S6.

Свидетели аппарата (по `<witness>` из teiHeader, дословно):
  NA     Novum Testamentum Graece **27** (Aland/Black/Martini/Metzger/Wikgren,
         Stuttgart: Deutsche Bibelgesellschaft, 1979)
  TR     Scrivener, Textus Stephanici A.D. 1550, 4th ed., corrected by E. Nestle
         (London/Cambridge, 1906)
  RP     Robinson & Pierpont, Byzantine Textform (2005)
  WH / WHapp / WHmarg / WHspur   Westcott & Hort
  Treg / Tregmarg                Tregelles
  ECM    Editio Critica Maior — **только Соборные послания** (1997–2005)
  Greeven  Huck, Synopse
  NIV    Reader's Greek New Testament (Goodrich/Lukaszewski)
  Holmes сам SBLGNT

Граница, которую этот аппарат НЕ закрывает
------------------------------------------
Атрибуция идёт **изданиям**, а не рукописям: `#NA`, `#TR`, `#RP`, `#WH`.
Здесь нет ни `א`, ни `B`, ни `P46`. И `#NA` — это edition=27 по заголовку (year=1979 ему противоречит), не NA28; UBS5
отдельно не представлен. Поэтому `LOCATOR_HOLD` сужается до рукописного
уровня и до NA28/UBS5, но не снимается.
"""
from __future__ import annotations

import os
import re
import sys
from collections import Counter
sys.dont_write_bytecode = True
import xml.etree.ElementTree as ET
from pathlib import Path

from nt_sources import witness_file, witnesses
from nt_refs import s1_verses

BOOKS = ["Мф", "Мк", "Лк", "Ин", "Деян", "Рим", "1 Кор", "2 Кор", "Гал", "Еф",
         "Флп", "Кол", "1 Фес", "2 Фес", "1 Тим", "2 Тим", "Тит", "Флм",
         "Евр", "Иак", "1 Пет", "2 Пет", "1 Ин", "2 Ин", "3 Ин", "Иуд", "Откр"]
BY_NUM = {f"B{i:02d}": name for i, name in enumerate(BOOKS, start=1)}
BY_NAME = {v: k for k, v in BY_NUM.items()}


def default_xml() -> Path:
    return witness_file("S7", "sblgnt_tei.xml", "NT_APPARATUS_XML")


class Apparatus:
    def __init__(self, path: Path | None = None):
        canonical = default_xml()
        if path is None:
            path = canonical
        elif not path.is_file() or path.read_bytes() != canonical.read_bytes():
            raise ValueError("S7 supplied XML differs from pinned source")
        if not path.is_file():
            raise SystemExit(f"аппарат SBLGNT не найден в {path}; "
                             f"задайте NT_APPARATUS_XML")
        self.path = path
        self.tree = ET.parse(path)
        self.root = self.tree.getroot()
        # TEI comes namespaced: tag == "{http://www.tei-c.org/ns/1.0}div".
        # Срезаем пространство имён у всех элементов, иначе ни один тег не
        # совпадёт и индекс останется пустым (так и было в первой версии:
        # 0 свидетелей, 0 вариантов при 6929 <app> в файле).
        for el in self.root.iter():
            if isinstance(el.tag, str) and el.tag.startswith("{"):
                el.tag = el.tag.split("}", 1)[1]
        self.entries: dict[str, list[dict]] = {}
        self.witnesses: dict[str, str] = {}
        for w in self.root.iter("witness"):
            wid = w.get("xml:id") or w.get("{http://www.w3.org/XML/1998/namespace}id")
            txt = re.sub(r"\s+", " ", "".join(w.itertext())).strip()
            self.witnesses[wid] = txt
        self._index()
        expected = witnesses()["S7"]
        actual = (self.count(), len(self.entries), len(self.witnesses),
                  sum(len(e["rdg"]) for entries in self.entries.values() for e in entries))
        wanted = tuple(expected[k] for k in ("appEntries", "appPositions", "witnesses", "rdgElements"))
        if actual != wanted:
            raise ValueError(f"S7 parsed cardinality mismatch: {actual} != {wanted}")
        cited = Counter(w for entries in self.entries.values() for e in entries
                        for rd in e["rdg"] for w in rd["wit"])
        if dict(cited) != expected["siglaCitationCounts"]:
            raise ValueError("S7 siglum citation census differs from SSOT")
        for entries in self.entries.values():
            for entry in entries:
                for reading in entry["rdg"]:
                    if set(reading["wit"]) - self.witnesses.keys():
                        raise ValueError(f"S7 unknown witness siglum: {reading['wit']}")

    @staticmethod
    def _xmlid(el):
        return el.get("xml:id") or el.get("{http://www.w3.org/XML/1998/namespace}id") or ""

    def _index(self):
        # свидетели лежат в teiHeader и обходятся отдельно, потому что после
        # среза пространства имён iter() по root их всё равно находит
        cur_book = cur_ch = cur_v = None
        for el in self.root.iter():
            tag = el.tag
            if tag == "div" and el.get("type") == "book":
                cur_book = self._xmlid(el)
            elif tag == "milestone":
                xid = self._xmlid(el)
                if el.get("unit") == "chapter":
                    m = re.match(r"(B\d+)K(\d+)$", xid)
                    if m:
                        cur_book, cur_ch = m.group(1), int(m.group(2))
                elif el.get("unit") == "verse":
                    m = re.match(r"(B\d+)K(\d+)V(\d+)$", xid)
                    if m:
                        cur_book, cur_ch, cur_v = m.group(1), int(m.group(2)), int(m.group(3))
            elif tag == "app":
                if not (cur_book in BY_NUM and cur_ch and cur_v):
                    raise ValueError("S7 app entry without a valid verse locator")
                key = f"{BY_NUM.get(cur_book, cur_book)} {cur_ch}:{cur_v}"
                lemel = el.find("lem")
                lem = re.sub(r"\s+", " ", "".join(lemel.itertext())).strip() if lemel is not None else ""
                rdgs = []
                for r in el.findall("rdg"):
                    rdgs.append({"wit": (r.get("wit") or "").replace("#", "").split(),
                                 "text": re.sub(r"\s+", " ", "".join(r.itertext())).strip()})
                self.entries.setdefault(key, []).append({"lem": lem, "rdg": rdgs})

    def at(self, ref: str) -> list[dict]:
        return self.entries.get(ref, [])

    def count(self) -> int:
        return sum(len(v) for v in self.entries.values())


def main(argv: list[str]) -> int:
    a = Apparatus()
    print(f"аппарат: {a.path.name}; вариантов: {a.count()} "
          f"в {len(a.entries)} позициях; свидетелей: {len(a.witnesses)}")
    if not argv:
        return 0
    if argv[0] == "--witnesses":
        for k, v in sorted(a.witnesses.items()):
            print(f"  {k:9s} {v[:150]}")
        return 0
    known_refs = s1_verses()
    for ref in argv:
        if ref not in known_refs and ref not in a.entries:
            raise ValueError(f"invalid verse reference: {ref}")
        items = a.at(ref)
        print(f"\n=== {ref} — записей: {len(items)} ===")
        for it in items:
            print(f"  lem : {it['lem']}")
            for r in it["rdg"]:
                print(f"    {'+'.join(r['wit']):28s} {r['text']}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main(sys.argv[1:]))
    except (KeyError, OSError, ValueError, ET.ParseError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
