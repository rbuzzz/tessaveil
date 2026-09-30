"""Bounded offline command line validation for the research catalogue."""

import argparse
import os
from pathlib import Path
import subprocess
import sys
import tempfile

from .generator import render_catalog
from .loader import load_catalog
from .validator import KINDS, SCHEMA_DIR, validate_catalog


MAX_PRINTED_FINDINGS = 25


def _plain_path(path: Path) -> bool:
    return not path.is_symlink() and not path.is_junction()


def _generate(catalog, check: bool) -> int:
    """Stage the complete pair before replacement; roll back ordinary failures.

    The exclusive marker makes concurrent generators and interrupted publication
    fail closed. Two files cannot be power-loss atomic: after process death keep
    the marker and staging/backup files for manual inspection and recovery.
    Check mode is read-only, including on missing files or a leftover marker.
    """
    try:
        rendered = [render_catalog(catalog, locale).encode("utf-8") for locale in ("en", "ru")]
        docs = catalog.root / "docs"
        paths = [docs / name for name in ("catalog.md", "catalog.ru.md")]
        marker = docs / ".catalog-generation.lock"
        if not _plain_path(docs) or (docs.exists() and not docs.is_dir()):
            raise ValueError("unsafe output directory")
        if marker.exists() or not _plain_path(marker):
            raise ValueError("generation in progress or interrupted")
        if any(not _plain_path(p) or (p.exists() and not p.is_file()) for p in paths):
            raise ValueError("unsafe output file")
        if check:
            matching = all(p.is_file() and p.read_bytes() == content for p, content in zip(paths, rendered))
            # Recheck the marker after reading so an in-flight writer fails closed.
            if marker.exists() or not _plain_path(marker):
                raise ValueError("generation in progress or interrupted")
            print("generation: documents match" if matching else "error generate: missing or stale documents")
            return 0 if matching else 1
        docs.mkdir(exist_ok=True)
        marker.mkdir()  # Exclusive; never remove a marker belonging to another writer.
        staging = None
        restored = False
        replaced = []
        try:
            staging = Path(tempfile.mkdtemp(prefix=".catalog-stage-", dir=docs))
            old = [p.read_bytes() if p.exists() else None for p in paths]
            for index, content in enumerate(rendered):
                (staging / f"new-{index}").write_bytes(content)
                if old[index] is not None:
                    (staging / f"old-{index}").write_bytes(old[index])
            try:
                for index, target in enumerate(paths):
                    os.replace(staging / f"new-{index}", target)
                    replaced.append(index)
            except OSError:
                for index in reversed(replaced):
                    if old[index] is None:
                        paths[index].unlink()
                    else:
                        os.replace(staging / f"old-{index}", paths[index])
                restored = True
                raise
            restored = True
        except OSError:
            # If no replacements started, the original pair is still intact.
            if not replaced:
                restored = True
            raise
        finally:
            if restored:
                if staging is not None:
                    for child in staging.iterdir():
                        child.unlink()
                    staging.rmdir()
                marker.rmdir()
        print("generation: wrote both documents")
        return 0
    except (OSError, ValueError):
        # Do not print exception paths or source metadata.
        print("error generate: input/output rejected; inspect catalogue, output files and generation marker")
        return 1


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
    generate.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)
    try:
        catalog = load_catalog(args.root)
    except (OSError, ValueError) as exc:
        print("error loader: input rejected" if args.command == "generate" else f"error loader: {str(exc)[:120]}")
        return 1
    if not _schema_gate(catalog):
        return 1
    if args.command == "generate":
        return _generate(catalog, args.check)
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
