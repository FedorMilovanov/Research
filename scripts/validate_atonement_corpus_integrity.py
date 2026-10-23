#!/usr/bin/env python3
"""Read-only integrity gate for the ИСКУПЛЕНИЕ (atonement) corpus as it exists in main.

It does not re-state any theology. It asserts the four structural facts that were
silently violated before the 2026-10-15 audit and that nothing else in this
repository checks:

  1. the root spine of the corpus is complete, single-owned and every root file is
     registered in the corpus navigation (no unannounced second `00_*` index);
  2. the machine registry may not point at a git path that does not exist — this is
     what happened to `parallelAgents.briefsPath` after the coordination layer was
     removed from git, leaving the Drive mirror as the only copy of the protocol;
  3. a doctrine must not acquire a second entrypoint: the adjacent polemic lane
     `docs/research/atonement/` is checked in both directions (registered <=> present,
     and every file of the lane listed in its own index);
  4. nothing may advertise publication: no self-approval token is allowed, and the
     corpus authority must keep stating that a quote-safe Product article does not exist.

Fail-closed. Writes nothing. Exit 1 on any drift. Perimeter: dead file references are enforced on the
machine registry and on the three governance documents; ordinary prose is left alone on purpose, because
an audit sentence may legitimately name a file that no longer exists.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "ИСКУПЛЕНИЕ"
DOCS = ROOT / "docs" / "research" / "atonement"
REG = CORPUS / "data" / "atonement-corpus-v1.json"
AUTHORITY = CORPUS / "00_CURRENT_AUTHORITY_2026-10-07.md"
NAV = CORPUS / "00_README_AND_NAVIGATION.md"
LEDGER = CORPUS / "07_DRIVE_LIBRARY_AND_RIGHTS_LEDGER.md"
RECON = CORPUS / "17_RECONCILIATION_WITH_CANONICAL_SPINE_2026-10-15.md"
ROOT_README = ROOT / "README.md"

SPINE = (
    "00_README_AND_NAVIGATION.md",
    "00_CURRENT_AUTHORITY_2026-10-07.md",
    "01_MASTER_RESEARCH_MAP_AND_SERIES_ARCHITECTURE.md",
    "02_TERMS_DEFINITIONS_AND_WHAT_IS_ATONEMENT.md",
    "03_BIBLICAL_CORPUS_AND_REDEMPTION_VOCABULARY.md",
    "04_LIMITED_VS_UNIVERSAL_QUESTION_MAP.md",
    "05_SOURCE_REGISTRY_AND_ACQUISITION_QUEUE.md",
    "06_PUBLICATION_ARCHITECTURE_FOR_GOSPOD_BOG.md",
    "07_DRIVE_LIBRARY_AND_RIGHTS_LEDGER.md",
    "08_MURRAY_RAA_SOURCE_CARD.md",
    "09_MURRAY_RAA_INTAKE_AND_COMPLETENESS.md",
    "10_MURRAY_RAA_ARGUMENT_MAP_PRIVATE_STUDY.md",
    "11_MURRAY_OTHER_WORKS_HARD_TEXTS.md",
    "12_HARD_TEXTS_EXTENT_CARDS.md",
    "13_DORT_II_CALVIN_OWEN_EXTENT.md",
    "14_OWEN_DEATH_OF_DEATH_BOOK_IV_LOCATORS.md",
    "15_CALVIN_III24_AND_DORT_II_LOCATORS.md",
    "16_DORT_HEAD_II_ENGLISH_1840_PRIMARY_TEXT.md",
)
SUBLANES = ("ot", "nt", "fathers", "synthesis")
AUTHORITY_ID = "ATONEMENT-CORPUS-AUTHORITY-2026-10-07"
ERRATUM_MARK = "erratum"
FORBIDDEN = (
    "PUBLICATION APPROVED",
    "approved for publication",
    "готов к публикации",
    "цитатный корпус закрыт",
    "публикация разрешена",
)
GIT_PATH = re.compile(r"`((?:ИСКУПЛЕНИЕ|data|docs)/[\w./А-Яа-яЁё-]+?\.(?:md|json|py|ts))`")
NUMBERED = re.compile(r"^(\d{2})_[A-Z0-9_]")

errors: list[str] = []


def req(condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.is_file() else ""


def walk_paths(node, prefix="", holder=None):
    """Every string leaf of the registry with its key path and its nearest object.

    The nearest object travels along because a dead reference is only legal when *that entry*
    declares it (erratum / gitPathState / Drive-only), and a sibling section must not be able to
    grant the exemption by accident.
    """
    if isinstance(node, dict):
        for key, value in node.items():
            yield from walk_paths(value, f"{prefix}.{key}" if prefix else str(key), node)
    elif isinstance(node, list):
        for index, value in enumerate(node):
            yield from walk_paths(value, f"{prefix}[{index}]", holder)
    elif isinstance(node, str):
        yield prefix, node, holder


def resolve(reference: str) -> bool:
    """A governance document may cite a path from the repo root or from inside the corpus."""
    return any((base / reference).exists() for base in (ROOT, CORPUS, DOCS))


# ------------------------------------------------ conflict-ledger statuses --
# Единственный сводный счётчик лана (таблица «Итоговая сводка») был единственной цифрой, которую не
# проверял никто: гейт делегировал числа статусов этой таблице, а таблица жила своей жизнью и молча
# отстала на пять записей. Поэтому разбор записей вынесен в функцию с двумя потребителями: проверка
# сверяет с ней текст таблицы, а режим --print-ledger-summary печатает тот же разбор готовыми
# строками markdown. Держать определение в одном месте — иначе «сводка» и «проверка сводки» разойдутся
# ровно так же, как разошлись таблица и записи.
LEDGER_MD = CORPUS / "synthesis" / "02_CONFLICT_LEDGER.md"
STATUS_DECL = re.compile(r"^- \*\*Статус:\*\* `([A-Z][A-Z0-9_\-]*)`(.*)$")
STATUS_RIVAL = re.compile(r"Статус[^\n`]{0,12}`([A-Z][A-Z0-9_\-]*)`")
STATUS_ASPECT = re.compile(r"\+\s*`([A-Z][A-Z0-9_\-]*)`")
SUMMARY_HEADER = "| Статус | Количество | Записи (основной статус) | Как аспект |"
SUMMARY_SEP = "|---|---|---|---|"
LIVE = {"записейЛеджера": -1, "строкСводки": -1}


def ledger_records(text):
    """C-NN -> строки тела, в порядке файла. Запись = всё между её заголовком и следующим `## `."""
    bodies, order, cur = {}, [], None
    for line in text.split("\n"):
        head = re.match(r"^## (C-\d{2})\.", line)
        if head:
            cur = head.group(1)
            bodies[cur] = []
            order.append(cur)
        elif re.match(r"^## ", line):
            cur = None
        elif cur is not None:
            bodies[cur].append(line)
    return bodies, order


def ledger_status_map(text, vocab):
    """{C-NN: (основной статус, [аспекты])} и список нарушений. Определение ровно одно, общее."""
    bodies, order = ledger_records(text)
    got, problems = {}, []
    for cid in order:
        decls = [m for m in (STATUS_DECL.match(line) for line in bodies[cid]) if m]
        if len(decls) != 1:
            problems.append(
                f"{cid}: деклараций статуса {len(decls)}, а обязана быть ровно одна — строка, начинающаяся "
                "с «- **Статус:**» и значением в обратных кавычках. Пока допустимы три формы и два объявления в одной "
                "записи, «число по статусу» означает «то, на что парсер наткнулся первым»"
            )
            continue
        primary, aspects = decls[0].group(1), STATUS_ASPECT.findall(decls[0].group(2))
        for tok in [primary] + aspects:
            if tok not in vocab:
                problems.append(
                    f"{cid}: статус `{tok}` вне statusVocabulary — словарь закрыт: новое значение сначала "
                    "объявляется в реестре (conflictLedgerGovernance20261023), иначе опечатка в статусе "
                    "выглядит как новый класс записей"
                )
        rivals = [line for line in bodies[cid] if not STATUS_DECL.match(line) and STATUS_RIVAL.search(line)]
        if rivals:
            n = len(rivals)
            word = "строка" if n == 1 else ("строки" if n < 5 else "строк")
            problems.append(
                f"{cid}: кроме канонической декларации в записи ещё {n} {word} с «Статус» рядом с токеном "
                f"в обратных кавычках (первая: {rivals[0].strip()[:70]!r}) — объявление статуса обязано быть "
                "одним: либо допиши аспект в ту же строку после «+», либо убери слово «Статус» из этого места, "
                "иначе «число по статусу» снова зависит от порядка строк в записи"
            )
        got[cid] = (primary, aspects)
    return got, order, problems


def ledger_summary(got, order, vocab):
    """Строки таблицы сводки: подпись статуса берётся из словаря реестра, а не из головы пишущего."""
    rows = []
    for status in vocab:
        primary = sorted(c for c in order if got.get(c, ("", []))[0] == status)
        aspects = sorted(c for c in order if status in got.get(c, ("", []))[1])
        rows.append(f"| `{status}` — {vocab[status]} | {len(primary)} | {', '.join(primary) or '—'} | "
                    f"{', '.join(aspects) or '—'} |")
    return rows


def ledger_table_lines(text):
    """То, что написано в файле под «## Итоговая сводка», как список строк таблицы."""
    at = text.find("## Итоговая сводка")
    if at < 0:
        return []
    out = []
    for line in text[at:].split("\n")[1:]:
        if line.startswith("|"):
            out.append(line.rstrip())
        elif out and line.strip() == "":
            break
    return out


if "--print-ledger-summary" in sys.argv[1:]:
    try:
        _reg = json.loads(read(REG))
    except Exception as _exc:  # noqa: BLE001
        print(f"не прочитан реестр: {_exc}", file=sys.stderr)
        sys.exit(2)
    _voc = {str(x.get("status")): str(x.get("meaning") or "")
            for x in ((_reg.get("conflictLedgerGovernance20261023") or {}).get("statusVocabulary") or [])
            if isinstance(x, dict) and x.get("status")}
    _got, _order, _prob = ledger_status_map(read(LEDGER_MD), _voc)
    for _p in _prob:
        print(f"!-- {_p}", file=sys.stderr)
    if not _voc:
        print("!-- statusVocabulary пуст: печатать нечего, словарь статусов не выдуман из текста записей",
              file=sys.stderr)
        sys.exit(1)
    print(SUMMARY_HEADER)
    print(SUMMARY_SEP)
    for _row in ledger_summary(_got, _order, _voc):
        print(_row)
    sys.exit(1 if _prob else 0)


# ----------------------------------------------------------------- root spine --
for name in SPINE:
    path = CORPUS / name
    if not path.is_file():
        errors.append(f"corpus spine file absent: {name}")
    elif path.stat().st_size < 400:
        errors.append(f"corpus spine file suspiciously small: {name}")

measured_root = len([p for p in CORPUS.glob("*.md") if NUMBERED.match(p.name)])
req(measured_root == len(SPINE) + 1,
    f"corpus root holds {measured_root} numbered files while the gate expects {len(SPINE) + 1} "
    "(SPINE + the reconciliation record): update SPINE deliberately, do not let it drift)")

duplicates = {
    prefix: sorted(p.name for p in CORPUS.glob(f"{prefix}*"))
    for prefix in ("00_CURRENT_AUTHORITY", "00_README_AND_NAVIGATION")
}
for prefix, found in duplicates.items():
    if len(found) != 1:
        errors.append(f"{prefix} must be single-owned, found: {found}")

nav_text = read(NAV)
for path in sorted(CORPUS.glob("*.md")):
    if not NUMBERED.match(path.name) or path.name == NAV.name:
        continue
    if path.name not in nav_text:
        errors.append(f"root corpus file not registered in navigation: {path.name}")
for ghost in set(re.findall(r"`(\d{2}_[A-Z0-9_]+\.md)`", nav_text)):
    if not (CORPUS / ghost).is_file():
        errors.append(f"navigation lists a file that does not exist: {ghost}")

