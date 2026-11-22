#!/usr/bin/env python3
"""Offline tests for scripts/audit_relative_links.py.

The audit is a locator check, so these tests fix its contract: a relative link
either resolves to bytes inside the checkout or it does not; archived copies of
root documents are explained rather than rewritten; quoted syntax inside code
fences and backticks is not a locator; and a justified exception never covers a
newly dead link.
"""
from __future__ import annotations

from contextlib import redirect_stderr, redirect_stdout
import io
import json
import tempfile
import unittest
from pathlib import Path

import audit_relative_links as arl


class Fixture:
    """A throwaway repository with a predictable link fabric."""

    def __init__(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        (self.root / "data").mkdir()
        (self.root / "docs").mkdir()

    def write(self, rel: str, text: str) -> Path:
        path = self.root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def scan(self, exceptions: dict | None = None) -> dict:
        return arl.scan(self.root, exceptions or {})

    def close(self) -> None:
        self._tmp.cleanup()


class ClassificationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.fx = Fixture()
        self.fx.write("docs/target.md", "# target\n")
        self.fx.write("docs/sub/deep.md", "# deep\n")

    def tearDown(self) -> None:
        self.fx.close()

    def _states(self, text: str) -> dict[str, str]:
        self.fx.write("docs/page.md", text)
        report = self.fx.scan()
        return {f["target"]: f["state"] for f in report["findings"]}

    def test_resolving_link_is_not_a_defect(self) -> None:
        report = self.fx.scan() if self.fx.write("docs/page.md", "[t](target.md)") else None
        self.assertEqual(report["totals"]["defects"], 0)
        self.assertEqual(report["totals"]["byState"]["resolves"], 1)

    def test_missing_link_is_reported_with_line_number(self) -> None:
        self.fx.write("docs/page.md", "line one\n\n[t](nope.md)\n")
        report = self.fx.scan()
        self.assertEqual(report["totals"]["defects"], 1)
        finding = report["findings"][0]
        self.assertEqual(finding["line"], 3)
        self.assertEqual(finding["reason"], "no such path")

    def test_escaping_link_is_outside(self) -> None:
        states = self._states("[x](../../etc/passwd)")
        self.assertEqual(states["../../etc/passwd"], "outside")

    def test_scheme_links_are_external(self) -> None:
        self.fx.write("docs/page.md", "[a](https://example.org/x) [b](mailto:x@y.z) [c](#anchor)")
        report = self.fx.scan()
        self.assertEqual(report["totals"]["byState"]["external"], 2)
        self.assertEqual(report["totals"]["defects"], 0)  # external/aside links never enter findings
        self.assertEqual(report["findings"], [])

    def test_in_page_anchor_is_checked_against_its_own_file(self) -> None:
        self.fx.write("docs/page.md", "# Top\n\n[a](#top) [b](#nowhere)\n")
        states = self.fx.scan()["totals"]["byState"]
        self.assertEqual((states["fragment"], states["missing-fragment"]), (1, 1))

    def test_dead_in_page_anchor_is_reported_but_not_a_defect(self) -> None:
        # The slug rules here are an approximation; gating on our own approximation would
        # turn a guess into a verdict, so a dead in-page anchor is reported by state only.
        self.fx.write("docs/page.md", "# Top\n\n[b](#nowhere)\n")
        report = self.fx.scan()
        self.assertEqual(report["totals"]["defects"], 0)
        self.assertEqual(report["totals"]["byState"]["missing-fragment"], 1)

    def test_fragment_census_counts_both_kinds(self) -> None:
        self.fx.write("docs/target.md", "# Head\n\n## Part\n")
        self.fx.write("docs/page.md", "# Top\n\n[a](#top) [b](target.md#part)\n")
        fragments = self.fx.scan()["totals"]["fragments"]
        self.assertEqual((fragments["total"], fragments["inPage"], fragments["crossFile"],
                          fragments["resolved"], fragments["unresolved"]), (2, 1, 1, 2, 0))

    def test_bare_host_is_unqualified(self) -> None:
        states = self._states("[pdf](www.example.org/report.pdf)")
        self.assertEqual(states["www.example.org/report.pdf"], "unqualified")
        self.assertEqual(self.fx.scan()["findings"][0]["reason"], "missing scheme")

    def test_percent_encoded_path_resolves(self) -> None:
        (self.fx.root / "docs" / "ТРУДНЫЕ ТЕКСТЫ").mkdir()
        (self.fx.root / "docs" / "ТРУДНЫЕ ТЕКСТЫ" / "a.md").write_text("x", encoding="utf-8")
        states = self._states("[t](%D0%A2%D0%A0%D0%A3%D0%94%D0%9D%D0%AB%D0%95%20%D0%A2%D0%95%D0%9A%D0%A1%D0%A2%D0%AB/a.md)")
        self.assertEqual(states, {})

    def test_archive_copy_reason_names_the_root(self) -> None:
        self.fx.write("target.md", "# root-level doc\n")
        self.fx.write("history/copy.md", "[t](target.md)")
        report = self.fx.scan()
        finding = report["findings"][0]
        self.assertEqual(finding["state"], "missing")
        self.assertIn("repository root", finding["reason"])


class QuotedSyntaxTests(unittest.TestCase):
    def setUp(self) -> None:
        self.fx = Fixture()
        self.fx.write("docs/page.md", "")

    def tearDown(self) -> None:
        self.fx.close()

    def test_fenced_block_is_not_a_locator(self) -> None:
        self.fx.write("docs/page.md", "```\n[a](missing.md)\n```\n")
        self.assertEqual(self.fx.scan()["totals"]["defects"], 0)

    def test_inline_code_is_not_a_locator(self) -> None:
        self.fx.write("docs/page.md", "В статьях markdown-ссылок `[…](…)` ноль, а `[x](gone.md)` — пример.\n")
        self.assertEqual(self.fx.scan()["totals"]["defects"], 0)

    def test_fence_does_not_hide_the_rest_of_the_file(self) -> None:
        self.fx.write("docs/page.md", "```\ncode\n```\n[real](gone.md)\n")
        report = self.fx.scan()
        self.assertEqual(report["totals"]["defects"], 1)
        self.assertEqual(report["findings"][0]["line"], 4)


class ExceptionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.fx = Fixture()
        self.fx.write("docs/page.md", "[a](gone.md)\n[b](also-gone.md)\n")

    def tearDown(self) -> None:
        self.fx.close()

    def test_unexplained_defect_blocks_strict(self) -> None:
        report = self.fx.scan()
        self.assertEqual(report["totals"]["unexplained"], 2)
        self.assertEqual(report["totals"]["explained"], 0)

    def test_exception_is_exact_pair_only(self) -> None:
        exc = {("docs/page.md", "gone.md"): "историческая запись"}
        report = self.fx.scan(exc)
        self.assertEqual(report["totals"]["explained"], 1)
        self.assertEqual(report["totals"]["unexplained"], 1)

    def test_exception_requires_reason(self) -> None:
        path = self.fx.root / "exc.json"
        path.write_text(json.dumps({"exceptions": [{"file": "docs/page.md", "target": "gone.md"}]}),
                        encoding="utf-8")
        with self.assertRaises(ValueError):
            arl.load_exceptions(path)

    def test_missing_exceptions_file_is_not_an_error(self) -> None:
        self.assertEqual(arl.load_exceptions(self.fx.root / "nope.json"), {})


class SectionAnchorTests(unittest.TestCase):
    """A ``#fragment`` must name a heading that exists in the target file.

    Section locators are the cheapest kind of citation to get wrong: the file
    stays put while the heading is reworded, and the link keeps looking alive.
    """

    def setUp(self) -> None:
        self.fx = Fixture()

    def tearDown(self) -> None:
        self.fx.close()

    def _state(self, target_text: str, link: str) -> str:
        target = self.fx.write("docs/target.md", target_text)
        page = self.fx.write("docs/page.md", f"[t]({link})\n")
        state, _reason = arl.classify(link, page, self.fx.root)
        return state

    def test_existing_heading_resolves(self) -> None:
        self.assertEqual(self._state("# Head\n\n## Part Two\n", "target.md#part-two"), "resolves")

    def test_absent_heading_is_a_defect(self) -> None:
        self.assertEqual(self._state("# Head\n\n## Part Two\n", "target.md#part-three"), "missing-anchor")

    def test_explicit_html_id_resolves(self) -> None:
        for anchor in ('<a id="reader-scope"></a>', "<a id='reader-scope'></a>",
                       '<a id=reader-scope></a>'):
            with self.subTest(anchor=anchor):
                self.assertEqual(self._state(anchor, "target.md#reader-scope"), "resolves")

    def test_legacy_named_anchor_resolves(self) -> None:
        self.assertEqual(self._state('<a name="old-scope"></a>',
                                     "target.md#old-scope"), "resolves")

    def test_id_on_another_html_element_resolves(self) -> None:
        self.assertEqual(self._state('<span id="scope">text</span>',
                                     "target.md#scope"), "resolves")

    def test_explicit_in_page_anchor_resolves(self) -> None:
        self.fx.write("docs/page.md", '<a id="scope"></a>\n[scope](#scope)\n')
        report = self.fx.scan()
        self.assertEqual(report["totals"]["byState"]["fragment"], 1)
        self.assertEqual(report["totals"]["byState"]["missing-fragment"], 0)

    def test_an_unrelated_html_id_does_not_hide_a_dead_locator(self) -> None:
        self.assertEqual(self._state('<a id="real"></a>',
                                     "target.md#not-real"), "missing-anchor")
        self.assertEqual(self._state('<span name="not-an-anchor">text</span>',
                                     "target.md#not-an-anchor"), "missing-anchor")

    def test_quoted_or_commented_html_is_not_an_anchor(self) -> None:
        for text in ('```html\n<a id="example"></a>\n```',
                     '~~~html\n<a id="example"></a>\n~~~',
                     '`<a id="example"></a>`',
                     '<!-- <a id="example"></a> -->',
                     '&lt;a id="example"&gt;&lt;/a&gt;'):
            with self.subTest(text=text):
                self.assertEqual(self._state(text, "target.md#example"), "missing-anchor")

    def test_fenced_heading_is_not_an_anchor(self) -> None:
        self.assertEqual(self._state('```md\n## Example\n```\n',
                                     "target.md#example"), "missing-anchor")

    def test_inline_code_words_still_belong_to_a_real_heading(self) -> None:
        self.assertEqual(self._state('## Reader `scope`\n',
                                     "target.md#reader-scope"), "resolves")

    def test_real_html_anchor_needs_no_exception_but_a_typo_still_blocks(self) -> None:
        self.fx.write("docs/target.md", '<a id="scope"></a>\n')
        self.fx.write("docs/page.md", '[yes](target.md#scope)\n[no](target.md#typo)\n')
        report = self.fx.scan()
        self.assertEqual(report["totals"]["byState"]["resolves"], 1)
        self.assertEqual(report["totals"]["unexplained"], 1)
        self.assertEqual(report["findings"][0]["target"], "target.md#typo")

    def test_dash_forms_do_not_change_the_heading(self) -> None:
        # GitHub renders an en dash as nothing, so 6\u20137 and 6-7 are one place.
        heading = "## 9. \u0425\u043e\u0434\u0436, \u0433\u043b. VII \u00a7\u00a76\u20137\n"
        self.assertEqual(
            self._state(heading, "target.md#9-\u0445\u043e\u0434\u0436-\u0433\u043b-vii-6-7"),
            "resolves",
        )

    def test_anchor_is_checked_case_insensitively(self) -> None:
        self.assertEqual(self._state("## Proof\n", "target.md#Proof"), "resolves")

    def test_fragment_on_a_missing_file_stays_missing(self) -> None:
        self.assertEqual(self._state("## Proof\n", "gone.md#proof"), "missing")

    def test_non_markdown_fragment_is_not_checked(self) -> None:
        (self.fx.root / "docs" / "data.json").write_text("{}", encoding="utf-8")
        self.assertEqual(self._state("## Proof\n", "data.json#anything"), "resolves")

    def test_line_anchor_is_left_alone(self) -> None:
        self.assertEqual(self._state("## Proof\n", "target.md#L12"), "resolves")

    def test_missing_anchor_counts_as_a_defect(self) -> None:
        self.fx.write("docs/target.md", "## Part Two\n")
        self.fx.write("docs/page.md", "[t](target.md#part-three)\n")
        report = self.fx.scan()
        self.assertEqual(report["totals"]["byState"]["missing-anchor"], 1)
        self.assertEqual(report["totals"]["defects"], 1)

    def test_slug_uses_visible_words_of_a_heading(self) -> None:
        self.assertEqual(
            arl.normalise_anchor(arl.slugify("See [`x`](x.md) now")), "see-now"
        )


class LineAnchorTests(unittest.TestCase):
    """Only complete GitHub line tokens may bypass the heading lookup."""

    def setUp(self) -> None:
        self.fx = Fixture()
        self.fx.write("docs/target.md", "## Proof\n")
        self.page = self.fx.write("docs/page.md", "")

    def tearDown(self) -> None:
        self.fx.close()

    def state(self, link: str) -> str:
        return arl.classify(link, self.page, self.fx.root)[0]

    def strict(self, link: str) -> tuple[int, str, str]:
        self.fx.write("docs/page.md", f"[t]({link})\n")
        before = {p.relative_to(self.fx.root): (p.read_bytes(), p.stat().st_mtime_ns,
                                               p.stat().st_mode)
                  for p in self.fx.root.rglob("*") if p.is_file()}
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = arl.main(["--root", str(self.fx.root), "--strict"])
        after = {p.relative_to(self.fx.root): (p.read_bytes(), p.stat().st_mtime_ns,
                                              p.stat().st_mode)
                 for p in self.fx.root.rglob("*") if p.is_file()}
        self.assertEqual(before, after, "the audit must not repair or rewrite a locator")
        return code, out.getvalue(), err.getvalue()

    def test_line_prefix_alone_does_not_exempt_a_missing_heading(self) -> None:
        for fragment in ("L", "LostAnchor", "L12suffix", "L12-typo", "L0", "L01",
                         "L1-L", "L1-L0", "L1-L02", "L1-L2-extra", "L１", "L1-L٢"):
            with self.subTest(fragment=fragment):
                self.assertEqual(self.state(f"target.md#{fragment}"), "missing-anchor")

    def test_complete_ascii_line_tokens_and_url_encoding_keep_the_allowance(self) -> None:
        for fragment in ("L1", "L12", "L12-L34", "%4C12%2D%4C34"):
            with self.subTest(fragment=fragment):
                state, reason = arl.classify(f"target.md#{fragment}", self.page, self.fx.root)
                self.assertEqual(state, "resolves")
                self.assertIn("line bounds not checked", reason)

    def test_real_L_named_heading_or_html_anchor_still_resolves(self) -> None:
        for text, fragment in (("## Library\n", "Library"),
                               ('<a id="L12suffix"></a>\n', "L12suffix")):
            with self.subTest(fragment=fragment):
                self.fx.write("docs/target.md", text)
                self.assertEqual(self.state(f"target.md#{fragment}"), "resolves")

    def test_line_typo_is_counted_as_a_defect_and_unresolved_fragment(self) -> None:
        self.fx.write("docs/page.md", "[yes](target.md#L12)\n[no](target.md#L12suffix)\n")
        report = self.fx.scan()
        self.assertEqual(report["totals"]["byState"]["resolves"], 1)
        self.assertEqual(report["totals"]["byState"]["missing-anchor"], 1)
        self.assertEqual(report["totals"]["unexplained"], 1)
        self.assertEqual(report["totals"]["fragments"]["unresolved"], 1)
        self.assertEqual(report["findings"][0]["line"], 2)

    def test_an_exception_for_another_target_cannot_waive_a_line_typo(self) -> None:
        self.fx.write("docs/page.md", "[no](target.md#LostAnchor)\n")
        report = self.fx.scan({("docs/page.md", "target.md#L12"): "unrelated target"})
        self.assertEqual(report["totals"]["explained"], 0)
        self.assertEqual(report["totals"]["unexplained"], 1)
        self.assertEqual(report["findings"][0]["target"], "target.md#LostAnchor")

    def test_strict_cli_rejects_unknown_L_fragment_without_writes(self) -> None:
        code, out, err = self.strict("target.md#LostAnchor")
        self.assertEqual(code, 1)
        self.assertIn("missing-anchor=1", out)
        self.assertIn("1 unexplained dead locators", err)

    def test_strict_cli_accepts_supported_line_syntax_without_writes(self) -> None:
        code, out, err = self.strict("target.md#L12-L34")
        self.assertEqual(code, 0)
        self.assertIn("resolves=1", out)
        self.assertEqual(err, "")

    def test_valid_line_token_does_not_hide_a_missing_file(self) -> None:
        self.assertEqual(self.state("gone.md#L12"), "missing")

    def test_valid_line_token_does_not_hide_an_escape_from_the_repository(self) -> None:
        self.assertEqual(self.state("../../outside.md#L12"), "outside")


class FencedBlockTests(unittest.TestCase):
    """Top-level fences cannot manufacture anchors or hide later real links."""

    def setUp(self) -> None:
        self.fx = Fixture()

    def tearDown(self) -> None:
        self.fx.close()

    def findings(self, text: str) -> list[tuple[int, str]]:
        self.fx.write("docs/page.md", text)
        return [(row["line"], row["target"]) for row in self.fx.scan()["findings"]]

    def test_shorter_backticks_do_not_manufacture_a_heading(self) -> None:
        target = self.fx.write("docs/target.md",
                               "````markdown\n```\n## Ghost\n```\n````\n## Reader `scope`\n")
        page = self.fx.write("docs/page.md", "")
        self.assertEqual(arl.anchors_of(target), {"reader-scope"})
        self.assertEqual(arl.classify("target.md#ghost", page, self.fx.root)[0], "missing-anchor")
        self.assertEqual(arl.classify("target.md#reader-scope", page, self.fx.root)[0], "resolves")

    def test_other_marker_neither_exposes_example_nor_hides_real_link(self) -> None:
        for marker, other in (("```", "~~~"), ("~~~", "```")):
            with self.subTest(marker=marker):
                text = f"{marker}text\n{other}\n[example](not-real.md)\n{marker}\n[real](gone.md)\n"
                self.assertEqual(self.findings(text), [(5, "gone.md")])

    def test_closing_marker_with_text_is_still_code(self) -> None:
        for marker in ("```", "~~~"):
            for tail in (" text", "\u00a0", " `not whitespace`"):
                with self.subTest(marker=marker, tail=tail):
                    text = f"{marker}\n{marker}{tail}\n[example](not-real.md)\n{marker}\n[real](gone.md)\n"
                    self.assertEqual(self.findings(text), [(5, "gone.md")])

    def test_closer_must_match_or_exceed_opening_length(self) -> None:
        for marker in ("`", "~"):
            for width in (3, 4, 5):
                for indent in ("", " ", "  ", "   "):
                    with self.subTest(marker=marker, width=width, indent=indent):
                        text = (f"{indent}{marker * width}text\n{marker * (width - 1)}\n"
                                f"[example](not-real.md)\n{indent}{marker * (width + 1)} \t\n"
                                "[real](gone.md)\n")
                        self.assertEqual(self.findings(text), [(5, "gone.md")])

    def test_backtick_info_string_cannot_contain_a_backtick(self) -> None:
        for opener in ("```lang `invalid", "````lang ```", "```lang```"):
            with self.subTest(opener=opener):
                self.assertEqual(self.findings(opener + "\n[real](gone.md)\n"), [(2, "gone.md")])

    def test_tilde_info_string_can_contain_backticks(self) -> None:
        text = "~~~lang `allowed`\n[example](not-real.md)\n~~~\n[real](gone.md)\n"
        self.assertEqual(self.findings(text), [(4, "gone.md")])

    def test_tab_or_nonspace_prefix_does_not_open_a_top_level_fence(self) -> None:
        for prefix in ("\t", " \t", "\u00a0", "    "):
            with self.subTest(prefix=prefix):
                self.assertEqual(self.findings(prefix + "```text\n[real](gone.md)\n"),
                                 [(2, "gone.md")])

    def test_unterminated_fence_hides_examples_through_end_of_file(self) -> None:
        for opener, not_closer in (("````text", "```"), ("```text", "~~~"),
                                   ("~~~~text", "~~~"), ("~~~text", "```")):
            with self.subTest(opener=opener, not_closer=not_closer):
                text = f"# Real\n{opener}\n{not_closer}\n## Ghost\n[example](gone.md)\n"
                target = self.fx.write("docs/target.md", text)
                self.fx.write("docs/page.md", "")
                self.assertEqual(arl.anchors_of(target), {"real"})
                self.assertEqual(self.fx.scan()["findings"], [])

    def test_shorter_fence_cannot_manufacture_an_html_anchor(self) -> None:
        target = self.fx.write("docs/target.md",
                               '````html\n```\n<a id="ghost"></a>\n```\n````\n<a id="real"></a>\n')
        page = self.fx.write("docs/page.md", "")
        self.assertEqual(arl.anchors_of(target), {"real"})
        self.assertEqual(arl.classify("target.md#ghost", page, self.fx.root)[0], "missing-anchor")
        self.assertEqual(arl.classify("target.md#real", page, self.fx.root)[0], "resolves")

    def test_strict_cli_rejects_quoted_heading_without_writes(self) -> None:
        self.fx.write("docs/target.md", "````md\n```\n## Ghost\n```\n````\n")
        self.fx.write("docs/page.md", "[reader](target.md#ghost)\n")
        before = {p.relative_to(self.fx.root): (p.read_bytes(), p.stat().st_mode,
                                               p.stat().st_mtime_ns)
                  for p in self.fx.root.rglob("*") if p.is_file()}
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = arl.main(["--root", str(self.fx.root), "--strict", "--summary"])
        after = {p.relative_to(self.fx.root): (p.read_bytes(), p.stat().st_mode,
                                              p.stat().st_mtime_ns)
                 for p in self.fx.root.rglob("*") if p.is_file()}
        self.assertEqual(before, after)
        self.assertEqual(code, 1)
        self.assertIn("missing-anchor=1", out.getvalue())
        self.assertIn("1 unexplained dead locators", err.getvalue())


class InterfaceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.fx = Fixture()
        self.fx.write("docs/page.md", "[a](gone.md)\n")

    def tearDown(self) -> None:
        self.fx.close()

    def test_scan_is_read_only(self) -> None:
        before = sorted(p.name for p in self.fx.root.rglob("*"))
        self.fx.scan()
        self.assertEqual(before, sorted(p.name for p in self.fx.root.rglob("*")))

    def test_json_inventory_round_trips(self) -> None:
        report = self.fx.scan()
        payload = json.loads(json.dumps(report, ensure_ascii=False))
        self.assertEqual(payload["schemaVersion"], arl.SCHEMA_VERSION)
        self.assertEqual(payload["authorityId"], arl.AUTHORITY_ID)
        self.assertIn("byState", payload["totals"])

    def test_strict_exit_code(self) -> None:
        out = self.fx.root / "out.json"
        code = arl.main(["--root", str(self.fx.root), "-o", str(out), "--strict"])
        self.assertEqual(code, 1)
        self.assertTrue(out.is_file())

    def test_strict_passes_when_everything_is_explained(self) -> None:
        exc = self.fx.root / "exc.json"
        exc.write_text(json.dumps({"exceptions": [
            {"file": "docs/page.md", "target": "gone.md", "reason": "test reason"}]}), encoding="utf-8")
        code = arl.main(["--root", str(self.fx.root), "--exceptions", str(exc), "--strict"])
        self.assertEqual(code, 0)


if __name__ == "__main__":
    unittest.main()
