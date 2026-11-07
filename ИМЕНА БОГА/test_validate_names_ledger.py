"""Mutation tests for the read-only Names of God ledger validator."""
from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from validate_names_ledger import validate, validate_extension, validate_source_access, validate_apocalyptic

ROOT = Path(__file__).resolve().parent


class ResearchEvidenceGuardTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.baseline = json.loads((ROOT / "data" / "names_ledger_v1.json").read_text(encoding="utf-8"))
        cls.extension = json.loads((ROOT / "data" / "names_extension_ledger_v1.json").read_text(encoding="utf-8"))
        cls.sources = json.loads((ROOT / "data" / "source_access_register_v1.json").read_text(encoding="utf-8"))

    def test_current_research_corpora_pass_structure(self) -> None:
        self.assertEqual([], validate(self.baseline))
        self.assertEqual([], validate_extension(self.extension, self.baseline))
        self.assertEqual([], validate_source_access(self.sources))
        self.assertEqual([], validate_apocalyptic(self.baseline, self.extension))

    def test_altar_cannot_be_promoted_to_personal_name(self) -> None:
        data = copy.deepcopy(self.baseline)
        next(row for row in data["records"] if row["id"] == "nissi")["category"] = "personal_divine_name"
        self.assertTrue(validate(data))

    def test_two_roi_roots_must_not_be_conflated(self) -> None:
        data = copy.deepcopy(self.baseline)
        next(row for row in data["records"] if row["id"] == "ro-i")["lexicalRoot"] = "ראה"
        self.assertTrue(any("lexical collision" in error for error in validate(data)))

    def test_yireh_passive_verb_cannot_be_erased(self) -> None:
        data = copy.deepcopy(self.baseline)
        next(row for row in data["records"] if row["id"] == "yireh")["morphologyNote"]["verb2"] = "יִרְאֶה"
        self.assertTrue(any("Genesis 22:14" in error for error in validate(data)))

    def test_two_jeremiah_referents_and_old_greek_absence_are_preserved(self) -> None:
        data = copy.deepcopy(self.baseline)
        next(row for row in data["records"] if row["id"] == "tsidkenu")["witnesses"] = []
        self.assertTrue(validate(data))

    def test_baseline_cannot_gain_a_silent_30th_arena_name(self) -> None:
        data = copy.deepcopy(self.baseline)
        data["records"].append(copy.deepcopy(data["records"][0]))
        self.assertTrue(validate(data))

    def test_extension_cannot_reuse_existing_arena_id(self) -> None:
        data = copy.deepcopy(self.extension)
        data["records"][0]["id"] = "yhwh"
        self.assertTrue(any("duplicate ID" in error for error in validate_extension(data, self.baseline)))

    def test_extension_publication_and_rights_hold_are_required(self) -> None:
        data = copy.deepcopy(self.extension)
        data["records"][0]["publicationState"] = "PROMOTE"
        data["records"][0]["holds"] = []
        self.assertTrue(any("publication" in error for error in validate_extension(data, self.baseline)))

    def test_greek_entry_cannot_become_hebrew_without_a_text_change(self) -> None:
        data = copy.deepcopy(self.extension)
        next(row for row in data["records"] if row["id"] == "poimen-ho-kalos")["language"] = "hebrew"
        self.assertTrue(any("script absent" in error for error in validate_extension(data, self.baseline)))


    def test_greever_article_cannot_be_relabelled_as_yah_lexicography(self) -> None:
        data = copy.deepcopy(self.sources)
        next(row for row in data["records"] if row["id"] == "SRC-GREEVER-2020")["sourceRole"] = "LEXICAL_ATTESTATION"
        self.assertTrue(any("relevance/role" in error for error in validate_source_access(data)))

    def test_shaw_abstract_cannot_become_complete_4q120_collation(self) -> None:
        data = copy.deepcopy(self.sources)
        next(row for row in data["records"] if row["id"] == "SRC-SHAW-2002")["accessState"] = "FULL_OBJECT_VERIFIED"
        self.assertTrue(any("catalogue falsely promoted" in error for error in validate_source_access(data)))

    def test_article_specific_license_does_not_erase_thgnt_rights(self) -> None:
        data = copy.deepcopy(self.sources)
        next(row for row in data["records"] if row["id"] == "SRC-THGNT-LUKE")["rightsState"] = "PUBLICATION_ELIGIBLE"
        self.assertTrue(any("rights" in error or "license" in error or "THGNT" in error
                            for error in validate_source_access(data)))

    def test_source_cannot_be_approved_by_merely_linking_it(self) -> None:
        data = copy.deepcopy(self.sources)
        next(row for row in data["records"] if row["id"] == "SRC-VANWOLDE-2021")["publicationState"] = "PROMOTE"
        self.assertTrue(any("publication not authorized" in error for error in validate_source_access(data)))

    def test_luke_132_speaker_agent_recipient_must_not_be_conflated(self) -> None:
        agent = next(row for row in self.extension["records"] if row["id"] == "kyrios-ho-theos")
        roles = agent["discourseRoles"]
        self.assertIn("Gabriel", roles["narrativeSpeaker"])
        self.assertIn("κύριος ὁ θεὸς", roles["grammaticalAgent"])
        self.assertIn("Jesus", roles["recipient"])
        self.assertNotEqual(roles["narrativeSpeaker"], roles["grammaticalAgent"])


    def test_hidden_bidi_controls_are_not_permitted_in_script_forms(self) -> None:
        data = copy.deepcopy(self.baseline)
        row = next(row for row in data["records"] if row["id"] == "yhwh")
        row["verifiedForm"] += chr(0x202E)  # RIGHT-TO-LEFT OVERRIDE
        self.assertTrue(any("format/bidi control" in error for error in validate(data)))

    def test_non_nfc_greek_is_rejected(self) -> None:
        import unicodedata
        data = copy.deepcopy(self.extension)
        row = next(row for row in data["records"] if row["id"] == "ho-on-erchomenos")
        form = unicodedata.normalize("NFD", row["verifiedDigitalForm"])
        self.assertNotEqual(form, row["verifiedDigitalForm"])
        row["verifiedDigitalForm"] = form
        self.assertTrue(any("NFC-normalized" in error for error in validate_extension(data, self.baseline)))


    def test_genesis_35_7_place_is_not_altar(self) -> None:
        data = copy.deepcopy(self.baseline)
        row = next(x for x in data["records"] if x["id"] == "el-bethel")
        row["attestations"][0]["namedObject"] = "altar"
        self.assertTrue(any("Genesis 35:7" in issue and "regression" in issue for issue in validate(data)))

    def test_el_elyon_abram_speech_not_melchizedek(self) -> None:
        data = copy.deepcopy(self.baseline)
        row = next(x for x in data["records"] if x["id"] == "el-elyon")
        next(x for x in row["attestations"] if x["verse"] == "Genesis 14:22")["speaker"] = "Melchizedek"
        self.assertTrue(any("Genesis 14:22" in issue and "regression" in issue for issue in validate(data)))

    def test_shaddai_is_not_all_divine_first_person_speech(self) -> None:
        data = copy.deepcopy(self.baseline)
        row = next(x for x in data["records"] if x["id"] == "el-shaddai")
        next(x for x in row["attestations"] if x["verse"] == "Genesis 28:3")["speaker"] = "God"
        self.assertTrue(any("Genesis 28:3" in issue and "regression" in issue for issue in validate(data)))

    def test_hagar_name_invocation_not_place_naming(self) -> None:
        data = copy.deepcopy(self.baseline)
        row = next(x for x in data["records"] if x["id"] == "el-roi")
        row["attestations"][0]["speechAct"] = "place_naming"
        self.assertTrue(any("Genesis 16:13" in issue and "regression" in issue for issue in validate(data)))

    def test_el_olam_invocation_not_beersheba_place_name(self) -> None:
        data = copy.deepcopy(self.baseline)
        row = next(x for x in data["records"] if x["id"] == "el-olam")
        row["attestations"][0]["namedObject"] = "place"
        self.assertTrue(any("Genesis 21:33" in issue and "regression" in issue for issue in validate(data)))

    def test_exodus_6_3_pointing_cannot_be_silently_normalized(self) -> None:
        data = copy.deepcopy(self.baseline)
        row = next(x for x in data["records"] if x["id"] == "el-shaddai")
        row["attestations"][-1]["surface"] = "בְּאֵל שַׁדַּי"
        self.assertTrue(any("Exodus 6:3" in issue for issue in validate(data)))

    def test_cargill_abstract_cannot_be_promoted_to_fully_collated_text(self) -> None:
        data = copy.deepcopy(self.sources)
        row = next(x for x in data["records"] if x["id"] == "SRC-CARGILL-2019")
        row["accessState"] = "FULL_OBJECT_VERIFIED"
        self.assertTrue(any("Cargill chapter abstract" in issue for issue in validate_source_access(data)))

    def test_patriarchal_attestation_counter_drift_is_rejected(self) -> None:
        data = copy.deepcopy(self.baseline)
        data["auditProtocol"]["patriarchalAttestations"]["totalAttestations"] = 29
        self.assertTrue(any("patriarchal attestation counter drift" in issue for issue in validate(data)))


    def test_genesis_14_19_lamed_prefix_cannot_be_silently_dropped(self) -> None:
        data = copy.deepcopy(self.baseline)
        row = next(x for x in data["records"] if x["id"] == "el-elyon")
        occurrence = next(x for x in row["attestations"] if x["verse"] == "Genesis 14:19")
        occurrence["surface"] = "אֵל עֶלְיוֹן"
        self.assertTrue(any("Genesis 14:19" in issue and "surface changed" in issue for issue in validate(data)))

    def test_missing_all_shaddai_attestations_rejects_without_exception(self) -> None:
        data = copy.deepcopy(self.baseline)
        row = next(x for x in data["records"] if x["id"] == "el-shaddai")
        row["attestations"] = []
        errors = validate(data)
        self.assertTrue(any("el-shaddai" in issue for issue in errors))


    def test_daniel_7_9_yomin_cannot_be_silently_normalized_to_yomaya(self) -> None:
        data = copy.deepcopy(self.baseline)
        row = next(r for r in data["records"] if r["id"] == "atiq-yomin")
        next(x for x in row["attestations"] if x["verse"] == "Daniel 7:9")["surface"] = "עַתִּיק יוֹמַיָּא"
        self.assertTrue(any("Daniel 7:9" in v for v in validate_apocalyptic(data, self.extension)))

    def test_daniel_7_13_ancient_cannot_be_made_same_as_son_of_man(self) -> None:
        data = copy.deepcopy(self.baseline)
        row = next(r for r in data["records"] if r["id"] == "atiq-yomin")
        row["referentBoundary"] = "The Ancient is the figure who comes toward himself"
        self.assertTrue(any("two vision figures" in v for v in validate_apocalyptic(data, self.extension)))

    def test_revelation_1_8_theos_difference_must_be_retained(self) -> None:
        data = copy.deepcopy(self.baseline)
        row = next(r for r in data["records"] if r["id"] == "alpha-omega")
        row["printedEditionDiffs"][0]["variant2"] = "Both SBL and TR have ὁ θεός"
        self.assertTrue(any("θεός difference" in v for v in validate_apocalyptic(data, self.extension)))

    def test_revelation_21_6_eimi_difference_must_be_retained(self) -> None:
        data = copy.deepcopy(self.baseline)
        row = next(r for r in data["records"] if r["id"] == "alpha-omega")
        row["printedEditionDiffs"][1]["variant1"] = "Both editions have ἐγώ εἰμι"
        self.assertTrue(any("εἰμι omission" in v for v in validate_apocalyptic(data, self.extension)))

    def test_revelation_22_13_speaker_evidence_not_promoted_to_explicit(self) -> None:
        data = copy.deepcopy(self.baseline)
        row = next(r for r in data["records"] if r["id"] == "alpha-omega")
        next(x for x in row["attestations"] if x["verse"] == "Revelation 22:13")["speakerEvidence"] = "explicit_speech_attribution_in_verse"
        self.assertTrue(any("narrative voice" in v for v in validate_apocalyptic(data, self.extension)))

    def test_revelation_21_22_almighty_cannot_be_deleted(self) -> None:
        data = copy.deepcopy(self.baseline)
        row = next(r for r in data["records"] if r["id"] == "pantokrator")
        row["attestations"] = row["attestations"][:1]
        self.assertTrue(any("apocalyptic verse set drift" in v for v in validate_apocalyptic(data, self.extension)))

    def test_revelation_1_4_separate_from_jesus_in_verse_5(self) -> None:
        data = copy.deepcopy(self.extension)
        row = next(r for r in data["records"] if r["id"] == "ho-on-erchomenos")
        row["attestations"][0]["surface"] = "ὁ ἐρχόμενος"
        self.assertTrue(any("Greek original surface" in v for v in validate_apocalyptic(self.baseline, data)))

    def test_public_domain_tr1550_cannot_override_publication_hold(self) -> None:
        data = copy.deepcopy(self.sources)
        row = next(r for r in data["records"] if r["id"] == "SRC-TR1550-REV18")
        row["publicationState"] = "PROMOTE"
        self.assertTrue(any("publication" in v for v in validate_source_access(data)))

    def test_proprietary_thgnt_revelation_must_retain_rights(self) -> None:
        data = copy.deepcopy(self.sources)
        row = next(r for r in data["records"] if r["id"] == "SRC-THGNT-REV216")
        row["rightsState"] = "PUBLICATION_ELIGIBLE"
        self.assertTrue(any("THGNT" in v or "license" in v for v in validate_source_access(data)))

    def test_sbl_editorial_intro_cannot_be_collated_manuscript_apparatus(self) -> None:
        data = copy.deepcopy(self.sources)
        row = next(r for r in data["records"] if r["id"] == "SRC-SBL-INTRO")
        row["sourceRole"] = "MANUSCRIPT_CRITICAL_APPARATUS"
        self.assertTrue(any("relevance/role" in v for v in validate_source_access(data)))

    def test_missing_apocalyptic_attestation_list_is_fail_closed(self) -> None:
        data = copy.deepcopy(self.baseline)
        row = next(r for r in data["records"] if r["id"] == "atiq-yomin")
        row.pop("attestations")
        self.assertTrue(any("apocalyptic" in v for v in validate_apocalyptic(data, self.extension)))


    def test_sblgnt_official_license_is_text_only_and_cannot_be_widened(self) -> None:
        data = copy.deepcopy(self.sources)
        row = next(r for r in data["records"] if r["id"] == "SRC-SBLGNT-CCBY-LICENSE")
        row["licenseScope"] = "ALL_VERSES_ALL_BIBLEGATEWAY_GRAPHICS_ALL_TRANSLATIONS"
        self.assertTrue(any("text-only license boundaries" in issue
                            for issue in validate_source_access(data)))

    def test_sblgnt_license_does_not_automatically_license_host_page(self) -> None:
        data = copy.deepcopy(self.sources)
        row = next(r for r in data["records"] if r["id"] == "SRC-SBL-REVELATION")
        row["rightsState"] = "PUBLICATION_ELIGIBLE"
        self.assertTrue(any("host website display" in issue for issue in validate_source_access(data)))

    def test_sblgnt_license_rights_do_not_approve_unreviewed_claims(self) -> None:
        data = copy.deepcopy(self.sources)
        row = next(r for r in data["records"] if r["id"] == "SRC-SBLGNT-CCBY-LICENSE")
        row["publicationState"] = "PROMOTE"
        self.assertTrue(any("publication" in issue for issue in validate_source_access(data)))

    def test_sblgnt_publisher_license_must_have_ccby_attestation(self) -> None:
        data = copy.deepcopy(self.sources)
        row = next(r for r in data["records"] if r["id"] == "SRC-SBLGNT-CCBY-LICENSE")
        row["license"] = "License unknown"
        self.assertTrue(any("official CC BY 4.0 publisher-license" in issue
                            for issue in validate_source_access(data)))


if __name__ == "__main__":
    unittest.main()
