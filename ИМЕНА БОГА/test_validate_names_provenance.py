"""Adversarial graph tests: linking is necessary but never publication approval."""
from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from validate_names_provenance import validate_provenance

ROOT = Path(__file__).resolve().parent


class ProvenanceGraphTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.baseline = json.loads((ROOT / "data/names_ledger_v1.json").read_text(encoding="utf-8"))
        cls.extension = json.loads((ROOT / "data/names_extension_ledger_v1.json").read_text(encoding="utf-8"))
        cls.sources = json.loads((ROOT / "data/source_access_register_v1.json").read_text(encoding="utf-8"))
        cls.editions = json.loads((ROOT / "data/names_edition_registry_v1.json").read_text(encoding="utf-8"))
        cls.claims = json.loads((ROOT / "data/names_claim_registry_v1.json").read_text(encoding="utf-8"))

    def check(self, **overrides) -> list[str]:
        return validate_provenance(
            overrides.get("baseline", self.baseline),
            overrides.get("extension", self.extension),
            overrides.get("sources", self.sources),
            overrides.get("editions", self.editions),
            overrides.get("claims", self.claims),
        )

    def mutate(self, rid: str, ledger: str = "baseline", index: int = 0) -> tuple[dict, dict]:
        clone = copy.deepcopy(self.baseline if ledger == "baseline" else self.extension)
        row = next(x for x in clone["records"] if x["id"] == rid)
        return clone, row["attestations"][index]

    def test_current_105_observations_have_valid_source_edition_edges(self) -> None:
        self.assertEqual([], self.check())

    def test_cannot_delete_an_entire_record_occurrence_link(self) -> None:
        d, att = self.mutate("yah", "extension", 0)
        row = next(r for r in d["records"] if r["id"] == "yah")
        row["attestations"].pop(0)
        self.assertTrue(any("105 current" in e for e in self.check(extension=d)))

    def test_candidate_local_stable_id_cannot_be_reassigned(self) -> None:
        d, att = self.mutate("el", "baseline", 1)
        att["attestationId"] = "ATT-BASE-YHWH-01"
        self.assertTrue(any("missing/duplicate/stale attestation ID" in e for e in self.check(baseline=d)))

    def test_duplicate_attestation_id_is_not_a_valid_verse_witness(self) -> None:
        d, att = self.mutate("yireh", "baseline", 1)
        att["attestationId"] = "ATT-BASE-YIREH-01"
        self.assertTrue(any("duplicate/stale attestation" in e for e in self.check(baseline=d)))

    def test_source_id_cannot_be_a_deleted_source(self) -> None:
        d, att = self.mutate("yhwh")
        att["sourceId"] = "SRC-NONEXISTENT"
        self.assertTrue(any("orphan source" in e for e in self.check(baseline=d)))

    def test_exodus_yhwh_cannot_inherit_sblgnt_edition(self) -> None:
        d, att = self.mutate("yhwh")
        att["editionId"] = "ED-SBLGNT-2010-BIBLEGATEWAY"
        self.assertTrue(any("edition text does not match" in e for e in self.check(baseline=d)))

    def test_daniel_aramaic_not_automatically_hebrew_mt_source(self) -> None:
        d, att = self.mutate("elah-shmaya", "extension")
        att["sourceId"] = "SRC-MT-MECHON"
        self.assertTrue(any("MT Aramaic/Hebrew" in e for e in self.check(extension=d)))

    def test_lxx_exodus17_not_ancient_greek_isaiah_7(self) -> None:
        d, att = self.mutate("nissi", "baseline", 1)
        att["sourceId"] = "SRC-RAHLFS-ISAIAH"
        self.assertTrue(any("publisher LXX chapter/edition" in e for e in self.check(baseline=d)))

    def test_sblgnt_verse_host_must_not_inherit_publisher_ccby_license_record(self) -> None:
        d, att = self.mutate("ego-eimi", "baseline", 2)
        att["sourceId"] = "SRC-SBLGNT-CCBY-LICENSE"
        self.assertTrue(any("SBLGNT passage source incorrectly" in e for e in self.check(baseline=d)))

    def test_untagged_multiedition_james5_4_not_edition_pinned(self) -> None:
        d, att = self.mutate("sabaoth", "baseline", 4)
        att["editionPinStatus"] = "URL_VERSION_PINNED"
        self.assertTrue(any("unpinned Greek edition" in e for e in self.check(baseline=d)))

    def test_new_multiedition_page_cannot_be_whitelisted_by_accident(self) -> None:
        d, att = self.mutate("ego-eimi", "baseline", 1)
        att["sourceUrl"] = "https://www.biblegateway.com/verse/grc/John%208%3A58"
        att["editionPinStatus"] = "MULTI_EDITION_DISPLAY_REQUIRES_RECHECK"
        self.assertTrue(any("unpinned Greek edition" in e for e in self.check(baseline=d)))

    def test_thgnt_luke_edition_selection_hold_must_remain(self) -> None:
        d, att = self.mutate("kyrios-ho-theos", "extension")
        att["editionPinStatus"] = "URL_VERSION_PINNED"
        self.assertTrue(any("THGNT multiedition display" in e for e in self.check(extension=d)))

    def test_claim_cannot_point_to_no_original_verse(self) -> None:
        d = copy.deepcopy(self.claims)
        x = next(c for c in d["records"] if c["claimId"] == "CLM-JOHN9-9-HUMAN-EGO-EIMI")
        x["attestationIds"] = ["ATT-BASE-YHWH-01"]
        self.assertTrue(any("lost its independently reviewed text witnesses" in e for e in self.check(claims=d)))

    def test_claim_cannot_cite_a_nonexistent_text_witness(self) -> None:
        d = copy.deepcopy(self.claims)
        d["records"][0]["attestationIds"] = ["ATT-BASE-FOO-99"]
        self.assertTrue(any("orphaned attestation" in e for e in self.check(claims=d)))

    def test_claim_source_link_must_include_direct_original_text(self) -> None:
        d = copy.deepcopy(self.claims)
        x = next(c for c in d["records"] if c["claimId"] == "CLM-LXX-EX3-JOHN8-DIFFERENT-CLAUSES")
        x["sourceIds"] = ["SRC-ROESEL-2007"]
        self.assertTrue(any("lost mandatory direct textual sources" in e for e in self.check(claims=d)))

    def test_claim_is_not_product_ready_after_structural_linking(self) -> None:
        d = copy.deepcopy(self.claims)
        d["records"][0]["publicationState"] = "READY_FOR_SITE"
        self.assertTrue(any("falsely authorized for Product" in e for e in self.check(claims=d)))

    def test_edition_cannot_claim_manuscript_collation(self) -> None:
        d = copy.deepcopy(self.editions)
        d["records"][0]["criticalEditionCollated"] = True
        self.assertTrue(any("falsely promoted" in e for e in self.check(editions=d)))

    def test_thgnt_edition_copyright_gate_must_remain(self) -> None:
        d = copy.deepcopy(self.editions)
        x = next(e for e in d["records"] if e["id"] == "ED-THGNT-2017-BIBLEGATEWAY")
        x["rightsState"] = "PUBLICATION_ELIGIBLE"
        self.assertTrue(any("copyright of Greek edition" in e for e in self.check(editions=d)))


    def test_new_research_claim_can_be_added_without_editing_seed_list(self) -> None:
        d = copy.deepcopy(self.claims)
        c = copy.deepcopy(d["records"][0])
        c["claimId"] = "CLM-NEW-VERIFIED-EDGE"
        c["statement"] = "A strictly provisional original-script locus claim for review."
        d["records"].append(c)
        self.assertEqual([], self.check(claims=d))

    def test_new_claim_cannot_avoid_mandatory_direct_source(self) -> None:
        d = copy.deepcopy(self.claims)
        c = copy.deepcopy(d["records"][0])
        c["claimId"] = "CLM-NEW-BROKEN-EDGE"
        c["sourceIds"] = ["SRC-ROESEL-2007"]
        d["records"].append(c)
        self.assertTrue(any("lost mandatory direct textual sources" in e for e in self.check(claims=d)))

    def test_duplicate_claim_id_rejected_even_when_seed_count_preserved(self) -> None:
        d = copy.deepcopy(self.claims)
        d["records"].append(copy.deepcopy(d["records"][0]))
        self.assertTrue(any("duplicate claim ID" in e for e in self.check(claims=d)))

    def test_malformed_claim_is_a_validation_failure_not_exception(self) -> None:
        d = copy.deepcopy(self.claims)
        d["records"].append({"claimId": ["not-a-string"]})
        self.assertTrue(any("malformed claim ID" in e for e in self.check(claims=d)))

    def test_unknown_claim_type_cannot_be_inferred(self) -> None:
        d = copy.deepcopy(self.claims)
        d["records"][0]["claimType"] = "FULLY_CERTIFIED"
        self.assertTrue(any("untyped editorial assertion" in e for e in self.check(claims=d)))

    def test_claim_must_preserve_pending_review_tasks(self) -> None:
        d = copy.deepcopy(self.claims)
        d["records"][0]["reviewNeeded"] = []
        self.assertTrue(any("pending independent review tasks" in e for e in self.check(claims=d)))

    def test_orphaned_relation_is_rejected(self) -> None:
        d = copy.deepcopy(self.claims)
        d["semanticRelations"][0]["toClaimId"] = "CLM-NONEXISTENT"
        self.assertTrue(any("orphaned or self-referential claim edge" in e for e in self.check(claims=d)))

    def test_unknown_relation_type_does_not_pass(self) -> None:
        d = copy.deepcopy(self.claims)
        d["semanticRelations"][0]["relationType"] = "SAME_DIVINE_NAME"
        self.assertTrue(any("unknown semantic relation type" in e for e in self.check(claims=d)))

    def test_immutable_relation_cannot_be_dropped(self) -> None:
        d = copy.deepcopy(self.claims)
        d["semanticRelations"].pop()
        self.assertTrue(any("required semantic boundary" in e for e in self.check(claims=d)))

    def test_relation_cannot_promote_to_product(self) -> None:
        d = copy.deepcopy(self.claims)
        d["semanticRelations"][0]["publicationState"] = "READY"
        self.assertTrue(any("unlawfully promoted relationship" in e for e in self.check(claims=d)))

    def test_relation_self_loop_is_rejected(self) -> None:
        d = copy.deepcopy(self.claims)
        d["semanticRelations"][0]["toClaimId"] = d["semanticRelations"][0]["fromClaimId"]
        self.assertTrue(any("self-referential claim edge" in e for e in self.check(claims=d)))

    def test_unhashable_attestation_reference_fails_closed(self) -> None:
        d = copy.deepcopy(self.claims)
        d["records"][0]["attestationIds"] = [["malformed"]]
        self.assertTrue(any("non-string or duplicate text references" in e for e in self.check(claims=d)))

    def test_non_string_source_reference_fails_closed(self) -> None:
        d = copy.deepcopy(self.claims)
        d["records"][0]["sourceIds"] = [{"not": "an ID"}]
        self.assertTrue(any("lacking unique source references" in e for e in self.check(claims=d)))

    def test_new_semantic_relation_with_valid_research_edges_is_allowed(self) -> None:
        d = copy.deepcopy(self.claims)
        d["semanticRelations"].append({
            "relationId": "REL-EXTRA-VALID",
            "fromClaimId": "CLM-EX3-15-DIVINE-NAME",
            "toClaimId": "CLM-ABBA-THREE-PRAYER-SUBJECTS",
            "relationType": "LIMITS_INFERENCE",
            "rationale": "Merely a typed research-only comparative boundary, not a doctrinal identity.",
            "publicationState": "BLOCKED",
        })
        self.assertEqual([], self.check(claims=d))


if __name__ == "__main__":
    unittest.main()
