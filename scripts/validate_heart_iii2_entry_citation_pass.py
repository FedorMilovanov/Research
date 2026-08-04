#!/usr/bin/env python3
"""Validate the complete III.2 entry citation pass over both immutable R1 dossiers."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
BUILDER = ROOT / "scripts/build_heart_whole_book_citation_inventory.py"
EXEGESIS = ROOT / "СЕРИЯ СЕРДЦЕ/62_R1_REGENERATION_EXEGESIS.md"
SYSTEMATICS = ROOT / "СЕРИЯ СЕРДЦЕ/63_R1_REGENERATION_SYSTEMATICS.md"
READER = ROOT / "СЕРИЯ СЕРДЦЕ/121_READER_CHAPTER_III2_REGENERATION_2026-08-04.md"
ASSEMBLY = ROOT / "data/heart-iii2-reader-assembly-2026-08-04.json"
CURRENT = ROOT / "data/heart-entry-citation-pass-current-v7-2026-08-04.json"
RECEIPT = ROOT / "data/heart-iii2-citation-review-2026-08-04.json"
HUMAN = ROOT / "СЕРИЯ СЕРДЦЕ/123_III2_ENTRY_CITATION_PASS_2026-08-04.md"
WORKFLOW = ROOT / ".github/workflows/heart-reader-assembly.yml"
EXPECTED_BLOBS = {
    EXEGESIS: "d75117cf00cf0bb859fc40a67a26dca4c039ec57",
    SYSTEMATICS: "143b3477792f52a9fa5721431ff64e7ffb2a4d5a",
    READER: "a3f66d265cd66eff7187dcd5c511faf645833988",
    ASSEMBLY: "82e2a70977d67591c3a290248f102601c7c4d5dc",
    CURRENT: "86c932764ca2eba3bec726876f2cb73a0c78e762",
    BUILDER: "6e8fb1af57bc72d26a9ca91d5b84b1fec3de7f12",
}
EXPECTED_FULL_SHA = {
    EXEGESIS: "7ecab949786b371e93df8f68e91a51fdb5af2b77e5fbf6fad4998b8a54d17d29",
    SYSTEMATICS: "a382b72d7db263da03e073c6d2f032b4eef81caa3cfcc1008d30e817c1f2a0ae",
}
REFERENCE_HASH = "5383b18c99faadd09427126d461e1339326734eb5d107b850615defe2e2a186a"
BASE_MANIFEST_HASH = "80f1ee2c8d01200ff5a85a828f59a267ce1703f8f1971a7b0971f19f179788d6"
SECTION_SUMMARY_HASH = "0196b7d3a578e2e7b04acd56254c5a9f9bb6a39cb9f1b795a829f9edb8c49f12"
EXTERNAL_SET_HASH = "616381ad2cb3a43ebe2494e9eb838c9f22fbbe58ce7fba881078eed4badf8c08"
SECTION_ROLE_HASH = "9b0f7d2ee5255e0f733701cae6ba5f17adb97b85a673e9011fba6108aa55a576"
CLASSIFIED_HASH = "b486c76ec4bfc806dbab1389e64899a06a33509341120550aa1c8a45175b2fdf"
URL_DISPOSITION_HASH = "8b1430c850c6826dcab99cf7fc743e9c8b296983c3d56965a24eff5a5313c1f9"
EXEGETICAL = "EXEGETICAL_SCRIPTURE_OR_GRAMMATICAL_SURFACE"
ATTRIBUTED = "ATTRIBUTED_CONFESSIONAL_OR_THEOLOGICAL_WITNESS_SURFACE"
EDITORIAL = "EDITORIAL_SYSTEMATIC_OR_CAUTION_SURFACE"
HOLD_TERMS = [
    "НЕ ВЕРИФИЦИРОВАНО", "не верифицирован", "кандидат", "Открытые вопросы",
    "выходные данные установить", "не использовать", "опасност", "неточно",
    "не найден", "не подтверд", "сомнитель", "проверить атрибуцию", "HOLD",
    "NO-DIRECT-QUOTE", "перед публикацией", "желательно контрольное сличение",
]
VERIFIED_TERMS = [
    "ВЕРИФИЦИРОВАНО", "SAFE CLOSURE", "подтверждено", "точная фраза",
    "дословно", "проверен", "проверено",
]
EXEGESIS_EXEGETICAL = {
    "0. Фон: Иез. 36:25–27 — обетование, которое Никодим обязан был знать",
    "1. Ин. 3:3–8 — «должно вам родиться свыше»",
    "2. Иак. 1:18 — «восхотев, родил Он нас словом истины»",
    "3. 1 Пет. 1:22–25 — нетленное семя",
    "4. Тит. 3:4–7 — «баня возрождения»: честный разбор",
    "5. Еф. 2:1–10 — мёртвых оживил",
    "6. 1 Ин.: грамматика перфекта γεγέννηται — рождённость как состояние и её признаки",
}
EXEGESIS_ATTRIBUTED = {
    "Реформаторы", "Пуритане", "Баптисты (конфессиональная линия статьи)",
    "Современные консервативные", "Отцы (свидетель, не якорь)",
    "A. Джон Гилл, Exposition of the New Testament",
    "B. Конфессия и систематика (баптистская/реформатская)",
    "C. Современные консервативные комментаторы", "D. Реформаторы",
    "E. Пуритане и проповедники", "F. Отцы",
}
EXEGESIS_EDITORIAL = {
    "R1 · Возрождение — экзегетический фундамент (досье для статьи III.2 «Рождение свыше»)",
    "Задача и место в книге", "Рабочие тезисы", "Предлагаемая структура статьи III.2",
    "Чего избегать", "Открытые вопросы / что ещё копать",
}
SYSTEMATICS_EXEGETICAL = {
    "1. Иез. 36:26–27 — ВЗ-обетование, фон всего НЗ-учения",
    "2. Ин. 3:3–8 — рождение свыше", "3. Ин. 1:12–13 — рождены не от воли",
    "4. Еф. 2:1, 4–5 — оживление мёртвого",
    "5. Ин. 6:44, 65 — неспособность прийти без привлечения",
    "6. Деян. 16:14 — Лидия: открытое сердце",
    "7. Иак. 1:18 и 1 Пет. 1:23 — родил словом; семя нетленное",
    "8. Тит. 3:5 — «баня возрождения» (крещальный вопрос честно)",
    "9. 1 Ин. 2:29; 3:9; 4:7; 5:1, 4, 18 — грамматика перфекта: рождённость как состояние-причина",
    "10. 2 Кор. 5:17 — новое творение (текст Уитфилда)",
}
SYSTEMATICS_ATTRIBUTED = {
    "1. Исповедание: 1689 LBCF, глава 10 «Of Effectual Calling / О действенном призвании»",
    "2. Джон Гилл (баптист, 1697–1771) — A Body of Doctrinal Divinity (1769)",
    "3. Луис Беркхоф (реформат, 1873–1957) — Systematic Theology (1938/1941)",
    "4. Герман Бавинк (реформат, 1854–1921) — Reformed Dogmatics, т. 4; Saved by Grace",
    "5. Томас Бостон (пуританин-шотландец, 1676–1732) — Human Nature in its Fourfold State (1720)",
    "6. Проповедники", "7. Отцы (свидетель, не якорь)", "А. Исповедания",
    "Б. Джон Гилл", "В. Луис Беркхоф",
    "Г. Herman Bavinck — Reformed Dogmatics IV, chapter 1 (calling and regeneration)",
    "Д. У. Г. Т. Шедд (для узла immediate/mediate)", "Е. Томас Бостон",
    "Ж. Чарльз Сперджен", "Ж. Джордж Уитфилд", "З. Современные консервативные",
    "И. Бавинк (фрагменты)",
}
SYSTEMATICS_EDITORIAL = {
    "R1 (систематика). Возрождение: исповедание, догматика, проповедники — досье для III.2 «Рождение свыше»",
    "Задача и место в книге", "1. Монергизм vs синергизм",
    "2. Возрождение предшествует вере — аргументы (реформатская линия)",
    "3. Возрождение ≠ обращение (порядок и связь)",
    "4. Слово — средство ли в самом возрождении? (immediate/mediate, кратко)",
    "Рабочие тезисы III.2", "Возможная структура статьи", "Чего избегать",
    "Открытые вопросы / что ещё копать",
}
EXPECTED_CLASS_COUNTS = {
    EXEGETICAL: 175,
    ATTRIBUTED: 349,
    EDITORIAL: 85,
}
EXPECTED_URL_COUNTS = {
    "DOSSIER_VERIFIED_OR_SAFE_CLOSURE_SOURCE": 35,
    "DOSSIER_SUPPORT_RECORD_NO_READER_TRANSFER": 5,
    "DOSSIER_OPEN_OR_DIRECT_QUOTE_HOLD": 25,
    "DOSSIER_SOURCE_URL_REPAIR_REQUIRED": 2,
}
REPAIR_URLS = [
    "https://www.monergism.com/regeneration-6`",
    "https://www.reformedreader.org/ccc/1689lbc/english/Chapter10.htm**",
]
errors: list[str] = []


def require(value: bool, message: str) -> None:
    if not value:
        errors.append(message)


def read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"{path.relative_to(ROOT)}: {exc}")
        return {}
    require(isinstance(value, dict), f"{path.relative_to(ROOT)} must be an object")
    return value if isinstance(value, dict) else {}


def git_blob(path: Path) -> str:
    return subprocess.check_output(
        ["git", "hash-object", str(path.relative_to(ROOT))], cwd=ROOT, text=True
    ).strip()


def normalize(value: str) -> str:
    value = re.sub(r"<[^>]+>", " ", value)
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def digest(value: Any) -> str:
    payload = value if isinstance(value, str) else json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def heading_rows(text: str) -> list[dict[str, Any]]:
    return [
        {"offset": match.start(), "level": len(match.group(1)), "title": match.group(2).strip()}
        for match in re.finditer(r"(?m)^(#{1,4})\s+(.+?)\s*$", text)
    ]


def heading_for(rows: list[dict[str, Any]], offset: int) -> str:
    current = "frontmatter-or-introduction"
    for row in rows:
        if int(row["offset"]) > offset:
            break
        current = str(row["title"])
    return current


def extract_surfaces(text: str, owner: str, module: Any) -> list[dict[str, Any]]:
    headings = heading_rows(text)
    rows: list[dict[str, Any]] = []
    patterns = [
        ("RUSSIAN", re.compile(r"«([^»\n]{8,})»")),
        ("CURLY", re.compile(r"“([^”\n]{8,})”")),
        ("MD_BLOCK", re.compile(r"(?m)^\s*>\s?(\S.*)$")),
        ("HTML_BLOCK", re.compile(r"<blockquote[^>]*>(.*?)</blockquote>", re.S | re.I)),
    ]
    for surface_type, pattern in patterns:
        for match in pattern.finditer(text):
            value = normalize(match.group(1))
            left = max(0, match.start() - 300)
            right = min(len(text), match.end() + 300)
            nearby = sorted(
                {module.normalize_ref(item.group(0)) for item in module.SCRIPTURE_RE.finditer(text[left:right])},
                key=str.casefold,
            )
            rows.append({
                "owner": owner,
                "position": match.start(),
                "section": heading_for(headings, match.start()),
                "type": surface_type,
                "sha256": digest(value),
                "chars": len(value),
                "nearbyScripture": nearby,
            })
    rows.sort(key=lambda row: int(row["position"]))
    for index, row in enumerate(rows, start=1):
        row["ownerIndex"] = index
        del row["position"]
    return rows


def url_contexts(text: str, owner: str, url: str) -> list[dict[str, Any]]:
    headings = heading_rows(text)
    rows: list[dict[str, Any]] = []
    cursor = 0
    while True:
        offset = text.find(url, cursor)
        if offset < 0:
            break
        left = max(0, offset - 500)
        right = min(len(text), offset + len(url) + 500)
        context = normalize(text[left:right])
        rows.append({
            "owner": owner,
            "section": heading_for(headings, offset),
            "contextSha256": digest(context),
            "holdTerms": sorted(
                {term for term in HOLD_TERMS if term.casefold() in context.casefold()}, key=str.casefold
            ),
            "verifiedTerms": sorted(
                {term for term in VERIFIED_TERMS if term.casefold() in context.casefold()}, key=str.casefold
            ),
        })
        cursor = offset + 1
    return rows


def classify_url(contexts: list[dict[str, Any]], url: str) -> str:
    if url.endswith("`") or url.endswith("**"):
        return "DOSSIER_SOURCE_URL_REPAIR_REQUIRED"
    if any(row["holdTerms"] for row in contexts) or any(
        "Открытые вопросы" in str(row["section"]) for row in contexts
    ):
        return "DOSSIER_OPEN_OR_DIRECT_QUOTE_HOLD"
    if any(row["verifiedTerms"] for row in contexts):
        return "DOSSIER_VERIFIED_OR_SAFE_CLOSURE_SOURCE"
    return "DOSSIER_SUPPORT_RECORD_NO_READER_TRANSFER"


def quote_count(scan: dict[str, Any]) -> int:
    return scan["inlineQuotationSegments"] + scan["markdownBlockquotes"] + scan["htmlBlockquotes"]


parser = argparse.ArgumentParser()
parser.add_argument("--product-root", type=Path, required=True)
args = parser.parse_args()
product_root = args.product_root.resolve()

for path, expected in EXPECTED_BLOBS.items():
    require(path.is_file(), f"immutable witness missing: {path.relative_to(ROOT)}")
    if path.is_file():
        require(git_blob(path) == expected, f"immutable witness blob drift: {path.relative_to(ROOT)}")

texts = {
    "R1_EXEGESIS": EXEGESIS.read_text(encoding="utf-8"),
    "R1_SYSTEMATICS": SYSTEMATICS.read_text(encoding="utf-8"),
}
for path, expected in EXPECTED_FULL_SHA.items():
    require(digest(path.read_text(encoding="utf-8")) == expected, f"source full SHA drift: {path.name}")

spec = importlib.util.spec_from_file_location("heart_inventory", BUILDER)
assert spec is not None and spec.loader is not None
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
scans = {
    "R1_EXEGESIS": module.scan_owner(module.r(str(EXEGESIS.relative_to(ROOT)), "III.2 R1 exegesis owner"), product_root),
    "R1_SYSTEMATICS": module.scan_owner(module.r(str(SYSTEMATICS.relative_to(ROOT)), "III.2 R1 systematics owner"), product_root),
}
reader_scan = module.scan_owner(module.r(str(READER.relative_to(ROOT)), "III.2 reader"), product_root)

require(len(scans["R1_EXEGESIS"]["scriptureReferences"]) == 64, "III.2 exegesis Scripture count drift")
require(quote_count(scans["R1_EXEGESIS"]) == 230, "III.2 exegesis quotation count drift")
require(len(scans["R1_EXEGESIS"]["externalLinks"]) == 37, "III.2 exegesis external-link count drift")
require(len(scans["R1_SYSTEMATICS"]["scriptureReferences"]) == 74, "III.2 systematics Scripture count drift")
require(quote_count(scans["R1_SYSTEMATICS"]) == 379, "III.2 systematics quotation count drift")
require(len(scans["R1_SYSTEMATICS"]["externalLinks"]) == 39, "III.2 systematics external-link count drift")

union_refs = sorted(
    set(scans["R1_EXEGESIS"]["scriptureReferences"]) | set(scans["R1_SYSTEMATICS"]["scriptureReferences"]),
    key=str.casefold,
)
union_external = sorted(
    set(scans["R1_EXEGESIS"]["externalLinks"]) | set(scans["R1_SYSTEMATICS"]["externalLinks"]),
    key=str.casefold,
)
union_internal = sorted(
    set(scans["R1_EXEGESIS"]["internalArticleLinks"]) | set(scans["R1_SYSTEMATICS"]["internalArticleLinks"]),
    key=str.casefold,
)
require(len(union_refs) == 115 and digest(union_refs) == REFERENCE_HASH, "III.2 Scripture union/hash drift")
require(len(union_external) == 67 and digest(union_external) == EXTERNAL_SET_HASH, "III.2 external URL union/hash drift")
require(union_internal == ["/articles/onsite/"], "III.2 detected internal path drift")

surfaces = extract_surfaces(texts["R1_EXEGESIS"], "R1_EXEGESIS", module) + extract_surfaces(
    texts["R1_SYSTEMATICS"], "R1_SYSTEMATICS", module
)
require(len(surfaces) == 609, "III.2 deterministic surface decomposition drift")
base_manifest = [
    {key: row[key] for key in (
        "owner", "ownerIndex", "section", "type", "sha256", "chars", "nearbyScripture"
    )}
    for row in surfaces
]
require(digest(base_manifest) == BASE_MANIFEST_HASH, "III.2 base surface manifest drift")
section_buckets: dict[str, dict[str, Any]] = {}
for row in surfaces:
    key = f"{row['owner']}::{row['section']}"
    bucket = section_buckets.setdefault(key, {"surfaces": 0, "types": Counter(), "withNearbyScripture": 0})
    bucket["surfaces"] += 1
    bucket["types"][row["type"]] += 1
    bucket["withNearbyScripture"] += int(bool(row["nearbyScripture"]))
section_summary = {
    key: {
        "surfaces": value["surfaces"],
        "types": dict(sorted(value["types"].items())),
        "withNearbyScripture": value["withNearbyScripture"],
    }
    for key, value in sorted(section_buckets.items())
}
require(digest(section_summary) == SECTION_SUMMARY_HASH, "III.2 section summary drift")

section_role_map: dict[str, str] = {}
for section in EXEGESIS_EXEGETICAL:
    section_role_map[f"R1_EXEGESIS::{section}"] = EXEGETICAL
for section in EXEGESIS_ATTRIBUTED:
    section_role_map[f"R1_EXEGESIS::{section}"] = ATTRIBUTED
for section in EXEGESIS_EDITORIAL:
    section_role_map[f"R1_EXEGESIS::{section}"] = EDITORIAL
for section in SYSTEMATICS_EXEGETICAL:
    section_role_map[f"R1_SYSTEMATICS::{section}"] = EXEGETICAL
for section in SYSTEMATICS_ATTRIBUTED:
    section_role_map[f"R1_SYSTEMATICS::{section}"] = ATTRIBUTED
for section in SYSTEMATICS_EDITORIAL:
    section_role_map[f"R1_SYSTEMATICS::{section}"] = EDITORIAL
require(set(section_role_map) == set(section_summary), "III.2 section role map is not exhaustive")
require(digest(section_role_map) == SECTION_ROLE_HASH, "III.2 section role map hash drift")
classified: list[dict[str, Any]] = []
class_counts: Counter[str] = Counter()
owner_class_counts: dict[str, Counter[str]] = {
    "R1_EXEGESIS": Counter(), "R1_SYSTEMATICS": Counter()
}
for global_index, row in enumerate(surfaces, start=1):
    role = section_role_map[f"{row['owner']}::{row['section']}"]
    class_counts[role] += 1
    owner_class_counts[row["owner"]][role] += 1
    classified.append({
        "globalIndex": global_index,
        "owner": row["owner"],
        "ownerIndex": row["ownerIndex"],
        "section": row["section"],
        "type": row["type"],
        "sha256": row["sha256"],
        "chars": row["chars"],
        "role": role,
    })
require(dict(class_counts) == EXPECTED_CLASS_COUNTS, "III.2 quotation taxonomy count drift")
require(dict(owner_class_counts["R1_EXEGESIS"]) == {
    EXEGETICAL: 117, ATTRIBUTED: 78, EDITORIAL: 35
}, "III.2 exegesis taxonomy drift")
require(dict(owner_class_counts["R1_SYSTEMATICS"]) == {
    EXEGETICAL: 58, ATTRIBUTED: 271, EDITORIAL: 50
}, "III.2 systematics taxonomy drift")
require(digest(classified) == CLASSIFIED_HASH, "III.2 classified manifest drift")

url_manifest: list[dict[str, Any]] = []
for url in union_external:
    contexts: list[dict[str, Any]] = []
    for owner in ("R1_EXEGESIS", "R1_SYSTEMATICS"):
        if url in scans[owner]["externalLinks"]:
            contexts.extend(url_contexts(texts[owner], owner, url))
    url_manifest.append({
        "url": url,
        "owners": sorted({str(row["owner"]) for row in contexts}),
        "status": classify_url(contexts, url),
        "occurrences": len(contexts),
        "sections": sorted({f"{row['owner']}::{row['section']}" for row in contexts}, key=str.casefold),
        "contexts": contexts,
        "readerTransfer": False,
        "directQuoteBulkApproval": False,
    })
url_counts = Counter(row["status"] for row in url_manifest)
require(dict(url_counts) == EXPECTED_URL_COUNTS, "III.2 URL disposition count drift")
require(sum(int(row["occurrences"]) for row in url_manifest) == 97, "III.2 URL occurrence count drift")
require([row["url"] for row in url_manifest if row["status"] == "DOSSIER_SOURCE_URL_REPAIR_REQUIRED"] == REPAIR_URLS, "III.2 malformed URL repair set drift")
require(digest(url_manifest) == URL_DISPOSITION_HASH, "III.2 URL disposition manifest drift")

source_combined = texts["R1_EXEGESIS"] + "\n" + texts["R1_SYSTEMATICS"]
require(source_combined.count("/articles/onsite/") == 2, "III.2 onsite path occurrence drift")
for containing in (
    "https://www.monergism.com/thethreshold/articles/onsite/monergism_grid.html",
    "https://www.monergism.com/thethreshold/articles/onsite/regeneration_grudem.html",
):
    require(containing in source_combined, f"III.2 false-positive containing URL missing: {containing}")
require(not (product_root / "src/content/articles/onsite.mdx").exists(), "unexpected Product onsite target now exists on pinned snapshot")

require(len(reader_scan["scriptureReferences"]) == 25, "III.2 reader Scripture count drift")
require(quote_count(reader_scan) == 0, "III.2 reader quotation detected")
require(len(reader_scan["externalLinks"]) == 0, "III.2 reader external link detected")
require(len(reader_scan["internalArticleLinks"]) == 0, "III.2 reader internal link detected")
require(reader_scan["footnoteDefinitions"] == 0, "III.2 reader footnote detected")
require(reader_scan["sourceHeadings"] == [], "III.2 reader source heading detected")

current = read_json(CURRENT)
assembly = read_json(ASSEMBLY)
receipt = read_json(RECEIPT)
require(current.get("authorityId") == "HEART-ENTRY-CITATION-PASS-CURRENT-V7-2026-08-04", "current V7 authority drift")
require(current.get("currentCounts", {}).get("entryCitationPassComplete") == 10, "current V7 completion count drift")
require(current.get("currentCounts", {}).get("assembledReaderEntries") == 10, "current V7 reader count drift")
require(current.get("currentCounts", {}).get("dossierUrlHoldsRetained") == 15, "current V7 dossier hold count drift")
require(assembly.get("authorityId") == "HEART-III2-READER-ASSEMBLY-2026-08-04", "III.2 assembly authority drift")
require(assembly.get("effectiveCounts", {}).get("assembledReaders") == 11, "III.2 assembly reader count drift")
require(assembly.get("effectiveCounts", {}).get("entryCitationPassComplete") == 10, "III.2 assembly pre-review count drift")

require(receipt.get("authorityId") == "HEART-III2-CITATION-REVIEW-2026-08-04", "III.2 receipt authority drift")
require(receipt.get("status") == "III2_ENTRY_CITATION_PASS_COMPLETE_READER_REVIEWED_ZERO_NEW_DIRECT_QUOTES", "III.2 receipt status drift")
require(receipt.get("entry") == {"order": 7, "id": "HEART-BOOK-III2", "label": "III.2 Рождение свыше и обновление"}, "III.2 receipt entry drift")
require(receipt.get("historicalUnion") == {
    "ownerSurfaces": 2,
    "scriptureReferences": 115,
    "quotationSurfaces": 609,
    "externalLinks": 67,
    "ownerUrlRecords": 76,
    "internalArticleLinksDetected": 1,
    "scriptureReferenceSetSha256": REFERENCE_HASH,
    "baseSurfaceManifestSha256": BASE_MANIFEST_HASH,
    "sectionSummarySha256": SECTION_SUMMARY_HASH,
    "externalLinkSetSha256": EXTERNAL_SET_HASH,
}, "III.2 receipt historical union drift")
classification = receipt.get("quotationClassification", {})
require(classification.get("classes") == EXPECTED_CLASS_COUNTS, "III.2 receipt class counts drift")
require(classification.get("byOwner") == {
    "R1_EXEGESIS": {EXEGETICAL: 117, ATTRIBUTED: 78, EDITORIAL: 35},
    "R1_SYSTEMATICS": {EXEGETICAL: 58, ATTRIBUTED: 271, EDITORIAL: 50},
}, "III.2 receipt owner taxonomy drift")
require(classification.get("total") == 609, "III.2 receipt taxonomy total drift")
require(classification.get("sectionRoleMapSha256") == SECTION_ROLE_HASH, "III.2 receipt role-map hash drift")
require(classification.get("classifiedManifestSha256") == CLASSIFIED_HASH, "III.2 receipt classified hash drift")
require(classification.get("bulkDirectQuoteApproval") is False and classification.get("readerTransfer") == 0, "III.2 receipt quote boundary weakened")
external = receipt.get("externalLinkDisposition", {})
require(external.get("unique") == 67 and external.get("ownerUrlRecords") == 76 and external.get("occurrences") == 97, "III.2 receipt URL totals drift")
require(external.get("counts") == EXPECTED_URL_COUNTS, "III.2 receipt URL counts drift")
require(external.get("sourceUrlRepairsRequired") == REPAIR_URLS, "III.2 receipt URL repair set drift")
require(external.get("urlDispositionManifestSha256") == URL_DISPOSITION_HASH, "III.2 receipt URL manifest hash drift")
require(external.get("readerTransfer") == 0 and external.get("newDirectQuotesApproved") == 0, "III.2 receipt URL transfer boundary weakened")
internal = receipt.get("internalPathDisposition", {})
require(internal.get("detected") == "/articles/onsite/", "III.2 receipt internal detection drift")
require(internal.get("status") == "EXTERNAL_URL_PATH_FRAGMENT_FALSE_POSITIVE", "III.2 receipt internal disposition drift")
require(internal.get("detectedOccurrences") == 2 and internal.get("unresolvedInternalPathsAdded") == 0, "III.2 receipt internal count drift")
review = receipt.get("readerReview", {})
require(review.get("gitBlob") == EXPECTED_BLOBS[READER] and review.get("wordCount") == 1718, "III.2 receipt reader witness drift")
require(review.get("scriptureReferences") == 25, "III.2 receipt reader Scripture drift")
for key in (
    "quotationSurfaces", "externalLinks", "internalArticleLinks", "footnoteDefinitions",
    "sourceHeadings", "historicalDossierQuotationTransfer", "historicalDossierLinkTransfer",
    "newDirectQuotesApproved",
):
    require(review.get(key) == 0, f"III.2 receipt reader {key} drift")
require(receipt.get("retainedHoldsAndRepairs") == {
    "productSourceRepairsRequired": 4,
    "priorPart2DossierUrlHoldsRetained": 15,
    "iii2DossierUrlHoldsAdded": 25,
    "totalDossierUrlHoldsRetained": 40,
    "iii2DossierSourceUrlRepairsRequired": 2,
    "part2UnresolvedInternalPathsRetained": 1,
    "iii2UnresolvedInternalPathsAdded": 0,
}, "III.2 retained backlog drift")
require(receipt.get("effectiveState") == {
    "previous": "ASSEMBLED_READER_CITATION_OPEN",
    "current": "ENTRY_CITATION_PASS_COMPLETE",
    "entryCitationPassComplete": True,
    "assembledReaderCitationReviewComplete": True,
}, "III.2 effective state drift")
require(receipt.get("effectiveCounts") == {
    "finalBookEntries": 18,
    "entryCitationPassComplete": 11,
    "entryCitationPassOpen": 7,
    "assembledReaders": 11,
    "assembledReaderCitationReviewsComplete": 11,
    "missingStandaloneFinalReaders": 7,
    "productSourceOnlyEntries": 3,
    "researchDossierOnlyEntries": 4,
    "productSourceRepairsRequired": 4,
    "dossierUrlHoldsRetained": 40,
    "dossierSourceUrlRepairsRequired": 2,
    "unresolvedInternalPathsRetained": 1,
    "newDirectQuotesApproved": 0,
}, "III.2 effective count drift")
boundary = receipt.get("publicationBoundary", {})
require(boundary.get("iii2EntryCitationPassComplete") is True, "III.2 receipt pass incomplete")
require(boundary.get("allCurrentlyAssembledReadersCitationReviewed") is True, "III.2 receipt review incomplete")
for key in (
    "currentV8CompositionComplete", "wholeBookReaderAssemblyComplete", "wholeBookCitationPassComplete",
    "wholeBookTransitionDedupPassComplete", "wholeBookLineEditComplete", "manuscriptBundleComplete",
    "productReleaseComplete", "productSourceRepairsComplete", "dossierUrlHoldsResolved",
    "dossierSourceUrlRepairsComplete", "unresolvedInternalPathsResolved",
):
    require(boundary.get(key) is False, f"III.2 publication boundary weakened: {key}")
require(boundary.get("newDirectQuotesApproved") == 0, "III.2 publication quote boundary drift")

human = HUMAN.read_text(encoding="utf-8") if HUMAN.is_file() else ""
for marker in (
    "HEART-III2-CITATION-REVIEW-2026-08-04", "115 / 115", "609 / 609", "67 / 67",
    "175", "349", "85", "35", "5", "25", "2",
    "ENTRY CITATION PASSES COMPLETE = 11 / 18", "ASSEMBLED READER CITATION REVIEWS = 11 / 11",
    "DOSSIER URL HOLDS RETAINED = 40", "DOSSIER SOURCE URL REPAIRS REQUIRED = 2",
    "CURRENT V8 COMPOSITION COMPLETE = FALSE", "WHOLE-BOOK CITATION PASS = OPEN",
    "PRODUCT RELEASE = NOT CLAIMED",
):
    require(marker in human, f"III.2 human authority marker missing: {marker}")
require(not (ROOT / "scripts/diagnose_heart_iii2_citation.py").exists(), "temporary III.2 diagnostic script retained")
require(not (ROOT / ".github/workflows/diagnose-heart-iii2-citation.yml").exists(), "temporary III.2 diagnostic workflow retained")
workflow = WORKFLOW.read_text(encoding="utf-8") if WORKFLOW.is_file() else ""
require("validate_heart_iii2_entry_citation_pass.py" in workflow, "permanent III.2 citation gate missing")
require("diagnose_heart_iii2_citation.py" not in workflow, "diagnostic III.2 step retained in permanent workflow")

if errors:
    print(f"Heart III.2 entry citation pass: FAIL ({len(errors)})", file=sys.stderr)
    for error in errors:
        print(f"- {error}", file=sys.stderr)
    raise SystemExit(1)

print("Heart III.2 entry citation pass: PASS")
print("- historical: 115 Scripture / 609 classified surfaces / 67 unique external / 1 false-positive internal")
print("- taxonomy: 175 exegetical / 349 attributed / 85 editorial")
print("- URLs: 35 verified / 5 support / 25 hold / 2 repair; 97 occurrences")
print("- reader: 25 Scripture / 0 quote-link-footnote-source surfaces")
print("- effective state: 11/18 complete; reviews 11/11; V8 remains separate")
