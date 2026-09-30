"""Contract for the complete Windows v1 research obligation."""

import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "catalog" / "required" / "windows-v1.json"
STATUSES = {"verified", "documented", "blocked", "no-mnemonic-confirmed"}


def requirements():
    return json.loads(MANIFEST.read_text(encoding="utf-8"))["requirements"]


class RequiredSetTests(unittest.TestCase):
    def test_required_manifest_contains_every_named_product(self):
        by_id = {item["id"] for item in requirements()}
        expected = {
            "dictionary-bip39-" + code for code in
            ("en", "ja", "ko", "es", "zh-hans", "zh-hant", "fr", "it", "cs", "pt")
        }
        expected |= {"dictionary-monero-" + code for code in
                     ("en", "de", "es", "fr", "it", "nl", "pt", "ru", "ja", "zh-hans", "eo", "jbo", "en-old")}
        expected |= {"dictionary-polyseed-" + code for code in
                     ("en", "ja", "ko", "es", "fr", "it", "cs", "pt", "zh-hans", "zh-hant")}
        expected |= {"dictionary-" + name for name in
                     ("slip39-en", "electrum-v1-en", "pgp-even", "pgp-odd", "zano-en", "sia-legacy")}
        expected |= {"scheme-" + name for name in (
            "bip39", "ton-native", "ton-multichain-bip39", "monero-legacy", "mymonero",
            "polyseed", "slip39-share", "algorand-25", "cardano-byron", "cardano-icarus",
            "cardano-hardware", "cardano-daedalus-27", "electrum-v1", "electrum-v2",
            "substrate-bip39", "decred-pgp33", "decred-bip39", "cake-decred-15",
            "zano-modern", "zano-legacy-24", "zano-legacy-25", "sia-bip39",
            "sia-legacy-28", "sia-legacy-29", "zcash-bip39", "zcash-non-mnemonic",
            "chia-bip39")}
        expected |= {"wallet-" + name for name in (
            "tonkeeper-classic", "tonkeeper-multichain", "gram-wallet", "mytonwallet",
            "ton-space", "tonhub", "openmask", "phantom", "solflare", "backpack", "glow",
            "cake-wallet", "trust-wallet", "metamask", "coinbase-wallet", "exodus",
            "atomic-wallet", "onekey", "ledger", "trezor", "okx-wallet", "bitget-wallet",
            "safepal", "tangem-seed", "keystone", "bitbox02", "ellipal", "coinomi",
            "guarda", "tokenpocket", "imtoken", "rabby", "rainbow", "zerion",
            "electrum", "sparrow", "bluewallet", "coldcard", "blockstream-jade",
            "passport", "seedsigner", "keplr", "leap", "cosmostation", "yoroi",
            "daedalus", "lace", "eternl", "nami", "typhon", "monero-gui-cli",
            "mymonero", "feather", "exodus-monero", "pera-wallet", "defly",
            "decrediton", "zano-wallet", "cake-wallet-zano", "siad", "sia-ui",
            "walletd", "zallet", "zcash-official", "chia-wallet", "polkadot-js",
            "subwallet", "talisman", "temple", "kukai")}
        expected |= {"network-" + name for name in (
            "bitcoin", "ethereum", "base", "bnb-chain", "polygon", "avalanche",
            "arbitrum", "solana", "tron", "cosmos", "tezos", "polkadot", "kusama",
            "cardano", "algorand", "monero", "zcash", "chia", "decred", "zano", "sia", "ton")}
        self.assertEqual(expected - by_id, set())

    def test_historical_is_not_a_support_status(self):
        for item in requirements():
            with self.subTest(item=item["id"]):
                self.assertIs(type(item["historical"]), bool)
                self.assertNotEqual(item["status"], "historical")
                self.assertIn(item["status"], STATUSES | {None})
                if item["status"] is None:
                    self.assertEqual(item["research_state"], "pending")
                    self.assertEqual(item["record_ids"], [])
                else:
                    self.assertEqual(item["research_state"], "terminal")
                    self.assertTrue(item["record_ids"])

    def test_required_ids_are_unique(self):
        ids = [item["id"] for item in requirements()]
        self.assertEqual(len(ids), len(set(ids)))


if __name__ == "__main__":
    unittest.main()
