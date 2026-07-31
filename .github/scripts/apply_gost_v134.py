from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path("БАПТИСТЫ РОССИИ/baptists_v120_TRUE_GROUPED")
MD = ROOT / "groups/06_DATA_AND_PROOF_LEDGERS.md"
SOURCE = ROOT / "data/SOURCE_ANCHORS.csv"
PROOF = ROOT / "data/PROOF_STATUS_LEDGER.csv"
MICRO = ROOT / "data/NEXT_MICROBATCH.csv"
MARKER = "## v134 — HOLD/B resolution sweep: editorial roles and person authorities"


def read_csv(path: Path):
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def write_csv(path: Path, fields, rows):
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\r\n", extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def normalize(fields, values):
    return {field: values.get(field, "") for field in fields}


def upsert(rows, fields, key, values):
    value = values[key]
    matches = [index for index, row in enumerate(rows) if row.get(key) == value]
    if len(matches) > 1:
        raise RuntimeError(f"duplicate existing key {key}={value}: {matches}")
    row = normalize(fields, values)
    if matches:
        rows[matches[0]] = row
    else:
        rows.append(row)


source_fields, source_rows = read_csv(SOURCE)
sources = [
    {
        "source_id": "GOST-134-SRC-SULAWKA",
        "url": "https://theo-logos.pl/bitstreams/b91bb0e7-6815-4cad-97d7-2c614d563b9b/download",
        "confirms": "Declared BUW/BN physical query covers Gost 1935-1939 and Woskriesnaja Szkola 1933-1935; names late editorial roles.",
        "source": "A. R. Sulawka / Kultura-Media-Teologia",
        "authority_level": "A2 academic physical issue survey; primary colophons pending",
        "used_for": "late Gost and appendix editorial-role verification",
        "version": "v134",
        "source_key": "GOST-134-SRC-SULAWKA",
        "use": "academic issue-survey verification with attribution",
        "label": "Sulawka physical issue survey",
        "type": "academic article full PDF",
        "trust_note": "Exact quotations remain visual-screenshot pending; 1936 endpoint and 247 count are synthesis rather than complete physical inventory.",
        "source_type": "academic issue survey",
        "note": "Gost queried 1935-1939; appendix queried 1933-1935. Do not promote to primary-colophon status.",
    },
    {
        "source_id": "GOST-134-SRC-HUSARUK-FAMILY",
        "url": "https://www.everand.com/book/624459311/Awaiting-The-Dawn-My-Life-in-a-Nazi-Concentration-Camp",
        "confirms": "Family-edited introduction places Vladimir Husaruk in Warsaw from 1926, university and chemistry work, marriage and orphanage leadership.",
        "source": "Husaruk family-edited English memoir edition",
        "authority_level": "B+ family person authority",
        "used_for": "W. I. Husaruk / Vladimir Husaruk identity chain",
        "version": "v134",
        "source_key": "GOST-134-SRC-HUSARUK-FAMILY",
        "use": "person-authority convergence only",
        "label": "Vladimir Husaruk Warsaw biography",
        "type": "family-edited memoir introduction",
        "trust_note": "Strong biographical bridge; not a primary employment or signature record.",
        "source_type": "family person authority",
        "note": "Pair with contemporary 1946 notice, RSL 1949 record and Sulawka role evidence.",
    },
    {
        "source_id": "GOST-134-SRC-HUSARUK-RSL",
        "url": "https://search.rsl.ru/ru/record/01000371468",
        "confirms": "Official RSL record identifies Vladimir Gusaruk as author of the 1949 concentration-camp memoir and exposes a direct digital route.",
        "source": "Russian State Library",
        "authority_level": "A official library authority record",
        "used_for": "Russian memoir author identity and publication control",
        "version": "v134",
        "source_key": "GOST-134-SRC-HUSARUK-RSL",
        "use": "official author/publication identity",
        "label": "Vladimir Gusaruk 1949 memoir",
        "type": "official library digital record",
        "trust_note": "Full prewar biographical pages still require inspection.",
        "source_type": "official library record",
        "note": "Do not infer editorial employment from catalog metadata alone.",
    },
    {
        "source_id": "GOST-134-SRC-HUSARUK-1946",
        "url": "https://www.scribd.com/document/980393151/EditorinChief-Northwestern-Pilot-Bible",
        "confirms": "August 1946 notice describes Rev. W. Husaruk as university graduate, camp survivor and leader of more than 20,000 Baptists in the British zone, with wife and four children.",
        "source": "Northwestern Pilot institutional-community periodical scan",
        "authority_level": "A-/B+ contemporary person control via scan mirror",
        "used_for": "1946 minister / 1949 memoir-author identity convergence",
        "version": "v134",
        "source_key": "GOST-134-SRC-HUSARUK-1946",
        "use": "contemporary person control",
        "label": "Rev. W. Husaruk 1946",
        "type": "contemporary periodical notice",
        "trust_note": "Does not independently prove prewar editorial employment.",
        "source_type": "contemporary institutional press",
        "note": "Preserve mirror provenance; seek canonical scan if direct quotation is needed.",
    },
    {
        "source_id": "GOST-134-SRC-JESAKOW-SKOTARCZAK",
        "url": "https://www.researchgate.net/publication/331241713_Edukacja_ewangelicznych_chrzescijan_w_Polsce_w_okresie_miedzywojennym",
        "confirms": "Academic study names Leon Jesakow among lecturers of the Warsaw Bible School in the late 1930s.",
        "source": "Dorota Skotarczak",
        "authority_level": "A2/B+ academic named-role evidence",
        "used_for": "prewar first-name and Warsaw-role authority chain",
        "version": "v134",
        "source_key": "GOST-134-SRC-JESAKOW-SKOTARCZAK",
        "use": "person-role authority convergence",
        "label": "Leon Jesakow Bible School lecturer",
        "type": "academic article",
        "trust_note": "Not a civil identity or signature record.",
        "source_type": "academic person-role source",
        "note": "Pair with official postwar school history and mf Call #238.",
    },
    {
        "source_id": "GOST-134-SRC-JESAKOW-METHODIST",
        "url": "https://szkola.metodysci.pl/historia-szkoly/",
        "confirms": "Official school history names ks. Leonid Jesakow as director in 1949-1956 and records emigration to the USA in 1956.",
        "source": "Methodist English School official history",
        "authority_level": "A official denominational institutional history",
        "used_for": "postwar Leonid Jesakow identity continuity",
        "version": "v134",
        "source_key": "GOST-134-SRC-JESAKOW-METHODIST",
        "use": "official person-history control",
        "label": "Leonid Jesakow school director",
        "type": "official institutional history",
        "trust_note": "Primary personnel file still required for signature/date closure.",
        "source_type": "official institutional history",
        "note": "Supports continuity with prewar Leon Jesakow and missionary-file locator.",
    },
    {
        "source_id": "GOST-134-SRC-JESAKOW-MF238",
        "url": "https://anyflip.com/ober/zwqj/basic",
        "confirms": "Finding-aid transcription gives exact locator mf Call #238: Jesakow, Leonid (Rev.), 1949.",
        "source": "Methodist missionary files finding aid",
        "authority_level": "A2 exact folder locator; contents unseen",
        "used_for": "primary person-authority closure request",
        "version": "v134",
        "source_key": "GOST-134-SRC-JESAKOW-MF238",
        "use": "targeted identity-file request",
        "label": "Jesakow Leonid missionary file",
        "type": "archive finding-aid transcription",
        "trust_note": "Folder contents, signature and prewar references remain unseen.",
        "source_type": "missionary-file finding aid",
        "note": "Request selected identity/service pages only.",
    },
    {
        "source_id": "GOST-134-SRC-FETLER-EARLY-SUPPLEMENT",
        "url": "https://ru.scribd.com/document/467281539/%D0%92%D0%98-1-2020",
        "confirms": "Later confessional memory describes surviving 1920s Sunday-school materials as a Gost supplement under V. A. Fetler.",
        "source": "Vestnik Istiny 1/2020",
        "authority_level": "B confessional memory",
        "used_for": "separation of early child-material layer from Warsaw 1933-1936 series",
        "version": "v134",
        "source_key": "GOST-134-SRC-FETLER-EARLY-SUPPLEMENT",
        "use": "series-separation control only",
        "label": "Early Gost child materials under Fetler",
        "type": "later confessional memory",
        "trust_note": "Not a colophon and not evidence that the distinct Warsaw Woskriesnaja Szkola had Fetler as editor.",
        "source_type": "confessional memory",
        "note": "Do not merge early 1920s materials with the 1933-1936 appendix series.",
    },
]
for row in sources:
    upsert(source_rows, source_fields, "source_id", row)
