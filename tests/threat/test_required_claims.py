"""Guard owner-required public warnings, not a proof of product security.

Missing scenarios, lost negations and translation drift are publication bugs.
These intentionally narrow copy checks supplement human semantic review.
"""

from html import unescape
from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[2]
SCENARIOS = {
    "exe": ("executable", "исполняем"),
    "ciphertext": ("ciphertext", "шифротекст"),
    "guessing": ("offline", "офлайн"),
    "master": ("master password", "мастер-парол"),
    "order": ("order key", "ключ порядка"),
    "hostile": ("IME", "IME"),
    "spin": ("Spin", "Spin"),
    "versions": ("different tables", "разные таблицы"),
    "temporary": ("temporary", "временн"),
    "mobile": ("two bits", "двух бит"),
    "password-loss": ("master or sheet password", "мастер-пароля или пароля листа"),
    "source": ("source wallet", "исходного кошелька"),
    "physical": ("physical", "физическ"),
    "rollback": ("rollback", "откат"),
    "filesystem": ("atomic", "атомар"),
}

# Each independently specified clause is required in the matching language.
# Keep negations and objects together: a keyword alone cannot pass these checks.
CLAUSES = {
    "matrix": (
        ("UI delays, attempt counters and self-destruction cannot restrict a copied file",),
        ("Задержки UI, счётчики и самоуничтожение не ограничивают скопированный файл",),
    ),
    "boundary": (
        ("briefly sees the current word and column", "cannot defeat a compromised OS",
         "does not validate complete phrases", "does not replace a separate cold backup or trusted hardware-wallet process",
         "not a second cryptographic boundary", "best effort", "swap", "crash dumps"),
        ("кратковременно видит текущее слово и столбец", "не может противостоять скомпрометированной ОС",
         "не проверяет целые фразы", "не заменяет отдельную холодную резервную копию или доверенную процедуру аппаратного кошелька",
         "не является вторым криптографическим барьером", "по мере возможности", "подкачк", "аварийные дампы"),
    ),
    "spin-contract": (
        ("same UI process", "no explicit validity result", "no success signal", "no target-column output",
         "no saved metadata signal", "visible row contents may differ", "valid input visibly places the requested word",
         "repeated observations and attempts can correlate", "not a proof against observation"),
        ("одинаковый процесс в UI", "нет явного результата допустимости", "нет сигнала успеха",
         "нет вывода целевого столбца", "нет сохранённого признака результата",
         "видимое содержимое строк может различаться", "допустимый ввод явно помещает запрошенное слово",
         "повторные наблюдения и попытки позволяют сопоставлять", "не доказательство защиты от наблюдения"),
    ),
    "copy-contract": (
        ("identical redundant copies", "do not add a new table-comparison signal", "different saved tables",
         "manual copies", "replacement sheets", "interrupted-save remnants",
         "full row or table re-randomization does not remove cross-version intersection risk",
         "no cosmetic reshuffle", "before editing a previously saved row", "best-effort cleanup is not secure erasure"),
        ("идентичные резервные копии", "не добавляют нового сигнала сравнения таблиц", "разные сохранённые таблицы",
         "ручные копии", "заменяющие листы", "остатки прерванного сохранения",
         "полная повторная рандомизация строки или таблицы не устраняет риск пересечения разных версий",
         "косметической перетасовки нет", "перед изменением ранее сохранённой строки",
         "очистка по мере возможности не является гарантированным стиранием"),
    ),
    "dictionary-contract": (
        ("immutable dictionary snapshot", "revised list creates a new unverified sheet",
         "fill and independently verify it again", '"Verified by me" never transfers',
         "table cells, row state and protection state do not transfer", "old sheet stays unchanged until explicit deletion",
         "no automatic phrase-preserving migration"),
        ("неизменяемый снимок словаря", "изменённый список создаёт новый непроверенный лист",
         "заполнить и независимо проверить его заново", '"Verified by me" никогда не переносится',
         "ячейки таблицы, состояние строк и защиты не переносятся", "старый лист остаётся неизменным до явного удаления",
         "автоматического переноса с сохранением фразы нет"),
    ),
    "save-contract": (
        ("clear technical header plus authenticated ciphertext", "no plaintext payload", "no rollback detection",
         "No password attempt limit or self-destruction policy prevents offline guessing of copies.",
         "local NTFS", "removable NTFS", "removable exFAT", "FAT32", "network shares", "cloud-synchronized folders",
         "read-only or Save As to a verified target", "does not prove power-loss durability"),
        ("открытый технический заголовок и аутентифицированный шифротекст", "без открытого содержимого полезной нагрузки",
         "Ограничение попыток пароля или самоуничтожение не предотвращает офлайн-подбор копий.",
         "обнаружение отката не обещается", "локальный NTFS", "съёмный NTFS", "съёмный exFAT", "FAT32",
         "сетевые ресурсы", "папки облачной синхронизации", "только чтение или Save As на проверенный носитель",
         "не доказывает сохранность при потере питания"),
    ),
    "gates": (
        ("research completion does not grant release permission", "Windows release: NO-GO", "format/KDF freeze: NO-GO",
         "physical mobile evidence: blocked", "removable-media guarantees: NO-GO", "not implemented product guarantees"),
        ("завершение исследования не разрешает релиз", "релиз Windows: NO-GO", "фиксация формата/KDF: NO-GO",
         "физические мобильные проверки: blocked", "гарантии съёмных носителей: NO-GO", "не реализованные гарантии продукта"),
    ),
}

