# ADR 0002 — Envelope and KDF remain provisional

Date: 2026-09-29. Format freeze: NO-GO. KDF freeze: NO-GO.
Decision status: provisional / blocked. Windows release readiness: NO-GO.

The [Task 6 report](../../reports/spikes/mobile-kdf.md) records authored Rust and
native adapter contracts, literal normalization vectors and the physical matrix.
Following explicit permission for an isolated toolchain, Rust 1.90.0 Windows GNU
now builds/tests successfully with Cargo.lock. The 172-byte synthetic binary is
generated and independently opened using rust-argon2 3.0.0 and Orion 0.17.11; its
SHA-256 is recorded in the report. Nine Rust tests pass, including normalization,
bounds, corrupted authentication and independent crypto checks. There is still
no native Android/iOS build or physical measurement. Host tests cannot clear those
gates. Task 5 also left desktop selection blocked.

Retain Argon2id v19 64 MiB / 3 / 4 as the sole provisional allowlisted candidate.
Absolute encoding bounds are 64–256 MiB, 3–6 iterations, parallelism 1–8, fixed
32-byte output and 16-byte salt. Reject out-of-bounds values before password
processing/KDF allocation; distinguish unsupported in-bound profiles from wrong
password/authentication failure. Never clamp parameters or lower the candidate.
NFC UTF-8 remains authoritative in Rust, with explicit-length native input and
embedded-NUL rejection. No native normalization path is permitted.

The disposable `TVSPIKE0` layout is not a frozen `.tessaveil` format. Its immutable
header prefix authenticates DEK wrapping; its full header authenticates the payload.
Only a fixed synthetic CBOR marker is supported. Deterministic test keys/nonces are
not production key generation. Direct library pins/provenance/license notes are in
the report; transitive versions/checksums are locked and a metadata/license-file
inventory covers runtime/build closure and test dependencies. Full legal/security
and SignPath reviews remain pending. No third-party source/binary is bundled in Git.

Exact Task 4 blockers:

- No present portable-device entry; adb unavailable. No physical device identity, arm64 architecture, or 4 GiB RAM evidence was supplied.
- No present portable-device entry; adb unavailable. No current mid-range physical Android model or access evidence was supplied.
- No present portable-device entry and no accessible Mac/Xcode host; physical iPhone class and access were not supplied.
- No present portable-device entry and no accessible Mac/Xcode host; current physical iPhone class and access were not supplied.
- Current host is Windows; local Xcode command-line tools are absent and no configured Mac/Xcode host access was supplied.

Host pinned/locked builds, independent shared-fixture checks and Rust tests are now
available evidence. Reopen the freeze decision only after native builds and native
byte-equivalence/authentication tests, and measured reliable opening
on all four required physical classes. Record repeated duration, true process peak
memory, OOM/failure, thermal observations, hardware/OS and exact core/library revision.
Simulators and CI can establish compilation only, never physical acceptance.

An unavailable or failing required class keeps both freezes prohibited. Any target
exclusion or changed requirement requires a separate explicit owner/security
decision specifying the precise acceptance change, evidence, compatibility effect
and offline-guessing cost. Provisioning devices and satisfying the current profile
is the default path; an automatic cost reduction is not an alternative. Research
completion grants no release, product implementation or security exception.
