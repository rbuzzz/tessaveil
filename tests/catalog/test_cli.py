"""CLI exit contract for strict and incremental catalogue review."""

from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = Path(__file__).parent / "fixtures" / "valid-minimal"


class CliTests(unittest.TestCase):
    def run_cli(self, root: Path, *args: str):
        return subprocess.run([sys.executable, "-m", "tools.catalog.cli", "validate",
                               "--root", str(root), *args], cwd=ROOT,
                              capture_output=True, text=True, check=False)

    def test_valid_fixture_terminal_and_release_modes(self):
        result = self.run_cli(FIXTURE, "--require-terminal")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        result = self.run_cli(FIXTURE, "--require-release-ready")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("required-blocked", result.stdout)

    def test_incremental_flag_relaxes_pending_only(self):
        result = self.run_cli(ROOT, "--allow-incomplete-required")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("required-pending", result.stdout)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            shutil.copytree(FIXTURE, root, dirs_exist_ok=True)
            wallet = root / "catalog/wallets/synthetic-wallet.json"
            wallet.write_bytes(b"\xff")
            result = self.run_cli(root, "--allow-incomplete-required")
            self.assertNotEqual(result.returncode, 0)
            self.assertNotIn("\xff", result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
