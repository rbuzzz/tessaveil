# Avalonia/NativeAOT — Source contract

Build: BLOCKED — .NET SDK, Rust/Cargo, MSVC and Windows SDK availability are
unverified; command/default-location checks found no usable toolchain.
No exact framework/compiler version, lockfile, compiled UI or binary is available.

Implement [the shared contract](../probe-contract.json) in a small C# Avalonia shell:
`Program.cs`, `App.axaml`, `ProbeWindow.axaml`, `SyntheticTableModel.cs`, and
`Probe.csproj`. Use a masked TextBox, virtualizing read-only DataGrid with 36 explicit
columns and lazy rows, automation names, focus order and theme resources. If the
selected control cannot meet virtualization/NativeAOT requirements, record failure;
do not replace it with a smaller or eager table.

The companion Rust crate has only `probe_core_version() -> u32 { 1 }`, exported
through a C ABI from a `staticlib`. The NativeAOT link must resolve the function from
that archive into the EXE; the input field never crosses the boundary. Do not use a
runtime-loaded Rust DLL and call that static linkage. Keep the link map, archive
hash, managed interop declaration and PE/module evidence.

Once exact versions are provisioned and pinned, build the core for
`x86_64-pc-windows-msvc`, then publish with `PublishAot=true`, `win-x64`, Release,
trimming/AOT diagnostics enabled and explicit native archive linkage. Freeze the
SDK in `global.json`, package versions/lockfile and Rust toolchain/Cargo lockfile
before collecting measurements. Resolve every relevant analyzer warning explicitly.
The NativeAOT publish shape is documented by Microsoft; native graphics/text DLLs
and resources must still be inventoried, not assumed embedded.

Follow [the common evidence procedure](../README.md). Single EXE, static Rust,
no extraction, no runtime requirement, secure-control behavior and accessibility
are all unknown until built and observed. This source contract is not compilation
evidence. Preliminary licenses and exact blockers are in the comparison report.
