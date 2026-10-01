# Tessaveil Windows v1 Transition Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn the current synthetic Windows alpha into the most complete evidence-backed Windows v1 candidate possible in one pass, while keeping real-data use fail-closed until every mandatory external gate is proven on the exact candidate.

**Architecture:** Preserve the static Qt 6.8.3 presentation layer, narrow C ABI, and Rust-owned security/domain core. Extend the existing schema-2 engineering format without changing its interpretation; add product operations through explicit Rust APIs and controller operations, then expose them in Qt. A machine-readable release decision separates implementation completion from authorization to remove `synthetic only`.

**Tech Stack:** Rust 1.90.0, Argon2id, XChaCha20-Poly1305, static Qt Widgets 6.8.3, C ABI 1, PowerShell packaging, Python repository gates, GitHub Actions provenance.

**Spec:** `docs/superpowers/specs/2026-09-29-tessaveil-foundation-windows-v1-design.md`, constrained by `THREAT_MODEL.md`, `docs/superpowers/specs/2026-09-29-tessaveil-registry-threat-model-design.md`, and the owner request dated 2026-09-30.

## Global Constraints

- Use only invented synthetic fixtures and public standard vectors. Never accept, log, commit, transmit, or test a real phrase, order key, private key, funded-wallet backup, or user vault.
- Tessaveil never accepts or returns a complete phrase/order key, derives wallet material, checks balances, exports plaintext, or stores a Spin target/validity result.
- Every selectable profile is backed by terminal `verified` wallet, scheme, dictionary, evidence, license, and signing decisions. Import support never proves generation. Tonkeeper Multichain and Gram Wallet remain unavailable unless their existing evidence gaps are actually closed.
- The Qt UI must reject any individual input over 4,096 UTF-8 bytes before `tv_call`; the Rust ABI retains fatal fail-closed behavior for malformed foreign calls.
- Schema 2 and `.tessaveil-alpha` remain explicit engineering format identifiers unless this plan adds and tests a versioned migration. No silent reinterpretation, extension rename, KDF weakening, or format freeze is allowed.
- Existing-sheet dictionary snapshots are immutable. A changed custom dictionary creates a fresh unverified sheet with no inherited table, password, verification state, or row state.
- All writes use adjacent authenticated ciphertext images and preserve the prior valid file on failure. No unverified filesystem receives an atomicity claim.
- Tests, reviews, manifests, generated documents, commits, pushes, and PR updates are sequential. No two implementers edit the shared tree at once.
- `synthetic only` can be removed only by a machine-readable exact-candidate decision showing every clean-Windows, physical-mobile, removable-media, independent-audit, catalogue, signing, security, documentation, and supply-chain gate as passed. Missing evidence means `NO-GO`.
- Every behavior change follows RED → verified failure → minimal GREEN → focused tests → full affected suite → commit → independent task review.

## Review Focus

1. A user-originated UTF-8 size error must be recoverable and must preserve the live dirty session, table, previous file, and ability to save; only a malformed foreign ABI call destroys its controller.
2. Backup, restore, password change, RNG failure, and injected save failures must never replace a valid destination with unauthenticated or partial data.
3. Row-count and dictionary choices must follow the selected exact profile/mode snapshot; no hard-coded 24-word assumption or import-to-generation inference is allowed.
4. Explicit lock, inactivity, Windows session lock, sleep, ordinary application deactivation, and close must have distinct tested behavior for dirty state and sensitive controls.
5. UI copy, documentation, and the release-decision report must not imply that internal reviews, CI, a development host, a VM, or an unsigned artifact clears a physical or independent gate.

---

### Task 1: Preserve dirty sessions on oversized Unicode input

**Files:**
- Modify: `apps/tessaveil-windows/window.cpp`
- Modify: `apps/tessaveil-windows/tests/ui.cpp`
- Verify: `apps/tessaveil-windows/controller/tests/abi.rs`

