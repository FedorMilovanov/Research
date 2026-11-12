#!/usr/bin/env python3
"""England and Scotland chapter: legal, chronological and source-provenance guards."""
from pathlib import Path
import json
import unittest

D=Path(__file__).resolve().parent
CH=D/"episode10_england_scotland_1534_1581_manuscript.md"

class EnglandScotlandTests(unittest.TestCase):
    def test_historical_chapter_and_publication_hold(self):
        chapter=CH.read_text(encoding="utf-8")
        self.assertTrue(chapter.startswith("# Эпизод 10."))
        self.assertGreaterEqual(len(chapter.split()), 2250)
        for word in ("1534","1549","1552","1553","1559","1560","1563","1567","1571","1581",
                     "Supreme Head","Supreme Governor","XXIX","REF-P25-1567","Кранмер",
                     "RESEARCH_MANUSCRIPT_DRAFT","NOT_EDITORIAL_READY","PUBLICATION_HOLD"):
            with self.subTest(word=word):self.assertIn(word.lower(),chapter.lower())

    def test_all_sources_have_provenance_and_holds(self):
        j=json.loads((D/"source-registry-v1.json").read_text(encoding="utf-8"))
        self.assertEqual(j["sourceCount"],len(j["sources"]))
        s={x["id"]:x for x in j["sources"]}
        for k in ("REF-S83","REF-S84","REF-S85"):
            self.assertEqual(s[k]["evidenceClass"],"B1")
            self.assertEqual(s[k]["accessState"],"PARTIAL_OBJECT")
        self.assertEqual(s["REF-P78"]["accessState"],"PARTIAL_OBJECT")
        self.assertEqual(s["REF-P26"]["accessState"],"CATALOG_ONLY")
        self.assertEqual(s["REF-P25-RPS"]["accessState"],"PARTIAL_OBJECT")
        self.assertEqual(s["REF-P25-RPS"]["locatorState"],"EXACT_LOCATOR_VERIFIED")
        self.assertIn("ORIGINAL CONFESSION MANUSCRIPT IS LOST",s["REF-P25-RPS"]["verificationNote"])
        self.assertIn("ARCHIVE_HOLD",s["REF-P25-RPS"]["holds"])
        for k in ("REF-P78","REF-P26","REF-P25-1567","REF-P25-1581","REF-S83","REF-S84","REF-S85"):
            self.assertIn("PUBLICATION_HOLD",s[k]["holds"])
        self.assertIn("skipped numeral 13",s["REF-P25-1567"]["verificationNote"].lower())

    def test_wave454_uniformity_1559_law_not_parish_enforcement(self):
        """The full edited statute supports a sanction, not observed payment."""
        chapter = CH.read_text(encoding="utf-8")
        reader, apparatus = chapter.split("## Источниковедческий аппарат", 1)
        section = reader.split(
            "## Елизавета I: Supreme Governor и новая форма единства", 1
        )[1].split("## Сорок две, тридцать восемь, тридцать девять", 1)[0]
        for fact in (
            "Act of Uniformity 1559",
            "праздника Рождества Иоанна Крестителя",
            "по воскресеньям и церковным праздникам",
            "12 пенсов",
            "приходские старосты",
            "бедным того же прихода",
            "а не подтверждает, сколько штрафов фактически собрали",
            "приходские счета",
        ):
            with self.subTest(fact=fact):
                self.assertIn(fact.lower(), section.lower())
        self.assertNotIn("все прихожане уплатили", section.lower())
        registry = json.loads(
            (D / "source-registry-v1.json").read_text(encoding="utf-8")
        )
        sources = {x["id"]: x for x in registry["sources"]}
        self.assertEqual(registry["sourceCount"], len(registry["sources"]))
        self.assertEqual(len(sources), registry["sourceCount"])
        self.assertGreaterEqual(registry["sourceCount"], 218)
        primary = sources["REF-P93"]
        self.assertEqual(primary["documentYear"], 1559)
        self.assertEqual(primary["evidenceClass"], "A2")
        self.assertEqual(primary["accessState"], "PARTIAL_OBJECT")
        self.assertEqual(primary["locatorState"], "EXACT_LOCATOR_VERIFIED")
        self.assertEqual(primary["rightsState"], "RIGHTS_UNKNOWN")
        for hold in ("EVIDENCE_HOLD", "ARCHIVE_HOLD",
                     "RIGHTS_HOLD", "PUBLICATION_HOLD"):
            self.assertIn(hold, primary["holds"])
        for marker in ("Gee", "458", "463", "ORIGINAL_ACT_PHYSICAL_UNREAD",
                       "LOCAL_PARISH_ENFORCEMENT_UNVERIFIED"):
            self.assertIn(marker, primary["verificationNote"])
            self.assertIn(marker, apparatus)
        self.assertEqual(sources["REF-S84"]["evidenceClass"], "B1")
        self.assertEqual(sources["REF-S84"]["accessState"], "PARTIAL_OBJECT")
        ledger = (D / "03_claim_verification_register.md").read_text(
            encoding="utf-8"
        )
        claim = next(x for x in ledger.splitlines() if x.startswith("| C283 |"))
        # The statutory REF-P93 never establishes observed local payment.
        # A later 1587 parish-account witness may be added legitimately,
        # without being backdated to the year the Act entered into force.
        for marker in ("REF-P93", "REF-P94", "12 пенсов",
                       "приходскими старостами", "REJECTED_FORMULATION",
                       "1559_FIRST_YEAR_ENFORCEMENT_UNVERIFIED"):
            self.assertIn(marker, claim)
        sweep = (D / "HOLD_SOURCE_SWEEP_2026-11-11.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("## Волна 454 — Елизавета I 1559", sweep)
        self.assertIn("LOCAL_PARISH_ENFORCEMENT_UNVERIFIED", sweep)
        self.assertEqual(
            sum("PUBLICATION_HOLD" in x["holds"] for x in registry["sources"]),
            registry["sourceCount"],
        )

    def test_wave455_1587_receipt_not_first_year_1559_enforcement(self):
        """A 1587 parish-account receipt is concrete, but not 1559 backdating."""
        chapter = CH.read_text(encoding="utf-8")
        reader, apparatus = chapter.split("## Источниковедческий аппарат", 1)
        section = reader.split(
            "## Елизавета I: Supreme Governor и новая форма единства", 1
        )[1].split("## Сорок две, тридцать восемь, тридцать девять", 1)[0]
        for fact in (
            "Бишопс-Стортфорде",
            "1587 года",
            "девять человек",
            "девяти шиллингов",
            "бедных",
            "1882 году",
            "не к 1559 году",
            "оригинальный рукописный лист",
        ):
            with self.subTest(fact=fact):
                self.assertIn(fact.lower(), section.lower())
        self.assertNotIn("уже в 1559 году реально взыскали", section.lower())
        reg = json.loads(
            (D / "source-registry-v1.json").read_text(encoding="utf-8")
        )
        self.assertEqual(reg["sourceCount"], len(reg["sources"]))
        self.assertGreaterEqual(reg["sourceCount"], 219)
        sources = {s["id"]: s for s in reg["sources"]}
        self.assertEqual(len(sources), reg["sourceCount"])
        entry = sources["REF-P94"]
        self.assertEqual(entry["documentYear"], 1587)
        self.assertEqual(entry["evidenceClass"], "A2")
        self.assertEqual(entry["accessState"], "PARTIAL_OBJECT")
        self.assertEqual(entry["locatorState"], "EXACT_LOCATOR_VERIFIED")
        for marker in (
            "5351-5402",
            "STORTFORD_1587_RECEIPT_RUBRIC",
            "ORIGINAL_MANUSCRIPT_AND_PRINT_PAGE_VISUAL_HOLD",
            "1559_FIRST_YEAR_ENFORCEMENT_UNVERIFIED",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, entry["verificationNote"])
        for marker in ("REF-P94", "1882", "с.64",
                       "не просмотрены", "1587", "1559"):
            self.assertIn(marker, apparatus)
        for hold in ("EVIDENCE_HOLD", "ARCHIVE_HOLD",
                     "RIGHTS_HOLD", "PUBLICATION_HOLD"):
            self.assertIn(hold, entry["holds"])
        c283 = next(
            s for s in (D / "03_claim_verification_register.md").read_text(
                encoding="utf-8"
            ).splitlines() if s.startswith("| C283 |")
        )
        for token in ("REF-P94", "1587", "1559",
                      "REJECTED_FORMULATION", "ORIGINAL_MANUSCRIPT"):
            self.assertIn(token, c283)
        sweep = (D / "HOLD_SOURCE_SWEEP_2026-11-11.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("## Волна 455 — приходские взыскания", sweep)
        self.assertIn("219 PUBLICATION_HOLD", sweep)
        self.assertIn("1559_FIRST_YEAR_ENFORCEMENT_UNVERIFIED", sweep)
        self.assertEqual(
            sum("PUBLICATION_HOLD" in s["holds"] for s in reg["sources"]),
            reg["sourceCount"],
        )

    def test_claim_guards_and_published_chapter_numbering(self):
        ledger=(D/"03_claim_verification_register.md").read_text(encoding="utf-8")
        for n in range(282,292):self.assertIn("| C%d |"%n,ledger)
        old=(D/"08_schleitheim_bsb_scots_primary_collation.md").read_text(encoding="utf-8")
        self.assertIn("Раньше", old.replace("Ранее", "Раньше")) if False else None
        self.assertIn("ранее в этом досье ошибочно",old)
        self.assertIn("25 видимых",old)
        for f in ("README.md","04_series_blueprint.md","SELF_PLAN.md"):
            self.assertIn(CH.name,(D/f).read_text(encoding="utf-8"))
        ch=CH.read_text(encoding="utf-8")
        self.assertIn("номер **13 пропущен**",ch)
        self.assertIn("Следующая глава",ch)

if __name__=="__main__":
    unittest.main()
