"""Mutation regressions for reader crosswalk, preventing invented scholarly completion."""
from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from validate_names_reader import validate_reader_crosswalk, EXPECTED_READER_FILES

ROOT = Path(__file__).resolve().parent


class ReaderCrosswalkTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry = json.loads((ROOT / "data/names_reader_claim_crosswalk_v1.json").read_text(encoding="utf-8"))
        cls.claims = json.loads((ROOT / "data/names_claim_registry_v1.json").read_text(encoding="utf-8"))
        cls.sources = json.loads((ROOT / "data/source_access_register_v1.json").read_text(encoding="utf-8"))
        cls.readers = {x: (ROOT / x).read_text(encoding="utf-8") for x in EXPECTED_READER_FILES.values()}

    def check(self, registry=None, claims=None, sources=None, readers=None):
        return validate_reader_crosswalk(
            self.registry if registry is None else registry,
            self.claims if claims is None else claims,
            self.sources if sources is None else sources,
            self.readers if readers is None else readers,
        )

    def test_full_three_reader_sections_are_current(self):
        self.assertEqual([], self.check())

    def test_must_not_claim_external_peer_review(self):
        change = copy.deepcopy(self.registry)
        change["independentScholarlyReviewsAccepted"] = 1
        self.assertTrue(any("cannot grant" in e for e in self.check(registry=change)))

    def test_must_not_claim_product_rights(self):
        for field, val in (("publicationState", "APPROVED"), ("productApprovals", 1),
                           ("rightsClearanceGranted", True), ("criticalManuscriptCollationsCompleted", 1)):
            with self.subTest(field=field):
                change = copy.deepcopy(self.registry)
                change[field] = val
                self.assertTrue(any("cannot grant" in e for e in self.check(registry=change)))

    def test_must_not_omit_a_reader_or_clone_chapter(self):
        for mutation in ("remove", "clone"):
            with self.subTest(mutation=mutation):
                changed = copy.deepcopy(self.registry)
                changed["chapters"] = (changed["chapters"][:-1] if mutation == "remove"
                                       else changed["chapters"][:2] + [copy.deepcopy(changed["chapters"][1])])
                self.assertTrue(any("exactly three unique" in e for e in self.check(registry=changed)))

    def test_must_not_invent_claim_ids(self):
        changed = copy.deepcopy(self.registry)
        changed["chapters"][0]["sections"][0]["claimIds"][0] = "CLM-INVENTED-DIVINE-NAME"
        self.assertTrue(any("orphaned registered claim" in e for e in self.check(registry=changed)))

    def test_must_not_forge_claim_to_source_evidence(self):
        changed = copy.deepcopy(self.registry)
        changed["chapters"][1]["sections"][0]["claimSourceIds"] = ["SRC-NONEXISTENT"]
        self.assertTrue(any("stored claim-source trace differs" in e for e in self.check(registry=changed)))

    def test_must_not_make_supplemental_artifact_a_phantom_source(self):
        changed = copy.deepcopy(self.registry)
        changed["chapters"][2]["sections"][8]["supplementalSourceIds"] = ["SRC-INVENTED-DEIRALLA-FACSIMILE"]
        self.assertTrue(any("unsupported supplemental source" in e for e in self.check(registry=changed)))

    def test_unsupported_ruth_job_gap_cannot_be_silently_relabelled_as_proven(self):
        changed = copy.deepcopy(self.registry)
        changed["chapters"][2]["sections"][9]["editorialRole"] = "EXACT_RESEARCH_CLAIM_MATCH"
        self.assertTrue(any("unproved section" in e for e in self.check(registry=changed)))

    def test_secondary_theology_requires_explicit_unclosed_boundary(self):
        changed = copy.deepcopy(self.registry)
        changed["chapters"][0]["sections"][3]["unresolvedArgumentBoundary"] = ""
        self.assertTrue(any("uncertainty or claim gap" in e for e in self.check(registry=changed)))

    def test_chapter_heading_deleted_from_reader_cannot_leave_map_green(self):
        changed = dict(self.readers)
        path = EXPECTED_READER_FILES["CH-PILOT-03"]
        changed[path] = changed[path].replace("### Бог, Который сотворил", "## Бог, Который сотворил", 1)
        self.assertTrue(any("actual narrative headings" in e for e in self.check(readers=changed)))

    def test_chapter_heading_rearranged_without_map_change_fails(self):
        changed = copy.deepcopy(self.registry)
        changed["chapters"][1]["sections"][0], changed["chapters"][1]["sections"][1] = (
            changed["chapters"][1]["sections"][1], changed["chapters"][1]["sections"][0]
        )
        self.assertTrue(any("actual narrative headings" in e for e in self.check(registry=changed)))

    def test_chapter3_does_not_regress_to_lab_report_as_main_text(self):
        changed = dict(self.readers)
        path = EXPECTED_READER_FILES["CH-PILOT-03"]
        changed[path] = changed[path].replace(
            "### Когда «Шаддай» звучит без «Эль»",
            ("Одно и то же громоздкое археологическое отступление. " * 950)
            + "\n### Когда «Шаддай» звучит без «Эль»", 1,
        )
        self.assertTrue(any("exceeds word budget" in e for e in self.check(readers=changed)))

    def test_deir_alla_original_long_research_cannot_be_discarded(self):
        changed = dict(self.readers)
        path = EXPECTED_READER_FILES["CH-PILOT-03"]
        changed[path] = changed[path].replace("GrN-", "UNDISCLOSED-")
        self.assertTrue(any("detailed research evidence missing" in e for e in self.check(readers=changed)))

    def test_deir_alla_real_photo_must_not_be_replaced_by_drawing(self):
        changed = dict(self.readers)
        path = EXPECTED_READER_FILES["CH-PILOT-03"]
        changed[path] = changed[path].replace(
            "tal_dayr_alla_bileam_jordanmus.jpg", "rendered_reconstruction.jpg", 1
        )
        self.assertTrue(any("original museum photo replaced" in e for e in self.check(readers=changed)))

    def test_photos_stay_in_original_reader_and_appendix_count(self):
        changed = dict(self.readers)
        path = EXPECTED_READER_FILES["CH-PILOT-03"]
        changed[path] = changed[path].replace("![Современная реконструкция", "[Современная реконструкция", 1)
        changed[path] = changed[path].replace("![Плакат музейной выставки", "[Плакат музейной выставки", 1)
        self.assertTrue(any("image and original research preservation" in e for e in self.check(readers=changed)))

    def test_claim_publication_approval_does_not_override_pilot_gate(self):
        changed = copy.deepcopy(self.claims)
        target = next(x for x in changed["records"] if x["claimId"] == "CLM-EX3-15-DIVINE-NAME")
        target["editorialState"] = "ACCEPTED"
        self.assertTrue(any("cannot promote mapped research-held claim" in e for e in self.check(claims=changed)))

    def test_source_publication_approval_does_not_override_pilot_gate(self):
        changed = copy.deepcopy(self.sources)
        target = next(x for x in changed["records"] if x["id"] == "SRC-MT-MECHON")
        target["publicationState"] = "APPROVED"
        self.assertTrue(any("source was prematurely promoted" in e for e in self.check(sources=changed)))

    def test_reader_cannot_remove_original_editorial_status(self):
        changed = dict(self.readers)
        path = EXPECTED_READER_FILES["CH-PILOT-01"]
        changed[path] = changed[path].replace("NOT EDITORIAL_READY", "FULLY_APPROVED")
        self.assertTrue(any("editorial hold removed" in e for e in self.check(readers=changed)))


if __name__ == "__main__":
    unittest.main()
