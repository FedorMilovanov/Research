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
          "CLM-REV1-8-LORD-GOD-ALPHA":({"ATT-BASE-ALPHA-OMEGA-01","ATT-BASE-PANTOKRATOR-01","ATT-EXT-HO-ON-ERCHOMENOS-02"},"EXPLICIT_SAME_VERSE"),
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

    def test_eight_lexical_loci_have_six_non_product_claims(self) -> None:
        mapping = {
            "CLM-GEN1-DEUT6-DIVINE-ELOHIM": {"ATT-BASE-ELOHIM-01","ATT-BASE-ELOHIM-03"},
            "CLM-EX20-OTHER-GODS-NEGATIVE": {"ATT-BASE-ELOHIM-02"},
            "CLM-EX34-DEUT32-POSITIVE-EL": {"ATT-BASE-EL-01","ATT-BASE-EL-02"},
            "CLM-DEUT32-12-FOREIGN-EL-NEGATED": {"ATT-BASE-EL-03"},
            "CLM-JUD6-25-BAAL-ALTAR-DISTINCTION": {"ATT-BASE-SHALOM-03"},
            "CLM-GEN35-7-EL-BETHEL-PLACE": {"ATT-BASE-EL-BETHEL-01"},
        }
        for cid,att in mapping.items():
            row=next(x for x in self.claims["records"] if x["claimId"]==cid)
            self.assertEqual(att,set(row["attestationIds"]))
            self.assertEqual("RESEARCH_HOLD",row["editorialState"])
            self.assertEqual("BLOCKED",row["publicationState"])

    def test_elo_him_creator_cannot_be_made_a_plural_creator_subject(self) -> None:
        d,o=self.mutate("elohim","baseline",0)
        o["verbAgreement"]="Qal 3mp plural"
        self.assertTrue(any("lexical referent/named object" in e for e in self.check(baseline=d)))

    def test_elo_him_foreign_gods_cannot_become_yhwh(self) -> None:
        d,o=self.mutate("elohim","baseline",1)
        o["referentClass"]="SINGULAR_CREATOR_GOD"
        o["isDivineDesignation"]=True
        self.assertTrue(any("lexical referent/named object" in e for e in self.check(baseline=d)))

    def test_exodus_20_reversed_numbering_rejected(self) -> None:
        d,o=self.mutate("elohim","baseline",1)
        o["numbering"]["mechonMamreHebrew"]="Exodus 20:3"
        self.assertTrue(any("Hebrew versus common English/Russian numbering lost" in e for e in self.check(baseline=d)))

    def test_exodus_20_verse_label_swap_without_numbering_edit_rejected(self) -> None:
        d,o=self.mutate("elohim","baseline",1)
        o["verse"]="Exodus 20:3 MT"
        self.assertTrue(any("lexical referent/named object" in e for e in self.check(baseline=d)))

    def test_shema_yhwh_identity_not_converted_to_foreign_god(self) -> None:
        d,o=self.mutate("elohim","baseline",2)
        o["contextRole"]="other_gods_prohibited"
        self.assertTrue(any("lexical referent/named object" in e for e in self.check(baseline=d)))

    def test_el_ex34_attributes_not_changed_to_foreign_referent(self) -> None:
        d,o=self.mutate("el","baseline",0)
        o["referentClass"]="OTHER_GOD_NEGATED"
        self.assertTrue(any("lexical referent/named object" in e for e in self.check(baseline=d)))

    def test_el_deut32_positive_not_changed_to_foreign_referent(self) -> None:
        d,o=self.mutate("el","baseline",1)
        o["speechAct"]="negative_foreign_god_contrast"
        self.assertTrue(any("lexical referent/named object" in e for e in self.check(baseline=d)))

    def test_el_deut32_12_negated_foreign_el_not_promoted_to_yhwh(self) -> None:
        d,o=self.mutate("el","baseline",2)
        o["isYHWH"]=True
        o["referentClass"]="YHWH"
        self.assertTrue(any("lexical referent/named object" in e for e in self.check(baseline=d)))

    def test_judges_baal_altar_not_mapped_to_yhwh_shalom_altar(self) -> None:
        d,o=self.mutate("shalom","baseline",2)
        o["namedObject"]="YHWH-shalom altar"
        self.assertTrue(any("lexical referent/named object" in e for e in self.check(baseline=d)))

    def test_gen35_7_place_naming_not_reassigned_to_altar(self) -> None:
        d,o=self.mutate("el-bethel","baseline",0)
        o["namedObject"]="altar"
        self.assertTrue(any("lexical referent/named object" in e for e in self.check(baseline=d)))

    def test_context_claim_cannot_swap_foreign_el_with_yhwh_el(self) -> None:
        d=copy.deepcopy(self.claims)
        row=next(x for x in d["records"] if x["claimId"]=="CLM-DEUT32-12-FOREIGN-EL-NEGATED")
        row["attestationIds"]=["ATT-BASE-EL-02"]
        self.assertTrue(any("lost its independently reviewed text witnesses" in e for e in self.check(claims=d)))

    def test_mandatory_lexical_claim_cannot_be_deleted(self) -> None:
        d=copy.deepcopy(self.claims)
        d["records"]=[x for x in d["records"] if x["claimId"]!="CLM-GEN35-7-EL-BETHEL-PLACE"]
        self.assertTrue(any("required lexical referent or named-object claim missing" in e for e in self.check(claims=d)))

    def test_cross_locus_object_contrast_cannot_collapse_into_same_referent(self) -> None:
        d=copy.deepcopy(self.claims)
        row=next(x for x in d["semanticRelations"] if x["relationId"]=="REL-GIDEON-YHWH-BAAL-ALTAR")
        row["relationType"]="SPECIFIES_SPEECH_AGENT"
        self.assertTrue(any("required semantic boundary" in e for e in self.check(claims=d)))


    def test_five_speech_claims_link_exact_eight_original_attestations(self) -> None:
        mapping={
            "CLM-EX15-26-YHWH-HEALER": {"ATT-BASE-RAPHA-01"},
            "CLM-JER17-14-HEAL-ME-PRAYER": {"ATT-BASE-RAPHA-02"},
            "CLM-EX31-LEV20-YHWH-SANCTIFIES": {"ATT-BASE-MEKODDISHKEM-01","ATT-BASE-MEKODDISHKEM-02"},
            "CLM-PS23-YHWH-MY-SHEPHERD": {"ATT-BASE-RO-I-01"},
            "CLM-JOHN10-JESUS-GOOD-SHEPHERD": {"ATT-BASE-RO-I-02","ATT-EXT-POIMEN-HO-KALOS-01","ATT-EXT-POIMEN-HO-KALOS-02"},
        }
        for cid,att in mapping.items():
            row=next(x for x in self.claims["records"] if x["claimId"]==cid)
            self.assertEqual(att,set(row["attestationIds"]))
            self.assertEqual("RESEARCH_HOLD",row["editorialState"])
            self.assertEqual("BLOCKED",row["publicationState"])

    def test_exodus_healer_divine_speaker_not_changed_to_prophet(self) -> None:
        d,o=self.mutate("rapha","baseline",0)
        o["namingActor"]="Jeremiah"
        self.assertTrue(any("covenant/shepherd speaker morphology" in e for e in self.check(baseline=d)))

    def test_exodus_healer_second_person_singular_not_plural(self) -> None:
        d,o=self.mutate("rapha","baseline",0)
        o["morphology"]="2mp"
        self.assertTrue(any("covenant/shepherd speaker morphology" in e for e in self.check(baseline=d)))

    def test_jeremiah_prayer_not_changed_to_yhwh_predication(self) -> None:
        d,o=self.mutate("rapha","baseline",1)
        o["speechAct"]="divine_self_predication"
        self.assertTrue(any("covenant/shepherd speaker morphology" in e for e in self.check(baseline=d)))

    def test_jeremiah_heal_me_not_participle_your_healer(self) -> None:
        d,o=self.mutate("rapha","baseline",1)
        o["morphology"]="רֹפְאֶךָ 2ms"
        self.assertTrue(any("covenant/shepherd speaker morphology" in e for e in self.check(baseline=d)))

    def test_exodus_sanctification_sabbath_context_not_erased(self) -> None:
        d,o=self.mutate("mekoddishkem","baseline",0)
        o["covenantSetting"]="no historical context"
        self.assertTrue(any("covenant/shepherd speaker morphology" in e for e in self.check(baseline=d)))

    def test_leviticus_sanctifier_plural_not_made_first_person(self) -> None:
        d,o=self.mutate("mekoddishkem","baseline",1)
        o["morphology"]="1cs"
        self.assertTrue(any("covenant/shepherd speaker morphology" in e for e in self.check(baseline=d)))

    def test_psalm_shepherd_not_same_root_as_hagar_el_roi(self) -> None:
        d,o=self.mutate("ro-i","baseline",0)
        o["root"]="ראה"
        self.assertTrue(any("covenant/shepherd speaker morphology" in e for e in self.check(baseline=d)))

    def test_psalm_hebrew_shepherd_not_ascribed_to_jesus_as_speaker(self) -> None:
        d,o=self.mutate("ro-i","baseline",0)
        o["speechAct"]="christological_shepherd_self_description"
        self.assertTrue(any("covenant/shepherd speaker morphology" in e for e in self.check(baseline=d)))

    def test_john10_11_speech_not_made_literal_psalm_hebrew(self) -> None:
        d,o=self.mutate("ro-i","baseline",1)
        o["languageBoundary"]="same Hebrew lexeme"
        self.assertTrue(any("covenant/shepherd speaker morphology" in e for e in self.check(baseline=d)))

    def test_john10_11_explicit_nominal_predicate_not_absolute_ego_eimi(self) -> None:
        d,o=self.mutate("poimen-ho-kalos","extension",0)
        o["syntax"]="ABSOLUTE_EGO_EIMI"
        self.assertTrue(any("covenant/shepherd speaker morphology" in e for e in self.check(extension=d)))

    def test_john10_14_same_predicate_not_removed(self) -> None:
        d,o=self.mutate("poimen-ho-kalos","extension",1)
        o["fullClause"]="ἐγώ εἰμι"
        self.assertTrue(any("covenant/shepherd speaker morphology" in e for e in self.check(extension=d)))

    def test_john10_14_pinned_single_edition_url_not_replaced(self) -> None:
        d,o=self.mutate("poimen-ho-kalos","extension",1)
        o["sourceUrl"]="https://www.biblegateway.com/passage/?search=John+10%3A11&version=SBLGNT"
        self.assertTrue(any("verified pinned Greek passage URL changed" in e for e in self.check(extension=d)))

    def test_healing_prayer_cannot_swap_divine_self_predication_witness(self) -> None:
        d=copy.deepcopy(self.claims)
        r=next(x for x in d["records"] if x["claimId"]=="CLM-JER17-14-HEAL-ME-PRAYER")
        r["attestationIds"]=["ATT-BASE-RAPHA-01"]
        self.assertTrue(any("lost its independently reviewed text witnesses" in e for e in self.check(claims=d)))

    def test_covenant_sanctifier_claim_cannot_silently_disappear(self) -> None:
        d=copy.deepcopy(self.claims)
        d["records"]=[x for x in d["records"] if x["claimId"]!="CLM-EX31-LEV20-YHWH-SANCTIFIES"]
        self.assertTrue(any("required covenant and shepherd speech claims missing" in e for e in self.check(claims=d)))

    def test_psalm_and_john_shepherd_boundary_must_stay_limited(self) -> None:
        d=copy.deepcopy(self.claims)
        r=next(x for x in d["semanticRelations"] if x["relationId"]=="REL-PS23-JOHN10-SHEPHERD-BOUNDARY")
        r["relationType"]="CONTRASTS_REFERENT"
        self.assertTrue(any("required semantic boundary" in e for e in self.check(claims=d)))

    def test_healer_and_sanctifier_suffix_boundary_must_stay_typed(self) -> None:
        d=copy.deepcopy(self.claims)
        r=next(x for x in d["semanticRelations"] if x["relationId"]=="REL-YHWH-SANCTIFY-HEAL-SUFFIX")
        r["relationType"]="CONTRASTS_NAMED_OBJECT"
        self.assertTrue(any("required semantic boundary" in e for e in self.check(claims=d)))


    def test_john6_18_claims_link_exact_source_loci(self) -> None:
        expected = {
            "CLM-JOHN6-20-ASSURANCE": "ATT-BASE-EGO-EIMI-01",
            "CLM-JOHN18-5-ARREST-IDENTITY": "ATT-BASE-EGO-EIMI-04",
            "CLM-JOHN18-6-NARRATOR-REPRISE": "ATT-BASE-EGO-EIMI-05",
            "CLM-JOHN18-8-IDENTITY-AND-RELEASE": "ATT-BASE-EGO-EIMI-06",
        }
        for cid, aid in expected.items():
            item = next(c for c in self.claims["records"] if c["claimId"] == cid)
            self.assertEqual([aid], item["attestationIds"])
            self.assertEqual("RESEARCH_HOLD", item["editorialState"])
            self.assertEqual("BLOCKED", item["publicationState"])

    def test_john6_20_jesus_not_reclassified_as_human_healed(self) -> None:
        d,obs=self.mutate("ego-eimi","baseline",0)
        obs["speaker"]="formerly blind man"
        self.assertTrue(any("John6/18 speaker/discourse control changed" in e for e in self.check(baseline=d)))

    def test_john6_20_assurance_not_promoted_to_inherent_divine_lexeme(self) -> None:
        d,obs=self.mutate("ego-eimi","baseline",0)
        obs["divineNameClaim"]="INHERENT_UNIQUE_PROPER_NAME"
        self.assertTrue(any("John6/18 speaker/discourse control changed" in e for e in self.check(baseline=d)))

    def test_john6_20_disciples_not_replaced_by_arrest_party(self) -> None:
        d,obs=self.mutate("ego-eimi","baseline",0)
        obs["speechTarget"]="arresting party"
        self.assertTrue(any("John6/18 speaker/discourse control changed" in e for e in self.check(baseline=d)))

    def test_john6_20_single_edition_url_stays_fixed(self) -> None:
        d,obs=self.mutate("ego-eimi","baseline",0)
        obs["sourceUrl"]="https://www.biblegateway.com/passage/?search=John+6&version=SBLGNT"
        self.assertTrue(any("verified pinned Greek passage URL changed" in e for e in self.check(baseline=d)))

    def test_john18_5_explicit_nazarene_question_not_erased(self) -> None:
        d,obs=self.mutate("ego-eimi","baseline",3)
        obs["claimScope"]="God announces unique name"
        self.assertTrue(any("John6/18 speaker/discourse control changed" in e for e in self.check(baseline=d)))

    def test_john18_5_identity_answer_not_changed_to_absolute_divine_naming(self) -> None:
        d,obs=self.mutate("ego-eimi","baseline",3)
        obs["speechAct"]="absolute_divine_proper_name"
        self.assertTrue(any("John6/18 speaker/discourse control changed" in e for e in self.check(baseline=d)))

    def test_john18_6_narrator_reprise_is_not_a_second_new_utterance(self) -> None:
        d,obs=self.mutate("ego-eimi","baseline",4)
        obs["speechAct"]="new_independent_utterance"
        self.assertTrue(any("John6/18 speaker/discourse control changed" in e for e in self.check(baseline=d)))

    def test_john18_6_falling_not_deleted_or_turned_into_unproved_mechanism(self) -> None:
        d,obs=self.mutate("ego-eimi","baseline",4)
        obs["claimScope"]="divine force literally pushes people backwards"
        self.assertTrue(any("John6/18 speaker/discourse control changed" in e for e in self.check(baseline=d)))

    def test_john18_6_narrative_attribution_not_direct_jesus_new_speech(self) -> None:
        d,obs=self.mutate("ego-eimi","baseline",4)
        obs["speaker"]="Jesus"
        self.assertTrue(any("John6/18 speaker/discourse control changed" in e for e in self.check(baseline=d)))

    def test_john18_8_release_request_not_lost(self) -> None:
        d,obs=self.mutate("ego-eimi","baseline",5)
        obs["claimScope"]="only a name revelation"
        self.assertTrue(any("John6/18 speaker/discourse control changed" in e for e in self.check(baseline=d)))

    def test_john18_8_edition_url_not_switched_to_other_publisher(self) -> None:
        d,obs=self.mutate("ego-eimi","baseline",5)
        obs["sourceUrl"]="https://www.biblegateway.com/passage/?search=John+18&version=KJV"
        self.assertTrue(any("verified pinned Greek passage URL changed" in e for e in self.check(baseline=d)))

    def test_john18_reprise_claim_witness_cannot_swap_to_new_speech(self) -> None:
        d=copy.deepcopy(self.claims)
        row=next(x for x in d["records"] if x["claimId"]=="CLM-JOHN18-6-NARRATOR-REPRISE")
        row["attestationIds"]=["ATT-BASE-EGO-EIMI-06"]
        self.assertTrue(any("lost its independently reviewed text witnesses" in e for e in self.check(claims=d)))

    def test_john6_speech_claim_required(self) -> None:
        d=copy.deepcopy(self.claims)
        d["records"]=[x for x in d["records"] if x["claimId"]!="CLM-JOHN6-20-ASSURANCE"]
        self.assertTrue(any("required John6/18 discourse claims missing" in e for e in self.check(claims=d)))

    def test_john18_narrator_vs_direct_semantic_relation_required(self) -> None:
        d=copy.deepcopy(self.claims)
        row=next(x for x in d["semanticRelations"] if x["relationId"]=="REL-JOHN18-6-8-AGENCY")
        row["relationType"]="CONTRASTS_NAMED_OBJECT"
        self.assertTrue(any("required semantic boundary" in e for e in self.check(claims=d)))


    def test_yireh_nissi_claims_cover_four_previous_unlinked_loci(self) -> None:
        targets = {
            "CLM-GEN22-8-ABRAHAM-PROVISION-ANSWER":"ATT-BASE-YIREH-01",
            "CLM-GEN22-14-MOUNTAIN-NIPHAL":"ATT-BASE-YIREH-03",
            "CLM-EX17-16-MT-HAND-THRONE-CRUX":"ATT-BASE-NISSI-03",
            "CLM-EX17-16-LXX-HIDDEN-HAND":"ATT-BASE-NISSI-04",
        }
        for cid, aid in targets.items():
            row=next(c for c in self.claims["records"] if c["claimId"]==cid)
            self.assertEqual([aid],row["attestationIds"])
            self.assertEqual("RESEARCH_HOLD",row["editorialState"])
            self.assertEqual("BLOCKED",row["publicationState"])

    def test_gen22_8_abraham_not_replaced_by_yhwh_divine_self_naming(self) -> None:
        d,o=self.mutate("yireh","baseline",0)
        o["namingActor"]="YHWH, direct divine self naming"
        self.assertTrue(any("Gen22/Ex17 Hebrew or LXX locus text/role guard" in e for e in self.check(baseline=d)))

    def test_gen22_8_not_silent_place_naming(self) -> None:
        d,o=self.mutate("yireh","baseline",0)
        o["namedObject"]="place"
        self.assertTrue(any("Gen22/Ex17 Hebrew or LXX locus text/role guard" in e for e in self.check(baseline=d)))

    def test_gen22_8_morphology_not_niphal_from_proverb(self) -> None:
        d,o=self.mutate("yireh","baseline",0)
        o["morphology"]="יֵרָאֶה Niphal yiqtol 3ms (secondary preliminary)"
        self.assertTrue(any("Gen22/Ex17 Hebrew or LXX locus text/role guard" in e for e in self.check(baseline=d)))

    def test_gen22_8_speech_target_is_isaac(self) -> None:
        d,o=self.mutate("yireh","baseline",0)
        o["directAddress"]="Abraham to an altar"
        self.assertTrue(any("Gen22/Ex17 Hebrew or LXX locus text/role guard" in e for e in self.check(baseline=d)))

    def test_gen22_14_mountain_niphal_not_qal_place_name(self) -> None:
        d,o=self.mutate("yireh","baseline",2)
        o["surface"]="יְהוָה יִרְאֶה"
        self.assertTrue(any("Gen22/Ex17 Hebrew or LXX locus text/role guard" in e for e in self.check(baseline=d)))

    def test_gen22_14_community_proverb_not_new_abraham_naming(self) -> None:
        d,o=self.mutate("yireh","baseline",2)
        o["namingActor"]="Abraham"
        self.assertTrue(any("Gen22/Ex17 Hebrew or LXX locus text/role guard" in e for e in self.check(baseline=d)))

    def test_gen22_14_niphal_translation_alternatives_preserved(self) -> None:
        d,o=self.mutate("yireh","baseline",2)
        o["translationScope"]="always only YHWH will provide"
        self.assertTrue(any("Gen22/Ex17 Hebrew or LXX locus text/role guard" in e for e in self.check(baseline=d)))

    def test_gen22_mountain_does_not_lose_attributed_NET_review(self) -> None:
        d=copy.deepcopy(self.claims)
        row=next(c for c in d["records"] if c["claimId"]=="CLM-GEN22-14-MOUNTAIN-NIPHAL")
        row["sourceIds"]=["SRC-MT-MECHON"]
        self.assertTrue(any("Hebrew/Greek or NET attributed source triangle lost" in e for e in self.check(claims=d)))

    def test_ex17_16_mt_throne_not_conjectural_banner(self) -> None:
        d,o=self.mutate("nissi","baseline",2)
        o["surface"]="כִּי-יָד עַל-נֵס יָהּ"
        self.assertTrue(any("Gen22/Ex17 Hebrew or LXX locus text/role guard" in e for e in self.check(baseline=d)))

    def test_ex17_16_mt_conjecture_not_promoted_to_attested_reading(self) -> None:
        d,o=self.mutate("nissi","baseline",2)
        o["textualStatus"]="N_ES_ATTESTED_AS_MT"
        self.assertTrue(any("Gen22/Ex17 Hebrew or LXX locus text/role guard" in e for e in self.check(baseline=d)))

    def test_ex17_16_mt_readings_under_debate_not_silently_deleted(self) -> None:
        d,o=self.mutate("nissi","baseline",2)
        o["readingsUnderDebate"]=["banner נֵס is certain"]
        self.assertTrue(any("Gen22/Ex17 Hebrew or LXX locus text/role guard" in e for e in self.check(baseline=d)))

    def test_ex17_16_lxx_secret_hand_not_replaced_by_hebrew_throne(self) -> None:
        d,o=self.mutate("nissi","baseline",3)
        o["surface"]="כִּי-יָד עַל-כֵּס יָהּ"
        self.assertTrue(any("Gen22/Ex17 Hebrew or LXX locus text/role guard" in e for e in self.check(baseline=d)))

    def test_ex17_16_lxx_labeled_not_literal_to_mt(self) -> None:
        d,o=self.mutate("nissi","baseline",3)
        o["textualStatus"]="DIRECT_LITERAL_TRANSLATION_MT_HAND_THRONE"
        self.assertTrue(any("Gen22/Ex17 Hebrew or LXX locus text/role guard" in e for e in self.check(baseline=d)))

    def test_ex17_16_lxx_publisher_source_cannot_switch(self) -> None:
        d,o=self.mutate("nissi","baseline",3)
        o["sourceUrl"]="https://mechon-mamre.org/p/pt/pt0217.htm"
        self.assertTrue(any("Gen22/Ex17 Hebrew or LXX locus text/role guard" in e for e in self.check(baseline=d)))

    def test_ex17_16_hypothesis_not_allowed_without_translator_note(self) -> None:
        d=copy.deepcopy(self.claims)
        row=next(c for c in d["records"] if c["claimId"]=="CLM-EX17-16-MT-HAND-THRONE-CRUX")
        row["sourceIds"]=["SRC-MT-MECHON"]
        self.assertTrue(any("Hebrew/Greek or NET attributed source triangle lost" in e for e in self.check(claims=d)))

    def test_ex17_16_claim_cannot_inherit_altar_named_observation(self) -> None:
        d=copy.deepcopy(self.claims)
        row=next(c for c in d["records"] if c["claimId"]=="CLM-EX17-16-LXX-HIDDEN-HAND")
        row["attestationIds"]=["ATT-BASE-NISSI-02"]
        self.assertTrue(any("lost its independently reviewed text witnesses" in e for e in self.check(claims=d)))

    def test_gen22_niphal_claim_cannot_be_removed(self) -> None:
        d=copy.deepcopy(self.claims)
        d["records"]=[c for c in d["records"] if c["claimId"]!="CLM-GEN22-14-MOUNTAIN-NIPHAL"]
        self.assertTrue(any("required Yireh/Nissi name-versus-explanation claims missing" in e for e in self.check(claims=d)))

    def test_ex17_16_mt_lxx_relation_type_not_turned_into_equivalence(self) -> None:
        d=copy.deepcopy(self.claims)
        row=next(c for c in d["semanticRelations"] if c["relationId"]=="REL-EX17-MT-LXX-SECRET-HAND")
        row["relationType"]="CONTRASTS_REFERENT"
        self.assertTrue(any("required semantic boundary" in e for e in self.check(claims=d)))

    def test_shaddai_gen17_speaker_cannot_be_isaac(self) -> None:
        d,o=self.mutate("el-shaddai","baseline",0)
        o["speaker"]="Isaac"
        self.assertTrue(any("Shaddai/Sabaoth speaker and printed surface guard changed" in e for e in self.check(baseline=d)))

    def test_shaddai_gen17_self_speech_cannot_be_blessing(self) -> None:
        d,o=self.mutate("el-shaddai","baseline",0)
        o["speechAct"]="benediction"
        self.assertTrue(any("Shaddai/Sabaoth speaker and printed surface guard changed" in e for e in self.check(baseline=d)))

    def test_shaddai_gen28_benediction_speaker_cannot_be_yhwh(self) -> None:
        d,o=self.mutate("el-shaddai","baseline",1)
        o["speaker"]="YHWH"
        self.assertTrue(any("Shaddai/Sabaoth speaker and printed surface guard changed" in e for e in self.check(baseline=d)))

    def test_shaddai_gen28_original_prefix_must_remain(self) -> None:
        d,o=self.mutate("el-shaddai","baseline",1)
        o["surface"]="אֵל שַׁדַּי"
        self.assertTrue(any("Shaddai/Sabaoth speaker and printed surface guard changed" in e for e in self.check(baseline=d)))

    def test_shaddai_gen35_god_not_isaac(self) -> None:
        d,o=self.mutate("el-shaddai","baseline",2)
        o["speaker"]="Isaac"
        self.assertTrue(any("Shaddai/Sabaoth speaker and printed surface guard changed" in e for e in self.check(baseline=d)))

    def test_shaddai_gen35_self_speech_not_place_naming(self) -> None:
        d,o=self.mutate("el-shaddai","baseline",2)
        o["speechAct"]="place_naming"
        self.assertTrue(any("Shaddai/Sabaoth speaker and printed surface guard changed" in e for e in self.check(baseline=d)))

    def test_shaddai_ex6_vowel_written_form_not_normalized(self) -> None:
        d,o=self.mutate("el-shaddai","baseline",3)
        o["surface"]="בְּאֵל שַׁדַּי"
        self.assertTrue(any("Shaddai/Sabaoth speaker and printed surface guard changed" in e for e in self.check(baseline=d)))

    def test_shaddai_ex6_speaker_is_not_moses(self) -> None:
        d,o=self.mutate("el-shaddai","baseline",3)
        o["speaker"]="Moses"
        self.assertTrue(any("Shaddai/Sabaoth speaker and printed surface guard changed" in e for e in self.check(baseline=d)))

    def test_shaddai_ex6_retrospective_is_not_benediction(self) -> None:
        d,o=self.mutate("el-shaddai","baseline",3)
        o["speechAct"]="benediction"
        self.assertTrue(any("Shaddai/Sabaoth speaker and printed surface guard changed" in e for e in self.check(baseline=d)))

    def test_sabaoth_1sam1_worship_preposition_locked(self) -> None:
        d,o=self.mutate("sabaoth","baseline",0)
        o["originalPrefix"]="none"
        self.assertTrue(any("Shaddai/Sabaoth speaker and printed surface guard changed" in e for e in self.check(baseline=d)))

    def test_sabaoth_1sam1_narrator_not_direct_yhwh_speech(self) -> None:
        d,o=self.mutate("sabaoth","baseline",0)
        o["speaker"]="YHWH"
        self.assertTrue(any("Shaddai/Sabaoth speaker and printed surface guard changed" in e for e in self.check(baseline=d)))

    def test_sabaoth_1sam1_source_not_switched_to_sam17(self) -> None:
        d,o=self.mutate("sabaoth","baseline",0)
        o["sourceUrl"]="https://mechon-mamre.org/p/pt/pt08a17.htm"
        self.assertTrue(any("Shaddai/Sabaoth speaker and printed surface guard changed" in e for e in self.check(baseline=d)))

    def test_sabaoth_david_speech_not_angelic(self) -> None:
        d,o=self.mutate("sabaoth","baseline",1)
        o["speaker"]="seraphim addressing each other"
        self.assertTrue(any("Shaddai/Sabaoth speaker and printed surface guard changed" in e for e in self.check(baseline=d)))

    def test_sabaoth_david_military_context_must_stay(self) -> None:
        d,o=self.mutate("sabaoth","baseline",1)
        o["contextClause"]="only angelic forces"
        self.assertTrue(any("Shaddai/Sabaoth speaker and printed surface guard changed" in e for e in self.check(baseline=d)))

    def test_sabaoth_isaiah_seraphim_not_isaiah(self) -> None:
        d,o=self.mutate("sabaoth","baseline",2)
        o["speaker"]="Isaiah"
        self.assertTrue(any("Shaddai/Sabaoth speaker and printed surface guard changed" in e for e in self.check(baseline=d)))

    def test_sabaoth_isaiah_hymn_not_david_invocation(self) -> None:
        d,o=self.mutate("sabaoth","baseline",2)
        o["contextRole"]="warrior_invocation"
        self.assertTrue(any("Shaddai/Sabaoth speaker and printed surface guard changed" in e for e in self.check(baseline=d)))

    def test_sabaoth_zechariah_mixed_voice_not_only_divine_i(self) -> None:
        d,o=self.mutate("sabaoth","baseline",3)
        o["speaker"]="YHWH direct only"
        self.assertTrue(any("Shaddai/Sabaoth speaker and printed surface guard changed" in e for e in self.check(baseline=d)))

    def test_sabaoth_zechariah_third_person_flock_fixed(self) -> None:
        d,o=self.mutate("sabaoth","baseline",3)
        o["referent"]="unknown human general"
        self.assertTrue(any("Shaddai/Sabaoth speaker and printed surface guard changed" in e for e in self.check(baseline=d)))


    def test_shaddai_sabaoth_claim_seven_ids_cover_eight_attestations(self) -> None:
        exp={
            "CLM-ELSHADDAI-GEN17-35-DIVINE-SELF":{"ATT-BASE-EL-SHADDAI-01","ATT-BASE-EL-SHADDAI-03"},
            "CLM-ELSHADDAI-GEN28-ISAAC-BLESSING":{"ATT-BASE-EL-SHADDAI-02"},
            "CLM-ELSHADDAI-EX6-RETROSPECTIVE-REVELATION":{"ATT-BASE-EL-SHADDAI-04"},
            "CLM-SABAOTH-1SAM1-3-NARRATOR-WORSHIP":{"ATT-BASE-SABAOTH-01"},
            "CLM-SABAOTH-1SAM17-45-DAVID-BATTLE":{"ATT-BASE-SABAOTH-02"},
            "CLM-SABAOTH-ISA6-3-SERAPHIM-HYMN":{"ATT-BASE-SABAOTH-03"},
            "CLM-SABAOTH-ZECH10-3-PROPHETIC-VOICE":{"ATT-BASE-SABAOTH-04"},
        }
        for cid,att in exp.items():
            item=next(x for x in self.claims["records"] if x["claimId"]==cid)
            self.assertEqual(att,set(item["attestationIds"]))
            self.assertEqual("RESEARCH_HOLD",item["editorialState"])
            self.assertEqual("BLOCKED",item["publicationState"])

    def test_shaddai_ex6_uncertain_etymology_not_promoted_to_certainty(self) -> None:
        d=copy.deepcopy(self.claims)
        item=next(x for x in d["records"] if x["claimId"]=="CLM-ELSHADDAI-EX6-RETROSPECTIVE-REVELATION")
        item["etymologyStatus"]="CERTAIN_MOUNTAIN"
        self.assertTrue(any("unresolved Shaddai Exodus6 hypothesis guard changed" in e for e in self.check(claims=d)))

    def test_shaddai_ex6_revelation_controversy_not_resolved_by_fiat(self) -> None:
        d=copy.deepcopy(self.claims)
        item=next(x for x in d["records"] if x["claimId"]=="CLM-ELSHADDAI-EX6-RETROSPECTIVE-REVELATION")
        item["revelationInterpretationStatus"]="SCHOLARLY_CONSENSUS"
        self.assertTrue(any("unresolved Shaddai Exodus6 hypothesis guard changed" in e for e in self.check(claims=d)))

    def test_shaddai_ex6_net_notes_must_remain_attributed(self) -> None:
        d=copy.deepcopy(self.claims)
        item=next(x for x in d["records"] if x["claimId"]=="CLM-ELSHADDAI-EX6-RETROSPECTIVE-REVELATION")
        item["sourceIds"]=["SRC-MT-MECHON"]
        self.assertTrue(any("NET Exodus6 attributed notes and MT source pairing lost" in e for e in self.check(claims=d)))

    def test_shaddai_isaac_blessing_claim_required(self) -> None:
        d=copy.deepcopy(self.claims)
        d["records"]=[x for x in d["records"] if x["claimId"]!="CLM-ELSHADDAI-GEN28-ISAAC-BLESSING"]
        self.assertTrue(any("required Shaddai/Sabaoth speaker claims missing" in e for e in self.check(claims=d)))

    def test_sabaoth_isaiah6_not_roman9_direct_quote(self) -> None:
        d=copy.deepcopy(self.claims)
        item=next(x for x in d["semanticRelations"] if x["relationId"]=="REL-SABAOTH-ISA6-ROM9-QUOTE")
        item["relationType"]="CONTRASTS_REFERENT"
        self.assertTrue(any("required semantic boundary" in e for e in self.check(claims=d)))

    def test_elyon_narrator_not_melchizedek_speaker(self) -> None:
        d,o=self.mutate("el-elyon","baseline",0)
        o["speaker"]="Melchizedek"
        self.assertTrue(any("Elyon/Qanna actor/name/MT printed locus changed" in e for e in self.check(baseline=d)))

    def test_elyon_gen14_18_priest_not_oath(self) -> None:
        d,o=self.mutate("el-elyon","baseline",0)
        o["speechAct"]="oath_invocation"
        self.assertTrue(any("Elyon/Qanna actor/name/MT printed locus changed" in e for e in self.check(baseline=d)))

    def test_elyon_gen14_18_lamed_not_lost(self) -> None:
        d,o=self.mutate("el-elyon","baseline",0)
        o["surface"]="אֵל עֶלְיוֹן"
        self.assertTrue(any("Elyon/Qanna actor/name/MT printed locus changed" in e for e in self.check(baseline=d)))

    def test_elyon_gen14_19_melchizedek_not_abram(self) -> None:
        d,o=self.mutate("el-elyon","baseline",1)
        o["speaker"]="Abram"
        self.assertTrue(any("Elyon/Qanna actor/name/MT printed locus changed" in e for e in self.check(baseline=d)))

    def test_elyon_gen14_19_blessing_not_doxology(self) -> None:
        d,o=self.mutate("el-elyon","baseline",1)
        o["speechAct"]="doxology"
        self.assertTrue(any("Elyon/Qanna actor/name/MT printed locus changed" in e for e in self.check(baseline=d)))

    def test_elyon_gen14_20_doxology_not_blessing(self) -> None:
        d,o=self.mutate("el-elyon","baseline",2)
        o["speechAct"]="blessing"
        self.assertTrue(any("Elyon/Qanna actor/name/MT printed locus changed" in e for e in self.check(baseline=d)))

    def test_elyon_gen14_20_unprefixed_form_protected(self) -> None:
        d,o=self.mutate("el-elyon","baseline",2)
        o["surface"]="לְאֵל עֶלְיוֹן"
        self.assertTrue(any("Elyon/Qanna actor/name/MT printed locus changed" in e for e in self.check(baseline=d)))

    def test_elyon_gen14_22_abram_oath_speaker(self) -> None:
        d,o=self.mutate("el-elyon","baseline",3)
        o["speaker"]="Melchizedek"
        self.assertTrue(any("Elyon/Qanna actor/name/MT printed locus changed" in e for e in self.check(baseline=d)))

    def test_elyon_gen14_22_yhwh_explicit_mt_not_silent(self) -> None:
        d,o=self.mutate("el-elyon","baseline",3)
        o["surface"]="אֵל עֶלְיוֹן"
        self.assertTrue(any("Elyon/Qanna actor/name/MT printed locus changed" in e for e in self.check(baseline=d)))

    def test_qanna_ex34_name_clause_protected(self) -> None:
        d,o=self.mutate("el-qanna","baseline",0)
        o["nameClause"]="none"
        self.assertTrue(any("Elyon/Qanna actor/name/MT printed locus changed" in e for e in self.check(baseline=d)))

    def test_qanna_ex34_other_god_not_yhwh(self) -> None:
        d,o=self.mutate("el-qanna","baseline",0)
        o["contrast"]="לְאֵל קַנָּא"
        self.assertTrue(any("Elyon/Qanna actor/name/MT printed locus changed" in e for e in self.check(baseline=d)))

    def test_qanna_ex34_speaker_not_moses(self) -> None:
        d,o=self.mutate("el-qanna","baseline",0)
        o["speaker"]="Moses warning Israel"
        self.assertTrue(any("Elyon/Qanna actor/name/MT printed locus changed" in e for e in self.check(baseline=d)))

    def test_qanna_deut4_moses_not_yhwh(self) -> None:
        d,o=self.mutate("el-qanna","baseline",1)
        o["speaker"]="YHWH"
        self.assertTrue(any("Elyon/Qanna actor/name/MT printed locus changed" in e for e in self.check(baseline=d)))

    def test_qanna_deut4_no_name_statement(self) -> None:
        d,o=self.mutate("el-qanna","baseline",1)
        o["selfNamingInVerse"]=True
        self.assertTrue(any("Elyon/Qanna actor/name/MT printed locus changed" in e for e in self.check(baseline=d)))

    def test_qanna_deut4_fiery_descriptor_not_exodus_syntax(self) -> None:
        d,o=self.mutate("el-qanna","baseline",1)
        o["surface"]="קַנָּא שְׁמוֹ"
        self.assertTrue(any("Elyon/Qanna actor/name/MT printed locus changed" in e for e in self.check(baseline=d)))

    def test_elyon_qanna_five_claims_cover_six_printed_attestations(self) -> None:
        expected = {
            "CLM-ELYON-GEN14-18-PRIEST-NARRATOR":{"ATT-BASE-EL-ELYON-01"},
            "CLM-ELYON-GEN14-19-20-PRIEST-BLESS-DOXOLOGY":{"ATT-BASE-EL-ELYON-02","ATT-BASE-EL-ELYON-03"},
            "CLM-ELYON-GEN14-22-ABRAM-YHWH-OATH":{"ATT-BASE-EL-ELYON-04"},
            "CLM-QANNA-EX34-14-NAME-CHARACTER":{"ATT-BASE-EL-QANNA-01"},
            "CLM-QANNA-DEUT4-24-MOSES-WARNING":{"ATT-BASE-EL-QANNA-02"},
        }
        for cid, att in expected.items():
            row=next(r for r in self.claims["records"] if r["claimId"]==cid)
            self.assertEqual(att,set(row["attestationIds"]))
            self.assertEqual("RESEARCH_HOLD",row["editorialState"])
            self.assertEqual("BLOCKED",row["publicationState"])

    def test_elyon_gen14_22_cargill_gloss_not_upgraded_to_verified_variant(self) -> None:
        d=copy.deepcopy(self.claims)
        row=next(r for r in d["records"] if r["claimId"]=="CLM-ELYON-GEN14-22-ABRAM-YHWH-OATH")
        row["historicalHypothesisStatus"]="MANUSCRIPT_OMISSION_PROVED"
        self.assertTrue(any("Elyon/Qanna cautious attribution and name evidence lost" in e for e in self.check(claims=d)))

    def test_elyon_gen14_22_cargill_secondary_source_cannot_be_dropped(self) -> None:
        d=copy.deepcopy(self.claims)
        row=next(r for r in d["records"] if r["claimId"]=="CLM-ELYON-GEN14-22-ABRAM-YHWH-OATH")
        row["sourceIds"]=["SRC-MT-MECHON","SRC-NET-GEN14"]
        self.assertTrue(any("NET / Cargill attribution source link lost" in e for e in self.check(claims=d)))

    def test_elyon_creator_possessor_lexical_alternatives_still_visible(self) -> None:
        d=copy.deepcopy(self.claims)
        row=next(r for r in d["records"] if r["claimId"]=="CLM-ELYON-GEN14-19-20-PRIEST-BLESS-DOXOLOGY")
        row["creatorPossessorStatus"]="CREATOR_ONLY_CERTAIN"
        self.assertTrue(any("Elyon/Qanna cautious attribution and name evidence lost" in e for e in self.check(claims=d)))

    def test_qanna_deut4_cannot_be_promoted_to_explicit_name_clause(self) -> None:
        d=copy.deepcopy(self.claims)
        row=next(r for r in d["records"] if r["claimId"]=="CLM-QANNA-DEUT4-24-MOSES-WARNING")
        row["nameEvidenceStatus"]="EXPLICIT_NAME_CLAUSE_CHARACTER_EPITHET"
        self.assertTrue(any("Elyon/Qanna cautious attribution and name evidence lost" in e for e in self.check(claims=d)))

    def test_qanna_ex34_explicit_name_clause_claim_required(self) -> None:
        d=copy.deepcopy(self.claims)
        d["records"]=[r for r in d["records"] if r["claimId"]!="CLM-QANNA-EX34-14-NAME-CHARACTER"]
        self.assertTrue(any("required Elyon/Qanna speech/name claims missing" in e for e in self.check(claims=d)))

    def test_elyon_melchizedek_abram_edge_must_distinguish_speakers(self) -> None:
        d=copy.deepcopy(self.claims)
        row=next(r for r in d["semanticRelations"] if r["relationId"]=="REL-ELYON-MELCHIZEDEK-ABRAM")
        row["relationType"]="CONTRASTS_REFERENT"
        self.assertTrue(any("required semantic boundary" in e for e in self.check(claims=d)))

    def test_dan7_9_absolute_form_not_emphatic(self) -> None:
        d,o=self.mutate("atiq-yomin","baseline",0)
        o["surface"]="עַתִּיק יוֹמַיָּא"
        self.assertTrue(any("Daniel7/Revelation Greek or Aramaic context control changed" in e for e in self.check(baseline=d)))

    def test_dan7_9_vision_speaker_not_ancient_self(self) -> None:
        d,o=self.mutate("atiq-yomin","baseline",0)
        o["speaker"]="Ancient of Days speaks directly"
        self.assertTrue(any("Daniel7/Revelation Greek or Aramaic context control changed" in e for e in self.check(baseline=d)))

    def test_dan7_9_sitting_judge_referent(self) -> None:
        d,o=self.mutate("atiq-yomin","baseline",0)
        o["referent"]="son of man approaching"
        self.assertTrue(any("Daniel7/Revelation Greek or Aramaic context control changed" in e for e in self.check(baseline=d)))

    def test_dan7_13_emphatic_form_not_absolute(self) -> None:
        d,o=self.mutate("atiq-yomin","baseline",1)
        o["surface"]="עַתִּיק יוֹמִין"
        self.assertTrue(any("Daniel7/Revelation Greek or Aramaic context control changed" in e for e in self.check(baseline=d)))

    def test_dan7_13_ancient_not_same_as_approaching_figure(self) -> None:
        d,o=self.mutate("atiq-yomin","baseline",1)
        o["referent"]="approaching son of man is Ancient of Days"
        self.assertTrue(any("Daniel7/Revelation Greek or Aramaic context control changed" in e for e in self.check(baseline=d)))

    def test_dan7_13_speaker_is_daniel_vision(self) -> None:
        d,o=self.mutate("atiq-yomin","baseline",1)
        o["speaker"]="an angel speaks in direct address"
        self.assertTrue(any("Daniel7/Revelation Greek or Aramaic context control changed" in e for e in self.check(baseline=d)))

    def test_dan7_22_ancient_judgment_not_sonman_approach(self) -> None:
        d,o=self.mutate("atiq-yomin","baseline",2)
        o["referent"]="Ancient approached by son of man"
        self.assertTrue(any("Daniel7/Revelation Greek or Aramaic context control changed" in e for e in self.check(baseline=d)))

    def test_dan7_22_different_verse_must_remain(self) -> None:
        d,o=self.mutate("atiq-yomin","baseline",2)
        o["verse"]="Daniel 7:13"
        self.assertTrue(any("Daniel7/Revelation Greek or Aramaic context control changed" in e for e in self.check(baseline=d)))

    def test_rev1_4_formula_is_greeting_not_christ_direct_speech(self) -> None:
        d,o=self.mutate("ho-on-erchomenos","extension",0)
        o["speakerCue"]="Jesus explicitly says I am"
        self.assertTrue(any("Daniel7/Revelation Greek or Aramaic context control changed" in e for e in self.check(extension=d)))

    def test_rev1_4_formula_exact_sblgnt_preserved(self) -> None:
        d,o=self.mutate("ho-on-erchomenos","extension",0)
        o["surface"]="ὁ ὤν"
        self.assertTrue(any("Daniel7/Revelation Greek or Aramaic context control changed" in e for e in self.check(extension=d)))

    def test_rev1_4_source_cannot_change_edition(self) -> None:
        d,o=self.mutate("ho-on-erchomenos","extension",0)
        o["sourceUrl"]="https://www.biblegateway.com/passage/?search=Revelation+1%3A4-8&version=KJV"
        self.assertTrue(any("Daniel7/Revelation Greek or Aramaic context control changed" in e for e in self.check(extension=d)))

    def test_rev1_8_explicit_lord_god_speaker(self) -> None:
        d,o=self.mutate("ho-on-erchomenos","extension",1)
        o["speaker"]="John addressing churches"
        self.assertTrue(any("Daniel7/Revelation Greek or Aramaic context control changed" in e for e in self.check(extension=d)))

    def test_rev1_8_explicit_speaker_cue_locked(self) -> None:
        d,o=self.mutate("ho-on-erchomenos","extension",1)
        o["speakerCue"]="John's greeting distinguishes three ἀπό sources"
        self.assertTrue(any("Daniel7/Revelation Greek or Aramaic context control changed" in e for e in self.check(extension=d)))

    def test_rev1_8_formula_same_printed_surface(self) -> None:
        d,o=self.mutate("ho-on-erchomenos","extension",1)
        o["surface"]="ἐγώ εἰμι ὁ ὤν"
        self.assertTrue(any("Daniel7/Revelation Greek or Aramaic context control changed" in e for e in self.check(extension=d)))

    def test_rev21_22_john_narration_not_lord_god_direct_speech(self) -> None:
        d,o=self.mutate("pantokrator","baseline",1)
        o["speaker"]="κύριος, ὁ θεός (Lord God)"
        self.assertTrue(any("Daniel7/Revelation Greek or Aramaic context control changed" in e for e in self.check(baseline=d)))

    def test_rev21_22_lamb_referent_preserved(self) -> None:
        d,o=self.mutate("pantokrator","baseline",1)
        o["referent"]="God and Lamb same grammatical noun"
        self.assertTrue(any("Daniel7/Revelation Greek or Aramaic context control changed" in e for e in self.check(baseline=d)))

    def test_rev21_22_separate_verse_not_rev1_8(self) -> None:
        d,o=self.mutate("pantokrator","baseline",1)
        o["verse"]="Revelation 1:8"
        self.assertTrue(any("Daniel7/Revelation Greek or Aramaic context control changed" in e for e in self.check(baseline=d)))

    def test_rev21_22_edition_pin_exact_chapter(self) -> None:
        d,o=self.mutate("pantokrator","baseline",1)
        o["sourceUrl"]="https://www.biblegateway.com/passage/?search=Revelation+21&version=THGNT"
        self.assertTrue(any("Daniel7/Revelation Greek or Aramaic context control changed" in e for e in self.check(baseline=d)))

    def test_dan7_rev_six_new_attestation_links(self) -> None:
        expected={
            "CLM-DAN7-9-ANCIENT-THRONED-JUDGE":{"ATT-BASE-ATIQ-YOMIN-01"},
            "CLM-DAN7-13-ANCIENT-SON-OF-MAN-DISTINCT":{"ATT-BASE-ATIQ-YOMIN-02"},
            "CLM-DAN7-22-ANCIENT-GRANTS-JUDGMENT":{"ATT-BASE-ATIQ-YOMIN-03"},
            "CLM-REV1-4-JOHN-GREETING-TRIAD":{"ATT-EXT-HO-ON-ERCHOMENOS-01"},
            "CLM-REV21-22-LORD-GOD-LAMB-TEMPLE":{"ATT-BASE-PANTOKRATOR-02"},
            "CLM-REV1-8-LORD-GOD-ALPHA":{"ATT-EXT-HO-ON-ERCHOMENOS-02","ATT-BASE-PANTOKRATOR-01","ATT-BASE-ALPHA-OMEGA-01"},
        }
        for cid, att in expected.items():
            r=next(x for x in self.claims["records"] if x["claimId"]==cid)
            self.assertTrue(att.issubset(set(r["attestationIds"])))
            self.assertEqual("RESEARCH_HOLD",r["editorialState"])
            self.assertEqual("BLOCKED",r["publicationState"])

    def test_dan7_absolute_secondary_parse_cannot_be_certified_as_BDB(self) -> None:
        d=copy.deepcopy(self.claims)
        x=next(c for c in d["records"] if c["claimId"]=="CLM-DAN7-9-ANCIENT-THRONED-JUDGE")
        x["grammaticalEvidenceStatus"]="PRIMARY_BDB_COLLATED_CONFIRMED"
        self.assertTrue(any("Daniel7/Revelation grammar, speaker or interpretation guard changed" in e for e in self.check(claims=d)))

    def test_dan7_judisch_source_not_silently_deleted(self) -> None:
        d=copy.deepcopy(self.claims)
        x=next(c for c in d["records"] if c["claimId"]=="CLM-DAN7-13-ANCIENT-SON-OF-MAN-DISTINCT")
        x["sourceIds"]=["SRC-DANIEL-ARAMAIC"]
        self.assertTrue(any("original Aramaic and attributed Judisch secondary source lost" in e for e in self.check(claims=d)))

    def test_rev1_4_greeting_not_promoted_to_divine_direct_quote(self) -> None:
        d=copy.deepcopy(self.claims)
        x=next(c for c in d["records"] if c["claimId"]=="CLM-REV1-4-JOHN-GREETING-TRIAD")
        x["speakerEvidenceLevel"]="EXPLICIT_LORD_GOD_SPEECH_IN_1_4"
        self.assertTrue(any("Daniel7/Revelation grammar, speaker or interpretation guard changed" in e for e in self.check(claims=d)))

    def test_rev1_8_existing_claim_must_retain_new_extension_witness(self) -> None:
        d=copy.deepcopy(self.claims)
        x=next(c for c in d["records"] if c["claimId"]=="CLM-REV1-8-LORD-GOD-ALPHA")
        x["attestationIds"].remove("ATT-EXT-HO-ON-ERCHOMENOS-02")
        self.assertTrue(any("lost its independently reviewed text witnesses" in e for e in self.check(claims=d)))

    def test_rev21_22_john_narration_speaker_tag_preserved(self) -> None:
        d=copy.deepcopy(self.claims)
        x=next(c for c in d["records"] if c["claimId"]=="CLM-REV21-22-LORD-GOD-LAMB-TEMPLE")
        x["speakerEvidenceLevel"]="GOD_SPEAKS_DIRECTLY_IN_21_22"
        self.assertTrue(any("Daniel7/Revelation grammar, speaker or interpretation guard changed" in e for e in self.check(claims=d)))

    def test_dan7_scene_figures_not_collapsed_semantic_relation(self) -> None:
        d=copy.deepcopy(self.claims)
        x=next(c for c in d["semanticRelations"] if c["relationId"]=="REL-DAN7-9-13-APPROACH-DISTINCTION")
        x["relationType"]="CONTRASTS_NAMED_OBJECT"
        self.assertTrue(any("required semantic boundary" in e for e in self.check(claims=d)))

    def test_rev1_4_vs_1_8_speech_relation_must_be_preserved(self) -> None:
        d=copy.deepcopy(self.claims)
        x=next(c for c in d["semanticRelations"] if c["relationId"]=="REL-REV1-4-REV1-8-GREETING-VS-QUOTE")
        x["relationType"]="CONTRASTS_GRAMMATICAL_FORM"
        self.assertTrue(any("required semantic boundary" in e for e in self.check(claims=d)))

    def test_adonai_ex34_moses_not_yhwh_direct_speech(self) -> None:
        d,o=self.mutate("adonai","baseline",0)
        o["speaker"]="YHWH first-person naming"
        self.assertTrue(any("Adonai/Qedosh/Yah original-language speech/form guard changed" in err for err in self.check(baseline=d)))

    def test_adonai_ex34_two_tokens_same_verse_protected(self) -> None:
        d,o=self.mutate("adonai","baseline",0)
        o["tokenOccurrenceCount"]=1
        self.assertTrue(any("Adonai/Qedosh/Yah original-language speech/form guard changed" in err for err in self.check(baseline=d)))

    def test_adonai_ex34_speech_is_prayer(self) -> None:
        d,o=self.mutate("adonai","baseline",0)
        o["contextRole"]="new_proper_name_revelation"
        self.assertTrue(any("Adonai/Qedosh/Yah original-language speech/form guard changed" in err for err in self.check(baseline=d)))

    def test_adonai_isa6_accusative_marker_not_lost(self) -> None:
        d,o=self.mutate("adonai","baseline",1)
        o["grammaticalMarker"]="none"
        self.assertTrue(any("Adonai/Qedosh/Yah original-language speech/form guard changed" in err for err in self.check(baseline=d)))

    def test_adonai_isa6_throne_vision_not_moses_prayer(self) -> None:
        d,o=self.mutate("adonai","baseline",1)
        o["speaker"]="Moses addressing God"
        self.assertTrue(any("Adonai/Qedosh/Yah original-language speech/form guard changed" in err for err in self.check(baseline=d)))

    def test_adonai_ps8_suffixed_form_not_plain_adonai(self) -> None:
        d,o=self.mutate("adonai","baseline",2)
        o["surface"]="יְהוָה אֲדֹנָי"
        self.assertTrue(any("Adonai/Qedosh/Yah original-language speech/form guard changed" in err for err in self.check(baseline=d)))

    def test_adonai_ps8_possessive_vocalization_not_same(self) -> None:
        d,o=self.mutate("adonai","baseline",2)
        o["notExactSameVocalization"]=False
        self.assertTrue(any("Adonai/Qedosh/Yah original-language speech/form guard changed" in err for err in self.check(baseline=d)))

    def test_qedosh_isa1_object_marker_not_lost(self) -> None:
        d,o=self.mutate("qedosh-yisrael","baseline",0)
        o["grammaticalMarker"]="none"
        self.assertTrue(any("Adonai/Qedosh/Yah original-language speech/form guard changed" in err for err in self.check(baseline=d)))

    def test_qedosh_isa1_prophetic_accusation_not_yhwh_direct(self) -> None:
        d,o=self.mutate("qedosh-yisrael","baseline",0)
        o["speaker"]="YHWH speaking through prophet"
        self.assertTrue(any("Adonai/Qedosh/Yah original-language speech/form guard changed" in err for err in self.check(baseline=d)))

    def test_qedosh_isa43_i_yhwh_self_reference_necessary(self) -> None:
        d,o=self.mutate("qedosh-yisrael","baseline",1)
        o["selfReferenceClause"]="only human king says I"
        self.assertTrue(any("Adonai/Qedosh/Yah original-language speech/form guard changed" in err for err in self.check(baseline=d)))

    def test_qedosh_isa43_yhwh_voice_not_prophet_address(self) -> None:
        d,o=self.mutate("qedosh-yisrael","baseline",1)
        o["speaker"]="Isaiah, own voice"
        self.assertTrue(any("Adonai/Qedosh/Yah original-language speech/form guard changed" in err for err in self.check(baseline=d)))

    def test_qedosh_isa47_comma_editorial_not_new_lexeme(self) -> None:
        d,o=self.mutate("qedosh-yisrael","baseline",2)
        o["editionPunctuation"]="new name Kadosh only"
        self.assertTrue(any("Adonai/Qedosh/Yah original-language speech/form guard changed" in err for err in self.check(baseline=d)))

    def test_qedosh_isa47_speaker_uncertainty_not_certain_divine(self) -> None:
        d,o=self.mutate("qedosh-yisrael","baseline",2)
        o["speaker"]="YHWH personally named from mouth"
        self.assertTrue(any("Adonai/Qedosh/Yah original-language speech/form guard changed" in err for err in self.check(baseline=d)))

    def test_yah_ex15_free_yah_not_bet_prefix(self) -> None:
        d,o=self.mutate("yah","extension",0)
        o["prefixOnName"]="בְּ"
        self.assertTrue(any("Adonai/Qedosh/Yah original-language speech/form guard changed" in err for err in self.check(extension=d)))

    def test_yah_ex15_speakers_moses_and_israel(self) -> None:
        d,o=self.mutate("yah","extension",0)
        o["narrativeSpeaker"]="YHWH speaks from cloud"
        self.assertTrue(any("Adonai/Qedosh/Yah original-language speech/form guard changed" in err for err in self.check(extension=d)))

    def test_yah_ex15_short_name_not_other_deity(self) -> None:
        d,o=self.mutate("yah","extension",0)
        o["nameRole"]="UNRELATED_NAME_OF_OTHER_GOD"
        self.assertTrue(any("Adonai/Qedosh/Yah original-language speech/form guard changed" in err for err in self.check(extension=d)))

    def test_yah_ps68_bet_must_not_swap_to_conjectural_ki(self) -> None:
        d,o=self.mutate("yah","extension",1)
        o["surface"]="כִּי יָהּ שְׁמוֹ"
        self.assertTrue(any("Adonai/Qedosh/Yah original-language speech/form guard changed" in err for err in self.check(extension=d)))

    def test_yah_ps68_english_mt_verse_numbering_protected(self) -> None:
        d,o=self.mutate("yah","extension",1)
        o["verse"]="Psalms 68:4 MT"
        self.assertTrue(any("Adonai/Qedosh/Yah original-language speech/form guard changed" in err for err in self.check(extension=d)))

    def test_yah_ps68_net_conjecture_status_remains_hypothetical(self) -> None:
        d,o=self.mutate("yah","extension",1)
        o["textualConjecture"]="NET proves MT is כִּי יָהּ שְׁמוֹ"
        self.assertTrue(any("Adonai/Qedosh/Yah original-language speech/form guard changed" in err for err in self.check(extension=d)))

    def test_adonai_qedosh_yah_all_eight_claim_links_hold(self) -> None:
        expected={
            "CLM-ADONAI-EX34-9-MOSES-PRAYER":"ATT-BASE-ADONAI-01",
            "CLM-ADONAI-ISA6-1-VISION":"ATT-BASE-ADONAI-02",
            "CLM-ADONAI-PS8-2-OUR-LORD-SUFFIX":"ATT-BASE-ADONAI-03",
            "CLM-QEDOSH-ISA1-4-REJECTED-HOLY":"ATT-BASE-QEDOSH-YISRAEL-01",
            "CLM-QEDOSH-ISA43-3-GOD-SELF-SAVIOR":"ATT-BASE-QEDOSH-YISRAEL-02",
            "CLM-QEDOSH-ISA47-4-REDEEMER-DOXOLOGY":"ATT-BASE-QEDOSH-YISRAEL-03",
            "CLM-YAH-EX15-2-SUNG-ABBREVIATED-NAME":"ATT-EXT-YAH-01",
            "CLM-YAH-PS68-5-BET-NAME-CONJECTURE":"ATT-EXT-YAH-02",
        }
        for cid,aid in expected.items():
            r=next(x for x in self.claims["records"] if x["claimId"]==cid)
            self.assertEqual([aid],r["attestationIds"])
            self.assertEqual("RESEARCH_HOLD",r["editorialState"])
            self.assertEqual("BLOCKED",r["publicationState"])

    def test_adonai_human_genesis23_negative_control_must_remain(self) -> None:
        d=copy.deepcopy(self.baseline)
        row=next(x for x in d["records"] if x["id"]=="adonai")
        row["negativeControls"]=[]
        self.assertTrue(any("Adonai human honorific Genesis23 negative-control lost" in x for x in self.check(baseline=d)))

    def test_yah_ps68_source_net_conjecture_attribution_required(self) -> None:
        d=copy.deepcopy(self.claims)
        r=next(x for x in d["records"] if x["claimId"]=="CLM-YAH-PS68-5-BET-NAME-CONJECTURE")
        r["sourceIds"]=["SRC-MT-MECHON","SRC-JBQ-YAH-2014"]
        self.assertTrue(any("Yah original MT / secondary source attribution lost" in x for x in self.check(claims=d)))

    def test_yah_ps68_conjecture_cannot_promote_to_printed_mt(self) -> None:
        d=copy.deepcopy(self.claims)
        r=next(x for x in d["records"] if x["claimId"]=="CLM-YAH-PS68-5-BET-NAME-CONJECTURE")
        r["textualReconstructionStatus"]="DIRECT_ANCIENT_MANUSCRIPT_CERTIFIED"
        self.assertTrue(any("Adonai/Qedosh/Yah interpretive boundary changed" in x for x in self.check(claims=d)))

    def test_qedosh_isa47_speaker_doubt_cannot_be_removed(self) -> None:
        d=copy.deepcopy(self.claims)
        r=next(x for x in d["records"] if x["claimId"]=="CLM-QEDOSH-ISA47-4-REDEEMER-DOXOLOGY")
        r["nameEvidenceStatus"]="DIRECT_YHWH_NEW_PERSONAL_NAME"
        self.assertTrue(any("Adonai/Qedosh/Yah interpretive boundary changed" in x for x in self.check(claims=d)))

    def test_adonai_ps8_not_lexically_identical_to_ex34(self) -> None:
        d=copy.deepcopy(self.claims)
        x=next(r for r in d["semanticRelations"] if r["relationId"]=="REL-ADONAI-ADONEINU-SUFFIX")
        x["relationType"]="CONTRASTS_REFERENT"
        self.assertTrue(any("required semantic boundary" in e for e in self.check(claims=d)))

    def test_qedosh_isa1_oracle_speaker_relation_must_stay(self) -> None:
        d=copy.deepcopy(self.claims)
        x=next(r for r in d["semanticRelations"] if r["relationId"]=="REL-QEDOSH-ACCUSATION-ORACLE")
        x["relationType"]="CONTRASTS_GRAMMATICAL_FORM"
        self.assertTrue(any("required semantic boundary" in e for e in self.check(claims=d)))


if __name__ == "__main__":
    unittest.main()
