"""Filesystem research contracts; opt-in tests touch only dedicated Public roots.

Breaks caught: unsafe target acceptance, damaged-image acceptance, replacement
before verification, incomplete destination after interruption, overstated claims.
"""
import hashlib
import json
import os
from pathlib import Path
import shutil
import struct
import subprocess
import unittest
import uuid

ROOT = Path(__file__).resolve().parents[2]
SPIKE = ROOT / "spikes/filesystems"
PHASES = ("AfterCreate", "AfterWrite", "AfterFlush", "AfterVerify", "BeforeReplace", "AfterReplace", "None")


class FilesystemReportTests(unittest.TestCase):
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
        equipment = (ROOT / "reports/spikes/equipment-availability.md").read_text(encoding="utf-8")
        blocker = next(line.split("|")[6].strip() for line in equipment.splitlines()
                       if line.startswith("| pre-provisioned empty removable device"))
        for name in ("removable NTFS", "removable exFAT"):
            row = next(line for line in report.splitlines() if line.startswith("| " + name + " |"))
            self.assertIn(blocker, row)
            self.assertIn("unapproved / NO-GO", row)
        for name in ("FAT32", "network shares", "cloud-sync folders", "untested filesystems"):
            row = next(line for line in report.splitlines() if line.startswith("| " + name + " |"))
            self.assertIn("no atomicity promise", row)
            self.assertIn("no silent in-place update", row)
        evidence = json.loads((SPIKE / "local-ntfs-evidence.json").read_text(encoding="utf-8"))
        self.assertEqual(evidence["filesystem"], "NTFS")
        self.assertEqual(evidence["device_class"], "local fixed development volume")
        self.assertEqual(evidence["scope"], "process interruption at named boundaries only")
        self.assertEqual(evidence["release_readiness"], "NO-GO")
        self.assertEqual({row["phase"] for row in evidence["matrix"]}, set(PHASES))
        for row in evidence["matrix"]:
            self.assertTrue(row["authenticated"])
            self.assertEqual(row["observed"], "new" if row["phase"] in ("AfterReplace", "None") else "old")
            self.assertEqual(row["exit_code"], 0 if row["phase"] == "None" else 86)
            self.assertEqual(row["target_length"], 4140)
            self.assertEqual(row["old_sha256"], evidence["fixture_sha256"])
            self.assertNotEqual(row["old_sha256"], row["new_sha256"])
            self.assertRegex(row["new_sha256"], r"^[a-f0-9]{64}$")
            self.assertEqual(row["actual_sha256"], row[row["observed"] + "_sha256"])
            temporary = {"AfterCreate": (0, False), "AfterWrite": (0, False),
                         "AfterFlush": (4140, True), "AfterVerify": (4140, True),
                         "BeforeReplace": (4140, True), "AfterReplace": (None, None), "None": (None, None)}
            self.assertEqual((row["temporary_length"], row["temporary_authenticated"]), temporary[row["phase"]])
        for name in ("README.md", "../../docs/adr/0003-filesystem-replace.md"):
            self.assertTrue((SPIKE / name).is_file())


@unittest.skipUnless(os.name == "nt" and os.environ.get("TESSAVEIL_RUN_FILESYSTEM_PROBE") == "1",
                     "explicit local filesystem probe opt-in required")
class FilesystemProbeTests(unittest.TestCase):
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
            'C:\', 'C:\Users\Public', '.', '..', '\\server\share\test',
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
        self.assertEqual(len(matrix["matrix"]), 7)
        for row in matrix["matrix"]:
            self.assertTrue(row["authenticated"])
            self.assertEqual(row["observed"], "new" if row["phase"] in ("AfterReplace", "None") else "old")
        self.assertTrue(matrix["nonempty_rejected"])
        self.assertTrue(matrix["junction_rejected"])


if __name__ == "__main__":
    unittest.main()
