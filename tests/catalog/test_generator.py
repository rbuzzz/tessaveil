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
UNC_GUIDANCE = (
    "//synthetic-host/private-share/backup",
    "Backup: //synthetic-host/private-share/backup",
    "Backup://synthetic-host/private-share/backup",
    'Backup "//synthetic-host/private-share/backup".',
    "Backup (//synthetic-host/private-share/backup).",
    "Backup\n//synthetic-host/private-share/backup",
    r"Backup \\synthetic-host\private-share\backup",
    r"Backup: \\synthetic-host/private-share\backup",
)
WRAPPED_PATHS = (
    "«//synthetic-host/private-share/backup»",
    r'“C:\Synthetic\backup”',
    r'‘\\synthetic-host\private-share\backup’',
    "**/synthetic-vault**", "__/synthetic-vault__", "`/synthetic-vault`",
    "[/synthetic-vault]", "（/synthetic-vault）", "…/synthetic-vault…",
    "Backup:«**//synthetic-host/private-share/backup**»",
    r"Backup=‘__C:\Synthetic\backup__’",
    "[backup](//synthetic-host/private-share/backup)",
    "（https://example.invalid）//synthetic-host/private-share/backup",
    "~~/synthetic-vault~~", r"~~\\synthetic-host\private-share\backup~~", "~~~/synthetic-home~~",
    "~~https://example.invalid/path~~//synthetic-host/private-share/backup",
    "**https://example.invalid/path**/synthetic-vault",
    "__https://example.invalid/path__/synthetic-vault",
    "~https://example.invalid/path~/synthetic-vault",
)
BALANCED_URLS = (
    "https://example.invalid/help/(synthetic)/path",
    "http://example.invalid/search?q=(/help)&next=(nested(one))/end",
    "https://[2001:db8::1]/(synthetic)/path?next=(/help)",
    "https://example.invalid/search?q='/help'&next=(one)/end",
)
VALID_AUTHORITY_URLS = (
    "https://docs.example.invalid/a%20b?next=%2Fhelp#part%31",
    "http://192.0.2.10:8080/%E2%82%AC", "https://[2001:db8::1]:443/a%2Fb",
    "https://EXAMPLE.invalid./(part)/~public?value=100%25",
)
INVALID_AUTHORITY_URLS = (
    "https://example.invalid%ZZ//synthetic-host/private-share",
    "https://example.invalid^//synthetic-host/private-share",
    "https://synthetic-user@example.invalid/path", "https://synthetic-user:public@example.invalid/path",
    "https://example.invalid/bad%", "https://example.invalid/?q=%0G", "https://example.invalid/#part%1",
    "https://%65xample.invalid/path", "https://еxample.invalid/path",  # Cyrillic e, not ASCII DNS.
    "https://example.invalid：443/path", "https://bad_host.invalid/path",
    "https://-bad.invalid/path", "https://bad-.invalid/path", "https://bad..invalid/path",
    "https://999.0.0.1/path", "https://192.0.2.01/path", "https://[2001:db8::1]suffix/path",
    "https://[2001:db8::1%25zone]/path", "https://example.invalid:/path",
    "https://example.invalid:65536/path", "https://example.invalid/path\x00suffix",
    "https:// /path", "https://example.invalid: 443/path", "https://[2001:db8::1 ]/path",
    "https://exam%20ple.invalid/path", "https://[2001:db8::1]:/path",
    "https://exa,mple.invalid/path", "https://exa;mple.invalid/path", "https://exa!mple.invalid/path",
)


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
                    handoff = {"research/subproject-1-verification.md", "../THIRD_PARTY_NOTICES"}
                    self.assertTrue(link.startswith(("../catalog/", "#")) or link in handoff, link)
                    if link in handoff:
                        self.assertTrue((ROOT / "docs" / link).is_file(), link)
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
        modified = replace(wallet, data={**wallet.data, "guidance": "private path C:" + "\\Users" + "\\Synthetic\\vault"})
        with self.assertRaises(ValueError):
            self.render(replace(catalog, wallets=(modified,)))

    def test_single_component_absolute_metadata_path_is_rejected(self):
        catalog = load_catalog(FIXTURE)
        wallet = catalog.wallets[0]
        modified = replace(wallet, data={**wallet.data, "guidance": "private path /synthetic-vault"})
        with self.assertRaises(ValueError):
            self.render(replace(catalog, wallets=(modified,)))

    def test_unc_metadata_in_prose_is_rejected_in_both_locales(self):
        catalog = load_catalog(FIXTURE)
        wallet = catalog.wallets[0]
        for locale in ("en", "ru"):
            for guidance in UNC_GUIDANCE:
                with self.subTest(locale=locale, guidance=guidance):
                    modified = replace(wallet, data={**wallet.data, "guidance": guidance})
                    with self.assertRaises(ValueError):
                        self.render(replace(catalog, wallets=(modified,)), locale)

    def test_normal_https_metadata_remains_renderable_in_both_locales(self):
        catalog = load_catalog(FIXTURE)
        wallet = catalog.wallets[0]
        for locale in ("en", "ru"):
            for url in ("https://example.invalid/backup", "HTTPS://example.invalid:8443/backup",
                        "https://example.invalid/backup?next=/help#restore",
                        "https://[2001:db8::1]/backup"):
                with self.subTest(locale=locale, url=url):
                    modified = replace(wallet, data={**wallet.data, "guidance": f"See ({url}) for official guidance."})
                    output = self.render(replace(catalog, wallets=(modified,)), locale)
                    self.assertIn("for official guidance.", output)
                    self.assertNotIn(url, output)  # Remains escaped, not an autolink.

    def test_wrapped_absolute_paths_are_rejected_in_both_locales(self):
        catalog = load_catalog(FIXTURE)
        wallet = catalog.wallets[0]
        for locale in ("en", "ru"):
            for guidance in WRAPPED_PATHS:
                with self.subTest(locale=locale, guidance=guidance):
                    modified = replace(wallet, data={**wallet.data, "guidance": guidance})
                    with self.assertRaises(ValueError):
                        self.render(replace(catalog, wallets=(modified,)), locale)

    def test_balanced_parentheses_in_http_uris_are_preserved_in_both_locales(self):
        catalog = load_catalog(FIXTURE)
        wallet = catalog.wallets[0]
        for locale in ("en", "ru"):
            for url in BALANCED_URLS:
                with self.subTest(locale=locale, url=url):
                    modified = replace(wallet, data={**wallet.data,
                        "guidance": f"See [official source]({url}) for details."})
                    output = self.render(replace(catalog, wallets=(modified,)), locale)
                    self.assertIn("for details.", output)
                    self.assertIn("example.invalid" if "example.invalid" in url else "2001", output)
                    self.assertIn("\\(", output)

    def test_metadata_scanner_rejects_control_characters_and_excess_size(self):
        catalog = load_catalog(FIXTURE)
        wallet = catalog.wallets[0]
        for guidance in ("https://example.invalid/path\x00suffix", "x" * (16 * 1024 + 1)):
            with self.subTest(case="control" if "\x00" in guidance else "size"):
                modified = replace(wallet, data={**wallet.data, "guidance": guidance})
                with self.assertRaises(ValueError):
                    self.render(replace(catalog, wallets=(modified,)))

    def test_uri_authority_and_invalid_separators_fail_closed(self):
        catalog = load_catalog(FIXTURE)
        wallet = catalog.wallets[0]
        for locale in ("en", "ru"):
            for guidance in ("https:///path", "https://example.invalid:invalid/(one)",
                             "https://example.invalid:65536/(one)",
                             r"https://example.invalid/path\private", "https://example.invalid/path(one"):
                with self.subTest(locale=locale, guidance=guidance):
                    modified = replace(wallet, data={**wallet.data, "guidance": guidance})
                    with self.assertRaises(ValueError):
                        self.render(replace(catalog, wallets=(modified,)), locale)

    def test_strict_authorities_and_percent_escapes_in_both_locales(self):
        catalog = load_catalog(FIXTURE)
        wallet = catalog.wallets[0]
        for locale in ("en", "ru"):
            for url in INVALID_AUTHORITY_URLS:
                with self.subTest(locale=locale, url=url):
                    modified = replace(wallet, data={**wallet.data, "guidance": url})
                    with self.assertRaises(ValueError):
                        self.render(replace(catalog, wallets=(modified,)), locale)
            for url in VALID_AUTHORITY_URLS:
                with self.subTest(locale=locale, url=url):
                    modified = replace(wallet, data={**wallet.data, "guidance": f"See ({url}) for details."})
                    output = self.render(replace(catalog, wallets=(modified,)), locale)
                    self.assertIn("for details.", output)
                    self.assertIn("%", output)

    def test_benign_tildes_render_as_inert_prose_in_both_locales(self):
        catalog = load_catalog(FIXTURE)
        wallet = catalog.wallets[0]
        modified = replace(wallet, data={**wallet.data, "guidance": "About ~5 items; ~~obsolete~~ label."})
        for locale in ("en", "ru"):
            output = self.render(replace(catalog, wallets=(modified,)), locale)
            self.assertIn(r"About \~5 items; \~\~obsolete\~\~ label.", output)

    def test_markdown_wrapped_valid_uri_is_inert_but_not_rejected(self):
        catalog = load_catalog(FIXTURE)
        wallet = catalog.wallets[0]
        for locale in ("en", "ru"):
            for marker in ("*", "**", "***", "_", "__", "___", "~", "~~"):
                with self.subTest(locale=locale, marker=marker):
                    modified = replace(wallet, data={**wallet.data,
                        "guidance": marker + "https://example.invalid/path" + marker})
                    output = self.render(replace(catalog, wallets=(modified,)), locale)
                    self.assertIn("example.invalid/path", output)
                    self.assertNotIn("https://", output)

    def test_sentence_punctuation_after_valid_uri_remains_prose(self):
        catalog = load_catalog(FIXTURE)
        wallet = catalog.wallets[0]
        for locale in ("en", "ru"):
            for punctuation in (",", ";", "!"):
                with self.subTest(locale=locale, punctuation=punctuation):
                    modified = replace(wallet, data={**wallet.data,
                        "guidance": f"See https://example.invalid{punctuation} then read the guidance."})
                    output = self.render(replace(catalog, wallets=(modified,)), locale)
                    self.assertIn("example.invalid", output)
                    self.assertIn("then read the guidance.", output)


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

    def test_unc_guidance_fails_before_any_output_mutation(self):
        for guidance in (UNC_GUIDANCE[1], UNC_GUIDANCE[-2], WRAPPED_PATHS[0]):
            for existing in (False, True):
                with self.subTest(guidance=guidance, existing=existing), tempfile.TemporaryDirectory() as directory:
                    self.root = Path(directory)
                    shutil.copytree(FIXTURE, self.root, dirs_exist_ok=True)
                    docs = self.root / "docs"
                    if existing:
                        docs.mkdir()
                        for name in ("catalog.md", "catalog.ru.md"):
                            (docs / name).write_bytes(b"previous\n")
                    path = self.root / "catalog/wallets/synthetic-wallet.json"
                    data = json.loads(path.read_text(encoding="utf-8"))
                    data["guidance"] = guidance
                    path.write_text(json.dumps(data), encoding="utf-8")

                    def snapshot():
                        return {p.relative_to(self.root): (p.stat().st_mtime_ns,
                                p.read_bytes() if p.is_file() else None)
                                for p in self.root.rglob("*")}

                    before = snapshot()
                    for args in ((), ("--check",)):
                        result = self.cli(*args)
                        self.assertNotEqual(result.returncode, 0)
                        diagnostic = result.stdout + result.stderr
                        self.assertLess(len(diagnostic), 256)
                        self.assertNotIn("synthetic-host", diagnostic)
                        self.assertNotIn(str(self.root), diagnostic)
                        self.assertNotIn("Traceback", diagnostic)
                        self.assertEqual(before, snapshot())

    def test_balanced_url_generates_both_locales_and_check_is_nonmutating(self):
        path = self.root / "catalog/wallets/synthetic-wallet.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        data["guidance"] = f"See ({BALANCED_URLS[0]}) for details."
        path.write_text(json.dumps(data), encoding="utf-8")
        result = self.cli()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        docs = self.root / "docs"
        before = {p.name: (p.read_bytes(), p.stat().st_mtime_ns) for p in docs.iterdir()}
        self.assertEqual(set(before), {"catalog.md", "catalog.ru.md"})
        for content, _ in before.values():
            self.assertIn(b"/\\(synthetic\\)/path", content)
        self.assertEqual(self.cli("--check").returncode, 0)
        self.assertEqual(before, {p.name: (p.read_bytes(), p.stat().st_mtime_ns) for p in docs.iterdir()})

    def test_strike_paths_and_bad_uris_reject_before_publication(self):
        cases = (("~~/synthetic-vault~~", False),
                 (r"~~\\synthetic-host\private-share\backup~~", True),
                 ("~~~/synthetic-home~~", True),
                 (INVALID_AUTHORITY_URLS[0], False), (INVALID_AUTHORITY_URLS[2], True))
        for guidance, existing in cases:
            with self.subTest(guidance=guidance), tempfile.TemporaryDirectory() as directory:
                self.root = Path(directory)
                shutil.copytree(FIXTURE, self.root, dirs_exist_ok=True)
                docs = self.root / "docs"
                if existing:
                    docs.mkdir()
                    for name in ("catalog.md", "catalog.ru.md"):
                        (docs / name).write_bytes(b"previous\n")
                path = self.root / "catalog/wallets/synthetic-wallet.json"
                data = json.loads(path.read_text(encoding="utf-8"))
                data["guidance"] = guidance
                path.write_text(json.dumps(data), encoding="utf-8")

                def snapshot():
                    return {p.relative_to(self.root): (p.stat().st_mtime_ns,
                            p.read_bytes() if p.is_file() else None)
                            for p in self.root.rglob("*")}

                before = snapshot()
                result = self.cli()
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(before, snapshot())
                diagnostic = result.stdout + result.stderr
                self.assertLess(len(diagnostic), 256)
                for forbidden in (guidance, "synthetic-host", "synthetic-user", str(self.root), "Traceback"):
                    self.assertNotIn(forbidden, diagnostic)

    def test_dns_ipv4_ipv6_and_encoded_paths_publish_both_documents(self):
        path = self.root / "catalog/wallets/synthetic-wallet.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        data["guidance"] = " ".join(VALID_AUTHORITY_URLS)
        path.write_text(json.dumps(data), encoding="utf-8")
        result = self.cli()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        for name in ("catalog.md", "catalog.ru.md"):
            output = (self.root / "docs" / name).read_text(encoding="utf-8")
            for fragment in ("192.0.2.10", "2001", "%20", "%2F", "%E2%82%AC", "%25"):
                self.assertIn(fragment, output)
        self.assertEqual(self.cli("--check").returncode, 0)

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
