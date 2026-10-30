#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Сверка помеченных цитат Писания в черновиках серии «Искупление» с текстом перевода.

Зачем этот файл существует. После того как в черновиках нашлись ошибки цитирования
(перевёрнутое различие Дорт II.1–IV, «угашение» вместо «прощения» в Рим. 3:25,
приписанные греческие формы), проверять цитаты глазами по одной стало недостаточно:
нужен сплошной прогон, который для каждой пометки «(Синодальный)» отвечает, есть ли
такая строка в самом стихе. Этот скрипт ничего не решает о богословии — он только
сравнивает текст.

Что считается цитатой. Фрагмент в «ёлочках», сразу за которым в скобках стоит
«Синодальный» (в любом окружении: «Синодальный перевод», «фрагмент, Синодальный»).
Пометки «пересказ» из сверки исключаются: пересказ не обязан совпадать.

Почему нужен внешний файл. В репозитории лежит только карта прав на Писание
(BIBLE_CORPUS/00_…), самого текста нет. Поэтому текст подаётся через --bible в формате
TSV: книга<TAB>сокращение<TAB>глава<TAB>стих<TAB>номер<TAB>текст. Такой формат отдаёт,
например, открытая транскрипция github.com/alexbkv/syn (Unlicense). Транскрипция — не
печатное издание: её согласие с печатным Синодальным на цитируемых стихах проверяется
отдельно, и в отчёте это записывается числом проверенных стихов.

Статусы одной цитаты (по каждому поданному своду):
  EXACT        фрагмент найден в стихе (после нормализации);
  SEGMENTS     фрагмент с многоточием: все сегменты найдены по порядку;
  RANGE        стих — диапазон, текст склеен из стихов по порядку;
  MISMATCH     хотя бы один сегмент не найден;
  VERSE_MISSING адрес есть, стиха нет в поданном своде.

Сводный статус цитаты:
  CONFIRMED           все поданные своды подтверждают цитату;
  CONFIRMED_MULTI     то же, но статусы сводов различаются (например EXACT и RANGE);
  SOURCE_CONFLICT     один свод подтверждает, другой нет — приговора цитате нет, нужен третий источник;
  NO_SOURCE_SUPPORTS  ни один свод не подтверждает: расхождение считается установленным;
  NO_REF              пометка «Синодальный» без адреса стиха (в строке адрес не найден);
  PARSE_FAIL          адрес найден, но не разобран.

Команды:
  --check   код 1, если есть MISMATCH/VERSE_MISSING/PARSE_FAIL (EXACT и SEGMENTS — норма);
  --write   записать отчёт JSON в --json (по умолчанию evidence-файл круга).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# Сокращения книг в черновиках → сокращения в TSV.
BOOK_ALIASES = {
    "быт": "Быт", "исх": "Исх", "лев": "Лев", "чис": "Чис", "втор": "Втор",
    "нав": "Нав", "суд": "Суд", "руф": "Руф", "1цар": "1Цар", "2цар": "2Цар",
    "3цар": "3Цар", "4цар": "4Цар", "1пар": "1Пар", "2пар": "2Пар",
    "езд": "Езд", "неем": "Неем", "есф": "Есф", "иов": "Иов", "пс": "Пс",
    "прит": "Прит", "притч": "Прит", "еккл": "Еккл", "песн": "Песн",
    "ис": "Ис", "иер": "Иер", "плач": "Плач", "иез": "Иез", "дан": "Дан",
    "ос": "Ос", "иоил": "Иоил", "ам": "Ам", "авд": "Авд", "ион": "Ион",
    "мих": "Мих", "наум": "Наум", "авв": "Ав", "соф": "Соф", "агг": "Аг",
    "заx": "Зах", "зах": "Зах", "мал": "Мал",
    "мф": "Мф", "матф": "Мф", "мк": "Мк", "лк": "Лк", "ин": "Ин",
    "деян": "Деян", "иак": "Иак", "1пет": "1Пет", "2пет": "2Пет",
    "1ин": "1Ин", "2ин": "2Ин", "3ин": "3Ин", "иуд": "Иуд",
    "рим": "Рим", "1кор": "1Кор", "2кор": "2Кор", "гал": "Гал", "еф": "Еф",
    "фил": "Фил", "флп": "Фил", "кол": "Кол", "1фес": "1Фес", "2фес": "2Фес",
    "1тим": "1Тим", "2тим": "2Тим", "тит": "Тит", "флм": "Флм", "евр": "Евр",
    "откр": "Откр", "откр.": "Откр",
}