# ---------------------------------------------------------------- sub-corpora --
for sub in SUBLANES:
    sub_dir = CORPUS / sub
    if not sub_dir.is_dir():
        errors.append(f"sub-corpus absent: {CORPUS.name}/{sub}/")
        continue
    md = [p for p in sub_dir.glob("*.md") if NUMBERED.match(p.name)]
    if not md:
        errors.append(f"sub-corpus has no numbered files: {sub}/")
    if not list((sub_dir / "data").glob("*corpus*.json")):
        errors.append(f"sub-corpus has no machine registry in data/: {sub}/")
    if not any("AUTHORITY" in p.name.upper() for p in md):
        errors.append(f"sub-corpus has no own authority file: {sub}/")
sublane_files = sum(len([p for p in (CORPUS / sub).glob("*.md") if NUMBERED.match(p.name)])
                    for sub in SUBLANES if (CORPUS / sub).is_dir())

# ------------------------------------------------------------- machine registry --
registry = {}
try:
    registry = json.loads(read(REG))
except Exception as exc:  # noqa: BLE001 - a broken registry must fail the gate
    errors.append(f"corpus registry unreadable: {exc}")
if registry:
    req(registry.get("authorityId") == AUTHORITY_ID, "registry: authorityId drift")
    agents = registry.get("parallelAgents", {}) if isinstance(registry.get("parallelAgents"), dict) else {}
    # единственный легальный способ сослаться на отсутствующий путь — объявить его отсутствующим
    absent_prefixes = tuple(str(v) for v in (agents.get("declaredAbsentPrefixes") or [])
                            if agents.get("gitPathState"))
    for key_path, raw, _h in walk_paths(registry):
        value = raw.split(" ")[0]          # «…/14_….md §2.6» — якорь раздела, не часть пути
        if not value.startswith(("ИСКУПЛЕНИЕ/", "data/", "docs/", "scripts/")):
            continue
        if resolve(value):
            continue
        if value.startswith(absent_prefixes):
            continue
        if ERRATUM_MARK in key_path.lower() or "gitpathstate" in key_path.lower():
            continue
        errors.append(f"registry: {key_path} points at an absent git path {value!r} "
                      "without an erratum/gitPathState/declaredAbsentPrefixes declaration")
    req(bool(agents.get("gitPathState")) == bool(absent_prefixes),
        "registry: parallelAgents.gitPathState and declaredAbsentPrefixes must be declared together")
    # Имя файла корпуса без префикса пути — это всё равно обещание, что файл в дереве есть.
    # Проза корпуса вне периметра сознательно (см. docstring): историческая запись вправе назвать
    # несуществующий файл, и превращать это в красный CI значило бы учить всех ослаблять гейт.
    bases = [ROOT, CORPUS] + [CORPUS / sub for sub in SUBLANES] + [DOCS]
    for key_path, value, holder in walk_paths(registry):
        name = value.strip()
        if not re.fullmatch(r"(?:[\w./-]+/)?\d{2}_[\w.-]+\.(?:md|json)", name):
            continue
        if name.startswith(absent_prefixes):   # то же объявление отсутствия, что и уPrefixed-скана
            continue
        if any((b / name).exists() or (b / name.split("/")[-1]).exists() for b in bases):
            continue
        declared = isinstance(holder, dict) and any(
            "erratum" in str(v).lower() for v in holder.values() if isinstance(v, str))
        if not declared:
            errors.append(f"registry: {key_path} names a corpus file that exists nowhere in the tree "
                          f"({name!r}) — either restore it or mark the entry with an erratum note")
    lanes = registry.get("adjacentLanes") or []
    req(any(str(item.get("path", "")).endswith("docs/research/atonement") for item in lanes),
        "registry: the adjacent polemic lane is not declared in adjacentLanes")
    for lane in lanes:
        holder = lane.get("registeredIn")
        if holder and not (ROOT / str(holder)).is_file():
            errors.append(f"registry: adjacentLanes.registeredIn points at {holder}")
    drive_parent = str(registry.get("drive", {}).get("parentId", ""))
    req(bool(re.fullmatch(r"[0-9A-Za-z_-]{28,}", drive_parent)),
        "registry: drive.parentId (the Drive intake root) is missing or malformed")

# --------------------------------------------------------- governance documents --
for path in (AUTHORITY, NAV, LEDGER):
    text = read(path)
    if not text:
        errors.append(f"governance document missing: {path.name}")
        continue
    for line_no, line in enumerate(text.splitlines(), 1):
        for referenced in GIT_PATH.findall(line):
            if resolve(referenced):
                continue
            if ERRATUM_MARK in line.lower():
                continue
            errors.append(
                f"{path.name}:{line_no} references an absent git path {referenced!r} "
                "without an erratum line"
            )

root_readme = read(ROOT_README)
registering_lines = [line for line in root_readme.splitlines() if AUTHORITY.name in line]
req(len(registering_lines) == 1,
    f"root README must hold exactly one registration line for the corpus authority, found {len(registering_lines)}")
for line in registering_lines:
    req(CORPUS.name in line, "root README: the corpus authority must be registered by its ИСКУПЛЕНИЕ/ path")

# ------------------------------------------------------------- the docs lane --
if not DOCS.is_dir():
    errors.append("adjacent lane absent: docs/research/atonement — если лан сознательно влит в "
                  "ИСКУПЛЕНИЕ/ или перенесён, удали в том же коммите adjacentLanes из реестра, "
                  "пункт 12 в 00_CURRENT_AUTHORITY и эту проверку; молча «починить» нельзя")
else:
    lane_files = sorted(p for p in DOCS.glob("*.md") if NUMBERED.match(p.name))
    numbers = [p.name[:2] for p in lane_files]
    for duplicate in sorted({n for n in numbers if numbers.count(n) > 1}):
        errors.append(f"docs lane has two files numbered {duplicate}_")
    lane_index = read(DOCS / "README.md")
    for path in lane_files:
        if path.name not in lane_index:
            errors.append(f"docs lane file missing from its own index: {path.name}")
    authority_text = read(AUTHORITY)
    req("docs/research/atonement" in authority_text,
        "docs lane exists but is not registered in the corpus authority (two entrypoints for one graph)")

# ------------------------------------------------------ the gate's own wiring --
gate = registry.get("integrityGate", {}) if registry else {}
gate_script = str(gate.get("script", ""))
gate_workflow = str(gate.get("workflow", ""))
req(bool(gate_workflow) and (ROOT / gate_workflow).is_file(),
    "registry: integrityGate.workflow is absent — a corpus whose gate is not wired has no protection")
req(gate_script == "scripts/" + Path(__file__).name,
    f"registry: integrityGate.script must point at scripts/{Path(__file__).name}")
wf = read(ROOT / gate_workflow) if gate_workflow else ""
if wf:
    req(gate_script in wf, "gate workflow does not run integrityGate.script")
    req(re.search(r"push:\s*\n\s*branches:\s*\[?\s*main", wf),
        "gate workflow does not run on push to main (PR-only trigger = zero protection on main)")
    req("schedule:" in wf and "cron:" in wf, "gate workflow lost its weekly scheduled run")

self_text = Path(__file__).read_text(encoding="utf-8")
req(len(self_text) > 4000 and "publicationEligible=false" in self_text,
    "the gate script has been hollowed out (stub) while the registry still calls it a gate")

# ----------------------------------------------------- conflict-ledger arithmetic --
CONFLICTS = CORPUS / "synthesis" / "02_CONFLICT_LEDGER.md"
if not CONFLICTS.is_file():
    errors.append("conflict ledger absent: synthesis/02_CONFLICT_LEDGER.md")
ledger = read(CONFLICTS)
entries = [int(n) for n in re.findall(r"(?m)^## C-(\d{2})\.", ledger)]
actual = max((int(n) for n in re.findall(r"\bC-(\d{2})\b", ledger)), default=0)
# нумерация без разрывов: 24 заголовка должны давать ровно C-01…C-24, иначе «максимум» и «число»
# расходятся, и ли́дер, сверенный по максимуму, врёт всё равно
if entries and actual and (sorted(set(entries)) != list(range(1, actual + 1))):
    gaps = sorted(set(range(1, actual + 1)) - set(entries))
    dups = len(entries) - len(set(entries))
    errors.append(
        f"conflict ledger: max index C-{actual:02d}, но записей `## C-NN.` — {len(set(entries))} "
        f"(пропуски {gaps[:6]}, повторных номеров {dups}): у каждого расхождения ровно один номер"
    )
# --------- правило 21 (23.10.2026): сводка обязана разлагаться на записи, а не пересказываться --
LIVE["записейЛеджера"] = len(set(entries))
_gov = (registry.get("conflictLedgerGovernance20261023") or {})
_vocab: dict[str, str] = {}
for _x in (_gov.get("statusVocabulary") or []):
    if isinstance(_x, dict) and str(_x.get("status") or "").strip():
        _vocab[str(_x["status"]).strip()] = str(_x.get("meaning") or "").strip()
if not _vocab:
    errors.append(
        "conflictLedgerGovernance20261023.statusVocabulary пуст или блока нет — сводку леджера нечем "
        "сверять; без закрытого словаря «статус» — это любое слово, которое автор записи поставил в "
        "обратные кавычки, а правило 18 уже запрещает молчаливо отсутствующий обязательный блок"
    )
else:
    if any(not m for m in _vocab.values()):
        errors.append("statusVocabulary: есть статусы без подписи meaning — подпись печатается в таблице "
                      "сводки и обязана быть объявлена, а не сочинена по месту")
    _got, _order, _prob = ledger_status_map(ledger, _vocab)
    errors.extend(_prob)
    _prim = {c: v[0] for c, v in _got.items()}
    _asp = {c: v[1] for c, v in _got.items()}
    _unused = [s for s in _vocab if s not in set(_prim.values()) and not any(s in a for a in _asp.values())]
    if _unused:
        errors.append(f"statusVocabulary объявляет {_unused}, которых нет ни в одной записи леджера — "
                      "словарь обязан соответствовать записям, а не переживать их (мёртвое правило "
                      "страшнее отсутствия правила: оно создаёт видимость проверки)")
    _gen = [SUMMARY_HEADER, SUMMARY_SEP] + ledger_summary(_got, _order, _vocab)
    _actual = ledger_table_lines(ledger)
    LIVE["строкСводки"] = len([x for x in _actual if x.startswith("| `")])
    if not _actual:
        errors.append("в леджере нет таблицы «## Итоговая сводка» — её отсутствие выглядит как "
                      "«сверять нечего», а не как нарушение; строка обязана быть и обязана совпасть")
    elif _actual != _gen:
        first = next((i for i, (a, b) in enumerate(zip(_actual, _gen)) if a != b), min(len(_actual), len(_gen)))
        errors.append(
            f"сводка леджера разошлась с записями (первое расхождение — строка {first + 1}): в файле "
            f"{(_actual[first] if first < len(_actual) else 'нет строки')!r}, записи дают "
            f"{(_gen[first] if first < len(_gen) else 'нет строки')!r}; таблицу не правят руками — "
            "переснять: python3 -B scripts/validate_atonement_corpus_integrity.py --print-ledger-summary "
            "и вставить вывод под заголовок «## Итоговая сводка» (строк в таблице "
            f"{len([x for x in _actual if x.startswith('| `')])}, записей {LIVE['записейЛеджера']})"
        )
# сверяется КАЖДЫЙ объявленный диапазон, а не один названный мной путь: дрейф жил во втором ли́дере
# (synthesis/00_SYNTHESIS_AUTHORITY объявлял C-01…C-15 при леджере C-24), и проверка по одному
# файлу его пропускала по построению
for auth in sorted(CORPUS.rglob("00_*AUTHORITY*.md")):
    claimed = [int(n) for n in re.findall(r"C-\d{2}\s*[.…]+\s*C-?(\d{2})", read(auth))]
    if claimed and actual and max(claimed) != actual:
        errors.append(
            f"{auth.relative_to(ROOT)}: объявлен диапазон C-01…C-{max(claimed):02d}, в леджере "
            f"C-{actual:02d} ({len(set(entries))} записей) — обнови ли́дер, не оставляй счётчик устаревшим; "
            "переснять: grep -cE '^## C-[0-9]{2}\\.' synthesis/02_CONFLICT_LEDGER.md. Числа статусов "
            "в ли́дер не переносить: они сведены таблицей в самом леджере, а таблица с 23.10 сверяется "
            "правилом 21 с записями (пересъём: --print-ledger-summary); дубль числа и есть источник дрейфа, "
            "и единственный способ его видеть — сделать дубль проверяемым"
        )

