"""Behavioral packaging boundaries: reject bad bytes before publication."""

import importlib.util
import json
from pathlib import Path
import tempfile
import struct
import unittest
import warnings
import zipfile

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location("alpha_package", ROOT / "packaging/windows/alpha.py")
alpha = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(alpha)


class WindowsAlphaPackageTests(unittest.TestCase):
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
        self.assertNotIn("if", build["steps"][upload])
        self.assertEqual(build["steps"][upload]["with"]["if-no-files-found"], "error")
        provenance = workflow["jobs"]["provenance"]
        self.assertEqual(provenance["needs"], ["windows-alpha"])
        self.assertEqual(provenance["permissions"], {"contents": "read", "id-token": "write", "attestations": "write"})
        attest = next(step for step in provenance["steps"] if step.get("uses", "").startswith("actions/attest@"))
        self.assertEqual(attest["with"].get("create-storage-record"), False)
        self.assertEqual(attest["with"]["subject-path"], "verified-artifact/*.zip")
        self.assertFalse(any(key.startswith("predicate") for key in attest["with"]))
        for job in workflow["jobs"].values():
            for step in job["steps"]:
                self.assertFalse(step.get("continue-on-error", False))
                if "uses" in step:
                    self.assertRegex(step["uses"], r"^actions/[a-z-]+@[a-f0-9]{40}$")

    def test_relink_proof_rejects_same_input_stale_sha_or_changed_application_objects(self):
        objects = {"application/main.obj": "c" * 64}
        proof = {"source_sha": "a" * 40, "original_exe_sha256": "b" * 64,
                 "modified_exe_sha256": "d" * 64, "application_sha256": objects,
                 "modified_qt_marker_in_application": True, "marker_probe": "MODIFIED_QT_CONFIRMED",
                 "synthetic_smoke": {"open_close_reopen_lock": True, "authentication_safe": True, "all_five_password_controls_masked": True}}
        alpha.check_relink_proof(proof, "a" * 40, "b" * 64, objects)
        for changed in ({"source_sha": "e" * 40}, {"modified_exe_sha256": "b" * 64}, {"application_sha256": {}}, {"synthetic_smoke": {}}):
            with self.subTest(changed=changed), self.assertRaisesRegex(ValueError, "relink"):
                alpha.check_relink_proof(dict(proof, **changed), "a" * 40, "b" * 64, objects)

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
        files = {name: b"public" for name in ("THIRD_PARTY_ALPHA.md", "THIRD_PARTY_NOTICES", "LICENSE", "user-guide.md", "known-limitations.md", "PE-imports.json", "runtime-observation.json")}
        files.update({"Tessaveil.exe": executable, "SOURCE_SHA": b"a" * 40 + b"\n",
                      "sbom.cdx.json": b'{"bomFormat":"CycloneDX","specVersion":"1.6"}',
                      "release-evidence.json": json.dumps({"source_sha": "a" * 40, "exe_sha256": alpha.digest(executable)}).encode()})
        files["vendor-build-prefixes.json"] = json.dumps(alpha.vendor_scan_copy(executable, {}, {})[1]).encode()
        files["PE-imports.json"] = json.dumps({"exe_sha256": alpha.digest(executable), "imports": ["KERNEL32.dll"]}).encode()
        files["SHA256SUMS"] = alpha.make_manifest(files)
        alpha.audit_runtime(files, "a" * 40, frozenset({"abandon"}), dictionary)
        self.assertEqual(files["Tessaveil.exe"], executable)
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
