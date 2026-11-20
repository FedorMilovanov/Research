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
    source-missing     источник не отдал величину (нет файла, упал скрипт);
    claim-broken       сломано само объявление: в шаблоне нет обещанной группы.

Три вида источника, и они ловят разное — поэтому перепутать их нельзя:

    external   машинный артефакт или вывод скрипта; он и есть истина, документ
               обязан ему соответствовать. Ловит дрейф документа.
    cross      другой документ (README против таблицы квитанций). Ловит дрейф
               одного из двух — но не обоих сразу.
    internal   проза против таблицы (или против числа хешей) внутри одного
               документа. Ловит расхождение слов с собственной таблицей и не
               ловит неверную таблицу: она не источник.

Печатается и разбивка по видам, чтобы «26 совпало» не читалось как «26 раз
проверено против независимых данных».

Отдельно печатается список величин, у которых источника нет вовсе. Они не
проверяются — но и не выдают себя за проверенные: у каждой названа причина,
почему её нельзя пересчитать из репозитория (размер объекта, снятый запросом к
Drive; число из имени файла, а не из подсчёта строк). Проверяется только то,
что фраза с таким числом на месте: исчезнувшее число — тоже дефект.

Якорь — часть работы, а не помеха. Переписали фразу, в которой стоит число,
— обновите якорь в объявлении; якорь обязан быть уникальным и не содержать
самого проверяемого числа (иначе подмена даёт `anchor-missing` вместо `stale`).
Обе ошибки скрипт называет, а не прячет.

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
        "files": r"Файлов с такими записями: (\d+)",
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


def prose_holds() -> int:
    """Записи, называющие HOLD прозой при пустом или отсутствующем `holds`."""
    out = _run(["python3", "-B", "scripts/audit_prose_holds.py", "--summary"])
    found = re.search(r"называющих HOLD в прозе[^:]*: (\d+)", out)
    if not found:
        raise RuntimeError("audit_prose_holds.py --summary не назвал число")
    return int(found.group(1))


def promotion_gaps() -> int:
    """Записи PROMOTE с объявленным пробелом в доказательствах."""
    out = _run(["python3", "-B", "scripts/audit_hold_coverage_gaps.py", "--promotion-gaps"])
    found = re.search(r"Записей PROMOTE с объявленным пробелом[^:]*: (\d+)", out)
    if not found:
        raise RuntimeError("--promotion-gaps не назвал число")
    return int(found.group(1))


def gate_counts() -> dict[str, int]:
    """Сколько гейтов и информационных счётчиков объявляет сам раннер."""
    import importlib.util as _iu
    spec = _iu.spec_from_file_location("_rg", ROOT / "scripts" / "run_research_gates.py")
    module = _iu.module_from_spec(spec)
    spec.loader.exec_module(module)
    return {"gates": len(module.GATES), "informational": len(module.INFORMATIONAL)}


def inventory_totals() -> dict[str, int]:
    """Итоги инвентаря — из сгенерированного JSON, а не из таблицы README."""
    data = json.loads((ROOT / "docs" / "research" / "holds" / "HOLD_INVENTORY.json").read_text(encoding="utf-8"))
    totals = data["totals"]
    return {"nodes": totals["json_nodes_with_holds"], "entries": totals["json_hold_entries"]}


def mirror_summary() -> dict[str, int]:
    """Строка сведения о зеркалах — из самого скрипта, а не из цитаты в записке."""
    out = _run(["python3", "-B", "scripts/check_drive_mirror_pairs.py", "--summary"])
    found = re.search(
        r"DRIVE MIRROR PAIRS: (\d+) записей, названных коммитов (\d+), отстают (\d+) "
        r"\(максимум (\d+) ревизий\), без ревизии (\d+)", out)
    if not found:
        raise RuntimeError("check_drive_mirror_pairs.py --summary не назвал ожидаемых чисел")
    names = ("records", "revisions", "lagging", "max_behind", "no_revision")
    return {name: int(found.group(i + 1)) for i, name in enumerate(names)}


def rule25_note() -> dict[str, int]:
    """Строка правила 25 — из валидатора, а не из цитаты в записке."""
    out = _run(["python3", "-B", "scripts/validate_atonement_corpus_integrity.py"])
    found = re.search(
        r"ПРАВИЛО 25 \(зеркала ланов\): (\d+) записей с gitFile, из них с названной ревизией "
        r"(\d+), с объявленным лагом (\d+)", out)
    if not found:
        raise RuntimeError("валидатор не напечатал строку «зеркала ланов»")
    return {"records": int(found.group(1)), "with_revision": int(found.group(2)),
            "lagging": int(found.group(3))}


