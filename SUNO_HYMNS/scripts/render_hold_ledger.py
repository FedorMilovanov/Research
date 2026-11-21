#!/usr/bin/env python3
"""Собрать RESEARCH/OPEN_HOLDS.md — сводку незакрытых HOLD-ов реестров.

Читает source-registry и claim-ledger, пишет Markdown-зеркало. Реестры не меняет.
Запись:  python3 scripts/render_hold_ledger.py
Проверка без записи: python3 scripts/render_hold_ledger.py --check
Проверка сохраняет дату готового снимка; это не новая сборка и не проверка прав.

Зеркало нужно затем, чтобы расхождение между тем, что заявлено в досье, и тем, что
действительно не проверено, было видно в один взгляд: HOLD, о котором забыли, — это
дыра, замаскированная под вывод.
"""

import argparse
import datetime
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC_JSON = ROOT / "data" / "source-registry-v1.json"
CLM_JSON = ROOT / "data" / "claim-ledger-v1.json"
OUT = ROOT / "RESEARCH" / "OPEN_HOLDS.md"

HEADER_PREFIX = (
    "Файл собран скриптом `scripts/render_hold_ledger.py` из `data/source-registry-v1.json` "
    "и `data/claim-ledger-v1.json`; сборка от "
)
HEADER_SUFFIX = (
    ". **Вручную не править** — при изменении "
    "реестров пересобрать: `python3 scripts/render_hold_ledger.py`."
)
HEADER_RE = re.compile(re.escape(HEADER_PREFIX) + r"(\d{4}-\d{2}-\d{2})" + re.escape(HEADER_SUFFIX))

HOLD_GLOSS = [
    ("ARCHIVE_HOLD",
     "источник существует, но содержание недоступно: пейволл, закрытый архив, недоступная "
     "книга, файл, который не удалось открыть"),
    ("LOCATOR_HOLD",
     "цитата есть, а точного локатора нет или он не сверен с печатным изданием: нет страницы, "
     "столбца, номера строки"),
    ("EVIDENCE_HOLD",
     "свидетельству не хватает силы: источник не приобретён, содержание известно по "
     "вторичному пересказу, утверждение держится на одном косвенном свидетельстве"),
    ("RIGHTS_HOLD",
     "права на воспроизведение не выяснены: цитировать минимально необходимым объёмом, "
     "целиком текст не перепечатывать"),
]

ACTIONABLE = ("ARCHIVE_HOLD", "LOCATOR_HOLD", "EVIDENCE_HOLD")


def recorded_date(text):
    """Accept only the generated header, never a date-like phrase in the body."""
    lines = text.splitlines()
    match = HEADER_RE.fullmatch(lines[2]) if len(lines) > 2 else None
    if match is None:
        raise ValueError("не распознан заголовок с датой сборки")
    return datetime.date.fromisoformat(match[1])


