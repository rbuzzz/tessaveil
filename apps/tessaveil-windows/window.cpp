#include "window.h"
#include "bridge.h"
#include "ui/strings.h"
#include "ui/theme.h"
#include <QtWidgets>
#include <cstring>
#include <memory>
#include <windows.h>
#include <wtsapi32.h>

namespace {
void wipe(void *p, size_t size) { SecureZeroMemory(p, size); }
quintptr ownProcessForegroundWindow(quintptr) {
  const HWND foreground = GetForegroundWindow();
  if (!foreground)
    return 0;
  DWORD processId = 0;
  GetWindowThreadProcessId(foreground, &processId);
  return processId == GetCurrentProcessId()
             ? reinterpret_cast<quintptr>(foreground)
             : 0;
}
bool field(TvInput &in, int slot, QString value) {
  auto bytes = value.toUtf8();
  const bool fits = bytes.size() <= sizeof(in.data[slot]);
  if (fits) {
    in.len[slot] = static_cast<uint32_t>(bytes.size());
    std::memcpy(in.data[slot], bytes.constData(), bytes.size());
  }
  wipe(bytes.data(), bytes.size());
  wipe(value.data(), value.size() * sizeof(QChar));
  return fits;
}
class Secret : public QLineEdit {
public:
  explicit Secret(const QString &name) {
    setObjectName(name);
    setEchoMode(Password);
    setMaxLength(4096);
    setContextMenuPolicy(Qt::NoContextMenu);
    setAcceptDrops(false);
    setDragEnabled(false);
    setInputMethodHints(Qt::ImhHiddenText | Qt::ImhSensitiveData |
                        Qt::ImhNoPredictiveText);
  }
  bool consume(TvInput &in, int slot) {
    QString value = text();
    setText(QString());
    return field(in, slot, std::move(value));
  }
  void erase() {
    QString value = text();
    setText(QString()); // Also drops the widget's undo state.
    wipe(value.data(), value.size() * sizeof(QChar));
  }

protected:
  bool event(QEvent *e) override {
    if (e->type() == QEvent::ShortcutOverride ||
        e->type() == QEvent::KeyPress) {
      auto k = static_cast<QKeyEvent *>(e);
      if (k->matches(QKeySequence::Copy) || k->matches(QKeySequence::Cut) ||
          k->matches(QKeySequence::Paste) || k->matches(QKeySequence::Undo) ||
          k->matches(QKeySequence::Redo)) {
        e->accept();
        return true;
      }
    }
    if (e->type() == QEvent::ContextMenu || e->type() == QEvent::DragEnter ||
        e->type() == QEvent::Drop) {
      e->ignore();
      return true;
    }
    return QLineEdit::event(e);
  }
};
class Bridge {
  uint64_t id = tv_new();

public:
  TvReply state{};
  ~Bridge() {
    tv_free(id);
    wipe(&state, sizeof(state));
  }
  int request(uint32_t op, uint32_t a, uint32_t b, TvInput &in, TvReply &out) {
    int code = tv_call(id, op, a, b, &in, &out);
    wipe(&in, sizeof(in));
    if (out.abi != 1 || out.text_len > 4096) {
      wipe(&out, sizeof(out));
      return -1;
    }
    return code;
  }
  int action(uint32_t op, uint32_t a, uint32_t b, TvInput &in,
             QString &message, QString *successText = nullptr) {
    TvReply out{};
    int code = request(op, a, b, in, out);
    state = out;
    wipe(state.text, sizeof(state.text));
    state.text_len = 0;
    if (code)
      message = code < 0 ? "fatal"
                         : QString::fromUtf8(
                               reinterpret_cast<char *>(out.text), out.text_len);
    else {
      message.clear();
      if (successText)
        *successText =
            QString::fromUtf8(reinterpret_cast<char *>(out.text), out.text_len);
    }
    wipe(&out, sizeof(out));
    return code;
  }
  QString query(uint32_t op, uint32_t a = 0, uint32_t b = 0) {
    TvInput in{};
    TvReply out{};
    int code = request(op, a, b, in, out);
    QString value = code == 0
                        ? QString::fromUtf8(reinterpret_cast<char *>(out.text),
                                            out.text_len)
                        : QString();
    wipe(&out, sizeof(out));
    return value;
  }
};
class TableModel : public QAbstractTableModel {
  Bridge &core;
  int rows = 0, columns = 0;

public:
  explicit TableModel(Bridge &core, QObject *parent)
      : QAbstractTableModel(parent), core(core) {}
  void refresh() {
    beginResetModel();
    rows = static_cast<int>(core.state.rows);
    columns = static_cast<int>(core.state.columns);
    endResetModel();
  }
  int rowCount(const QModelIndex &parent = {}) const override {
    return parent.isValid() ? 0 : rows;
  }
  int columnCount(const QModelIndex &parent = {}) const override {
    return parent.isValid() ? 0 : columns;
  }
  QVariant data(const QModelIndex &i, int role) const override {
    if (!i.isValid() || role != Qt::DisplayRole)
      return {};
    return core.query(Cell, i.row(), i.column());
  }
  QVariant headerData(int section, Qt::Orientation orientation,
                      int role) const override {
    if (role != Qt::DisplayRole && role != Qt::AccessibleTextRole)
      return {};
    return orientation == Qt::Vertical
               ? QString::number(section + 1)
               : QString("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ")
                     .mid(section, 1);
  }
  Qt::ItemFlags flags(const QModelIndex &i) const override {
    return i.isValid() ? Qt::ItemIsEnabled : Qt::NoItemFlags;
  }
};
class Table : public QTableView {
public:
  Table() {
    setObjectName("table");
    setSelectionMode(NoSelection);
    setEditTriggers(NoEditTriggers);
    setContextMenuPolicy(Qt::NoContextMenu);
    setAcceptDrops(false);
    viewport()->setAcceptDrops(false);
    setDragEnabled(false);
    setDragDropMode(NoDragDrop);
    setTextElideMode(Qt::ElideNone);
    setHorizontalScrollMode(ScrollPerPixel);
    setVerticalScrollMode(ScrollPerPixel);
    setFocusPolicy(Qt::StrongFocus);
    setTabKeyNavigation(false);
    horizontalHeader()->setSectionResizeMode(QHeaderView::ResizeToContents);
    verticalHeader()->setSectionResizeMode(QHeaderView::Fixed);
    verticalHeader()->setMinimumSectionSize(24);
    horizontalHeader()->setMinimumSectionSize(90);
    verticalHeader()->setDefaultSectionSize(29);
    QFont cellFont("Consolas");
    cellFont.setPixelSize(13);
    setFont(cellFont);
  }

protected:
  void keyPressEvent(QKeyEvent *e) override {
    if (e->matches(QKeySequence::Copy) || e->matches(QKeySequence::Cut) ||
        e->matches(QKeySequence::Paste) ||
        e->matches(QKeySequence::SelectAll)) {
      e->accept();
      return;
    }
    QTableView::keyPressEvent(e);
  }
};
QLabel *label(QString text, const char *name = nullptr) {
  auto l = new QLabel(text);
  l->setWordWrap(true);
  l->setTextInteractionFlags(Qt::NoTextInteraction);
  if (name)
    l->setObjectName(name);
  return l;
}
QPushButton *button(QString text, const char *name) {
  auto b = new QPushButton(text);
  b->setObjectName(name);
  b->setAccessibleName(text.remove('&'));
  return b;
}
} // namespace
class Window::Impl : public QObject {
  Window &w;
  Bridge core;
  std::function<qint64()> clock;
  std::function<quintptr(quintptr)> ownedForegroundWindow;
  QElapsedTimer elapsed;
  qint64 lastInput = 0;
  uint32_t timeoutGeneration = 0;
  uint32_t privacySignalGeneration = 0;
  Qt::ApplicationState privacyApplicationState = Qt::ApplicationActive;
  quintptr trackedOwnedForegroundWindow = 0;
  bool updating = false, accepted = false;
  bool privacyActive = false;
  QString locale = "en";
  QString currentTheme = "system";
  QWidget *warning;
  QWidget *workspace;
  QWidget *appPage;
  QWidget *privacyCover;
  QStackedWidget *pages;
  QLineEdit *path, *profileFilter;
  Secret *master;
  QLabel *status, *message, *sheetState, *profileDetails;
  QComboBox *profiles, *lengths, *columns, *sheets, *minutes, *localeChoice,
      *themeChoice;
  struct ProfileChoice {
    QString text;
    QString searchText;
    int catalogIndex;
    bool selectable;
  };
  QVector<ProfileChoice> profileChoices;
  QLineEdit *sheetName;
  Secret *sheetPassword, *symbol1, *symbol2, *word;
  QSpinBox *row;
  QCheckBox *verificationConsent, *spinConsent;
  Table *table;
  TableModel *model;
  QTimer *privacyForegroundTimer;
  QList<QPushButton *> vaultButtons, editButtons;
  QPushButton *create, *open, *unlock, *save, *closeVault, *lock, *add,
      *protect, *unlockSheet, *unlockMaster, *addCustom, *replaceDictionary,
      *renameSheet, *deleteSheet, *backup, *restore, *changePassword, *verify;
  void bindText(QWidget *widget, const char *key) {
    widget->setProperty("textKey", key);
  }
  void bindAccessible(QWidget *widget, const char *key) {
    widget->setProperty("accessibleKey", key);
  }
  void bindPlaceholder(QLineEdit *widget, const char *key) {
    widget->setProperty("placeholderKey", key);
  }
  void translateWidget(QWidget *widget) {
    const QByteArray textKey = widget->property("textKey").toByteArray();
    if (!textKey.isEmpty()) {
      const QString value = uiText(locale, textKey.constData());
      if (auto label = qobject_cast<QLabel *>(widget))
        label->setText(value);
      else if (auto button = qobject_cast<QAbstractButton *>(widget)) {
        button->setText(value);
        button->setAccessibleName(QString(value).remove('&'));
      }
    }
    const QByteArray accessibleKey =
        widget->property("accessibleKey").toByteArray();
    if (!accessibleKey.isEmpty())
      widget->setAccessibleName(uiText(locale, accessibleKey.constData()));
    const QByteArray placeholderKey =
        widget->property("placeholderKey").toByteArray();
    if (!placeholderKey.isEmpty())
      if (auto line = qobject_cast<QLineEdit *>(widget))
        line->setPlaceholderText(uiText(locale, placeholderKey.constData()));
  }
  QLabel *translatedLabel(const char *key, const char *name = nullptr) {
    auto value = label(QString(), name);
    bindText(value, key);
    translateWidget(value);
    return value;
  }
  QPushButton *translatedButton(const char *key, const char *name) {
    auto value = button(QString(), name);
    bindText(value, key);
    translateWidget(value);
    return value;
  }
  QCheckBox *translatedCheck(const char *key, const char *name) {
    auto value = new QCheckBox;
    value->setObjectName(name);
    bindText(value, key);
    translateWidget(value);
    return value;
  }
  void applyLanguage() {
    w.setWindowTitle(uiText(locale, "title"));
    translateWidget(appPage);
    for (auto widget : w.findChildren<QWidget *>())
      translateWidget(widget);
    const QVariant selectedLocale = localeChoice->currentData();
    localeChoice->setItemText(0, uiText(locale, "languageEnglish"));
    localeChoice->setItemText(1, uiText(locale, "languageRussian"));
    localeChoice->setCurrentIndex(localeChoice->findData(selectedLocale));
    const QVariant selectedTheme = themeChoice->currentData();
    themeChoice->setItemText(0, uiText(locale, "themeSystem"));
    themeChoice->setItemText(1, uiText(locale, "themeLight"));
    themeChoice->setItemText(2, uiText(locale, "themeDark"));
    themeChoice->setCurrentIndex(themeChoice->findData(selectedTheme));
    for (int index = 0; index < minutes->count(); ++index)
      minutes->setItemText(
          index,
          uiText(locale, "minutes").arg(minutes->itemData(index).toInt()));
    columns->setItemText(0, uiText(locale, "columns10"));
    columns->setItemText(1, uiText(locale, "columns36"));
    for (int index = 0; index < lengths->count(); ++index)
      lengths->setItemText(
          index,
          uiText(locale, "rows").arg(lengths->itemData(index).toInt()));
    row->setPrefix(uiText(locale, "rowPrefix"));
    message->setAccessibleName(uiText(locale, "messageA11y"));
    refresh();
    refreshProfile();
  }
  void announce(const QString &value) {
    message->setText(value);
    message->setAccessibleName(value.isEmpty() ? uiText(locale, "messageA11y")
                                               : value);
    QAccessibleEvent event(message, QAccessible::Alert);
    QAccessible::updateAccessibility(&event);
  }
  QString choosePath(bool save, const char *titleKey, const char *filterKey) {
    clearInputs();
    return save ? QFileDialog::getSaveFileName(
                      &w, uiText(locale, titleKey), QString(),
                      uiText(locale, filterKey), nullptr,
                      QFileDialog::DontConfirmOverwrite)
                : QFileDialog::getOpenFileName(&w, uiText(locale, titleKey),
                                               QString(),
                                               uiText(locale, filterKey));
  }
  void restoreStoredLocale() {
    const QString storedLocale = core.query(Locale, PreferenceGet);
    if (storedLocale != "en" && storedLocale != "ru")
      return;
    locale = storedLocale;
    updating = true;
    localeChoice->setCurrentIndex(localeChoice->findData(storedLocale));
    updating = false;
    applyLanguage();
  }
  void persistProcessLocale() {
    if (core.state.state != 2)
      return;
    if (core.query(Locale, PreferenceGet) == locale)
      return;
    TvInput input{};
    const bool valid = field(input, 0, locale);
    action(Locale, PreferenceSet, 0, input, valid);
  }
  QLineEdit *dialogPath(QDialog &dialog, QVBoxLayout &layout,
                        const char *objectName, const char *labelKey,
                        const char *titleKey, const char *filterKey,
                        bool save) {
    layout.addWidget(label(uiText(locale, labelKey)));
    auto line = new QLineEdit;
    line->setObjectName(objectName);
    line->setAccessibleName(uiText(locale, labelKey));
    line->setReadOnly(true);
    line->setAcceptDrops(false);
    layout.addWidget(line);
    auto browse = button(uiText(locale, "browse"),
                         QByteArray(objectName).append("Browse").constData());
    layout.addWidget(browse);
    connect(browse, &QPushButton::clicked, &dialog,
            [this, line, save, titleKey, filterKey] {
              const QString selected =
                  choosePath(save, titleKey, filterKey);
              if (!selected.isEmpty())
                line->setText(selected);
            });
    return line;
  }
  QDialogButtonBox *dialogButtons(QDialog &dialog, QVBoxLayout &layout) {
    auto buttons = new QDialogButtonBox(QDialogButtonBox::Ok |
                                        QDialogButtonBox::Cancel);
    buttons->button(QDialogButtonBox::Ok)
        ->setText(uiText(locale, "dialogOk"));
    buttons->button(QDialogButtonBox::Cancel)
        ->setText(uiText(locale, "dialogCancel"));
    connect(buttons, &QDialogButtonBox::accepted, &dialog, &QDialog::accept);
    connect(buttons, &QDialogButtonBox::rejected, &dialog, &QDialog::reject);
    layout.addWidget(buttons);
    return buttons;
  }
  void runCreateDialog() {
    QDialog dialog(&w);
    dialog.setObjectName("createVaultDialog");
    dialog.setWindowTitle(uiText(locale, "create"));
    auto layout = new QVBoxLayout(&dialog);
    auto selectedPath = dialogPath(dialog, *layout, "createPath",
                                   "vaultDestinationLabel", "selectNewVault",
                                   "cipherFilter", true);
    auto name = new QLineEdit(uiText(locale, "defaultVaultName"));
    name->setObjectName("createVaultName");
    name->setMaxLength(4096);
    name->setAcceptDrops(false);
    bindAccessible(name, "vaultNameA11y");
    bindPlaceholder(name, "vaultNamePlaceholder");
    translateWidget(name);
    layout->addWidget(name);
    auto passwordGuidance =
        label(uiErrorText(locale, "password-policy"),
              "createPasswordGuidance");
    passwordGuidance->setAccessibleName(passwordGuidance->text());
    layout->addWidget(passwordGuidance);
    auto password = new Secret("createMaster");
    bindAccessible(password, "newPassword");
    bindPlaceholder(password, "newPassword");
    translateWidget(password);
    layout->addWidget(password);
    auto confirmation = new Secret("createConfirmation");
    bindAccessible(confirmation, "confirmPassword");
    bindPlaceholder(confirmation, "confirmPassword");
    translateWidget(confirmation);
    layout->addWidget(confirmation);
    dialogButtons(dialog, *layout);
    if (dialog.exec() != QDialog::Accepted) {
      password->erase();
      confirmation->erase();
      announce(uiText(locale, "cancelled"));
      return;
    }
    if (password->text() != confirmation->text()) {
      password->erase();
      confirmation->erase();
      announce(uiText(locale, "passwordMismatch"));
      return;
    }
    const QString chosen = selectedPath->text();
    TvInput input{};
    bool valid = field(input, 0, chosen);
    valid &= password->consume(input, 1);
    valid &= field(input, 2, name->text());
    valid &= confirmation->consume(input, 3);
    if (action(Create, 0, 0, input, valid)) {
      path->setText(chosen);
      lastInput = clock();
      persistProcessLocale();
    }
  }
  void runOpenDialog() {
    QDialog dialog(&w);
    dialog.setObjectName("openVaultDialog");
    dialog.setWindowTitle(uiText(locale, "open"));
    auto layout = new QVBoxLayout(&dialog);
    auto selectedPath = dialogPath(dialog, *layout, "openPath",
                                   "vaultSourceLabel", "selectVault",
                                   "cipherFilter", false);
    auto password = new Secret("openMaster");
    bindAccessible(password, "masterA11y");
    bindPlaceholder(password, "masterPlaceholder");
    translateWidget(password);
    layout->addWidget(password);
    dialogButtons(dialog, *layout);
    if (dialog.exec() != QDialog::Accepted) {
      password->erase();
      announce(uiText(locale, "cancelled"));
      return;
    }
    const QString chosen = selectedPath->text();
    TvInput input{};
    bool valid = field(input, 0, chosen);
    valid &= password->consume(input, 1);
    if (action(Open, 0, 0, input, valid)) {
      path->setText(chosen);
      lastInput = clock();
      restoreStoredLocale();
    }
  }
  void runBackupDialog() {
    QDialog dialog(&w);
    dialog.setObjectName("backupDialog");
    dialog.setWindowTitle(uiText(locale, "backup"));
    auto layout = new QVBoxLayout(&dialog);
    layout->addWidget(label(uiText(locale, "backupWarning")));
    auto destination =
        dialogPath(dialog, *layout, "backupPath", "destinationLabel",
                   "selectBackup", "cipherFilter", true);
    dialogButtons(dialog, *layout);
    if (dialog.exec() != QDialog::Accepted) {
      announce(uiText(locale, "cancelled"));
      return;
    }
    TvInput input{};
    const bool valid = field(input, 0, destination->text());
    if (action(Backup, 0, 0, input, valid))
      announce(uiText(locale, "backupComplete"));
  }
  void runRestoreDialog() {
    QDialog dialog(&w);
    dialog.setObjectName("restoreDialog");
    dialog.setWindowTitle(uiText(locale, "restore"));
    auto layout = new QVBoxLayout(&dialog);
    auto source = dialogPath(dialog, *layout, "restoreSource", "sourceLabel",
                             "selectRestoreSource", "cipherFilter", false);
    auto destination = dialogPath(
        dialog, *layout, "restoreDestination", "destinationLabel",
        "selectRestoreDestination", "cipherFilter", true);
    auto restoreGuidance =
        label(uiText(locale, "restorePasswordGuidance"),
              "restorePasswordGuidance");
    restoreGuidance->setAccessibleName(restoreGuidance->text());
    layout->addWidget(restoreGuidance);
    auto password = new Secret("restorePassword");
    bindAccessible(password, "masterA11y");
    bindPlaceholder(password, "masterPlaceholder");
    translateWidget(password);
    layout->addWidget(password);
    dialogButtons(dialog, *layout);
    if (dialog.exec() != QDialog::Accepted) {
      password->erase();
      announce(uiText(locale, "cancelled"));
      return;
    }
    TvInput input{};
    bool valid = field(input, 0, source->text());
    valid &= field(input, 1, destination->text());
    valid &= password->consume(input, 2);
    if (action(Restore, 0, 0, input, valid)) {
      path->setText(destination->text());
      lastInput = clock();
      const QString storedLocale = core.query(Locale, PreferenceGet);
      if (storedLocale == "en" || storedLocale == "ru")
        locale = storedLocale;
      updating = true;
      localeChoice->setCurrentIndex(localeChoice->findData(locale));
      updating = false;
      applyLanguage();
      announce(uiText(locale, "restoreComplete"));
    }
  }
  void runChangePasswordDialog() {
    QDialog dialog(&w);
    dialog.setObjectName("changePasswordDialog");
    dialog.setWindowTitle(uiText(locale, "changePassword"));
    auto layout = new QVBoxLayout(&dialog);
    layout->addWidget(
        label(uiText(locale, "rotationWarning"), "rotationWarning"));
    auto current = new Secret("currentMaster");
    auto replacement = new Secret("newMaster");
    auto confirmation = new Secret("confirmNewMaster");
    for (auto entry : {current, replacement, confirmation}) {
      bindAccessible(entry, entry == current       ? "currentPassword"
                            : entry == replacement ? "newPassword"
                                                   : "confirmPassword");
      bindPlaceholder(entry, entry == current       ? "currentPassword"
                             : entry == replacement ? "newPassword"
                                                    : "confirmPassword");
      translateWidget(entry);
      layout->addWidget(entry);
    }
    dialogButtons(dialog, *layout);
    if (dialog.exec() != QDialog::Accepted) {
      current->erase();
      replacement->erase();
      confirmation->erase();
      announce(uiText(locale, "cancelled"));
      return;
    }
    if (replacement->text() != confirmation->text()) {
      current->erase();
      replacement->erase();
      confirmation->erase();
      announce(uiText(locale, "passwordMismatch"));
      return;
    }
    TvInput input{};
    bool valid = current->consume(input, 0);
    valid &= replacement->consume(input, 1);
    valid &= confirmation->consume(input, 2);
    if (action(ChangePassword, 0, 0, input, valid))
      announce(uiText(locale, "rotationComplete"));
  }
  void runCustomDialog(bool replacement) {
    clearInputs();
    QDialog dialog(&w);
    dialog.setObjectName(replacement ? "replaceDictionaryDialog"
                                     : "customDictionaryDialog");
    dialog.setWindowTitle(
        uiText(locale, replacement ? "replaceDictionary" : "customSheet"));
    auto layout = new QVBoxLayout(&dialog);
    layout->addWidget(label(uiText(locale, "customWarning")));
    auto name = new QLineEdit;
    name->setObjectName(replacement ? "replacementName" : "customName");
    name->setMaxLength(4096);
    name->setAccessibleName(uiText(locale, replacement ? "replacementName"
                                                       : "customName"));
    name->setPlaceholderText(name->accessibleName());
    name->setAcceptDrops(false);
    layout->addWidget(name);
    auto dictionary = dialogPath(dialog, *layout, "dictionaryPath",
                                 "dictionaryLabel", "selectDictionary",
                                 "dictionaryFilter", false);
    QComboBox *rows = nullptr;
    QComboBox *columnCount = nullptr;
    QCheckBox *acknowledgement = nullptr;
    if (!replacement) {
      rows = new QComboBox;
      rows->setObjectName("customRows");
      for (int value : {12, 13, 15, 16, 18, 20, 21, 24, 25, 26, 27, 28, 29,
                        33})
        rows->addItem(uiText(locale, "rows").arg(value), value);
      rows->setCurrentIndex(rows->findData(24));
      rows->setAccessibleName(uiText(locale, "customRows"));
      layout->addWidget(rows);
      columnCount = new QComboBox;
      columnCount->setObjectName("customColumns");
      columnCount->addItem(uiText(locale, "columns10"), 10);
      columnCount->addItem(uiText(locale, "columns36"), 36);
      columnCount->setAccessibleName(uiText(locale, "customColumns"));
      layout->addWidget(columnCount);
    } else {
      acknowledgement = new QCheckBox(uiText(locale, "replacementAck"));
      acknowledgement->setObjectName("replacementAck");
      layout->addWidget(acknowledgement);
    }
    dialogButtons(dialog, *layout);
    if (dialog.exec() != QDialog::Accepted) {
      announce(uiText(locale, "cancelled"));
      return;
    }
    TvInput input{};
    bool valid = field(input, 0, name->text());
    valid &= field(input, 1, dictionary->text());
    if (replacement) {
      if (action(ReplaceDictionary, acknowledgement->isChecked() ? 1 : 0, 0,
                 input, valid)) {
        updating = true;
        sheets->setCurrentIndex(sheets->count() - 1);
        updating = false;
      }
    } else if (action(AddCustom, rows->currentData().toUInt(),
                      columnCount->currentData().toUInt(), input, valid)) {
      updating = true;
      sheets->setCurrentIndex(sheets->count() - 1);
      updating = false;
    }
  }
  void runRenameDialog() {
    QDialog dialog(&w);
    dialog.setObjectName("renameDialog");
    dialog.setWindowTitle(uiText(locale, "renameSheet"));
    auto layout = new QVBoxLayout(&dialog);
    auto name = new QLineEdit;
    name->setObjectName("renameName");
    name->setMaxLength(4096);
    name->setAccessibleName(uiText(locale, "renameName"));
    name->setPlaceholderText(name->accessibleName());
    layout->addWidget(name);
    dialogButtons(dialog, *layout);
    if (dialog.exec() != QDialog::Accepted)
      return;
    TvInput input{};
    const bool valid = field(input, 0, name->text());
    action(RenameSheet, 0, 0, input, valid);
  }
  void runDeleteDialog() {
    clearInputs();
    QDialog dialog(&w);
    dialog.setObjectName("deleteDialog");
    dialog.setWindowTitle(uiText(locale, "deleteSheet"));
    auto layout = new QVBoxLayout(&dialog);
    auto exact = new QLineEdit;
    exact->setObjectName("deleteExactName");
    exact->setMaxLength(4096);
    exact->setAccessibleName(uiText(locale, "deleteExactName"));
    exact->setPlaceholderText(exact->accessibleName());
    layout->addWidget(exact);
    auto finalConfirmation =
        new QCheckBox(uiText(locale, "deleteFinal"));
    finalConfirmation->setObjectName("deleteFinal");
    layout->addWidget(finalConfirmation);
    dialogButtons(dialog, *layout);
    if (dialog.exec() != QDialog::Accepted)
      return;
    TvInput input{};
    const bool valid = field(input, 0, exact->text());
    action(DeleteSheet, finalConfirmation->isChecked() ? 1 : 0, 0, input,
           valid);
  }
  bool selectedProfileIsAvailable() const {
    return profiles->currentData(Qt::UserRole + 1).toBool();
  }
  void setProfileDetails(const QString &value) {
    profileDetails->setText(value);
    profileDetails->setAccessibleName(value);
    profileDetails->setAccessibleDescription(value);
    QAccessibleEvent event(profileDetails, QAccessible::NameChanged);
    QAccessible::updateAccessibility(&event);
    QAccessibleEvent description(profileDetails,
                                 QAccessible::DescriptionChanged);
    QAccessible::updateAccessibility(&description);
  }
  void refreshProfile() {
    const int profile = profiles->currentData().toInt();
    if (profile < 0) {
      setProfileDetails(uiText(locale, "profileNoMatches"));
      lengths->clear();
      add->setEnabled(false);
      return;
    }
    const QString name = core.query(ProfileFieldValue, profile, ProfileName);
    const QString id = core.query(ProfileFieldValue, profile, ProfileId);
    const QString mode = core.query(ProfileFieldValue, profile, ProfileMode);
    const QString reason = uiProfileReason(
        locale, core.query(ProfileFieldValue, profile, ProfileReason));
    const QString platform =
        core.query(ProfileFieldValue, profile, ProfilePlatform);
    const QString status = core.query(ProfileFieldValue, profile, ProfileStatus);
    const QString minimum =
        core.query(ProfileFieldValue, profile, ProfileVersionMin);
    const QString maximum =
        core.query(ProfileFieldValue, profile, ProfileVersionMax);
    setProfileDetails(
        QString("%1\n%2 · %3 · %4\n%5 — %6\n%7%8")
            .arg(name, platform, status, mode, minimum, maximum, id,
                 reason.isEmpty() ? QString() : QString(" · %1").arg(reason)));
    lengths->clear();
    const int count = core.query(ProfileLengthCount, profile).toInt();
    for (int index = 0; index < count; ++index) {
      const int value = core.query(ProfileLength, profile, index).toInt();
      if (value > 0)
      lengths->addItem(uiText(locale, "rows").arg(value), value);
    }
    add->setEnabled(core.state.state == 2 && selectedProfileIsAvailable() &&
                    lengths->count() > 0);
  }
  void filterProfiles(const QString &filter) {
    const int previous = profiles->currentIndex() >= 0
                             ? profiles->currentData().toInt()
                             : -1;
    {
      QSignalBlocker blocker(profiles);
      profiles->clear();
      for (const auto &choice : profileChoices) {
        if (!filter.isEmpty() &&
            !choice.searchText.contains(filter, Qt::CaseInsensitive))
          continue;
        profiles->addItem(choice.text, choice.catalogIndex);
        const int row = profiles->count() - 1;
        profiles->setItemData(row, choice.selectable, Qt::UserRole + 1);
        profiles->setItemData(row, choice.text, Qt::ToolTipRole);
      }
      int selected = profiles->findData(previous);
      if (selected < 0)
        selected = profiles->count() > 0 ? 0 : -1;
      profiles->setCurrentIndex(selected);
    }
    refreshProfile();
  }
  bool action(uint32_t op, uint32_t a, uint32_t b, TvInput &in,
              bool fieldsValid = true) {
    if (!fieldsValid) {
      wipe(&in, sizeof(in));
      announce(uiText(locale, "inputTooLong"));
      return false;
    }
    QString text, successText;
    int code = core.action(op, a, b, in, text, &successText);
    if (code == 0 &&
        (op == Create || op == Open || op == Unlock || op == Timeout ||
         op == Activity || op == Restore)) {
      bool ok = false;
      const uint32_t generation = successText.toUInt(&ok);
      if (ok && generation != 0)
        timeoutGeneration = generation;
    }
    announce(code == 0 ? QString() : uiErrorText(locale, text));
    refresh();
    return code == 0;
  }
  bool action(uint32_t op, uint32_t a = 0, uint32_t b = 0) {
    TvInput in{};
    return action(op, a, b, in);
  }
  void clearInputs() {
    for (auto s : w.findChildren<QLineEdit *>()) {
      if (auto secret = dynamic_cast<Secret *>(s))
        secret->erase();
    }
    for (auto acknowledgement : w.findChildren<QCheckBox *>())
      acknowledgement->setChecked(false);
  }
  void refresh() {
    updating = true;
    const auto &s = core.state;
    const bool isOpen = s.state == 2;
    status->setText(uiText(locale,
                           isOpen ? (s.dirty ? "stateDirty" : "stateClean")
                                  : (s.state == 1 ? "stateLocked"
                                                  : "stateClosed")));
    status->setAccessibleName(uiText(locale, "stateA11y").arg(status->text()));
    workspace->setVisible(isOpen);
    create->setEnabled(accepted && s.state == 0);
    open->setEnabled(accepted && s.state == 0);
    unlock->setEnabled(accepted && s.state == 1);
    master->setVisible(s.state == 1);
    unlock->setVisible(s.state == 1);
    save->setEnabled(isOpen);
    closeVault->setEnabled(s.state != 0);
    lock->setEnabled(isOpen);
    backup->setEnabled(isOpen);
    restore->setEnabled(accepted && s.state == 0);
    changePassword->setEnabled(isOpen);
    addCustom->setEnabled(isOpen);
    add->setEnabled(isOpen && selectedProfileIsAvailable() &&
                    lengths->count() > 0);
    const int previous = sheets->currentIndex();
    sheets->clear();
    for (uint32_t i = 0; i < s.sheets; ++i)
      sheets->addItem(core.query(SheetName, i));
    sheets->setCurrentIndex(
        qBound(0, previous, static_cast<int>(s.sheets) - 1));
    const bool editable = isOpen && s.rows && !s.protected_sheet;
    for (auto b : editButtons)
      b->setEnabled(editable);
    replaceDictionary->setEnabled(editable);
    renameSheet->setEnabled(editable);
    deleteSheet->setEnabled(editable);
    protect->setEnabled(editable);
    unlockSheet->setEnabled(isOpen && s.rows && s.protected_sheet);
    unlockMaster->setEnabled(unlockSheet->isEnabled());
    verificationConsent->setEnabled(editable && !s.verified);
    const QString verifyText =
        uiText(locale, s.verified ? "unverifyButton" : "verifiedButton");
    verify->setText(verifyText);
    verify->setAccessibleName(verifyText);
    sheetState->setText(
        s.rows
            ? QString("%1 · %2").arg(
                  uiText(locale, s.protected_sheet ? "sheetProtected"
                                                    : "sheetEditable"),
                  uiText(locale,
                         s.verified ? "sheetVerified" : "sheetUnverified"))
            : uiText(locale, "noSheet"));
    row->setMaximum(qMax(1, static_cast<int>(s.rows)));
    model->refresh();
    updating = false;
  }
  bool finish(uint32_t op) {
    uint32_t decision = 0;
    if (core.state.dirty) {
      QMessageBox box(
          QMessageBox::Warning, uiText(locale, "unsavedTitle"),
          uiText(locale, "unsavedPrompt"),
          QMessageBox::Save | QMessageBox::Discard | QMessageBox::Cancel, &w);
      box.button(QMessageBox::Save)->setText(uiText(locale, "dialogSave"));
      box.button(QMessageBox::Discard)
          ->setText(uiText(locale, "dialogDiscard"));
      box.button(QMessageBox::Cancel)
          ->setText(uiText(locale, "dialogCancel"));
      box.setDefaultButton(QMessageBox::Cancel);
      int answer = box.exec();
      if (answer != QMessageBox::Save && answer != QMessageBox::Discard)
        return false;
      decision = answer == QMessageBox::Save ? 1 : 2;
    }
    clearInputs();
    return action(op, decision);
  }

public:
  Impl(Window &w, std::function<qint64()> time,
       std::function<quintptr(quintptr)> foregroundWindow)
      : QObject(&w), w(w), clock(std::move(time)),
        ownedForegroundWindow(std::move(foregroundWindow)) {
    elapsed.start();
    if (!clock)
      clock = [this] { return elapsed.elapsed(); };
    if (!ownedForegroundWindow)
      ownedForegroundWindow = ownProcessForegroundWindow;
    lastInput = clock();
    w.setWindowTitle(uiText(locale, "title"));
    QFont uiFont("Segoe UI");
    uiFont.setPixelSize(13);
    w.setFont(uiFont);
    w.resize(1280, 720);
    w.setMinimumSize(900, 600);
    w.setAcceptDrops(false);
    applySemanticTheme(*qApp, w, currentTheme);
    pages = new QStackedWidget;
    pages->setObjectName("privacyPages");
    w.setCentralWidget(pages);
    appPage = new QWidget;
    appPage->setObjectName("applicationPage");
    auto root = new QVBoxLayout(appPage);
    root->setContentsMargins(16, 12, 16, 12);
    pages->addWidget(appPage);
    privacyCover = new QWidget;
    privacyCover->setObjectName("privacyCover");
    auto privacyLayout = new QVBoxLayout(privacyCover);
    privacyLayout->addStretch();
    auto privacyTitle = translatedLabel("privacyTitle");
    privacyTitle->setAlignment(Qt::AlignCenter);
    bindAccessible(privacyTitle, "privacyA11y");
    privacyLayout->addWidget(privacyTitle);
    privacyLayout->addWidget(translatedLabel("privacyBody"));
    privacyLayout->addStretch();
    pages->addWidget(privacyCover);
    pages->setCurrentWidget(appPage);
    root->addWidget(translatedLabel("banner"));
    warning = new QWidget;
    auto warnLayout = new QVBoxLayout(warning);
    warnLayout->addWidget(translatedLabel("warning"));
    auto accept = translatedButton("warningAccept", "warningAccept");
    warnLayout->addWidget(accept);
    root->addWidget(warning);
    auto vault = new QGridLayout;
    path = new QLineEdit;
    path->setObjectName("path");
    path->setReadOnly(true);
    bindAccessible(path, "pathA11y");
    bindPlaceholder(path, "pathPlaceholder");
    translateWidget(path);
    path->setAcceptDrops(false);
    master = new Secret("master");
    bindAccessible(master, "masterA11y");
    bindPlaceholder(master, "masterPlaceholder");
    translateWidget(master);
    vault->addWidget(path, 0, 0, 1, 6);
    vault->addWidget(master, 1, 0, 1, 4);
    create = translatedButton("create", "create");
    open = translatedButton("open", "open");
    unlock = translatedButton("unlock", "unlock");
    save = translatedButton("save", "save");
    closeVault = translatedButton("close", "closeVault");
    lock = translatedButton("lock", "lock");
    vaultButtons = {create, open, unlock, save, closeVault, lock};
    for (int i = 0; i < vaultButtons.size(); ++i)
      vault->addWidget(vaultButtons[i], 2, i);
    root->addLayout(vault);
    auto recoveryLine = new QHBoxLayout;
    backup = translatedButton("backup", "backup");
    restore = translatedButton("restore", "restore");
    changePassword = translatedButton("changePassword", "changePassword");
    recoveryLine->addWidget(backup);
    recoveryLine->addWidget(restore);
    recoveryLine->addWidget(changePassword);
    root->addLayout(recoveryLine);
    auto stateLine = new QHBoxLayout;
    status = label(uiText(locale, "stateClosed"), "state");
    stateLine->addWidget(status, 1);
    stateLine->addWidget(translatedLabel("inactivity"));
    minutes = new QComboBox;
    minutes->setObjectName("minutes");
    bindAccessible(minutes, "minutesA11y");
    for (int m : {1, 5, 15, 30})
      minutes->addItem(uiText(locale, "minutes").arg(m), m);
    minutes->setCurrentIndex(1);
    stateLine->addWidget(minutes);
    localeChoice = new QComboBox;
    localeChoice->setObjectName("locale");
    bindAccessible(localeChoice, "localeA11y");
    localeChoice->addItem(uiText(locale, "languageEnglish"), "en");
    localeChoice->addItem(uiText(locale, "languageRussian"), "ru");
    stateLine->addWidget(localeChoice);
    themeChoice = new QComboBox;
    themeChoice->setObjectName("theme");
    bindAccessible(themeChoice, "themeA11y");
    themeChoice->addItem(uiText(locale, "themeSystem"), "system");
    themeChoice->addItem(uiText(locale, "themeLight"), "light");
    themeChoice->addItem(uiText(locale, "themeDark"), "dark");
    stateLine->addWidget(themeChoice);
    root->addLayout(stateLine);
    message = label("", "message");
    root->addWidget(message);
    workspace = new QWidget;
    auto work = new QHBoxLayout(workspace);
    work->setContentsMargins(0, 0, 0, 0);
    auto sidebar = new QWidget;
    sidebar->setMinimumWidth(270);
    sidebar->setMaximumWidth(340);
    auto side = new QVBoxLayout(sidebar);
    side->setContentsMargins(0, 0, 8, 0);
    side->addWidget(translatedLabel("sheetsHeading"));
    sheets = new QComboBox;
    sheets->setObjectName("sheets");
    bindAccessible(sheets, "currentSheetA11y");
    side->addWidget(sheets);
    auto nextSheet = translatedButton("nextSheet", "nextSheet");
    side->addWidget(nextSheet);
    connect(nextSheet, &QPushButton::clicked, this, [this] {
      if (sheets->count() > 0)
        sheets->setCurrentIndex((sheets->currentIndex() + 1) % sheets->count());
    });
    side->addWidget(translatedLabel("profileFilterLabel"));
    profileFilter = new QLineEdit;
    profileFilter->setObjectName("profileFilter");
    profileFilter->setClearButtonEnabled(true);
    bindAccessible(profileFilter, "profileFilterA11y");
    bindPlaceholder(profileFilter, "profileFilterPlaceholder");
    translateWidget(profileFilter);
    side->addWidget(profileFilter);
    profiles = new QComboBox;
    profiles->setObjectName("profiles");
    bindAccessible(profiles, "profileA11y");
    profiles->setSizeAdjustPolicy(
        QComboBox::AdjustToMinimumContentsLengthWithIcon);
    profiles->setMinimumContentsLength(22);
    profiles->view()->setMinimumWidth(650);
    int count = core.query(ProfileCount).toInt();
    for (int i = 0; i < count; ++i) {
      const bool enabled =
          core.query(ProfileFieldValue, i, ProfileSelectable) == "1";
      const QString name = core.query(ProfileFieldValue, i, ProfileName);
      const QString mode = core.query(ProfileFieldValue, i, ProfileMode);
      const QString status = core.query(ProfileFieldValue, i, ProfileStatus);
      const QString platform =
          core.query(ProfileFieldValue, i, ProfilePlatform);
      const QString minimum =
          core.query(ProfileFieldValue, i, ProfileVersionMin);
      const QString maximum =
          core.query(ProfileFieldValue, i, ProfileVersionMax);
      const QString id = core.query(ProfileFieldValue, i, ProfileId);
      const QString reason = core.query(ProfileFieldValue, i, ProfileReason);
      const QString text =
          QString("%1 / %2 / %3 / %4").arg(name, platform, status, mode);
      profileChoices.push_back(
          {text,
           QString("%1 %2 %3 %4 %5 %6 %7 %8")
               .arg(name, platform, status, mode, minimum, maximum, id, reason),
           i, enabled});
      profiles->addItem(text, i);
      profiles->setItemData(i, enabled, Qt::UserRole + 1);
      profiles->setItemData(i, text, Qt::ToolTipRole);
    }
    for (int i = 0; i < profiles->count(); ++i) {
      if (profiles->itemData(i, Qt::UserRole + 1).toBool()) {
        profiles->setCurrentIndex(i);
        break;
      }
    }
    side->addWidget(profiles);
    profileDetails = label("", "profileDetails");
    side->addWidget(profileDetails);
    sheetName = new QLineEdit(uiText(locale, "defaultSheetName"));
    sheetName->setObjectName("sheetName");
    bindAccessible(sheetName, "sheetNameA11y");
    sheetName->setMaxLength(4096);
    side->addWidget(sheetName);
    columns = new QComboBox;
    columns->setObjectName("columns");
    bindAccessible(columns, "columnA11y");
    columns->addItem(uiText(locale, "columns10"), 10);
    columns->addItem(uiText(locale, "columns36"), 36);
    columns->setCurrentIndex(1);
    side->addWidget(columns);
    lengths = new QComboBox;
    lengths->setObjectName("lengths");
    bindAccessible(lengths, "lengthA11y");
    side->addWidget(lengths);
    add = translatedButton("addSheet", "add");
    side->addWidget(add);
    addCustom = translatedButton("customSheet", "addCustom");
    replaceDictionary =
        translatedButton("replaceDictionary", "replaceDictionary");
    renameSheet = translatedButton("renameSheet", "renameSheet");
    deleteSheet = translatedButton("deleteSheet", "deleteSheet");
    side->addWidget(addCustom);
    side->addWidget(replaceDictionary);
    side->addWidget(renameSheet);
    side->addWidget(deleteSheet);
    refreshProfile();
    sheetState = label("", "sheetState");
    side->addWidget(sheetState);
    sheetPassword = new Secret("sheetPassword");
    bindAccessible(sheetPassword, "sheetCredentialA11y");
    bindPlaceholder(sheetPassword, "sheetPasswordPlaceholder");
    translateWidget(sheetPassword);
    side->addWidget(sheetPassword);
    auto protectLine = new QHBoxLayout;
    auto set = translatedButton("setPassword", "setSheetPassword");
    protect = translatedButton("protect", "protect");
    protectLine->addWidget(set);
    protectLine->addWidget(protect);
    side->addLayout(protectLine);
    auto unlockLine = new QHBoxLayout;
    unlockSheet = translatedButton("unlockSheet", "unlockSheet");
    unlockMaster = translatedButton("useMaster", "unlockMaster");
    unlockLine->addWidget(unlockSheet);
    unlockLine->addWidget(unlockMaster);
    side->addLayout(unlockLine);
    side->addWidget(translatedLabel("protectionInfo"));
    verificationConsent =
        translatedCheck("verificationConsent", "verificationConsent");
    side->addWidget(translatedLabel("verificationGuide"));
    side->addWidget(verificationConsent);
    verify = translatedButton("verifiedButton", "verify");
    side->addWidget(verify);
    side->addWidget(translatedLabel("spinWarning"));
    side->addWidget(translatedLabel("spinGuide"));
    side->addStretch();
    auto sidebarScroll = new QScrollArea;
    sidebarScroll->setWidget(sidebar);
    sidebarScroll->setWidgetResizable(true);
    sidebarScroll->setMinimumWidth(290);
    sidebarScroll->setMaximumWidth(355);
    sidebarScroll->setFrameShape(QFrame::NoFrame);
    work->addWidget(sidebarScroll);
    auto main = new QVBoxLayout;
    table = new Table;
    bindAccessible(table, "tableA11y");
    translateWidget(table);
    model = new TableModel(core, table);
    table->setModel(model);
    main->addWidget(table, 1);
    spinConsent = translatedCheck("spinConsent", "spinConsent");
    main->addWidget(spinConsent);
    auto spinLine = new QHBoxLayout;
    row = new QSpinBox;
    row->setObjectName("row");
    row->setPrefix(uiText(locale, "rowPrefix"));
    row->setMinimum(1);
    bindAccessible(row, "rowA11y");
    symbol1 = new Secret("symbol1");
    bindAccessible(symbol1, "symbolA11y");
    bindPlaceholder(symbol1, "symbolPlaceholder");
    translateWidget(symbol1);
    symbol1->setMaxLength(1);
    symbol1->setMaximumWidth(100);
    symbol2 = new Secret("symbol2");
    bindAccessible(symbol2, "symbolA11y");
    bindPlaceholder(symbol2, "repeatPlaceholder");
    translateWidget(symbol2);
    symbol2->setMaxLength(1);
    symbol2->setMaximumWidth(100);
    word = new Secret("word");
    word->setMaxLength(128);
    bindAccessible(word, "wordA11y");
    bindPlaceholder(word, "wordPlaceholder");
    translateWidget(word);
    auto spin = translatedButton("spin", "spin");
    for (auto widget : QList<QWidget *>{row, symbol1, symbol2, word, spin})
      spinLine->addWidget(widget);
    main->addLayout(spinLine);
    work->addLayout(main, 1);
    root->addWidget(workspace, 1);
    editButtons = {set, verify, spin};
    const QList<QWidget *> focusOrder{
        accept,          create,          open,       master,
        unlock,          save,            closeVault, lock,
        backup,          restore,         changePassword,
        minutes,         localeChoice,    themeChoice,
        sheets,          nextSheet,       profileFilter, profiles,
        sheetName,       columns,         lengths,
        add,             addCustom,       replaceDictionary,
        renameSheet,     deleteSheet,     sheetPassword,
        set,             protect,         unlockSheet,
        unlockMaster,    verificationConsent,
        verify,          table,           spinConsent,
        row,             symbol1,         symbol2,
        word,            spin};
    for (int index = 1; index < focusOrder.size(); ++index)
      QWidget::setTabOrder(focusOrder[index - 1], focusOrder[index]);
    connect(accept, &QPushButton::clicked, this, [this] {
      accepted = true;
      warning->hide();
      action(Ack);
      create->setFocus();
    });
    connect(create, &QPushButton::clicked, this,
            [this] { runCreateDialog(); });
    connect(open, &QPushButton::clicked, this, [this] { runOpenDialog(); });
    connect(unlock, &QPushButton::clicked, this, [this] {
      TvInput input{};
      const bool fieldsValid = master->consume(input, 0);
      if (action(Unlock, 0, 0, input, fieldsValid)) {
        lastInput = clock();
        restoreStoredLocale();
      }
    });
    connect(backup, &QPushButton::clicked, this,
            [this] { runBackupDialog(); });
    connect(restore, &QPushButton::clicked, this,
            [this] { runRestoreDialog(); });
    connect(changePassword, &QPushButton::clicked, this,
            [this] { runChangePasswordDialog(); });
    connect(addCustom, &QPushButton::clicked, this,
            [this] { runCustomDialog(false); });
    connect(replaceDictionary, &QPushButton::clicked, this,
            [this] { runCustomDialog(true); });
    connect(renameSheet, &QPushButton::clicked, this,
            [this] { runRenameDialog(); });
    connect(deleteSheet, &QPushButton::clicked, this,
            [this] { runDeleteDialog(); });
    connect(save, &QPushButton::clicked, this, [this] {
      clearInputs();
      if (action(Save))
        announce(uiText(locale, "saved"));
    });
    connect(closeVault, &QPushButton::clicked, this, [this] { finish(Close); });
    connect(lock, &QPushButton::clicked, this, [this] { finish(Lock); });
    connect(add, &QPushButton::clicked, this, [this] {
      clearInputs();
      TvInput input{};
      bool fieldsValid = field(input, 0, sheetName->text());
      fieldsValid &= field(input, 1, lengths->currentData().toString());
      if (action(Add, profiles->currentData().toUInt(),
                 columns->currentData().toUInt(), input, fieldsValid)) {
        updating = true;
        sheets->setCurrentIndex(sheets->count() - 1);
        updating = false;
      }
    });
    connect(profiles, &QComboBox::currentIndexChanged, this,
            [this](int) { refreshProfile(); });
    connect(profileFilter, &QLineEdit::textChanged, this,
            [this](const QString &text) { filterProfiles(text); });
    connect(sheets, &QComboBox::currentIndexChanged, this, [this](int index) {
      if (!updating && index >= 0) {
        clearInputs();
        action(Select, index);
      }
    });
    connect(minutes, &QComboBox::currentIndexChanged, this, [this] {
      if (!updating) {
        action(Timeout, minutes->currentData().toUInt());
        lastInput = clock();
      }
    });
    connect(localeChoice, &QComboBox::currentIndexChanged, this, [this] {
      if (updating)
        return;
      const QString requested = localeChoice->currentData().toString();
      if (requested != "en" && requested != "ru")
        return;
      locale = requested;
      applyLanguage();
      persistProcessLocale();
    });
    connect(themeChoice, &QComboBox::currentIndexChanged, this, [this] {
      if (updating)
        return;
      const QString requested = themeChoice->currentData().toString();
      TvInput input{};
      const bool fieldsValid = field(input, 0, requested);
      if (action(Theme, PreferenceSet, 0, input, fieldsValid)) {
        currentTheme = requested;
        applySemanticTheme(*qApp, this->w, currentTheme);
      }
    });
    for (auto pair :
         {std::pair{set, SetSheetPassword}, std::pair{unlockSheet, UnlockSheet},
          std::pair{unlockMaster, UnlockMaster}})
      connect(pair.first, &QPushButton::clicked, this,
              [this, op = pair.second] {
                TvInput input{};
                const bool fieldsValid = sheetPassword->consume(input, 0);
                action(op, 0, 0, input, fieldsValid);
              });
    connect(protect, &QPushButton::clicked, this, [this] {
      clearInputs();
      action(Protect);
    });
    connect(verify, &QPushButton::clicked, this, [this] {
      if (core.state.verified) {
        action(Verify, 0);
        verificationConsent->setChecked(false);
      } else if (verificationConsent->isChecked()) {
        action(Verify, 1);
        verificationConsent->setChecked(false);
      }
    });
    connect(spin, &QPushButton::clicked, this, [this] {
      if (!spinConsent->isChecked()) {
        clearInputs();
        announce(uiText(locale, "spinAck"));
        return;
      }
      TvInput input{};
      bool fieldsValid = true;
      fieldsValid &= symbol1->consume(input, 0);
      fieldsValid &= symbol2->consume(input, 1);
      fieldsValid &= word->consume(input, 2);
      spinConsent->setChecked(false);
      action(Spin, row->value() - 1, 0, input, fieldsValid);
      symbol1->setFocus();
    });
    auto timer = new QTimer(this);
    timer->setObjectName("inactivityTimer");
    connect(timer, &QTimer::timeout, this, [this] {
      if (core.state.state == 2 &&
          clock() - lastInput >=
              static_cast<qint64>(core.state.minutes) * 60000)
        forceLock();
      else if (core.state.state == 2) {
        TvInput in{};
        QString unused;
        core.action(Tick, timeoutGeneration, 0, in, unused);
        if (core.state.state != 2) {
          clearInputs();
          refresh();
        }
      }
    });
    timer->start(250);
    privacyForegroundTimer = new QTimer(this);
    privacyForegroundTimer->setObjectName("privacyForegroundTimer");
    privacyForegroundTimer->setInterval(50);
    connect(privacyForegroundTimer, &QTimer::timeout, this,
            [this] { evaluatePrivacyDeparture(); });
    connect(qApp, &QGuiApplication::applicationStateChanged, this,
            [this](Qt::ApplicationState state) {
              privacyApplicationState = state;
              const uint32_t generation = ++privacySignalGeneration;
              if (state == Qt::ApplicationActive) {
                resumeFromPrivacy(true);
              } else if (state == Qt::ApplicationSuspended) {
                privacyForegroundTimer->stop();
                forceLock();
              } else {
                privacyForegroundTimer->start();
                QTimer::singleShot(0, this, [this, generation] {
                  if (generation != privacySignalGeneration)
                    return;
                  evaluatePrivacyDeparture();
                });
              }
            });
    qApp->installEventFilter(this);
    action(Info);
    applyLanguage();
    accept->setFocus();
  }
  void prepareForWindowDestruction() {
    // QMainWindow hides child views after Window's destructor body. Retire the
    // bridge-backed model while Bridge is still alive so teardown cannot query
    // decrypted table state through a dangling reference.
    table->setModel(nullptr);
  }
  ~Impl() override {
    qApp->removeEventFilter(this);
  }
  bool close() { return finish(Close); }
  void rejectOwnedDialogs() {
    for (auto widget : QApplication::topLevelWidgets()) {
      if (auto dialog = qobject_cast<QDialog *>(widget);
          dialog && (dialog->parentWidget() == &w || w.isAncestorOf(dialog)))
        dialog->reject();
    }
  }
  void evaluatePrivacyDeparture() {
    if (privacyApplicationState == Qt::ApplicationActive) {
      privacyForegroundTimer->stop();
      return;
    }
    if (privacyApplicationState == Qt::ApplicationSuspended) {
      privacyForegroundTimer->stop();
      forceLock();
      return;
    }
    const quintptr owned = ownedForegroundWindow(w.winId());
    if (owned == w.winId()) {
      if (privacyActive)
        resumeFromPrivacy(false);
      return;
    }
    if (owned) {
      clearInputs();
      trackedOwnedForegroundWindow = owned;
      return;
    }
    enterPrivacyCover();
  }
  void closeTrackedOwnedWindow() {
    const HWND candidate =
        reinterpret_cast<HWND>(trackedOwnedForegroundWindow);
    trackedOwnedForegroundWindow = 0;
    if (!candidate || !IsWindow(candidate) || candidate ==
        reinterpret_cast<HWND>(w.winId()))
      return;
    DWORD processId = 0;
    GetWindowThreadProcessId(candidate, &processId);
    if (processId == GetCurrentProcessId())
      PostMessageW(candidate, WM_CLOSE, 0, 0);
  }
  void enterPrivacyCover() {
    if (privacyActive)
      return;
    clearInputs();
    closeTrackedOwnedWindow();
    rejectOwnedDialogs();
    privacyActive = true;
    pages->setCurrentWidget(privacyCover);
  }
  void resumeFromPrivacy(bool confirmedApplicationActive) {
    if (confirmedApplicationActive)
      privacyApplicationState = Qt::ApplicationActive;
    ++privacySignalGeneration;
    if (confirmedApplicationActive)
      privacyForegroundTimer->stop();
    else
      privacyForegroundTimer->start();
    trackedOwnedForegroundWindow = 0;
    leavePrivacyCover();
  }
  void leavePrivacyCover() {
    if (core.state.state == 2 &&
        clock() - lastInput >=
            static_cast<qint64>(core.state.minutes) * 60000) {
      forceLock();
    } else if (core.state.state == 2) {
      action(Tick, timeoutGeneration);
    }
    if (privacyActive) {
      privacyActive = false;
      pages->setCurrentWidget(appPage);
    }
    refresh();
  }
  void forceLock() {
    // Pending UI input exists even without an open Rust session.
    rejectOwnedDialogs();
    clearInputs();
    if (core.state.state != 2)
      return;
    const bool dirty = core.state.dirty;
    workspace->hide();
    action(Lock, 2);
    announce(dirty ? uiText(locale, "lockedDiscarded") : QString());
  }
  bool eventFilter(QObject *object, QEvent *e) override {
    if (object == &w && e->type() == QEvent::WindowActivate)
      resumeFromPrivacy(false);
    if (e->type() == QEvent::KeyPress ||
        e->type() == QEvent::MouseButtonPress || e->type() == QEvent::Wheel ||
        e->type() == QEvent::TouchBegin) {
      auto widget = qobject_cast<QWidget *>(object);
      if (widget && (widget == &w || w.isAncestorOf(widget)) &&
          core.state.state == 2) {
        if (clock() - lastInput >=
            static_cast<qint64>(core.state.minutes) * 60000) {
          forceLock();
          return true;
        }
        lastInput = clock();
        TvInput in{};
        QString ignored, generationText;
        core.action(Activity, 0, 0, in, ignored, &generationText);
        bool ok = false;
        const uint32_t generation = generationText.toUInt(&ok);
        if (ok && generation != 0)
          timeoutGeneration = generation;
        if (core.state.state != 2) {
          clearInputs();
          refresh();
          return true;
        }
      }
    }
    return false;
  }
};
Window::Window(std::function<qint64()> clock,
               std::function<bool(quintptr)> registerSession,
               std::function<quintptr(quintptr)> ownedForegroundWindow)
    : QMainWindow(),
      impl(new Impl(*this, std::move(clock),
                    std::move(ownedForegroundWindow))) {
  notificationsRegistered =
      registerSession
          ? registerSession(winId())
          : WTSRegisterSessionNotification(reinterpret_cast<HWND>(winId()),
                                           NOTIFY_FOR_THIS_SESSION);
  if (!notificationsRegistered) {
    impl->forceLock();
    centralWidget()->setEnabled(false);
    statusBar()->showMessage(uiText("en", "sessionMonitor"));
  }
}
Window::~Window() {
  impl->prepareForWindowDestruction();
  if (notificationsRegistered)
    WTSUnRegisterSessionNotification(reinterpret_cast<HWND>(winId()));
  // Impl is parented to Window. Let QObject retire it after QMainWindow and
  // QWidget finish hiding/destroying child controls that may emit signals.
}
void Window::closeEvent(QCloseEvent *e) {
  if (impl->close())
    e->accept();
  else
    e->ignore();
}
bool Window::nativeEvent(const QByteArray &type, void *message,
                         qintptr *result) {
  auto m = static_cast<MSG *>(message);
  if ((m->message == WM_WTSSESSION_CHANGE && m->wParam == WTS_SESSION_LOCK) ||
      (m->message == WM_POWERBROADCAST &&
       (m->wParam == PBT_APMSUSPEND || m->wParam == PBT_APMQUERYSUSPEND))) {
    impl->forceLock();
    *result = TRUE;
    return true;
  }
  return QMainWindow::nativeEvent(type, message, result);
}
