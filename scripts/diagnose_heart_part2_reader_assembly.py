#!/usr/bin/env python3
"""Temporary read-only Part II source and reader decomposition."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUILDER = ROOT / "scripts/build_heart_whole_book_citation_inventory.py"
R3 = Path("СЕРИЯ СЕРДЦЕ/65_R3_UNREGENERATE_STRUGGLE.md")
R4 = Path("СЕРИЯ СЕРДЦЕ/66_R4_FOUR_SOILS.md")
I3 = Path("СЕРИЯ СЕРДЦЕ/109_READER_CHAPTER_I3_FALLEN_HEART_JEREMIAH_17_2026-08-04.md")
READER = Path("СЕРИЯ СЕРДЦЕ/113_READER_CHAPTER_II_FALLEN_HEART_DIAGNOSIS_2026-08-04.md")
CURRENT = Path("data/heart-entry-citation-pass-current-v5-2026-08-04.json")
INTEGRATION = Path("data/heart-whole-book-integration-2026-08-04.json")
TRIAGE = Path("data/heart-entry-citation-dispositions-2026-08-04.json")

parser = argparse.ArgumentParser()
parser.add_argument("--product-root", type=Path, required=True)
parser.add_argument("--output", type=Path, required=True)
args = parser.parse_args()
product_root = args.product_root.resolve()

spec = importlib.util.spec_from_file_location("heart_inventory", BUILDER)
assert spec is not None and spec.loader is not None
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def scan(path: Path, role: str) -> dict:
    text = (ROOT / path).read_text(encoding="utf-8")
    owner = module.scan_owner(module.r(str(path), role), product_root)
    headings = [m.group(1).strip() for m in re.finditer(r"(?m)^#{1,4}\s+(.+?)\s*$", text)]
    return {
        "path": str(path),
        "gitBlob": None,
        "sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "bytes": len(text.encode("utf-8")),
        "words": len(re.findall(r"[A-Za-zА-Яа-яЁё0-9]+(?:[.–—-][A-Za-zА-Яа-яЁё0-9]+)*", text)),
        "headings": headings,
        "scan": owner,
        "text": text,
    }

payload = {
    "r3": scan(R3, "Part II unregenerate-struggle owner"),
    "r4": scan(R4, "Part II four-soils owner"),
    "i3Boundary": scan(I3, "preceding I.3 reader boundary"),
    "reader": scan(READER, "assembled Part II reader"),
    "currentV5": json.loads((ROOT / CURRENT).read_text(encoding="utf-8")),
    "integration": json.loads((ROOT / INTEGRATION).read_text(encoding="utf-8")),
    "triage": json.loads((ROOT / TRIAGE).read_text(encoding="utf-8")),
}
payload["r3"]["gitBlob"] = "ae55b1fad5cccbdb623c551a14222e0f51ec084a"
payload["r4"]["gitBlob"] = "f82780e13cb064aa89c06427d11a938662fc3ff8"
payload["i3Boundary"]["gitBlob"] = "a958066bff3010f14540d67c900c362bd88de98a"
args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

def brief(item: dict) -> dict:
    return {
        "words": item["words"],
        "sha256": item["sha256"],
        "refs": len(item["scan"]["scriptureReferences"]),
        "quotes": item["scan"]["inlineQuotationSegments"] + item["scan"]["markdownBlockquotes"] + item["scan"]["htmlBlockquotes"],
        "external": len(item["scan"]["externalLinks"]),
        "internal": len(item["scan"]["internalArticleLinks"]),
        "sourceHeadings": item["scan"]["sourceHeadings"],
        "footnotes": item["scan"]["footnoteDefinitions"],
    }
print(json.dumps({"r3": brief(payload["r3"]), "r4": brief(payload["r4"]), "reader": brief(payload["reader"])}, ensure_ascii=False))
