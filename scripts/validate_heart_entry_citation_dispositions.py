#!/usr/bin/env python3
"""Validate deterministic citation-disposition triage for all eighteen Heart entries."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
BUILDER = ROOT / "scripts/build_heart_whole_book_citation_inventory.py"
REGISTRY = ROOT / "data/heart-entry-citation-dispositions-2026-08-04.json"
HUMAN = ROOT / "СЕРИЯ СЕРДЦЕ/91_ENTRY_CITATION_DISPOSITION_TRIAGE_2026-08-04.md"
CURRENT = ROOT / "СЕРИЯ СЕРДЦЕ/90_CITATION_INVENTORY_CURRENT_OVERLAY_2026-08-04.md"
INVENTORY_SHA = "b25ff1a498057f6c20d92e5f98965338c40a9de752af198e9de97fefcf81b000"

errors: list[str] = []


def require(condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


def canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha256_text(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def import_builder() -> Any:
    spec = importlib.util.spec_from_file_location("heart_citation_builder", BUILDER)
    require(spec is not None and spec.loader is not None, "inventory builder import unavailable")
    if spec is None or spec.loader is None:
        return None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def build_dispositions(inventory: dict[str, Any]) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    blocker_counts: dict[str, int] = {}

    for entry in inventory["entries"]:
        aggregate = entry["aggregate"]
        state = entry["currentState"]
        blockers: list[str] = []
        if aggregate["uniqueScriptureReferences"]:
            blockers.append("SCRIPTURE_VERSION_ABBREVIATION_CONTEXT_REVIEW_REQUIRED")
        if aggregate["quotationSurfaceCount"]:
            blockers.append("QUOTATION_CLASSIFICATION_LOCATOR_REVIEW_REQUIRED")
        if aggregate["externalLinks"]:
            blockers.append("EXTERNAL_LINK_ADEQUACY_STABILITY_REVIEW_REQUIRED")
        if "NO_EXPLICIT_SOURCE_HEADING_IN_SCANNED_SCOPE" in aggregate["manualReviewReasons"]:
            blockers.append("SOURCE_HEADING_OR_BIBLIOGRAPHY_OWNER_REQUIRED")
        if not entry["readerAssembled"]:
            blockers.append("READER_MANUSCRIPT_ASSEMBLY_REQUIRED_BEFORE_FINAL_CITATION_PASS")

        if state == "ASSEMBLED_READER":
            lane = "ASSEMBLED_READER_ENTRY_REVIEW"
            next_action = "CLASSIFY_QUOTATIONS_NORMALIZE_SCRIPTURE_AND_RESOLVE_LOCATORS"
        elif state == "PRODUCT_SOURCE_ONLY":
            lane = "PRODUCT_SOURCE_TO_READER_AND_CITATION_REVIEW"
            next_action = "ASSEMBLE_BOOK_READER_THEN_CLASSIFY_QUOTATIONS_AND_RESOLVE_LOCATORS"
        elif state == "RESEARCH_DOSSIER_ONLY":
            lane = "DOSSIER_TO_READER_AND_CITATION_REVIEW"
            next_action = "ASSEMBLE_READER_FROM_DOSSIER_THEN_RUN_ENTRY_CITATION_PASS"
        else:
            raise ValueError(f"unsupported entry state: {state}")

        for blocker in blockers:
            blocker_counts[blocker] = blocker_counts.get(blocker, 0) + 1

        owners = entry["owners"]
        rows.append({
            "order": entry["order"],
            "id": entry["id"],
            "label": entry["label"],
            "currentState": state,
            "readerAssembled": entry["readerAssembled"],
            "inventoryEntrySha256": sha256_text(entry),
            "detected": {
                "ownerSurfaces": len(owners),
                "sourceHeadings": sum(len(owner["sourceHeadings"]) for owner in owners),
                "scriptureReferences": len(aggregate["uniqueScriptureReferences"]),
                "externalLinks": len(aggregate["externalLinks"]),
                "internalArticleLinks": len(aggregate["internalArticleLinks"]),
                "quotationSurfaces": aggregate["quotationSurfaceCount"],
            },
            "disposition": {
                "triageState": "TRIAGED_OPEN",
                "reviewLane": lane,
                "blockers": blockers,
                "nextCanonicalAction": next_action,
                "entryCitationPassComplete": False,
                "newDirectQuotesApproved": 0,
            },
        })

    return {
        "schemaVersion": 1,
        "authorityId": "HEART-ENTRY-CITATION-DISPOSITIONS-2026-08-04",
        "status": "EIGHTEEN_ENTRY_DISPOSITION_TRIAGE_COMPLETE_CITATION_PASS_OPEN",
        "generatedAt": "2026-08-04",
        "sourceInventory": {
            "authorityId": inventory["authorityId"],
            "decodedJsonSha256": INVENTORY_SHA,
            "transportAuthorityId": "HEART-WHOLE-BOOK-CITATION-INVENTORY-ENCODING-V2-2026-08-04",
            "researchSnapshot": inventory["researchSnapshot"],
            "productSnapshot": inventory["productSnapshot"],
        },
        "method": {
            "mode": "DETERMINISTIC_TRIAGE_OVER_COMMITTED_INVENTORY",
            "scope": "all eighteen final-order entries",
            "boundary": "Triage coverage classifies work lanes and blockers. It does not verify references, approve quotations, resolve locators, assemble missing readers or complete any entry citation pass.",
        },
        "entries": rows,
        "counts": {
            "finalBookEntries": 18,
            "triagedEntries": 18,
            "openEntries": 18,
            "entryCitationPassComplete": 0,
            "assembledReaderEntries": 4,
            "productSourceOnlyEntries": 8,
            "researchDossierOnlyEntries": 6,
            "entriesRequiringScriptureReview": blocker_counts.get("SCRIPTURE_VERSION_ABBREVIATION_CONTEXT_REVIEW_REQUIRED", 0),
            "entriesRequiringQuotationReview": blocker_counts.get("QUOTATION_CLASSIFICATION_LOCATOR_REVIEW_REQUIRED", 0),
            "entriesRequiringExternalLinkReview": blocker_counts.get("EXTERNAL_LINK_ADEQUACY_STABILITY_REVIEW_REQUIRED", 0),
            "entriesRequiringSourceHeadingOrBibliographyOwner": blocker_counts.get("SOURCE_HEADING_OR_BIBLIOGRAPHY_OWNER_REQUIRED", 0),
            "entriesRequiringReaderAssembly": blocker_counts.get("READER_MANUSCRIPT_ASSEMBLY_REQUIRED_BEFORE_FINAL_CITATION_PASS", 0),
            "newDirectQuotesApproved": 0,
        },
        "publicationBoundary": {
            "citationInventoryComplete": True,
            "entryDispositionTriageComplete": True,
            "wholeBookCitationPassComplete": False,
            "wholeBookReaderAssemblyComplete": False,
            "wholeBookLineEditComplete": False,
            "manuscriptBundleComplete": False,
            "productReleaseComplete": False,
        },
        "nextTransaction": "Resolve entry blockers in explicit chapter-level review transactions, beginning with assembled readers, without bulk approval or manuscript rewriting by implication.",
    }


parser = argparse.ArgumentParser()
parser.add_argument("--product-root", type=Path, required=True)
product_root = parser.parse_args().product_root.resolve()

builder = import_builder()
live_inventory = builder.build(product_root) if builder is not None else {}
pretty_inventory = (json.dumps(live_inventory, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
require(hashlib.sha256(pretty_inventory).hexdigest() == INVENTORY_SHA, "fresh inventory JSON authority drift")

expected = build_dispositions(live_inventory) if live_inventory else {}
try:
    actual = json.loads(REGISTRY.read_text(encoding="utf-8"))
except Exception as exc:
    errors.append(f"disposition registry read failed: {exc}")
    actual = {}
require(canonical(actual) == canonical(expected), "disposition registry differs from deterministic fresh-scan triage")

counts = actual.get("counts", {})
require(counts.get("finalBookEntries") == 18, "final entry count drift")
require(counts.get("triagedEntries") == counts.get("openEntries") == 18, "triage coverage drift")
require(counts.get("entryCitationPassComplete") == 0, "citation pass was silently advanced")
require(counts.get("entriesRequiringScriptureReview") == 18, "Scripture-review blocker count drift")
require(counts.get("entriesRequiringQuotationReview") == 18, "quotation-review blocker count drift")
require(counts.get("entriesRequiringExternalLinkReview") == 12, "external-link blocker count drift")
require(counts.get("entriesRequiringSourceHeadingOrBibliographyOwner") == 7, "source-heading blocker count drift")
require(counts.get("entriesRequiringReaderAssembly") == 14, "reader-assembly blocker count drift")
require(counts.get("newDirectQuotesApproved") == 0, "new direct quote was silently approved")

entries = actual.get("entries", [])
require(isinstance(entries, list) and len(entries) == 18, "exactly eighteen disposition rows required")
if isinstance(entries, list):
    require([row.get("order") for row in entries if isinstance(row, dict)] == list(range(1, 19)), "disposition order drift")
    require(all(row.get("disposition", {}).get("triageState") == "TRIAGED_OPEN" for row in entries if isinstance(row, dict)), "every row must remain TRIAGED_OPEN")
    require(all(row.get("disposition", {}).get("entryCitationPassComplete") is False for row in entries if isinstance(row, dict)), "entry pass must remain false")
    require(all(row.get("disposition", {}).get("newDirectQuotesApproved") == 0 for row in entries if isinstance(row, dict)), "row-level quote approval drift")

human = HUMAN.read_text(encoding="utf-8") if HUMAN.is_file() else ""
current = CURRENT.read_text(encoding="utf-8") if CURRENT.is_file() else ""
for marker in (
    "HEART-ENTRY-CITATION-DISPOSITIONS-2026-08-04",
    "DISPOSITION TRIAGE COVERAGE = 18 / 18",
    "ENTRY CITATION PASS COMPLETE = 0 / 18",
    "SCRIPTURE REVIEW REQUIRED = 18 / 18",
    "QUOTATION REVIEW REQUIRED = 18 / 18",
    "EXTERNAL-LINK REVIEW REQUIRED = 12 / 18",
    "SOURCE-HEADING / BIBLIOGRAPHY OWNER REQUIRED = 7 / 18",
    "READER ASSEMBLY REQUIRED = 14 / 18",
    "NEW DIRECT QUOTES APPROVED = 0",
):
    require(marker in human, f"human disposition marker missing: {marker}")
for marker in (
    "CITATION INVENTORY = COMPLETE",
    "ENTRY CITATION PASS COMPLETE = 0 / 18",
    "WHOLE-BOOK CITATION PASS = OPEN",
):
    require(marker in current, f"current inventory overlay marker missing: {marker}")

for forbidden in (
    "ENTRY CITATION PASS COMPLETE = 18 / 18",
    "WHOLE-BOOK CITATION PASS = CLOSED",
    "NEW DIRECT QUOTES APPROVED = 1",
    "PRODUCT RELEASE = COMPLETE",
    "TODO",
    "TBD",
):
    require(forbidden not in human, f"human disposition authority contains forbidden marker: {forbidden}")

if errors:
    print(f"Heart entry citation dispositions: FAIL ({len(errors)})", file=sys.stderr)
    for error in errors:
        print(f"- {error}", file=sys.stderr)
    raise SystemExit(1)

print(
    "Heart entry citation dispositions: PASS — "
    "18/18 triaged open, 0/18 citation passes, "
    "18 Scripture reviews, 18 quotation reviews, 12 external-link reviews, "
    "7 bibliography-owner gaps, 14 reader assemblies"
)
