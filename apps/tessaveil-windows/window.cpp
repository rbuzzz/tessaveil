#include "window.h"
#include "bridge.h"
#include <QtWidgets>
#include <cstring>
#include <memory>
#include <windows.h>
#include <wtsapi32.h>

namespace {
void wipe(void *p, size_t size) { SecureZeroMemory(p, size); }
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
    setAccessibleName(name == "master" ? "Master password"
                      : name == "word" ? "One word"
                      : name == "sheetPassword"
                          ? "Sheet password or master credential"
                          : "Column symbol confirmation");
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
             QString &message) {
    TvReply out{};
    int code = request(op, a, b, in, out);
    state = out;
    wipe(state.text, sizeof(state.text));
    state.text_len = 0;
    if (code)
      message = code < 0
                    ? "The session is unavailable. Close and restart the alpha."
                    : QString::fromUtf8(reinterpret_cast<char *>(out.text),
                                        out.text_len);
    else
      message.clear();
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
    if (role != Qt::DisplayRole)
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
    setAccessibleName("Current decoy table. No target cells are marked.");
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
    horizontalHeader()->setSectionResizeMode(QHeaderView::Fixed);
    verticalHeader()->setSectionResizeMode(QHeaderView::Fixed);
    verticalHeader()->setMinimumSectionSize(24);
    horizontalHeader()->setDefaultSectionSize(150);
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
  QElapsedTimer elapsed;
  qint64 lastInput = 0;
  bool updating = false, accepted = false;
  QWidget *warning;
  QWidget *workspace;
  QLineEdit *path;
  Secret *master;
  QLabel *status, *message, *sheetState;
  QComboBox *profiles, *columns, *sheets, *minutes;
  QLineEdit *sheetName;
  Secret *sheetPassword, *symbol1, *symbol2, *word;
  QSpinBox *row;
  QCheckBox *verificationConsent, *spinConsent;
  Table *table;
  TableModel *model;
  QList<QPushButton *> vaultButtons, editButtons;
  QPushButton *create, *open, *unlock, *save, *closeVault, *lock, *add,
      *protect, *unlockSheet, *unlockMaster;
  bool action(uint32_t op, uint32_t a, uint32_t b, TvInput &in,
              bool fieldsValid = true) {
    if (!fieldsValid) {
      wipe(&in, sizeof(in));
      message->setText("Input exceeds the 4096-byte UTF-8 limit. Shorten it "
                       "and try again.");
      return false;
    }
    QString text;
    int code = core.action(op, a, b, in, text);
    message->setText(text);
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
    verificationConsent->setChecked(false);
    spinConsent->setChecked(false);
  }
  void refresh() {
    updating = true;
    const auto &s = core.state;
    const bool isOpen = s.state == 2;
    status->setText(
        isOpen ? (s.dirty ? "Open / unsaved changes" : "Open / saved")
               : (s.state == 1 ? "Locked — enter master password to reopen"
                               : "Closed"));
    workspace->setVisible(isOpen);
    create->setEnabled(accepted && !isOpen);
    open->setEnabled(accepted && !isOpen);
    unlock->setEnabled(accepted && s.state == 1);
    save->setEnabled(isOpen);
    closeVault->setEnabled(s.state != 0);
    lock->setEnabled(isOpen);
    const int previous = sheets->currentIndex();
    sheets->clear();
    for (uint32_t i = 0; i < s.sheets; ++i)
      sheets->addItem(core.query(SheetName, i));
    sheets->setCurrentIndex(
        qBound(0, previous, static_cast<int>(s.sheets) - 1));
    const bool editable = isOpen && s.rows && !s.protected_sheet;
    for (auto b : editButtons)
      b->setEnabled(editable);
    protect->setEnabled(editable);
    unlockSheet->setEnabled(isOpen && s.rows && s.protected_sheet);
    unlockMaster->setEnabled(unlockSheet->isEnabled());
    sheetState->setText(
        s.rows
            ? QString("%1 · %2").arg(
                  s.protected_sheet ? "Protected" : "Editing enabled",
                  s.verified ? "Verified by me" : "Not independently verified")
            : "No sheet yet");
    row->setMaximum(qMax(1, static_cast<int>(s.rows)));
    model->refresh();
    updating = false;
  }
  bool finish(uint32_t op) {
    uint32_t decision = 0;
    if (core.state.dirty) {
      QMessageBox box(
          QMessageBox::Warning, "Unsaved synthetic changes",
          "Save before closing or locking? Automatic inactivity, deactivation, "
          "Windows lock or sleep discards unsaved changes.",
          QMessageBox::Save | QMessageBox::Discard | QMessageBox::Cancel, &w);
      box.setDefaultButton(QMessageBox::Cancel);
      int answer = box.exec();
      if (answer == QMessageBox::Cancel)
        return false;
      decision = answer == QMessageBox::Save ? 1 : 2;
    }
    clearInputs();
    return action(op, decision);
  }

public:
  Impl(Window &w, std::function<qint64()> time)
      : QObject(&w), w(w), clock(std::move(time)) {
    elapsed.start();
    if (!clock)
      clock = [this] { return elapsed.elapsed(); };
    lastInput = clock();
    w.setWindowTitle("Tessaveil — unsigned synthetic alpha");
    QFont uiFont("Segoe UI");
    uiFont.setPixelSize(13);
    w.setFont(uiFont);
    w.resize(1280, 720);
    w.setMinimumSize(900, 600);
    w.setAcceptDrops(false);
    w.setStyleSheet(
        "QMainWindow,QWidget{background:#111c27;color:#e8eff5;font-family:'"
        "Segoe UI';font-size:13px;} "
        "QLineEdit,QComboBox,QSpinBox,QTableView{background:#192b3b;border:1px "
        "solid #70899e;border-radius:4px;padding:5px;} "
        "QPushButton{background:#24435a;border:1px solid "
        "#70899e;border-radius:5px;padding:7px;} "
        "QPushButton:disabled{color:#8798a6;background:#1a2936;} "
        "QLineEdit:focus,QComboBox:focus,QSpinBox:focus,QPushButton:focus,"
        "QTableView:focus,QCheckBox:focus{border:2px solid #6adecc;} "
        "QHeaderView::section{background:#24435a;color:#eef7ff;padding:5px;} "
        "QTableView{gridline-color:#385063;font-family:Consolas;} "
        "QCheckBox{padding:4px;} "
        "QCheckBox::indicator{width:16px;height:16px;}");
    auto central = new QWidget;
    auto root = new QVBoxLayout(central);
    root->setContentsMargins(16, 12, 16, 12);
    w.setCentralWidget(central);
    root->addWidget(
        label("TESSAVEIL  /  UNSIGNED ENGINEERING ALPHA — synthetic data only; "
              "never use real assets. No migration promise. Release and format "
              "freeze: NO-GO."));
    warning = new QWidget;
    auto warnLayout = new QVBoxLayout(warning);
    warnLayout->addWidget(
        label("This is a development-host experiment, not a security release. "
              "Multiple saved versions can reveal unchanged words by row "
              "comparison after password disclosure. Sheet passwords prevent "
              "accidental edits; they do not protect against master-password "
              "compromise. Inactivity, app deactivation, Windows lock and "
              "sleep discard unsaved changes and lock immediately. Memory "
              "clearing is best effort; a compromised OS can capture input."));
    auto accept =
        button("I understand — use synthetic data only", "warningAccept");
    warnLayout->addWidget(accept);
    root->addWidget(warning);
    auto vault = new QGridLayout;
    path = new QLineEdit;
    path->setObjectName("path");
    path->setAccessibleName("Vault path on development local NTFS");
    path->setPlaceholderText(
        "Full path to a .tessaveil-alpha file on local NTFS");
    path->setAcceptDrops(false);
    master = new Secret("master");
    master->setPlaceholderText("Master password (15+ characters to create)");
    vault->addWidget(path, 0, 0, 1, 3);
    vault->addWidget(master, 0, 3, 1, 3);
    create = button("&Create vault", "create");
    open = button("&Open vault", "open");
    unlock = button("&Unlock vault", "unlock");
    save = button("&Save", "save");
    closeVault = button("Close vault", "closeVault");
    lock = button("&Lock", "lock");
    vaultButtons = {create, open, unlock, save, closeVault, lock};
    for (int i = 0; i < vaultButtons.size(); ++i)
      vault->addWidget(vaultButtons[i], 1, i);
    root->addLayout(vault);
    auto stateLine = new QHBoxLayout;
    status = label("Closed", "state");
    stateLine->addWidget(status, 1);
    stateLine->addWidget(label("Inactivity lock:"));
    minutes = new QComboBox;
    minutes->setObjectName("minutes");
    minutes->setAccessibleName("Inactivity lock minutes");
    for (int m : {1, 5, 15, 30})
      minutes->addItem(QString::number(m) + " minutes", m);
    minutes->setCurrentIndex(1);
    stateLine->addWidget(minutes);
    root->addLayout(stateLine);
    message = label("", "message");
    message->setStyleSheet("color:#ffc2b4");
    root->addWidget(message);
    workspace = new QWidget;
    auto work = new QHBoxLayout(workspace);
    work->setContentsMargins(0, 0, 0, 0);
    auto sidebar = new QWidget;
    sidebar->setMinimumWidth(270);
    sidebar->setMaximumWidth(340);
    auto side = new QVBoxLayout(sidebar);
    side->setContentsMargins(0, 0, 8, 0);
    side->addWidget(label("SHEETS / ALPHA MATRIX"));
    sheets = new QComboBox;
    sheets->setObjectName("sheets");
    sheets->setAccessibleName("Current sheet");
    side->addWidget(sheets);
    auto nextSheet = button("Next sheet", "nextSheet");
    side->addWidget(nextSheet);
    connect(nextSheet, &QPushButton::clicked, this, [this] {
      if (sheets->count() > 0)
        sheets->setCurrentIndex((sheets->currentIndex() + 1) % sheets->count());
    });
    profiles = new QComboBox;
    profiles->setObjectName("profiles");
    profiles->setAccessibleName(
        "Profile and mode; unavailable reasons included");
    profiles->setSizeAdjustPolicy(
        QComboBox::AdjustToMinimumContentsLengthWithIcon);
    profiles->setMinimumContentsLength(22);
    profiles->view()->setMinimumWidth(650);
    int count = core.query(ProfileCount).toInt();
    for (int i = 0; i < count; ++i) {
      auto fields = core.query(Profile, i).split('\t');
      if (fields.size() != 5)
        continue;
      const bool enabled = fields[0] == "1";
      QString text = fields[1] + " / " + fields[3] +
                     (enabled ? "" : " — unavailable: " + fields[4]);
      profiles->addItem(text, i);
      profiles->setItemData(i, text, Qt::ToolTipRole);
      auto m = qobject_cast<QStandardItemModel *>(profiles->model());
      m->item(i)->setEnabled(enabled);
    }
    for (int i = 0; i < profiles->count(); ++i) {
      if (profiles->model()->flags(profiles->model()->index(i, 0)) &
          Qt::ItemIsEnabled) {
        profiles->setCurrentIndex(i);
        break;
      }
    }
    side->addWidget(profiles);
    sheetName = new QLineEdit("Synthetic sheet");
    sheetName->setObjectName("sheetName");
    sheetName->setAccessibleName("Sheet name");
    sheetName->setMaxLength(128);
    side->addWidget(sheetName);
    columns = new QComboBox;
    columns->setObjectName("columns");
    columns->setAccessibleName("Column count");
    columns->addItem("10 columns / 24 rows", 10);
    columns->addItem("36 columns / 24 rows", 36);
    columns->setCurrentIndex(1);
    side->addWidget(columns);
    add = button("Add synthetic sheet", "add");
    side->addWidget(add);
    sheetState = label("", "sheetState");
    side->addWidget(sheetState);
    sheetPassword = new Secret("sheetPassword");
    sheetPassword->setPlaceholderText("Sheet password / master credential");
    side->addWidget(sheetPassword);
    auto protectLine = new QHBoxLayout;
    auto set = button("Set password", "setSheetPassword");
    protect = button("Protect", "protect");
    protectLine->addWidget(set);
    protectLine->addWidget(protect);
    side->addLayout(protectLine);
    auto unlockLine = new QHBoxLayout;
    unlockSheet = button("Unlock sheet", "unlockSheet");
    unlockMaster = button("Use master", "unlockMaster");
    unlockLine->addWidget(unlockSheet);
    unlockLine->addWidget(unlockMaster);
    side->addLayout(unlockLine);
    side->addWidget(label("Sheet protection prevents accidental edits, not "
                          "disclosure after master-password compromise."));
    verificationConsent = new QCheckBox("I independently checked recovery");
    verificationConsent->setObjectName("verificationConsent");
    side->addWidget(
        label("Verify only after recovery in the original trusted wallet or "
              "official hardware check. Tessaveil does no cryptographic "
              "verification; never paste a full phrase here."));
    side->addWidget(verificationConsent);
    auto verify = button("Verified by me", "verify");
    side->addWidget(verify);
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
    model = new TableModel(core, table);
    table->setModel(model);
    main->addWidget(table, 1);
    main->addWidget(label("ONE ROW / SPIN — repeated observations and "
                          "different saved copies can reveal unchanged words. "
                          "Re-randomizing decoys does not remove this risk."));
    spinConsent = new QCheckBox(
        "I understand the row-comparison risk (required for each Spin)");
    spinConsent->setObjectName("spinConsent");
    main->addWidget(spinConsent);
    auto spinLine = new QHBoxLayout;
    row = new QSpinBox;
    row->setObjectName("row");
    row->setPrefix("Row ");
    row->setMinimum(1);
    row->setAccessibleName("Row number");
    symbol1 = new Secret("symbol1");
    symbol1->setPlaceholderText("Symbol");
    symbol1->setMaxLength(1);
    symbol1->setMaximumWidth(100);
    symbol2 = new Secret("symbol2");
    symbol2->setPlaceholderText("Repeat");
    symbol2->setMaxLength(1);
    symbol2->setMaximumWidth(100);
    word = new Secret("word");
    word->setMaxLength(128);
    word->setPlaceholderText("One word only");
    auto spin = button("Spin", "spin");
    for (auto widget : QList<QWidget *>{row, symbol1, symbol2, word, spin})
      spinLine->addWidget(widget);
    main->addLayout(spinLine);
    main->addWidget(label("Use ASCII 0–9 / A–Z. Check your keyboard layout. No "
                          "validity or target signal is shown."));
    work->addLayout(main, 1);
    root->addWidget(workspace, 1);
    editButtons = {set, verify, spin};
    connect(accept, &QPushButton::clicked, this, [this] {
      accepted = true;
      warning->hide();
      action(Ack);
      path->setFocus();
    });
    for (auto pair : {std::pair{create, Create}, std::pair{open, Open},
                      std::pair{unlock, Unlock}})
      connect(pair.first, &QPushButton::clicked, this,
              [this, op = pair.second] {
                TvInput input{};
                bool fieldsValid = true;
                if (op == Unlock)
                  fieldsValid &= master->consume(input, 0);
                else {
                  fieldsValid &= field(input, 0, path->text());
                  fieldsValid &= master->consume(input, 1);
                  fieldsValid &= field(input, 2, "Synthetic vault");
                }
                if (action(op, 0, 0, input, fieldsValid))
                  lastInput = clock();
              });
    connect(save, &QPushButton::clicked, this, [this] {
      clearInputs();
      action(Save);
    });
    connect(closeVault, &QPushButton::clicked, this, [this] { finish(Close); });
    connect(lock, &QPushButton::clicked, this, [this] { finish(Lock); });
    connect(add, &QPushButton::clicked, this, [this] {
      clearInputs();
      TvInput input{};
      const bool fieldsValid = field(input, 0, sheetName->text());
      if (action(Add, profiles->currentData().toUInt(),
                 columns->currentData().toUInt(), input, fieldsValid)) {
        updating = true;
        sheets->setCurrentIndex(sheets->count() - 1);
        updating = false;
      }
    });
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
      if (verificationConsent->isChecked()) {
        action(Verify, 1);
        verificationConsent->setChecked(false);
      }
    });
    connect(spin, &QPushButton::clicked, this, [this] {
      if (!spinConsent->isChecked()) {
        clearInputs();
        message->setText(
            "Read and acknowledge the row-comparison warning before Spin.");
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
        core.action(Tick, 0, 0, in, unused);
        if (core.state.state != 2) {
          clearInputs();
          refresh();
        }
      }
    });
    timer->start(250);
    connect(qApp, &QGuiApplication::applicationStateChanged, this,
            [this](Qt::ApplicationState state) {
              if (state != Qt::ApplicationActive)
                forceLock();
            });
    qApp->installEventFilter(this);
    action(Info);
    path->setFocus();
  }
  ~Impl() override { qApp->removeEventFilter(this); }
  bool close() { return finish(Close); }
  void forceLock() {
    // Pending UI input exists even without an open Rust session.
    clearInputs();
    if (core.state.state != 2)
      return;
    const bool dirty = core.state.dirty;
    workspace->hide();
    action(Lock, 2);
    message->setText(dirty ? "Locked. Unsaved synthetic changes were "
                             "discarded; the last saved vault is unchanged."
                           : "");
  }
  bool eventFilter(QObject *object, QEvent *e) override {
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
        QString ignored;
        core.action(Activity, 0, 0, in, ignored);
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
               std::function<bool(quintptr)> registerSession)
    : QMainWindow(), impl(new Impl(*this, std::move(clock))) {
  notificationsRegistered =
      registerSession
          ? registerSession(winId())
          : WTSRegisterSessionNotification(reinterpret_cast<HWND>(winId()),
                                           NOTIFY_FOR_THIS_SESSION);
  if (!notificationsRegistered) {
    impl->forceLock();
    centralWidget()->setEnabled(false);
    statusBar()->showMessage("Windows session monitoring is unavailable. Close "
                             "the alpha; opening a vault is disabled.");
  }
}
Window::~Window() {
  if (notificationsRegistered)
    WTSUnRegisterSessionNotification(reinterpret_cast<HWND>(winId()));
  delete impl;
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