# ------------------------------------------------------------ merge hygiene --
# соседний лан конфликтует с корпусом по 27 путям (предполёт 2026-10-16), поэтому закоммиченные
# маркеры разрешения конфликта — реальный, а не гипотетический способ испортить корпус
CONFLICT_LINE = re.compile(r"^(?P<kind>[<>=|]{7})(?: .*)?$")
for path in sorted(CORPUS.rglob("*.md")) + sorted(CORPUS.rglob("*.json")):
    text = path.read_text(encoding="utf-8", errors="ignore")
    hits = {}
    for line_no, line in enumerate(text.splitlines(), 1):
        found = CONFLICT_LINE.match(line)
        if found:
            hits.setdefault(found.group("kind"), []).append(line_no)
    # «=======» сам по себе законен как underlined-заголовок markdown, поэтому считается
    # признаком конфликта только в файле, где есть ещё и <<<<<<< или >>>>>>>
    real = {"<<<<<<<", ">>>>>>>", "|||||||"} & set(hits)
    if real:
        for kind in sorted(real | {"======="} & set(hits)):
            errors.append(f"{path.relative_to(ROOT)}:{hits[kind][0]} unresolved merge-conflict marker "
                          f"{kind!r} (строки {', '.join(map(str, hits[kind][:4]))}) — корпус не должен "
                          "содержать незакрытые разрешения конфликтов")

# ------------------------------------------------------------- publication wall --
for path in list(CORPUS.rglob("*.md")) + list(DOCS.rglob("*.md")):
    text = path.read_text(encoding="utf-8", errors="ignore")
    for token in FORBIDDEN:
        if token.lower() in text.lower():
            errors.append(f"{path.relative_to(ROOT)}: forbidden self-approval token {token!r}")
authority_text = read(AUTHORITY)
req("Quote-safe Product" in authority_text and "NO" in authority_text,
    "corpus authority lost its quote-safe Product = NO statement")
req("## 3. HOLD" in authority_text, "corpus authority lost its HOLD section")
req(RECON.is_file(), "the reconciliation record of the 2026-10-15 audit must stay in the corpus")
if RECON.is_file():
    recon_text = read(RECON)
    for needle in ("unrelated", "99 — HOLD", "7 880", "Erratum 2026-10-22", "a01664c8"):
        req(needle in recon_text, f"reconciliation record no longer states {needle!r}")

# ------------------------------------------------ measurement hygiene (2026-10-22) --
# Урок сессии: два дня выводы опирались на git-замеры, которые давала СЛОМАННАЯ СРЕДА
# (shallow-клон: пустой merge-base -> «unrelated histories» -> «16/20 add/add», «битый JSON
# реестра в дереве мержа», «squash сносит ot/»). На полной истории те же концы дают 0 конфликтов.
# Поэтому защищаемся машиной: любая записанная съёмка обязана (1) иметь точное время, (2) иметь
# способ переснять себя, (3) не прятать плейсхолдеры в измеренных полях, и (4) сверяться с git'ом
# там, где git её видит.
notes = []
if REG.is_file():
    reg = json.loads(read(REG))

    # (1)+(2) датированная съёмка обязана быть точной и переснимаемой
    STAMP = re.compile(r"^(?:at|measuredAt|checkedAt|measuredOn|measuredAtGit)$")
    HOW = {"method", "methods", "how", "howRule", "recheckCommand", "proofCommand", "measuredIn",
           "measuredFromTheirBase", "which", "command", "measuredBy"}
    _stamp_sites = {}

    def walk_measure(node, where, label=None):
        if isinstance(node, dict):
            stamps = sorted(k for k in node if STAMP.match(str(k)))
            if stamps and label is not None:
                # поле в словаре может быть не одно: считать надо все, иначе «проверено N мест» врёт
                _stamp_sites[label] = _stamp_sites.get(label, 0) + len(stamps)
            for st in stamps:
                # раньше проверялся только stamps[0]; если в записи два поля даты (at + measuredAtGit),
                # второе оставалось необследованным — дыра, найденная при ручной перепроверке
                val = str(node[st])
                if not re.search(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}", val):
                    errors.append(
                        f"{where}.{st} = {val!r}: съёмка без точного времени (HH:MM). Дата без "
                        "часов не позволяет отличить «устарело» от «проверено сегодня»"
                    )
            if stamps and not (set(map(str, node)) & HOW):
                errors.append(
                    f"{where}: датировано, но способа переснять нет (нет ни одного из {sorted(HOW)[:4]}…). "
                    "Число, которое нельзя переснять, — это мнение, а не замер"
                )
            for key, val in node.items():
                walk_measure(val, f"{where}.{key}", label)
        elif isinstance(node, list):
            for i, val in enumerate(node):
                walk_measure(val, f"{where}[{i}]", label)
    # обход по ВСЕМ machine-реестрам корпуса, а не по одному: у четырёх под-корпусов
    # сегодня ноль полей этой формы, поэтому распространение ничего не ломает — но именно поэтому
    # оно единственное, что помешает им заболеть тем же через неделю
    _registries = [("реестр", REG)]
    for _sub in SUBLANES:
        _d = CORPUS / _sub / "data"
        if _d.is_dir():
            for _q in sorted(_d.glob("*corpus*.json")):
                _registries.append((f"реестр {_sub}", _q))
    _docs = {}
    for _label, _path in _registries:
        try:
            _docs[_label] = json.loads(read(_path))
        except Exception as _exc:  # noqa: BLE001
            errors.append(f"{_label} ({_path.name}) не читается: {_exc}")
    for _label in _docs:
        walk_measure(_docs[_label], _label, _label)

    # (2b) число проверяемых мест обязано быть записано и сверено: иначе «ноль нарушений» неотличим
    # от «правилу не за что зацепиться». У своих реестров расхождение — ошибка; у чужих, которые поле
    # только что приобрели, — записка: требовать от соседа править мой реестр я не вправе
    _decl = ((reg.get("integrityGate") or {}).get("scopeOfMeasurementRules") or {}).get(
        "stampedFieldsPerRegistry") or {}
    if "корпус" not in _decl:
        errors.append(
            "integrityGate.scopeOfMeasurementRules.stampedFieldsPerRegistry нет — сколько мест правило "
            "действительно видит должно быть записано, а не выводимо из моего молчания"
        )
    for _lab, _got in sorted(_stamp_sites.items()):
        _k = "корпус" if _lab == "реестр" else _lab.replace("реестр ", "")
        drift = (_decl[_k] != _got) if _k in _decl else bool(_got)
        if not drift:
            continue
        msg = (f"stampedFieldsPerRegistry[{_k!r}] = {_decl.get(_k)!r}, а обход правила нашёл {_got} полей формы "
               "at|measuredAt|checkedAt|measuredOn|measuredAtGit")
        if _k == "корпус":
            errors.append(msg + " — число в реестре обязано совпадать с тем, что видит проверка (считать надо тем же "
                                "определением, которым проверяешь)")
        else:
            # чужой реестр: сама датированная съёмка обязана быть точной (правила (1)-(3) выше их ловят), но
            # моя запись о количестве их полей — моя бухгалтерия, и требовать от соседа править мой файл я не вправе
            notes.append(msg + " — счётчик в моём реестре устарел из-за чужих изменений; исправлю я, блокировать "
                               "чужой прогон из-за своей цифры не буду")

    # (3) плейсхолдеры в измеренных полях
    MEASURED_KEY = re.compile(r"(?:At|Time|Bytes|Count|Total|Lines|Size)$", re.I)
    FAKE = re.compile(r"\d{2}:[0-5]?xZ|\d{2}:\d{2}x|\bX{2,4}:\d{2}\b|\bTODO\b|\bTBD\b|плейсхолд|placeholder", re.I)
    def walk_fake(node, where):
        if isinstance(node, dict):
            for key, val in node.items():
                if MEASURED_KEY.search(str(key)) and isinstance(val, (str, int, float)) and FAKE.search(str(val)):
                    errors.append(f"{where}.{key} = {val!r}: измеренное поле содержит плейсхолдер — "
                                  "снимите число командой вместо правки текста")
                walk_fake(val, f"{where}.{key}")
        elif isinstance(node, list):
            for i, val in enumerate(node):
                walk_fake(val, f"{where}[{i}]")
    for _label in _docs:
        walk_fake(_docs[_label], _label)

    # (4) записанные времена коммитов сверяются с git'ом (когда объект доступен)
    checks = (reg.get("branchTopologyAudit20261022") or {}).get("commitTimeChecks") or {}
    if checks:
        import os
        import subprocess
        env = dict(os.environ, TZ="UTC")
        unseen = []
        for sha, want in sorted(checks.items()):
            if subprocess.run(["git", "cat-file", "-e", sha + "^{commit}"], cwd=ROOT,
                              capture_output=True).returncode != 0:
                unseen.append(sha)
                continue
            got = subprocess.run(["git", "log", "-1", "--date=format-local:%Y-%m-%dT%H:%M:%SZ",
                                  "--format=%cd", sha], cwd=ROOT, env=env, capture_output=True,
                                 text=True).stdout.strip()
            if got != want:
                errors.append(
                    f"commitTimeChecks[{sha}] = {want!r}, git даёт {got!r}. Канон: TZ=UTC git log -1 "
                    "--date=format-local:%Y-%m-%dT%H:%M:%SZ --format=%cd. Формат %cI не нормализует: "
                    "он печатает смещение, записанное в коммите (+03:00 у владельческих), и потому "
                    "рожает сдвиг на 3 часа"
                )
        if unseen:
            notes.append(f"commitTimeChecks: {len(unseen)} sha недоступно в этом клоне — не проверено "
                         f"({', '.join(unseen[:4])})")
        if len(unseen) == len(checks):
            errors.append(
                f"commitTimeChecks: ни одна из {len(checks)} записей не сверена (git не видит ни одного "
                "коммита) — проверка, которая ничего не сверяет, не имеет права называться PASS; "
                "обычная причина — shallow-клон или отсутствие .git"
            )

# --------------------------------------------- governance docs -> registry refs --
# Коммит ae2821a (22.10) уехал с правкой 17_, ссылающейся на реестровый ключ, которого скрипт-заполнитель
# не создал (упал на KeyError, а коммит стоял отдельной командой). Ослаблять внимание бессмысленно: ссылка
# на несуществующие данные должна быть невозможна. Проверяются только те `ключ.подключ` в markdown корпуса,
# чей первый сегмент — реальный верхний ключ реестра; прозаическое «git status» или имя файла не трогается.
REF = re.compile(r"`([A-Za-z][A-Za-z0-9_]*)((?:\.[A-Za-z0-9_]+|\[\d+\])+?)`")


def _resolve(root_node, path_str):
    node = root_node
    for step in re.findall(r"\.([A-Za-z0-9_]+)|\[(\d+)\]", path_str):
        attr, idx = step
        if idx:
            if not isinstance(node, list) or not (0 <= int(idx) < len(node)):
                return False
            node = node[int(idx)]
        else:
            if not isinstance(node, dict) or attr not in node:
                return False
            node = node[attr]
    return True


_top_keys = set(registry) if isinstance(registry, dict) else set()
for _md in sorted(CORPUS.rglob("*.md")):
    _text = read(_md)
    if "реестр" not in _text and "atonement-corpus-v1.json" not in _text:
        continue
    for _m in REF.finditer(_text):
        head, tail = _m.group(1), _m.group(2)
        if head not in _top_keys or not tail:
            continue
        if re.search(r"[A-Z]{2,}", tail):
            # описательный шаблон имени (`driveMirrors.fileNN` = «file + номер файла»), а не путь к записи:
            # исключение точечное и только для верхнерегистровых маркеров — строчный ключ обязан разрешиться
            continue
        if head not in registry or not _resolve(registry[head], tail):
            errors.append(
                f"{_md.relative_to(ROOT)} ссылается на `{head}{tail}`, но такого пути в "
                f"data/atonement-corpus-v1.json нет — запись не внесена (или внесена под другим именем); "
                "ссылку убрать нельзя, надо внести данные: python3 -B "
                "scripts/validate_atonement_corpus_integrity.py"
            )

