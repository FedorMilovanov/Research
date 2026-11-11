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
        self.assertEqual(self.source_count, 205)
        self.assertEqual(len(self.sources), 205)
        bge = self.sources["REF-P86"]
        self.assertEqual(bge["accessState"], "PARTIAL_OBJECT")
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
        self.assertEqual(bge["accessState"], "PARTIAL_OBJECT")
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
        self.assertEqual(self.source_count, 205)
        self.assertEqual(self.sources["REF-P86"]["accessState"], "PARTIAL_OBJECT")
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
        self.assertEqual(bge["accessState"], "PARTIAL_OBJECT")
        self.assertEqual(bge["checkedAt"], "2026-11-10")
        self.assertIn("CorrMss 2026/448", bge["verificationNote"])
        self.assertIn("FOLIO_IMAGES_UNREAD", bge["verificationNote"])
        for hold in ("ARCHIVE_HOLD", "RIGHTS_HOLD", "PUBLICATION_HOLD"):
            self.assertIn(hold, bge["holds"])

    def test_wave418_custodian_date_and_folio_5_are_not_false_image_colla(self):
        """Custodian correspondence confirms 22 May and f.5, not pixel-level reading."""
        request = (HERE / "nantes_bge_ms_fr_413_archival_request.md").read_text(encoding="utf-8")
        packet = (HERE / "independent_review_packets.md").read_text(encoding="utf-8")
        for doc in (self.chapter, self.dossier, request, packet, self.plan):
            for value in ("CUSTODIAN_DATE_22_MAY_1599_CONFIRMED",
                          "ARTICLE_XI_CONTINUES_F5",
                          "EARLY_XI_COLLATION_HOLD",
                          "RIGHTS_HOLD", "PUBLICATION_HOLD"):
                with self.subTest(value=value,doc=doc[:23]):
                    self.assertIn(value, doc)
        for doc in (request, self.dossier, packet, self.plan):
            for leaf in ("f.4v", "f.5", "f.28", "FOLIO_IMAGES_UNREAD",
                         "FOLIO_28_DIRECT_PALEOGRAPHIC_COLLATION_HOLD"):
                with self.subTest(leaf=leaf,doc=doc[:23]):
                    self.assertIn(leaf, doc)
        self.assertIn("COPY_DATE_CONFLICT_22_29_MAY_1599", request)
        self.assertIn("29", self.dossier)
        self.assertIn("TIFF_TRANSFER_OFFERED_NOT_COLLATED", request)
        self.assertIn("REVIEW_PACKETS_PREPARED / NOT_SENT", packet)
        source = self.sources["REF-P86"]
        self.assertEqual(source["checkedAt"], "2026-11-10")
        self.assertEqual(source["accessState"], "PARTIAL_OBJECT")
        self.assertIn("CUSTODIAN_DATE_22_MAY_1599_CONFIRMED", source["verificationNote"])
        c301 = next(line for line in self.claims.splitlines() if line.startswith("| C301 |"))
        for term in ("ARTICLE_XI_CONTINUES_F5", "FOLIO_IMAGES_UNREAD",
                     "22 мая 1599", "COPY_DATE_CONFLICT_22_29_MAY_1599"):
            self.assertIn(term, c301)
        for value in ("ARCHIVE_HOLD", "RIGHTS_HOLD", "PUBLICATION_HOLD"):
            self.assertIn(value, source["holds"])

    def test_wave422_private_tiff_evidence_is_partial_not_publication(self):
        """Image custody and initial visual inspection are not manuscript collation."""
        request = (HERE / "nantes_bge_ms_fr_413_archival_request.md").read_text(encoding="utf-8")
        packet = (HERE / "independent_review_packets.md").read_text(encoding="utf-8")
        source = self.sources["REF-P86"]
        self.assertEqual(source["accessState"], "PARTIAL_OBJECT")
        self.assertTrue(source["verificationNote"].startswith("2026-11-10 WAVE425"))
        self.assertIn("2026-11-10 WAVE423", source["verificationNote"])
        self.assertIn("2026-11-10 WAVE422", source["verificationNote"])
        for token in ("FILES_ACQUIRED_DIRECTLY", "THREE_FOLIOS_VISUALLY_INSPECTED",
                      "F028V_CERTIFICATION_DIRECT_READ_HOLD", "EARLY_XI_COLLATION_HOLD",
                      "ORIGINAL_GENEVAN_COLLATION_HOLD"):
            with self.subTest(token=token):
                self.assertIn(token, source["verificationNote"])
                self.assertIn(token, self.plan)
        originals = {
            "ms_fr_00413_f004v.tif": ("42 102 794", "f7f413206e723ab0931a3e57623636a9f94161f5113adc33201fb7fa02ca1379"),
            "ms_fr_00413_f005r.tif": ("42 102 722", "32945087dc4e3966c7e8b02778a390b37c0f8b25d036d40b69b431aea06c3003"),
            "ms_fr_00413_f028v.tif": ("42 102 002", "383fb8c108bd9161ce4d17c606f61e2ec7582d19c74521ed18ff95eefd04ebc7"),
        }
        for name, (size, sha256) in originals.items():
            with self.subTest(name=name):
                self.assertIn(name, request)
                self.assertIn(size, request)
                self.assertIn(sha256, request)
        for document in (request, packet, self.dossier, self.chapter, self.plan, self.claims):
            with self.subTest(document=document[:24]):
                self.assertIn("F028V_CERTIFICATION_DIRECT_READ_HOLD", document)
                self.assertIn("EARLY_XI_COLLATION_HOLD", document)
                self.assertIn("RIGHTS_HOLD", document)
                self.assertIn("PUBLICATION_HOLD", document)
        self.assertIn("REVIEW_PACKETS_PREPARED / NOT_SENT", packet)
        for hold in ("ARCHIVE_HOLD", "RIGHTS_HOLD", "PUBLICATION_HOLD"):
            self.assertIn(hold, source["holds"])
        # The private transfer token and protected photo bytes must not enter public research docs.
        import re
        for document in (request, packet, self.dossier, self.chapter, self.plan, self.claims):
            self.assertIsNone(re.search(
                r"https?://(?:www\.)?swisstransfer\.com/[a-z]{2}/[0-9a-f-]{36}",
                document, flags=re.IGNORECASE))

    def test_wave423_original_xi_junction_is_scoped_direct_comparison(self):
        """Direct photo comparison establishes a bounded variant, not full collation."""
        request = (HERE / "nantes_bge_ms_fr_413_archival_request.md").read_text(encoding="utf-8")
        packet = (HERE / "independent_review_packets.md").read_text(encoding="utf-8")
        source = self.sources["REF-P86"]
        marker = "EARLY_XI_F4V_F5R_JUNCTION_DIRECTLY_OBSERVED"
        paris = "PARIS_XI_L441_L455_ADDITIONAL_EXCEPTION_BLOCK"
        self.assertEqual(source["accessState"], "PARTIAL_OBJECT")
        for label, document in (("source", source["verificationNote"]),
                                ("archive", request), ("dossier", self.dossier),
                                ("chapter", self.chapter), ("claim", self.claims),
                                ("packet", packet), ("self-plan", self.plan)):
            with self.subTest(document=label):
                self.assertIn(marker, document)
                self.assertIn(paris, document)
                self.assertIn("EARLY_XI_COLLATION_HOLD", document)
                self.assertIn("RIGHTS_HOLD", document)
                self.assertIn("PUBLICATION_HOLD", document)
        for token in ("f.4v", "f.5r", "L441", "L455", "L456", "Voulons et entendons"):
            with self.subTest(token=token):
                self.assertIn(token, request)
        for token in ("FULL_DIPLOMATIC_XI_COLLATION_HOLD",
                      "ORIGINAL_GENEVAN_COLLATION_HOLD",
                      "F028V_CERTIFICATION_DIRECT_READ_HOLD"):
            self.assertIn(token, source["verificationNote"])
            self.assertIn(token, self.plan)
        self.assertIn("REVIEW_PACKETS_PREPARED / NOT_SENT", packet)
        for hold in ("ARCHIVE_HOLD", "RIGHTS_HOLD", "PUBLICATION_HOLD"):
            self.assertIn(hold, source["holds"])
        self.assertEqual(self.source_count, 205)

    def test_wave424_folio28_side_and_xi_line_map_remain_evidence_limited(self):
        """A draft question about f28r is not proof that f28r bears the certification."""
        archive = (HERE / "nantes_bge_ms_fr_413_archival_request.md").read_text(encoding="utf-8")
        packet = (HERE / "independent_review_packets.md").read_text(encoding="utf-8")
        source = self.sources["REF-P86"]
        for token in ("F28R_SIDE_UNCONFIRMED", "F28R_REQUEST_DRAFT_UNSENT",
                      "F028V_CERTIFICATION_DIRECT_READ_HOLD"):
            for label, document in (("archive", archive), ("packet", packet),
                                    ("self-plan", self.plan)):
                with self.subTest(token=token, doc=label):
                    self.assertIn(token, document)
        for token in ("L423–440", "L441–455", "L456–463", "L464",
                      "f.4v", "f.5r", "Voulons et entendons"):
            with self.subTest(segment=token):
                self.assertIn(token, archive)
        self.assertIn("REVIEW_PACKETS_PREPARED / NOT_SENT", packet)
        self.assertEqual(source["accessState"], "PARTIAL_OBJECT")
        for hold in ("ARCHIVE_HOLD", "RIGHTS_HOLD", "PUBLICATION_HOLD"):
            self.assertIn(hold, source["holds"])
        for document in (archive, packet, self.plan):
            self.assertIn("FULL_DIPLOMATIC_XI_COLLATION_HOLD", document)
            self.assertIn("PUBLICATION_HOLD", document)
            self.assertNotIn("F28R_DATE_DIRECTLY_READ", document)

    def test_wave425_exception_starts_inside_printed_L440(self):
        """Registered Paris print splits 'fors &' and 'excepté' across L440/L441."""
        request = (HERE / "nantes_bge_ms_fr_413_archival_request.md").read_text(encoding="utf-8")
        packet = (HERE / "independent_review_packets.md").read_text(encoding="utf-8")
        source = self.sources["REF-P86"]
        marker = "PARIS_XI_EXCEPTION_STARTS_L440_FORS_ET"
        for label, document in (("source", source["verificationNote"]),
                                ("archive", request), ("dossier", self.dossier),
                                ("chapter", self.chapter), ("claim", self.claims),
                                ("packet", packet), ("plan", self.plan)):
            with self.subTest(document=label):
                self.assertIn(marker, document)
                self.assertIn("RIGHTS_HOLD", document)
                self.assertIn("PUBLICATION_HOLD", document)
        for label, document in (("source", source["verificationNote"]),
                                ("archive", request), ("packet", packet),
                                ("plan", self.plan)):
            with self.subTest(complete_boundary=label):
                self.assertIn("PARIS_XI_L440_L455_COMPLETE_BLOCK", document)
        for token in ("L440", "fors &", "L441", "excepté", "L455",
                      "L456", "Voulons & entendons"):
            with self.subTest(print_anchor=token):
                self.assertIn(token, request)
        self.assertEqual(source["accessState"], "PARTIAL_OBJECT")
        self.assertIn("FULL_DIPLOMATIC_XI_COLLATION_HOLD", source["verificationNote"])
        self.assertIn("F28R_SIDE_UNCONFIRMED", self.plan)
        self.assertIn("REVIEW_PACKETS_PREPARED / NOT_SENT", packet)
        self.assertNotIn(marker, self.chapter.split("## Источниковедческий аппарат", 1)[0])
        self.assertEqual(self.source_count, 205)
        for hold in ("ARCHIVE_HOLD", "RIGHTS_HOLD", "PUBLICATION_HOLD"):
            self.assertIn(hold, source["holds"])

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
