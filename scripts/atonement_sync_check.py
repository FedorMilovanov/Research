#!/usr/bin/env python3
"""Read-only regression gate for the documented atonement synchronization.

Checks retained corrections, pinned verse controls and coverage of explicitly
marked Synodal quotations. A PASS is NOT an exegetical verdict or a new examination
of printed sources. The control snapshot can be independently replayed with:
  python3 -B scripts/atonement_sync_sources.py --cache /outside/repo --fetch --verify

The historical 2026-10-30 reports remain historical; current repair states live in
synchronization_2026-11-02.json. New evidence may change an accepted formulation,
but the corresponding repair record must be reviewed rather than silently lost.

Wave 2 also checks the scoped PDF evidence record and the bytes of superseded Git
snapshots. It does not download private sources. An optional read-only replay is:
  python3 -B scripts/atonement_sync_check.py --prokopenko-pdf /outside/repo/article.pdf
That option needs pypdf (the recorded extraction used 6.21.4); ordinary CI does not.
Without it, PASS means retained controls, not a new PDF extraction or full reading.

Wave 3 adds offline OT/patristic/John11 controls and bounded reading provenance.
Fresh external byte/extract replay is separate and never implicit:
  python3 -B scripts/atonement_wave3_sources.py --source-root /outside/repo/sources
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import io
import json
from pathlib import Path
import re
import subprocess
import unicodedata

from atonement_draft_citation_audit import audit_quotes
from atonement_sync_sources import SOURCES
from atonement_wave3_sources import CONTROL as WAVE3_CONTROL, check_controls as check_wave3
from atonement_wave4_sources import CONTROL as WAVE4_CONTROL, check_controls as check_wave4
from atonement_wave5_sources import CONTROL as WAVE5_CONTROL, check_controls as check_wave5
from atonement_wave6_sources import CONTROL as WAVE6_CONTROL, check_controls as check_wave6
from atonement_wave7_sources import CONTROL as WAVE7_CONTROL, check_controls as check_wave7
from atonement_wave8_sources import CONTROL as WAVE8_CONTROL, check_controls as check_wave8
from atonement_wave9_sources import CONTROL as WAVE9_CONTROL, check_controls as check_wave9

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = "ИСКУПЛЕНИЕ/evidence"
REPORT = f"{EVIDENCE}/synchronization_2026-11-02.json"
CONTROL = f"{EVIDENCE}/source_controls_2026-11-02.json"
DRAFTS = "ИСКУПЛЕНИЕ/synthesis/drafts"
PROKOPENKO_SHA256 = "d7c7519ddbe845110c50793450dccf980f38783ef757c337c83ea1c71f99bea8"
PROKOPENKO_MD5 = "263c762500bfdf65da3a904d69ba642f"
PROKOPENKO_BYTES = 919808
PDF_CONTROL_IDS = {"P08", "P10", "P19", "P23", "P24", "P25", "P26", "P29", "P29b",
                   "P30", "P31a", "P31b", "P31c", "P34"}
SYNTHESIS_REPAIR_IDS = {f"S{i:02}" for i in range(1, 43)}


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
        if row.get("historicalRetained"):
            # Explicitly preserved history is not an active accepted claim. The
            # reviewed supersession notice must precede the old wording.
            if "SUPERSEDED" not in required or removed not in text:
                errors.append(f"{ident}: historical retention lost its explicit boundary/text")
            if required in text and removed in text and text.index(required) > text.index(removed):
                errors.append(f"{ident}: supersession notice must precede historical wording")
        elif removed in text:
            errors.append(f"{ident}: rejected wording still present in {file}")
        if required not in text:
            errors.append(f"{ident}: reviewed replacement missing in {file}")
        basis_file = row["basis"].get("file")
        if basis_file and not (root / basis_file).is_file():
            errors.append(f"{ident}: missing evidence file {basis_file}")
    expected = {f"Q{i:02}" for i in range(1, 24)} | {f"G{i:02}" for i in range(1, 6)}
    expected |= SYNTHESIS_REPAIR_IDS
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


def check_wave2(root: Path, report: dict) -> list[str]:
    """Validate provenance and scoped claims; do not infer reading from access."""
    errors = []
    wave = report.get("wave2")
    if not isinstance(wave, dict) or not isinstance(wave.get("primaryArticle"), dict):
        return ["wave2: missing primary article/provenance"]
    source = wave["primaryArticle"]
    policy = json.loads((root / "data/repository-evidence-policy-v2.json").read_text(encoding="utf-8"))
    axes = {"evidenceClass": "sourceClasses", "accessState": "accessStates", "locatorState": "locatorStates",
            "rightsState": "rightsStates", "publicationState": "publicationStates"}
    for field, vocabulary in axes.items():
        if source.get(field) not in policy[vocabulary]:
            errors.append(f"wave2: missing/noncanonical source axis {field}")
    if source.get("publicationEligible") is not False or source.get("publicationState") != "BLOCKED":
        errors.append("wave2: source access cannot authorize Product publication")
    if (source.get("sha256"), source.get("md5"), source.get("bytes")) != (
            PROKOPENKO_SHA256, PROKOPENKO_MD5, PROKOPENKO_BYTES):
        errors.append("wave2: primary PDF byte pin changed")
    pages = source.get("readPages", [])
    if source.get("pageCount") != 40 or pages != [8, 9, 10, 11, *range(19, 37)]:
        errors.append("wave2: declared reading scope changed; preserve this dated observation")
    if source.get("fullReadingClaimed") is not False:
        errors.append("wave2: full access is not full reading")
    for field in ("id", "title", "author", "url", "driveFileId", "hashVerification", "locatorScope", "custody"):
        if not source.get(field):
            errors.append(f"wave2: missing provenance field {field}")
    controls = source.get("controls", [])
    ids = [row.get("id") for row in controls]
    if len(ids) != len(set(ids)) or not PDF_CONTROL_IDS <= set(ids):
        errors.append("wave2: lost/duplicate primary PDF control")
    for row in controls:
        if type(row.get("pdfPage")) is not int or row.get("pdfPage") not in pages or not row.get("text", "").strip():
            errors.append(f"wave2: empty or out-of-scope PDF control {row.get('id')}")
    for row in report["repairs"]:
        if row["id"] not in SYNTHESIS_REPAIR_IDS:
            continue
        basis = row.get("basis", {})
        if basis.get("sourceId") and basis["sourceId"] != source["id"]:
            errors.append(f"{row['id']}: unregistered primary source")
        if not set(basis.get("controlIds", [])) <= set(ids):
            errors.append(f"{row['id']}: nonexistent PDF evidence control")
    snapshots = wave.get("supersededSnapshots", [])
    expected_files = {r["file"] for r in report["repairs"] if r["id"] in SYNTHESIS_REPAIR_IDS}
    files = [row.get("file") for row in snapshots]
    if len(files) != len(set(files)) or not expected_files <= set(files):
        errors.append("wave2: missing/duplicate superseded snapshot")
    for row in snapshots:
        file, commit = row.get("file", ""), row.get("commit", "")
        if not re.fullmatch(r"[0-9a-f]{40}", commit) or not re.fullmatch(r"[0-9a-f]{40}", row.get("blob", "")):
            errors.append(f"wave2: invalid Git snapshot pin {file}")
            continue
        result = subprocess.run(["git", "cat-file", "blob", f"{commit}:{file}"], cwd=root,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        if result.returncode:
            errors.append(f"wave2: Git snapshot unavailable (full history required): {file}")
            continue
        raw = result.stdout
        blob = hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()
        if (len(raw), hashlib.sha256(raw).hexdigest(), blob) != (row.get("bytes"), row.get("sha256"), row["blob"]):
            errors.append(f"wave2: Git snapshot bytes/hash mismatch: {file}")
    return errors


def pdf_control_text(text: str) -> str:
    """Only Unicode/whitespace normalization; no paraphrase or fuzzy matching."""
    return " ".join(unicodedata.normalize("NFC", text).split())


def verify_pdf_bytes(raw: bytes, source: dict) -> list[str]:
    errors = []
    if len(raw) != source["bytes"]:
        errors.append("PDF: byte size mismatch")
    if hashlib.sha256(raw).hexdigest() != source["sha256"]:
        errors.append("PDF: SHA-256 mismatch")
    if hashlib.md5(raw, usedforsecurity=False).hexdigest() != source["md5"]:
        errors.append("PDF: MD5 mismatch")
    return errors


def verify_pdf_page_controls(texts: list[str], source: dict) -> list[str]:
    """Used on extracted pages, not as proof that all pages were read by a person."""
    errors = []
    if len(texts) != source["pageCount"]:
        errors.append("PDF: page inventory mismatch")
    for row in source["controls"]:
        n = row["pdfPage"]
        if not 1 <= n <= len(texts) or pdf_control_text(row["text"]) not in pdf_control_text(texts[n - 1]):
            errors.append(f"PDF: control {row['id']} absent from declared page {n}")
    return errors


def verify_prokopenko_pdf(path: Path, source: dict) -> list[str]:
    """Optional local replay. Never fetch, save, or publish the source."""
    raw = path.read_bytes()
    errors = verify_pdf_bytes(raw, source)
    if errors:
        return errors
    try:
        from pypdf import PdfReader
    except ImportError as exc:
        raise ValueError("optional PDF replay requires pypdf; recorded extraction used 6.21.4") from exc
    reader = PdfReader(io.BytesIO(raw))
    texts = [page.extract_text() or "" for page in reader.pages]
    errors += verify_pdf_page_controls(texts, source)
    search = source.get("searchScope", {})
    if search:
        russian, latin = [], []
        for n, text in enumerate(texts, 1):
            russian.extend([n] * len(re.findall(r"Бакстер\w*", text, re.IGNORECASE)))
            latin.extend([n] * len(re.findall(r"Baxter", text, re.IGNORECASE)))
        if {"Russian": russian, "Latin": latin} != search["hits"]:
            errors.append("PDF: Baxter search-context inventory changed")
    return errors


def check(root: Path, report: dict, control: dict) -> tuple[list[str], dict]:
    if report.get("publicationEligible") is not False or control.get("publicationEligible") is not False:
        return ["synchronization must not silently authorize Product publication"], {}
    corpora = witnesses(control)
    errors = check_repairs(root, report)
    errors += check_greek(control, report["greekChecks"])
    errors += check_wave2(root, report)
    wave3_control = json.loads((root / WAVE3_CONTROL).read_text(encoding="utf-8"))
    errors += check_wave3(root, report, wave3_control)
    wave4_control = json.loads((root / WAVE4_CONTROL).read_text(encoding="utf-8"))
    errors += check_wave4(root, report, wave4_control)
    wave5_control = json.loads((root / WAVE5_CONTROL).read_text(encoding="utf-8"))
    errors += check_wave5(root, report, wave5_control)
    wave6_control = json.loads((root / WAVE6_CONTROL).read_text(encoding="utf-8"))
    errors += check_wave6(root, report, wave6_control)
    wave7_control = json.loads((root / WAVE7_CONTROL).read_text(encoding="utf-8"))
    errors += check_wave7(root, report, wave7_control)
    wave8_control = json.loads((root / WAVE8_CONTROL).read_text(encoding="utf-8"))
    errors += check_wave8(root, report, wave8_control)
    wave9_control = json.loads((root / WAVE9_CONTROL).read_text(encoding="utf-8"))
    errors += check_wave9(root, report, wave9_control)
    drafts = sorted((root / DRAFTS).glob("*.md"))
    # The dated baseline scope remains 13. New drafts must be independently
    # inventoried and byte-identified; neither changing that historical count
    # nor silently ignoring new files is permitted.
    additions = report.get("postReviewDrafts", [])
    if not isinstance(additions, list):
        errors.append("post-review draft inventory must be a list")
        additions = []
    added_paths: set[str] = set()
    for item in additions:
        if not isinstance(item, dict):
            errors.append("post-review draft declaration is not an object")
            continue
        declared_path, digest = item.get("path"), item.get("sha256")
        if not isinstance(declared_path, str) or not isinstance(digest, str):
            errors.append("post-review draft lacks path/sha256")
            continue
        rel = Path(declared_path)
        if rel.parent != Path(DRAFTS) or rel.suffix != ".md" or declared_path != rel.as_posix():
            errors.append(f"post-review draft path outside the drafts directory: {declared_path}")
            continue
        if declared_path in added_paths:
            errors.append(f"duplicate post-review draft declaration: {declared_path}")
            continue
        added_paths.add(declared_path)
        if item.get("publicationEligible") is not False:
            errors.append(f"post-review draft must remain unpublished: {declared_path}")
        target = root / rel
        if not target.is_file():
            errors.append(f"declared post-review draft absent: {declared_path}")
        elif not re.fullmatch(r"[0-9a-f]{64}", digest):
            errors.append(f"invalid post-review draft sha256: {declared_path}")
        elif hashlib.sha256(target.read_bytes()).hexdigest() != digest:
            errors.append(f"post-review draft bytes differ from declaration: {declared_path}")
    current_paths = {p.relative_to(root).as_posix() for p in drafts}
    if (not added_paths.issubset(current_paths)
            or len(drafts) - len(added_paths) != report["draftCount"]):
        errors.append("draft inventory differs from reviewed baseline plus declared additions")
    rows = audit_quotes(root / DRAFTS, corpora)
    counts = dict(Counter(r["status"] for r in rows))
    if len(rows) != report["markedCitationCount"]:
        errors.append(f"quotation coverage drift: {len(rows)} != {report['markedCitationCount']}")
    for row in rows:
        if row["status"] not in ("CONFIRMED", "CONFIRMED_MULTI"):
            errors.append(f"{row['file']}:{row['line']} {row['status']}: {row['ref_use']}")
    return errors, {"drafts": len(drafts), "markedCitations": len(rows), "counts": counts,
                    "repairRecords": len(report["repairs"]), "pathRepairs": len(report.get("pathRepairs", [])),
                    "primaryPdfControls": len(report.get("wave2", {}).get("primaryArticle", {}).get("controls", [])),
                    "pdfReplay": "NOT_RUN", "supersededSnapshots": len(report.get("wave2", {}).get("supersededSnapshots", [])),
                    "wave3SourceFiles": len(wave3_control["files"]), "wave3Extracts": len(wave3_control["extracts"]),
                    "wave3SupersededSnapshots": len(report.get("wave3", {}).get("supersededSnapshots", [])),
                    "wave3SourceReplay": "NOT_RUN", "readingMeasuredByLabels": False,
                    "wave4SourceFiles": len(wave4_control["files"]), "wave4Extracts": len(wave4_control["extracts"]),
                    "wave4RenderedWebObservations": len(wave4_control["webObservations"]),
                    "wave4SourceReplay": "NOT_RUN",
                    "wave5SourceFiles": len(wave5_control["files"]),
                    "wave5GreekContexts": len(wave5_control["greekContexts"]),
                    "wave5RenderedWebObservations": len(wave5_control["webObservations"]),
                    "wave5SourceReplay": "NOT_RUN", "webHttpReplay": "NOT_AVAILABLE_RENDERED_OBSERVATIONS_ONLY",
                    "wave6SourceFiles": len(wave6_control["files"]),
                    "wave6Contexts": len(wave6_control["contexts"]),
                    "wave6VersePairs": sum(len(p["verseMap"]) for p in wave6_control["pairings"]),
                    "wave6SourceReplay": "NOT_RUN",
                    "wave7ControlledArtifacts": len(wave7_control["files"]),
                    "wave7GreekCandidates": len(wave7_control["candidates"]),
                    "wave7GreekOriginalVerified": False,
                    "wave7SourceReplay": "NOT_RUN",
                    "wave8ControlledArtifacts": len(wave8_control["files"]),
                    "wave8VisuallyInspectedA1Scans": wave8_control["statistics"]["visuallyInspectedA1PrintScans"],
                    "wave8GreekOriginalFor1152Verified": False,
                    "wave8SourceReplay": "NOT_RUN",
                    "wave9ControlledArtifacts": len(wave9_control["files"]),
                    "wave9VisuallyInspectedA1Scans": wave9_control["statistics"]["visuallyInspectedA1PrintScans"],
                    "wave9CorrectedA1TeiXml": wave9_control["statistics"]["correctedA1TeiXmlObjects"],
                    "wave9FullCyril1152GreekOriginalVerified": False,
                    "wave9SourceReplay": "NOT_RUN"}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", type=Path, default=ROOT)
    ap.add_argument("--prokopenko-pdf", type=Path,
                    help="optional byte/page replay against a locally supplied PDF (requires pypdf)")
    args = ap.parse_args()
    try:
        report = json.loads((args.root / REPORT).read_text(encoding="utf-8"))
        control = json.loads((args.root / CONTROL).read_text(encoding="utf-8"))
        errors, summary = check(args.root, report, control)
        if args.prokopenko_pdf:
            pdf_errors = verify_prokopenko_pdf(args.prokopenko_pdf, report["wave2"]["primaryArticle"])
            errors += pdf_errors
            summary["pdfReplay"] = "FAIL" if pdf_errors else "PASS"
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f"ATONEMENT SYNC: FAIL — {exc}")
        return 1
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True))
    for error in errors:
        print("FAIL:", error)
    if errors:
        return 1
    print("ATONEMENT SYNC: PASS — retained corrections, source controls and Git snapshot bytes; NOT full reading/theological/publication approval")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
