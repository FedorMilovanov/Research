#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Проверка локаторов-пересказов в черновиках «Искупления»: тот ли это стих.

Зачем этот файл существует. Два рода ошибок уже найдены в черновиках: испорченная
цитата (её ловит atonement_draft_citation_audit.py) и — отдельно — ссылка на стих,
который говорит другое. Второй род коварнее: текст черновика помечен «(пересказ)»,
поэтому сверка цитат его пропускает, а номер стиха при этом может быть неверным
(так Наум 1:3 был назван 1:2) или стих может вообще не иметь отношения к мысли.

Что делает скрипт. Он не выносит богословских суждений. Он берёт каждый адрес стиха
в черновике вместе с окружением (окно строки), вычитает из окружения сам адрес,
служебные пометки и стоп-слова, и сравнивает оставшиеся слова с текстом названного
стиха: сколько слов пересказа вообще встречается в стихе. Низкое совпадение — не
приговор, а сигнал: такое место надо прочитать руками. Высокое совпадение тоже не
доказательство: пересказ может совпадать словами и расходиться смыслом.

Порог. Место попадает в список на чтение, если (а) совпало меньше 20% слов пересказа
и стих не короче восьми слов, или (б) в стихе нет ни одного слова пересказа, или
(в) стих не найден по адресу. Это намеренно щедро: лучше прочитать лишнее.

Команды:
  --list    только список сигналов (по умолчанию);
  --all     все адреса с коэффициентом;
  --json    записать отчёт.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

BOOK_ALIASES = {
    "быт": "Быт", "исх": "Исх", "лев": "Лев", "чис": "Чис", "втор": "Втор", "нав": "Нав",
    "суд": "Суд", "руф": "Руф", "1цар": "1Цар", "2цар": "2Цар", "3цар": "3Цар", "4цар": "4Цар",
    "1пар": "1Пар", "2пар": "2Пар", "езд": "Езд", "неем": "Неем", "есф": "Есф", "иов": "Иов",
    "пс": "Пс", "прит": "Прит", "притч": "Прит", "еккл": "Еккл", "песн": "Песн", "ис": "Ис",
    "иер": "Иер", "плач": "Плач", "иез": "Иез", "дан": "Дан", "ос": "Ос", "иоил": "Иоил",
    "ам": "Ам", "авд": "Авд", "ион": "Ион", "мих": "Мих", "наум": "Наум", "авв": "Ав",
    "соф": "Соф", "агг": "Аг", "зах": "Зах", "мал": "Мал",
    "мф": "Мф", "матф": "Мф", "мк": "Мк", "лк": "Лк", "ин": "Ин", "деян": "Деян",
    "иак": "Иак", "1пет": "1Пет", "2пет": "2Пет", "1ин": "1Ин", "2ин": "2Ин", "3ин": "3Ин",
    "иуд": "Иуд", "рим": "Рим", "1кор": "1Кор", "2кор": "2Кор", "гал": "Гал", "еф": "Еф",
    "фил": "Фил", "флп": "Фил", "кол": "Кол", "1фес": "1Фес", "2фес": "2Фес", "1тим": "1Тим",
    "2тим": "2Тим", "тит": "Тит", "флм": "Флм", "евр": "Евр", "откр": "Откр",
}

REF_RE = re.compile(
    r"(\d?\s*[А-Яа-яЁё]{2,8})\.?\s*(\d+)\s*:\s*(\d+)(?:\s*[–\-—]\s*(\d+))?"
)

STOP = set(
    """и в во не что он на я с со как а то все она так его но да ты к у же вы за бы по
    только ее мне было вот от меня еще нет о из ему теперь когда даже ну вдруг ли если
    уже или ни быть был него до вас нибудь опять уж вам ведь там потом себя ничего ей
    может они тут где есть надо ней для мы тебя их чем была сам чтоб без будто чего раз
    тоже себе под будет ж тогда кто этот того потому этого какой совсем ним здесь этом
    один почти мой тем чтобы нее сейчас были куда зачем всех никогда можно при наконец
    два об другой хоть после над больше тот через эти нас про всего них какая много
    разве три эту моя впрочем хорошо свою этой перед иногда лучше чуть том нельзя такой
    им более всегда конечно всю между это который которые которая которое которых
    является этот эта эти того тому этим сие сей оный""".split()
)


def normalize_words(text: str) -> list[str]:
    text = text.lower().replace("ё", "е")
    text = re.sub(r"[^а-яa-z0-9 ]+", " ", text)
    out = []
    for w in text.split():
        if len(w) >= 5 and w not in STOP:
            out.append(w[:5])  # грубая основа: первые пять букв
    return out


