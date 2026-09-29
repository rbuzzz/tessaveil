# Tessaveil: foundation and Windows v1 design

**Date:** 2026-09-29

**Status:** Approved for implementation planning after owner-requested revisions

**Implementation scope:** research foundation, shared vault core, Figma design system, and Windows v1

**Follow-on scope:** Android and iOS receive a separate specification and implementation plan after Windows v1

## 1. Product intent

Tessaveil is an offline application for making encrypted, visually obfuscated backup tables from mnemonic phrases that already exist. The user remembers a sequence of column symbols and manually reads one word from each row. The application stores the filled decoy table, but it never stores which cells form the original phrase.

The first release is a portable, self-contained `Tessaveil.exe` for Windows 10 22H2 x64 and Windows 11 x64. It uses a separate encrypted `.tessaveil` vault file, requires no installation or administrator access, and continues to work without a network connection or account.

The product succeeds when a user can:

1. select an accurately researched wallet and mnemonic profile;
2. create and unlock an authenticated encrypted vault;
3. create one or more protected sheets with 10 or 36 columns;
4. place one word at a time without persisting the column sequence or complete phrase;
5. save, copy, reopen, and restore an encrypted backup;
6. independently reconstruct and verify the phrase in the original trusted wallet;
7. understand the limits of the protection without misleading security claims.

## 2. Scope boundaries

### 2.1 Included in Windows v1

- A versioned, evidence-backed registry of dictionaries, mnemonic schemes, wallet profiles, and their verification status.
- The complete mandatory research catalogue in section 8.
- Local creation, opening, saving, copying, and restoration of encrypted vault files.
- Multiple sheets per vault, wallet and scheme labels, sheet protection, and the user-controlled “Verified by me” flag.
- Full table generation from built-in or user-supplied dictionaries.
- Single-row Spin with no validity signal and no stored target metadata.
- Russian and English UI, light and dark themes, keyboard operation, and Windows scaling support.
- A Figma design system and Windows, Android, and iOS screen designs.
- Public source, security documentation, tests, SBOM, provenance, and release artifacts.

### 2.2 Explicit non-goals

Tessaveil v1 does not:

- generate wallets or real mnemonic phrases;
- reconstruct, reorder, validate, or export a complete phrase;
- validate mnemonic checksums or derive addresses, keys, or balances;
- connect to a blockchain, wallet service, analytics system, font CDN, or application server;
- provide plaintext, CSV, screenshot, clipboard, or print export;
- keep edit history, drafts, previous sheet versions, or automatic backups;
- offer cloud or self-hosted synchronization, QR pairing, or vault transfer;
- claim protection against a compromised operating system, keylogger, malicious IME, process-memory reader, or prolonged screen recording;
- implement key destruction or data deletion after failed password attempts.

The absence of built-in history does not make multiple manually copied or interrupted-save versions safe to compare. If an attacker later obtains the master password and two different tables made from the same phrase, unchanged real words can stand out across rows even when every decoy was regenerated. Backup guidance and edit flows must state this explicitly.

Future QR or synchronization features may transfer only authenticated ciphertext and non-secret protocol metadata. They must never contain a master password, order key, mnemonic phrase, or target-cell information.

## 3. Delivery decomposition

The product is too large for a single undifferentiated implementation. Work is divided into four independently reviewable subprojects:

1. **Research registry and threat model.** Establish provenance, licensing, status, and security claims before a wallet mode becomes selectable.
2. **Design system and Windows UX.** Build the Figma library and validate the sensitive input, table, backup, and recovery flows.
3. **Shared core and Windows v1.** Implement the vault format, catalogue compiler, row operation, Windows application, CI, and release process.
4. **Android and iOS.** Reuse the vault format and Rust core through UniFFI, with native Kotlin/Compose and SwiftUI applications. This subproject begins only after Windows v1 is released.

This specification governs subprojects 1–3. It constrains, but does not authorize implementation of, subproject 4.

## 4. Architecture

### 4.1 Preliminary technology choice

Rust plus Avalonia/NativeAOT is the preferred candidate, not a final selection, until the mandatory spike passes. The realistic candidates are:

