# Cake Wallet current matrix and final research coverage

Reviewed 2026-09-29 under [source policy](../source-policy.md) and
[licensing policy](../licensing.md). **Research terminal; Windows release
NO-GO.** No wallet was run, restored, synced or funded. No signing, native
library execution, provider submission, paid operation or device test occurred.

Task15's163/163 result proved closure of its existing manifest, not Cake
completeness. This inventory was independently reconstructed from the official
cryptocurrency documentation, generated wallet-type configuration, four
platform configurations, UI handlers, wallet services and locked dependencies.
Tests maintain a literal expected inventory; expectations are not generated
from the required manifest or catalogue.

## Source and platform boundary

Cake repository revision:
`9679f91a8c9f63d00500c2b7cc18daf00949bdef`.
All new current Cake profiles have this singleton source boundary. This does
not claim every release binary bearing the version contains those sources.

| Platform configuration | Version / build | Current networks |
| --- | --- | --- |
| Android | 6.4.5 /4425 | all16 below |
| iOS | 6.4.5 /445 | all16 below |
| macOS | 6.4.4 /153 |13: excludes Decred, Zano, Zcash |
| Linux | 6.4.4 /82 |13: excludes Decred, Zano, Zcash |

There is no current Windows configuration in the inspected Cake setup script.
The Tessaveil Windows research manifest records wallets whose original
platform may be mobile/desktop; this is not a Cake Windows-release claim.
Absent desktop networks have explicit availability-boundary records, not
fabricated mnemonic support. Shared Dart hardware dispatch does not establish
device/model/transport/OS reachability; every hardware record says so.

The README's shorter feature list is not the inventory authority. The official
current crypto index and enabled source configurations identify16 chains.
ERC20 and other chain tokens do not create new mnemonic formats. Wownero is
export-only legacy; Haven was removed; Banano is an optional source flag
disabled in all four reviewed configurations, not a current supported chain.

## Independently reviewed network and mode matrix

C = fresh creation; I = existing mnemonic import; G = existing wallet-group
phrase reuse, never fresh generation. Every matrix row is expanded into
separate platform/mode record IDs. Rows grouping lengths mean choices within
one source mode, not that all accepted import lengths can be freshly created.
Additional language identities split the actual Monero dictionaries.

| Current network | Mnemonic creation | Mnemonic import / reuse | Non-mnemonic or external recovery |
| --- | --- | --- | --- |
| Monero | Polyseed16, legacy25, BIP39-derived12 |16,25, BIP39 parser12/15/18/21/24; G | spend/view keys and address, view-only, external hardware |
| Bitcoin | BIP39-shaped12/24; Cake Electrum24 prefix100 | BIP39 parser five lengths; G; Electrum100 and eb predicate branches | xpub/view-only; hardware |
| Litecoin | BIP39-shaped12/24; Cake Electrum24 prefix100 | BIP39 parser five lengths; G; Electrum100/eb branches | xpub or MWEB scan/public material; hardware |
| Bitcoin Cash | BIP39-shaped12/24 | BIP39 parser five lengths; G | no additional current credential branch asserted |
| Dogecoin | BIP39-shaped12/24 | BIP39 parser five lengths; G | no additional branch asserted |
| Ethereum | BIP39-shaped12/24 | BIP39 parser five lengths; G | private key; hardware dispatch |
| Polygon | BIP39-shaped12/24 | BIP39 parser five lengths; G | private key; hardware dispatch |
| Base | BIP39-shaped12/24 | BIP39 parser five lengths; G | private key; hardware dispatch |
| Arbitrum | BIP39-shaped12/24 | BIP39 parser five lengths; G | private key; hardware dispatch |
| BNB Smart Chain | BIP39-shaped12/24 | BIP39 parser five lengths; G | private key; hardware dispatch |
| Solana | BIP39-shaped12/24 | BIP39 parser five lengths; G | private key |
| Tron | BIP39-shaped12/24 | BIP39 parser five lengths; G | private key |
| Nano | native24; HD12/24 | native24; HD parser five lengths; G |32-byte hex seed,64-byte hex HD material |
| Decred | current12/24 |12/24; native15; G | public/view-only material |
| Zano | current12/24 |12/24; native26; G | no additional branch asserted |
| Zcash | current12/24 | Dart parser five lengths, native acceptance unresolved; G | extended private spending key |

