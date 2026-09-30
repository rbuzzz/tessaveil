#pragma once
#include <QMainWindow>
#include <functional>
class Window : public QMainWindow {
  class Impl;
  Impl *impl;
  bool notificationsRegistered = false;

public:
  explicit Window(std::function<qint64()> clock = {},
                  std::function<bool(quintptr)> registerSession = {});
  ~Window() override;

protected:
  void closeEvent(QCloseEvent *) override;
  bool nativeEvent(const QByteArray &, void *, qintptr *) override;
};
