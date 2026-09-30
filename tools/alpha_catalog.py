"""Deterministic, offline, fail-closed Windows alpha catalogue projection.

The approval set is a ceiling, never an independent source of selectability.
Every projection validates the complete catalogue, including dependency,
word-list hash, evidence, redistribution and SignPath decisions.
"""

import argparse
import hashlib
import json
import os
from pathlib import Path
import tempfile
import sys

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.catalog.loader import load_catalog
from tools.catalog.validator import validate_catalog


APPROVED = frozenset((name, "ton-native-generated") for name in
                     ("mytonwallet-native", "tonhub", "tonkeeper-classic"))


def _plain(value):
    if hasattr(value, "items"):
        return {key: _plain(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_plain(item) for item in value]
    return value


def _bytes(value):
    return (json.dumps(value, ensure_ascii=True, sort_keys=True, indent=2) + "\n").encode("utf-8")


def project(catalog):
    if any(f.severity == "error" for f in validate_catalog(catalog, require_terminal=True)):
        raise ValueError("alpha catalogue validation failed")
    schemes = {r.id: r for r in catalog.schemes}
    dictionaries = {r.id: r for r in catalog.dictionaries}
    records = sorted((*catalog.wallets, *catalog.schemes, *catalog.dictionaries,
                      *catalog.evidence, *catalog.required_sets), key=lambda r: r.id)
    digest = hashlib.sha256(_bytes([_plain(r.data) for r in records])).hexdigest()
    profiles = []
    for wallet in sorted(catalog.wallets, key=lambda r: r.id):
        data = wallet.data
        scheme = schemes.get(data["scheme_id"])
        deps = [dictionaries[i] for i in scheme.data["dictionary_ids"]] if scheme else []
        reason = ""
        if data["status"] != "verified":
            reason = "wallet-status:" + data["status"]
        elif not scheme or scheme.data["status"] != "verified":
            reason = "scheme-not-verified"
        elif not deps or any(d.data["status"] != "verified" or d.wordlist_bytes is None or
                            d.data["license"]["repository_redistribution"] != "allowed" or
                            d.data["license"]["signpath_compatible"] != "compatible" for d in deps):
            reason = "dictionary-or-license-not-verified"
        elif (wallet.id, data["mode_id"]) not in APPROVED:
            reason = "outside-approved-alpha-scope"
        evidence = sorted(set(data["evidence_ids"]) |
                          (set(scheme.data["evidence_ids"]) if scheme else set()) |
                          {e for d in deps for e in (*d.data["evidence_ids"],
                                                     *d.data["license"]["decision_evidence"])})
        profiles.append({
            "profile_id": wallet.id, "mode_id": data["mode_id"],
            "display_name": _plain(data["display_name"]), "status": data["status"],
            "scheme_id": data["scheme_id"], "selectable": not reason, "reason": reason,
            "platform": data["platform"], "version_interval": _plain(data["version_interval"]),
            "evidence_ids": evidence,
            "supported_lengths": list(scheme.data["supported_lengths"]) if scheme else [],
            "dictionaries": [{"id": d.id, "sha256": d.data["sha256"],
                              "wordlist_path": d.data["wordlist_path"],
                              "normalization": d.data["normalization"]} for d in deps],
        })
    return {"schema_version": 1, "catalog_sha256": digest, "profiles": profiles}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--output", type=Path)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)
    output = args.output or args.root / "generated/alpha/profile-matrix.json"
    stage = None
    try:
        content = _bytes(project(load_catalog(args.root)))
        if args.check:
            if not output.is_file() or output.read_bytes() != content:
                print("alpha catalogue: generated matrix drift")
                return 1
        else:
            output.parent.mkdir(parents=True, exist_ok=True)
            with tempfile.NamedTemporaryFile(dir=output.parent, delete=False) as handle:
                stage = Path(handle.name)
                handle.write(content)
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(stage, output)
            stage = None
        print("alpha catalogue: OK")
        return 0
    except (OSError, ValueError, KeyError, TypeError):
        print("alpha catalogue: rejected input or output")
        return 1
    finally:
        if stage is not None:
            stage.unlink(missing_ok=True)


if __name__ == "__main__":
    raise SystemExit(main())
