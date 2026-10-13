#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Еврейский MT (BHS) из Text-Fabric-данных ETCBC/bhsa-min — доступ по ссылкам.

Зачем этот инструмент
---------------------
До него утверждения вида «LXX передаёт כַּפֹּרֶת как ἱλαστήριон» были ВЫВОДОМ
из греческого соответствия и стояли под MT_HOLD. Здесь они становятся прямой
проверкой по еврейскому оригиналу.

Данные
------
ETCBC/bhsa-min @ f600a50fd902b6c9d31d67cf5611365df4169bce, TF-версия 2021,
датасет BHSA (Biblia Hebraica Stuttgartensia Amstelodamensis).

Права — читать внимательно, это не MIT:
  * LICENSE в репозитории — MIT, но он покрывает код дистилляции;
  * сами данные по README репозитория BHSA идут под CC BY-NC 4.0,
    DOI 10.17026/dans-z6y-skyh;
  * некоммерческое исследование и публикация результатов разрешены с
    атрибуцией; коммерческое использование — только с согласия
    German Bible Society (zentrale@dbg.de).
  * README bhsa-min прямо говорит, что версия «distilled from the full
    version», поэтому лицензия данных наследуется, а не заменяется MIT.

Два подводных камня формата .tf, на которых этот модуль уже горел
-----------------------------------------------------------------
1. Пустые строки — ЭТО ЗНАЧЕНИЯ. В g_word_utf8.tf их 6488: у слота может не
   быть огласованной формы. Разделитель заголовка и данных ровно один, он идёт
   сразу за последней '@'-строкой. Пропускать все пустые строки нельзя: массив
   слов сжимается, и ссылки начинают съезжать тем сильнее, чем дальше по канону
   (Gen 1:1 остаётся верным, Lev 16:2 уезжает в Lev 17, Is 53 — в Is 65).
2. В oslots.tab стоит только в ПЕРВОЙ строке; дальше узлы идут подряд, поэтому
   номер узла надо инкрементировать, а не ждать табуляции.

