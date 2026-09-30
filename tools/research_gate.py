"""Research CI verifies an honest report; this is NEVER a release promotion gate."""

import argparse
from dataclasses import asdict
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

from tools.catalog.loader import load_catalog
from tools.catalog.validator import validate_catalog

REPORT = "docs/research/subproject-1-verification.md"


def read_contract(root):
    text = (root / REPORT).read_text(encoding="utf-8")
    blocks = re.findall(r"```json\n(.*?)\n```", text, re.S)
    if len(blocks) != 1:
        raise ValueError("missing or ambiguous gate contract")
    return json.loads(blocks[0])


def overall_status(code, blockers):
    return "GO" if code == 0 and not blockers else "NO-GO"


def matches(expected, code, output):
    return (code in (0, 1) and expected == {
        "exit_code": code, "output": output, "status": "GO" if code == 0 else "NO-GO"})


def verify_inputs(root, report):
    errors = []
    required = {p.relative_to(root).as_posix() for pattern in ("reports/spikes/*.md", "docs/adr/*.md")
                for p in root.glob(pattern)} | {"docs/research/third-party-notices-source.txt"}
    if set(report["evidence_sha256"]) != required:
        errors.append("missing or unexpected evidence fingerprints")
    equipment = root / "reports/spikes/equipment-availability.md"
    rows = [line.split("|")[1:-1] for line in equipment.read_text(encoding="utf-8").splitlines()
            if line.startswith("| ")]
    blockers = [{"environment": row[0].strip(), "reason": row[5].strip()}
                for row in rows if len(row) == 7 and row[4].strip() == "blocked"]
    if report["external_blockers"] != blockers:
        errors.append("physical/clean-equipment blockers differ from inventory")
    for relative, digest in report["evidence_sha256"].items():
        path = root / relative
        if (path.is_absolute() and not path.resolve().is_relative_to(root.resolve())) or ".." in Path(relative).parts:
            errors.append("unsafe evidence path")
        elif not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != digest:
            errors.append(f"evidence drift: {relative}")
    return tuple(errors)


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate-sha")
    args = parser.parse_args(argv)
    root = Path.cwd()
    try:
        report = read_contract(root)
        errors = list(verify_inputs(root, report))
        if args.candidate_sha is not None:
            head = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
            if not re.fullmatch(r"[0-9a-f]{40}", args.candidate_sha) or head != args.candidate_sha:
                errors.append("CI candidate does not match checkout HEAD")
            if subprocess.run(["git", "diff", "--quiet", "HEAD", "--"]).returncode != 0:
                errors.append("candidate tracked tree is dirty")
            base = report["audited_input_sha"]
            if not re.fullmatch(r"[0-9a-f]{40}", base) or subprocess.run(
                    ["git", "merge-base", "--is-ancestor", base, head]).returncode != 0:
                errors.append("audited input is not an ancestor of candidate")
            print(f"CI candidate: {head}; audited input: {base}")
        catalog = load_catalog(root)
        terminal = validate_catalog(catalog, require_terminal=True)
        if any(f.severity == "error" for f in terminal):
            errors.append("terminal research validation failed")
        result = subprocess.run([sys.executable, "-m", "tools.catalog.cli", "validate", "--root", ".",
                                 "--require-release-ready"], capture_output=True, text=True, encoding="utf-8")
        print(result.stdout, end="")
        if result.stderr or not matches(report["catalogue_release"], result.returncode, result.stdout):
            errors.append("release CLI exit/output differs from committed report")
        actual = [asdict(f) for f in validate_catalog(catalog, require_terminal=True, require_release_ready=True)]
        if actual != report["release_findings"]:
            errors.append("complete release findings differ from committed report")
        if overall_status(result.returncode, report["external_blockers"]) != report["windows_release"]:
            errors.append("overall Windows release status differs from evidence")
        if report["research_completeness"] != "COMPLETE":
            errors.append("research completeness not recorded")
        for error in errors:
            print(f"error handoff: {error}")
        print(f"research report: {'FAIL' if errors else 'PASS'}; Windows release: {report['windows_release']}")
        return 1 if errors else 0
    except (OSError, ValueError, KeyError, TypeError, subprocess.SubprocessError):
        print("error handoff: malformed report or unavailable evidence")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
