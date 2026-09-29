# BIP39 and TON research batch

Verified UTC: **2026-09-29**. Research/source reviewer: Codex task-10 implementer.
Policies: [source policy](../source-policy.md), [licensing](../licensing.md).
This is catalogue evidence, not wallet recovery software or a release approval.

## Results and exact scope

Ten BIP39 dictionaries and the BIP39/TON-native schemes are verified. The
TON-multichain scheme remains documented: its BIP39 stage has public known
answers, but this batch has not reproduced an independent public full TON-path
known answer. This limitation is carried into its wallet profiles.

| Record | Status | Scope and decision |
| --- | --- | --- |
| `tonkeeper-classic` | verified | web; source-4942adcdcddf55d57e3d3fc3676f019caf87357e; ton-native-generated. Source snapshot only: extension manifest 3.0.0; web package is 0.0.0 and supplies no deployed release boundary. No claim for every installed Tonkeeper or Keeper version. CreateStandardWallet creates and displays native 24 words; TRON integration does not turn that phrase into a BIP39 root. Pro multi-account MAM is excluded. |
| `tonkeeper-multichain` | documented | cross-platform; documentation-snapshot-2026-09-29-version-unresolved; bip39-multichain-generated. Official rebranding documentation confirms a separate new multichain wallet and says old native 24 words cannot be converted. It does not pin app platform/version or generation word count. Pinned web source proves BIP39 import derivation, not that its new-wallet screen generates this mode. Exact first/last mobile versions and full-path known answer remain unproven; 12/24 are scheme lengths, not asserted generation lengths. Keeper (formerly Tonkeeper) is not the unrelated Waves Keeper product; Pro MAM is excluded. |
| `gram-wallet` | documented | android; documentation-snapshot-2026-09-29-version-unresolved; mnemonic-backup-unresolved. Identity fixed to My Wallet Apps Ltd., Android package io.gramwallet.app linked by gramwallet.io. Publisher says it uses My Wallet's engine; this does not prove a shared mnemonic algorithm or backup flow. No exact app version, exportable phrase length, generation method or source-to-package binding established. generates_mnemonic=false means generation is not confirmed, not that the product has no mnemonic. Do not inherit the behavior of Telegram's historical Gram test wallet or other similarly named products. |
| `mytonwallet` | documented | web; 26.9.8-source-f042bcc06b84f0cec928a29795f1cb8bf60a3e9c; bip39-multichain-generated. Exact source snapshot supports default 128-bit BIP39 generation (12 words), native-mode override and backup display. Import of 24-word BIP39 does not imply new 24-word generation. Full TON-path public known answer not reproduced; no blanket mapping to installed web/mobile releases or historical version intervals. |
| `mytonwallet-native` | verified | web; 26.9.8-source-f042bcc06b84f0cec928a29795f1cb8bf60a3e9c; ton-native-generated. Exact source snapshot only. forceAddingTonOnlyAccount chooses native generation; native generator returns 24 words and rejects BIP39-ambiguous candidates. This mode coexists with BIP39 in the same source version. No assertion that all builds or older/newer installed versions expose the same mode. |
| `ton-space` | documented | web; documentation-snapshot-2026-09-29-version-unresolved; manual-mnemonic-backup. Legacy TON Space help URL redirects to current DeFi Account documentation. Manual backup exposes 24 words; current official security page calls it BIP-39 but supplies no derivation path, source revision or product version transition. Native TON versus multichain semantics cannot be resolved from that wording. No scheme is selected; do not substitute historical TON-native assumptions. Email backup and custodial Crypto Wallet are separate modes and cannot be represented by this manual-mnemonic profile. Contract W5/v4R2 is not an app version or mnemonic scheme boundary. |
| `tonhub` | verified | android; 2.5.45-source-a2503f79d14868d65349ad7035d18389c6e2f996; ton-native-generated. Exact React Native Android source snapshot only; creation invokes native mnemonicNew and displays its 24-word result before backup confirmation. Derivation uses mnemonicToWalletKey. Hardware/Ledger, imported accounts, iOS binaries and other app versions are not covered by this profile. Wallet contract version changes do not establish mnemonic changes. |
| `openmask` | documented | web; 0.22.0-source-9150d57d530296f8b27ae59e4dfce865be81550e; ton-native-generated. OpenProduct's Chrome extension source creates and displays a tonweb-mnemonic phrase. Package declares tonweb-mnemonic ^1.0.1; reviewed library 1.0.1 defaults to native 24. Exact deployed extension/dependency artifact binding and a wallet-level reproducible recovery vector remain unproven; this source-backed mapping is documented, not selectable. Ledger and imported modes excluded. |

