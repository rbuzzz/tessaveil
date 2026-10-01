#include "strings.h"
#include <QHash>

namespace {
struct Copy {
  const char *en;
  const char *ru;
};

const QHash<QString, Copy> &catalog() {
  static const QHash<QString, Copy> values{
      {"title", {"Tessaveil — unsigned synthetic candidate", "Tessaveil — неподписанный синтетический кандидат"}},
      {"fatal", {"The session is unavailable. Close and restart Tessaveil.", "Сеанс недоступен. Закройте и перезапустите Tessaveil."}},
      {"inputTooLong", {"Input exceeds the 4096-byte UTF-8 limit. Shorten it and try again.", "Ввод превышает предел 4096 байт UTF-8. Сократите его и повторите."}},
      {"stateDirty", {"Open / unsaved changes", "Открыто / есть несохранённые изменения"}},
      {"stateClean", {"Open / saved", "Открыто / сохранено"}},
      {"stateLocked", {"Locked — enter master password to reopen", "Заблокировано — введите мастер-пароль"}},
      {"stateClosed", {"Closed", "Закрыто"}},
      {"stateA11y", {"State: %1", "Состояние: %1"}},
      {"messageA11y", {"Status and error announcement", "Объявление состояния и ошибки"}},
      {"sheetProtected", {"Protected", "Защищён"}},
      {"sheetEditable", {"Editing enabled", "Редактирование разрешено"}},
      {"sheetVerified", {"Verified by me", "Проверено мной"}},
      {"sheetUnverified", {"Not independently verified", "Независимо не проверено"}},
      {"noSheet", {"No sheet yet", "Листов пока нет"}},
      {"unsavedTitle", {"Unsaved synthetic changes", "Несохранённые синтетические изменения"}},
      {"unsavedPrompt", {"Save before closing or locking? Automatic inactivity, Windows lock or sleep discards unsaved changes.", "Сохранить перед закрытием или блокировкой? Автоблокировка, блокировка Windows и сон отбрасывают несохранённые изменения."}},
      {"privacyTitle", {"Tessaveil is covered while inactive", "Tessaveil скрыт, пока приложение неактивно"}},
      {"privacyBody", {"Return to Tessaveil to refresh the timeout state. Ordinary application deactivation does not change vault data.", "Вернитесь в Tessaveil для проверки тайм-аута. Обычная деактивация приложения не меняет данные хранилища."}},
      {"privacyA11y", {"Privacy cover", "Экран конфиденциальности"}},
      {"banner", {"TESSAVEIL / UNSIGNED ENGINEERING CANDIDATE — synthetic data only; never use real assets. Schema 2 and .tessaveil-alpha remain experimental. Release and format freeze: NO-GO.", "TESSAVEIL / НЕПОДПИСАННЫЙ ИНЖЕНЕРНЫЙ КАНДИДАТ — только синтетические данные; не используйте реальные активы. Schema 2 и .tessaveil-alpha остаются экспериментальными. Релиз и фиксация формата: NO-GO."}},
      {"warning", {"Development-host candidate, not a security release. Different saved tables can reveal unchanged words after password disclosure. Sheet passwords prevent accidental edits, not master-password compromise. Inactivity, Windows lock and sleep discard unsaved changes. Memory clearing is best effort; a compromised OS can capture input.", "Кандидат для рабочего компьютера, не защищённый релиз. Разные сохранённые таблицы могут раскрыть неизменные слова после раскрытия пароля. Пароль листа предотвращает случайные правки, но не компрометацию мастер-пароля. Бездействие, блокировка Windows и сон отбрасывают несохранённые изменения. Очистка памяти выполняется по мере возможности; скомпрометированная ОС может перехватить ввод."}},
      {"warningAccept", {"I understand — use synthetic data only", "Понимаю — использовать только синтетические данные"}},
      {"pathA11y", {"Vault path on development local NTFS", "Путь к хранилищу на локальном тестовом NTFS"}},
      {"pathPlaceholder", {"Selected .tessaveil-alpha ciphertext file", "Выбранный файл шифротекста .tessaveil-alpha"}},
      {"vaultNameA11y", {"Vault name", "Название хранилища"}},
      {"vaultNamePlaceholder", {"Vault name", "Название хранилища"}},
      {"defaultVaultName", {"Synthetic vault", "Синтетическое хранилище"}},
      {"defaultSheetName", {"Synthetic sheet", "Синтетический лист"}},
      {"confirmMasterA11y", {"Confirm new master password", "Подтверждение нового мастер-пароля"}},
      {"confirmMasterPlaceholder", {"Confirm new master password", "Повторите новый мастер-пароль"}},
      {"chooseCreatePath", {"Choose new ciphertext file", "Выбрать новый файл шифротекста"}},
      {"chooseOpenPath", {"Choose existing ciphertext file", "Выбрать существующий файл шифротекста"}},
      {"masterA11y", {"Master password", "Мастер-пароль"}},
      {"masterPlaceholder", {"Master password", "Мастер-пароль"}},
      {"wordA11y", {"One word", "Одно слово"}},
      {"sheetCredentialA11y", {"Sheet password or master credential", "Пароль листа или мастер-пароль"}},
      {"symbolA11y", {"Column symbol confirmation", "Подтверждение символа столбца"}},
      {"create", {"&Create vault", "&Создать хранилище"}},
      {"open", {"&Open vault", "&Открыть хранилище"}},
      {"unlock", {"&Unlock vault", "&Разблокировать"}},
      {"save", {"&Save", "&Сохранить"}},
      {"close", {"Close vault", "Закрыть хранилище"}},
      {"lock", {"&Lock", "&Заблокировать"}},
      {"inactivity", {"Inactivity lock:", "Блокировка при бездействии:"}},
      {"minutesA11y", {"Inactivity lock minutes", "Минуты до блокировки"}},
      {"minutes", {"%1 minutes", "%1 мин"}},
      {"sheetsHeading", {"SHEETS / CANDIDATE MATRIX", "ЛИСТЫ / МАТРИЦА КАНДИДАТА"}},
      {"currentSheetA11y", {"Current sheet", "Текущий лист"}},
      {"nextSheet", {"Next sheet", "Следующий лист"}},
      {"profileA11y", {"Exact product, platform, version, status and mode; unavailable reasons included", "Точные продукт, платформа, версия, статус и режим; причины недоступности показаны"}},
      {"profileDetailsA11y", {"Exact profile details", "Точные сведения профиля"}},
      {"profileFilterLabel", {"Find an exact wallet profile", "Найти точный профиль кошелька"}},
      {"profileFilterA11y", {"Search all wallet profiles, including unavailable profiles", "Поиск по всем профилям кошельков, включая недоступные"}},
      {"profileFilterPlaceholder", {"Product, platform, version, status, mode or ID", "Продукт, платформа, версия, статус, режим или ID"}},
      {"profileNoMatches", {"No profile matches this search. Clear the search to inspect all profiles.", "Нет профилей по этому запросу. Очистите поиск, чтобы просмотреть все профили."}},
      {"reasonDocumented", {"Creation in Tessaveil is unavailable. Evidence exists, but it is insufficient to support Tessaveil sheet creation for this exact product, platform, version and mode. Creation remains unavailable; verify this exact combination in the original wallet and use the original wallet's own backup/export workflow.", "Создание профиля в Tessaveil недоступно. Подтверждающие сведения существуют, но их недостаточно для создания листа Tessaveil для этого точного сочетания продукта, платформы, версии и режима. Создание остаётся недоступным; проверьте это точное сочетание в исходном кошельке и используйте собственный процесс резервного копирования/экспорта исходного кошелька."}},
      {"reasonBlocked", {"Creation in Tessaveil is unavailable because the evidence is incomplete or conflicting. Verify the exact mode and version, then use the original wallet's own backup/export process.", "Создание профиля в Tessaveil недоступно: сведения неполны или противоречивы. Проверьте точный режим и версию, затем используйте собственный процесс резервного копирования/экспорта исходного кошелька."}},
      {"reasonNoMnemonic", {"Creation in Tessaveil is unavailable because this mode is documented as not using a mnemonic. Confirm the exact mode, then use the original wallet's own backup/export process.", "Создание профиля в Tessaveil недоступно: для этого режима документировано отсутствие мнемонической фразы. Подтвердите точный режим, затем используйте собственный процесс резервного копирования/экспорта исходного кошелька."}},
      {"reasonUnknown", {"Availability details cannot be displayed safely. Verify the exact mode and version in the original wallet.", "Сведения о доступности нельзя безопасно показать. Проверьте точный режим и версию в исходном кошельке."}},
      {"sheetNameA11y", {"Sheet name", "Название листа"}},
      {"columnA11y", {"Column count", "Количество столбцов"}},
      {"columns10", {"10 columns", "10 столбцов"}},
      {"columns36", {"36 columns", "36 столбцов"}},
      {"lengthA11y", {"Allowed row length for exact profile", "Разрешённая длина точного профиля"}},
      {"rows", {"%1 rows", "%1 строк"}},
      {"addSheet", {"Add synthetic sheet", "Добавить синтетический лист"}},
      {"sheetPasswordPlaceholder", {"Sheet password / master credential", "Пароль листа / мастер-пароль"}},
      {"setPassword", {"Set password", "Задать пароль"}},
      {"protect", {"Protect", "Защитить"}},
      {"unlockSheet", {"Unlock sheet", "Разблокировать лист"}},
      {"useMaster", {"Use master", "Использовать мастер-пароль"}},
      {"protectionInfo", {"Sheet protection prevents accidental edits, not disclosure after master-password compromise.", "Защита листа предотвращает случайные правки, но не раскрытие после компрометации мастер-пароля."}},
      {"verificationConsent", {"I independently checked recovery", "Я независимо проверил восстановление"}},
      {"verificationGuide", {"Verify only through the original trusted wallet or official hardware-wallet backup check. Tessaveil performs no cryptographic verification; never paste a complete phrase here.", "Проверяйте только через исходный доверенный кошелёк или официальную проверку резервной копии аппаратного кошелька. Tessaveil не выполняет криптографическую проверку; никогда не вставляйте сюда полную фразу."}},
      {"verifiedButton", {"Verified by me", "Проверено мной"}},
      {"unverifyButton", {"Remove Verified by me", "Снять отметку «Проверено мной»"}},
      {"tableA11y", {"Current decoy table. No target cells are marked.", "Текущая таблица ложных слов. Целевые ячейки не отмечены."}},
      {"spinWarning", {"ONE ROW / SPIN — repeated observations and different saved copies can reveal unchanged words. Re-randomizing decoys does not remove this risk.", "ОДНА СТРОКА / SPIN — повторные наблюдения и разные сохранённые копии могут раскрыть неизменные слова. Повторная рандомизация ложных слов не устраняет этот риск."}},
      {"spinConsent", {"I understand the row-comparison risk (required for each Spin)", "Я понимаю риск сравнения строк (для каждой попытки Spin)"}},
      {"rowPrefix", {"Row ", "Строка "}},
      {"rowA11y", {"Row number", "Номер строки"}},
      {"symbolPlaceholder", {"Symbol", "Символ"}},
      {"repeatPlaceholder", {"Repeat", "Повтор"}},
      {"wordPlaceholder", {"One word only", "Только одно слово"}},
      {"spin", {"Spin", "Spin"}},
      {"spinGuide", {"Use ASCII 0–9 / A–Z. Check the keyboard layout. No validity or target signal is shown.", "Используйте ASCII 0–9 / A–Z. Проверьте раскладку. Сигнал допустимости или цели не показывается."}},
      {"spinAck", {"Read and acknowledge the row-comparison warning before Spin.", "Прочитайте и подтвердите предупреждение о сравнении строк перед Spin."}},
      {"lockedDiscarded", {"Locked. Unsaved synthetic changes were discarded; the last saved vault is unchanged.", "Заблокировано. Несохранённые синтетические изменения отброшены; последний сохранённый файл не изменён."}},
      {"sessionMonitor", {"Windows session monitoring is unavailable. Close Tessaveil; opening a vault is disabled.", "Мониторинг сеанса Windows недоступен. Закройте Tessaveil; открытие хранилища отключено."}},
      {"localeA11y", {"Interface language", "Язык интерфейса"}},
      {"languageEnglish", {"English", "English"}},
      {"languageRussian", {"Russian", "Русский"}},
      {"themeA11y", {"Color theme", "Цветовая тема"}},
      {"themeSystem", {"System", "Системная"}},
      {"themeLight", {"Light", "Светлая"}},
      {"themeDark", {"Dark", "Тёмная"}},
      {"saved", {"Vault saved.", "Хранилище сохранено."}},
      {"backup", {"Create encrypted backup", "Создать зашифрованную резервную копию"}},
      {"restore", {"Restore encrypted backup", "Восстановить зашифрованную резервную копию"}},
      {"changePassword", {"Change master password", "Сменить мастер-пароль"}},
      {"customSheet", {"Add custom dictionary sheet", "Добавить лист пользовательского словаря"}},
      {"replaceDictionary", {"Create replacement from revised dictionary", "Создать замену из изменённого словаря"}},
      {"renameSheet", {"Rename sheet", "Переименовать лист"}},
      {"deleteSheet", {"Delete sheet", "Удалить лист"}},
      {"backupWarning", {"Keep redundant copies of the same unchanged table. Different versions can reveal invariant words after password disclosure.", "Храните резервные копии одной неизменённой таблицы. Разные версии могут раскрыть неизменные слова после раскрытия пароля."}},
      {"rotationWarning", {"Password rotation re-encrypts the current file but does not revoke old backups or their old passwords.", "Смена пароля повторно шифрует текущий файл, но не отзывает старые копии или их прежние пароли."}},
      {"restorePasswordGuidance", {"The selected backup requires the original/old master password that was used when that backup was created.", "Для выбранной резервной копии нужен исходный/старый мастер-пароль, который использовался при её создании."}},
      {"customWarning", {"A revised dictionary creates a fresh unverified sheet. Nothing transfers; retaining different tables for one phrase enables comparison risk.", "Изменённый словарь создаёт новый непроверенный лист. Ничего не переносится; сохранение разных таблиц одной фразы создаёт риск сравнения."}},
      {"cipherFilter", {"Tessaveil engineering vault (*.tessaveil-alpha)", "Инженерное хранилище Tessaveil (*.tessaveil-alpha)"}},
      {"dictionaryFilter", {"UTF-8 word list (*.txt);;All files (*)", "Список слов UTF-8 (*.txt);;Все файлы (*)"}},
      {"selectNewVault", {"Choose a new encrypted vault", "Выберите новое зашифрованное хранилище"}},
      {"selectVault", {"Choose an encrypted vault", "Выберите зашифрованное хранилище"}},
      {"selectBackup", {"Choose a new encrypted backup", "Выберите новую зашифрованную резервную копию"}},
      {"selectRestoreSource", {"Choose an encrypted backup to restore", "Выберите зашифрованную копию для восстановления"}},
      {"selectRestoreDestination", {"Choose a new restored vault", "Выберите новый восстановленный файл"}},
      {"selectDictionary", {"Choose a local UTF-8 dictionary", "Выберите локальный словарь UTF-8"}},
      {"pathLabel", {"Ciphertext path", "Путь к шифротексту"}},
      {"sourceLabel", {"Encrypted backup", "Зашифрованная резервная копия"}},
      {"destinationLabel", {"New destination", "Новый файл назначения"}},
      {"vaultSourceLabel", {"Encrypted vault file", "Файл зашифрованного хранилища"}},
      {"vaultDestinationLabel", {"New encrypted vault file", "Новый файл зашифрованного хранилища"}},
      {"dictionaryLabel", {"Local UTF-8 dictionary", "Локальный словарь UTF-8"}},
      {"currentPassword", {"Current master password", "Текущий мастер-пароль"}},
      {"newPassword", {"New master password", "Новый мастер-пароль"}},
      {"confirmPassword", {"Confirm new master password", "Повторите новый мастер-пароль"}},
      {"passwordMismatch", {"The two new password entries do not match.", "Введённые новые пароли не совпадают."}},
      {"cancelled", {"Operation cancelled; the current session is unchanged.", "Операция отменена; текущий сеанс не изменён."}},
      {"backupComplete", {"Encrypted redundancy copy created.", "Зашифрованная резервная копия создана."}},
      {"restoreComplete", {"Encrypted backup restored and opened.", "Зашифрованная резервная копия восстановлена и открыта."}},
      {"rotationComplete", {"Master password changed; old copies and passwords are not revoked.", "Мастер-пароль изменён; старые копии и пароли не отозваны."}},
      {"customName", {"New sheet name", "Название нового листа"}},
      {"customRows", {"Rows", "Строки"}},
      {"customColumns", {"Columns", "Столбцы"}},
      {"replacementName", {"Replacement sheet name", "Название заменяющего листа"}},
      {"replacementAck", {"I understand this creates a fresh unverified sheet and does not change the old snapshot", "Я понимаю, что создаётся новый непроверенный лист, а старый снимок не меняется"}},
      {"renameName", {"New sheet name", "Новое название листа"}},
      {"deleteExactName", {"Type the exact current sheet name", "Введите точное текущее название листа"}},
      {"deleteFinal", {"Final confirmation: delete this sheet from the current vault", "Окончательное подтверждение: удалить этот лист из текущего хранилища"}},
      {"browse", {"Browse…", "Обзор…"}},
      {"dialogOk", {"Continue", "Продолжить"}},
      {"dialogCancel", {"Cancel", "Отмена"}},
      {"dialogSave", {"Save", "Сохранить"}},
      {"dialogDiscard", {"Discard", "Не сохранять"}},
  };
  return values;
}

const QHash<QString, Copy> &errors() {
  static const QHash<QString, Copy> values{
      {"invalid-header", {"This is not a supported Tessaveil vault header.", "Заголовок файла Tessaveil не поддерживается."}},
      {"unsupported-version", {"This vault version is not supported.", "Версия хранилища не поддерживается."}},
      {"kdf-out-of-bounds", {"The vault requests out-of-policy KDF parameters.", "Хранилище запрашивает параметры KDF вне допустимых границ."}},
      {"unsupported-kdf", {"The KDF profile is unsupported or too resource-intensive.", "Профиль KDF не поддерживается или слишком ресурсоёмок."}},
      {"truncated", {"The vault file is truncated.", "Файл хранилища обрезан."}},
      {"too-large", {"The selected file or value exceeds the supported bound.", "Выбранный файл или значение превышает допустимый предел."}},
      {"authentication", {"The password is incorrect or the vault is damaged.", "Пароль неверен или хранилище повреждено."}},
      {"invalid-password", {"The password value is invalid.", "Недопустимое значение пароля."}},
      {"password-policy", {"Use a master password of at least 15 Unicode characters.", "Используйте мастер-пароль длиной не менее 15 символов Unicode."}},
      {"access-denied", {"The operation is not allowed in the current state.", "Операция недоступна в текущем состоянии."}},
      {"insufficient-space", {"There is not enough space to complete the authenticated write.", "Недостаточно места для завершения аутентифицированной записи."}},
      {"io", {"The file operation failed. The previous valid vault is unchanged.", "Операция с файлом завершилась ошибкой. Предыдущее корректное хранилище не изменено."}},
      {"already-exists", {"The destination already exists; choose a new file.", "Файл назначения уже существует; выберите новый файл."}},
      {"invalid-path", {"Choose a valid local ciphertext path.", "Выберите корректный локальный путь к шифротексту."}},
      {"unsupported-filesystem", {"This storage target is not approved for updates.", "Это место хранения не разрешено для обновлений."}},
      {"locked", {"Unlock the vault or sheet before continuing.", "Разблокируйте хранилище или лист."}},
      {"unsaved-changes", {"Save the current changes before making an encrypted backup.", "Сохраните текущие изменения перед созданием зашифрованной резервной копии."}},
      {"invalid-payload", {"The requested value or operation is invalid.", "Запрошенное значение или операция недопустимы."}},
      {"temporary-remains", {"Saving failed. A temporary file may contain a clear technical header and encrypted payload; treat it as a sensitive version.", "Сохранение не выполнено. Временный файл может содержать открытый технический заголовок и зашифрованную полезную нагрузку; считайте его чувствительной версией."}},
  };
  return values;
}

QString choose(const QString &locale, const Copy &copy) {
  return QString::fromUtf8(locale == "ru" ? copy.ru : copy.en);
}
} // namespace

QString uiText(const QString &locale, const char *key) {
  const auto found = catalog().constFind(QString::fromLatin1(key));
  return found == catalog().cend() ? QString::fromLatin1(key)
                                   : choose(locale, found.value());
}

QString uiErrorText(const QString &locale, const QString &key) {
  const auto found = errors().constFind(key);
  return found == errors().cend() ? uiText(locale, "fatal")
                                  : choose(locale, found.value());
}

QString uiProfileReason(const QString &locale, const QString &reason) {
  if (reason.isEmpty())
    return {};
  if (reason == "wallet-status:documented")
    return uiText(locale, "reasonDocumented");
  if (reason == "wallet-status:blocked")
    return uiText(locale, "reasonBlocked");
  if (reason == "wallet-status:no-mnemonic-confirmed")
    return uiText(locale, "reasonNoMnemonic");
  return uiText(locale, "reasonUnknown");
}
