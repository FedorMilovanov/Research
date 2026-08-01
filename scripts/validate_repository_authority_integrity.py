#!/usr/bin/env python3
"""Repository-wide fail-closed authority and validator integrity checks."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKOUT_SHA = "3d3c42e5aac5ba805825da76410c181273ba90b1"
SETUP_PYTHON_SHA = "a26af69be951a213d495a4c3e4e4022e16d87065"
UPLOAD_ARTIFACT_SHA = "65462800fd760344b1a7b4382951275a0abb4808"
errors: list[str] = []


def require(condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


def read(rel: str) -> str:
    try:
        return (ROOT / rel).read_text(encoding="utf-8")
    except OSError as exc:
        errors.append(f"cannot read {rel}: {exc}")
        return ""


def load(rel: str) -> dict:
    try:
        value = json.loads(read(rel))
    except json.JSONDecodeError as exc:
        errors.append(f"invalid JSON {rel}: {exc}")
        return {}
    if not isinstance(value, dict):
        errors.append(f"{rel} must contain an object")
        return {}
    return value


# Global policy and public entry points.
policy = load("data/repository-evidence-policy-v2.json")
require(policy.get("schemaVersion") == 2, "evidence policy schemaVersion must be 2")
require(set(policy.get("sourceClasses", {})) == {"A1", "A2", "A3", "B1", "C", "D"}, "canonical source classes drift")
require(
    set(policy.get("holds", [])) == {"EVIDENCE_HOLD", "LOCATOR_HOLD", "ARCHIVE_HOLD", "RIGHTS_HOLD", "PUBLICATION_HOLD"},
    "canonical HOLD set drift",
)
agent_rules = read("AGENT_RULES.md")
readme = read("README.md")
for text, label in ((agent_rules, "AGENT_RULES"), (readme, "README")):
    require("A, B, C или HOLD" not in text, f"legacy A/B/C/HOLD taxonomy remains in {label}")
    require("Level A, B, C или HOLD" not in text, f"legacy Level taxonomy remains in {label}")
require("repository-evidence-policy-v2.json" in agent_rules, "AGENT_RULES must link canonical policy")
require("repository-evidence-policy-v2.json" in readme, "README must link canonical policy")
for cls in ("`A1`", "`A2`", "`A3`", "`B1`", "`C`", "`D`"):
    require(cls in agent_rules, f"AGENT_RULES missing source class {cls}")

# Critical control-plane workflows must pin checkout and remain read-only.
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
    ".github/workflows/baptist-proof-ledger-v2.yml",
]
for rel in critical_workflows:
    text = read(rel)
    require(f"actions/checkout@{CHECKOUT_SHA}" in text, f"{rel}: checkout action is not SHA-pinned")
    require("actions/checkout@v4" not in text, f"{rel}: floating checkout tag remains")
    require("git diff --exit-code" in text, f"{rel}: missing read-only assertion")

# Source-library acquisition workflows must use pinned toolchains and explicit custody.
source_workflows = [
    ".github/workflows/audit-google-drive-upload-links.yml",
    ".github/workflows/audit-official-digital-collections-links.yml",
    ".github/workflows/build-commons-russian-literature-open-pdf-archive.yml",
    ".github/workflows/build-commons-second-editorial-40-pdf.yml",
    ".github/workflows/build-ephemera-review-candidates.yml",
    ".github/workflows/build-poet-portrait-review-candidates.yml",
    ".github/workflows/download-approved-core-poet-portraits.yml",
    ".github/workflows/download-approved-ephemera-originals.yml",
    ".github/workflows/official-core-acquisition-40plus.yml",
]
for rel in source_workflows:
    text = read(rel)
    require(f"actions/checkout@{CHECKOUT_SHA}" in text, f"{rel}: checkout is not pinned")
    require(f"actions/setup-python@{SETUP_PYTHON_SHA}" in text, f"{rel}: setup-python is not pinned")
    require("requirements/source-audit.txt" in text, f"{rel}: pinned dependency file missing")
    require("git diff --exit-code" in text, f"{rel}: read-only assertion missing")
    if "upload-artifact" in text:
        require(f"actions/upload-artifact@{UPLOAD_ARTIFACT_SHA}" in text, f"{rel}: upload-artifact is not pinned")
for rel in source_workflows[2:]:
    text = read(rel)
    require("EPHEMERAL_ACTION_ARTIFACT" in text, f"{rel}: custody state is not explicit")
    require("publicationEligible" in text, f"{rel}: publication boundary is not explicit")
require(load("data/artifact-custody-policy-v2.json").get("policy", {}).get("actionsArtifactIsNeverDurableByItself") is True, "artifact custody policy drift")

# Total audit must execute committed code without runtime source mutation.
total_workflow = read(".github/workflows/total-cross-repo-source-audit.yml")
total_script = read("SOURCE_LIBRARY/tools/total_cross_repo_source_audit.py")
require("Harden malformed URL handling" not in total_workflow, "total audit still patches source at runtime")
require("p.write_text(s.replace" not in total_workflow, "runtime source rewrite remains in total audit")
require("except ValueError" in total_script, "committed total audit lacks malformed-URL guard")
require("GATE_FAILURE" in total_script, "total audit does not enforce baselines")

# Transitive OSK dependencies.
w9 = read(".github/workflows/osk-wave9-modern-diotrophes.yml")
for dependency in (
    "data/osk-source-registry-core-*-2026-08-01.json",
    "data/osk-wave2-source-registry-*-2026-08-01.json",
    "data/osk-wave7-article-audit-source-registry-2026-08-01.json",
):
    require(dependency in w9, f"Wave 9 workflow missing transitive trigger: {dependency}")
w10_workflow = read(".github/workflows/osk-wave10-faithful-witness.yml")
w10_validator = read("scripts/validate_osk_wave10_faithful_witness.py")
for dependency in (
    "data/osk-wave9-modern-diotrophes-source-manifest-2026-08-01.json",
    "data/osk-wave9-modern-diotrophes-outline-2026-08-01.json",
):
    require(dependency in w10_workflow, f"Wave 10 workflow missing parent trigger: {dependency}")
    require(Path(dependency).name in w10_validator, f"Wave 10 validator does not read parent input: {dependency}")
require("inherited source ids absent from Wave 9 parent" in w10_validator, "Wave 10 lacks inherited-ID parent proof")

# Cross-repository Product pin.
w7_workflow = read(".github/workflows/osk-wave7-product-article-audit.yml")
w7_validator = read("scripts/validate_osk_wave7_product_article_audit.py")
require("repository: FedorMilovanov/gb-is-my-strength" in w7_workflow, "Wave 7 does not checkout Product repository")
require("PRODUCT_REPO" in w7_validator and "rev-parse" in w7_validator and "hash-object" in w7_validator, "Wave 7 does not verify Product commit/blob")

# Historical and active byte pins.
bratsky = read("scripts/validate_bratsky_listok_authority_manifest.py")
require("rev-parse" in bratsky and "commit:path" in bratsky, "Bratsky commit pins are not byte-verified")
gill = read("scripts/gill-pr2-lossless-reconciliation-audit.mjs")
require("git('hash-object'" in gill, "Gill archive blob is not computed from bytes")
genesis = read("scripts/validate_genesis6_authority_manifest.py")
require("contentSha256" in genesis and "base_blob != head_blob" in genesis, "Genesis active bytes are not locked to authorityBaseCommit")

# Heart trust and locator contract.
heart = read("scripts/check_heart_source_closure.py")
require("TRUSTED_SOURCE_CLASSES" in heart, "Heart trust classes are not validator-owned")
require("trusted_source_classes" not in heart, "Heart still trusts registry-provided class list")
require("QUOTE_SAFE_LOCATORS" in heart and "edition_or_version" in heart and "context_verified" in heart, "Heart quote-safe locator contract incomplete")

# Public projection composition.
projection_workflow = read(".github/workflows/public-projection-queue.yml")
projection_validator = read("scripts/validate_public_projection_queue.py")
for dependency in (
    "00_RESEARCH_CURRENT_AUTHORITY_2026-08-01.md",
    "PUBLIC_PROJECTION_OSK_WAVE6_OVERLAY_2026-08-01.md",
    "data/public-projection-current-2026-08-02.json",
    "data/public-projection-osk-wave6-overlay-2026-08-01.json",
):
    require(dependency in projection_workflow, f"projection workflow missing trigger: {dependency}")
require("apply_osk_overlay" in projection_validator, "projection validator does not compose overlay")
require("WAVES_1_TO_11" in projection_validator, "projection validator lacks current OSK state")

# Single media allowlist.
portrait = read("SOURCE_LIBRARY/tools/download_approved_core_poet_portraits.py")
require("core-poet-portraits-allowlist-v2.json" in portrait, "portrait downloader does not read canonical allowlist")
require("SELECTED:" not in portrait, "hard-coded portrait selection remains")
require((ROOT / "data/core-poet-portraits-allowlist-v2.json").is_file(), "canonical portrait allowlist missing")

# Baptist ledger v2 canonicalization.
baptist_schema = load("data/baptist-proof-ledger-schema-v2.json")
baptist_normalizer = read("scripts/normalize_baptist_proof_ledger.py")
require(baptist_schema.get("schemaVersion") == 2, "Baptist proof-ledger schema drift")
require("item_id" in baptist_normalizer and "secondary_id" in baptist_normalizer, "Baptist legacy IDs are not normalized")
require("number.is_integer" in baptist_normalizer, "Baptist float years are not normalized")
require("cmp /tmp/first.csv" in read(".github/workflows/baptist-proof-ledger-v2.yml"), "Baptist canonical output is not determinism-tested")

require((ROOT / "archive-ledgers/README.md").is_file(), "main lacks durable archive-branch index")

if errors:
    print(f"Repository authority integrity: FAIL ({len(errors)})", file=sys.stderr)
    for error in errors:
        print(f"- {error}", file=sys.stderr)
    raise SystemExit(1)
print("Repository authority integrity: PASS")