A source singleton means min=max at the stated full commit, not all binaries
bearing that package version. An unresolved documentation snapshot is explicitly
marked version-unresolved and non-selectable; it is not a fabricated app version.
No first/last historical release boundary is inferred. Native and BIP39 modes can
coexist: My Wallet 26.9.8 source has two records at the same revision/platform,
distinguished by mode. Tonkeeper Classic and Multichain share product identity,
but web-source and vendor-documentation scopes differ. Name aliases never merge
these identities. Tonkeeper Pro MAM, hardware/import/private-key modes, and
custodial/email-backup modes are excluded from generated mnemonic profiles.

No record uses no-mnemonic-confirmed: lacking sufficient evidence is not proof
that a mnemonic does not exist. Gram's generates_mnemonic=false means unconfirmed
generation under the closed boolean schema; limitations state that explicitly.

TON Space is deliberately unmapped. Its legacy help link redirects to DeFi
Account, whose current security page calls its 24 words BIP-39 without the path
or app version needed to resolve native versus multichain semantics. Contract
versions W5 and v4R2 do not resolve this ambiguity. This contrary wording remains
visible instead of being overwritten by historical TON assumptions.

## Scheme and normalization decisions

- BIP39 supports 12/15/18/21/24 words from 128/160/192/224/256 entropy bits.
  Each word is selected by an 11-bit index after the prescribed SHA-256 checksum.
  Words, sentence and optional passphrase use UTF-8 NFKD; the mnemonic seed
  stage is PBKDF2-HMAC-SHA512, 2048 iterations, salt mnemonic plus passphrase.
- Japanese display separates words with U+3000; NFKD turns it into an ASCII
  space. Tests cover this and composed/decomposed forms in every public vector.
  No byte normalization, sorting, case folding, accent removal or translation
  was performed on stored word lists. Spanish/French input conveniences in
  upstream guidance are not permission to modify stored words.
- TON native uses 24 English words and a different seed/check predicate:
  HMAC-SHA512 keyed by joined words with password as message, PBKDF2-HMAC-SHA512
  with TON default seed and 100000 rounds, and a 32-byte Ed25519 seed prefix.
  TON seed version uses 390 rounds for the basic-seed predicate. Library
  lowercase/trim behavior is documented separately from BIP39 NFKD.
- TEP-3 defines multichain 12/24-word import/profile support through BIP39 and
  SLIP-0010 Ed25519, path m/44'/607'/0', indexed for subwallets. It recommends
  new 12-word multichain or native 24-word generation and discourages new
  24-word multichain generation. Scheme lengths are not wallet generation claims.
- Optional mnemonic passwords are external secrets. An application PIN is not
  one. Tessaveil stores neither and never derives user keys or validates a
  complete user phrase. Derivation below is exclusively public research tests.

## Exact BIP39 source bytes

Authoritative repository: bitcoin/bips at `3a10b5b5f0a7586df8928d580a3009744ebb2079`.
Paths are bip-0039/<filename>.txt. Downloaded response bytes were copied unchanged;
UTF-8, LF and one final LF are preserved. Each list has 2048 lines and 2048 unique
NFKD words; all are already NFKD. The fixture stores independent expected hashes
and byte lengths, so changing both a list and its catalogue hash still fails.

