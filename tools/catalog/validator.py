"""Offline schema parity and cross-record, fail-closed validation."""

from datetime import date
import hashlib
import json
from pathlib import Path
import re
import unicodedata
from urllib.parse import urlsplit
from typing import Any, Mapping

from .model import Catalog, Finding, Record


SCHEMA_DIR = Path(__file__).resolve().parents[2] / "catalog" / "schema"
KINDS = (("dictionaries", "dictionary"), ("schemes", "scheme"),
         ("wallets", "wallet"), ("evidence", "evidence"), ("required_sets", "required-set"))
TERMINAL = {"verified", "documented", "blocked", "no-mnemonic-confirmed"}
PRIMARY_EVIDENCE = {"official-specification", "official-documentation", "official-source"}
SUPPORTED_LENGTHS = {12, 13, 15, 16, 18, 20, 21, 24, 25, 26, 27, 28, 29, 33}
SUPPORTED_SCHEMA_KEYS = frozenset({
    "$schema", "$id", "title", "type", "required", "properties", "additionalProperties",
    "const", "enum", "minLength", "pattern", "uniqueItems", "minItems", "maxItems",
    "items", "minimum", "anyOf", "allOf", "if", "then", "format",
})
SUPPORTED_TYPES = frozenset({"object", "array", "string", "integer", "number", "boolean", "null"})


def _schema_supported(schema: Any) -> bool:
    if not isinstance(schema, Mapping) or any(key not in SUPPORTED_SCHEMA_KEYS for key in schema):
        return False
    if "type" in schema:
        types = schema["type"] if isinstance(schema["type"], list) else [schema["type"]]
        if not types or any(name not in SUPPORTED_TYPES for name in types):
            return False
    if "format" in schema and schema["format"] not in ("date", "uri"):
        return False
    if "additionalProperties" in schema and type(schema["additionalProperties"]) is not bool:
        return False
    children = []
    for key in ("properties",):
        if key in schema:
            if not isinstance(schema[key], Mapping):
                return False
            children.extend(schema[key].values())
    for key in ("items", "if", "then"):
        if key in schema:
            children.append(schema[key])
    for key in ("anyOf", "allOf"):
        if key in schema:
            if not isinstance(schema[key], list):
                return False
            children.extend(schema[key])
    return all(_schema_supported(child) for child in children)


def _json_equal(left: Any, right: Any) -> bool:
    if type(left) is bool or type(right) is bool:
        return type(left) is type(right) and left == right
    if type(left) in (int, float) and type(right) in (int, float):
        return left == right
    if isinstance(left, Mapping) and isinstance(right, Mapping):
        return left.keys() == right.keys() and all(_json_equal(left[key], right[key]) for key in left)
    if isinstance(left, (list, tuple)) and isinstance(right, (list, tuple)):
        return len(left) == len(right) and all(_json_equal(a, b) for a, b in zip(left, right))
    return type(left) is type(right) and left == right


def _type_matches(value: Any, expected: str) -> bool:
    return {
        "object": lambda: isinstance(value, Mapping),
        "array": lambda: isinstance(value, (list, tuple)),
        "string": lambda: isinstance(value, str),
        "integer": lambda: type(value) is int,
        "number": lambda: type(value) in (int, float),
        "boolean": lambda: type(value) is bool,
        "null": lambda: value is None,
    }[expected]()


