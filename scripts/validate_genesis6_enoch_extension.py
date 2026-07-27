#!/usr/bin/env python3
"""Fail-closed validator for the Genesis 6 Enoch extension articles 6A–6B."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys


EXPECTED_KEYS = ("6A", "6B")
EXPECTED_SLUGS = {
    "6A": "kniga-enoha-kotoroy-ne-bylo-kak-raznye-proizvedeniya-stali-korpusom",
    "6B": "mozhno-li-doveryat-1-enohu-kanonicheskiy-audit",
}
EXPECTED_GROUPS = {"6A": 27, "6B": 26}
EXPECTED_BLOCKING_HOLDS = [
    "1-enoch-15-8-12-demon-origin",
    "1-enoch-70-71-son-of-man",
    "astronomical-book-version-plurality",
]
EXPECTED_PRESERVED_HOLDS = [
    "1-enoch-10-8-interpretive-scope",
    "parables-date-and-witness-form",
    "animal-apocalypse-decomposition",
    "chapter-108-relation-to-epistle",
    "codex-panopolitanus-editorial-intention",
]
EXPECTED_RESOLVED_EVIDENCE = {
    "id": "1-enoch-10-8-version-control",
    "resolution": "text-established-interpretation-qualified",
    "documentId": "GEN6-ENOCH-10-8-DECISION-LX",
    "evidence": "Greek and Ge'ez full clause; Aramaic 4Q202 locus 10:8-12 partial/reconstructed",
}
EXPECTED_RESOLVED_POLICY = {
    "id": "manuscript-image-rights",
    "resolution": "no-manuscript-image-reproduction",
    "evidence": "site main 522f0e1cae4fb9ce5a4631cfe856421f1952f4bc",
}
EXPECTED_CLOSED_GATES = [
    "claim-level-source-apparatus",
    "reader-bibliography-microaudit",
    "site-provenance",
    "exact-head-technical-ci",
    "manuscript-image-rights-by-no-reproduction",
    "1-enoch-10-8-version-control",
]
DECISION_ID = "GEN6-ENOCH-10-8-DECISION-LX"
DECISION_PATH = "ТРУДНЫЕ ТЕКСТЫ/1_ENOCH_LX_10_8_VERSION_CONTROL_DECISION.md"


def fail(message: str) -> None:
    print(f"ERROR genesis6 enoch extension: {message}", file=sys.stderr)
    raise SystemExit(1)


def read_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        fail(f"cannot read {path}: {error}")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".", help="Research repository root")
    args = parser.parse_args()
    root = Path(args.root).resolve()

    manifest_path = root / "data/genesis6-enoch-extension-authority-manifest.json"
    ledger_path = root / "data/genesis6-enoch-extension-publication-ledger.json"

    if not manifest_path.is_file():
        fail("missing extension authority manifest")
    if not ledger_path.is_file():
        fail("missing extension publication ledger")

    manifest = read_json(manifest_path)
    ledger = read_json(ledger_path)

    for name, document in (("manifest", manifest), ("ledger", ledger)):
        if document.get("schemaVersion") != 3:
            fail(f"{name} schemaVersion must be 3")
        if document.get("seriesId") != "genesis-6":
            fail(f"{name} seriesId must be genesis-6")
        if document.get("extensionId") != "genesis6-enoch-articles-6a-6b":
            fail(f"{name} extensionId drift")

    if ledger.get("manifestPath") != "data/genesis6-enoch-extension-authority-manifest.json":
        fail("ledger manifestPath drift")
    if ledger.get("manifestSha256") != sha256(manifest_path):
        fail("ledger manifest digest drift")

    expected_policy = {
        "canonicalScriptureGoverns": True,
        "academicFindingsRequireLayerSeparation": True,
        "siteStateMustRemainDraftNoindex": True,
        "furtherResearchMustCloseBlockingHolds": True,
        "preservedUncertaintyMustRemainExplicit": True,
        "manuscriptImagesRequireExplicitRightsDecision": True,
        "noManuscriptImageReproductionResolvesRightsGate": True,
    }
    if manifest.get("policy") != expected_policy:
        fail("manifest policy drift")

    documents = manifest.get("documents")
    if not isinstance(documents, list) or not documents:
        fail("manifest documents must be a non-empty list")

    document_ids: set[str] = set()
    decision_document = None
    for document in documents:
        document_id = document.get("id")
        relative_path = document.get("path")
        if not isinstance(document_id, str) or not document_id:
            fail("document id missing")
        if document_id in document_ids:
            fail(f"duplicate document id {document_id}")
        document_ids.add(document_id)
        if not isinstance(relative_path, str) or not (root / relative_path).is_file():
            fail(f"missing authority document for {document_id}: {relative_path}")
        if document_id == DECISION_ID:
            decision_document = document

    expected_decision_document = {
        "id": DECISION_ID,
        "path": DECISION_PATH,
        "role": "locus-version-control-decision",
        "requiredFor": ["6B"],
    }
    if decision_document != expected_decision_document:
        fail("10:8 decision document binding drift")

    decision_text = (root / DECISION_PATH).read_text(encoding="utf-8")
    for marker in [
        "1-enoch-10-8-version-control",
        "1-enoch-10-8-interpretive-scope",
        "TEXT-ESTABLISHED / INTERPRETATION-QUALIFIED",
        "4Q202 / 4QEnᵇ",
        "Codex Panopolitanus",
        "ወላዕሌሁ ጸሐፍ ኵሎ ኀጢአተ",
        "Публикационная блокировка серии **не снимается**",
    ]:
        if marker not in decision_text:
            fail(f"10:8 decision missing marker: {marker}")

    acceptance = manifest.get("siteAcceptance")
    if not isinstance(acceptance, dict):
        fail("siteAcceptance missing")
    if acceptance.get("repository") != "FedorMilovanov/gb-is-my-strength":
        fail("siteAcceptance repository drift")
    if acceptance.get("acceptedHead") != "b315998937e4fdd68e204d01660adb65707cd0e6":
        fail("siteAcceptance acceptedHead drift")
    if acceptance.get("mergeCommit") != "522f0e1cae4fb9ce5a4631cfe856421f1952f4bc":
        fail("siteAcceptance mergeCommit drift")
    if acceptance.get("claimLevelGroups") != EXPECTED_GROUPS:
        fail("siteAcceptance claim-level group counts drift")
    if acceptance.get("closedGates") != EXPECTED_CLOSED_GATES[:-1]:
        fail("siteAcceptance closed gates drift")
    if acceptance.get("publicationAuthorized") is not False:
        fail("site acceptance must not authorize publication")

    registry = manifest.get("holdRegistry")
    if not isinstance(registry, dict):
        fail("holdRegistry missing")
    if set(registry) != {"blocking", "preservedUncertainty", "resolvedByEvidence", "resolvedByPolicy"}:
        fail("holdRegistry keys drift")
    if registry.get("blocking") != EXPECTED_BLOCKING_HOLDS:
        fail("blocking HOLD registry drift")
    if registry.get("preservedUncertainty") != EXPECTED_PRESERVED_HOLDS:
        fail("preserved uncertainty registry drift")
    if registry.get("resolvedByEvidence") != [EXPECTED_RESOLVED_EVIDENCE]:
        fail("evidence resolution registry drift")
    if registry.get("resolvedByPolicy") != [EXPECTED_RESOLVED_POLICY]:
        fail("policy resolution registry drift")

    categories = (
        registry["blocking"]
        + registry["preservedUncertainty"]
        + [item["id"] for item in registry["resolvedByEvidence"]]
        + [item["id"] for item in registry["resolvedByPolicy"]]
    )
    if len(categories) != len(set(categories)):
        fail("HOLD categories must be disjoint")
    if manifest.get("namedHolds") != categories:
        fail("namedHolds must equal the ordered union of HOLD categories")

    manifest_articles = manifest.get("draftArticles")
    ledger_bundles = ledger.get("bundles")
    if not isinstance(manifest_articles, list) or len(manifest_articles) != 2:
        fail("manifest must contain exactly two draftArticles")
    if not isinstance(ledger_bundles, list) or len(ledger_bundles) != 2:
        fail("ledger must contain exactly two bundles")

    by_key = {item.get("articleKey"): item for item in manifest_articles}
    ledger_by_key = {item.get("articleKey"): item for item in ledger_bundles}
    if tuple(sorted(by_key)) != EXPECTED_KEYS:
        fail("manifest article keys must be exactly 6A and 6B")
    if tuple(sorted(ledger_by_key)) != EXPECTED_KEYS:
        fail("ledger article keys must be exactly 6A and 6B")

    for key in EXPECTED_KEYS:
        article = by_key[key]
        bundle = ledger_by_key[key]
        if article.get("slug") != EXPECTED_SLUGS[key]:
            fail(f"{key} slug drift")
        if article.get("publicationStatus") != "source-audited-version-hold":
            fail(f"{key} publicationStatus must remain source-audited-version-hold")
        if article.get("requiredSiteState") != {"draft": True, "noindex": True}:
            fail(f"{key} requiredSiteState must be draft/noindex")
        if article.get("rightsMode") != "no-manuscript-image-reproduction":
            fail(f"{key} rightsMode drift")
        ordered_ids = article.get("orderedDocumentIds")
        if not isinstance(ordered_ids, list) or not ordered_ids:
            fail(f"{key} orderedDocumentIds missing")
        missing_ids = [document_id for document_id in ordered_ids if document_id not in document_ids]
        if missing_ids:
            fail(f"{key} references unknown documents: {missing_ids}")
        if key == "6B" and DECISION_ID not in ordered_ids:
            fail("6B bundle must include the 10:8 decision")
        if key == "6A" and DECISION_ID in ordered_ids:
            fail("6A bundle must not claim the 10:8 decision")
        if bundle != article:
            fail(f"{key} ledger bundle drift")

    release = ledger.get("releaseDecision")
    if not isinstance(release, dict):
        fail("releaseDecision missing")
    if release.get("state") != "blocked":
        fail("extension release must remain blocked")
    if release.get("mayPublish") is not False or release.get("mayRemoveNoindex") is not False:
        fail("publication and noindex removal must remain forbidden")
    if release.get("mayMergeAsDraftContent") is not True:
        fail("draft content merge policy drift")
    if release.get("closedGates") != EXPECTED_CLOSED_GATES:
        fail("ledger closed gates drift")
    if release.get("blockingHolds") != EXPECTED_BLOCKING_HOLDS:
        fail("ledger blocking holds drift")
    if release.get("preservedUncertainty") != EXPECTED_PRESERVED_HOLDS:
        fail("ledger preserved uncertainty drift")
    if release.get("resolvedByEvidence") != [EXPECTED_RESOLVED_EVIDENCE]:
        fail("ledger evidence resolution drift")
    if release.get("resolvedByPolicy") != [EXPECTED_RESOLVED_POLICY]:
        fail("ledger policy resolution drift")

    print(
        "Genesis 6 Enoch extension authority: PASS "
        f"({len(documents)} documents, {len(manifest_articles)} source-audited draft articles, "
        f"{len(EXPECTED_BLOCKING_HOLDS)} blocking HOLDs, 10:8 text established, "
        f"manifest {sha256(manifest_path)})"
    )


if __name__ == "__main__":
    main()
