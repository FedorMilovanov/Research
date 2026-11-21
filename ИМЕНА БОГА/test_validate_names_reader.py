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

    def test_ruth_job_direct_digital_mt_locus_cannot_be_moved_or_promoted(self):
        mutations = (
            (0, "url", "https://mechon-mamre.org/p/pt/pt2705.htm"),
            (0, "sourceId", "SRC-NONEXISTENT"),
            (0, "speakerAndForce", "YHWH_DIRECT_SPEECH"),
            (1, "locus", "Job 6:17"),
            (1, "witnessScope", "ANCIENT_MANUSCRIPT_DIRECT_COLLATION"),
            (2, "claimGraphStatus", "APPROVED_REGISTERED_CLAIM"),
        )
        for idx, field, fake in mutations:
            with self.subTest(index=idx, field=field):
                changed = copy.deepcopy(self.registry)
                changed["chapters"][2]["sections"][9]["directTextLoci"][idx][field] = fake
                self.assertTrue(any("CH03 Ruth/Job direct digital-MT trace drifted" in e
                                    for e in self.check(registry=changed)))

    def test_ruth_job_reader_links_hold_and_modern_mt_status_remain_enforced(self):
        for mutation in ("delete_locus", "erase_source_link", "erase_hold", "upgrade_mt"):
            with self.subTest(mutation=mutation):
                changed = copy.deepcopy(self.registry)
                readers = dict(self.readers)
                sources = copy.deepcopy(self.sources)
                row = changed["chapters"][2]["sections"][9]
                if mutation == "delete_locus":
                    row["directTextLoci"].pop()
                elif mutation == "erase_source_link":
                    path = EXPECTED_READER_FILES["CH-PILOT-03"]
                    readers[path] = readers[path].replace(
                        "https://mechon-mamre.org/p/pt/pt2901.htm", "https://invalid.example/ruth", 1)
                elif mutation == "erase_hold":
                    row["unresolvedArgumentBoundary"] = "All source graph gaps closed."
                else:
                    mt = next(s for s in sources["records"] if s["id"] == "SRC-MT-MECHON")
                    mt["criticalEditionCollated"] = True
                err = self.check(registry=changed, readers=readers, sources=sources)
                self.assertTrue(any("CH03 Ruth/Job" in e for e in err), err)

    def test_ch03_source_urls_cannot_be_moved_out_of_their_section_or_duplicated(self):
        path = EXPECTED_READER_FILES["CH-PILOT-03"]
        heading = "### Когда «Шаддай» звучит без «Эль»"
        for url in (
                "https://mechon-mamre.org/p/pt/pt2901.htm",
                "https://mechon-mamre.org/p/pt/pt2705.htm",
                "https://mechon-mamre.org/p/pt/pt2742.htm"):
            with self.subTest(url=url, mutation="moved"):
                original = self.readers[path]
                link = next(part for part in original.splitlines()
                            if f"]({url})" in part)
                # Move only the Markdown link, preserving all other content.
                import re
                match = re.search(r"\[[^\]]+\]\(" + re.escape(url) + r"\)", link)
                self.assertIsNotNone(match)
                token = match.group()
                moved = original.replace(token, "", 1)
                moved = moved.replace(heading, token + "\n\n" + heading, 1)
                mutated = dict(self.readers)
                mutated[path] = moved
                err = self.check(readers=mutated)
                self.assertTrue(
                    any("source hyperlink must appear exactly once inside its own" in e
                        for e in err), err,
                )
            with self.subTest(url=url, mutation="duplicated"):
                original = self.readers[path]
                pos = original.index(f"]({url})")
                token_start = original.rfind("[", 0, pos)
                token_end = pos + len(f"]({url})")
                token = original[token_start:token_end]
                duplicate = dict(self.readers)
                duplicate[path] = original[:token_end] + " " + token + original[token_end:]
                err = self.check(readers=duplicate)
                self.assertTrue(
                    any("source hyperlink must appear exactly once inside its own" in e
                        for e in err), err,
                )

    def test_direct_text_loci_must_not_appear_in_unrelated_sections(self):
        for chapter_idx, section_idx in ((0, 0), (1, 0), (2, 0), (2, 8)):
            with self.subTest(chapter=chapter_idx, section=section_idx):
                changed = copy.deepcopy(self.registry)
                changed["chapters"][chapter_idx]["sections"][section_idx]["directTextLoci"] = []
                self.assertTrue(
                    any("direct digital-MT trace illegally attached" in e
                        for e in self.check(registry=changed))
                )

    def test_seow_research_commentary_cannot_be_omitted_or_promoted(self):
        source_id = "SRC-SEOW-INTERPRETATION-2026-JOB42-7-10-DIVINE-ANGER"
        for mutation in ("drop_link", "fake_article", "promote_source", "fake_role", "erase_apparatus"):
            with self.subTest(mutation=mutation):
                registry = copy.deepcopy(self.registry)
                sources = copy.deepcopy(self.sources)
                readers = dict(self.readers)
                row = registry["chapters"][2]["sections"][9]
                article = next(s for s in sources["records"] if s["id"] == source_id)
                if mutation == "drop_link":
                    row["supplementalSourceIds"] = []
                elif mutation == "fake_article":
                    row["supplementalSourceIds"] = ["SRC-KRUGER-SHADDAY-JOB-2023-CONTEXT-CRITIQUE"]
                elif mutation == "promote_source":
                    article["criticalEditionCollated"] = True
                elif mutation == "fake_role":
                    article["sourceRole"] = "ANCIENT_ORIGINAL_HEBREW_CODEX_COLLATED"
                else:
                    path = EXPECTED_READER_FILES["CH-PILOT-03"]
                    readers[path] = readers[path].replace(
                        "https://journals.sagepub.com/doi/full/10.1177/00209643251410214",
                        "https://invalid.example/journal", 1)
                issues = self.check(registry=registry, sources=sources, readers=readers)
                self.assertTrue(any("CH03 Seow" in issue for issue in issues), issues)

    def test_provisional_ruth_job_assertions_are_exact_held_digital_loci_not_new_claims(self):
        mutations = (
            (0, "id", "CLM-FALSELY-APPROVED-RUTH"),
            (0, "sourceId", "SRC-UNREGISTERED"),
            (0, "hebrewExcerpt", "שַׁדַּי"),
            (0, "prohibitedInference", "The narrator endorses all of Naomi's claims."),
            (1, "boundedAssertion", "YHWH personally speaks the warning in Job 5:17."),
            (1, "locus", "Job 4:17"),
            (2, "state", "INDEPENDENT_SCHOLAR_APPROVED"),
            (2, "publicationState", "PROMOTE"),
        )
        for i, field, fake in mutations:
            with self.subTest(index=i, field=field):
                change = copy.deepcopy(self.registry)
                change["chapters"][2]["sections"][9]["provisionalReaderAssertions"][i][field] = fake
                self.assertTrue(
                    any("provisional source-located assertions drifted" in e
                        for e in self.check(registry=change))
                )
        path = EXPECTED_READER_FILES["CH-PILOT-03"]
        replaced = dict(self.readers)
        replaced[path] = replaced[path].replace(
            "`לֹא דִבַּרְתֶּם אֵלַי נְכוֹנָה`",
            "`השדים`", 1)
        self.assertTrue(
            any("exact original-script excerpt missing" in e
                for e in self.check(readers=replaced))
        )

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