def _schema_valid(value: Any, schema: Mapping[str, Any]) -> bool:
    """Evaluate the closed JSON Schema vocabulary used by this repository."""
    expected = schema.get("type")
    if expected is not None and not any(_type_matches(value, t) for t in
                                    (expected if isinstance(expected, list) else [expected])):
        return False
    if "const" in schema and not _json_equal(value, schema["const"]):
        return False
    if "enum" in schema and not any(_json_equal(value, item) for item in schema["enum"]):
        return False
    if isinstance(value, Mapping):
        if any(key not in value for key in schema.get("required", ())):
            return False
        properties = schema.get("properties", {})
        if schema.get("additionalProperties") is False and any(key not in properties for key in value):
            return False
        if any(not _schema_valid(item, properties[key]) for key, item in value.items() if key in properties):
            return False
    if isinstance(value, (list, tuple)):
        if len(value) < schema.get("minItems", 0) or len(value) > schema.get("maxItems", float("inf")):
            return False
        if schema.get("uniqueItems") and any(_json_equal(value[i], value[j]) for i in range(len(value)) for j in range(i + 1, len(value))):
            return False
        if "items" in schema and any(not _schema_valid(item, schema["items"]) for item in value):
            return False
    if isinstance(value, str):
        if len(value) < schema.get("minLength", 0):
            return False
        if "pattern" in schema and re.search(schema["pattern"], value) is None:
            return False
        if schema.get("format") == "date":
            try:
                if date.fromisoformat(value).isoformat() != value:
                    return False
            except ValueError:
                return False
        if schema.get("format") == "uri" and not (urlsplit(value).scheme and urlsplit(value).netloc):
            return False
    if type(value) in (int, float) and value < schema.get("minimum", float("-inf")):
        return False
    if "anyOf" in schema and not any(_schema_valid(value, part) for part in schema["anyOf"]):
        return False
    if "allOf" in schema and not all(_schema_valid(value, part) for part in schema["allOf"]):
        return False
    if "if" in schema and _schema_valid(value, schema["if"]):
        if "then" in schema and not _schema_valid(value, schema["then"]):
            return False
    return True


