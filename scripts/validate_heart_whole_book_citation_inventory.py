#!/usr/bin/env python3
"""Validate the versioned Heart citation inventory transport against a fresh scan."""
from __future__ import annotations

import argparse
import base64
import gzip
import hashlib
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
ENCODING = ROOT / "data/heart-whole-book-citation-inventory-2026-08-04.v2.encoding.json"
BUILDER = ROOT / "scripts/build_heart_whole_book_citation_inventory.py"
HUMAN = ROOT / "СЕРИЯ СЕРДЦЕ/89_WHOLE_BOOK_CITATION_INVENTORY_2026-08-04.md"
BASE_CURRENT = ROOT / "СЕРИЯ СЕРДЦЕ/00_CURRENT_AUTHORITY_2026-08-04.md"
CURRENT = ROOT / "СЕРИЯ СЕРДЦЕ/90_CITATION_INVENTORY_CURRENT_OVERLAY_2026-08-04.md"

JSON_SHA = "b25ff1a498057f6c20d92e5f98965338c40a9de752af198e9de97fefcf81b000"
EXPECTED_PART_PATHS = [
    "data/heart-whole-book-citation-inventory-2026-08-04.v2.part01.b64",
    "data/heart-whole-book-citation-inventory-2026-08-04.v2.part02a.b64",
    "data/heart-whole-book-citation-inventory-2026-08-04.v2.part02b.b64",
    "data/heart-whole-book-citation-inventory-2026-08-04.v2.part02c.b64",
    "data/heart-whole-book-citation-inventory-2026-08-04.v2.part02d.b64",
    "data/heart-whole-book-citation-inventory-2026-08-04.v2.part03.b64",
    "data/heart-whole-book-citation-inventory-2026-08-04.v2.part04.b64",
]
EXPECTED_COUNTS = {
    "finalBookEntries": 18,
    "assembledReader": 4,
    "productSourceOnly": 8,
    "researchDossierOnly": 6,
    "ownerRequired": 0,
    "uniqueOwnerFiles": 31,
    "uniqueScriptureReferences": 1063,
    "uniqueExternalLinks": 414,
    "uniqueInternalArticleLinks": 22,
    "ownerSurfacesScanned": 38,
    "footnoteDefinitions": 0,
    "markdownBlockquotes": 1115,
    "htmlBlockquotes": 0,
    "inlineQuotationSegments": 3271,
    "sourceHeadings": 20,
    "entriesRequiringManualBookReview": 18,
    "entryCitationPassComplete": 0,
    "newDirectQuotesApproved": 0,
}

errors: list[str] = []


def require(condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"{path.relative_to(ROOT)}: {exc}")
        return {}
    require(isinstance(value, dict), f"{path.relative_to(ROOT)}: object required")
    return value if isinstance(value, dict) else {}


def import_builder() -> Any:
    spec = importlib.util.spec_from_file_location("heart_citation_builder", BUILDER)
    require(spec is not None and spec.loader is not None, "builder import spec unavailable")
    if spec is None or spec.loader is None:
        return None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


parser = argparse.ArgumentParser()
parser.add_argument("--product-root", type=Path, required=True)
product_root = parser.parse_args().product_root.resolve()

