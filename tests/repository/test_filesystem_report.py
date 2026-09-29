"""Filesystem research contracts; opt-in tests touch only dedicated Public roots.

Breaks caught: unsafe target acceptance, damaged-image acceptance, replacement
before verification, incomplete destination after interruption, overstated claims.
"""
import copy
import hashlib
import json
import os
from pathlib import Path
import shutil
import struct
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[2]
SPIKE = ROOT / "spikes/filesystems"
PHASES = ("AfterCreate", "AfterWrite", "AfterFlush", "AfterVerify", "BeforeReplace", "AfterReplace", "None")
API = "FileStream.CreateNew -> Write -> Flush(true) -> close/reopen -> AES-GCM verify -> File.Replace(no backup, ignoreMetadataErrors=false)"


class FilesystemContracts(unittest.TestCase):
    def assert_interruption_matrix(self, evidence):
        """One contract for both historical evidence and fresh subprocess output."""
        self.assertEqual(evidence["filesystem"], "NTFS")
        self.assertEqual(evidence["device_class"], "local fixed development volume")
        self.assertEqual(evidence["scope"], "process interruption at named boundaries only")
        self.assertEqual(evidence["release_readiness"], "NO-GO")
        self.assertEqual(evidence["api"], API)
        self.assertEqual(evidence["fixture_sha256"], hashlib.sha256(
            (SPIKE / "fixtures/header-and-ciphertext.bin").read_bytes()).hexdigest())
        self.assertEqual(len(evidence["matrix"]), 7)
        self.assertEqual({row["phase"] for row in evidence["matrix"]}, set(PHASES))
        expected = {
            "AfterCreate": ("old", 86, 0, False),
            "AfterWrite": ("old", 86, 0, False),
            "AfterFlush": ("old", 86, 4140, True),
            "AfterVerify": ("old", 86, 4140, True),
            "BeforeReplace": ("old", 86, 4140, True),
            "AfterReplace": ("new", 86, None, None),
            "None": ("new", 0, None, None),
        }
        for row in evidence["matrix"]:
            generation, exit_code, temporary_length, temporary_auth = expected[row["phase"]]
            self.assertIs(row["authenticated"], True)
            self.assertEqual(row["observed"], generation)
            self.assertEqual(row["exit_code"], exit_code)
            self.assertEqual(row["target_length"], 4140)
            self.assertEqual(row["old_sha256"], evidence["fixture_sha256"])
            self.assertNotEqual(row["old_sha256"], row["new_sha256"])
            self.assertRegex(row["new_sha256"], r"^[a-f0-9]{64}$")
            self.assertEqual(row["actual_sha256"], row[generation + "_sha256"])
            self.assertEqual(row["temporary_length"], temporary_length, row["phase"])
            self.assertIs(row["temporary_authenticated"], temporary_auth, row["phase"])
        self.assertIs(evidence["nonempty_rejected"], True)
        self.assertIs(evidence["junction_rejected"], True)

    def assert_report_contract(self, report, evidence):
        self.assert_interruption_matrix(evidence)
        # Closed claim table: no second local row or extra all-NTFS approval row.
        heading = "| Filesystem / device class | Result and claim scope | Exact blocker / policy |"
        self.assertEqual(report.count(heading), 1)
        table = report.split(heading, 1)[1].strip().split("\n\n", 1)[0].splitlines()[1:]
        rows = [[cell.strip() for cell in line.strip().strip("|").split("|")] for line in table]
        names = {"local fixed NTFS", "removable NTFS", "removable exFAT", "FAT32",
                 "network shares", "cloud-sync folders", "untested filesystems"}
        self.assertEqual(len(rows), len(names))
        self.assertEqual({row[0] for row in rows}, names)
        for row in rows:
            self.assertEqual(len(row), 3)
        self.assertEqual(sum(row[0] == "local fixed NTFS" for row in rows), 1)
        local = next(row for row in rows if row[0] == "local fixed NTFS")
        self.assertIn(evidence["os_architecture"], ("64-разрядная", "64-bit"))
        # An allowlisted claim grammar rejects affirmative all-NTFS, removable,
        # power-loss or mid-syscall guarantees even if appended to valid wording.
        self.assertEqual(local[1],
            f"PASS: {evidence['scope']}; {evidence['device_class']}; "
            f"Windows version {evidence['os_version']} x64, build {evidence['os_build']} ({evidence['display_version']}); "
            f"PowerShell {evidence['powershell']}, {evidence['dotnet']}; File.Replace; "
            f"4140-byte images; 7/7 matrix rows; evidence {evidence['verified_utc']}")
        self.assertEqual(local[2], "No all-NTFS, removable-media, power-loss, mid-syscall or general atomicity guarantee; research scope only")
        equipment = (ROOT / "reports/spikes/equipment-availability.md").read_text(encoding="utf-8")
        blocker = next(line.split("|")[6].strip() for line in equipment.splitlines()
                       if line.startswith("| pre-provisioned empty removable device"))
        for name in ("removable NTFS", "removable exFAT"):
            row = next(row for row in rows if row[0] == name)
            self.assertEqual(row[1], "unapproved / NO-GO")
            self.assertEqual(row[2], blocker)
        for name in ("FAT32", "network shares", "cloud-sync folders", "untested filesystems"):
            row = next(row for row in rows if row[0] == name)
            self.assertEqual(row[1], "no atomicity promise")
            self.assertEqual(row[2], "no silent in-place update; read-only or Save As to a separately verified target")


