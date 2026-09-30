"""Offline deterministic alpha archives. No upload, signing or provenance claims."""

import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import stat
import struct
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from tools.sensitive_material import inspect_text  # noqa: E402


def pe_imports(data):
    def unpack(fmt, offset):
        if offset < 0 or offset + struct.calcsize(fmt) > len(data):
            raise ValueError("PE truncated")
        return struct.unpack_from(fmt, data, offset)
    if data[:2] != b"MZ":
        raise ValueError("PE DOS signature missing")
    pe = unpack("<I", 60)[0]
    if data[pe:pe + 4] != b"PE\0\0":
        raise ValueError("PE signature missing")
    machine, count = unpack("<HH", pe + 4)
    size = unpack("<H", pe + 20)[0]
    optional = pe + 24
    if machine != 0x8664 or not 1 <= count <= 96 or size < 240 or unpack("<H", optional)[0] != 0x20b:
        raise ValueError("PE must be bounded AMD64 PE32+")
    if unpack("<I", optional + 108)[0] < 16:
        raise ValueError("PE directory table incomplete")
    if any(unpack("<II", optional + 112 + 8 * 4)) or any(unpack("<II", optional + 112 + 8 * 13)):
        raise ValueError("PE signature or delayed imports are not permitted")
    sections = [unpack("<IIII", optional + size + i * 40 + 8) for i in range(count)]
    def file_offset(rva):
        for virtual_size, address, raw_size, raw_offset in sections:
            if address <= rva < address + min(virtual_size, raw_size):
                offset = raw_offset + rva - address
                if offset < len(data):
                    return offset
        raise ValueError("PE import RVA outside bounded sections")
    rva, length = unpack("<II", optional + 120)
    if not rva or not 20 <= length <= 65536:
        raise ValueError("PE import table invalid")
    imports = []
    allowed = frozenset("advapi32 authz bcrypt bcryptprimitives comdlg32 crypt32 d2d1 d3d9 d3d11 d3d12 dbghelp dwmapi dwrite dxgi gdi32 imm32 kernel32 mpr msvcrt netapi32 ntdll ole32 oleaut32 rpcrt4 runtimeobject setupapi shcore shell32 shlwapi synchronization ucrtbase user32 userenv uxtheme version winmm winspool ws2_32 wtsapi32".split())
    for index in range(length // 20):
        entry = unpack("<IIIII", file_offset(rva + index * 20))
        if not any(entry):
            if not imports:
                raise ValueError("PE has no system imports")
            return sorted(set(imports), key=str.lower)
        offset = file_offset(entry[3])
        end = data.find(b"\0", offset, offset + 256)
        if end < 0:
            raise ValueError("PE import name unterminated")
        try:
            name = data[offset:end].decode("ascii")
        except UnicodeDecodeError as error:
            raise ValueError("PE invalid import name") from error
        lower = name.lower()
        if not re.fullmatch(r"[a-z0-9_-]+\.dll", lower) or not (lower[:-4] in allowed or lower.startswith("api-ms-win-")):
            raise ValueError("PE non-system runtime dependency")
        imports.append(name)
    raise ValueError("PE import table not terminated")


def vendor_scan_copy(executable, sources, pins):
    if set(sources) != set(pins) or any(digest(sources[name]) != pins[name] for name in pins):
        raise ValueError("vendor archive member hash mismatch")
    # Only the upstream LLVM-MinGW CI workspace prefix, and only complete
    # byte strings independently present in immutable supplier archive members.
    prefix = b"/ho" + b"me/runner/work/llvm-mingw/"
    spans = []
    cleaned = bytearray(executable)
    for match in re.finditer(re.escape(prefix) + rb"[^\x00\r\n]+", executable):
        raw = match[0]
        proof = sorted(name for name, data in sources.items() if raw + b"\0" in data)
        if not proof:
            raise ValueError("vendor build string lacks exact supplier proof")
        spans.append({"offset": match.start(), "length": len(raw), "sha256": digest(raw), "supplier_members": proof})
        cleaned[match.start():match.end()] = b" " * len(raw)
    return bytes(cleaned), {"exe_sha256": digest(executable), "spans": spans,
                            "supplier_member_sha256": pins}


def link_inventory(text, archives):
    members = set(re.findall(r"^\S+\s+\S+\s+\d+\s+([^\r\n]+?\.(?:obj|o)):\(", text, re.M))
    if not members:
        raise ValueError("unmapped: empty link map")
    result = {}
    for member in sorted(members):
        basename = member.replace("\\", "/").rsplit("/", 1)[-1]
        matches = sorted(name for name, names in archives.items() if basename in names)
        if not matches:
            raise ValueError("unmapped object: " + basename)
        result[basename] = sorted(set(result.get(basename, []) + matches))
    return result


def qt_attributions(data):
    # Qt's pinned attribution files contain literal newlines in quoted strings.
    # Retain the text verbatim; our emitted SBOM uses standard escaped JSON.
    parsed = json.loads(data, strict=False)
    records = parsed if isinstance(parsed, list) else [parsed]
    if any(not isinstance(item, dict) or not item.get("Id") or not item.get("Name") for item in records):
        raise ValueError("invalid Qt attribution record")
    return records


def audit_runtime(files, source_sha, words, public_dictionary=b"", vendor_sources=None, vendor_pins=None):
    required = {"Tessaveil.exe", "SOURCE_SHA", "SHA256SUMS", "sbom.cdx.json",
                "THIRD_PARTY_ALPHA.md", "THIRD_PARTY_NOTICES", "LICENSE",
                "user-guide.md", "known-limitations.md", "release-evidence.json",
                "PE-imports.json", "runtime-observation.json", "vendor-build-prefixes.json"}
    if set(files) != required or files["SOURCE_SHA"] != (source_sha + "\n").encode():
        raise ValueError("runtime inventory or source SHA mismatch")
    verify_manifest(files)
    imports = pe_imports(files["Tessaveil.exe"])
    if json.loads(files["PE-imports.json"]) != {"exe_sha256": digest(files["Tessaveil.exe"]), "imports": imports}:
        raise ValueError("PE imports evidence mismatch")
    sbom = json.loads(files["sbom.cdx.json"])
    if sbom.get("bomFormat") != "CycloneDX" or sbom.get("specVersion") != "1.6":
        raise ValueError("invalid SBOM")
    evidence = json.loads(files["release-evidence.json"])
    if evidence.get("source_sha") != source_sha or evidence.get("exe_sha256") != digest(files["Tessaveil.exe"]):
        raise ValueError("runtime evidence is stale")
    scanned_exe, vendor_report = vendor_scan_copy(files["Tessaveil.exe"], vendor_sources or {}, vendor_pins or {})
    if json.loads(files["vendor-build-prefixes.json"]) != vendor_report:
        raise ValueError("vendor prefix evidence is stale")
    for name, data in files.items():
        if name == "Tessaveil.exe":
            data = scanned_exe
            if public_dictionary:
                data = data.replace(public_dictionary, b"<verified-public-dictionary>")
        scan_bytes(name, data, words)


def rust_components(packages, metadata):
    locked = {(p["name"], p["version"]): p for p in packages}
    actual = {(p["name"], p["version"]): p for p in metadata["packages"]}
    if locked.keys() != actual.keys():
        raise ValueError("locked metadata package drift")
    components = []
    for key, item in sorted(actual.items()):
        lock = locked[key]
        if item.get("source") != lock.get("source"):
            raise ValueError("locked metadata source drift")
        if not item.get("license"):
            raise ValueError("missing dependency license")
        ref = f"pkg:cargo/{key[0]}@{key[1]}"
        component = {"type": "library", "bom-ref": ref, "name": key[0], "version": key[1],
                     "licenses": [{"expression": item["license"].replace("MIT/Apache-2.0", "MIT OR Apache-2.0")}],
                     "properties": [{"name": "tessaveil:scope", "value": "locked graph including dev/build/conditional dependencies"}]}
        if lock.get("source"):
            if not re.fullmatch(r"[0-9a-f]{64}", lock.get("checksum", "")):
                raise ValueError("locked metadata checksum missing")
            component["purl"] = ref
            component["hashes"] = [{"alg": "SHA-256", "content": lock["checksum"]}]
            component["externalReferences"] = [{"type": "distribution", "url": f"https://static.crates.io/crates/{key[0]}/{key[0]}-{key[1]}.crate"}]
        components.append(component)
    return components


def digest(data):
    return hashlib.sha256(data).hexdigest()


def safe_name(name):
    path = PurePosixPath(name)
    return (bool(name) and not path.is_absolute() and "\\" not in name
            and ":" not in name and "\0" not in name
            and all(part not in ("", ".", "..") and not part.endswith((".", " "))
                    for part in name.split("/")))


def read_archive(path):
    files, seen, total = {}, set(), 0
    with zipfile.ZipFile(path) as archive:
        if len(archive.infolist()) > 100000:
            raise ValueError("unsafe archive: too many entries")
        for entry in archive.infolist():
            total += entry.file_size
            if (not safe_name(entry.filename) or entry.filename.casefold() in seen
                    or stat.S_ISLNK(entry.external_attr >> 16) or entry.is_dir()
                    or entry.flag_bits & 1 or total > 2 * 1024**3):
                raise ValueError("unsafe archive")
            seen.add(entry.filename.casefold())
            files[entry.filename] = archive.read(entry)
    return files


def make_manifest(files):
    if "SHA256SUMS" in files or any(not safe_name(name) for name in files):
        raise ValueError("manifest: unsafe name")
    return "".join(f"{digest(files[name])}  {name}\n" for name in sorted(files)).encode()


def verify_manifest(files):
    expected = make_manifest({name: data for name, data in files.items() if name != "SHA256SUMS"})
    if files.get("SHA256SUMS") != expected:
        raise ValueError("manifest: missing, extra or changed bytes")


def scan_bytes(name, data, words):
    # Never print matched bytes. Both common encodings are inspected even in PE/object files.
    if data.startswith(b"TSVALPHA"):
        raise ValueError("sensitive: vault payload")
    for text in (data.decode("utf-8", errors="replace"), data.decode("utf-16le", errors="replace")):
        if (inspect_text(name, text, words) or re.search(
                r"synthetic-(?:master|sheet|wrong)-password", text, re.I)):
            raise ValueError("sensitive: content rejected")


def require_distribution_clearance(evidence, source_sha):
    required = ("corresponding_source", "application_material", "modified_qt_relink",
                "replacement_information", "qt_third_party_review", "rust_runtime_review",
                "dictionary_review", "artifact_audit")
    if (not re.fullmatch(r"[0-9a-f]{40}", source_sha)
            or evidence.get("source_sha") != source_sha
            or evidence.get("status") != "PASS"
            or any(evidence.get(key) is not True for key in required)):
        raise ValueError("compliance: redistribution gate is BLOCKED")


def check_relink_proof(proof, source_sha, executable_sha256, application_hashes):
    if (proof.get("source_sha") != source_sha
            or proof.get("original_exe_sha256") != executable_sha256
            or not re.fullmatch(r"[a-f0-9]{64}", proof.get("modified_exe_sha256", ""))
            or proof["modified_exe_sha256"] == executable_sha256
            or proof.get("application_sha256") != application_hashes
            or not application_hashes
            or proof.get("modified_qt_marker_in_application") is not True
            or proof.get("marker_probe") != "MODIFIED_QT_CONFIRMED"
            or any(proof.get("synthetic_smoke", {}).get(key) is not True for key in
                   ("open_close_reopen_lock", "authentication_safe", "all_five_password_controls_masked"))):
        raise ValueError("relink proof missing, stale or not a modified-library exercise")


def verify_license_bindings(files, bindings):
    expected = {name: digest(data) for name, data in files.items() if name.startswith(
        ("qt-licenses/", "qt-third-party/", "qt-attributions/", "rust-licenses/", "runtime-notices/")) or name in ("LICENSE", "license-review.md")}
    if not expected or bindings != expected:
        raise ValueError("license bindings missing, extra or changed bytes")


def verify_inventory(files, expected):
    if sorted(files) != sorted(expected) or len(expected) != len(set(expected)):
        raise ValueError("inventory: missing or unrelated compliance member")


def write_archive(path, files):
    # ZIP_STORED avoids zlib-version-dependent output. Fixed metadata, exact bytes.
    if any(not safe_name(name) for name in files):
        raise ValueError("unsafe archive")
    with zipfile.ZipFile(path, "x", compression=zipfile.ZIP_STORED) as archive:
        for name in sorted(files):
            info = zipfile.ZipInfo(name, (1980, 1, 1, 0, 0, 0))
            info.create_system = 3
            info.external_attr = (stat.S_IFREG | 0o644) << 16
            archive.writestr(info, files[name])
