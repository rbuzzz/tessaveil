"""Public format projections only; never user phrases or wallet recovery."""
from pathlib import Path
import hashlib
import hmac
import json
import unittest

from tools.catalog.loader import load_catalog
from tools.catalog.validator import validate_catalog

ROOT = Path(__file__).resolve().parents[2]
DICTIONARIES = {'electrum-v1-en', 'pgp-even', 'pgp-odd'}
SCHEMES = {'electrum-v1', 'electrum-v2', 'substrate-bip39', 'decred-pgp33',
           'decred-bip39', 'cake-decred-15'}
WALLETS = {'electrum', 'polkadot-js', 'subwallet', 'talisman', 'decrediton',
           'cake-wallet-decred'}


class ElectrumSubstrateDecredTests(unittest.TestCase):
    def batch(self):
        catalog = load_catalog(ROOT)
        records = {r.id: r for r in (*catalog.dictionaries, *catalog.schemes, *catalog.wallets)}
        self.assertFalse((DICTIONARIES | SCHEMES | WALLETS) - records.keys(),
                         'Missing Task13 research profiles')
        return catalog, records

    def test_required_profiles_are_terminal_and_not_inferred_selectable(self):
        catalog, records = self.batch()
        required = {r.id: r.data for s in catalog.required_sets for r in s.requirements}
        for kind, identifiers in [('dictionary', DICTIONARIES), ('scheme', SCHEMES), ('wallet', WALLETS)]:
            for identifier in identifiers:
                self.assertEqual(required[kind + '-' + identifier]['research_state'], 'terminal')
                self.assertEqual(required[kind + '-' + identifier]['status'], records[identifier].data['status'])
        for identifier in WALLETS:
            row = records[identifier].data
            self.assertIn(row['status'], ('documented', 'blocked'))
            self.assertTrue(row['limitations'])
            self.assertEqual(row['version_interval']['min'], row['version_interval']['max'])
        self.assertFalse([f for f in validate_catalog(catalog, allow_incomplete_required=True)
                          if f.severity == 'error'])

    def test_pgp33_alternates_position_halves_including_checksum(self):
        _, records = self.batch()
        scheme = records['decred-pgp33'].data
        self.assertEqual(tuple(scheme['supported_lengths']), (33,))
        self.assertEqual(tuple(scheme['dictionary_ids']), ('pgp-even', 'pgp-odd'))
        rules = scheme['position_rules']
        self.assertIn('positions 1,3,5,7,9,11,13,15,17,19,21,23,25,27,29,31,33: pgp-even', rules)
        self.assertIn('positions 2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32: pgp-odd', rules)
        halves = [records[i].wordlist_bytes.decode().splitlines() for i in ('pgp-even', 'pgp-odd')]
        self.assertEqual([len(set(words)) for words in halves], [256, 256])
        self.assertFalse(set(halves[0]) & set(halves[1]))
        for identifier, expected in [('pgp-even', '37a65f88512467edd12a1ab3eeb5f4328230e86711a8efde6333361ce10f4fcf'),
                                     ('pgp-odd', 'c2f23c2233d4d7291107e8f796c374d0cb1fb30c1391bcb4f6480243de8ebf5a')]:
            self.assertEqual(hashlib.sha256(records[identifier].wordlist_bytes).hexdigest(), expected)
        fixture = json.loads((ROOT / 'tests/catalog/fixtures/public/electrum-substrate-decred.json').read_text('utf-8'))
        self.assertTrue(fixture['pgp33'])
        self.assertTrue(all(len(v['indices']) == 33 for v in fixture['pgp33']))
        for vector in [*fixture['pgp33'], *fixture['pgp_public']]:
            seed = bytes.fromhex(vector['seed_hex'])
            checksum = hashlib.sha256(hashlib.sha256(seed).digest()).digest()[0]
            indices = [*seed, checksum]
            self.assertEqual(indices, vector['indices'])
            sentence = ' '.join(halves[pos % 2][value] for pos, value in enumerate(indices))
            self.assertEqual(hashlib.sha256(sentence.encode()).hexdigest(), vector['sentence_sha256'])
            for pos, word in enumerate(sentence.split()):
                self.assertNotIn(word, halves[1 - pos % 2])

    def test_format_identity_does_not_follow_shared_vocabulary(self):
        _, records = self.batch()
        for identifier in ('electrum-v2', 'substrate-bip39', 'decred-bip39'):
            self.assertEqual(tuple(records[identifier].data['dictionary_ids']), ('bip39-en',))
        self.assertEqual(tuple(records['electrum-v1'].data['dictionary_ids']), ('electrum-v1-en',))
        for identifier in SCHEMES:
            self.assertTrue(records[identifier].data['no_key_derivation'])
            self.assertTrue(records[identifier].data['no_complete_phrase_validation'])
        self.assertNotEqual(records['decrediton'].data['scheme_id'], records['cake-wallet-decred'].data['scheme_id'])

    def test_public_vectors_preserve_electrum_and_substrate_semantics(self):
        _, records = self.batch()
        fixture = json.loads((ROOT / 'tests/catalog/fixtures/public/electrum-substrate-decred.json').read_text('utf-8'))
        words = records['bip39-en'].wordlist_bytes.decode().splitlines()
        for vector in fixture['electrum_v2']:
            sentence = ' '.join(words[i] for i in vector['indices']).encode()
            self.assertTrue(hmac.new(b'Seed version', sentence, 'sha512').hexdigest().startswith(vector['prefix']))
            seed = hashlib.pbkdf2_hmac('sha512', sentence, b'electrum' + vector['passphrase'].encode(), 2048)
            self.assertEqual(hashlib.sha256(seed).hexdigest(), vector['seed_sha256'])
            self.assertNotEqual(seed, hashlib.pbkdf2_hmac('sha512', sentence, b'mnemonic' + vector['passphrase'].encode(), 2048))
        for vector in fixture['substrate']:
            entropy = bytes.fromhex(vector['entropy_hex'])
            entropy_bits = len(entropy) * 8
            check_bits = entropy_bits // 32
            payload = (int.from_bytes(entropy, 'big') << check_bits) | (hashlib.sha256(entropy).digest()[0] >> (8-check_bits))
            count = (entropy_bits + check_bits) // 11
            indices = [(payload >> (11*(count-1-i))) & 2047 for i in range(count)]
            self.assertEqual(indices, vector['indices'])
            sentence = ' '.join(words[i] for i in indices).encode()
            seed = hashlib.pbkdf2_hmac('sha512', entropy, b'mnemonicSubstrate', 2048)
            self.assertEqual(hashlib.sha256(seed).hexdigest(), vector['seed_sha256'])
            self.assertNotEqual(seed, hashlib.pbkdf2_hmac('sha512', sentence, b'mnemonicSubstrate', 2048))

    def test_cake_native_and_current_creation_are_separate_nonselectable_modes(self):
        catalog, records = self.batch()
        native = records['cake-wallet-decred'].data
        current = records.get('cake-wallet-decred-bip39')
        self.assertIsNotNone(current, 'Current BIP39 creation must not overwrite native15 import')
        self.assertTrue(native['import_only'])
        self.assertFalse(native['generates_mnemonic'])
        self.assertTrue(current.data['generates_mnemonic'])
        self.assertEqual(current.data['status'], 'blocked')
        self.assertNotEqual(native['scheme_id'], current.data['scheme_id'])
        self.assertEqual(tuple(records['cake-decred-15'].data['supported_lengths']), (15,))
        self.assertEqual(tuple(records['cake-decred-15'].data['dictionary_ids']), ('bip39-en',))
        self.assertEqual(records['cake-decred-15'].data['external_secret']['kind'], 'none')
        self.assertEqual(tuple(records[current.data['scheme_id']].data['supported_lengths']), (12, 24))
        self.assertEqual(tuple(records['polkadot-js'].data['network_ids']), ('polkadot', 'kusama'))
        # Every source-only profile is nonselectable, including additional modes.
        extra = {'electrum-v1-import', 'electrum-bip39-import', 'cake-wallet-decred-bip39'}
        for wallet in catalog.wallets:
            if wallet.id in WALLETS | extra:
                self.assertNotEqual(wallet.data['status'], 'verified')

    def test_unresolved_electrum_legacy_license_does_not_bundle_bytes(self):
        catalog, records = self.batch()
        record = records['electrum-v1-en']
        self.assertEqual(record.data['status'], 'blocked')
        self.assertIsNone(record.wordlist_bytes)
        self.assertIsNone(record.data['wordlist_path'])
        self.assertEqual(record.data['license']['repository_redistribution'], 'unclear')
        self.assertEqual(record.data['license']['signpath_compatible'], 'pending')
        self.assertFalse((ROOT / 'wordlists/electrum-v1-en').exists())
        blocked = {f.location for f in validate_catalog(catalog, require_release_ready=True)
                   if f.code == 'required-blocked'}
        self.assertIn('dictionary-electrum-v1-en', blocked)
