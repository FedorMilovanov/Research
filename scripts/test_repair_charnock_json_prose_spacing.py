import unittest

from repair_charnock_json_prose_spacing import (
    PROTECTED,
    index_rows,
    repair,
    repin,
    verify,
    canonical,
    digest,
)


class JsonProseRepairTests(unittest.TestCase):
    def test_repair_touches_values_but_never_keys_or_protected_rows(self):
        node = {
            "headerKey1word": "Погребение30июля1680",
            "routingReview": {"edgeBoundarySnapshot": [{"boundary": "Одна статья2014"}]},
        }
        fixed = repair(node)
        self.assertIn("headerKey1word", fixed, "keys must survive unchanged")
        self.assertEqual(fixed["headerKey1word"], "Погребение 30 июля 1680")
        self.assertEqual(fixed["routingReview"]["edgeBoundarySnapshot"][0]["boundary"], "Одна статья2014")
        self.assertIn("routingReview.edgeBoundarySnapshot", PROTECTED)

    def test_pin_is_rederived_from_its_own_row(self):
        before = {"a.json": {"rows": [{"id": "R1", "boundary": "Одна статья2014"}],
                             "pins": [{"canonicalRowSha256": digest({"id": "R1", "boundary": "Одна статья2014"})}]}}
        after = repair(before)
        refreshed, proof = repin(after, index_rows(before))
        self.assertEqual(refreshed, 1)
        self.assertEqual(len(proof), 1)
        self.assertEqual(after["a.json"]["pins"][0]["canonicalRowSha256"],
                         digest({"id": "R1", "boundary": "Одна статья 2014"}))

    def test_live_files_are_consistent_with_their_pins(self):
        report = verify("HEAD")
        self.assertEqual(report["pinsStale"], [])
        self.assertEqual(report["nonWhitespaceDriftVsBase"], [])
        self.assertGreater(report["pinsResolvingInternally"], 100)


if __name__ == "__main__":
    unittest.main()
