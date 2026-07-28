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
EXPECTED_BLOCKING_HOLDS: list[str] = []
EXPECTED_PRESERVED_HOLDS = [
    "1-enoch-10-8-interpretive-scope",
    "1-enoch-15-8-12-version-details-and-demon-identity",
    "1-enoch-70-71-composition-and-figure-identity",
    "astronomical-book-reconstruction-direction-and-joins",
    "parables-date-and-witness-form",
    "animal-apocalypse-decomposition",
    "chapter-108-relation-to-epistle",
    "codex-panopolitanus-editorial-intention",
]
EXPECTED_RESOLVED_EVIDENCE = [
    {
        "id": "1-enoch-10-8-version-control",
        "resolution": "text-established-interpretation-qualified",
        "documentId": "GEN6-ENOCH-10-8-DECISION-LX",
        "evidence": "Greek and Ge'ez full clause; Aramaic 4Q202 locus 10:8-12 partial/reconstructed",
    },
    {
        "id": "1-enoch-15-8-12-demon-origin",
        "resolution": "core-model-established-canonical-status-qualified",
        "documentId": "GEN6-ENOCH-15-8-12-DECISION-LXI",
        "evidence": "Greek Syncellus and Codex Panopolitanus plus full Ge'ez preserve the core model; Aramaic 4Q204 is contextual/partial",
    },
    {
        "id": "1-enoch-70-71-son-of-man",
        "resolution": "direct-address-established-composition-and-identity-qualified",
        "documentId": "GEN6-ENOCH-70-71-DECISION-LXV",
        "evidence": "LXII evidence chain plus modern critical translation support second-person 71:14; Charles third-person is an emendation; composition and total identity remain qualified",
    },
    {
        "id": "astronomical-book-version-plurality",
        "resolution": "textual-plurality-established-evolution-model-qualified",
        "documentId": "GEN6-ENOCH-ASTRONOMICAL-DECISION-LXVI",
        "evidence": "4Q208/4Q209 continuity and scheme-level plurality are established by Ratzon's full reconstruction; direction of adaptation and exact joins remain qualified",
    },
]
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
    "1-enoch-15-8-12-demon-origin",
    "1-enoch-70-71-son-of-man",
    "astronomical-book-version-plurality",
]
EVIDENCE_DOCUMENTS = {
    "GEN6-ENOCH-ASTRONOMICAL-PROTOCOL-LXIII": {
        "path": "ТРУДНЫЕ ТЕКСТЫ/1_ENOCH_LXIII_ASTRONOMICAL_BOOK_VERSION_PLURALITY_BLOCKING_HOLD_PROTOCOL.md",
        "role": "locus-evidence-protocol",
        "requiredFor": ["6A", "6B"],
    },
    "GEN6-ENOCH-ASTRONOMICAL-PUBLIC-GATE-LXIII-A": {
        "path": "ТРУДНЫЕ ТЕКСТЫ/1_ENOCH_LXIII_A_ASTRONOMICAL_PUBLIC_EVIDENCE_AND_FULL_TEXT_ACCESS_GATE.md",
        "role": "public-text-and-access-gate",
        "requiredFor": ["6A", "6B"],
    },
    "GEN6-ENOCH-ASTRONOMICAL-CHARLES-ADDENDUM-LXIII-B": {
        "path": "ТРУДНЫЕ ТЕКСТЫ/1_ENOCH_LXIII_B_ASTRONOMICAL_CHARLES_1906_HISTORICAL_APPARATUS_ADDENDUM.md",
        "role": "historical-multi-ms-apparatus-evidence",
        "requiredFor": ["6A", "6B"],
    },
    "GEN6-ENOCH-70-71-PROTOCOL-LXII": {
        "path": "ТРУДНЫЕ ТЕКСТЫ/1_ENOCH_LXII_70_71_SON_OF_MAN_BLOCKING_HOLD_CLOSURE_PROTOCOL.md",
        "role": "locus-evidence-protocol",
        "requiredFor": ["6B"],
    },
    "GEN6-ENOCH-70-71-PUBLIC-GATE-LXII-A": {
        "path": "ТРУДНЫЕ ТЕКСТЫ/1_ENOCH_LXII_A_70_71_PUBLIC_TEXT_TRANSLATION_AND_ACCESS_GATE.md",
        "role": "public-text-and-access-gate",
        "requiredFor": ["6B"],
    },
    "GEN6-ENOCH-70-71-CHARLES-ADDENDUM-LXII-B": {
        "path": "ТРУДНЫЕ ТЕКСТЫ/1_ENOCH_LXII_B_70_71_CHARLES_1906_DIRECT_APPARATUS_ADDENDUM.md",
        "role": "historical-multi-ms-apparatus-evidence",
        "requiredFor": ["6B"],
    },
}
DECISIONS = {
    "GEN6-ENOCH-10-8-DECISION-LX": {
        "path": "ТРУДНЫЕ ТЕКСТЫ/1_ENOCH_LX_10_8_VERSION_CONTROL_DECISION.md",
        "requiredFor": ["6B"],
        "markers": [
            "1-enoch-10-8-version-control",
            "TEXT-ESTABLISHED / INTERPRETATION-QUALIFIED",
            "Публикационная блокировка серии **не снимается**",
        ],
    },
    "GEN6-ENOCH-15-8-12-DECISION-LXI": {
        "path": "ТРУДНЫЕ ТЕКСТЫ/1_ENOCH_LXI_15_8_12_DEMON_ORIGIN_VERSION_CONTROL_DECISION.md",
        "requiredFor": ["6B"],
        "markers": [
            "1-enoch-15-8-12-demon-origin",
            "CORE-MODEL-ESTABLISHED / CANONICAL-STATUS-QUALIFIED",
            "Публикационная блокировка серии **не снимается**",
        ],
    },
    "GEN6-ENOCH-70-71-DECISION-LXV": {
        "path": "ТРУДНЫЕ ТЕКСТЫ/1_ENOCH_LXV_70_71_SON_OF_MAN_AUTHORITY_DECISION.md",
        "requiredFor": ["6B"],
        "markers": [
            "1-enoch-70-71-son-of-man",
            "DIRECT-ADDRESS-ESTABLISHED / COMPOSITION-AND-IDENTITY-QUALIFIED",
            "astronomical-book-version-plurality",
            "Публикационная блокировка серии **не снимается**",
        ],
    },
    "GEN6-ENOCH-ASTRONOMICAL-DECISION-LXVI": {
        "path": "ТРУДНЫЕ ТЕКСТЫ/1_ENOCH_LXVI_ASTRONOMICAL_BOOK_VERSION_PLURALITY_AUTHORITY_DECISION.md",
        "requiredFor": ["6A", "6B"],
        "markers": [
            "astronomical-book-version-plurality",
            "TEXTUAL-PLURALITY-ESTABLISHED / EVOLUTION-MODEL-QUALIFIED",
            "astronomical-book-reconstruction-direction-and-joins",
            "SAME-COMPOSITION",
            "PEER-REVIEWED-CURRENT-RECONSTRUCTION",
            "Research blockers закрыты; site implementation и publication authorization ещё не закрыты",
        ],
    },
}


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
        if document.get("schemaVersion") != 6:
            fail(f"{name} schemaVersion must be 6")
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
    document_by_id: dict[str, dict] = {}
    for document in documents:
        document_id = document.get("id")
        relative_path = document.get("path")
        if not isinstance(document_id, str) or not document_id:
            fail("document id missing")
        if document_id in document_ids:
            fail(f"duplicate document id {document_id}")
        document_ids.add(document_id)
        document_by_id[document_id] = document
        if not isinstance(relative_path, str) or not (root / relative_path).is_file():
            fail(f"missing authority document for {document_id}: {relative_path}")

    for evidence_id, contract in EVIDENCE_DOCUMENTS.items():
        expected_document = {
            "id": evidence_id,
            "path": contract["path"],
            "role": contract["role"],
            "requiredFor": contract["requiredFor"],
        }
        if document_by_id.get(evidence_id) != expected_document:
            fail(f"{evidence_id} evidence binding drift")

    for decision_id, contract in DECISIONS.items():
        expected_document = {
            "id": decision_id,
            "path": contract["path"],
            "role": "locus-version-control-decision",
            "requiredFor": contract["requiredFor"],
        }
        if document_by_id.get(decision_id) != expected_document:
            fail(f"{decision_id} document binding drift")
        decision_text = (root / contract["path"]).read_text(encoding="utf-8")
        for marker in contract["markers"]:
            if marker not in decision_text:
                fail(f"{decision_id} missing marker: {marker}")

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
    if acceptance.get("closedGates") != EXPECTED_CLOSED_GATES[:5]:
        fail("siteAcceptance closed gates drift")
    if acceptance.get("publicationAuthorized") is not False:
        fail("site acceptance must not authorize publication")

    registry = manifest.get("holdRegistry")
    if not isinstance(registry, dict):
        fail("holdRegistry missing")
    if set(registry) != {"blocking", "preservedUncertainty", "resolvedByEvidence", "resolvedByPolicy"}:
        fail("holdRegistry keys drift")
    if registry.get("blocking") != EXPECTED_BLOCKING_HOLDS:
        fail("blocking HOLD registry must be empty")
    if registry.get("preservedUncertainty") != EXPECTED_PRESERVED_HOLDS:
        fail("preserved uncertainty registry drift")
    if registry.get("resolvedByEvidence") != EXPECTED_RESOLVED_EVIDENCE:
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

    decision_ids = list(DECISIONS)
    astronomical_ids = [
        "GEN6-ENOCH-ASTRONOMICAL-PROTOCOL-LXIII",
        "GEN6-ENOCH-ASTRONOMICAL-PUBLIC-GATE-LXIII-A",
        "GEN6-ENOCH-ASTRONOMICAL-CHARLES-ADDENDUM-LXIII-B",
        "GEN6-ENOCH-ASTRONOMICAL-DECISION-LXVI",
    ]
    enoch_70_ids = [
        "GEN6-ENOCH-70-71-PROTOCOL-LXII",
        "GEN6-ENOCH-70-71-PUBLIC-GATE-LXII-A",
        "GEN6-ENOCH-70-71-CHARLES-ADDENDUM-LXII-B",
        "GEN6-ENOCH-70-71-DECISION-LXV",
    ]

    for key in EXPECTED_KEYS:
        article = by_key[key]
        bundle = ledger_by_key[key]
        if article.get("slug") != EXPECTED_SLUGS[key]:
            fail(f"{key} slug drift")
        if article.get("publicationStatus") != "research-ready-site-implementation-hold":
            fail(f"{key} publicationStatus must be research-ready-site-implementation-hold")
        if article.get("requiredSiteState") != {"draft": True, "noindex": True}:
            fail(f"{key} requiredSiteState must remain draft/noindex")
        if article.get("rightsMode") != "no-manuscript-image-reproduction":
            fail(f"{key} rightsMode drift")
        ordered_ids = article.get("orderedDocumentIds")
        if not isinstance(ordered_ids, list) or not ordered_ids:
            fail(f"{key} orderedDocumentIds missing")
        missing_ids = [document_id for document_id in ordered_ids if document_id not in document_ids]
        if missing_ids:
            fail(f"{key} references unknown documents: {missing_ids}")
        missing_astronomical = [document_id for document_id in astronomical_ids if document_id not in ordered_ids]
        if missing_astronomical:
            fail(f"{key} bundle missing Astronomical evidence/decision: {missing_astronomical}")
        if key == "6B":
            missing_decisions = [decision_id for decision_id in decision_ids if decision_id not in ordered_ids]
            missing_70 = [document_id for document_id in enoch_70_ids if document_id not in ordered_ids]
            if missing_decisions:
                fail(f"6B bundle missing decisions: {missing_decisions}")
            if missing_70:
                fail(f"6B bundle missing 70-71 evidence/decision: {missing_70}")
        if key == "6A":
            forbidden = [
                document_id
                for document_id in decision_ids + enoch_70_ids
                if document_id != "GEN6-ENOCH-ASTRONOMICAL-DECISION-LXVI"
                and document_id in ordered_ids
            ]
            if forbidden:
                fail(f"6A bundle must not claim 6B-only evidence/decisions: {forbidden}")
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
    if release.get("researchBlockersClosed") is not True:
        fail("researchBlockersClosed must be true")
    if release.get("siteImplementationRequired") is not True:
        fail("siteImplementationRequired must be true")
    if release.get("explicitPublicationPassRequired") is not True:
        fail("explicitPublicationPassRequired must be true")
    if release.get("closedGates") != EXPECTED_CLOSED_GATES:
        fail("ledger closed gates drift")
    if release.get("blockingHolds") != EXPECTED_BLOCKING_HOLDS:
        fail("ledger blockingHolds must be empty")
    if release.get("preservedUncertainty") != EXPECTED_PRESERVED_HOLDS:
        fail("ledger preserved uncertainty drift")
    if release.get("resolvedByEvidence") != EXPECTED_RESOLVED_EVIDENCE:
        fail("ledger evidence resolution drift")
    if release.get("resolvedByPolicy") != [EXPECTED_RESOLVED_POLICY]:
        fail("ledger policy resolution drift")

    print(
        "Genesis 6 Enoch extension authority: PASS "
        f"({len(documents)} documents, {len(manifest_articles)} research-ready draft articles, "
        "0 Research blocking HOLDs, site implementation still required, "
        f"manifest {sha256(manifest_path)})"
    )


if __name__ == "__main__":
    main()
