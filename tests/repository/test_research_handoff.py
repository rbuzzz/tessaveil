"""Executable final gates reject drift and distinguish research from release."""

import copy
import json
from pathlib import Path
import unittest

from tools.catalog.loader import load_catalog
from tools import research_gate, notices

ROOT = Path(__file__).resolve().parents[2]


class ResearchHandoffTests(unittest.TestCase):
    def test_notices_include_every_bundled_dictionary_and_are_deterministic(self):
        catalog = load_catalog(ROOT)
        text = notices.render(catalog)
        self.assertEqual(text, notices.render(catalog))
        for record in catalog.dictionaries:
            if record.wordlist_bytes is not None:
                self.assertIn(record.data["sha256"], text)
                self.assertIn(record.data["wordlist_path"], text)
                self.assertIn(record.data["source"]["revision"], text)
        self.assertEqual((ROOT / "THIRD_PARTY_NOTICES").read_text(encoding="utf-8"), text)

    def test_pending_bundled_license_fails_notice_generation(self):
        from dataclasses import replace
        catalog = load_catalog(ROOT)
        first = catalog.dictionaries[0]
        bad = replace(first, data={**first.data, "license": {
            **first.data["license"], "signpath_compatible": "pending"}})
        with self.assertRaises(ValueError):
            notices.render(replace(catalog, dictionaries=(bad, *catalog.dictionaries[1:])))

    def test_release_result_must_match_exact_committed_output(self):
        expected = {"exit_code": 1, "output": "blocked\n", "status": "NO-GO"}
        self.assertTrue(research_gate.matches(expected, 1, "blocked\n"))
        self.assertFalse(research_gate.matches(expected, 0, "blocked\n"))
        self.assertFalse(research_gate.matches(expected, 1, "other blocker\n"))
        self.assertFalse(research_gate.matches({**expected, "status": "GO"}, 1, "blocked\n"))

    def test_report_evidence_hash_changes_fail_closed(self):
        report = research_gate.read_contract(ROOT)
        self.assertEqual(research_gate.verify_inputs(ROOT, report), ())
        bad = copy.deepcopy(report)
        key = next(iter(bad["evidence_sha256"]))
        bad["evidence_sha256"][key] = "0" * 64
        self.assertTrue(research_gate.verify_inputs(ROOT, bad))

    def test_physical_blockers_cannot_be_overridden_by_catalogue_go(self):
        report = research_gate.read_contract(ROOT)
        self.assertTrue(report["external_blockers"])
        self.assertEqual(research_gate.overall_status(0, report["external_blockers"]), "NO-GO")
        self.assertEqual(research_gate.overall_status(1, []), "NO-GO")
        self.assertEqual(research_gate.overall_status(0, []), "GO")

    def test_omitted_physical_blocker_or_evidence_fails(self):
        report = research_gate.read_contract(ROOT)
        bad = copy.deepcopy(report)
        bad["external_blockers"] = []
        self.assertTrue(research_gate.verify_inputs(ROOT, bad))
        bad = copy.deepcopy(report)
        bad["evidence_sha256"] = {}
        self.assertTrue(research_gate.verify_inputs(ROOT, bad))

    def test_quantum_signing_boundary_is_stated_in_both_languages(self):
        text = (ROOT / "THREAT_MODEL.md").read_text(encoding="utf-8")
        english, russian = text.split("## Русский", 1)
        for section, terms in ((english, ("quantum", "signature", "migration")),
                               (russian, ("квант", "подпис", "миграц"))):
            with self.subTest(language=terms[0]):
                self.assertTrue(all(term in section.lower() for term in terms))


if __name__ == "__main__":
    unittest.main()
