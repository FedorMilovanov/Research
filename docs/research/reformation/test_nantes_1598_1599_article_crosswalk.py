#!/usr/bin/env python3
"""Read-only Nantes 1598/1599 variant crosswalk: legal identity > raw article counts.

An academic secondary comparison is not independent autograph collation.
The Paris 1599 article XXXVII and deleted original 1598 article 37 differ.
"""
from pathlib import Path
import json
import re
import unittest

HERE = Path(__file__).resolve().parent


class NantesVariantCrosswalkTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chapter = (HERE / "episode11_france_catholic_reform_nantes_1545_1599_manuscript.md").read_text(encoding="utf-8")
        cls.dossier = (HERE / "09_france_confession_nantes_source_study.md").read_text(encoding="utf-8")
        cls.ledger = (HERE / "03_claim_verification_register.md").read_text(encoding="utf-8")
        registry = json.loads((HERE / "source-registry-v1.json").read_text(encoding="utf-8"))
        cls.n = registry["sourceCount"]
        cls.sources = {s["id"]: s for s in registry["sources"]}

    def test_valid_documentary_basis_and_not_fake_autographs(self):
        self.assertEqual(self.n, 200)
        self.assertEqual(len(self.sources), self.n)
        for id in ("REF-P86", "REF-S97", "REF-S98", "REF-P27", "REF-P29"):
            self.assertIn(id, self.sources)
            self.assertEqual(self.sources[id]["publicationState"], "REFERENCE")
            self.assertIn("PUBLICATION_HOLD", self.sources[id]["holds"])
        for id in ("REF-P86", "REF-P29"):
            with self.subTest(id=id):
                self.assertEqual(self.sources[id]["accessState"], "CATALOG_ONLY")
                self.assertIn("ARCHIVE_HOLD", self.sources[id]["holds"])
        for id in ("REF-S97", "REF-S98", "REF-P27"):
            self.assertEqual(self.sources[id]["accessState"], "PARTIAL_OBJECT")

    def test_two_different_article_37_and_retained_bordeaux_office(self):
        for word in ("первоначальную статью 37", "исключили", "XXXVII",
                     "Бордо", "заместителей", "L926–935",
                     "лист 023r", "не** доказывает отмены"):
            with self.subTest(word=word):
                self.assertIn(word.lower(), self.chapter.lower())
        for word in ("исходная статья 37", "ранняя статья 37",
                     "XXXVII", "Бордо", "Blatt 023r", "L926–935"):
            self.assertIn(word.lower(), self.dossier.lower())

    def test_article_count_mechanism_is_not_third_document(self):
        for word in ("95", "92", "93–95", "одну статью 92",
                     "56 особых статей", "brevets",
                     "ORIGINAL_GENEVAN_COLLATION_HOLD"):
            with self.subTest(word=word):
                self.assertIn(word.lower(), self.chapter.lower())
        self.assertIn("95 – 1 удалённая – 2", self.dossier)
        self.assertIn("не означает", self.dossier)
        self.assertIn("93", self.chapter)

    def test_specific_evidence_in_claim_ledger_and_dossier(self):
        claims = re.findall(r"^\| C(\d+) \|", self.ledger, re.MULTILINE)
        self.assertEqual([int(c) for c in claims], list(range(1, 320)))
        claim = next(l for l in self.ledger.splitlines() if l.startswith("| C302 |"))
        for marker in ("REF-P86", "REF-S97", "REF-S98", "REF-P27",
                       "95", "92", "XXXVII", "Бордо", "L926–935"):
            self.assertIn(marker, claim)
        for marker in ("BGE", "Ms. fr. 413", "AN J", "Garrisson", "Cottret",
                       "CATALOG_ONLY", "ARCHIVE_HOLD", "RIGHTS_HOLD"):
            self.assertIn(marker, self.dossier)

    def test_handoff_gates_remain_open(self):
        plan = (HERE / "SELF_PLAN.md").read_text(encoding="utf-8")
        for key in ("RF-NANTES-1598-1599-ARTICLE-CROSSWALK", "STOP_DISCOVERY",
                    "INDEPENDENT_EXTERNAL_REVIEW_OPEN", "ORIGINAL_GENEVAN_COLLATION_HOLD",
                    "RIGHTS_HOLD", "THEOLOGICAL_PEER_REVIEW_OPEN",
                    "EDITORIAL_HANDOFF_HOLD", "PUBLICATION_HOLD"):
            self.assertIn(key, plan)
        for id in ("REF-P86", "REF-S97", "REF-S98"):
            self.assertIn("RIGHTS_HOLD", self.sources[id]["holds"])


if __name__ == "__main__":
    unittest.main()
