import json
import tempfile
import unittest
from pathlib import Path

from build_charnock_custody_manifest import (
    CUSTODY_OUT,
    PACKET_MANIFEST_OUT,
    RECEIPT,
    ROOT,
    build,
    check,
    rehashed_xml_count,
    verified_members,
)


class CustodyManifestTests(unittest.TestCase):
    def setUp(self):
        self.receipt = json.loads((ROOT / RECEIPT).read_text(encoding="utf-8"))
        self.files = self.receipt["sourceManifest"]["files"]

    def test_packet_manifest_reproduces_the_receipt_pin(self):
        _, raw = build()
        from hashlib import sha256

        self.assertEqual(sha256(raw).hexdigest(), self.receipt["sourceManifestSha256"])
        self.assertEqual(raw, (ROOT / PACKET_MANIFEST_OUT).read_bytes())

    def test_committed_custody_manifest_is_reproducible(self):
        report = check()
        self.assertEqual(report["state"], "CUSTODY_MANIFEST_REPRODUCIBLE")
        self.assertEqual(report["fileCount"], len(self.files))
        self.assertEqual(report["sourceArchiveSha256"], self.receipt["sourceArchiveSha256"])
        self.assertEqual(report["destinationSha256Readback"], self.receipt["sourceArchiveSha256"])
        self.assertEqual(report["publicationState"], "BLOCKED")
        self.assertEqual(len(report["manifestSha256"]), 64)

    def test_manifest_pins_every_member_and_totals_them(self):
        custody, _ = build()
        self.assertEqual(set(custody["fileManifest"]), set(self.files))
        self.assertEqual(custody["fileCount"], 46)
        self.assertEqual(
            custody["totalBytes"], sum(item["bytes"] for item in self.files.values())
        )
        stripped = {
            path: {"bytes": item["bytes"], "sha256": item["sha256"]}
            for path, item in custody["fileManifest"].items()
        }
        self.assertEqual(stripped, self.files)
        self.assertTrue(
            all(item["verifiedFrom"] in {"repo", "receipt-pin (object not present in checkout)"}
                for item in custody["fileManifest"].values())
        )

    def test_member_drift_is_refused_instead_of_published(self):
        drifted = {path: dict(pin) for path, pin in self.files.items()}
        target = "data/charnock-biographical-anchors-v1.json"
        drifted[target]["sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "drifted from its receipt pin"):
            verified_members(drifted)

    def test_missing_member_is_refused(self):
        broken = {path: dict(pin) for path, pin in self.files.items()}
        broken["data/charnock-not-there.json"] = {"bytes": 1, "sha256": "1" * 64}
        with self.assertRaisesRegex(ValueError, "missing"):
            verified_members(broken)

    def test_xml_replay_counts_only_matching_objects(self):
        xml_pins = {path: pin for path, pin in self.files.items() if path.startswith("xml/")}
        self.assertTrue(xml_pins)
        with tempfile.TemporaryDirectory() as tmp:
            first = sorted(xml_pins)[0]
            local = Path(tmp) / Path(first).name
            local.write_bytes(b"<TEI>not the packet</TEI>")
            with self.assertRaisesRegex(ValueError, "XML object drifted"):
                rehashed_xml_count(xml_pins, tmp)

    def test_custody_manifest_names_its_source_receipt(self):
        custody, _ = build()
        self.assertEqual(custody["derivedFrom"]["receipt"], RECEIPT)
        self.assertEqual(
            custody["derivedFrom"]["sourceManifestSha256"], self.receipt["sourceManifestSha256"]
        )
        self.assertEqual(custody["supersedes"], "data/charnock-custody-manifest-v4.json")
        self.assertEqual(custody["regenerateWith"], "python3 scripts/build_charnock_custody_manifest.py")
        self.assertEqual(CUSTODY_OUT, "data/charnock-custody-manifest-v5.json")


if __name__ == "__main__":
    unittest.main()