**Interfaces:**
- Consumes: `TvInput` slots with a 4,096-byte capacity and fatal Rust ABI validation for foreign callers.
- Produces: a Qt-side `field`/`Secret::consume` result that prevents `tv_call` when UTF-8 does not fit and reports a recoverable localized validation error.

- [ ] **Step 1: Add the native failing regression**

  Create an unsaved synthetic sheet, snapshot its table digest and prior encrypted file, submit `QString(2049, QChar(0x044f))` as the sheet password, and assert that state remains `Open / unsaved changes`, rows/digest/file remain unchanged, an actionable size error appears, and a later short password plus Save still works.

- [ ] **Step 2: Run the native test and record RED**

  Run: `apps/tessaveil-windows/build.ps1 -ToolchainRoot C:\Users\Public\TessaveilToolchains -Test`

  Expected: the new assertion observes `Closed` on the unfixed build while the previous encrypted file is unchanged.

- [ ] **Step 3: Add one pre-FFI UTF-8 guard shared by every Qt input path**

  Make `field` and `Secret::consume` return success/failure, wipe temporary QString/QByteArray storage on both paths, clear the widget, skip `tv_call` on failure, and retain `Bridge::state` and the live handle. Do not truncate, reduce the character limit to 2,048, or weaken `ffi.rs`.

- [ ] **Step 4: Verify GREEN and ABI defense**

  Run the native test, `cargo test --locked -p tessaveil-windows-controller --test abi`, then `cargo test --locked --all-targets`.

- [ ] **Step 5: Commit**

  Commit: `fix: preserve sessions on oversized unicode input`.

### Task 2: Add authenticated backup, restore, and master-password rotation

**Files:**
- Modify: `crates/tessaveil-core/src/{crypto,error,store}.rs`
- Modify: `crates/tessaveil-core/src/lib.rs`
- Create: `crates/tessaveil-core/tests/recovery.rs`
- Modify: `crates/tessaveil-core/tests/{atomic_save,corruption,vault_roundtrip}.rs`
- Modify: `docs/alpha/vault-format.md`

**Interfaces:**
- Produces: `OpenVault::backup_to(destination)`, `VaultService::restore(source, destination, password, storage)`, and `OpenVault::change_master_password(current, replacement)`; all preserve schema 2 and return bounded `VaultError` values.
- Produces: an injectable cryptographic random source available only through internal/test constructors, with the production default bound to the OS CSPRNG.

- [ ] **Step 1: RED for backup and restore**

  Assert that backup requires a clean saved session, authenticates the current saved image, refuses alias/self/overwrite and unsafe targets, creates a byte-identical encrypted redundancy copy, and restore authenticates before creating a destination. Wrong passwords, damage, truncation, access denial, and pre-existing destinations leave both source and destination unchanged.

- [ ] **Step 2: GREEN for backup and restore**

  Implement identity-safe copy/flush/reopen/authenticate behavior using existing bounded readers and storage policy checks; never decrypt to disk or present a temporary file as an empty vault.

- [ ] **Step 3: RED for password rotation and randomness failure**

  Require current-password authentication; assert new salt, DEK, wrapping nonce and payload nonce, new-password success, old-password failure, unchanged payload/table, and unchanged file/session on RNG or persistence failure.

- [ ] **Step 4: GREEN for password rotation and injectable randomness**

  Re-encrypt the complete payload through one atomic persistence transaction. Keep production CSPRNG fail-closed; expose no deterministic production path.

- [ ] **Step 5: Verify and commit**

  Run focused recovery/corruption/atomic-save tests, full Rust tests and Python discovery. Commit: `feat: add authenticated vault recovery operations`.

### Task 3: Complete sheet, profile-length, and custom-dictionary domain operations

