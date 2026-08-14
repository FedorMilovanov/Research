#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from collections import Counter
from pathlib import Path

import validate_product_handoff as core

ROOT = Path(__file__).resolve().parents[1]
HANDOFF = ROOT / "product_handoff"
AUTHORITY_SHA = "0142430af8ba80f28e0fd9cde669d32611a1d2af"
EXPECTED_AUTHORITY_DIGEST = "1f444991ecc2f180abdbe0f459148ba8dbf0a5045b1d8888e462683c78366c7d"
SCHEMA_VERSION = 2
RELEASE_FORMAT_VERSION = 1
EXPECTED_COUNTS = {
    "total": 144,
    "chapter4": 72,
    "chapter5": 72,
    "current_holds": 0,
    "competitive_candidates": 0,
    "source_identity_records": 112,
    "claim_source_inspection_edges": 282,
}
EXPECTED_PROTOTYPE_DISPOSITIONS = {
    "SAFE": 26,
    "NEEDS_REWRITE": 19,
    "COURSE_POSITION_ONLY": 2,
    "NONCOMPETITIVE_ONLY": 12,
    "REJECT_AS_PRODUCT_TEMPLATE": 5,
}
REFERENCE_DRIFT_IDS = ["w3mcq_003", "w3mcq_020", "w3mcq_027", "w3mcq_037", "w3mcq_047"]
RAW_FILES = (
    "chapter4-product-handoff.json",
    "chapter5-product-handoff.json",
    "claim-overclaim-blacklist.json",
    "source-identity-package.json",
    "claim-inspection-manifest.json",
    "prototype-audit.json",
    "ranking-audit.json",
    "integrity-summary.json",
)
SAFE_CLASS_MAP = {
    "SAFE_TEMPLATE": "SAFE",
    "NEEDS_REWRITE": "NEEDS_REWRITE",
    "COURSE_POSITION_ONLY": "COURSE_POSITION_ONLY",
    "NONCOMPETITIVE_ONLY": "NONCOMPETITIVE_ONLY",
    "REJECT_AS_PRODUCT_TEMPLATE": "REJECT_AS_PRODUCT_TEMPLATE",
}


class ReleaseError(RuntimeError):
    pass


def canonical_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def numeric_candidate_key(candidate_id: str) -> int:
    return int(str(candidate_id).split("_")[-1])


def assert_expected_authority_digest(value: str) -> None:
    if value != EXPECTED_AUTHORITY_DIGEST:
        raise ReleaseError(
            f"authority digest drift: expected {EXPECTED_AUTHORITY_DIGEST}, got {value}"
        )


def authority_digest_from_effective(effective: dict[str, dict]) -> str:
    ordered = [
        {
            "candidate_id": qid,
            "effective_claim_digest": core.effective_claim_digest(effective[qid]),
        }
        for qid in sorted(effective, key=numeric_candidate_key)
    ]
    return core.stable_hash(ordered)


def edge_digest_payload(edge: dict) -> dict:
    keys = (
        "candidate_id",
        "source_id",
        "evidence_status",
        "access_state",
        "inspection_scope",
        "owning_lane",
        "claim_limit",
        "source_minimum_provenance",
    )
    return {key: edge.get(key) for key in keys}


def compute_edge_id(edge: dict) -> str:
    return "edge_" + core.stable_hash(edge_digest_payload(edge))[:20]


def _positive_claim_text(rec: dict) -> str:
    return "\n".join(
        str(rec.get(key) or "")
        for key in ("stem", "keyed_concept", "tested_distinction")
    )


def load_semantic_policy() -> dict:
    path = HANDOFF / "semantic-boundary-policy.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("schema_version") != SCHEMA_VERSION:
        raise ReleaseError("semantic boundary policy schema drift")
    if data.get("research_authority_sha") != AUTHORITY_SHA:
        raise ReleaseError("semantic boundary policy authority SHA drift")
    return data


