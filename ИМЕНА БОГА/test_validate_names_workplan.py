"""Negative regression tests: a green workplan CI must not be a false completion signal."""
from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from validate_names_workplan import validate_names_workplan

ROOT = Path(__file__).resolve().parent


class NamesResearchWorkplanTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.plan = json.loads((ROOT / "data/names_research_workplan_v1.json").read_text(encoding="utf-8"))
        cls.baseline = json.loads((ROOT / "data/names_ledger_v1.json").read_text(encoding="utf-8"))
        cls.extension = json.loads((ROOT / "data/names_extension_ledger_v1.json").read_text(encoding="utf-8"))
        cls.sources = json.loads((ROOT / "data/source_access_register_v1.json").read_text(encoding="utf-8"))
        cls.tests = (ROOT / "test_validate_names_ledger.py").read_text(encoding="utf-8")
        cls.nav = (ROOT / "00_README_AND_NAVIGATION.md").read_text(encoding="utf-8")
        cls.guide = (ROOT / "11_MASTER_RESEARCH_WORKPLAN_AND_ACCEPTANCE.md").read_text(encoding="utf-8")
        cls.media = (ROOT / "12_TMS_BARRICK_CHOU_SOURCE_REVIEW.md").read_text(encoding="utf-8")

    def check(self, plan: dict | None = None, **changes) -> list[str]:
        return validate_names_workplan(
            self.plan if plan is None else plan,
            baseline=changes.get("baseline", self.baseline),
            extension=changes.get("extension", self.extension),
            sources=changes.get("sources", self.sources),
            corpus_tests=changes.get("corpus_tests", self.tests),
            navigation=changes.get("navigation", self.nav),
            guide=changes.get("guide", self.guide),
            media_document=changes.get("media_document", self.media),
        )

    def test_current_workplan_is_consistent(self) -> None:
        self.assertEqual([], self.check())

    def test_closure_requires_actual_verification_not_a_badge(self) -> None:
        plan = copy.deepcopy(self.plan)
        task = next(t for t in plan["tasks"] if t["id"] == "NG-06")
        task["status"] = "DONE"
        self.assertTrue(any("DONE without witnessed" in e for e in self.check(plan)))

    def test_closed_task_cannot_have_unwitnessed_timestamp(self) -> None:
        plan = copy.deepcopy(self.plan)
        task = next(t for t in plan["tasks"] if t["id"] == "NG-05")
        task["closureAt"] = "2026-11-07"
        self.assertTrue(any("false closure timestamp" in e for e in self.check(plan)))

    def test_cannot_drop_task_id_from_master_board(self) -> None:
        plan = copy.deepcopy(self.plan)
        plan["tasks"] = [t for t in plan["tasks"] if t["id"] != "NG-14"]
        self.assertTrue(any("original sixteen stable" in e for e in self.check(plan)))

    def test_orphaned_prerequisite_fails(self) -> None:
        plan = copy.deepcopy(self.plan)
        task = next(t for t in plan["tasks"] if t["id"] == "NG-02")
        task["dependsOn"] = ["NG-99"]
        self.assertTrue(any("orphan dependency" in e for e in self.check(plan)))

    def test_circular_prerequisites_are_not_a_valid_workflow(self) -> None:
        plan = copy.deepcopy(self.plan)
        task = next(t for t in plan["tasks"] if t["id"] == "NG-01")
        task["dependsOn"].append("NG-02")
        self.assertTrue(any("dependency cycle" in e for e in self.check(plan)))

    def test_phases_cannot_omit_a_task(self) -> None:
        plan = copy.deepcopy(self.plan)
        plan["phases"][4]["tasks"].remove("NG-15")
        self.assertTrue(any("phase task coverage" in e for e in self.check(plan)))

    def test_barrick_original_page_cannot_be_missing_from_media_queue(self) -> None:
        plan = copy.deepcopy(self.plan)
        plan["mediaQueue"] = [m for m in plan["mediaQueue"] if m["id"] != "MEDIA-BARRICK-04"]
        self.assertTrue(any("core media queue" in e for e in self.check(plan)))

    def test_zhakevich_course_must_not_be_marked_watched_from_catalog(self) -> None:
        plan = copy.deepcopy(self.plan)
        media = next(x for x in plan["mediaQueue"] if x["id"] == "MEDIA-TMS-JZ-01")
        media["status"] = "WATCHED_WITH_AUDIO"
        self.assertTrue(any("falsely claimed fully watched" in e for e in self.check(plan)))

    def test_external_lecture_must_have_https_url(self) -> None:
        plan = copy.deepcopy(self.plan)
        media = next(x for x in plan["mediaQueue"] if x["id"] == "MEDIA-CHOU-JZ-02")
        media["url"] = "http://unknown.invalid/video"
        self.assertTrue(any("unsafe or missing source URL" in e for e in self.check(plan)))

    def test_99_source_witnesses_must_not_be_silently_fabricated(self) -> None:
        plan = copy.deepcopy(self.plan)
        plan["baseline"]["contextAttestations"] = 999
        self.assertTrue(any("contextAttestations snapshot drifted" in e for e in self.check(plan)))

    def test_growing_source_registry_requires_new_plan_snapshot(self) -> None:
        sources = copy.deepcopy(self.sources)
        sources["records"].append({"id": "SRC-UNVERIFIED", "publicationState": "BLOCKED"})
        self.assertTrue(any("sourceRegisterEntries snapshot drifted" in e for e in self.check(sources=sources)))

    def test_critical_approval_cannot_be_backfilled_without_source(self) -> None:
        plan = copy.deepcopy(self.plan)
        plan["baseline"]["criticalCollationsCompleted"] = 1
        self.assertTrue(any("unearned critical collation" in e for e in self.check(plan)))

    def test_navigation_must_keep_canonical_plan_links(self) -> None:
        self.assertTrue(any("omitted from research navigation" in e for e in
                            self.check(navigation="# outdated navigation")))

    def test_lecture_audit_must_keep_tms_source_names_and_identifiers(self) -> None:
        self.assertTrue(any("expected lecture provenance missing" in e for e in
                            self.check(media_document="All evidence here")))

    def test_publication_block_applies_to_all_source_records(self) -> None:
        sources = copy.deepcopy(self.sources)
        sources["records"][0]["publicationState"] = "PUBLICATION_ELIGIBLE"
        self.assertTrue(any("corpus unexpectedly published" in e for e in self.check(sources=sources)))


if __name__ == "__main__":
    unittest.main()
