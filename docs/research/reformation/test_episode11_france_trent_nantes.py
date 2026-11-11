#!/usr/bin/env python3
"""French Reformation episode 11: source status, dates and legal limits."""
from pathlib import Path
import json
import unittest

D=Path(__file__).resolve().parent
CH=D/"episode11_france_catholic_reform_nantes_1545_1599_manuscript.md"

class FranceTrentNantesTests(unittest.TestCase):
    def test_chapter_exists_with_historical_sequence_and_holds(self):
        s=CH.read_text(encoding="utf-8")
        self.assertTrue(s.startswith("# Эпизод 11."))
        self.assertGreaterEqual(len(s.split()),2600)
        for part in ("1545","1547","1559","1562","1563","1571","1572","1598","1599",
                     "2 апреля 1571","12 апреля", "Тридент", "Васси",
                     "Варфоломеевская", "Нант", "Источниковедческий аппарат",
                     "RESEARCH_MANUSCRIPT_DRAFT", "NOT_EDITORIAL_READY","PUBLICATION_HOLD"):
            with self.subTest(part=part):self.assertIn(part.lower(),s.lower())
        self.assertIn("двенадцатой, заключительной",s.lower())

    def test_source_provenance_not_upgrade_by_summary(self):
        r=json.loads((D/"source-registry-v1.json").read_text(encoding="utf-8"))
        self.assertEqual(r["sourceCount"],len(r["sources"]))
        records={s["id"]:s for s in r["sources"]}
        for key in ("REF-S86","REF-S87","REF-S88","REF-S89","REF-S90"):
            with self.subTest(key=key):
                self.assertEqual(records[key]["evidenceClass"],"B1")
                self.assertEqual(records[key]["accessState"],"PARTIAL_OBJECT")
                self.assertIn("PUBLICATION_HOLD",records[key]["holds"])
        self.assertEqual(records["REF-P27"]["accessState"],"PARTIAL_OBJECT")
        self.assertEqual(records["REF-P29"]["accessState"],"CATALOG_ONLY")
        self.assertEqual(records["REF-P28"]["accessState"],"PARTIAL_OBJECT")
        self.assertEqual(records["REF-P30"]["accessState"],"CATALOG_ONLY")
        for key in ("REF-P18","REF-P20","REF-P27","REF-P28","REF-P29"):
            self.assertIn("PUBLICATION_HOLD",records[key]["holds"])

    def test_nantes_paris_special_article_is_not_erased_by_general_prohibition(self):
        s = CH.read_text(encoding="utf-8")
        reader, apparatus = s.split("## Источниковедческий аппарат", 1)
        claim = next(line for line in (D / "03_claim_verification_register.md").read_text(encoding="utf-8").splitlines()
                     if line.startswith("| C301 |"))
        packet = (D / "independent_review_packets.md").read_text(encoding="utf-8")
        reg = json.loads((D / "source-registry-v1.json").read_text(encoding="utf-8"))
        source = next(x for x in reg["sources"] if x["id"] == "REF-S101")
        for marker in ("Особая статья XXXIII", "не далее пяти лье",
                       "одного определённого места", "общую статью XIV",
                       "не разрешение открыть службы"):
            self.assertIn(marker.lower(), reader.lower())
        for marker in ("REF-S101", "376–377", "L488–504",
                       "ORIGINAL_ART33_PRINT_COLLATION_HOLD", "LOCAL_EXECUTION_HOLD"):
            self.assertIn(marker, apparatus)
        for marker in ("особая статья XXXIII", "SECONDARY_CHECKED",
                       "ORIGINAL_ART33_PRINT_COLLATION_HOLD"):
            self.assertIn(marker.lower(), claim.lower())
        self.assertIn("особую статью **XXXIII**", packet)
        self.assertEqual(source["evidenceClass"], "B1")
        self.assertEqual(source["accessState"], "PARTIAL_OBJECT")
        self.assertIn("PUBLICATION_HOLD", source["holds"])
        self.assertIn("not physically inspected original", source["verificationNote"].lower())

    def test_wave431_primary_edition_found_but_not_claimed_as_read(self):
        chapter = CH.read_text(encoding="utf-8")
        dossier = (D / "09_france_confession_nantes_source_study.md").read_text(encoding="utf-8")
        claims = (D / "03_claim_verification_register.md").read_text(encoding="utf-8")
        row = next(line for line in claims.splitlines() if line.startswith("| C301 |"))
        packet = (D / "independent_review_packets.md").read_text(encoding="utf-8")
        for marker in ("FRBNF33814462", "NUMM-319439", "bpt6k3194390",
                       "8-LB35-727 (F)", "ORIGINAL_ART33_PRINT_COLLATION_HOLD",
                       "TITLE_VARIANT_INTERPRETATION_HOLD"):
            with self.subTest(marker=marker):
                self.assertIn(marker, dossier)
                self.assertIn(marker, chapter)
                self.assertIn(marker, packet)
        for marker in ("FRBNF33814462", "FRBNF33814457",
                       "ORIGINAL_ART33_PRINT_COLLATION_HOLD",
                       "TITLE_VARIANT_INTERPRETATION_HOLD"):
            self.assertIn(marker, row)
        self.assertIn("403/bot_blocked", dossier)
        self.assertIn("отдельная печать 1621", packet)
        # Bibliographic discovery does not promote a source ID or alter other evidence contracts.
        data = json.loads((D / "source-registry-v1.json").read_text(encoding="utf-8"))
        self.assertEqual(data["sourceCount"], 206)
        bost = next(s for s in data["sources"] if s["id"] == "REF-S101")
        self.assertEqual(bost["evidenceClass"], "B1")
        self.assertEqual(bost["accessState"], "PARTIAL_OBJECT")
        self.assertIn("PUBLICATION_HOLD", bost["holds"])

    def test_wave432_particular_articles_date_not_transferred_to_general_edict(self):
        content = CH.read_text(encoding="utf-8")
        reader, apparatus = content.split("## Источниковедческий аппарат", 1)
        dossier = (D / "09_france_confession_nantes_source_study.md").read_text(encoding="utf-8")
        packet = (D / "independent_review_packets.md").read_text(encoding="utf-8")
        claims = (D / "03_claim_verification_register.md").read_text(encoding="utf-8")
        c302 = next(x for x in claims.splitlines() if x.startswith("| C302 |"))
        for marker in ("30 апреля или 2 мая", "позднейший королевский акт",
                       "общего эдикта", "не следует сводить"):
            self.assertIn(marker.lower(), reader.lower())
        for marker in ("Hildesheimer", "Bimbenet-Privat",
                       "GENERAL_VS_PARTICULAR_DATE_SEPARATED",
                       "RETROSPECTIVE_1685_2MAY_REFERENCE",
                       "ORIGINAL_ART33_PRINT_COLLATION_HOLD"):
            for s in (apparatus, dossier, packet):
                with self.subTest(marker=marker):
                    self.assertIn(marker, s)
        for marker in ("C302", "30 avril ou 2 mai", "A65",
                       "1598_SIGNED_ARTICLES_DIRECT_READ_HOLD"):
            self.assertIn(marker, c302)
        self.assertIn("timeout", dossier)
        registry = json.loads((D / "source-registry-v1.json").read_text(encoding="utf-8"))
        self.assertEqual(registry["sourceCount"], 206)
        self.assertTrue(all("PUBLICATION_HOLD" in s["holds"] for s in registry["sources"]))

    def test_wave433_newberry_1622_is_distinct_primary_witness_not_original_1598(self):
        reader = CH.read_text(encoding="utf-8")
        narrative, apparatus = reader.split("## Источниковедческий аппарат", 1)
        dossier = (D/"09_france_confession_nantes_source_study.md").read_text(encoding="utf-8")
        claims = (D/"03_claim_verification_register.md").read_text(encoding="utf-8")
        packet = (D/"independent_review_packets.md").read_text(encoding="utf-8")
        registry = json.loads((D/"source-registry-v1.json").read_text(encoding="utf-8"))
        acquisitions = json.loads((D/"acquisition-manifest-v1.json").read_text(encoding="utf-8"))
        self.assertEqual(registry["sourceCount"], 206)
        self.assertEqual(len(registry["sources"]), 206)
        self.assertEqual(acquisitions["sourceCount"], 16)
        self.assertEqual(len(acquisitions["sourceRecords"]), 16)
        src = next(s for s in registry["sources"] if s["id"] == "REF-P87")
        acquired = next(s for s in acquisitions["sourceRecords"] if s["id"] == "REF-P87")
        self.assertEqual(src["documentYear"], 1622)
        self.assertEqual(src["evidenceClass"], "A1")
        self.assertEqual(src["accessState"], "PARTIAL_OBJECT")
        self.assertEqual(src["rightsState"], "RIGHTS_UNKNOWN")
        self.assertIn("RIGHTS_HOLD", src["holds"])
        self.assertIn("PUBLICATION_HOLD", src["holds"])
        self.assertEqual(acquired["acquisitionState"], "DOWNLOADED_VERIFIED")
        self.assertEqual(acquired["actualBytes"], 2784696)
        self.assertEqual(acquired["sha256"],
                         "d8481415ed48ad4f283e0dd9dc6426bdc511c2c3e6e858bd07d53a7e3c705356")
        self.assertEqual(acquired["retainedLocalCopy"]["digitalPages"], 28)
        self.assertEqual(acquired["retainedLocalCopy"]["historicalPrintedPages"], 23)
        self.assertEqual(acquired["retainedLocalCopy"]["visuallyInspectedPdfPages"], [3, 5, 14, 15, 24, 25])
        self.assertEqual(acquisitions["fileBytesInGit"], 0)
        for marker in ("Особая статья XXXIV", "колоколами", "синодов",
                       "1622 года", "приказ", "регистрацию"):
            self.assertIn(marker.lower(), narrative.lower())
        for part in (apparatus, dossier, packet):
            for marker in ("REF-P87", "d8481415ed48ad4f283e0dd9dc6426bdc511c2c3e6e858bd07d53a7e3c705356",
                           "1622", "ORIGINAL_ART33_PRINT_COLLATION_HOLD",
                           "REGISTRATION_EXECUTION_HOLD"):
                self.assertIn(marker, part)
        c301 = next(x for x in claims.splitlines() if x.startswith("| C301 |"))
        c302 = next(x for x in claims.splitlines() if x.startswith("| C302 |"))
        for row in (c301, c302):
            self.assertIn("REF-P87", row)
            self.assertIn("PUBLICATION_HOLD", row)
        self.assertIn("REGISTRATION_ORDER_NOT_EXECUTION", apparatus)
        old = next(s for s in registry["sources"] if s["id"] == "REF-S101")
        self.assertEqual(old["evidenceClass"], "B1")
        self.assertEqual(old["accessState"], "PARTIAL_OBJECT")

    def test_wave434_registration_evidence_1885_is_not_a_court_register(self):
        text = CH.read_text(encoding="utf-8")
        reader, apparatus = text.split("## Источниковедческий аппарат", 1)
        dossier = (D/"09_france_confession_nantes_source_study.md").read_text(encoding="utf-8")
        packet = (D/"independent_review_packets.md").read_text(encoding="utf-8")
        c301 = next(x for x in (D/"03_claim_verification_register.md").read_text(encoding="utf-8").splitlines()
                    if x.startswith("| C301 |"))
        registry = json.loads((D/"source-registry-v1.json").read_text(encoding="utf-8"))
        ref = next(x for x in registry["sources"] if x["id"] == "REF-P87")
        acquired = json.loads((D/"acquisition-manifest-v1.json").read_text(encoding="utf-8"))
        for marker in ("позднейших переизданиях", "Бост", "протокола",
                       "общий эдикт и особые статьи"):
            self.assertIn(marker.lower(), reader.lower())
        for marker in ("FRBNF33814458", "BNF_1622_CATALOG_MATCH",
                       "WIKISOURCE_1885_REPRINT_PROVENANCE",
                       "REGISTRATION_TITLE_ASSERTION_CONFLICT_OPEN",
                       "REGISTER_BOOK_DIRECT_CHECK_HOLD",
                       "REGISTRATION_ORDER_NOT_EXECUTION"):
            for label, item in (("apparatus",apparatus), ("dossier",dossier)):
                with self.subTest(marker=marker, document=label):
                    self.assertIn(marker, item)
        for marker in ("FRBNF33814458", "1885", "aussi vérifiez en Parlement",
                       "REGISTRATION_TITLE_ASSERTION_CONFLICT_OPEN",
                       "REGISTER_BOOK_DIRECT_CHECK_HOLD"):
            self.assertIn(marker, packet)
            self.assertIn(marker, c301)
        self.assertIn("WIKISOURCE_1885_REPRINT_PROVENANCE", ref["verificationNote"])
        self.assertIn("BNF_1622_CATALOG_MATCH", ref["verificationNote"])
        self.assertEqual(ref["documentYear"], 1622)
        self.assertEqual(ref["evidenceClass"], "A1")
        self.assertEqual(ref["accessState"], "PARTIAL_OBJECT")
        self.assertIn("PUBLICATION_HOLD", ref["holds"])
        self.assertEqual(registry["sourceCount"], 206)
        self.assertEqual(acquired["sourceCount"], 16)
        self.assertEqual(acquired["fileBytesInGit"], 0)

    def test_wave436_rouen_courts_archive_and_hold(self):
        reg=json.loads((D/"source-registry-v1.json").read_text(encoding="utf-8"))
        self.assertEqual(reg["sourceCount"],206)
        rec=next(x for x in reg["sources"] if x["id"]=="REF-S103")
        self.assertEqual(rec["evidenceClass"],"B1")
        self.assertEqual(rec["accessState"],"PARTIAL_OBJECT")
        self.assertIn("PUBLICATION_HOLD",rec["holds"])
        chapter=CH.read_text(encoding="utf-8")
        dossier=(D/"09_france_confession_nantes_source_study.md").read_text(encoding="utf-8")
        packet=(D/"independent_review_packets.md").read_text(encoding="utf-8")
        plan=(D/"SELF_PLAN.md").read_text(encoding="utf-8")
        claim=next(x for x in (D/"03_claim_verification_register.md").read_text(encoding="utf-8").splitlines() if x.startswith("| C301 |"))
        for mark in ("REF-S103","1B 110","1B 5414","3B 14","1B 801","1609","1610"):
            self.assertIn(mark,dossier)
            self.assertIn(mark,packet)
        for mark in ("REF-S103","3B 14","1610"):
            self.assertIn(mark,chapter)
            self.assertIn(mark,claim)
        for record in ("FRBNF33850380", "FRBNF36434434"):
            self.assertIn(record,dossier)
            self.assertIn(record,packet)
        self.assertIn("COUR_DES_AIDES_TRANSCRIPTION_NOT_PARLEMENT_REGISTRATION",dossier)
        self.assertIn("ROUEN_1609_1610_REGISTER_DIRECT_CHECK_HOLD",plan)
        self.assertIn("PUBLICATION_HOLD",plan)

    def test_wave437_rouen_1599_registration_1609_restrictions_1610_particulars(self):
        chapter=CH.read_text(encoding="utf-8")
        narrative, apparatus=chapter.split("## Источниковедческий аппарат",1)
        dossier=(D/"09_france_confession_nantes_source_study.md").read_text(encoding="utf-8")
        packet=(D/"independent_review_packets.md").read_text(encoding="utf-8")
        plan=(D/"SELF_PLAN.md").read_text(encoding="utf-8")
        claims=(D/"03_claim_verification_register.md").read_text(encoding="utf-8")
        c301=next(l for l in claims.splitlines() if l.startswith("| C301 |"))
        data=json.loads((D/"source-registry-v1.json").read_text(encoding="utf-8"))
        self.assertEqual(data["sourceCount"],206)
        self.assertEqual(len(data["sources"]),206)
        self.assertIn("23 сентября 1599", narrative)
        self.assertIn("5 августа 1609", narrative)
        self.assertIn("1610", narrative)
        self.assertIn("не включил 56 особых статей", narrative)
        self.assertIn("регистрац", narrative.lower())
        for marker in ("1599_GENERAL_EDICT_REGISTERED_WITH_RESERVATIONS",
                       "1609_RESTRICTIONS_LIFTED_NOT_FIRST_1599_REGISTRATION",
                       "1610_PARTICULAR_ARTICLES_SEPARATE_ACT",
                       "ROYAL_JUSSION_ORDER_NOT_EXECUTION"):
            self.assertIn(marker,dossier)
            self.assertIn(marker,packet)
            self.assertIn(marker,c301)
        for marker in ("BHH 107", "ms.11/1", "Sentilhes", "1B 799", "1B 801"):
            self.assertIn(marker,dossier)
            self.assertIn(marker,packet)
            self.assertIn(marker,plan)
        self.assertIn("wave437",next(s for s in data["sources"] if s["id"]=="REF-S103")["verificationNote"].lower())
        self.assertIn("PUBLICATION_HOLD",next(s for s in data["sources"] if s["id"]=="REF-S103")["holds"])
        self.assertIn("ORIGINAL_ART33_PRINT_COLLATION_HOLD",plan)
        self.assertIn("NOT_EDITORIAL_READY",plan)

    def test_reader_navigation_and_historical_overclaims_rejected(self):
        for path in ("README.md","SELF_PLAN.md","04_series_blueprint.md",
                     "09_france_confession_nantes_source_study.md"):
            self.assertIn(CH.name,(D/path).read_text(encoding="utf-8"))
        reg=(D/"03_claim_verification_register.md").read_text(encoding="utf-8")
        for i in range(292,304):
            self.assertIn("| C%d |"%i,reg)
        s=CH.read_text(encoding="utf-8")
        for piece in ("статья VI", "статья XIII", "статья XIV", "92 статей",
                      "56 особых", "25 февраля 1599", "2 апреля 1571",
                      "12 апреля", "совест", "не"):
            self.assertIn(piece.lower(),s.lower())

if __name__=="__main__":
    unittest.main()