class FilesystemReportTests(FilesystemContracts):
    def test_fixture_is_bounded_header_and_authenticated_ciphertext(self):
        path = SPIKE / "fixtures/header-and-ciphertext.bin"
        self.assertTrue(path.is_file(), "synthetic filesystem fixture absent")
        image = path.read_bytes()
        self.assertEqual(len(image), 4140)
        self.assertEqual(image[:12], b"TVFS0001\x00\x00\x01\x00")
        self.assertEqual(struct.unpack_from("<I", image, 12)[0], 4096)
        self.assertNotEqual(image[16:28], bytes(12))
        self.assertNotIn(b"synthetic", image[28:])
        evidence_path = SPIKE / "local-ntfs-evidence.json"
        self.assertTrue(evidence_path.is_file(), "interruption evidence absent")
        evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
        self.assertEqual(evidence["fixture_sha256"], hashlib.sha256(image).hexdigest())

    def test_claims_require_complete_evidence_and_preserve_equipment_blockers(self):
        path = ROOT / "reports/spikes/filesystem-matrix.md"
        self.assertTrue(path.is_file(), "filesystem matrix absent")
        report = path.read_text(encoding="utf-8")
        evidence = json.loads((SPIKE / "local-ntfs-evidence.json").read_text(encoding="utf-8"))
        self.assert_report_contract(report, evidence)
        for name in ("README.md", "../../docs/adr/0003-filesystem-replace.md"):
            self.assertTrue((SPIKE / name).is_file())


class FilesystemContractMutationTests(FilesystemContracts):
    def setUp(self):
        self.evidence = json.loads((SPIKE / "local-ntfs-evidence.json").read_text(encoding="utf-8"))
        self.report = (ROOT / "reports/spikes/filesystem-matrix.md").read_text(encoding="utf-8")

    def test_rejects_expanded_or_missing_local_claim(self):
        local = next(line for line in self.report.splitlines() if line.startswith("| local "))
        for claim in ("Guaranteed atomic replacement for all NTFS volumes",
                      "Guaranteed atomic replacement for removable NTFS and exFAT",
                      "Guaranteed power-loss durability", "Guaranteed mid-syscall atomicity"):
            with self.subTest(claim=claim):
                cells = local.split("|")
                cells[2] = f" {claim} "
                changed = self.report.replace(local, "|".join(cells))
                with self.assertRaises(AssertionError):
                    self.assert_report_contract(changed, self.evidence)
                # Appending an overclaim must also fail despite a valid prefix.
                cells[2] = local.split("|")[2].rstrip() + f"; {claim} "
                with self.assertRaises(AssertionError):
                    self.assert_report_contract(self.report.replace(local, "|".join(cells)), self.evidence)
        for replacement in ("", local + "\n" + local):
            with self.subTest(replacement="missing" if not replacement else "duplicate"):
                with self.assertRaises(AssertionError):
                    self.assert_report_contract(self.report.replace(local, replacement), self.evidence)
        for name in ("removable NTFS", "removable exFAT"):
            with self.subTest(removable=name):
                row = next(line for line in self.report.splitlines() if line.startswith("| " + name + " |"))
                changed = row.replace("unapproved / NO-GO", "unapproved / NO-GO; guaranteed atomic replacement")
                with self.assertRaises(AssertionError):
                    self.assert_report_contract(self.report.replace(row, changed), self.evidence)

    def test_rejects_unflushed_or_incomplete_temporary_images(self):
        for phase in ("AfterFlush", "AfterVerify", "BeforeReplace"):
            # AfterVerify is the implementation's reopen-and-authenticate phase.
            for length, authenticated in ((0, False), (4139, False), (4140, False)):
                with self.subTest(phase=phase, length=length, authenticated=authenticated):
                    changed = copy.deepcopy(self.evidence)
                    row = next(row for row in changed["matrix"] if row["phase"] == phase)
                    row["temporary_length"] = length
                    row["temporary_authenticated"] = authenticated
                    with self.assertRaises(AssertionError):
                        self.assert_interruption_matrix(changed)

    def test_rejects_report_environment_drift(self):
        for field in ("os_version", "os_build", "display_version", "powershell", "dotnet", "verified_utc"):
            with self.subTest(field=field):
                changed = copy.deepcopy(self.evidence)
                changed[field] = "unmeasured"
                with self.assertRaises(AssertionError):
                    self.assert_report_contract(self.report, changed)

    def test_rejects_matrix_phase_or_target_drift(self):
        mutations = (("phase", "UnknownPhase"), ("phase", "AfterReplace"),
                     ("observed", "new"), ("authenticated", False),
                     ("target_length", 4139), ("exit_code", 0),
                     ("actual_sha256", "0" * 64))
        for field, value in mutations:
            with self.subTest(field=field, value=value):
                changed = copy.deepcopy(self.evidence)
                changed["matrix"][0][field] = value
                with self.assertRaises(AssertionError):
                    self.assert_interruption_matrix(changed)


