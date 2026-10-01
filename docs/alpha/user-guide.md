# Tessaveil unsigned Windows v1 candidate guide

**Synthetic data only. Unsigned. Not RC/stable. Never use a real recovery
phrase, order key, private key, funded-wallet backup, or user vault.** The
candidate uses schema 2 and `.tessaveil-alpha`; format/KDF freeze and migration
remain unapproved. Verdict: **NO-GO для реальных данных**.

Security audit: not yet independently completed

[English](#english) · [Русский](#русский)

## English

### Exact supported profiles

Only these profile/mode/version pairs are selectable. Each uses
`ton-native-generated`, the reviewed BIP39 English bytes as the eligible table
dictionary, and exactly 24 rows; shared words do not make other schemes
compatible.

| Profile / mode | Platform | Exact source scope | Rows |
| --- | --- | --- | ---: |
| `mytonwallet-native / ton-native-generated` | web | `26.9.8-source-f042bcc06b84f0cec928a29795f1cb8bf60a3e9c` | 24 |
| `tonhub / ton-native-generated` | Android | `2.5.45-source-a2503f79d14868d65349ad7035d18389c6e2f996` | 24 |
| `tonkeeper-classic / ton-native-generated` | web | `source-4942adcdcddf55d57e3d3fc3676f019caf87357e` | 24 |

The following priority modes remain visible but non-selectable:

- Tonkeeper Multichain (`bip39-multichain-generated`) is `documented`: official
  rebranding confirms a separate multichain wallet, but exact platform/version,
  generated word count, first/last versions, and a full-path known answer are
  not established. BIP39 import is not generation evidence.
- Gram Wallet (`mnemonic-backup-unresolved`) is `documented`: product identity is
  bounded to My Wallet Apps Ltd. and Android package `io.gramwallet.app`, but no
  exact app version, exportable phrase length, generation algorithm, or
  source-to-package binding is established.
- MyTonWallet multichain (`bip39-multichain-generated`) is `documented`: the exact
  source generates 12-word BIP39 by default and can import 24 words, but a full
  TON-path known answer and release-wide mapping are not complete.
- Every other mandatory record keeps the terminal status and reason in
  [`docs/catalog.md`](../catalog.md). `documented`, `blocked`,
  `no-mnemonic-confirmed`, import-only, passkey, MPC, cloud, and private-key modes
  are never silently promoted.

For any unavailable mode, use the original trusted wallet's official backup and
recovery process. Match the exact product, platform, version, and mode. Never
give a complete phrase to Tessaveil, a test, CI, an agent, or a website.

### Candidate verification and launch

The hosted artifact container and files must start with
`Tessaveil-unsigned-synthetic-windows-v1-candidate-<source-sha>`. Keep together:

- `...-runtime.zip`;
- `...-compliance.zip`;
- `...-release-decision.json`;
- `...-manifest.json`.

The external manifest records the exact source SHA, names, byte sizes, and
SHA-256 values of both ZIPs, `Tessaveil.exe`, decision, CycloneDX SBOM, and
notices. Verify the manifest, both archive manifests, the independent
`verify.py --distribution` result, and GitHub provenance for all four hosted
subjects before extracting runtime. A hash detects changed bytes; it does not
establish publisher identity. `Tessaveil.exe` has no Authenticode signature.
A technical package PASS never changes the machine-readable real-data verdict.

Launch only `Tessaveil.exe` from the verified runtime directory. There is no
installer, updater, account, sidecar Qt DLL, network feature, or provider call.
Use a normal writable local NTFS directory outside cloud synchronization for
synthetic evaluation. Development-host NTFS evidence does not prove removable
NTFS/exFAT or power-loss durability.

### Create, open, and manage sheets

1. Acknowledge the synthetic-only warning. Create a new path ending in
   `.tessaveil-alpha` with an invented master password of at least 15 normalized
   Unicode characters, or open an existing synthetic vault. Wrong password and
   authenticated damage intentionally share one safe message; neither opens an
   empty vault.
2. Select one exact supported profile, 10 or 36 columns, and the supported row
   length. The core fills the full table with OS randomness. The app never
   constructs a complete phrase or order key.
3. A local UTF-8 custom dictionary is validated for decoding, line shape,
   normalization collisions, case/diacritic anomalies, and sufficient unique
   words. Its normalized snapshot is encrypted inside the sheet. Changing the
   list creates a fresh unverified replacement sheet; cells, protection, row
   state, and “Verified by me” never transfer.
4. Rename requires an unlocked protected state. Delete additionally requires
   the exact sheet name and confirmation. Sheet password protects against
   accidental edits after vault unlock; it is a verifier inside the encrypted
   payload, not a second encryption layer.
5. For Spin, enter one row, the same symbol twice, and one invented word. The
   complete row is regenerated. There is no validity/success flag, target marker,
   or saved completion state. A valid input is visibly placed, so the visible
   rows are not promised to be indistinguishable. Repeated attempts trigger a
   neutral correlation warning and can narrow the true word.
6. Set “Verified by me” only after checking recovery with the original trusted
   wallet or official hardware-wallet backup procedure. Tessaveil does not
   verify the phrase. Any Spin clears that assertion.
7. Save encrypts the complete state and protects sheets. Manual close/lock offers
   Save, Discard, or Cancel. A failed save retains the dirty session and previous
   authenticated file. Temporary remnants have a clear technical header and
   encrypted payload, not an open payload, but can preserve another table
   version.

Russian/English, system/light/dark theme, and 1/5/15/30-minute timeout settings
are available for the current protected state. Ordinary deactivation shows a
privacy cover; inactivity, Windows lock, and sleep perform actual lock and
discard unsaved changes, leaving the last saved file. Save before switching
away when you need pending changes.

### Backup, restore, and password rotation

- Backup is allowed only from a clean saved session. It reopens and authenticates
  the saved image, rejects aliases/self/overwrite/unsafe targets, and writes a
  **byte-identical encrypted redundancy copy**. Identical copies of one unchanged
  table add no new table-comparison signal, though every copy adds an exposure
  location. Verify that each copy is readable and keep copies in independent
  locations alongside a separate cold backup.
- Restore authenticates the source with its existing master password before it
  creates a new destination. It never bypasses the password, repairs damage, or
  overwrites an existing destination. Restore failure leaves source and
  destination unchanged.
- If the master password is lost, Tessaveil has no reset, recovery key, backdoor,
  order-key recovery, or “Verified by me” bypass. The vault may be permanently
  inaccessible; retain an independently verified original-wallet recovery path.
- Password rotation requires the current password and creates a new salt, DEK,
  wrapping nonce, payload nonce, and encrypted image. It does not revoke or
  erase old copies, their old passwords, already exposed plaintext, or rollback.
- Before editing a saved row or creating a replacement sheet, inventory old
  copies. If an attacker later obtains the password and decrypts different
  tables for the same phrase, unchanged real words can stand out. Regenerating
  every decoy does not remove this cross-version leakage. Do not destroy the
  only usable recovery copy merely to reduce version count.

### Protection boundary

A compromised computer can capture typed symbols/words, screen content, process
memory, IME buffers, paging, dumps, or recordings. Input clearing and privacy
cover are best effort. Tessaveil has no plaintext/CSV/screenshot/print export,
clipboard workflow, drag/drop secret import, telemetry, or network operation,
but it cannot control hostile software or OS capture. Stop using a suspected
device for secrets and follow the original wallet's incident procedure.

## Русский

### Точно поддерживаемые профили

Выбираются только следующие сочетания профиля, режима и версии. В каждом режиме
используются `ton-native-generated`, проверенные байты английского BIP39 как
допустимый словарь таблицы и ровно 24 строки. Общий словарь не делает разные
мнемонические схемы совместимыми.

| Профиль / режим | Платформа | Точная область исходников | Строки |
| --- | --- | --- | ---: |
| `mytonwallet-native / ton-native-generated` | web | `26.9.8-source-f042bcc06b84f0cec928a29795f1cb8bf60a3e9c` | 24 |
| `tonhub / ton-native-generated` | Android | `2.5.45-source-a2503f79d14868d65349ad7035d18389c6e2f996` | 24 |
| `tonkeeper-classic / ton-native-generated` | web | `source-4942adcdcddf55d57e3d3fc3676f019caf87357e` | 24 |

Приоритетные, но недоступные режимы:

- Tonkeeper Multichain (`bip39-multichain-generated`) имеет статус `documented`:
  официально подтверждён отдельный мультичейн-кошелёк, но не установлены точная
  платформа/версия, число генерируемых слов, границы версий и полный known answer.
  Импорт BIP39 не доказывает генерацию.
- Gram Wallet (`mnemonic-backup-unresolved`) — `documented`: идентичность
  ограничена My Wallet Apps Ltd. и Android-пакетом `io.gramwallet.app`, но нет
  точной версии, длины экспортируемой фразы, алгоритма генерации и связи
  исходников с пакетом.
- Мультичейн MyTonWallet (`bip39-multichain-generated`) — `documented`: точный
  срез исходников по умолчанию создаёт 12 слов BIP39 и импортирует 24, но нет
  полного known answer пути TON и привязки ко всем выпускам.
- Конечный статус и причина остальных обязательных записей находятся в
  [`docs/catalog.ru.md`](../catalog.ru.md). `documented`, `blocked`,
  `no-mnemonic-confirmed`, import-only, passkey, MPC, cloud и private-key режимы
  не повышаются скрыто.

Для недоступного режима используйте официальное резервирование/восстановление
исходного доверенного кошелька и сверяйте продукт, платформу, версию и режим.
Никогда не передавайте полную фразу Tessaveil, тесту, CI, агенту или сайту.

### Проверка кандидата и запуск

Имена контейнера и файлов hosted-артефакта начинаются с
`Tessaveil-unsigned-synthetic-windows-v1-candidate-<source-sha>`. Храните вместе
`-runtime.zip`, `-compliance.zip`, `-release-decision.json` и `-manifest.json`.
Внешний манифест содержит точный source SHA, имена, размеры и SHA-256 обоих ZIP,
`Tessaveil.exe`, решения, CycloneDX SBOM и уведомлений. До распаковки runtime
проверьте манифест, внутренние манифесты, `verify.py --distribution` и GitHub
provenance всех четырёх hosted-файлов. Хеш обнаруживает изменение байтов, но не
удостоверяет издателя. У EXE нет Authenticode. Технический PASS упаковки не
меняет machine-readable вердикт по реальным данным.

Запускайте только `Tessaveil.exe` из проверенного runtime-каталога. У кандидата
нет установщика, обновлятора, аккаунта, боковых Qt DLL, сети или provider calls.
Для синтетической проверки используйте обычный доступный для записи локальный
NTFS вне облачной синхронизации. Это не доказывает съёмные NTFS/exFAT и потерю
питания.

### Создание, открытие и листы

1. Подтвердите предупреждение и создайте новый `.tessaveil-alpha` с придуманным
   мастер-паролем минимум из 15 нормализованных Unicode-символов либо откройте
   синтетический файл. Неверный пароль и нарушение аутентичности имеют одно
   безопасное сообщение и никогда не открывают «пустое» хранилище.
2. Выберите точный профиль, 10/36 столбцов и допустимую длину. Таблица целиком
   заполняется случайностью ОС; полная фраза и ключ порядка не создаются.
3. Локальный UTF-8 словарь проверяется на декодирование, форму строк, коллизии
   нормализации, регистр/диакритику и число уникальных слов. Его снимок шифруется
   в листе. Новый список создаёт отдельный непроверенный лист без переноса ячеек,
   защиты, состояния строк и отметки «Проверено мной».
4. Переименование требует разблокированного листа. Удаление дополнительно требует
   точного имени и подтверждения. Пароль листа — проверочный признак внутри уже
   зашифрованного payload, а не второй слой шифрования.
5. Spin принимает одну строку, два одинаковых символа и одно слово. Вся строка
   генерируется заново без флага допустимости/успеха, целевой метки или сохранённой
   отметки. Допустимое слово видно в строке, поэтому содержимое не обещано
   неразличимым. Повторы получают нейтральное предупреждение и могут сузить поиск.
6. Ставьте «Проверено мной» только после проверки восстановления исходным
   доверенным кошельком или официальной процедурой аппаратного кошелька. Это не
   криптографическая проверка Tessaveil; любой Spin снимает отметку.
7. Save шифрует состояние и защищает листы. Ручные Close/Lock предлагают Save,
   Discard или Cancel. Ошибка записи сохраняет dirty-сессию и предыдущий
   аутентичный файл. Временный остаток содержит открытый технический заголовок и
   шифротекст, а не открытый payload, но может сохранить другую версию таблицы.

Доступны русский/английский, системная/светлая/тёмная тема и таймауты 1/5/15/30
минут. Обычная деактивация показывает защитную завесу; бездействие, блокировка
Windows и сон действительно блокируют и отбрасывают несохранённые изменения,
оставляя последний сохранённый файл. Сохраняйтесь до переключения приложения.

### Резервная копия, восстановление и смена пароля

- Backup доступен только для чистой сохранённой сессии. Образ повторно открывается
  и аутентифицируется; запрещены self/alias/overwrite/опасная цель. Создаётся
  **побайтно идентичная зашифрованная резервная копия**. Идентичные копии одной
  неизменённой таблицы не дают нового сигнала сравнения, но добавляют места
  возможного раскрытия. Проверяйте читаемость и храните раздельно вместе с
  независимой холодной копией.
- Restore сначала аутентифицирует источник его действующим мастер-паролем и лишь
  затем создаёт новый файл. Он не обходит пароль, не чинит повреждение и не
  перезаписывает существующую цель. Ошибка не меняет источник и цель.
- Потерянный мастер-пароль нельзя сбросить или восстановить через backdoor, ключ
  порядка, пароль листа либо «Проверено мной». Файл может стать недоступным
  навсегда; заранее проверьте независимый путь восстановления исходного кошелька.
- Смена пароля требует текущий пароль и создаёт новые соль, DEK, nonce обёртки и
  payload и новый зашифрованный образ. Она не отзывает и не стирает старые копии,
  их старые пароли, уже раскрытый текст или возможность отката.
- До правки сохранённой строки или нового заменяющего листа учтите старые копии.
  Если атакующий позднее расшифрует разные таблицы одной фразы, неизменные
  настоящие слова могут выделиться. Обновление всех ложных слов не устраняет
  сравнение версий. Не уничтожайте единственную пригодную копию восстановления.

### Граница защиты

Скомпрометированный компьютер может перехватить символы/слова, экран, память
процесса, IME, подкачку, дампы или запись. Очистка ввода и завеса — best effort.
Нет plaintext/CSV/screenshot/print export, clipboard workflow, drag/drop секретов,
телеметрии и сети, но Tessaveil не управляет враждебной ОС. Прекратите работу с
секретами на подозрительном устройстве и следуйте incident-процедуре кошелька.
