"""Deterministic, offline catalogue metadata; never render word-list payloads."""

import html
import ipaddress
from pathlib import PurePosixPath, PureWindowsPath
import string
from typing import Literal
import unicodedata
from urllib.parse import quote, urlsplit

from .loader import DEFAULT_LIMITS
from .model import Catalog, Record
from .validator import validate_catalog


def _validate_uri(uri: str) -> None:
    """Strict ASCII HTTP(S) URI grammar; no decoding, DNS or network lookup.

    International hostnames must use ASCII DNS form, and non-ASCII path/query
    bytes must be percent-encoded. Userinfo and scoped IPv6 are not public
    catalogue provenance. Only complete percent escapes qualify as URI syntax.
    """
    allowed = string.ascii_letters + string.digits + "-._~:/?#[]@!$&'()*+,;=%"
    if any(char not in allowed for char in uri):
        raise ValueError("invalid URI character in rendered metadata")
    for index, char in enumerate(uri):
        if char == "%" and (len(uri[index + 1:index + 3]) != 2 or
                            any(c not in string.hexdigits for c in uri[index + 1:index + 3])):
            raise ValueError("invalid URI percent escape in rendered metadata")
    url = urlsplit(uri)
    authority = url.netloc
    if url.scheme.lower() not in ("http", "https") or not authority or any(c in authority for c in "@%"):
        raise ValueError("invalid URI authority in rendered metadata")
    if authority.startswith("["):
        host, closer, tail = authority[1:].partition("]")
        if not closer or (tail and not tail.startswith(":")):
            raise ValueError("invalid IPv6 authority in rendered metadata")
        ipaddress.IPv6Address(host)
        port_present, port = bool(tail), tail[1:]
    else:
        host, separator, port = authority.partition(":")
        port_present = bool(separator)
        if not host or "[" in host or "]" in host:
            raise ValueError("invalid URI host in rendered metadata")
        if all(c in string.digits + "." for c in host):
            ipaddress.IPv4Address(host)
        else:
            dns = host[:-1] if host.endswith(".") else host
            alphanumeric = string.ascii_letters + string.digits
            if not dns or len(dns) > 253 or any(
                    not label or len(label) > 63 or label[0] not in alphanumeric or
                    label[-1] not in alphanumeric or any(c not in alphanumeric + "-" for c in label)
                    for label in dns.split(".")):
                raise ValueError("invalid DNS host in rendered metadata")
    if port_present and (not port or len(port) > 5 or
                         any(c not in string.digits for c in port) or int(port) > 65535):
        raise ValueError("invalid URI port in rendered metadata")


def _uri_end(value: str, start: int) -> int:
    """Consume one URI, retaining balanced path/query parentheses and IPv6.

    Unmatched outer closers belong to prose/Markdown. Quotes, whitespace and
    markup delimiters end the URI; backslashes and malformed authority reject.
    The caller bounds the entire string; each character is scanned at most once.
    """
    end = start
    closers = []
    single_quoted = start > 0 and value[start - 1] == "'"
    marker = next((m for m in ("***", "___", "**", "__", "~~", "*", "_", "~")
                   if value[max(0, start - len(m)):start] == m), None)
    while end < len(value):
        char = value[end]
        if marker and not closers and value.startswith(marker, end):
            # An intraword underscore is URI content, not closing emphasis.
            after = value[end + len(marker):end + len(marker) + 1]
            if "_" not in marker or not after.isalnum():
                break
        if (char.isspace() or char in '<>"`{}' or
                (single_quoted and char == "'") or
                (unicodedata.category(char) in ("Pi", "Pf", "Ps", "Pe") and char not in "()[]")):
            break
        if char == "\\":
            raise ValueError("invalid URL in rendered metadata")
        if char in "([":
            closers.append(")" if char == "(" else "]")
        elif char in ")]":
            if not closers:
                break
            if char != closers.pop():
                raise ValueError("unbalanced URL in rendered metadata")
        end += 1
    if closers:
        raise ValueError("unbalanced URL in rendered metadata")
    # Sentence punctuation at a span boundary belongs to prose. Internal
    # punctuation still passes through the strict authority/escape grammar.
    while end > start and value[end - 1] in ",;!":
        end -= 1
    _validate_uri(value[start:end])
    return end


