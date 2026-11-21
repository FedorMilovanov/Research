"""Regression tests for the read-only Markdown operational-state audit."""

import contextlib
import io
from pathlib import Path
import tempfile
import unittest
from unittest import mock

import audit_registry_consistency as audit


class MirrorStatesTests(unittest.TestCase):
    def problems(self, record, text, fields=("claimStatus",)):
        problems = []
        audit.check_mirror_states([record], text, fields, problems)
        return problems

    def test_id_mention_does_not_count_as_a_card(self):
        record = {"id": "CLM-A", "claimStatus": "RESEARCH_OPEN"}
        self.assertTrue(self.problems(record, "See CLM-A in another dossier."))

    def test_id_prefix_does_not_count_as_a_card(self):
        record = {"id": "CLM-A", "claimStatus": "RESEARCH_OPEN"}
        self.assertTrue(self.problems(record, "## CLM-A-LONGER\n**Review state:** RESEARCH_OPEN\n"))

    def test_missing_holds_fail_even_if_named_in_prose(self):
        record = {"id": "CLM-A", "claimStatus": "RESEARCH_OPEN", "holds": ["ARCHIVE_HOLD"]}
        text = "## CLM-A\n**Review state:** RESEARCH_OPEN\n**Limits:** Keep ARCHIVE_HOLD.\n"
        self.assertTrue(self.problems(record, text))

    def test_another_card_cannot_supply_a_missing_hold(self):
        record = {"id": "CLM-A", "claimStatus": "RESEARCH_OPEN", "holds": ["ARCHIVE_HOLD"]}
        text = ("## CLM-A\n**Review state:** RESEARCH_OPEN\n"
                "## CLM-B\n**Holds:** ARCHIVE_HOLD\n")
        self.assertTrue(self.problems(record, text))

    def test_unrelated_heading_ends_the_card(self):
        record = {"id": "CLM-A", "claimStatus": "RESEARCH_OPEN", "holds": ["ARCHIVE_HOLD"]}
        text = ("## CLM-A\n**Review state:** RESEARCH_OPEN\n"
                "## Commentary\n**Holds:** ARCHIVE_HOLD\n")
        self.assertTrue(self.problems(record, text))

    def test_bold_code_and_compact_fields(self):
        record = {"id": "CLM-A", "claimStatus": "RESEARCH_OPEN", "holds": ["ARCHIVE_HOLD"]}
        for state in ("RESEARCH_OPEN", "**RESEARCH_OPEN**", "`RESEARCH_OPEN`"):
            for extra in ("", "**Sources:** SRC-A · **Level:** series · "):
                with self.subTest(state=state, extra=extra):
                    text = f"### CLM-A — title\n**Review state:** {state} · {extra}**HOLDs:** ARCHIVE_HOLD.\n"
                    self.assertEqual([], self.problems(record, text))

    def test_plain_historical_review_and_holds_on_one_line(self):
        record = {"id": "CLM-A", "claimStatus": "EVIDENCE_HOLD", "holds": ["EVIDENCE_HOLD"]}
        text = "### CLM-A\nReview state: **EVIDENCE_HOLD**. HOLDs: EVIDENCE_HOLD.\n"
        self.assertEqual([], self.problems(record, text))

    def test_note_only_revision_inherits_operational_fields(self):
        record = {"id": "CLM-A", "claimStatus": "RESEARCH_OPEN", "holds": ["RIGHTS_HOLD"]}
        text = ("## CLM-A\n**Review state:** RESEARCH_OPEN\n**HOLDs:** RIGHTS_HOLD\n"
                "### Revised: CLM-A\n**Added note:** No new acquisition.\n")
        self.assertEqual([], self.problems(record, text))

    def test_revision_replaces_only_explicit_fields(self):
        record = {"id": "CLM-A", "claimStatus": "RESEARCH_OPEN", "holds": ["RIGHTS_HOLD"]}
        text = ("## CLM-A\n**Review state:** EVIDENCE_HOLD\n**HOLDs:** RIGHTS_HOLD\n"
                "### Revised: CLM-A\n**Review state:** RESEARCH_OPEN\n")
        self.assertEqual([], self.problems(record, text))

    def test_explicit_empty_holds_override_an_old_declaration(self):
        record = {"id": "CLM-A", "claimStatus": "RESEARCH_OPEN", "holds": ["RIGHTS_HOLD"]}
        text = ("## CLM-A\n**Review state:** RESEARCH_OPEN\n**HOLDs:** RIGHTS_HOLD\n"
                "### Revised: CLM-A\n**HOLDs:** none\n")
        self.assertTrue(self.problems(record, text))

    def test_extra_hold_and_wrong_status_fail(self):
        record = {"id": "CLM-A", "claimStatus": "RESEARCH_OPEN"}
        text = "## CLM-A\n**Review state:** VERIFIED_NEGATIVE\n**Holds:** EVIDENCE_HOLD\n"
        self.assertEqual(2, len(self.problems(record, text)))

    def test_absent_hold_declaration_is_allowed_only_for_an_empty_set(self):
        record = {"id": "CLM-A", "claimStatus": "RESEARCH_OPEN"}
        self.assertEqual([], self.problems(record, "## CLM-A\n**Review state:** RESEARCH_OPEN\n"))

    def test_source_state_axes_in_both_formats(self):
        record = {"id": "SRC-A", "evidenceClass": "D", "accessState": "NOT_ACQUIRED",
                  "locatorState": "LOCATOR_MISSING", "rightsState": "RIGHTS_UNKNOWN",
                  "publicationState": "BLOCKED", "holds": ["RIGHTS_HOLD"]}
        for compact in (False, True):
            with self.subTest(compact=compact):
                labels = ["Evidence class", "Access", "Locator", "Rights", "Publication", "HOLDs"]
                if not compact:
                    labels[1:5] = [label + " state" for label in labels[1:5]]
                values = ["**D**", "NOT_ACQUIRED", "LOCATOR_MISSING", "RIGHTS_UNKNOWN", "BLOCKED", "RIGHTS_HOLD"]
                lines = [f"{label}: {value}" for label, value in zip(labels, values)]
                body = "- " + (" · " if compact else "\n- ").join(lines)
                text = "## SRC-A\n" + body + "\n"
                self.assertEqual([], self.problems(record, text, audit.SOURCE_STATES))
                for value in values[:5]:
                    with self.subTest(value=value):
                        self.assertTrue(self.problems(record, text.replace(value, "WRONG"), audit.SOURCE_STATES))

    def test_fenced_examples_do_not_supply_a_card(self):
        record = {"id": "CLM-A", "claimStatus": "RESEARCH_OPEN"}
        for marker in ("```", "````", "~~~"):
            with self.subTest(marker=marker):
                text = f"{marker}markdown\n## CLM-A\n**Review state:** RESEARCH_OPEN\n{marker}\n"
                self.assertTrue(self.problems(record, text))

    def test_fenced_example_does_not_override_or_truncate_a_real_card(self):
        record = {"id": "CLM-A", "claimStatus": "RESEARCH_OPEN", "holds": ["RIGHTS_HOLD"]}
        text = ("## CLM-A\n**Review state:** RESEARCH_OPEN\n"
                "````markdown\n### Revised: CLM-A\n**Review state:** VERIFIED_NEGATIVE\n"
                "```\n**HOLDs:** ARCHIVE_HOLD\n````\n**HOLDs:** RIGHTS_HOLD\n")
        self.assertEqual([], self.problems(record, text))

    def test_commented_out_card_and_fields_are_ignored(self):
        record = {"id": "CLM-A", "claimStatus": "RESEARCH_OPEN", "holds": ["RIGHTS_HOLD"]}
        hidden = "<!--\n## CLM-A\n**Review state:** RESEARCH_OPEN\n**HOLDs:** RIGHTS_HOLD\n-->\n"
        self.assertTrue(self.problems(record, hidden))
        text = ("## CLM-A\n**Review state:** RESEARCH_OPEN\n**HOLDs:** RIGHTS_HOLD\n"
                "<!--\n### Revised: CLM-A\n**HOLDs:** ARCHIVE_HOLD\n-->\n")
        self.assertEqual([], self.problems(record, text))
        text = ("## CLM-A\n**Review state:** RESEARCH_OPEN <!-- old label -->\n"
                "<!--\n```markdown\n### Revised: CLM-A\n-->\n**HOLDs:** RIGHTS_HOLD\n")
        self.assertEqual([], self.problems(record, text))

    def test_state_requires_a_complete_token_not_a_valid_prefix(self):
        record = {"id": "CLM-A", "claimStatus": "RESEARCH_OPEN"}
        for value in ("RESEARCH_OPENtypo", "RESEARCH_OPEN / VERIFIED_NEGATIVE",
                      "RESEARCH_OPEN, VERIFIED_NEGATIVE"):
            with self.subTest(value=value):
                self.assertTrue(self.problems(record, f"## CLM-A\n**Review state:** {value}\n"))

    def test_existing_parenthetical_and_dash_annotations_are_allowed(self):
        record = {"id": "CLM-A", "claimStatus": "RESEARCH_OPEN"}
        for suffix in (" (projectLevel: true — method fact)", " — scope note", ".", ";"):
            with self.subTest(suffix=suffix):
                text = f"## CLM-A\n**Review state:** RESEARCH_OPEN{suffix}\n"
                self.assertEqual([], self.problems(record, text))

    def test_invalid_hold_declaration_is_not_an_empty_set(self):
        record = {"id": "CLM-A", "claimStatus": "RESEARCH_OPEN"}
        for value in ("typo", "rights_hold", "none / ARCHIVE_HOLD", ".", "none..."):
            with self.subTest(value=value):
                text = f"## CLM-A\n**Review state:** RESEARCH_OPEN\n**HOLDs:** {value}\n"
                self.assertTrue(self.problems(record, text))

    def test_existing_explicit_empty_hold_markers_are_allowed(self):
        record = {"id": "CLM-A", "claimStatus": "RESEARCH_OPEN"}
        for value in ("", "none", "None recorded.", "нет", "—"):
            with self.subTest(value=value):
                text = f"## CLM-A\n**Review state:** RESEARCH_OPEN\n**HOLDs:** {value}\n"
                self.assertEqual([], self.problems(record, text))

    def test_prose_suffix_cannot_supply_a_hold_declaration(self):
        record = {"id": "CLM-A", "claimStatus": "RESEARCH_OPEN", "holds": ["ARCHIVE_HOLD"]}
        for separator in (". ", " · "):
            with self.subTest(separator=separator):
                text = ("## CLM-A\n**Review state:** RESEARCH_OPEN\n"
                        f"**Limits:** Historical example{separator}HOLDs: ARCHIVE_HOLD.\n")
                self.assertTrue(self.problems(record, text))

    def test_label_quoted_in_a_note_cannot_clear_a_current_hold(self):
        record = {"id": "CLM-A", "claimStatus": "RESEARCH_OPEN", "holds": ["RIGHTS_HOLD"]}
        for separator in (". ", " · "):
            with self.subTest(separator=separator):
                text = ("## CLM-A\n**Review state:** RESEARCH_OPEN\n**HOLDs:** RIGHTS_HOLD\n"
                        f"### Revised: CLM-A\n**Notes:** Old example{separator}HOLDs: none\n")
                self.assertEqual([], self.problems(record, text))

    def test_compact_separator_does_not_discard_an_invalid_suffix(self):
        record = {"id": "CLM-A", "claimStatus": "RESEARCH_OPEN", "holds": ["RIGHTS_HOLD"]}
        for state, holds in (("RESEARCH_OPEN · VERIFIED_NEGATIVE", "RIGHTS_HOLD"),
                             ("RESEARCH_OPEN", "RIGHTS_HOLD · typo")):
            with self.subTest(state=state, holds=holds):
                text = f"## CLM-A\n**Review state:** {state}\n**HOLDs:** {holds}\n"
                self.assertTrue(self.problems(record, text))

    def test_empty_source_holds_cannot_consume_the_next_line(self):
        parsed = audit.mirror_states("## SRC-A\n- HOLDs: \n- Supports: Keep RIGHTS_HOLD in other cases.\n")
        self.assertEqual(set(), parsed["SRC-A"]["holds"])


class AuditOutputTests(unittest.TestCase):
    def test_document_count_does_not_double_count_overlapping_scans(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            research = root / "SUNO_HYMNS" / "RESEARCH"
            suno = root / "SUNO_HYMNS" / "SUNO"
            research.mkdir(parents=True)
            suno.mkdir()
            for path in (research / "a.md", suno / "b.md", root / "SUNO_HYMNS" / "README.md"):
                path.write_text("# Test\n", encoding="utf-8")
            output = io.StringIO()
            with mock.patch.multiple(audit, ROOT=root, RESEARCH=research, SUNO=suno,
                                     SRC_MD=research / "SOURCE_REGISTER.md",
                                     CLM_MD=research / "CLAIM_LEDGER.md"), \
                    mock.patch.object(audit, "load", return_value=[]), \
                    contextlib.redirect_stdout(output):
                self.assertEqual(0, audit.main())
            self.assertIn("документов проверено: 3\n", output.getvalue())


if __name__ == "__main__":
    unittest.main()