write_csv(SOURCE, source_fields, source_rows)

proof_fields, proof_rows = read_csv(PROOF)
proofs = [
    {
        "item_id": "GOST-130-004",
        "corpus": "Воскресная школа",
        "issue": "Gusaruk source chain / Seiatel Istiny 1926 no.2 p.15",
        "status": "later_editorial_role_academic_issue_survey_verified_exact_1926_wording_and_primary_colophon_pending",
        "pages": "Sulawka survey 1933-1935; p.15 target unseen",
        "holding": "BUW/BN surveyed run; RUEBU target; MHC exclusion",
        "source": "Sulawka; Gusaruk profile; RUEBU; Potapova; Vins; MHC; Emigrantika",
        "next_action": "Request exact p.15 wording/provenance and selected 1933, 1935 and 1936 colophons only",
        "year": "1926 source lead / 1933-1936 appendix",
        "source_url": "https://theo-logos.pl/bitstreams/b91bb0e7-6815-4cad-97d7-2c614d563b9b/download",
        "verification_note": "General later Husaruk editorial role is academically issue-survey verified and no longer depends solely on p.15. Exact 1926 wording, first year, 1936 endpoint and primary colophons remain pending.",
        "version": "v134",
    },
    {
        "item_id": "GOST-134-001",
        "corpus": "Gost late Warsaw run",
        "issue": "1935 through July 1936 editorial control",
        "status": "academic_issue_survey_verified_primary_colophons_pending",
        "pages": "surveyed Gost 1935-1939; role endpoint VII 1936",
        "holding": "BUW/BN physical query declared by Sulawka",
        "source": "Sulawka official full PDF",
        "next_action": "Obtain representative 1935 and July 1936 or adjacent colophons",
        "year": "1935-1936",
        "source_url": "https://theo-logos.pl/bitstreams/b91bb0e7-6815-4cad-97d7-2c614d563b9b/download",
        "verification_note": "L. Jesiakow responsible editor and W. Husaruk editor-publisher through VII 1936 are usable with academic attribution; not quote-ready primary imprint evidence.",
        "version": "v134",
    },
    {
        "item_id": "GOST-134-002",
        "corpus": "Woskriesnaja Szkola",
        "issue": "1933-1936 chronology and editorial roles",
        "status": "academic_issue_survey_verified_1933_1935_1936_endpoint_scholarly_primary_colophons_pending",
        "pages": "surveyed 1933-1935; synthesized endpoint 1936",
        "holding": "BUW/BN physical query declared by Sulawka",
        "source": "Sulawka official full PDF",
        "next_action": "Obtain opening 1933, transition 1935 and any 1936 title/colophon controls",
        "year": "1933-1936",
        "source_url": "https://theo-logos.pl/bitstreams/b91bb0e7-6815-4cad-97d7-2c614d563b9b/download",
        "verification_note": "W. I. Husaruk editor-publisher and L. Jaskow responsible editor from 1935 are academically verified for surveyed years. Total 24 and 1936 endpoint remain scholarly synthesis.",
        "version": "v134",
    },
    {
        "item_id": "GOST-134-003",
        "corpus": "Person authority",
        "issue": "W. I. Husaruk / Vladimir Husaruk",
        "status": "identity_resolved_very_high_multi_source_confidence_primary_personnel_signature_pending",
        "pages": "1926 Warsaw bridge; 1946 control; 1949 memoir authority",
        "holding": "family edition; contemporary press; RSL; academic issue survey",
        "source": "Husaruk family edition; Northwestern Pilot; RSL; Sulawka",
        "next_action": "Close with representative colophon, personnel file, signature or civil record",
        "year": "1926-1949",
        "source_url": "https://search.rsl.ru/ru/record/01000371468",
        "verification_note": "Treat Warsaw W. I. Husaruk as Vladimir Husaruk with explicit very-high-confidence qualification; no generic identity HOLD remains.",
        "version": "v134",
    },
    {
        "item_id": "GOST-134-004",
        "corpus": "Person authority",
        "issue": "L. Jesakow / Jesiakow / Jaskow / Leon / Leonid Jesakow",
        "status": "identity_resolved_very_high_multi_source_confidence_primary_authority_file_pending",
        "pages": "prewar school/editor roles; 1949-1956 history; mf Call #238",
        "holding": "academic article; official Methodist history; missionary-file locator",
        "source": "Sulawka; Skotarczak; Methodist school history; mf Call #238",
        "next_action": "Request selected mf #238 identity/signature/prewar-service pages and APL board/signature controls",
        "year": "1935-1956",
        "source_url": "https://szkola.metodysci.pl/historia-szkoly/",
        "verification_note": "Treat variants as Leon/Leonid Jesakow with very-high-confidence qualification; primary authority file still pending.",
        "version": "v134",
    },
    {
        "item_id": "GOST-134-005",
        "corpus": "Series boundary",
        "issue": "early 1920s Gost child materials vs Woskriesnaja Szkola 1933-1936",
        "status": "distinct_layers_preserved_no_editor_transfer",
        "pages": "later memory only",
        "holding": "Vestnik Istiny 1/2020 memory",
        "source": "Vestnik Istiny 1/2020",
        "next_action": "Seek early physical supplement title/colophon separately; do not merge with later Warsaw series",
        "year": "1920s memory / 1933-1936 later series",
        "source_url": "https://ru.scribd.com/document/467281539/%D0%92%D0%98-1-2020",
        "verification_note": "Fetler memory supports an early child-material layer only and does not contradict Husaruk role in the distinct later series.",
        "version": "v134",
    },
]
for row in proofs:
    upsert(proof_rows, proof_fields, "item_id", row)
