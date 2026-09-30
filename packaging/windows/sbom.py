"""Reconstruct SBOM expectations from reviewed source metadata, never from a SBOM.

The checked-in inventory is normalized cargo metadata plus license/notice metadata
read from checksum-verified Rust runtime crate manifests. The producer must compare
fresh locked metadata to it. The offline verifier needs no developer cache/network.
Qt attribution is independently read from the complete pinned archive; Windows
imports come from the actual PE. Source inventories include non-linked dependencies.
"""
import argparse
import io
import json
from pathlib import Path
import re
import subprocess
import tomllib
import zipfile

import alpha

QT_HASH = "992bf7766e214a341ef793eb3665fb784787d2fd666955f5f507f4c6f1f770dd"
INVENTORY = alpha.ROOT / "packaging/windows/sbom-source-inventory.json"


def normalize_metadata(metadata):
    references = {p["id"]: f"pkg:cargo/{p['name']}@{p['version']}" for p in metadata["packages"]}
    packages = [{**{key: p.get(key) for key in ("name", "version", "source", "license")}, "id": references[p["id"]]} for p in metadata["packages"]]
    nodes = [{"id": references[n["id"]], "dependencies": sorted(references[d] for d in n["dependencies"])} for n in metadata["resolve"]["nodes"]]
    return {"packages": sorted(packages, key=lambda p: p["id"]), "resolve": {"nodes": sorted(nodes, key=lambda n: n["id"])}}


def check_metadata(metadata, expected):
    if normalize_metadata(metadata) != expected:
        raise ValueError("SBOM source inventory differs from live locked Cargo metadata")


def runtime_metadata(components):
    return [{"name": c["name"], "version": c["version"], "license": c["licenses"][0]["expression"],
             "notices": next(p["value"] for p in c["properties"] if p["name"] == "tessaveil:notices").split(",")}
            for c in components]


def check_runtime_metadata(components, expected):
    if runtime_metadata(components) != expected:
        raise ValueError("SBOM source inventory differs from hash-verified runtime crate manifests")


def source_inventory():
    source = json.loads(INVENTORY.read_bytes())
    if source["cargo_lock_sha256"] != alpha.digest((alpha.ROOT / "Cargo.lock").read_bytes()):
        raise ValueError("SBOM source inventory Cargo.lock drift")
    return source


