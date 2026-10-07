#!/usr/bin/env python3
"""Read-only integrity gate for the ИСКУПЛЕНИЕ (redemption/atonement) corpus.

Fails closed. Writes nothing. Enforces the five-axis evidence model, the
Wave-0 inventory counts that the markdown dossiers actually contain, the
no-quote-until-verified boundary, and the rights boundary that forbids
placing copyrighted full text in the corpus Drive tree.
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REG = ROOT / "data/redemption-corpus-authority-2026-10-07.json"
CORPUS = ROOT / "ИСКУПЛЕНИЕ"

F = {
    "current": "00_CURRENT_AUTHORITY_2026-10-07.md",
    "charter": "00_MASTER_RESEARCH_MAP_AND_CHARTER_2026-10-07.md",
    "intro_w0": "01_W0_INTRODUCTION_AND_TERMINOLOGY_2026-10-07.md",
    "scripture": "02_W0_SCRIPTURE_CORPUS_FOR_WHOM_2026-10-07.md",
    "sources": "03_W0_SOURCE_REGISTRY_2026-10-07.md",
    "models": "04_W0_COMPETING_MODELS_TAXONOMY_2026-10-07.md",
    "acquisition": "05_W0_ACQUISITION_FAMILIES_AND_DRIVE_INTAKE_2026-10-07.md",
    "product": "06_PUBLICATION_ARCHITECTURE_FOR_GOSPOD_BOG_2026-10-07.md",
    "primary": "10_W0_PRIMARY_TEXT_DORT_HEAD_II_AND_CALVIN_2026-10-07.md",
    "mirror": "07_W0_DRIVE_MIRROR_RECEIPT_2026-10-07.md",
    "index": "README.md",
}

ALLOWED_CLASSES = {"A1", "A2", "A3", "B1", "C", "D"}
EXPECTED_GROUPS = {"A": 22, "B": 23, "C": 12, "D": 7, "TC": 7}
EXPECTED_TOTAL = 71
EXPECTED_SOURCE_RECORDS = 113
EXPECTED_FAMILIES = 13
ALLOWED_PUB_STATES = {"HOLD", "FORBIDDEN-AS-evidence", "DO_NOT_IMPLEMENT_UNTIL_W6"}
DRIVE_ROOT = "1VULVPNq4DbBFS5KvBDpSkJOlx4jbEQAV"
DRIVE_CHILDREN = 7
FORBIDDEN_TOKENS = (
    "PUBLICATION APPROVED",
    "approved for publication",
    "цитатный корпус закрыт",
    "публикация разрешена",
)

errors: list[str] = []
notes: list[str] = []


def req(condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


def read(path: Path) -> str:
    if not path.exists():
        errors.append(f"missing file: {path.relative_to(ROOT)}")
        return ""
    return path.read_text(encoding="utf-8")


def non_ascii_anomalies(text: str, label: str) -> None:
    """Scripts that must never appear in these Russian-language dossiers."""
    bad = re.findall(r"[\u0600-\u06ff\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uac00-\ud7af]", text)
    if bad:
        errors.append(f"{label}: foreign-script contamination {sorted(set(bad))[:6]}")


# ---------------------------------------------------------------- registry ---
data = {}
try:
    data = json.loads(REG.read_text(encoding="utf-8"))
except Exception as exc:  # noqa: BLE001 - fail closed on any parse problem
    errors.append(f"{REG.name}: {exc}")

req(isinstance(data, dict) and data.get("schemaVersion") == 1, "registry: schemaVersion drift")
req(
    data.get("authorityId") == "REDEMPTION-CORPUS-AUTHORITY-2026-10-07",
    "registry: authorityId drift",
)
req(
    data.get("status")
    == "WAVE0_OPEN_CHARTER_TERMINOLOGY_REGISTRY_PRIMARYTEXT_NO_PUBLICATION",
    "registry: status drift (must not advertise closure)",
)
req(data.get("corpus") == "ИСКУПЛЕНИЕ", "registry: corpus key drift")
req(data.get("lastVerifiedAt") == "2026-10-07", "registry: lastVerifiedAt drift")

gov = data.get("governance", {})
req(
    gov.get("evidencePolicy") == "data/repository-evidence-policy-v2.json",
    "registry: single evidence policy pointer drift",
)
req(Path(gov.get("evidencePolicy", "")).exists(), "registry: evidence policy file missing")
req(
    gov.get("allowedSourceClasses") == ["A1", "A2", "A3", "B1", "C", "D"],
    "registry: source-class drift (no local A/B/C ladder allowed)",
)
req(
    gov.get("independentAxes")
    == ["evidenceClass", "accessState", "locatorState", "rightsState", "publicationState"],
    "registry: axis drift",
)
req(
    gov.get("holdFlags") == ["EVIDENCE", "LOCATOR", "ARCHIVE", "RIGHTS", "PUBLICATION"],
    "registry: hold-flag drift",
)
req(gov.get("b1CannotSolelySupportDisputedQuote") is True, "registry: B1 sole-support rule drift")
req(gov.get("failClosed") is True, "registry: failClosed drift")
req(gov.get("validatorsReadOnly") is True, "registry: validator read-only pledge drift")

# ------------------------------------------------------------ corpus files ---
texts = {key: read(CORPUS / name) for key, name in F.items()}
for key, text in texts.items():
    if text:
        non_ascii_anomalies(text, f"ИСКУПЛЕНИЕ/{F[key]}")
        for token in FORBIDDEN_TOKENS:
            if token.lower() in text.lower():
                errors.append(f"ИСКУПЛЕНИЕ/{F[key]}: forbidden self-approval token {token!r}")

req(len(F) == 11, "file map drift")
for key in F:
    req(key in texts and texts[key] != "", f"corpus file not loaded: {key}")

# Referenced paths in the registry must exist (spineHistory lists deliberately absent files).
registry_live = {k: v for k, v in data.items() if k != "spineHistory"}
for candidate in set(re.findall(r'"((?:ИСКУПЛЕНИЕ|data|AGENT_RULES\.md)[^"]*?)"', json.dumps(registry_live, ensure_ascii=False))):
    req(Path(candidate).exists(), f"registry references missing path: {candidate}")

# ---------------------------------------------------- scripture inventory ---
scripture = texts["scripture"]
ids = re.findall(r"^\|\s*`([ABCD]|TC)-(\d{2})`", scripture, re.M)
counts = Counter(group for group, _ in ids)
req(dict(counts) == EXPECTED_GROUPS, f"scripture inventory drift: {dict(counts)}")
req(len(ids) == EXPECTED_TOTAL, f"scripture locus total drift: {len(ids)} != {EXPECTED_TOTAL}")
dupes = [pair for pair, n in Counter(ids).items() if n > 1]
req(not dupes, f"duplicate scripture ids: {dupes}")
req(
    "ORIGINAL-LANGUAGE STRINGS VERIFIED: 0" in scripture,
    "scripture dossier lost its no-verified-originals boundary",
)
for field in ("LEXEME_VERIFIED", "MORPHOLOGY_VERIFIED", "APPARATUS_CHECKED"):
    req(field in scripture, f"scripture dossier missing verification field {field}")
for marker in ("Синодальн", "BIBLE_CORPUS"):
    req(marker in scripture, f"scripture dossier missing dependency marker {marker}")

inv = data.get("scriptureInventory", {})
req(inv.get("groups") == EXPECTED_GROUPS, "registry: scripture group drift")
req(inv.get("total") == EXPECTED_TOTAL, "registry: scripture total drift")
req(inv.get("originalLanguageStringsVerified") == 0, "registry: original-language count must stay 0 in Wave 0")
req(inv.get("synodalQuotationsAllowed") is False, "registry: Synodal quotation gate must be false")
req(
    inv.get("verificationFieldsRequiredBeforeW2")
    == ["LEXEME_VERIFIED", "MORPHOLOGY_VERIFIED", "APPARATUS_CHECKED"],
    "registry: W2 entry gate drift",
)

# ---------------------------------------------------------- source registry ---
sources = texts["sources"]
record_rows = re.findall(r"^\|\s*`(RED-SRC-\d{4})`", sources, re.M)
records = re.findall(r"`(RED-SRC-\d{4})`", sources)
req(len(set(record_rows)) == EXPECTED_SOURCE_RECORDS, f"source registry record drift: {len(set(record_rows))}")
req(len(record_rows) == len(set(record_rows)), "source registry: duplicate record rows")
req(set(records) == set(record_rows), "source registry: cross-reference to an unregistered record id")
rows = re.findall(r"^\|\s*`RED-SRC-\d{4}`\s*\|(.*?)\|\s*$", sources, re.M)
req(len(rows) >= 60, f"source registry: too few parseable rows ({len(rows)})")
for row in rows:
    cells = [c.strip() for c in row.split("|")]
    classes = [c for c in cells if c in ALLOWED_CLASSES or c == "D"]
    req(bool(classes), f"source row without an allowed evidence class: {row[:70]}")
    for cls in classes:
        req(cls in ALLOWED_CLASSES, f"source row class outside policy: {cls}")
    if "NONE" in cells:
        req(
            "HOLD" in row or "FORBIDDEN" in row or "UNKNOWN" in row or "PD" in row,
            f"source row with ACCESS NONE lacks a rights/publication boundary: {row[:70]}",
        )
req("COPYRIGHT | HOLD" in sources or "RIGHTS_HOLD" in sources, "source registry: rights boundary drift")
req("запись" in sources and "Пустое" in sources, "source registry: state-legend drift")

reg_sources = data.get("sourceRegistry", {})
req(reg_sources.get("recordCount") == EXPECTED_SOURCE_RECORDS, "registry: source record count drift")
req(
    reg_sources.get("modernBooksInDrive") == 0,
    "registry: copyrighted full text must not be recorded as placed in Drive",
)
req(reg_sources.get("recordsWithFullAccess") == 2, "registry: FULL-access count drift (Wave 0 ceiling)")

# ------------------------------------------------------------------ models ---
models = texts["models"]
for axis in ("O-1", "O-2", "O-3", "O-4", "O-5", "O-6"):
    req(f"`{axis}`" in models, f"model axes missing {axis}")
found_models = sorted(set(re.findall(r"### `(M-\d{2})`", models)))
req(
    found_models == data.get("models", {}).get("ids"),
    f"model id drift: {found_models} vs {data.get('models', {}).get('ids')}",
)
req("Fairness" in models or "честн" in models.lower(), "models dossier lost its fairness rule")
for label in ("гипотетич", "Amyraut", "Davenant", "hyper"):
    req(label.lower() in models.lower(), f"models dossier missing required distinction {label}")

# ------------------------------------------------------------- acquisition ---
acq = texts["acquisition"]
families = sorted(set(re.findall(r"`(RED-FAM-[A-Z][A-Z\-]+)`", acq)))
req(len(families) == EXPECTED_FAMILIES, f"acquisition family count drift: {len(families)}")
req(
    families == sorted(data.get("acquisitionFamilies", [])),
    "registry/markdown acquisition-family drift",
)
req(
    all(re.search(rf"### `{fam}`", acq) for fam in families),
    "acquisition family without an owned section",
)
state = data.get("acquisitionState", {})
req(state.get("families") == EXPECTED_FAMILIES, "registry: family count drift")
req(state.get("directQuotesFromCopyrightedBooks") == 0, "registry: copyrighted-quote count must stay 0")
req(state.get("userPlacedFilesInDrive") == 4, "registry: Drive intake count drift")
req(state.get("objectsPresentInDriveRequiringHashVerification") == 4, "registry: unverified-object count drift")
req(state.get("verifiedFileReceipts") == 1, "registry: presence must never be counted as a receipt")
for key in ("driveNameAloneIsReceipt", "previewAloneIsFullText", "bibliographyAloneSupportsClaim"):
    req(state.get("receiptPolicy", {}).get(key) is False, f"registry: receipt policy {key} must be false")
    req(key in acq, f"acquisition dossier lost receipt policy {key}")
req("sha256" in acq, "acquisition dossier: sha256 receipt requirement drift")

# --------------------------------------------------------------- Drive tree ---
drive = data.get("drive", {})
req(drive.get("rootId") == DRIVE_ROOT, "registry: Drive root drift")
children = drive.get("subfolders", [])
req(len(children) == DRIVE_CHILDREN, f"registry: Drive subfolder count drift ({len(children)})")
req(all(re.fullmatch(r"[0-9A-Za-z_-]{20,}", c.get("id", "")) for c in children), "registry: Drive id shape drift")
policy = drive.get("policy", {})
req(policy.get("copyrightedFullTextUploadAllowed") is False, "registry: Drive rights boundary drift")
req(policy.get("fullTextAllowedOnlyWhenRightsVerified") is True, "registry: Drive PD-verification rule drift")

# ----------------------------------------------------------- primary texts ---
primary = texts["primary"]
req("SECOND HEAD OF DOCTRINE" in primary or "Head II" in primary, "primary dossier: Dort head drift")
for art in range(1, 10):
    req(f"ARTICLE {['I','II','III','IV','V','VI','VII','VIII','IX'][art-1]}." in primary, f"primary dossier missing Dort article {art}")
req("abundantly sufficient to expiate the sins of the whole world" in primary, "primary dossier: Dort II/III wording drift")
req("all those, and those only, who were from eternity chosen" in primary, "primary dossier: Dort II/VIII wording drift")
req("promiscuously and without distinction" in primary, "primary dossier: Dort II/V wording drift")
req("Rejection of Errors" in primary, "primary dossier: Dort errors/rejections boundary drift")
req("expiation made by Christ, extends to all who by faith embrace the gospel" in primary, "primary dossier: Calvin wording drift")
claims_in_primary = set(re.findall(r"`(RED-CLM-\d{3})`", primary))
claims_in_registry = {c.get("id") for c in data.get("claims", [])}
req(claims_in_primary == claims_in_registry, f"claim mirror drift: {sorted(claims_in_primary ^ claims_in_registry)}")
req(
    len(data.get("claims", [])) == 7
    and all(c.get("status") == "SUPPORTED_BY_VERIFIED_PRIMARY_TEXT" for c in data.get("claims", [])),
    "registry: claim status drift",
)
pt = data.get("primaryTexts", [])
req(len(pt) == 2, "registry: primary text count drift")
pre = data.get("drive", {}).get("preexistingObjects", {})
req(len(pre.get("bookCopies", [])) == 4, "registry: pre-existing book copies must be accounted for")
for b in pre.get("bookCopies", []):
    req(re.fullmatch(r"[0-9A-Za-z_-]{28,}", b.get("fileId", "")) is not None, "registry: book copy id shape drift")
    req(b.get("publicationState") == "HOLD" and b.get("rightsState") == "PD-CLAIM-UNVERIFIED", "registry: book copy boundary drift")
    req(b.get("bytes", 0) > 1_000_000, "registry: book copy byte size drift")
req("RECEIVED_UNHASHED" in texts["mirror"], "mirror receipt must record pre-existing books as unhashed")
req("не является" in texts["mirror"] and "sha256" in texts["mirror"], "mirror receipt lost the presence-is-not-receipt rule")
for entry in pt:
    req(entry.get("evidenceClass") in ALLOWED_CLASSES, "registry: primary text class drift")
    req(entry.get("publicationState") == "HOLD", "registry: primary text must stay on PUBLICATION_HOLD")
    req(entry.get("locatorState") == "LOCATOR_PARTIAL", "registry: primary text locator state drift")

# ------------------------------------------------------------- Drive mirror ---
mirror = texts["mirror"]
req(len(set(re.findall(r"`([0-9A-Za-z_-]{28,})`", mirror))) >= 11, "mirror receipt: drive-id column drift")
req(len(re.findall(r"`[0-9a-f]{64}`", mirror)) >= 11, "mirror receipt: sha256 column drift")
req(re.search(r"BOOKS RECEIVED\s*=\s*4 PD-COPIES PRESENT, 0 hash-verified RECEIVED receipts", mirror) is not None,
    "mirror receipt must state that book copies are present but zero are hash-verified receipts")
req(re.search(r"COPYRIGHTED FULL TEXT PLACED\s*=\s*0", mirror) is not None, "mirror receipt lost the no-copyrighted-full-text boundary")
req(mirror.count("| `") >= 11, "mirror receipt: fewer rows than mirrored objects")
req("не является" in mirror.lower() and "приёмк" in mirror.lower(), "mirror receipt must disclaim being an acquisition receipt")
mirror_state = data.get("drive", {}).get("mirror", {})
req(mirror_state.get("objectsMirrored") == 11, "registry: mirror object count drift")
req(mirror_state.get("rowsInReceiptTable") == 12, "registry: mirror table row count drift")
req(mirror_state.get("staleObjects") == 0, "registry: a stale mirror must be declared, not hidden")
req(len(mirror_state.get("objectsBehindByOneRevision", [])) == 3, "registry: mirror-lag declaration drift")
req("MIRROR-LAG" in texts["mirror"], "mirror receipt must name the lagging objects explicitly")
req("STALE" in texts["mirror"], "mirror receipt must state the stale-object verdict")
req(mirror_state.get("bookFullTextsMirrored") == 0, "registry: mirror must not count books")
req(mirror_state.get("conversionToGoogleDocs") is False, "registry: mirror conversion drift")
req(Path(mirror_state.get("receiptFile", "")).exists(), "registry: mirror receipt file missing")

# ------------------------------------------------------------- the intro pair ---
req("SUPERSEDED" not in texts["index"], "index: silent-supersession marker not allowed here")
req(json.dumps(data.get("introductions", []), ensure_ascii=False).count('"role"') == 1, "registry: exactly one terminology owner allowed")
req((CORPUS / "01_VVEDENIE_TERMINY_I_OPREDULENIYA_2026-10-07.md").exists() is False,
    "a second introduction reappeared: adjudicate it against the spine instead of leaving two owners")
hist = json.dumps(data.get("spineHistory", {}), ensure_ascii=False)
for marker in ("notCarriedOver", "reestablished", "ruleIfTheyReappear", "01_VVEDENIE_TERMINY"):
    req(marker in hist, f"registry: spineHistory missing {marker}")
for entry in data.get("introductions", []):
    req(Path(entry.get("file", "")).exists(), "registry: introduction file missing")

# --------------------------------------------------------- product boundary ---
product = texts["product"]
req("DO NOT IMPLEMENT" in product, "product proposal lost its do-not-implement banner")
req(product.count("/articles/") >= 12, "product proposal: launch article set drift")
req("section" in product and "content.config.ts" in product, "product proposal: schema-gate note drift")
req("route-search-policy" in product, "product proposal: route registration drift")
req("glossary" in product and "original-words" in product, "product proposal: terminology layer drift")
for row in re.findall(r"^\|\s*\d+\s*\|\s*`(/articles/[a-z0-9-]+)`", product, re.M):
    req(re.fullmatch(r"/articles/[a-z0-9-]+", row) is not None, f"product route violates slug regex: {row}")
    req("ограниченн" not in row, f"product route carries a polemical label: {row}")
pa = data.get("publicationArchitecture", {})
req(pa.get("status") == "PROPOSAL_DO_NOT_IMPLEMENT_UNTIL_W6", "registry: product status drift")
req(pa.get("directPushToProductMainAllowed") is False, "registry: product write boundary drift")
req(pa.get("articleCountIsOpenEnded") is True, "registry: article count must stay open-ended")

# ---------------------------------------------------------------- waves/RQs ---
waves = data.get("waves", [])
req([w.get("id") for w in waves] == [f"W{i}" for i in range(8)], "registry: wave spine drift")
req(sum(1 for w in waves if w.get("status") == "NOT_STARTED") == 6, "registry: wave status drift")
req([w for w in waves if w.get("id") == "W6"][0].get("status") == "GATE_NOT_OPEN", "registry: W6 gate drift")
charter = texts["charter"]
for wave in [f"W{i}" for i in range(8)]:
    req(wave in charter, f"charter missing wave {wave}")
rq = data.get("researchQuestion", {})
req(rq.get("subQuestions") == [f"RQ-{i}" for i in range(1, 7)], "registry: research-question spine drift")
for key, path in rq.get("subQuestionFiles", {}).items():
    req(Path(path).exists(), f"registry: {key} points at missing file {path}")

# ------------------------------------------------------ verification & holds ---
ver = data.get("verification", {})
req(ver.get("publicationEligible") is False, "registry: publicationEligible must be false")
req(ver.get("quotationsPageVerified") == 0, "registry: quotationsPageVerified must be 0 in Wave 0")
holds = data.get("holds", {})
req(set(holds) == {"EVIDENCE", "LOCATOR", "ARCHIVE", "RIGHTS", "PUBLICATION"}, "registry: hold ledger drift")
req(all(v for v in holds.values()), "registry: empty hold category")
req(
    "CLOSED_WITH_HOLDS" in json.dumps(ver),
    "registry: closure statement must state CLOSED_WITH_HOLDS",
)

# ------------------------------------------------------------- index hygiene ---
index = texts["index"]
for key, name in F.items():
    if key == "index":
        continue
    req(name in index, f"index does not list corpus file {name}")
present = {p.name for p in CORPUS.glob("*.md")}
listed = set(re.findall(r"`(\d{2}_[A-Z0-9_]+\.md)`", index)) | set(F.values())
for orphan in sorted(present - listed):
    errors.append(f"corpus file absent from index: {orphan}")
for ghost in sorted(listed - present):
    errors.append(f"index lists a file that does not exist: {ghost}")
req("Research closure ≠ Product" in index, "index: authority-boundary line drift")
req(DRIVE_ROOT in index, "index: Drive root drift")

if errors:
    print("REDEMPTION CORPUS INTEGRITY: FAIL")
    for err in errors:
        print(f"  - {err}")
    sys.exit(1)

notes.append(
    "W0 spine verified: {total} scripture loci, {src} source records, {fam} acquisition families, "
    "0 verified original-language strings, 0 page-verified quotations, publicationEligible=false".format(
        total=EXPECTED_TOTAL, src=EXPECTED_SOURCE_RECORDS, fam=EXPECTED_FAMILIES
    )
)
for n in notes:
    print(f"  note: {n}")
print("REDEMPTION CORPUS INTEGRITY: PASS")
