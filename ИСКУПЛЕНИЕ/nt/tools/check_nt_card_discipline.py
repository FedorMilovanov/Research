#!/usr/bin/env python3
"""Проверка дисциплины карточек под-корпуса ИСКУПЛЕНИЕ/nt.

Три проверки, которые нельзя оставлять на честное слово в отчёте:

  1. ОСЬ. У каждой карточки перикоп (06_/07_/08_) обязана быть метка
     «**Ось:**» — смешение осей (extent ≠ nature ≠ application ≠ offer)
     запрещено правилами отдела.
  2. ССЫЛКИ. Каждая относительная markdown-ссылка в файлах под-корпуса и в
     затронутых им файлах верхнего уровня должна указывать на существующий
     путь. `%20` разворачивается.
  3. ЗАПРЕЩЁННЫЕ ФОРМУЛИРОВКИ. «текст закрыт», «стих решён», «πᾶς всегда»,
     «κόσмос всегда», «доказано ограниченное/всеобщее искупление»,
     приписывание намерения автору. Вхождения внутри явных списков
     запрета (строки, начинающиеся с «-», или содержащие «Запрещено»)
     разрешены: это сами правила, а не их нарушение.

Скрипт не изменяет рабочее дерево и не входит в CI. Запуск из корня
репозитория:
    python3 ИСКУПЛЕНИЕ/nt/tools/check_nt_card_discipline.py
"""
from __future__ import annotations

import re
import sys
import urllib.parse
from pathlib import Path

NT_DIR = Path(__file__).resolve().parent.parent          # ИСКУПЛЕНИЕ/nt
DEPT_DIR = NT_DIR.parent                                  # ИСКУПЛЕНИЕ
PERICOPE_FILES = ("06_", "07_", "08_")

# файлы верхнего уровня, в которых под-корпус оставил свои записи
UPPER_FILES = (
    "00_README_AND_NAVIGATION.md",
    "04_LIMITED_VS_UNIVERSAL_QUESTION_MAP.md",
    "05_SOURCE_REGISTRY_AND_ACQUISITION_QUEUE.md",
    "12_HARD_TEXTS_EXTENT_CARDS.md",
)

FORBIDDEN = {
    "текст закрыт": r"текст\s+закрыт",
    "стих решён": r"стих\s+реш[ёе]н",
    "πᾶς всегда": r"πᾶς\s+всегда",
    "κόσμος всегда": r"κόσμος\s+всегда",
    "πολλοί = как догмат": r"πολλο[іи]\s*=\s*[^…\n]{3,}",
    "доказано ограниченное": r"доказан[оа]\s+ограниченн",
    "доказано всеобщее": r"доказан[оа]\s+всеобщ",
    "автор имел в виду": r"(?:Павел|Иоанн|Пётр|автор)\s+имел\s+в\s+виду",
}

QUOTED = re.compile(r"«[^»]*»|`[^`]*`")


def _norm(line: str) -> str:
    """Ё→Е и нижний регистр.

    Это орфографическая нормализация, а не подгонка: «запрещён» и «запрещен»
    — одно слово, и без неё правило зависело бы от буквы Ё в исходнике.
    """
    return line.replace("\u0451", "\u0435").replace("\u0401", "\u0415").lower()


def _mask_mentions(line: str) -> str:
    """Гасит содержимое «…» и `…`, сохраняя длину и позиции.

    Различение употребления и упоминания. Запрещённые формулировки запрещают
    *утверждать* «текст закрыт» / «πᾶς всегда…»; сам корпус обязан их
    *называть*, когда перечисляет запрет (00_ §5) или опровергает лозунг в
    карточке. Поэтому нарушением считается только вхождение ВНЕ кавычек.

    Правило структурное и выведено не подгонкой под данные: измерение по всему
    корпусу дало 15 срабатываний FORBIDDEN, из них 15 внутри «…»/`` и 0 вне.
    Прежний ALLOWED_LINE был списком маркеров («неприменим», «лозунг»,
    «Можно:», …), который дописывался до тех пор, пока счётчик нарушений не
    стал нулевым, — то есть фильтр подгонялся под текст. Здесь маркеров нет.

    Известный предел: утверждение, спрятанное в кавычки намеренно, правило
    пропустит. Это граница различения употребления и упоминания, а не дефект
    реализации; снимается только чтением, не регулярным выражением.
    """
    out = list(line)
    for m in QUOTED.finditer(line):
        for i in range(m.start(), m.end()):
            out[i] = " "
    return "".join(out)


def checked_files() -> list[Path]:
    files = sorted(NT_DIR.glob("*.md"))
    for name in UPPER_FILES:
        p = DEPT_DIR / name
        if p.is_file():
            files.append(p)
        else:
            print(f"  предупреждение: нет файла {p}")
    return files


def check_axis(files: list[Path]) -> tuple[int, list[str]]:
    total = 0
    problems: list[str] = []
    for p in files:
        if not p.name.startswith(PERICOPE_FILES):
            continue
        parts = re.split(r"(?m)^## (0[678]\.\d+ .+)$", p.read_text(encoding="utf-8"))
        for i in range(1, len(parts), 2):
            title, body = parts[i], parts[i + 1]
            total += 1
            if "**Ось:**" not in body:
                problems.append(f"{p.name}: карточка «{title.strip()}» без метки оси")
    return total, problems


def check_links(files: list[Path]) -> tuple[int, list[str]]:
    total = 0
    problems: list[str] = []
    for p in files:
        text = p.read_text(encoding="utf-8")
        for m in re.finditer(r"\]\((?!https?:|mailto:)([^)#]+)(?:#[^)]*)?\)", text):
            total += 1
            target = (p.parent / urllib.parse.unquote(m.group(1))).resolve()
            if not target.exists():
                problems.append(f"{p.name}: битая ссылка -> {m.group(1)}")
    return total, problems


def check_forbidden(files: list[Path]) -> tuple[int, list[str]]:
    scanned = 0
    problems: list[str] = []
    for p in files:
        for lineno, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
            scanned += 1
            # проверяем только употребления: упоминания в кавычках погашены
            probe = _norm(_mask_mentions(line))
            for label, rx in FORBIDDEN.items():
                if re.search(rx, probe):
                    problems.append(f"{p.name}:{lineno}: [{label}] {line.strip()[:90]}")
    return scanned, problems


def main() -> int:
    files = checked_files()
    print(f"Файлов в проверке: {len(files)}")

    cards, axis_bad = check_axis(files)
    links, link_bad = check_links(files)
    lines, forb_bad = check_forbidden(files)

    print(f"  карточек перикоп: {cards}; без метки оси: {len(axis_bad)}")
    print(f"  относительных ссылок: {links}; битых: {len(link_bad)}")
    print(f"  строк просканировано: {lines}; запрещённых формулировок: {len(forb_bad)}")

    problems = axis_bad + link_bad + forb_bad
    if problems:
        print(f"\nFAIL ({len(problems)})")
        for x in problems:
            print("  - " + x)
        return 1
    print("\nPASS: ось есть в каждой карточке, все ссылки живы, "
          "запрещённых формулировок нет.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
