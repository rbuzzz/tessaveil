# ADR 0001 — Static Qt for Windows alpha engineering

Date: 2026-09-30. Selected candidate: Qt 6.8.3 static Widgets, **alpha only**.
This is **not a Windows v1 technology freeze**.
Windows release readiness: NO-GO. Qt redistribution readiness: NO-GO.

## Evidence and decision

Use a C++/Qt Widgets frontend for the Windows alpha, retaining the existing Rust
core and introducing a narrow C ABI in the dependent integration task. The probe
calls a separate constant-only C++ archive; it does **not** prove Rust integration,
vault interoperability, cryptography or safe secret handling in the eventual app.

The [comparison report](../../reports/spikes/windows.md) and
[raw evidence](../../spikes/windows/evidence.json) replace the previous unbuilt
comparison with pinned source builds and equal real probes on one development
host. Qt and Slint use the same 10,000 × 36 lazy table, masked input, theme switch
and constant core button; Avalonia implements the same contract but NativeAOT
publishing is blocked. Ten sequential warm launches per built candidate use the
same observer. Readiness is a visible, responsive window plus DwmFlush, not an
instrumented first-content frame or independent cold boots.

| Candidate | Actual evidence | Alpha disposition |
| --- | --- | --- |
| Static Qt 6.8.3 | One 18,018,304-byte EXE; median readiness 253.529 ms; no Qt or development-runtime DLL imports; UIA password value not exposed; input mutation and core invocation observed | Selected for engineering |
| Slint 1.13.1 / Rust 1.90.0 | One 5,094,400-byte EXE; median readiness 242.835 ms; final Rust LLD build runs after GNU-linker crash diagnosis | Rejected: UIA ValuePattern exposes synthetic password even with the tested empty accessible-value override |
| Avalonia 11.3.7 / .NET SDK 8.0.414 | Managed source compiled and Rust MSVC archive built; NativeAOT publish stops at absent Visual C++ platform linker | Development-host toolchain blocker; not proof NativeAOT is impossible |

Qt's security observation, successful static artifact and usable real table justify
the engineering choice. Slint's smaller size cannot compensate for the observed
password exposure. Qt's first upstream build failure was resolved by disabling both
OpenGL and dynamic OpenGL consistently, without patching upstream source. Full
commands, exact versions, hashes, initial failures and repaired configurations are
in the report and [probe READMEs](../../spikes/windows/README.md).

Empty dedicated TEMP before/after snapshots do not exclude transient extraction.
Loaded host monitoring modules have unresolved provenance. Neither toolchain-free
PATH runs nor this development host prove clean-machine dependencies, no-network
operation, Narrator compatibility or full keyboard/scaling/performance acceptance.
Unknown complete release criteria remain U, not zero and not a weighted ranking.

## Static Qt redistribution gate

Technical suitability is separate from permission to distribute. The inspected
QtBase 6.8.3 Core/Gui/Widgets and Windows-platform source headers offer
`LicenseRef-Qt-Commercial OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only`.
The proposed route is LGPLv3, not an assertion that our current build is ready for
distribution. Original project code remains Apache-2.0.

Before Task 5 publishes **any** alpha binary, verify and preserve a lawful Qt
redistribution bundle: exact corresponding library source and modifications,
notices and license texts, application object files or equivalent material and
instructions that actually permit relinking the static executable against a
modified library, compliant reverse-engineering/replacement terms, and installation
information where LGPLv3 section 4(e)/GPLv3 section 6 requires it. Verify the
relinking procedure, all enabled Qt modules and bundled third-party obligations,
and how this interacts with signing. Alternatively establish a different valid
license route with evidence. A single runtime EXE does not eliminate separate
source, object or compliance artifacts. This gate is open; no commercial license
purchase, redistribution approval or SignPath compatibility is implied.

## Remaining release gates

The original exact clean-target blockers remain:

- No Windows 10 target or clean-image provenance was supplied; local host is Windows 11 development OS.
- Local Windows 11 Pro x64 build 26200 is a development host; no clean target provenance or separate access was supplied. Hyper-V VM enumeration was unavailable, so no configured clean VM could be verified.

Repeat the same artifact checks on both documented clean targets as a non-admin,
offline and without development runtimes. Add process-tree file events, ordinary
user-temp observation, network capture, cold boots and first-frame timing. Complete
keyboard order, table corners and scrolling, realized-control counts, Narrator,
light/dark fidelity and 100/150/200% scaling checks. Implement and test the Rust C ABI
and shared synthetic-vault vectors. Finish SBOM/license/relinking/SignPath review.
Physical mobile/KDF and filesystem gates remain independent and are not replaced
by this spike. A later evidence-backed ADR must explicitly approve a Windows v1
freeze; this alpha decision grants no release exception.
