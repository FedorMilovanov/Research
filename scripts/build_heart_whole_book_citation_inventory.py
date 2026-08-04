#!/usr/bin/env python3
"""Build/check the read-only Heart whole-book citation/reference inventory."""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data/heart-whole-book-citation-inventory-2026-08-04.json"
RESEARCH_SNAPSHOT = "92bb7c3708b77f6e8344e8c29261d93ecea4debb"
PRODUCT_COMMIT = "0fbe7d1ead9ebd1bea867418e254da438ec63329"

BOOK_TOKEN = r"(?:[1-4]\s*)?(?:Быт(?:ие)?|Исх(?:од)?|Лев(?:ит)?|Чис(?:ла)?|Втор(?:озаконие)?|Иис(?:ус)?\s*Нав(?:ин)?|Суд(?:ьи)?|Руфь|Цар(?:ств)?|Пар(?:алипоменон)?|Езд(?:ра)?|Неем(?:ия)?|Есф(?:ирь)?|Иов|Пс(?:алом|алмы)?|Притч(?:и)?|Еккл(?:есиаст)?|Песн(?:ь\s*Песней)?|Ис(?:айя)?|Иер(?:емия)?|Плач|Иез(?:екииль)?|Дан(?:иил)?|Ос(?:ия)?|Иоил|Ам(?:ос)?|Авд(?:ий)?|Ион(?:а)?|Мих(?:ей)?|Наум|Авв(?:акум)?|Соф(?:ония)?|Агг(?:ей)?|Зах(?:ария)?|Мал(?:ахия)?|Мф|Матф(?:ей)?|Мк|Марк|Лк|Лук(?:а)?|Ин|Иоанн(?:а)?|Деян(?:ия)?|Рим(?:лянам)?|Кор(?:инфянам)?|Гал(?:атам)?|Еф(?:есянам)?|Флп|Филиппийцам|Кол(?:оссянам)?|Фес(?:салоникийцам)?|Тим(?:офею)?|Тит(?:у)?|Флм|Филимону|Евр(?:еям)?|Иак(?:ова)?|Пет(?:ра)?|Иуд(?:ы)?|Откр(?:овение)?|Gen(?:esis)?|Exod(?:us)?|Lev(?:iticus)?|Num(?:bers)?|Deut(?:eronomy)?|Josh(?:ua)?|Judg(?:es)?|Ruth|Sam(?:uel)?|Kings?|Chron(?:icles)?|Ezra|Neh(?:emiah)?|Esth(?:er)?|Job|Ps(?:alm|alms)?|Prov(?:erbs)?|Eccl(?:esiastes)?|Song(?:\s+of\s+Songs)?|Isa(?:iah)?|Jer(?:emiah)?|Lam(?:entations)?|Ezek(?:iel)?|Dan(?:iel)?|Hos(?:ea)?|Joel|Amos|Obad(?:iah)?|Jonah|Mic(?:ah)?|Nah(?:um)?|Hab(?:akkuk)?|Zeph(?:aniah)?|Hag(?:gai)?|Zech(?:ariah)?|Mal(?:achi)?|Matt(?:hew)?|Mark|Luke|John|Acts|Rom(?:ans)?|Cor(?:inthians)?|Gal(?:atians)?|Eph(?:esians)?|Phil(?:ippians)?|Col(?:ossians)?|Thess(?:alonians)?|Tim(?:othy)?|Titus|Philem(?:on)?|Heb(?:rews)?|James|Peter|Jude|Rev(?:elation)?)"
SCRIPTURE_RE = re.compile(
    rf"(?<![\w/]){BOOK_TOKEN}\.?\s+\d+(?:(?::|\.)\d+(?:[a-zа-я]?)(?:[–—-]\d+[a-zа-я]?)?)?(?:[–—-]\d+(?:(?::|\.)\d+)?)?(?:\s*[,;]\s*\d+(?:(?::|\.)\d+)?)?",
    re.IGNORECASE,
)
URL_RE = re.compile(r"https?://[^\s<>()\]\[\"']+")
ARTICLE_LINK_RE = re.compile(r"/articles/[a-z0-9-]+/")
FOOTNOTE_RE = re.compile(r"^\[\^[^\]]+\]:", re.MULTILINE)
SOURCE_HEADING_RE = re.compile(
    r"^#{1,6}\s+(.{0,120}(?:источник|сверк|литератур|примечан|bibliograph|source|references?).{0,120})$",
    re.IGNORECASE | re.MULTILINE,
)
RUSSIAN_QUOTE_RE = re.compile(r"«[^»\n]{8,}»")
CURLY_QUOTE_RE = re.compile(r"“[^”\n]{8,}”")
HTML_BLOCKQUOTE_RE = re.compile(r"<blockquote\b", re.IGNORECASE)
MARKDOWN_BLOCKQUOTE_RE = re.compile(r"^\s*>\s?\S", re.MULTILINE)


