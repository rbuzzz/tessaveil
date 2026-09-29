from pathlib import Path
import re
import unittest


REPORT = Path(__file__).resolve().parents[2] / "reports/spikes/equipment-availability.md"
REQUIRED = {
    "clean Windows 10 22H2 x64",
    "clean Windows 11 x64",
    "physical arm64 Android 4 GiB lower-bound",
    "current mid-range physical Android",
    "physical iPhone 11/A13/4 GiB-class lower-bound",
    "current physical iPhone",
    "Mac/Xcode host",
    "pre-provisioned empty removable device for NTFS and exFAT",
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
        self.assertEqual(set(actual), REQUIRED)
        for name, row in actual.items():
            with self.subTest(environment=name):
                self.assertEqual(len(row), 7)
                self.assertTrue(all(row[1:]))
                self.assertRegex(row[3], r"^\d{4}-\d{2}-\d{2}$")
                self.assertIn(row[4], {"available", "blocked"})
                if row[4] == "blocked":
                    self.assertRegex(row[6], r"Task [567].*BLOCKED")


if __name__ == "__main__":
    unittest.main()