README_CLAUSES = (
    ("briefly sees the current word and column", "cannot defeat a compromised OS", "does not validate complete phrases",
     "does not replace a separate cold backup or trusted hardware-wallet process",
     "full row or table re-randomization does not remove cross-version intersection risk", "Windows release remains NO-GO"),
    ("кратковременно видит текущее слово и столбец", "не может противостоять скомпрометированной ОС", "не проверяет целые фразы",
     "не заменяет отдельную холодную резервную копию или доверенную процедуру аппаратного кошелька",
     "полная повторная рандомизация строки или таблицы не устраняет риск пересечения разных версий", "релиз Windows остаётся NO-GO"),
)


def normalized(text):
    return " ".join(text.casefold().split())


def section(text, anchor):
    match = re.search(rf'<!-- {re.escape(anchor)} -->\s*(.*?)(?=<!-- |\Z)', text, re.S)
    return match.group(1) if match else ""


def claim_text(text):
    """Expose ordinary Markdown wording before checking selected overclaims.

    Preserve visible words and whitespace across quote continuations, hard
    breaks and HTML entities, including negative quantifiers such as No/не.
    This is a bounded copy guard, not a complete Markdown or language parser.
    """
    text = re.sub(r"\\\r?\n", "\n", text)
    text = re.sub(r"(?m)^[ \t]*(?:>[ \t]*)+", "", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"<br\b[^>]*>", "\n", text, flags=re.I)
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"[*_`]", "", text)
    return normalized(unescape(text))