write_csv(PROOF, proof_fields, proof_rows)

micro_fields, micro_rows = read_csv(MICRO)


def set_micro(predicate, values):
    matches = [index for index, row in enumerate(micro_rows) if predicate(row.get("item", ""))]
    if len(matches) > 1:
        raise RuntimeError(f"ambiguous microbatch matches: {matches}")
    row = normalize(micro_fields, values)
    if matches:
        micro_rows[matches[0]] = row
    else:
        micro_rows.append(row)


set_micro(
    lambda value: value == "Obtain Seiatel Istiny 1926 no.2 p.15",
    {
        "priority": "P0",
        "item": "Obtain Seiatel Istiny 1926 no.2 p.15",
        "goal": "Acquire cover, contents, p.15 and colophon plus the 100-year source list to verify exact 1926 wording and early provenance only",
        "blocker": "Later Husaruk editorial role is academically verified independently; target page and exact early chronology remain unseen.",
    },
)
set_micro(
    lambda value: "Kłaczkow" in value or "Klaczkow" in value,
    {
        "priority": "P0",
        "item": "Kłaczkow exact pages p.116 and p.261",
        "goal": "Obtain readable p.116 and p.261 with adjacent notes; verify appendix statement, Gost chronology, 247-count meaning and cited holdings",
        "blocker": "Official 456-page digital object is known but viewer/page extraction is unavailable; broad chapter reproduction is unnecessary.",
    },
)
set_micro(
    lambda value: value == "Gost/Woskriesnaja selected colophons 1933-1936",
    {
        "priority": "P0",
        "item": "Gost/Woskriesnaja selected colophons 1933-1936",
        "goal": "Acquire only appendix 1933 opening, 1935 editor transition, any 1936 endpoint, plus Gost 1935 and July 1936 or adjacent colophons with shelfmarks/binding relation",
        "blocker": "Academic physical-survey roles are resolved; primary imprint and exact endpoint closure remain.",
    },
)
write_csv(MICRO, micro_fields, micro_rows)

