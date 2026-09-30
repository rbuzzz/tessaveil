# Static Qt executable probe

Implements [probe-contract.json](../probe-contract.json) with QtBase 6.8.3,
LLVM-MinGW 20250709 / Clang 20.1.8, CMake 3.31.8 and Ninja 1.12.1.
The real QTableView uses QAbstractTableModel (10,000 × 36), password QLineEdit,
explicit keyboard tab order, palette toggle and a separate constant-only C++ archive.
All evidence is development-host only.

QtBase source, build tree, install prefix and toolchains belong in the external
ASCII `$ToolchainRoot`, never in the repository. After sourcing environment.ps1,
configure with:

```powershell
cmake -S "$ToolchainRoot/qtbase-everywhere-src-6.8.3" -B "$ToolchainRoot/build/qt-static" -G Ninja -DCMAKE_BUILD_TYPE=Release -DBUILD_SHARED_LIBS=OFF -DFEATURE_static_runtime=ON -DQT_BUILD_TESTS=OFF -DQT_BUILD_EXAMPLES=OFF -DINPUT_opengl=no -DFEATURE_opengl=OFF -DFEATURE_opengl_dynamic=OFF -DFEATURE_sql=OFF -DFEATURE_network=OFF -DCMAKE_C_COMPILER=clang -DCMAKE_CXX_COMPILER=clang++ -DCMAKE_INSTALL_PREFIX="$ToolchainRoot/qt-6.8.3-static"
cmake --build "$ToolchainRoot/build/qt-static" --parallel 8
cmake --install "$ToolchainRoot/build/qt-static"
cmake -S spikes/windows/qt-static -B "$ToolchainRoot/build/qt-probe" -G Ninja -DCMAKE_BUILD_TYPE=Release -DCMAKE_PREFIX_PATH="$ToolchainRoot/qt-6.8.3-static" -DCMAKE_C_COMPILER=clang -DCMAKE_CXX_COMPILER=clang++
cmake --build "$ToolchainRoot/build/qt-probe"
New-Item -ItemType Directory "$ToolchainRoot/artifacts/qt-new"
Copy-Item "$ToolchainRoot/build/qt-probe/TessaveilQtProbe.exe" "$ToolchainRoot/artifacts/qt-new/"
llvm-strip --strip-all "$ToolchainRoot/artifacts/qt-new/TessaveilQtProbe.exe"
pwsh -NoProfile -File spikes/windows/measure.ps1 -Executable "$ToolchainRoot/artifacts/qt-new/TessaveilQtProbe.exe" -ReadObj "$ToolchainRoot/llvm-mingw-20250709-ucrt-x86_64/bin/llvm-readobj.exe" -ObservationRoot "$ToolchainRoot/observations/qt-new"
powershell -NoProfile -File spikes/windows/inspect-ui.ps1 -Executable "$ToolchainRoot/artifacts/qt-new/TessaveilQtProbe.exe" -ValidatePassword
```

The project rejects a dynamic Qt installation. Static Qt licensing/relinking,
third-party source/notices and SignPath eligibility remain release prerequisites;
no paid license is bought and no redistribution approval is claimed. No mobile
Rust/UniFFI reuse is proved by this C++ constant call.
