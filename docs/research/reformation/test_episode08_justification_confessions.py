#!/usr/bin/env python3
"""Evidence, historical chronology and publication guards for episode 08."""
from pathlib import Path
import json
import unittest

D = Path(__file__).resolve().parent
E8 = D / "episode08_justification_confessions_1530_1563_manuscript.md"

class JustificationBookTests(unittest.TestCase):
    def test_coherent_chapter_and_distinct_dates(self):
        content=E8.read_text(encoding="utf-8")
        self.assertTrue(content.startswith("# Эпизод 08."))
        self.assertGreaterEqual(len(content.split()), 1700)
        for marker in ("1530", "1547", "1563", "Меланхтон", "Аугсбург",
                       "Тридент", "Гейдельберг", "Источниковедческий аппарат",
                       "RESEARCH_MANUSCRIPT_DRAFT", "NOT_EDITORIAL_READY", "PUBLICATION_HOLD"):
            with self.subTest(marker=marker):
                self.assertIn(marker.lower(), content.lower())
        self.assertIn("следующей главе", content.lower())

    def test_arguments_not_flattened_and_primary_status_honest(self):
        content=E8.read_text(encoding="utf-8")
        for marker in ("статья IV", "статья VI", "статья XX",
                       "канон IX", "канон XI", "канон XXIV",
                       "вопросе 60", "вопрос 64", "первопечат",
                       "баптист", "не", "благодат"):
            with self.subTest(marker=marker):
                self.assertIn(marker.lower(), content.lower())
        r=json.loads((D/"source-registry-v1.json").read_text(encoding="utf-8"))
        s={x["id"]: x for x in r["sources"]}
        self.assertEqual(r["sourceCount"],len(r["sources"]))
        self.assertEqual(s["REF-P17"]["accessState"],"CATALOG_ONLY")
        self.assertEqual(s["REF-P77"]["accessState"],"PARTIAL_OBJECT")
        self.assertEqual(s["REF-P77"]["locatorState"],"EXACT_LOCATOR_VERIFIED")
        self.assertEqual(s["REF-P14"]["accessState"],"PARTIAL_OBJECT")
        self.assertEqual(s["REF-P20"]["accessState"],"PARTIAL_OBJECT")
        for id in ("REF-P14","REF-P17","REF-P20","REF-P77"):
            self.assertIn("PUBLICATION_HOLD",s[id]["holds"])

    def test_wave426_augsburg_V_and_IX_are_distinct_confessional_charges(self):
        """Chapter 08 must tell the reader what the 1530 text says without
        claiming its polemical portrait was proved for all Anabaptists.
        """
        content = E8.read_text(encoding="utf-8")
        reader, apparatus = content.split(
            "## Источниковедческий аппарат — вне основного повествования", 1
        )
        for token in (
            "**статья V**", "**статье IX**", "внешнего Слова",
            "собственным приготовлениям и делам",
            "крестить младенцев",
            "каждый анабаптист",
            "по их собственным исповеданиям",
        ):
            with self.subTest(reader_token=token):
                self.assertIn(token, reader)
        self.assertLess(reader.index("**статья V**"), reader.index("**статье IX**"))
        self.assertNotIn("REF-P14", reader)
        self.assertNotIn("RESEARCH_MANUSCRIPT_DRAFT", reader)
        for token in (
            "REF-P14", "статьи V и IX",
            "ORIGINAL_LANGUAGE_HOLD", "INDEPENDENT_EXTERNAL_REVIEW_OPEN",
            "THEOLOGICAL_PEER_REVIEW_OPEN", "RIGHTS_HOLD",
            "PUBLICATION_HOLD",
        ):
            with self.subTest(apparatus_token=token):
                self.assertIn(token, apparatus)

        sources = json.loads(
            (D / "source-registry-v1.json").read_text(encoding="utf-8")
        )
        self.assertGreaterEqual(sources["sourceCount"], 205)
        rows = {row["id"]: row for row in sources["sources"]}
        self.assertEqual(rows["REF-P14"]["accessState"], "PARTIAL_OBJECT")
        self.assertEqual(rows["REF-P20"]["accessState"], "PARTIAL_OBJECT")
        for source_id, marker in (
            ("REF-P14", "2026-11-11 WAVE426"),
            ("REF-P20", "2026-11-11 WAVE426"),
        ):
            with self.subTest(source=source_id):
                row = rows[source_id]
                self.assertIn(marker, row["verificationNote"])
                self.assertTrue(any(word in row["verificationNote"].lower()
                                    for word in ("not independently collated",
                                                 "yet to collate", "uncollated")))
                self.assertIn("RIGHTS_HOLD", row["holds"])
                self.assertIn("PUBLICATION_HOLD", row["holds"])
        ledger = (D / "03_claim_verification_register.md").read_text(
            encoding="utf-8"
        )
        c273 = next(line for line in ledger.splitlines()
                    if line.startswith("| C273 |"))
        for token in ("ст. V и IX", "полемические формулировки",
                      "ORIGINAL_LANGUAGE_HOLD", "REJECTED_FORMULATION"):
            with self.subTest(claim_token=token):
                self.assertIn(token, c273)
        reviewer = (D / "independent_review_packets.md").read_text(
            encoding="utf-8"
        )
        t02 = next(line for line in reviewer.splitlines()
                   if line.startswith("| T-02 /"))
        self.assertIn("Аугсбургское исповедание **V/IX**", t02)
        self.assertIn("REVIEW_PACKETS_PREPARED / NOT_SENT", reviewer)
        plan = (D / "SELF_PLAN.md").read_text(encoding="utf-8")
        active_plan = plan.split("---", 1)[0]
        self.assertIn("ТЕКУЩИЙ ПАСПОРТ И ОЧЕРЕДЬ", active_plan)
        self.assertIn("RF-EDITORIAL-EP08-AUGSBURG-V-IX-ANABAPTIST-SCOPE", plan)
        self.assertIn("INDEPENDENT_EXTERNAL_REVIEW_OPEN", active_plan)
        self.assertIn("THEOLOGICAL_PEER_REVIEW_OPEN", active_plan)
        self.assertIn("PUBLICATION_HOLD", active_plan)

    def test_wave443_trent_latin_and_first_print_not_conflated(self):
        """Original-language web transcription is checked, but no Paris 1547
        print image was declared collation-complete and no peer-review invented.
        """
        chapter = E8.read_text(encoding="utf-8")
        _, apparatus = chapter.split(
            "## Источниковедческий аппарат — вне основного повествования", 1
        )
        for token in (
            "Canon XIII", "Canon XXIV", "omni homini",
            "nihil aliud requiri", "exclusa gratia et charitate",
            "iustitiam acceptam", "B-6903 (2)",
            "A–E⁴", "editio princeps 1531",
            "Q 7188-4 B RES", "не сверены визуально",
            "INDEPENDENT_CONFESSIONAL_REVIEW_OPEN",
        ):
            with self.subTest(token=token):
                self.assertIn(token, apparatus)
        registry = json.loads(
            (D / "source-registry-v1.json").read_text(encoding="utf-8")
        )
        by = {row["id"]: row for row in registry["sources"]}
        for source_id in ("REF-P14", "REF-P17", "REF-P20"):
            self.assertIn("WAVE443-T03-LATIN", by[source_id]["verificationNote"])
            self.assertIn("PUBLICATION_HOLD", by[source_id]["holds"])
        self.assertEqual(by["REF-P20"]["accessState"], "PARTIAL_OBJECT")
        self.assertIn("LOCATOR_HOLD", by["REF-P20"]["holds"])
        self.assertEqual(by["REF-P17"]["accessState"], "CATALOG_ONLY")
        self.assertIn("ARCHIVE_HOLD", by["REF-P17"]["holds"])
        self.assertIn("LOCATOR_HOLD", by["REF-P17"]["holds"])

    def test_wave443_direct_heidelberg_third_print_without_spurious_release(self):
        """Visually reviewed original 1563 printed pp 42–44 are evidence of
        Q60–64 only, not first/second editions or blanket reuse permissions.
        """
        chapter = E8.read_text(encoding="utf-8")
        self.assertIn("**REF-P89 — ВОЛНА 443", chapter)
        self.assertIn("печатным страницам 42–44", chapter)
        self.assertIn("PDF стр. 48–50", chapter)
        for q in range(60, 65):
            with self.subTest(question=q):
                self.assertIn(f"| **{q}** |", chapter)
        for marker in (
            "ORIGINAL_1563_THIRD_EDITION_Q60_Q64_PAGE_IMAGES_DIRECTLY_VIEWED",
            "RIGHTS_HOLD", "ARCHIVE_HOLD", "PUBLICATION_HOLD",
            "первое и второе немецкие издания",
        ):
            self.assertIn(marker, chapter)

        reg = json.loads((D / "source-registry-v1.json").read_text(encoding="utf-8"))
        rows = {x["id"]: x for x in reg["sources"]}
        self.assertEqual(reg["sourceCount"], len(rows))
        self.assertEqual(rows["REF-P17"]["accessState"], "CATALOG_ONLY")
        p89 = rows["REF-P89"]
        self.assertEqual(p89["documentYear"], 1563)
        self.assertEqual(p89["accessState"], "PARTIAL_OBJECT")
        self.assertEqual(p89["locatorState"], "EXACT_LOCATOR_VERIFIED")
        self.assertEqual(p89["rightsState"], "RIGHTS_UNKNOWN")
        for h in ("ARCHIVE_HOLD", "RIGHTS_HOLD", "PUBLICATION_HOLD"):
            self.assertIn(h, p89["holds"])
        self.assertIn("FIRSTHAND_VISUAL_IMAGE_READ", p89["verificationNote"])
        self.assertIn("PDF digital pages 48, 49, 50", p89["verificationNote"])
        manifest = json.loads(
            (D / "acquisition-manifest-v1.json").read_text(encoding="utf-8")
        )
        self.assertEqual(manifest["sourceCount"], len(manifest["sourceRecords"]))
        rec = next(x for x in manifest["sourceRecords"] if x["id"] == "REF-P89")
        self.assertEqual(rec["actualBytes"], 12055145)
        self.assertEqual(
            rec["sha256"],
            "9a418fefc3541f772cca13d3bf4a41c0d4195e03aaa66f51571fc20a35e93f44",
        )
        self.assertEqual(rec["retainedLocalCopy"]["visuallyInspectedPdfPages"], [48, 49, 50])
        self.assertFalse(rec["retainedLocalCopy"]["allPagesWordByWordTranscribed"])
        self.assertFalse(rec["retainedLocalCopy"]["firstOrSecond1563EditionCollated"])
        self.assertEqual(manifest["fileBytesInGit"], 0)
        claim_lines = (D / "03_claim_verification_register.md").read_text(
            encoding="utf-8").splitlines()
        for id in (272, 273):
            line = next(x for x in claim_lines if x.startswith(f"| C{id} |"))
            self.assertIn("REF-P89", line)
            self.assertIn("PUBLICATION_HOLD" if id == 272 else "THEOLOGICAL_PEER_REVIEW_OPEN", line)

    def test_wave443_cologne_original_print_exact_canons_with_paris_hold(self):
        """The Cologne 1547 primary print was visually read at precisely three
        canvases; the Paris 1547 edition and full council text were not."""
        apparatus = E8.read_text(encoding="utf-8").split(
            "## Источниковедческий аппарат — вне основного повествования", 1
        )[1]
        for token in (
            "REF-P90", "VD16 K2078", "bsb10176467", "scan 27",
            "scan 28", "scan 31", "BP16_112717",
            "ARCHIVE_HOLD", "RIGHTS_HOLD", "PUBLICATION_HOLD",
            "INDEPENDENT_CONFESSIONAL_REVIEW_OPEN",
        ):
            with self.subTest(token=token):
                self.assertIn(token, apparatus)
        registry = json.loads((D / "source-registry-v1.json").read_text(encoding="utf-8"))
        p = {x["id"]: x for x in registry["sources"]}
        cologne = p["REF-P90"]
        self.assertEqual(cologne["documentYear"], 1547)
        self.assertEqual(cologne["accessState"], "PARTIAL_OBJECT")
        self.assertEqual(cologne["locatorState"], "EXACT_LOCATOR_VERIFIED")
        self.assertEqual(cologne["rightsState"], "PERMISSION_REQUIRED")
        self.assertIn("NoC-NC/1.0", cologne["verificationNote"])
        for hold in ("ARCHIVE_HOLD", "RIGHTS_HOLD", "PUBLICATION_HOLD"):
            self.assertIn(hold, cologne["holds"])
        self.assertIn("DIRECT_VISUAL_ORIGINAL_LATIN_PRINT_CHECKED", cologne["verificationNote"])
        self.assertIn("Gallica", p["REF-P20"]["verificationNote"]
                      + cologne["verificationNote"])
        self.assertIn("LOCATOR_HOLD", p["REF-P20"]["holds"])
        manifest = json.loads((D / "acquisition-manifest-v1.json").read_text(encoding="utf-8"))
        rec = next(row for row in manifest["sourceRecords"] if row["id"] == "REF-P90")
        self.assertEqual(manifest["sourceCount"], len(manifest["sourceRecords"]))
        self.assertEqual(rec["acquisitionState"], "VERIFIED_TEMP_DISCARDED")
        self.assertEqual(rec["actualBytes"], 68660)
        self.assertEqual(rec["sha256"],
                         "5333a30ba575d635e0802029c9a0ee074adffc821c814a6e54ceae0b529853d4")
        self.assertEqual([x["scan"] for x in rec["derivativeReceipts"]], [27, 28, 31])
        self.assertIn("TEMP_CLEANED=True", rec["tempDisposition"])
        self.assertEqual(manifest["fileBytesInGit"], 0)
        ledger = (D / "03_claim_verification_register.md").read_text(encoding="utf-8")
        for claim_id in (27, 271):
            row = next(line for line in ledger.splitlines()
                       if line.startswith(f"| C{claim_id} |"))
            self.assertIn("REF-P90", row)
            self.assertIn("PARIS_1547_VARIANT_HOLD", row)

    def test_wave445_augsburg_print_history_and_trent_xiii_reader_gates(self):
        """Presentation-year manuscripts, unauthorized prints and authorized
        1531 edition must not be conflated with direct page collation.
        Trent XIII concerns required certainty for each, not every hope.
        """
        chapter = E8.read_text(encoding="utf-8")
        reader, apparatus = chapter.split(
            "## Источниковедческий аппарат — вне основного повествования", 1
        )
        for token in (
            "25 июня 1530 года",
            "несанкционированные издания",
            "авторизованная печатная редакция",
            "1531 году",
            "**Канон XIII**",
            "*каждому человеку необходимо*",
            "Это не запрет всякого доверия",
        ):
            with self.subTest(reader_token=token):
                self.assertIn(token, reader)
        self.assertNotIn("REF-P14", reader)
        self.assertNotIn("NOT_EDITORIAL_READY", reader)
        for token in (
            "Bridwell", "BRA2651/A–B",
            "Georg Rhau, 1531", "несанкционированные печати",
            "страницы физического экземпляра Bridwell",
            "REF-P90", "REF-P89",
            "REF-P20", "ORIGINAL_EDITION_COLLATION_HOLD",
            "Кёльн", "парижские", "не коллированы",
            "INDEPENDENT_CONFESSIONAL_REVIEW_OPEN",
            "THEOLOGICAL_PEER_REVIEW_OPEN", "PUBLICATION_HOLD",
        ):
            with self.subTest(apparatus_token=token):
                self.assertIn(token, apparatus)
        # These absolute claims became false after scoped visual inspection
        # of two historical print witnesses in wave 443.
        self.assertNotIn(
            "оригинальные немецкая/латинская редакции Аугсбургского исповедания;"
            " официальный латинский текст Тридента VI и его канонов;",
            apparatus,
        )

        registry = json.loads(
            (D / "source-registry-v1.json").read_text(encoding="utf-8")
        )
        rows = {row["id"]: row for row in registry["sources"]}
        self.assertEqual(registry["sourceCount"], 215)
        self.assertEqual(len(rows), 215)
        a = rows["REF-P14"]
        self.assertEqual(a["documentYear"], 1530)
        self.assertEqual(a["accessState"], "PARTIAL_OBJECT")
        self.assertEqual(a["rightsState"], "RIGHTS_UNKNOWN")
        self.assertIn("Bridwell", a["verificationNote"])
        self.assertIn("NOT inspected 1531 leaf images", a["verificationNote"])
        self.assertIn("PUBLICATION_HOLD", a["holds"])
        self.assertIn("RIGHTS_HOLD", a["holds"])
        t = rows["REF-P20"]
        self.assertIn("LOCATOR_HOLD", t["holds"])
        self.assertIn("PUBLICATION_HOLD", t["holds"])
        ledger = (D / "03_claim_verification_register.md").read_text(
            encoding="utf-8"
        )
        for cid in (269, 273):
            row = next(line for line in ledger.splitlines()
                       if line.startswith(f"| C{cid} |"))
            self.assertIn("1531", row)
            self.assertIn("не коллированы", row
                          if cid == 273 else row.replace(
                              "не сопоставлены", "не коллированы"))
            self.assertIn("REJECTED_FORMULATION", row)
        plan = (D / "SELF_PLAN.md").read_text(encoding="utf-8")
        current = plan.split("\n---\n", 1)[0]
        self.assertIn("волна 445", current)
        self.assertIn("214 PUBLICATION_HOLD", current)
        self.assertIn("INDEPENDENT_EXTERNAL_REVIEW_OPEN", current)
        self.assertIn("THEOLOGICAL_PEER_REVIEW_OPEN", current)

    def test_wave446_apologia_original_print_does_not_masquerade_as_augsburg1530(self):
        """A directly read Apologia 1531 witness is not direct CA 1530/31
        text collation and never carries an image reuse permission."""
        chapter = E8.read_text(encoding="utf-8")
        reader, apparatus = chapter.split(
            "## Источниковедческий аппарат — вне основного повествования", 1
        )
        for token in (
            "## Апология 1531 года",
            "Что такое оправдывающая вера?",
            "исторических событий",
            "не на основании собственных заслуг",
            "шестнадцать лет спустя",
        ):
            with self.subTest(reader=token):
                self.assertIn(token, reader)
        self.assertNotIn("REF-P91", reader)
        for token in (
            "REF-P91", "bsb11411960", "VD16 C4734",
            "цифровой кадр 24", "кадр 25", "кадр 26",
            "QVID SIT FIDES IVSTIFICANS",
            "assentiri promissioni Dei",
            "non operibus, sed sola fide",
            "отдельного латинского первоисточника",
            "PERMISSION_REQUIRED",
            "ARCHIVE_HOLD", "RIGHTS_HOLD", "PUBLICATION_HOLD",
        ):
            with self.subTest(apparatus=token):
                self.assertIn(token, apparatus)
        registry = json.loads(
            (D / "source-registry-v1.json").read_text(encoding="utf-8")
        )
        rows = {row["id"]: row for row in registry["sources"]}
        self.assertEqual(len(rows), 215)
        self.assertEqual(registry["sourceCount"], len(rows))
        p91 = rows["REF-P91"]
        self.assertEqual(p91["documentYear"], 1531)
        self.assertEqual(p91["evidenceClass"], "A1")
        self.assertEqual(p91["accessState"], "PARTIAL_OBJECT")
        self.assertEqual(p91["locatorState"], "EXACT_LOCATOR_VERIFIED")
        self.assertEqual(p91["rightsState"], "PERMISSION_REQUIRED")
        self.assertEqual(p91["publicationState"], "REFERENCE")
        self.assertEqual(set(p91["holds"]), {
            "ARCHIVE_HOLD", "RIGHTS_HOLD", "PUBLICATION_HOLD",
        })
        for token in (
            "APOLOGIA", "noticiam historiae", "manifest 294469 bytes",
            "DIRECTLY VISUALLY READ", "NO new acquisition manifest receipt",
        ):
            self.assertIn(token, p91["verificationNote"])
        self.assertEqual(rows["REF-P14"]["documentYear"], 1530)
        self.assertEqual(rows["REF-P14"]["accessState"], "PARTIAL_OBJECT")
        claim = next(
            x for x in (D / "03_claim_verification_register.md")
            .read_text(encoding="utf-8").splitlines()
            if x.startswith("| C269 |")
        )
        self.assertIn("REF-P91", claim)
        self.assertIn("другой текст", claim)
        manifest = json.loads(
            (D / "acquisition-manifest-v1.json").read_text(encoding="utf-8")
        )
        self.assertEqual(manifest["sourceCount"], 18)
        self.assertEqual(len(manifest["sourceRecords"]), 18)
        self.assertNotIn("REF-P91", [x["id"] for x in manifest["sourceRecords"]])
        self.assertEqual(manifest["fileBytesInGit"], 0)
        matrix = (D / "HOLD_SOURCE_SWEEP_2026-11-11.md").read_text(
            encoding="utf-8")
        for token in ("### 446.1.", "scan 24", "scan 25", "scan 26",
                      "215 REF / 319 C / 18 acquisition receipts"):
            self.assertIn(token, matrix)
        plan = (D / "SELF_PLAN.md").read_text(encoding="utf-8")
        current = plan.split("\n---\n", 1)[0]
        for token in ("волна 446", "215 REF", "215 PUBLICATION_HOLD",
                      "INDEPENDENT_EXTERNAL_REVIEW_OPEN",
                      "THEOLOGICAL_PEER_REVIEW_OPEN"):
            self.assertIn(token, current)

    def test_registry_and_book_navigation(self):
        ledger=(D/"03_claim_verification_register.md").read_text(encoding="utf-8")
        for i in range(268,274):
            self.assertIn("| C%d |"%i,ledger)
        for filename in ("README.md","SELF_PLAN.md","04_series_blueprint.md"):
            self.assertIn(E8.name, (D/filename).read_text(encoding="utf-8"))
        readme=(D/"README.md").read_text(encoding="utf-8")
        self.assertLess(readme.find("episode07_luther_peasants_war"),readme.find(E8.name))
        self.assertIn("NOT_EDITORIAL_READY",(D/"SELF_PLAN.md").read_text(encoding="utf-8"))
        self.assertIn("немецкой транскрипции GHDI",(D/"episode07_luther_peasants_war_1524_1525_manuscript.md").read_text(encoding="utf-8"))

if __name__=="__main__":
    unittest.main()