def render(sources, claims, generated_on):
    """Build the existing view in memory; no registry, output or clock writes."""
    src_counts = {k: 0 for k, _ in HOLD_GLOSS}
    clm_counts = {k: 0 for k, _ in HOLD_GLOSS}
    for s in sources:
        for h in s.get("holds", []):
            src_counts[h] = src_counts.get(h, 0) + 1
    for c in claims:
        for h in c.get("holds", []):
            clm_counts[h] = clm_counts.get(h, 0) + 1

    out = []
    out.append("# OPEN_HOLDS — открытые HOLD-ы реестров SUNO_HYMNS")
    out.append("")
    out.append(f"{HEADER_PREFIX}{generated_on.isoformat()}{HEADER_SUFFIX}")
    out.append("")
    out.append("Смысл сводки: HOLD — это обещание, которое ещё не исполнено. Список ниже — перечень "
               "того, что в текстах рубрики **нельзя** выдавать за проверенное.")
    out.append("")
    out.append("## Что означает каждый вид")
    out.append("")
    for name, gloss in HOLD_GLOSS:
        out.append(f"- `{name}` — {gloss}.")
    out.append("")
    out.append("## Сводка")
    out.append("")
    out.append("| Вид | У источников | У тезисов |")
    out.append("|---|---|---|")
    for name, _ in HOLD_GLOSS:
        out.append(f"| `{name}` | {src_counts.get(name, 0)} | {clm_counts.get(name, 0)} |")
    out.append("")
    out.append("`RIGHTS_HOLD` стоит почти на всём: это общая оговорка о правах, а не конкретная дыра. "
               "Отдельного внимания требуют три остальных вида.")
    out.append("")

    for name in ACTIONABLE:
        ss = [s for s in sources if name in s.get("holds", [])]
        cc = [c for c in claims if name in c.get("holds", [])]
        out.append(f"## `{name}`")
        out.append("")
        if ss:
            out.append("**Источники**")
            out.append("")
            for s in sorted(ss, key=lambda x: x["id"]):
                out.append(f"- `{s['id']}` — {s['title']}  ")
                out.append(f"  доступ: `{s['accessState']}`, локатор: `{s['locatorState']}`, "
                           f"права: `{s['rightsState']}`")
            out.append("")
        if cc:
            out.append("**Тезисы**")
            out.append("")
            for c in sorted(cc, key=lambda x: x["id"]):
                out.append(f"- `{c['id']}` — {c['topic']}  ")
                out.append(f"  статус: `{c['claimStatus']}`")
            out.append("")

    blocked = [s for s in sources
               if "RIGHTS_HOLD" in s.get("holds", [])
               and s.get("rightsState") in ("PERMISSION_REQUIRED", "RIGHTS_BLOCKED", "NOT_CLEARED")
               and s.get("accessState") != "FULL_OBJECT_VERIFIED"]
    out.append("## `RIGHTS_HOLD`: где права требуют отдельного решения")
    out.append("")
    if blocked:
        out.append("Источники, у которых права помечены как требующие разрешения или не выясненные "
                   "и при этом текст не прочитан полностью:")
        out.append("")
        for s in sorted(blocked, key=lambda x: x["id"]):
            out.append(f"- `{s['id']}` — {s['title']}  ")
            out.append(f"  доступ: `{s['accessState']}`, права: `{s['rightsState']}`")
        out.append("")
    else:
        out.append("Таких источников сейчас нет.")
        out.append("")

    out.append("## Порядок закрытия")
    out.append("")
    out.append("1. HOLD снимается только после того, как сделано дело: источник прочитан, "
               "локатор сверен, права выяснены. Формулировки «проверено» без этого не пишутся.")
    out.append("2. При снятии HOLD правится и реестр, и зеркала; затем этот файл пересобирается.")
    out.append("3. Если дыру закрыть нельзя (архив недоступен), она остаётся в списке и "
               "прямо оговаривается в тексте рубрики.")
    out.append("")

    return "\n".join(out) + "\n", src_counts, clm_counts


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="сверить снимок с реестрами без записи")
    args = parser.parse_args(argv)
    label = OUT.relative_to(ROOT) if OUT.is_relative_to(ROOT) else OUT
    try:
        on_disk = OUT.read_bytes().decode("utf-8") if args.check else None
        generated_on = recorded_date(on_disk) if args.check else datetime.date.today()
        sources = json.loads(SRC_JSON.read_text(encoding="utf-8"))["sources"]
        claims = json.loads(CLM_JSON.read_text(encoding="utf-8"))["claims"]
        text, src_counts, clm_counts = render(sources, claims, generated_on)
    except (OSError, UnicodeError, ValueError) as exc:
        print(f"SUNO hold ledger: FAIL — {label}: {exc}", file=sys.stderr)
        return 1

    if args.check:
        if on_disk != text:
            print(f"SUNO hold ledger: FAIL — {label} не соответствует реестрам; "
                  "пересобрать: python3 SUNO_HYMNS/scripts/render_hold_ledger.py", file=sys.stderr)
            return 1
        print(f"SUNO hold ledger: PASS — содержимое соответствует реестрам; "
              f"дата снимка {generated_on.isoformat()} сохранена, это не новая сборка")
        return 0

    try:
        OUT.write_bytes(text.encode("utf-8"))
    except OSError as exc:
        print(f"SUNO hold ledger: FAIL — {label}: {exc}", file=sys.stderr)
        return 1
    print(f"собрано: {label}; "
          f"ARCHIVE={src_counts['ARCHIVE_HOLD']}/{clm_counts['ARCHIVE_HOLD']} "
          f"LOCATOR={src_counts['LOCATOR_HOLD']}/{clm_counts['LOCATOR_HOLD']} "
          f"EVIDENCE={src_counts['EVIDENCE_HOLD']}/{clm_counts['EVIDENCE_HOLD']} "
          f"RIGHTS={src_counts['RIGHTS_HOLD']}/{clm_counts['RIGHTS_HOLD']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
