"""Offline bounded repository scan. Findings never echo matched material.

Heuristics complement review; they do not prove that arbitrary secrets are absent.
Only exact reviewed public vectors and catalogue-validated word lists bypass
mnemonic/vector heuristics; credential and personal-path checks still apply.
"""

import hashlib
import json
from pathlib import Path
import re
import subprocess
import unicodedata

from tools.catalog.loader import load_catalog
from tools.catalog.validator import validate_catalog

PUBLIC_VECTORS = {
    "tests/catalog/fixtures/public/bip39-ton.json": "f49c34e3db29481cf7f4d94bebbaf3454a174d0baabf0e3e6a0f560203c45a22",
    "tests/catalog/fixtures/public/electrum-substrate-decred.json": "4f036ea306f7f78bb0a8a297524c70c9b614ccbedbe254bc98ce5fc0fd78a3bc",
    "tests/catalog/fixtures/public/monero-polyseed.json": "d3c7ea5d716b07c0ad5ca0bd5da7a0f1f0ebe8a2255f977fde6945e0193a8c2b",
    "tests/catalog/fixtures/public/slip39-algorand-cardano.json": "1944fa56fbe97267e6d7fb268a78df3d4fd6ad274b29b855c5f4b1a121d394ea",
    "tests/catalog/fixtures/public/zano-sia-zcash-chia.json": "4485e6ba9bb273679cf7863a1c9c8c4db14e649de44d362ee7088b4d9160f733",
}
SYNTHETIC_BINARIES = {
    "spikes/mobile/vectors/synthetic-vault-v0.bin": "2a18dd58f2711fa3ca3cbbc2433df3dea48cc9596765ee9fbfe676ad3ee2d50c",
    "spikes/filesystems/fixtures/header-and-ciphertext.bin": "bc5ea167e4fd6ce42b623f3a2d268fbba7b6bd60201344a0b32dfe6a922a0c01",
}
PATTERNS = {
    "private-key": re.compile(r"-----BEGIN (?:[A-Z0-9]+ )*PRIVATE KEY(?: BLOCK)?-----"),
    "github-token": re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})"),
    "figma-token": re.compile(r"\bfig[du]_[A-Za-z0-9_-]{20,}"),
    "personal-path": re.compile(r"(?:[A-Za-z]:[\\/]+Users[\\/]+(?!Public(?:[\\/]|\Z))[^\s\\/\"']+|(?<![:/\\])/(?:home|Users)/[^\s/\"']+)", re.I),
}
VECTOR = re.compile(r'"(?:seed_hex|secret_key|private_key|mnemonic|phrase|indices|word_indices)"\s*:\s*(?:"[^"\n]+"|\[\s*\d)', re.I)


def reviewed_vector(path, payload, allowlist=PUBLIC_VECTORS):
    return path in allowlist and hashlib.sha256(payload).hexdigest() == allowlist[path]


def inspect_text(path, text, words, *, reviewed=False):
    findings = [kind for kind, pattern in PATTERNS.items() if pattern.search(text)]
    if reviewed:
        return tuple(findings)
    if VECTOR.search(text):
        findings.append("unreviewed-vector")
    # NFKD covers the bundled Unicode lists, including ideographic whitespace.
    normalized = unicodedata.normalize("NFKD", text).lower()
    run = 0
    previous = 0
    for match in re.finditer(r"[^\W\d_](?:[^\W\d_]|[\u0300-\u036f\u3099\u309a])*", normalized, re.UNICODE):
        separator = normalized[previous:match.start()]
        if re.search(r"[^\s\"',\[\]]", separator):
            run = 0
        run = run + 1 if match.group() in words else 0
        if run >= 12:
            findings.append("mnemonic-like")
            break
        previous = match.end()
    return tuple(findings)


def scan_repository(root):
    catalog = load_catalog(root)
    if any(f.severity == "error" for f in validate_catalog(catalog, require_terminal=True)):
        return (("catalog", "invalid-scan-input"),)
    lists = {r.data["wordlist_path"]: r.data["sha256"] for r in catalog.dictionaries if r.wordlist_bytes is not None}
    words = frozenset(unicodedata.normalize("NFKD", w).lower()
                      for r in catalog.dictionaries if r.wordlist_bytes is not None
                      for w in r.wordlist_bytes.decode("utf-8").splitlines())
    result = subprocess.run(["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
                            cwd=root, capture_output=True, check=True)
    paths = sorted(set(p.decode("utf-8") for p in result.stdout.split(b"\0") if p))
    findings = []
    for relative in paths:
        path = root / relative
        if path.is_symlink() or not path.is_file() or path.stat().st_size > 16 * 1024 * 1024:
            findings.append((relative, "unsafe-or-oversized-file"))
            continue
        payload = path.read_bytes()
        if relative in SYNTHETIC_BINARIES:
            if not reviewed_vector(relative, payload, SYNTHETIC_BINARIES):
                findings.append((relative, "synthetic-binary-drift"))
            continue
        try:
            text = payload.decode("utf-8")
            if "\0" in text:
                raise ValueError("binary")
        except (UnicodeError, ValueError):
            findings.append((relative, "unreviewed-binary"))
            continue
        if relative in PUBLIC_VECTORS and not reviewed_vector(relative, payload):
            findings.append((relative, "public-vector-drift"))
        reviewed = reviewed_vector(relative, payload) or reviewed_vector(relative, payload, lists)
        findings.extend((relative, kind) for kind in inspect_text(relative, text, words, reviewed=reviewed))
    return tuple(findings)


if __name__ == "__main__":
    findings = scan_repository(Path.cwd())
    for path, kind in findings:
        print(f"error sensitive-material {path}: {kind}")
    print(f"sensitive-material: {len(findings)} findings (heuristic scan, not an audit)")
    raise SystemExit(bool(findings))
