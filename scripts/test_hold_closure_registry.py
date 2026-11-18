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

    def test_verification_commands_are_runnable_strings(self) -> None:
        for entry in self.data["confirmations"]:
            verification = entry.get("verification")
            if not isinstance(verification, dict):
                continue
            with self.subTest(entry["id"]):
                self.assertIn("python3", verification.get("command", "") + verification.get("tests", ""))

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

    def test_not_closed_is_not_empty(self) -> None:
        # The registry must keep saying what stays blocked; an empty list would
        # read as "everything is closed", which no audit has established.
        self.assertTrue(self.data.get("notClosed"))


if __name__ == "__main__":
    unittest.main()
