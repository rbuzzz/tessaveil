"""Bounded offline command line validation for the research catalogue."""

import argparse
from pathlib import Path
import subprocess
import sys

from .loader import load_catalog
from .validator import KINDS, SCHEMA_DIR, validate_catalog


MAX_PRINTED_FINDINGS = 25


def _schema_gate(catalog) -> bool:
    for attr, kind in KINDS:
        paths = [str(record.path) for record in getattr(catalog, attr)]
        for start in range(0, len(paths), 100):
            result = subprocess.run(
                [sys.executable, "-m", "check_jsonschema", "--schemafile",
                 str(SCHEMA_DIR / f"{kind}.schema.json"), *paths[start:start + 100]],
                capture_output=True, text=True, check=False,
            )
            if result.returncode != 0:
                print(f"error schema {kind}: pinned schema engine rejected input")
                return False
    return True


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m tools.catalog.cli")
    commands = parser.add_subparsers(dest="command", required=True)
    validate = commands.add_parser("validate")
    validate.add_argument("--root", type=Path, default=Path("."))
    mode = validate.add_mutually_exclusive_group()
    mode.add_argument("--require-terminal", action="store_true")
    mode.add_argument("--require-release-ready", action="store_true")
    validate.add_argument("--allow-incomplete-required", action="store_true")
    generate = commands.add_parser("generate")
    generate.add_argument("--root", type=Path, default=Path("."))
    generate.add_argument("--check", action="store_true", required=True)
    args = parser.parse_args(argv)
    if args.command == "generate":
        print("error generate: generated catalogue check is not implemented")
        return 1
    try:
        catalog = load_catalog(args.root)
    except (OSError, ValueError) as exc:
        print(f"error loader: {str(exc)[:120]}")
        return 1
    if not _schema_gate(catalog):
        return 1
    findings = validate_catalog(
        catalog, require_terminal=True,
        require_release_ready=args.require_release_ready,
        allow_incomplete_required=args.allow_incomplete_required,
    )
    for finding in findings[:MAX_PRINTED_FINDINGS]:
        print(f"{finding.severity} {finding.code} {finding.location}: {finding.message}")
    if len(findings) > MAX_PRINTED_FINDINGS:
        print(f"... {len(findings) - MAX_PRINTED_FINDINGS} further findings omitted")
    errors = sum(finding.severity == "error" for finding in findings)
    print(f"validation: {errors} errors, {len(findings) - errors} warnings")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
