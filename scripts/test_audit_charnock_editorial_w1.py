"""Read-only objective checks for ED-09 ten-chapter and text-only release-scope QA.

This proves structure and source accounting, not philological approval or rights.
"""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "БИОГРАФИИ" / "Стивен Чарнок"
MANUSCRIPTS = BASE / "manuscripts"
READER = BASE / "reader-preview" / "CHARNOCK_FULL_BOOK_EDITORIAL_READER_2026-11-21.md"
NAV = BASE / "reader-preview" / "README.md"
REPORT = BASE / "supplemental-audits" / "ED09_FULL_BOOK_EDITORIAL_QA_AND_TEXT_RIGHTS_2026-11-21.md"
RECEIPT = ROOT / "data" / "charnock-editorial-book-receipt-v1-20261121.json"
EXTERNAL = BASE / "supplemental-audits" / "ED06_EXTERNAL_REVIEW_PACKET_ALL12_2026-11-18.md"
DEFS = re.compile(r"^\[\^([^]]+)\]:", re.MULTILINE)
CITES = re.compile(r"\[\^([^]]+)\]")
MEDIA = re.compile(r"!\[[^]]*\]\(|<\s*(?:img|video|audio|iframe|picture)\b|data:image/", re.IGNORECASE)
EMPTY_LINK = re.compile(r"\]\(\s*\)")
PLACEHOLDER = re.compile(r"\b(?:TODO|FIXME|TBD)\b")


class CharnockEditorialW1Tests(unittest.TestCase):
    def test_all_ten_manuscripts_have_fully_used_unique_note_ids(self):
        files = sorted(MANUSCRIPTS.glob("*_WORKING_DRAFT.md"))
        self.assertEqual(len(files), 10)
        counts = []
        for path in files:
            body = path.read_text(encoding="utf-8")
            definitions = DEFS.findall(body)
            citations = CITES.findall(body)
            self.assertEqual(len(definitions), len(set(definitions)), path.name)
            self.assertEqual(set(definitions), set(citations), path.name)
            self.assertIsNone(MEDIA.search(body), path.name)
            self.assertIsNone(EMPTY_LINK.search(body), path.name)
            self.assertIsNone(PLACEHOLDER.search(body), path.name)
            counts.append(len(definitions))
        self.assertEqual(sum(counts), 180)
        self.assertEqual(sorted(counts), sorted((13, 20, 18, 17, 18, 21, 20, 20, 19, 14)))

    def test_reader_is_text_only_and_180_notes_unambiguous(self):
        reader = READER.read_text(encoding="utf-8")
        ids = DEFS.findall(reader)
        self.assertEqual(len(ids), 180)
        self.assertEqual(len(set(ids)), 180)
        self.assertIsNone(MEDIA.search(reader))
        self.assertIsNone(EMPTY_LINK.search(reader))
        self.assertIsNone(PLACEHOLDER.search(reader))
        self.assertIn("DRAFT / RESEARCH_ONLY / PUBLICATION_HOLD", reader[:1500])

    def test_navigation_mentions_real_custody_and_no_stale_open_pr(self):
        nav = NAV.read_text(encoding="utf-8")
        receipt = json.loads(RECEIPT.read_text(encoding="utf-8"))
        self.assertIn("charnock-editorial-book-receipt-v1-20261121.json", nav)
        self.assertIn("PR #624 слит", nav)
        self.assertNotIn("создаётся в [PR #624]", nav)
        self.assertEqual(receipt["sourceFileCount"], 17)
        self.assertEqual(receipt["manuscriptCount"], 10)
        self.assertTrue(receipt["sourceDestinationExactByteMatch"])
        self.assertEqual(receipt["sourceGitSha"], "962010d55e38cabf3f0c04670ec16a9d5a80704e")
        self.assertIn("PUBLICATION_HOLD", receipt["holds"])
        self.assertIn("DRAFT / RESEARCH_ONLY / PUBLICATION_HOLD", nav)

    def test_12_review_ids_proposed_only_and_holds_preserved(self):
        body = REPORT.read_text(encoding="utf-8")
        external = EXTERNAL.read_text(encoding="utf-8")
        ids = re.findall(r"^\| `(TR-[A-Z0-9-]+)` \|", body, re.MULTILINE)
        self.assertEqual(len(ids), 12)
        self.assertEqual(len(set(ids)), 12)
        for key in ids:
            self.assertIn(key, external)
        for key in ("TR-MERCY", "TR-Q-06", "TR-Q-07", "TR-Q-10"):
            self.assertIn(f"**`{key}`", body)
        for flag in ("RIGHTS_HOLD", "PUBLICATION_HOLD", "INDEPENDENT_REVIEW 0/12"):
            self.assertIn(flag, body)
        self.assertIn("EXTERNAL_REVIEW 0/12", external)
        self.assertIn("NOT_PERFORMED", external)
        self.assertNotIn("EXTERNAL_REVIEW 12/12", body)

    def test_early_1699_margin_185_is_grounded_and_hold_limited(self):
        chapter = (MANUSCRIPTS / "II_UCHENYI_I_PROPOVEDNIK_WORKING_DRAFT.md").read_text(encoding="utf-8")
        reader = READER.read_text(encoding="utf-8")
        ed02 = (BASE / "supplemental-audits" / "ED02_LINGENDES_84_87_TO_CHARNOCK_621_ALIGNMENT_2026-11-18.md").read_text(encoding="utf-8")
        for text, prefix in ((chapter, "[^9]:"), (reader, "[^ch2-9]:")):
            self.assertIn(prefix, text)
            footnote = text.split(prefix, 1)[1].split("\n[^", 1)[0]
            self.assertIn("EARLY_1699_IMAGE_OCR_CORROBORATED", footnote)
            self.assertIn("p. 185", footnote)
            self.assertIn("кадре 520", footnote)
            self.assertIn("1684", footnote)
            self.assertIn("CATALOG_ONLY", footnote)
            self.assertNotIn("PAGE_NUMBER_IMAGE_PENDING", footnote)
            self.assertNotIn("ED-02 CLOSED", footnote)
        self.assertIn("page=459", ed02)
        self.assertIn("page=520", ed02)
        self.assertIn("p.185", ed02)
        self.assertIn("HUMAN_FACSIMILE_REVIEW_PENDING", ed02)
        self.assertIn("PUBLICATION_HOLD", ed02)


if __name__ == "__main__":
    unittest.main()
