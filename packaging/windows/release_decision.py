"""Strict Windows v1 release-decision validation and exact-candidate binding."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
import re


REAL_DATA_VERDICT = "кандидат допущен к использованию с реальными данными"
NO_GO_VERDICT = "NO-GO для реальных данных"
MANDATORY_GATE_IDS = (
    "catalogue-research-readiness",
    "selectable-profile-vectors",
    "core-security-failure-suite",
    "parser-fuzz-evidence",
    "format-kdf-physical-freeze",
    "figma-handoff",
    "complete-windows-workflows",
    "clean-windows-10",
    "clean-windows-11",
    "physical-android-4gib",
    "physical-android-current",
    "physical-iphone-a13",
    "physical-iphone-current",
    "mac-xcode-native-build",
    "removable-ntfs",
    "removable-exfat",
    "controlled-power-loss",
    "network-trace",
    "temp-extraction-trace",
    "process-file-startup-log-trace",
    "accessibility-narrator-scaling",
    "independent-security-audit",
    "signpath-authenticode",
    "licensing",
    "sbom-notices",
    "qt-source-relink",
    "exact-sha-ci",
    "github-provenance",
    "bilingual-docs-threat-limitations-parity",
)
NO_DEVELOPMENT_SUBSTITUTION = frozenset(
    {
        "format-kdf-physical-freeze",
        "figma-handoff",
        "clean-windows-10",
        "clean-windows-11",
        "physical-android-4gib",
        "physical-android-current",
        "physical-iphone-a13",
        "physical-iphone-current",
        "mac-xcode-native-build",
        "removable-ntfs",
        "removable-exfat",
        "controlled-power-loss",
        "network-trace",
        "temp-extraction-trace",
        "process-file-startup-log-trace",
        "accessibility-narrator-scaling",
        "independent-security-audit",
        "signpath-authenticode",
    }
)
HOSTED_GITHUB_GATES = frozenset({"exact-sha-ci", "github-provenance"})
HOSTED_GITHUB_ENVIRONMENT = "GitHub-hosted runner windows-2022"
_SHA256 = re.compile(r"[0-9a-f]{64}")
_GIT_SHA = re.compile(r"[0-9a-f]{40}")
_DATE = re.compile(r"20[0-9]{2}-[01][0-9]-[0-3][0-9]")
_RECEIPT_PATH = re.compile(r"[A-Za-z0-9][A-Za-z0-9._/-]*\.json")
_DEVELOPMENT = re.compile(
    r"development(?:-| )host|hosted runner|simulator|emulator|virtual machine|\bvm\b",
    re.IGNORECASE,
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _exact_keys(value: dict, expected: set[str], label: str) -> None:
    if not isinstance(value, dict) or set(value) != expected:
        raise ValueError(f"{label} fields are missing or unknown")


def validate(report: dict, *, template: bool = False) -> dict:
    _exact_keys(
        report,
        {"schema_version", "policy", "candidate", "verdict", "gates"},
        "report",
    )
    if type(report["schema_version"]) is not int or report["schema_version"] != 1:
        raise ValueError("unsupported release-decision schema")
    policy = report["policy"]
    _exact_keys(
        policy,
        {"candidate_binding", "real_data_rule", "missing_evidence"},
        "policy",
    )
    if policy != {
        "candidate_binding": "source-sha-plus-runtime-compliance-executable-sha256",
        "real_data_rule": "all-mandatory-gates-pass",
        "missing_evidence": "blocked",
    }:
        raise ValueError("release-decision policy drift")

    candidate = report["candidate"]
    _exact_keys(
        candidate,
        {"kind", "source_sha", "artifacts", "provenance_subject_sha256"},
        "candidate",
    )
    if template:
        if candidate != {
            "kind": "policy-template",
            "source_sha": None,
            "artifacts": {},
            "provenance_subject_sha256": [],
        }:
            raise ValueError("policy template must not claim a candidate SHA or artifact")
    else:
        source_sha = candidate.get("source_sha")
        if (
            candidate["kind"] != "exact-candidate"
            or not isinstance(source_sha, str)
            or not _GIT_SHA.fullmatch(source_sha)
        ):
            raise ValueError("exact candidate source SHA missing or malformed")
        artifacts = candidate["artifacts"]
        _exact_keys(artifacts, {"runtime", "compliance", "executable"}, "artifacts")
        for name, record in artifacts.items():
            _exact_keys(record, {"sha256"}, f"artifact {name}")
            if not isinstance(record["sha256"], str) or not _SHA256.fullmatch(
                record["sha256"]
            ):
                raise ValueError(f"artifact {name} hash malformed")
        if candidate["provenance_subject_sha256"] != [
            artifacts["runtime"]["sha256"],
            artifacts["compliance"]["sha256"],
        ]:
            raise ValueError("provenance subjects are not the runtime/compliance hashes")

    rows = report["gates"]
    if not isinstance(rows, list):
        raise ValueError("gates must be a list")
    if any(not isinstance(row, dict) for row in rows):
        raise ValueError("each gate must be an object")
    ids = [row.get("id") for row in rows]
    if any(not isinstance(gate_id, str) for gate_id in ids):
        raise ValueError("gate id must be a string")
    if len(rows) != len(MANDATORY_GATE_IDS) or len(ids) != len(set(ids)):
        raise ValueError("mandatory gate rows are missing or duplicated")
    if set(ids) != set(MANDATORY_GATE_IDS):
        raise ValueError("mandatory gate rows are missing or unknown")
    for row in rows:
        _exact_keys(
            row,
            {"id", "result", "evidence", "blocker", "clearance_action"},
            "gate",
        )
        if row["result"] not in {"pass", "fail", "blocked"}:
            raise ValueError("gate result must be pass, fail or blocked")
        evidence = row["evidence"]
        _exact_keys(
            evidence,
            {"scope", "sha256", "environment", "date", "receipts", "references"},
            "gate evidence",
        )
        if (
            not isinstance(evidence["scope"], str)
            or not evidence["scope"].strip()
            or not isinstance(evidence["sha256"], str)
            or not _SHA256.fullmatch(evidence["sha256"])
            or not isinstance(evidence["environment"], str)
            or not evidence["environment"].strip()
            or not isinstance(evidence["date"], str)
            or not _DATE.fullmatch(evidence["date"])
            or not isinstance(evidence["references"], list)
            or not evidence["references"]
            or any(not isinstance(item, str) or not item.strip() for item in evidence["references"])
        ):
            raise ValueError("gate evidence scope/hash/environment/date/reference invalid")
        receipts = evidence["receipts"]
        if not isinstance(receipts, list):
            raise ValueError("gate evidence receipts must be a list")
        receipt_paths = []
        for receipt in receipts:
            _exact_keys(receipt, {"path", "sha256"}, "gate evidence receipt")
            if (
                not isinstance(receipt["path"], str)
                or not _RECEIPT_PATH.fullmatch(receipt["path"])
                or receipt["path"].startswith("/")
                or ".." in receipt["path"].split("/")
                or not isinstance(receipt["sha256"], str)
                or not _SHA256.fullmatch(receipt["sha256"])
            ):
                raise ValueError("gate evidence receipt path/hash invalid")
            receipt_paths.append(receipt["path"])
        if len(receipt_paths) != len(set(receipt_paths)):
            raise ValueError("gate evidence receipts are duplicated")
        if row["result"] == "pass":
            if row["blocker"] is not None or row["clearance_action"] is not None:
                raise ValueError("passed gate cannot retain a blocker")
            if row["id"] in NO_DEVELOPMENT_SUBSTITUTION and _DEVELOPMENT.search(
                evidence["environment"] + " " + evidence["scope"]
            ):
                raise ValueError("development-host evidence cannot substitute for this gate")
            if (
                row["id"] in HOSTED_GITHUB_GATES
                and evidence["environment"] != HOSTED_GITHUB_ENVIRONMENT
            ):
                raise ValueError(
                    "exact-SHA CI and provenance require GitHub-hosted runner windows-2022"
                )
        elif (
            not isinstance(row["blocker"], str)
            or not row["blocker"].strip()
            or not isinstance(row["clearance_action"], str)
            or not row["clearance_action"].strip()
        ):
            raise ValueError("fail/blocked gate requires blocker and clearance action")

    expected_verdict = (
        REAL_DATA_VERDICT
        if all(row["result"] == "pass" for row in rows)
        else NO_GO_VERDICT
    )
    if report["verdict"] != expected_verdict:
        raise ValueError("release verdict does not match mandatory gate results")
    return report


def materialize(
    template_report: dict,
    source_sha: str,
    runtime_path: Path,
    compliance_path: Path,
    executable_path: Path,
) -> dict:
    validate(template_report, template=True)
    if not isinstance(source_sha, str) or not _GIT_SHA.fullmatch(source_sha):
        raise ValueError("source SHA malformed")
    report = copy.deepcopy(template_report)
    runtime_hash = digest(runtime_path)
    compliance_hash = digest(compliance_path)
    report["candidate"] = {
        "kind": "exact-candidate",
        "source_sha": source_sha,
        "artifacts": {
            "runtime": {"sha256": runtime_hash},
            "compliance": {"sha256": compliance_hash},
            "executable": {"sha256": digest(executable_path)},
        },
        "provenance_subject_sha256": [runtime_hash, compliance_hash],
    }
    return validate(report)


def validate_exact_candidate(
    report: dict,
    source_sha: str,
    runtime_path: Path,
    compliance_path: Path,
    executable_path: Path,
) -> dict:
    return validate_exact_candidate_hashes(
        report,
        source_sha,
        digest(runtime_path),
        digest(compliance_path),
        digest(executable_path),
    )


def validate_exact_candidate_hashes(
    report: dict,
    source_sha: str,
    runtime_sha256: str,
    compliance_sha256: str,
    executable_sha256: str,
) -> dict:
    validate(report)
    candidate = report["candidate"]
    if candidate["source_sha"] != source_sha:
        raise ValueError("candidate source SHA is stale")
    actual = {
        "runtime": runtime_sha256,
        "compliance": compliance_sha256,
        "executable": executable_sha256,
    }
    if any(candidate["artifacts"][name]["sha256"] != value for name, value in actual.items()):
        raise ValueError("candidate artifact hash drift")
    return report


def _load_receipt(evidence_root: Path, record: dict) -> dict:
    root = evidence_root.resolve(strict=True)
    candidate = (root / record["path"]).resolve(strict=False)
    try:
        candidate.relative_to(root)
    except ValueError as error:
        raise ValueError("evidence receipt escapes the evidence root") from error
    if not candidate.is_file():
        raise ValueError(f"evidence receipt missing: {record['path']}")
    if digest(candidate) != record["sha256"]:
        raise ValueError(f"evidence receipt hash drift: {record['path']}")
    try:
        receipt = json.loads(candidate.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise ValueError(f"evidence receipt is unreadable: {record['path']}") from error
    _exact_keys(
        receipt,
        {
            "schema_version",
            "gate_id",
            "result",
            "candidate",
            "scope",
            "environment",
            "date",
        },
        "evidence receipt",
    )
    if type(receipt["schema_version"]) is not int or receipt["schema_version"] != 1:
        raise ValueError("unsupported evidence receipt schema")
    return receipt


def require_real_data(report: dict, evidence_root: Path | None = None) -> None:
    validate(report, template=report.get("candidate", {}).get("kind") == "policy-template")
    if report["candidate"]["kind"] != "exact-candidate":
        raise ValueError("real-data authorization requires an exact candidate")
    if report["verdict"] != REAL_DATA_VERDICT:
        raise ValueError("real-data authorization requires every mandatory gate to pass")
    if evidence_root is None:
        raise ValueError("real-data authorization requires an evidence root")
    try:
        root = evidence_root.resolve(strict=True)
    except OSError as error:
        raise ValueError("real-data evidence root is missing") from error
    if not root.is_dir():
        raise ValueError("real-data evidence root is not a directory")

    for row in report["gates"]:
        evidence = row["evidence"]
        receipts = evidence["receipts"]
        if not receipts:
            raise ValueError(f"real-data gate has no evidence receipt: {row['id']}")
        if evidence["sha256"] != receipts[0]["sha256"]:
            raise ValueError(f"gate evidence hash does not identify its primary receipt: {row['id']}")
        for record in receipts:
            receipt = _load_receipt(root, record)
            if receipt["gate_id"] != row["id"] or receipt["result"] != "pass":
                raise ValueError(f"evidence receipt gate/result mismatch: {record['path']}")
            if receipt["candidate"] != report["candidate"]:
                raise ValueError(f"evidence receipt candidate binding mismatch: {record['path']}")
            for field in ("scope", "environment", "date"):
                if receipt[field] != evidence[field]:
                    raise ValueError(
                        f"evidence receipt {field} mismatch: {record['path']}"
                    )


def encode(report: dict) -> bytes:
    return (json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode(
        "utf-8"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    validation = subparsers.add_parser("validate")
    validation.add_argument("--report", type=Path, required=True)
    validation.add_argument("--template", action="store_true")
    for command in ("materialize", "verify"):
        item = subparsers.add_parser(command)
        item.add_argument("--report", type=Path, required=True)
        item.add_argument("--source-sha", required=True)
        item.add_argument("--runtime", type=Path, required=True)
        item.add_argument("--compliance", type=Path, required=True)
        item.add_argument("--executable", type=Path, required=True)
        if command == "materialize":
            item.add_argument("--output", type=Path, required=True)
        else:
            item.add_argument("--require-real-data", action="store_true")
            item.add_argument("--evidence-root", type=Path)
    args = parser.parse_args()
    report = json.loads(args.report.read_text(encoding="utf-8"))
    if args.command == "validate":
        validate(report, template=args.template)
    elif args.command == "materialize":
        result = materialize(
            report, args.source_sha, args.runtime, args.compliance, args.executable
        )
        args.output.write_bytes(encode(result))
    else:
        validate_exact_candidate(
            report, args.source_sha, args.runtime, args.compliance, args.executable
        )
        if args.require_real_data:
            require_real_data(report, args.evidence_root)
    print(json.dumps({"status": "PASS", "verdict": report["verdict"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
