# Development-host Windows alpha observation

Date: 2026-09-30. Source base: `d0de2087ae1c62647590e3a26997b337a00dc5ac`.
Scope: the Task 4 commit containing this document, native Qt Widgets plus the
real `tessaveil-core`. **This is not clean-Windows evidence or release approval.**
No executable was published. Unsigned alpha, synthetic only; release/freeze and
static Qt redistribution remain NO-GO.

## Architecture and ownership

`apps/tessaveil-windows/controller` is a workspace Rust static library. One
controller owns each `OpenVault`; decrypted payload, keys, dictionary and sheets
remain inside the core's non-cloneable Rust owner. Qt holds an opaque integer
handle and a fixed metadata reply. The virtualized `QAbstractTableModel` asks for
one display cell at a time. No full-payload, phrase, order-key, target-column,
serialized-plaintext or row-history API is exposed to C++. Core APIs required no
extension and schema 2 is unchanged.

ABI v1 uses fixed C layouts checked on both sides: 16,400-byte input and
4,136-byte reply, text offset 40. Every input has an explicit byte length bounded
at 4,096; invalid UTF-8/length/handles fail closed. Every extern boundary catches
unwinding. A poisoned registry drops its session owners. Destroy is explicit;
stale handles cannot mutate a replacement session. Null-peer rejection still
wipes the valid buffer. Calls are synchronous, pointers are disjoint/exclusively
borrowed, and neither side retains a foreign pointer. There are no callbacks or
C++ exceptions across the ABI. Allocation aborts are outside unwind containment.

Qt necessarily holds transient masked entry text and individual visible cell
strings; it never owns the full decrypted payload. Entry widgets clear before
the synchronous command. UTF-8 bridge buffers are passed by reference, zeroed by
Rust on success and failure, and wiped again on the C++ side; temporary Qt input
strings and replies are wiped. GUI/IME/framework/OS copies remain best effort,
not a forensic-erasure or hostile-OS guarantee. No secrets are logged.

Inactivity is enforced in Rust and by the UI privacy timer. Injected monotonic
time tests check the default five-minute boundary without sleeping five minutes.
Real key/mouse/wheel/touch events reset activity. Paint/timer events do not.
Deactivation, Windows session lock and suspend cover the workspace, clear input
and lock. Automatic locks discard dirty state; manual close/lock offers Save,
Discard or Cancel. Save failure keeps the dirty session and previous file. The
launch warning and guide explain that policy. Timeout choices last for the app run.
Failure to register Windows session notifications disables vault access and
locks the controller; an injected registration failure has a RED/GREEN regression.

## Actual builds and tests

Development host: Windows 11 Pro x64 build 26200, as characterized in the
[stack spike](../../reports/spikes/windows.md). Pins: Rust/Cargo 1.90.0 GNU,
Clang 20.1.8 / LLVM-MinGW 20250709 UCRT x64, QtBase 6.8.3 static, CMake 3.31.8,
Ninja 1.12.1, PowerShell 7.6.5; UIA observer Windows PowerShell 5.1.

Reproduction commands (external ASCII `$ToolchainRoot`, repository working dir):

```powershell
pwsh -NoProfile -File apps/tessaveil-windows/build.ps1 -ToolchainRoot $ToolchainRoot -Test
. ./spikes/windows/environment.ps1 -ToolchainRoot $ToolchainRoot
$env:CARGO_TARGET_DIR = "$ToolchainRoot/alpha-target"
$env:RUSTDOCFLAGS = '-C link-self-contained=yes'
cargo fmt --check
cargo clippy --workspace --all-targets --all-features --locked -- -D warnings
cargo test --workspace --all-targets --locked
cargo test --workspace --doc --locked
python tools/run_tests.py
python tools/alpha_catalog.py --check
python -m tools.sensitive_material
python -m tools.history_sensitive_material --root .
```

Results: formatting and warning-denying clippy passed; workspace/all-targets
passed 39 tests, followed by eight passing controller tests after two additional
edge cases (the 33 unchanged core tests had passed in the workspace run). Both
ownership doctests passed. The full Python suite passed 226 tests with four
environment-dependent skips in 264.490 seconds. Catalogue generation check and
both sensitive-material scanners passed with zero findings. Native UI tests
passed at all three application scales, and the final 100% run additionally
passed the session-registration failure regression.

The native test creates actual encrypted vaults in an owned `QTemporaryDir` and
exercises warning gating, create, three selectable profiles, 10/36 columns,
sheet selection, protection/unlock, explicit verification, Spin, save, close,
reopen, inactivity, master unlock, wrong password, damaged ciphertext, sleep and
deactivation. It also checks password echo semantics, shortcut rejection,
no context popup, no selection/export, zero cell editors, both scrollbars,
Tab leaving the table, control size and explicit Consolas table typography.
The same production window/model/bridge is linked into app and tests.

Controller tests use real NTFS files and real crypto, with injected time only.
They cover dirty-close refusal, failing save and save-before-close preserving the
prior file, authentication/corruption equivalence, unsupported version/header,
password policy, catalogue availability, dimensions, sheet verification and
protection, Spin's empty outward result, reopen and timeout discard. Core
valid/invalid Spin and ownership doctests remain mandatory. Supplemental edge
coverage is distinguished from the initial RED/GREEN implementation batches.