| ID | Upstream filename | Bytes | SHA-256 |
| --- | --- | ---: | --- |
| bip39-en | english.txt | 13116 | `2f5eed53a4727b4bf8880d8f3f199efc90e58503646d9ff8eff3a2ed3b24dbda` |
| bip39-ja | japanese.txt | 26423 | `2eed0aef492291e061633d7ad8117f1a2b03eb80a29d0e4e3117ac2528d05ffd` |
| bip39-ko | korean.txt | 37832 | `9e95f86c167de88f450f0aaf89e87f6624a57f973c67b516e338e8e8b8897f60` |
| bip39-es | spanish.txt | 13996 | `46846a5a0139d1e3cb77293e521c2865f7bcdb82c44e8d0a06a2cd0ecba48c0b` |
| bip39-zh-hans | chinese_simplified.txt | 8192 | `5c5942792bd8340cb8b27cd592f1015edf56a8c5b26276ee18a482428e7c5726` |
| bip39-zh-hant | chinese_traditional.txt | 8192 | `417b26b3d8500a4ae3d59717d7011952db6fc2fb84b807f3f94ac734e89c1b5f` |
| bip39-fr | french.txt | 16777 | `ebc3959ab7801a1df6bac4fa7d970652f1df76b683cd2f4003c941c63d517e59` |
| bip39-it | italian.txt | 16033 | `d392c49fdb700a24cd1fceb237c1f65dcc128f6b34a8aacb58b59384b5c648c2` |
| bip39-cs | czech.txt | 14945 | `7e80e161c3e93d9554c2efb78d4e3cebf8fc727e9c52e03b83b94406bdcc95fc` |
| bip39-pt | portuguese.txt | 15671 | `2685e9c194c82ae67e10ba59d9ea5345a23dc093e92276fc5361f6667d79cd3f` |

All ten byte streams also match the exact corresponding reference-implementation
files under src/mnemonic/wordlist at trezor/python-mnemonic
`b57a5ad77a981e743f4167ab2f7927a55c1e82a8`. Its additional Russian/Turkish lists
are not part of the ten-list BIP39 specification scope and were not bundled.
TON crypto wordlist.ts was independently token-extracted in memory: 2048 tokens
match the BIP39 English order exactly. Its code file was not copied into the repo.

## License and signing component review

The BIPs repository has no single blanket root license for all BIPs. BIP39 itself
declares MIT. The explicit additional redistribution basis is the actual root
MIT license at the pinned Trezor reference revision, linked by BIP39 itself:
all ten exact files match its licensed wordlist directory byte-for-byte, and
vectors.json belongs to the same tree. Review of that tree found LICENSE and no
wordlist-specific COPYING/NOTICE/license override. This is not an inference from
the repository being public or from an SPDX label alone.

Decision for these exact lists and the 240-vector projection:
repository_redistribution=allowed; signpath_compatible=compatible.
MIT's notice-retention condition is fulfilled by the complete upstream text,
copyright and contributor credits in [THIRD_PARTY_NOTICES](../../../THIRD_PARTY_NOTICES).
The five TON public-vector projections have the actual Whales Corp. MIT license
and copyright in the same notices file. No wallet implementation code, dependencies
or binary is bundled; in particular Tonhub's GPL/commercial text grants no
permission used here and its code is not redistributed.

This source-data component assessment uses the OSI MIT entry and SignPath's OSS
terms, not a fictitious SignPath license whitelist. No commercial dual-license
restriction accompanies the selected MIT data. Foundation acceptance, project
eligibility, security review, binaries and future payload review remain separate.
All previous physical-device/filesystem/release gates remain NO-GO as before.

## Public vectors and independent reproduction

Fixture: tests/catalog/fixtures/public/bip39-ton.json. It is explicitly public,
non-funded test material. Never use these deterministic values for assets.

- BIP39: 240 cases, 24 per language from the pinned Trezor vectors.json. For
  each, retain upstream array index, public entropy, SHA-256 of the published
  NFKD sentence, and the published expected seed; passphrase is TREZOR. This
  projection avoids storing complete mnemonic strings. The test reconstructs
  indices from entropy/checksum and reads the real committed dictionary; its
  expected fingerprint/seed came from upstream, not from our implementation.
- TON native: five cases from pinned ton-crypto mnemonic.spec.ts. Convert the
  published English words to zero-based BIP39 indices and retain the first
  32 bytes of the published secretKey (the Ed25519 seed). Python stdlib HMAC and
  PBKDF2 reproduce those known answers and basic-seed checks. Ed25519 public keys,
  addresses and wallet binaries are not claimed to have been executed.
- The test uses Python 3.14.2 hashlib, hmac and unicodedata; no third-party
  cryptographic implementation is installed for it. The test is strictly offline.
  BIP39 expected outputs cover 12/18/24 words; the normative spec supplies
  15/21-word support. We do not mislabel synthetic outputs as upstream vectors.

Commands from repository root:

```text
python -m unittest tests.catalog.test_bip39_ton -v
python -m tools.catalog.cli validate --root . --allow-incomplete-required
python -m tools.catalog.cli generate --root .
python -m tools.catalog.cli generate --root . --check
python tools/run_tests.py
```

