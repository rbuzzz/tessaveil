"""Sensitive-data regressions use constructed synthetic strings, never credentials."""

import hashlib
from pathlib import Path
import unittest

from tools import sensitive_material as scan

ROOT = Path(__file__).resolve().parents[2]


class SensitiveMaterialTests(unittest.TestCase):
    def test_credentials_and_personal_paths_are_rejected_without_echoing_values(self):
        samples = ["-----BEGIN " + "OPENSSH PRIVATE KEY-----",
                   "-----BEGIN " + "PGP PRIVATE KEY BLOCK-----",
                   "ghp" + "_" + "x" * 36, "github" + "_pat_" + "x" * 82,
                   "figd" + "_" + "x" * 40,
                   "C:" + "/Us" + "ers/Alice/file", "/" + "home/alice/file",
                   "/" + "Users/alice/file"]
        for value in samples:
            with self.subTest(kind=value[:4]):
                findings = scan.inspect_text("sample.txt", value, frozenset())
                self.assertTrue(findings)
                self.assertNotIn(value, str(findings))

    def test_mnemonic_run_across_lines_and_json_arrays_is_rejected(self):
        words = frozenset({"abandon", "ability"})
        for value in (" ".join(["abandon"] * 12),
                      "\n".join(["ability"] * 12),
                      '["' + '", "'.join(["abandon"] * 12) + '"]'):
            self.assertIn("mnemonic-like", scan.inspect_text("fixture.json", value, words))

    def test_public_exception_requires_exact_windows_path_component(self):
        for drive in ("C", "d", "Z"):
            for separator in ("\\", "/"):
                for users, public in (("Users", "Public"), ("uSeRs", "pUbLiC")):
                    prefix = drive + ":" + separator + users + separator
                    for suffix in (".Alice", "-Alice", " Alice", "_Alice", "'Alice"):
                        with self.subTest(drive=drive, separator=separator, suffix=suffix):
                            value = prefix + public + suffix + separator + "file"
                            self.assertIn("personal-path", scan.inspect_text("sample.txt", value, frozenset()))
                    for tail in ("", separator + "file"):
                        with self.subTest(drive=drive, separator=separator, tail=tail):
                            value = prefix + public + tail
                            self.assertNotIn("personal-path", scan.inspect_text("sample.txt", value, frozenset()))
        # The common Windows Public directory is not a POSIX profile exception.
        for prefix in ("/" + "Users/", "/" + "home/"):
            self.assertIn("personal-path", scan.inspect_text("sample.txt", prefix + "Public/file", frozenset()))

    def test_key_material_and_index_fixtures_require_exact_reviewed_hash(self):
        for value in ('{"seed_' + 'hex": "' + "ab" * 32 + '"}',
                      '{"indi' + 'ces": [1,2,3,4,5,6,7,8,9,10,11,12]}'):
            self.assertIn("unreviewed-vector", scan.inspect_text("new.json", value, frozenset()))
        payload = b'{"seed_' + b'hex": "synthetic"}'
        digest = hashlib.sha256(payload).hexdigest()
        allow = {"reviewed.json": digest}
        self.assertTrue(scan.reviewed_vector("reviewed.json", payload, allow))
        self.assertFalse(scan.reviewed_vector("elsewhere.json", payload, allow))
        self.assertFalse(scan.reviewed_vector("reviewed.json", payload + b" ", allow))

    def test_decomposed_unicode_mnemonic_is_rejected(self):
        import unicodedata
        word = unicodedata.normalize("NFKD", "ábaco")
        self.assertIn("mnemonic-like", scan.inspect_text("sample.txt", " ".join([word] * 12), frozenset({word})))

    def test_repository_contains_no_sensitive_material(self):
        self.assertEqual(scan.scan_repository(ROOT), ())


if __name__ == "__main__":
    unittest.main()