encoding = read_json(ENCODING)
require(encoding.get("schemaVersion") == 2, "encoding schema drift")
require(
    encoding.get("authorityId")
    == "HEART-WHOLE-BOOK-CITATION-INVENTORY-ENCODING-V2-2026-08-04",
    "encoding authority drift",
)
require(
    encoding.get("supersedes")
    == "HEART-WHOLE-BOOK-CITATION-INVENTORY-ENCODING-2026-08-04",
    "encoding supersession drift",
)
require(encoding.get("encoding") == "gzip+base64-chunks", "encoding mode drift")
require(encoding.get("decodedJsonBytes") == 285803, "decoded JSON size drift")
require(encoding.get("decodedJsonSha256") == JSON_SHA, "decoded JSON manifest SHA drift")
require(encoding.get("gzipBytes") == 46416, "gzip size drift")
require(
    encoding.get("gzipSha256")
    == "e1aea3fdbe537972bfc9382d2fa0267d661dd70f5929602ecfcd50dda5f0f834",
    "gzip SHA drift",
)
require(encoding.get("base64Characters") == 61888, "base64 character count drift")
require(
    encoding.get("decodedAuthorityId")
    == "HEART-WHOLE-BOOK-CITATION-INVENTORY-2026-08-04",
    "decoded authority pointer drift",
)
require(
    encoding.get("decodedStatus")
    == "EIGHTEEN_ENTRY_READ_ONLY_CITATION_INVENTORY_COMPLETE_BOOK_PASS_OPEN",
    "decoded status pointer drift",
)
require(
    "corrupted V1 storage transport" in str(encoding.get("transportBoundary", ""))
    and "four independently hashed subparts" in str(encoding.get("transportBoundary", "")),
    "transport correction boundary missing",
)

parts = encoding.get("parts", [])
require(isinstance(parts, list) and len(parts) == 7, "exactly seven ordered transport parts required")
if isinstance(parts, list):
    require([part.get("path") for part in parts if isinstance(part, dict)] == EXPECTED_PART_PATHS, "transport part order drift")

encoded_parts: list[str] = []
if isinstance(parts, list):
    for index, part in enumerate(parts, start=1):
        require(isinstance(part, dict), f"part {index}: object required")
        if not isinstance(part, dict):
            continue
        path = ROOT / str(part.get("path", ""))
        require(path.is_file(), f"part {index}: file missing")
        if not path.is_file():
            continue
        normalized = "".join(path.read_text(encoding="ascii").split())
        require(len(normalized) == part.get("characters"), f"part {index}: character count drift")
        require(sha256(normalized.encode("ascii")) == part.get("normalizedSha256"), f"part {index}: normalized SHA drift")
        encoded_parts.append(normalized)

encoded = "".join(encoded_parts)
require(len(encoded) == encoding.get("base64Characters"), "assembled base64 length drift")
try:
    compressed = base64.b64decode(encoded, validate=True)
except Exception as exc:
    errors.append(f"base64 decode failed: {exc}")
    compressed = b""
require(len(compressed) == encoding.get("gzipBytes"), "decoded gzip size drift")
require(sha256(compressed) == encoding.get("gzipSha256"), "decoded gzip SHA drift")
try:
    decoded = gzip.decompress(compressed)
except Exception as exc:
    errors.append(f"gzip decode failed: {exc}")
    decoded = b""
require(len(decoded) == encoding.get("decodedJsonBytes"), "decoded JSON byte size drift")
require(sha256(decoded) == JSON_SHA, "decoded JSON SHA drift")
try:
    snapshot = json.loads(decoded.decode("utf-8"))
except Exception as exc:
    errors.append(f"decoded JSON parse failed: {exc}")
    snapshot = {}

builder = import_builder()
live = builder.build(product_root) if builder is not None else {}
require(canonical(snapshot) == canonical(live), "encoded inventory differs from fresh read-only scan")
require(snapshot.get("schemaVersion") == 1, "inventory schema drift")
require(snapshot.get("authorityId") == "HEART-WHOLE-BOOK-CITATION-INVENTORY-2026-08-04", "inventory authority drift")
require(snapshot.get("status") == "EIGHTEEN_ENTRY_READ_ONLY_CITATION_INVENTORY_COMPLETE_BOOK_PASS_OPEN", "inventory status drift")
require(snapshot.get("researchSnapshot") == "92bb7c3708b77f6e8344e8c29261d93ecea4debb", "Research snapshot drift")
require(
    snapshot.get("productSnapshot")
    == {
        "repository": "FedorMilovanov/gb-is-my-strength",
        "commit": "0fbe7d1ead9ebd1bea867418e254da438ec63329",
    },
    "Product snapshot drift",
)
require(snapshot.get("counts") == EXPECTED_COUNTS, "inventory count drift")

