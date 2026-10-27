"""Synthetic TCP-shaped fixtures;no historical books invented by these tests."""
import hashlib
from pathlib import Path
import tempfile
import unittest
from audit_charnock_translation_contexts import TARGETS, extract


class TranslationContextTests(unittest.TestCase):
    def fixture(self, signature='Edw. Veel.', licence=None, duplicate=False, heading=True):
        if licence is None:
            licence = ('This keyboarded and encoded edition of the work described above is co-owned. '
                       'This text is available for reuse, according to the terms of Creative Commons 0 1.0 Universal licence. '
                       'The text can be copied, modified, distributed and performed, even for commercial purposes, all without asking permission.')
        raw = {}
        for identifier in ['A32724', 'A32726', 'B20167']:
            header = '<teiHeader><fileDesc><publicationStmt><availability><p>' + licence + '</p></availability></publicationStmt></fileDesc></teiHeader>'
            if identifier == 'B20167':
                front = '<front><div><head>Advertisement</head><p>' + TARGETS['TR-VEEL'][2] + ', fixture only.</p><p>Next.</p><signed>' + signature + '</signed></div></front>'
                title = 'Chiefest Sinners Objects of Choicest Mercy.' if heading else 'Other work'
                body = '<body><div><head>' + title + '</head><pb n="1"/><epigraph><p>Epigraph excluded from paragraph index.</p></epigraph><p>First observation.</p><p>' + TARGETS['TR-MERCY'][2] + '</p><p>For the last.</p></div></body>'
            else:
                key, page = ('TR-TXT03', '64') if identifier == 'A32724' else ('TR-TXT08', '7')
                probe = TARGETS[key][2]
                front = '<front/>'
                paragraph = '<p>' + probe + ' is uncertain.</p>'
                body = '<body><div><head>Fixture discourse</head><pb n="' + page + '"/><p>Before.</p>' + paragraph + (paragraph if duplicate else '') + '<p>After.</p></div></body>'
            raw[identifier] = ('<TEI xmlns="http://www.tei-c.org/ns/1.0">' + header + '<text>' + front + body + '</text></TEI>').encode()
        registry = dict(sources={k:dict(size=len(v), sha256=hashlib.sha256(v).hexdigest()) for k,v in raw.items()},
                        anchors=[dict(id='TXT-03',teiPages=['64']),dict(id='TXT-08',teiPages=['7']),dict(id='BIB-06',teiPages=[None])])
        return raw, registry

    def run_fixture(self, raw, registry):
        with tempfile.TemporaryDirectory() as directory:
            for key, value in raw.items():
                (Path(directory) / (key + '.xml')).write_bytes(value)
            return extract(Path(directory), registry)

    def test_four_contexts(self):
        self.assertEqual(len(self.run_fixture(*self.fixture())),4)

    def test_voice_separation(self):
        records = self.run_fixture(*self.fixture())
        self.assertEqual(records['TR-VEEL']['voice'], 'VEEL_EDITORIAL')
        self.assertEqual(records['TR-MERCY']['voice'], 'CHARNOCK_BODY')

    def test_epigraph_not_counted_as_body_paragraph(self):
        record = self.run_fixture(*self.fixture())['TR-MERCY']
        self.assertEqual(record['localParagraphIndexZeroBased'],1)
        self.assertNotIn('Epigraph', str(record['contextWindow']))

    def test_byte_pin_failure(self):
        raw, registry = self.fixture()
        raw['A32724'] += b' '
        with self.assertRaisesRegex(ValueError,'byte pin'):
            self.run_fixture(raw,registry)

    def test_unknown_licence_fails_closed(self):
        with self.assertRaisesRegex(ValueError,'licence not recognized'):
            self.run_fixture(*self.fixture(licence='Rights unknown'))

    def test_cc0_keyword_without_waiver_not_enough(self):
        with self.assertRaisesRegex(ValueError,'licence not recognized'):
            self.run_fixture(*self.fixture(licence='This work is NOT CC0'))

    def test_signature_required(self):
        with self.assertRaisesRegex(ValueError,'voice/section'):
            self.run_fixture(*self.fixture(signature='Unknown'))

    def test_unique_probe_required(self):
        with self.assertRaisesRegex(ValueError,'probe must be unique'):
            self.run_fixture(*self.fixture(duplicate=True))

    def test_page_one_not_enough_for_mercy_identity(self):
        with self.assertRaisesRegex(ValueError,'voice/section'):
            self.run_fixture(*self.fixture(heading=False))

    def test_wrong_printed_page_fails(self):
        raw, registry = self.fixture()
        registry['anchors'][0]['teiPages']=['65']
        with self.assertRaisesRegex(ValueError,'printed probe locator'):
            self.run_fixture(raw,registry)


if __name__ == '__main__':
    unittest.main()
