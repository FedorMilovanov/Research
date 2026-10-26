"""Synthetic receipts below are unit fixtures, never evidence of an upload."""
import copy
import hashlib
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from audit_charnock_handoff import (
    ROOT, REGISTRY, audit_contract, canonical_bytes, inspect, observed_counts, verify_receipt,
)


class HandoffTests(unittest.TestCase):
    def setUp(self):
        self.registry = json.loads((ROOT / REGISTRY).read_text())

    def fixture(self):
        contract = self.registry['handoffContract']
        files = {}
        for name in contract['requiredRepoFiles']:
            raw = (ROOT / name).read_bytes()
            files[name] = dict(bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())
        for identifier, src in self.registry['sources'].items():
            files['xml/' + identifier + '.xml'] = dict(bytes=src['size'], sha256=src['sha256'])
        manifest = dict(contractId=contract['id'], counts=observed_counts(self.registry), files=files)
        digest = hashlib.sha256(b'synthetic test archive; not a real upload').hexdigest()
        return dict(contractId=contract['id'], custodyState='ACQUIRED_DURABLE',
                    publicationState='BLOCKED', holds=['PUBLICATION_HOLD'],
                    sourceArtifactName='SYNTHETIC-TEST-NOT-AN-UPLOAD.zip', sourceWorkflowRun=None,
                    sourceWorkflowRunReason='Synthetic unit fixture,not a workflow',sourceArchiveBytes=123,
                    destinationParentIds=[contract['destinationParentId']],
                    sourceManifestSha256=hashlib.sha256(canonical_bytes(manifest)).hexdigest(),
                    sourceManifest=manifest, sourceArchiveSha256=digest,
                    destinationProvider='Google Drive', destinationObjectId='synthetic-unit-fixture-only',
                    destinationPath='synthetic fixture,not a Drive path', destinationBytes=123,
                    destinationSha256Readback=digest, verifiedAtUtc='2026-10-25T21:00:00Z',
                    verifiedBy='UNIT-TEST-NOT-A-REMOTE-OBSERVATION',
                    verificationMethod='INDEPENDENT_DRIVE_GET_FILE_SHA256_CHECKSUM')

    def test_current_contract(self):
        self.assertEqual(audit_contract(self.registry,packet_replay=True)['counts']['dossierOwners'], 18)

    def test_ten_planned_not_eighteen_authored(self):
        self.assertEqual(observed_counts(self.registry)['plannedDocuments'], 10)

    def test_missing_owner_fails(self):
        self.registry['handoffContract']['dossierOwners'].pop()
        with self.assertRaises(ValueError):
            audit_contract(self.registry)

    def test_duplicate_owner_fails(self):
        owners = self.registry['handoffContract']['dossierOwners']
        owners[-1] = copy.deepcopy(owners[0])
        with self.assertRaisesRegex(ValueError, 'distinct'):
            audit_contract(self.registry)

    def test_count_drift_fails(self):
        self.registry['handoffContract']['expectedCounts']['tcpAnchors'] += 1
        with self.assertRaisesRegex(ValueError, 'count snapshot'):
            audit_contract(self.registry)

    def test_fixture_receipt_preserves_publication_hold(self):
        result = verify_receipt(self.registry, self.fixture())
        self.assertEqual(result['state'], 'BOUNDED_RESEARCH_COMPLETE')
        self.assertEqual(result['publicationState'], 'BLOCKED')

    def test_md5_without_server_sha_is_insufficient(self):
        receipt = self.fixture()
        del receipt['destinationSha256Readback']
        receipt['destinationMd5Readback'] = 'legacy-md5-is-not-sha256'
        with self.assertRaisesRegex(ValueError, 'SHA256'):
            verify_receipt(self.registry, receipt)

    def test_server_sha_mismatch_fails(self):
        receipt = self.fixture()
        receipt['destinationSha256Readback'] = hashlib.sha256(b'other bytes').hexdigest()
        with self.assertRaisesRegex(ValueError, 'SHA256'):
            verify_receipt(self.registry, receipt)

    def test_manifest_tampering_fails(self):
        receipt = self.fixture()
        receipt['sourceManifest']['counts']['tcpAnchors'] += 1
        with self.assertRaisesRegex(ValueError, 'manifest'):
            verify_receipt(self.registry, receipt)

    def test_rehashed_manifest_cannot_hide_changed_file(self):
        receipt = self.fixture()
        receipt['sourceManifest']['files']['AGENT_RULES.md']['bytes'] += 1
        receipt['sourceManifestSha256'] = hashlib.sha256(canonical_bytes(receipt['sourceManifest'])).hexdigest()
        with self.assertRaisesRegex(ValueError, 'differs'):
            verify_receipt(self.registry, receipt)

    def test_publication_promotion_fails(self):
        receipt = self.fixture()
        receipt['publicationState'] = 'APPROVED'
        with self.assertRaises(ValueError):
            verify_receipt(self.registry, receipt)

    def test_missing_receipt_is_not_completion(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name in self.registry['handoffContract']['requiredRepoFiles']:
                target = root / name
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(ROOT / name, target)
            # External Research owners are intentionally not in this isolated packet;
            # test the missing receipt gate after separately validating the contract.
            from unittest.mock import patch
            with patch('audit_charnock_handoff.audit_contract', return_value={'state': 'READY_FOR_CUSTODY'}):
                self.assertEqual(inspect(self.registry, root)['state'], 'READY_FOR_CUSTODY')
                with self.assertRaisesRegex(ValueError, 'Receipt required'):
                    inspect(self.registry, root, require_receipt=True)


if __name__ == '__main__':
    unittest.main()
