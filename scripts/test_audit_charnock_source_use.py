"""Synthetic extraction mechanics;fixtures are not historical source evidence."""
import hashlib
from pathlib import Path
import tempfile
import unittest
from audit_charnock_source_use import extract, PROBES, body_text_and_pages


class SourceUseTests(unittest.TestCase):
    def fixture(self, missing=False, duplicate=False):
        divisions = []
        for index, (identifier, probe) in enumerate(PROBES.items()):
            start, target = [(620, 621), (710, 710), (729, 729)][index]
            value = 'not found' if missing and index == 0 else probe
            if duplicate and index == 0:
                value += ' ' + probe
            divisions.append(f'<div type="discourse"><head>Fixture{index}</head><pb n="{start}"/>'
                             f'<p>Before. <pb n="{target}"/>{value}'
                             '<note>Named reference.</note> After.</p></div>')
        raw = ('<TEI xmlns="http://www.tei-c.org/ns/1.0"><text><body>'
               + ''.join(divisions) + '</body></text></TEI>').encode()
        registry = {'sources': {'A32723': {'size': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}}}
        return raw, registry

    def run_fixture(self, raw, registry):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'fixture.xml'
            path.write_bytes(raw)
            return extract(path, registry)

    def test_three_source_contexts(self):
        result = self.run_fixture(*self.fixture())
        self.assertEqual(set(result), set(PROBES))

    def test_paragraph_and_note_pages_distinct(self):
        result = self.run_fixture(*self.fixture())['CASE-LINGENDES']
        self.assertEqual(result['paragraphStartTeiPage'], '620')
        self.assertEqual(result['probeTeiPages'], ['621'])
        self.assertEqual(result['marginalNotes'][0]['teiPage'], '621')
        self.assertNotIn('Named reference', result['bodyParagraph'])
        self.assertIn('After.', result['bodyParagraph'])

    def test_wrong_bytes_fail(self):
        raw, registry = self.fixture()
        with self.assertRaisesRegex(ValueError, 'byte pin'):
            self.run_fixture(raw + b' ', registry)

    def test_missing_probe_fails(self):
        with self.assertRaisesRegex(ValueError, 'not found'):
            self.run_fixture(*self.fixture(missing=True))

    def test_duplicate_probe_fails(self):
        with self.assertRaisesRegex(ValueError, 'not unique'):
            self.run_fixture(*self.fixture(duplicate=True))

    def test_note_free_locator_view_retains_tails(self):
        raw = ('<TEI xmlns="http://www.tei-c.org/ns/1.0"><text><body><pb n="621"/>'
               '<p>He seemed<note>Marginal reference.<pb n="999"/></note> to descend'
               '<fw>Running header.</fw> for a time.</p></body></text></TEI>').encode()
        text, pages = body_text_and_pages(raw)
        self.assertEqual(text, 'He seemed to descend for a time.')
        self.assertEqual(set(pages), {'621'})

    def test_note_free_view_preserves_real_page_crossing(self):
        raw = ('<TEI xmlns="http://www.tei-c.org/ns/1.0"><text><body><pb n="710"/>'
               '<p>First <pb n="711"/>second.</p></body></text></TEI>').encode()
        text, pages = body_text_and_pages(raw)
        self.assertEqual(text, 'First second.')
        self.assertEqual(list(dict.fromkeys(pages)), ['710', '711'])
        self.assertEqual(len(text),len(pages))

    def test_note_free_view_normalizes_long_s_without_losing_labels(self):
        raw = ('<TEI xmlns="http://www.tei-c.org/ns/1.0"><text><body><pb n="729"/>'
               '<p>  Firſt   word. </p></body></text></TEI>').encode()
        text, pages = body_text_and_pages(raw)
        self.assertEqual(text, 'First word.')
        self.assertEqual(len(text),len(pages))

    def test_deterministic(self):
        data = self.fixture()
        self.assertEqual(self.run_fixture(*data), self.run_fixture(*data))



class AcquisitionBoundaryTests(unittest.TestCase):
    def plan(self):
        import json
        return json.loads((Path(__file__).resolve().parents[1] / 'data/charnock-series-editorial-plan-v1.json').read_text())

    def check(self, plan):
        from audit_charnock_source_use import check_acquisition_boundary
        return check_acquisition_boundary(plan)

    def test_saved_bounded_record(self):
        self.assertEqual(self.check(self.plan()), 3)

    def test_no_global_absence(self):
        p = self.plan()
        p['counterpartAcquisitionReview']['allDriveAbsenceProven'] = True
        with self.assertRaises(ValueError): self.check(p)

    def test_truncated_search_not_exhaustive(self):
        p = self.plan()
        p['counterpartAcquisitionReview']['partialQuery']['usedForExhaustiveConclusion'] = True
        with self.assertRaises(ValueError): self.check(p)

    def test_no_raw_promotion(self):
        p = self.plan()
        p['counterpartAcquisitionReview']['completedQueries'][2]['returnedFiles'][0]['classification'] = 'RAW'
        with self.assertRaises(ValueError): self.check(p)

    def test_source_pin_bound(self):
        p = self.plan()
        p['sourceUseCases'][0]['acquisitionBoundaryReview']['sourceContextSha256'] = '0'*64
        with self.assertRaises(ValueError): self.check(p)

    def test_no_claim_or_hold_clearance(self):
        for field, value in [('excludedUntilAcquired', []), ('holds', []), ('publicationState', 'APPROVED')]:
            with self.subTest(field=field):
                p = self.plan()
                p['sourceUseCases'][0]['acquisitionBoundaryReview'][field] = value
                with self.assertRaises(ValueError): self.check(p)

    def test_no_ed02_closure(self):
        p = self.plan()
        next(t for t in p['tasks'] if t['id']=='ED-02')['status'] = 'DONE_BOUNDED'
        with self.assertRaises(ValueError): self.check(p)


if __name__ == '__main__':
    unittest.main()
