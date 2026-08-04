#!/usr/bin/env python3
"""Temporary read-only diagnostic for X.2 current Scripture token granularity."""
from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUILDER = ROOT / "scripts/build_heart_whole_book_citation_inventory.py"
READER = ROOT / "СЕРИЯ СЕРДЦЕ/97_READER_CHAPTER_X2_GLORIFIED_HEART_2026-08-04.md"
DOSSIER = ROOT / "СЕРИЯ СЕРДЦЕ/77_P0_JUDGMENT_TWO_RESURRECTIONS_2026-08-02.md"
X1_READER = ROOT / "СЕРИЯ СЕРДЦЕ/81_READER_CHAPTER_X1_JUDGMENT_TWO_RESURRECTIONS_2026-08-02.md"
PRODUCT_PATH = Path("src/content/articles/osvobozhdennoe-serdce.mdx")
SECTION_IDS = ["chetyre-sostoyaniya", "vopl-i-otvet", "ne-besplotnoe-parenie", "ne-sposobno-greshit", "pobeda-nad-vragom"]

parser = argparse.ArgumentParser()
parser.add_argument("--product-root", type=Path, required=True)
parser.add_argument("--output", type=Path, required=True)
args = parser.parse_args()
product_root = args.product_root.resolve()
spec = importlib.util.spec_from_file_location("builder", BUILDER)
assert spec is not None and spec.loader is not None
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
reader = module.scan_owner(module.r(str(READER.relative_to(ROOT)), "reader"), product_root)
dossier = module.scan_owner(module.r(str(DOSSIER.relative_to(ROOT)), "dossier"), product_root)
x1 = module.scan_owner(module.r(str(X1_READER.relative_to(ROOT)), "x1"), product_root)
product_text = (product_root / PRODUCT_PATH).read_text(encoding="utf-8")
product_scoped = "\n".join(module.extract_sections(product_text, [section_id]) for section_id in SECTION_IDS)
product_refs = sorted({module.normalize_ref(match.group(0)) for match in module.SCRIPTURE_RE.finditer(product_scoped)}, key=str.casefold)
support = set(dossier["scriptureReferences"]) | set(x1["scriptureReferences"])
historical = support | set(product_refs)
reader_refs = set(reader["scriptureReferences"])
current = historical | reader_refs
payload = {
    "reader": sorted(reader_refs, key=str.casefold),
    "product": product_refs,
    "supportCount": len(support),
    "historicalCount": len(historical),
    "currentCount": len(current),
    "readerAddedTokens": sorted(reader_refs - historical, key=str.casefold),
    "historicalTokensCoveredByReader": sorted(reader_refs & historical, key=str.casefold),
}
args.output.parent.mkdir(parents=True, exist_ok=True)
args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(payload, ensure_ascii=False))