All16 have official per-cryptocurrency document evidence and pinned service
evidence. A permissive Dart parser is explicitly **not** proof of native/UI
acceptance or compatibility. The eb predicate is present in shared Bitcoin
and Litecoin code; the blocked profile does not assert useful Bitcoin MWEB
recovery, creation or cross-platform MWEB parity.

## Format, dictionary, normalization and external secrets

- General Cake BIP39: separate `cake-bip39-create`12/24 and
  `cake-bip39-import`12/15/18/21/24. Locked dependency
  `anicdh/bip39@3633daa2026b98c523ae9a091322be2903f7a8ab`
  has English-only2048 words, ASCII-space splitting and case-sensitive lookup.
  PBKDF2 uses mnemonic code units, UTF8 salt,2048 HMAC-SHA512 iterations but
  does not apply required NFKD. Optional Unicode passphrase compatibility is
  blocked; do not reuse the normative BIP39 scheme just because words match.
  Source random generation uses nextInt(255), excluding255; entropy security
  is outside this format audit and not certified.
- Cake Electrum: `generateElectrumMnemonic` with264-bit strength generates
  English24 prefix100, not generic Electrum12/13. Separate creation24,
  restore100, and restore-eb schemes. Source restore checks prefixes without
  constraining word count, so import supported_lengths remains empty and
  blocked, not an invented bound. NFKD/lowercase wrapper has a combining-range
  loop that adds nothing, a literal string whitespace split and UTF16-based
  CJK handling. Optional normalized extension and `electrum` salt are not
  interchangeable with BIP39. No custom Unicode implementation was copied.
- Nano native24 uses English BIP39 vocabulary to encode32 entropy bytes
  directly, not sentence PBKDF2. HD create12/24 and parser-import five lengths
  are separate schemes. Locked
  `perishllc/nanoutil@c01a9c552917008d8fbc6b540db657031625b04f`
  derives with fixed mnemonic salt and hardened44/165/index path. Cake service
  does not forward the credentials passphrase: external_secret is none, not
  an optional BIP39 extension.64-hex-character import may re-encode native24;
 128-hex-character material remains non-mnemonic with null seed getter.
- Monero:10 Polyseed languages (en,ja,ko,es,fr,it,cs,pt,zh-hans,zh-hant) and
 10 legacy languages (en,de,es,fr,it,nl,pt,ru,ja,zh-hans) are individually
  represented in20 schemes and160 creation/import/platform records. Selector
  mapping justifies dictionary identity at a documented boundary, **not**
  exact FFI dictionary byte parity, prefix/checksumless recognition, Unicode
  passphrase compatibility or independent recovery. Esperanto, Lojban and
  EnglishOld are not silently claimed current Cake creation options.
  Fresh BIP39 is12 only: an additional exact12 scheme/profile sits beside the
  retained earlier generic research anchor. Imports/groups can pass all five
  BIP39 lengths. Derivation uses hardened44,128,account then0,0 and little-endian
  scalar reduction before English legacy encoding. This is not generic BIP39
  or a native legacy phrase. Optional extension remains blocked by normalization.
- Decred: official docs identify native15 before6.4.2, with continued import.
  Task13's claim of conflicting/unversioned documentation was a reading error;
  the same body hash supports the explicit transition. Android libwallet pin
  `ecc4a5fb9594368777848de42d7e072d62406507` and dcrdex
  `37585833528544f80dddd92dcdff10a78ad01e1f` remain the native15 authority.
  Every15-word input dispatches native, not BIP39-15; birthday/checksum and
  no-passphrase semantics differ. Current12/24 uses NFC instead of NFKD.
  iOS native dependency parity remains unverified, hence source records are
  nonselectable. No18/21 native Decred import was inferred from Dart prechecks.
- Zano: official docs date native26 before6.4.3. Current12/24 BIP39-derived
  creation/import and native26 import are separate.
  Dart accepts other BIP39 lengths but UI/native support is not asserted.
  Native seed password differs from BIP39; native dictionary license remains
  unresolved. Task14's exact Dart list gap is now closed, its native/binary
  recovery and license blockers are not.
  Global historical24/25 schemes remain mandatory outside Cake. No inspected
  Cake release or bound native dependency proves Cake reachability for those
  historical formats, so inventing Cake24/25 identities would be misleading.
