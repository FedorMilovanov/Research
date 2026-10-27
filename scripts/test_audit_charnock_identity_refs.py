"""Small offline tests; fixtures do not stand in for historical source evidence."""
import hashlib
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import audit_charnock_identity_refs as audit


class IdentityExtractionTests(unittest.TestCase):
    def run_fixture(self, xml):
        raw = xml.encode('utf-8')
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'fixture.xml'
            path.write_bytes(raw)
            pinned = {'A32723': ('fixture-only', hashlib.sha256(raw).hexdigest())}
            with patch.object(audit, 'SOURCES', pinned):
                before = path.read_bytes()
                result = audit.extract(path)
                self.assertEqual(path.read_bytes(), before)
                return result

    def test_note_scope_context_and_printed_page(self):
        result = self.run_fixture('''<TEI xmlns="http://www.tei-c.org/ns/1.0">
        <teiHeader><note>Lingend metadata</note></teiHeader>
        <text><body><pb n="621"/><p>Context
        <note>Lingend de Euchariſt, p. 84, 85.</note> tail</p>
        <p>Raynaud without a note</p></body></text></TEI>''')
        self.assertEqual(result['counts']['LING'], 1)
        self.assertEqual(result['counts']['RAY'], 0)
        self.assertEqual(result['notes'][0]['printed_page_label'], '621')
        self.assertIn('Eucharist', result['notes'][0]['note'])
        self.assertIn('Context', result['notes'][0]['parent_context'])
        self.assertIn('tail', result['notes'][0]['parent_context'])

    def test_page_label_is_not_invented(self):
        result = self.run_fixture('''<TEI xmlns="http://www.tei-c.org/ns/1.0">
        <text><p><note>Sanct. in loc.</note></p></text></TEI>''')
        self.assertIsNone(result['notes'][0]['printed_page_label'])

    def test_nearest_discourse_heading_not_nested_section(self):
        result = self.run_fixture('''<TEI xmlns="http://www.tei-c.org/ns/1.0">
        <text><body><div type="discourse"><head>Gods <hi>Dominion</hi>.</head>
        <div type="section"><head>Election</head><pb n="729"/>
        <p><note>Dalle in loc.</note></p></div></div>
        <div type="discourse"><head>Other discourse</head></div></body></text></TEI>''')
        self.assertEqual(result['notes'][0]['discourse_heading'], 'Gods Dominion.')

    def test_missing_discourse_heading_is_not_inferred(self):
        result = self.run_fixture('''<TEI xmlns="http://www.tei-c.org/ns/1.0">
        <text><div type="discourse"><p><note>Dalle in loc.</note></p></div></text></TEI>''')
        self.assertIsNone(result['notes'][0]['discourse_heading'])

    def test_inventory_separates_preface_and_discourse_notes(self):
        result = self.run_fixture('''<TEI xmlns="http://www.tei-c.org/ns/1.0">
        <teiHeader><note>metadata excluded</note></teiHeader>
        <text><front><p><note>preface</note></p></front><body>
        <div type="discourse"><head>First</head><p><note>Dalle</note>
        <note>Other author</note></p></div></body></text></TEI>''')
        inv = result['witness_inventory']
        self.assertEqual(inv['text_note_elements'], 3)
        self.assertEqual(inv['discourse_note_elements'], 2)
        self.assertEqual(inv['outside_discourses_note_elements'], 1)
        self.assertEqual(inv['discourse_divisions'], 1)
        self.assertEqual(result['counts']['DAIL'], 1)

    def test_nested_discourse_notes_not_double_counted_in_total(self):
        result = self.run_fixture('''<TEI xmlns="http://www.tei-c.org/ns/1.0">
        <text><div type="discourse"><head>Outer</head><note>One</note>
        <div type="discourse"><head>Inner</head><note>Two</note></div>
        </div></text></TEI>''')
        inv = result['witness_inventory']
        self.assertEqual(inv['discourse_note_elements'], 2)
        self.assertEqual(inv['outside_discourses_note_elements'], 0)
        self.assertEqual(inv['discourse_divisions'], 2)

    def test_raynard_variant_and_separate_pages(self):
        result = self.run_fixture('''<TEI xmlns="http://www.tei-c.org/ns/1.0">
        <text><pb n="710"/><p><note>Raynaud. Theolog. Natural.</note></p>
        <pb n="776"/><p><note>Raynard de Deo p. 766.</note></p></text></TEI>''')
        self.assertEqual(result['counts']['RAY'], 2)
        self.assertEqual([n['printed_page_label'] for n in result['notes']], ['710', '776'])

    def test_parent_and_note_can_be_on_different_pages(self):
        result = self.run_fixture('''<TEI xmlns="http://www.tei-c.org/ns/1.0">
        <text><pb n="229"/><p><note>Placeus</note> opening
        <pb n="230"/><note>Daile Melang des Sermons</note> ending</p></text></TEI>''')
        self.assertEqual(result['counts']['DAIL'], 1)
        self.assertEqual(result['notes'][1]['printed_page_label'], '230')
        self.assertEqual(result['notes'][1]['parent_start_page_label'], '229')

    def test_daille_variants_and_non_note_exclusion(self):
        result = self.run_fixture('''<TEI xmlns="http://www.tei-c.org/ns/1.0">
        <text><p>Daillé outside note<note>Daillè Serm.</note>
        <note>Dail••é</note><note>Dalle in loc.</note>
        <note>Daily bread</note></p></text></TEI>''')
        # 'daily' must not be counted as an author's name.
        self.assertEqual(result['counts']['DAIL'], 3)

    def test_second_witness_uses_its_own_pin(self):
        raw = b'<TEI xmlns="http://www.tei-c.org/ns/1.0"><text><p><note>Daille</note></p></text></TEI>'
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'second.xml'
            path.write_bytes(raw)
            pins = {'A32723': ('first', '0' * 64),
                    'A32724': ('second', hashlib.sha256(raw).hexdigest())}
            with patch.object(audit, 'SOURCES', pins):
                result = audit.extract(path, 'A32724')
                self.assertEqual(result['tcp'], 'A32724')
                self.assertEqual(result['revision'], 'second')
                self.assertEqual(result['counts']['DAIL'], 1)
                with self.assertRaisesRegex(ValueError, 'A32723: SHA-256 mismatch'):
                    audit.extract(path)
                self.assertEqual(path.read_bytes(), raw)

    def test_non_charnock_witness_rejected(self):
        with self.assertRaisesRegex(ValueError, 'Unsupported Charnock witness'):
            audit.extract(Path('not-read.xml'), 'A35345')

    def test_missing_text_is_rejected(self):
        with self.assertRaisesRegex(ValueError, 'no TEI text body'):
            self.run_fixture('<TEI xmlns="http://www.tei-c.org/ns/1.0"/>')

    def test_bad_checksum_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'bad.xml'
            path.write_text('<wrong/>')
            with self.assertRaisesRegex(ValueError, 'SHA-256 mismatch'):
                audit.extract(path)


if __name__ == '__main__':
    unittest.main()
