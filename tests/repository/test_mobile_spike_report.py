"""Repository contracts only: these tests do not execute Rust or mobile code."""
import json
from pathlib import Path
import tomllib
import unicodedata
import unittest

ROOT = Path(__file__).resolve().parents[2]
MOBILE = ROOT / "spikes/mobile"


class MobileSpikeTests(unittest.TestCase):
    def read_json(self, name):
        path = MOBILE / name
        self.assertTrue(path.is_file(), f"missing contract: {name}")
        return json.loads(path.read_text(encoding="utf-8"))

    def test_normalization_vectors_have_independent_expected_bytes(self):
        vectors = self.read_json("vectors/password-normalization.json")
        self.assertEqual(vectors["authority"], "Rust NFC UTF-8")
        by_id = {row["id"]: row for row in vectors["cases"]}
        self.assertEqual(len(by_id), len(vectors["cases"]))
        for name in ("composed", "decomposed", "combining", "cyrillic", "japanese", "non-bmp", "empty", "nul"):
            self.assertIn(name, by_id)
        for row in vectors["cases"]:
            with self.subTest(case=row["id"]):
                raw = bytes.fromhex(row["input_utf8_hex"])
                value = raw.decode("utf-8")
                if "\0" in value:
                    self.assertEqual(row["error"], "EmbeddedNul")
                    self.assertNotIn("nfc_utf8_hex", row)
                else:
                    # Independent fixture-data check, never a product normalization path.
                    self.assertEqual(unicodedata.normalize("NFC", value).encode().hex(), row["nfc_utf8_hex"])
        self.assertEqual(by_id["composed"]["nfc_utf8_hex"], by_id["decomposed"]["nfc_utf8_hex"])

    def test_absent_binary_is_blocked_not_a_fake_crypto_success(self):
        fixture = self.read_json("vectors/fixture-status.json")
        self.assertEqual(fixture["status"], "BLOCKED")
        self.assertFalse((MOBILE / "vectors/synthetic-vault-v0.bin").exists())
        self.assertIsNone(fixture["sha256"])
        self.assertFalse(fixture["rust_execution_verified"])
        self.assertFalse(fixture["independent_crypto_verified"])
        self.assertIn("Rust/Cargo", fixture["blocker"])

    def test_dependency_contract_is_exact_and_not_a_claim_of_locked_build(self):
        path = MOBILE / "core/Cargo.toml"
        self.assertTrue(path.is_file(), "Rust Cargo contract absent")
        manifest = tomllib.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(set(manifest["dependencies"]), {"argon2", "chacha20poly1305", "unicode-normalization", "zeroize"})
        for dep in manifest["dependencies"].values():
            version = dep if isinstance(dep, str) else dep["version"]
            self.assertRegex(version, r"^=\d+\.\d+\.\d+$")
        self.assertEqual(set(manifest["lib"]["crate-type"]), {"rlib", "staticlib", "cdylib"})

    def test_physical_evidence_cannot_clear_freeze(self):
        evidence = self.read_json("evidence-status.json")
        self.assertEqual(evidence["format_freeze"], "NO-GO")
        self.assertEqual(evidence["kdf_freeze"], "NO-GO")
        self.assertEqual(evidence["candidate_profiles"], [[65536, 3, 4]])
        equipment = (ROOT / "reports/spikes/equipment-availability.md").read_text(encoding="utf-8")
        expected = {"physical arm64 Android 4 GiB lower-bound", "current mid-range physical Android", "physical iPhone 11/A13/4 GiB-class lower-bound", "current physical iPhone", "Mac/Xcode host"}
        self.assertEqual({row["class"] for row in evidence["targets"]}, expected)
        for row in evidence["targets"]:
            with self.subTest(target=row["class"]):
                self.assertEqual(row["status"], "BLOCKED")
                equipment_row = next(line for line in equipment.splitlines() if line.startswith("| " + row["class"] + " |"))
                self.assertEqual(row["blocker"], equipment_row.split("|")[6].strip())
                for field in ("model", "os", "duration_us", "peak_memory_bytes", "oom", "thermal", "normalization_match"):
                    self.assertIsNone(row[field], field)
        for name in ("reports/spikes/mobile-kdf.md", "docs/adr/0002-kdf-envelope-bounds.md"):
            path = ROOT / name
            self.assertTrue(path.is_file(), f"missing decision: {name}")
            text = path.read_text(encoding="utf-8")
            self.assertIn("NO-GO", text)
            self.assertIn("owner/security", text)
            for row in evidence["targets"]:
                self.assertIn(row["blocker"], text)


if __name__ == "__main__":
    unittest.main()
