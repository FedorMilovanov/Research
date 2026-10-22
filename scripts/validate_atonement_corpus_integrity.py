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
actual = max((int(n) for n in re.findall(r"\bC-(\d{2})\b", ledger)), default=0)
claimed = [int(n) for n in re.findall(r"C-\d{2}\s*[.…]+\s*C-?(\d{2})", read(AUTHORITY))]
if claimed and actual and max(claimed) != actual:
    errors.append(
        f"conflict ledger holds C-01…C-{actual:02d} while the corpus authority claims "
        f"…C-{max(claimed):02d}: update the authority, do not leave the count stale"
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
    def walk_measure(node, where):
        if isinstance(node, dict):
            stamps = sorted(k for k in node if STAMP.match(str(k)))
            if stamps:
                val = str(node[stamps[0]])
                if not re.search(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}", val):
                    errors.append(
                        f"{where}.{stamps[0]} = {val!r}: съёмка без точного времени (HH:MM). Дата без "
                        "часов не позволяет отличить «устарело» от «проверено сегодня»"
                    )
                if not (set(map(str, node)) & HOW):
                    errors.append(
                        f"{where}: датировано, но способа переснять нет (нет ни одного из {sorted(HOW)[:4]}…). "
                        "Число, которое нельзя переснять, — это мнение, а не замер"
                    )
            for key, val in node.items():
                walk_measure(val, f"{where}.{key}")
        elif isinstance(node, list):
            for i, val in enumerate(node):
                walk_measure(val, f"{where}[{i}]")
    walk_measure(reg, "реестр")

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
    walk_fake(reg, "реестр")

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