def r(path: str, role: str, sections: list[str] | None = None) -> dict[str, Any]:
    return {"surface": "research", "path": path, "role": role, "sections": sections or []}


def p(path: str, role: str, sections: list[str] | None = None) -> dict[str, Any]:
    return {"surface": "product", "path": path, "role": role, "sections": sections or []}


ENTRIES: list[dict[str, Any]] = [
    {
        "order": 1,
        "id": "HEART-BOOK-I1",
        "label": "I.1 Что Библия называет сердцем",
        "state": "PRODUCT_SOURCE_ONLY",
        "manuscripts": [p("src/content/articles/chto-bibliya-nazyvaet-serdcem.mdx", "primary Product manuscript")],
        "support": [],
    },
    {
        "order": 2,
        "id": "HEART-BOOK-I2",
        "label": "I.2 Сердце в Эдеме",
        "state": "ASSEMBLED_READER",
        "manuscripts": [r("СЕРИЯ СЕРДЦЕ/79_READER_CHAPTER_I2_HEART_IN_EDEN_2026-08-02.md", "assembled reader")],
        "support": [r("СЕРИЯ СЕРДЦЕ/75_P0_EDEN_HEART_CREATED_AND_FALLEN_2026-08-02.md", "P0 evidence dossier")],
    },
    {
        "order": 3,
        "id": "HEART-BOOK-I3",
        "label": "I.3 Падшее сердце: Иеремия 17",
        "state": "PRODUCT_SOURCE_ONLY",
        "manuscripts": [p("src/content/articles/krajne-li-isporcheno-serdce.mdx", "primary Product manuscript")],
        "support": [],
    },
    {
        "order": 4,
        "id": "HEART-BOOK-I4",
        "label": "I.4 Внутренний человек и телесная жизнь",
        "state": "PRODUCT_SOURCE_ONLY",
        "manuscripts": [p("src/content/articles/serdce-i-telo.mdx", "primary Product manuscript")],
        "support": [
            p("src/content/articles/chto-bibliya-nazyvaet-serdcem.mdx", "whole-person definition support"),
            r("СЕРИЯ СЕРДЦЕ/60_V81_JAY_ADAMS_PRIMARY_SOURCE_DEEPENING.md", "inner-person and embodied-habit boundary"),
            r("СЕРИЯ СЕРДЦЕ/61_V82_PSYCHOTROPIC_MEDICATION_BODY_SOUL_BIBLICAL_COUNSELING.md", "body-soul and medical-competence boundary"),
        ],
    },
    {
        "order": 5,
        "id": "HEART-BOOK-II",
        "label": "II Диагноз падшего сердца",
        "state": "RESEARCH_DOSSIER_ONLY",
        "manuscripts": [],
        "support": [
            r("СЕРИЯ СЕРДЦЕ/65_R3_UNREGENERATE_STRUGGLE.md", "R3 evidence dossier"),
            r("СЕРИЯ СЕРДЦЕ/66_R4_FOUR_SOILS.md", "R4 evidence dossier"),
        ],
    },
    {
        "order": 6,
        "id": "HEART-BOOK-III1",
        "label": "III.1 Обещание нового сердца",
        "state": "PRODUCT_SOURCE_ONLY",
        "manuscripts": [p("src/content/articles/novoe-serdce.mdx", "primary Product manuscript")],
        "support": [],
    },
    {
        "order": 7,
        "id": "HEART-BOOK-III2",
        "label": "III.2 Рождение свыше и обновление",
        "state": "RESEARCH_DOSSIER_ONLY",
        "manuscripts": [],
        "support": [
            r("СЕРИЯ СЕРДЦЕ/62_R1_REGENERATION_EXEGESIS.md", "R1 exegesis dossier"),
            r("СЕРИЯ СЕРДЦЕ/63_R1_REGENERATION_SYSTEMATICS.md", "R1 systematics dossier"),
        ],
    },
    {
        "order": 8,
        "id": "HEART-BOOK-III3",
        "label": "III.3 Сокрушённое сердце: покаяние",
        "state": "ASSEMBLED_READER",
        "manuscripts": [r("СЕРИЯ СЕРДЦЕ/80_READER_CHAPTER_III3_BROKEN_HEART_REPENTANCE_2026-08-02.md", "assembled reader")],
        "support": [r("СЕРИЯ СЕРДЦЕ/76_P0_BROKEN_HEART_REPENTANCE_2026-08-02.md", "P0 evidence dossier")],
    },
    {
        "order": 9,
        "id": "HEART-BOOK-III4",
        "label": "III.4 Сердце и Дух",
        "state": "PRODUCT_SOURCE_ONLY",
        "manuscripts": [p("src/content/articles/serdce-i-duh.mdx", "primary Product manuscript")],
        "support": [r("СЕРИЯ СЕРДЦЕ/64_R2_OT_REGENERATION_INDWELLING.md", "R2 continuity dossier")],
    },
    {
        "order": 10,
        "id": "HEART-BOOK-IV",
        "label": "IV Сердце и слово Божие",
        "state": "RESEARCH_DOSSIER_ONLY",
        "manuscripts": [],
        "support": [r("СЕРИЯ СЕРДЦЕ/68_R7A_WORD_AND_HEART.md", "R7a evidence dossier")],
    },
    {
        "order": 11,
        "id": "HEART-BOOK-V",
        "label": "V Сердце в борьбе с грехом",
        "state": "PRODUCT_SOURCE_ONLY",
        "manuscripts": [p("src/content/articles/rimlyanam-7-veruyushchiy-ili-neveruyushchiy.mdx", "primary Product manuscript")],
        "support": [
            r("СЕРИЯ СЕРДЦЕ/65_R3_UNREGENERATE_STRUGGLE.md", "unregenerate-struggle boundary"),
            r("СЕРИЯ СЕРДЦЕ/66_R4_FOUR_SOILS.md", "four-soils boundary"),
            r("СЕРИЯ СЕРДЦЕ/67_R5_TWO_STRUGGLES.md", "two-struggles boundary"),
        ],
    },
    {
        "order": 12,
        "id": "HEART-BOOK-VI",
        "label": "VI Сердце ученика и фарисея",
        "state": "RESEARCH_DOSSIER_ONLY",
        "manuscripts": [],
        "support": [r("СЕРИЯ СЕРДЦЕ/69_R7B_PHARISEE_DISCIPLE.md", "R7b evidence dossier")],
    },
    {
        "order": 13,
        "id": "HEART-BOOK-VII",
        "label": "VII Сердце в страдании и унынии",
        "state": "PRODUCT_SOURCE_ONLY",
        "manuscripts": [
            p("src/content/articles/tma-na-serdce.mdx", "primary Product manuscript"),
            p("src/content/articles/serdce-pod-skorbyu.mdx", "companion Product manuscript"),
        ],
        "support": [
            r("СЕРИЯ СЕРДЦЕ/65_V84B_DEPRESSION_THEOLOGICAL_PRIMACY_AND_AXIS_CORRECTION.md", "theological-axis boundary"),
            r("СЕРИЯ СЕРДЦЕ/67_V84D_SOURCE_LOCATOR_AND_EVIDENCE_STATUS_CLOSURE.md", "source-locator boundary"),
            r("СЕРИЯ СЕРДЦЕ/72_V84I_POST_MERGE_TOTAL_AUDIT_AND_CLOSURE_GATES.md", "material and safety closure"),
        ],
    },
    {
        "order": 14,
        "id": "HEART-BOOK-VIII",
        "label": "VIII Взирая на славу Христа",
        "state": "RESEARCH_DOSSIER_ONLY",
        "manuscripts": [],
        "support": [r("СЕРИЯ СЕРДЦЕ/70_R8_BEHOLDING_GLORY.md", "R8 evidence dossier")],
    },
    {
        "order": 15,
        "id": "HEART-BOOK-IX",
        "label": "IX Христос Апокалипсиса и сердце",
        "state": "RESEARCH_DOSSIER_ONLY",
        "manuscripts": [],
        "support": [r("СЕРИЯ СЕРДЦЕ/71_R9_CHRIST_OF_REVELATION.md", "R9 evidence dossier")],
    },
    {
        "order": 16,
        "id": "HEART-BOOK-X1",
        "label": "X.1 Суд сердца: два воскресения",
        "state": "ASSEMBLED_READER",
        "manuscripts": [r("СЕРИЯ СЕРДЦЕ/81_READER_CHAPTER_X1_JUDGMENT_TWO_RESURRECTIONS_2026-08-02.md", "assembled reader")],
        "support": [r("СЕРИЯ СЕРДЦЕ/77_P0_JUDGMENT_TWO_RESURRECTIONS_2026-08-02.md", "P0 evidence dossier")],
    },
    {
        "order": 17,
        "id": "HEART-BOOK-X2",
        "label": "X.2 Освобождённое сердце",
        "state": "PRODUCT_SOURCE_ONLY",
        "manuscripts": [
            p(
                "src/content/articles/osvobozhdennoe-serdce.mdx",
                "positive glorification Product sections",
                ["chetyre-sostoyaniya", "vopl-i-otvet", "ne-besplotnoe-parenie", "ne-sposobno-greshit", "pobeda-nad-vragom"],
            )
        ],
        "support": [
            r("СЕРИЯ СЕРДЦЕ/77_P0_JUDGMENT_TWO_RESURRECTIONS_2026-08-02.md", "resurrection/judgment boundary"),
            r("СЕРИЯ СЕРДЦЕ/81_READER_CHAPTER_X1_JUDGMENT_TWO_RESURRECTIONS_2026-08-02.md", "reader transition boundary"),
        ],
    },
    {
        "order": 18,
        "id": "HEART-BOOK-X3",
        "label": "X.3 Заключительная надежда",
        "state": "ASSEMBLED_READER",
        "manuscripts": [r("СЕРИЯ СЕРДЦЕ/88_READER_CHAPTER_X3_CONCLUDING_HOPE_2026-08-04.md", "assembled paraphrase-only reader")],
        "support": [
            p("src/content/articles/osvobozhdennoe-serdce.mdx", "exact Product conclusion source", ["vyhod"]),
            r("СЕРИЯ СЕРДЦЕ/71_R9_CHRIST_OF_REVELATION.md", "risen-Christ boundary"),
        ],
    },
]


