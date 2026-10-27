"""Packaging regressions; keep the historical atlas test packet byte-identical."""
from pathlib import Path
import unittest


class MergePackagingTests(unittest.TestCase):
    def test_department_navigation_counts_research_documents_not_chapters(self):
        root = Path(__file__).resolve().parents[1]
        navigation = (root / 'БИОГРАФИИ/00_README_AND_NAVIGATION.md').read_text()
        for department in ('Джон Гилл', 'Стивен Чарнок'):
            row = next(line for line in navigation.splitlines() if line.startswith('| [`' + department + '/`'))
            count = len(list((root / 'БИОГРАФИИ' / department).glob('*.md')))
            self.assertEqual(int(row.split('|')[3].strip()), count)
        self.assertIn('Документов Research', navigation)

    def test_source_download_cache_is_not_a_durable_evidence_directory(self):
        root = Path(__file__).resolve().parents[1]
        self.assertIn('.cache/', (root / '.gitignore').read_text().splitlines())


if __name__ == "__main__":
    unittest.main()