**Files:**
- Modify: `crates/tessaveil-core/src/{catalog,model,sheet}.rs`
- Modify: `crates/tessaveil-core/tests/{catalog_gate,sheet_contract,spin_contract}.rs`
- Modify: `apps/tessaveil-windows/controller/src/lib.rs`
- Modify: `apps/tessaveil-windows/controller/tests/workflow.rs`
- Modify: `apps/tessaveil-windows/bridge.h`

**Interfaces:**
- Produces: exact-profile supported-length queries; profile sheet creation with a caller-selected allowed length; custom dictionary validation/import; sheet rename and guarded deletion; immutable replacement-sheet creation.
- Produces: controller operations for these behaviors without exposing full-phrase or target metadata.

- [ ] **Step 1: RED for all supported lengths and exact modes**

  Assert 10/36 columns and every length allowed by the selected profile; reject unsupported lengths and keep Tonkeeper classic, Tonkeeper multichain, Gram Wallet, MyTonWallet modes distinct. Assert only the three currently verified exact pairs are selectable.

- [ ] **Step 2: GREEN profile-length selection**

  Remove the controller's hard-coded 24 rows and bind creation to the selected profile's allowlisted length.

- [ ] **Step 3: RED/GREEN custom dictionary flow**

  Validate UTF-8, NUL/control/whitespace, normalization collisions, case/diacritic anomalies, counts and 10/36 eligibility before mutation. Store the normalized snapshot only in the encrypted payload; a revised list creates a new unverified sheet with no inherited state.

- [ ] **Step 4: RED/GREEN rename, delete, and replacement**

  Require unlocked protected state, exact-name confirmation for deletion, bounds/aggregate-budget checks, and warnings represented as explicit controller prerequisites. Never mutate an old snapshot in place.

- [ ] **Step 5: Verify and commit**

  Run catalogue generation/drift checks, focused Rust/controller tests, full Rust and Python suites. Commit: `feat: complete sheet and dictionary workflows`.

### Task 4: Complete controller lifecycle and recovery operations

**Files:**
- Modify: `apps/tessaveil-windows/controller/src/{lib,ffi}.rs`
- Modify: `apps/tessaveil-windows/controller/tests/{abi,workflow}.rs`
- Modify: `apps/tessaveil-windows/bridge.h`

**Interfaces:**
- Consumes: Task 2 recovery APIs and Task 3 domain APIs.
- Produces: bounded C ABI operations for backup, restore, password rotation, custom sheets, sheet management, locale/theme preferences, and structured profile details.

- [ ] **Step 1: RED for lifecycle distinctions**

  Assert explicit lock/close prompts, inactivity/Windows-lock/sleep immediate lock, ordinary application deactivation without destructive locking, stale timeout rejection, secret-control clearing, and documented dirty-state outcomes.

- [ ] **Step 2: GREEN controller operations**

  Add operations without increasing field limits or returning secret-derived metadata. Ordinary domain/user errors return nonfatal code 1; malformed pointers/lengths/UTF-8, panic, poisoned registry, and invalid ABI output remain fatal code -1 and destroy the suspect controller.

- [ ] **Step 3: RED/GREEN recovery controller flows**

  Cover create/open/save/verify/backup/close/restore/reopen/password-change and all failure paths, including preserving an open dirty session when a recoverable operation fails.

- [ ] **Step 4: Verify and commit**

  Run controller workflow/ABI tests and all Rust tests. Commit: `feat: complete Windows controller lifecycle`.

### Task 5: Complete the Windows user workflows, localization, themes, and accessibility

**Files:**
- Refactor/Modify: `apps/tessaveil-windows/window.{h,cpp}`
- Create as needed: focused files under `apps/tessaveil-windows/ui/`
- Modify: `apps/tessaveil-windows/CMakeLists.txt`
- Modify: `apps/tessaveil-windows/tests/{ui.cpp,observe.ps1}`
- Modify: `docs/alpha/dev-host-ui-observation.md`

