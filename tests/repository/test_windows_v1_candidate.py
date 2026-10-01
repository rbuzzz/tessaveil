"""Exact-candidate names, external manifest and packaged guidance contracts."""

import copy
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "packaging/windows"))

SPEC = importlib.util.spec_from_file_location(
    "candidate_manifest", ROOT / "packaging/windows/candidate_manifest.py"
)
candidate_manifest = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(candidate_manifest)

import alpha


class WindowsV1CandidateTests(unittest.TestCase):
    SHA = "a" * 40

    def test_names_are_conspicuously_unsigned_synthetic_and_exact_sha_bound(self):
        names = candidate_manifest.names(self.SHA)
        base = f"Tessaveil-unsigned-synthetic-windows-v1-candidate-{self.SHA}"
        self.assertEqual(
            names,
            {
                "container": base,
                "runtime": base + "-runtime.zip",
                "compliance": base + "-compliance.zip",
                "decision": base + "-release-decision.json",
                "manifest": base + "-manifest.json",
            },
        )
        for invalid in ("", "A" * 40, "a" * 39, "a" * 41, "../" + "a" * 40):
            with self.subTest(source_sha=invalid), self.assertRaisesRegex(
                ValueError, "source SHA"
            ):
                candidate_manifest.names(invalid)

    def test_external_manifest_binds_names_sizes_and_hashes_for_every_required_subject(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            names = candidate_manifest.names(self.SHA)
            runtime_path = root / names["runtime"]
            compliance_path = root / names["compliance"]
            decision_path = root / names["decision"]
            executable = b"MZ-public-synthetic-executable"
            sbom = b'{"bomFormat":"CycloneDX","specVersion":"1.6"}\n'
            notices = b"Public third-party notices\n"
            alpha.write_archive(
                runtime_path,
                {
                    "Tessaveil.exe": executable,
                    "sbom.cdx.json": sbom,
                    "THIRD_PARTY_NOTICES": notices,
                },
            )
            alpha.write_archive(compliance_path, {"SOURCE_SHA": (self.SHA + "\n").encode()})
            decision_path.write_bytes(
                json.dumps(
                    {
                        "verdict": "NO-GO для реальных данных",
                        "candidate": {"source_sha": self.SHA},
                    }
                ).encode()
            )

            report = candidate_manifest.materialize(
                self.SHA, runtime_path, compliance_path, decision_path
            )
            candidate_manifest.validate_exact_candidate(
                report, self.SHA, runtime_path, compliance_path, decision_path
            )

            self.assertEqual(report["candidate"]["name"], names["container"])
            self.assertIs(report["candidate"]["unsigned"], True)
            self.assertIs(report["candidate"]["synthetic_only"], True)
            self.assertIs(report["candidate"]["real_data_authorized"], False)
            self.assertEqual(
                report["candidate"]["verdict"], "NO-GO для реальных данных"
            )
            self.assertEqual(
                report["provenance_subjects"],
                [names["runtime"], names["compliance"], names["decision"], names["manifest"]],
            )
            expected = {
                "runtime_zip": (names["runtime"], runtime_path.read_bytes()),
                "compliance_zip": (names["compliance"], compliance_path.read_bytes()),
                "release_decision": (names["decision"], decision_path.read_bytes()),
                "executable": ("Tessaveil.exe", executable),
                "sbom": ("sbom.cdx.json", sbom),
                "notices": ("THIRD_PARTY_NOTICES", notices),
            }
            for key, (filename, payload) in expected.items():
                with self.subTest(artifact=key):
                    record = report["artifacts"][key]
                    self.assertEqual(record["filename"], filename)
                    self.assertEqual(record["bytes"], len(payload))
                    self.assertEqual(record["sha256"], alpha.digest(payload))

            changed = copy.deepcopy(report)
            changed["artifacts"]["runtime_zip"]["sha256"] = "b" * 64
            with self.assertRaisesRegex(ValueError, "manifest"):
                candidate_manifest.validate_exact_candidate(
                    changed, self.SHA, runtime_path, compliance_path, decision_path
                )
            runtime_path.write_bytes(runtime_path.read_bytes() + b"changed")
            with self.assertRaisesRegex(ValueError, "manifest"):
                candidate_manifest.validate_exact_candidate(
                    report, self.SHA, runtime_path, compliance_path, decision_path
                )

    def test_compliance_guidance_is_exact_source_material(self):
        material = candidate_manifest.guidance_material(ROOT)
        self.assertEqual(
            set(material),
            {
                "candidate-docs/README.md",
                "candidate-docs/README.ru.md",
                "candidate-docs/THREAT_MODEL.md",
                "candidate-docs/user-guide.md",
                "candidate-docs/known-limitations.md",
                "candidate-docs/release-evidence.md",
                "candidate-docs/test-protocols.md",
            },
        )
        candidate_manifest.verify_guidance_material(material, ROOT)
        changed = dict(material)
        changed["candidate-docs/known-limitations.md"] += b"drift"
        with self.assertRaisesRegex(ValueError, "guidance"):
            candidate_manifest.verify_guidance_material(changed, ROOT)

    def test_hosted_pipeline_uses_exact_candidate_names_manifest_and_four_provenance_subjects(self):
        workflow = json.loads((ROOT / ".github/workflows/windows-alpha.yml").read_bytes())
        expected_base = (
            "Tessaveil-unsigned-synthetic-windows-v1-candidate-${{ github.sha }}"
        )
        build_steps = workflow["jobs"]["windows-alpha"]["steps"]
        upload = next(
            step
            for step in build_steps
            if step.get("uses", "").startswith("actions/upload-artifact@")
        )
        self.assertEqual(upload["with"]["name"], expected_base)
        upload_paths = set(upload["with"]["path"].splitlines())
        self.assertEqual(
            upload_paths,
            {
                "${{ env.ALPHA_ROOT }}/alpha-output/" + expected_base + "-runtime.zip",
                "${{ env.ALPHA_ROOT }}/alpha-output/" + expected_base + "-compliance.zip",
                "${{ env.ALPHA_ROOT }}/alpha-output/" + expected_base + "-release-decision.json",
                "${{ env.ALPHA_ROOT }}/alpha-output/" + expected_base + "-manifest.json",
            },
        )
        provenance = workflow["jobs"]["provenance"]["steps"]
        download = next(
            step
            for step in provenance
            if step.get("uses", "").startswith("actions/download-artifact@")
        )
        self.assertEqual(download["with"]["name"], expected_base)
        attest = next(
            step
            for step in provenance
            if step.get("uses", "").startswith("actions/attest@")
        )
        self.assertEqual(
            set(attest["with"]["subject-path"].splitlines()),
            {
                "verified-artifact/" + expected_base + "-runtime.zip",
                "verified-artifact/" + expected_base + "-compliance.zip",
                "verified-artifact/" + expected_base + "-release-decision.json",
                "verified-artifact/" + expected_base + "-manifest.json",
            },
        )
        strict = next(
            step
            for step in provenance
            if step.get("name") == "Strict machine-readable attestation verification"
        )
        self.assertIn("--manifest", strict["run"])
        self.assertIn("-manifest.json", strict["run"])

    def test_packaging_sources_require_manifest_and_verified_candidate_guidance(self):
        finish = (ROOT / "packaging/windows/finish.py").read_text(encoding="utf-8")
        gate = (ROOT / "packaging/windows/gate.ps1").read_text(encoding="utf-8")
        verifier = (ROOT / "packaging/windows/verify.py").read_text(encoding="utf-8")
        inventory = json.loads(
            (ROOT / "packaging/windows/compliance-inventory.json").read_bytes()
        )
        self.assertIn("candidate_manifest.materialize", finish)
        self.assertIn("manifest_path=manifest_path", finish)
        self.assertIn("candidate_manifest.names", gate)
        self.assertIn("--manifest", gate)
        self.assertIn("candidate_manifest.validate_exact_candidate", verifier)
        self.assertIn("candidate_manifest.verify_guidance_material", verifier)
        for name in candidate_manifest.guidance_material(ROOT):
            with self.subTest(name=name):
                self.assertIn(name, inventory)


if __name__ == "__main__":
    unittest.main()
