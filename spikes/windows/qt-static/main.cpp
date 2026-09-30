#include <QApplication>
#include <QAbstractTableModel>
#include <QTableView>
#include <QLineEdit>
#include <QPushButton>
#include <QLabel>
#include <QVBoxLayout>
#include <QHeaderView>
#include <cstdint>
extern "C" std::uint32_t probe_core_version();
class SyntheticModel final : public QAbstractTableModel {
public:
    using QAbstractTableModel::QAbstractTableModel;
    int rowCount(const QModelIndex& parent = {}) const override { return parent.isValid() ? 0 : 10000; }
    int columnCount(const QModelIndex& parent = {}) const override { return parent.isValid() ? 0 : 36; }
    QVariant data(const QModelIndex& index, int role) const override {
        if (!index.isValid() || role != Qt::DisplayRole) return {};
        return QString("TEST-R%1-C%2").arg(index.row(), 5, 10, QChar('0')).arg(index.column(), 2, 10, QChar('0'));
    }
    QVariant headerData(int section, Qt::Orientation orientation, int role) const override {
        if (role != Qt::DisplayRole) return {};
        return orientation == Qt::Vertical ? QString::number(section) : section < 10 ? QString::number(section) : QString(QChar('A' + section - 10));
    }
};
int main(int argc, char** argv) {
    QApplication app(argc, argv);
    QWidget window; window.setWindowTitle("Tessaveil synthetic Qt probe"); window.resize(1280, 720);
    auto layout = new QVBoxLayout(&window); auto bar = new QHBoxLayout();
    auto input = new QLineEdit("TEST-INPUT-42!"); input->setEchoMode(QLineEdit::Password);
    input->setAccessibleName("Test input"); input->setContextMenuPolicy(Qt::NoContextMenu);
    auto invoke = new QPushButton("Invoke core"); auto theme = new QPushButton("Theme"); auto result = new QLabel("Core: 0");
    bar->addWidget(new QLabel("Test input")); bar->addWidget(input); bar->addWidget(invoke); bar->addWidget(theme); bar->addWidget(result);
    layout->addLayout(bar);
    auto table = new QTableView(); table->setModel(new SyntheticModel(table)); table->horizontalHeader()->setDefaultSectionSize(172);
    table->setEditTriggers(QAbstractItemView::NoEditTriggers); layout->addWidget(table);
    QWidget::setTabOrder(input, invoke); QWidget::setTabOrder(invoke, theme); QWidget::setTabOrder(theme, table);
    QObject::connect(invoke, &QPushButton::clicked, [&] { result->setText(QString("Core: %1").arg(probe_core_version())); input->clear(); });
    QObject::connect(theme, &QPushButton::clicked, [&] {
        static bool dark = false; dark = !dark;
        window.setStyleSheet(dark ? "QWidget { background:#171717; color:#FFFFFF; } :focus { border:1px solid #80BFFF; }" : "QWidget { background:#FFFFFF; color:#171717; } :focus { border:1px solid #005FCC; }");
    });
    window.show(); return app.exec();
}
