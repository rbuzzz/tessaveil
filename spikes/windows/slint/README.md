# Slint — Source contract

Build: BLOCKED — Rust/Cargo and a Windows C/C++ linker/SDK are unavailable in
command/default-location checks. No exact Slint/compiler version, backend selection,
Cargo lockfile, compiled UI or binary is available.

Implement [the shared contract](../probe-contract.json) in `Cargo.toml`, `build.rs`,
`ui/probe.slint`, `src/main.rs` and a separate `probe-core` library crate. Use one
masked input, a virtualized list/table viewport with 36 columns, sticky headings,
lazy synthetic model, keyboard focus and semantic light/dark tokens. Verify that the
chosen viewport virtualizes rows and horizontal cells rather than assuming a repeater
does so. Instrument realized controls and preserve the 10,000-row workload.

Invoke the separate Rust core crate's public `probe_core_version() -> u32 { 1 }`
from the button callback and show `1`. This is an in-process Rust module boundary,
not evidence of a foreign ABI or UniFFI integration. Input text stays in the masked
control and is never passed to core, logged, saved or placed on the clipboard.

After provisioning, pin Rust and all crate versions, check in Cargo.lock, choose and
record the Windows backend/renderer/features, then build the Release executable for
`x86_64-pc-windows-msvc` with the locked dependency set. Record CRT linking mode,
graphics dependencies, native DLLs and resources. Retain the linker map and module
inventory; no dynamic-runtime or static-packaging success is presumed.

Follow [the common evidence procedure](../README.md). Verify UIA/Narrator password
semantics, keyboard focus and scrolling on both clean targets. Slint's licensing
choice and every transitive component require review before bundling; see the report.
This source contract is not a compiled or measured probe.
