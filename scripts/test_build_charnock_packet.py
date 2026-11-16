import hashlib
import json
import tempfile
import unittest
import zipfile
from pathlib import Path

import build_charnock_packet as packet


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


class PacketBuildTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / "alpha.md").write_text("alpha\n", encoding="utf-8")
        (self.root / "xml").mkdir()
        (self.root / "xml" / "A1.xml").write_text("<TEI>one</TEI>", encoding="utf-8")
        files = {}
        for rel in ("alpha.md", "xml/A1.xml"):
            raw = (self.root / rel).read_bytes()
            files[rel] = {"bytes": len(raw), "sha256": sha(raw)}
        self.receipt = {
            "sourceManifest": {
                "contractId": "CHARNOCK-HANDOFF-V1",
                "kind": "TEST_PACKET",
                "counts": {"xmlObjects": 1},
                "files": files,
            }
        }
        (self.root / "receipt.json").write_text(json.dumps(self.receipt), encoding="utf-8")
        self._saved_root = packet.ROOT
        packet.ROOT = self.root
        self.xml_dir = self.root / "xml"

    def tearDown(self):
        packet.ROOT = self._saved_root
        self.tmp.cleanup()

    def _build(self, allow_drift=False):
        return packet.build(
            "receipt.json",
            "TEST.zip",
            self.root / "out" / "test.zip",
            self.root / "out" / "manifest.json",
            self.xml_dir,
            allow_drift=allow_drift,
        )

    def test_archive_is_byte_reproducible(self):
        first = self._build()
        raw_first = (self.root / "out" / "test.zip").read_bytes()
        second = self._build()
        raw_second = (self.root / "out" / "test.zip").read_bytes()
        self.assertEqual(raw_first, raw_second)
        self.assertEqual(first["zipSha256"], second["zipSha256"])
        self.assertEqual(first["manifestSha256"], second["manifestSha256"])

    def test_manifest_member_is_inside_the_archive(self):
        self._build()
        with zipfile.ZipFile(self.root / "out" / "test.zip") as archive:
            names = archive.namelist()
            payload = json.loads(archive.read(packet.MANIFEST_MEMBER))
        self.assertEqual(names, ["alpha.md", packet.MANIFEST_MEMBER, "xml/A1.xml"])
        self.assertEqual(set(payload["files"]), {"alpha.md", "xml/A1.xml"})

    def test_undeclared_drift_blocks_the_build(self):
        (self.root / "alpha.md").write_text("alpha changed\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "no longer matches the base receipt"):
            self._build()

    def test_declared_drift_is_packaged_and_reported(self):
        (self.root / "alpha.md").write_text("alpha changed\n", encoding="utf-8")
        report = self._build(allow_drift=True)
        self.assertEqual(report["changedSinceBaseReceipt"], ["alpha.md"])
        with zipfile.ZipFile(self.root / "out" / "test.zip") as archive:
            self.assertEqual(archive.read("alpha.md"), b"alpha changed\n")

    def test_missing_member_is_refused(self):
        (self.root / "xml" / "A1.xml").unlink()
        with self.assertRaisesRegex(ValueError, "missing"):
            self._build(allow_drift=True)


if __name__ == "__main__":
    unittest.main()
