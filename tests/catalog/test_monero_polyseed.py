"""Offline Monero-family research contracts. Never print recovery words."""
from pathlib import Path
import hashlib
import json
import unicodedata
import zlib
import unittest
from tools.catalog.loader import load_catalog
from tools.catalog.validator import validate_catalog
from tools.catalog.generator import render_catalog

ROOT = Path(__file__).resolve().parents[2]
MONERO = ('en', 'de', 'es', 'fr', 'it', 'nl', 'pt', 'ru', 'ja', 'zh-hans', 'eo', 'jbo', 'en-old')
POLYSEED = ('en', 'ja', 'ko', 'es', 'fr', 'it', 'cs', 'pt', 'zh-hans', 'zh-hant')
DICTIONARIES = {'monero-' + x for x in MONERO} | {'polyseed-' + x for x in POLYSEED}
SCHEMES = {'monero-legacy', 'mymonero-13', 'polyseed-16'}
WALLETS = {'monero-gui-cli', 'mymonero', 'feather', 'cake-wallet-monero', 'exodus-monero-export'}

class MoneroPolyseedTests(unittest.TestCase):
    def test_profiles_without_aliases_render_without_trailing_spaces(self):
        catalog = load_catalog(ROOT)
        for locale in ('en', 'ru'):
            self.assertTrue(all(line == line.rstrip() for line in render_catalog(catalog, locale).splitlines()),
                            'Empty optional profile fields leave trailing spaces')

    def test_required_ids_are_available_without_bip39_substitution(self):
        catalog = load_catalog(ROOT)
        for records, expected in ((catalog.dictionaries, DICTIONARIES), (catalog.schemes, SCHEMES), (catalog.wallets, WALLETS)):
            missing = expected - {r.id for r in records}
            self.assertFalse(missing, 'Missing batch IDs: ' + ', '.join(sorted(missing)))
        schemes = {r.id: r.data for r in catalog.schemes}
        for identifier, length in [('monero-legacy', 25), ('mymonero-13', 13), ('polyseed-16', 16)]:
            self.assertEqual(tuple(schemes[identifier]['supported_lengths']), (length,))
            self.assertTrue(all(not d.startswith('bip39-') for d in schemes[identifier]['dictionary_ids']))

    def batch(self):
        catalog = load_catalog(ROOT)
        self.assertTrue(DICTIONARIES <= {r.id for r in catalog.dictionaries}, 'Missing Monero-family dictionaries')
        path = ROOT / 'tests/catalog/fixtures/public/monero-polyseed.json'
        self.assertTrue(path.is_file(), 'Missing public source-projection fixture')
        return catalog, json.loads(path.read_text('utf-8'))

    def test_exact_dictionary_bytes_counts_order_and_source_native_rules(self):
        catalog, fixture = self.batch()
        records = {r.id: r for r in catalog.dictionaries}
        self.assertEqual(set(fixture['wordlists']), DICTIONARIES)
        for identifier in sorted(DICTIONARIES):
            with self.subTest(dictionary=identifier):
                record = records[identifier]
                expected = fixture['wordlists'][identifier]
                blob = record.wordlist_bytes
                self.assertIsNotNone(blob)
                self.assertTrue(hashlib.sha256(blob).hexdigest() == expected['sha256'], 'Source word-list fingerprint mismatch')
                self.assertEqual(len(blob), expected['bytes'])
                words = blob.decode('utf-8').splitlines()
                count = 2048 if identifier.startswith('polyseed-') else 1626
                self.assertEqual(len(words), count)
                self.assertEqual(record.data['word_count'], count)
                self.assertEqual(record.data['sha256'], expected['sha256'])
                self.assertEqual(record.data['source']['revision'], expected['revision'])
                self.assertTrue(blob.endswith(b'\n') and b'\r' not in blob)
                for form in ('NFC', 'NFKD'):
                    self.assertEqual(len({unicodedata.normalize(form, w) for w in words}), count)
                if identifier.startswith('polyseed-'):
                    self.assertEqual(record.data['normalization'], 'NFKD')
                    self.assertTrue(unicodedata.normalize('NFKD', blob.decode()).encode() == blob)
                else:
                    self.assertEqual(record.data['normalization'], 'none')
                self.assertEqual(record.data['license']['repository_redistribution'], 'allowed')
                self.assertEqual(record.data['license']['signpath_compatible'], 'compatible')
                self.assertEqual(record.data['historical'], identifier == 'monero-en-old')
                verified = {'monero-en', 'monero-de', 'monero-pt', 'polyseed-en', 'polyseed-es'}
                self.assertEqual(record.data['status'], 'verified' if identifier in verified else 'documented')
                self.assertEqual(bool(record.data['test_vector_ids']), identifier in verified)
        self.assertNotEqual(records['monero-en-old'].wordlist_bytes, records['monero-en'].wordlist_bytes)
        # The upstream modified lists must never be silently replaced by BIP39.
        for lang in ('es', 'ja', 'cs'):
            self.assertNotEqual(records['polyseed-' + lang].wordlist_bytes, records['bip39-' + lang].wordlist_bytes)

    def test_public_monero_checksum_and_mymonero_entropy(self):
        catalog, fixture = self.batch()
        records = {r.id: r for r in catalog.dictionaries}
        for vector in fixture['legacy_vectors']:
            words = records[vector['dictionary']].wordlist_bytes.decode().splitlines()
            sentence = [words[i] for i in vector['indices']]
            payload, check = sentence[:-1], sentence[-1]
            prefix = fixture['wordlists'][vector['dictionary']]['prefix']
            checksum = zlib.crc32(''.join(w[:prefix] for w in payload).encode()) % len(payload)
            self.assertTrue(payload[checksum] == check, 'Public legacy checksum mismatch')
            self.assertTrue(hashlib.sha256(' '.join(sentence).encode()).hexdigest() == vector['sentence_sha256'])
            if 'entropy' in vector:
                output = bytearray()
                for offset in range(0, len(payload), 3):
                    a, b, c = vector['indices'][offset:offset+3]
                    value = a + 1626 * ((b-a) % 1626) + 1626**2 * ((c-b) % 1626)
                    output.extend(value.to_bytes(4, 'little'))
                self.assertTrue(output.hex() == vector['entropy'], 'MyMonero public entropy mismatch')

    def test_public_polyseed_words_checksum_and_embedded_data(self):
        catalog, fixture = self.batch()
        records = {r.id: r for r in catalog.dictionaries}
        for vector in fixture['polyseed_vectors']:
            words = records[vector['dictionary']].wordlist_bytes.decode().splitlines()
            idx = vector['indices']
            self.assertEqual(len(idx), 16)
            sentence = ' '.join(words[i] for i in idx)
            self.assertTrue(hashlib.sha256(sentence.encode()).hexdigest() == vector['sentence_sha256'])
            self.assertEqual(unicodedata.normalize('NFKD', unicodedata.normalize('NFC', sentence)), sentence)
            # GF(2^11), modulus x^11+x^3+1 (0x805); Monero coin flag is zero.
            result = 0
            for coefficient in reversed(idx):
                result = (result << 1) ^ (0x805 if result & 0x400 else 0)
                result ^= coefficient
            self.assertEqual(result, 0)
            bits = ''.join(f'{i >> 1:010b}' for i in idx[1:])
            secret = bytes(int(bits[i:i+8], 2) for i in range(0, 150, 8))
            extra = int(''.join(str(i & 1) for i in idx[1:]), 2)
            self.assertTrue(secret.hex() == vector['secret'], 'Public Polyseed secret mismatch')
            self.assertEqual(extra & 1023, vector['birthday'])
            self.assertEqual(extra >> 10, vector['features'])

    def test_batch_terminal_manifest_evidence_and_modes(self):
        catalog, fixture = self.batch()
        records = {r.id: r for r in (*catalog.dictionaries, *catalog.schemes, *catalog.wallets)}
        evidence = {r.id: r.data for r in catalog.evidence}
        requirements = {r.id: r.data for s in catalog.required_sets for r in s.requirements}
        mappings = {**{'dictionary-' + x: x for x in DICTIONARIES},
                    **{'wallet-' + x: x for x in WALLETS - {'cake-wallet-monero', 'exodus-monero-export'}},
                    'wallet-cake-wallet': 'cake-wallet-monero', 'wallet-exodus-monero': 'exodus-monero-export',
                    'scheme-monero-legacy': 'monero-legacy', 'scheme-mymonero': 'mymonero-13', 'scheme-polyseed': 'polyseed-16'}
        for requirement, identifier in mappings.items():
            self.assertEqual(requirements[requirement]['research_state'], 'terminal')
            self.assertIn(identifier, requirements[requirement]['record_ids'])
            self.assertEqual(requirements[requirement]['status'], records[identifier].data['status'])
        for identifier in DICTIONARIES | SCHEMES | set(fixture['wallets']):
            record = records[identifier].data
            for eid in record['evidence_ids']:
                self.assertIn(identifier, evidence[eid]['record_ids'])
                self.assertNotIn('example.invalid', evidence[eid]['url'])
                if evidence[eid]['source_type'] == 'official-source':
                    self.assertRegex(evidence[eid]['revision'], r'^[a-f0-9]{40}$')
        identities = set()
        for identifier, expected in fixture['wallets'].items():
            wallet = records[identifier].data
            self.assertEqual(wallet['scheme_id'], expected['scheme'])
            self.assertEqual(wallet['status'], expected['status'])
            self.assertEqual(wallet['import_only'], expected['import_only'])
            self.assertEqual(wallet['generates_mnemonic'], expected['generates'])
            self.assertEqual(wallet['version_interval']['min'], wallet['version_interval']['max'])
            identity = (wallet['product_id'], wallet['platform'], wallet['version_interval']['min'], wallet['mode_id'])
            self.assertNotIn(identity, identities, 'Overlapping version range within the same specific mode')
            identities.add(identity)
            self.assertTrue(wallet['limitations'])
        self.assertEqual(records['cake-wallet-monero'].data['version_interval'], records['cake-wallet-monero-legacy'].data['version_interval'])
        self.assertEqual(records['cake-wallet-monero'].data['product_id'], records['cake-wallet-monero-legacy'].data['product_id'])
        self.assertNotEqual(records['cake-wallet-monero'].data['mode_id'], records['cake-wallet-monero-legacy'].data['mode_id'])
        errors = [str(f) for f in validate_catalog(catalog, allow_incomplete_required=True) if f.severity == 'error']
        self.assertEqual(errors, [])
        for locale in ('en', 'ru'):
            rendered = render_catalog(catalog, locale)
            for identifier in DICTIONARIES | SCHEMES | WALLETS:
                self.assertIn(identifier, rendered)
