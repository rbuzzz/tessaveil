# Windows alpha stack probes

Real implementations of [probe-contract.json](probe-contract.json):
[Avalonia NativeAOT](avalonia-nativeaot/README.md), [Slint](slint/README.md), and
[static Qt](qt-static/README.md). The earlier `qt6` directory is a historical source
contract; the actual CMake project is `qt-static`.

See [the measured comparison](../../reports/spikes/windows.md),
[machine-readable evidence](evidence.json) and [ADR 0001](../../docs/adr/0001-desktop-stack.md).
Alpha selection is not clean Windows evidence or a Windows v1 technology freeze.

## Provisioning and reproduction

Install the report's exact official archive versions into an external, user-owned
ASCII `$ToolchainRoot`. Verify the recorded hashes before extraction. Rustup 1.28.2
is run in manager mode as `downloads/rustup.exe`, with process-local `RUSTUP_HOME`
and `CARGO_HOME`; set `auto-self-update disable` then install
`1.90.0-x86_64-pc-windows-gnu --profile minimal --component rustfmt`.
Extract the .NET SDK, CMake, Ninja, LLVM-MinGW and QtBase archives there.
No global PATH, registry, admin installation, binary toolchain, package cache or
absolute machine path belongs in tracked files.

Dot-source `environment.ps1 -ToolchainRoot $ToolchainRoot` only in a disposable
PowerShell process. It configures a portable GNU/Rust linker plus LLVM dlltool,
the latter's runtime path, isolated package/temp homes and disabled .NET telemetry
and development-certificate generation. Candidate READMEs contain build commands.
Build failures and crash evidence are preserved in the report, not scored as zero.

## Shared observation

Copy the candidate executable alone into a new external artifact directory.
Use `measure.ps1` with that executable, the pinned `llvm-readobj.exe`, and a new
empty `ObservationRoot`. It runs ten sequential launches, records byte count,
SHA-256, PE imports, loaded-module basenames, peak working set and separate TEMP/TMP
snapshots before/after each normal exit. Child PATH contains only Windows paths,
so the development toolchain cannot supply a missing runtime DLL. Do not collect
startup data while either compiler is running.

Timing starts immediately before `Process.Start` and stops at a visible top-level
window responding to WM_NULL followed by DwmFlush. It is a useful common readiness
proxy, **not** an instrumented first-content-frame latency. These are warm dev-host
launches, not independent cold boots. `inspect-ui.ps1`, run with Windows PowerShell
5.1, observes UI Automation roles/password/focusable flags and invokes the constant
core button. It attempts to read only synthetic password markers through
ValuePattern and records exposure booleans, never the input text. It does not
certify Narrator or measure keyboard navigation, scaling or scrolling performance.

The models expose the same 10,000 × 36 coordinate strings lazily. Framework-native
table views, masked controls and keyboard behaviors are under test, not assumed to
be security-certified. Framework default theme/focus details and sticky row labels
need application-level acceptance testing. The constant call returns `1` and is
not synthetic-vault interoperability evidence.

Before Windows v1, repeat on clean Windows 10 22H2 x64 and Windows 11 x64 with
documented image provenance, no development runtimes, no network and a non-admin
account. Add full process-tree file events (snapshots miss create/delete extraction),
normal user-temp observation, outbound-network capture, cold boots, first-frame
instrumentation, Narrator/password semantics, complete keyboard path, all four table
corners, realized-control counts, scrolling timings and 100/150/200% scaling.
All release gates remain NO-GO until their actual evidence exists.

Repository-only checks:

```powershell
python -m unittest tests.repository.test_windows_spike_report -v
python tools/run_tests.py
```
