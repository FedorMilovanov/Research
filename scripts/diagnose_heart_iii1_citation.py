#!/usr/bin/env python3
"""Temporary read-only III.1 quotation and link decomposition."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUILDER = ROOT / "scripts/build_heart_whole_book_citation_inventory.py"
PRODUCT_REL = Path("src/content/articles/novoe-serdce.mdx")
PRODUCT_COMMIT = "0fbe7d1ead9ebd1bea867418e254da438ec63329"
PRODUCT_BLOB = "8d4936d6b58b380215b259a5511a8c2bfad33a46"


def norm(value: str) -> str:
    value = re.sub(r"<[^>]+>", " ", value)
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def sha(value: str) -> str:
    return hashlib.sha256(norm(value).encode("utf-8")).hexdigest()


parser = argparse.ArgumentParser()
parser.add_argument("--product-root", type=Path, required=True)
args = parser.parse_args()
product_root = args.product_root.resolve()
path = product_root / PRODUCT_REL
assert subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=product_root, text=True).strip() == PRODUCT_COMMIT
assert subprocess.check_output(["git", "hash-object", str(PRODUCT_REL)], cwd=product_root, text=True).strip() == PRODUCT_BLOB
text = path.read_text(encoding="utf-8")

spec = importlib.util.spec_from_file_location("heart_inventory", BUILDER)
assert spec is not None and spec.loader is not None
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

starts = list(re.finditer(r'<h2\s+id="([^"]+)"[^>]*>', text, flags=re.I))
sections: list[tuple[int, int, str]] = []
for index, match in enumerate(starts):
    end = starts[index + 1].start() if index + 1 < len(starts) else len(text)
    sections.append((match.start(), end, match.group(1)))


def section_for(pos: int) -> str:
    for start, end, section_id in sections:
        if start <= pos < end:
            return section_id
    return "frontmatter-or-intro"


rows: list[dict[str, object]] = []
patterns = [
    ("RUSSIAN_GUILLEMETS", re.compile(r"«([^»\n]{8,})»")),
    ("CURLY_QUOTES", re.compile(r"“([^”\n]{8,})”")),
]
for kind, pattern in patterns:
    for match in pattern.finditer(text):
        left = max(0, match.start() - 240)
        right = min(len(text), match.end() + 240)
        refs = sorted({module.normalize_ref(item.group(0)) for item in module.SCRIPTURE_RE.finditer(text[left:right])}, key=str.casefold)
        value = match.group(1)
        rows.append({
            "offset": match.start(),
            "section": section_for(match.start()),
            "kind": kind,
            "text": norm(value),
            "normalizedSha256": sha(value),
            "chars": len(norm(value)),
            "nearbyScripture": refs,
        })

for match in re.finditer(r"^\s*>\s?(\S.*)$", text, flags=re.M):
    left = max(0, match.start() - 240)
    right = min(len(text), match.end() + 240)
    refs = sorted({module.normalize_ref(item.group(0)) for item in module.SCRIPTURE_RE.finditer(text[left:right])}, key=str.casefold)
    value = match.group(1)
    rows.append({
        "offset": match.start(),
        "section": section_for(match.start()),
        "kind": "MARKDOWN_BLOCKQUOTE_LINE",
        "text": norm(value),
        "normalizedSha256": sha(value),
        "chars": len(norm(value)),
        "nearbyScripture": refs,
    })

rows.sort(key=lambda row: int(row["offset"]))
for index, row in enumerate(rows, start=1):
    row["index"] = index
    del row["offset"]

links = []
for match in module.ARTICLE_LINK_RE.finditer(text):
    links.append({
        "section": section_for(match.start()),
        "target": match.group(0),
        "context": norm(text[max(0, match.start()-100):min(len(text), match.end()+100)]),
    })

scan = module.scan_owner(module.p(str(PRODUCT_REL), "historical full III.1 owner"), product_root)
payload = {
    "authority": "HEART-III1-CITATION-DIAGNOSTIC-2026-08-04",
    "productCommit": PRODUCT_COMMIT,
    "productBlob": PRODUCT_BLOB,
    "counts": {
        "scriptureReferences": len(scan["scriptureReferences"]),
        "quotationSurfaces": scan["inlineQuotationSegments"] + scan["markdownBlockquotes"] + scan["htmlBlockquotes"],
        "externalLinks": len(scan["externalLinks"]),
        "internalArticleLinks": len(scan["internalArticleLinks"]),
    },
    "scriptureReferences": scan["scriptureReferences"],
    "quotationRows": rows,
    "internalLinks": links,
}
assert payload["counts"] == {
    "scriptureReferences": 30,
    "quotationSurfaces": 67,
    "externalLinks": 0,
    "internalArticleLinks": 4,
}
assert len(rows) == 67
print("III1_DIAGNOSTIC_JSON_BEGIN")
print(json.dumps(payload, ensure_ascii=False, separators=(",", ":")))
print("III1_DIAGNOSTIC_JSON_END")