RED/GREEN records: initial controller workflow failed at unimplemented command
stubs (3 failures); ABI test failed on zero handle; native window test failed on
missing warning action. Subsequent regressions reproduced retained sessions after
mutex poisoning, unwiped input with a null output peer, missing accessible next
sheet navigation and the wrong table font. Their implementations pass. Layout
checks exposed inherited host font clipping; explicit 13px UI type, a scrollable
sidebar and bounded 29px table rows repaired it. Two test-only clippy findings
were fixed without suppressions. No core invariant was weakened.

## Live UIA, scales and reviewed images

`tests/observe.ps1` launches the actual `Tessaveil.exe`, operates only that
process's controls, and fails on missing controls or unexpected UIA responses.
It observes Password semantics, two successful synthetic value mutations and
mask-only reads; all five secret inputs expose masks rather than input values.
Master-input keyboard focus is observed. Sheet selection must report the actual
36-column sheet before its capture. It checks open, lock, generic authentication
failure, unlock/reopen and close through live widget invocations.

The observer uses an explicit child environment, disables automatic host DPI
scaling and applies Qt scale factors 1, 1.5 and 2. It does not change Windows
display settings. This verifies 100/150/200% **application scaling**, not moving
between differently scaled physical monitors. Client layout is 1280×720 logical
pixels, with native frame dimensions added by Windows. Native tests run at the
same scales. On this host UIA combo popup selection alone did not commit its
current value; the real, tested **Next sheet** button provides an accessible
alternative. Narrator and a complete assistive-technology audit remain open.

The following seven PNGs are bounded application-window captures, visually
reviewed for synthetic content and exact-hash allowlisted by the repository
scanner. All table cells come from the separate observation fixture's invented
`synthetic-NNN` dictionary. There are no real mnemonic words, entered secrets,
full phrases, local user paths or unrelated windows in these images:

- [Launch warning, 100%](screenshots/launch-scale-1.png)
- [10 columns, 100%](screenshots/table-10-scale-1.png)
- [36 columns, 100%](screenshots/table-36-scale-1.png)
- [36 columns, 150%](screenshots/table-36-scale-1.5.png)
- [36 columns, 200%](screenshots/table-36-scale-2.png)
- [Locked, 100%](screenshots/locked-scale-1.png)
- [Generic authentication error, 100%](screenshots/authentication-error-scale-1.png)

The fixture creator is a development-only Cargo example, never linked into the
app. It creates a new encrypted file using the real core; it does not bypass the
production controller. The native happy-path tests separately exercise the three
actual available profiles. Observation fixtures and redundant captures were
removed after checking the exact owned paths; secure erasure on SSD is not claimed.

No Tessaveil Figma file/node was supplied. The unrelated Renderis file was not
accessed or used. Implementation follows the approved written focused-process
direction; no pixel-perfect Figma comparison is claimed.

## Artifact/runtime and remaining limits

Locally built, unstripped `Tessaveil.exe`: 26,347,520 bytes. SHA-256:
`1b2eaa2ac5a7ccf1c15b40d2f73428b4f9007c8a7f38ed0a223cf3f72ca5b953`.
This identifies a dev artifact, not a published or signed release. Qt's cache
reports `BUILD_SHARED_LIBS=OFF` and `FEATURE_network=OFF`.

PE imports were inspected with `llvm-readobj --coff-imports`: Windows API/UCRT
families plus KERNEL32, SHCORE, WTSAPI32, ntdll, version, USER32, ole32, UxTheme,
GDI32, WS2_32, WINMM, SHELL32, ADVAPI32, NETAPI32, AUTHZ, USERENV, DWrite,
SETUPAPI, IMM32, dwmapi, SHLWAPI, d3d9, OLEAUT32, dxgi, d3d12, d3d11, bcrypt,
bcryptprimitives and comdlg32. No Qt/LLVM/application DLL is required alongside
the EXE. Networking-related system imports are not proof of network activity or
its absence; no outbound packet/process trace was performed. Runtime enumeration
also sees host `ebehmoni.dll` and `PSHook64.dll`, already observed in the spike;
their provenance remains unresolved. No host component was modified.

The host denied native clipboard opening and Qt could not retain even a public
synthetic sentinel. Accordingly tests assert intercepted clipboard shortcuts,
unchanged input and no clipboard-change signals; **OS clipboard-content
observation is unverified**. No existing user clipboard content was read. Initial
observer attempts that required empty password values were rejected until actual
mask-only behavior was explicitly checked; no unknown error counted as success.

No network, telemetry, update, provider submit, screenshot/export/print/import or
clipboard feature exists in the app. The observer's capture capability is a
separate development script. This observation does not establish clean Windows
10/11 launch, transient TEMP/file-event absence, network silence, physical mobile,
removable-media durability, independent audit or signing readiness.

**Task 5 must not publish the binary** before the verified LGPLv3 corresponding
source/object/relinking/install-information bundle or another lawful route is
complete. A single runtime EXE does not satisfy that separate gate.
