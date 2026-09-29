"""Task14 format boundaries; public metadata only, never wallet recovery."""
from pathlib import Path
import hashlib
import json
import unittest

from tools.catalog.loader import load_catalog
from tools.catalog.validator import validate_catalog

ROOT = Path(__file__).resolve().parents[2]
DICTIONARIES = {'zano-en', 'sia-legacy'}
SCHEMES = {'zano-modern', 'zano-legacy-24', 'zano-legacy-25', 'sia-bip39',
           'sia-legacy-28', 'sia-legacy-29', 'zcash-bip39', 'zcash-non-mnemonic', 'chia-bip39'}
WALLETS = {'zano-wallet', 'cake-wallet-zano', 'sia-walletd', 'sia-ui', 'siad',
           'zallet', 'zcash-official', 'chia-wallet'}


class ZanoSiaZcashChiaTests(unittest.TestCase):
    def batch(self):
        catalog = load_catalog(ROOT)
        records = {r.id: r for r in (*catalog.dictionaries, *catalog.schemes, *catalog.wallets)}
        self.assertFalse((DICTIONARIES | SCHEMES | WALLETS) - records.keys(), 'Missing Task14 profiles')
        return catalog, records

    def test_required_history_has_terminal_support_and_wallets_stay_nonselectable(self):
        catalog, records = self.batch()
        required = {r.id: r.data for s in catalog.required_sets for r in s.requirements}
        for kind, ids in [('dictionary', DICTIONARIES), ('scheme', SCHEMES), ('wallet', WALLETS)]:
            for identifier in ids:
                requirement = 'wallet-walletd' if identifier == 'sia-walletd' else kind + '-' + identifier
                self.assertEqual(required[requirement]['research_state'], 'terminal')
                self.assertEqual(required[requirement]['status'], records[identifier].data['status'])
        for identifier in WALLETS:
            row = records[identifier].data
            self.assertNotEqual(row['status'], 'verified')
            self.assertTrue(row['limitations'])
            self.assertEqual(row['version_interval']['min'], row['version_interval']['max'])
        for identifier in ('zano-legacy-24', 'zano-legacy-25', 'sia-legacy-28', 'sia-legacy-29', 'sia-ui', 'siad'):
            self.assertTrue(records[identifier].data['historical'])
        self.assertFalse([f for f in validate_catalog(catalog, allow_incomplete_required=True) if f.severity == 'error'])

    def test_lengths_and_non_mnemonic_material_cannot_be_conflated(self):
        _, records = self.batch()
        for identifier, lengths in [('zano-modern', (26,)), ('zano-legacy-24', (24,)),
                                    ('zano-legacy-25', (25,)), ('sia-bip39', (12,)),
                                    ('sia-legacy-28', (28,)), ('sia-legacy-29', (29,)),
                                    ('chia-bip39', (24,))]:
            self.assertEqual(tuple(records[identifier].data['supported_lengths']), lengths)
        non = records['zcash-non-mnemonic'].data
        self.assertEqual(non['status'], 'no-mnemonic-confirmed')
        self.assertFalse(non['dictionary_ids'])
        self.assertFalse(non['supported_lengths'])
        for identifier in SCHEMES:
            self.assertTrue(records[identifier].data['no_key_derivation'])
            self.assertTrue(records[identifier].data['no_complete_phrase_validation'])
        self.assertEqual(records['sia-walletd'].data['scheme_id'], 'sia-bip39')
        self.assertTrue(any('legacy' in s.lower() for s in records['sia-walletd'].data['limitations']))
        self.assertNotEqual(records['zano-modern'].data['dictionary_ids'], records['sia-bip39'].data['dictionary_ids'])

    def test_unresolved_zano_list_is_not_bundled(self):
        _, records = self.batch()
        row = records['zano-en']
        self.assertEqual(row.data['status'], 'blocked')
        self.assertIsNone(row.wordlist_bytes)
        self.assertEqual(row.data['license']['repository_redistribution'], 'unclear')
        self.assertEqual(row.data['license']['signpath_compatible'], 'pending')
        self.assertFalse((ROOT / 'wordlists/zano-en').exists())

    def test_sia_dictionary_order_and_public_codec_vectors(self):
        _, records = self.batch()
        row = records['sia-legacy']
        words = row.wordlist_bytes.decode().splitlines()
        self.assertEqual(len(words), 1626)
        self.assertEqual(len({w[:3] for w in words}), 1626)
        fixture = json.loads((ROOT / 'tests/catalog/fixtures/public/zano-sia-zcash-chia.json').read_text('utf-8'))
        for vector in fixture['sia_codec']:
            entropy = bytes.fromhex(vector['bytes_hex'])
            number = sum((b + 1) * 256**i for i, b in enumerate(entropy)) - 1
            indices = []
            while number >= 1626:
                indices.append(number % 1626)
                number = (number - 1626) // 1626
            indices.append(number)
            self.assertEqual(indices, vector['indices'])
        self.assertEqual(hashlib.sha256(row.wordlist_bytes).hexdigest(), fixture['sia_dictionary_sha256'])

    def test_public_chia_empty_passphrase_vectors_and_zcash_library_vector(self):
        _, records = self.batch()
        fixture = json.loads((ROOT / 'tests/catalog/fixtures/public/zano-sia-zcash-chia.json').read_text('utf-8'))
        words = records['bip39-en'].wordlist_bytes.decode().splitlines()
        self.assertEqual(len(fixture['chia']), 24)
        for vector in fixture['chia']:
            entropy = bytes.fromhex(vector['entropy_hex'])
            check_bits = len(entropy) // 4
            value = (int.from_bytes(entropy, 'big') << check_bits) | (hashlib.sha256(entropy).digest()[0] >> (8-check_bits))
            count = (len(entropy)*8 + check_bits) // 11
            indices = [(value >> (11*(count-1-i))) & 2047 for i in range(count)]
            self.assertEqual(indices, vector['indices'])
            sentence = ' '.join(words[i] for i in indices).encode()
            seed = hashlib.pbkdf2_hmac('sha512', sentence, b'mnemonic', 2048)
            self.assertEqual(hashlib.sha256(seed).hexdigest(), vector['seed_sha256'])
            self.assertNotEqual(seed, hashlib.pbkdf2_hmac('sha512', sentence, b'mnemonicTREZOR', 2048))
        z = fixture['bip0039_empty']
        sentence = ' '.join(words[i] for i in z['indices']).encode()
        self.assertEqual(hashlib.pbkdf2_hmac('sha512', sentence, b'mnemonic', 2048).hex(), z['seed_hex'])
        for identifier in ('chia-bip39', 'zcash-bip39', 'sia-bip39'):
            self.assertEqual(records[identifier].data['external_secret']['kind'], 'none')

    def test_cake_bip39_creation_does_not_overwrite_native_import(self):
        _, records = self.batch()
        native = records['cake-wallet-zano'].data
        current = records['cake-wallet-zano-bip39'].data
        self.assertTrue(native['import_only'])
        self.assertFalse(native['generates_mnemonic'])
        self.assertTrue(current['generates_mnemonic'])
        self.assertNotEqual(current['scheme_id'], native['scheme_id'])
        self.assertEqual(current['status'], 'blocked')
