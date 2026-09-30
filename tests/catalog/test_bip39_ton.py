"""Real Task 10 catalogue contracts; diagnostics never print recovery words."""

from pathlib import Path
import hashlib
import hmac
import json
import unicodedata
import unittest

from tools.catalog.loader import load_catalog
from tools.catalog.generator import render_catalog
from tools.catalog.validator import validate_catalog

ROOT = Path(__file__).resolve().parents[2]
LANGUAGES = ('en', 'ja', 'ko', 'es', 'zh-hans', 'zh-hant', 'fr', 'it', 'cs', 'pt')
DICTIONARIES = {'bip39-' + language for language in LANGUAGES}
SCHEMES = {'bip39', 'ton-native', 'ton-multichain-bip39'}
WALLETS = {'tonkeeper-classic', 'tonkeeper-multichain', 'gram-wallet',
           'mytonwallet', 'ton-space', 'tonhub', 'openmask'}
PUBLIC = json.loads((ROOT / 'tests/catalog/fixtures/public/bip39-ton.json').read_text('utf-8'))


class Bip39TonTests(unittest.TestCase):
    def test_batch_metadata_renders_both_locales(self):
        catalog = load_catalog(ROOT)
        for locale in ('en', 'ru'):
            rendered = render_catalog(catalog, locale)
            self.assertIn('ton-multichain-bip39', rendered)
            self.assertIn('gram-wallet', rendered)

    def test_required_batch_records_exist_and_have_terminal_evidence(self):
        catalog = load_catalog(ROOT)
        for records, expected in ((catalog.dictionaries, DICTIONARIES),
                                  (catalog.schemes, SCHEMES), (catalog.wallets, WALLETS)):
            missing = expected - {record.id for record in records}
            self.assertFalse(missing, 'Missing batch IDs: ' + ', '.join(sorted(missing)))
        errors = [str(f) for f in validate_catalog(catalog, allow_incomplete_required=True)
                  if f.severity == 'error']
        self.assertEqual(errors, [])

    def test_scheme_lengths_and_ton_modes_remain_distinct(self):
        catalog = load_catalog(ROOT)
        schemes = {record.id: record.data for record in catalog.schemes}
        self.assertTrue(SCHEMES <= schemes.keys(), 'Missing BIP39/TON schemes')
        self.assertEqual(tuple(schemes['bip39']['supported_lengths']), (12, 15, 18, 21, 24))
        self.assertEqual(tuple(schemes['ton-native']['supported_lengths']), (24,))
        self.assertEqual(tuple(schemes['ton-multichain-bip39']['supported_lengths']), (12, 24))
        wallets = {record.id: record.data for record in catalog.wallets}
        self.assertTrue(WALLETS <= wallets.keys(), 'Missing TON wallets')
        self.assertEqual(wallets['tonkeeper-classic']['scheme_id'], 'ton-native')
        self.assertEqual(wallets['tonkeeper-multichain']['scheme_id'], 'ton-multichain-bip39')
        self.assertEqual(wallets['tonkeeper-classic']['product_id'],
                         wallets['tonkeeper-multichain']['product_id'])
        self.assertNotEqual(wallets['tonkeeper-classic']['mode_id'],
                            wallets['tonkeeper-multichain']['mode_id'])

    def test_exact_upstream_bytes_counts_normalization_and_license_gates(self):
        dictionaries = {r.id: r for r in load_catalog(ROOT).dictionaries}
        self.assertTrue(DICTIONARIES <= dictionaries.keys(), 'Missing BIP39 dictionaries')
        for language in LANGUAGES:
            with self.subTest(language=language):
                record = dictionaries['bip39-' + language]
                data, blob = record.data, record.wordlist_bytes
                self.assertIsNotNone(blob)
                expected = PUBLIC['wordlists'][language]
                self.assertEqual(hashlib.sha256(blob).hexdigest(), expected['sha256'])
                self.assertEqual(len(blob), expected['bytes'])
                words = blob.decode('utf-8').splitlines()
                self.assertEqual(len(words), 2048)
                self.assertEqual(len({unicodedata.normalize('NFKD', w) for w in words}), 2048)
                self.assertTrue(blob.endswith(b'\n') and b'\r' not in blob)
                self.assertTrue(unicodedata.normalize('NFKD', blob.decode()).encode() == blob,
                                'Stored dictionary is not already NFKD')
                self.assertEqual(data['normalization'], 'NFKD')
                self.assertEqual(data['source']['revision'], PUBLIC['bip39_revision'])
                self.assertEqual(data['sha256'], expected['sha256'])
                self.assertEqual(data['license']['repository_redistribution'], 'allowed')
                self.assertEqual(data['license']['signpath_compatible'], 'compatible')
                self.assertEqual(data['license']['spdx_or_name'], 'MIT')

    def test_independent_public_bip39_known_answers_all_ten_languages(self):
        dictionaries = {r.id: r for r in load_catalog(ROOT).dictionaries}
        self.assertTrue(DICTIONARIES <= dictionaries.keys(), 'Missing BIP39 dictionaries')
        self.assertEqual(len(PUBLIC['bip39_vectors']), 240)
        self.assertEqual({v['language'] for v in PUBLIC['bip39_vectors']}, set(LANGUAGES))
        for vector in PUBLIC['bip39_vectors']:
            with self.subTest(language=vector['language'], index=vector['upstream_index']):
                words = dictionaries['bip39-' + vector['language']].wordlist_bytes.decode().splitlines()
                entropy = bytes.fromhex(vector['entropy'])
                bits = ''.join(f'{byte:08b}' for byte in entropy)
                bits += f'{hashlib.sha256(entropy).digest()[0]:08b}'[:len(entropy) // 4]
                sentence = ' '.join(words[int(bits[i:i+11], 2)] for i in range(0, len(bits), 11))
                normalized = unicodedata.normalize('NFKD', sentence).encode()
                composed = unicodedata.normalize('NFC', sentence)
                self.assertTrue(unicodedata.normalize('NFKD', composed).encode() == normalized,
                                'Composed/decomposed public sentence differs after NFKD')
                if vector['language'] == 'ja':
                    self.assertTrue(unicodedata.normalize('NFKD', sentence.replace(' ', '\u3000')).encode()
                                    == normalized, 'Japanese ideographic separator normalization mismatch')
                self.assertTrue(hashlib.sha256(normalized).hexdigest() == vector['mnemonic_nfkd_sha256'],
                                'Public mnemonic fingerprint mismatch')
                # Offline research test only; no production key/phrase API is introduced.
                seed = hashlib.pbkdf2_hmac('sha512', normalized, b'mnemonicTREZOR', 2048)
                self.assertTrue(seed.hex() == vector['seed'], 'Public seed known answer mismatch')

    def test_ton_public_known_answers_are_not_bip39_seed_derivation(self):
        dictionaries = {r.id: r for r in load_catalog(ROOT).dictionaries}
        self.assertTrue('bip39-en' in dictionaries, 'Missing TON shared English dictionary')
        words = dictionaries['bip39-en'].wordlist_bytes.decode().splitlines()
        self.assertEqual(len(PUBLIC['ton_vectors']), 5)
        for index, vector in enumerate(PUBLIC['ton_vectors']):
            with self.subTest(index=index):
                self.assertEqual(len(vector['word_indices']), 24)
                sentence = ' '.join(words[i] for i in vector['word_indices']).encode()
                entropy = hmac.digest(sentence, b'', 'sha512')
                seed = hashlib.pbkdf2_hmac('sha512', entropy, b'TON default seed', 100000)[:32]
                self.assertTrue(seed.hex() == vector['seed32'], 'TON public seed known answer mismatch')
                self.assertEqual(hashlib.pbkdf2_hmac('sha512', entropy, b'TON seed version', 390)[0], 0)
                self.assertNotEqual(seed, hashlib.pbkdf2_hmac('sha512', sentence, b'mnemonic', 2048)[:32])

    def test_required_manifest_modes_and_evidence_are_closed_for_this_batch(self):
        catalog = load_catalog(ROOT)
        records = {r.id: r for r in (*catalog.dictionaries, *catalog.schemes, *catalog.wallets)}
        evidence = {r.id: r for r in catalog.evidence}
        requirements = {i.id: i for r in catalog.required_sets for i in r.requirements}
        for kind, ids in (('dictionary', DICTIONARIES), ('scheme', SCHEMES), ('wallet', WALLETS)):
            for identifier in sorted(ids):
                with self.subTest(record=identifier):
                    self.assertTrue(identifier in records, 'Missing batch record: ' + identifier)
                    item = requirements[kind + '-' + identifier].data
                    self.assertEqual(item['research_state'], 'terminal')
                    self.assertIn(identifier, item['record_ids'])
                    self.assertEqual(item['status'], records[identifier].data['status'])
                    for eid in records[identifier].data['evidence_ids']:
                        source = evidence[eid].data
                        self.assertIn(identifier, source['record_ids'])
                        self.assertNotIn('example.invalid', source['url'])
                        self.assertEqual(source['verified_on'], '2026-09-29')
                        if source['source_type'] == 'official-source':
                            self.assertRegex(source['revision'], r'^[a-f0-9]{40}$')
                    for eid in records[identifier].data.get('test_vector_ids', ()):
                        self.assertEqual(evidence[eid].data['source_type'], 'public-test-vector')
        wallets = [r.data for r in catalog.wallets if r.id in WALLETS or r.id == 'mytonwallet-native']
        identities = set()
        for wallet in wallets:
            # This batch deliberately claims only a singleton source revision or a
            # bounded documentation snapshot; no unproven open-ended version ranges.
            self.assertEqual(wallet['version_interval']['min'], wallet['version_interval']['max'])
            key = (wallet['product_id'], wallet['platform'], wallet['version_interval']['min'], wallet['mode_id'])
            self.assertNotIn(key, identities, 'Overlapping concrete wallet mode')
            identities.add(key)
        self.assertTrue('mytonwallet-native' in records, 'Missing simultaneous TON-native mode')
        native, multi = records['mytonwallet-native'].data, records['mytonwallet'].data
        self.assertEqual(native['version_interval'], multi['version_interval'])
        self.assertEqual(native['product_id'], multi['product_id'])
        self.assertNotEqual(native['mode_id'], multi['mode_id'])
        self.assertEqual(native['scheme_id'], 'ton-native')
        self.assertEqual(multi['scheme_id'], 'ton-multichain-bip39')
        for uncertain in ('gram-wallet', 'ton-space'):
            self.assertEqual(records[uncertain].data['status'], 'documented')
            self.assertIsNone(records[uncertain].data['scheme_id'])
            self.assertTrue(records[uncertain].data['limitations'])
