"""Adversarial distribution verification against actual gate-produced archives.

Run by gate.ps1 after full build/relink. Archive reads alone are replaced with
mutated copies; no schema, source, manifest, license or evidence check is mocked.
Ordinary repository tests cannot build a Windows Qt archive and skip this case.
"""
import copy
import json
import os
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "packaging/windows"))
import alpha
import candidate_manifest


class WindowsAlphaDistributionTests(unittest.TestCase):
    @unittest.skipUnless(os.environ.get("TESSAVEIL_ALPHA_AUDIT_ROOT"), "requires gate-produced Windows archives")
    def test_distribution_rejects_rechecksummed_sbom_and_observation_substitution(self):
        import verify
        output = Path(os.environ["TESSAVEIL_ALPHA_AUDIT_ROOT"])
        source_sha = os.environ["TESSAVEIL_CANDIDATE_SHA"]
        paths = candidate_manifest.paths(output, source_sha)
        runtime_path, compliance_path = paths["runtime"], paths["compliance"]
        runtime, compliance = alpha.read_archive(runtime_path), alpha.read_archive(compliance_path)
        sha = runtime["SOURCE_SHA"].decode().strip()
        original = json.loads(runtime["sbom.cdx.json"])
        mutations = [("empty SBOM", "sbom.cdx.json", {"bomFormat": "CycloneDX", "specVersion": "1.6", "version": 1}, "SBOM")]
        # Cover each independently reconstructed inventory family, not one count.
        for prefix in ("pkg:cargo/", "rust-runtime:", "qt-source:", "qtbase", "bip39-en", "rust-std", "llvm-mingw-runtime", "windows:"):
            changed = copy.deepcopy(original)
            removed = next(c for c in changed["components"] if c["bom-ref"].startswith(prefix))
            changed["components"].remove(removed)
            mutations.append(("missing " + prefix, "sbom.cdx.json", changed, "SBOM"))
        for key, replacement in (("version", "999.0.0"), ("licenses", [{"expression": "GPL-3.0-only"}]),
                                 ("hashes", [{"alg": "SHA-256", "content": "f" * 64}]), ("bom-ref", "substituted")):
            changed = copy.deepcopy(original)
            changed["components"][0][key] = replacement
            mutations.append(("wrong " + key, "sbom.cdx.json", changed, "SBOM"))
        for label in ("missing graph", "missing root refs", "invalid reference", "stale application"):
            changed = copy.deepcopy(original)
            if label == "missing graph":
                changed["dependencies"] = []
            elif label == "stale application":
                changed["metadata"]["component"]["version"] = "f" * 40
            else:
                next(n for n in changed["dependencies"] if n["ref"] == "Tessaveil")["dependsOn"] = [] if label == "missing root refs" else ["missing"]
            mutations.append((label, "sbom.cdx.json", changed, "SBOM"))
        observed = json.loads(runtime["runtime-observation.json"])
        mutations.append(("empty observation", "runtime-observation.json", {}, "observation"))
        for key in ("all_five_password_controls_masked", "keyboard_focus_observed", "open_close_reopen_lock", "authentication_safe"):
            for missing in (True, False):
                changed = copy.deepcopy(observed)
                if missing:
                    del changed[key]
                else:
                    changed[key] = False
                mutations.append((key + str(missing), "runtime-observation.json", changed, "observation"))
        for key, value in (("source_sha", "f" * 40), ("exe_sha256", "f" * 64), ("password_observations", [])):
            mutations.append(("stale/malformed " + key, "runtime-observation.json", dict(observed, **{key: value}), "observation"))
        for label, name, value, error in mutations:
            modified = dict(runtime)
            modified[name] = json.dumps(value).encode()
            modified.pop("SHA256SUMS")
            modified["SHA256SUMS"] = alpha.make_manifest(modified)
            with self.subTest(mutation=label), patch.object(alpha, "read_archive", side_effect=lambda path: modified if path == runtime_path else compliance):
                with self.assertRaisesRegex(ValueError, error):
                    verify.verify(
                        runtime_path,
                        compliance_path,
                        sha,
                        distribution=True,
                        decision_path=paths["decision"],
                        manifest_path=paths["manifest"],
                    )