def normalize_ref(value: str) -> str:
    value = re.sub(r"\s+", " ", value.strip())
    value = re.sub(r"\s*([:.,;–—-])\s*", r"\1", value)
    return value.rstrip(".,;:")


def trim_url(value: str) -> str:
    return value.rstrip(".,;:!?)}]»”)'")


def extract_sections(text: str, section_ids: list[str]) -> str:
    if not section_ids:
        return text
    starts = list(re.finditer(r"<h2\s+id=\"([^\"]+)\"[^>]*>", text, re.IGNORECASE))
    blocks: dict[str, str] = {}
    for index, match in enumerate(starts):
        end = starts[index + 1].start() if index + 1 < len(starts) else len(text)
        blocks[match.group(1)] = text[match.start():end]
    missing = [section_id for section_id in section_ids if section_id not in blocks]
    if missing:
        raise ValueError(f"missing section ids: {missing}")
    return "\n".join(blocks[section_id] for section_id in section_ids)


def scan_owner(spec: dict[str, Any], product_root: Path) -> dict[str, Any]:
    root = ROOT if spec["surface"] == "research" else product_root
    path = root / spec["path"]
    if not path.is_file():
        raise FileNotFoundError(f"{spec['surface']} owner missing: {spec['path']}")
    full_text = path.read_text(encoding="utf-8")
    scoped_text = extract_sections(full_text, spec["sections"])
    references = sorted({normalize_ref(match.group(0)) for match in SCRIPTURE_RE.finditer(scoped_text)}, key=str.casefold)
    external_links = sorted({trim_url(match.group(0)) for match in URL_RE.finditer(scoped_text)}, key=str.casefold)
    article_links = sorted(set(ARTICLE_LINK_RE.findall(scoped_text)))
    source_headings = sorted({re.sub(r"\s+", " ", heading.strip()) for heading in SOURCE_HEADING_RE.findall(scoped_text)}, key=str.casefold)
    return {
        "surface": spec["surface"],
        "path": spec["path"],
        "role": spec["role"],
        "sections": spec["sections"],
        "fullFileSha256": hashlib.sha256(full_text.encode("utf-8")).hexdigest(),
        "scopedSha256": hashlib.sha256(scoped_text.encode("utf-8")).hexdigest(),
        "scopedBytes": len(scoped_text.encode("utf-8")),
        "scriptureReferences": references,
        "externalLinks": external_links,
        "internalArticleLinks": article_links,
        "footnoteDefinitions": len(FOOTNOTE_RE.findall(scoped_text)),
        "markdownBlockquotes": len(MARKDOWN_BLOCKQUOTE_RE.findall(scoped_text)),
        "htmlBlockquotes": len(HTML_BLOCKQUOTE_RE.findall(scoped_text)),
        "inlineQuotationSegments": len(RUSSIAN_QUOTE_RE.findall(scoped_text)) + len(CURLY_QUOTE_RE.findall(scoped_text)),
        "sourceHeadings": source_headings,
    }


