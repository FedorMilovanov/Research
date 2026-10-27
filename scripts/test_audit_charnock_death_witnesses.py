"""Calendar arithmetic and fail-closed witness boundaries;no event date adjudication."""
import copy
import datetime
import json
from pathlib import Path
import tempfile
import unittest
from audit_charnock_death_witnesses import ROOT, jdn, calendar_review, check_review, check_supplements


class CalendarTests(unittest.TestCase):
    def test_standard_jdn_anchor(self):
        self.assertEqual(jdn(2000,1,1,'GREGORIAN'),2451545)

    def test_julian_wednesday_matches_printed_weekday_only(self):
        row = calendar_review()['rows'][1]
        self.assertEqual(row['julianWeekday'],'Wednesday')
        self.assertEqual(row['prolepticGregorianWeekday'],'Sunday')
        self.assertEqual(datetime.date.fromisoformat(row['equivalentGregorianDate']).weekday(),2)

    def test_style_offset_is_ten_not_one(self):
        rows = calendar_review()['rows']
        self.assertEqual({r['calendarOffsetDays'] for r in rows},{10})
        self.assertEqual(rows[0]['equivalentGregorianDate'],'1680-08-06')
        self.assertEqual(rows[1]['equivalentGregorianDate'],'1680-08-07')
        self.assertFalse(calendar_review()['deathConflictResolved'])

    def test_burial_conversion_separate_from_death(self):
        row = calendar_review()['rows'][2]
        self.assertEqual(row['julianWeekday'],'Friday')
        self.assertEqual(row['equivalentGregorianDate'],'1680-08-09')

    def test_leap_rules_are_calendar_specific(self):
        self.assertIsInstance(jdn(1900,2,29,'JULIAN'),int)
        with self.assertRaisesRegex(ValueError,'Invalid calendar date'):
            jdn(1900,2,29,'GREGORIAN')

    def test_calendar_must_be_explicit(self):
        with self.assertRaisesRegex(ValueError,'Explicit'):
            jdn(1680,7,28,'OLD_STYLE_ASSUMED')


class DeathWitnessTests(unittest.TestCase):
    def setUp(self):
        self.plan = json.loads((ROOT/'data/charnock-series-editorial-plan-v1.json').read_text())
        self.registry = json.loads((ROOT/self.plan['baselineRegistry']).read_text())
        self.review = self.plan['deathWitnessReview']

    def check(self):
        return check_review(self.plan,self.registry)

    def test_current_conflict_retained(self):
        self.assertFalse(self.check()['deathConflictResolved'])

    def test_majority_not_resolution(self):
        self.review['deathConflictResolved'] = True
        with self.assertRaisesRegex(ValueError,'retain event conflict'):
            self.check()

    def test_anonymous_objects_not_independent_votes(self):
        self.review['independenceEstablished'] = True
        with self.assertRaisesRegex(ValueError,'independence'):
            self.check()

    def test_wood_continuation_is_not_stephen(self):
        self.review['byteVerifiedContexts']['A71277']['continuationBelongsToStephen'] = True
        with self.assertRaisesRegex(ValueError,'Thomas'):
            self.check()

    def test_thomas_family_cannot_enter_stephen_context(self):
        self.review['byteVerifiedContexts']['A71277']['stephenContext'] += ' Agnes Norden'
        with self.assertRaisesRegex(ValueError,'Thomas'):
            self.check()

    def test_sayings_date_not_silently_corrected(self):
        self.review['byteVerifiedContexts']['B02133']['heading'] = 'THE SAYINGS July 27, 1680'
        with self.assertRaisesRegex(ValueError,'cannot be silently corrected'):
            self.check()

    def test_supplement_not_retroactive_historical_handoff(self):
        self.review['supplementalSources']['A52960']['inHistoricalHandoff'] = True
        with self.assertRaisesRegex(ValueError,'historical custody'):
            self.check()

    def test_text_licence_not_image_approval(self):
        self.review['supplementalSources']['A52960']['rightsScope'] = 'TEXT_AND_IMAGES'
        with self.assertRaisesRegex(ValueError,'does not approve images'):
            self.check()

    def test_supplement_bytes_actually_checked(self):
        sources = copy.deepcopy(self.review['supplementalSources'])
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for source in sources.values():
                target = root/source['localPath']
                target.parent.mkdir(parents=True,exist_ok=True)
                target.write_bytes((ROOT/source['localPath']).read_bytes())
            source = sources['A52960']
            target = root/source['localPath']
            target.write_bytes(target.read_bytes()+b' ')
            with self.assertRaisesRegex(ValueError,'byte pin mismatch'):
                check_supplements(sources,root)

    def test_witness_source_holds_not_removed(self):
        self.review['witnessDecisions'][0]['sourceStateSnapshot']['holds'] = []
        with self.assertRaisesRegex(ValueError,'cannot promote source axes'):
            self.check()


if __name__ == '__main__':
    unittest.main()
