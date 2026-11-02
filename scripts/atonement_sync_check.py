#!/usr/bin/env python3
"""Read-only regression gate for the documented atonement synchronization.

Checks retained corrections, pinned verse controls and coverage of explicitly
marked Synodal quotations. A PASS is NOT an exegetical verdict or a new examination
of printed sources. The control snapshot can be independently replayed with:
  python3 -B scripts/atonement_sync_sources.py --cache /outside/repo --fetch --verify

The historical 2026-10-30 reports remain historical; current repair states live in
synchronization_2026-11-02.json. New evidence may change an accepted formulation,
but the corresponding repair record must be reviewed rather than silently lost.
"""
from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path

from atonement_draft_citation_audit import audit_quotes
from atonement_sync_sources import SOURCES

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = "ИСКУПЛЕНИЕ/evidence"
REPORT = f"{EVIDENCE}/synchronization_2026-11-02.json"
CONTROL = f"{EVIDENCE}/source_controls_2026-11-02.json"
DRAFTS = "ИСКУПЛЕНИЕ/synthesis/drafts"


def witnesses(control: dict) -> list[tuple[str, dict]]:
    if set(control["sources"]) != set(SOURCES):
        raise ValueError("unexpected or empty witness inventory")
    policy = json.loads((ROOT / "data/repository-evidence-policy-v2.json").read_text(encoding="utf-8"))
    axes = {"evidenceClass": "sourceClasses", "accessState": "accessStates", "locatorState": "locatorStates",
            "rightsState": "rightsStates", "publicationState": "publicationStates"}
    result = []
    for name, source in control["sources"].items():
        for field, vocabulary in axes.items():
            if source.get(field) not in policy[vocabulary]:
                raise ValueError(f"missing/noncanonical source axis: {name}/{field}")
        if source["publicationState"] != "BLOCKED":
            raise ValueError(f"source control cannot clear Product promotion: {name}")
        if (source["repository"], source["commit"]) != SOURCES[name]:
            raise ValueError(f"source pin mismatch: {name}")
        verses = {}
        for row in source["verses"]:
            key = (row["book"], row["chapter"], row["verse"])
            if key in verses or not row["text"].strip():
                raise ValueError(f"duplicate/empty control verse: {name}/{key}")
            if row["sourceFile"] not in source["files"]:
                raise ValueError(f"unhashed source file: {name}/{key}")
            verses[key] = row["text"]
        if not verses:
            raise ValueError(f"empty witness: {name}")
        if name in ("rst", "rsb"):
            result.append((name, verses))
    return result


def check_repairs(root: Path, report: dict, overrides: dict | None = None) -> list[str]:
    errors, texts, ids = [], {}, set()
    overrides = overrides or {}
    for row in report["repairs"]:
        ident, file = row["id"], row["file"]
        if ident in ids:
            errors.append(f"duplicate repair id: {ident}")
        ids.add(ident)
        if not (root / file).is_file():
            errors.append(f"{ident}: missing target {file}")
            continue
        text = texts.setdefault(file, overrides.get(file, (root / file).read_text(encoding="utf-8")))
        if not row.get("reason") or not row.get("basis"):
            errors.append(f"{ident}: missing rationale/evidence")
        removed, required = row.get("removed"), row.get("required")
        if not removed or not required:
            errors.append(f"{ident}: empty regression control")
            continue
        if removed in text:
            errors.append(f"{ident}: rejected wording still present in {file}")
        if required not in text:
            errors.append(f"{ident}: reviewed replacement missing in {file}")
        basis_file = row["basis"].get("file")
        if basis_file and not (root / basis_file).is_file():
            errors.append(f"{ident}: missing evidence file {basis_file}")
    expected = {f"Q{i:02}" for i in range(1, 24)} | {f"G{i:02}" for i in range(1, 6)}
    if not expected <= ids:
        errors.append(f"lost baseline repairs: {sorted(expected - ids)}")
    for row in report.get("pathRepairs", []):
        path = root / row["file"]
        if not (path.parent / row["after"]).is_file():
            errors.append(f"corrected path no longer resolves: {row}")
        text = overrides.get(row["file"], path.read_text(encoding="utf-8"))
        if f'`{row["before"]}`' in text:
            errors.append(f"broken path restored: {row}")
    return errors


def check_greek(control: dict, checks: list[dict]) -> list[str]:
    errors = []
    source = control["sources"]["py-sblgnt"]
    texts = {(r["book"], r["chapter"], r["verse"]): r["text"] for r in source["verses"]}
    for row in checks:
        key = tuple(row["verse"])
        if key not in texts:
            errors.append(f"Greek control missing: {key}")
            continue
        for fragment in row.get("present", []):
            if fragment not in texts[key]:
                errors.append(f"Greek witness does not contain {fragment!r}: {key}")
        for fragment in row.get("absent", []):
            if fragment in texts[key]:
                errors.append(f"Greek witness contains rejected {fragment!r}: {key}")
    if source["chapterVerseNumbers"].get("Тит|2") != list(range(1, 16)):
        errors.append("Titus 2 chapter inventory is not 1–15")
    return errors


def check(root: Path, report: dict, control: dict) -> tuple[list[str], dict]:
    if report.get("publicationEligible") is not False or control.get("publicationEligible") is not False:
        return ["synchronization must not silently authorize Product publication"], {}
    corpora = witnesses(control)
    errors = check_repairs(root, report)
    errors += check_greek(control, report["greekChecks"])
    drafts = sorted((root / DRAFTS).glob("*.md"))
    if len(drafts) != report["draftCount"]:
        errors.append("draft inventory differs from the reviewed scope")
    rows = audit_quotes(root / DRAFTS, corpora)
    counts = dict(Counter(r["status"] for r in rows))
    if len(rows) != report["markedCitationCount"]:
        errors.append(f"quotation coverage drift: {len(rows)} != {report['markedCitationCount']}")
    for row in rows:
        if row["status"] not in ("CONFIRMED", "CONFIRMED_MULTI"):
            errors.append(f"{row['file']}:{row['line']} {row['status']}: {row['ref_use']}")
    return errors, {"drafts": len(drafts), "markedCitations": len(rows), "counts": counts,
                    "repairRecords": len(report["repairs"]), "pathRepairs": len(report.get("pathRepairs", []))}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", type=Path, default=ROOT)
    args = ap.parse_args()
    try:
        report = json.loads((args.root / REPORT).read_text(encoding="utf-8"))
        control = json.loads((args.root / CONTROL).read_text(encoding="utf-8"))
        errors, summary = check(args.root, report, control)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f"ATONEMENT SYNC: FAIL — {exc}")
        return 1
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True))
    for error in errors:
        print("FAIL:", error)
    if errors:
        return 1
    print("ATONEMENT SYNC: PASS — corrected wording and digital quotation controls; NOT theological/publication approval")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