@unittest.skipUnless(os.name == "nt" and os.environ.get("TESSAVEIL_RUN_FILESYSTEM_PROBE") == "1",
                     "explicit local filesystem probe opt-in required")
class FilesystemProbeTests(FilesystemContracts):
    @classmethod
    def setUpClass(cls):
        cls.pwsh = shutil.which("pwsh")
        if not cls.pwsh:
            raise unittest.SkipTest("PowerShell 7 unavailable")

    def run_ps(self, code):
        self.assertTrue((SPIKE / "ReplaceProbe.ps1").is_file(), "bounded probe absent")
        return subprocess.run([self.pwsh, "-NoProfile", "-NonInteractive", "-Command", code],
                              cwd=ROOT, capture_output=True, text=True, encoding="utf-8", timeout=60)

    def dot(self):
        return ". './spikes/filesystems/ReplaceProbe.ps1'; "

    def test_unsafe_roots_fail_before_any_write(self):
        result = self.run_ps(self.dot() + r"""
          $candidates = @((Get-Location).Path, $HOME, $env:USERPROFILE,
            'C:\', ('C:' + '\Users' + '\Public'), '.', '..', '\\server\share\test',
            '\\?\C:\Users\Public\test', 'C:\Users\Public\OneDrive\test',
            'C:\Users\Public\Dropbox\test', 'C:\Users\Public\*',
            'C:\Users\Public\TessaveilReplaceProbe-00000000000000000000000000000000\..')
          foreach ($candidate in $candidates) {
            try { Invoke-ReplaceProbe -Root $candidate -FailurePhase None; throw 'UNSAFE_ACCEPTED' }
            catch { if ($_.Exception.Message -eq 'UNSAFE_ACCEPTED') { throw } }
          }
          'REJECTED'
        """)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("REJECTED", result.stdout)

    def test_authentication_rejects_every_corrupted_region_and_truncation(self):
        result = self.run_ps(self.dot() + r"""
          $bytes = [IO.File]::ReadAllBytes((Join-Path $PWD 'spikes/filesystems/fixtures/header-and-ciphertext.bin'))
          if (!(Test-ProbeImage $bytes)) { throw 'fixture authentication failed' }
          foreach ($index in @(0,8,9,10,11,12,16,27,28,1024,4123,4124,4139)) {
            $changed = $bytes.Clone(); $changed[$index] = $changed[$index] -bxor 1
            if (Test-ProbeImage $changed) { throw 'corruption accepted' }
          }
          if (Test-ProbeImage ([byte[]]$bytes[0..4138])) { throw 'truncation accepted' }
          if (Test-ProbeImage ([byte[]]($bytes + 0))) { throw 'trailing byte accepted' }
          'AUTHENTICATED'
        """)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("AUTHENTICATED", result.stdout)

    def test_real_process_interruption_preserves_complete_authenticated_image(self):
        result = self.run_ps(self.dot() + "& './spikes/filesystems/Test-ReplaceProbe.ps1'")
        self.assertEqual(result.returncode, 0, result.stderr)
        matrix = json.loads(result.stdout)
        self.assert_interruption_matrix(matrix)


if __name__ == "__main__":
    unittest.main()