def lag_split() -> dict[str, int]:
    """Сколько записей несут `lagBehindGit` и сколько из них объявляют лаг.

    Две величины, которые легко сложить в одну и потом читать неверно: поле есть у
    всех, кого касается вопрос, а «отстаёт» — только у части. Считается по индексу,
    а не по прозе записки.
    """
    data = json.loads((ROOT / "ИСКУПЛЕНИЕ" / "data" / "atonement-library-index.json").read_text(encoding="utf-8"))
    live_roles = {"lane-mirror", "ledger-mirror", "registry-mirror", "ssot-corpus-snapshot"}
    old_roles = {"registry-mirror-superseded", "superseded-mirror"}
    records = [r for r in data["records"] if "lagBehindGit" in r]
    live = [r for r in records if r.get("role") in live_roles]
    old = [r for r in records if r.get("role") in old_roles]
    return {
        "field_total": len(records),
        "live_field": len(live),
        "live_true": sum(1 for r in live if r["lagBehindGit"]),
        "old_field": len(old),
        "old_true": sum(1 for r in old if r["lagBehindGit"]),
    }


def holes_count() -> int:
    """Сколько случаев объявлены PASS-дырами — из самого скрипта батареи.

    Это дёшево (`--holes` не запускает прогон), поэтому число проверяемое. Числа
    самого прогона (поймано/непопаданий) — нет: он идёт восемь минут, и держать их
    в гейте значит платить восемью минутами за каждую правку документа.
    """
    out = _run(["python3", "-B", "scripts/run_atonement_mutation_battery.py", "--holes"])
    found = re.search(r"гейт не обязан ловить\): (\d+)", out)
    if not found:
        raise RuntimeError("--holes не назвал число")
    return int(found.group(1))


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


def receipts_totals() -> dict:
    """Числа квитанций хранения — из их JSON, а не из таблицы в прозе."""
    data = json.loads(
        (ROOT / "data" / "corpus-custody-receipts-2026-11-18.json").read_text(encoding="utf-8")
    )
    posting = data["sharingPosture"]["ancestors"]["totals"]
    return {
        "grand_total": posting["grandTotal"],
        "family_objects": posting["familyObjects"],
        "sections": data["corpusSectionsNotInLedger"]["corpus"]["childFolders"],
        "commons_bytes": data["corpora"][0]["aggregate"]["bytes"],
    }


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


def official_core_items() -> dict[str, int]:
    """Байты каждого из трёх наборов и их сумма — из JSON воспроизводимости.

    Заявленные байты лежат в документе статуса 2026-07-30; здесь важно, что
    проверенный размер (`bytes`) совпал с заявленным (`recordedBytes`), иначе
    цитата в записке и измерение расходятся.
    """
    data = json.loads(
        (ROOT / "data" / "official-core-datasets-reproducibility-2026-11-18.json").read_text(
            encoding="utf-8"
        )
    )
    out: dict[str, int] = {}
    for item in data["items"]:
        if item["bytes"] != item["recordedBytes"]:
            raise RuntimeError(f"{item['name']}: измерено {item['bytes']} ≠ заявлено {item['recordedBytes']}")
        out[item["repository"]] = int(item["bytes"])
    out["total"] = int(data["result"]["bytesTotal"])
    if out["total"] != sum(v for k, v in out.items() if k != "total"):
        raise RuntimeError("bytesTotal не равен сумме трёх наборов")
    return out


def artifact_custody() -> dict:
    """Снимок артефактов CI: итоги и раскладка по классам — из JSON, не из таблицы.

    Проверяет заодно две вещи, которые в документе только заявлены: число семей
    в итогах равно числу перечисленных семей, а сумма классов равна числу
    артефактов.
    """
    data = json.loads((ROOT / "data" / "artifact-custody-snapshot-2026-11-18.json").read_text(encoding="utf-8"))
    totals = data["totals"]
    if totals["families"] != len(data["families"]):
        raise RuntimeError(f"итог семей {totals['families']} ≠ перечислено {len(data['families'])}")
    if sum(totals["byClass"].values()) != totals["artifacts"]:
        raise RuntimeError(f"сумма классов {sum(totals['byClass'].values())} ≠ артефактов {totals['artifacts']}")
    out: dict = {
        "artifacts": totals["artifacts"],
        "families": len(data["families"]),
        "expired": totals["expired"],
        "gigabytes": f"{totals['bytes'] / 1e9:.2f}",
    }
    for cls, count in totals["byClass"].items():
        out["class:" + cls] = count
    return out


def crosscheck_hashes() -> int:
    """Полные 64-значные суммы, реально присутствующие в документе."""
    text = (HOLDS / "DRIVE_SHA256_READBACK_CROSSCHECK_2026-11-18.md").read_text(encoding="utf-8")
    return len(re.findall(r"`[0-9a-f]{64}`", text))



# Источники дорогие: валидатор корпуса идёт ~15 с, а `rule25_note` спрашивают три
# утверждения. Считаем один раз на прогон: иначе гейт платит за каждую цитату из
# одной и той же строки.
_CACHE: dict[str, object] = {}


