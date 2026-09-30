# Slint executable probe

Implements [probe-contract.json](../probe-contract.json) with Slint 1.13.1,
Rust 1.90.0 GNU, the winit backend, software renderer and AccessKit accessibility.
This is development-host evidence only. Results and limitations are in
[the comparison](../../../reports/spikes/windows.md) and [evidence.json](../evidence.json).

From the repository root, in a disposable PowerShell process with an external ASCII
`$ToolchainRoot` containing the pinned tools:

```powershell
. ./spikes/windows/environment.ps1 -ToolchainRoot $ToolchainRoot
$env:CARGO_TARGET_DIR = Join-Path $ToolchainRoot 'build/slint'
pwsh -NoProfile -File spikes/windows/slint/build.ps1 -ToolchainRoot $ToolchainRoot
pwsh -NoProfile -File spikes/windows/slint/build.ps1 -ToolchainRoot $ToolchainRoot -Test
New-Item -ItemType Directory "$ToolchainRoot/artifacts/slint-new"
Copy-Item "$env:CARGO_TARGET_DIR/release/tessaveil-slint-probe.exe" "$ToolchainRoot/artifacts/slint-new/"
pwsh -NoProfile -File spikes/windows/measure.ps1 -Executable "$ToolchainRoot/artifacts/slint-new/tessaveil-slint-probe.exe" -ReadObj "$ToolchainRoot/llvm-mingw-20250709-ucrt-x86_64/bin/llvm-readobj.exe" -ObservationRoot "$ToolchainRoot/observations/slint-new"
powershell -NoProfile -File spikes/windows/inspect-ui.ps1 -Executable "$ToolchainRoot/artifacts/slint-new/tessaveil-slint-probe.exe" -ValidatePassword # Expected exit 1: rejected password exposure
```

The helper uses `cargo rustc --locked --release` and final-link flags
`-C linker=<pinned-rust-lld> -C linker-flavor=ld.lld`. Plain GNU ld 2.42 produced
a real import-area access violation before window creation and in the test harness;
that configuration is rejected. The LLD-linked executable and native test are the
measured configuration. Host build dependencies keep the standard GNU toolchain.

This candidate is rejected for alpha: UI Automation ValuePattern exposes the
synthetic password. The checked-in `accessible-value: ""` override did not prevent
exposure after input mutation in the real observer. `inspect-ui.ps1
-ValidatePassword` therefore fails for this executable. This is a security failure,
not an unmeasured property or a successful workaround.

The lazy model computes a cell only when requested; the framework virtualizes visible
rows. No input reaches the separate constant-only core crate. Default framework
focus/accessibility/theme details need separate production hardening; no guarantee
of immutable GUI-string erasure is made. Royalty-free 2.0 is the proposed desktop
license route, requiring the AboutSlint widget or the specified public badge before
distribution; a complete dependency/SignPath review remains pending.
