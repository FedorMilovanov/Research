#!/usr/bin/env python3
"""Собрать RESEARCH/OPEN_HOLDS.md — сводку незакрытых HOLD-ов реестров.

Читает source-registry и claim-ledger, пишет Markdown-зеркало. Реестры не меняет.
Запуск:  python3 scripts/render_hold_ledger.py

Зеркало нужно затем, чтобы расхождение между тем, что заявлено в досье, и тем, что
действительно не проверено, было видно в один взгляд: HOLD, о котором забыли, — это
дыра, замаскированная под вывод.
"""

import datetime
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC_JSON = ROOT / "data" / "source-registry-v1.json"
CLM_JSON = ROOT / "data" / "claim-ledger-v1.json"
OUT = ROOT / "RESEARCH" / "OPEN_HOLDS.md"

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


def main():
    sources = json.loads(SRC_JSON.read_text(encoding="utf-8"))["sources"]
    claims = json.loads(CLM_JSON.read_text(encoding="utf-8"))["claims"]
    today = datetime.date.today().isoformat()

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
    out.append(f"Файл собран скриптом `scripts/render_hold_ledger.py` из `data/source-registry-v1.json` "
               f"и `data/claim-ledger-v1.json`; сборка от {today}. **Вручную не править** — при изменении "
               f"реестров пересобрать: `python3 scripts/render_hold_ledger.py`.")
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

    OUT.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"собрано: {OUT.relative_to(ROOT)}; "
          f"ARCHIVE={src_counts['ARCHIVE_HOLD']}/{clm_counts['ARCHIVE_HOLD']} "
          f"LOCATOR={src_counts['LOCATOR_HOLD']}/{clm_counts['LOCATOR_HOLD']} "
          f"EVIDENCE={src_counts['EVIDENCE_HOLD']}/{clm_counts['EVIDENCE_HOLD']} "
          f"RIGHTS={src_counts['RIGHTS_HOLD']}/{clm_counts['RIGHTS_HOLD']}")


if __name__ == "__main__":
    main()
