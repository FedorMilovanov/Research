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
        "REF-P46": ("CATALOG_ONLY", "RIGHTS_UNKNOWN"),
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
        "C85": ("REF-P44", "1521", "Blatt 5v"),
        "C86": ("REF-P44", "REF-P39", "REF-P45"),
        "C87": ("REF-P39", "REF-P44", "REF-S15"),
        "C88": ("REF-S15", "F add", "S.581"),
        "C89": ("REF-P45", "Neyn"),
        "C90": ("REF-S15", "S.583"),
        "C91": ("REF-S16", "REF-S14", "— нет"),
    }.items():
        row = claim_rows.get(id_, "")
        if any(term not in row for term in substrings):
            problems.append(f"{id_}: incomplete Worms first-print legal chronology or citation")
    # Seven 1800px JPEG derivatives were viewed and discarded; this offline
    # check covers receipt integrity only, NOT re-verification of remote bytes.
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
    if [(p, scan) for p, scan, _, _ in receipts] != [
            (str(p), str(p+16)) for p in range(578, 585)]:
        problems.append("Wrede 1896 page/IIIF receipt sequence 578-584/594-600 incomplete")
    if len({sha for _, _, _, sha in receipts}) != 7:
        problems.append("Wrede 1896 SHA receipts missing, repeated or malformed")
    lengths = [556830, 561385, 540789, 572148, 600618, 627903, 526127]
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
    ]
    if [sha for _, _, _, sha in receipts] != expected_sha:
        problems.append("Wrede 1896 SHA receipts changed without verified re-acquisition")
    if "F add. Ich kan nicht anders, hie stehe ich" not in wrede_section:
        problems.append("Wrede p582 variant apparatus has been removed")
    if "NoC-NC/1.0" not in wrede_section:
        problems.append("Wrede BSB digital photograph usage restriction removed")
    if "TEMP_CLEANED=True" not in wrede_section:
        problems.append("Wrede temporary photos cleanup not attested")
    if corpus.get("REF-P46", {}).get("locatorState") != "COARSE_LOCATOR_ONLY":
        problems.append("Wittenberg Latin 1521 photograph falsely marked fully checked")
    if "LOCATOR_HOLD" not in corpus.get("REF-P46", {}).get("holds", []):
        problems.append("Wittenberg Latin 1521 locator hold lost")
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
