#!/usr/bin/env python3
"""Temporary read-only I.1 Product section diagnostic."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUILDER = ROOT / "scripts/build_heart_whole_book_citation_inventory.py"
PRODUCT_PATH = Path("src/content/articles/chto-bibliya-nazyvaet-serdcem.mdx")

parser = argparse.ArgumentParser()
parser.add_argument("--product-root", type=Path, required=True)
parser.add_argument("--output", type=Path, required=True)
args = parser.parse_args()
product_root = args.product_root.resolve()
text = (product_root / PRODUCT_PATH).read_text(encoding="utf-8")

spec = importlib.util.spec_from_file_location("builder", BUILDER)
module = importlib.util.module_from_spec(spec)
assert spec is not None and spec.loader is not None
spec.loader.exec_module(module)

section_ids = re.findall(r'<h2\s+id="([^"]+)"', text)
sections = []
for section_id in section_ids:
    scoped = module.extract_sections(text, [section_id])
    sections.append({
        "id": section_id,
        "sha256": hashlib.sha256(scoped.encode("utf-8")).hexdigest(),
        "bytes": len(scoped.encode("utf-8")),
        "scriptureReferences": sorted({
            module.normalize_ref(match.group(0))
            for match in module.SCRIPTURE_RE.finditer(scoped)
        }, key=str.casefold),
        "externalLinks": sorted({
            module.trim_url(match.group(0))
            for match in module.URL_RE.finditer(scoped)
        }, key=str.casefold),
        "internalArticleLinks": sorted(set(module.ARTICLE_LINK_RE.findall(scoped))),
        "inlineQuotationSegments": len(re.findall(r'«([^»\n]{8,})»', scoped)) + len(re.findall(r'“([^”\n]{8,})”', scoped)),
        "markdownBlockquotes": sum(1 for line in scoped.splitlines() if re.match(r'^\s*>\s?\S', line)),
        "text": scoped,
    })

payload = {
    "product": {
        "repository": "FedorMilovanov/gb-is-my-strength",
        "commit": "0fbe7d1ead9ebd1bea867418e254da438ec63329",
        "path": str(PRODUCT_PATH),
        "fullSha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
    },
    "sectionOrder": section_ids,
    "sections": sections,
    "currentV3": json.loads((ROOT / "data/heart-entry-citation-pass-current-v3-2026-08-04.json").read_text(encoding="utf-8")),
    "triage": json.loads((ROOT / "data/heart-entry-citation-dispositions-2026-08-04.json").read_text(encoding="utf-8")),
}
args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({
    "sections": len(section_ids),
    "ids": section_ids,
    "uniqueScriptureReferences": len({ref for row in sections for ref in row["scriptureReferences"]}),
    "quotationSurfaces": sum(row["inlineQuotationSegments"] + row["markdownBlockquotes"] for row in sections),
    "externalLinks": len({url for row in sections for url in row["externalLinks"]}),
    "internalLinks": len({url for row in sections for url in row["internalArticleLinks"]}),
}, ensure_ascii=False))
