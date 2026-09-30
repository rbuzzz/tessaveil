# Windows desktop stack feasibility — executable alpha comparison

Verified (UTC): 2026-09-30

Stack decision: measured engineering selection, **alpha only**.
Selected candidate: static Qt 6.8.3 Widgets frontend; existing Rust core remains separate.
This is **not a Windows v1 technology freeze**. Windows release readiness: NO-GO.
Binary redistribution readiness: NO-GO until the static Qt compliance bundle is verified.

## Evidence and environment

Baseline `b77dabf96c5689e0676634d2264aaa647c89cd0a`, branch
`feature/windows-alpha`, origin `git@github.com:rbuzzz/tessaveil.git`; initial tree clean.
The real sources, build commands and common observers live in
[spikes/windows](../../spikes/windows/README.md). Raw numeric results, relative artifact
inventory, hashes, PE imports, loaded-module basenames, per-launch TEMP snapshots
and UIA observations are preserved in [evidence.json](../../spikes/windows/evidence.json).
The report-contract test checks required evidence without promoting missing measurements.

Host: Windows 11 Pro x64 development OS build 26200, Intel Core Ultra 7 258V
(8 cores / 8 logical processors), 33,880,342,528 physical-memory bytes.
PowerShell 7.6.5; Windows PowerShell/UIA observer 5.1.26100.9444; Python 3.14.2.
No simulator, clean image, mobile device, removable-media test or network-isolation
claim is substituted for missing equipment. All application data is synthetic.

## Exact tools and provenance

The versions below are deliberate research pins, not claims to be the latest.
Everything was provisioned into an external ASCII directory using process-local
environment variables; no toolchain/cache is committed. Archive URLs are pinned.

