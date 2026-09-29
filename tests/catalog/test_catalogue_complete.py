"""Independent source-reviewed inventory, not inferred from the manifest.

Cake pin 9679f91a8c9f63d00500c2b7cc18daf00949bdef: configure.dart,
four platform configurations, services and official per-crypto documentation.
Updating this inventory requires reviewing those authorities, not regenerating
expectations from catalog/*. See docs/research/batches/cake-wallet.md.
"""
from pathlib import Path
from collections import Counter
from dataclasses import replace
import unittest

from tools.catalog.generator import render_catalog
from tools.catalog.loader import load_catalog
from tools.catalog.validator import validate_catalog

ROOT = Path(__file__).resolve().parents[2]
PIN = '9679f91a8c9f63d00500c2b7cc18daf00949bdef'
FEATHER_PIN = '948773cf13c7486ee230eb67b6bac06b2f94c874'
POLYSEED_LANGUAGES = ('en', 'ja', 'ko', 'es', 'fr', 'it', 'cs', 'pt', 'zh-hans', 'zh-hant')
# Literal, independently reviewed mode inventory. Import is not generation.
CAKE_MODES = {
    # Polyseed restoration is covered separately by its three conditional paths
    # for every language/platform, never an optional-passphrase umbrella.
    'monero': 'polyseed-create legacy-create bip39-create legacy-import bip39-import bip39-group keys-import view-only hardware',
    'bitcoin': 'bip39-create bip39-import bip39-group electrum-create electrum-import mweb-import view-only hardware',
    'litecoin': 'bip39-create bip39-import bip39-group electrum-create electrum-import mweb-import view-only hardware',
    'bitcoin-cash': 'bip39-create bip39-import bip39-group',
    'dogecoin': 'bip39-create bip39-import bip39-group',
    'ethereum': 'bip39-create bip39-import bip39-group private-key hardware',
    'polygon': 'bip39-create bip39-import bip39-group private-key hardware',
    'base': 'bip39-create bip39-import bip39-group private-key hardware',
    'arbitrum': 'bip39-create bip39-import bip39-group private-key hardware',
    'bnb-chain': 'bip39-create bip39-import bip39-group private-key hardware',
    'solana': 'bip39-create bip39-import bip39-group private-key',
    'tron': 'bip39-create bip39-import bip39-group private-key',
    'nano': 'bip39-create bip39-import bip39-group native-create native-import hex32-import hex64-import',
    'decred': 'bip39-create bip39-import bip39-group native-import view-only',
    'zano': 'bip39-create bip39-import bip39-group native-import',
    'zcash': 'bip39-create bip39-import bip39-group private-key',
}
PRIOR_IDS = {
    ('monero', 'polyseed-create'): 'cake-wallet-monero',
    ('monero', 'legacy-create'): 'cake-wallet-monero-legacy',
    ('monero', 'bip39-create'): 'cake-wallet-monero-bip39',
    ('decred', 'native-import'): 'cake-wallet-decred',
    ('decred', 'bip39-create'): 'cake-wallet-decred-bip39',
    ('zano', 'native-import'): 'cake-wallet-zano',
    ('zano', 'bip39-create'): 'cake-wallet-zano-bip39',
}


class CatalogueCompleteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = load_catalog(ROOT)
        cls.records = {r.id: r for r in (*cls.catalog.dictionaries, *cls.catalog.schemes, *cls.catalog.wallets)}
        cls.requirements = {i.id: i for s in cls.catalog.required_sets for i in s.requirements}

    def test_every_required_reference_and_record_is_evidenced_terminal(self):
        self.assertEqual(validate_catalog(self.catalog, require_terminal=True), ())
        evidence = {r.id: r for r in self.catalog.evidence}
        covered = set()
        for item in self.requirements.values():
            self.assertEqual(item.data['research_state'], 'terminal', item.id)
            self.assertTrue(item.data['record_ids'], item.id)
            covered.update(item.data['record_ids'])
        self.assertFalse(set(self.records) - covered,
                         'Records omitted from required coverage: ' + ', '.join(sorted(set(self.records) - covered)))
        for record in self.records.values():
            self.assertIn(record.data['status'], {'verified', 'documented', 'blocked', 'no-mnemonic-confirmed'})
            self.assertTrue(record.data['evidence_ids'], record.id)
            for eid in record.data['evidence_ids']:
                self.assertIn(record.id, evidence[eid].data['record_ids'])
            self.assertTrue(any(evidence[e].data['source_type'].startswith('official-') for e in record.data['evidence_ids']))

    def test_independent_cake_inventory_cannot_be_satisfied_by_monero_only(self):
        expected = {}
        for network, modes in CAKE_MODES.items():
            platforms = ('android', 'ios') if network in {'decred', 'zano', 'zcash'} else ('android', 'ios', 'macos', 'linux')
            for platform in platforms:
                for mode in modes.split():
                    identifier = PRIOR_IDS.get((network, mode)) if platform == 'android' else None
                    identifier = identifier or f'cake-wallet-{network}-{mode}-{platform}'
                    expected[identifier] = (network, platform, mode)
        missing = set(expected) - self.records.keys()
        for platform in ('android', 'ios'):
            for length in (24, 25):
                self.assertFalse(f'cake-wallet-zano-native{length}-import-{platform}' in self.records,
                                 'Global Zano history does not establish a Cake product mode')
        self.assertFalse(missing, 'Missing Cake IDs: ' + ', '.join(sorted(missing)))
        for identifier, (network, platform, mode) in expected.items():
            row = self.records[identifier].data
            with self.subTest(record=identifier):
                self.assertEqual(row['product_id'], 'cake-wallet')
                self.assertEqual(tuple(row['network_ids']), (network,))
                self.assertEqual(row['platform'], platform)
                self.assertIn(PIN, row['version_interval']['min'])
                self.assertEqual(row['version_interval']['min'], row['version_interval']['max'])
                self.assertEqual(row['generates_mnemonic'], mode.endswith('-create'))
                self.assertNotEqual(row['status'], 'verified', 'No independent wallet recovery was established at this research boundary')
                self.assertTrue(row['limitations'])

    def test_distinct_lengths_normalization_and_non_mnemonic_modes(self):
        cases = {
            'cake-bip39-create': (12, 24), 'cake-bip39-import': (12, 15, 18, 21, 24),
            'cake-electrum-24': (24,), 'cake-nano-native': (24,),
            'cake-nano-hd-create': (12, 24), 'cake-nano-hd-import': (12, 15, 18, 21, 24),
            'cake-monero-bip39-import': (12, 15, 18, 21, 24), 'tevador-14-unresolved': (14,),
        }
        self.assertFalse(set(cases) - self.records.keys(), 'Missing distinct Cake/omitted recovery schemes')
        for identifier, lengths in cases.items():
            self.assertEqual(tuple(self.records[identifier].data['supported_lengths']), lengths)
        self.assertEqual(self.records['cake-electrum-24'].data['status'], 'blocked')
        self.assertEqual(self.records['cake-bip39-create'].data['status'], 'blocked')
        self.assertEqual(self.records['cake-nano-hd-create'].data['external_secret']['kind'], 'none')
        for identifier in ('cake-wallet-nano-hex64-import-android', 'cake-wallet-ethereum-private-key-android',
                           'cake-wallet-bitcoin-hardware-android', 'cake-wallet-app-backup-android'):
            self.assertIn(identifier, self.records)
            self.assertIsNone(self.records[identifier].data['scheme_id'])
            self.assertFalse(self.records[identifier].data['generates_mnemonic'])
        self.assertIn('feather-tevador-import', self.records)

    def test_release_gate_lists_all_required_blockers_independently(self):
        blocked = {i.id for i in self.requirements.values() if i.data['status'] == 'blocked'}
        self.assertTrue(blocked)
        self.assertEqual(validate_catalog(self.catalog, require_terminal=True, require_release_ready=False), ())
        findings = validate_catalog(self.catalog, require_release_ready=True)
        self.assertEqual({f.location for f in findings if f.code == 'required-blocked'}, blocked)
        self.assertTrue(all(f.severity == 'error' for f in findings))
        # Also exercise an independent small fixture: deleting the release branch
        # must fail this even if the real manifest were accidentally de-scoped.
        fixture = load_catalog(ROOT / 'tests/catalog/fixtures/valid-minimal')
        self.assertTrue(any(f.code == 'required-blocked' for f in validate_catalog(fixture, require_release_ready=True)))

    def test_language_and_fresh_monero_length_identities_are_explicit(self):
        languages = {
            'polyseed': ('en', 'ja', 'ko', 'es', 'fr', 'it', 'cs', 'pt', 'zh-hans', 'zh-hant'),
            'legacy': ('en', 'de', 'es', 'fr', 'it', 'nl', 'pt', 'ru', 'ja', 'zh-hans'),
        }
        self.assertTrue('cake-monero-bip39-create' in self.records)
        self.assertEqual(tuple(self.records['cake-monero-bip39-create'].data['supported_lengths']), (12,))
        for family, codes in languages.items():
            for code in codes:
                scheme_id = f'cake-monero-{family}-{code}'
                self.assertTrue(scheme_id in self.records, scheme_id)
                prefix = 'polyseed' if family == 'polyseed' else 'monero'
                self.assertEqual(tuple(self.records[scheme_id].data['dictionary_ids']), (f'{prefix}-{code}',))
                for platform in ('android', 'ios', 'macos', 'linux'):
                    for direction in (('create',) if family == 'polyseed' else ('create', 'import')):
                        identifier = f'cake-wallet-monero-{family}-{code}-{direction}-{platform}'
                        self.assertTrue(identifier in self.records, identifier)
                        self.assertEqual(self.records[identifier].data['scheme_id'], scheme_id)

    def test_polyseed_restore_conditions_cannot_conflate_offset_and_encryption(self):
        self.assert_polyseed_restore_contract(self.records)

    def assert_polyseed_restore_contract(self, records):
        expected = {
            'plain': ('isEncrypted=false; passphrase empty', 'none', 'generateKey'),
            'encrypted': ('isEncrypted=true', 'required-passphrase', 'polyseed.crypt'),
            'offset': ('isEncrypted=false; passphrase nonempty', 'required-passphrase',
                       'restoreWalletFromPolyseedWithOffset'),
        }
        evidence = {row.id: row.data for row in self.catalog.evidence}
        for language in POLYSEED_LANGUAGES:
            schemes = []
            for mode, (condition, secret, operation) in expected.items():
                sid = f'cake-monero-polyseed-{mode}-{language}'
                self.assertTrue(sid in records, sid)
                schemes.append(sid)
                scheme = records[sid].data
                self.assertEqual(tuple(scheme['dictionary_ids']), (f'polyseed-{language}',))
                self.assertEqual(tuple(scheme['supported_lengths']), (16,))
                self.assertEqual(scheme['external_secret']['kind'], secret)
                self.assertIn(condition, scheme['semantic_distinction'])
                self.assertIn(operation, scheme['semantic_distinction'])
                self.assertIn('cake-wallet-polyseed-dispatch', scheme['evidence_ids'])
                self.assertEqual(evidence['cake-wallet-polyseed-dispatch']['revision'], PIN)
                if mode == 'offset':
                    self.assertEqual(scheme['status'], 'blocked')
                    self.assertIn('English-only', scheme['semantic_distinction'])
                    self.assertIn('cake-wallet-polyseed-offset-native', scheme['evidence_ids'])
                for platform in ('android', 'ios', 'macos', 'linux'):
                    identifier = f'cake-wallet-monero-polyseed-{mode}-{language}-import-{platform}'
                    self.assertTrue(identifier in records, identifier)
                    row = records[identifier].data
                    self.assertEqual(row['scheme_id'], sid)
                    self.assertIn(condition, ' '.join(row['limitations']))
                    self.assertTrue(row['import_only'])
                    self.assertFalse(row['generates_mnemonic'])
            self.assertEqual(len(set(schemes)), 3)
            for platform in ('android', 'ios', 'macos', 'linux'):
                self.assertFalse(f'cake-wallet-monero-polyseed-{language}-import-{platform}' in records)
        for platform in ('android', 'ios', 'macos', 'linux'):
            self.assertFalse(f'cake-wallet-monero-polyseed-import-{platform}' in records)

    def test_polyseed_contract_rejects_missing_and_conflated_paths(self):
        identifier = 'cake-wallet-monero-polyseed-offset-en-import-android'
        missing = dict(self.records)
        del missing[identifier]
        with self.assertRaises(AssertionError):
            self.assert_polyseed_restore_contract(missing)
        conflated = dict(self.records)
        row = self.records[identifier]
        payload = dict(row.data)
        payload['scheme_id'] = 'cake-monero-polyseed-encrypted-en'
        conflated[identifier] = replace(row, data=payload)
        with self.assertRaises(AssertionError):
            self.assert_polyseed_restore_contract(conflated)

    def test_tevador_provenance_is_not_a_cake_source_alias(self):
        scheme = self.records['tevador-14-unresolved'].data
        self.assertEqual(scheme['version_interval']['min'], 'source-' + FEATHER_PIN)
        self.assertEqual(scheme['version_interval']['max'], 'source-' + FEATHER_PIN)
        evidence = {row.id: row.data for row in self.catalog.evidence}
        self.assertTrue(all(evidence[e]['revision'] == FEATHER_PIN for e in scheme['evidence_ids']))
        self.assertTrue('cake-wownero-14-unresolved' in self.records)
        cake_scheme = self.records['cake-wownero-14-unresolved'].data
        self.assertEqual(cake_scheme['version_interval']['min'], 'source-' + PIN)
        self.assertEqual(cake_scheme['status'], 'blocked')
        for platform in ('android', 'ios', 'macos', 'linux'):
            identifier = f'cake-wallet-wownero-legacy14-export-{platform}'
            self.assertTrue(identifier in self.records, identifier)
            row = self.records[identifier].data
            self.assertEqual(row['scheme_id'], 'cake-wownero-14-unresolved')
            for eid in ('cake-wallet-wownero-deprecation', 'cake-wallet-wownero-seed-export'):
                self.assertIn(eid, row['evidence_ids'])
                self.assertEqual(evidence[eid]['revision'], PIN)
                self.assertIn(identifier, evidence[eid]['record_ids'])
            self.assertFalse(f'cake-wallet-wownero-tevador14-export-{platform}' in self.records)

    @staticmethod
    def fresh_bip39_semantic_keys(wallets):
        # Identify the actual source path, not an arbitrary mode_id spelling.
        return [(r['product_id'], r['platform'], tuple(r['network_ids']),
                 r['version_interval']['min'], 'getBip39Seed', 'en', 12)
                for r in wallets if r['product_id'] == 'cake-wallet'
                and tuple(r['network_ids']) == ('monero',) and r['generates_mnemonic']
                and ('cake-wallet-monero-bip39-derive' in r['evidence_ids']
                     or r['scheme_id'] == 'cake-monero-bip39-create')]

    def test_fresh_bip39_has_one_semantic_identity_per_platform(self):
        wallets = [row.data for row in self.catalog.wallets]
        keys = self.fresh_bip39_semantic_keys(wallets)
        self.assertEqual(len(keys), 4, 'Same fresh English12 source path must not be duplicated')
        self.assertTrue(all(count == 1 for count in Counter(keys).values()))
        for platform in ('android', 'ios', 'macos', 'linux'):
            identifier = 'cake-wallet-monero-bip39' if platform == 'android' else f'cake-wallet-monero-bip39-create-{platform}'
            self.assertEqual(self.records[identifier].data['scheme_id'], 'cake-monero-bip39-create')
        clone = dict(self.records['cake-wallet-monero-bip39'].data)
        clone['id'], clone['mode_id'] = 'adversarial-new-id', 'unrelated-spelling'
        mutated = self.fresh_bip39_semantic_keys(wallets + [clone])
        self.assertTrue(any(count > 1 for count in Counter(mutated).values()),
                        'Renaming a mode cannot conceal semantic duplication')

    def test_generated_blocker_summary_contains_records_and_no_selectable_claim(self):
        for locale, heading in (('en', '## Required release blockers'), ('ru', '## Обязательные блокеры релиза')):
            output = render_catalog(self.catalog, locale)
            self.assertTrue(heading in output, 'Missing concise generated blocker summary')
            section = output.split(heading, 1)[1].split('\n## ', 1)[0]
            for item in self.requirements.values():
                if item.data['status'] == 'blocked':
                    self.assertIn(item.id, section)
                    for identifier in item.data['record_ids']:
                        self.assertIn(identifier, section)
            self.assertIn('NO-GO', output)
            # No UI selector exists at this research boundary. The generated
            # candidate surface must mark every nonverified record nonselectable.
            for kind, rows in (('wallet', self.catalog.wallets), ('scheme', self.catalog.schemes),
                               ('dictionary', self.catalog.dictionaries)):
                marker = ('Not selectable;' if locale == 'en' else 'Недоступно для выбора;')
                for row in rows:
                    record_section = output.split(f'<a id="{kind}-{row.id}"></a>', 1)[1].split('<a id=', 1)[0]
                    if marker not in record_section:
                        self.assertEqual(row.data['status'], 'verified', row.id)


if __name__ == '__main__':
    unittest.main()
