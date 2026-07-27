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
        if document.get("schemaVersion") != 1:
            fail(f"{name} schemaVersion must be 1")
        if document.get("seriesId") != "genesis-6":
            fail(f"{name} seriesId must be genesis-6")
        if document.get("extensionId") != "genesis6-enoch-articles-6a-6b":
            fail(f"{name} extensionId drift")

    if ledger.get("manifestPath") != "data/genesis6-enoch-extension-authority-manifest.json":
        fail("ledger manifestPath drift")
    if ledger.get("manifestSha256") != sha256(manifest_path):
        fail("ledger manifest digest drift")

    documents = manifest.get("documents")
    if not isinstance(documents, list) or not documents:
        fail("manifest documents must be a non-empty list")

    document_ids: set[str] = set()
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
        if article.get("publicationStatus") != "draft-noindex-hold":
            fail(f"{key} publicationStatus must remain draft-noindex-hold")
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

        expected_bundle = {
            "articleKey": article["articleKey"],
            "slug": article["slug"],
            "bundleId": article["bundleId"],
            "orderedDocumentIds": article["orderedDocumentIds"],
            "requiredSiteState": article["requiredSiteState"],
            "rightsMode": article["rightsMode"],
            "publicationStatus": article["publicationStatus"],
        }
        if bundle != expected_bundle:
            fail(f"{key} ledger bundle drift")

    release = ledger.get("releaseDecision")
    if not isinstance(release, dict):
        fail("releaseDecision missing")
    if release.get("state") != "blocked":
        fail("extension release must remain blocked")
    if release.get("mayPublish") is not False or release.get("mayRemoveNoindex") is not False:
        fail("publication and noindex removal must remain forbidden")

    holds = manifest.get("namedHolds")
    if not isinstance(holds, list) or len(holds) < 8:
        fail("named HOLD registry is incomplete")

    print(
        "Genesis 6 Enoch extension authority: PASS "
        f"({len(documents)} documents, {len(manifest_articles)} draft articles, "
        f"manifest {sha256(manifest_path)})"
    )


if __name__ == "__main__":
    main()
