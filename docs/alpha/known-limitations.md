# Known limitations — unsigned synthetic Windows v1 candidate

Verdict: **NO-GO для реальных данных**. No real funds, recovery phrases,
order keys, private keys, wallet backups, or user vaults. This is not RC/stable,
has no Authenticode signature, and makes no final format/KDF/migration promise.

Security audit: not yet independently completed

[English](#english) · [Русский](#русский)

## English

- Only three exact 24-row TON-native profiles listed in the user guide are
  selectable. Tonkeeper Multichain, Gram Wallet, MyTonWallet multichain, and the
  remaining mandatory catalogue records keep their actual non-selectable status.
  Import or shared word lists are not generation evidence.
- Schema 2, `.tessaveil-alpha`, and Argon2id 65,536 KiB / 3 iterations /
  parallelism 4 are engineering identifiers, not frozen mobile-compatible
  promises. Two physical Android classes, two physical iPhone classes, and a
  Mac/Xcode host have not completed the shared-vault/KDF protocol.
- Clean Windows 10 22H2 and Windows 11 execution is unverified. Development-host
  and GitHub-hosted Windows Server results do not substitute. Trusted Windows 10
  use would require current ESU updates after ordinary support ended.
- Local fixed NTFS process-boundary tests do not prove removable NTFS, removable
  exFAT, system-call atomicity, controlled power loss, or secure deletion. FAT32,
  network shares, cloud-synchronized folders, and untested storage have no
  atomicity promise.
- Exact-candidate packet, TEMP, child-process, file-event, sanitized startup-log,
  and independent Narrator/real-display scaling evidence is absent. Static lack
  of a network module and an empty snapshot do not prove zero transient events.
- Exact Segoe UI/Consolas rendering remains blocked in the Figma handoff; the
  preview uses documented Inter/Roboto Mono substitutes. WCAG-oriented design
  and automated UIA are not independent accessibility certification.
- Parser corpora and negative tests are present, but no completed sustained
  sanitizer-backed fuzz campaign or independent security audit clears the exact
  candidate. SignPath has not accepted the project and the EXE is unsigned.
- Input clearing, masked controls, privacy cover, and lock are best effort. A
  compromised OS, keylogger, hostile IME, screen recorder, memory reader, paging,
  or dump can expose secrets. Tessaveil cannot repair an already compromised
  original wallet or phrase.
- Restore never bypasses the master password. Losing it can make the vault
  permanently inaccessible. A sheet password is not a second encryption layer.
  Password rotation does not revoke old files or old passwords, detect rollback,
  or erase copies.
- Identical redundancy copies preserve one table, but every location adds
  exposure. Different saved tables, replacement sheets, or interrupted-save
  remnants for the same phrase can reveal invariant words after password
  disclosure; full decoy re-randomization does not remove that risk.
- There is no GitHub Release, tag, installer, updater, stable publication, or
  guaranteed byte-for-byte reproducibility across hosts. A package gate PASS
  proves only the audited package bytes; real-data authorization remains false
  until all 29 decision rows pass with exact receipts.

## Русский

- Выбираются только три точных 24-строчных TON-native профиля из инструкции.
  Tonkeeper Multichain, Gram Wallet, мультичейн MyTonWallet и остальные записи
  сохраняют фактический недоступный статус. Импорт и общий словарь не доказывают
  генерацию.
- Schema 2, `.tessaveil-alpha` и Argon2id 65 536 KiB / 3 итерации / parallelism 4
  — инженерные параметры, а не зафиксированное обещание мобильной совместимости.
  Два класса физических Android, два класса iPhone и Mac/Xcode ещё не выполнили
  протокол общего vault/KDF.
- Запуск на чистых Windows 10 22H2 и Windows 11 не проверен. Рабочий компьютер и
  GitHub-hosted Windows Server их не заменяют. Для доверенного Windows 10 после
  конца обычной поддержки потребуются актуальные ESU-обновления.
- Локальные process-boundary тесты фиксированного NTFS не доказывают съёмные NTFS,
  exFAT, атомарность внутри системного вызова, потерю питания и безопасное
  удаление. FAT32, сеть, облачная синхронизация и непроверенные носители не
  получают обещания атомарности.
- Нет полной трассы точного кандидата по пакетам, TEMP, дочерним процессам,
  файловым событиям и очищенным startup logs, а также независимой проверки
  Narrator/реального масштаба. Отсутствие сетевого модуля и пустой снимок не
  доказывают отсутствие кратковременных событий.
- Точная отрисовка Segoe UI/Consolas в Figma blocked; макет использует отмеченные
  замены Inter/Roboto Mono. WCAG-направление и автоматический UIA — не независимая
  сертификация доступности.
- Есть parser corpora и негативные тесты, но нет завершённого длительного
  sanitizer-fuzzing и независимого аудита точного кандидата. SignPath не принял
  проект; EXE не подписан.
- Очистка ввода, маскирование, завеса и блокировка — best effort. Враждебная ОС,
  keylogger, IME, запись экрана, чтение памяти, подкачка и дампы могут раскрыть
  секреты. Tessaveil не исправляет уже скомпрометированный кошелёк или фразу.
- Restore никогда не обходит мастер-пароль; его потеря может быть окончательной.
  Пароль листа — не второй слой шифрования. Смена мастер-пароля не отзывает
  старые файлы/пароли, не обнаруживает откат и не стирает копии.
- Идентичные резервные копии сохраняют одну таблицу, но добавляют места раскрытия.
  Разные версии, заменяющие листы и остатки прерванной записи одной фразы после
  раскрытия пароля могут выделить неизменные слова; полная рандомизация ложных
  слов риск не устраняет.
- Нет GitHub Release, тега, установщика, обновлятора, stable-публикации и
  гарантированной побайтной воспроизводимости между хостами. PASS упаковки
  относится только к проверенным байтам; реальные данные запрещены, пока все
  29 строк решения не получили pass с точными receipts.
