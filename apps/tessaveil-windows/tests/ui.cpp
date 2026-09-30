#include "../bridge.h"
#include "../ui/strings.h"
#include "../window.h"
#include <QtTest>
#include <QtWidgets>
#include <cstdio>
#include <memory>
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
HWND nativePickerWindow() {
  struct Search {
    DWORD process = GetCurrentProcessId();
    HWND window = nullptr;
  } search;
  EnumWindows(
      [](HWND window, LPARAM value) -> BOOL {
        auto search = reinterpret_cast<Search *>(value);
        DWORD process = 0;
        GetWindowThreadProcessId(window, &process);
        wchar_t className[32]{};
        GetClassNameW(window, className,
                      static_cast<int>(std::size(className)));
        if (process == search->process && IsWindowVisible(window) &&
            wcscmp(className, L"#32770") == 0) {
          search->window = window;
          return FALSE;
        }
        return TRUE;
      },
      reinterpret_cast<LPARAM>(&search));
  return search.window;
}
void inspectAndCloseNativePicker(std::function<void()> inspect,
                                 bool &observed) {
  auto attempts = std::make_shared<int>(0);
  auto retry = std::make_shared<std::function<void()>>();
  *retry = [attempts, retry, inspect = std::move(inspect), &observed] {
    if (const HWND picker = nativePickerWindow()) {
      observed = true;
      inspect();
      PostMessageW(picker, WM_CLOSE, 0, 0);
      *retry = {};
      return;
    }
    if (++*attempts < 200)
      QTimer::singleShot(10, *retry);
  };
  QTimer::singleShot(0, *retry);
}
void scheduleDialog(std::function<void(QDialog *)> configure) {
  QTimer::singleShot(0, [configure = std::move(configure)] {
    if (auto dialog = qobject_cast<QDialog *>(QApplication::activeModalWidget()))
      configure(dialog);
  });
}
struct DialogProbe {
  bool configured = false;
  int watchedSecrets = 0;
  QSet<const QObject *> clearedSecrets;
  bool allSecretsCleared() const {
    return clearedSecrets.size() == watchedSecrets;
  }
};
void watchSecret(QLineEdit *input, const QString &value, DialogProbe &probe) {
  ++probe.watchedSecrets;
  QObject::connect(input, &QLineEdit::textChanged, input,
                   [&probe, input](const QString &text) {
                     if (text.isEmpty())
                       probe.clearedSecrets.insert(input);
                   });
  input->setText(value);
}
DialogProbe attemptDialog(
    Window &w, const char *buttonName,
    std::function<void(QDialog *, DialogProbe &)> configure) {
  DialogProbe probe;
  scheduleDialog([&](QDialog *dialog) {
    probe.configured = true;
    configure(dialog, probe);
    dialog->accept();
  });
  find<QPushButton>(w, buttonName)->click();
  return probe;
}
void createVault(Window &w, const QString &path, const QString &password,
                 const QString &name = "Synthetic vault") {
  scheduleDialog([=](QDialog *dialog) {
    dialog->findChild<QLineEdit *>("createPath")->setText(path);
    dialog->findChild<QLineEdit *>("createVaultName")->setText(name);
    dialog->findChild<QLineEdit *>("createMaster")->setText(password);
    dialog->findChild<QLineEdit *>("createConfirmation")->setText(password);
    dialog->accept();
  });
  find<QPushButton>(w, "create")->click();
}
void openVault(Window &w, const QString &path, const QString &password) {
  scheduleDialog([=](QDialog *dialog) {
    dialog->findChild<QLineEdit *>("openPath")->setText(path);
    dialog->findChild<QLineEdit *>("openMaster")->setText(password);
    dialog->accept();
  });
  find<QPushButton>(w, "open")->click();
}
int privacyEventsScrubEveryState(QApplication &app) {
  Window w({}, {}, [](quintptr) { return 0; });
  w.show();
  QTest::qWait(100);
  find<QPushButton>(w, "warningAccept")->click();
  QTemporaryDir dir;
  REQUIRE(dir.isValid());
  const auto vaultPath = dir.filePath("privacy-synthetic.tessaveil-alpha");
  auto path = find<QLineEdit>(w, "path");
  auto master = find<QLineEdit>(w, "master");
  auto state = find<QLabel>(w, "state");
  auto cover = find<QWidget>(w, "privacyCover");
  REQUIRE(cover);
  pendingContext(w);
  Q_EMIT app.applicationStateChanged(Qt::ApplicationInactive);
  QCoreApplication::processEvents();
  REQUIRE(contextIsClear(w));
  REQUIRE(cover->isVisible());
  REQUIRE(state->text() == "Closed");
  Q_EMIT app.applicationStateChanged(Qt::ApplicationActive);
  REQUIRE(!cover->isVisible());

  // A real native picker can return focus to the main HWND before Qt emits a
  // matching application-state signal. Window activation must still uncover.
  Q_EMIT app.applicationStateChanged(Qt::ApplicationInactive);
  QCoreApplication::processEvents();
  REQUIRE(cover->isVisible());
  QEvent activateWindow(QEvent::WindowActivate);
  QApplication::sendEvent(&w, &activateWindow);
  REQUIRE(!cover->isVisible());

  createVault(w, vaultPath, "synthetic-master-password");
  find<QPushButton>(w, "add")->click();
  find<QPushButton>(w, "save")->click();
  REQUIRE(state->text() == "Open / saved");
  QFile vault(vaultPath);
  REQUIRE(vault.open(QIODevice::ReadOnly));
  const auto savedImage = vault.readAll(); // Encrypted file, not the payload.
  vault.close();
  find<QPushButton>(w, "add")->click();
  REQUIRE(state->text() == "Open / unsaved changes");
  const int dirtySheetCount = find<QComboBox>(w, "sheets")->count();
  pendingContext(w);
  Q_EMIT app.applicationStateChanged(Qt::ApplicationInactive);
  QCoreApplication::processEvents();
  REQUIRE(contextIsClear(w));
  REQUIRE(cover->isVisible());
  REQUIRE(state->text() == "Open / unsaved changes");
  REQUIRE(find<QComboBox>(w, "sheets")->count() == dirtySheetCount);
  REQUIRE(find<QTableView>(w, "table")->model()->rowCount() == 24);
  Q_EMIT app.applicationStateChanged(Qt::ApplicationActive);
  REQUIRE(!cover->isVisible());
  REQUIRE(state->text() == "Open / unsaved changes");

  pendingContext(w);
  SendMessage(reinterpret_cast<HWND>(w.winId()), WM_WTSSESSION_CHANGE,
              WTS_SESSION_LOCK, 0);
  REQUIRE(contextIsClear(w));
  REQUIRE(state->text().startsWith("Locked"));
  REQUIRE(find<QTableView>(w, "table")->model()->rowCount() == 0);
  REQUIRE(vault.open(QIODevice::ReadOnly));
  REQUIRE(vault.readAll() == savedImage);
  vault.close();
  master->setText("synthetic-master-password");
  find<QPushButton>(w, "unlock")->click();
  REQUIRE(find<QComboBox>(w, "sheets")->count() == 1);
  pendingContext(w);
  SendMessage(reinterpret_cast<HWND>(w.winId()), WM_POWERBROADCAST,
              PBT_APMSUSPEND, 0);
  REQUIRE(contextIsClear(w));
  REQUIRE(state->text().startsWith("Locked"));
  master->setText("synthetic-master-password");
  find<QPushButton>(w, "unlock")->click();
  find<QPushButton>(w, "closeVault")->click();
  return 0;
}
int pickerAltTabCannotBypassPrivacy(QApplication &app) {
  qint64 now = 0;
  quintptr ownedForeground = 0;
  Window w([&] { return now; }, {},
           [&](quintptr) { return ownedForeground; });
  w.show();
  QTest::qWait(100);
  find<QPushButton>(w, "warningAccept")->click();
  QTemporaryDir dir;
  REQUIRE(dir.isValid());
  createVault(w, dir.filePath("picker-privacy.tessaveil-alpha"),
              "synthetic-master-password");
  auto privacyTimer = find<QTimer>(w, "privacyForegroundTimer");
  auto cover = find<QWidget>(w, "privacyCover");
  auto state = find<QLabel>(w, "state");
  REQUIRE(privacyTimer && cover && state);

  // A process-owned native picker stays usable while it is foreground.
  pendingContext(w);
  ownedForeground = 1;
  Q_EMIT app.applicationStateChanged(Qt::ApplicationInactive);
  QMetaObject::invokeMethod(privacyTimer, "timeout", Qt::DirectConnection);
  REQUIRE(!cover->isVisible());
  REQUIRE(contextIsClear(w));

  // Alt-Tab to an external process is detected without a second state signal.
  ownedForeground = 0;
  QMetaObject::invokeMethod(privacyTimer, "timeout", Qt::DirectConnection);
  REQUIRE(cover->isVisible());
  REQUIRE(contextIsClear(w));

  // Some Windows transitions restore the main HWND before Qt publishes the
  // matching ApplicationActive signal. The bounded foreground monitor must
  // uncover only for that exact HWND and keep detecting another departure.
  ownedForeground = w.winId();
  QMetaObject::invokeMethod(privacyTimer, "timeout", Qt::DirectConnection);
  REQUIRE(!cover->isVisible());
  ownedForeground = 0;
  QMetaObject::invokeMethod(privacyTimer, "timeout", Qt::DirectConnection);
  REQUIRE(cover->isVisible());
  now = 1000;
  Q_EMIT app.applicationStateChanged(Qt::ApplicationActive);
  REQUIRE(!cover->isVisible());
  REQUIRE(state->text().startsWith("Open"));

  // Returning from an owned picker still checks the current timeout generation.
  pendingContext(w);
  ownedForeground = 1;
  Q_EMIT app.applicationStateChanged(Qt::ApplicationInactive);
  QMetaObject::invokeMethod(privacyTimer, "timeout", Qt::DirectConnection);
  REQUIRE(!cover->isVisible());
  now = 300000;
  Q_EMIT app.applicationStateChanged(Qt::ApplicationActive);
  REQUIRE(contextIsClear(w));
  REQUIRE(state->text().startsWith("Locked"));
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
int nativePickersScrubBeforeTheyBecomeUsable() {
  Window w;
  w.show();
  QTest::qWait(100);
  find<QPushButton>(w, "warningAccept")->click();
  auto exercise = [&](const char *actionName, const char *pathName,
                      std::function<void(QDialog *)> seed,
                      std::function<bool(QDialog *)> dialogIsClear) {
    bool configured = false;
    bool pickerObserved = false;
    bool scrubbed = false;
    bool readOnly = false;
    bool cancelledPathPreserved = false;
    scheduleDialog([&](QDialog *dialog) {
      auto selectedPath = dialog->findChild<QLineEdit *>(pathName);
      auto browse = dialog->findChild<QPushButton *>(
          QByteArray(pathName).append("Browse"));
      if (!selectedPath || !browse)
        return;
      configured = true;
      selectedPath->setText("synthetic-selected-path");
      seed(dialog);
      pendingContext(w);
      inspectAndCloseNativePicker(
          [&] {
            scrubbed = contextIsClear(w) && dialogIsClear(dialog);
            readOnly = selectedPath->isReadOnly();
          },
          pickerObserved);
      browse->click();
      cancelledPathPreserved =
          selectedPath->text() == "synthetic-selected-path";
      dialog->reject();
    });
    find<QPushButton>(w, actionName)->click();
    return configured && pickerObserved && scrubbed && readOnly &&
           cancelledPathPreserved;
  };

  REQUIRE(exercise(
      "create", "createPath",
      [](QDialog *dialog) {
        dialog->findChild<QLineEdit *>("createMaster")
            ->setText("synthetic-pending");
        dialog->findChild<QLineEdit *>("createConfirmation")
            ->setText("synthetic-pending");
      },
      [](QDialog *dialog) {
        return dialog->findChild<QLineEdit *>("createMaster")->text().isEmpty() &&
               dialog->findChild<QLineEdit *>("createConfirmation")
                   ->text()
                   .isEmpty();
      }));
  REQUIRE(exercise(
      "open", "openPath",
      [](QDialog *dialog) {
        dialog->findChild<QLineEdit *>("openMaster")
            ->setText("synthetic-pending");
      }, [](QDialog *dialog) {
        return dialog->findChild<QLineEdit *>("openMaster")->text().isEmpty();
      }));
  for (const char *pathName : {"restoreSource", "restoreDestination"}) {
    REQUIRE(exercise(
        "restore", pathName,
        [](QDialog *dialog) {
          dialog->findChild<QLineEdit *>("restorePassword")
              ->setText("synthetic-pending");
        }, [](QDialog *dialog) {
          return dialog->findChild<QLineEdit *>("restorePassword")
              ->text()
              .isEmpty();
        }));
  }

  QTemporaryDir dir;
  REQUIRE(dir.isValid());
  const QString vault = dir.filePath("picker-synthetic.tessaveil-alpha");
  createVault(w, vault, "synthetic-master-password");
  find<QPushButton>(w, "add")->click();
  find<QPushButton>(w, "save")->click();
  find<QPushButton>(w, "add")->click();
  auto table = find<QTableView>(w, "table");
  const QByteArray digest = tableDigest(table);
  const int sheets = find<QComboBox>(w, "sheets")->count();
  const QString activePath = find<QLineEdit>(w, "path")->text();
  const auto sessionPreserved = [&] {
    return find<QLabel>(w, "state")->text() == "Open / unsaved changes" &&
           find<QComboBox>(w, "sheets")->count() == sheets &&
           find<QLineEdit>(w, "path")->text() == activePath &&
           tableDigest(table) == digest;
  };
  const auto noSeed = [](QDialog *) {};
  const auto noDialogSecret = [](QDialog *) { return true; };
  REQUIRE(exercise("backup", "backupPath", noSeed, noDialogSecret));
  REQUIRE(sessionPreserved());
  REQUIRE(exercise("addCustom", "dictionaryPath", noSeed, noDialogSecret));
  REQUIRE(sessionPreserved());
  REQUIRE(exercise(
      "replaceDictionary", "dictionaryPath",
      [](QDialog *dialog) {
        dialog->findChild<QCheckBox *>("replacementAck")->setChecked(true);
      }, [](QDialog *dialog) {
        return !dialog->findChild<QCheckBox *>("replacementAck")->isChecked();
      }));
  REQUIRE(sessionPreserved());
  scheduleDialog([](QDialog *dialog) {
    if (auto box = qobject_cast<QMessageBox *>(dialog))
      box->button(QMessageBox::Discard)->click();
  });
  find<QPushButton>(w, "closeVault")->click();
  return 0;
}
int oversizedUnicodeKeepsDirtySession() {
  Window w;
  w.show();
  QTest::qWait(100);
  find<QPushButton>(w, "warningAccept")->click();
  QTemporaryDir dir;
  REQUIRE(dir.isValid());
  const auto vaultPath = dir.filePath("unicode-synthetic.tessaveil-alpha");
  createVault(w, vaultPath, "synthetic-master-password");
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
int oversizedDialogFieldFamiliesFailClosed() {
  const QString oversized(2049, QChar(0x044f));
  REQUIRE(oversized.toUtf8().size() == 4098);
  QTemporaryDir dir;
  REQUIRE(dir.isValid());
  const QString vault = dir.filePath("bounded-fields.tessaveil-alpha");
  const QString backup = dir.filePath("bounded-fields-backup.tessaveil-alpha");
  const QString dictionary = dir.filePath("bounded-dictionary.txt");
  QFile dictionaryFile(dictionary);
  REQUIRE(dictionaryFile.open(QIODevice::WriteOnly));
  for (int index = 0; index < 40; ++index)
    REQUIRE(dictionaryFile.write(
                QString("bounded%1\n").arg(index, 3, 10, QChar('0')).toUtf8()) >
            0);
  dictionaryFile.close();

  Window w;
  w.show();
  QTest::qWait(100);
  find<QPushButton>(w, "warningAccept")->click();
  auto state = find<QLabel>(w, "state");
  auto message = find<QLabel>(w, "message");
  auto table = find<QTableView>(w, "table");
  auto sheets = find<QComboBox>(w, "sheets");

  auto createAttempt = [&](const QString &target,
                           std::function<void(QDialog *, DialogProbe &)> set) {
    auto probe = attemptDialog(w, "create", [&](QDialog *dialog,
                                                 DialogProbe &attempt) {
      dialog->findChild<QLineEdit *>("createPath")->setText(target);
      dialog->findChild<QLineEdit *>("createVaultName")
          ->setText("Bounded synthetic vault");
      watchSecret(dialog->findChild<QLineEdit *>("createMaster"),
                  "synthetic-master-password", attempt);
      watchSecret(dialog->findChild<QLineEdit *>("createConfirmation"),
                  "synthetic-master-password", attempt);
      set(dialog, attempt);
    });
    REQUIRE(probe.configured && probe.allSecretsCleared());
    REQUIRE(state->text() == "Closed");
    REQUIRE(message->text().contains("4096"));
    REQUIRE(!QFileInfo::exists(target));
    return 0;
  };
  REQUIRE(createAttempt(dir.filePath("oversized-create-path.tessaveil-alpha"),
                        [&](QDialog *dialog, DialogProbe &) {
                          dialog->findChild<QLineEdit *>("createPath")
                              ->setText(oversized);
                        }) == 0);
  REQUIRE(createAttempt(dir.filePath("oversized-vault-name.tessaveil-alpha"),
                        [&](QDialog *dialog, DialogProbe &) {
                          dialog->findChild<QLineEdit *>("createVaultName")
                              ->setText(oversized);
                        }) == 0);
  REQUIRE(createAttempt(dir.filePath("oversized-create-secret.tessaveil-alpha"),
                        [&](QDialog *dialog, DialogProbe &probe) {
                          auto master =
                              dialog->findChild<QLineEdit *>("createMaster");
                          auto confirmation = dialog->findChild<QLineEdit *>(
                              "createConfirmation");
                          master->disconnect();
                          confirmation->disconnect();
                          probe.watchedSecrets = 0;
                          probe.clearedSecrets.clear();
                          watchSecret(master, oversized, probe);
                          watchSecret(confirmation, oversized, probe);
                        }) == 0);

  createVault(w, vault, "synthetic-master-password");
  REQUIRE(state->text() == "Open / saved");
  find<QPushButton>(w, "closeVault")->click();
  auto openAttempt = [&](std::function<void(QDialog *, DialogProbe &)> set) {
    auto probe = attemptDialog(w, "open", [&](QDialog *dialog,
                                               DialogProbe &attempt) {
      dialog->findChild<QLineEdit *>("openPath")->setText(vault);
      watchSecret(dialog->findChild<QLineEdit *>("openMaster"),
                  "synthetic-master-password", attempt);
      set(dialog, attempt);
    });
    REQUIRE(probe.configured && probe.allSecretsCleared());
    REQUIRE(state->text() == "Closed");
    REQUIRE(message->text().contains("4096"));
    return 0;
  };
  REQUIRE(openAttempt([&](QDialog *dialog, DialogProbe &) {
            dialog->findChild<QLineEdit *>("openPath")->setText(oversized);
          }) == 0);
  REQUIRE(openAttempt([&](QDialog *dialog, DialogProbe &probe) {
            auto password = dialog->findChild<QLineEdit *>("openMaster");
            password->disconnect();
            probe.watchedSecrets = 0;
            probe.clearedSecrets.clear();
            watchSecret(password, oversized, probe);
          }) == 0);
  openVault(w, vault, "synthetic-master-password");
  REQUIRE(state->text() == "Open / saved");

  auto assertOpenPreserved = [&](int sheetCount, const QByteArray &digest) {
    if (state->text() != "Open / saved" || sheets->count() != sheetCount ||
        tableDigest(table) != digest || !message->text().contains("4096"))
      return false;
    return true;
  };
  const int emptySheetCount = sheets->count();
  const QByteArray emptyDigest = tableDigest(table);
  find<QLineEdit>(w, "sheetName")->setText(oversized);
  find<QPushButton>(w, "add")->click();
  REQUIRE(assertOpenPreserved(emptySheetCount, emptyDigest));
  find<QLineEdit>(w, "sheetName")->setText("Bounded standard sheet");
  find<QPushButton>(w, "add")->click();
  find<QPushButton>(w, "save")->click();
  find<QLineEdit>(w, "sheetPassword")->setText("synthetic-master-password");
  find<QPushButton>(w, "unlockMaster")->click();
  const int sheetCount = sheets->count();
  const QByteArray digest = tableDigest(table);
  REQUIRE(sheetCount == 1 && state->text() == "Open / saved");
  REQUIRE(find<QPushButton>(w, "replaceDictionary")->isEnabled());

  auto openDialogAttempt =
      [&](const char *buttonName,
          std::function<void(QDialog *, DialogProbe &)> configure) {
        auto probe = attemptDialog(w, buttonName, std::move(configure));
        REQUIRE(probe.configured && probe.allSecretsCleared());
        REQUIRE(assertOpenPreserved(sheetCount, digest));
        return 0;
      };
  REQUIRE(openDialogAttempt("addCustom", [&](QDialog *dialog, DialogProbe &) {
            dialog->findChild<QLineEdit *>("customName")->setText(oversized);
            dialog->findChild<QLineEdit *>("dictionaryPath")
                ->setText(dictionary);
          }) == 0);
  REQUIRE(find<QPushButton>(w, "replaceDictionary")->isEnabled());
  REQUIRE(openDialogAttempt("addCustom", [&](QDialog *dialog, DialogProbe &) {
            dialog->findChild<QLineEdit *>("customName")
                ->setText("Bounded custom");
            dialog->findChild<QLineEdit *>("dictionaryPath")
                ->setText(oversized);
          }) == 0);
  REQUIRE(find<QPushButton>(w, "replaceDictionary")->isEnabled());
  REQUIRE(openDialogAttempt(
              "replaceDictionary", [&](QDialog *dialog, DialogProbe &) {
                dialog->findChild<QLineEdit *>("replacementName")
                    ->setText(oversized);
                dialog->findChild<QLineEdit *>("dictionaryPath")
                    ->setText(dictionary);
                dialog->findChild<QCheckBox *>("replacementAck")
                    ->setChecked(true);
              }) == 0);
  REQUIRE(openDialogAttempt(
              "replaceDictionary", [&](QDialog *dialog, DialogProbe &) {
                dialog->findChild<QLineEdit *>("replacementName")
                    ->setText("Bounded replacement");
                dialog->findChild<QLineEdit *>("dictionaryPath")
                    ->setText(oversized);
                dialog->findChild<QCheckBox *>("replacementAck")
                    ->setChecked(true);
              }) == 0);
  REQUIRE(openDialogAttempt("renameSheet", [&](QDialog *dialog, DialogProbe &) {
            dialog->findChild<QLineEdit *>("renameName")->setText(oversized);
          }) == 0);
  REQUIRE(sheets->currentText() == "Bounded standard sheet");
  REQUIRE(openDialogAttempt("deleteSheet", [&](QDialog *dialog, DialogProbe &) {
            dialog->findChild<QLineEdit *>("deleteExactName")
                ->setText(oversized);
            dialog->findChild<QCheckBox *>("deleteFinal")->setChecked(true);
          }) == 0);
  REQUIRE(openDialogAttempt("backup", [&](QDialog *dialog, DialogProbe &) {
            dialog->findChild<QLineEdit *>("backupPath")->setText(oversized);
          }) == 0);

  auto rotateAttempt = [&](bool oversizedCurrent) {
    return openDialogAttempt(
        "changePassword", [&](QDialog *dialog, DialogProbe &probe) {
          const QString currentValue =
              oversizedCurrent ? oversized : "synthetic-master-password";
          const QString replacementValue =
              oversizedCurrent ? "synthetic-new-password" : oversized;
          watchSecret(dialog->findChild<QLineEdit *>("currentMaster"),
                      currentValue, probe);
          watchSecret(dialog->findChild<QLineEdit *>("newMaster"),
                      replacementValue, probe);
          watchSecret(dialog->findChild<QLineEdit *>("confirmNewMaster"),
                      replacementValue, probe);
        });
  };
  REQUIRE(rotateAttempt(true) == 0);
  REQUIRE(rotateAttempt(false) == 0);

  auto validBackup = attemptDialog(
      w, "backup", [&](QDialog *dialog, DialogProbe &) {
        dialog->findChild<QLineEdit *>("backupPath")->setText(backup);
      });
  REQUIRE(validBackup.configured && QFileInfo::exists(backup));
  REQUIRE(state->text() == "Open / saved");
  find<QPushButton>(w, "closeVault")->click();

  auto restoreAttempt = [&](std::function<void(QDialog *, DialogProbe &)> set,
                            const QString &destination) {
    auto probe = attemptDialog(w, "restore", [&](QDialog *dialog,
                                                  DialogProbe &attempt) {
      dialog->findChild<QLineEdit *>("restoreSource")->setText(backup);
      dialog->findChild<QLineEdit *>("restoreDestination")
          ->setText(destination);
      watchSecret(dialog->findChild<QLineEdit *>("restorePassword"),
                  "synthetic-master-password", attempt);
      set(dialog, attempt);
    });
    REQUIRE(probe.configured && probe.allSecretsCleared());
    REQUIRE(state->text() == "Closed");
    REQUIRE(message->text().contains("4096"));
    REQUIRE(!QFileInfo::exists(destination));
    return 0;
  };
  REQUIRE(restoreAttempt(
              [&](QDialog *dialog, DialogProbe &) {
                dialog->findChild<QLineEdit *>("restoreSource")
                    ->setText(oversized);
              },
              dir.filePath("oversized-restore-source.tessaveil-alpha")) == 0);
  REQUIRE(restoreAttempt(
              [&](QDialog *dialog, DialogProbe &) {
                dialog->findChild<QLineEdit *>("restoreDestination")
                    ->setText(oversized);
              },
              dir.filePath("oversized-restore-destination.tessaveil-alpha")) ==
          0);
  REQUIRE(restoreAttempt(
              [&](QDialog *dialog, DialogProbe &probe) {
                auto password =
                    dialog->findChild<QLineEdit *>("restorePassword");
                password->disconnect();
                probe.watchedSecrets = 0;
                probe.clearedSecrets.clear();
                watchSecret(password, oversized, probe);
              },
              dir.filePath("oversized-restore-password.tessaveil-alpha")) == 0);
  openVault(w, vault, "synthetic-master-password");
  REQUIRE(state->text() == "Open / saved");
  REQUIRE(sheets->count() == sheetCount);
  REQUIRE(tableDigest(table) == digest);
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
  createVault(w, vaultPath, "synthetic-master-password");
  auto add = find<QPushButton>(w, "add");
  auto columns = find<QComboBox>(w, "columns");
  columns->setCurrentIndex(0);
  add->click();
  auto table = find<QTableView>(w, "table");
  REQUIRE(table->model()->columnCount() == 10);
  auto verifyConsent = find<QCheckBox>(w, "verificationConsent");
  auto sheetState = find<QLabel>(w, "sheetState");
  verifyConsent->setChecked(true);
  find<QPushButton>(w, "verify")->click();
  REQUIRE(sheetState->text().contains("Verified by me"));
  find<QPushButton>(w, "verify")->click();
  REQUIRE(!sheetState->text().contains("Verified by me"));
  verifyConsent->setChecked(true);
  find<QPushButton>(w, "verify")->click();
  find<QLineEdit>(w, "sheetPassword")->setText("synthetic-sheet-password");
  find<QPushButton>(w, "setSheetPassword")->click();
  find<QPushButton>(w, "protect")->click();
  const auto firstDigest = tableDigest(table);
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
int structuredProfilesExposeExactModeAndAllowedLengths() {
  Window w({}, {}, [](quintptr mainWindow) { return mainWindow; });
  w.show();
  QTest::qWait(100);
  find<QPushButton>(w, "warningAccept")->click();
  auto profiles = find<QComboBox>(w, "profiles");
  auto lengths = find<QComboBox>(w, "lengths");
  auto details = find<QLabel>(w, "profileDetails");
  auto profileFilter = find<QLineEdit>(w, "profileFilter");
  auto add = find<QPushButton>(w, "add");
  REQUIRE(profiles && lengths && details && profileFilter && add);
  QTemporaryDir dir;
  REQUIRE(dir.isValid());
  createVault(w, dir.filePath("profiles-synthetic.tessaveil-alpha"),
              "synthetic-master-password");
  REQUIRE(find<QLabel>(w, "state")->text().startsWith("Open"));
  REQUIRE(profiles->count() == 733);
  profileFilter->setFocus();
  QTest::keyClicks(profileFilter, "tonkeeper-multichain");
  REQUIRE(QApplication::focusWidget() == profileFilter);
  REQUIRE(profiles->count() == 1);
  REQUIRE(profiles->currentData().toInt() >= 0);
  REQUIRE(!profiles->currentData(Qt::UserRole + 1).toBool());
  REQUIRE(details->text().contains("Keeper / Tonkeeper Multichain"));
  REQUIRE(details->text().contains("cross-platform"));
  REQUIRE(details->text().contains("documented"));
  REQUIRE(details->text().contains("bip39-multichain-generated"));
  REQUIRE(details->text().contains(
      "documentation-snapshot-2026-09-29-version-unresolved"));
  REQUIRE(details->text().contains("original wallet"));
  auto accessible = QAccessible::queryAccessibleInterface(details);
  REQUIRE(accessible);
  REQUIRE(accessible->text(QAccessible::Name) == details->text());
  REQUIRE(accessible->text(QAccessible::Description) == details->text());
  QEvent activateWindow(QEvent::WindowActivate);
  QApplication::sendEvent(&w, &activateWindow);
  Q_EMIT qApp->applicationStateChanged(Qt::ApplicationActive);
  QCoreApplication::processEvents();
  REQUIRE(profiles->isVisible());
  profileFilter->setFocus();
  QTest::keyClick(profileFilter, Qt::Key_Tab);
  REQUIRE(QApplication::focusWidget() == profiles);
  const int unavailableProfile = profiles->currentData().toInt();
  auto locale = find<QComboBox>(w, "locale");
  REQUIRE(locale);
  locale->setCurrentIndex(locale->findData("ru"));
  REQUIRE(profiles->currentData().toInt() == unavailableProfile);
  REQUIRE(details->text().contains(
      QString::fromUtf8("Создание профиля в Tessaveil недоступно")));
  REQUIRE(details->text().contains(
      QString::fromUtf8("резервного копирования/экспорта")));
  REQUIRE(accessible->text(QAccessible::Name) == details->text());
  REQUIRE(accessible->text(QAccessible::Description) == details->text());
  locale->setCurrentIndex(locale->findData("en"));
  REQUIRE(profiles->currentData().toInt() == unavailableProfile);
  REQUIRE(details->text().contains("Creation in Tessaveil is unavailable"));
  REQUIRE(details->text().contains("original wallet's own backup/export"));
  REQUIRE(accessible->text(QAccessible::Name) == details->text());
  REQUIRE(accessible->text(QAccessible::Description) == details->text());
  profileFilter->clear();
  REQUIRE(profiles->count() == 733);
  profiles->setCurrentIndex(0); // Atomic Wallet documented profile.
  REQUIRE(details->text().contains("windows"));
  REQUIRE(details->text().contains("documented"));
  REQUIRE(details->text().contains(
      "version-unresolved-doc-2026-09-29-cd66b03392fb"));
  REQUIRE(details->text().contains("mnemonic-generated"));
  REQUIRE(!details->text().contains("wallet-status:"));
  REQUIRE(details->text().contains("original wallet"));
  REQUIRE(accessible->text(QAccessible::Name) == details->text());
  REQUIRE(accessible->text(QAccessible::Description) == details->text());
  const QString unknownReason =
      uiProfileReason("en", "unrecognized:internal-code");
  REQUIRE(unknownReason.contains("original wallet"));
  REQUIRE(!unknownReason.contains("unrecognized"));
  const QString unknownReasonRu =
      uiProfileReason("ru", "unrecognized:internal-code");
  REQUIRE(unknownReasonRu.contains(QString::fromUtf8("исходном кошельке")));
  REQUIRE(!unknownReasonRu.contains("unrecognized"));
  const QString documentedEnglish =
      uiProfileReason("en", "wallet-status:documented");
  REQUIRE(documentedEnglish.contains("Evidence exists"));
  REQUIRE(documentedEnglish.contains(
      "insufficient to support Tessaveil sheet creation for this exact "
      "product, platform, version and mode"));
  REQUIRE(documentedEnglish.contains("Creation remains unavailable"));
  REQUIRE(documentedEnglish.contains(
      "original wallet's own backup/export workflow"));
  REQUIRE(!documentedEnglish.contains("version is unresolved"));
  const QString documentedRussian =
      uiProfileReason("ru", "wallet-status:documented");
  REQUIRE(documentedRussian.contains(
      QString::fromUtf8("Подтверждающие сведения существуют")));
  REQUIRE(documentedRussian.contains(
      QString::fromUtf8("недостаточно для создания листа Tessaveil для этого "
                        "точного сочетания продукта, платформы, версии и режима")));
  REQUIRE(documentedRussian.contains(
      QString::fromUtf8("Создание остаётся недоступным")));
  REQUIRE(documentedRussian.contains(
      QString::fromUtf8("собственный процесс резервного копирования/экспорта "
                        "исходного кошелька")));
  REQUIRE(!documentedRussian.contains(
      QString::fromUtf8("точная поддерживаемая версия")));
  for (const auto &reason : {"wallet-status:documented",
                             "wallet-status:blocked",
                             "wallet-status:no-mnemonic-confirmed"}) {
    const QString english = uiProfileReason("en", reason);
    REQUIRE(english.contains("Creation in Tessaveil is unavailable"));
    REQUIRE(english.contains("original wallet's own backup/export"));
    const QString russian = uiProfileReason("ru", reason);
    REQUIRE(russian.contains(
        QString::fromUtf8("Создание профиля в Tessaveil недоступно")));
    REQUIRE(russian.contains(
        QString::fromUtf8("резервного копирования/экспорта")));
  }
  REQUIRE(!add->isEnabled());
  REQUIRE(lengths->count() == 0);
  int selectable = 0;
  for (int index = 0; index < profiles->count(); ++index) {
    REQUIRE(profiles->model()->flags(profiles->model()->index(index, 0)) &
            Qt::ItemIsEnabled);
    profiles->setCurrentIndex(index);
    if (add->isEnabled()) {
      ++selectable;
      REQUIRE(lengths->count() == 1);
      REQUIRE(lengths->currentData().toInt() == 24);
    }
  }
  REQUIRE(selectable == 3);
  find<QPushButton>(w, "save")->click();
  find<QPushButton>(w, "closeVault")->click();
  return 0;
}
int closedLocaleLocalizesDialogsAndPersistsOnCreate() {
  Window w;
  w.show();
  QTest::qWait(100);
  find<QPushButton>(w, "warningAccept")->click();
  QTemporaryDir dir;
  REQUIRE(dir.isValid());
  const QString vault = dir.filePath("pre-vault-locale.tessaveil-alpha");
  auto localeChoice = find<QComboBox>(w, "locale");
  REQUIRE(localeChoice && find<QLabel>(w, "state")->text() == "Closed");

  localeChoice->setCurrentIndex(localeChoice->findData("ru"));
  REQUIRE(find<QLabel>(w, "state")->text() == QString::fromUtf8("Закрыто"));
  REQUIRE(find<QPushButton>(w, "create")->text().contains(
      QString::fromUtf8("Создать хранилище")));
  bool createDialogRussian = false;
  scheduleDialog([&](QDialog *dialog) {
    auto buttons = dialog->findChild<QDialogButtonBox *>();
    auto guidance = dialog->findChild<QLabel *>("createPasswordGuidance");
    createDialogRussian =
        dialog->windowTitle().contains(QString::fromUtf8("Создать хранилище")) &&
        buttons && buttons->button(QDialogButtonBox::Ok)->text() ==
                       QString::fromUtf8("Продолжить") &&
        guidance && guidance->text().contains(
                        QString::fromUtf8("не менее 15 символов Unicode")) &&
        guidance->accessibleName() == guidance->text();
    dialog->findChild<QLineEdit *>("createPath")->setText(vault);
    dialog->findChild<QLineEdit *>("createMaster")
        ->setText("synthetic-master-password");
    dialog->findChild<QLineEdit *>("createConfirmation")
        ->setText("synthetic-master-password");
    dialog->accept();
  });
  find<QPushButton>(w, "create")->click();
  REQUIRE(createDialogRussian);
  REQUIRE(localeChoice->currentData().toString() == "ru");
  REQUIRE(find<QLabel>(w, "state")->text().contains(QString::fromUtf8("Открыто")));
  find<QPushButton>(w, "add")->click();
  find<QPushButton>(w, "save")->click();
  const bool createdVaultSaved =
      find<QLabel>(w, "state")->text() == QString::fromUtf8("Открыто / сохранено");
  find<QPushButton>(w, "closeVault")->click();
  REQUIRE(createdVaultSaved);

  localeChoice->setCurrentIndex(localeChoice->findData("en"));
  REQUIRE(find<QLabel>(w, "state")->text() == "Closed");
  bool openDialogEnglish = false;
  scheduleDialog([&](QDialog *dialog) {
    auto buttons = dialog->findChild<QDialogButtonBox *>();
    openDialogEnglish = dialog->windowTitle().contains("Open vault") &&
                        buttons &&
                        buttons->button(QDialogButtonBox::Ok)->text() ==
                            "Continue";
    dialog->findChild<QLineEdit *>("openPath")->setText(vault);
    dialog->findChild<QLineEdit *>("openMaster")
        ->setText("synthetic-master-password");
    dialog->accept();
  });
  find<QPushButton>(w, "open")->click();
  REQUIRE(openDialogEnglish);
  const bool restoredRussian = localeChoice->currentData().toString() == "ru";
  const bool openedRussian =
      find<QLabel>(w, "state")->text().contains(QString::fromUtf8("Открыто"));
  find<QPushButton>(w, "closeVault")->click();
  REQUIRE(restoredRussian);
  REQUIRE(openedRussian);
  bool restoreGuidanceRussian = false;
  scheduleDialog([&](QDialog *dialog) {
    auto guidance =
        dialog->findChild<QLabel *>("restorePasswordGuidance");
    restoreGuidanceRussian =
        guidance && guidance->text().contains(
                        QString::fromUtf8("исходный/старый мастер-пароль")) &&
        guidance->text().contains(QString::fromUtf8("резервной копии"));
    dialog->reject();
  });
  find<QPushButton>(w, "restore")->click();
  REQUIRE(restoreGuidanceRussian);
  return 0;
}
int localeAndThemeSwitchWithoutReplacingSession() {
  Window w;
  w.show();
  QTest::qWait(100);
  find<QPushButton>(w, "warningAccept")->click();
  QTemporaryDir dir;
  REQUIRE(dir.isValid());
  const QString vault = dir.filePath("locale-synthetic.tessaveil-alpha");
  createVault(w, vault, "synthetic-master-password");
  find<QPushButton>(w, "add")->click();
  const int sheets = find<QComboBox>(w, "sheets")->count();
  auto locale = find<QComboBox>(w, "locale");
  auto theme = find<QComboBox>(w, "theme");
  REQUIRE(locale && theme);
  REQUIRE(locale->findData("ru") >= 0);
  locale->setCurrentIndex(locale->findData("ru"));
  REQUIRE(find<QLabel>(w, "state")->text().contains(QString::fromUtf8("Открыто")));
  REQUIRE(find<QComboBox>(w, "sheets")->count() == sheets);
  REQUIRE(find<QLabel>(w, "state")->accessibleName().contains(
      QString::fromUtf8("Состояние")));
  theme->setCurrentIndex(theme->findData("light"));
  REQUIRE(w.property("tessaveilTheme").toString() == "light");
  REQUIRE(find<QComboBox>(w, "sheets")->count() == sheets);
  theme->setCurrentIndex(theme->findData("dark"));
  REQUIRE(w.property("tessaveilTheme").toString() == "dark");
  find<QPushButton>(w, "save")->click();
  find<QPushButton>(w, "closeVault")->click();
  openVault(w, vault, "synthetic-master-password");
  REQUIRE(locale->currentData().toString() == "ru");
  REQUIRE(find<QLabel>(w, "state")->text().contains(QString::fromUtf8("Открыто")));
  find<QPushButton>(w, "lock")->click();
  find<QLineEdit>(w, "master")->setText("synthetic-wrong-password");
  find<QPushButton>(w, "unlock")->click();
  REQUIRE(find<QLabel>(w, "message")->text() ==
          QString::fromUtf8("Пароль неверен или хранилище повреждено."));
  find<QPushButton>(w, "closeVault")->click();
  return 0;
}
int candidateWorkflowControlsArePresentAndBounded() {
  Window w;
  w.show();
  QTest::qWait(100);
  find<QPushButton>(w, "warningAccept")->click();
  auto createButton = find<QPushButton>(w, "create");
  auto openButton = find<QPushButton>(w, "open");
  auto addCustom = find<QPushButton>(w, "addCustom");
  auto replace = find<QPushButton>(w, "replaceDictionary");
  auto rename = find<QPushButton>(w, "renameSheet");
  auto remove = find<QPushButton>(w, "deleteSheet");
  auto backup = find<QPushButton>(w, "backup");
  auto restore = find<QPushButton>(w, "restore");
  auto rotate = find<QPushButton>(w, "changePassword");
  REQUIRE(createButton && openButton && addCustom && replace && rename &&
          remove && backup && restore && rotate);
  REQUIRE(find<QLineEdit>(w, "path")->isReadOnly());
  bool focusedCreate = false;
  scheduleDialog([&](QDialog *dialog) {
    auto createPath = dialog->findChild<QLineEdit *>("createPath");
    auto vaultName = dialog->findChild<QLineEdit *>("createVaultName");
    auto password = dialog->findChild<QLineEdit *>("createMaster");
    auto confirmation =
        dialog->findChild<QLineEdit *>("createConfirmation");
    auto guidance = dialog->findChild<QLabel *>("createPasswordGuidance");
    focusedCreate = dialog->objectName() == "createVaultDialog" &&
                    createPath && createPath->isReadOnly() && vaultName &&
                    password && confirmation && guidance &&
                    guidance->text().contains("at least 15 Unicode characters") &&
                    guidance->accessibleName() == guidance->text() &&
                    password->echoMode() == QLineEdit::Password &&
                    confirmation->echoMode() == QLineEdit::Password &&
                    !confirmation->acceptDrops() &&
                    confirmation->maxLength() == 4096;
    dialog->reject();
  });
  createButton->click();
  QCoreApplication::processEvents();
  REQUIRE(focusedCreate);
  bool focusedOpen = false;
  scheduleDialog([&](QDialog *dialog) {
    focusedOpen = dialog->objectName() == "openVaultDialog" &&
                   dialog->findChild<QLineEdit *>("openPath") &&
                   dialog->findChild<QLineEdit *>("openMaster");
    dialog->reject();
  });
  openButton->click();
  QCoreApplication::processEvents();
  REQUIRE(focusedOpen);
  return 0;
}
int recoveryAndSheetDialogsUseRealControllerFlows() {
  QTemporaryDir dir;
  REQUIRE(dir.isValid());
  const QString source = dir.filePath("workflow-source.tessaveil-alpha");
  const QString backup = dir.filePath("workflow-backup.tessaveil-alpha");
  const QString restored = dir.filePath("workflow-restored.tessaveil-alpha");
  const QString dictionary = dir.filePath("synthetic-dictionary.txt");
  const QString revised = dir.filePath("synthetic-dictionary-revised.txt");
  for (const auto &entry : {std::pair{dictionary, "syntheticword"},
                            std::pair{revised, "revisedword"}}) {
    QFile file(entry.first);
    REQUIRE(file.open(QIODevice::WriteOnly));
    for (int index = 0; index < 40; ++index)
      REQUIRE(file.write(
                  QString("%1%2\n").arg(entry.second).arg(index, 3, 10, QChar('0'))
                      .toUtf8()) > 0);
    file.close();
  }
  Window w;
  w.show();
  QTest::qWait(100);
  find<QPushButton>(w, "warningAccept")->click();
  createVault(w, source, "synthetic-master-password");
  find<QPushButton>(w, "add")->click();
  find<QPushButton>(w, "save")->click();
  REQUIRE(find<QLabel>(w, "state")->text() == "Open / saved");

  bool backupConfigured = false;
  bool rotationSecretsProtected = false;
  bool rotationCopyWarningPresent = false;
  bool restoreOldPasswordGuidancePresent = false;
  scheduleDialog([&](QDialog *dialog) {
    auto value = dialog->findChild<QLineEdit *>("backupPath");
    if (!value)
      return;
    value->setText(QString(2049, QChar(0x044f)));
    backupConfigured = true;
    dialog->accept();
  });
  find<QPushButton>(w, "backup")->click();
  REQUIRE(backupConfigured);
  REQUIRE(find<QLabel>(w, "state")->text() == "Open / saved");
  REQUIRE(find<QLabel>(w, "message")->text().contains("4096"));
  REQUIRE(!QFileInfo::exists(backup));

  scheduleDialog([&](QDialog *dialog) {
    dialog->findChild<QLineEdit *>("backupPath")->setText(backup);
    dialog->accept();
  });
  find<QPushButton>(w, "backup")->click();
  REQUIRE(QFileInfo::exists(backup));
  QFile sourceFile(source), backupFile(backup);
  REQUIRE(sourceFile.open(QIODevice::ReadOnly));
  REQUIRE(backupFile.open(QIODevice::ReadOnly));
  REQUIRE(sourceFile.readAll() == backupFile.readAll());
  sourceFile.close();
  backupFile.close();

  const int initialSheetCount = find<QComboBox>(w, "sheets")->count();
  pendingContext(w);
  scheduleDialog([](QDialog *dialog) { dialog->reject(); });
  find<QPushButton>(w, "addCustom")->click();
  REQUIRE(contextIsClear(w));
  REQUIRE(find<QComboBox>(w, "sheets")->count() == initialSheetCount);

  pendingContext(w);
  scheduleDialog([&](QDialog *dialog) {
    dialog->findChild<QLineEdit *>("customName")->setText("Synthetic custom");
    dialog->findChild<QLineEdit *>("dictionaryPath")->setText(dictionary);
    dialog->findChild<QComboBox *>("customRows")->setCurrentIndex(
        dialog->findChild<QComboBox *>("customRows")->findData(12));
    dialog->findChild<QComboBox *>("customColumns")->setCurrentIndex(
        dialog->findChild<QComboBox *>("customColumns")->findData(10));
    dialog->accept();
  });
  find<QPushButton>(w, "addCustom")->click();
  REQUIRE(contextIsClear(w));
  REQUIRE(find<QComboBox>(w, "sheets")->count() == 2);
  REQUIRE(find<QTableView>(w, "table")->model()->rowCount() == 12);
  REQUIRE(find<QTableView>(w, "table")->model()->columnCount() == 10);
  REQUIRE(!find<QLabel>(w, "sheetState")->text().contains("Verified by me"));

  pendingContext(w);
  scheduleDialog([&](QDialog *dialog) {
    dialog->findChild<QLineEdit *>("replacementName")
        ->setText("Must not replace");
    dialog->findChild<QLineEdit *>("dictionaryPath")->setText(revised);
    dialog->accept();
  });
  find<QPushButton>(w, "replaceDictionary")->click();
  REQUIRE(contextIsClear(w));
  REQUIRE(find<QComboBox>(w, "sheets")->count() == 2);
  REQUIRE(find<QComboBox>(w, "sheets")->currentText() == "Synthetic custom");

  pendingContext(w);
  scheduleDialog([&](QDialog *dialog) {
    dialog->findChild<QLineEdit *>("replacementName")
        ->setText("Synthetic replacement");
    dialog->findChild<QLineEdit *>("dictionaryPath")->setText(revised);
    dialog->findChild<QCheckBox *>("replacementAck")->setChecked(true);
    dialog->accept();
  });
  find<QPushButton>(w, "replaceDictionary")->click();
  REQUIRE(contextIsClear(w));
  REQUIRE(find<QComboBox>(w, "sheets")->count() == 3);
  REQUIRE(find<QComboBox>(w, "sheets")->currentText() ==
          "Synthetic replacement");
  REQUIRE(!find<QLabel>(w, "sheetState")->text().contains("Verified by me"));

  scheduleDialog([&](QDialog *dialog) {
    dialog->findChild<QLineEdit *>("renameName")->setText("Renamed replacement");
    dialog->accept();
  });
  find<QPushButton>(w, "renameSheet")->click();
  REQUIRE(find<QComboBox>(w, "sheets")->currentText() == "Renamed replacement");
  pendingContext(w);
  scheduleDialog([&](QDialog *dialog) {
    dialog->findChild<QLineEdit *>("deleteExactName")->setText("Wrong name");
    dialog->findChild<QCheckBox *>("deleteFinal")->setChecked(true);
    dialog->accept();
  });
  find<QPushButton>(w, "deleteSheet")->click();
  REQUIRE(contextIsClear(w));
  REQUIRE(find<QComboBox>(w, "sheets")->count() == 3);
  REQUIRE(find<QComboBox>(w, "sheets")->currentText() ==
          "Renamed replacement");
  pendingContext(w);
  scheduleDialog([&](QDialog *dialog) {
    dialog->findChild<QLineEdit *>("deleteExactName")
        ->setText("Renamed replacement");
    dialog->findChild<QCheckBox *>("deleteFinal")->setChecked(true);
    dialog->accept();
  });
  find<QPushButton>(w, "deleteSheet")->click();
  REQUIRE(contextIsClear(w));
  REQUIRE(find<QComboBox>(w, "sheets")->count() == 2);

  scheduleDialog([&](QDialog *dialog) {
    auto current = dialog->findChild<QLineEdit *>("currentMaster");
    auto replacement = dialog->findChild<QLineEdit *>("newMaster");
    auto confirmation = dialog->findChild<QLineEdit *>("confirmNewMaster");
    auto warning = dialog->findChild<QLabel *>("rotationWarning");
    rotationCopyWarningPresent =
        warning && warning->text().contains("does not revoke old backups") &&
        warning->text().contains("old passwords");
    rotationSecretsProtected =
        current && replacement && confirmation &&
        current->echoMode() == QLineEdit::Password &&
        replacement->echoMode() == QLineEdit::Password &&
        confirmation->echoMode() == QLineEdit::Password;
    if (!rotationSecretsProtected)
      return;
    current->setText("synthetic-master-password");
    replacement->setText("synthetic-rotated-password");
    confirmation->setText("synthetic-rotated-password");
    dialog->accept();
  });
  find<QPushButton>(w, "changePassword")->click();
  REQUIRE(rotationSecretsProtected);
  REQUIRE(rotationCopyWarningPresent);
  REQUIRE(find<QLabel>(w, "state")->text() == "Open / saved");
  find<QPushButton>(w, "closeVault")->click();
  openVault(w, source, "synthetic-master-password");
  REQUIRE(find<QLabel>(w, "state")->text() == "Closed");
  openVault(w, source, "synthetic-rotated-password");
  REQUIRE(find<QLabel>(w, "state")->text() == "Open / saved");
  find<QPushButton>(w, "closeVault")->click();

  scheduleDialog([&](QDialog *dialog) {
    auto guidance =
        dialog->findChild<QLabel *>("restorePasswordGuidance");
    restoreOldPasswordGuidancePresent =
        guidance && guidance->text().contains("original/old master password") &&
        guidance->text().contains("selected backup");
    dialog->findChild<QLineEdit *>("restoreSource")->setText(backup);
    dialog->findChild<QLineEdit *>("restoreDestination")->setText(restored);
    dialog->findChild<QLineEdit *>("restorePassword")
        ->setText("synthetic-master-password");
    dialog->accept();
  });
  find<QPushButton>(w, "restore")->click();
  REQUIRE(restoreOldPasswordGuidancePresent);
  REQUIRE(find<QLabel>(w, "state")->text() == "Open / saved");
  REQUIRE(find<QLineEdit>(w, "path")->text() == restored);
  REQUIRE(find<QComboBox>(w, "sheets")->count() == 1);
  find<QPushButton>(w, "closeVault")->click();
  return 0;
}
int restoreRefreshesActivityAndLocalizedProfile() {
  QTemporaryDir dir;
  REQUIRE(dir.isValid());
  const QString source = dir.filePath("restore-time-source.tessaveil-alpha");
  const QString backup = dir.filePath("restore-time-backup.tessaveil-alpha");
  const QString restored =
      dir.filePath("restore-time-destination.tessaveil-alpha");
  qint64 now = 0;
  Window w([&] { return now; });
  w.show();
  QTest::qWait(100);
  find<QPushButton>(w, "warningAccept")->click();
  createVault(w, source, "synthetic-master-password");
  find<QComboBox>(w, "locale")
      ->setCurrentIndex(find<QComboBox>(w, "locale")->findData("ru"));
  find<QPushButton>(w, "add")->click();
  find<QPushButton>(w, "save")->click();
  scheduleDialog([&](QDialog *dialog) {
    dialog->findChild<QLineEdit *>("backupPath")->setText(backup);
    dialog->accept();
  });
  find<QPushButton>(w, "backup")->click();
  REQUIRE(QFileInfo::exists(backup));
  find<QPushButton>(w, "closeVault")->click();
  find<QComboBox>(w, "locale")
      ->setCurrentIndex(find<QComboBox>(w, "locale")->findData("en"));
  auto filter = find<QLineEdit>(w, "profileFilter");
  auto details = find<QLabel>(w, "profileDetails");
  filter->setText("tonkeeper-multichain");
  REQUIRE(details->text().contains("Creation in Tessaveil"));

  now = 10 * 60000;
  scheduleDialog([&](QDialog *dialog) {
    dialog->findChild<QLineEdit *>("restoreSource")->setText(backup);
    dialog->findChild<QLineEdit *>("restoreDestination")->setText(restored);
    dialog->findChild<QLineEdit *>("restorePassword")
        ->setText("synthetic-master-password");
    dialog->accept();
  });
  find<QPushButton>(w, "restore")->click();
  auto state = find<QLabel>(w, "state");
  auto timer = find<QTimer>(w, "inactivityTimer");
  REQUIRE(state->text() == QString::fromUtf8("Открыто / сохранено"));
  REQUIRE(find<QComboBox>(w, "locale")->currentData().toString() == "ru");
  REQUIRE(details->text().contains(
      QString::fromUtf8("Создание профиля в Tessaveil недоступно")));
  auto accessible = QAccessible::queryAccessibleInterface(details);
  REQUIRE(accessible);
  REQUIRE(accessible->text(QAccessible::Name) == details->text());
  REQUIRE(accessible->text(QAccessible::Description) == details->text());
  QMetaObject::invokeMethod(timer, "timeout", Qt::DirectConnection);
  REQUIRE(state->text().startsWith(QString::fromUtf8("Открыто")));
  now += 299999;
  QMetaObject::invokeMethod(timer, "timeout", Qt::DirectConnection);
  REQUIRE(state->text().startsWith(QString::fromUtf8("Открыто")));
  now += 1;
  QMetaObject::invokeMethod(timer, "timeout", Qt::DirectConnection);
  REQUIRE(state->text().startsWith(QString::fromUtf8("Заблокировано")));
  find<QPushButton>(w, "closeVault")->click();
  return 0;
}
int windowsLockInvalidatesSensitiveDialog() {
  QTemporaryDir dir;
  REQUIRE(dir.isValid());
  Window w;
  w.show();
  QTest::qWait(100);
  find<QPushButton>(w, "warningAccept")->click();
  createVault(w, dir.filePath("dialog-lock.tessaveil-alpha"),
              "synthetic-master-password");
  find<QPushButton>(w, "add")->click();
  bool invalidated = false;
  scheduleDialog([&](QDialog *dialog) {
    auto target = dialog->findChild<QLineEdit *>("backupPath");
    if (!target)
      return;
    target->setText(dir.filePath("must-not-exist.tessaveil-alpha"));
    SendMessage(reinterpret_cast<HWND>(w.winId()), WM_WTSSESSION_CHANGE,
                WTS_SESSION_LOCK, 0);
    QCoreApplication::processEvents();
    invalidated = !dialog->isVisible();
    if (dialog->isVisible())
      dialog->reject();
  });
  find<QPushButton>(w, "backup")->click();
  REQUIRE(invalidated);
  REQUIRE(find<QLabel>(w, "state")->text().startsWith("Locked"));
  REQUIRE(find<QTableView>(w, "table")->model()->rowCount() == 0);
  REQUIRE(!QFileInfo::exists(dir.filePath("must-not-exist.tessaveil-alpha")));
  return 0;
}
int explicitDirtySaveDiscardCancel() {
  QTemporaryDir dir;
  REQUIRE(dir.isValid());
  const QString vault = dir.filePath("explicit-decisions.tessaveil-alpha");
  Window w;
  w.show();
  QTest::qWait(100);
  find<QPushButton>(w, "warningAccept")->click();
  createVault(w, vault, "synthetic-master-password");
  find<QPushButton>(w, "add")->click();
  scheduleDialog([](QDialog *dialog) {
    if (auto box = qobject_cast<QMessageBox *>(dialog))
      box->button(QMessageBox::Cancel)->click();
  });
  find<QPushButton>(w, "closeVault")->click();
  REQUIRE(find<QLabel>(w, "state")->text() == "Open / unsaved changes");
  scheduleDialog([](QDialog *dialog) {
    if (auto box = qobject_cast<QMessageBox *>(dialog))
      box->button(QMessageBox::Save)->click();
  });
  find<QPushButton>(w, "closeVault")->click();
  REQUIRE(find<QLabel>(w, "state")->text() == "Closed");
  openVault(w, vault, "synthetic-master-password");
  REQUIRE(find<QComboBox>(w, "sheets")->count() == 1);
  find<QPushButton>(w, "add")->click();
  REQUIRE(find<QComboBox>(w, "sheets")->count() == 2);
  scheduleDialog([](QDialog *dialog) {
    if (auto box = qobject_cast<QMessageBox *>(dialog))
      box->button(QMessageBox::Discard)->click();
  });
  find<QPushButton>(w, "closeVault")->click();
  REQUIRE(find<QLabel>(w, "state")->text() == "Closed");
  openVault(w, vault, "synthetic-master-password");
  REQUIRE(find<QComboBox>(w, "sheets")->count() == 1);
  find<QPushButton>(w, "closeVault")->click();
  return 0;
}
int main(int argc, char **argv) {
  QApplication app(argc, argv);
  REQUIRE(structuredProfilesExposeExactModeAndAllowedLengths() == 0);
  REQUIRE(closedLocaleLocalizesDialogsAndPersistsOnCreate() == 0);
  REQUIRE(localeAndThemeSwitchWithoutReplacingSession() == 0);
  REQUIRE(candidateWorkflowControlsArePresentAndBounded() == 0);
  REQUIRE(recoveryAndSheetDialogsUseRealControllerFlows() == 0);
  REQUIRE(restoreRefreshesActivityAndLocalizedProfile() == 0);
  REQUIRE(windowsLockInvalidatesSensitiveDialog() == 0);
  REQUIRE(explicitDirtySaveDiscardCancel() == 0);
  REQUIRE(privacyEventsScrubEveryState(app) == 0);
  REQUIRE(pickerAltTabCannotBypassPrivacy(app) == 0);
  REQUIRE(nativePickersScrubBeforeTheyBecomeUsable() == 0);
  REQUIRE(oversizedUnicodeKeepsDirtySession() == 0);
  REQUIRE(oversizedDialogFieldFamiliesFailClosed() == 0);
  REQUIRE(addingSheetScrubsPreviousContext() == 0);
  {
    Window unavailable({}, [](quintptr) { return false; });
    REQUIRE(!unavailable.centralWidget()->isEnabled());
  }
  qint64 now = 0;
  Window w([&] { return now; }, {}, [](quintptr) { return 0; });
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
  createVault(w, dir.filePath("synthetic.tessaveil-alpha"),
              "synthetic-master-password");
  REQUIRE(password->text().isEmpty());
  auto state = find<QLabel>(w, "state");
  REQUIRE(state->text().startsWith("Open"));
  auto profiles = find<QComboBox>(w, "profiles");
  REQUIRE(profiles);
  int available = 0;
  int availableProfile = -1;
  for (int i = 0; i < profiles->count(); ++i) {
    profiles->setCurrentIndex(i);
    if (find<QPushButton>(w, "add")->isEnabled()) {
      available++;
      availableProfile = i;
    }
  }
  REQUIRE(available == 3);
  REQUIRE(availableProfile >= 0);
  profiles->setCurrentIndex(availableProfile);
  auto columns = find<QComboBox>(w, "columns");
  auto add = find<QPushButton>(w, "add");
  auto table = find<QTableView>(w, "table");
  REQUIRE(columns && add && table);
  columns->setCurrentIndex(0);
  add->click();
  REQUIRE(table->model()->columnCount() == 10);
  REQUIRE(table->model()->rowCount() == 24);
  REQUIRE(table->horizontalHeader()->sectionResizeMode(0) ==
          QHeaderView::ResizeToContents);
  REQUIRE(!table->model()
               ->headerData(0, Qt::Horizontal, Qt::AccessibleTextRole)
               .toString()
               .isEmpty());
  REQUIRE(!table->model()
               ->headerData(0, Qt::Vertical, Qt::AccessibleTextRole)
               .toString()
               .isEmpty());
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
  if (table->height() < 150)
    std::fprintf(stderr,
                 "layout diagnostics: window=%dx%d table=%dx%d parent=%dx%d "
                 "path=%d state=%d message=%d\n",
                 w.width(), w.height(), table->width(), table->height(),
                 table->parentWidget()->width(), table->parentWidget()->height(),
                 path->height(), state->height(),
                 find<QLabel>(w, "message")->height());
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
  const QString activePath = dir.filePath("synthetic.tessaveil-alpha");
  const HANDLE denyReplace = CreateFileW(
      reinterpret_cast<LPCWSTR>(activePath.utf16()), GENERIC_READ,
      FILE_SHARE_READ, nullptr, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, nullptr);
  REQUIRE(denyReplace != INVALID_HANDLE_VALUE);
  find<QPushButton>(w, "save")->click();
  REQUIRE(state->text() == "Open / unsaved changes");
  REQUIRE(!find<QLabel>(w, "message")->text().isEmpty());
  CloseHandle(denyReplace);
  find<QPushButton>(w, "save")->click();
  REQUIRE(state->text() == "Open / saved");
  find<QPushButton>(w, "closeVault")->click();
  REQUIRE(state->text() == "Closed");
  openVault(w, dir.filePath("synthetic.tessaveil-alpha"),
            "synthetic-master-password");
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
  REQUIRE(find<QLabel>(w, "message")->accessibleName() == authentication);
  REQUIRE(password->text().isEmpty());
  find<QPushButton>(w, "closeVault")->click();
  const auto corruptPath = dir.filePath("corrupt-copy.tessaveil-alpha");
  REQUIRE(QFile::copy(dir.filePath("synthetic.tessaveil-alpha"), corruptPath));
  QFile damaged(corruptPath);
  REQUIRE(damaged.open(QIODevice::ReadWrite));
  REQUIRE(damaged.seek(damaged.size() - 1));
  auto byte = damaged.read(1);
  REQUIRE(byte.size() == 1);
  byte[0] = byte[0] ^ 1;
  REQUIRE(damaged.seek(damaged.size() - 1));
  REQUIRE(damaged.write(byte) == 1);
  damaged.close();
  openVault(w, corruptPath, "synthetic-master-password");
  REQUIRE(state->text() == "Closed");
  REQUIRE(find<QLabel>(w, "message")->text() == authentication);
  openVault(w, dir.filePath("synthetic.tessaveil-alpha"),
            "synthetic-master-password");
  REQUIRE(state->text() == "Open / saved");
  find<QPushButton>(w, "closeVault")->click();
  createVault(w, dir.filePath("second.tessaveil-alpha"),
              "synthetic-master-password");
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
  QCoreApplication::processEvents();
  REQUIRE(state->text() == "Open / unsaved changes");
  REQUIRE(find<QWidget>(w, "privacyCover")->isVisible());
  Q_EMIT app.applicationStateChanged(Qt::ApplicationActive);
  REQUIRE(state->text() == "Open / unsaved changes");
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
