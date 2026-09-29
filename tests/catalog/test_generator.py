"""Rendered metadata and fail-closed document publication contracts."""

from dataclasses import replace
import importlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from tools.catalog.loader import load_catalog


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = Path(__file__).parent / "fixtures" / "valid-minimal"


class GeneratorTests(unittest.TestCase):
    def render(self, catalog, locale="en"):
        try:
            generator = importlib.import_module("tools.catalog.generator")
        except ModuleNotFoundError:
            self.fail("render_catalog is not implemented")
        return generator.render_catalog(catalog, locale)

    def test_stable_order_and_shared_dictionary_details(self):
        catalog = load_catalog(FIXTURE)
        another = replace(catalog.schemes[-1], id="aaa-shared", data={
            **catalog.schemes[-1].data, "id": "aaa-shared"})
        evidence = replace(catalog.evidence[0], data={**catalog.evidence[0].data,
            "record_ids": (*catalog.evidence[0].data["record_ids"], "aaa-shared")})
        catalog = replace(catalog, schemes=(*catalog.schemes, another), evidence=(evidence,))
        first = self.render(catalog)
        second = self.render(replace(catalog, schemes=tuple(reversed(catalog.schemes)),
                                    dictionaries=tuple(reversed(catalog.dictionaries))))
        self.assertEqual(first, second)
        self.assertEqual(first, self.render(catalog))
        self.assertEqual(first.count('id="dictionary-synthetic-en"'), 1)
        self.assertLess(first.index('id="scheme-aaa-shared"'),
                        first.index('id="scheme-synthetic-scheme"'))
        self.assertIn("[synthetic-en](#dictionary-synthetic-en)", first)

    def test_bilingual_metadata_and_relative_links_without_word_contents(self):
        catalog = load_catalog(FIXTURE)
        for locale, title in (("en", "Synthetic Wallet"), ("ru", "Синтетический кошелёк")):
            with self.subTest(locale=locale):
                output = self.render(catalog, locale)
                for value in (title, "synthetic-network", "1.0", "2026-09-29", "CC0-1.0",
                              "fixture-v1", "allowed", "compatible", "no-mnemonic-confirmed",
                              "blocked", "NFKD", "12", "36", "false",
                              "Synthetic fixture only; no real wallet compatibility."):
                    self.assertIn(value, output)
                self.assertIn("../catalog/evidence/synthetic-evidence.json", output)
                self.assertNotIn(str(catalog.root), output)
                self.assertNotIn("wordlist_bytes", output)
                for word in catalog.dictionaries[1].wordlist_bytes.decode().splitlines():
                    self.assertNotIn(word, output)
                for link in re.findall(r"\]\(([^)]+)\)", output):
                    self.assertTrue(link.startswith(("../catalog/", "#")), link)
                self.assertNotIn("\r", output)
                self.assertTrue(output.endswith("\n"))
        self.assertIn("Generated", self.render(catalog))
        self.assertIn("use the wallet's own backup procedure", self.render(catalog))
        self.assertIn("резервного копирования самого кошелька", self.render(catalog, "ru"))

    def test_pending_requirements_remain_visible_without_support_claim(self):
        catalog = load_catalog(FIXTURE)
        required = catalog.required_sets[0]
        item = required.requirements[0]
        data = {**item.data, "research_state": "pending", "status": None, "record_ids": ()}
        required = replace(required, requirements=(replace(item, data=data),),
                           data={**required.data, "requirements": (data,)})
        output = self.render(replace(catalog, required_sets=(required,)))
        self.assertIn("dictionary-synthetic-en", output)
        self.assertIn("pending", output)
        self.assertIn("NO-GO", output)

    def test_invalid_locale_and_invalid_catalog_fail_closed(self):
        catalog = load_catalog(FIXTURE)
        with self.assertRaises(ValueError):
            self.render(catalog, "de")
        with self.assertRaises(ValueError):
            self.render(replace(catalog, evidence=()))

    def test_untrusted_markdown_is_text_and_absolute_metadata_is_rejected(self):
        catalog = load_catalog(FIXTURE)
        wallet = catalog.wallets[0]
        modified = replace(wallet, data={**wallet.data, "guidance": "[remote](https://example.invalid) | <img>\r\nnext"})
        output = self.render(replace(catalog, wallets=(modified,)))
        self.assertNotIn("<img>", output)
        self.assertNotIn("[remote](https://", output)
        self.assertNotIn("https://", output)  # No implicit external autolinks either.
        self.assertNotIn("\r", output)
        modified = replace(wallet, data={**wallet.data, "guidance": "private path C:\\Users\\Synthetic\\vault"})
        with self.assertRaises(ValueError):
            self.render(replace(catalog, wallets=(modified,)))

    def test_single_component_absolute_metadata_path_is_rejected(self):
        catalog = load_catalog(FIXTURE)
        wallet = catalog.wallets[0]
        modified = replace(wallet, data={**wallet.data, "guidance": "private path /synthetic-vault"})
        with self.assertRaises(ValueError):
            self.render(replace(catalog, wallets=(modified,)))


class GenerationCliTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        shutil.copytree(FIXTURE, self.root, dirs_exist_ok=True)

    def cli(self, *args):
        return subprocess.run([sys.executable, "-m", "tools.catalog.cli", "generate",
                               "--root", str(self.root), *args], cwd=ROOT,
                              capture_output=True, text=True, encoding="utf-8", check=False)

    def test_generate_check_drift_and_missing_are_nonmutating(self):
        self.assertNotEqual(self.cli("--check").returncode, 0)
        self.assertFalse((self.root / "docs").exists())
        result = self.cli()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        paths = [self.root / "docs" / name for name in ("catalog.md", "catalog.ru.md")]
        original = [path.read_bytes() for path in paths]
        self.assertEqual(self.cli("--check").returncode, 0)
        self.assertEqual(self.cli().returncode, 0)
        self.assertEqual(original, [path.read_bytes() for path in paths])
        paths[1].write_bytes(original[1] + b"drift\n")
        before = [(path.read_bytes(), path.stat().st_mtime_ns) for path in paths]
        self.assertNotEqual(self.cli("--check").returncode, 0)
        self.assertEqual(before, [(path.read_bytes(), path.stat().st_mtime_ns) for path in paths])

    def test_invalid_input_leaves_both_existing_documents_untouched(self):
        docs = self.root / "docs"
        docs.mkdir()
        for name in ("catalog.md", "catalog.ru.md"):
            (docs / name).write_bytes(b"previous\n")
        path = self.root / "catalog/wallets/synthetic-wallet.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        data["scheme_id"] = "missing-scheme"
        path.write_text(json.dumps(data), encoding="utf-8")
        for args in ((), ("--check",)):
            result = self.cli(*args)
            self.assertNotEqual(result.returncode, 0)
            self.assertNotIn("Traceback", result.stderr)
            self.assertNotIn(str(self.root), result.stdout + result.stderr)
            for name in ("catalog.md", "catalog.ru.md"):
                self.assertEqual((docs / name).read_bytes(), b"previous\n")

    def test_second_output_obstruction_does_not_replace_first(self):
        docs = self.root / "docs"
        docs.mkdir()
        (docs / "catalog.md").write_bytes(b"previous\n")
        (docs / "catalog.ru.md").mkdir()
        result = self.cli()
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn("Traceback", result.stderr)
        self.assertEqual((docs / "catalog.md").read_bytes(), b"previous\n")

    def test_existing_generation_marker_blocks_writing_and_read_only_check(self):
        docs = self.root / "docs"
        docs.mkdir()
        (docs / ".catalog-generation.lock").mkdir()
        for args in ((), ("--check",)):
            result = self.cli(*args)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual([p.name for p in docs.iterdir()], [".catalog-generation.lock"])

    def test_locale_render_failure_never_publishes_either_language(self):
        from tools.catalog import cli
        from tools.catalog.generator import render_catalog

        def fail_ru(catalog, locale):
            if locale == "ru":
                raise ValueError("synthetic locale failure")
            return render_catalog(catalog, locale)

        with patch("tools.catalog.cli.render_catalog", side_effect=fail_ru):
            self.assertNotEqual(cli._generate(load_catalog(self.root), False), 0)
        self.assertFalse((self.root / "docs").exists())

    def test_rollback_failure_keeps_recovery_marker_and_check_fails_closed(self):
        from tools.catalog import cli
        docs = self.root / "docs"
        docs.mkdir()
        for name in ("catalog.md", "catalog.ru.md"):
            (docs / name).write_bytes(b"previous\n")
        import os
        real_replace = os.replace
        calls = 0

        def fail_after_first(source, target):
            nonlocal calls
            calls += 1
            if calls >= 2:
                raise OSError("synthetic persistent IO failure")
            return real_replace(source, target)

        with patch("os.replace", side_effect=fail_after_first):
            self.assertNotEqual(cli._generate(load_catalog(self.root), False), 0)
        self.assertTrue((docs / ".catalog-generation.lock").is_dir())
        stages = list(docs.glob(".catalog-stage-*"))
        self.assertEqual(len(stages), 1)
        self.assertEqual((stages[0] / "old-0").read_bytes(), b"previous\n")
        before = {p.relative_to(docs): p.read_bytes() for p in docs.rglob("*") if p.is_file()}
        self.assertNotEqual(self.cli("--check").returncode, 0)
        self.assertEqual(before, {p.relative_to(docs): p.read_bytes() for p in docs.rglob("*") if p.is_file()})

    def test_second_replace_failure_rolls_back_pair(self):
        from tools.catalog import cli
        docs = self.root / "docs"
        docs.mkdir()
        for name in ("catalog.md", "catalog.ru.md"):
            (docs / name).write_bytes(b"previous\n")
        import os
        real_replace = os.replace
        calls = 0

        def fail_second(source, target):
            nonlocal calls
            calls += 1
            if calls == 2:
                raise OSError("synthetic replacement failure")
            return real_replace(source, target)

        with patch("os.replace", side_effect=fail_second):
            try:
                result = cli.main(["generate", "--root", str(self.root)])
            except SystemExit:
                self.fail("generate must accept calls without --check")
            self.assertNotEqual(result, 0)
        self.assertGreaterEqual(calls, 2)
        for name in ("catalog.md", "catalog.ru.md"):
            self.assertEqual((docs / name).read_bytes(), b"previous\n")
        self.assertEqual(sorted(path.name for path in docs.iterdir()), ["catalog.md", "catalog.ru.md"])


if __name__ == "__main__":
    unittest.main()
