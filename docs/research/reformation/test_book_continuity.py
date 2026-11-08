#!/usr/bin/env python3
"""Fail-closed, read-only whole-book navigation and release-gate checks.

Internal integrity of existing manuscripts is testable; independent history,
theological review, original-language collation and image/translation rights are
not inferred from a passing test.
"""
from pathlib import Path
from urllib.parse import unquote
import json
import re
import unittest

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2].resolve()
PARTS = (
    "00_introduction_manuscript.md",
    "episode01_historical_gateway_draft.md",
    "episode02_indulgences_1517_manuscript.md",
    "episode03_luther_worms_1520_1521_manuscript.md",
    "episode04_zurich_zwingli_1523_1525_manuscript.md",
    "episode05_marburg_colloquy_1529_manuscript.md",
    "episode06_schleitheim_1527_1529_manuscript.md",
    "episode07_luther_peasants_war_1524_1525_manuscript.md",
    "episode08_justification_confessions_1530_1563_manuscript.md",
    "episode09_calvin_geneva_1535_1555_manuscript.md",
    "episode10_england_scotland_1534_1581_manuscript.md",
    "episode11_france_catholic_reform_nantes_1545_1599_manuscript.md",
    "episode12_reformation_everyday_life_1520_1600_manuscript.md",
    "epilogue_reformation_last_restoration_manuscript.md",
)
LINK_RE = re.compile(r"\]\(([^)]+)\)")
REF_RE = re.compile(r"\bREF-[A-Z0-9]+(?:-[A-Z0-9]+)*\b")
CLAIM_RE = re.compile(r"^\| C([0-9]+) \|", flags=re.MULTILINE)


class BookContinuityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.texts = {
            name: (HERE / name).read_text(encoding="utf-8") for name in PARTS
        }

    def test_single_complete_ordered_fourteen_part_book(self):
        self.assertEqual(len(PARTS), 14)
        self.assertEqual(len(PARTS), len(set(PARTS)))
        self.assertEqual(PARTS[0], "00_introduction_manuscript.md")
        self.assertEqual(PARTS[-1], "epilogue_reformation_last_restoration_manuscript.md")
        for i, name in enumerate(PARTS[1:-1], 1):
            with self.subTest(chapter=i):
                self.assertTrue(self.texts[name].startswith(f"# Эпизод {i:02}."))
        actual = {p.name for p in HERE.glob("episode[0-9][0-9]_*_manuscript.md")}
        actual.add("episode01_historical_gateway_draft.md")
        self.assertEqual(actual, set(PARTS[1:-1]),
                         "Do not silently create or omit a thirteenth historical chapter")

    def test_all_thirteen_forward_transitions_in_reader_text(self):
        for src, dest in zip(PARTS, PARTS[1:]):
            reader = self.texts[src].split("## Источниковедчес", 1)[0]
            with self.subTest(src=src, dest=dest):
                self.assertIn("](" + dest + ")", reader,
                              "Forward book navigation must be present in reader prose")
        self.assertIn("1530, 1547 и 1563", self.texts[PARTS[8]])
        self.assertIn("1535–1555", self.texts[PARTS[8]])
        self.assertIn("1534–1581", self.texts[PARTS[9]])
        self.assertIn("1545–1599", self.texts[PARTS[10]])

    def test_every_local_markdown_link_resolves_inside_repository(self):
        for name, content in self.texts.items():
            for raw in LINK_RE.findall(content):
                dest = raw.split(None, 1)[0]  # ignore optional Markdown title
                if dest.startswith(("http://", "https://", "mailto:", "#")):
                    continue
                rel = unquote(dest).split("#", 1)[0].split("?", 1)[0]
                if not rel.lower().endswith(".md"):
                    continue
                target = (HERE / rel).resolve()
                with self.subTest(chapter=name, target=rel):
                    self.assertTrue(target.is_relative_to(REPO), "link leaves repository")
                    self.assertTrue(target.is_file(), "local book reference is broken")

    def test_source_ids_are_registered_and_claims_remain_contiguous(self):
        registry = json.loads(
            (HERE / "source-registry-v1.json").read_text(encoding="utf-8")
        )
        sources = registry["sources"]
        ids = [entry["id"] for entry in sources]
        self.assertEqual(registry["sourceCount"], 204)
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(len(ids), registry["sourceCount"])
        known = set(ids)
        for name, content in self.texts.items():
            for sid in set(REF_RE.findall(content)):
                with self.subTest(book=name, source=sid):
                    self.assertIn(sid, known, "do not cite invented source IDs")
        claims = (HERE / "03_claim_verification_register.md").read_text(encoding="utf-8")
        numbered = [int(x) for x in CLAIM_RE.findall(claims)]
        self.assertEqual(numbered, list(range(1, 320)))
        self.assertIn("| C302 |", claims)
        # C315 must follow the actual 14-part book without promoting publication.
        c315 = next((line for line in claims.splitlines() if line.startswith("| C315 |")), None)
        self.assertIsNotNone(c315)
        self.assertIn("уже написанный богословский эпилог", c315)
        self.assertIn("14 частей", c315)
        self.assertIn("REJECTED_FORMULATION", c315)
        self.assertIn("PUBLICATION_HOLD", c315)
        self.assertNotIn("ещё не написанный богословский эпилог", c315)
        self.assertIn("95 общих статей", claims)
        self.assertIn("92", claims)

    def test_wave402_independent_review_packets_are_complete_not_approved(self):
        """Cross-book review coverage is testable; expert endorsement is not."""
        packet = (HERE / "independent_review_packets.md").read_text(encoding="utf-8")
        self.assertIn("Пакет A — независимый историк", packet)
        self.assertIn("Пакет B — независимый богослов", packet)
        self.assertIn("REVIEW_PACKETS_PREPARED / NOT_SENT", packet)
        self.assertIn("INDEPENDENT_EXTERNAL_REVIEW_OPEN", packet)
        self.assertIn("THEOLOGICAL_PEER_REVIEW_OPEN", packet)
        self.assertIn("PUBLICATION_HOLD", packet)
        self.assertIn("ORIGINAL_PRINT_COLLATION_HOLD", packet)
        self.assertIn("ARCHIVE_HOLD", packet)
        self.assertIn("RIGHTS_HOLD", packet)
        for name in PARTS:
            with self.subTest(part=name):
                self.assertIn("](" + name + ")", packet)
        for prefix, total in (("H", 9), ("T", 8)):
            for i in range(1, total + 1):
                with self.subTest(review=f"{prefix}-{i:02}"):
                    self.assertIn(f"{prefix}-{i:02}", packet)
            self.assertNotIn(f"{prefix}-{total + 1:02}", packet)

        plan = (HERE / "SELF_PLAN.md").read_text(encoding="utf-8")
        # Wave 402's evidence contract persists after its passport becomes history.
        self.assertRegex(
            plan,
            r"(?m)^## (?:ТЕКУЩИЙ ПАСПОРТ И ОЧЕРЕДЬ — волна 402\\b|ИСТОРИЧЕСКИЙ СРЕЗ ВОЛНЫ 402\\b)".replace("\\\\", "\\"),
        )
        active = re.findall(r"(?m)^## ТЕКУЩИЙ ПАСПОРТ И ОЧЕРЕДЬ — волна \d+\b", plan)
        self.assertEqual(len(active), 1, "the self-plan must have exactly one active wave")
        self.assertIn("ИСТОРИЧЕСКИЙ СРЕЗ ВОЛНЫ 401", plan)
        self.assertIn("](independent_review_packets.md)", plan)
        self.assertIn("NOT_SENT", plan)

        # Editorial handoff must cover omitted physical witnesses and chronology.
        rows = {label: next(
            (line for line in packet.splitlines() if line.startswith("| " + label + " /")),
            None,
        ) for label in ("H-03", "H-04", "H-08", "T-02")}
        for label, row in rows.items():
            with self.subTest(review=label):
                self.assertIsNotNone(row)
        for marker in ("C257–C261", "C181, C207", "REF-P24-BSB1/BSB2",
                       "REF-P11/P12"):
            self.assertIn(marker, rows["H-03"])
        for marker in ("C248–C256", "Z/K", "7, 13, 15"):
            self.assertIn(marker, rows["H-04"])
        for marker in ("C292–C303", "35-статейный", "02.04", "12.04.1571"):
            self.assertIn(marker, rows["H-08"])
        self.assertIn("статьи 38, 42 Цвингли", rows["T-02"])
        self.assertNotIn("``38,42", packet)
        self.assertIn("вне совершенства Христова", packet)
        self.assertIn("не** выполнена", packet)

    def test_nantes_two_editions_and_non_evidence_of_third(self):
        text = self.texts["episode11_france_catholic_reform_nantes_1545_1599_manuscript.md"]
        for key in ("95 общих статей", "92 статей", "93",
                    "Ms fr. 413", "25 февраля 1599",
                    "ARTICLE_COUNT_ORIGINAL_COLLATION_HOLD",
                    "CATALOG_ONLY", "56 особых статей"):
            with self.subTest(key=key):
                self.assertIn(key.lower(), text.lower())
        self.assertIn("не** считать это доказанным третьим текстовым состоянием", text)

    def test_draft_not_misrepresented_as_independently_approved(self):
        for name, s in self.texts.items():
            with self.subTest(name=name):
                for key in ("RESEARCH_MANUSCRIPT_DRAFT", "NOT_EDITORIAL_READY",
                            "PUBLICATION_HOLD"):
                    self.assertIn(key, s)
        registry = json.loads(
            (HERE / "source-registry-v1.json").read_text(encoding="utf-8")
        )
        for item in registry["sources"]:
            with self.subTest(id=item["id"]):
                self.assertEqual(item["publicationState"], "REFERENCE")
                self.assertIn("PUBLICATION_HOLD", item["holds"])
        plan = (HERE / "SELF_PLAN.md").read_text(encoding="utf-8")
        for gate in ("RF-BOOK-FINAL-REVIEW", "INDEPENDENT_EXTERNAL_REVIEW_OPEN",
                     "THEOLOGICAL_PEER_REVIEW_OPEN", "ORIGINAL_PRINT_COLLATION_HOLD",
                     "RIGHTS_HOLD", "EDITORIAL_HANDOFF_HOLD", "STOP_DISCOVERY"):
            self.assertIn(gate, plan)
        readme = (HERE / "README.md").read_text(encoding="utf-8")
        blueprint = (HERE / "04_series_blueprint.md").read_text(encoding="utf-8")
        for name in PARTS:
            self.assertIn("](" + name + ")", readme)
            self.assertIn("](" + name + ")", blueprint)


if __name__ == "__main__":
    unittest.main()
