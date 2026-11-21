#!/usr/bin/env python3
"""Offline tests for scripts/audit_ci_triggers.py.

The checker is about one sentence: the workflow's ``paths:`` list is a claim about what
the gates read. These tests keep that sentence falsifiable - a duplicated entry, two
lists that disagree, a script that runs without being a trigger, an input that is read
through an artefact, and a workflow whose shape cannot be parsed at all.
"""
from __future__ import annotations

import ast
import tempfile
import unittest
from pathlib import Path

import audit_ci_triggers as act

WORKFLOW = """\
name: Holds inventory (read-only)

on:
  pull_request:
    paths:
      - 'scripts/gate.py'
      - 'data/input.json'
  push:
    branches: [main]
    paths:
      - 'scripts/gate.py'
      - 'data/input.json'
  workflow_dispatch:

permissions:
  contents: read

jobs:
  inventory:
    runs-on: ubuntu-24.04
    steps:
      - name: Run the gate
        run: python3 -B scripts/gate.py --check
"""

GATE = """\
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data" / "input.json"
"""


class Fixture:
    def __init__(self) -> None:
        self._dir = tempfile.TemporaryDirectory()
        self.root = Path(self._dir.name)
        (self.root / "scripts").mkdir()
        (self.root / "data").mkdir()
        (self.root / "scripts" / "gate.py").write_text(GATE, encoding="utf-8")
        (self.root / "data" / "input.json").write_text("{}\n", encoding="utf-8")

    def close(self) -> None:
        self._dir.cleanup()

    def workflow(self, text: str = WORKFLOW) -> str:
        return text


class TriggerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.fx = Fixture()

    def tearDown(self) -> None:
        self.fx.close()

    def test_clean_workflow_passes(self) -> None:
        self.assertEqual(act.check(self.fx.workflow(), root=self.fx.root, declared={}), [])

    def test_duplicate_entry_is_reported(self) -> None:
        text = self.fx.workflow().replace(
            "      - 'data/input.json'\n  push:",
            "      - 'data/input.json'\n      - 'data/input.json'\n  push:")
        problems = act.check(text, root=self.fx.root, declared={})
        self.assertTrue(any("duplicate trigger path" in p for p in problems), problems)

    def test_asymmetric_lists_are_reported(self) -> None:
        text = self.fx.workflow().replace(
            "  push:\n    branches: [main]\n    paths:\n      - 'scripts/gate.py'\n      - 'data/input.json'",
            "  push:\n    branches: [main]\n    paths:\n      - 'scripts/gate.py'")
        problems = act.check(text, root=self.fx.root, declared={})
        self.assertTrue(any("listed for pull_request but not for push" in p for p in problems), problems)

    def test_untriggered_script_is_reported(self) -> None:
        (self.fx.root / "scripts" / "extra.py").write_text("print('x')\n", encoding="utf-8")
        text = self.fx.workflow().replace(
            "run: python3 -B scripts/gate.py --check",
            "run: python3 -B scripts/gate.py --check && python3 -B scripts/extra.py")
        problems = act.check(text, root=self.fx.root, declared={})
        self.assertTrue(any("scripts/extra.py" in p and "not a trigger path" in p for p in problems), problems)

    def test_input_read_by_a_script_is_required(self) -> None:
        (self.fx.root / "data" / "hidden.json").write_text("{}\n", encoding="utf-8")
        gate = (self.fx.root / "scripts" / "gate.py")
        gate.write_text(GATE + 'HIDDEN = ROOT / "data" / "hidden.json"\n', encoding="utf-8")
        problems = act.check(self.fx.workflow(), root=self.fx.root, declared={})
        self.assertTrue(any("data/hidden.json" in p for p in problems), problems)

    def test_missing_trigger_path_is_reported(self) -> None:
        text = self.fx.workflow().replace("      - 'data/input.json'", "      - 'data/absent.json'")
        problems = act.check(text, root=self.fx.root, declared={})
        self.assertTrue(any("does not exist in pull_request" in p for p in problems), problems)

    def test_shape_errors_fail_loudly(self) -> None:
        with self.assertRaises(act.WorkflowError):
            act.trigger_lists("on:\n  push:\n    paths:\n      - 'a'\n")
        with self.assertRaises(act.WorkflowError):
            act.trigger_lists("on:\n  pull_request:\n    branches: [main]\n")
        with self.assertRaises(act.WorkflowError):
            act.check("on:\n  pull_request:\n    paths:\n      - 'x'\n  push:\n    paths:\n      - 'x'\n",
                      root=self.fx.root, declared={})

    def test_declared_inputs_are_checked_against_reality(self) -> None:
        for artefact, inputs in act.DECLARED_INPUTS.items():
            with self.subTest(artefact):
                self.assertTrue(inputs, "a declared input without paths proves nothing")
                for path, reason in inputs:
                    self.assertIn(path, act.trigger_lists(
                        Path(act.WORKFLOW).read_text(encoding="utf-8"))["pull_request"],
                        f"{path} is declared ({reason}) but not a trigger")


class TestModuleLayoutTests(unittest.TestCase):
    """A direct invocation must discover the same classes as unittest discovery."""

    def test_main_guard_is_unique_and_last_when_present(self) -> None:
        scripts = Path(__file__).resolve().parent
        for path in sorted(scripts.glob("test_*.py")):
            module = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            guards = [node for node in module.body if isinstance(node, ast.If)
                      and isinstance(node.test, ast.Compare)
                      and isinstance(node.test.left, ast.Name)
                      and node.test.left.id == "__name__"]
            with self.subTest(path.name):
                self.assertLessEqual(len(guards), 1, "duplicate __main__ guards")
                if guards:
                    self.assertIs(module.body[-1], guards[0],
                                  "classes below unittest.main() do not run on direct invocation")


if __name__ == "__main__":
    unittest.main()
