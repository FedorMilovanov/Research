#!/usr/bin/env python3
"""Offline tests for scripts/audit_relative_links.py.

The audit is a locator check, so these tests fix its contract: a relative link
either resolves to bytes inside the checkout or it does not; archived copies of
root documents are explained rather than rewritten; quoted syntax inside code
fences and backticks is not a locator; and a justified exception never covers a
newly dead link.
"""
from __future__ import annotations

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


class CommittedReportTests(unittest.TestCase):
    """The committed report is what §8's table is generated from, so it has to describe this tree.

    Its freshness was checked in CI only - a ``cmp`` between a fresh run and the committed file.
    That step caught a stale report in the §32 commit while the whole local suite was green:
    two recordLocations of the new closure added two resolvable locators, the report still said
    2 885, and nothing here compared the two. A check that exists only in the workflow is not a
    check the author runs.
    """

    def test_committed_report_matches_a_fresh_run(self) -> None:
        root = Path(__file__).resolve().parents[1]
        report = root / "data" / "relative-links-audit-2026-11-18.json"
        exceptions = arl.load_exceptions(root / "data" / "relative-link-exceptions-v1.json")
        fresh = arl.scan(root, exceptions)
        self.assertEqual(json.loads(report.read_text(encoding="utf-8")), fresh,
                         "data/relative-links-audit-2026-11-18.json no longer describes this tree; "
                         "re-run the audit to -o and regenerate §8")
if __name__ == "__main__":
    unittest.main()
