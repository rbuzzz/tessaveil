from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]


class RepositoryPolicyTests(unittest.TestCase):
    def test_foundation_files_exist(self):
        required = (
            ".gitattributes",
            ".gitignore",
            "LICENSE",
            "README.md",
            "README.ru.md",
            "CONTRIBUTING.md",
            "SECURITY.md",
            "PRIVACY.md",
            "CODE_SIGNING_POLICY.md",
            "THIRD_PARTY_NOTICES",
            "requirements-dev.txt",
            "tools/run_tests.py",
            "docs/research/name-check.md",
            ".github/workflows/catalog-quality.yml",
        )
        for relative_path in required:
            with self.subTest(path=relative_path):
                self.assertTrue((ROOT / relative_path).is_file())

    def test_license_identifies_apache(self):
        self.assertIn("Apache License", (ROOT / "LICENSE").read_text(encoding="utf-8"))

    def test_both_readmes_disclose_audit_status(self):
        for name in ("README.md", "README.ru.md"):
            with self.subTest(path=name):
                self.assertIn(
                    "Security audit: not yet independently completed",
                    (ROOT / name).read_text(encoding="utf-8"),
                )

    def test_privacy_requires_explicit_transfer_request(self):
        self.assertIn(
            "transfers no information unless the user explicitly requests it",
            (ROOT / "PRIVACY.md").read_text(encoding="utf-8"),
        )

    def test_unsigned_rc_is_never_stable(self):
        self.assertIn(
            "unsigned RCs are never stable releases",
            (ROOT / "CODE_SIGNING_POLICY.md").read_text(encoding="utf-8"),
        )


if __name__ == "__main__":
    unittest.main()