text = MD.read_text(encoding="utf-8-sig")
if MARKER not in text:
    block = """

## v134 — HOLD/B resolution sweep: editorial roles and person authorities

More than 70 candidate links, PDFs, catalog records and person references were triaged. Only evidence that independently changes a status or narrows a primary closure route is retained.

| Node | Previous state | v134 decision | Remaining primary gate |
|---|---|---|---|
| Late `Gost` editors | Husaruk/Jesakow partly HOLD outside 1934 local colophons | Suławka's declared BUW/BN query of `Gost` 1935–1939 supports `L. Jesiakow` as responsible editor and `W. Husaruk` as editor-publisher through July 1936. `ACADEMIC ISSUE-SURVEY VERIFIED`. | Representative 1935 and July 1936 or adjacent colophons. |
| `Woskriesnaja Szkoła` roles | derivative p.15 chain; role HOLD | Suławka's physical query covers 1933–1935 and supports `W. I. Husaruk` as editor-publisher and `L. Jaśków` as responsible editor from 1935. `ACADEMIC ISSUE-SURVEY VERIFIED`. | Opening 1933, transition 1935 and any 1936 colophons; 1936 endpoint/24 total remain scholarly synthesis. |
| W. I. Husaruk identity | semantic/person HOLD | Family Warsaw biography from 1926, contemporary 1946 `Rev. W. Husaruk`, official RSL 1949 memoir record and the surveyed editorial role converge on Vladimir Husaruk. `IDENTITY RESOLVED — VERY HIGH CONFIDENCE`. | Personnel/signature/civil authority record. |
| L. Jesakow identity | probable Leon/Leonid | Prewar academic `Leon Jesakow`, official postwar `ks. Leonid Jesaków`, and exact missionary-file locator `mf Call #238` form a continuous chain. `IDENTITY RESOLVED — VERY HIGH CONFIDENCE`. | Selected mf #238 identity/signature pages and APL board controls. |
| Fetler child-material memory | apparent conflict with Husaruk | A later memory concerns an earlier 1920s child-material layer under V. A. Fetler. It is not transferred to the distinct Warsaw 1933–1936 series. | Separate early supplement title/colophon. |

Status boundaries retained:

- no `quote_ready` promotion without visual page/facsimile control;
- `Сеятель Истины` 1926 no.2 p.15 remains required for exact wording and early provenance, not for the now independently supported later editorial role;
- Kupsch pp.172–182, congress numbering X/XI/XII and the unnamed rival society remain unresolved;
- Kłaczkow is narrowed to p.116 and p.261 rather than a broad chapter request;
- no institutional request was sent and no paid work or binary acquisition was initiated.

Evidence routes:

- Suławka full PDF: https://theo-logos.pl/bitstreams/b91bb0e7-6815-4cad-97d7-2c614d563b9b/download
- Husaruk family edition: https://www.everand.com/book/624459311/Awaiting-The-Dawn-My-Life-in-a-Nazi-Concentration-Camp
- RSL memoir authority: https://search.rsl.ru/ru/record/01000371468
- 1946 person control: https://www.scribd.com/document/980393151/EditorinChief-Northwestern-Pilot-Bible
- Methodist school history: https://szkola.metodysci.pl/historia-szkoly/
- Jesakow mf #238 finding aid: https://anyflip.com/ober/zwqj/basic
- early Fetler-layer memory: https://ru.scribd.com/document/467281539/%D0%92%D0%98-1-2020
"""
    MD.write_text(text.rstrip() + block + "\n", encoding="utf-8")

for path, key, values in (
    (SOURCE, "source_id", [row["source_id"] for row in sources]),
    (PROOF, "item_id", [row["item_id"] for row in proofs]),
):
    _, rows = read_csv(path)
    for value in values:
        count = sum(1 for row in rows if row.get(key) == value)
        if count != 1:
            raise RuntimeError(f"{path}: {key}={value} count={count}")

if MD.read_text(encoding="utf-8-sig").count(MARKER) != 1:
    raise RuntimeError("v134 grouped marker is not unique")

print("Gost v134 HOLD-resolution integration prepared successfully")