| Candidate | Advantages | Primary risks to prove or reject |
| --- | --- | --- |
| Rust core + Avalonia/.NET NativeAOT | Strong separation of a reusable core, mature desktop composition, productive Windows UI, future UniFFI mobile reuse | NativeAOT compatibility, true single-EXE behavior, static Rust linkage, accessibility, binary size, native dependency and `%TEMP%` behavior |
| Rust + Slint | Native-oriented Rust stack and potentially simple static packaging | Windows accessibility, dense-table maturity, secure-input behavior, platform polish, and long-term mobile integration |
| C++ + statically linked Qt 6 | Mature desktop widgets, tables, accessibility, and broad platform support | Static-link licensing obligations, build complexity, artifact size, native mobile UX, and maintaining a safe FFI boundary |

Tauri remains outside the spike because its WebView2 dependency conflicts directly with the no-required-runtime acceptance criterion. Reusing the Windows UI framework unchanged on mobile is not a goal; future production mobile UIs remain Kotlin/Compose and SwiftUI unless a later approved mobile specification changes that decision.

### 4.2 Component boundaries

The UI owns presentation and navigation only. It never implements cryptography, vault parsing, dictionary rules, or mnemonic semantics.

The core exposes narrow operations:

- query verified catalogue records;
- validate and import a custom dictionary;
- create, open, save, back up, and change the password of a vault;
- create or mutate sheet metadata;
- generate a complete decoy table from a profile;
- spin exactly one row from a transient column symbol and one transient word;
- return a new row without returning validity, target position, or phrase-level information.

The core does not expose an API that accepts or returns a complete mnemonic phrase or order key.

### 4.3 Mandatory desktop and mobile feasibility spikes

Before building these probes or filling the catalogue at scale, record whether the required clean Windows 10/11 environments, physical Android/iPhone classes, Mac/Xcode host, and pre-provisioned removable test media are actually available. Each unavailable class is an exact documented blocker. A simulator, virtual disk, Windows Server runner, or ordinary development machine may provide build evidence where relevant but never substitutes for a required physical, removable-media, or clean-machine verification.

Before production implementation, a throwaway Windows spike compares all three candidates using the same minimal vault-open and dense-table shell. The ADR scores clean-machine launch, packaging, accessibility, dependency surface, license obligations, design fidelity, maintenance cost, and future core reuse. Rust + Avalonia/NativeAOT becomes final only if it demonstrates:

1. one NativeAOT `Tessaveil.exe` with the Rust core statically linked into it;
2. launch on clean Windows 10 22H2 x64 and Windows 11 x64 without a separately installed .NET runtime;
3. no extraction of application assemblies or native payloads into `%TEMP%` during launch or normal use;
4. no required network access;
5. an inspected dependency list containing only expected Windows system dependencies and explicitly documented native libraries;
6. identical creation and opening of a fixed synthetic vault vector across Rust and the planned foreign-function boundary;
7. documented binary size, startup time, build constraints, and unsupported NativeAOT behavior.

Before the file format or standard KDF profile is frozen, a separate minimal mobile harness must:

1. open the same synthetic vault through the Rust boundary on physical arm64 Android and iPhone devices;
2. benchmark candidate Argon2id profiles on at least a physical arm64 Android class with 4 GiB RAM, a current mid-range Android class, an iPhone 11/A13/4 GiB class as the provisional lower bound, and a current iPhone class;
3. record wall time, peak memory, failure/OOM behavior, thermal observations, OS, hardware class, and core/library revision;
4. prove identical password NFC normalization and UTF-8 bytes with composed/decomposed Unicode, combining marks, non-BMP characters, and embedded-NUL rejection;
5. reject out-of-policy KDF parameters before allocation or password processing, without clamping or silently weakening them.

These spikes are disposable evidence, not application releases. Failure of any mandatory item stops format/technology freeze and triggers an evidence-backed architecture revision instead of a hidden workaround.

## 5. Vault format and cryptography

### 5.1 File envelope

`.tessaveil` is a versioned binary format. Its cleartext header contains only:

- magic bytes and format version;
- KDF and AEAD identifiers;
- a 128-bit random salt;
- bounded Argon2id parameters;
- independent nonces for DEK wrapping and payload encryption;
- wrapped 256-bit data-encryption key;
- ciphertext length and other parsing lengths required to read the envelope.

The immutable header prefix is associated data for DEK wrapping. The complete encoded header, including the wrapped DEK, is associated data for payload encryption. This avoids a circular dependency while authenticating every header field. Names, locale, wallet profiles, custom dictionaries, sheet settings, protection verifiers, verification flags, and tables exist only inside the encrypted payload.

The encrypted payload uses an explicitly deterministic canonical CBOR schema. Unknown mandatory fields cause a version error; optional future fields are versioned and bounded. Parser limits apply before allocation to the file size, collection counts, string sizes, dictionary sizes, dimensions, and KDF parameters.

