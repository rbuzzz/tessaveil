# Provisional encrypted alpha vault core

Engineering-only format, version 1; synthetic data only. Extension:
`.tessaveil-alpha`. This is not `.tessaveil`, has no migration promise, is not a
production backup format, and does not close the KDF, physical-mobile,
cross-platform, clean-Windows, removable-media, audit or release gates.
The core is GUI-independent Rust 1.90.0; it does not depend on Qt.

## Envelope

Integers in the open header are unsigned little-endian. The header is exactly
140 bytes; there are no optional cleartext fields or trailing bytes.

| Offset | Bytes | Meaning |
| --- | --- | --- |
| 0 | 8 | ASCII `TSVALPHA` |
| 8 | 2 | Alpha envelope version 1 |
| 10 | 1 | KDF ID 1: Argon2id, Argon2 version 0x13 |
| 11 | 1 | AEAD ID 1: XChaCha20-Poly1305 |
| 12 | 4 | Memory in KiB |
| 16 | 4 | Iterations |
| 20 | 4 | Parallelism |
| 24 | 16 | OS-random salt |
| 40 | 24 | Independent OS-random wrapping nonce |
| 64 | 24 | Independent OS-random payload nonce |
| 88 | 4 | Payload ciphertext length including 16-byte tag |
| 92 | 32 | Encrypted 256-bit DEK |
| 124 | 16 | DEK wrapping tag |
| 140 | Variable | Payload ciphertext, then 16-byte tag |

Wrapping AAD is the exact bytes `[0,92)`. Payload AAD is the exact complete
header `[0,140)`, including wrapped DEK and tag. Both nonces are independently
drawn and must differ. Every save draws two fresh nonces; creation draws new
salt and DEK. Open retains KEK and DEK, never the password. Password change is
not implemented by this task; it must create a new salt, KEK, DEK and nonces.

Absolute encoding bounds are 65,536–262,144 KiB, 3–6 iterations, 1–8 lanes,
32-byte output and 16-byte salt. The **only** alpha creation/open allowlist
tuple is `(65536, 3, 4)`. Out-of-bounds and non-allowlisted profiles are rejected
before password normalization, Argon2 workspace allocation or ciphertext
allocation. No clamping, automatic fallback or profile weakening occurs.
Argon2 uses an explicit zeroizing 64 MiB block workspace.

Maximum plaintext CBOR is 8,388,608 bytes; maximum ciphertext is 8,388,624
bytes; maximum complete file is 8,388,764 bytes. Minimum ciphertext length is
17 bytes. File metadata and a stack-resident 140-byte header are checked before
allocating the body. Extra bytes are rejected. A length-limited reader retains
its Windows handle with write sharing denied during authentication.

## Password input

Explicit-length Rust UTF-8 strings are normalized to NFC inside the core.
Embedded NUL and input/output over 4,096 UTF-8 bytes are rejected. The output
owner reserves 4,096 bytes before receiving secret bytes; checked pushes cannot
grow it and free unwiped prefixes. The ASCII blocklist uses allocation-free
case-insensitive comparison and creates no lowercase password copy. Creation
requires at least 15 normalized Unicode scalar values; 64 characters and
non-BMP characters are supported. No composition rules apply. A small local
alpha blocklist rejects four common long passwords and a repeated single
character pattern; this is a deliberately limited engineering filter, not a
finished common-password database or strength estimator. There is no telemetry.
Opening never applies a changed creation policy to an existing password.

## Deterministic CBOR schema

The codec is private to the crate and hand-implements only this restricted CBOR
grammar. It does not use generic maps or dynamic values. Every array and text
string has a definite length; unsigned integers and lengths use their shortest
encoding. CBOR length bytes are big-endian as required by CBOR. Indefinite
lengths, non-shortest encodings, tags, maps, floats, negative integers, invalid
UTF-8, embedded NUL, unexpected fields and trailing bytes are rejected.

```
Payload = [1, name, locale, [Sheet...]]
Sheet = [name, profile_id, [dictionary_word...], [[cell...], ...],
         verified_by_user, protected]
```