# ------------------------------------- обязательные блоки реестра (правило 18) --
# Гейт читает governance-блоки через .get(...) or {}, поэтому молчаливое удаление целого
# блока выглядит как зелёное состояние: код возврата не теряется — теряется обязанность
# проверять. Присутствие каждого обязательного блока требуется явно (22.10.2026).
_REQUIRED_BLOCKS = [
    ("branchTopologyAudit20261022.commitTimeChecks",
     lambda: (reg.get("branchTopologyAudit20261022") or {}).get("commitTimeChecks")),
    ("driveSourceAudit20261016.correctionsPending",
     lambda: (reg.get("driveSourceAudit20261016") or {}).get("correctionsPending")),
    ("driveSourceAudit20261016.correctionsPendingCount",
     lambda: (reg.get("driveSourceAudit20261016") or {}).get("correctionsPendingCount")),
    ("integrityGate.rules.mutationGroups",
     lambda: ((reg.get("integrityGate") or {}).get("rules") or {}).get("mutationGroups")),
    ("integrityGate.rules.mutationTotal",
     lambda: ((reg.get("integrityGate") or {}).get("rules") or {}).get("mutationTotal")),
    ("integrityGate.rules.mutationScore20261022",
     lambda: ((reg.get("integrityGate") or {}).get("rules") or {}).get("mutationScore20261022")),
    ("branchTopologyAudit20261022.branchRetirement.recheckCommand",
     lambda: ((reg.get("branchTopologyAudit20261022") or {}).get("branchRetirement") or {}).get("recheckCommand")),
]
for _blk_name, _blk_get in _REQUIRED_BLOCKS:
    try:
        _blk_val = _blk_get()
    except Exception as _exc:  # noqa: BLE001
        errors.append(f"registry: обязательный блок {_blk_name} нечитаем: {_exc}")
        continue
    if not _blk_val:
        errors.append(
            f"registry: обязательный блок {_blk_name} отсутствует или пуст — отсутствие проверки "
            "не должно выглядеть как её прохождение (правило 18)"
        )

# ------------------------------------------- correctionsPending: единая схема --
# 22.10: шесть записей были в форме where/was/now, одна — where/status/erratum, седьмая — what/*. Из-за этого
# «сколько открытых» нельзя ни посчитать, ни проверить — а это единственный вопрос, который имеет смысл к
# незакрытому периметру. Схема приведена к where/defect/resolution/applied, и далее она требуется машиной.
_cpc = (reg.get("driveSourceAudit20261016") or {}).get("correctionsPending") or []
# «единая схема» обязана означать то, что проверяется: не «есть обязательный каркас» (тогда лишние ключи
# плодятся и счётчик снова зависит от удачи), а каркас + закрытый список разрешённых полей.
_sch = (reg.get("driveSourceAudit20261016") or {}).get("correctionsPendingSchema") or {}
_REQ = tuple(_sch.get("required") or ())
_OPT = set(_sch.get("optional") or ())
if _cpc and not _REQ:
    errors.append(
        "correctionsPendingSchema.required нет — «единая схема» без перечня обязательных ключей означает "
        "«схема есть у того, кто смотрит последним»"
    )
    _REQ = ("where", "defect", "resolution", "applied", "why", "checkedAgainstMain20261022")
for _i, _c in enumerate(_cpc):
    _miss = [k for k in _REQ if k not in _c]
    _extra = sorted(set(map(str, _c)) - set(_REQ) - _OPT)
    if _extra:
        errors.append(
            f"correctionsPending[{_i}] несёт ключи {_extra} вне разрешённой схемы — запись с собственным набором "
            "полей нельзя ни посчитать, ни прочитать; перенести смысл в why/resolution или расширить "
            "correctionsPendingSchema.optional (расширение — явный шаг, а не молчаливая вольность)"
        )
    if _miss:
        errors.append(
            f"реестр.driveSourceAudit20261016.correctionsPending[{_i}] без обязательных ключей {_miss} — "
            "запись в произвольной форме не читается машиной и не считается; перенести текст в where/defect/resolution"
        )
    _empty = [k for k in _REQ if isinstance(_c.get(k), str) and not _c[k].strip()]
    if _empty:
        errors.append(
            f"correctionsPending[{_i}] пустые в смысловых полях {_empty}: наличие ключа — ещё не утверждение. "
            "Схема, допускающая пустоту там, где живёт смысл, проверяет форму и молчит о содержании; если поле "
            "незаполнимо по делу (например, applied без сделанного), запись обязана быть открытой, а не закрытой пустотой"
        )
    if _c.get("applied") is True and not str(_c.get("resolution") or "").strip():
        errors.append(
            f"correctionsPending[{_i}] помечена applied=true без resolution — «закрыто» без того, чем закрыто, "
            "неотличимо от «забыли»"
        )
    if "applied" in _c and not isinstance(_c["applied"], bool):
        errors.append(
            f"correctionsPending[{_i}].applied = {_c['applied']!r}: только true/false, иначе «закрыто» становится мнением"
        )
_claim = (reg.get("driveSourceAudit20261016") or {}).get("correctionsPendingCount") or {}
if _cpc and _claim:
    _open = sum(1 for c in _cpc if not c.get("applied"))
    if (_claim.get("total"), _claim.get("open"), _claim.get("applied")) != (len(_cpc), _open, len(_cpc) - _open):
        errors.append(
            f"correctionsPendingCount говорит total/open/applied = "
            f"{_claim.get('total')}/{_claim.get('open')}/{_claim.get('applied')}, а по составу "
            f"{len(_cpc)}/{_open}/{len(_cpc) - _open}: после любой новой записи или закрытия число обязано быть переснято"
        )
elif _cpc and not _claim:
    errors.append("correctionsPending есть, а correctionsPendingCount нет — число открытых записей никто не сверяет")

# ------------------------------------------- смешанное письмо в governance-слое --
# Три опечатки за один день («файловold», «валидаторыPASS», «правилa», «Соumur» вместо Сомюра) — это не вкус, а
# класс: латинская буква внутри кириллического слова не видна глазами и меняет слово в поиске, в цитате и в diff.
# Проверка ограничена governance-слоем этого лана (файлы корня ИСКУПЛЕНИЕ/*.md) — не из удобства, а по праву:
# под-корпусы nt/ и fathers/ содержат те же дефекты (12 вхождений в 5 файлах), но они чужие, и там заведено
# открытое замечание, а не моя правка.
MIXED = re.compile(r"[А-Яа-яЁё][A-Za-z]{1,}[А-Яа-яЁё]*|[A-Za-z]{1,}[А-Яа-яЁё][A-Za-zА-Яа-яЁё]*")
# Цитата дефектного слова — не его употребление: «в файле было Соumur» обязана оставаться точной. Поэтому
# перед поиском вырезаются «ёлочки» и `backtick`--spans (общий способ для дока и для сообщений коммитов),
# а то, что осталось без кавычек, — это то, чем я пользуюсь, и оно обязано быть русским.
QUOTED = re.compile(r'«[^»]*»|`[^`]*`|"[^"]*"')


def mixed_words(text: str):
    """Слова, где кириллица и латиница склеены. Ищем целыми токенами, а не границей график: сообщение
    «8:рpusа» найти слово не помогает, «8:корpusа» — помогает."""
    bare = QUOTED.sub(" ", text)
    out = []
    for m in re.finditer(r"[^\W\d_]+", bare):
        w = m.group(0)
        if re.search(r"[А-Яа-яЁё]", w) and re.search(r"[A-Za-z]", w):
            out.append(w)
    return out
# Цитата самого дефекта обязана оставаться точной («в файле было Соumur вместо Сомюр»), поэтому исключение
# разрешено — но только построчно, только этим маркером, и число маркеров сверяется с объявленным в реестре.
# Иначе «ослабили проверку» превращается в «добавили ещё один case» — молча и необратимо.
EXEMPT = "<!-- mixed-script:цитата-дефекта -->"

# ---- реестр массы «четырёхпунктников» (docs/research/atonement/35_) — измеряется, а не цитируется
MASS_FILE = DOCS / "35_four_point_authors_mass_registry.md"
MASS_ROW = re.compile(r"^\|\s*FP-(\d+)\s*\|")
MASS_Q = re.compile(r"^- Q-(\d+) —")
MASS_CLS = ("A1", "A2", "B1", "B2", "C")
MASS_LOC = re.compile(r"(с\.\s*\d|с\.\s*\d|pp?\.\s*\d|col\.|пар\.\s*\d|§\s*\d|§\d|PL \d+:\d+|CSEL|GCS|WA \d|по лану|по корпусу)")
MASS_LANEREF = re.compile(r"`(\d{2})_`")
MASS_PATHREF = re.compile(r"`(ИСКУПЛЕНИЕ/[A-Za-z0-9_/.\-]+?)(?:\s[^`]*)?`")

CJK_GLYPH = re.compile(r"[\u3000-\u9fff\uff01-\uff5e\u3001-\u303f]")


def cjk_hits(paths):
    """CJK вне цитат: {путь: [(строка, фрагмент)]}. Цитатные скобки вычитываются — освобождение для
    цитаты защищает и опечатки, поэтому «образец дефекта» в backtick'ах остаётся законным (ср. правило 22)."""
    out = {}
    for p in paths:
        try:
            txt = p.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        hits = []
        for n, line in enumerate(txt.split("\n"), 1):
            bare = QUOTED.sub(" ", line)
            for m in CJK_GLYPH.finditer(bare):
                hits.append((n, bare[max(0, m.start() - 6):m.start() + 7].strip()))
        if hits:
            out[str(p.relative_to(ROOT))] = hits
    return out


def measure_mass_registry():
    """Определение, которым мерит правило 23: строка = «| FP-NN | … | `класс` | …».

    Возвращает (rows, queue, lane_refs, exists); rows = {номер: (класс, текст строки)}.
    """
    if not MASS_FILE.is_file():
        return {}, set(), set(), False
    rows: dict[int, tuple] = {}
    queue: set[int] = set()
    refs: set[str] = set()
    for line in MASS_FILE.read_text(encoding="utf-8", errors="replace").split("\n"):
        m = MASS_ROW.match(line)
        if m:
            found = re.findall(r"`(A1|A2|B1|B2|C)`", line)
            rows[int(m.group(1))] = (found[0] if found else None, line)
            refs.update(MASS_LANEREF.findall(line))
        else:
            # путь проверяется по всему файлу: ссылка в прозе обязана находиться так же, как в таблице
            refs.update(MASS_PATHREF.findall(line))
        mq = MASS_Q.match(line)
        if mq:
            queue.add(int(mq.group(1)))
    return rows, queue, refs, True


_exempt_total = 0
for _md in sorted(CORPUS.glob("*.md")):
    _txt = read(_md)
    _bad = []
    _exempt = 0
    for _ln, _line in enumerate(_txt.split("\n"), 1):
        if EXEMPT in _line:
            _exempt += 1
            continue
        for _w in mixed_words(_line):
            _bad.append(f"{_ln}:{_w}")
    _exempt_total += _exempt
    if _bad:
        errors.append(
            f"{_md.relative_to(ROOT)}: {len(_bad)} слов смешанного письма (кириллица+латиница в одном слове): "
            f"{', '.join(_bad[:6])}{'…' if len(_bad) > 6 else ''} — исправить букву, а не искать глазами; "
            "переснять: grep -nE '[А-Яа-яЁё][A-Za-z]|[A-Za-z][А-Яа-яЁё]' " + _md.name +
            " | grep -v mixed-script:цитата-дефекта"
        )
_msc = (reg.get("integrityGate") or {}).get("mixedScriptCheck") or {}
if "exemptionsDeclared" in _msc and int(_msc["exemptionsDeclared"]) != _exempt_total:
    errors.append(
        f"mixedScriptCheck.exemptionsDeclared = {_msc['exemptionsDeclared']}, строк с маркером в периметре — {_exempt_total}: "
        "исключение из проверки — это тоже факт, он обязан быть переснят (grep -c '" + EXEMPT + "' ИСКУПЛЕНИЕ/*.md)"
    )

