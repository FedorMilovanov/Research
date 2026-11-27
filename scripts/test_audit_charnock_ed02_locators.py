"""Fail-closed provenance guards for the two distinct Lingendes references.

These checks preserve the evidence boundary; they do NOT verify a facsimile,
re-read the external facsimile, review translations, or authorize publication.
"""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHAPTER = (
    ROOT / "БИОГРАФИИ/Стивен Чарнок/manuscripts/"
    "II_UCHENYI_I_PROPOVEDNIK_WORKING_DRAFT.md"
)
DOSSIER = (
    ROOT / "БИОГРАФИИ/Стивен Чарнок/supplemental-audits/"
    "ED02_LINGENDES_84_87_TO_CHARNOCK_621_ALIGNMENT_2026-11-18.md"
)
RECEIPT = ROOT / "data/charnock-editorial-book-receipt-v1-20261123-pr629.json"
VISUAL = (
    ROOT / "БИОГРАФИИ/Стивен Чарнок/supplemental-audits/"
    "ED02_1699_N520_PRINTED_521_MARGINAL_185_VISUAL_2026-11-23.md"
)
DEFINITIONS = re.compile(r"(?ms)^\[\^(\d+)\]:\s*(.*?)(?=^\[\^\d+\]:|^---\s*$|\Z)")


def get_note(source, number):
    notes = dict(DEFINITIONS.findall(source))
    return notes[number]


class CharnockED02LocatorGuards(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manuscript = CHAPTER.read_text(encoding="utf-8")
        cls.dossier = DOSSIER.read_text(encoding="utf-8")
        cls.note_1682 = get_note(cls.manuscript, "8")
        cls.note_1699 = get_note(cls.manuscript, "9")

    def test_1682_printed_84_85_not_silently_emended_to_87(self):
        note = self.note_1682
        self.assertIn("Charnock A32723", note)
        self.assertIn("печатная p.621", note)
        self.assertIn("p.84,85", note)
        self.assertIn("pp.84–87", note)
        self.assertIn("Не исправлять печатную сноску на p.87", note)

    def test_1699_n520_printed_p521_replaces_unreliable_513(self):
        # Recorded human visual witness: test checks exact attribution and caveats,
        # it does NOT itself independently reopen or parse the external facsimile.
        note = self.note_1699
        self.assertIn("London, 1699", note)
        self.assertIn("кадре 520", note)
        self.assertIn("печатную **p.521**", note)
        self.assertIn("достоверный номер этого листа — p.521", note)
        self.assertIn("n520 к p.513", note)
        self.assertIn("confidence=null", note)
        self.assertIn("опровергнута визуально", note)
        self.assertIn("EARLY_1699_IMAGE_OCR_CORROBORATED", note)
        self.assertIn("EARLY_1699_IMAGE_WITNESS_VERIFIED", note)
        self.assertIn("CATALOG_ONLY", note)

    def test_visual_witness_records_same_leaf_header_and_margin(self):
        proof = VISUAL.read_text(encoding="utf-8")
        self.assertIn("leaf n520", proof)
        self.assertIn("печатная p. 521", proof)
        self.assertIn("p. 185", proof)
        self.assertIn("_0520.jp2", proof)
        self.assertIn("pct:0,0,100,25/1600,", proof)
        self.assertIn("pct:65,42,35,48/1800,", proof)
        self.assertIn("1684", proof)
        self.assertIn("PUBLICATION_HOLD", proof)

    def test_1699_and_1682_marginalia_stay_distinct(self):
        self.assertIn("p.84,85", self.note_1682)
        self.assertIn("p. 185.", self.note_1699)
        self.assertIn("ссылка 1682", self.note_1699)
        self.assertIn("отдельная нерешённая колляция", self.note_1699)
        self.assertIn("ED-02 LOCATOR_HOLD", self.dossier)

    def test_custody_receipt_is_specific_to_pinned_source_not_release(self):
        receipt = json.loads(RECEIPT.read_text(encoding="utf-8"))
        self.assertEqual(
            receipt["sourceGitSha"],
            "21b9cbbc2961a772bc36c5bc1790bcd3952a092f",
        )
        self.assertEqual(receipt["sourceFileCount"], 17)
        self.assertEqual(receipt["manuscriptCount"], 10)
        self.assertEqual(receipt["editorialReaderCount"], 1)
        self.assertTrue(receipt["sourceDestinationExactByteMatch"])
        self.assertEqual(
            receipt["archiveSha256"], receipt["destinationSha256Readback"]
        )
        self.assertEqual(receipt["archiveBytes"], receipt["destinationBytesReadback"])
        self.assertEqual(receipt["publicationState"], "BLOCKED")
        self.assertEqual(receipt["independentTranslationReview"], "0/12")
        for hold in ("ED02_LOCATOR_HOLD", "ED06_INDEPENDENT_REVIEW_HOLD",
                     "RIGHTS_HOLD", "PUBLICATION_HOLD"):
            self.assertIn(hold, receipt["holds"])


if __name__ == "__main__":
    unittest.main()
