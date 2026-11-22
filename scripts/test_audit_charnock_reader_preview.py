"""Fail-closed structural checks for the dated, editorial-only Charnock reader proof.

This validates the assembled reading copy, not historical claims or release rights.
No files are written.
"""
import re
import unittest
from pathlib import Path
from urllib.parse import unquote

from audit_charnock_manuscripts import MANUSCRIPT_DIR, MANUSCRIPTS

ROOT = Path(__file__).resolve().parents[1]
PREVIEW = ROOT / 'БИОГРАФИИ/Стивен Чарнок/reader-preview/CHARNOCK_FULL_BOOK_EDITORIAL_READER_2026-11-21.md'
CHAPTERS = re.compile(r'^## (Введение\. .+|Часть [IVX]+\. .+|Справочник\. .+)$', re.MULTILINE)
SOURCE = re.compile(r'^### (?:Источниковые примечания|Примечания к первичным)', re.MULTILINE)
DEFINITION = re.compile(r'^\[\^([^\]]+)\]:', re.MULTILINE)
REFERENCE = re.compile(r'\[\^([^\]]+)\](?!:)')
LINK = re.compile(r'\]\((\.\./[^)]+)\)')
EXPECTED_NOTES = (13, 20, 18, 17, 18, 21, 20, 20, 19, 14)
EXPECTED_PREFIXES = ('intro', 'ch1', 'ch2', 'ch3', 'ch4', 'ch5', 'ch6', 'ch7', 'ch8', 'ref')


class CharnockReaderProofTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.body = PREVIEW.read_text(encoding='utf-8')
        cls.sections = list(CHAPTERS.finditer(cls.body))

    def test_status_is_research_only_and_pinned_to_source_snapshot(self):
        opening = self.body[:1800]
        self.assertIn('DRAFT / RESEARCH_ONLY / PUBLICATION_HOLD', opening)
        self.assertIn('443d6aa94ee9685f7534deace0351931cd2d3c20', opening)
        self.assertIn('а не SHA действующего полного корпуса', opening)
        self.assertNotIn('Исходные файлы не изменены', opening)
        for hold in ('ED-02', 'ED-06', 'ED-08'):
            self.assertIn(hold, opening)
        self.assertIn('не разрешение на публикацию', opening)

    def test_navigation_does_not_present_historical_main_as_current(self):
        navigation = (PREVIEW.parent / 'README.md').read_text(encoding='utf-8')
        self.assertIn('Историческая инженерная точка сборки, не текущий HEAD', navigation)
        self.assertNotIn('Текущая инженерная опора:', navigation)
        self.assertIn('PR #616', navigation)

    def test_ten_reader_sections_and_linked_contents(self):
        self.assertEqual(len(self.sections), 10)
        self.assertTrue(self.sections[0].group(1).startswith('Введение.'))
        self.assertTrue(self.sections[-1].group(1).startswith('Справочник.'))
        toc = self.body.split('## Содержание\n\n', 1)[1].split('\n\n---', 1)[0]
        self.assertEqual(len(re.findall(r'^\d+\. \[', toc, re.MULTILINE)), 10)

    def test_toc_links_match_actual_headings_not_just_item_count(self):
        """The ten Markdown links must resolve to the actual GitHub heading slugs."""
        toc = self.body.split('## Содержание\n\n', 1)[1].split('\n\n---', 1)[0]
        links = re.findall(
            r'^\d+\. \[([^\]]+)\]\(#([^)]+)\)
        all_definitions = DEFINITION.findall(self.body)
        self.assertEqual(len(all_definitions), 180)
        self.assertEqual(len(set(all_definitions)), 180)
        for index, section in enumerate(self.sections):
            after = self.sections[index + 1].start() if index + 1 < len(self.sections) else len(self.body)
            chunk = self.body[section.end():after]
            source = SOURCE.search(chunk)
            self.assertIsNotNone(source, section.group(1))
            reader, notes = chunk[:source.start()], chunk[source.end():]
            definitions = DEFINITION.findall(notes)
            self.assertEqual(len(definitions), EXPECTED_NOTES[index], section.group(1))
            self.assertEqual(set(REFERENCE.findall(reader)), set(definitions), section.group(1))
            self.assertTrue(all(x.startswith(EXPECTED_PREFIXES[index] + '-') for x in definitions))
            self.assertFalse(DEFINITION.search(reader), section.group(1))

    def test_no_editor_backstage_or_internal_section_headers(self):
        self.assertNotRegex(self.body, r'(?m)^#{2,6} (?:Редакторская приёмка|Редакторский контроль)')
        self.assertEqual(len(SOURCE.findall(self.body)), 10)

    def test_reader_prose_and_all_notes_match_current_ten_manuscripts(self):
        """Catch any stale prose or footnote even when all 180 IDs still exist."""
        self.assertEqual(len(self.sections), len(MANUSCRIPTS))
        for index, name in enumerate(MANUSCRIPTS):
            original = (ROOT / MANUSCRIPT_DIR / name).read_text(encoding='utf-8')
            front = re.search(r'^---\s*$', original, re.MULTILINE)
            backstage = re.search(
                r'^## (?:Редакторская приёмка|Редакторский контроль)',
                original, re.MULTILINE,
            )
            self.assertIsNotNone(front, name)
            self.assertIsNotNone(backstage, name)
            self.assertLess(front.end(), backstage.start(), name)
            reader_section = original[front.end():backstage.start()].strip()
            reader_section = re.sub(
                r'^(#{2,5}) (.+)$',
                lambda match: '#' + match.group(1) + ' ' + match.group(2),
                reader_section, flags=re.MULTILINE,
            )
            reader_section = re.sub(
                r'\[\^([^\]]+)\]',
                lambda match: f'[^{EXPECTED_PREFIXES[index]}-{match.group(1)}]',
                reader_section,
            )
            after = self.sections[index + 1].start() if index + 1 < len(self.sections) else len(self.body)
            printed_section = self.body[self.sections[index].end():after].strip()
            self.assertTrue(printed_section.endswith('---'), name)
            self.assertEqual(printed_section, reader_section, name)

    def test_chapter_vii_coverage_reflects_verified_source_readings(self):
        """Prevent the source-depth map from reverting to obsolete partial-read claims."""
        self.assertEqual(len(self.sections), 10)
        chapter = self.body[
            self.sections[7].start():self.sections[8].start()
        ]
        self.assertIn('| Пастырский вопрос | Сочинение и издание | Объём изученного текста |', chapter)
        self.assertIn('| Откуда вражда к Богу? |', chapter)
        self.assertIn('34 абзаца, печатные с. 6–12', chapter)
        self.assertIn('| Для чего помнить Пятое ноября? |', chapter)
        self.assertIn('Весь основной цифровой текст с эпиграфом', chapter)
        self.assertIn('§§21.73–21.74', chapter)
        self.assertIn('§§21.88–21.90', chapter)
        self.assertNotIn('Начало на печатной с. 42', chapter)
        self.assertNotIn(
            'В трактате о провидении и памятной проповеди Пятого ноября изучены отдельные',
            chapter,
        )

    def test_manuscripts_and_reader_have_no_invisible_or_mixed_script_typos(self):
        """Catch invisible soft hyphens and Cyrillic/Latin homoglyphs in prose."""
        invisible = re.compile(r'[\u00ad\u200b\u200c\u200d\u2060\ufeff]')
        mixed_word = re.compile(r'(?:[A-Za-z][А-Яа-яЁё]|[А-Яа-яЁё][A-Za-z])')
        texts = [(str(PREVIEW), self.body)]
        for name in MANUSCRIPTS:
            path = ROOT / MANUSCRIPT_DIR / name
            texts.append((name, path.read_text(encoding='utf-8')))
        for name, text in texts:
            with self.subTest(file=name):
                self.assertIsNone(invisible.search(text), name)
                self.assertIsNone(mixed_word.search(text), name)

    def test_no_duplicate_horizontal_rules_between_chapters(self):
        self.assertNotRegex(self.body, r'(?m)^---[ \t]*\n\s*---[ \t]*$')

    def test_research_links_survive_path_preserving_move(self):
        links = LINK.findall(self.body)
        self.assertGreaterEqual(len(links), 230)
        for link in links:
            path_part = unquote(link.split('#', 1)[0].strip())
            resolved = (PREVIEW.parent / path_part).resolve()
            self.assertTrue(resolved.is_relative_to(ROOT), link)
            self.assertTrue(resolved.exists(), link)


if __name__ == '__main__':
    unittest.main()
, toc, re.MULTILINE,
        )
        self.assertEqual(len(links), len(self.sections))
        for (label, link_target), chapter in zip(links, self.sections):
            heading = chapter.group(1)
            slug = re.sub(r'[^\w -]', '', heading.lower()).replace(' ', '-')
            self.assertEqual(label, heading)
            self.assertEqual(link_target, slug, heading)

    def test_chapter_iv_ends_once_without_repeated_theological_summary(self):
        section = self.body[
            self.sections[4].start():self.sections[5].start()
        ]
        self.assertEqual(section.count('### Богословие, обращённое к совести'), 1)
        self.assertNotIn('### Четыре линии одной пастырской заботы', section)
        self.assertIn('сходятся в одном вопросе', section)
        self.assertIn('разрозненные проповеди и записи приобрели печатную форму', section)

    def test_notes_are_unique_and_cited_from_each_readers_text(self):
        all_definitions = DEFINITION.findall(self.body)
        self.assertEqual(len(all_definitions), 180)
        self.assertEqual(len(set(all_definitions)), 180)
        for index, section in enumerate(self.sections):
            after = self.sections[index + 1].start() if index + 1 < len(self.sections) else len(self.body)
            chunk = self.body[section.end():after]
            source = SOURCE.search(chunk)
            self.assertIsNotNone(source, section.group(1))
            reader, notes = chunk[:source.start()], chunk[source.end():]
            definitions = DEFINITION.findall(notes)
            self.assertEqual(len(definitions), EXPECTED_NOTES[index], section.group(1))
            self.assertEqual(set(REFERENCE.findall(reader)), set(definitions), section.group(1))
            self.assertTrue(all(x.startswith(EXPECTED_PREFIXES[index] + '-') for x in definitions))
            self.assertFalse(DEFINITION.search(reader), section.group(1))

    def test_no_editor_backstage_or_internal_section_headers(self):
        self.assertNotRegex(self.body, r'(?m)^#{2,6} (?:Редакторская приёмка|Редакторский контроль)')
        self.assertEqual(len(SOURCE.findall(self.body)), 10)

    def test_reader_prose_and_all_notes_match_current_ten_manuscripts(self):
        """Catch any stale prose or footnote even when all 180 IDs still exist."""
        self.assertEqual(len(self.sections), len(MANUSCRIPTS))
        for index, name in enumerate(MANUSCRIPTS):
            original = (ROOT / MANUSCRIPT_DIR / name).read_text(encoding='utf-8')
            front = re.search(r'^---\s*$', original, re.MULTILINE)
            backstage = re.search(
                r'^## (?:Редакторская приёмка|Редакторский контроль)',
                original, re.MULTILINE,
            )
            self.assertIsNotNone(front, name)
            self.assertIsNotNone(backstage, name)
            self.assertLess(front.end(), backstage.start(), name)
            reader_section = original[front.end():backstage.start()].strip()
            reader_section = re.sub(
                r'^(#{2,5}) (.+)$',
                lambda match: '#' + match.group(1) + ' ' + match.group(2),
                reader_section, flags=re.MULTILINE,
            )
            reader_section = re.sub(
                r'\[\^([^\]]+)\]',
                lambda match: f'[^{EXPECTED_PREFIXES[index]}-{match.group(1)}]',
                reader_section,
            )
            after = self.sections[index + 1].start() if index + 1 < len(self.sections) else len(self.body)
            printed_section = self.body[self.sections[index].end():after].strip()
            self.assertTrue(printed_section.endswith('---'), name)
            self.assertEqual(printed_section, reader_section, name)

    def test_chapter_vii_coverage_reflects_verified_source_readings(self):
        """Prevent the source-depth map from reverting to obsolete partial-read claims."""
        self.assertEqual(len(self.sections), 10)
        chapter = self.body[
            self.sections[7].start():self.sections[8].start()
        ]
        self.assertIn('| Пастырский вопрос | Сочинение и издание | Объём изученного текста |', chapter)
        self.assertIn('| Откуда вражда к Богу? |', chapter)
        self.assertIn('34 абзаца, печатные с. 6–12', chapter)
        self.assertIn('| Для чего помнить Пятое ноября? |', chapter)
        self.assertIn('Весь основной цифровой текст с эпиграфом', chapter)
        self.assertIn('§§21.73–21.74', chapter)
        self.assertIn('§§21.88–21.90', chapter)
        self.assertNotIn('Начало на печатной с. 42', chapter)
        self.assertNotIn(
            'В трактате о провидении и памятной проповеди Пятого ноября изучены отдельные',
            chapter,
        )

    def test_manuscripts_and_reader_have_no_invisible_or_mixed_script_typos(self):
        """Catch invisible soft hyphens and Cyrillic/Latin homoglyphs in prose."""
        invisible = re.compile(r'[\u00ad\u200b\u200c\u200d\u2060\ufeff]')
        mixed_word = re.compile(r'(?:[A-Za-z][А-Яа-яЁё]|[А-Яа-яЁё][A-Za-z])')
        texts = [(str(PREVIEW), self.body)]
        for name in MANUSCRIPTS:
            path = ROOT / MANUSCRIPT_DIR / name
            texts.append((name, path.read_text(encoding='utf-8')))
        for name, text in texts:
            with self.subTest(file=name):
                self.assertIsNone(invisible.search(text), name)
                self.assertIsNone(mixed_word.search(text), name)

    def test_no_duplicate_horizontal_rules_between_chapters(self):
        self.assertNotRegex(self.body, r'(?m)^---[ \t]*\n\s*---[ \t]*$')

    def test_research_links_survive_path_preserving_move(self):
        links = LINK.findall(self.body)
        self.assertGreaterEqual(len(links), 230)
        for link in links:
            path_part = unquote(link.split('#', 1)[0].strip())
            resolved = (PREVIEW.parent / path_part).resolve()
            self.assertTrue(resolved.is_relative_to(ROOT), link)
            self.assertTrue(resolved.exists(), link)


if __name__ == '__main__':
    unittest.main()
