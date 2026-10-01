#include <QtCore/qglobal.h>
#include <cstdio>
#include <cstring>
int main() {
    const bool modified = std::strcmp(qVersion(), "6.8.3-tessaveil-relink-test") == 0;
    std::puts(modified ? "MODIFIED_QT_CONFIRMED" : "ORIGINAL_QT");
    return modified ? 0 : 1;
}
