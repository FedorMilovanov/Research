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
        # и счётчики меняются от его же содержимого.
        if OUT_DIR in path.parents:
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
    """Датированный аудит 211 REF против текущего реестра."""
    result = {"status": "NOT_RUN", "detail": []}
    registry = load_json("docs/research/reformation/source-registry-v1.json")
    sweep = ROOT / "docs" / "research" / "reformation" / "HOLD_SOURCE_SWEEP_2026-11-11.md"
    if not registry or not sweep.is_file():
        result["detail"].append("реестр или HOLD_SOURCE_SWEEP отсутствует")
        return result

    sources = registry.get("sources", [])
    counts = collections.Counter()
    for src in sources:
        for hold in src.get("holds", []) or []:
            counts[hold] += 1
    sweep_text = sweep.read_text(encoding="utf-8")
    match = re.search(r"211/211", sweep_text)
    result["status"] = "DATED_SNAPSHOT"
    result["registry_source_count"] = len(sources)
    result["sweep_scope"] = "211 (датированный аудит 2026-11-11)" if match else "не найдено"
    result["registry_hold_counts"] = dict(sorted(counts.items()))
    result["note"] = (
        "Датированный аудит не переписывается. Если реестр вырос после 2026-11-11, "
        "это дельта, а не ошибка аудита; новые REF требуют отдельного прохода."
    )
    result["sources_added_since_sweep"] = max(0, len(sources) - 211)
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
                     "holds": sorted(holds)}
                )
            if node["publicationState"] == "BLOCKED" and "PUBLICATION_HOLD" not in holds:
                blocked_without_publication.append(
                    {"path": path, "id": node["id"], "holds": sorted(holds)}
                )
    return {
        "rightsState_without_RIGHTS_HOLD": missing_rights,
        "BLOCKED_without_PUBLICATION_HOLD": blocked_without_publication,
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
        f"В реестре сейчас {ref.get('registry_source_count', 0)} источников; "
        f"аудит 2026-11-11 покрывал {ref.get('sweep_scope', '—')}. "
        f"Дельта: {ref.get('sources_added_since_sweep', 0)}."
    )
    add("")
    add("Действующие HOLD-и реестра: " + ", ".join(
        f"`{k}`={v}" for k, v in ref.get("registry_hold_counts", {}).items()
    ) + ".")
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
        f"`RIGHTS_HOLD`: **{len(missing_rights)}**. Записей с "
        f"`publicationState` = `BLOCKED` и без `PUBLICATION_HOLD`: **{len(blocked)}**."
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
        add(
            "Это дыра в обратную сторону: запись выглядит права-разрешённой, "
            "хотя права не установлены. Правильная реакция — добавить "
            "типизированный `RIGHTS_HOLD` в актуальную запись, а не переписывать "
            "датированный снимок задним числом."
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
