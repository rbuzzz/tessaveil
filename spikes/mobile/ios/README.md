# iOS source contract — BLOCKED

`Probe.swift` is the disposable adapter contract, not an Xcode project, signed
application or verified Swift/C ABI. A Mac/Xcode host and both physical iPhone
classes are unavailable. Toolchain and deployment versions are unselected.

When provisioned, create a disposable host target, expose
`../include/tessaveil_probe.h` in its bridging header, and statically link the Rust
`aarch64-apple-ios` archive. Record and pin Xcode/Swift/SDK/Rust versions and target
deployment range. Package the same independently verified synthetic binary by
exact hash. Call `SyntheticProbe.open` on a worker queue from a transient secure
input control and display only `ProbeSummary.display`.

Convert transient native text with `Array(text.utf8)` and pass its explicit byte
count. Do not use C-string termination, NSString normalization, preferences,
state restoration, logging or stored password properties. Embedded NUL stays in
the buffer for Rust rejection; all NFC behavior belongs to Rust. Clear input UI
and mutable copies best-effort after use; Swift copy-on-write/String/IME/OS buffers
prevent a guarantee of erasure. This adapter is not a complete secure UI/lifecycle.

Run shared normalization vectors through the completed FFI adapter in native
tests; show or log no normalized bytes. Use Instruments/device diagnostics to
record peak memory (currently UINT64_MAX = unmeasured), wall time, OOM/failure,
thermal state, OS, hardware class and exact core/library revision. Neither a
simulator build nor macOS/CI timings substitute for physical iPhone measurements.
