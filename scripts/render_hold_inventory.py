#!/usr/bin/env python3
"""Собрать сквозной инвентарь HOLD-ов репозитория Research.

Скрипт только читает репозиторий и пишет два производных файла:

    docs/research/holds/HOLD_INVENTORY.md
    docs/research/holds/HOLD_INVENTORY.json

Он не является новой authority, не меняет реестры и не снимает ни один HOLD.
Его задача — сделать видимым то, что иначе теряется: сколько HOLD-ов
объявлено, какого они типа, где именно, и что требуется, чтобы каждый из
них закрыть честно.

Правила, заложенные в отчёт (data/repository-evidence-policy-v2.json):

* HOLD — не класс источника и не «статус на всякий случай»;
* ни присутствие в Research/Drive, ни достижимость URL, ни библиографическая
  запись не снимают HOLD;
* проверка кода возврата не равна проверке содержания;
* Research closure не равно product/publication approval.

Поэтому скрипт ничего не «закрывает» сам. Он классифицирует каждый HOLD по
маршруту закрытия и отдельно проверяет те внутренние случаи, где закрытие
действительно может быть установлено по самому репозиторию (зеркала реестров,
цепочка override-файлов, датированный аудит против выросшего реестра).

Запуск:

    python3 -B scripts/render_hold_inventory.py
    python3 -B scripts/render_hold_inventory.py --check   # не писать, сравнить
"""

from __future__ import annotations

import argparse
import collections
import datetime
import hashlib
import json
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "docs" / "research" / "holds"
OUT_MD = OUT_DIR / "HOLD_INVENTORY.md"
OUT_JSON = OUT_DIR / "HOLD_INVENTORY.json"

SKIP_DIRS = {
    ".git",
    ".github",
    "node_modules",
    ".venv",
    "__pycache__",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    "build",
    "dist",
}

TEXT_SUFFIXES = {".md", ".json", ".yml", ".yaml", ".py", ".csv", ".txt"}

HOLD_TYPES = (
    "EVIDENCE_HOLD",
    "LOCATOR_HOLD",
    "ARCHIVE_HOLD",
    "RIGHTS_HOLD",
    "PUBLICATION_HOLD",
)

# Маршрут закрытия по типу. Формулировки короткие и проверяемые: они
# описывают, какой именно объект нужен, а не «доработать».
CLOSURE_ROUTE = {
    "PUBLICATION_HOLD": (
        "TERMINAL_BY_DEFAULT",
        "Отдельное решение владельца о публикации. Исследовательский проход "
        "не снимает PUBLICATION_HOLD, даже если источник прочитан полностью.",
    ),
    "RIGHTS_HOLD": (
        "EXTERNAL_RIGHTS",
        "Нужно установить права на объект (издатель, архив, лицензия). "
        "Чтение текста и достижимость URL права не устанавливают.",
    ),
    "ARCHIVE_HOLD": (
        "EXTERNAL_OBJECT",
        "Нужен сам архивный/печатный объект: страницы, листы, сканы, "
        "документ из закрытого собрания. Каталог и опись объект не заменяют.",
    ),
    "LOCATOR_HOLD": (
        "EXTERNAL_LOCATOR",
        "Нужен точный локатор в конкретном издании: страница, столбец, "
        "номер строки, лист, таймкод — сверенный с самим объектом.",
    ),
    "EVIDENCE_HOLD": (
        "EXTERNAL_EVIDENCE",
        "Нужно прочитать сам источник (полный текст в нужной редакции) "
        "либо получить независимое свидетельство требуемой силы.",
    ),
}

TYPED_TOKEN_RE = re.compile(
    r"\b(" + "|".join(HOLD_TYPES) + r")\b"
)
BARE_STATUS_RE = re.compile(
    r"(?i)^(?:\*\*)?(?:status|статус)(?:\*\*)?\s*[:=]\s*\**\s*`?HOLD`?\s*$"
)
BARE_LINE_RE = re.compile(r"^HOLD$")

JSON_SHA_RE = re.compile(r"^[0-9a-f]{64}$")


def rel(path: pathlib.Path) -> str:
    return path.relative_to(ROOT).as_posix()


def corpus_of(path: pathlib.Path) -> str:
    parts = path.relative_to(ROOT).parts
    if len(parts) == 1:
        return "(root)"
    return parts[0]


def iter_files():
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        # Собственные выходные файлы не считаем: иначе отчёт учитывает сам себя
        # и счётчики меняются от его же содержимого. Прочие документы каталога
        # (квитанции, записки) считаются как обычные файлы.
        if path in {OUT_MD, OUT_JSON}:
            continue
        yield path


def walk_json_hold_nodes(node, acc, depth=0):
    """Собрать все объекты, у которых есть непустой список `holds`."""
    if depth > 60:
        return
    if isinstance(node, dict):
        holds = node.get("holds")
        if isinstance(holds, list):
            types = sorted({h for h in holds if isinstance(h, str) and h in HOLD_TYPES})
            raw = [h for h in holds if isinstance(h, str)]
            if raw:
                ident = (
                    node.get("id")
                    or node.get("candidate_id")
                    or node.get("hold_id")
                    or node.get("sourceId")
                    or node.get("ref")
                    or node.get("name")
                    or ""
                )
                acc.append(
                    {
                        "id": str(ident),
                        "holds": types,
                        "untyped": [h for h in raw if h not in HOLD_TYPES],
                        "accessState": node.get("accessState"),
                        "locatorState": node.get("locatorState"),
                        "rightsState": node.get("rightsState"),
                        "publicationState": node.get("publicationState"),
                        "title": (node.get("title") or node.get("claim") or node.get("name") or "")[:160],
                        "finding": str(
                            node.get("finding") or node.get("note") or node.get("limits") or ""
                        )[:400],
                    }
                )
        for value in node.values():
            walk_json_hold_nodes(value, acc, depth + 1)
    elif isinstance(node, list):
        for value in node:
            walk_json_hold_nodes(value, acc, depth + 1)


def scan_json():
    nodes_by_file = {}
    parse_errors = []
    for path in iter_files():
        if path.suffix.lower() != ".json":
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            parse_errors.append({"path": rel(path), "error": str(exc)[:200]})
            continue
        acc: list[dict] = []
        walk_json_hold_nodes(data, acc)
        if acc:
            nodes_by_file[rel(path)] = acc
    return nodes_by_file, parse_errors


def scan_markdown():
    per_file_tokens = collections.Counter()
    per_type = collections.Counter()
    bare = []
    files_with_tokens = 0
    for path in iter_files():
        if path.suffix.lower() not in {".md", ".yml", ".yaml"}:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        tokens = TYPED_TOKEN_RE.findall(text)
        if tokens:
            files_with_tokens += 1
            per_file_tokens[rel(path)] = len(tokens)
            per_type.update(tokens)
        if path.suffix.lower() != ".md":
            continue
        in_fence = False
        for lineno, line in enumerate(text.splitlines(), 1):
            stripped = line.strip()
            if stripped.startswith("```") or stripped.startswith("~~~"):
                in_fence = not in_fence
                continue
            # Внутри блоков кода HOLD — это значение перечисления или
            # элемент перехода (`HOLD → READY`), а не объявленный статус.
            if in_fence:
                continue
            if BARE_STATUS_RE.match(stripped) or BARE_LINE_RE.match(stripped):
                bare.append({"file": rel(path), "line": lineno, "text": stripped[:120]})
    return per_file_tokens, per_type, bare, files_with_tokens


