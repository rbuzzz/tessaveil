"""Exact unsigned/synthetic Windows candidate names and external manifest."""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
import re

import alpha


NO_GO_VERDICT = "NO-GO для реальных данных"
_SHA = re.compile(r"[0-9a-f]{40}")
_SHA256 = re.compile(r"[0-9a-f]{64}")
_PREFIX = "Tessaveil-unsigned-synthetic-windows-v1-candidate-"
_GUIDANCE = {
    "candidate-docs/README.md": "README.md",
    "candidate-docs/README.ru.md": "README.ru.md",
    "candidate-docs/THREAT_MODEL.md": "THREAT_MODEL.md",
    "candidate-docs/user-guide.md": "docs/alpha/user-guide.md",
    "candidate-docs/known-limitations.md": "docs/alpha/known-limitations.md",
    "candidate-docs/release-evidence.md": "docs/alpha/release-evidence.md",
    "candidate-docs/test-protocols.md": "reports/windows-v1/test-protocols.md",
}


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def names(source_sha: str) -> dict[str, str]:
    if not isinstance(source_sha, str) or not _SHA.fullmatch(source_sha):
        raise ValueError("source SHA malformed")
    base = _PREFIX + source_sha
    return {
        "container": base,
        "runtime": base + "-runtime.zip",
        "compliance": base + "-compliance.zip",
        "decision": base + "-release-decision.json",
        "manifest": base + "-manifest.json",
    }


def paths(output: Path, source_sha: str) -> dict[str, Path]:
    resolved = names(source_sha)
    return {key: output / value for key, value in resolved.items() if key != "container"}


def guidance_material(root: Path) -> dict[str, bytes]:
    return {name: (root / source).read_bytes() for name, source in _GUIDANCE.items()}


def verify_guidance_material(files: dict[str, bytes], root: Path) -> None:
    expected = guidance_material(root)
    if any(files.get(name) != data for name, data in expected.items()):
        raise ValueError("candidate guidance material missing or changed")


def _outer(filename: str, data: bytes) -> dict:
    return {"filename": filename, "bytes": len(data), "sha256": digest(data)}


def _inner(container: str, filename: str, data: bytes) -> dict:
    return {
        "container": container,
        "filename": filename,
        "bytes": len(data),
        "sha256": digest(data),
    }


def materialize(
    source_sha: str,
    runtime_path: Path,
    compliance_path: Path,
    decision_path: Path,
) -> dict:
    resolved = names(source_sha)
    if (
        runtime_path.name != resolved["runtime"]
        or compliance_path.name != resolved["compliance"]
        or decision_path.name != resolved["decision"]
    ):
        raise ValueError("candidate manifest artifact filename mismatch")
    runtime_bytes = runtime_path.read_bytes()
    compliance_bytes = compliance_path.read_bytes()
    decision_bytes = decision_path.read_bytes()
    runtime = alpha.read_archive(runtime_path)
    for member in ("Tessaveil.exe", "sbom.cdx.json", "THIRD_PARTY_NOTICES"):
        if member not in runtime:
            raise ValueError("candidate manifest runtime member missing")
    try:
        decision = json.loads(decision_bytes)
    except (UnicodeError, json.JSONDecodeError) as error:
        raise ValueError("candidate manifest release decision unreadable") from error
    if (
        decision.get("verdict") != NO_GO_VERDICT
        or decision.get("candidate", {}).get("source_sha") != source_sha
    ):
        raise ValueError("candidate manifest release decision is stale or promoted")
    artifacts = {
        "runtime_zip": _outer(resolved["runtime"], runtime_bytes),
        "compliance_zip": _outer(resolved["compliance"], compliance_bytes),
        "release_decision": _outer(resolved["decision"], decision_bytes),
        "executable": _inner(resolved["runtime"], "Tessaveil.exe", runtime["Tessaveil.exe"]),
        "sbom": _inner(resolved["runtime"], "sbom.cdx.json", runtime["sbom.cdx.json"]),
        "notices": _inner(
            resolved["runtime"], "THIRD_PARTY_NOTICES", runtime["THIRD_PARTY_NOTICES"]
        ),
    }
    return {
        "schema_version": 1,
        "candidate": {
            "name": resolved["container"],
            "source_sha": source_sha,
            "unsigned": True,
            "synthetic_only": True,
            "real_data_authorized": False,
            "verdict": NO_GO_VERDICT,
        },
        "artifacts": artifacts,
        "provenance_subjects": [
            resolved["runtime"],
            resolved["compliance"],
            resolved["decision"],
            resolved["manifest"],
        ],
    }


def validate(report: dict) -> dict:
    if not isinstance(report, dict) or set(report) != {
        "schema_version",
        "candidate",
        "artifacts",
        "provenance_subjects",
    }:
        raise ValueError("candidate manifest fields invalid")
    candidate = report["candidate"]
    if not isinstance(candidate, dict) or set(candidate) != {
        "name",
        "source_sha",
        "unsigned",
        "synthetic_only",
        "real_data_authorized",
        "verdict",
    }:
        raise ValueError("candidate manifest identity invalid")
    resolved = names(candidate.get("source_sha"))
    if candidate != {
        "name": resolved["container"],
        "source_sha": candidate["source_sha"],
        "unsigned": True,
        "synthetic_only": True,
        "real_data_authorized": False,
        "verdict": NO_GO_VERDICT,
    }:
        raise ValueError("candidate manifest status invalid")
    if type(report["schema_version"]) is not int or report["schema_version"] != 1:
        raise ValueError("candidate manifest schema invalid")
    if report["provenance_subjects"] != [
        resolved["runtime"],
        resolved["compliance"],
        resolved["decision"],
        resolved["manifest"],
    ]:
        raise ValueError("candidate manifest provenance subjects invalid")
    expected_artifacts = {
        "runtime_zip",
        "compliance_zip",
        "release_decision",
        "executable",
        "sbom",
        "notices",
    }
    artifacts = report["artifacts"]
    if not isinstance(artifacts, dict) or set(artifacts) != expected_artifacts:
        raise ValueError("candidate manifest artifact set invalid")
    for key, record in artifacts.items():
        outer = key in {"runtime_zip", "compliance_zip", "release_decision"}
        required = {"filename", "bytes", "sha256"} | (set() if outer else {"container"})
        if (
            not isinstance(record, dict)
            or set(record) != required
            or not isinstance(record["filename"], str)
            or not record["filename"]
            or type(record["bytes"]) is not int
            or record["bytes"] < 1
            or not isinstance(record["sha256"], str)
            or not _SHA256.fullmatch(record["sha256"])
        ):
            raise ValueError("candidate manifest artifact record invalid")
    return report


def validate_exact_candidate(
    report: dict,
    source_sha: str,
    runtime_path: Path,
    compliance_path: Path,
    decision_path: Path,
) -> dict:
    validate(report)
    try:
        expected = materialize(source_sha, runtime_path, compliance_path, decision_path)
    except (OSError, ValueError) as error:
        raise ValueError("candidate manifest exact-byte verification failed") from error
    if report != expected:
        raise ValueError("candidate manifest exact-byte verification failed")
    return report


def encode(report: dict) -> bytes:
    validate(report)
    return (json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode(
        "utf-8"
    )
