"""Negative controls for Charnock manuscript lint, offline and read-only."""
import tempfile
import unittest
from pathlib import Path

from audit_charnock_manuscripts import MANUSCRIPT_DIR, MANUSCRIPTS, audit


class ManuscriptStructureTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.manuscripts = self.root / MANUSCRIPT_DIR
        self.manuscripts.mkdir(parents=True)
        (self.root / 'БИОГРАФИИ/Стивен Чарнок' / '00_README_AND_NAVIGATION.md').write_text('# Owner\n', encoding='utf-8')
        for name in MANUSCRIPTS:
            (self.manuscripts / name).write_text(
                '# Draft\nDRAFT / RESEARCH_ONLY / PUBLICATION_HOLD\n\n'
                '## Глава\nClaim.[^1] [owner](../00_README_AND_NAVIGATION.md)\n\n'
                '## Источниковые примечания\n'
                '[^1]: Source, printed p. 2.\n\n'
                '## Редакторская приёмка — вне читательского текста\n'
                'DRAFT / RESEARCH_ONLY / PUBLICATION_HOLD\n', encoding='utf-8')

    def modify(self, addition):
        file = self.manuscripts / MANUSCRIPTS[0]
        file.write_text(file.read_text(encoding='utf-8') + addition, encoding='utf-8')

    def test_valid(self):
        result = audit(self.root)
        self.assertEqual(result['manuscripts'], 10)
        self.assertEqual(result['footnotes'], 10)
        self.assertEqual(result['internalTargets'], 1)

    def test_missing_file(self):
        (self.manuscripts / MANUSCRIPTS[1]).unlink()
        with self.assertRaisesRegex(ValueError, 'missing manuscript'):
            audit(self.root)

    def test_missing_definition(self):
        self.modify('Bad citation.[^missing]\n')
        with self.assertRaisesRegex(ValueError, 'undefined footnote'):
            audit(self.root)

    def test_duplicate_definition(self):
        self.modify('[^1]: Duplicate definition.\n')
        with self.assertRaisesRegex(ValueError, 'duplicate footnote'):
            audit(self.root)

    def test_unused_definition(self):
        self.modify('[^9]: Unused.\n')
        with self.assertRaisesRegex(ValueError, 'unused footnote'):
            audit(self.root)

    def test_dead_relative_link(self):
        self.modify('[broken](../absent.md)\n')
        with self.assertRaisesRegex(ValueError, 'broken relative target'):
            audit(self.root)

    def test_outside_root_link(self):
        self.modify('[escape](../../../../absent.md)\n')
        with self.assertRaisesRegex(ValueError, 'broken relative target'):
            audit(self.root)

    def test_missing_hold_in_header(self):
        path = self.manuscripts / MANUSCRIPTS[0]
        path.write_text(path.read_text(encoding='utf-8').replace('PUBLICATION_HOLD', 'RELEASED'), encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'missing PUBLICATION_HOLD'):
            audit(self.root)


    def test_missing_source_heading(self):
        path = self.manuscripts / MANUSCRIPTS[0]
        path.write_text(path.read_text(encoding='utf-8').replace(
            '## Источниковые примечания', '## Неизвестный раздел'), encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'expected exactly one sources section'):
            audit(self.root)

    def test_missing_backstage_heading(self):
        path = self.manuscripts / MANUSCRIPTS[0]
        path.write_text(path.read_text(encoding='utf-8').replace(
            '## Редакторская приёмка', '## Другое название'), encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'expected exactly one backstage section'):
            audit(self.root)

    def test_swapped_source_and_backstage_headings(self):
        path = self.manuscripts / MANUSCRIPTS[0]
        content = path.read_text(encoding='utf-8')
        content = content.replace('## Источниковые примечания', '## SWAP')
        content = content.replace('## Редакторская приёмка', '## Источниковые примечания')
        content = content.replace('## SWAP', '## Редакторская приёмка')
        path.write_text(content, encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'sources section must precede backstage'):
            audit(self.root)

    def test_backstage_must_be_final_section(self):
        self.modify('\n## Another chapter\nMust not follow backstage.\n')
        with self.assertRaisesRegex(ValueError, 'backstage must be the final'):
            audit(self.root)

    def test_note_definition_not_in_backstage(self):
        path = self.manuscripts / MANUSCRIPTS[0]
        content = path.read_text(encoding='utf-8')
        content = content.replace('[^1]: Source, printed p. 2.\n', '')
        path.write_text(content + '\n[^1]: Source, printed p. 2.\n', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'footnote definition outside sources'):
            audit(self.root)

    def test_backstage_citation_does_not_count_as_reader_usage(self):
        path = self.manuscripts / MANUSCRIPTS[0]
        content = path.read_text(encoding='utf-8').replace('Claim.[^1]', 'Claim.')
        content = content.replace(
            'DRAFT / RESEARCH_ONLY / PUBLICATION_HOLD\n',
            'DRAFT / RESEARCH_ONLY / PUBLICATION_HOLD\n',
            1
        )
        content += '\nEditorial reference only.[^1]\n'
        path.write_text(content, encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'not cited by reader text'):
            audit(self.root)

    def test_source_only_citation_does_not_count_as_reader_usage(self):
        path = self.manuscripts / MANUSCRIPTS[0]
        content = path.read_text(encoding='utf-8').replace('Claim.[^1]', 'Claim.')
        content = content.replace('[^1]: Source, printed p. 2.', 'See [^1].\n[^1]: Source, printed p. 2.')
        path.write_text(content, encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'not cited by reader text'):
            audit(self.root)

    def test_editorial_word_in_reader_heading_is_not_backstage(self):
        path = self.manuscripts / MANUSCRIPTS[0]
        content = path.read_text(encoding='utf-8').replace(
            '## Источниковые примечания',
            '## Что действительно подтверждает редакторскую похвалу\n'
            'Текст исследования.\n\n## Источниковые примечания')
        path.write_text(content, encoding='utf-8')
        self.assertEqual(audit(self.root)['footnotes'], 10)


if __name__ == '__main__':
    unittest.main()
