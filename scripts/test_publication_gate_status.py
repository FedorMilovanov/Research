#!/usr/bin/env python3
"""Offline tests for scripts/publication_gate_status.py.

The gate is about composition and drift. The contract: overlays must be applied
before anything is read as current; the composed counts must agree with what the
authority declares; a record that appears, vanishes, changes disposition/holds/
nextAction, or becomes PROMOTE while holding a hold must fail the check; and
missing authority files or lost rights ids must be counted, never smoothed over.
"""
from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

import publication_gate_status as pg


def record(rid: str, disposition: str = "BLOCKED", holds: tuple[str, ...] = ("PUBLICATION_HOLD",),
           authority: str = "authority.md", next_action: str = "do the bounded thing") -> dict:
    return {
        "id": rid,
        "corpus": rid.upper(),
        "disposition": disposition,
        "researchStatus": "TEST",
        "sourceAuthorities": [authority],
        "holds": list(holds),
        "rightsLedgerIds": ["DRV-TEST"],
        "nextAction": next_action,
    }


class Repo:
    """Temporary checkout with a base queue, a current authority and an overlay."""

    def __init__(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        (self.root / "data").mkdir()
        self.write("authority.md", "authority\n")
        self.write("data/rights.json", json.dumps({"id": "DRV-TEST"}))
        self.write("data/public-projection-queue-2026-08-01.json", json.dumps({
            "authorityId": "BASE",
            "records": [record("alpha"), record("beta", holds=("RIGHTS_HOLD",))],
        }))
        self.write("data/public-projection-current-2026-08-02.json", json.dumps({
            "authorityId": "CURRENT",
            "baseQueue": "data/public-projection-queue-2026-08-01.json",
            "overlays": [],
            "compositionRule": "apply overlays",
            "policy": {"promoteRequiresNoHolds": True},
            "effectiveCounts": {"PROMOTE": 0, "REFERENCE": 0, "SUPERSEDED": 0, "BLOCKED": 2, "total": 2},
        }))

    def write(self, rel: str, text: str) -> Path:
        path = self.root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def set_current(self, **overrides) -> None:
        path = self.root / "data" / "public-projection-current-2026-08-02.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        data.update(overrides)
        path.write_text(json.dumps(data), encoding="utf-8")

    def snapshot(self) -> dict:
        return pg.augment(pg.load_composed(self.root), self.root)

    def close(self) -> None:
        self._tmp.cleanup()


class CompositionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.repo = Repo()

    def tearDown(self) -> None:
        self.repo.close()

    def test_base_alone_is_not_current(self) -> None:
        composed = pg.load_composed(self.repo.root)
        self.assertEqual(composed["currentAuthority"], "CURRENT")
        self.assertEqual(composed["composedCounts"], {"BLOCKED": 2})

    def test_overlay_replaces_the_record(self) -> None:
        self.repo.write("data/overlay.json", json.dumps({
            "authority_id": "OVL-1",
            "supersedes_queue_record_id": "alpha",
            "effective_record": record("alpha", disposition="REFERENCE"),
        }))
        self.repo.set_current(overlays=["data/overlay.json"],
                              effectiveCounts={"PROMOTE": 0, "REFERENCE": 1, "SUPERSEDED": 0,
                                               "BLOCKED": 1, "total": 2})
        snapshot = self.repo.snapshot()
        by_id = {r["id"]: r for r in snapshot["records"]}
        self.assertEqual(by_id["alpha"]["disposition"], "REFERENCE")
        self.assertEqual(by_id["alpha"]["previousDisposition"], "BLOCKED")
        self.assertEqual(by_id["alpha"]["supersededBy"], "OVL-1")
        self.assertEqual(snapshot["composedCounts"], {"BLOCKED": 1, "REFERENCE": 1})

    def test_overlay_naming_unknown_record_raises(self) -> None:
        self.repo.write("data/overlay.json", json.dumps({
            "authority_id": "OVL-X",
            "supersedes_queue_record_id": "nope",
            "effective_record": record("nope"),
        }))
        self.repo.set_current(overlays=["data/overlay.json"])
        with self.assertRaises(ValueError):
            pg.load_composed(self.repo.root)

    def test_overlay_without_payload_raises(self) -> None:
        self.repo.write("data/overlay.json", json.dumps({"authority_id": "OVL-Y"}))
        self.repo.set_current(overlays=["data/overlay.json"])
        with self.assertRaises(ValueError):
            pg.load_composed(self.repo.root)


class CheckTests(unittest.TestCase):
    def setUp(self) -> None:
        self.repo = Repo()
        self.committed = self.repo.snapshot()

    def tearDown(self) -> None:
        self.repo.close()

    def test_identical_snapshot_passes(self) -> None:
        self.assertEqual(pg.check(self.repo.snapshot(), self.committed), [])

    def test_new_record_fails(self) -> None:
        path = self.repo.root / "data" / "public-projection-queue-2026-08-01.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        data["records"].append(record("gamma"))
        path.write_text(json.dumps(data), encoding="utf-8")
        problems = pg.check(self.repo.snapshot(), self.committed)
        self.assertTrue(any("record appeared" in p for p in problems), problems)

    def test_vanished_record_fails(self) -> None:
        path = self.repo.root / "data" / "public-projection-queue-2026-08-01.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        data["records"] = [r for r in data["records"] if r["id"] != "beta"]
        path.write_text(json.dumps(data), encoding="utf-8")
        problems = pg.check(self.repo.snapshot(), self.committed)
        self.assertTrue(any("record vanished" in p for p in problems), problems)

    def test_disposition_change_fails(self) -> None:
        path = self.repo.root / "data" / "public-projection-queue-2026-08-01.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        data["records"][0]["disposition"] = "REFERENCE"
        path.write_text(json.dumps(data), encoding="utf-8")
        problems = pg.check(self.repo.snapshot(), self.committed)
        self.assertTrue(any("disposition changed" in p for p in problems), problems)

    def test_next_action_change_fails(self) -> None:
        path = self.repo.root / "data" / "public-projection-queue-2026-08-01.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        data["records"][0]["nextAction"] = "something weaker"
        path.write_text(json.dumps(data), encoding="utf-8")
        problems = pg.check(self.repo.snapshot(), self.committed)
        self.assertTrue(any("nextAction changed" in p for p in problems), problems)

    def test_promote_with_holds_fails_policy(self) -> None:
        path = self.repo.root / "data" / "public-projection-queue-2026-08-01.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        data["records"][0]["disposition"] = "PROMOTE"
        path.write_text(json.dumps(data), encoding="utf-8")
        problems = pg.check(self.repo.snapshot(), self.committed)
        self.assertTrue(any("PROMOTE declared with holds" in p for p in problems), problems)


class AugmentTests(unittest.TestCase):
    def setUp(self) -> None:
        self.repo = Repo()

    def tearDown(self) -> None:
        self.repo.close()

    def test_missing_authority_file_is_counted(self) -> None:
        path = self.repo.root / "data" / "public-projection-queue-2026-08-01.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        data["records"][0]["sourceAuthorities"] = ["nowhere/absent.md"]
        path.write_text(json.dumps(data), encoding="utf-8")
        snapshot = self.repo.snapshot()
        self.assertEqual(snapshot["checks"]["recordsWithMissingAuthorityFile"], 1)

    def test_lost_rights_id_is_counted(self) -> None:
        path = self.repo.root / "data" / "public-projection-queue-2026-08-01.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        data["records"][0]["rightsLedgerIds"] = ["DRV-NOT-ANYWHERE"]
        path.write_text(json.dumps(data), encoding="utf-8")
        snapshot = self.repo.snapshot()
        self.assertEqual(snapshot["checks"]["rightsIdsNotRecorded"], 1)

    def test_snapshot_is_read_only(self) -> None:
        before = sorted(p.relative_to(self.repo.root).as_posix() for p in self.repo.root.rglob("*"))
        self.repo.snapshot()
        after = sorted(p.relative_to(self.repo.root).as_posix() for p in self.repo.root.rglob("*"))
        self.assertEqual(before, after)

    def test_rights_ledger_entry_is_attached_verbatim(self) -> None:
        self.repo.write("data/physical-rights-ledger-2026-08-01.json", json.dumps({
            "driveCheckedAt": "2026-08-01",
            "rule": "Drive presence proves custody only.",
            "records": [{"id": "DRV-TEST", "corpusId": "alpha",
                         "rightsState": "ITEM_LEVEL_REVIEW_REQUIRED",
                         "publicationEligible": False,
                         "driveObjects": [{"id": "x"}, {"id": "y"}]}],
        }))
        snapshot = self.repo.snapshot()
        by_id = {r["id"]: r for r in snapshot["records"]}
        self.assertEqual(by_id["alpha"]["rightsLedger"]["rightsState"], "ITEM_LEVEL_REVIEW_REQUIRED")
        self.assertEqual(by_id["alpha"]["rightsLedger"]["driveObjects"], 2)
        self.assertIsNone(by_id["beta"]["rightsLedger"])
        self.assertEqual(snapshot["checks"]["recordsWithoutRightsLedgerEntry"], 1)
        self.assertEqual(snapshot["checks"]["rightsLedgerEntriesPublicationEligible"], 0)

    def test_publication_eligible_true_is_counted(self) -> None:
        self.repo.write("data/physical-rights-ledger-2026-08-01.json", json.dumps({
            "records": [{"id": "DRV-TEST", "corpusId": "alpha", "rightsState": "OK",
                         "publicationEligible": True, "driveObjects": []}],
        }))
        snapshot = self.repo.snapshot()
        self.assertEqual(snapshot["checks"]["rightsLedgerEntriesPublicationEligible"], 1)

    def test_summary_mentions_every_record(self) -> None:
        text = pg.summary(self.repo.snapshot())
        self.assertIn("alpha", text)
        self.assertIn("beta", text)
        self.assertIn("PROMOTE 0", text)


if __name__ == "__main__":
    unittest.main()
