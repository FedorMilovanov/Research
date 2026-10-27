"""Synthetic fixtures;not records of acquired historical books."""
import hashlib
from pathlib import Path
import tempfile
import unittest
from audit_charnock_publication_titles import extract


class PublicationTitleTests(unittest.TestCase):
    def fixture(self, count=7, missing=False, duplicate=False):
        files, units, sources = {}, [], {}
        for i in range(count):
            identifier = 'FIXTURE' + str(i)
            title = '' if missing and i == 0 else '<div type="title_page"><p>TITLE ' + str(i) + '</p></div>'
            if duplicate and i == 0:
                title += '<div type="title_page"><p>OTHER TITLE</p></div>'
            raw = ('<TEI xmlns="http://www.tei-c.org/ns/1.0"><text><front>'
                   '<div type="half_title"><p>HALF TITLE NOT FULL TITLE</p></div>' + title
                   + '<div type="to_the_reader"><p>PREFACE NOT TITLE</p></div></front>'
                   '<body><p>Body</p></body></text></TEI>').encode()
            files[identifier + '.xml'] = raw
            units.append(dict(id='PUB-' + str(i), source=identifier, unitType='PRINTED_OBJECT'))
            sources[identifier] = dict(size=len(raw), sha256=hashlib.sha256(raw).hexdigest())
        units.append(dict(id='UNACQUIRED-FAMILY', unitType='ACQUISITION_FAMILY'))
        return files, dict(sources=sources, bibliographyUnits=units)

    def run_fixture(self, files, registry):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name, raw in files.items():
                (root / name).write_bytes(raw)
            return extract(root, registry)

    def test_seven_titles_not_family_acquisition(self):
        result = self.run_fixture(*self.fixture())
        self.assertEqual(len(result), 7)

    def test_half_title_not_used(self):
        result = self.run_fixture(*self.fixture())
        self.assertEqual(result['PUB-0']['titleText'], 'TITLE 0')

    def test_preface_not_included(self):
        result = self.run_fixture(*self.fixture())
        self.assertNotIn('PREFACE', result['PUB-0']['titleText'])

    def test_bad_bytes_fail(self):
        files, registry = self.fixture()
        files['FIXTURE0.xml'] += b' '
        with self.assertRaisesRegex(ValueError, 'byte pin'):
            self.run_fixture(files, registry)

    def test_missing_title_cannot_fall_back_to_half_title(self):
        with self.assertRaisesRegex(ValueError, 'explicit title_page'):
            self.run_fixture(*self.fixture(missing=True))

    def test_duplicate_title_fails(self):
        with self.assertRaisesRegex(ValueError, 'explicit title_page'):
            self.run_fixture(*self.fixture(duplicate=True))

    def test_wrong_object_count_fails(self):
        with self.assertRaisesRegex(ValueError, 'Seven printed'):
            self.run_fixture(*self.fixture(count=6))

    def test_deterministic(self):
        data = self.fixture()
        self.assertEqual(self.run_fixture(*data), self.run_fixture(*data))


if __name__ == '__main__':
    unittest.main()
