#!/usr/bin/env python3
"""Offline integrity tests for data/hold-closure-registry-v1.json.

The registry is the only place where a HOLD may be called closed, so its own
bookkeeping has to be checkable: every confirmation must name records that
exist, every record it names must be in the checkout, and every confirmation
must be visible in the human-readable register. A confirmation nobody can find
is indistinguishable from an invented one.
"""
from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data" / "hold-closure-registry-v1.json"
REGISTER = ROOT / "docs" / "research" / "HOLDS_REGISTER_2026-11-18.md"


class RegistryShapeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = json.loads(REGISTRY.read_text(encoding="utf-8"))

    def test_ids_are_unique_and_prefixed(self) -> None:
        ids = [c["id"] for c in self.data["confirmations"]]
        self.assertEqual(len(ids), len(set(ids)))
        for one in ids:
            self.assertTrue(one.startswith("HCR-"), one)

    def test_every_confirmation_states_what_it_does_not_close(self) -> None:
        for entry in self.data["confirmations"]:
            with self.subTest(entry["id"]):
                self.assertEqual(entry["status"], "CONFIRMATION_NOT_CLOSURE")
                self.assertTrue(entry.get("limits"), "a confirmation needs its limits written down")

    def test_record_locations_exist(self) -> None:
        for entry in self.data["confirmations"]:
            for record in entry.get("recordLocations", []):
                path = record.split(" ")[0].split("§")[0].strip()
                if not path or path.startswith("HCR-"):
                    continue
                with self.subTest(entry["id"], record=record):
                    self.assertTrue((ROOT / path).exists(), f"{entry['id']}: missing {path}")

    def test_verification_names_a_repeatable_route(self) -> None:
        # A check that cannot be repeated is a claim. The route may be a local
        # script or an external connector, but it has to be named.
        for entry in self.data["confirmations"]:
            verification = entry.get("verification")
            if not isinstance(verification, dict):
                continue
            text = verification.get("command", "") + verification.get("tests", "")
            with self.subTest(entry["id"]):
                self.assertTrue(
                    "python3" in text or "соединитель" in text or "connector" in text,
                    f"{entry['id']}: verification names no repeatable route",
                )

    def test_external_route_declares_why_ci_cannot_run_it(self) -> None:
        for entry in self.data["confirmations"]:
            verification = entry.get("verification")
            if not isinstance(verification, dict):
                continue
            text = (verification.get("command", "") + verification.get("tests", "")).lower()
            if "python3" in text:
                continue
            with self.subTest(entry["id"]):
                self.assertTrue(
                    "ci" in text,
                    f"{entry['id']}: a non-script route must say what CI does with it",
                )

    def test_every_confirmation_is_visible_in_the_register(self) -> None:
        text = REGISTER.read_text(encoding="utf-8")
        for entry in self.data["confirmations"]:
            with self.subTest(entry["id"]):
                self.assertIn(entry["id"], text)


# Numbers that count the register itself, or a set that grows with every commit. They are
# printed live by the tools that own them; a copy inside a closure record is wrong the next
# time anything is added - which is exactly what happened (claims 46 -> 52, paths 49 -> 50).
SELF_COUNTS = {"closures", "confirmations", "openItems", "claims", "triggerPaths"}

# A standalone number (or ratio) in prose, but not a version, an algorithm or a section id.
MEASUREMENT = re.compile(r"(?<![\w§-])\d[\d\s\u2009]*(?![\w-])")


class ClosureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = json.loads(REGISTRY.read_text(encoding="utf-8"))

    def test_closures_carry_evidence(self) -> None:
        for entry in self.data.get("closures", []):
            with self.subTest(entry.get("id")):
                self.assertTrue(entry.get("evidence") or entry.get("recordLocations"),
                                "a closure without a locator is a claim")

    def test_open_items_have_stable_identity(self) -> None:
        ids = [entry.get("id") for entry in self.data.get("notClosed", [])]
        self.assertTrue(all(ids), "every open item needs an id, not a sentence")
        self.assertEqual(len(ids), len(set(ids)), "open item ids must be unique")

    def test_open_item_titles_carry_no_measurements(self) -> None:
        # A number inside a name is a counter with no field: nothing re-measures it, and
        # when it drifts the name silently lies. Measurements belong in checked prose.
        for entry in self.data.get("notClosed", []):
            with self.subTest(entry.get("id")):
                self.assertIsNone(re.search(r"\d", entry.get("title", "")),
                                  "open item title must not carry a number")

    def test_closures_do_not_quote_the_register_size(self) -> None:
        for entry in self.data.get("closures", []):
            for obj in entry.get("objects") or []:
                if not isinstance(obj, dict):
                    continue
                with self.subTest(entry.get("id")):
                    self.assertFalse(SELF_COUNTS & set(obj),
                                     f"self-count leaked into a closure record: {SELF_COUNTS & set(obj)}")

    def test_records_do_not_quote_the_suite_size(self) -> None:
        # previousState is exempt on purpose: it quotes what the earlier wording said, and
        # records 24 quotes "27 tests (they are 30)" as the evidence of the drift it closed.
        # Every other field states the present, where a copied total is a stale total.
        for entry in self.data.get("closures", []):
            for field in ("title", "closedScope", "method", "objects"):
                blob = json.dumps(entry.get(field), ensure_ascii=False)
                with self.subTest(f"{entry.get('id')} {field}"):
                    self.assertIsNone(re.search(r"\d+\s+(?:офлайн-)?тест", blob),
                                      "the suite prints its own size")

    def test_confirmation_titles_carry_no_measurements(self) -> None:
        # Same rule as the open items: a number inside a name has no field behind it.
        # Identifiers are not measurements: "v3", "SHA-256" and "§19" stay allowed, while
        # "17 объектов", "36/36" and "8 из 24" do not.
        for entry in self.data.get("confirmations", []):
            with self.subTest(entry.get("id")):
                self.assertIsNone(MEASUREMENT.search(entry.get("title", "")),
                                  "confirmation title must not carry a measurement")

    def test_confirmation_expectations_carry_no_measurements(self) -> None:
        # The registry's own verification.expect strings had drifted: they still quoted
        # resolves=2 856, external=5 974 and 27 tests after the artefacts moved on.
        for entry in self.data.get("confirmations", []):
            expect = (entry.get("verification") or {}).get("expect", "")
            with self.subTest(entry.get("id")):
                self.assertIsNone(MEASUREMENT.search(expect),
                                  "expectations must point at counters, not repeat measurements")

    def test_confirmation_counters_resolve(self) -> None:
        root = REGISTRY.parents[1] if REGISTRY.parent.name == "data" else REGISTRY.parent
        for entry in self.data.get("confirmations", []):
            for counter in entry.get("counters", []):
                with self.subTest(f"{entry.get('id')} {counter.get('label')}"):
                    path = root / counter["artefact"]
                    self.assertTrue(path.is_file(), f"missing artefact {counter['artefact']}")
                    node = json.loads(path.read_text(encoding="utf-8"))
                    for part in counter["field"].split("."):
                        node = node[part]
                    self.assertIsInstance(node, int)

    def test_not_closed_is_not_empty(self) -> None:
        # The registry must keep saying what stays blocked; an empty list would
        # read as "everything is closed", which no audit has established.
        self.assertTrue(self.data.get("notClosed"))



class HoldTypeDeclarationTests(unittest.TestCase):
    """A HOLD type the evidence policy does not know must be declared before it is used.

    Record 08 carried `TEXT_INTEGRITY_HOLD`, which no other file in the repository mentions:
    the register that documents non-canonical `holds` had invented one and printed it in §0
    among the flags from the policy. It is now declared in `localAxes` with a reason, and this
    test refuses both an undeclared type and a declaration that duplicates the policy.
    """

    @classmethod
    def setUpClass(cls) -> None:
        cls.data = json.loads(REGISTRY.read_text(encoding="utf-8"))
        policy = json.loads((ROOT / "data" / "repository-evidence-policy-v2.json").read_text(encoding="utf-8"))
        cls.canonical = {h for h in policy.get("holds", []) if isinstance(h, str)}
        cls.local = {axis.get("value") for axis in cls.data.get("localAxes", []) if isinstance(axis, dict)}

    def test_every_hold_type_is_known(self) -> None:
        for entry in self.data.get("closures", []) + self.data.get("confirmations", []):
            with self.subTest(entry.get("id")):
                self.assertIn(entry.get("holdType"), self.canonical | self.local,
                              "a HOLD type must be declared by the policy or by localAxes")

    def test_local_axes_state_a_reason(self) -> None:
        for axis in self.data.get("localAxes", []):
            with self.subTest(axis.get("value")):
                self.assertTrue(axis.get("value"))
                self.assertGreater(len(axis.get("reason") or ""), 40, "a deviation needs its reason")

    def test_local_axes_do_not_duplicate_the_policy(self) -> None:
        self.assertEqual(sorted(self.local & self.canonical), [],
                         "an axis declared local is not local if the policy already names it")


if __name__ == "__main__":
    unittest.main()
