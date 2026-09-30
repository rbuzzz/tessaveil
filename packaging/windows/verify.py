"""Independently unpack and audit analysis archives; fail closed for distribution."""
import argparse
import json
from pathlib import Path
import sys
import io
import zipfile

from jsonschema import Draft7Validator
from referencing import Registry, Resource

import alpha
import sbom


def verify(runtime_path, compliance_path, source_sha, distribution=False):
    runtime = alpha.read_archive(runtime_path)
    compliance = alpha.read_archive(compliance_path)
    expected = json.loads((alpha.ROOT / "packaging/windows/compliance-inventory.json").read_bytes())
    if distribution:
        expected.append("relink-proof.json")
    alpha.verify_inventory(compliance, expected)
    alpha.verify_manifest(runtime)
    alpha.verify_manifest(compliance)
    if compliance.get("SOURCE_SHA") != (source_sha + "\n").encode():
        raise ValueError("compliance source SHA mismatch")
    required = {"qtbase-6.8.3.zip", "application/main.obj", "application/alpha_ui.a",
                "application/controller.a", "relink.ps1", "relink/CMakeLists.txt",
                "qt-options.json", "qt-generated/features.json", "RELINKING.md",
                "qt-licenses/GPL-3.0-only.txt", "qt-licenses/LGPL-3.0-only.txt",
                "license-bindings.json", "license-review.md", "build-receipt.json",
                "runtime-notices/rust/compiler-builtins-LICENSE.txt",
                "runtime-notices/rust/library-Cargo.lock", "runtime-notices/mingw-linked-sources.json",
                "runtime-notices/llvm/libcxx-LICENSE.TXT", "runtime-notices/llvm/libcxxabi-LICENSE.TXT",
                "runtime-notices/llvm/libunwind-LICENSE.TXT", "runtime-notices/mingw/COPYING"}
    if not required.issubset(compliance):
        raise ValueError("compliance bundle incomplete")
    if alpha.digest(compliance["qtbase-6.8.3.zip"]) != "992bf7766e214a341ef793eb3665fb784787d2fd666955f5f507f4c6f1f770dd":
        raise ValueError("compliance Qt source hash mismatch")
    for relative in ("relink.ps1", "relink/CMakeLists.txt", "relink/marker.cpp", "qt-options.json", "distribution-review.json", "runtime-sources.json", "toolchains.json", "RELINKING.md", "license-review.md"):
        if compliance.get(relative) != (alpha.ROOT / "packaging/windows" / relative).read_bytes():
            raise ValueError("compliance source/configuration policy drift")
    alpha.verify_license_bindings(compliance, json.loads(compliance["license-bindings.json"]))
    schemas = {}
    for pin in json.loads(compliance["toolchains.json"])["downloads"]:
        if pin["file"].endswith(".schema.json"):
            data = compliance["schemas/" + pin["file"]]
            if alpha.digest(data) != pin["sha256"]:
                raise ValueError("SBOM schema drift")
            schemas[pin["file"]] = json.loads(data)
    registry = Registry().with_resources((schema["$id"], Resource.from_contents(schema)) for schema in schemas.values())
    if next(Draft7Validator(schemas["cyclonedx-1.6.schema.json"], registry=registry).iter_errors(json.loads(runtime["sbom.cdx.json"])), None):
        raise ValueError("SBOM fails pinned official CycloneDX 1.6 schema")
    alpha.check_sbom(json.loads(runtime["sbom.cdx.json"]), sbom.document(compliance, runtime["Tessaveil.exe"], source_sha))
    with zipfile.ZipFile(io.BytesIO(compliance["qtbase-6.8.3.zip"])) as qt_source:
        for name, data in compliance.items():
            if name.startswith("qt-licenses/"):
                source_name = "LICENSES/" + name.split("/", 1)[1]
            elif name.startswith(("qt-third-party/", "qt-attributions/")):
                source_name = name.split("/", 1)[1]
            else:
                continue
            if data != qt_source.read("qtbase-everywhere-src-6.8.3/" + source_name):
                raise ValueError("Qt notice differs from complete source")
    application_hashes = {name: alpha.digest(compliance[name]) for name in required if name.startswith("application/")}
    receipt = json.loads(compliance["build-receipt.json"])
    if receipt.get("source_sha") != source_sha or receipt.get("files") != {"Tessaveil.exe": alpha.digest(runtime["Tessaveil.exe"]), **application_hashes} or receipt.get("native_tests") != "PASS":
        raise ValueError("tested build/object receipt mismatch")
    source_policy = json.loads(compliance["runtime-sources.json"])
    if alpha.digest(compliance["runtime-notices/rust/library-Cargo.lock"]) != source_policy["rust_library_lock_sha256"]:
        raise ValueError("Rust runtime source lock mismatch")
    linked = json.loads(compliance["linked-inputs.json"])
    if linked.get("exe_sha256") != alpha.digest(runtime["Tessaveil.exe"]):
        raise ValueError("linked runtime inventory is stale")
    source_bindings = json.loads(compliance["runtime-notices/mingw-linked-sources.json"])
    for name, binding in source_bindings.items():
        if name not in linked["members"] or binding["source_sha256"] != alpha.digest(compliance["runtime-notices/" + binding["source"]]):
            raise ValueError("MinGW linked source binding mismatch")
    expected_members = {name for name in linked["members"] if name.startswith("lib64_") or name in ("crt2.o", "crtbegin.o", "crtend.o")}
    if set(source_bindings) != expected_members:
        raise ValueError("MinGW source coverage incomplete")
    for name in compliance:
        if name.endswith((".exe", ".dll", ".tessaveil-alpha", ".tmp", ".pdb")) or "/tests/" in name:
            raise ValueError("unexpected compliance file")
    record = json.loads((alpha.ROOT / "catalog/dictionaries/bip39-en.json").read_bytes())
    wordlist = (alpha.ROOT / record["wordlist_path"]).read_bytes()
    if alpha.digest(wordlist) != record["sha256"]:
        raise ValueError("dictionary changed")
    words = frozenset(wordlist.decode().splitlines())
    # Structural and hash verification always happens, including analysis mode.
    # Sensitive audit remains strict: failures are never a successful candidate.
    vendor_policy = json.loads((alpha.ROOT / "packaging/windows/vendor-members.json").read_bytes())
    if json.loads(compliance["vendor-members.json"]) != vendor_policy:
        raise ValueError("vendor source policy drift")
    vendor_sources = {name: compliance["vendor-inputs/" + name] for name in vendor_policy["members"]}
    alpha.audit_runtime(runtime, source_sha, words, wordlist, vendor_sources, vendor_policy["members"])
    for name, data in compliance.items():
        if name != "qtbase-6.8.3.zip":
            if name.startswith("vendor-inputs/"):
                data, _ = alpha.vendor_scan_copy(data, vendor_sources, vendor_policy["members"])
            alpha.scan_bytes(name, data.replace(wordlist, b"<verified-public-dictionary>"), words)
    if distribution:
        evidence = json.loads(runtime["release-evidence.json"])
        if evidence.get("working_tree_dirty") or receipt.get("working_tree_dirty") or evidence.get("audit_findings"):
            raise ValueError("candidate is analysis-only")
        alpha.require_distribution_clearance(evidence.get("compliance", {}), source_sha)
        alpha.check_relink_proof(json.loads(compliance["relink-proof.json"]), source_sha, alpha.digest(runtime["Tessaveil.exe"]), application_hashes)
        if evidence.get("relink_proof_sha256") != alpha.digest(compliance["relink-proof.json"]):
            raise ValueError("runtime and compliance relink evidence differ")
    return {"source_sha": source_sha, "runtime_sha256": alpha.digest(runtime_path.read_bytes()),
            "compliance_sha256": alpha.digest(compliance_path.read_bytes())}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runtime", type=Path, required=True)
    parser.add_argument("--compliance", type=Path, required=True)
    parser.add_argument("--source-sha", required=True)
    parser.add_argument("--distribution", action="store_true")
    args = parser.parse_args()
    try:
        print(json.dumps(verify(args.runtime, args.compliance, args.source_sha, args.distribution)))
    except (ValueError, KeyError) as error:
        print("BLOCKED: " + str(error), file=sys.stderr)
        raise SystemExit(1)
