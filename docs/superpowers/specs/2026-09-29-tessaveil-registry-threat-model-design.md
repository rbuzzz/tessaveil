# Tessaveil subproject 1: registry and threat-model design

**Date:** 2026-09-29

**Status:** Approved for implementation planning after owner-requested revisions

**Parent design:** `2026-09-29-tessaveil-foundation-windows-v1-design.md`

## 1. Goal

Create the evidence and security foundation that must exist before Figma production work or application implementation. The result is a machine-verifiable catalogue of mnemonic dictionaries, schemes, and wallet profiles, an explicit threat model that defines what Tessaveil can and cannot protect, and disposable feasibility evidence needed before technology and vault-format freeze.

This subproject produces durable repository artifacts, validation tooling, and throwaway desktop/mobile/filesystem probes. It does not produce a distributable Tessaveil application, production vault implementation, Figma file, or public release binary.

## 2. Deliverables

- Versioned source records under `catalog/dictionaries`, `catalog/schemes`, `catalog/wallets`, and `catalog/evidence`.
- Redistributable dictionary sources under `wordlists/<dictionary-id>/<revision>.txt` only after licensing is confirmed.
- A schema and fail-closed validator for every record type.
- Deterministically generated `docs/catalog.md` in Russian and English-compatible structure.
- `THREAT_MODEL.md` with scenario, asset, attacker, exposure, mitigation, residual risk, and user guidance for every required threat.
- `THIRD_PARTY_NOTICES` entries and per-dictionary decisions covering source-license compliance, repository redistribution, and SignPath Foundation eligibility.
- CI checks for the registry, wordlists, documentation generation, and repository secrets.
- Research notes tied to primary URLs, pinned revisions, verification dates, and reproducible evidence.
- A comparative ADR for Rust + Avalonia/NativeAOT, Rust + Slint, and static C++/Qt 6 based on actual Windows probes rather than a preselected winner.
- A mobile compatibility/KDF report from physical Android and iPhone classes before the envelope and standard Argon2id profile are frozen.
- A filesystem matrix documenting temporary-file content and interruption behavior on local NTFS, removable NTFS, and removable exFAT.

## 3. Registry boundaries

Dictionary, scheme, wallet profile, and evidence are independent entities. A wallet profile references a scheme; a scheme references one or more dictionaries. Sharing a word list never implies compatible mnemonic semantics or key derivation.

### 3.1 Dictionary record

Required fields:

- stable ID and display names;
- language and script;
- authoritative source URL and pinned revision/version;
- license, attribution text, explicit redistribution decision, and compatibility with the selected code-signing arrangement;
- encoding and exact normalization rule;
- word count, byte-level SHA-256, order, and position rules;
- normalized duplicate analysis;
- test-vector references.

Normalization is scheme-specific when required and is never globally assumed. For example, BIP-39 requires UTF-8 NFKD, while other lists may have different canonical behavior.

### 3.2 Scheme record

Required fields:

- stable ID and version interval;
- exact dictionary references;
- supported lengths;
- position-dependent selection rules;
- external-secret information such as an optional passphrase;
- semantic distinction from other schemes using the same words;
- official vectors or reproducible examples;
- statement that Tessaveil does not derive keys or validate complete phrases.

### 3.3 Wallet-profile record

Required fields:

- product name, aliases, platform, version interval, and a stable concrete mode ID;
- network or ecosystem;
- exact scheme reference;
- support status, evidence references, and last verification date;
- user-facing limitations for passkey, MPC, cloud, private-key-only, import-only, and non-exportable modes.

Ambiguous names and changed behavior create separate profiles. Several modes of one wallet may coexist for the same platform and version interval; they remain separate records distinguished by mode ID. A conflict exists only when product identity, platform, overlapping version interval, and the concrete mode all collide, not merely because the wallet name matches. Import capability alone is not evidence that the wallet creates that mnemonic.

### 3.4 Evidence record

Evidence priority is:

1. official specification;
2. official product documentation;
3. official source code at a pinned commit;
4. reproducible public test vector.

Each claim links to the exact evidence that supports it. Conflicting evidence is preserved and resolved by product version rather than silently combined.

## 4. Status and support policy

Support status is one of:

- `verified`: all required provenance, license, hash/count, rules, mapping, and vectors pass;
- `documented`: relevant evidence exists but is insufficient for selectable support;
- `blocked`: ambiguity, provenance, or licensing prevents support;
- `no-mnemonic-confirmed`: research confirms that the applicable mode does not expose a supported mnemonic backup.

