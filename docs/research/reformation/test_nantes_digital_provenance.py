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
        self.assertEqual(self.source_count, 204)
        self.assertEqual(len(self.sources), 204)
        bge = self.sources["REF-P86"]
        self.assertEqual(bge["accessState"], "CATALOG_ONLY")
        self.assertIn("29 May 1599", bge["verificationNote"])
        for hold in ("ARCHIVE_HOLD", "RIGHTS_HOLD", "PUBLICATION_HOLD"):
            self.assertIn(hold, bge["holds"])

    def test_conflicting_certification_date_never_collapses_to_one(self):
        marker = "COPY_DATE_CONFLICT_22_29_MAY_1599"
        for name, doc in (("chapter", self.chapter), ("dossier", self.dossier), ("plan", self.plan)):
            with self.subTest(name=name):
                self.assertIn(marker, doc)
                self.assertIn("22", doc)
                self.assertIn("29", doc)
        claim = next(x for x in self.claims.splitlines() if x.startswith("| C301 |"))
        self.assertIn(marker, claim)
        bge = self.sources["REF-P86"]
        self.assertIn(marker, bge["verificationNote"])
        self.assertIn("22 May 1599", bge["verificationNote"])
        self.assertIn("29 May 1599", bge["verificationNote"])
        self.assertEqual(bge["accessState"], "CATALOG_ONLY")
        self.assertIn("ARCHIVE_HOLD", bge["holds"])
        self.assertIn("RIGHTS_HOLD", bge["holds"])
        self.assertIn("PUBLICATION_HOLD", bge["holds"])

    def test_bge_archival_request_and_reply_are_distinct_evidence_stages(self):
        request = (HERE / "nantes_bge_ms_fr_413_archival_request.md").read_text(encoding="utf-8")
        for token in ("BGE Ms. fr. 413", "num.bge@geneve.ch",
                      "22 mai 1599", "29 mai 1599", "article XI",
                      "EARLY_XI_COLLATION_HOLD", "COPY_DATE_CONFLICT_22_29_MAY_1599",
                      "ARCHIVE_INQUIRY_SENT / RESPONSE_PENDING", "RIGHTS_HOLD", "PUBLICATION_HOLD"):
            with self.subTest(token=token):
                self.assertIn(token, request)
        self.assertIn("nantes_bge_ms_fr_413_archival_request.md", self.dossier)
        self.assertIn("nantes_bge_ms_fr_413_archival_request.md", self.plan)
        self.assertIn("ARCHIVE_REPLY_RECEIVED", self.plan)
        self.assertIn("ARCHIVE_INQUIRY_SENT / RESPONSE_PENDING", self.plan)  # archived, not current
        self.assertIn("REF-P86 CATALOG_ONLY", self.dossier)
        self.assertIn("14:19:53 UTC", request)
        self.assertIn("14:19:53 UTC", self.plan)
        self.assertNotIn("ARCHIVE_ACCESS_REQUEST_DRAFT / NOT_SENT", request)
        self.assertEqual(self.source_count, 204)
        self.assertEqual(self.sources["REF-P86"]["accessState"], "CATALOG_ONLY")
        self.assertIn("PUBLICATION_HOLD", self.sources["REF-P86"]["holds"])

    def test_custodian_named_folios_not_mistaken_for_transcribed_ms(self):
        request = (HERE / "nantes_bge_ms_fr_413_archival_request.md").read_text(encoding="utf-8")
        packet = (HERE / "independent_review_packets.md").read_text(encoding="utf-8")
        self.assertIn("CorrMss 2026/448", request)
        self.assertIn("09.11.2026", request)
        self.assertIn("ARCHIVE_REPLY_RECEIVED", request)
        self.assertIn("DIGITAL_OBJECT_LOCATED", request)
        self.assertIn("FOLIO_LOCATORS_CONFIRMED", request)
        self.assertIn("FOLIO_IMAGES_UNREAD", request)
        self.assertIn("COPY_DATE_CONFLICT_22_29_MAY_1599", request)
        self.assertIn("EARLY_XI_COLLATION_HOLD", request)
        self.assertIn("Anubis", request)
        self.assertIn("RESPONSE_PENDING", request)  # historical, explicitly superseded
        for locator in (
            "https://archives.bge-geneve.ch/ark:/17786/vtac61f062330e0a126",
            "%2Fcanvas%2F0%2F65",
            "%2Fcanvas%2F0%2F18",
        ):
            with self.subTest(locator=locator):
                self.assertIn(locator, request)
                self.assertIn(locator, self.dossier)
                self.assertIn(locator, self.chapter)
                self.assertIn(locator, packet)
        for folio in ("folio 28", "folio 4v"):
            for document in (request, self.dossier, self.chapter):
                self.assertIn(folio, document)
        self.assertIn("f. 28", packet)
        self.assertIn("f. 4v", packet)
        c301 = next(x for x in self.claims.splitlines() if x.startswith("| C301 |"))
        for token in ("ARCHIVE_REPLY_RECEIVED", "FOLIO_IMAGES_UNREAD",
                      "COPY_DATE_CONFLICT_22_29_MAY_1599", "EARLY_XI_COLLATION_HOLD"):
            self.assertIn(token, c301)
        bge = self.sources["REF-P86"]
        self.assertEqual(bge["accessState"], "CATALOG_ONLY")
        self.assertEqual(bge["checkedAt"], "2026-11-09")
        self.assertIn("CorrMss 2026/448", bge["verificationNote"])
        self.assertIn("FOLIO_IMAGES_UNREAD", bge["verificationNote"])
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
