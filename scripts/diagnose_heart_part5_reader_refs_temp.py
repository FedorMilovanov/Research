#!/usr/bin/env python3
"""Temporary read-only diagnostic: Part V reader Scripture refs outside reviewed owner union."""
from __future__ import annotations

import argparse
import importlib.util
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUILDER = ROOT / "scripts/build_heart_whole_book_citation_inventory.py"
READER = ROOT / "СЕРИЯ СЕРДЦЕ/133_READER_CHAPTER_V_HEART_IN_WAR_2026-08-09.md"
R3 = ROOT / "СЕРИЯ СЕРДЦЕ/65_R3_UNREGENERATE_STRUGGLE.md"
R4 = ROOT / "СЕРИЯ СЕРДЦЕ/66_R4_FOUR_SOILS.md"
R5 = ROOT / "СЕРИЯ СЕРДЦЕ/67_R5_TWO_STRUGGLES.md"
PRODUCT_REL = Path("src/components/article-pilots/rimlyanam7/Rimlyanam7Body.astro")
PRODUCT_COMMIT = "0fbe7d1ead9ebd1bea867418e254da438ec63329"

parser = argparse.ArgumentParser()
parser.add_argument("--product-root", type=Path, required=True)
args = parser.parse_args()
product_root = args.product_root.resolve()
if subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=product_root, text=True).strip() != PRODUCT_COMMIT:
    raise SystemExit("Product snapshot drift")

spec = importlib.util.spec_from_file_location("heart_inventory", BUILDER)
assert spec is not None and spec.loader is not None
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

owner_specs = [
    module.p(str(PRODUCT_REL), "native Romans 7 Body"),
    module.r(str(R3.relative_to(ROOT)), "R3 support"),
    module.r(str(R4.relative_to(ROOT)), "R4 support"),
    module.r(str(R5.relative_to(ROOT)), "R5 support"),
]
union_refs = sorted({ref for owner in owner_specs for ref in module.scan_owner(owner, product_root)["scriptureReferences"]}, key=str.casefold)
reader_scan = module.scan_owner(module.r(str(READER.relative_to(ROOT)), "Part V reader"), product_root)
reader_refs = sorted(reader_scan["scriptureReferences"], key=str.casefold)
reader_only = sorted(set(reader_refs) - set(union_refs), key=str.casefold)
covered = sorted(set(reader_refs) & set(union_refs), key=str.casefold)
print("HEART_PART5_READER_REF_DELTA=" + json.dumps({
    "readerRefs": reader_refs,
    "readerRefCount": len(reader_refs),
    "ownerUnionCount": len(union_refs),
    "coveredReaderRefs": covered,
    "readerOnlyRefs": reader_only,
}, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
if not reader_only:
    raise SystemExit("diagnostic expected a non-empty reader-only set because the permanent validator already failed")
raise SystemExit(1)
