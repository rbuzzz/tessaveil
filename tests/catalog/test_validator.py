"""Cross-record and fail-closed catalogue checks."""

import json
from pathlib import Path
import shutil
import tempfile
import unittest

from tools.catalog.loader import load_catalog
from tools.catalog.validator import validate_catalog


FIXTURE = Path(__file__).parent / "fixtures" / "valid-minimal"


class ValidatorTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        shutil.copytree(FIXTURE, self.root, dirs_exist_ok=True)

    def edit(self, relative, change):
        path = self.root / relative
        payload = json.loads(path.read_text(encoding="utf-8"))
        change(payload)
        path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")

    def codes(self, **options):
        return {finding.code for finding in validate_catalog(load_catalog(self.root), **options)
                if finding.severity == "error"}

    def test_valid_fixture_is_terminal_but_not_release_ready(self):
        self.assertEqual(self.codes(), set())
        self.assertIn("required-blocked", self.codes(require_release_ready=True))

    def test_missing_required_can_be_relaxed_only_for_incremental_work(self):
        self.edit("catalog/required/windows-v1.json", lambda p: p["requirements"].append({
            "id": "wallet-pending", "display_name": {"en": "Pending", "ru": "Pending"},
            "record_ids": [], "research_state": "pending", "status": None, "historical": False,
        }))
        self.assertIn("required-pending", self.codes())
        findings = validate_catalog(load_catalog(self.root), allow_incomplete_required=True)
        self.assertEqual([f.severity for f in findings if f.code == "required-pending"], ["warning"])

    def test_rejects_broken_scheme_reference(self):
        self.edit("catalog/wallets/synthetic-wallet.json", lambda p: p.update(scheme_id="absent"))
        self.assertIn("missing-reference", self.codes())

    def test_rejects_missing_or_unpinned_evidence(self):
        self.edit("catalog/dictionaries/synthetic-en.json", lambda p: p.update(evidence_ids=["absent"]))
        self.assertIn("missing-evidence", self.codes())
        self.edit("catalog/dictionaries/synthetic-en.json", lambda p: p.update(evidence_ids=["synthetic-evidence"]))
        self.edit("catalog/evidence/synthetic-evidence.json", lambda p: p.update(revision=""))
        self.assertIn("unpinned-evidence", self.codes())

    def test_rejects_word_count_and_sha_mismatch(self):
        self.edit("catalog/dictionaries/synthetic-en.json", lambda p: p.update(word_count=99, sha256="0" * 64))
        self.assertIn("word-count", self.codes())
        self.assertIn("word-sha256", self.codes())

    def test_rejects_normalization_collisions(self):
        shutil.copytree(Path(__file__).parent / "fixtures/normalization-collision",
                        self.root, dirs_exist_ok=True)
        self.assertIn("normalization-collision", self.codes())

    def test_rejects_unsupported_phrase_length(self):
        self.edit("catalog/schemes/synthetic-scheme.json", lambda p: p.update(supported_lengths=[11]))
        self.assertIn("unsupported-length", self.codes())

    def test_verified_license_must_allow_redistribution_and_signpath(self):
        self.edit("catalog/dictionaries/synthetic-en.json", lambda p: p["license"].update(
            repository_redistribution="pending", signpath_compatible="pending"))
        self.assertIn("license-decision", self.codes())

    def test_duplicate_required_ids_are_semantic_even_when_items_differ(self):
        self.edit("catalog/required/windows-v1.json", lambda p: p["requirements"].append({
            **p["requirements"][0], "display_name": {"en": "Different", "ru": "Different"}
        }))
        self.assertIn("duplicate-required-id", self.codes())

    def test_missing_required_manifest_fails_closed(self):
        (self.root / "catalog/required/windows-v1.json").unlink()
        self.assertIn("required-set-missing", self.codes())


if __name__ == "__main__":
    unittest.main()
