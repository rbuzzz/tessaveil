"""Collect primary runtime notices from hash-pinned source material, offline by default."""
import argparse
import io
import json
from pathlib import Path
import re
import tarfile
import tomllib
import urllib.request
import zipfile

import alpha


def material(root, fetch=False, linked_rust=frozenset(), linked_members=()):
    policy = json.loads((Path(__file__).parent / "runtime-sources.json").read_bytes())
    downloads = root / "downloads"
    def pinned(name, url, expected):
        path = downloads / name
        if not path.exists() and fetch:
            with urllib.request.urlopen(url, timeout=120) as response:
                data = response.read()
            if alpha.digest(data) != expected:
                raise ValueError("runtime source download hash mismatch")
            path.write_bytes(data)
        data = path.read_bytes()
        if alpha.digest(data) != expected:
            raise ValueError("runtime source hash mismatch: " + name)
        return data

    files, components = {}, []
    for pin in policy["downloads"]:
        data = pinned(pin["file"], pin["url"], pin["sha256"])
        if pin["file"].endswith(".zip"):
            # Full source is retained locally for file-level review. Distribute
            # notices, not another library's test tree or build cache.
            with zipfile.ZipFile(io.BytesIO(data)) as source:
                source_index = {item.filename.split("/", 1)[-1]: item for item in source.infolist() if not item.is_dir()}
                for item in source.infolist():
                    relative = item.filename.split("/", 1)[-1]
                    if not item.is_dir() and (relative.startswith("COPYING") or relative in ("DISCLAIMER", "DISCLAIMER.PD")):
                        files["mingw/" + relative] = source.read(item)
                bindings = {}
                for member in linked_members:
                    match = re.match(r"lib64_.+_a-(.+)\.o$", member)
                    stem = match[1] if match else {"crt2.o": "crtexe", "crtbegin.o": "crtbegin", "crtend.o": "crtend"}.get(member)
                    if stem is None:
                        continue
                    choices = [name for name in source_index if name.startswith("mingw-w64-crt/") and Path(name).stem == stem and Path(name).suffix in (".c", ".S") and "/softmath/" not in name and "/arm" not in name]
                    if len(choices) != 1:
                        raise ValueError("ambiguous or missing MinGW source: " + member)
                    name = choices[0]
                    body = source.read(source_index[name])
                    if re.search(rb"Cephes|Moshier", body, re.I):
                        raise ValueError("linked MinGW source requires additional Cephes review: " + member)
                    destination = "mingw-linked-source/" + name
                    files[destination] = body
                    bindings[member] = {"source": destination, "source_sha256": alpha.digest(body), "archive_sha256": pin["sha256"]}
                files["mingw-linked-sources.json"] = json.dumps(bindings, sort_keys=True, indent=2).encode()
        else:
            files["llvm/" + pin["file"]] = data
    rust = root / "rustup/toolchains/1.90.0-x86_64-pc-windows-gnu"
    library = rust / "lib/rustlib/src/rust/library"
    lock = (library / "Cargo.lock").read_bytes()
    if alpha.digest(lock) != policy["rust_library_lock_sha256"]:
        raise ValueError("Rust standard library source lock drift")
    files["rust/library-Cargo.lock"] = lock
    files["rust/COPYRIGHT-library.html"] = (rust / "share/doc/rust/COPYRIGHT-library.html").read_bytes()
    files["rust/compiler-builtins-LICENSE.txt"] = (library / "compiler-builtins/LICENSE.txt").read_bytes()
    for package in tomllib.loads(lock.decode())["package"]:
        if not package.get("source"):
            continue
        if package["source"] != "registry+https://github.com/rust-lang/crates.io-index":
            raise ValueError("unreviewed Rust runtime source")
        stem = package["name"] + "-" + package["version"]
        url = f"https://static.crates.io/crates/{package['name']}/{stem}.crate"
        data = pinned(stem + ".crate", url, package["checksum"])
        with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as archive:
            manifest = tomllib.loads(archive.extractfile(stem + "/Cargo.toml").read().decode())
            license_id = manifest["package"].get("license")
            if not license_id:
                raise ValueError("Rust runtime license metadata missing")
            notices = []
            for item in archive.getmembers():
                path = Path(item.name)
                if item.isfile() and len(path.parts) == 2 and path.name.upper().startswith(("LICENSE", "LICENCE", "COPYING", "COPYRIGHT", "NOTICE")):
                    name = "rust/" + item.name
                    files[name] = archive.extractfile(item).read()
                    notices.append(name)
            if not notices and package["name"].replace("-", "_") in linked_rust:
                raise ValueError("Rust runtime license text missing: " + stem)
        components.append({"type": "library", "bom-ref": "rust-runtime:" + stem,
                           "name": package["name"], "version": package["version"],
                           "licenses": [{"expression": license_id.replace("MIT/Apache-2.0", "MIT OR Apache-2.0")}],
                           "hashes": [{"alg": "SHA-256", "content": package["checksum"]}],
                           "externalReferences": [{"type": "distribution", "url": url}],
                           "description": "Pinned Rust standard-library source dependency graph; includes non-Windows/build-only entries",
                           "properties": [{"name": "tessaveil:notices", "value": ",".join(notices)},
                                          {"name": "tessaveil:linked-object-observed", "value": str(package["name"].replace("-", "_") in linked_rust).lower()}]})
    return files, components


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--toolchain-root", type=Path, required=True)
    parser.add_argument("--fetch", action="store_true")
    args = parser.parse_args()
    files, components = material(args.toolchain_root, args.fetch)
    print(f"Verified {len(files)} primary runtime notice files; {len(components)} locked standard-library dependencies")