if REG.is_file():
    # (1w) гранульность времени: правило по ИМЕНИ ключа пропускало даты, лежащие под другими именами
    # (wave_date, cutoff, checkedOn, ingestedIntoGit). Смотрю на ФОРМУ значения: если это ровно
    # ГГГГ-ММ-ДД, поле обязано либо нести часы (имя съёмки), либо быть объявлено днём по определению.
    DATEONLY = re.compile(r"^\d{4}-\d{2}-\d{2}$")
    # имя оканчивается на At|On|Time — поле обещает отметку времени; Date|Day — обещает день, и требовать
    # от него часов значит подменять смысл поля удобной проверкой
    MEASUREMENT_NAME = re.compile(r"(?:at|on|time|timestamp)$", re.I)
    _daydecl = ((reg.get("integrityGate") or {}).get("dayGranularity") or {})
    _declared_paths = {str(x.get("path")) for x in (_daydecl.get("declared") or [])}

    def walk_granularity(node, path, src, acc):
        if isinstance(node, dict):
            for key, val in node.items():
                # сами декларации дневной гранульности содержат даты — это реестр исключений, а не поле-съёмка;
                # иначе правило кормится собственным текстом и никогда не сойдётся
                if src == "реестр" and path == ".integrityGate" and str(key) == "dayGranularity":
                    continue
                if isinstance(val, str) and DATEONLY.match(val.strip()):
                    acc.append((src, path + "." + str(key), bool(MEASUREMENT_NAME.search(str(key)))))
                walk_granularity(val, path + "." + str(key), src, acc)
        elif isinstance(node, list):
            for i, val in enumerate(node):
                walk_granularity(val, f"{path}[{i}]", src, acc)

    _gran = []
    for _label, _path in _registries:
        if _label in _docs:
            walk_granularity(_docs[_label], "", _label, _gran)
    for _src, _pth, _ismeas in _gran:
        if _src != "реестр":
            continue
        if _ismeas:
            errors.append(
                f"корпус{_pth} = значение-дата без часов при имени, обозначающем съёмку: точность дня здесь не "
                "определение, а незамеренное время — переснимите git'ом канонической командой: TZ=UTC git log -1 --date=format-local:%Y-%m-%dT%H:%M:%SZ --format=%cd (не %cI: он выдаёт локальное смещение и уже ломал сверку на +03:00) "
                "или назовите поле днём по определению и объявите в integrityGate.dayGranularity"
            )
        elif _pth not in _declared_paths:
            errors.append(
                f"корпус{_pth}: дата ровно в один день нигде не объявлена как дневная гранульность — "
                "либо переснять с часами, либо записать в integrityGate.dayGranularity.declared с whyDay; "
                "иначе читатель не отличит «измерено в этот день» от «не догадались померить точнее»"
            )
    def _laney(label):
        return "корпус" if label == "реестр" else label.replace("реестр ", "")

    _counts = {}
    for _src, _pth, _ismeas in _gran:
        _counts[_laney(_src)] = _counts.get(_laney(_src), 0) + 1
    _gran_foreign = {k: v for k, v in _counts.items() if k != "корпус"}
    _smr = (reg.get("integrityGate") or {}).get("scopeOfMeasurementRules") or {}
    _daydecl_fig = _smr.get("dayOnlyFieldsPerRegistry") or {}
    _myday = _counts.get("корпус", 0)
    if _daydecl_fig:
        _badfig = {k: (v, _counts.get(k, 0)) for k, v in _daydecl_fig.items() if _counts.get(k, 0) != v}
        _absent = sorted(set(_counts) - set(map(str, _daydecl_fig)))
        if _absent:
            errors.append(f"dayOnlyFieldsPerRegistry не покрывает ланы {_absent} — в них поля дневной точности есть")
        if _badfig:
            _mine = {k: v for k, v in _badfig.items() if k == "корпус"}
            _theirs = {k: v for k, v in _badfig.items() if k != "корпус"}
            if _mine:
                errors.append(
                    "scopeOfMeasurementRules.dayOnlyFieldsPerRegistry разошёлся с обходом по моему периметру: "
                    + ", ".join(f"{k}: записано {v[0]!r}, видим {v[1]}" for k, v in sorted(_mine.items()))
                    + " — моё собственное число обязано быть переснятым, а не унаследованным"
                )
            if _theirs:
                # цифра о чужом лане живёт в моём файле, а править его может только владелец лана:
                # блокировать чужой прогон моим устаревшим числом — то же зло, что и молчание о нём
                notes.append(
                    "dayOnlyFieldsPerRegistry разошёлся с обходом по чужим реестрам: "
                    + ", ".join(f"{k}: записано {v[0]!r}, видим {v[1]}" for k, v in sorted(_theirs.items()))
                    + " — замечание владельцу лана; прогон не блокируется, потому что переснять чужую бухгалтерию "
                    "из этого PR я не могу, а врать молчанием не хочу"
                )
        # нуль для существующего лана — это не лишнее число, а ровно то, что мы просим держать на виду
        _lanes = {_laney(_l) for _l in _docs}
        _extrafig = sorted(set(map(str, _daydecl_fig)) - _lanes)
        if _extrafig:
            errors.append(
                f"dayOnlyFieldsPerRegistry содержит {_extrafig}, а такого лана нет среди просматриваемых реестров — "
                "ссылка на несуществующий периметр хуже, чем ноль"
            )
    elif _myday or _gran_foreign:
        errors.append(
            "число полей «дата ровно в день» по пяти реестрам не записано в scopeOfMeasurementRules."
            "dayOnlyFieldsPerRegistry — без него «ноль нарушений» снова означает «правило молчало»"
        )
    if _gran_foreign:
        _fmeas = sum(1 for src, pth, ismeas in _gran if src != "реестр" and ismeas)
        if _fmeas:
            notes.append(
                f"в чужих под-реестрах {_fmeas} полей с именем съёмки и точностью в один день — не ошибка владельца "
                "этого PR: правило (1w) к чужим данным применяется как измерение, а не как блокировка"
            )

    # (2f) лестница версий гейта: если число ошибок по версиям разложено, сумма групп обязана равняться
    # числу строк лестницы — то же требование, что к раскладке ошибок на родителе и к собственному счёту мутаций
    _lad = (reg.get("branchTopologyAudit20261022") or {}).get("gateOnMainTree", {}).get("measurementLadder20261022") or {}
    if _lad.get("breakdown"):
        _lrows = len(_lad.get("rows") or [])
        _lsum = sum(int(v) for v in _lad["breakdown"].values())
        _lver = int(_lad.get("versionGroups", -1))
        if _lsum != _lrows or _lver != _lrows:
            errors.append(
                "measurementLadder20261022: групп %d, строк %d, versionGroups %d — раскладка, итог и состав обязаны "
                "сойтись, иначе таблица версий выдаёт себя за доказательство, оставаясь списком"
                % (_lsum, _lrows, _lver)
            )
        _vals = {}
        for _r in _lad.get("rows") or []:
            _vals[int(_r.get("errorsOnMain", -1))] = _vals.get(int(_r.get("errorsOnMain", -1)), 0) + 1
        if {str(k): v for k, v in _vals.items()} != {str(k): int(v) for k, v in _lad["breakdown"].items()}:
            errors.append(
                "measurementLadder20261022.breakdown не совпадает с фактическим распределением строк по errorsOnMain "
                "(обход видит %s) — группа, которую никто не пересчитал, это украшение таблицы" % sorted(_vals.items())
            )

    # (2e) форма документа-сверки:число строк и число разделов — тоже числа, которые я публикую, значит они
    # обязаны пересниматься этим же обходом, а не переживать следующую правку текста.
    _doc_fig = reg.get("reconciliationDocument20261022") or {}
    _docp = CORPUS / str(_doc_fig.get("path", ""))
    if _doc_fig and _docp.is_file():
        _dtxt = read(_docp)
        _dlines = len(_dtxt.rstrip("\n").split("\n"))
        _dh2 = len([x for x in _dtxt.split("\n") if x.startswith("## ")])
        _dh3 = len([x for x in _dtxt.split("\n") if x.startswith("### ")])
        _dwant = {"lines": _dlines, "sectionsH2": _dh2, "sectionsH3": _dh3}
        _dbad = {k: (int(_doc_fig.get(k, -1)), v) for k, v in _dwant.items() if int(_doc_fig.get(k, -1)) != v}
        if _dbad:
            errors.append(
                "reconciliationDocument20261022 разошёлся с файлом: "
                + ", ".join(f"{k}: записано {v[0]!r}, видим {v[1]}" for k, v in sorted(_dbad.items()))
                + " — заголовок правят чаще, чем цифру под ним; переснимите или уберите поле"
            )
        _dlev = re.search(r"^(#{3,4}) 15\. ", _dtxt, re.M)
        _dsub = len(re.findall(r"^### 15[a-e]\. ", _dtxt, re.M))
        if _dlev and _dlev.group(1) != "##":
            errors.append("раздел 15 описан_level %s, хотя его соседи 0–14 — это ##; разноуровневые заголовки ломают и счётчик разделов" % _dlev.group(1))
        if _dsub < 5:
            errors.append(f"подразделов 15a–15e найдено {_dsub} из 5 — один съехал с уровня или переименован")

    # (2d) арифметика собственного отчёта: число прогонов-мутаций обязано совпадать с суммой групп,
    # а сумма — с тем, что написано в человекочитаемой строке. Иначе «41» и «13+3+5…» расходятся молча,
    # ровно как расходятся любые два места, где одно число записано дважды.
    _mg = (reg.get("integrityGate", {}).get("rules") or {}).get("mutationGroups")
    if _mg:
        _sum = sum(int(x.get("count", 0)) for x in _mg)
        _tot = int(((reg.get("integrityGate", {}).get("rules") or {}).get("mutationTotal") or -1))
        _strn = str((reg.get("integrityGate", {}).get("rules") or {}).get("mutationScore20261022") or "")
        _lead = re.match(r"\s*(\d+)", _strn)
        if _sum != _tot:
            errors.append(
                f"integrityGate.rules.mutationTotal = {_tot}, а сумма групп — {_sum}: разложение и итог — это "
                "одно число в двух местах, и они обязаны сойтись"
            )
        if not _lead or int(_lead.group(1)) != _sum:
            errors.append(
                f"в строке mutationScore20261022Leading = {(_lead.group(1) if _lead else None)!r}, а группы дают {_sum} — "
                "цифра, которую цитируют в отчёте, обязана быть тем же числом, что и разложение под ней"
            )
        _blank = [i for i, x in enumerate(_mg) if not str(x.get("label") or "").strip() or int(x.get("count", 0)) <= 0]
        if _blank:
            errors.append(f"группы мутаций {_blank} без подписи или с нулевым счётом — пустая группа прячет расхождение")

    # (2c) живые счётчики: число, записанное в двух местах, обязано разойтись — поэтому то, что можно
    # переснять этим же обходом, переснимается, а не цитируется
    _live = ((reg.get("reproducibility20261022") or {}).get("countsLive") or {})
    _audit = reg.get("branchTopologyAudit20261022") or {}
    _expect = {
        "ключейРеестра": len(reg),
        "правилГейта": len(((reg.get("integrityGate") or {}).get("rules") or {}).get("list") or []),
        "shaВсверкеВремен": len(_audit.get("commitTimeChecks") or {}),
        "строкВАудитеТопологии": len(_audit.get("rows") or []),
        "записейЛеджера": LIVE["записейЛеджера"],
        "строкСводки": LIVE["строкСводки"],
        "строкРеестраМассы": len(measure_mass_registry()[0]),
        "очередейДобычиМассы": len(measure_mass_registry()[1]),
    }
    if _live:
        for _k, _v in sorted(_expect.items()):
            if _k in _live and int(_live[_k]) != _v:
                errors.append(
                    f"reproducibility20261022.countsLive[{_k!r}] = {_live[_k]!r}, а обход видит {_v} — живой "
                    "счётчик не имеет права быть цитатой: или число переснято, или блок надо убирать"
                )
        _missing = sorted(set(_expect) - set(_live))
        if _missing:
            errors.append(
                f"countsLive не содержит {_missing} — блок закрыт: в нём объявлены ровно проверяемые числа, "
                "иначе «число есть» снова означает «кто-то когда-то посчитал»"
            )
        _extra = sorted(set(map(str, _live)) - set(_expect) - {"measuredAt", "method", "recheckCommand", "why",
                                                                "removedFigures"})
        if _extra:
            errors.append(
                f"countsLive содержит {_extra}: в блоке живут только числа, которые переснимает этот же обход; "
                "остальное — в тех записях, где у числа есть источник"
            )