CITE_RE = re.compile(r"«([^»]{2,400})»\s*\(([^()]{0,120})\)")
ELLIPSIS = re.compile(r"…|\.\.\.")


def normalize(text: str) -> str:
    """Нормализация для сравнения: регистр, ё, пунктуация, пробелы."""
    t = text.lower().replace("ё", "е")
    t = re.sub(r"[«»„“”\"'`_*]", " ", t)
    t = re.sub(r"[.,;:!?—–\-()\[\]]", " ", t)
    t = re.sub(r"\s+", " ", t)
    return t.strip()


def load_bible(path: Path) -> dict[tuple[str, int, int], str]:
    verses: dict[tuple[str, int, int], str] = {}
    with path.open(encoding="utf-8") as fh:
        for raw in fh:
            parts = raw.rstrip("\n").split("\t")
            if len(parts) >= 6:
                # Колонки: книга, сокращение, номер книги, глава, стих, текст.
                _, abbr, _book_no, ch, vs, text = parts[:6]
            elif len(parts) == 4:
                # Колонки: сокращение, глава, стих, текст (свод RST parsed66).
                abbr, ch, vs, text = parts
            else:
                continue
            try:
                key = (abbr, int(ch), int(vs))
            except ValueError:
                continue
            verses[key] = text.strip()
    return verses


def parse_ref(ref: str):
    """'Рим. 3:25' → ('Рим', 3, 25, 25); 'Ис. 53:5–6' → ('Ис', 53, 5, 6).

    Возвращает (book, chapter, first, last) или None, если адреса нет.
    Глава без стиха ('Евр. 9–10') адресом стиха не считается.
    """
    m = re.match(
        r"^\s*(\d?\s*[А-Яа-яЁё.]+)\s+(\d+)\s*:\s*(\d+)(?:\s*[–\-—]\s*(\d+))?",
        ref,
    )
    if not m:
        return None
    book_raw = m.group(1).replace(".", "").replace(" ", "").lower()
    book = BOOK_ALIASES.get(book_raw)
    if not book:
        return None
    ch = int(m.group(2))
    first = int(m.group(3))
    last = int(m.group(4)) if m.group(4) else first
    return book, ch, first, last


def verse_text(verses, book, ch, first, last) -> tuple[str | None, list[int]]:
    spans, miss = [], []
    for v in range(first, last + 1):
        t = verses.get((book, ch, v))
        if t is None:
            miss.append(v)
        else:
            spans.append(t)
    if miss:
        return None, miss
    return " ".join(spans), []


def check_quote(quote: str, text: str) -> tuple[str, list[str]]:
    norm_quote = normalize(quote)
    segments = [s for s in (normalize(x) for x in ELLIPSIS.split(quote)) if s]
    if not segments:
        return "PARSE_FAIL", []
    norm_text = normalize(text)
    if len(segments) == 1:
        # Одиночный фрагмент: сверяем сегмент, а не строку с многоточием —
        # иначе цитата «…» на конце всегда считалась бы расхождением.
        if segments[0] in norm_text:
            return "EXACT", []
        return "MISMATCH", segments
    pos, missing = 0, []
    for seg in segments:
        idx = norm_text.find(seg, pos)
        if idx < 0:
            missing.append(seg)
        else:
            pos = idx + len(seg)
    if missing:
        return "MISMATCH", missing
    return "SEGMENTS", []


