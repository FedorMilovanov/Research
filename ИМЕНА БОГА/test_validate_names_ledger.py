"""Mutation tests for the read-only Names of God ledger validator."""
from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from validate_names_ledger import validate, validate_extension, validate_source_access, validate_apocalyptic, validate_prophetic_namings, validate_six_title_attestations, validate_memorial_attestations, validate_speech_intertext, validate_extension_attestations, validate_core_name_lexeme, validate_full_coverage

ROOT = Path(__file__).resolve().parent


class ResearchEvidenceGuardTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.baseline = json.loads((ROOT / "data" / "names_ledger_v1.json").read_text(encoding="utf-8"))
        cls.extension = json.loads((ROOT / "data" / "names_extension_ledger_v1.json").read_text(encoding="utf-8"))
        cls.sources = json.loads((ROOT / "data" / "source_access_register_v1.json").read_text(encoding="utf-8"))
        cls.title_contract = json.loads((ROOT / "data" / "attestation_contract_v1.json").read_text(encoding="utf-8"))
        cls.memorial_contract = json.loads((ROOT / "data" / "memorial_attestation_contract_v1.json").read_text(encoding="utf-8"))
        cls.speech_contract = json.loads((ROOT / "data" / "speech_intertext_contract_v1.json").read_text(encoding="utf-8"))
        cls.extension_contract = json.loads((ROOT / "data" / "extension_attestation_contract_v1.json").read_text(encoding="utf-8"))
        cls.core_contract = json.loads((ROOT / "data" / "core_name_lexeme_contract_v1.json").read_text(encoding="utf-8"))

    def test_current_research_corpora_pass_structure(self) -> None:
        self.assertEqual([], validate(self.baseline))
        self.assertEqual([], validate_extension(self.extension, self.baseline))
        self.assertEqual([], validate_source_access(self.sources))
        self.assertEqual([], validate_apocalyptic(self.baseline, self.extension))
        self.assertEqual([], validate_prophetic_namings(self.baseline))
        self.assertEqual([], validate_six_title_attestations(self.baseline, self.title_contract))
        self.assertEqual([], validate_memorial_attestations(self.baseline, self.memorial_contract))
        self.assertEqual([], validate_speech_intertext(self.baseline, self.speech_contract))
        self.assertEqual([], validate_extension_attestations(self.extension, self.extension_contract))
        self.assertEqual([], validate_core_name_lexeme(self.baseline, self.core_contract))
        self.assertEqual([], validate_full_coverage(self.baseline, self.extension))

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


    def test_daniel_absolute_emphatic_parsing_cannot_be_swapped(self) -> None:
        data = copy.deepcopy(self.baseline)
        row = next(r for r in data["records"] if r["id"] == "atiq-yomin")
        row["lexicalNote"]["parsingEvidence"]["analyses"][0]["state"] = "emphatic"
        self.assertTrue(any("absolute/emphatic plural parsing" in issue
                            for issue in validate_apocalyptic(data, self.extension)))

    def test_confessional_daniel_grammar_cannot_be_called_primary_lexicon(self) -> None:
        data = copy.deepcopy(self.sources)
        row = next(r for r in data["records"] if r["id"] == "SRC-JUDISCH-DAN7-ARAMAIC")
        row["primaryLexiconStatus"] = "BDB_FULL_TEXT_COLLATED"
        self.assertTrue(any("primary lexicon verification" in issue
                            for issue in validate_source_access(data)))

    def test_daniel_grammar_is_still_secondary_B1(self) -> None:
        data = copy.deepcopy(self.baseline)
        row = next(r for r in data["records"] if r["id"] == "atiq-yomin")
        row["lexicalNote"]["parsingEvidence"]["evidenceClass"] = "A1"
        self.assertTrue(any("erroneously promoted" in issue
                            for issue in validate_apocalyptic(data, self.extension)))


    def test_isaiah_9_5_cannot_be_renumbered_as_mt_9_6(self) -> None:
        data = copy.deepcopy(self.baseline)
        row = next(r for r in data["records"] if r["id"] == "el-gibbor")
        row["attestations"][0]["numbering"]["hebrew"] = "Isaiah 9:6"
        self.assertTrue(any("numbering systems" in issue for issue in validate_prophetic_namings(data)))

    def test_isaiah_10_21_lexical_el_prefix_cannot_be_removed(self) -> None:
        data = copy.deepcopy(self.baseline)
        row = next(r for r in data["records"] if r["id"] == "el-gibbor")
        row["attestations"][1]["surface"] = "אֵל גִּבּוֹר"
        self.assertTrue(any("Isaiah 10:21" in issue for issue in validate_prophetic_namings(data)))

    def test_isaiah_9_greek_expansion_cannot_be_silently_ascribed_to_rahlfs(self) -> None:
        data = copy.deepcopy(self.baseline)
        row = next(r for r in data["records"] if r["id"] == "el-gibbor")
        row["printedGreekWitnesses"][0]["longListTheosIschyros"] = True
        self.assertTrue(any("Rahlfs-Hanhart short name" in issue for issue in validate_prophetic_namings(data)))

    def test_greek_orthodox_expanded_text_requires_edition_provenance(self) -> None:
        data = copy.deepcopy(self.baseline)
        row = next(r for r in data["records"] if r["id"] == "el-gibbor")
        row["printedGreekWitnesses"][1]["claimScope"] = "ORIGINAL_LXX_MANUSCRIPT_VERIFIED"
        self.assertTrue(any("Greek digital variants falsely promoted" in issue for issue in validate_prophetic_namings(data)))

    def test_jeremiah_33_16_jerusalem_feminine_not_royal_masculine(self) -> None:
        data = copy.deepcopy(self.baseline)
        row = next(r for r in data["records"] if r["id"] == "tsidkenu")
        r33 = next(x for x in row["attestations"] if x["verse"] == "Jeremiah 33:16")
        r33["nameDelimiter"] = "וְזֶה-שְּׁמוֹ"
        self.assertTrue(any("feminine city cue" in issue for issue in validate_prophetic_namings(data)))

    def test_jeremiah_old_greek_absence_cannot_be_replaced_with_fake_greek(self) -> None:
        data = copy.deepcopy(self.baseline)
        row = next(r for r in data["records"] if r["id"] == "tsidkenu")
        r33 = next(x for x in row["attestations"] if x["verse"] == "Jeremiah 33:16")
        r33["oldGreekPassageStatus"] = "LXX_JEREMIAH_33_16_VERIFIED"
        self.assertTrue(any("Old Greek absence" in issue for issue in validate_prophetic_namings(data)))

    def test_ezekiel_48_35_city_cannot_be_named_personal_yhwh(self) -> None:
        data = copy.deepcopy(self.baseline)
        row = next(r for r in data["records"] if r["id"] == "shammah")
        row["attestations"][0]["namedObject"] = "God"
        self.assertTrue(any("Ezekiel 48:35" in issue for issue in validate_prophetic_namings(data)))

    def test_lxx_isaiah_7_naming_verb_is_not_matthew_plural(self) -> None:
        data = copy.deepcopy(self.baseline)
        row = next(r for r in data["records"] if r["id"] == "immanuel")
        rx = next(x for x in row["attestations"] if x["verse"] == "Isaiah 7:14 LXX Rahlfs-Hanhart")
        rx["nameDelimiter"] = "καλέσουσιν τὸ ὄνομα αὐτοῦ"
        self.assertTrue(any("LXX Isaiah 7:14 singular" in issue for issue in validate_prophetic_namings(data)))

    def test_matthew_1_23_name_verb_cannot_be_hebrew_singular(self) -> None:
        data = copy.deepcopy(self.baseline)
        row = next(r for r in data["records"] if r["id"] == "immanuel")
        rx = next(x for x in row["attestations"] if x["verse"] == "Matthew 1:23")
        rx["namingVerbForm"] = "καλέσεις 2nd singular"
        self.assertTrue(any("Matthew 1:23 plural" in issue for issue in validate_prophetic_namings(data)))

    def test_isaiah_8_10_is_assurance_not_child_naming(self) -> None:
        data = copy.deepcopy(self.baseline)
        row = next(r for r in data["records"] if r["id"] == "immanuel")
        rx = next(x for x in row["attestations"] if x["verse"] == "Isaiah 8:10")
        rx["receptionLayer"] = "NEW_PERSONAL_NAME"
        self.assertTrue(any("Isaiah 8:10 assurance" in issue for issue in validate_prophetic_namings(data)))

    def test_rahlfs_publisher_edition_cannot_become_public_domain(self) -> None:
        data = copy.deepcopy(self.sources)
        row = next(r for r in data["records"] if r["id"] == "SRC-RAHLFS-ISAIAH")
        row["rightsState"] = "PUBLICATION_ELIGIBLE"
        self.assertTrue(any("Rahlfs-Hanhart edited digital text" in issue for issue in validate_source_access(data)))

    def test_leuchter_abstract_cannot_become_verified_old_greek_codex(self) -> None:
        data = copy.deepcopy(self.sources)
        row = next(r for r in data["records"] if r["id"] == "SRC-LEUCHTER-JER33")
        row["accessState"] = "FULL_OBJECT_VERIFIED"
        self.assertTrue(any("Leuchter abstract" in issue for issue in validate_source_access(data)))

    def test_prophetic_empty_witnesses_are_rejected_without_exceptions(self) -> None:
        data = copy.deepcopy(self.baseline)
        row = next(r for r in data["records"] if r["id"] == "immanuel")
        row["attestations"] = []
        self.assertTrue(any("prophetic immanuel" in issue for issue in validate_prophetic_namings(data)))


    def test_matthew_greek_is_not_mislabelled_rahlfs_lxx(self) -> None:
        data = copy.deepcopy(self.baseline)
        row = next(r for r in data["records"] if r["id"] == "immanuel")
        witness = next(x for x in row["attestations"] if x["verse"] == "Matthew 1:23")
        witness["edition"] = "Rahlfs-Hanhart 2006 via Deutsche Bibelgesellschaft"
        self.assertTrue(any("edition-specific rights/witness provenance" in issue
                            for issue in validate_prophetic_namings(data)))

    def test_greek_lxx_cannot_inherit_sblgnt_licensed_edition(self) -> None:
        data = copy.deepcopy(self.baseline)
        row = next(r for r in data["records"] if r["id"] == "immanuel")
        witness = next(x for x in row["attestations"] if x["verse"] == "Isaiah 7:14 LXX Rahlfs-Hanhart")
        witness["rightsState"] = "RIGHTS_UNKNOWN"
        witness["edition"] = "SBLGNT 2010 via BibleGateway"
        self.assertTrue(any("edition-specific rights/witness provenance" in issue
                            for issue in validate_prophetic_namings(data)))


    def test_six_title_corpus_contract_requires_22_exact_witnesses(self) -> None:
        data = copy.deepcopy(self.baseline)
        row = next(x for x in data["records"] if x["id"] == "sabaoth")
        row["attestations"].pop()
        self.assertTrue(any("22 reviewed contextual" in e for e in validate_six_title_attestations(data, self.title_contract)))

    def test_six_title_contract_core_fields_cannot_be_weakened(self) -> None:
        contract = copy.deepcopy(self.title_contract)
        contract["requiredFields"].remove("sourceUrl")
        self.assertTrue(any("schema weakened" in e for e in validate_six_title_attestations(self.baseline, contract)))

    def test_six_title_source_url_must_match_independently_locked_contract(self) -> None:
        data = copy.deepcopy(self.baseline)
        row = next(x for x in data["records"] if x["id"] == "qedosh-yisrael")
        row["attestations"][1]["sourceUrl"] = "https://example.com/unknown-greek"
        self.assertTrue(any("field sourceUrl differs" in e for e in validate_six_title_attestations(data, self.title_contract)))

    def test_sabaoth_in_samuel_lamed_is_preserved(self) -> None:
        data = copy.deepcopy(self.baseline)
        row = next(x for x in data["records"] if x["id"] == "sabaoth")
        row["attestations"][0]["surface"] = "יְהוָה צְבָאוֹת"
        self.assertTrue(any("1 Sam 1:3 lamed" in e for e in validate_six_title_attestations(data, self.title_contract)))

    def test_sabaoth_james_genitive_not_roman_nominative(self) -> None:
        data = copy.deepcopy(self.baseline)
        row = next(x for x in data["records"] if x["id"] == "sabaoth")
        row["attestations"][4]["surface"] = "κύριος Σαβαὼθ"
        self.assertTrue(any("James genitive Greek" in e for e in validate_six_title_attestations(data, self.title_contract)))

    def test_sabaoth_romans_nominative_not_james_genitive(self) -> None:
        data = copy.deepcopy(self.baseline)
        row = next(x for x in data["records"] if x["id"] == "sabaoth")
        row["attestations"][5]["surface"] = "Κυρίου Σαβαὼθ"
        self.assertTrue(any("Romans nominative Greek" in e for e in validate_six_title_attestations(data, self.title_contract)))

    def test_qanna_naming_is_not_erased_from_exodus_34_14(self) -> None:
        data = copy.deepcopy(self.baseline)
        row = next(x for x in data["records"] if x["id"] == "el-qanna")
        row["attestations"][0]["nameClause"] = ""
        self.assertTrue(any("naming formula suppressed" in e for e in validate_six_title_attestations(data, self.title_contract)))

    def test_qanna_deuteronomy_is_descriptor_not_repeated_naming_ritual(self) -> None:
        data = copy.deepcopy(self.baseline)
        row = next(x for x in data["records"] if x["id"] == "el-qanna")
        row["attestations"][1]["selfNamingInVerse"] = True
        self.assertTrue(any("wrongly promoted" in e for e in validate_six_title_attestations(data, self.title_contract)))

    def test_deuteronomy_other_rock_cannot_be_yhwh(self) -> None:
        data = copy.deepcopy(self.baseline)
        row = next(x for x in data["records"] if x["id"] == "tsur")
        next(x for x in row["attestations"] if x["verse"] == "Deuteronomy 32:37")["isDivineDesignation"] = True
        self.assertTrue(any("foreign rock falsely" in e for e in validate_six_title_attestations(data, self.title_contract)))

    def test_deuteronomy_two_contrasted_rocks_cannot_be_collapsed(self) -> None:
        data = copy.deepcopy(self.baseline)
        row = next(x for x in data["records"] if x["id"] == "tsur")
        next(x for x in row["attestations"] if x["verse"] == "Deuteronomy 32:31")["referentClass"] = "YHWH_ONLY"
        self.assertTrue(any("foreign rock falsely" in e for e in validate_six_title_attestations(data, self.title_contract)))

    def test_isaiah_holy_one_grammatical_object_is_marked(self) -> None:
        data = copy.deepcopy(self.baseline)
        row = next(x for x in data["records"] if x["id"] == "qedosh-yisrael")
        row["attestations"][0]["grammaticalMarker"] = ""
        self.assertTrue(any("Isaiah 1:4 object marker" in e for e in validate_six_title_attestations(data, self.title_contract)))

    def test_adonai_moses_uses_twice_in_exodus_34_9(self) -> None:
        data = copy.deepcopy(self.baseline)
        row = next(x for x in data["records"] if x["id"] == "adonai")
        row["attestations"][0]["tokenOccurrenceCount"] = 1
        self.assertTrue(any("repeated Adonai" in e for e in validate_six_title_attestations(data, self.title_contract)))

    def test_adoni_human_address_cannot_become_divine(self) -> None:
        data = copy.deepcopy(self.baseline)
        row = next(x for x in data["records"] if x["id"] == "adonai")
        row["negativeControls"] = []
        self.assertTrue(any("human adoni negative control" in e for e in validate_six_title_attestations(data, self.title_contract)))

    def test_psalm_eight_adonenu_cannot_be_normalized_to_adonai(self) -> None:
        data = copy.deepcopy(self.baseline)
        row = next(x for x in data["records"] if x["id"] == "adonai")
        row["attestations"][2]["surface"] = "יְהוָה אֲדֹנָי"
        self.assertTrue(any("Psalm 8 suffixed" in e for e in validate_six_title_attestations(data, self.title_contract)))

    def test_elohim_plural_noun_does_not_override_singular_bara(self) -> None:
        data = copy.deepcopy(self.baseline)
        row = next(x for x in data["records"] if x["id"] == "elohim")
        row["attestations"][0]["verbAgreement"] = "plural"
        self.assertTrue(any("singular agreement" in e for e in validate_six_title_attestations(data, self.title_contract)))

    def test_exodus_20_2_versification_and_other_gods_are_both_required(self) -> None:
        data = copy.deepcopy(self.baseline)
        row = next(x for x in data["records"] if x["id"] == "elohim")
        rx = row["attestations"][1]
        rx["numbering"]["mechonMamreHebrew"] = "Exodus 20:3"
        rx["referentClass"] = "YHWH"
        self.assertTrue(any("Exodus 20 false gods or versification" in e for e in validate_six_title_attestations(data, self.title_contract)))

    def test_cambridge_article_rights_are_ccby_but_not_bible_versions(self) -> None:
        data = copy.deepcopy(self.sources)
        row = next(x for x in data["records"] if x["id"] == "SRC-CAMBRIDGE-GOD-PRONOUNS")
        row["licenseScope"] = "ALL_BIBLE_VERSIONS_AND_IMAGES"
        self.assertTrue(any("Nicholas Adams Cambridge" in e for e in validate_source_access(data)))

    def test_suchard_historical_grammar_is_still_secondary(self) -> None:
        data = copy.deepcopy(self.sources)
        row = next(x for x in data["records"] if x["id"] == "SRC-SUCHARD-ELOHIM-2025")
        row["evidenceClass"] = "A1"
        self.assertTrue(any("Suchard 2025" in e for e in validate_source_access(data)))


    def test_memorial_place_is_not_altar_in_genesis_22(self) -> None:
        d = copy.deepcopy(self.baseline)
        r = next(x for x in d["records"] if x["id"] == "yireh")
        r["attestations"][1]["namedObject"] = "altar"
        self.assertTrue(any("Gen22:14 names PLACE" in e for e in validate_memorial_attestations(d, self.memorial_contract)))

    def test_memorial_qal_not_niphal_in_genesis_22(self) -> None:
        d = copy.deepcopy(self.baseline)
        r = next(x for x in d["records"] if x["id"] == "yireh")
        r["attestations"][2]["surface"] = "בְּהַר יְהוָה יִרְאֶה"
        self.assertTrue(any("Gen22 Qal versus Niphal" in e for e in validate_memorial_attestations(d, self.memorial_contract)))

    def test_memorial_exodus_17_15_moses_named_altar_not_yhwh(self) -> None:
        d = copy.deepcopy(self.baseline)
        r = next(x for x in d["records"] if x["id"] == "nissi")
        r["attestations"][0]["namedObject"] = "God"
        self.assertTrue(any("Ex17:15 altar name" in e for e in validate_memorial_attestations(d, self.memorial_contract)))

    def test_memorial_exodus_17_lxx_refuge_not_rewritten_as_banner(self) -> None:
        d = copy.deepcopy(self.baseline)
        r = next(x for x in d["records"] if x["id"] == "nissi")
        r["attestations"][1]["surface"] = "Κύριός μου σημεῖον"
        self.assertTrue(any("MT banner vs LXX refuge" in e for e in validate_memorial_attestations(d, self.memorial_contract)))

    def test_memorial_exodus_17_16_conjecture_not_presented_as_mt(self) -> None:
        d = copy.deepcopy(self.baseline)
        r = next(x for x in d["records"] if x["id"] == "nissi")
        r["attestations"][2]["surface"] = "כִּי-יָד עַל-נֵס יָהּ"
        self.assertTrue(any("secret-hand and conjecture" in e for e in validate_memorial_attestations(d, self.memorial_contract)))

    def test_memorial_lxx_exodus_cannot_inherit_sblgnt_license(self) -> None:
        d = copy.deepcopy(self.baseline)
        r = next(x for x in d["records"] if x["id"] == "nissi")
        r["attestations"][1]["rightsState"] = "PUBLICATION_ELIGIBLE"
        self.assertTrue(any("Rahlfs Exodus17 reuse gate" in e for e in validate_memorial_attestations(d, self.memorial_contract)))

    def test_memorial_judges_speech_not_same_as_altar_name(self) -> None:
        d = copy.deepcopy(self.baseline)
        r = next(x for x in d["records"] if x["id"] == "shalom")
        r["attestations"][0]["namedObject"] = "altar"
        self.assertTrue(any("Judg6 peace speech" in e for e in validate_memorial_attestations(d, self.memorial_contract)))

    def test_memorial_baal_altar_does_not_become_gideon_altar(self) -> None:
        d = copy.deepcopy(self.baseline)
        r = next(x for x in d["records"] if x["id"] == "shalom")
        r["attestations"][2]["namedObject"] = "altar"
        self.assertTrue(any("Baal altar conflated" in e for e in validate_memorial_attestations(d, self.memorial_contract)))

    def test_memorial_healer_addressee_is_second_masculine_singular(self) -> None:
        d = copy.deepcopy(self.baseline)
        r = next(x for x in d["records"] if x["id"] == "rapha")
        r["attestations"][0]["morphology"] = "2mp plural"
        self.assertTrue(any("healer 2ms" in e for e in validate_memorial_attestations(d, self.memorial_contract)))

    def test_memorial_sanctifier_addressee_is_second_masculine_plural(self) -> None:
        d = copy.deepcopy(self.baseline)
        r = next(x for x in d["records"] if x["id"] == "mekoddishkem")
        r["attestations"][0]["morphology"] = "1cs first person"
        self.assertTrue(any("sanctification 2mp" in e for e in validate_memorial_attestations(d, self.memorial_contract)))

    def test_memorial_psalm_shepherd_does_not_inherit_hagar_seeing_root(self) -> None:
        d = copy.deepcopy(self.baseline)
        r = next(x for x in d["records"] if x["id"] == "ro-i")
        r["attestations"][0]["root"] = "ראה"
        self.assertTrue(any("seeing/shepherd roots" in e for e in validate_memorial_attestations(d, self.memorial_contract)))

    def test_memorial_john_christological_speaker_not_psalmist(self) -> None:
        d = copy.deepcopy(self.baseline)
        r = next(x for x in d["records"] if x["id"] == "ro-i")
        r["attestations"][1]["namingActor"] = "psalmist"
        self.assertTrue(any("NT speaker/intertext" in e for e in validate_memorial_attestations(d, self.memorial_contract)))

    def test_memorial_cannot_delete_whole_shepherd_occurrence_set(self) -> None:
        d = copy.deepcopy(self.baseline)
        r = next(x for x in d["records"] if x["id"] == "ro-i")
        r["attestations"] = []
        self.assertTrue(any("16 unique reviewed contexts" in e for e in validate_memorial_attestations(d, self.memorial_contract)))

    def test_memorial_contract_locus_ids_cannot_be_swapped(self) -> None:
        c = copy.deepcopy(self.memorial_contract)
        c["lockedAttestations"][0]["locusId"] = c["lockedAttestations"][1]["locusId"]
        self.assertTrue(any("duplicate contract locus" in e for e in validate_memorial_attestations(self.baseline, c)))

    def test_memorial_contract_cannot_drop_source_locator_schema(self) -> None:
        c = copy.deepcopy(self.memorial_contract)
        c["lockedFields"].remove("sourceUrl")
        self.assertTrue(any("contract weakened" in e for e in validate_memorial_attestations(self.baseline, c)))

    def test_memorial_source_rights_are_specific_to_rahlfs_greek(self) -> None:
        d = copy.deepcopy(self.sources)
        r = next(x for x in d["records"] if x["id"] == "SRC-RAHLFS-EXODUS17")
        r["rightsState"] = "PUBLICATION_ELIGIBLE"
        self.assertTrue(any("Rahlfs Exodus17 digital LXX" in e for e in validate_source_access(d)))

    def test_net_exodus_17_banner_textual_emendation_stays_conjecture(self) -> None:
        d = copy.deepcopy(self.sources)
        r = next(x for x in d["records"] if x["id"] == "SRC-NET-EXODUS17")
        r["forbiddenUse"] = "Publisher fully approves literal textual proof"
        self.assertTrue(any("textual emendation" in e for e in validate_source_access(d)))


    def test_abba_mark_prayer_speaker_cannot_be_paul(self) -> None:
        d = copy.deepcopy(self.baseline)
        r = next(x for x in d["records"] if x["id"] == "abba")
        r["attestations"][0]["speaker"] = "Paul"
        self.assertTrue(any("changed speaker" in e for e in validate_speech_intertext(d, self.speech_contract)))

    def test_abba_romans_cannot_exchange_our_cry_with_spirit_agent(self) -> None:
        d = copy.deepcopy(self.baseline)
        r = next(x for x in d["records"] if x["id"] == "abba")
        r["attestations"][1]["agentOfCry"] = "Spirit of Son, κρᾶζον"
        self.assertTrue(any("crying agents collapsed" in e for e in validate_speech_intertext(d, self.speech_contract)))

    def test_abba_galatians_spirit_cries_not_paul_plural(self) -> None:
        d = copy.deepcopy(self.baseline)
        r = next(x for x in d["records"] if x["id"] == "abba")
        r["attestations"][2]["agentOfCry"] = "we, κράζομεν"
        self.assertTrue(any("crying agents collapsed" in e for e in validate_speech_intertext(d, self.speech_contract)))

    def test_abba_is_aramaic_transliteration_in_greek_not_hebrew_mss(self) -> None:
        d = copy.deepcopy(self.baseline)
        r = next(x for x in d["records"] if x["id"] == "abba")
        r["attestations"][0]["languageOrigin"] = "ORIGINAL_HEBREW_MANUSCRIPT"
        self.assertTrue(any("Greek script versus Aramaic" in e for e in validate_speech_intertext(d, self.speech_contract)))

    def test_abba_thgnt_accents_do_not_replace_sblgnt_surface(self) -> None:
        d = copy.deepcopy(self.baseline)
        r = next(x for x in d["records"] if x["id"] == "abba")
        r["attestations"][0]["surface"] = "ἀββᾶ ὁ πατήρ"
        self.assertTrue(any("SBLGNT Abba original Greek" in e for e in validate_speech_intertext(d, self.speech_contract)))

    def test_abba_editorial_accent_differences_remain_labeled(self) -> None:
        d = copy.deepcopy(self.baseline)
        r = next(x for x in d["records"] if x["id"] == "abba")
        r["printedOrthography"]["thgnt"] = "Αββα"
        self.assertTrue(any("publisher-specific accents" in e for e in validate_speech_intertext(d, self.speech_contract)))

    def test_john9_ego_eimi_spoken_by_nondivine_healed_man(self) -> None:
        d = copy.deepcopy(self.baseline)
        r = next(x for x in d["records"] if x["id"] == "ego-eimi")
        rx = next(x for x in r["attestations"] if x["locusId"] == "ego-john9-human")
        rx["isDivineDesignation"] = True
        self.assertTrue(any("ordinary human ego eimi" in e for e in validate_speech_intertext(d, self.speech_contract)))

    def test_john9_speaker_cannot_be_replaced_by_jesus(self) -> None:
        d = copy.deepcopy(self.baseline)
        r = next(x for x in d["records"] if x["id"] == "ego-eimi")
        rx = next(x for x in r["attestations"] if x["locusId"] == "ego-john9-human")
        rx["speaker"] = "Jesus"
        self.assertTrue(any("ordinary human ego eimi" in e for e in validate_speech_intertext(d, self.speech_contract)))

    def test_john8_preabraham_context_not_ordinary_identity(self) -> None:
        d = copy.deepcopy(self.baseline)
        r = next(x for x in d["records"] if x["id"] == "ego-eimi")
        rx = next(x for x in r["attestations"] if x["locusId"] == "ego-john8-preabraham")
        rx["claimScope"] = "just saying I am the same man"
        self.assertTrue(any("before-Abraham" in e for e in validate_speech_intertext(d, self.speech_contract)))

    def test_lxx_ex3_14_full_ho_on_not_removed_to_force_john8_quote(self) -> None:
        d = copy.deepcopy(self.baseline)
        r = next(x for x in d["records"] if x["id"] == "ehyeh")
        rx = next(x for x in r["attestations"] if x["locusId"] == "ehyeh-ex3-greek")
        rx["surface"] = "Ἐγώ εἰμι"
        self.assertTrue(any("LXX Exodus 3:14 full" in e for e in validate_speech_intertext(d, self.speech_contract)))

    def test_lxx_ex3_cannot_inherit_sblgnt_ccby_license(self) -> None:
        d = copy.deepcopy(self.baseline)
        r = next(x for x in d["records"] if x["id"] == "ehyeh")
        rx = next(x for x in r["attestations"] if x["locusId"] == "ehyeh-ex3-greek")
        rx["rightsState"] = "PUBLICATION_ELIGIBLE"
        self.assertTrue(any("license / contextual relation" in e for e in validate_speech_intertext(d, self.speech_contract)))

    def test_exodus3_12_promise_vs_exodus3_14_self_declaration(self) -> None:
        d = copy.deepcopy(self.baseline)
        r = next(x for x in d["records"] if x["id"] == "ehyeh")
        rx = next(x for x in r["attestations"] if x["locusId"] == "ehyeh-ex3-promise")
        rx["surface"] = "אֶהְיֶה אֲשֶׁר אֶהְיֶה"
        self.assertTrue(any("Hebrew promise/naming distinction" in e for e in validate_speech_intertext(d, self.speech_contract)))

    def test_speech_intertext_contract_cannot_drop_speaker(self) -> None:
        c = copy.deepcopy(self.speech_contract)
        c["lockedFields"].remove("speaker")
        self.assertTrue(any("source/speaker fields removed" in e for e in validate_speech_intertext(self.baseline, c)))

    def test_speech_intertext_dropped_loci_fail_closed(self) -> None:
        d = copy.deepcopy(self.baseline)
        r = next(x for x in d["records"] if x["id"] == "ego-eimi")
        r["attestations"] = []
        self.assertTrue(any("12 unique locked" in e for e in validate_speech_intertext(d, self.speech_contract)))

    def test_barr_full_article_not_falsely_claimed_read(self) -> None:
        d = copy.deepcopy(self.sources)
        r = next(x for x in d["records"] if x["id"] == "SRC-BARR-ABBA-1988")
        r["accessState"] = "FULL_OBJECT_VERIFIED"
        self.assertTrue(any("Barr paywalled full article" in e for e in validate_source_access(d)))

    def test_rahlfs_exodus3_license_not_from_sblgnt(self) -> None:
        d = copy.deepcopy(self.sources)
        r = next(x for x in d["records"] if x["id"] == "SRC-RAHLFS-EXODUS3")
        r["rightsState"] = "PUBLICATION_ELIGIBLE"
        self.assertTrue(any("publisher LXX full" in e for e in validate_source_access(d)))

    def test_sblgnt_john_9_human_source_role_cannot_be_erased(self) -> None:
        d = copy.deepcopy(self.sources)
        r = next(x for x in d["records"] if x["id"] == "SRC-SBLGNT-JOHN-EGO")
        r["supportedUse"] = "John8:58 divine name in every utterance"
        self.assertTrue(any("nondivine John9:9" in e for e in validate_source_access(d)))


    def test_extension_yah_psalm68_bet_prefix_cannot_be_erased(self) -> None:
        d = copy.deepcopy(self.extension)
        x = next(r for r in d["records"] if r["id"] == "yah")
        x["attestations"][1]["surface"] = "יָהּ שְׁמוֹ"
        self.assertTrue(any("Psalm68 bet prefix" in e for e in validate_extension_attestations(d, self.extension_contract)))

    def test_extension_yah_psalm68_mt_vs_english_numbering(self) -> None:
        d = copy.deepcopy(self.extension)
        x = next(r for r in d["records"] if r["id"] == "yah")
        x["attestations"][1]["numbering"]["mt"] = "Psalms 68:4"
        self.assertTrue(any("Psalm68 versification" in e for e in validate_extension_attestations(d, self.extension_contract)))

    def test_extension_psalm68_net_conjecture_is_not_printed_mt(self) -> None:
        d = copy.deepcopy(self.extension)
        x = next(r for r in d["records"] if r["id"] == "yah")
        x["attestations"][1]["textualConjecture"] = "MT conclusively reads כִּי יָהּ שְׁמוֹ"
        self.assertTrue(any("conjecture promoted to MT" in e for e in validate_extension_attestations(d, self.extension_contract)))

    def test_extension_eloah_deut32_rejected_object_not_jeshurun_subject(self) -> None:
        d = copy.deepcopy(self.extension)
        x = next(r for r in d["records"] if r["id"] == "eloah")
        x["attestations"][0]["grammaticalActor"] = "Eloah"
        self.assertTrue(any("Eloah object of Jeshurun" in e for e in validate_extension_attestations(d, self.extension_contract)))

    def test_extension_daniel_2_aramaic_cannot_be_labelled_hebrew(self) -> None:
        d = copy.deepcopy(self.extension)
        x = next(r for r in d["records"] if r["id"] == "elah-shmaya")
        x["attestations"][0]["language"] = "hebrew"
        self.assertTrue(any("Daniel2 Aramaic language" in e for e in validate_extension_attestations(d, self.extension_contract)))

    def test_extension_daniel_2_19_prefix_lamed_is_preserved(self) -> None:
        d = copy.deepcopy(self.extension)
        x = next(r for r in d["records"] if r["id"] == "elah-shmaya")
        x["attestations"][1]["surface"] = "אֱלָהּ שְׁמַיָּא"
        self.assertTrue(any("Aramaic language/lamed prefix" in e for e in validate_extension_attestations(d, self.extension_contract)))

    def test_extension_daniel_2_pagan_gods_negative_control_not_lost(self) -> None:
        d = copy.deepcopy(self.extension)
        x = next(r for r in d["records"] if r["id"] == "elah-shmaya")
        x["negativeControls"] = [y for y in x["negativeControls"] if y["verse"] != "Daniel 2:11"]
        self.assertTrue(any("pagan gods vs God" in e for e in validate_extension_attestations(d, self.extension_contract)))

    def test_extension_daniel_2_28_god_in_heaven_is_not_same_surface(self) -> None:
        d = copy.deepcopy(self.extension)
        x = next(r for r in d["records"] if r["id"] == "elah-shmaya")
        x["negativeControls"][1]["surface"] = "אֱלָהּ שְׁמַיָּא"
        self.assertTrue(any("pagan gods vs God" in e for e in validate_extension_attestations(d, self.extension_contract)))

    def test_extension_psalm_42_bet_not_substituted_for_lamed(self) -> None:
        d = copy.deepcopy(self.extension)
        x = next(r for r in d["records"] if r["id"] == "el-hay")
        x["attestations"][0]["prefixOnEl"] = "בְּ"
        self.assertTrue(any("Psalm42 lamed" in e for e in validate_extension_attestations(d, self.extension_contract)))

    def test_extension_psalm_42_3_mt_vs_english_42_2(self) -> None:
        d = copy.deepcopy(self.extension)
        x = next(r for r in d["records"] if r["id"] == "el-hay")
        x["attestations"][0]["numbering"]["commonEnglish"] = "Psalms 42:3"
        self.assertTrue(any("Psalm42 lamed and verse numbering" in e for e in validate_extension_attestations(d, self.extension_contract)))

    def test_extension_isaiah_63_our_father_not_novel_aramaic_abba(self) -> None:
        d = copy.deepcopy(self.extension)
        x = next(r for r in d["records"] if r["id"] == "avinu")
        x["attestations"][0]["language"] = "aramaic"
        self.assertTrue(any("Hebrew corporate Father prayer" in e for e in validate_extension_attestations(d, self.extension_contract)))

    def test_extension_psalm_27_poetic_light_not_named_personal_name(self) -> None:
        d = copy.deepcopy(self.extension)
        x = next(r for r in d["records"] if r["id"] == "yhwh-ori")
        x["attestations"][0]["namingActInVerse"] = True
        self.assertTrue(any("poetic light falsely turned" in e for e in validate_extension_attestations(d, self.extension_contract)))

    def test_extension_psalm_27_stronghold_poetic_parallel_preserved(self) -> None:
        d = copy.deepcopy(self.extension)
        x = next(r for r in d["records"] if r["id"] == "yhwh-ori")
        x["attestations"][0]["linkedPoeticMetaphor"] = "יְהוָה אוֹרִי"
        self.assertTrue(any("poetic light falsely turned" in e for e in validate_extension_attestations(d, self.extension_contract)))

    def test_extension_deuteronomy_32_faithful_god_and_rock_parallel(self) -> None:
        d = copy.deepcopy(self.extension)
        x = next(r for r in d["records"] if r["id"] == "el-emunah")
        x["attestations"][0]["contextParallel"] = "no rock"
        self.assertTrue(any("faithful God separated from Rock" in e for e in validate_extension_attestations(d, self.extension_contract)))

    def test_extension_exodus_34_moral_descriptors_not_each_own_name(self) -> None:
        d = copy.deepcopy(self.extension)
        x = next(r for r in d["records"] if r["id"] == "el-rahum-hannun")
        x["attestations"][0]["qualifier"] = "EACH_ADJECTIVE_PROVEN_TO_BE_A_PERSONAL_NAME"
        self.assertTrue(any("Exodus34 naming proclamation" in e for e in validate_extension_attestations(d, self.extension_contract)))

    def test_extension_luke1_32_gabriel_must_remain_speaker(self) -> None:
        d = copy.deepcopy(self.extension)
        x = next(r for r in d["records"] if r["id"] == "kyrios-ho-theos")
        x["attestations"][0]["narrativeSpeaker"] = "Jesus"
        self.assertTrue(any("Luke1:32 Gabriel" in e for e in validate_extension_attestations(d, self.extension_contract)))

    def test_extension_luke1_32_god_agent_jesus_dative_recipient(self) -> None:
        d = copy.deepcopy(self.extension)
        x = next(r for r in d["records"] if r["id"] == "kyrios-ho-theos")
        x["attestations"][0]["recipient"] = "YHWH"
        self.assertTrue(any("Luke1:32 Gabriel/Lord God/Jesus" in e for e in validate_extension_attestations(d, self.extension_contract)))

    def test_extension_luke_thgnt_copyright_not_sblgnt_licensed(self) -> None:
        d = copy.deepcopy(self.extension)
        x = next(r for r in d["records"] if r["id"] == "kyrios-ho-theos")
        x["attestations"][0]["rightsState"] = "PUBLICATION_ELIGIBLE"
        self.assertTrue(any("THGNT rights conflated" in e for e in validate_extension_attestations(d, self.extension_contract)))

    def test_extension_john10_good_shepherd_explicit_predicate(self) -> None:
        d = copy.deepcopy(self.extension)
        x = next(r for r in d["records"] if r["id"] == "poimen-ho-kalos")
        x["attestations"][0]["syntax"] = "ABSOLUTE_EGO_EIMI_WITHOUT_PREDICATE"
        self.assertTrue(any("John predicate silently made absolute" in e for e in validate_extension_attestations(d, self.extension_contract)))

    def test_extension_john10_14_ego_eimi_case_remains_edition_specific(self) -> None:
        d = copy.deepcopy(self.extension)
        x = next(r for r in d["records"] if r["id"] == "poimen-ho-kalos")
        x["attestations"][1]["fullClause"] = "Ἐγώ εἰμι ὁ ποιμὴν ὁ καλός"
        self.assertTrue(any("John10 shepherd verses" in e for e in validate_extension_attestations(d, self.extension_contract)))

    def test_extension_john11_resurrection_and_life_not_solo_word(self) -> None:
        d = copy.deepcopy(self.extension)
        x = next(r for r in d["records"] if r["id"] == "anastasis-zoe")
        x["attestations"][0]["fullClause"] = "Ἐγώ εἰμι ἡ ἀνάστασις"
        self.assertTrue(any("John11 both resurrection and life" in e for e in validate_extension_attestations(d, self.extension_contract)))

    def test_extension_independent_contract_cannot_drop_provenance_field(self) -> None:
        c = copy.deepcopy(self.extension_contract)
        c["lockedFields"].remove("sourceUrl")
        self.assertTrue(any("source/speaker contract weakened" in e for e in validate_extension_attestations(self.extension, c)))

    def test_extension_dropping_14_contexts_fails_closed(self) -> None:
        d = copy.deepcopy(self.extension)
        x = next(r for r in d["records"] if r["id"] == "anastasis-zoe")
        x["attestations"] = []
        self.assertTrue(any("exactly 14 unique" in e for e in validate_extension_attestations(d, self.extension_contract)))

    def test_suchard_article_ccby_does_not_imply_lexical_consensus(self) -> None:
        d = copy.deepcopy(self.sources)
        x = next(r for r in d["records"] if r["id"] == "SRC-SUCHARD-ELOHIM-2025")
        x["evidenceClass"] = "A1"
        self.assertTrue(any("Suchard article CC BY" in e for e in validate_source_access(d)))

    def test_suchard_ccby_must_remain_article_only(self) -> None:
        d = copy.deepcopy(self.sources)
        x = next(r for r in d["records"] if r["id"] == "SRC-SUCHARD-ELOHIM-2025")
        x["licenseScope"] = "ALL_OTHER_BIBLICAL_TRANSLATIONS"
        self.assertTrue(any("Suchard article CC BY" in e for e in validate_source_access(d)))

    def test_suchard_article_cannot_be_reset_to_unverified_rights(self) -> None:
        d = copy.deepcopy(self.sources)
        x = next(r for r in d["records"] if r["id"] == "SRC-SUCHARD-ELOHIM-2025")
        x["rightsState"] = "RIGHTS_UNKNOWN"
        self.assertTrue(any("Suchard article CC BY" in e for e in validate_source_access(d)))

    def test_jbq_yah_article_not_auto_primary_or_open_license(self) -> None:
        d = copy.deepcopy(self.sources)
        x = next(r for r in d["records"] if r["id"] == "SRC-JBQ-YAH-2014")
        x["rightsState"] = "PUBLICATION_ELIGIBLE"
        self.assertTrue(any("JBQ Yah bibliography" in e for e in validate_source_access(d)))

    def test_net_psalm68_emendation_not_a_cited_manuscript(self) -> None:
        d = copy.deepcopy(self.sources)
        x = next(r for r in d["records"] if r["id"] == "SRC-NET-PS68")
        x["supportedUse"] = "MT already reads conjectural ki Yah"
        self.assertTrue(any("conjectural NET Psalm68" in e for e in validate_source_access(d)))


    def test_core_yhwh_exodus3_divine_name_marker_cannot_disappear(self) -> None:
        d = copy.deepcopy(self.baseline)
        r = next(x for x in d["records"] if x["id"] == "yhwh")
        r["attestations"][0]["nameClaim"] = "not a name"
        self.assertTrue(any("Exodus3 YHWH divine personal name" in e for e in validate_core_name_lexeme(d, self.core_contract)))

    def test_core_yhwh_ex3_ehyeh_1cs_distinct_from_full_name(self) -> None:
        d = copy.deepcopy(self.baseline)
        r = next(x for x in d["records"] if x["id"] == "yhwh")
        r["attestations"][0]["relatedButDistinct"] = "both words identical letters"
        self.assertTrue(any("confused with Ehyeh" in e for e in validate_core_name_lexeme(d, self.core_contract)))

    def test_core_yhwh_ex6_self_declaration_not_ehyeh_substitution(self) -> None:
        d = copy.deepcopy(self.baseline)
        r = next(x for x in d["records"] if x["id"] == "yhwh")
        r["attestations"][1]["surface"] = "אֲנִי אֶהְיֶה"
        self.assertTrue(any("Exodus6:2 self-revelation" in e for e in validate_core_name_lexeme(d, self.core_contract)))

    def test_core_ex6_name_known_to_patriarchs_has_contextual_issue(self) -> None:
        d = copy.deepcopy(self.baseline)
        r = next(x for x in d["records"] if x["id"] == "yhwh")
        r["attestations"][1]["nextVerseQualifier"] = "simple unequivocal pronunciation problem"
        self.assertTrue(any("6:3 known-to-patriarchs nuance" in e for e in validate_core_name_lexeme(d, self.core_contract)))

    def test_core_ex15_yhwh_name_hymn_is_not_direct_divine_speech(self) -> None:
        d = copy.deepcopy(self.baseline)
        r = next(x for x in d["records"] if x["id"] == "yhwh")
        r["attestations"][2]["speaker"] = "God speaking first person"
        self.assertTrue(any("Exodus15 YHWH name hymn" in e for e in validate_core_name_lexeme(d, self.core_contract)))

    def test_core_el_ex34_attribute_phrase_with_proclaimed_yhwh(self) -> None:
        d = copy.deepcopy(self.baseline)
        r = next(x for x in d["records"] if x["id"] == "el")
        r["attestations"][0]["contextualClause"] = "El as unique distinct deity"
        self.assertTrue(any("El attribute phrases" in e for e in validate_core_name_lexeme(d, self.core_contract)))

    def test_core_el_deut32_faithful_rock_parallel_preserved(self) -> None:
        d = copy.deepcopy(self.baseline)
        r = next(x for x in d["records"] if x["id"] == "el")
        r["attestations"][1]["poeticParallel"] = "not the Rock"
        self.assertTrue(any("El attribute phrases" in e for e in validate_core_name_lexeme(d, self.core_contract)))

    def test_core_el_deut32_strange_god_cannot_be_identified_as_yhwh(self) -> None:
        d = copy.deepcopy(self.baseline)
        r = next(x for x in d["records"] if x["id"] == "el")
        r["attestations"][2]["isYHWH"] = True
        self.assertTrue(any("foreign or putative god wrongly" in e for e in validate_core_name_lexeme(d, self.core_contract)))

    def test_core_el_deut32_strange_god_negation_must_remain(self) -> None:
        d = copy.deepcopy(self.baseline)
        r = next(x for x in d["records"] if x["id"] == "el")
        r["attestations"][2]["negationClause"] = "YHWH and a second true god"
        self.assertTrue(any("negative El clauses deleted" in e for e in validate_core_name_lexeme(d, self.core_contract)))

    def test_core_el_isa43_10_formed_god_negation_must_remain(self) -> None:
        d = copy.deepcopy(self.baseline)
        r = next(x for x in d["records"] if x["id"] == "el")
        r["attestations"][3]["negationClause"] = "I was formed"
        self.assertTrue(any("negative El clauses deleted" in e for e in validate_core_name_lexeme(d, self.core_contract)))

    def test_core_el_isa43_10_other_god_not_yhwh(self) -> None:
        d = copy.deepcopy(self.baseline)
        r = next(x for x in d["records"] if x["id"] == "el")
        r["attestations"][3]["referentClass"] = "YHWH"
        self.assertTrue(any("foreign or putative god wrongly" in e for e in validate_core_name_lexeme(d, self.core_contract)))

    def test_core_el_isa43_12_positive_divine_self_predication(self) -> None:
        d = copy.deepcopy(self.baseline)
        r = next(x for x in d["records"] if x["id"] == "el")
        r["attestations"][4]["isYHWH"] = False
        self.assertTrue(any("positive El divine self-predication" in e for e in validate_core_name_lexeme(d, self.core_contract)))

    def test_core_referents_not_collapsible_to_a_single_global_el_name(self) -> None:
        d = copy.deepcopy(self.baseline)
        r = next(x for x in d["records"] if x["id"] == "el")
        for item in r["attestations"]:
            item["referentClass"] = "YHWH"
        self.assertTrue(any("foreign or putative god wrongly" in e for e in validate_core_name_lexeme(d, self.core_contract)))

    def test_core_source_contract_rejects_deleted_exact_verse(self) -> None:
        d = copy.deepcopy(self.baseline)
        r = next(x for x in d["records"] if x["id"] == "el")
        r["attestations"].pop()
        self.assertTrue(any("eight unique YHWH/El contexts" in e for e in validate_core_name_lexeme(d, self.core_contract)))

    def test_core_contract_cannot_drop_speaker_and_referent_lock(self) -> None:
        c = copy.deepcopy(self.core_contract)
        c["lockedFields"].remove("referentClass")
        self.assertTrue(any("referent lock weakened" in e for e in validate_core_name_lexeme(self.baseline, c)))

    def test_full_coverage_cannot_lose_yhwh_baseline_attestations(self) -> None:
        d = copy.deepcopy(self.baseline)
        r = next(x for x in d["records"] if x["id"] == "yhwh")
        r["attestations"] = []
        self.assertTrue(any("Arena/yhwh lacks independently" in e for e in validate_full_coverage(d, self.extension)))

    def test_full_coverage_cannot_lose_unrelated_extension_attestations(self) -> None:
        d = copy.deepcopy(self.extension)
        r = next(x for x in d["records"] if x["id"] == "anastasis-zoe")
        r["attestations"] = []
        self.assertTrue(any("extension/anastasis-zoe lacks" in e for e in validate_full_coverage(self.baseline, d)))

    def test_full_coverage_not_product_approval_after_one_form_checked(self) -> None:
        d = copy.deepcopy(self.extension)
        r = next(x for x in d["records"] if x["id"] == "yah")
        r["publicationState"] = "PROMOTE"
        self.assertTrue(any("extension/yah unreviewed Product promotion" in e for e in validate_full_coverage(self.baseline, d)))


    def test_speech_contract_cannot_drop_exodus_moses_addressee(self) -> None:
        c = copy.deepcopy(self.speech_contract)
        row = next(x for x in c["lockedAttestations"] if x["locusId"] == "ehyeh-ex3-greek")
        row.pop("addressee")
        self.assertTrue(any("divine referent/addressee error in locked contract" in e
                            for e in validate_speech_intertext(self.baseline, c)))

    def test_wrong_referent_in_both_ledger_and_contract_still_fails(self) -> None:
        d = copy.deepcopy(self.baseline)
        c = copy.deepcopy(self.speech_contract)
        row = next(x for x in d["records"] if x["id"] == "ehyeh")
        for occ in row["attestations"]:
            occ["referent"] = "Moses"
        for occ in c["lockedAttestations"]:
            if occ.get("baselineId") == "ehyeh":
                occ["referent"] = "Moses"
        self.assertTrue(any("divine referent/addressee error" in e
                            for e in validate_speech_intertext(d, c)))


    def test_liebermann_accepted_manuscript_cannot_be_misreported_as_critical_apparatus(self) -> None:
        d=copy.deepcopy(self.sources)
        src=next(r for r in d["records"] if r["id"]=="SRC-VT-LIEBERMANN-JEREMIAH-2023")
        src["criticalEditionCollated"]=True
        self.assertTrue(any("falsely claims edition collation" in e for e in validate_source_access(d)))

    def test_liebermann_2022_online_publication_not_same_as_2023_journal_issue(self) -> None:
        d=copy.deepcopy(self.sources)
        src=next(r for r in d["records"] if r["id"]=="SRC-VT-LIEBERMANN-JEREMIAH-2023")
        src["firstOnlineYear"]=2023
        self.assertTrue(any("Liebermann issue/online year" in e for e in validate_source_access(d)))

    def test_liebermann_reuse_rights_not_automatically_cleared(self) -> None:
        d=copy.deepcopy(self.sources)
        src=next(r for r in d["records"] if r["id"]=="SRC-VT-LIEBERMANN-JEREMIAH-2023")
        src["rightsState"]="PUBLICATION_ELIGIBLE"
        self.assertTrue(any("Liebermann issue/online year" in e for e in validate_source_access(d)))


    def test_revelation_net_note_must_not_claim_manuscript_collation(self) -> None:
        d=copy.deepcopy(self.sources)
        row=next(x for x in d["records"] if x["id"]=="SRC-NET-REV1-8")
        row["criticalEditionCollated"]=True
        self.assertTrue(any("falsely claims edition collation" in e for e in validate_source_access(d)))

    def test_revelation_tabb_commentary_rights_not_waived(self) -> None:
        d=copy.deepcopy(self.sources)
        row=next(x for x in d["records"] if x["id"]=="SRC-TABB-REVELATION22")
        row["rightsState"]="PUBLICATION_ELIGIBLE"
        self.assertTrue(any("Revelation secondary source falsely promoted" in e for e in validate_source_access(d)))

    def test_revelation_edition_note_not_mislabeled_as_primary_text(self) -> None:
        d=copy.deepcopy(self.sources)
        row=next(x for x in d["records"] if x["id"]=="SRC-NET-REV1-8")
        row["sourceRole"]="GREEK_TEXT_SURFACE_ONLY"
        self.assertTrue(any("source relevance/role changed" in e for e in validate_source_access(d)))

    def test_deir_alla_source_roles_are_closed_and_counted(self) -> None:
        self.assertEqual([], validate_source_access(self.sources))
        d = copy.deepcopy(self.sources)
        d["records"].append(copy.deepcopy(d["records"][-1]))
        self.assertTrue(any("duplicate id" in e for e in validate_source_access(d)))

    def test_deir_alla_cc_by_sa_visual_license_is_immutable(self) -> None:
        d = copy.deepcopy(self.sources)
        row = next(x for x in d["records"] if x["id"] == "SRC-IMG-DEIRALLA-DISDERO-2020")
        row["licenseUrl"] = "https://creativecommons.org/licenses/by/4.0/"
        self.assertTrue(any("image license or attribution evidence" in e for e in validate_source_access(d)))

    def test_deir_alla_cc0_visual_cannot_inherit_rights_of_other_photo(self) -> None:
        d = copy.deepcopy(self.sources)
        row = next(x for x in d["records"] if x["id"] == "SRC-IMG-DEIRALLA-LEIDEN-POSTER-1989")
        row["url"] = "https://www.worldhistory.org/image/10089/the-balam-text-from-deir-alla/"
        self.assertTrue(any("image license or attribution evidence" in e for e in validate_source_access(d)))

    def test_deir_alla_museum_photo_cannot_become_publication_eligible(self) -> None:
        d = copy.deepcopy(self.sources)
        row = next(x for x in d["records"] if x["id"] == "SRC-IMG-DEIRALLA-AMIN-WHE-2019")
        row["rightsState"] = "PUBLICATION_ELIGIBLE"
        self.assertTrue(any("Deir Alla access/rights/locator" in e for e in validate_source_access(d)))

    def test_deir_alla_1976_editio_princeps_not_claimed_read(self) -> None:
        d = copy.deepcopy(self.sources)
        row = next(x for x in d["records"] if x["id"] == "SRC-DEIRALLA-HOFTIJZER-VANDERKOOIJ-1976-CONTENTS")
        row["accessState"] = "FULL_OBJECT_VERIFIED"
        self.assertTrue(any("Deir Alla access/rights/locator" in e for e in validate_source_access(d)))

    def test_deir_alla_2025_noncommercial_license_guard(self) -> None:
        d = copy.deepcopy(self.sources)
        row = next(x for x in d["records"] if x["id"] == "SRC-TSOLIN-ORIEKHOVA-DEIRALLA-2025")
        row["licenseScope"] = "unrestricted"
        self.assertTrue(any("noncommercial source license omitted" in e for e in validate_source_access(d)))

    def test_deir_alla_acor_non_balaam_identity_preserved(self) -> None:
        d = copy.deepcopy(self.sources)
        row = next(x for x in d["records"] if x["id"] == "SRC-IMG-DEIRALLA-ACOR-LAPP-1987-NOT-BALAAM")
        row["title"] = "ACOR ancient Balaam inscription"
        row["sourceObjectState"] = "A photograph of Balaam inscription"
        self.assertTrue(any("misidentified as Balaam" in e for e in validate_source_access(d)))


    def test_deir_alla_livius_actual_museum_photo_cc0_is_source_specific(self) -> None:
        d = copy.deepcopy(self.sources)
        row = next(x for x in d["records"] if x["id"] == "SRC-IMG-DEIRALLA-LENDERING-LIVIUS-CC0")
        row["license"] = "CC BY-SA 4.0"
        self.assertTrue(any("Deir Alla image license or attribution evidence" in e for e in validate_source_access(d)))
        row["license"] = "CC0 1.0"
        row["rightsState"] = "PERMISSION_REQUIRED"
        self.assertTrue(any("Deir Alla access/rights/locator status changed" in e for e in validate_source_access(d)))

    def test_deir_alla_lemaire_2021_source_is_not_claimed_fully_read(self) -> None:
        d = copy.deepcopy(self.sources)
        row = next(x for x in d["records"] if x["id"] == "SRC-LEMAIRE-DEIRALLA-SCRIBAL-2021")
        row["accessState"] = "FULL_OBJECT_VERIFIED"
        self.assertTrue(any("Deir Alla access/rights/locator" in e for e in validate_source_access(d)))

    def test_deir_alla_lemaire_2021_old_copy_is_not_proven(self) -> None:
        d = copy.deepcopy(self.sources)
        row = next(x for x in d["records"] if x["id"] == "SRC-LEMAIRE-DEIRALLA-SCRIBAL-2021")
        row["hypothesisStatus"] = "ORIGINAL_10TH_CENTURY_DOCUMENT_FOUND"
        self.assertTrue(any("historical copy/dating claim falsely promoted" in e for e in validate_source_access(d)))

    def test_deir_alla_hackett_museum_visit_is_not_our_autopsy(self) -> None:
        d = copy.deepcopy(self.sources)
        row = next(x for x in d["records"] if x["id"] == "SRC-HACKETT-DEIRALLA-FIRSTHAND-1986")
        row["autopsyBoundary"] = "ANCIENT_PLASTER_DIRECTLY_COLLATED_BY_RESEARCH_2026"
        self.assertTrue(any("firsthand material scope overclaimed" in e for e in validate_source_access(d)))

    def test_deir_alla_hackett_biblical_revocalization_stays_disputed(self) -> None:
        d = copy.deepcopy(self.sources)
        row = next(x for x in d["records"] if x["id"] == "SRC-HACKETT-DEIRALLA-FIRSTHAND-1986")
        row["hypothesisStatus"] = "BIBLICAL_SHADDAYYIM_READING_ESTABLISHED"
        self.assertTrue(any("scholarly hypothesis" in e for e in validate_source_access(d)))

    def test_deir_alla_lemaire1984_one_page_cannot_be_promoted_to_complete_book(self) -> None:
        d = copy.deepcopy(self.sources)
        row = next(x for x in d["records"] if x["id"] == "SRC-LEMAIRE-REVIEW-HACKETT-1984-P142")
        row["accessState"] = "FULL_OBJECT_VERIFIED"
        self.assertTrue(any("Deir Alla access/rights/locator" in e for e in validate_source_access(d)))

    def test_deir_alla_lemaire1984_fragment_and_dating_claim_must_stay_disputed(self) -> None:
        d = copy.deepcopy(self.sources)
        row = next(x for x in d["records"] if x["id"] == "SRC-LEMAIRE-REVIEW-HACKETT-1984-P142")
        row["comparisonScope"] = "CERTAIN_CHRONOLOGY_AND_FINAL_PLACEMENT_OF_ALL_FRAGMENTS"
        self.assertTrue(any("one-page source scope" in e for e in validate_source_access(d)))

    def test_deir_alla_adaj1979_phase_IX_stays_preliminary_not_c14_absolute(self) -> None:
        d = copy.deepcopy(self.sources)
        row = next(x for x in d["records"] if x["id"] == "SRC-ADAJ1979-IBRAHIM-VANDERKOOIJ-PHASEIX")
        row["datingScope"] = "C14_CONFIRMED_750_BCE_WITHOUT_ERROR"
        self.assertTrue(any("provisional phase dating" in e for e in validate_source_access(d)))

    def test_deir_alla_adaj1979_parsed_pdf_cannot_imply_visual_photo_check(self) -> None:
        d = copy.deepcopy(self.sources)
        row = next(x for x in d["records"] if x["id"] == "SRC-ADAJ1979-IBRAHIM-VANDERKOOIJ-PHASEIX")
        row["imageScope"] = "ALL_ANCIENT_PLASTER_FACSIMILES_VISUALLY_COLLATED"
        self.assertTrue(any("PDF visual scope falsely promoted" in e for e in validate_source_access(d)))

    def test_deir_alla_lemaire1985_atda_1976_p16_was_not_directly_checked(self) -> None:
        d = copy.deepcopy(self.sources)
        row = next(x for x in d["records"] if x["id"] == "SRC-LEMAIRE-DEIRALLA-1985-RADIOCARBON-PP271272")
        row["carbonScope"] = "1976_C14_SAMPLE_PHOTO_AND_MODERN_RECALIBRATION_DIRECTLY_VALIDATED"
        self.assertTrue(any("radiocarbon provenance" in e for e in validate_source_access(d)))

    def test_deir_alla_lemaire1985_amos1_1_earthquake_is_not_certain(self) -> None:
        d = copy.deepcopy(self.sources)
        row = next(x for x in d["records"] if x["id"] == "SRC-LEMAIRE-DEIRALLA-1985-RADIOCARBON-PP271272")
        row["earthquakeScope"] = "CERTAIN_MATCH_OF_AMOS_1_1_QUAKE_AND_DEIRALLA_DESTRUCTION"
        self.assertTrue(any("Amos-earthquake conjecture" in e for e in validate_source_access(d)))

    def test_deir_alla_adaj1986_two_samples_not_exact_inscription_date(self) -> None:
        d = copy.deepcopy(self.sources)
        row = next(x for x in d["records"] if x["id"] == "SRC-ADAJ1986-IBRAHIM-VANDERKOOIJ-2C14-P142")
        row["carbonScope"] = "AM0S_1_1_750_BCE_EARTHQUAKE_EXACTLY_PROVEN"
        self.assertTrue(any("radiocarbon calibration" in e for e in validate_source_access(d)))

    def test_deir_alla_adaj1986_bench_room_not_proven_temple(self) -> None:
        d = copy.deepcopy(self.sources)
        row = next(x for x in d["records"] if x["id"] == "SRC-ADAJ1986-IBRAHIM-VANDERKOOIJ-2C14-P142")
        row["functionScope"] = "EXCAVATION_PROVES_FULL_SANCTUARY_FUNCTION"
        self.assertTrue(any("room function" in e for e in validate_source_access(d)))

    def test_deir_alla_weinstein_vs_1986_lab_number_conflict_is_open(self) -> None:
        d = copy.deepcopy(self.sources)
        row = next(x for x in d["records"] if x["id"] == "SRC-WEINSTEIN-1984-DEIRALLA-C14-CONFLICT-P351")
        row["discrepancyScope"] = "C14_SAMPLE_CONFLICT_RESOLVED_WITHOUT_ORIGINAL_LAB_LIST"
        self.assertTrue(any("GrN-5283/5633 source conflict" in e for e in validate_source_access(d)))

    def test_deir_alla_weinstein_does_not_invent_1972_lab_autopsy(self) -> None:
        d = copy.deepcopy(self.sources)
        row = next(x for x in d["records"] if x["id"] == "SRC-WEINSTEIN-1984-DEIRALLA-C14-CONFLICT-P351")
        row["laboratorySourceAccess"] = "VOGEL_WATERBOLK_1972_R14_P53_FULL_ORIGINAL_READ"
        self.assertTrue(any("1972 laboratory-access boundary" in e for e in validate_source_access(d)))

    def test_deir_alla_livius_translation_cannot_inherit_photo_cc0_rights(self) -> None:
        d = copy.deepcopy(self.sources)
        row = next(x for x in d["records"] if x["id"] == "SRC-LIVIUS-LEVINE-COMPOSITE-TRANSLATION-2003")
        row["rightsState"] = "PUBLICATION_ELIGIBLE"
        self.assertTrue(any("Livius composite translation wrongly treated as a primary or free text" in e for e in validate_source_access(d)))


if __name__ == "__main__":
    unittest.main()
