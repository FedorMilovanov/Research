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

Fail-closed. Writes nothing. Exit 1 on any drift.
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

# ------------------------------------------------------------- machine registry --
registry = {}
try:
    registry = json.loads(read(REG))
except Exception as exc:  # noqa: BLE001 - a broken registry must fail the gate
    errors.append(f"corpus registry unreadable: {exc}")
if registry:
    req(registry.get("authorityId") == AUTHORITY_ID, "registry: authorityId drift")
    agents = registry.get("parallelAgents", {})
    state = str(agents.get("gitPathState", ""))
    for key, value in agents.items():
        if not isinstance(value, str):
            continue
        if value.startswith(("ИСКУПЛЕНИЕ/", "data/", "docs/")) and not resolve(value):
            req(bool(state), f"registry: parallelAgents.{key} points at an absent git path "
                            f"{value!r} and no gitPathState declares it")
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
    errors.append("adjacent lane absent: docs/research/atonement")
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

# ----------------------------------------------------- conflict-ledger arithmetic --
ledger = read(CORPUS / "synthesis" / "02_CONFLICT_LEDGER.md")
actual = max((int(n) for n in re.findall(r"\bC-(\d{2})\b", ledger)), default=0)
claimed = [int(n) for n in re.findall(r"C-\d{2}\s*[.…]+\s*C-?(\d{2})", read(AUTHORITY))]
if claimed and actual and max(claimed) != actual:
    errors.append(
        f"conflict ledger holds C-01…C-{actual:02d} while the corpus authority claims "
        f"…C-{max(claimed):02d}: update the authority, do not leave the count stale"
    )

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
    for needle in ("unrelated", "99 — HOLD", "7 908"):
        req(needle in recon_text, f"reconciliation record no longer states {needle!r}")

if errors:
    print("ATONEMENT CORPUS INTEGRITY: FAIL")
    for err in errors:
        print(f"  - {err}")
    sys.exit(1)
print(f"ATONEMENT CORPUS INTEGRITY: PASS ({len(SPINE)} root files, {len(SUBLANES)} sub-corpora, "
      f"{len(list(DOCS.glob('*.md')))} lane files, conflict ledger C-01…C-{actual:02d}, "
      "publicationEligible=false)")