def validate_semantic_boundaries(effective: dict[str, dict]) -> None:
    import re

    policy = load_semantic_policy()
    for anchor in policy.get("anchors", []):
        candidate_ids = anchor.get("candidate_ids") or []
        patterns = [re.compile(pattern, re.I) for pattern in anchor.get("forbidden_positive_claim_regex", [])]
        for qid in candidate_ids:
            if qid not in effective:
                raise ReleaseError(f"semantic anchor references missing candidate {qid}")
            text = _positive_claim_text(effective[qid])
            for rx in patterns:
                if rx.search(text):
                    raise ReleaseError(
                        f"semantic boundary {anchor.get('id')} violated by {qid}: {rx.pattern}"
                    )

    project_anchors = policy.get("project_position_anchors") or []
    for anchor in project_anchors:
        qid = anchor["candidate_id"]
        expected = anchor["position"]
        actual = (effective.get(qid) or {}).get("position")
        if actual != expected:
            raise ReleaseError(
                f"project/neutral authority drift for {qid}: expected {expected}, got {actual}"
            )


def run_core(output_dir: Path) -> str:
    cmd = [
        sys.executable,
        str(ROOT / "scripts" / "validate_product_handoff.py"),
        "--emit-dir",
        str(output_dir),
    ]
    result = subprocess.run(cmd, check=False, capture_output=True, text=True)
    if result.returncode != 0:
        raise ReleaseError(
            "canonical validator failed:\n" + (result.stdout or "") + (result.stderr or "")
        )
    return result.stdout.strip()


def load_raw(directory: Path) -> dict[str, object]:
    names = {path.name for path in directory.iterdir() if path.is_file()}
    if names != set(RAW_FILES):
        raise ReleaseError(f"raw artifact set drift: {sorted(names)}")
    return {
        name: json.loads((directory / name).read_text(encoding="utf-8"))
        for name in RAW_FILES
    }


def assert_raw_byte_equivalence(a: Path, b: Path) -> None:
    for name in RAW_FILES:
        left = (a / name).read_bytes()
        right = (b / name).read_bytes()
        if left != right:
            raise ReleaseError(f"non-deterministic canonical generator bytes: {name}")


