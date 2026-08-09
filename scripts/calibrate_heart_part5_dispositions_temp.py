#!/usr/bin/env python3
"""Temporary read-only disposition calibration for Part V."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
BUILDER = ROOT / "scripts/build_heart_whole_book_citation_inventory.py"
PART2 = ROOT / "data/heart-part2-citation-review-2026-08-04.json"
R5 = ROOT / "СЕРИЯ СЕРДЦЕ/67_R5_TWO_STRUGGLES.md"
PRODUCT_REL = Path("src/components/article-pilots/rimlyanam7/Rimlyanam7Body.astro")
PRODUCT_COMMIT = "0fbe7d1ead9ebd1bea867418e254da438ec63329"

PRODUCT_ROLE_SECTIONS = {
    "EXEGETICAL_SCRIPTURE_OR_DOCTRINAL_SURFACE": [
        "Коротко",
        "I. В чём именно вопрос",
        "II. Римлянам 6–8: три звена одной цепи",
        "III. Что именно повторяется в Рим. 7:14–25",
        "IV. Позиция 1: Павел описывает верующего",
        "V. Позиция 2: Павел описывает человека под законом до освобождения Духом",
        "VIII. Почему я считаю, что Рим. 7 применим к верующему",
        "IX. Пастырский вывод: кому Рим. 7 утешение, а кому предупреждение",
        "Твёрдо, но не дубинкой",
        "Как отличить в себе",
    ],
    "ATTRIBUTED_WITNESS_OR_SOURCE_BANK_SURFACE": [
        "VI. Ллойд-Джонс: не зрелый христианин и не обычный невозрождённый",
        "VII. TMSJ / Джей Стрит: старозаветная борьба глазами Нового Завета",
        "Источники и сверка",
    ],
    "EDITORIAL_CHROME_OR_NAVIGATION_SURFACE": ["frontmatter-or-introduction", "Читайте также"],
}
R5_ROLE_SECTIONS = {
    "EXEGETICAL_SCRIPTURE_OR_LEXICAL_SURFACE": [
        "1. Лк. 18:9–14 — фарисей и мытарь: две борьбы на молитве (центральный текст статьи)",
        "2. 2 Кор. 7:10–11 — две печали: анатомия «плода поражений»",
        "3. Рим. 2:14–15 — совесть есть у всех: почему борьба совести реальна",
        "4. Рим. 7:22 + 8:13 — отличительные глаголы возрождённой борьбы",
        "5. Гал. 5:16–25 — сама борьба как признак Духа; плод Духа как признак победы",
        "6. 1 Ин. — направление пути (ось 6): рождённость видна по вектору, не по безупречности",
        "7. Библейские пары-кейсы (материал для живой ткани статьи)",
        "8. Мф. 26:41 / Owen: искушение и «вхождение в искушение» (для оси 2 — оружие)",
    ],
    "ATTRIBUTED_WITNESS_OR_QUOTE_BANK_SURFACE": [
        "1. Matthew Mead, «The Almost Christian Discovered» (1661) — обязательный источник статьи",
        "2. John Owen, «Of the Mortification of Sin in Believers» (1656) — гл. 2, 5–8",
        "3. John Owen, «Of Temptation» (1658) — оружие возрождённой борьбы",
        "4. Кратко (уже верифицировано в корпусе, использовать перекрёстно)",
        "Б. Реформаторы",
        "В. Баптисты",
        "Г. Современные консервативные",
        "Д. Отцы (свидетель, не догматический якорь)",
        "Е. Jonathan Edwards, «A Treatise Concerning Religious Affections» (1746) — полные списки",
        "Ж. Гордость морального победителя vs смирение побеждающего Духом (сводный узел)",
        "Цитатный банк (полные источники и статус верификации)",
    ],
    "EDITORIAL_STRUCTURAL_OR_CAUTION_SURFACE": [
        "R5 — Две борьбы: борьба совести и борьба Духа (различение) — досье для статьи V.3",
        "Задача и место в книге",
        "Предлагаемая структура (H2)",
        "Строки-якоря серии (обязательны, из R7/R8)",
        "Чего избегать (guardrails)",
        "Открытые вопросы / что ещё копать",
    ],
}


def sha(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def normalize(value: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", value)).strip()


def headings(text: str) -> list[tuple[int, str]]:
    rows = [(m.start(), normalize(m.group(2))) for m in re.finditer(r"(?m)^(#{1,4})\s+(.+?)\s*$", text)]
    rows += [(m.start(), normalize(m.group(1))) for m in re.finditer(r"<h[2-4]\b[^>]*>(.*?)</h[2-4]>", text, re.I | re.S)]
    return sorted(rows)


def section_at(rows: list[tuple[int, str]], pos: int) -> str:
    current = "frontmatter-or-introduction"
    for at, title in rows:
        if at > pos:
            break
        current = title
    return current


def quote_sections(text: str) -> list[str]:
    hs = headings(text)
    rows: list[tuple[int, str]] = []
    for pattern in (r"«([^»\n]{8,})»", r"“([^”\n]{8,})”", r"(?m)^\s*>\s?(\S.*)$", r"<blockquote[^>]*>(.*?)</blockquote>"):
        for m in re.finditer(pattern, text, re.I | re.S if "blockquote" in pattern else 0):
            rows.append((m.start(), section_at(hs, m.start())))
    return [section for _, section in sorted(rows)]


def classify_roles(sections: list[str], mapping: dict[str, list[str]]) -> tuple[dict[str, int], list[str]]:
    reverse = {section: role for role, values in mapping.items() for section in values}
    missing = sorted({section for section in sections if section not in reverse}, key=str.casefold)
    counts = Counter(reverse[section] for section in sections if section in reverse)
    return dict(sorted(counts.items())), missing


def url_registry(text: str, urls: list[str], method: dict[str, Any]) -> list[dict[str, Any]]:
    hs = headings(text)
    rows: list[dict[str, Any]] = []
    for raw_url in urls:
        canonical = raw_url[:-1] if raw_url.endswith('`') else raw_url
        occurrences: list[dict[str, Any]] = []
        cursor = 0
        while True:
            pos = text.find(raw_url, cursor)
            if pos < 0:
                break
            left = max(0, pos - 500)
            right = min(len(text), pos + len(raw_url) + 500)
            context = normalize(text[left:right])
            occurrences.append({
                "section": section_at(hs, pos),
                "contextSha256": hashlib.sha256(context.encode()).hexdigest(),
                "holdTerms": sorted([term for term in method["holdTerms"] if term.casefold() in context.casefold()], key=str.casefold),
                "verifiedTerms": sorted([term for term in method["verifiedTerms"] if term.casefold() in context.casefold()], key=str.casefold),
            })
            cursor = pos + 1
        if raw_url.endswith('`'):
            status = "MARKDOWN_CODE_DELIMITER_SCANNER_ARTIFACT"
        elif any(o["holdTerms"] for o in occurrences):
            status = "DOSSIER_OPEN_OR_DIRECT_QUOTE_HOLD"
        elif any(o["verifiedTerms"] for o in occurrences):
            status = "DOSSIER_VERIFIED_OR_SAFE_CLOSURE_SOURCE"
        else:
            status = "DOSSIER_SUPPORT_RECORD_NO_READER_TRANSFER"
        rows.append({
            "rawUrl": raw_url,
            "canonicalUrl": canonical,
            "status": status,
            "occurrences": len(occurrences),
            "sections": sorted({o["section"] for o in occurrences}, key=str.casefold),
            "contexts": occurrences,
            "readerTransfer": False,
            "bulkDirectQuoteApproval": False,
        })
    return rows


parser = argparse.ArgumentParser()
parser.add_argument("--product-root", required=True)
args = parser.parse_args()
product_root = Path(args.product_root).resolve()
if subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=product_root, text=True).strip() != PRODUCT_COMMIT:
    raise SystemExit("Product snapshot drift")

spec = importlib.util.spec_from_file_location("heart_inventory", BUILDER)
assert spec is not None and spec.loader is not None
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

product_text = (product_root / PRODUCT_REL).read_text(encoding="utf-8")
r5_text = R5.read_text(encoding="utf-8")
product_scan = module.scan_owner(module.p(str(PRODUCT_REL), "native Romans 7"), product_root)
r5_scan = module.scan_owner(module.r(str(R5.relative_to(ROOT)), "R5"), product_root)
product_role_counts, product_missing = classify_roles(quote_sections(product_text), PRODUCT_ROLE_SECTIONS)
r5_role_counts, r5_missing = classify_roles(quote_sections(r5_text), R5_ROLE_SECTIONS)
if product_missing or r5_missing:
    raise SystemExit(f"unmapped quote sections: product={product_missing} r5={r5_missing}")
part2 = json.loads(PART2.read_text(encoding="utf-8"))
method = part2["externalLinkReview"]["method"]
r5_urls = sorted(r5_scan["externalLinks"], key=str.casefold)
r5_url_registry = url_registry(r5_text, r5_urls, method)
product_urls = [
    {"url": url, "status": "NON_CITATION_UI_OR_SCHEMA_URL", "readerTransfer": False}
    for url in sorted(product_scan["externalLinks"], key=str.casefold)
]
result = {
    "productRoleCounts": product_role_counts,
    "productRoleMapSha256": sha(PRODUCT_ROLE_SECTIONS),
    "r5RoleCounts": r5_role_counts,
    "r5RoleMapSha256": sha(R5_ROLE_SECTIONS),
    "r5UrlStatusCounts": dict(sorted(Counter(row["status"] for row in r5_url_registry).items())),
    "r5UrlRegistrySha256": sha(r5_url_registry),
    "r5UrlOccurrences": sum(row["occurrences"] for row in r5_url_registry),
    "productUrlRegistrySha256": sha(product_urls),
    "productUrlStatusCounts": dict(sorted(Counter(row["status"] for row in product_urls).items())),
    "r5MalformedScannerArtifacts": [row["rawUrl"] for row in r5_url_registry if row["status"] == "MARKDOWN_CODE_DELIMITER_SCANNER_ARTIFACT"],
}
print("HEART_PART5_DISPOSITION_CALIBRATION=" + json.dumps(result, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
print("Part V disposition calibration: FAIL (expected red-first calibration)")
raise SystemExit(1)