**Interfaces:**
- Consumes: Task 4 C ABI only.
- Produces: complete keyboard-operable Windows flows without full-phrase input or output.

- [ ] **Step 1: RED native workflows**

  Cover create/open/reopen, save confirmation, profile/mode/status display, allowed row-length selection, 10/36 columns, custom dictionary sheet, sheet rename/delete/protection, neutral Spin, Verified-by-me guidance, backup, restore, password change, wrong password, damaged file, oversized multilingual inputs, dirty lock/close, timeout, Windows lock/sleep, and recovery after every recoverable error.

- [ ] **Step 2: GREEN product flows**

  Implement the smallest focused Qt components. Use file pickers only for ciphertext vaults/backups and local dictionary lists; prohibit clipboard, drag/drop into secret controls, plaintext export, print, screenshot features and network operations.

- [ ] **Step 3: RED/GREEN Russian/English and light/dark**

  Centralize every visible string and semantic color. Persist locale/theme only inside the encrypted vault or per-process nonsecret UI state; do not create telemetry or account settings.

- [ ] **Step 4: Accessibility and scaling checks**

  Verify keyboard order, visible focus, password UIA non-exposure, nonsecret accessible names, table headers/corners, 1280x720, 100/150/200% development-host layouts, and no target-cell distinction. Record development-host evidence without claiming clean Windows or Narrator completion.

- [ ] **Step 5: Verify and commit**

  Run native tests, UIA observation, full Rust and Python suites. Commit: `feat: complete Tessaveil Windows candidate workflows`.

### Task 6: Reconcile the Tessaveil Figma system with implemented Windows flows

**Files:**
- Modify only an explicitly identified Figma file named `Tessaveil — Product Design`
- Create: `reports/windows-v1/figma-handoff.md`
- Modify: `tests/repository/**`

**Interfaces:**
- Consumes: the completed Task 5 Windows flows and semantic UI states.
- Produces: inspected Figma evidence for required Windows screens/states and a code-to-design handoff report; never modifies an unrelated Renderis or other project file.

- [ ] **Step 1: Identify the authorized design target**

  Use the connected Figma integration to locate an explicitly Tessaveil-owned file and record its file identity. If none exists or identity is ambiguous, make no Figma mutation and record `blocked` with the exact owner action needed; never reuse an open unrelated file.

- [ ] **Step 2: Reconcile required Windows screens and security states**

  When an authorized file exists, update the component instances and Windows pages for vault selection/create/unlock, profile status, custom dictionary, sheet creation/edit/protection/delete, Spin/repeat warning, verification, backup/restore/password change, lock/privacy cover and every actionable error. Keep examples synthetic and remove local paths/tokens/secrets.

- [ ] **Step 3: Check foundations and accessibility handoff**

  Verify light/dark semantic variables, Russian/English copy coverage, focus order, 1280x720 and 100/150/200% layouts, no target-cell emphasis, and explicit annotations for controls that must not expose secret values to accessibility APIs.

- [ ] **Step 4: Record evidence and commit**

  Write the exact Figma identity/node links or the exact blocker to `reports/windows-v1/figma-handoff.md`, add a repository gate preventing an absent/ambiguous disposition, run the focused and full Python suites, and commit: `docs: record Windows v1 Figma handoff`.

### Task 7: Harden exact-candidate security, failure, and release-decision gates

**Files:**
- Modify/Create: `crates/tessaveil-core/tests/**`
- Modify/Create: `tests/repository/**`
- Modify: `packaging/windows/{gate.ps1,verify.py,distribution-review.json}`
- Create: `reports/windows-v1/release-decision.json`
- Create: `reports/windows-v1/test-protocols.md`
- Modify: `.github/workflows/windows-alpha.yml`

**Interfaces:**
- Produces: a fail-closed exact-SHA decision with one entry per acceptance gate, evidence reference, result (`pass`, `fail`, `blocked`), and rule that only all-pass may authorize real-data candidate wording.