def _memoize(fn):
    def wrapper(*args, **kwargs):
        if fn.__name__ not in _CACHE:
            _CACHE[fn.__name__] = fn(*args, **kwargs)
        return _CACHE[fn.__name__]
    return wrapper


for _name in ("holes_count", "audit_summary", "prose_holds", "promotion_gaps", "gate_counts", "inventory_totals",
              "receipts_totals", "matrix_numbers", "official_core_bytes", "official_core_matched",
              "crosscheck_hashes", "peter_registry", "mirror_summary", "rule25_note",
              "official_core_items", "artifact_custody"):
    globals()[_name] = _memoize(globals()[_name])


# --- утверждения --------------------------------------------------------------

CLAIMS: list[dict] = [
    {
        "id": "readme.gates_count",
        "doc": "README.md",
        "anchor": "гейтов +",
        "pattern": r"#\s*(\d+) гейтов \+ (\d+) информационных",
        "group": 1,
        "expected": lambda: gate_counts()["gates"],
        "source": "len(GATES) в scripts/run_research_gates.py",
    },
    {
        "id": "readme.informational_count",
        "doc": "README.md",
        "anchor": "гейтов +",
        "pattern": r"#\s*(\d+) гейтов \+ (\d+) информационных",
        "group": 2,
        "expected": lambda: gate_counts()["informational"],
        "source": "len(INFORMATIONAL) в scripts/run_research_gates.py",
    },
    {
        "id": "readme.claims_count",
        "doc": "README.md",
        "anchor": "с их источниками",
        "pattern": r"#\s*(\d+) (?:чисел|числа|число) с их источниками",
        "expected": lambda: len(CLAIMS),
        "source": "len(CLAIMS) в этом же скрипте — число, которое нельзя завысить",
    },
    {
        "id": "readme.summary_records",
        "doc": "README.md",
        "anchor": "и их раскладка",
        "pattern": r"#\s*(\d+) и их раскладка",
        "expected": lambda: audit_summary()["records"],
        "source": "audit_hold_coverage_gaps.py --summary",
    },
    {
        "id": "readme.no_holds_field",
        "doc": "README.md",
        "anchor": "без поля holds",
        "pattern": r"#\s*(\d+) без поля holds",
        "expected": lambda: audit_summary()["no_field"],
        "source": "audit_hold_coverage_gaps.py --no-holds-field",
    },
    {
        "id": "readme.prose_holds",
        "doc": "README.md",
        "anchor": "с HOLD в прозе",
        "pattern": r"#\s*(\d+) с HOLD в прозе",
        "expected": prose_holds,
        "source": "audit_prose_holds.py --summary",
    },
    {
        "id": "readme.promotion_gaps",
        "doc": "README.md",
        "anchor": "PROMOTE с пробелом",
        "pattern": r"#\s*(\d+) PROMOTE с пробелом",
        "expected": promotion_gaps,
        "source": "audit_hold_coverage_gaps.py --promotion-gaps",
    },
    {
        "id": "readme.inventory_nodes",
        "doc": "README.md",
        "anchor": "| `HOLD_INVENTORY.md` / `.json` |",
        "pattern": r"(\d[\d ]*) записей /",
        "expected": lambda: inventory_totals()["nodes"],
        "source": "HOLD_INVENTORY.json → totals.json_nodes_with_holds",
    },
    {
        "id": "readme.inventory_entries",
        "doc": "README.md",
        "anchor": "| `HOLD_INVENTORY.md` / `.json` |",
        "pattern": r"/ (\d[\d ]*) вхождений",
        "expected": lambda: inventory_totals()["entries"],
        "source": "HOLD_INVENTORY.json → totals.json_hold_entries",
    },
    {
        "id": "mirror_note.lane_mirror_records",
        "doc": "ИСКУПЛЕНИЕ/evidence/DOC_MIRRORS_EXPORT_TAILS_2026-11-18.md",
        "outside_holds": True,
        "anchor": "ПРАВИЛО 25 (зеркала ланов):",
        "pattern": r"ланов\): (\d+) записей с gitFile, из них с названной ревизией (\d+), с объявленным лагом (\d+)",
        "group": 1,
        "kind": "cross",
        "kindNote": "перекрёстная: цитата в записке против вывода валидатора",
        "expected": lambda: rule25_note()["records"],
        "source": "validate_atonement_corpus_integrity.py, строка «зеркала ланов», первое число",
    },
    {
        "id": "mirror_note.lane_mirror_with_revision",
        "doc": "ИСКУПЛЕНИЕ/evidence/DOC_MIRRORS_EXPORT_TAILS_2026-11-18.md",
        "outside_holds": True,
        "anchor": "ПРАВИЛО 25 (зеркала ланов):",
        "pattern": r"ланов\): (\d+) записей с gitFile, из них с названной ревизией (\d+), с объявленным лагом (\d+)",
        "group": 2,
        "kind": "cross",
        "kindNote": "перекрёстная: цитата в записке против вывода валидатора",
        "expected": lambda: rule25_note()["with_revision"],
        "source": "validate_atonement_corpus_integrity.py, строка «зеркала ланов», второе число",
    },
    {
        "id": "mirror_note.lane_mirror_lagging",
        "doc": "ИСКУПЛЕНИЕ/evidence/DOC_MIRRORS_EXPORT_TAILS_2026-11-18.md",
        "outside_holds": True,
        "anchor": "ПРАВИЛО 25 (зеркала ланов):",
        "pattern": r"ланов\): (\d+) записей с gitFile, из них с названной ревизией (\d+), с объявленным лагом (\d+)",
        "group": 3,
        "kind": "cross",
        "kindNote": "перекрёстная: цитата в записке против вывода валидатора",
        "expected": lambda: rule25_note()["lagging"],
        "source": "validate_atonement_corpus_integrity.py, строка «зеркала ланов», третье число",
    },
    {
        "id": "mirror_note.lag_field_total",
        "doc": "ИСКУПЛЕНИЕ/evidence/DOC_MIRRORS_EXPORT_TAILS_2026-11-18.md",
        "outside_holds": True,
        "anchor": "Проверяя, сколько записей вообще объявляют лаг",
        "pattern": r"получил \*\*(\d+)\*\*",
        "expected": lambda: lag_split()["field_total"],
        "source": "индекс библиотеки: записей с полем lagBehindGit",
    },
    {
        "id": "mirror_note.lag_live_field",
        "doc": "ИСКУПЛЕНИЕ/evidence/DOC_MIRRORS_EXPORT_TAILS_2026-11-18.md",
        "outside_holds": True,
        "anchor": "| «Зеркало отстаёт от дерева сейчас» |",
        "pattern": r"\| \*\*(\d+)\*\* \| \*\*(\d+)\*\* \|",
        "group": 1,
        "expected": lambda: lag_split()["live_field"],
        "source": "индекс: роли зеркал с полем lagBehindGit",
    },
    {
        "id": "mirror_note.lag_live_true",
        "doc": "ИСКУПЛЕНИЕ/evidence/DOC_MIRRORS_EXPORT_TAILS_2026-11-18.md",
        "outside_holds": True,
        "anchor": "| «Зеркало отстаёт от дерева сейчас» |",
        "pattern": r"\| \*\*(\d+)\*\* \| \*\*(\d+)\*\* \|",
        "group": 2,
        "expected": lambda: lag_split()["live_true"],
        "source": "индекс: из них lagBehindGit = true",
    },
    {
        "id": "mirror_note.lag_old_field",
        "doc": "ИСКУПЛЕНИЕ/evidence/DOC_MIRRORS_EXPORT_TAILS_2026-11-18.md",
        "outside_holds": True,
        "anchor": "| «Слепок отставал в момент заливки» |",
        "pattern": r"\| \*\*(\d+)\*\* \| \*\*(\d+)\*\* \|",
        "group": 1,
        "expected": lambda: lag_split()["old_field"],
        "source": "индекс: роли снятых слепков с полем lagBehindGit",
    },
    {
        "id": "mirror_note.lag_old_true",
        "doc": "ИСКУПЛЕНИЕ/evidence/DOC_MIRRORS_EXPORT_TAILS_2026-11-18.md",
        "outside_holds": True,
        "anchor": "| «Слепок отставал в момент заливки» |",
        "pattern": r"\| \*\*(\d+)\*\* \| \*\*(\d+)\*\* \|",
        "group": 2,
        "expected": lambda: lag_split()["old_true"],
        "source": "индекс: из них lagBehindGit = true",
    },
    {
        "id": "mirror_note.records",
        "doc": "ИСКУПЛЕНИЕ/evidence/DOC_MIRRORS_EXPORT_TAILS_2026-11-18.md",
        "outside_holds": True,
        "anchor": "Текущий вывод (дословно",
        "pattern": r"(\d+) записей, названных коммитов (\d+), отстают (\d+) \(максимум (\d+) ревизий\), без ревизии (\d+)",
        "group": 1,
        "kind": "cross",
        "kindNote": "перекрёстная: цитата в записке против вывода скрипта",
        "expected": lambda: mirror_summary()["records"],
        "source": "check_drive_mirror_pairs.py --summary, первое число",
    },
    {
        "id": "mirror_note.revisions",
        "doc": "ИСКУПЛЕНИЕ/evidence/DOC_MIRRORS_EXPORT_TAILS_2026-11-18.md",
        "outside_holds": True,
        "anchor": "Текущий вывод (дословно",
        "pattern": r"(\d+) записей, названных коммитов (\d+), отстают (\d+) \(максимум (\d+) ревизий\), без ревизии (\d+)",
        "group": 2,
        "kind": "cross",
        "kindNote": "перекрёстная: цитата в записке против вывода скрипта",
        "expected": lambda: mirror_summary()["revisions"],
        "source": "check_drive_mirror_pairs.py --summary, второе число",
    },
    {
        "id": "mirror_note.lagging",
        "doc": "ИСКУПЛЕНИЕ/evidence/DOC_MIRRORS_EXPORT_TAILS_2026-11-18.md",
        "outside_holds": True,
        "anchor": "Текущий вывод (дословно",
        "pattern": r"(\d+) записей, названных коммитов (\d+), отстают (\d+) \(максимум (\d+) ревизий\), без ревизии (\d+)",
        "group": 3,
        "kind": "cross",
        "kindNote": "перекрёстная: цитата в записке против вывода скрипта",
        "expected": lambda: mirror_summary()["lagging"],
        "source": "check_drive_mirror_pairs.py --summary, третье число",
    },
    {
        "id": "mirror_note.no_revision",
        "doc": "ИСКУПЛЕНИЕ/evidence/DOC_MIRRORS_EXPORT_TAILS_2026-11-18.md",
        "outside_holds": True,
        "anchor": "Текущий вывод (дословно",
        "pattern": r"(\d+) записей, названных коммитов (\d+), отстают (\d+) \(максимум (\d+) ревизий\), без ревизии (\d+)",
        "group": 5,
        "kind": "cross",
        "kindNote": "перекрёстная: цитата в записке против вывода скрипта",
        "expected": lambda: mirror_summary()["no_revision"],
        "source": "check_drive_mirror_pairs.py --summary, последнее число",
    },
    {
        "id": "triage.files",
        "doc": "UNDER_ACQUIRED_WITHOUT_HOLD_TRIAGE_2026-11-18.md",
        "anchor": "| Файлов |",
        "pattern": r"\| Файлов \| (\d+) \|",
        "expected": lambda: audit_summary()["files"],
        "source": "audit_hold_coverage_gaps.py --summary, строка «Файлов с такими записями»",
    },
    {
        "id": "readme.pass_holes",
        "doc": "README.md",
        "anchor": "не недоработка, а названные места",
        "pattern": r"(\d+) PASS-дыр — не недоработка",
        "expected": holes_count,
        "source": "run_atonement_mutation_battery.py --holes, строка «гейт не обязан ловить»",
    },
    {
        "id": "mirror_note.pass_holes",
        "doc": "ИСКУПЛЕНИЕ/evidence/DOC_MIRRORS_EXPORT_TAILS_2026-11-18.md",
        "outside_holds": True,
        "anchor": "PASS-дыр в прогоне",
        "pattern": r"(\d+) PASS-дыр в прогоне",
        "expected": holes_count,
        "source": "run_atonement_mutation_battery.py --holes, строка «гейт не обязан ловить»",
    },
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
        "kind": "cross",
        "kindNote": "перекрёстная: README против таблицы §13 квитанций — ловит дрейф одного из двух, не обоих",
        "doc": "README.md",
        "anchor": "с Drive по SHA-256 — сверено",
        "pattern": r"сверено (\d+) строк",
        "expected": lambda: receipts_catalog()["rows"],
        "source": "сумма столбца «Объектов» таблицы §13 квитанций",
    },
    {
        "id": "receipts.catalog_rows",
        "kind": "internal",
        "kindNote": "внутренняя: проза того же документа против его таблицы §13",
        "doc": "CORPUS_CUSTODY_RECEIPTS_2026-11-18.md",
        "anchor": "честная формулировка такая:",
        "pattern": r"сверено (\d+) строк",
        "expected": lambda: receipts_catalog()["rows"],
        "source": "сумма столбца «Объектов» таблицы §13 квитанций",
    },
    {
        "id": "receipts.catalog_full_matches",
        "kind": "internal",
        "kindNote": "внутренняя: проза того же документа против столбца «Совпало»",
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
        "id": "readme.sharing_grand_total",
        "doc": "README.md",
        "anchor": "доступ проверен у",
        "pattern": r"доступ проверен у (\d+)",
        "expected": lambda: receipts_totals()["grand_total"],
        "source": "data/corpus-custody-receipts JSON → sharingPosture.ancestors.totals.grandTotal",
    },
    {
        "id": "readme.sharing_family_objects",
        "doc": "README.md",
        "anchor": "объекта квитанций;",
        "pattern": r"(\d+) объекта квитанций",
        "expected": lambda: receipts_totals()["family_objects"],
        "source": "data/corpus-custody-receipts JSON → sharingPosture.ancestors.totals.familyObjects",
    },
    {
        "id": "readme.corpus_sections",
        "doc": "README.md",
        "anchor": "разделов корпуса",
        "pattern": r"(\d+) разделов корпуса",
        "expected": lambda: receipts_totals()["sections"],
        "source": "data/corpus-custody-receipts JSON → corpusSectionsNotInLedger.corpus.childFolders",
    },
    {
        "id": "receipts.commons_shard_bytes",
        "doc": "CORPUS_CUSTODY_RECEIPTS_2026-11-18.md",
        "anchor": "| **Итого** | 9 объектов |",
        "pattern": r"\*\*(\d[\d\s]*\d)\*\*",
        "expected": lambda: receipts_totals()["commons_bytes"],
        "source": "data/corpus-custody-receipts JSON → corpora[0].aggregate.bytes (сумма девяти шардов)",
    },
    {
        "id": "matrix.objects_vs_table",
        "kind": "internal",
        "kindNote": "внутренняя: проза §2 против таблицы категорий того же документа",
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
        "kind": "internal",
        "kindNote": "внутренняя: заявленное число против числа полных хешей в том же документе",
        "doc": "DRIVE_SHA256_READBACK_CROSSCHECK_2026-11-18.md",
        "anchor": "Зачем:** проверить снаружи",
        "pattern": r"Проверено (\d+) значений",
        "expected": crosscheck_hashes,
        "source": "число полных 64-значных хешей в самом документе",
    },
    # --- снимок артефактов CI: до этого числа не проверял никто ---------------
    {
        "id": "artifact_snapshot.artifacts",
        "doc": "ARTIFACT_CUSTODY_SNAPSHOT_2026-11-18.md",
        "anchor": "Живых артефактов (без отчётов сканера)",
        "pattern": r"\*\*(\d+)\*\* в",
        "expected": lambda: artifact_custody()["artifacts"],
        "source": "data/artifact-custody-snapshot JSON → totals.artifacts",
    },
    {
        "id": "artifact_snapshot.families",
        "doc": "ARTIFACT_CUSTODY_SNAPSHOT_2026-11-18.md",
        "anchor": "Живых артефактов (без отчётов сканера)",
        "pattern": r"\*\*(\d+)\*\* семьях",
        "expected": lambda: artifact_custody()["families"],
        "source": "data/artifact-custody-snapshot JSON → len(families), сверено с totals.families",
    },
    {
        "id": "artifact_snapshot.gigabytes",
        "doc": "ARTIFACT_CUSTODY_SNAPSHOT_2026-11-18.md",
        "anchor": "Живых артефактов (без отчётов сканера)",
        "pattern": r"суммарно \*\*([\d.]+) ГБ\*\*",
        "expected": lambda: artifact_custody()["gigabytes"],
        "source": "data/artifact-custody-snapshot JSON → totals.bytes / 1e9, два знака",
    },
    {
        "id": "artifact_snapshot.expired",
        "doc": "ARTIFACT_CUSTODY_SNAPSHOT_2026-11-18.md",
        "anchor": "Ноль здесь читается узко",
        "pattern": r"Просроченных: \*\*(\d+)\*\*",
        "expected": lambda: artifact_custody()["expired"],
        "source": "data/artifact-custody-snapshot JSON → totals.expired",
    },
    {
        "id": "artifact_snapshot.class_durable_on_drive",
        "doc": "ARTIFACT_CUSTODY_SNAPSHOT_2026-11-18.md",
        "anchor": "байты на Drive есть, квитанция записана",
        "pattern": r"\| `DURABLE_ON_DRIVE_RECEIPTED` \| (\d+) \|",
        "expected": lambda: artifact_custody()["class:DURABLE_ON_DRIVE_RECEIPTED"],
        "source": "data/artifact-custody-snapshot JSON → totals.byClass",
    },
    {
        "id": "artifact_snapshot.class_no_durable_destination",
        "doc": "ARTIFACT_CUSTODY_SNAPSHOT_2026-11-18.md",
        "anchor": "на Drive только манифест, объекты живут лишь в артефакте",
        "pattern": r"\| `NO_DURABLE_DESTINATION` \| (\d+) \|",
        "expected": lambda: artifact_custody()["class:NO_DURABLE_DESTINATION"],
        "source": "data/artifact-custody-snapshot JSON → totals.byClass",
    },
    {
        "id": "artifact_snapshot.class_regenerable_audit",
        "doc": "ARTIFACT_CUSTODY_SNAPSHOT_2026-11-18.md",
        "anchor": "пересобирается; потеря артефакта не теряет доказательство",
        "pattern": r"\| `REGENERABLE_AUDIT` \| (\d+) \|",
        "expected": lambda: artifact_custody()["class:REGENERABLE_AUDIT"],
        "source": "data/artifact-custody-snapshot JSON → totals.byClass",
    },
    # --- официальные наборы: заявленные байты и их сумма ---------------------
    {
        "id": "official_gaps.stepbible_bytes",
        "doc": "OFFICIAL_CORE_59_AND_LEDGER_GAPS_2026-11-18.md",
        "anchor": "| STEPBible Data snapshot |",
        "pattern": r"(\d[\d ]*) Б",
        "expected": lambda: official_core_items()["STEPBible/STEPBible-Data"],
        "source": "data/official-core-datasets-reproducibility JSON → items[0].bytes",
    },
    {
        "id": "official_gaps.morphhb_bytes",
        "doc": "OFFICIAL_CORE_59_AND_LEDGER_GAPS_2026-11-18.md",
        "anchor": "| Open Scriptures `morphhb` snapshot |",
        "pattern": r"(\d[\d ]*) Б",
        "expected": lambda: official_core_items()["openscriptures/morphhb"],
        "source": "data/official-core-datasets-reproducibility JSON → items[1].bytes",
    },
    {
        "id": "official_gaps.sblgnt_bytes",
        "doc": "OFFICIAL_CORE_59_AND_LEDGER_GAPS_2026-11-18.md",
        "anchor": "| Faithlife SBLGNT snapshot |",
        "pattern": r"(\d[\d ]*) Б",
        "expected": lambda: official_core_items()["Faithlife/SBLGNT"],
        "source": "data/official-core-datasets-reproducibility JSON → items[2].bytes",
    },
    {
        "id": "official_gaps.declared_total",
        "doc": "OFFICIAL_CORE_59_AND_LEDGER_GAPS_2026-11-18.md",
        "anchor": "| **Итого заявлено** |",
        "pattern": r"\*\*(\d[\d ]*) Б\*\*",
        "expected": lambda: official_core_items()["total"],
        "source": "data/official-core-datasets-reproducibility JSON → result.bytesTotal, сверено с суммой трёх",
    },
]


