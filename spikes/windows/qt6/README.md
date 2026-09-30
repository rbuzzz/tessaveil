# Qt 6 — Source contract

Build: BLOCKED — Qt development libraries, CMake/Ninja and MSVC/Windows SDK are
unavailable in command/default-location checks. No exact Qt/compiler version,
static configuration, compiled UI or binary is available.

Implement [the shared contract](../probe-contract.json) in `CMakeLists.txt`,
`main.cpp`, `ProbeWindow.cpp`, `SyntheticTableModel.cpp` and `probe_core.cpp/.h`.
Use a QLineEdit with Password echo mode, read-only QTableView with a lazy
QAbstractTableModel returning 10,000 by 36 synthetic cells, visible headers, keyboard
focus and theme palette tokens. Confirm viewport-only rendering and actual
accessibility behavior; do not instantiate one widget per cell.

The separate static C++ core library exports `uint32_t probe_core_version(void)`
through a C-compatible header and returns only `1`. Call it on button activation.
This checks a C++ boundary proposal, not Rust or UniFFI reuse. A future Rust C ABI
adapter and shared mobile vectors remain separate work, explicitly scored unknown.
The masked text is not passed across the boundary or persisted.

After provisioning, pin the Qt source revision, compiler, CMake, Ninja, SDK and
dependencies; build Qt Core/Gui/Widgets and the Windows platform plugin statically
with a documented Release configuration and explicit CRT policy. Link the core
archive and necessary static plugins, embedding required resources. Save the CMake
cache/configuration summary and link map. Then inventory PE imports, loaded modules,
fonts/graphics dependencies and all required files using the common procedure.

Follow [the common evidence procedure](../README.md). A static Qt build is not
automatically one dependency-free EXE. Before any distribution, choose and document
the license path including static relinking/source/notice obligations for each
module and third-party component. No commercial purchase or licensing acceptance
is implicit. This source contract is not compilation or performance evidence.