- Zcash: distinct Cake12/24 creation and five-length Dart import schemes,
  optional passphrase and birthday passed to zkool. Native derivation/Unicode
  parity remains blocked; no inheritance from Zallet24 with empty passphrase.
  Official docs warn about Zashi change addresses. Private import requires
  secret-extended-key-main1 material, not a new mnemonic.

The locked BIP39 English literal and Cake Electrum English literal were
independently projected, without executing upstream code, to UTF8 LF with
final LF:2048 words each, byte-equal to existing `bip39-en`,
SHA256 `2f5eed53a4727b4bf8880d8f3f199efc90e58503646d9ff8eff3a2ed3b24dbda`.
This reuses approved vocabulary bytes only. No new wordlist, upstream
implementation, native library or binary was bundled. Existing attribution
and license decisions remain unchanged; no implicit relicensing of dependencies.
No additional distinct redistributable dictionary was established.

## Non-mnemonic and historical boundaries

Private keys, xpubs, view keys, Nano hex and hardware signer backup are not
fresh mnemonic creation. Key-import/hardware credentials retain null scheme
IDs. App backup has a separate record for each platform: encrypted v3
containers with legacyv1/v2 restore and an external backup password. Cloud
storage of a container is not evidence of a seedless-login wallet.

Wownero's three former16/25/14 formats remain separate export-only historical
profiles on all four configurations. No active sync/create/restore is claimed.
The14-word branch is blocked. Research also found Task11's omitted Feather
Tevador14 import at `948773cf13c7486ee230eb67b6bac06b2f94c874`.
Its UI calls monero_seed wordlist::english and restore invokes coin name,
birthday and correction handling. Exact dependency/list/license and independent
recovery were not established. A blocked14-word scheme and Feather profile
make the gap explicit, without guessing an alternate wordlist or reusing
Polyseed. The supported-length vocabulary now permits14 only as metadata;
it adds no phrase validator or table-generation behavior.

## Audit of Tasks10–15

The audit reviewed six batch notes, record references and their tests. Existing
mandatory identities are all retained unchanged; no required item is removed
or status downgraded to pending.24 previously orphaned records now have their
own required identities, including already-blocked Cake schemes/wallets.
That closes a manifest omission which previously concealed those release
blockers. Exact24 IDs are in the task report.

- Task10 BIP39/TON: confirmed10 dictionary languages and separation of TON
  native from generic BIP39. No new format gap proven in this bounded audit.
- Task11 Monero/Polyseed: added omitted Feather14 and precise Cake language,
  fresh12 and import/group boundaries. Earlier generic Cake records remain
  anchors, not completeness evidence.
- Task12 SLIP39/Algorand/Cardano: previously unrequired alternate lengths,
  paper27, Pera universal, Byron and Yoroi/Daedalus modes now required.
  Hardware and wallet-identity blockers remain unchanged.
- Task13 Electrum/Substrate/Decred: corrected documentation error, included
  existing alternate/import records, identified Cake-specific24/normalization
  and native-versus-current dispatch rather than borrowing Electrum/BIP39.
- Task14 Zano/Sia/Zcash/Chia: included legacy/standalone and current Cake
  modes that lacked required identities; Zano license and native parity remain.
- Task15 named wallets/networks: its163-item mechanical boundary is preserved;
  it never establishes current Cake network completeness or release readiness.

This is a source-bound terminal inventory, not a claim that all unspecified
historical versions, token networks, hardware combinations or future wallet
features are exhaustively certified.

## Gates and release decision

The completeness suite proves every required item references evidenced
terminal records, every dictionary/scheme/wallet is covered, the independent
16-network/platform/mode inventory exists, language dictionaries are split,
and nonverified generated entries are explicitly nonselectable.
There is no product selector in this foundation; verified records are only
candidates for future table creation.

The strict terminal gate can pass with documented and blocked records.
The independent release gate must return nonzero for each required blocker.
Both generated catalogs contain the exact concise blocker-ID/source-record
section. Its list is generated from metadata, not manually maintained prose.
Device, clean-machine, filesystem, audit, signing and release gates remain
NO-GO independently of catalogue status.

