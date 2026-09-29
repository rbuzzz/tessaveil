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
            for separator in ("\\", "/", "//", "\\/", "/\\", "\\\\"):
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

    def test_posix_roots_in_uris_or_repeated_slashes_are_not_windows_exceptions(self):
        cases = [("file:" + "/" * 3, "home", "Alice"),
                 ("file:" + "/" * 3, "Users", "Public"),
                 ("/" * 3, "Users", "Public.Alice"),
                 ("/" * 2, "home", "Public"),
                 ("file:" + "/", "Users", "Public"),
                 ("file:" + "/" * 2, "Users", "Public"),
                 ("file:" + "/" * 3, "Users", "Public-Alice"),
                 ("/", "Users", "\\Alice"),
                 ("/", "home", "\\Public"),
                 ("prefixC:" + "/", "Users", "Public"),
                 ("_C:" + "/", "Users", "Public"),
                 ("1C:" + "/", "Users", "Public")]
        for prefix, directory, profile in cases:
            with self.subTest(prefix=prefix, directory=directory, profile=profile):
                value = prefix + directory + "/" + profile + "/file"
                self.assertIn("personal-path", scan.inspect_text("sample.txt", value, frozenset()))

    def test_windows_public_with_repeated_or_mixed_root_separator(self):
        for separator in ("/", "//", "\\/", "\\\\/"):
            public = "C:" + separator + "Users" + "/Public"
            self.assertNotIn("personal-path", scan.inspect_text("sample.txt", public, frozenset()))
            self.assertNotIn("personal-path", scan.inspect_text("sample.txt", public + "\\file", frozenset()))
            for suffix in (".Alice", "-Alice"):
                self.assertIn("personal-path", scan.inspect_text("sample.txt", public + suffix + "/file", frozenset()))

    def test_public_span_does_not_hide_other_private_paths_in_the_same_text(self):
        public = "C:" + "/" + "Users" + "/Public/file"
        private = "file:" + "/" * 3 + "home" + "/Alice/file"
        for value in (public + " " + private, private + " " + public,
                      public + "\n" + private + "\n" + public):
            self.assertIn("personal-path", scan.inspect_text("sample.txt", value, frozenset()))

    def test_uri_scheme_continuations_cannot_create_a_public_drive_exception(self):
        for scheme in ("file+x", "file-x", "file.x", "x+y", "a-Z", "a.B", "a_", "аx"):
            with self.subTest(scheme=scheme):
                value = scheme + ":" + "/" * 3 + "Users" + "/Public/file"
                self.assertIn("personal-path", scan.inspect_text("sample.txt", value, frozenset()))

    def test_drive_exemption_is_ascii_despite_case_insensitive_users(self):
        for fake_drive in ("İ", "ı", "ſ", "K"):
            with self.subTest(fake_drive=fake_drive):
                value = fake_drive + ":" + "/Users" + "/Public/file"
                self.assertIn("personal-path", scan.inspect_text("sample.txt", value, frozenset()))

    def test_real_ascii_drive_after_text_markdown_and_path_delimiters(self):
        for prefix in ("", " ", "\n", "`", '"', "'", "(", "[", "/", "\\"):
            for drive in ("C", "d"):
                with self.subTest(prefix=prefix, drive=drive):
                    root = prefix + drive + ":" + "/uSeRs" + "/pUbLiC"
                    self.assertNotIn("personal-path", scan.inspect_text("sample.txt", root, frozenset()))
                    self.assertNotIn("personal-path", scan.inspect_text("sample.txt", root + "/file", frozenset()))
                    for suffix in (".Alice", "-Alice"):
                        self.assertIn("personal-path", scan.inspect_text("sample.txt", root + suffix + "/file", frozenset()))

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
