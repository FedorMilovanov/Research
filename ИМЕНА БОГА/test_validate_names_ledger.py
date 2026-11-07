"""Mutation tests for the read-only Names of God ledger validator."""
from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from validate_names_ledger import validate, validate_extension, validate_source_access, validate_apocalyptic, validate_prophetic_namings, validate_six_title_attestations

ROOT = Path(__file__).resolve().parent


class ResearchEvidenceGuardTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.baseline = json.loads((ROOT / "data" / "names_ledger_v1.json").read_text(encoding="utf-8"))
        cls.extension = json.loads((ROOT / "data" / "names_extension_ledger_v1.json").read_text(encoding="utf-8"))
        cls.sources = json.loads((ROOT / "data" / "source_access_register_v1.json").read_text(encoding="utf-8"))
        cls.title_contract = json.loads((ROOT / "data" / "attestation_contract_v1.json").read_text(encoding="utf-8"))

    def test_current_research_corpora_pass_structure(self) -> None:
        self.assertEqual([], validate(self.baseline))
        self.assertEqual([], validate_extension(self.extension, self.baseline))
        self.assertEqual([], validate_source_access(self.sources))
        self.assertEqual([], validate_apocalyptic(self.baseline, self.extension))
        self.assertEqual([], validate_prophetic_namings(self.baseline))
        self.assertEqual([], validate_six_title_attestations(self.baseline, self.title_contract))

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


if __name__ == "__main__":
    unittest.main()
