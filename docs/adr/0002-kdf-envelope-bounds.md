# ADR 0002 — Envelope and KDF remain provisional

Date: 2026-09-29. Format freeze: NO-GO. KDF freeze: NO-GO.
Decision status: provisional / blocked. Windows release readiness: NO-GO.

The [Task 6 report](../../reports/spikes/mobile-kdf.md) records authored Rust and
native adapter contracts, literal normalization vectors, unavailable toolchains and
the physical matrix. There is no executed Rust build, native build, independently
verified cryptographic binary fixture or physical measurement. Passing repository
contract tests cannot clear those gates. Task 5 also left desktop selection blocked.

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
the report; transitive lock, independent cryptographic validation, full license and
SignPath reviews are pending. No third-party implementation is bundled.

Exact Task 4 blockers:

- No present portable-device entry; adb unavailable. No physical device identity, arm64 architecture, or 4 GiB RAM evidence was supplied.
- No present portable-device entry; adb unavailable. No current mid-range physical Android model or access evidence was supplied.
- No present portable-device entry and no accessible Mac/Xcode host; physical iPhone class and access were not supplied.
- No present portable-device entry and no accessible Mac/Xcode host; current physical iPhone class and access were not supplied.
- Current host is Windows; local Xcode command-line tools are absent and no configured Mac/Xcode host access was supplied.

Reopen only after pinned/locked builds, independently checked shared fixture/hash,
Rust and native byte-equivalence/authentication tests, and measured reliable opening
on all four required physical classes. Record repeated duration, true process peak
memory, OOM/failure, thermal observations, hardware/OS and exact core/library revision.
Simulators and CI can establish compilation only, never physical acceptance.

An unavailable or failing required class keeps both freezes prohibited. Any target
exclusion or changed requirement requires a separate explicit owner/security
decision specifying the precise acceptance change, evidence, compatibility effect
and offline-guessing cost. Provisioning devices and satisfying the current profile
is the default path; an automatic cost reduction is not an alternative. Research
completion grants no release, product implementation or security exception.
