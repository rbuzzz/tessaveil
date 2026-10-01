#include "theme.h"
#include <QtWidgets>

void applySemanticTheme(QApplication &application, QWidget &window,
                        const QString &theme) {
  QPalette palette = theme == "system" ? application.style()->standardPalette()
                                        : QPalette();
  QString errorColor = "#9b2c20";
  if (theme == "dark") {
    errorColor = "#ffc2b4";
    palette.setColor(QPalette::Window, QColor("#111c27"));
    palette.setColor(QPalette::WindowText, QColor("#e8eff5"));
    palette.setColor(QPalette::Base, QColor("#192b3b"));
    palette.setColor(QPalette::AlternateBase, QColor("#203649"));
    palette.setColor(QPalette::Text, QColor("#e8eff5"));
    palette.setColor(QPalette::Button, QColor("#24435a"));
    palette.setColor(QPalette::ButtonText, QColor("#eef7ff"));
    palette.setColor(QPalette::Highlight, QColor("#2b7a78"));
    palette.setColor(QPalette::HighlightedText, QColor("#ffffff"));
    palette.setColor(QPalette::PlaceholderText, QColor("#9dafbd"));
  } else if (theme == "light") {
    palette.setColor(QPalette::Window, QColor("#f4f7fa"));
    palette.setColor(QPalette::WindowText, QColor("#152331"));
    palette.setColor(QPalette::Base, QColor("#ffffff"));
    palette.setColor(QPalette::AlternateBase, QColor("#e7eef4"));
    palette.setColor(QPalette::Text, QColor("#152331"));
    palette.setColor(QPalette::Button, QColor("#d9e7ef"));
    palette.setColor(QPalette::ButtonText, QColor("#102331"));
    palette.setColor(QPalette::Highlight, QColor("#006c67"));
    palette.setColor(QPalette::HighlightedText, QColor("#ffffff"));
    palette.setColor(QPalette::PlaceholderText, QColor("#546776"));
  }
  window.setPalette(palette);
  window.setStyleSheet(QString(
      "QLineEdit,QComboBox,QSpinBox,QTableView{border:1px solid palette(mid);"
      "border-radius:4px;padding:5px;}"
      "QPushButton{border:1px solid palette(mid);border-radius:5px;padding:7px;}"
      "QLineEdit:focus,QComboBox:focus,QSpinBox:focus,QPushButton:focus,"
      "QTableView:focus,QCheckBox:focus{border:2px solid #008f83;}"
      "QHeaderView::section{background:palette(button);color:palette(button-text);"
      "padding:5px;}QTableView{gridline-color:palette(mid);font-family:Consolas;}"
      "QCheckBox{padding:4px;}QCheckBox::indicator{width:16px;height:16px;}"
      "QLabel#message{color:%1;}").arg(errorColor));
  window.setProperty("tessaveilTheme", theme);
  window.update();
}
