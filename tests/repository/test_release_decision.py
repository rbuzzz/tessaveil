"""Fail-closed Windows v1 release-decision contracts."""

import copy
import hashlib
import importlib.util
import inspect
import json
from pathlib import Path
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location(
    "release_decision", ROOT / "packaging/windows/release_decision.py"
)
release_decision = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(release_decision)


class ReleaseDecisionTests(unittest.TestCase):
    def setUp(self):
        self.template_path = ROOT / "reports/windows-v1/release-decision.json"
        self.template = json.loads(self.template_path.read_text(encoding="utf-8"))

    def test_committed_policy_ledger_is_complete_honest_and_not_sha_claiming(self):
        validated = release_decision.validate(self.template, template=True)
        self.assertEqual(validated["verdict"], "NO-GO для реальных данных")
        self.assertEqual(validated["candidate"]["kind"], "policy-template")
        self.assertIsNone(validated["candidate"]["source_sha"])
        self.assertEqual(
            {row["id"] for row in validated["gates"]},
            set(release_decision.MANDATORY_GATE_IDS),
        )
        self.assertTrue(all("receipts" in row["evidence"] for row in validated["gates"]))

    def test_independent_tsvalpha_fixture_metadata_binds_generator_and_bytes(self):
        fixture_root = ROOT / "crates/tessaveil-core/tests/fixtures"
        metadata = json.loads((fixture_root / "tsvalpha-schema2.json").read_text())
        image = bytes.fromhex((fixture_root / "tsvalpha-schema2.hex").read_text())
        generator = ROOT / metadata["generator"]["path"]
        requirements = ROOT / metadata["generator"]["requirements_path"]
        self.assertEqual(len(image), metadata["fixture_bytes"])
        self.assertEqual(hashlib.sha256(image).hexdigest(), metadata["fixture_sha256"])
        self.assertEqual(hashlib.sha256(generator.read_bytes()).hexdigest(), metadata["generator"]["sha256"])
        self.assertEqual(hashlib.sha256(requirements.read_bytes()).hexdigest(), metadata["generator"]["requirements_sha256"])
        pinned = {
            name.lower(): version
            for name, version in (
                line.split("==", 1)
                for line in requirements.read_text(encoding="utf-8").splitlines()
                if line
            )
        }
        self.assertEqual(
            pinned,
            {name.lower(): version for name, version in metadata["generator"]["packages"].items()},
        )
        self.assertEqual(
            {name.lower() for name in metadata["generator"]["sources"]}, set(pinned)
        )
        self.assertEqual(image[:10], b"TSVALPHA\x02\x00")
        self.assertIn("outside RustCrypto", metadata["generator"]["independence"])

    def test_policy_evidence_hashes_bind_the_first_repository_reference(self):
        for row in self.template["gates"]:
            reference = ROOT / row["evidence"]["references"][0]
            with self.subTest(gate=row["id"], reference=reference):
                self.assertTrue(reference.is_file())
                self.assertEqual(
                    hashlib.sha256(reference.read_bytes()).hexdigest(),
                    row["evidence"]["sha256"],
                )

    def test_external_gate_protocol_is_operator_ready_and_non_destructive(self):
        protocol = (ROOT / "reports/windows-v1/test-protocols.md").read_text(
            encoding="utf-8"
        )
        for gate_id in release_decision.MANDATORY_GATE_IDS:
            with self.subTest(gate=gate_id):
                self.assertIn(f"`{gate_id}`", protocol)
        for pin in (
            "Rust 1.90.0",
            "Python 3.12.10",
            "PowerShell 7.6.5",
            "cargo-fuzz 0.13.2",
            "Process Monitor 4.11",
            "Android SDK Platform-Tools 37.0.1",
            "Android NDK 30.0.16248370",
            "Xcode 26.5",
            "Windows SDK 10.0.26100.9169",
        ):
            with self.subTest(pin=pin):
                self.assertIn(pin, protocol)
        for command in (
            "Get-FileHash",
            "python packaging/windows/release_decision.py verify",
            "--require-real-data --evidence-root",
            "pktmon start",
            "Procmon64.exe",
            "adb shell",
            "xcodebuild -version",
            "signtool.exe verify",
            "gh run watch",
            "gh attestation verify",
        ):
            with self.subTest(command=command):
                self.assertIn(command, protocol)
        self.assertIn("60 minutes per fuzz target", protocol)
        self.assertIn("AfterCreate, AfterWrite, AfterFlush, AfterVerify, BeforeReplace, AfterReplace", protocol)
        self.assertIn("GitHub-hosted runner windows-2022", protocol)
        self.assertIn("receipts/<gate-id>.json", protocol)
        for forbidden in ("Format-Volume", "format.com", "diskpart /s"):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, protocol)

    def test_integrity_rejects_missing_duplicate_unknown_result_or_verdict(self):
        cases = []
        missing = copy.deepcopy(self.template)
        missing["gates"].pop()
        cases.append(missing)
        duplicate = copy.deepcopy(self.template)
        duplicate["gates"][-1] = copy.deepcopy(duplicate["gates"][0])
        cases.append(duplicate)
        unknown = copy.deepcopy(self.template)
        unknown["gates"][0]["id"] = "invented-gate"
        cases.append(unknown)
        result = copy.deepcopy(self.template)
        result["gates"][0]["result"] = "pending"
        cases.append(result)
        evidence = copy.deepcopy(self.template)
        evidence["gates"][0]["evidence"].pop("environment")
        cases.append(evidence)
        verdict = copy.deepcopy(self.template)
        verdict["verdict"] = "GO"
        cases.append(verdict)
        for report in cases:
            with self.subTest(report=report), self.assertRaises(ValueError):
                release_decision.validate(report, template=True)

    def test_integrity_rejects_malformed_types_without_an_unhandled_exception(self):
        mutations = [
            ("schema version", ("schema_version",), True),
            ("candidate source", ("candidate", "source_sha"), 7),
            ("gate id", ("gates", 0, "id"), []),
            ("evidence hash", ("gates", 0, "evidence", "sha256"), None),
            ("evidence date", ("gates", 0, "evidence", "date"), 20261001),
        ]
        for label, path, replacement in mutations:
            report = copy.deepcopy(self.template)
            cursor = report
            for component in path[:-1]:
                cursor = cursor[component]
            cursor[path[-1]] = replacement
            with self.subTest(label=label), self.assertRaises(ValueError):
                release_decision.validate(report, template=True)

    def test_exact_candidate_rejects_stale_sha_hash_drift_and_development_substitution(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            runtime = root / "runtime.zip"
            compliance = root / "compliance.zip"
            executable = root / "Tessaveil.exe"
            runtime.write_bytes(b"synthetic-runtime")
            compliance.write_bytes(b"synthetic-compliance")
            executable.write_bytes(b"MZ-synthetic-executable")
            sha = "a" * 40
            report = release_decision.materialize(
                self.template, sha, runtime, compliance, executable
            )
            release_decision.validate_exact_candidate(
                report, sha, runtime, compliance, executable
            )

            with self.assertRaisesRegex(ValueError, "source SHA"):
                release_decision.validate_exact_candidate(
                    report, "b" * 40, runtime, compliance, executable
                )
            runtime.write_bytes(b"drift")
            with self.assertRaisesRegex(ValueError, "hash"):
                release_decision.validate_exact_candidate(
                    report, sha, runtime, compliance, executable
                )

            runtime.write_bytes(b"synthetic-runtime")
            substituted = copy.deepcopy(report)
            row = next(
                row for row in substituted["gates"] if row["id"] == "clean-windows-11"
            )
            row["result"] = "pass"
            row["blocker"] = None
            row["clearance_action"] = None
            row["evidence"]["environment"] = "Windows 11 development host"
            with self.assertRaisesRegex(ValueError, "development-host"):
                release_decision.validate_exact_candidate(
                    substituted, sha, runtime, compliance, executable
                )

    def test_hosted_github_evidence_is_only_valid_for_ci_and_provenance_gates(self):
        report = copy.deepcopy(self.template)
        environment = "GitHub-hosted runner windows-2022"
        for gate_id in ("exact-sha-ci", "github-provenance"):
            row = next(row for row in report["gates"] if row["id"] == gate_id)
            row["result"] = "pass"
            row["blocker"] = None
            row["clearance_action"] = None
            row["evidence"]["environment"] = environment
            row["evidence"]["scope"] = "exact event SHA hosted verification"
        release_decision.validate(report, template=True)

        development = copy.deepcopy(report)
        row = next(row for row in development["gates"] if row["id"] == "exact-sha-ci")
        row["evidence"]["environment"] = "Windows development host"
        with self.assertRaisesRegex(ValueError, "GitHub-hosted"):
            release_decision.validate(development, template=True)

        substituted = copy.deepcopy(report)
        row = next(row for row in substituted["gates"] if row["id"] == "clean-windows-11")
        row["result"] = "pass"
        row["blocker"] = None
        row["clearance_action"] = None
        row["evidence"]["environment"] = environment
        with self.assertRaisesRegex(ValueError, "development-host"):
            release_decision.validate(substituted, template=True)

    def test_real_data_mode_fails_until_every_mandatory_gate_passes(self):
        release_decision.validate(self.template, template=True)
        with self.assertRaisesRegex(ValueError, "real-data"):
            release_decision.require_real_data(self.template)

        self.assertIn(
            "evidence_root", inspect.signature(release_decision.require_real_data).parameters
        )

        all_pass = copy.deepcopy(self.template)
        all_pass["candidate"] = {
            "kind": "exact-candidate",
            "source_sha": "a" * 40,
            "artifacts": {
                name: {"sha256": hashlib.sha256(name.encode()).hexdigest()}
                for name in ("runtime", "compliance", "executable")
            },
            "provenance_subject_sha256": [
                hashlib.sha256(b"runtime").hexdigest(),
                hashlib.sha256(b"compliance").hexdigest(),
            ],
        }
        for row in all_pass["gates"]:
            row["result"] = "pass"
            row["blocker"] = None
            row["clearance_action"] = None
            row["evidence"]["scope"] = "independent exact-candidate evidence"
            row["evidence"]["environment"] = (
                release_decision.HOSTED_GITHUB_ENVIRONMENT
                if row["id"] in release_decision.HOSTED_GITHUB_GATES
                else "verified external environment"
            )
            row["evidence"]["receipts"] = []
        all_pass["verdict"] = release_decision.REAL_DATA_VERDICT

        with tempfile.TemporaryDirectory() as directory:
            evidence_root = Path(directory)
            for row in all_pass["gates"]:
                relative = f"receipts/{row['id']}.json"
                receipt = {
                    "schema_version": 1,
                    "gate_id": row["id"],
                    "result": "pass",
                    "candidate": copy.deepcopy(all_pass["candidate"]),
                    "scope": row["evidence"]["scope"],
                    "environment": row["evidence"]["environment"],
                    "date": row["evidence"]["date"],
                }
                path = evidence_root / relative
                path.parent.mkdir(exist_ok=True)
                path.write_text(
                    json.dumps(receipt, ensure_ascii=False, sort_keys=True) + "\n",
                    encoding="utf-8",
                )
                receipt_hash = hashlib.sha256(path.read_bytes()).hexdigest()
                row["evidence"]["sha256"] = receipt_hash
                row["evidence"]["receipts"] = [
                    {"path": relative, "sha256": receipt_hash}
                ]

            release_decision.validate(all_pass)
            with self.assertRaisesRegex(ValueError, "evidence root"):
                release_decision.require_real_data(all_pass)

            reference_only = copy.deepcopy(all_pass)
            reference_only["gates"][0]["evidence"]["receipts"] = []
            with self.assertRaisesRegex(ValueError, "receipt"):
                release_decision.require_real_data(reference_only, evidence_root)

            release_decision.require_real_data(all_pass, evidence_root)

            first = all_pass["gates"][0]["evidence"]["receipts"][0]
            first_path = evidence_root / first["path"]
            original = first_path.read_bytes()
            first_path.unlink()
            with self.assertRaisesRegex(ValueError, "missing"):
                release_decision.require_real_data(all_pass, evidence_root)
            first_path.write_bytes(original + b"drift")
            with self.assertRaisesRegex(ValueError, "hash"):
                release_decision.require_real_data(all_pass, evidence_root)

            receipt = json.loads(original)
            receipt["candidate"]["source_sha"] = "b" * 40
            first_path.write_text(
                json.dumps(receipt, ensure_ascii=False, sort_keys=True) + "\n",
                encoding="utf-8",
            )
            changed_hash = hashlib.sha256(first_path.read_bytes()).hexdigest()
            first["sha256"] = changed_hash
            all_pass["gates"][0]["evidence"]["sha256"] = changed_hash
            with self.assertRaisesRegex(ValueError, "candidate"):
                release_decision.require_real_data(all_pass, evidence_root)

        unbound = copy.deepcopy(all_pass)
        unbound["candidate"] = copy.deepcopy(self.template["candidate"])
        release_decision.validate(unbound, template=True)
        with self.assertRaisesRegex(ValueError, "exact candidate"):
            release_decision.require_real_data(unbound, Path("unused"))


if __name__ == "__main__":
    unittest.main()
