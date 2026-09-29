"""The one shared fixture corpus must agree with the pinned schema engine."""

from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

from tools.catalog.loader import load_catalog
from tools.catalog.validator import validate_catalog


ROOT = Path(__file__).resolve().parents[2]
FIXTURES = Path(__file__).parent / "fixtures"
KINDS = {"dictionaries": "dictionary", "schemes": "scheme", "wallets": "wallet",
         "evidence": "evidence", "required": "required-set"}


class SchemaParityTests(unittest.TestCase):
    def test_shared_fixture_cases(self):
        cases = [None, *sorted((FIXTURES / "invalid-schema").iterdir())]
        for overlay in cases:
            with self.subTest(case=overlay.name if overlay else "valid-minimal"):
                with tempfile.TemporaryDirectory() as directory:
                    root = Path(directory)
                    shutil.copytree(FIXTURES / "valid-minimal", root, dirs_exist_ok=True)
                    if overlay:
                        shutil.copytree(overlay, root, dirs_exist_ok=True)
                    schema_ok = True
                    for folder, kind in KINDS.items():
                        for instance in sorted((root / "catalog" / folder).glob("*.json")):
                            result = subprocess.run([
                                sys.executable, "-m", "check_jsonschema", "--schemafile",
                                str(ROOT / "catalog/schema" / f"{kind}.schema.json"), str(instance),
                            ], capture_output=True, text=True, check=False)
                            schema_ok &= result.returncode == 0
                    try:
                        findings = validate_catalog(load_catalog(root))
                        python_ok = not any(f.severity == "error" for f in findings)
                    except ValueError:
                        python_ok = False
                    self.assertEqual(python_ok, schema_ok)


if __name__ == "__main__":
    unittest.main()
