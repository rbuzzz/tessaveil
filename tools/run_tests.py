"""Run the repository's discovered unittest suite, rejecting empty discovery."""

from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    suite = unittest.defaultTestLoader.discover(
        start_dir=str(ROOT / "tests"), top_level_dir=str(ROOT)
    )
    count = suite.countTestCases()
    print(f"Discovered tests: {count}", flush=True)
    if count == 0:
        print("No tests discovered; refusing an empty test run.", file=sys.stderr)
        return 1

    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