`historical` is a separate lifecycle flag. A historical profile must still be `verified` before becoming selectable.

Only `verified` profiles are eligible for table creation in later subprojects. Other records remain visible in the generated catalogue with a reason and guidance to use the wallet's own backup procedure.

Every mandatory item must have a terminal documented result. An evidence-backed `blocked` status is a valid completion result for the research catalogue. It independently keeps Windows release readiness at `NO-GO` unless the owner explicitly approves a precise acceptance-criterion change; research never invents a compatible list to clear that gate.

## 5. Mandatory research set

The complete required set is defined in sections 8.3 and 8.4 of the parent design. It includes all ten BIP-39 languages; TON native and multichain modes; Monero legacy, MyMonero, and Polyseed; SLIP-39; Algorand; Cardano historical and current modes; Electrum v1 and v2+; Polkadot/Substrate; Decred; Zano; Sia; Zcash/Zallet; Chia; every named wallet; and every named network.

The research output must explicitly resolve:

- wallet versions that create different phrase formats;
- export versus import-only behavior;
- shared lists with incompatible mnemonic semantics;
- position-dependent lists and unusual lengths;
- additional secrets that Tessaveil must describe but never store;
- products with no exportable mnemonic;
- redistribution rights for every bundled word list.

No required item may disappear because it is difficult to verify.

## 6. User dictionaries

The schema defines a separate custom-dictionary profile labeled “Custom — compatibility not verified.” Later application code will import UTF-8, apply the declared normalization, detect normalized duplicates and case/diacritic anomalies, and require enough unique eligible words for 10 or 36 columns.

Custom dictionaries never enter the built-in registry as verified data. Their complete reproducible content belongs only inside the user's encrypted vault.

The application contract represented by the schema treats a sheet's dictionary snapshot as immutable. A revised custom list creates a new unverified sheet that the user fills and checks again. No table, row state, protection state, or “Verified by me” flag migrates automatically, because Tessaveil does not know the true words and columns.

## 7. Validator and generated documentation

The validator fails on:

- schema violations or unknown mandatory fields;
- duplicate IDs and broken references;
- source files whose byte count, word count, order, or SHA-256 changed;
- duplicates introduced by the required normalization;
- invalid phrase lengths or position rules;
- missing primary evidence, pinned revision, verification date, or license decision;
- missing or failing test vectors;
- a generated `docs/catalog.md` diff not committed with its source change.

JSON Schema 2020-12 is executed in CI with pinned `check-jsonschema==0.38.2`; the Python validator remains responsible for bounded loading and cross-record semantics. Both engines consume the same valid/invalid fixture corpus, and a parity test requires identical fixture classification so neither implementation can drift unnoticed from the other.

The generated catalogue presents one searchable product/network index while deduplicating underlying dictionaries. It shows version, scheme, lengths, language, passphrase information, evidence, verification date, lifecycle flag, and status. Generation is deterministic and does not fetch the network during a normal build.

## 8. Threat model

`THREAT_MODEL.md` covers at minimum:

- executable theft without a vault;
- ciphertext theft and offline password guessing;
- disclosure of master password plus table access;
- weak, repeated, observed, or disclosed order keys;
- malware, keylogger, hostile IME, clipboard, screenshots, prolonged recording, process memory, dumps, and swap;
- intersection leakage across repeated Spin attempts;
- comparison of different saved tables for the same phrase obtained from manual backups, replacement sheets, or interrupted-save temporary files;
- mobile group-selection leakage and the fixed group-order mitigation;
- loss of master or sheet passwords;
- compromised source wallet, hardware wallet, or original phrase;
- file corruption, power loss, rollback, and partial atomic writes;
- physical loss or destruction of devices and backups.

For each scenario the document names assets, attacker capabilities, protection offered, limitations, mitigations, and user action. It states that:

- the process necessarily sees the current word and column briefly;
- the application cannot defeat a compromised OS;
- Spin is limited visual masking, not a proof against observation;
- sheet passwords prevent accidental UI actions but are not an independent cryptographic boundary;
- offline attempt limits and self-destruction do not protect copied ciphertext;
- the table does not replace a separate cold backup or trusted hardware-wallet process.
- re-randomizing a row or complete table does not eliminate comparison leakage if an attacker later decrypts another version; the product therefore provides no cosmetic reshuffle or automatic dictionary migration.

