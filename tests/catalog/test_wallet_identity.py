"""Wallet identity and named coverage contracts, using real validation."""

import copy
import json
from dataclasses import replace
import unittest
from pathlib import Path

from tools.catalog.loader import load_catalog
from tools.catalog.model import WalletRecord
from tools.catalog.validator import validate_catalog

ROOT = Path(__file__).resolve().parents[2]
NAMED = set("trust-wallet metamask coinbase-wallet exodus atomic-wallet onekey ledger okx-wallet bitget-wallet safepal tangem-seed keystone bitbox02 ellipal coinomi guarda tokenpocket imtoken rabby rainbow zerion sparrow bluewallet coldcard blockstream-jade passport seedsigner phantom solflare backpack glow keplr leap cosmostation temple kukai".split())


class WalletIdentityTests(unittest.TestCase):
    def pair(self, **changes):
        catalog = load_catalog(ROOT / "tests/catalog/fixtures/valid-minimal")
        data = json.loads(catalog.wallets[0].path.read_text(encoding="utf-8"))
        data.update(product_id="sample-wallet", product_name="Sample Wallet", aliases=[],
                    mode_id="mnemonic-generated", platform="web",
                    version_interval={"min": "1.0", "max": "2.0"})
        other = copy.deepcopy(data)
        other.update(id="second-wallet", **changes)
        return replace(catalog, wallets=(
            WalletRecord(data["id"], catalog.wallets[0].path, data),
            WalletRecord(other["id"], catalog.wallets[0].path, other)))

    def codes(self, catalog):
        return {f.code for f in validate_catalog(catalog)}

    def test_no_overlapping_product_platform_version_mode(self):
        self.assertIn("wallet-identity-overlap", self.codes(self.pair()))

    def test_same_product_can_have_distinct_modes(self):
        self.assertNotIn("wallet-identity-overlap", self.codes(self.pair(mode_id="mnemonic-imported")))
        self.assertNotIn("wallet-alias-ambiguity", self.codes(self.pair(mode_id="mnemonic-imported")))

    def test_import_only_is_not_generation_evidence(self):
        self.assertIn("wallet-import-generation", self.codes(self.pair(import_only=True, generates_mnemonic=True)))

    def test_all_named_products_have_terminal_status(self):
        catalog = load_catalog(ROOT)
        items = {r.id: r.data for s in catalog.required_sets for r in s.requirements}
        for name in sorted(NAMED):
            with self.subTest(product=name):
                item = items["wallet-" + name]
                self.assertEqual(item["research_state"], "terminal", name)
                self.assertTrue(item["record_ids"])
                for identifier in item["record_ids"]:
                    record = next(r for r in catalog.wallets if r.id == identifier)
                    self.assertIn(record.data["status"], {"documented", "blocked", "no-mnemonic-confirmed"})
                    self.assertTrue(record.data["evidence_ids"])

    def test_all_networks_have_evidenced_terminal_profiles(self):
        catalog = load_catalog(ROOT)
        wallets = {r.id: r for r in catalog.wallets}
        evidence = {r.id: r for r in catalog.evidence}
        for item in catalog.required_sets[0].requirements:
            if item.id.startswith("network-"):
                with self.subTest(network=item.id):
                    self.assertEqual(item.data["research_state"], "terminal")
                    self.assertTrue(item.data["record_ids"])
                    for identifier in item.data["record_ids"]:
                        wallet = wallets[identifier]
                        self.assertIn(item.id[8:], wallet.data["network_ids"])
                        self.assertTrue(any(evidence[e].data["source_type"].startswith("official-")
                                            for e in wallet.data["evidence_ids"]))

    def test_numeric_versions_compare_numerically_and_touching_bounds_overlap(self):
        for interval, overlaps in [({"min": "2.0", "max": "3.0"}, True),
                                   ({"min": "2.0.1", "max": "10.0"}, False),
                                   ({"min": "10.0", "max": None}, False),
                                   ({"min": "1.0.0", "max": "1.9"}, True)]:
            with self.subTest(interval=interval):
                self.assertEqual("wallet-identity-overlap" in self.codes(self.pair(version_interval=interval)), overlaps)

    def test_unknown_versions_fail_closed_and_reverse_range_rejected(self):
        self.assertIn("wallet-identity-overlap", self.codes(self.pair(version_interval={"min": "snapshot-a", "max": None})))
        self.assertIn("wallet-version-interval", self.codes(self.pair(version_interval={"min": "3", "max": "2"})))

    def test_oversized_numeric_version_is_bounded_and_fails_closed(self):
        self.assertIn("wallet-identity-overlap", self.codes(self.pair(
            version_interval={"min": "9" * 5000, "max": None})))

    def test_distinct_source_snapshots_cannot_prove_disjoint_versions(self):
        catalog = self.pair()
        left, right = catalog.wallets
        left.data["version_interval"] = {"min": "source-abc", "max": "source-abc"}
        right.data["version_interval"] = {"min": "source-def", "max": "source-def"}
        self.assertIn("wallet-identity-overlap", self.codes(catalog))

    def test_alias_normalization_catches_ambiguous_product_spelling(self):
        self.assertIn("wallet-alias-ambiguity", self.codes(self.pair(product_id="other-wallet", aliases=["  ＳＡＭＰＬＥ wallet  "])))
        self.assertNotIn("wallet-alias-ambiguity", self.codes(self.pair(product_id="other-wallet", aliases=["Sample Wallet"], mode_id="private-key-imported")))

    def test_disjoint_platforms_and_versions_can_reuse_alias(self):
        self.assertNotIn("wallet-alias-ambiguity", self.codes(self.pair(product_id="other", aliases=["Sample Wallet"], platform="ios")))
        self.assertNotIn("wallet-alias-ambiguity", self.codes(self.pair(product_id="other", aliases=["Sample Wallet"], version_interval={"min": "3", "max": "4"})))

    def test_cross_platform_scope_overlaps_concrete_platform(self):
        self.assertIn("wallet-identity-overlap", self.codes(self.pair(platform="cross-platform")))

    def test_normalized_duplicate_aliases_in_one_record_are_rejected(self):
        self.assertIn("wallet-alias-ambiguity", self.codes(self.pair(aliases=["My Wallet", " my  wallet "])))

    def test_documented_simultaneous_modes_preserve_different_recovery_material(self):
        wallets = {r.id: r.data for r in load_catalog(ROOT).wallets}
        cases = {
            "metamask-social-login": (True, False, None),
            "coinbase-wallet": (False, True, None),
            "coinbase-wallet-smart-recovery": (True, False, None),
            "okx-wallet-mpc": (False, False, None),
            "keplr-social-login": (False, False, None),
            "guarda": (False, False, None),
            "guarda-mnemonic-import": (False, True, None),
            "keystone-shamir": (True, False, "slip39-share"),
        }
        for identifier, expected in cases.items():
            with self.subTest(identifier=identifier):
                self.assertIn(identifier, set(wallets))
                data = wallets[identifier]
                self.assertEqual((data["generates_mnemonic"], data["import_only"], data["scheme_id"]), expected)
                self.assertNotEqual(data["status"], "verified")

    def test_network_guidance_does_not_claim_generation_or_recovery(self):
        catalog = load_catalog(ROOT)
        profiles = [r for r in catalog.wallets if r.data["mode_id"] == "network-search-guidance"]
        self.assertEqual(len(profiles), 22)
        for record in profiles:
            self.assertFalse(record.data["generates_mnemonic"])
            self.assertFalse(record.data["import_only"])
            self.assertEqual(record.data["status"], "documented")
        self.assertTrue(all(r.data["status"] != "verified" for r in profiles))

    def test_mobile_app_scope_overlaps_mobile_not_web(self):
        for platform, overlaps in (("ios", True), ("android", True), ("cross-platform", True), ("web", False)):
            with self.subTest(platform=platform):
                catalog = self.pair(platform=platform)
                catalog.wallets[0].data["platform"] = "mobile-app"
                codes = self.codes(catalog)
                self.assertNotIn("schema", codes)
                self.assertEqual("wallet-identity-overlap" in codes, overlaps)

    def test_okx_social_login_has_own_evidenced_nonselectable_mode(self):
        catalog = load_catalog(ROOT)
        wallets = {r.id: r.data for r in catalog.wallets}
        self.assertIn("okx-wallet-social-login", set(wallets))
        data = wallets["okx-wallet-social-login"]
        self.assertEqual(data["mode_id"], "social-login")
        self.assertEqual(data["status"], "documented")
        self.assertFalse(data["generates_mnemonic"])
        self.assertFalse(data["import_only"])
        self.assertIsNone(data["scheme_id"])
        text = " ".join(data["limitations"])
        for term in ("Google", "Apple", "email", "manual", "underlying mnemonic"):
            self.assertIn(term, text)
        evidence = next(r.data for r in catalog.evidence if r.id == "wallet-okx-wallet")
        self.assertIn(data["id"], evidence["record_ids"])
        requirement = next(r.data for r in catalog.required_sets[0].requirements if r.id == "wallet-okx-wallet")
        self.assertIn(data["id"], requirement["record_ids"])

    def test_coinbase_app_modes_do_not_inherit_smart_wallet_web_scope(self):
        wallets = {r.id: r.data for r in load_catalog(ROOT).wallets}
        for identifier in ("coinbase-wallet", "coinbase-wallet-social-login"):
            self.assertEqual(wallets[identifier]["platform"], "mobile-app")
            self.assertIn("not establish web", " ".join(wallets[identifier]["limitations"]))
        for identifier in ("coinbase-wallet-passkey", "coinbase-wallet-smart-recovery"):
            self.assertEqual(wallets[identifier]["platform"], "web")

    def test_exodus_screen_protection_is_not_passkey_availability(self):
        catalog = load_catalog(ROOT)
        wallet = next(r.data for r in catalog.wallets if r.id == "exodus-passkey")
        evidence = next(r.data for r in catalog.evidence if r.id == "wallet-exodus")
        for text in (" ".join(wallet["limitations"]), evidence["claim"]):
            self.assertNotIn("Web3 Wallet lacks that feature", text)
            self.assertIn("screen-recording", text)
            self.assertIn("not passkey", text)

    def test_current_manifest_terminal_does_not_close_task16_cake_inventory(self):
        # This tests the Task15 boundary, NOT completeness of current Cake modes.
        note = (ROOT / "docs/research/batches/named-wallets-networks.md").read_text(encoding="utf-8")
        self.assertIn("163/163", note)
        self.assertIn("current-manifest mechanics only", note)
        self.assertIn("cannot close Task16", note)
        self.assertIn("generic Cake requirement predates Task15", note)


if __name__ == "__main__":
    unittest.main()
