#!/usr/bin/env python3
"""Wave 392: date of original text != date of registration != date of a certified copy.

A modern transcription titled "avril 1598" can still transmit the Paris
registered text of 1599. Bibliothèque de Genève institutional evidence
does not establish that manuscript leaves were directly collated.
"""
import json
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent


class NantesDigitalProvenanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chapter = (HERE / "episode11_france_catholic_reform_nantes_1545_1599_manuscript.md").read_text(encoding="utf-8")
        cls.dossier = (HERE / "09_france_confession_nantes_source_study.md").read_text(encoding="utf-8")
        cls.claims = (HERE / "03_claim_verification_register.md").read_text(encoding="utf-8")
        cls.plan = (HERE / "SELF_PLAN.md").read_text(encoding="utf-8")
        data = json.loads((HERE / "source-registry-v1.json").read_text(encoding="utf-8"))
        cls.source_count = data["sourceCount"]
        cls.sources = {s["id"]: s for s in data["sources"]}

    def test_april_1598_title_cannot_be_read_as_original_95_article_witness(self):
        for t in ("Nicole Dufournaud", "2003", "XCII", "25 février 1599",
                  "зарегистрированного текстового состояния"):
            with self.subTest(marker=t):
                self.assertIn(t, self.dossier)
        for t in ("2003", "XCII", "25 февраля 1599 года",
                  "не всякое электронное издание"):
            with self.subTest(marker=t):
                self.assertIn(t.lower(), self.chapter.lower())
        row = next(x for x in self.claims.splitlines() if x.startswith("| C301 |"))
        self.assertIn("DIGITAL_TITLE_NOT_EARLY_WITNESS", row)

    def test_copy_date_is_not_editorial_state_or_direct_leaf_read(self):
        self.assertIn("29.05.1599", self.dossier)
        self.assertIn("29 мая 1599 года", self.chapter)
        self.assertIn("2010–2011", self.plan)
        self.assertEqual(self.source_count, 202)
        self.assertEqual(len(self.sources), 202)
        bge = self.sources["REF-P86"]
        self.assertEqual(bge["accessState"], "CATALOG_ONLY")
        self.assertIn("29 May 1599", bge["verificationNote"])
        for hold in ("ARCHIVE_HOLD", "RIGHTS_HOLD", "PUBLICATION_HOLD"):
            self.assertIn(hold, bge["holds"])

    def test_xi_remains_secondary_variant_and_not_publication_approved(self):
        for doc in (self.chapter, self.dossier, self.plan):
            for token in ("EARLY_XI_COLLATION_HOLD", "ORIGINAL_GENEVAN_COLLATION_HOLD"):
                with self.subTest(doc=doc[:20], token=token):
                    self.assertIn(token, doc)
        for token in ("STOP_DISCOVERY", "INDEPENDENT_EXTERNAL_REVIEW_OPEN",
                      "THEOLOGICAL_PEER_REVIEW_OPEN", "RIGHTS_HOLD", "PUBLICATION_HOLD"):
            self.assertIn(token, self.plan)
        self.assertEqual(self.sources["REF-S99"]["evidenceClass"], "B1")
        self.assertEqual(self.sources["REF-P27"]["accessState"], "PARTIAL_OBJECT")


if __name__ == "__main__":
    unittest.main()
