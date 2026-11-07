"""Mutation tests for the read-only Names of God ledger validator."""
from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from validate_names_ledger import validate, validate_extension, validate_source_access

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


if __name__ == "__main__":
    unittest.main()
