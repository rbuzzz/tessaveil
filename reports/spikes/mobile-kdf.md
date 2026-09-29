# Mobile vault/KDF feasibility — Task 6

Verified (UTC): 2026-09-29. Format freeze: NO-GO. KDF freeze: NO-GO.
Result: source contracts and blocked evidence; no physical compatibility claim.
Baseline: `c028d0419b95411fa272003b98ef38cceba29cbc` on
`feature/tessaveil-research-foundation`, origin `git@github.com:rbuzzz/tessaveil.git`.

## Implemented scope and actual evidence

The [disposable Rust source](../../spikes/mobile/core/src/lib.rs) specifies bounded
parsing, pre-KDF profile rejection, Rust NFC UTF-8, Argon2id, wrapped DEK and
authenticated synthetic CBOR through `probe_open_vault`. Kotlin/JNI and Swift
source adapters pass explicit byte lengths and return only status/duration/memory.
They contain no native normalization or password persistence. Neither adapter is
a complete app/build project; secure UI and lifecycle integration remain pending.

Read-only discovery found rustc/cargo/rustup/adb/xcodebuild/xcrun/gradle/java/swift/
clang absent from PATH; standard Cargo compiler/executable locations also absent.
No configured alternate toolchain was supplied. This is bounded discovery, not
proof that no installation exists anywhere. No toolchain was installed, VM or
emulator launched, device contacted, remote target used or package fetched.

Rust/Cargo execution, native platform compilation and runtime tests: BLOCKED.
There is no generated Cargo.lock, resolved transitive tree, compiler version or
artifact hash. Direct pins do not prove a locked or reproducible build.
No physical wall time, process peak memory, OOM/failure or thermal result exists.
The core's memory sentinel and JSON null values mean unmeasured, not zero cost.

The repository contract test was first observed RED with four missing-artifact
failures. Its later GREEN result checks data/report contracts only. Python checks
literal Unicode fixture bytes independently with its standard normalization
library; it is not a vault implementation and does not establish Rust/native NFC
agreement. Rust behavioral tests were authored first but could not run RED/GREEN.

## Cryptographic fixture blocker

`synthetic-vault-v0.bin`: BLOCKED, intentionally absent. Rust/Cargo is unavailable,
so the source generator has not executed. No independently verified cryptographic
fixture or expected ciphertext has been obtained. Local Python library discovery
found PyNaCl/cryptography but no argon2 module; no Python crypto code was used and
no inference of an exact lanes=4 interoperable fixture is made. A source generator
plus same-library round trip is not independent verification.

The [fixture status](../../spikes/mobile/vectors/fixture-status.json) explicitly
records null SHA-256 and false Rust/independent execution flags. Do not create a
placeholder, random byte blob, plaintext `.bin`, or claim that the planned file was
opened. Before promotion, generate it with Rust, independently verify the exact
Argon2id and both XChaCha20-Poly1305 layers with pinned licensed tooling, record
known-answer evidence and hash, then replay unchanged bytes on both native hosts.

## Physical candidate matrix

Candidate set contains only the specification's provisional 64 MiB / 3 / 4 tuple;
no alternative cost was selected or implicitly weakened. The following table
applies to that candidate. Each missing measurement is explicitly unknown.

| Required class | Model / OS | Open / NFC match | Wall time / peak memory | OOM / failure / thermal | Result |
| --- | --- | --- | --- | --- | --- |
| physical arm64 Android 4 GiB lower-bound | unknown / unknown | unmeasured / unmeasured | unmeasured / unmeasured | unmeasured / unmeasured / unmeasured | BLOCKED: A1 |
| current mid-range physical Android | unknown / unknown | unmeasured / unmeasured | unmeasured / unmeasured | unmeasured / unmeasured / unmeasured | BLOCKED: A2 |
| physical iPhone 11/A13/4 GiB-class lower-bound | unknown / unknown | unmeasured / unmeasured | unmeasured / unmeasured | unmeasured / unmeasured / unmeasured | BLOCKED: I1 |
| current physical iPhone | unknown / unknown | unmeasured / unmeasured | unmeasured / unmeasured | unmeasured / unmeasured / unmeasured | BLOCKED: I2 |
| Mac/Xcode host | unknown / unknown | build unverified | not a physical benchmark | not applicable | BLOCKED: M |

Exact blockers copied from [Task 4](equipment-availability.md):

