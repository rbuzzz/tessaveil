# Avalonia NativeAOT executable source

Implements [probe-contract.json](../probe-contract.json), pinned to .NET SDK 8.0.414,
Avalonia 11.3.7 and Rust 1.90.0. The lazy 10,000-row DataGrid has 36 template columns,
masked input and a constant-only direct C ABI call into a Rust static archive.
The compiled XAML includes Fluent/DataGrid resources without a dynamic StyleInclude.

Development-host result: managed compilation and the Rust MSVC static archive succeed;
NativeAOT publish is BLOCKED by the missing Visual C++ platform linker. This is a
host-toolchain blocker, not proof that Avalonia cannot satisfy packaging requirements.
No native executable, byte-size or startup measurement is claimed.

```powershell
. ./spikes/windows/environment.ps1 -ToolchainRoot $ToolchainRoot
$env:RUSTFLAGS = ''
$env:CARGO_TARGET_DIR = Join-Path $ToolchainRoot 'build/avalonia-core'
& "$ToolchainRoot/downloads/rustup.exe" target add x86_64-pc-windows-msvc --toolchain 1.90.0-x86_64-pc-windows-gnu
cargo build --locked --release --target x86_64-pc-windows-msvc --manifest-path spikes/windows/avalonia-nativeaot/probe-core/Cargo.toml
Push-Location spikes/windows/avalonia-nativeaot
dotnet publish -p:RestoreLockedMode=true -c Release -r win-x64 -p:ProbeCoreLibrary="$env:CARGO_TARGET_DIR/x86_64-pc-windows-msvc/release/probe_core.lib" -o "$ToolchainRoot/build/avalonia"
Pop-Location
```

After supplying the missing official C++ workload/SDK in an appropriately provisioned
build environment, use the same [measurement script](../measure.ps1) and inspect all
native graphics/text dependencies. Static archive existence does not prove EXE linkage.
