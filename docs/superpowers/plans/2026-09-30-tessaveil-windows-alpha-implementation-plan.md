# Tessaveil Windows Alpha Implementation Plan

> **For Codex:** execute this plan with `superpowers:subagent-driven-development`. One implementer and one fresh reviewer per task; tasks, commits, pushes, manifest/generated-document edits and `main` integration are sequential.

**Goal:** deliver a runnable synthetic-data-only Windows alpha as one `Tessaveil.exe` that creates, saves, closes and reopens an encrypted vault; manages protected 10/36-column sheets; performs Spin without a validity signal; locks on inactivity; and rejects corruption safely.

**Architecture:** a Rust workspace provides a GUI-independent security/domain core and a thin Windows UI selected only after reproducible candidate builds. The alpha vault uses a deliberately provisional `.tessaveil-alpha` envelope and pinned KDF profile; it has no migration promise and cannot freeze the future `.tessaveil` format. Catalogue-derived selectable profiles are generated from terminal `verified` records only.

**Tech Stack:** pinned Rust/Cargo; XChaCha20-Poly1305, Argon2id, canonical CBOR, `zeroize`; the Windows GUI stack is chosen by Task 1 from real Avalonia NativeAOT, Slint and static Qt evidence; GitHub Actions Windows artifact; CycloneDX or SPDX SBOM.

**Approved specification:** `docs/superpowers/specs/2026-09-29-tessaveil-foundation-windows-v1-design.md`

## Non-negotiable alpha boundary

- Use only synthetic test words, passwords and vaults. Never enter or process a real seed, private key, wallet backup or production vault.
- Never construct, return, persist, log or validate a whole recovery phrase, ordering key, target column or Spin-validity flag.
- Expose only catalogue profiles whose wallet, scheme, dictionary, licensing and signing decisions are all `verified`. The initial selectable matrix is exactly `mytonwallet-native/ton-native-generated`, `tonhub/ton-native-generated`, and `tonkeeper-classic/ton-native-generated`; everything else is shown as unavailable, not silently omitted or guessed.
- The only alpha extension is `.tessaveil-alpha`; `.tessaveil`, the KDF defaults and the cross-platform format remain unfrozen until physical Android/iPhone evidence exists. Excessive-but-bounded KDF profiles fail before allocation.
- No network, telemetry, clipboard copy, plaintext export, phrase import, phrase assembly or automatic dictionary migration.
- Atomic-save claims are limited to the tested dev-host filesystem. Clean Windows 10/11, physical Android/iPhone, removable-media interruption, independent security audit and signing remain explicit release blockers.
- Every production behavior follows red-green-refactor: add a behavior test, run it and record the expected failure, add the minimum implementation, then run the focused and full affected suites.

## Review focus

1. Reject malformed/truncated files and KDF bounds before large allocation; wrong password and authenticated-payload damage share one outward error.
2. Spin returns a replacement row only; valid and invalid inputs expose the same API/state transition and persist no target, candidate or validity metadata.
3. Inactivity lock zeroizes decrypted session material and blocks stale timers/events from reopening or mutating a vault.
4. Dictionary changes create a new unverified sheet with a new immutable snapshot; prior verification never transfers.
5. Failed saves preserve the previous authenticated vault; temporary files contain only an open technical header and ciphertext.

## Task 1: Build and measure the Windows candidates, then select the stack

**Files**

- Modify: `spikes/windows/probe-contract.json`
- Create: `spikes/windows/avalonia-nativeaot/**`
- Create: `spikes/windows/slint/**`
- Create: `spikes/windows/qt-static/**`
- Modify: `reports/spikes/windows.md`
- Modify: `docs/adr/0001-desktop-stack.md`
- Modify: `tests/repository/test_windows_spike_report.py`

**Steps**

1. Add a failing report-contract test requiring exact toolchain versions, commands, artifact inventory, byte sizes, startup measurements, PE imports, temporary-file before/after observation and blocker text for every candidate.
2. Install pinned tools only in an isolated/user ASCII path outside the repository; record versions and hashes, never machine-specific paths.
3. Build equivalent minimal dense-table/keyboard probes for Avalonia NativeAOT, Slint and static Qt. A failed build is evidence only after the exact failure is captured; it is not scored as zero.
4. Measure every feasible candidate with the same script and synthetic data. Do not count this dev host as a clean Windows result.
5. Update the report and ADR with the measured winner and explicit rejected/blocked alternatives; run the focused test, `python tools/run_tests.py`, and any candidate-native tests.
6. Commit: `research: select measured Windows alpha stack`.

## Task 2: Implement the provisional encrypted-vault core

**Files**

- Create: `Cargo.toml`, `Cargo.lock`, `rust-toolchain.toml`
- Create: `crates/tessaveil-core/Cargo.toml`
- Create: `crates/tessaveil-core/src/{lib,error,format,kdf,crypto,model,store,session}.rs`
- Create: `crates/tessaveil-core/tests/{format_contract,vault_roundtrip,corruption,atomic_save,session_lock}.rs`
- Create: `docs/alpha/vault-format.md`

**Public boundary**

- `VaultService::create(path, password, CreateOptions) -> Result<OpenVault, VaultError>`
- `VaultService::open(path, password) -> Result<OpenVault, VaultError>`
- `OpenVault::{save,lock,payload_mut}`; no API returns serialized plaintext or a whole phrase.