# ------------------------------------------------- mixed script, out of scope --
# Число чужих вхождений, записанное в реестре как аргумент «я туда не вступала», обязано пересниматься: иначе
# «они больны» превращается в то, что я только что запретила себе — в цифру, которая пережила собственных хозяев.
_out = (reg.get("integrityGate", {}).get("mixedScriptCheck") or {}).get("outOfScope") or {}
if _out:
    _files_seen = set()
    _occ_seen = 0
    for _md in sorted(CORPUS.rglob("*.md")):
        if _md.parent == CORPUS:
            continue  # периметр, где я имею право исправлять, проверен выше и обязан быть нулевым
        _text = read(_md)
        for _line in _text.split("\n"):
            if EXEMPT in _line:
                continue
            _occ_seen += len(mixed_words(_line))
            if mixed_words(_line):
                _files_seen.add(str(_md.relative_to(ROOT)))
    if int(_out.get("occurrences", -1)) != _occ_seen:
        errors.append(
            f"mixedScriptCheck.outOfScope.occurrences = {_out.get('occurrences')!r}, а обход видит {_occ_seen} — "
            "чужой периметр я не лечу, но считать его обязана: «там 12» без пересъёмки значит «я помню, что было 12»"
        )
    if int(_out.get("files", -1)) != len(_files_seen):
        errors.append(
            f"mixedScriptCheck.outOfScope.files = {_out.get('files')!r}, а обход нашёл {len(_files_seen)} файлов "
            f"({sorted(_files_seen)[:3]}…)"
        )

# --------------------------------------------- JSON-листья: правило 19 (23.10) --
# До сего круга смешанное письмо искалось только на *.md: из-за этого ни один реестр
# (включая собственный) не проверялся — на JSON проверка была пуста по построению,
# потому что кавычки-цитаты вырезают всё содержимое строки целиком. Теперь класс
# определяется формой значения: проверяется каждый строковый лист дерева, а не файл
# по расширению. Своё -> errors; чужие под-реестры -> notes (правило 17).
QUOTED_JSON = re.compile(r"\u00ab[^\u00bb]*\u00bb")
def _leaf_hits(obj):
    out = []
    def walk(o, path):
        if isinstance(o, dict):
            for k, v in o.items():
                walk(v, path + "." + str(k))
        elif isinstance(o, list):
            for i, v in enumerate(o):
                walk(v, "%s[%d]" % (path, i))
        elif isinstance(o, str):
            for w in mixed_words(QUOTED_JSON.sub(" ", o)):
                out.append((path, w))
    walk(obj, "")
    return out

_own_json_hits = []
_sub_json_hits = []
_json_files_scanned = 0
for _jp in sorted(CORPUS.rglob("*.json")):
    try:
        _jd = json.loads(read(_jp))
    except Exception:
        continue  # нечитаемый JSON уже ловится другими проверками, здесь не дублируем
    _json_files_scanned += 1
    _hits = _leaf_hits(_jd)
    if _jp == REG:
        _own_json_hits.extend(_hits)
    elif _hits:
        _sub_json_hits.extend((str(_jp.relative_to(ROOT)) + p, w) for p, w in _hits)
if _own_json_hits:
    errors.append(
        f"правило 19: в собственном реестре {len(_own_json_hits)} смешанных написаний в строковых "
        f"листьях ({[w for _p, w in _own_json_hits][:4]}) — цитата должна стоять в «ёлочках», а употребление обязано быть русским"
    )
_jrec = (msc := {}).get("jsonLeafScan") if False else ((reg.get("integrityGate", {}).get("mixedScriptCheck") or {}).get("jsonLeafScan") or {})
if _jrec:
    if int(_jrec.get("ownOccurrences", -1)) != len(_own_json_hits):
        errors.append(
            f"jsonLeafScan.ownOccurrences = {_jrec.get('ownOccurrences')!r}, а обход видит {len(_own_json_hits)}: "
            "собственное число обязано совпадать с обходом"
        )
    if int(_jrec.get("scannedFiles", -1)) != _json_files_scanned:
        errors.append(
            f"jsonLeafScan.scannedFiles = {_jrec.get('scannedFiles')!r}, а обход видит {_json_files_scanned} JSON-файлов "
            "в ИСКУПЛЕНИЕ/** — раскладка обязана сходиться со съёмом"
        )
    if int(_jrec.get("foreignOccurrences", -1)) != len(_sub_json_hits):
        notes.append(
            f"jsonLeafScan.foreignOccurrences записано {_jrec.get('foreignOccurrences')!r}, обход видит {len(_sub_json_hits)} "
            f"({sorted({p for p, _w in _sub_json_hits})[:3]}) — чужой периметр считается, но не блокирует прогон"
        )


# ------------------------------ git-ссылки реестра: правило 20 (23.10.2026) --
# Число, за которым стоит команда вида «git show <sha>:…», живо ровно столько,
# сколько жив объект. Squash-мерж и удаление ветки убивают объект, но не убивают
# запись: мёртвая ссылка переживает себя как обещание, которое никто не проверил.
# Сегодня я насчитала «99 мёртвых sha» на shallow-клоне, где не читались и живые:
# поэтому класс различий — не «объект пропал», а «объект недостижим ИЗ ЭТОЙ СРЕДЫ»,
# и в неподходящей среде проверка обязана молчать осознанно, а не выдавать ноль.
SHA_TOKEN = re.compile(r"\b[0-9a-f]{7,40}\b")
_MARK = "verifiability20261023"


def _sha_tokens(obj):
    """sha-подобные токены в СТРОКОВЫХ ЗНАЧЕНИЯХ дерева (ключи не считаем: recordCommit
    заведомо ключён мёртвыми sha, и это его назначение)."""
    out = {}

    def walk(o, p):
        if isinstance(o, dict):
            for k, v in o.items():
                walk(v, p + "." + str(k))
        elif isinstance(o, list):
            for i, v in enumerate(o):
                walk(v, "%s[%d]" % (p, i))
        elif isinstance(o, str):
            for m in SHA_TOKEN.findall(o):
                if len(m) not in (7, 8, 40) or re.fullmatch(r"[0-9]+", m):
                    continue
                out.setdefault(m, []).append(p)

    walk(obj, "")
    return out


def _unreachable(tokens):
    """set токенов, НЕдостижимых из main; None = среда не годна (shallow или нет origin/main).

    Определение обязано быть относительным, а не «объект есть в этом клоне»: в моём клоне
    16 токенов не разрешились из-за амбигуити (лишние объекты удалённых веток дали общий
    префикс), зато разрешились 16 таких, которых в main нет вовсе. На чистом клоне CI те же
    числа дали byBlock 52 против моих 68 — то есть проверка меряла свойство клона. Достижимость
    из origin/main совпадает в обоих клонах до символа (54 живых, расхождение пустое), поэтому
    она и выбрана как канон."""
    try:
        import subprocess as _sp
        if _sp.run(["git", "rev-parse", "--is-shallow-repository"], cwd=ROOT,
                   capture_output=True, text=True).stdout.strip() == "true":
            return None
        base = _sp.run(["git", "rev-parse", "--verify", "-q", "origin/main"], cwd=ROOT,
                       capture_output=True, text=True).stdout.strip()
        if not base:  # например, прогон на detached-дереве без remote-tracking: не выдумываем результат
            return None
        objs = _sp.run(["git", "rev-list", "--objects", base], cwd=ROOT, capture_output=True, text=True).stdout
    except Exception:  # noqa: BLE001 - нет git'а: не подменяем измерение нулём
        return None
    full = sorted({line.split(" ")[0] for line in objs.split("\n") if line})
    import bisect

    def reachable(tok):
        k = bisect.bisect_left(full, tok)
        return k < len(full) and full[k].startswith(tok)

    return {t for t in tokens if not reachable(t)}


_audit = ((reg.get("integrityGate") or {}).get("shaCitationAudit20261023") or {})
_own_tokens = _sha_tokens(reg)
_own_dead = _unreachable(_own_tokens)
if _own_dead is None:
    notes.append(
        "правило 20: среда shallow или git недоступен — аудит sha-ссылок не исполняется. "
        "Это не «ссылок нет»: на таком клоне я сегодня прочитала 99 мёртвых вместо 46 настоящих"
    )
else:
    # (1) каждая мёртвая ссылка обязана иметь живой пересъём через запись, и запись обязана её содержать
    _rec = _audit.get("recordCommit") or {}
    _noRec, _badRec = [], []
    for tok in sorted(_own_dead):
        rc = _rec.get(tok)
        if not rc:
            _noRec.append(tok)
            continue
        try:
            import subprocess as _sp
            blob = _sp.run(["git", "show", "%s:%s" % (rc, REG.relative_to(ROOT))], cwd=ROOT,
                           capture_output=True, text=True)
            if blob.returncode != 0 or tok not in blob.stdout:
                _badRec.append(tok)
        except Exception:  # noqa: BLE001
            _badRec.append(tok)
    if _noRec:
        errors.append(
            f"правило 20: {len(_noRec)} sha-ссылок реестра ведут на недостижимый объект и не имеют "
            f"пересъёма через запись ({_noRec[:4]}…) — «значение по git show» без живого git show это вера"
        )
    if _badRec:
        errors.append(
            f"правило 20: {len(_badRec)} записей recordCommit не содержат свой токен ({_badRec[:3]}…) — "
            "команда пересъёма записана, но не исполнена: проверять надо вывод, а наличие строки в реестре"
        )
    # (2) блок с мёртвой ссылкой обязан объявить историчность
    _fields_dead = {}
    for tok in _own_dead:
        for p in _own_tokens[tok]:
            _fields_dead[p.lstrip(".").split(".")[0].split("[")[0]] = _fields_dead.get(
                p.lstrip(".").split(".")[0].split("[")[0], 0) + 1
    _untagged = []
    for top in _fields_dead:
        blk = reg.get(top)
        marked = isinstance(blk, dict) and _MARK in blk
        if isinstance(blk, list) and not marked:
            marked = all(_MARK in x for x in blk if isinstance(x, dict) and _sha_tokens(x) and
                         any(t in _own_dead for t in _sha_tokens(x))) and any(isinstance(x, dict) and _MARK in x for x in blk)
        if not marked:
            _untagged.append(top)
    if _untagged:
        errors.append(
            f"правило 20: блоки с недостижимыми git-ссылками без поля {_MARK}: {sorted(_untagged)} — "
            "историчность надо объявить словами, иначе число притворяется проверяемым"
        )
    # (3) форма поля: обещание «время коммита по команде» без статуса при мёртвом объекте
    _prom = []

    def _scan_promises(o, p):
        if isinstance(o, dict):
            dead_here = any(t in _own_dead for t in _sha_tokens(o))
            for k, v in o.items():
                if dead_here and re.search(r"TimeCommand$", str(k)) and not any(
                        re.search(r"TimeStatus$|TimeUnverifiable$", str(k2)) for k2 in o):
                    _prom.append(p + "." + str(k))
                _scan_promises(v, p + "." + str(k))
        elif isinstance(o, list):
            for i, v in enumerate(o):
                _scan_promises(v, "%s[%d]" % (p, i))

    _scan_promises({k: v for k, v in reg.items() if k != "integrityGate"}, "")
    if _prom:
        errors.append(
            f"правило 20: {len(_prom)} полей вида *TimeCommand ссылаются на мёртвый объект и не имеют "
            f"*TimeStatus ({_prom[:2]}…) — команда, которая ничего не вернёт, обязана это сказать"
        )
    # (4) собственные числа аудита обязаны совпадать с обходом
    if _audit:
        _live_fields = sum(1 for tok in _own_dead for _ in _own_tokens[tok])
        _want = {"uniqueShaTokens": len(_own_tokens), "reachableTokens": len(_own_tokens) - len(_own_dead),
                 "unreachableTokens": len(_own_dead), "fieldsWithDeadLinks": _live_fields, "byBlock": _fields_dead}
        _drift = {k: (_audit.get(k), v) for k, v in _want.items() if _audit.get(k) != v}
        _bb_rec = _audit.get("byBlock") or {}
        if sum(int(v) for v in _bb_rec.values()) != int(_audit.get("fieldsWithDeadLinks", -1)):
            errors.append(
                "shaCitationAudit20261023: раскладка byBlock даёт %d, а fieldsWithDeadLinks = %s — таблица, "
                "которая не сходится с собственной суммой, не имеет права называться замером"
                % (sum(int(v) for v in _bb_rec.values()), _audit.get("fieldsWithDeadLinks"))
            )

        if _drift:
            errors.append(
                "shaCitationAudit20261023 разошёлся с обходом: "
                + ", ".join(f"{k}: записано {a!r}, видим {b!r}" for k, (a, b) in sorted(_drift.items()))
                + " — аудит, который не сверяется с тем, что порождает заметки, это заметка про аудит"
            )
    # (5) чужие под-реестры: считать, но не блокировать (правило 17)
    _foreign = {}
    for _label, _path in _registries:
        if _path == REG:
            continue
        try:
            _fd = json.loads(read(_path))
        except Exception:  # noqa: BLE001
            continue
        _ft = _sha_tokens(_fd)
        _fd_dead = _unreachable(_ft)
        if _fd_dead:
            _foreign[_label] = len(_fd_dead)
    if _foreign:
        notes.append(
            f"правило 20: в чужих под-реестрах недостижимых sha-ссылок по ланам {_foreign} — чужие прогоны "
            "моими числами не блокируются; исправлять их вправе только владелец лана"
        )


