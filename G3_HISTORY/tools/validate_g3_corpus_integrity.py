#!/usr/bin/env python3
"""Deterministic integrity checks for the merged G3 research corpus.

This validator is intentionally network-free. It verifies the repository-side
evidence graph, publication firewall, Buck item registry, and G3 workflow
hardening. It does not promote any historical claim and does not replace the
external acquisition workflows.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
G3 = REPO / "G3_HISTORY"
WORKFLOWS = REPO / ".github" / "workflows"

ALLOWED_CLAIM_STATES = {
    "VERIFIED_PRIMARY",
    "CORROBORATED",
    "PARTIALLY_VERIFIED",
    "DISPUTED",
    "UNVERIFIED",
    "INFERENCE",
    "REFUTED",
}
ALLOWED_SOURCE_CLASSES = {"A1", "A2", "A3", "B1", "C", "D"}

REQUIRED_FILES = [
    G3 / "README.md",
    G3 / "SOURCE_LEDGER.md",
    G3 / "CLAIMS_LEDGER.md",
    G3 / "OPEN_QUESTIONS.md",
    G3 / "P0_CLOSURE_CHECKPOINT_2026-09-08.md",
    G3 / "BUCK_ITEMS" / "README.md",
    G3 / "DURABLE_CUSTODY_POLICY.md",
    G3 / "DURABLE_CUSTODY_MANIFEST.json",
]

G3_WORKFLOWS = [
    "g3-archive-content-inventory-acquisition.yml",
    "g3-buck-media-windows.yml",
    "g3-buck-rss-media-inventory.yml",
    "g3-buck-titus-media-acquisition.yml",
    "g3-content-inventory-acquisition.yml",
    "g3-douglas-property-acquisition.yml",
    "g3-georgia-entity-acquisition.yml",
    "g3-irs-raw-acquisition.yml",
    "g3-wayback-2025-board-transition.yml",
    "g3-wayback-late-board-acquisition.yml",
    "g3-corpus-integrity.yml",
    "g3-main-governance-audit.yml",
]

CRITICAL_CLAIM_STATES = {
    "G3-C009": "REFUTED",
    "G3-C018": "REFUTED",
    "G3-C029": "REFUTED",
    "G3-C030": "UNVERIFIED",
    "G3-C040": "REFUTED",
    "G3-C041": "UNVERIFIED",
    "G3-C048": "DISPUTED",
}


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)


def parse_table_rows(text: str, prefix: str, expected_columns: int) -> list[list[str]]:
    rows: list[list[str]] = []
    for raw in text.splitlines():
        if not raw.startswith(f"| {prefix}"):
            continue
        cells = [cell.strip() for cell in raw.strip().strip("|").split("|")]
        if len(cells) < expected_columns:
            raise ValueError(f"{prefix} row has {len(cells)} columns: {raw[:180]}")
        rows.append(cells)
    return rows


def main() -> int:
    errors: list[str] = []

    for path in REQUIRED_FILES:
        if not path.is_file():
            errors.append(f"missing required canonical file: {path.relative_to(REPO)}")

    if errors:
        for error in errors:
            fail(error)
        return 2

    readme = (G3 / "README.md").read_text(encoding="utf-8")
    claims_text = (G3 / "CLAIMS_LEDGER.md").read_text(encoding="utf-8")
    sources_text = (G3 / "SOURCE_LEDGER.md").read_text(encoding="utf-8")
    open_text = (G3 / "OPEN_QUESTIONS.md").read_text(encoding="utf-8")
    buck_readme = (G3 / "BUCK_ITEMS" / "README.md").read_text(encoding="utf-8")

    for name, text in [
        ("README.md", readme),
        ("CLAIMS_LEDGER.md", claims_text),
        ("OPEN_QUESTIONS.md", open_text),
        ("BUCK_ITEMS/README.md", buck_readme),
    ]:
        if "PUBLICATION_HOLD" not in text:
            errors.append(f"{name} lost PUBLICATION_HOLD")

    source_rows = parse_table_rows(sources_text, "G3-S", 9)
    source_ids: set[str] = set()
    for cells in source_rows:
        sid = cells[0]
        if sid in source_ids:
            errors.append(f"duplicate source id: {sid}")
        source_ids.add(sid)
        klass = cells[3]
        if klass not in ALLOWED_SOURCE_CLASSES:
            errors.append(f"{sid}: invalid source class {klass!r}")
    if len(source_ids) < 50:
        errors.append(f"unexpectedly small source ledger: {len(source_ids)} rows")

    claim_rows = parse_table_rows(claims_text, "G3-C", 5)
    claim_ids: set[str] = set()
    claim_states: dict[str, str] = {}
    for cells in claim_rows:
        cid, _, state, evidence, note = cells[:5]
        if cid in claim_ids:
            errors.append(f"duplicate claim id: {cid}")
        claim_ids.add(cid)
        claim_states[cid] = state
        if state not in ALLOWED_CLAIM_STATES:
            errors.append(f"{cid}: invalid claim state {state!r}")
        refs = set(re.findall(r"G3-S\d{3}", evidence + " " + note))
        missing = sorted(refs - source_ids)
        if missing:
            errors.append(f"{cid}: references missing source id(s): {', '.join(missing)}")
    if len(claim_ids) < 50:
        errors.append(f"unexpectedly small claim ledger: {len(claim_ids)} rows")

    for cid, expected in CRITICAL_CLAIM_STATES.items():
        actual = claim_states.get(cid)
        if actual != expected:
            errors.append(f"{cid}: critical firewall state {actual!r}, expected {expected!r}")

    qids = re.findall(r"^### Q(\d{3})\b", open_text, flags=re.M)
    if len(qids) != len(set(qids)):
        errors.append("duplicate Qxxx headings in OPEN_QUESTIONS.md")
    expected_q = {f"{i:03d}" for i in range(1, 23)}
    missing_q = sorted(expected_q - set(qids))
    if missing_q:
        errors.append(f"OPEN_QUESTIONS missing Q ids: {', '.join(missing_q)}")
    for required_phrase in [
        "DATASET_REQUIRED",
        "0/17 ITEM_VERIFIED",
        "DISPUTED / PRIMARY PMBC DOCUMENT_HOLD",
        "PUBLICATION_HOLD",
    ]:
        if required_phrase not in open_text:
            errors.append(f"OPEN_QUESTIONS lost required boundary phrase: {required_phrase!r}")

    item_rows = []
    item_re = re.compile(
        r"^\|\s*(\d{2})\s*\|.*?\|\s*\[`([^`]+\.md)`\]\(([^)]+\.md)\)\s*\|\s*$"
    )
    for line in buck_readme.splitlines():
        match = item_re.match(line)
        if match:
            item_rows.append(match.groups())
    item_numbers = [num for num, _, _ in item_rows]
    if item_numbers != [f"{i:02d}" for i in range(1, 18)]:
        errors.append(f"Buck registry rows are not exactly 01..17: {item_numbers}")
    for num, label, rel in item_rows:
        if label != rel:
            errors.append(f"Buck item {num}: link label/path mismatch: {label} vs {rel}")
        path = G3 / "BUCK_ITEMS" / rel
        if not path.is_file():
            errors.append(f"Buck item {num}: missing file {rel}")
    if "**0/17** are declared `ITEM_VERIFIED`" not in buck_readme:
        errors.append("Buck registry lost explicit 0/17 ITEM_VERIFIED firewall")
    if "45 proven instances" not in buck_readme:
        errors.append("Buck numerical-verdict firewall text missing")

    action_ref = re.compile(r"^\s*uses:\s*[^@\s]+@([^\s#]+)", flags=re.M)
    for name in G3_WORKFLOWS:
        path = WORKFLOWS / name
        if not path.is_file():
            errors.append(f"missing G3 workflow: {name}")
            continue
        text = path.read_text(encoding="utf-8")
        if "research/g3-history-20260907" in text:
            errors.append(f"{name}: still tied to retired research branch")
        if name not in {"g3-corpus-integrity.yml", "g3-main-governance-audit.yml"}:
            if "workflow_dispatch:" not in text:
                errors.append(f"{name}: missing workflow_dispatch")
            if "pull_request:" not in text:
                errors.append(f"{name}: missing pull_request trigger")
        if name == "g3-main-governance-audit.yml" and "branches: [main]" not in text:
            errors.append(f"{name}: must audit push events on main")
        if "concurrency:" not in text or "cancel-in-progress: true" not in text:
            errors.append(f"{name}: missing cancel-in-progress concurrency")
        if "pip install --upgrade" in text or "pip install -U " in text:
            errors.append(f"{name}: contains unconstrained pip upgrade")
        for ref in action_ref.findall(text):
            if not re.fullmatch(r"[0-9a-f]{40}", ref):
                errors.append(f"{name}: action ref is not pinned to 40-hex SHA: {ref}")

    locks = {
        G3 / "requirements-media.lock": [
            "yt-dlp==2026.8.19",
            "openai-whisper==20250625",
        ],
        G3 / "requirements-content.lock": ["requests==2.34.2"],
    }
    for path, required_lines in locks.items():
        if not path.is_file():
            errors.append(f"missing dependency lock: {path.relative_to(REPO)}")
            continue
        lines = {
            line.strip()
            for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.lstrip().startswith("#")
        }
        for required in required_lines:
            if required not in lines:
                errors.append(f"{path.name}: missing exact pin {required}")

    if errors:
        for error in errors:
            fail(error)
        print(f"G3_CORPUS_INTEGRITY=FAIL errors={len(errors)}", file=sys.stderr)
        return 2

    print(
        "G3_CORPUS_INTEGRITY=PASS "
        f"sources={len(source_ids)} claims={len(claim_ids)} "
        f"open_questions={len(qids)} buck_items={len(item_rows)} "
        f"workflows={len(G3_WORKFLOWS)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
