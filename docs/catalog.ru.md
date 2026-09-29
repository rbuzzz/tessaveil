# Каталог Tessaveil

> Создано автоматически из catalog/*. Не редактировать; команда: `python -m tools.catalog.cli generate --root .`.

Только исследование. Проверенная запись — лишь кандидат для создания таблиц в будущем. Общий словарь не означает совместимость схем. Ключи не выводятся, целые фразы не проверяются. Внешние секреты не сохраняются.

Готовность релиза: NO-GO; проверка каталога не закрывает требования физических устройств, чистых систем, файловых систем, аудита и релиза.

## Индекс продуктов

| Продукт / профиль | Платформа / режим | Сети | Схема | Статус |
| --- | --- | --- | --- | --- |
| Cake Wallet Monero / [cake-wallet-monero](#wallet-cake-wallet-monero) | android / polyseed-16-generated | monero | [polyseed-16](#scheme-polyseed-16) | documented |
| Cake Wallet Monero / [cake-wallet-monero-bip39](#wallet-cake-wallet-monero-bip39) | android / bip39-monero-generated-unresolved | monero | — | documented |
| Cake Wallet Monero / [cake-wallet-monero-legacy](#wallet-cake-wallet-monero-legacy) | android / legacy-25-generated | monero | [monero-legacy](#scheme-monero-legacy) | documented |
| Exodus / [exodus-monero-export](#wallet-exodus-monero-export) | windows / monero-25-export | monero | [monero-legacy](#scheme-monero-legacy) | documented |
| Feather / [feather](#wallet-feather) | windows / polyseed-16-generated | monero | [polyseed-16](#scheme-polyseed-16) | documented |
| Feather / [feather-legacy-import](#wallet-feather-legacy-import) | windows / legacy-25-import | monero | [monero-legacy](#scheme-monero-legacy) | documented |
| Gram Wallet / [gram-wallet](#wallet-gram-wallet) | android / mnemonic-backup-unresolved | ton | — | documented |
| Monero CLI / [monero-cli-polyseed](#wallet-monero-cli-polyseed) | windows / polyseed-16-generated | monero | [polyseed-16](#scheme-polyseed-16) | documented |
| Monero CLI / [monero-gui-cli](#wallet-monero-gui-cli) | windows / legacy-25-generated | monero | [monero-legacy](#scheme-monero-legacy) | documented |
| Monero GUI / [monero-gui](#wallet-monero-gui) | windows / generated-seed-unresolved | monero | — | documented |
| MyMonero / [mymonero](#wallet-mymonero) | windows / legacy-13-restore | monero | [mymonero-13](#scheme-mymonero-13) | documented |
| MyMonero / [mymonero-generated](#wallet-mymonero-generated) | windows / generated-backup-unresolved | monero | — | documented |
| My Wallet / MyTonWallet / [mytonwallet](#wallet-mytonwallet) | web / bip39-multichain-generated | ton | [ton-multichain-bip39](#scheme-ton-multichain-bip39) | documented |
| My Wallet / MyTonWallet — TON only / [mytonwallet-native](#wallet-mytonwallet-native) | web / ton-native-generated | ton | [ton-native](#scheme-ton-native) | verified |
| OpenMask / [openmask](#wallet-openmask) | web / ton-native-generated | ton | [ton-native](#scheme-ton-native) | documented |
| Tonhub / [tonhub](#wallet-tonhub) | android / ton-native-generated | ton | [ton-native](#scheme-ton-native) | verified |
| Tonkeeper Classic / [tonkeeper-classic](#wallet-tonkeeper-classic) | web / ton-native-generated | ton | [ton-native](#scheme-ton-native) | verified |
| Keeper / Tonkeeper Multichain / [tonkeeper-multichain](#wallet-tonkeeper-multichain) | cross-platform / bip39-multichain-generated | ton | [ton-multichain-bip39](#scheme-ton-multichain-bip39) | documented |
| TON Space / DeFi Account / [ton-space](#wallet-ton-space) | web / manual-mnemonic-backup | ton | — | documented |

## Индекс сетей

- monero: [cake-wallet-monero](#wallet-cake-wallet-monero), [cake-wallet-monero-bip39](#wallet-cake-wallet-monero-bip39), [cake-wallet-monero-legacy](#wallet-cake-wallet-monero-legacy), [exodus-monero-export](#wallet-exodus-monero-export), [feather](#wallet-feather), [feather-legacy-import](#wallet-feather-legacy-import), [monero-cli-polyseed](#wallet-monero-cli-polyseed), [monero-gui](#wallet-monero-gui), [monero-gui-cli](#wallet-monero-gui-cli), [mymonero](#wallet-mymonero), [mymonero-generated](#wallet-mymonero-generated)
- ton: [gram-wallet](#wallet-gram-wallet), [mytonwallet](#wallet-mytonwallet), [mytonwallet-native](#wallet-mytonwallet-native), [openmask](#wallet-openmask), [ton-space](#wallet-ton-space), [tonhub](#wallet-tonhub), [tonkeeper-classic](#wallet-tonkeeper-classic), [tonkeeper-multichain](#wallet-tonkeeper-multichain)

## Профили кошельков

<a id="wallet-cake-wallet-monero"></a>

### Cake Wallet Monero — Polyseed creation — cake-wallet-monero

- Исходная запись: [cake-wallet-monero](../catalog/wallets/cake-wallet-monero.json)
- Статус: documented
- Причина: Доказательств недостаточно для доступной поддержки.
- Рекомендация: Недоступно для выбора; используйте процедуру резервного копирования самого кошелька.
- Диапазон версий (min / max): source-9679f91a8c9f63d00500c2b7cc18daf00949bdef / source-9679f91a8c9f63d00500c2b7cc18daf00949bdef
- Дата проверки: 2026-09-29
- Историческая запись: false
- Доказательства: [monero-cake-export](../catalog/evidence/monero-cake-export.json), [monero-cake-seed](../catalog/evidence/monero-cake-seed.json), [monero-cake-ui](../catalog/evidence/monero-cake-ui.json), [monero-cake-version](../catalog/evidence/monero-cake-version.json), [monero-cake-wallet-monero-wallet](../catalog/evidence/monero-cake-wallet-monero-wallet.json)
- Подтверждаемое утверждение: Backup UI obtains wallet.seed; separate from import service branches. Reviewed 2026-09-29; response byte SHA-256 e57829ad9284056ec12b705e5e2c289434a6d952966ad232adfaca0c8616986c. See docs/research/batches/monero-polyseed.md.
- Подтверждаемое утверждение: seed getter delegates getSeed; separate seedLegacy helper exists. Runtime artifact not executed. Reviewed 2026-09-29; response byte SHA-256 a5b4e7ef6cfa274eec62670850358f433c26c0f19cdea5cf1f081592e3712e68. See docs/research/batches/monero-polyseed.md.
- Подтверждаемое утверждение: Explicit legacy 25, Polyseed 16 \(default\), BIP39 12 mode labels. Reviewed 2026-09-29; response byte SHA-256 04848d36e285949e61e16b53c9cd9589d0896eaf3921575ea86fba983ad6d5fe. See docs/research/batches/monero-polyseed.md.
- Подтверждаемое утверждение: Root version template 0.0.0 is not a released version; source SHA singleton only. Reviewed 2026-09-29; response byte SHA-256 bc50a0936bf299070e19fcd721af9d5c76f374da719d720cea8ff029f289a21b. See docs/research/batches/monero-polyseed.md.
- Подтверждаемое утверждение: Android source snapshot only; default seedType=polyseed, Polyseed.create and separate legacy/bip39 branches. Generated pubspec version is 0.0.0 placeholder\: exact commit is the version bound, not an invented release. Reviewed 2026-09-29; response byte SHA-256 9e0591a1fa987aa48ad876fecdb5ad41b77accd8cdd9fc2a382a90563148d727. See docs/research/batches/monero-polyseed.md.
- Другие названия: —
- Схема: [polyseed-16](#scheme-polyseed-16)
- Создаёт мнемонику / только импорт: true / false
- Ограничения: Android source snapshot only; default seedType=polyseed, Polyseed.create and separate legacy/bip39 branches. Generated pubspec version is 0.0.0 placeholder\: exact commit is the version bound, not an invented release.; Documented, not selectable\: no exact released artifact and independent wallet-level recovery vector verified. Import, generation and export claims must be assessed separately.
- Рекомендация профиля: Use the trusted original wallet backup/recovery procedure; match product, platform, exact version and concrete mode. Never type a full phrase into Tessaveil or a website.

<a id="wallet-cake-wallet-monero-bip39"></a>

### Cake Wallet Monero — BIP39-derived mode — cake-wallet-monero-bip39

- Исходная запись: [cake-wallet-monero-bip39](../catalog/wallets/cake-wallet-monero-bip39.json)
- Статус: documented
- Причина: Доказательств недостаточно для доступной поддержки.
- Рекомендация: Недоступно для выбора; используйте процедуру резервного копирования самого кошелька.
- Диапазон версий (min / max): source-9679f91a8c9f63d00500c2b7cc18daf00949bdef / source-9679f91a8c9f63d00500c2b7cc18daf00949bdef
- Дата проверки: 2026-09-29
- Историческая запись: false
- Доказательства: [monero-cake-ui](../catalog/evidence/monero-cake-ui.json), [monero-cake-version](../catalog/evidence/monero-cake-version.json), [monero-cake-wallet-monero-bip39-wallet](../catalog/evidence/monero-cake-wallet-monero-bip39-wallet.json)
- Подтверждаемое утверждение: Explicit legacy 25, Polyseed 16 \(default\), BIP39 12 mode labels. Reviewed 2026-09-29; response byte SHA-256 04848d36e285949e61e16b53c9cd9589d0896eaf3921575ea86fba983ad6d5fe. See docs/research/batches/monero-polyseed.md.
- Подтверждаемое утверждение: Root version template 0.0.0 is not a released version; source SHA singleton only. Reviewed 2026-09-29; response byte SHA-256 bc50a0936bf299070e19fcd721af9d5c76f374da719d720cea8ff029f289a21b. See docs/research/batches/monero-polyseed.md.
- Подтверждаемое утверждение: Distinct 12-word BIP39-derived mode exists in source; Monero derivation path/transform is not generic BIP39 wallet compatibility. Full mode research outside this three-scheme batch; leave unmapped and non-selectable, never substitute for Polyseed/legacy. Reviewed 2026-09-29; response byte SHA-256 18d553ebf4da1994bd39be740c417a8c708c5d54aff82d8c364fa4927cb8fd77. See docs/research/batches/monero-polyseed.md.
- Другие названия: —
- Схема: —
- Создаёт мнемонику / только импорт: true / false
- Ограничения: Distinct 12-word BIP39-derived mode exists in source; Monero derivation path/transform is not generic BIP39 wallet compatibility. Full mode research outside this three-scheme batch; leave unmapped and non-selectable, never substitute for Polyseed/legacy.; Documented, not selectable\: no exact released artifact and independent wallet-level recovery vector verified. Import, generation and export claims must be assessed separately.
- Рекомендация профиля: Use the trusted original wallet backup/recovery procedure; match product, platform, exact version and concrete mode. Never type a full phrase into Tessaveil or a website.

<a id="wallet-cake-wallet-monero-legacy"></a>

### Cake Wallet Monero — legacy creation — cake-wallet-monero-legacy

- Исходная запись: [cake-wallet-monero-legacy](../catalog/wallets/cake-wallet-monero-legacy.json)
- Статус: documented
- Причина: Доказательств недостаточно для доступной поддержки.
- Рекомендация: Недоступно для выбора; используйте процедуру резервного копирования самого кошелька.
- Диапазон версий (min / max): source-9679f91a8c9f63d00500c2b7cc18daf00949bdef / source-9679f91a8c9f63d00500c2b7cc18daf00949bdef
- Дата проверки: 2026-09-29
- Историческая запись: false
- Доказательства: [monero-cake-export](../catalog/evidence/monero-cake-export.json), [monero-cake-seed](../catalog/evidence/monero-cake-seed.json), [monero-cake-ui](../catalog/evidence/monero-cake-ui.json), [monero-cake-version](../catalog/evidence/monero-cake-version.json), [monero-cake-wallet-monero-legacy-wallet](../catalog/evidence/monero-cake-wallet-monero-legacy-wallet.json)
- Подтверждаемое утверждение: Backup UI obtains wallet.seed; separate from import service branches. Reviewed 2026-09-29; response byte SHA-256 e57829ad9284056ec12b705e5e2c289434a6d952966ad232adfaca0c8616986c. See docs/research/batches/monero-polyseed.md.
- Подтверждаемое утверждение: seed getter delegates getSeed; separate seedLegacy helper exists. Runtime artifact not executed. Reviewed 2026-09-29; response byte SHA-256 a5b4e7ef6cfa274eec62670850358f433c26c0f19cdea5cf1f081592e3712e68. See docs/research/batches/monero-polyseed.md.
- Подтверждаемое утверждение: Explicit legacy 25, Polyseed 16 \(default\), BIP39 12 mode labels. Reviewed 2026-09-29; response byte SHA-256 04848d36e285949e61e16b53c9cd9589d0896eaf3921575ea86fba983ad6d5fe. See docs/research/batches/monero-polyseed.md.
- Подтверждаемое утверждение: Root version template 0.0.0 is not a released version; source SHA singleton only. Reviewed 2026-09-29; response byte SHA-256 bc50a0936bf299070e19fcd721af9d5c76f374da719d720cea8ff029f289a21b. See docs/research/batches/monero-polyseed.md.
- Подтверждаемое утверждение: Separate legacy creation branch delegates native createWallet; UI labels 25 words. FFI/dependency artifact binding and full recovery vector remain unresolved; no iOS/desktop claim. Reviewed 2026-09-29; response byte SHA-256 9e0591a1fa987aa48ad876fecdb5ad41b77accd8cdd9fc2a382a90563148d727. See docs/research/batches/monero-polyseed.md.
- Другие названия: —
- Схема: [monero-legacy](#scheme-monero-legacy)
- Создаёт мнемонику / только импорт: true / false
- Ограничения: Separate legacy creation branch delegates native createWallet; UI labels 25 words. FFI/dependency artifact binding and full recovery vector remain unresolved; no iOS/desktop claim.; Documented, not selectable\: no exact released artifact and independent wallet-level recovery vector verified. Import, generation and export claims must be assessed separately.
- Рекомендация профиля: Use the trusted original wallet backup/recovery procedure; match product, platform, exact version and concrete mode. Never type a full phrase into Tessaveil or a website.

<a id="wallet-exodus-monero-export"></a>

### Exodus Desktop — Monero 25-word export — exodus-monero-export

- Исходная запись: [exodus-monero-export](../catalog/wallets/exodus-monero-export.json)
- Статус: documented
- Причина: Доказательств недостаточно для доступной поддержки.
- Рекомендация: Недоступно для выбора; используйте процедуру резервного копирования самого кошелька.
- Диапазон версий (min / max): version-unresolved-doc-2026-01-20 / version-unresolved-doc-2026-01-20
- Дата проверки: 2026-09-29
- Историческая запись: false
- Доказательства: [monero-exodus-doc](../catalog/evidence/monero-exodus-doc.json)
- Подтверждаемое утверждение: Official article updated January 20 2026\: XMR support ended August 18 2025, but Desktop Settings/Assets/Monero Private Keys still exports a 25-word mnemonic. Mobile users must sync to Desktop. Cake restore instructions select Legacy 25 English. Article gives no app version interval; direct body retrieval was blocked \(HTTP 403\), so no body hash or immutable snapshot is claimed. Read through web retrieval.
- Другие названия: Exodus Desktop
- Схема: [monero-legacy](#scheme-monero-legacy)
- Создаёт мнемонику / только импорт: false / false
- Ограничения: Export of an existing Monero wallet only; generates\_mnemonic=false does not deny export. App versions and full export derivation vector are unresolved, so documented/non-selectable.; Windows Desktop path documented \(Mac also mentioned but not generalized here\); Mobile must sync to Desktop. No 25-word import-into-Exodus or fresh XMR creation claim. The global Exodus 12-word backup is distinct.
- Рекомендация профиля: Use the vendor migration instructions and a trusted compatible wallet; do not enter the full phrase in Tessaveil. XMR support cessation does not mean seed export is absent.

<a id="wallet-feather"></a>

### Feather — Polyseed creation — feather

- Исходная запись: [feather](../catalog/wallets/feather.json)
- Статус: documented
- Причина: Доказательств недостаточно для доступной поддержки.
- Рекомендация: Недоступно для выбора; используйте процедуру резервного копирования самого кошелька.
- Диапазон версий (min / max): 2.9.1-source-948773cf13c7486ee230eb67b6bac06b2f94c874 / 2.9.1-source-948773cf13c7486ee230eb67b6bac06b2f94c874
- Дата проверки: 2026-09-29
- Историческая запись: false
- Доказательства: [monero-feather-create](../catalog/evidence/monero-feather-create.json), [monero-feather-version](../catalog/evidence/monero-feather-version.json), [monero-feather-wallet](../catalog/evidence/monero-feather-wallet.json)
- Подтверждаемое утверждение: Creation rejects non-Polyseed and non-English; restoration handles Polyseed, Tevador 14 and legacy separately. Reviewed 2026-09-29; response byte SHA-256 dc79e1b6aace91076f1f9da96411706661830f55fda93926776d83e22d3ab8e5. See docs/research/batches/monero-polyseed.md.
- Подтверждаемое утверждение: Project version 2.9.1 at this source revision. Reviewed 2026-09-29; response byte SHA-256 d1eb1b67c42fbeb682a945225097cec2c434040d42d1ce583e640f9f6450e8b7. See docs/research/batches/monero-polyseed.md.
- Подтверждаемое утверждение: Feather 2.9.1 source\: new seeds are English Polyseed only. Source creation and display examined; no released-binary recovery/vector claim. Reviewed 2026-09-29; response byte SHA-256 53c8e05132d18d59a27df07231bbb4fe7a4aa0d559f5d32c28262810e73bce89. See docs/research/batches/monero-polyseed.md.
- Другие названия: —
- Схема: [polyseed-16](#scheme-polyseed-16)
- Создаёт мнемонику / только импорт: true / false
- Ограничения: Feather 2.9.1 source\: new seeds are English Polyseed only. Source creation and display examined; no released-binary recovery/vector claim.; Documented, not selectable\: no exact released artifact and independent wallet-level recovery vector verified. Import, generation and export claims must be assessed separately.
- Рекомендация профиля: Use the trusted original wallet backup/recovery procedure; match product, platform, exact version and concrete mode. Never type a full phrase into Tessaveil or a website.

<a id="wallet-feather-legacy-import"></a>

### Feather — legacy import — feather-legacy-import

- Исходная запись: [feather-legacy-import](../catalog/wallets/feather-legacy-import.json)
- Статус: documented
- Причина: Доказательств недостаточно для доступной поддержки.
- Рекомендация: Недоступно для выбора; используйте процедуру резервного копирования самого кошелька.
- Диапазон версий (min / max): 2.9.1-source-948773cf13c7486ee230eb67b6bac06b2f94c874 / 2.9.1-source-948773cf13c7486ee230eb67b6bac06b2f94c874
- Дата проверки: 2026-09-29
- Историческая запись: false
- Доказательства: [monero-feather-legacy-import-wallet](../catalog/evidence/monero-feather-legacy-import-wallet.json), [monero-feather-version](../catalog/evidence/monero-feather-version.json)
- Подтверждаемое утверждение: Legacy 25-word \(also checksumless 24-word\) restore is separate from generation. 14-word Tevador restore is another format and is not mapped to Polyseed/MyMonero. Reviewed 2026-09-29; response byte SHA-256 dc79e1b6aace91076f1f9da96411706661830f55fda93926776d83e22d3ab8e5. See docs/research/batches/monero-polyseed.md.
- Подтверждаемое утверждение: Project version 2.9.1 at this source revision. Reviewed 2026-09-29; response byte SHA-256 d1eb1b67c42fbeb682a945225097cec2c434040d42d1ce583e640f9f6450e8b7. See docs/research/batches/monero-polyseed.md.
- Другие названия: —
- Схема: [monero-legacy](#scheme-monero-legacy)
- Создаёт мнемонику / только импорт: false / true
- Ограничения: Legacy 25-word \(also checksumless 24-word\) restore is separate from generation. 14-word Tevador restore is another format and is not mapped to Polyseed/MyMonero.; Documented, not selectable\: no exact released artifact and independent wallet-level recovery vector verified. Import, generation and export claims must be assessed separately.
- Рекомендация профиля: Use the trusted original wallet backup/recovery procedure; match product, platform, exact version and concrete mode. Never type a full phrase into Tessaveil or a website.

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

<a id="wallet-monero-cli-polyseed"></a>

### Monero CLI — Polyseed creation — monero-cli-polyseed

- Исходная запись: [monero-cli-polyseed](../catalog/wallets/monero-cli-polyseed.json)
- Статус: documented
- Причина: Доказательств недостаточно для доступной поддержки.
- Рекомендация: Недоступно для выбора; используйте процедуру резервного копирования самого кошелька.
- Диапазон версий (min / max): source-2f9d1bbb2c553dc75f3335bd1452117dfddd86fa / source-2f9d1bbb2c553dc75f3335bd1452117dfddd86fa
- Дата проверки: 2026-09-29
- Историческая запись: false
- Доказательства: [monero-cli-version](../catalog/evidence/monero-cli-version.json), [monero-monero-cli-polyseed-wallet](../catalog/evidence/monero-monero-cli-polyseed-wallet.json)
- Подтверждаемое утверждение: Development source declares 0.18.1.0; exact commit singleton is authoritative, not a release range. Reviewed 2026-09-29; response byte SHA-256 cddb09cd7a59eefe5486766145baf2849a9161a504545a649d83e034a81ea83a. See docs/research/batches/monero-polyseed.md.
- Подтверждаемое утверждение: Default deterministic new-wallet source mode is Polyseed; --use-legacy-seed is a distinct simultaneous choice. Non-deterministic, multisig, hardware and view-only modes excluded. Reviewed 2026-09-29; response byte SHA-256 54534a83e1c17bf4d5176dbdb2c1293399575058ad4db3f58948c958bda3ff15. See docs/research/batches/monero-polyseed.md.
- Другие названия: —
- Схема: [polyseed-16](#scheme-polyseed-16)
- Создаёт мнемонику / только импорт: true / false
- Ограничения: Default deterministic new-wallet source mode is Polyseed; --use-legacy-seed is a distinct simultaneous choice. Non-deterministic, multisig, hardware and view-only modes excluded.; Documented, not selectable\: no exact released artifact and independent wallet-level recovery vector verified. Import, generation and export claims must be assessed separately.
- Рекомендация профиля: Use the trusted original wallet backup/recovery procedure; match product, platform, exact version and concrete mode. Never type a full phrase into Tessaveil or a website.

<a id="wallet-monero-gui"></a>

### Monero GUI — generated seed — monero-gui

- Исходная запись: [monero-gui](../catalog/wallets/monero-gui.json)
- Статус: documented
- Причина: Доказательств недостаточно для доступной поддержки.
- Рекомендация: Недоступно для выбора; используйте процедуру резервного копирования самого кошелька.
- Диапазон версий (min / max): source-01d6640aff7fd1c1a87932e14e8439383e1229c5 / source-01d6640aff7fd1c1a87932e14e8439383e1229c5
- Дата проверки: 2026-09-29
- Историческая запись: false
- Доказательства: [monero-monero-gui-wallet](../catalog/evidence/monero-monero-gui-wallet.json)
- Подтверждаемое утверждение: Wizard creates an in-memory wallet then displays wallet.seed. Exact pinned backend dependency and scheme are unresolved in this GUI snapshot; do not substitute current CLI behavior. Reviewed 2026-09-29; response byte SHA-256 ce321b1d39e21dfa6e50c36d07206f2d7d37acb8d4cef3d1c9225db473a6b7af. See docs/research/batches/monero-polyseed.md.
- Другие названия: —
- Схема: —
- Создаёт мнемонику / только импорт: true / false
- Ограничения: Wizard creates an in-memory wallet then displays wallet.seed. Exact pinned backend dependency and scheme are unresolved in this GUI snapshot; do not substitute current CLI behavior.; Documented, not selectable\: no exact released artifact and independent wallet-level recovery vector verified. Import, generation and export claims must be assessed separately.
- Рекомендация профиля: Use the trusted original wallet backup/recovery procedure; match product, platform, exact version and concrete mode. Never type a full phrase into Tessaveil or a website.

<a id="wallet-monero-gui-cli"></a>

### Monero CLI — legacy creation — monero-gui-cli

- Исходная запись: [monero-gui-cli](../catalog/wallets/monero-gui-cli.json)
- Статус: documented
- Причина: Доказательств недостаточно для доступной поддержки.
- Рекомендация: Недоступно для выбора; используйте процедуру резервного копирования самого кошелька.
- Диапазон версий (min / max): source-2f9d1bbb2c553dc75f3335bd1452117dfddd86fa / source-2f9d1bbb2c553dc75f3335bd1452117dfddd86fa
- Дата проверки: 2026-09-29
- Историческая запись: false
- Доказательства: [monero-cli-version](../catalog/evidence/monero-cli-version.json), [monero-monero-gui-cli-wallet](../catalog/evidence/monero-monero-gui-cli-wallet.json)
- Подтверждаемое утверждение: Development source declares 0.18.1.0; exact commit singleton is authoritative, not a release range. Reviewed 2026-09-29; response byte SHA-256 cddb09cd7a59eefe5486766145baf2849a9161a504545a649d83e034a81ea83a. See docs/research/batches/monero-polyseed.md.
- Подтверждаемое утверждение: Exact CLI source revision, explicit --use-legacy-seed mode. Default source creation is now Polyseed. GUI is a separate record; neither label implies all CLI/GUI versions. Reviewed 2026-09-29; response byte SHA-256 54534a83e1c17bf4d5176dbdb2c1293399575058ad4db3f58948c958bda3ff15. See docs/research/batches/monero-polyseed.md.
- Другие названия: —
- Схема: [monero-legacy](#scheme-monero-legacy)
- Создаёт мнемонику / только импорт: true / false
- Ограничения: Exact CLI source revision, explicit --use-legacy-seed mode. Default source creation is now Polyseed. GUI is a separate record; neither label implies all CLI/GUI versions.; Documented, not selectable\: no exact released artifact and independent wallet-level recovery vector verified. Import, generation and export claims must be assessed separately.
- Рекомендация профиля: Use the trusted original wallet backup/recovery procedure; match product, platform, exact version and concrete mode. Never type a full phrase into Tessaveil or a website.

<a id="wallet-mymonero"></a>

### MyMonero — legacy 13-word restoration — mymonero

- Исходная запись: [mymonero](../catalog/wallets/mymonero.json)
- Статус: documented
- Причина: Доказательств недостаточно для доступной поддержки.
- Рекомендация: Недоступно для выбора; используйте процедуру резервного копирования самого кошелька.
- Диапазон версий (min / max): 1.3.2-source-5c7455d30e4e20150962f5f74efd83477962a05e / 1.3.2-source-5c7455d30e4e20150962f5f74efd83477962a05e
- Дата проверки: 2026-09-29
- Историческая запись: false
- Доказательства: [monero-my-core](../catalog/evidence/monero-my-core.json), [monero-mymonero-wallet](../catalog/evidence/monero-mymonero-wallet.json)
- Подтверждаемое утверждение: new\_wallet creates 32-byte/25-word backups; decoded\_seed handles 13 and 25 and hashes 16-byte seeds. Core/app binding remains unproven. Reviewed 2026-09-29; response byte SHA-256 ea6d34729151cffd2b7cdd1a16c31507ff3122242540646ac9797cc0797bb7b4. See docs/research/batches/monero-polyseed.md.
- Подтверждаемое утверждение: App 1.3.2 source and core decoder source reviewed separately; exact app-to-core artifact binding is not established. Historical 13-word restore capability is documented in core, not a claim that current app creates 13 words. Reviewed 2026-09-29; response byte SHA-256 c00f3699d4f244e57dba1522665910687c0fdf2228edfc576f83a717dfc75457. See docs/research/batches/monero-polyseed.md.
- Другие названия: —
- Схема: [mymonero-13](#scheme-mymonero-13)
- Создаёт мнемонику / только импорт: false / true
- Ограничения: App 1.3.2 source and core decoder source reviewed separately; exact app-to-core artifact binding is not established. Historical 13-word restore capability is documented in core, not a claim that current app creates 13 words.; Documented, not selectable\: no exact released artifact and independent wallet-level recovery vector verified. Import, generation and export claims must be assessed separately.
- Рекомендация профиля: Use the trusted original wallet backup/recovery procedure; match product, platform, exact version and concrete mode. Never type a full phrase into Tessaveil or a website.

<a id="wallet-mymonero-generated"></a>

### MyMonero — generated backup — mymonero-generated

- Исходная запись: [mymonero-generated](../catalog/wallets/mymonero-generated.json)
- Статус: documented
- Причина: Доказательств недостаточно для доступной поддержки.
- Рекомендация: Недоступно для выбора; используйте процедуру резервного копирования самого кошелька.
- Диапазон версий (min / max): 1.3.2-source-5c7455d30e4e20150962f5f74efd83477962a05e / 1.3.2-source-5c7455d30e4e20150962f5f74efd83477962a05e
- Дата проверки: 2026-09-29
- Историческая запись: false
- Доказательства: [monero-my-core](../catalog/evidence/monero-my-core.json), [monero-mymonero-generated-wallet](../catalog/evidence/monero-mymonero-generated-wallet.json)
- Подтверждаемое утверждение: new\_wallet creates 32-byte/25-word backups; decoded\_seed handles 13 and 25 and hashes 16-byte seeds. Core/app binding remains unproven. Reviewed 2026-09-29; response byte SHA-256 ea6d34729151cffd2b7cdd1a16c31507ff3122242540646ac9797cc0797bb7b4. See docs/research/batches/monero-polyseed.md.
- Подтверждаемое утверждение: App shows backup mnemonic. Reviewed core new\_wallet generates 32-byte/25-word format, but dependency artifact binding to this app revision remains unproven. No new 13-word creation claim. Reviewed 2026-09-29; response byte SHA-256 1772443b59b4c4286aa30054f41d7f6110c35e2d471344b00346ca7774c9c674. See docs/research/batches/monero-polyseed.md.
- Другие названия: —
- Схема: —
- Создаёт мнемонику / только импорт: true / false
- Ограничения: App shows backup mnemonic. Reviewed core new\_wallet generates 32-byte/25-word format, but dependency artifact binding to this app revision remains unproven. No new 13-word creation claim.; Documented, not selectable\: no exact released artifact and independent wallet-level recovery vector verified. Import, generation and export claims must be assessed separately.
- Рекомендация профиля: Use the trusted original wallet backup/recovery procedure; match product, platform, exact version and concrete mode. Never type a full phrase into Tessaveil or a website.

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

<a id="scheme-monero-legacy"></a>

### monero-legacy — monero-legacy

- Исходная запись: [monero-legacy](../catalog/schemes/monero-legacy.json)
- Статус: documented
- Причина: Доказательств недостаточно для доступной поддержки.
- Рекомендация: Недоступно для выбора; используйте процедуру резервного копирования самого кошелька.
- Диапазон версий (min / max): 2f9d1bbb2c553dc75f3335bd1452117dfddd86fa / 2f9d1bbb2c553dc75f3335bd1452117dfddd86fa
- Дата проверки: 2026-09-29
- Историческая запись: false
- Доказательства: [monero-legacy-vectors](../catalog/evidence/monero-legacy-vectors.json), [monero-monero-legacy-scheme](../catalog/evidence/monero-monero-legacy-scheme.json)
- Подтверждаемое утверждение: Public Portuguese checksum and German case-tolerance examples; projection stores dictionary indices and expected phrase fingerprint. Offline test reproduces source CRC32 prefix check, not private-key/address derivation. Reviewed 2026-09-29; response byte SHA-256 520fec49e96e4b01d472f627e109b7a343f80e58291eed793f7ca76f2e63a1d1. See docs/research/batches/monero-polyseed.md.
- Подтверждаемое утверждение: Eight little-endian 32-bit chunks map to 24 base-1626 words; CRC32 of language-specific prefixes selects repeated 25th checksum word. Not BIP39. EnglishOld has a separate historical dictionary and is excluded from current-generation language list; no selectable historical 25-word mode is inferred. Source supports additional checksumless restore lengths; this profile covers standard 25 only. Reviewed 2026-09-29; response byte SHA-256 f92675503096425c92f6cc8b38946a707db6999cfcd95657f87a58d364051e4f. See docs/research/batches/monero-polyseed.md.
- Словари: [monero-de](#dictionary-monero-de), [monero-en](#dictionary-monero-en), [monero-eo](#dictionary-monero-eo), [monero-es](#dictionary-monero-es), [monero-fr](#dictionary-monero-fr), [monero-it](#dictionary-monero-it), [monero-ja](#dictionary-monero-ja), [monero-jbo](#dictionary-monero-jbo), [monero-nl](#dictionary-monero-nl), [monero-pt](#dictionary-monero-pt), [monero-ru](#dictionary-monero-ru), [monero-zh-hans](#dictionary-monero-zh-hans)
- Допустимые длины: 25
- Позиционные правила: One dictionary per phrase; same vocabulary at each position. Last word is repeated checksum for 25/13; first word is Polyseed checksum for 16. No complete user phrase validation.
- Семантика: Eight little-endian 32-bit chunks map to 24 base-1626 words; CRC32 of language-specific prefixes selects repeated 25th checksum word. Not BIP39. EnglishOld has a separate historical dictionary and is excluded from current-generation language list; no selectable historical 25-word mode is inferred. Source supports additional checksumless restore lengths; this profile covers standard 25 only. Documented\: offline tests establish encoding/checksum only; full independent key derivation and exact wallet artifact binding are not established.
- Внешний секрет / сохраняется: optional-passphrase / false
- Рекомендация о внешнем секрете: Keep any supported seed offset/encryption passphrase separately. Tessaveil never stores it. App login passwords/PINs are not automatically mnemonic secrets; verify exact wallet mode.
- Тестовые векторы: [monero-legacy-vectors](../catalog/evidence/monero-legacy-vectors.json)

<a id="scheme-mymonero-13"></a>

### mymonero-13 — mymonero-13

- Исходная запись: [mymonero-13](../catalog/schemes/mymonero-13.json)
- Статус: documented
- Причина: Доказательств недостаточно для доступной поддержки.
- Рекомендация: Недоступно для выбора; используйте процедуру резервного копирования самого кошелька.
- Диапазон версий (min / max): 9637c91cbe5f46e67156c66c739932294808109d / 9637c91cbe5f46e67156c66c739932294808109d
- Дата проверки: 2026-09-29
- Историческая запись: false
- Доказательства: [monero-mymonero-13-scheme](../catalog/evidence/monero-mymonero-13-scheme.json), [monero-mymonero-vectors](../catalog/evidence/monero-mymonero-vectors.json)
- Подтверждаемое утверждение: Legacy MyMonero\: four 32-bit chunks encode a 16-byte seed as 12 words plus prefix CRC32 checksum. Keccak expansion before scalar reduction differs from 32-byte Monero legacy. Current core new\_wallet creates a 32-byte/25-word seed; 13 words are retained for legacy decoding. English vector only; other language/product mappings are not verified. Reviewed 2026-09-29; response byte SHA-256 ea6d34729151cffd2b7cdd1a16c31507ff3122242540646ac9797cc0797bb7b4. See docs/research/batches/monero-polyseed.md.
- Подтверждаемое утверждение: Published 13-word prefix mnemonic resolves to the same address as published 16-byte seed 9c973aa296b79bbf452781dd3d32ad7f. Offline projection tests entropy and checksum only; no address/Keccak claim. Reviewed 2026-09-29; response byte SHA-256 8292f763a1b2bf70052dc959a2672e73a1b4035d5c379bbccb4e03f6a2de6634. See docs/research/batches/monero-polyseed.md.
- Словари: [monero-en](#dictionary-monero-en)
- Допустимые длины: 13
- Позиционные правила: One dictionary per phrase; same vocabulary at each position. Last word is repeated checksum for 25/13; first word is Polyseed checksum for 16. No complete user phrase validation.
- Семантика: Legacy MyMonero\: four 32-bit chunks encode a 16-byte seed as 12 words plus prefix CRC32 checksum. Keccak expansion before scalar reduction differs from 32-byte Monero legacy. Current core new\_wallet creates a 32-byte/25-word seed; 13 words are retained for legacy decoding. English vector only; other language/product mappings are not verified. Documented\: offline tests establish encoding/checksum only; full independent key derivation and exact wallet artifact binding are not established.
- Внешний секрет / сохраняется: none / false
- Рекомендация о внешнем секрете: Keep any supported seed offset/encryption passphrase separately. Tessaveil never stores it. App login passwords/PINs are not automatically mnemonic secrets; verify exact wallet mode.
- Тестовые векторы: [monero-mymonero-vectors](../catalog/evidence/monero-mymonero-vectors.json)

<a id="scheme-polyseed-16"></a>

### polyseed-16 — polyseed-16

- Исходная запись: [polyseed-16](../catalog/schemes/polyseed-16.json)
- Статус: documented
- Причина: Доказательств недостаточно для доступной поддержки.
- Рекомендация: Недоступно для выбора; используйте процедуру резервного копирования самого кошелька.
- Диапазон версий (min / max): 56f634647d4f75596de20a6259b0cf1933949fdc / 56f634647d4f75596de20a6259b0cf1933949fdc
- Дата проверки: 2026-09-29
- Историческая запись: false
- Доказательства: [monero-polyseed-16-scheme](../catalog/evidence/monero-polyseed-16-scheme.json), [monero-polyseed-vectors](../catalog/evidence/monero-polyseed-vectors.json)
- Подтверждаемое утверждение: Sixteen 11-bit indices\: first is GF\(2048\) checksum, remaining words interleave 150 secret bits, 5 feature bits and 10 birthday bits. Coin domain separation and PBKDF2-HMAC-SHA256 \(10000\) differ from BIP39; modified Spanish/Japanese/Czech orders must be preserved. Optional seed encryption passphrase is not an app password. Reviewed 2026-09-29; response byte SHA-256 51abea48365ac1e4f8fb364be55a69550f81e265d6d96487c418e223789845d8. See docs/research/batches/monero-polyseed.md.
- Подтверждаемое утверждение: Published English/Spanish fixed phrases, random byte inputs, birthday and PBKDF2-input assertions. Projection tests dictionary order, GF checksum and secret/date unpacking. Upstream PBKDF2 is a dummy\: these are NOT derived-key known answers. Reviewed 2026-09-29; response byte SHA-256 3bc51ff2c12c3840e93d5e87a8da47516f806e3d51dc72ea6049f7f439dba4d5. See docs/research/batches/monero-polyseed.md.
- Словари: [polyseed-cs](#dictionary-polyseed-cs), [polyseed-en](#dictionary-polyseed-en), [polyseed-es](#dictionary-polyseed-es), [polyseed-fr](#dictionary-polyseed-fr), [polyseed-it](#dictionary-polyseed-it), [polyseed-ja](#dictionary-polyseed-ja), [polyseed-ko](#dictionary-polyseed-ko), [polyseed-pt](#dictionary-polyseed-pt), [polyseed-zh-hans](#dictionary-polyseed-zh-hans), [polyseed-zh-hant](#dictionary-polyseed-zh-hant)
- Допустимые длины: 16
- Позиционные правила: One dictionary per phrase; same vocabulary at each position. Last word is repeated checksum for 25/13; first word is Polyseed checksum for 16. No complete user phrase validation.
- Семантика: Sixteen 11-bit indices\: first is GF\(2048\) checksum, remaining words interleave 150 secret bits, 5 feature bits and 10 birthday bits. Coin domain separation and PBKDF2-HMAC-SHA256 \(10000\) differ from BIP39; modified Spanish/Japanese/Czech orders must be preserved. Optional seed encryption passphrase is not an app password. Documented\: offline tests establish encoding/checksum only; full independent key derivation and exact wallet artifact binding are not established.
- Внешний секрет / сохраняется: optional-passphrase / false
- Рекомендация о внешнем секрете: Keep any supported seed offset/encryption passphrase separately. Tessaveil never stores it. App login passwords/PINs are not automatically mnemonic secrets; verify exact wallet mode.
- Тестовые векторы: [monero-polyseed-vectors](../catalog/evidence/monero-polyseed-vectors.json)

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

<a id="dictionary-monero-de"></a>

### monero-de — monero-de

- Исходная запись: [monero-de](../catalog/dictionaries/monero-de.json)
- Статус: verified
- Причина: Проверенная исследовательская запись; не гарантия релиза или безопасности.
- Диапазон версий (min / max): 2f9d1bbb2c553dc75f3335bd1452117dfddd86fa / 2f9d1bbb2c553dc75f3335bd1452117dfddd86fa
- Дата проверки: 2026-09-29
- Историческая запись: false
- Доказательства: [monero-de-source](../catalog/evidence/monero-de-source.json), [monero-legacy-vectors](../catalog/evidence/monero-legacy-vectors.json), [monero-monero-license](../catalog/evidence/monero-monero-license.json), [monero-monero-rules](../catalog/evidence/monero-monero-rules.json), [monero-osi-bsd](../catalog/evidence/monero-osi-bsd.json), [monero-signpath](../catalog/evidence/monero-signpath.json)
- Подтверждаемое утверждение: Exact ordered dictionary array and applicable file-level license header reviewed. Source-token extraction and byte hashes are independently checked against the public fixture; no complete phrase is stored here. Reviewed 2026-09-29; response byte SHA-256 7b910a96bc94d19eb3e4edd8179db383a68b03a7608396bbee0fdc46a7d4e88e. See docs/research/batches/monero-polyseed.md.
- Подтверждаемое утверждение: Public Portuguese checksum and German case-tolerance examples; projection stores dictionary indices and expected phrase fingerprint. Offline test reproduces source CRC32 prefix check, not private-key/address derivation. Reviewed 2026-09-29; response byte SHA-256 520fec49e96e4b01d472f627e109b7a343f80e58291eed793f7ca76f2e63a1d1. See docs/research/batches/monero-polyseed.md.
- Подтверждаемое утверждение: BSD-3-Clause source-data redistribution allowed with exact copyright/license/disclaimer retention and no endorsement. File-level MIT overrides for dabura667 lists retained. Reviewed by Codex for this source-data payload only. Reviewed 2026-09-29; response byte SHA-256 1f99d6b6e1ae17de27147ff2e1e0238fa8c7d5a8accd0f1ac062c89365516abd. See docs/research/batches/monero-polyseed.md.
- Подтверждаемое утверждение: 1626 entries; codepoint prefixes and case-insensitive lookup. utf8canonical re-encodes codepoints with towlower, not NFC/NFKD. EnglishOld tolerates duplicate prefixes and short words. Reviewed 2026-09-29; response byte SHA-256 2bc256f01c6904af914cb7c6526254267ed463882e216fd0eb1d9bbdf4bf5bb4. See docs/research/batches/monero-polyseed.md.
- Подтверждаемое утверждение: OSI lists BSD-3-Clause as approved. This corroborates only the component-license decision, not project acceptance. Response-body SHA-256 0dfece33194f06d15b862c323f7ed32ba6ab7f512a7fda11880bb2e1401518f8.
- Подтверждаемое утверждение: Codex component assessment\: reviewed BSD-3-Clause/MIT and Apache-2.0\+MIT data licenses are OSI-approved and impose no commercial dual-licensing; notices are retained. Compatible for this data-only payload. Foundation acceptance, project eligibility and release signing remain unproven. Response-body SHA-256 6610cf889bbe0dc7533abaa310bc7a5cc9a61ae6c2ce0798a08109c925b46c51.
- Язык: de
- Письменность: Latn
- Кодировка: UTF-8
- Нормализация: none
- Количество слов: 1626
- SHA-256: e1e6653cf418e0a392a5cd34160a8cdacb5dfce8edbac0e124fba8d7daff1f69
- Порядок слов: Exact upstream array order; zero-based indices. Extract literal UTF-8 tokens unchanged; remove C/C\+\+ wrapper and indentation, append LF after every token. No sorting, lowercasing or Unicode rewriting. Source file and extracted byte hashes in batch note.
- Позиционные правила: Same vocabulary at every eligible position; upstream prefix length 4. Never evaluate a user phrase checksum.; Source-native lookup\: Unicode codepoint lowercase and language-specific prefix, with no NFC/NFKD transform; normalization=none preserves source characters.; Language coverage is not a wallet generation claim.
- Ревизия источника: 2f9d1bbb2c553dc75f3335bd1452117dfddd86fa
- Лицензия: BSD-3-Clause
- Атрибуция: Exact source file notices and upstream license retained in THIRD\_PARTY\_NOTICES; dabura667 / The Monero Project and original dictionary contributors.
- Распространение в репозитории: allowed
- Совместимость с SignPath: compatible
- Доказательства лицензии: [monero-de-source](../catalog/evidence/monero-de-source.json), [monero-monero-license](../catalog/evidence/monero-monero-license.json), [monero-osi-bsd](../catalog/evidence/monero-osi-bsd.json), [monero-signpath](../catalog/evidence/monero-signpath.json)
- Тестовые векторы: [monero-legacy-vectors](../catalog/evidence/monero-legacy-vectors.json)

<a id="dictionary-monero-en"></a>

### monero-en — monero-en

- Исходная запись: [monero-en](../catalog/dictionaries/monero-en.json)
- Статус: verified
- Причина: Проверенная исследовательская запись; не гарантия релиза или безопасности.
- Диапазон версий (min / max): 2f9d1bbb2c553dc75f3335bd1452117dfddd86fa / 2f9d1bbb2c553dc75f3335bd1452117dfddd86fa
- Дата проверки: 2026-09-29
- Историческая запись: false
- Доказательства: [monero-en-source](../catalog/evidence/monero-en-source.json), [monero-monero-license](../catalog/evidence/monero-monero-license.json), [monero-monero-rules](../catalog/evidence/monero-monero-rules.json), [monero-mymonero-vectors](../catalog/evidence/monero-mymonero-vectors.json), [monero-osi-bsd](../catalog/evidence/monero-osi-bsd.json), [monero-signpath](../catalog/evidence/monero-signpath.json)
- Подтверждаемое утверждение: Exact ordered dictionary array and applicable file-level license header reviewed. Source-token extraction and byte hashes are independently checked against the public fixture; no complete phrase is stored here. Reviewed 2026-09-29; response byte SHA-256 9bd756d29e689aae0e6e7f8b1196c4f35df350225c4668d4f6f41842f05fc2ca. See docs/research/batches/monero-polyseed.md.
- Подтверждаемое утверждение: BSD-3-Clause source-data redistribution allowed with exact copyright/license/disclaimer retention and no endorsement. File-level MIT overrides for dabura667 lists retained. Reviewed by Codex for this source-data payload only. Reviewed 2026-09-29; response byte SHA-256 1f99d6b6e1ae17de27147ff2e1e0238fa8c7d5a8accd0f1ac062c89365516abd. See docs/research/batches/monero-polyseed.md.
- Подтверждаемое утверждение: 1626 entries; codepoint prefixes and case-insensitive lookup. utf8canonical re-encodes codepoints with towlower, not NFC/NFKD. EnglishOld tolerates duplicate prefixes and short words. Reviewed 2026-09-29; response byte SHA-256 2bc256f01c6904af914cb7c6526254267ed463882e216fd0eb1d9bbdf4bf5bb4. See docs/research/batches/monero-polyseed.md.
- Подтверждаемое утверждение: Published 13-word prefix mnemonic resolves to the same address as published 16-byte seed 9c973aa296b79bbf452781dd3d32ad7f. Offline projection tests entropy and checksum only; no address/Keccak claim. Reviewed 2026-09-29; response byte SHA-256 8292f763a1b2bf70052dc959a2672e73a1b4035d5c379bbccb4e03f6a2de6634. See docs/research/batches/monero-polyseed.md.
- Подтверждаемое утверждение: OSI lists BSD-3-Clause as approved. This corroborates only the component-license decision, not project acceptance. Response-body SHA-256 0dfece33194f06d15b862c323f7ed32ba6ab7f512a7fda11880bb2e1401518f8.
- Подтверждаемое утверждение: Codex component assessment\: reviewed BSD-3-Clause/MIT and Apache-2.0\+MIT data licenses are OSI-approved and impose no commercial dual-licensing; notices are retained. Compatible for this data-only payload. Foundation acceptance, project eligibility and release signing remain unproven. Response-body SHA-256 6610cf889bbe0dc7533abaa310bc7a5cc9a61ae6c2ce0798a08109c925b46c51.
- Язык: en
- Письменность: Latn
- Кодировка: UTF-8
- Нормализация: none
- Количество слов: 1626
- SHA-256: eaa6bce7dd92f4d6dd74f224264e0ef4ad21095d68ec77616b26ceb599baf4f7
- Порядок слов: Exact upstream array order; zero-based indices. Extract literal UTF-8 tokens unchanged; remove C/C\+\+ wrapper and indentation, append LF after every token. No sorting, lowercasing or Unicode rewriting. Source file and extracted byte hashes in batch note.
- Позиционные правила: Same vocabulary at every eligible position; upstream prefix length 3. Never evaluate a user phrase checksum.; Source-native lookup\: Unicode codepoint lowercase and language-specific prefix, with no NFC/NFKD transform; normalization=none preserves source characters.; Language coverage is not a wallet generation claim.
- Ревизия источника: 2f9d1bbb2c553dc75f3335bd1452117dfddd86fa
- Лицензия: BSD-3-Clause
- Атрибуция: Exact source file notices and upstream license retained in THIRD\_PARTY\_NOTICES; dabura667 / The Monero Project and original dictionary contributors.
- Распространение в репозитории: allowed
- Совместимость с SignPath: compatible
- Доказательства лицензии: [monero-en-source](../catalog/evidence/monero-en-source.json), [monero-monero-license](../catalog/evidence/monero-monero-license.json), [monero-osi-bsd](../catalog/evidence/monero-osi-bsd.json), [monero-signpath](../catalog/evidence/monero-signpath.json)
- Тестовые векторы: [monero-mymonero-vectors](../catalog/evidence/monero-mymonero-vectors.json)

<a id="dictionary-monero-en-old"></a>

### monero-en-old — monero-en-old

- Исходная запись: [monero-en-old](../catalog/dictionaries/monero-en-old.json)
- Статус: documented
- Причина: Доказательств недостаточно для доступной поддержки.
- Рекомендация: Недоступно для выбора; используйте процедуру резервного копирования самого кошелька.
- Диапазон версий (min / max): 2f9d1bbb2c553dc75f3335bd1452117dfddd86fa / 2f9d1bbb2c553dc75f3335bd1452117dfddd86fa
- Дата проверки: 2026-09-29
- Историческая запись: true
- Доказательства: [monero-en-old-source](../catalog/evidence/monero-en-old-source.json), [monero-monero-license](../catalog/evidence/monero-monero-license.json), [monero-monero-rules](../catalog/evidence/monero-monero-rules.json), [monero-osi-bsd](../catalog/evidence/monero-osi-bsd.json), [monero-signpath](../catalog/evidence/monero-signpath.json)
- Подтверждаемое утверждение: Exact ordered dictionary array and applicable file-level license header reviewed. Source-token extraction and byte hashes are independently checked against the public fixture; no complete phrase is stored here. Reviewed 2026-09-29; response byte SHA-256 20c9090994c5b441f2e550cddbf266d604b64e495d9b172e45a8031e1aa5d578. See docs/research/batches/monero-polyseed.md.
- Подтверждаемое утверждение: BSD-3-Clause source-data redistribution allowed with exact copyright/license/disclaimer retention and no endorsement. File-level MIT overrides for dabura667 lists retained. Reviewed by Codex for this source-data payload only. Reviewed 2026-09-29; response byte SHA-256 1f99d6b6e1ae17de27147ff2e1e0238fa8c7d5a8accd0f1ac062c89365516abd. See docs/research/batches/monero-polyseed.md.
- Подтверждаемое утверждение: 1626 entries; codepoint prefixes and case-insensitive lookup. utf8canonical re-encodes codepoints with towlower, not NFC/NFKD. EnglishOld tolerates duplicate prefixes and short words. Reviewed 2026-09-29; response byte SHA-256 2bc256f01c6904af914cb7c6526254267ed463882e216fd0eb1d9bbdf4bf5bb4. See docs/research/batches/monero-polyseed.md.
- Подтверждаемое утверждение: OSI lists BSD-3-Clause as approved. This corroborates only the component-license decision, not project acceptance. Response-body SHA-256 0dfece33194f06d15b862c323f7ed32ba6ab7f512a7fda11880bb2e1401518f8.
- Подтверждаемое утверждение: Codex component assessment\: reviewed BSD-3-Clause/MIT and Apache-2.0\+MIT data licenses are OSI-approved and impose no commercial dual-licensing; notices are retained. Compatible for this data-only payload. Foundation acceptance, project eligibility and release signing remain unproven. Response-body SHA-256 6610cf889bbe0dc7533abaa310bc7a5cc9a61ae6c2ce0798a08109c925b46c51.
- Язык: en
- Письменность: Latn
- Кодировка: UTF-8
- Нормализация: none
- Количество слов: 1626
- SHA-256: c8da327d316f8ee758b790068e618077ac271a89fd77ec1250c59ae40e7b599e
- Порядок слов: Exact upstream array order; zero-based indices. Extract literal UTF-8 tokens unchanged; remove C/C\+\+ wrapper and indentation, append LF after every token. No sorting, lowercasing or Unicode rewriting. Source file and extracted byte hashes in batch note.
- Позиционные правила: Same vocabulary at every eligible position; upstream prefix length 4. Never evaluate a user phrase checksum.; Source-native lookup\: Unicode codepoint lowercase and language-specific prefix, with no NFC/NFKD transform; normalization=none preserves source characters.; Historical restore-only EnglishOld\: excluded from generation language list; duplicate prefixes and short words explicitly allowed by upstream.
- Ревизия источника: 2f9d1bbb2c553dc75f3335bd1452117dfddd86fa
- Лицензия: BSD-3-Clause
- Атрибуция: Exact source file notices and upstream license retained in THIRD\_PARTY\_NOTICES; dabura667 / The Monero Project and original dictionary contributors.
- Распространение в репозитории: allowed
- Совместимость с SignPath: compatible
- Доказательства лицензии: [monero-en-old-source](../catalog/evidence/monero-en-old-source.json), [monero-monero-license](../catalog/evidence/monero-monero-license.json), [monero-osi-bsd](../catalog/evidence/monero-osi-bsd.json), [monero-signpath](../catalog/evidence/monero-signpath.json)
- Тестовые векторы: —

<a id="dictionary-monero-eo"></a>

### monero-eo — monero-eo

- Исходная запись: [monero-eo](../catalog/dictionaries/monero-eo.json)
- Статус: documented
- Причина: Доказательств недостаточно для доступной поддержки.
- Рекомендация: Недоступно для выбора; используйте процедуру резервного копирования самого кошелька.
- Диапазон версий (min / max): 2f9d1bbb2c553dc75f3335bd1452117dfddd86fa / 2f9d1bbb2c553dc75f3335bd1452117dfddd86fa
- Дата проверки: 2026-09-29
- Историческая запись: false
- Доказательства: [monero-eo-source](../catalog/evidence/monero-eo-source.json), [monero-monero-license](../catalog/evidence/monero-monero-license.json), [monero-monero-rules](../catalog/evidence/monero-monero-rules.json), [monero-osi-bsd](../catalog/evidence/monero-osi-bsd.json), [monero-signpath](../catalog/evidence/monero-signpath.json)
- Подтверждаемое утверждение: Exact ordered dictionary array and applicable file-level license header reviewed. Source-token extraction and byte hashes are independently checked against the public fixture; no complete phrase is stored here. Reviewed 2026-09-29; response byte SHA-256 382d9f9bfcf293e4dc9f156042fe5a3f2a151191bae368a494eaf53c77e16043. See docs/research/batches/monero-polyseed.md.
- Подтверждаемое утверждение: BSD-3-Clause source-data redistribution allowed with exact copyright/license/disclaimer retention and no endorsement. File-level MIT overrides for dabura667 lists retained. Reviewed by Codex for this source-data payload only. Reviewed 2026-09-29; response byte SHA-256 1f99d6b6e1ae17de27147ff2e1e0238fa8c7d5a8accd0f1ac062c89365516abd. See docs/research/batches/monero-polyseed.md.
- Подтверждаемое утверждение: 1626 entries; codepoint prefixes and case-insensitive lookup. utf8canonical re-encodes codepoints with towlower, not NFC/NFKD. EnglishOld tolerates duplicate prefixes and short words. Reviewed 2026-09-29; response byte SHA-256 2bc256f01c6904af914cb7c6526254267ed463882e216fd0eb1d9bbdf4bf5bb4. See docs/research/batches/monero-polyseed.md.
- Подтверждаемое утверждение: OSI lists BSD-3-Clause as approved. This corroborates only the component-license decision, not project acceptance. Response-body SHA-256 0dfece33194f06d15b862c323f7ed32ba6ab7f512a7fda11880bb2e1401518f8.
- Подтверждаемое утверждение: Codex component assessment\: reviewed BSD-3-Clause/MIT and Apache-2.0\+MIT data licenses are OSI-approved and impose no commercial dual-licensing; notices are retained. Compatible for this data-only payload. Foundation acceptance, project eligibility and release signing remain unproven. Response-body SHA-256 6610cf889bbe0dc7533abaa310bc7a5cc9a61ae6c2ce0798a08109c925b46c51.
- Язык: eo
- Письменность: Latn
- Кодировка: UTF-8
- Нормализация: none
- Количество слов: 1626
- SHA-256: aa53b9b2af6586e8df69bcf04b17af4f06cac9e7ad20420d45b265f9aa18b32d
- Порядок слов: Exact upstream array order; zero-based indices. Extract literal UTF-8 tokens unchanged; remove C/C\+\+ wrapper and indentation, append LF after every token. No sorting, lowercasing or Unicode rewriting. Source file and extracted byte hashes in batch note.
- Позиционные правила: Same vocabulary at every eligible position; upstream prefix length 4. Never evaluate a user phrase checksum.; Source-native lookup\: Unicode codepoint lowercase and language-specific prefix, with no NFC/NFKD transform; normalization=none preserves source characters.; Language coverage is not a wallet generation claim.
- Ревизия источника: 2f9d1bbb2c553dc75f3335bd1452117dfddd86fa
- Лицензия: BSD-3-Clause
- Атрибуция: Exact source file notices and upstream license retained in THIRD\_PARTY\_NOTICES; dabura667 / The Monero Project and original dictionary contributors.
- Распространение в репозитории: allowed
- Совместимость с SignPath: compatible
- Доказательства лицензии: [monero-eo-source](../catalog/evidence/monero-eo-source.json), [monero-monero-license](../catalog/evidence/monero-monero-license.json), [monero-osi-bsd](../catalog/evidence/monero-osi-bsd.json), [monero-signpath](../catalog/evidence/monero-signpath.json)
- Тестовые векторы: —

<a id="dictionary-monero-es"></a>

### monero-es — monero-es

- Исходная запись: [monero-es](../catalog/dictionaries/monero-es.json)
- Статус: documented
- Причина: Доказательств недостаточно для доступной поддержки.
- Рекомендация: Недоступно для выбора; используйте процедуру резервного копирования самого кошелька.
- Диапазон версий (min / max): 2f9d1bbb2c553dc75f3335bd1452117dfddd86fa / 2f9d1bbb2c553dc75f3335bd1452117dfddd86fa
- Дата проверки: 2026-09-29
- Историческая запись: false
- Доказательства: [monero-es-source](../catalog/evidence/monero-es-source.json), [monero-monero-license](../catalog/evidence/monero-monero-license.json), [monero-monero-rules](../catalog/evidence/monero-monero-rules.json), [monero-osi-bsd](../catalog/evidence/monero-osi-bsd.json), [monero-osi-mit](../catalog/evidence/monero-osi-mit.json), [monero-signpath](../catalog/evidence/monero-signpath.json)
- Подтверждаемое утверждение: Exact ordered dictionary array and applicable file-level license header reviewed. Source-token extraction and byte hashes are independently checked against the public fixture; no complete phrase is stored here. Reviewed 2026-09-29; response byte SHA-256 994a941260f53e066753204f4b92c20bb1d830b58e76ff89c2caa71c34d546ef. See docs/research/batches/monero-polyseed.md.
- Подтверждаемое утверждение: BSD-3-Clause source-data redistribution allowed with exact copyright/license/disclaimer retention and no endorsement. File-level MIT overrides for dabura667 lists retained. Reviewed by Codex for this source-data payload only. Reviewed 2026-09-29; response byte SHA-256 1f99d6b6e1ae17de27147ff2e1e0238fa8c7d5a8accd0f1ac062c89365516abd. See docs/research/batches/monero-polyseed.md.
- Подтверждаемое утверждение: 1626 entries; codepoint prefixes and case-insensitive lookup. utf8canonical re-encodes codepoints with towlower, not NFC/NFKD. EnglishOld tolerates duplicate prefixes and short words. Reviewed 2026-09-29; response byte SHA-256 2bc256f01c6904af914cb7c6526254267ed463882e216fd0eb1d9bbdf4bf5bb4. See docs/research/batches/monero-polyseed.md.
- Подтверждаемое утверждение: OSI lists BSD-3-Clause as approved. This corroborates only the component-license decision, not project acceptance. Response-body SHA-256 0dfece33194f06d15b862c323f7ed32ba6ab7f512a7fda11880bb2e1401518f8.
- Подтверждаемое утверждение: OSI identifies MIT as an approved open-source license; this corroborates the local component assessment, while the pinned reference repository license supplies the actual permission. Reviewed 2026-09-29; byte SHA-256 004c79db0a335488afc87600d89f447dce7fb4d24d510af15ed4381a24be848c. See docs/research/batches/bip39-ton.md. Same-day review reused from Task 10; corroborates MIT file-level scope for these lists only.
- Подтверждаемое утверждение: Codex component assessment\: reviewed BSD-3-Clause/MIT and Apache-2.0\+MIT data licenses are OSI-approved and impose no commercial dual-licensing; notices are retained. Compatible for this data-only payload. Foundation acceptance, project eligibility and release signing remain unproven. Response-body SHA-256 6610cf889bbe0dc7533abaa310bc7a5cc9a61ae6c2ce0798a08109c925b46c51.
- Язык: es
- Письменность: Latn
- Кодировка: UTF-8
- Нормализация: none
- Количество слов: 1626
- SHA-256: 05da8a20ae4a5af8fc1bd02d20d1282cf72ce1a6c98b9be60b1eff4c79d424fb
- Порядок слов: Exact upstream array order; zero-based indices. Extract literal UTF-8 tokens unchanged; remove C/C\+\+ wrapper and indentation, append LF after every token. No sorting, lowercasing or Unicode rewriting. Source file and extracted byte hashes in batch note.
- Позиционные правила: Same vocabulary at every eligible position; upstream prefix length 4. Never evaluate a user phrase checksum.; Source-native lookup\: Unicode codepoint lowercase and language-specific prefix, with no NFC/NFKD transform; normalization=none preserves source characters.; Language coverage is not a wallet generation claim.
- Ревизия источника: 2f9d1bbb2c553dc75f3335bd1452117dfddd86fa
- Лицензия: MIT
- Атрибуция: Exact source file notices and upstream license retained in THIRD\_PARTY\_NOTICES; dabura667 / The Monero Project and original dictionary contributors.
- Распространение в репозитории: allowed
- Совместимость с SignPath: compatible
- Доказательства лицензии: [monero-es-source](../catalog/evidence/monero-es-source.json), [monero-monero-license](../catalog/evidence/monero-monero-license.json), [monero-osi-bsd](../catalog/evidence/monero-osi-bsd.json), [monero-osi-mit](../catalog/evidence/monero-osi-mit.json), [monero-signpath](../catalog/evidence/monero-signpath.json)
- Тестовые векторы: —

<a id="dictionary-monero-fr"></a>

### monero-fr — monero-fr

- Исходная запись: [monero-fr](../catalog/dictionaries/monero-fr.json)
- Статус: documented
- Причина: Доказательств недостаточно для доступной поддержки.
- Рекомендация: Недоступно для выбора; используйте процедуру резервного копирования самого кошелька.
- Диапазон версий (min / max): 2f9d1bbb2c553dc75f3335bd1452117dfddd86fa / 2f9d1bbb2c553dc75f3335bd1452117dfddd86fa
- Дата проверки: 2026-09-29
- Историческая запись: false
- Доказательства: [monero-fr-source](../catalog/evidence/monero-fr-source.json), [monero-monero-license](../catalog/evidence/monero-monero-license.json), [monero-monero-rules](../catalog/evidence/monero-monero-rules.json), [monero-osi-bsd](../catalog/evidence/monero-osi-bsd.json), [monero-signpath](../catalog/evidence/monero-signpath.json)
- Подтверждаемое утверждение: Exact ordered dictionary array and applicable file-level license header reviewed. Source-token extraction and byte hashes are independently checked against the public fixture; no complete phrase is stored here. Reviewed 2026-09-29; response byte SHA-256 f4e42ab4eb9824a2cd829f132e33dfc46ae31c5788a37c9726d393e7cc809a82. See docs/research/batches/monero-polyseed.md.
- Подтверждаемое утверждение: BSD-3-Clause source-data redistribution allowed with exact copyright/license/disclaimer retention and no endorsement. File-level MIT overrides for dabura667 lists retained. Reviewed by Codex for this source-data payload only. Reviewed 2026-09-29; response byte SHA-256 1f99d6b6e1ae17de27147ff2e1e0238fa8c7d5a8accd0f1ac062c89365516abd. See docs/research/batches/monero-polyseed.md.
- Подтверждаемое утверждение: 1626 entries; codepoint prefixes and case-insensitive lookup. utf8canonical re-encodes codepoints with towlower, not NFC/NFKD. EnglishOld tolerates duplicate prefixes and short words. Reviewed 2026-09-29; response byte SHA-256 2bc256f01c6904af914cb7c6526254267ed463882e216fd0eb1d9bbdf4bf5bb4. See docs/research/batches/monero-polyseed.md.
- Подтверждаемое утверждение: OSI lists BSD-3-Clause as approved. This corroborates only the component-license decision, not project acceptance. Response-body SHA-256 0dfece33194f06d15b862c323f7ed32ba6ab7f512a7fda11880bb2e1401518f8.
- Подтверждаемое утверждение: Codex component assessment\: reviewed BSD-3-Clause/MIT and Apache-2.0\+MIT data licenses are OSI-approved and impose no commercial dual-licensing; notices are retained. Compatible for this data-only payload. Foundation acceptance, project eligibility and release signing remain unproven. Response-body SHA-256 6610cf889bbe0dc7533abaa310bc7a5cc9a61ae6c2ce0798a08109c925b46c51.
- Язык: fr
- Письменность: Latn
- Кодировка: UTF-8
- Нормализация: none
- Количество слов: 1626
- SHA-256: b17376bb1341cc32b8a7088d23c0dba3b25743c167f4e4f3d8062946ffd93e87
- Порядок слов: Exact upstream array order; zero-based indices. Extract literal UTF-8 tokens unchanged; remove C/C\+\+ wrapper and indentation, append LF after every token. No sorting, lowercasing or Unicode rewriting. Source file and extracted byte hashes in batch note.
- Позиционные правила: Same vocabulary at every eligible position; upstream prefix length 4. Never evaluate a user phrase checksum.; Source-native lookup\: Unicode codepoint lowercase and language-specific prefix, with no NFC/NFKD transform; normalization=none preserves source characters.; Language coverage is not a wallet generation claim.
- Ревизия источника: 2f9d1bbb2c553dc75f3335bd1452117dfddd86fa
- Лицензия: BSD-3-Clause
- Атрибуция: Exact source file notices and upstream license retained in THIRD\_PARTY\_NOTICES; dabura667 / The Monero Project and original dictionary contributors.
- Распространение в репозитории: allowed
- Совместимость с SignPath: compatible
- Доказательства лицензии: [monero-fr-source](../catalog/evidence/monero-fr-source.json), [monero-monero-license](../catalog/evidence/monero-monero-license.json), [monero-osi-bsd](../catalog/evidence/monero-osi-bsd.json), [monero-signpath](../catalog/evidence/monero-signpath.json)
- Тестовые векторы: —

<a id="dictionary-monero-it"></a>

### monero-it — monero-it

- Исходная запись: [monero-it](../catalog/dictionaries/monero-it.json)
- Статус: documented
- Причина: Доказательств недостаточно для доступной поддержки.
- Рекомендация: Недоступно для выбора; используйте процедуру резервного копирования самого кошелька.
- Диапазон версий (min / max): 2f9d1bbb2c553dc75f3335bd1452117dfddd86fa / 2f9d1bbb2c553dc75f3335bd1452117dfddd86fa
- Дата проверки: 2026-09-29
- Историческая запись: false
- Доказательства: [monero-it-source](../catalog/evidence/monero-it-source.json), [monero-monero-license](../catalog/evidence/monero-monero-license.json), [monero-monero-rules](../catalog/evidence/monero-monero-rules.json), [monero-osi-bsd](../catalog/evidence/monero-osi-bsd.json), [monero-signpath](../catalog/evidence/monero-signpath.json)
- Подтверждаемое утверждение: Exact ordered dictionary array and applicable file-level license header reviewed. Source-token extraction and byte hashes are independently checked against the public fixture; no complete phrase is stored here. Reviewed 2026-09-29; response byte SHA-256 d02956b528db827646a1f6f78c1a19716b9334985cb893eb09409834a04045db. See docs/research/batches/monero-polyseed.md.
- Подтверждаемое утверждение: BSD-3-Clause source-data redistribution allowed with exact copyright/license/disclaimer retention and no endorsement. File-level MIT overrides for dabura667 lists retained. Reviewed by Codex for this source-data payload only. Reviewed 2026-09-29; response byte SHA-256 1f99d6b6e1ae17de27147ff2e1e0238fa8c7d5a8accd0f1ac062c89365516abd. See docs/research/batches/monero-polyseed.md.
- Подтверждаемое утверждение: 1626 entries; codepoint prefixes and case-insensitive lookup. utf8canonical re-encodes codepoints with towlower, not NFC/NFKD. EnglishOld tolerates duplicate prefixes and short words. Reviewed 2026-09-29; response byte SHA-256 2bc256f01c6904af914cb7c6526254267ed463882e216fd0eb1d9bbdf4bf5bb4. See docs/research/batches/monero-polyseed.md.
- Подтверждаемое утверждение: OSI lists BSD-3-Clause as approved. This corroborates only the component-license decision, not project acceptance. Response-body SHA-256 0dfece33194f06d15b862c323f7ed32ba6ab7f512a7fda11880bb2e1401518f8.
- Подтверждаемое утверждение: Codex component assessment\: reviewed BSD-3-Clause/MIT and Apache-2.0\+MIT data licenses are OSI-approved and impose no commercial dual-licensing; notices are retained. Compatible for this data-only payload. Foundation acceptance, project eligibility and release signing remain unproven. Response-body SHA-256 6610cf889bbe0dc7533abaa310bc7a5cc9a61ae6c2ce0798a08109c925b46c51.
- Язык: it
- Письменность: Latn
- Кодировка: UTF-8
- Нормализация: none
- Количество слов: 1626
- SHA-256: aea041cbb43e8e3b817b48b64001df3e28949002d99c920a8a46231319bcc121
- Порядок слов: Exact upstream array order; zero-based indices. Extract literal UTF-8 tokens unchanged; remove C/C\+\+ wrapper and indentation, append LF after every token. No sorting, lowercasing or Unicode rewriting. Source file and extracted byte hashes in batch note.
- Позиционные правила: Same vocabulary at every eligible position; upstream prefix length 4. Never evaluate a user phrase checksum.; Source-native lookup\: Unicode codepoint lowercase and language-specific prefix, with no NFC/NFKD transform; normalization=none preserves source characters.; Language coverage is not a wallet generation claim.
- Ревизия источника: 2f9d1bbb2c553dc75f3335bd1452117dfddd86fa
- Лицензия: BSD-3-Clause
- Атрибуция: Exact source file notices and upstream license retained in THIRD\_PARTY\_NOTICES; dabura667 / The Monero Project and original dictionary contributors.
- Распространение в репозитории: allowed
- Совместимость с SignPath: compatible
- Доказательства лицензии: [monero-it-source](../catalog/evidence/monero-it-source.json), [monero-monero-license](../catalog/evidence/monero-monero-license.json), [monero-osi-bsd](../catalog/evidence/monero-osi-bsd.json), [monero-signpath](../catalog/evidence/monero-signpath.json)
- Тестовые векторы: —

<a id="dictionary-monero-ja"></a>

### monero-ja — monero-ja

- Исходная запись: [monero-ja](../catalog/dictionaries/monero-ja.json)
- Статус: documented
- Причина: Доказательств недостаточно для доступной поддержки.
- Рекомендация: Недоступно для выбора; используйте процедуру резервного копирования самого кошелька.
- Диапазон версий (min / max): 2f9d1bbb2c553dc75f3335bd1452117dfddd86fa / 2f9d1bbb2c553dc75f3335bd1452117dfddd86fa
- Дата проверки: 2026-09-29
- Историческая запись: false
- Доказательства: [monero-ja-source](../catalog/evidence/monero-ja-source.json), [monero-monero-license](../catalog/evidence/monero-monero-license.json), [monero-monero-rules](../catalog/evidence/monero-monero-rules.json), [monero-osi-bsd](../catalog/evidence/monero-osi-bsd.json), [monero-osi-mit](../catalog/evidence/monero-osi-mit.json), [monero-signpath](../catalog/evidence/monero-signpath.json)
- Подтверждаемое утверждение: Exact ordered dictionary array and applicable file-level license header reviewed. Source-token extraction and byte hashes are independently checked against the public fixture; no complete phrase is stored here. Reviewed 2026-09-29; response byte SHA-256 3701f067006b60e95e266e7a385b472c5bddeb6f476e737eed6d3b7febefe6d5. See docs/research/batches/monero-polyseed.md.
- Подтверждаемое утверждение: BSD-3-Clause source-data redistribution allowed with exact copyright/license/disclaimer retention and no endorsement. File-level MIT overrides for dabura667 lists retained. Reviewed by Codex for this source-data payload only. Reviewed 2026-09-29; response byte SHA-256 1f99d6b6e1ae17de27147ff2e1e0238fa8c7d5a8accd0f1ac062c89365516abd. See docs/research/batches/monero-polyseed.md.
- Подтверждаемое утверждение: 1626 entries; codepoint prefixes and case-insensitive lookup. utf8canonical re-encodes codepoints with towlower, not NFC/NFKD. EnglishOld tolerates duplicate prefixes and short words. Reviewed 2026-09-29; response byte SHA-256 2bc256f01c6904af914cb7c6526254267ed463882e216fd0eb1d9bbdf4bf5bb4. See docs/research/batches/monero-polyseed.md.
- Подтверждаемое утверждение: OSI lists BSD-3-Clause as approved. This corroborates only the component-license decision, not project acceptance. Response-body SHA-256 0dfece33194f06d15b862c323f7ed32ba6ab7f512a7fda11880bb2e1401518f8.
- Подтверждаемое утверждение: OSI identifies MIT as an approved open-source license; this corroborates the local component assessment, while the pinned reference repository license supplies the actual permission. Reviewed 2026-09-29; byte SHA-256 004c79db0a335488afc87600d89f447dce7fb4d24d510af15ed4381a24be848c. See docs/research/batches/bip39-ton.md. Same-day review reused from Task 10; corroborates MIT file-level scope for these lists only.
- Подтверждаемое утверждение: Codex component assessment\: reviewed BSD-3-Clause/MIT and Apache-2.0\+MIT data licenses are OSI-approved and impose no commercial dual-licensing; notices are retained. Compatible for this data-only payload. Foundation acceptance, project eligibility and release signing remain unproven. Response-body SHA-256 6610cf889bbe0dc7533abaa310bc7a5cc9a61ae6c2ce0798a08109c925b46c51.
- Язык: ja
- Письменность: Jpan
- Кодировка: UTF-8
- Нормализация: none
- Количество слов: 1626
- SHA-256: 0e879f11f3806e6b25738598cfec6f372364af7fb8c59b4874d7a406f6b0fee7
- Порядок слов: Exact upstream array order; zero-based indices. Extract literal UTF-8 tokens unchanged; remove C/C\+\+ wrapper and indentation, append LF after every token. No sorting, lowercasing or Unicode rewriting. Source file and extracted byte hashes in batch note.
- Позиционные правила: Same vocabulary at every eligible position; upstream prefix length 3. Never evaluate a user phrase checksum.; Source-native lookup\: Unicode codepoint lowercase and language-specific prefix, with no NFC/NFKD transform; normalization=none preserves source characters.; Language coverage is not a wallet generation claim.
- Ревизия источника: 2f9d1bbb2c553dc75f3335bd1452117dfddd86fa
- Лицензия: MIT
- Атрибуция: Exact source file notices and upstream license retained in THIRD\_PARTY\_NOTICES; dabura667 / The Monero Project and original dictionary contributors.
- Распространение в репозитории: allowed
- Совместимость с SignPath: compatible
- Доказательства лицензии: [monero-ja-source](../catalog/evidence/monero-ja-source.json), [monero-monero-license](../catalog/evidence/monero-monero-license.json), [monero-osi-bsd](../catalog/evidence/monero-osi-bsd.json), [monero-osi-mit](../catalog/evidence/monero-osi-mit.json), [monero-signpath](../catalog/evidence/monero-signpath.json)
- Тестовые векторы: —

<a id="dictionary-monero-jbo"></a>

### monero-jbo — monero-jbo

- Исходная запись: [monero-jbo](../catalog/dictionaries/monero-jbo.json)
- Статус: documented
- Причина: Доказательств недостаточно для доступной поддержки.
- Рекомендация: Недоступно для выбора; используйте процедуру резервного копирования самого кошелька.
- Диапазон версий (min / max): 2f9d1bbb2c553dc75f3335bd1452117dfddd86fa / 2f9d1bbb2c553dc75f3335bd1452117dfddd86fa
- Дата проверки: 2026-09-29
- Историческая запись: false
- Доказательства: [monero-jbo-source](../catalog/evidence/monero-jbo-source.json), [monero-monero-license](../catalog/evidence/monero-monero-license.json), [monero-monero-rules](../catalog/evidence/monero-monero-rules.json), [monero-osi-bsd](../catalog/evidence/monero-osi-bsd.json), [monero-signpath](../catalog/evidence/monero-signpath.json)
- Подтверждаемое утверждение: Exact ordered dictionary array and applicable file-level license header reviewed. Source-token extraction and byte hashes are independently checked against the public fixture; no complete phrase is stored here. Reviewed 2026-09-29; response byte SHA-256 6c84dedd2609060f30368b92b5e377207e28afcda5401b5060d57c633e623a04. See docs/research/batches/monero-polyseed.md.
- Подтверждаемое утверждение: BSD-3-Clause source-data redistribution allowed with exact copyright/license/disclaimer retention and no endorsement. File-level MIT overrides for dabura667 lists retained. Reviewed by Codex for this source-data payload only. Reviewed 2026-09-29; response byte SHA-256 1f99d6b6e1ae17de27147ff2e1e0238fa8c7d5a8accd0f1ac062c89365516abd. See docs/research/batches/monero-polyseed.md.
- Подтверждаемое утверждение: 1626 entries; codepoint prefixes and case-insensitive lookup. utf8canonical re-encodes codepoints with towlower, not NFC/NFKD. EnglishOld tolerates duplicate prefixes and short words. Reviewed 2026-09-29; response byte SHA-256 2bc256f01c6904af914cb7c6526254267ed463882e216fd0eb1d9bbdf4bf5bb4. See docs/research/batches/monero-polyseed.md.
- Подтверждаемое утверждение: OSI lists BSD-3-Clause as approved. This corroborates only the component-license decision, not project acceptance. Response-body SHA-256 0dfece33194f06d15b862c323f7ed32ba6ab7f512a7fda11880bb2e1401518f8.
- Подтверждаемое утверждение: Codex component assessment\: reviewed BSD-3-Clause/MIT and Apache-2.0\+MIT data licenses are OSI-approved and impose no commercial dual-licensing; notices are retained. Compatible for this data-only payload. Foundation acceptance, project eligibility and release signing remain unproven. Response-body SHA-256 6610cf889bbe0dc7533abaa310bc7a5cc9a61ae6c2ce0798a08109c925b46c51.
- Язык: jbo
- Письменность: Latn
- Кодировка: UTF-8
- Нормализация: none
- Количество слов: 1626
- SHA-256: 19c3f71b26c808bbe9ed7ab944ac1c8b1f11307f96d27d01874c093520c972f9
- Порядок слов: Exact upstream array order; zero-based indices. Extract literal UTF-8 tokens unchanged; remove C/C\+\+ wrapper and indentation, append LF after every token. No sorting, lowercasing or Unicode rewriting. Source file and extracted byte hashes in batch note.
- Позиционные правила: Same vocabulary at every eligible position; upstream prefix length 4. Never evaluate a user phrase checksum.; Source-native lookup\: Unicode codepoint lowercase and language-specific prefix, with no NFC/NFKD transform; normalization=none preserves source characters.; Language coverage is not a wallet generation claim.
- Ревизия источника: 2f9d1bbb2c553dc75f3335bd1452117dfddd86fa
- Лицензия: BSD-3-Clause
- Атрибуция: Exact source file notices and upstream license retained in THIRD\_PARTY\_NOTICES; dabura667 / The Monero Project and original dictionary contributors.
- Распространение в репозитории: allowed
- Совместимость с SignPath: compatible
- Доказательства лицензии: [monero-jbo-source](../catalog/evidence/monero-jbo-source.json), [monero-monero-license](../catalog/evidence/monero-monero-license.json), [monero-osi-bsd](../catalog/evidence/monero-osi-bsd.json), [monero-signpath](../catalog/evidence/monero-signpath.json)
- Тестовые векторы: —

<a id="dictionary-monero-nl"></a>

### monero-nl — monero-nl

- Исходная запись: [monero-nl](../catalog/dictionaries/monero-nl.json)
- Статус: documented
- Причина: Доказательств недостаточно для доступной поддержки.
- Рекомендация: Недоступно для выбора; используйте процедуру резервного копирования самого кошелька.
- Диапазон версий (min / max): 2f9d1bbb2c553dc75f3335bd1452117dfddd86fa / 2f9d1bbb2c553dc75f3335bd1452117dfddd86fa
- Дата проверки: 2026-09-29
- Историческая запись: false
- Доказательства: [monero-monero-license](../catalog/evidence/monero-monero-license.json), [monero-monero-rules](../catalog/evidence/monero-monero-rules.json), [monero-nl-source](../catalog/evidence/monero-nl-source.json), [monero-osi-bsd](../catalog/evidence/monero-osi-bsd.json), [monero-signpath](../catalog/evidence/monero-signpath.json)
- Подтверждаемое утверждение: BSD-3-Clause source-data redistribution allowed with exact copyright/license/disclaimer retention and no endorsement. File-level MIT overrides for dabura667 lists retained. Reviewed by Codex for this source-data payload only. Reviewed 2026-09-29; response byte SHA-256 1f99d6b6e1ae17de27147ff2e1e0238fa8c7d5a8accd0f1ac062c89365516abd. See docs/research/batches/monero-polyseed.md.
- Подтверждаемое утверждение: 1626 entries; codepoint prefixes and case-insensitive lookup. utf8canonical re-encodes codepoints with towlower, not NFC/NFKD. EnglishOld tolerates duplicate prefixes and short words. Reviewed 2026-09-29; response byte SHA-256 2bc256f01c6904af914cb7c6526254267ed463882e216fd0eb1d9bbdf4bf5bb4. See docs/research/batches/monero-polyseed.md.
- Подтверждаемое утверждение: Exact ordered dictionary array and applicable file-level license header reviewed. Source-token extraction and byte hashes are independently checked against the public fixture; no complete phrase is stored here. Reviewed 2026-09-29; response byte SHA-256 775d05f737f453d6798876d99961bb3bcfc49d47cb57860d3c0b2a03b9a64822. See docs/research/batches/monero-polyseed.md.
- Подтверждаемое утверждение: OSI lists BSD-3-Clause as approved. This corroborates only the component-license decision, not project acceptance. Response-body SHA-256 0dfece33194f06d15b862c323f7ed32ba6ab7f512a7fda11880bb2e1401518f8.
- Подтверждаемое утверждение: Codex component assessment\: reviewed BSD-3-Clause/MIT and Apache-2.0\+MIT data licenses are OSI-approved and impose no commercial dual-licensing; notices are retained. Compatible for this data-only payload. Foundation acceptance, project eligibility and release signing remain unproven. Response-body SHA-256 6610cf889bbe0dc7533abaa310bc7a5cc9a61ae6c2ce0798a08109c925b46c51.
- Язык: nl
- Письменность: Latn
- Кодировка: UTF-8
- Нормализация: none
- Количество слов: 1626
- SHA-256: 9b2005b2c4d95360361949c7f5b43ef6a021d3ce31f01f6101a24d93540e790a
- Порядок слов: Exact upstream array order; zero-based indices. Extract literal UTF-8 tokens unchanged; remove C/C\+\+ wrapper and indentation, append LF after every token. No sorting, lowercasing or Unicode rewriting. Source file and extracted byte hashes in batch note.
- Позиционные правила: Same vocabulary at every eligible position; upstream prefix length 4. Never evaluate a user phrase checksum.; Source-native lookup\: Unicode codepoint lowercase and language-specific prefix, with no NFC/NFKD transform; normalization=none preserves source characters.; Language coverage is not a wallet generation claim.
- Ревизия источника: 2f9d1bbb2c553dc75f3335bd1452117dfddd86fa
- Лицензия: BSD-3-Clause
- Атрибуция: Exact source file notices and upstream license retained in THIRD\_PARTY\_NOTICES; dabura667 / The Monero Project and original dictionary contributors.
- Распространение в репозитории: allowed
- Совместимость с SignPath: compatible
- Доказательства лицензии: [monero-monero-license](../catalog/evidence/monero-monero-license.json), [monero-nl-source](../catalog/evidence/monero-nl-source.json), [monero-osi-bsd](../catalog/evidence/monero-osi-bsd.json), [monero-signpath](../catalog/evidence/monero-signpath.json)
- Тестовые векторы: —

<a id="dictionary-monero-pt"></a>

### monero-pt — monero-pt

- Исходная запись: [monero-pt](../catalog/dictionaries/monero-pt.json)
- Статус: verified
- Причина: Проверенная исследовательская запись; не гарантия релиза или безопасности.
- Диапазон версий (min / max): 2f9d1bbb2c553dc75f3335bd1452117dfddd86fa / 2f9d1bbb2c553dc75f3335bd1452117dfddd86fa
- Дата проверки: 2026-09-29
- Историческая запись: false
- Доказательства: [monero-legacy-vectors](../catalog/evidence/monero-legacy-vectors.json), [monero-monero-license](../catalog/evidence/monero-monero-license.json), [monero-monero-rules](../catalog/evidence/monero-monero-rules.json), [monero-osi-bsd](../catalog/evidence/monero-osi-bsd.json), [monero-osi-mit](../catalog/evidence/monero-osi-mit.json), [monero-pt-source](../catalog/evidence/monero-pt-source.json), [monero-signpath](../catalog/evidence/monero-signpath.json)
- Подтверждаемое утверждение: Public Portuguese checksum and German case-tolerance examples; projection stores dictionary indices and expected phrase fingerprint. Offline test reproduces source CRC32 prefix check, not private-key/address derivation. Reviewed 2026-09-29; response byte SHA-256 520fec49e96e4b01d472f627e109b7a343f80e58291eed793f7ca76f2e63a1d1. See docs/research/batches/monero-polyseed.md.
- Подтверждаемое утверждение: BSD-3-Clause source-data redistribution allowed with exact copyright/license/disclaimer retention and no endorsement. File-level MIT overrides for dabura667 lists retained. Reviewed by Codex for this source-data payload only. Reviewed 2026-09-29; response byte SHA-256 1f99d6b6e1ae17de27147ff2e1e0238fa8c7d5a8accd0f1ac062c89365516abd. See docs/research/batches/monero-polyseed.md.
- Подтверждаемое утверждение: 1626 entries; codepoint prefixes and case-insensitive lookup. utf8canonical re-encodes codepoints with towlower, not NFC/NFKD. EnglishOld tolerates duplicate prefixes and short words. Reviewed 2026-09-29; response byte SHA-256 2bc256f01c6904af914cb7c6526254267ed463882e216fd0eb1d9bbdf4bf5bb4. See docs/research/batches/monero-polyseed.md.
- Подтверждаемое утверждение: OSI lists BSD-3-Clause as approved. This corroborates only the component-license decision, not project acceptance. Response-body SHA-256 0dfece33194f06d15b862c323f7ed32ba6ab7f512a7fda11880bb2e1401518f8.
- Подтверждаемое утверждение: OSI identifies MIT as an approved open-source license; this corroborates the local component assessment, while the pinned reference repository license supplies the actual permission. Reviewed 2026-09-29; byte SHA-256 004c79db0a335488afc87600d89f447dce7fb4d24d510af15ed4381a24be848c. See docs/research/batches/bip39-ton.md. Same-day review reused from Task 10; corroborates MIT file-level scope for these lists only.
- Подтверждаемое утверждение: Exact ordered dictionary array and applicable file-level license header reviewed. Source-token extraction and byte hashes are independently checked against the public fixture; no complete phrase is stored here. Reviewed 2026-09-29; response byte SHA-256 0a6b191930a29f1ae827c1f5f8905548035bac5e5b41386f0978cf39e4adcfa1. See docs/research/batches/monero-polyseed.md.
- Подтверждаемое утверждение: Codex component assessment\: reviewed BSD-3-Clause/MIT and Apache-2.0\+MIT data licenses are OSI-approved and impose no commercial dual-licensing; notices are retained. Compatible for this data-only payload. Foundation acceptance, project eligibility and release signing remain unproven. Response-body SHA-256 6610cf889bbe0dc7533abaa310bc7a5cc9a61ae6c2ce0798a08109c925b46c51.
- Язык: pt
- Письменность: Latn
- Кодировка: UTF-8
- Нормализация: none
- Количество слов: 1626
- SHA-256: 9099aaa5470c568ca91f0040222760af55720ddc3f3a6f9e1736d4c2dd9247da
- Порядок слов: Exact upstream array order; zero-based indices. Extract literal UTF-8 tokens unchanged; remove C/C\+\+ wrapper and indentation, append LF after every token. No sorting, lowercasing or Unicode rewriting. Source file and extracted byte hashes in batch note.
- Позиционные правила: Same vocabulary at every eligible position; upstream prefix length 4. Never evaluate a user phrase checksum.; Source-native lookup\: Unicode codepoint lowercase and language-specific prefix, with no NFC/NFKD transform; normalization=none preserves source characters.; Language coverage is not a wallet generation claim.
- Ревизия источника: 2f9d1bbb2c553dc75f3335bd1452117dfddd86fa
- Лицензия: MIT
- Атрибуция: Exact source file notices and upstream license retained in THIRD\_PARTY\_NOTICES; dabura667 / The Monero Project and original dictionary contributors.
- Распространение в репозитории: allowed
- Совместимость с SignPath: compatible
- Доказательства лицензии: [monero-monero-license](../catalog/evidence/monero-monero-license.json), [monero-osi-bsd](../catalog/evidence/monero-osi-bsd.json), [monero-osi-mit](../catalog/evidence/monero-osi-mit.json), [monero-pt-source](../catalog/evidence/monero-pt-source.json), [monero-signpath](../catalog/evidence/monero-signpath.json)
- Тестовые векторы: [monero-legacy-vectors](../catalog/evidence/monero-legacy-vectors.json)

<a id="dictionary-monero-ru"></a>

### monero-ru — monero-ru

- Исходная запись: [monero-ru](../catalog/dictionaries/monero-ru.json)
- Статус: documented
- Причина: Доказательств недостаточно для доступной поддержки.
- Рекомендация: Недоступно для выбора; используйте процедуру резервного копирования самого кошелька.
- Диапазон версий (min / max): 2f9d1bbb2c553dc75f3335bd1452117dfddd86fa / 2f9d1bbb2c553dc75f3335bd1452117dfddd86fa
- Дата проверки: 2026-09-29
- Историческая запись: false
- Доказательства: [monero-monero-license](../catalog/evidence/monero-monero-license.json), [monero-monero-rules](../catalog/evidence/monero-monero-rules.json), [monero-osi-bsd](../catalog/evidence/monero-osi-bsd.json), [monero-ru-source](../catalog/evidence/monero-ru-source.json), [monero-signpath](../catalog/evidence/monero-signpath.json)
- Подтверждаемое утверждение: BSD-3-Clause source-data redistribution allowed with exact copyright/license/disclaimer retention and no endorsement. File-level MIT overrides for dabura667 lists retained. Reviewed by Codex for this source-data payload only. Reviewed 2026-09-29; response byte SHA-256 1f99d6b6e1ae17de27147ff2e1e0238fa8c7d5a8accd0f1ac062c89365516abd. See docs/research/batches/monero-polyseed.md.
- Подтверждаемое утверждение: 1626 entries; codepoint prefixes and case-insensitive lookup. utf8canonical re-encodes codepoints with towlower, not NFC/NFKD. EnglishOld tolerates duplicate prefixes and short words. Reviewed 2026-09-29; response byte SHA-256 2bc256f01c6904af914cb7c6526254267ed463882e216fd0eb1d9bbdf4bf5bb4. See docs/research/batches/monero-polyseed.md.
- Подтверждаемое утверждение: OSI lists BSD-3-Clause as approved. This corroborates only the component-license decision, not project acceptance. Response-body SHA-256 0dfece33194f06d15b862c323f7ed32ba6ab7f512a7fda11880bb2e1401518f8.
- Подтверждаемое утверждение: Exact ordered dictionary array and applicable file-level license header reviewed. Source-token extraction and byte hashes are independently checked against the public fixture; no complete phrase is stored here. Reviewed 2026-09-29; response byte SHA-256 2d3f282d11e917fcdd6248b87002f5b982b6abaa773e9676d21886b6a50a4762. See docs/research/batches/monero-polyseed.md.
- Подтверждаемое утверждение: Codex component assessment\: reviewed BSD-3-Clause/MIT and Apache-2.0\+MIT data licenses are OSI-approved and impose no commercial dual-licensing; notices are retained. Compatible for this data-only payload. Foundation acceptance, project eligibility and release signing remain unproven. Response-body SHA-256 6610cf889bbe0dc7533abaa310bc7a5cc9a61ae6c2ce0798a08109c925b46c51.
- Язык: ru
- Письменность: Cyrl
- Кодировка: UTF-8
- Нормализация: none
- Количество слов: 1626
- SHA-256: fd225689dda9d342acae6bd58ecbdba3274ded07d89936ce979a95f6d60c64ea
- Порядок слов: Exact upstream array order; zero-based indices. Extract literal UTF-8 tokens unchanged; remove C/C\+\+ wrapper and indentation, append LF after every token. No sorting, lowercasing or Unicode rewriting. Source file and extracted byte hashes in batch note.
- Позиционные правила: Same vocabulary at every eligible position; upstream prefix length 4. Never evaluate a user phrase checksum.; Source-native lookup\: Unicode codepoint lowercase and language-specific prefix, with no NFC/NFKD transform; normalization=none preserves source characters.; Language coverage is not a wallet generation claim.
- Ревизия источника: 2f9d1bbb2c553dc75f3335bd1452117dfddd86fa
- Лицензия: BSD-3-Clause
- Атрибуция: Exact source file notices and upstream license retained in THIRD\_PARTY\_NOTICES; dabura667 / The Monero Project and original dictionary contributors.
- Распространение в репозитории: allowed
- Совместимость с SignPath: compatible
- Доказательства лицензии: [monero-monero-license](../catalog/evidence/monero-monero-license.json), [monero-osi-bsd](../catalog/evidence/monero-osi-bsd.json), [monero-ru-source](../catalog/evidence/monero-ru-source.json), [monero-signpath](../catalog/evidence/monero-signpath.json)
- Тестовые векторы: —

<a id="dictionary-monero-zh-hans"></a>

### monero-zh-hans — monero-zh-hans

- Исходная запись: [monero-zh-hans](../catalog/dictionaries/monero-zh-hans.json)
- Статус: documented
- Причина: Доказательств недостаточно для доступной поддержки.
- Рекомендация: Недоступно для выбора; используйте процедуру резервного копирования самого кошелька.
- Диапазон версий (min / max): 2f9d1bbb2c553dc75f3335bd1452117dfddd86fa / 2f9d1bbb2c553dc75f3335bd1452117dfddd86fa
- Дата проверки: 2026-09-29
- Историческая запись: false
- Доказательства: [monero-monero-license](../catalog/evidence/monero-monero-license.json), [monero-monero-rules](../catalog/evidence/monero-monero-rules.json), [monero-osi-bsd](../catalog/evidence/monero-osi-bsd.json), [monero-osi-mit](../catalog/evidence/monero-osi-mit.json), [monero-signpath](../catalog/evidence/monero-signpath.json), [monero-zh-hans-source](../catalog/evidence/monero-zh-hans-source.json)
- Подтверждаемое утверждение: BSD-3-Clause source-data redistribution allowed with exact copyright/license/disclaimer retention and no endorsement. File-level MIT overrides for dabura667 lists retained. Reviewed by Codex for this source-data payload only. Reviewed 2026-09-29; response byte SHA-256 1f99d6b6e1ae17de27147ff2e1e0238fa8c7d5a8accd0f1ac062c89365516abd. See docs/research/batches/monero-polyseed.md.
- Подтверждаемое утверждение: 1626 entries; codepoint prefixes and case-insensitive lookup. utf8canonical re-encodes codepoints with towlower, not NFC/NFKD. EnglishOld tolerates duplicate prefixes and short words. Reviewed 2026-09-29; response byte SHA-256 2bc256f01c6904af914cb7c6526254267ed463882e216fd0eb1d9bbdf4bf5bb4. See docs/research/batches/monero-polyseed.md.
- Подтверждаемое утверждение: OSI lists BSD-3-Clause as approved. This corroborates only the component-license decision, not project acceptance. Response-body SHA-256 0dfece33194f06d15b862c323f7ed32ba6ab7f512a7fda11880bb2e1401518f8.
- Подтверждаемое утверждение: OSI identifies MIT as an approved open-source license; this corroborates the local component assessment, while the pinned reference repository license supplies the actual permission. Reviewed 2026-09-29; byte SHA-256 004c79db0a335488afc87600d89f447dce7fb4d24d510af15ed4381a24be848c. See docs/research/batches/bip39-ton.md. Same-day review reused from Task 10; corroborates MIT file-level scope for these lists only.
- Подтверждаемое утверждение: Codex component assessment\: reviewed BSD-3-Clause/MIT and Apache-2.0\+MIT data licenses are OSI-approved and impose no commercial dual-licensing; notices are retained. Compatible for this data-only payload. Foundation acceptance, project eligibility and release signing remain unproven. Response-body SHA-256 6610cf889bbe0dc7533abaa310bc7a5cc9a61ae6c2ce0798a08109c925b46c51.
- Подтверждаемое утверждение: Exact ordered dictionary array and applicable file-level license header reviewed. Source-token extraction and byte hashes are independently checked against the public fixture; no complete phrase is stored here. Reviewed 2026-09-29; response byte SHA-256 4a38fbe7279616aa78aa11dbcf425d0ba5305fd2089cb4421d544f2c540d50fd. See docs/research/batches/monero-polyseed.md.
- Язык: zh-hans
- Письменность: Hans
- Кодировка: UTF-8
- Нормализация: none
- Количество слов: 1626
- SHA-256: d0b846b2036f55182892d98c2410996c399ed3aee5be2d6cbfaf594e599dd522
- Порядок слов: Exact upstream array order; zero-based indices. Extract literal UTF-8 tokens unchanged; remove C/C\+\+ wrapper and indentation, append LF after every token. No sorting, lowercasing or Unicode rewriting. Source file and extracted byte hashes in batch note.
- Позиционные правила: Same vocabulary at every eligible position; upstream prefix length 1. Never evaluate a user phrase checksum.; Source-native lookup\: Unicode codepoint lowercase and language-specific prefix, with no NFC/NFKD transform; normalization=none preserves source characters.; Language coverage is not a wallet generation claim.
- Ревизия источника: 2f9d1bbb2c553dc75f3335bd1452117dfddd86fa
- Лицензия: MIT
- Атрибуция: Exact source file notices and upstream license retained in THIRD\_PARTY\_NOTICES; dabura667 / The Monero Project and original dictionary contributors.
- Распространение в репозитории: allowed
- Совместимость с SignPath: compatible
- Доказательства лицензии: [monero-monero-license](../catalog/evidence/monero-monero-license.json), [monero-osi-bsd](../catalog/evidence/monero-osi-bsd.json), [monero-osi-mit](../catalog/evidence/monero-osi-mit.json), [monero-signpath](../catalog/evidence/monero-signpath.json), [monero-zh-hans-source](../catalog/evidence/monero-zh-hans-source.json)
- Тестовые векторы: —

<a id="dictionary-polyseed-cs"></a>

### polyseed-cs — polyseed-cs

- Исходная запись: [polyseed-cs](../catalog/dictionaries/polyseed-cs.json)
- Статус: documented
- Причина: Доказательств недостаточно для доступной поддержки.
- Рекомендация: Недоступно для выбора; используйте процедуру резервного копирования самого кошелька.
- Диапазон версий (min / max): 56f634647d4f75596de20a6259b0cf1933949fdc / 56f634647d4f75596de20a6259b0cf1933949fdc
- Дата проверки: 2026-09-29
- Историческая запись: false
- Доказательства: [monero-osi-apache](../catalog/evidence/monero-osi-apache.json), [monero-polyseed-license](../catalog/evidence/monero-polyseed-license.json), [monero-polyseed-notice](../catalog/evidence/monero-polyseed-notice.json), [monero-polyseed-rules](../catalog/evidence/monero-polyseed-rules.json), [monero-signpath](../catalog/evidence/monero-signpath.json), [polyseed-cs-source](../catalog/evidence/polyseed-cs-source.json)
- Подтверждаемое утверждение: OSI lists Apache-2.0 as approved. This corroborates only the component-license decision, not project acceptance. Response-body SHA-256 1377faaaa81ba356528c4053d80e32fd12d84b794ed2667f09bf94aaca7458eb.
- Подтверждаемое утверждение: Apache-2.0 permits this modified source-data projection subject to license, notices and modification marking; root project LICENSE contains identical Apache text. No commercial dual-license requirement. Reviewed 2026-09-29; response byte SHA-256 cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30. See docs/research/batches/monero-polyseed.md.
- Подтверждаемое утверждение: Polyseed attribution and BIP39-derived dictionary MIT obligations apply cumulatively with Apache-2.0; complete upstream NOTICE retained in THIRD\_PARTY\_NOTICES. Reviewed 2026-09-29; response byte SHA-256 442cd16cdc8913cd76a9f7bd1047a0aea68ede782d94db3556392e18f39ad64e. See docs/research/batches/monero-polyseed.md.
- Подтверждаемое утверждение: Ten lists, NFKD word invariant, ordinal index lookup, language-dependent prefixes/accent handling; no BIP39 substitution. Reviewed 2026-09-29; response byte SHA-256 f30f867f5afd3bab323d85a8678868862d94dde09ed7801ab45a74f9b563b447. See docs/research/batches/monero-polyseed.md.
- Подтверждаемое утверждение: Codex component assessment\: reviewed BSD-3-Clause/MIT and Apache-2.0\+MIT data licenses are OSI-approved and impose no commercial dual-licensing; notices are retained. Compatible for this data-only payload. Foundation acceptance, project eligibility and release signing remain unproven. Response-body SHA-256 6610cf889bbe0dc7533abaa310bc7a5cc9a61ae6c2ce0798a08109c925b46c51.
- Подтверждаемое утверждение: Exact ordered dictionary array and applicable file-level license header reviewed. Source-token extraction and byte hashes are independently checked against the public fixture; no complete phrase is stored here. Reviewed 2026-09-29; response byte SHA-256 395c70fb0de3e4c9034da698c679269227c1783d0ae56617bb8bcfd950eb9cd3. See docs/research/batches/monero-polyseed.md.
- Язык: cs
- Письменность: Latn
- Кодировка: UTF-8
- Нормализация: NFKD
- Количество слов: 2048
- SHA-256: 195136b3ba0f3099a9df625e0963f4efb56625b91c3a76bc5b4a9466a26880f7
- Порядок слов: Exact upstream array order; zero-based indices. Extract literal UTF-8 tokens unchanged; remove C/C\+\+ wrapper and indentation, append LF after every token. No sorting, lowercasing or Unicode rewriting. Source file and extracted byte hashes in batch note.
- Позиционные правила: Same 2048-entry vocabulary at all 16 positions. First word is polynomial checksum; no BIP39 checksum semantics.; Input uses NFKD; output may compose NFC for accented/Japanese/Korean language flags. Latin prefix matching and French/Spanish accent-insensitivity are separate from stored NFKD bytes.; Language coverage is not a wallet generation claim.
- Ревизия источника: 56f634647d4f75596de20a6259b0cf1933949fdc
- Лицензия: Apache-2.0 AND MIT
- Атрибуция: Copyright \(c\) 2020-2026 tevador; BIP-39 authors copyright 2013. Upstream NOTICE and Apache/MIT terms retained in THIRD\_PARTY\_NOTICES.
- Распространение в репозитории: allowed
- Совместимость с SignPath: compatible
- Доказательства лицензии: [monero-osi-apache](../catalog/evidence/monero-osi-apache.json), [monero-polyseed-license](../catalog/evidence/monero-polyseed-license.json), [monero-polyseed-notice](../catalog/evidence/monero-polyseed-notice.json), [monero-signpath](../catalog/evidence/monero-signpath.json), [polyseed-cs-source](../catalog/evidence/polyseed-cs-source.json)
- Тестовые векторы: —

<a id="dictionary-polyseed-en"></a>

### polyseed-en — polyseed-en

- Исходная запись: [polyseed-en](../catalog/dictionaries/polyseed-en.json)
- Статус: verified
- Причина: Проверенная исследовательская запись; не гарантия релиза или безопасности.
- Диапазон версий (min / max): 56f634647d4f75596de20a6259b0cf1933949fdc / 56f634647d4f75596de20a6259b0cf1933949fdc
- Дата проверки: 2026-09-29
- Историческая запись: false
- Доказательства: [monero-osi-apache](../catalog/evidence/monero-osi-apache.json), [monero-polyseed-license](../catalog/evidence/monero-polyseed-license.json), [monero-polyseed-notice](../catalog/evidence/monero-polyseed-notice.json), [monero-polyseed-rules](../catalog/evidence/monero-polyseed-rules.json), [monero-polyseed-vectors](../catalog/evidence/monero-polyseed-vectors.json), [monero-signpath](../catalog/evidence/monero-signpath.json), [polyseed-en-source](../catalog/evidence/polyseed-en-source.json)
- Подтверждаемое утверждение: OSI lists Apache-2.0 as approved. This corroborates only the component-license decision, not project acceptance. Response-body SHA-256 1377faaaa81ba356528c4053d80e32fd12d84b794ed2667f09bf94aaca7458eb.
- Подтверждаемое утверждение: Apache-2.0 permits this modified source-data projection subject to license, notices and modification marking; root project LICENSE contains identical Apache text. No commercial dual-license requirement. Reviewed 2026-09-29; response byte SHA-256 cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30. See docs/research/batches/monero-polyseed.md.
- Подтверждаемое утверждение: Polyseed attribution and BIP39-derived dictionary MIT obligations apply cumulatively with Apache-2.0; complete upstream NOTICE retained in THIRD\_PARTY\_NOTICES. Reviewed 2026-09-29; response byte SHA-256 442cd16cdc8913cd76a9f7bd1047a0aea68ede782d94db3556392e18f39ad64e. See docs/research/batches/monero-polyseed.md.
- Подтверждаемое утверждение: Ten lists, NFKD word invariant, ordinal index lookup, language-dependent prefixes/accent handling; no BIP39 substitution. Reviewed 2026-09-29; response byte SHA-256 f30f867f5afd3bab323d85a8678868862d94dde09ed7801ab45a74f9b563b447. See docs/research/batches/monero-polyseed.md.
- Подтверждаемое утверждение: Published English/Spanish fixed phrases, random byte inputs, birthday and PBKDF2-input assertions. Projection tests dictionary order, GF checksum and secret/date unpacking. Upstream PBKDF2 is a dummy\: these are NOT derived-key known answers. Reviewed 2026-09-29; response byte SHA-256 3bc51ff2c12c3840e93d5e87a8da47516f806e3d51dc72ea6049f7f439dba4d5. See docs/research/batches/monero-polyseed.md.
- Подтверждаемое утверждение: Codex component assessment\: reviewed BSD-3-Clause/MIT and Apache-2.0\+MIT data licenses are OSI-approved and impose no commercial dual-licensing; notices are retained. Compatible for this data-only payload. Foundation acceptance, project eligibility and release signing remain unproven. Response-body SHA-256 6610cf889bbe0dc7533abaa310bc7a5cc9a61ae6c2ce0798a08109c925b46c51.
- Подтверждаемое утверждение: Exact ordered dictionary array and applicable file-level license header reviewed. Source-token extraction and byte hashes are independently checked against the public fixture; no complete phrase is stored here. Reviewed 2026-09-29; response byte SHA-256 6e32fb9d56d5c8a304d173937deec9dc9d64e52d15a9104f1c63dc45b7911f47. See docs/research/batches/monero-polyseed.md.
- Язык: en
- Письменность: Latn
- Кодировка: UTF-8
- Нормализация: NFKD
- Количество слов: 2048
- SHA-256: 2f5eed53a4727b4bf8880d8f3f199efc90e58503646d9ff8eff3a2ed3b24dbda
- Порядок слов: Exact upstream array order; zero-based indices. Extract literal UTF-8 tokens unchanged; remove C/C\+\+ wrapper and indentation, append LF after every token. No sorting, lowercasing or Unicode rewriting. Source file and extracted byte hashes in batch note.
- Позиционные правила: Same 2048-entry vocabulary at all 16 positions. First word is polynomial checksum; no BIP39 checksum semantics.; Input uses NFKD; output may compose NFC for accented/Japanese/Korean language flags. Latin prefix matching and French/Spanish accent-insensitivity are separate from stored NFKD bytes.; Language coverage is not a wallet generation claim.
- Ревизия источника: 56f634647d4f75596de20a6259b0cf1933949fdc
- Лицензия: Apache-2.0 AND MIT
- Атрибуция: Copyright \(c\) 2020-2026 tevador; BIP-39 authors copyright 2013. Upstream NOTICE and Apache/MIT terms retained in THIRD\_PARTY\_NOTICES.
- Распространение в репозитории: allowed
- Совместимость с SignPath: compatible
- Доказательства лицензии: [monero-osi-apache](../catalog/evidence/monero-osi-apache.json), [monero-polyseed-license](../catalog/evidence/monero-polyseed-license.json), [monero-polyseed-notice](../catalog/evidence/monero-polyseed-notice.json), [monero-signpath](../catalog/evidence/monero-signpath.json), [polyseed-en-source](../catalog/evidence/polyseed-en-source.json)
- Тестовые векторы: [monero-polyseed-vectors](../catalog/evidence/monero-polyseed-vectors.json)

<a id="dictionary-polyseed-es"></a>

### polyseed-es — polyseed-es

- Исходная запись: [polyseed-es](../catalog/dictionaries/polyseed-es.json)
- Статус: verified
- Причина: Проверенная исследовательская запись; не гарантия релиза или безопасности.
- Диапазон версий (min / max): 56f634647d4f75596de20a6259b0cf1933949fdc / 56f634647d4f75596de20a6259b0cf1933949fdc
- Дата проверки: 2026-09-29
- Историческая запись: false
- Доказательства: [monero-osi-apache](../catalog/evidence/monero-osi-apache.json), [monero-polyseed-license](../catalog/evidence/monero-polyseed-license.json), [monero-polyseed-notice](../catalog/evidence/monero-polyseed-notice.json), [monero-polyseed-rules](../catalog/evidence/monero-polyseed-rules.json), [monero-polyseed-vectors](../catalog/evidence/monero-polyseed-vectors.json), [monero-signpath](../catalog/evidence/monero-signpath.json), [polyseed-es-source](../catalog/evidence/polyseed-es-source.json)
- Подтверждаемое утверждение: OSI lists Apache-2.0 as approved. This corroborates only the component-license decision, not project acceptance. Response-body SHA-256 1377faaaa81ba356528c4053d80e32fd12d84b794ed2667f09bf94aaca7458eb.
- Подтверждаемое утверждение: Apache-2.0 permits this modified source-data projection subject to license, notices and modification marking; root project LICENSE contains identical Apache text. No commercial dual-license requirement. Reviewed 2026-09-29; response byte SHA-256 cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30. See docs/research/batches/monero-polyseed.md.
- Подтверждаемое утверждение: Polyseed attribution and BIP39-derived dictionary MIT obligations apply cumulatively with Apache-2.0; complete upstream NOTICE retained in THIRD\_PARTY\_NOTICES. Reviewed 2026-09-29; response byte SHA-256 442cd16cdc8913cd76a9f7bd1047a0aea68ede782d94db3556392e18f39ad64e. See docs/research/batches/monero-polyseed.md.
- Подтверждаемое утверждение: Ten lists, NFKD word invariant, ordinal index lookup, language-dependent prefixes/accent handling; no BIP39 substitution. Reviewed 2026-09-29; response byte SHA-256 f30f867f5afd3bab323d85a8678868862d94dde09ed7801ab45a74f9b563b447. See docs/research/batches/monero-polyseed.md.
- Подтверждаемое утверждение: Published English/Spanish fixed phrases, random byte inputs, birthday and PBKDF2-input assertions. Projection tests dictionary order, GF checksum and secret/date unpacking. Upstream PBKDF2 is a dummy\: these are NOT derived-key known answers. Reviewed 2026-09-29; response byte SHA-256 3bc51ff2c12c3840e93d5e87a8da47516f806e3d51dc72ea6049f7f439dba4d5. See docs/research/batches/monero-polyseed.md.
- Подтверждаемое утверждение: Codex component assessment\: reviewed BSD-3-Clause/MIT and Apache-2.0\+MIT data licenses are OSI-approved and impose no commercial dual-licensing; notices are retained. Compatible for this data-only payload. Foundation acceptance, project eligibility and release signing remain unproven. Response-body SHA-256 6610cf889bbe0dc7533abaa310bc7a5cc9a61ae6c2ce0798a08109c925b46c51.
- Подтверждаемое утверждение: Exact ordered dictionary array and applicable file-level license header reviewed. Source-token extraction and byte hashes are independently checked against the public fixture; no complete phrase is stored here. Reviewed 2026-09-29; response byte SHA-256 90405262a658434062b1d26cc7799c1d7fbeb11486c93a01153c733315c0cc0d. See docs/research/batches/monero-polyseed.md.
- Язык: es
- Письменность: Latn
- Кодировка: UTF-8
- Нормализация: NFKD
- Количество слов: 2048
- SHA-256: 31e589970a7490b1d62534c57b97b65b7d8ec7e7fcdad4830af1e324ed387c52
- Порядок слов: Exact upstream array order; zero-based indices. Extract literal UTF-8 tokens unchanged; remove C/C\+\+ wrapper and indentation, append LF after every token. No sorting, lowercasing or Unicode rewriting. Source file and extracted byte hashes in batch note.
- Позиционные правила: Same 2048-entry vocabulary at all 16 positions. First word is polynomial checksum; no BIP39 checksum semantics.; Input uses NFKD; output may compose NFC for accented/Japanese/Korean language flags. Latin prefix matching and French/Spanish accent-insensitivity are separate from stored NFKD bytes.; Language coverage is not a wallet generation claim.
- Ревизия источника: 56f634647d4f75596de20a6259b0cf1933949fdc
- Лицензия: Apache-2.0 AND MIT
- Атрибуция: Copyright \(c\) 2020-2026 tevador; BIP-39 authors copyright 2013. Upstream NOTICE and Apache/MIT terms retained in THIRD\_PARTY\_NOTICES.
- Распространение в репозитории: allowed
- Совместимость с SignPath: compatible
- Доказательства лицензии: [monero-osi-apache](../catalog/evidence/monero-osi-apache.json), [monero-polyseed-license](../catalog/evidence/monero-polyseed-license.json), [monero-polyseed-notice](../catalog/evidence/monero-polyseed-notice.json), [monero-signpath](../catalog/evidence/monero-signpath.json), [polyseed-es-source](../catalog/evidence/polyseed-es-source.json)
- Тестовые векторы: [monero-polyseed-vectors](../catalog/evidence/monero-polyseed-vectors.json)

<a id="dictionary-polyseed-fr"></a>

### polyseed-fr — polyseed-fr

- Исходная запись: [polyseed-fr](../catalog/dictionaries/polyseed-fr.json)
- Статус: documented
- Причина: Доказательств недостаточно для доступной поддержки.
- Рекомендация: Недоступно для выбора; используйте процедуру резервного копирования самого кошелька.
- Диапазон версий (min / max): 56f634647d4f75596de20a6259b0cf1933949fdc / 56f634647d4f75596de20a6259b0cf1933949fdc
- Дата проверки: 2026-09-29
- Историческая запись: false
- Доказательства: [monero-osi-apache](../catalog/evidence/monero-osi-apache.json), [monero-polyseed-license](../catalog/evidence/monero-polyseed-license.json), [monero-polyseed-notice](../catalog/evidence/monero-polyseed-notice.json), [monero-polyseed-rules](../catalog/evidence/monero-polyseed-rules.json), [monero-signpath](../catalog/evidence/monero-signpath.json), [polyseed-fr-source](../catalog/evidence/polyseed-fr-source.json)
- Подтверждаемое утверждение: OSI lists Apache-2.0 as approved. This corroborates only the component-license decision, not project acceptance. Response-body SHA-256 1377faaaa81ba356528c4053d80e32fd12d84b794ed2667f09bf94aaca7458eb.
- Подтверждаемое утверждение: Apache-2.0 permits this modified source-data projection subject to license, notices and modification marking; root project LICENSE contains identical Apache text. No commercial dual-license requirement. Reviewed 2026-09-29; response byte SHA-256 cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30. See docs/research/batches/monero-polyseed.md.
- Подтверждаемое утверждение: Polyseed attribution and BIP39-derived dictionary MIT obligations apply cumulatively with Apache-2.0; complete upstream NOTICE retained in THIRD\_PARTY\_NOTICES. Reviewed 2026-09-29; response byte SHA-256 442cd16cdc8913cd76a9f7bd1047a0aea68ede782d94db3556392e18f39ad64e. See docs/research/batches/monero-polyseed.md.
- Подтверждаемое утверждение: Ten lists, NFKD word invariant, ordinal index lookup, language-dependent prefixes/accent handling; no BIP39 substitution. Reviewed 2026-09-29; response byte SHA-256 f30f867f5afd3bab323d85a8678868862d94dde09ed7801ab45a74f9b563b447. See docs/research/batches/monero-polyseed.md.
- Подтверждаемое утверждение: Codex component assessment\: reviewed BSD-3-Clause/MIT and Apache-2.0\+MIT data licenses are OSI-approved and impose no commercial dual-licensing; notices are retained. Compatible for this data-only payload. Foundation acceptance, project eligibility and release signing remain unproven. Response-body SHA-256 6610cf889bbe0dc7533abaa310bc7a5cc9a61ae6c2ce0798a08109c925b46c51.
- Подтверждаемое утверждение: Exact ordered dictionary array and applicable file-level license header reviewed. Source-token extraction and byte hashes are independently checked against the public fixture; no complete phrase is stored here. Reviewed 2026-09-29; response byte SHA-256 0cb937a44ac79218a35e4d10f757d85dcd482cb4ed1482928644d0292ab8f0e2. See docs/research/batches/monero-polyseed.md.
- Язык: fr
- Письменность: Latn
- Кодировка: UTF-8
- Нормализация: NFKD
- Количество слов: 2048
- SHA-256: ebc3959ab7801a1df6bac4fa7d970652f1df76b683cd2f4003c941c63d517e59
- Порядок слов: Exact upstream array order; zero-based indices. Extract literal UTF-8 tokens unchanged; remove C/C\+\+ wrapper and indentation, append LF after every token. No sorting, lowercasing or Unicode rewriting. Source file and extracted byte hashes in batch note.
- Позиционные правила: Same 2048-entry vocabulary at all 16 positions. First word is polynomial checksum; no BIP39 checksum semantics.; Input uses NFKD; output may compose NFC for accented/Japanese/Korean language flags. Latin prefix matching and French/Spanish accent-insensitivity are separate from stored NFKD bytes.; Language coverage is not a wallet generation claim.
- Ревизия источника: 56f634647d4f75596de20a6259b0cf1933949fdc
- Лицензия: Apache-2.0 AND MIT
- Атрибуция: Copyright \(c\) 2020-2026 tevador; BIP-39 authors copyright 2013. Upstream NOTICE and Apache/MIT terms retained in THIRD\_PARTY\_NOTICES.
- Распространение в репозитории: allowed
- Совместимость с SignPath: compatible
- Доказательства лицензии: [monero-osi-apache](../catalog/evidence/monero-osi-apache.json), [monero-polyseed-license](../catalog/evidence/monero-polyseed-license.json), [monero-polyseed-notice](../catalog/evidence/monero-polyseed-notice.json), [monero-signpath](../catalog/evidence/monero-signpath.json), [polyseed-fr-source](../catalog/evidence/polyseed-fr-source.json)
- Тестовые векторы: —

<a id="dictionary-polyseed-it"></a>

### polyseed-it — polyseed-it

- Исходная запись: [polyseed-it](../catalog/dictionaries/polyseed-it.json)
- Статус: documented
- Причина: Доказательств недостаточно для доступной поддержки.
- Рекомендация: Недоступно для выбора; используйте процедуру резервного копирования самого кошелька.
- Диапазон версий (min / max): 56f634647d4f75596de20a6259b0cf1933949fdc / 56f634647d4f75596de20a6259b0cf1933949fdc
- Дата проверки: 2026-09-29
- Историческая запись: false
- Доказательства: [monero-osi-apache](../catalog/evidence/monero-osi-apache.json), [monero-polyseed-license](../catalog/evidence/monero-polyseed-license.json), [monero-polyseed-notice](../catalog/evidence/monero-polyseed-notice.json), [monero-polyseed-rules](../catalog/evidence/monero-polyseed-rules.json), [monero-signpath](../catalog/evidence/monero-signpath.json), [polyseed-it-source](../catalog/evidence/polyseed-it-source.json)
- Подтверждаемое утверждение: OSI lists Apache-2.0 as approved. This corroborates only the component-license decision, not project acceptance. Response-body SHA-256 1377faaaa81ba356528c4053d80e32fd12d84b794ed2667f09bf94aaca7458eb.
- Подтверждаемое утверждение: Apache-2.0 permits this modified source-data projection subject to license, notices and modification marking; root project LICENSE contains identical Apache text. No commercial dual-license requirement. Reviewed 2026-09-29; response byte SHA-256 cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30. See docs/research/batches/monero-polyseed.md.
- Подтверждаемое утверждение: Polyseed attribution and BIP39-derived dictionary MIT obligations apply cumulatively with Apache-2.0; complete upstream NOTICE retained in THIRD\_PARTY\_NOTICES. Reviewed 2026-09-29; response byte SHA-256 442cd16cdc8913cd76a9f7bd1047a0aea68ede782d94db3556392e18f39ad64e. See docs/research/batches/monero-polyseed.md.
- Подтверждаемое утверждение: Ten lists, NFKD word invariant, ordinal index lookup, language-dependent prefixes/accent handling; no BIP39 substitution. Reviewed 2026-09-29; response byte SHA-256 f30f867f5afd3bab323d85a8678868862d94dde09ed7801ab45a74f9b563b447. See docs/research/batches/monero-polyseed.md.
- Подтверждаемое утверждение: Codex component assessment\: reviewed BSD-3-Clause/MIT and Apache-2.0\+MIT data licenses are OSI-approved and impose no commercial dual-licensing; notices are retained. Compatible for this data-only payload. Foundation acceptance, project eligibility and release signing remain unproven. Response-body SHA-256 6610cf889bbe0dc7533abaa310bc7a5cc9a61ae6c2ce0798a08109c925b46c51.
- Подтверждаемое утверждение: Exact ordered dictionary array and applicable file-level license header reviewed. Source-token extraction and byte hashes are independently checked against the public fixture; no complete phrase is stored here. Reviewed 2026-09-29; response byte SHA-256 211787e3a762b7b55e7f2f422dc16e843399697ef078b10b2773ba62972a312a. See docs/research/batches/monero-polyseed.md.
- Язык: it
- Письменность: Latn
- Кодировка: UTF-8
- Нормализация: NFKD
- Количество слов: 2048
- SHA-256: d392c49fdb700a24cd1fceb237c1f65dcc128f6b34a8aacb58b59384b5c648c2
- Порядок слов: Exact upstream array order; zero-based indices. Extract literal UTF-8 tokens unchanged; remove C/C\+\+ wrapper and indentation, append LF after every token. No sorting, lowercasing or Unicode rewriting. Source file and extracted byte hashes in batch note.
- Позиционные правила: Same 2048-entry vocabulary at all 16 positions. First word is polynomial checksum; no BIP39 checksum semantics.; Input uses NFKD; output may compose NFC for accented/Japanese/Korean language flags. Latin prefix matching and French/Spanish accent-insensitivity are separate from stored NFKD bytes.; Language coverage is not a wallet generation claim.
- Ревизия источника: 56f634647d4f75596de20a6259b0cf1933949fdc
- Лицензия: Apache-2.0 AND MIT
- Атрибуция: Copyright \(c\) 2020-2026 tevador; BIP-39 authors copyright 2013. Upstream NOTICE and Apache/MIT terms retained in THIRD\_PARTY\_NOTICES.
- Распространение в репозитории: allowed
- Совместимость с SignPath: compatible
- Доказательства лицензии: [monero-osi-apache](../catalog/evidence/monero-osi-apache.json), [monero-polyseed-license](../catalog/evidence/monero-polyseed-license.json), [monero-polyseed-notice](../catalog/evidence/monero-polyseed-notice.json), [monero-signpath](../catalog/evidence/monero-signpath.json), [polyseed-it-source](../catalog/evidence/polyseed-it-source.json)
- Тестовые векторы: —

<a id="dictionary-polyseed-ja"></a>

### polyseed-ja — polyseed-ja

- Исходная запись: [polyseed-ja](../catalog/dictionaries/polyseed-ja.json)
- Статус: documented
- Причина: Доказательств недостаточно для доступной поддержки.
- Рекомендация: Недоступно для выбора; используйте процедуру резервного копирования самого кошелька.
- Диапазон версий (min / max): 56f634647d4f75596de20a6259b0cf1933949fdc / 56f634647d4f75596de20a6259b0cf1933949fdc
- Дата проверки: 2026-09-29
- Историческая запись: false
- Доказательства: [monero-osi-apache](../catalog/evidence/monero-osi-apache.json), [monero-polyseed-license](../catalog/evidence/monero-polyseed-license.json), [monero-polyseed-notice](../catalog/evidence/monero-polyseed-notice.json), [monero-polyseed-rules](../catalog/evidence/monero-polyseed-rules.json), [monero-signpath](../catalog/evidence/monero-signpath.json), [polyseed-ja-source](../catalog/evidence/polyseed-ja-source.json)
- Подтверждаемое утверждение: OSI lists Apache-2.0 as approved. This corroborates only the component-license decision, not project acceptance. Response-body SHA-256 1377faaaa81ba356528c4053d80e32fd12d84b794ed2667f09bf94aaca7458eb.
- Подтверждаемое утверждение: Apache-2.0 permits this modified source-data projection subject to license, notices and modification marking; root project LICENSE contains identical Apache text. No commercial dual-license requirement. Reviewed 2026-09-29; response byte SHA-256 cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30. See docs/research/batches/monero-polyseed.md.
- Подтверждаемое утверждение: Polyseed attribution and BIP39-derived dictionary MIT obligations apply cumulatively with Apache-2.0; complete upstream NOTICE retained in THIRD\_PARTY\_NOTICES. Reviewed 2026-09-29; response byte SHA-256 442cd16cdc8913cd76a9f7bd1047a0aea68ede782d94db3556392e18f39ad64e. See docs/research/batches/monero-polyseed.md.
- Подтверждаемое утверждение: Ten lists, NFKD word invariant, ordinal index lookup, language-dependent prefixes/accent handling; no BIP39 substitution. Reviewed 2026-09-29; response byte SHA-256 f30f867f5afd3bab323d85a8678868862d94dde09ed7801ab45a74f9b563b447. See docs/research/batches/monero-polyseed.md.
- Подтверждаемое утверждение: Codex component assessment\: reviewed BSD-3-Clause/MIT and Apache-2.0\+MIT data licenses are OSI-approved and impose no commercial dual-licensing; notices are retained. Compatible for this data-only payload. Foundation acceptance, project eligibility and release signing remain unproven. Response-body SHA-256 6610cf889bbe0dc7533abaa310bc7a5cc9a61ae6c2ce0798a08109c925b46c51.
- Подтверждаемое утверждение: Exact ordered dictionary array and applicable file-level license header reviewed. Source-token extraction and byte hashes are independently checked against the public fixture; no complete phrase is stored here. Reviewed 2026-09-29; response byte SHA-256 c309fd0d6c435de214262dd5c96331b8a48bd9a9a3b3b6659d2817056ecc1887. See docs/research/batches/monero-polyseed.md.
- Язык: ja
- Письменность: Jpan
- Кодировка: UTF-8
- Нормализация: NFKD
- Количество слов: 2048
- SHA-256: 438b4d19c4af485650822ae0d08855090a6812e2a2ed6fb793583ae90f3e6248
- Порядок слов: Exact upstream array order; zero-based indices. Extract literal UTF-8 tokens unchanged; remove C/C\+\+ wrapper and indentation, append LF after every token. No sorting, lowercasing or Unicode rewriting. Source file and extracted byte hashes in batch note.
- Позиционные правила: Same 2048-entry vocabulary at all 16 positions. First word is polynomial checksum; no BIP39 checksum semantics.; Input uses NFKD; output may compose NFC for accented/Japanese/Korean language flags. Latin prefix matching and French/Spanish accent-insensitivity are separate from stored NFKD bytes.; Language coverage is not a wallet generation claim.
- Ревизия источника: 56f634647d4f75596de20a6259b0cf1933949fdc
- Лицензия: Apache-2.0 AND MIT
- Атрибуция: Copyright \(c\) 2020-2026 tevador; BIP-39 authors copyright 2013. Upstream NOTICE and Apache/MIT terms retained in THIRD\_PARTY\_NOTICES.
- Распространение в репозитории: allowed
- Совместимость с SignPath: compatible
- Доказательства лицензии: [monero-osi-apache](../catalog/evidence/monero-osi-apache.json), [monero-polyseed-license](../catalog/evidence/monero-polyseed-license.json), [monero-polyseed-notice](../catalog/evidence/monero-polyseed-notice.json), [monero-signpath](../catalog/evidence/monero-signpath.json), [polyseed-ja-source](../catalog/evidence/polyseed-ja-source.json)
- Тестовые векторы: —

<a id="dictionary-polyseed-ko"></a>

### polyseed-ko — polyseed-ko

- Исходная запись: [polyseed-ko](../catalog/dictionaries/polyseed-ko.json)
- Статус: documented
- Причина: Доказательств недостаточно для доступной поддержки.
- Рекомендация: Недоступно для выбора; используйте процедуру резервного копирования самого кошелька.
- Диапазон версий (min / max): 56f634647d4f75596de20a6259b0cf1933949fdc / 56f634647d4f75596de20a6259b0cf1933949fdc
- Дата проверки: 2026-09-29
- Историческая запись: false
- Доказательства: [monero-osi-apache](../catalog/evidence/monero-osi-apache.json), [monero-polyseed-license](../catalog/evidence/monero-polyseed-license.json), [monero-polyseed-notice](../catalog/evidence/monero-polyseed-notice.json), [monero-polyseed-rules](../catalog/evidence/monero-polyseed-rules.json), [monero-signpath](../catalog/evidence/monero-signpath.json), [polyseed-ko-source](../catalog/evidence/polyseed-ko-source.json)
- Подтверждаемое утверждение: OSI lists Apache-2.0 as approved. This corroborates only the component-license decision, not project acceptance. Response-body SHA-256 1377faaaa81ba356528c4053d80e32fd12d84b794ed2667f09bf94aaca7458eb.
- Подтверждаемое утверждение: Apache-2.0 permits this modified source-data projection subject to license, notices and modification marking; root project LICENSE contains identical Apache text. No commercial dual-license requirement. Reviewed 2026-09-29; response byte SHA-256 cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30. See docs/research/batches/monero-polyseed.md.
- Подтверждаемое утверждение: Polyseed attribution and BIP39-derived dictionary MIT obligations apply cumulatively with Apache-2.0; complete upstream NOTICE retained in THIRD\_PARTY\_NOTICES. Reviewed 2026-09-29; response byte SHA-256 442cd16cdc8913cd76a9f7bd1047a0aea68ede782d94db3556392e18f39ad64e. See docs/research/batches/monero-polyseed.md.
- Подтверждаемое утверждение: Ten lists, NFKD word invariant, ordinal index lookup, language-dependent prefixes/accent handling; no BIP39 substitution. Reviewed 2026-09-29; response byte SHA-256 f30f867f5afd3bab323d85a8678868862d94dde09ed7801ab45a74f9b563b447. See docs/research/batches/monero-polyseed.md.
- Подтверждаемое утверждение: Codex component assessment\: reviewed BSD-3-Clause/MIT and Apache-2.0\+MIT data licenses are OSI-approved and impose no commercial dual-licensing; notices are retained. Compatible for this data-only payload. Foundation acceptance, project eligibility and release signing remain unproven. Response-body SHA-256 6610cf889bbe0dc7533abaa310bc7a5cc9a61ae6c2ce0798a08109c925b46c51.
- Подтверждаемое утверждение: Exact ordered dictionary array and applicable file-level license header reviewed. Source-token extraction and byte hashes are independently checked against the public fixture; no complete phrase is stored here. Reviewed 2026-09-29; response byte SHA-256 0b56d27f7c1d3c6d13af9248d981d90a7d515222e3858fe6eca2f1aae7ea6ac9. See docs/research/batches/monero-polyseed.md.
- Язык: ko
- Письменность: Kore
- Кодировка: UTF-8
- Нормализация: NFKD
- Количество слов: 2048
- SHA-256: 9e95f86c167de88f450f0aaf89e87f6624a57f973c67b516e338e8e8b8897f60
- Порядок слов: Exact upstream array order; zero-based indices. Extract literal UTF-8 tokens unchanged; remove C/C\+\+ wrapper and indentation, append LF after every token. No sorting, lowercasing or Unicode rewriting. Source file and extracted byte hashes in batch note.
- Позиционные правила: Same 2048-entry vocabulary at all 16 positions. First word is polynomial checksum; no BIP39 checksum semantics.; Input uses NFKD; output may compose NFC for accented/Japanese/Korean language flags. Latin prefix matching and French/Spanish accent-insensitivity are separate from stored NFKD bytes.; Language coverage is not a wallet generation claim.
- Ревизия источника: 56f634647d4f75596de20a6259b0cf1933949fdc
- Лицензия: Apache-2.0 AND MIT
- Атрибуция: Copyright \(c\) 2020-2026 tevador; BIP-39 authors copyright 2013. Upstream NOTICE and Apache/MIT terms retained in THIRD\_PARTY\_NOTICES.
- Распространение в репозитории: allowed
- Совместимость с SignPath: compatible
- Доказательства лицензии: [monero-osi-apache](../catalog/evidence/monero-osi-apache.json), [monero-polyseed-license](../catalog/evidence/monero-polyseed-license.json), [monero-polyseed-notice](../catalog/evidence/monero-polyseed-notice.json), [monero-signpath](../catalog/evidence/monero-signpath.json), [polyseed-ko-source](../catalog/evidence/polyseed-ko-source.json)
- Тестовые векторы: —

<a id="dictionary-polyseed-pt"></a>

### polyseed-pt — polyseed-pt

- Исходная запись: [polyseed-pt](../catalog/dictionaries/polyseed-pt.json)
- Статус: documented
- Причина: Доказательств недостаточно для доступной поддержки.
- Рекомендация: Недоступно для выбора; используйте процедуру резервного копирования самого кошелька.
- Диапазон версий (min / max): 56f634647d4f75596de20a6259b0cf1933949fdc / 56f634647d4f75596de20a6259b0cf1933949fdc
- Дата проверки: 2026-09-29
- Историческая запись: false
- Доказательства: [monero-osi-apache](../catalog/evidence/monero-osi-apache.json), [monero-polyseed-license](../catalog/evidence/monero-polyseed-license.json), [monero-polyseed-notice](../catalog/evidence/monero-polyseed-notice.json), [monero-polyseed-rules](../catalog/evidence/monero-polyseed-rules.json), [monero-signpath](../catalog/evidence/monero-signpath.json), [polyseed-pt-source](../catalog/evidence/polyseed-pt-source.json)
- Подтверждаемое утверждение: OSI lists Apache-2.0 as approved. This corroborates only the component-license decision, not project acceptance. Response-body SHA-256 1377faaaa81ba356528c4053d80e32fd12d84b794ed2667f09bf94aaca7458eb.
- Подтверждаемое утверждение: Apache-2.0 permits this modified source-data projection subject to license, notices and modification marking; root project LICENSE contains identical Apache text. No commercial dual-license requirement. Reviewed 2026-09-29; response byte SHA-256 cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30. See docs/research/batches/monero-polyseed.md.
- Подтверждаемое утверждение: Polyseed attribution and BIP39-derived dictionary MIT obligations apply cumulatively with Apache-2.0; complete upstream NOTICE retained in THIRD\_PARTY\_NOTICES. Reviewed 2026-09-29; response byte SHA-256 442cd16cdc8913cd76a9f7bd1047a0aea68ede782d94db3556392e18f39ad64e. See docs/research/batches/monero-polyseed.md.
- Подтверждаемое утверждение: Ten lists, NFKD word invariant, ordinal index lookup, language-dependent prefixes/accent handling; no BIP39 substitution. Reviewed 2026-09-29; response byte SHA-256 f30f867f5afd3bab323d85a8678868862d94dde09ed7801ab45a74f9b563b447. See docs/research/batches/monero-polyseed.md.
- Подтверждаемое утверждение: Codex component assessment\: reviewed BSD-3-Clause/MIT and Apache-2.0\+MIT data licenses are OSI-approved and impose no commercial dual-licensing; notices are retained. Compatible for this data-only payload. Foundation acceptance, project eligibility and release signing remain unproven. Response-body SHA-256 6610cf889bbe0dc7533abaa310bc7a5cc9a61ae6c2ce0798a08109c925b46c51.
- Подтверждаемое утверждение: Exact ordered dictionary array and applicable file-level license header reviewed. Source-token extraction and byte hashes are independently checked against the public fixture; no complete phrase is stored here. Reviewed 2026-09-29; response byte SHA-256 40e9919edf8b768a12cdfc3c3cd2343fa16a628ad0e8d2749b4c026af7c9bf70. See docs/research/batches/monero-polyseed.md.
- Язык: pt
- Письменность: Latn
- Кодировка: UTF-8
- Нормализация: NFKD
- Количество слов: 2048
- SHA-256: 2685e9c194c82ae67e10ba59d9ea5345a23dc093e92276fc5361f6667d79cd3f
- Порядок слов: Exact upstream array order; zero-based indices. Extract literal UTF-8 tokens unchanged; remove C/C\+\+ wrapper and indentation, append LF after every token. No sorting, lowercasing or Unicode rewriting. Source file and extracted byte hashes in batch note.
- Позиционные правила: Same 2048-entry vocabulary at all 16 positions. First word is polynomial checksum; no BIP39 checksum semantics.; Input uses NFKD; output may compose NFC for accented/Japanese/Korean language flags. Latin prefix matching and French/Spanish accent-insensitivity are separate from stored NFKD bytes.; Language coverage is not a wallet generation claim.
- Ревизия источника: 56f634647d4f75596de20a6259b0cf1933949fdc
- Лицензия: Apache-2.0 AND MIT
- Атрибуция: Copyright \(c\) 2020-2026 tevador; BIP-39 authors copyright 2013. Upstream NOTICE and Apache/MIT terms retained in THIRD\_PARTY\_NOTICES.
- Распространение в репозитории: allowed
- Совместимость с SignPath: compatible
- Доказательства лицензии: [monero-osi-apache](../catalog/evidence/monero-osi-apache.json), [monero-polyseed-license](../catalog/evidence/monero-polyseed-license.json), [monero-polyseed-notice](../catalog/evidence/monero-polyseed-notice.json), [monero-signpath](../catalog/evidence/monero-signpath.json), [polyseed-pt-source](../catalog/evidence/polyseed-pt-source.json)
- Тестовые векторы: —

<a id="dictionary-polyseed-zh-hans"></a>

### polyseed-zh-hans — polyseed-zh-hans

- Исходная запись: [polyseed-zh-hans](../catalog/dictionaries/polyseed-zh-hans.json)
- Статус: documented
- Причина: Доказательств недостаточно для доступной поддержки.
- Рекомендация: Недоступно для выбора; используйте процедуру резервного копирования самого кошелька.
- Диапазон версий (min / max): 56f634647d4f75596de20a6259b0cf1933949fdc / 56f634647d4f75596de20a6259b0cf1933949fdc
- Дата проверки: 2026-09-29
- Историческая запись: false
- Доказательства: [monero-osi-apache](../catalog/evidence/monero-osi-apache.json), [monero-polyseed-license](../catalog/evidence/monero-polyseed-license.json), [monero-polyseed-notice](../catalog/evidence/monero-polyseed-notice.json), [monero-polyseed-rules](../catalog/evidence/monero-polyseed-rules.json), [monero-signpath](../catalog/evidence/monero-signpath.json), [polyseed-zh-hans-source](../catalog/evidence/polyseed-zh-hans-source.json)
- Подтверждаемое утверждение: OSI lists Apache-2.0 as approved. This corroborates only the component-license decision, not project acceptance. Response-body SHA-256 1377faaaa81ba356528c4053d80e32fd12d84b794ed2667f09bf94aaca7458eb.
- Подтверждаемое утверждение: Apache-2.0 permits this modified source-data projection subject to license, notices and modification marking; root project LICENSE contains identical Apache text. No commercial dual-license requirement. Reviewed 2026-09-29; response byte SHA-256 cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30. See docs/research/batches/monero-polyseed.md.
- Подтверждаемое утверждение: Polyseed attribution and BIP39-derived dictionary MIT obligations apply cumulatively with Apache-2.0; complete upstream NOTICE retained in THIRD\_PARTY\_NOTICES. Reviewed 2026-09-29; response byte SHA-256 442cd16cdc8913cd76a9f7bd1047a0aea68ede782d94db3556392e18f39ad64e. See docs/research/batches/monero-polyseed.md.
- Подтверждаемое утверждение: Ten lists, NFKD word invariant, ordinal index lookup, language-dependent prefixes/accent handling; no BIP39 substitution. Reviewed 2026-09-29; response byte SHA-256 f30f867f5afd3bab323d85a8678868862d94dde09ed7801ab45a74f9b563b447. See docs/research/batches/monero-polyseed.md.
- Подтверждаемое утверждение: Codex component assessment\: reviewed BSD-3-Clause/MIT and Apache-2.0\+MIT data licenses are OSI-approved and impose no commercial dual-licensing; notices are retained. Compatible for this data-only payload. Foundation acceptance, project eligibility and release signing remain unproven. Response-body SHA-256 6610cf889bbe0dc7533abaa310bc7a5cc9a61ae6c2ce0798a08109c925b46c51.
- Подтверждаемое утверждение: Exact ordered dictionary array and applicable file-level license header reviewed. Source-token extraction and byte hashes are independently checked against the public fixture; no complete phrase is stored here. Reviewed 2026-09-29; response byte SHA-256 cabe21517dcde33e517926ab29d7b58bb5e5f97b7b5a6a631e9137f256a5165b. See docs/research/batches/monero-polyseed.md.
- Язык: zh-hans
- Письменность: Hans
- Кодировка: UTF-8
- Нормализация: NFKD
- Количество слов: 2048
- SHA-256: 5c5942792bd8340cb8b27cd592f1015edf56a8c5b26276ee18a482428e7c5726
- Порядок слов: Exact upstream array order; zero-based indices. Extract literal UTF-8 tokens unchanged; remove C/C\+\+ wrapper and indentation, append LF after every token. No sorting, lowercasing or Unicode rewriting. Source file and extracted byte hashes in batch note.
- Позиционные правила: Same 2048-entry vocabulary at all 16 positions. First word is polynomial checksum; no BIP39 checksum semantics.; Input uses NFKD; output may compose NFC for accented/Japanese/Korean language flags. Latin prefix matching and French/Spanish accent-insensitivity are separate from stored NFKD bytes.; Language coverage is not a wallet generation claim.
- Ревизия источника: 56f634647d4f75596de20a6259b0cf1933949fdc
- Лицензия: Apache-2.0 AND MIT
- Атрибуция: Copyright \(c\) 2020-2026 tevador; BIP-39 authors copyright 2013. Upstream NOTICE and Apache/MIT terms retained in THIRD\_PARTY\_NOTICES.
- Распространение в репозитории: allowed
- Совместимость с SignPath: compatible
- Доказательства лицензии: [monero-osi-apache](../catalog/evidence/monero-osi-apache.json), [monero-polyseed-license](../catalog/evidence/monero-polyseed-license.json), [monero-polyseed-notice](../catalog/evidence/monero-polyseed-notice.json), [monero-signpath](../catalog/evidence/monero-signpath.json), [polyseed-zh-hans-source](../catalog/evidence/polyseed-zh-hans-source.json)
- Тестовые векторы: —

<a id="dictionary-polyseed-zh-hant"></a>

### polyseed-zh-hant — polyseed-zh-hant

- Исходная запись: [polyseed-zh-hant](../catalog/dictionaries/polyseed-zh-hant.json)
- Статус: documented
- Причина: Доказательств недостаточно для доступной поддержки.
- Рекомендация: Недоступно для выбора; используйте процедуру резервного копирования самого кошелька.
- Диапазон версий (min / max): 56f634647d4f75596de20a6259b0cf1933949fdc / 56f634647d4f75596de20a6259b0cf1933949fdc
- Дата проверки: 2026-09-29
- Историческая запись: false
- Доказательства: [monero-osi-apache](../catalog/evidence/monero-osi-apache.json), [monero-polyseed-license](../catalog/evidence/monero-polyseed-license.json), [monero-polyseed-notice](../catalog/evidence/monero-polyseed-notice.json), [monero-polyseed-rules](../catalog/evidence/monero-polyseed-rules.json), [monero-signpath](../catalog/evidence/monero-signpath.json), [polyseed-zh-hant-source](../catalog/evidence/polyseed-zh-hant-source.json)
- Подтверждаемое утверждение: OSI lists Apache-2.0 as approved. This corroborates only the component-license decision, not project acceptance. Response-body SHA-256 1377faaaa81ba356528c4053d80e32fd12d84b794ed2667f09bf94aaca7458eb.
- Подтверждаемое утверждение: Apache-2.0 permits this modified source-data projection subject to license, notices and modification marking; root project LICENSE contains identical Apache text. No commercial dual-license requirement. Reviewed 2026-09-29; response byte SHA-256 cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30. See docs/research/batches/monero-polyseed.md.
- Подтверждаемое утверждение: Polyseed attribution and BIP39-derived dictionary MIT obligations apply cumulatively with Apache-2.0; complete upstream NOTICE retained in THIRD\_PARTY\_NOTICES. Reviewed 2026-09-29; response byte SHA-256 442cd16cdc8913cd76a9f7bd1047a0aea68ede782d94db3556392e18f39ad64e. See docs/research/batches/monero-polyseed.md.
- Подтверждаемое утверждение: Ten lists, NFKD word invariant, ordinal index lookup, language-dependent prefixes/accent handling; no BIP39 substitution. Reviewed 2026-09-29; response byte SHA-256 f30f867f5afd3bab323d85a8678868862d94dde09ed7801ab45a74f9b563b447. See docs/research/batches/monero-polyseed.md.
- Подтверждаемое утверждение: Codex component assessment\: reviewed BSD-3-Clause/MIT and Apache-2.0\+MIT data licenses are OSI-approved and impose no commercial dual-licensing; notices are retained. Compatible for this data-only payload. Foundation acceptance, project eligibility and release signing remain unproven. Response-body SHA-256 6610cf889bbe0dc7533abaa310bc7a5cc9a61ae6c2ce0798a08109c925b46c51.
- Подтверждаемое утверждение: Exact ordered dictionary array and applicable file-level license header reviewed. Source-token extraction and byte hashes are independently checked against the public fixture; no complete phrase is stored here. Reviewed 2026-09-29; response byte SHA-256 7ddbd0546736c7e53077b97bef5f6697f752f6a78ea7e4429987b66f14a118ba. See docs/research/batches/monero-polyseed.md.
- Язык: zh-hant
- Письменность: Hant
- Кодировка: UTF-8
- Нормализация: NFKD
- Количество слов: 2048
- SHA-256: 417b26b3d8500a4ae3d59717d7011952db6fc2fb84b807f3f94ac734e89c1b5f
- Порядок слов: Exact upstream array order; zero-based indices. Extract literal UTF-8 tokens unchanged; remove C/C\+\+ wrapper and indentation, append LF after every token. No sorting, lowercasing or Unicode rewriting. Source file and extracted byte hashes in batch note.
- Позиционные правила: Same 2048-entry vocabulary at all 16 positions. First word is polynomial checksum; no BIP39 checksum semantics.; Input uses NFKD; output may compose NFC for accented/Japanese/Korean language flags. Latin prefix matching and French/Spanish accent-insensitivity are separate from stored NFKD bytes.; Language coverage is not a wallet generation claim.
- Ревизия источника: 56f634647d4f75596de20a6259b0cf1933949fdc
- Лицензия: Apache-2.0 AND MIT
- Атрибуция: Copyright \(c\) 2020-2026 tevador; BIP-39 authors copyright 2013. Upstream NOTICE and Apache/MIT terms retained in THIRD\_PARTY\_NOTICES.
- Распространение в репозитории: allowed
- Совместимость с SignPath: compatible
- Доказательства лицензии: [monero-osi-apache](../catalog/evidence/monero-osi-apache.json), [monero-polyseed-license](../catalog/evidence/monero-polyseed-license.json), [monero-polyseed-notice](../catalog/evidence/monero-polyseed-notice.json), [monero-signpath](../catalog/evidence/monero-signpath.json), [polyseed-zh-hant-source](../catalog/evidence/polyseed-zh-hant-source.json)
- Тестовые векторы: —

## Ревизии доказательств

- [bip39-guidance](../catalog/evidence/bip39-guidance.json): official-specification; 3a10b5b5f0a7586df8928d580a3009744ebb2079; 2026-09-29
- [bip39-license](../catalog/evidence/bip39-license.json): official-source; b57a5ad77a981e743f4167ab2f7927a55c1e82a8; 2026-09-29
- [bip39-osi-mit](../catalog/evidence/bip39-osi-mit.json): official-documentation; sha256\:004c79db0a335488afc87600d89f447dce7fb4d24d510af15ed4381a24be848c; 2026-09-29
- [bip39-signpath](../catalog/evidence/bip39-signpath.json): official-documentation; sha256\:6610cf889bbe0dc7533abaa310bc7a5cc9a61ae6c2ce0798a08109c925b46c51; 2026-09-29
- [bip39-spec](../catalog/evidence/bip39-spec.json): official-specification; 3a10b5b5f0a7586df8928d580a3009744ebb2079; 2026-09-29
- [bip39-vectors](../catalog/evidence/bip39-vectors.json): public-test-vector; b57a5ad77a981e743f4167ab2f7927a55c1e82a8; 2026-09-29
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
| dictionary-monero-de — MONERO — Немецкий | terminal | verified | [monero-de](../catalog/dictionaries/monero-de.json) |
| dictionary-monero-en — MONERO — Английский | terminal | verified | [monero-en](../catalog/dictionaries/monero-en.json) |
| dictionary-monero-en-old — MONERO — Старый английский | terminal | documented | [monero-en-old](../catalog/dictionaries/monero-en-old.json) |
| dictionary-monero-eo — MONERO — Эсперанто | terminal | documented | [monero-eo](../catalog/dictionaries/monero-eo.json) |
| dictionary-monero-es — MONERO — Испанский | terminal | documented | [monero-es](../catalog/dictionaries/monero-es.json) |
| dictionary-monero-fr — MONERO — Французский | terminal | documented | [monero-fr](../catalog/dictionaries/monero-fr.json) |
| dictionary-monero-it — MONERO — Итальянский | terminal | documented | [monero-it](../catalog/dictionaries/monero-it.json) |
| dictionary-monero-ja — MONERO — Японский | terminal | documented | [monero-ja](../catalog/dictionaries/monero-ja.json) |
| dictionary-monero-jbo — MONERO — Ложбан | terminal | documented | [monero-jbo](../catalog/dictionaries/monero-jbo.json) |
| dictionary-monero-nl — MONERO — Нидерландский | terminal | documented | [monero-nl](../catalog/dictionaries/monero-nl.json) |
| dictionary-monero-pt — MONERO — Португальский | terminal | verified | [monero-pt](../catalog/dictionaries/monero-pt.json) |
| dictionary-monero-ru — MONERO — Русский | terminal | documented | [monero-ru](../catalog/dictionaries/monero-ru.json) |
| dictionary-monero-zh-hans — MONERO — Китайский упрощённый | terminal | documented | [monero-zh-hans](../catalog/dictionaries/monero-zh-hans.json) |
| dictionary-pgp-even — pgp even | pending | — | — |
| dictionary-pgp-odd — pgp odd | pending | — | — |
| dictionary-polyseed-cs — POLYSEED — Чешский | terminal | documented | [polyseed-cs](../catalog/dictionaries/polyseed-cs.json) |
| dictionary-polyseed-en — POLYSEED — Английский | terminal | verified | [polyseed-en](../catalog/dictionaries/polyseed-en.json) |
| dictionary-polyseed-es — POLYSEED — Испанский | terminal | verified | [polyseed-es](../catalog/dictionaries/polyseed-es.json) |
| dictionary-polyseed-fr — POLYSEED — Французский | terminal | documented | [polyseed-fr](../catalog/dictionaries/polyseed-fr.json) |
| dictionary-polyseed-it — POLYSEED — Итальянский | terminal | documented | [polyseed-it](../catalog/dictionaries/polyseed-it.json) |
| dictionary-polyseed-ja — POLYSEED — Японский | terminal | documented | [polyseed-ja](../catalog/dictionaries/polyseed-ja.json) |
| dictionary-polyseed-ko — POLYSEED — Корейский | terminal | documented | [polyseed-ko](../catalog/dictionaries/polyseed-ko.json) |
| dictionary-polyseed-pt — POLYSEED — Португальский | terminal | documented | [polyseed-pt](../catalog/dictionaries/polyseed-pt.json) |
| dictionary-polyseed-zh-hans — POLYSEED — Китайский упрощённый | terminal | documented | [polyseed-zh-hans](../catalog/dictionaries/polyseed-zh-hans.json) |
| dictionary-polyseed-zh-hant — POLYSEED — Китайский традиционный | terminal | documented | [polyseed-zh-hant](../catalog/dictionaries/polyseed-zh-hant.json) |
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
| scheme-monero-legacy — monero legacy | terminal | documented | [monero-legacy](../catalog/schemes/monero-legacy.json) |
| scheme-mymonero — mymonero | terminal | documented | [mymonero-13](../catalog/schemes/mymonero-13.json) |
| scheme-polyseed — polyseed | terminal | documented | [polyseed-16](../catalog/schemes/polyseed-16.json) |
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
| wallet-cake-wallet — cake wallet | terminal | documented | [cake-wallet-monero](../catalog/wallets/cake-wallet-monero.json) |
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
| wallet-exodus-monero — exodus monero | terminal | documented | [exodus-monero-export](../catalog/wallets/exodus-monero-export.json) |
| wallet-feather — feather | terminal | documented | [feather](../catalog/wallets/feather.json) |
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
| wallet-monero-gui-cli — monero gui cli | terminal | documented | [monero-gui-cli](../catalog/wallets/monero-gui-cli.json) |
| wallet-mymonero — mymonero | terminal | documented | [mymonero](../catalog/wallets/mymonero.json) |
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
