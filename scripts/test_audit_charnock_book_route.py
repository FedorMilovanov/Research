"""Synthetic XML fixtures test extraction mechanics,not historical evidence."""
import hashlib
from pathlib import Path
import tempfile
import unittest

from audit_charnock_book_route import extract, plain
import xml.etree.ElementTree as ET


class BookRouteTests(unittest.TestCase):
    def fixture(self, count=14, omit_probe=False):
        probes = {2: 'Men may have Atheistical hearts', 3: 'THE words are part',
                  6: 'The Creation was a real change', 14: 'THE Subject of this'}
        parts = []
        for number in range(1, count + 1):
            text = probes.get(number, 'Ordinary paragraph')
            if omit_probe and number == 2:
                text = 'No target'
            parts.append(f'<div type="discourse"><pb n="{number}"/><head>Test {number}</head>'
                         f'<p>Before</p><p>{text}<note>Not authorial prose</note> tail</p>'
                         '<p>After</p><p>Next</p></div>')
        raw = ('<TEI xmlns="http://www.tei-c.org/ns/1.0"><text><body>' + ''.join(parts)
               + '</body></text></TEI>').encode()
        registry = {'sources': {'A32723': {'size': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}}}
        return raw, registry

    def run_fixture(self, raw, registry):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'fixture.xml'
            path.write_bytes(raw)
            return extract(path, registry)

    def test_fourteen_routes_four_contexts(self):
        report = self.run_fixture(*self.fixture())
        self.assertEqual(len(report['route']), 14)
        self.assertEqual(len(report['contexts']), 4)

    def test_bad_sha_fails(self):
        raw, registry = self.fixture()
        with self.assertRaisesRegex(ValueError, 'SHA mismatch'):
            self.run_fixture(raw + b' ', registry)

    def test_wrong_discourse_count_fails(self):
        with self.assertRaisesRegex(ValueError, 'fourteen'):
            self.run_fixture(*self.fixture(count=13))

    def test_missing_probe_fails(self):
        with self.assertRaisesRegex(ValueError, 'exactly one'):
            self.run_fixture(*self.fixture(omit_probe=True))

    def test_note_removed_tail_preserved(self):
        report = self.run_fixture(*self.fixture())
        text = report['contexts'][0]['contextWindow'][1]['text']
        self.assertNotIn('Not authorial prose', text)
        self.assertTrue(text.endswith(' tail'))
        self.assertEqual(report['route'][0]['noteElements'], 1)

    def test_normalization(self):
        node = ET.fromstring('<p xmlns="http://www.tei-c.org/ns/1.0">firſt <fw>header</fw> next</p>')
        self.assertEqual(plain(node), 'first next')

    def test_no_epigraph_invented(self):
        report = self.run_fixture(*self.fixture())
        self.assertIsNone(report['route'][0]['epigraph'])

    def test_deterministic(self):
        data = self.fixture()
        self.assertEqual(self.run_fixture(*data), self.run_fixture(*data))


if __name__ == '__main__':
    unittest.main()
