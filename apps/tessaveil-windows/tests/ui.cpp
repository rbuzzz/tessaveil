#include "../bridge.h"
#include "../window.h"
#include <QtTest>
#include <QtWidgets>
#include <cstdio>
#include <windows.h>
#include <wtsapi32.h>
#define REQUIRE(x)                                                             \
  do {                                                                         \
    if (!(x)) {                                                                \
      std::fprintf(stderr, "FAIL line %d: %s\n", __LINE__, #x);                \
      return 1;                                                                \
    }                                                                          \
  } while (0)
template <class T> T *find(Window &w, const char *name) {
  return w.findChild<T *>(name);
}
// These helpers seed only invented pending input, never a real phrase.
void pendingContext(Window &w) {
  for (const auto name :
       {"master", "sheetPassword", "word", "symbol1", "symbol2"})
    find<QLineEdit>(w, name)->setText("synthetic-pending");
  for (const auto name : {"spinConsent", "verificationConsent"})
    find<QCheckBox>(w, name)->setChecked(true);
}
bool contextIsClear(Window &w) {
  for (const auto name :
       {"master", "sheetPassword", "word", "symbol1", "symbol2"}) {
    const auto input = find<QLineEdit>(w, name);
    if (!input->text().isEmpty() || input->isUndoAvailable())
      return false;
  }
  return !find<QCheckBox>(w, "spinConsent")->isChecked() &&
         !find<QCheckBox>(w, "verificationConsent")->isChecked();
}
int privacyEventsScrubEveryState(QApplication &app) {
  Window w;
  w.show();
  QTest::qWait(100);
  find<QPushButton>(w, "warningAccept")->click();
  QTemporaryDir dir;
  REQUIRE(dir.isValid());
  const auto vaultPath = dir.filePath("privacy-synthetic.tessaveil-alpha");
  auto path = find<QLineEdit>(w, "path");
  path->setText(vaultPath);
  auto master = find<QLineEdit>(w, "master");
  auto state = find<QLabel>(w, "state");
  QByteArray savedImage;
  for (int initialState = 0; initialState < 3; ++initialState) {
    if (initialState == 1) {
      master->setText("synthetic-master-password");
      find<QPushButton>(w, "create")->click();
      find<QPushButton>(w, "add")->click();
      find<QPushButton>(w, "save")->click();
      REQUIRE(state->text() == "Open / saved");
      QFile vault(vaultPath);
      REQUIRE(vault.open(QIODevice::ReadOnly));
      savedImage = vault.readAll(); // Encrypted file, not the payload.
      find<QPushButton>(w, "lock")->click();
    }
    for (int route = 0; route < 6; ++route) {
      if (initialState == 2) {
        master->setText("synthetic-master-password");
        find<QPushButton>(w, "unlock")->click();
        REQUIRE(find<QComboBox>(w, "sheets")->count() == 1);
        find<QPushButton>(w, "add")->click();
        REQUIRE(state->text() == "Open / unsaved changes");
      }
      pendingContext(w);
      REQUIRE(!contextIsClear(w));
      Q_EMIT app.applicationStateChanged(Qt::ApplicationActive);
      REQUIRE(!contextIsClear(w));
      switch (route) {
      case 0:
        Q_EMIT app.applicationStateChanged(Qt::ApplicationInactive);
        break;
      case 1:
        Q_EMIT app.applicationStateChanged(Qt::ApplicationHidden);
        break;
      case 2:
        Q_EMIT app.applicationStateChanged(Qt::ApplicationSuspended);
        break;
      case 3:
        SendMessage(reinterpret_cast<HWND>(w.winId()), WM_POWERBROADCAST,
                    PBT_APMSUSPEND, 0);
        break;
      case 4:
        SendMessage(reinterpret_cast<HWND>(w.winId()), WM_POWERBROADCAST,
                    PBT_APMQUERYSUSPEND, 0);
        break;
      case 5:
        SendMessage(reinterpret_cast<HWND>(w.winId()), WM_WTSSESSION_CHANGE,
                    WTS_SESSION_LOCK, 0);
        break;
      }
      REQUIRE(contextIsClear(w));
      REQUIRE(path->text() == vaultPath);
      REQUIRE(initialState == 0 ? state->text() == "Closed"
                                : state->text().startsWith("Locked"));
      REQUIRE(find<QTableView>(w, "table")->model()->rowCount() == 0);
      if (initialState != 0) {
        QFile vault(vaultPath);
        REQUIRE(vault.open(QIODevice::ReadOnly));
        REQUIRE(vault.readAll() == savedImage);
      }
    }
  }
  master->setText("synthetic-master-password");
  find<QPushButton>(w, "unlock")->click();
  REQUIRE(find<QComboBox>(w, "sheets")->count() == 1);
  find<QPushButton>(w, "closeVault")->click();
  return 0;
}
QByteArray tableDigest(QTableView *table) {
  QCryptographicHash hash(QCryptographicHash::Sha256);
  auto model = table->model();
  for (int row = 0; row < model->rowCount(); ++row)
    for (int column = 0; column < model->columnCount(); ++column) {
      hash.addData(model->data(model->index(row, column)).toString().toUtf8());
      hash.addData(QByteArray(1, '\0'));
    }
  return hash.result(); // Retain a digest, not a copy of the whole table.
}
int oversizedUnicodeKeepsDirtySession() {
  Window w;
  w.show();
  QTest::qWait(100);
  find<QPushButton>(w, "warningAccept")->click();
  QTemporaryDir dir;
  REQUIRE(dir.isValid());
  const auto vaultPath = dir.filePath("unicode-synthetic.tessaveil-alpha");
  find<QLineEdit>(w, "path")->setText(vaultPath);
  find<QLineEdit>(w, "master")->setText("synthetic-master-password");
  find<QPushButton>(w, "create")->click();
  auto add = find<QPushButton>(w, "add");
  add->click();
  find<QPushButton>(w, "save")->click();
  QFile vault(vaultPath);
  REQUIRE(vault.open(QIODevice::ReadOnly));
  const auto savedImage = vault.readAll();
  vault.close();
  add->click();
  auto state = find<QLabel>(w, "state");
  auto table = find<QTableView>(w, "table");
  auto sheets = find<QComboBox>(w, "sheets");
  auto password = find<QLineEdit>(w, "sheetPassword");
  REQUIRE(state->text() == "Open / unsaved changes");
  const auto digest = tableDigest(table);
  const int rows = table->model()->rowCount();
  const int sheetCount = sheets->count();
  password->setText(QString(2049, QChar(0x044f)));
  find<QPushButton>(w, "setSheetPassword")->click();
  REQUIRE(state->text() == "Open / unsaved changes");
  REQUIRE(password->text().isEmpty());
  REQUIRE(sheets->count() == sheetCount);
  REQUIRE(table->model()->rowCount() == rows);
  REQUIRE(tableDigest(table) == digest);
  const auto error = find<QLabel>(w, "message")->text();
  REQUIRE(error.contains("4096") && error.contains("Shorten"));
  REQUIRE(vault.open(QIODevice::ReadOnly));
  REQUIRE(vault.readAll() == savedImage);
  vault.close();
  password->setText("synthetic-sheet-password");
  find<QPushButton>(w, "setSheetPassword")->click();
  REQUIRE(state->text() == "Open / unsaved changes");
  find<QPushButton>(w, "save")->click();
  REQUIRE(state->text() == "Open / saved");
  REQUIRE(vault.open(QIODevice::ReadOnly));
  REQUIRE(vault.readAll() != savedImage);
  vault.close();
  find<QPushButton>(w, "closeVault")->click();
  return 0;
}
int addingSheetScrubsPreviousContext() {
  Window w;
  w.show();
  QTest::qWait(100);
  find<QPushButton>(w, "warningAccept")->click();
  QTemporaryDir dir;
  REQUIRE(dir.isValid());
  const auto vaultPath =
      dir.filePath("sheet-context-synthetic.tessaveil-alpha");
  find<QLineEdit>(w, "path")->setText(vaultPath);
  find<QLineEdit>(w, "master")->setText("synthetic-master-password");
  find<QPushButton>(w, "create")->click();
  auto add = find<QPushButton>(w, "add");
  auto columns = find<QComboBox>(w, "columns");
  columns->setCurrentIndex(0);
  add->click();
  auto table = find<QTableView>(w, "table");
  REQUIRE(table->model()->columnCount() == 10);
  auto verifyConsent = find<QCheckBox>(w, "verificationConsent");
  verifyConsent->setChecked(true);
  find<QPushButton>(w, "verify")->click();
  find<QLineEdit>(w, "sheetPassword")->setText("synthetic-sheet-password");
  find<QPushButton>(w, "setSheetPassword")->click();
  find<QPushButton>(w, "protect")->click();
  const auto firstDigest = tableDigest(table);
  auto sheetState = find<QLabel>(w, "sheetState");
  REQUIRE(sheetState->text().contains("Protected"));
  REQUIRE(sheetState->text().contains("Verified by me"));
  auto sheetName = find<QLineEdit>(w, "sheetName");
  sheetName->setText("Synthetic second sheet");
  columns->setCurrentIndex(1);
  auto profiles = find<QComboBox>(w, "profiles");
  const int profile = profiles->currentIndex();
  pendingContext(w);
  REQUIRE(!contextIsClear(w));
  add->click();
  REQUIRE(contextIsClear(w));
  auto sheets = find<QComboBox>(w, "sheets");
  REQUIRE(sheets->count() == 2 && sheets->currentIndex() == 1);
  REQUIRE(sheets->currentText() == "Synthetic second sheet");
  REQUIRE(sheetName->text() == "Synthetic second sheet");
  REQUIRE(find<QLineEdit>(w, "path")->text() == vaultPath);
  REQUIRE(profiles->currentIndex() == profile);
  REQUIRE(columns->currentIndex() == 1);
  REQUIRE(table->model()->rowCount() == 24);
  REQUIRE(table->model()->columnCount() == 36);
  REQUIRE(sheetState->text().contains("Editing enabled"));
  REQUIRE(!sheetState->text().contains("Verified by me"));
  const auto secondDigest = tableDigest(table);
  // Neither old acknowledgment may authorize an action in the new context.
  find<QPushButton>(w, "verify")->click();
  REQUIRE(!sheetState->text().contains("Verified by me"));
  find<QPushButton>(w, "spin")->click();
  REQUIRE(tableDigest(table) == secondDigest);
  REQUIRE(contextIsClear(w));
  find<QLineEdit>(w, "symbol1")->setText("?");
  find<QLineEdit>(w, "symbol2")->setText("!");
  find<QLineEdit>(w, "word")->setText("synthetic-fresh-invalid-token");
  find<QCheckBox>(w, "spinConsent")->setChecked(true);
  find<QPushButton>(w, "spin")->click();
  REQUIRE(contextIsClear(w));
  const auto spunDigest = tableDigest(table);
  REQUIRE(spunDigest != secondDigest);
  verifyConsent->setChecked(true);
  find<QPushButton>(w, "verify")->click();
  REQUIRE(sheetState->text().contains("Verified by me"));
  pendingContext(w);
  sheets->setCurrentIndex(0);
  REQUIRE(contextIsClear(w));
  REQUIRE(table->model()->columnCount() == 10);
  REQUIRE(tableDigest(table) == firstDigest);
  REQUIRE(sheetState->text().contains("Protected"));
  REQUIRE(sheetState->text().contains("Verified by me"));
  sheets->setCurrentIndex(1);
  REQUIRE(table->model()->columnCount() == 36);
  REQUIRE(tableDigest(table) == spunDigest);
  REQUIRE(sheetState->text().contains("Editing enabled"));
  REQUIRE(sheetState->text().contains("Verified by me"));
  find<QPushButton>(w, "save")->click();
  find<QPushButton>(w, "closeVault")->click();
  return 0;
}
int main(int argc, char **argv) {
  QApplication app(argc, argv);
  REQUIRE(privacyEventsScrubEveryState(app) == 0);
  REQUIRE(oversizedUnicodeKeepsDirtySession() == 0);
  REQUIRE(addingSheetScrubsPreviousContext() == 0);
  {
    Window unavailable({}, [](quintptr) { return false; });
    REQUIRE(!unavailable.centralWidget()->isEnabled());
  }
  qint64 now = 0;
  Window w([&] { return now; });
  w.show();
  QTest::qWait(100);
  auto accept = find<QPushButton>(w, "warningAccept");
  REQUIRE(accept);
  auto create = find<QPushButton>(w, "create");
  REQUIRE(create);
  REQUIRE(!create->isEnabled());
  accept->click();
  REQUIRE(create->isEnabled());
  auto path = find<QLineEdit>(w, "path");
  auto password = find<QLineEdit>(w, "master");
  REQUIRE(path && password);
  REQUIRE(password->echoMode() == QLineEdit::Password);
  REQUIRE(!password->acceptDrops());
  REQUIRE(password->contextMenuPolicy() == Qt::NoContextMenu);
  password->setText("synthetic-input");
  password->selectAll();
  QSignalSpy clipboardChanges(QApplication::clipboard(),
                              &QClipboard::dataChanged);
  QKeyEvent shortcut(QEvent::ShortcutOverride, Qt::Key_V, Qt::ControlModifier);
  shortcut.setAccepted(false);
  QApplication::sendEvent(password, &shortcut);
  REQUIRE(shortcut.isAccepted());
  QTest::keyClick(password, Qt::Key_C, Qt::ControlModifier);
  REQUIRE(clipboardChanges.count() == 0);
  QTest::keyClick(password, Qt::Key_V, Qt::ControlModifier);
  REQUIRE(password->text() == "synthetic-input");
  password->clear();
  password->setFocus();
  QTest::keyClick(password, Qt::Key_Tab);
  REQUIRE(QApplication::focusWidget() != password);
  QTemporaryDir dir;
  REQUIRE(dir.isValid());
  path->setText(dir.filePath("synthetic.tessaveil-alpha"));
  password->setText("synthetic-master-password");
  create->click();
  REQUIRE(password->text().isEmpty());
  auto state = find<QLabel>(w, "state");
  REQUIRE(state->text().startsWith("Open"));
  auto profiles = find<QComboBox>(w, "profiles");
  REQUIRE(profiles);
  int available = 0;
  for (int i = 0; i < profiles->count(); ++i) {
    if (profiles->model()->flags(profiles->model()->index(i, 0)) &
        Qt::ItemIsEnabled) {
      available++;
      profiles->setCurrentIndex(i);
    }
  }
  REQUIRE(available == 3);
  auto columns = find<QComboBox>(w, "columns");
  auto add = find<QPushButton>(w, "add");
  auto table = find<QTableView>(w, "table");
  REQUIRE(columns && add && table);
  columns->setCurrentIndex(0);
  add->click();
  REQUIRE(table->model()->columnCount() == 10);
  REQUIRE(table->model()->rowCount() == 24);
  REQUIRE(table->findChildren<QLineEdit *>().isEmpty());
  REQUIRE(table->selectionMode() == QAbstractItemView::NoSelection);
  REQUIRE(!table->acceptDrops());
  REQUIRE(table->contextMenuPolicy() == Qt::NoContextMenu);
  columns->setCurrentIndex(1);
  add->click();
  REQUIRE(table->model()->columnCount() == 36);
  auto nextSheet = find<QPushButton>(w, "nextSheet");
  REQUIRE(nextSheet);
  nextSheet->click();
  REQUIRE(table->model()->columnCount() == 10);
  nextSheet->click();
  REQUIRE(table->model()->columnCount() == 36);
  REQUIRE(table->tabKeyNavigation() == false);
  QCoreApplication::processEvents();
  REQUIRE(table->height() >= 150);
  REQUIRE(table->font().family() == "Consolas");
  REQUIRE(table->verticalHeader()->defaultSectionSize() <= 30);
  for (auto control : w.findChildren<QPushButton *>()) {
    if (control->isVisible())
      REQUIRE(control->height() >= 26);
  }
  table->horizontalScrollBar()->setValue(
      table->horizontalScrollBar()->maximum());
  table->verticalScrollBar()->setValue(table->verticalScrollBar()->maximum());
  REQUIRE(table->horizontalScrollBar()->value() > 0);
  REQUIRE(table->verticalScrollBar()->value() > 0);
  table->setFocus();
  QTest::keyClick(table, Qt::Key_Tab);
  REQUIRE(QApplication::focusWidget() != table);
  QTest::keyClick(table, Qt::Key_A, Qt::ControlModifier);
  REQUIRE(table->selectionModel()->selectedIndexes().isEmpty());
  QContextMenuEvent context(QContextMenuEvent::Mouse, QPoint(5, 5),
                            QPoint(5, 5));
  QApplication::sendEvent(password, &context);
  REQUIRE(!QApplication::activePopupWidget());
  auto secret = find<QLineEdit>(w, "sheetPassword");
  REQUIRE(secret);
  secret->setText("synthetic-sheet-password");
  find<QPushButton>(w, "setSheetPassword")->click();
  REQUIRE(secret->text().isEmpty());
  find<QPushButton>(w, "protect")->click();
  REQUIRE(!find<QPushButton>(w, "spin")->isEnabled());
  secret->setText("synthetic-sheet-password");
  find<QPushButton>(w, "unlockSheet")->click();
  REQUIRE(find<QPushButton>(w, "spin")->isEnabled());
  auto verify = find<QCheckBox>(w, "verificationConsent");
  REQUIRE(verify);
  verify->setChecked(true);
  find<QPushButton>(w, "verify")->click();
  REQUIRE(find<QLabel>(w, "sheetState")->text().contains("Verified by me"));
  find<QCheckBox>(w, "spinConsent")->setChecked(true);
  find<QLineEdit>(w, "symbol1")->setText("?");
  find<QLineEdit>(w, "symbol2")->setText("!");
  find<QLineEdit>(w, "word")->setText("synthetic-invalid-token");
  find<QPushButton>(w, "spin")->click();
  REQUIRE(find<QLineEdit>(w, "word")->text().isEmpty());
  REQUIRE(find<QLabel>(w, "message")->text().isEmpty());
  REQUIRE(!find<QLabel>(w, "sheetState")->text().contains("Verified by me"));
  find<QPushButton>(w, "save")->click();
  REQUIRE(state->text() == "Open / saved");
  find<QPushButton>(w, "closeVault")->click();
  REQUIRE(state->text() == "Closed");
  password->setText("synthetic-master-password");
  find<QPushButton>(w, "open")->click();
  REQUIRE(state->text() == "Open / saved");
  REQUIRE(table->model()->columnCount() == 10);
  auto timer = find<QTimer>(w, "inactivityTimer");
  REQUIRE(timer);
  now = 299999;
  QMetaObject::invokeMethod(timer, "timeout", Qt::DirectConnection);
  REQUIRE(state->text().startsWith("Open"));
  now = 300000;
  QMetaObject::invokeMethod(timer, "timeout", Qt::DirectConnection);
  REQUIRE(state->text().startsWith("Locked"));
  REQUIRE(table->model()->rowCount() == 0);
  password->setText("synthetic-master-password");
  find<QPushButton>(w, "unlock")->click();
  REQUIRE(state->text().startsWith("Open"));
  find<QPushButton>(w, "lock")->click();
  REQUIRE(state->text().startsWith("Locked"));
  password->setText("synthetic-wrong-password");
  find<QPushButton>(w, "unlock")->click();
  const auto authentication = find<QLabel>(w, "message")->text();
  REQUIRE(authentication ==
          "The password is incorrect or the vault is damaged.");
  REQUIRE(password->text().isEmpty());
  find<QPushButton>(w, "closeVault")->click();
  const auto corruptPath = dir.filePath("corrupt-copy.tessaveil-alpha");
  REQUIRE(QFile::copy(dir.filePath("synthetic.tessaveil-alpha"), corruptPath));
  path->setText(corruptPath);
  QFile damaged(corruptPath);
  REQUIRE(damaged.open(QIODevice::ReadWrite));
  REQUIRE(damaged.seek(damaged.size() - 1));
  auto byte = damaged.read(1);
  REQUIRE(byte.size() == 1);
  byte[0] = byte[0] ^ 1;
  REQUIRE(damaged.seek(damaged.size() - 1));
  REQUIRE(damaged.write(byte) == 1);
  damaged.close();
  password->setText("synthetic-master-password");
  find<QPushButton>(w, "open")->click();
  REQUIRE(state->text() == "Closed");
  REQUIRE(find<QLabel>(w, "message")->text() == authentication);
  path->setText(dir.filePath("synthetic.tessaveil-alpha"));
  password->setText("synthetic-master-password");
  find<QPushButton>(w, "open")->click();
  REQUIRE(state->text() == "Open / saved");
  find<QPushButton>(w, "closeVault")->click();
  path->setText(dir.filePath("second.tessaveil-alpha"));
  password->setText("synthetic-master-password");
  create->click();
  add->click();
  find<QLineEdit>(w, "word")->setText("synthetic-pending");
  SendMessage(reinterpret_cast<HWND>(w.winId()), WM_POWERBROADCAST,
              PBT_APMSUSPEND, 0);
  REQUIRE(state->text().startsWith("Locked"));
  REQUIRE(find<QLineEdit>(w, "word")->text().isEmpty());
  REQUIRE(table->model()->rowCount() == 0);
  password->setText("synthetic-master-password");
  find<QPushButton>(w, "unlock")->click();
  REQUIRE(table->model()->rowCount() == 0);
  add->click();
  Q_EMIT app.applicationStateChanged(Qt::ApplicationInactive);
  REQUIRE(state->text().startsWith("Locked"));
  password->setText("synthetic-master-password");
  find<QPushButton>(w, "unlock")->click();
  add->click();
  QTimer::singleShot(0, [&] {
    auto box = qobject_cast<QMessageBox *>(QApplication::activeModalWidget());
    if (box)
      box->button(QMessageBox::Cancel)->click();
  });
  find<QPushButton>(w, "closeVault")->click();
  // The host can deactivate this native test during the modal. Both outcomes
  // must fail safe: Cancel preserves dirty state, or lifecycle lock discards
  // it.
  REQUIRE(state->text() == "Open / unsaved changes" ||
          state->text().startsWith("Locked"));
  REQUIRE(clipboardChanges.count() == 0);
  std::puts("PASS: native synthetic workflow, restrictions, focus, "
            "virtualization, inactivity");
  return 0;
}
