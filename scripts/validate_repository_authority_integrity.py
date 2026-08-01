#!/usr/bin/env python3
"""Repository-wide fail-closed authority and validator integrity checks.

This checker intentionally validates control-plane relationships that individual
corpus validators cannot see: evidence-policy consistency, transitive workflow
triggers, byte-pin enforcement, read-only audit behavior, and cross-repository
snapshot verification contracts.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKOUT_SHA = "3d3c42e5aac5ba805825da76410c181273ba90b1"
errors: list[str] = []


def require(condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


def read(rel: str) -> str:
    path = ROOT / rel
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        errors.append(f"cannot read {rel}: {exc}")
        return ""


def load(rel: str) -> dict:
    text = read(rel)
    try:
        value = json.loads(text)
    except json.JSONDecodeError as exc:
        errors.append(f"invalid JSON {rel}: {exc}")
        return {}
    if not isinstance(value, dict):
        errors.append(f"{rel} must contain an object")
        return {}
    return value


policy = load("data/repository-evidence-policy-v2.json")
require(policy.get("schemaVersion") == 2, "evidence policy schemaVersion must be 2")
require(
    set(policy.get("sourceClasses", {})) == {"A1", "A2", "A3", "B1", "C", "D"},
    "canonical source classes must be exactly A1/A2/A3/B1/C/D",
)
require(
    set(policy.get("holds", []))
    == {"EVIDENCE_HOLD", "LOCATOR_HOLD", "ARCHIVE_HOLD", "RIGHTS_HOLD", "PUBLICATION_HOLD"},
    "canonical HOLD set drift",
)

agent_rules = read("AGENT_RULES.md")
require("repository-evidence-policy-v2.json" in agent_rules, "AGENT_RULES must link canonical policy")
for legacy in ("**Level A**", "**Level B**", "**Level C**"):
    require(legacy not in agent_rules, f"legacy taxonomy remains in AGENT_RULES: {legacy}")
for cls in ("`A1`", "`A2`", "`A3`", "`B1`", "`C`", "`D`"):
    require(cls in agent_rules, f"AGENT_RULES missing source class {cls}")

critical_workflows = [
    ".github/workflows/repository-authority-integrity.yml",
    ".github/workflows/public-projection-queue.yml",
    ".github/workflows/osk-wave7-product-article-audit.yml",
    ".github/workflows/osk-wave9-modern-diotrophes.yml",
    ".github/workflows/osk-wave10-faithful-witness.yml",
    ".github/workflows/bratsky-listok-authority-manifest.yml",
    ".github/workflows/gill-pr2-lossless-reconciliation.yml",
    ".github/workflows/genesis6-authority-manifest.yml",
    ".github/workflows/heart-source-closure.yml",
    ".github/workflows/total-cross-repo-source-audit.yml",
]
for rel in critical_workflows:
    text = read(rel)
    require(f"actions/checkout@{CHECKOUT_SHA}" in text, f"{rel}: checkout action is not SHA-pinned")
    require("actions/checkout@v4" not in text, f"{rel}: floating checkout tag remains")

# Total audit must execute committed code without runtime source mutation.
total_workflow = read(".github/workflows/total-cross-repo-source-audit.yml")
total_script = read("SOURCE_LIBRARY/tools/total_cross_repo_source_audit.py")
require("Harden malformed URL handling" not in total_workflow, "total audit still patches source at runtime")
require("p.write_text(s.replace" not in total_workflow, "runtime source rewrite remains in total audit")
require("git diff --exit-code" in total_workflow, "total audit must prove validators are read-only")
require("except ValueError" in total_script, "committed total audit lacks malformed-URL guard")

# Wave 9 reads Wave 1/2 shards and Wave 7 controls, so those paths must trigger it.
w9 = read(".github/workflows/osk-wave9-modern-diotrophes.yml")
for dependency in (
    "data/osk-source-registry-core-*-2026-08-01.json",
    "data/osk-wave2-source-registry-*-2026-08-01.json",
    "data/osk-wave7-article-audit-source-registry-2026-08-01.json",
):
    require(dependency in w9, f"Wave 9 workflow missing transitive trigger: {dependency}")

# Wave 10 must open and validate the declared parent authority, not only repeat its ID.
w10_workflow = read(".github/workflows/osk-wave10-faithful-witness.yml")
w10_validator = read("scripts/validate_osk_wave10_faithful_witness.py")
for dependency in (
    "data/osk-wave9-modern-diotrophes-source-manifest-2026-08-01.json",
    "data/osk-wave9-modern-diotrophes-outline-2026-08-01.json",
):
    require(dependency in w10_workflow, f"Wave 10 workflow missing parent trigger: {dependency}")
    require(Path(dependency).name in w10_validator, f"Wave 10 validator does not read parent input: {dependency}")
require("inherited source ids absent from Wave 9 parent" in w10_validator, "Wave 10 lacks inherited-ID parent proof")

# Cross-repository Product pins must be verified against a checked-out Product repository.
w7_workflow = read(".github/workflows/osk-wave7-product-article-audit.yml")
w7_validator = read("scripts/validate_osk_wave7_product_article_audit.py")
require("repository: FedorMilovanov/gb-is-my-strength" in w7_workflow, "Wave 7 does not checkout Product repository")
require("PRODUCT_REPO" in w7_validator and "git rev-parse" in w7_validator, "Wave 7 does not verify Product commit/blob")

# Historical commit/blob markers must be checked against Git object bytes.
bratsky = read("scripts/validate_bratsky_listok_authority_manifest.py")
require("rev-parse" in bratsky and "commit:path" in bratsky, "Bratsky commit pins are not byte-verified")
gill = read("scripts/gill-pr2-lossless-reconciliation-audit.mjs")
require("git hash-object" in gill, "Gill archive blob marker is not computed from bytes")

genesis = read("scripts/validate_genesis6_authority_manifest.py")
require("contentSha256" in genesis, "Genesis active documents lack content SHA validation")

heart = read("scripts/check_heart_source_closure.py")
require("TRUSTED_SOURCE_CLASSES" in heart, "Heart registry still self-defines trusted classes")
require("trusted_source_classes" not in heart, "Heart validator still trusts registry-provided class list")
require("locator" in heart and "edition_or_version" in heart, "Heart quote-safe contract lacks locator/version checks")

projection_workflow = read(".github/workflows/public-projection-queue.yml")
projection_validator = read("scripts/validate_public_projection_queue.py")
for dependency in (
    "00_RESEARCH_CURRENT_AUTHORITY_2026-08-01.md",
    "PUBLIC_PROJECTION_OSK_WAVE6_OVERLAY_2026-08-01.md",
    "data/public-projection-osk-wave6-overlay-2026-08-01.json",
):
    require(dependency in projection_workflow, f"projection workflow missing authority trigger: {dependency}")
require("apply_osk_overlay" in projection_validator, "projection validator does not compose the OSK overlay")
require("WAVES_1_TO_11" in projection_validator, "projection validator does not enforce current OSK state")

portrait = read("SOURCE_LIBRARY/tools/download_approved_core_poet_portraits.py")
require("core-poet-portraits-allowlist-v2.json" in portrait, "portrait downloader still embeds a second allowlist")
require("SELECTED:" not in portrait, "hard-coded portrait selection remains")
require((ROOT / "data/core-poet-portraits-allowlist-v2.json").is_file(), "canonical portrait allowlist missing")

require((ROOT / "archive-ledgers/README.md").is_file(), "main lacks durable archive-branch index")

if errors:
    print(f"Repository authority integrity: FAIL ({len(errors)})", file=sys.stderr)
    for error in errors:
        print(f"- {error}", file=sys.stderr)
    raise SystemExit(1)

print("Repository authority integrity: PASS")
