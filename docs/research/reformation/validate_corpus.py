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
    }


if __name__ == "__main__":
    errors, stats = validate()
    print(json.dumps({"ok": not errors, "stats": stats, "errors": errors},
                     ensure_ascii=False, indent=2))
    sys.exit(1 if errors else 0)