def collect(drafts: Path):
    out = []
    for path in sorted(drafts.glob("*.md")):
        lines = path.read_text(encoding="utf-8").splitlines()
        for lineno, line in enumerate(lines, 1):
            for m in CITE_RE.finditer(line):
                quote, paren = m.group(1).strip(), m.group(2)
                if "инодальн" not in paren:
                    continue
                if "ересказ" in paren:
                    continue
                ref_raw = paren.strip()
                ref_use, resolved_from = ref_raw, "paren"
                if parse_ref(ref_raw) is None:
                    # Пометка без адреса: ищем адрес стиха в самой строке — сначала до цитаты
                    # (ближайший), затем после неё. Это подсказка, а не доказательство: в отчёте
                    # источник адреса помечается отдельно.
                    pattern = (
                        r"(\d?\s*[А-Яа-яЁё.]{2,6}\.?\s*\d+\s*:\s*\d+(?:\s*[–\-—]\s*\d+)?)"
                    )
                    before = [c.group(1) for c in re.finditer(pattern, line[: m.start()])]
                    after = [c.group(1) for c in re.finditer(pattern, line[m.end():])]
                    for cand in list(reversed(before)) + after:
                        if parse_ref(cand):
                            ref_use, resolved_from = cand.strip(), "context"
                            break
                out.append(
                    {
                        "file": path.name,
                        "line": lineno,
                        "ref_raw": ref_raw,
                        "ref_use": ref_use,
                        "resolved_from": resolved_from,
                        "quote": quote,
                    }
                )
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--drafts", default="ИСКУПЛЕНИЕ/synthesis/drafts")
    ap.add_argument(
        "--bible",
        action="append",
        required=True,
        help=(
            "TSV Синодального; можно указать дважды (две независимые транскрипции). "
            "4 колонки: сокр., глава, стих, текст; 6 колонок: книга, сокр., № книги, глава, стих, текст"
        ),
    )
    ap.add_argument("--json", default=None, help="куда записать отчёт JSON")
    ap.add_argument("--check", action="store_true", help="код 1 при расхождениях цитат")
    ap.add_argument("--print-all", action="store_true", help="печатать и совпадения")
    args = ap.parse_args(argv)

    corpora = [(Path(b).name, load_bible(Path(b))) for b in args.bible]
    rows = collect(Path(args.drafts))

    good = {"EXACT", "SEGMENTS", "RANGE"}
    report = []
    for row in rows:
        ref = parse_ref(row["ref_use"])
        if ref is None:
            status = "NO_REF" if not re.search(r"\d+:\d+", row["ref_raw"]) else "PARSE_FAIL"
            row.update(status=status, per_corpus={}, verse_text=None, missing=[])
            report.append(row)
            continue

        book, ch, first, last = ref
        per_corpus, texts = {}, {}
        for name, verses in corpora:
            text, miss = verse_text(verses, book, ch, first, last)
            if text is None:
                per_corpus[name] = ("VERSE_MISSING", [str(v) for v in miss])
                continue
            status, missing = check_quote(row["quote"], text)
            if status == "EXACT" and last != first:
                status = "RANGE"
            per_corpus[name] = (status, missing)
            texts[name] = text

        statuses = {st for st, _ in per_corpus.values()}
        if statuses <= good:
            # Хотя бы один свод подтверждает цитату, и ни один не противоречит ей.
            status = "CONFIRMED" if len(statuses) == 1 else "CONFIRMED_MULTI"
        elif statuses & good:
            # Один свод подтверждает, другой нет: расхождение источников, а не приговора цитате.
            status = "SOURCE_CONFLICT"
        else:
            status = "NO_SOURCE_SUPPORTS"
        if "VERSE_MISSING" in statuses and "NO_SOURCE_SUPPORTS" not in statuses:
            status = "VERSE_MISSING"

        missing = []
        for st, miss in per_corpus.values():
            missing.extend(miss)
        row.update(
            status=status,
            per_corpus={k: v[0] for k, v in per_corpus.items()},
            verse_ref=f"{book} {ch}:{first}-{last}",
            verse_text=next(iter(texts.values()), None),
            missing=missing,
        )
        report.append(row)

    counts: dict[str, int] = {}
    for r in report:
        counts[r["status"]] = counts.get(r["status"], 0) + 1

    print(f"цитат с пометкой Синодального: {len(report)}")
    for k in sorted(counts):
        print(f"  {k}: {counts[k]}")
    bad = [r for r in report if r["status"] not in ("CONFIRMED", "CONFIRMED_MULTI", "NO_REF")]
    for r in report:
        if r["status"] not in ("CONFIRMED", "CONFIRMED_MULTI") or args.print_all:
            print(f"\n[{r['status']}] {r['file']}:{r['line']}  ({r['ref_raw']})")
            print(f"  цитата: {r['quote'][:220]}")
            if r.get("per_corpus"):
                print(f"  своды:  {r['per_corpus']}")
            if r.get("missing"):
                print(f"  не найдено: {' | '.join(s[:90] for s in r['missing'])}")
            if r.get("verse_text"):
                print(f"  стих:   {r['verse_text'][:300]}")

    if args.json:
        payload = {
            "generated": "2026-10-30",
            "drafts": args.drafts,
            "bibles": [str(b) for b in args.bible],
            "method": (
                "Каждый фрагмент в «ёлочках» с пометкой «Синодальный» сверяется с текстом стиха "
                "в каждой поданной транскрипции; расхождение считается установленным только там, "
                "где его подтверждают все поданные своды."
            ),
            "counts": counts,
            "citations": report,
        }
        Path(args.json).write_text(
            json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8"
        )
        print(f"\nотчёт записан: {args.json}")

    if args.check and bad:
        print(f"\nРАСХОЖДЕНИЙ: {len(bad)}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