def contract_errors(text):
    errors = []
    for index, lang in enumerate(("en", "ru")):
        matrix = section(text, f"{lang}:matrix")
        rows = {}
        for line in matrix.splitlines():
            cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
            if cells and cells[0] in SCENARIOS:
                if cells[0] in rows:
                    errors.append(f"{lang}:duplicate:{cells[0]}")
                rows[cells[0]] = cells
        if set(rows) != set(SCENARIOS):
            errors.append(f"{lang}:scenarios")
        for scenario, cells in rows.items():
            # ID, scenario, asset, attacker, protection, limitation, mitigation,
            # residual risk, user guidance: none may be an empty placeholder.
            if len(cells) != 9 or any(len(cell) < 8 for cell in cells[1:]):
                errors.append(f"{lang}:incomplete:{scenario}")
            if normalized(SCENARIOS[scenario][index]) not in normalized(" ".join(cells)):
                errors.append(f"{lang}:topic:{scenario}")
        for contract, translations in CLAUSES.items():
            body = normalized(section(text, f"{lang}:{contract}"))
            for clause in translations[index]:
                if normalized(clause) not in body:
                    errors.append(f"{lang}:{contract}:{clause}")
    # Reject common positive overclaims even if warnings elsewhere remain intact.
    visible = claim_text(text)
    for claim in (
        r"(?:tessaveil|spin) (?:is |makes .*? )?(?:unbreakable|indistinguishable)",
        r"(?:row|table) (?:updates?|re-randomization) (?:eliminates?|removes?) (?:all )?(?:comparison|intersection|cross-version) risk",
        r"(?:guarantees? secure erasure|guarantees? rollback detection|atomic on all filesystems)",
        r"(?:tessaveil|spin) (?:неуязвим|неразличим)",
        r"(?:обновление|рандомизация) (?:строки|таблицы) устраняет риск",
        r"(?:гарантирует безопасное стирание|гарантирует обнаружение отката|атомарно на всех файловых системах)",
        r"(?:password attempt limits? (?:or|and) self-destruction(?: policy)?|"
        r"(?:ui delays, )?attempt counters(?: and self-destruction)?|self-destruction(?: policy)?) "
        r"(?:prevents? offline guessing of copies|protects? copied ciphertext from offline guessing|can restrict a copied file)",
        r"самоуничтожение (?:предотвращает офлайн-подбор копий|ограничивают скопированный файл|"
        r"защищает скопированный шифротекст от офлайн-подбора)",
        r"счётчики попыток защищают скопированный шифротекст от офлайн-подбора",
    ):
        for match in re.finditer(claim, visible):
            # Match the whole subject, including its alternatives, so a skipped
            # "No password ... or self-destruction ..." cannot be rematched as
            # a positive claim starting halfway through that same subject.
            # Other valid negatives (cannot, do not, не) do not match the
            # adjacent positive subject/verb patterns in the first place.
            if re.search(r"\b(?:no|not)\s+$", visible[:match.start()]):
                continue
            errors.append(f"overclaim:{claim}")
            break
    return errors


