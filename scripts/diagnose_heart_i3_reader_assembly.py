#!/usr/bin/env python3
"""Temporary read-only exact I.3 Product and reader decomposition."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
BUILDER = ROOT / "scripts/build_heart_whole_book_citation_inventory.py"
PRODUCT_PATH = Path("src/content/articles/krajne-li-isporcheno-serdce.mdx")
READER_PATH = Path("СЕРИЯ СЕРДЦЕ/109_READER_CHAPTER_I3_FALLEN_HEART_JEREMIAH_17_2026-08-04.md")
I1_READER = ROOT / "СЕРИЯ СЕРДЦЕ/105_READER_CHAPTER_I1_WHAT_BIBLE_CALLS_HEART_2026-08-04.md"
I2_READER = ROOT / "СЕРИЯ СЕРДЦЕ/79_READER_CHAPTER_I2_HEART_IN_EDEN_2026-08-02.md"
R3 = ROOT / "СЕРИЯ СЕРДЦЕ/65_R3_UNREGENERATE_STRUGGLE.md"
R4 = ROOT / "СЕРИЯ СЕРДЦЕ/66_R4_FOUR_SOILS.md"
CURRENT_V4 = ROOT / "data/heart-entry-citation-pass-current-v4-2026-08-04.json"
INTEGRATION = ROOT / "data/heart-whole-book-integration-2026-08-04.json"
TRIAGE = ROOT / "data/heart-entry-citation-dispositions-2026-08-04.json"

parser = argparse.ArgumentParser()
parser.add_argument("--product-root", type=Path, required=True)
parser.add_argument("--output", type=Path, required=True)
args = parser.parse_args()
product_root = args.product_root.resolve()

spec = importlib.util.spec_from_file_location("heart_inventory", BUILDER)
assert spec is not None and spec.loader is not None
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

product_text = (product_root / PRODUCT_PATH).read_text(encoding="utf-8")
reader_text = (ROOT / READER_PATH).read_text(encoding="utf-8")
full_scan = module.scan_owner(module.p(str(PRODUCT_PATH), "historical full I.3 owner"), product_root)
reader_scan = module.scan_owner(module.r(str(READER_PATH), "assembled I.3 reader"), product_root)
section_starts = [(m.start(), m.group(1)) for m in re.finditer(r'<h2\s+id="([^"]+)"', product_text)]
sections: list[dict[str, Any]] = []
for index, (start, section_id) in enumerate(section_starts):
    end = section_starts[index + 1][0] if index + 1 < len(section_starts) else len(product_text)
    scoped = product_text[start:end]
    refs = sorted({module.normalize_ref(m.group(0)) for m in module.SCRIPTURE_RE.finditer(scoped)}, key=str.casefold)
    external = sorted({module.trim_url(m.group(0)) for m in module.URL_RE.finditer(scoped)}, key=str.casefold)
    internal = sorted(set(module.ARTICLE_LINK_RE.findall(scoped)))
    russian = re.findall(r"«([^»\n]{8,})»", scoped)
    curly = re.findall(r"“([^”\n]{8,})”", scoped)
    markdown_blocks = [line.lstrip()[1:].strip() for line in scoped.splitlines() if re.match(r"^\s*>\s?\S", line)]
    html_blocks = [re.sub(r"<[^>]+>", " ", item).strip() for item in re.findall(r"<blockquote[^>]*>(.*?)</blockquote>", scoped, flags=re.S | re.I)]
    sections.append({
        "id": section_id,
        "sha256": hashlib.sha256(scoped.encode("utf-8")).hexdigest(),
        "bytes": len(scoped.encode("utf-8")),
        "scriptureReferences": refs,
        "externalLinks": external,
        "internalArticleLinks": internal,
        "inlineQuotationSegments": len(russian) + len(curly),
        "markdownBlockquotes": len(markdown_blocks),
        "htmlBlockquotes": len(html_blocks),
        "quotationSurfaces": len(russian) + len(curly) + len(markdown_blocks) + len(html_blocks),
        "text": scoped,
    })

payload = {
    "product": {
        "repository": "FedorMilovanov/gb-is-my-strength",
        "commit": "0fbe7d1ead9ebd1bea867418e254da438ec63329",
        "path": str(PRODUCT_PATH),
        "gitBlob": "dc27b7a06d37321a068e971c02af4a0df3028ae6",
        "fullSha256": hashlib.sha256(product_text.encode("utf-8")).hexdigest(),
        "fullScan": full_scan,
        "sections": sections,
    },
    "reader": {
        "path": str(READER_PATH),
        "fullSha256": hashlib.sha256(reader_text.encode("utf-8")).hexdigest(),
        "scan": reader_scan,
    },
    "boundaries": {
        "i1Reader": I1_READER.read_text(encoding="utf-8"),
        "i2Reader": I2_READER.read_text(encoding="utf-8"),
        "partIiR3": R3.read_text(encoding="utf-8"),
        "partIiR4": R4.read_text(encoding="utf-8"),
        "currentV4": json.loads(CURRENT_V4.read_text(encoding="utf-8")),
        "integration": json.loads(INTEGRATION.read_text(encoding="utf-8")),
        "triage": json.loads(TRIAGE.read_text(encoding="utf-8")),
    },
}
args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({
    "sections": len(sections),
    "sectionIds": [row["id"] for row in sections],
    "fullRefs": len(full_scan["scriptureReferences"]),
    "fullQuotes": full_scan["inlineQuotationSegments"] + full_scan["markdownBlockquotes"] + full_scan["htmlBlockquotes"],
    "fullExternal": len(full_scan["externalLinks"]),
    "fullInternal": len(full_scan["internalArticleLinks"]),
    "readerRefs": len(reader_scan["scriptureReferences"]),
    "readerQuotes": reader_scan["inlineQuotationSegments"] + reader_scan["markdownBlockquotes"] + reader_scan["htmlBlockquotes"],
    "readerExternal": len(reader_scan["externalLinks"]),
    "readerInternal": len(reader_scan["internalArticleLinks"]),
    "sectionBytes": {row["id"]: row["bytes"] for row in sections},
    "sectionRefs": {row["id"]: len(row["scriptureReferences"]) for row in sections},
    "sectionQuotes": {row["id"]: row["quotationSurfaces"] for row in sections},
}, ensure_ascii=False))
