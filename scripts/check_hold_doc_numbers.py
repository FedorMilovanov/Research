#!/usr/bin/env python3
"""Сверить числа в документах HOLD-кластера с тем, из чего они взяты.

Зачем: за один день в этих документах нашлись три числа, которые разошлись с
действительностью молча — «44 записи 1 Петра» (такой развёртки нет ни в одном
режиме аудита), «сделано 6 сравнений из 5 941» (в квитанциях давно 38) и суммы
`official core`, проверенные по восьмизначному префиксу вместо полного хеша.
Во всех трёх случаях число было верным на момент, когда его записали, и
перестало быть верным потом, а заметить это было нечем: рядом с числом не
стояло ничего, что можно пересчитать.

Этот скрипт ставит рядом. Каждое утверждение — это:

* документ и уникальная строка-якорь в нём;
* регулярное выражение с одной группой — само число;
* источник: функция, которая пересчитывает ожидаемое значение заново;
* пояснение, откуда источник берёт величину.

Различаются пять состояний, и они не одно и то же:

    match              число в документе равно пересчитанному;
    stale              число разошлось с источником — это дефект;
    anchor-missing     строки-якоря нет: документ переписали, проверять нечего;
    anchor-ambiguous   якорь встречается дважды: непонятно, какое число сверять;
    source-missing     источник не отдал величину (нет файла, упал скрипт).

Скрипт ничего не правит. Он не решает, какое число верно: он показывает, где
число в прозе перестало быть измерением.

    python3 -B scripts/check_hold_doc_numbers.py            # проверить
    python3 -B scripts/check_hold_doc_numbers.py --verbose  # и показать источники
"""

from __future__ import annotations

import json
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
HOLDS = ROOT / "docs" / "research" / "holds"


# --- источники: пересчитывают ожидаемое значение -----------------------------


def _run(cmd: list[str]) -> str:
    proc = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    return (proc.stdout or "") + (proc.stderr or "")


def audit_summary() -> dict[str, int]:
    """Числа зеркального аудита HOLD — из его же вывода, а не из памяти."""
    out = _run(["python3", "-B", "scripts/audit_hold_coverage_gaps.py", "--summary"])
    numbers: dict[str, int] = {}
    patterns = {
        "records": r"Записей «объект не приобретён, HOLD не выставлен»: (\d+)",
        "declared": r"сами называют объём осмотра[^:]*: (\d+)",
        "silent": r"молчат о нём совсем: (\d+)",
        "no_field": r"записей без поля holds вовсе — (\d+)",
    }
    for key, pattern in patterns.items():
        found = re.search(pattern, out)
        if found:
            numbers[key] = int(found.group(1))
    return numbers


def receipts_catalog() -> dict[str, int]:
    """Строки каталога: сумма таблицы §13 квитанций, а не число из прозы."""
    text = (HOLDS / "CORPUS_CUSTODY_RECEIPTS_2026-11-18.md").read_text(encoding="utf-8")
    lines = text.splitlines()
    total = full = 0
    inside = False
    for line in lines:
        if line.startswith("| Что сверялось | Объектов | Совпало |"):
            inside = True
            continue
        if inside:
            if not line.startswith("|"):
                break
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) < 3 or set(cells[0]) <= set("-: "):
                continue
            try:
                objects = int(re.sub(r"\D", "", cells[1]) or 0)
            except ValueError:
                continue
            total += objects
            # «30 полных + 1 по префиксу» — полных меньше, чем объектов.
            head = cells[2].split("+")[0]
            try:
                full += int(re.sub(r"\D", "", head) or 0)
            except ValueError:
                full += objects
    return {"rows": total, "full": full}