### 5.2 Key hierarchy

- The master password is normalized as NFC and encoded as UTF-8.
- Password normalization and byte encoding occur inside the shared Rust boundary, not independently in each native UI. Wrappers pass explicit-length Unicode input and reject embedded NUL rather than relying on C-string termination.
- Argon2id derives a 256-bit key-encryption key.
- The provisional standard-profile candidate is the RFC 9106 second recommended profile: 64 MiB memory, 3 iterations, and parallelism 4. It is not frozen until the physical-device prototype passes.
- The format represents only bounded Argon2id values: memory 64–256 MiB, iterations 3–6, parallelism 1–8, a fixed 32-byte output, and a 16-byte salt. The eventual creation profile is an allowlisted tuple within those absolute bounds and is recorded in the format ADR.
- A client rejects parameters outside the absolute bounds before allocation. A tuple inside the encoding bounds but outside that client's approved profile set produces “Unsupported or too resource-intensive KDF profile,” not “wrong password.” It is never clamped or silently weakened.
- If the provisional profile cannot run reliably on a required target class, format freeze stops for an explicit security/product decision; the implementation does not automatically lower its cost.
- A cryptographically random 256-bit DEK encrypts the payload with XChaCha20-Poly1305.
- The KEK wraps the DEK with a separate XChaCha20-Poly1305 nonce.
- Changing the master password creates a new salt, KEK, DEK, and both nonces, then re-encrypts the complete payload.

Only maintained, reviewed implementations of Argon2id, XChaCha20-Poly1305, the operating-system CSPRNG, and zeroization primitives may be used. Exact dependencies and pinned versions are recorded in an ADR after the spike; no custom cryptographic primitive is permitted.

### 5.3 Password policy

- Minimum: 15 Unicode characters after normalization.
- At least 64 characters are supported.
- No composition rules are imposed.
- A local, bundled common-password and common-pattern check is performed without telemetry.
- Password-strength estimates are scenario ranges based on measured Argon2id rates and explicit assumptions, never a precise time derived only from length.
- Order-key education uses length, alphabet, repetition, and user-selected randomness assumptions. The actual order key is not entered into or evaluated by the estimator.

### 5.4 Atomic persistence

Saving writes an adjacent temporary `.tessaveil` image containing the open technical header and authenticated ciphertext, but no open payload. The sequence is:

1. serialize and encrypt a complete new image;
2. write and flush the temporary file;
3. reopen it and verify structure and AEAD authentication;
4. atomically replace the target where the filesystem supports it;
5. report failure without modifying the previous valid vault.

An interrupted save may leave a temporary file with a clear technical header and encrypted payload, never an open payload. That file may be a different table version and therefore participates in the cross-version comparison risk after password disclosure. The UI identifies it without presenting it as a valid empty vault and cleans it on a best-effort basis without claiming secure erasure. Migration creates a new authenticated image and never writes plaintext to disk.

The atomic-replacement claim is limited to filesystems and device classes exercised by the release matrix. Local NTFS, removable NTFS, and removable exFAT are tested separately with same-directory replacement and injected interruption. A filesystem is listed as atomic only after those tests pass. On FAT32, network shares, cloud-synchronized folders, or any unverified filesystem, the application makes no atomicity promise: it opens read-only or requires Save As to a verified target rather than silently performing an unsafe in-place update. Release documentation lists the tested filesystem, Windows version, device class, API path, and observed guarantees.

The application does not claim rollback detection because no trusted external monotonic state exists.

## 6. Stored and forbidden data

The encrypted payload may store:

- current sheets and complete decoy tables;
- stable catalogue/profile identifiers and required profile snapshots;
- user-visible names and labels;
- complete imported custom dictionaries;
- sheet protection verifiers and settings;
- the user-controlled “Verified by me” flag;
- vault preferences needed for offline operation.

It must never store, even encrypted:

- an order key, its hash, length, repetition period, pattern, hint, or verifier;
- the target column or cell for any row;
- a word entered during Spin;
- a complete mnemonic phrase, phrase ordering, checksum result, derived key, or address;
- completion markers identifying successfully processed rows;
- input history, drafts, prior table versions, or prior sheets;
- clipboard, screenshot, or telemetry copies of secret input.

The serializer has structural tests that reject forbidden fields and scans test vaults for synthetic secret markers.

## 7. Table creation and Spin

### 7.1 Table generation

