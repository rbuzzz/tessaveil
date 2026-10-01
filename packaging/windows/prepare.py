"""Create LOCAL ANALYSIS material only. Distribution requires gate.ps1 success."""
import argparse
import json
from pathlib import Path
import re
import posixpath
import subprocess
import tomllib
import zipfile

import alpha
import candidate_manifest
import inventory
import runtime_material
import sbom

ROOT = alpha.ROOT
QT_HASH = "992bf7766e214a341ef793eb3665fb784787d2fd666955f5f507f4c6f1f770dd"


def encode(value):
    return (json.dumps(value, ensure_ascii=True, sort_keys=True, indent=2) + "\n").encode()


def run(*command):
    return subprocess.run(command, cwd=ROOT, capture_output=True, check=True).stdout


def prepare(args):
    sha = run("git", "rev-parse", "HEAD").decode().strip()
    if not re.fullmatch(r"[0-9a-f]{40}", args.source_sha) or sha != args.source_sha:
        raise ValueError("source SHA does not match checkout")
    dirty = bool(run("git", "status", "--porcelain", "--untracked-files=all"))
    if dirty and not args.analysis_only:
        raise ValueError("dirty checkout cannot produce an exact-SHA candidate")
    if args.output.exists():
        raise ValueError("output must be a new directory")
    receipt = json.loads((args.build / "build-receipt.json").read_bytes())
    if receipt.get("source_sha") != sha or receipt.get("native_tests") != "PASS" or (receipt.get("working_tree_dirty") and not args.analysis_only):
        raise ValueError("build receipt does not identify this candidate")
    qt_archive = (args.toolchain_root / "downloads/qtbase-6.8.3.zip").read_bytes()
    if alpha.digest(qt_archive) != QT_HASH:
        raise ValueError("Qt source archive mismatch")
    matrix = json.loads((ROOT / "generated/alpha/profile-matrix.json").read_bytes())
    dictionary = json.loads((ROOT / "catalog/dictionaries/bip39-en.json").read_bytes())
    if dictionary["license"]["repository_redistribution"] != "allowed" or dictionary["license"]["signpath_compatible"] != "compatible":
        raise ValueError("dictionary licensing gate blocked")
    wordlist = (ROOT / dictionary["wordlist_path"]).read_bytes()
    if alpha.digest(wordlist) != dictionary["sha256"]:
        raise ValueError("dictionary hash mismatch")
    # Keep the exact licensed public list distinct from an unreviewed phrase.
    words = frozenset(wordlist.decode().splitlines())
    metadata = json.loads(run("cargo", "metadata", "--locked", "--offline", "--format-version", "1"))
    source_inventory = sbom.source_inventory()
    sbom.check_metadata(metadata, source_inventory["cargo_metadata"])
    packages = tomllib.loads((ROOT / "Cargo.lock").read_text(encoding="utf-8"))["package"]
    components = alpha.rust_components(packages, metadata)
    linked = inventory.inventory(args.toolchain_root, args.build, args.rust_library)
    linked_rust = frozenset(match[1] for name in linked["members"] if (match := re.match(r"^([a-zA-Z0-9_]+)-[0-9a-f]{16}\.", name)))
    runtime_notices, runtime_components = runtime_material.material(args.toolchain_root, linked_rust=linked_rust, linked_members=linked["members"])
    sbom.check_runtime_metadata(runtime_components, source_inventory["runtime_metadata"])
    components.extend(runtime_components)
    runtime_policy = json.loads((ROOT / "packaging/windows/runtime-sources.json").read_bytes())
    builtin = next(package for package in tomllib.loads(runtime_notices["rust/library-Cargo.lock"].decode())["package"] if package["name"] == "compiler_builtins")
    components.append({"type": "library", "bom-ref": "rust-compiler-builtins", "name": "compiler_builtins", "version": builtin["version"],
                       "licenses": [{"expression": "MIT AND (Apache-2.0 WITH LLVM-exception)"}],
                       "externalReferences": [{"type": "vcs", "url": "https://github.com/rust-lang/rust/tree/" + runtime_policy["rust_source_commit"] + "/library/compiler-builtins"}],
                       "description": "Exact rust-src library lock and compound compiler-builtins license preserved in compliance material"})
    components.extend([
        {"type": "library", "bom-ref": "qtbase", "name": "QtBase", "version": "6.8.3", "licenses": [{"expression": "LGPL-3.0-only"}], "hashes": [{"alg": "SHA-256", "content": QT_HASH}], "description": "Core, Gui, Widgets, EntryPoint, Windows/style/image plugins; exact complete corresponding source bundled separately"},
        {"type": "data", "bom-ref": "bip39-en", "name": "bip39-en", "version": dictionary["source"]["revision"], "licenses": [{"license": {"id": "MIT"}}], "hashes": [{"alg": "SHA-256", "content": dictionary["sha256"]}], "externalReferences": [{"type": "distribution", "url": dictionary["source"]["url"]}]},
        {"type": "library", "bom-ref": "rust-std", "name": "Rust standard library", "version": "1.90.0", "licenses": [{"expression": "(MIT OR Apache-2.0) AND Unicode-3.0 AND BSD-2-Clause"}], "description": "See exact rust-src lock, compiler-builtins and per-dependency notices in compliance material"},
        {"type": "library", "bom-ref": "llvm-mingw-runtime", "name": "LLVM-MinGW static runtime", "version": "20250709", "licenses": [{"expression": "(Apache-2.0 WITH LLVM-exception) AND ZPL-2.1 AND LicenseRef-MinGW-Individual-Notices"}], "description": "Exact source/member mapping and complete notices accompany compliance material"},
    ])
    compliance = {"SOURCE_SHA": (sha + "\n").encode(), "qtbase-6.8.3.zip": qt_archive,
                  "application/main.obj": (args.build / "CMakeFiles/Tessaveil.dir/main.cpp.obj").read_bytes(),
                  "application/alpha_ui.a": (args.build / "libalpha_ui.a").read_bytes(),
                  "application/controller.a": args.rust_library.read_bytes(),
                  "LICENSE": (ROOT / "LICENSE").read_bytes()}
    if receipt.get("files") != {"Tessaveil.exe": alpha.digest((args.build / "Tessaveil.exe").read_bytes()), **{name: alpha.digest(data) for name, data in compliance.items() if name.startswith("application/")}}:
        raise ValueError("built application material changed after tests")
    compliance["build-receipt.json"] = encode(receipt)
    for relative in ("candidate_manifest.py", "release_decision.py", "relink.ps1", "qt-options.json", "toolchains.json", "runtime-sources.json", "vendor-members.json", "distribution-review.json", "license-review.md", "relink/CMakeLists.txt", "relink/marker.cpp", "RELINKING.md"):
        compliance[relative] = (ROOT / "packaging/windows" / relative).read_bytes()
    compliance["release-decision-template.json"] = (
        ROOT / "reports/windows-v1/release-decision.json"
    ).read_bytes()
    compliance.update(candidate_manifest.guidance_material(ROOT))
    for pin in json.loads(compliance["toolchains.json"])["downloads"]:
        if pin["file"].endswith(".schema.json"):
            data = (args.toolchain_root / "downloads" / pin["file"]).read_bytes()
            if alpha.digest(data) != pin["sha256"]:
                raise ValueError("SBOM schema hash mismatch")
            compliance["schemas/" + pin["file"]] = data
    compliance["linked-inputs.json"] = encode(linked)
    compliance.update({"runtime-notices/" + name: data for name, data in runtime_notices.items()})
    vendor_policy = json.loads((ROOT / "packaging/windows/vendor-members.json").read_bytes())
    supplier_archive = args.toolchain_root / "downloads/llvm-mingw-20250709.zip"
    if alpha.digest(supplier_archive.read_bytes()) != vendor_policy["archive_sha256"]:
        raise ValueError("vendor archive identity mismatch")
    with zipfile.ZipFile(supplier_archive) as supplier:
        vendor_sources = {name: supplier.read(name) for name in vendor_policy["members"]}
    compliance.update({"vendor-inputs/" + name: data for name, data in vendor_sources.items()})
    with zipfile.ZipFile(args.toolchain_root / "downloads/qtbase-6.8.3.zip") as archive:
        for info in archive.infolist():
            if info.is_dir():
                continue
            relative = info.filename.split("/", 1)[1]
            if relative.startswith("LICENSES/"):
                compliance["qt-licenses/" + relative[9:]] = archive.read(info)
            if relative.endswith("qt_attribution.json"):
                raw = archive.read(info)
                compliance["qt-attributions/" + relative] = raw
                records = alpha.qt_attributions(raw)
                for record in records:
                    if record.get("LicenseFile"):
                        license_path = posixpath.normpath(posixpath.join(posixpath.dirname(info.filename), record["LicenseFile"]))
                        if not license_path.startswith("qtbase-everywhere-src-6.8.3/"):
                            raise ValueError("Qt attribution license outside source")
                        compliance["qt-third-party/" + license_path.split("/", 1)[1]] = archive.read(license_path)
                    component = {"type": "library", "bom-ref": "qt-source:" + relative + ":" + record["Id"],
                                 "name": record["Name"], "description": "Qt source inventory; inclusion in linked executable requires review",
                                 "properties": [{"name": "tessaveil:source-path", "value": relative}]}
                    if record.get("LicenseId"):
                        component["licenses"] = [{"expression": record["LicenseId"]}]
                    if record.get("Version"):
                        component["version"] = str(record["Version"])
                    components.append(component)
        # Inline/compound notices not represented by a single LicenseFile.
        for relative in ("src/3rdparty/libjpeg/LICENSE", "src/3rdparty/libjpeg/LICENSE.md", "src/3rdparty/libjpeg/README.ijg", "src/3rdparty/libjpeg/COPYRIGHT.txt", "src/3rdparty/libjpeg/ijg-license.txt", "src/3rdparty/wintab/wintab.h"):
            name = "qtbase-everywhere-src-6.8.3/" + relative
            if name in archive.namelist():
                compliance["qt-third-party/" + relative] = archive.read(name)
    for package in metadata["packages"]:
        if not package.get("source"):
            continue
        directory = Path(package["manifest_path"]).parent
        for path in sorted(directory.iterdir()):
            if path.is_file() and path.name.upper().startswith(("LICENSE", "LICENCE", "COPYING", "NOTICE", "COPYRIGHT")):
                compliance[f"rust-licenses/{package['name']}-{package['version']}/{path.name}"] = path.read_bytes()
    # Preserve generated feature/configuration inputs, with portable placeholders.
    for path in sorted((args.toolchain_root / "qt-6.8.3-static/include").rglob("*config*.h")):
        compliance["qt-generated/" + path.relative_to(args.toolchain_root / "qt-6.8.3-static/include").as_posix()] = path.read_bytes()
    # CMake's cache can contain mixed host encodings and unrelated search paths.
    # Export only its ASCII feature decisions; never ship a build cache.
    cache = (args.toolchain_root / "build/qt-static/CMakeCache.txt").read_bytes().decode("latin1")
    features = dict(re.findall(r"^((?:FEATURE_|QT_FEATURE_|INPUT_|BUILD_SHARED_LIBS|QT_BUILD_)[A-Za-z0-9_]*):[^=\n]+=([^\r\n]*)", cache, re.M))
    compliance["qt-generated/features.json"] = encode(features)
    expected_qt = json.loads(compliance["distribution-review.json"])["qt_runtime_archives"]
    actual_qt = sorted(Path(name).name for name in linked["archives"] if name.startswith("qt-6.8.3-static/") and name.endswith(".a"))
    if actual_qt != sorted(expected_qt):
        raise ValueError("Qt linked module review drift")
    with zipfile.ZipFile(supplier_archive) as supplier:
        for name, expected in linked["archives"].items():
            if name.startswith("llvm-mingw-") and alpha.digest(supplier.read(name)) != expected:
                raise ValueError("linked runtime differs from pinned supplier archive")
    compliance["license-bindings.json"] = encode({name: alpha.digest(data) for name, data in compliance.items() if name.startswith(("qt-licenses/", "qt-third-party/", "qt-attributions/", "rust-licenses/", "runtime-notices/")) or name in ("LICENSE", "license-review.md")})
    exe = (args.build / "Tessaveil.exe").read_bytes()
    scanned_exe, vendor_report = alpha.vendor_scan_copy(exe, vendor_sources, vendor_policy["members"])
    imports_output = run(str(args.toolchain_root / "llvm-mingw-20250709-ucrt-x86_64/bin/llvm-readobj.exe"), "--coff-imports", str(args.build / "Tessaveil.exe")).decode()
    imports = sorted(set(re.findall(r"Name: ([^\r\n]+\.dll)", imports_output, re.I)), key=str.lower)
    if imports != alpha.pe_imports(exe):
        raise ValueError("independent PE parser disagrees with LLVM")
    if not imports or any(re.search(r"(?:qt[0-9]|libstdc|libgcc|libwinpthread|vcruntime|msvcp[0-9])", name, re.I) for name in imports):
        raise ValueError("PE runtime dependency gate failed")
    components.extend({"type": "operating-system", "bom-ref": "windows:" + name.lower(), "name": name, "description": "Host Windows/UCRT system import; supplied by the OS, not redistributed"} for name in imports)
    document = sbom.document(compliance, exe, sha)
    alpha.check_sbom({"components": components}, {"components": document["components"]})
    alpha.check_observation(json.loads(args.observation.read_bytes()), sha, alpha.digest(exe))
    evidence = {"source_sha": sha, "working_tree_dirty": dirty, "exe_sha256": alpha.digest(exe), "exe_bytes": len(exe),
                "status": "LOCAL_ANALYSIS_ONLY", "unsigned": True, "authenticode": False,
                "synthetic_only": True, "release_freeze": "NO-GO", "github_provenance": "NOT RUN",
                "real_data_verdict": candidate_manifest.NO_GO_VERDICT,
                "compliance": json.loads((ROOT / "packaging/windows/distribution-review.json").read_bytes()),
                "alpha_matrix_sha256": alpha.digest((ROOT / "generated/alpha/profile-matrix.json").read_bytes()), "cargo_lock_sha256": alpha.digest((ROOT / "Cargo.lock").read_bytes())}
    runtime = {"Tessaveil.exe": exe, "SOURCE_SHA": (sha + "\n").encode(),
               "sbom.cdx.json": encode(document),
               "release-evidence.json": encode(evidence), "PE-imports.json": encode({"exe_sha256": alpha.digest(exe), "imports": imports}),
               "runtime-observation.json": args.observation.read_bytes(),
               "vendor-build-prefixes.json": encode(vendor_report)}
    for source, destination in (("LICENSE", "LICENSE"), ("THIRD_PARTY_NOTICES", "THIRD_PARTY_NOTICES"), ("THIRD_PARTY_ALPHA.md", "THIRD_PARTY_ALPHA.md"), ("README.md", "README.md"), ("README.ru.md", "README.ru.md"), ("THREAT_MODEL.md", "THREAT_MODEL.md"), ("docs/alpha/user-guide.md", "user-guide.md"), ("docs/alpha/known-limitations.md", "known-limitations.md"), ("docs/alpha/release-evidence.md", "release-evidence.md")):
        runtime[destination] = (ROOT / source).read_bytes()
    # Do not bypass the scanner for opaque application objects. Only the exact,
    # separately hashed dictionary may be removed for phrase-run detection.
    findings = []
    for label, collection in (("runtime", runtime), ("compliance", compliance)):
        for name, data in collection.items():
            if name == "qtbase-6.8.3.zip":
                continue  # Complete, hash-verified upstream archive; never filtered.
            try:
                if label == "runtime" and name == "Tessaveil.exe":
                    data = scanned_exe
                elif name.startswith("vendor-inputs/"):
                    data, _ = alpha.vendor_scan_copy(data, vendor_sources, vendor_policy["members"])
                alpha.scan_bytes(name, data.replace(wordlist, b"<verified-public-dictionary>"), words)
            except ValueError:
                findings.append({"scope": label, "file": name, "category": "sensitive-content-review-required"})
    if findings and not args.analysis_only:
        raise ValueError("artifact audit failed; no distribution archive produced")
    evidence["audit_findings"] = findings
    runtime["release-evidence.json"] = encode(evidence)
    for collection in (runtime, compliance):
        collection["SHA256SUMS"] = alpha.make_manifest(collection)
    args.output.mkdir(parents=True)
    for label, collection in (("runtime", runtime), ("compliance", compliance)):
        for name, data in collection.items():
            path = args.output / label / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
        alpha.write_archive(args.output / (label + "-analysis.zip"), collection)
    print(json.dumps({"source_sha": sha, "status": "LOCAL_ANALYSIS_ONLY", "exe_sha256": alpha.digest(exe), "exe_bytes": len(exe)}))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("toolchain-root", "build", "rust-library", "output", "observation"):
        parser.add_argument("--" + name, required=True, type=Path)
    parser.add_argument("--source-sha", required=True)
    parser.add_argument("--analysis-only", action="store_true")
    prepare(parser.parse_args())