def _check_metadata(value: str) -> None:
    """Bounded offline scanner: isolate complete URIs, then inspect prose paths."""
    if len(value.encode("utf-8")) > DEFAULT_LIMITS.max_string_bytes:
        raise ValueError("rendered metadata exceeds limit")
    if any(unicodedata.category(c).startswith("C") and c not in "\r\n\t" for c in value):
        raise ValueError("control character in rendered metadata")

    def check_candidate(chars):
        token = "".join(chars)
        # Preserve explicit relative paths; dots used as surrounding prose may
        # not conceal an otherwise absolute candidate.
        if not token.startswith(("./", "../")):
            token = token.lstrip(".")
        if len(token) > 1 and (PurePosixPath(token).is_absolute() or
                              PureWindowsPath(token).is_absolute() or
                              token.startswith(("\\", "~/"))):
            raise ValueError("absolute path in rendered metadata")

    candidate = []
    index = 0
    while index < len(value):
        if (index == 0 or not value[index - 1].isalnum()) and (
                value[index:index + 8].lower().startswith(("https://", "http://"))):
            check_candidate(candidate)
            candidate = []
            index = _uri_end(value, index)
            continue
        char = value[index]
        # Unicode punctuation and symbols include guillemets, smart/fullwidth
        # quotes and Markdown wrappers. Path separators and relative/home roots
        # retain their meaning. Labels split at ':'; Windows drive roots do not.
        drive_colon = (char == ":" and len(candidate) == 1 and
                       candidate[0] in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz" and
                       value[index + 1:index + 2] in ("/", "\\"))
        home_tilde = char == "~" and not candidate and value[index + 1:index + 2] == "/"
        boundary = char.isspace() or (unicodedata.category(char)[0] in "PS" and
                                     char not in "/\\." and not drive_colon and not home_tilde)
        if boundary:
            check_candidate(candidate)
            candidate = []
        else:
            candidate.append(char)
        index += 1
    check_candidate(candidate)


def _text(value) -> str:
    """Keep source prose inert in Markdown and reject local-path disclosures."""
    if value is None:
        return "—"
    if isinstance(value, bool):
        return str(value).lower()
    value = str(value)
    _check_metadata(value)
    value = html.escape(" ".join(value.split()), quote=False)
    for character in "\\`*_{}[]()#+!|:~":
        value = value.replace(character, "\\" + character)
    return value


