#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

CLASSES = {"base", "overlay", "manifest", "closeout", "historical"}
STATUSES = {"active", "superseded", "historical"}
HEX40 = re.compile(r"^[0-9a-f]{40}$")


def git(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", "-C", str(root), *args], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)


def load(path: Path, errors: list[str]) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"cannot read {path}: {exc}")
        return {}


def validate(root: Path, manifest_path: Path, ledger_path: Path) -> list[str]:
    errors: list[str] = []
    manifest = load(manifest_path, errors)
    ledger = load(ledger_path, errors)
    if errors:
        return errors
    if manifest.get("schemaVersion") != 1:
        errors.append("manifest.schemaVersion must be 1")
    if manifest.get("seriesId") != "genesis-6":
        errors.append("manifest.seriesId must be genesis-6")
    base = manifest.get("authorityBaseCommit", "")
    if not isinstance(base, str) or not HEX40.fullmatch(base):
        errors.append("authorityBaseCommit must be a lowercase 40-char SHA")

    docs = manifest.get("documents", [])
    if not isinstance(docs, list) or not docs:
        errors.append("documents must be a non-empty array")
        docs = []
    by_id: dict[str, dict] = {}
    exclusive: dict[str, str] = {}
    for index, document in enumerate(docs):
        if not isinstance(document, dict):
            errors.append(f"documents[{index}] must be an object")
            continue
        did = document.get("id")
        if not isinstance(did, str) or not re.fullmatch(r"[A-Z0-9-]+", did):
            errors.append(f"documents[{index}].id is invalid")
            continue
        if did in by_id:
            errors.append(f"duplicate document id {did}")
        by_id[did] = document
        path = document.get("path")
        if not isinstance(path, str) or not path:
            errors.append(f"{did}: path is missing")
        elif not (root / path).is_file():
            errors.append(f"{did}: registered path is missing: {path}")
        if document.get("authorityClass") not in CLASSES:
            errors.append(f"{did}: invalid authorityClass")
        if document.get("status") not in STATUSES:
            errors.append(f"{did}: invalid status")
        articles = document.get("scope", {}).get("articles", []) if isinstance(document.get("scope"), dict) else []
        if not isinstance(articles, list) or any(article not in (6, 7, 8, 9) for article in articles):
            errors.append(f"{did}: scope.articles must use 6-9")
        scopes = document.get("canonicalScopes", [])
        if not isinstance(scopes, list) or any(not isinstance(scope, str) or not scope for scope in scopes):
            errors.append(f"{did}: canonicalScopes must be strings")
            scopes = []
        if document.get("status") == "active" and document.get("exclusive"):
            for scope in scopes:
                if scope in exclusive:
                    errors.append(f"exclusive authority collision for {scope}: {exclusive[scope]} and {did}")
                exclusive[scope] = did
        if document.get("authorityClass") == "closeout" and (
            document.get("contentAuthority") or document.get("mandatoryForSite") or document.get("sitePublicationEligible")
        ):
            errors.append(f"{did}: closeout cannot be content authority or publication input")

    for did, document in by_id.items():
        for field in ("supersedes", "appliesTo"):
            values = document.get(field, [])
            if not isinstance(values, list):
                errors.append(f"{did}: {field} must be an array")
                continue
            for target in values:
                if target not in by_id:
                    errors.append(f"{did}: {field} references missing id {target}")
                if target == did:
                    errors.append(f"{did}: self-reference in {field}")
        if document.get("authorityClass") == "overlay" and document.get("status") == "active":
            targets = document.get("appliesTo", [])
            if not targets:
                errors.append(f"{did}: active overlay requires appliesTo")
            elif not any(by_id.get(target, {}).get("status") == "active" and by_id.get(target, {}).get("authorityClass") == "base" for target in targets):
                errors.append(f"{did}: active overlay must apply to an active base")

    graph = {did: list(document.get("supersedes", [])) for did, document in by_id.items()}
    state: dict[str, int] = {}
    stack: list[str] = []

    def visit(node: str) -> None:
        if state.get(node) == 1:
            cycle = stack[stack.index(node):] + [node] if node in stack else [node]
            errors.append("supersession cycle: " + " -> ".join(cycle))
            return
        if state.get(node) == 2:
            return
        state[node] = 1
        stack.append(node)
        for child in graph.get(node, []):
            if child in graph:
                visit(child)
        stack.pop()
        state[node] = 2

    for node in graph:
        visit(node)

    rights = manifest.get("rightsDecisions", [])
    rights_by_id: dict[str, dict] = {}
    if not isinstance(rights, list):
        errors.append("rightsDecisions must be an array")
        rights = []
    for decision in rights:
        rid = decision.get("id") if isinstance(decision, dict) else None
        if not isinstance(rid, str) or not rid:
            errors.append("rights decision requires id")
            continue
        if rid in rights_by_id:
            errors.append(f"duplicate rights decision {rid}")
        rights_by_id[rid] = decision
        authority = decision.get("authorityDocumentId")
        if authority not in by_id or by_id[authority].get("status") != "active":
            errors.append(f"{rid}: authorityDocumentId must be active")
        if decision.get("originalAssetState") in {"permission-pending", "hold", "permission-required"}:
            alternative = decision.get("approvedAlternative")
            if not isinstance(alternative, dict) or not alternative.get("type"):
                errors.append(f"{rid}: unresolved rights require approvedAlternative")
            elif alternative.get("documentId") not in by_id:
                errors.append(f"{rid}: alternative document is missing")
        if not decision.get("siteEligible"):
            errors.append(f"{rid}: decision must be siteEligible")

    bundles = manifest.get("publicationBundles", [])
    articles: set[int] = set()
    bundle_ids: set[str] = set()
    if not isinstance(bundles, list):
        errors.append("publicationBundles must be an array")
        bundles = []
    for bundle in bundles:
        if not isinstance(bundle, dict):
            errors.append("publication bundle must be an object")
            continue
        bid = bundle.get("bundleId")
        article = bundle.get("article")
        if not isinstance(bid, str) or not bid or bid in bundle_ids:
            errors.append(f"invalid or duplicate bundleId {bid}")
        bundle_ids.add(bid)
        if article not in (6, 7, 8, 9):
            errors.append(f"{bid}: article must be 6-9")
            continue
        if article in articles:
            errors.append(f"duplicate bundle for article {article}")
        articles.add(article)
        base_id = bundle.get("readerBaseId")
        base_doc = by_id.get(base_id)
        if not base_doc or base_doc.get("authorityClass") != "base" or base_doc.get("status") != "active" or not base_doc.get("sitePublicationEligible"):
            errors.append(f"{bid}: readerBaseId must be an active site-eligible base")
        ordered = bundle.get("orderedDocumentIds", [])
        if not isinstance(ordered, list) or not ordered:
            errors.append(f"{bid}: orderedDocumentIds must be non-empty")
            ordered = []
        if len(ordered) != len(set(ordered)):
            errors.append(f"{bid}: duplicate orderedDocumentIds")
        if base_id not in ordered:
            errors.append(f"{bid}: reader base is absent")
        for did in ordered:
            document = by_id.get(did)
            if not document:
                errors.append(f"{bid}: unknown document {did}")
            elif document.get("status") != "active" or document.get("authorityClass") in {"historical", "closeout"}:
                errors.append(f"{bid}: invalid publication input {did}")
        mandatory = {
            did for did, document in by_id.items()
            if document.get("status") == "active" and document.get("mandatoryForSite") and article in document.get("scope", {}).get("articles", [])
        }
        missing = sorted(mandatory - set(ordered))
        if missing:
            errors.append(f"{bid}: omits mandatory inputs: {', '.join(missing)}")
        decisions = bundle.get("rightsDecisionIds", [])
        if not isinstance(decisions, list) or not decisions:
            errors.append(f"{bid}: rightsDecisionIds must be non-empty")
        for rid in decisions:
            if rid not in rights_by_id:
                errors.append(f"{bid}: unknown rights decision {rid}")
    if articles != {6, 7, 8, 9}:
        errors.append(f"publication bundles must cover exactly 6-9, got {sorted(articles)}")

    readme = (root / "README.md").read_text(encoding="utf-8")
    for required in manifest.get("readmeRequiredPaths", []):
        if Path(required).name not in readme:
            errors.append(f"README authority link drift: {Path(required).name}")

    digest = hashlib.sha256(manifest_path.read_bytes()).hexdigest()
    if ledger.get("schemaVersion") != 1 or ledger.get("seriesId") != "genesis-6":
        errors.append("ledger schema/series mismatch")
    if ledger.get("authorityBaseCommit") != base:
        errors.append("ledger authorityBaseCommit mismatch")
    if ledger.get("manifestPath") != manifest_path.relative_to(root).as_posix():
        errors.append("ledger manifestPath mismatch")
    if ledger.get("manifestSha256") != digest:
        errors.append("ledger manifestSha256 mismatch")
    expected = [
        {key: bundle[key] for key in ("bundleId", "article", "readerBaseId", "orderedDocumentIds", "rightsDecisionIds", "publicationStatus")}
        for bundle in bundles
    ]
    if ledger.get("bundles") != expected:
        errors.append("ledger bundles drift from manifest")

    # Active authority bytes are locked to authorityBaseCommit. Git blob identity is
    # the durable content hash; contentSha256 is computed as an additional witness.
    if HEX40.fullmatch(base):
        if git(root, "cat-file", "-e", f"{base}^{{commit}}").returncode:
            errors.append(f"authorityBaseCommit unavailable: {base}")
        elif git(root, "merge-base", "--is-ancestor", base, "HEAD").returncode:
            errors.append(f"authorityBaseCommit is not an ancestor of HEAD: {base}")
        else:
            for did, document in by_id.items():
                path = document.get("path")
                if not isinstance(path, str) or not path:
                    continue
                if git(root, "cat-file", "-e", f"{base}:{path}").returncode:
                    errors.append(f"{did}: path absent at authorityBaseCommit: {path}")
                    continue
                if document.get("status") != "active":
                    continue
                base_blob = git(root, "rev-parse", f"{base}:{path}").stdout.strip()
                head_blob = git(root, "rev-parse", f"HEAD:{path}").stdout.strip()
                working_blob = git(root, "hash-object", path).stdout.strip()
                contentSha256 = hashlib.sha256((root / path).read_bytes()).hexdigest()
                if not re.fullmatch(r"[0-9a-f]{64}", contentSha256):
                    errors.append(f"{did}: invalid contentSha256 computation")
                if head_blob != working_blob:
                    errors.append(f"{did}: working bytes differ from HEAD blob")
                if base_blob != head_blob:
                    errors.append(f"{did}: active authority bytes drifted from authorityBaseCommit ({base_blob} != {head_blob})")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--manifest", default="data/genesis6-authority-manifest.json")
    parser.add_argument("--ledger", default="data/genesis6-publication-ledger.json")
    args = parser.parse_args()
    root = args.root.resolve()
    errors = validate(root, root / args.manifest, root / args.ledger)
    if errors:
        print("Genesis 6 authority manifest: FAIL", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    manifest = json.loads((root / args.manifest).read_text(encoding="utf-8"))
    digest = hashlib.sha256((root / args.manifest).read_bytes()).hexdigest()
    print(
        f"Genesis 6 authority manifest: PASS ({len(manifest['documents'])} documents, "
        f"{len(manifest['publicationBundles'])} bundles, {len(manifest['rightsDecisions'])} rights decisions, "
        f"active bytes locked to authorityBaseCommit, sha256={digest})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
