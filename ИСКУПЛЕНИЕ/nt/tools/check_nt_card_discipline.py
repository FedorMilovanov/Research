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
sys.dont_write_bytecode = True
import urllib.parse
from pathlib import Path

from nt_sources import ROOT, registry
from nt_refs import cards

NT_DIR = Path(__file__).resolve().parent.parent          # ИСКУПЛЕНИЕ/nt
DEPT_DIR = NT_DIR.parent                                  # ИСКУПЛЕНИЕ
# 10_ — ось предложения: карточки того же устройства, что 06_/07_/08_,
# поэтому контролируются тем же правилом (ось + ссылки + формулировки).
PERICOPE_FILES = ("06_", "07_", "08_", "10_")

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
    "πολλοί = как догмат": r"πολλοί\s*=\s*[^…\n]{3,}",
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
    for name in registry()["requiredMarkdownFiles"]:
        p = ROOT / name
        if not p.is_file():
            raise ValueError(f"required file missing: {p}")
        if p not in files:
            files.append(p)
    return files


def check_inventory(files: list[Path]) -> list[str]:
    problems = []
    if registry()["nonTextCards"] != ["08.34"]:
        problems.append("non-text exception drift: only the justified James silence card is registered")
    by_name = {p.name: p for p in files}
    for row in registry()["pericopeCards"]:
        path = ROOT / row["file"]
        if path.name not in by_name:
            problems.append(f"required pericope file missing: {path.name}")
            continue
        prefix = path.name[:2]
        expected = {f"{prefix}.{i}" for i in range(1, row["cards"] + 1)}
        expected |= {x.split()[0] for x in row.get("extraSections", [])}
        actual = [cid for cid, title, body in cards(by_name[path.name])]
        if len(actual) != len(set(actual)) or set(actual) != expected:
            problems.append(f"{path.name}: SSOT card inventory drift: expected {sorted(expected)}, found {actual}")
    return problems


def check_axis(files: list[Path]) -> tuple[int, list[str]]:
    total = 0
    problems: list[str] = []
    for p in files:
        if not p.name.startswith(PERICOPE_FILES):
            continue
        parts = re.split(r"(?m)^## ((?:0[678]|10)\.\d+ .+)$", p.read_text(encoding="utf-8"))
        for i in range(1, len(parts), 2):
            title, body = parts[i], parts[i + 1]
            total += 1
            m = re.search(r"\*\*Ось:\*\*([^\n]+)", body)
            if not m:
                problems.append(f"{p.name}: карточка «{title.strip()}» без метки оси")
            elif not set(re.findall(r"`([^`]+)`", m[1])) or set(re.findall(r"`([^`]+)`", m[1])) - set(registry()["axes"]):
                problems.append(f"{p.name}: карточка «{title.strip()}» без канонической оси")
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


def check_readings(files: list[Path]) -> tuple[int, list[str]]:
    """§3.3 брифа: ≥2 живых чтения ИЛИ явный `N` с объяснением.

    Бриф требует минимум два живых чтения, помеченных как particular и
    universal/general. Но он же говорит, что «не решает» — полный результат.
    Поэтому правило проверяемое и честное одновременно:

      - ≥2 помеченных чтения (`A`/`B`/`N`/`P`/`U`)  -> принято;
      - ровно одно и это `N`                        -> принято только если
        в карточке есть раздел «Что не доказывает» с содержательным ответом;
      - иначе                                       -> нарушение.

    Без второй ветки проверка требовала бы выдумывать второе чтение там, где
    текст просто не на оси объёма, — это было бы подкладкой, а не экзегезой.
    Без первой ветки одиночный `N` проходил бы и там, где текст на оси.
    """
    total = 0
    problems: list[str] = []
    for p in files:
        if not p.name.startswith(PERICOPE_FILES):
            continue
        text = p.read_text(encoding="utf-8")
        parts = re.split(r"(?m)^## ((?:0[678]|10)\.\d+ .+)$", text)
        for i in range(1, len(parts), 2):
            title, body = parts[i].strip(), parts[i + 1]
            # Требование §3.3 относится к карточкам ПЕРВИЧНОГО ТЕКСТА. Служебные
            # разделы (счётчики поля, синтез, сводка сверки) не цитируют один
            # стих и поэтому не могут иметь «чтений» этого стиха. Признак
            # структурный: у текстовой карточки есть блок «**Текст S1:**».
            if "**Текст S1:**" not in body and "**Текст S1 (" not in body:
                continue
            m = re.search(r"\*\*(?:Живые )?[Чч]тения[^\n*]*\*\*(.+?)(?=\n\*\*|\n---|\Z)",
                          body, re.S)
            seg = m.group(1) if m else ""
            labs = set(re.findall(r"`([ABNPU])`", seg))
            if len(labs) >= 2:
                total += 1
                continue
            m2 = re.search(r"\*\*Что не доказывает:\*\*\s*(.+)", body)
            explains = bool(m2) and len(m2.group(1).strip()) >= 12
            if len(labs) == 1 and labs == {"N"} and explains:
                total += 1
                continue
            total += 1
            problems.append(
                f"{p.name}: карточка «{title.split()[0]}» — чтений {len(labs)}"
                f"{'' if not labs else ' ' + '/'.join(sorted(labs))};"
                f" пояснения «что не доказывает» нет" if not explains else
                f"{p.name}: карточка «{title.split()[0]}» — на оси extent нужно ≥2 чтения")
    return total, problems