Ссылки — английские названия книг BHSA: 'Exodus 25:17', 'Isaiah 53:11'.
Нумерация стихов в Псалмах по BHS включает надписание как стих 1, то есть
сдвинута относительно английской/русской нумерации на единицу.
"""
from __future__ import annotations

import bisect
import os
import sys
sys.dont_write_bytecode = True
from pathlib import Path

from nt_sources import registry, verify_dataset, witness_dir, witnesses

DEFAULT = witness_dir("S6", verify=False)


def data_lines(p: Path) -> list[str]:
    """Строки данных .tf-файла, ВКЛЮЧАЯ пустые (они являются значениями).

    Заголовок — все '@'-строки в начале файла; за ним ровно одна пустая
    строка-разделитель, и только она отбрасывается.
    """
    lines = p.read_text(encoding="utf-8").splitlines()
    last_at = max((i for i, l in enumerate(lines) if l.startswith("@")),
                  default=-1)
    if last_at < 0:
        raise SystemExit(f"{p}: не похоже на файл Text-Fabric (нет '@'-строк)")
    data = lines[last_at + 1:]
    if data and data[0].strip() == "":
        data = data[1:]
    return data


class MT:
    """Доступ к BHSA: ссылка -> еврейский текст, лексемы, счётчики."""

    def __init__(self, root: Path | None = None):
        root = witness_dir("S6") if root is None else Path(root)
        verify_dataset("S6", witnesses()["S6"], root)
        if not root.is_dir():
            raise SystemExit(
                f"MT (BHS) не найден в {root}. Скачайте corpus-скриптом "
                f"(ETCBC/bhsa-min) или задайте NT_MT_DIR.")
        self.root = Path(root)
        r = self.root

        self.types: dict[str, tuple[int, int]] = {}
        for line in data_lines(r / "otype.tf"):
            if not line.strip():
                continue
            rng, otype = line.rsplit("\t", 1)
            lo, hi = (int(x) for x in rng.split("-")) if "-" in rng \
                else (int(rng), int(rng))
            self.types[otype] = (lo, hi)
        self.max_word = self.types["word"][1]

        self.book_en = self._node_feature("book@en.tf")
        self.chapter_n = self._node_feature("chapter.tf")
        self.verse_n = self._node_feature("verse.tf")
        self.gword = {i: v for i, v in
                      enumerate(data_lines(r / "g_word_utf8.tf"), start=1)}
        self.lex = {i: v for i, v in
                    enumerate(data_lines(r / "lex_utf8.tf"), start=1)}
        # trailer пуст там, где за словом НЕ следует пробел (проклитики типа
        # וְ/הַ/לְ склеиваются со следующим словом). Без этого еврейская
        # цитата выглядит рваной: «וְ עָשִׂיתָ כַפֹּרֶת» вместо «וְעָשִׂיתָ כַפֹּרֶת».
        self.trailer = {i: v for i, v in
                        enumerate(data_lines(r / "trailer_utf8.tf"), start=1)}

        # oslots: узел -> диапазон слотов. Таб только в первой строке.
        self.slots: dict[int, tuple[int, int]] = {}
        node = 0
        for line in data_lines(r / "oslots.tf"):
            if not line.strip():
                continue
            if "\t" in line:
                head, rng = line.split("\t", 1)
                node = int(head)
            else:
                node += 1
                rng = line
            first = rng.split(",")[0].strip()
            if not first:
                continue
            a, b = ((int(x) for x in first.split("-")) if "-" in first
                    else (int(first), int(first)))
            self.slots[node] = (a, b)

        def spans(otype: str) -> list[tuple[int, int, int]]:
            lo, hi = self.types[otype]
            out = [(self.slots[n][0], self.slots[n][1], n)
                   for n in range(lo, hi + 1) if n in self.slots]
            out.sort()
            return out

        self._books = spans("book")
        self._chapters = spans("chapter")
        self._book_starts = [s[0] for s in self._books]
        self._chap_starts = [s[0] for s in self._chapters]

        # Ссылка -> узел стиха.
        vlo, vhi = self.types["verse"]
        self.by_ref: dict[str, int] = {}
        self.verse_order: list[tuple[int, int, int]] = []
        for n in range(vlo, vhi + 1):
            if n not in self.slots:
                continue
            s = self.slots[n][0]
            bk = self._at(self._book_starts, self._books, s)
            ch = self._at(self._chap_starts, self._chapters, s)
            if bk is None or ch is None:
                continue
            key = (f"{self.book_en.get(bk)} {self.chapter_n.get(ch)}"
                   f":{self.verse_n.get(n)}")
            self.by_ref[key] = n
            self.verse_order.append((s, self.slots[n][1], n))
        self.verse_order.sort()
        self._verse_starts = [v[0] for v in self.verse_order]
        # Обратный индекс: слот -> узел стиха (для поиска по лексемам).
        self._slot_verse: list[int] = [0] * (self.max_word + 1)
        for s, e, n in self.verse_order:
            for w in range(s, e + 1):
                self._slot_verse[w] = n
        self._node_ref: dict[int, str] = {v: k for k, v in self.by_ref.items()}
        expected = witnesses()["S6"]
        if self.max_word != expected["wordSlots"] or len(self.by_ref) != expected["verses"]:
            raise ValueError("S6 parsed word/verse cardinality differs from SSOT")
        if any(len(feature) != self.max_word for feature in (self.gword, self.lex, self.trailer)):
            raise ValueError("S6 word features lost empty values or slots")
        if any(n == 0 for n in self._slot_verse[1:]):
            raise ValueError("S6 word slot without a verse locator")

    # -- разбор признаков -------------------------------------------------
    def _node_feature(self, name: str) -> dict[int, str]:
        out: dict[int, str] = {}
        node = 0
        for line in data_lines(self.root / name):
            if "\t" in line:
                head, val = line.split("\t", 1)
                node = int(head)
            else:
                node += 1
                val = line
            out[node] = val.rstrip("\n")
        return out

    @staticmethod
    def _at(starts: list[int], spans: list, slot: int):
        i = bisect.bisect_right(starts, slot) - 1
        if i < 0:
            return None
        s, e, node = spans[i]
        return node if s <= slot <= e else None

    # -- публичное --------------------------------------------------------
    def text(self, ref: str) -> str:
        n = self.by_ref.get(ref)
        if n is None:
            raise KeyError(ref)
        a, b = self.slots[n]
        return " ".join(self.gword.get(i, "") for i in range(a, b + 1)).strip()

    def words(self, ref: str) -> list[str]:
        """Слова стиха с проклитиками склеенными (по trailer_utf8)."""
        n = self.by_ref.get(ref)
        if n is None:
            raise KeyError(ref)
        a, b = self.slots[n]
        out: list[str] = []
        for i in range(a, b + 1):
            w = self.gword.get(i, "")
            if out and self.trailer.get(i - 1, " ") == "":
                out[-1] += w
            else:
                out.append(w)
        return out

    def text_words(self, ref: str) -> str:
        return " ".join(self.words(ref))

    def lexemes(self, ref: str) -> list[str]:
        n = self.by_ref.get(ref)
        if n is None:
            raise KeyError(ref)
        a, b = self.slots[n]
        return [self.lex.get(i, "") for i in range(a, b + 1)]

    def has_lexeme(self, ref: str, lexeme: str) -> bool:
        return lexeme in self.lexemes(ref)

    def find_lexeme(self, lexeme: str) -> list[tuple[str, str]]:
        """Все (ссылка, словоформа) для лексемы. Точное совпадение лексемы."""
        hits: list[tuple[str, str]] = []
        seen: set[int] = set()
        for w, lx in self.lex.items():
            if lx != lexeme or w > self.max_word:
                continue
            n = self._slot_verse[w]
            if n and n not in seen:
                seen.add(n)
                hits.append((self._node_ref.get(n, f"node{n}"), self.gword.get(w, "")))
        return hits

    def count_lexeme(self, lexeme: str) -> int:
        return sum(1 for w, lx in self.lex.items()
                   if lx == lexeme and w <= self.max_word)

    def refs(self, book: str) -> list[str]:
        return [k for k in self.by_ref if k.startswith(book + " ")]


def main(argv: list[str]) -> int:
    mt = MT()
    print(f"стихов: {len(mt.by_ref)}; слов-слотов: {mt.max_word}")
    failures = 0
    for arg in argv:
        if arg.startswith("count:"):
            lx = arg.split(":", 1)[1]
            print(f"count {lx}: {mt.count_lexeme(lx)}")
        elif arg.startswith("find:"):
            lx = arg.split(":", 1)[1]
            for ref, form in mt.find_lexeme(lx):
                print(f"  {ref}\t{form}")
        else:
            try:
                print(f"{arg}: {mt.text_words(arg)}")
            except KeyError:
                print(f"{arg}: НЕ НАЙДЕНО")
                failures += 1
    return 1 if failures else 0


if __name__ == "__main__":
    try:
        raise SystemExit(main(sys.argv[1:]))
    except (KeyError, OSError, ValueError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
