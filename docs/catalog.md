# Tessaveil catalogue

> Generated from catalog/*. Do not edit; run `python -m tools.catalog.cli generate --root .`.

Research only. A verified record is only a candidate for later table creation. Shared dictionaries do not imply compatible schemes. No key derivation or complete phrase validation. External secrets are never stored.

Release readiness: NO-GO; catalogue validation does not resolve physical-device, clean-machine, filesystem, audit or release gates.

## Product index

| Product / profile | Platform / mode | Networks | Scheme | Status |
| --- | --- | --- | --- | --- |
| Cake Wallet / [cake-wallet-decred](#wallet-cake-wallet-decred) | android / native-15-import | decred | [cake-decred-15](#scheme-cake-decred-15) | documented |
| Cake Wallet / [cake-wallet-decred-bip39](#wallet-cake-wallet-decred-bip39) | android / bip39-shaped-12-24 | decred | [cake-decred-bip39-12-24](#scheme-cake-decred-bip39-12-24) | blocked |
| Cake Wallet Monero / [cake-wallet-monero](#wallet-cake-wallet-monero) | android / polyseed-16-generated | monero | [polyseed-16](#scheme-polyseed-16) | documented |
| Cake Wallet Monero / [cake-wallet-monero-bip39](#wallet-cake-wallet-monero-bip39) | android / bip39-monero-generated-unresolved | monero | — | documented |
| Cake Wallet Monero / [cake-wallet-monero-legacy](#wallet-cake-wallet-monero-legacy) | android / legacy-25-generated | monero | [monero-legacy](#scheme-monero-legacy) | documented |
| Cake Wallet Zano — native seed import / [cake-wallet-zano](#wallet-cake-wallet-zano) | android / native26-import | zano | [zano-modern](#scheme-zano-modern) | documented |
| Cake Wallet Zano — BIP39 creation / [cake-wallet-zano-bip39](#wallet-cake-wallet-zano-bip39) | android / bip39-derived-create | zano | [cake-zano-bip39](#scheme-cake-zano-bip39) | blocked |
| Chia reference wallet — default English24 / [chia-wallet](#wallet-chia-wallet) | windows / english24-generate | chia | [chia-bip39](#scheme-chia-bip39) | documented |
| Daedalus / [daedalus](#wallet-daedalus) | windows / icarus-24-created | cardano | [cardano-icarus-24](#scheme-cardano-icarus-24) | documented |
| Daedalus / [daedalus-byron](#wallet-daedalus-byron) | windows / byron-12-import | cardano | [cardano-byron](#scheme-cardano-byron) | documented |
| Daedalus / [daedalus-paper-27](#wallet-daedalus-paper-27) | windows / byron-paper-27-import | cardano | [cardano-daedalus-27](#scheme-cardano-daedalus-27) | documented |
| Daedalus / [daedalus-yoroi-15](#wallet-daedalus-yoroi-15) | windows / icarus-15-import | cardano | [cardano-icarus-15](#scheme-cardano-icarus-15) | documented |
| Decrediton / [decrediton](#wallet-decrediton) | windows / native-pgp33 | decred | [decred-pgp33](#scheme-decred-pgp33) | documented |
| Defly / [defly](#wallet-defly) | android / native-account-created-backup-unresolved | algorand | — | blocked |
| Electrum / [electrum](#wallet-electrum) | windows / native-english-segwit | bitcoin | [electrum-v2](#scheme-electrum-v2) | documented |
| Electrum / [electrum-bip39-import](#wallet-electrum-bip39-import) | windows / bip39-import | bitcoin | [bip39](#scheme-bip39) | documented |
| Electrum / [electrum-v1-import](#wallet-electrum-v1-import) | windows / legacy-v1-import | bitcoin | [electrum-v1](#scheme-electrum-v1) | blocked |
| Eternl / [eternl](#wallet-eternl) | web / software-recovery-24-unresolved | cardano | — | blocked |
| Exodus / [exodus-monero-export](#wallet-exodus-monero-export) | windows / monero-25-export | monero | [monero-legacy](#scheme-monero-legacy) | documented |
| Feather / [feather](#wallet-feather) | windows / polyseed-16-generated | monero | [polyseed-16](#scheme-polyseed-16) | documented |
| Feather / [feather-legacy-import](#wallet-feather-legacy-import) | windows / legacy-25-import | monero | [monero-legacy](#scheme-monero-legacy) | documented |
| Gram Wallet / [gram-wallet](#wallet-gram-wallet) | android / mnemonic-backup-unresolved | ton | — | documented |
| Lace / [lace](#wallet-lace) | web / software-24-created-unresolved | cardano | — | documented |
| Monero CLI / [monero-cli-polyseed](#wallet-monero-cli-polyseed) | windows / polyseed-16-generated | monero | [polyseed-16](#scheme-polyseed-16) | documented |
| Monero CLI / [monero-gui-cli](#wallet-monero-gui-cli) | windows / legacy-25-generated | monero | [monero-legacy](#scheme-monero-legacy) | documented |
| Monero GUI / [monero-gui](#wallet-monero-gui) | windows / generated-seed-unresolved | monero | — | documented |
| MyMonero / [mymonero](#wallet-mymonero) | windows / legacy-13-restore | monero | [mymonero-13](#scheme-mymonero-13) | documented |
| MyMonero / [mymonero-generated](#wallet-mymonero-generated) | windows / generated-backup-unresolved | monero | — | documented |
| My Wallet / MyTonWallet / [mytonwallet](#wallet-mytonwallet) | web / bip39-multichain-generated | ton | [ton-multichain-bip39](#scheme-ton-multichain-bip39) | documented |
| My Wallet / MyTonWallet — TON only / [mytonwallet-native](#wallet-mytonwallet-native) | web / ton-native-generated | ton | [ton-native](#scheme-ton-native) | verified |
| Nami / [nami](#wallet-nami) | web / icarus-24-created | cardano | [cardano-icarus-24](#scheme-cardano-icarus-24) | documented |
| OpenMask / [openmask](#wallet-openmask) | web / ton-native-generated | ton | [ton-native](#scheme-ton-native) | documented |
| Pera Wallet / [pera-wallet](#wallet-pera-wallet) | ios / legacy-algo25-existing-backup-export | algorand | [algorand-25](#scheme-algorand-25) | documented |
| Pera Wallet / [pera-wallet-universal](#wallet-pera-wallet-universal) | ios / universal-hd24-created | algorand | — | documented |
| Polkadot.js extension / [polkadot-js](#wallet-polkadot-js) | web / sr25519-default-12 | kusama, polkadot | [substrate-bip39](#scheme-substrate-bip39) | documented |
| Sia-UI v1.3.3 — legacy import / [sia-ui](#wallet-sia-ui) | windows / legacy28-import | sia | [sia-legacy-28](#scheme-sia-legacy-28) | documented |
| Sia-UI v1.3.3 — legacy29 import / [sia-ui-29](#wallet-sia-ui-29) | windows / legacy29-import | sia | [sia-legacy-29](#scheme-sia-legacy-29) | documented |
| Sia walletd UI0.36.2 — seed mode / [sia-walletd](#wallet-sia-walletd) | web / english12-create | sia | [sia-bip39](#scheme-sia-bip39) | documented |
| siad — legacy28 seed export / [siad](#wallet-siad) | linux / legacy28-export | sia | [sia-legacy-28](#scheme-sia-legacy-28) | documented |
| siad — legacy29 seed export / [siad-29](#wallet-siad-29) | linux / legacy29-export | sia | [sia-legacy-29](#scheme-sia-legacy-29) | documented |
| SubWallet / [subwallet](#wallet-subwallet) | web / general-sr25519 | kusama, polkadot | [substrate-bip39](#scheme-substrate-bip39) | documented |
| Talisman / [talisman](#wallet-talisman) | web / substrate-sr25519-12-24 | kusama, polkadot | [substrate-bip39](#scheme-substrate-bip39) | documented |
| Tonhub / [tonhub](#wallet-tonhub) | android / ton-native-generated | ton | [ton-native](#scheme-ton-native) | verified |
| Tonkeeper Classic / [tonkeeper-classic](#wallet-tonkeeper-classic) | web / ton-native-generated | ton | [ton-native](#scheme-ton-native) | verified |
| Keeper / Tonkeeper Multichain / [tonkeeper-multichain](#wallet-tonkeeper-multichain) | cross-platform / bip39-multichain-generated | ton | [ton-multichain-bip39](#scheme-ton-multichain-bip39) | documented |
| Trezor Model T / [trezor-model-t](#wallet-trezor-model-t) | hardware / suite-single-share-20-created | multi-chain | [slip39-share-20](#scheme-slip39-share-20) | documented |
| Trezor Model T / [trezor-model-t-multi-share](#wallet-trezor-model-t-multi-share) | hardware / suite-multi-share-20-created | multi-chain | [slip39-share-20](#scheme-slip39-share-20) | documented |
| Trezor Safe3 / [trezor-safe-3](#wallet-trezor-safe-3) | hardware / suite-single-share-20-created | multi-chain | [slip39-share-20](#scheme-slip39-share-20) | documented |
| Trezor Safe3 / [trezor-safe-3-multi-share](#wallet-trezor-safe-3-multi-share) | hardware / suite-multi-share-20-created | multi-chain | [slip39-share-20](#scheme-slip39-share-20) | documented |
| Trezor Safe5 / [trezor-safe-5](#wallet-trezor-safe-5) | hardware / suite-single-share-20-created | multi-chain | [slip39-share-20](#scheme-slip39-share-20) | documented |
| Trezor Safe5 / [trezor-safe-5-multi-share](#wallet-trezor-safe-5-multi-share) | hardware / suite-multi-share-20-created | multi-chain | [slip39-share-20](#scheme-slip39-share-20) | documented |
| Trezor Safe7 / [trezor-safe-7](#wallet-trezor-safe-7) | hardware / suite-single-share-20-created | multi-chain | [slip39-share-20](#scheme-slip39-share-20) | documented |
| Trezor Safe7 / [trezor-safe-7-multi-share](#wallet-trezor-safe-7-multi-share) | hardware / suite-multi-share-20-created | multi-chain | [slip39-share-20](#scheme-slip39-share-20) | documented |
| Typhon / [typhon](#wallet-typhon) | web / web-mnemonic-created-unresolved | cardano | — | blocked |
| TON Space / DeFi Account / [ton-space](#wallet-ton-space) | web / manual-mnemonic-backup | ton | — | documented |
| Yoroi / [yoroi](#wallet-yoroi) | web / icarus-15-created | cardano | [cardano-icarus-15](#scheme-cardano-icarus-15) | documented |
| Zallet — English24 generation / [zallet](#wallet-zallet) | linux / english24-generate | zcash | [zcash-bip39](#scheme-zcash-bip39) | documented |
| Zano CLI — native26 / [zano-wallet](#wallet-zano-wallet) | linux / native26 | zano | [zano-modern](#scheme-zano-modern) | documented |
| Zano CLI — legacy25 import / [zano-wallet-legacy25](#wallet-zano-wallet-legacy25) | linux / legacy25-import | zano | [zano-legacy-25](#scheme-zano-legacy-25) | documented |
| zcashd — English mnemonic mode / [zcash-official](#wallet-zcash-official) | linux / zip339-english24 | zcash | [zcash-bip39](#scheme-zcash-bip39) | documented |
| zcashd — standalone key export / [zcash-official-standalone](#wallet-zcash-official-standalone) | linux / standalone-key-export | zcash | — | no-mnemonic-confirmed |

## Network index

- algorand: [defly](#wallet-defly), [pera-wallet](#wallet-pera-wallet), [pera-wallet-universal](#wallet-pera-wallet-universal)
- bitcoin: [electrum](#wallet-electrum), [electrum-bip39-import](#wallet-electrum-bip39-import), [electrum-v1-import](#wallet-electrum-v1-import)
- cardano: [daedalus](#wallet-daedalus), [daedalus-byron](#wallet-daedalus-byron), [daedalus-paper-27](#wallet-daedalus-paper-27), [daedalus-yoroi-15](#wallet-daedalus-yoroi-15), [eternl](#wallet-eternl), [lace](#wallet-lace), [nami](#wallet-nami), [typhon](#wallet-typhon), [yoroi](#wallet-yoroi)
- chia: [chia-wallet](#wallet-chia-wallet)
- decred: [cake-wallet-decred](#wallet-cake-wallet-decred), [cake-wallet-decred-bip39](#wallet-cake-wallet-decred-bip39), [decrediton](#wallet-decrediton)
- kusama: [polkadot-js](#wallet-polkadot-js), [subwallet](#wallet-subwallet), [talisman](#wallet-talisman)
- monero: [cake-wallet-monero](#wallet-cake-wallet-monero), [cake-wallet-monero-bip39](#wallet-cake-wallet-monero-bip39), [cake-wallet-monero-legacy](#wallet-cake-wallet-monero-legacy), [exodus-monero-export](#wallet-exodus-monero-export), [feather](#wallet-feather), [feather-legacy-import](#wallet-feather-legacy-import), [monero-cli-polyseed](#wallet-monero-cli-polyseed), [monero-gui](#wallet-monero-gui), [monero-gui-cli](#wallet-monero-gui-cli), [mymonero](#wallet-mymonero), [mymonero-generated](#wallet-mymonero-generated)
- multi-chain: [trezor-model-t](#wallet-trezor-model-t), [trezor-model-t-multi-share](#wallet-trezor-model-t-multi-share), [trezor-safe-3](#wallet-trezor-safe-3), [trezor-safe-3-multi-share](#wallet-trezor-safe-3-multi-share), [trezor-safe-5](#wallet-trezor-safe-5), [trezor-safe-5-multi-share](#wallet-trezor-safe-5-multi-share), [trezor-safe-7](#wallet-trezor-safe-7), [trezor-safe-7-multi-share](#wallet-trezor-safe-7-multi-share)
- polkadot: [polkadot-js](#wallet-polkadot-js), [subwallet](#wallet-subwallet), [talisman](#wallet-talisman)
- sia: [sia-ui](#wallet-sia-ui), [sia-ui-29](#wallet-sia-ui-29), [sia-walletd](#wallet-sia-walletd), [siad](#wallet-siad), [siad-29](#wallet-siad-29)
- ton: [gram-wallet](#wallet-gram-wallet), [mytonwallet](#wallet-mytonwallet), [mytonwallet-native](#wallet-mytonwallet-native), [openmask](#wallet-openmask), [ton-space](#wallet-ton-space), [tonhub](#wallet-tonhub), [tonkeeper-classic](#wallet-tonkeeper-classic), [tonkeeper-multichain](#wallet-tonkeeper-multichain)
- zano: [cake-wallet-zano](#wallet-cake-wallet-zano), [cake-wallet-zano-bip39](#wallet-cake-wallet-zano-bip39), [zano-wallet](#wallet-zano-wallet), [zano-wallet-legacy25](#wallet-zano-wallet-legacy25)
- zcash: [zallet](#wallet-zallet), [zcash-official](#wallet-zcash-official), [zcash-official-standalone](#wallet-zcash-official-standalone)

## Wallet profiles

<a id="wallet-cake-wallet-decred"></a>

### Cake Wallet Decred — Android native15 import — cake-wallet-decred

- Source record: [cake-wallet-decred](../catalog/wallets/cake-wallet-decred.json)
- Status: documented
- Reason: Evidence is insufficient for selectable support.
- Guidance: Not selectable; use the wallet's own backup procedure.
- Version interval (min / max): source-9679f91a8c9f63d00500c2b7cc18daf00949bdef / source-9679f91a8c9f63d00500c2b7cc18daf00949bdef
- Verified on: 2026-09-29
- Historical: false
- Evidence: [decred-cake-build](../catalog/evidence/decred-cake-build.json), [decred-cake-create](../catalog/evidence/decred-cake-create.json), [decred-cake-dependency](../catalog/evidence/decred-cake-dependency.json), [decred-cake-dispatch](../catalog/evidence/decred-cake-dispatch.json), [decred-cake-doc](../catalog/evidence/decred-cake-doc.json), [decred-cake-native](../catalog/evidence/decred-cake-native.json), [decred-cake-seed](../catalog/evidence/decred-cake-seed.json)
- Evidence claim: Android build source pins decred/libwallet ecc4a5fb9594368777848de42d7e072d62406507. This proves declared source binding, not executed release-binary contents. No iOS/macOS/Windows parity inferred.
- Evidence claim: Pinned current Cake service creates BIP39 using strength256 only for requested24, otherwise128; it passes mnemonic and seedpass to native libwallet. restoreFromSeed forwards native15. No current15 generation claim and no Android binary tested.
- Evidence claim: Pinned libwallet requires dcrdex v1.0.5 resolved for review to full commit37585833528544f80dddd92dcdff10a78ad01e1f.
- Evidence claim: createWallet dispatches every15-word mnemonic to dcrdex native decoder,12/24 to libwallet BIP39-shaped decoder, otherwise errors. Thus ordinary15-word BIP39 input is not general BIP39 import here.
- Evidence claim: Retrieved2026-09-29 Seed Format text states15-word creation/restoration without exact app version. It conflicts with pinned current12/24 creation source; retain as dated unversioned documentation, not a current universal claim.
- Evidence claim: Native15 encodes18 entropy bytes \(144 bits\),2 big-endian Unix-day birthday bytes \(16 bits\),5 high SHA256 checksum bits as15 big-endian11-bit indices. Not BIP39 entropy semantics.
- Evidence claim: Native15 rejects nonempty seedpass and transforms18-byte entropy by BLAKE256\(entropy \|\| big-endian uint32\(42\)\); BIP39-shaped12/24 applies passphrase even empty. Local wallet encryption password is separate.
- Aliases: —
- Scheme: [cake-decred-15](#scheme-cake-decred-15)
- Generates mnemonic / import only: false / true
- Limitations: Source-bound native15 restore. Documentation15 creation is unversioned and conflicts with current12/24 creation; exact historical creation interval unresolved. No iOS/macOS parity or BIP39-15 compatibility.; Non-selectable\: exact released artifact and independent wallet recovery not verified. A source commit is a singleton evidence boundary, not an all-version support promise.
- Profile guidance: Use the original wallet backup procedure and match exact product, platform, version and mode. Never enter a complete phrase or external recovery secret into Tessaveil.

<a id="wallet-cake-wallet-decred-bip39"></a>

### Cake Wallet Decred — Android current12/24 creation — cake-wallet-decred-bip39

- Source record: [cake-wallet-decred-bip39](../catalog/wallets/cake-wallet-decred-bip39.json)
- Status: blocked
- Reason: Support is blocked; see evidence and license decisions below.
- Guidance: Not selectable; use the wallet's own backup procedure.
- Version interval (min / max): source-9679f91a8c9f63d00500c2b7cc18daf00949bdef / source-9679f91a8c9f63d00500c2b7cc18daf00949bdef
- Verified on: 2026-09-29
- Historical: false
- Evidence: [decred-cake-build](../catalog/evidence/decred-cake-build.json), [decred-cake-create](../catalog/evidence/decred-cake-create.json), [decred-cake-doc](../catalog/evidence/decred-cake-doc.json), [decred-cake-nfc](../catalog/evidence/decred-cake-nfc.json)
- Evidence claim: Android build source pins decred/libwallet ecc4a5fb9594368777848de42d7e072d62406507. This proves declared source binding, not executed release-binary contents. No iOS/macOS/Windows parity inferred.
- Evidence claim: Pinned current Cake service creates BIP39 using strength256 only for requested24, otherwise128; it passes mnemonic and seedpass to native libwallet. restoreFromSeed forwards native15. No current15 generation claim and no Android binary tested.
- Evidence claim: Retrieved2026-09-29 Seed Format text states15-word creation/restoration without exact app version. It conflicts with pinned current12/24 creation source; retain as dated unversioned documentation, not a current universal claim.
- Evidence claim: ApplyPassphrase normalizes words/pass to NFC, while BIP39 requires NFKD. ASCII examples do not establish general compatibility. Keep source-specific12/24 profile blocked pending Unicode behavior and released-artifact recovery review.
- Aliases: —
- Scheme: [cake-decred-bip39-12-24](#scheme-cake-decred-bip39-12-24)
- Generates mnemonic / import only: true / false
- Limitations: Blocked NFC versus normative BIP39 NFKD passphrase behavior; Dart prevalidation is not native format proof. No released-binary/Unicode recovery verified.; Non-selectable\: exact released artifact and independent wallet recovery not verified. A source commit is a singleton evidence boundary, not an all-version support promise.
- Profile guidance: Use the original wallet backup procedure and match exact product, platform, version and mode. Never enter a complete phrase or external recovery secret into Tessaveil.

<a id="wallet-cake-wallet-monero"></a>

### Cake Wallet Monero — Polyseed creation — cake-wallet-monero

- Source record: [cake-wallet-monero](../catalog/wallets/cake-wallet-monero.json)
- Status: documented
- Reason: Evidence is insufficient for selectable support.
- Guidance: Not selectable; use the wallet's own backup procedure.
- Version interval (min / max): source-9679f91a8c9f63d00500c2b7cc18daf00949bdef / source-9679f91a8c9f63d00500c2b7cc18daf00949bdef
- Verified on: 2026-09-29
- Historical: false
- Evidence: [monero-cake-export](../catalog/evidence/monero-cake-export.json), [monero-cake-seed](../catalog/evidence/monero-cake-seed.json), [monero-cake-ui](../catalog/evidence/monero-cake-ui.json), [monero-cake-version](../catalog/evidence/monero-cake-version.json), [monero-cake-wallet-monero-wallet](../catalog/evidence/monero-cake-wallet-monero-wallet.json)
- Evidence claim: Backup UI obtains wallet.seed; separate from import service branches. Reviewed 2026-09-29; response byte SHA-256 e57829ad9284056ec12b705e5e2c289434a6d952966ad232adfaca0c8616986c. See docs/research/batches/monero-polyseed.md.
- Evidence claim: seed getter delegates getSeed; separate seedLegacy helper exists. Runtime artifact not executed. Reviewed 2026-09-29; response byte SHA-256 a5b4e7ef6cfa274eec62670850358f433c26c0f19cdea5cf1f081592e3712e68. See docs/research/batches/monero-polyseed.md.
- Evidence claim: Explicit legacy 25, Polyseed 16 \(default\), BIP39 12 mode labels. Reviewed 2026-09-29; response byte SHA-256 04848d36e285949e61e16b53c9cd9589d0896eaf3921575ea86fba983ad6d5fe. See docs/research/batches/monero-polyseed.md.
- Evidence claim: Root version template 0.0.0 is not a released version; source SHA singleton only. Reviewed 2026-09-29; response byte SHA-256 bc50a0936bf299070e19fcd721af9d5c76f374da719d720cea8ff029f289a21b. See docs/research/batches/monero-polyseed.md.
- Evidence claim: Android source snapshot only; default seedType=polyseed, Polyseed.create and separate legacy/bip39 branches. Generated pubspec version is 0.0.0 placeholder\: exact commit is the version bound, not an invented release. Reviewed 2026-09-29; response byte SHA-256 9e0591a1fa987aa48ad876fecdb5ad41b77accd8cdd9fc2a382a90563148d727. See docs/research/batches/monero-polyseed.md.
- Aliases: —
- Scheme: [polyseed-16](#scheme-polyseed-16)
- Generates mnemonic / import only: true / false
- Limitations: Android source snapshot only; default seedType=polyseed, Polyseed.create and separate legacy/bip39 branches. Generated pubspec version is 0.0.0 placeholder\: exact commit is the version bound, not an invented release.; Documented, not selectable\: no exact released artifact and independent wallet-level recovery vector verified. Import, generation and export claims must be assessed separately.
- Profile guidance: Use the trusted original wallet backup/recovery procedure; match product, platform, exact version and concrete mode. Never type a full phrase into Tessaveil or a website.

<a id="wallet-cake-wallet-monero-bip39"></a>

### Cake Wallet Monero — BIP39-derived mode — cake-wallet-monero-bip39

- Source record: [cake-wallet-monero-bip39](../catalog/wallets/cake-wallet-monero-bip39.json)
- Status: documented
- Reason: Evidence is insufficient for selectable support.
- Guidance: Not selectable; use the wallet's own backup procedure.
- Version interval (min / max): source-9679f91a8c9f63d00500c2b7cc18daf00949bdef / source-9679f91a8c9f63d00500c2b7cc18daf00949bdef
- Verified on: 2026-09-29
- Historical: false
- Evidence: [monero-cake-ui](../catalog/evidence/monero-cake-ui.json), [monero-cake-version](../catalog/evidence/monero-cake-version.json), [monero-cake-wallet-monero-bip39-wallet](../catalog/evidence/monero-cake-wallet-monero-bip39-wallet.json)
- Evidence claim: Explicit legacy 25, Polyseed 16 \(default\), BIP39 12 mode labels. Reviewed 2026-09-29; response byte SHA-256 04848d36e285949e61e16b53c9cd9589d0896eaf3921575ea86fba983ad6d5fe. See docs/research/batches/monero-polyseed.md.
- Evidence claim: Root version template 0.0.0 is not a released version; source SHA singleton only. Reviewed 2026-09-29; response byte SHA-256 bc50a0936bf299070e19fcd721af9d5c76f374da719d720cea8ff029f289a21b. See docs/research/batches/monero-polyseed.md.
- Evidence claim: Distinct 12-word BIP39-derived mode exists in source; Monero derivation path/transform is not generic BIP39 wallet compatibility. Full mode research outside this three-scheme batch; leave unmapped and non-selectable, never substitute for Polyseed/legacy. Reviewed 2026-09-29; response byte SHA-256 18d553ebf4da1994bd39be740c417a8c708c5d54aff82d8c364fa4927cb8fd77. See docs/research/batches/monero-polyseed.md.
- Aliases: —
- Scheme: —
- Generates mnemonic / import only: true / false
- Limitations: Distinct 12-word BIP39-derived mode exists in source; Monero derivation path/transform is not generic BIP39 wallet compatibility. Full mode research outside this three-scheme batch; leave unmapped and non-selectable, never substitute for Polyseed/legacy.; Documented, not selectable\: no exact released artifact and independent wallet-level recovery vector verified. Import, generation and export claims must be assessed separately.
- Profile guidance: Use the trusted original wallet backup/recovery procedure; match product, platform, exact version and concrete mode. Never type a full phrase into Tessaveil or a website.

<a id="wallet-cake-wallet-monero-legacy"></a>

### Cake Wallet Monero — legacy creation — cake-wallet-monero-legacy

- Source record: [cake-wallet-monero-legacy](../catalog/wallets/cake-wallet-monero-legacy.json)
- Status: documented
- Reason: Evidence is insufficient for selectable support.
- Guidance: Not selectable; use the wallet's own backup procedure.
- Version interval (min / max): source-9679f91a8c9f63d00500c2b7cc18daf00949bdef / source-9679f91a8c9f63d00500c2b7cc18daf00949bdef
- Verified on: 2026-09-29
- Historical: false
- Evidence: [monero-cake-export](../catalog/evidence/monero-cake-export.json), [monero-cake-seed](../catalog/evidence/monero-cake-seed.json), [monero-cake-ui](../catalog/evidence/monero-cake-ui.json), [monero-cake-version](../catalog/evidence/monero-cake-version.json), [monero-cake-wallet-monero-legacy-wallet](../catalog/evidence/monero-cake-wallet-monero-legacy-wallet.json)
- Evidence claim: Backup UI obtains wallet.seed; separate from import service branches. Reviewed 2026-09-29; response byte SHA-256 e57829ad9284056ec12b705e5e2c289434a6d952966ad232adfaca0c8616986c. See docs/research/batches/monero-polyseed.md.
- Evidence claim: seed getter delegates getSeed; separate seedLegacy helper exists. Runtime artifact not executed. Reviewed 2026-09-29; response byte SHA-256 a5b4e7ef6cfa274eec62670850358f433c26c0f19cdea5cf1f081592e3712e68. See docs/research/batches/monero-polyseed.md.
- Evidence claim: Explicit legacy 25, Polyseed 16 \(default\), BIP39 12 mode labels. Reviewed 2026-09-29; response byte SHA-256 04848d36e285949e61e16b53c9cd9589d0896eaf3921575ea86fba983ad6d5fe. See docs/research/batches/monero-polyseed.md.
- Evidence claim: Root version template 0.0.0 is not a released version; source SHA singleton only. Reviewed 2026-09-29; response byte SHA-256 bc50a0936bf299070e19fcd721af9d5c76f374da719d720cea8ff029f289a21b. See docs/research/batches/monero-polyseed.md.
- Evidence claim: Separate legacy creation branch delegates native createWallet; UI labels 25 words. FFI/dependency artifact binding and full recovery vector remain unresolved; no iOS/desktop claim. Reviewed 2026-09-29; response byte SHA-256 9e0591a1fa987aa48ad876fecdb5ad41b77accd8cdd9fc2a382a90563148d727. See docs/research/batches/monero-polyseed.md.
- Aliases: —
- Scheme: [monero-legacy](#scheme-monero-legacy)
- Generates mnemonic / import only: true / false
- Limitations: Separate legacy creation branch delegates native createWallet; UI labels 25 words. FFI/dependency artifact binding and full recovery vector remain unresolved; no iOS/desktop claim.; Documented, not selectable\: no exact released artifact and independent wallet-level recovery vector verified. Import, generation and export claims must be assessed separately.
- Profile guidance: Use the trusted original wallet backup/recovery procedure; match product, platform, exact version and concrete mode. Never type a full phrase into Tessaveil or a website.

<a id="wallet-cake-wallet-zano"></a>

### Cake Wallet Zano — native seed import — cake-wallet-zano

- Source record: [cake-wallet-zano](../catalog/wallets/cake-wallet-zano.json)
- Status: documented
- Reason: Evidence is insufficient for selectable support.
- Guidance: Not selectable; use the wallet's own backup procedure.
- Version interval (min / max): 9679f91a8c9f63d00500c2b7cc18daf00949bdef / 9679f91a8c9f63d00500c2b7cc18daf00949bdef
- Verified on: 2026-09-29
- Historical: false
- Evidence: [zano-cake-modes](../catalog/evidence/zano-cake-modes.json)
- Evidence claim: Pinned Cake Android-targeted source creates12/24 BIP39 mnemonics, dispatches BIP39 restore separately from native Zano seed restore. No current native26 creation assertion; native backend release binding unresolved.
- Aliases: —
- Scheme: [zano-modern](#scheme-zano-modern)
- Generates mnemonic / import only: false / true
- Limitations: Native seed restore dispatch shown; native library pin/accepted lengths unresolved. No current native26 creation claim.; Non-selectable\: exact shipped binary/dependency binding and independent restoration were not verified. Singleton source boundary is not an all-version compatibility claim.
- Profile guidance: Match original product, platform, version and mode; use its native backup procedure. Never enter a complete phrase, private key or external secret into Tessaveil.

<a id="wallet-cake-wallet-zano-bip39"></a>

### Cake Wallet Zano — BIP39 creation — cake-wallet-zano-bip39

- Source record: [cake-wallet-zano-bip39](../catalog/wallets/cake-wallet-zano-bip39.json)
- Status: blocked
- Reason: Support is blocked; see evidence and license decisions below.
- Guidance: Not selectable; use the wallet's own backup procedure.
- Version interval (min / max): 9679f91a8c9f63d00500c2b7cc18daf00949bdef / 9679f91a8c9f63d00500c2b7cc18daf00949bdef
- Verified on: 2026-09-29
- Historical: false
- Evidence: [zano-cake-bip39](../catalog/evidence/zano-cake-bip39.json), [zano-cake-modes](../catalog/evidence/zano-cake-modes.json)
- Evidence claim: Cake calls bip39 then BIP32 hardened44, hardened128, hardened0, child0, child0 and reduces private-key bytes as a little-endian integer modulo Ed25519 order. Exact Dart dependency byte/normalization and native binary binding not verified; own blocked scheme, no native26 compatibility inference.
- Evidence claim: Pinned Cake Android-targeted source creates12/24 BIP39 mnemonics, dispatches BIP39 restore separately from native Zano seed restore. No current native26 creation assertion; native backend release binding unresolved.
- Aliases: —
- Scheme: [cake-zano-bip39](#scheme-cake-zano-bip39)
- Generates mnemonic / import only: true / false
- Limitations: 12/24 creation source differs from native26; dependency normalization and binary parity unresolved.; Non-selectable\: exact shipped binary/dependency binding and independent restoration were not verified. Singleton source boundary is not an all-version compatibility claim.
- Profile guidance: Match original product, platform, version and mode; use its native backup procedure. Never enter a complete phrase, private key or external secret into Tessaveil.

<a id="wallet-chia-wallet"></a>

### Chia reference wallet — default English24 — chia-wallet

- Source record: [chia-wallet](../catalog/wallets/chia-wallet.json)
- Status: documented
- Reason: Evidence is insufficient for selectable support.
- Guidance: Not selectable; use the wallet's own backup procedure.
- Version interval (min / max): af0d7eab5fb12bbd8af51f47a7123ee700d74c2a / af0d7eab5fb12bbd8af51f47a7123ee700d74c2a
- Verified on: 2026-09-29
- Historical: false
- Evidence: [chia-source](../catalog/evidence/chia-source.json), [chia-vectors](../catalog/evidence/chia-vectors.json)
- Evidence claim: generate\_mnemonic uses32 random bytes =&gt;24 BIP39-English words. mnemonic\_to\_seed normalizes NFKD, PBKDF2-HMAC-SHA5122048, salt mnemonic with no user extension. Master keyring passphrase is separate; BLS derivation is not BIP32.
- Evidence claim: 24 published English entropy/mnemonic/empty-passphrase seed vectors projected to indices and expected seed fingerprints. Includes12/18/24 primitive cases; generation profile remains24 only.
- Aliases: —
- Scheme: [chia-bip39](#scheme-chia-bip39)
- Generates mnemonic / import only: true / false
- Limitations: Keyring master password does not extend mnemonic. Import primitive lengths/prefixes do not prove GUI generation choices.; Non-selectable\: exact shipped binary/dependency binding and independent restoration were not verified. Singleton source boundary is not an all-version compatibility claim.
- Profile guidance: Match original product, platform, version and mode; use its native backup procedure. Never enter a complete phrase, private key or external secret into Tessaveil.

<a id="wallet-daedalus"></a>

### Daedalus — Windows24 creation — daedalus

- Source record: [daedalus](../catalog/wallets/daedalus.json)
- Status: documented
- Reason: Evidence is insufficient for selectable support.
- Guidance: Not selectable; use the wallet's own backup procedure.
- Version interval (min / max): 11.4.0-source-6c57eb94753211f66d3a63f49d031bf746044755 / 11.4.0-source-6c57eb94753211f66d3a63f49d031bf746044755
- Verified on: 2026-09-29
- Historical: false
- Evidence: [cardano-daedalus-create](../catalog/evidence/cardano-daedalus-create.json), [cardano-daedalus-lengths](../catalog/evidence/cardano-daedalus-lengths.json), [cardano-daedalus-version](../catalog/evidence/cardano-daedalus-version.json)
- Evidence claim: getWalletRecoveryPhrase calls generateAccountMnemonics\(WALLET\_RECOVERY\_PHRASE\_WORD\_COUNT\); cryptoConfig defines24. English list supplied in crypto.ts. No current27-word creation inferred. See docs/research/batches/slip39-algorand-cardano.md. Retrieved byte SHA-256 55fdbd3fd1851cf46fee7444bb90323ff440e46f99dbe30fb67d2cfc36991d7c.
- Evidence claim: Explicit constants distinguish regular 24, legacy12, Yoroi15 and paper 27, split18 printed plus9 written. Constants do not prove creation routes; api and restore mapping evidence are separate. See docs/research/batches/slip39-algorand-cardano.md. Retrieved byte SHA-256 58d94791c7826fca095e4f56e213ea04cd69a4cd915eab0b7cb3103b8f35a265.
- Evidence claim: Source package version11.4.0 at full SHA; this is a source singleton, not attestation of downloaded binary. See docs/research/batches/slip39-algorand-cardano.md. Retrieved byte SHA-256 4af61443fb0bf72a23c1ee4aa5faaf70adc5cced3a3d6e358e91f4cdf2bf73c8.
- Aliases: —
- Scheme: [cardano-icarus-24](#scheme-cardano-icarus-24)
- Generates mnemonic / import only: true / false
- Limitations: Regular software creation uses 24 English words. Exact backend dependency/binary recovery not verified. Separate legacy/foreign restore modes are not new-wallet choices. Seed display at creation does not establish later export.; Non-selectable\: exact released-artifact binding and independent wallet recovery have not been verified. A dated unresolved-version marker is not a release interval; false generation means no generation claim for this specific record, not proof of absence.
- Profile guidance: Use the original trusted wallet backup/recovery procedure. Match product, platform, exact version and specific mode. Never enter a complete phrase/share or extra passphrase into Tessaveil.

<a id="wallet-daedalus-byron"></a>

### Daedalus — byron-12-import — daedalus-byron

- Source record: [daedalus-byron](../catalog/wallets/daedalus-byron.json)
- Status: documented
- Reason: Evidence is insufficient for selectable support.
- Guidance: Not selectable; use the wallet's own backup procedure.
- Version interval (min / max): 11.4.0-source-6c57eb94753211f66d3a63f49d031bf746044755 / 11.4.0-source-6c57eb94753211f66d3a63f49d031bf746044755
- Verified on: 2026-09-29
- Historical: true
- Evidence: [cardano-daedalus-lengths](../catalog/evidence/cardano-daedalus-lengths.json), [cardano-daedalus-restore](../catalog/evidence/cardano-daedalus-restore.json), [cardano-daedalus-version](../catalog/evidence/cardano-daedalus-version.json)
- Evidence claim: Explicit constants distinguish regular 24, legacy12, Yoroi15 and paper 27, split18 printed plus9 written. Constants do not prove creation routes; api and restore mapping evidence are separate. See docs/research/batches/slip39-algorand-cardano.md. Retrieved byte SHA-256 58d94791c7826fca095e4f56e213ea04cd69a4cd915eab0b7cb3103b8f35a265.
- Evidence claim: Restore options map regular24, legacy Byron 12, Yoroi15, and certificate 27 separately. Import capability is not evidence of current12/15/27 creation. See docs/research/batches/slip39-algorand-cardano.md. Retrieved byte SHA-256 2535b05897dc65e3dbb3654462c426ca07ad12eb62f957dbbf88f77321b93e85.
- Evidence claim: Source package version11.4.0 at full SHA; this is a source singleton, not attestation of downloaded binary. See docs/research/batches/slip39-algorand-cardano.md. Retrieved byte SHA-256 4af61443fb0bf72a23c1ee4aa5faaf70adc5cced3a3d6e358e91f4cdf2bf73c8.
- Aliases: —
- Scheme: [cardano-byron](#scheme-cardano-byron)
- Generates mnemonic / import only: false / true
- Limitations: Historical random/Byron 12 import.; Non-selectable\: exact released-artifact binding and independent wallet recovery have not been verified. A dated unresolved-version marker is not a release interval; false generation means no generation claim for this specific record, not proof of absence.
- Profile guidance: Use the original trusted wallet backup/recovery procedure. Match product, platform, exact version and specific mode. Never enter a complete phrase/share or extra passphrase into Tessaveil.

<a id="wallet-daedalus-paper-27"></a>

### Daedalus — byron-paper-27-import — daedalus-paper-27

- Source record: [daedalus-paper-27](../catalog/wallets/daedalus-paper-27.json)
- Status: documented
- Reason: Evidence is insufficient for selectable support.
- Guidance: Not selectable; use the wallet's own backup procedure.
- Version interval (min / max): 11.4.0-source-6c57eb94753211f66d3a63f49d031bf746044755 / 11.4.0-source-6c57eb94753211f66d3a63f49d031bf746044755
- Verified on: 2026-09-29
- Historical: true
- Evidence: [cardano-daedalus-lengths](../catalog/evidence/cardano-daedalus-lengths.json), [cardano-daedalus-restore](../catalog/evidence/cardano-daedalus-restore.json), [cardano-daedalus-version](../catalog/evidence/cardano-daedalus-version.json), [cardano-paper-rules](../catalog/evidence/cardano-paper-rules.json)
- Evidence claim: Explicit constants distinguish regular 24, legacy12, Yoroi15 and paper 27, split18 printed plus9 written. Constants do not prove creation routes; api and restore mapping evidence are separate. See docs/research/batches/slip39-algorand-cardano.md. Retrieved byte SHA-256 58d94791c7826fca095e4f56e213ea04cd69a4cd915eab0b7cb3103b8f35a265.
- Evidence claim: Restore options map regular24, legacy Byron 12, Yoroi15, and certificate 27 separately. Import capability is not evidence of current12/15/27 creation. See docs/research/batches/slip39-algorand-cardano.md. Retrieved byte SHA-256 2535b05897dc65e3dbb3654462c426ca07ad12eb62f957dbbf88f77321b93e85.
- Evidence claim: Source package version11.4.0 at full SHA; this is a source singleton, not attestation of downloaded binary. See docs/research/batches/slip39-algorand-cardano.md. Retrieved byte SHA-256 4af61443fb0bf72a23c1ee4aa5faaf70adc5cced3a3d6e358e91f4cdf2bf73c8.
- Evidence claim: getScrambledInput separates first18 scrambled certificate words and last9 password words. PBKDF2-HMAC-SHA512 of nine-word suffix with mnemonic salt, 2048 rounds, 32 bytes; rust-cardano-crypto performs unscrambling. This is not a 27-word BIP39 phrase. Nine words are inside27, not an extra user secret. See docs/research/batches/slip39-algorand-cardano.md. Retrieved byte SHA-256 02c137b08bf4394f95afeaf6e81a538ff39b15719fe326b8dbf1728c1a04cfd4.
- Aliases: —
- Scheme: [cardano-daedalus-27](#scheme-cardano-daedalus-27)
- Generates mnemonic / import only: false / true
- Limitations: Historical18\+9 paper certificate import; no current reachable paper creation proven.; Non-selectable\: exact released-artifact binding and independent wallet recovery have not been verified. A dated unresolved-version marker is not a release interval; false generation means no generation claim for this specific record, not proof of absence.
- Profile guidance: Use the original trusted wallet backup/recovery procedure. Match product, platform, exact version and specific mode. Never enter a complete phrase/share or extra passphrase into Tessaveil.

<a id="wallet-daedalus-yoroi-15"></a>

### Daedalus — icarus-15-import — daedalus-yoroi-15

- Source record: [daedalus-yoroi-15](../catalog/wallets/daedalus-yoroi-15.json)
- Status: documented
- Reason: Evidence is insufficient for selectable support.
- Guidance: Not selectable; use the wallet's own backup procedure.
- Version interval (min / max): 11.4.0-source-6c57eb94753211f66d3a63f49d031bf746044755 / 11.4.0-source-6c57eb94753211f66d3a63f49d031bf746044755
- Verified on: 2026-09-29
- Historical: false
- Evidence: [cardano-daedalus-lengths](../catalog/evidence/cardano-daedalus-lengths.json), [cardano-daedalus-restore](../catalog/evidence/cardano-daedalus-restore.json), [cardano-daedalus-version](../catalog/evidence/cardano-daedalus-version.json)
- Evidence claim: Explicit constants distinguish regular 24, legacy12, Yoroi15 and paper 27, split18 printed plus9 written. Constants do not prove creation routes; api and restore mapping evidence are separate. See docs/research/batches/slip39-algorand-cardano.md. Retrieved byte SHA-256 58d94791c7826fca095e4f56e213ea04cd69a4cd915eab0b7cb3103b8f35a265.
- Evidence claim: Restore options map regular24, legacy Byron 12, Yoroi15, and certificate 27 separately. Import capability is not evidence of current12/15/27 creation. See docs/research/batches/slip39-algorand-cardano.md. Retrieved byte SHA-256 2535b05897dc65e3dbb3654462c426ca07ad12eb62f957dbbf88f77321b93e85.
- Evidence claim: Source package version11.4.0 at full SHA; this is a source singleton, not attestation of downloaded binary. See docs/research/batches/slip39-algorand-cardano.md. Retrieved byte SHA-256 4af61443fb0bf72a23c1ee4aa5faaf70adc5cced3a3d6e358e91f4cdf2bf73c8.
- Aliases: —
- Scheme: [cardano-icarus-15](#scheme-cardano-icarus-15)
- Generates mnemonic / import only: false / true
- Limitations: Yoroi15 import is separate from Daedalus24 creation.; Non-selectable\: exact released-artifact binding and independent wallet recovery have not been verified. A dated unresolved-version marker is not a release interval; false generation means no generation claim for this specific record, not proof of absence.
- Profile guidance: Use the original trusted wallet backup/recovery procedure. Match product, platform, exact version and specific mode. Never enter a complete phrase/share or extra passphrase into Tessaveil.

<a id="wallet-decrediton"></a>

### Decrediton — Windows native PGP33 creation — decrediton

- Source record: [decrediton](../catalog/wallets/decrediton.json)
- Status: documented
- Reason: Evidence is insufficient for selectable support.
- Guidance: Not selectable; use the wallet's own backup procedure.
- Version interval (min / max): 2.1.6-source-942eed0b34d09316d753942abdbec8dc5320cbed / 2.1.6-source-942eed0b34d09316d753942abdbec8dc5320cbed
- Verified on: 2026-09-29
- Historical: false
- Evidence: [decred-bip39-doc](../catalog/evidence/decred-bip39-doc.json), [decred-decrediton-create](../catalog/evidence/decred-decrediton-create.json)
- Evidence claim: Official source documentation distinguishes PGP33 direct wallet seed from BIP39 sentence\+passphrase seed; describes external conversion to hex for Decrediton/dcrwallet. This does not prove native BIP39 phrase generation or direct phrase import in Decrediton.
- Evidence claim: Decrediton2.1.6-source generateSeed obtains a seed service response; createWallet accepts seed separately. Combined with official PGP33 docs this establishes software seed creation, not BIP39 creation. Exact backend binary binding remains unresolved.
- Aliases: —
- Scheme: [decred-pgp33](#scheme-decred-pgp33)
- Generates mnemonic / import only: true / false
- Limitations: Source2.1.6 and docs prove native seed creation; backend release binding and recovery not tested. BIP39 conversion to hex is external, not native phrase generation.; Non-selectable\: exact released artifact and independent wallet recovery not verified. A source commit is a singleton evidence boundary, not an all-version support promise.
- Profile guidance: Use the original wallet backup procedure and match exact product, platform, version and mode. Never enter a complete phrase or external recovery secret into Tessaveil.

<a id="wallet-defly"></a>

### Defly — native account backup unresolved — defly

- Source record: [defly](../catalog/wallets/defly.json)
- Status: blocked
- Reason: Support is blocked; see evidence and license decisions below.
- Guidance: Not selectable; use the wallet's own backup procedure.
- Version interval (min / max): app-version-unresolved-doc-2026-09-29 / app-version-unresolved-doc-2026-09-29
- Verified on: 2026-09-29
- Historical: false
- Evidence: [algorand-defly-create](../catalog/evidence/algorand-defly-create.json)
- Evidence claim: Create a New Account section describes new account and subsequent mnemonic display via backup reminder; import, Ledger and watch paths are separate. Exact word count, dictionary/derivation, app version and platform-specific behavior not in retrieved text. Do not infer25 from Algorand name. See docs/research/batches/slip39-algorand-cardano.md. Read through web retrieval; direct response was HTTP 403. No raw-body hash or immutable capture asserted.
- Aliases: —
- Scheme: —
- Generates mnemonic / import only: true / false
- Limitations: Manual proves account creation and mnemonic display; exact Android artifact, word count and semantics not proven.25-word mapping remains blocked. Android is the scoped research target, not proof of parity with iOS.; Non-selectable\: exact released-artifact binding and independent wallet recovery have not been verified. A dated unresolved-version marker is not a release interval; false generation means no generation claim for this specific record, not proof of absence.
- Profile guidance: Use the original trusted wallet backup/recovery procedure. Match product, platform, exact version and specific mode. Never enter a complete phrase/share or extra passphrase into Tessaveil.

<a id="wallet-electrum"></a>

### Electrum — Windows native English segwit — electrum

- Source record: [electrum](../catalog/wallets/electrum.json)
- Status: documented
- Reason: Evidence is insufficient for selectable support.
- Guidance: Not selectable; use the wallet's own backup procedure.
- Version interval (min / max): 4.8.2-source-ede66c89887234c83b0def133b3100fe92a160eb / 4.8.2-source-ede66c89887234c83b0def133b3100fe92a160eb
- Verified on: 2026-09-29
- Historical: false
- Evidence: [electrum-qt-create](../catalog/evidence/electrum-qt-create.json), [electrum-v2-source](../catalog/evidence/electrum-v2-source.json), [electrum-version](../catalog/evidence/electrum-version.json), [electrum-wizard-modes](../catalog/evidence/electrum-wizard-modes.json)
- Evidence claim: Qt WCCreateSeed selects default segwit \(standard only with WIZARD\_DONT\_CREATE\_SEGWIT\); creates English mnemonic and displays SeedWidget. This pins a native desktop creation flow, not just an import API.
- Evidence claim: Electrum 4.8.2-source\: default English 132-bit make\_seed uses HMAC-SHA512 Seed version prefixes, normalized sentence and electrum-prefixed PBKDF2 salt, not BIP39 entropy/checksum semantics. Old recognition accepts 12/24 words; native generation normally 12 with possible nonce overflow to 13. No wallet artifact tested.
- Evidence claim: Source package labels itself 4.8.2, with prefixes 01 standard, 100 segwit, 101 2FA, 102 2FA segwit; no release binary binding inferred.
- Evidence claim: Pinned wizard distinguishes old, standard, segwit and BIP39 restoration. BIP39 import is not native seed generation; two-factor/multisig are outside these Windows software profiles.
- Aliases: —
- Scheme: [electrum-v2](#scheme-electrum-v2)
- Generates mnemonic / import only: true / false
- Limitations: Scoped to native segwit source generation. Standard,2FA, multisig, Android, BIP39 import and legacy restore are different modes.; Non-selectable\: exact released artifact and independent wallet recovery not verified. A source commit is a singleton evidence boundary, not an all-version support promise.
- Profile guidance: Use the original wallet backup procedure and match exact product, platform, version and mode. Never enter a complete phrase or external recovery secret into Tessaveil.

<a id="wallet-electrum-bip39-import"></a>

### Electrum — Windows BIP39 import — electrum-bip39-import

- Source record: [electrum-bip39-import](../catalog/wallets/electrum-bip39-import.json)
- Status: documented
- Reason: Evidence is insufficient for selectable support.
- Guidance: Not selectable; use the wallet's own backup procedure.
- Version interval (min / max): 4.8.2-source-ede66c89887234c83b0def133b3100fe92a160eb / 4.8.2-source-ede66c89887234c83b0def133b3100fe92a160eb
- Verified on: 2026-09-29
- Historical: false
- Evidence: [electrum-version](../catalog/evidence/electrum-version.json), [electrum-wizard-modes](../catalog/evidence/electrum-wizard-modes.json)
- Evidence claim: Source package labels itself 4.8.2, with prefixes 01 standard, 100 segwit, 101 2FA, 102 2FA segwit; no release binary binding inferred.
- Evidence claim: Pinned wizard distinguishes old, standard, segwit and BIP39 restoration. BIP39 import is not native seed generation; two-factor/multisig are outside these Windows software profiles.
- Aliases: —
- Scheme: [bip39](#scheme-bip39)
- Generates mnemonic / import only: false / true
- Limitations: Native Electrum generation is not BIP39. Exact imported path and script selection require original backup metadata.; Non-selectable\: exact released artifact and independent wallet recovery not verified. A source commit is a singleton evidence boundary, not an all-version support promise.
- Profile guidance: Use the original wallet backup procedure and match exact product, platform, version and mode. Never enter a complete phrase or external recovery secret into Tessaveil.

<a id="wallet-electrum-v1-import"></a>

### Electrum — Windows legacy v1 restore — electrum-v1-import

- Source record: [electrum-v1-import](../catalog/wallets/electrum-v1-import.json)
- Status: blocked
- Reason: Support is blocked; see evidence and license decisions below.
- Guidance: Not selectable; use the wallet's own backup procedure.
- Version interval (min / max): 4.8.2-source-ede66c89887234c83b0def133b3100fe92a160eb / 4.8.2-source-ede66c89887234c83b0def133b3100fe92a160eb
- Verified on: 2026-09-29
- Historical: true
- Evidence: [electrum-v2-source](../catalog/evidence/electrum-v2-source.json), [electrum-version](../catalog/evidence/electrum-version.json), [electrum-wizard-modes](../catalog/evidence/electrum-wizard-modes.json)
- Evidence claim: Electrum 4.8.2-source\: default English 132-bit make\_seed uses HMAC-SHA512 Seed version prefixes, normalized sentence and electrum-prefixed PBKDF2 salt, not BIP39 entropy/checksum semantics. Old recognition accepts 12/24 words; native generation normally 12 with possible nonce overflow to 13. No wallet artifact tested.
- Evidence claim: Source package labels itself 4.8.2, with prefixes 01 standard, 100 segwit, 101 2FA, 102 2FA segwit; no release binary binding inferred.
- Evidence claim: Pinned wizard distinguishes old, standard, segwit and BIP39 restoration. BIP39 import is not native seed generation; two-factor/multisig are outside these Windows software profiles.
- Aliases: —
- Scheme: [electrum-v1](#scheme-electrum-v1)
- Generates mnemonic / import only: false / true
- Limitations: Legacy12/24 recognition only. No legacy dictionary bundled pending provenance/license review. No native v1 creation claimed.; Non-selectable\: exact released artifact and independent wallet recovery not verified. A source commit is a singleton evidence boundary, not an all-version support promise.
- Profile guidance: Use the original wallet backup procedure and match exact product, platform, version and mode. Never enter a complete phrase or external recovery secret into Tessaveil.

<a id="wallet-eternl"></a>

### Eternl — recovery24 unresolved — eternl

- Source record: [eternl](../catalog/wallets/eternl.json)
- Status: blocked
- Reason: Support is blocked; see evidence and license decisions below.
- Guidance: Not selectable; use the wallet's own backup procedure.
- Version interval (min / max): app-version-unresolved-doc-2026-09-29 / app-version-unresolved-doc-2026-09-29
- Verified on: 2026-09-29
- Historical: false
- Evidence: [cardano-eternl-doc](../catalog/evidence/cardano-eternl-doc.json)
- Evidence claim: Official recovery-phrase FAQ identifies24-word recovery. Retrieved text does not establish exact app version, concrete generation/export path or root-key algorithm. No inherited Cardano/Icarus support. See docs/research/batches/slip39-algorand-cardano.md. Read through web retrieval; direct response was HTTP 403. No raw-body hash or immutable capture asserted.
- Aliases: —
- Scheme: —
- Generates mnemonic / import only: false / false
- Limitations: 24-word recovery described, but generation versus later export, exact web version and derivation remain unproven. false generation is no evidence-backed claim, not a claim that Eternl cannot create wallets.; Non-selectable\: exact released-artifact binding and independent wallet recovery have not been verified. A dated unresolved-version marker is not a release interval; false generation means no generation claim for this specific record, not proof of absence.
- Profile guidance: Use the original trusted wallet backup/recovery procedure. Match product, platform, exact version and specific mode. Never enter a complete phrase/share or extra passphrase into Tessaveil.

<a id="wallet-exodus-monero-export"></a>

### Exodus Desktop — Monero 25-word export — exodus-monero-export

- Source record: [exodus-monero-export](../catalog/wallets/exodus-monero-export.json)
- Status: documented
- Reason: Evidence is insufficient for selectable support.
- Guidance: Not selectable; use the wallet's own backup procedure.
- Version interval (min / max): version-unresolved-doc-2026-01-20 / version-unresolved-doc-2026-01-20
- Verified on: 2026-09-29
- Historical: false
- Evidence: [monero-exodus-doc](../catalog/evidence/monero-exodus-doc.json)
- Evidence claim: Official article updated January 20 2026\: XMR support ended August 18 2025, but Desktop Settings/Assets/Monero Private Keys still exports a 25-word mnemonic. Mobile users must sync to Desktop. Cake restore instructions select Legacy 25 English. Article gives no app version interval; direct body retrieval was blocked \(HTTP 403\), so no body hash or immutable snapshot is claimed. Read through web retrieval.
- Aliases: Exodus Desktop
- Scheme: [monero-legacy](#scheme-monero-legacy)
- Generates mnemonic / import only: false / false
- Limitations: Export of an existing Monero wallet only; generates\_mnemonic=false does not deny export. App versions and full export derivation vector are unresolved, so documented/non-selectable.; Windows Desktop path documented \(Mac also mentioned but not generalized here\); Mobile must sync to Desktop. No 25-word import-into-Exodus or fresh XMR creation claim. The global Exodus 12-word backup is distinct.
- Profile guidance: Use the vendor migration instructions and a trusted compatible wallet; do not enter the full phrase in Tessaveil. XMR support cessation does not mean seed export is absent.

<a id="wallet-feather"></a>

### Feather — Polyseed creation — feather

- Source record: [feather](../catalog/wallets/feather.json)
- Status: documented
- Reason: Evidence is insufficient for selectable support.
- Guidance: Not selectable; use the wallet's own backup procedure.
- Version interval (min / max): 2.9.1-source-948773cf13c7486ee230eb67b6bac06b2f94c874 / 2.9.1-source-948773cf13c7486ee230eb67b6bac06b2f94c874
- Verified on: 2026-09-29
- Historical: false
- Evidence: [monero-feather-create](../catalog/evidence/monero-feather-create.json), [monero-feather-version](../catalog/evidence/monero-feather-version.json), [monero-feather-wallet](../catalog/evidence/monero-feather-wallet.json)
- Evidence claim: Creation rejects non-Polyseed and non-English; restoration handles Polyseed, Tevador 14 and legacy separately. Reviewed 2026-09-29; response byte SHA-256 dc79e1b6aace91076f1f9da96411706661830f55fda93926776d83e22d3ab8e5. See docs/research/batches/monero-polyseed.md.
- Evidence claim: Project version 2.9.1 at this source revision. Reviewed 2026-09-29; response byte SHA-256 d1eb1b67c42fbeb682a945225097cec2c434040d42d1ce583e640f9f6450e8b7. See docs/research/batches/monero-polyseed.md.
- Evidence claim: Feather 2.9.1 source\: new seeds are English Polyseed only. Source creation and display examined; no released-binary recovery/vector claim. Reviewed 2026-09-29; response byte SHA-256 53c8e05132d18d59a27df07231bbb4fe7a4aa0d559f5d32c28262810e73bce89. See docs/research/batches/monero-polyseed.md.
- Aliases: —
- Scheme: [polyseed-16](#scheme-polyseed-16)
- Generates mnemonic / import only: true / false
- Limitations: Feather 2.9.1 source\: new seeds are English Polyseed only. Source creation and display examined; no released-binary recovery/vector claim.; Documented, not selectable\: no exact released artifact and independent wallet-level recovery vector verified. Import, generation and export claims must be assessed separately.
- Profile guidance: Use the trusted original wallet backup/recovery procedure; match product, platform, exact version and concrete mode. Never type a full phrase into Tessaveil or a website.

<a id="wallet-feather-legacy-import"></a>

### Feather — legacy import — feather-legacy-import

- Source record: [feather-legacy-import](../catalog/wallets/feather-legacy-import.json)
- Status: documented
- Reason: Evidence is insufficient for selectable support.
- Guidance: Not selectable; use the wallet's own backup procedure.
- Version interval (min / max): 2.9.1-source-948773cf13c7486ee230eb67b6bac06b2f94c874 / 2.9.1-source-948773cf13c7486ee230eb67b6bac06b2f94c874
- Verified on: 2026-09-29
- Historical: false
- Evidence: [monero-feather-legacy-import-wallet](../catalog/evidence/monero-feather-legacy-import-wallet.json), [monero-feather-version](../catalog/evidence/monero-feather-version.json)
- Evidence claim: Legacy 25-word \(also checksumless 24-word\) restore is separate from generation. 14-word Tevador restore is another format and is not mapped to Polyseed/MyMonero. Reviewed 2026-09-29; response byte SHA-256 dc79e1b6aace91076f1f9da96411706661830f55fda93926776d83e22d3ab8e5. See docs/research/batches/monero-polyseed.md.
- Evidence claim: Project version 2.9.1 at this source revision. Reviewed 2026-09-29; response byte SHA-256 d1eb1b67c42fbeb682a945225097cec2c434040d42d1ce583e640f9f6450e8b7. See docs/research/batches/monero-polyseed.md.
- Aliases: —
- Scheme: [monero-legacy](#scheme-monero-legacy)
- Generates mnemonic / import only: false / true
- Limitations: Legacy 25-word \(also checksumless 24-word\) restore is separate from generation. 14-word Tevador restore is another format and is not mapped to Polyseed/MyMonero.; Documented, not selectable\: no exact released artifact and independent wallet-level recovery vector verified. Import, generation and export claims must be assessed separately.
- Profile guidance: Use the trusted original wallet backup/recovery procedure; match product, platform, exact version and concrete mode. Never type a full phrase into Tessaveil or a website.

<a id="wallet-gram-wallet"></a>

### Gram Wallet — gram-wallet

- Source record: [gram-wallet](../catalog/wallets/gram-wallet.json)
- Status: documented
- Reason: Evidence is insufficient for selectable support.
- Guidance: Not selectable; use the wallet's own backup procedure.
- Version interval (min / max): documentation-snapshot-2026-09-29-version-unresolved / documentation-snapshot-2026-09-29-version-unresolved
- Verified on: 2026-09-29
- Historical: false
- Evidence: [ton-gram-identity](../catalog/evidence/ton-gram-identity.json), [ton-gram-store](../catalog/evidence/ton-gram-store.json)
- Evidence claim: gramwallet.io identifies the current self-custodial TON wallet and links installation; current identity must not inherit historical Telegram Gram behavior. Reviewed 2026-09-29; byte SHA-256 c498efe1d81425f59fb294f1184c5a64ddd913c5cc22784759d2bd58691e7da2. See docs/research/batches/bip39-ton.md.
- Evidence claim: Publisher-provided listing identifies My Wallet Apps Ltd., Android package io.gramwallet.app, September 7 2026 update and shared My Wallet engine. It does not establish exact mnemonic generation/export or version boundary; user reviews are not evidence. Reviewed 2026-09-29; byte SHA-256 3f2c0e813940801893d846b36313173f6e7a2865b1bc41d80cc74fd1c90a2518. See docs/research/batches/bip39-ton.md.
- Aliases: Gram
- Scheme: —
- Generates mnemonic / import only: false / false
- Limitations: Identity fixed to My Wallet Apps Ltd., Android package io.gramwallet.app linked by gramwallet.io. Publisher says it uses My Wallet's engine; this does not prove a shared mnemonic algorithm or backup flow.; No exact app version, exportable phrase length, generation method or source-to-package binding established. generates\_mnemonic=false means generation is not confirmed, not that the product has no mnemonic.; Do not inherit the behavior of Telegram's historical Gram test wallet or other similarly named products.
- Profile guidance: Use the original trusted wallet's backup and recovery procedure. Match exact product, platform, source version and mode. Never enter a complete recovery phrase into Tessaveil or a website.

<a id="wallet-lace"></a>

### Lace — extension24 creation — lace

- Source record: [lace](../catalog/wallets/lace.json)
- Status: documented
- Reason: Evidence is insufficient for selectable support.
- Guidance: Not selectable; use the wallet's own backup procedure.
- Version interval (min / max): app-version-unresolved-doc-2026-07-14 / app-version-unresolved-doc-2026-07-14
- Verified on: 2026-09-29
- Historical: false
- Evidence: [cardano-lace-create](../catalog/evidence/cardano-lace-create.json)
- Evidence claim: Edited 2026-07-14 Route B\: browser-extension software wallet creates/displays24-word backup. Route A hardware connection creates no new phrase in Lace. Exact app version/derivation unspecified. See docs/research/batches/slip39-algorand-cardano.md. Retrieved byte SHA-256 ce02d32706cf597d8f3861e3040d487d7e8862020069ccdf6e40aa48b7a83f19.
- Aliases: —
- Scheme: —
- Generates mnemonic / import only: true / false
- Limitations: 24-word generation/display confirmed. No exact version or algorithm/library binding to Icarus established; leave unmapped. Modern PGP paper backup is not Daedalus27. Hardware pairing, import and mobile are distinct.; Non-selectable\: exact released-artifact binding and independent wallet recovery have not been verified. A dated unresolved-version marker is not a release interval; false generation means no generation claim for this specific record, not proof of absence.
- Profile guidance: Use the original trusted wallet backup/recovery procedure. Match product, platform, exact version and specific mode. Never enter a complete phrase/share or extra passphrase into Tessaveil.

<a id="wallet-monero-cli-polyseed"></a>

### Monero CLI — Polyseed creation — monero-cli-polyseed

- Source record: [monero-cli-polyseed](../catalog/wallets/monero-cli-polyseed.json)
- Status: documented
- Reason: Evidence is insufficient for selectable support.
- Guidance: Not selectable; use the wallet's own backup procedure.
- Version interval (min / max): source-2f9d1bbb2c553dc75f3335bd1452117dfddd86fa / source-2f9d1bbb2c553dc75f3335bd1452117dfddd86fa
- Verified on: 2026-09-29
- Historical: false
- Evidence: [monero-cli-version](../catalog/evidence/monero-cli-version.json), [monero-monero-cli-polyseed-wallet](../catalog/evidence/monero-monero-cli-polyseed-wallet.json)
- Evidence claim: Development source declares 0.18.1.0; exact commit singleton is authoritative, not a release range. Reviewed 2026-09-29; response byte SHA-256 cddb09cd7a59eefe5486766145baf2849a9161a504545a649d83e034a81ea83a. See docs/research/batches/monero-polyseed.md.
- Evidence claim: Default deterministic new-wallet source mode is Polyseed; --use-legacy-seed is a distinct simultaneous choice. Non-deterministic, multisig, hardware and view-only modes excluded. Reviewed 2026-09-29; response byte SHA-256 54534a83e1c17bf4d5176dbdb2c1293399575058ad4db3f58948c958bda3ff15. See docs/research/batches/monero-polyseed.md.
- Aliases: —
- Scheme: [polyseed-16](#scheme-polyseed-16)
- Generates mnemonic / import only: true / false
- Limitations: Default deterministic new-wallet source mode is Polyseed; --use-legacy-seed is a distinct simultaneous choice. Non-deterministic, multisig, hardware and view-only modes excluded.; Documented, not selectable\: no exact released artifact and independent wallet-level recovery vector verified. Import, generation and export claims must be assessed separately.
- Profile guidance: Use the trusted original wallet backup/recovery procedure; match product, platform, exact version and concrete mode. Never type a full phrase into Tessaveil or a website.

<a id="wallet-monero-gui"></a>

### Monero GUI — generated seed — monero-gui

- Source record: [monero-gui](../catalog/wallets/monero-gui.json)
- Status: documented
- Reason: Evidence is insufficient for selectable support.
- Guidance: Not selectable; use the wallet's own backup procedure.
- Version interval (min / max): source-01d6640aff7fd1c1a87932e14e8439383e1229c5 / source-01d6640aff7fd1c1a87932e14e8439383e1229c5
- Verified on: 2026-09-29
- Historical: false
- Evidence: [monero-monero-gui-wallet](../catalog/evidence/monero-monero-gui-wallet.json)
- Evidence claim: Wizard creates an in-memory wallet then displays wallet.seed. Exact pinned backend dependency and scheme are unresolved in this GUI snapshot; do not substitute current CLI behavior. Reviewed 2026-09-29; response byte SHA-256 ce321b1d39e21dfa6e50c36d07206f2d7d37acb8d4cef3d1c9225db473a6b7af. See docs/research/batches/monero-polyseed.md.
- Aliases: —
- Scheme: —
- Generates mnemonic / import only: true / false
- Limitations: Wizard creates an in-memory wallet then displays wallet.seed. Exact pinned backend dependency and scheme are unresolved in this GUI snapshot; do not substitute current CLI behavior.; Documented, not selectable\: no exact released artifact and independent wallet-level recovery vector verified. Import, generation and export claims must be assessed separately.
- Profile guidance: Use the trusted original wallet backup/recovery procedure; match product, platform, exact version and concrete mode. Never type a full phrase into Tessaveil or a website.

<a id="wallet-monero-gui-cli"></a>

### Monero CLI — legacy creation — monero-gui-cli

- Source record: [monero-gui-cli](../catalog/wallets/monero-gui-cli.json)
- Status: documented
- Reason: Evidence is insufficient for selectable support.
- Guidance: Not selectable; use the wallet's own backup procedure.
- Version interval (min / max): source-2f9d1bbb2c553dc75f3335bd1452117dfddd86fa / source-2f9d1bbb2c553dc75f3335bd1452117dfddd86fa
- Verified on: 2026-09-29
- Historical: false
- Evidence: [monero-cli-version](../catalog/evidence/monero-cli-version.json), [monero-monero-gui-cli-wallet](../catalog/evidence/monero-monero-gui-cli-wallet.json)
- Evidence claim: Development source declares 0.18.1.0; exact commit singleton is authoritative, not a release range. Reviewed 2026-09-29; response byte SHA-256 cddb09cd7a59eefe5486766145baf2849a9161a504545a649d83e034a81ea83a. See docs/research/batches/monero-polyseed.md.
- Evidence claim: Exact CLI source revision, explicit --use-legacy-seed mode. Default source creation is now Polyseed. GUI is a separate record; neither label implies all CLI/GUI versions. Reviewed 2026-09-29; response byte SHA-256 54534a83e1c17bf4d5176dbdb2c1293399575058ad4db3f58948c958bda3ff15. See docs/research/batches/monero-polyseed.md.
- Aliases: —
- Scheme: [monero-legacy](#scheme-monero-legacy)
- Generates mnemonic / import only: true / false
- Limitations: Exact CLI source revision, explicit --use-legacy-seed mode. Default source creation is now Polyseed. GUI is a separate record; neither label implies all CLI/GUI versions.; Documented, not selectable\: no exact released artifact and independent wallet-level recovery vector verified. Import, generation and export claims must be assessed separately.
- Profile guidance: Use the trusted original wallet backup/recovery procedure; match product, platform, exact version and concrete mode. Never type a full phrase into Tessaveil or a website.

<a id="wallet-mymonero"></a>

### MyMonero — legacy 13-word restoration — mymonero

- Source record: [mymonero](../catalog/wallets/mymonero.json)
- Status: documented
- Reason: Evidence is insufficient for selectable support.
- Guidance: Not selectable; use the wallet's own backup procedure.
- Version interval (min / max): 1.3.2-source-5c7455d30e4e20150962f5f74efd83477962a05e / 1.3.2-source-5c7455d30e4e20150962f5f74efd83477962a05e
- Verified on: 2026-09-29
- Historical: false
- Evidence: [monero-my-core](../catalog/evidence/monero-my-core.json), [monero-mymonero-wallet](../catalog/evidence/monero-mymonero-wallet.json)
- Evidence claim: new\_wallet creates 32-byte/25-word backups; decoded\_seed handles 13 and 25 and hashes 16-byte seeds. Core/app binding remains unproven. Reviewed 2026-09-29; response byte SHA-256 ea6d34729151cffd2b7cdd1a16c31507ff3122242540646ac9797cc0797bb7b4. See docs/research/batches/monero-polyseed.md.
- Evidence claim: App 1.3.2 source and core decoder source reviewed separately; exact app-to-core artifact binding is not established. Historical 13-word restore capability is documented in core, not a claim that current app creates 13 words. Reviewed 2026-09-29; response byte SHA-256 c00f3699d4f244e57dba1522665910687c0fdf2228edfc576f83a717dfc75457. See docs/research/batches/monero-polyseed.md.
- Aliases: —
- Scheme: [mymonero-13](#scheme-mymonero-13)
- Generates mnemonic / import only: false / true
- Limitations: App 1.3.2 source and core decoder source reviewed separately; exact app-to-core artifact binding is not established. Historical 13-word restore capability is documented in core, not a claim that current app creates 13 words.; Documented, not selectable\: no exact released artifact and independent wallet-level recovery vector verified. Import, generation and export claims must be assessed separately.
- Profile guidance: Use the trusted original wallet backup/recovery procedure; match product, platform, exact version and concrete mode. Never type a full phrase into Tessaveil or a website.

<a id="wallet-mymonero-generated"></a>

### MyMonero — generated backup — mymonero-generated

- Source record: [mymonero-generated](../catalog/wallets/mymonero-generated.json)
- Status: documented
- Reason: Evidence is insufficient for selectable support.
- Guidance: Not selectable; use the wallet's own backup procedure.
- Version interval (min / max): 1.3.2-source-5c7455d30e4e20150962f5f74efd83477962a05e / 1.3.2-source-5c7455d30e4e20150962f5f74efd83477962a05e
- Verified on: 2026-09-29
- Historical: false
- Evidence: [monero-my-core](../catalog/evidence/monero-my-core.json), [monero-mymonero-generated-wallet](../catalog/evidence/monero-mymonero-generated-wallet.json)
- Evidence claim: new\_wallet creates 32-byte/25-word backups; decoded\_seed handles 13 and 25 and hashes 16-byte seeds. Core/app binding remains unproven. Reviewed 2026-09-29; response byte SHA-256 ea6d34729151cffd2b7cdd1a16c31507ff3122242540646ac9797cc0797bb7b4. See docs/research/batches/monero-polyseed.md.
- Evidence claim: App shows backup mnemonic. Reviewed core new\_wallet generates 32-byte/25-word format, but dependency artifact binding to this app revision remains unproven. No new 13-word creation claim. Reviewed 2026-09-29; response byte SHA-256 1772443b59b4c4286aa30054f41d7f6110c35e2d471344b00346ca7774c9c674. See docs/research/batches/monero-polyseed.md.
- Aliases: —
- Scheme: —
- Generates mnemonic / import only: true / false
- Limitations: App shows backup mnemonic. Reviewed core new\_wallet generates 32-byte/25-word format, but dependency artifact binding to this app revision remains unproven. No new 13-word creation claim.; Documented, not selectable\: no exact released artifact and independent wallet-level recovery vector verified. Import, generation and export claims must be assessed separately.
- Profile guidance: Use the trusted original wallet backup/recovery procedure; match product, platform, exact version and concrete mode. Never type a full phrase into Tessaveil or a website.

<a id="wallet-mytonwallet"></a>

### My Wallet / MyTonWallet — mytonwallet

- Source record: [mytonwallet](../catalog/wallets/mytonwallet.json)
- Status: documented
- Reason: Evidence is insufficient for selectable support.
- Guidance: Not selectable; use the wallet's own backup procedure.
- Version interval (min / max): 26.9.8-source-f042bcc06b84f0cec928a29795f1cb8bf60a3e9c / 26.9.8-source-f042bcc06b84f0cec928a29795f1cb8bf60a3e9c
- Verified on: 2026-09-29
- Historical: false
- Evidence: [ton-my-auth](../catalog/evidence/ton-my-auth.json), [ton-my-backup](../catalog/evidence/ton-my-backup.json), [ton-my-common](../catalog/evidence/ton-my-common.json), [ton-my-create](../catalog/evidence/ton-my-create.json), [ton-my-derive](../catalog/evidence/ton-my-derive.json), [ton-my-path](../catalog/evidence/ton-my-path.json), [ton-my-version](../catalog/evidence/ton-my-version.json), [ton-tep3](../catalog/evidence/ton-tep3.json)
- Evidence claim: generateMnemonic\(isBip39\) selects BIP39 or native generation; not a product-name-wide assumption. Reviewed 2026-09-29; byte SHA-256 c6401d8455eb936f01cf951ba523eba8a19d69b386e3b116af256dc2a5b578a1. See docs/research/batches/bip39-ton.md.
- Evidence claim: BackupSecretWords retrieves fetchMnemonic and renders SecretWordsContent, proving the reviewed mnemonic modes expose manual backup in this web source. Reviewed 2026-09-29; byte SHA-256 724207d342eefabc654f030fc5df8720a96c8267c04ca5da822baa0fbd7325b1. See docs/research/batches/bip39-ton.md.
- Evidence claim: generateBip39Mnemonic uses bip39.generateMnemonic\(128\), hence 12 words; getMnemonic exports a stored secret. Import validation is a separate operation. Reviewed 2026-09-29; byte SHA-256 e435194f56181b0b9c1ac44934c1adf96b1518d53cbe76ac6a27ba455af432c6. See docs/research/batches/bip39-ton.md.
- Evidence claim: Creation passes \!forceAddingTonOnlyAccount to generateMnemonic, preserving distinct simultaneous modes. Reviewed 2026-09-29; byte SHA-256 3bc4849d9a8573e9e06182f4aefbc17e2aa358ff37e24c49d24cb5a24a210786. See docs/research/batches/bip39-ton.md.
- Evidence claim: TON auth.ts generates 24 native words, rerolling BIP39 ambiguity; explicit bip39 accounts use BIP39 seed and Ed25519 path derivation. Stored native words use TON default seed without implicit normalization. Reviewed 2026-09-29; byte SHA-256 35286bbfb6c1d6022569738a054dd32d060b1fc48c6a1143dab1df705a218211. See docs/research/batches/bip39-ton.md.
- Evidence claim: TON\_BIP39\_PATH is hardened path components 44, 607, account index; slot zero is the TEP-3 main-account path. Reviewed 2026-09-29; byte SHA-256 5d799c9d1ec5fc23bf85245a477772a744cbf19a0ef7bef0aa8ecf9c1bd1c670. See docs/research/batches/bip39-ton.md.
- Evidence claim: package.json names mytonwallet version 26.9.8. Catalogue claims only this full source commit, not an entire release interval. Reviewed 2026-09-29; byte SHA-256 93b9311800850e215a424d9eefdb512958e33cbe0ad3e7fe17d0bbf771698e32. See docs/research/batches/bip39-ton.md.
- Evidence claim: TEP-3 sections 2-4 and 8-12 distinguish native 24-word TON and multichain BIP39 12/24-word modes sharing the English vocabulary, with TON path hardened path components 44, 607, 0 for the latter. It recommends new 12-word multichain or native 24-word generation, not new 24-word multichain. Import may encounter both. TEP is guidance, not proof of any product release transition; Pro MAM is a separate derivation. Reviewed 2026-09-29; byte SHA-256 4049020b927f72f7187b04f3e61e27f478caf1669fd528f21b815417b428be4b. See docs/research/batches/bip39-ton.md.
- Aliases: My Wallet, MyTonWallet
- Scheme: [ton-multichain-bip39](#scheme-ton-multichain-bip39)
- Generates mnemonic / import only: true / false
- Limitations: Exact source snapshot supports default 128-bit BIP39 generation \(12 words\), native-mode override and backup display. Import of 24-word BIP39 does not imply new 24-word generation.; Full TON-path public known answer not reproduced; no blanket mapping to installed web/mobile releases or historical version intervals.
- Profile guidance: Use the original trusted wallet's backup and recovery procedure. Match exact product, platform, source version and mode. Never enter a complete recovery phrase into Tessaveil or a website.

<a id="wallet-mytonwallet-native"></a>

### My Wallet / MyTonWallet — TON only — mytonwallet-native

- Source record: [mytonwallet-native](../catalog/wallets/mytonwallet-native.json)
- Status: verified
- Reason: Verified research record; not a release or security guarantee.
- Version interval (min / max): 26.9.8-source-f042bcc06b84f0cec928a29795f1cb8bf60a3e9c / 26.9.8-source-f042bcc06b84f0cec928a29795f1cb8bf60a3e9c
- Verified on: 2026-09-29
- Historical: false
- Evidence: [ton-my-auth](../catalog/evidence/ton-my-auth.json), [ton-my-backup](../catalog/evidence/ton-my-backup.json), [ton-my-create](../catalog/evidence/ton-my-create.json), [ton-my-derive](../catalog/evidence/ton-my-derive.json), [ton-my-version](../catalog/evidence/ton-my-version.json), [ton-native-source](../catalog/evidence/ton-native-source.json), [ton-tep3](../catalog/evidence/ton-tep3.json)
- Evidence claim: generateMnemonic\(isBip39\) selects BIP39 or native generation; not a product-name-wide assumption. Reviewed 2026-09-29; byte SHA-256 c6401d8455eb936f01cf951ba523eba8a19d69b386e3b116af256dc2a5b578a1. See docs/research/batches/bip39-ton.md.
- Evidence claim: BackupSecretWords retrieves fetchMnemonic and renders SecretWordsContent, proving the reviewed mnemonic modes expose manual backup in this web source. Reviewed 2026-09-29; byte SHA-256 724207d342eefabc654f030fc5df8720a96c8267c04ca5da822baa0fbd7325b1. See docs/research/batches/bip39-ton.md.
- Evidence claim: Creation passes \!forceAddingTonOnlyAccount to generateMnemonic, preserving distinct simultaneous modes. Reviewed 2026-09-29; byte SHA-256 3bc4849d9a8573e9e06182f4aefbc17e2aa358ff37e24c49d24cb5a24a210786. See docs/research/batches/bip39-ton.md.
- Evidence claim: TON auth.ts generates 24 native words, rerolling BIP39 ambiguity; explicit bip39 accounts use BIP39 seed and Ed25519 path derivation. Stored native words use TON default seed without implicit normalization. Reviewed 2026-09-29; byte SHA-256 35286bbfb6c1d6022569738a054dd32d060b1fc48c6a1143dab1df705a218211. See docs/research/batches/bip39-ton.md.
- Evidence claim: package.json names mytonwallet version 26.9.8. Catalogue claims only this full source commit, not an entire release interval. Reviewed 2026-09-29; byte SHA-256 93b9311800850e215a424d9eefdb512958e33cbe0ad3e7fe17d0bbf771698e32. See docs/research/batches/bip39-ton.md.
- Evidence claim: TON crypto mnemonic.ts\: mnemonicNew defaults to 24; entropy is HMAC-SHA512\(key=space-joined words, message=optional password\), then PBKDF2-HMAC-SHA512 with TON default seed salt and 100000 iterations; first 32 bytes seed Ed25519. Basic-seed check uses TON seed version and 390 iterations. Native lowercase/trim behavior is not a universal BIP39 NFKD rule. Reviewed 2026-09-29; byte SHA-256 79518c5f905daaa4e64f09454e8a82dbb1c8d1b310305ef84b25e85b2c77126a. See docs/research/batches/bip39-ton.md.
- Evidence claim: TEP-3 sections 2-4 and 8-12 distinguish native 24-word TON and multichain BIP39 12/24-word modes sharing the English vocabulary, with TON path hardened path components 44, 607, 0 for the latter. It recommends new 12-word multichain or native 24-word generation, not new 24-word multichain. Import may encounter both. TEP is guidance, not proof of any product release transition; Pro MAM is a separate derivation. Reviewed 2026-09-29; byte SHA-256 4049020b927f72f7187b04f3e61e27f478caf1669fd528f21b815417b428be4b. See docs/research/batches/bip39-ton.md.
- Aliases: MyTonWallet TON only
- Scheme: [ton-native](#scheme-ton-native)
- Generates mnemonic / import only: true / false
- Limitations: Exact source snapshot only. forceAddingTonOnlyAccount chooses native generation; native generator returns 24 words and rejects BIP39-ambiguous candidates. This mode coexists with BIP39 in the same source version.; No assertion that all builds or older/newer installed versions expose the same mode.
- Profile guidance: Use the original trusted wallet's backup and recovery procedure. Match exact product, platform, source version and mode. Never enter a complete recovery phrase into Tessaveil or a website.

<a id="wallet-nami"></a>

### Nami — extension24 creation — nami

- Source record: [nami](../catalog/wallets/nami.json)
- Status: documented
- Reason: Evidence is insufficient for selectable support.
- Guidance: Not selectable; use the wallet's own backup procedure.
- Version interval (min / max): 3.9.6-source-e52e0bdb02eb1ec224db26f48b0192685a30f99e / 3.9.6-source-e52e0bdb02eb1ec224db26f48b0192685a30f99e
- Verified on: 2026-09-29
- Historical: false
- Evidence: [cardano-nami-create](../catalog/evidence/cardano-nami-create.json), [cardano-nami-derive](../catalog/evidence/cardano-nami-derive.json), [cardano-nami-version](../catalog/evidence/cardano-nami-version.json)
- Evidence claim: Creation calls generateMnemonic\(256\), displays indexed words then verifies chosen positions before createWallet. Restore branch separate. Establishes24-word creation, not later re-export. See docs/research/batches/slip39-algorand-cardano.md. Retrieved byte SHA-256 d79776a12f8f7c4c6a4dc93e159c58110509494e169f84f2c556f139ccaf109c.
- Evidence claim: createWallet converts BIP39 mnemonic to entropy, then from\_bip39\_entropy\(entropy, empty bytes\). Local encryption password is separate; hardware helpers not same mode. See docs/research/batches/slip39-algorand-cardano.md. Retrieved byte SHA-256 8c50628956578649ab228d7cfb6a29dcf8ac104e53f2c0a4fa67731ac913ce57.
- Evidence claim: Source package3.9.6. Historical snapshot scope only; no claim of maintained/current released app or binary recovery. See docs/research/batches/slip39-algorand-cardano.md. Retrieved byte SHA-256 81438dedcb3b9b8223148da27f89c7e5e5cb215ff0cffb6ed01527c0231d6ef4.
- Aliases: —
- Scheme: [cardano-icarus-24](#scheme-cardano-icarus-24)
- Generates mnemonic / import only: true / false
- Limitations: Source-only Chrome extension; Icarus-like from\_bip39\_entropy with empty password. Library lock/artifact binding and wallet-level recovery not reproduced; no claim of current maintenance.; Non-selectable\: exact released-artifact binding and independent wallet recovery have not been verified. A dated unresolved-version marker is not a release interval; false generation means no generation claim for this specific record, not proof of absence.
- Profile guidance: Use the original trusted wallet backup/recovery procedure. Match product, platform, exact version and specific mode. Never enter a complete phrase/share or extra passphrase into Tessaveil.

<a id="wallet-openmask"></a>

### OpenMask — openmask

- Source record: [openmask](../catalog/wallets/openmask.json)
- Status: documented
- Reason: Evidence is insufficient for selectable support.
- Guidance: Not selectable; use the wallet's own backup procedure.
- Version interval (min / max): 0.22.0-source-9150d57d530296f8b27ae59e4dfce865be81550e / 0.22.0-source-9150d57d530296f8b27ae59e4dfce865be81550e
- Verified on: 2026-09-29
- Historical: false
- Evidence: [ton-openmask-create](../catalog/evidence/ton-openmask-create.json), [ton-openmask-identity](../catalog/evidence/ton-openmask-identity.json), [ton-openmask-version](../catalog/evidence/ton-openmask-version.json), [ton-tep3](../catalog/evidence/ton-tep3.json), [ton-tonweb-generate](../catalog/evidence/ton-tonweb-generate.json), [ton-tonweb-seed](../catalog/evidence/ton-tonweb-seed.json), [ton-tonweb-version](../catalog/evidence/ton-tonweb-version.json)
- Evidence claim: CreateWallet.tsx calls tonweb-mnemonic.generateMnemonic, displays recovery words, and checks selected words before wallet creation. Reviewed 2026-09-29; byte SHA-256 12d7e29578a4c58d76665375cc4ab498e010b5871baa290e0aaba24819a11362. See docs/research/batches/bip39-ton.md.
- Evidence claim: OpenProduct repository README identifies OpenMask Chrome/Chromium extension and its official openmask.app website. Reviewed 2026-09-29; byte SHA-256 007ec00e241abeb6d6aa354fe8251a3d6e5cc340af53847a140a885ac6e82249. See docs/research/batches/bip39-ton.md.
- Evidence claim: package.json identifies @openmask/extension version 0.22.0 and tonweb-mnemonic ^1.0.1; a range does not pin the installed dependency. Reviewed 2026-09-29; byte SHA-256 5c4d9320793ae712801603af2bccd294dbd1beaf5bae2739de280dd3fca2fa6a. See docs/research/batches/bip39-ton.md.
- Evidence claim: TEP-3 sections 2-4 and 8-12 distinguish native 24-word TON and multichain BIP39 12/24-word modes sharing the English vocabulary, with TON path hardened path components 44, 607, 0 for the latter. It recommends new 12-word multichain or native 24-word generation, not new 24-word multichain. Import may encounter both. TEP is guidance, not proof of any product release transition; Pro MAM is a separate derivation. Reviewed 2026-09-29; byte SHA-256 4049020b927f72f7187b04f3e61e27f478caf1669fd528f21b815417b428be4b. See docs/research/batches/bip39-ton.md.
- Evidence claim: Reviewed tonweb-mnemonic generator defaults to 24 words from its English list and TON basic-seed predicate. This does not bind every OpenMask installation to this source. Reviewed 2026-09-29; byte SHA-256 f0f05bd83dd03b22463be3deb85787ba3c69e094c88ad889ceed17073dea7249. See docs/research/batches/bip39-ton.md.
- Evidence claim: tonweb-mnemonic uses TON entropy, PBKDF2 with TON default seed and returns the first 32 bytes, not BIP39 seed derivation. Reviewed 2026-09-29; byte SHA-256 c2e34f6888d3b8b3192567bbe6dbdb1fc1e4a1db51228089a62c4c2e8e8f70b7. See docs/research/batches/bip39-ton.md.
- Evidence claim: Reviewed tonweb-mnemonic package is version 1.0.1 at this exact commit. Reviewed 2026-09-29; byte SHA-256 3a5777133b2ccfa280a3ab0bcd030d63a93ec07f97370f589845e26a1b158574. See docs/research/batches/bip39-ton.md.
- Aliases: OpenMask Browser Extension
- Scheme: [ton-native](#scheme-ton-native)
- Generates mnemonic / import only: true / false
- Limitations: OpenProduct's Chrome extension source creates and displays a tonweb-mnemonic phrase. Package declares tonweb-mnemonic ^1.0.1; reviewed library 1.0.1 defaults to native 24.; Exact deployed extension/dependency artifact binding and a wallet-level reproducible recovery vector remain unproven; this source-backed mapping is documented, not selectable. Ledger and imported modes excluded.
- Profile guidance: Use the original trusted wallet's backup and recovery procedure. Match exact product, platform, source version and mode. Never enter a complete recovery phrase into Tessaveil or a website.

<a id="wallet-pera-wallet"></a>

### Pera Wallet — existing legacy25 backup export — pera-wallet

- Source record: [pera-wallet](../catalog/wallets/pera-wallet.json)
- Status: documented
- Reason: Evidence is insufficient for selectable support.
- Guidance: Not selectable; use the wallet's own backup procedure.
- Version interval (min / max): app-version-unresolved-doc-2026-08-31 / app-version-unresolved-doc-2026-08-31
- Verified on: 2026-09-29
- Historical: false
- Evidence: [algorand-pera-backup](../catalog/evidence/algorand-pera-backup.json), [algorand-pera-migration](../catalog/evidence/algorand-pera-migration.json)
- Evidence claim: Updated 2026-08-31\: mobile backup at creation and later view are described separately; article includes24 and 25 without exact app version. Scope iOS only in records; no equivalence between formats. See docs/research/batches/slip39-algorand-cardano.md. Retrieved byte SHA-256 4fad7c798ef8891ca31f4ee64051c570fd8d4952665f70738635c26eb425c9d6.
- Evidence claim: Updated 2026-05-28\: distinguishes24-word Universal and 25-word Legacy Algo 25 recovery. Restoration does not prove new legacy generation. See docs/research/batches/slip39-algorand-cardano.md. Retrieved byte SHA-256 30fa382990ea359398ccde9c9a4ccdd2e031b6b83721f9aede4cb46cb57c506b.
- Aliases: —
- Scheme: [algorand-25](#scheme-algorand-25)
- Generates mnemonic / import only: false / false
- Limitations: 25-word legacy recovery is documented; backup page permits later viewing. Record is export of an existing key; new25-word creation at current versions is unproven. Universal 24 is a separate mode. No web/Android/rekeyed/Ledger/Quantum generalization.; Non-selectable\: exact released-artifact binding and independent wallet recovery have not been verified. A dated unresolved-version marker is not a release interval; false generation means no generation claim for this specific record, not proof of absence.
- Profile guidance: Use the original trusted wallet backup/recovery procedure. Match product, platform, exact version and specific mode. Never enter a complete phrase/share or extra passphrase into Tessaveil.

<a id="wallet-pera-wallet-universal"></a>

### Pera Wallet — Universal 24 creation — pera-wallet-universal

- Source record: [pera-wallet-universal](../catalog/wallets/pera-wallet-universal.json)
- Status: documented
- Reason: Evidence is insufficient for selectable support.
- Guidance: Not selectable; use the wallet's own backup procedure.
- Version interval (min / max): app-version-unresolved-doc-2025-06-04 / app-version-unresolved-doc-2025-06-04
- Verified on: 2026-09-29
- Historical: false
- Evidence: [algorand-pera-backup](../catalog/evidence/algorand-pera-backup.json), [algorand-pera-universal](../catalog/evidence/algorand-pera-universal.json)
- Evidence claim: Updated 2026-08-31\: mobile backup at creation and later view are described separately; article includes24 and 25 without exact app version. Scope iOS only in records; no equivalence between formats. See docs/research/batches/slip39-algorand-cardano.md. Retrieved byte SHA-256 4fad7c798ef8891ca31f4ee64051c570fd8d4952665f70738635c26eb425c9d6.
- Evidence claim: Updated 2025-06-04\: iOS onboarding generates24-word BIP39 HD Universal wallets; Android described as forthcoming there. Dated source not generalized to current Android. Exact derivation/dependency binding not established. See docs/research/batches/slip39-algorand-cardano.md. Retrieved byte SHA-256 d54c39508a76f426bd3958cfbae5600d8f737aa05d4356540be617986a4c0b81.
- Aliases: —
- Scheme: —
- Generates mnemonic / import only: true / false
- Limitations: Official FAQ is dated 2025-06-04;24-word HD phrase is not Algorand25. Full Algorand HD derivation research and exact app version absent; leave scheme unmapped.; Non-selectable\: exact released-artifact binding and independent wallet recovery have not been verified. A dated unresolved-version marker is not a release interval; false generation means no generation claim for this specific record, not proof of absence.
- Profile guidance: Use the original trusted wallet backup/recovery procedure. Match product, platform, exact version and specific mode. Never enter a complete phrase/share or extra passphrase into Tessaveil.

<a id="wallet-polkadot-js"></a>

### Polkadot.js — extension sr25519 creation — polkadot-js

- Source record: [polkadot-js](../catalog/wallets/polkadot-js.json)
- Status: documented
- Reason: Evidence is insufficient for selectable support.
- Guidance: Not selectable; use the wallet's own backup procedure.
- Version interval (min / max): source-54f44022004f4cefb4a2b929f3a397715a134d6f / source-54f44022004f4cefb4a2b929f3a397715a134d6f
- Verified on: 2026-09-29
- Historical: false
- Evidence: [substrate-polkadot-create](../catalog/evidence/substrate-polkadot-create.json), [substrate-polkadot-type](../catalog/evidence/substrate-polkadot-type.json), [substrate-polkadot-ui](../catalog/evidence/substrate-polkadot-ui.json)
- Evidence claim: Extension handler seedCreate calls mnemonicGenerate with default12; accepts12/15/18/21/24 on validation, which is not proof UI creates all. createFromUri receives explicit type; Ethereum branch distinct.
- Evidence claim: DEFAULT\_TYPE is sr25519. Dependency implementation/released extension recovery not pinned end-to-end here; mapped primitive stays documented.
- Evidence claim: CreateAccount generates fresh seed, displays it and creates selected network account; this profile is browser extension default sr25519 for Polkadot/Kusama, excluding Ethereum.
- Aliases: —
- Scheme: [substrate-bip39](#scheme-substrate-bip39)
- Generates mnemonic / import only: true / false
- Limitations: Default UI12 only; scheme lists primitive input lengths, not UI generation choices. Dependency/backend and released extension binding unverified; exclude Ethereum/JSON/hardware.; Non-selectable\: exact released artifact and independent wallet recovery not verified. A source commit is a singleton evidence boundary, not an all-version support promise.
- Profile guidance: Use the original wallet backup procedure and match exact product, platform, version and mode. Never enter a complete phrase or external recovery secret into Tessaveil.

<a id="wallet-sia-ui"></a>

### Sia-UI v1.3.3 — legacy import — sia-ui

- Source record: [sia-ui](../catalog/wallets/sia-ui.json)
- Status: documented
- Reason: Evidence is insufficient for selectable support.
- Guidance: Not selectable; use the wallet's own backup procedure.
- Version interval (min / max): cd7e221b98fc7a395de25bd8dfaa4f4de2a6e3d2 / cd7e221b98fc7a395de25bd8dfaa4f4de2a6e3d2
- Verified on: 2026-09-29
- Historical: true
- Evidence: [sia-siad-seed](../catalog/evidence/sia-siad-seed.json), [sia-ui-history](../catalog/evidence/sia-ui-history.json)
- Evidence claim: SeedToString appends first6 bytes of crypto.HashObject\(seed\) to32-byte seed then entropy-mnemonics conversion. StringToSeed requires28/29 English words, exact formatting/lowercase and38 decoded bytes before checksum. Both lengths are one variable-length codec, not two incompatible algorithms.
- Evidence claim: Sia-UI v1.3.3 source restores a supplied seed and trims seed/password separately. Custom password is local wallet encryption, not mnemonic derivation extension. Precise shipped siad binary and historical creation behavior unresolved.
- Aliases: —
- Scheme: [sia-legacy-28](#scheme-sia-legacy-28)
- Generates mnemonic / import only: false / true
- Limitations: Historical GUI accepts seed string; exact bundled siad version unverified. Paired29 profile preserves variable-length codec identity; no current network support promised.; Non-selectable\: exact shipped binary/dependency binding and independent restoration were not verified. Singleton source boundary is not an all-version compatibility claim.
- Profile guidance: Match original product, platform, version and mode; use its native backup procedure. Never enter a complete phrase, private key or external secret into Tessaveil.

<a id="wallet-sia-ui-29"></a>

### Sia-UI v1.3.3 — legacy29 import — sia-ui-29

- Source record: [sia-ui-29](../catalog/wallets/sia-ui-29.json)
- Status: documented
- Reason: Evidence is insufficient for selectable support.
- Guidance: Not selectable; use the wallet's own backup procedure.
- Version interval (min / max): cd7e221b98fc7a395de25bd8dfaa4f4de2a6e3d2 / cd7e221b98fc7a395de25bd8dfaa4f4de2a6e3d2
- Verified on: 2026-09-29
- Historical: true
- Evidence: [sia-siad-seed](../catalog/evidence/sia-siad-seed.json), [sia-ui-history](../catalog/evidence/sia-ui-history.json)
- Evidence claim: SeedToString appends first6 bytes of crypto.HashObject\(seed\) to32-byte seed then entropy-mnemonics conversion. StringToSeed requires28/29 English words, exact formatting/lowercase and38 decoded bytes before checksum. Both lengths are one variable-length codec, not two incompatible algorithms.
- Evidence claim: Sia-UI v1.3.3 source restores a supplied seed and trims seed/password separately. Custom password is local wallet encryption, not mnemonic derivation extension. Precise shipped siad binary and historical creation behavior unresolved.
- Aliases: —
- Scheme: [sia-legacy-29](#scheme-sia-legacy-29)
- Generates mnemonic / import only: false / true
- Limitations: Historical GUI route only; exact bundled backend dependency unresolved.; Non-selectable\: exact shipped binary/dependency binding and independent restoration were not verified. Singleton source boundary is not an all-version compatibility claim.
- Profile guidance: Match original product, platform, version and mode; use its native backup procedure. Never enter a complete phrase, private key or external secret into Tessaveil.

<a id="wallet-sia-walletd"></a>

### Sia walletd UI0.36.2 — seed mode — sia-walletd

- Source record: [sia-walletd](../catalog/wallets/sia-walletd.json)
- Status: documented
- Reason: Evidence is insufficient for selectable support.
- Guidance: Not selectable; use the wallet's own backup procedure.
- Version interval (min / max): f4e3ff774c4f6a5b9830abf1767485215a26a349 / f4e3ff774c4f6a5b9830abf1767485215a26a349
- Verified on: 2026-09-29
- Historical: false
- Evidence: [sia-current-codec](../catalog/evidence/sia-current-codec.json), [sia-server-boundary](../catalog/evidence/sia-server-boundary.json), [sia-web-create](../catalog/evidence/sia-web-create.json), [sia-web-sdk](../catalog/evidence/sia-web-sdk.json)
- Evidence claim: coreutils v0.24.1 supports only12 words, English BIP39 entropy/checksum encoding; ordered list equals existing BIP39-English. SeedFromPhrase hashes16-byte entropy with BLAKE2b-256, not BIP39 PBKDF2. No extra passphrase; case-sensitive lookup and strings.Fields whitespace.
- Evidence claim: walletd server README explicitly permits externally derived keys from12-word, legacy28-word, Ledger or other methods. This does not imply its embedded UI accepts legacy phrases; retain both scopes and older hardfork documentation warning.
- Evidence claim: walletd UI0.36.2 source generates via SDK.generateSeedPhrase and validates12-word seed. This UI seed mode excludes legacy28/29; release binary binding not tested.
- Evidence claim: UI SDK routes phrase generation and seed parsing to coreutils/wallet; sdk/go.mod pins v0.24.1. This is the12-word UI route; generic walletd server can track externally derived legacy addresses.
- Aliases: —
- Scheme: [sia-bip39](#scheme-sia-bip39)
- Generates mnemonic / import only: true / false
- Limitations: This UI seed mode accepts12 only; legacy28/29 cannot be entered here. Generic walletd server remains seed-agnostic and may track/sign externally prepared legacy transactions.; Non-selectable\: exact shipped binary/dependency binding and independent restoration were not verified. Singleton source boundary is not an all-version compatibility claim.
- Profile guidance: Match original product, platform, version and mode; use its native backup procedure. Never enter a complete phrase, private key or external secret into Tessaveil.

<a id="wallet-siad"></a>

### siad — legacy28 seed export — siad

- Source record: [siad](../catalog/wallets/siad.json)
- Status: documented
- Reason: Evidence is insufficient for selectable support.
- Guidance: Not selectable; use the wallet's own backup procedure.
- Version interval (min / max): 66e7fc630585887c30033379d2a0a8bf5c618177 / 66e7fc630585887c30033379d2a0a8bf5c618177
- Verified on: 2026-09-29
- Historical: true
- Evidence: [sia-siad-dependency](../catalog/evidence/sia-siad-dependency.json), [sia-siad-seed](../catalog/evidence/sia-siad-seed.json)
- Evidence claim: siad pins gitlab.com/NebulousLabs/entropy-mnemonics pseudo-version7532f67e3500, resolved through official GitLab to7532f67e35008b0f36bbebb20d5a6ee8f14a22f5.
- Evidence claim: SeedToString appends first6 bytes of crypto.HashObject\(seed\) to32-byte seed then entropy-mnemonics conversion. StringToSeed requires28/29 English words, exact formatting/lowercase and38 decoded bytes before checksum. Both lengths are one variable-length codec, not two incompatible algorithms.
- Aliases: —
- Scheme: [sia-legacy-28](#scheme-sia-legacy-28)
- Generates mnemonic / import only: true / false
- Limitations: Legacy codec can produce28 or29 depending on input; separate profile29 covers other length. Historical software, not a current network-support promise.; Non-selectable\: exact shipped binary/dependency binding and independent restoration were not verified. Singleton source boundary is not an all-version compatibility claim.
- Profile guidance: Match original product, platform, version and mode; use its native backup procedure. Never enter a complete phrase, private key or external secret into Tessaveil.

<a id="wallet-siad-29"></a>

### siad — legacy29 seed export — siad-29

- Source record: [siad-29](../catalog/wallets/siad-29.json)
- Status: documented
- Reason: Evidence is insufficient for selectable support.
- Guidance: Not selectable; use the wallet's own backup procedure.
- Version interval (min / max): 66e7fc630585887c30033379d2a0a8bf5c618177 / 66e7fc630585887c30033379d2a0a8bf5c618177
- Verified on: 2026-09-29
- Historical: true
- Evidence: [sia-siad-dependency](../catalog/evidence/sia-siad-dependency.json), [sia-siad-seed](../catalog/evidence/sia-siad-seed.json)
- Evidence claim: siad pins gitlab.com/NebulousLabs/entropy-mnemonics pseudo-version7532f67e3500, resolved through official GitLab to7532f67e35008b0f36bbebb20d5a6ee8f14a22f5.
- Evidence claim: SeedToString appends first6 bytes of crypto.HashObject\(seed\) to32-byte seed then entropy-mnemonics conversion. StringToSeed requires28/29 English words, exact formatting/lowercase and38 decoded bytes before checksum. Both lengths are one variable-length codec, not two incompatible algorithms.
- Aliases: —
- Scheme: [sia-legacy-29](#scheme-sia-legacy-29)
- Generates mnemonic / import only: true / false
- Limitations: Same32-byte seed\+6-byte checksum codec as28; do not interpret length as release version.; Non-selectable\: exact shipped binary/dependency binding and independent restoration were not verified. Singleton source boundary is not an all-version compatibility claim.
- Profile guidance: Match original product, platform, version and mode; use its native backup procedure. Never enter a complete phrase, private key or external secret into Tessaveil.

<a id="wallet-subwallet"></a>

### SubWallet — extension general sr25519 creation — subwallet

- Source record: [subwallet](../catalog/wallets/subwallet.json)
- Status: documented
- Reason: Evidence is insufficient for selectable support.
- Guidance: Not selectable; use the wallet's own backup procedure.
- Version interval (min / max): source-1f9b2a4cb6fea68193e5e012dcca7284a1dd0d80 / source-1f9b2a4cb6fea68193e5e012dcca7284a1dd0d80
- Verified on: 2026-09-29
- Historical: false
- Evidence: [substrate-subwallet](../catalog/evidence/substrate-subwallet.json)
- Evidence claim: General mnemonic creation handler defaults12 and has12/15/18/21/24 validation lengths. It constructs sr25519 plus other coin types; this record is only general sr25519 Polkadot/Kusama. TON-native and Ethereum not equated. Dependency/UI/artifact binding unresolved.
- Aliases: —
- Scheme: [substrate-bip39](#scheme-substrate-bip39)
- Generates mnemonic / import only: true / false
- Limitations: Source handler defaults12; validation lengths do not prove every UI creation option. Forked keyring and frontend dependency binding unresolved; no TON-native/Ethereum/mobile mapping.; Non-selectable\: exact released artifact and independent wallet recovery not verified. A source commit is a singleton evidence boundary, not an all-version support promise.
- Profile guidance: Use the original wallet backup procedure and match exact product, platform, version and mode. Never enter a complete phrase or external recovery secret into Tessaveil.

<a id="wallet-talisman"></a>

### Talisman — extension Substrate mnemonic creation — talisman

- Source record: [talisman](../catalog/wallets/talisman.json)
- Status: documented
- Reason: Evidence is insufficient for selectable support.
- Guidance: Not selectable; use the wallet's own backup procedure.
- Version interval (min / max): 3.10.0-source-2cee3ef46633cdc3e90bb0fed6855fa25fc87692 / 3.10.0-source-2cee3ef46633cdc3e90bb0fed6855fa25fc87692
- Verified on: 2026-09-29
- Historical: false
- Evidence: [substrate-talisman](../catalog/evidence/substrate-talisman.json), [substrate-talisman-ui](../catalog/evidence/substrate-talisman-ui.json)
- Evidence claim: Talisman uses scure BIP39 English generation12/24; sr25519/ed25519/ecdsa use entropy-based32-byte PBKDF2 result, Ethereum/Solana sentence-based64-byte classic result. Its NFKD password normalization is a consumer behavior, absent from raw substrate-bip39 function.
- Evidence claim: Mnemonic creation UI explicitly generates12 and24 independently, default12. Source version3.10.0; no binary recovery asserted.
- Aliases: —
- Scheme: [substrate-bip39](#scheme-substrate-bip39)
- Generates mnemonic / import only: true / false
- Limitations: UI generates12/24; NFKD password normalization in this consumer differs from raw primitive behavior. Hardware, Ethereum, Solana and derived paths not equated.; Non-selectable\: exact released artifact and independent wallet recovery not verified. A source commit is a singleton evidence boundary, not an all-version support promise.
- Profile guidance: Use the original wallet backup procedure and match exact product, platform, version and mode. Never enter a complete phrase or external recovery secret into Tessaveil.

<a id="wallet-ton-space"></a>

### TON Space / DeFi Account — ton-space

- Source record: [ton-space](../catalog/wallets/ton-space.json)
- Status: documented
- Reason: Evidence is insufficient for selectable support.
- Guidance: Not selectable; use the wallet's own backup procedure.
- Version interval (min / max): documentation-snapshot-2026-09-29-version-unresolved / documentation-snapshot-2026-09-29-version-unresolved
- Verified on: 2026-09-29
- Historical: false
- Evidence: [ton-space-doc](../catalog/evidence/ton-space-doc.json), [ton-space-security](../catalog/evidence/ton-space-security.json)
- Evidence claim: Current vendor DeFi Account page, reached from legacy TON Space URL, describes creation and separate manual/email backup; W5/v4R2 are contract versions and do not pin app mnemonic semantics. Reviewed 2026-09-29; byte SHA-256 506a3bc3c0a4861601fc606c90320acac8d4a2bd91a639b27190567530006d37. See docs/research/batches/bip39-ton.md.
- Evidence claim: Vendor Security headings What is a Secret Recovery Phrase and How can I find my seed phrase describe 24 words, viewing backup in settings, and use the term BIP-39 without publishing derivation/version details. This evidence gap prevents native/multichain mapping. Reviewed 2026-09-29; byte SHA-256 7f5a40f0e43d00d2a620972b9f2a1a5370ed4ad660f6d65d5ca25bc36f71b8dd. See docs/research/batches/bip39-ton.md.
- Aliases: DeFi Account, TON Space, TON Wallet
- Scheme: —
- Generates mnemonic / import only: true / false
- Limitations: Legacy TON Space help URL redirects to current DeFi Account documentation. Manual backup exposes 24 words; current official security page calls it BIP-39 but supplies no derivation path, source revision or product version transition.; Native TON versus multichain semantics cannot be resolved from that wording. No scheme is selected; do not substitute historical TON-native assumptions.; Email backup and custodial Crypto Wallet are separate modes and cannot be represented by this manual-mnemonic profile. Contract W5/v4R2 is not an app version or mnemonic scheme boundary.
- Profile guidance: Use the original trusted wallet's backup and recovery procedure. Match exact product, platform, source version and mode. Never enter a complete recovery phrase into Tessaveil or a website.

<a id="wallet-tonhub"></a>

### Tonhub — tonhub

- Source record: [tonhub](../catalog/wallets/tonhub.json)
- Status: verified
- Reason: Verified research record; not a release or security guarantee.
- Version interval (min / max): 2.5.45-source-a2503f79d14868d65349ad7035d18389c6e2f996 / 2.5.45-source-a2503f79d14868d65349ad7035d18389c6e2f996
- Verified on: 2026-09-29
- Historical: false
- Evidence: [ton-native-source](../catalog/evidence/ton-native-source.json), [ton-tep3](../catalog/evidence/ton-tep3.json), [tonhub-create](../catalog/evidence/tonhub-create.json), [tonhub-derive](../catalog/evidence/tonhub-derive.json), [tonhub-identity](../catalog/evidence/tonhub-identity.json), [tonhub-version](../catalog/evidence/tonhub-version.json)
- Evidence claim: TON crypto mnemonic.ts\: mnemonicNew defaults to 24; entropy is HMAC-SHA512\(key=space-joined words, message=optional password\), then PBKDF2-HMAC-SHA512 with TON default seed salt and 100000 iterations; first 32 bytes seed Ed25519. Basic-seed check uses TON seed version and 390 iterations. Native lowercase/trim behavior is not a universal BIP39 NFKD rule. Reviewed 2026-09-29; byte SHA-256 79518c5f905daaa4e64f09454e8a82dbb1c8d1b310305ef84b25e85b2c77126a. See docs/research/batches/bip39-ton.md.
- Evidence claim: TEP-3 sections 2-4 and 8-12 distinguish native 24-word TON and multichain BIP39 12/24-word modes sharing the English vocabulary, with TON path hardened path components 44, 607, 0 for the latter. It recommends new 12-word multichain or native 24-word generation, not new 24-word multichain. Import may encounter both. TEP is guidance, not proof of any product release transition; Pro MAM is a separate derivation. Reviewed 2026-09-29; byte SHA-256 4049020b927f72f7187b04f3e61e27f478caf1669fd528f21b815417b428be4b. See docs/research/batches/bip39-ton.md.
- Evidence claim: WalletCreateFragment invokes @ton/crypto mnemonicNew and displays the result in MnemonicsView before backup confirmation; native default is 24 words. Reviewed 2026-09-29; byte SHA-256 dafdd9c99b91982918502e45f077b9d5af518e6c531aa878fb666bc2ad9a1329. See docs/research/batches/bip39-ton.md.
- Evidence claim: createWalletFromMnemonics calls @ton/crypto mnemonicToWalletKey; this is TON-native, not ordinary BIP39 derivation. Reviewed 2026-09-29; byte SHA-256 b8341c61165ac9778a00e7eb7546b29a43ed0cc09ad520fdd3ce63011f8a5795. See docs/research/batches/bip39-ton.md.
- Evidence claim: Upstream README identifies this repository as Tonhub Wallet. Its GPL/distribution text is not permission to bundle wallet code; no wallet code is included. Reviewed 2026-09-29; byte SHA-256 59da82be7e3db101c4a8f72ee2b4e618ba6db87f9edaa5b9f939dd87f0a4c74b. See docs/research/batches/bip39-ton.md.
- Evidence claim: package.json is version 2.5.45 at the exact source commit. No binary or other-version identity is asserted. Reviewed 2026-09-29; byte SHA-256 ef41072e6abb6d6f983d669e0f8e9a8f182fd73a98406b251ad68f31379c6386. See docs/research/batches/bip39-ton.md.
- Aliases: Tonhub Wallet
- Scheme: [ton-native](#scheme-ton-native)
- Generates mnemonic / import only: true / false
- Limitations: Exact React Native Android source snapshot only; creation invokes native mnemonicNew and displays its 24-word result before backup confirmation. Derivation uses mnemonicToWalletKey.; Hardware/Ledger, imported accounts, iOS binaries and other app versions are not covered by this profile. Wallet contract version changes do not establish mnemonic changes.
- Profile guidance: Use the original trusted wallet's backup and recovery procedure. Match exact product, platform, source version and mode. Never enter a complete recovery phrase into Tessaveil or a website.

<a id="wallet-tonkeeper-classic"></a>

### Tonkeeper Classic — tonkeeper-classic

- Source record: [tonkeeper-classic](../catalog/wallets/tonkeeper-classic.json)
- Status: verified
- Reason: Verified research record; not a release or security guarantee.
- Version interval (min / max): source-4942adcdcddf55d57e3d3fc3676f019caf87357e / source-4942adcdcddf55d57e3d3fc3676f019caf87357e
- Verified on: 2026-09-29
- Historical: false
- Evidence: [ton-native-source](../catalog/evidence/ton-native-source.json), [ton-tep3](../catalog/evidence/ton-tep3.json), [tonkeeper-create](../catalog/evidence/tonkeeper-create.json), [tonkeeper-derive](../catalog/evidence/tonkeeper-derive.json), [tonkeeper-version](../catalog/evidence/tonkeeper-version.json)
- Evidence claim: TON crypto mnemonic.ts\: mnemonicNew defaults to 24; entropy is HMAC-SHA512\(key=space-joined words, message=optional password\), then PBKDF2-HMAC-SHA512 with TON default seed salt and 100000 iterations; first 32 bytes seed Ed25519. Basic-seed check uses TON seed version and 390 iterations. Native lowercase/trim behavior is not a universal BIP39 NFKD rule. Reviewed 2026-09-29; byte SHA-256 79518c5f905daaa4e64f09454e8a82dbb1c8d1b310305ef84b25e85b2c77126a. See docs/research/batches/bip39-ton.md.
- Evidence claim: TEP-3 sections 2-4 and 8-12 distinguish native 24-word TON and multichain BIP39 12/24-word modes sharing the English vocabulary, with TON path hardened path components 44, 607, 0 for the latter. It recommends new 12-word multichain or native 24-word generation, not new 24-word multichain. Import may encounter both. TEP is guidance, not proof of any product release transition; Pro MAM is a separate derivation. Reviewed 2026-09-29; byte SHA-256 4049020b927f72f7187b04f3e61e27f478caf1669fd528f21b815417b428be4b. See docs/research/batches/bip39-ton.md.
- Evidence claim: CreateStandardWallet invokes mnemonicNew\(24\), displays Words, checks backup and persists mnemonicType=ton. Reviewed 2026-09-29; byte SHA-256 a60930c7ec15e52b5cd5735738199b2cce50c3da510a424fe29b4eb7e642e74e. See docs/research/batches/bip39-ton.md.
- Evidence claim: mnemonicService distinguishes explicit ton from bip39; BIP39 follows hardened path components 44, 607, 0. This proves handling/derivation, not multichain generation by all products. Reviewed 2026-09-29; byte SHA-256 9852941011f82ec14e865c0cf33d78fa3944eeed5c61deeade94b65412d87643. See docs/research/batches/bip39-ton.md.
- Evidence claim: Extension manifest version is 3.0.0 at this exact source commit; web package 0.0.0 is not a deployed-version identifier. Reviewed 2026-09-29; byte SHA-256 7d8f4c2373bd7dcf5a3d5cd3e11407848baa178efef1ddda12b60b9c2c82b600. See docs/research/batches/bip39-ton.md.
- Aliases: Tonkeeper
- Scheme: [ton-native](#scheme-ton-native)
- Generates mnemonic / import only: true / false
- Limitations: Source snapshot only\: extension manifest 3.0.0; web package is 0.0.0 and supplies no deployed release boundary. No claim for every installed Tonkeeper or Keeper version.; CreateStandardWallet creates and displays native 24 words; TRON integration does not turn that phrase into a BIP39 root. Pro multi-account MAM is excluded.
- Profile guidance: Use the original trusted wallet's backup and recovery procedure. Match exact product, platform, source version and mode. Never enter a complete recovery phrase into Tessaveil or a website.

<a id="wallet-tonkeeper-multichain"></a>

### Keeper / Tonkeeper Multichain — tonkeeper-multichain

- Source record: [tonkeeper-multichain](../catalog/wallets/tonkeeper-multichain.json)
- Status: documented
- Reason: Evidence is insufficient for selectable support.
- Guidance: Not selectable; use the wallet's own backup procedure.
- Version interval (min / max): documentation-snapshot-2026-09-29-version-unresolved / documentation-snapshot-2026-09-29-version-unresolved
- Verified on: 2026-09-29
- Historical: false
- Evidence: [ton-keeper-doc](../catalog/evidence/ton-keeper-doc.json), [ton-tep3](../catalog/evidence/ton-tep3.json), [tonkeeper-derive](../catalog/evidence/tonkeeper-derive.json)
- Evidence claim: Keeper vendor explains Tonkeeper rebranding, new multichain-wallet creation and inability to directly convert existing native 24-word accounts. Documentation omits generation count, platform and exact app release boundary. Reviewed 2026-09-29; byte SHA-256 d7091696af9e14b254c181906e1a8e8b48a339835ae65ac753593cabcbcb768a. See docs/research/batches/bip39-ton.md.
- Evidence claim: TEP-3 sections 2-4 and 8-12 distinguish native 24-word TON and multichain BIP39 12/24-word modes sharing the English vocabulary, with TON path hardened path components 44, 607, 0 for the latter. It recommends new 12-word multichain or native 24-word generation, not new 24-word multichain. Import may encounter both. TEP is guidance, not proof of any product release transition; Pro MAM is a separate derivation. Reviewed 2026-09-29; byte SHA-256 4049020b927f72f7187b04f3e61e27f478caf1669fd528f21b815417b428be4b. See docs/research/batches/bip39-ton.md.
- Evidence claim: mnemonicService distinguishes explicit ton from bip39; BIP39 follows hardened path components 44, 607, 0. This proves handling/derivation, not multichain generation by all products. Reviewed 2026-09-29; byte SHA-256 9852941011f82ec14e865c0cf33d78fa3944eeed5c61deeade94b65412d87643. See docs/research/batches/bip39-ton.md.
- Aliases: Keeper, Tonkeeper multichain
- Scheme: [ton-multichain-bip39](#scheme-ton-multichain-bip39)
- Generates mnemonic / import only: true / false
- Limitations: Official rebranding documentation confirms a separate new multichain wallet and says old native 24 words cannot be converted. It does not pin app platform/version or generation word count.; Pinned web source proves BIP39 import derivation, not that its new-wallet screen generates this mode. Exact first/last mobile versions and full-path known answer remain unproven; 12/24 are scheme lengths, not asserted generation lengths.; Keeper \(formerly Tonkeeper\) is not the unrelated Waves Keeper product; Pro MAM is excluded.
- Profile guidance: Use the original trusted wallet's backup and recovery procedure. Match exact product, platform, source version and mode. Never enter a complete recovery phrase into Tessaveil or a website.

<a id="wallet-trezor-model-t"></a>

### Trezor Model T — suite-single-share-20-created — trezor-model-t

- Source record: [trezor-model-t](../catalog/wallets/trezor-model-t.json)
- Status: documented
- Reason: Evidence is insufficient for selectable support.
- Guidance: Not selectable; use the wallet's own backup procedure.
- Version interval (min / max): suite-firmware-version-unresolved-doc-2026-09-29 / suite-firmware-version-unresolved-doc-2026-09-29
- Verified on: 2026-09-29
- Historical: false
- Evidence: [slip39-trezor-model-t](../catalog/evidence/slip39-trezor-model-t.json)
- Evidence claim: Trezor Model T\: device-specific table row confirms20-word SLIP39 single/multi backup options. 12-word BIP39 is default; SLIP39 is an explicit choice. Exact Suite/firmware versions unpublished in article; no33-word Suite creation or cross-model inference. See docs/research/batches/slip39-algorand-cardano.md. Read through web retrieval; direct response was HTTP 403. No raw-body hash or immutable capture asserted.
- Aliases: —
- Scheme: [slip39-share-20](#scheme-slip39-share-20)
- Generates mnemonic / import only: true / false
- Limitations: 12-word BIP39 is default; SLIP39 is an explicit choice. Hardware platform only; Suite host OS/version and firmware bounds unresolved. No promise for all firmware, Model One, 33-word Suite creation or CLI advanced groups. See exact device row.; Non-selectable\: exact released-artifact binding and independent wallet recovery have not been verified. A dated unresolved-version marker is not a release interval; false generation means no generation claim for this specific record, not proof of absence.
- Profile guidance: Use the original trusted wallet backup/recovery procedure. Match product, platform, exact version and specific mode. Never enter a complete phrase/share or extra passphrase into Tessaveil.

<a id="wallet-trezor-model-t-multi-share"></a>

### Trezor Model T — suite-multi-share-20-created — trezor-model-t-multi-share

- Source record: [trezor-model-t-multi-share](../catalog/wallets/trezor-model-t-multi-share.json)
- Status: documented
- Reason: Evidence is insufficient for selectable support.
- Guidance: Not selectable; use the wallet's own backup procedure.
- Version interval (min / max): suite-firmware-version-unresolved-doc-2026-09-29 / suite-firmware-version-unresolved-doc-2026-09-29
- Verified on: 2026-09-29
- Historical: false
- Evidence: [slip39-trezor-model-t](../catalog/evidence/slip39-trezor-model-t.json)
- Evidence claim: Trezor Model T\: device-specific table row confirms20-word SLIP39 single/multi backup options. 12-word BIP39 is default; SLIP39 is an explicit choice. Exact Suite/firmware versions unpublished in article; no33-word Suite creation or cross-model inference. See docs/research/batches/slip39-algorand-cardano.md. Read through web retrieval; direct response was HTTP 403. No raw-body hash or immutable capture asserted.
- Aliases: —
- Scheme: [slip39-share-20](#scheme-slip39-share-20)
- Generates mnemonic / import only: true / false
- Limitations: 12-word BIP39 is default; SLIP39 is an explicit choice. Hardware platform only; Suite host OS/version and firmware bounds unresolved. No promise for all firmware, Model One, 33-word Suite creation or CLI advanced groups. See exact device row.; Non-selectable\: exact released-artifact binding and independent wallet recovery have not been verified. A dated unresolved-version marker is not a release interval; false generation means no generation claim for this specific record, not proof of absence.
- Profile guidance: Use the original trusted wallet backup/recovery procedure. Match product, platform, exact version and specific mode. Never enter a complete phrase/share or extra passphrase into Tessaveil.

<a id="wallet-trezor-safe-3"></a>

### Trezor Safe 3 — suite-single-share-20-created — trezor-safe-3

- Source record: [trezor-safe-3](../catalog/wallets/trezor-safe-3.json)
- Status: documented
- Reason: Evidence is insufficient for selectable support.
- Guidance: Not selectable; use the wallet's own backup procedure.
- Version interval (min / max): suite-firmware-version-unresolved-doc-2026-09-29 / suite-firmware-version-unresolved-doc-2026-09-29
- Verified on: 2026-09-29
- Historical: false
- Evidence: [slip39-trezor-safe-3](../catalog/evidence/slip39-trezor-safe-3.json)
- Evidence claim: Trezor Safe 3\: device-specific table row confirms20-word SLIP39 single/multi backup options. before June2024 BIP39 default; from June2024 SLIP39 default; dates describe setup era, not a firmware number. Exact Suite/firmware versions unpublished in article; no33-word Suite creation or cross-model inference. See docs/research/batches/slip39-algorand-cardano.md. Read through web retrieval; direct response was HTTP 403. No raw-body hash or immutable capture asserted.
- Aliases: —
- Scheme: [slip39-share-20](#scheme-slip39-share-20)
- Generates mnemonic / import only: true / false
- Limitations: before June2024 BIP39 default; from June2024 SLIP39 default; dates describe setup era, not a firmware number. Hardware platform only; Suite host OS/version and firmware bounds unresolved. No promise for all firmware, Model One, 33-word Suite creation or CLI advanced groups. See exact device row.; Non-selectable\: exact released-artifact binding and independent wallet recovery have not been verified. A dated unresolved-version marker is not a release interval; false generation means no generation claim for this specific record, not proof of absence.
- Profile guidance: Use the original trusted wallet backup/recovery procedure. Match product, platform, exact version and specific mode. Never enter a complete phrase/share or extra passphrase into Tessaveil.

<a id="wallet-trezor-safe-3-multi-share"></a>

### Trezor Safe 3 — suite-multi-share-20-created — trezor-safe-3-multi-share

- Source record: [trezor-safe-3-multi-share](../catalog/wallets/trezor-safe-3-multi-share.json)
- Status: documented
- Reason: Evidence is insufficient for selectable support.
- Guidance: Not selectable; use the wallet's own backup procedure.
- Version interval (min / max): suite-firmware-version-unresolved-doc-2026-09-29 / suite-firmware-version-unresolved-doc-2026-09-29
- Verified on: 2026-09-29
- Historical: false
- Evidence: [slip39-trezor-safe-3](../catalog/evidence/slip39-trezor-safe-3.json)
- Evidence claim: Trezor Safe 3\: device-specific table row confirms20-word SLIP39 single/multi backup options. before June2024 BIP39 default; from June2024 SLIP39 default; dates describe setup era, not a firmware number. Exact Suite/firmware versions unpublished in article; no33-word Suite creation or cross-model inference. See docs/research/batches/slip39-algorand-cardano.md. Read through web retrieval; direct response was HTTP 403. No raw-body hash or immutable capture asserted.
- Aliases: —
- Scheme: [slip39-share-20](#scheme-slip39-share-20)
- Generates mnemonic / import only: true / false
- Limitations: before June2024 BIP39 default; from June2024 SLIP39 default; dates describe setup era, not a firmware number. Hardware platform only; Suite host OS/version and firmware bounds unresolved. No promise for all firmware, Model One, 33-word Suite creation or CLI advanced groups. See exact device row.; Non-selectable\: exact released-artifact binding and independent wallet recovery have not been verified. A dated unresolved-version marker is not a release interval; false generation means no generation claim for this specific record, not proof of absence.
- Profile guidance: Use the original trusted wallet backup/recovery procedure. Match product, platform, exact version and specific mode. Never enter a complete phrase/share or extra passphrase into Tessaveil.

<a id="wallet-trezor-safe-5"></a>

### Trezor Safe 5 — suite-single-share-20-created — trezor-safe-5

- Source record: [trezor-safe-5](../catalog/wallets/trezor-safe-5.json)
- Status: documented
- Reason: Evidence is insufficient for selectable support.
- Guidance: Not selectable; use the wallet's own backup procedure.
- Version interval (min / max): suite-firmware-version-unresolved-doc-2026-09-29 / suite-firmware-version-unresolved-doc-2026-09-29
- Verified on: 2026-09-29
- Historical: false
- Evidence: [slip39-trezor-safe-5](../catalog/evidence/slip39-trezor-safe-5.json)
- Evidence claim: Trezor Safe 5\: device-specific table row confirms20-word SLIP39 single/multi backup options. 20-word single-share is documented default. Exact Suite/firmware versions unpublished in article; no33-word Suite creation or cross-model inference. See docs/research/batches/slip39-algorand-cardano.md. Read through web retrieval; direct response was HTTP 403. No raw-body hash or immutable capture asserted.
- Aliases: —
- Scheme: [slip39-share-20](#scheme-slip39-share-20)
- Generates mnemonic / import only: true / false
- Limitations: 20-word single-share is documented default. Hardware platform only; Suite host OS/version and firmware bounds unresolved. No promise for all firmware, Model One, 33-word Suite creation or CLI advanced groups. See exact device row.; Non-selectable\: exact released-artifact binding and independent wallet recovery have not been verified. A dated unresolved-version marker is not a release interval; false generation means no generation claim for this specific record, not proof of absence.
- Profile guidance: Use the original trusted wallet backup/recovery procedure. Match product, platform, exact version and specific mode. Never enter a complete phrase/share or extra passphrase into Tessaveil.

<a id="wallet-trezor-safe-5-multi-share"></a>

### Trezor Safe 5 — suite-multi-share-20-created — trezor-safe-5-multi-share

- Source record: [trezor-safe-5-multi-share](../catalog/wallets/trezor-safe-5-multi-share.json)
- Status: documented
- Reason: Evidence is insufficient for selectable support.
- Guidance: Not selectable; use the wallet's own backup procedure.
- Version interval (min / max): suite-firmware-version-unresolved-doc-2026-09-29 / suite-firmware-version-unresolved-doc-2026-09-29
- Verified on: 2026-09-29
- Historical: false
- Evidence: [slip39-trezor-safe-5](../catalog/evidence/slip39-trezor-safe-5.json)
- Evidence claim: Trezor Safe 5\: device-specific table row confirms20-word SLIP39 single/multi backup options. 20-word single-share is documented default. Exact Suite/firmware versions unpublished in article; no33-word Suite creation or cross-model inference. See docs/research/batches/slip39-algorand-cardano.md. Read through web retrieval; direct response was HTTP 403. No raw-body hash or immutable capture asserted.
- Aliases: —
- Scheme: [slip39-share-20](#scheme-slip39-share-20)
- Generates mnemonic / import only: true / false
- Limitations: 20-word single-share is documented default. Hardware platform only; Suite host OS/version and firmware bounds unresolved. No promise for all firmware, Model One, 33-word Suite creation or CLI advanced groups. See exact device row.; Non-selectable\: exact released-artifact binding and independent wallet recovery have not been verified. A dated unresolved-version marker is not a release interval; false generation means no generation claim for this specific record, not proof of absence.
- Profile guidance: Use the original trusted wallet backup/recovery procedure. Match product, platform, exact version and specific mode. Never enter a complete phrase/share or extra passphrase into Tessaveil.

<a id="wallet-trezor-safe-7"></a>

### Trezor Safe 7 — suite-single-share-20-created — trezor-safe-7

- Source record: [trezor-safe-7](../catalog/wallets/trezor-safe-7.json)
- Status: documented
- Reason: Evidence is insufficient for selectable support.
- Guidance: Not selectable; use the wallet's own backup procedure.
- Version interval (min / max): suite-firmware-version-unresolved-doc-2026-09-29 / suite-firmware-version-unresolved-doc-2026-09-29
- Verified on: 2026-09-29
- Historical: false
- Evidence: [slip39-trezor-safe-7](../catalog/evidence/slip39-trezor-safe-7.json)
- Evidence claim: Trezor Safe 7\: device-specific table row confirms20-word SLIP39 single/multi backup options. 20-word single-share is documented default. Exact Suite/firmware versions unpublished in article; no33-word Suite creation or cross-model inference. See docs/research/batches/slip39-algorand-cardano.md. Read through web retrieval; direct response was HTTP 403. No raw-body hash or immutable capture asserted.
- Aliases: —
- Scheme: [slip39-share-20](#scheme-slip39-share-20)
- Generates mnemonic / import only: true / false
- Limitations: 20-word single-share is documented default. Hardware platform only; Suite host OS/version and firmware bounds unresolved. No promise for all firmware, Model One, 33-word Suite creation or CLI advanced groups. See exact device row.; Non-selectable\: exact released-artifact binding and independent wallet recovery have not been verified. A dated unresolved-version marker is not a release interval; false generation means no generation claim for this specific record, not proof of absence.
- Profile guidance: Use the original trusted wallet backup/recovery procedure. Match product, platform, exact version and specific mode. Never enter a complete phrase/share or extra passphrase into Tessaveil.

<a id="wallet-trezor-safe-7-multi-share"></a>

### Trezor Safe 7 — suite-multi-share-20-created — trezor-safe-7-multi-share

- Source record: [trezor-safe-7-multi-share](../catalog/wallets/trezor-safe-7-multi-share.json)
- Status: documented
- Reason: Evidence is insufficient for selectable support.
- Guidance: Not selectable; use the wallet's own backup procedure.
- Version interval (min / max): suite-firmware-version-unresolved-doc-2026-09-29 / suite-firmware-version-unresolved-doc-2026-09-29
- Verified on: 2026-09-29
- Historical: false
- Evidence: [slip39-trezor-safe-7](../catalog/evidence/slip39-trezor-safe-7.json)
- Evidence claim: Trezor Safe 7\: device-specific table row confirms20-word SLIP39 single/multi backup options. 20-word single-share is documented default. Exact Suite/firmware versions unpublished in article; no33-word Suite creation or cross-model inference. See docs/research/batches/slip39-algorand-cardano.md. Read through web retrieval; direct response was HTTP 403. No raw-body hash or immutable capture asserted.
- Aliases: —
- Scheme: [slip39-share-20](#scheme-slip39-share-20)
- Generates mnemonic / import only: true / false
- Limitations: 20-word single-share is documented default. Hardware platform only; Suite host OS/version and firmware bounds unresolved. No promise for all firmware, Model One, 33-word Suite creation or CLI advanced groups. See exact device row.; Non-selectable\: exact released-artifact binding and independent wallet recovery have not been verified. A dated unresolved-version marker is not a release interval; false generation means no generation claim for this specific record, not proof of absence.
- Profile guidance: Use the original trusted wallet backup/recovery procedure. Match product, platform, exact version and specific mode. Never enter a complete phrase/share or extra passphrase into Tessaveil.

<a id="wallet-typhon"></a>

### Typhon — web mnemonic creation unresolved — typhon

- Source record: [typhon](../catalog/wallets/typhon.json)
- Status: blocked
- Reason: Support is blocked; see evidence and license decisions below.
- Guidance: Not selectable; use the wallet's own backup procedure.
- Version interval (min / max): app-version-unresolved-doc-2026-09-29 / app-version-unresolved-doc-2026-09-29
- Verified on: 2026-09-29
- Historical: false
- Evidence: [cardano-typhon-create](../catalog/evidence/cardano-typhon-create.json)
- Evidence claim: Official help distinguishes web/extension creation, import and hardware connection. Web Create Wallet creates a new mnemonic. Retrieved article does not give exact mnemonic count or algorithm/version. See docs/research/batches/slip39-algorand-cardano.md. Read through web retrieval; direct response was HTTP 403. No raw-body hash or immutable capture asserted.
- Aliases: —
- Scheme: —
- Generates mnemonic / import only: true / false
- Limitations: Creation supported by official help, but12/15/24 selector and derivation not established by primary retrieved article. Import choices and testnet UI are not production generation evidence. No extension/mobile inference.; Non-selectable\: exact released-artifact binding and independent wallet recovery have not been verified. A dated unresolved-version marker is not a release interval; false generation means no generation claim for this specific record, not proof of absence.
- Profile guidance: Use the original trusted wallet backup/recovery procedure. Match product, platform, exact version and specific mode. Never enter a complete phrase/share or extra passphrase into Tessaveil.

<a id="wallet-yoroi"></a>

### Yoroi — extension15 creation — yoroi

- Source record: [yoroi](../catalog/wallets/yoroi.json)
- Status: documented
- Reason: Evidence is insufficient for selectable support.
- Guidance: Not selectable; use the wallet's own backup procedure.
- Version interval (min / max): source-91febfc95a288d3436b891356c87645611ea603a / source-91febfc95a288d3436b891356c87645611ea603a
- Verified on: 2026-09-29
- Historical: false
- Evidence: [cardano-yoroi-backup](../catalog/evidence/cardano-yoroi-backup.json), [cardano-yoroi-create](../catalog/evidence/cardano-yoroi-create.json)
- Evidence claim: Creation requests recovery phrase, initiates backup display, and finishes using that same phrase. This establishes creation/backup separately from import. Extension scope only. See docs/research/batches/slip39-algorand-cardano.md. Retrieved byte SHA-256 330e545c3035cc251c40ae6dd7895495a48f530cbe58d664159c6e0e87579c16.
- Evidence claim: generateAdaMnemonic explicitly generates160 bits/15 words; generateWalletRootKey passes BIP39 entropy and empty mnemonic password to from\_bip39\_entropy. Distinct Ledger helper is not default software generation. See docs/research/batches/slip39-algorand-cardano.md. Retrieved byte SHA-256 cb4e95b9bc4e8a30ecd3f6520424e556560155503ad03456988bf5a3fed4fa21.
- Aliases: —
- Scheme: [cardano-icarus-15](#scheme-cardano-icarus-15)
- Generates mnemonic / import only: true / false
- Limitations: Chrome-family extension source singleton; no mobile or all-releases claim.15 words, empty mnemonic password; spending password separately encrypts local wallet. Later seed re-export not established.; Non-selectable\: exact released-artifact binding and independent wallet recovery have not been verified. A dated unresolved-version marker is not a release interval; false generation means no generation claim for this specific record, not proof of absence.
- Profile guidance: Use the original trusted wallet backup/recovery procedure. Match product, platform, exact version and specific mode. Never enter a complete phrase/share or extra passphrase into Tessaveil.

<a id="wallet-zallet"></a>

### Zallet — English24 generation — zallet

- Source record: [zallet](../catalog/wallets/zallet.json)
- Status: documented
- Reason: Evidence is insufficient for selectable support.
- Guidance: Not selectable; use the wallet's own backup procedure.
- Version interval (min / max): f9dcd4d31439feb813c95ac2516814421f5b04df / f9dcd4d31439feb813c95ac2516814421f5b04df
- Verified on: 2026-09-29
- Historical: false
- Evidence: [zcash-zallet-create](../catalog/evidence/zcash-zallet-create.json), [zcash-zallet-empty](../catalog/evidence/zcash-zallet-empty.json), [zcash-zallet-export](../catalog/evidence/zcash-zallet-export.json)
- Evidence claim: generate-mnemonic chooses Count\:\:Words24 and English from32 random bytes; encrypted storage and backup confirmation are separate. Source-only beta scope, not tested released wallet.
- Evidence claim: Keystore reconstructs BIP39 mnemonic.to\_seed\(""\) and separately retains legacy non-mnemonic HD seeds. age identity passphrase encrypts storage and is not a BIP39 derivation passphrase.
- Evidence claim: Official book distinguishes mnemonic accounts from z\_importkey and standalone migrated keys; encrypted mnemonic export also requires its age identity. Exported phrase alone does not cover all wallet material.
- Aliases: —
- Scheme: [zcash-bip39](#scheme-zcash-bip39)
- Generates mnemonic / import only: true / false
- Limitations: Beta source; age-encrypted mnemonic export also needs age identity. Extra standalone keys are outside mnemonic backup.; Non-selectable\: exact shipped binary/dependency binding and independent restoration were not verified. Singleton source boundary is not an all-version compatibility claim.
- Profile guidance: Match original product, platform, version and mode; use its native backup procedure. Never enter a complete phrase, private key or external secret into Tessaveil.

<a id="wallet-zano-wallet"></a>

### Zano CLI — native26 — zano-wallet

- Source record: [zano-wallet](../catalog/wallets/zano-wallet.json)
- Status: documented
- Reason: Evidence is insufficient for selectable support.
- Guidance: Not selectable; use the wallet's own backup procedure.
- Version interval (min / max): e55c8ec47b76ed809162a958cf4600e03256a96a / e55c8ec47b76ed809162a958cf4600e03256a96a
- Verified on: 2026-09-29
- Historical: false
- Evidence: [zano-modes](../catalog/evidence/zano-modes.json), [zano-timestamp-password](../catalog/evidence/zano-timestamp-password.json)
- Evidence claim: get\_seed\_phrase emits 24 data words, timestamp/password-flag word25 and checksum/auditable word26. restore\_from\_seed\_phrase accepts25/26 and rejects24 at this exact commit. Seed password encrypts binary seed with legacy ChaCha; it is not BIP39 extension.
- Evidence claim: Timestamp is quantized with WALLET\_BRAIN\_DATE\_QUANTUM; word25 carries password-use flag. validate\_password uses a restricted ASCII regex; no Unicode NFKD or BIP39 salt is applied.
- Aliases: —
- Scheme: [zano-modern](#scheme-zano-modern)
- Generates mnemonic / import only: true / false
- Limitations: Native26 creation shown in core; Linux CLI entry-to-binary boundary unverified. Legacy24 rejected;25 import must preserve timestamp/password context.; Non-selectable\: exact shipped binary/dependency binding and independent restoration were not verified. Singleton source boundary is not an all-version compatibility claim.
- Profile guidance: Match original product, platform, version and mode; use its native backup procedure. Never enter a complete phrase, private key or external secret into Tessaveil.

<a id="wallet-zano-wallet-legacy25"></a>

### Zano CLI — legacy25 import — zano-wallet-legacy25

- Source record: [zano-wallet-legacy25](../catalog/wallets/zano-wallet-legacy25.json)
- Status: documented
- Reason: Evidence is insufficient for selectable support.
- Guidance: Not selectable; use the wallet's own backup procedure.
- Version interval (min / max): e55c8ec47b76ed809162a958cf4600e03256a96a / e55c8ec47b76ed809162a958cf4600e03256a96a
- Verified on: 2026-09-29
- Historical: true
- Evidence: [zano-history-vector](../catalog/evidence/zano-history-vector.json), [zano-modes](../catalog/evidence/zano-modes.json)
- Evidence claim: Pinned public wallet\_seed\_entries explicitly marks legacy24 invalid and old25 valid; includes26 checksum cases. Reviewed as upstream tests only, not executed recovery or evidence of which old release generated24.
- Evidence claim: get\_seed\_phrase emits 24 data words, timestamp/password-flag word25 and checksum/auditable word26. restore\_from\_seed\_phrase accepts25/26 and rejects24 at this exact commit. Seed password encrypts binary seed with legacy ChaCha; it is not BIP39 extension.
- Aliases: —
- Scheme: [zano-legacy-25](#scheme-zano-legacy-25)
- Generates mnemonic / import only: false / true
- Limitations: Historical25 accepted by current source; no historical generation interval proven.; Non-selectable\: exact shipped binary/dependency binding and independent restoration were not verified. Singleton source boundary is not an all-version compatibility claim.
- Profile guidance: Match original product, platform, version and mode; use its native backup procedure. Never enter a complete phrase, private key or external secret into Tessaveil.

<a id="wallet-zcash-official"></a>

### zcashd — English mnemonic mode — zcash-official

- Source record: [zcash-official](../catalog/wallets/zcash-official.json)
- Status: documented
- Reason: Evidence is insufficient for selectable support.
- Guidance: Not selectable; use the wallet's own backup procedure.
- Version interval (min / max): 558f686599586f55def3db86955d74d3be44605e / 558f686599586f55def3db86955d74d3be44605e
- Verified on: 2026-09-29
- Historical: false
- Evidence: [zcash-create](../catalog/evidence/zcash-create.json), [zcash-ffi](../catalog/evidence/zcash-ffi.json)
- Evidence claim: zcashd mnemonic source constructs BIP39 phrase from32-byte entropy, checks Zcash account derivability; FromLegacySeed creates a NEW mnemonic seed with nonce adjustment, not an identity-preserving conversion of every old key.
- Evidence claim: ZIP339 interface selects BIP39 languages and explicitly derives with empty passphrase. This batch is English24 only; standalone keys and legacy raw HD seeds are separate.
- Aliases: —
- Scheme: [zcash-bip39](#scheme-zcash-bip39)
- Generates mnemonic / import only: true / false
- Limitations: Exact mnemonic source only; old raw HD seeds and imported standalone keys need separate backups. zcashd bip0039 dependency version not bound to Zallet's.; Non-selectable\: exact shipped binary/dependency binding and independent restoration were not verified. Singleton source boundary is not an all-version compatibility claim.
- Profile guidance: Match original product, platform, version and mode; use its native backup procedure. Never enter a complete phrase, private key or external secret into Tessaveil.

<a id="wallet-zcash-official-standalone"></a>

### zcashd — standalone key export — zcash-official-standalone

- Source record: [zcash-official-standalone](../catalog/wallets/zcash-official-standalone.json)
- Status: no-mnemonic-confirmed
- Reason: This mode does not expose a supported mnemonic backup.
- Guidance: Not selectable; use the wallet's own backup procedure.
- Version interval (min / max): 558f686599586f55def3db86955d74d3be44605e / 558f686599586f55def3db86955d74d3be44605e
- Verified on: 2026-09-29
- Historical: false
- Evidence: [zcash-standalone](../catalog/evidence/zcash-standalone.json)
- Evidence claim: dumpprivkey and z\_exportkey export standalone transparent or shielded private-key encodings. These are not mnemonic word-table profiles; mnemonic backup cannot be assumed to cover imported keys.
- Aliases: —
- Scheme: —
- Generates mnemonic / import only: false / false
- Limitations: No mnemonic word table. Native dumpprivkey/z\_exportkey formats and full wallet backups retain necessary material.; Non-selectable\: exact shipped binary/dependency binding and independent restoration were not verified. Singleton source boundary is not an all-version compatibility claim.
- Profile guidance: Match original product, platform, version and mode; use its native backup procedure. Never enter a complete phrase, private key or external secret into Tessaveil.

## Schemes

<a id="scheme-algorand-25"></a>

### Algorand — legacy25 account key — algorand-25

- Source record: [algorand-25](../catalog/schemes/algorand-25.json)
- Status: documented
- Reason: Evidence is insufficient for selectable support.
- Guidance: Not selectable; use the wallet's own backup procedure.
- Version interval (min / max): 189855d43cba5d20e66248693d74332052ccb08e / 189855d43cba5d20e66248693d74332052ccb08e
- Verified on: 2026-09-29
- Historical: false
- Evidence: [algorand-algorithm](../catalog/evidence/algorand-algorithm.json), [algorand-dictionary](../catalog/evidence/algorand-dictionary.json), [algorand-license](../catalog/evidence/algorand-license.json), [algorand-vectors](../catalog/evidence/algorand-vectors.json)
- Evidence claim: Legacy account key representation\: 32 seed bytes become 24 little-endian 11-bit indices with eight zero padding bits; word 25 is the first little-endian 11 bits of SHA-512/256\(seed\). The 24th data index is 0..7, not any of 2048. No BIP39 checksum, PBKDF2 seed or universal-HD mapping is implied. from\_private\_key exports the first 32 bytes separately from generation. See docs/research/batches/slip39-algorand-cardano.md. Retrieved byte SHA-256 6d9387e3ee7213c14a1dec9f53a22f2880ee80b00df8457430f5ecae21f2c74e.
- Evidence claim: Extracted word\_list\_raw literal equals verified bip39-en entry-for-entry and in order \(2048\); LF serialization matches SHA-256 2f5eed53a4727b4bf8880d8f3f199efc90e58503646d9ff8eff3a2ed3b24dbda. Reuse existing dictionary reference; no second word file. See docs/research/batches/slip39-algorand-cardano.md. Retrieved byte SHA-256 bacc048829f092449fea722912b268ec9d6f5494776ca4ece50f463bb80e77d7.
- Evidence claim: MIT \(c\)2020 Algorand applies to public-vector projection. Retain license in THIRD\_PARTY\_NOTICES. No SDK or SDK dictionary file bundled. See docs/research/batches/slip39-algorand-cardano.md. Retrieved byte SHA-256 32b60f70e2a09ff695719af28a8ff60a8188d79de889d03913965f0d4b3d6055.
- Evidence claim: TestMnemonic.test\_zero\_mnemonic publishes the all-zero key fixed answer. Two additional clearly synthetic seeds \(ascending bytes and all FF\) are projected using the reviewed pinned upstream \_from\_key functions, independently of offline integer-based tests. No account/provider calls. See docs/research/batches/slip39-algorand-cardano.md. Retrieved byte SHA-256 9d1ae77d906174a845979221cf483b01e8756aeadf5e3d66d5f45ca6aca1d79f.
- Dictionaries: [bip39-en](#dictionary-bip39-en)
- Supported lengths: 25
- Position rules: Words1-23 are11-bit little-endian indices. Word24 holds the remaining3 seed bits \(indices0..7\); eight padding bits must be zero.; Word25 is an11-bit SHA-512/256 checksum index from the same dictionary; it is not a passphrase or a repeated Monero checksum word. Tessaveil never checks complete user phrases.
- Semantics: Shares BIP39 English words only; legacy32-byte account seed encoding differs from BIP39 and Pera Universal 24 HD. Public tests establish encoding only; no independent wallet recovery demonstrated.
- External secret / stored: none / false
- External-secret guidance: Any supported mnemonic passphrase stays outside Tessaveil; wallet login/spending passwords are distinct. Paper27 already includes its nine password words; no extra secret is inferred.
- Test vectors: [algorand-vectors](../catalog/evidence/algorand-vectors.json)

<a id="scheme-bip39"></a>

### BIP39 — bip39

- Source record: [bip39](../catalog/schemes/bip39.json)
- Status: verified
- Reason: Verified research record; not a release or security guarantee.
- Version interval (min / max): 3a10b5b5f0a7586df8928d580a3009744ebb2079 / 3a10b5b5f0a7586df8928d580a3009744ebb2079
- Verified on: 2026-09-29
- Historical: false
- Evidence: [bip39-spec](../catalog/evidence/bip39-spec.json), [bip39-vectors](../catalog/evidence/bip39-vectors.json)
- Evidence claim: Bitcoin BIP39 specifies 2048 indexed words, 12/15/18/21/24 lengths and UTF-8 NFKD for words, sentence and optional passphrase; equal vocabulary does not establish TON derivation. Reviewed 2026-09-29; byte SHA-256 afcbcbed36fe9eb734bd607398a8c124683ded2a75c3830e1b16c47b043a9134. See docs/research/batches/bip39-ton.md.
- Evidence claim: Trezor's public vectors.json supplies 24 independent entropy/mnemonic/seed known answers per language for all ten lists, with passphrase TREZOR. Offline test reconstructs words from entropy, checks published normalized sentence fingerprints and PBKDF2 seed. Public, non-funded data only; fixture projection contains no user phrase. Reviewed 2026-09-29; byte SHA-256 fa3b937b7cff9c9b8ecd3aa011faeb8d6dd67993174b72326e83f4de8fdb30f8. See docs/research/batches/bip39-ton.md.
- Dictionaries: [bip39-cs](#dictionary-bip39-cs), [bip39-en](#dictionary-bip39-en), [bip39-es](#dictionary-bip39-es), [bip39-fr](#dictionary-bip39-fr), [bip39-it](#dictionary-bip39-it), [bip39-ja](#dictionary-bip39-ja), [bip39-ko](#dictionary-bip39-ko), [bip39-pt](#dictionary-bip39-pt), [bip39-zh-hans](#dictionary-bip39-zh-hans), [bip39-zh-hant](#dictionary-bip39-zh-hant)
- Supported lengths: 12, 15, 18, 21, 24
- Position rules: The same dictionary is eligible at every word position. Phrase checksum or seed validity is never evaluated by Tessaveil.
- Semantics: Entropy plus SHA-256 checksum selects 11-bit word indices. UTF-8 NFKD sentence and passphrase feed PBKDF2-HMAC-SHA512 with 2048 iterations and mnemonic-prefixed salt. The research tests reproduce public vectors only; Tessaveil never derives user keys or validates a complete phrase. Language changes produce different seeds.
- External secret / stored: optional-passphrase / false
- External-secret guidance: A scheme passphrase is external and never stored by Tessaveil. A wallet PIN or application password is not proof of a mnemonic passphrase; verify support in the exact source wallet.
- Test vectors: [bip39-vectors](../catalog/evidence/bip39-vectors.json)

<a id="scheme-cake-decred-15"></a>

### Cake Decred — native15 birthday format — cake-decred-15

- Source record: [cake-decred-15](../catalog/schemes/cake-decred-15.json)
- Status: documented
- Reason: Evidence is insufficient for selectable support.
- Guidance: Not selectable; use the wallet's own backup procedure.
- Version interval (min / max): 37585833528544f80dddd92dcdff10a78ad01e1f / 37585833528544f80dddd92dcdff10a78ad01e1f
- Verified on: 2026-09-29
- Historical: false
- Evidence: [decred-cake-build](../catalog/evidence/decred-cake-build.json), [decred-cake-dependency](../catalog/evidence/decred-cake-dependency.json), [decred-cake-dispatch](../catalog/evidence/decred-cake-dispatch.json), [decred-cake-doc](../catalog/evidence/decred-cake-doc.json), [decred-cake-native](../catalog/evidence/decred-cake-native.json), [decred-cake-seed](../catalog/evidence/decred-cake-seed.json), [decred-cake-words](../catalog/evidence/decred-cake-words.json)
- Evidence claim: Android build source pins decred/libwallet ecc4a5fb9594368777848de42d7e072d62406507. This proves declared source binding, not executed release-binary contents. No iOS/macOS/Windows parity inferred.
- Evidence claim: Pinned libwallet requires dcrdex v1.0.5 resolved for review to full commit37585833528544f80dddd92dcdff10a78ad01e1f.
- Evidence claim: createWallet dispatches every15-word mnemonic to dcrdex native decoder,12/24 to libwallet BIP39-shaped decoder, otherwise errors. Thus ordinary15-word BIP39 input is not general BIP39 import here.
- Evidence claim: Retrieved2026-09-29 Seed Format text states15-word creation/restoration without exact app version. It conflicts with pinned current12/24 creation source; retain as dated unversioned documentation, not a current universal claim.
- Evidence claim: Native15 encodes18 entropy bytes \(144 bits\),2 big-endian Unix-day birthday bytes \(16 bits\),5 high SHA256 checksum bits as15 big-endian11-bit indices. Not BIP39 entropy semantics.
- Evidence claim: Native15 rejects nonempty seedpass and transforms18-byte entropy by BLAKE256\(entropy \|\| big-endian uint32\(42\)\); BIP39-shaped12/24 applies passphrase even empty. Local wallet encryption password is separate.
- Evidence claim: All2048 native15 words match existing bip39-en entry-for-entry in order. Only shared vocabulary is asserted; no duplicate list or Blue Oak implementation bytes bundled.
- Dictionaries: [bip39-en](#dictionary-bip39-en)
- Supported lengths: 15
- Position rules: Words encode144-bit entropy,16-bit big-endian Unix days, then5 high SHA256 checksum bits over those20 bytes. All15 use BIP39 English vocabulary.; Words1-13 contain143 entropy bits; word14 contains last entropy bit plus first10 date bits; word15 contains last6 date bits plus5 checksum bits. No checksum-only word.
- Semantics: Native dcrdex15 semantics, with libwallet BLAKE256\(entropy \|\| uint32be\(42\)\) Decred transformation. Current pinned Cake restores this format but creates BIP39-shaped12/24. Nonempty recovery passphrase rejected. No native15 independent fixed vector/wallet recovery yet.
- External secret / stored: none / false
- External-secret guidance: No derivation passphrase in this profile. Local wallet encryption password is distinct and is never stored.
- Test vectors: —

<a id="scheme-cake-decred-bip39-12-24"></a>

### Cake Decred — source-specific12/24 \(NFC deviation\) — cake-decred-bip39-12-24

- Source record: [cake-decred-bip39-12-24](../catalog/schemes/cake-decred-bip39-12-24.json)
- Status: blocked
- Reason: Support is blocked; see evidence and license decisions below.
- Guidance: Not selectable; use the wallet's own backup procedure.
- Version interval (min / max): ecc4a5fb9594368777848de42d7e072d62406507 / ecc4a5fb9594368777848de42d7e072d62406507
- Verified on: 2026-09-29
- Historical: false
- Evidence: [decred-cake-build](../catalog/evidence/decred-cake-build.json), [decred-cake-create](../catalog/evidence/decred-cake-create.json), [decred-cake-dispatch](../catalog/evidence/decred-cake-dispatch.json), [decred-cake-nfc](../catalog/evidence/decred-cake-nfc.json), [decred-cake-seed](../catalog/evidence/decred-cake-seed.json)
- Evidence claim: Android build source pins decred/libwallet ecc4a5fb9594368777848de42d7e072d62406507. This proves declared source binding, not executed release-binary contents. No iOS/macOS/Windows parity inferred.
- Evidence claim: Pinned current Cake service creates BIP39 using strength256 only for requested24, otherwise128; it passes mnemonic and seedpass to native libwallet. restoreFromSeed forwards native15. No current15 generation claim and no Android binary tested.
- Evidence claim: createWallet dispatches every15-word mnemonic to dcrdex native decoder,12/24 to libwallet BIP39-shaped decoder, otherwise errors. Thus ordinary15-word BIP39 input is not general BIP39 import here.
- Evidence claim: ApplyPassphrase normalizes words/pass to NFC, while BIP39 requires NFKD. ASCII examples do not establish general compatibility. Keep source-specific12/24 profile blocked pending Unicode behavior and released-artifact recovery review.
- Evidence claim: Native15 rejects nonempty seedpass and transforms18-byte entropy by BLAKE256\(entropy \|\| big-endian uint32\(42\)\); BIP39-shaped12/24 applies passphrase even empty. Local wallet encryption password is separate.
- Dictionaries: [bip39-en](#dictionary-bip39-en)
- Supported lengths: 12, 24
- Position rules: Current Cake creates128/256-bit BIP39-shaped12/24. Libwallet uses NFC passphrase normalization rather than normative NFKD.
- Semantics: Blocked\: general BIP39 compatibility is not established for Unicode passphrases; keep separate from both native15 and normative Decred BIP39.
- External secret / stored: optional-passphrase / false
- External-secret guidance: Any supported recovery passphrase and derivation path stay outside Tessaveil. Local encryption/unlock passwords are distinct.
- Test vectors: —

<a id="scheme-cake-zano-bip39"></a>

### Cake Zano BIP39-derived12/24 — cake-zano-bip39

- Source record: [cake-zano-bip39](../catalog/schemes/cake-zano-bip39.json)
- Status: blocked
- Reason: Support is blocked; see evidence and license decisions below.
- Guidance: Not selectable; use the wallet's own backup procedure.
- Version interval (min / max): 9679f91a8c9f63d00500c2b7cc18daf00949bdef / 9679f91a8c9f63d00500c2b7cc18daf00949bdef
- Verified on: 2026-09-29
- Historical: false
- Evidence: [zano-cake-bip39](../catalog/evidence/zano-cake-bip39.json), [zano-cake-modes](../catalog/evidence/zano-cake-modes.json)
- Evidence claim: Cake calls bip39 then BIP32 hardened44, hardened128, hardened0, child0, child0 and reduces private-key bytes as a little-endian integer modulo Ed25519 order. Exact Dart dependency byte/normalization and native binary binding not verified; own blocked scheme, no native26 compatibility inference.
- Evidence claim: Pinned Cake Android-targeted source creates12/24 BIP39 mnemonics, dispatches BIP39 restore separately from native Zano seed restore. No current native26 creation assertion; native backend release binding unresolved.
- Dictionaries: [bip39-en](#dictionary-bip39-en)
- Supported lengths: 12, 24
- Position rules: Dart BIP39 mnemonic -&gt; BIP32 hardened44, hardened128, hardened0, child0, child0 -&gt; little-endian modulo Ed25519 order.
- Semantics: Unverified Dart dependency normalization and native derivation binding; separate from native Zano26.
- External secret / stored: optional-passphrase / false
- External-secret guidance: Exact original seed password and mode are required for recovery when used; never store the secret in Tessaveil.
- Test vectors: —

<a id="scheme-cardano-byron"></a>

### Cardano — historical Daedalus Byron 12 — cardano-byron

- Source record: [cardano-byron](../catalog/schemes/cardano-byron.json)
- Status: documented
- Reason: Evidence is insufficient for selectable support.
- Guidance: Not selectable; use the wallet's own backup procedure.
- Version interval (min / max): 4ca4dcefccc7143672cf07a0b760d9e5abfc7797 / 4ca4dcefccc7143672cf07a0b760d9e5abfc7797
- Verified on: 2026-09-29
- Historical: true
- Evidence: [cardano-byron-rules](../catalog/evidence/cardano-byron-rules.json), [cardano-cip3](../catalog/evidence/cardano-cip3.json), [cardano-daedalus-lengths](../catalog/evidence/cardano-daedalus-lengths.json)
- Evidence claim: Deprecated Daedalus random/Byron root format uses iterative HMAC/SHA512 with Root Seed Chain domain and rejection/tweaking; differs from Icarus. Public examples are 12 words; current/historical wallet scope is separately sourced. See docs/research/batches/slip39-algorand-cardano.md. Retrieved byte SHA-256 0d46c673348dccdaf32f1cc3732a744745494478417cb6e2388247ecd12a25d6.
- Evidence claim: Recovery phrase conversion follows BIP39, but Byron, Icarus, Icarus-Trezor and Ledger/BitBox02 master-key algorithms are distinct. CIP 3 names Yoroi/Daedalus explicitly. Citation only; CC-BY-4.0 document and vector bytes are not redistributed. See docs/research/batches/slip39-algorand-cardano.md. Retrieved byte SHA-256 84a4abe37702847073aac805452c570ac8bc80a8723d89875826f3d5f1f034e4.
- Evidence claim: Explicit constants distinguish regular 24, legacy12, Yoroi15 and paper 27, split18 printed plus9 written. Constants do not prove creation routes; api and restore mapping evidence are separate. See docs/research/batches/slip39-algorand-cardano.md. Retrieved byte SHA-256 58d94791c7826fca095e4f56e213ea04cd69a4cd915eab0b7cb3103b8f35a265.
- Dictionaries: [bip39-en](#dictionary-bip39-en)
- Supported lengths: 12
- Position rules: Twelve BIP39 dictionary words encode entropy/checksum; legacy random/Byron master-key semantics, not Icarus or Ledger.
- Semantics: Deprecated random-address Daedalus mode; initial entropy preprocessing, backend artifact and full fixed recovery not reproduced. Non-selectable.
- External secret / stored: none / false
- External-secret guidance: Any supported mnemonic passphrase stays outside Tessaveil; wallet login/spending passwords are distinct. Paper27 already includes its nine password words; no extra secret is inferred.
- Test vectors: —

<a id="scheme-cardano-daedalus-27"></a>

### Daedalus — historical paper 27 — cardano-daedalus-27

- Source record: [cardano-daedalus-27](../catalog/schemes/cardano-daedalus-27.json)
- Status: documented
- Reason: Evidence is insufficient for selectable support.
- Guidance: Not selectable; use the wallet's own backup procedure.
- Version interval (min / max): 6c57eb94753211f66d3a63f49d031bf746044755 / 6c57eb94753211f66d3a63f49d031bf746044755
- Verified on: 2026-09-29
- Historical: true
- Evidence: [cardano-daedalus-dictionary](../catalog/evidence/cardano-daedalus-dictionary.json), [cardano-daedalus-lengths](../catalog/evidence/cardano-daedalus-lengths.json), [cardano-paper-license](../catalog/evidence/cardano-paper-license.json), [cardano-paper-rules](../catalog/evidence/cardano-paper-rules.json), [cardano-paper-vector](../catalog/evidence/cardano-paper-vector.json)
- Evidence claim: Extracted 2048 literal words match verified bip39-en in exact order; no duplicated file committed. crypto.ts explicitly passes this English list to generation. See docs/research/batches/slip39-algorand-cardano.md. Retrieved byte SHA-256 6a445ce64e8068dc7f523546e4f7788c0315365ff1561b389eea524629e18386.
- Evidence claim: Explicit constants distinguish regular 24, legacy12, Yoroi15 and paper 27, split18 printed plus9 written. Constants do not prove creation routes; api and restore mapping evidence are separate. See docs/research/batches/slip39-algorand-cardano.md. Retrieved byte SHA-256 58d94791c7826fca095e4f56e213ea04cd69a4cd915eab0b7cb3103b8f35a265.
- Evidence claim: Codex review 2026-09-29\: Daedalus root Apache-2.0 LICENSE and LICENSE NOTICE at the same revision cover the explicitly synthetic public certificate fixture. Intended redistribution is only modified indices/fingerprints, with modification notice, complete Apache text \(root LICENSE and THIRD\_PARTY\_NOTICES\) and Copyright 2019 IOHK notice retained. Repository redistribution allowed; local SignPath component license compatible, not Foundation acceptance or release approval. No CC-BY CIP vector bytes or runtime crypto dependency bundled. NOTICE SHA-256 d7fe15fe73be69f2543950c5b87a9c3964bd31ccbaa51a6127e7d88aea877190. See docs/research/batches/slip39-algorand-cardano.md.
- Evidence claim: getScrambledInput separates first18 scrambled certificate words and last9 password words. PBKDF2-HMAC-SHA512 of nine-word suffix with mnemonic salt, 2048 rounds, 32 bytes; rust-cardano-crypto performs unscrambling. This is not a 27-word BIP39 phrase. Nine words are inside27, not an extra user secret. See docs/research/batches/slip39-algorand-cardano.md. Retrieved byte SHA-256 02c137b08bf4394f95afeaf6e81a538ff39b15719fe326b8dbf1728c1a04cfd4.
- Evidence claim: Upstream explicitly synthetic, never-funded public certificate \(2026-08-27\), projected to 27 indices and sentence/password hashes. Tests verify partition and password input only, NOT unscrambling or recovery. Source notes creation retirement but retained source helpers are not proof of reachable creation UI. See docs/research/batches/slip39-algorand-cardano.md. Retrieved byte SHA-256 2c7449afaf97bf85b62537c655323def5bb6f328755dae303ac3f52a6465e13b.
- Dictionaries: [bip39-en](#dictionary-bip39-en)
- Supported lengths: 27
- Position rules: Positions1-18\: scrambled paper-certificate mnemonic. Positions19-27\: nine-word input to certificate-password KDF. All use English dictionary; concatenation is not a BIP39 mnemonic.
- Semantics: Historical27 =18\+9 certificate for a Byron 12 wallet. Never concatenate into Icarus, generic BIP39 or modern Lace PGP paper mode. Offline vector only verifies dictionary/partition/password; full rust-cardano-crypto unscrambling remains unverified.
- External secret / stored: none / false
- External-secret guidance: Any supported mnemonic passphrase stays outside Tessaveil; wallet login/spending passwords are distinct. Paper27 already includes its nine password words; no extra secret is inferred.
- Test vectors: [cardano-paper-vector](../catalog/evidence/cardano-paper-vector.json)

<a id="scheme-cardano-hardware"></a>

### Cardano — unresolved hardware-specific modes — cardano-hardware

- Source record: [cardano-hardware](../catalog/schemes/cardano-hardware.json)
- Status: blocked
- Reason: Support is blocked; see evidence and license decisions below.
- Guidance: Not selectable; use the wallet's own backup procedure.
- Version interval (min / max): 4ca4dcefccc7143672cf07a0b760d9e5abfc7797 / 4ca4dcefccc7143672cf07a0b760d9e5abfc7797
- Verified on: 2026-09-29
- Historical: false
- Evidence: [cardano-cip3](../catalog/evidence/cardano-cip3.json), [cardano-hardware-rules](../catalog/evidence/cardano-hardware-rules.json), [cardano-icarus-rules](../catalog/evidence/cardano-icarus-rules.json)
- Evidence claim: Recovery phrase conversion follows BIP39, but Byron, Icarus, Icarus-Trezor and Ledger/BitBox02 master-key algorithms are distinct. CIP 3 names Yoroi/Daedalus explicitly. Citation only; CC-BY-4.0 document and vector bytes are not redistributed. See docs/research/batches/slip39-algorand-cardano.md. Retrieved byte SHA-256 84a4abe37702847073aac805452c570ac8bc80a8723d89875826f3d5f1f034e4.
- Evidence claim: Ledger/BitBox02 use a BIP39 seed then a distinct HMAC/rejection scheme, unlike Icarus-Trezor. Hardware is not a single phrase format. No model/firmware/creation length binding researched here\: umbrella record blocked with empty dictionary/length lists. See docs/research/batches/slip39-algorand-cardano.md. Retrieved byte SHA-256 164975c4556ae04fa00377f431e37be35b6fdd2b84b0fd7843a859093c3fe62f.
- Evidence claim: Icarus uses PBKDF2-HMAC-SHA512, 4096 iterations, entropy as salt, optional separate mnemonic password, 96 output bytes then bit tweaks. Icarus-Trezor retains the extra checksum byte for 24-word input; below 24 it matches Icarus. Never substitute a generic BIP39 seed derivation. See docs/research/batches/slip39-algorand-cardano.md. Retrieved byte SHA-256 f83da5fbdc6865a0de83edb7219208908e109b2a50671c8a9682d7c3d1179a85.
- Dictionaries: —
- Supported lengths: —
- Position rules: No shared selectable hardware dictionary or length set. Match exact vendor/model/firmware/backup and derivation mode first.
- Semantics: Icarus-Trezor and Ledger/BitBox02 differ, including Trezor 24 checksum-byte handling. Generic hardware label is blocked; SLIP39 device support does not prove Cardano derivation. No universal length/mapping asserted.
- External secret / stored: optional-passphrase / false
- External-secret guidance: Any supported mnemonic passphrase stays outside Tessaveil; wallet login/spending passwords are distinct. Paper27 already includes its nine password words; no extra secret is inferred.
- Test vectors: —

<a id="scheme-cardano-icarus"></a>

### Cardano — Icarus 15/24 — cardano-icarus

- Source record: [cardano-icarus](../catalog/schemes/cardano-icarus.json)
- Status: documented
- Reason: Evidence is insufficient for selectable support.
- Guidance: Not selectable; use the wallet's own backup procedure.
- Version interval (min / max): 4ca4dcefccc7143672cf07a0b760d9e5abfc7797 / 4ca4dcefccc7143672cf07a0b760d9e5abfc7797
- Verified on: 2026-09-29
- Historical: false
- Evidence: [cardano-cip3](../catalog/evidence/cardano-cip3.json), [cardano-daedalus-lengths](../catalog/evidence/cardano-daedalus-lengths.json), [cardano-icarus-rules](../catalog/evidence/cardano-icarus-rules.json)
- Evidence claim: Recovery phrase conversion follows BIP39, but Byron, Icarus, Icarus-Trezor and Ledger/BitBox02 master-key algorithms are distinct. CIP 3 names Yoroi/Daedalus explicitly. Citation only; CC-BY-4.0 document and vector bytes are not redistributed. See docs/research/batches/slip39-algorand-cardano.md. Retrieved byte SHA-256 84a4abe37702847073aac805452c570ac8bc80a8723d89875826f3d5f1f034e4.
- Evidence claim: Explicit constants distinguish regular 24, legacy12, Yoroi15 and paper 27, split18 printed plus9 written. Constants do not prove creation routes; api and restore mapping evidence are separate. See docs/research/batches/slip39-algorand-cardano.md. Retrieved byte SHA-256 58d94791c7826fca095e4f56e213ea04cd69a4cd915eab0b7cb3103b8f35a265.
- Evidence claim: Icarus uses PBKDF2-HMAC-SHA512, 4096 iterations, entropy as salt, optional separate mnemonic password, 96 output bytes then bit tweaks. Icarus-Trezor retains the extra checksum byte for 24-word input; below 24 it matches Icarus. Never substitute a generic BIP39 seed derivation. See docs/research/batches/slip39-algorand-cardano.md. Retrieved byte SHA-256 f83da5fbdc6865a0de83edb7219208908e109b2a50671c8a9682d7c3d1179a85.
- Dictionaries: [bip39-en](#dictionary-bip39-en)
- Supported lengths: 15, 24
- Position rules: Same BIP39 English dictionary at every position; entropy/checksum packing is BIP39, master-key derivation is Icarus.; 15-word Yoroi creation and 24-word Daedalus creation are separate exact source modes; listed lengths are scoped profiles, not all theoretical Icarus inputs.
- Semantics: Icarus 96-byte root, 4096-round PBKDF2, entropy salt, separate optional mnemonic password. Yoroi/Nami examined source uses empty mnemonic password; spending password is not this secret. No wallet-level recovery vector independently reproduced. Trezor 24 checksum deviation is excluded.
- External secret / stored: optional-passphrase / false
- External-secret guidance: Any supported mnemonic passphrase stays outside Tessaveil; wallet login/spending passwords are distinct. Paper27 already includes its nine password words; no extra secret is inferred.
- Test vectors: —

<a id="scheme-cardano-icarus-15"></a>

### Cardano — Icarus 15 — cardano-icarus-15

- Source record: [cardano-icarus-15](../catalog/schemes/cardano-icarus-15.json)
- Status: documented
- Reason: Evidence is insufficient for selectable support.
- Guidance: Not selectable; use the wallet's own backup procedure.
- Version interval (min / max): 4ca4dcefccc7143672cf07a0b760d9e5abfc7797 / 4ca4dcefccc7143672cf07a0b760d9e5abfc7797
- Verified on: 2026-09-29
- Historical: false
- Evidence: [cardano-cip3](../catalog/evidence/cardano-cip3.json), [cardano-icarus-rules](../catalog/evidence/cardano-icarus-rules.json), [cardano-yoroi-create](../catalog/evidence/cardano-yoroi-create.json)
- Evidence claim: Recovery phrase conversion follows BIP39, but Byron, Icarus, Icarus-Trezor and Ledger/BitBox02 master-key algorithms are distinct. CIP 3 names Yoroi/Daedalus explicitly. Citation only; CC-BY-4.0 document and vector bytes are not redistributed. See docs/research/batches/slip39-algorand-cardano.md. Retrieved byte SHA-256 84a4abe37702847073aac805452c570ac8bc80a8723d89875826f3d5f1f034e4.
- Evidence claim: Icarus uses PBKDF2-HMAC-SHA512, 4096 iterations, entropy as salt, optional separate mnemonic password, 96 output bytes then bit tweaks. Icarus-Trezor retains the extra checksum byte for 24-word input; below 24 it matches Icarus. Never substitute a generic BIP39 seed derivation. See docs/research/batches/slip39-algorand-cardano.md. Retrieved byte SHA-256 f83da5fbdc6865a0de83edb7219208908e109b2a50671c8a9682d7c3d1179a85.
- Evidence claim: generateAdaMnemonic explicitly generates160 bits/15 words; generateWalletRootKey passes BIP39 entropy and empty mnemonic password to from\_bip39\_entropy. Distinct Ledger helper is not default software generation. See docs/research/batches/slip39-algorand-cardano.md. Retrieved byte SHA-256 cb4e95b9bc4e8a30ecd3f6520424e556560155503ad03456988bf5a3fed4fa21.
- Dictionaries: [bip39-en](#dictionary-bip39-en)
- Supported lengths: 15
- Position rules: Same BIP39 English dictionary at every position; entropy/checksum packing is BIP39, master-key derivation is Icarus.; 15-word Yoroi creation and 24-word Daedalus creation are separate exact source modes; listed lengths are scoped profiles, not all theoretical Icarus inputs.
- Semantics: Icarus 96-byte root, 4096-round PBKDF2, entropy salt, separate optional mnemonic password. Yoroi/Nami examined source uses empty mnemonic password; spending password is not this secret. No wallet-level recovery vector independently reproduced. Trezor 24 checksum deviation is excluded.
- External secret / stored: optional-passphrase / false
- External-secret guidance: Any supported mnemonic passphrase stays outside Tessaveil; wallet login/spending passwords are distinct. Paper27 already includes its nine password words; no extra secret is inferred.
- Test vectors: —

<a id="scheme-cardano-icarus-24"></a>

### Cardano — Icarus 24 — cardano-icarus-24

- Source record: [cardano-icarus-24](../catalog/schemes/cardano-icarus-24.json)
- Status: documented
- Reason: Evidence is insufficient for selectable support.
- Guidance: Not selectable; use the wallet's own backup procedure.
- Version interval (min / max): 4ca4dcefccc7143672cf07a0b760d9e5abfc7797 / 4ca4dcefccc7143672cf07a0b760d9e5abfc7797
- Verified on: 2026-09-29
- Historical: false
- Evidence: [cardano-cip3](../catalog/evidence/cardano-cip3.json), [cardano-daedalus-dictionary](../catalog/evidence/cardano-daedalus-dictionary.json), [cardano-daedalus-lengths](../catalog/evidence/cardano-daedalus-lengths.json), [cardano-icarus-rules](../catalog/evidence/cardano-icarus-rules.json)
- Evidence claim: Recovery phrase conversion follows BIP39, but Byron, Icarus, Icarus-Trezor and Ledger/BitBox02 master-key algorithms are distinct. CIP 3 names Yoroi/Daedalus explicitly. Citation only; CC-BY-4.0 document and vector bytes are not redistributed. See docs/research/batches/slip39-algorand-cardano.md. Retrieved byte SHA-256 84a4abe37702847073aac805452c570ac8bc80a8723d89875826f3d5f1f034e4.
- Evidence claim: Extracted 2048 literal words match verified bip39-en in exact order; no duplicated file committed. crypto.ts explicitly passes this English list to generation. See docs/research/batches/slip39-algorand-cardano.md. Retrieved byte SHA-256 6a445ce64e8068dc7f523546e4f7788c0315365ff1561b389eea524629e18386.
- Evidence claim: Explicit constants distinguish regular 24, legacy12, Yoroi15 and paper 27, split18 printed plus9 written. Constants do not prove creation routes; api and restore mapping evidence are separate. See docs/research/batches/slip39-algorand-cardano.md. Retrieved byte SHA-256 58d94791c7826fca095e4f56e213ea04cd69a4cd915eab0b7cb3103b8f35a265.
- Evidence claim: Icarus uses PBKDF2-HMAC-SHA512, 4096 iterations, entropy as salt, optional separate mnemonic password, 96 output bytes then bit tweaks. Icarus-Trezor retains the extra checksum byte for 24-word input; below 24 it matches Icarus. Never substitute a generic BIP39 seed derivation. See docs/research/batches/slip39-algorand-cardano.md. Retrieved byte SHA-256 f83da5fbdc6865a0de83edb7219208908e109b2a50671c8a9682d7c3d1179a85.
- Dictionaries: [bip39-en](#dictionary-bip39-en)
- Supported lengths: 24
- Position rules: Same BIP39 English dictionary at every position; entropy/checksum packing is BIP39, master-key derivation is Icarus.; 15-word Yoroi creation and 24-word Daedalus creation are separate exact source modes; listed lengths are scoped profiles, not all theoretical Icarus inputs.
- Semantics: Icarus 96-byte root, 4096-round PBKDF2, entropy salt, separate optional mnemonic password. Yoroi/Nami examined source uses empty mnemonic password; spending password is not this secret. No wallet-level recovery vector independently reproduced. Trezor 24 checksum deviation is excluded.
- External secret / stored: optional-passphrase / false
- External-secret guidance: Any supported mnemonic passphrase stays outside Tessaveil; wallet login/spending passwords are distinct. Paper27 already includes its nine password words; no extra secret is inferred.
- Test vectors: —

<a id="scheme-chia-bip39"></a>

### Chia default English24 — chia-bip39

- Source record: [chia-bip39](../catalog/schemes/chia-bip39.json)
- Status: documented
- Reason: Evidence is insufficient for selectable support.
- Guidance: Not selectable; use the wallet's own backup procedure.
- Version interval (min / max): af0d7eab5fb12bbd8af51f47a7123ee700d74c2a / af0d7eab5fb12bbd8af51f47a7123ee700d74c2a
- Verified on: 2026-09-29
- Historical: false
- Evidence: [chia-license](../catalog/evidence/chia-license.json), [chia-source](../catalog/evidence/chia-source.json), [chia-vectors](../catalog/evidence/chia-vectors.json)
- Evidence claim: Apache-2.0 Copyright2026 Chia Network Inc. covers modified public test projections; original Trezor BIP39 provenance and existing MIT notice retained too. Full Apache terms already in THIRD\_PARTY\_NOTICES/root LICENSE. Codex2026-09-29 data-only allowed/local SignPath compatible, not acceptance.
- Evidence claim: generate\_mnemonic uses32 random bytes =&gt;24 BIP39-English words. mnemonic\_to\_seed normalizes NFKD, PBKDF2-HMAC-SHA5122048, salt mnemonic with no user extension. Master keyring passphrase is separate; BLS derivation is not BIP32.
- Evidence claim: 24 published English entropy/mnemonic/empty-passphrase seed vectors projected to indices and expected seed fingerprints. Includes12/18/24 primitive cases; generation profile remains24 only.
- Dictionaries: [bip39-en](#dictionary-bip39-en)
- Supported lengths: 24
- Position rules: Default generation24; primitive import also accepts12/15/18/21/24 and4-character English prefixes.
- Semantics: BIP39 encoding and empty-passphrase PBKDF2 feed BLS keys; no BIP32 or generic wallet compatibility implied.
- External secret / stored: none / false
- External-secret guidance: No mnemonic derivation extension in this exact mode. Local storage/unlock passwords are separate; never enter them into Tessaveil.
- Test vectors: [chia-vectors](../catalog/evidence/chia-vectors.json)

<a id="scheme-decred-bip39"></a>

### Decred — BIP39 compatibility family — decred-bip39

- Source record: [decred-bip39](../catalog/schemes/decred-bip39.json)
- Status: documented
- Reason: Evidence is insufficient for selectable support.
- Guidance: Not selectable; use the wallet's own backup procedure.
- Version interval (min / max): 30e042a46a97cf78f9766904d3ca4e5ed253266d / 30e042a46a97cf78f9766904d3ca4e5ed253266d
- Verified on: 2026-09-29
- Historical: false
- Evidence: [decred-bip39-doc](../catalog/evidence/decred-bip39-doc.json)
- Evidence claim: Official source documentation distinguishes PGP33 direct wallet seed from BIP39 sentence\+passphrase seed; describes external conversion to hex for Decrediton/dcrwallet. This does not prove native BIP39 phrase generation or direct phrase import in Decrediton.
- Dictionaries: [bip39-en](#dictionary-bip39-en)
- Supported lengths: 12, 15, 18, 21, 24
- Position rules: BIP39 entropy and checksum lengths; mnemonic\+optional NFKD passphrase derive a seed. Only vocabulary/general family is mapped, no wallet-specific path.
- Semantics: Official docs describe external BIP39-to-hex conversion for native wallet restoration. This is not direct Decrediton BIP39 generation/import and not Cake15. Exact hardware/product recovery remains unverified.
- External secret / stored: optional-passphrase / false
- External-secret guidance: Any supported recovery passphrase and derivation path stay outside Tessaveil. Local encryption/unlock passwords are distinct.
- Test vectors: —

<a id="scheme-decred-pgp33"></a>

### Decred — native PGP33 — decred-pgp33

- Source record: [decred-pgp33](../catalog/schemes/decred-pgp33.json)
- Status: documented
- Reason: Evidence is insufficient for selectable support.
- Guidance: Not selectable; use the wallet's own backup procedure.
- Version interval (min / max): c0fee6b52ad30961cfc3e06017d5e7516952615e / c0fee6b52ad30961cfc3e06017d5e7516952615e
- Verified on: 2026-09-29
- Historical: false
- Evidence: [decred-decrediton-license](../catalog/evidence/decred-decrediton-license.json), [decred-pgp-checksum](../catalog/evidence/decred-pgp-checksum.json), [decred-pgp-position](../catalog/evidence/decred-pgp-position.json), [decred-pgp-vectors](../catalog/evidence/decred-pgp-vectors.json), [decred-pgp33-reference](../catalog/evidence/decred-pgp33-reference.json)
- Evidence claim: ISC notice retained for modified synthetic output projections from the official Decrediton encoder. No implementation/library or wallet binary bundled.
- Evidence claim: EncodeMnemonic appends first byte of double SHA256\(seed\), selecting the half at index len\(seed\). For 32 bytes, word33 uses the even half. Other accepted seed lengths are not mapped to the PGP33 profile.
- Evidence claim: ByteToMnemonic selects half by zero-based position, not byte parity. DecodeMnemonics rejects wrong-position half and compares words case-insensitively.
- Evidence claim: Public known-answer mnemonicTests cover 20- and 31-byte seeds; fixed expected words project to indices/fingerprints and corroborate ordering/checksum. They are not mislabeled 33-word examples.
- Evidence claim: Reviewed pinned independent official JavaScript encodeMnemonic produces expected 33-word outputs for synthetic zero and ascending 32-byte seeds using Node24.13 WebCrypto; no wallet process or network execution. Used as reference, not implementation under test.
- Dictionaries: [pgp-even](#dictionary-pgp-even), [pgp-odd](#dictionary-pgp-odd)
- Supported lengths: 33
- Position rules: positions 1,3,5,7,9,11,13,15,17,19,21,23,25,27,29,31,33\: pgp-even; positions 2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32\: pgp-odd; Position numbers above are one-based. Bytes determine index within a half; positions determine half. Word33 encodes first byte SHA256\(SHA256\(seed\)\) and is even-half, not a passphrase.
- Semantics: 32-byte raw wallet seed plus one checksum byte. Never substitute BIP39 or Cake native15 even though all target Decred.
- External secret / stored: none / false
- External-secret guidance: No derivation passphrase in this profile. Local wallet encryption password is distinct and is never stored.
- Test vectors: [decred-pgp-vectors](../catalog/evidence/decred-pgp-vectors.json), [decred-pgp33-reference](../catalog/evidence/decred-pgp33-reference.json)

<a id="scheme-electrum-v1"></a>

### Electrum v1 — legacy import12/24 — electrum-v1

- Source record: [electrum-v1](../catalog/schemes/electrum-v1.json)
- Status: blocked
- Reason: Support is blocked; see evidence and license decisions below.
- Guidance: Not selectable; use the wallet's own backup procedure.
- Version interval (min / max): ede66c89887234c83b0def133b3100fe92a160eb / ede66c89887234c83b0def133b3100fe92a160eb
- Verified on: 2026-09-29
- Historical: true
- Evidence: [electrum-legacy-list](../catalog/evidence/electrum-legacy-list.json), [electrum-v2-source](../catalog/evidence/electrum-v2-source.json)
- Evidence claim: Pinned legacy encoder has 1626 English words in fixed order and encodes each 32-bit chunk as three dependent indices. File MIT header also cites a Wiktionary contemporary-poetry list; cumulative upstream data rights are not resolved. No legacy list bytes bundled.
- Evidence claim: Electrum 4.8.2-source\: default English 132-bit make\_seed uses HMAC-SHA512 Seed version prefixes, normalized sentence and electrum-prefixed PBKDF2 salt, not BIP39 entropy/checksum semantics. Old recognition accepts 12/24 words; native generation normally 12 with possible nonce overflow to 13. No wallet artifact tested.
- Dictionaries: [electrum-v1-en](#dictionary-electrum-v1-en)
- Supported lengths: 12, 24
- Position rules: Three-word groups encode32-bit chunks using modulo1626 relative indices; no BIP39 checksum. Current old recognition accepts12/24, not all historical variants.
- Semantics: Legacy pre2.0 encoding as recognized by pinned4.8.2 source; no current generation claim. Dictionary licensing blocks selection.
- External secret / stored: none / false
- External-secret guidance: No derivation passphrase in this profile. Local wallet encryption password is distinct and is never stored.
- Test vectors: —

<a id="scheme-electrum-v2"></a>

### Electrum v2 — English native seed — electrum-v2

- Source record: [electrum-v2](../catalog/schemes/electrum-v2.json)
- Status: documented
- Reason: Evidence is insufficient for selectable support.
- Guidance: Not selectable; use the wallet's own backup procedure.
- Version interval (min / max): ede66c89887234c83b0def133b3100fe92a160eb / ede66c89887234c83b0def133b3100fe92a160eb
- Verified on: 2026-09-29
- Historical: false
- Evidence: [electrum-public-vectors](../catalog/evidence/electrum-public-vectors.json), [electrum-v2-dictionary](../catalog/evidence/electrum-v2-dictionary.json), [electrum-v2-source](../catalog/evidence/electrum-v2-source.json), [electrum-vector-license](../catalog/evidence/electrum-vector-license.json), [electrum-version](../catalog/evidence/electrum-version.json)
- Evidence claim: Public English segwit vectors with empty and explicit passphrase; projections preserve indices and expected seed fingerprints, tested offline. Tests also show old12/24 and 13-word native seed recognition. No user phrases or recovery.
- Evidence claim: Exact upstream English bytes equal existing bip39-en SHA-256; equality proves vocabulary only.
- Evidence claim: Electrum 4.8.2-source\: default English 132-bit make\_seed uses HMAC-SHA512 Seed version prefixes, normalized sentence and electrum-prefixed PBKDF2 salt, not BIP39 entropy/checksum semantics. Old recognition accepts 12/24 words; native generation normally 12 with possible nonce overflow to 13. No wallet artifact tested.
- Evidence claim: MIT applies to modified public test projections; complete notice retained in THIRD\_PARTY\_NOTICES. No legacy dictionary permission is inferred.
- Evidence claim: Source package labels itself 4.8.2, with prefixes 01 standard, 100 segwit, 101 2FA, 102 2FA segwit; no release binary binding inferred.
- Dictionaries: [bip39-en](#dictionary-bip39-en)
- Supported lengths: 12, 13
- Position rules: English132-bit default generation normally12 words; nonce overflow may yield13. This is a scoped generation profile, not every accepted Electrum length.; HMAC-SHA512 Seed version prefix determines type; normalized sentence uses electrum salt for PBKDF2. Standard01 and segwit100 remain different wallet modes.
- Semantics: Same dictionary as BIP39, different integrity and derivation. Only English default standard/segwit generation lengths researched; no2FA, multisig or arbitrary-bit CLI support inferred.
- External secret / stored: optional-passphrase / false
- External-secret guidance: Any supported recovery passphrase and derivation path stay outside Tessaveil. Local encryption/unlock passwords are distinct.
- Test vectors: [electrum-public-vectors](../catalog/evidence/electrum-public-vectors.json)

<a id="scheme-monero-legacy"></a>

### monero-legacy — monero-legacy

- Source record: [monero-legacy](../catalog/schemes/monero-legacy.json)
- Status: documented
- Reason: Evidence is insufficient for selectable support.
- Guidance: Not selectable; use the wallet's own backup procedure.
- Version interval (min / max): 2f9d1bbb2c553dc75f3335bd1452117dfddd86fa / 2f9d1bbb2c553dc75f3335bd1452117dfddd86fa
- Verified on: 2026-09-29
- Historical: false
- Evidence: [monero-legacy-vectors](../catalog/evidence/monero-legacy-vectors.json), [monero-monero-legacy-scheme](../catalog/evidence/monero-monero-legacy-scheme.json)
- Evidence claim: Public Portuguese checksum and German case-tolerance examples; projection stores dictionary indices and expected phrase fingerprint. Offline test reproduces source CRC32 prefix check, not private-key/address derivation. Reviewed 2026-09-29; response byte SHA-256 520fec49e96e4b01d472f627e109b7a343f80e58291eed793f7ca76f2e63a1d1. See docs/research/batches/monero-polyseed.md.
- Evidence claim: Eight little-endian 32-bit chunks map to 24 base-1626 words; CRC32 of language-specific prefixes selects repeated 25th checksum word. Not BIP39. EnglishOld has a separate historical dictionary and is excluded from current-generation language list; no selectable historical 25-word mode is inferred. Source supports additional checksumless restore lengths; this profile covers standard 25 only. Reviewed 2026-09-29; response byte SHA-256 f92675503096425c92f6cc8b38946a707db6999cfcd95657f87a58d364051e4f. See docs/research/batches/monero-polyseed.md.
- Dictionaries: [monero-de](#dictionary-monero-de), [monero-en](#dictionary-monero-en), [monero-eo](#dictionary-monero-eo), [monero-es](#dictionary-monero-es), [monero-fr](#dictionary-monero-fr), [monero-it](#dictionary-monero-it), [monero-ja](#dictionary-monero-ja), [monero-jbo](#dictionary-monero-jbo), [monero-nl](#dictionary-monero-nl), [monero-pt](#dictionary-monero-pt), [monero-ru](#dictionary-monero-ru), [monero-zh-hans](#dictionary-monero-zh-hans)
- Supported lengths: 25
- Position rules: One dictionary per phrase; same vocabulary at each position. Last word is repeated checksum for 25/13; first word is Polyseed checksum for 16. No complete user phrase validation.
- Semantics: Eight little-endian 32-bit chunks map to 24 base-1626 words; CRC32 of language-specific prefixes selects repeated 25th checksum word. Not BIP39. EnglishOld has a separate historical dictionary and is excluded from current-generation language list; no selectable historical 25-word mode is inferred. Source supports additional checksumless restore lengths; this profile covers standard 25 only. Documented\: offline tests establish encoding/checksum only; full independent key derivation and exact wallet artifact binding are not established.
- External secret / stored: optional-passphrase / false
- External-secret guidance: Keep any supported seed offset/encryption passphrase separately. Tessaveil never stores it. App login passwords/PINs are not automatically mnemonic secrets; verify exact wallet mode.
- Test vectors: [monero-legacy-vectors](../catalog/evidence/monero-legacy-vectors.json)

<a id="scheme-mymonero-13"></a>

### mymonero-13 — mymonero-13

- Source record: [mymonero-13](../catalog/schemes/mymonero-13.json)
- Status: documented
- Reason: Evidence is insufficient for selectable support.
- Guidance: Not selectable; use the wallet's own backup procedure.
- Version interval (min / max): 9637c91cbe5f46e67156c66c739932294808109d / 9637c91cbe5f46e67156c66c739932294808109d
- Verified on: 2026-09-29
- Historical: false
- Evidence: [monero-mymonero-13-scheme](../catalog/evidence/monero-mymonero-13-scheme.json), [monero-mymonero-vectors](../catalog/evidence/monero-mymonero-vectors.json)
- Evidence claim: Legacy MyMonero\: four 32-bit chunks encode a 16-byte seed as 12 words plus prefix CRC32 checksum. Keccak expansion before scalar reduction differs from 32-byte Monero legacy. Current core new\_wallet creates a 32-byte/25-word seed; 13 words are retained for legacy decoding. English vector only; other language/product mappings are not verified. Reviewed 2026-09-29; response byte SHA-256 ea6d34729151cffd2b7cdd1a16c31507ff3122242540646ac9797cc0797bb7b4. See docs/research/batches/monero-polyseed.md.
- Evidence claim: Published 13-word prefix mnemonic resolves to the same address as published 16-byte seed 9c973aa296b79bbf452781dd3d32ad7f. Offline projection tests entropy and checksum only; no address/Keccak claim. Reviewed 2026-09-29; response byte SHA-256 8292f763a1b2bf70052dc959a2672e73a1b4035d5c379bbccb4e03f6a2de6634. See docs/research/batches/monero-polyseed.md.
- Dictionaries: [monero-en](#dictionary-monero-en)
- Supported lengths: 13
- Position rules: One dictionary per phrase; same vocabulary at each position. Last word is repeated checksum for 25/13; first word is Polyseed checksum for 16. No complete user phrase validation.
- Semantics: Legacy MyMonero\: four 32-bit chunks encode a 16-byte seed as 12 words plus prefix CRC32 checksum. Keccak expansion before scalar reduction differs from 32-byte Monero legacy. Current core new\_wallet creates a 32-byte/25-word seed; 13 words are retained for legacy decoding. English vector only; other language/product mappings are not verified. Documented\: offline tests establish encoding/checksum only; full independent key derivation and exact wallet artifact binding are not established.
- External secret / stored: none / false
- External-secret guidance: Keep any supported seed offset/encryption passphrase separately. Tessaveil never stores it. App login passwords/PINs are not automatically mnemonic secrets; verify exact wallet mode.
- Test vectors: [monero-mymonero-vectors](../catalog/evidence/monero-mymonero-vectors.json)

<a id="scheme-polyseed-16"></a>

### polyseed-16 — polyseed-16

- Source record: [polyseed-16](../catalog/schemes/polyseed-16.json)
- Status: documented
- Reason: Evidence is insufficient for selectable support.
- Guidance: Not selectable; use the wallet's own backup procedure.
- Version interval (min / max): 56f634647d4f75596de20a6259b0cf1933949fdc / 56f634647d4f75596de20a6259b0cf1933949fdc
- Verified on: 2026-09-29
- Historical: false
- Evidence: [monero-polyseed-16-scheme](../catalog/evidence/monero-polyseed-16-scheme.json), [monero-polyseed-vectors](../catalog/evidence/monero-polyseed-vectors.json)
- Evidence claim: Sixteen 11-bit indices\: first is GF\(2048\) checksum, remaining words interleave 150 secret bits, 5 feature bits and 10 birthday bits. Coin domain separation and PBKDF2-HMAC-SHA256 \(10000\) differ from BIP39; modified Spanish/Japanese/Czech orders must be preserved. Optional seed encryption passphrase is not an app password. Reviewed 2026-09-29; response byte SHA-256 51abea48365ac1e4f8fb364be55a69550f81e265d6d96487c418e223789845d8. See docs/research/batches/monero-polyseed.md.
- Evidence claim: Published English/Spanish fixed phrases, random byte inputs, birthday and PBKDF2-input assertions. Projection tests dictionary order, GF checksum and secret/date unpacking. Upstream PBKDF2 is a dummy\: these are NOT derived-key known answers. Reviewed 2026-09-29; response byte SHA-256 3bc51ff2c12c3840e93d5e87a8da47516f806e3d51dc72ea6049f7f439dba4d5. See docs/research/batches/monero-polyseed.md.
- Dictionaries: [polyseed-cs](#dictionary-polyseed-cs), [polyseed-en](#dictionary-polyseed-en), [polyseed-es](#dictionary-polyseed-es), [polyseed-fr](#dictionary-polyseed-fr), [polyseed-it](#dictionary-polyseed-it), [polyseed-ja](#dictionary-polyseed-ja), [polyseed-ko](#dictionary-polyseed-ko), [polyseed-pt](#dictionary-polyseed-pt), [polyseed-zh-hans](#dictionary-polyseed-zh-hans), [polyseed-zh-hant](#dictionary-polyseed-zh-hant)
- Supported lengths: 16
- Position rules: One dictionary per phrase; same vocabulary at each position. Last word is repeated checksum for 25/13; first word is Polyseed checksum for 16. No complete user phrase validation.
- Semantics: Sixteen 11-bit indices\: first is GF\(2048\) checksum, remaining words interleave 150 secret bits, 5 feature bits and 10 birthday bits. Coin domain separation and PBKDF2-HMAC-SHA256 \(10000\) differ from BIP39; modified Spanish/Japanese/Czech orders must be preserved. Optional seed encryption passphrase is not an app password. Documented\: offline tests establish encoding/checksum only; full independent key derivation and exact wallet artifact binding are not established.
- External secret / stored: optional-passphrase / false
- External-secret guidance: Keep any supported seed offset/encryption passphrase separately. Tessaveil never stores it. App login passwords/PINs are not automatically mnemonic secrets; verify exact wallet mode.
- Test vectors: [monero-polyseed-vectors](../catalog/evidence/monero-polyseed-vectors.json)

<a id="scheme-sia-bip39"></a>

### Sia12 — BIP39 encoding, BLAKE2b entropy seed — sia-bip39

- Source record: [sia-bip39](../catalog/schemes/sia-bip39.json)
- Status: documented
- Reason: Evidence is insufficient for selectable support.
- Guidance: Not selectable; use the wallet's own backup procedure.
- Version interval (min / max): 024db888b8bb80b5e54876baaf868c03c9aa0902 / 024db888b8bb80b5e54876baaf868c03c9aa0902
- Verified on: 2026-09-29
- Historical: false
- Evidence: [sia-current-codec](../catalog/evidence/sia-current-codec.json), [sia-web-sdk](../catalog/evidence/sia-web-sdk.json)
- Evidence claim: coreutils v0.24.1 supports only12 words, English BIP39 entropy/checksum encoding; ordered list equals existing BIP39-English. SeedFromPhrase hashes16-byte entropy with BLAKE2b-256, not BIP39 PBKDF2. No extra passphrase; case-sensitive lookup and strings.Fields whitespace.
- Evidence claim: UI SDK routes phrase generation and seed parsing to coreutils/wallet; sdk/go.mod pins v0.24.1. This is the12-word UI route; generic walletd server can track externally derived legacy addresses.
- Dictionaries: [bip39-en](#dictionary-bip39-en)
- Supported lengths: 12
- Position rules: 128 entropy bits and4 SHA256 checksum bits;12 English11-bit indices.
- Semantics: BLAKE2b-256 over entropy yields Sia32-byte seed. Not standard BIP39 sentence PBKDF2; no passphrase.
- External secret / stored: none / false
- External-secret guidance: No mnemonic derivation extension in this exact mode. Local storage/unlock passwords are separate; never enter them into Tessaveil.
- Test vectors: —

<a id="scheme-sia-legacy-28"></a>

### Sia legacy28 — bijective base1626 — sia-legacy-28

- Source record: [sia-legacy-28](../catalog/schemes/sia-legacy-28.json)
- Status: documented
- Reason: Evidence is insufficient for selectable support.
- Guidance: Not selectable; use the wallet's own backup procedure.
- Version interval (min / max): 66e7fc630585887c30033379d2a0a8bf5c618177 / 66e7fc630585887c30033379d2a0a8bf5c618177
- Verified on: 2026-09-29
- Historical: true
- Evidence: [sia-codec](../catalog/evidence/sia-codec.json), [sia-siad-dependency](../catalog/evidence/sia-siad-dependency.json), [sia-siad-seed](../catalog/evidence/sia-siad-seed.json)
- Evidence claim: Legacy codec is a length-preserving bijective base256/base1626 conversion with little-endian digit order, not Monero three-word chunks; per-word NFC and English prefix matching; FromString splits literal spaces.
- Evidence claim: siad pins gitlab.com/NebulousLabs/entropy-mnemonics pseudo-version7532f67e3500, resolved through official GitLab to7532f67e35008b0f36bbebb20d5a6ee8f14a22f5.
- Evidence claim: SeedToString appends first6 bytes of crypto.HashObject\(seed\) to32-byte seed then entropy-mnemonics conversion. StringToSeed requires28/29 English words, exact formatting/lowercase and38 decoded bytes before checksum. Both lengths are one variable-length codec, not two incompatible algorithms.
- Dictionaries: [sia-legacy](#dictionary-sia-legacy)
- Supported lengths: 28
- Position rules: 32-byte seed plus6-byte BLAKE2b checksum becomes28 or29 words under the SAME variable-length codec.
- Semantics: Length is output-dependent; not separate generations, not Monero triplets or BIP39. Exact historical release coverage/recovery remains unverified.
- External secret / stored: none / false
- External-secret guidance: No mnemonic derivation extension in this exact mode. Local storage/unlock passwords are separate; never enter them into Tessaveil.
- Test vectors: —

<a id="scheme-sia-legacy-29"></a>

### Sia legacy29 — bijective base1626 — sia-legacy-29

- Source record: [sia-legacy-29](../catalog/schemes/sia-legacy-29.json)
- Status: documented
- Reason: Evidence is insufficient for selectable support.
- Guidance: Not selectable; use the wallet's own backup procedure.
- Version interval (min / max): 66e7fc630585887c30033379d2a0a8bf5c618177 / 66e7fc630585887c30033379d2a0a8bf5c618177
- Verified on: 2026-09-29
- Historical: true
- Evidence: [sia-codec](../catalog/evidence/sia-codec.json), [sia-siad-dependency](../catalog/evidence/sia-siad-dependency.json), [sia-siad-seed](../catalog/evidence/sia-siad-seed.json)
- Evidence claim: Legacy codec is a length-preserving bijective base256/base1626 conversion with little-endian digit order, not Monero three-word chunks; per-word NFC and English prefix matching; FromString splits literal spaces.
- Evidence claim: siad pins gitlab.com/NebulousLabs/entropy-mnemonics pseudo-version7532f67e3500, resolved through official GitLab to7532f67e35008b0f36bbebb20d5a6ee8f14a22f5.
- Evidence claim: SeedToString appends first6 bytes of crypto.HashObject\(seed\) to32-byte seed then entropy-mnemonics conversion. StringToSeed requires28/29 English words, exact formatting/lowercase and38 decoded bytes before checksum. Both lengths are one variable-length codec, not two incompatible algorithms.
- Dictionaries: [sia-legacy](#dictionary-sia-legacy)
- Supported lengths: 29
- Position rules: 32-byte seed plus6-byte BLAKE2b checksum becomes28 or29 words under the SAME variable-length codec.
- Semantics: Length is output-dependent; not separate generations, not Monero triplets or BIP39. Exact historical release coverage/recovery remains unverified.
- External secret / stored: none / false
- External-secret guidance: No mnemonic derivation extension in this exact mode. Local storage/unlock passwords are separate; never enter them into Tessaveil.
- Test vectors: —

<a id="scheme-slip39-share"></a>

### SLIP-39 — individual share — slip39-share

- Source record: [slip39-share](../catalog/schemes/slip39-share.json)
- Status: documented
- Reason: Evidence is insufficient for selectable support.
- Guidance: Not selectable; use the wallet's own backup procedure.
- Version interval (min / max): 570ed55b7fde158f1116be34fc2faa35dada5912 / 570ed55b7fde158f1116be34fc2faa35dada5912
- Verified on: 2026-09-29
- Historical: false
- Evidence: [slip39-rules](../catalog/evidence/slip39-rules.json), [slip39-spec](../catalog/evidence/slip39-spec.json), [slip39-vectors](../catalog/evidence/slip39-vectors.json)
- Evidence claim: Big-endian 10-bit indices; 4 metadata words, padded share value, 3 checksum words; threshold/count fields are encoded minus one. All positions use the same list. Source-native input lowercases and splits whitespace, without Unicode normalization. See docs/research/batches/slip39-algorand-cardano.md. Retrieved byte SHA-256 3ee6f46415ba34dd8c1bc5f92601b17151854a35425e098d1de857ca714205c5.
- Evidence claim: Format of the share mnemonic, Two-level scheme, Checksum and Passphrase sections define 20/33 words for 128/256 bits; 15-bit ID, extendable flag, exponent, group/member fields and three RS1024 words. Standard allows other lengths; catalogue scope only 20/33. Tessaveil stores neither complete shares nor thresholds as recovered secrets and never combines/reconstructs shares. See docs/research/batches/slip39-algorand-cardano.md. Retrieved byte SHA-256 7b4269f66f10f03ac685ea7c76f742bfbf56211af1af29339eadef9acba1f856.
- Evidence claim: Public cases 1, 4, 17, 20, 42, 44 projected into indices/fingerprints; tests check individual-share metadata/padding/RS1024 only. No combining, master-secret recovery, decryption or wallet derivation is executed. See docs/research/batches/slip39-algorand-cardano.md. Retrieved byte SHA-256 13ebecebdd869dd2bc2cdf69e7ce3a158cf106cac76c39d17682b1c6cdabbdc4.
- Dictionaries: [slip39-en](#dictionary-slip39-en)
- Supported lengths: 20, 33
- Position rules: Words1-2\:15-bit identifier, extendable flag, 4-bit iteration exponent. Words3-4\:4-bit group index, group threshold-1, group count-1, member index, member threshold-1.; Words5 through last-3 encode left-zero-padded share bytes; last3 encode RS1024 checksum. Same list all positions. Standard 128/256 bits gives 20/33 words.
- Semantics: Individual share profile, never a whole reconstructed wallet secret. Tessaveil never combines/reconstructs shares, derives keys or validates a complete user share. Optional passphrase is separate. Documented\: vectors cover share encoding/metadata only, not wallet recovery.
- External secret / stored: optional-passphrase / false
- External-secret guidance: Any supported mnemonic passphrase stays outside Tessaveil; wallet login/spending passwords are distinct. Paper27 already includes its nine password words; no extra secret is inferred.
- Test vectors: [slip39-vectors](../catalog/evidence/slip39-vectors.json)

<a id="scheme-slip39-share-20"></a>

### SLIP-39 — individual share \(20-word Suite mode\) — slip39-share-20

- Source record: [slip39-share-20](../catalog/schemes/slip39-share-20.json)
- Status: documented
- Reason: Evidence is insufficient for selectable support.
- Guidance: Not selectable; use the wallet's own backup procedure.
- Version interval (min / max): 570ed55b7fde158f1116be34fc2faa35dada5912 / 570ed55b7fde158f1116be34fc2faa35dada5912
- Verified on: 2026-09-29
- Historical: false
- Evidence: [slip39-rules](../catalog/evidence/slip39-rules.json), [slip39-spec](../catalog/evidence/slip39-spec.json), [slip39-vectors](../catalog/evidence/slip39-vectors.json)
- Evidence claim: Big-endian 10-bit indices; 4 metadata words, padded share value, 3 checksum words; threshold/count fields are encoded minus one. All positions use the same list. Source-native input lowercases and splits whitespace, without Unicode normalization. See docs/research/batches/slip39-algorand-cardano.md. Retrieved byte SHA-256 3ee6f46415ba34dd8c1bc5f92601b17151854a35425e098d1de857ca714205c5.
- Evidence claim: Format of the share mnemonic, Two-level scheme, Checksum and Passphrase sections define 20/33 words for 128/256 bits; 15-bit ID, extendable flag, exponent, group/member fields and three RS1024 words. Standard allows other lengths; catalogue scope only 20/33. Tessaveil stores neither complete shares nor thresholds as recovered secrets and never combines/reconstructs shares. See docs/research/batches/slip39-algorand-cardano.md. Retrieved byte SHA-256 7b4269f66f10f03ac685ea7c76f742bfbf56211af1af29339eadef9acba1f856.
- Evidence claim: Public cases 1, 4, 17, 20, 42, 44 projected into indices/fingerprints; tests check individual-share metadata/padding/RS1024 only. No combining, master-secret recovery, decryption or wallet derivation is executed. See docs/research/batches/slip39-algorand-cardano.md. Retrieved byte SHA-256 13ebecebdd869dd2bc2cdf69e7ce3a158cf106cac76c39d17682b1c6cdabbdc4.
- Dictionaries: [slip39-en](#dictionary-slip39-en)
- Supported lengths: 20
- Position rules: Words1-2\:15-bit identifier, extendable flag, 4-bit iteration exponent. Words3-4\:4-bit group index, group threshold-1, group count-1, member index, member threshold-1.; Words5 through last-3 encode left-zero-padded share bytes; last3 encode RS1024 checksum. Same list all positions. Standard 128/256 bits gives 20/33 words.
- Semantics: Individual share profile, never a whole reconstructed wallet secret. Tessaveil never combines/reconstructs shares, derives keys or validates a complete user share. Optional passphrase is separate. Documented\: vectors cover share encoding/metadata only, not wallet recovery.
- External secret / stored: optional-passphrase / false
- External-secret guidance: Any supported mnemonic passphrase stays outside Tessaveil; wallet login/spending passwords are distinct. Paper27 already includes its nine password words; no extra secret is inferred.
- Test vectors: [slip39-vectors](../catalog/evidence/slip39-vectors.json)

<a id="scheme-substrate-bip39"></a>

### Substrate — English BIP39 entropy semantics — substrate-bip39

- Source record: [substrate-bip39](../catalog/schemes/substrate-bip39.json)
- Status: documented
- Reason: Evidence is insufficient for selectable support.
- Guidance: Not selectable; use the wallet's own backup procedure.
- Version interval (min / max): ceb4fe5a3c7ac91da2e272037797ebecb56aa177 / ceb4fe5a3c7ac91da2e272037797ebecb56aa177
- Verified on: 2026-09-29
- Historical: false
- Evidence: [substrate-entropy](../catalog/evidence/substrate-entropy.json), [substrate-vector-license](../catalog/evidence/substrate-vector-license.json), [substrate-vectors](../catalog/evidence/substrate-vectors.json)
- Evidence claim: substrate-bip39 0.4.6 uses recovered BIP39 entropy bytes as PBKDF2-HMAC-SHA512 password, mnemonic\+password salt, 2048 rounds, 64-byte result; mini-secret first32. Not standard sentence-based BIP39 seed derivation. Function itself does not normalize passwords; consumers must be distinguished.
- Evidence claim: Apache-2.0 public test projections modified and attributed to Copyright2019-2020 Parity Technologies \(UK\) Ltd. Complete Apache license already retained; no library bundled.
- Evidence claim: Published VECTORS with Substrate password projected to entropy, BIP39-English indices and expected seed SHA256. Offline reproduction proves only this primitive, not a wallet/network/derivation path.
- Dictionaries: [bip39-en](#dictionary-bip39-en)
- Supported lengths: 12, 15, 18, 21, 24
- Position rules: BIP39 word encoding/checksum recovers16/20/24/28/32 entropy bytes. PBKDF2 uses those bytes, not the mnemonic sentence.
- Semantics: Polkadot/Kusama source family; primitive evidence is not wallet/path/address compatibility. sr25519, ed25519, ecdsa, Ethereum and hardware modes must not be conflated. Raw primitive does not normalize password; consumer behavior varies.
- External secret / stored: optional-passphrase / false
- External-secret guidance: Any supported recovery passphrase and derivation path stay outside Tessaveil. Local encryption/unlock passwords are distinct.
- Test vectors: [substrate-vectors](../catalog/evidence/substrate-vectors.json)

<a id="scheme-ton-multichain-bip39"></a>

### TON multichain — BIP39 12/24 words — ton-multichain-bip39

- Source record: [ton-multichain-bip39](../catalog/schemes/ton-multichain-bip39.json)
- Status: documented
- Reason: Evidence is insufficient for selectable support.
- Guidance: Not selectable; use the wallet's own backup procedure.
- Version interval (min / max): fe8a154e4dad9f5c0bf7240df278cb50ec6cd908 / fe8a154e4dad9f5c0bf7240df278cb50ec6cd908
- Verified on: 2026-09-29
- Historical: false
- Evidence: [bip39-spec](../catalog/evidence/bip39-spec.json), [bip39-vectors](../catalog/evidence/bip39-vectors.json), [ton-my-derive](../catalog/evidence/ton-my-derive.json), [ton-my-path](../catalog/evidence/ton-my-path.json), [ton-tep3](../catalog/evidence/ton-tep3.json)
- Evidence claim: Bitcoin BIP39 specifies 2048 indexed words, 12/15/18/21/24 lengths and UTF-8 NFKD for words, sentence and optional passphrase; equal vocabulary does not establish TON derivation. Reviewed 2026-09-29; byte SHA-256 afcbcbed36fe9eb734bd607398a8c124683ded2a75c3830e1b16c47b043a9134. See docs/research/batches/bip39-ton.md.
- Evidence claim: Trezor's public vectors.json supplies 24 independent entropy/mnemonic/seed known answers per language for all ten lists, with passphrase TREZOR. Offline test reconstructs words from entropy, checks published normalized sentence fingerprints and PBKDF2 seed. Public, non-funded data only; fixture projection contains no user phrase. Reviewed 2026-09-29; byte SHA-256 fa3b937b7cff9c9b8ecd3aa011faeb8d6dd67993174b72326e83f4de8fdb30f8. See docs/research/batches/bip39-ton.md.
- Evidence claim: TON auth.ts generates 24 native words, rerolling BIP39 ambiguity; explicit bip39 accounts use BIP39 seed and Ed25519 path derivation. Stored native words use TON default seed without implicit normalization. Reviewed 2026-09-29; byte SHA-256 35286bbfb6c1d6022569738a054dd32d060b1fc48c6a1143dab1df705a218211. See docs/research/batches/bip39-ton.md.
- Evidence claim: TON\_BIP39\_PATH is hardened path components 44, 607, account index; slot zero is the TEP-3 main-account path. Reviewed 2026-09-29; byte SHA-256 5d799c9d1ec5fc23bf85245a477772a744cbf19a0ef7bef0aa8ecf9c1bd1c670. See docs/research/batches/bip39-ton.md.
- Evidence claim: TEP-3 sections 2-4 and 8-12 distinguish native 24-word TON and multichain BIP39 12/24-word modes sharing the English vocabulary, with TON path hardened path components 44, 607, 0 for the latter. It recommends new 12-word multichain or native 24-word generation, not new 24-word multichain. Import may encounter both. TEP is guidance, not proof of any product release transition; Pro MAM is a separate derivation. Reviewed 2026-09-29; byte SHA-256 4049020b927f72f7187b04f3e61e27f478caf1669fd528f21b815417b428be4b. See docs/research/batches/bip39-ton.md.
- Dictionaries: [bip39-en](#dictionary-bip39-en)
- Supported lengths: 12, 24
- Position rules: The same dictionary is eligible at every word position. Phrase checksum or seed validity is never evaluated by Tessaveil.
- Semantics: TEP-3 BIP39 then SLIP-0010 Ed25519 at hardened path components 44, 607, 0, with indexed subwallet paths. 12 and 24 are import/profile lengths; TEP discourages new 24-word multichain generation. BIP39 public vectors verify only its seed stage. An independent published full TON derivation-path known answer has not been reproduced in this batch, so this scheme remains documented and not selectable.
- External secret / stored: optional-passphrase / false
- External-secret guidance: A scheme passphrase is external and never stored by Tessaveil. A wallet PIN or application password is not proof of a mnemonic passphrase; verify support in the exact source wallet.
- Test vectors: [bip39-vectors](../catalog/evidence/bip39-vectors.json)

<a id="scheme-ton-native"></a>

### TON native — 24 words — ton-native

- Source record: [ton-native](../catalog/schemes/ton-native.json)
- Status: verified
- Reason: Verified research record; not a release or security guarantee.
- Version interval (min / max): fe8a154e4dad9f5c0bf7240df278cb50ec6cd908 / fe8a154e4dad9f5c0bf7240df278cb50ec6cd908
- Verified on: 2026-09-29
- Historical: false
- Evidence: [ton-native-license](../catalog/evidence/ton-native-license.json), [ton-native-source](../catalog/evidence/ton-native-source.json), [ton-native-vectors](../catalog/evidence/ton-native-vectors.json), [ton-native-wordlist](../catalog/evidence/ton-native-wordlist.json), [ton-tep3](../catalog/evidence/ton-tep3.json)
- Evidence claim: The actual MIT license permits the five public vector projections with retained Copyright \(c\) 2021-2023 Whales Corp. and permission notice in THIRD\_PARTY\_NOTICES. No TON implementation code or wallet binaries are bundled. Reviewed 2026-09-29; byte SHA-256 33578b9ea1522de18164cf1d1ef8e52f50d748ae17c7d38b4fa5e6f50207f8eb. See docs/research/batches/bip39-ton.md.
- Evidence claim: TON crypto mnemonic.ts\: mnemonicNew defaults to 24; entropy is HMAC-SHA512\(key=space-joined words, message=optional password\), then PBKDF2-HMAC-SHA512 with TON default seed salt and 100000 iterations; first 32 bytes seed Ed25519. Basic-seed check uses TON seed version and 390 iterations. Native lowercase/trim behavior is not a universal BIP39 NFKD rule. Reviewed 2026-09-29; byte SHA-256 79518c5f905daaa4e64f09454e8a82dbb1c8d1b310305ef84b25e85b2c77126a. See docs/research/batches/bip39-ton.md.
- Evidence claim: Five public mnemonic.spec.ts vectors independently provide 24 English words and expected Ed25519 secretKey. Fixture retains zero-based dictionary indices and the first 32 bytes of each published secretKey \(seed\). Offline standard-library HMAC/PBKDF2 checks those published seeds and the basic-seed predicate; it does not test Ed25519 public keys or addresses. Reviewed 2026-09-29; byte SHA-256 ba6936664624168caf454df777b4ef8354c034c49b121a493c44237e4880cd83. See docs/research/batches/bip39-ton.md.
- Evidence claim: TON crypto's wordlist.ts contains exactly the same 2048 English tokens in the same order as the pinned BIP39 English list. Compared by extracting its single-quoted alphabetic tokens; only the unchanged BIP39 text file is bundled. Source byte SHA-256 2bc9a19c24279d659c4d02e08f9381af16cd62bdbb5103ce1815db4a7861c9db. Reviewed 2026-09-29; see docs/research/batches/bip39-ton.md.
- Evidence claim: TEP-3 sections 2-4 and 8-12 distinguish native 24-word TON and multichain BIP39 12/24-word modes sharing the English vocabulary, with TON path hardened path components 44, 607, 0 for the latter. It recommends new 12-word multichain or native 24-word generation, not new 24-word multichain. Import may encounter both. TEP is guidance, not proof of any product release transition; Pro MAM is a separate derivation. Reviewed 2026-09-29; byte SHA-256 4049020b927f72f7187b04f3e61e27f478caf1669fd528f21b815417b428be4b. See docs/research/batches/bip39-ton.md.
- Dictionaries: [bip39-en](#dictionary-bip39-en)
- Supported lengths: 24
- Position rules: The same dictionary is eligible at every word position. Phrase checksum or seed validity is never evaluated by Tessaveil.
- Semantics: English BIP39 vocabulary only; TON HMAC/PBKDF2 seed and seed-version constraints differ from BIP39 checksum and seed derivation. Native 24 words are not automatically BIP39-compatible. V3/V4/V5 are smart-contract versions, not mnemonic scheme versions. Tests cover public seed derivation only, not addresses.
- External secret / stored: optional-passphrase / false
- External-secret guidance: A scheme passphrase is external and never stored by Tessaveil. A wallet PIN or application password is not proof of a mnemonic passphrase; verify support in the exact source wallet.
- Test vectors: [ton-native-vectors](../catalog/evidence/ton-native-vectors.json)

<a id="scheme-zano-legacy-24"></a>

### Zano historical24 — rejected by inspected current core — zano-legacy-24

- Source record: [zano-legacy-24](../catalog/schemes/zano-legacy-24.json)
- Status: blocked
- Reason: Support is blocked; see evidence and license decisions below.
- Guidance: Not selectable; use the wallet's own backup procedure.
- Version interval (min / max): e55c8ec47b76ed809162a958cf4600e03256a96a / e55c8ec47b76ed809162a958cf4600e03256a96a
- Verified on: 2026-09-29
- Historical: true
- Evidence: [zano-codec](../catalog/evidence/zano-codec.json), [zano-history-vector](../catalog/evidence/zano-history-vector.json), [zano-modes](../catalog/evidence/zano-modes.json)
- Evidence claim: Exact 1626 English indices; eight native little-endian 32-bit groups become 24 words in eight dependent modulo-1626 triplets. List equals Electrum v1 tuple in order, not Monero current English or BIP39. Case-sensitive membership; no lowercase or Unicode normalization is applied by this codec.
- Evidence claim: Pinned public wallet\_seed\_entries explicitly marks legacy24 invalid and old25 valid; includes26 checksum cases. Reviewed as upstream tests only, not executed recovery or evidence of which old release generated24.
- Evidence claim: get\_seed\_phrase emits 24 data words, timestamp/password-flag word25 and checksum/auditable word26. restore\_from\_seed\_phrase accepts25/26 and rejects24 at this exact commit. Seed password encrypts binary seed with legacy ChaCha; it is not BIP39 extension.
- Dictionaries: [zano-en](#dictionary-zano-en)
- Supported lengths: 24
- Position rules: Historical24 has no timestamp/checksum words. Inspected restore explicitly rejects24.
- Semantics: Historical generating release and password behavior unresolved; length is research identity, not accepted current input.
- External secret / stored: other / false
- External-secret guidance: Exact original seed password and mode are required for recovery when used; never store the secret in Tessaveil.
- Test vectors: [zano-history-vector](../catalog/evidence/zano-history-vector.json)

<a id="scheme-zano-legacy-25"></a>

### Zano historical25 import — zano-legacy-25

- Source record: [zano-legacy-25](../catalog/schemes/zano-legacy-25.json)
- Status: blocked
- Reason: Support is blocked; see evidence and license decisions below.
- Guidance: Not selectable; use the wallet's own backup procedure.
- Version interval (min / max): e55c8ec47b76ed809162a958cf4600e03256a96a / e55c8ec47b76ed809162a958cf4600e03256a96a
- Verified on: 2026-09-29
- Historical: true
- Evidence: [zano-history-vector](../catalog/evidence/zano-history-vector.json), [zano-modes](../catalog/evidence/zano-modes.json), [zano-timestamp-password](../catalog/evidence/zano-timestamp-password.json)
- Evidence claim: Pinned public wallet\_seed\_entries explicitly marks legacy24 invalid and old25 valid; includes26 checksum cases. Reviewed as upstream tests only, not executed recovery or evidence of which old release generated24.
- Evidence claim: get\_seed\_phrase emits 24 data words, timestamp/password-flag word25 and checksum/auditable word26. restore\_from\_seed\_phrase accepts25/26 and rejects24 at this exact commit. Seed password encrypts binary seed with legacy ChaCha; it is not BIP39 extension.
- Evidence claim: Timestamp is quantized with WALLET\_BRAIN\_DATE\_QUANTUM; word25 carries password-use flag. validate\_password uses a restricted ASCII regex; no Unicode NFKD or BIP39 salt is applied.
- Dictionaries: [zano-en](#dictionary-zano-en)
- Supported lengths: 25
- Position rules: Words1..24 binary data; word25 timestamp/password flag; no word26 checksum.
- Semantics: Accepted by inspected current core; original historical generation boundary not established. Not Monero25.
- External secret / stored: optional-passphrase / false
- External-secret guidance: Exact original seed password and mode are required for recovery when used; never store the secret in Tessaveil.
- Test vectors: [zano-history-vector](../catalog/evidence/zano-history-vector.json)

<a id="scheme-zano-modern"></a>

### Zano native26 — zano-modern

- Source record: [zano-modern](../catalog/schemes/zano-modern.json)
- Status: blocked
- Reason: Support is blocked; see evidence and license decisions below.
- Guidance: Not selectable; use the wallet's own backup procedure.
- Version interval (min / max): e55c8ec47b76ed809162a958cf4600e03256a96a / e55c8ec47b76ed809162a958cf4600e03256a96a
- Verified on: 2026-09-29
- Historical: false
- Evidence: [zano-codec](../catalog/evidence/zano-codec.json), [zano-history-vector](../catalog/evidence/zano-history-vector.json), [zano-modes](../catalog/evidence/zano-modes.json), [zano-timestamp-password](../catalog/evidence/zano-timestamp-password.json)
- Evidence claim: Exact 1626 English indices; eight native little-endian 32-bit groups become 24 words in eight dependent modulo-1626 triplets. List equals Electrum v1 tuple in order, not Monero current English or BIP39. Case-sensitive membership; no lowercase or Unicode normalization is applied by this codec.
- Evidence claim: Pinned public wallet\_seed\_entries explicitly marks legacy24 invalid and old25 valid; includes26 checksum cases. Reviewed as upstream tests only, not executed recovery or evidence of which old release generated24.
- Evidence claim: get\_seed\_phrase emits 24 data words, timestamp/password-flag word25 and checksum/auditable word26. restore\_from\_seed\_phrase accepts25/26 and rejects24 at this exact commit. Seed password encrypts binary seed with legacy ChaCha; it is not BIP39 extension.
- Evidence claim: Timestamp is quantized with WALLET\_BRAIN\_DATE\_QUANTUM; word25 carries password-use flag. validate\_password uses a restricted ASCII regex; no Unicode NFKD or BIP39 salt is applied.
- Dictionaries: [zano-en](#dictionary-zano-en)
- Supported lengths: 26
- Position rules: Words1..24 encode32 bytes; word25 is timestamp/password flag; word26 is checksum/auditable flag.
- Semantics: Native Zano; not BIP39, Monero25 or Cake BIP39. Dictionary provenance blocks selection; no local recovery test.
- External secret / stored: optional-passphrase / false
- External-secret guidance: Exact original seed password and mode are required for recovery when used; never store the secret in Tessaveil.
- Test vectors: [zano-history-vector](../catalog/evidence/zano-history-vector.json)

<a id="scheme-zcash-bip39"></a>

### Zcash English24 mnemonic mode — zcash-bip39

- Source record: [zcash-bip39](../catalog/schemes/zcash-bip39.json)
- Status: documented
- Reason: Evidence is insufficient for selectable support.
- Guidance: Not selectable; use the wallet's own backup procedure.
- Version interval (min / max): f9dcd4d31439feb813c95ac2516814421f5b04df / f9dcd4d31439feb813c95ac2516814421f5b04df
- Verified on: 2026-09-29
- Historical: false
- Evidence: [zcash-bip0039](../catalog/evidence/zcash-bip0039.json), [zcash-bip0039-vector](../catalog/evidence/zcash-bip0039-vector.json), [zcash-create](../catalog/evidence/zcash-create.json), [zcash-ffi](../catalog/evidence/zcash-ffi.json), [zcash-vector-license](../catalog/evidence/zcash-vector-license.json), [zcash-zallet-create](../catalog/evidence/zcash-zallet-create.json), [zcash-zallet-empty](../catalog/evidence/zcash-zallet-empty.json)
- Evidence claim: Zallet Cargo.lock pins bip0039 0.12.0; downloaded crate SHA256 matches568b6890865156d9043af490d4c4081c385dd68ea10acd6ca15733d511e6b51c and vcs commit. NFKD PBKDF2-HMAC-SHA512/2048, salt mnemonic\+passphrase. English ordered list equals existing BIP39-English. zcashd dependency binding is not inferred from Zallet's lock.
- Evidence claim: Published to\_seed\(""\) doc-test projected to12 word indices plus literal expected64-byte seed. Primitive corroboration only, not24-word Zallet recovery.
- Evidence claim: zcashd mnemonic source constructs BIP39 phrase from32-byte entropy, checks Zcash account derivability; FromLegacySeed creates a NEW mnemonic seed with nonce adjustment, not an identity-preserving conversion of every old key.
- Evidence claim: ZIP339 interface selects BIP39 languages and explicitly derives with empty passphrase. This batch is English24 only; standalone keys and legacy raw HD seeds are separate.
- Evidence claim: MIT branch chosen for modified public doc-test projection, Copyright2020 Qinxuan Chen; full notice retained. Codex2026-09-29 data redistribution allowed/local SignPath compatible. No Rust dependency or wallet binary bundled.
- Evidence claim: generate-mnemonic chooses Count\:\:Words24 and English from32 random bytes; encrypted storage and backup confirmation are separate. Source-only beta scope, not tested released wallet.
- Evidence claim: Keystore reconstructs BIP39 mnemonic.to\_seed\(""\) and separately retains legacy non-mnemonic HD seeds. age identity passphrase encrypts storage and is not a BIP39 derivation passphrase.
- Dictionaries: [bip39-en](#dictionary-bip39-en)
- Supported lengths: 24
- Position rules: 256-bit entropy plus8 checksum bits;24 English words. Account/network/ZIP32 context remains essential.
- Semantics: Exact English mnemonic mode with empty BIP39 extension. Imported standalone keys and old HD seed bytes are not covered.
- External secret / stored: none / false
- External-secret guidance: No mnemonic derivation extension in this exact mode. Local storage/unlock passwords are separate; never enter them into Tessaveil.
- Test vectors: [zcash-bip0039-vector](../catalog/evidence/zcash-bip0039-vector.json)

<a id="scheme-zcash-non-mnemonic"></a>

### Zcash standalone keys / raw legacy HD seed — no word table — zcash-non-mnemonic

- Source record: [zcash-non-mnemonic](../catalog/schemes/zcash-non-mnemonic.json)
- Status: no-mnemonic-confirmed
- Reason: This mode does not expose a supported mnemonic backup.
- Guidance: Not selectable; use the wallet's own backup procedure.
- Version interval (min / max): 558f686599586f55def3db86955d74d3be44605e / 558f686599586f55def3db86955d74d3be44605e
- Verified on: 2026-09-29
- Historical: false
- Evidence: [zcash-standalone](../catalog/evidence/zcash-standalone.json), [zcash-zallet-empty](../catalog/evidence/zcash-zallet-empty.json), [zcash-zallet-export](../catalog/evidence/zcash-zallet-export.json)
- Evidence claim: dumpprivkey and z\_exportkey export standalone transparent or shielded private-key encodings. These are not mnemonic word-table profiles; mnemonic backup cannot be assumed to cover imported keys.
- Evidence claim: Keystore reconstructs BIP39 mnemonic.to\_seed\(""\) and separately retains legacy non-mnemonic HD seeds. age identity passphrase encrypts storage and is not a BIP39 derivation passphrase.
- Evidence claim: Official book distinguishes mnemonic accounts from z\_importkey and standalone migrated keys; encrypted mnemonic export also requires its age identity. Exported phrase alone does not cover all wallet material.
- Dictionaries: —
- Supported lengths: —
- Position rules: Not applicable\: non-mnemonic material has no word positions or candidate table.
- Semantics: Non-mnemonic key material requires native wallet backup/export and any encryption identity. No vocabulary, word count, table, or universal mnemonic conversion.
- External secret / stored: other / false
- External-secret guidance: Exact original seed password and mode are required for recovery when used; never store the secret in Tessaveil.
- Test vectors: —

## Dictionaries (one entry per ID)

<a id="dictionary-bip39-cs"></a>

### BIP39 — Czech — bip39-cs

- Source record: [bip39-cs](../catalog/dictionaries/bip39-cs.json)
- Status: verified
- Reason: Verified research record; not a release or security guarantee.
- Version interval (min / max): 3a10b5b5f0a7586df8928d580a3009744ebb2079 / 3a10b5b5f0a7586df8928d580a3009744ebb2079
- Verified on: 2026-09-29
- Historical: false
- Evidence: [bip39-guidance](../catalog/evidence/bip39-guidance.json), [bip39-license](../catalog/evidence/bip39-license.json), [bip39-osi-mit](../catalog/evidence/bip39-osi-mit.json), [bip39-signpath](../catalog/evidence/bip39-signpath.json), [bip39-spec](../catalog/evidence/bip39-spec.json), [bip39-vectors](../catalog/evidence/bip39-vectors.json)
- Evidence claim: BIP39 links exactly ten language lists and language-specific guidance; Japanese generation uses ideographic spaces, which NFKD converts to ASCII spaces. Original source line order and bytes are preserved. Reviewed 2026-09-29; byte SHA-256 363a51bc4748d95541bb156e0439de7b51f28b260433c09874e5891dd3b0f883. See docs/research/batches/bip39-ton.md.
- Evidence claim: Local license review by Codex\: the actual MIT license of the BIP39 reference implementation permits redistribution with copyright and permission notice. Every bundled bitcoin/bips list is byte-identical to src/mnemonic/wordlist at this licensed reference revision; vectors.json is in the same repository. No directory-specific exception was found. Notices preserve the license and attribution. repository\_redistribution=allowed for these exact bytes and public test projections, not arbitrary BIPs material. Reviewed 2026-09-29; byte SHA-256 d5e3c7c62a84e80073201e2f6e5130e9e6804fa05f8ac4f8b26a13c7d3969697. See docs/research/batches/bip39-ton.md.
- Evidence claim: OSI identifies MIT as an approved open-source license; this corroborates the local component assessment, while the pinned reference repository license supplies the actual permission. Reviewed 2026-09-29; byte SHA-256 004c79db0a335488afc87600d89f447dce7fb4d24d510af15ed4381a24be848c. See docs/research/batches/bip39-ton.md.
- Evidence claim: Local component review by Codex\: the exact MIT-licensed lists are source data with no executable dependencies or proprietary restrictions. Together with retained MIT notices and OSI approval this supports signpath\_compatible=compatible for this payload only. SignPath terms require OSS components; this is not Foundation acceptance or project release/signing approval. Reviewed 2026-09-29; byte SHA-256 6610cf889bbe0dc7533abaa310bc7a5cc9a61ae6c2ce0798a08109c925b46c51. See docs/research/batches/bip39-ton.md.
- Evidence claim: Bitcoin BIP39 specifies 2048 indexed words, 12/15/18/21/24 lengths and UTF-8 NFKD for words, sentence and optional passphrase; equal vocabulary does not establish TON derivation. Reviewed 2026-09-29; byte SHA-256 afcbcbed36fe9eb734bd607398a8c124683ded2a75c3830e1b16c47b043a9134. See docs/research/batches/bip39-ton.md.
- Evidence claim: Trezor's public vectors.json supplies 24 independent entropy/mnemonic/seed known answers per language for all ten lists, with passphrase TREZOR. Offline test reconstructs words from entropy, checks published normalized sentence fingerprints and PBKDF2 seed. Public, non-funded data only; fixture projection contains no user phrase. Reviewed 2026-09-29; byte SHA-256 fa3b937b7cff9c9b8ecd3aa011faeb8d6dd67993174b72326e83f4de8fdb30f8. See docs/research/batches/bip39-ton.md.
- Language: cs
- Script: Latn
- Encoding: UTF-8
- Normalization: NFKD
- Word count: 2048
- SHA-256: 7e80e161c3e93d9554c2efb78d4e3cebf8fc727e9c52e03b83b94406bdcc95fc
- Order rule: Exact upstream source line order; zero-based 11-bit indices 0 through 2047. UTF-8 LF bytes and final newline preserved without transformation.
- Position rules: The same dictionary is eligible at every word position. Phrase checksum or seed validity is never evaluated by Tessaveil.
- Source revision: 3a10b5b5f0a7586df8928d580a3009744ebb2079
- License: MIT
- Attribution: BIP39 authors Marek Palatinus, Pavol Rusnak, Aaron Voisine, Sean Bowe and word-list contributors. Byte-identical reference copy\: Copyright \(c\) 2013-2016 Pavol Rusnak. Full license and language credits in THIRD\_PARTY\_NOTICES.
- Repository redistribution: allowed
- SignPath compatibility: compatible
- License evidence: [bip39-license](../catalog/evidence/bip39-license.json), [bip39-osi-mit](../catalog/evidence/bip39-osi-mit.json), [bip39-signpath](../catalog/evidence/bip39-signpath.json)
- Test vectors: [bip39-vectors](../catalog/evidence/bip39-vectors.json)

<a id="dictionary-bip39-en"></a>

### BIP39 — English — bip39-en

- Source record: [bip39-en](../catalog/dictionaries/bip39-en.json)
- Status: verified
- Reason: Verified research record; not a release or security guarantee.
- Version interval (min / max): 3a10b5b5f0a7586df8928d580a3009744ebb2079 / 3a10b5b5f0a7586df8928d580a3009744ebb2079
- Verified on: 2026-09-29
- Historical: false
- Evidence: [bip39-guidance](../catalog/evidence/bip39-guidance.json), [bip39-license](../catalog/evidence/bip39-license.json), [bip39-osi-mit](../catalog/evidence/bip39-osi-mit.json), [bip39-signpath](../catalog/evidence/bip39-signpath.json), [bip39-spec](../catalog/evidence/bip39-spec.json), [bip39-vectors](../catalog/evidence/bip39-vectors.json)
- Evidence claim: BIP39 links exactly ten language lists and language-specific guidance; Japanese generation uses ideographic spaces, which NFKD converts to ASCII spaces. Original source line order and bytes are preserved. Reviewed 2026-09-29; byte SHA-256 363a51bc4748d95541bb156e0439de7b51f28b260433c09874e5891dd3b0f883. See docs/research/batches/bip39-ton.md.
- Evidence claim: Local license review by Codex\: the actual MIT license of the BIP39 reference implementation permits redistribution with copyright and permission notice. Every bundled bitcoin/bips list is byte-identical to src/mnemonic/wordlist at this licensed reference revision; vectors.json is in the same repository. No directory-specific exception was found. Notices preserve the license and attribution. repository\_redistribution=allowed for these exact bytes and public test projections, not arbitrary BIPs material. Reviewed 2026-09-29; byte SHA-256 d5e3c7c62a84e80073201e2f6e5130e9e6804fa05f8ac4f8b26a13c7d3969697. See docs/research/batches/bip39-ton.md.
- Evidence claim: OSI identifies MIT as an approved open-source license; this corroborates the local component assessment, while the pinned reference repository license supplies the actual permission. Reviewed 2026-09-29; byte SHA-256 004c79db0a335488afc87600d89f447dce7fb4d24d510af15ed4381a24be848c. See docs/research/batches/bip39-ton.md.
- Evidence claim: Local component review by Codex\: the exact MIT-licensed lists are source data with no executable dependencies or proprietary restrictions. Together with retained MIT notices and OSI approval this supports signpath\_compatible=compatible for this payload only. SignPath terms require OSS components; this is not Foundation acceptance or project release/signing approval. Reviewed 2026-09-29; byte SHA-256 6610cf889bbe0dc7533abaa310bc7a5cc9a61ae6c2ce0798a08109c925b46c51. See docs/research/batches/bip39-ton.md.
- Evidence claim: Bitcoin BIP39 specifies 2048 indexed words, 12/15/18/21/24 lengths and UTF-8 NFKD for words, sentence and optional passphrase; equal vocabulary does not establish TON derivation. Reviewed 2026-09-29; byte SHA-256 afcbcbed36fe9eb734bd607398a8c124683ded2a75c3830e1b16c47b043a9134. See docs/research/batches/bip39-ton.md.
- Evidence claim: Trezor's public vectors.json supplies 24 independent entropy/mnemonic/seed known answers per language for all ten lists, with passphrase TREZOR. Offline test reconstructs words from entropy, checks published normalized sentence fingerprints and PBKDF2 seed. Public, non-funded data only; fixture projection contains no user phrase. Reviewed 2026-09-29; byte SHA-256 fa3b937b7cff9c9b8ecd3aa011faeb8d6dd67993174b72326e83f4de8fdb30f8. See docs/research/batches/bip39-ton.md.
- Language: en
- Script: Latn
- Encoding: UTF-8
- Normalization: NFKD
- Word count: 2048
- SHA-256: 2f5eed53a4727b4bf8880d8f3f199efc90e58503646d9ff8eff3a2ed3b24dbda
- Order rule: Exact upstream source line order; zero-based 11-bit indices 0 through 2047. UTF-8 LF bytes and final newline preserved without transformation.
- Position rules: The same dictionary is eligible at every word position. Phrase checksum or seed validity is never evaluated by Tessaveil.
- Source revision: 3a10b5b5f0a7586df8928d580a3009744ebb2079
- License: MIT
- Attribution: BIP39 authors Marek Palatinus, Pavol Rusnak, Aaron Voisine, Sean Bowe and word-list contributors. Byte-identical reference copy\: Copyright \(c\) 2013-2016 Pavol Rusnak. Full license and language credits in THIRD\_PARTY\_NOTICES.
- Repository redistribution: allowed
- SignPath compatibility: compatible
- License evidence: [bip39-license](../catalog/evidence/bip39-license.json), [bip39-osi-mit](../catalog/evidence/bip39-osi-mit.json), [bip39-signpath](../catalog/evidence/bip39-signpath.json)
- Test vectors: [bip39-vectors](../catalog/evidence/bip39-vectors.json)

<a id="dictionary-bip39-es"></a>

### BIP39 — Spanish — bip39-es

- Source record: [bip39-es](../catalog/dictionaries/bip39-es.json)
- Status: verified
- Reason: Verified research record; not a release or security guarantee.
- Version interval (min / max): 3a10b5b5f0a7586df8928d580a3009744ebb2079 / 3a10b5b5f0a7586df8928d580a3009744ebb2079
- Verified on: 2026-09-29
- Historical: false
- Evidence: [bip39-guidance](../catalog/evidence/bip39-guidance.json), [bip39-license](../catalog/evidence/bip39-license.json), [bip39-osi-mit](../catalog/evidence/bip39-osi-mit.json), [bip39-signpath](../catalog/evidence/bip39-signpath.json), [bip39-spec](../catalog/evidence/bip39-spec.json), [bip39-vectors](../catalog/evidence/bip39-vectors.json)
- Evidence claim: BIP39 links exactly ten language lists and language-specific guidance; Japanese generation uses ideographic spaces, which NFKD converts to ASCII spaces. Original source line order and bytes are preserved. Reviewed 2026-09-29; byte SHA-256 363a51bc4748d95541bb156e0439de7b51f28b260433c09874e5891dd3b0f883. See docs/research/batches/bip39-ton.md.
- Evidence claim: Local license review by Codex\: the actual MIT license of the BIP39 reference implementation permits redistribution with copyright and permission notice. Every bundled bitcoin/bips list is byte-identical to src/mnemonic/wordlist at this licensed reference revision; vectors.json is in the same repository. No directory-specific exception was found. Notices preserve the license and attribution. repository\_redistribution=allowed for these exact bytes and public test projections, not arbitrary BIPs material. Reviewed 2026-09-29; byte SHA-256 d5e3c7c62a84e80073201e2f6e5130e9e6804fa05f8ac4f8b26a13c7d3969697. See docs/research/batches/bip39-ton.md.
- Evidence claim: OSI identifies MIT as an approved open-source license; this corroborates the local component assessment, while the pinned reference repository license supplies the actual permission. Reviewed 2026-09-29; byte SHA-256 004c79db0a335488afc87600d89f447dce7fb4d24d510af15ed4381a24be848c. See docs/research/batches/bip39-ton.md.
- Evidence claim: Local component review by Codex\: the exact MIT-licensed lists are source data with no executable dependencies or proprietary restrictions. Together with retained MIT notices and OSI approval this supports signpath\_compatible=compatible for this payload only. SignPath terms require OSS components; this is not Foundation acceptance or project release/signing approval. Reviewed 2026-09-29; byte SHA-256 6610cf889bbe0dc7533abaa310bc7a5cc9a61ae6c2ce0798a08109c925b46c51. See docs/research/batches/bip39-ton.md.
- Evidence claim: Bitcoin BIP39 specifies 2048 indexed words, 12/15/18/21/24 lengths and UTF-8 NFKD for words, sentence and optional passphrase; equal vocabulary does not establish TON derivation. Reviewed 2026-09-29; byte SHA-256 afcbcbed36fe9eb734bd607398a8c124683ded2a75c3830e1b16c47b043a9134. See docs/research/batches/bip39-ton.md.
- Evidence claim: Trezor's public vectors.json supplies 24 independent entropy/mnemonic/seed known answers per language for all ten lists, with passphrase TREZOR. Offline test reconstructs words from entropy, checks published normalized sentence fingerprints and PBKDF2 seed. Public, non-funded data only; fixture projection contains no user phrase. Reviewed 2026-09-29; byte SHA-256 fa3b937b7cff9c9b8ecd3aa011faeb8d6dd67993174b72326e83f4de8fdb30f8. See docs/research/batches/bip39-ton.md.
- Language: es
- Script: Latn
- Encoding: UTF-8
- Normalization: NFKD
- Word count: 2048
- SHA-256: 46846a5a0139d1e3cb77293e521c2865f7bcdb82c44e8d0a06a2cd0ecba48c0b
- Order rule: Exact upstream source line order; zero-based 11-bit indices 0 through 2047. UTF-8 LF bytes and final newline preserved without transformation.
- Position rules: The same dictionary is eligible at every word position. Phrase checksum or seed validity is never evaluated by Tessaveil.
- Source revision: 3a10b5b5f0a7586df8928d580a3009744ebb2079
- License: MIT
- Attribution: BIP39 authors Marek Palatinus, Pavol Rusnak, Aaron Voisine, Sean Bowe and word-list contributors. Byte-identical reference copy\: Copyright \(c\) 2013-2016 Pavol Rusnak. Full license and language credits in THIRD\_PARTY\_NOTICES.
- Repository redistribution: allowed
- SignPath compatibility: compatible
- License evidence: [bip39-license](../catalog/evidence/bip39-license.json), [bip39-osi-mit](../catalog/evidence/bip39-osi-mit.json), [bip39-signpath](../catalog/evidence/bip39-signpath.json)
- Test vectors: [bip39-vectors](../catalog/evidence/bip39-vectors.json)

<a id="dictionary-bip39-fr"></a>

### BIP39 — French — bip39-fr

- Source record: [bip39-fr](../catalog/dictionaries/bip39-fr.json)
- Status: verified
- Reason: Verified research record; not a release or security guarantee.
- Version interval (min / max): 3a10b5b5f0a7586df8928d580a3009744ebb2079 / 3a10b5b5f0a7586df8928d580a3009744ebb2079
- Verified on: 2026-09-29
- Historical: false
- Evidence: [bip39-guidance](../catalog/evidence/bip39-guidance.json), [bip39-license](../catalog/evidence/bip39-license.json), [bip39-osi-mit](../catalog/evidence/bip39-osi-mit.json), [bip39-signpath](../catalog/evidence/bip39-signpath.json), [bip39-spec](../catalog/evidence/bip39-spec.json), [bip39-vectors](../catalog/evidence/bip39-vectors.json)
- Evidence claim: BIP39 links exactly ten language lists and language-specific guidance; Japanese generation uses ideographic spaces, which NFKD converts to ASCII spaces. Original source line order and bytes are preserved. Reviewed 2026-09-29; byte SHA-256 363a51bc4748d95541bb156e0439de7b51f28b260433c09874e5891dd3b0f883. See docs/research/batches/bip39-ton.md.
- Evidence claim: Local license review by Codex\: the actual MIT license of the BIP39 reference implementation permits redistribution with copyright and permission notice. Every bundled bitcoin/bips list is byte-identical to src/mnemonic/wordlist at this licensed reference revision; vectors.json is in the same repository. No directory-specific exception was found. Notices preserve the license and attribution. repository\_redistribution=allowed for these exact bytes and public test projections, not arbitrary BIPs material. Reviewed 2026-09-29; byte SHA-256 d5e3c7c62a84e80073201e2f6e5130e9e6804fa05f8ac4f8b26a13c7d3969697. See docs/research/batches/bip39-ton.md.
- Evidence claim: OSI identifies MIT as an approved open-source license; this corroborates the local component assessment, while the pinned reference repository license supplies the actual permission. Reviewed 2026-09-29; byte SHA-256 004c79db0a335488afc87600d89f447dce7fb4d24d510af15ed4381a24be848c. See docs/research/batches/bip39-ton.md.
- Evidence claim: Local component review by Codex\: the exact MIT-licensed lists are source data with no executable dependencies or proprietary restrictions. Together with retained MIT notices and OSI approval this supports signpath\_compatible=compatible for this payload only. SignPath terms require OSS components; this is not Foundation acceptance or project release/signing approval. Reviewed 2026-09-29; byte SHA-256 6610cf889bbe0dc7533abaa310bc7a5cc9a61ae6c2ce0798a08109c925b46c51. See docs/research/batches/bip39-ton.md.
- Evidence claim: Bitcoin BIP39 specifies 2048 indexed words, 12/15/18/21/24 lengths and UTF-8 NFKD for words, sentence and optional passphrase; equal vocabulary does not establish TON derivation. Reviewed 2026-09-29; byte SHA-256 afcbcbed36fe9eb734bd607398a8c124683ded2a75c3830e1b16c47b043a9134. See docs/research/batches/bip39-ton.md.
- Evidence claim: Trezor's public vectors.json supplies 24 independent entropy/mnemonic/seed known answers per language for all ten lists, with passphrase TREZOR. Offline test reconstructs words from entropy, checks published normalized sentence fingerprints and PBKDF2 seed. Public, non-funded data only; fixture projection contains no user phrase. Reviewed 2026-09-29; byte SHA-256 fa3b937b7cff9c9b8ecd3aa011faeb8d6dd67993174b72326e83f4de8fdb30f8. See docs/research/batches/bip39-ton.md.
- Language: fr
- Script: Latn
- Encoding: UTF-8
- Normalization: NFKD
- Word count: 2048
- SHA-256: ebc3959ab7801a1df6bac4fa7d970652f1df76b683cd2f4003c941c63d517e59
- Order rule: Exact upstream source line order; zero-based 11-bit indices 0 through 2047. UTF-8 LF bytes and final newline preserved without transformation.
- Position rules: The same dictionary is eligible at every word position. Phrase checksum or seed validity is never evaluated by Tessaveil.
- Source revision: 3a10b5b5f0a7586df8928d580a3009744ebb2079
- License: MIT
- Attribution: BIP39 authors Marek Palatinus, Pavol Rusnak, Aaron Voisine, Sean Bowe and word-list contributors. Byte-identical reference copy\: Copyright \(c\) 2013-2016 Pavol Rusnak. Full license and language credits in THIRD\_PARTY\_NOTICES.
- Repository redistribution: allowed
- SignPath compatibility: compatible
- License evidence: [bip39-license](../catalog/evidence/bip39-license.json), [bip39-osi-mit](../catalog/evidence/bip39-osi-mit.json), [bip39-signpath](../catalog/evidence/bip39-signpath.json)
- Test vectors: [bip39-vectors](../catalog/evidence/bip39-vectors.json)

<a id="dictionary-bip39-it"></a>

### BIP39 — Italian — bip39-it

- Source record: [bip39-it](../catalog/dictionaries/bip39-it.json)
- Status: verified
- Reason: Verified research record; not a release or security guarantee.
- Version interval (min / max): 3a10b5b5f0a7586df8928d580a3009744ebb2079 / 3a10b5b5f0a7586df8928d580a3009744ebb2079
- Verified on: 2026-09-29
- Historical: false
- Evidence: [bip39-guidance](../catalog/evidence/bip39-guidance.json), [bip39-license](../catalog/evidence/bip39-license.json), [bip39-osi-mit](../catalog/evidence/bip39-osi-mit.json), [bip39-signpath](../catalog/evidence/bip39-signpath.json), [bip39-spec](../catalog/evidence/bip39-spec.json), [bip39-vectors](../catalog/evidence/bip39-vectors.json)
- Evidence claim: BIP39 links exactly ten language lists and language-specific guidance; Japanese generation uses ideographic spaces, which NFKD converts to ASCII spaces. Original source line order and bytes are preserved. Reviewed 2026-09-29; byte SHA-256 363a51bc4748d95541bb156e0439de7b51f28b260433c09874e5891dd3b0f883. See docs/research/batches/bip39-ton.md.
- Evidence claim: Local license review by Codex\: the actual MIT license of the BIP39 reference implementation permits redistribution with copyright and permission notice. Every bundled bitcoin/bips list is byte-identical to src/mnemonic/wordlist at this licensed reference revision; vectors.json is in the same repository. No directory-specific exception was found. Notices preserve the license and attribution. repository\_redistribution=allowed for these exact bytes and public test projections, not arbitrary BIPs material. Reviewed 2026-09-29; byte SHA-256 d5e3c7c62a84e80073201e2f6e5130e9e6804fa05f8ac4f8b26a13c7d3969697. See docs/research/batches/bip39-ton.md.
- Evidence claim: OSI identifies MIT as an approved open-source license; this corroborates the local component assessment, while the pinned reference repository license supplies the actual permission. Reviewed 2026-09-29; byte SHA-256 004c79db0a335488afc87600d89f447dce7fb4d24d510af15ed4381a24be848c. See docs/research/batches/bip39-ton.md.
- Evidence claim: Local component review by Codex\: the exact MIT-licensed lists are source data with no executable dependencies or proprietary restrictions. Together with retained MIT notices and OSI approval this supports signpath\_compatible=compatible for this payload only. SignPath terms require OSS components; this is not Foundation acceptance or project release/signing approval. Reviewed 2026-09-29; byte SHA-256 6610cf889bbe0dc7533abaa310bc7a5cc9a61ae6c2ce0798a08109c925b46c51. See docs/research/batches/bip39-ton.md.
- Evidence claim: Bitcoin BIP39 specifies 2048 indexed words, 12/15/18/21/24 lengths and UTF-8 NFKD for words, sentence and optional passphrase; equal vocabulary does not establish TON derivation. Reviewed 2026-09-29; byte SHA-256 afcbcbed36fe9eb734bd607398a8c124683ded2a75c3830e1b16c47b043a9134. See docs/research/batches/bip39-ton.md.
- Evidence claim: Trezor's public vectors.json supplies 24 independent entropy/mnemonic/seed known answers per language for all ten lists, with passphrase TREZOR. Offline test reconstructs words from entropy, checks published normalized sentence fingerprints and PBKDF2 seed. Public, non-funded data only; fixture projection contains no user phrase. Reviewed 2026-09-29; byte SHA-256 fa3b937b7cff9c9b8ecd3aa011faeb8d6dd67993174b72326e83f4de8fdb30f8. See docs/research/batches/bip39-ton.md.
- Language: it
- Script: Latn
- Encoding: UTF-8
- Normalization: NFKD
- Word count: 2048
- SHA-256: d392c49fdb700a24cd1fceb237c1f65dcc128f6b34a8aacb58b59384b5c648c2
- Order rule: Exact upstream source line order; zero-based 11-bit indices 0 through 2047. UTF-8 LF bytes and final newline preserved without transformation.
- Position rules: The same dictionary is eligible at every word position. Phrase checksum or seed validity is never evaluated by Tessaveil.
- Source revision: 3a10b5b5f0a7586df8928d580a3009744ebb2079
- License: MIT
- Attribution: BIP39 authors Marek Palatinus, Pavol Rusnak, Aaron Voisine, Sean Bowe and word-list contributors. Byte-identical reference copy\: Copyright \(c\) 2013-2016 Pavol Rusnak. Full license and language credits in THIRD\_PARTY\_NOTICES.
- Repository redistribution: allowed
- SignPath compatibility: compatible
- License evidence: [bip39-license](../catalog/evidence/bip39-license.json), [bip39-osi-mit](../catalog/evidence/bip39-osi-mit.json), [bip39-signpath](../catalog/evidence/bip39-signpath.json)
- Test vectors: [bip39-vectors](../catalog/evidence/bip39-vectors.json)

<a id="dictionary-bip39-ja"></a>

### BIP39 — Japanese — bip39-ja

- Source record: [bip39-ja](../catalog/dictionaries/bip39-ja.json)
- Status: verified
- Reason: Verified research record; not a release or security guarantee.
- Version interval (min / max): 3a10b5b5f0a7586df8928d580a3009744ebb2079 / 3a10b5b5f0a7586df8928d580a3009744ebb2079
- Verified on: 2026-09-29
- Historical: false
- Evidence: [bip39-guidance](../catalog/evidence/bip39-guidance.json), [bip39-license](../catalog/evidence/bip39-license.json), [bip39-osi-mit](../catalog/evidence/bip39-osi-mit.json), [bip39-signpath](../catalog/evidence/bip39-signpath.json), [bip39-spec](../catalog/evidence/bip39-spec.json), [bip39-vectors](../catalog/evidence/bip39-vectors.json)
- Evidence claim: BIP39 links exactly ten language lists and language-specific guidance; Japanese generation uses ideographic spaces, which NFKD converts to ASCII spaces. Original source line order and bytes are preserved. Reviewed 2026-09-29; byte SHA-256 363a51bc4748d95541bb156e0439de7b51f28b260433c09874e5891dd3b0f883. See docs/research/batches/bip39-ton.md.
- Evidence claim: Local license review by Codex\: the actual MIT license of the BIP39 reference implementation permits redistribution with copyright and permission notice. Every bundled bitcoin/bips list is byte-identical to src/mnemonic/wordlist at this licensed reference revision; vectors.json is in the same repository. No directory-specific exception was found. Notices preserve the license and attribution. repository\_redistribution=allowed for these exact bytes and public test projections, not arbitrary BIPs material. Reviewed 2026-09-29; byte SHA-256 d5e3c7c62a84e80073201e2f6e5130e9e6804fa05f8ac4f8b26a13c7d3969697. See docs/research/batches/bip39-ton.md.
- Evidence claim: OSI identifies MIT as an approved open-source license; this corroborates the local component assessment, while the pinned reference repository license supplies the actual permission. Reviewed 2026-09-29; byte SHA-256 004c79db0a335488afc87600d89f447dce7fb4d24d510af15ed4381a24be848c. See docs/research/batches/bip39-ton.md.
- Evidence claim: Local component review by Codex\: the exact MIT-licensed lists are source data with no executable dependencies or proprietary restrictions. Together with retained MIT notices and OSI approval this supports signpath\_compatible=compatible for this payload only. SignPath terms require OSS components; this is not Foundation acceptance or project release/signing approval. Reviewed 2026-09-29; byte SHA-256 6610cf889bbe0dc7533abaa310bc7a5cc9a61ae6c2ce0798a08109c925b46c51. See docs/research/batches/bip39-ton.md.
- Evidence claim: Bitcoin BIP39 specifies 2048 indexed words, 12/15/18/21/24 lengths and UTF-8 NFKD for words, sentence and optional passphrase; equal vocabulary does not establish TON derivation. Reviewed 2026-09-29; byte SHA-256 afcbcbed36fe9eb734bd607398a8c124683ded2a75c3830e1b16c47b043a9134. See docs/research/batches/bip39-ton.md.
- Evidence claim: Trezor's public vectors.json supplies 24 independent entropy/mnemonic/seed known answers per language for all ten lists, with passphrase TREZOR. Offline test reconstructs words from entropy, checks published normalized sentence fingerprints and PBKDF2 seed. Public, non-funded data only; fixture projection contains no user phrase. Reviewed 2026-09-29; byte SHA-256 fa3b937b7cff9c9b8ecd3aa011faeb8d6dd67993174b72326e83f4de8fdb30f8. See docs/research/batches/bip39-ton.md.
- Language: ja
- Script: Jpan
- Encoding: UTF-8
- Normalization: NFKD
- Word count: 2048
- SHA-256: 2eed0aef492291e061633d7ad8117f1a2b03eb80a29d0e4e3117ac2528d05ffd
- Order rule: Exact upstream source line order; zero-based 11-bit indices 0 through 2047. UTF-8 LF bytes and final newline preserved without transformation.
- Position rules: The same dictionary is eligible at every word position. Phrase checksum or seed validity is never evaluated by Tessaveil.
- Source revision: 3a10b5b5f0a7586df8928d580a3009744ebb2079
- License: MIT
- Attribution: BIP39 authors Marek Palatinus, Pavol Rusnak, Aaron Voisine, Sean Bowe and word-list contributors. Byte-identical reference copy\: Copyright \(c\) 2013-2016 Pavol Rusnak. Full license and language credits in THIRD\_PARTY\_NOTICES.
- Repository redistribution: allowed
- SignPath compatibility: compatible
- License evidence: [bip39-license](../catalog/evidence/bip39-license.json), [bip39-osi-mit](../catalog/evidence/bip39-osi-mit.json), [bip39-signpath](../catalog/evidence/bip39-signpath.json)
- Test vectors: [bip39-vectors](../catalog/evidence/bip39-vectors.json)

<a id="dictionary-bip39-ko"></a>

### BIP39 — Korean — bip39-ko

- Source record: [bip39-ko](../catalog/dictionaries/bip39-ko.json)
- Status: verified
- Reason: Verified research record; not a release or security guarantee.
- Version interval (min / max): 3a10b5b5f0a7586df8928d580a3009744ebb2079 / 3a10b5b5f0a7586df8928d580a3009744ebb2079
- Verified on: 2026-09-29
- Historical: false
- Evidence: [bip39-guidance](../catalog/evidence/bip39-guidance.json), [bip39-license](../catalog/evidence/bip39-license.json), [bip39-osi-mit](../catalog/evidence/bip39-osi-mit.json), [bip39-signpath](../catalog/evidence/bip39-signpath.json), [bip39-spec](../catalog/evidence/bip39-spec.json), [bip39-vectors](../catalog/evidence/bip39-vectors.json)
- Evidence claim: BIP39 links exactly ten language lists and language-specific guidance; Japanese generation uses ideographic spaces, which NFKD converts to ASCII spaces. Original source line order and bytes are preserved. Reviewed 2026-09-29; byte SHA-256 363a51bc4748d95541bb156e0439de7b51f28b260433c09874e5891dd3b0f883. See docs/research/batches/bip39-ton.md.
- Evidence claim: Local license review by Codex\: the actual MIT license of the BIP39 reference implementation permits redistribution with copyright and permission notice. Every bundled bitcoin/bips list is byte-identical to src/mnemonic/wordlist at this licensed reference revision; vectors.json is in the same repository. No directory-specific exception was found. Notices preserve the license and attribution. repository\_redistribution=allowed for these exact bytes and public test projections, not arbitrary BIPs material. Reviewed 2026-09-29; byte SHA-256 d5e3c7c62a84e80073201e2f6e5130e9e6804fa05f8ac4f8b26a13c7d3969697. See docs/research/batches/bip39-ton.md.
- Evidence claim: OSI identifies MIT as an approved open-source license; this corroborates the local component assessment, while the pinned reference repository license supplies the actual permission. Reviewed 2026-09-29; byte SHA-256 004c79db0a335488afc87600d89f447dce7fb4d24d510af15ed4381a24be848c. See docs/research/batches/bip39-ton.md.
- Evidence claim: Local component review by Codex\: the exact MIT-licensed lists are source data with no executable dependencies or proprietary restrictions. Together with retained MIT notices and OSI approval this supports signpath\_compatible=compatible for this payload only. SignPath terms require OSS components; this is not Foundation acceptance or project release/signing approval. Reviewed 2026-09-29; byte SHA-256 6610cf889bbe0dc7533abaa310bc7a5cc9a61ae6c2ce0798a08109c925b46c51. See docs/research/batches/bip39-ton.md.
- Evidence claim: Bitcoin BIP39 specifies 2048 indexed words, 12/15/18/21/24 lengths and UTF-8 NFKD for words, sentence and optional passphrase; equal vocabulary does not establish TON derivation. Reviewed 2026-09-29; byte SHA-256 afcbcbed36fe9eb734bd607398a8c124683ded2a75c3830e1b16c47b043a9134. See docs/research/batches/bip39-ton.md.
- Evidence claim: Trezor's public vectors.json supplies 24 independent entropy/mnemonic/seed known answers per language for all ten lists, with passphrase TREZOR. Offline test reconstructs words from entropy, checks published normalized sentence fingerprints and PBKDF2 seed. Public, non-funded data only; fixture projection contains no user phrase. Reviewed 2026-09-29; byte SHA-256 fa3b937b7cff9c9b8ecd3aa011faeb8d6dd67993174b72326e83f4de8fdb30f8. See docs/research/batches/bip39-ton.md.
- Language: ko
- Script: Hang
- Encoding: UTF-8
- Normalization: NFKD
- Word count: 2048
- SHA-256: 9e95f86c167de88f450f0aaf89e87f6624a57f973c67b516e338e8e8b8897f60
- Order rule: Exact upstream source line order; zero-based 11-bit indices 0 through 2047. UTF-8 LF bytes and final newline preserved without transformation.
- Position rules: The same dictionary is eligible at every word position. Phrase checksum or seed validity is never evaluated by Tessaveil.
- Source revision: 3a10b5b5f0a7586df8928d580a3009744ebb2079
- License: MIT
- Attribution: BIP39 authors Marek Palatinus, Pavol Rusnak, Aaron Voisine, Sean Bowe and word-list contributors. Byte-identical reference copy\: Copyright \(c\) 2013-2016 Pavol Rusnak. Full license and language credits in THIRD\_PARTY\_NOTICES.
- Repository redistribution: allowed
- SignPath compatibility: compatible
- License evidence: [bip39-license](../catalog/evidence/bip39-license.json), [bip39-osi-mit](../catalog/evidence/bip39-osi-mit.json), [bip39-signpath](../catalog/evidence/bip39-signpath.json)
- Test vectors: [bip39-vectors](../catalog/evidence/bip39-vectors.json)

<a id="dictionary-bip39-pt"></a>

### BIP39 — Portuguese — bip39-pt

- Source record: [bip39-pt](../catalog/dictionaries/bip39-pt.json)
- Status: verified
- Reason: Verified research record; not a release or security guarantee.
- Version interval (min / max): 3a10b5b5f0a7586df8928d580a3009744ebb2079 / 3a10b5b5f0a7586df8928d580a3009744ebb2079
- Verified on: 2026-09-29
- Historical: false
- Evidence: [bip39-guidance](../catalog/evidence/bip39-guidance.json), [bip39-license](../catalog/evidence/bip39-license.json), [bip39-osi-mit](../catalog/evidence/bip39-osi-mit.json), [bip39-signpath](../catalog/evidence/bip39-signpath.json), [bip39-spec](../catalog/evidence/bip39-spec.json), [bip39-vectors](../catalog/evidence/bip39-vectors.json)
- Evidence claim: BIP39 links exactly ten language lists and language-specific guidance; Japanese generation uses ideographic spaces, which NFKD converts to ASCII spaces. Original source line order and bytes are preserved. Reviewed 2026-09-29; byte SHA-256 363a51bc4748d95541bb156e0439de7b51f28b260433c09874e5891dd3b0f883. See docs/research/batches/bip39-ton.md.
- Evidence claim: Local license review by Codex\: the actual MIT license of the BIP39 reference implementation permits redistribution with copyright and permission notice. Every bundled bitcoin/bips list is byte-identical to src/mnemonic/wordlist at this licensed reference revision; vectors.json is in the same repository. No directory-specific exception was found. Notices preserve the license and attribution. repository\_redistribution=allowed for these exact bytes and public test projections, not arbitrary BIPs material. Reviewed 2026-09-29; byte SHA-256 d5e3c7c62a84e80073201e2f6e5130e9e6804fa05f8ac4f8b26a13c7d3969697. See docs/research/batches/bip39-ton.md.
- Evidence claim: OSI identifies MIT as an approved open-source license; this corroborates the local component assessment, while the pinned reference repository license supplies the actual permission. Reviewed 2026-09-29; byte SHA-256 004c79db0a335488afc87600d89f447dce7fb4d24d510af15ed4381a24be848c. See docs/research/batches/bip39-ton.md.
- Evidence claim: Local component review by Codex\: the exact MIT-licensed lists are source data with no executable dependencies or proprietary restrictions. Together with retained MIT notices and OSI approval this supports signpath\_compatible=compatible for this payload only. SignPath terms require OSS components; this is not Foundation acceptance or project release/signing approval. Reviewed 2026-09-29; byte SHA-256 6610cf889bbe0dc7533abaa310bc7a5cc9a61ae6c2ce0798a08109c925b46c51. See docs/research/batches/bip39-ton.md.
- Evidence claim: Bitcoin BIP39 specifies 2048 indexed words, 12/15/18/21/24 lengths and UTF-8 NFKD for words, sentence and optional passphrase; equal vocabulary does not establish TON derivation. Reviewed 2026-09-29; byte SHA-256 afcbcbed36fe9eb734bd607398a8c124683ded2a75c3830e1b16c47b043a9134. See docs/research/batches/bip39-ton.md.
- Evidence claim: Trezor's public vectors.json supplies 24 independent entropy/mnemonic/seed known answers per language for all ten lists, with passphrase TREZOR. Offline test reconstructs words from entropy, checks published normalized sentence fingerprints and PBKDF2 seed. Public, non-funded data only; fixture projection contains no user phrase. Reviewed 2026-09-29; byte SHA-256 fa3b937b7cff9c9b8ecd3aa011faeb8d6dd67993174b72326e83f4de8fdb30f8. See docs/research/batches/bip39-ton.md.
- Language: pt
- Script: Latn
- Encoding: UTF-8
- Normalization: NFKD
- Word count: 2048
- SHA-256: 2685e9c194c82ae67e10ba59d9ea5345a23dc093e92276fc5361f6667d79cd3f
- Order rule: Exact upstream source line order; zero-based 11-bit indices 0 through 2047. UTF-8 LF bytes and final newline preserved without transformation.
- Position rules: The same dictionary is eligible at every word position. Phrase checksum or seed validity is never evaluated by Tessaveil.
- Source revision: 3a10b5b5f0a7586df8928d580a3009744ebb2079
- License: MIT
- Attribution: BIP39 authors Marek Palatinus, Pavol Rusnak, Aaron Voisine, Sean Bowe and word-list contributors. Byte-identical reference copy\: Copyright \(c\) 2013-2016 Pavol Rusnak. Full license and language credits in THIRD\_PARTY\_NOTICES.
- Repository redistribution: allowed
- SignPath compatibility: compatible
- License evidence: [bip39-license](../catalog/evidence/bip39-license.json), [bip39-osi-mit](../catalog/evidence/bip39-osi-mit.json), [bip39-signpath](../catalog/evidence/bip39-signpath.json)
- Test vectors: [bip39-vectors](../catalog/evidence/bip39-vectors.json)

<a id="dictionary-bip39-zh-hans"></a>

### BIP39 — Chinese Simplified — bip39-zh-hans

- Source record: [bip39-zh-hans](../catalog/dictionaries/bip39-zh-hans.json)
- Status: verified
- Reason: Verified research record; not a release or security guarantee.
- Version interval (min / max): 3a10b5b5f0a7586df8928d580a3009744ebb2079 / 3a10b5b5f0a7586df8928d580a3009744ebb2079
- Verified on: 2026-09-29
- Historical: false
- Evidence: [bip39-guidance](../catalog/evidence/bip39-guidance.json), [bip39-license](../catalog/evidence/bip39-license.json), [bip39-osi-mit](../catalog/evidence/bip39-osi-mit.json), [bip39-signpath](../catalog/evidence/bip39-signpath.json), [bip39-spec](../catalog/evidence/bip39-spec.json), [bip39-vectors](../catalog/evidence/bip39-vectors.json)
- Evidence claim: BIP39 links exactly ten language lists and language-specific guidance; Japanese generation uses ideographic spaces, which NFKD converts to ASCII spaces. Original source line order and bytes are preserved. Reviewed 2026-09-29; byte SHA-256 363a51bc4748d95541bb156e0439de7b51f28b260433c09874e5891dd3b0f883. See docs/research/batches/bip39-ton.md.
- Evidence claim: Local license review by Codex\: the actual MIT license of the BIP39 reference implementation permits redistribution with copyright and permission notice. Every bundled bitcoin/bips list is byte-identical to src/mnemonic/wordlist at this licensed reference revision; vectors.json is in the same repository. No directory-specific exception was found. Notices preserve the license and attribution. repository\_redistribution=allowed for these exact bytes and public test projections, not arbitrary BIPs material. Reviewed 2026-09-29; byte SHA-256 d5e3c7c62a84e80073201e2f6e5130e9e6804fa05f8ac4f8b26a13c7d3969697. See docs/research/batches/bip39-ton.md.
- Evidence claim: OSI identifies MIT as an approved open-source license; this corroborates the local component assessment, while the pinned reference repository license supplies the actual permission. Reviewed 2026-09-29; byte SHA-256 004c79db0a335488afc87600d89f447dce7fb4d24d510af15ed4381a24be848c. See docs/research/batches/bip39-ton.md.
- Evidence claim: Local component review by Codex\: the exact MIT-licensed lists are source data with no executable dependencies or proprietary restrictions. Together with retained MIT notices and OSI approval this supports signpath\_compatible=compatible for this payload only. SignPath terms require OSS components; this is not Foundation acceptance or project release/signing approval. Reviewed 2026-09-29; byte SHA-256 6610cf889bbe0dc7533abaa310bc7a5cc9a61ae6c2ce0798a08109c925b46c51. See docs/research/batches/bip39-ton.md.
- Evidence claim: Bitcoin BIP39 specifies 2048 indexed words, 12/15/18/21/24 lengths and UTF-8 NFKD for words, sentence and optional passphrase; equal vocabulary does not establish TON derivation. Reviewed 2026-09-29; byte SHA-256 afcbcbed36fe9eb734bd607398a8c124683ded2a75c3830e1b16c47b043a9134. See docs/research/batches/bip39-ton.md.
- Evidence claim: Trezor's public vectors.json supplies 24 independent entropy/mnemonic/seed known answers per language for all ten lists, with passphrase TREZOR. Offline test reconstructs words from entropy, checks published normalized sentence fingerprints and PBKDF2 seed. Public, non-funded data only; fixture projection contains no user phrase. Reviewed 2026-09-29; byte SHA-256 fa3b937b7cff9c9b8ecd3aa011faeb8d6dd67993174b72326e83f4de8fdb30f8. See docs/research/batches/bip39-ton.md.
- Language: zh-hans
- Script: Hans
- Encoding: UTF-8
- Normalization: NFKD
- Word count: 2048
- SHA-256: 5c5942792bd8340cb8b27cd592f1015edf56a8c5b26276ee18a482428e7c5726
- Order rule: Exact upstream source line order; zero-based 11-bit indices 0 through 2047. UTF-8 LF bytes and final newline preserved without transformation.
- Position rules: The same dictionary is eligible at every word position. Phrase checksum or seed validity is never evaluated by Tessaveil.
- Source revision: 3a10b5b5f0a7586df8928d580a3009744ebb2079
- License: MIT
- Attribution: BIP39 authors Marek Palatinus, Pavol Rusnak, Aaron Voisine, Sean Bowe and word-list contributors. Byte-identical reference copy\: Copyright \(c\) 2013-2016 Pavol Rusnak. Full license and language credits in THIRD\_PARTY\_NOTICES.
- Repository redistribution: allowed
- SignPath compatibility: compatible
- License evidence: [bip39-license](../catalog/evidence/bip39-license.json), [bip39-osi-mit](../catalog/evidence/bip39-osi-mit.json), [bip39-signpath](../catalog/evidence/bip39-signpath.json)
- Test vectors: [bip39-vectors](../catalog/evidence/bip39-vectors.json)

<a id="dictionary-bip39-zh-hant"></a>

### BIP39 — Chinese Traditional — bip39-zh-hant

- Source record: [bip39-zh-hant](../catalog/dictionaries/bip39-zh-hant.json)
- Status: verified
- Reason: Verified research record; not a release or security guarantee.
- Version interval (min / max): 3a10b5b5f0a7586df8928d580a3009744ebb2079 / 3a10b5b5f0a7586df8928d580a3009744ebb2079
- Verified on: 2026-09-29
- Historical: false
- Evidence: [bip39-guidance](../catalog/evidence/bip39-guidance.json), [bip39-license](../catalog/evidence/bip39-license.json), [bip39-osi-mit](../catalog/evidence/bip39-osi-mit.json), [bip39-signpath](../catalog/evidence/bip39-signpath.json), [bip39-spec](../catalog/evidence/bip39-spec.json), [bip39-vectors](../catalog/evidence/bip39-vectors.json)
- Evidence claim: BIP39 links exactly ten language lists and language-specific guidance; Japanese generation uses ideographic spaces, which NFKD converts to ASCII spaces. Original source line order and bytes are preserved. Reviewed 2026-09-29; byte SHA-256 363a51bc4748d95541bb156e0439de7b51f28b260433c09874e5891dd3b0f883. See docs/research/batches/bip39-ton.md.
- Evidence claim: Local license review by Codex\: the actual MIT license of the BIP39 reference implementation permits redistribution with copyright and permission notice. Every bundled bitcoin/bips list is byte-identical to src/mnemonic/wordlist at this licensed reference revision; vectors.json is in the same repository. No directory-specific exception was found. Notices preserve the license and attribution. repository\_redistribution=allowed for these exact bytes and public test projections, not arbitrary BIPs material. Reviewed 2026-09-29; byte SHA-256 d5e3c7c62a84e80073201e2f6e5130e9e6804fa05f8ac4f8b26a13c7d3969697. See docs/research/batches/bip39-ton.md.
- Evidence claim: OSI identifies MIT as an approved open-source license; this corroborates the local component assessment, while the pinned reference repository license supplies the actual permission. Reviewed 2026-09-29; byte SHA-256 004c79db0a335488afc87600d89f447dce7fb4d24d510af15ed4381a24be848c. See docs/research/batches/bip39-ton.md.
- Evidence claim: Local component review by Codex\: the exact MIT-licensed lists are source data with no executable dependencies or proprietary restrictions. Together with retained MIT notices and OSI approval this supports signpath\_compatible=compatible for this payload only. SignPath terms require OSS components; this is not Foundation acceptance or project release/signing approval. Reviewed 2026-09-29; byte SHA-256 6610cf889bbe0dc7533abaa310bc7a5cc9a61ae6c2ce0798a08109c925b46c51. See docs/research/batches/bip39-ton.md.
- Evidence claim: Bitcoin BIP39 specifies 2048 indexed words, 12/15/18/21/24 lengths and UTF-8 NFKD for words, sentence and optional passphrase; equal vocabulary does not establish TON derivation. Reviewed 2026-09-29; byte SHA-256 afcbcbed36fe9eb734bd607398a8c124683ded2a75c3830e1b16c47b043a9134. See docs/research/batches/bip39-ton.md.
- Evidence claim: Trezor's public vectors.json supplies 24 independent entropy/mnemonic/seed known answers per language for all ten lists, with passphrase TREZOR. Offline test reconstructs words from entropy, checks published normalized sentence fingerprints and PBKDF2 seed. Public, non-funded data only; fixture projection contains no user phrase. Reviewed 2026-09-29; byte SHA-256 fa3b937b7cff9c9b8ecd3aa011faeb8d6dd67993174b72326e83f4de8fdb30f8. See docs/research/batches/bip39-ton.md.
- Language: zh-hant
- Script: Hant
- Encoding: UTF-8
- Normalization: NFKD
- Word count: 2048
- SHA-256: 417b26b3d8500a4ae3d59717d7011952db6fc2fb84b807f3f94ac734e89c1b5f
- Order rule: Exact upstream source line order; zero-based 11-bit indices 0 through 2047. UTF-8 LF bytes and final newline preserved without transformation.
- Position rules: The same dictionary is eligible at every word position. Phrase checksum or seed validity is never evaluated by Tessaveil.
- Source revision: 3a10b5b5f0a7586df8928d580a3009744ebb2079
- License: MIT
- Attribution: BIP39 authors Marek Palatinus, Pavol Rusnak, Aaron Voisine, Sean Bowe and word-list contributors. Byte-identical reference copy\: Copyright \(c\) 2013-2016 Pavol Rusnak. Full license and language credits in THIRD\_PARTY\_NOTICES.
- Repository redistribution: allowed
- SignPath compatibility: compatible
- License evidence: [bip39-license](../catalog/evidence/bip39-license.json), [bip39-osi-mit](../catalog/evidence/bip39-osi-mit.json), [bip39-signpath](../catalog/evidence/bip39-signpath.json)
- Test vectors: [bip39-vectors](../catalog/evidence/bip39-vectors.json)

<a id="dictionary-electrum-v1-en"></a>

### Electrum v1 — English \(rights unresolved\) — electrum-v1-en

- Source record: [electrum-v1-en](../catalog/dictionaries/electrum-v1-en.json)
- Status: blocked
- Reason: Support is blocked; see evidence and license decisions below.
- Guidance: Not selectable; use the wallet's own backup procedure.
- Version interval (min / max): ede66c89887234c83b0def133b3100fe92a160eb / ede66c89887234c83b0def133b3100fe92a160eb
- Verified on: 2026-09-29
- Historical: true
- Evidence: [electrum-legacy-license](../catalog/evidence/electrum-legacy-license.json), [electrum-legacy-list](../catalog/evidence/electrum-legacy-list.json)
- Evidence claim: MIT grant covers Electrum software; old\_mnemonic.py separately credits a Wiktionary frequency list. Codex review 2026-09-29 cannot establish original list revision, attribution chain or cumulative terms\: redistribution unclear and SignPath pending for that list. This is uncertainty, not a finding of infringement.
- Evidence claim: Pinned legacy encoder has 1626 English words in fixed order and encodes each 32-bit chunk as three dependent indices. File MIT header also cites a Wiktionary contemporary-poetry list; cumulative upstream data rights are not resolved. No legacy list bytes bundled.
- Language: en
- Script: Latn
- Encoding: UTF-8
- Normalization: none
- Word count: 1626
- SHA-256: —
- Order rule: Source tuple order; do not sort. No approved committed byte artifact.
- Position rules: Each three-word group encodes 32 bits with modulo-1626 dependent indices; no BIP39 checksum.
- Source revision: ede66c89887234c83b0def133b3100fe92a160eb
- License: MIT file header; upstream frequency-list terms unresolved
- Attribution: Copyright \(C\) 2011 thomasv@gitorious; Wiktionary Contemporary poetry frequency-list provenance unresolved.
- Repository redistribution: unclear
- SignPath compatibility: pending
- License evidence: [electrum-legacy-license](../catalog/evidence/electrum-legacy-license.json), [electrum-legacy-list](../catalog/evidence/electrum-legacy-list.json)
- Test vectors: —

<a id="dictionary-monero-de"></a>

### monero-de — monero-de

- Source record: [monero-de](../catalog/dictionaries/monero-de.json)
- Status: verified
- Reason: Verified research record; not a release or security guarantee.
- Version interval (min / max): 2f9d1bbb2c553dc75f3335bd1452117dfddd86fa / 2f9d1bbb2c553dc75f3335bd1452117dfddd86fa
- Verified on: 2026-09-29
- Historical: false
- Evidence: [monero-de-source](../catalog/evidence/monero-de-source.json), [monero-legacy-vectors](../catalog/evidence/monero-legacy-vectors.json), [monero-monero-license](../catalog/evidence/monero-monero-license.json), [monero-monero-rules](../catalog/evidence/monero-monero-rules.json), [monero-osi-bsd](../catalog/evidence/monero-osi-bsd.json), [monero-signpath](../catalog/evidence/monero-signpath.json)
- Evidence claim: Exact ordered dictionary array and applicable file-level license header reviewed. Source-token extraction and byte hashes are independently checked against the public fixture; no complete phrase is stored here. Reviewed 2026-09-29; response byte SHA-256 7b910a96bc94d19eb3e4edd8179db383a68b03a7608396bbee0fdc46a7d4e88e. See docs/research/batches/monero-polyseed.md.
- Evidence claim: Public Portuguese checksum and German case-tolerance examples; projection stores dictionary indices and expected phrase fingerprint. Offline test reproduces source CRC32 prefix check, not private-key/address derivation. Reviewed 2026-09-29; response byte SHA-256 520fec49e96e4b01d472f627e109b7a343f80e58291eed793f7ca76f2e63a1d1. See docs/research/batches/monero-polyseed.md.
- Evidence claim: BSD-3-Clause source-data redistribution allowed with exact copyright/license/disclaimer retention and no endorsement. File-level MIT overrides for dabura667 lists retained. Reviewed by Codex for this source-data payload only. Reviewed 2026-09-29; response byte SHA-256 1f99d6b6e1ae17de27147ff2e1e0238fa8c7d5a8accd0f1ac062c89365516abd. See docs/research/batches/monero-polyseed.md.
- Evidence claim: 1626 entries; codepoint prefixes and case-insensitive lookup. utf8canonical re-encodes codepoints with towlower, not NFC/NFKD. EnglishOld tolerates duplicate prefixes and short words. Reviewed 2026-09-29; response byte SHA-256 2bc256f01c6904af914cb7c6526254267ed463882e216fd0eb1d9bbdf4bf5bb4. See docs/research/batches/monero-polyseed.md.
- Evidence claim: OSI lists BSD-3-Clause as approved. This corroborates only the component-license decision, not project acceptance. Response-body SHA-256 0dfece33194f06d15b862c323f7ed32ba6ab7f512a7fda11880bb2e1401518f8.
- Evidence claim: Codex component assessment\: reviewed BSD-3-Clause/MIT and Apache-2.0\+MIT data licenses are OSI-approved and impose no commercial dual-licensing; notices are retained. Compatible for this data-only payload. Foundation acceptance, project eligibility and release signing remain unproven. Response-body SHA-256 6610cf889bbe0dc7533abaa310bc7a5cc9a61ae6c2ce0798a08109c925b46c51.
- Language: de
- Script: Latn
- Encoding: UTF-8
- Normalization: none
- Word count: 1626
- SHA-256: e1e6653cf418e0a392a5cd34160a8cdacb5dfce8edbac0e124fba8d7daff1f69
- Order rule: Exact upstream array order; zero-based indices. Extract literal UTF-8 tokens unchanged; remove C/C\+\+ wrapper and indentation, append LF after every token. No sorting, lowercasing or Unicode rewriting. Source file and extracted byte hashes in batch note.
- Position rules: Same vocabulary at every eligible position; upstream prefix length 4. Never evaluate a user phrase checksum.; Source-native lookup\: Unicode codepoint lowercase and language-specific prefix, with no NFC/NFKD transform; normalization=none preserves source characters.; Language coverage is not a wallet generation claim.
- Source revision: 2f9d1bbb2c553dc75f3335bd1452117dfddd86fa
- License: BSD-3-Clause
- Attribution: Exact source file notices and upstream license retained in THIRD\_PARTY\_NOTICES; dabura667 / The Monero Project and original dictionary contributors.
- Repository redistribution: allowed
- SignPath compatibility: compatible
- License evidence: [monero-de-source](../catalog/evidence/monero-de-source.json), [monero-monero-license](../catalog/evidence/monero-monero-license.json), [monero-osi-bsd](../catalog/evidence/monero-osi-bsd.json), [monero-signpath](../catalog/evidence/monero-signpath.json)
- Test vectors: [monero-legacy-vectors](../catalog/evidence/monero-legacy-vectors.json)

<a id="dictionary-monero-en"></a>

### monero-en — monero-en

- Source record: [monero-en](../catalog/dictionaries/monero-en.json)
- Status: verified
- Reason: Verified research record; not a release or security guarantee.
- Version interval (min / max): 2f9d1bbb2c553dc75f3335bd1452117dfddd86fa / 2f9d1bbb2c553dc75f3335bd1452117dfddd86fa
- Verified on: 2026-09-29
- Historical: false
- Evidence: [monero-en-source](../catalog/evidence/monero-en-source.json), [monero-monero-license](../catalog/evidence/monero-monero-license.json), [monero-monero-rules](../catalog/evidence/monero-monero-rules.json), [monero-mymonero-vectors](../catalog/evidence/monero-mymonero-vectors.json), [monero-osi-bsd](../catalog/evidence/monero-osi-bsd.json), [monero-signpath](../catalog/evidence/monero-signpath.json)
- Evidence claim: Exact ordered dictionary array and applicable file-level license header reviewed. Source-token extraction and byte hashes are independently checked against the public fixture; no complete phrase is stored here. Reviewed 2026-09-29; response byte SHA-256 9bd756d29e689aae0e6e7f8b1196c4f35df350225c4668d4f6f41842f05fc2ca. See docs/research/batches/monero-polyseed.md.
- Evidence claim: BSD-3-Clause source-data redistribution allowed with exact copyright/license/disclaimer retention and no endorsement. File-level MIT overrides for dabura667 lists retained. Reviewed by Codex for this source-data payload only. Reviewed 2026-09-29; response byte SHA-256 1f99d6b6e1ae17de27147ff2e1e0238fa8c7d5a8accd0f1ac062c89365516abd. See docs/research/batches/monero-polyseed.md.
- Evidence claim: 1626 entries; codepoint prefixes and case-insensitive lookup. utf8canonical re-encodes codepoints with towlower, not NFC/NFKD. EnglishOld tolerates duplicate prefixes and short words. Reviewed 2026-09-29; response byte SHA-256 2bc256f01c6904af914cb7c6526254267ed463882e216fd0eb1d9bbdf4bf5bb4. See docs/research/batches/monero-polyseed.md.
- Evidence claim: Published 13-word prefix mnemonic resolves to the same address as published 16-byte seed 9c973aa296b79bbf452781dd3d32ad7f. Offline projection tests entropy and checksum only; no address/Keccak claim. Reviewed 2026-09-29; response byte SHA-256 8292f763a1b2bf70052dc959a2672e73a1b4035d5c379bbccb4e03f6a2de6634. See docs/research/batches/monero-polyseed.md.
- Evidence claim: OSI lists BSD-3-Clause as approved. This corroborates only the component-license decision, not project acceptance. Response-body SHA-256 0dfece33194f06d15b862c323f7ed32ba6ab7f512a7fda11880bb2e1401518f8.
- Evidence claim: Codex component assessment\: reviewed BSD-3-Clause/MIT and Apache-2.0\+MIT data licenses are OSI-approved and impose no commercial dual-licensing; notices are retained. Compatible for this data-only payload. Foundation acceptance, project eligibility and release signing remain unproven. Response-body SHA-256 6610cf889bbe0dc7533abaa310bc7a5cc9a61ae6c2ce0798a08109c925b46c51.
- Language: en
- Script: Latn
- Encoding: UTF-8
- Normalization: none
- Word count: 1626
- SHA-256: eaa6bce7dd92f4d6dd74f224264e0ef4ad21095d68ec77616b26ceb599baf4f7
- Order rule: Exact upstream array order; zero-based indices. Extract literal UTF-8 tokens unchanged; remove C/C\+\+ wrapper and indentation, append LF after every token. No sorting, lowercasing or Unicode rewriting. Source file and extracted byte hashes in batch note.
- Position rules: Same vocabulary at every eligible position; upstream prefix length 3. Never evaluate a user phrase checksum.; Source-native lookup\: Unicode codepoint lowercase and language-specific prefix, with no NFC/NFKD transform; normalization=none preserves source characters.; Language coverage is not a wallet generation claim.
- Source revision: 2f9d1bbb2c553dc75f3335bd1452117dfddd86fa
- License: BSD-3-Clause
- Attribution: Exact source file notices and upstream license retained in THIRD\_PARTY\_NOTICES; dabura667 / The Monero Project and original dictionary contributors.
- Repository redistribution: allowed
- SignPath compatibility: compatible
- License evidence: [monero-en-source](../catalog/evidence/monero-en-source.json), [monero-monero-license](../catalog/evidence/monero-monero-license.json), [monero-osi-bsd](../catalog/evidence/monero-osi-bsd.json), [monero-signpath](../catalog/evidence/monero-signpath.json)
- Test vectors: [monero-mymonero-vectors](../catalog/evidence/monero-mymonero-vectors.json)

<a id="dictionary-monero-en-old"></a>

### monero-en-old — monero-en-old

- Source record: [monero-en-old](../catalog/dictionaries/monero-en-old.json)
- Status: documented
- Reason: Evidence is insufficient for selectable support.
- Guidance: Not selectable; use the wallet's own backup procedure.
- Version interval (min / max): 2f9d1bbb2c553dc75f3335bd1452117dfddd86fa / 2f9d1bbb2c553dc75f3335bd1452117dfddd86fa
- Verified on: 2026-09-29
- Historical: true
- Evidence: [monero-en-old-source](../catalog/evidence/monero-en-old-source.json), [monero-monero-license](../catalog/evidence/monero-monero-license.json), [monero-monero-rules](../catalog/evidence/monero-monero-rules.json), [monero-osi-bsd](../catalog/evidence/monero-osi-bsd.json), [monero-signpath](../catalog/evidence/monero-signpath.json)
- Evidence claim: Exact ordered dictionary array and applicable file-level license header reviewed. Source-token extraction and byte hashes are independently checked against the public fixture; no complete phrase is stored here. Reviewed 2026-09-29; response byte SHA-256 20c9090994c5b441f2e550cddbf266d604b64e495d9b172e45a8031e1aa5d578. See docs/research/batches/monero-polyseed.md.
- Evidence claim: BSD-3-Clause source-data redistribution allowed with exact copyright/license/disclaimer retention and no endorsement. File-level MIT overrides for dabura667 lists retained. Reviewed by Codex for this source-data payload only. Reviewed 2026-09-29; response byte SHA-256 1f99d6b6e1ae17de27147ff2e1e0238fa8c7d5a8accd0f1ac062c89365516abd. See docs/research/batches/monero-polyseed.md.
- Evidence claim: 1626 entries; codepoint prefixes and case-insensitive lookup. utf8canonical re-encodes codepoints with towlower, not NFC/NFKD. EnglishOld tolerates duplicate prefixes and short words. Reviewed 2026-09-29; response byte SHA-256 2bc256f01c6904af914cb7c6526254267ed463882e216fd0eb1d9bbdf4bf5bb4. See docs/research/batches/monero-polyseed.md.
- Evidence claim: OSI lists BSD-3-Clause as approved. This corroborates only the component-license decision, not project acceptance. Response-body SHA-256 0dfece33194f06d15b862c323f7ed32ba6ab7f512a7fda11880bb2e1401518f8.
- Evidence claim: Codex component assessment\: reviewed BSD-3-Clause/MIT and Apache-2.0\+MIT data licenses are OSI-approved and impose no commercial dual-licensing; notices are retained. Compatible for this data-only payload. Foundation acceptance, project eligibility and release signing remain unproven. Response-body SHA-256 6610cf889bbe0dc7533abaa310bc7a5cc9a61ae6c2ce0798a08109c925b46c51.
- Language: en
- Script: Latn
- Encoding: UTF-8
- Normalization: none
- Word count: 1626
- SHA-256: c8da327d316f8ee758b790068e618077ac271a89fd77ec1250c59ae40e7b599e
- Order rule: Exact upstream array order; zero-based indices. Extract literal UTF-8 tokens unchanged; remove C/C\+\+ wrapper and indentation, append LF after every token. No sorting, lowercasing or Unicode rewriting. Source file and extracted byte hashes in batch note.
- Position rules: Same vocabulary at every eligible position; upstream prefix length 4. Never evaluate a user phrase checksum.; Source-native lookup\: Unicode codepoint lowercase and language-specific prefix, with no NFC/NFKD transform; normalization=none preserves source characters.; Historical restore-only EnglishOld\: excluded from generation language list; duplicate prefixes and short words explicitly allowed by upstream.
- Source revision: 2f9d1bbb2c553dc75f3335bd1452117dfddd86fa
- License: BSD-3-Clause
- Attribution: Exact source file notices and upstream license retained in THIRD\_PARTY\_NOTICES; dabura667 / The Monero Project and original dictionary contributors.
- Repository redistribution: allowed
- SignPath compatibility: compatible
- License evidence: [monero-en-old-source](../catalog/evidence/monero-en-old-source.json), [monero-monero-license](../catalog/evidence/monero-monero-license.json), [monero-osi-bsd](../catalog/evidence/monero-osi-bsd.json), [monero-signpath](../catalog/evidence/monero-signpath.json)
- Test vectors: —

<a id="dictionary-monero-eo"></a>

### monero-eo — monero-eo

- Source record: [monero-eo](../catalog/dictionaries/monero-eo.json)
- Status: documented
- Reason: Evidence is insufficient for selectable support.
- Guidance: Not selectable; use the wallet's own backup procedure.
- Version interval (min / max): 2f9d1bbb2c553dc75f3335bd1452117dfddd86fa / 2f9d1bbb2c553dc75f3335bd1452117dfddd86fa
- Verified on: 2026-09-29
- Historical: false
- Evidence: [monero-eo-source](../catalog/evidence/monero-eo-source.json), [monero-monero-license](../catalog/evidence/monero-monero-license.json), [monero-monero-rules](../catalog/evidence/monero-monero-rules.json), [monero-osi-bsd](../catalog/evidence/monero-osi-bsd.json), [monero-signpath](../catalog/evidence/monero-signpath.json)
- Evidence claim: Exact ordered dictionary array and applicable file-level license header reviewed. Source-token extraction and byte hashes are independently checked against the public fixture; no complete phrase is stored here. Reviewed 2026-09-29; response byte SHA-256 382d9f9bfcf293e4dc9f156042fe5a3f2a151191bae368a494eaf53c77e16043. See docs/research/batches/monero-polyseed.md.
- Evidence claim: BSD-3-Clause source-data redistribution allowed with exact copyright/license/disclaimer retention and no endorsement. File-level MIT overrides for dabura667 lists retained. Reviewed by Codex for this source-data payload only. Reviewed 2026-09-29; response byte SHA-256 1f99d6b6e1ae17de27147ff2e1e0238fa8c7d5a8accd0f1ac062c89365516abd. See docs/research/batches/monero-polyseed.md.
- Evidence claim: 1626 entries; codepoint prefixes and case-insensitive lookup. utf8canonical re-encodes codepoints with towlower, not NFC/NFKD. EnglishOld tolerates duplicate prefixes and short words. Reviewed 2026-09-29; response byte SHA-256 2bc256f01c6904af914cb7c6526254267ed463882e216fd0eb1d9bbdf4bf5bb4. See docs/research/batches/monero-polyseed.md.
- Evidence claim: OSI lists BSD-3-Clause as approved. This corroborates only the component-license decision, not project acceptance. Response-body SHA-256 0dfece33194f06d15b862c323f7ed32ba6ab7f512a7fda11880bb2e1401518f8.
- Evidence claim: Codex component assessment\: reviewed BSD-3-Clause/MIT and Apache-2.0\+MIT data licenses are OSI-approved and impose no commercial dual-licensing; notices are retained. Compatible for this data-only payload. Foundation acceptance, project eligibility and release signing remain unproven. Response-body SHA-256 6610cf889bbe0dc7533abaa310bc7a5cc9a61ae6c2ce0798a08109c925b46c51.
- Language: eo
- Script: Latn
- Encoding: UTF-8
- Normalization: none
- Word count: 1626
- SHA-256: aa53b9b2af6586e8df69bcf04b17af4f06cac9e7ad20420d45b265f9aa18b32d
- Order rule: Exact upstream array order; zero-based indices. Extract literal UTF-8 tokens unchanged; remove C/C\+\+ wrapper and indentation, append LF after every token. No sorting, lowercasing or Unicode rewriting. Source file and extracted byte hashes in batch note.
- Position rules: Same vocabulary at every eligible position; upstream prefix length 4. Never evaluate a user phrase checksum.; Source-native lookup\: Unicode codepoint lowercase and language-specific prefix, with no NFC/NFKD transform; normalization=none preserves source characters.; Language coverage is not a wallet generation claim.
- Source revision: 2f9d1bbb2c553dc75f3335bd1452117dfddd86fa
- License: BSD-3-Clause
- Attribution: Exact source file notices and upstream license retained in THIRD\_PARTY\_NOTICES; dabura667 / The Monero Project and original dictionary contributors.
- Repository redistribution: allowed
- SignPath compatibility: compatible
- License evidence: [monero-eo-source](../catalog/evidence/monero-eo-source.json), [monero-monero-license](../catalog/evidence/monero-monero-license.json), [monero-osi-bsd](../catalog/evidence/monero-osi-bsd.json), [monero-signpath](../catalog/evidence/monero-signpath.json)
- Test vectors: —

<a id="dictionary-monero-es"></a>

### monero-es — monero-es

- Source record: [monero-es](../catalog/dictionaries/monero-es.json)
- Status: documented
- Reason: Evidence is insufficient for selectable support.
- Guidance: Not selectable; use the wallet's own backup procedure.
- Version interval (min / max): 2f9d1bbb2c553dc75f3335bd1452117dfddd86fa / 2f9d1bbb2c553dc75f3335bd1452117dfddd86fa
- Verified on: 2026-09-29
- Historical: false
- Evidence: [monero-es-source](../catalog/evidence/monero-es-source.json), [monero-monero-license](../catalog/evidence/monero-monero-license.json), [monero-monero-rules](../catalog/evidence/monero-monero-rules.json), [monero-osi-bsd](../catalog/evidence/monero-osi-bsd.json), [monero-osi-mit](../catalog/evidence/monero-osi-mit.json), [monero-signpath](../catalog/evidence/monero-signpath.json)
- Evidence claim: Exact ordered dictionary array and applicable file-level license header reviewed. Source-token extraction and byte hashes are independently checked against the public fixture; no complete phrase is stored here. Reviewed 2026-09-29; response byte SHA-256 994a941260f53e066753204f4b92c20bb1d830b58e76ff89c2caa71c34d546ef. See docs/research/batches/monero-polyseed.md.
- Evidence claim: BSD-3-Clause source-data redistribution allowed with exact copyright/license/disclaimer retention and no endorsement. File-level MIT overrides for dabura667 lists retained. Reviewed by Codex for this source-data payload only. Reviewed 2026-09-29; response byte SHA-256 1f99d6b6e1ae17de27147ff2e1e0238fa8c7d5a8accd0f1ac062c89365516abd. See docs/research/batches/monero-polyseed.md.
- Evidence claim: 1626 entries; codepoint prefixes and case-insensitive lookup. utf8canonical re-encodes codepoints with towlower, not NFC/NFKD. EnglishOld tolerates duplicate prefixes and short words. Reviewed 2026-09-29; response byte SHA-256 2bc256f01c6904af914cb7c6526254267ed463882e216fd0eb1d9bbdf4bf5bb4. See docs/research/batches/monero-polyseed.md.
- Evidence claim: OSI lists BSD-3-Clause as approved. This corroborates only the component-license decision, not project acceptance. Response-body SHA-256 0dfece33194f06d15b862c323f7ed32ba6ab7f512a7fda11880bb2e1401518f8.
- Evidence claim: OSI identifies MIT as an approved open-source license; this corroborates the local component assessment, while the pinned reference repository license supplies the actual permission. Reviewed 2026-09-29; byte SHA-256 004c79db0a335488afc87600d89f447dce7fb4d24d510af15ed4381a24be848c. See docs/research/batches/bip39-ton.md. Same-day review reused from Task 10; corroborates MIT file-level scope for these lists only.
- Evidence claim: Codex component assessment\: reviewed BSD-3-Clause/MIT and Apache-2.0\+MIT data licenses are OSI-approved and impose no commercial dual-licensing; notices are retained. Compatible for this data-only payload. Foundation acceptance, project eligibility and release signing remain unproven. Response-body SHA-256 6610cf889bbe0dc7533abaa310bc7a5cc9a61ae6c2ce0798a08109c925b46c51.
- Language: es
- Script: Latn
- Encoding: UTF-8
- Normalization: none
- Word count: 1626
- SHA-256: 05da8a20ae4a5af8fc1bd02d20d1282cf72ce1a6c98b9be60b1eff4c79d424fb
- Order rule: Exact upstream array order; zero-based indices. Extract literal UTF-8 tokens unchanged; remove C/C\+\+ wrapper and indentation, append LF after every token. No sorting, lowercasing or Unicode rewriting. Source file and extracted byte hashes in batch note.
- Position rules: Same vocabulary at every eligible position; upstream prefix length 4. Never evaluate a user phrase checksum.; Source-native lookup\: Unicode codepoint lowercase and language-specific prefix, with no NFC/NFKD transform; normalization=none preserves source characters.; Language coverage is not a wallet generation claim.
- Source revision: 2f9d1bbb2c553dc75f3335bd1452117dfddd86fa
- License: MIT
- Attribution: Exact source file notices and upstream license retained in THIRD\_PARTY\_NOTICES; dabura667 / The Monero Project and original dictionary contributors.
- Repository redistribution: allowed
- SignPath compatibility: compatible
- License evidence: [monero-es-source](../catalog/evidence/monero-es-source.json), [monero-monero-license](../catalog/evidence/monero-monero-license.json), [monero-osi-bsd](../catalog/evidence/monero-osi-bsd.json), [monero-osi-mit](../catalog/evidence/monero-osi-mit.json), [monero-signpath](../catalog/evidence/monero-signpath.json)
- Test vectors: —

<a id="dictionary-monero-fr"></a>

### monero-fr — monero-fr

- Source record: [monero-fr](../catalog/dictionaries/monero-fr.json)
- Status: documented
- Reason: Evidence is insufficient for selectable support.
- Guidance: Not selectable; use the wallet's own backup procedure.
- Version interval (min / max): 2f9d1bbb2c553dc75f3335bd1452117dfddd86fa / 2f9d1bbb2c553dc75f3335bd1452117dfddd86fa
- Verified on: 2026-09-29
- Historical: false
- Evidence: [monero-fr-source](../catalog/evidence/monero-fr-source.json), [monero-monero-license](../catalog/evidence/monero-monero-license.json), [monero-monero-rules](../catalog/evidence/monero-monero-rules.json), [monero-osi-bsd](../catalog/evidence/monero-osi-bsd.json), [monero-signpath](../catalog/evidence/monero-signpath.json)
- Evidence claim: Exact ordered dictionary array and applicable file-level license header reviewed. Source-token extraction and byte hashes are independently checked against the public fixture; no complete phrase is stored here. Reviewed 2026-09-29; response byte SHA-256 f4e42ab4eb9824a2cd829f132e33dfc46ae31c5788a37c9726d393e7cc809a82. See docs/research/batches/monero-polyseed.md.
- Evidence claim: BSD-3-Clause source-data redistribution allowed with exact copyright/license/disclaimer retention and no endorsement. File-level MIT overrides for dabura667 lists retained. Reviewed by Codex for this source-data payload only. Reviewed 2026-09-29; response byte SHA-256 1f99d6b6e1ae17de27147ff2e1e0238fa8c7d5a8accd0f1ac062c89365516abd. See docs/research/batches/monero-polyseed.md.
- Evidence claim: 1626 entries; codepoint prefixes and case-insensitive lookup. utf8canonical re-encodes codepoints with towlower, not NFC/NFKD. EnglishOld tolerates duplicate prefixes and short words. Reviewed 2026-09-29; response byte SHA-256 2bc256f01c6904af914cb7c6526254267ed463882e216fd0eb1d9bbdf4bf5bb4. See docs/research/batches/monero-polyseed.md.
- Evidence claim: OSI lists BSD-3-Clause as approved. This corroborates only the component-license decision, not project acceptance. Response-body SHA-256 0dfece33194f06d15b862c323f7ed32ba6ab7f512a7fda11880bb2e1401518f8.
- Evidence claim: Codex component assessment\: reviewed BSD-3-Clause/MIT and Apache-2.0\+MIT data licenses are OSI-approved and impose no commercial dual-licensing; notices are retained. Compatible for this data-only payload. Foundation acceptance, project eligibility and release signing remain unproven. Response-body SHA-256 6610cf889bbe0dc7533abaa310bc7a5cc9a61ae6c2ce0798a08109c925b46c51.
- Language: fr
- Script: Latn
- Encoding: UTF-8
- Normalization: none
- Word count: 1626
- SHA-256: b17376bb1341cc32b8a7088d23c0dba3b25743c167f4e4f3d8062946ffd93e87
- Order rule: Exact upstream array order; zero-based indices. Extract literal UTF-8 tokens unchanged; remove C/C\+\+ wrapper and indentation, append LF after every token. No sorting, lowercasing or Unicode rewriting. Source file and extracted byte hashes in batch note.
- Position rules: Same vocabulary at every eligible position; upstream prefix length 4. Never evaluate a user phrase checksum.; Source-native lookup\: Unicode codepoint lowercase and language-specific prefix, with no NFC/NFKD transform; normalization=none preserves source characters.; Language coverage is not a wallet generation claim.
- Source revision: 2f9d1bbb2c553dc75f3335bd1452117dfddd86fa
- License: BSD-3-Clause
- Attribution: Exact source file notices and upstream license retained in THIRD\_PARTY\_NOTICES; dabura667 / The Monero Project and original dictionary contributors.
- Repository redistribution: allowed
- SignPath compatibility: compatible
- License evidence: [monero-fr-source](../catalog/evidence/monero-fr-source.json), [monero-monero-license](../catalog/evidence/monero-monero-license.json), [monero-osi-bsd](../catalog/evidence/monero-osi-bsd.json), [monero-signpath](../catalog/evidence/monero-signpath.json)
- Test vectors: —

<a id="dictionary-monero-it"></a>

### monero-it — monero-it

- Source record: [monero-it](../catalog/dictionaries/monero-it.json)
- Status: documented
- Reason: Evidence is insufficient for selectable support.
- Guidance: Not selectable; use the wallet's own backup procedure.
- Version interval (min / max): 2f9d1bbb2c553dc75f3335bd1452117dfddd86fa / 2f9d1bbb2c553dc75f3335bd1452117dfddd86fa
- Verified on: 2026-09-29
- Historical: false
- Evidence: [monero-it-source](../catalog/evidence/monero-it-source.json), [monero-monero-license](../catalog/evidence/monero-monero-license.json), [monero-monero-rules](../catalog/evidence/monero-monero-rules.json), [monero-osi-bsd](../catalog/evidence/monero-osi-bsd.json), [monero-signpath](../catalog/evidence/monero-signpath.json)
- Evidence claim: Exact ordered dictionary array and applicable file-level license header reviewed. Source-token extraction and byte hashes are independently checked against the public fixture; no complete phrase is stored here. Reviewed 2026-09-29; response byte SHA-256 d02956b528db827646a1f6f78c1a19716b9334985cb893eb09409834a04045db. See docs/research/batches/monero-polyseed.md.
- Evidence claim: BSD-3-Clause source-data redistribution allowed with exact copyright/license/disclaimer retention and no endorsement. File-level MIT overrides for dabura667 lists retained. Reviewed by Codex for this source-data payload only. Reviewed 2026-09-29; response byte SHA-256 1f99d6b6e1ae17de27147ff2e1e0238fa8c7d5a8accd0f1ac062c89365516abd. See docs/research/batches/monero-polyseed.md.
- Evidence claim: 1626 entries; codepoint prefixes and case-insensitive lookup. utf8canonical re-encodes codepoints with towlower, not NFC/NFKD. EnglishOld tolerates duplicate prefixes and short words. Reviewed 2026-09-29; response byte SHA-256 2bc256f01c6904af914cb7c6526254267ed463882e216fd0eb1d9bbdf4bf5bb4. See docs/research/batches/monero-polyseed.md.
- Evidence claim: OSI lists BSD-3-Clause as approved. This corroborates only the component-license decision, not project acceptance. Response-body SHA-256 0dfece33194f06d15b862c323f7ed32ba6ab7f512a7fda11880bb2e1401518f8.
- Evidence claim: Codex component assessment\: reviewed BSD-3-Clause/MIT and Apache-2.0\+MIT data licenses are OSI-approved and impose no commercial dual-licensing; notices are retained. Compatible for this data-only payload. Foundation acceptance, project eligibility and release signing remain unproven. Response-body SHA-256 6610cf889bbe0dc7533abaa310bc7a5cc9a61ae6c2ce0798a08109c925b46c51.
- Language: it
- Script: Latn
- Encoding: UTF-8
- Normalization: none
- Word count: 1626
- SHA-256: aea041cbb43e8e3b817b48b64001df3e28949002d99c920a8a46231319bcc121
- Order rule: Exact upstream array order; zero-based indices. Extract literal UTF-8 tokens unchanged; remove C/C\+\+ wrapper and indentation, append LF after every token. No sorting, lowercasing or Unicode rewriting. Source file and extracted byte hashes in batch note.
- Position rules: Same vocabulary at every eligible position; upstream prefix length 4. Never evaluate a user phrase checksum.; Source-native lookup\: Unicode codepoint lowercase and language-specific prefix, with no NFC/NFKD transform; normalization=none preserves source characters.; Language coverage is not a wallet generation claim.
- Source revision: 2f9d1bbb2c553dc75f3335bd1452117dfddd86fa
- License: BSD-3-Clause
- Attribution: Exact source file notices and upstream license retained in THIRD\_PARTY\_NOTICES; dabura667 / The Monero Project and original dictionary contributors.
- Repository redistribution: allowed
- SignPath compatibility: compatible
- License evidence: [monero-it-source](../catalog/evidence/monero-it-source.json), [monero-monero-license](../catalog/evidence/monero-monero-license.json), [monero-osi-bsd](../catalog/evidence/monero-osi-bsd.json), [monero-signpath](../catalog/evidence/monero-signpath.json)
- Test vectors: —

<a id="dictionary-monero-ja"></a>

### monero-ja — monero-ja

- Source record: [monero-ja](../catalog/dictionaries/monero-ja.json)
- Status: documented
- Reason: Evidence is insufficient for selectable support.
- Guidance: Not selectable; use the wallet's own backup procedure.
- Version interval (min / max): 2f9d1bbb2c553dc75f3335bd1452117dfddd86fa / 2f9d1bbb2c553dc75f3335bd1452117dfddd86fa
- Verified on: 2026-09-29
- Historical: false
- Evidence: [monero-ja-source](../catalog/evidence/monero-ja-source.json), [monero-monero-license](../catalog/evidence/monero-monero-license.json), [monero-monero-rules](../catalog/evidence/monero-monero-rules.json), [monero-osi-bsd](../catalog/evidence/monero-osi-bsd.json), [monero-osi-mit](../catalog/evidence/monero-osi-mit.json), [monero-signpath](../catalog/evidence/monero-signpath.json)
- Evidence claim: Exact ordered dictionary array and applicable file-level license header reviewed. Source-token extraction and byte hashes are independently checked against the public fixture; no complete phrase is stored here. Reviewed 2026-09-29; response byte SHA-256 3701f067006b60e95e266e7a385b472c5bddeb6f476e737eed6d3b7febefe6d5. See docs/research/batches/monero-polyseed.md.
- Evidence claim: BSD-3-Clause source-data redistribution allowed with exact copyright/license/disclaimer retention and no endorsement. File-level MIT overrides for dabura667 lists retained. Reviewed by Codex for this source-data payload only. Reviewed 2026-09-29; response byte SHA-256 1f99d6b6e1ae17de27147ff2e1e0238fa8c7d5a8accd0f1ac062c89365516abd. See docs/research/batches/monero-polyseed.md.
- Evidence claim: 1626 entries; codepoint prefixes and case-insensitive lookup. utf8canonical re-encodes codepoints with towlower, not NFC/NFKD. EnglishOld tolerates duplicate prefixes and short words. Reviewed 2026-09-29; response byte SHA-256 2bc256f01c6904af914cb7c6526254267ed463882e216fd0eb1d9bbdf4bf5bb4. See docs/research/batches/monero-polyseed.md.
- Evidence claim: OSI lists BSD-3-Clause as approved. This corroborates only the component-license decision, not project acceptance. Response-body SHA-256 0dfece33194f06d15b862c323f7ed32ba6ab7f512a7fda11880bb2e1401518f8.
- Evidence claim: OSI identifies MIT as an approved open-source license; this corroborates the local component assessment, while the pinned reference repository license supplies the actual permission. Reviewed 2026-09-29; byte SHA-256 004c79db0a335488afc87600d89f447dce7fb4d24d510af15ed4381a24be848c. See docs/research/batches/bip39-ton.md. Same-day review reused from Task 10; corroborates MIT file-level scope for these lists only.
- Evidence claim: Codex component assessment\: reviewed BSD-3-Clause/MIT and Apache-2.0\+MIT data licenses are OSI-approved and impose no commercial dual-licensing; notices are retained. Compatible for this data-only payload. Foundation acceptance, project eligibility and release signing remain unproven. Response-body SHA-256 6610cf889bbe0dc7533abaa310bc7a5cc9a61ae6c2ce0798a08109c925b46c51.
- Language: ja
- Script: Jpan
- Encoding: UTF-8
- Normalization: none
- Word count: 1626
- SHA-256: 0e879f11f3806e6b25738598cfec6f372364af7fb8c59b4874d7a406f6b0fee7
- Order rule: Exact upstream array order; zero-based indices. Extract literal UTF-8 tokens unchanged; remove C/C\+\+ wrapper and indentation, append LF after every token. No sorting, lowercasing or Unicode rewriting. Source file and extracted byte hashes in batch note.
- Position rules: Same vocabulary at every eligible position; upstream prefix length 3. Never evaluate a user phrase checksum.; Source-native lookup\: Unicode codepoint lowercase and language-specific prefix, with no NFC/NFKD transform; normalization=none preserves source characters.; Language coverage is not a wallet generation claim.
- Source revision: 2f9d1bbb2c553dc75f3335bd1452117dfddd86fa
- License: MIT
- Attribution: Exact source file notices and upstream license retained in THIRD\_PARTY\_NOTICES; dabura667 / The Monero Project and original dictionary contributors.
- Repository redistribution: allowed
- SignPath compatibility: compatible
- License evidence: [monero-ja-source](../catalog/evidence/monero-ja-source.json), [monero-monero-license](../catalog/evidence/monero-monero-license.json), [monero-osi-bsd](../catalog/evidence/monero-osi-bsd.json), [monero-osi-mit](../catalog/evidence/monero-osi-mit.json), [monero-signpath](../catalog/evidence/monero-signpath.json)
- Test vectors: —

<a id="dictionary-monero-jbo"></a>

### monero-jbo — monero-jbo

- Source record: [monero-jbo](../catalog/dictionaries/monero-jbo.json)
- Status: documented
- Reason: Evidence is insufficient for selectable support.
- Guidance: Not selectable; use the wallet's own backup procedure.
- Version interval (min / max): 2f9d1bbb2c553dc75f3335bd1452117dfddd86fa / 2f9d1bbb2c553dc75f3335bd1452117dfddd86fa
- Verified on: 2026-09-29
- Historical: false
- Evidence: [monero-jbo-source](../catalog/evidence/monero-jbo-source.json), [monero-monero-license](../catalog/evidence/monero-monero-license.json), [monero-monero-rules](../catalog/evidence/monero-monero-rules.json), [monero-osi-bsd](../catalog/evidence/monero-osi-bsd.json), [monero-signpath](../catalog/evidence/monero-signpath.json)
- Evidence claim: Exact ordered dictionary array and applicable file-level license header reviewed. Source-token extraction and byte hashes are independently checked against the public fixture; no complete phrase is stored here. Reviewed 2026-09-29; response byte SHA-256 6c84dedd2609060f30368b92b5e377207e28afcda5401b5060d57c633e623a04. See docs/research/batches/monero-polyseed.md.
- Evidence claim: BSD-3-Clause source-data redistribution allowed with exact copyright/license/disclaimer retention and no endorsement. File-level MIT overrides for dabura667 lists retained. Reviewed by Codex for this source-data payload only. Reviewed 2026-09-29; response byte SHA-256 1f99d6b6e1ae17de27147ff2e1e0238fa8c7d5a8accd0f1ac062c89365516abd. See docs/research/batches/monero-polyseed.md.
- Evidence claim: 1626 entries; codepoint prefixes and case-insensitive lookup. utf8canonical re-encodes codepoints with towlower, not NFC/NFKD. EnglishOld tolerates duplicate prefixes and short words. Reviewed 2026-09-29; response byte SHA-256 2bc256f01c6904af914cb7c6526254267ed463882e216fd0eb1d9bbdf4bf5bb4. See docs/research/batches/monero-polyseed.md.
- Evidence claim: OSI lists BSD-3-Clause as approved. This corroborates only the component-license decision, not project acceptance. Response-body SHA-256 0dfece33194f06d15b862c323f7ed32ba6ab7f512a7fda11880bb2e1401518f8.
- Evidence claim: Codex component assessment\: reviewed BSD-3-Clause/MIT and Apache-2.0\+MIT data licenses are OSI-approved and impose no commercial dual-licensing; notices are retained. Compatible for this data-only payload. Foundation acceptance, project eligibility and release signing remain unproven. Response-body SHA-256 6610cf889bbe0dc7533abaa310bc7a5cc9a61ae6c2ce0798a08109c925b46c51.
- Language: jbo
- Script: Latn
- Encoding: UTF-8
- Normalization: none
- Word count: 1626
- SHA-256: 19c3f71b26c808bbe9ed7ab944ac1c8b1f11307f96d27d01874c093520c972f9
- Order rule: Exact upstream array order; zero-based indices. Extract literal UTF-8 tokens unchanged; remove C/C\+\+ wrapper and indentation, append LF after every token. No sorting, lowercasing or Unicode rewriting. Source file and extracted byte hashes in batch note.
- Position rules: Same vocabulary at every eligible position; upstream prefix length 4. Never evaluate a user phrase checksum.; Source-native lookup\: Unicode codepoint lowercase and language-specific prefix, with no NFC/NFKD transform; normalization=none preserves source characters.; Language coverage is not a wallet generation claim.
- Source revision: 2f9d1bbb2c553dc75f3335bd1452117dfddd86fa
- License: BSD-3-Clause
- Attribution: Exact source file notices and upstream license retained in THIRD\_PARTY\_NOTICES; dabura667 / The Monero Project and original dictionary contributors.
- Repository redistribution: allowed
- SignPath compatibility: compatible
- License evidence: [monero-jbo-source](../catalog/evidence/monero-jbo-source.json), [monero-monero-license](../catalog/evidence/monero-monero-license.json), [monero-osi-bsd](../catalog/evidence/monero-osi-bsd.json), [monero-signpath](../catalog/evidence/monero-signpath.json)
- Test vectors: —

<a id="dictionary-monero-nl"></a>

### monero-nl — monero-nl

- Source record: [monero-nl](../catalog/dictionaries/monero-nl.json)
- Status: documented
- Reason: Evidence is insufficient for selectable support.
- Guidance: Not selectable; use the wallet's own backup procedure.
- Version interval (min / max): 2f9d1bbb2c553dc75f3335bd1452117dfddd86fa / 2f9d1bbb2c553dc75f3335bd1452117dfddd86fa
- Verified on: 2026-09-29
- Historical: false
- Evidence: [monero-monero-license](../catalog/evidence/monero-monero-license.json), [monero-monero-rules](../catalog/evidence/monero-monero-rules.json), [monero-nl-source](../catalog/evidence/monero-nl-source.json), [monero-osi-bsd](../catalog/evidence/monero-osi-bsd.json), [monero-signpath](../catalog/evidence/monero-signpath.json)
- Evidence claim: BSD-3-Clause source-data redistribution allowed with exact copyright/license/disclaimer retention and no endorsement. File-level MIT overrides for dabura667 lists retained. Reviewed by Codex for this source-data payload only. Reviewed 2026-09-29; response byte SHA-256 1f99d6b6e1ae17de27147ff2e1e0238fa8c7d5a8accd0f1ac062c89365516abd. See docs/research/batches/monero-polyseed.md.
- Evidence claim: 1626 entries; codepoint prefixes and case-insensitive lookup. utf8canonical re-encodes codepoints with towlower, not NFC/NFKD. EnglishOld tolerates duplicate prefixes and short words. Reviewed 2026-09-29; response byte SHA-256 2bc256f01c6904af914cb7c6526254267ed463882e216fd0eb1d9bbdf4bf5bb4. See docs/research/batches/monero-polyseed.md.
- Evidence claim: Exact ordered dictionary array and applicable file-level license header reviewed. Source-token extraction and byte hashes are independently checked against the public fixture; no complete phrase is stored here. Reviewed 2026-09-29; response byte SHA-256 775d05f737f453d6798876d99961bb3bcfc49d47cb57860d3c0b2a03b9a64822. See docs/research/batches/monero-polyseed.md.
- Evidence claim: OSI lists BSD-3-Clause as approved. This corroborates only the component-license decision, not project acceptance. Response-body SHA-256 0dfece33194f06d15b862c323f7ed32ba6ab7f512a7fda11880bb2e1401518f8.
- Evidence claim: Codex component assessment\: reviewed BSD-3-Clause/MIT and Apache-2.0\+MIT data licenses are OSI-approved and impose no commercial dual-licensing; notices are retained. Compatible for this data-only payload. Foundation acceptance, project eligibility and release signing remain unproven. Response-body SHA-256 6610cf889bbe0dc7533abaa310bc7a5cc9a61ae6c2ce0798a08109c925b46c51.
- Language: nl
- Script: Latn
- Encoding: UTF-8
- Normalization: none
- Word count: 1626
- SHA-256: 9b2005b2c4d95360361949c7f5b43ef6a021d3ce31f01f6101a24d93540e790a
- Order rule: Exact upstream array order; zero-based indices. Extract literal UTF-8 tokens unchanged; remove C/C\+\+ wrapper and indentation, append LF after every token. No sorting, lowercasing or Unicode rewriting. Source file and extracted byte hashes in batch note.
- Position rules: Same vocabulary at every eligible position; upstream prefix length 4. Never evaluate a user phrase checksum.; Source-native lookup\: Unicode codepoint lowercase and language-specific prefix, with no NFC/NFKD transform; normalization=none preserves source characters.; Language coverage is not a wallet generation claim.
- Source revision: 2f9d1bbb2c553dc75f3335bd1452117dfddd86fa
- License: BSD-3-Clause
- Attribution: Exact source file notices and upstream license retained in THIRD\_PARTY\_NOTICES; dabura667 / The Monero Project and original dictionary contributors.
- Repository redistribution: allowed
- SignPath compatibility: compatible
- License evidence: [monero-monero-license](../catalog/evidence/monero-monero-license.json), [monero-nl-source](../catalog/evidence/monero-nl-source.json), [monero-osi-bsd](../catalog/evidence/monero-osi-bsd.json), [monero-signpath](../catalog/evidence/monero-signpath.json)
- Test vectors: —

<a id="dictionary-monero-pt"></a>

### monero-pt — monero-pt

- Source record: [monero-pt](../catalog/dictionaries/monero-pt.json)
- Status: verified
- Reason: Verified research record; not a release or security guarantee.
- Version interval (min / max): 2f9d1bbb2c553dc75f3335bd1452117dfddd86fa / 2f9d1bbb2c553dc75f3335bd1452117dfddd86fa
- Verified on: 2026-09-29
- Historical: false
- Evidence: [monero-legacy-vectors](../catalog/evidence/monero-legacy-vectors.json), [monero-monero-license](../catalog/evidence/monero-monero-license.json), [monero-monero-rules](../catalog/evidence/monero-monero-rules.json), [monero-osi-bsd](../catalog/evidence/monero-osi-bsd.json), [monero-osi-mit](../catalog/evidence/monero-osi-mit.json), [monero-pt-source](../catalog/evidence/monero-pt-source.json), [monero-signpath](../catalog/evidence/monero-signpath.json)
- Evidence claim: Public Portuguese checksum and German case-tolerance examples; projection stores dictionary indices and expected phrase fingerprint. Offline test reproduces source CRC32 prefix check, not private-key/address derivation. Reviewed 2026-09-29; response byte SHA-256 520fec49e96e4b01d472f627e109b7a343f80e58291eed793f7ca76f2e63a1d1. See docs/research/batches/monero-polyseed.md.
- Evidence claim: BSD-3-Clause source-data redistribution allowed with exact copyright/license/disclaimer retention and no endorsement. File-level MIT overrides for dabura667 lists retained. Reviewed by Codex for this source-data payload only. Reviewed 2026-09-29; response byte SHA-256 1f99d6b6e1ae17de27147ff2e1e0238fa8c7d5a8accd0f1ac062c89365516abd. See docs/research/batches/monero-polyseed.md.
- Evidence claim: 1626 entries; codepoint prefixes and case-insensitive lookup. utf8canonical re-encodes codepoints with towlower, not NFC/NFKD. EnglishOld tolerates duplicate prefixes and short words. Reviewed 2026-09-29; response byte SHA-256 2bc256f01c6904af914cb7c6526254267ed463882e216fd0eb1d9bbdf4bf5bb4. See docs/research/batches/monero-polyseed.md.
- Evidence claim: OSI lists BSD-3-Clause as approved. This corroborates only the component-license decision, not project acceptance. Response-body SHA-256 0dfece33194f06d15b862c323f7ed32ba6ab7f512a7fda11880bb2e1401518f8.
- Evidence claim: OSI identifies MIT as an approved open-source license; this corroborates the local component assessment, while the pinned reference repository license supplies the actual permission. Reviewed 2026-09-29; byte SHA-256 004c79db0a335488afc87600d89f447dce7fb4d24d510af15ed4381a24be848c. See docs/research/batches/bip39-ton.md. Same-day review reused from Task 10; corroborates MIT file-level scope for these lists only.
- Evidence claim: Exact ordered dictionary array and applicable file-level license header reviewed. Source-token extraction and byte hashes are independently checked against the public fixture; no complete phrase is stored here. Reviewed 2026-09-29; response byte SHA-256 0a6b191930a29f1ae827c1f5f8905548035bac5e5b41386f0978cf39e4adcfa1. See docs/research/batches/monero-polyseed.md.
- Evidence claim: Codex component assessment\: reviewed BSD-3-Clause/MIT and Apache-2.0\+MIT data licenses are OSI-approved and impose no commercial dual-licensing; notices are retained. Compatible for this data-only payload. Foundation acceptance, project eligibility and release signing remain unproven. Response-body SHA-256 6610cf889bbe0dc7533abaa310bc7a5cc9a61ae6c2ce0798a08109c925b46c51.
- Language: pt
- Script: Latn
- Encoding: UTF-8
- Normalization: none
- Word count: 1626
- SHA-256: 9099aaa5470c568ca91f0040222760af55720ddc3f3a6f9e1736d4c2dd9247da
- Order rule: Exact upstream array order; zero-based indices. Extract literal UTF-8 tokens unchanged; remove C/C\+\+ wrapper and indentation, append LF after every token. No sorting, lowercasing or Unicode rewriting. Source file and extracted byte hashes in batch note.
- Position rules: Same vocabulary at every eligible position; upstream prefix length 4. Never evaluate a user phrase checksum.; Source-native lookup\: Unicode codepoint lowercase and language-specific prefix, with no NFC/NFKD transform; normalization=none preserves source characters.; Language coverage is not a wallet generation claim.
- Source revision: 2f9d1bbb2c553dc75f3335bd1452117dfddd86fa
- License: MIT
- Attribution: Exact source file notices and upstream license retained in THIRD\_PARTY\_NOTICES; dabura667 / The Monero Project and original dictionary contributors.
- Repository redistribution: allowed
- SignPath compatibility: compatible
- License evidence: [monero-monero-license](../catalog/evidence/monero-monero-license.json), [monero-osi-bsd](../catalog/evidence/monero-osi-bsd.json), [monero-osi-mit](../catalog/evidence/monero-osi-mit.json), [monero-pt-source](../catalog/evidence/monero-pt-source.json), [monero-signpath](../catalog/evidence/monero-signpath.json)
- Test vectors: [monero-legacy-vectors](../catalog/evidence/monero-legacy-vectors.json)

<a id="dictionary-monero-ru"></a>

### monero-ru — monero-ru

- Source record: [monero-ru](../catalog/dictionaries/monero-ru.json)
- Status: documented
- Reason: Evidence is insufficient for selectable support.
- Guidance: Not selectable; use the wallet's own backup procedure.
- Version interval (min / max): 2f9d1bbb2c553dc75f3335bd1452117dfddd86fa / 2f9d1bbb2c553dc75f3335bd1452117dfddd86fa
- Verified on: 2026-09-29
- Historical: false
- Evidence: [monero-monero-license](../catalog/evidence/monero-monero-license.json), [monero-monero-rules](../catalog/evidence/monero-monero-rules.json), [monero-osi-bsd](../catalog/evidence/monero-osi-bsd.json), [monero-ru-source](../catalog/evidence/monero-ru-source.json), [monero-signpath](../catalog/evidence/monero-signpath.json)
- Evidence claim: BSD-3-Clause source-data redistribution allowed with exact copyright/license/disclaimer retention and no endorsement. File-level MIT overrides for dabura667 lists retained. Reviewed by Codex for this source-data payload only. Reviewed 2026-09-29; response byte SHA-256 1f99d6b6e1ae17de27147ff2e1e0238fa8c7d5a8accd0f1ac062c89365516abd. See docs/research/batches/monero-polyseed.md.
- Evidence claim: 1626 entries; codepoint prefixes and case-insensitive lookup. utf8canonical re-encodes codepoints with towlower, not NFC/NFKD. EnglishOld tolerates duplicate prefixes and short words. Reviewed 2026-09-29; response byte SHA-256 2bc256f01c6904af914cb7c6526254267ed463882e216fd0eb1d9bbdf4bf5bb4. See docs/research/batches/monero-polyseed.md.
- Evidence claim: OSI lists BSD-3-Clause as approved. This corroborates only the component-license decision, not project acceptance. Response-body SHA-256 0dfece33194f06d15b862c323f7ed32ba6ab7f512a7fda11880bb2e1401518f8.
- Evidence claim: Exact ordered dictionary array and applicable file-level license header reviewed. Source-token extraction and byte hashes are independently checked against the public fixture; no complete phrase is stored here. Reviewed 2026-09-29; response byte SHA-256 2d3f282d11e917fcdd6248b87002f5b982b6abaa773e9676d21886b6a50a4762. See docs/research/batches/monero-polyseed.md.
- Evidence claim: Codex component assessment\: reviewed BSD-3-Clause/MIT and Apache-2.0\+MIT data licenses are OSI-approved and impose no commercial dual-licensing; notices are retained. Compatible for this data-only payload. Foundation acceptance, project eligibility and release signing remain unproven. Response-body SHA-256 6610cf889bbe0dc7533abaa310bc7a5cc9a61ae6c2ce0798a08109c925b46c51.
- Language: ru
- Script: Cyrl
- Encoding: UTF-8
- Normalization: none
- Word count: 1626
- SHA-256: fd225689dda9d342acae6bd58ecbdba3274ded07d89936ce979a95f6d60c64ea
- Order rule: Exact upstream array order; zero-based indices. Extract literal UTF-8 tokens unchanged; remove C/C\+\+ wrapper and indentation, append LF after every token. No sorting, lowercasing or Unicode rewriting. Source file and extracted byte hashes in batch note.
- Position rules: Same vocabulary at every eligible position; upstream prefix length 4. Never evaluate a user phrase checksum.; Source-native lookup\: Unicode codepoint lowercase and language-specific prefix, with no NFC/NFKD transform; normalization=none preserves source characters.; Language coverage is not a wallet generation claim.
- Source revision: 2f9d1bbb2c553dc75f3335bd1452117dfddd86fa
- License: BSD-3-Clause
- Attribution: Exact source file notices and upstream license retained in THIRD\_PARTY\_NOTICES; dabura667 / The Monero Project and original dictionary contributors.
- Repository redistribution: allowed
- SignPath compatibility: compatible
- License evidence: [monero-monero-license](../catalog/evidence/monero-monero-license.json), [monero-osi-bsd](../catalog/evidence/monero-osi-bsd.json), [monero-ru-source](../catalog/evidence/monero-ru-source.json), [monero-signpath](../catalog/evidence/monero-signpath.json)
- Test vectors: —

<a id="dictionary-monero-zh-hans"></a>

### monero-zh-hans — monero-zh-hans

- Source record: [monero-zh-hans](../catalog/dictionaries/monero-zh-hans.json)
- Status: documented
- Reason: Evidence is insufficient for selectable support.
- Guidance: Not selectable; use the wallet's own backup procedure.
- Version interval (min / max): 2f9d1bbb2c553dc75f3335bd1452117dfddd86fa / 2f9d1bbb2c553dc75f3335bd1452117dfddd86fa
- Verified on: 2026-09-29
- Historical: false
- Evidence: [monero-monero-license](../catalog/evidence/monero-monero-license.json), [monero-monero-rules](../catalog/evidence/monero-monero-rules.json), [monero-osi-bsd](../catalog/evidence/monero-osi-bsd.json), [monero-osi-mit](../catalog/evidence/monero-osi-mit.json), [monero-signpath](../catalog/evidence/monero-signpath.json), [monero-zh-hans-source](../catalog/evidence/monero-zh-hans-source.json)
- Evidence claim: BSD-3-Clause source-data redistribution allowed with exact copyright/license/disclaimer retention and no endorsement. File-level MIT overrides for dabura667 lists retained. Reviewed by Codex for this source-data payload only. Reviewed 2026-09-29; response byte SHA-256 1f99d6b6e1ae17de27147ff2e1e0238fa8c7d5a8accd0f1ac062c89365516abd. See docs/research/batches/monero-polyseed.md.
- Evidence claim: 1626 entries; codepoint prefixes and case-insensitive lookup. utf8canonical re-encodes codepoints with towlower, not NFC/NFKD. EnglishOld tolerates duplicate prefixes and short words. Reviewed 2026-09-29; response byte SHA-256 2bc256f01c6904af914cb7c6526254267ed463882e216fd0eb1d9bbdf4bf5bb4. See docs/research/batches/monero-polyseed.md.
- Evidence claim: OSI lists BSD-3-Clause as approved. This corroborates only the component-license decision, not project acceptance. Response-body SHA-256 0dfece33194f06d15b862c323f7ed32ba6ab7f512a7fda11880bb2e1401518f8.
- Evidence claim: OSI identifies MIT as an approved open-source license; this corroborates the local component assessment, while the pinned reference repository license supplies the actual permission. Reviewed 2026-09-29; byte SHA-256 004c79db0a335488afc87600d89f447dce7fb4d24d510af15ed4381a24be848c. See docs/research/batches/bip39-ton.md. Same-day review reused from Task 10; corroborates MIT file-level scope for these lists only.
- Evidence claim: Codex component assessment\: reviewed BSD-3-Clause/MIT and Apache-2.0\+MIT data licenses are OSI-approved and impose no commercial dual-licensing; notices are retained. Compatible for this data-only payload. Foundation acceptance, project eligibility and release signing remain unproven. Response-body SHA-256 6610cf889bbe0dc7533abaa310bc7a5cc9a61ae6c2ce0798a08109c925b46c51.
- Evidence claim: Exact ordered dictionary array and applicable file-level license header reviewed. Source-token extraction and byte hashes are independently checked against the public fixture; no complete phrase is stored here. Reviewed 2026-09-29; response byte SHA-256 4a38fbe7279616aa78aa11dbcf425d0ba5305fd2089cb4421d544f2c540d50fd. See docs/research/batches/monero-polyseed.md.
- Language: zh-hans
- Script: Hans
- Encoding: UTF-8
- Normalization: none
- Word count: 1626
- SHA-256: d0b846b2036f55182892d98c2410996c399ed3aee5be2d6cbfaf594e599dd522
- Order rule: Exact upstream array order; zero-based indices. Extract literal UTF-8 tokens unchanged; remove C/C\+\+ wrapper and indentation, append LF after every token. No sorting, lowercasing or Unicode rewriting. Source file and extracted byte hashes in batch note.
- Position rules: Same vocabulary at every eligible position; upstream prefix length 1. Never evaluate a user phrase checksum.; Source-native lookup\: Unicode codepoint lowercase and language-specific prefix, with no NFC/NFKD transform; normalization=none preserves source characters.; Language coverage is not a wallet generation claim.
- Source revision: 2f9d1bbb2c553dc75f3335bd1452117dfddd86fa
- License: MIT
- Attribution: Exact source file notices and upstream license retained in THIRD\_PARTY\_NOTICES; dabura667 / The Monero Project and original dictionary contributors.
- Repository redistribution: allowed
- SignPath compatibility: compatible
- License evidence: [monero-monero-license](../catalog/evidence/monero-monero-license.json), [monero-osi-bsd](../catalog/evidence/monero-osi-bsd.json), [monero-osi-mit](../catalog/evidence/monero-osi-mit.json), [monero-signpath](../catalog/evidence/monero-signpath.json), [monero-zh-hans-source](../catalog/evidence/monero-zh-hans-source.json)
- Test vectors: —

<a id="dictionary-pgp-even"></a>

### Decred PGP — even positions \(zero-based\) — pgp-even

- Source record: [pgp-even](../catalog/dictionaries/pgp-even.json)
- Status: verified
- Reason: Verified research record; not a release or security guarantee.
- Version interval (min / max): c0fee6b52ad30961cfc3e06017d5e7516952615e / c0fee6b52ad30961cfc3e06017d5e7516952615e
- Verified on: 2026-09-29
- Historical: false
- Evidence: [decred-decrediton-license](../catalog/evidence/decred-decrediton-license.json), [decred-pgp-license](../catalog/evidence/decred-pgp-license.json), [decred-pgp-list](../catalog/evidence/decred-pgp-list.json), [decred-pgp-osi](../catalog/evidence/decred-pgp-osi.json), [decred-pgp-position](../catalog/evidence/decred-pgp-position.json), [decred-pgp-signpath](../catalog/evidence/decred-pgp-signpath.json), [decred-pgp-vectors](../catalog/evidence/decred-pgp-vectors.json), [decred-pgp33-reference](../catalog/evidence/decred-pgp33-reference.json)
- Evidence claim: ISC notice retained for modified synthetic output projections from the official Decrediton encoder. No implementation/library or wallet binary bundled.
- Evidence claim: Reviewed 2026-09-29\: root ISC and explicit ISC wordlist header permit these two modified list projections with complete original notices retained. Redistribution allowed. Local component signing compatibility assessed separately; no project acceptance.
- Evidence claim: ISC-licensed alternatingWords literal contains 512 words\: index 2\*b even half, 2\*b\+1 odd half; exact source case retained. UTF-8 LF projection with final LF, no sorting.
- Evidence claim: OSI identifies ISC as an approved license; actual grant and scope are supplied by pinned Decred source/header. Component compatibility only.
- Evidence claim: ByteToMnemonic selects half by zero-based position, not byte parity. DecodeMnemonics rejects wrong-position half and compares words case-insensitively.
- Evidence claim: Reviewed 2026-09-29\: OSS terms require OSI-approved licensing across components. Exact ISC list projections with notices satisfy local component licensing assessment; this is not Foundation acceptance or signing/release approval.
- Evidence claim: Public known-answer mnemonicTests cover 20- and 31-byte seeds; fixed expected words project to indices/fingerprints and corroborate ordering/checksum. They are not mislabeled 33-word examples.
- Evidence claim: Reviewed pinned independent official JavaScript encodeMnemonic produces expected 33-word outputs for synthetic zero and ascending 32-byte seeds using Node24.13 WebCrypto; no wallet process or network execution. Used as reference, not implementation under test.
- Language: en
- Script: Latn
- Encoding: UTF-8
- Normalization: none
- Word count: 256
- SHA-256: 37a65f88512467edd12a1ab3eeb5f4328230e86711a8efde6333361ce10f4fcf
- Order rule: Extract alternatingWords at source indices 0\:\:2; preserve source spelling/case; UTF-8 LF and one final LF. Index is byte value 0..255.
- Position rules: Only odd one-based rows including 33 in Decred PGP33; never use union of both halves.
- Source revision: c0fee6b52ad30961cfc3e06017d5e7516952615e
- License: ISC
- Attribution: Copyright \(c\) 2015 The Decred developers \(wordlist\); 2013-2016 The btcsuite developers and 2015-2020 The Decred developers \(root\). Complete ISC notices in THIRD\_PARTY\_NOTICES.
- Repository redistribution: allowed
- SignPath compatibility: compatible
- License evidence: [decred-pgp-license](../catalog/evidence/decred-pgp-license.json), [decred-pgp-osi](../catalog/evidence/decred-pgp-osi.json), [decred-pgp-signpath](../catalog/evidence/decred-pgp-signpath.json)
- Test vectors: [decred-pgp-vectors](../catalog/evidence/decred-pgp-vectors.json), [decred-pgp33-reference](../catalog/evidence/decred-pgp33-reference.json)

<a id="dictionary-pgp-odd"></a>

### Decred PGP — odd positions \(zero-based\) — pgp-odd

- Source record: [pgp-odd](../catalog/dictionaries/pgp-odd.json)
- Status: verified
- Reason: Verified research record; not a release or security guarantee.
- Version interval (min / max): c0fee6b52ad30961cfc3e06017d5e7516952615e / c0fee6b52ad30961cfc3e06017d5e7516952615e
- Verified on: 2026-09-29
- Historical: false
- Evidence: [decred-decrediton-license](../catalog/evidence/decred-decrediton-license.json), [decred-pgp-license](../catalog/evidence/decred-pgp-license.json), [decred-pgp-list](../catalog/evidence/decred-pgp-list.json), [decred-pgp-osi](../catalog/evidence/decred-pgp-osi.json), [decred-pgp-position](../catalog/evidence/decred-pgp-position.json), [decred-pgp-signpath](../catalog/evidence/decred-pgp-signpath.json), [decred-pgp-vectors](../catalog/evidence/decred-pgp-vectors.json), [decred-pgp33-reference](../catalog/evidence/decred-pgp33-reference.json)
- Evidence claim: ISC notice retained for modified synthetic output projections from the official Decrediton encoder. No implementation/library or wallet binary bundled.
- Evidence claim: Reviewed 2026-09-29\: root ISC and explicit ISC wordlist header permit these two modified list projections with complete original notices retained. Redistribution allowed. Local component signing compatibility assessed separately; no project acceptance.
- Evidence claim: ISC-licensed alternatingWords literal contains 512 words\: index 2\*b even half, 2\*b\+1 odd half; exact source case retained. UTF-8 LF projection with final LF, no sorting.
- Evidence claim: OSI identifies ISC as an approved license; actual grant and scope are supplied by pinned Decred source/header. Component compatibility only.
- Evidence claim: ByteToMnemonic selects half by zero-based position, not byte parity. DecodeMnemonics rejects wrong-position half and compares words case-insensitively.
- Evidence claim: Reviewed 2026-09-29\: OSS terms require OSI-approved licensing across components. Exact ISC list projections with notices satisfy local component licensing assessment; this is not Foundation acceptance or signing/release approval.
- Evidence claim: Public known-answer mnemonicTests cover 20- and 31-byte seeds; fixed expected words project to indices/fingerprints and corroborate ordering/checksum. They are not mislabeled 33-word examples.
- Evidence claim: Reviewed pinned independent official JavaScript encodeMnemonic produces expected 33-word outputs for synthetic zero and ascending 32-byte seeds using Node24.13 WebCrypto; no wallet process or network execution. Used as reference, not implementation under test.
- Language: en
- Script: Latn
- Encoding: UTF-8
- Normalization: none
- Word count: 256
- SHA-256: c2f23c2233d4d7291107e8f796c374d0cb1fb30c1391bcb4f6480243de8ebf5a
- Order rule: Extract alternatingWords at source indices 1\:\:2; preserve source spelling/case; UTF-8 LF and one final LF. Index is byte value 0..255.
- Position rules: Only even one-based rows through 32 in Decred PGP33; never use union of both halves.
- Source revision: c0fee6b52ad30961cfc3e06017d5e7516952615e
- License: ISC
- Attribution: Copyright \(c\) 2015 The Decred developers \(wordlist\); 2013-2016 The btcsuite developers and 2015-2020 The Decred developers \(root\). Complete ISC notices in THIRD\_PARTY\_NOTICES.
- Repository redistribution: allowed
- SignPath compatibility: compatible
- License evidence: [decred-pgp-license](../catalog/evidence/decred-pgp-license.json), [decred-pgp-osi](../catalog/evidence/decred-pgp-osi.json), [decred-pgp-signpath](../catalog/evidence/decred-pgp-signpath.json)
- Test vectors: [decred-pgp-vectors](../catalog/evidence/decred-pgp-vectors.json), [decred-pgp33-reference](../catalog/evidence/decred-pgp33-reference.json)

<a id="dictionary-polyseed-cs"></a>

### polyseed-cs — polyseed-cs

- Source record: [polyseed-cs](../catalog/dictionaries/polyseed-cs.json)
- Status: documented
- Reason: Evidence is insufficient for selectable support.
- Guidance: Not selectable; use the wallet's own backup procedure.
- Version interval (min / max): 56f634647d4f75596de20a6259b0cf1933949fdc / 56f634647d4f75596de20a6259b0cf1933949fdc
- Verified on: 2026-09-29
- Historical: false
- Evidence: [monero-osi-apache](../catalog/evidence/monero-osi-apache.json), [monero-polyseed-license](../catalog/evidence/monero-polyseed-license.json), [monero-polyseed-notice](../catalog/evidence/monero-polyseed-notice.json), [monero-polyseed-rules](../catalog/evidence/monero-polyseed-rules.json), [monero-signpath](../catalog/evidence/monero-signpath.json), [polyseed-cs-source](../catalog/evidence/polyseed-cs-source.json)
- Evidence claim: OSI lists Apache-2.0 as approved. This corroborates only the component-license decision, not project acceptance. Response-body SHA-256 1377faaaa81ba356528c4053d80e32fd12d84b794ed2667f09bf94aaca7458eb.
- Evidence claim: Apache-2.0 permits this modified source-data projection subject to license, notices and modification marking; root project LICENSE contains identical Apache text. No commercial dual-license requirement. Reviewed 2026-09-29; response byte SHA-256 cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30. See docs/research/batches/monero-polyseed.md.
- Evidence claim: Polyseed attribution and BIP39-derived dictionary MIT obligations apply cumulatively with Apache-2.0; complete upstream NOTICE retained in THIRD\_PARTY\_NOTICES. Reviewed 2026-09-29; response byte SHA-256 442cd16cdc8913cd76a9f7bd1047a0aea68ede782d94db3556392e18f39ad64e. See docs/research/batches/monero-polyseed.md.
- Evidence claim: Ten lists, NFKD word invariant, ordinal index lookup, language-dependent prefixes/accent handling; no BIP39 substitution. Reviewed 2026-09-29; response byte SHA-256 f30f867f5afd3bab323d85a8678868862d94dde09ed7801ab45a74f9b563b447. See docs/research/batches/monero-polyseed.md.
- Evidence claim: Codex component assessment\: reviewed BSD-3-Clause/MIT and Apache-2.0\+MIT data licenses are OSI-approved and impose no commercial dual-licensing; notices are retained. Compatible for this data-only payload. Foundation acceptance, project eligibility and release signing remain unproven. Response-body SHA-256 6610cf889bbe0dc7533abaa310bc7a5cc9a61ae6c2ce0798a08109c925b46c51.
- Evidence claim: Exact ordered dictionary array and applicable file-level license header reviewed. Source-token extraction and byte hashes are independently checked against the public fixture; no complete phrase is stored here. Reviewed 2026-09-29; response byte SHA-256 395c70fb0de3e4c9034da698c679269227c1783d0ae56617bb8bcfd950eb9cd3. See docs/research/batches/monero-polyseed.md.
- Language: cs
- Script: Latn
- Encoding: UTF-8
- Normalization: NFKD
- Word count: 2048
- SHA-256: 195136b3ba0f3099a9df625e0963f4efb56625b91c3a76bc5b4a9466a26880f7
- Order rule: Exact upstream array order; zero-based indices. Extract literal UTF-8 tokens unchanged; remove C/C\+\+ wrapper and indentation, append LF after every token. No sorting, lowercasing or Unicode rewriting. Source file and extracted byte hashes in batch note.
- Position rules: Same 2048-entry vocabulary at all 16 positions. First word is polynomial checksum; no BIP39 checksum semantics.; Input uses NFKD; output may compose NFC for accented/Japanese/Korean language flags. Latin prefix matching and French/Spanish accent-insensitivity are separate from stored NFKD bytes.; Language coverage is not a wallet generation claim.
- Source revision: 56f634647d4f75596de20a6259b0cf1933949fdc
- License: Apache-2.0 AND MIT
- Attribution: Copyright \(c\) 2020-2026 tevador; BIP-39 authors copyright 2013. Upstream NOTICE and Apache/MIT terms retained in THIRD\_PARTY\_NOTICES.
- Repository redistribution: allowed
- SignPath compatibility: compatible
- License evidence: [monero-osi-apache](../catalog/evidence/monero-osi-apache.json), [monero-polyseed-license](../catalog/evidence/monero-polyseed-license.json), [monero-polyseed-notice](../catalog/evidence/monero-polyseed-notice.json), [monero-signpath](../catalog/evidence/monero-signpath.json), [polyseed-cs-source](../catalog/evidence/polyseed-cs-source.json)
- Test vectors: —

<a id="dictionary-polyseed-en"></a>

### polyseed-en — polyseed-en

- Source record: [polyseed-en](../catalog/dictionaries/polyseed-en.json)
- Status: verified
- Reason: Verified research record; not a release or security guarantee.
- Version interval (min / max): 56f634647d4f75596de20a6259b0cf1933949fdc / 56f634647d4f75596de20a6259b0cf1933949fdc
- Verified on: 2026-09-29
- Historical: false
- Evidence: [monero-osi-apache](../catalog/evidence/monero-osi-apache.json), [monero-polyseed-license](../catalog/evidence/monero-polyseed-license.json), [monero-polyseed-notice](../catalog/evidence/monero-polyseed-notice.json), [monero-polyseed-rules](../catalog/evidence/monero-polyseed-rules.json), [monero-polyseed-vectors](../catalog/evidence/monero-polyseed-vectors.json), [monero-signpath](../catalog/evidence/monero-signpath.json), [polyseed-en-source](../catalog/evidence/polyseed-en-source.json)
- Evidence claim: OSI lists Apache-2.0 as approved. This corroborates only the component-license decision, not project acceptance. Response-body SHA-256 1377faaaa81ba356528c4053d80e32fd12d84b794ed2667f09bf94aaca7458eb.
- Evidence claim: Apache-2.0 permits this modified source-data projection subject to license, notices and modification marking; root project LICENSE contains identical Apache text. No commercial dual-license requirement. Reviewed 2026-09-29; response byte SHA-256 cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30. See docs/research/batches/monero-polyseed.md.
- Evidence claim: Polyseed attribution and BIP39-derived dictionary MIT obligations apply cumulatively with Apache-2.0; complete upstream NOTICE retained in THIRD\_PARTY\_NOTICES. Reviewed 2026-09-29; response byte SHA-256 442cd16cdc8913cd76a9f7bd1047a0aea68ede782d94db3556392e18f39ad64e. See docs/research/batches/monero-polyseed.md.
- Evidence claim: Ten lists, NFKD word invariant, ordinal index lookup, language-dependent prefixes/accent handling; no BIP39 substitution. Reviewed 2026-09-29; response byte SHA-256 f30f867f5afd3bab323d85a8678868862d94dde09ed7801ab45a74f9b563b447. See docs/research/batches/monero-polyseed.md.
- Evidence claim: Published English/Spanish fixed phrases, random byte inputs, birthday and PBKDF2-input assertions. Projection tests dictionary order, GF checksum and secret/date unpacking. Upstream PBKDF2 is a dummy\: these are NOT derived-key known answers. Reviewed 2026-09-29; response byte SHA-256 3bc51ff2c12c3840e93d5e87a8da47516f806e3d51dc72ea6049f7f439dba4d5. See docs/research/batches/monero-polyseed.md.
- Evidence claim: Codex component assessment\: reviewed BSD-3-Clause/MIT and Apache-2.0\+MIT data licenses are OSI-approved and impose no commercial dual-licensing; notices are retained. Compatible for this data-only payload. Foundation acceptance, project eligibility and release signing remain unproven. Response-body SHA-256 6610cf889bbe0dc7533abaa310bc7a5cc9a61ae6c2ce0798a08109c925b46c51.
- Evidence claim: Exact ordered dictionary array and applicable file-level license header reviewed. Source-token extraction and byte hashes are independently checked against the public fixture; no complete phrase is stored here. Reviewed 2026-09-29; response byte SHA-256 6e32fb9d56d5c8a304d173937deec9dc9d64e52d15a9104f1c63dc45b7911f47. See docs/research/batches/monero-polyseed.md.
- Language: en
- Script: Latn
- Encoding: UTF-8
- Normalization: NFKD
- Word count: 2048
- SHA-256: 2f5eed53a4727b4bf8880d8f3f199efc90e58503646d9ff8eff3a2ed3b24dbda
- Order rule: Exact upstream array order; zero-based indices. Extract literal UTF-8 tokens unchanged; remove C/C\+\+ wrapper and indentation, append LF after every token. No sorting, lowercasing or Unicode rewriting. Source file and extracted byte hashes in batch note.
- Position rules: Same 2048-entry vocabulary at all 16 positions. First word is polynomial checksum; no BIP39 checksum semantics.; Input uses NFKD; output may compose NFC for accented/Japanese/Korean language flags. Latin prefix matching and French/Spanish accent-insensitivity are separate from stored NFKD bytes.; Language coverage is not a wallet generation claim.
- Source revision: 56f634647d4f75596de20a6259b0cf1933949fdc
- License: Apache-2.0 AND MIT
- Attribution: Copyright \(c\) 2020-2026 tevador; BIP-39 authors copyright 2013. Upstream NOTICE and Apache/MIT terms retained in THIRD\_PARTY\_NOTICES.
- Repository redistribution: allowed
- SignPath compatibility: compatible
- License evidence: [monero-osi-apache](../catalog/evidence/monero-osi-apache.json), [monero-polyseed-license](../catalog/evidence/monero-polyseed-license.json), [monero-polyseed-notice](../catalog/evidence/monero-polyseed-notice.json), [monero-signpath](../catalog/evidence/monero-signpath.json), [polyseed-en-source](../catalog/evidence/polyseed-en-source.json)
- Test vectors: [monero-polyseed-vectors](../catalog/evidence/monero-polyseed-vectors.json)

<a id="dictionary-polyseed-es"></a>

### polyseed-es — polyseed-es

- Source record: [polyseed-es](../catalog/dictionaries/polyseed-es.json)
- Status: verified
- Reason: Verified research record; not a release or security guarantee.
- Version interval (min / max): 56f634647d4f75596de20a6259b0cf1933949fdc / 56f634647d4f75596de20a6259b0cf1933949fdc
- Verified on: 2026-09-29
- Historical: false
- Evidence: [monero-osi-apache](../catalog/evidence/monero-osi-apache.json), [monero-polyseed-license](../catalog/evidence/monero-polyseed-license.json), [monero-polyseed-notice](../catalog/evidence/monero-polyseed-notice.json), [monero-polyseed-rules](../catalog/evidence/monero-polyseed-rules.json), [monero-polyseed-vectors](../catalog/evidence/monero-polyseed-vectors.json), [monero-signpath](../catalog/evidence/monero-signpath.json), [polyseed-es-source](../catalog/evidence/polyseed-es-source.json)
- Evidence claim: OSI lists Apache-2.0 as approved. This corroborates only the component-license decision, not project acceptance. Response-body SHA-256 1377faaaa81ba356528c4053d80e32fd12d84b794ed2667f09bf94aaca7458eb.
- Evidence claim: Apache-2.0 permits this modified source-data projection subject to license, notices and modification marking; root project LICENSE contains identical Apache text. No commercial dual-license requirement. Reviewed 2026-09-29; response byte SHA-256 cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30. See docs/research/batches/monero-polyseed.md.
- Evidence claim: Polyseed attribution and BIP39-derived dictionary MIT obligations apply cumulatively with Apache-2.0; complete upstream NOTICE retained in THIRD\_PARTY\_NOTICES. Reviewed 2026-09-29; response byte SHA-256 442cd16cdc8913cd76a9f7bd1047a0aea68ede782d94db3556392e18f39ad64e. See docs/research/batches/monero-polyseed.md.
- Evidence claim: Ten lists, NFKD word invariant, ordinal index lookup, language-dependent prefixes/accent handling; no BIP39 substitution. Reviewed 2026-09-29; response byte SHA-256 f30f867f5afd3bab323d85a8678868862d94dde09ed7801ab45a74f9b563b447. See docs/research/batches/monero-polyseed.md.
- Evidence claim: Published English/Spanish fixed phrases, random byte inputs, birthday and PBKDF2-input assertions. Projection tests dictionary order, GF checksum and secret/date unpacking. Upstream PBKDF2 is a dummy\: these are NOT derived-key known answers. Reviewed 2026-09-29; response byte SHA-256 3bc51ff2c12c3840e93d5e87a8da47516f806e3d51dc72ea6049f7f439dba4d5. See docs/research/batches/monero-polyseed.md.
- Evidence claim: Codex component assessment\: reviewed BSD-3-Clause/MIT and Apache-2.0\+MIT data licenses are OSI-approved and impose no commercial dual-licensing; notices are retained. Compatible for this data-only payload. Foundation acceptance, project eligibility and release signing remain unproven. Response-body SHA-256 6610cf889bbe0dc7533abaa310bc7a5cc9a61ae6c2ce0798a08109c925b46c51.
- Evidence claim: Exact ordered dictionary array and applicable file-level license header reviewed. Source-token extraction and byte hashes are independently checked against the public fixture; no complete phrase is stored here. Reviewed 2026-09-29; response byte SHA-256 90405262a658434062b1d26cc7799c1d7fbeb11486c93a01153c733315c0cc0d. See docs/research/batches/monero-polyseed.md.
- Language: es
- Script: Latn
- Encoding: UTF-8
- Normalization: NFKD
- Word count: 2048
- SHA-256: 31e589970a7490b1d62534c57b97b65b7d8ec7e7fcdad4830af1e324ed387c52
- Order rule: Exact upstream array order; zero-based indices. Extract literal UTF-8 tokens unchanged; remove C/C\+\+ wrapper and indentation, append LF after every token. No sorting, lowercasing or Unicode rewriting. Source file and extracted byte hashes in batch note.
- Position rules: Same 2048-entry vocabulary at all 16 positions. First word is polynomial checksum; no BIP39 checksum semantics.; Input uses NFKD; output may compose NFC for accented/Japanese/Korean language flags. Latin prefix matching and French/Spanish accent-insensitivity are separate from stored NFKD bytes.; Language coverage is not a wallet generation claim.
- Source revision: 56f634647d4f75596de20a6259b0cf1933949fdc
- License: Apache-2.0 AND MIT
- Attribution: Copyright \(c\) 2020-2026 tevador; BIP-39 authors copyright 2013. Upstream NOTICE and Apache/MIT terms retained in THIRD\_PARTY\_NOTICES.
- Repository redistribution: allowed
- SignPath compatibility: compatible
- License evidence: [monero-osi-apache](../catalog/evidence/monero-osi-apache.json), [monero-polyseed-license](../catalog/evidence/monero-polyseed-license.json), [monero-polyseed-notice](../catalog/evidence/monero-polyseed-notice.json), [monero-signpath](../catalog/evidence/monero-signpath.json), [polyseed-es-source](../catalog/evidence/polyseed-es-source.json)
- Test vectors: [monero-polyseed-vectors](../catalog/evidence/monero-polyseed-vectors.json)

<a id="dictionary-polyseed-fr"></a>

### polyseed-fr — polyseed-fr

- Source record: [polyseed-fr](../catalog/dictionaries/polyseed-fr.json)
- Status: documented
- Reason: Evidence is insufficient for selectable support.
- Guidance: Not selectable; use the wallet's own backup procedure.
- Version interval (min / max): 56f634647d4f75596de20a6259b0cf1933949fdc / 56f634647d4f75596de20a6259b0cf1933949fdc
- Verified on: 2026-09-29
- Historical: false
- Evidence: [monero-osi-apache](../catalog/evidence/monero-osi-apache.json), [monero-polyseed-license](../catalog/evidence/monero-polyseed-license.json), [monero-polyseed-notice](../catalog/evidence/monero-polyseed-notice.json), [monero-polyseed-rules](../catalog/evidence/monero-polyseed-rules.json), [monero-signpath](../catalog/evidence/monero-signpath.json), [polyseed-fr-source](../catalog/evidence/polyseed-fr-source.json)
- Evidence claim: OSI lists Apache-2.0 as approved. This corroborates only the component-license decision, not project acceptance. Response-body SHA-256 1377faaaa81ba356528c4053d80e32fd12d84b794ed2667f09bf94aaca7458eb.
- Evidence claim: Apache-2.0 permits this modified source-data projection subject to license, notices and modification marking; root project LICENSE contains identical Apache text. No commercial dual-license requirement. Reviewed 2026-09-29; response byte SHA-256 cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30. See docs/research/batches/monero-polyseed.md.
- Evidence claim: Polyseed attribution and BIP39-derived dictionary MIT obligations apply cumulatively with Apache-2.0; complete upstream NOTICE retained in THIRD\_PARTY\_NOTICES. Reviewed 2026-09-29; response byte SHA-256 442cd16cdc8913cd76a9f7bd1047a0aea68ede782d94db3556392e18f39ad64e. See docs/research/batches/monero-polyseed.md.
- Evidence claim: Ten lists, NFKD word invariant, ordinal index lookup, language-dependent prefixes/accent handling; no BIP39 substitution. Reviewed 2026-09-29; response byte SHA-256 f30f867f5afd3bab323d85a8678868862d94dde09ed7801ab45a74f9b563b447. See docs/research/batches/monero-polyseed.md.
- Evidence claim: Codex component assessment\: reviewed BSD-3-Clause/MIT and Apache-2.0\+MIT data licenses are OSI-approved and impose no commercial dual-licensing; notices are retained. Compatible for this data-only payload. Foundation acceptance, project eligibility and release signing remain unproven. Response-body SHA-256 6610cf889bbe0dc7533abaa310bc7a5cc9a61ae6c2ce0798a08109c925b46c51.
- Evidence claim: Exact ordered dictionary array and applicable file-level license header reviewed. Source-token extraction and byte hashes are independently checked against the public fixture; no complete phrase is stored here. Reviewed 2026-09-29; response byte SHA-256 0cb937a44ac79218a35e4d10f757d85dcd482cb4ed1482928644d0292ab8f0e2. See docs/research/batches/monero-polyseed.md.
- Language: fr
- Script: Latn
- Encoding: UTF-8
- Normalization: NFKD
- Word count: 2048
- SHA-256: ebc3959ab7801a1df6bac4fa7d970652f1df76b683cd2f4003c941c63d517e59
- Order rule: Exact upstream array order; zero-based indices. Extract literal UTF-8 tokens unchanged; remove C/C\+\+ wrapper and indentation, append LF after every token. No sorting, lowercasing or Unicode rewriting. Source file and extracted byte hashes in batch note.
- Position rules: Same 2048-entry vocabulary at all 16 positions. First word is polynomial checksum; no BIP39 checksum semantics.; Input uses NFKD; output may compose NFC for accented/Japanese/Korean language flags. Latin prefix matching and French/Spanish accent-insensitivity are separate from stored NFKD bytes.; Language coverage is not a wallet generation claim.
- Source revision: 56f634647d4f75596de20a6259b0cf1933949fdc
- License: Apache-2.0 AND MIT
- Attribution: Copyright \(c\) 2020-2026 tevador; BIP-39 authors copyright 2013. Upstream NOTICE and Apache/MIT terms retained in THIRD\_PARTY\_NOTICES.
- Repository redistribution: allowed
- SignPath compatibility: compatible
- License evidence: [monero-osi-apache](../catalog/evidence/monero-osi-apache.json), [monero-polyseed-license](../catalog/evidence/monero-polyseed-license.json), [monero-polyseed-notice](../catalog/evidence/monero-polyseed-notice.json), [monero-signpath](../catalog/evidence/monero-signpath.json), [polyseed-fr-source](../catalog/evidence/polyseed-fr-source.json)
- Test vectors: —

<a id="dictionary-polyseed-it"></a>

### polyseed-it — polyseed-it

- Source record: [polyseed-it](../catalog/dictionaries/polyseed-it.json)
- Status: documented
- Reason: Evidence is insufficient for selectable support.
- Guidance: Not selectable; use the wallet's own backup procedure.
- Version interval (min / max): 56f634647d4f75596de20a6259b0cf1933949fdc / 56f634647d4f75596de20a6259b0cf1933949fdc
- Verified on: 2026-09-29
- Historical: false
- Evidence: [monero-osi-apache](../catalog/evidence/monero-osi-apache.json), [monero-polyseed-license](../catalog/evidence/monero-polyseed-license.json), [monero-polyseed-notice](../catalog/evidence/monero-polyseed-notice.json), [monero-polyseed-rules](../catalog/evidence/monero-polyseed-rules.json), [monero-signpath](../catalog/evidence/monero-signpath.json), [polyseed-it-source](../catalog/evidence/polyseed-it-source.json)
- Evidence claim: OSI lists Apache-2.0 as approved. This corroborates only the component-license decision, not project acceptance. Response-body SHA-256 1377faaaa81ba356528c4053d80e32fd12d84b794ed2667f09bf94aaca7458eb.
- Evidence claim: Apache-2.0 permits this modified source-data projection subject to license, notices and modification marking; root project LICENSE contains identical Apache text. No commercial dual-license requirement. Reviewed 2026-09-29; response byte SHA-256 cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30. See docs/research/batches/monero-polyseed.md.
- Evidence claim: Polyseed attribution and BIP39-derived dictionary MIT obligations apply cumulatively with Apache-2.0; complete upstream NOTICE retained in THIRD\_PARTY\_NOTICES. Reviewed 2026-09-29; response byte SHA-256 442cd16cdc8913cd76a9f7bd1047a0aea68ede782d94db3556392e18f39ad64e. See docs/research/batches/monero-polyseed.md.
- Evidence claim: Ten lists, NFKD word invariant, ordinal index lookup, language-dependent prefixes/accent handling; no BIP39 substitution. Reviewed 2026-09-29; response byte SHA-256 f30f867f5afd3bab323d85a8678868862d94dde09ed7801ab45a74f9b563b447. See docs/research/batches/monero-polyseed.md.
- Evidence claim: Codex component assessment\: reviewed BSD-3-Clause/MIT and Apache-2.0\+MIT data licenses are OSI-approved and impose no commercial dual-licensing; notices are retained. Compatible for this data-only payload. Foundation acceptance, project eligibility and release signing remain unproven. Response-body SHA-256 6610cf889bbe0dc7533abaa310bc7a5cc9a61ae6c2ce0798a08109c925b46c51.
- Evidence claim: Exact ordered dictionary array and applicable file-level license header reviewed. Source-token extraction and byte hashes are independently checked against the public fixture; no complete phrase is stored here. Reviewed 2026-09-29; response byte SHA-256 211787e3a762b7b55e7f2f422dc16e843399697ef078b10b2773ba62972a312a. See docs/research/batches/monero-polyseed.md.
- Language: it
- Script: Latn
- Encoding: UTF-8
- Normalization: NFKD
- Word count: 2048
- SHA-256: d392c49fdb700a24cd1fceb237c1f65dcc128f6b34a8aacb58b59384b5c648c2
- Order rule: Exact upstream array order; zero-based indices. Extract literal UTF-8 tokens unchanged; remove C/C\+\+ wrapper and indentation, append LF after every token. No sorting, lowercasing or Unicode rewriting. Source file and extracted byte hashes in batch note.
- Position rules: Same 2048-entry vocabulary at all 16 positions. First word is polynomial checksum; no BIP39 checksum semantics.; Input uses NFKD; output may compose NFC for accented/Japanese/Korean language flags. Latin prefix matching and French/Spanish accent-insensitivity are separate from stored NFKD bytes.; Language coverage is not a wallet generation claim.
- Source revision: 56f634647d4f75596de20a6259b0cf1933949fdc
- License: Apache-2.0 AND MIT
- Attribution: Copyright \(c\) 2020-2026 tevador; BIP-39 authors copyright 2013. Upstream NOTICE and Apache/MIT terms retained in THIRD\_PARTY\_NOTICES.
- Repository redistribution: allowed
- SignPath compatibility: compatible
- License evidence: [monero-osi-apache](../catalog/evidence/monero-osi-apache.json), [monero-polyseed-license](../catalog/evidence/monero-polyseed-license.json), [monero-polyseed-notice](../catalog/evidence/monero-polyseed-notice.json), [monero-signpath](../catalog/evidence/monero-signpath.json), [polyseed-it-source](../catalog/evidence/polyseed-it-source.json)
- Test vectors: —

<a id="dictionary-polyseed-ja"></a>

### polyseed-ja — polyseed-ja

- Source record: [polyseed-ja](../catalog/dictionaries/polyseed-ja.json)
- Status: documented
- Reason: Evidence is insufficient for selectable support.
- Guidance: Not selectable; use the wallet's own backup procedure.
- Version interval (min / max): 56f634647d4f75596de20a6259b0cf1933949fdc / 56f634647d4f75596de20a6259b0cf1933949fdc
- Verified on: 2026-09-29
- Historical: false
- Evidence: [monero-osi-apache](../catalog/evidence/monero-osi-apache.json), [monero-polyseed-license](../catalog/evidence/monero-polyseed-license.json), [monero-polyseed-notice](../catalog/evidence/monero-polyseed-notice.json), [monero-polyseed-rules](../catalog/evidence/monero-polyseed-rules.json), [monero-signpath](../catalog/evidence/monero-signpath.json), [polyseed-ja-source](../catalog/evidence/polyseed-ja-source.json)
- Evidence claim: OSI lists Apache-2.0 as approved. This corroborates only the component-license decision, not project acceptance. Response-body SHA-256 1377faaaa81ba356528c4053d80e32fd12d84b794ed2667f09bf94aaca7458eb.
- Evidence claim: Apache-2.0 permits this modified source-data projection subject to license, notices and modification marking; root project LICENSE contains identical Apache text. No commercial dual-license requirement. Reviewed 2026-09-29; response byte SHA-256 cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30. See docs/research/batches/monero-polyseed.md.
- Evidence claim: Polyseed attribution and BIP39-derived dictionary MIT obligations apply cumulatively with Apache-2.0; complete upstream NOTICE retained in THIRD\_PARTY\_NOTICES. Reviewed 2026-09-29; response byte SHA-256 442cd16cdc8913cd76a9f7bd1047a0aea68ede782d94db3556392e18f39ad64e. See docs/research/batches/monero-polyseed.md.
- Evidence claim: Ten lists, NFKD word invariant, ordinal index lookup, language-dependent prefixes/accent handling; no BIP39 substitution. Reviewed 2026-09-29; response byte SHA-256 f30f867f5afd3bab323d85a8678868862d94dde09ed7801ab45a74f9b563b447. See docs/research/batches/monero-polyseed.md.
- Evidence claim: Codex component assessment\: reviewed BSD-3-Clause/MIT and Apache-2.0\+MIT data licenses are OSI-approved and impose no commercial dual-licensing; notices are retained. Compatible for this data-only payload. Foundation acceptance, project eligibility and release signing remain unproven. Response-body SHA-256 6610cf889bbe0dc7533abaa310bc7a5cc9a61ae6c2ce0798a08109c925b46c51.
- Evidence claim: Exact ordered dictionary array and applicable file-level license header reviewed. Source-token extraction and byte hashes are independently checked against the public fixture; no complete phrase is stored here. Reviewed 2026-09-29; response byte SHA-256 c309fd0d6c435de214262dd5c96331b8a48bd9a9a3b3b6659d2817056ecc1887. See docs/research/batches/monero-polyseed.md.
- Language: ja
- Script: Jpan
- Encoding: UTF-8
- Normalization: NFKD
- Word count: 2048
- SHA-256: 438b4d19c4af485650822ae0d08855090a6812e2a2ed6fb793583ae90f3e6248
- Order rule: Exact upstream array order; zero-based indices. Extract literal UTF-8 tokens unchanged; remove C/C\+\+ wrapper and indentation, append LF after every token. No sorting, lowercasing or Unicode rewriting. Source file and extracted byte hashes in batch note.
- Position rules: Same 2048-entry vocabulary at all 16 positions. First word is polynomial checksum; no BIP39 checksum semantics.; Input uses NFKD; output may compose NFC for accented/Japanese/Korean language flags. Latin prefix matching and French/Spanish accent-insensitivity are separate from stored NFKD bytes.; Language coverage is not a wallet generation claim.
- Source revision: 56f634647d4f75596de20a6259b0cf1933949fdc
- License: Apache-2.0 AND MIT
- Attribution: Copyright \(c\) 2020-2026 tevador; BIP-39 authors copyright 2013. Upstream NOTICE and Apache/MIT terms retained in THIRD\_PARTY\_NOTICES.
- Repository redistribution: allowed
- SignPath compatibility: compatible
- License evidence: [monero-osi-apache](../catalog/evidence/monero-osi-apache.json), [monero-polyseed-license](../catalog/evidence/monero-polyseed-license.json), [monero-polyseed-notice](../catalog/evidence/monero-polyseed-notice.json), [monero-signpath](../catalog/evidence/monero-signpath.json), [polyseed-ja-source](../catalog/evidence/polyseed-ja-source.json)
- Test vectors: —

<a id="dictionary-polyseed-ko"></a>

### polyseed-ko — polyseed-ko

- Source record: [polyseed-ko](../catalog/dictionaries/polyseed-ko.json)
- Status: documented
- Reason: Evidence is insufficient for selectable support.
- Guidance: Not selectable; use the wallet's own backup procedure.
- Version interval (min / max): 56f634647d4f75596de20a6259b0cf1933949fdc / 56f634647d4f75596de20a6259b0cf1933949fdc
- Verified on: 2026-09-29
- Historical: false
- Evidence: [monero-osi-apache](../catalog/evidence/monero-osi-apache.json), [monero-polyseed-license](../catalog/evidence/monero-polyseed-license.json), [monero-polyseed-notice](../catalog/evidence/monero-polyseed-notice.json), [monero-polyseed-rules](../catalog/evidence/monero-polyseed-rules.json), [monero-signpath](../catalog/evidence/monero-signpath.json), [polyseed-ko-source](../catalog/evidence/polyseed-ko-source.json)
- Evidence claim: OSI lists Apache-2.0 as approved. This corroborates only the component-license decision, not project acceptance. Response-body SHA-256 1377faaaa81ba356528c4053d80e32fd12d84b794ed2667f09bf94aaca7458eb.
- Evidence claim: Apache-2.0 permits this modified source-data projection subject to license, notices and modification marking; root project LICENSE contains identical Apache text. No commercial dual-license requirement. Reviewed 2026-09-29; response byte SHA-256 cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30. See docs/research/batches/monero-polyseed.md.
- Evidence claim: Polyseed attribution and BIP39-derived dictionary MIT obligations apply cumulatively with Apache-2.0; complete upstream NOTICE retained in THIRD\_PARTY\_NOTICES. Reviewed 2026-09-29; response byte SHA-256 442cd16cdc8913cd76a9f7bd1047a0aea68ede782d94db3556392e18f39ad64e. See docs/research/batches/monero-polyseed.md.
- Evidence claim: Ten lists, NFKD word invariant, ordinal index lookup, language-dependent prefixes/accent handling; no BIP39 substitution. Reviewed 2026-09-29; response byte SHA-256 f30f867f5afd3bab323d85a8678868862d94dde09ed7801ab45a74f9b563b447. See docs/research/batches/monero-polyseed.md.
- Evidence claim: Codex component assessment\: reviewed BSD-3-Clause/MIT and Apache-2.0\+MIT data licenses are OSI-approved and impose no commercial dual-licensing; notices are retained. Compatible for this data-only payload. Foundation acceptance, project eligibility and release signing remain unproven. Response-body SHA-256 6610cf889bbe0dc7533abaa310bc7a5cc9a61ae6c2ce0798a08109c925b46c51.
- Evidence claim: Exact ordered dictionary array and applicable file-level license header reviewed. Source-token extraction and byte hashes are independently checked against the public fixture; no complete phrase is stored here. Reviewed 2026-09-29; response byte SHA-256 0b56d27f7c1d3c6d13af9248d981d90a7d515222e3858fe6eca2f1aae7ea6ac9. See docs/research/batches/monero-polyseed.md.
- Language: ko
- Script: Kore
- Encoding: UTF-8
- Normalization: NFKD
- Word count: 2048
- SHA-256: 9e95f86c167de88f450f0aaf89e87f6624a57f973c67b516e338e8e8b8897f60
- Order rule: Exact upstream array order; zero-based indices. Extract literal UTF-8 tokens unchanged; remove C/C\+\+ wrapper and indentation, append LF after every token. No sorting, lowercasing or Unicode rewriting. Source file and extracted byte hashes in batch note.
- Position rules: Same 2048-entry vocabulary at all 16 positions. First word is polynomial checksum; no BIP39 checksum semantics.; Input uses NFKD; output may compose NFC for accented/Japanese/Korean language flags. Latin prefix matching and French/Spanish accent-insensitivity are separate from stored NFKD bytes.; Language coverage is not a wallet generation claim.
- Source revision: 56f634647d4f75596de20a6259b0cf1933949fdc
- License: Apache-2.0 AND MIT
- Attribution: Copyright \(c\) 2020-2026 tevador; BIP-39 authors copyright 2013. Upstream NOTICE and Apache/MIT terms retained in THIRD\_PARTY\_NOTICES.
- Repository redistribution: allowed
- SignPath compatibility: compatible
- License evidence: [monero-osi-apache](../catalog/evidence/monero-osi-apache.json), [monero-polyseed-license](../catalog/evidence/monero-polyseed-license.json), [monero-polyseed-notice](../catalog/evidence/monero-polyseed-notice.json), [monero-signpath](../catalog/evidence/monero-signpath.json), [polyseed-ko-source](../catalog/evidence/polyseed-ko-source.json)
- Test vectors: —

<a id="dictionary-polyseed-pt"></a>

### polyseed-pt — polyseed-pt

- Source record: [polyseed-pt](../catalog/dictionaries/polyseed-pt.json)
- Status: documented
- Reason: Evidence is insufficient for selectable support.
- Guidance: Not selectable; use the wallet's own backup procedure.
- Version interval (min / max): 56f634647d4f75596de20a6259b0cf1933949fdc / 56f634647d4f75596de20a6259b0cf1933949fdc
- Verified on: 2026-09-29
- Historical: false
- Evidence: [monero-osi-apache](../catalog/evidence/monero-osi-apache.json), [monero-polyseed-license](../catalog/evidence/monero-polyseed-license.json), [monero-polyseed-notice](../catalog/evidence/monero-polyseed-notice.json), [monero-polyseed-rules](../catalog/evidence/monero-polyseed-rules.json), [monero-signpath](../catalog/evidence/monero-signpath.json), [polyseed-pt-source](../catalog/evidence/polyseed-pt-source.json)
- Evidence claim: OSI lists Apache-2.0 as approved. This corroborates only the component-license decision, not project acceptance. Response-body SHA-256 1377faaaa81ba356528c4053d80e32fd12d84b794ed2667f09bf94aaca7458eb.
- Evidence claim: Apache-2.0 permits this modified source-data projection subject to license, notices and modification marking; root project LICENSE contains identical Apache text. No commercial dual-license requirement. Reviewed 2026-09-29; response byte SHA-256 cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30. See docs/research/batches/monero-polyseed.md.
- Evidence claim: Polyseed attribution and BIP39-derived dictionary MIT obligations apply cumulatively with Apache-2.0; complete upstream NOTICE retained in THIRD\_PARTY\_NOTICES. Reviewed 2026-09-29; response byte SHA-256 442cd16cdc8913cd76a9f7bd1047a0aea68ede782d94db3556392e18f39ad64e. See docs/research/batches/monero-polyseed.md.
- Evidence claim: Ten lists, NFKD word invariant, ordinal index lookup, language-dependent prefixes/accent handling; no BIP39 substitution. Reviewed 2026-09-29; response byte SHA-256 f30f867f5afd3bab323d85a8678868862d94dde09ed7801ab45a74f9b563b447. See docs/research/batches/monero-polyseed.md.
- Evidence claim: Codex component assessment\: reviewed BSD-3-Clause/MIT and Apache-2.0\+MIT data licenses are OSI-approved and impose no commercial dual-licensing; notices are retained. Compatible for this data-only payload. Foundation acceptance, project eligibility and release signing remain unproven. Response-body SHA-256 6610cf889bbe0dc7533abaa310bc7a5cc9a61ae6c2ce0798a08109c925b46c51.
- Evidence claim: Exact ordered dictionary array and applicable file-level license header reviewed. Source-token extraction and byte hashes are independently checked against the public fixture; no complete phrase is stored here. Reviewed 2026-09-29; response byte SHA-256 40e9919edf8b768a12cdfc3c3cd2343fa16a628ad0e8d2749b4c026af7c9bf70. See docs/research/batches/monero-polyseed.md.
- Language: pt
- Script: Latn
- Encoding: UTF-8
- Normalization: NFKD
- Word count: 2048
- SHA-256: 2685e9c194c82ae67e10ba59d9ea5345a23dc093e92276fc5361f6667d79cd3f
- Order rule: Exact upstream array order; zero-based indices. Extract literal UTF-8 tokens unchanged; remove C/C\+\+ wrapper and indentation, append LF after every token. No sorting, lowercasing or Unicode rewriting. Source file and extracted byte hashes in batch note.
- Position rules: Same 2048-entry vocabulary at all 16 positions. First word is polynomial checksum; no BIP39 checksum semantics.; Input uses NFKD; output may compose NFC for accented/Japanese/Korean language flags. Latin prefix matching and French/Spanish accent-insensitivity are separate from stored NFKD bytes.; Language coverage is not a wallet generation claim.
- Source revision: 56f634647d4f75596de20a6259b0cf1933949fdc
- License: Apache-2.0 AND MIT
- Attribution: Copyright \(c\) 2020-2026 tevador; BIP-39 authors copyright 2013. Upstream NOTICE and Apache/MIT terms retained in THIRD\_PARTY\_NOTICES.
- Repository redistribution: allowed
- SignPath compatibility: compatible
- License evidence: [monero-osi-apache](../catalog/evidence/monero-osi-apache.json), [monero-polyseed-license](../catalog/evidence/monero-polyseed-license.json), [monero-polyseed-notice](../catalog/evidence/monero-polyseed-notice.json), [monero-signpath](../catalog/evidence/monero-signpath.json), [polyseed-pt-source](../catalog/evidence/polyseed-pt-source.json)
- Test vectors: —

<a id="dictionary-polyseed-zh-hans"></a>

### polyseed-zh-hans — polyseed-zh-hans

- Source record: [polyseed-zh-hans](../catalog/dictionaries/polyseed-zh-hans.json)
- Status: documented
- Reason: Evidence is insufficient for selectable support.
- Guidance: Not selectable; use the wallet's own backup procedure.
- Version interval (min / max): 56f634647d4f75596de20a6259b0cf1933949fdc / 56f634647d4f75596de20a6259b0cf1933949fdc
- Verified on: 2026-09-29
- Historical: false
- Evidence: [monero-osi-apache](../catalog/evidence/monero-osi-apache.json), [monero-polyseed-license](../catalog/evidence/monero-polyseed-license.json), [monero-polyseed-notice](../catalog/evidence/monero-polyseed-notice.json), [monero-polyseed-rules](../catalog/evidence/monero-polyseed-rules.json), [monero-signpath](../catalog/evidence/monero-signpath.json), [polyseed-zh-hans-source](../catalog/evidence/polyseed-zh-hans-source.json)
- Evidence claim: OSI lists Apache-2.0 as approved. This corroborates only the component-license decision, not project acceptance. Response-body SHA-256 1377faaaa81ba356528c4053d80e32fd12d84b794ed2667f09bf94aaca7458eb.
- Evidence claim: Apache-2.0 permits this modified source-data projection subject to license, notices and modification marking; root project LICENSE contains identical Apache text. No commercial dual-license requirement. Reviewed 2026-09-29; response byte SHA-256 cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30. See docs/research/batches/monero-polyseed.md.
- Evidence claim: Polyseed attribution and BIP39-derived dictionary MIT obligations apply cumulatively with Apache-2.0; complete upstream NOTICE retained in THIRD\_PARTY\_NOTICES. Reviewed 2026-09-29; response byte SHA-256 442cd16cdc8913cd76a9f7bd1047a0aea68ede782d94db3556392e18f39ad64e. See docs/research/batches/monero-polyseed.md.
- Evidence claim: Ten lists, NFKD word invariant, ordinal index lookup, language-dependent prefixes/accent handling; no BIP39 substitution. Reviewed 2026-09-29; response byte SHA-256 f30f867f5afd3bab323d85a8678868862d94dde09ed7801ab45a74f9b563b447. See docs/research/batches/monero-polyseed.md.
- Evidence claim: Codex component assessment\: reviewed BSD-3-Clause/MIT and Apache-2.0\+MIT data licenses are OSI-approved and impose no commercial dual-licensing; notices are retained. Compatible for this data-only payload. Foundation acceptance, project eligibility and release signing remain unproven. Response-body SHA-256 6610cf889bbe0dc7533abaa310bc7a5cc9a61ae6c2ce0798a08109c925b46c51.
- Evidence claim: Exact ordered dictionary array and applicable file-level license header reviewed. Source-token extraction and byte hashes are independently checked against the public fixture; no complete phrase is stored here. Reviewed 2026-09-29; response byte SHA-256 cabe21517dcde33e517926ab29d7b58bb5e5f97b7b5a6a631e9137f256a5165b. See docs/research/batches/monero-polyseed.md.
- Language: zh-hans
- Script: Hans
- Encoding: UTF-8
- Normalization: NFKD
- Word count: 2048
- SHA-256: 5c5942792bd8340cb8b27cd592f1015edf56a8c5b26276ee18a482428e7c5726
- Order rule: Exact upstream array order; zero-based indices. Extract literal UTF-8 tokens unchanged; remove C/C\+\+ wrapper and indentation, append LF after every token. No sorting, lowercasing or Unicode rewriting. Source file and extracted byte hashes in batch note.
- Position rules: Same 2048-entry vocabulary at all 16 positions. First word is polynomial checksum; no BIP39 checksum semantics.; Input uses NFKD; output may compose NFC for accented/Japanese/Korean language flags. Latin prefix matching and French/Spanish accent-insensitivity are separate from stored NFKD bytes.; Language coverage is not a wallet generation claim.
- Source revision: 56f634647d4f75596de20a6259b0cf1933949fdc
- License: Apache-2.0 AND MIT
- Attribution: Copyright \(c\) 2020-2026 tevador; BIP-39 authors copyright 2013. Upstream NOTICE and Apache/MIT terms retained in THIRD\_PARTY\_NOTICES.
- Repository redistribution: allowed
- SignPath compatibility: compatible
- License evidence: [monero-osi-apache](../catalog/evidence/monero-osi-apache.json), [monero-polyseed-license](../catalog/evidence/monero-polyseed-license.json), [monero-polyseed-notice](../catalog/evidence/monero-polyseed-notice.json), [monero-signpath](../catalog/evidence/monero-signpath.json), [polyseed-zh-hans-source](../catalog/evidence/polyseed-zh-hans-source.json)
- Test vectors: —

<a id="dictionary-polyseed-zh-hant"></a>

### polyseed-zh-hant — polyseed-zh-hant

- Source record: [polyseed-zh-hant](../catalog/dictionaries/polyseed-zh-hant.json)
- Status: documented
- Reason: Evidence is insufficient for selectable support.
- Guidance: Not selectable; use the wallet's own backup procedure.
- Version interval (min / max): 56f634647d4f75596de20a6259b0cf1933949fdc / 56f634647d4f75596de20a6259b0cf1933949fdc
- Verified on: 2026-09-29
- Historical: false
- Evidence: [monero-osi-apache](../catalog/evidence/monero-osi-apache.json), [monero-polyseed-license](../catalog/evidence/monero-polyseed-license.json), [monero-polyseed-notice](../catalog/evidence/monero-polyseed-notice.json), [monero-polyseed-rules](../catalog/evidence/monero-polyseed-rules.json), [monero-signpath](../catalog/evidence/monero-signpath.json), [polyseed-zh-hant-source](../catalog/evidence/polyseed-zh-hant-source.json)
- Evidence claim: OSI lists Apache-2.0 as approved. This corroborates only the component-license decision, not project acceptance. Response-body SHA-256 1377faaaa81ba356528c4053d80e32fd12d84b794ed2667f09bf94aaca7458eb.
- Evidence claim: Apache-2.0 permits this modified source-data projection subject to license, notices and modification marking; root project LICENSE contains identical Apache text. No commercial dual-license requirement. Reviewed 2026-09-29; response byte SHA-256 cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30. See docs/research/batches/monero-polyseed.md.
- Evidence claim: Polyseed attribution and BIP39-derived dictionary MIT obligations apply cumulatively with Apache-2.0; complete upstream NOTICE retained in THIRD\_PARTY\_NOTICES. Reviewed 2026-09-29; response byte SHA-256 442cd16cdc8913cd76a9f7bd1047a0aea68ede782d94db3556392e18f39ad64e. See docs/research/batches/monero-polyseed.md.
- Evidence claim: Ten lists, NFKD word invariant, ordinal index lookup, language-dependent prefixes/accent handling; no BIP39 substitution. Reviewed 2026-09-29; response byte SHA-256 f30f867f5afd3bab323d85a8678868862d94dde09ed7801ab45a74f9b563b447. See docs/research/batches/monero-polyseed.md.
- Evidence claim: Codex component assessment\: reviewed BSD-3-Clause/MIT and Apache-2.0\+MIT data licenses are OSI-approved and impose no commercial dual-licensing; notices are retained. Compatible for this data-only payload. Foundation acceptance, project eligibility and release signing remain unproven. Response-body SHA-256 6610cf889bbe0dc7533abaa310bc7a5cc9a61ae6c2ce0798a08109c925b46c51.
- Evidence claim: Exact ordered dictionary array and applicable file-level license header reviewed. Source-token extraction and byte hashes are independently checked against the public fixture; no complete phrase is stored here. Reviewed 2026-09-29; response byte SHA-256 7ddbd0546736c7e53077b97bef5f6697f752f6a78ea7e4429987b66f14a118ba. See docs/research/batches/monero-polyseed.md.
- Language: zh-hant
- Script: Hant
- Encoding: UTF-8
- Normalization: NFKD
- Word count: 2048
- SHA-256: 417b26b3d8500a4ae3d59717d7011952db6fc2fb84b807f3f94ac734e89c1b5f
- Order rule: Exact upstream array order; zero-based indices. Extract literal UTF-8 tokens unchanged; remove C/C\+\+ wrapper and indentation, append LF after every token. No sorting, lowercasing or Unicode rewriting. Source file and extracted byte hashes in batch note.
- Position rules: Same 2048-entry vocabulary at all 16 positions. First word is polynomial checksum; no BIP39 checksum semantics.; Input uses NFKD; output may compose NFC for accented/Japanese/Korean language flags. Latin prefix matching and French/Spanish accent-insensitivity are separate from stored NFKD bytes.; Language coverage is not a wallet generation claim.
- Source revision: 56f634647d4f75596de20a6259b0cf1933949fdc
- License: Apache-2.0 AND MIT
- Attribution: Copyright \(c\) 2020-2026 tevador; BIP-39 authors copyright 2013. Upstream NOTICE and Apache/MIT terms retained in THIRD\_PARTY\_NOTICES.
- Repository redistribution: allowed
- SignPath compatibility: compatible
- License evidence: [monero-osi-apache](../catalog/evidence/monero-osi-apache.json), [monero-polyseed-license](../catalog/evidence/monero-polyseed-license.json), [monero-polyseed-notice](../catalog/evidence/monero-polyseed-notice.json), [monero-signpath](../catalog/evidence/monero-signpath.json), [polyseed-zh-hant-source](../catalog/evidence/polyseed-zh-hant-source.json)
- Test vectors: —

<a id="dictionary-sia-legacy"></a>

### Sia legacy English1626 — sia-legacy

- Source record: [sia-legacy](../catalog/dictionaries/sia-legacy.json)
- Status: verified
- Reason: Verified research record; not a release or security guarantee.
- Version interval (min / max): 7532f67e35008b0f36bbebb20d5a6ee8f14a22f5 / 7532f67e35008b0f36bbebb20d5a6ee8f14a22f5
- Verified on: 2026-09-29
- Historical: true
- Evidence: [sia-codec](../catalog/evidence/sia-codec.json), [sia-codec-vectors](../catalog/evidence/sia-codec-vectors.json), [sia-license](../catalog/evidence/sia-license.json), [sia-list](../catalog/evidence/sia-list.json)
- Evidence claim: Legacy codec is a length-preserving bijective base256/base1626 conversion with little-endian digit order, not Monero three-word chunks; per-word NFC and English prefix matching; FromString splits literal spaces.
- Evidence claim: Ten published codec boundary cases project to byte inputs and dictionary indices; \[90,5\] maps to\[0,0\]. These are codec vectors, not28/29-word wallet recovery vectors.
- Evidence claim: Codex2026-09-29 reviewed MIT root grant \(Copyright2015 Nebulous\) and cumulative Monero2014-2015 BSD-3-Clause english.go terms; full notices retained for list and modified public codec projections. Data-only redistribution allowed, local SignPath OSS compatibility assessed compatible, not Foundation acceptance.
- Evidence claim: Exact siad go.mod dependency\: 1626 English words, source order, unique3-character prefixes, NFC. Explicit Monero BSD-3-Clause file grant; UTF-8 LF extraction changes representation only.
- Language: en
- Script: Latn
- Encoding: UTF-8
- Normalization: NFC
- Word count: 1626
- SHA-256: eaa6bce7dd92f4d6dd74f224264e0ef4ad21095d68ec77616b26ceb599baf4f7
- Order rule: EnglishDictionary array order, zero-based; UTF-8 LF with final newline.
- Position rules: All positions use full list; unique3-character English prefixes; not Monero triplet semantics.
- Source revision: 7532f67e35008b0f36bbebb20d5a6ee8f14a22f5
- License: BSD-3-Clause AND MIT
- Attribution: Copyright2014-2015 The Monero Project; Copyright2015 Nebulous. Full terms in THIRD\_PARTY\_NOTICES; modified UTF-8 LF projection.
- Repository redistribution: allowed
- SignPath compatibility: compatible
- License evidence: [sia-license](../catalog/evidence/sia-license.json), [sia-list](../catalog/evidence/sia-list.json)
- Test vectors: [sia-codec-vectors](../catalog/evidence/sia-codec-vectors.json)

<a id="dictionary-slip39-en"></a>

### SLIP-39 — English — slip39-en

- Source record: [slip39-en](../catalog/dictionaries/slip39-en.json)
- Status: verified
- Reason: Verified research record; not a release or security guarantee.
- Version interval (min / max): 17fcce14736afe498871d3018e4fa9330443471a / 17fcce14736afe498871d3018e4fa9330443471a
- Verified on: 2026-09-29
- Historical: false
- Evidence: [slip39-license](../catalog/evidence/slip39-license.json), [slip39-list](../catalog/evidence/slip39-list.json), [slip39-osi-mit](../catalog/evidence/slip39-osi-mit.json), [slip39-rules](../catalog/evidence/slip39-rules.json), [slip39-signpath](../catalog/evidence/slip39-signpath.json), [slip39-spec](../catalog/evidence/slip39-spec.json), [slip39-vectors](../catalog/evidence/slip39-vectors.json)
- Evidence claim: Codex review 2026-09-29\: MIT covers this repository word-list and public-vector projection; retain SatoshiLabs 2019 copyright and full permission/disclaimer in THIRD\_PARTY\_NOTICES. No implementation library is bundled. Repository redistribution allowed for these exact bytes. See docs/research/batches/slip39-algorand-cardano.md. Retrieved byte SHA-256 332f92f7f90a1c957b473b902a5daf39ad5eb179d8828e0304b4c40faa0123c0.
- Evidence claim: Exact 1024-entry English dictionary. Byte-identical to normative SLIP-0039 list. No transformation or sorting. See docs/research/batches/slip39-algorand-cardano.md. Retrieved byte SHA-256 bcc4555340332d169718aed8bf31dd9d5248cb7da6e5d355140ef4f1e601eec3.
- Evidence claim: Official OSI page inspected through web retrieval on 2026-09-29 confirms MIT as an OSI-approved license. Direct HTTP fetch returned 403; no new raw-body fingerprint or immutable capture asserted. This corroborates component classification, not Foundation acceptance.
- Evidence claim: Big-endian 10-bit indices; 4 metadata words, padded share value, 3 checksum words; threshold/count fields are encoded minus one. All positions use the same list. Source-native input lowercases and splits whitespace, without Unicode normalization. See docs/research/batches/slip39-algorand-cardano.md. Retrieved byte SHA-256 3ee6f46415ba34dd8c1bc5f92601b17151854a35425e098d1de857ca714205c5.
- Evidence claim: Codex local component assessment\: MIT data and public test projections impose no proprietary or commercial dual-license requirement; required attribution/license are retained. Compatible only at component-license level. Foundation acceptance and project/release eligibility remain unproven. See docs/research/batches/slip39-algorand-cardano.md. Retrieved byte SHA-256 6610cf889bbe0dc7533abaa310bc7a5cc9a61ae6c2ce0798a08109c925b46c51.
- Evidence claim: Format of the share mnemonic, Two-level scheme, Checksum and Passphrase sections define 20/33 words for 128/256 bits; 15-bit ID, extendable flag, exponent, group/member fields and three RS1024 words. Standard allows other lengths; catalogue scope only 20/33. Tessaveil stores neither complete shares nor thresholds as recovered secrets and never combines/reconstructs shares. See docs/research/batches/slip39-algorand-cardano.md. Retrieved byte SHA-256 7b4269f66f10f03ac685ea7c76f742bfbf56211af1af29339eadef9acba1f856.
- Evidence claim: Public cases 1, 4, 17, 20, 42, 44 projected into indices/fingerprints; tests check individual-share metadata/padding/RS1024 only. No combining, master-secret recovery, decryption or wallet derivation is executed. See docs/research/batches/slip39-algorand-cardano.md. Retrieved byte SHA-256 13ebecebdd869dd2bc2cdf69e7ce3a158cf106cac76c39d17682b1c6cdabbdc4.
- Language: en
- Script: Latn
- Encoding: UTF-8
- Normalization: none
- Word count: 1024
- SHA-256: bcc4555340332d169718aed8bf31dd9d5248cb7da6e5d355140ef4f1e601eec3
- Order rule: Unchanged upstream UTF-8 LF bytes including final LF. Zero-based 10-bit indices in source order; no sort, normalization or case rewriting.
- Position rules: Same 1024-word vocabulary at every share position. First four words encode metadata, last three are RS1024 checksum; metadata is not BIP39 entropy.; Only ASCII words; source input lowercases and splits whitespace. Never combine shares or evaluate user-share validity in Tessaveil.
- Source revision: 17fcce14736afe498871d3018e4fa9330443471a
- License: MIT
- Attribution: Copyright 2019 SatoshiLabs. Complete MIT notice in THIRD\_PARTY\_NOTICES.
- Repository redistribution: allowed
- SignPath compatibility: compatible
- License evidence: [slip39-license](../catalog/evidence/slip39-license.json), [slip39-osi-mit](../catalog/evidence/slip39-osi-mit.json), [slip39-signpath](../catalog/evidence/slip39-signpath.json)
- Test vectors: [slip39-vectors](../catalog/evidence/slip39-vectors.json)

<a id="dictionary-zano-en"></a>

### Zano English — provenance blocked — zano-en

- Source record: [zano-en](../catalog/dictionaries/zano-en.json)
- Status: blocked
- Reason: Support is blocked; see evidence and license decisions below.
- Guidance: Not selectable; use the wallet's own backup procedure.
- Version interval (min / max): e55c8ec47b76ed809162a958cf4600e03256a96a / e55c8ec47b76ed809162a958cf4600e03256a96a
- Verified on: 2026-09-29
- Historical: false
- Evidence: [zano-codec](../catalog/evidence/zano-codec.json), [zano-license](../catalog/evidence/zano-license.json)
- Evidence claim: Exact 1626 English indices; eight native little-endian 32-bit groups become 24 words in eight dependent modulo-1626 triplets. List equals Electrum v1 tuple in order, not Monero current English or BIP39. Case-sensitive membership; no lowercase or Unicode normalization is applied by this codec.
- Evidence claim: Reviewed root MIT-like grant and mnemonic file BSD-3-Clause header. Exact list matches Electrum-old's Wiktionary-derived vocabulary; original frequency-list data-license provenance remains unresolved. Codex2026-09-29\: unclear redistribution/pending SignPath, no list bytes bundled.
- Language: en
- Script: Latn
- Encoding: UTF-8
- Normalization: none
- Word count: 1626
- SHA-256: —
- Order rule: Exact numeric indices; matches Electrum-old tuple. No approved committed byte artifact.
- Position rules: Triplets encode32-bit groups; metadata words25/26 also use same1626 indices.
- Source revision: e55c8ec47b76ed809162a958cf4600e03256a96a
- License: BSD-3-Clause file; original frequency-list rights unresolved
- Attribution: Monero2014; Zano/Louisdor2014-2018; Electrum-old/Wiktionary source chain requires review.
- Repository redistribution: unclear
- SignPath compatibility: pending
- License evidence: [zano-license](../catalog/evidence/zano-license.json)
- Test vectors: —

## Evidence revisions

- [algorand-algorithm](../catalog/evidence/algorand-algorithm.json): official-source; 189855d43cba5d20e66248693d74332052ccb08e; 2026-09-29
- [algorand-defly-create](../catalog/evidence/algorand-defly-create.json): official-documentation; reviewed-2026-09-29-version-unpublished; 2026-09-29
- [algorand-dictionary](../catalog/evidence/algorand-dictionary.json): official-source; 189855d43cba5d20e66248693d74332052ccb08e; 2026-09-29
- [algorand-license](../catalog/evidence/algorand-license.json): official-source; 189855d43cba5d20e66248693d74332052ccb08e; 2026-09-29
- [algorand-pera-backup](../catalog/evidence/algorand-pera-backup.json): official-documentation; snapshot-2026-09-29-sha256-4fad7c798ef8891ca31f4ee64051c570fd8d4952665f70738635c26eb425c9d6; 2026-09-29
- [algorand-pera-migration](../catalog/evidence/algorand-pera-migration.json): official-documentation; snapshot-2026-09-29-sha256-30fa382990ea359398ccde9c9a4ccdd2e031b6b83721f9aede4cb46cb57c506b; 2026-09-29
- [algorand-pera-universal](../catalog/evidence/algorand-pera-universal.json): official-documentation; snapshot-2026-09-29-sha256-d54c39508a76f426bd3958cfbae5600d8f737aa05d4356540be617986a4c0b81; 2026-09-29
- [algorand-vectors](../catalog/evidence/algorand-vectors.json): public-test-vector; 189855d43cba5d20e66248693d74332052ccb08e; 2026-09-29
- [bip39-guidance](../catalog/evidence/bip39-guidance.json): official-specification; 3a10b5b5f0a7586df8928d580a3009744ebb2079; 2026-09-29
- [bip39-license](../catalog/evidence/bip39-license.json): official-source; b57a5ad77a981e743f4167ab2f7927a55c1e82a8; 2026-09-29
- [bip39-osi-mit](../catalog/evidence/bip39-osi-mit.json): official-documentation; sha256\:004c79db0a335488afc87600d89f447dce7fb4d24d510af15ed4381a24be848c; 2026-09-29
- [bip39-signpath](../catalog/evidence/bip39-signpath.json): official-documentation; sha256\:6610cf889bbe0dc7533abaa310bc7a5cc9a61ae6c2ce0798a08109c925b46c51; 2026-09-29
- [bip39-spec](../catalog/evidence/bip39-spec.json): official-specification; 3a10b5b5f0a7586df8928d580a3009744ebb2079; 2026-09-29
- [bip39-vectors](../catalog/evidence/bip39-vectors.json): public-test-vector; b57a5ad77a981e743f4167ab2f7927a55c1e82a8; 2026-09-29
- [cardano-byron-rules](../catalog/evidence/cardano-byron-rules.json): official-specification; 4ca4dcefccc7143672cf07a0b760d9e5abfc7797; 2026-09-29
- [cardano-cip3](../catalog/evidence/cardano-cip3.json): official-specification; 4ca4dcefccc7143672cf07a0b760d9e5abfc7797; 2026-09-29
- [cardano-daedalus-create](../catalog/evidence/cardano-daedalus-create.json): official-source; 6c57eb94753211f66d3a63f49d031bf746044755; 2026-09-29
- [cardano-daedalus-dictionary](../catalog/evidence/cardano-daedalus-dictionary.json): official-source; 6c57eb94753211f66d3a63f49d031bf746044755; 2026-09-29
- [cardano-daedalus-lengths](../catalog/evidence/cardano-daedalus-lengths.json): official-source; 6c57eb94753211f66d3a63f49d031bf746044755; 2026-09-29
- [cardano-daedalus-restore](../catalog/evidence/cardano-daedalus-restore.json): official-source; 6c57eb94753211f66d3a63f49d031bf746044755; 2026-09-29
- [cardano-daedalus-version](../catalog/evidence/cardano-daedalus-version.json): official-source; 6c57eb94753211f66d3a63f49d031bf746044755; 2026-09-29
- [cardano-eternl-doc](../catalog/evidence/cardano-eternl-doc.json): official-documentation; reviewed-2026-09-29-version-unpublished; 2026-09-29
- [cardano-hardware-rules](../catalog/evidence/cardano-hardware-rules.json): official-specification; 4ca4dcefccc7143672cf07a0b760d9e5abfc7797; 2026-09-29
- [cardano-icarus-rules](../catalog/evidence/cardano-icarus-rules.json): official-specification; 4ca4dcefccc7143672cf07a0b760d9e5abfc7797; 2026-09-29
- [cardano-lace-create](../catalog/evidence/cardano-lace-create.json): official-documentation; snapshot-2026-09-29-sha256-ce02d32706cf597d8f3861e3040d487d7e8862020069ccdf6e40aa48b7a83f19; 2026-09-29
- [cardano-nami-create](../catalog/evidence/cardano-nami-create.json): official-source; e52e0bdb02eb1ec224db26f48b0192685a30f99e; 2026-09-29
- [cardano-nami-derive](../catalog/evidence/cardano-nami-derive.json): official-source; e52e0bdb02eb1ec224db26f48b0192685a30f99e; 2026-09-29
- [cardano-nami-version](../catalog/evidence/cardano-nami-version.json): official-source; e52e0bdb02eb1ec224db26f48b0192685a30f99e; 2026-09-29
- [cardano-paper-license](../catalog/evidence/cardano-paper-license.json): official-source; 6c57eb94753211f66d3a63f49d031bf746044755; 2026-09-29
- [cardano-paper-rules](../catalog/evidence/cardano-paper-rules.json): official-source; 6c57eb94753211f66d3a63f49d031bf746044755; 2026-09-29
- [cardano-paper-vector](../catalog/evidence/cardano-paper-vector.json): public-test-vector; 6c57eb94753211f66d3a63f49d031bf746044755; 2026-09-29
- [cardano-typhon-create](../catalog/evidence/cardano-typhon-create.json): official-documentation; reviewed-2026-09-29-version-unpublished; 2026-09-29
- [cardano-yoroi-backup](../catalog/evidence/cardano-yoroi-backup.json): official-source; 91febfc95a288d3436b891356c87645611ea603a; 2026-09-29
- [cardano-yoroi-create](../catalog/evidence/cardano-yoroi-create.json): official-source; 91febfc95a288d3436b891356c87645611ea603a; 2026-09-29
- [chia-license](../catalog/evidence/chia-license.json): official-source; af0d7eab5fb12bbd8af51f47a7123ee700d74c2a; 2026-09-29
- [chia-source](../catalog/evidence/chia-source.json): official-source; af0d7eab5fb12bbd8af51f47a7123ee700d74c2a; 2026-09-29
- [chia-vectors](../catalog/evidence/chia-vectors.json): public-test-vector; af0d7eab5fb12bbd8af51f47a7123ee700d74c2a; 2026-09-29
- [decred-bip39-doc](../catalog/evidence/decred-bip39-doc.json): official-source; 30e042a46a97cf78f9766904d3ca4e5ed253266d; 2026-09-29
- [decred-cake-build](../catalog/evidence/decred-cake-build.json): official-source; 9679f91a8c9f63d00500c2b7cc18daf00949bdef; 2026-09-29
- [decred-cake-create](../catalog/evidence/decred-cake-create.json): official-source; 9679f91a8c9f63d00500c2b7cc18daf00949bdef; 2026-09-29
- [decred-cake-dependency](../catalog/evidence/decred-cake-dependency.json): official-source; ecc4a5fb9594368777848de42d7e072d62406507; 2026-09-29
- [decred-cake-dispatch](../catalog/evidence/decred-cake-dispatch.json): official-source; ecc4a5fb9594368777848de42d7e072d62406507; 2026-09-29
- [decred-cake-doc](../catalog/evidence/decred-cake-doc.json): official-documentation; retrieved-2026-09-29; 2026-09-29
- [decred-cake-native](../catalog/evidence/decred-cake-native.json): official-source; 37585833528544f80dddd92dcdff10a78ad01e1f; 2026-09-29
- [decred-cake-nfc](../catalog/evidence/decred-cake-nfc.json): official-source; ecc4a5fb9594368777848de42d7e072d62406507; 2026-09-29
- [decred-cake-seed](../catalog/evidence/decred-cake-seed.json): official-source; ecc4a5fb9594368777848de42d7e072d62406507; 2026-09-29
- [decred-cake-words](../catalog/evidence/decred-cake-words.json): official-source; 37585833528544f80dddd92dcdff10a78ad01e1f; 2026-09-29
- [decred-decrediton-create](../catalog/evidence/decred-decrediton-create.json): official-source; 942eed0b34d09316d753942abdbec8dc5320cbed; 2026-09-29
- [decred-decrediton-license](../catalog/evidence/decred-decrediton-license.json): official-source; 942eed0b34d09316d753942abdbec8dc5320cbed; 2026-09-29
- [decred-pgp-checksum](../catalog/evidence/decred-pgp-checksum.json): official-source; c0fee6b52ad30961cfc3e06017d5e7516952615e; 2026-09-29
- [decred-pgp-license](../catalog/evidence/decred-pgp-license.json): official-source; c0fee6b52ad30961cfc3e06017d5e7516952615e; 2026-09-29
- [decred-pgp-list](../catalog/evidence/decred-pgp-list.json): official-source; c0fee6b52ad30961cfc3e06017d5e7516952615e; 2026-09-29
- [decred-pgp-osi](../catalog/evidence/decred-pgp-osi.json): official-documentation; retrieved-2026-09-29; 2026-09-29
- [decred-pgp-position](../catalog/evidence/decred-pgp-position.json): official-source; c0fee6b52ad30961cfc3e06017d5e7516952615e; 2026-09-29
- [decred-pgp-signpath](../catalog/evidence/decred-pgp-signpath.json): official-documentation; retrieved-2026-09-29; 2026-09-29
- [decred-pgp-vectors](../catalog/evidence/decred-pgp-vectors.json): public-test-vector; c0fee6b52ad30961cfc3e06017d5e7516952615e; 2026-09-29
- [decred-pgp33-reference](../catalog/evidence/decred-pgp33-reference.json): public-test-vector; 942eed0b34d09316d753942abdbec8dc5320cbed; 2026-09-29
- [electrum-legacy-license](../catalog/evidence/electrum-legacy-license.json): official-source; ede66c89887234c83b0def133b3100fe92a160eb; 2026-09-29
- [electrum-legacy-list](../catalog/evidence/electrum-legacy-list.json): official-source; ede66c89887234c83b0def133b3100fe92a160eb; 2026-09-29
- [electrum-public-vectors](../catalog/evidence/electrum-public-vectors.json): public-test-vector; ede66c89887234c83b0def133b3100fe92a160eb; 2026-09-29
- [electrum-qt-create](../catalog/evidence/electrum-qt-create.json): official-source; ede66c89887234c83b0def133b3100fe92a160eb; 2026-09-29
- [electrum-v2-dictionary](../catalog/evidence/electrum-v2-dictionary.json): official-source; ede66c89887234c83b0def133b3100fe92a160eb; 2026-09-29
- [electrum-v2-source](../catalog/evidence/electrum-v2-source.json): official-source; ede66c89887234c83b0def133b3100fe92a160eb; 2026-09-29
- [electrum-vector-license](../catalog/evidence/electrum-vector-license.json): official-source; ede66c89887234c83b0def133b3100fe92a160eb; 2026-09-29
- [electrum-version](../catalog/evidence/electrum-version.json): official-source; ede66c89887234c83b0def133b3100fe92a160eb; 2026-09-29
- [electrum-wizard-modes](../catalog/evidence/electrum-wizard-modes.json): official-source; ede66c89887234c83b0def133b3100fe92a160eb; 2026-09-29
- [monero-cake-export](../catalog/evidence/monero-cake-export.json): official-source; 9679f91a8c9f63d00500c2b7cc18daf00949bdef; 2026-09-29
- [monero-cake-seed](../catalog/evidence/monero-cake-seed.json): official-source; 9679f91a8c9f63d00500c2b7cc18daf00949bdef; 2026-09-29
- [monero-cake-ui](../catalog/evidence/monero-cake-ui.json): official-source; 9679f91a8c9f63d00500c2b7cc18daf00949bdef; 2026-09-29
- [monero-cake-version](../catalog/evidence/monero-cake-version.json): official-source; 9679f91a8c9f63d00500c2b7cc18daf00949bdef; 2026-09-29
- [monero-cake-wallet-monero-bip39-wallet](../catalog/evidence/monero-cake-wallet-monero-bip39-wallet.json): official-source; 9679f91a8c9f63d00500c2b7cc18daf00949bdef; 2026-09-29
- [monero-cake-wallet-monero-legacy-wallet](../catalog/evidence/monero-cake-wallet-monero-legacy-wallet.json): official-source; 9679f91a8c9f63d00500c2b7cc18daf00949bdef; 2026-09-29
- [monero-cake-wallet-monero-wallet](../catalog/evidence/monero-cake-wallet-monero-wallet.json): official-source; 9679f91a8c9f63d00500c2b7cc18daf00949bdef; 2026-09-29
- [monero-cli-version](../catalog/evidence/monero-cli-version.json): official-source; 2f9d1bbb2c553dc75f3335bd1452117dfddd86fa; 2026-09-29
- [monero-de-source](../catalog/evidence/monero-de-source.json): official-source; 2f9d1bbb2c553dc75f3335bd1452117dfddd86fa; 2026-09-29
- [monero-en-old-source](../catalog/evidence/monero-en-old-source.json): official-source; 2f9d1bbb2c553dc75f3335bd1452117dfddd86fa; 2026-09-29
- [monero-en-source](../catalog/evidence/monero-en-source.json): official-source; 2f9d1bbb2c553dc75f3335bd1452117dfddd86fa; 2026-09-29
- [monero-eo-source](../catalog/evidence/monero-eo-source.json): official-source; 2f9d1bbb2c553dc75f3335bd1452117dfddd86fa; 2026-09-29
- [monero-es-source](../catalog/evidence/monero-es-source.json): official-source; 2f9d1bbb2c553dc75f3335bd1452117dfddd86fa; 2026-09-29
- [monero-exodus-doc](../catalog/evidence/monero-exodus-doc.json): official-documentation; published-update-2026-01-20-reviewed-2026-09-29; 2026-09-29
- [monero-feather-create](../catalog/evidence/monero-feather-create.json): official-source; 948773cf13c7486ee230eb67b6bac06b2f94c874; 2026-09-29
- [monero-feather-legacy-import-wallet](../catalog/evidence/monero-feather-legacy-import-wallet.json): official-source; 948773cf13c7486ee230eb67b6bac06b2f94c874; 2026-09-29
- [monero-feather-version](../catalog/evidence/monero-feather-version.json): official-source; 948773cf13c7486ee230eb67b6bac06b2f94c874; 2026-09-29
- [monero-feather-wallet](../catalog/evidence/monero-feather-wallet.json): official-source; 948773cf13c7486ee230eb67b6bac06b2f94c874; 2026-09-29
- [monero-fr-source](../catalog/evidence/monero-fr-source.json): official-source; 2f9d1bbb2c553dc75f3335bd1452117dfddd86fa; 2026-09-29
- [monero-it-source](../catalog/evidence/monero-it-source.json): official-source; 2f9d1bbb2c553dc75f3335bd1452117dfddd86fa; 2026-09-29
- [monero-ja-source](../catalog/evidence/monero-ja-source.json): official-source; 2f9d1bbb2c553dc75f3335bd1452117dfddd86fa; 2026-09-29
- [monero-jbo-source](../catalog/evidence/monero-jbo-source.json): official-source; 2f9d1bbb2c553dc75f3335bd1452117dfddd86fa; 2026-09-29
- [monero-legacy-vectors](../catalog/evidence/monero-legacy-vectors.json): public-test-vector; 2f9d1bbb2c553dc75f3335bd1452117dfddd86fa; 2026-09-29
- [monero-monero-cli-polyseed-wallet](../catalog/evidence/monero-monero-cli-polyseed-wallet.json): official-source; 2f9d1bbb2c553dc75f3335bd1452117dfddd86fa; 2026-09-29
- [monero-monero-gui-cli-wallet](../catalog/evidence/monero-monero-gui-cli-wallet.json): official-source; 2f9d1bbb2c553dc75f3335bd1452117dfddd86fa; 2026-09-29
- [monero-monero-gui-wallet](../catalog/evidence/monero-monero-gui-wallet.json): official-source; 01d6640aff7fd1c1a87932e14e8439383e1229c5; 2026-09-29
- [monero-monero-legacy-scheme](../catalog/evidence/monero-monero-legacy-scheme.json): official-source; 2f9d1bbb2c553dc75f3335bd1452117dfddd86fa; 2026-09-29
- [monero-monero-license](../catalog/evidence/monero-monero-license.json): official-source; 2f9d1bbb2c553dc75f3335bd1452117dfddd86fa; 2026-09-29
- [monero-monero-rules](../catalog/evidence/monero-monero-rules.json): official-source; 2f9d1bbb2c553dc75f3335bd1452117dfddd86fa; 2026-09-29
- [monero-my-core](../catalog/evidence/monero-my-core.json): official-source; 9637c91cbe5f46e67156c66c739932294808109d; 2026-09-29
- [monero-mymonero-13-scheme](../catalog/evidence/monero-mymonero-13-scheme.json): official-source; 9637c91cbe5f46e67156c66c739932294808109d; 2026-09-29
- [monero-mymonero-generated-wallet](../catalog/evidence/monero-mymonero-generated-wallet.json): official-source; 5c7455d30e4e20150962f5f74efd83477962a05e; 2026-09-29
- [monero-mymonero-vectors](../catalog/evidence/monero-mymonero-vectors.json): public-test-vector; 9637c91cbe5f46e67156c66c739932294808109d; 2026-09-29
- [monero-mymonero-wallet](../catalog/evidence/monero-mymonero-wallet.json): official-source; 5c7455d30e4e20150962f5f74efd83477962a05e; 2026-09-29
- [monero-nl-source](../catalog/evidence/monero-nl-source.json): official-source; 2f9d1bbb2c553dc75f3335bd1452117dfddd86fa; 2026-09-29
- [monero-osi-apache](../catalog/evidence/monero-osi-apache.json): official-documentation; snapshot-2026-09-29-sha256-1377faaaa81ba356528c4053d80e32fd12d84b794ed2667f09bf94aaca7458eb; 2026-09-29
- [monero-osi-bsd](../catalog/evidence/monero-osi-bsd.json): official-documentation; snapshot-2026-09-29-sha256-0dfece33194f06d15b862c323f7ed32ba6ab7f512a7fda11880bb2e1401518f8; 2026-09-29
- [monero-osi-mit](../catalog/evidence/monero-osi-mit.json): official-documentation; sha256\:004c79db0a335488afc87600d89f447dce7fb4d24d510af15ed4381a24be848c; 2026-09-29
- [monero-polyseed-16-scheme](../catalog/evidence/monero-polyseed-16-scheme.json): official-source; 56f634647d4f75596de20a6259b0cf1933949fdc; 2026-09-29
- [monero-polyseed-license](../catalog/evidence/monero-polyseed-license.json): official-source; 56f634647d4f75596de20a6259b0cf1933949fdc; 2026-09-29
- [monero-polyseed-notice](../catalog/evidence/monero-polyseed-notice.json): official-source; 56f634647d4f75596de20a6259b0cf1933949fdc; 2026-09-29
- [monero-polyseed-rules](../catalog/evidence/monero-polyseed-rules.json): official-source; 56f634647d4f75596de20a6259b0cf1933949fdc; 2026-09-29
- [monero-polyseed-vectors](../catalog/evidence/monero-polyseed-vectors.json): public-test-vector; 56f634647d4f75596de20a6259b0cf1933949fdc; 2026-09-29
- [monero-pt-source](../catalog/evidence/monero-pt-source.json): official-source; 2f9d1bbb2c553dc75f3335bd1452117dfddd86fa; 2026-09-29
- [monero-ru-source](../catalog/evidence/monero-ru-source.json): official-source; 2f9d1bbb2c553dc75f3335bd1452117dfddd86fa; 2026-09-29
- [monero-signpath](../catalog/evidence/monero-signpath.json): official-documentation; snapshot-2026-09-29-sha256-6610cf889bbe0dc7533abaa310bc7a5cc9a61ae6c2ce0798a08109c925b46c51; 2026-09-29
- [monero-zh-hans-source](../catalog/evidence/monero-zh-hans-source.json): official-source; 2f9d1bbb2c553dc75f3335bd1452117dfddd86fa; 2026-09-29
- [polyseed-cs-source](../catalog/evidence/polyseed-cs-source.json): official-source; 56f634647d4f75596de20a6259b0cf1933949fdc; 2026-09-29
- [polyseed-en-source](../catalog/evidence/polyseed-en-source.json): official-source; 56f634647d4f75596de20a6259b0cf1933949fdc; 2026-09-29
- [polyseed-es-source](../catalog/evidence/polyseed-es-source.json): official-source; 56f634647d4f75596de20a6259b0cf1933949fdc; 2026-09-29
- [polyseed-fr-source](../catalog/evidence/polyseed-fr-source.json): official-source; 56f634647d4f75596de20a6259b0cf1933949fdc; 2026-09-29
- [polyseed-it-source](../catalog/evidence/polyseed-it-source.json): official-source; 56f634647d4f75596de20a6259b0cf1933949fdc; 2026-09-29
- [polyseed-ja-source](../catalog/evidence/polyseed-ja-source.json): official-source; 56f634647d4f75596de20a6259b0cf1933949fdc; 2026-09-29
- [polyseed-ko-source](../catalog/evidence/polyseed-ko-source.json): official-source; 56f634647d4f75596de20a6259b0cf1933949fdc; 2026-09-29
- [polyseed-pt-source](../catalog/evidence/polyseed-pt-source.json): official-source; 56f634647d4f75596de20a6259b0cf1933949fdc; 2026-09-29
- [polyseed-zh-hans-source](../catalog/evidence/polyseed-zh-hans-source.json): official-source; 56f634647d4f75596de20a6259b0cf1933949fdc; 2026-09-29
- [polyseed-zh-hant-source](../catalog/evidence/polyseed-zh-hant-source.json): official-source; 56f634647d4f75596de20a6259b0cf1933949fdc; 2026-09-29
- [sia-codec](../catalog/evidence/sia-codec.json): official-source; 7532f67e35008b0f36bbebb20d5a6ee8f14a22f5; 2026-09-29
- [sia-codec-vectors](../catalog/evidence/sia-codec-vectors.json): public-test-vector; 7532f67e35008b0f36bbebb20d5a6ee8f14a22f5; 2026-09-29
- [sia-current-codec](../catalog/evidence/sia-current-codec.json): official-source; 024db888b8bb80b5e54876baaf868c03c9aa0902; 2026-09-29
- [sia-license](../catalog/evidence/sia-license.json): official-source; 7532f67e35008b0f36bbebb20d5a6ee8f14a22f5; 2026-09-29
- [sia-list](../catalog/evidence/sia-list.json): official-source; 7532f67e35008b0f36bbebb20d5a6ee8f14a22f5; 2026-09-29
- [sia-server-boundary](../catalog/evidence/sia-server-boundary.json): official-source; aa523f95c5b2a106a3c0d9675205c90305d2d9d9; 2026-09-29
- [sia-siad-dependency](../catalog/evidence/sia-siad-dependency.json): official-source; 66e7fc630585887c30033379d2a0a8bf5c618177; 2026-09-29
- [sia-siad-seed](../catalog/evidence/sia-siad-seed.json): official-source; 66e7fc630585887c30033379d2a0a8bf5c618177; 2026-09-29
- [sia-ui-history](../catalog/evidence/sia-ui-history.json): official-source; cd7e221b98fc7a395de25bd8dfaa4f4de2a6e3d2; 2026-09-29
- [sia-web-create](../catalog/evidence/sia-web-create.json): official-source; f4e3ff774c4f6a5b9830abf1767485215a26a349; 2026-09-29
- [sia-web-sdk](../catalog/evidence/sia-web-sdk.json): official-source; f4e3ff774c4f6a5b9830abf1767485215a26a349; 2026-09-29
- [slip39-license](../catalog/evidence/slip39-license.json): official-source; 17fcce14736afe498871d3018e4fa9330443471a; 2026-09-29
- [slip39-list](../catalog/evidence/slip39-list.json): official-source; 17fcce14736afe498871d3018e4fa9330443471a; 2026-09-29
- [slip39-osi-mit](../catalog/evidence/slip39-osi-mit.json): official-documentation; reviewed-2026-09-29-version-unpublished; 2026-09-29
- [slip39-rules](../catalog/evidence/slip39-rules.json): official-source; 17fcce14736afe498871d3018e4fa9330443471a; 2026-09-29
- [slip39-signpath](../catalog/evidence/slip39-signpath.json): official-documentation; snapshot-2026-09-29-sha256-6610cf889bbe0dc7533abaa310bc7a5cc9a61ae6c2ce0798a08109c925b46c51; 2026-09-29
- [slip39-spec](../catalog/evidence/slip39-spec.json): official-specification; 570ed55b7fde158f1116be34fc2faa35dada5912; 2026-09-29
- [slip39-trezor-model-t](../catalog/evidence/slip39-trezor-model-t.json): official-documentation; reviewed-2026-09-29-version-unpublished; 2026-09-29
- [slip39-trezor-safe-3](../catalog/evidence/slip39-trezor-safe-3.json): official-documentation; reviewed-2026-09-29-version-unpublished; 2026-09-29
- [slip39-trezor-safe-5](../catalog/evidence/slip39-trezor-safe-5.json): official-documentation; reviewed-2026-09-29-version-unpublished; 2026-09-29
- [slip39-trezor-safe-7](../catalog/evidence/slip39-trezor-safe-7.json): official-documentation; reviewed-2026-09-29-version-unpublished; 2026-09-29
- [slip39-vectors](../catalog/evidence/slip39-vectors.json): public-test-vector; 17fcce14736afe498871d3018e4fa9330443471a; 2026-09-29
- [substrate-entropy](../catalog/evidence/substrate-entropy.json): official-source; ceb4fe5a3c7ac91da2e272037797ebecb56aa177; 2026-09-29
- [substrate-polkadot-create](../catalog/evidence/substrate-polkadot-create.json): official-source; 54f44022004f4cefb4a2b929f3a397715a134d6f; 2026-09-29
- [substrate-polkadot-type](../catalog/evidence/substrate-polkadot-type.json): official-source; 54f44022004f4cefb4a2b929f3a397715a134d6f; 2026-09-29
- [substrate-polkadot-ui](../catalog/evidence/substrate-polkadot-ui.json): official-source; 54f44022004f4cefb4a2b929f3a397715a134d6f; 2026-09-29
- [substrate-subwallet](../catalog/evidence/substrate-subwallet.json): official-source; 1f9b2a4cb6fea68193e5e012dcca7284a1dd0d80; 2026-09-29
- [substrate-talisman](../catalog/evidence/substrate-talisman.json): official-source; 2cee3ef46633cdc3e90bb0fed6855fa25fc87692; 2026-09-29
- [substrate-talisman-ui](../catalog/evidence/substrate-talisman-ui.json): official-source; 2cee3ef46633cdc3e90bb0fed6855fa25fc87692; 2026-09-29
- [substrate-vector-license](../catalog/evidence/substrate-vector-license.json): official-source; ceb4fe5a3c7ac91da2e272037797ebecb56aa177; 2026-09-29
- [substrate-vectors](../catalog/evidence/substrate-vectors.json): public-test-vector; ceb4fe5a3c7ac91da2e272037797ebecb56aa177; 2026-09-29
- [ton-gram-identity](../catalog/evidence/ton-gram-identity.json): official-documentation; sha256\:c498efe1d81425f59fb294f1184c5a64ddd913c5cc22784759d2bd58691e7da2; 2026-09-29
- [ton-gram-store](../catalog/evidence/ton-gram-store.json): official-documentation; sha256\:3f2c0e813940801893d846b36313173f6e7a2865b1bc41d80cc74fd1c90a2518; 2026-09-29
- [ton-keeper-doc](../catalog/evidence/ton-keeper-doc.json): official-documentation; sha256\:d7091696af9e14b254c181906e1a8e8b48a339835ae65ac753593cabcbcb768a; 2026-09-29
- [ton-my-auth](../catalog/evidence/ton-my-auth.json): official-source; f042bcc06b84f0cec928a29795f1cb8bf60a3e9c; 2026-09-29
- [ton-my-backup](../catalog/evidence/ton-my-backup.json): official-source; f042bcc06b84f0cec928a29795f1cb8bf60a3e9c; 2026-09-29
- [ton-my-common](../catalog/evidence/ton-my-common.json): official-source; f042bcc06b84f0cec928a29795f1cb8bf60a3e9c; 2026-09-29
- [ton-my-create](../catalog/evidence/ton-my-create.json): official-source; f042bcc06b84f0cec928a29795f1cb8bf60a3e9c; 2026-09-29
- [ton-my-derive](../catalog/evidence/ton-my-derive.json): official-source; f042bcc06b84f0cec928a29795f1cb8bf60a3e9c; 2026-09-29
- [ton-my-path](../catalog/evidence/ton-my-path.json): official-source; f042bcc06b84f0cec928a29795f1cb8bf60a3e9c; 2026-09-29
- [ton-my-version](../catalog/evidence/ton-my-version.json): official-source; f042bcc06b84f0cec928a29795f1cb8bf60a3e9c; 2026-09-29
- [ton-native-license](../catalog/evidence/ton-native-license.json): official-source; c3435833a0da52a96f674c352c4c6f91fcc07f6d; 2026-09-29
- [ton-native-source](../catalog/evidence/ton-native-source.json): official-source; c3435833a0da52a96f674c352c4c6f91fcc07f6d; 2026-09-29
- [ton-native-vectors](../catalog/evidence/ton-native-vectors.json): public-test-vector; c3435833a0da52a96f674c352c4c6f91fcc07f6d; 2026-09-29
- [ton-native-wordlist](../catalog/evidence/ton-native-wordlist.json): official-source; c3435833a0da52a96f674c352c4c6f91fcc07f6d; 2026-09-29
- [ton-openmask-create](../catalog/evidence/ton-openmask-create.json): official-source; 9150d57d530296f8b27ae59e4dfce865be81550e; 2026-09-29
- [ton-openmask-identity](../catalog/evidence/ton-openmask-identity.json): official-source; 9150d57d530296f8b27ae59e4dfce865be81550e; 2026-09-29
- [ton-openmask-version](../catalog/evidence/ton-openmask-version.json): official-source; 9150d57d530296f8b27ae59e4dfce865be81550e; 2026-09-29
- [ton-space-doc](../catalog/evidence/ton-space-doc.json): official-documentation; sha256\:506a3bc3c0a4861601fc606c90320acac8d4a2bd91a639b27190567530006d37; 2026-09-29
- [ton-space-security](../catalog/evidence/ton-space-security.json): official-documentation; sha256\:7f5a40f0e43d00d2a620972b9f2a1a5370ed4ad660f6d65d5ca25bc36f71b8dd; 2026-09-29
- [ton-tep3](../catalog/evidence/ton-tep3.json): official-specification; fe8a154e4dad9f5c0bf7240df278cb50ec6cd908; 2026-09-29
- [ton-tonweb-generate](../catalog/evidence/ton-tonweb-generate.json): official-source; a338a00d4ca0ed833431e0e49e4cfad766ac713c; 2026-09-29
- [ton-tonweb-seed](../catalog/evidence/ton-tonweb-seed.json): official-source; a338a00d4ca0ed833431e0e49e4cfad766ac713c; 2026-09-29
- [ton-tonweb-version](../catalog/evidence/ton-tonweb-version.json): official-source; a338a00d4ca0ed833431e0e49e4cfad766ac713c; 2026-09-29
- [tonhub-create](../catalog/evidence/tonhub-create.json): official-source; a2503f79d14868d65349ad7035d18389c6e2f996; 2026-09-29
- [tonhub-derive](../catalog/evidence/tonhub-derive.json): official-source; a2503f79d14868d65349ad7035d18389c6e2f996; 2026-09-29
- [tonhub-identity](../catalog/evidence/tonhub-identity.json): official-source; a2503f79d14868d65349ad7035d18389c6e2f996; 2026-09-29
- [tonhub-version](../catalog/evidence/tonhub-version.json): official-source; a2503f79d14868d65349ad7035d18389c6e2f996; 2026-09-29
- [tonkeeper-create](../catalog/evidence/tonkeeper-create.json): official-source; 4942adcdcddf55d57e3d3fc3676f019caf87357e; 2026-09-29
- [tonkeeper-derive](../catalog/evidence/tonkeeper-derive.json): official-source; 4942adcdcddf55d57e3d3fc3676f019caf87357e; 2026-09-29
- [tonkeeper-version](../catalog/evidence/tonkeeper-version.json): official-source; 4942adcdcddf55d57e3d3fc3676f019caf87357e; 2026-09-29
- [zano-cake-bip39](../catalog/evidence/zano-cake-bip39.json): official-source; 9679f91a8c9f63d00500c2b7cc18daf00949bdef; 2026-09-29
- [zano-cake-modes](../catalog/evidence/zano-cake-modes.json): official-source; 9679f91a8c9f63d00500c2b7cc18daf00949bdef; 2026-09-29
- [zano-codec](../catalog/evidence/zano-codec.json): official-source; e55c8ec47b76ed809162a958cf4600e03256a96a; 2026-09-29
- [zano-history-vector](../catalog/evidence/zano-history-vector.json): public-test-vector; e55c8ec47b76ed809162a958cf4600e03256a96a; 2026-09-29
- [zano-license](../catalog/evidence/zano-license.json): official-source; e55c8ec47b76ed809162a958cf4600e03256a96a; 2026-09-29
- [zano-modes](../catalog/evidence/zano-modes.json): official-source; e55c8ec47b76ed809162a958cf4600e03256a96a; 2026-09-29
- [zano-timestamp-password](../catalog/evidence/zano-timestamp-password.json): official-source; e55c8ec47b76ed809162a958cf4600e03256a96a; 2026-09-29
- [zcash-bip0039](../catalog/evidence/zcash-bip0039.json): official-source; 1a6cc63a53721781aabd695307cc41b82ca76813; 2026-09-29
- [zcash-bip0039-vector](../catalog/evidence/zcash-bip0039-vector.json): public-test-vector; 1a6cc63a53721781aabd695307cc41b82ca76813; 2026-09-29
- [zcash-create](../catalog/evidence/zcash-create.json): official-source; 558f686599586f55def3db86955d74d3be44605e; 2026-09-29
- [zcash-ffi](../catalog/evidence/zcash-ffi.json): official-source; 558f686599586f55def3db86955d74d3be44605e; 2026-09-29
- [zcash-standalone](../catalog/evidence/zcash-standalone.json): official-source; 558f686599586f55def3db86955d74d3be44605e; 2026-09-29
- [zcash-vector-license](../catalog/evidence/zcash-vector-license.json): official-source; 1a6cc63a53721781aabd695307cc41b82ca76813; 2026-09-29
- [zcash-zallet-create](../catalog/evidence/zcash-zallet-create.json): official-source; f9dcd4d31439feb813c95ac2516814421f5b04df; 2026-09-29
- [zcash-zallet-empty](../catalog/evidence/zcash-zallet-empty.json): official-source; f9dcd4d31439feb813c95ac2516814421f5b04df; 2026-09-29
- [zcash-zallet-export](../catalog/evidence/zcash-zallet-export.json): official-source; f9dcd4d31439feb813c95ac2516814421f5b04df; 2026-09-29

## Mandatory research coverage

Pending is an unfinished research state, not a support status. Missing records remain visible. Source links contain full provenance URLs.

### [windows-v1](../catalog/required/windows-v1.json)

| Requirement | Research state | Status | Records |
| --- | --- | --- | --- |
| dictionary-bip39-cs — BIP39 cs | terminal | verified | [bip39-cs](../catalog/dictionaries/bip39-cs.json) |
| dictionary-bip39-en — BIP39 en | terminal | verified | [bip39-en](../catalog/dictionaries/bip39-en.json) |
| dictionary-bip39-es — BIP39 es | terminal | verified | [bip39-es](../catalog/dictionaries/bip39-es.json) |
| dictionary-bip39-fr — BIP39 fr | terminal | verified | [bip39-fr](../catalog/dictionaries/bip39-fr.json) |
| dictionary-bip39-it — BIP39 it | terminal | verified | [bip39-it](../catalog/dictionaries/bip39-it.json) |
| dictionary-bip39-ja — BIP39 ja | terminal | verified | [bip39-ja](../catalog/dictionaries/bip39-ja.json) |
| dictionary-bip39-ko — BIP39 ko | terminal | verified | [bip39-ko](../catalog/dictionaries/bip39-ko.json) |
| dictionary-bip39-pt — BIP39 pt | terminal | verified | [bip39-pt](../catalog/dictionaries/bip39-pt.json) |
| dictionary-bip39-zh-hans — BIP39 zh-hans | terminal | verified | [bip39-zh-hans](../catalog/dictionaries/bip39-zh-hans.json) |
| dictionary-bip39-zh-hant — BIP39 zh-hant | terminal | verified | [bip39-zh-hant](../catalog/dictionaries/bip39-zh-hant.json) |
| dictionary-electrum-v1-en — electrum v1 en | terminal | blocked | [electrum-v1-en](../catalog/dictionaries/electrum-v1-en.json) |
| dictionary-monero-de — MONERO de | terminal | verified | [monero-de](../catalog/dictionaries/monero-de.json) |
| dictionary-monero-en — MONERO en | terminal | verified | [monero-en](../catalog/dictionaries/monero-en.json) |
| dictionary-monero-en-old — MONERO en-old | terminal | documented | [monero-en-old](../catalog/dictionaries/monero-en-old.json) |
| dictionary-monero-eo — MONERO eo | terminal | documented | [monero-eo](../catalog/dictionaries/monero-eo.json) |
| dictionary-monero-es — MONERO es | terminal | documented | [monero-es](../catalog/dictionaries/monero-es.json) |
| dictionary-monero-fr — MONERO fr | terminal | documented | [monero-fr](../catalog/dictionaries/monero-fr.json) |
| dictionary-monero-it — MONERO it | terminal | documented | [monero-it](../catalog/dictionaries/monero-it.json) |
| dictionary-monero-ja — MONERO ja | terminal | documented | [monero-ja](../catalog/dictionaries/monero-ja.json) |
| dictionary-monero-jbo — MONERO jbo | terminal | documented | [monero-jbo](../catalog/dictionaries/monero-jbo.json) |
| dictionary-monero-nl — MONERO nl | terminal | documented | [monero-nl](../catalog/dictionaries/monero-nl.json) |
| dictionary-monero-pt — MONERO pt | terminal | verified | [monero-pt](../catalog/dictionaries/monero-pt.json) |
| dictionary-monero-ru — MONERO ru | terminal | documented | [monero-ru](../catalog/dictionaries/monero-ru.json) |
| dictionary-monero-zh-hans — MONERO zh-hans | terminal | documented | [monero-zh-hans](../catalog/dictionaries/monero-zh-hans.json) |
| dictionary-pgp-even — pgp even | terminal | verified | [pgp-even](../catalog/dictionaries/pgp-even.json) |
| dictionary-pgp-odd — pgp odd | terminal | verified | [pgp-odd](../catalog/dictionaries/pgp-odd.json) |
| dictionary-polyseed-cs — POLYSEED cs | terminal | documented | [polyseed-cs](../catalog/dictionaries/polyseed-cs.json) |
| dictionary-polyseed-en — POLYSEED en | terminal | verified | [polyseed-en](../catalog/dictionaries/polyseed-en.json) |
| dictionary-polyseed-es — POLYSEED es | terminal | verified | [polyseed-es](../catalog/dictionaries/polyseed-es.json) |
| dictionary-polyseed-fr — POLYSEED fr | terminal | documented | [polyseed-fr](../catalog/dictionaries/polyseed-fr.json) |
| dictionary-polyseed-it — POLYSEED it | terminal | documented | [polyseed-it](../catalog/dictionaries/polyseed-it.json) |
| dictionary-polyseed-ja — POLYSEED ja | terminal | documented | [polyseed-ja](../catalog/dictionaries/polyseed-ja.json) |
| dictionary-polyseed-ko — POLYSEED ko | terminal | documented | [polyseed-ko](../catalog/dictionaries/polyseed-ko.json) |
| dictionary-polyseed-pt — POLYSEED pt | terminal | documented | [polyseed-pt](../catalog/dictionaries/polyseed-pt.json) |
| dictionary-polyseed-zh-hans — POLYSEED zh-hans | terminal | documented | [polyseed-zh-hans](../catalog/dictionaries/polyseed-zh-hans.json) |
| dictionary-polyseed-zh-hant — POLYSEED zh-hant | terminal | documented | [polyseed-zh-hant](../catalog/dictionaries/polyseed-zh-hant.json) |
| dictionary-sia-legacy — sia legacy | terminal | verified | [sia-legacy](../catalog/dictionaries/sia-legacy.json) |
| dictionary-slip39-en — slip39 en | terminal | verified | [slip39-en](../catalog/dictionaries/slip39-en.json) |
| dictionary-zano-en — zano en | terminal | blocked | [zano-en](../catalog/dictionaries/zano-en.json) |
| network-algorand — algorand | pending | — | — |
| network-arbitrum — arbitrum | pending | — | — |
| network-avalanche — avalanche | pending | — | — |
| network-base — base | pending | — | — |
| network-bitcoin — bitcoin | pending | — | — |
| network-bnb-chain — bnb chain | pending | — | — |
| network-cardano — cardano | pending | — | — |
| network-chia — chia | terminal | documented | [chia-wallet](../catalog/wallets/chia-wallet.json) |
| network-cosmos — cosmos | pending | — | — |
| network-decred — decred | terminal | documented | [decrediton](../catalog/wallets/decrediton.json) |
| network-ethereum — ethereum | pending | — | — |
| network-kusama — kusama | terminal | documented | [polkadot-js](../catalog/wallets/polkadot-js.json), [subwallet](../catalog/wallets/subwallet.json), [talisman](../catalog/wallets/talisman.json) |
| network-monero — monero | pending | — | — |
| network-polkadot — polkadot | terminal | documented | [polkadot-js](../catalog/wallets/polkadot-js.json), [subwallet](../catalog/wallets/subwallet.json), [talisman](../catalog/wallets/talisman.json) |
| network-polygon — polygon | pending | — | — |
| network-sia — sia | terminal | documented | [sia-walletd](../catalog/wallets/sia-walletd.json) |
| network-solana — solana | pending | — | — |
| network-tezos — tezos | pending | — | — |
| network-ton — ton | pending | — | — |
| network-tron — tron | pending | — | — |
| network-zano — zano | terminal | documented | [zano-wallet](../catalog/wallets/zano-wallet.json) |
| network-zcash — zcash | terminal | documented | [zallet](../catalog/wallets/zallet.json) |
| scheme-algorand-25 — algorand 25 | terminal | documented | [algorand-25](../catalog/schemes/algorand-25.json) |
| scheme-bip39 — bip39 | terminal | verified | [bip39](../catalog/schemes/bip39.json) |
| scheme-cake-decred-15 — cake decred 15 | terminal | documented | [cake-decred-15](../catalog/schemes/cake-decred-15.json) |
| scheme-cardano-byron — cardano byron | terminal | documented | [cardano-byron](../catalog/schemes/cardano-byron.json) |
| scheme-cardano-daedalus-27 — cardano daedalus 27 | terminal | documented | [cardano-daedalus-27](../catalog/schemes/cardano-daedalus-27.json) |
| scheme-cardano-hardware — cardano hardware | terminal | blocked | [cardano-hardware](../catalog/schemes/cardano-hardware.json) |
| scheme-cardano-icarus — cardano icarus | terminal | documented | [cardano-icarus](../catalog/schemes/cardano-icarus.json) |
| scheme-chia-bip39 — chia bip39 | terminal | documented | [chia-bip39](../catalog/schemes/chia-bip39.json) |
| scheme-decred-bip39 — decred bip39 | terminal | documented | [decred-bip39](../catalog/schemes/decred-bip39.json) |
| scheme-decred-pgp33 — decred pgp33 | terminal | documented | [decred-pgp33](../catalog/schemes/decred-pgp33.json) |
| scheme-electrum-v1 — electrum v1 | terminal | blocked | [electrum-v1](../catalog/schemes/electrum-v1.json) |
| scheme-electrum-v2 — electrum v2 | terminal | documented | [electrum-v2](../catalog/schemes/electrum-v2.json) |
| scheme-monero-legacy — monero legacy | terminal | documented | [monero-legacy](../catalog/schemes/monero-legacy.json) |
| scheme-mymonero — mymonero | terminal | documented | [mymonero-13](../catalog/schemes/mymonero-13.json) |
| scheme-polyseed — polyseed | terminal | documented | [polyseed-16](../catalog/schemes/polyseed-16.json) |
| scheme-sia-bip39 — sia bip39 | terminal | documented | [sia-bip39](../catalog/schemes/sia-bip39.json) |
| scheme-sia-legacy-28 — sia legacy 28 | terminal | documented | [sia-legacy-28](../catalog/schemes/sia-legacy-28.json) |
| scheme-sia-legacy-29 — sia legacy 29 | terminal | documented | [sia-legacy-29](../catalog/schemes/sia-legacy-29.json) |
| scheme-slip39-share — slip39 share | terminal | documented | [slip39-share](../catalog/schemes/slip39-share.json) |
| scheme-substrate-bip39 — substrate bip39 | terminal | documented | [substrate-bip39](../catalog/schemes/substrate-bip39.json) |
| scheme-ton-multichain-bip39 — ton multichain bip39 | terminal | documented | [ton-multichain-bip39](../catalog/schemes/ton-multichain-bip39.json) |
| scheme-ton-native — ton native | terminal | verified | [ton-native](../catalog/schemes/ton-native.json) |
| scheme-zano-legacy-24 — zano legacy 24 | terminal | blocked | [zano-legacy-24](../catalog/schemes/zano-legacy-24.json) |
| scheme-zano-legacy-25 — zano legacy 25 | terminal | blocked | [zano-legacy-25](../catalog/schemes/zano-legacy-25.json) |
| scheme-zano-modern — zano modern | terminal | blocked | [zano-modern](../catalog/schemes/zano-modern.json) |
| scheme-zcash-bip39 — zcash bip39 | terminal | documented | [zcash-bip39](../catalog/schemes/zcash-bip39.json) |
| scheme-zcash-non-mnemonic — zcash non mnemonic | terminal | no-mnemonic-confirmed | [zcash-non-mnemonic](../catalog/schemes/zcash-non-mnemonic.json) |
| wallet-atomic-wallet — atomic wallet | pending | — | — |
| wallet-backpack — backpack | pending | — | — |
| wallet-bitbox02 — bitbox02 | pending | — | — |
| wallet-bitget-wallet — bitget wallet | pending | — | — |
| wallet-blockstream-jade — blockstream jade | pending | — | — |
| wallet-bluewallet — bluewallet | pending | — | — |
| wallet-cake-wallet — cake wallet | terminal | documented | [cake-wallet-monero](../catalog/wallets/cake-wallet-monero.json) |
| wallet-cake-wallet-decred — cake wallet decred | terminal | documented | [cake-wallet-decred](../catalog/wallets/cake-wallet-decred.json) |
| wallet-cake-wallet-zano — cake wallet zano | terminal | documented | [cake-wallet-zano](../catalog/wallets/cake-wallet-zano.json) |
| wallet-chia-wallet — chia wallet | terminal | documented | [chia-wallet](../catalog/wallets/chia-wallet.json) |
| wallet-coinbase-wallet — coinbase wallet | pending | — | — |
| wallet-coinomi — coinomi | pending | — | — |
| wallet-coldcard — coldcard | pending | — | — |
| wallet-cosmostation — cosmostation | pending | — | — |
| wallet-daedalus — daedalus | terminal | documented | [daedalus](../catalog/wallets/daedalus.json) |
| wallet-decrediton — decrediton | terminal | documented | [decrediton](../catalog/wallets/decrediton.json) |
| wallet-defly — defly | terminal | blocked | [defly](../catalog/wallets/defly.json) |
| wallet-electrum — electrum | terminal | documented | [electrum](../catalog/wallets/electrum.json) |
| wallet-ellipal — ellipal | pending | — | — |
| wallet-eternl — eternl | terminal | blocked | [eternl](../catalog/wallets/eternl.json) |
| wallet-exodus — exodus | pending | — | — |
| wallet-exodus-monero — exodus monero | terminal | documented | [exodus-monero-export](../catalog/wallets/exodus-monero-export.json) |
| wallet-feather — feather | terminal | documented | [feather](../catalog/wallets/feather.json) |
| wallet-glow — glow | pending | — | — |
| wallet-gram-wallet — gram wallet | terminal | documented | [gram-wallet](../catalog/wallets/gram-wallet.json) |
| wallet-guarda — guarda | pending | — | — |
| wallet-imtoken — imtoken | pending | — | — |
| wallet-keplr — keplr | pending | — | — |
| wallet-keystone — keystone | pending | — | — |
| wallet-kukai — kukai | pending | — | — |
| wallet-lace — lace | terminal | documented | [lace](../catalog/wallets/lace.json) |
| wallet-leap — leap | pending | — | — |
| wallet-ledger — ledger | pending | — | — |
| wallet-metamask — metamask | pending | — | — |
| wallet-monero-gui-cli — monero gui cli | terminal | documented | [monero-gui-cli](../catalog/wallets/monero-gui-cli.json) |
| wallet-mymonero — mymonero | terminal | documented | [mymonero](../catalog/wallets/mymonero.json) |
| wallet-mytonwallet — mytonwallet | terminal | documented | [mytonwallet](../catalog/wallets/mytonwallet.json) |
| wallet-nami — nami | terminal | documented | [nami](../catalog/wallets/nami.json) |
| wallet-okx-wallet — okx wallet | pending | — | — |
| wallet-onekey — onekey | pending | — | — |
| wallet-openmask — openmask | terminal | documented | [openmask](../catalog/wallets/openmask.json) |
| wallet-passport — passport | pending | — | — |
| wallet-pera-wallet — pera wallet | terminal | documented | [pera-wallet](../catalog/wallets/pera-wallet.json) |
| wallet-phantom — phantom | pending | — | — |
| wallet-polkadot-js — polkadot js | terminal | documented | [polkadot-js](../catalog/wallets/polkadot-js.json) |
| wallet-rabby — rabby | pending | — | — |
| wallet-rainbow — rainbow | pending | — | — |
| wallet-safepal — safepal | pending | — | — |
| wallet-seedsigner — seedsigner | pending | — | — |
| wallet-sia-ui — sia ui | terminal | documented | [sia-ui](../catalog/wallets/sia-ui.json) |
| wallet-siad — siad | terminal | documented | [siad](../catalog/wallets/siad.json) |
| wallet-solflare — solflare | pending | — | — |
| wallet-sparrow — sparrow | pending | — | — |
| wallet-subwallet — subwallet | terminal | documented | [subwallet](../catalog/wallets/subwallet.json) |
| wallet-talisman — talisman | terminal | documented | [talisman](../catalog/wallets/talisman.json) |
| wallet-tangem-seed — tangem seed | pending | — | — |
| wallet-temple — temple | pending | — | — |
| wallet-tokenpocket — tokenpocket | pending | — | — |
| wallet-ton-space — ton space | terminal | documented | [ton-space](../catalog/wallets/ton-space.json) |
| wallet-tonhub — tonhub | terminal | verified | [tonhub](../catalog/wallets/tonhub.json) |
| wallet-tonkeeper-classic — tonkeeper classic | terminal | verified | [tonkeeper-classic](../catalog/wallets/tonkeeper-classic.json) |
| wallet-tonkeeper-multichain — tonkeeper multichain | terminal | documented | [tonkeeper-multichain](../catalog/wallets/tonkeeper-multichain.json) |
| wallet-trezor — trezor | pending | — | — |
| wallet-trezor-model-t — trezor model t | terminal | documented | [trezor-model-t](../catalog/wallets/trezor-model-t.json) |
| wallet-trezor-safe-3 — trezor safe 3 | terminal | documented | [trezor-safe-3](../catalog/wallets/trezor-safe-3.json) |
| wallet-trezor-safe-5 — trezor safe 5 | terminal | documented | [trezor-safe-5](../catalog/wallets/trezor-safe-5.json) |
| wallet-trezor-safe-7 — trezor safe 7 | terminal | documented | [trezor-safe-7](../catalog/wallets/trezor-safe-7.json) |
| wallet-trust-wallet — trust wallet | pending | — | — |
| wallet-typhon — typhon | terminal | blocked | [typhon](../catalog/wallets/typhon.json) |
| wallet-walletd — walletd | terminal | documented | [sia-walletd](../catalog/wallets/sia-walletd.json) |
| wallet-yoroi — yoroi | terminal | documented | [yoroi](../catalog/wallets/yoroi.json) |
| wallet-zallet — zallet | terminal | documented | [zallet](../catalog/wallets/zallet.json) |
| wallet-zano-wallet — zano wallet | terminal | documented | [zano-wallet](../catalog/wallets/zano-wallet.json) |
| wallet-zcash-official — zcash official | terminal | documented | [zcash-official](../catalog/wallets/zcash-official.json) |
| wallet-zerion — zerion | pending | — | — |