The independent canonical vector for an empty payload is `84 01 60 60 80`.
The writer emits this same representation every time for the same model;
encryption intentionally remains randomized.

| Field | Limit |
| --- | --- |
| Name (vault or sheet) | 256 UTF-8 bytes |
| Locale | 16 UTF-8 bytes |
| Profile ID | 128 UTF-8 bytes |
| Sheets | 32 |
| Dictionary entries per sheet | 8,192 |
| Dictionary word or table cell | 128 UTF-8 bytes |
| Rows | Empty, or 12,13,15,16,18,20,21,24,25,26,27,28,29,33 |
| Columns | Exactly 10 or 36, identical for every row in a sheet |
| Total encoded payload | 8 MiB |

Count and text-size limits are checked before their associated allocations.
The serializer uses one bounded buffer, avoiding plaintext reallocation copies.
These are structural bounds, not catalogue/profile validation; domain sheet
operations are the next task. Adding mandatory fields requires a schema
discriminator/envelope version bump. A correctly decoded discriminator other
than 1 returns `UnsupportedVersion`, including when the future array has a
different arity. The canonical outer array/count and first discriminator are
read before applying the exact v1 arity. Empty/overlong/noncanonical prefixes
remain malformed; a shape change without a version bump is
malformed authenticated data and returns `Authentication`.

There are no stored fields for Spin input, target column, ordering information,
whole phrases, validity, history, completion markers or prior versions. No
generic metadata map is available to smuggle such fields into the schema.

## Public ownership boundary

`VaultService::create(path, password, CreateOptions)` and `open(path, password)`
return `OpenVault`. Its operations are `save`, `lock`, `is_locked`,
`payload_mut`, `activity`, `timeout_token`, `expire`, `set_inactivity`, and
`set_storage_policy`. `CreateOptions` carries a label, storage policy and
inactivity choice. No API returns serialized plaintext, keys, whole phrases,
Spin validity or target columns. Crypto and serialization modules/functions
are private. Payload and Sheet types/fields are crate-private; `payload_mut`
returns a borrowed `PayloadEditor` without Deref, Default or ownership transfer.
Its current domain operations are `name()` and bounded `rename()`.
The next task can add narrow sheet operations inside this crate. Sensitive
model/key owners do not implement `Debug` or `Clone`.

Timeouts are 1/5/15/30 minutes, default 5. Tokens contain session identity,
generation and monotonic deadline. Activity and timeout changes invalidate
prior tokens; another session's token cannot lock the current session. Late
activity cannot revive an expired vault. Payload access and save check expiry
even if a UI timer was delayed. The host must call `lock()` immediately on OS
session lock/sleep and cover sensitive UI. Returned model borrows must remain
short-lived; the host must not keep a borrow across event-loop iterations.

Lock/drop destroy the owned payload and zeroizing KEK/DEK. Decrypted CBOR,
normalized passwords, temporary key buffers and the Argon2 workspace use
zeroizing owners. Unit tests inspect live zeroization and lock behavior; they
never read freed memory. This is best-effort memory hygiene, not protection
against OS/IME copies, normalization-library scratch space, process inspection,
paging, crash dumps, aborts or caller-owned string copies.

## Error categories

`Authentication` always displays: “The password is incorrect or the vault is
damaged.” This covers wrong passwords, wrap/payload AEAD failures and malformed
authenticated CBOR. A proved unsupported payload discriminator and an open
unsupported envelope version return `UnsupportedVersion`. Invalid magic,
algorithm identifiers or equal nonces return `InvalidHeader`. Unsupported KDF,
out-of-bounds KDF, truncated file, excessive size, invalid password input,
creation-password policy, insufficient space, access/sharing denial, invalid
path, existing target, unsupported filesystem, locked state and other I/O
have distinct safe categories. No failure becomes an empty vault.

`TemporaryRemains { cause, path }` reports an owned encrypted temp image if
best-effort cleanup fails. `path: Some(...)` is queried from the owned handle
after cleanup failure, so a concurrent rename does not report a stale creation
name. `None` explicitly means the OS could not resolve a current name. Display
omits the path; the UI may present it with the version-comparison warning, but
must not infer a missing name or blindly delete it later by pathname.

