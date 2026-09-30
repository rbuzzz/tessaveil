"""Bind outputs of a completed build/native-test step to its exact checkout."""
import argparse
import json
from pathlib import Path
import subprocess

import alpha


def receipt(root):
    files = {"Tessaveil.exe": root / "build/alpha-package/Tessaveil.exe",
             "application/main.obj": root / "build/alpha-package/CMakeFiles/Tessaveil.dir/main.cpp.obj",
             "application/alpha_ui.a": root / "build/alpha-package/libalpha_ui.a",
             "application/controller.a": root / "alpha-package-target/release/libtessaveil_windows_controller.a"}
    return {"source_sha": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=alpha.ROOT).decode().strip(),
            "working_tree_dirty": bool(subprocess.check_output(["git", "status", "--porcelain", "--untracked-files=all"], cwd=alpha.ROOT)),
            "files": {name: alpha.digest(path.read_bytes()) for name, path in files.items()},
            "native_tests": "PASS", "scope": "Written only after real release build and native synthetic E2E exit zero; not provenance"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--toolchain-root", type=Path, required=True)
    args = parser.parse_args()
    (args.toolchain_root / "build/alpha-package/build-receipt.json").write_text(json.dumps(receipt(args.toolchain_root), sort_keys=True, indent=2) + "\n", encoding="utf-8")