- The default alphabet is `0–9, A–Z` with 36 columns.
- A 10-column `0–9` mode is available.
- The supported model is extensible and initially covers 12, 13, 15, 16, 18, 20, 21, 24, 25, 26, 27, 28, 29, and 33 rows.
- Selecting a verified profile immediately fills every cell using the full eligible dictionary and the OS CSPRNG.
- Position-dependent schemes use the eligible list for that position, including Decred PGP even/odd lists.
- Words do not repeat within one row when the eligible dictionary is large enough. This rule says nothing about whether a user's real phrase may repeat a word.

### 7.2 Single-row operation

For one row, the user enters the same column symbol twice and one word in masked, non-autocompleting controls. The two symbols are compared transiently. A layout warning appears when the profile permits ASCII `A–Z` but the active keyboard may produce other characters.

On Spin:

1. the complete current row is freshly generated;
2. if the word is allowed for that profile and position, it is placed in the transiently selected column;
3. otherwise, that column receives an ordinary random word just like every other cell;
4. the core returns only the new row and no validity result;
5. the transient inputs are cleared immediately on a best-effort basis.

The UI does not mark the target cell, display a success/error state, or retain a completion flag. The user decides visually whether to continue. A second attempt shows a neutral warning that repeated observations may correlate rows; it does not reveal whether the previous input was valid.

Neither UI nor core constructs the complete phrase. Immutable GUI strings, IME buffers, paging, crash dumps, and hostile processes cannot be guaranteed to erase data; this limitation is stated in the product and threat model.

## 8. Evidence registry and mandatory catalogue

### 8.1 Registry model

The source registry is split into:

```text
catalog/
  dictionaries/
  schemes/
  wallets/
  evidence/
wordlists/
  <dictionary-id>/<revision>.txt
```

Four independent record types prevent a shared word list from being confused with a shared mnemonic scheme:

- **Dictionary:** stable ID, language, source URL, pinned revision, license decision, attribution, count, SHA-256, encoding, normalization, ordering, position rules, and test vectors.
- **Scheme:** dictionary references, permitted lengths, position rules, passphrase information, and mnemonic semantics. Tessaveil records these semantics but does not derive keys.
- **Wallet profile:** product, platform, version interval, stable concrete mode ID, aliases, network, scheme, status, evidence references, and verification date. Several modes of one product may coexist in the same platform/version interval; only the full product + platform + overlapping version interval + mode key is a conflict.
- **Evidence:** official specification, official documentation, official source at a pinned commit, or a reproducible public test vector.

Evidence priority is official specification, then official documentation, then official source, then reproducible public vectors. Conflicting versions become separate profiles and are never silently merged.

### 8.2 Status policy

- `verified`: source, license decision, count, hash, rules, mappings, and required vectors pass.
- `documented`: evidence exists but is insufficient for support.
- `blocked`: provenance, licensing, or ambiguity prevents support.
- `no-mnemonic-confirmed`: the product or mode was researched but does not expose a supported mnemonic backup.
- `historical` is an independent lifecycle flag rather than a support status. A legacy profile must still be `verified` before it is selectable.

Only `verified` profiles are selectable for table creation. Other profiles remain searchable with a plain-language reason and a recommendation to use the wallet's own backup mechanism.

Every mandatory catalogue item must have a terminal, documented status before a release candidate. An evidenced `blocked` status may complete the research catalogue, but it independently prevents Windows v1 unless the owner explicitly approves a precise change to the acceptance criterion.

### 8.3 Mandatory dictionaries and schemes

The Windows v1 research set includes:

- BIP-39 with all ten official dictionaries: English, Japanese, Korean, Spanish, Chinese Simplified, Chinese Traditional, French, Italian, Czech, and Portuguese; lengths 12/15/18/21/24 where the wallet actually supports them.
- TON-native 24-word mnemonics and TON multichain BIP-39 12/24 as separate schemes despite a shared English list.
- Monero legacy 25 words: English, German, Spanish, French, Italian, Dutch, Portuguese, Russian, Japanese, Chinese Simplified, Esperanto, Lojban, and historical EnglishOld.
- MyMonero 13 words as a separate profile.
- Polyseed 16 words with its ten own dictionaries: English, Japanese, Korean, Spanish, French, Italian, Czech, Portuguese, Chinese Simplified, and Chinese Traditional.
- SLIP-39 with its 1024-word list and each share represented by a separate sheet; 20/33-word variants only where confirmed. Tessaveil does not combine shares.
- Algorand 25 words using the documented format and vocabulary.
- Cardano 12, 15, 24, and historical 27-word modes, separated by Byron/Icarus/hardware-wallet semantics where relevant.
- Electrum v2+ and historical Electrum v1 as separate schemes and sources.
- Polkadot/Substrate modes with explicit differentiation from ordinary BIP-39 derivation semantics.
- Decred 33-word PGP even/odd format, verified BIP-39 modes, and the version-specific 15-word Cake Wallet mode as independent profiles.
- Zano's 1626-word dictionary and verified modern 26-word and historical 24/25-word modes.
- Sia's current 12-word BIP-39 mode and historical 28/29-word siad/Sia-UI modes, including the walletd compatibility limitation.
- Verified Zcash/Zallet 24-word BIP-39 modes and separate non-mnemonic key-material modes.
- Chia's verified 24-word BIP-39 mode.
- Any additional distinct dictionary discovered while researching the named products below.

