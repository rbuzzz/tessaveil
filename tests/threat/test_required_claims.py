"""Guard owner-required public warnings, not a proof of product security.

Missing scenarios, lost negations and translation drift are publication bugs.
These intentionally narrow copy checks supplement human semantic review.
"""

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
         "local NTFS", "removable NTFS", "removable exFAT", "FAT32", "network shares", "cloud-synchronized folders",
         "read-only or Save As to a verified target", "does not prove power-loss durability"),
        ("открытый технический заголовок и аутентифицированный шифротекст", "без открытого содержимого полезной нагрузки",
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
    for claim in (
        r"(?:tessaveil|spin) (?:is |makes .*? )?(?:unbreakable|indistinguishable)",
        r"(?:row|table) (?:updates?|re-randomization) (?:eliminates?|removes?) (?:all )?(?:comparison|intersection|cross-version) risk",
        r"(?:guarantees? secure erasure|guarantees? rollback detection|atomic on all filesystems)",
        r"(?:tessaveil|spin) (?:неуязвим|неразличим)",
        r"(?:обновление|рандомизация) (?:строки|таблицы) устраняет риск",
        r"(?:гарантирует безопасное стирание|гарантирует обнаружение отката|атомарно на всех файловых системах)",
    ):
        if re.search(claim, normalized(text)):
            errors.append(f"overclaim:{claim}")
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


if __name__ == "__main__":
    unittest.main()