The batch test checks IDs, closed required entries, source pins/backlinks, license
choices, independent hashes/counts, public vectors, native/multichain separation,
exact singleton mode identities and unresolved modes. General interval-overlap
validation for future mixed historical intervals remains Task 15's scope.

## Source retrieval ledger

All sources below were fetched and inspected on 2026-09-29 UTC. HTTPS raw file
URLs contain full commit revisions. Mutable official documentation uses a dated
response-body SHA-256; dynamic HTML can change and is not claimed to be an
immutable archive. A fingerprint is not authenticity proof. URLs are primary
publishers only; search results and store user reviews did not supply claims.
The OSI HTTP body used PowerShell Invoke-WebRequest after urllib received 403;
other hashes use decoded HTTP body bytes from urllib. No source snapshot needing
separate redistribution permission was added to the repository.

| Evidence / source | Type / level | Exact source URL | SHA-256 |
| --- | --- | --- | --- |
| bip39-spec | official-specification / 1 | [source](https://raw.githubusercontent.com/bitcoin/bips/3a10b5b5f0a7586df8928d580a3009744ebb2079/bip-0039.mediawiki) | `afcbcbed36fe9eb734bd607398a8c124683ded2a75c3830e1b16c47b043a9134` |
| bip39-guidance | official-specification / 1 | [source](https://raw.githubusercontent.com/bitcoin/bips/3a10b5b5f0a7586df8928d580a3009744ebb2079/bip-0039/bip-0039-wordlists.md) | `363a51bc4748d95541bb156e0439de7b51f28b260433c09874e5891dd3b0f883` |
| bip39-license | official-source / 3 | [source](https://raw.githubusercontent.com/trezor/python-mnemonic/b57a5ad77a981e743f4167ab2f7927a55c1e82a8/LICENSE) | `d5e3c7c62a84e80073201e2f6e5130e9e6804fa05f8ac4f8b26a13c7d3969697` |
| bip39-vectors | public-test-vector / 4 | [source](https://raw.githubusercontent.com/trezor/python-mnemonic/b57a5ad77a981e743f4167ab2f7927a55c1e82a8/vectors.json) | `fa3b937b7cff9c9b8ecd3aa011faeb8d6dd67993174b72326e83f4de8fdb30f8` |
| ton-tep3 | official-specification / 1 | [source](https://raw.githubusercontent.com/ton-blockchain/TEPs/fe8a154e4dad9f5c0bf7240df278cb50ec6cd908/text/0003-wallets.md) | `4049020b927f72f7187b04f3e61e27f478caf1669fd528f21b815417b428be4b` |
| ton-native-source | official-source / 3 | [source](https://raw.githubusercontent.com/ton-org/ton-crypto/c3435833a0da52a96f674c352c4c6f91fcc07f6d/src/mnemonic/mnemonic.ts) | `79518c5f905daaa4e64f09454e8a82dbb1c8d1b310305ef84b25e85b2c77126a` |
| ton-native-vectors | public-test-vector / 4 | [source](https://raw.githubusercontent.com/ton-org/ton-crypto/c3435833a0da52a96f674c352c4c6f91fcc07f6d/src/mnemonic/mnemonic.spec.ts) | `ba6936664624168caf454df777b4ef8354c034c49b121a493c44237e4880cd83` |
| ton-native-license | official-source / 3 | [source](https://raw.githubusercontent.com/ton-org/ton-crypto/c3435833a0da52a96f674c352c4c6f91fcc07f6d/LICENSE) | `33578b9ea1522de18164cf1d1ef8e52f50d748ae17c7d38b4fa5e6f50207f8eb` |
| tonkeeper-create | official-source / 3 | [source](https://raw.githubusercontent.com/tonkeeper/tonkeeper-web/4942adcdcddf55d57e3d3fc3676f019caf87357e/packages/uikit/src/pages/import/CreateStandardWallet.tsx) | `a60930c7ec15e52b5cd5735738199b2cce50c3da510a424fe29b4eb7e642e74e` |
| tonkeeper-derive | official-source / 3 | [source](https://raw.githubusercontent.com/tonkeeper/tonkeeper-web/4942adcdcddf55d57e3d3fc3676f019caf87357e/packages/core/src/service/mnemonicService.ts) | `9852941011f82ec14e865c0cf33d78fa3944eeed5c61deeade94b65412d87643` |
| tonkeeper-version | official-source / 3 | [source](https://raw.githubusercontent.com/tonkeeper/tonkeeper-web/4942adcdcddf55d57e3d3fc3676f019caf87357e/apps/extension/public/manifest.json) | `7d8f4c2373bd7dcf5a3d5cd3e11407848baa178efef1ddda12b60b9c2c82b600` |
| ton-my-common | official-source / 3 | [source](https://raw.githubusercontent.com/mytonwallet-org/mytonwallet/f042bcc06b84f0cec928a29795f1cb8bf60a3e9c/src/api/common/mnemonic.ts) | `e435194f56181b0b9c1ac44934c1adf96b1518d53cbe76ac6a27ba455af432c6` |
| ton-my-auth | official-source / 3 | [source](https://raw.githubusercontent.com/mytonwallet-org/mytonwallet/f042bcc06b84f0cec928a29795f1cb8bf60a3e9c/src/api/methods/auth.ts) | `c6401d8455eb936f01cf951ba523eba8a19d69b386e3b116af256dc2a5b578a1` |
| ton-my-create | official-source / 3 | [source](https://raw.githubusercontent.com/mytonwallet-org/mytonwallet/f042bcc06b84f0cec928a29795f1cb8bf60a3e9c/src/global/actions/api/auth.ts) | `3bc4849d9a8573e9e06182f4aefbc17e2aa358ff37e24c49d24cb5a24a210786` |
| ton-my-derive | official-source / 3 | [source](https://raw.githubusercontent.com/mytonwallet-org/mytonwallet/f042bcc06b84f0cec928a29795f1cb8bf60a3e9c/src/api/chains/ton/auth.ts) | `35286bbfb6c1d6022569738a054dd32d060b1fc48c6a1143dab1df705a218211` |
| ton-my-backup | official-source / 3 | [source](https://raw.githubusercontent.com/mytonwallet-org/mytonwallet/f042bcc06b84f0cec928a29795f1cb8bf60a3e9c/src/components/settings/backup/BackupSecretWords.tsx) | `724207d342eefabc654f030fc5df8720a96c8267c04ca5da822baa0fbd7325b1` |
| ton-my-path | official-source / 3 | [source](https://raw.githubusercontent.com/mytonwallet-org/mytonwallet/f042bcc06b84f0cec928a29795f1cb8bf60a3e9c/src/api/chains/ton/derivationConstants.ts) | `5d799c9d1ec5fc23bf85245a477772a744cbf19a0ef7bef0aa8ecf9c1bd1c670` |
| ton-my-version | official-source / 3 | [source](https://raw.githubusercontent.com/mytonwallet-org/mytonwallet/f042bcc06b84f0cec928a29795f1cb8bf60a3e9c/package.json) | `93b9311800850e215a424d9eefdb512958e33cbe0ad3e7fe17d0bbf771698e32` |
| tonhub-create | official-source / 3 | [source](https://raw.githubusercontent.com/tonwhales/wallet/a2503f79d14868d65349ad7035d18389c6e2f996/app/fragments/onboarding/WalletCreateFragment.tsx) | `dafdd9c99b91982918502e45f077b9d5af518e6c531aa878fb666bc2ad9a1329` |
| tonhub-derive | official-source / 3 | [source](https://raw.githubusercontent.com/tonwhales/wallet/a2503f79d14868d65349ad7035d18389c6e2f996/app/utils/createWalletFromMnemonics.ts) | `b8341c61165ac9778a00e7eb7546b29a43ed0cc09ad520fdd3ce63011f8a5795` |
| tonhub-version | official-source / 3 | [source](https://raw.githubusercontent.com/tonwhales/wallet/a2503f79d14868d65349ad7035d18389c6e2f996/package.json) | `ef41072e6abb6d6f983d669e0f8e9a8f182fd73a98406b251ad68f31379c6386` |
| tonhub-identity | official-source / 3 | [source](https://raw.githubusercontent.com/tonwhales/wallet/a2503f79d14868d65349ad7035d18389c6e2f996/README.md) | `59da82be7e3db101c4a8f72ee2b4e618ba6db87f9edaa5b9f939dd87f0a4c74b` |
| ton-openmask-create | official-source / 3 | [source](https://raw.githubusercontent.com/OpenProduct/openmask-extension/9150d57d530296f8b27ae59e4dfce865be81550e/src/view/screen/import/CreateWallet.tsx) | `12d7e29578a4c58d76665375cc4ab498e010b5871baa290e0aaba24819a11362` |
| ton-openmask-version | official-source / 3 | [source](https://raw.githubusercontent.com/OpenProduct/openmask-extension/9150d57d530296f8b27ae59e4dfce865be81550e/package.json) | `5c4d9320793ae712801603af2bccd294dbd1beaf5bae2739de280dd3fca2fa6a` |
| ton-openmask-identity | official-source / 3 | [source](https://raw.githubusercontent.com/OpenProduct/openmask-extension/9150d57d530296f8b27ae59e4dfce865be81550e/README.md) | `007ec00e241abeb6d6aa354fe8251a3d6e5cc340af53847a140a885ac6e82249` |
| ton-tonweb-generate | official-source / 3 | [source](https://raw.githubusercontent.com/toncenter/tonweb-mnemonic/a338a00d4ca0ed833431e0e49e4cfad766ac713c/src/functions/generate-mnemonic.ts) | `f0f05bd83dd03b22463be3deb85787ba3c69e094c88ad889ceed17073dea7249` |
| ton-tonweb-seed | official-source / 3 | [source](https://raw.githubusercontent.com/toncenter/tonweb-mnemonic/a338a00d4ca0ed833431e0e49e4cfad766ac713c/src/functions/mnemonic-to-seed.ts) | `c2e34f6888d3b8b3192567bbe6dbdb1fc1e4a1db51228089a62c4c2e8e8f70b7` |
| ton-tonweb-version | official-source / 3 | [source](https://raw.githubusercontent.com/toncenter/tonweb-mnemonic/a338a00d4ca0ed833431e0e49e4cfad766ac713c/package.json) | `3a5777133b2ccfa280a3ab0bcd030d63a93ec07f97370f589845e26a1b158574` |
| ton-keeper-doc | official-documentation / 2 | [source](https://keeperwallet.helpscoutdocs.com/article/181-rebranding) | `d7091696af9e14b254c181906e1a8e8b48a339835ae65ac753593cabcbcb768a` |
| ton-gram-identity | official-documentation / 2 | [source](https://gramwallet.io/) | `c498efe1d81425f59fb294f1184c5a64ddd913c5cc22784759d2bd58691e7da2` |
| ton-gram-store | official-documentation / 2 | [source](https://play.google.com/store/apps/details?hl=en_US&id=io.gramwallet.app) | `3f2c0e813940801893d846b36313173f6e7a2865b1bc41d80cc74fd1c90a2518` |
| ton-space-doc | official-documentation / 2 | [source](https://help.wallet.tg/article/1032-welcome-to-defi-account) | `506a3bc3c0a4861601fc606c90320acac8d4a2bd91a639b27190567530006d37` |
| ton-space-security | official-documentation / 2 | [source](https://help.walt.io/article/86-security) | `7f5a40f0e43d00d2a620972b9f2a1a5370ed4ad660f6d65d5ca25bc36f71b8dd` |
| bip39-osi-mit | official-documentation / 2 | [source](https://opensource.org/license/mit) | `004c79db0a335488afc87600d89f447dce7fb4d24d510af15ed4381a24be848c` |
| bip39-signpath | official-documentation / 2 | [source](https://signpath.org/terms.html) | `6610cf889bbe0dc7533abaa310bc7a5cc9a61ae6c2ce0798a08109c925b46c51` |
| ton-native-wordlist | official-source / 3 | [source](https://raw.githubusercontent.com/ton-org/ton-crypto/c3435833a0da52a96f674c352c4c6f91fcc07f6d/src/mnemonic/wordlist.ts) | `2bc9a19c24279d659c4d02e08f9381af16cd62bdbb5103ce1815db4a7861c9db` |

## Remaining evidence gaps

Selectable support is withheld for the TON multichain scheme, Tonkeeper
Multichain, My Wallet BIP39 mode, Gram Wallet, TON Space and OpenMask as detailed
above. Native profiles are confined to their exact reviewed source versions;
no historical version interval or deployed-store equivalence has been invented.
Future promotion needs an independent full-path vector where absent, exact
product/platform/version bindings, and resolution of the TON Space terminology.
Only Task 10's 20 required entries are closed; other batches and network coverage
remain pending in the global manifest. Catalogue completion is not release GO.