Passphrases are described as external secrets but never stored in table metadata.

### 8.4 Mandatory named products and networks

Every item below must be researched and represented, even when the result is `no-mnemonic-confirmed`:

- Tonkeeper classic and multichain, Gram Wallet, My Wallet/MyTonWallet, TON Space, Tonhub, and OpenMask.
- Phantom, Solflare, Backpack, and Glow.
- Cake Wallet across all current supported networks and phrase formats.
- Trust Wallet, MetaMask, Coinbase Wallet mnemonic mode, Exodus, Atomic Wallet, OneKey, Ledger, and Trezor.
- OKX Wallet, Bitget Wallet, SafePal, Tangem seed-phrase mode, Keystone, BitBox02, ELLIPAL, Coinomi, Guarda, TokenPocket, imToken, Rabby, Rainbow, and Zerion.
- Electrum, Sparrow, BlueWallet, Coldcard, Blockstream Jade, Passport, and SeedSigner.
- Keplr, Leap, and Cosmostation.
- Yoroi, Daedalus, Lace, Eternl, Nami, and Typhon.
- Monero GUI/CLI, MyMonero, Feather, and version-specific Monero export from Exodus.
- Pera Wallet and Defly.
- Decrediton, Zano Wallet, Cake Wallet Zano, and current and historical Sia products.
- Relevant profiles for Bitcoin, Ethereum, Base, BNB Chain, Polygon, Avalanche, Arbitrum, Solana, TRON, Cosmos, Tezos, Temple, Kukai, Polkadot, Kusama, Cardano, Algorand, Monero, Zcash, Chia, Decred, Zano, and Sia.

Import support is not evidence that a wallet creates the same mnemonic. Passkey, MPC, social-login, cloud-backup, private-key-only, and non-exportable modes are described but not converted into invented mnemonic profiles. Multiple such modes may coexist under one wallet name and remain separate by stable mode ID. Gram Wallet and other ambiguous product names are split by product identity, platform, version, and mode rather than inheriting historical behavior by name.

### 8.5 User dictionaries

A user may import a local UTF-8 list. The importer checks decoding, normalized duplicates, case and diacritic anomalies, line shape, and whether enough unique eligible words exist for 10 or 36 columns. The complete normalized source needed to reproduce the table offline is stored inside the encrypted vault.

The profile is labeled “Custom — compatibility not verified.” Every existing sheet owns an immutable snapshot of the dictionary used to build it. A populated sheet cannot switch that snapshot or automatically regenerate rows.

Choosing a revised list creates a new sheet. The user must fill and independently verify it from the beginning; “Verified by me,” row state, table cells, and protection state are not inherited. Windows v1 provides no automatic phrase-preserving migration because the application neither knows nor may reconstruct the true words and columns. The old sheet remains unchanged until explicit deletion, and the creation flow warns that retaining two different tables for the same phrase can enable cross-version comparison if both are later decrypted.

### 8.6 Generated catalogue and CI

Build tooling compiles the source records into a deterministic embedded registry and generates `docs/catalog.md` from the same data. Runtime catalogue use is offline.

CI fails closed on schema errors, duplicate IDs, normalization collisions, mismatched count or hash, invalid lengths, missing evidence, undecided licensing, broken wallet-to-scheme-to-dictionary references, or failed vectors.

## 9. Application lifecycle and errors

### 9.1 States

The visible state machine is:

```text
Closed → Unlocking → Open/Clean ↔ Open/Dirty → Saving → Open/Clean
                                  ↘ Editing one row ↗
```

Authentication or structural failure never transitions to an empty vault.

