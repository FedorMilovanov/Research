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
                'Claim.[^1] [owner](../00_README_AND_NAVIGATION.md)\n\n'
                '[^1]: Source, printed p. 2.\n', encoding='utf-8')

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


if __name__ == '__main__':
    unittest.main()
