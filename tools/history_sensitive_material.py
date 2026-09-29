"""Read-only scan of every distinct blob reachable from local Git refs.

Findings contain object IDs and classes only; blob contents and paths are never
printed. A full checkout is required so CI cannot silently scan a shallow slice.
"""

import argparse
import hashlib
from pathlib import Path
import re
import subprocess
import unicodedata

from tools.catalog.loader import load_catalog
from tools.catalog.validator import UNRESOLVED_VOCABULARY_SHA256, validate_catalog
from tools.sensitive_material import PUBLIC_VECTORS, SYNTHETIC_BINARIES, inspect_text

MAX_BLOB_BYTES = 16 * 1024 * 1024
OID = re.compile(rb"[0-9a-f]{40,64}")
# Reviewed earlier revisions of synthetic path tests. Only their path finding is
# exempt; credential and private-key classes still fail for these exact blobs.
REVIEWED_SYNTHETIC_PATH_BLOBS = frozenset({
    "27124d5b5deafe24ba3d96eeaaff1680e8862c40",
    "41190ba6d5901ce1845fc02f50042be3b3538b1b",
    "83fee807048a8c06be58b74b7208d5dc26758072",
    "926484a3d4f029cf6c7ddbce9de2fd77d237874b",
    "ab30a2193a8ee2c15ae3c5b23276434f0460a009",
    "c3d873f50698e8929ee45c0f1c263b5bfccea26e",
})
# Earlier public source-projection fixtures at their exact Git blob IDs. These
# revisions predate the current vector allowlist; generic secret/path checks run.
REVIEWED_HISTORICAL_VECTOR_BLOBS = frozenset({
    "5b21cbab486d0180e26399594804e94aab7d3377",  # Monero/Polyseed
    "c27af168e6d09f30d41ac4a25182162a92e89eca",  # Zano/Sia/Zcash/Chia
})


def _git(root, *args, input=None):
    return subprocess.run(["git", *args], cwd=root, input=input, capture_output=True,
                          check=True).stdout


def scan_history(root, *, max_blob_bytes=MAX_BLOB_BYTES, words=None):
    root = Path(root)
    reviewed_text_hashes = set(PUBLIC_VECTORS.values()) | set(UNRESOLVED_VOCABULARY_SHA256)
    if (root / "catalog").is_dir():
        catalog = load_catalog(root)
        if any(f.severity == "error" for f in validate_catalog(catalog, require_terminal=True)):
            return (("catalog", "invalid-scan-input"),)
        reviewed_text_hashes.update(r.data["sha256"] for r in catalog.dictionaries
                                    if r.wordlist_bytes is not None)
        if words is None:
            words = frozenset(unicodedata.normalize("NFKD", word).lower()
                              for r in catalog.dictionaries if r.wordlist_bytes is not None
                              for word in r.wordlist_bytes.decode("utf-8").splitlines())
    if words is None:
        words = frozenset()
    if _git(root, "rev-parse", "--is-shallow-repository").strip() != b"false":
        return (("history", "shallow-checkout"),)
    listed = _git(root, "rev-list", "--objects", "--all").splitlines()
    oids = sorted({line.split(b" ", 1)[0] for line in listed})
    if not oids or any(not OID.fullmatch(oid) for oid in oids):
        return (("history", "invalid-object-list"),)
    checked = _git(root, "cat-file", "--batch-check=%(objectname) %(objecttype) %(objectsize)",
                   input=b"\n".join(oids) + b"\n").splitlines()
    if len(checked) != len(oids):
        return (("history", "invalid-object-list"),)
    blobs = []
    findings = []
    for line in checked:
        parts = line.split()
        if len(parts) != 3 or not OID.fullmatch(parts[0]) or not parts[2].isdigit():
            return (("history", "invalid-object-list"),)
        if parts[1] != b"blob":
            continue
        oid = parts[0].decode("ascii")
        size = int(parts[2])
        if size > max_blob_bytes:
            findings.append((oid, "oversized-blob"))
        else:
            blobs.append((oid, size))
    allowed_binary_hashes = frozenset(SYNTHETIC_BINARIES.values())
    with subprocess.Popen(["git", "cat-file", "--batch"], cwd=root,
                          stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                          stderr=subprocess.DEVNULL) as process:
        for oid, size in blobs:
            process.stdin.write(oid.encode("ascii") + b"\n")
            process.stdin.flush()
            header = process.stdout.readline().split()
            if (len(header) != 3 or header[0] != oid.encode("ascii") or
                    header[1] != b"blob" or header[2] != str(size).encode("ascii")):
                findings.append((oid, "malformed-blob"))
                break
            payload = process.stdout.read(size)
            delimiter = process.stdout.read(1)
            if len(payload) != size or delimiter != b"\n":
                findings.append((oid, "malformed-blob"))
                break
            try:
                text = payload.decode("utf-8")
                if "\0" in text:
                    raise ValueError("binary")
            except (UnicodeError, ValueError):
                if hashlib.sha256(payload).hexdigest() not in allowed_binary_hashes:
                    findings.append((oid, "unreviewed-binary"))
                continue
            digest = hashlib.sha256(payload).hexdigest()
            findings.extend((oid, kind) for kind in inspect_text(
                "history-blob", text, words,
                reviewed=digest in reviewed_text_hashes or oid in REVIEWED_HISTORICAL_VECTOR_BLOBS)
                            if kind != "personal-path" or oid not in REVIEWED_SYNTHETIC_PATH_BLOBS)
        process.stdin.close()
        if process.wait() != 0:
            findings.append(("history", "git-object-read-failed"))
    return tuple(findings)


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args(argv)
    try:
        findings = scan_history(args.root)
    except (OSError, ValueError, subprocess.CalledProcessError):
        findings = (("history", "git-scan-failed"),)
    for oid, kind in findings:
        print(f"error history-sensitive-material {oid}: {kind}")
    print(f"history-sensitive-material: {len(findings)} findings across reachable refs")
    return int(bool(findings))


if __name__ == "__main__":
    raise SystemExit(main())