def load_bible(path: Path) -> dict[tuple[str, int, int], str]:
    verses: dict[tuple[str, int, int], str] = {}
    with path.open(encoding="utf-8") as fh:
        for raw in fh:
            parts = raw.rstrip("\n").split("\t")
            if len(parts) == 4:
                abbr, ch, vs, text = parts
            elif len(parts) >= 6:
                _, abbr, _no, ch, vs, text = parts[:6]
            else:
                continue
            try:
                verses[(abbr, int(ch), int(vs))] = text
            except ValueError:
                continue
    return verses


def verse_span(verses, book, ch, first, last):
    parts, missing = [], []
    for v in range(first, last + 1):
        t = verses.get((book, ch, v))
        if t is None:
            missing.append(v)
        else:
            parts.append(t)
    return (" ".join(parts) if parts else None), missing


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--drafts", default="ИСКУПЛЕНИЕ/synthesis/drafts")
    ap.add_argument("--bible", required=True)
    ap.add_argument("--all", action="store_true", help="печатать все адреса, не только сигналы")
    ap.add_argument("--json", default=None)
    args = ap.parse_args(argv)

    verses = load_bible(Path(args.bible))
    rows = []
    for path in sorted(Path(args.drafts).glob("*.md")):
        for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            matches = list(REF_RE.finditer(line))
            for idx, m in enumerate(matches):
                book = BOOK_ALIASES.get(m.group(1).strip().lower().replace(".", ""))
                if not book:
                    continue
                ch, first = int(m.group(2)), int(m.group(3))
                last = int(m.group(4)) if m.group(4) else first
                text, missing = verse_span(verses, book, ch, first, last)
                # Окно — клауза вокруг адреса: от конца предыдущего адреса до начала
                # следующего, но не шире 180 знаков в каждую сторону. Сам адрес вырезан.
                lo = matches[idx - 1].end() if idx else 0
                hi = matches[idx + 1].start() if idx + 1 < len(matches) else len(line)
                lo, hi = max(lo, m.start() - 180), min(hi, m.end() + 180)
                window = line[lo:m.start()] + " " + line[m.end():hi]
                draft_words = set(normalize_words(window))
                if not text:
                    verdict = "VERSE_MISSING"
                    ratio = 0.0
                else:
                    verse_words = set(normalize_words(text))
                    if not draft_words:
                        continue
                    shared = draft_words & verse_words
                    ratio = len(shared) / len(draft_words)
                    if not shared:
                        verdict = "NO_SHARED_WORDS"
                    elif ratio < 0.20 and len(normalize_words(text)) >= 8:
                        verdict = "LOW_OVERLAP"
                    else:
                        verdict = "OK"
                rows.append(
                    {
                        "file": path.name,
                        "line": lineno,
                        "ref": f"{book} {ch}:{first}" + (f"-{last}" if last != first else ""),
                        "ratio": round(ratio, 3),
                        "verdict": verdict,
                        "draft": re.sub(r"\s+", " ", window).strip()[:300],
                        "verse": (text or "")[:300],
                        "missing": missing,
                    }
                )

    flagged = [r for r in rows if r["verdict"] != "OK"]
    counts: dict[str, int] = {}
    for r in rows:
        counts[r["verdict"]] = counts.get(r["verdict"], 0) + 1
    print(f"адресов стихов в черновиках: {len(rows)}")
    for k in sorted(counts):
        print(f"  {k}: {counts[k]}")
    print()
    show = rows if args.all else flagged
    for r in show:
        if r["verdict"] == "OK" and not args.all:
            continue
        print(f"[{r['verdict']} {r['ratio']}] {r['file']}:{r['line']}  {r['ref']}")
        print(f"   черновик: {r['draft'][:220]}")
        print(f"   стих:     {r['verse'][:220]}")
        print()

    if args.json:
        Path(args.json).write_text(
            json.dumps(
                {
                    "generated": "2026-10-30",
                    "method": (
                        "Сравнение словаря пересказа с словарём названного стиха. Порог — сигнал "
                        "к чтению, не приговор: совпадение слов не доказывает совпадения смысла, "
                        "а расхождение слов не доказывает ошибки."
                    ),
                    "counts": counts,
                    "refs": rows,
                },
                ensure_ascii=False,
                indent=1,
            ),
            encoding="utf-8",
        )
        print(f"отчёт записан: {args.json}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
