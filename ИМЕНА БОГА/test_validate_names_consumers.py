"""Negative / positive checks for existing Research consumers and Product HOLD."""
from __future__ import annotations
import copy
import unittest

from validate_names_consumers import (
    DATA, EXPECTED_CONTRACTS, ROOT, load_json, validate_consumer_contracts,
)


class ConsumerCompatibilityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.b = load_json(DATA / "names_ledger_v1.json")
        cls.e = load_json(DATA / "names_extension_ledger_v1.json")
        cls.crosswalk = load_json(DATA / "names_locus_compat_v1.json")
        cls.inv = load_json(DATA / "names_consumer_compat_v1.json")
        cls.docs = {name: load_json(ROOT / p) for name, p, _, _, _ in EXPECTED_CONTRACTS}

    def check(self, b=None, e=None, x=None, inv=None, docs=None):
        return validate_consumer_contracts(
            self.b if b is None else b, self.e if e is None else e,
            self.crosswalk if x is None else x, self.inv if inv is None else inv,
            self.docs if docs is None else docs,
        )

    def test_all_current_internal_consumer_contracts_valid(self):
        self.assertEqual([], self.check())

    def test_four_independent_inline_groups_cover_50_unique(self):
        self.assertEqual([16, 12, 14, 8], [
            len(self.docs[k]["lockedAttestations"]) for k in
            ("memorial", "speech", "extension", "core")
        ])

    def test_general_original_snapshot_22_without_locus(self):
        rows = self.docs["general"]["lockedAttestations"]
        self.assertEqual(22, len(rows))
        self.assertTrue(all("locusId" not in row for row in rows))

    def test_legacy_inline_contract_cannot_lose_witness(self):
        d = copy.deepcopy(self.docs)
        d["memorial"]["lockedAttestations"].pop()
        self.assertTrue(any("expected 16 independent lock snapshots" in x for x in self.check(docs=d)))

    def test_legacy_inline_contract_cannot_duplicate_witness(self):
        d = copy.deepcopy(self.docs)
        a = d["core"]["lockedAttestations"]
        a[1] = copy.deepcopy(a[0])
        self.assertTrue(any("duplicate internal contract witness" in x for x in self.check(docs=d)))

    def test_existing_locus_id_cannot_rename_in_snapshot(self):
        d = copy.deepcopy(self.docs)
        d["speech"]["lockedAttestations"][0]["locusId"] = "made-up-new-locus"
        self.assertTrue(any("pinned inline locusId lost" in x for x in self.check(docs=d)))

    def test_existing_locus_id_cannot_move_to_other_record(self):
        d = copy.deepcopy(self.docs)
        d["core"]["lockedAttestations"][0]["baselineId"] = "sabaoth"
        self.assertTrue(any("witness moved to wrong original record" in x for x in self.check(docs=d)))

    def test_existing_contract_verse_change_detected(self):
        d = copy.deepcopy(self.docs)
        d["memorial"]["lockedAttestations"][0]["verse"] = "Genesis 500"
        self.assertTrue(any("exact snapshot field drift (verse)" in x for x in self.check(docs=d)))

    def test_existing_contract_original_surface_change_detected(self):
        d = copy.deepcopy(self.docs)
        d["core"]["lockedAttestations"][0]["surface"] = "not original Hebrew"
        self.assertTrue(any("exact snapshot field drift (surface)" in x for x in self.check(docs=d)))

    def test_existing_contract_edition_change_detected(self):
        d = copy.deepcopy(self.docs)
        d["extension"]["lockedAttestations"][0]["edition"] = "Other Bible"
        self.assertTrue(any("exact snapshot field drift (edition)" in x for x in self.check(docs=d)))

    def test_existing_contract_source_url_change_detected(self):
        d = copy.deepcopy(self.docs)
        d["speech"]["lockedAttestations"][0]["sourceUrl"] = "https://example.org/fake"
        self.assertTrue(any("exact snapshot field drift (sourceUrl)" in x for x in self.check(docs=d)))

    def test_contract_permissions_cannot_be_upgraded(self):
        d = copy.deepcopy(self.docs)
        d["core"]["lockedAttestations"][0]["rightsState"] = "PUBLICATION_ELIGIBLE"
        self.assertTrue(any("exact snapshot field drift (rightsState)" in x for x in self.check(docs=d)))

    def test_contract_manuscript_collation_cannot_be_faked(self):
        d = copy.deepcopy(self.docs)
        d["memorial"]["lockedAttestations"][0]["criticalEditionStatus"] = "COLLATED"
        self.assertTrue(any("exact snapshot field drift (criticalEditionStatus)" in x for x in self.check(docs=d)))

    def test_contract_publication_state_cannot_be_faked(self):
        d = copy.deepcopy(self.docs)
        d["extension"]["lockedAttestations"][0]["publicationState"] = "APPROVED"
        self.assertTrue(any("exact snapshot field drift (publicationState)" in x for x in self.check(docs=d)))

    def test_generic_contract_locus_cannot_be_backfilled_inline(self):
        d = copy.deepcopy(self.docs)
        d["general"]["lockedAttestations"][0]["locusId"] = "arbitrary-legacy"
        self.assertTrue(any("general 22-history contract must remain without locusId" in x for x in self.check(docs=d)))

    def test_generic_contract_surface_mutation_loses_uniqueness(self):
        d = copy.deepcopy(self.docs)
        d["general"]["lockedAttestations"][0]["surface"] = "wrong text"
        self.assertTrue(any("general contract source witness not unique" in x for x in self.check(docs=d)))

    def test_generic_contract_verse_mutation_loses_uniqueness(self):
        d = copy.deepcopy(self.docs)
        d["general"]["lockedAttestations"][0]["verse"] = "Genesis 999"
        self.assertTrue(any("general contract source witness not unique" in x for x in self.check(docs=d)))

    def test_generic_source_rights_mutation_detected(self):
        d = copy.deepcopy(self.docs)
        d["general"]["lockedAttestations"][0]["rightsState"] = "PUBLICATION_ELIGIBLE"
        self.assertTrue(any("exact snapshot field drift (rightsState)" in x for x in self.check(docs=d)))

    def test_generic_snapshot_cannot_duplicate_another(self):
        d = copy.deepcopy(self.docs)
        d["general"]["lockedAttestations"][1] = copy.deepcopy(d["general"]["lockedAttestations"][0])
        self.assertTrue(any("generic snapshot duplicated" in x for x in self.check(docs=d)))

    def test_inventory_counts_cannot_falsify_consumer_coverage(self):
        d = copy.deepcopy(self.inv)
        d["internalEvidence"]["internalLocusSnapshotsCovered"] = 105
        self.assertTrue(any("internal contract inventory/counters changed" in x for x in self.check(inv=d)))

    def test_inventory_cannot_claim_deployment_witness(self):
        d = copy.deepcopy(self.inv)
        d["v2Gate"]["deploymentEvidence"] = "PRODUCTION_CONFIRMED"
        self.assertTrue(any("external/V2/rights/critical manuscript gate" in x for x in self.check(inv=d)))

    def test_inventory_cannot_auto_approve_inline_backfill(self):
        d = copy.deepcopy(self.inv)
        d["v2Gate"]["automaticInlineBackfill"] = True
        self.assertTrue(any("external/V2/rights/critical manuscript gate" in x for x in self.check(inv=d)))

    def test_inspected_external_repos_cannot_claim_consumer_verified(self):
        d = copy.deepcopy(self.inv)
        d["externalCandidates"][0]["consumerContract"] = "VERIFIED"
        self.assertTrue(any("inspected external repository results are not runtime proofs" in x for x in self.check(inv=d)))

    def test_legacy_source_50_and_general_22_disjoint(self):
        d = copy.deepcopy(self.crosswalk)
        generic_aid = "ATT-BASE-SABAOTH-01"
        item = next(x for x in d["mappings"] if x["attestationId"] == generic_aid)
        item["mode"] = "PRESERVE_INLINE_V1"
        self.assertTrue(self.check(x=d))

    def test_json_contract_witness_malformed_fails_cleanly(self):
        d = copy.deepcopy(self.docs)
        d["general"]["lockedAttestations"][0] = None
        self.assertTrue(any("malformed contract witness" in x for x in self.check(docs=d)))


if __name__ == "__main__":
    unittest.main()
