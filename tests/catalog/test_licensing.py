"""Fail-closed licensing gates and executable policy decision tables."""

import json
from pathlib import Path
import shutil
import tempfile
import unittest

from tools.catalog.loader import load_catalog
from tools.catalog.validator import validate_catalog


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = Path(__file__).parent / "fixtures" / "valid-minimal"
DICTIONARY = "catalog/dictionaries/synthetic-en.json"
EVIDENCE = "catalog/evidence/synthetic-evidence.json"


class LicensingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        shutil.copytree(FIXTURE, self.root, dirs_exist_ok=True)
        self.edit(EVIDENCE, source_type="official-specification")

    def edit(self, relative, **changes):
        path = self.root / relative
        payload = json.loads(path.read_text(encoding="utf-8"))
        payload.update(changes)
        path.write_text(json.dumps(payload), encoding="utf-8")

    def license(self, redistribution, signing, **changes):
        data = json.loads((self.root / DICTIONARY).read_text(encoding="utf-8"))
        data["license"].update(repository_redistribution=redistribution,
                               signpath_compatible=signing)
        self.edit(DICTIONARY, **{**data, **changes})

    def findings(self):
        return validate_catalog(load_catalog(self.root))

    def codes(self, record="synthetic-en"):
        return {f.code for f in self.findings() if f.location == record and f.severity == "error"}

    def test_verified_requires_primary_evidence(self):
        self.edit(EVIDENCE, source_type="public-test-vector")
        for record in ("synthetic-en", "synthetic-scheme", "synthetic-wallet"):
            with self.subTest(record=record):
                self.assertIn("primary-evidence", self.codes(record))

    def test_malformed_primary_evidence_cannot_clear_verified_gate(self):
        self.edit(EVIDENCE, verified_on="2026-02-30")
        self.assertIn("primary-evidence", self.codes())

    def test_official_source_requires_full_commit_pin(self):
        for revision in ("main", "v1.0", "a" * 7, "a" * 40 + "\n"):
            with self.subTest(revision=repr(revision)):
                self.edit(EVIDENCE, source_type="official-source", revision=revision)
                self.assertIn("unpinned-evidence", self.codes("synthetic-evidence"))
                self.assertIn("primary-evidence", self.codes())
        for revision in ("a" * 40, "a" * 64):
            self.edit(EVIDENCE, revision=revision)
            self.assertEqual(self.codes(), set())

    def test_verified_requires_redistribution_permission(self):
        for value in ("forbidden", "unclear", "denied", "pending", "allowed (assumed)", None):
            with self.subTest(value=value):
                self.license(value, "compatible")
                self.assertIn("license-decision", self.codes())

    def test_verified_requires_signpath_compatibility(self):
        for value in ("incompatible", "pending", "compatible (assumed)", None):
            with self.subTest(value=value):
                self.license("allowed", value)
                self.assertIn("license-decision", self.codes())

    def test_redistributable_but_signpath_incompatible_fixture_fails(self):
        overlay = Path(__file__).parent / "fixtures/invalid-schema/signpath-incompatible"
        self.assertTrue(overlay.is_dir(), "missing redistributable but incompatible fixture")
        shutil.copytree(overlay, self.root, dirs_exist_ok=True)
        self.assertIn("license-decision", self.codes())
        self.assertIn("schema", self.codes())

    def test_nonverified_bundling_cannot_bypass_license_gate(self):
        for redistribution, signing in (("forbidden", "compatible"), ("unclear", "compatible"),
                                        ("allowed", "incompatible"), ("allowed", "pending")):
            with self.subTest(redistribution=redistribution, signing=signing):
                self.license(redistribution, signing, status="documented")
                self.assertIn("license-decision", self.codes())
                self.edit(DICTIONARY, wordlist_path=None)
                self.assertNotIn("license-decision", self.codes())
                self.edit(DICTIONARY, wordlist_path="wordlists/synthetic-en/v1.txt")

    def test_nonpositive_decisions_are_valid_metadata_without_bundling(self):
        for redistribution in ("allowed", "forbidden", "unclear"):
            for signing in ("compatible", "incompatible", "pending"):
                with self.subTest(redistribution=redistribution, signing=signing):
                    self.license(redistribution, signing, status="documented", wordlist_path=None)
                    self.assertEqual(self.codes(), set())
        for legacy in ("denied", "pending"):
            self.license(legacy, "compatible", status="documented", wordlist_path=None)
            self.assertIn("schema", self.codes())

    def policy_rows(self, name, heading):
        path = ROOT / "docs/research" / name
        self.assertTrue(path.is_file(), f"missing policy {name}")
        text = path.read_text(encoding="utf-8")
        self.assertIn(heading, text)
        section = text.split(heading, 1)[1].split("\n## ", 1)[0]
        return [tuple(cell.strip().strip("`") for cell in line.strip().strip("|").split("|"))
                for line in section.splitlines() if line.startswith("| ")][2:]

    def test_documented_license_matrix_matches_real_validator(self):
        rows = self.policy_rows("licensing.md", "## Executable decision matrix")
        expected = {(r, s): "pass" if (r, s) == ("allowed", "compatible") else "block"
                    for r in ("allowed", "forbidden", "unclear")
                    for s in ("compatible", "incompatible", "pending")}
        self.assertEqual(len(rows), 9)
        self.assertEqual({(r, s): result for r, s, result in rows}, expected)
        for redistribution, signing, outcome in rows:
            with self.subTest(redistribution=redistribution, signing=signing):
                self.license(redistribution, signing)
                self.assertEqual(not self.codes(), outcome == "pass")

    def test_documented_evidence_levels_match_real_validator(self):
        rows = self.policy_rows("source-policy.md", "## Evidence priority contract")
        self.assertEqual(rows, [
            ("1", "official-specification", "yes"),
            ("2", "official-documentation", "yes"),
            ("3", "official-source", "yes"),
            ("4", "public-test-vector", "no"),
        ])
        for _, source_type, primary in rows:
            self.edit(EVIDENCE, source_type=source_type, revision="a" * 40)
            self.assertEqual("primary-evidence" not in self.codes(), primary == "yes")


if __name__ == "__main__":
    unittest.main()
