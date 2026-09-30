"""Offline public research contracts; no user phrases or share reconstruction."""
from pathlib import Path
import hashlib
import json
import unittest
from tools.catalog.loader import load_catalog
from tools.catalog.validator import validate_catalog
from tools.catalog.generator import render_catalog

ROOT = Path(__file__).resolve().parents[2]
WALLETS = {'trezor-model-t', 'trezor-safe-3', 'trezor-safe-5', 'trezor-safe-7',
           'pera-wallet', 'defly', 'yoroi', 'daedalus', 'lace', 'eternl', 'nami', 'typhon'}
SCHEMES = {'slip39-share', 'algorand-25', 'cardano-byron', 'cardano-icarus',
           'cardano-hardware', 'cardano-daedalus-27'}

class Slip39AlgorandCardanoTests(unittest.TestCase):
    def test_algorand_dictionary_provenance_preserves_existing_final_lf(self):
        _, records = self.batch()
        blob = records['bip39-en'].wordlist_bytes
        # Independently extracted from word_list_raw() at the pinned SDK revision;
        # no upstream wordlist copy or network dependency belongs in this suite.
        self.assertEqual(len(blob), 13116)
        self.assertTrue(blob.endswith(b'\n'))
        unchanged = hashlib.sha256(blob).hexdigest()
        extra_lf = hashlib.sha256(blob + b'\n').hexdigest()
        self.assertEqual(unchanged, '2f5eed53a4727b4bf8880d8f3f199efc90e58503646d9ff8eff3a2ed3b24dbda')
        self.assertEqual(extra_lf, '24ce42c2fd4a95c1b86bbee9bce1e1cf255bd0022e19bab6bd591afd68b7efdb')
        self.assertNotEqual(unchanged, extra_lf)
        note = ' '.join((ROOT / 'docs/research/batches/slip39-algorand-cardano.md').read_text('utf-8').split())
        self.assertIn('The literal already includes a final LF; its unchanged UTF-8 bytes', note)
        self.assertNotIn('Appending a final LF', note)

    def test_unmapped_hardware_lengths_render_as_absent_in_both_locales(self):
        catalog, _ = self.batch()
        for locale, label in [('en', 'Supported lengths'), ('ru', 'Допустимые длины')]:
            text = render_catalog(catalog, locale)
            self.assertTrue('- ' + label + ': —' in text, 'Absent lengths need a visible marker')
            self.assertTrue(all(line == line.rstrip() for line in text.splitlines()))

    def batch(self):
        catalog = load_catalog(ROOT)
        records = {r.id: r for r in (*catalog.dictionaries, *catalog.schemes, *catalog.wallets)}
        self.assertFalse((WALLETS | SCHEMES | {'slip39-en'}) - records.keys(), 'Missing Task12 profiles')
        return catalog, records

    def test_complete_batch_and_shared_dictionary_semantics(self):
        _, records = self.batch()
        for identifier, lengths in {'slip39-share': (20, 33), 'algorand-25': (25,),
                                    'cardano-byron': (12,), 'cardano-icarus': (15, 24),
                                    'cardano-daedalus-27': (27,)}.items():
            self.assertEqual(tuple(records[identifier].data['supported_lengths']), lengths)
        for identifier in SCHEMES - {'slip39-share', 'cardano-hardware'}:
            self.assertEqual(tuple(records[identifier].data['dictionary_ids']), ('bip39-en',))
        self.assertEqual(tuple(records['slip39-share'].data['dictionary_ids']), ('slip39-en',))
        self.assertEqual(tuple(records['cardano-hardware'].data['supported_lengths']), ())
        self.assertTrue(records['cardano-daedalus-27'].data['historical'])
        bip = records['bip39-en'].wordlist_bytes
        copies = [p for p in (ROOT / 'wordlists').rglob('*.txt') if p.read_bytes() == bip]
        # Polyseed has an independently licensed same-byte upstream English projection.
        self.assertTrue(all(p.parent.name in {'bip39-en', 'polyseed-en'} for p in copies))
        for scheme in SCHEMES:
            self.assertTrue(records[scheme].data['no_key_derivation'])
            self.assertTrue(records[scheme].data['no_complete_phrase_validation'])
        for model in ('trezor-model-t', 'trezor-safe-3', 'trezor-safe-5', 'trezor-safe-7'):
            scheme = records[records[model].data['scheme_id']].data
            self.assertEqual(tuple(scheme['supported_lengths']), (20,))
        self.assertEqual(records['pera-wallet'].data['scheme_id'], 'algorand-25')
        self.assertFalse(records['pera-wallet'].data['generates_mnemonic'])
        self.assertNotEqual(records['pera-wallet-universal'].data['scheme_id'], 'algorand-25')

    def test_terminal_research_does_not_clear_release_or_infer_wallet_generation(self):
        catalog, records = self.batch()
        required = {r.id: r.data for s in catalog.required_sets for r in s.requirements}
        for prefix, ids in [('dictionary', {'slip39-en'}), ('scheme', SCHEMES), ('wallet', WALLETS)]:
            for identifier in ids:
                row = required[prefix + '-' + identifier]
                self.assertEqual(row['research_state'], 'terminal')
                self.assertIn(identifier, row['record_ids'])
                self.assertEqual(row['status'], records[identifier].data['status'])
        identities = set()
        for wallet in catalog.wallets:
            if wallet.id not in WALLETS and not wallet.id.startswith(('daedalus-', 'yoroi-', 'trezor-', 'pera-wallet-')):
                continue
            row = wallet.data
            self.assertIn(row['status'], ('documented', 'blocked'))
            self.assertTrue(row['limitations'])
            self.assertEqual(row['version_interval']['min'], row['version_interval']['max'])
            key = (row['product_id'], row['platform'], row['version_interval']['min'], row['mode_id'])
            self.assertNotIn(key, identities)
            identities.add(key)
        self.assertFalse([f for f in validate_catalog(catalog, allow_incomplete_required=True) if f.severity == 'error'])
        blocked = {f.location for f in validate_catalog(catalog, require_release_ready=True)
                   if f.severity == 'error' and f.code == 'required-blocked'}
        self.assertTrue({'scheme-cardano-hardware', 'wallet-defly', 'wallet-eternl', 'wallet-typhon'} <= blocked)

    def test_public_vectors_pin_dictionary_and_position_rules(self):
        _, records = self.batch()
        path = ROOT / 'tests/catalog/fixtures/public/slip39-algorand-cardano.json'
        self.assertTrue(path.is_file(), 'Missing independently published vector projections')
        fixture = json.loads(path.read_text('utf-8'))
        blob = records['slip39-en'].wordlist_bytes
        self.assertEqual(hashlib.sha256(blob).hexdigest(), fixture['slip39_wordlist_sha256'])
        self.assertEqual(len(blob.decode().splitlines()), 1024)
        self.assertEqual(len(set(blob.decode().splitlines())), 1024)
        self.assertEqual(len(blob), 7231)
        self.assertEqual(records['slip39-en'].data['sha256'], fixture['slip39_wordlist_sha256'])
        self.assertEqual(records['slip39-en'].data['license']['repository_redistribution'], 'allowed')
        self.assertEqual(records['slip39-en'].data['license']['signpath_compatible'], 'compatible')
        words = blob.decode().splitlines()
        polynomial = [0xe0e040, 0x1c1c080, 0x3838100, 0x7070200, 0xe0e0009,
                      0x1c0c2412, 0x38086c24, 0x3090fc48, 0x21b1f890, 0x3f3f120]
        for vector in fixture['slip39']:
            idx = vector['indices']
            self.assertIn(len(idx), (20, 33))
            self.assertTrue(hashlib.sha256(' '.join(words[i] for i in idx).encode()).hexdigest() == vector['sentence_sha256'])
            header = (idx[0] << 10) | idx[1]
            self.assertEqual([header >> 5, bool(header & 16), header & 15], vector['identifier_extendable_exponent'])
            params = (idx[2] << 10) | idx[3]
            metadata = [params >> 16, ((params >> 12) & 15) + 1,
                        ((params >> 8) & 15) + 1, (params >> 4) & 15, (params & 15) + 1]
            self.assertEqual(metadata, vector['group_index_threshold_count_member_index_threshold'])
            residue = 1
            domain = b'shamir_extendable' if header & 16 else b'shamir'
            for coefficient in [*domain, *idx]:
                top = residue >> 20
                residue = ((residue & 0xfffff) << 10) ^ coefficient
                for bit, generator in enumerate(polynomial):
                    if (top >> bit) & 1:
                        residue ^= generator
            self.assertEqual(residue, 1)
            padding = (len(idx) - 7) * 10 - (128 if len(idx) == 20 else 256)
            self.assertLess(idx[4], 1 << (10-padding))
        for vector in fixture['algorand']:
            seed = bytes.fromhex(vector['seed_hex'])
            indices = [(int.from_bytes(seed, 'little') >> (11*i)) & 2047 for i in range(24)]
            check = int.from_bytes(hashlib.new('sha512_256', seed).digest()[:2], 'little') & 2047
            self.assertEqual(indices + [check], vector['indices'])
            self.assertLess(indices[23], 8, 'Final data word has eight padding zero bits')
            words = records['bip39-en'].wordlist_bytes.decode().splitlines()
            self.assertTrue(hashlib.sha256(' '.join(words[i] for i in vector['indices']).encode()).hexdigest() == vector['sentence_sha256'])
        paper = fixture['daedalus_paper']
        self.assertEqual(len(paper['indices']), 27)
        self.assertEqual(paper['partition'], [18, 9])
        words = records['bip39-en'].wordlist_bytes.decode().splitlines()
        self.assertTrue(hashlib.sha256(' '.join(words[i] for i in paper['indices']).encode()).hexdigest() == paper['sentence_sha256'])
        # This nine-word suffix is a password input, not an independent BIP39 seed.
        suffix = ' '.join(words[i] for i in paper['indices'][18:]).encode()
        password = hashlib.pbkdf2_hmac('sha512', suffix, b'mnemonic', 2048, 32)
        self.assertTrue(hashlib.sha256(password).hexdigest() == paper['password_sha256'])