# --- величины, у которых источника нет: названы, а не спрятаны -----------------
#
# Число без источника в этом скрипте не проверяется — и не должно притворяться
# проверенным. Но и молчать о нём нельзя: читатель вправе знать, какие цифры
# раздела держатся на одном прочтении. Здесь перечислены те, что остались вне
# проверки, с причиной, по которой источника нет. Проверяется только одно:
# фраза с таким числом всё ещё на месте — исчезнувшее число тоже дефект.

UNSOURCED = [
    {
        "doc": "CORPUS_CUSTODY_RECEIPTS_2026-11-18.md",
        "anchor": "| Размер | 1 285 100 997 B |",
        "number": "1 285 100 997 B",
        "why": "размер объекта Drive снят get_file в момент сверки и в JSON квитанций не переносился; "
               "повторить его можно только запросом к Drive",
    },
    {
        "doc": "CORPUS_CUSTODY_RECEIPTS_2026-11-18.md",
        "anchor": "число 5 941 взято из имени файла, а не из подсчёта строк",
        "number": "5 941",
        "why": "взято из имени каталога `SINICHKIN — MASTER FILE CATALOG — 5941 FILES.csv`, "
               "а не подсчётом строк: сам каталог прочитан на 9 000 символов из 1 469 442",
    },
    {
        "doc": "README.md",
        "anchor": "38 строк каталога из 5 941 (0,64 %)",
        "number": "0,64 %",
        "why": "доля посчитана от 38 и 5 941; оба слагаемых названы, но 5 941 — из имени файла (см. выше)",
    },
    {
        "doc": "OFFICIAL_CORE_59_AND_LEDGER_GAPS_2026-11-18.md",
        "anchor": "| 123 193 373 | 2026-11-17T06:17:53Z",
        "number": "123 193 373",
        "why": "размер одного артефакта снят gh api в момент сверки, а снапшот хранит только сумму "
               "по семье; повторено вручную 2026-11-20 — артефакт на месте и число совпало, но "
               "командой в репозитории эта величина не закреплена, а семья с 2026-11-19 уже другая",
    },
    {
        "doc": "OFFICIAL_CORE_59_AND_LEDGER_GAPS_2026-11-18.md",
        "anchor": "| 899 703 400 | 2026-11-17T06:36:43Z",
        "number": "899 703 400",
        "why": "то же: размер отдельного артефакта из gh api, в снапшоте только сумма по семье; "
               "вручную 2026-11-20 совпало",
    },
    {
        "doc": "OFFICIAL_CORE_59_AND_LEDGER_GAPS_2026-11-18.md",
        "anchor": "разница 12 174 Б",
        "number": "12 174",
        "why": "разность между размером артефакта (без источника, см. выше) и заявленной суммой "
               "трёх наборов (та самая сумма проверяема); считается на месте, источника нет у "
               "уменьшаемого",
    },
]


