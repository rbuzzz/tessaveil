#include "../bridge.h"
#include "../window.h"
#include <QtTest>
#include <QtWidgets>
#include <cstdio>
#include <windows.h>
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
int main(int argc, char **argv) {
  QApplication app(argc, argv);
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
  QFile damaged(dir.filePath("synthetic.tessaveil-alpha"));
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
