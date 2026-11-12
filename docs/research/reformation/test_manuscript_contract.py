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
        for preserved_limit in (
            "полная глава пока не коллирована в Research",
            "конкретные археологические утверждения требуют отдельных локаторов",
            "не** критическая проверка всех рукописей",
            "Доступные аннотации и выдержки не подменяют полный критический разбор",
            "чтобы не повторять их дважды",
        ):
            with self.subTest(limit=preserved_limit):
                self.assertIn(preserved_limit, moved)
        self.assertIn("](episode01_historical_gateway_draft.md)", reader)
        self.assertIn("NOT_EDITORIAL_READY", intro)
        self.assertIn("PUBLICATION_HOLD", intro)

    def test_introduction_reader_starts_with_story_and_ends_with_navigation(self):
        """Keep editorial metadata outside the reader and avoid a false ending."""
        intro = INTRO.read_text(encoding="utf-8")
        reader, apparatus = intro.split(
            "## Источниковедческие и редакционные примечания", 1
        )
        self.assertTrue(reader.startswith(
            "# Что такое Реформация? От Эдема до Европы накануне 1517 года\n\n## Не всякое изменение — реформа"
        ))
        meta_label = "Единственное книжное введение; редакторское разграничение"
        self.assertNotIn(meta_label, reader)
        self.assertEqual(apparatus.count(meta_label), 1)
        for gate in ("RESEARCH_MANUSCRIPT_DRAFT", "NOT_EDITORIAL_READY",
                     "PUBLICATION_HOLD", "eBible RUSSYN"):
            self.assertIn(gate, apparatus)
        conclusion = reader.index("## Вместо заключения к введению")
        nav = "Далее — [«Европа перед 1517 годом»](episode01_historical_gateway_draft.md)."
        self.assertEqual(reader.count(nav), 1)
        self.assertGreater(reader.index(nav), conclusion)
        self.assertEqual(reader.split(nav, 1)[1].strip(), "---")
        self.assertNotIn("На этом мы завершаем большое введение.", reader)

    def test_wave452_intro_hands_historical_causes_to_chapter01_and_theology_to_epilogue(self):
        """A reader-facing boundary, not a source deletion or review-gate upgrade."""
        intro = INTRO.read_text(encoding="utf-8")
        reader, apparatus = intro.split(
            "## Источниковедческие и редакционные примечания", 1
        )
        historical = reader.split("## 17. Почему именно XVI век?", 1)[1].split(
            "## Вместо заключения к введению", 1
        )[0]
        conclusion = reader.split("## Вместо заключения к введению", 1)[1]
        chapter01 = EPISODE01.read_text(encoding="utf-8").split(
            "## Источниковедческий аппарат", 1
        )[0]
        for factual_thread in ("гуманист", "княжеск", "город", "печать",
                               "университет"):
            with self.subTest(factual_thread=factual_thread):
                self.assertIn(factual_thread, chapter01.lower())
        self.assertNotIn("К концу XV столетия в западном христианстве", historical)
        for required in (
            "исторические причины Реформации необходимо исследовать отдельно",
            "истории Европы около 1450–1517 годов",
        ):
            self.assertIn(required, historical)
        for required in (
            "Наша задача не доказать заранее",
            "Исторические выводы потребуют свидетельств эпохи",
            "оценка учения и поклонения",
            "Христианская надежда связана с Христом",
            "премилленаристская перспектива",
            "альтернативные толкования Откр. 19–22",
            "будут рассмотрены **в эпилоге**",
        ):
            with self.subTest(required=required):
                self.assertIn(required.lower(), conclusion.lower())
        self.assertNotIn("Итак, что означает Реформация?", conclusion)
        self.assertEqual(conclusion.count("премилленарист"), 1)
        self.assertIn("### Исторические свидетельства ранней", apparatus)
        self.assertIn("NOT_EDITORIAL_READY", apparatus)
        self.assertIn("PUBLICATION_HOLD", apparatus)
        ending = (HERE / "episode12_reformation_everyday_life_1520_1600_manuscript.md"
                  ).read_text(encoding="utf-8")
        self.assertIn("Здесь заканчивается **двенадцатая историческая глава**.", ending)
        self.assertIn("](epilogue_reformation_last_restoration_manuscript.md)", ending)
        epilogue = (HERE / "epilogue_reformation_last_restoration_manuscript.md"
                    ).read_text(encoding="utf-8")
        self.assertIn("принято премилленаристское прочтение", epilogue)
        self.assertIn("Амилленаристское прочтение", epilogue)
        self.assertIn("Постмилленаристское прочтение", epilogue)

    def test_kings_18_22_digital_witnesses_not_conflated(self):
        """Different Synodal web editions are evidence of variance, not a collation."""
        intro = INTRO.read_text(encoding="utf-8")
        reader, apparatus = intro.split(
            "## Источниковедческие и редакционные примечания", 1
        )
        self.assertIn("две доступные цифровые публикации", reader)
        self.assertIn("eBible RUSSYN", reader)
        self.assertIn("RST на Biblia.com", reader)
        self.assertIn("Историю разночтений нельзя установить", reader)
        self.assertIn("масоретский текст", reader)
        self.assertIn("Септуагинты", reader)
        self.assertIn("https://ebible.org/russyn/1KI18.htm", apparatus)
        self.assertIn("https://biblia.com/bible/rst/1-kings/18/19-22", apparatus)
        self.assertIn("https://lemma.gebible.app/v/1-kings/18/22", apparatus)
        self.assertIn("18:19", apparatus)
        self.assertIn("18:22", apparatus)
        self.assertIn("не выполненная колляция русских исторических печатей", apparatus)
        self.assertIn("что именно русская публикация отражает первоначальный текст", apparatus)
        self.assertIn("RESEARCH_MANUSCRIPT_DRAFT", intro)
        self.assertIn("NOT_EDITORIAL_READY", intro)
        self.assertIn("PUBLICATION_HOLD", intro)

    def test_wave409_first_three_chapters_have_reader_first_prose(self):
        """Reader prose is separate from operational status; chapter sections retain hierarchy."""
        chapters = (
            ("episode01_historical_gateway_draft.md",
             "Рабочий исторический вход для уже запланированного эпизода",
             "### Реформа до Реформации", "## Реформа до Реформации"),
            ("episode02_indulgences_1517_manuscript.md",
             "Самостоятельный книжный черновик второго из двенадцати",
             "### Вопрос, который нельзя было решить покупкой грамоты",
             "## Вопрос, который нельзя было решить покупкой грамоты"),
            ("episode03_luther_worms_1520_1521_manuscript.md",
             "Книжная рукопись третьего из двенадцати",
             "### Когда один спор перестал быть местным",
             "## Когда один спор перестал быть местным"),
        )
        for name, meta_label, former_heading, proper_heading in chapters:
            with self.subTest(name=name):
                text = (HERE / name).read_text(encoding="utf-8")
                reader, apparatus = text.split("## Источниковедческий аппарат", 1)
                self.assertNotIn(meta_label, reader)
                self.assertEqual(apparatus.count(meta_label), 1)
                self.assertNotIn(former_heading, reader)
                self.assertIn(proper_heading, reader)
                self.assertIn("RESEARCH_MANUSCRIPT_DRAFT", apparatus)
                self.assertIn("NOT_EDITORIAL_READY", apparatus)
                self.assertIn("PUBLICATION_HOLD", apparatus)
                self.assertNotIn("## Рабочий текст", reader)
                self.assertNotIn("## Исторический рассказ", reader)

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