def peter_registry() -> dict[str, int]:
    """Записи 1 Петра «объект не приобретён»: с пустым `holds` и без поля вовсе.

    Считается обходом самих файлов, а не по памяти: две схемы (`accessState` и
    `access_state`), четыре состояния приобретения, поле `holds` в трёх написаниях.
    Именно это число когда-то стояло в прозе как «44», не совпадая ни с одним
    режимом аудита.
    """
    states = {"PARTIAL_OBJECT", "CATALOG_ONLY", "LINK_ONLY", "NOT_ACQUIRED"}
    hold_keys = ("holds", "hold", "activeHolds", "active_holds")
    empty = no_field = 0
    for path in sorted((ROOT / "1_PETER_BOT").rglob("*.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            continue

        def walk(node):
            nonlocal empty, no_field
            if isinstance(node, dict):
                access = node.get("accessState") or node.get("access_state")
                if isinstance(access, str) and access.strip().upper() in states:
                    present = [k for k in hold_keys if k in node]
                    if present:
                        value = node[present[0]]
                        if isinstance(value, list) and not [v for v in value if str(v).strip()]:
                            empty += 1
                    else:
                        no_field += 1
                for value in node.values():
                    walk(value)
            elif isinstance(node, list):
                for value in node:
                    walk(value)

        walk(data)
    return {"empty_holds": empty, "no_field": no_field}


def matrix_numbers() -> dict[str, int]:
    """Объекты и категории матрицы прав — из JSON и из её собственной таблицы."""
    data = json.loads(
        (ROOT / "data" / "rights-determination-matrix-2026-11-18.json").read_text(encoding="utf-8")
    )
    rows: list[dict] = []

    def walk(node) -> None:
        if isinstance(node, dict):
            if isinstance(node.get("category"), str):
                rows.append(node)
            for value in node.values():
                walk(value)
        elif isinstance(node, list):
            for value in node:
                walk(value)

    walk(data)
    text = (HOLDS / "RIGHTS_DETERMINATION_MATRIX_2026-11-18.md").read_text(encoding="utf-8")
    table_sum = 0
    table_rows = 0
    inside = False
    for line in text.splitlines():
        if line.startswith("| Категория | Объектов |"):
            inside = True
            continue
        if inside:
            if not line.startswith("|"):
                break
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) < 2 or set(cells[0]) <= set("-: "):
                continue
            try:
                table_sum += int(cells[1])
            except ValueError:
                continue
            table_rows += 1
    return {
        "json_rows": len(rows),
        "json_categories": len({r["category"] for r in rows}),
        "table_sum": table_sum,
        "table_rows": table_rows,
    }


def official_core_bytes() -> int:
    data = json.loads(
        (ROOT / "data" / "official-core-datasets-reproducibility-2026-11-18.json").read_text(
            encoding="utf-8"
        )
    )
    return int(data["result"]["bytesTotal"])


def official_core_matched() -> str:
    data = json.loads(
        (ROOT / "data" / "official-core-datasets-reproducibility-2026-11-18.json").read_text(
            encoding="utf-8"
        )
    )
    result = data["result"]
    return f"{result['matched']}/{result['total']}"


def crosscheck_hashes() -> int:
    """Полные 64-значные суммы, реально присутствующие в документе."""
    text = (HOLDS / "DRIVE_SHA256_READBACK_CROSSCHECK_2026-11-18.md").read_text(encoding="utf-8")
    return len(re.findall(r"`[0-9a-f]{64}`", text))


# --- утверждения --------------------------------------------------------------

CLAIMS: list[dict] = [
    {
        "id": "triage.records",
        "doc": "UNDER_ACQUIRED_WITHOUT_HOLD_TRIAGE_2026-11-18.md",
        "anchor": "| Записей | **",
        "pattern": r"\*\*(\d+)\*\*",
        "expected": lambda: audit_summary()["records"],
        "source": "audit_hold_coverage_gaps.py --summary, строка «Записей»",
    },
    {
        "id": "triage.declared",
        "doc": "UNDER_ACQUIRED_WITHOUT_HOLD_TRIAGE_2026-11-18.md",
        "anchor": "| Объявляют объём осмотра сами |",
        "pattern": r"\*\*(\d+)\*\*",
        "expected": lambda: audit_summary()["declared"],
        "source": "audit_hold_coverage_gaps.py --summary, строка «сами называют объём»",
    },
    {
        "id": "triage.silent",
        "doc": "UNDER_ACQUIRED_WITHOUT_HOLD_TRIAGE_2026-11-18.md",
        "anchor": "| Молчат о нём |",
        "pattern": r"\*\*(\d+)\*\*",
        "expected": lambda: audit_summary()["silent"],
        "source": "audit_hold_coverage_gaps.py --summary, строка «молчат»",
    },
    {
        "id": "triage.no_holds_field",
        "doc": "UNDER_ACQUIRED_WITHOUT_HOLD_TRIAGE_2026-11-18.md",
        "anchor": "| поля `holds` нет вовсе | **",
        "pattern": r"\*\*(\d+)\*\*",
        "expected": lambda: audit_summary()["no_field"],
        "source": "audit_hold_coverage_gaps.py --no-holds-field",
    },
    {
        "id": "readme.catalog_rows",
        "doc": "README.md",
        "anchor": "с Drive по SHA-256 — сверено",
        "pattern": r"сверено (\d+) строк",
        "expected": lambda: receipts_catalog()["rows"],
        "source": "сумма столбца «Объектов» таблицы §13 квитанций",
    },
    {
        "id": "receipts.catalog_rows",
        "doc": "CORPUS_CUSTODY_RECEIPTS_2026-11-18.md",
        "anchor": "честная формулировка такая:",
        "pattern": r"сверено (\d+) строк",
        "expected": lambda: receipts_catalog()["rows"],
        "source": "сумма столбца «Объектов» таблицы §13 квитанций",
    },
    {
        "id": "receipts.catalog_full_matches",
        "doc": "CORPUS_CUSTODY_RECEIPTS_2026-11-18.md",
        "anchor": "**Итог одного блока:**",
        "pattern": r"\*\*(\d+) совпали по полному",
        "expected": lambda: receipts_catalog()["full"],
        "source": "столбец «Совпало» таблицы §13 без строк «по префиксу»",
    },
    {
        "id": "triage.peter_empty_holds",
        "doc": "UNDER_ACQUIRED_WITHOUT_HOLD_TRIAGE_2026-11-18.md",
        "anchor": "1 Петра с пустым `holds`",
        "pattern": r"\*\*(\d+) записей 1 Петра",
        "expected": lambda: peter_registry()["empty_holds"],
        "source": "обход 1_PETER_BOT/**/*.json: четыре состояния, поле holds есть и пусто",
    },
    {
        "id": "matrix.objects_vs_table",
        "doc": "RIGHTS_DETERMINATION_MATRIX_2026-11-18.md",
        "anchor": "Всего объектов: **",
        "pattern": r"Всего объектов: \*\*(\d+)\*\*",
        "expected": lambda: matrix_numbers()["table_sum"],
        "source": "сумма столбца «Объектов» таблицы категорий §2",
    },
    {
        "id": "matrix.categories_vs_json",
        "doc": "RIGHTS_DETERMINATION_MATRIX_2026-11-18.md",
        "anchor": "| `PD_WORK_MODERN_TRANSCRIPTION` |",
        "pattern": r"^\| `[A-Z_]+` \| (\d+) \|",
        "count_rows": True,
        "expected": lambda: matrix_numbers()["json_categories"],
        "source": "число различных `category` в data/rights-determination-matrix JSON",
    },
    {
        "id": "official_core.bytes_total",
        "doc": "OFFICIAL_CORE_DATASETS_REPRODUCIBILITY_2026-11-18.md",
        "anchor": "| **Итого** | | **",
        "pattern": r"\*\*(\d[\d\s]*\d)\*\*",
        "expected": lambda: official_core_bytes(),
        "source": "data/official-core-datasets-reproducibility JSON → result.bytesTotal",
    },
    {
        "id": "official_core.matched",
        "doc": "OFFICIAL_CORE_DATASETS_REPRODUCIBILITY_2026-11-18.md",
        "anchor": "| **Итого** | | **",
        "pattern": r"\*\*(\d+/\d+)\*\*",
        "expected": official_core_matched,
        "source": "data/official-core-datasets-reproducibility JSON → matched/total",
    },
    {
        "id": "crosscheck.full_hashes",
        "doc": "DRIVE_SHA256_READBACK_CROSSCHECK_2026-11-18.md",
        "anchor": "Зачем:** проверить снаружи",
        "pattern": r"Проверено (\d+) значений",
        "expected": crosscheck_hashes,
        "source": "число полных 64-значных хешей в самом документе",
    },
]


def normalise(value: str) -> str:
    return re.sub(r"[\s\u00a0]", "", value)


def check(claim: dict, verbose: bool) -> tuple[str, str, str]:
    """Вернуть (состояние, что в документе, что в источнике)."""
    path = HOLDS / claim["doc"]
    if not path.exists():
        return "source-missing", "—", f"нет файла {claim['doc']}"
    lines = path.read_text(encoding="utf-8").splitlines()
    hits = [line for line in lines if claim["anchor"] in line]
    if not hits:
        return "anchor-missing", "—", "якорь не найден"
    if len(hits) > 1:
        return "anchor-ambiguous", f"{len(hits)} строк", "якорь не уникален"
    try:
        expected = claim["expected"]()
    except Exception as error:  # источник обязан быть надёжнее документа
        return "source-missing", "—", f"{type(error).__name__}: {error}"

    if claim.get("count_rows"):
        text = path.read_text(encoding="utf-8")
        inside = False
        rows = 0
        for line in text.splitlines():
            if claim["anchor"] in line:
                inside = True
            if inside and re.match(claim["pattern"], line):
                rows += 1
            elif inside and rows and not line.startswith("|"):
                break
        printed = rows
    else:
        found = re.search(claim["pattern"], hits[0])
        if not found:
            return "anchor-missing", "—", "в строке-якоре нет числа"
        printed = found.group(1)

    if normalise(str(printed)) == normalise(str(expected)):
        return "match", str(printed), str(expected)
    return "stale", str(printed), str(expected)


def main(argv: list[str]) -> int:
    verbose = "--verbose" in argv
    results = []
    for claim in CLAIMS:
        state, printed, expected = check(claim, verbose)
        results.append((claim, state, printed, expected))

    bad = [r for r in results if r[1] not in ("match",)]
    print(f"ЧИСЛА В ДОКУМЕНТАХ HOLD-КЛАСТЕРА: {len(results)} утверждений, "
          f"совпало {sum(1 for r in results if r[1] == 'match')}, разошлось {len(bad)}")
    for claim, state, printed, expected in results:
        if state == "match" and not verbose:
            continue
        print(f"  {state:16} {claim['id']:30} документ={printed} источник={expected}")
        if state != "match":
            print(f"                   {claim['doc']}: {claim['source']}")

    if bad:
        print("\nЧисло в прозе перестало быть измерением. Либо пересчитать его источником, "
              "либо переписать фразу так, чтобы она перестала утверждать величину.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
