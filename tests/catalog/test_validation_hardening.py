"""Dependency closure, bounded uniqueness, and malformed-input regressions."""

from dataclasses import replace
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

from jsonschema import Draft202012Validator

from tools.catalog.generator import render_catalog
from tools.catalog.loader import load_catalog
from tools.catalog import validator
from tools.notices import render as render_notices
from tools.sensitive_material import scan_repository


FIXTURE = Path(__file__).parent / "fixtures/valid-minimal"


class ValidationHardeningTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        shutil.copytree(FIXTURE, self.root, dirs_exist_ok=True)

    def edit(self, relative, **changes):
        path = self.root / "catalog" / relative
        data = json.loads(path.read_text(encoding="utf-8"))
        data.update(changes)
        path.write_text(json.dumps(data), encoding="utf-8")

    def test_verified_wallet_requires_verified_scheme(self):
        for scheme in (None, "synthetic-blocked-scheme", "synthetic-non-mnemonic"):
            with self.subTest(scheme=scheme):
                self.edit("wallets/synthetic-wallet.json", scheme_id=scheme)
                findings = validator.validate_catalog(load_catalog(self.root))
                self.assertTrue(any(f.location == "synthetic-wallet" and
                                    f.severity == "error" for f in findings))
        self.edit("wallets/synthetic-wallet.json", scheme_id="synthetic-scheme")
        self.edit("schemes/synthetic-scheme.json", status="documented")
        self.assertIn("verified-dependency", {f.code for f in validator.validate_catalog(load_catalog(self.root))
                                             if f.location == "synthetic-wallet"})

    def test_verified_scheme_requires_verified_dictionary(self):
        for status in ("documented", "blocked", "no-mnemonic-confirmed"):
            with self.subTest(status=status):
                self.edit("dictionaries/synthetic-en.json", status=status)
                findings = validator.validate_catalog(load_catalog(self.root))
                self.assertIn("verified-dependency", {f.code for f in findings
                                                     if f.location == "synthetic-scheme"})

    def test_verified_scheme_requires_loaded_bytes_and_positive_decisions(self):
        catalog = load_catalog(self.root)
        dictionary = next(r for r in catalog.dictionaries if r.id == "synthetic-en")
        variants = [replace(dictionary, wordlist_bytes=None)]
        for key, value in (("repository_redistribution", "unclear"),
                           ("signpath_compatible", "pending")):
            variants.append(replace(dictionary, data={**dictionary.data, "license": {
                **dictionary.data["license"], key: value}}))
        for dictionary in variants:
            changed = replace(catalog, dictionaries=tuple(
                dictionary if r.id == dictionary.id else r for r in catalog.dictionaries))
            self.assertIn("verified-dependency", {f.code for f in validator.validate_catalog(changed)
                                                 if f.location == "synthetic-scheme"})

    def test_nonselectable_research_keeps_incomplete_links(self):
        for status in ("documented", "blocked", "no-mnemonic-confirmed"):
            with self.subTest(status=status):
                self.edit("wallets/synthetic-wallet.json", status=status, scheme_id=None)
                self.edit("schemes/synthetic-scheme.json", status=status,
                          dictionary_ids=[], supported_lengths=[], test_vector_ids=[])
                path = self.root / "catalog/required/windows-v1.json"
                data = json.loads(path.read_text(encoding="utf-8"))
                for item in data["requirements"]:
                    if item["id"] in ("scheme-synthetic-scheme", "wallet-synthetic-wallet",
                                      "network-synthetic-network"):
                        item["status"] = status
                path.write_text(json.dumps(data), encoding="utf-8")
                self.assertEqual(validator.validate_catalog(load_catalog(self.root)), ())

    def test_long_invalid_identity_remains_invalid_for_every_consumer(self):
        path = self.root / "catalog/wallets/synthetic-wallet.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        data["id"] = "x" * 121
        del data["generates_mnemonic"]
        path.write_text(json.dumps(data), encoding="utf-8")
        catalog = load_catalog(self.root)
        findings = validator.validate_catalog(catalog)
        self.assertTrue(any(f.code == "schema" and f.location == "x" * 120 for f in findings))
        self.assertTrue(all(len(f.location) <= 120 for f in findings))
        with self.assertRaises(ValueError):
            render_catalog(catalog, "en")
        with self.assertRaises(ValueError):
            render_notices(catalog)
        self.assertEqual(scan_repository(self.root), (("catalog", "invalid-scan-input"),))

    def test_sensitive_scanner_rejects_unloadable_catalogue(self):
        (self.root / "catalog/wallets/synthetic-wallet.json").write_text("{", encoding="utf-8")
        self.assertEqual(scan_repository(self.root), (("catalog", "invalid-scan-input"),))

    def test_invalid_wallet_networks_do_not_crash_required_references(self):
        self.edit("wallets/synthetic-wallet.json", network_ids=None)
        catalog = load_catalog(self.root)
        self.assertIn("schema", {f.code for f in validator.validate_catalog(catalog)})
        with self.assertRaises(ValueError):
            render_catalog(catalog, "en")
        with self.assertRaises(ValueError):
            render_notices(catalog)
        self.assertEqual(scan_repository(self.root), (("catalog", "invalid-scan-input"),))

    def test_overflowing_json_number_in_unique_array_is_rejected(self):
        path = self.root / "catalog/wallets/synthetic-wallet.json"
        text = path.read_text(encoding="utf-8").replace('"aliases": []', '"aliases": [1e999]')
        path.write_text(text, encoding="utf-8")
        self.assertIn("schema", {f.code for f in validator.validate_catalog(load_catalog(self.root))})

    def test_malformed_uri_is_a_schema_finding(self):
        self.edit("evidence/synthetic-evidence.json", url="https://[")
        self.assertIn("schema", {f.code for f in validator.validate_catalog(load_catalog(self.root))})


class UniqueItemsTests(unittest.TestCase):
    def test_json_equality_matches_schema_engine(self):
        schema = {"type": "array", "uniqueItems": True}
        cases = [([True, 1, False, 0, None, "1", [], {}], True),
                 ([1, 1.0], False), ([0, -0.0], False),
                 ([{"a": [1, {"b": False}]}, {"a": [1.0, {"b": False}]}], False),
                 ([{"a": 1, "b": 2}, {"b": 2.0, "a": 1.0}], False),
                 ([[True], [1]], True), ([{"a": True}, {"a": 1}], True),
                 ([[1, 2], [2, 1]], True), ([None, None], False),
                 (["1", "1"], False), ([[], []], False), ([{}, {}], False)]
        for values, expected in cases:
            with self.subTest(values=values):
                self.assertEqual(Draft202012Validator(schema).is_valid(values), expected)
                self.assertEqual(validator._schema_valid(values, schema), expected)

    def test_large_unique_array_has_linear_work_budget(self):
        # Count actual validator line execution, not elapsed time or a mocked result.
        # A return to pairwise comparison exceeds this budget long before completion.
        values = [f"record-{i}" for i in range(4096)]
        budget = 100 * len(values) + 1000
        events = 0

        def trace(frame, event, arg):
            nonlocal events
            if event == "line" and frame.f_code.co_filename == validator.__file__:
                events += 1
                if events > budget:
                    raise AssertionError("uniqueItems exceeded linear work budget")
            return trace

        previous = sys.gettrace()
        try:
            sys.settrace(trace)
            self.assertTrue(validator._schema_valid(values, {"uniqueItems": True}))
        finally:
            sys.settrace(previous)
        self.assertFalse(validator._schema_valid([*values, values[-1]], {"uniqueItems": True}))


if __name__ == "__main__":
    unittest.main()