class RequiredClaimsTests(unittest.TestCase):
    def read_model(self):
        path = ROOT / "THREAT_MODEL.md"
        self.assertTrue(path.is_file(), "Public threat model is missing")
        return path.read_text(encoding="utf-8")

    def test_bilingual_matrix_and_warning_contracts(self):
        self.assertEqual([], contract_errors(self.read_model()))

    def test_each_required_clause_is_enforced_in_its_own_language(self):
        text = self.read_model()
        for index, lang in enumerate(("en", "ru")):
            for contract, translations in CLAUSES.items():
                for clause in translations[index]:
                    with self.subTest(lang=lang, contract=contract, clause=clause):
                        body = section(text, f"{lang}:{contract}")
                        changed = re.sub(re.escape(clause), "[warning omitted]", body, flags=re.I)
                        self.assertNotEqual(body, changed)
                        self.assertTrue(contract_errors(text.replace(body, changed)))

    def test_matrix_omission_empty_capability_and_duplicate_are_rejected(self):
        text = self.read_model()
        for lang in ("en", "ru"):
            for scenario in SCENARIOS:
                with self.subTest(lang=lang, scenario=scenario):
                    body = section(text, f"{lang}:matrix")
                    row = next(line for line in body.splitlines() if line.startswith(f"| {scenario} |"))
                    for changed in (body.replace(row, ""), body.replace(row, row + "\n" + row)):
                        self.assertTrue(contract_errors(text.replace(body, changed)))
                    cells = row.split("|")
                    cells[4] = " "  # attacker capability, not merely scenario label
                    self.assertTrue(contract_errors(text.replace(body, body.replace(row, "|".join(cells)))))

    def test_positive_security_overclaims_fail_even_with_all_warnings_present(self):
        text = self.read_model()
        for claim in ("Tessaveil is unbreakable.", "Spin is indistinguishable.",
                      "Row updates remove cross-version risk.", "Table re-randomization eliminates intersection risk.",
                      "Tessaveil guarantees secure erasure.", "Atomic on all filesystems.",
                      "Tessaveil неуязвим.", "Обновление строки устраняет риск.",
                      "Tessaveil гарантирует обнаружение отката."):
            with self.subTest(claim=claim):
                self.assertTrue(contract_errors(text + "\n" + claim))

    def test_readme_parity_and_public_model_link(self):
        for index, name in enumerate(("README.md", "README.ru.md")):
            text = (ROOT / name).read_text(encoding="utf-8")
            with self.subTest(name=name):
                self.assertRegex(text, r"\[[^\]]+\]\(THREAT_MODEL\.md(?:#[^)]+)?\)")
                for clause in README_CLAUSES[index]:
                    self.assertIn(normalized(clause), normalized(text))

    def test_offline_copy_limits_reject_deletion_and_bilingual_inversion(self):
        text = self.read_model()
        changes = (
            ("en:save-contract",
             "No password attempt limit or self-destruction policy prevents offline guessing of copies.",
             "Password attempt limit or self-destruction policy prevents offline guessing of copies."),
            ("ru:save-contract",
             "Ограничение попыток пароля или самоуничтожение не предотвращает офлайн-подбор копий.",
             "Ограничение попыток пароля или самоуничтожение предотвращает офлайн-подбор копий."),
            ("en:matrix",
             "UI delays, attempt counters and self-destruction cannot restrict a copied file",
             "UI delays, attempt counters and self-destruction can restrict a copied file"),
            ("ru:matrix",
             "Задержки UI, счётчики и самоуничтожение не ограничивают скопированный файл",
             "Задержки UI, счётчики и самоуничтожение ограничивают скопированный файл"),
        )
        inverted = text
        for anchor, warning, overclaim in changes:
            inverted = inverted.replace(warning, overclaim)
            with self.subTest(anchor=anchor):
                self.assertIn(warning, section(text, anchor))
                for replacement in ("[limitation omitted]", overclaim):
                    errors = contract_errors(text.replace(warning, replacement))
                    self.assertTrue(any(error.startswith(anchor + ":") for error in errors))
        # The review reproduction changes both languages and both locations.
        # Assert language-local failures, not just disappearance of a topic token.
        errors = contract_errors(inverted)
        for anchor, _, _ in changes:
            with self.subTest(simultaneous_inversion=anchor):
                self.assertTrue(any(error.startswith(anchor + ":") for error in errors))

    def test_offline_copy_overclaims_fail_with_original_warnings_intact(self):
        text = self.read_model()
        for claim in (
            "Password attempt limit or self-destruction policy prevents offline guessing of copies.",
            "Password attempt limits and self-destruction prevent offline guessing of copies.",
            "UI delays, attempt counters and self-destruction can restrict a copied file.",
            "Attempt counters protect copied ciphertext from offline guessing.",
            "Self-destruction protects copied ciphertext from offline guessing.",
            "Ограничение попыток пароля или самоуничтожение предотвращает офлайн-подбор копий.",
            "Задержки UI, счётчики и самоуничтожение ограничивают скопированный файл.",
            "Счётчики попыток защищают скопированный шифротекст от офлайн-подбора.",
            "Самоуничтожение защищает скопированный шифротекст от офлайн-подбора.",
        ):
            with self.subTest(claim=claim):
                errors = contract_errors(text + "\n" + claim)
                self.assertTrue(any(error.startswith("overclaim:") for error in errors))

    def test_offline_copy_overclaims_survive_markdown_and_cell_separators(self):
        text = self.read_model()
        claims = (
            "Attempt counters protect copied ciphertext from offline guessing.",
            "Password attempt limit or self-destruction policy prevents offline guessing of copies.",
            "Самоуничтожение защищает скопированный шифротекст от офлайн-подбора.",
        )
        for claim in claims:
            for wrapper in ("- {}", "1. {}", "**{}**", "__{}__", "> {}", "> - **{}**",
                            "`{}`", "Advice: {}", "Existing statement; {}", "[{}](#offline)"):
                with self.subTest(claim=claim, wrapper=wrapper):
                    errors = contract_errors(text + "\n" + wrapper.format(claim))
                    self.assertTrue(any(error.startswith("overclaim:") for error in errors))
        for claim in (
            "**Attempt counters** protect copied ciphertext from offline guessing.",
            "Attempt counters **protect** copied ciphertext from offline guessing.",
            "Attempt counters\nprotect copied ciphertext from offline guessing.",
            "[Attempt counters](#offline) protect copied ciphertext from offline guessing.",
            "<strong>Attempt counters</strong> protect copied ciphertext from offline guessing.",
            "**Самоуничтожение** защищает скопированный шифротекст от офлайн-подбора.",
        ):
            with self.subTest(inline_markup=claim):
                self.assertTrue(any(error.startswith("overclaim:")
                                    for error in contract_errors(text + "\n" + claim)))
        protection = "Argon2id is intended to raise cost per guess"
        self.assertIn(protection, text)
        for claim in claims:
            with self.subTest(semicolon_in_guessing_cell=claim):
                changed = text.replace(protection, protection + "; " + claim)
                self.assertTrue(any(error.startswith("overclaim:") for error in contract_errors(changed)))

    def test_offline_copy_negative_warnings_remain_accepted_with_markdown(self):
        text = self.read_model()
        for warning in (
            "No password attempt limit or self-destruction policy prevents offline guessing of copies.",
            "**No** password attempt limit or self-destruction policy prevents offline guessing of copies.",
            "No **password attempt limit or self-destruction policy** prevents offline guessing of copies.",
            "Attempt counters do not protect copied ciphertext from offline guessing.",
            "UI delays, attempt counters and self-destruction cannot restrict a copied file.",
            "Ограничение попыток пароля или самоуничтожение не предотвращает офлайн-подбор копий.",
            "Самоуничтожение **не** защищает скопированный шифротекст от офлайн-подбора.",
            "Счётчики попыток не защищают скопированный шифротекст от офлайн-подбора.",
        ):
            for wrapper in ("- {}", "> **{}**", "Existing statement; {}"):
                with self.subTest(warning=warning, wrapper=wrapper):
                    self.assertEqual([], contract_errors(text + "\n" + wrapper.format(warning)))

    def test_visible_breaks_preserve_positive_and_negative_claim_polarity(self):
        text = self.read_model()
        cases = (
            ("Attempt counters", "protect copied ciphertext from offline guessing.", True),
            ("Самоуничтожение", "защищает скопированный шифротекст от офлайн-подбора.", True),
            ("No", "password attempt limit or self-destruction policy prevents offline guessing of copies.", False),
            ("Самоуничтожение не", "защищает скопированный шифротекст от офлайн-подбора.", False),
        )
        for head, tail, overclaim in cases:
            for separator in ("\n> ", "\n> > ", "<br>", "<br/>", "<BR />", "&nbsp;",
                              "&#160;", "&#xA0;", "\\\n", "\\\r\n", "  \n"):
                with self.subTest(head=head, separator=separator):
                    rendered = "> " + head + separator + tail
                    # Literal unformatted wording is the independent expectation.
                    # In particular, normalization must not lose No/не or join words.
                    self.assertEqual((head + " " + tail).casefold(), claim_text(rendered))
                    errors = contract_errors(text + "\n" + rendered)
                    if overclaim:
                        self.assertTrue(any(error.startswith("overclaim:") for error in errors))
                    else:
                        self.assertEqual([], errors)

    def test_composed_quote_break_entity_and_negation_cases(self):
        text = self.read_model()
        cases = (
            ("> **Attempt counters**\\\n> protect&nbsp;copied ciphertext from offline guessing.", True),
            ("> **Самоуничтожение**<br>защищает&#160;скопированный шифротекст от офлайн-подбора.", True),
            ("> **No**\\\n> password&nbsp;attempt limit or self-destruction policy prevents offline guessing of copies.", False),
            ("> Самоуничтожение **не**<br>защищает&nbsp;скопированный шифротекст от офлайн-подбора.", False),
        )
        for rendered, overclaim in cases:
            with self.subTest(rendered=rendered):
                errors = contract_errors(text + "\n" + rendered)
                if overclaim:
                    self.assertTrue(any(error.startswith("overclaim:") for error in errors))
                else:
                    self.assertEqual([], errors)


if __name__ == "__main__":
    unittest.main()
