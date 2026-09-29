# Synthetic mobile KDF probe — source contract, not a product

Format freeze: NO-GO. KDF freeze: NO-GO. Execution/build evidence: BLOCKED.
The [report](../../reports/spikes/mobile-kdf.md) and
[ADR](../../docs/adr/0002-kdf-envelope-bounds.md) distinguish available repository
checks from unavailable Rust, native builds, crypto fixture and physical evidence.

`core` contains a Rust implementation candidate and unexecuted behavioral tests.
`android` and `ios` contain explicit-length adapter source contracts, not complete
platform build projects. No APK, IPA, product UI or production vault is delivered.
Every input is invented synthetic data. Never use a real password, phrase or vault.

## Narrow interface and error contract

`probe_open_vault(bytes: &[u8], password_utf8: &[u8]) -> ProbeResult` returns only
status class, elapsed microseconds and an unmeasured-memory sentinel. A matching
C ABI is defined in `include/tessaveil_probe.h`; callers keep buffers alive for the
synchronous call. `memory_bytes == UINT64_MAX` (JNI `-1`) is unknown, never a peak
measurement or Argon2 memory budget. The adapters display those three fields only.

Status values: 0 success, 1 invalid envelope, 2 unsupported version, 3 unsupported
algorithm, 4 KDF out of absolute bounds, 5 unsupported in-bound profile, 6 invalid
UTF-8, 7 embedded NUL, 8 password too long, 9 password too short, 10 wrong password
or failed authentication, 11 unsupported synthetic payload, 12 internal error,
13 invalid FFI argument. An error never becomes a successful empty vault.

The only allowlisted profile is provisional Argon2id v19: 65536 KiB / 3 / 4.
Absolute encoding bounds: 65536–262144 KiB, iterations 3–6, parallelism 1–8,
32-byte output and 16-byte salt. Bounds and allowlist checks precede password
decoding, normalization and KDF allocation. No clamping or fallback profile exists.
NFC UTF-8 is authoritative inside Rust; wrappers only encode Unicode and pass byte
lengths. Normalization vectors include empty input; unlocking separately rejects
fewer than 15 Unicode scalar values after NFC. Maximum input/output UTF-8 is 1024
bytes, supporting at least 64 characters. This is not the future common-password
filter or a completed production password policy.

## Disposable envelope v0

All integer fields are little-endian. This layout is not `.tessaveil` v1 and is not
frozen. A 4096-byte file bound applies before parsing/heap allocation.

| Byte offset | Size | Field |
| --- | --- | --- |
| 0 | 8 | `TVSPIKE0` |
| 8 | 2 | Version 0 |
| 10 | 1 + 1 | Argon2id and XChaCha20-Poly1305 IDs, both 1 |
| 12 | 4 + 4 + 4 | KiB, iterations, parallelism |
| 24 | 2 + 2 | Output length 32, salt length 16 |
| 28 | 16 | Public synthetic salt |
| 44 | 24 | DEK-wrap nonce |
| 68 | 24 | Payload nonce (separate) |
| 92 | 4 | Ciphertext length including its 16-byte tag |
| 96 | 48 | 32-byte DEK plus wrapping authentication tag |
| 144 | bounded | Ciphertext plus payload authentication tag |

Bytes 0–95 are DEK-wrap AAD. Bytes 0–143 (including wrapped DEK) are payload AAD.
Only an authenticated canonical CBOR `{ "synthetic": true }` marker is accepted.
No generic CBOR parser, table schema, mnemonic processing, file-save routine or
production RNG is implemented. Test construction uses deliberately public fixed
salt, DEK and distinct nonces; production creation must never reuse this recipe.
Rust clears its owned normalized buffer/keys/plaintext best-effort. Wrapper/OS
copies, allocator internals and process termination/OOM remain limitations.

## Reproduction after toolchains become available

Current commands below are instructions, not recorded successful executions.
Review exact direct dependency pins and resolve/audit transitive dependencies,
then generate and commit a Cargo.lock and record the exact Rust compiler/targets.

1. Run `cargo check --manifest-path spikes/mobile/core/Cargo.toml --all-targets`.
2. Run `cargo run --manifest-path spikes/mobile/core/Cargo.toml --example fixture`.
   It creates a candidate `vectors/synthetic-vault-v0.bin` without overwriting an
   existing file. No binary is currently committed: see `fixture-status.json`.
3. Independently derive the KEK at the exact tuple and decrypt both layers using a
   separately maintained implementation; record tool/library pins, licenses, known
   answer validation, fixture SHA-256 and expected plaintext. A Rust self-generated
   round trip alone is insufficient. Do not mark the fixture verified until this passes.
4. Run `cargo test --manifest-path spikes/mobile/core/Cargo.toml`. The shared-file
   test deliberately fails if the binary is absent; no ignored success substitutes.
   Tests cover normalized equivalence, NUL/invalid UTF-8/empty/limits, bounds before
   KDF, distinct unsupported in-bound profiles, corrupted authenticated regions,
   format bounds and FFI null/length checks. They have not executed here.
5. Complete the two disposable native build hosts described in their READMEs,
   build both, verify ABI/statuses and replay shared vectors through each wrapper.
6. Run the exact same fixture/hash on all four required physical classes. For the
   sole candidate 64 MiB / 3 / 4 collect cold/warm repeated wall-time, process peak
   memory (with method/baseline), OOM/failure, thermal state, hardware/OS/RAM/arm64,
   core commit and locked library revisions. Do not write normalized/secret bytes
   to device logs. Unknowns remain null. Failed targets keep freeze at NO-GO.

`python -m unittest tests.repository.test_mobile_spike_report -v` validates fixture
data, Cargo pins and honest report gates only. It does not compile or exercise Rust,
cryptography, JNI, Swift or a physical device. Python's normalization here is an
independent repository-level data check, never the product implementation.