The default inactivity timeout is five minutes. The user may choose 1, 5, 15, or 30 minutes, but not “never.” Windows session lock and sleep lock the vault immediately. Locking removes usable keys and current input on a best-effort basis and covers sensitive UI before returning to the vault list.

### 9.2 Error contract

- Wrong password and failed envelope authentication intentionally share: “The password is incorrect or the vault is damaged.”
- Invalid magic/header, unsupported version, out-of-policy KDF parameters, truncated file, insufficient space, and access denial have distinct actionable messages.
- A failed save retains the last valid vault and identifies any remaining temporary file as a clear technical header plus encrypted payload, including its cross-version comparison risk.
- Local delays after failures are UX throttling only and are never described as protection from offline guessing.

### 9.3 Sheet protection

After a successful save, a sheet returns to protected mode. Editing rows or deletion requires either the master password or the optional sheet password selected by the user. Deletion also requires entering the sheet name and a final confirmation. The dictionary snapshot of a populated sheet is immutable; a different dictionary always starts a separate unverified sheet as defined in section 8.5.

Before changing a row in any sheet that has previously been saved, the UI warns that old backups, copied vaults, or an interrupted-save temporary file may preserve a different table for the same phrase. Comparing such versions after password disclosure can identify invariant real words; full row or table re-randomization does not remove that risk. Tessaveil therefore offers no cosmetic “reshuffle table” operation and never describes re-randomization as safe migration.

The sheet password is a salted verifier inside the already encrypted payload. It protects against accidental UI actions after vault unlock and is not a second cryptographic boundary if the master password or decrypted payload is compromised.

The “Verified by me” flag can be set only after a separate explanation asks the user to restore through the original trusted wallet or an official hardware-wallet backup check. Tessaveil performs no cryptographic verification and does not ask the user to paste a full phrase into another application.

## 10. Threat model requirements

`THREAT_MODEL.md` separately analyzes:

- theft of the EXE alone;
- theft and offline attack of vault ciphertext;
- disclosure of the master password and table;
- weak, repeated, or disclosed order keys;
- malware, keyloggers, hostile IMEs, memory access, swap, crash dumps, and screen recording during entry or viewing;
- repeated-Spin intersection attacks;
- comparison of manually retained backups, replaced sheets, and interrupted-save temporary files containing different tables for the same original phrase;
- loss of a master or sheet password;
- compromise of the originating wallet or hardware wallet;
- physical destruction or loss of one or all copies;
- rollback to an older valid ciphertext.

Selecting one of four mobile column groups would reveal approximately two bits per row and could expose repetition in a short order key. Therefore mobile does not allow direct group selection or free group swiping during reconstruction.

A fully compromised operating system can capture the symbol, word, UI, or process memory. Screen protection and short-lived buffers reduce incidental exposure but do not change that boundary. The product recommends an updated trusted device and a separate cold backup without promising absolute security.

Identical copies of one unchanged encrypted table do not add a new table-comparison signal, but different saved versions can. The guidance distinguishes redundancy from versioning, warns before post-save row edits or replacement-sheet creation, and never claims that refreshing every decoy prevents intersection analysis.

## 11. UX and Figma

### 11.1 Visual direction

Windows uses the approved “focused process” direction: compact vault and sheet navigation, a prominent current-row secure-input area, visible warnings, and the full table as context. It must look like a dedicated security product rather than a spreadsheet clone.

### 11.2 Figma file structure

The file is named `Tessaveil — Product Design` and contains:

1. `00 — Cover & Principles`
2. `01 — Foundations`
3. `02 — Components`
4. `03 — Windows`
5. `04 — Android`
6. `05 — iOS`
7. `06 — Flows & Security States`
8. `07 — Handoff`

Foundations use variables and semantic tokens for light/dark colors, typography, spacing, radii, elevation, and focus. Screens use component instances rather than detached copies. Components cover buttons, secure controls, cells, headers, tabs, profile cards, dialogs, warnings, status badges, sheet protection, and errors.

### 11.3 Required flows

The Windows designs cover vault selection, creation, unlock, password guidance, profile search, custom dictionary import, sheet creation, table workspace, row Spin, repeated-Spin warning, verification guidance, backup, restore, password change, sheet protection, rename/delete, settings, locking, and every defined error state.

Windows keeps row numbers and column headers visible while scrolling all 36 columns and never truncates cell words. Highlighting and animation apply uniformly to the row and never mark the target cell.

