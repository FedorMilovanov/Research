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
        att["sourceUrl"] = "https://www.biblegateway.com/verse/grc/James%205%3A4"
        self.assertTrue(any("unpinned Greek edition" in e for e in self.check(baseline=d)))

    def test_new_multiedition_page_cannot_be_whitelisted_by_accident(self) -> None:
        d, att = self.mutate("ego-eimi", "baseline", 1)
        att["sourceUrl"] = "https://www.biblegateway.com/verse/grc/John%208%3A58"
        att["editionPinStatus"] = "MULTI_EDITION_DISPLAY_REQUIRES_RECHECK"
        self.assertTrue(any("unpinned Greek edition" in e for e in self.check(baseline=d)))

    def test_thgnt_luke_edition_selection_hold_must_remain(self) -> None:
        d, att = self.mutate("kyrios-ho-theos", "extension")
        att["sourceUrl"] = "https://www.biblegateway.com/verse/grc/Luke%201%3A32"
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


    def test_four_greek_urls_are_single_edition_and_original_verse_covered(self) -> None:
        for rid, index, kind in [
            ("sabaoth", 4, "baseline"),
            ("sabaoth", 5, "baseline"),
            ("abba", 2, "baseline"),
            ("kyrios-ho-theos", 0, "extension"),
        ]:
            doc = self.baseline if kind == "baseline" else self.extension
            row = next(x for x in doc["records"] if x["id"] == rid)["attestations"][index]
            self.assertEqual("URL_VERSION_PINNED", row["editionPinStatus"])
            self.assertIn(row["sourceUrl"], [
                "https://www.biblegateway.com/passage/?search=James+5%3A1-11&version=SBLGNT",
                "https://www.biblegateway.com/passage/?search=Romans+9%3A14-29&version=SBLGNT",
                "https://www.biblegateway.com/passage/?search=Galatians+4%3A4-7&version=SBLGNT",
                "https://www.biblegateway.com/passage/?search=Luke+1%3A30-33&version=THGNT",
            ])

    def test_greek_version_must_not_be_multi_edition_encoded(self) -> None:
        d, att = self.mutate("abba", "baseline", 2)
        att["sourceUrl"] = "https://www.biblegateway.com/passage/?search=Galatians+4%3A4-7&version=SBLGNT%3BTHGNT"
        self.assertTrue(any("unpinned Greek edition" in e for e in self.check(baseline=d)))

    def test_greek_version_must_not_be_repeated(self) -> None:
        d, att = self.mutate("abba", "baseline", 2)
        att["sourceUrl"] += "&version=SBLGNT"
        self.assertTrue(any("unpinned Greek edition" in e for e in self.check(baseline=d)))

    def test_pinned_greek_book_cannot_be_switched(self) -> None:
        d, att = self.mutate("abba", "baseline", 2)
        att["sourceUrl"] = "https://www.biblegateway.com/passage/?search=Romans+4%3A4-7&version=SBLGNT"
        self.assertTrue(any("wrong SBLGNT verse" in e for e in self.check(baseline=d)))

    def test_pinned_greek_verse_must_be_in_passage_range(self) -> None:
        d, att = self.mutate("abba", "baseline", 2)
        att["sourceUrl"] = "https://www.biblegateway.com/passage/?search=Galatians+4%3A1-5&version=SBLGNT"
        self.assertTrue(any("wrong SBLGNT verse" in e for e in self.check(baseline=d)))

    def test_pinned_greek_passage_cannot_be_a_fake_host(self) -> None:
        d, att = self.mutate("abba", "baseline", 2)
        att["sourceUrl"] = "https://evil.invalid/passage/?search=Galatians+4%3A4-7&version=SBLGNT"
        self.assertTrue(any("unpinned Greek edition" in e for e in self.check(baseline=d)))

    def test_pinned_greek_passage_requires_https(self) -> None:
        d, att = self.mutate("abba", "baseline", 2)
        att["sourceUrl"] = att["sourceUrl"].replace("https:", "http:", 1)
        self.assertTrue(any("unpinned Greek edition" in e for e in self.check(baseline=d)))

    def test_pinned_greek_evidence_anchor_drift_rejected(self) -> None:
        d, att = self.mutate("abba", "baseline", 2)
        att["sourceUrl"] = "https://www.biblegateway.com/passage/?search=Galatians+4&version=SBLGNT"
        self.assertTrue(any("verified pinned Greek passage URL changed" in e for e in self.check(baseline=d)))

    def test_thgnt_cannot_inherit_sblgnt_link(self) -> None:
        d, att = self.mutate("kyrios-ho-theos", "extension", 0)
        att["sourceUrl"] = "https://www.biblegateway.com/passage/?search=Luke+1%3A30-33&version=SBLGNT"
        self.assertTrue(any("THGNT multiedition display" in e for e in self.check(extension=d)))

    def test_thgnt_original_verse_cannot_be_replaced_by_neighbor(self) -> None:
        d, att = self.mutate("kyrios-ho-theos", "extension", 0)
        att["sourceUrl"] = "https://www.biblegateway.com/passage/?search=Luke+1%3A33&version=THGNT"
        self.assertTrue(any("wrong verse" in e for e in self.check(extension=d)))


    def test_four_new_claims_provisionally_link_pinned_original_verses(self) -> None:
        expected = {
            "CLM-JAS5-4-SABAOTH-GENITIVE": "ATT-BASE-SABAOTH-05",
            "CLM-ROM9-29-SABAOTH-ISAIAH": "ATT-BASE-SABAOTH-06",
            "CLM-GAL4-6-ABBA-SPIRIT": "ATT-BASE-ABBA-03",
            "CLM-LUK1-32-GABRIEL-AGENT": "ATT-EXT-KYRIOS-HO-THEOS-01",
        }
        for cid, aid in expected.items():
            row = next(c for c in self.claims["records"] if c["claimId"] == cid)
            self.assertEqual([aid], row["attestationIds"])
            self.assertEqual("RESEARCH_HOLD", row["editorialState"])
            self.assertEqual("BLOCKED", row["publicationState"])

    def test_required_greek_claim_cannot_be_erased(self) -> None:
        d = copy.deepcopy(self.claims)
        d["records"] = [r for r in d["records"] if r["claimId"] != "CLM-ROM9-29-SABAOTH-ISAIAH"]
        self.assertTrue(any("Greek source-pinned claim seeds missing" in e for e in self.check(claims=d)))

    def test_greek_claim_cannot_swap_pinned_attestation(self) -> None:
        d = copy.deepcopy(self.claims)
        row = next(c for c in d["records"] if c["claimId"] == "CLM-JAS5-4-SABAOTH-GENITIVE")
        row["attestationIds"] = ["ATT-BASE-SABAOTH-06"]
        self.assertTrue(any("lost its independently reviewed text witnesses" in e for e in self.check(claims=d)))

    def test_new_greek_claim_must_retain_direct_edition_source(self) -> None:
        d = copy.deepcopy(self.claims)
        row = next(c for c in d["records"] if c["claimId"] == "CLM-LUK1-32-GABRIEL-AGENT")
        row["sourceIds"] = ["SRC-SBLGNT-DIGITAL-NT"]
        self.assertTrue(any("lost mandatory direct textual sources" in e for e in self.check(claims=d)))

    def test_new_semantic_relation_cannot_silently_change_case(self) -> None:
        d = copy.deepcopy(self.claims)
        row = next(x for x in d["semanticRelations"] if x["relationId"] == "REL-SABAOTH-CASING-CONTEXT")
        row["relationType"] = "CONTRASTS_REFERENT"
        self.assertTrue(any("required semantic boundary" in e for e in self.check(claims=d)))


    def test_divine_egoeimi_in_exodus_cannot_refer_to_moses(self) -> None:
        for idx in (0, 1, 2):
            d, obs = self.mutate("ehyeh", "baseline", idx)
            obs["referent"] = "Moses"
            self.assertTrue(any("divine self-reference wrongly attributed" in e for e in self.check(baseline=d)))

    def test_moses_is_addressee_not_formal_divine_referent(self) -> None:
        for idx in (0, 1, 2):
            d, obs = self.mutate("ehyeh", "baseline", idx)
            obs.pop("addressee")
            self.assertTrue(any("missing or incorrect speech addressee" in e for e in self.check(baseline=d)))

    def test_exodus_three_speech_cannot_be_reassigned_to_moses(self) -> None:
        d, obs = self.mutate("ehyeh", "baseline", 1)
        obs["speaker"] = "Moses"
        self.assertTrue(any("divine first-person speaker changed" in e for e in self.check(baseline=d)))

    def test_exodus_role_claim_is_required(self) -> None:
        d = copy.deepcopy(self.claims)
        d["records"] = [x for x in d["records"] if x["claimId"] != "CLM-EX3-EHYEH-DIVINE-REFERENT"]
        self.assertTrue(any("Exodus 3 divine referent claim missing" in e for e in self.check(claims=d)))

    def test_exodus_role_claim_requires_all_three_loci(self) -> None:
        d = copy.deepcopy(self.claims)
        row = next(x for x in d["records"] if x["claimId"] == "CLM-EX3-EHYEH-DIVINE-REFERENT")
        row["attestationIds"].remove("ATT-BASE-EHYEH-01")
        self.assertTrue(any("lost its independently reviewed text witnesses" in e for e in self.check(claims=d)))

    def test_exodus_role_relation_stays_bound_to_correct_claims(self) -> None:
        d = copy.deepcopy(self.claims)
        row = next(x for x in d["semanticRelations"] if x["relationId"] == "REL-EX3-SELF-SPEECH-VS-ADDRESSEE")
        row["toClaimId"] = "CLM-YHWH-HISTORICAL-PRONUNCIATION"
        self.assertTrue(any("required semantic boundary" in e for e in self.check(claims=d)))


    def test_three_prophetic_names_remain_correctly_typed_and_held(self) -> None:
        cases = {
            "CLM-JER23-6-DAVIDIC-ROYAL-NAME": "ATT-BASE-TSIDKENU-01",
            "CLM-JER33-16-JERUSALEM-CITY-NAME": "ATT-BASE-TSIDKENU-02",
            "CLM-EZ48-35-CITY-NAMING": "ATT-BASE-SHAMMAH-01",
        }
        for cid,aid in cases.items():
            row = next(x for x in self.claims["records"] if x["claimId"]==cid)
            self.assertEqual([aid],row["attestationIds"])
            self.assertEqual("RESEARCH_HOLD",row["editorialState"])
            self.assertEqual("BLOCKED",row["publicationState"])

    def test_jeremiah_royal_claim_cannot_be_reassigned_to_city_verse(self) -> None:
        d = copy.deepcopy(self.claims)
        row=next(x for x in d["records"] if x["claimId"]=="CLM-JER23-6-DAVIDIC-ROYAL-NAME")
        row["attestationIds"]=["ATT-BASE-TSIDKENU-02"]
        self.assertTrue(any("lost its independently reviewed text witnesses" in x for x in self.check(claims=d)))

    def test_city_claim_cannot_erase_mt_verse_source(self) -> None:
        d=copy.deepcopy(self.claims)
        row=next(x for x in d["records"] if x["claimId"]=="CLM-JER33-16-JERUSALEM-CITY-NAME")
        row["sourceIds"]=["SRC-VT-LIEBERMANN-JEREMIAH-2023"]
        self.assertTrue(any("lost mandatory direct textual sources" in x for x in self.check(claims=d)))

    def test_prophetic_city_claim_cannot_disappear_silently(self) -> None:
        d=copy.deepcopy(self.claims)
        d["records"]=[r for r in d["records"] if r["claimId"]!="CLM-EZ48-35-CITY-NAMING"]
        self.assertTrue(any("required prophetic royal/city claim boundary missing" in x for x in self.check(claims=d)))

    def test_royal_and_city_semantic_relation_is_immutable(self) -> None:
        d=copy.deepcopy(self.claims)
        row=next(x for x in d["semanticRelations"] if x["relationId"]=="REL-JER-ROYAL-CITY-NAMING")
        row["relationType"]="SPECIFIES_SPEECH_AGENT"
        self.assertTrue(any("required semantic boundary" in x for x in self.check(claims=d)))



    def test_rock_three_claims_cover_five_distinct_loci(self) -> None:
        exact = {
            "CLM-DEUT32-ROCK-DIVINE-METAPHOR": {
                "ATT-BASE-TSUR-01", "ATT-BASE-TSUR-02", "ATT-BASE-TSUR-05"
            },
            "CLM-DEUT32-31-ROCK-CONTRAST": {"ATT-BASE-TSUR-03"},
            "CLM-DEUT32-37-FOREIGN-REFUGE": {"ATT-BASE-TSUR-04"},
        }
        for cid, wanted in exact.items():
            item = next(x for x in self.claims["records"] if x["claimId"] == cid)
            self.assertEqual(wanted, set(item["attestationIds"]))
            self.assertEqual("RESEARCH_HOLD", item["editorialState"])
            self.assertEqual("BLOCKED", item["publicationState"])

    def test_rock_divine_context_does_not_become_foreign(self) -> None:
        d,obs = self.mutate("tsur","baseline",0)
        obs["referentClass"] = "FALSE_OBJECT_OF_REFUGE"
        self.assertTrue(any("Rock referent/isDivineDesignation conflated" in e for e in self.check(baseline=d)))

    def test_rock_mixed_context_does_not_become_all_divine(self) -> None:
        d,obs = self.mutate("tsur","baseline",2)
        obs["referentClass"] = "TRUE_GOD"
        obs["isDivineDesignation"] = True
        self.assertTrue(any("Rock referent/isDivineDesignation conflated" in e for e in self.check(baseline=d)))

    def test_rock_foreign_context_does_not_become_yhwh(self) -> None:
        d,obs = self.mutate("tsur","baseline",3)
        obs["referentClass"] = "TRUE_GOD"
        obs["isDivineDesignation"] = True
        self.assertTrue(any("Rock referent/isDivineDesignation conflated" in e for e in self.check(baseline=d)))

    def test_rock_is_divine_designation_cannot_be_inferred_for_mixed(self) -> None:
        d,obs = self.mutate("tsur","baseline",2)
        obs["isDivineDesignation"] = False
        self.assertTrue(any("Rock referent/isDivineDesignation conflated" in e for e in self.check(baseline=d)))

    def test_rock_claim_cannot_swap_a_mixed_locus_for_positive_one(self) -> None:
        d = copy.deepcopy(self.claims)
        item = next(x for x in d["records"] if x["claimId"] == "CLM-DEUT32-31-ROCK-CONTRAST")
        item["attestationIds"] = ["ATT-BASE-TSUR-01"]
        self.assertTrue(any("lost its independently reviewed text witnesses" in e for e in self.check(claims=d)))

    def test_rock_required_claim_cannot_be_deleted(self) -> None:
        d = copy.deepcopy(self.claims)
        d["records"] = [x for x in d["records"] if x["claimId"] != "CLM-DEUT32-37-FOREIGN-REFUGE"]
        self.assertTrue(any("required Rock contrast claim boundary missing" in e for e in self.check(claims=d)))

    def test_rock_relation_cannot_collapse_mixed_and_foreign(self) -> None:
        d = copy.deepcopy(self.claims)
        item = next(x for x in d["semanticRelations"] if x["relationId"] == "REL-TSUR-MIXED-AND-FOREIGN")
        item["toClaimId"] = "CLM-DEUT32-ROCK-DIVINE-METAPHOR"
        self.assertTrue(any("required semantic boundary" in e for e in self.check(claims=d)))

    def test_deut_32_30_pronoun_warning_cannot_be_lost(self) -> None:
        d = copy.deepcopy(self.claims)
        item = next(x for x in d["records"] if x["claimId"] == "CLM-DEUT32-31-ROCK-CONTRAST")
        item["statement"] = item["statement"].replace("32:30", "32:31")
        self.assertTrue(any("32:30 pronoun antecedent caution lost" in e for e in self.check(claims=d)))


    def test_immanuel_five_loci_must_have_distinct_claims(self) -> None:
        for i,cid in enumerate([
            "CLM-ISA7-14-CHILD-NAMING", "CLM-ISA7-14-LXX-NAMING-VERB",
            "CLM-ISA8-8-IMMANUEL-ADDRESS", "CLM-ISA8-10-DIVINE-PRESENCE",
            "CLM-MATT1-23-IMMANUEL-GLOSS"
        ], start=1):
            row=next(x for x in self.claims["records"] if x["claimId"]==cid)
            self.assertEqual([f"ATT-BASE-IMMANUEL-0{i}"],row["attestationIds"])
            self.assertEqual("RESEARCH_HOLD",row["editorialState"])
            self.assertEqual("BLOCKED",row["publicationState"])

    def test_isaiah_8_10_assurance_cannot_become_child_naming(self) -> None:
        d,o=self.mutate("immanuel","baseline",3)
        o["speechAct"]="prophetic_child_naming"
        self.assertTrue(any("Immanuel speech act/named object conflated" in e for e in self.check(baseline=d)))

    def test_isaiah_8_8_contextual_address_must_stay_uncertain(self) -> None:
        d,o=self.mutate("immanuel","baseline",2)
        o["namedObject"]="Jesus definitively addressed in the eighth-century oracle"
        self.assertTrue(any("Immanuel speech act/named object conflated" in e for e in self.check(baseline=d)))

    def test_isaiah_7_child_naming_cannot_become_divine_self_naming(self) -> None:
        d,o=self.mutate("immanuel","baseline",0)
        o["namedObject"]="God naming Himself"
        self.assertTrue(any("Immanuel speech act/named object conflated" in e for e in self.check(baseline=d)))

    def test_immanuel_lxx_verb_cannot_inherit_matthews_plural(self) -> None:
        d,o=self.mutate("immanuel","baseline",1)
        o["namingVerbForm"]="καλέσουσιν 3rd plural"
        self.assertTrue(any("LXX Isaiah καλέσεις vs Matthew" in e for e in self.check(baseline=d)))

    def test_immanuel_matthew_cannot_inherit_lxx_singular(self) -> None:
        d,o=self.mutate("immanuel","baseline",4)
        o["namingVerbForm"]="καλέσεις second person singular"
        self.assertTrue(any("Matthew Immanuel name grammar/gloss lost" in e for e in self.check(baseline=d)))

    def test_matthew_immanuel_explanatory_gloss_must_remain(self) -> None:
        d,o=self.mutate("immanuel","baseline",4)
        o.pop("translationInVerse")
        self.assertTrue(any("Matthew Immanuel name grammar/gloss lost" in e for e in self.check(baseline=d)))

    def test_immanuel_citation_cannot_be_reassigned_to_isaiah_8_10(self) -> None:
        d=json.loads(json.dumps(self.claims))
        row=next(x for x in d["records"] if x["claimId"]=="CLM-MATT1-23-IMMANUEL-GLOSS")
        row["attestationIds"]=["ATT-BASE-IMMANUEL-04"]
        self.assertTrue(any("lost its independently reviewed text witnesses" in e for e in self.check(claims=d)))

    def test_required_immanuel_claim_cannot_disappear(self) -> None:
        d=json.loads(json.dumps(self.claims))
        d["records"]=[x for x in d["records"] if x["claimId"]!="CLM-ISA8-8-IMMANUEL-ADDRESS"]
        self.assertTrue(any("required Immanuel textual role claims missing" in e for e in self.check(claims=d)))

    def test_immanuel_greek_comparison_relation_cannot_change(self) -> None:
        d=json.loads(json.dumps(self.claims))
        row=next(x for x in d["semanticRelations"] if x["relationId"]=="REL-IMMANUEL-LXX-MATTHEW-VERB")
        row["relationType"]="CONTRASTS_REFERENT"
        self.assertTrue(any("required semantic boundary" in e for e in self.check(claims=d)))

    def test_isaiah_8_8_10_semantic_boundary_cannot_change(self) -> None:
        d=json.loads(json.dumps(self.claims))
        row=next(x for x in d["semanticRelations"] if x["relationId"]=="REL-IMMANUEL-ISA8-ADDRESS-ASSERTION")
        row["toClaimId"]="CLM-MATT1-23-IMMANUEL-GLOSS"
        self.assertTrue(any("required semantic boundary" in e for e in self.check(claims=d)))


    def test_edition_specific_greek_immanuel_diacritics_not_interchanged(self) -> None:
        d,o=self.mutate("immanuel","baseline",1)
        o["surface"]="Ἐμμανουήλ"
        self.assertTrue(any("exact printed Immanuel source form changed" in e for e in self.check(baseline=d)))

    def test_isaiah_7_hebrew_almah_and_naming_verb_uncertainty_retained(self) -> None:
        d,o=self.mutate("immanuel","baseline",0)
        o["namingVerbAnalysis"]="no contested issue; exact same as Matthew"
        self.assertTrue(any("Isaiah 7 Hebrew lexeme/naming verb uncertainty erased" in e for e in self.check(baseline=d)))

    def test_sblgnt_matthew_single_edition_url_cannot_change(self) -> None:
        d,o=self.mutate("immanuel","baseline",4)
        o["sourceUrl"]="https://www.biblegateway.com/passage/?search=Matthew+1&version=SBLGNT"
        self.assertTrue(any("verified pinned Greek passage URL changed" in e for e in self.check(baseline=d)))


    def test_revelation_five_loci_claims_keep_edition_speaker_tiers(self) -> None:
        expected={
          "CLM-REV1-8-LORD-GOD-ALPHA":({"ATT-BASE-ALPHA-OMEGA-01","ATT-BASE-PANTOKRATOR-01"},"EXPLICIT_SAME_VERSE"),
          "CLM-REV21-6-THRONE-SPEAKER":({"ATT-BASE-ALPHA-OMEGA-02","ATT-EXT-ARCHE-TELOS-01"},"EXPLICIT_PRIOR_NARRATOR_CUE"),
          "CLM-REV22-13-CHRISTOLOGICAL-INFERENCE":({"ATT-BASE-ALPHA-OMEGA-03","ATT-EXT-ARCHE-TELOS-02"},"CONTEXT_INFERRED_NOT_NAMED_AT_VERSE_13"),
          "CLM-REV1-8-SBL-TR-EXPANSION":({"ATT-BASE-ALPHA-OMEGA-01"},"PRINTED_VARIANT_NOT_NEW_SPEAKER"),
        }
        for cid,(att,tier) in expected.items():
            row=next(x for x in self.claims["records"] if x["claimId"]==cid)
            self.assertEqual(att,set(row["attestationIds"]))
            self.assertEqual(tier,row["speakerEvidenceLevel"])
            self.assertEqual("BLOCKED",row["publicationState"])

    def test_revelation_1_8_cannot_substitute_jesus_as_explicit_name(self) -> None:
        d,o=self.mutate("alpha-omega","baseline",0)
        o["speaker"]="I Jesus in Rev1:8"
        self.assertTrue(any("Revelation speaker evidence conflated" in e for e in self.check(baseline=d)))

    def test_revelation_pantokrator_speech_attribution_cannot_disappear(self) -> None:
        d,o=self.mutate("pantokrator","baseline",0)
        o["speakerEvidence"]="inferred_from_Rev22"
        self.assertTrue(any("Revelation speaker evidence conflated" in e for e in self.check(baseline=d)))

    def test_revelation_21_6_inherited_throne_speaker_not_jesus_direct(self) -> None:
        d,o=self.mutate("alpha-omega","baseline",1)
        o["speakerEvidence"]="explicit I Jesus in Rev21:6"
        self.assertTrue(any("Revelation speaker evidence conflated" in e for e in self.check(baseline=d)))

    def test_revelation_21_6_beginning_end_throne_link_not_lost(self) -> None:
        d,o=self.mutate("arche-telos","extension",0)
        o["speaker"]="speaker inferred contextually"
        self.assertTrue(any("Revelation speaker evidence conflated" in e for e in self.check(extension=d)))

    def test_revelation_22_13_jesus_not_named_directly_in_verse(self) -> None:
        d,o=self.mutate("alpha-omega","baseline",2)
        o["speakerEvidence"]="explicit I Jesus in same verse"
        self.assertTrue(any("Revelation speaker evidence conflated" in e for e in self.check(baseline=d)))

    def test_revelation_22_13_arche_telos_interleaved_voices_not_removed(self) -> None:
        d,o=self.mutate("arche-telos","extension",1)
        o["speakerCue"]="unambiguous single speaker whole book"
        self.assertTrue(any("Revelation speaker evidence conflated" in e for e in self.check(extension=d)))

    def test_revelation_explicit_claim_cannot_become_context_inferred(self) -> None:
        d=copy.deepcopy(self.claims)
        row=next(x for x in d["records"] if x["claimId"]=="CLM-REV1-8-LORD-GOD-ALPHA")
        row["speakerEvidenceLevel"]="CONTEXT_INFERRED_NOT_NAMED_AT_VERSE_13"
        self.assertTrue(any("speaker evidence tier promoted" in e for e in self.check(claims=d)))

    def test_revelation_22_13_claim_must_retain_review_hold(self) -> None:
        d=copy.deepcopy(self.claims)
        row=next(x for x in d["records"] if x["claimId"]=="CLM-REV22-13-CHRISTOLOGICAL-INFERENCE")
        row["requiresIndependentSpeakerReview"]=False
        self.assertTrue(any("speaker evidence tier promoted" in e for e in self.check(claims=d)))

    def test_revelation_21_speaker_claim_cannot_be_deleted(self) -> None:
        d=copy.deepcopy(self.claims)
        d["records"]=[x for x in d["records"] if x["claimId"]!="CLM-REV21-6-THRONE-SPEAKER"]
        self.assertTrue(any("required Revelation speaker/edition claim missing" in e for e in self.check(claims=d)))

    def test_revelation_22_claim_cannot_inherit_revelation_1_witness(self) -> None:
        d=copy.deepcopy(self.claims)
        row=next(x for x in d["records"] if x["claimId"]=="CLM-REV22-13-CHRISTOLOGICAL-INFERENCE")
        row["attestationIds"]=["ATT-BASE-ALPHA-OMEGA-01","ATT-EXT-ARCHE-TELOS-02"]
        self.assertTrue(any("lost its independently reviewed text witnesses" in e for e in self.check(claims=d)))

    def test_revelation_semantic_boundary_cannot_be_renamed_as_identity(self) -> None:
        d=copy.deepcopy(self.claims)
        row=next(x for x in d["semanticRelations"] if x["relationId"]=="REL-REV-21-22-SPEAKER")
        row["relationType"]="CONTRASTS_REFERENT"
        self.assertTrue(any("required semantic boundary" in e for e in self.check(claims=d)))

    def test_revelation_1_8_variant_requires_both_edition_sources(self) -> None:
        d=copy.deepcopy(self.claims)
        row=next(x for x in d["records"] if x["claimId"]=="CLM-REV1-8-SBL-TR-EXPANSION")
        row["sourceIds"]=["SRC-SBLGNT-DIGITAL-NT"]
        self.assertTrue(any("Revelation printed edition comparison lost direct sources" in e for e in self.check(claims=d)))

    def test_revelation_22_commentary_not_silently_unattributed(self) -> None:
        d=copy.deepcopy(self.claims)
        row=next(x for x in d["records"] if x["claimId"]=="CLM-REV22-13-CHRISTOLOGICAL-INFERENCE")
        row["sourceIds"].remove("SRC-TABB-REVELATION22")
        self.assertTrue(any("Revelation 22 speaker commentary attribution lost" in e for e in self.check(claims=d)))

    def test_revelation_pinned_22_sblgnt_url_not_silent_edition_switch(self) -> None:
        d,o=self.mutate("alpha-omega","baseline",2)
        o["sourceUrl"]="https://www.biblegateway.com/passage/?search=Revelation+22&version=TR1550"
        self.assertTrue(any("verified pinned Greek passage URL changed" in e for e in self.check(baseline=d)))


if __name__ == "__main__":
    unittest.main()