**Steps**

1. RED: tests for the alpha magic/version, NFC UTF-8 password normalization, embedded-NUL rejection, Argon2id bounds, independent wrap/payload nonces and AAD, canonical-CBOR bounds, round-trip and outward error taxonomy.
2. GREEN: implement a bounded open header plus authenticated ciphertext using pinned Argon2id and XChaCha20-Poly1305 dependencies; lock the dependency graph.
3. RED/GREEN: corrupt every header/ciphertext region and every truncation boundary; prove allocation limits are checked first and authentication failures are indistinguishable.
4. RED/GREEN: write-through temporary header+ciphertext, flush, reopen/authenticate the complete temporary image, then replace; failure leaves the old vault intact.
5. RED/GREEN: inactivity session state supports 1/5/15/30 minutes (default 5), rejects stale timeout tokens and zeroizes secrets on lock/drop.
6. Run `cargo fmt --check`, `cargo clippy --locked --all-targets -- -D warnings`, `cargo test --locked --all-targets`, and `python tools/run_tests.py`.
7. Commit: `feat: add provisional encrypted alpha vault core`.

## Task 3: Implement catalogue projection, sheets and Spin

**Files**

- Create: `tools/alpha_catalog.py`
- Create: `generated/alpha/profile-matrix.json`
- Modify: `crates/tessaveil-core/src/{catalog,sheet,spin,model}.rs`
- Create: `crates/tessaveil-core/tests/{catalog_gate,sheet_contract,spin_contract}.rs`
- Modify: `tests/catalog/test_generation.py`

**Steps**

1. RED/GREEN: generate the alpha matrix from catalogue state; fail closed if any dependency/status/license changes. Assert exactly the three approved profile/mode identities are selectable and all other terminal records carry an unavailable reason.
2. RED/GREEN: create only 10- or 36-column sheets with supported row lengths, CSPRNG-generated decoys and an immutable dictionary snapshot.
3. RED/GREEN: sheet protection uses a salted verifier; `Verified by me` is explicit state. A dictionary change produces a new unverified sheet and never rewrites an existing sheet.
4. RED/GREEN: `spin_row(request, rng) -> Result<ReplacementRow, SpinError>` accepts the two-symbol/word input but returns only the full replacement row. Valid/invalid candidates follow the same public transition and persist no candidate, target or result flag.
5. Run generator drift checks, Rust tests and the full Python suite.
6. Commit: `feat: add verified alpha profiles sheets and spin`.

## Task 4: Build the Windows alpha UI and lifecycle

**Files**

- Create: `apps/tessaveil-windows/**`
- Create: `apps/tessaveil-windows/tests/**`
- Create: `docs/alpha/user-guide.md`

**Steps**

1. RED: controller/view-model tests for first-run warning, create/open/save/close/reopen, password/authentication failure, corruption messages, profile availability, 10/36 columns, sheet protection, Spin, lock/unlock and default inactivity timeout.
2. GREEN: implement the smallest UI over `tessaveil-core`; keep decrypted state in one session owner and never bind a full phrase or ordering key into the UI.
3. Add keyboard navigation, readable focus, scaling and dense-table behavior established by Task 1. Disable clipboard/export/import and network-capable features.
4. Exercise the synthetic happy path and each error state on the dev host; save screenshots and a bounded manual observation report without upgrading clean-machine evidence.
5. Run native UI tests, all Rust tests and the full Python suite.
6. Commit: `feat: add Tessaveil Windows alpha workflow`.

## Task 5: Package, attest and publish the alpha candidate

**Files**

- Create/Modify: `.github/workflows/windows-alpha.yml`
- Create: `packaging/windows/**`
- Create: `docs/alpha/release-evidence.md`
- Create: `docs/alpha/known-limitations.md`
- Create: `THIRD_PARTY_ALPHA.md`

**Steps**

1. RED/GREEN: repository tests require a Windows build on the exact commit, one `Tessaveil.exe` runtime artifact, locked dependencies, SBOM, third-party notices, SHA-256 manifest and an artifact-content check rejecting plaintext/synthetic fixture leakage.
2. Build release mode and run a synthetic end-to-end test: create vault, add/protect sheet, Spin, save, close, reopen, lock, and reject a corrupted copy.
3. Record EXE size/hash, PE imports, runtime dependencies, temporary-file observation and launch instructions. State prominently: unsigned Windows alpha, not RC/stable; no format/KDF migration promise.
4. Run secret/history scanners, generated/notices checks, Rust format/lint/tests, full Python suite and the exact local alpha gate.
5. Push `feature/windows-alpha`, wait for exact-SHA branch and PR CI, attach the workflow artifact, and open a PR to `main`. Do not create an RC/stable GitHub Release and do not merge without the owner's next release decision.
6. Commit: `build: package Tessaveil Windows alpha`.

## Acceptance evidence

- Exact source SHA, PR URL and successful exact-SHA CI runs.
- Downloadable `Tessaveil.exe`, SHA-256, SBOM, third-party notices and launch instructions.
- Passing synthetic round-trip/corruption/Spin/sheet-protection/inactivity-lock tests.
- Measured stack decision and dependency/runtime inventory.
- Known limitations preserving `NO-GO` for RC/stable, clean Windows, physical mobile, removable-media, audit, signing and final vault/KDF freeze.
