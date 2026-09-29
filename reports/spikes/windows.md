# Windows desktop stack feasibility — Task 5

Verified (UTC): 2026-09-29

Stack decision: provisional / blocked. Selected candidate: none.
Windows release readiness: NO-GO.

This is an evidence-backed blocked research result. No framework was built, no UI
probe ran, and no release artifact exists. The deliverable is the equivalent
[probe contract and reproduction procedure](../../spikes/windows/README.md), three
candidate source contracts, read-only discovery, and the comparison below. Missing
toolchains prevent executable implementations and artifact measurements. Unknown
measurements are not failures of the framework or successful zero-valued results.

## Local toolchain evidence

Baseline: `ffe798951c2e6d95c87a22e4b318b6653a3ef681`,
`feature/tessaveil-research-foundation`, origin `git@github.com:rbuzzz/tessaveil.git`.
The initial working tree was clean. No AGENTS.md exists in this worktree.
The host is the Windows 11 Pro x64 development machine identified by Task 4,
build 26200, not a clean target.

Read-only `Get-Command` checks found `dotnet`, `rustc`, `cargo`, `rustup`, `cmake`,
`ninja`, `qmake6`, `qmake`, `qtpaths6`, `cl`, `clang`, and `dumpbin` absent from PATH.
`Test-Path` checks also found no .NET executable under Program Files, Rust compiler
under the standard Cargo directory, CMake executable under Program Files, `C:\Qt`,
or Visual Studio Installer `vswhere.exe`. No separately configured SDK/toolchain
was provided. This does not prove that no installation exists anywhere on disk.
Exact versions of those tools/frameworks: BLOCKED, no usable installation found;
no downloaded or compiled version is inferred from the documentation.

Observed supporting tools: PowerShell `7.6.5` (`$PSVersionTable.PSVersion`),
Python `3.14.2` (`python --version`). These can validate report contracts and discover
availability, but cannot compile any of the three candidate GUIs. Reproduce discovery
with `pwsh -NoProfile -File spikes/windows/verify.ps1`. The script emits no user paths
and performs no installations, VM launches, builds, application launches or network calls.

## Exact environment blockers inherited from Task 4

From [equipment availability](equipment-availability.md), without substituting a
developer workstation, simulator or Windows Server CI for either target:

- B-W10: No Windows 10 target or clean-image provenance was supplied; local host is Windows 11 development OS.
- B-W11: Local Windows 11 Pro x64 build 26200 is a development host; no clean target provenance or separate access was supplied. Hyper-V VM enumeration was unavailable, so no configured clean VM could be verified.
- B-A: .NET SDK and Rust/Cargo absent from PATH/default locations; MSVC/Windows SDK usability unverified, no Visual Studio locator available. Avalonia/NativeAOT build cannot be attempted reproducibly.
- B-S: Rust/Cargo absent from PATH/default locations; Windows linker/SDK usability unverified. Slint build cannot be attempted reproducibly.
- B-Q: Qt, CMake/Ninja absent from PATH/default locations; Windows compiler/SDK usability unverified. Static Qt 6 build cannot be attempted reproducibly.
- B-M: No candidate executable exists, so PE/dependency inspection, file count, size, startup, `%TEMP%` traces, accessibility, virtualization and core-boundary execution have no artifact to measure.

## Equivalent evidence matrix

Each BLOCKED cell identifies the missing input, not a guessed measurement.
Source contracts require the same masked input, virtualized 10,000 x 36 synthetic
table, keyboard path, themes and constant-only core call. No seed or cryptography
is implemented. No local runtime experiment substitutes for clean-machine evidence.

| Metric | Avalonia/NativeAOT | Slint | Qt 6 |
| --- | --- | --- | --- |
| Exact toolchain versions | BLOCKED: B-A; no SDK/framework/compiler versions observed | BLOCKED: B-S; no Rust/Slint/compiler versions observed | BLOCKED: B-Q; no Qt/compiler/CMake versions observed |
| License disposition | DOCUMENTED: L-A MIT framework; transitive review pending | DOCUMENTED: L-S license choice unresolved; transitive review pending | DOCUMENTED: L-Q static-link obligations unresolved; module review pending |
| Build / source status | BLOCKED: B-A; source contract only | BLOCKED: B-S; source contract only | BLOCKED: B-Q; source contract only |
| Clean Windows 10 | BLOCKED: B-W10 and B-M | BLOCKED: B-W10 and B-M | BLOCKED: B-W10 and B-M |
| Clean Windows 11 | BLOCKED: B-W11 and B-M | BLOCKED: B-W11 and B-M | BLOCKED: B-W11 and B-M |
| Single EXE / file count | BLOCKED: B-M; no runtime inventory | BLOCKED: B-M; no runtime inventory | BLOCKED: B-M; no runtime inventory |
| PE imports / loaded modules | BLOCKED: B-M; no PE or process to inspect | BLOCKED: B-M; no PE or process to inspect | BLOCKED: B-M; no PE or process to inspect |
| Native libraries / runtime prerequisites | BLOCKED: B-M; graphics/text/CRT dependencies unknown | BLOCKED: B-M; backend/renderer/CRT dependencies unknown | BLOCKED: B-M; platform plugin/graphics/CRT dependencies unknown |
| %TEMP% before/after | BLOCKED: B-M; no launch or before/after snapshots/event trace | BLOCKED: B-M; no launch or before/after snapshots/event trace | BLOCKED: B-M; no launch or before/after snapshots/event trace |
| Accessibility / keyboard focus | BLOCKED: B-M; no UIA/Narrator/focus observations | BLOCKED: B-M; no UIA/Narrator/focus observations | BLOCKED: B-M; no UIA/Narrator/focus observations |
| Binary size | BLOCKED: B-M; bytes unknown | BLOCKED: B-M; bytes unknown | BLOCKED: B-M; bytes unknown |
| Startup measurement | BLOCKED: B-M; milliseconds unknown; no runs | BLOCKED: B-M; milliseconds unknown; no runs | BLOCKED: B-M; milliseconds unknown; no runs |
| Virtualized table / themes | BLOCKED: B-A and B-M; contract unexecuted | BLOCKED: B-S and B-M; contract unexecuted | BLOCKED: B-Q and B-M; contract unexecuted |
| Core boundary | BLOCKED: B-A and B-M; C ABI/static Rust contract unexecuted | BLOCKED: B-S and B-M; separate Rust crate contract unexecuted | BLOCKED: B-Q and B-M; C ABI/static C++ contract unexecuted |

