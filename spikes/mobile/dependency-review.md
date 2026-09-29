# Task 6 locked dependency inventory

Verified UTC: 2026-09-29. Scope: disposable probe and host-only tests.
Cargo.lock is the exact registry/version/checksum authority. `cargo metadata
--locked --format-version 1` supplied package identities, declared licenses and
upstream repositories; `cargo tree --locked --edges normal,build --target all`
identified the normal/build closure including target-specific dependencies.
There are 47 registry packages plus the original Apache-2.0 probe.

License headers/files were also inspected for all four runtime direct dependencies,
both independent crypto implementations, generic-array, subtle, tinyvec and
unicode-ident. This is a declared-license inventory and targeted text inspection,
not full legal clearance, vulnerability scanning, provenance attestation, complete
Unicode-data review or a security audit. Downloads live only in ignored Cargo cache;
no vendor sources or third-party binaries are committed/distributed.

## Runtime/build closure

Retain the chosen license and required notices for any future distribution.
Legacy `MIT/Apache-2.0` declarations below are preserved verbatim.

| Package | Version | Declared license |
| --- | --- | --- |
| aead | 0.5.2 | MIT OR Apache-2.0 |
| argon2 | 0.5.3 | MIT OR Apache-2.0 |
| base64ct | 1.8.3 | Apache-2.0 OR MIT |
| blake2 | 0.10.6 | MIT OR Apache-2.0 |
| block-buffer | 0.10.4 | MIT OR Apache-2.0 |
| cfg-if | 1.0.5 | MIT OR Apache-2.0 |
| chacha20 | 0.9.1 | Apache-2.0 OR MIT |
| chacha20poly1305 | 0.10.1 | Apache-2.0 OR MIT |
| cipher | 0.4.4 | MIT OR Apache-2.0 |
| cpufeatures | 0.2.17 | MIT OR Apache-2.0 |
| crypto-common | 0.1.7 | MIT OR Apache-2.0 |
| digest | 0.10.7 | MIT OR Apache-2.0 |
| generic-array | 0.14.7 | MIT |
| getrandom | 0.2.17 | MIT OR Apache-2.0 |
| inout | 0.1.4 | MIT OR Apache-2.0 |
| libc | 0.2.189 | MIT OR Apache-2.0 |
| opaque-debug | 0.3.1 | MIT OR Apache-2.0 |
| password-hash | 0.5.0 | MIT OR Apache-2.0 |
| poly1305 | 0.8.0 | Apache-2.0 OR MIT |
| rand_core | 0.6.4 | MIT OR Apache-2.0 |
| subtle | 2.6.1 | BSD-3-Clause |
| tinyvec | 1.13.3 | Zlib OR Apache-2.0 OR MIT |
| typenum | 1.20.1 | MIT OR Apache-2.0 |
| unicode-normalization | 0.1.24 | MIT/Apache-2.0 |
| universal-hash | 0.5.1 | MIT OR Apache-2.0 |
| version_check (build) | 0.9.5 | MIT/Apache-2.0 |
| wasi (target-specific) | 0.11.1+wasi-snapshot-preview1 | Apache-2.0 WITH LLVM-exception OR Apache-2.0 OR MIT |
| zeroize | 1.8.1 | Apache-2.0 OR MIT |

Direct primary sources: [RustCrypto Argon2 0.5.3](https://docs.rs/argon2/0.5.3/argon2/),
[XChaCha20-Poly1305 0.10.1](https://docs.rs/chacha20poly1305/0.10.1/chacha20poly1305/),
[Unicode normalization v0.1.24 manifest](https://github.com/unicode-rs/unicode-normalization/blob/v0.1.24/Cargo.toml)
and [zeroize 1.8.1](https://docs.rs/crate/zeroize/1.8.1). Exact research pins do not
claim latest versions or release approval. Unicode generated data needs separate
complete notice review before bundling.

## Additional test/resolution-only packages

These are not new runtime crypto dependencies. Cargo.lock includes optional
resolution packages: presence in the lock does not imply compilation on this host.

| Package | Version | Declared license |
| --- | --- | --- |
| arrayvec | 0.7.8 | MIT OR Apache-2.0 |
| base64 | 0.22.1 | MIT OR Apache-2.0 |
| blake2b_simd | 1.0.5 | MIT |
| constant_time_eq | 0.4.2 | CC0-1.0 OR MIT-0 OR Apache-2.0 |
| crossbeam-utils | 0.8.23 | MIT OR Apache-2.0 |
| fiat-crypto | 0.3.0 | MIT OR Apache-2.0 OR BSD-1-Clause |
| itoa | 1.0.18 | MIT OR Apache-2.0 |
| memchr | 2.8.3 | Unlicense OR MIT |
| orion | 0.17.11 | MIT |
| proc-macro2 | 1.0.107 | MIT OR Apache-2.0 |
| quote | 1.0.47 | MIT OR Apache-2.0 |
| rust-argon2 | 3.0.0 | MIT/Apache-2.0 |
| ryu | 1.0.23 | Apache-2.0 OR BSL-1.0 |
| serde | 1.0.229 | MIT OR Apache-2.0 |
| serde_core | 1.0.229 | MIT OR Apache-2.0 |
| serde_derive | 1.0.229 | MIT OR Apache-2.0 |
| serde_json | 1.0.145 | MIT OR Apache-2.0 |
| syn | 3.0.6 | MIT OR Apache-2.0 |
| unicode-ident | 1.0.26 | (MIT OR Apache-2.0) AND Unicode-3.0 |

Independent primitive sources: [SRU Systems rust-argon2 3.0.0](https://docs.rs/rust-argon2/3.0.0/argon2/struct.Config.html)
(upstream `sru-systems/rust-argon2`, copyright Martijn Rijkeboer, separate BLAKE2b
implementation) and [Orion 0.17.11 manifest](https://github.com/orion-rs/orion/blob/0.17.11/Cargo.toml)
with [AEAD source](https://github.com/orion-rs/orion/blob/0.17.11/src/hazardous/aead/xchacha20poly1305.rs)
(copyright 2018–2025 Orion Developers, MIT, fiat-crypto Poly1305). Exact archive
checksums are in Cargo.lock. These are separately maintained from RustCrypto;
shared zeroize/subtle utilities and one compiler/host limit independence.
Test-only [serde_json 1.0.145](https://docs.rs/crate/serde_json/1.0.145) reads vector data.

No missing declared license was found. MIT notices, Apache license/NOTICE handling,
BSD-3-Clause conditions and additional Unicode-3.0 terms cannot be replaced by the
repository Apache license. Full file-level review, attribution bundle, SBOM,
vulnerability review and SignPath compatibility decision remain pending before any
binary/source bundling or release. This inventory is not distribution approval.