The document distinguishes identical redundant copies from different table versions. It also states that a temporary vault image contains a clear technical header and authenticated ciphertext, not an open payload, and may still preserve a comparison-useful version after master-password disclosure.

## 9. Feasibility evidence gates

Before any risky probe or bulk catalogue population, a dated equipment matrix records availability or an exact blocker for clean Windows 10/11 environments, every required physical Android/iPhone class, the Mac/Xcode host, and pre-provisioned removable test media. Simulators and hosted runners may prove builds only; they never substitute for a required physical or clean-machine result. A missing environment is a terminal research finding and a continuing technology, format, filesystem, or release blocker as applicable.

### 9.1 Windows technology comparison

The same minimal secure-input and dense-table probe is built with Rust + Avalonia/NativeAOT, Rust + Slint, and statically linked C++/Qt 6. The report compares clean Windows 10/11 launch, single-EXE packaging, actual static/native dependencies, `%TEMP%` writes, accessibility, table behavior, license obligations, binary size, and mobile-core reuse. Rust + Avalonia/NativeAOT remains provisional until its evidence wins this comparison and satisfies the parent specification.

### 9.2 Mobile format/KDF probe

A minimal non-product harness opens one synthetic vault through the proposed shared core on physical arm64 Android and iPhone devices. It measures the provisional Argon2id profile on a 4 GiB arm64 Android class, a current mid-range Android class, an iPhone 11/A13/4 GiB class as the provisional lower bound, and a current iPhone class.

The report records time, peak memory, failure/OOM behavior, device/OS class, normalization bytes, and library revision. It proves identical NFC UTF-8 handling with composed/decomposed and non-BMP vectors. Absolute file bounds are memory 64–256 MiB, iterations 3–6, parallelism 1–8, fixed 32-byte output, and 16-byte salt. Parameters outside those bounds are rejected before allocation; unsupported in-bound tuples produce a distinct profile error and are never clamped. A failing required device class stops format freeze rather than silently weakening Argon2id.

### 9.3 Filesystem probe

The save probe writes only the clear technical header and encrypted payload to an adjacent temporary file. Same-directory replace and injected interruption are tested separately on local NTFS, removable NTFS, and removable exFAT. The final documentation claims atomic replacement only for combinations that pass. FAT32, network shares, cloud-synchronized folders, and unverified filesystems receive no blanket guarantee and are not silently updated in place.

## 10. Testing and CI

- Schema fixtures for valid and invalid records.
- Exact hash/count/order tests for every accepted dictionary.
- Unicode and normalization fixtures for every language/script family.
- Mapping tests from wallet profile to scheme, dictionary, and allowed length.
- Position-dependent fixtures, including Decred even/odd words.
- Public official vectors where available and clearly synthetic fixtures otherwise.
- Deterministic documentation-generation test.
- Secret scanning that rejects credentials and seed-like test material outside an explicit synthetic-vector allowlist.
- License/attribution completeness check, including SignPath Foundation compatibility for every distributed word list.

Tests must never use a real wallet phrase, funded key, user vault, or local credential.

## 11. Acceptance criteria

This research subproject is complete when:

- every mandatory product, network, dictionary, and scheme has a documented record and terminal status;
- every `verified` record passes its source, license, hash/count, mapping, and vector checks;
- all unresolved conflicts are represented as versioned records or explicit blockers;
- generated catalogue documentation exactly matches the source registry;
- the threat model covers every required scenario and contains no absolute security claim;
- the technology comparison either records the clean-machine and packaging evidence or an exact equipment/technical blocker, and leaves Rust + Avalonia/NativeAOT provisional unless every selection requirement passes;
- the mobile prototype either opens the shared synthetic vault and records physical-device normalization/KDF evidence or records the exact unavailable-device/technical blocker; format freeze remains prohibited while blocked;
- the filesystem report limits atomicity claims to tested combinations, describes temporary files precisely, and records unavailable removable-media evidence as a blocker rather than simulating it;
- every bundled word list is compatible with both its own license and the selected SignPath signing arrangement;
- mandatory research CI checks pass at the exact commit, while the separate release-readiness result may honestly remain `NO-GO`;
- no real secrets or user-specific paths appear in tracked files or history;
- blockers that prevent Windows v1 are reported with evidence and an exact requested acceptance change.

Research completion never grants Windows release permission. The next subproject may begin only after these artifacts are reviewed and the required release blockers are understood; Windows release remains prohibited until every mandatory blocker is resolved or the owner separately changes the affected acceptance criterion.
