"""Finalize only an independently audited clean-SHA build and real Qt relink."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys

import alpha
import release_decision
import verify


def encode(value):
    return (json.dumps(value, sort_keys=True, indent=2) + "\n").encode()


def finish(output, relink, smoke_path, source_sha):
    if subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=alpha.ROOT).decode().strip() != source_sha or subprocess.check_output(["git", "status", "--porcelain", "--untracked-files=all"], cwd=alpha.ROOT):
        raise ValueError("finalization requires the exact clean source checkout")
    runtime_path, compliance_path = output / "runtime-analysis.zip", output / "compliance-analysis.zip"
    verify.verify(runtime_path, compliance_path, source_sha)
    runtime, compliance = alpha.read_archive(runtime_path), alpha.read_archive(compliance_path)
    evidence = json.loads(runtime["release-evidence.json"])
    receipt = json.loads(compliance["build-receipt.json"])
    if evidence.get("working_tree_dirty") or receipt.get("working_tree_dirty") or evidence.get("audit_findings"):
        raise ValueError("analysis-only build cannot be finalized")
    modified = (relink / "app/Tessaveil.exe").read_bytes()
    marker = subprocess.run([str(relink / "app/qt_marker.exe")], capture_output=True, check=True).stdout.decode().strip()
    application = {name: alpha.digest(data) for name, data in compliance.items() if name.startswith("application/")}
    # The staged objects were the link inputs; reject any change since packaging.
    if any(alpha.digest((output / "compliance" / name).read_bytes()) != digest for name, digest in application.items()):
        raise ValueError("application objects changed during relink")
    proof = {"source_sha": source_sha, "original_exe_sha256": alpha.digest(runtime["Tessaveil.exe"]),
             "modified_exe_sha256": alpha.digest(modified), "application_sha256": application,
             "modified_qt_marker_in_application": b"6.8.3-tessaveil-relink-test" in modified,
             "marker_probe": marker, "synthetic_smoke": json.loads(smoke_path.read_bytes()),
             "qt_source_sha256": alpha.digest(compliance["qtbase-6.8.3.zip"]),
             "modified_qt_source_sha256": {name: alpha.digest((relink / "qtbase-everywhere-src-6.8.3" / name).read_bytes()) for name in ("src/corelib/global/qlibraryinfo.cpp", "src/widgets/kernel/qapplication.cpp")},
             "scope": "Actual modified Qt rebuilt from bundled source and unchanged application material relinked; primary EXE remains unmodified Qt"}
    alpha.check_relink_proof(proof, source_sha, alpha.digest(runtime["Tessaveil.exe"]), application)
    review = json.loads(compliance["distribution-review.json"])
    if review.get("release_decision_required") is not True or review.get(
        "real_data_authorization"
    ) != "all-mandatory-gates-pass":
        raise ValueError("distribution review does not require the fail-closed release decision")
    clearance = {"status": "PASS", "source_sha": source_sha,
                 "corresponding_source": True, "application_material": True,
                 "modified_qt_relink": True, "replacement_information": True,
                 "qt_third_party_review": review.get("qt_third_party_review"),
                 "rust_runtime_review": review.get("rust_runtime_review"),
                 "dictionary_review": review.get("dictionary_review"), "artifact_audit": True}
    alpha.require_distribution_clearance(clearance, source_sha)
    evidence.update({"status": "LOCAL_EXACT_SHA_ALPHA_GATE_PASS", "compliance": clearance,
                     "github_provenance": "NOT CLAIMED BY LOCAL GATE; official CI attestation required",
                     "relink_proof_sha256": alpha.digest(encode(proof))})
    runtime["release-evidence.json"] = encode(evidence)
    compliance["relink-proof.json"] = encode(proof)
    for files in (runtime, compliance):
        files.pop("SHA256SUMS")
        files["SHA256SUMS"] = alpha.make_manifest(files)
    alpha.write_archive(output / "runtime.zip", runtime)
    alpha.write_archive(output / "compliance.zip", compliance)
    decision = release_decision.materialize(
        json.loads((alpha.ROOT / "reports/windows-v1/release-decision.json").read_bytes()),
        source_sha,
        output / "runtime.zip",
        output / "compliance.zip",
        output / "runtime/Tessaveil.exe",
    )
    decision_path = output / "release-decision.json"
    decision_path.write_bytes(release_decision.encode(decision))
    result = verify.verify(
        output / "runtime.zip",
        output / "compliance.zip",
        source_sha,
        distribution=True,
        decision_path=decision_path,
    )
    subprocess.run([sys.executable, "-m", "unittest", "tests.repository.test_windows_alpha_distribution", "-v"],
                   cwd=alpha.ROOT, env=dict(os.environ, TESSAVEIL_ALPHA_AUDIT_ROOT=str(output.resolve())), check=True)
    # Workflow checks this receipt as well as process success before uploading.
    (output / "GATE-PASS.json").write_bytes(encode(result))
    print(json.dumps(result))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("output", "relink", "smoke"):
        parser.add_argument("--" + name, type=Path, required=True)
    parser.add_argument("--source-sha", required=True)
    args = parser.parse_args()
    finish(args.output, args.relink, args.smoke, args.source_sha)
