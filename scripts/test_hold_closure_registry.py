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

    def test_not_closed_is_not_empty(self) -> None:
        # The registry must keep saying what stays blocked; an empty list would
        # read as "everything is closed", which no audit has established.
        self.assertTrue(self.data.get("notClosed"))


if __name__ == "__main__":
    unittest.main()