Mobile presents one row as four fixed groups:

```text
0–8 → 9–H → I–Q → R–Z
```

Only “Next group” advances. The next row is available after all four groups have been shown. There is no direct group picker, reverse/free swipe, found marker, highlight, or persisted group/scroll/dwell history. Backgrounding immediately places a neutral privacy cover and locks according to the mobile security lifecycle. Android uses `FLAG_SECURE`; iOS covers app-switcher snapshots and reacts to screen-capture state. These are mitigations, not guarantees.

### 11.4 Design acceptance

- Windows layouts are checked at 1280×720 and larger, and at 100%, 150%, and 200% scaling.
- Mobile layouts are checked at 390 and 320 logical pixels.
- Keyboard focus is visible and complete; screen-reader names do not reveal hidden input.
- Contrast meets WCAG AA; touch targets are at least 48 dp on Android and 44 pt on iOS.
- Typography clearly distinguishes `0/O` and `1/I`.
- All examples are synthetic and cannot be used as a real funded-wallet mnemonic.
- Figma contains no tokens, local user paths, real vaults, secrets, or external production data.

## 12. Verification strategy

### 12.1 Core and catalogue

- Known-answer vectors for Argon2id and XChaCha20-Poly1305.
- Deterministic cross-language vault fixtures containing synthetic data.
- Authentication failures after mutation of every envelope region.
- Round trips for create, reopen, resave, password change, backup, and migration.
- Fault injection around every atomic-save step.
- Tests proving forbidden order/target/word markers are absent from serialized data.
- Dictionary hashes, counts, ordering, Unicode normalization, position rules, and mappings.
- 10/36 columns and every required row length.
- Valid and invalid Spin inputs follow the same interaction and control states: no explicit validity result, success flag, target-column output, differentiated error, or persisted metadata. The visible row contents may differ and a valid input must visibly place the requested word.
- Property tests for table dimensions, uniqueness policy, bounds, and round trips.
- Fuzzing of envelope parsing, CBOR payload parsing, catalogue parsing, and position-dependent formats.

Only invented synthetic inputs and public standard vectors are committed.

### 12.2 Windows application

- Automated tests for the critical create/open/sheet/Spin/save/backup/restore/error flow.
- Keyboard and accessibility checks for sensitive controls.
- Network observation proving normal vault workflows make no outbound requests.
- Process/file observation proving the release executable does not extract application payloads to `%TEMP%`.
- Clean-machine tests on Windows 10 22H2 x64 and Windows 11 x64 without development runtimes or administrator access.
- Startup and bounded diagnostic log review with no secret content.

Windows 10 documentation states that a device used as a trusted computer must remain on current ESU security updates after ordinary support ends.

### 12.3 Security and supply chain

- Independent internal review of vault boundaries and cryptographic use.
- Locked dependencies, vulnerability scanning, license review, and `THIRD_PARTY_NOTICES`. Every distributed dictionary also receives an explicit compatibility decision for repository redistribution and SignPath Foundation's OSS-signing conditions.
- SBOM, repository secret scanning, and release artifact provenance.
- `SECURITY.md`, vulnerability reporting instructions, and an external-audit worklist.
- The public statement: `Security audit: not yet independently completed.`

Public source is not presented as an independent security audit. “Unbreakable,” “state of the art,” and equivalent claims are prohibited.

## 13. Repository and release policy

### 13.1 Repository

The target is the public GitHub repository `rbuzzz/tessaveil` on branch `main`. Before creation, availability and obvious category conflicts are checked; this is not represented as legal trademark clearance.

The repository includes Russian and English README files, Apache-2.0 for original code, dictionary-specific licensing and attribution, `THIRD_PARTY_NOTICES`, `SECURITY.md`, `CONTRIBUTING.md`, `THREAT_MODEL.md`, generated `docs/catalog.md`, ADRs, build/test instructions, and release verification instructions.

No real phrase, funded key, real vault, credential, Figma token, GitHub token, or local user path may appear in source, history, issues, CI output, release artifacts, or Figma.

### 13.2 CI release gate

A release candidate is built in GitHub Actions from an exact commit only after mandatory CI succeeds. The release publishes:

- `Tessaveil.exe`;
- SHA-256 checksum file;
- GitHub artifact attestation/provenance tied to the repository, workflow, and commit;
- SBOM and third-party notices;
- test and clean-machine verification summary;
- known limitations and signature status.

### 13.3 SignPath Foundation sequence

The approved signing path is:

