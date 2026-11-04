#!/usr/bin/env python3
"""Fail-closed, read-only validator for the RESEARCH Reformation corpus.

Run from any directory:
  python docs/research/reformation/validate_corpus.py

Checks only local repository files. Never downloads, publishes, deletes or writes.
It cannot prove historical truth, legal reuse rights or visual manuscript collation.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
POLICY_PATH = ROOT / "data" / "repository-evidence-policy-v2.json"
EXPECTED_ORIGINAL_GIT_BLOB = "4e34cfe0e21d6b1e3d62c7adc04a44e227679ba0"
SOURCE_ID_RE = re.compile(r"^REF-[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)*$")
CLAIM_RE = re.compile(r"^\|\s*(C\d{2,})\s*\|", re.MULTILINE)
MD_LINK_RE = re.compile(r"\]\(([^)]+)\)")
EXACT_REF_RE = re.compile(r"\bREF-(?:P|S|C)\d\d(?:-[A-Z0-9]+)*\b")
REQUIRED_SOURCE = {
    "id", "documentYear", "title", "evidenceClass", "accessState",
    "locatorState", "rightsState", "publicationState", "holds",
    "url", "verificationNote",
}


def json_read(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def git_blob_sha(data: bytes) -> str:
    header = b"blob " + str(len(data)).encode("ascii") + b"\0"
    return hashlib.sha1(header + data).hexdigest()


def validate() -> tuple[list[str], dict[str, int]]:
    problems: list[str] = []
    policy = json_read(POLICY_PATH)
    source = json_read(HERE / "source-registry-v1.json")
    manifest = json_read(HERE / "acquisition-manifest-v1.json")
    rows = source.get("sources", [])
    corpus = {item.get("id"): item for item in rows if isinstance(item, dict)}
    if source.get("sourceCount") != len(rows):
        problems.append("registry sourceCount differs from row count")
    if len(corpus) != len(rows):
        problems.append("duplicate or missing source IDs")
    enum_fields = {
        "evidenceClass": set(policy["sourceClasses"]),
        "accessState": set(policy["accessStates"]),
        "locatorState": set(policy["locatorStates"]),
        "rightsState": set(policy["rightsStates"]),
        "publicationState": set(policy["publicationStates"]),
    }
    holds_allowed = set(policy["holds"])
    for i, item in enumerate(rows):
        if not isinstance(item, dict):
            problems.append(f"source row {i} is not an object")
            continue
        name = str(item.get("id", f"index:{i}"))
        if not SOURCE_ID_RE.fullmatch(name):
            problems.append(f"invalid source ID: {name}")
        missing = REQUIRED_SOURCE - set(item)
        if missing:
            problems.append(f"{name} missing fields: {sorted(missing)}")
        for key, allowed in enum_fields.items():
            if item.get(key) not in allowed:
                problems.append(f"{name}: invalid {key}={item.get(key)}")
        hs = item.get("holds")
        if not isinstance(hs, list):
            problems.append(f"{name}: holds must be a list")
            continue
        for h in hs:
            if h not in holds_allowed:
                problems.append(f"{name}: unknown hold {h}")
        if item.get("publicationState") != "REFERENCE":
            problems.append(f"{name}: publication status not REFERENCE; manual audit required")
        if "PUBLICATION_HOLD" not in hs:
            problems.append(f"{name}: missing PUBLICATION_HOLD")
        if item.get("accessState") == "FULL_OBJECT_VERIFIED" and "ARCHIVE_HOLD" in hs:
            problems.append(f"{name}: FULL_OBJECT_VERIFIED with ARCHIVE_HOLD: review status")
    items = manifest.get("sourceRecords", [])
    if manifest.get("sourceCount") != len(items):
        problems.append("acquisition sourceCount differs from row count")
    if len({x.get("id") for x in items}) != len(items):
        problems.append("duplicate acquisition IDs")
    if manifest.get("fileBytesInGit") != 0:
        problems.append("manifest no longer states zero binary file bytes in Git")
    for record in items:
        name = record.get("id")
        parent_id = record.get("parentSourceId")
        if name not in corpus:
            # An individual acquired edition can be a child of a registered
            # umbrella work. The parent relation MUST be explicitly recorded.
            if not (
                parent_id in corpus
                and isinstance(name, str)
                and name.startswith(parent_id + "-")
                and SOURCE_ID_RE.fullmatch(name)
            ):
                problems.append(
                    f"acquisition entry {name} lacks an explicit valid parentSourceId"
                )
        elif parent_id is not None:
            problems.append(
                f"acquisition {name}: parentSourceId is redundant for a registered source"
            )
        sha = record.get("sha256")
        state = record.get("acquisitionState", "")
        permitted_states = {
            "NOT_DOWNLOADED", "DOWNLOAD_ATTEMPT_FAILED",
            "LINKS_VERIFIED_NO_DOWNLOAD", "VERIFIED_TEMP_DISCARDED",
            "DOWNLOADED_VERIFIED",
        }
        if state not in permitted_states:
            problems.append(f"acquisition {name}: unknown acquisitionState {state}")
        if sha is not None and not re.fullmatch(r"[a-f0-9]{64}", str(sha)):
            problems.append(f"acquisition {name} claims malformed SHA256")
        if state in {"VERIFIED_TEMP_DISCARDED", "DOWNLOADED_VERIFIED"}:
            if sha is None:
                problems.append(f"acquisition {name}: verified bytes without hash")
            if not isinstance(record.get("actualBytes"), int) or record["actualBytes"] <= 0:
                problems.append(f"acquisition {name}: verified bytes without positive size")
        elif sha is not None:
            problems.append(f"acquisition {name}: hash for an unverified download")
        if state == "VERIFIED_TEMP_DISCARDED":
            if not isinstance(record.get("tempDisposition"), str) or "TEMP_CLEANED=True" not in record["tempDisposition"]:
                problems.append(f"acquisition {name}: discarded download has no cleanup proof")
    # BSB 1527: verify a witnessed digital acquisition, not a fictitious
    # full critical collation. The inventory holds SHA digests of 1200px
    # generated IIIF JPEGs, NOT masters, manuscripts, or printed words.
    bsb = json_read(HERE / "bsb-1527-iiif-derivatives-v1.json")
    objects = bsb.get("objects", [])
    scans = bsb.get("scans", [])
    targets = {
        "bsb00027178": ("REF-P24-BSB1", 32, 32, 0),
        "bsb00112324": ("REF-P24-BSB2", 34, 32, 2),
    }
    if bsb.get("schemaVersion") != 1:
        problems.append("BSB image receipt schemaVersion != 1")
    if len(objects) != 2 or {o.get("id") for o in objects} != set(targets):
        problems.append("BSB object inventory must contain two specific witnesses")
    if len(scans) != 66:
        problems.append("BSB 1527 receipts not exactly 66 scanned images")
    if not bsb.get("tempFilesDeletedAtManifestConstruction"):
        problems.append("BSB verification did not confirm temporary cleanup")
    for flag in (
        "masterImagesDownloaded", "printerTextFullyTranscribed",
        "allPrintedPagesWordByWordCollated", "originalPhotosCommittedToGit",
    ):
        if bsb.get(flag) is not False:
            problems.append(f"BSB not-verified flag altered: {flag}")
    for obj in objects:
        name = obj.get("id")
        if name not in targets:
            continue
        src, count, printed, extra = targets[name]
        if (obj.get("sourceId"), obj.get("canvases"),
            obj.get("printedPages"), obj.get("additionalTargets")) != (
                src, count, printed, extra
            ):
            problems.append(f"BSB {name}: wrong metadata / printed page count")
        if obj.get("manifestUrl") != (
            f"https://api.digitale-sammlungen.de/iiif/presentation/v2/{name}/manifest"
        ):
            problems.append(f"BSB {name}: wrong manifest URL")
        if not re.fullmatch(r"[a-f0-9]{64}", str(obj.get("manifestSha256"))):
            problems.append(f"BSB {name}: malformed manifest SHA")
        if not isinstance(obj.get("manifestBytes"), int) or obj["manifestBytes"] <= 0:
            problems.append(f"BSB {name}: manifest length invalid")
        rec = next((x for x in items if x.get("id") == src), {})
        if (rec.get("sha256"), rec.get("actualBytes")) != (
            obj.get("manifestSha256"), obj.get("manifestBytes")
        ):
            problems.append(f"BSB {name}: acquisition manifest SHA/bytes contradict IIIF receipt")
        if rec.get("derivativeReceipts") != "bsb-1527-iiif-derivatives-v1.json":
            problems.append(f"BSB {name}: missing derivative receipt link")
        if rec.get("acquisitionState") != "VERIFIED_TEMP_DISCARDED":
            problems.append(f"BSB {name}: acquisition status missing verified-discarded")
        entry = corpus.get(src, {})
        if entry.get("accessState") != "PARTIAL_OBJECT":
            problems.append(f"BSB {src}: must remain PARTIAL_OBJECT without full collation")
        if entry.get("locatorState") != "EXACT_LOCATOR_VERIFIED":
            problems.append(f"BSB {src}: scan locators not verified")
        if "ARCHIVE_HOLD" not in entry.get("holds", []):
            problems.append(f"BSB {src}: missing full-text-collation ARCHIVE_HOLD")
    seen_scans: set[tuple[str, int]] = set()
    for row in scans:
        obj = row.get("objectId")
        page = row.get("scan")
        key = (obj, page)
        if obj not in targets or not isinstance(page, int):
            problems.append(f"BSB bad image key: {key}")
            continue
        max_page = targets[obj][1]
        if not (1 <= page <= max_page):
            problems.append(f"BSB page outside object: {key}")
        if key in seen_scans:
            problems.append(f"BSB duplicate image: {key}")
        seen_scans.add(key)
        expected_kind = (
            "color-calibration-target" if obj == "bsb00112324" and page == 33
            else "resolution-calibration-target" if obj == "bsb00112324" and page == 34
            else "printed-page"
        )
        if row.get("kind") != expected_kind:
            problems.append(f"BSB {key}: wrong printed/calibration kind")
        expected_url = (
            f"https://api.digitale-sammlungen.de/iiif/image/v2/"
            f"{obj}_{page:05d}/full/1200,/0/default.jpg"
        )
        if row.get("url") != expected_url:
            problems.append(f"BSB {key}: wrong IIIF source URL")
        if not re.fullmatch(r"[a-f0-9]{64}", str(row.get("sha256"))):
            problems.append(f"BSB {key}: malformed derivative SHA")
        if not isinstance(row.get("bytes"), int) or row.get("bytes") <= 0:
            problems.append(f"BSB {key}: derivative byte count invalid")
    for obj, (_, count, _, _) in targets.items():
        if {n for name, n in seen_scans if name == obj} != set(range(1, count + 1)):
            problems.append(f"BSB {obj}: missing image sequence members")
    if sum(s.get("bytes", 0) for s in scans if isinstance(s.get("bytes"), int)) != 24526953:
        problems.append("BSB 1527 verified byte total drifted without re-acquisition")
    claims = (HERE / "03_claim_verification_register.md").read_text(encoding="utf-8")
    ids = [int(m.group(1)[1:]) for m in CLAIM_RE.finditer(claims)]
    if ids != list(range(1, len(ids) + 1)):
        problems.append("claim IDs are not unique, continuous and in numeric order")
    for line in claims.splitlines():
        if not CLAIM_RE.match(line):
            continue
        claim_id = CLAIM_RE.match(line).group(1)
        for ref in EXACT_REF_RE.findall(line):
            if ref not in corpus:
                problems.append(f"{claim_id}: undefined source reference {ref}")
    # Contract regression checks: a valid ID could still refer to the wrong topic.
    semantic = {
        "C21": ("REF-S09", "REF-S07"),
        "C49": ("REF-P34", None),
        "C50": ("REF-S08", None),
        "C55": ("REF-P31", None),
        "C75": ("REF-P39", None),
        "C77": ("REF-S13", None),
        "C78": ("REF-S13", None),
        "C79": ("REF-P40", None),
        "C82": ("REF-P42", None),
        "C84": ("REF-P43", None),
    }
    claim_rows = {CLAIM_RE.match(s).group(1): s for s in claims.splitlines() if CLAIM_RE.match(s)}
    for id_, (required, forbidden) in semantic.items():
        row = claim_rows.get(id_, "")
        if required not in row:
            problems.append(f"{id_}: missing mandatory topic source {required}")
        if forbidden and forbidden in row:
            problems.append(f"{id_}: stale conflicting source {forbidden}")
    if "1542" not in str(corpus.get("REF-P31", {}).get("verificationNote", "")):
        problems.append("REF-P31 provenance no longer identifies 1542 printed base")
    if "2016" not in str(corpus.get("REF-P34", {}).get("verificationNote", "")):
        problems.append("REF-P34 provenance no longer identifies 2016 conservation")
    # Worms 1521 witness hierarchy and digitization rights are substantive
    # provenance constraints, not permissions to publish any part of the corpus.
    worms = {
        "REF-P39": ("PARTIAL_OBJECT", "PERMISSION_REQUIRED"),
        "REF-P40": ("PARTIAL_OBJECT", "PUBLICATION_ELIGIBLE"),
        "REF-P41": ("PARTIAL_OBJECT", "PUBLICATION_ELIGIBLE"),
        "REF-P42": ("PARTIAL_OBJECT", "RIGHTS_UNKNOWN"),
        "REF-P43": ("PARTIAL_OBJECT", "PERMISSION_REQUIRED"),
        "REF-S13": ("PARTIAL_OBJECT", "PUBLICATION_ELIGIBLE"),
        "REF-S14": ("PARTIAL_OBJECT", "PERMISSION_REQUIRED"),
        "REF-P44": ("PARTIAL_OBJECT", "PERMISSION_REQUIRED"),
        "REF-P45": ("PARTIAL_OBJECT", "PERMISSION_REQUIRED"),
        "REF-P46": ("PARTIAL_OBJECT", "RIGHTS_UNKNOWN"),
        "REF-P47": ("PARTIAL_OBJECT", "PERMISSION_REQUIRED"),
        "REF-P48": ("PARTIAL_OBJECT", "RIGHTS_UNKNOWN"),
        "REF-S15": ("PARTIAL_OBJECT", "PERMISSION_REQUIRED"),
        "REF-S16": ("PARTIAL_OBJECT", "RIGHTS_UNKNOWN"),
    }
    for ref, (access, rights) in worms.items():
        w = corpus.get(ref, {})
        if w.get("accessState") != access or w.get("rightsState") != rights:
            problems.append(f"{ref}: Worms witness accessibility/rights regression")
        if "PUBLICATION_HOLD" not in w.get("holds", []):
            problems.append(f"{ref}: Worms publication hold unexpectedly removed")
        if "ARCHIVE_HOLD" not in w.get("holds", []):
            problems.append(f"{ref}: Worms uncollated primary-object hold removed")
    for id_, substrings in {
        "C75": ("REF-P39", "REF-S14", "формула"),
        "C77": ("REF-P40", "REF-S13", "26"),
        "C79": ("REF-P40", "A1r", "B4"),
        "C84": ("REF-P43", "GHDI"),
        "C85": ("REF-P44", "REF-P46", "REF-S15", "1521", "S.556", "NOT_INDEPENDENT"),
        "C86": ("REF-P44", "REF-P46", "REF-P39", "REF-P45", "REF-P47"),
        "C87": ("REF-P39", "REF-P44", "REF-S15"),
        "C88": ("REF-S15", "F add", "Q add", "S.570", "S.582", "NOT_INDEPENDENT"),
        "C89": ("REF-P45", "Neyn"),
        "C90": ("REF-S15", "S.583"),
        "C91": ("REF-S15", "REF-S16", "REF-S14", "S.556"),
        "C92": ("REF-P47", "REF-S15", "nit anderst", "19 апреля", "NOT_STENOGRAPHY"),
        "C93": ("REF-P47", "Lucifer", "ZV23319", "не"),
        "C94": ("REF-P48", "Reg. E 81", "обрывается", "INCOMPLETE_AUTOGRAPH_NOT_SPOKEN_CONCLUSION"),
    }.items():
        row = claim_rows.get(id_, "")
        if any(term not in row for term in substrings):
            problems.append(f"{id_}: incomplete Worms first-print legal chronology or citation")
    # Sixteen 1800px JPEG derivatives were viewed and discarded in two
    # source-critical acquisition batches. This read-only check validates
    # recorded bytes and provenance, NOT live remote bytes or publication rights.
    wrede = (HERE / "12_worms_1521_speech_edict_source_dossier.md").read_text(
        encoding="utf-8")
    if "### Текстологическая колляция" not in wrede:
        problems.append("Wrede 1896 visual collation section missing")
        wrede_section = ""
    else:
        wrede_section = wrede.split("### Текстологическая колляция", 1)[1].split(
            "### P40.", 1)[0]
    receipts = re.findall(
        r"^\|\s*(\d{3})\s*\|\s*(\d{3})\s*\|\s*(\d+)\s*\|\s*\x60([a-f0-9]{64})\x60\s*\|$",
        wrede_section, re.MULTILINE)
    expected_pages = list(range(578, 585)) + [554, 555, 556] + list(range(569, 575))
    if [(p, scan) for p, scan, _, _ in receipts] != [
            (str(p), str(p+16)) for p in expected_pages]:
        problems.append("Wrede 1896 exact 16-page IIIF acquisition receipts incomplete")
    if len({sha for _, _, _, sha in receipts}) != 16:
        problems.append("Wrede 1896 SHA receipts missing, repeated or malformed")
    lengths = [
        556830, 561385, 540789, 572148, 600618, 627903, 526127,
        532242, 517396, 578474, 568107, 520336, 588611,
        641510, 569756, 577411,
    ]
    if [int(size) for _, _, size, _ in receipts] != lengths:
        problems.append("Wrede 1896 downloaded JPEG byte counts changed")
    expected_sha = [
        "fc65a7e41da0daba033dd151c611132ecfa0e335477e22e065234f2eca7202ca",
        "9f2ce265b268174454df83a65647d6863c6f1e5332b5a47339f9aaef17bad9c0",
        "c85ba0f11b3de3c56091032c057f649ed4fe3ebf18ce273c47a1b46546d04316",
        "c875be511e67cea417d2f16ac5b595fd7f041e38fef5cfdd3190e8086072f615",
        "06f2453a6b055ef0d8900d98910338cf50dd8cfe43d04f597129fbc0d1f94c72",
        "f762fb6261c45a2031cda9b602ceb13ce0c329b1a7ed0587d05a6487be78e383",
        "7744574be57fb5de638612553662066659f94bf6ab1f23758f7b30168a091788",
        "56c3e7c8456f746b7641995d9f85a67cd910711c8688a98a1a64dba8ffd03dbb",
        "7c66c9a38b95078072fcd03185865cb68b94a73a07c165437e2a714f89181def",
        "8135bce780447c78bc63c5d6b917260b94dbb78050da597e9c85a693a6f54da4",
        "6211b4ef0c91287b2c616897cd2f158909a692b8c65dedb2edf123435301ce9e",
        "9139d864063b8b21f37fb74c6e7c0e82e59f1ae631c22961c8c81f01c5c1cd97",
        "af65ab1af979d3186f8d8352c98494ff06781602c3c0a8706f0c99df6ffed9a6",
        "6ce0ac28cc69f1920230d62efd0c30fae3d4568fc7c9aadd28ef7bc846b57fd7",
        "6f77a837fdb776ca246b52a942a44be3031fdc7bd0ad4f13a14dbd35a7f231e7",
        "d17d21c0e0c6752092c6d4c8750f04e946360ddd2f16f1ba753fe46340db2725",
    ]
    if [sha for _, _, _, sha in receipts] != expected_sha:
        problems.append("Wrede 1896 SHA receipts changed without verified re-acquisition")
    for proof in (
            "F add. Ich kan nicht anders, hie stehe ich",
            "Q add. Ich kan nicht anderst, hie stehe ich",
            "F ist jedenfalls ein Nachdruck von U",
            "не два независимых источника",
            "НЕ два независимых подтверждения",
            "S.556", "S.570", "S.571", "S.573",
            "F/Fa/Q", "NoC-NC/1.0"):
        if proof not in wrede_section:
            problems.append(f"Wrede source stemma/evidence independence guard missing: {proof}")
    if "NoC-NC/1.0" not in wrede_section:
        problems.append("Wrede BSB digital photograph usage restriction removed")
    if "TEMP_CLEANED=True" not in wrede_section:
        problems.append("Wrede temporary photos cleanup not attested")
    if "TWO_INDEPENDENT_1521_PRINT_PAGES_VISUALLY_CHECKED" in claim_rows.get("C85", ""):
        problems.append("Worms C85 falsely counts F/Q as two independent oral sources")
    if "NOT_INDEPENDENT" not in claim_rows.get("C85", ""):
        problems.append("Worms C85 missing print-dependence qualification")
    if "NOT_INDEPENDENT" not in claim_rows.get("C88", ""):
        problems.append("Worms C88 missing critical F/Q stemma verdict")
    s15_note = corpus.get("REF-S15", {}).get("verificationNote", "")
    for proof in ("no.79", "pp554-556", "pp569-574", "F Nachdruck von U",
                  "NOT two independent oral witnesses", "16 files", "TEMP_CLEANED=True"):
        if proof not in s15_note:
            problems.append(f"Wrede source registry has lost verified original-print context: {proof}")
    # LMU VD16 L3650 original three-page PDF was actually visually inspected;
    # receipts pin the downloaded PDF bytes, not a live network reacquisition.
    p46 = corpus.get("REF-P46", {})
    if p46.get("locatorState") != "EXACT_LOCATOR_VERIFIED":
        problems.append("Wittenberg Latin 1521 original PDF locator must stay verified")
    if p46.get("url") != "https://epub.ub.uni-muenchen.de/14521/":
        problems.append("Wittenberg Latin 1521 LMU item permalink changed")
    if "LOCATOR_HOLD" in p46.get("holds", []):
        problems.append("Wittenberg Latin 1521 checked leaf falsely still catalog-only")
    if not {"RIGHTS_HOLD", "PUBLICATION_HOLD", "ARCHIVE_HOLD"} <= set(p46.get("holds", [])):
        problems.append("Wittenberg Latin 1521 unresolved photo rights or attribution hold removed")
    latin_pdf = "https://epub.ub.uni-muenchen.de/14521/1/4Luth.209_7.pdf"
    latin_sha = "2b7bd600f28d1805a46d2d3b577c6f01dbbd2b21a7e70caa8ead518c037edb4f"
    latin_note = p46.get("verificationNote", "")
    if any(token not in latin_note for token in
           (latin_pdf, latin_sha, "2451627", "TEMP_CLEANED=True", "not oral stenography")):
        problems.append("Wittenberg Latin 1521 checked PDF identity/interpretation receipt missing")
    if any(token not in wrede_section for token in
           (latin_pdf, latin_sha, "2451627", "TEMP_CLEANED=True", "PDF 2")):
        problems.append("Wittenberg Latin 1521 visual receipt missing from dossier 12")
    if "REF-P46" not in claim_rows.get("C85", "") or "REF-P46" not in claim_rows.get("C86", ""):
        problems.append("Latin 1521 print disconnected from comparative claims C85-C86")
    # Augsburg VD16 A3024 is a genuine photographed early PRINT, but not
    # Peutinger's original 19 April letter or an independent verbatim speech.
    p47 = corpus.get("REF-P47", {})
    p47_note = str(p47.get("verificationNote", ""))
    p47_pdf = "https://www.dilibri.de/stbwo/download/pdf/2040713"
    p47_sha = "4fd0fb21456c815bb6d701307bdfe97eeae9080f27aea7b64a1072659a48fe79"
    if p47.get("url") != "https://www.dilibri.de/urn/urn:nbn:de:0128-5-2820":
        problems.append("Augsburg 1521 P47 library locator changed")
    if p47.get("locatorState") != "EXACT_LOCATOR_VERIFIED":
        problems.append("Augsburg 1521 P47 original PDF locator no longer verified")
    if not {"ARCHIVE_HOLD", "RIGHTS_HOLD", "PUBLICATION_HOLD"} <= set(p47.get("holds", [])):
        problems.append("Augsburg 1521 P47 letter/print rights hold removed")
    if any(token not in p47_note for token in
           (p47_pdf, p47_sha, "3253175", "ALL 16", "TEMP_CLEANED=True",
            "original manuscript/letter was NOT photographed",
            "NOT a stenographic transcript", "Pope pamphlet",
            "NOT on-site iconography", "CC BY-NC-SA 3.0")):
        problems.append("Augsburg 1521 P47 visual receipt, independence or rights lost")
    if any(token not in wrede_section for token in
           (p47_pdf, p47_sha, "3253175", "PDF", "кадре 10",
            "самого автора сообщения", "не** сказанная Лютером",
            "Пейтингера", "VD16 ZV23319")):
        problems.append("Augsburg P47 primary-print/curatorial limits absent from dossier")
    if any(token not in claim_rows.get("C92", "") for token in
           ("REF-P47", "Got kum mir zehülff", "nit anderst",
            "PRINTED_REPORT_NOT_AUTOGRAPH_NOT_STENOGRAPHY")):
        problems.append("C92 P47 narrative voice misattribution or source lost")
    if any(token not in claim_rows.get("C93", "") for token in
           ("REF-P47", "ZV23319", "ORIGINAL_TITLE_IMAGE_VISUALLY_CHECKED",
            "RECYCLED_PROPAGANDA_IMAGE_NOT_EVENT_RECORD")):
        problems.append("C93 P47 recycled woodcut context lost")
    p47_receipt = next((rec for rec in items if rec.get("id") == "REF-P47"), {})
    if (p47_receipt.get("acquisitionState") != "VERIFIED_TEMP_DISCARDED"
            or p47_receipt.get("sha256") != p47_sha
            or p47_receipt.get("actualBytes") != 3253175
            or p47_receipt.get("catalog") != p47.get("url")
            or p47_receipt.get("downloadAccess") != p47_pdf
            or p47_receipt.get("accessState") != "PARTIAL_OBJECT"
            or p47_receipt.get("locatorState") != "EXACT_LOCATOR_VERIFIED"
            or p47_receipt.get("publicationState") != "REFERENCE"):
        problems.append("Augsburg P47 acquisition manifest no longer matches verified source bytes")
    if any(token not in str(p47_receipt.get("rights", "")) for token in
           ("CC BY-NC-SA 3.0", "RIGHTS_HOLD", "PUBLICATION_HOLD")):
        problems.append("Augsburg P47 acquisition image-reuse restrictions lost")
    if "TEMP_CLEANED=True" not in str(p47_receipt.get("tempDisposition", "")):
        problems.append("Augsburg P47 canonical temp cleanup receipt missing")
    if "| REF-P47 |" not in (HERE / "02_open_primary_sources_and_reading.md").read_text(
            encoding="utf-8"):
        problems.append("Augsburg P47 missing from primary-source reading list")
    # The Weimar autograph Reg E 81 is an incomplete physical draft seen
    # via institutional museum photography, NOT an acquired full facsimile,
    # stenographic transcript, or proof of what Luther said at the ending.
    p48 = corpus.get("REF-P48", {})
    p48_note = str(p48.get("verificationNote", ""))
    p48_url = ("https://artsandculture.google.com/asset/"
               "luther%E2%80%99s-address-before-the-imperial-diet-in-worms-"
               "notes-in-his-own-hand-martin-luther/uAEBA1Vc8H_uCQ?hl=en")
    if p48.get("url") != p48_url:
        problems.append("Weimar 1521 autograph Reg E81 museum photo locator changed")
    if p48.get("locatorState") != "EXACT_LOCATOR_VERIFIED":
        problems.append("Weimar Reg E81 autograph precise archive locator lost")
    if not {"ARCHIVE_HOLD", "RIGHTS_HOLD", "PUBLICATION_HOLD"} <= set(p48.get("holds", [])):
        problems.append("Weimar Reg E81 manuscript/full-reuse hold removed")
    if any(token not in p48_note for token in (
            "Reg. E 81", "UNESCO", "Morgan Library",
            "BREAKS OFF IN THE MIDDLE OF A SENTENCE",
            "NOT a complete speech record", "NO downloaded photo",
            "NO new acquisition-manifest row", "full institutional scan")):
        problems.append("Weimar Reg E81 partial autograph provenance/limits lost")
    if any(token not in wrede_section for token in (
            "### P48.", "Reg. E 81", "музейной фотографии",
            "обрывается посреди предложения", "13 записями",
            "не доказательство, что фраза не прозвучала",
            "RIGHTS_HOLD / PUBLICATION_HOLD")):
        problems.append("Weimar Reg E81 incomplete autograph context absent from Worms dossier")
    if any(token not in claim_rows.get("C94", "") for token in (
            "REF-P48", "обрывается посреди предложения",
            "не доказывает ни произнесение, ни непроизнесение",
            "INCOMPLETE_AUTOGRAPH_NOT_SPOKEN_CONCLUSION")):
        problems.append("C94 Weimar autograph falsely promoted into completed speech conclusion")
    if any(rec.get("id") == "REF-P48" for rec in items):
        problems.append("Weimar autograph museum photo falsely inserted as downloaded acquisition")
    if "| REF-P48 |" not in (HERE / "02_open_primary_sources_and_reading.md").read_text(
            encoding="utf-8"):
        problems.append("Weimar Reg E81 autograph missing from primary source list")
    # Zurich research acquisition 2026-11-04: metadata manifest alone is NOT
    # a photographed or read 1523 original; the 1525 official PDF is a real
    # privately retained local copy, NOT released and NOT word-by-word collated.
    zwingli = corpus.get("REF-P09-PRINT", {})
    z_man = next((rec for rec in items if rec.get("id") == "REF-P09-PRINT"), {})
    z_meta = z_man.get("metadataReceipt", {})
    meta_sha = "367e21601ed4c3d66126977e0e4e83fc5792b04964861ed41e8a508ce1183fa7"
    if zwingli.get("accessState") != "CATALOG_ONLY" or zwingli.get("locatorState") != "EXACT_LOCATOR_VERIFIED":
        problems.append("Zurich 1523 image-blocked work falsely promoted to read source")
    if zwingli.get("rightsState") != "RIGHTS_UNKNOWN" or not {
            "ARCHIVE_HOLD", "RIGHTS_HOLD", "PUBLICATION_HOLD"} <= set(zwingli.get("holds", [])):
        problems.append("Zurich 1523 NoC-US/CNE image-rights discrepancy silently dropped")
    if z_man.get("acquisitionState") != "NOT_DOWNLOADED" or z_man.get("sha256") is not None:
        problems.append("Zurich 1523 original JPEGs falsely registered as downloaded")
    if (z_meta.get("sha256") != meta_sha or z_meta.get("actualBytes") != 90592
            or z_meta.get("canvases") != 29 or z_meta.get("physicalPrintedPages") != 16
            or z_meta.get("imageFilesDownloaded") != 0 or z_meta.get("retained") is not True):
        problems.append("Zurich 1523 verified bibliographic manifest receipt corrupted")
    if (z_meta.get("rightsManifest") != "https://rightsstatements.org/vocab/CNE/1.0/"
            or z_meta.get("rightsItem") != "https://rightsstatements.org/page/NoC-US/1.0/"):
        problems.append("Zurich 1523 conflicting image-rights metadata lost")
    if any(t not in str(zwingli.get("verificationNote", "")) for t in
           (meta_sha, "HTTP 403", "29", "16", "NoC-US", "CNE/1.0")):
        problems.append("Zurich 1523 original print metadata/copyright qualification lost")
    luther = corpus.get("REF-P07-ZRH", {})
    l_acq = next((rec for rec in items if rec.get("id") == "REF-P07-ZRH"), {})
    retained = l_acq.get("retainedLocalCopy", {})
    l_sha = "898107c6e63848aca753e8c0989520ffa3c008ca37bf33f7835bc6cfbbb49239"
    if (luther.get("accessState") != "PARTIAL_OBJECT"
            or luther.get("locatorState") != "EXACT_LOCATOR_VERIFIED"
            or "ARCHIVE_HOLD" not in luther.get("holds", [])):
        problems.append("Zurich 1525 original PDF access/partial transcription misclassified")
    if (l_acq.get("acquisitionState") != "DOWNLOADED_VERIFIED"
            or l_acq.get("actualBytes") != 8239895
            or l_acq.get("sha256") != l_sha
            or retained.get("sha256") != l_sha
            or retained.get("actualBytes") != 8239895
            or retained.get("storageClass") != "PRIVATE_RESEARCH_ONLY"):
        problems.append("Zurich 1525 verified retained PDF receipt inconsistent")
    if (retained.get("visuallyCheckedPages") != [5, 6, 7, 8, 14, 15, 16, 28, 29, 30]
            or retained.get("fullPageCollationCompleted") is not False):
        problems.append("Zurich 1525 claimed page/complete-collation status not supported")
    if "Luther_1525_Froschauer_VD16_L4693" not in str(retained.get("localRelativePath", "")):
        problems.append("Zurich 1525 private-retention destination missing")
    if not {"RIGHTS_HOLD", "PUBLICATION_HOLD"} <= set(luther.get("holds", [])):
        problems.append("Zurich 1525 private archive erroneously treated as publication permission")
    for claim_id, required in {
            "C95": ("REF-P09-PRINT", meta_sha, "NO_IMAGE_BYTES_NO_TEXT_COLLATION", "CNE/1.0"),
            "C96": ("REF-P09-PRINT", "27 января", "29 января", "DATE_HOLD_ON_EMORY_CARD"),
            "C97": ("REF-P07-ZRH", l_sha, "PERSISTENT_PRIVATE_SOURCE_NOT_PUBLICATION_APPROVAL"),
            "C98": ("REF-P07-ZRH", "p.6", "p.30", "SAMPLED_PRINTED_LEAVES_NOT_FULL_COLLATION"),
    }.items():
        if any(token not in claim_rows.get(claim_id, "") for token in required):
            problems.append(f"{claim_id}: Zurich evidence/hold regression")
    dossier_06 = (HERE / "06_primary_source_collation_2026-11-04.md").read_text(encoding="utf-8")
    for token in ("## 9. Реальное пополнение", meta_sha, l_sha,
                  "29 цифровых кадров", "NoC-US", "CNE/1.0",
                  "ЗВ", "частной библиотеке"):
        # A limited list of structural evidence/claims; cannot prove content
        # without reading external original images or their licensing terms.
        if token not in dossier_06 and token != "ЗВ":
            problems.append(f"Zurich main dossier lost audited evidence: {token}")
    # New genuine 1523 originals: short four-leaf 67-article print and
    # distinct 254-leaf commentary. Full PDF acquisition ≠ textual collation.
    z67 = corpus.get("REF-P09-ZRH-67", {})
    a67 = next((rec for rec in items if rec.get("id") == "REF-P09-ZRH-67"), {})
    z67_disk = a67.get("retainedLocalCopy", {})
    z67_sha = "6f7aa50455a95566c82328dc24f42907018ff6c882564a2da46cfcad2f1fe19f"
    if (z67.get("accessState") != "PARTIAL_OBJECT"
            or z67.get("locatorState") != "EXACT_LOCATOR_VERIFIED"
            or z67.get("rightsState") != "PUBLICATION_ELIGIBLE"
            or z67.get("publicationState") != "REFERENCE"
            or not {"ARCHIVE_HOLD", "PUBLICATION_HOLD"} <= set(z67.get("holds", []))):
        problems.append("Zwingli Z819 source rights/access prematurely promoted")
    if (a67.get("acquisitionState") != "DOWNLOADED_VERIFIED"
            or a67.get("actualBytes") != 3349092 or a67.get("sha256") != z67_sha
            or z67_disk.get("bytes") != 3349092
            or z67_disk.get("sha256") != z67_sha
            or z67_disk.get("historicalLeaves") != 4
            or z67_disk.get("digitalPages") != 13
            or z67_disk.get("originalPrintPdfPages") != list(range(2, 10))
            or z67_disk.get("firstNumberedArticle") != 1
            or z67_disk.get("lastNumberedArticle") != 67
            or z67_disk.get("allDigitalImagesViewed") is not True
            or z67_disk.get("fullWordByWordCollation") is not False
            or z67_disk.get("originalColophonPrinterConfirmed") is not False):
        problems.append("Zwingli Z819 four-leaf original scanned/retained receipt, text or printer limit altered")
    if ("Zwingli_1523_Froschauer_67_Theses_VD16_Z819"
            not in str(z67_disk.get("localRelativePath", ""))):
        problems.append("Zwingli Z819 original PDF destination lost")
    if any(x not in str(z67.get("verificationNote", "")) for x in
           (z67_sha, "13 DIGITAL", "67", "not a word-for-word", "LIBRARY BIBLIOGRAPHIC")):
        problems.append("Zwingli Z819 provenance or printing caveat lost")
    zlong = corpus.get("REF-P09-EXPLANATION", {})
    a_long = next((rec for rec in items if rec.get("id") == "REF-P09-EXPLANATION"), {})
    long_disk = a_long.get("retainedLocalCopy", {})
    long_sha = "3331c5863552131a3f3ad779bae0613b7651f499ed68fee40c8980a340ef77fa"
    if (zlong.get("accessState") != "PARTIAL_OBJECT"
            or zlong.get("locatorState") != "EXACT_LOCATOR_VERIFIED"
            or "ARCHIVE_HOLD" not in zlong.get("holds", [])
            or "PUBLICATION_HOLD" not in zlong.get("holds", [])):
        problems.append("Zwingli Z821 commentary research hold removed")
    if (a_long.get("acquisitionState") != "DOWNLOADED_VERIFIED"
            or a_long.get("sha256") != long_sha
            or a_long.get("actualBytes") != 136718994
            or long_disk.get("sha256") != long_sha
            or long_disk.get("bytes") != 136718994
            or long_disk.get("digitalPages") != 513
            or long_disk.get("historicalLeaves") != 254
            or long_disk.get("sampledPdfPages") != [1, 2, 3, 4, 5, 6]
            or long_disk.get("fullWordByWordCollation") is not False
            or long_disk.get("firsthandDisputationDateFromPreface") != "29 January 1523 at PDF p5"
            or long_disk.get("titleNumeralCriticalReading", {}).get("literalPrinted") != "XIX"
            or long_disk.get("titleNumeralCriticalReading", {}).get("editorialCorrection") != "XXIX"
            or long_disk.get("titleNumeralCriticalReading", {}).get("separateNineteenJanuaryDisputationEstablished") is not False):
        problems.append("Zwingli Z821 acquired 254-leaf original, date or incomplete collation altered")
    if ("Zwingli_1523_Froschauer_Usslegen_VD16_Z821"
            not in str(long_disk.get("localRelativePath", ""))):
        problems.append("Zwingli Z821 retained original PDF path missing")
    if any(x not in str(zlong.get("verificationNote", "")) for x in
           (long_sha, "29 tag Jenners", "513 DIGITAL", "XIX [sic]", "XXIX", "NOT complete")):
        problems.append("Zwingli 1523 original author dating/context lost")
    if (retained.get("wholePdfVisuallyInspected") is not True
            or retained.get("digitalPages") != 33
            or retained.get("historicalLeaves") != 14
            or retained.get("fullPageCollationCompleted") is not False
            or "Wittemberg" not in str(retained.get("titleImprint", ""))
            or "Zurich" not in str(retained.get("actualPrinterColophon", ""))):
        problems.append("Zurich 1525 Froschauer actual colophon/title and full visual PDF limits lost")
    for cid, substrings in {
        "C99": ("REF-P09-ZRH-67", z67_sha, "ZURICH_67_FULL_IMAGE_SEQUENCE_NOT_FULL_TRANSCRIPTION"),
        "C100": ("REF-P09-EXPLANATION", "29 января", "19 января", "1523_FIRST_PERSON_29_JAN_NOT_19_TITLE_OR_27_METADATA", "TITLE_XIX_SCHOLARLY_CORRECTED_TO_XXIX_NOT_SEPARATE_EVENT", "Wood"),
        "C101": ("REF-P09-EXPLANATION", long_sha, "FULL_BYTES_NOT_FULL_TRANSCRIPTION"),
        "C102": ("REF-P07-ZRH", "p.4", "p.30", "TITLE_WITTENBERG_COLOPHON_ZURICH"),
    }.items():
        if any(t not in claim_rows.get(cid, "") for t in substrings):
            problems.append(f"{cid}: new primary-copy acquisition/chronology evidence lost")
    source_readings = (HERE / "02_open_primary_sources_and_reading.md").read_text(encoding="utf-8")
    if not all(f"| {k} |" in source_readings for k in
               ("REF-P09-PRINT", "REF-P09-ZRH-67", "REF-P09-EXPLANATION")):
        problems.append("Three distinct 1523 printed witness entries improperly conflated")
    collation = (HERE / "06_primary_source_collation_2026-11-04.md").read_text(
        encoding="utf-8")
    if any(t not in collation for t in
           ("## 10. Два реально сохранённых", z67_sha, long_sha,
            "PDF p.5", "29 января 1523", "XIX", "XXIX", "Jon D. Wood", "254", "67", "Ramminger",
            "Wittemberg", "колофон", "PUBLICATION_HOLD")):
        problems.append("Zwingli original 1523 visual-page map or publisher limits lost")
    # Enforce source interpretation without inventing independent eyewitnesses:
    # a byte receipt cannot prove the letter autograph or oral delivery.
    for file in HERE.glob("*.md"):
        text = file.read_text(encoding="utf-8")
        for match in MD_LINK_RE.finditer(text):
            target = match.group(1).split("#", 1)[0].split("?", 1)[0]
            if not target or target.startswith(("http://", "https://", "mailto:")):
                continue
            resolved = (file.parent / unquote(target)).resolve()
            if not resolved.is_relative_to(ROOT):
                problems.append(f"{file.name}: relative link outside repo: {target}")
            elif not resolved.is_file():
                problems.append(f"{file.name}: broken relative link: {target}")
    ledger_bytes = (HERE / "source-ledger-2026-11-03-original.md").read_bytes()
    observed = git_blob_sha(ledger_bytes)
    if observed != EXPECTED_ORIGINAL_GIT_BLOB:
        problems.append("user-supplied original ledger has changed (Git blob mismatch)")
    return problems, {
        "sources": len(rows),
        "claims": len(ids),
        "acquisitions": len(items),
        "markdownFiles": len(list(HERE.glob("*.md"))),
        "bsbIIIFDerivatives": len(scans),
    }


if __name__ == "__main__":
    errors, stats = validate()
    print(json.dumps({"ok": not errors, "stats": stats, "errors": errors},
                     ensure_ascii=False, indent=2))
    sys.exit(1 if errors else 0)
