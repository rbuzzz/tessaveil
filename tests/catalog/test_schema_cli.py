"""Run the pinned schema engine on the shared catalogue fixture corpus."""

from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[2]
SCHEMAS = ROOT / "catalog" / "schema"
FIXTURES = Path(__file__).resolve().parent / "fixtures"


class SchemaCliTests(unittest.TestCase):
    def test_valid_minimal_catalogue_records(self):
        case = FIXTURES / "valid-minimal"
        for kind, relative in (
            ("dictionary", "catalog/dictionaries/synthetic-en.json"),
            ("scheme", "catalog/schemes/synthetic-scheme.json"),
            ("wallet", "catalog/wallets/synthetic-wallet.json"),
            ("evidence", "catalog/evidence/synthetic-evidence.json"),
            ("required-set", "catalog/required/windows-v1.json"),
        ):
            with self.subTest(kind=kind):
                result = self._check(kind, case / relative)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_blocked_dictionary_can_record_unknown_source_details(self):
        instance = FIXTURES / "valid-minimal" / "catalog" / "dictionaries" / "synthetic-blocked.json"
        self.assertTrue(instance.is_file())
        result = self._check("dictionary", instance)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_terminal_schemes_can_record_absent_mnemonic_details(self):
        for name in ("synthetic-blocked-scheme", "synthetic-non-mnemonic"):
            with self.subTest(name=name):
                instance = FIXTURES / "valid-minimal" / "catalog" / "schemes" / f"{name}.json"
                self.assertTrue(instance.is_file())
                result = self._check("scheme", instance)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_repository_required_manifest_matches_schema(self):
        result = self._check("required-set", ROOT / "catalog" / "required" / "windows-v1.json")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_invalid_schema_cases(self):
        for kind, relative in (
            ("wallet", "historical-status/catalog/wallets/synthetic-wallet.json"),
            ("wallet", "unknown-field/catalog/wallets/synthetic-wallet.json"),
            ("wallet", "verified-wallet-without-scheme/catalog/wallets/synthetic-wallet.json"),
            ("dictionary", "missing-license-decision/catalog/dictionaries/synthetic-en.json"),
            ("required-set", "duplicate-required-ids/catalog/required/windows-v1.json"),
            ("scheme", "verified-scheme-incomplete/catalog/schemes/synthetic-scheme.json"),
        ):
            with self.subTest(case=relative):
                instance = FIXTURES / "invalid-schema" / relative
                self.assertTrue(instance.is_file(), f"Missing fixture: {relative}")
                result = self._check(kind, instance)
                self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertIn("Schema validation errors were encountered.", result.stdout + result.stderr)

    @staticmethod
    def _check(kind: str, instance: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, "-m", "check_jsonschema", "--schemafile",
             str(SCHEMAS / f"{kind}.schema.json"), str(instance)],
            cwd=ROOT, capture_output=True, text=True, check=False,
        )


if __name__ == "__main__":
    unittest.main()