def check_method(files: list[Path]) -> tuple[int, list[str]]:
    """Structural floor, not a machine certificate of sound exegesis.

    Explicit context/OT boundaries may record a negative result. Primary
    quotes cannot be deleted to turn a text card into an unexamined service
    section. The one whole-book silence card is registered separately.
    """
    total, problems = 0, []
    nontext = set(registry()["nonTextCards"])
    for p in files:
        if not p.name.startswith(PERICOPE_FILES):
            continue
        for cid, title, body in cards(p):
            if cid.endswith(".0") or cid.startswith("10.") and int(cid.split(".")[1]) > 9:
                continue
            total += 1
            labels = re.findall(r"(?m)^\*\*([^\n]*?)\*\*", body)
            if cid not in nontext and not any(x.startswith("Текст S1") for x in labels):
                problems.append(f"{p.name}: {cid}: primary S1 quotation missing")
            for label, marker in [("syntax", r"[Сс]интаксис"), ("context", r"[Кк]онтекст"),
                                  ("OT boundary", r"Связь с ВЗ"), ("non-proof", r"Что не доказывает")]:
                blocks = list(re.finditer(r"(?m)^\*\*([^\n*]+)\*\*(.*?)(?=\n\*\*|\n---|\Z)", body, re.S))
                matching = [m[2].strip() for m in blocks if re.search(marker, m[1])]
                if not matching:
                    problems.append(f"{p.name}: {cid}: mandatory {label} block missing")
                elif not any(len(re.sub(r"[`*\s]", "", text)) >= 12 for text in matching):
                    problems.append(f"{p.name}: {cid}: mandatory {label} block empty/placeholder")
            quote = re.search(r"\*\*Текст S1[^\n*]*\*\*(.*?)(?=\n\*\*|\n---|\Z)", body, re.S)
            if cid not in nontext and (not quote or not re.search(r"`[^`]*[\u0370-\u03ff\u1f00-\u1fff][^`]*`", quote[1])):
                problems.append(f"{p.name}: {cid}: primary quotation empty")
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

    inventory_bad = check_inventory(files)
    card_n, axis_bad = check_axis(files)
    method_n, method_bad = check_method(files)
    links, link_bad = check_links(files)
    lines, forb_bad = check_forbidden(files)
    read_n, read_bad = check_readings(files)

    print(f"  карточек перикоп: {card_n}; без канонической оси: {len(axis_bad)}")
    print(f"  карточек с обязательными блоками: {method_n}; пропусков: {len(method_bad)}")
    print(f"  карточек с чтениями по §3.3: {read_n}; с нарушением: {len(read_bad)}")
    print(f"  относительных ссылок: {links}; битых: {len(link_bad)}")
    print(f"  строк просканировано: {lines}; запрещённых формулировок: {len(forb_bad)}")

    problems = inventory_bad + axis_bad + link_bad + forb_bad + read_bad + method_bad
    if problems:
        print(f"\nFAIL ({len(problems)})")
        for x in problems:
            print("  - " + x)
        return 1
    print("\nPASS: inventory, canonical axes, primary/syntax/context/OT/non-proof blocks, "
          "explicit readings and links; structural floor, not an exegesis certificate.")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (KeyError, OSError, ValueError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        sys.exit(1)