- A1: No present portable-device entry; adb unavailable. No physical device identity, arm64 architecture, or 4 GiB RAM evidence was supplied.
- A2: No present portable-device entry; adb unavailable. No current mid-range physical Android model or access evidence was supplied.
- I1: No present portable-device entry and no accessible Mac/Xcode host; physical iPhone class and access were not supplied.
- I2: No present portable-device entry and no accessible Mac/Xcode host; current physical iPhone class and access were not supplied.
- M: Current host is Windows; local Xcode command-line tools are absent and no configured Mac/Xcode host access was supplied.

No simulator, developer desktop, macOS runner or CI build substitutes for any
physical row. Task 5's constant-call contracts do not establish vault interoperability.

## Provisional policy, provenance and license review

Absolute encoded bounds remain 64–256 MiB / 3–6 / 1–8, output 32 bytes, salt 16
bytes. Outside bounds rejects before password processing/KDF; in-bound tuples
outside the single allowlist return UnsupportedProfile, never AuthenticationFailed
and never clamped. Wrong password and authentication corruption share one class.
NFC is performed only in Rust. Vectors cover composed/decomposed, reordered combining
marks, Cyrillic, Japanese, non-BMP, empty normalization and embedded-NUL rejection.

Primary references inspected on 2026-09-29 UTC; these are exact source/API planning
pins, not installed, independently audited or release-approved libraries:

| Dependency / reference | Exact pin and primary provenance | License / disposition |
| --- | --- | --- |
| RustCrypto Argon2 | [argon2 0.5.3](https://docs.rs/argon2/0.5.3/argon2/) | MIT OR Apache-2.0; planned Apache-2.0 option, transitive audit pending |
| RustCrypto XChaCha20-Poly1305 | [chacha20poly1305 0.10.1](https://docs.rs/chacha20poly1305/0.10.1/chacha20poly1305/) | MIT OR Apache-2.0; planned Apache-2.0 option, transitive audit pending |
| Unicode NFC | [unicode-normalization v0.1.24 manifest](https://github.com/unicode-rs/unicode-normalization/blob/v0.1.24/Cargo.toml) | MIT/Apache-2.0; upstream Unicode data and tinyvec review pending |
| RustCrypto zeroization | [zeroize 1.8.1](https://docs.rs/crate/zeroize/1.8.1) | MIT OR Apache-2.0; planned Apache-2.0 option |
| Test-only JSON reader | [serde_json 1.0.145](https://docs.rs/crate/serde_json/1.0.145), [Apache license](https://docs.rs/crate/serde_json/1.0.145/source/LICENSE-APACHE) | Apache-2.0 option; development-only |
| Provisional Argon2id profile | [RFC 9106](https://www.rfc-editor.org/rfc/rfc9106), section 4 | 64 MiB / 3 / 4 recommendation; device feasibility still unmeasured |
| JNI byte boundary | [Oracle JNI types, JDK 8](https://docs.oracle.com/javase/8/docs/technotes/guides/jni/spec/types.html) | JNI strings use modified UTF-8; source contract uses byte arrays |
| Swift UTF-8 view | [Apple String.UTF8View](https://developer.apple.com/documentation/swift/string/utf8view) | Standard UTF-8 view; deployment toolchain remains unselected |

No third-party source or binary was copied/bundled; original probe source remains
Apache-2.0. Before distribution: resolve/lock all dependencies, review notices,
vulnerabilities and Unicode data licenses, add full attribution/SBOM and obtain the
separate SignPath compatibility decision. No final license or signing approval is
claimed. Exact pins are research candidates, not a claim they are latest versions.

## Decision and reopening

The [ADR](../../docs/adr/0002-kdf-envelope-bounds.md) retains format/KDF NO-GO.
Provision a Rust toolchain and both native build hosts, produce/independently verify
the fixture, pass Rust/native vectors and collect all four physical device results.
Record fixture hash, core commit, locked library revisions, model/OS, repeated
wall time, process peak memory, OOM/failure and thermal evidence for each candidate.
Then conduct security review before changing the freeze decision.

If a required target cannot reliably run 64 MiB / 3 / 4, stop and obtain a separate
owner/security decision: explicitly exclude/change that target acceptance criterion
or approve a revised format/KDF security design with measured offline-guessing and
compatibility consequences. No exclusion, lower profile or freeze is authorized by
this blocked research result. Windows release readiness remains NO-GO.