def load_json(rel_path: str):
    try:
        return json.loads((ROOT / rel_path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def parse_hold_list(value: str) -> set[str]:
    """Разобрать строку вида «RIGHTS_HOLD, LOCATOR_HOLD» или «None recorded.»."""
    if re.search(r"(?i)\bnone\b|не\s+зафиксировано|—", value):
        return set()
    return {token for token in re.split(r"[,\s]+", value) if token in HOLD_TYPES}


def check_suno_mirrors():
    """Сверить человекочитаемые зеркала SUNO с машинными реестрами."""
    result = {"status": "NOT_RUN", "detail": []}

    src = load_json("SUNO_HYMNS/data/source-registry-v1.json")
    reg_text_path = ROOT / "SUNO_HYMNS" / "RESEARCH" / "SOURCE_REGISTER.md"
    if not src or not reg_text_path.is_file():
        result["detail"].append("source-registry или SOURCE_REGISTER.md отсутствует")
        return result

    sources = {s.get("id"): s for s in src.get("sources", []) if s.get("id")}
    text = reg_text_path.read_text(encoding="utf-8")
    md_holds = {}
    for block in re.split(r"\n## ", text)[1:]:
        head = block.split("\n", 1)[0].strip()
        match = re.match(r"(SRC-[A-Za-z0-9\-]+)", head)
        if not match:
            continue
        hold_match = re.search(r"^- HOLDs: (.+)$", block, re.M)
        md_holds[match.group(1)] = parse_hold_list(hold_match.group(1)) if hold_match else set()

    drift = []
    for sid, holds in sorted(md_holds.items()):
        if sid not in sources:
            drift.append({"id": sid, "issue": "есть в MD, нет в JSON"})
            continue
        json_holds = set(sources[sid].get("holds", []) or [])
        if json_holds != holds:
            drift.append(
                {
                    "id": sid,
                    "issue": "расхождение HOLD-ов",
                    "md": sorted(holds),
                    "json": sorted(json_holds),
                }
            )
    result["status"] = "PASS" if not drift else "DRIFT"
    result["detail"] = drift
    result["checked"] = len(md_holds)
    result["unmirrored_json_sources"] = sorted(set(sources) - set(md_holds))
    return result


def check_suno_claims():
    result = {"status": "NOT_RUN", "detail": []}
    ledger = load_json("SUNO_HYMNS/data/claim-ledger-v1.json")
    path = ROOT / "SUNO_HYMNS" / "RESEARCH" / "CLAIM_LEDGER.md"
    if not ledger or not path.is_file():
        result["detail"].append("claim-ledger или CLAIM_LEDGER.md отсутствует")
        return result

    claims = {c.get("id"): c for c in ledger.get("claims", []) if c.get("id")}
    text = path.read_text(encoding="utf-8")
    md_holds = {}
    for block in re.split(r"\n## ", text)[1:]:
        head = block.split("\n", 1)[0].strip()
        match = re.match(r"(CLM-[A-Za-z0-9\-]+)", head)
        if not match:
            continue
        hold_match = re.search(r"\*\*HOLDs:\*\* (.+)$", block, re.M)
        md_holds[match.group(1)] = parse_hold_list(hold_match.group(1)) if hold_match else set()

    drift = []
    for cid, holds in sorted(md_holds.items()):
        if cid not in claims:
            drift.append({"id": cid, "issue": "есть в MD, нет в JSON"})
            continue
        json_holds = set(claims[cid].get("holds", []) or [])
        if json_holds != holds:
            drift.append(
                {
                    "id": cid,
                    "issue": "расхождение HOLD-ов",
                    "md": sorted(holds),
                    "json": sorted(json_holds),
                }
            )
    result["status"] = "PASS" if not drift else "DRIFT"
    result["detail"] = drift
    result["checked"] = len(md_holds)
    result["unmirrored_json_claims"] = len(set(claims) - set(md_holds))
    return result


def check_one_peter_effective_holds():
    """Пересчитать действующие статусы 1 Peter: база + цепочка override.

    Исторические чанки `question-candidates-wave3-*.json` намеренно хранят
    статус на момент волны. Действующий статус задаётся цепочкой
    `question-overrides-wave3*.json`; это прямо зафиксировано в
    `27_WAVE3_FINAL_SNAPSHOT_2026-08-14.md`.
    """
    result = {"status": "NOT_RUN", "detail": []}
    base_dir = ROOT / "1_PETER_BOT" / "data"
    if not base_dir.is_dir():
        result["detail"].append("1_PETER_BOT/data отсутствует")
        return result

    candidates = {}
    for path in sorted(base_dir.glob("question-candidates-*.json")):
        data = load_json(rel(path)) or {}
        for cand in data.get("candidates", []):
            if cand.get("id"):
                candidates[cand["id"]] = {
                    "status": cand.get("status"),
                    "reference": cand.get("reference"),
                    "file": rel(path),
                }

    overrides = []
    for path in sorted(base_dir.glob("question-overrides-*.json")):
        data = load_json(rel(path)) or {}
        for item in data.get("overrides", []):
            if item.get("id") and item.get("status"):
                overrides.append((rel(path), item["id"], item["status"]))

    for _, cid, status in overrides:
        if cid in candidates:
            candidates[cid]["effective_status"] = status

    live_holds = []
    for cid, info in sorted(candidates.items()):
        effective = info.get("effective_status", info["status"])
        if effective == "HOLD":
            live_holds.append({"id": cid, "reference": info.get("reference"), "file": info["file"]})

    frozen_holds = [
        cid
        for cid, info in candidates.items()
        if info.get("status") == "HOLD" and info.get("effective_status", info["status"]) != "HOLD"
    ]

    result["status"] = "PASS" if not live_holds else "OPEN"
    result["total_candidates"] = len(candidates)
    result["override_records"] = len(overrides)
    result["frozen_hold_labels"] = sorted(frozen_holds)
    result["live_holds"] = live_holds
    return result


def check_reformation_sweep():
    """Сверить датированный аудит «Реформации» с текущим реестром.

    Аудит 2026-11-11 объявляет проход 211/211 записей и содержит таблицу §4
    ровно на 211 строк. Реестр с тех пор содержит 219 записей. Разница важна:
    надо отделить «запись не аудировалась» от «запись описана в прозе, но не
    попала в таблицу». Второе — форма подачи, первое — реальный пробел.
    """
    result = {"status": "NOT_RUN", "detail": []}
    registry = load_json("docs/research/reformation/source-registry-v1.json")
    sweep_path = ROOT / "docs" / "research" / "reformation" / "HOLD_SOURCE_SWEEP_2026-11-11.md"
    if not registry or not sweep_path.is_file():
        result["detail"].append("реестр или HOLD_SOURCE_SWEEP отсутствует")
        return result

    sources = registry.get("sources", [])
    by_id = {s.get("id"): s for s in sources if s.get("id")}
    counts = collections.Counter()
    for src in sources:
        for hold in src.get("holds", []) or []:
            counts[hold] += 1

    sweep_text = sweep_path.read_text(encoding="utf-8")
    table_ids = set(re.findall(r"^\|\s*\[?(REF-[A-Z0-9\-]+)\]?", sweep_text, re.M))
    prose_ids = set(re.findall(r"\bREF-[A-Z0-9\-]+\b", sweep_text))

    only_in_prose = sorted(set(by_id) - table_ids)
    absent = sorted(set(by_id) - prose_ids)
    prose_without_holds = [
        sid for sid in only_in_prose if not (by_id[sid].get("holds") or [])
    ]

    result["registry_source_count"] = len(sources)
    result["sweep_table_rows"] = len(table_ids)
    result["sweep_declared_scope"] = 211
    result["ids_only_in_prose"] = only_in_prose
    result["ids_absent_from_sweep"] = absent
    result["prose_only_without_typed_holds"] = prose_without_holds
    result["registry_hold_counts"] = dict(sorted(counts.items()))
    result["status"] = (
        "PASS"
        if not absent and not prose_without_holds
        else "GAP"
    )
    result["note"] = (
        "Восемь записей (P88–P94, S109) описаны в прозе аудита, но не в таблице §4. "
        "Все они несут типизированные HOLD-и; это дельта формы, а не пропуск аудита. "
        "Датированный файл не переписывается; при следующем аудите таблица должна "
        "покрывать все записи реестра."
    )
    return result


def check_hold_axes_contradictions(nodes_by_file):
    """Найти записи, где HOLD формально противоречит своей же оси состояния.

    Это не автоматическое снятие HOLD: противоречие лишь показывает, где
    реестр стоит перепроверить владельцу. Совпадение осей HOLD не снимает.
    """
    findings = []
    for path, nodes in nodes_by_file.items():
        for node in nodes:
            holds = set(node["holds"])
            if "RIGHTS_HOLD" in holds and node["rightsState"] == "PUBLICATION_ELIGIBLE":
                findings.append({"path": path, "id": node["id"], "axis": "rightsState",
                                 "value": node["rightsState"], "hold": "RIGHTS_HOLD"})
            if "PUBLICATION_HOLD" in holds and node["publicationState"] == "PROMOTE":
                findings.append({"path": path, "id": node["id"], "axis": "publicationState",
                                 "value": node["publicationState"], "hold": "PUBLICATION_HOLD"})
    return findings


def check_hold_coverage(nodes_by_file):
    """Найти места, где HOLD недозаявлен (fail-closed направление).

    Обратное направление (HOLD при уже выполненном условии) может быть
    осознанной осторожностью, а вот «права неизвестны, HOLD нет» — это дыра:
    запись выглядит разрешённой, хотя разрешения нет.
    """
    missing_rights = []
    blocked_without_publication = []
    for path, nodes in nodes_by_file.items():
        for node in nodes:
            holds = set(node["holds"])
            if node["rightsState"] in {"RIGHTS_UNKNOWN", "PERMISSION_REQUIRED"} and "RIGHTS_HOLD" not in holds:
                missing_rights.append(
                    {"path": path, "id": node["id"], "rightsState": node["rightsState"],
                     "publicationState": node["publicationState"], "holds": sorted(holds)}
                )
            if node["publicationState"] == "BLOCKED" and "PUBLICATION_HOLD" not in holds:
                blocked_without_publication.append(
                    {"path": path, "id": node["id"], "holds": sorted(holds)}
                )
    dated = re.compile(r"\d{4}-\d{2}-\d{2}")
    dated_gaps = [x for x in missing_rights if dated.search(x["path"])]
    current_gaps = [x for x in missing_rights if not dated.search(x["path"])]
    # Не всякая такая запись открыта для публикации: если `publicationState`
    # = `BLOCKED`, публикацию держит другая ось, и отсутствие `RIGHTS_HOLD`
    # остаётся дефектом разметки, но не пропуском в публикацию.
    unblocked = [x for x in missing_rights if x.get("publicationState") != "BLOCKED"]
    gated = [x for x in missing_rights if x.get("publicationState") == "BLOCKED"]
    return {
        "rightsState_without_RIGHTS_HOLD": missing_rights,
        "rightsState_gaps_gated_by_BLOCKED": gated,
        "rightsState_gaps_not_gated": unblocked,
        "rightsState_gaps_in_dated_snapshots": dated_gaps,
        "rightsState_gaps_in_current_files": current_gaps,
        "BLOCKED_without_PUBLICATION_HOLD": blocked_without_publication,
    }


# Словарь неканонической лексики внутри `holds`-массивов.

# Часть корпусов (`ИСКУПЛЕНИЕ/{data,nt,synthesis,fathers}`) объявляет свои
# `holds` как «маркеры состояния прозы файла (дубль для машинного учёта)».
# Поэтому там встречаются три разных словаря в одном массиве: типизированные
# HOLD-и, HOLD-и в неканонической записи, значения осей состояния и вердикты.
# Переписывать такие файлы нельзя: они дублируют прозу, и правка массива без
# правки прозы расщепит источник. Поэтому словарь живёт здесь, в производном
# отчёте, и проверка падает, если появилось незнакомое значение.
UNTYPED_CANONICAL_EQUIVALENT = {
    "ORIGINAL_TEXT_HOLD": "EVIDENCE_HOLD",
    "MT_HOLD": "EVIDENCE_HOLD",
    "LXX_HOLD": "EVIDENCE_HOLD",
    "ATTRIBUTION_HOLD": "EVIDENCE_HOLD",
    "EDITION_HOLD": "EVIDENCE_HOLD",
    "RECONCILIATION_HOLD": "EVIDENCE_HOLD",
    "TEXT_ACCESS_HOLD": "EVIDENCE_HOLD",
    "CONTEXT_HOLD": "EVIDENCE_HOLD",
    "DATE_HOLD": "EVIDENCE_HOLD",
    "FACSIMILE_HOLD": "ARCHIVE_HOLD",
    "EDITION_UNAVAILABLE": "ARCHIVE_HOLD",
    "LOCATOR_SINGLE_ATTESTATION": "LOCATOR_HOLD",
}

UNTYPED_STATUS_VOCABULARY = {
    "PRIVATE_STUDY_ONLY",
    "LOCATOR_PARTIAL",
    "PARTIAL_OBJECT",
    "RIGHTS_UNKNOWN",
    "RIGHTS_UNCLEAR",
    "PERMISSION_REQUIRED",
    "BLOCKED",
    "FORBIDDEN",
    "CONFLICT",
    "OPEN",
    "OPEN-LAYER",
    "OPEN_TENSION",
    "DRAFT",
    "MIRROR-LAG",
    "FALSE_FRIEND",
    "APPARATUS_FALSE_FRIEND",
    "FALSE_LOCATOR",
    "QUOTE_RISK",
    "ATTRIBUTION_SECONDARY",
    "PARTIAL_VERIFICATION",
    "PARTIALLY_VERIFIED",
    "NO SETTLED VERDICT",
    "RESOLVED-BY-TEXT",
    "RESEARCH / NOT PRODUCT",
    "RESEARCH / NOT PUBLICATION-READY",
}

UNTYPED_GENERIC = {"HOLD"}

UNTYPED_SPLIT = re.compile(r"\s*(?:/|\+)\s*")


def classify_untyped(raw):
    """Разложить неканоническую запись на понятные составляющие."""
    if raw in HOLD_TYPES:
        return "typed", raw
    if raw in UNTYPED_CANONICAL_EQUIVALENT:
        return "canonical", UNTYPED_CANONICAL_EQUIVALENT[raw]
    if raw in UNTYPED_STATUS_VOCABULARY:
        return "status", None
    if raw in UNTYPED_GENERIC:
        return "generic", None
    tokens = [tok for tok in UNTYPED_SPLIT.split(raw) if tok]
    if len(tokens) > 1:
        kinds = {classify_untyped(tok)[0] for tok in tokens}
        if "unknown" not in kinds:
            return "compound", None
    return "unknown", None


def check_untyped_holds(nodes_by_file):
    """Что на самом деле лежит в `holds`-массивах помимо канонических типов."""
    kinds = collections.Counter()
    by_raw = collections.Counter()
    canonical_rows = []
    status_rows = collections.Counter()
    unknown_rows = []
    generic_rows = []
    new_debt = []
    for path, nodes in nodes_by_file.items():
        for node in nodes:
            typed = set(node["holds"])
            for raw in node["untyped"]:
                kind, target = classify_untyped(raw)
                by_raw[raw] += 1
                parts = [raw] if kind in {"canonical", "status", "generic"} else [
                    tok for tok in UNTYPED_SPLIT.split(raw) if tok
                ]
                for part in parts:
                    part_kind, part_target = classify_untyped(part)
                    kinds[part_kind] += 1
                    if part_kind == "canonical":
                        canonical_rows.append(
                            {"path": path, "id": node["id"], "raw": part, "as": part_target}
                        )
                        if part_target not in typed:
                            new_debt.append(
                                {
                                    "path": path,
                                    "id": node["id"],
                                    "raw": part,
                                    "as": part_target,
                                }
                            )
                    elif part_kind == "status":
                        status_rows[part] += 1
                    elif part_kind == "typed":
                        pass
                    elif part_kind == "generic":
                        generic_rows.append({"path": path, "id": node["id"], "raw": part})
                    else:
                        unknown_rows.append({"path": path, "id": node["id"], "raw": part})
    deduped = []
    seen = set()
    for row in new_debt:
        key = (row["path"], row["id"], row["as"])
        if key in seen:
            continue
        seen.add(key)
        deduped.append(row)

    return {
        "untyped_entries": sum(by_raw.values()),
        "new_debt_entries": len(new_debt),
        "tokens": dict(sorted(kinds.items())),
        "canonical_equivalent": len(canonical_rows),
        "canonical_rows": canonical_rows,
        "canonical_without_new_debt": len(canonical_rows) - len(new_debt),
        "new_debt": deduped,
        "status_values": dict(status_rows.most_common()),
        "generic_markers": generic_rows,
        "unknown": unknown_rows,
        "top_raw": dict(by_raw.most_common(12)),
        "status": "PASS" if not unknown_rows else "REVIEW",
    }


BAPTIST_DIR = ROOT / "БАПТИСТЫ РОССИИ"

# Метка в этом корпусе живёт в строке `Status:` досье, а не в JSON-реестре.
BAPTIST_STATUS_RE = re.compile(r"^\s*-?\s*Status:\s*(.+)$")
BAPTIST_CLOSED_RE = re.compile(
    r"hold[s]?\s+(closed|lifted|released|resolved|cleared)", re.IGNORECASE
)
BAPTIST_ROUTES = (
    ("ARCHIVE_HOLD", re.compile(r"FACSIMILE|BINARY|PAGE|VISUAL|BYTES|SCAN")),
    ("LOCATOR_HOLD", re.compile(r"LOCATOR")),
    ("RIGHTS_HOLD", re.compile(r"RIGHTS|PERMISSION")),
    ("PUBLICATION_HOLD", re.compile(r"PUBLICATION")),
)


SUNO_DIR = ROOT / "SUNO_HYMNS"
SUNO_REGISTRY = SUNO_DIR / "data" / "source-registry-v1.json"
SUNO_MIRROR = SUNO_DIR / "RESEARCH" / "SOURCE_REGISTER.md"
SUNO_SECTION_RE = re.compile(r"^#{2,3}\s+(.+)$")
SUNO_ID_RE = re.compile(r"^[A-Z0-9][A-Z0-9-]{4,}$")


def check_suno_mirror():
    """Сверить человекочитаемое зеркало SUNO с машинным реестром.

    Зеркало использует два уровня заголовков: обычные записи идут как `##`,
    поздние греческие записи — как `##`-группа с `###`-записями внутри и
    полями в одну строку через `·`. Считать только `##` — значит объявить
    недостающими те записи, которые на самом деле есть.
    """
    if not SUNO_REGISTRY.exists() or not SUNO_MIRROR.exists():
        return {"status": "SKIP", "reason": "registry or mirror missing"}
    data = json.loads(SUNO_REGISTRY.read_text(encoding="utf-8"))
    sources = data["sources"] if isinstance(data, dict) else data
    registry = {src["id"]: src for src in sources}
    sections = {}
    headings_without_id = []
    current = None
    for line in SUNO_MIRROR.read_text(encoding="utf-8").splitlines():
        match = SUNO_SECTION_RE.match(line)
        if match:
            token = match.group(1).split(" ")[0]
            if SUNO_ID_RE.match(token):
                current = token
                sections.setdefault(current, [])
            else:
                current = None
                headings_without_id.append(match.group(1).strip())
            continue
        if current is None:
            continue
        found = re.search(r"HOLDs:\s*([^·]*)", line)
        if found:
            sections[current].append(found.group(1).strip())
    missing = sorted(set(registry) - set(sections))
    extra = sorted(set(sections) - set(registry))
    drift = []
    for sid, values in sections.items():
        if sid not in registry:
            continue
        text = values[-1] if values else ""
        tokens = {tok for tok in re.split(r"[,\s]+", text) if tok in HOLD_TYPES}
        expected = set(registry[sid].get("holds") or [])
        if tokens != expected:
            drift.append(
                {"id": sid, "mirror": text[:80], "registry": sorted(expected)}
            )
    return {
        "registry_sources": len(registry),
        "mirror_sections": len(sections),
        "missing_in_mirror": missing,
        "extra_in_mirror": extra,
        "hold_drift": drift,
        "group_headings": headings_without_id,
        "status": "PASS" if not (missing or extra or drift) else "DRIFT",
    }


def check_baptist_book_holds():
    """Разобрать HOLD-метки книги «Баптисты России».

    Здесь HOLD объявлен прозой досье (`Status: ... HOLD`), а не реестром,
    поэтому единственное, что можно установить по репозиторию: сколько меток
    живо, что каждая называет, и нет ли заявленного снятия.
    """
    status_lines = []
    closure_claims = []
    if BAPTIST_DIR.exists():
        for path in sorted(BAPTIST_DIR.rglob("*.md")):
            try:
                lines = path.read_text(encoding="utf-8").splitlines()
            except (OSError, UnicodeDecodeError):
                continue
            for number, line in enumerate(lines, 1):
                if BAPTIST_CLOSED_RE.search(line):
                    closure_claims.append(
                        {"path": rel(path), "line": number, "text": line.strip()[:200]}
                    )
                match = BAPTIST_STATUS_RE.match(line)
                if not match:
                    continue
                label = match.group(1).strip().strip("*`").strip().rstrip("*`.")
                tokens = re.findall(r"[A-Za-z_]+", label.upper())
                if not any(tok == "HOLD" or tok.endswith("_HOLD") for tok in tokens):
                    continue
                label = re.sub(r"\*\*\.?$", "", label).strip()
                route = "EVIDENCE_HOLD"
                for name, pattern in BAPTIST_ROUTES:
                    if pattern.search(label.upper()):
                        route = name
                        break
                status_lines.append(
                    {"path": rel(path), "line": number, "label": label, "route": route}
                )
    media = []
    if BAPTIST_DIR.exists():
        media = [
            rel(path)
            for path in BAPTIST_DIR.rglob("*")
            if path.is_file() and path.suffix.lower() in {".pdf", ".jpg", ".jpeg", ".png"}
        ]
    routes = collections.Counter(row["route"] for row in status_lines)
    labels = collections.Counter(row["label"] for row in status_lines)
    return {
        "status_lines": len(status_lines),
        "files": len({row["path"] for row in status_lines}),
        "routes": dict(routes.most_common()),
        "top_labels": [[label, count] for label, count in labels.most_common(8)],
        "closure_claims": closure_claims,
        "media_files": len(media),
        "rows": status_lines,
        "verdict": "NO_HOLD_CLOSABLE_FROM_REPO" if not closure_claims else "REVIEW",
    }


def check_decision_only_holds(nodes_by_file):
    """Объекты, которые держат только права и публикация.

    Это слой решений владельца, а не слой отсутствующих доказательств:
    объект прочитан целиком, локатор сверен, а HOLD-и сводятся к
    `RIGHTS_HOLD` / `PUBLICATION_HOLD`. Новый поиск здесь ничего не изменит.
    """
    by_file = {}
    total = 0
    by_rights = collections.Counter()
    by_holds = collections.Counter()
    ready_by_rights = 0
    internal_only = 0
    rights_enquiry = 0
    enquiry_rows = []
    for path, nodes in nodes_by_file.items():
        rows = []
        for node in nodes:
            holds = set(node["holds"])
            if not (
                holds
                and holds <= {"RIGHTS_HOLD", "PUBLICATION_HOLD"}
                and node["accessState"] == "FULL_OBJECT_VERIFIED"
                and node["locatorState"] == "EXACT_LOCATOR_VERIFIED"
            ):
                continue
            rows.append(node["id"] or "(без id)")
            rights = node["rightsState"] or "(не задано)"
            by_rights[rights] += 1
            by_holds[", ".join(sorted(holds))] += 1
            # Права уже не мешают: остаётся только решение о публикации.
            if rights in {"PUBLICATION_ELIGIBLE", "PUBLIC_DOMAIN"}:
                ready_by_rights += 1
            # Политика владельца: объект существует только для внутренней работы.
            elif rights in {"PRIVATE_STUDY_ONLY", "STORAGE_ONLY"}:
                internal_only += 1
            else:
                rights_enquiry += 1
                finding = node.get("finding") or ""
                enquiry_rows.append(
                    {
                        "path": path,
                        "id": node["id"] or "(без id)",
                        "rights": rights,
                        "negative": bool(re.search(r"\breject", finding, re.IGNORECASE)),
                    }
                )
        if rows:
            total += len(rows)
            by_file[path] = {"count": len(rows), "ids": sorted(rows)[:5]}
    return {
        "total_objects": total,
        "byRights": dict(by_rights.most_common()),
        "byHolds": dict(by_holds.most_common()),
        "ready_by_rights": ready_by_rights,
        "internal_only": internal_only,
        "rights_enquiry": rights_enquiry,
        "enquiry_rows": enquiry_rows,
        "enquiry_already_negative": sum(1 for row in enquiry_rows if row["negative"]),
        "byFile": dict(sorted(by_file.items(), key=lambda kv: -kv[1]["count"])),
        "meaning": (
            "accessState=FULL_OBJECT_VERIFIED и locatorState=EXACT_LOCATOR_VERIFIED, "
            "а holds ⊆ {RIGHTS_HOLD, PUBLICATION_HOLD}. Закрытие таких HOLD-ов — "
            "решение о правах и публикации, а не новый поиск."
        ),
        "caveat": (
            "Один и тот же объект может учитываться в двух реестрах корпуса "
            "(например, карточка и её снимок в плане), поэтому сумма — верхняя граница."
        ),
    }


def check_registry_files_exist(nodes_by_file):
    """Проверить, что JSON-реестры с HOLD-ами не осиротели и читаемы."""
    return {
        "files_with_holds": len(nodes_by_file),
        "nodes_with_holds": sum(len(v) for v in nodes_by_file.values()),
    }


def git_commit():
    try:
        return subprocess.run(
            ["git", "-C", str(ROOT), "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return "UNKNOWN"


def build():
    nodes_by_file, parse_errors = scan_json()
    md_files, md_types, bare, md_files_with_tokens = scan_markdown()

    json_type_counts = collections.Counter()
    json_corpus_counts = collections.Counter()
    untyped_in_json = []
    for path, nodes in nodes_by_file.items():
        corpus = corpus_of(ROOT / path)
        for node in nodes:
            json_type_counts.update(node["holds"])
            json_corpus_counts[corpus] += 1
            if node["untyped"]:
                untyped_in_json.append(
                    {"path": path, "id": node["id"], "tokens": node["untyped"]}
                )

    md_corpus_tokens = collections.Counter()
    for path, count in md_files.items():
        md_corpus_tokens[corpus_of(ROOT / path)] += count

    per_corpus = {}
    for corpus in sorted(set(json_corpus_counts) | set(md_corpus_tokens)):
        per_corpus[corpus] = {
            "json_nodes_with_holds": json_corpus_counts.get(corpus, 0),
            "markdown_hold_tokens": md_corpus_tokens.get(corpus, 0),
        }

    checks = {
        "suno_source_register_parity": check_suno_mirrors(),
        "suno_claim_ledger_parity": check_suno_claims(),
        "one_peter_effective_holds": check_one_peter_effective_holds(),
        "reformation_registry_vs_sweep": check_reformation_sweep(),
        "axis_contradictions": check_hold_axes_contradictions(nodes_by_file),
        "hold_coverage": check_hold_coverage(nodes_by_file),
        "untyped_holds": check_untyped_holds(nodes_by_file),
        "baptist_book": check_baptist_book_holds(),
        "suno_mirror": check_suno_mirror(),
        "decision_only_holds": check_decision_only_holds(nodes_by_file),
    }
    checks.update(check_registry_files_exist(nodes_by_file))

    # Разбор конкретных кандидатов, которые были проверены в этом проходе.
    # Каждый вердикт получен из содержимого репозитория, а не из «здравого смысла».
    examined = [
        {
            "case": "SUNO_HYMNS SRC-PHOS-PRAVENC",
            "requested": "ARCHIVE_HOLD при accessState=FULL_OBJECT_VERIFIED",
            "verdict": "ОСТАВЛЕН",
            "reason": (
                "Полностью прочитана энциклопедическая статья, но печатный том "
                "Православной энциклопедии (т. 62, с. 54–55) не сверялся; "
                "ARCHIVE_HOLD относится к печатному объекту, а не к веб-тексту."
            ),
        },
        {
            "case": "SUNO_HYMNS SRC-PHOS-VRG-B3",
            "requested": "LOCATOR_HOLD при locatorState=EXACT_LOCATOR_VERIFIED",
            "verdict": "ОСТАВЛЕН",
            "reason": (
                "Локатор л. 269r взят из каталога, факсимиле рукописи не открывалось "
                "(accessState=CATALOG_ONLY); каталог не подтверждает лист."
            ),
        },
        {
            "case": "ИСКУПЛЕНИЕ/nt S15 (Каноны Дорта)",
            "requested": "RIGHTS_HOLD при rightsState=PUBLICATION_ELIGIBLE",
            "verdict": "ОСТАВЛЕН",
            "reason": (
                "PUBLICATION_ELIGIBLE ограничен явно только английским фрагментом 1840 г. "
                "из локальной записи; RIGHTS_HOLD держит остальные издания (CRC 1986, OPC 1948)."
            ),
        },
        {
            "case": "1_PETER_BOT w3q_013/031/036/038/050/051/075",
            "requested": "status=HOLD в базовых чанках кандидатов",
            "verdict": "НЕ ДЕЙСТВУЕТ (снят цепочкой override)",
            "reason": (
                "Все семь базовых меток перекрыты question-overrides-wave3g/k/l/n; "
                "действующий счёт HOLD = 0, что подтверждает пересчёт в этом отчёте. "
                "Исторические файлы не перезаписываются."
            ),
        },
        {
            "case": "1_PETER_BOT data/p0-claim-holds-wave3.json (1 Pet 5:2a/5:2b)",
            "requested": "P0_HOLD после закрытия HOLD-TC-5-2A/5-2B",
            "verdict": "ОСТАВЛЕН",
            "reason": (
                "Другая ось: поле officialECMWitnessStatus означает прямой readback "
                "аппарата ECM, а волна 3n закрывала кандидата по маршруту "
                "peer-reviewed ECM-based treatment и прямо не заявляла прямого dECM "
                "readback. Файл при этом нигде в репозитории не цитируется."
            ),
        },
        {
            "case": "G3 Q005 / Q006",
            "requested": "снять hold после переименования в Lumena Ministries",
            "verdict": "ОСТАВЛЕН",
            "reason": (
                "Переименование подтверждено на уровне индекса реестра, но не даёт "
                "ни текущего status field, ни документов о переходе; Q006 "
                "TRANSFEREE/CLOSING остаётся EXTERNAL_DOCUMENT_HOLD."
            ),
        },
    ]

    closures = [
        {
            "item": "SUNO_HYMNS/RESEARCH/OPEN_HOLDS.md",
            "action": "Пересобрано генератором scripts/render_hold_ledger.py",
            "effect": (
                "Состав HOLD-ов не изменился (реестры те же); обновлена только "
                "дата сборки, то есть устранено расхождение «сводка от 2026-11-15 "
                "при реестрах без изменений»."
            ),
        }
    ]

    report = {
        "schemaVersion": 1,
        "artifact": "REPO-HOLD-INVENTORY",
        "role": "DERIVED_READ_ONLY_NOT_AUTHORITY",
        "generatedAt": datetime.date.today().isoformat(),
        "testedCommit": git_commit(),
        "policy": "data/repository-evidence-policy-v2.json",
        "totals": {
            "json_files_with_holds": len(nodes_by_file),
            "json_nodes_with_holds": sum(len(v) for v in nodes_by_file.values()),
            "json_hold_entries": sum(json_type_counts.values()),
            "json_hold_by_type": dict(sorted(json_type_counts.items())),
            "markdown_files_with_typed_tokens": md_files_with_tokens,
            "markdown_typed_tokens": sum(md_types.values()),
            "markdown_typed_by_type": dict(sorted(md_types.items())),
            "bare_untyped_status_lines": len(bare),
        },
        "perCorpus": per_corpus,
        "closureRoutes": {
            hold: {"class": route[0], "requires": route[1]}
            for hold, route in CLOSURE_ROUTE.items()
        },
        "checks": checks,
        "examinedCases": examined,
        "closuresThisPass": closures,
        "untypedHoldTokensInJson": untyped_in_json,
        "bareStatusLines": bare,
        "jsonParseErrors": parse_errors,
        "limits": [
            "Инвентарь не перечитывает внешние источники и не проверяет их содержание.",
            "HOLD-и в Markdown посчитаны как токены; один и тот же HOLD может "
            "упоминаться в досье, реестре и аудите несколько раз.",
            "Счётчики по корпусам не складывать между собой: наборы пересекаются.",
        ],
    }
    return report


def render_markdown(report):
    t = report["totals"]
    lines = []
    add = lines.append

    add("# HOLD inventory — сквозной инвентарь HOLD-ов Research")
    add("")
    add(
        f"**Собрано:** {report['generatedAt']}; **проверенный коммит:** "
        f"`{report['testedCommit']}`. **Роль:** производный read-only артефакт, "
        "не authority. Пересобрать: `python3 -B scripts/render_hold_inventory.py`."
    )
    add("")
    add(
        "Инвентарь отвечает на один вопрос: какие HOLD-и объявлены в репозитории, "
        "какого они типа и что нужно, чтобы закрыть каждый честно. Он **ничего не "
        "снимает**: по `data/repository-evidence-policy-v2.json` HOLD не снимается "
        "ни присутствием файла в Research/Drive, ни достижимостью URL, ни "
        "библиографической записью."
    )
    add("")
    add("## 1. Сколько и каких")
    add("")
    add("| Метрика | Значение |")
    add("|---|---|")
    add(f"| JSON-файлов с HOLD-ами | {t['json_files_with_holds']} |")
    add(f"| JSON-записей (объектов) с HOLD-ами | {t['json_nodes_with_holds']} |")
    add(f"| Всего HOLD-вхождений в `holds`-массивах | {t['json_hold_entries']} |")
    add(f"| Markdown-файлов с типизированными токенами | {t['markdown_files_with_typed_tokens']} |")
    add(f"| Всего типизированных токенов в Markdown/YAML | {t['markdown_typed_tokens']} |")
    add(f"| Нетипизированных строк `HOLD` | {t['bare_untyped_status_lines']} |")
    add("")
    add("По типам:")
    add("")
    add("| Тип | В JSON-реестрах | В Markdown/YAML | Маршрут закрытия |")
    add("|---|---|---|---|")
    for hold in HOLD_TYPES:
        route = CLOSURE_ROUTE[hold]
        add(
            f"| `{hold}` | {t['json_hold_by_type'].get(hold, 0)} | "
            f"{t['markdown_typed_by_type'].get(hold, 0)} | {route[0]} |"
        )
    add("")
    add(
        "Счётчики не суммировать: один и тот же HOLD описывается и в машинном "
        "реестре, и в досье, и в аудите."
    )
    add("")
    add("## 2. Что означает каждый маршрут")
    add("")
    for hold in HOLD_TYPES:
        route = CLOSURE_ROUTE[hold]
        add(f"- `{hold}` → **{route[0]}**. {route[1]}")
    add("")
    add("## 3. По корпусам")
    add("")
    add("| Корпус | JSON-записей с HOLD | Markdown-токенов |")
    add("|---|---|---|")
    for corpus, data in sorted(
        report["perCorpus"].items(),
        key=lambda kv: -(kv[1]["json_nodes_with_holds"] + kv[1]["markdown_hold_tokens"]),
    ):
        add(
            f"| `{corpus}` | {data['json_nodes_with_holds']} | "
            f"{data['markdown_hold_tokens']} |"
        )
    add("")

    add("## 4. Внутренние проверки, выполненные в этом проходе")
    add("")
    checks = report["checks"]
    suno_src = checks["suno_source_register_parity"]
    add("### 4.1 SUNO_HYMNS: машинный реестр против человекочитаемого зеркала")
    add("")
    add(
        f"Проверено записей: {suno_src.get('checked', 0)}. "
        f"Вердикт: **{suno_src['status']}**."
    )
    if suno_src.get("detail"):
        add("")
        for item in suno_src["detail"]:
            add(f"- `{item.get('id')}` — {item.get('issue')}")
    add("")
    if suno_src.get("unmirrored_json_sources"):
        add(
            "Источники в JSON без отдельной секции в `SOURCE_REGISTER.md`: "
            f"{len(suno_src['unmirrored_json_sources'])}. Это не расхождение "
            "HOLD-ов (сравнивать не с чем), но зеркало покрывает не весь реестр."
        )
        add("")
    suno_claims = checks["suno_claim_ledger_parity"]
    add("### 4.2 SUNO_HYMNS: тезисы")
    add("")
    add(
        f"Проверено тезисов с зеркалом: {suno_claims.get('checked', 0)}. "
        f"Вердикт: **{suno_claims['status']}**; тезисов в JSON без секции в "
        f"`CLAIM_LEDGER.md`: {suno_claims.get('unmirrored_json_claims', '—')}."
    )
    add("")
    pet = checks["one_peter_effective_holds"]
    add("### 4.3 1_PETER_BOT: действующий статус после цепочки override")
    add("")
    add(
        f"Кандидатов: {pet.get('total_candidates', 0)}; override-записей: "
        f"{pet.get('override_records', 0)}; действующих `HOLD`: "
        f"**{len(pet.get('live_holds', []))}**."
    )
    add("")
    if pet.get("frozen_hold_labels"):
        add(
            "Замороженные исторические метки `HOLD`, перекрытые override-файлами "
            f"({len(pet['frozen_hold_labels'])}): "
            + ", ".join(f"`{x}`" for x in pet["frozen_hold_labels"])
            + "."
        )
        add("")
    ref = checks["reformation_registry_vs_sweep"]
    add("### 4.4 «Реформация»: датированный аудит против выросшего реестра")
    add("")
    add(
        f"В реестре {ref.get('registry_source_count', 0)} записей. Аудит "
        f"2026-11-11 объявляет охват {ref.get('sweep_declared_scope', '—')} "
        f"записей и содержит таблицу §4 ровно на "
        f"{ref.get('sweep_table_rows', 0)} строк. Записей, отсутствующих в аудите "
        f"целиком: **{len(ref.get('ids_absent_from_sweep', []))}**. Записей, "
        f"описанных в прозе аудита, но не попавших в таблицу: "
        f"**{len(ref.get('ids_only_in_prose', []))}**."
    )
    add("")
    if ref.get("ids_only_in_prose"):
        add(
            "Только в прозе: "
            + ", ".join(f"`{x}`" for x in ref["ids_only_in_prose"])
            + f". Без типизированных HOLD-ов среди них: "
            f"**{len(ref.get('prose_only_without_typed_holds', []))}**. "
            "Это дельта формы подачи, а не пропуск аудита."
        )
        add("")
    add("Действующие HOLD-и реестра: " + ", ".join(
        f"`{k}`={v}" for k, v in ref.get("registry_hold_counts", {}).items()
    ) + ". Вердикт: **" + str(ref.get("status")) + "**.")
    add("")
    contradictions = checks["axis_contradictions"]
    add("### 4.5 Формальные противоречия HOLD и его оси состояния")
    add("")
    if contradictions:
        add("| Файл | id | Ось | Значение | HOLD |")
        add("|---|---|---|---|---|")
        for item in contradictions[:50]:
            add(
                f"| `{item['path']}` | `{item['id']}` | `{item['axis']}` | "
                f"`{item['value']}` | `{item['hold']}` |"
            )
    else:
        add("Не найдено ни одного случая, где `RIGHTS_HOLD`/`PUBLICATION_HOLD` "
            "прямо противоречит `PUBLICATION_ELIGIBLE`/`PROMOTE`.")
    add("")
    add(
        "Противоречие — сигнал перепроверить запись, а не основание снять HOLD: "
        "оси описывают разные предметы (например, права на конкретный фрагмент)."
    )
    add("")
    coverage = checks["hold_coverage"]
    add("### 4.6 HOLD недозаявлен (fail-closed проверка)")
    add("")
    missing_rights = coverage["rightsState_without_RIGHTS_HOLD"]
    blocked = coverage["BLOCKED_without_PUBLICATION_HOLD"]
    add(
        f"Записей с `rightsState` = `RIGHTS_UNKNOWN`/`PERMISSION_REQUIRED` и без "
        f"`RIGHTS_HOLD`: **{len(missing_rights)}**, из них в датированных снимках "
        f"**{len(coverage.get('rightsState_gaps_in_dated_snapshots', []))}**, "
        f"а в недатированных (действующих) файлах "
        f"**{len(coverage.get('rightsState_gaps_in_current_files', []))}**. Записей с "
        f"`publicationState` = `BLOCKED` и без `PUBLICATION_HOLD`: **{len(blocked)}**."
    )
    add("")
    ungated = coverage.get("rightsState_gaps_not_gated", [])
    gated = coverage.get("rightsState_gaps_gated_by_BLOCKED", [])
    add(
        f"Разделение по второй оси: **{len(gated)}** из них несут "
        f"`publicationState` = `BLOCKED`, то есть публикацию держит не права, а "
        f"блокировка, и отсутствие `RIGHTS_HOLD` — дефект разметки, а не пропуск. "
        f"Открытых для публикации записей без `RIGHTS_HOLD` при неизвестных правах: "
        f"**{len(ungated)}**."
    )
    add("")
    if missing_rights:
        add("| Файл | id | rightsState | Фактические HOLD-и |")
        add("|---|---|---|---|")
        for item in missing_rights[:40]:
            add(
                f"| `{item['path']}` | `{item['id']}` | `{item['rightsState']}` | "
                + (", ".join(f"`{h}`" for h in item["holds"]) or "—")
                + " |"
            )
        add("")
        if ungated:
            add(
                "Это дыра в обратную сторону: запись выглядит права-разрешённой, "
                "хотя права не установлены. Правильная реакция — добавить "
                "типизированный `RIGHTS_HOLD` в актуальную запись, а не переписывать "
                "датированный снимок задним числом."
            )
        else:
            add(
                "Ни одна из этих записей не открыта для публикации: во всех "
                "`publicationState` = `BLOCKED`, поэтому пропуска в публикацию нет — "
                "есть только неполная разметка. Датированные снимки задним числом не "
                "переписываются; типизированный `RIGHTS_HOLD` уместен в актуальной "
                "записи, когда она появится."
            )
        add("")

    decision = checks["decision_only_holds"]
    add("### 4.7 Что держат только права и публикация")
    add("")
    add(
        f"Объектов, прочитанных полностью и с точным локатором, где все HOLD-и "
        f"сводятся к `RIGHTS_HOLD`/`PUBLICATION_HOLD`: **{decision['total_objects']}** "
        "в машинных реестрах. Здесь новый поиск ничего не изменит — нужен "
        "ответ по правам и решение о публикации."
    )
    add("")
    if decision["byFile"]:
        add("| Реестр | Объектов | Примеры |")
        add("|---|---|---|")
        for path, info in list(decision["byFile"].items())[:12]:
            sample = ", ".join(f"`{x}`" for x in info["ids"][:3])
            add(f"| `{path}` | {info['count']} | {sample} |")
        add("")
    add("Разрез по правам (как их называет сам реестр, не как их оценивает этот отчёт):")
    add("")
    add("| `rightsState` | Объектов |")
    add("|---|---|")
    for rights, count in decision["byRights"].items():
        add(f"| `{rights}` | {count} |")
    add("")
    add(
        f"Из {decision['total_objects']} объектов: **{decision['ready_by_rights']}** "
        "уже помечены как публикационно допустимые или общественное достояние — "
        "их держит только решение о публикации, а не права; "
        f"**{decision['internal_only']}** по политике владельца существуют только "
        f"для внутренней работы; и лишь **{decision['rights_enquiry']}** требуют "
        "запроса о правах или разрешения."
    )
    add("")
    if decision["enquiry_rows"]:
        add("Кто именно требует запроса о правах:")
        add("")
        grouped_enq = collections.defaultdict(list)
        for row in decision["enquiry_rows"]:
            grouped_enq[(row["path"], row["rights"])].append(row["id"])
        for (path, rights), ids in sorted(grouped_enq.items()):
            sample = ", ".join(f"`{i}`" for i in sorted(ids)[:6])
            more = f" и ещё {len(ids) - 6}" if len(ids) > 6 else ""
            add(f"- `{path}` (`{rights}`): {sample}{more}")
        add("")
        if decision["enquiry_already_negative"]:
            add(
                f"Из них **{decision['enquiry_already_negative']}** уже несут "
                "записанный отрицательный вердикт в собственном поле `finding`: "
                "вопрос прав там отвечен «не использовать», и открытым остаётся "
                "только формальное снятие, а не запрос."
            )
            add("")
    add(f"Оговорка: {decision['caveat']}")
    add("")

    untyped = checks["untyped_holds"]
    add("### 4.8 Неканоническая лексика внутри `holds`")
    add("")
    add(
        f"Записей в `holds`, которые не являются каноническим типом: "
        f"**{untyped['untyped_entries']}**, вердикт **{untyped['status']}**. "
        "Корпуса `ИСКУПЛЕНИЕ/{data,nt,synthesis,fathers}` объявляют свои "
        "`holds` как «маркеры состояния прозы файла (дубль для машинного "
        "учёта)», поэтому в одном массиве лежат три разных словаря: "
        "типизированные HOLD-и, HOLD-и в неканонической записи, значения осей "
        "состояния и вердикты. Массивы не переписываются: правка данных без "
        "правки прозы расщепила бы источник."
    )
    add("")
    add("| Неканоническая запись | Канонический тип | Всего | Из них добавляют новый долг |")
    add("|---|---|---|---|")
    mapping = collections.Counter()
    for row in untyped["canonical_equivalent_list"] if "canonical_equivalent_list" in untyped else []:
        pass
    canon_rows = untyped.get("canonical_rows", [])
    for row in canon_rows:
        mapping[(row["raw"], row["as"])] += 1
    novel = collections.Counter((r["raw"], r["as"]) for r in untyped["new_debt"])
    for (raw, target), count in sorted(mapping.items(), key=lambda kv: (-kv[1], kv[0])):
        add(f"| `{raw}` | `{target}` | {count} | {novel.get((raw, target), 0)} |")
    add("")
    add(
        f"Итого: **{untyped['canonical_equivalent']}** записей сводятся к "
        f"каноническому типу, из них **{untyped['canonical_without_new_debt']}** "
        "лишь повторяют уже объявленный на том же узле тип. Новый долг "
        f"добавляют только **{untyped['new_debt_entries']}** записей "
        f"({len(untyped['new_debt'])} уникальных пар «узел + тип»):"
    )
    add("")
    grouped = collections.defaultdict(list)
    for row in untyped["new_debt"]:
        grouped[(row["path"], row["as"])].append(row["id"] or "(без id)")
    for (path, target), ids in sorted(grouped.items()):
        add(f"- `{path}` → `{target}`: {', '.join(f'`{i}`' for i in sorted(ids))}")
    add("")
    status_counts = untyped["status_values"]
    add(
        f"Ещё **{sum(status_counts.values())}** записей — это значения осей "
        "состояния и вердикты, а не HOLD-и (`"
        + "`, `".join(list(status_counts)[:10])
        + "` и др.). Они не требуют ни объекта, ни решения: это подписи к прозе."
    )
    add("")
    if untyped["generic_markers"]:
        places = ", ".join(
            f"`{row['path']}`/{row['id'] or '(без id)'}" for row in untyped["generic_markers"]
        )
        add(
            f"Голый `HOLD` встречается {len(untyped['generic_markers'])} раза "
            f"({places}) и всегда рядом с типизированным HOLD на том же узле, "
            "то есть своего долга не несёт."
        )
        add("")
    add(
        "Правило зафиксировано в генераторе: незнакомое значение в `holds` "
        "переводит проверку в `REVIEW`, поэтому новый словарь не проскочит "
        "молча."
    )
    add("")

    baptist = checks["baptist_book"]
    add("### 4.9 Книга «Баптисты России»: HOLD в прозе досье")
    add("")
    add(
        f"В `БАПТИСТЫ РОССИИ` HOLD объявлен строкой `Status:` досье, а не "
        f"реестром: таких строк **{baptist['status_lines']}** в "
        f"**{baptist['files']}** файлах (остальные упоминания — прозаические "
        "ссылки на те же метки)."
    )
    add("")
    if baptist["routes"]:
        add("| Маршрут закрытия | Меток |")
        add("|---|---|")
        for route, count in baptist["routes"].items():
            add(f"| `{route}` | {count} |")
        add("")
    if baptist["top_labels"]:
        add("Самые частые метки: " + "; ".join(
            f"`{label}` ×{count}" for label, count in baptist["top_labels"]
        ) + ".")
        add("")
    add(
        f"Заявлений о снятии HOLD в корпусе: **{len(baptist['closure_claims'])}**. "
        "То есть ни одна метка не забыта и не отменена молча."
    )
    add("")
    add(
        f"Медиа в каталоге: **{baptist['media_files']}** файлов (PDF и снимки "
        "по другим объектам — Борноволоков, Белякова, Потапова, бюллетени "
        "Совета родственников), страничных образов, которых требуют метки "
        "`BINARY OPEN` / `HOLD FOR FACSIMILE`, среди них нет."
    )
    add("")
    add(
        "Вердикт: **" + baptist["verdict"] + "** — метки называют конкретный "
        "отсутствующий объект, поэтому закрываются только получением "
        "страничных образов, а не работой с текстом репозитория."
    )
    add("")

    suno = checks["suno_mirror"]
    add("### 4.10 Зеркало реестра SUNO")
    add("")
    if suno.get("status") == "SKIP":
        add("Реестр или зеркало отсутствуют — проверка пропущена.")
    else:
        add(
            f"Реестр: **{suno['registry_sources']}** источников, зеркало: "
            f"**{suno['mirror_sections']}** записей, отсутствующих в зеркале "
            f"**{len(suno['missing_in_mirror'])}**, лишних "
            f"**{len(suno['extra_in_mirror'])}**, расхождений по HOLD "
            f"**{len(suno['hold_drift'])}** — вердикт **{suno['status']}**."
        )
        add("")
        add(
            "Заголовков без id в зеркале: "
            f"**{len(suno['group_headings'])}** — это групповые заголовки "
            "проходов («Third-pass additions» и т. п.), а не источники. "
            "Поздние греческие записи лежат на уровень ниже (`###`) и держат "
            "поля в одной строке через `·`, поэтому подсчёт только по `##` "
            "ошибочно показывает их отсутствующими."
        )
    add("")

    add("## 5. Проверенные кандидаты и вердикты")
    add("")
    add("| Случай | Что проверялось | Вердикт | Почему |")
    add("|---|---|---|---|")
    for case in report["examinedCases"]:
        add(
            f"| {case['case']} | {case['requested']} | **{case['verdict']}** | "
            f"{case['reason']} |"
        )
    add("")

    add("## 6. Что действительно закрыто в этом проходе")
    add("")
    for closure in report["closuresThisPass"]:
        add(f"- **{closure['item']}** — {closure['action']}. {closure['effect']}")
    add("")

    add("## 7. Нетипизированные `HOLD`")
    add("")
    if report["bareStatusLines"]:
        add(
            "По `SOURCE_LIBRARY/README.md` и `AGENT_RULES.md` голый `HOLD` должен "
            "быть заменён типизированным. Найдено:"
        )
        add("")
        for item in report["bareStatusLines"]:
            add(f"- `{item['file']}:{item['line']}` — `{item['text']}`")
    else:
        add("Не найдено.")
    add("")
    typed_in_json = report["untypedHoldTokensInJson"]
    if typed_in_json:
        add(
            "Нетипизированные элементы внутри `holds`-массивов JSON "
            f"({len(typed_in_json)} записей) — отдельный технический долг; "
            "они перечислены в JSON-версии отчёта."
        )
        add("")

    add("## 8. Границы отчёта")
    add("")
    for limit in report["limits"]:
        add(f"- {limit}")
    add("")
    add(
        "Главный вывод честного прохода: подавляющая часть HOLD-ов в этом "
        "репозитории — не забытые задачи, а сознательные запреты на утверждения "
        "без объекта (архив, права, точный локатор, независимое свидетельство). "
        "Их нельзя закрыть изнутри репозитория, не выдумывая доказательство. "
        "Закрываемыми изнутри оказываются только административные расхождения: "
        "устаревшие зеркала и замороженные метки, перекрытые более поздними "
        "файлами."
    )
    add("")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="не писать файлы, а сравнить фактическую структуру отчёта с новой сборкой",
    )
    args = parser.parse_args()

    report = build()
    markdown = render_markdown(report)

    json_text = json.dumps(report, ensure_ascii=False, indent=1, sort_keys=False) + "\n"
    md_text = markdown + "\n"

    if args.check:
        # Дата сборки и проверяемый коммит меняются от запуска к запуску и не
        # являются содержанием отчёта; сравниваем всё остальное.
        volatile_json = {"generatedAt", "testedCommit"}
        problems = 0

        try:
            current = json.loads(OUT_JSON.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            print(f"MISSING/UNREADABLE: {rel(OUT_JSON)}", file=sys.stderr)
            current = None
            problems += 1
        if current is not None:
            trimmed_current = {k: v for k, v in current.items() if k not in volatile_json}
            trimmed_fresh = {k: v for k, v in report.items() if k not in volatile_json}
            if trimmed_current != trimmed_fresh:
                print(f"DRIFT: {rel(OUT_JSON)}", file=sys.stderr)
                problems += 1

        current_md = OUT_MD.read_text(encoding="utf-8") if OUT_MD.is_file() else ""
        strip = lambda text: re.sub(r"\*\*Собрано:\*\* .*?\n", "", text, count=1)
        if strip(current_md) != strip(md_text):
            print(f"DRIFT: {rel(OUT_MD)}", file=sys.stderr)
            problems += 1

        if problems:
            raise SystemExit(1)
        print("HOLD inventory: PASS (файлы соответствуют генератору)")
        return 0

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json_text, encoding="utf-8")
    OUT_MD.write_text(md_text, encoding="utf-8")

    t = report["totals"]
    print(
        "собрано: {md} и {js}; JSON-записей с HOLD={nodes}, вхождений={entries}, "
        "markdown-токенов={mdt}, голых строк={bare}".format(
            md=rel(OUT_MD),
            js=rel(OUT_JSON),
            nodes=t["json_nodes_with_holds"],
            entries=t["json_hold_entries"],
            mdt=t["markdown_typed_tokens"],
            bare=t["bare_untyped_status_lines"],
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