| Artifact | Version | SHA-256 |
| --- | --- | --- |
| [rustup archive](https://static.rust-lang.org/rustup/archive/1.28.2/x86_64-pc-windows-gnu/rustup-init.exe) | 1.28.2 | ccbfd951d8024856043b3a0c3903a59f39937bce8d3074768b0d3da55f21e817 |
| rustc.exe | 1.90.0, 1159e78c4, 2025-09-14 | 511d566f5950e657074a6e71afc1e72e43e73bc4f6d51581de2d0a9d9678aa55 |
| cargo.exe | 1.90.0, 840b83a10 | d3da8806a70cb304d9e63fa7538846062f7dabdc23a486ab42a52952037e5af5 |
| [.NET SDK zip](https://builds.dotnet.microsoft.com/dotnet/Sdk/8.0.414/dotnet-sdk-8.0.414-win-x64.zip) | 8.0.414 | 4b7084ea97216c1f98e19bac1960b7715dfad7678d963d482976a284a8332e34 |
| [LLVM-MinGW UCRT x64 archive](https://github.com/mstorsjo/llvm-mingw/releases/tag/20250709) | 20250709; Clang/LLVM 20.1.8 | 82babcd6aae4dc3606e8e0471d816989c384b4bf86a139f184a8b4a1b2c2758d |
| [CMake Windows x64 zip](https://github.com/Kitware/CMake/releases/tag/v3.31.8) | 3.31.8 | 81aa9964dbabd71fe02e7ec50472fd3ad56138c49944515ece9001efbff8d719 |
| [Ninja Windows zip](https://github.com/ninja-build/ninja/releases/tag/v1.12.1) | 1.12.1 | f550fec705b6d6ff58f2db3c374c2277a37691678d6aba463adcbb129108467a |
| [QtBase source zip](https://download.qt.io/archive/qt/6.8/6.8.3/submodules/qtbase-everywhere-src-6.8.3.zip) | 6.8.3 | 992bf7766e214a341ef793eb3665fb784787d2fd666955f5f507f4c6f1f770dd |
| Avalonia NuGet | 11.3.7 | 16c073de6c129fe259bd2002105646cd805d5fee2b14748541f97d4584fb0403 |
| Slint crate | 1.13.1 | f467a64a49620e41807016dc1d519ba0ebb9d1322f734853059f93b8c3f3d2bd |

Rustup and Qt archives matched official checksum files; LLVM matched its GitHub
asset digest. .NET also matched the official release-metadata SHA-512:
`ae86d5d9aeff5be9db7e306e0f85f708a41cd611f3cbef99ce60a3fe48c19d18fa1137d8f632d959ebc2b032e594b6970850581dd0e2afe64b9842d59899d2d6`.
Cargo.lock and packages.lock.json pin the resolved dependency sets.
Rust's bundled GNU ld is 2.42; final Slint application linking uses Rust LLD 20.1.8.
Qt uses Clang 20.1.8, static Qt/CRT linkage flags and a final llvm-strip pass.

The first .NET invocation unexpectedly created its default task-owned HTTPS
development certificate. That exact newly created certificate was removed and its
absence verified; subsequent invocations disable certificate creation explicitly.
No certificate identifiers or machine-specific paths are stored in the evidence.

## Equivalent experiment and limits

Each source implements a 1280×720 logical-pixel window, masked labelled input,
constant-only core call, theme button and lazy 10,000×36 coordinate-string model.
Qt uses QTableView/QAbstractTableModel; Slint uses StandardTableView/Model;
Avalonia uses DataGrid/IReadOnlyList with cell templates. This is a comparison
of framework-native shells, not identical control geometry. Sticky row labels,
exact theme/focus tokens, complete keyboard/scaling behavior and frame-rate /
realized-control-count measurements remain application acceptance work.

The two feasible EXEs were copied alone to separate artifact directories. Both
ran through the same `measure.ps1` with Windows-only child PATH and dedicated
TEMP/TMP directories. The final ten-run batches ran sequentially after all owned
compilers and UIA checks completed. A preliminary batch that overlapped an observer
was discarded, not combined with the final data.

Startup is monotonic Process.Start → correctly titled visible HWND answering
WM_NULL → DwmFlush. This is a window-readiness proxy, **not first-content-frame
instrumentation**, independent cold boots, or clean-machine performance.
The observer filters transient toolkit helper windows; an early tiny helper-window
capture was rejected. Own-window captures later showed both real dense tables.
No GUI screenshot includes user data, and screenshots are not release certification.

UIA checks inspect IsPassword and attempt ValuePattern reading before and after
setting a second synthetic value. Only exposed/not-exposed booleans are recorded.
They then invoke the real core button. No plaintext test input is copied to this report.

## Measured comparison

| Metric | Avalonia/NativeAOT | Slint | Qt 6 |
| --- | --- | --- | --- |
| Exact toolchain versions | DOCUMENTED: SDK 8.0.414; Avalonia 11.3.7; Rust 1.90.0; ILCompiler 8.0.20 | DOCUMENTED: Rust 1.90.0; Slint 1.13.1; LLD 20.1.8 | DOCUMENTED: Qt 6.8.3; Clang 20.1.8; CMake 3.31.8; Ninja 1.12.1 |
| License disposition | DOCUMENTED: MIT framework; full transitive review pending | DOCUMENTED: GPLv3 / Royalty-free 2.0 / commercial options; rejected technically | DOCUMENTED: LGPL-3.0-only route for Core/Gui/Widgets/Windows plugin; redistribution bundle BLOCKED |
| Build / source status | BLOCKED: managed compilation and Rust MSVC archive pass; NativeAOT platform linker absent | MEASURED: final LLD executable builds/runs; GNU ld configuration rejected | MEASURED: static QtBase and actual probe compile and run |
| Clean Windows 10 | BLOCKED: B-W10 | BLOCKED: B-W10 | BLOCKED: B-W10 |
| Clean Windows 11 | BLOCKED: B-W11 | BLOCKED: B-W11 | BLOCKED: B-W11 |
| Single EXE / file count | BLOCKED: no published native EXE | MEASURED: one runtime EXE, 5,094,400 bytes | MEASURED: one runtime EXE, 18,018,304 bytes |
| PE imports / loaded modules | BLOCKED: native publish failed | MEASURED: Windows API imports; module list in evidence; host hooks present | MEASURED: Windows/UCRT/graphics imports; module list in evidence; host hooks present |
| Native libraries / runtime prerequisites | BLOCKED: static graphics/dependency shape not observed | MEASURED: single EXE launches with Windows-only PATH on dev host | MEASURED: single EXE launches with Windows-only PATH; no Qt/LLVM DLL shipped |
| %TEMP% before/after | BLOCKED: no candidate launch | MEASURED: 10 empty-before/empty-after dedicated snapshots; transient extraction UNKNOWN | MEASURED: 10 empty-before/empty-after dedicated snapshots; transient extraction UNKNOWN |
| Accessibility / keyboard focus | BLOCKED: no native UI runtime | MEASURED: password role true but UIA value exposed; empty-value override fails; REJECTED | MEASURED: password role true, value not exposed, input setter and core invoke pass; full keyboard/Narrator pending |
| Binary size | BLOCKED: no native artifact | MEASURED: 5,094,400 bytes, SHA-256 in evidence | MEASURED: 18,018,304 bytes, SHA-256 in evidence |
| Startup measurement | BLOCKED: no native artifact | MEASURED: 10 warm runs; median 242.835 ms; range 224.476–471.031 ms | MEASURED: 10 warm runs; median 253.529 ms; range 229.370–753.770 ms |
| Virtualized table / themes | BLOCKED: actual source compiles, runtime unverified | DOCUMENTED: lazy model/native table renders; max working set 35,389,440 bytes; scroll/scaling metrics pending | DOCUMENTED: lazy model/native table renders; max working set 43,335,680 bytes; scroll/scaling metrics pending |
| Core boundary | BLOCKED: Rust static archive built; final EXE linkage unproved | MEASURED: separate Rust constant crate/native bounds test passes; not a vault FFI test | MEASURED: static C++ constant call shows 1; Rust vault boundary remains a separate integration gate |

Raw final startup milliseconds:

- Slint: 312.748, 224.476, 471.031, 251.397, 242.690, 238.563, 242.980, 237.668, 238.781, 251.506.
- Qt: 396.896, 253.114, 753.770, 229.370, 645.790, 249.475, 237.850, 253.943, 238.343, 643.848.

Slint SHA-256: `a798c561f79f35969b52fa80f51a37948b117c1797b9cb630780efbb044410e4`.
Qt SHA-256: `bf726cf33c583f83201d0a30796267450f4813e72dbc16eb75c861aa97ef0ec6`.
The smaller Slint artifact and similar median do not outweigh the password exposure.
The sample is too small and the host too uncontrolled for a general performance ranking.

PE imports contain Windows API DLL names; this is not clean-target dependency proof.
Both running processes also loaded `ebehmoni.dll` and `PSHook64.dll` from the host.
Their provenance is unresolved here; no claim of exclusively system loaded modules
is made. The tools neither remove nor change those host components. Network capture,
normal-user-TEMP observation and full process-tree event tracing remain unperformed.

## Reproducible failures and repairs

- Avalonia: `dotnet publish -p:RestoreLockedMode=true -c Release -r win-x64`
  with the generated Rust `ProbeCoreLibrary` exits 1 in
  `Microsoft.NETCore.Native.Windows.targets(123,5)`: “Platform linker not found.”
  The missing official Visual C++ / Windows SDK workload is a development-host
  toolchain blocker. No claim that NativeAOT itself is impossible is made.
  Static Rust linkage: BLOCKED until a final executable/link map can prove it.
- Slint: initial GNU ld 2.42 executable and native test harness exited
  `0xC0000005`; the event's address `0x4d9c24` falls in the import-area RVA.
  Minimal standard-only and raw-dylib Rust probes both passed. Changing only the
  final application/test link to pinned Rust LLD made the window and bounds test
  run. Exact lower-level responsibility for the mixed GNU/LLVM import failure
  is not conclusively attributed. The reproducible helper keeps this configuration.
- Slint's standard password LineEdit exposes its synthetic value through UIA
  despite IsPassword=true. The attempted `accessible-value: ""` override does
  not prevent exposure after input mutation. `inspect-ui.ps1 -ValidatePassword`
  exits 1 both before and after that attempt. Input SetValue still succeeds.
  This is a measured security/interaction rejection, not an unknown scored as zero.
  The failed override remains in the throwaway probe as reproducible evidence.
- Qt: the first real static build stopped in `qwindowswindow.cpp:2403` because
  `QOpenGLStaticContext` was excluded while dynamicgl stayed enabled. Setting
  only `FEATURE_opengl_dynamic=OFF` then triggered the configure guard requiring
  an explicit “no OpenGL” input. The final supported configuration sets
  `INPUT_opengl=no`, `FEATURE_opengl=OFF`, and `FEATURE_opengl_dynamic=OFF`.
  The full source build and probe then passed without modifying upstream source.
  The remaining upstream warnings concern missing basic cpp/winrt support and
  duplicated UIA macro definitions; affected behavior still needs target validation.

## Licensing: engineering selection is not redistribution approval

The pinned QtBase source headers for Core, Gui, Widgets and the Windows platform
plugin offer `LicenseRef-Qt-Commercial OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only`.
The intended open-source route here is **LGPL-3.0-only**, not a commercial purchase.
[Qt's licensing overview](https://doc.qt.io/qt-6.8/licensing.html),
[its LGPL obligations](https://www.qt.io/development/open-source-lgpl-obligations)
and the [pinned LGPL text](https://github.com/qt/qtbase/blob/v6.8.3/LICENSES/LGPL-3.0-only.txt)
must be applied to the actual combined artifact.

Before any public alpha binary, the packaging task must deliver and verify the
LGPLv3 static-link route: notices and GPL/LGPL texts, Minimal Corresponding Source
including the exact Qt build/configuration and changes, and Corresponding
Application Code suitable for recombining/relinking with a modified Qt version
(e.g. relinkable object files plus required source/build scripts). Preserve the
right to modify Qt and reverse-engineer for debugging those modifications.
Provide Installation Information where LGPLv3 §4e/GPLv3 §6 requires it. Demonstrate
a working relink workflow; a URL to upstream sources alone is not evidence of a
complete package. A different lawful route needs its own explicit evidence.

The **one-EXE runtime** requirement does not remove separate source, notices,
objects or compliance artifacts. The bundle is not assembled or verified in this
spike: **redistribution remains blocked**, including the later alpha packaging task.
Original repository code remains Apache-2.0. No automatic relicensing, commercial
license, certificate purchase or distribution exception is selected.

Qt's bundled third-party dependencies require their own inventory/terms, including
FreeType 2.13.3 (FTL or GPL-2.0-only, plus subcomponents), HarfBuzz 10.4.0 (MIT),
PCRE2, zlib, libpng, libjpeg, double-conversion and platform components. Source
`qt_attribution.json` files and final link inputs are the starting evidence, not a
completed SBOM. LLVM runtime/MinGW notices also need inclusion.

Other primary evidence:
[Avalonia MIT](https://github.com/AvaloniaUI/Avalonia/blob/11.3.7/licence.md),
[Slint 1.13.1 royalty-free terms](https://github.com/slint-ui/slint/blob/v1.13.1/LICENSES/LicenseRef-Slint-Royalty-free-2.0.md)
and [Microsoft NativeAOT prerequisites](https://learn.microsoft.com/en-us/dotnet/core/deploying/native-aot/).
Slint also offers GPLv3/commercial routes; its royalty-free route has attribution
requirements and is not Apache-2.0. SignPath compatibility: pending for every full
dependency set and the chosen distribution arrangement.

## Preserved release gates and scoring

- B-W10: No Windows 10 target or clean-image provenance was supplied; local host is Windows 11 development OS.
- B-W11: Local Windows 11 Pro x64 build 26200 is a development host; no clean target provenance or separate access was supplied. Hyper-V VM enumeration was unavailable, so no configured clean VM could be verified.

U means unknown, not zero. The original weighted release score remains incomplete.
The alpha engineering choice uses the actual build/package/input observations above;
it does not turn them into complete release scores or clear any physical-machine gate.

| Criterion | Weight | Avalonia/NativeAOT | Slint | Qt 6 | Evidence needed |
| --- | --- | --- | --- | --- | --- |
| Portability | 20 | U | U | U | Both clean targets |
| Dependencies | 20 | U | U | U | Full event trace and clean-target module/dependency review |
| Accessibility | 15 | U | U | U | Complete Narrator/keyboard/scaling acceptance; Slint has observed value exposure |
| Table performance | 15 | U | U | U | Common scrolling workload and realized-control/frame metrics |
| Figma fidelity | 5 | U | U | U | Approved production design comparison |
| License obligations | 10 | U | U | U | Proven static redistribution bundle and complete SBOM |
| Maintenance | 5 | U | U | U | Sustained reproducible build/upgrade evidence |
| Rust/UniFFI reuse | 10 | U | U | U | Actual Rust C ABI vault vectors and physical mobile results |

Observed score coverage: 0/8 for each candidate at the **complete release-criterion**
level; total undefined. This does not erase the measured alpha observations.
See [ADR 0001](../../docs/adr/0001-desktop-stack.md) for the scoped engineering decision.