- [ ] **Step 1: RED for crypto/format/failure evidence**

  Require independent Argon2id/XChaCha20 vectors, NFC composed/decomposed/non-BMP/embedded-NUL cases, every KDF bound, wrong password, every envelope-region mutation, truncation/extra bytes, random-source failure, password rotation, backup/restore, and injected save boundaries.

- [ ] **Step 2: RED/GREEN release decision**

  Enumerate catalogue, clean Windows 10/11, physical Android classes, physical iPhone classes/Mac, removable NTFS, removable exFAT, power-loss, network/TEMP/process tracing, accessibility, independent audit, signing, licensing/SBOM/relink, exact-SHA CI and provenance. Missing or development-host-only evidence is `blocked`, never inherited or converted to `pass`.

- [ ] **Step 3: Add ready-to-run external protocols**

  Specify exact candidate hashes, device provenance, non-admin/offline Windows steps, KDF measurements, filesystem interruption points, rollback/version-comparison observation, evidence capture and pass/fail criteria. Do not format or mutate an unidentified device.

- [ ] **Step 4: Verify and commit**

  Run the full Rust/Python/native/security/package gate locally. Commit: `test: add Windows v1 release decision gates`.

### Task 8: Update Russian guidance and exact-candidate distribution evidence

**Files:**
- Modify: `README.md`, `README.ru.md`
- Modify: `docs/alpha/{user-guide,known-limitations,release-evidence}.md`
- Modify: `THREAT_MODEL.md`
- Modify: `packaging/windows/**`
- Modify: `THIRD_PARTY_ALPHA.md`

**Interfaces:**
- Consumes: final Task 7 decision and exact candidate build outputs.
- Produces: bilingual user/reviewer instructions and an unsigned candidate package that cannot be mistaken for stable or real-data-approved software.

- [ ] **Step 1: Document supported exact profiles**

  List the three selectable exact pairs and their pinned scope. List Tonkeeper Multichain, Gram Wallet and other mandatory entries with their real terminal statuses/reasons and original-wallet guidance.

- [ ] **Step 2: Document backup and recovery**

  Explain creation, verification, identical redundancy copies, restore, password loss, source-wallet recovery check, Spin/protection limits, compromised-computer boundary, and cross-version comparison leakage. Never instruct users to give a phrase to Tessaveil, tests, CI, agents, or a website.

- [ ] **Step 3: Build and independently verify the exact artifact**

  Produce runtime/compliance ZIPs, `Tessaveil.exe`, SHA-256 manifest, SBOM, notices, full Qt source/relink material and distribution audit on the final source SHA. Verify artifact contents and absence of secret/synthetic marker leakage.

- [ ] **Step 4: Commit**

  Commit: `build: prepare evidence-backed Windows v1 candidate`.

- [ ] **Step 5: Push and wait for exact branch/PR CI**

  Push sequentially to `feature/windows-alpha`, keep PR #2 open, wait for exact-SHA catalogue and Windows/provenance workflows, download artifacts, verify hashes and strict GitHub attestations. Do not merge, tag, create a GitHub Release or publish stable.

## Final acceptance report

- Exact source SHA and PR merge SHA.
- Exact branch and PR workflow URLs and conclusions.
- Downloadable artifact names, expiry, byte sizes and SHA-256 values; strict provenance verification results.
- Complete selectable profile/mode/version list and unavailable priority-profile reasons.
- Recorded RED/GREEN result for the 2,049-Cyrillic-character regression.
- Test counts and results for Rust, Python, native Qt, packaging, distribution, security and generated-data gates.
- One row for every real-data/release criterion with evidence and disposition.
- Verdict must be exactly either `кандидат допущен к использованию с реальными данными` when every mandatory row passes, or `NO-GO для реальных данных` with each blocker and the concrete action required to clear it.
- PR remains open and stable release remains unpublished for owner review.