def render_catalog(catalog: Catalog, locale: Literal["en", "ru"]) -> str:
    """Render both locales from the same validated model, with stable ID order.

    Pending research is visible; malformed existing records never render.
    Prose is public research metadata, not a place for secrets. This projection
    does not emit wordlist_bytes, collision words, URLs or vector payloads.
    """
    if locale not in ("en", "ru"):
        raise ValueError("unsupported catalogue locale")
    findings = validate_catalog(catalog, allow_incomplete_required=True)
    if any(f.severity == "error" for f in findings):
        raise ValueError("invalid catalogue cannot be rendered")

    def tr(en, ru):
        return en if locale == "en" else ru

    def source(record: Record) -> str:
        path = record.path.resolve().relative_to(catalog.root.resolve())
        if path.parts[0] != "catalog" or path.suffix != ".json":
            raise ValueError("record link outside catalogue")
        return f"[{_text(record.id)}](../{quote(path.as_posix(), safe='/')})"

    def ref(kind, identifier):
        return f"[{_text(identifier)}](#{kind}-{identifier})" if identifier else "—"

    def refs(kind, identifiers):
        return ", ".join(ref(kind, item) for item in sorted(identifiers)) or "—"

    evidence = {r.id: r for r in catalog.evidence}
    records = {r.id: r for r in (*catalog.wallets, *catalog.schemes, *catalog.dictionaries)}
    backup = tr("Not selectable; use the wallet's own backup procedure.",
                "Недоступно для выбора; используйте процедуру резервного копирования самого кошелька.")
    reasons = {
        "verified": tr("Verified research record; not a release or security guarantee.",
                       "Проверенная исследовательская запись; не гарантия релиза или безопасности."),
        "documented": tr("Evidence is insufficient for selectable support.",
                         "Доказательств недостаточно для доступной поддержки."),
        "blocked": tr("Support is blocked; see evidence and license decisions below.",
                      "Поддержка заблокирована; см. доказательства и решения о лицензии ниже."),
        "no-mnemonic-confirmed": tr("This mode does not expose a supported mnemonic backup.",
                                    "Этот режим не предоставляет поддерживаемую мнемоническую резервную копию."),
    }
    lines = [tr("# Tessaveil catalogue", "# Каталог Tessaveil"), "",
             tr("> Generated from catalog/*. Do not edit; run `python -m tools.catalog.cli generate --root .`.",
                "> Создано автоматически из catalog/*. Не редактировать; команда: `python -m tools.catalog.cli generate --root .`."), "",
             tr("Research only. A verified record is only a candidate for later table creation. Shared dictionaries do not imply compatible schemes. No key derivation or complete phrase validation. External secrets are never stored.",
                "Только исследование. Проверенная запись — лишь кандидат для создания таблиц в будущем. Общий словарь не означает совместимость схем. Ключи не выводятся, целые фразы не проверяются. Внешние секреты не сохраняются."), "",
             tr("Release readiness: NO-GO; catalogue validation does not resolve physical-device, clean-machine, filesystem, audit or release gates.",
                "Готовность релиза: NO-GO; проверка каталога не закрывает требования физических устройств, чистых систем, файловых систем, аудита и релиза."), ""]

    def section(en, ru):
        lines.extend([tr(f"## {en}", f"## {ru}"), ""])

    def field(en, ru, value):
        lines.append(f"- {tr(en, ru)}: {value}")

    def common(record, kind):
        data = record.data
        lines.extend([f'<a id="{kind}-{record.id}"></a>', "",
                      f"### {_text(data['display_name'][locale])} — {_text(record.id)}", ""])
        field("Source record", "Исходная запись", source(record))
        field("Status", "Статус", _text(data["status"]))
        field("Reason", "Причина", reasons[data["status"]])
        if data["status"] != "verified":
            field("Guidance", "Рекомендация", backup)
        version = data["version_interval"]
        field("Version interval (min / max)", "Диапазон версий (min / max)",
              f"{_text(version['min'])} / {_text(version['max'])}")
        field("Verified on", "Дата проверки", _text(data["verified_on"]))
        field("Historical", "Историческая запись", _text(data["historical"]))
        field("Evidence", "Доказательства", ", ".join(source(evidence[i]) for i in sorted(data["evidence_ids"])))
        for identifier in sorted(data["evidence_ids"]):
            item = evidence[identifier]
            field("Evidence claim", "Подтверждаемое утверждение", _text(item.data["claim"]))

    section("Required release blockers", "Обязательные блокеры релиза")
    blocked = sorted((item for required in catalog.required_sets for item in required.requirements
                      if item.data["status"] == "blocked"), key=lambda item: item.id)
    lines.append(tr(f"{len(blocked)} required items remain blocked. Terminal research is not release approval.",
                    f"Заблокировано обязательных пунктов: {len(blocked)}. Завершённое исследование не разрешает релиз."))
    lines.append("")
    for item in blocked:
        links = ", ".join(source(records[i]) for i in sorted(item.data["record_ids"]))
        lines.append(f"- {_text(item.id)}: {links}")
    lines.append("")
    section("Product index", "Индекс продуктов")
    lines.extend([tr("| Product / profile | Platform / mode | Networks | Scheme | Status |",
                     "| Продукт / профиль | Платформа / режим | Сети | Схема | Статус |"),
                  "| --- | --- | --- | --- | --- |"])
    for record in sorted(catalog.wallets, key=lambda r: (r.data["product_id"], r.id)):
        d = record.data
        lines.append(f"| {_text(d['product_name'])} / {ref('wallet', record.id)} | {_text(d['platform'])} / {_text(d['mode_id'])} | {_text(', '.join(sorted(d['network_ids'])))} | {ref('scheme', d['scheme_id'])} | {_text(d['status'])} |")
    lines.append("")
    section("Network index", "Индекс сетей")
    networks = sorted({n for r in catalog.wallets for n in r.data["network_ids"]})
    for network in networks:
        profiles = sorted(r.id for r in catalog.wallets if network in r.data["network_ids"])
        field(network, network, refs("wallet", profiles))
    lines.append("")
    section("Wallet profiles", "Профили кошельков")
    for record in sorted(catalog.wallets, key=lambda r: r.id):
        d = record.data
        common(record, "wallet")
        field("Aliases", "Другие названия", _text(", ".join(sorted(d["aliases"])) or None))
        field("Scheme", "Схема", ref("scheme", d["scheme_id"]))
        field("Generates mnemonic / import only", "Создаёт мнемонику / только импорт",
              f"{_text(d['generates_mnemonic'])} / {_text(d['import_only'])}")
        field("Limitations", "Ограничения", _text("; ".join(d["limitations"])))
        field("Profile guidance", "Рекомендация профиля", _text(d["guidance"]))
        lines.append("")
    section("Schemes", "Схемы")
    for record in sorted(catalog.schemes, key=lambda r: r.id):
        d = record.data
        common(record, "scheme")
        field("Dictionaries", "Словари", refs("dictionary", d["dictionary_ids"]))
        field("Supported lengths", "Допустимые длины", _text(", ".join(map(str, sorted(d["supported_lengths"]))) or None))
        field("Position rules", "Позиционные правила", _text("; ".join(d["position_rules"])))
        field("Semantics", "Семантика", _text(d["semantic_distinction"]))
        secret = d["external_secret"]
        field("External secret / stored", "Внешний секрет / сохраняется",
              f"{_text(secret['kind'])} / {_text(secret['stored'])}")
        field("External-secret guidance", "Рекомендация о внешнем секрете", _text(secret.get("guidance")))
        field("Test vectors", "Тестовые векторы", ", ".join(source(evidence[i]) for i in sorted(d["test_vector_ids"])) or "—")
        lines.append("")
    section("Dictionaries (one entry per ID)", "Словари (одна запись на ID)")
    for record in sorted(catalog.dictionaries, key=lambda r: r.id):
        d = record.data
        common(record, "dictionary")
        for key, en, ru in (("language", "Language", "Язык"), ("script", "Script", "Письменность"),
                            ("encoding", "Encoding", "Кодировка"), ("normalization", "Normalization", "Нормализация"),
                            ("word_count", "Word count", "Количество слов"), ("sha256", "SHA-256", "SHA-256"),
                            ("order_rule", "Order rule", "Порядок слов")):
            field(en, ru, _text(d[key]))
        field("Position rules", "Позиционные правила", _text("; ".join(d["position_rules"])))
        field("Source revision", "Ревизия источника", _text(d["source"]["revision"] if d["source"] else None))
        license_data = d["license"]
        for key, en, ru in (("spdx_or_name", "License", "Лицензия"), ("attribution", "Attribution", "Атрибуция"),
                            ("repository_redistribution", "Repository redistribution", "Распространение в репозитории"),
                            ("signpath_compatible", "SignPath compatibility", "Совместимость с SignPath")):
            field(en, ru, _text(license_data[key]))
        field("License evidence", "Доказательства лицензии", ", ".join(source(evidence[i]) for i in sorted(license_data["decision_evidence"])))
        field("Test vectors", "Тестовые векторы", ", ".join(source(evidence[i]) for i in sorted(d["test_vector_ids"])) or "—")
        lines.append("")
    section("Evidence revisions", "Ревизии доказательств")
    for record in sorted(catalog.evidence, key=lambda r: r.id):
        d = record.data
        lines.append(f"- {source(record)}: {_text(d['source_type'])}; {_text(d['revision'])}; {_text(d['verified_on'])}")
    lines.append("")
    section("Mandatory research coverage", "Охват обязательного исследования")
    lines.extend([tr("Pending is an unfinished research state, not a support status. Missing records remain visible. Source links contain full provenance URLs.",
                     "Pending означает незавершённое исследование, а не статус поддержки. Отсутствующие записи остаются видимыми. Полные URL источников находятся в исходных записях."), ""])
    for required in sorted(catalog.required_sets, key=lambda r: r.id):
        lines.extend([f"### {source(required)}", "",
                      tr("| Requirement | Research state | Status | Records |", "| Требование | Состояние исследования | Статус | Записи |"),
                      "| --- | --- | --- | --- |"])
        for item in sorted(required.requirements, key=lambda r: r.id):
            d = item.data
            links = ", ".join(source(records[i]) if i in records else _text(i) for i in sorted(d["record_ids"])) or "—"
            lines.append(f"| {_text(item.id)} — {_text(d['display_name'][locale])} | {_text(d['research_state'])} | {_text(d['status'])} | {links} |")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"
