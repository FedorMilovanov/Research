#!/usr/bin/env python3
"""Generate the versioned Heart citation inventory transport from a fresh exact scan.

Temporary bootstrap utility. It writes only the v2 encoding manifest and four
base64 transport parts. The decoded JSON authority is unchanged and must match
the pinned SHA before any output is accepted.
"""
from __future__ import annotations

import argparse
import base64
import gzip
import hashlib
import importlib.util
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
BUILDER = ROOT / "scripts/build_heart_whole_book_citation_inventory.py"
PREFIX = "heart-whole-book-citation-inventory-2026-08-04.v2"
ENCODING = ROOT / f"data/{PREFIX}.encoding.json"
JSON_SHA = "b25ff1a498057f6c20d92e5f98965338c40a9de752af198e9de97fefcf81b000"
PART_COUNT = 4


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def import_builder() -> Any:
    spec = importlib.util.spec_from_file_location("heart_citation_builder", BUILDER)
    if spec is None or spec.loader is None:
        raise RuntimeError("builder import spec unavailable")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write_if_changed(path: Path, content: str) -> bool:
    previous = path.read_text(encoding="utf-8") if path.is_file() else None
    if previous == content:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return True


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--product-root", type=Path, required=True)
    args = parser.parse_args()

    builder = import_builder()
    report = builder.build(args.product_root.resolve())
    decoded = (json.dumps(report, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    actual_json_sha = sha256(decoded)
    if actual_json_sha != JSON_SHA:
        raise SystemExit(f"decoded JSON authority drift: {actual_json_sha}")

    compressed = gzip.compress(decoded, compresslevel=9, mtime=0)
    encoded = base64.b64encode(compressed).decode("ascii")
    if len(encoded) % PART_COUNT != 0:
        raise SystemExit("base64 transport no longer divides into four equal parts")
    part_size = len(encoded) // PART_COUNT
    parts: list[dict[str, Any]] = []
    changed = False

    for index in range(PART_COUNT):
        part = encoded[index * part_size:(index + 1) * part_size]
        relative = f"data/{PREFIX}.part{index + 1:02}.b64"
        changed |= write_if_changed(ROOT / relative, part + "\n")
        parts.append({
            "path": relative,
            "characters": len(part),
            "normalizedSha256": sha256(part.encode("ascii")),
        })

    manifest = {
        "schemaVersion": 2,
        "authorityId": "HEART-WHOLE-BOOK-CITATION-INVENTORY-ENCODING-V2-2026-08-04",
        "supersedes": "HEART-WHOLE-BOOK-CITATION-INVENTORY-ENCODING-2026-08-04",
        "encoding": "gzip+base64-chunks",
        "decodedJsonPath": "data/heart-whole-book-citation-inventory-2026-08-04.json",
        "decodedJsonBytes": len(decoded),
        "decodedJsonSha256": actual_json_sha,
        "gzipBytes": len(compressed),
        "gzipSha256": sha256(compressed),
        "base64Characters": len(encoded),
        "parts": parts,
        "decodedAuthorityId": "HEART-WHOLE-BOOK-CITATION-INVENTORY-2026-08-04",
        "decodedStatus": "EIGHTEEN_ENTRY_READ_ONLY_CITATION_INVENTORY_COMPLETE_BOOK_PASS_OPEN",
        "transportBoundary": "V2 replaces only the corrupted V1 storage transport. The decoded inventory JSON authority and fresh-scan equality are unchanged.",
    }
    changed |= write_if_changed(ENCODING, json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")

    print(
        "Heart citation encoding v2: "
        f"{'UPDATED' if changed else 'UNCHANGED'} — "
        f"JSON {len(decoded)} bytes/{actual_json_sha}, "
        f"gzip {len(compressed)} bytes/{manifest['gzipSha256']}, "
        f"4 parts × {part_size} chars"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
