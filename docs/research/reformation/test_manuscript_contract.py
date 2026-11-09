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

    def test_single_biblical_epilogue_separate_from_twelve_histories(self):
        epilogue = HERE / "epilogue_reformation_last_restoration_manuscript.md"
        self.assertTrue(epilogue.is_file())
        s = epilogue.read_text(encoding="utf-8")
        self.assertTrue(s.startswith("# Эпилог."))
        self.assertGreaterEqual(len(s.split()), 1600)
        for marker in ("RESEARCH_MANUSCRIPT_DRAFT", "NOT_EDITORIAL_READY",
                       "PUBLICATION_HOLD", "премилленарист",
                       "амилленарист", "постмилленарист", "Откр. 20",
                       "1 Кор. 15", "глава 32", "глава 31"):
            self.assertIn(marker.lower(), s.lower())
        self.assertNotRegex(epilogue.name, r"^episode\d{2}_")
        for name in ("README.md", "04_series_blueprint.md",
                     "SELF_PLAN.md", "episode12_reformation_everyday_life_1520_1600_manuscript.md"):
            self.assertIn(epilogue.name,(HERE/name).read_text(encoding="utf-8"))
        # There is still exactly one introductory book text and 12 histories.
        self.assertEqual(len(list(HERE.glob("episode[0-9][0-9]_*_manuscript.md"))) + 1, 12)

    def test_reader_edits_keep_facts_and_full_apparatus(self):
        intro = INTRO.read_text(encoding="utf-8")
        ch1 = EPISODE01.read_text(encoding="utf-8")
        a = intro.split("## Источниковедческие и редакционные примечания", 1)
        b = ch1.split("## Источниковедческий аппарат и статус", 1)
        self.assertEqual(len(a), 2)
        self.assertEqual(len(b), 2)
        self.assertLess(len(a[0].split()), 5300)
        self.assertLess(len(b[0].split()), 4500)
        self.assertIn("NOT_EDITORIAL_READY", intro)
        self.assertIn("NOT_EDITORIAL_READY", ch1)
        # Editor moves evidence, not the historic witness or numbered concordance.
        self.assertIn("Маркион",a[1])
        for marker in ("Kalliope", "Theodor Dieter", "### Досье к октябрю",
                       "| Стандартный №", "95 тезисов"):
            self.assertIn(marker,b[1])
        self.assertIn("### Исторические свидетельства ранней",a[1])

    def test_introduction_reader_source_notes_are_preserved_in_apparatus(self):
        """Keep the same twelve textual witnesses and the forward navigation."""
        intro = INTRO.read_text(encoding="utf-8")
        reader, apparatus = intro.split(
            "## Источниковедческие и редакционные примечания", 1
        )
        label = "### Перенесённые источниковые примечания к читательским разделам — волна 404"
        self.assertEqual(apparatus.count(label), 1)
        moved, remainder = apparatus.split(label, 1)[1].split(
            "### Исторические свидетельства ранней", 1
        )
        self.assertTrue(remainder.strip())
        import re
        standalone = re.compile(
            r"(?m)^\*(?:Библейский текст и формулировка стиха|Тексты|Текст|"
            r"Академическая опора|Редакционная ссылка на отдельное начало эпизода 01):\*"
        )
        self.assertEqual(standalone.findall(reader), [])
        self.assertEqual(len(standalone.findall(moved)), 12)
        for locator in (
            "https://ebible.org/russyn/EXO32.htm",
            "https://ebible.org/russyn/JDG02.htm",
            "https://ebible.org/russyn/1KI11.htm",
            "https://ebible.org/russyn/1KI18.htm",
            "https://ebible.org/russyn/2KI18.htm",
            "https://ebible.org/russyn/2KI22.htm",
            "https://ebible.org/russyn/1KI22.htm",
            "https://ebible.org/russyn/JER07.htm",
            "https://ebible.org/russyn/LAM05.htm",
            "Oxford Classical Dictionary — Maccabees",
            "https://ebible.org/russyn/REV02.htm",
            "Подробные сведения о Гутенберге",
        ):
            with self.subTest(locator=locator):
                self.assertIn(locator, moved)
                self.assertNotIn(locator, reader)
        self.assertIn("](episode01_historical_gateway_draft.md)", reader)
        self.assertIn("NOT_EDITORIAL_READY", intro)
        self.assertIn("PUBLICATION_HOLD", intro)

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
