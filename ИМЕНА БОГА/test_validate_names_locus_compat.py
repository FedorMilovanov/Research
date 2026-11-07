"""Adversarial sidecar compatibility tests, without editing any V1 ledger."""
from __future__ import annotations

import copy
import unittest

from validate_names_locus_compat import (
    DATA, load_json, resolve_locus_id, validate_locus_compat,
)


class LocusCompatibilityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.baseline = load_json(DATA / "names_ledger_v1.json")
        cls.extension = load_json(DATA / "names_extension_ledger_v1.json")
        cls.registry = load_json(DATA / "names_locus_compat_v1.json")

    def check(self, baseline=None, extension=None, registry=None):
        return validate_locus_compat(
            self.baseline if baseline is None else baseline,
            self.extension if extension is None else extension,
            self.registry if registry is None else registry,
        )

    def match(self, aid: str):
        row = next(x for x in self.registry["mappings"] if x["attestationId"] == aid)
        doc = self.baseline if row["ledger"] == "baseline" else self.extension
        witness = next(
            a for parent in doc["records"] if parent["id"] == row["recordId"]
            for a in parent["attestations"] if a["attestationId"] == aid
        )
        return row, witness

    def test_baseline_105_identity_map_is_valid(self):
        self.assertEqual([], self.check())
        self.assertEqual(105, len(self.registry["mappings"]))

    def test_original_50_inline_and_55_missing_remain_unchanged(self):
        rows = self.registry["mappings"]
        self.assertEqual(50, sum(m["mode"] == "PRESERVE_INLINE_V1" for m in rows))
        self.assertEqual(55, sum(m["mode"] == "SIDECAR_ALIAS_ONLY_V1" for m in rows))
        self.assertEqual(51, sum(m["ledger"] == "baseline" and m["inlineLocusId"] is None for m in rows))
        self.assertEqual(4, sum(m["ledger"] == "extension" and m["inlineLocusId"] is None for m in rows))

    def test_all_105_resolve_without_mutating_inline_v1(self):
        self.assertEqual(105, len({resolve_locus_id(self.match(m["attestationId"])[1], m) for m in self.registry["mappings"]}))
        for m in self.registry["mappings"]:
            _, witness = self.match(m["attestationId"])
            self.assertEqual(m["inlineLocusId"], witness.get("locusId"))

    def test_existing_v1_locus_id_preserved(self):
        row, w = self.match("ATT-BASE-YHWH-01")
        self.assertEqual("PRESERVE_INLINE_V1", row["mode"])
        self.assertEqual(w["locusId"], resolve_locus_id(w, row))

    def test_baseline_missing_inline_has_stable_derived_alias(self):
        row, w = self.match("ATT-BASE-TSIDKENU-01")
        self.assertEqual("SIDECAR_ALIAS_ONLY_V1", row["mode"])
        self.assertNotIn("locusId", w)
        self.assertEqual("legacy-att-base-tsidkenu-01", resolve_locus_id(w, row))

    def test_extension_missing_inline_has_stable_derived_alias(self):
        rows = [r for r in self.registry["mappings"] if r["ledger"] == "extension" and r["inlineLocusId"] is None]
        self.assertEqual(4, len(rows))
        row, w = self.match(rows[0]["attestationId"])
        self.assertEqual("legacy-" + row["attestationId"].lower(), resolve_locus_id(w, row))

    def test_mapping_loses_a_row(self):
        d = copy.deepcopy(self.registry)
        d["mappings"].pop()
        self.assertTrue(any("missing or extra 105 witness mappings" in e for e in self.check(registry=d)))

    def test_added_unreviewed_attestation_has_no_mapping(self):
        d = copy.deepcopy(self.extension)
        a = next(r for r in d["records"] if r["id"] == "eloah")
        new = copy.deepcopy(a["attestations"][0])
        new["attestationId"] = "ATT-EXT-ELOAH-02"
        new["locusId"] = "new-silent-locus"
        a["attestations"].append(new)
        self.assertTrue(any("missing or extra 105 witness mappings" in e for e in self.check(extension=d)))

    def test_orphan_registry_mapping_fails(self):
        d = copy.deepcopy(self.registry)
        d["mappings"][0]["attestationId"] = "ATT-EXT-MISSING-01"
        self.assertTrue(any("orphan mapped attestation" in e for e in self.check(registry=d)))

    def test_duplicate_mapped_attestation_fails(self):
        d = copy.deepcopy(self.registry)
        d["mappings"][1]["attestationId"] = d["mappings"][0]["attestationId"]
        self.assertTrue(any("duplicate/invalid mapped attestation ID" in e for e in self.check(registry=d)))

    def test_alias_renaming_fails_closed(self):
        d = copy.deepcopy(self.registry)
        r = next(x for x in d["mappings"] if x["mode"] == "SIDECAR_ALIAS_ONLY_V1")
        r["resolvedLocusId"] = "a-convenient-but-unstable-alias"
        self.assertTrue(any("not stable attestation-derived" in e for e in self.check(registry=d)))

    def test_existing_inline_renamed_in_ledger_fails_closed(self):
        d = copy.deepcopy(self.baseline)
        a = next(r for r in d["records"] if r["id"] == "yhwh")["attestations"][0]
        a["locusId"] = "arbitrary-new-identifier"
        self.assertTrue(any("existing inline locusId changed" in e for e in self.check(baseline=d)))

    def test_existing_inline_renamed_in_sidecar_fails_closed(self):
        d = copy.deepcopy(self.registry)
        r = next(x for x in d["mappings"] if x["mode"] == "PRESERVE_INLINE_V1")
        r["resolvedLocusId"] = "arbitrary-new-identifier"
        self.assertTrue(any("existing inline locusId changed" in e for e in self.check(registry=d)))

    def test_alias_pushed_into_v1_inline_is_not_silent(self):
        d = copy.deepcopy(self.baseline)
        a = next(r for r in d["records"] if r["id"] == "tsidkenu")["attestations"][0]
        a["locusId"] = "legacy-att-base-tsidkenu-01"
        self.assertTrue(any("alias-only witness silently changed inline V1" in e for e in self.check(baseline=d)))

    def test_duplicate_resolved_locus_id_across_witnesses_fails(self):
        d = copy.deepcopy(self.registry)
        items = [x for x in d["mappings"] if x["mode"] == "PRESERVE_INLINE_V1"]
        items[1]["resolvedLocusId"] = items[0]["resolvedLocusId"]
        self.assertTrue(any("existing inline locusId changed" in e or "duplicate resolved locusId" in e for e in self.check(registry=d)))

    def test_swap_parent_record_does_not_change_provenance(self):
        d = copy.deepcopy(self.registry)
        d["mappings"][0]["recordId"] = "unrelated-record"
        self.assertTrue(any("original parent ownership changed" in e for e in self.check(registry=d)))

    def test_source_fk_swap_fails_closed(self):
        d = copy.deepcopy(self.registry)
        d["mappings"][0]["sourceId"] = "SRC-NONEXISTENT"
        self.assertTrue(any("resolver witness binding mismatch (sourceId)" in e for e in self.check(registry=d)))

    def test_edition_fk_swap_fails_closed(self):
        d = copy.deepcopy(self.registry)
        d["mappings"][0]["editionId"] = "ED-NONEXISTENT"
        self.assertTrue(any("resolver witness binding mismatch (editionId)" in e for e in self.check(registry=d)))

    def test_verse_swap_fails_closed(self):
        d = copy.deepcopy(self.registry)
        d["mappings"][0]["verse"] = "Exodus 999"
        self.assertTrue(any("resolver witness binding mismatch (verse)" in e for e in self.check(registry=d)))

    def test_empty_or_malformed_mapping_is_error_not_exception(self):
        d = copy.deepcopy(self.registry)
        d["mappings"][0]["resolvedLocusId"] = []
        self.assertTrue(self.check(registry=d))
        d["mappings"][0] = None
        self.assertTrue(any("non-object mapping" in e for e in self.check(registry=d)))

    def test_unapproved_mode_is_rejected(self):
        d = copy.deepcopy(self.registry)
        d["mappings"][0]["mode"] = "AUTO_BACKFILLED_TO_PRODUCT"
        self.assertTrue(any("unsupported migration mode" in e for e in self.check(registry=d)))

    def test_publication_and_consumer_migration_hold(self):
        d = copy.deepcopy(self.registry)
        d["status"] = "PRODUCT_APPROVED"
        self.assertTrue(any("publication HOLD promoted" in e for e in self.check(registry=d)))
        d = copy.deepcopy(self.registry)
        d["lifecycle"]["consumers"] = "AUTO_PUSHED_TO_ALL_SITES"
        self.assertTrue(any("unsafe automatic consumer migration" in e for e in self.check(registry=d)))

    def test_counts_cannot_falsely_claim_inline_zero(self):
        d = copy.deepcopy(self.registry)
        d["counts"]["missingInlineLocusIds"] = 0
        self.assertTrue(any("registry counts or Product approvals drifted" in e for e in self.check(registry=d)))

    def test_no_published_product_claim_from_resolver(self):
        self.assertEqual("RESEARCH_HOLD_NO_AUTOMATIC_LEDGER_OR_PRODUCT_MUTATION", self.registry["status"])
        self.assertEqual(0, self.registry["counts"]["productApprovals"])


if __name__ == "__main__":
    unittest.main()
