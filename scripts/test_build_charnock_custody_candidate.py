"""Synthetic custody fixtures are not proof of an archival upload or Drive readback."""
import json
import tempfile
import unittest
from pathlib import Path
from zipfile import ZipFile

from build_charnock_custody_candidate import build

SHA = "a" * 40


class CharnockCustodyCandidateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.out = self.root / "out"
        self.paths = [f"research/volume-{i:02d}.md" for i in range(14)] + ["research/Чарнок-источник.md"]
        baseline = {
            "contractId": "CHARNOCK-CUSTODY-V2",
            "fileManifest": {name: {"bytes": 999} for name in self.paths},
        }
        p = self.root / "data/charnock-custody-manifest-v2.json"
        p.parent.mkdir(parents=True)
        p.write_text(json.dumps(baseline, ensure_ascii=False), encoding="utf-8")
        for i, name in enumerate(self.paths):
            target = self.root / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(f"Чарнок: изменённый источник {i}\n", encoding="utf-8")

    def tearDown(self):
        self.temp.cleanup()

    def build(self):
        return build(self.root, "data/charnock-custody-manifest-v2.json", self.out, SHA)

    def test_rehashes_real_bytes_and_preserves_all_holds(self):
        report = self.build()
        with ZipFile(self.out / report["archiveName"]) as archive:
            manifest = json.loads(archive.read("manifest.json"))
            self.assertEqual(manifest["fileCount"], 15)
            self.assertEqual(manifest["custodyState"], "PENDING_INDEPENDENT_DRIVE_SHA256_READBACK")
            self.assertEqual(manifest["publicationState"], "BLOCKED")
            self.assertIsNone(manifest["independentDestinationReceipt"])
            for name in self.paths:
                source = (self.root / name).read_bytes()
                self.assertEqual(archive.read("files/" + name), source)
                self.assertEqual(manifest["fileManifest"][name]["bytes"], len(source))
        self.assertEqual(report["destinationState"], "NOT_UPLOADED_OR_VERIFIED")

    def test_reproducible_and_does_not_mutate_sources(self):
        original = (self.root / self.paths[0]).read_bytes()
        first = self.build()
        second = self.build()
        self.assertEqual(first["archiveSha256"], second["archiveSha256"])
        self.assertEqual((self.root / self.paths[0]).read_bytes(), original)

    def test_source_edit_changes_archive(self):
        first = self.build()
        (self.root / self.paths[0]).write_text("новое содержание", encoding="utf-8")
        second = self.build()
        self.assertNotEqual(first["archiveSha256"], second["archiveSha256"])

    def test_missing_file_fails_closed(self):
        (self.root / self.paths[0]).unlink()
        with self.assertRaisesRegex(ValueError, "Missing or unsafe"):
            self.build()

    def test_path_traversal_fails_closed(self):
        p = self.root / "data/charnock-custody-manifest-v2.json"
        item = json.loads(p.read_text(encoding="utf-8"))
        item["fileManifest"].pop(self.paths[0])
        item["fileManifest"]["../other.txt"] = {}
        p.write_text(json.dumps(item), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "Unsafe Charnock custody path"):
            self.build()

    def test_non_commit_reference_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "full 40-digit"):
            build(self.root, "data/charnock-custody-manifest-v2.json", self.out, "main")


if __name__ == "__main__":
    unittest.main()
