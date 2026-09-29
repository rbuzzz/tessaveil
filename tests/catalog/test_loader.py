"""Boundary tests for untrusted catalogue input."""

import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch

from tools.catalog.loader import load_catalog, LoadLimits


FIXTURE = Path(__file__).parent / "fixtures" / "valid-minimal"


class LoaderTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        shutil.copytree(FIXTURE, self.root, dirs_exist_ok=True)
        self.wallet = self.root / "catalog/wallets/synthetic-wallet.json"

    def test_valid_fixture_loads_immutable_records(self):
        catalog = load_catalog(self.root)
        self.assertEqual(len(catalog.dictionaries), 2)
        self.assertEqual(catalog.wallets[0].id, "synthetic-wallet")
        with self.assertRaises(AttributeError):
            catalog.wallets[0].id = "changed"

    def test_rejects_invalid_utf8(self):
        self.wallet.write_bytes(b"\xff")
        with self.assertRaisesRegex(ValueError, "UTF-8"):
            load_catalog(self.root)

    def test_rejects_duplicate_json_keys(self):
        self.wallet.write_text('{"schema_version":1,"id":"a","id":"b"}', encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "duplicate JSON key"):
            load_catalog(self.root)

    def test_rejects_oversized_record_before_decoding(self):
        self.wallet.write_bytes(b" " * (1024 * 1024 + 1))
        with self.assertRaisesRegex(ValueError, "record size"):
            load_catalog(self.root)

    def test_rejects_record_count_limit(self):
        with self.assertRaisesRegex(ValueError, "record count"):
            load_catalog(self.root, LoadLimits(max_records=1))

    def test_record_limit_stops_enumeration_without_consuming_more_paths(self):
        original_glob = Path.glob

        def paths(directory, pattern):
            if directory.name == "dictionaries":
                yield directory / "first.json"
                yield directory / "second.json"
                raise AssertionError("enumerated beyond the record limit")
            yield from original_glob(directory, pattern)

        with patch.object(Path, "glob", paths):
            with self.assertRaisesRegex(ValueError, "record count"):
                load_catalog(self.root, LoadLimits(max_records=1))

    def test_rejects_long_nested_string(self):
        payload = json.loads(self.wallet.read_text(encoding="utf-8"))
        payload["guidance"] = "x" * (16 * 1024 + 1)
        self.wallet.write_text(json.dumps(payload), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "string length"):
            load_catalog(self.root)

    def test_string_limit_counts_utf8_bytes_at_boundary(self):
        payload = json.loads(self.wallet.read_text(encoding="utf-8"))
        payload["guidance"] = "я" * 8192  # exactly 16,384 UTF-8 bytes
        self.wallet.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
        self.assertEqual(load_catalog(self.root).wallets[0].id, "synthetic-wallet")
        payload["guidance"] += "я"
        self.wallet.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "string length"):
            load_catalog(self.root)
        payload["guidance"] = "я" * 16_384  # 32 KiB in UTF-8
        self.wallet.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "string length"):
            load_catalog(self.root)

    def test_deep_json_is_bounded_loader_error(self):
        self.wallet.write_bytes(b'{"schema_version":1,"x":' + b"[" * 1100 + b"0" + b"]" * 1100 + b"}")
        with self.assertRaisesRegex(ValueError, "nesting"):
            load_catalog(self.root)

    def test_rejects_oversized_wordlist(self):
        wordlist = self.root / "wordlists/synthetic-en/v1.txt"
        with wordlist.open("wb") as stream:
            stream.truncate(16 * 1024 * 1024 + 1)
        with self.assertRaisesRegex(ValueError, "word-list size"):
            load_catalog(self.root)

    def test_rejects_unknown_schema_version(self):
        payload = json.loads(self.wallet.read_text(encoding="utf-8"))
        payload["schema_version"] = 2
        self.wallet.write_text(json.dumps(payload), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "schema version"):
            load_catalog(self.root)

    def test_rejects_wordlist_path_escape(self):
        dictionary = self.root / "catalog/dictionaries/synthetic-en.json"
        payload = json.loads(dictionary.read_text(encoding="utf-8"))
        payload["wordlist_path"] = "../outside.txt"
        dictionary.write_text(json.dumps(payload), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "word-list path"):
            load_catalog(self.root)

    def test_malformed_nested_license_is_reportable_not_a_crash(self):
        dictionary = self.root / "catalog/dictionaries/synthetic-en.json"
        payload = json.loads(dictionary.read_text(encoding="utf-8"))
        payload["license"]["decision_evidence"] = None
        dictionary.write_text(json.dumps(payload), encoding="utf-8")
        from tools.catalog.validator import validate_catalog
        findings = validate_catalog(load_catalog(self.root))
        self.assertIn("schema", {finding.code for finding in findings})

    def test_rejects_catalog_directory_symlink(self):
        outside = self.root / "outside"
        (self.root / "catalog").rename(outside)
        try:
            (self.root / "catalog").symlink_to(outside, target_is_directory=True)
        except OSError:
            self.skipTest("directory symlinks unavailable")
        with self.assertRaisesRegex(ValueError, "catalogue path"):
            load_catalog(self.root)


if __name__ == "__main__":
    unittest.main()