entries = snapshot.get("entries", [])
require(isinstance(entries, list) and len(entries) == 18, "inventory must contain eighteen entries")
if isinstance(entries, list):
    require([row.get("order") for row in entries if isinstance(row, dict)] == list(range(1, 19)), "entry order drift")
    require(
        all(row.get("aggregate", {}).get("entryCitationPassComplete") is False for row in entries if isinstance(row, dict)),
        "an entry citation pass was silently approved",
    )
    require(
        all(
            "BOOK_LEVEL_CITATION_REVIEW_REQUIRED"
            in row.get("aggregate", {}).get("manualReviewReasons", [])
            for row in entries
            if isinstance(row, dict)
        ),
        "manual book review reason missing",
    )

require(
    snapshot.get("publicationBoundary")
    == {
        "allEighteenEntriesOwnerMapped": True,
        "citationInventoryComplete": True,
        "wholeBookReaderAssemblyComplete": False,
        "wholeBookCitationPassComplete": False,
        "wholeBookTransitionDedupPassComplete": False,
        "wholeBookLineEditComplete": False,
        "manuscriptBundleComplete": False,
        "productReleaseComplete": False,
        "newDirectQuotesApproved": 0,
    },
    "publication boundary drift",
)

human = HUMAN.read_text(encoding="utf-8") if HUMAN.is_file() else ""
base_current = BASE_CURRENT.read_text(encoding="utf-8") if BASE_CURRENT.is_file() else ""
current = CURRENT.read_text(encoding="utf-8") if CURRENT.is_file() else ""
for marker in (
    "CITATION INVENTORY = COMPLETE",
    "ENTRY CITATION PASS COMPLETE = 0 / 18",
    "ENTRIES REQUIRING MANUAL BOOK REVIEW = 18 / 18",
    "WHOLE-BOOK CITATION PASS = OPEN",
    "UNIQUE SCRIPTURE REFERENCES = 1063",
    "UNIQUE EXTERNAL LINKS = 414",
    JSON_SHA,
):
    require(marker in human, f"human inventory marker missing: {marker}")
for marker in (
    "ALL 18 ENTRIES OWNER-MAPPED = TRUE",
    "ASSEMBLED READER OWNERS = 4",
    "STANDALONE OWNER GAPS = 0",
    "WHOLE-BOOK CITATION PASS = OPEN",
):
    require(marker in base_current, f"base current marker missing: {marker}")
for marker in (
    "HEART-CITATION-INVENTORY-CURRENT-OVERLAY-2026-08-04",
    "HEART-WHOLE-BOOK-CITATION-INVENTORY-ENCODING-V2-2026-08-04",
    "CORRUPTED V1 TRANSPORT = SUPERSEDED BY V2",
    "BOOTSTRAP --write MODE IN PERMANENT CI = REMOVED",
    "ENCODED REGISTRY FRESH-SCAN DRIFT GUARD = BOUND",
    "ENTRY CITATION PASS COMPLETE = 0 / 18",
):
    require(marker in current, f"current overlay marker missing: {marker}")

for text, name in ((human, "human inventory"), (base_current, "base current"), (current, "current overlay")):
    for forbidden in (
        "WHOLE-BOOK CITATION PASS = CLOSED",
        "ENTRY CITATION PASS COMPLETE = 18 / 18",
        "MANUSCRIPT BUNDLE = COMPLETE",
        "PRODUCT RELEASE = COMPLETE",
        "TODO",
        "TBD",
    ):
        require(forbidden not in text, f"{name} contains forbidden marker: {forbidden}")

if errors:
    print(f"Heart whole-book citation inventory: FAIL ({len(errors)})", file=sys.stderr)
    for error in errors:
        print(f"- {error}", file=sys.stderr)
    raise SystemExit(1)

print(
    "Heart whole-book citation inventory: PASS — "
    "18 entries, 31 files, 1063 Scripture refs, 414 external links, "
    "0/18 citation passes; v2 transport decoded and fresh-scan equal"
)