# ---------------------------------------------------- commit message hygiene --
# Тот же класс, что и в файлах, я сегодня трижды занесла в сообщения коммитов (кириллическая строка с латинской
# буквой и дважды — иероглифы, затесавшиеся там, где я сжимала два придаточных). Историю PR ради этого не
# переписывают, поэтому требование только к tip'у: его и так проверяет CI на каждом push, а следующая правка
# обязана быть чище предыдущей.
try:
    import subprocess as _sp
    _msg = _sp.run(["git", "log", "-1", "--format=%B"], cwd=ROOT, capture_output=True, text=True).stdout
    _parents = _sp.run(["git", "log", "-1", "--format=%P"], cwd=ROOT, capture_output=True, text=True).stdout.split()
    _subject = _msg.split("\n", 1)[0]
except Exception:  # noqa: BLE001 - git может быть недоступен (не репозиторий): тогда проверка честно молчит
    _msg, _parents, _subject = "", [], ""
# Сообщение merge/squash, которое сгенерировал GitHub из заголовка и тела PR, автору не принадлежит: там
# окажется любой цитируемый дефект, который я сама же и починила в тексте, и ни один из 44 подзаголовков
# истории я не вправе переписывать. Требование к тому, кто пишет коммит, а не к тому, кто его мержит.
_generated = len(_parents) > 1 or _subject.startswith("Merge branch") or bool(re.match(r"^.+\(#[0-9]+\)$", _subject))
if _msg and not _generated:
    _cjk = sorted(set(re.findall(r"[\u3040-\u30ff\u4e00-\u9fff]+", _msg)))
    if _cjk:
        errors.append(
            "сообщение последнего коммита содержит не-кириллическое восточное начертание "
            f"{_cjk[:4]} — правь текст через git commit --amend -F <файл> (флаг -m с двойными кавычками "
            "и так съедает backtick-цитаты)"
        )
    _mixed = sorted(set(mixed_words(_msg)))
    if _mixed:
        errors.append(
            f"сообщение последнего коммита содержит {len(_mixed)} слов смешанного письма: {_mixed[:5]} — "
            "в таком виде сообщение не ищется по-русски (git log --grep не найдёт)"
        )

# ---- правило 22 (23.10.2026): периметр смешанного письма — измерение, а не воспоминание
_repo_audit = (reg.get("integrityGate", {}).get("mixedScriptCheck") or {}).get("repoWideAudit20261023") or {}
if not _repo_audit:
    errors.append("реестр: в integrityGate.mixedScriptCheck нет блока repoWideAudit20261023 — остаток чужих ланов обязан быть проверяемым инвентарём (файлы, вхождения, классы, причины отказа от правки), а не числом из памяти или из текста PR")
else:
    import subprocess as _sp22
    if not _repo_audit.get("recheckCommand"):
        errors.append("ПРАВИЛО 22: у repoWideAudit20261023 нет recheckCommand — блок, который никто не может переснять, это ровно та болезнь, которую мы тут лечим")
    for _k22 in ("files", "occurrences", "byFile", "classes", "revokedDueToForeignHashPin",
                 "fixedByThisRound", "fixedMethod", "measuredAt", "method", "why",
                 "strictnessSplit", "neighbourGatesRun"):
        if _k22 not in _repo_audit:
            errors.append(f"ПРАВИЛО 22: в repoWideAudit20261023 нет поля «{_k22}»")
    _d22 = {x["path"]: x["count"] for x in _repo_audit.get("byFile", [])}
    if len(_d22) != _repo_audit.get("files") or sum(_d22.values()) != _repo_audit.get("occurrences"):
        errors.append(f"ПРАВИЛО 22: блок не сходится сам с собой: пофайловая раскладка даёт {len(_d22)} файлов / "
                      f"{sum(_d22.values())} вхождений, заявлено {_repo_audit.get('files')} / {_repo_audit.get('occurrences')}")
    _csum22 = sum(_repo_audit.get("classes", {}).values())
    if _csum22 != _repo_audit.get("occurrences"):
        errors.append(f"ПРАВИЛО 22: классы остатка складываются в {_csum22}, а вхождений {_repo_audit.get('occurrences')} — "
                      "инвентарь обязан объяснять каждое вхождение, а не большинство")
    for _e22 in _repo_audit.get("revokedDueToForeignHashPin", []):
        if not _e22.get("path") or not _e22.get("pinnedBy"):
            errors.append("ПРАВИЛО 22: запись revokedDueToForeignHashPin без path или без pinnedBy — «сюда нельзя» должно быть чем-то проверяемо")
            continue
        for _pin in _e22["pinnedBy"]:
            if not (ROOT / _pin).is_file():
                errors.append(f"ПРАВИЛО 22: заявленный пин {_pin} (файл {_e22['path']}) не найден в репозитории — "
                              "либо чужой лан снял пин и правку надо вернуться и сделать, либо ссылка в инвентаре выдумана")
    _seen22: dict[str, int] = {}
    _tracked22 = [x.decode("utf-8") for x in _sp22.run(["git", "ls-files", "-z"], capture_output=True).stdout.split(b"\0") if x]
    for _rel in _tracked22:
        if _rel.startswith("ИСКУПЛЕНИЕ/") or not _rel.endswith((".md", ".json")):
            continue
        try:
            _t22 = (ROOT / _rel).read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        _n22 = sum(len(mixed_words(_l)) for _l in _t22.split("\n") if EXEMPT not in _l)
        if _n22:
            _seen22[_rel] = _n22
    if _d22 != _seen22:
        _gone22 = sorted(set(_d22) - set(_seen22))
        _new22 = sorted(set(_seen22) - set(_d22))
        _drift22 = sorted(k for k in set(_d22) & set(_seen22) if _d22[k] != _seen22[k])
        notes.append("ПРАВИЛО 22: инвентарь чужого периметра разошёлся с деревом — обход даёт %d файлов / %d вхождений, "
                     "заявлено %d / %d; вычистили: %s; появилось: %s; сменилось число: %s. Для чужих файлов это заметка, "
                     "а не ошибка: блокировать чужой прогон из-за своего счётчика нельзя (правило 17) — переснимает "
                     "владелец декларации, команда в recheckCommand"
                     % (len(_seen22), sum(_seen22.values()), _repo_audit.get("files"), _repo_audit.get("occurrences"),
                        ", ".join(_gone22[:3]) or "—", ", ".join(_new22[:3]) or "—", ", ".join(_drift22[:3]) or "—"))
    _adj22 = []
    for _md22 in sorted(set(DOCS.rglob("*.md"))):
        try:
            _t22 = _md22.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for _no22, _l in enumerate(_t22.split("\n"), start=1):
            if EXEMPT in _l:
                continue
            for _w22 in mixed_words(_l):
                _adj22.append("%s:%d %s" % (_md22.name, _no22, _w22))
    if _adj22:
        errors.append("ПРАВИЛО 22: в docs/research/atonement/** найдено смешанное письмо (%d: %s) — смежный лан корпуса "
                      "входит в периметр как ошибка, потому что корпус и он болеют одним дефектом; чинится тем же "
                      "порядком: кандидат обязан быть аттестован ланом (см. fixedMethod в инвентаре)"
                      % (len(_adj22), ", ".join(_adj22[:5])))

# ---- правило 23 (23.10.2026): масса носителей позиции — проверяемый реестр, а не список имён
_mrows, _mq, _mrefs, _mexists = measure_mass_registry()
_ma = reg.get("fourPointMassRegistry20261023") or {}
if not _ma:
    errors.append("реестр: нет блока fourPointMassRegistry20261023 — «мы собрали всю массу четырёхпунктников» обязано быть чем-то переснимаемым (число строк, классы достоверности, очередь добычи), иначе это снова слово в тексте PR")
if not _mexists:
    errors.append(f"ПРАВИЛО 23: заявленный реестр массы не найден — {MASS_FILE.relative_to(ROOT)}; блок в JSON без файла есть обещание, а не данные")
else:
    if not _ma:
        pass
    else:
        for _k in ("entries", "perClass", "queueLength", "shareA1Percent", "measuredAt", "method",
                   "recheckCommand", "perimeter", "classesVocabulary", "why", "foundThisRound", "laneDefectRecorded"):
            if _k not in _ma:
                errors.append(f"ПРАВИЛО 23: в fourPointMassRegistry20261023 нет поля «{_k}»")
        if not _ma.get("recheckCommand"):
            errors.append("ПРАВИЛО 23: у реестра массы нет recheckCommand — число, которое нельзя переснять, не имеет права называться измерением")
        _mdecl = {str(x): int(y) for x, y in (_ma.get("perClass") or {}).items()}
        _meas = {c: sum(1 for n, (k, l) in _mrows.items() if k == c) for c in MASS_CLS}
        if len(_mrows) != _ma.get("entries"):
            errors.append(f"ПРАВИЛО 23: заявлено {_ma.get('entries')} строк реестра, обход видит {len(_mrows)} — переснять: {MASS_FILE.name}")
        if _mdecl != _meas:
            errors.append(f"ПРАВИЛО 23: классы достоверности разошлись: заявлено {_mdecl}, обход видит {_meas}")
        if sum(_mdecl.values()) != _ma.get("entries"):
            errors.append("ПРАВИЛО 23: сумма классов не равна числу строк — реестр обязан объяснять каждую строку, а не большинство")
        if _ma.get("queueLength") != len(_mq):
            errors.append(f"ПРАВИЛО 23: очередь добычи: заявлено {_ma.get('queueLength')} адресов, в файле {len(_mq)}")
        if not _ma.get("shareA1Percent") or int(_ma.get("shareA1Percent")) != round(100 * _meas["A1"] / max(1, len(_mrows))):
            errors.append(f"ПРАВИЛО 23: доля прочитанного по первичному изданию: заявлено {int(_ma.get('shareA1Percent') or 0)}%, "
                          f"обход считает {round(100 * _meas['A1'] / max(1, len(_mrows)))}% — «масса собрана» не имеет права звучать громче, чем это число")
        _ids = sorted(_mrows)
        if _ids != list(range(1, len(_ids) + 1)):
            gaps = sorted(set(range(1, max(_ids) + 1)) - set(_ids))
            dups = [n for n in _ids if _ids.count(n) > 1]
            errors.append(f"ПРАВИЛО 23: нумерация строк реестра не непрерывна (пропуски {gaps[:5]}, повторы {dups[:5]}) — "
                          "номер строки это адрес, по которому ходит очередь; дырявая нумерация позволяет «снять» улику, вырезав строку")
        _nocls = [n for n, (k, l) in _mrows.items() if k not in MASS_CLS]
        if _nocls:
            errors.append(f"ПРАВИЛО 23: строки без класса достоверности (или с вне словаря): FP-{_nocls[0]:02d}… — всего {len(_nocls)}; "
                          f"словарь закрыт: {', '.join(MASS_CLS)}")
        _cset = {n for n, (k, l) in _mrows.items() if k == "C"}
        if _cset != _mq:
            errors.append(f"ПРАВИЛО 23: строки `C` и очередь разошлись: только в C {sorted(_cset - _mq)[:5]}, только в очереди {sorted(_mq - _cset)[:5]} — "
                          "каждая «надо добыть» обязана иметь адресата, иначе «масса» собирается вычёркиванием неудобных строк")
        _noloc = [n for n, (k, l) in _mrows.items() if k == "A1" and not MASS_LOC.search(l)]
        if _noloc:
            errors.append(f"ПРАВИЛО 23: {len(_noloc)} строк класса `A1` без локатора (первая — FP-{_noloc[0]:02d}) — «сверено по изданию» без страницы/колонки/парграфа "
                          "е ровно тот дефект, из-за которого весь этот корпус и затеян")
        # CJK-скан реестра и корпуса: прилипшие азиатские глифы — фирменный артефакт «написано по памяти»
        _cjk_lane = cjk_hits(sorted(DOCS.glob("*.md")))
        _cjk_root = cjk_hits(sorted(CORPUS.glob("*.md")))
        _cjk_sub = cjk_hits(sorted(p for d in ("ot", "nt", "synthesis", "fathers") for p in (CORPUS / d).rglob("*.md")))
        _ncjk = sum(len(v) for v in _cjk_lane.values()) + sum(len(v) for v in _cjk_root.values())
        _cjk_decl = _ma.get("cjkScan20261023") or {}
        for _k in ("scope", "laneOccurrences", "rootOccurrences", "subLaneOccurrences", "recheckCommand", "checkedAt"):
            if _k not in _cjk_decl:
                errors.append(f"ПРАВИЛО 23: в fourPointMassRegistry20261023.cjkScan20261023 нет поля «{_k}»")
        if (_cjk_decl.get("laneOccurrences") if _cjk_decl.get("laneOccurrences") is not None else -1) != sum(len(v) for v in _cjk_lane.values()):
            errors.append(f"ПРАВИЛО 23: CJK в docs/research/atonement: заявлено {_cjk_decl.get('laneOccurrences')}, "
                          f"обход видит {sum(len(v) for v in _cjk_lane.values())} ({list(_cjk_lane)[:3]})")
        if (_cjk_decl.get("rootOccurrences") if _cjk_decl.get("rootOccurrences") is not None else -1) != sum(len(v) for v in _cjk_root.values()):
            errors.append(f"ПРАВИЛО 23: CJK в корневых файлах корпуса: заявлено {_cjk_decl.get('rootOccurrences')}, "
                          f"обход видит {sum(len(v) for v in _cjk_root.values())} ({list(_cjk_root)[:3]})")
        if _ncjk:
            _where = "; ".join(f"{k}:{v[0][0]} {v[0][1]!r}" for k, v in list(_cjk_lane.items()) + list(_cjk_root.items())[:3])
            errors.append(f"ПРАВИЛО 23: {_ncjk} CJK-глифов вне цитат в реестре/корпусе ({_where}) — это не иероглифика, "
                          "это прилипшее при наборе по памяти: чинить букву, а не помечать исключение")
        if (_cjk_decl.get("subLaneOccurrences") if _cjk_decl.get("subLaneOccurrences") is not None else -1) != sum(len(v) for v in _cjk_sub.values()):
            notes.append(f"ПРАВИЛО 23: CJK в под-ланах корпуса: обход видит {sum(len(v) for v in _cjk_sub.values())}, "
                         f"заявлено {_cjk_decl.get('subLaneOccurrences')} — чужой прогон моим числом не блокируется")
        _badref = sorted(r for r in _mrefs if r.startswith(("ИСКУПЛЕНИЕ/", "docs/")) and not (ROOT / r).exists()
                         or not r.startswith(("ИСКУПЛЕНИЕ/", "docs/")) and not list(DOCS.glob(r + "*")) and not list(CORPUS.glob(r + "*")))
        if _badref:
            errors.append(f"ПРАВИЛО 23: {len(_badref)} ссылок реестра ведут на несуществующий файл лана ({_badref[:5]}) — ссылка «см. 22_» обязана находиться")

