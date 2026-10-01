"""Behavioral packaging boundaries: reject bad bytes before publication."""

import importlib.util
import copy
import json
from pathlib import Path
import tempfile
import struct
import sys
import unittest
import warnings
import zipfile

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "packaging/windows"))
SPEC = importlib.util.spec_from_file_location("alpha_package", ROOT / "packaging/windows/alpha.py")
alpha = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(alpha)


class WindowsAlphaPackageTests(unittest.TestCase):
    @staticmethod
    def observation(exe_sha="b" * 64):
        return {"source_sha": "a" * 40, "exe_sha256": exe_sha, "scale": "1",
                "password_observations": [{"getter": "OBSERVED_MASKED", "setter": "SET", "password": True}] * 2,
                "all_five_password_controls_masked": True, "keyboard_focus_observed": True,
                "open_close_reopen_lock": True, "authentication_safe": True,
                "modules": ["Tessaveil.exe", "KERNEL32.dll"],
                "scope": "Development host UIA only; no clean Windows, Narrator, clipboard contents, network trace or release claim"}

    def test_observation_rejects_empty_false_missing_malformed_and_stale_receipts(self):
        good = self.observation()
        alpha.check_observation(good, "a" * 40, "b" * 64)
        bad = [{}, dict(good, source_sha="c" * 40), dict(good, exe_sha256="d" * 64),
               dict(good, password_observations=[]), dict(good, modules=[]),
               dict(good, scale="9"), dict(good, scope=""),
               dict(good, password_observations=[{"getter": "EXPOSED", "setter": "SET", "password": True}] * 2)]
        for key in ("all_five_password_controls_masked", "keyboard_focus_observed", "open_close_reopen_lock", "authentication_safe"):
            bad.extend([dict(good, **{key: False}), dict(good, **{key: 1}), {k: v for k, v in good.items() if k != key}])
        for value in bad:
            with self.subTest(value=value), self.assertRaisesRegex(ValueError, "observation"):
                alpha.check_observation(value, "a" * 40, "b" * 64)

    def test_sbom_rejects_schema_valid_incomplete_substituted_or_disconnected_graph(self):
        expected = {"bomFormat": "CycloneDX", "specVersion": "1.6", "version": 1,
                    "metadata": {"component": {"type": "application", "bom-ref": "Tessaveil", "name": "Tessaveil", "version": "a" * 40}},
                    "components": [{"type": "library", "bom-ref": "pkg:cargo/example@1.0.0", "name": "example", "version": "1.0.0",
                                    "licenses": [{"expression": "MIT"}], "hashes": [{"alg": "SHA-256", "content": "b" * 64}]}],
                    "dependencies": [{"ref": "Tessaveil", "dependsOn": ["pkg:cargo/example@1.0.0"]}, {"ref": "pkg:cargo/example@1.0.0", "dependsOn": []}]}
        alpha.check_sbom(expected, copy.deepcopy(expected))
        invalid = [{"bomFormat": "CycloneDX", "specVersion": "1.6", "version": 1}]
        for key in ("components", "dependencies"):
            value = copy.deepcopy(expected)
            value[key] = []
            invalid.append(value)
        for key, replacement in (("version", "2.0.0"), ("licenses", [{"expression": "GPL-3.0-only"}]),
                                 ("hashes", [{"alg": "SHA-256", "content": "c" * 64}]), ("bom-ref", "substituted")):
            value = copy.deepcopy(expected)
            value["components"][0][key] = replacement
            invalid.append(value)
        for refs in ([], ["missing"]):
            value = copy.deepcopy(expected)
            value["dependencies"][0]["dependsOn"] = refs
            invalid.append(value)
        value = copy.deepcopy(expected)
        value["metadata"]["component"]["version"] = "d" * 40
        invalid.append(value)
        for value in invalid:
            with self.subTest(value=value), self.assertRaisesRegex(ValueError, "SBOM"):
                alpha.check_sbom(value, expected)

    def test_sbom_source_inventory_rejects_live_license_or_dependency_graph_drift(self):
        spec = importlib.util.spec_from_file_location("alpha_sbom", ROOT / "packaging/windows/sbom.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        metadata = {"packages": [{"id": "local-app", "name": "application", "version": "1.0.0", "source": None, "license": "Apache-2.0"},
                                 {"id": "registry-lib", "name": "library", "version": "2.0.0", "source": "registry", "license": "MIT"}],
                    "resolve": {"nodes": [{"id": "local-app", "dependencies": ["registry-lib"]}, {"id": "registry-lib", "dependencies": []}]}}
        expected = {"packages": [{"id": "pkg:cargo/application@1.0.0", "name": "application", "version": "1.0.0", "source": None, "license": "Apache-2.0"},
                                 {"id": "pkg:cargo/library@2.0.0", "name": "library", "version": "2.0.0", "source": "registry", "license": "MIT"}],
                    "resolve": {"nodes": [{"id": "pkg:cargo/application@1.0.0", "dependencies": ["pkg:cargo/library@2.0.0"]}, {"id": "pkg:cargo/library@2.0.0", "dependencies": []}]}}
        self.assertEqual(module.normalize_metadata(metadata), expected)
        module.check_metadata(metadata, expected)
        for field in ("license", "graph"):
            changed = copy.deepcopy(metadata)
            if field == "license":
                changed["packages"][1]["license"] = "GPL-3.0-only"
            else:
                changed["resolve"]["nodes"][0]["dependencies"] = []
            with self.subTest(field=field), self.assertRaisesRegex(ValueError, "inventory"):
                module.check_metadata(changed, expected)

    def test_clean_ci_fetches_complete_locked_graph_before_offline_packaging(self):
        script = (ROOT / "packaging/windows/ci.ps1").read_text()
        self.assertIn("cargo fetch --locked\n", script)
        self.assertLess(script.index("cargo fetch --locked"), script.index("cargo clippy"))
        fetch_line = next(line for line in script.splitlines() if "cargo fetch" in line)
        self.assertNotIn("--target", fetch_line)
        self.assertIn("if($LASTEXITCODE){throw 'Complete locked Cargo fetch failed'}", script)

    def test_headful_gate_fails_closed_with_foreground_owner_diagnostics(self):
        observer = (ROOT / "apps/tessaveil-windows/tests/observe.ps1").read_text()
        self.assertIn("candidateValid=", observer)
        self.assertIn("foregroundName=", observer)
        self.assertIn("if($stable -lt 4){throw", observer)
        self.assertIn("could not retain foreground", observer)
        self.assertNotIn("LockApp", observer)

    def test_compliance_inventory_rejects_unrelated_files_even_with_valid_manifest(self):
        files = {"SOURCE_SHA": b"public", "application/main.obj": b"public"}
        alpha.verify_inventory(files, sorted(files))
        with self.assertRaisesRegex(ValueError, "inventory"):
            alpha.verify_inventory(dict(files, unrelated=b"public"), sorted(files))
        with self.assertRaisesRegex(ValueError, "inventory"):
            alpha.verify_inventory(files, ["SOURCE_SHA"])

    def test_workflow_exact_sha_windows_gate_precedes_upload_and_official_provenance_is_least_privilege(self):
        workflow = json.loads((ROOT / ".github/workflows/windows-alpha.yml").read_bytes())
        self.assertEqual(workflow["on"]["push"]["branches"], ["feature/windows-alpha"])
        self.assertIn("pull_request", workflow["on"])
        self.assertIn("workflow_dispatch", workflow["on"])
        self.assertEqual(workflow["permissions"], {"contents": "read"})
        build = workflow["jobs"]["windows-alpha"]
        self.assertEqual(build["runs-on"], "windows-2022")
        self.assertEqual(build["steps"][0]["with"]["ref"], "${{ github.sha }}")
        self.assertFalse(build["steps"][0]["with"]["persist-credentials"])
        upload = next(i for i, step in enumerate(build["steps"]) if step.get("uses", "").startswith("actions/upload-artifact@"))
        self.assertIn("GATE-PASS.json", build["steps"][upload - 1]["run"])
        self.assertIn("($kind + '_sha256')", build["steps"][upload - 1]["run"])
        self.assertIn("manifest", build["steps"][upload - 1]["run"])
        self.assertNotIn("if", build["steps"][upload])
        self.assertEqual(build["steps"][upload]["with"]["if-no-files-found"], "error")
        self.assertIn("release-decision.json", build["steps"][upload]["with"]["path"])
        self.assertIn("-manifest.json", build["steps"][upload]["with"]["path"])
        provenance = workflow["jobs"]["provenance"]
        self.assertEqual(provenance["needs"], ["windows-alpha"])
        self.assertEqual(provenance["permissions"], {"contents": "read", "id-token": "write", "attestations": "write"})
        provenance_steps = provenance["steps"]
        provenance_checkouts = [
            (index, step)
            for index, step in enumerate(provenance_steps)
            if step.get("uses", "").startswith("actions/checkout@")
        ]
        self.assertEqual(len(provenance_checkouts), 1)
        checkout_index, checkout = provenance_checkouts[0]
        self.assertEqual(checkout["with"]["ref"], "${{ github.sha }}")
        self.assertEqual(checkout["with"]["fetch-depth"], 1)
        self.assertFalse(checkout["with"]["persist-credentials"])
        attest = next(step for step in provenance["steps"] if step.get("uses", "").startswith("actions/attest@"))
        self.assertEqual(attest["with"].get("create-storage-record"), False)
        self.assertIn("-runtime.zip", attest["with"]["subject-path"])
        self.assertIn("-compliance.zip", attest["with"]["subject-path"])
        self.assertIn("-release-decision.json", attest["with"]["subject-path"])
        self.assertIn("-manifest.json", attest["with"]["subject-path"])
        self.assertFalse(any(key.startswith("predicate") for key in attest["with"]))
        strict = next(step for step in provenance["steps"] if step.get("name") == "Strict machine-readable attestation verification")
        self.assertLess(checkout_index, provenance_steps.index(strict))
        self.assertIn("--deny-self-hosted-runners", strict["run"])
        self.assertIn("--format json", strict["run"])
        self.assertIn("--signer-workflow", strict["run"])
        self.assertIn("--source-digest $env:GITHUB_SHA", strict["run"])
        self.assertIn("--source-ref $env:GITHUB_REF", strict["run"])
        self.assertIn("packaging/windows/verify.py", strict["run"])
        self.assertIn("--distribution", strict["run"])
        self.assertIn("--manifest", strict["run"])
        for job in workflow["jobs"].values():
            for step in job["steps"]:
                self.assertFalse(step.get("continue-on-error", False))
                if "uses" in step:
                    self.assertRegex(step["uses"], r"^actions/[a-z-]+@[a-f0-9]{40}$")

    def test_distribution_review_requires_the_fail_closed_release_decision(self):
        review = json.loads((ROOT / "packaging/windows/distribution-review.json").read_bytes())
        self.assertIs(review.get("release_decision_required"), True)
        self.assertIs(review.get("candidate_manifest_required"), True)
        self.assertIs(review.get("candidate_guidance_required"), True)
        self.assertEqual(review.get("real_data_authorization"), "all-mandatory-gates-pass")

    def test_relink_proof_rejects_same_input_stale_sha_or_changed_application_objects(self):
        objects = {"application/main.obj": "c" * 64}
        proof = {"source_sha": "a" * 40, "original_exe_sha256": "b" * 64,
                 "modified_exe_sha256": "d" * 64, "application_sha256": objects,
                 "modified_qt_marker_in_application": True, "marker_probe": "MODIFIED_QT_CONFIRMED",
                 "synthetic_smoke": self.observation("d" * 64)}
        alpha.check_relink_proof(proof, "a" * 40, "b" * 64, objects)
        for changed in ({"source_sha": "e" * 40}, {"modified_exe_sha256": "b" * 64}, {"application_sha256": {}}, {"synthetic_smoke": {}}, {"synthetic_smoke": None}):
            with self.subTest(changed=changed), self.assertRaisesRegex(ValueError, "relink"):
                alpha.check_relink_proof(dict(proof, **changed), "a" * 40, "b" * 64, objects)
        for changed in ({"keyboard_focus_observed": False}, {"source_sha": "e" * 40}, {"exe_sha256": "b" * 64}):
            with self.subTest(changed=changed), self.assertRaisesRegex(ValueError, "relink"):
                alpha.check_relink_proof(dict(proof, synthetic_smoke=dict(proof["synthetic_smoke"], **changed)), "a" * 40, "b" * 64, objects)

    def test_license_bindings_require_every_notice_and_exact_bytes(self):
        files = {"LICENSE": b"public notice", "runtime-notices/one": b"primary terms"}
        bindings = {name: alpha.digest(data) for name, data in files.items()}
        alpha.verify_license_bindings(files, bindings)
        for changed in ({"LICENSE": "a" * 64}, dict(bindings, extra="b" * 64), {}):
            with self.assertRaisesRegex(ValueError, "license"):
                alpha.verify_license_bindings(files, changed)

    @staticmethod
    def sample_pe(library=b"KERNEL32.dll"):
        data = bytearray(1024)
        data[:2] = b"MZ"
        struct.pack_into("<I", data, 60, 128)
        data[128:132] = b"PE\0\0"
        struct.pack_into("<HH", data, 132, 0x8664, 1)
        struct.pack_into("<H", data, 148, 240)
        struct.pack_into("<H", data, 152, 0x20b)
        struct.pack_into("<I", data, 260, 16)
        struct.pack_into("<II", data, 272, 4096, 40)
        struct.pack_into("<IIII", data, 400, 512, 4096, 512, 512)
        struct.pack_into("<IIIII", data, 512, 0, 0, 0, 4160, 0)
        data[576:576 + len(library)] = library
        return bytes(data)

    def test_independent_pe_parser_reads_real_table_and_rejects_truncation_signature_and_sidecars(self):
        self.assertEqual(alpha.pe_imports(self.sample_pe()), ["KERNEL32.dll"])
        for invalid in (b"MZ", self.sample_pe(b"Qt6Core.dll"), self.sample_pe()[:530]):
            with self.assertRaisesRegex(ValueError, "PE"):
                alpha.pe_imports(invalid)
        signed = bytearray(self.sample_pe())
        struct.pack_into("<II", signed, 296, 900, 40)
        with self.assertRaisesRegex(ValueError, "PE"):
            alpha.pe_imports(bytes(signed))

    def test_vendor_prefix_review_is_byte_source_hash_and_exe_bound(self):
        vendor = b"/ho" + b"me/runner/work/llvm-mingw/vendor-source.cpp"
        library = b"public archive" + vendor + b"\0"
        executable = b"MZ\0" + vendor + b"\0"
        cleaned, report = alpha.vendor_scan_copy(executable, {"vendor.a": library}, {"vendor.a": alpha.digest(library)})
        self.assertNotIn(vendor, cleaned)
        self.assertEqual(report["exe_sha256"], alpha.digest(executable))
        self.assertEqual(report["spans"][0]["offset"], 3)
        with self.assertRaisesRegex(ValueError, "vendor"):
            alpha.vendor_scan_copy(executable, {"vendor.a": library + b"drift"}, {"vendor.a": alpha.digest(library)})
        with self.assertRaisesRegex(ValueError, "vendor"):
            alpha.vendor_scan_copy(executable.replace(b"source", b"private"), {"vendor.a": library}, {"vendor.a": alpha.digest(library)})
        self.assertIn(b"/ho" + b"me/private/", alpha.vendor_scan_copy(b"MZ/ho" + b"me/private/secret", {}, {})[0])

    def test_link_map_membership_preserves_ambiguity_and_rejects_missing_objects(self):
        mapping = alpha.link_inventory("00001000 00000100 16 file.cpp.obj:(.text)\n00001100 00000010 8 runtime.o:(.data)\n", {"qt.a": {"file.cpp.obj"}, "app.a": {"file.cpp.obj"}, "crt.a": {"runtime.o"}})
        self.assertEqual(mapping, {"file.cpp.obj": ["app.a", "qt.a"], "runtime.o": ["crt.a"]})
        with self.assertRaisesRegex(ValueError, "unmapped"):
            alpha.link_inventory("00001000 00000100 16 unknown.o:(.text)\n", {})

    def test_dictionary_scan_exclusion_does_not_change_manifest_or_executable_hash(self):
        dictionary = b"abandon\n" * 12
        executable = self.sample_pe() + dictionary
        files = {name: b"public" for name in ("THIRD_PARTY_ALPHA.md", "THIRD_PARTY_NOTICES", "LICENSE", "README.md", "README.ru.md", "THREAT_MODEL.md", "user-guide.md", "known-limitations.md", "release-evidence.md", "PE-imports.json", "runtime-observation.json")}
        files.update({"Tessaveil.exe": executable, "SOURCE_SHA": b"a" * 40 + b"\n",
                      "sbom.cdx.json": b'{"bomFormat":"CycloneDX","specVersion":"1.6"}',
                      "release-evidence.json": json.dumps({"source_sha": "a" * 40, "exe_sha256": alpha.digest(executable), "unsigned": True, "synthetic_only": True, "real_data_verdict": "NO-GO для реальных данных"}).encode()})
        files["vendor-build-prefixes.json"] = json.dumps(alpha.vendor_scan_copy(executable, {}, {})[1]).encode()
        files["PE-imports.json"] = json.dumps({"exe_sha256": alpha.digest(executable), "imports": ["KERNEL32.dll"]}).encode()
        files["runtime-observation.json"] = json.dumps(self.observation(alpha.digest(executable))).encode()
        files["SHA256SUMS"] = alpha.make_manifest(files)
        alpha.audit_runtime(files, "a" * 40, frozenset({"abandon"}), dictionary)
        self.assertEqual(files["Tessaveil.exe"], executable)
        substituted = dict(files, **{"runtime-observation.json": b"{}"})
        substituted.pop("SHA256SUMS")
        substituted["SHA256SUMS"] = alpha.make_manifest(substituted)
        with self.assertRaisesRegex(ValueError, "observation"):
            alpha.audit_runtime(substituted, "a" * 40, frozenset({"abandon"}), dictionary)
        files["Tessaveil.exe"] += b"changed"
        with self.assertRaisesRegex(ValueError, "manifest"):
            alpha.audit_runtime(files, "a" * 40, frozenset({"abandon"}), dictionary)

    def test_qt_attribution_normalizes_upstream_literal_newline_without_losing_terms(self):
        raw = b'{"Id":"example","Name":"Example","License":"MIT\nnotice","LicenseId":"MIT"}'
        records = alpha.qt_attributions(raw)
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["License"], "MIT\nnotice")
        self.assertEqual(json.loads(json.dumps(records))[0]["LicenseId"], "MIT")

    def test_runtime_audit_rejects_wrong_sha_missing_metadata_and_sidecars(self):
        files = {"SOURCE_SHA": b"a" * 40 + b"\n", "Tessaveil.exe": b"MZ"}
        for changed in (files, dict(files, **{"Qt6Core.dll": b"MZ"})):
            changed = dict(changed, SHA256SUMS=alpha.make_manifest(changed))
            with self.assertRaises(ValueError):
                alpha.audit_runtime(changed, "b" * 40, frozenset())
        with self.assertRaises(ValueError):
            alpha.audit_runtime(dict(files, SHA256SUMS=alpha.make_manifest(files)), "a" * 40, frozenset())

    def test_sbom_lock_drift_or_missing_license_is_rejected(self):
        package = {"name": "example", "version": "1.0.0", "source": "registry+https://github.com/rust-lang/crates.io-index", "checksum": "a" * 64}
        metadata = {"packages": [{"id": "example", "name": "example", "version": "2.0.0", "license": "MIT", "source": package["source"]}], "resolve": {"nodes": []}}
        with self.assertRaisesRegex(ValueError, "locked metadata"):
            alpha.rust_components([package], metadata)
        metadata["packages"][0]["version"] = "1.0.0"
        metadata["packages"][0]["license"] = None
        with self.assertRaisesRegex(ValueError, "license"):
            alpha.rust_components([package], metadata)

    def test_archive_rejects_traversal_duplicate_case_and_links(self):
        for names in (("../escape",), ("/absolute",), ("a", "A"), ("a", "a"), ("a:stream",)):
            with self.subTest(names=names), tempfile.TemporaryDirectory() as temporary:
                archive = Path(temporary) / "bad.zip"
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore", UserWarning)
                    with zipfile.ZipFile(archive, "w") as output:
                        for name in names:
                            output.writestr(name, b"public")
                with self.assertRaisesRegex(ValueError, "unsafe archive"):
                    alpha.read_archive(archive)

    def test_manifest_checks_every_byte_and_rejects_extra_files(self):
        payload = {"SOURCE_SHA": b"a" * 40 + b"\n", "notice.txt": b"public\n"}
        manifest = alpha.make_manifest(payload)
        self.assertEqual(manifest.splitlines()[1].split(b"  ")[1], b"notice.txt")
        alpha.verify_manifest(dict(payload, SHA256SUMS=manifest))
        for changed in (dict(payload, **{"notice.txt": b"changed"}), dict(payload, extra=b"public")):
            with self.assertRaisesRegex(ValueError, "manifest"):
                alpha.verify_manifest(dict(changed, SHA256SUMS=manifest))

    def test_scan_rejects_local_paths_credentials_vaults_and_phrase_runs(self):
        cases = [b"TSVALPHA" + bytes(150), b"synthetic-" + b"master-password",
                 ("C:" + "/Use" + "rs/ExamplePrivateProfile/source.cpp").encode(),
                 ("C:" + "\\Users\\ExamplePrivateProfile\\source.cpp").encode("utf-16le"),
                 ("abandon " * 12).encode(),
                 ("ghp_" + "a" * 30).encode()]
        for data in cases:
            with self.subTest(size=len(data)), self.assertRaisesRegex(ValueError, "sensitive"):
                alpha.scan_bytes("payload", data, frozenset({"abandon"}))
        alpha.scan_bytes("notice", b"Unsigned Windows engineering alpha. Synthetic data only.", frozenset())

    def test_upload_gate_never_promotes_missing_or_unverified_compliance(self):
        for evidence in ({}, {"relinked": True}, {"status": "PASS", "source_sha": "b" * 40}):
            with self.subTest(evidence=evidence), self.assertRaisesRegex(ValueError, "compliance"):
                alpha.require_distribution_clearance(evidence, "a" * 40)

    def test_deterministic_archive_roundtrip_and_checksum(self):
        with tempfile.TemporaryDirectory() as temporary:
            first, second = (Path(temporary) / name for name in ("one.zip", "two.zip"))
            files = {"notice.txt": b"public", "SOURCE_SHA": b"a" * 40}
            alpha.write_archive(first, files)
            alpha.write_archive(second, dict(reversed(list(files.items()))))
            self.assertTrue(first.is_file(), "archive was not produced")
            self.assertTrue(second.is_file(), "archive was not produced")
            self.assertEqual(first.read_bytes(), second.read_bytes())
            self.assertEqual(alpha.read_archive(first), files)


if __name__ == "__main__":
    unittest.main()