def unsourced_report() -> list[tuple[str, str, str]]:
    """(id, состояние, пояснение) для каждой величины без источника."""
    out = []
    for item in UNSOURCED:
        path = HOLDS / item["doc"]
        text = path.read_text(encoding="utf-8") if path.exists() else ""
        hits = text.count(item["anchor"])
        if hits == 1:
            out.append((item["doc"], "unsourced-present", item["number"]))
        elif hits == 0:
            out.append((item["doc"], "unsourced-missing", item["number"]))
        else:
            out.append((item["doc"], "unsourced-ambiguous", item["number"]))
    return out



def plural(n: int, one: str, few: str, many: str) -> str:
    """Русская форма числительного: 1 утверждение, 2 утверждения, 31 утверждение, 11 утверждений."""
    if n % 10 == 1 and n % 100 != 11:
        return one
    if 2 <= n % 10 <= 4 and not 12 <= n % 100 <= 14:
        return few
    return many


def normalise(value: str) -> str:
    return re.sub(r"[\s\u00a0]", "", value)


def check(claim: dict, verbose: bool) -> tuple[str, str, str]:
    """Вернуть (состояние, что в документе, что в источнике)."""
    path = (ROOT / claim["doc"]) if claim.get("outside_holds") else (HOLDS / claim["doc"])
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
        if rows == 0:
            # Ноль строк значит, что таблица не найдена или сменила заголовок.
            # Сравнивать этот ноль с ожидаемым числом — значит объявлять дефект
            # документа там, где сломался якорь.
            return "anchor-missing", "—", "таблица под якорем не найдена"
        printed = rows
    else:
        found = re.search(claim["pattern"], hits[0])
        if not found:
            return "anchor-missing", "—", "в строке-якоре нет числа"
        try:
            printed = found.group(claim.get("group", 1))
        except IndexError:
            # Объявление обещает группу, которой в регулярке нет. Это дефект
            # объявления, а не документа, и он обязан быть назван, а не уронить
            # прогон трейсбеком: иначе гейт падает «непонятно почему».
            return "claim-broken", "—", f"в шаблоне нет группы {claim.get('group', 1)}"

    if normalise(str(printed)) == normalise(str(expected)):
        return "match", str(printed), str(expected)
    return "stale", str(printed), str(expected)