def validate_raw(raw: dict[str, object]) -> None:
    summary = raw["integrity-summary.json"]
    assert isinstance(summary, dict)
    assert_expected_authority_digest(str(summary.get("authority_digest_sha256")))

    ch4 = raw["chapter4-product-handoff.json"]
    ch5 = raw["chapter5-product-handoff.json"]
    assert isinstance(ch4, dict) and isinstance(ch5, dict)
    claims = list(ch4.get("records") or []) + list(ch5.get("records") or [])
    if len(claims) != EXPECTED_COUNTS["total"]:
        raise ReleaseError(f"effective claim count drift: {len(claims)}")
    if len(ch4.get("records") or []) != EXPECTED_COUNTS["chapter4"]:
        raise ReleaseError("Chapter 4 count drift")
    if len(ch5.get("records") or []) != EXPECTED_COUNTS["chapter5"]:
        raise ReleaseError("Chapter 5 count drift")
    if len({row["candidate_id"] for row in claims}) != EXPECTED_COUNTS["total"]:
        raise ReleaseError("effective candidate ID uniqueness drift")
    if any(len(str(row.get("effective_claim_digest") or "")) != 64 for row in claims):
        raise ReleaseError("effective claim digest missing or malformed")

    for key in ("current_holds", "competitive_candidates", "source_identity_records", "claim_source_inspection_edges"):
        expected = EXPECTED_COUNTS[key]
        actual = summary.get(key)
        if actual != expected:
            raise ReleaseError(f"{key} drift: expected {expected}, got {actual}")

    identities = (raw["source-identity-package.json"] or {}).get("records") or []
    if len(identities) != EXPECTED_COUNTS["source_identity_records"]:
        raise ReleaseError("source identity package count drift")
    forbidden_identity_keys = {
        "claim_id",
        "claim_confidence",
        "claim_position",
        "claim_ready",
        "passage_exegesis_proved",
        "ranking_ready",
        "inspection_depth",
        "strongest_evidence_status",
    }
    for row in identities:
        if forbidden_identity_keys & set(row):
            raise ReleaseError(f"claim-depth laundering into source identity: {row.get('source_id')}")
        if row.get("identity_only") is not True:
            raise ReleaseError(f"source identity is not identity-only: {row.get('source_id')}")

    edges = (raw["claim-inspection-manifest.json"] or {}).get("records") or []
    if len(edges) != EXPECTED_COUNTS["claim_source_inspection_edges"]:
        raise ReleaseError("claim/source edge count drift")
    edge_ids = [row.get("claim_inspection_edge_id") for row in edges]
    if len(set(edge_ids)) != len(edge_ids):
        raise ReleaseError("claim/source edge IDs are not unique")
    for row in edges:
        if compute_edge_id(row) != row.get("claim_inspection_edge_id"):
            raise ReleaseError(f"edge ID formula drift: {row.get('candidate_id')}:{row.get('source_id')}")

    proto_rows = (raw["prototype-audit.json"] or {}).get("records") or []
    if len(proto_rows) != 64:
        raise ReleaseError("prototype count drift")
    disposition_counts = Counter(SAFE_CLASS_MAP.get(row.get("classification"), row.get("classification")) for row in proto_rows)
    if dict(disposition_counts) != EXPECTED_PROTOTYPE_DISPOSITIONS:
        raise ReleaseError(
            f"prototype disposition drift: expected {EXPECTED_PROTOTYPE_DISPOSITIONS}, got {dict(disposition_counts)}"
        )
    rejects = sorted(
        row["prototype_id"]
        for row in proto_rows
        if row.get("classification") == "REJECT_AS_PRODUCT_TEMPLATE"
    )
    if rejects != REFERENCE_DRIFT_IDS:
        raise ReleaseError(f"reject prototype set drift: {rejects}")
    for row in proto_rows:
        if row.get("prototype_id") in REFERENCE_DRIFT_IDS and "REFERENCE_DRIFT" not in (row.get("reasons") or []):
            raise ReleaseError(f"REFERENCE_DRIFT reason disappeared: {row.get('prototype_id')}")

    rank_rows = (raw["ranking-audit.json"] or {}).get("records") or []
    if any(row.get("admitted") for row in rank_rows):
        raise ReleaseError("Research validator attempted ranking admission")
    discrepancies = [row["candidate_id"] for row in rank_rows if row.get("discrepancy_candidate")]
    if discrepancies != ["w3q_123"]:
        raise ReleaseError(f"ranking discrepancy drift: {discrepancies}")


