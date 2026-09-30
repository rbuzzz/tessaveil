# ADR 0001 — Desktop stack remains provisional

Date: 2026-09-29. Stack decision: provisional / blocked.
Selected candidate: none. Windows release readiness: NO-GO.

## Context and evidence

The specification proposes Rust + Avalonia/NativeAOT alongside Rust + Slint and
static C++/Qt 6. The [comparison report](../../reports/spikes/windows.md) records
equal probe contracts, bounded local discovery, dated primary licensing sources,
unknown measurements and weighted criteria. All three required build toolchains
are unavailable in the inspected PATH and default locations. There is no compiled
candidate, PE inventory, static linkage proof, temp trace, size/startup measurement
or accessibility observation. Contract validation is not a GUI test.

Task 4's exact clean-target blockers remain:

- No Windows 10 target or clean-image provenance was supplied; local host is Windows 11 development OS.
- Local Windows 11 Pro x64 build 26200 is a development host; no clean target provenance or separate access was supplied. Hyper-V VM enumeration was unavailable, so no configured clean VM could be verified.

## Decision and consequences

Keep Rust + Avalonia/NativeAOT as the specification's provisional candidate only.
Do not select a winner, freeze the desktop technology, or clear Windows release
readiness. Slint and Qt 6 remain equally unmeasured alternatives. The comparison
has zero observed scoring coverage and no defensible total or ranking.

Accept the documented technical/environment blockers as this task's research
result, with source contracts for later implementation. This does not claim that
the planned build and physical checks ran. No framework license route, third-party
redistribution approval, SignPath compatibility or certificate purchase is selected.
The repository's Apache-2.0 policy for original code remains intact.

## Reopening criteria

Provide exact pinned SDK/compiler/framework dependencies and build all three
[equivalent probes](../../spikes/windows/README.md). Record actual artifact hashes,
single-EXE/file-count results, PE imports and modules, static Rust linkage for
Avalonia, native/CRT dependencies, `%TEMP%` snapshots plus event traces, keyboard
and password accessibility, themes/scaling, dense-table behavior, size and startup.
Repeat on both supported clean Windows versions without development runtimes,
administrator requirements or network access. Development-host results, simulators
and Windows Server CI cannot replace the two clean-target results.

Finish license/SBOM/SignPath review and measured scoring before a later ADR revision
selects a candidate. The constant core call is not a synthetic vault interoperability
result: integrate Task 6's shared vector evidence before claiming that parent-spec
requirement. The separate physical-mobile/KDF and filesystem gates also remain.
Any change to these acceptance criteria requires the owner's separate decision;
the blocked research result grants no release exception.