def document(compliance, executable, source_sha):
    source = source_inventory()
    metadata = source["cargo_metadata"]
    packages = tomllib.loads((alpha.ROOT / "Cargo.lock").read_text(encoding="utf-8"))["package"]
    components = alpha.rust_components(packages, metadata)
    linked = json.loads(compliance["linked-inputs.json"])
    if linked.get("exe_sha256") != alpha.digest(executable):
        raise ValueError("SBOM linked inventory EXE mismatch")
    linked_rust = frozenset(match[1] for name in linked["members"] if (match := re.match(r"^([a-zA-Z0-9_]+)-[0-9a-f]{16}\.", name)))
    runtime_lock = compliance["runtime-notices/rust/library-Cargo.lock"]
    policy = json.loads((alpha.ROOT / "packaging/windows/runtime-sources.json").read_bytes())
    if alpha.digest(runtime_lock) != source["rust_library_lock_sha256"] or source["rust_library_lock_sha256"] != policy["rust_library_lock_sha256"]:
        raise ValueError("SBOM runtime lock drift")
    runtime_packages = tomllib.loads(runtime_lock.decode())["package"]
    runtime_inventory = {(p["name"], p["version"]): p for p in source["runtime_metadata"]}
    if set(runtime_inventory) != {(p["name"], p["version"]) for p in runtime_packages if p.get("source")}:
        raise ValueError("SBOM runtime inventory incomplete")
    for package in runtime_packages:
        if not package.get("source"):
            continue
        item = runtime_inventory[(package["name"], package["version"])]
        stem = package["name"] + "-" + package["version"]
        if any(name and "runtime-notices/" + name not in compliance for name in item["notices"]):
            raise ValueError("SBOM runtime notice missing")
        components.append({"type": "library", "bom-ref": "rust-runtime:" + stem,
                           "name": package["name"], "version": package["version"],
                           "licenses": [{"expression": item["license"]}],
                           "hashes": [{"alg": "SHA-256", "content": package["checksum"]}],
                           "externalReferences": [{"type": "distribution", "url": f"https://static.crates.io/crates/{package['name']}/{stem}.crate"}],
                           "description": "Pinned Rust standard-library source dependency graph; includes non-Windows/build-only entries",
                           "properties": [{"name": "tessaveil:notices", "value": ",".join(item["notices"])},
                                          {"name": "tessaveil:linked-object-observed", "value": str(package["name"].replace("-", "_") in linked_rust).lower()}]})
    builtin = next(p for p in runtime_packages if p["name"] == "compiler_builtins")
    components.append({"type": "library", "bom-ref": "rust-compiler-builtins", "name": "compiler_builtins", "version": builtin["version"],
                       "licenses": [{"expression": "MIT AND (Apache-2.0 WITH LLVM-exception)"}],
                       "externalReferences": [{"type": "vcs", "url": "https://github.com/rust-lang/rust/tree/" + policy["rust_source_commit"] + "/library/compiler-builtins"}],
                       "description": "Exact rust-src library lock and compound compiler-builtins license preserved in compliance material"})
    dictionary = json.loads((alpha.ROOT / "catalog/dictionaries/bip39-en.json").read_bytes())
    if alpha.digest((alpha.ROOT / dictionary["wordlist_path"]).read_bytes()) != dictionary["sha256"]:
        raise ValueError("SBOM dictionary hash drift")
    components.extend([
        {"type": "library", "bom-ref": "qtbase", "name": "QtBase", "version": "6.8.3", "licenses": [{"expression": "LGPL-3.0-only"}], "hashes": [{"alg": "SHA-256", "content": QT_HASH}], "description": "Core, Gui, Widgets, EntryPoint, Windows/style/image plugins; exact complete corresponding source bundled separately"},
        {"type": "data", "bom-ref": "bip39-en", "name": "bip39-en", "version": dictionary["source"]["revision"], "licenses": [{"license": {"id": "MIT"}}], "hashes": [{"alg": "SHA-256", "content": dictionary["sha256"]}], "externalReferences": [{"type": "distribution", "url": dictionary["source"]["url"]}]},
        {"type": "library", "bom-ref": "rust-std", "name": "Rust standard library", "version": "1.90.0", "licenses": [{"expression": "(MIT OR Apache-2.0) AND Unicode-3.0 AND BSD-2-Clause"}], "description": "See exact rust-src lock, compiler-builtins and per-dependency notices in compliance material"},
        {"type": "library", "bom-ref": "llvm-mingw-runtime", "name": "LLVM-MinGW static runtime", "version": "20250709", "licenses": [{"expression": "(Apache-2.0 WITH LLVM-exception) AND ZPL-2.1 AND LicenseRef-MinGW-Individual-Notices"}], "description": "Exact source/member mapping and complete notices accompany compliance material"},
    ])
    if alpha.digest(compliance["qtbase-6.8.3.zip"]) != QT_HASH:
        raise ValueError("SBOM Qt source hash mismatch")
    with zipfile.ZipFile(io.BytesIO(compliance["qtbase-6.8.3.zip"])) as archive:
        for info in archive.infolist():
            if not info.is_dir() and info.filename.endswith("qt_attribution.json"):
                relative = info.filename.split("/", 1)[1]
                for record in alpha.qt_attributions(archive.read(info)):
                    component = {"type": "library", "bom-ref": "qt-source:" + relative + ":" + record["Id"],
                                 "name": record["Name"], "description": "Qt source inventory; inclusion in linked executable requires review",
                                 "properties": [{"name": "tessaveil:source-path", "value": relative}]}
                    if record.get("LicenseId"):
                        component["licenses"] = [{"expression": record["LicenseId"]}]
                    if record.get("Version"):
                        component["version"] = str(record["Version"])
                    components.append(component)
    components.extend({"type": "operating-system", "bom-ref": "windows:" + name.lower(), "name": name, "description": "Host Windows/UCRT system import; supplied by the OS, not redistributed"} for name in alpha.pe_imports(executable))
    dependencies = [{"ref": n["id"], "dependsOn": n["dependencies"]} for n in metadata["resolve"]["nodes"]]
    qt_archives = {name: sha for name, sha in linked["archives"].items() if name.startswith("qt-6.8.3-static/") and name.endswith(".a")}
    review = json.loads((alpha.ROOT / "packaging/windows/distribution-review.json").read_bytes())
    if sorted(Path(name).name for name in qt_archives) != sorted(review["qt_runtime_archives"]):
        raise ValueError("SBOM Qt linked module review drift")
    # Every graph node is explicit, including leaves. Root is the complete source
    # inventory scope, not a claim that conditional/test-only sources are linked.
    refs = {c["bom-ref"] for c in components}
    if len(refs) != len(components):
        raise ValueError("SBOM duplicate source component")
    known_nodes = {n["ref"] for n in dependencies}
    if known_nodes != {p["id"] for p in metadata["packages"]} or any(not set(n["dependsOn"]).issubset(refs) for n in dependencies):
        raise ValueError("SBOM Cargo dependency graph incomplete")
    dependencies.extend({"ref": ref, "dependsOn": []} for ref in sorted(refs - known_nodes))
    dependencies.append({"ref": "Tessaveil", "dependsOn": sorted(refs)})
    return {"bomFormat": "CycloneDX", "specVersion": "1.6", "version": 1,
            "metadata": {"component": {"type": "application", "bom-ref": "Tessaveil", "name": "Tessaveil", "version": source_sha,
                                       "hashes": [{"alg": "SHA-256", "content": alpha.digest(executable)}], "licenses": [{"expression": "Apache-2.0"}],
                                       "properties": [{"name": "tessaveil:dependency-scope", "value": "complete source inventory; conditional/dev/build entries are not necessarily linked"},
                                                      {"name": "tessaveil:linked-qt-archives", "value": json.dumps(qt_archives, sort_keys=True)}]}},
            "components": components, "dependencies": sorted(dependencies, key=lambda n: n["ref"])}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Print normalized source inventory from real locked metadata; review and commit separately. Never consumes SBOM output.")
    parser.add_argument("--toolchain-root", type=Path, required=True)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    import runtime_material
    metadata = json.loads(subprocess.check_output(["cargo", "metadata", "--locked", "--offline", "--format-version", "1"], cwd=alpha.ROOT))
    notices, components = runtime_material.material(args.toolchain_root)
    generated = {"cargo_lock_sha256": alpha.digest((alpha.ROOT / "Cargo.lock").read_bytes()),
                 "rust_library_lock_sha256": alpha.digest(notices["rust/library-Cargo.lock"]),
                 "cargo_metadata": normalize_metadata(metadata), "runtime_metadata": runtime_metadata(components)}
    if args.check:
        if generated != source_inventory():
            raise SystemExit("SBOM source inventory drift")
        print("SBOM source inventory matches locked Cargo metadata and hash-verified runtime crate manifests")
    else:
        print(json.dumps(generated, sort_keys=True, indent=2))