def enrich_release(raw: dict[str, object]) -> dict[str, bytes]:
    release = copy.deepcopy(raw)

    proto = release["prototype-audit.json"]
    for row in proto["records"]:
        row["prototype_disposition"] = SAFE_CLASS_MAP[row["classification"]]

    rank = release["ranking-audit.json"]
    for row in rank["records"]:
        if row["candidate_id"] == "w3q_123":
            row["disposition"] = "NO_PRODUCT_RANKING_ADMISSION"
            row["proposal_allowed_only_via_separate_product_ranking_review"] = True
        else:
            row["disposition"] = "NO_RESEARCH_RANKING_ADMISSION"

    ch4 = release["chapter4-product-handoff.json"]["records"]
    ch5 = release["chapter5-product-handoff.json"]["records"]
    claims = sorted(ch4 + ch5, key=lambda row: numeric_candidate_key(row["candidate_id"]))
    claim_digests = {
        "schema_version": SCHEMA_VERSION,
        "research_authority_sha": AUTHORITY_SHA,
        "whole_authority_sha256": EXPECTED_AUTHORITY_DIGEST,
        "count": len(claims),
        "records": [
            {
                "candidate_id": row["candidate_id"],
                "effective_claim_digest": row["effective_claim_digest"],
            }
            for row in claims
        ],
    }

    edges = release["claim-inspection-manifest.json"]["records"]
    edge_index = {
        "schema_version": SCHEMA_VERSION,
        "research_authority_sha": AUTHORITY_SHA,
        "count": len(edges),
        "records": [
            {
                "candidate_id": row["candidate_id"],
                "source_id": row["source_id"],
                "claim_inspection_edge_id": row["claim_inspection_edge_id"],
                "owning_lane": row["owning_lane"],
                "inspection_depth_class": row["inspection_depth_class"],
            }
            for row in edges
        ],
    }

    semantic_policy = load_semantic_policy()

    summary = release["integrity-summary.json"]
    summary.update(
        {
            "research_authority_sha": AUTHORITY_SHA,
            "handoff_schema_version": SCHEMA_VERSION,
            "release_format_version": RELEASE_FORMAT_VERSION,
            "whole_authority_sha256": EXPECTED_AUTHORITY_DIGEST,
            "effective_claims_total": EXPECTED_COUNTS["total"],
            "prototype_disposition_counts": EXPECTED_PROTOTYPE_DISPOSITIONS,
            "reference_drift_prototype_ids": REFERENCE_DRIFT_IDS,
            "w3q_123_disposition": "NO_PRODUCT_RANKING_ADMISSION",
            "deterministic_two_run_byte_equivalent": True,
            "source_depth_boundaries_machine_enforced": True,
        }
    )

    payload_objects: dict[str, object] = {
        "chapter4-product-handoff.json": release["chapter4-product-handoff.json"],
        "chapter5-product-handoff.json": release["chapter5-product-handoff.json"],
        "claim-overclaim-blacklist.json": release["claim-overclaim-blacklist.json"],
        "source-identity-package.json": release["source-identity-package.json"],
        "claim-inspection-manifest.json": release["claim-inspection-manifest.json"],
        "prototype-audit.json": proto,
        "ranking-audit.json": rank,
        "integrity-summary.json": summary,
        "claim-digests.json": claim_digests,
        "claim-source-edge-ids.json": edge_index,
        "semantic-boundary-policy.json": semantic_policy,
    }
    payload_bytes = {name: canonical_bytes(value) for name, value in payload_objects.items()}
    payload_hashes = {name: sha256_bytes(payload) for name, payload in sorted(payload_bytes.items())}
    release_payload_sha256 = core.stable_hash(payload_hashes)

    manifest = {
        "schema_version": SCHEMA_VERSION,
        "release_format_version": RELEASE_FORMAT_VERSION,
        "release_id": EXPECTED_AUTHORITY_DIGEST,
        "immutable": True,
        "research_authority_sha": AUTHORITY_SHA,
        "authority_digest_sha256": EXPECTED_AUTHORITY_DIGEST,
        "whole_authority_sha256": EXPECTED_AUTHORITY_DIGEST,
        "authority_digest_definition": "SHA-256 stable hash of the ordered 144 (candidate_id, effective_claim_digest) pairs derived from effective Research records.",
        "release_payload_sha256": release_payload_sha256,
        "payload_file_sha256": payload_hashes,
        "counts": EXPECTED_COUNTS,
        "prototype_disposition_counts": EXPECTED_PROTOTYPE_DISPOSITIONS,
        "reference_drift_prototype_ids": REFERENCE_DRIFT_IDS,
        "w3q_123_disposition": "NO_PRODUCT_RANKING_ADMISSION",
        "generator": "1_PETER_BOT/scripts/build_product_handoff_release.py",
        "determinism": "TWO_INDEPENDENT_CANONICAL_GENERATOR_RUNS_BYTE_EQUIVALENT",
        "release_path": f"1_PETER_BOT/product_handoff/releases/{EXPECTED_AUTHORITY_DIGEST}",
    }
    payload_bytes["release-manifest.json"] = canonical_bytes(manifest)
    return payload_bytes


