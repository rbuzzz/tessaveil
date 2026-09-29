# Каталог Tessaveil

> Создано автоматически из catalog/*. Не редактировать; команда: `python -m tools.catalog.cli generate --root .`.

Только исследование. Проверенная запись — лишь кандидат для создания таблиц в будущем. Общий словарь не означает совместимость схем. Ключи не выводятся, целые фразы не проверяются. Внешние секреты не сохраняются.

Готовность релиза: NO-GO; проверка каталога не закрывает требования физических устройств, чистых систем, файловых систем, аудита и релиза.

## Индекс продуктов

| Продукт / профиль | Платформа / режим | Сети | Схема | Статус |
| --- | --- | --- | --- | --- |
| Gram Wallet / [gram-wallet](#wallet-gram-wallet) | android / mnemonic-backup-unresolved | ton | — | documented |
| My Wallet / MyTonWallet / [mytonwallet](#wallet-mytonwallet) | web / bip39-multichain-generated | ton | [ton-multichain-bip39](#scheme-ton-multichain-bip39) | documented |
| My Wallet / MyTonWallet — TON only / [mytonwallet-native](#wallet-mytonwallet-native) | web / ton-native-generated | ton | [ton-native](#scheme-ton-native) | verified |
| OpenMask / [openmask](#wallet-openmask) | web / ton-native-generated | ton | [ton-native](#scheme-ton-native) | documented |
| Tonhub / [tonhub](#wallet-tonhub) | android / ton-native-generated | ton | [ton-native](#scheme-ton-native) | verified |
| Tonkeeper Classic / [tonkeeper-classic](#wallet-tonkeeper-classic) | web / ton-native-generated | ton | [ton-native](#scheme-ton-native) | verified |
| Keeper / Tonkeeper Multichain / [tonkeeper-multichain](#wallet-tonkeeper-multichain) | cross-platform / bip39-multichain-generated | ton | [ton-multichain-bip39](#scheme-ton-multichain-bip39) | documented |
| TON Space / DeFi Account / [ton-space](#wallet-ton-space) | web / manual-mnemonic-backup | ton | — | documented |

## Индекс сетей

- ton: [gram-wallet](#wallet-gram-wallet), [mytonwallet](#wallet-mytonwallet), [mytonwallet-native](#wallet-mytonwallet-native), [openmask](#wallet-openmask), [ton-space](#wallet-ton-space), [tonhub](#wallet-tonhub), [tonkeeper-classic](#wallet-tonkeeper-classic), [tonkeeper-multichain](#wallet-tonkeeper-multichain)

## Профили кошельков

<a id="wallet-gram-wallet"></a>

### Gram Wallet — gram-wallet

- Исходная запись: [gram-wallet](../catalog/wallets/gram-wallet.json)
- Статус: documented
- Причина: Доказательств недостаточно для доступной поддержки.
- Рекомендация: Недоступно для выбора; используйте процедуру резервного копирования самого кошелька.
- Диапазон версий (min / max): documentation-snapshot-2026-09-29-version-unresolved / documentation-snapshot-2026-09-29-version-unresolved
- Дата проверки: 2026-09-29
- Историческая запись: false
- Доказательства: [ton-gram-identity](../catalog/evidence/ton-gram-identity.json), [ton-gram-store](../catalog/evidence/ton-gram-store.json)
- Подтверждаемое утверждение: gramwallet.io identifies the current self-custodial TON wallet and links installation; current identity must not inherit historical Telegram Gram behavior. Reviewed 2026-09-29; byte SHA-256 c498efe1d81425f59fb294f1184c5a64ddd913c5cc22784759d2bd58691e7da2. See docs/research/batches/bip39-ton.md.
- Подтверждаемое утверждение: Publisher-provided listing identifies My Wallet Apps Ltd., Android package io.gramwallet.app, September 7 2026 update and shared My Wallet engine. It does not establish exact mnemonic generation/export or version boundary; user reviews are not evidence. Reviewed 2026-09-29; byte SHA-256 3f2c0e813940801893d846b36313173f6e7a2865b1bc41d80cc74fd1c90a2518. See docs/research/batches/bip39-ton.md.
- Другие названия: Gram
- Схема: —
- Создаёт мнемонику / только импорт: false / false
- Ограничения: Identity fixed to My Wallet Apps Ltd., Android package io.gramwallet.app linked by gramwallet.io. Publisher says it uses My Wallet's engine; this does not prove a shared mnemonic algorithm or backup flow.; No exact app version, exportable phrase length, generation method or source-to-package binding established. generates\_mnemonic=false means generation is not confirmed, not that the product has no mnemonic.; Do not inherit the behavior of Telegram's historical Gram test wallet or other similarly named products.
- Рекомендация профиля: Use the original trusted wallet's backup and recovery procedure. Match exact product, platform, source version and mode. Never enter a complete recovery phrase into Tessaveil or a website.

<a id="wallet-mytonwallet"></a>

### My Wallet / MyTonWallet — mytonwallet

- Исходная запись: [mytonwallet](../catalog/wallets/mytonwallet.json)
- Статус: documented
- Причина: Доказательств недостаточно для доступной поддержки.
- Рекомендация: Недоступно для выбора; используйте процедуру резервного копирования самого кошелька.
- Диапазон версий (min / max): 26.9.8-source-f042bcc06b84f0cec928a29795f1cb8bf60a3e9c / 26.9.8-source-f042bcc06b84f0cec928a29795f1cb8bf60a3e9c
- Дата проверки: 2026-09-29
- Историческая запись: false
- Доказательства: [ton-my-auth](../catalog/evidence/ton-my-auth.json), [ton-my-backup](../catalog/evidence/ton-my-backup.json), [ton-my-common](../catalog/evidence/ton-my-common.json), [ton-my-create](../catalog/evidence/ton-my-create.json), [ton-my-derive](../catalog/evidence/ton-my-derive.json), [ton-my-path](../catalog/evidence/ton-my-path.json), [ton-my-version](../catalog/evidence/ton-my-version.json), [ton-tep3](../catalog/evidence/ton-tep3.json)
- Подтверждаемое утверждение: generateMnemonic\(isBip39\) selects BIP39 or native generation; not a product-name-wide assumption. Reviewed 2026-09-29; byte SHA-256 c6401d8455eb936f01cf951ba523eba8a19d69b386e3b116af256dc2a5b578a1. See docs/research/batches/bip39-ton.md.
- Подтверждаемое утверждение: BackupSecretWords retrieves fetchMnemonic and renders SecretWordsContent, proving the reviewed mnemonic modes expose manual backup in this web source. Reviewed 2026-09-29; byte SHA-256 724207d342eefabc654f030fc5df8720a96c8267c04ca5da822baa0fbd7325b1. See docs/research/batches/bip39-ton.md.
- Подтверждаемое утверждение: generateBip39Mnemonic uses bip39.generateMnemonic\(128\), hence 12 words; getMnemonic exports a stored secret. Import validation is a separate operation. Reviewed 2026-09-29; byte SHA-256 e435194f56181b0b9c1ac44934c1adf96b1518d53cbe76ac6a27ba455af432c6. See docs/research/batches/bip39-ton.md.
- Подтверждаемое утверждение: Creation passes \!forceAddingTonOnlyAccount to generateMnemonic, preserving distinct simultaneous modes. Reviewed 2026-09-29; byte SHA-256 3bc4849d9a8573e9e06182f4aefbc17e2aa358ff37e24c49d24cb5a24a210786. See docs/research/batches/bip39-ton.md.
- Подтверждаемое утверждение: TON auth.ts generates 24 native words, rerolling BIP39 ambiguity; explicit bip39 accounts use BIP39 seed and Ed25519 path derivation. Stored native words use TON default seed without implicit normalization. Reviewed 2026-09-29; byte SHA-256 35286bbfb6c1d6022569738a054dd32d060b1fc48c6a1143dab1df705a218211. See docs/research/batches/bip39-ton.md.
- Подтверждаемое утверждение: TON\_BIP39\_PATH is hardened path components 44, 607, account index; slot zero is the TEP-3 main-account path. Reviewed 2026-09-29; byte SHA-256 5d799c9d1ec5fc23bf85245a477772a744cbf19a0ef7bef0aa8ecf9c1bd1c670. See docs/research/batches/bip39-ton.md.
- Подтверждаемое утверждение: package.json names mytonwallet version 26.9.8. Catalogue claims only this full source commit, not an entire release interval. Reviewed 2026-09-29; byte SHA-256 93b9311800850e215a424d9eefdb512958e33cbe0ad3e7fe17d0bbf771698e32. See docs/research/batches/bip39-ton.md.
- Подтверждаемое утверждение: TEP-3 sections 2-4 and 8-12 distinguish native 24-word TON and multichain BIP39 12/24-word modes sharing the English vocabulary, with TON path hardened path components 44, 607, 0 for the latter. It recommends new 12-word multichain or native 24-word generation, not new 24-word multichain. Import may encounter both. TEP is guidance, not proof of any product release transition; Pro MAM is a separate derivation. Reviewed 2026-09-29; byte SHA-256 4049020b927f72f7187b04f3e61e27f478caf1669fd528f21b815417b428be4b. See docs/research/batches/bip39-ton.md.
- Другие названия: My Wallet, MyTonWallet
- Схема: [ton-multichain-bip39](#scheme-ton-multichain-bip39)
- Создаёт мнемонику / только импорт: true / false
- Ограничения: Exact source snapshot supports default 128-bit BIP39 generation \(12 words\), native-mode override and backup display. Import of 24-word BIP39 does not imply new 24-word generation.; Full TON-path public known answer not reproduced; no blanket mapping to installed web/mobile releases or historical version intervals.
- Рекомендация профиля: Use the original trusted wallet's backup and recovery procedure. Match exact product, platform, source version and mode. Never enter a complete recovery phrase into Tessaveil or a website.

<a id="wallet-mytonwallet-native"></a>

### My Wallet / MyTonWallet — TON only — mytonwallet-native

- Исходная запись: [mytonwallet-native](../catalog/wallets/mytonwallet-native.json)
- Статус: verified
- Причина: Проверенная исследовательская запись; не гарантия релиза или безопасности.
- Диапазон версий (min / max): 26.9.8-source-f042bcc06b84f0cec928a29795f1cb8bf60a3e9c / 26.9.8-source-f042bcc06b84f0cec928a29795f1cb8bf60a3e9c
- Дата проверки: 2026-09-29
- Историческая запись: false
- Доказательства: [ton-my-auth](../catalog/evidence/ton-my-auth.json), [ton-my-backup](../catalog/evidence/ton-my-backup.json), [ton-my-create](../catalog/evidence/ton-my-create.json), [ton-my-derive](../catalog/evidence/ton-my-derive.json), [ton-my-version](../catalog/evidence/ton-my-version.json), [ton-native-source](../catalog/evidence/ton-native-source.json), [ton-tep3](../catalog/evidence/ton-tep3.json)
- Подтверждаемое утверждение: generateMnemonic\(isBip39\) selects BIP39 or native generation; not a product-name-wide assumption. Reviewed 2026-09-29; byte SHA-256 c6401d8455eb936f01cf951ba523eba8a19d69b386e3b116af256dc2a5b578a1. See docs/research/batches/bip39-ton.md.
- Подтверждаемое утверждение: BackupSecretWords retrieves fetchMnemonic and renders SecretWordsContent, proving the reviewed mnemonic modes expose manual backup in this web source. Reviewed 2026-09-29; byte SHA-256 724207d342eefabc654f030fc5df8720a96c8267c04ca5da822baa0fbd7325b1. See docs/research/batches/bip39-ton.md.
- Подтверждаемое утверждение: Creation passes \!forceAddingTonOnlyAccount to generateMnemonic, preserving distinct simultaneous modes. Reviewed 2026-09-29; byte SHA-256 3bc4849d9a8573e9e06182f4aefbc17e2aa358ff37e24c49d24cb5a24a210786. See docs/research/batches/bip39-ton.md.
- Подтверждаемое утверждение: TON auth.ts generates 24 native words, rerolling BIP39 ambiguity; explicit bip39 accounts use BIP39 seed and Ed25519 path derivation. Stored native words use TON default seed without implicit normalization. Reviewed 2026-09-29; byte SHA-256 35286bbfb6c1d6022569738a054dd32d060b1fc48c6a1143dab1df705a218211. See docs/research/batches/bip39-ton.md.
- Подтверждаемое утверждение: package.json names mytonwallet version 26.9.8. Catalogue claims only this full source commit, not an entire release interval. Reviewed 2026-09-29; byte SHA-256 93b9311800850e215a424d9eefdb512958e33cbe0ad3e7fe17d0bbf771698e32. See docs/research/batches/bip39-ton.md.
- Подтверждаемое утверждение: TON crypto mnemonic.ts\: mnemonicNew defaults to 24; entropy is HMAC-SHA512\(key=space-joined words, message=optional password\), then PBKDF2-HMAC-SHA512 with TON default seed salt and 100000 iterations; first 32 bytes seed Ed25519. Basic-seed check uses TON seed version and 390 iterations. Native lowercase/trim behavior is not a universal BIP39 NFKD rule. Reviewed 2026-09-29; byte SHA-256 79518c5f905daaa4e64f09454e8a82dbb1c8d1b310305ef84b25e85b2c77126a. See docs/research/batches/bip39-ton.md.
- Подтверждаемое утверждение: TEP-3 sections 2-4 and 8-12 distinguish native 24-word TON and multichain BIP39 12/24-word modes sharing the English vocabulary, with TON path hardened path components 44, 607, 0 for the latter. It recommends new 12-word multichain or native 24-word generation, not new 24-word multichain. Import may encounter both. TEP is guidance, not proof of any product release transition; Pro MAM is a separate derivation. Reviewed 2026-09-29; byte SHA-256 4049020b927f72f7187b04f3e61e27f478caf1669fd528f21b815417b428be4b. See docs/research/batches/bip39-ton.md.
- Другие названия: MyTonWallet TON only
- Схема: [ton-native](#scheme-ton-native)
- Создаёт мнемонику / только импорт: true / false
- Ограничения: Exact source snapshot only. forceAddingTonOnlyAccount chooses native generation; native generator returns 24 words and rejects BIP39-ambiguous candidates. This mode coexists with BIP39 in the same source version.; No assertion that all builds or older/newer installed versions expose the same mode.
- Рекомендация профиля: Use the original trusted wallet's backup and recovery procedure. Match exact product, platform, source version and mode. Never enter a complete recovery phrase into Tessaveil or a website.

<a id="wallet-openmask"></a>

### OpenMask — openmask

- Исходная запись: [openmask](../catalog/wallets/openmask.json)
- Статус: documented
- Причина: Доказательств недостаточно для доступной поддержки.
- Рекомендация: Недоступно для выбора; используйте процедуру резервного копирования самого кошелька.
- Диапазон версий (min / max): 0.22.0-source-9150d57d530296f8b27ae59e4dfce865be81550e / 0.22.0-source-9150d57d530296f8b27ae59e4dfce865be81550e
- Дата проверки: 2026-09-29
- Историческая запись: false
- Доказательства: [ton-openmask-create](../catalog/evidence/ton-openmask-create.json), [ton-openmask-identity](../catalog/evidence/ton-openmask-identity.json), [ton-openmask-version](../catalog/evidence/ton-openmask-version.json), [ton-tep3](../catalog/evidence/ton-tep3.json), [ton-tonweb-generate](../catalog/evidence/ton-tonweb-generate.json), [ton-tonweb-seed](../catalog/evidence/ton-tonweb-seed.json), [ton-tonweb-version](../catalog/evidence/ton-tonweb-version.json)
- Подтверждаемое утверждение: CreateWallet.tsx calls tonweb-mnemonic.generateMnemonic, displays recovery words, and checks selected words before wallet creation. Reviewed 2026-09-29; byte SHA-256 12d7e29578a4c58d76665375cc4ab498e010b5871baa290e0aaba24819a11362. See docs/research/batches/bip39-ton.md.
- Подтверждаемое утверждение: OpenProduct repository README identifies OpenMask Chrome/Chromium extension and its official openmask.app website. Reviewed 2026-09-29; byte SHA-256 007ec00e241abeb6d6aa354fe8251a3d6e5cc340af53847a140a885ac6e82249. See docs/research/batches/bip39-ton.md.
- Подтверждаемое утверждение: package.json identifies @openmask/extension version 0.22.0 and tonweb-mnemonic ^1.0.1; a range does not pin the installed dependency. Reviewed 2026-09-29; byte SHA-256 5c4d9320793ae712801603af2bccd294dbd1beaf5bae2739de280dd3fca2fa6a. See docs/research/batches/bip39-ton.md.
- Подтверждаемое утверждение: TEP-3 sections 2-4 and 8-12 distinguish native 24-word TON and multichain BIP39 12/24-word modes sharing the English vocabulary, with TON path hardened path components 44, 607, 0 for the latter. It recommends new 12-word multichain or native 24-word generation, not new 24-word multichain. Import may encounter both. TEP is guidance, not proof of any product release transition; Pro MAM is a separate derivation. Reviewed 2026-09-29; byte SHA-256 4049020b927f72f7187b04f3e61e27f478caf1669fd528f21b815417b428be4b. See docs/research/batches/bip39-ton.md.
- Подтверждаемое утверждение: Reviewed tonweb-mnemonic generator defaults to 24 words from its English list and TON basic-seed predicate. This does not bind every OpenMask installation to this source. Reviewed 2026-09-29; byte SHA-256 f0f05bd83dd03b22463be3deb85787ba3c69e094c88ad889ceed17073dea7249. See docs/research/batches/bip39-ton.md.
- Подтверждаемое утверждение: tonweb-mnemonic uses TON entropy, PBKDF2 with TON default seed and returns the first 32 bytes, not BIP39 seed derivation. Reviewed 2026-09-29; byte SHA-256 c2e34f6888d3b8b3192567bbe6dbdb1fc1e4a1db51228089a62c4c2e8e8f70b7. See docs/research/batches/bip39-ton.md.
- Подтверждаемое утверждение: Reviewed tonweb-mnemonic package is version 1.0.1 at this exact commit. Reviewed 2026-09-29; byte SHA-256 3a5777133b2ccfa280a3ab0bcd030d63a93ec07f97370f589845e26a1b158574. See docs/research/batches/bip39-ton.md.
- Другие названия: OpenMask Browser Extension
- Схема: [ton-native](#scheme-ton-native)
- Создаёт мнемонику / только импорт: true / false
- Ограничения: OpenProduct's Chrome extension source creates and displays a tonweb-mnemonic phrase. Package declares tonweb-mnemonic ^1.0.1; reviewed library 1.0.1 defaults to native 24.; Exact deployed extension/dependency artifact binding and a wallet-level reproducible recovery vector remain unproven; this source-backed mapping is documented, not selectable. Ledger and imported modes excluded.
- Рекомендация профиля: Use the original trusted wallet's backup and recovery procedure. Match exact product, platform, source version and mode. Never enter a complete recovery phrase into Tessaveil or a website.

<a id="wallet-ton-space"></a>

### TON Space / DeFi Account — ton-space

- Исходная запись: [ton-space](../catalog/wallets/ton-space.json)
- Статус: documented
- Причина: Доказательств недостаточно для доступной поддержки.
- Рекомендация: Недоступно для выбора; используйте процедуру резервного копирования самого кошелька.
- Диапазон версий (min / max): documentation-snapshot-2026-09-29-version-unresolved / documentation-snapshot-2026-09-29-version-unresolved
- Дата проверки: 2026-09-29
- Историческая запись: false
- Доказательства: [ton-space-doc](../catalog/evidence/ton-space-doc.json), [ton-space-security](../catalog/evidence/ton-space-security.json)
- Подтверждаемое утверждение: Current vendor DeFi Account page, reached from legacy TON Space URL, describes creation and separate manual/email backup; W5/v4R2 are contract versions and do not pin app mnemonic semantics. Reviewed 2026-09-29; byte SHA-256 506a3bc3c0a4861601fc606c90320acac8d4a2bd91a639b27190567530006d37. See docs/research/batches/bip39-ton.md.
- Подтверждаемое утверждение: Vendor Security headings What is a Secret Recovery Phrase and How can I find my seed phrase describe 24 words, viewing backup in settings, and use the term BIP-39 without publishing derivation/version details. This evidence gap prevents native/multichain mapping. Reviewed 2026-09-29; byte SHA-256 7f5a40f0e43d00d2a620972b9f2a1a5370ed4ad660f6d65d5ca25bc36f71b8dd. See docs/research/batches/bip39-ton.md.
- Другие названия: DeFi Account, TON Space, TON Wallet
- Схема: —
- Создаёт мнемонику / только импорт: true / false
- Ограничения: Legacy TON Space help URL redirects to current DeFi Account documentation. Manual backup exposes 24 words; current official security page calls it BIP-39 but supplies no derivation path, source revision or product version transition.; Native TON versus multichain semantics cannot be resolved from that wording. No scheme is selected; do not substitute historical TON-native assumptions.; Email backup and custodial Crypto Wallet are separate modes and cannot be represented by this manual-mnemonic profile. Contract W5/v4R2 is not an app version or mnemonic scheme boundary.
- Рекомендация профиля: Use the original trusted wallet's backup and recovery procedure. Match exact product, platform, source version and mode. Never enter a complete recovery phrase into Tessaveil or a website.

<a id="wallet-tonhub"></a>

### Tonhub — tonhub

- Исходная запись: [tonhub](../catalog/wallets/tonhub.json)
- Статус: verified
- Причина: Проверенная исследовательская запись; не гарантия релиза или безопасности.
- Диапазон версий (min / max): 2.5.45-source-a2503f79d14868d65349ad7035d18389c6e2f996 / 2.5.45-source-a2503f79d14868d65349ad7035d18389c6e2f996
- Дата проверки: 2026-09-29
- Историческая запись: false
- Доказательства: [ton-native-source](../catalog/evidence/ton-native-source.json), [ton-tep3](../catalog/evidence/ton-tep3.json), [tonhub-create](../catalog/evidence/tonhub-create.json), [tonhub-derive](../catalog/evidence/tonhub-derive.json), [tonhub-identity](../catalog/evidence/tonhub-identity.json), [tonhub-version](../catalog/evidence/tonhub-version.json)
- Подтверждаемое утверждение: TON crypto mnemonic.ts\: mnemonicNew defaults to 24; entropy is HMAC-SHA512\(key=space-joined words, message=optional password\), then PBKDF2-HMAC-SHA512 with TON default seed salt and 100000 iterations; first 32 bytes seed Ed25519. Basic-seed check uses TON seed version and 390 iterations. Native lowercase/trim behavior is not a universal BIP39 NFKD rule. Reviewed 2026-09-29; byte SHA-256 79518c5f905daaa4e64f09454e8a82dbb1c8d1b310305ef84b25e85b2c77126a. See docs/research/batches/bip39-ton.md.
- Подтверждаемое утверждение: TEP-3 sections 2-4 and 8-12 distinguish native 24-word TON and multichain BIP39 12/24-word modes sharing the English vocabulary, with TON path hardened path components 44, 607, 0 for the latter. It recommends new 12-word multichain or native 24-word generation, not new 24-word multichain. Import may encounter both. TEP is guidance, not proof of any product release transition; Pro MAM is a separate derivation. Reviewed 2026-09-29; byte SHA-256 4049020b927f72f7187b04f3e61e27f478caf1669fd528f21b815417b428be4b. See docs/research/batches/bip39-ton.md.
- Подтверждаемое утверждение: WalletCreateFragment invokes @ton/crypto mnemonicNew and displays the result in MnemonicsView before backup confirmation; native default is 24 words. Reviewed 2026-09-29; byte SHA-256 dafdd9c99b91982918502e45f077b9d5af518e6c531aa878fb666bc2ad9a1329. See docs/research/batches/bip39-ton.md.
- Подтверждаемое утверждение: createWalletFromMnemonics calls @ton/crypto mnemonicToWalletKey; this is TON-native, not ordinary BIP39 derivation. Reviewed 2026-09-29; byte SHA-256 b8341c61165ac9778a00e7eb7546b29a43ed0cc09ad520fdd3ce63011f8a5795. See docs/research/batches/bip39-ton.md.
- Подтверждаемое утверждение: Upstream README identifies this repository as Tonhub Wallet. Its GPL/distribution text is not permission to bundle wallet code; no wallet code is included. Reviewed 2026-09-29; byte SHA-256 59da82be7e3db101c4a8f72ee2b4e618ba6db87f9edaa5b9f939dd87f0a4c74b. See docs/research/batches/bip39-ton.md.
- Подтверждаемое утверждение: package.json is version 2.5.45 at the exact source commit. No binary or other-version identity is asserted. Reviewed 2026-09-29; byte SHA-256 ef41072e6abb6d6f983d669e0f8e9a8f182fd73a98406b251ad68f31379c6386. See docs/research/batches/bip39-ton.md.
- Другие названия: Tonhub Wallet
- Схема: [ton-native](#scheme-ton-native)
- Создаёт мнемонику / только импорт: true / false
- Ограничения: Exact React Native Android source snapshot only; creation invokes native mnemonicNew and displays its 24-word result before backup confirmation. Derivation uses mnemonicToWalletKey.; Hardware/Ledger, imported accounts, iOS binaries and other app versions are not covered by this profile. Wallet contract version changes do not establish mnemonic changes.
- Рекомендация профиля: Use the original trusted wallet's backup and recovery procedure. Match exact product, platform, source version and mode. Never enter a complete recovery phrase into Tessaveil or a website.

<a id="wallet-tonkeeper-classic"></a>

### Tonkeeper Classic — tonkeeper-classic

- Исходная запись: [tonkeeper-classic](../catalog/wallets/tonkeeper-classic.json)
- Статус: verified
- Причина: Проверенная исследовательская запись; не гарантия релиза или безопасности.
- Диапазон версий (min / max): source-4942adcdcddf55d57e3d3fc3676f019caf87357e / source-4942adcdcddf55d57e3d3fc3676f019caf87357e
- Дата проверки: 2026-09-29
- Историческая запись: false
- Доказательства: [ton-native-source](../catalog/evidence/ton-native-source.json), [ton-tep3](../catalog/evidence/ton-tep3.json), [tonkeeper-create](../catalog/evidence/tonkeeper-create.json), [tonkeeper-derive](../catalog/evidence/tonkeeper-derive.json), [tonkeeper-version](../catalog/evidence/tonkeeper-version.json)
- Подтверждаемое утверждение: TON crypto mnemonic.ts\: mnemonicNew defaults to 24; entropy is HMAC-SHA512\(key=space-joined words, message=optional password\), then PBKDF2-HMAC-SHA512 with TON default seed salt and 100000 iterations; first 32 bytes seed Ed25519. Basic-seed check uses TON seed version and 390 iterations. Native lowercase/trim behavior is not a universal BIP39 NFKD rule. Reviewed 2026-09-29; byte SHA-256 79518c5f905daaa4e64f09454e8a82dbb1c8d1b310305ef84b25e85b2c77126a. See docs/research/batches/bip39-ton.md.
- Подтверждаемое утверждение: TEP-3 sections 2-4 and 8-12 distinguish native 24-word TON and multichain BIP39 12/24-word modes sharing the English vocabulary, with TON path hardened path components 44, 607, 0 for the latter. It recommends new 12-word multichain or native 24-word generation, not new 24-word multichain. Import may encounter both. TEP is guidance, not proof of any product release transition; Pro MAM is a separate derivation. Reviewed 2026-09-29; byte SHA-256 4049020b927f72f7187b04f3e61e27f478caf1669fd528f21b815417b428be4b. See docs/research/batches/bip39-ton.md.
- Подтверждаемое утверждение: CreateStandardWallet invokes mnemonicNew\(24\), displays Words, checks backup and persists mnemonicType=ton. Reviewed 2026-09-29; byte SHA-256 a60930c7ec15e52b5cd5735738199b2cce50c3da510a424fe29b4eb7e642e74e. See docs/research/batches/bip39-ton.md.
- Подтверждаемое утверждение: mnemonicService distinguishes explicit ton from bip39; BIP39 follows hardened path components 44, 607, 0. This proves handling/derivation, not multichain generation by all products. Reviewed 2026-09-29; byte SHA-256 9852941011f82ec14e865c0cf33d78fa3944eeed5c61deeade94b65412d87643. See docs/research/batches/bip39-ton.md.
- Подтверждаемое утверждение: Extension manifest version is 3.0.0 at this exact source commit; web package 0.0.0 is not a deployed-version identifier. Reviewed 2026-09-29; byte SHA-256 7d8f4c2373bd7dcf5a3d5cd3e11407848baa178efef1ddda12b60b9c2c82b600. See docs/research/batches/bip39-ton.md.
- Другие названия: Tonkeeper
- Схема: [ton-native](#scheme-ton-native)
- Создаёт мнемонику / только импорт: true / false
- Ограничения: Source snapshot only\: extension manifest 3.0.0; web package is 0.0.0 and supplies no deployed release boundary. No claim for every installed Tonkeeper or Keeper version.; CreateStandardWallet creates and displays native 24 words; TRON integration does not turn that phrase into a BIP39 root. Pro multi-account MAM is excluded.
- Рекомендация профиля: Use the original trusted wallet's backup and recovery procedure. Match exact product, platform, source version and mode. Never enter a complete recovery phrase into Tessaveil or a website.

<a id="wallet-tonkeeper-multichain"></a>

### Keeper / Tonkeeper Multichain — tonkeeper-multichain

- Исходная запись: [tonkeeper-multichain](../catalog/wallets/tonkeeper-multichain.json)
- Статус: documented
- Причина: Доказательств недостаточно для доступной поддержки.
- Рекомендация: Недоступно для выбора; используйте процедуру резервного копирования самого кошелька.
- Диапазон версий (min / max): documentation-snapshot-2026-09-29-version-unresolved / documentation-snapshot-2026-09-29-version-unresolved
- Дата проверки: 2026-09-29
- Историческая запись: false
- Доказательства: [ton-keeper-doc](../catalog/evidence/ton-keeper-doc.json), [ton-tep3](../catalog/evidence/ton-tep3.json), [tonkeeper-derive](../catalog/evidence/tonkeeper-derive.json)
- Подтверждаемое утверждение: Keeper vendor explains Tonkeeper rebranding, new multichain-wallet creation and inability to directly convert existing native 24-word accounts. Documentation omits generation count, platform and exact app release boundary. Reviewed 2026-09-29; byte SHA-256 d7091696af9e14b254c181906e1a8e8b48a339835ae65ac753593cabcbcb768a. See docs/research/batches/bip39-ton.md.
- Подтверждаемое утверждение: TEP-3 sections 2-4 and 8-12 distinguish native 24-word TON and multichain BIP39 12/24-word modes sharing the English vocabulary, with TON path hardened path components 44, 607, 0 for the latter. It recommends new 12-word multichain or native 24-word generation, not new 24-word multichain. Import may encounter both. TEP is guidance, not proof of any product release transition; Pro MAM is a separate derivation. Reviewed 2026-09-29; byte SHA-256 4049020b927f72f7187b04f3e61e27f478caf1669fd528f21b815417b428be4b. See docs/research/batches/bip39-ton.md.
- Подтверждаемое утверждение: mnemonicService distinguishes explicit ton from bip39; BIP39 follows hardened path components 44, 607, 0. This proves handling/derivation, not multichain generation by all products. Reviewed 2026-09-29; byte SHA-256 9852941011f82ec14e865c0cf33d78fa3944eeed5c61deeade94b65412d87643. See docs/research/batches/bip39-ton.md.
- Другие названия: Keeper, Tonkeeper multichain
- Схема: [ton-multichain-bip39](#scheme-ton-multichain-bip39)
- Создаёт мнемонику / только импорт: true / false
- Ограничения: Official rebranding documentation confirms a separate new multichain wallet and says old native 24 words cannot be converted. It does not pin app platform/version or generation word count.; Pinned web source proves BIP39 import derivation, not that its new-wallet screen generates this mode. Exact first/last mobile versions and full-path known answer remain unproven; 12/24 are scheme lengths, not asserted generation lengths.; Keeper \(formerly Tonkeeper\) is not the unrelated Waves Keeper product; Pro MAM is excluded.
- Рекомендация профиля: Use the original trusted wallet's backup and recovery procedure. Match exact product, platform, source version and mode. Never enter a complete recovery phrase into Tessaveil or a website.

## Схемы

<a id="scheme-bip39"></a>

### BIP39 — bip39

- Исходная запись: [bip39](../catalog/schemes/bip39.json)
- Статус: verified
- Причина: Проверенная исследовательская запись; не гарантия релиза или безопасности.
- Диапазон версий (min / max): 3a10b5b5f0a7586df8928d580a3009744ebb2079 / 3a10b5b5f0a7586df8928d580a3009744ebb2079
- Дата проверки: 2026-09-29
- Историческая запись: false
- Доказательства: [bip39-spec](../catalog/evidence/bip39-spec.json), [bip39-vectors](../catalog/evidence/bip39-vectors.json)
- Подтверждаемое утверждение: Bitcoin BIP39 specifies 2048 indexed words, 12/15/18/21/24 lengths and UTF-8 NFKD for words, sentence and optional passphrase; equal vocabulary does not establish TON derivation. Reviewed 2026-09-29; byte SHA-256 afcbcbed36fe9eb734bd607398a8c124683ded2a75c3830e1b16c47b043a9134. See docs/research/batches/bip39-ton.md.
- Подтверждаемое утверждение: Trezor's public vectors.json supplies 24 independent entropy/mnemonic/seed known answers per language for all ten lists, with passphrase TREZOR. Offline test reconstructs words from entropy, checks published normalized sentence fingerprints and PBKDF2 seed. Public, non-funded data only; fixture projection contains no user phrase. Reviewed 2026-09-29; byte SHA-256 fa3b937b7cff9c9b8ecd3aa011faeb8d6dd67993174b72326e83f4de8fdb30f8. See docs/research/batches/bip39-ton.md.
- Словари: [bip39-cs](#dictionary-bip39-cs), [bip39-en](#dictionary-bip39-en), [bip39-es](#dictionary-bip39-es), [bip39-fr](#dictionary-bip39-fr), [bip39-it](#dictionary-bip39-it), [bip39-ja](#dictionary-bip39-ja), [bip39-ko](#dictionary-bip39-ko), [bip39-pt](#dictionary-bip39-pt), [bip39-zh-hans](#dictionary-bip39-zh-hans), [bip39-zh-hant](#dictionary-bip39-zh-hant)
- Допустимые длины: 12, 15, 18, 21, 24
- Позиционные правила: The same dictionary is eligible at every word position. Phrase checksum or seed validity is never evaluated by Tessaveil.
- Семантика: Entropy plus SHA-256 checksum selects 11-bit word indices. UTF-8 NFKD sentence and passphrase feed PBKDF2-HMAC-SHA512 with 2048 iterations and mnemonic-prefixed salt. The research tests reproduce public vectors only; Tessaveil never derives user keys or validates a complete phrase. Language changes produce different seeds.
- Внешний секрет / сохраняется: optional-passphrase / false
- Рекомендация о внешнем секрете: A scheme passphrase is external and never stored by Tessaveil. A wallet PIN or application password is not proof of a mnemonic passphrase; verify support in the exact source wallet.
- Тестовые векторы: [bip39-vectors](../catalog/evidence/bip39-vectors.json)

<a id="scheme-ton-multichain-bip39"></a>

### TON multichain — BIP39 12/24 words — ton-multichain-bip39

- Исходная запись: [ton-multichain-bip39](../catalog/schemes/ton-multichain-bip39.json)
- Статус: documented
- Причина: Доказательств недостаточно для доступной поддержки.
- Рекомендация: Недоступно для выбора; используйте процедуру резервного копирования самого кошелька.
- Диапазон версий (min / max): fe8a154e4dad9f5c0bf7240df278cb50ec6cd908 / fe8a154e4dad9f5c0bf7240df278cb50ec6cd908
- Дата проверки: 2026-09-29
- Историческая запись: false
- Доказательства: [bip39-spec](../catalog/evidence/bip39-spec.json), [bip39-vectors](../catalog/evidence/bip39-vectors.json), [ton-my-derive](../catalog/evidence/ton-my-derive.json), [ton-my-path](../catalog/evidence/ton-my-path.json), [ton-tep3](../catalog/evidence/ton-tep3.json)
- Подтверждаемое утверждение: Bitcoin BIP39 specifies 2048 indexed words, 12/15/18/21/24 lengths and UTF-8 NFKD for words, sentence and optional passphrase; equal vocabulary does not establish TON derivation. Reviewed 2026-09-29; byte SHA-256 afcbcbed36fe9eb734bd607398a8c124683ded2a75c3830e1b16c47b043a9134. See docs/research/batches/bip39-ton.md.
- Подтверждаемое утверждение: Trezor's public vectors.json supplies 24 independent entropy/mnemonic/seed known answers per language for all ten lists, with passphrase TREZOR. Offline test reconstructs words from entropy, checks published normalized sentence fingerprints and PBKDF2 seed. Public, non-funded data only; fixture projection contains no user phrase. Reviewed 2026-09-29; byte SHA-256 fa3b937b7cff9c9b8ecd3aa011faeb8d6dd67993174b72326e83f4de8fdb30f8. See docs/research/batches/bip39-ton.md.
- Подтверждаемое утверждение: TON auth.ts generates 24 native words, rerolling BIP39 ambiguity; explicit bip39 accounts use BIP39 seed and Ed25519 path derivation. Stored native words use TON default seed without implicit normalization. Reviewed 2026-09-29; byte SHA-256 35286bbfb6c1d6022569738a054dd32d060b1fc48c6a1143dab1df705a218211. See docs/research/batches/bip39-ton.md.
- Подтверждаемое утверждение: TON\_BIP39\_PATH is hardened path components 44, 607, account index; slot zero is the TEP-3 main-account path. Reviewed 2026-09-29; byte SHA-256 5d799c9d1ec5fc23bf85245a477772a744cbf19a0ef7bef0aa8ecf9c1bd1c670. See docs/research/batches/bip39-ton.md.
- Подтверждаемое утверждение: TEP-3 sections 2-4 and 8-12 distinguish native 24-word TON and multichain BIP39 12/24-word modes sharing the English vocabulary, with TON path hardened path components 44, 607, 0 for the latter. It recommends new 12-word multichain or native 24-word generation, not new 24-word multichain. Import may encounter both. TEP is guidance, not proof of any product release transition; Pro MAM is a separate derivation. Reviewed 2026-09-29; byte SHA-256 4049020b927f72f7187b04f3e61e27f478caf1669fd528f21b815417b428be4b. See docs/research/batches/bip39-ton.md.
- Словари: [bip39-en](#dictionary-bip39-en)
- Допустимые длины: 12, 24
- Позиционные правила: The same dictionary is eligible at every word position. Phrase checksum or seed validity is never evaluated by Tessaveil.
- Семантика: TEP-3 BIP39 then SLIP-0010 Ed25519 at hardened path components 44, 607, 0, with indexed subwallet paths. 12 and 24 are import/profile lengths; TEP discourages new 24-word multichain generation. BIP39 public vectors verify only its seed stage. An independent published full TON derivation-path known answer has not been reproduced in this batch, so this scheme remains documented and not selectable.
- Внешний секрет / сохраняется: optional-passphrase / false
- Рекомендация о внешнем секрете: A scheme passphrase is external and never stored by Tessaveil. A wallet PIN or application password is not proof of a mnemonic passphrase; verify support in the exact source wallet.
- Тестовые векторы: [bip39-vectors](../catalog/evidence/bip39-vectors.json)

<a id="scheme-ton-native"></a>

### TON native — 24 words — ton-native

- Исходная запись: [ton-native](../catalog/schemes/ton-native.json)
- Статус: verified
- Причина: Проверенная исследовательская запись; не гарантия релиза или безопасности.
- Диапазон версий (min / max): fe8a154e4dad9f5c0bf7240df278cb50ec6cd908 / fe8a154e4dad9f5c0bf7240df278cb50ec6cd908
- Дата проверки: 2026-09-29
- Историческая запись: false
- Доказательства: [ton-native-license](../catalog/evidence/ton-native-license.json), [ton-native-source](../catalog/evidence/ton-native-source.json), [ton-native-vectors](../catalog/evidence/ton-native-vectors.json), [ton-native-wordlist](../catalog/evidence/ton-native-wordlist.json), [ton-tep3](../catalog/evidence/ton-tep3.json)
- Подтверждаемое утверждение: The actual MIT license permits the five public vector projections with retained Copyright \(c\) 2021-2023 Whales Corp. and permission notice in THIRD\_PARTY\_NOTICES. No TON implementation code or wallet binaries are bundled. Reviewed 2026-09-29; byte SHA-256 33578b9ea1522de18164cf1d1ef8e52f50d748ae17c7d38b4fa5e6f50207f8eb. See docs/research/batches/bip39-ton.md.
- Подтверждаемое утверждение: TON crypto mnemonic.ts\: mnemonicNew defaults to 24; entropy is HMAC-SHA512\(key=space-joined words, message=optional password\), then PBKDF2-HMAC-SHA512 with TON default seed salt and 100000 iterations; first 32 bytes seed Ed25519. Basic-seed check uses TON seed version and 390 iterations. Native lowercase/trim behavior is not a universal BIP39 NFKD rule. Reviewed 2026-09-29; byte SHA-256 79518c5f905daaa4e64f09454e8a82dbb1c8d1b310305ef84b25e85b2c77126a. See docs/research/batches/bip39-ton.md.
- Подтверждаемое утверждение: Five public mnemonic.spec.ts vectors independently provide 24 English words and expected Ed25519 secretKey. Fixture retains zero-based dictionary indices and the first 32 bytes of each published secretKey \(seed\). Offline standard-library HMAC/PBKDF2 checks those published seeds and the basic-seed predicate; it does not test Ed25519 public keys or addresses. Reviewed 2026-09-29; byte SHA-256 ba6936664624168caf454df777b4ef8354c034c49b121a493c44237e4880cd83. See docs/research/batches/bip39-ton.md.
- Подтверждаемое утверждение: TON crypto's wordlist.ts contains exactly the same 2048 English tokens in the same order as the pinned BIP39 English list. Compared by extracting its single-quoted alphabetic tokens; only the unchanged BIP39 text file is bundled. Source byte SHA-256 2bc9a19c24279d659c4d02e08f9381af16cd62bdbb5103ce1815db4a7861c9db. Reviewed 2026-09-29; see docs/research/batches/bip39-ton.md.
- Подтверждаемое утверждение: TEP-3 sections 2-4 and 8-12 distinguish native 24-word TON and multichain BIP39 12/24-word modes sharing the English vocabulary, with TON path hardened path components 44, 607, 0 for the latter. It recommends new 12-word multichain or native 24-word generation, not new 24-word multichain. Import may encounter both. TEP is guidance, not proof of any product release transition; Pro MAM is a separate derivation. Reviewed 2026-09-29; byte SHA-256 4049020b927f72f7187b04f3e61e27f478caf1669fd528f21b815417b428be4b. See docs/research/batches/bip39-ton.md.
- Словари: [bip39-en](#dictionary-bip39-en)
- Допустимые длины: 24
- Позиционные правила: The same dictionary is eligible at every word position. Phrase checksum or seed validity is never evaluated by Tessaveil.
- Семантика: English BIP39 vocabulary only; TON HMAC/PBKDF2 seed and seed-version constraints differ from BIP39 checksum and seed derivation. Native 24 words are not automatically BIP39-compatible. V3/V4/V5 are smart-contract versions, not mnemonic scheme versions. Tests cover public seed derivation only, not addresses.
- Внешний секрет / сохраняется: optional-passphrase / false
- Рекомендация о внешнем секрете: A scheme passphrase is external and never stored by Tessaveil. A wallet PIN or application password is not proof of a mnemonic passphrase; verify support in the exact source wallet.
- Тестовые векторы: [ton-native-vectors](../catalog/evidence/ton-native-vectors.json)

## Словари (одна запись на ID)

<a id="dictionary-bip39-cs"></a>

### BIP39 — Чешский — bip39-cs

- Исходная запись: [bip39-cs](../catalog/dictionaries/bip39-cs.json)
- Статус: verified
- Причина: Проверенная исследовательская запись; не гарантия релиза или безопасности.
- Диапазон версий (min / max): 3a10b5b5f0a7586df8928d580a3009744ebb2079 / 3a10b5b5f0a7586df8928d580a3009744ebb2079
- Дата проверки: 2026-09-29
- Историческая запись: false
- Доказательства: [bip39-guidance](../catalog/evidence/bip39-guidance.json), [bip39-license](../catalog/evidence/bip39-license.json), [bip39-osi-mit](../catalog/evidence/bip39-osi-mit.json), [bip39-signpath](../catalog/evidence/bip39-signpath.json), [bip39-spec](../catalog/evidence/bip39-spec.json), [bip39-vectors](../catalog/evidence/bip39-vectors.json)
- Подтверждаемое утверждение: BIP39 links exactly ten language lists and language-specific guidance; Japanese generation uses ideographic spaces, which NFKD converts to ASCII spaces. Original source line order and bytes are preserved. Reviewed 2026-09-29; byte SHA-256 363a51bc4748d95541bb156e0439de7b51f28b260433c09874e5891dd3b0f883. See docs/research/batches/bip39-ton.md.
- Подтверждаемое утверждение: Local license review by Codex\: the actual MIT license of the BIP39 reference implementation permits redistribution with copyright and permission notice. Every bundled bitcoin/bips list is byte-identical to src/mnemonic/wordlist at this licensed reference revision; vectors.json is in the same repository. No directory-specific exception was found. Notices preserve the license and attribution. repository\_redistribution=allowed for these exact bytes and public test projections, not arbitrary BIPs material. Reviewed 2026-09-29; byte SHA-256 d5e3c7c62a84e80073201e2f6e5130e9e6804fa05f8ac4f8b26a13c7d3969697. See docs/research/batches/bip39-ton.md.
- Подтверждаемое утверждение: OSI identifies MIT as an approved open-source license; this corroborates the local component assessment, while the pinned reference repository license supplies the actual permission. Reviewed 2026-09-29; byte SHA-256 004c79db0a335488afc87600d89f447dce7fb4d24d510af15ed4381a24be848c. See docs/research/batches/bip39-ton.md.
- Подтверждаемое утверждение: Local component review by Codex\: the exact MIT-licensed lists are source data with no executable dependencies or proprietary restrictions. Together with retained MIT notices and OSI approval this supports signpath\_compatible=compatible for this payload only. SignPath terms require OSS components; this is not Foundation acceptance or project release/signing approval. Reviewed 2026-09-29; byte SHA-256 6610cf889bbe0dc7533abaa310bc7a5cc9a61ae6c2ce0798a08109c925b46c51. See docs/research/batches/bip39-ton.md.
- Подтверждаемое утверждение: Bitcoin BIP39 specifies 2048 indexed words, 12/15/18/21/24 lengths and UTF-8 NFKD for words, sentence and optional passphrase; equal vocabulary does not establish TON derivation. Reviewed 2026-09-29; byte SHA-256 afcbcbed36fe9eb734bd607398a8c124683ded2a75c3830e1b16c47b043a9134. See docs/research/batches/bip39-ton.md.
- Подтверждаемое утверждение: Trezor's public vectors.json supplies 24 independent entropy/mnemonic/seed known answers per language for all ten lists, with passphrase TREZOR. Offline test reconstructs words from entropy, checks published normalized sentence fingerprints and PBKDF2 seed. Public, non-funded data only; fixture projection contains no user phrase. Reviewed 2026-09-29; byte SHA-256 fa3b937b7cff9c9b8ecd3aa011faeb8d6dd67993174b72326e83f4de8fdb30f8. See docs/research/batches/bip39-ton.md.
- Язык: cs
- Письменность: Latn
- Кодировка: UTF-8
- Нормализация: NFKD
- Количество слов: 2048
- SHA-256: 7e80e161c3e93d9554c2efb78d4e3cebf8fc727e9c52e03b83b94406bdcc95fc
- Порядок слов: Exact upstream source line order; zero-based 11-bit indices 0 through 2047. UTF-8 LF bytes and final newline preserved without transformation.
- Позиционные правила: The same dictionary is eligible at every word position. Phrase checksum or seed validity is never evaluated by Tessaveil.
- Ревизия источника: 3a10b5b5f0a7586df8928d580a3009744ebb2079
- Лицензия: MIT
- Атрибуция: BIP39 authors Marek Palatinus, Pavol Rusnak, Aaron Voisine, Sean Bowe and word-list contributors. Byte-identical reference copy\: Copyright \(c\) 2013-2016 Pavol Rusnak. Full license and language credits in THIRD\_PARTY\_NOTICES.
- Распространение в репозитории: allowed
- Совместимость с SignPath: compatible
- Доказательства лицензии: [bip39-license](../catalog/evidence/bip39-license.json), [bip39-osi-mit](../catalog/evidence/bip39-osi-mit.json), [bip39-signpath](../catalog/evidence/bip39-signpath.json)
- Тестовые векторы: [bip39-vectors](../catalog/evidence/bip39-vectors.json)

<a id="dictionary-bip39-en"></a>

### BIP39 — Английский — bip39-en

- Исходная запись: [bip39-en](../catalog/dictionaries/bip39-en.json)
- Статус: verified
- Причина: Проверенная исследовательская запись; не гарантия релиза или безопасности.
- Диапазон версий (min / max): 3a10b5b5f0a7586df8928d580a3009744ebb2079 / 3a10b5b5f0a7586df8928d580a3009744ebb2079
- Дата проверки: 2026-09-29
- Историческая запись: false
- Доказательства: [bip39-guidance](../catalog/evidence/bip39-guidance.json), [bip39-license](../catalog/evidence/bip39-license.json), [bip39-osi-mit](../catalog/evidence/bip39-osi-mit.json), [bip39-signpath](../catalog/evidence/bip39-signpath.json), [bip39-spec](../catalog/evidence/bip39-spec.json), [bip39-vectors](../catalog/evidence/bip39-vectors.json)
- Подтверждаемое утверждение: BIP39 links exactly ten language lists and language-specific guidance; Japanese generation uses ideographic spaces, which NFKD converts to ASCII spaces. Original source line order and bytes are preserved. Reviewed 2026-09-29; byte SHA-256 363a51bc4748d95541bb156e0439de7b51f28b260433c09874e5891dd3b0f883. See docs/research/batches/bip39-ton.md.
- Подтверждаемое утверждение: Local license review by Codex\: the actual MIT license of the BIP39 reference implementation permits redistribution with copyright and permission notice. Every bundled bitcoin/bips list is byte-identical to src/mnemonic/wordlist at this licensed reference revision; vectors.json is in the same repository. No directory-specific exception was found. Notices preserve the license and attribution. repository\_redistribution=allowed for these exact bytes and public test projections, not arbitrary BIPs material. Reviewed 2026-09-29; byte SHA-256 d5e3c7c62a84e80073201e2f6e5130e9e6804fa05f8ac4f8b26a13c7d3969697. See docs/research/batches/bip39-ton.md.
- Подтверждаемое утверждение: OSI identifies MIT as an approved open-source license; this corroborates the local component assessment, while the pinned reference repository license supplies the actual permission. Reviewed 2026-09-29; byte SHA-256 004c79db0a335488afc87600d89f447dce7fb4d24d510af15ed4381a24be848c. See docs/research/batches/bip39-ton.md.
- Подтверждаемое утверждение: Local component review by Codex\: the exact MIT-licensed lists are source data with no executable dependencies or proprietary restrictions. Together with retained MIT notices and OSI approval this supports signpath\_compatible=compatible for this payload only. SignPath terms require OSS components; this is not Foundation acceptance or project release/signing approval. Reviewed 2026-09-29; byte SHA-256 6610cf889bbe0dc7533abaa310bc7a5cc9a61ae6c2ce0798a08109c925b46c51. See docs/research/batches/bip39-ton.md.
- Подтверждаемое утверждение: Bitcoin BIP39 specifies 2048 indexed words, 12/15/18/21/24 lengths and UTF-8 NFKD for words, sentence and optional passphrase; equal vocabulary does not establish TON derivation. Reviewed 2026-09-29; byte SHA-256 afcbcbed36fe9eb734bd607398a8c124683ded2a75c3830e1b16c47b043a9134. See docs/research/batches/bip39-ton.md.
- Подтверждаемое утверждение: Trezor's public vectors.json supplies 24 independent entropy/mnemonic/seed known answers per language for all ten lists, with passphrase TREZOR. Offline test reconstructs words from entropy, checks published normalized sentence fingerprints and PBKDF2 seed. Public, non-funded data only; fixture projection contains no user phrase. Reviewed 2026-09-29; byte SHA-256 fa3b937b7cff9c9b8ecd3aa011faeb8d6dd67993174b72326e83f4de8fdb30f8. See docs/research/batches/bip39-ton.md.
- Язык: en
- Письменность: Latn
- Кодировка: UTF-8
- Нормализация: NFKD
- Количество слов: 2048
- SHA-256: 2f5eed53a4727b4bf8880d8f3f199efc90e58503646d9ff8eff3a2ed3b24dbda
- Порядок слов: Exact upstream source line order; zero-based 11-bit indices 0 through 2047. UTF-8 LF bytes and final newline preserved without transformation.
- Позиционные правила: The same dictionary is eligible at every word position. Phrase checksum or seed validity is never evaluated by Tessaveil.
- Ревизия источника: 3a10b5b5f0a7586df8928d580a3009744ebb2079
- Лицензия: MIT
- Атрибуция: BIP39 authors Marek Palatinus, Pavol Rusnak, Aaron Voisine, Sean Bowe and word-list contributors. Byte-identical reference copy\: Copyright \(c\) 2013-2016 Pavol Rusnak. Full license and language credits in THIRD\_PARTY\_NOTICES.
- Распространение в репозитории: allowed
- Совместимость с SignPath: compatible
- Доказательства лицензии: [bip39-license](../catalog/evidence/bip39-license.json), [bip39-osi-mit](../catalog/evidence/bip39-osi-mit.json), [bip39-signpath](../catalog/evidence/bip39-signpath.json)
- Тестовые векторы: [bip39-vectors](../catalog/evidence/bip39-vectors.json)

<a id="dictionary-bip39-es"></a>

### BIP39 — Испанский — bip39-es

- Исходная запись: [bip39-es](../catalog/dictionaries/bip39-es.json)
- Статус: verified
- Причина: Проверенная исследовательская запись; не гарантия релиза или безопасности.
- Диапазон версий (min / max): 3a10b5b5f0a7586df8928d580a3009744ebb2079 / 3a10b5b5f0a7586df8928d580a3009744ebb2079
- Дата проверки: 2026-09-29
- Историческая запись: false
- Доказательства: [bip39-guidance](../catalog/evidence/bip39-guidance.json), [bip39-license](../catalog/evidence/bip39-license.json), [bip39-osi-mit](../catalog/evidence/bip39-osi-mit.json), [bip39-signpath](../catalog/evidence/bip39-signpath.json), [bip39-spec](../catalog/evidence/bip39-spec.json), [bip39-vectors](../catalog/evidence/bip39-vectors.json)
- Подтверждаемое утверждение: BIP39 links exactly ten language lists and language-specific guidance; Japanese generation uses ideographic spaces, which NFKD converts to ASCII spaces. Original source line order and bytes are preserved. Reviewed 2026-09-29; byte SHA-256 363a51bc4748d95541bb156e0439de7b51f28b260433c09874e5891dd3b0f883. See docs/research/batches/bip39-ton.md.
- Подтверждаемое утверждение: Local license review by Codex\: the actual MIT license of the BIP39 reference implementation permits redistribution with copyright and permission notice. Every bundled bitcoin/bips list is byte-identical to src/mnemonic/wordlist at this licensed reference revision; vectors.json is in the same repository. No directory-specific exception was found. Notices preserve the license and attribution. repository\_redistribution=allowed for these exact bytes and public test projections, not arbitrary BIPs material. Reviewed 2026-09-29; byte SHA-256 d5e3c7c62a84e80073201e2f6e5130e9e6804fa05f8ac4f8b26a13c7d3969697. See docs/research/batches/bip39-ton.md.
- Подтверждаемое утверждение: OSI identifies MIT as an approved open-source license; this corroborates the local component assessment, while the pinned reference repository license supplies the actual permission. Reviewed 2026-09-29; byte SHA-256 004c79db0a335488afc87600d89f447dce7fb4d24d510af15ed4381a24be848c. See docs/research/batches/bip39-ton.md.
- Подтверждаемое утверждение: Local component review by Codex\: the exact MIT-licensed lists are source data with no executable dependencies or proprietary restrictions. Together with retained MIT notices and OSI approval this supports signpath\_compatible=compatible for this payload only. SignPath terms require OSS components; this is not Foundation acceptance or project release/signing approval. Reviewed 2026-09-29; byte SHA-256 6610cf889bbe0dc7533abaa310bc7a5cc9a61ae6c2ce0798a08109c925b46c51. See docs/research/batches/bip39-ton.md.
- Подтверждаемое утверждение: Bitcoin BIP39 specifies 2048 indexed words, 12/15/18/21/24 lengths and UTF-8 NFKD for words, sentence and optional passphrase; equal vocabulary does not establish TON derivation. Reviewed 2026-09-29; byte SHA-256 afcbcbed36fe9eb734bd607398a8c124683ded2a75c3830e1b16c47b043a9134. See docs/research/batches/bip39-ton.md.
- Подтверждаемое утверждение: Trezor's public vectors.json supplies 24 independent entropy/mnemonic/seed known answers per language for all ten lists, with passphrase TREZOR. Offline test reconstructs words from entropy, checks published normalized sentence fingerprints and PBKDF2 seed. Public, non-funded data only; fixture projection contains no user phrase. Reviewed 2026-09-29; byte SHA-256 fa3b937b7cff9c9b8ecd3aa011faeb8d6dd67993174b72326e83f4de8fdb30f8. See docs/research/batches/bip39-ton.md.
- Язык: es
- Письменность: Latn
- Кодировка: UTF-8
- Нормализация: NFKD
- Количество слов: 2048
- SHA-256: 46846a5a0139d1e3cb77293e521c2865f7bcdb82c44e8d0a06a2cd0ecba48c0b
- Порядок слов: Exact upstream source line order; zero-based 11-bit indices 0 through 2047. UTF-8 LF bytes and final newline preserved without transformation.
- Позиционные правила: The same dictionary is eligible at every word position. Phrase checksum or seed validity is never evaluated by Tessaveil.
- Ревизия источника: 3a10b5b5f0a7586df8928d580a3009744ebb2079
- Лицензия: MIT
- Атрибуция: BIP39 authors Marek Palatinus, Pavol Rusnak, Aaron Voisine, Sean Bowe and word-list contributors. Byte-identical reference copy\: Copyright \(c\) 2013-2016 Pavol Rusnak. Full license and language credits in THIRD\_PARTY\_NOTICES.
- Распространение в репозитории: allowed
- Совместимость с SignPath: compatible
- Доказательства лицензии: [bip39-license](../catalog/evidence/bip39-license.json), [bip39-osi-mit](../catalog/evidence/bip39-osi-mit.json), [bip39-signpath](../catalog/evidence/bip39-signpath.json)
- Тестовые векторы: [bip39-vectors](../catalog/evidence/bip39-vectors.json)

<a id="dictionary-bip39-fr"></a>

### BIP39 — Французский — bip39-fr

- Исходная запись: [bip39-fr](../catalog/dictionaries/bip39-fr.json)
- Статус: verified
- Причина: Проверенная исследовательская запись; не гарантия релиза или безопасности.
- Диапазон версий (min / max): 3a10b5b5f0a7586df8928d580a3009744ebb2079 / 3a10b5b5f0a7586df8928d580a3009744ebb2079
- Дата проверки: 2026-09-29
- Историческая запись: false
- Доказательства: [bip39-guidance](../catalog/evidence/bip39-guidance.json), [bip39-license](../catalog/evidence/bip39-license.json), [bip39-osi-mit](../catalog/evidence/bip39-osi-mit.json), [bip39-signpath](../catalog/evidence/bip39-signpath.json), [bip39-spec](../catalog/evidence/bip39-spec.json), [bip39-vectors](../catalog/evidence/bip39-vectors.json)
- Подтверждаемое утверждение: BIP39 links exactly ten language lists and language-specific guidance; Japanese generation uses ideographic spaces, which NFKD converts to ASCII spaces. Original source line order and bytes are preserved. Reviewed 2026-09-29; byte SHA-256 363a51bc4748d95541bb156e0439de7b51f28b260433c09874e5891dd3b0f883. See docs/research/batches/bip39-ton.md.
- Подтверждаемое утверждение: Local license review by Codex\: the actual MIT license of the BIP39 reference implementation permits redistribution with copyright and permission notice. Every bundled bitcoin/bips list is byte-identical to src/mnemonic/wordlist at this licensed reference revision; vectors.json is in the same repository. No directory-specific exception was found. Notices preserve the license and attribution. repository\_redistribution=allowed for these exact bytes and public test projections, not arbitrary BIPs material. Reviewed 2026-09-29; byte SHA-256 d5e3c7c62a84e80073201e2f6e5130e9e6804fa05f8ac4f8b26a13c7d3969697. See docs/research/batches/bip39-ton.md.
- Подтверждаемое утверждение: OSI identifies MIT as an approved open-source license; this corroborates the local component assessment, while the pinned reference repository license supplies the actual permission. Reviewed 2026-09-29; byte SHA-256 004c79db0a335488afc87600d89f447dce7fb4d24d510af15ed4381a24be848c. See docs/research/batches/bip39-ton.md.
- Подтверждаемое утверждение: Local component review by Codex\: the exact MIT-licensed lists are source data with no executable dependencies or proprietary restrictions. Together with retained MIT notices and OSI approval this supports signpath\_compatible=compatible for this payload only. SignPath terms require OSS components; this is not Foundation acceptance or project release/signing approval. Reviewed 2026-09-29; byte SHA-256 6610cf889bbe0dc7533abaa310bc7a5cc9a61ae6c2ce0798a08109c925b46c51. See docs/research/batches/bip39-ton.md.
- Подтверждаемое утверждение: Bitcoin BIP39 specifies 2048 indexed words, 12/15/18/21/24 lengths and UTF-8 NFKD for words, sentence and optional passphrase; equal vocabulary does not establish TON derivation. Reviewed 2026-09-29; byte SHA-256 afcbcbed36fe9eb734bd607398a8c124683ded2a75c3830e1b16c47b043a9134. See docs/research/batches/bip39-ton.md.
- Подтверждаемое утверждение: Trezor's public vectors.json supplies 24 independent entropy/mnemonic/seed known answers per language for all ten lists, with passphrase TREZOR. Offline test reconstructs words from entropy, checks published normalized sentence fingerprints and PBKDF2 seed. Public, non-funded data only; fixture projection contains no user phrase. Reviewed 2026-09-29; byte SHA-256 fa3b937b7cff9c9b8ecd3aa011faeb8d6dd67993174b72326e83f4de8fdb30f8. See docs/research/batches/bip39-ton.md.
- Язык: fr
- Письменность: Latn
- Кодировка: UTF-8
- Нормализация: NFKD
- Количество слов: 2048
- SHA-256: ebc3959ab7801a1df6bac4fa7d970652f1df76b683cd2f4003c941c63d517e59
- Порядок слов: Exact upstream source line order; zero-based 11-bit indices 0 through 2047. UTF-8 LF bytes and final newline preserved without transformation.
- Позиционные правила: The same dictionary is eligible at every word position. Phrase checksum or seed validity is never evaluated by Tessaveil.
- Ревизия источника: 3a10b5b5f0a7586df8928d580a3009744ebb2079
- Лицензия: MIT
- Атрибуция: BIP39 authors Marek Palatinus, Pavol Rusnak, Aaron Voisine, Sean Bowe and word-list contributors. Byte-identical reference copy\: Copyright \(c\) 2013-2016 Pavol Rusnak. Full license and language credits in THIRD\_PARTY\_NOTICES.
- Распространение в репозитории: allowed
- Совместимость с SignPath: compatible
- Доказательства лицензии: [bip39-license](../catalog/evidence/bip39-license.json), [bip39-osi-mit](../catalog/evidence/bip39-osi-mit.json), [bip39-signpath](../catalog/evidence/bip39-signpath.json)
- Тестовые векторы: [bip39-vectors](../catalog/evidence/bip39-vectors.json)

<a id="dictionary-bip39-it"></a>

### BIP39 — Итальянский — bip39-it

- Исходная запись: [bip39-it](../catalog/dictionaries/bip39-it.json)
- Статус: verified
- Причина: Проверенная исследовательская запись; не гарантия релиза или безопасности.
- Диапазон версий (min / max): 3a10b5b5f0a7586df8928d580a3009744ebb2079 / 3a10b5b5f0a7586df8928d580a3009744ebb2079
- Дата проверки: 2026-09-29
- Историческая запись: false
- Доказательства: [bip39-guidance](../catalog/evidence/bip39-guidance.json), [bip39-license](../catalog/evidence/bip39-license.json), [bip39-osi-mit](../catalog/evidence/bip39-osi-mit.json), [bip39-signpath](../catalog/evidence/bip39-signpath.json), [bip39-spec](../catalog/evidence/bip39-spec.json), [bip39-vectors](../catalog/evidence/bip39-vectors.json)
- Подтверждаемое утверждение: BIP39 links exactly ten language lists and language-specific guidance; Japanese generation uses ideographic spaces, which NFKD converts to ASCII spaces. Original source line order and bytes are preserved. Reviewed 2026-09-29; byte SHA-256 363a51bc4748d95541bb156e0439de7b51f28b260433c09874e5891dd3b0f883. See docs/research/batches/bip39-ton.md.
- Подтверждаемое утверждение: Local license review by Codex\: the actual MIT license of the BIP39 reference implementation permits redistribution with copyright and permission notice. Every bundled bitcoin/bips list is byte-identical to src/mnemonic/wordlist at this licensed reference revision; vectors.json is in the same repository. No directory-specific exception was found. Notices preserve the license and attribution. repository\_redistribution=allowed for these exact bytes and public test projections, not arbitrary BIPs material. Reviewed 2026-09-29; byte SHA-256 d5e3c7c62a84e80073201e2f6e5130e9e6804fa05f8ac4f8b26a13c7d3969697. See docs/research/batches/bip39-ton.md.
- Подтверждаемое утверждение: OSI identifies MIT as an approved open-source license; this corroborates the local component assessment, while the pinned reference repository license supplies the actual permission. Reviewed 2026-09-29; byte SHA-256 004c79db0a335488afc87600d89f447dce7fb4d24d510af15ed4381a24be848c. See docs/research/batches/bip39-ton.md.
- Подтверждаемое утверждение: Local component review by Codex\: the exact MIT-licensed lists are source data with no executable dependencies or proprietary restrictions. Together with retained MIT notices and OSI approval this supports signpath\_compatible=compatible for this payload only. SignPath terms require OSS components; this is not Foundation acceptance or project release/signing approval. Reviewed 2026-09-29; byte SHA-256 6610cf889bbe0dc7533abaa310bc7a5cc9a61ae6c2ce0798a08109c925b46c51. See docs/research/batches/bip39-ton.md.
- Подтверждаемое утверждение: Bitcoin BIP39 specifies 2048 indexed words, 12/15/18/21/24 lengths and UTF-8 NFKD for words, sentence and optional passphrase; equal vocabulary does not establish TON derivation. Reviewed 2026-09-29; byte SHA-256 afcbcbed36fe9eb734bd607398a8c124683ded2a75c3830e1b16c47b043a9134. See docs/research/batches/bip39-ton.md.
- Подтверждаемое утверждение: Trezor's public vectors.json supplies 24 independent entropy/mnemonic/seed known answers per language for all ten lists, with passphrase TREZOR. Offline test reconstructs words from entropy, checks published normalized sentence fingerprints and PBKDF2 seed. Public, non-funded data only; fixture projection contains no user phrase. Reviewed 2026-09-29; byte SHA-256 fa3b937b7cff9c9b8ecd3aa011faeb8d6dd67993174b72326e83f4de8fdb30f8. See docs/research/batches/bip39-ton.md.
- Язык: it
- Письменность: Latn
- Кодировка: UTF-8
- Нормализация: NFKD
- Количество слов: 2048
- SHA-256: d392c49fdb700a24cd1fceb237c1f65dcc128f6b34a8aacb58b59384b5c648c2
- Порядок слов: Exact upstream source line order; zero-based 11-bit indices 0 through 2047. UTF-8 LF bytes and final newline preserved without transformation.
- Позиционные правила: The same dictionary is eligible at every word position. Phrase checksum or seed validity is never evaluated by Tessaveil.
- Ревизия источника: 3a10b5b5f0a7586df8928d580a3009744ebb2079
- Лицензия: MIT
- Атрибуция: BIP39 authors Marek Palatinus, Pavol Rusnak, Aaron Voisine, Sean Bowe and word-list contributors. Byte-identical reference copy\: Copyright \(c\) 2013-2016 Pavol Rusnak. Full license and language credits in THIRD\_PARTY\_NOTICES.
- Распространение в репозитории: allowed
- Совместимость с SignPath: compatible
- Доказательства лицензии: [bip39-license](../catalog/evidence/bip39-license.json), [bip39-osi-mit](../catalog/evidence/bip39-osi-mit.json), [bip39-signpath](../catalog/evidence/bip39-signpath.json)
- Тестовые векторы: [bip39-vectors](../catalog/evidence/bip39-vectors.json)

<a id="dictionary-bip39-ja"></a>

### BIP39 — Японский — bip39-ja

- Исходная запись: [bip39-ja](../catalog/dictionaries/bip39-ja.json)
- Статус: verified
- Причина: Проверенная исследовательская запись; не гарантия релиза или безопасности.
- Диапазон версий (min / max): 3a10b5b5f0a7586df8928d580a3009744ebb2079 / 3a10b5b5f0a7586df8928d580a3009744ebb2079
- Дата проверки: 2026-09-29
- Историческая запись: false
- Доказательства: [bip39-guidance](../catalog/evidence/bip39-guidance.json), [bip39-license](../catalog/evidence/bip39-license.json), [bip39-osi-mit](../catalog/evidence/bip39-osi-mit.json), [bip39-signpath](../catalog/evidence/bip39-signpath.json), [bip39-spec](../catalog/evidence/bip39-spec.json), [bip39-vectors](../catalog/evidence/bip39-vectors.json)
- Подтверждаемое утверждение: BIP39 links exactly ten language lists and language-specific guidance; Japanese generation uses ideographic spaces, which NFKD converts to ASCII spaces. Original source line order and bytes are preserved. Reviewed 2026-09-29; byte SHA-256 363a51bc4748d95541bb156e0439de7b51f28b260433c09874e5891dd3b0f883. See docs/research/batches/bip39-ton.md.
- Подтверждаемое утверждение: Local license review by Codex\: the actual MIT license of the BIP39 reference implementation permits redistribution with copyright and permission notice. Every bundled bitcoin/bips list is byte-identical to src/mnemonic/wordlist at this licensed reference revision; vectors.json is in the same repository. No directory-specific exception was found. Notices preserve the license and attribution. repository\_redistribution=allowed for these exact bytes and public test projections, not arbitrary BIPs material. Reviewed 2026-09-29; byte SHA-256 d5e3c7c62a84e80073201e2f6e5130e9e6804fa05f8ac4f8b26a13c7d3969697. See docs/research/batches/bip39-ton.md.
- Подтверждаемое утверждение: OSI identifies MIT as an approved open-source license; this corroborates the local component assessment, while the pinned reference repository license supplies the actual permission. Reviewed 2026-09-29; byte SHA-256 004c79db0a335488afc87600d89f447dce7fb4d24d510af15ed4381a24be848c. See docs/research/batches/bip39-ton.md.
- Подтверждаемое утверждение: Local component review by Codex\: the exact MIT-licensed lists are source data with no executable dependencies or proprietary restrictions. Together with retained MIT notices and OSI approval this supports signpath\_compatible=compatible for this payload only. SignPath terms require OSS components; this is not Foundation acceptance or project release/signing approval. Reviewed 2026-09-29; byte SHA-256 6610cf889bbe0dc7533abaa310bc7a5cc9a61ae6c2ce0798a08109c925b46c51. See docs/research/batches/bip39-ton.md.
- Подтверждаемое утверждение: Bitcoin BIP39 specifies 2048 indexed words, 12/15/18/21/24 lengths and UTF-8 NFKD for words, sentence and optional passphrase; equal vocabulary does not establish TON derivation. Reviewed 2026-09-29; byte SHA-256 afcbcbed36fe9eb734bd607398a8c124683ded2a75c3830e1b16c47b043a9134. See docs/research/batches/bip39-ton.md.
- Подтверждаемое утверждение: Trezor's public vectors.json supplies 24 independent entropy/mnemonic/seed known answers per language for all ten lists, with passphrase TREZOR. Offline test reconstructs words from entropy, checks published normalized sentence fingerprints and PBKDF2 seed. Public, non-funded data only; fixture projection contains no user phrase. Reviewed 2026-09-29; byte SHA-256 fa3b937b7cff9c9b8ecd3aa011faeb8d6dd67993174b72326e83f4de8fdb30f8. See docs/research/batches/bip39-ton.md.
- Язык: ja
- Письменность: Jpan
- Кодировка: UTF-8
- Нормализация: NFKD
- Количество слов: 2048
- SHA-256: 2eed0aef492291e061633d7ad8117f1a2b03eb80a29d0e4e3117ac2528d05ffd
- Порядок слов: Exact upstream source line order; zero-based 11-bit indices 0 through 2047. UTF-8 LF bytes and final newline preserved without transformation.
- Позиционные правила: The same dictionary is eligible at every word position. Phrase checksum or seed validity is never evaluated by Tessaveil.
- Ревизия источника: 3a10b5b5f0a7586df8928d580a3009744ebb2079
- Лицензия: MIT
- Атрибуция: BIP39 authors Marek Palatinus, Pavol Rusnak, Aaron Voisine, Sean Bowe and word-list contributors. Byte-identical reference copy\: Copyright \(c\) 2013-2016 Pavol Rusnak. Full license and language credits in THIRD\_PARTY\_NOTICES.
- Распространение в репозитории: allowed
- Совместимость с SignPath: compatible
- Доказательства лицензии: [bip39-license](../catalog/evidence/bip39-license.json), [bip39-osi-mit](../catalog/evidence/bip39-osi-mit.json), [bip39-signpath](../catalog/evidence/bip39-signpath.json)
- Тестовые векторы: [bip39-vectors](../catalog/evidence/bip39-vectors.json)

<a id="dictionary-bip39-ko"></a>

### BIP39 — Корейский — bip39-ko

- Исходная запись: [bip39-ko](../catalog/dictionaries/bip39-ko.json)
- Статус: verified
- Причина: Проверенная исследовательская запись; не гарантия релиза или безопасности.
- Диапазон версий (min / max): 3a10b5b5f0a7586df8928d580a3009744ebb2079 / 3a10b5b5f0a7586df8928d580a3009744ebb2079
- Дата проверки: 2026-09-29
- Историческая запись: false
- Доказательства: [bip39-guidance](../catalog/evidence/bip39-guidance.json), [bip39-license](../catalog/evidence/bip39-license.json), [bip39-osi-mit](../catalog/evidence/bip39-osi-mit.json), [bip39-signpath](../catalog/evidence/bip39-signpath.json), [bip39-spec](../catalog/evidence/bip39-spec.json), [bip39-vectors](../catalog/evidence/bip39-vectors.json)
- Подтверждаемое утверждение: BIP39 links exactly ten language lists and language-specific guidance; Japanese generation uses ideographic spaces, which NFKD converts to ASCII spaces. Original source line order and bytes are preserved. Reviewed 2026-09-29; byte SHA-256 363a51bc4748d95541bb156e0439de7b51f28b260433c09874e5891dd3b0f883. See docs/research/batches/bip39-ton.md.
- Подтверждаемое утверждение: Local license review by Codex\: the actual MIT license of the BIP39 reference implementation permits redistribution with copyright and permission notice. Every bundled bitcoin/bips list is byte-identical to src/mnemonic/wordlist at this licensed reference revision; vectors.json is in the same repository. No directory-specific exception was found. Notices preserve the license and attribution. repository\_redistribution=allowed for these exact bytes and public test projections, not arbitrary BIPs material. Reviewed 2026-09-29; byte SHA-256 d5e3c7c62a84e80073201e2f6e5130e9e6804fa05f8ac4f8b26a13c7d3969697. See docs/research/batches/bip39-ton.md.
- Подтверждаемое утверждение: OSI identifies MIT as an approved open-source license; this corroborates the local component assessment, while the pinned reference repository license supplies the actual permission. Reviewed 2026-09-29; byte SHA-256 004c79db0a335488afc87600d89f447dce7fb4d24d510af15ed4381a24be848c. See docs/research/batches/bip39-ton.md.
- Подтверждаемое утверждение: Local component review by Codex\: the exact MIT-licensed lists are source data with no executable dependencies or proprietary restrictions. Together with retained MIT notices and OSI approval this supports signpath\_compatible=compatible for this payload only. SignPath terms require OSS components; this is not Foundation acceptance or project release/signing approval. Reviewed 2026-09-29; byte SHA-256 6610cf889bbe0dc7533abaa310bc7a5cc9a61ae6c2ce0798a08109c925b46c51. See docs/research/batches/bip39-ton.md.
- Подтверждаемое утверждение: Bitcoin BIP39 specifies 2048 indexed words, 12/15/18/21/24 lengths and UTF-8 NFKD for words, sentence and optional passphrase; equal vocabulary does not establish TON derivation. Reviewed 2026-09-29; byte SHA-256 afcbcbed36fe9eb734bd607398a8c124683ded2a75c3830e1b16c47b043a9134. See docs/research/batches/bip39-ton.md.
- Подтверждаемое утверждение: Trezor's public vectors.json supplies 24 independent entropy/mnemonic/seed known answers per language for all ten lists, with passphrase TREZOR. Offline test reconstructs words from entropy, checks published normalized sentence fingerprints and PBKDF2 seed. Public, non-funded data only; fixture projection contains no user phrase. Reviewed 2026-09-29; byte SHA-256 fa3b937b7cff9c9b8ecd3aa011faeb8d6dd67993174b72326e83f4de8fdb30f8. See docs/research/batches/bip39-ton.md.
- Язык: ko
- Письменность: Hang
- Кодировка: UTF-8
- Нормализация: NFKD
- Количество слов: 2048
- SHA-256: 9e95f86c167de88f450f0aaf89e87f6624a57f973c67b516e338e8e8b8897f60
- Порядок слов: Exact upstream source line order; zero-based 11-bit indices 0 through 2047. UTF-8 LF bytes and final newline preserved without transformation.
- Позиционные правила: The same dictionary is eligible at every word position. Phrase checksum or seed validity is never evaluated by Tessaveil.
- Ревизия источника: 3a10b5b5f0a7586df8928d580a3009744ebb2079
- Лицензия: MIT
- Атрибуция: BIP39 authors Marek Palatinus, Pavol Rusnak, Aaron Voisine, Sean Bowe and word-list contributors. Byte-identical reference copy\: Copyright \(c\) 2013-2016 Pavol Rusnak. Full license and language credits in THIRD\_PARTY\_NOTICES.
- Распространение в репозитории: allowed
- Совместимость с SignPath: compatible
- Доказательства лицензии: [bip39-license](../catalog/evidence/bip39-license.json), [bip39-osi-mit](../catalog/evidence/bip39-osi-mit.json), [bip39-signpath](../catalog/evidence/bip39-signpath.json)
- Тестовые векторы: [bip39-vectors](../catalog/evidence/bip39-vectors.json)

<a id="dictionary-bip39-pt"></a>

### BIP39 — Португальский — bip39-pt

- Исходная запись: [bip39-pt](../catalog/dictionaries/bip39-pt.json)
- Статус: verified
- Причина: Проверенная исследовательская запись; не гарантия релиза или безопасности.
- Диапазон версий (min / max): 3a10b5b5f0a7586df8928d580a3009744ebb2079 / 3a10b5b5f0a7586df8928d580a3009744ebb2079
- Дата проверки: 2026-09-29
- Историческая запись: false
- Доказательства: [bip39-guidance](../catalog/evidence/bip39-guidance.json), [bip39-license](../catalog/evidence/bip39-license.json), [bip39-osi-mit](../catalog/evidence/bip39-osi-mit.json), [bip39-signpath](../catalog/evidence/bip39-signpath.json), [bip39-spec](../catalog/evidence/bip39-spec.json), [bip39-vectors](../catalog/evidence/bip39-vectors.json)
- Подтверждаемое утверждение: BIP39 links exactly ten language lists and language-specific guidance; Japanese generation uses ideographic spaces, which NFKD converts to ASCII spaces. Original source line order and bytes are preserved. Reviewed 2026-09-29; byte SHA-256 363a51bc4748d95541bb156e0439de7b51f28b260433c09874e5891dd3b0f883. See docs/research/batches/bip39-ton.md.
- Подтверждаемое утверждение: Local license review by Codex\: the actual MIT license of the BIP39 reference implementation permits redistribution with copyright and permission notice. Every bundled bitcoin/bips list is byte-identical to src/mnemonic/wordlist at this licensed reference revision; vectors.json is in the same repository. No directory-specific exception was found. Notices preserve the license and attribution. repository\_redistribution=allowed for these exact bytes and public test projections, not arbitrary BIPs material. Reviewed 2026-09-29; byte SHA-256 d5e3c7c62a84e80073201e2f6e5130e9e6804fa05f8ac4f8b26a13c7d3969697. See docs/research/batches/bip39-ton.md.
- Подтверждаемое утверждение: OSI identifies MIT as an approved open-source license; this corroborates the local component assessment, while the pinned reference repository license supplies the actual permission. Reviewed 2026-09-29; byte SHA-256 004c79db0a335488afc87600d89f447dce7fb4d24d510af15ed4381a24be848c. See docs/research/batches/bip39-ton.md.
- Подтверждаемое утверждение: Local component review by Codex\: the exact MIT-licensed lists are source data with no executable dependencies or proprietary restrictions. Together with retained MIT notices and OSI approval this supports signpath\_compatible=compatible for this payload only. SignPath terms require OSS components; this is not Foundation acceptance or project release/signing approval. Reviewed 2026-09-29; byte SHA-256 6610cf889bbe0dc7533abaa310bc7a5cc9a61ae6c2ce0798a08109c925b46c51. See docs/research/batches/bip39-ton.md.
- Подтверждаемое утверждение: Bitcoin BIP39 specifies 2048 indexed words, 12/15/18/21/24 lengths and UTF-8 NFKD for words, sentence and optional passphrase; equal vocabulary does not establish TON derivation. Reviewed 2026-09-29; byte SHA-256 afcbcbed36fe9eb734bd607398a8c124683ded2a75c3830e1b16c47b043a9134. See docs/research/batches/bip39-ton.md.
- Подтверждаемое утверждение: Trezor's public vectors.json supplies 24 independent entropy/mnemonic/seed known answers per language for all ten lists, with passphrase TREZOR. Offline test reconstructs words from entropy, checks published normalized sentence fingerprints and PBKDF2 seed. Public, non-funded data only; fixture projection contains no user phrase. Reviewed 2026-09-29; byte SHA-256 fa3b937b7cff9c9b8ecd3aa011faeb8d6dd67993174b72326e83f4de8fdb30f8. See docs/research/batches/bip39-ton.md.
- Язык: pt
- Письменность: Latn
- Кодировка: UTF-8
- Нормализация: NFKD
- Количество слов: 2048
- SHA-256: 2685e9c194c82ae67e10ba59d9ea5345a23dc093e92276fc5361f6667d79cd3f
- Порядок слов: Exact upstream source line order; zero-based 11-bit indices 0 through 2047. UTF-8 LF bytes and final newline preserved without transformation.
- Позиционные правила: The same dictionary is eligible at every word position. Phrase checksum or seed validity is never evaluated by Tessaveil.
- Ревизия источника: 3a10b5b5f0a7586df8928d580a3009744ebb2079
- Лицензия: MIT
- Атрибуция: BIP39 authors Marek Palatinus, Pavol Rusnak, Aaron Voisine, Sean Bowe and word-list contributors. Byte-identical reference copy\: Copyright \(c\) 2013-2016 Pavol Rusnak. Full license and language credits in THIRD\_PARTY\_NOTICES.
- Распространение в репозитории: allowed
- Совместимость с SignPath: compatible
- Доказательства лицензии: [bip39-license](../catalog/evidence/bip39-license.json), [bip39-osi-mit](../catalog/evidence/bip39-osi-mit.json), [bip39-signpath](../catalog/evidence/bip39-signpath.json)
- Тестовые векторы: [bip39-vectors](../catalog/evidence/bip39-vectors.json)

<a id="dictionary-bip39-zh-hans"></a>

### BIP39 — Китайский упрощённый — bip39-zh-hans

- Исходная запись: [bip39-zh-hans](../catalog/dictionaries/bip39-zh-hans.json)
- Статус: verified
- Причина: Проверенная исследовательская запись; не гарантия релиза или безопасности.
- Диапазон версий (min / max): 3a10b5b5f0a7586df8928d580a3009744ebb2079 / 3a10b5b5f0a7586df8928d580a3009744ebb2079
- Дата проверки: 2026-09-29
- Историческая запись: false
- Доказательства: [bip39-guidance](../catalog/evidence/bip39-guidance.json), [bip39-license](../catalog/evidence/bip39-license.json), [bip39-osi-mit](../catalog/evidence/bip39-osi-mit.json), [bip39-signpath](../catalog/evidence/bip39-signpath.json), [bip39-spec](../catalog/evidence/bip39-spec.json), [bip39-vectors](../catalog/evidence/bip39-vectors.json)
- Подтверждаемое утверждение: BIP39 links exactly ten language lists and language-specific guidance; Japanese generation uses ideographic spaces, which NFKD converts to ASCII spaces. Original source line order and bytes are preserved. Reviewed 2026-09-29; byte SHA-256 363a51bc4748d95541bb156e0439de7b51f28b260433c09874e5891dd3b0f883. See docs/research/batches/bip39-ton.md.
- Подтверждаемое утверждение: Local license review by Codex\: the actual MIT license of the BIP39 reference implementation permits redistribution with copyright and permission notice. Every bundled bitcoin/bips list is byte-identical to src/mnemonic/wordlist at this licensed reference revision; vectors.json is in the same repository. No directory-specific exception was found. Notices preserve the license and attribution. repository\_redistribution=allowed for these exact bytes and public test projections, not arbitrary BIPs material. Reviewed 2026-09-29; byte SHA-256 d5e3c7c62a84e80073201e2f6e5130e9e6804fa05f8ac4f8b26a13c7d3969697. See docs/research/batches/bip39-ton.md.
- Подтверждаемое утверждение: OSI identifies MIT as an approved open-source license; this corroborates the local component assessment, while the pinned reference repository license supplies the actual permission. Reviewed 2026-09-29; byte SHA-256 004c79db0a335488afc87600d89f447dce7fb4d24d510af15ed4381a24be848c. See docs/research/batches/bip39-ton.md.
- Подтверждаемое утверждение: Local component review by Codex\: the exact MIT-licensed lists are source data with no executable dependencies or proprietary restrictions. Together with retained MIT notices and OSI approval this supports signpath\_compatible=compatible for this payload only. SignPath terms require OSS components; this is not Foundation acceptance or project release/signing approval. Reviewed 2026-09-29; byte SHA-256 6610cf889bbe0dc7533abaa310bc7a5cc9a61ae6c2ce0798a08109c925b46c51. See docs/research/batches/bip39-ton.md.
- Подтверждаемое утверждение: Bitcoin BIP39 specifies 2048 indexed words, 12/15/18/21/24 lengths and UTF-8 NFKD for words, sentence and optional passphrase; equal vocabulary does not establish TON derivation. Reviewed 2026-09-29; byte SHA-256 afcbcbed36fe9eb734bd607398a8c124683ded2a75c3830e1b16c47b043a9134. See docs/research/batches/bip39-ton.md.
- Подтверждаемое утверждение: Trezor's public vectors.json supplies 24 independent entropy/mnemonic/seed known answers per language for all ten lists, with passphrase TREZOR. Offline test reconstructs words from entropy, checks published normalized sentence fingerprints and PBKDF2 seed. Public, non-funded data only; fixture projection contains no user phrase. Reviewed 2026-09-29; byte SHA-256 fa3b937b7cff9c9b8ecd3aa011faeb8d6dd67993174b72326e83f4de8fdb30f8. See docs/research/batches/bip39-ton.md.
- Язык: zh-hans
- Письменность: Hans
- Кодировка: UTF-8
- Нормализация: NFKD
- Количество слов: 2048
- SHA-256: 5c5942792bd8340cb8b27cd592f1015edf56a8c5b26276ee18a482428e7c5726
- Порядок слов: Exact upstream source line order; zero-based 11-bit indices 0 through 2047. UTF-8 LF bytes and final newline preserved without transformation.
- Позиционные правила: The same dictionary is eligible at every word position. Phrase checksum or seed validity is never evaluated by Tessaveil.
- Ревизия источника: 3a10b5b5f0a7586df8928d580a3009744ebb2079
- Лицензия: MIT
- Атрибуция: BIP39 authors Marek Palatinus, Pavol Rusnak, Aaron Voisine, Sean Bowe and word-list contributors. Byte-identical reference copy\: Copyright \(c\) 2013-2016 Pavol Rusnak. Full license and language credits in THIRD\_PARTY\_NOTICES.
- Распространение в репозитории: allowed
- Совместимость с SignPath: compatible
- Доказательства лицензии: [bip39-license](../catalog/evidence/bip39-license.json), [bip39-osi-mit](../catalog/evidence/bip39-osi-mit.json), [bip39-signpath](../catalog/evidence/bip39-signpath.json)
- Тестовые векторы: [bip39-vectors](../catalog/evidence/bip39-vectors.json)

<a id="dictionary-bip39-zh-hant"></a>

### BIP39 — Китайский традиционный — bip39-zh-hant

- Исходная запись: [bip39-zh-hant](../catalog/dictionaries/bip39-zh-hant.json)
- Статус: verified
- Причина: Проверенная исследовательская запись; не гарантия релиза или безопасности.
- Диапазон версий (min / max): 3a10b5b5f0a7586df8928d580a3009744ebb2079 / 3a10b5b5f0a7586df8928d580a3009744ebb2079
- Дата проверки: 2026-09-29
- Историческая запись: false
- Доказательства: [bip39-guidance](../catalog/evidence/bip39-guidance.json), [bip39-license](../catalog/evidence/bip39-license.json), [bip39-osi-mit](../catalog/evidence/bip39-osi-mit.json), [bip39-signpath](../catalog/evidence/bip39-signpath.json), [bip39-spec](../catalog/evidence/bip39-spec.json), [bip39-vectors](../catalog/evidence/bip39-vectors.json)
- Подтверждаемое утверждение: BIP39 links exactly ten language lists and language-specific guidance; Japanese generation uses ideographic spaces, which NFKD converts to ASCII spaces. Original source line order and bytes are preserved. Reviewed 2026-09-29; byte SHA-256 363a51bc4748d95541bb156e0439de7b51f28b260433c09874e5891dd3b0f883. See docs/research/batches/bip39-ton.md.
- Подтверждаемое утверждение: Local license review by Codex\: the actual MIT license of the BIP39 reference implementation permits redistribution with copyright and permission notice. Every bundled bitcoin/bips list is byte-identical to src/mnemonic/wordlist at this licensed reference revision; vectors.json is in the same repository. No directory-specific exception was found. Notices preserve the license and attribution. repository\_redistribution=allowed for these exact bytes and public test projections, not arbitrary BIPs material. Reviewed 2026-09-29; byte SHA-256 d5e3c7c62a84e80073201e2f6e5130e9e6804fa05f8ac4f8b26a13c7d3969697. See docs/research/batches/bip39-ton.md.
- Подтверждаемое утверждение: OSI identifies MIT as an approved open-source license; this corroborates the local component assessment, while the pinned reference repository license supplies the actual permission. Reviewed 2026-09-29; byte SHA-256 004c79db0a335488afc87600d89f447dce7fb4d24d510af15ed4381a24be848c. See docs/research/batches/bip39-ton.md.
- Подтверждаемое утверждение: Local component review by Codex\: the exact MIT-licensed lists are source data with no executable dependencies or proprietary restrictions. Together with retained MIT notices and OSI approval this supports signpath\_compatible=compatible for this payload only. SignPath terms require OSS components; this is not Foundation acceptance or project release/signing approval. Reviewed 2026-09-29; byte SHA-256 6610cf889bbe0dc7533abaa310bc7a5cc9a61ae6c2ce0798a08109c925b46c51. See docs/research/batches/bip39-ton.md.
- Подтверждаемое утверждение: Bitcoin BIP39 specifies 2048 indexed words, 12/15/18/21/24 lengths and UTF-8 NFKD for words, sentence and optional passphrase; equal vocabulary does not establish TON derivation. Reviewed 2026-09-29; byte SHA-256 afcbcbed36fe9eb734bd607398a8c124683ded2a75c3830e1b16c47b043a9134. See docs/research/batches/bip39-ton.md.
- Подтверждаемое утверждение: Trezor's public vectors.json supplies 24 independent entropy/mnemonic/seed known answers per language for all ten lists, with passphrase TREZOR. Offline test reconstructs words from entropy, checks published normalized sentence fingerprints and PBKDF2 seed. Public, non-funded data only; fixture projection contains no user phrase. Reviewed 2026-09-29; byte SHA-256 fa3b937b7cff9c9b8ecd3aa011faeb8d6dd67993174b72326e83f4de8fdb30f8. See docs/research/batches/bip39-ton.md.
- Язык: zh-hant
- Письменность: Hant
- Кодировка: UTF-8
- Нормализация: NFKD
- Количество слов: 2048
- SHA-256: 417b26b3d8500a4ae3d59717d7011952db6fc2fb84b807f3f94ac734e89c1b5f
- Порядок слов: Exact upstream source line order; zero-based 11-bit indices 0 through 2047. UTF-8 LF bytes and final newline preserved without transformation.
- Позиционные правила: The same dictionary is eligible at every word position. Phrase checksum or seed validity is never evaluated by Tessaveil.
- Ревизия источника: 3a10b5b5f0a7586df8928d580a3009744ebb2079
- Лицензия: MIT
- Атрибуция: BIP39 authors Marek Palatinus, Pavol Rusnak, Aaron Voisine, Sean Bowe and word-list contributors. Byte-identical reference copy\: Copyright \(c\) 2013-2016 Pavol Rusnak. Full license and language credits in THIRD\_PARTY\_NOTICES.
- Распространение в репозитории: allowed
- Совместимость с SignPath: compatible
- Доказательства лицензии: [bip39-license](../catalog/evidence/bip39-license.json), [bip39-osi-mit](../catalog/evidence/bip39-osi-mit.json), [bip39-signpath](../catalog/evidence/bip39-signpath.json)
- Тестовые векторы: [bip39-vectors](../catalog/evidence/bip39-vectors.json)

## Ревизии доказательств

- [bip39-guidance](../catalog/evidence/bip39-guidance.json): official-specification; 3a10b5b5f0a7586df8928d580a3009744ebb2079; 2026-09-29
- [bip39-license](../catalog/evidence/bip39-license.json): official-source; b57a5ad77a981e743f4167ab2f7927a55c1e82a8; 2026-09-29
- [bip39-osi-mit](../catalog/evidence/bip39-osi-mit.json): official-documentation; sha256\:004c79db0a335488afc87600d89f447dce7fb4d24d510af15ed4381a24be848c; 2026-09-29
- [bip39-signpath](../catalog/evidence/bip39-signpath.json): official-documentation; sha256\:6610cf889bbe0dc7533abaa310bc7a5cc9a61ae6c2ce0798a08109c925b46c51; 2026-09-29
- [bip39-spec](../catalog/evidence/bip39-spec.json): official-specification; 3a10b5b5f0a7586df8928d580a3009744ebb2079; 2026-09-29
- [bip39-vectors](../catalog/evidence/bip39-vectors.json): public-test-vector; b57a5ad77a981e743f4167ab2f7927a55c1e82a8; 2026-09-29
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

## Охват обязательного исследования

Pending означает незавершённое исследование, а не статус поддержки. Отсутствующие записи остаются видимыми. Полные URL источников находятся в исходных записях.

### [windows-v1](../catalog/required/windows-v1.json)

| Требование | Состояние исследования | Статус | Записи |
| --- | --- | --- | --- |
| dictionary-bip39-cs — BIP39 — Чешский | terminal | verified | [bip39-cs](../catalog/dictionaries/bip39-cs.json) |
| dictionary-bip39-en — BIP39 — Английский | terminal | verified | [bip39-en](../catalog/dictionaries/bip39-en.json) |
| dictionary-bip39-es — BIP39 — Испанский | terminal | verified | [bip39-es](../catalog/dictionaries/bip39-es.json) |
| dictionary-bip39-fr — BIP39 — Французский | terminal | verified | [bip39-fr](../catalog/dictionaries/bip39-fr.json) |
| dictionary-bip39-it — BIP39 — Итальянский | terminal | verified | [bip39-it](../catalog/dictionaries/bip39-it.json) |
| dictionary-bip39-ja — BIP39 — Японский | terminal | verified | [bip39-ja](../catalog/dictionaries/bip39-ja.json) |
| dictionary-bip39-ko — BIP39 — Корейский | terminal | verified | [bip39-ko](../catalog/dictionaries/bip39-ko.json) |
| dictionary-bip39-pt — BIP39 — Португальский | terminal | verified | [bip39-pt](../catalog/dictionaries/bip39-pt.json) |
| dictionary-bip39-zh-hans — BIP39 — Китайский упрощённый | terminal | verified | [bip39-zh-hans](../catalog/dictionaries/bip39-zh-hans.json) |
| dictionary-bip39-zh-hant — BIP39 — Китайский традиционный | terminal | verified | [bip39-zh-hant](../catalog/dictionaries/bip39-zh-hant.json) |
| dictionary-electrum-v1-en — electrum v1 en | pending | — | — |
| dictionary-monero-de — MONERO — Немецкий | pending | — | — |
| dictionary-monero-en — MONERO — Английский | pending | — | — |
| dictionary-monero-en-old — MONERO — Старый английский | pending | — | — |
| dictionary-monero-eo — MONERO — Эсперанто | pending | — | — |
| dictionary-monero-es — MONERO — Испанский | pending | — | — |
| dictionary-monero-fr — MONERO — Французский | pending | — | — |
| dictionary-monero-it — MONERO — Итальянский | pending | — | — |
| dictionary-monero-ja — MONERO — Японский | pending | — | — |
| dictionary-monero-jbo — MONERO — Ложбан | pending | — | — |
| dictionary-monero-nl — MONERO — Нидерландский | pending | — | — |
| dictionary-monero-pt — MONERO — Португальский | pending | — | — |
| dictionary-monero-ru — MONERO — Русский | pending | — | — |
| dictionary-monero-zh-hans — MONERO — Китайский упрощённый | pending | — | — |
| dictionary-pgp-even — pgp even | pending | — | — |
| dictionary-pgp-odd — pgp odd | pending | — | — |
| dictionary-polyseed-cs — POLYSEED — Чешский | pending | — | — |
| dictionary-polyseed-en — POLYSEED — Английский | pending | — | — |
| dictionary-polyseed-es — POLYSEED — Испанский | pending | — | — |
| dictionary-polyseed-fr — POLYSEED — Французский | pending | — | — |
| dictionary-polyseed-it — POLYSEED — Итальянский | pending | — | — |
| dictionary-polyseed-ja — POLYSEED — Японский | pending | — | — |
| dictionary-polyseed-ko — POLYSEED — Корейский | pending | — | — |
| dictionary-polyseed-pt — POLYSEED — Португальский | pending | — | — |
| dictionary-polyseed-zh-hans — POLYSEED — Китайский упрощённый | pending | — | — |
| dictionary-polyseed-zh-hant — POLYSEED — Китайский традиционный | pending | — | — |
| dictionary-sia-legacy — sia legacy | pending | — | — |
| dictionary-slip39-en — slip39 en | pending | — | — |
| dictionary-zano-en — zano en | pending | — | — |
| network-algorand — algorand | pending | — | — |
| network-arbitrum — arbitrum | pending | — | — |
| network-avalanche — avalanche | pending | — | — |
| network-base — base | pending | — | — |
| network-bitcoin — bitcoin | pending | — | — |
| network-bnb-chain — bnb chain | pending | — | — |
| network-cardano — cardano | pending | — | — |
| network-chia — chia | pending | — | — |
| network-cosmos — cosmos | pending | — | — |
| network-decred — decred | pending | — | — |
| network-ethereum — ethereum | pending | — | — |
| network-kusama — kusama | pending | — | — |
| network-monero — monero | pending | — | — |
| network-polkadot — polkadot | pending | — | — |
| network-polygon — polygon | pending | — | — |
| network-sia — sia | pending | — | — |
| network-solana — solana | pending | — | — |
| network-tezos — tezos | pending | — | — |
| network-ton — ton | pending | — | — |
| network-tron — tron | pending | — | — |
| network-zano — zano | pending | — | — |
| network-zcash — zcash | pending | — | — |
| scheme-algorand-25 — algorand 25 | pending | — | — |
| scheme-bip39 — bip39 | terminal | verified | [bip39](../catalog/schemes/bip39.json) |
| scheme-cake-decred-15 — cake decred 15 | pending | — | — |
| scheme-cardano-byron — cardano byron | pending | — | — |
| scheme-cardano-daedalus-27 — cardano daedalus 27 | pending | — | — |
| scheme-cardano-hardware — cardano hardware | pending | — | — |
| scheme-cardano-icarus — cardano icarus | pending | — | — |
| scheme-chia-bip39 — chia bip39 | pending | — | — |
| scheme-decred-bip39 — decred bip39 | pending | — | — |
| scheme-decred-pgp33 — decred pgp33 | pending | — | — |
| scheme-electrum-v1 — electrum v1 | pending | — | — |
| scheme-electrum-v2 — electrum v2 | pending | — | — |
| scheme-monero-legacy — monero legacy | pending | — | — |
| scheme-mymonero — mymonero | pending | — | — |
| scheme-polyseed — polyseed | pending | — | — |
| scheme-sia-bip39 — sia bip39 | pending | — | — |
| scheme-sia-legacy-28 — sia legacy 28 | pending | — | — |
| scheme-sia-legacy-29 — sia legacy 29 | pending | — | — |
| scheme-slip39-share — slip39 share | pending | — | — |
| scheme-substrate-bip39 — substrate bip39 | pending | — | — |
| scheme-ton-multichain-bip39 — ton multichain bip39 | terminal | documented | [ton-multichain-bip39](../catalog/schemes/ton-multichain-bip39.json) |
| scheme-ton-native — ton native | terminal | verified | [ton-native](../catalog/schemes/ton-native.json) |
| scheme-zano-legacy-24 — zano legacy 24 | pending | — | — |
| scheme-zano-legacy-25 — zano legacy 25 | pending | — | — |
| scheme-zano-modern — zano modern | pending | — | — |
| scheme-zcash-bip39 — zcash bip39 | pending | — | — |
| scheme-zcash-non-mnemonic — zcash non mnemonic | pending | — | — |
| wallet-atomic-wallet — atomic wallet | pending | — | — |
| wallet-backpack — backpack | pending | — | — |
| wallet-bitbox02 — bitbox02 | pending | — | — |
| wallet-bitget-wallet — bitget wallet | pending | — | — |
| wallet-blockstream-jade — blockstream jade | pending | — | — |
| wallet-bluewallet — bluewallet | pending | — | — |
| wallet-cake-wallet — cake wallet | pending | — | — |
| wallet-cake-wallet-decred — cake wallet decred | pending | — | — |
| wallet-cake-wallet-zano — cake wallet zano | pending | — | — |
| wallet-chia-wallet — chia wallet | pending | — | — |
| wallet-coinbase-wallet — coinbase wallet | pending | — | — |
| wallet-coinomi — coinomi | pending | — | — |
| wallet-coldcard — coldcard | pending | — | — |
| wallet-cosmostation — cosmostation | pending | — | — |
| wallet-daedalus — daedalus | pending | — | — |
| wallet-decrediton — decrediton | pending | — | — |
| wallet-defly — defly | pending | — | — |
| wallet-electrum — electrum | pending | — | — |
| wallet-ellipal — ellipal | pending | — | — |
| wallet-eternl — eternl | pending | — | — |
| wallet-exodus — exodus | pending | — | — |
| wallet-exodus-monero — exodus monero | pending | — | — |
| wallet-feather — feather | pending | — | — |
| wallet-glow — glow | pending | — | — |
| wallet-gram-wallet — gram wallet | terminal | documented | [gram-wallet](../catalog/wallets/gram-wallet.json) |
| wallet-guarda — guarda | pending | — | — |
| wallet-imtoken — imtoken | pending | — | — |
| wallet-keplr — keplr | pending | — | — |
| wallet-keystone — keystone | pending | — | — |
| wallet-kukai — kukai | pending | — | — |
| wallet-lace — lace | pending | — | — |
| wallet-leap — leap | pending | — | — |
| wallet-ledger — ledger | pending | — | — |
| wallet-metamask — metamask | pending | — | — |
| wallet-monero-gui-cli — monero gui cli | pending | — | — |
| wallet-mymonero — mymonero | pending | — | — |
| wallet-mytonwallet — mytonwallet | terminal | documented | [mytonwallet](../catalog/wallets/mytonwallet.json) |
| wallet-nami — nami | pending | — | — |
| wallet-okx-wallet — okx wallet | pending | — | — |
| wallet-onekey — onekey | pending | — | — |
| wallet-openmask — openmask | terminal | documented | [openmask](../catalog/wallets/openmask.json) |
| wallet-passport — passport | pending | — | — |
| wallet-pera-wallet — pera wallet | pending | — | — |
| wallet-phantom — phantom | pending | — | — |
| wallet-polkadot-js — polkadot js | pending | — | — |
| wallet-rabby — rabby | pending | — | — |
| wallet-rainbow — rainbow | pending | — | — |
| wallet-safepal — safepal | pending | — | — |
| wallet-seedsigner — seedsigner | pending | — | — |
| wallet-sia-ui — sia ui | pending | — | — |
| wallet-siad — siad | pending | — | — |
| wallet-solflare — solflare | pending | — | — |
| wallet-sparrow — sparrow | pending | — | — |
| wallet-subwallet — subwallet | pending | — | — |
| wallet-talisman — talisman | pending | — | — |
| wallet-tangem-seed — tangem seed | pending | — | — |
| wallet-temple — temple | pending | — | — |
| wallet-tokenpocket — tokenpocket | pending | — | — |
| wallet-ton-space — ton space | terminal | documented | [ton-space](../catalog/wallets/ton-space.json) |
| wallet-tonhub — tonhub | terminal | verified | [tonhub](../catalog/wallets/tonhub.json) |
| wallet-tonkeeper-classic — tonkeeper classic | terminal | verified | [tonkeeper-classic](../catalog/wallets/tonkeeper-classic.json) |
| wallet-tonkeeper-multichain — tonkeeper multichain | terminal | documented | [tonkeeper-multichain](../catalog/wallets/tonkeeper-multichain.json) |
| wallet-trezor — trezor | pending | — | — |
| wallet-trezor-model-t — trezor model t | pending | — | — |
| wallet-trezor-safe-3 — trezor safe 3 | pending | — | — |
| wallet-trezor-safe-5 — trezor safe 5 | pending | — | — |
| wallet-trezor-safe-7 — trezor safe 7 | pending | — | — |
| wallet-trust-wallet — trust wallet | pending | — | — |
| wallet-typhon — typhon | pending | — | — |
| wallet-walletd — walletd | pending | — | — |
| wallet-yoroi — yoroi | pending | — | — |
| wallet-zallet — zallet | pending | — | — |
| wallet-zano-wallet — zano wallet | pending | — | — |
| wallet-zcash-official — zcash official | pending | — | — |
| wallet-zerion — zerion | pending | — | — |
