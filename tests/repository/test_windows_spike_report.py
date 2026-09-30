"""Guard Windows alpha spike evidence; these tests cannot infer a GUI pass."""

import json
from pathlib import Path
import re
import shutil
import subprocess
import unittest


ROOT = Path(__file__).resolve().parents[2]
CANDIDATES = ("Avalonia/NativeAOT", "Slint", "Qt 6")
METRICS = (
    "Exact toolchain versions", "License disposition", "Build / source status",
    "Clean Windows 10", "Clean Windows 11", "Single EXE / file count",
    "PE imports / loaded modules", "Native libraries / runtime prerequisites",
    "%TEMP% before/after", "Accessibility / keyboard focus", "Binary size",
    "Startup measurement", "Virtualized table / themes", "Core boundary",
)


class WindowsSpikeReportTests(unittest.TestCase):
    def test_alpha_measurements_have_reproducible_candidate_evidence(self):
        """Missing measurements must stay unknown; every build needs exact provenance."""
        evidence = json.loads(self.read("spikes/windows/evidence.json"))
        self.assertEqual(evidence["scope"], "development-host; not clean Windows evidence")
        self.assertEqual(set(evidence["candidates"]), {"avalonia-nativeaot", "slint", "qt-static"})
        self.assertFalse(evidence["redistribution_ready"])
        selected = evidence["candidates"][evidence["selected_alpha_candidate"]]
        self.assertEqual(selected["status"], "MEASURED")
        self.assertTrue(selected["uia"]["core_one_visible"])
        self.assertTrue(selected["uia"]["input_set_succeeded"])
        passwords = [control for control in selected["uia"]["controls"] if control["password"]]
        self.assertEqual(len(passwords), 1)
        self.assertFalse(passwords[0]["synthetic_password_exposed"])
        for name, candidate in evidence["candidates"].items():
            with self.subTest(candidate=name):
                self.assertTrue(candidate["toolchains"])
                for tool in candidate["toolchains"]:
                    self.assertRegex(tool["version"], r"\d+\.\d+")
                    self.assertRegex(tool["sha256"], r"^[0-9a-f]{64}$")
                self.assertTrue(candidate["build_command"])
                self.assertTrue(candidate["measurement_command"])
                self.assertIn(candidate["status"], ("MEASURED", "BLOCKED"))
                self.assertIsInstance(candidate["blockers"], list)
                for metric in ("artifacts", "startup_ms", "pe_imports", "temp_before", "temp_after"):
                    if candidate["status"] == "BLOCKED":
                        self.assertIsNone(candidate[metric], metric)
                        self.assertTrue(candidate["blockers"])
                    else:
                        self.assertIsInstance(candidate[metric], list)
                if candidate["status"] == "MEASURED":
                    self.assertTrue(candidate["artifacts"])
                    self.assertGreaterEqual(len(candidate["startup_ms"]), 10)
                    self.assertTrue(all(value > 0 for value in candidate["startup_ms"]))
                    self.assertTrue(candidate["pe_imports"])
                    self.assertEqual(len(candidate["temp_runs"]), len(candidate["startup_ms"]))
                    for observation in candidate["temp_runs"]:
                        self.assertIsInstance(observation["before"], list)
                        self.assertIsInstance(observation["after"], list)
                    for artifact in candidate["artifacts"]:
                        self.assertGreater(artifact["bytes"], 0)
                        self.assertRegex(artifact["sha256"], r"^[0-9a-f]{64}$")
                        self.assertFalse(Path(artifact["path"]).is_absolute())
                self.assertNotRegex(json.dumps(candidate), r"(?<![A-Za-z])[A-Za-z]:[\\/]")

    def read(self, relative):
        path = ROOT / relative
        self.assertTrue(path.is_file(), f"missing Windows spike artifact: {relative}")
        return path.read_text(encoding="utf-8")

    def test_every_candidate_has_explicit_evidence_or_blocker_for_every_metric(self):
        report = self.read("reports/spikes/windows.md")
        rows = {}
        for line in report.splitlines():
            if line.startswith("|"):
                cells = [c.strip() for c in line.strip("|").split("|")]
                if cells[0] in METRICS:
                    self.assertNotIn(cells[0], rows)
                    rows[cells[0]] = cells[1:]
        self.assertEqual(set(rows), set(METRICS))
        self.assertIn("| Metric | " + " | ".join(CANDIDATES) + " |", report)
        for metric, values in rows.items():
            with self.subTest(metric=metric):
                self.assertEqual(len(values), 3)
                for value in values:
                    self.assertRegex(value, r"^(BLOCKED|DOCUMENTED|MEASURED): .+")
                    self.assertNotIn("TBD", value)

    def test_clean_target_blockers_are_copied_without_promotion(self):
        equipment = self.read("reports/spikes/equipment-availability.md")
        report = self.read("reports/spikes/windows.md")
        adr = self.read("docs/adr/0001-desktop-stack.md")
        for environment in ("clean Windows 10 22H2 x64", "clean Windows 11 x64"):
            row = next(line for line in equipment.splitlines() if line.startswith(f"| {environment} |"))
            reason = row.strip("|").split("|")[5].strip()
            for document in (report, adr):
                self.assertIn(reason, document)
        for document in (report, adr):
            self.assertIn("Windows release readiness: NO-GO", document)
            self.assertIn("alpha only", document)
            self.assertIn("not a Windows v1 technology freeze", document)

    def test_release_unknowns_are_not_imputed_as_zero(self):
        report = self.read("reports/spikes/windows.md")
        for criterion in ("Portability", "Dependencies", "Accessibility", "Table performance",
                          "Figma fidelity", "License obligations", "Maintenance", "Rust/UniFFI reuse"):
            self.assertRegex(report, rf"(?m)^\| {re.escape(criterion)} \| \d+ \| U \| U \| U \| .+ \|$")
        self.assertIn("U means unknown, not zero", report)
        self.assertIn("Observed score coverage: 0/8 for each candidate", report)

    def test_equivalent_safe_probe_contract_and_adapter_handoffs(self):
        contract = json.loads(self.read("spikes/windows/probe-contract.json"))
        self.assertEqual(contract["table"], {"rows": 10000, "columns": 36, "cell": "TEST-R{row:05}-C{column:02}", "virtualized": True})
        self.assertEqual(contract["input"], {"masked": True, "test_value": "TEST-INPUT-42!", "persist": False})
        self.assertEqual(contract["themes"], ["light", "dark"])
        self.assertEqual(contract["focus_order"], ["input", "invoke", "theme", "table"])
        self.assertEqual(contract["boundary"], {"name": "probe_core_version", "input": None, "output_u32": 1})
        self.assertEqual(contract["forbidden"], ["cryptography", "mnemonics", "network", "persistent input", "clipboard"])
        for candidate in ("avalonia-nativeaot", "slint", "qt-static"):
            text = self.read(f"spikes/windows/{candidate}/README.md")
            self.assertIn("../probe-contract.json", text)
            self.assertIn("development-host", text.lower())
        for source in ("avalonia-nativeaot/Program.cs", "slint/src/main.rs", "qt-static/main.cpp"):
            self.read(f"spikes/windows/{source}")

    def test_primary_sources_and_static_rust_evidence_are_explicit(self):
        report = self.read("reports/spikes/windows.md")
        for source in ("https://github.com/AvaloniaUI/Avalonia/", "https://github.com/slint-ui/slint/",
                       "https://doc.qt.io/", "https://learn.microsoft.com/"):
            self.assertIn(source, report)
        self.assertIn("Verified (UTC): 2026-09-30", report)
        self.assertIn("Static Rust linkage: BLOCKED", report)
        self.assertIn("SignPath compatibility: pending", report)

    def test_discovery_script_returns_inventory_without_release_approval(self):
        script = ROOT / "spikes/windows/verify.ps1"
        self.assertTrue(script.is_file(), "missing read-only discovery script")
        if not shutil.which("pwsh"):
            self.skipTest("PowerShell unavailable; executable discovery test requires pwsh")
        result = subprocess.run(["pwsh", "-NoProfile", "-File", str(script)],
                                capture_output=True, text=True, timeout=30, check=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data["release_readiness"], "NO-GO")
        self.assertEqual(data["scope"], "read-only discovery; not build or clean-machine evidence")
        self.assertEqual(len(data["commands"]), 13)
        self.assertTrue(all(type(entry["available"]) is bool for entry in data["commands"]))
        self.assertNotRegex(result.stdout, r"[A-Za-z]:[\\/](Users|Дистрибутивы)")


if __name__ == "__main__":
    unittest.main()
