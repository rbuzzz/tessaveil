"""Record exact link-map/archive membership for offline licensing review.

Basename collisions are retained, never guessed away. This is evidence, not a
license clearance. Output contains portable relative paths and no raw link map.
"""
import argparse
import json
from pathlib import Path
import re
import subprocess

import alpha


def inventory(root, build, rust_library):
    llvm = root / "llvm-mingw-20250709-ucrt-x86_64"
    ninja = (build / "build.ninja").read_text(encoding="utf-8")
    link_rule = re.search(r"^build Tessaveil\.exe:.*$", ninja, re.M)
    if not link_rule:
        raise ValueError("missing application link rule")
    rule = link_rule[0].replace("$:", ":")
    paths = [path for path in sorted((root / "qt-6.8.3-static").rglob("*.a")) if path.as_posix() in rule]
    paths += [build / "libalpha_ui.a", rust_library]
    paths += [llvm / "x86_64-w64-mingw32/lib" / name for name in
              ("libc++.a", "libc++abi.a", "libunwind.a", "libwinpthread.a", "libmingw32.a", "libmingwex.a", "libucrt.a", "libucrtbase.a", "libuuid.a", "libdxguid.a")]
    paths += [llvm / "lib/clang/20/lib/windows/libclang_rt.builtins-x86_64.a"]
    members, hashes = {}, {}
    for path in paths:
        if not path.is_file():
            continue
        name = path.relative_to(root).as_posix()
        listing = subprocess.run([str(llvm / "bin/llvm-ar.exe"), "t", str(path)], check=True, capture_output=True).stdout.decode()
        members[name] = set(listing.splitlines())
        hashes[name] = alpha.digest(path.read_bytes())
    standalone = [build / "CMakeFiles/Tessaveil.dir/main.cpp.obj"]
    standalone += list((llvm / "x86_64-w64-mingw32/lib").glob("crt*.o"))
    standalone += [path for path in (root / "qt-6.8.3-static").rglob("*_init.cpp.obj") if path.as_posix() in rule]
    for path in standalone:
        name = path.relative_to(root).as_posix()
        members[name] = {path.name}
        hashes[name] = alpha.digest(path.read_bytes())
    mapping = alpha.link_inventory((build / "Tessaveil.map").read_text(), members)
    used = {archive for archives in mapping.values() for archive in archives}
    return {"exe_sha256": alpha.digest((build / "Tessaveil.exe").read_bytes()),
            "map_sha256": alpha.digest((build / "Tessaveil.map").read_bytes()),
            "archives": {name: hashes[name] for name in sorted(used)}, "members": mapping,
            "status": "MEMBERSHIP_ONLY_LICENSE_REVIEW_REQUIRED"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("toolchain-root", "build", "rust-library", "output"):
        parser.add_argument("--" + name, type=Path, required=True)
    args = parser.parse_args()
    report = inventory(args.toolchain_root, args.build, args.rust_library)
    args.output.write_text(json.dumps(report, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(f"Mapped {len(report['members'])} unique object names to {len(report['archives'])} candidate inputs")