def direct_quote_state(state: str, entry_id: str) -> str:
    if state == "ASSEMBLED_READER":
        return "PARAPHRASE_OR_COMPOSED_READER_NO_NEW_DIRECT_QUOTES_APPROVED" if entry_id == "HEART-BOOK-X3" else "READER_ASSEMBLY_APPROVED_ZERO_NEW_DIRECT_QUOTES"
    if state == "PRODUCT_SOURCE_ONLY":
        return "EXISTING_PRODUCT_QUOTATION_SURFACES_REQUIRE_BOOK_LEVEL_REVIEW"
    return "DOSSIER_EVIDENCE_BOUNDARIES_CONTROL_FUTURE_READER"


def build(product_root: Path) -> dict[str, Any]:
    entries_out: list[dict[str, Any]] = []
    state_counts: dict[str, int] = {}
    all_refs: set[str] = set()
    all_external: set[str] = set()
    all_internal: set[str] = set()
    unique_files: set[tuple[str, str]] = set()
    totals = {
        "ownerSurfacesScanned": 0,
        "footnoteDefinitions": 0,
        "markdownBlockquotes": 0,
        "htmlBlockquotes": 0,
        "inlineQuotationSegments": 0,
        "sourceHeadings": 0,
    }

    for entry in ENTRIES:
        owners: list[dict[str, Any]] = []
        for kind in ("manuscripts", "support"):
            for spec in entry[kind]:
                scanned = scan_owner(spec, product_root)
                scanned["ownerKind"] = "manuscript" if kind == "manuscripts" else "support"
                owners.append(scanned)
                unique_files.add((scanned["surface"], scanned["path"]))
                totals["ownerSurfacesScanned"] += 1
                for key in ("footnoteDefinitions", "markdownBlockquotes", "htmlBlockquotes", "inlineQuotationSegments"):
                    totals[key] += int(scanned[key])
                totals["sourceHeadings"] += len(scanned["sourceHeadings"])

        refs = sorted({ref for owner in owners for ref in owner["scriptureReferences"]}, key=str.casefold)
        external = sorted({url for owner in owners for url in owner["externalLinks"]}, key=str.casefold)
        internal = sorted({url for owner in owners for url in owner["internalArticleLinks"]})
        all_refs.update(refs)
        all_external.update(external)
        all_internal.update(internal)
        state_counts[entry["state"]] = state_counts.get(entry["state"], 0) + 1

        quote_surfaces = sum(
            owner["markdownBlockquotes"] + owner["htmlBlockquotes"] + owner["inlineQuotationSegments"]
            for owner in owners
        )
        manual_reasons = ["BOOK_LEVEL_CITATION_REVIEW_REQUIRED"]
        if entry["state"] == "RESEARCH_DOSSIER_ONLY":
            manual_reasons.append("READER_MANUSCRIPT_NOT_ASSEMBLED")
        if external:
            manual_reasons.append("EXTERNAL_LINKS_PRESENT")
        if quote_surfaces:
            manual_reasons.append("QUOTATION_SURFACES_PRESENT")
        if any(owner["footnoteDefinitions"] for owner in owners):
            manual_reasons.append("FOOTNOTES_PRESENT")
        if not any(owner["sourceHeadings"] for owner in owners):
            manual_reasons.append("NO_EXPLICIT_SOURCE_HEADING_IN_SCANNED_SCOPE")

        entries_out.append({
            "order": entry["order"],
            "id": entry["id"],
            "label": entry["label"],
            "currentState": entry["state"],
            "readerAssembled": entry["state"] == "ASSEMBLED_READER",
            "directQuoteState": direct_quote_state(entry["state"], entry["id"]),
            "owners": owners,
            "aggregate": {
                "uniqueScriptureReferences": refs,
                "externalLinks": external,
                "internalArticleLinks": internal,
                "quotationSurfaceCount": quote_surfaces,
                "manualReviewReasons": manual_reasons,
                "entryCitationPassComplete": False,
            },
        })

    return {
        "schemaVersion": 1,
        "authorityId": "HEART-WHOLE-BOOK-CITATION-INVENTORY-2026-08-04",
        "status": "EIGHTEEN_ENTRY_READ_ONLY_CITATION_INVENTORY_COMPLETE_BOOK_PASS_OPEN",
        "generatedAt": "2026-08-04",
        "lastVerifiedAt": "2026-08-04",
        "researchSnapshot": RESEARCH_SNAPSHOT,
        "productSnapshot": {
            "repository": "FedorMilovanov/gb-is-my-strength",
            "commit": PRODUCT_COMMIT,
        },
        "method": {
            "script": "scripts/build_heart_whole_book_citation_inventory.py",
            "mode": "READ_ONLY_DETERMINISTIC_SCAN",
            "scope": "primary manuscripts plus governing support owners for all eighteen final-order entries",
            "scriptureExtraction": "explicit Russian/English Bible-book token plus chapter/verse pattern",
            "quotationSurfaces": "Markdown blockquotes, HTML blockquotes and inline guillemet/curly-quote segments",
            "limitations": [
                "quotation surfaces are candidates, not automatic direct-quote classifications",
                "Scripture references outside the explicit token grammar require manual review",
                "link presence does not establish source adequacy, locator quality or accessibility",
                "inventory completion does not equal entry-level or whole-book citation approval",
            ],
        },
        "entries": entries_out,
        "counts": {
            "finalBookEntries": 18,
            "assembledReader": state_counts.get("ASSEMBLED_READER", 0),
            "productSourceOnly": state_counts.get("PRODUCT_SOURCE_ONLY", 0),
            "researchDossierOnly": state_counts.get("RESEARCH_DOSSIER_ONLY", 0),
            "ownerRequired": 0,
            "uniqueOwnerFiles": len(unique_files),
            "uniqueScriptureReferences": len(all_refs),
            "uniqueExternalLinks": len(all_external),
            "uniqueInternalArticleLinks": len(all_internal),
            **totals,
            "entriesRequiringManualBookReview": 18,
            "entryCitationPassComplete": 0,
            "newDirectQuotesApproved": 0,
        },
        "globalSurfaces": {
            "uniqueScriptureReferences": sorted(all_refs, key=str.casefold),
            "uniqueExternalLinks": sorted(all_external, key=str.casefold),
            "uniqueInternalArticleLinks": sorted(all_internal),
        },
        "publicationBoundary": {
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
        "nextTransaction": "Review the eighteen entry inventories, resolve missing locators/version identifiers and direct-quotation candidates, then record entry-level citation dispositions without rewriting manuscripts by implication.",
    }


def canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--product-root", type=Path, required=True)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    report = build(args.product_root.resolve())
    if args.write:
        REGISTRY.parent.mkdir(parents=True, exist_ok=True)
        REGISTRY.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"wrote {REGISTRY.relative_to(ROOT)}")
        return 0
    if not REGISTRY.is_file():
        payload = base64.b64encode((json.dumps(report, ensure_ascii=False, indent=2) + "\n").encode("utf-8")).decode("ascii")
        print("Heart citation inventory: REGISTRY MISSING")
        print(f"HEART_CITATION_INVENTORY_BASE64={payload}")
        return 1
    expected = json.loads(REGISTRY.read_text(encoding="utf-8"))
    if canonical(expected) != canonical(report):
        payload = base64.b64encode((json.dumps(report, ensure_ascii=False, indent=2) + "\n").encode("utf-8")).decode("ascii")
        print("Heart citation inventory: REGISTRY DRIFT")
        print(f"HEART_CITATION_INVENTORY_BASE64={payload}")
        return 1
    print(
        "Heart citation inventory: PASS — "
        f"18 entries, {report['counts']['uniqueOwnerFiles']} files, "
        f"{report['counts']['uniqueScriptureReferences']} Scripture refs, "
        f"{report['counts']['uniqueExternalLinks']} external links, book pass open"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