Static Rust linkage: BLOCKED. No Avalonia EXE, static archive, linker map, imports or
runtime modules exist to establish linkage. NativeAOT's self-contained deployment
description does not prove Rust or graphics libraries are statically linked. None
of the proposed constant-only calls proves synthetic vault creation/opening or
future UniFFI interoperability; that parent-spec requirement awaits Task 6 and
later integration, independently of toolchain availability.

## Licensing and primary sources

These are preliminary source reviews, not permission to bundle uninspected binaries.
No third-party code or assets were copied into the probes. Framework licenses do
not settle every native/transitive component. SignPath compatibility: pending for
every candidate's eventual full dependency set; no signing eligibility is asserted.
All sources below were inspected on 2026-09-29 UTC. Repository revisions pin the
license evidence only, not a selected framework/toolchain build.

- L-A: [Avalonia license at bc4d4396488b6b6b19b7fb81c74805cc84c12ac5](https://github.com/AvaloniaUI/Avalonia/blob/bc4d4396488b6b6b19b7fb81c74805cc84c12ac5/licence.md)
  uses MIT and requires retaining its copyright and permission notice. Dependencies
  and any optional components need separate review before redistribution.
- L-S: [Slint license at a8bac67980455bee65b254d7238abf83fc3696d9](https://github.com/slint-ui/slint/blob/a8bac67980455bee65b254d7238abf83fc3696d9/LICENSE.md)
  offers GPLv3, royalty-free and commercial framework paths. The royalty-free path
  includes attribution/disclosure requirements and excludes embedded systems.
  Documentation/examples being MIT does not make the framework MIT. Choose a
  specific applicable path and inspect its full terms/dependencies before bundling;
  no commercial purchase or automatic Apache-only distribution is assumed.
- L-Q: [Qt 6.11 licensing](https://doc.qt.io/qt-6.11/licensing.html) distinguishes
  LGPLv3, GPLv3-only modules, commercial terms and third-party code. The
  [official LGPL obligations](https://www.qt.io/development/open-source-lgpl-obligations)
  require source/notice and modification/relinking rights. Static distribution
  needs a concrete source/relinking package and module-by-module license decision;
  Apache-2.0 on original files does not discharge Qt obligations. No paid license
  or final redistribution approval is claimed.
- [Microsoft NativeAOT overview](https://learn.microsoft.com/en-us/dotnet/core/deploying/native-aot/)
  documents Windows C++ build prerequisites, self-contained native publication,
  trimming limitations and separate debug symbols. This supports planning only;
  it is not proof of this application's single-EXE, accessibility or no-extraction behavior.

## Scored decision with unknowns

Planned scale: 0 = measured failure, 1 = substantial measured limitations,
2 = meets the requirement with evidenced constraints, 3 = meets it with strong
evidence and no material unresolved limitation. U means unknown, not zero.
Weights total 100. A total would be `sum(weight * score / 3)` only after all
eight criteria have evidence. Never drop unknowns from the denominator or impute
framework reputation as a score. Hard packaging/clean-target gates override totals.

| Criterion | Weight | Avalonia/NativeAOT | Slint | Qt 6 | Evidence needed |
| --- | --- | --- | --- | --- | --- |
| Portability | 20 | U | U | U | Both clean targets; no admin/runtime/network requirements |
| Dependencies | 20 | U | U | U | Single EXE, PE/modules, no temp payload extraction |
| Accessibility | 15 | U | U | U | UIA/Narrator password behavior and complete keyboard path |
| Table performance | 15 | U | U | U | Identical virtualization/scroll workload, counts and timings |
| Figma fidelity | 5 | U | U | U | Later approved design comparison plus themes and scaling |
| License obligations | 10 | U | U | U | Chosen terms, full SBOM, redistribution/SignPath decisions |
| Maintenance | 5 | U | U | U | Reproducible locked build, diagnostics and upgrade experiment |
| Rust/UniFFI reuse | 10 | U | U | U | Boundary/vector integration and physical mobile evidence |

Observed score coverage: 0/8 for each candidate. Total score: undefined for each;
possible interval 0-100, not a ranking. License overview evidence alone cannot score
the eventual complete dependency set. Figma production design has not started.
The [ADR](../../docs/adr/0001-desktop-stack.md) retains the provisional candidate
without selecting it. Supply provisioned toolchains and both clean targets, implement
the identical contracts, then collect evidence before reconsidering any score or gate.
