# Windows comparison: reproducible probe contract

Status: source contracts only; all candidate builds and measurements BLOCKED.
There is no compilable UI project or release artifact in this directory. Toolchains
are unavailable in the inspected environment. These contracts preserve the same
experiment for a later provisioned host; they are not simulated successful probes.
See [the evidence report](../../reports/spikes/windows.md) and
[ADR 0001](../../docs/adr/0001-desktop-stack.md).

## Safe checks available now

From the repository root, run:

```powershell
pwsh -NoProfile -File spikes/windows/verify.ps1
python -m unittest tests.repository.test_windows_spike_report -v
```

The script only discovers command/default-location presence and prints a sanitized
inventory. Exit 0 means discovery completed, not that a candidate compiled or passed.
It never installs, downloads, launches a VM, starts a probe, or grants release readiness.
Commands absent from PATH and default locations may exist elsewhere; absence is
bounded to the inspected environment. A newly discovered tool still needs exact
version and working compiler/SDK evidence before the build blocker can be removed.

## Shared experiment

All adapters implement [probe-contract.json](probe-contract.json) without deviations.
Use one window at 1280x720 logical pixels. Table indices are zero-based: 10,000 rows,
36 columns labelled `0-9,A-Z`, cells `TEST-R00000-C00` through `TEST-R09999-C35`.
Rows/cells must be produced lazily with viewport virtualization; do not construct
360,000 UI controls. Keep row numbers and headers visible. Scroll to all four
corners and verify the literal coordinates with no truncation. Record realized
row/cell counts and frame timings while scrolling; measure, do not assume virtualization.

One labelled password control masks `TEST-INPUT-42!`, with no autocomplete, history,
clipboard action, or logging. This is visual masking, not a security or memory-erasure
claim. Use Tab/Shift+Tab in the contract order, visible focus and arrows/PageDown in
the table, and a keyboard-operable theme toggle. The invoke button calls
`uint32_t probe_core_version(void)` and shows `1`; it never forwards input text.
The constant-only core is not a vault vector or proof of cryptographic compatibility.
That later evidence still depends on Task 6.

Apply the exact light/dark semantic tokens from the JSON. Check 100%, 150%, 200%
Windows scaling. With Narrator/UI Automation inspect names, roles, focus and
password treatment: the actual masked value must not be spoken or exposed through
the value pattern. Record observations, UIA tool/version, and failures; upstream
support documentation is not a substitute. No real words, seed, keys or cryptography.

## Reproduction after toolchain and target blockers are resolved

1. Record exact compiler, linker, Windows SDK, framework and transitive versions,
   build flags, backend, lockfile hashes, source commit, licenses, and OS build.
   Implement each adapter's source contract, commit the sources/locks and build
   x64 Release from that commit. Current license-source revisions are not build pins.
2. Inventory every delivered file: relative path, size in bytes, SHA-256. Separate
   optional symbols from required runtime files. Inspect PE imports and delay-load
   imports with `dumpbin /imports`, recursively inspect non-system DLLs, and compare
   loaded modules during masked input, scrolling, theme and core-call operations.
   Classify each as Windows system, bundled native, framework runtime or unresolved.
   Preserve linker maps proving static core linkage; a lone EXE filename is insufficient.
3. On each clean Windows target, record clean-image provenance, OS build, ordinary
   non-admin account, absence of development runtimes and network disconnected.
   Copy only the declared runtime artifact set. Launch and exercise the same sequence.
   Record non-admin application operation separately from any observer privileges.
4. Snapshot a dedicated empty process TEMP/TMP directory before/after launch/use/exit
   and observe create/write/delete events for the full process tree with a provisioned
   filesystem tracer. Also observe the normal user temp location; log counts and
   sanitized relative names, not personal paths. Snapshot equality alone cannot
   detect extract-then-delete behavior. If tracing is unavailable, extraction remains
   unknown. Report trace tool/version, scope, event count, payload classification,
   failures and SHA-256 of sanitized evidence. Never interpret missing capture as zero.
5. Measure process start to first rendered, keyboard-responsive frame with a monotonic
   timer and explicit ready marker. Record ten warm runs and five independent cold
   boots per candidate on each target; retain raw milliseconds, median and range,
   cache/boot method, CPU/RAM class and instrumentation. Do not mix development and
   clean-target numbers or count idle/launcher time as first-frame timing.
6. Perform the shared accessibility, scaling and table checks; record per-target
   screenshots of synthetic content, realized-control counts, frame timings and
   peak working set. Collect outbound-network observations too. A screenshot or
   framework claim alone cannot establish any of these results.
7. Populate the report with artifact hashes and inspectable evidence, review the
   scored comparison and ADR. Both clean targets and all mandatory packaging checks
   must pass before selecting a winner. Source-contract tests and hosted CI cannot
   clear this gate. Task 6's synthetic vault boundary remains an independent gate.

No system component installation, remote target, simulator, VM launch or paid
service is part of these checks. Toolchain provisioning and clean-target access
must be supplied separately before the blocked work can resume.