def build_release_files() -> dict[str, bytes]:
    base, _ = core.read_candidates()
    effective, _ = core.apply_overrides(base)
    validate_semantic_boundaries(effective)
    assert_expected_authority_digest(authority_digest_from_effective(effective))

    with tempfile.TemporaryDirectory(prefix="1peter-handoff-a-") as a_name, tempfile.TemporaryDirectory(prefix="1peter-handoff-b-") as b_name:
        a = Path(a_name)
        b = Path(b_name)
        run_core(a)
        run_core(b)
        assert_raw_byte_equivalence(a, b)
        raw_a = load_raw(a)
        raw_b = load_raw(b)
        validate_raw(raw_a)
        validate_raw(raw_b)
        release_a = enrich_release(raw_a)
        release_b = enrich_release(raw_b)
        if release_a.keys() != release_b.keys():
            raise ReleaseError("release file-set nondeterminism")
        for name in release_a:
            if release_a[name] != release_b[name]:
                raise ReleaseError(f"release semantic byte nondeterminism: {name}")
        return release_a


def pointer_bytes() -> bytes:
    return canonical_bytes(
        {
            "schema_version": SCHEMA_VERSION,
            "release_format_version": RELEASE_FORMAT_VERSION,
            "immutable_release": True,
            "research_authority_sha": AUTHORITY_SHA,
            "authority_digest_sha256": EXPECTED_AUTHORITY_DIGEST,
            "whole_authority_sha256": EXPECTED_AUTHORITY_DIGEST,
            "release_path": f"releases/{EXPECTED_AUTHORITY_DIGEST}",
            "ranking_disposition_w3q_123": "NO_PRODUCT_RANKING_ADMISSION",
        }
    )


def write_release(output_root: Path, files: dict[str, bytes]) -> Path:
    release_dir = output_root / "releases" / EXPECTED_AUTHORITY_DIGEST
    if release_dir.exists():
        shutil.rmtree(release_dir)
    release_dir.mkdir(parents=True, exist_ok=True)
    for name, payload in sorted(files.items()):
        (release_dir / name).write_bytes(payload)
    (output_root / "CURRENT_RELEASE.json").write_bytes(pointer_bytes())
    return release_dir


def verify_committed(verify_root: Path, files: dict[str, bytes]) -> None:
    expected_pointer = pointer_bytes()
    actual_pointer = (verify_root / "CURRENT_RELEASE.json").read_bytes()
    if actual_pointer != expected_pointer:
        raise ReleaseError("canonical release pointer byte drift")
    release_dir = verify_root / "releases" / EXPECTED_AUTHORITY_DIGEST
    expected_names = set(files)
    actual_names = {p.name for p in release_dir.iterdir() if p.is_file()}
    if actual_names != expected_names:
        raise ReleaseError(
            f"committed immutable release file set drift: expected {sorted(expected_names)}, got {sorted(actual_names)}"
        )
    for name, payload in files.items():
        if (release_dir / name).read_bytes() != payload:
            raise ReleaseError(f"committed immutable release byte drift: {name}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-root", required=True)
    parser.add_argument("--verify-root")
    args = parser.parse_args()

    files = build_release_files()
    output_root = Path(args.output_root)
    output_root.mkdir(parents=True, exist_ok=True)
    release_dir = write_release(output_root, files)
    if args.verify_root:
        verify_committed(Path(args.verify_root), files)

    manifest = json.loads((release_dir / "release-manifest.json").read_text(encoding="utf-8"))
    print(json.dumps({
        "status": "IMMUTABLE_HANDOFF_RELEASE_VALID",
        "research_authority_sha": AUTHORITY_SHA,
        "authority_digest_sha256": EXPECTED_AUTHORITY_DIGEST,
        "release_payload_sha256": manifest["release_payload_sha256"],
        "release_files": len(files),
        "counts": EXPECTED_COUNTS,
        "prototype_disposition_counts": EXPECTED_PROTOTYPE_DISPOSITIONS,
        "w3q_123_disposition": "NO_PRODUCT_RANKING_ADMISSION",
        "verified_committed_release": bool(args.verify_root),
    }, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except (ReleaseError, core.AuditError, AssertionError, OSError, ValueError) as exc:
        print(f"IMMUTABLE_HANDOFF_RELEASE_FAIL: {exc}", file=sys.stderr)
        sys.exit(2)
