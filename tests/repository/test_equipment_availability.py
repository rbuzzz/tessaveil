from pathlib import Path
import re
import unittest


REPORT = Path(__file__).resolve().parents[2] / "reports/spikes/equipment-availability.md"
REQUIRED = {
    "clean Windows 10 22H2 x64": ("Task 5", "clean Windows 10", "release evidence", "No Windows 10 target"),
    "clean Windows 11 x64": ("Task 5", "clean Windows 11", "release evidence", "no clean target provenance"),
    "physical arm64 Android 4 GiB lower-bound": ("Task 6", "lower-bound Android", "Argon2id measurements", "No physical device identity"),
    "current mid-range physical Android": ("Task 6", "current Android", "Argon2id measurements", "No current mid-range physical Android model"),
    "physical iPhone 11/A13/4 GiB-class lower-bound": ("Task 6", "lower-bound iPhone", "Argon2id measurements", "physical iPhone class and access were not supplied"),
    "current physical iPhone": ("Task 6", "current iPhone", "Argon2id measurements", "current physical iPhone class and access were not supplied"),
    "Mac/Xcode host": ("Task 6", "iOS build", "physical measurement evidence", "no configured Mac/Xcode host access"),
    "pre-provisioned empty removable device for NTFS and exFAT": ("Task 7", "removable NTFS", "removable exFAT", "No pre-provisioned empty physical media"),
}


class EquipmentAvailabilityReportTests(unittest.TestCase):
    def test_required_equipment_has_terminal_evidence_and_gate(self):
        self.assertTrue(REPORT.is_file(), "equipment availability report is absent")
        lines = REPORT.read_text(encoding="utf-8").splitlines()
        rows = [
            [cell.strip() for cell in line.strip().strip("|").split("|")]
            for line in lines
            if line.startswith("|") and not re.fullmatch(r"[\s|:-]+", line)
        ]
        self.assertGreaterEqual(len(rows), 2)
        self.assertEqual(
            rows[0],
            ["Environment / device class", "Owner", "Access method", "Verified (UTC)", "Status", "Evidence or exact blocker", "Dependent gate"],
        )
        self.assertEqual(len(rows[1:]), len(REQUIRED))
        actual = {row[0]: row for row in rows[1:]}
        self.assertEqual(set(actual), set(REQUIRED))
        for name, row in actual.items():
            with self.subTest(environment=name):
                self.assertEqual(len(row), 7)
                self.assertTrue(all(row[1:]))
                self.assertRegex(row[3], r"^\d{4}-\d{2}-\d{2}$")
                self.assertIn(row[4], {"available", "blocked"})
                if row[4] == "blocked":
                    task, impact_a, impact_b, missing_evidence = REQUIRED[name]
                    self.assertIn(missing_evidence.lower(), row[5].lower())
                    self.assertTrue(row[6].startswith(task + " "))
                    self.assertIn(impact_a, row[6])
                    self.assertIn(impact_b, row[6])
                    self.assertTrue(row[6].endswith("BLOCKED"))

    def test_independent_no_go_decisions_remain_explicit(self):
        self.assertTrue(REPORT.is_file(), "equipment availability report is absent")
        report = REPORT.read_text(encoding="utf-8")
        for decision in (
            "Task 5 — Windows stack selection and release evidence: NO-GO",
            "Task 6 — Vault-format/KDF freeze: NO-GO",
            "Task 7 — Removable NTFS/exFAT atomicity claims: NO-GO",
        ):
            with self.subTest(decision=decision):
                self.assertIn(decision, report)


if __name__ == "__main__":
    unittest.main()
