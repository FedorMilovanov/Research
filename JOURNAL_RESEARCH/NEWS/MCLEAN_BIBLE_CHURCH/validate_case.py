#!/usr/bin/env python3
# coding: utf-8
"""Read-only gate for JOURNAL_RESEARCH/NEWS/MCLEAN_BIBLE_CHURCH.

Run from any directory:
    python JOURNAL_RESEARCH/NEWS/MCLEAN_BIBLE_CHURCH/validate_case.py
"""
from __future__ import annotations
import json
import re
from pathlib import Path

CASE_DIR = Path(__file__).resolve().parent
RESEARCH_ROOT = CASE_DIR.parents[2]
POLICY = json.loads((RESEARCH_ROOT / "data/repository-evidence-policy-v2.json").read_text(encoding="utf-8"))
DATA = json.loads((CASE_DIR / "sources.json").read_text(encoding="utf-8"))
TEXT = (CASE_DIR / "CASE.md").read_text(encoding="utf-8")

def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)

items = DATA["objects"]
require(DATA["publicationDecision"] == "PUBLICATION_HOLD", "Publication gate must stay HOLD")
require(len(items) >= 37, "Expected 37 objects after financial extension")
ids = [o["sourceId"] for o in items]
urls = [o["url"].rstrip("/") for o in items]
require(len(set(ids)) == len(ids), "Repeated sourceId")
require(len(set(urls)) == len(urls), "Duplicated URL in evidence registry")
mapping = {
    "evidenceClass": "sourceClasses",
    "accessState": "accessStates",
    "locatorState": "locatorStates",
    "rightsState": "rightsStates",
    "publicationState": "publicationStates",
}
for x in items:
    sid=x["sourceId"]
    require(re.fullmatch(r"JR-MBC-\d{3}",sid) is not None,sid+" invalid")
    require(x["url"].startswith("https://"),sid+" URL not secure")
    for field,policy_name in mapping.items():
        require(x[field] in POLICY[policy_name],sid+" "+field+" invalid")
    require(x["publicationState"] == "REFERENCE",sid+" publication state unexpectedly advanced")
    for h in x["holds"]:
        require(h in POLICY["holds"],sid+" invalid HOLD "+h)
    require("PUBLICATION_HOLD" in x["holds"],sid+" not guarded")
    if x["accessState"] != "FULL_OBJECT_VERIFIED":
        require("EVIDENCE_HOLD" in x["holds"],sid+" missing EVIDENCE_HOLD")
    if x["locatorState"] != "EXACT_LOCATOR_VERIFIED":
        require("LOCATOR_HOLD" in x["holds"],sid+" missing LOCATOR_HOLD")
    if x["rightsState"] != "PUBLICATION_ELIGIBLE":
        require("RIGHTS_HOLD" in x["holds"],sid+" missing RIGHTS_HOLD")
    require(bool(x["provesOnly"]) and bool(x["locator"]),sid+" lacks proof/locator statement")
# Direct references in the published research narrative must refer to present objects.
for sid in set(re.findall(r"JR-MBC-\d{3}(?!\d)", TEXT)):
    require(sid in ids, "CASE references missing source "+sid)
# Flag any mistaken assertion that 2017 NCN services addendum is 2016 SBC proposal.
require((("Attachment 9" in TEXT or "№9" in TEXT) and ("Attachment 10" in TEXT or "№10" in TEXT)), "Missing distinct 2016 attachment caveats")
require("два разных судебных дела" in TEXT.lower(), "Missing lawsuit distinction")
# Arithmetic controls of the two source-published one-page accounting schedules.
ncn_total = sum([1193797, 1213620, 1343052, 993052, 533186])
related_total = sum([272168, 439852, 713807, 537725])
require(ncn_total == 5276707 and 5276708-ncn_total == 1, "NCN arithmetic gate changed")
require(related_total == 1963552, "SBC-flow arithmetic gate changed")
require("$5,276,707" in TEXT and "$5,276,708" in TEXT,"Published $1 discrepancy not visible")
require("не" in TEXT and "финансов" in TEXT, "Narrative control absent")
for sid in ("JR-MBC-034", "JR-MBC-035", "JR-MBC-036", "JR-MBC-037", "JR-MBC-038"):
    require(sid in ids and sid in TEXT, sid + " source not referenced")
archive = next(o for o in items if o["sourceId"] == "JR-MBC-037")
require(
    {"INTERNAL_DOCUMENT_DATE_CONFLICT", "CROSS_DOCUMENT_REPORTED_COUNTS_CONFLICT"} <= set(archive.get("integrityFlags", [])),
    "2018 archive integrity caveats missing",
)
require(
    "04/25/2017" in TEXT and "28 декабря 2018" in TEXT,
    "Contradictory 2018 minutes dates omitted",
)
require("устава 2023 года" in TEXT, "Audit policy must identify applicable constitution year")
terms = next(o for o in items if o["sourceId"] == "JR-MBC-038")
require("AI_AUTOMATION_PROHIBITED_BY_SOURCE_TERMS" in terms.get("integrityFlags", []), "ACMS anti-bot restriction missing")
require("не производили автоматизированного поиска внутри ACMS" in TEXT, "Court access restriction not disclosed")
nc = next(o for o in items if o["sourceId"] == "JR-MBC-039")
require(nc["rightsState"] == "PRIVATE_STUDY_ONLY", "Confidential 2017 NCN report must not be publishable")
require("NOT_AN_AUDIT_OPINION" in nc.get("integrityFlags", []), "NCN summary is not an independent audit")
require({"PUBLICATION_HOLD", "RIGHTS_HOLD", "EVIDENCE_HOLD"} <= set(nc["holds"]), "Private NCN source missing HOLD")
require("JR-MBC-039" in TEXT and "58 977" in TEXT and "главным образом" in TEXT, "NCN accounting qualifier omitted")
print("JOURNAL_RESEARCH CASE GATE PASS:", len(items),
      "unique source documents;", len(set(ids)), "IDs; publication HOLD; arithmetic and case distinctions PASS")