1. Publish the first functional pre-release, `v0.1.0-rc.1`, without Authenticode because SignPath requires an already released and documented OSS project.
2. Protect that RC with SHA-256, GitHub artifact attestation/provenance, SBOM, exact-commit CI, and explicit “unsigned” labeling.
3. Enable GitHub 2FA and add the required code-signing policy, privacy statement, project roles, release documentation, and reproducible trusted build.
4. Apply to SignPath Foundation.
5. If accepted, integrate its GitHub trusted-build/origin-verification flow, manual release approval, and Authenticode signing.
6. Publish a signed subsequent RC and repeat Windows verification on the exact signed artifact.
7. Publish stable Windows v1 only after the signed RC passes all gates.

The certificate belongs to SignPath Foundation, so its name appears as publisher. Acceptance is not guaranteed. If SignPath rejects or does not accept the new project, `v0.1.0-rc.1` remains clearly marked as an unsigned pre-release and is never promoted or described as stable. The stable-release gate stops while the owner chooses between remediation and reapplication, a separately approved paid CA certificate, or an explicit revision allowing an unsigned stable release. No certificate is purchased and no unsigned RC is relabeled without that decision.

SmartScreen reputation is not guaranteed merely by Authenticode signing and may develop across releases. No EV-bypass claim is made.

## 14. Windows v1 acceptance criteria

Windows v1 is complete only when all of the following are true:

- every mandatory catalogue item has evidence, licensing disposition, and a terminal status;
- every bundled dictionary is compatible with both its own license obligations and the selected SignPath signing arrangement;
- every selectable profile is `verified` and passes its vectors;
- the Figma system and all required screens meet section 11;
- the comparative desktop spike selects a stack from measured evidence, all acceptance checks for that stack pass, and its ADR is committed;
- the signed release executable runs on both supported clean Windows versions without install, admin access, runtime installation, temp extraction, account, or network;
- vault creation/open/save/password-change/backup/restore and failure recovery pass;
- every forbidden-data and cryptographic test passes;
- all security, supply-chain, documentation, and release gates pass for the exact release commit and artifact;
- the public repository and signed GitHub Release are accessible;
- limitations, lack of independent audit, Windows 10 ESU requirement, and threat boundaries are visible.

An unmet technical requirement is never replaced with a mock, placeholder, or unsupported compatibility claim. Evidence is collected, a safe alternative is proposed, and any acceptance change requires explicit owner approval.

## 15. Mobile compatibility contract

Full Android and iOS applications begin together only after Windows v1. The minimal compatibility/KDF harness in section 4.3 is an earlier format gate, not a mobile product release.

The envelope, canonical payload schema, password byte normalization, KDF profile, catalogue IDs, forbidden-data rules, and cross-language vectors are frozen only after that harness opens the same synthetic vault and completes the physical-device measurements. The production contract remains that a Windows-created vault opens on both mobile platforms and vice versa without format conversion.

Mobile implementation receives its own written specification and plan covering platform key handling, lifecycle, backup-provider file access, accessibility, store policy, and release verification. Synchronization and QR remain out of scope.

## 16. Primary references

- BIP-39: <https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki>
- BIP-39 word-list guidance: <https://github.com/bitcoin/bips/blob/master/bip-0039/bip-0039-wordlists.md>
- TON TEP-3: <https://github.com/ton-blockchain/TEPs/blob/master/text/0003-wallets.md>
- Monero mnemonic documentation: <https://docs.getmonero.org/mnemonics/legacy/>
- Polyseed: <https://github.com/tevador/polyseed>
- SLIP-39: <https://github.com/satoshilabs/slips/blob/master/slip-0039.md>
- Cardano CIP-3: <https://cips.cardano.org/cip/CIP-3>
- Electrum seed format: <https://electrum.readthedocs.io/en/latest/seedphrase.html>
- Decred mnemonic seed: <https://docs.decred.org/advanced/mnemonic-seed/>
- Argon2id recommendations: <https://www.rfc-editor.org/rfc/rfc9106>
- XChaCha20-Poly1305: <https://doc.libsodium.org/secret-key_cryptography/aead>
- NIST password guidance: <https://pages.nist.gov/800-63-4/sp800-63b/passwords/>
- SignPath Foundation conditions: <https://signpath.org/terms.html>
- CA/Browser Forum code-signing requirements: <https://cabforum.org/working-groups/code-signing/requirements/>

These links are starting points. Each catalogue record must cite a current primary source, pinned source revision, and licensing evidence at implementation time.
