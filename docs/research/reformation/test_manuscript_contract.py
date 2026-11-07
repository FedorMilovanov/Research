#!/usr/bin/env python3
"""Book-level safety and navigation regressions for Reformation drafts."""
from pathlib import Path
import re
import unittest

HERE = Path(__file__).resolve().parent
INTRO = HERE / "00_introduction_manuscript.md"
EPISODE01 = HERE / "episode01_historical_gateway_draft.md"

class ReformationManuscriptTests(unittest.TestCase):
    def test_single_introduction_and_chapter_range(self):
        self.assertTrue(INTRO.is_file())
        self.assertTrue(EPISODE01.is_file())
        chapters = [EPISODE01, *sorted(HERE.glob("episode[0-9][0-9]_*_manuscript.md"))]
        ids = [int(re.search(r"episode(\d{2})_", p.name).group(1)) for p in chapters]
        self.assertEqual(len(ids), len(set(ids)), "two manuscripts for same episode")
        # Before wave 380 a missing chapter (e.g. #11) did not fail this test.
        # The accepted book has exactly twelve historical episodes, no gaps.
        self.assertEqual(ids, list(range(1, 13)),
                         "one or more historical chapters missing or duplicated")

    def test_all_manuscripts_remain_publication_hold(self):
        chapters = [INTRO, EPISODE01, *sorted(HERE.glob("episode[0-9][0-9]_*_manuscript.md"))]
        for path in chapters:
            content = path.read_text(encoding="utf-8")
            with self.subTest(path=path.name):
                self.assertIn("RESEARCH_MANUSCRIPT_DRAFT", content)
                self.assertIn("PUBLICATION_HOLD", content)
                self.assertGreaterEqual(len(content.split()), 300)

    def test_every_existing_episode_linked_from_authority_navigation(self):
        readme = (HERE / "README.md").read_text(encoding="utf-8")
        blueprint = (HERE / "04_series_blueprint.md").read_text(encoding="utf-8")
        chapters = [EPISODE01, *sorted(HERE.glob("episode[0-9][0-9]_*_manuscript.md"))]
        for path in chapters:
            with self.subTest(path=path.name):
                self.assertRegex(readme,
                                 r"\]\(" + re.escape(path.name) + r"(?:#[^)]*)?\)")
                self.assertRegex(blueprint,
                                 r"\]\(" + re.escape(path.name) + r"(?:#[^)]*)?\)")
        # All public release gates remain closed even if an individual early
        # chapter uses a shorter historical status line.
        self.assertIn("NOT_EDITORIAL_READY", readme)
        self.assertIn("PUBLICATION_HOLD", readme)

    def test_episode02_is_still_inside_existing_series(self):
        p = HERE / "episode02_indulgences_1517_manuscript.md"
        self.assertTrue(p.is_file())
        content = p.read_text(encoding="utf-8")
        self.assertTrue(content.startswith("# Эпизод 02."))
        self.assertIn("REF-P01", content)
        self.assertIn("REF-P02", content)
        self.assertIn("Источниковедческий аппарат", content)
        self.assertIn("PUBLICATION_HOLD", content)
        ep01 = EPISODE01.read_text(encoding="utf-8")
        self.assertIn(p.name, ep01)

if __name__ == "__main__":
    unittest.main()
