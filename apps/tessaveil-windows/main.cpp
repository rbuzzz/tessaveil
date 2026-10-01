#include "window.h"
#include <QApplication>
int main(int argc, char **argv) {
  QApplication app(argc, argv);
  app.setApplicationName("Tessaveil");
  Window window;
  window.show();
  return app.exec();
}
