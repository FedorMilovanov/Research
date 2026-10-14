"""Local pinned-data controls plus fail-closed CLI regressions (no network)."""
from __future__ import annotations

import contextlib
import io
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

sys.dont_write_bytecode = True
TOOLS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOLS))
import nt_sources
import mt_lookup
import mt_lxx_collation as collation
import manuscript_collation as manuscripts
from sbl_apparatus import Apparatus
from verify_nt_facts import computed_facts, validate_states
from verify_nt_variants import computed_variants


class PinnedCorpusTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = nt_sources.registry()
        cls.facts = computed_facts()
        cls.variants = computed_variants()
        cls.app = Apparatus()
        cls.colls = manuscripts.load_all()

    def test_canonical_states_and_historical_excerpts(self):
        self.assertEqual(validate_states(self.data), [])

    def test_facts_match_ssot(self):
        self.assertEqual(self.facts, self.data["verifiedComputedFacts"])

    def test_article_and_homograph_negative_regressions(self):
        grammar = self.facts["grammar"]
        self.assertEqual(grammar["MT_Isa53_articles_before_rab"], {"Isaiah 53:11":1,"Isaiah 53:12":1})
        self.assertEqual(grammar["MT_kpr_lex_utf8_by_sp"], {"verb":102,"subs":20})
        self.assertEqual(grammar["John6_37_piAn_count"], 1)
        self.assertEqual(grammar["Rev5_9_pas_lemma_count"], 1)
        self.assertEqual(grammar["Gal3_13_katara_tags"], ["----NSF-"])
        self.assertEqual(grammar["Matthew11_28_deute_pos"], ["D-"])
        self.assertEqual(grammar["1John2_2_article_before_sins"], 1)
        self.assertEqual(grammar["1John4_10_article_before_sins"], 1)

    def test_false_lxx_lemma_zeros_stay_refuted(self):
        probes = self.facts["lxxProbes"]
        self.assertEqual(probes["prefixCounts"]["ἱλασκ"], 0)
        self.assertEqual(probes["simplexHilasNonNounTokens"], 11)
        self.assertEqual(probes["positiveInflectedForms"]["Daniel_translatio_Graeca 4:30c"], "ἀπολυτρώσεως")
        self.assertEqual(probes["prefixCounts"]["καταλλαγ"], 5)

    def test_word_controls_match_ssot(self):
        self.assertEqual(self.variants, self.data["verifiedVariantControls"])
        self.assertEqual(self.variants["offerEqualInAllThreeTR"], 7)
        self.assertEqual(len(self.variants["wordEquality"]), 27)
        self.assertFalse(any(self.variants["wordEquality"]["Мк 14:24"].values()))
        self.assertFalse(any(self.variants["wordEquality"]["Мф 26:28"].values()))

    def test_s7_absent_na_is_not_implicit_agreement(self):
        readings = [r for e in self.app.at("Евр 2:9") for r in e["rdg"]]
        self.assertFalse(any("NA" in r["wit"] for r in readings))
        self.assertTrue(any("Treg" in r["wit"] and r["text"] == "χάριτι" for r in readings))
        self.assertEqual(self.app.count(), 6929)

    def test_xml_comments_not_active_and_mark_quarantined(self):
        byid = {c.sid:c for c in self.colls}
        self.assertEqual((byid["S10a"].active_unit_count, byid["S10a"].n_wit), (9554,600))
        self.assertEqual((byid["S10b"].active_unit_count, byid["S10b"].n_wit), (147,167))
        self.assertEqual(len(byid["S10b"].units), 146)
        self.assertEqual([u.uid for u in byid["S10b"].quarantined_units], ["B02K28V8U2-20"])
        self.assertEqual(byid["S10b"].at("Мк",28,8), [])
        self.assertEqual(sum(c.active_unit_count for c in self.colls), 9997)
        self.assertEqual(sum(len(c.units) for c in self.colls if c.sid != "S10b"), 9850)
        self.assertEqual(manuscripts.probe_counts(self.colls), self.data["manuscriptCollation"]["verifiedProbeCounts"])

    def test_wrong_book_probe_returns_failure(self):
        fake = SimpleNamespace(sid="fixture",book="Мк",verify_book=lambda s:(1,[("Лк",4),("Мк",1)]),
                               max_chapter=lambda:1,book_code=lambda:"02",rdg_a_matches_s1=lambda s:(0,0))
        with patch.object(manuscripts,"load_all",return_value=[fake]), \
             patch.object(manuscripts,"witness_dir",return_value=Path("/missing-fixture")), \
             patch.object(manuscripts,"load_s1",return_value={("02",1,1):"word",("03",1,1):"word"}), \
             contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(manuscripts.main(["--verify"]),1)

    def test_mt_missing_verse_returns_failure(self):
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(mt_lookup.main(["Genesis 999:1"]),1)

    def test_unexpected_lxx_word_failure_is_not_green(self):
        real = collation.LXX(collation.LXX_ROOT)
        old_has = real.has
        real.has = lambda ref,prefix: False if ref == "Exodus 25:16" else old_has(ref,prefix)
        with patch.object(collation,"LXX",return_value=real), contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(collation.main([]),1)

    def test_cli_missing_corpus_never_passes_or_fetches(self):
        names = ["nt_sources.py", "verify_nt_citations.py", "verify_nt_facts.py", "verify_nt_variants.py",
                 "mt_lookup.py", "mt_lxx_collation.py", "sbl_apparatus.py", "pericope_apparatus_sweep.py",
                 "manuscript_collation.py"]
        with tempfile.TemporaryDirectory() as d:
            env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", NT_CORPUS_HOME=d,
                       NT_SBLGNT_DIR=str(Path(d)/"S1"), NT_LXX_DIR=str(Path(d)/"S5"),
                       NT_MT_DIR=str(Path(d)/"S6"), NT_APPARATUS_XML=str(Path(d)/"S7.xml"))
            for name in names:
                with self.subTest(tool=name):
                    result = subprocess.run([sys.executable,str(TOOLS/name)],env=env,
                                            capture_output=True,text=True,timeout=15)
                    self.assertNotEqual(result.returncode,0,result.stdout)
                    self.assertNotIn("PASS:",result.stdout)
            self.assertEqual(list(Path(d).iterdir()), [], "validators must not implicitly fetch/write")


if __name__ == "__main__":
    unittest.main()