# ---- правило 24 (23.10.2026): «N вхождений» обязано быть переснятым в обеих азбуках и по названному файлу
# Повод конкретный: круг 16 записал в README лана, что разбора Буньяна в 15_patristic_and_reformation_misattributions.md
# нет («grep -i bunyan»: 0 вхождений). Обход был сделан по файлу другого лана (ИСКУПЛЕНИЕ/15_ — там и правда 0),
# а назван в правке был docs/research/atonement/15_, где «Буньян» встречается 17 раз. Латинский шаблон по
# кириллическому тексту не находит ничего, и «проверено обходом» становится самым опасным видом утверждения:
# измерено — но не по тому предмету. Отсюда три требования к строке, которая считает вхождения: оба алфавита
# названы, путь к файлу взят в обратные кавычки и стоит ближе всего к числу, и каждое число переснимается здесь же.
_MINE24 = [CORPUS / "00_README_AND_NAVIGATION.md", CORPUS / "05_SOURCE_REGISTRY_AND_ACQUISITION_QUEUE.md",
           CORPUS / "17_RECONCILIATION_WITH_CANONICAL_SPINE_2026-10-15.md",
           DOCS / "README.md", DOCS / "35_four_point_authors_mass_registry.md"]
_PC24 = re.compile("[«\"]([A-Za-z\u0410-\u042F\u0430-\u044F\u0401\u0451][A-Za-z\u0410-\u042F\u0430-\u044F\u0401\u0451-]{2,})[»\"][^0-9\n]{0,24}?(\\d+)\\s+вхождений")
_CYR24 = re.compile("[\u0410-\u042F\u0430-\u044F\u0401\u0451]")
_PATH24 = re.compile("`([^`]+\\.md)`")
_CNT24 = re.compile(r"\d+\s+вхождений")  # претензия обязана быть числом: «много вхождений» — не измерение
_MTH24 = re.compile(r"grep|греп|wc -l|обход|проверено|сверено", re.I)  # …и способом, названным в той же строке


def _occ24(text, pattern):
    return len(re.findall(re.escape(pattern), text, re.IGNORECASE))


def _file24(ref):
    for cand in ((ROOT / ref), (DOCS / Path(ref).name), (CORPUS / Path(ref).name)):
        if cand.exists():
            return cand
    return None


def _units24(text):
    """Единица сверки — смысловой блок, а не физическая строка: абзац переносится по ширине, и
    иначе «0 вхождений» осталось бы без названного файла только потому, что путь уехал на следующую
    строку. Табличные строки, пункты списков и заголовки остаются единицами сами по себе."""
    out, cur, cur_no = [], [], 1
    for n, ln in enumerate(text.split("\n"), start=1):
        if not ln.strip():
            if cur:
                out.append((cur_no, " ".join(cur)))
                cur = []
            continue
        if cur and re.match(r"^(\||-\s|\d+\.\s|#{1,6}\s)", ln):
            out.append((cur_no, " ".join(cur)))
            cur = []
        if not cur:
            cur_no = n
        cur.append(ln)
    if cur:
        out.append((cur_no, " ".join(cur)))
    return out


_claims24, _bad24, _recheck24 = 0, [], 0
for _f24 in _MINE24:
    if not _f24.exists():
        continue
    _t24 = _f24.read_text(encoding="utf-8", errors="replace")
    _units24r = _units24(_t24)
    for _no24, _l in _units24r:
        if (EXEMPT in _l or not _CNT24.search(_l) or not _MTH24.search(_l)
                or not _PATH24.search(_l)):
            continue
        _claims24 += 1
        _hits24 = list(_PC24.finditer(_l))
        _cyr24 = [m for m in _hits24 if _CYR24.search(m.group(1))]
        _lat24 = [m for m in _hits24 if not _CYR24.search(m.group(1))]
        _zero24 = [m for m in _hits24 if int(m.group(2)) == 0]
        if _zero24 and not (_cyr24 and _lat24):
            _bad24.append("%s:%d — «0 вхождений» назван одним шаблоном (кириллических %d, латинских %d из %d чисел); "
                          "имя в русском файле пишется кириллицей, и греп по латинице даёт «0» как артефакт азбуки, "
                          "а не как отсутствие" % (_f24.name, _no24, len(_cyr24), len(_lat24), len(_hits24)))
            continue
        if not _hits24:
            _bad24.append("%s:%d — блок утверждает число вхождений в названном файле, но ни одно из них не "
                          "оформлено как «шаблон» → N вхождений: переснять нечем" % (_f24.name, _no24))
            continue
        _paths24 = [(m.start(), m.group(1)) for m in _PATH24.finditer(_l)]
        _cache24, _miss24 = {}, []
        for m in _hits24:
            _near = None
            for _pos, _pp in _paths24:
                # путь обязан стоять в той же строке и быть ближайшим: форма претензии —
                # «X» → N вхождений по `файл.md`; если в строке два файла, к числу примыкает тот,
                # что ближе, и спорить с этим нельзя, иначе число припишется чужому файлу
                _d = abs(_pos - m.start())
                if _near is None or _d < _near[0]:
                    _near = (_d, _pp)
            if _near is None:
                _miss24.append("число «%s» заявлено без пути к файлу в обратных кавычках" % m.group(1))
                continue
            if _near[1] not in _cache24:
                _fp = _file24(_near[1])
                _cache24[_near[1]] = (_fp, _fp.read_text(encoding="utf-8", errors="replace") if _fp else None)
            _fp, _txt24 = _cache24[_near[1]]
            if _txt24 is None:
                _miss24.append("файл %s не найден" % _near[1])
                continue
            _recheck24 += 1
            _got24 = _occ24(_txt24, m.group(1))
            if _got24 != int(m.group(2)):
                _bad24.append("%s:%d — по %s шаблон «%s»: заявлено %s, обход видит %d"
                              % (_f24.name, _no24, _fp.name, m.group(1), m.group(2), _got24))
        if _miss24:
            _bad24.append("%s:%d — %s, значит «N вхождений» ничем не подтверждено"
                          % (_f24.name, _no24, "; ".join(_miss24[:2])))
if _bad24:
    errors.append("ПРАВИЛО 24: %d строки-претензии не выдерживают пересъёма (%s) — «мы проверили» обязано быть "
                  "проверяемым в обеих азбуках и по названному файлу" % (len(_bad24), "; ".join(_bad24[:4])))
_other24 = 0
_own24 = set(_MINE24)
for _f24 in sorted(set(list(CORPUS.rglob("*.md")) + list(DOCS.rglob("*.md"))) - _own24):
    try:
        _t24 = _f24.read_text(encoding="utf-8", errors="replace")
    except OSError:
        continue
    _other24 += sum(1 for _l in _t24.split("\n") if _CNT24.search(_l) and _MTH24.search(_l))
_decl24 = reg.get("grepBilingualAudit20261023") or {}
if _decl24:
    for _k in ("scope", "claimsChecked", "bilingualOk", "recheckedOccurrences", "otherLaneClaims",
               "recheckCommand", "checkedAt"):
        if _k not in _decl24:
            errors.append("ПРАВИЛО 24: в grepBilingualAudit20261023 нет поля «%s»" % _k)
    if int(_decl24.get("claimsChecked") or -1) != _claims24:
        errors.append("ПРАВИЛО 24: заявлено %s строки-претензии, обход видит %d"
                      % (_decl24.get("claimsChecked"), _claims24))
    if int(_decl24.get("bilingualOk") or -1) != _claims24 - len(_bad24):
        errors.append("ПРАВИЛО 24: двуалфавитных строк заявлено %s, обход видит %d"
                      % (_decl24.get("bilingualOk"), _claims24 - len(_bad24)))
    if int(_decl24.get("recheckedOccurrences") or -1) != _recheck24:
        errors.append("ПРАВИЛО 24: переснятых чисел заявлено %s, обход видит %d — правило, которое ничего "
                      "не переснимает, это не проверка, а формат"
                      % (_decl24.get("recheckedOccurrences"), _recheck24))
    if int(_decl24.get("otherLaneClaims") or -1) != _other24:
        notes.append("ПРАВИЛО 24: в чужих ланах %d строк того же вида (заявлено %s) — чужой прогон моим числом "
                     "не блокируется" % (_other24, _decl24.get("otherLaneClaims")))
else:
    notes.append("ПРАВИЛО 24: строк-претензий в моих файлах %d, переснято чисел %d, в чужих ланах ещё %d "
                 "(не блокируется)" % (_claims24, _recheck24, _other24))
for note in notes:
    print(f"ATONEMENT CORPUS INTEGRITY: note — {note}")
if errors:
    print("ATONEMENT CORPUS INTEGRITY: FAIL")
    for err in errors:
        print(f"  - {err}")
    sys.exit(1)
print(f"ATONEMENT CORPUS INTEGRITY: PASS ({measured_root} root files, {len(SUBLANES)} sub-corpora / "
      f"{sublane_files} sub-lane files, {len(list(DOCS.glob('*.md')))} lane files, "
      f"conflict ledger C-01…C-{actual:02d}, publicationEligible=false)")