## Storage capability and observed evidence

The format/crypto/model/session do not impose NTFS semantics. A separate
Windows path backend implements the alpha persistence capability. Policy
defaults to `ReadOnly`, including every `open()`. Engineering callers must
explicitly select `DevelopmentLocalNtfs` for creation/save. They must select a
provisioned ordinary local development directory, not a cloud-synchronized
folder; the core cannot identify every third-party synchronization agent.
The backend checks the resolved parent volume is `DRIVE_FIXED` and NTFS;
other filesystem/device classes and non-Windows writers fail closed with
`UnsupportedFilesystem`. Future tested backends need not change the format.

Save creates a random adjacent `.tessaveil-alpha-*.tmp` via exclusive creation,
with read/write/DELETE access and `FILE_FLAG_WRITE_THROUGH`, writes **only**
header and ciphertext, flushes and `sync_all`s. The owner denies write sharing
and stays open. `ReOpenFile` obtains a read view of that same file object for
complete structural/AEAD/schema verification. Replacement uses the owner handle
with `SetFileInformationByHandle(FileRenameInfo)`; replace-if-exists is false
for creation. It has no cross-volume copy fallback. Cleanup, including Drop,
uses that same handle with `FileDispositionInfo`, never an old pathname.
These APIs address the open file object even when another participant renames
the temp and places a different file under its former name.
[Microsoft API contracts](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-setfileinformationbyhandle),
[identity-preserving reopen](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-reopenfile).

Sharing permits rename/delete, and the regression tests exercise actual name
substitution. Only the verified object reaches the target; the substituted file
is neither committed nor cleaned. Failed pre-replacement operations retain the
previous target and mark only the owned object for deletion. A cleanup failure
returns `TemporaryRemains` instead. Nothing after successful replacement can
turn success into a failed-save result. The new handle-based rename protocol
does **not** claim a write-through metadata barrier or power-loss durability;
the explicit write-through/flush guarantee applies to the image contents.

Evidence: Windows 11 Pro 10.0.26200, development fixed NTFS volume; successful
same-directory replacement, injected failures before write/after write/after
flush/after verification/before replace, deliberately corrupted temp-image
verification, actual Windows sharing-denial replacement failure, source-name
substitution before replace/error cleanup, and a renamed read-only owned temp
whose failed cleanup reports its current handle-derived path. Tests use
owned temporary directories and synthetic values only. This evidence does not
establish crash/power-loss durability, clean Windows 10/11 behavior, removable
NTFS/exFAT, FAT32, network-share or cloud-folder guarantees. No secure-erasure
or rollback-detection claim is made. Interrupted encrypted temp images can
preserve another table version and expose unchanged words after later password
disclosure, just as manually retained old backups can.

## Dependencies and verification

Direct exact pins: Argon2 0.5.3 (default PHC/password-hash features disabled,
zeroize enabled); chacha20poly1305 0.10.1; getrandom 0.2.16; zeroize 1.8.1 with
derive; unicode-normalization 0.1.24; test-only tempfile 3.23.0; Windows-only windows-sys
0.61.2 with Foundation/FileSystem. OS entropy supplies all cryptographic random
bytes. There are no network, GUI, clipboard, export or telemetry dependencies
in the core. The root workspace excludes all disposable spike crates.

`Cargo.lock` locks every transitive version and registry checksum. The adjacent
`core-dependencies.md` records the exact metadata license inventory. This is an
engineering inventory, not the final release SBOM, notices bundle or independent
dependency audit. Required local checks are `cargo fmt --check`,
`cargo clippy --locked --all-targets -- -D warnings`,
`cargo test --locked --all-targets`, `python tools/run_tests.py`, and both
repository/history sensitive-material scanners. Use the existing Windows
environment helper and an external ASCII `CARGO_TARGET_DIR`; the GNU linker
cannot reliably link artifacts in the Unicode worktree path. Do not commit
local toolchain/cache paths or generated binaries.