Reproduction: syntax compile; `python -m unittest
tests.catalog.test_catalogue_complete -v`; `python tools/run_tests.py`;
`python -m tools.catalog.cli validate --root . --require-terminal`;
`python -m tools.catalog.cli validate --root . --require-release-ready`;
`python -m tools.catalog.cli generate --root .` and `--check`.
Pinned isolated Rust1.90 fmt/check/test use the existing host toolchain;
no installation or device run is required. Exact observations belong in the
ignored task report, not fabricated future success statements.

## Retrieval ledger

All entries below are exact response-body bytes after HTTP decoding, before
any token extraction. Source URLs pin full commits. Mutable official pages
are2026-09-29 snapshots whose evidence revision is the body SHA256, not a
claim that a document is immutable or a released binary is verified. This
ledger covers all new evidence source objects, including duplicated service
URLs used for network-specific claims. Raw review cache is untracked/ignored.
404 exploratory hardware/group-document links were not used as evidence.

| Evidence | Representation | Bytes | SHA256 |
| --- | --- | ---: | --- |
| [cake-audit-feather14](https://raw.githubusercontent.com/feather-wallet/feather/948773cf13c7486ee230eb67b6bac06b2f94c874/src/wizard/PageWalletRestoreSeed.cpp) | decoded HTTP body | 8289 | `c03228a2042ef744ab58d1a290602d735c04bdb6a7d2183d9240232acee8f4e9` |
| [cake-audit-feather14-code](https://raw.githubusercontent.com/feather-wallet/feather/948773cf13c7486ee230eb67b6bac06b2f94c874/src/utils/Seed.cpp) | decoded HTTP body | 5386 | `dc79e1b6aace91076f1f9da96411706661830f55fda93926776d83e22d3ab8e5` |
| [cake-wallet-arbitrum-doc](https://docs.cakewallet.com/cryptos/arbitrum/) | decoded HTTP body | 523986 | `430065062ca674183701bb2f563bcaf748601f454b41b4e4a089ae47a0dbcee2` |
| [cake-wallet-arbitrum-service](https://raw.githubusercontent.com/cake-tech/cake_wallet/9679f91a8c9f63d00500c2b7cc18daf00949bdef/cw_evm/lib/evm_chain_wallet_service.dart) | decoded HTTP body | 13862 | `fc805f732334aa2640869ce02667d5e5416bbc42f4e1c90226d66d0fa619b43d` |
| [cake-wallet-backup](https://raw.githubusercontent.com/cake-tech/cake_wallet/9679f91a8c9f63d00500c2b7cc18daf00949bdef/lib/core/backup_service_v3.dart) | decoded HTTP body | 19136 | `c8d1f3c2aeadff8a5a237a2c2a1602408e0149538c0daecd9e4fbcd1ddde6fd2` |
| [cake-wallet-base-doc](https://docs.cakewallet.com/cryptos/base/) | decoded HTTP body | 520495 | `70d1c1826cc2f47097f14b644cfbc3bd3ebb0ed567ea4e85a0b9eca7bf13fb5f` |
| [cake-wallet-base-service](https://raw.githubusercontent.com/cake-tech/cake_wallet/9679f91a8c9f63d00500c2b7cc18daf00949bdef/cw_evm/lib/evm_chain_wallet_service.dart) | decoded HTTP body | 13862 | `fc805f732334aa2640869ce02667d5e5416bbc42f4e1c90226d66d0fa619b43d` |
| [cake-wallet-bip39-code](https://raw.githubusercontent.com/anicdh/bip39/3633daa2026b98c523ae9a091322be2903f7a8ab/lib/src/bip39_base.dart) | decoded HTTP body | 4400 | `8262db1988a062f8537c062c37be9707dd89a5baf9f302d2ad3ee780fb707a5c` |
| [cake-wallet-bip39-list](https://raw.githubusercontent.com/anicdh/bip39/3633daa2026b98c523ae9a091322be2903f7a8ab/lib/src/wordlists/english.dart) | decoded HTTP body | 23377 | `d4e53cb6a61f78e2359b320e858c679b48f0daa5eb2c0f23ad22931bffc30a84` |
| [cake-wallet-bip39-pbkdf](https://raw.githubusercontent.com/anicdh/bip39/3633daa2026b98c523ae9a091322be2903f7a8ab/lib/src/utils/pbkdf2.dart) | decoded HTTP body | 988 | `9bfd90bfc505190d18cc1d76315f53afcea942f8f5e649d73da109cbe0911afe` |
| [cake-wallet-bitcoin-cash-doc](https://docs.cakewallet.com/cryptos/bitcoin-cash/) | decoded HTTP body | 501264 | `e591958fa01b5b1cea1444c9c1fb942260a51bdfaa004a6713e81bf80bad244a` |
| [cake-wallet-bitcoin-cash-service](https://raw.githubusercontent.com/cake-tech/cake_wallet/9679f91a8c9f63d00500c2b7cc18daf00949bdef/cw_bitcoin_cash/lib/src/bitcoin_cash_wallet_service.dart) | decoded HTTP body | 4423 | `13e06147e1823d0a3c96984a8ff538f28970cc50127c2f6369ef363cf96c1d7b` |
| [cake-wallet-bitcoin-doc](https://docs.cakewallet.com/cryptos/bitcoin/) | decoded HTTP body | 588479 | `08ce2c5fe727627a4bf504f07d607fc4ce0b5cd25933c30921dddcbd80f1258c` |
| [cake-wallet-bitcoin-service](https://raw.githubusercontent.com/cake-tech/cake_wallet/9679f91a8c9f63d00500c2b7cc18daf00949bdef/cw_bitcoin/lib/bitcoin_wallet_service.dart) | decoded HTTP body | 7617 | `1be9e79161193c03c6cf1fdedbe9c6f7c97e1957f9d7ce7e447f0c2cfab7bd16` |
| [cake-wallet-bnb-chain-doc](https://docs.cakewallet.com/cryptos/bnb-smart-chain/) | decoded HTTP body | 514188 | `f067fd5e96722ee38996d5fbaa809028aa2883dc0fb3a0abd25bd825b007899f` |
| [cake-wallet-bnb-chain-service](https://raw.githubusercontent.com/cake-tech/cake_wallet/9679f91a8c9f63d00500c2b7cc18daf00949bdef/cw_evm/lib/evm_chain_wallet_service.dart) | decoded HTTP body | 13862 | `fc805f732334aa2640869ce02667d5e5416bbc42f4e1c90226d66d0fa619b43d` |
| [cake-wallet-build-android](https://raw.githubusercontent.com/cake-tech/cake_wallet/9679f91a8c9f63d00500c2b7cc18daf00949bdef/scripts/android/pubspec_gen.sh) | decoded HTTP body | 595 | `e88578a3d149878e211ab06ce9f8ed75bcb7ac048be0588a7221c3a189bcdc70` |
| [cake-wallet-build-ios](https://raw.githubusercontent.com/cake-tech/cake_wallet/9679f91a8c9f63d00500c2b7cc18daf00949bdef/scripts/ios/app_config.sh) | decoded HTTP body | 1684 | `c8ed24a8d296f0a4fcdf3cb514132b6a81269b42310caff9068368ed888b3807` |
| [cake-wallet-build-linux](https://raw.githubusercontent.com/cake-tech/cake_wallet/9679f91a8c9f63d00500c2b7cc18daf00949bdef/scripts/linux/app_config.sh) | decoded HTTP body | 749 | `48c1eec61d1cc0333b1676d1e94ea1ccd10a755360ae1074a8eb72c6197534dd` |
| [cake-wallet-build-macos](https://raw.githubusercontent.com/cake-tech/cake_wallet/9679f91a8c9f63d00500c2b7cc18daf00949bdef/scripts/macos/app_config.sh) | decoded HTTP body | 2202 | `1dda0c1ee6cd6a26b328772059780f959c6439537c497c7eff1677efba22c4a8` |
| [cake-wallet-create-ui](https://raw.githubusercontent.com/cake-tech/cake_wallet/9679f91a8c9f63d00500c2b7cc18daf00949bdef/lib/core/wallet_creation_service.dart) | decoded HTTP body | 5061 | `91f40f0444282c50d58650e41effc1baeeed47cc9c946158e9c9785e12444d05` |
| [cake-wallet-decred-doc](https://docs.cakewallet.com/cryptos/decred/) | decoded HTTP body | 516873 | `60b015b6925b3c3e8af1cde9b06e34f017f4eb5c53ad8ebc76d2f4fe37100854` |
| [cake-wallet-decred-service](https://raw.githubusercontent.com/cake-tech/cake_wallet/9679f91a8c9f63d00500c2b7cc18daf00949bdef/cw_decred/lib/wallet_service.dart) | decoded HTTP body | 11988 | `52ebe2b13257d5dfd3841d938958d29a46ba8d48ac1d89a00945ffc6610a3a9f` |
| [cake-wallet-doc-inventory](https://docs.cakewallet.com/cryptos/) | decoded HTTP body | 560794 | `54d4d514f42d6b4ade94209c2a4fa26e21ba9ae5c809ec6e93c1ef75cce6a14a` |
| [cake-wallet-dogecoin-doc](https://docs.cakewallet.com/cryptos/dogecoin/) | decoded HTTP body | 497348 | `69f36429a216f307ae1ebffb544740f36f94d76a646d966aa812c9f2789e95da` |
| [cake-wallet-dogecoin-service](https://raw.githubusercontent.com/cake-tech/cake_wallet/9679f91a8c9f63d00500c2b7cc18daf00949bdef/cw_dogecoin/lib/src/dogecoin_wallet_service.dart) | decoded HTTP body | 4521 | `8ebb21cdbc17cfdd5246f04b165e8a635eeb1b784396c4144b9769b8b180e8cc` |
| [cake-wallet-electrum-code](https://raw.githubusercontent.com/cake-tech/cake_wallet/9679f91a8c9f63d00500c2b7cc18daf00949bdef/cw_bitcoin/lib/bitcoin_mnemonic.dart) | decoded HTTP body | 27448 | `c634c1ea84ac9969396c08bbed9e4719d8f0330948455755c3f518fa2632b977` |
| [cake-wallet-electrum-normalization](https://raw.githubusercontent.com/cake-tech/cake_wallet/9679f91a8c9f63d00500c2b7cc18daf00949bdef/cw_core/lib/utils/text_normalizer.dart) | decoded HTTP body | 4528 | `6e26b7a6418732a3b7ca74102044c9946da7bcf2a6be7f6a8d79d450e73faac3` |
| [cake-wallet-ethereum-doc](https://docs.cakewallet.com/cryptos/ethereum/) | decoded HTTP body | 525702 | `43968a483e7ab758df913c1ea9bd33cb3340d72a63dd2afdd61ce92f09b0515f` |
| [cake-wallet-ethereum-service](https://raw.githubusercontent.com/cake-tech/cake_wallet/9679f91a8c9f63d00500c2b7cc18daf00949bdef/cw_evm/lib/evm_chain_wallet_service.dart) | decoded HTTP body | 13862 | `fc805f732334aa2640869ce02667d5e5416bbc42f4e1c90226d66d0fa619b43d` |
| [cake-wallet-export](https://raw.githubusercontent.com/cake-tech/cake_wallet/9679f91a8c9f63d00500c2b7cc18daf00949bdef/lib/view_model/wallet_seed_view_model.dart) | decoded HTTP body | 4284 | `e57829ad9284056ec12b705e5e2c289434a6d952966ad232adfaca0c8616986c` |
| [cake-wallet-groups](https://raw.githubusercontent.com/cake-tech/cake_wallet/9679f91a8c9f63d00500c2b7cc18daf00949bdef/lib/view_model/wallet_groups_display_view_model.dart) | decoded HTTP body | 5580 | `7b6f504b7b1d1cd2d2a66eedbf9212404106d258a0e91c9f8f3dc74028b4bcac` |
| [cake-wallet-inventory](https://raw.githubusercontent.com/cake-tech/cake_wallet/9679f91a8c9f63d00500c2b7cc18daf00949bdef/tool/configure.dart) | decoded HTTP body | 81762 | `437e4970ed7c622e00deea127c1ce09051ed1376a5f8e3f880a8846bd34b83d3` |
| [cake-wallet-language-ui](https://raw.githubusercontent.com/cake-tech/cake_wallet/9679f91a8c9f63d00500c2b7cc18daf00949bdef/lib/src/widgets/seed_language_picker.dart) | decoded HTTP body | 4330 | `cf55210b69928bb702927e9bb8ec09105610a0e8d52eef8b82cb961c3b9dc769` |
| [cake-wallet-litecoin-doc](https://docs.cakewallet.com/cryptos/litecoin/) | decoded HTTP body | 516411 | `9d3c314c090fc2cb3f8ff8af60c7537f3db72d3cf6c8c3e80601a0437196e816` |
| [cake-wallet-litecoin-service](https://raw.githubusercontent.com/cake-tech/cake_wallet/9679f91a8c9f63d00500c2b7cc18daf00949bdef/cw_bitcoin/lib/litecoin_wallet_service.dart) | decoded HTTP body | 7717 | `5f1b2cfbd9d1a77bf622fe79bf8d36c88961226e7c6183dd405773c6064ff4fd` |
| [cake-wallet-lock](https://raw.githubusercontent.com/cake-tech/cake_wallet/9679f91a8c9f63d00500c2b7cc18daf00949bdef/pubspec.lock) | decoded HTTP body | 116278 | `53c2ab5bb6bdab34973118cb85c7e0d0b19edab1ff620c008673c8b7c04bcee1` |
| [cake-wallet-monero-bip39-derive](https://raw.githubusercontent.com/cake-tech/cake_wallet/9679f91a8c9f63d00500c2b7cc18daf00949bdef/cw_monero/lib/bip39_seed.dart) | decoded HTTP body | 1727 | `18d553ebf4da1994bd39be740c417a8c708c5d54aff82d8c364fa4927cb8fd77` |
| [cake-wallet-monero-doc](https://docs.cakewallet.com/cryptos/monero/) | decoded HTTP body | 629769 | `095a5c8b307c2f0cf46618989f1c39ec67af096af53ac27a5d2e0d4858922441` |
| [cake-wallet-monero-service](https://raw.githubusercontent.com/cake-tech/cake_wallet/9679f91a8c9f63d00500c2b7cc18daf00949bdef/cw_monero/lib/monero_wallet_service.dart) | decoded HTTP body | 19686 | `9e0591a1fa987aa48ad876fecdb5ad41b77accd8cdd9fc2a382a90563148d727` |
| [cake-wallet-nano-dependency](https://raw.githubusercontent.com/perishllc/nanoutil/c01a9c552917008d8fbc6b540db657031625b04f/lib/src/derivations.dart) | decoded HTTP body | 4863 | `6509a87693a3221da32f71cd2bc518fad96f723b66071dabaabc66ec3e4533d2` |
| [cake-wallet-nano-derive](https://raw.githubusercontent.com/cake-tech/cake_wallet/9679f91a8c9f63d00500c2b7cc18daf00949bdef/cw_nano/lib/nano_wallet.dart) | decoded HTTP body | 18206 | `1f868e2c498764f0d176a82752679816318995ae059496977e2d5bfabd82bcdf` |
| [cake-wallet-nano-doc](https://docs.cakewallet.com/cryptos/nano/) | decoded HTTP body | 482427 | `af76a60aefcffaf5cdfcacb4894c40fe67eedeb0fb946ef76c1bd4e688afa661` |
| [cake-wallet-nano-service](https://raw.githubusercontent.com/cake-tech/cake_wallet/9679f91a8c9f63d00500c2b7cc18daf00949bdef/cw_nano/lib/nano_wallet_service.dart) | decoded HTTP body | 7131 | `4dc13dbfec0c1e4bc4ed4c1edcd4220dab96dec5acf2dd4e2023ab25b4dceee2` |
| [cake-wallet-polygon-doc](https://docs.cakewallet.com/cryptos/polygon/) | decoded HTTP body | 521500 | `5030d73f897420c1b88d3b41f59d71abd025fb358db2cbc96fd5c8dd352b089e` |
| [cake-wallet-polygon-service](https://raw.githubusercontent.com/cake-tech/cake_wallet/9679f91a8c9f63d00500c2b7cc18daf00949bdef/cw_evm/lib/evm_chain_wallet_service.dart) | decoded HTTP body | 13862 | `fc805f732334aa2640869ce02667d5e5416bbc42f4e1c90226d66d0fa619b43d` |
| [cake-wallet-restore-ui](https://raw.githubusercontent.com/cake-tech/cake_wallet/9679f91a8c9f63d00500c2b7cc18daf00949bdef/lib/view_model/wallet_restore_view_model.dart) | decoded HTTP body | 13669 | `ea4b88f117f0c0cabb0cad33c4c285af5780f7c41f1e82d8f219a5c2dabeb159` |
| [cake-wallet-solana-doc](https://docs.cakewallet.com/cryptos/solana/) | decoded HTTP body | 545495 | `5722dad56a9db13fb1825b61dfe351e30e0331a4a1467ee3e8950c5366e50849` |
| [cake-wallet-solana-service](https://raw.githubusercontent.com/cake-tech/cake_wallet/9679f91a8c9f63d00500c2b7cc18daf00949bdef/cw_solana/lib/solana_wallet_service.dart) | decoded HTTP body | 5226 | `10e0c1399af842bb88e304656ecf92250a14799aae8293cd443402fa51f7547e` |
| [cake-wallet-tron-doc](https://docs.cakewallet.com/cryptos/tron/) | decoded HTTP body | 519424 | `e28d3f77f3416b6f54b01981923cdb206dd791ac3e55154ac9803e0c31cfb6ff` |
| [cake-wallet-tron-service](https://raw.githubusercontent.com/cake-tech/cake_wallet/9679f91a8c9f63d00500c2b7cc18daf00949bdef/cw_tron/lib/tron_wallet_service.dart) | decoded HTTP body | 4876 | `0848b778961dc1fb0d28169ddc1cb216ff24deeac56c78cd74cb58ed4e3fe9bb` |
| [cake-wallet-version-android](https://raw.githubusercontent.com/cake-tech/cake_wallet/9679f91a8c9f63d00500c2b7cc18daf00949bdef/scripts/android/app_env.sh) | decoded HTTP body | 1768 | `89af9336686ad40b26497f684dbfc799e1812e986e89bfbee716a0140176da74` |
| [cake-wallet-version-ios](https://raw.githubusercontent.com/cake-tech/cake_wallet/9679f91a8c9f63d00500c2b7cc18daf00949bdef/scripts/ios/app_env.sh) | decoded HTTP body | 1210 | `1a232b9a4e485e4cffb7807510e41b189567d4d1f66dad539862c78ed6a29db1` |
| [cake-wallet-version-linux](https://raw.githubusercontent.com/cake-tech/cake_wallet/9679f91a8c9f63d00500c2b7cc18daf00949bdef/scripts/linux/app_env.sh) | decoded HTTP body | 649 | `90114a912b9587122c7ce8077531221bd232730b6527e41bcf1ea589daf74a0e` |
| [cake-wallet-version-macos](https://raw.githubusercontent.com/cake-tech/cake_wallet/9679f91a8c9f63d00500c2b7cc18daf00949bdef/scripts/macos/app_env.sh) | decoded HTTP body | 1132 | `2d69fd803fa39d0aae25eb8fdd7cbd422538df22b8d9a0d5ed6447a0c9dac3c9` |
| [cake-wallet-wownero-doc](https://docs.cakewallet.com/cryptos/wownero/) | decoded HTTP body | 469262 | `e8e0871bc282b83696979608b64aa582738d728d131041a57395d8aad9c3ac80` |
| [cake-wallet-zano-doc](https://docs.cakewallet.com/cryptos/zano/) | decoded HTTP body | 505070 | `de26ec2ffcdee7a8b90d6ae1b216cfef4e6484fe469ff88e44d00838a30289cb` |
| [cake-wallet-zano-service](https://raw.githubusercontent.com/cake-tech/cake_wallet/9679f91a8c9f63d00500c2b7cc18daf00949bdef/cw_zano/lib/zano_wallet_service.dart) | decoded HTTP body | 5693 | `cdf92c7e65a094da6a76a055d7536c61efcb6ee2f597a334934a73ff25977791` |
| [cake-wallet-zcash-derive](https://raw.githubusercontent.com/cake-tech/cake_wallet/9679f91a8c9f63d00500c2b7cc18daf00949bdef/cw_zcash/lib/src/zcash_wallet.dart) | decoded HTTP body | 57871 | `5b9d676af0c39394a64e4e0ced265539cc4cb2c979e09d6a0bf69977c2608e46` |
| [cake-wallet-zcash-doc](https://docs.cakewallet.com/cryptos/zcash/) | decoded HTTP body | 527763 | `66df590f8e69c5fe186c8cb4c8860467e4d3693b8efb5e3771a985d24ece7d29` |
| [cake-wallet-zcash-service](https://raw.githubusercontent.com/cake-tech/cake_wallet/9679f91a8c9f63d00500c2b7cc18daf00949bdef/cw_zcash/lib/src/zcash_wallet_service.dart) | decoded HTTP body | 5983 | `1c86a44066694c54f5d58aee7b06a8e89cca2fa721a860f9ee3cdac2b656219a` |
