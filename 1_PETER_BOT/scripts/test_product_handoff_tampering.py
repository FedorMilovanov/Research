#!/usr/bin/env python3
from __future__ import annotations

import copy
import sys

import build_product_handoff_release as release
import validate_product_handoff as core


def expect_release_error(label, fn):
    try:
        fn()
    except release.ReleaseError:
        return
    raise AssertionError(f"tamper test did not fail closed: {label}")


def main() -> None:
    base, _ = core.read_candidates()
    effective, _ = core.apply_overrides(base)
    baseline_digest = release.authority_digest_from_effective(effective)
    release.assert_expected_authority_digest(baseline_digest)
    release.validate_semantic_boundaries(effective)

    # 1. Keeping the same w3q identity does not preserve content authority.
    claim_tamper = copy.deepcopy(effective)
    claim_tamper["w3q_001"]["keyed_concept"] = str(claim_tamper["w3q_001"].get("keyed_concept") or "") + " [TAMPER]"
    tampered_digest = release.authority_digest_from_effective(claim_tamper)
    assert tampered_digest != baseline_digest
    expect_release_error(
        "effective claim changed while candidate ID stayed stable",
        lambda: release.assert_expected_authority_digest(tampered_digest),
    )

    identity_lanes, inspection_lanes = core.read_sources()
    actual_edge = core.inspection_for(effective["w3q_001"], identity_lanes, inspection_lanes)[0]
    assert release.compute_edge_id(actual_edge) == actual_edge["claim_inspection_edge_id"]

    # 2. Source ownership and source depth are content-addressed on the claim edge.
    owner_tamper = copy.deepcopy(actual_edge)
    owner_tamper["owning_lane"] = owner_tamper["owning_lane"] + ".tampered"
    assert release.compute_edge_id(owner_tamper) != actual_edge["claim_inspection_edge_id"]

    depth_tamper = copy.deepcopy(actual_edge)
    depth_tamper["inspection_scope"] = str(depth_tamper["inspection_scope"]) + "; tampered_depth"
    assert release.compute_edge_id(depth_tamper) != actual_edge["claim_inspection_edge_id"]

    # 3. Access state is not passage evidence and cannot upgrade inspection depth.
    access_only = {
        "inspection_scope": "UNSPECIFIED",
        "evidence_status": "NOT_EXPLICITLY_LABELED",
        "access_state": "FULL_OBJECT",
    }
    baseline_class = core.inspection_depth_class(access_only)
    assert baseline_class != "CLAIM_INSPECTION_PRESENT"
    access_only["access_state"] = "PARTIAL_OBJECT"
    assert core.inspection_depth_class(access_only) == baseline_class

    # 4. The same source ID in a later/stronger lane does not lend its depth to a claim
    # whose effective source_minimum was authored in an earlier lane. layer_of()/
    # provenance_layer() normalize wave3g -> 3g and wave3n -> 3n.
    fake_claim = {
        "id": "w3q_fake_depth_boundary",
        "source_minimum": ["shared_source"],
        "_field_provenance": {
            "source_minimum": "override:question-overrides-wave3g.json"
        },
    }
    fake_inspection_lanes = {
        "shared_source": [
            {
                "path": "data/source-quorum-wave3g.json",
                "layer": "3g",
                "record": {
                    "source_id": "shared_source",
                    "evidence_status": "BIBLIOGRAPHIC_ONLY",
                    "access_state": "FULL_OBJECT",
                    "inspection_scope": "catalog_metadata_only",
                    "claim_limit": "identity/control only",
                },
                "lane_kind": "CLAIM_QUORUM",
            },
            {
                "path": "data/source-quorum-wave3n.json",
                "layer": "3n",
                "record": {
                    "source_id": "shared_source",
                    "evidence_status": "INSPECTED_FULL_TEXT",
                    "access_state": "FULL_OBJECT",
                    "inspection_scope": "exact_passage_inspected",
                    "claim_limit": "later independent claim lane",
                },
                "lane_kind": "CLAIM_QUORUM",
            },
        ]
    }
    fake_edges = core.inspection_for(fake_claim, {}, fake_inspection_lanes)
    assert len(fake_edges) == 1
    assert fake_edges[0]["owning_lane"] == "data/source-quorum-wave3g.json"
    assert fake_edges[0]["inspection_depth_class"] != "CLAIM_INSPECTION_PRESENT"
    assert core.exact_claim_ready(fake_edges) is False

    # 5. A project position cannot silently become neutral merely by editing the record.
    project_tamper = copy.deepcopy(effective)
    project_tamper["w3q_013"]["position"] = "neutral"
    assert release.authority_digest_from_effective(project_tamper) != baseline_digest
    expect_release_error(
        "project position silently neutralized",
        lambda: release.validate_semantic_boundaries(project_tamper),
    )

    # 6. ECM-based evidence cannot be relabeled as direct dECM readback.
    decm_tamper = copy.deepcopy(effective)
    decm_tamper["w3q_031"]["keyed_concept"] = str(decm_tamper["w3q_031"].get("keyed_concept") or "") + " Direct dECM readback."
    expect_release_error(
        "ECM-based treatment relabeled direct dECM",
        lambda: release.validate_semantic_boundaries(decm_tamper),
    )

    # 7. A named witness cannot be inflated into manuscript unanimity.
    manuscript_tamper = copy.deepcopy(effective)
    manuscript_tamper["w3q_137"]["keyed_concept"] = str(manuscript_tamper["w3q_137"].get("keyed_concept") or "") + " All manuscripts read this expansion."
    expect_release_error(
        "named manuscript inflated to manuscript unanimity",
        lambda: release.validate_semantic_boundaries(manuscript_tamper),
    )

    print(
        "TAMPER_SUITE_OK "
        "claim_digest source_owner source_depth access_vs_evidence lane_depth project_position ecm_vs_decm manuscript_unanimity"
    )


if __name__ == "__main__":
    try:
        main()
    except (AssertionError, core.AuditError, release.ReleaseError, OSError, ValueError) as exc:
        print(f"TAMPER_SUITE_FAIL: {exc}", file=sys.stderr)
        sys.exit(2)
