"""Bounded JSON and word-list loader; no network operations."""

from dataclasses import dataclass
import json
import os
from pathlib import Path
from types import MappingProxyType
from typing import Any

from .model import (Catalog, DictionaryRecord, EvidenceRecord, LicenseDecision,
                    RequiredItem, RequiredSet, SchemeRecord, SourceRef, WalletRecord)


@dataclass(frozen=True)
class LoadLimits:
    max_record_bytes: int = 1024 * 1024
    max_records: int = 10_000
    max_string_bytes: int = 16 * 1024
    max_wordlist_bytes: int = 16 * 1024 * 1024
    max_nesting: int = 128


DEFAULT_LIMITS = LoadLimits()
FOLDERS = ("dictionaries", "schemes", "wallets", "evidence", "required")


def _pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
    result = {}
    for key, value in items:
        if key in result:
            raise ValueError("duplicate JSON key")
        result[key] = value
    return result


def _reject_constant(value: str) -> None:
    raise ValueError("non-finite JSON number")


def _bounded_strings(value: Any, limits: LoadLimits) -> None:
    pending = [(value, 0)]
    while pending:
        current, depth = pending.pop()
        if depth > limits.max_nesting:
            raise ValueError("JSON nesting exceeds limit")
        if isinstance(current, str):
            if len(current.encode("utf-8")) > limits.max_string_bytes:
                raise ValueError("string length exceeds limit")
        elif isinstance(current, dict):
            for key, item in current.items():
                pending.append((key, depth + 1))
                pending.append((item, depth + 1))
        elif isinstance(current, list):
            pending.extend((item, depth + 1) for item in current)


def _freeze(value: Any) -> Any:
    if isinstance(value, dict):
        return MappingProxyType({key: _freeze(item) for key, item in value.items()})
    if isinstance(value, list):
        return tuple(_freeze(item) for item in value)
    return value


def _read_json(path: Path, limits: LoadLimits) -> dict[str, Any]:
    if path.is_symlink() or path.stat().st_size > limits.max_record_bytes:
        raise ValueError("record size or path rejected")
    try:
        document = json.loads(path.read_bytes().decode("utf-8"), object_pairs_hook=_pairs,
                              parse_constant=_reject_constant)
    except UnicodeDecodeError as exc:
        raise ValueError("invalid UTF-8 in record") from exc
    except json.JSONDecodeError as exc:
        raise ValueError("invalid JSON record") from exc
    except RecursionError as exc:
        raise ValueError("JSON nesting exceeds limit") from exc
    if not isinstance(document, dict):
        raise ValueError("JSON record must be an object")
    _bounded_strings(document, limits)
    if type(document.get("schema_version")) is not int or document["schema_version"] != 1:
        raise ValueError("unsupported schema version")
    return document


def _wordlist(root: Path, relative: Any, limits: LoadLimits) -> bytes | None:
    if relative is None:
        return None
    if not isinstance(relative, str):
        raise ValueError("invalid word-list path")
    path = Path(relative)
    if path.is_absolute() or "\\" in relative or not path.parts or path.parts[0] != "wordlists" or any(
        part in (".", "..") for part in path.parts
    ):
        raise ValueError("invalid word-list path")
    target = root / path
    if not target.resolve().is_relative_to(root.resolve()) or target.is_symlink():
        raise ValueError("invalid word-list path")
    if not target.is_file():
        raise ValueError("missing word-list file")
    if target.stat().st_size > limits.max_wordlist_bytes:
        raise ValueError("word-list size exceeds limit")
    data = target.read_bytes()
    try:
        data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("invalid UTF-8 in word list") from exc
    return data


def load_catalog(root: Path, limits: LoadLimits = DEFAULT_LIMITS) -> Catalog:
    """Load fixed catalogue folders only, rejecting oversized or ambiguous input."""
    root = Path(root).resolve()
    if (root / "catalog").is_symlink():
        raise ValueError("catalogue path rejected")
    files: list[tuple[str, Path]] = []
    for folder in FOLDERS:
        directory = root / "catalog" / folder
        if directory.is_symlink():
            raise ValueError("catalogue path rejected")
        if directory.is_dir():
            with os.scandir(directory) as entries:
                for entry in entries:
                    if entry.name.endswith(".json"):
                        files.append((folder, directory / entry.name))
                        if len(files) > limits.max_records:
                            raise ValueError("record count exceeds limit")
    files.sort(key=lambda item: (FOLDERS.index(item[0]), str(item[1])))
    groups: dict[str, list[Any]] = {folder: [] for folder in FOLDERS}
    for folder, path in files:
        data = _read_json(path, limits)
        identifier = data.get("id")
        if not isinstance(identifier, str):
            identifier = ""
        frozen = _freeze(data)
        if folder == "dictionaries":
            source = data.get("source")
            source_ref = SourceRef(source.get("url") if isinstance(source.get("url"), str) else None,
                                   source.get("revision") if isinstance(source.get("revision"), str) else None) if isinstance(source, dict) else None
            license_data = data.get("license")
            decision_evidence = license_data.get("decision_evidence") if isinstance(license_data, dict) else None
            license_ref = LicenseDecision(license_data.get("repository_redistribution"),
                                          license_data.get("signpath_compatible"),
                                          tuple(item for item in decision_evidence if isinstance(item, str))
                                          if isinstance(decision_evidence, list) else ()) if isinstance(license_data, dict) else None
            groups[folder].append(DictionaryRecord(identifier, path, frozen, source_ref,
                                                    license_ref, _wordlist(root, data.get("wordlist_path"), limits)))
        elif folder == "schemes":
            groups[folder].append(SchemeRecord(identifier, path, frozen))
        elif folder == "wallets":
            groups[folder].append(WalletRecord(identifier, path, frozen))
        elif folder == "evidence":
            groups[folder].append(EvidenceRecord(identifier, path, frozen))
        else:
            items = data.get("requirements", [])
            required = tuple(RequiredItem(item.get("id") if isinstance(item.get("id"), str) else "", _freeze(item)) for item in items
                             if isinstance(item, dict)) if isinstance(items, list) else ()
            groups[folder].append(RequiredSet(identifier, path, frozen, required))
    return Catalog(root, *(tuple(groups[folder]) for folder in FOLDERS))