def main(argv: list[str]) -> int:
    verbose = "--verbose" in argv
    results = []
    for claim in CLAIMS:
        state, printed, expected = check(claim, verbose)
        results.append((claim, state, printed, expected))

    unsourced = unsourced_report()
    bad = [r for r in results if r[1] not in ("match",)]
    kinds = {"internal": 0, "cross": 0, "external": 0}
    for r in results:
        # Опечатка в `kind` не должна ронять счёт целиком: имя класса проверяется
        # так же, как числа, — иначе счётчик становится местом, где прячется дефект.
        kind = r[0].get("kind", "external")
        if kind not in kinds:
            print(f"  claim-broken     {r[0]['id']:30} неизвестный kind={kind!r}")
            return 1
        kinds[kind] += 1
    print(f"ЧИСЛА В ДОКУМЕНТАХ HOLD-КЛАСТЕРА: {len(results)} {plural(len(results), 'утверждение', 'утверждения', 'утверждений')} "
          f"(внешний источник {kinds['external']}, перекрёстная {kinds['cross']}, "
          f"внутри одного документа {kinds['internal']}), "
          f"совпало {sum(1 for r in results if r[1] == 'match')}, разошлось {len(bad)}")
    print(f"  вне проверки (источника нет, причина названа): {len(unsourced)} {plural(len(unsourced), 'величина', 'величины', 'величин')} — "
          + "; ".join(f"{u[2]} ({u[1]})" for u in unsourced))
    for claim, state, printed, expected in results:
        if state == "match" and not verbose:
            continue
        print(f"  {state:16} {claim['id']:30} документ={printed} источник={expected}")
        if state != "match":
            print(f"                   {claim['doc']}: {claim['source']}")

    # Якорь, содержащий само проверяемое число, — известная ловушка: подмена числа в
    # документе тогда даёт не `stale`, а `anchor-missing`, и проверка выглядит сломанной
    # вместо того, чтобы выглядеть поймавшей. Считаются только точные совпадения.
    def _in_anchor(value: str, anchor: str) -> bool:
        # Подстрокой проверять нельзя: «6» найдётся внутри «256». Нужны границы цифр.
        return bool(re.search(r"(?<!\d)" + re.escape(normalise(value)) + r"(?!\d)", normalise(anchor)))

    traps = [r[0]["id"] for r in results
             if r[1] == "match" and normalise(str(r[2])) and _in_anchor(str(r[2]), r[0]["anchor"])]
    if traps:
        print(f"  внимание: якорь содержит проверяемое число в {len(traps)} {plural(len(traps), 'утверждении', 'утверждениях', 'утверждениях')} — такая пара "
              f"даст anchor-missing вместо stale: {', '.join(traps)}")

    missing_unsourced = [u for u in unsourced if u[1] != "unsourced-present"]
    if missing_unsourced:
        for doc, state, number in missing_unsourced:
            print(f"  {state:16} {number:20} {doc}: фраза с числом без источника исчезла или размножилась")
        return 1

    if bad:
        print("\nЧисло в прозе перестало быть измерением. Либо пересчитать его источником, "
              "либо переписать фразу так, чтобы она перестала утверждать величину.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
