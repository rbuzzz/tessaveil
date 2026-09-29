"""Immutable catalogue records. Source JSON is retained as frozen data."""

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping


@dataclass(frozen=True)
class SourceRef:
    url: str | None
    revision: str | None


@dataclass(frozen=True)
class LicenseDecision:
    repository_redistribution: str | None
    signpath_compatible: str | None
    decision_evidence: tuple[str, ...]


@dataclass(frozen=True)
class Record:
    id: str
    path: Path
    data: Mapping[str, Any]


@dataclass(frozen=True)
class DictionaryRecord(Record):
    source: SourceRef | None
    license: LicenseDecision | None
    wordlist_bytes: bytes | None


@dataclass(frozen=True)
class SchemeRecord(Record):
    pass


@dataclass(frozen=True)
class WalletRecord(Record):
    pass


@dataclass(frozen=True)
class EvidenceRecord(Record):
    pass


@dataclass(frozen=True)
class RequiredItem:
    id: str
    data: Mapping[str, Any]


@dataclass(frozen=True)
class RequiredSet(Record):
    requirements: tuple[RequiredItem, ...]


@dataclass(frozen=True)
class Catalog:
    root: Path
    dictionaries: tuple[DictionaryRecord, ...]
    schemes: tuple[SchemeRecord, ...]
    wallets: tuple[WalletRecord, ...]
    evidence: tuple[EvidenceRecord, ...]
    required_sets: tuple[RequiredSet, ...]


@dataclass(frozen=True)
class Finding:
    severity: str
    code: str
    location: str
    message: str