def validate_catalog(catalog: Catalog, require_terminal: bool = True,
                     require_release_ready: bool = False,
                     allow_incomplete_required: bool = False) -> tuple[Finding, ...]:
    """Return deterministic, bounded findings without exposing source words."""
    findings: list[Finding] = []

    def add(code: str, record: Record | str, message: str, severity: str = "error") -> None:
        location = record.id if isinstance(record, Record) else record
        findings.append(Finding(severity, code, location[:120], message))

    if not any(record.id == "windows-v1" for record in catalog.required_sets):
        add("required-set-missing", "windows-v1", "mandatory required set is missing")

    all_records: list[Record] = []
    for attr, kind in KINDS:
        schema = json.loads((SCHEMA_DIR / f"{kind}.schema.json").read_text(encoding="utf-8"))
        supported = _schema_supported(schema)
        if not supported:
            add("unsupported-schema", kind, "schema contains an unsupported keyword or value")
        for record in getattr(catalog, attr):
            all_records.append(record)
            if not supported or not _schema_valid(record.data, schema):
                add("schema", record, f"{kind} record violates schema")
    invalid = {finding.location for finding in findings if finding.code == "schema"}
    known: dict[str, Record] = {}
    for record in all_records:
        if record.id in known:
            add("duplicate-record-id", record, "record ID is duplicated")
        known[record.id] = record
    evidence = {record.id: record for record in catalog.evidence}
    dictionaries = {record.id: record for record in catalog.dictionaries}
    schemes = {record.id: record for record in catalog.schemes}
    wallets = {record.id: record for record in catalog.wallets}

    def refs(record: Record, ids: Any, targets: Mapping[str, Record], missing_code: str) -> None:
        if not isinstance(ids, (list, tuple)):
            return
        for identifier in ids:
            if isinstance(identifier, str) and identifier not in targets:
                add(missing_code, record, "referenced record is missing")

    def evidence_refs(record: Record, ids: Any) -> None:
        refs(record, ids, evidence, "missing-evidence")
        if not isinstance(ids, (list, tuple)):
            return
        for identifier in ids:
            target = evidence.get(identifier)
            backlinks = target.data.get("record_ids") if target else None
            if target and isinstance(backlinks, (list, tuple)) and record.id not in backlinks:
                add("evidence-backlink", record, "evidence does not name referencing record")

    for record in catalog.evidence:
        if record.id in invalid:
            add("unpinned-evidence", record, "evidence lacks a valid pinned source")
            continue
        if not record.data.get("revision") or not record.data.get("verified_on") or not record.data.get("url"):
            add("unpinned-evidence", record, "evidence lacks a pinned source")
        refs(record, record.data.get("record_ids"), known, "missing-reference")

    for record in (*catalog.dictionaries, *catalog.schemes, *catalog.wallets):
        if record.id in invalid:
            continue
        evidence_refs(record, record.data.get("evidence_ids"))
        if record.data.get("status") not in TERMINAL:
            add("unsupported-status", record, "unsupported status")
        if record.data.get("status") == "blocked" and not record.data.get("evidence_ids"):
            add("unevidenced-blocker", record, "blocker requires evidence")
        if record.data.get("status") == "verified" and not any(
            identifier in evidence and identifier not in invalid and
            evidence[identifier].data.get("source_type") in PRIMARY_EVIDENCE and
            record.id in evidence[identifier].data.get("record_ids", ())
            for identifier in record.data.get("evidence_ids", ())
        ):
            add("primary-evidence", record, "verified record requires valid primary evidence with backlink")

    for record in catalog.dictionaries:
        data = record.data
        license_data = data.get("license", {})
        if (data.get("status") == "verified" or record.wordlist_bytes is not None) and (
            not isinstance(license_data, Mapping) or
            license_data.get("repository_redistribution") != "allowed" or
            license_data.get("signpath_compatible") != "compatible"
        ):
            add("license-decision", record, "verified or bundled dictionary requires allowed and compatible license decisions")
        if record.id in invalid:
            continue
        evidence_refs(record, license_data.get("decision_evidence"))
        evidence_refs(record, data.get("test_vector_ids"))
        if record.wordlist_bytes is None:
            if data.get("status") == "verified":
                add("word-list-missing", record, "verified dictionary lacks word list")
            continue
        if hashlib.sha256(record.wordlist_bytes).hexdigest() != data.get("sha256"):
            add("word-sha256", record, "word-list SHA-256 mismatch")
        words = record.wordlist_bytes.decode("utf-8").splitlines()
        if len(words) != data.get("word_count"):
            add("word-count", record, "word-list count mismatch")
        normalization = data.get("normalization")
        if normalization in ("none", "NFC", "NFD", "NFKC", "NFKD"):
            normalized = words if normalization == "none" else [unicodedata.normalize(normalization, word) for word in words]
            unique_count = len(set(normalized))
            if unique_count != len(normalized):
                add("normalization-collision", record, "word list has normalization collisions")
            analysis = data.get("duplicate_analysis")
            if isinstance(analysis, Mapping) and analysis.get("normalized_unique_count") != unique_count:
                add("duplicate-analysis", record, "normalized unique count mismatch")

    for record in catalog.schemes:
        if record.id in invalid:
            continue
        refs(record, record.data.get("dictionary_ids"), dictionaries, "missing-reference")
        evidence_refs(record, record.data.get("test_vector_ids"))
        lengths = record.data.get("supported_lengths", ())
        if any(type(length) is not int or length not in SUPPORTED_LENGTHS for length in lengths):
            add("unsupported-length", record, "unsupported phrase length")

    for record in catalog.wallets:
        if record.id in invalid:
            continue
        scheme_id = record.data.get("scheme_id")
        if scheme_id is not None and scheme_id not in schemes:
            add("missing-reference", record, "scheme reference is missing")

    for required_set in catalog.required_sets:
        if required_set.id in invalid:
            continue
        seen: set[str] = set()
        for item in required_set.requirements:
            if item.id in seen:
                add("duplicate-required-id", item.id, "required ID is duplicated")
            seen.add(item.id)
            data = item.data
            if data.get("research_state") == "pending":
                if require_terminal or require_release_ready:
                    add("required-pending", item.id, "required research remains pending",
                        "warning" if allow_incomplete_required else "error")
                continue
            prefix = item.id.split("-", 1)[0]
            for identifier in data.get("record_ids", ()):
                target = known.get(identifier)
                matched = ((prefix == "dictionary" and identifier in dictionaries) or
                           (prefix == "scheme" and identifier in schemes) or
                           (prefix == "wallet" and identifier in wallets) or
                           (prefix == "network" and identifier in wallets and
                            item.id.removeprefix("network-") in wallets[identifier].data.get("network_ids", ())))
                if not target or not matched:
                    add("required-record-missing", item.id, "required record reference is missing",
                        "warning" if allow_incomplete_required and not target else "error")
                elif target.data.get("status") != data.get("status"):
                    add("required-status-mismatch", item.id, "required status differs from record")
            if require_release_ready and data.get("status") == "blocked":
                add("required-blocked", item.id, "required item remains blocked")
    return tuple(sorted(findings, key=lambda f: (f.location, f.code, f.severity, f.message)))
