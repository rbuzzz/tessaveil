#pragma once
#include <QString>
class QApplication;
class QWidget;

void applySemanticTheme(QApplication &application, QWidget &window,
                        const QString &theme);
