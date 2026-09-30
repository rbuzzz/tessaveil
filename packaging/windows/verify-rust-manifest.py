"""Compare installed Rust archive identities with the hash-pinned release manifest."""
from pathlib import Path
import sys
import tomllib


def verify(expected, installed):
    host = "x86_64-pc-windows-gnu"
    for name in ("cargo", "rustc", "rust-std", "rust-mingw", "rustfmt-preview", "clippy-preview", "rust-src"):
        target = "*" if name == "rust-src" else host
        left = expected["pkg"][name]["target"][target]
        right = installed["pkg"][name]["target"][target]
        for key in ("url", "hash", "xz_url", "xz_hash"):
            if left.get(key) != right.get(key) or not left.get(key):
                raise ValueError("Rust component archive identity mismatch")


if __name__ == "__main__":
    verify(*(tomllib.loads(Path(p).read_text()) for p in sys.argv[1:]))
