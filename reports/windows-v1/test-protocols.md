# Tessaveil Windows v1 external-gate test protocols

Status: ready to run after the exact candidate and required equipment exist.
Current disposition: **NO-GO для реальных данных**.

These protocols use only the committed public TSVALPHA schema-2 fixture and
invented synthetic labels. Never enter a mnemonic, order key, private key,
funded-wallet backup or user vault. A development host, VM, hosted runner,
simulator or predecessor artifact cannot replace an environment named below.

## 1. Exact-candidate identity gate

The operator starts from the materialized `release-decision.json`, not the
committed policy template. Before any external test, record and independently
rehash all four identities:

| Required identity | Exact source |
|---|---|
| source Git commit | `candidate.source_sha` (40 lowercase hex characters) |
| runtime ZIP SHA-256 | `candidate.artifacts.runtime.sha256` |
| compliance ZIP SHA-256 | `candidate.artifacts.compliance.sha256` |
| `Tessaveil.exe` SHA-256 | `candidate.artifacts.executable.sha256` |

The runtime and compliance digests must exactly equal
`candidate.provenance_subject_sha256` in that order. Extract the runtime ZIP to
a new empty directory, rehash `Tessaveil.exe`, and compare it to the decision and
the runtime `SHA256SUMS`. Verify the compliance archive independently with
`packaging/windows/verify.py`. A missing value, mismatch, stale source SHA,
different downloaded byte or unmaterialized policy template is **BLOCKED**; do
not continue on a “close enough” build.

Create one evidence directory named only with the source SHA. Preserve:

- the untouched downloaded artifacts and materialized decision;
- SHA-256 output produced by a second tool;
- UTC start/end timestamps and operator role (no personal home paths);
- sanitized device/environment provenance listed below;
- raw tool output plus a short signed-off PASS/FAIL/BLOCKED summary;
- explicit confirmation that all inputs were synthetic/public.

Do not edit a failed evidence bundle. Start a new run ID and cross-reference it.

## 2. Common result rules

**PASS** requires every named step on the exact bytes, complete raw evidence,
and no unresolved deviation. **FAIL** means the required environment existed and
a criterion was violated. **BLOCKED** means an environment, authority, tool,
identity, measurement or independent reviewer was unavailable. Missing evidence
is never PASS. Record one release-decision row per gate; do not combine device
classes, Windows versions, filesystems or trace types.

Every environment record contains only sanitized facts needed to reproduce the
result: manufacturer/model class, CPU architecture, RAM class, OS edition/build,
filesystem/device class, security-update state, tool/version, source SHA and UTC
date. Do not record usernames, serial numbers, phone identifiers, tokens, local
profile paths or network credentials.

## 3. Clean Windows 10 and Windows 11

Run separately on a clean Windows 10 22H2 x64 target and a clean Windows 11 x64
target. Record image origin and installation date. Windows 10 must have current
ESU security updates. A reused development machine or ordinary hosted runner is
BLOCKED, even if the executable launches.

Prerequisites:

1. Standard non-administrator local account; no Rust, Qt, Visual Studio, Python,
   .NET desktop runtime or Tessaveil build tree installed.
2. Network physically disconnected or disabled before copying the candidate.
3. Fresh evidence directory on a separate non-secret capture volume.
4. OS-native hash tool plus the pre-approved process/file/network capture tools.

Procedure:

1. Copy only the verified runtime material. Rehash the ZIP and EXE on target.
2. From the standard account, launch `Tessaveil.exe` without installation or
   elevation. Record startup duration, loaded modules and child processes.
3. Create a synthetic vault, add both 10- and 36-column sheets, exercise profile
   search, a local synthetic custom dictionary, Spin valid/invalid/repeat flows,
   save, close, reopen, lock, timeout and recoverable errors.
4. Exercise exact-name sheet deletion, protection, verify/remove verification,
   backup, Closed-only restore and password rotation. Confirm old backup/old
   password behavior and the cross-version warning.
5. Repeat in RU and EN and System/Light/Dark. Use keyboard only for one full run.
6. Repeat startup and critical workflow while still offline. Confirm no runtime
   installation, account prompt, admin prompt or application payload sidecar.
7. Collect the trace protocols in sections 7 and 8 on this same exact EXE.

PASS: all functions complete under the non-admin offline account; only expected
Windows system dependencies load; no application payload is extracted; no
network request occurs; all recovery/error boundaries preserve prior valid data.
Any functional/security discrepancy is FAIL. Missing clean-image provenance,
required trace or either Windows version is BLOCKED.

## 4. Physical mobile format/KDF matrix and Mac/Xcode

Run the same public fixture (SHA-256
`0298259eccd7ecb9d4ca47383f93d0982a00c1e0ae1b9bd850ca8b89935edf25`)
through the pinned native wrapper and shared Rust core on four distinct physical
classes:

1. arm64 Android with 4 GiB RAM (lower bound);
2. current mid-range physical Android;
3. iPhone 11/A13/4 GiB class (lower bound);
4. current physical iPhone.

iOS also requires a provenance-recorded Mac/Xcode host and native device build.
An emulator/simulator is useful build evidence but is BLOCKED for these rows.

For each physical class:

1. Record sanitized model class, RAM class, SoC, OS/build, battery/thermal state,
   native toolchain versions, wrapper/core source SHA and locked dependency hashes.
2. Rehash the unchanged fixture on-device. Open it using both composed `é` and
   decomposed `e + U+0301`, including the non-BMP crab character. Record the exact
   normalized UTF-8 hex returned by the test harness. Embedded NUL must reject.
3. After one warm-up, perform ten foreground cold-open measurements of provisional
   Argon2id 65,536 KiB / 3 iterations / parallelism 4. Record every wall time,
   process peak memory, allocation/OOM result and thermal state; do not report only
   an average.
4. Exercise below/minimum/maximum/above bounds for memory (65,535/65,536/262,144/
   262,145 KiB), iterations (2/3/6/7) and parallelism (0/1/8/9). Only 65,536/3/4
   is allowlisted; other in-bound tuples must return UnsupportedKdf, and out-of-
   bounds tuples must reject before password normalization or KDF allocation.
5. Mutate the wrap tag and payload tag. They and a wrong password must never open
   an empty vault or return payload data.

PASS for a device row requires identical normalized bytes, successful exact fixture
open, all rejection classes, ten complete measurements without OOM, and raw logs.
Any incompatibility/OOM is FAIL and stops format/KDF freeze pending an explicit
security/product decision. Missing device/Mac access or unmeasured peak memory is
BLOCKED. The freeze row passes only after all four device rows and Mac native build
pass and a separate freeze decision cites them.

## 5. Removable NTFS, removable exFAT and controlled power loss

Do not run this section until the owner identifies the exact dedicated empty
physical device and separately authorizes destructive preparation/testing. This
document deliberately contains no formatting command. Never infer authorization
from a mounted drive letter. A virtual disk, fixed internal volume, user backup
device or unidentified removable medium is BLOCKED.

Record sanitized device class/capacity/controller, connection type, Windows build,
filesystem, allocation-unit size, write-cache policy and candidate hashes. Confirm
in writing that the device is dedicated, empty and expendable.

For removable NTFS and removable exFAT separately, repeat every point five times:

1. after adjacent temporary-file creation;
2. after complete ciphertext write;
3. after file flush/sync;
4. after reopen and structural/AEAD verification;
5. immediately before replacement;
6. immediately after replacement;
7. uninterrupted control.

After each process interruption, reconnect/reopen without repair and hash every
surviving target and adjacent temporary image. The named vault must authenticate
as exactly the prior or new image. A complete temporary image must authenticate as
ciphertext; partial data must never appear as an empty vault. Capture leftover names
without assuming deletion is secure erasure.

Controlled hardware power loss repeats the same named points with approved power
control. Do not interrupt the development workstation or an unidentified device.
Record controller behavior after power restoration, filesystem health, directory
entry outcome, hashes and authentication. PASS requires only old-or-new authenticated
target at every repetition, with no partial target accepted. Any other outcome is
FAIL. Missing device, destructive authorization or safe power-control method is
BLOCKED.

Rollback/version-comparison observation: retain two explicitly synthetic different
table versions plus one identical redundancy copy during the experiment. Demonstrate
that an older authentic image still opens (rollback is not detected), identical
copies add no different-table signal, and different decrypted synthetic rows expose
invariant-cell intersection. Evidence must not claim that full row regeneration,
password rotation or cleanup removes this risk.

## 6. Parser/sanitizer/fuzz evidence

Run the deterministic repository parser corpora first. Then, against the exact source
SHA, run approved sanitizer builds and bounded fuzz targets for envelope parsing,
canonical payload CBOR, catalogue JSON/schema and position-dependent inputs. Record
compiler/sanitizer/fuzzer versions, target, seed corpus hash, dictionaries, invocation,
wall-clock duration, executions, coverage summary, crashes/timeouts and minimized
reproducers. A crash, memory error, unbounded allocation or unresolved timeout is FAIL.
No sanitizer/fuzzer environment or incomplete target coverage is BLOCKED; deterministic
unit corpora alone do not clear this gate.

## 7. Network, TEMP, process/file and startup-log traces

Capture these as separate rows on both clean Windows targets while running the full
section 3 workflow:

- packet and per-process network events with networking first disconnected and then
  connected but idle;
- recursive `%TEMP%` and relevant file events correlated to the Tessaveil PID;
- child process, loaded module, file-open/create/rename/delete and registry events;
- console/debug/startup logs, sanitized without deleting relevant event categories.

Begin capture before process creation and stop only after process exit and a bounded
quiet period. Hash raw traces. PASS requires zero application-originated network
activity, zero extracted application payload/assembly/native sidecar in TEMP, no
unexpected child process/provider call, only documented file operations, and no
secret/synthetic input echoed into logs. A tooling blind spot is BLOCKED, not PASS.

## 8. Accessibility, Narrator and scaling

On each clean Windows target, run keyboard-only creation through recovery and every
modal. Repeat at real 100%, 150% and 200% display scaling. With Narrator enabled,
record role/name/state/focus for every control; secret values, words, selected target
columns and hidden metadata must never be announced. Verify focus order, Escape/
default destructive behavior, visible focus, error alerts, table scrolling with row
and column context, `0/O` and `1/I` readability, and the privacy cover. Automated UIA
is supporting evidence only. PASS requires the complete human Narrator/scaling record
on both clean systems. Missing Narrator or physical scaling evidence is BLOCKED.

## 9. Catalogue, Figma, independent audit and signing

- **Catalogue:** rerun JSON Schema and Python semantic validation, generated-document
  drift, licenses and every selectable vector. PASS requires every mandatory release
  item to meet the approved terminal criterion; an evidence-backed `blocked` research
  row still blocks Windows release.
- **Figma:** make Segoe UI and Consolas available in the authorized `Tessaveil —
  Product Design` file or obtain explicit substitution approval, then rerun exact-font
  render/structure/accessibility inspection. Never use the unrelated Renderis file.
- **Independent audit:** give the reviewer exact source/artifact hashes, threat model,
  format, fixture, parser corpus and build evidence. Preserve scope, findings, severity,
  remediation commits and retest disposition. Internal/subagent review is not PASS.
- **SignPath/Authenticode:** after SignPath acceptance, verify the publisher, certificate
  chain/timestamp and PE signature of a subsequent signed RC, then rerun clean-Windows
  and hash/provenance checks on those signed bytes. Rejection/non-acceptance remains
  BLOCKED until the owner chooses an approved alternative; an unsigned RC is never stable.

## 10. Exact-SHA CI, SBOM, relink and GitHub provenance

After the final source commit is clean, run the pinned branch/PR workflow on that exact
event SHA. Download hosted artifacts rather than trusting local copies. Rehash every
downloaded byte; rerun the independent archive verifier; compare SBOM graph, notices,
Qt corresponding source, application objects and modified-Qt relink proof.

GitHub attestation verification must be machine-readable and strict for runtime ZIP,
compliance ZIP and the materialized decision: repository and signer workflow fixed,
self-hosted runners denied, subject digest equal to the downloaded bytes, and source
digest/ref equal to the exact workflow event. Preserve JSON verification receipts and
their SHA-256 values. A local checksum or predecessor attestation is not provenance.

PASS requires exact-SHA CI success, independently verified hosted bytes, complete
SBOM/notices/relink evidence and strict provenance for all subjects. A workflow still
running, artifact expiry, hash drift, unsupported attestation permission or predecessor
result is BLOCKED/FAIL as applicable.

## 11. Normative tool pins and acquisition record

The versions below are fixed for this candidate campaign. An operator may not
silently replace any of them with a package named `latest`. Before use, preserve
the installer/archive, its SHA-256, its Authenticode/notarization result where
applicable, the official download URL and the tool's own version output. A pin
which cannot be acquired or whose signature/hash is not independently approved
is **BLOCKED**, not permission to substitute another version.

| Purpose | Exact pin | Version command / authoritative local record |
|---|---|---|
| Product compiler | Rust 1.90.0 and Cargo 1.90.0 | `rustc -Vv`; `cargo -V`; `rust-toolchain.toml` |
| Candidate verification | Python 3.12.10 embedded x64 | `python --version`; SHA-256 in `packaging/windows/toolchains.json` |
| Windows operator shell | PowerShell 7.6.5 x64 portable | `pwsh --version`; record archive SHA-256 before copying to the clean target |
| Windows file/process trace | Microsoft Sysinternals Process Monitor 4.11 | `Procmon64.exe /?`; verify Microsoft signature and record binary SHA-256 |
| Windows signature verification | Windows SDK 10.0.26100.9169 x64 `signtool.exe` | `signtool.exe /?`; record SDK ISO and binary hashes |
| Android transport | Android SDK Platform-Tools 37.0.1 | `adb version`; record downloaded archive SHA-256 |
| Android native compiler | Android NDK 30.0.16248370 | `clang --version`; record package revision and archive SHA-1/SHA-256 |
| Apple native compiler | Xcode 26.5 with its bundled Swift/iOS SDK | `xcodebuild -version`; `xcrun swiftc --version`; `xcrun --sdk iphoneos --show-sdk-version` |
| Parser campaign | cargo-fuzz 0.13.2 with pinned nightly `nightly-2026-09-01` | `cargo fuzz --version`; `rustc +nightly-2026-09-01 -Vv` |
| Hosted verification | GitHub CLI 2.86.0 | `gh --version`; use only with the pinned workflow actions |

The Windows build inputs remain the exact archives and hashes in
`packaging/windows/toolchains.json`: LLVM-MinGW 20250709, CMake 3.31.8,
Ninja 1.12.1 and Qt 6.8.3. OS-inbox `Get-FileHash`, `pktmon`, Narrator,
Performance Monitor and PowerShell 5.1 are bound to the recorded OS build;
record their file versions and SHA-256 instead of treating them as floating
tools. The Android/iOS pins authorize a measurement harness only; the existing
disposable TVSPIKE0 probe cannot clear a TSVALPHA schema-2 product gate.

## 12. Exact commands, evidence layout and receipts

Work from a new evidence directory on a non-secret capture volume. Substitute
only the three angle-bracket values, never a user profile path:

```powershell
$SourceSha = '<40-lowercase-hex-source-sha>'
$EvidenceRoot = 'E:\TessaveilEvidence\<40-lowercase-hex-source-sha>'
$ArtifactRoot = Join-Path $EvidenceRoot 'downloaded-artifact'
git rev-parse HEAD
git status --porcelain
Get-FileHash -Algorithm SHA256 (Join-Path $ArtifactRoot 'runtime.zip')
Get-FileHash -Algorithm SHA256 (Join-Path $ArtifactRoot 'compliance.zip')
Get-FileHash -Algorithm SHA256 (Join-Path $ArtifactRoot 'runtime\Tessaveil.exe')
python packaging/windows/release_decision.py verify --report (Join-Path $ArtifactRoot 'release-decision.json') --source-sha $SourceSha --runtime (Join-Path $ArtifactRoot 'runtime.zip') --compliance (Join-Path $ArtifactRoot 'compliance.zip') --executable (Join-Path $ArtifactRoot 'runtime\Tessaveil.exe')
```

Capture UTC start/end, command line, exit code, stdout/stderr, exact tool version,
environment provenance and raw evidence for every run. Each mandatory gate gets
at least one immutable `receipts/<gate-id>.json` below `$EvidenceRoot`; references
to source files alone are not receipts. Each receipt has exactly these fields:

```json
{
  "schema_version": 1,
  "gate_id": "<mandatory-gate-id>",
  "result": "pass",
  "candidate": {
    "kind": "exact-candidate",
    "source_sha": "<40-lowercase-hex-source-sha>",
    "artifacts": {
      "runtime": {"sha256": "<64-lowercase-hex>"},
      "compliance": {"sha256": "<64-lowercase-hex>"},
      "executable": {"sha256": "<64-lowercase-hex>"}
    },
    "provenance_subject_sha256": ["<runtime-sha256>", "<compliance-sha256>"]
  },
  "scope": "<exact copy of the gate evidence scope>",
  "environment": "<exact copy of the gate evidence environment>",
  "date": "YYYY-MM-DD"
}
```

Hash each receipt with `Get-FileHash -Algorithm SHA256`; put its relative path
and lowercase digest into the gate's `evidence.receipts`, and make
`evidence.sha256` equal the first receipt hash. Do not edit a receipt after it is
hashed. The final authorization command rehashes artifacts and all receipt files,
and verifies each receipt's full exact-candidate binding:

```powershell
python packaging/windows/release_decision.py verify --report (Join-Path $EvidenceRoot 'release-decision.json') --source-sha $SourceSha --runtime (Join-Path $ArtifactRoot 'runtime.zip') --compliance (Join-Path $ArtifactRoot 'compliance.zip') --executable (Join-Path $ArtifactRoot 'runtime\Tessaveil.exe') --require-real-data --evidence-root $EvidenceRoot
```

Missing files, a changed byte, an escaped path, a policy reference without a
receipt, a different candidate object or an unmaterialized template must fail.

## 13. Gate-by-gate operator checklist

This table is normative together with sections 3–10. “Repository suite” means
the exact checked-out SHA, Rust 1.90.0 and Python 3.12.10. Every row produces its
own receipt even if another row uses the same raw trace.

| Gate ID | Exact run and minimum duration/repetition | PASS boundary |
|---|---|---|
| `catalogue-research-readiness` | `python -m unittest tests.repository.test_policy tests.repository.test_research_handoff -v`; review every terminal row once | Tests pass and no mandatory release row remains `blocked` or merely `documented`. |
| `selectable-profile-vectors` | `cargo test --locked -p tessaveil-core --test catalog_gate` once on the candidate | All selected product/platform/version/mode vectors pass; name equality alone is not a conflict. |
| `core-security-failure-suite` | `cargo test --locked -p tessaveil-core --test security_gate --test corruption --test recovery --test atomic_save` once, plus independent fixture regeneration in a disposable copy | All exact fixture, mutation, KDF, Unicode, entropy and persistence assertions pass. |
| `parser-fuzz-evidence` | Run deterministic `format_contract`, then four targets `envelope`, `canonical_cbor`, `catalogue_json`, `position_inputs` for **60 minutes per fuzz target** under cargo-fuzz 0.13.2/nightly-2026-09-01 and repeat sanitizer corpus once | Zero crash, timeout, sanitizer finding or unbounded allocation; target/corpus hashes and minimized outputs retained. Missing target is BLOCKED. |
| `format-kdf-physical-freeze` | Complete all four physical rows below, compare normalized UTF-8 and ten KDF samples per device, then record a separate signed freeze decision | All device and Mac rows pass the same exact fixture; no host/simulator substitution. |
| `figma-handoff` | In the authorized `Tessaveil — Product Design` file, capture file key/build, exact Segoe UI/Consolas availability, rendered RU/EN frames and accessibility structure once | Exact fonts or explicit owner-approved substitutes, correct file, and complete rendered inspection. |
| `complete-windows-workflows` | On each clean OS, run the section 3 workflow in RU/EN, three themes and keyboard-only; at least one complete run per combination | Every workflow completes with only synthetic data and all recovery/error states preserve authenticated data. |
| `clean-windows-10` | Windows 10 22H2 x64 with current ESU, standard user, offline; three cold launches and one full 90-minute workflow/trace run | Clean provenance, no installed runtime/elevation/network/payload extraction, all functions pass. |
| `clean-windows-11` | Clean Windows 11 x64, standard user, offline; three cold launches and one full 90-minute workflow/trace run | Same boundary as Windows 10. A development machine or hosted runner is rejected. |
| `physical-android-4gib` | arm64/4 GiB physical device; one warm-up plus ten cold KDF opens and full rejection matrix | Exact TSVALPHA hash/open, NFC equality, measured peak RSS, no OOM, correct failure classes. |
| `physical-android-current` | Current mid-range arm64 physical device; same ten cold runs | Same boundary; a second physical class is required. |
| `physical-iphone-a13` | iPhone 11/A13/4 GiB physical device; one warm-up plus ten cold opens | Same boundary with Instruments/device memory and thermal evidence. |
| `physical-iphone-current` | Current physical iPhone; same ten cold runs | Same boundary; simulator evidence is supporting only. |
| `mac-xcode-native-build` | `xcodebuild -version`, Swift/SDK version capture, clean device archive and native tests once with Xcode 26.5 | Locked exact-source arm64 device build and native tests pass; Mac provenance retained. |
| `removable-ntfs` | Pre-identified dedicated empty device, already prepared as NTFS under separate written authority; seven interruption/control points, five repetitions each | Only prior or new authenticated exact image survives every run. |
| `removable-exfat` | Same on a separately recorded exFAT preparation; seven points, five repetitions each | Same old-or-new authenticated boundary; no inference from NTFS. |
| `controlled-power-loss` | Approved isolated power controller; seven points, five repetitions per filesystem | Old-or-new authenticated target only; filesystem/controller health captured after power restoration. |
| `network-trace` | `pktmon` capture on both clean OS targets for disconnected and connected-idle full workflows; begin before launch and retain 30 seconds after exit | Zero Tessaveil-originated packet/event; tool blind spot is BLOCKED. |
| `temp-extraction-trace` | Process Monitor 4.11 plus recursive `%TEMP%` before/after inventories on both clean targets for the full workflow | No Tessaveil application payload, assembly or native sidecar is created/extracted. |
| `process-file-startup-log-trace` | Process Monitor 4.11 process/file/registry/module trace plus captured stdout/stderr, three cold launches and full workflow | No unexpected child/provider, path, registry mutation or secret in logs. |
| `accessibility-narrator-scaling` | Human Narrator/keyboard run on both OSes at actual 100%, 150%, 200%; one full workflow per scale | Names/roles/state/focus correct; no secret/target metadata announced; no clipping or blocked action. |
| `independent-security-audit` | Independent reviewer receives exact hashes, threat/format, fixture/corpora/build evidence; review, remediation and retest have bounded dates | All in-scope findings resolved or explicitly accepted by the owner; internal/subagent review never passes. |
| `signpath-authenticode` | SignPath-accepted project signs a subsequent candidate; run Windows SDK 10.0.26100.9169 `signtool.exe verify /pa /all /v Tessaveil.exe` and repeat exact-byte/provenance/clean-Windows checks | Expected publisher, valid chain and timestamp on the tested bytes. Unsigned RC/non-acceptance is BLOCKED. |
| `licensing` | Run repository policy tests, inspect every shipped dictionary/tool/runtime license and signing-distribution compatibility once | Every shipped byte has compatible terms and traceable notice/source obligation. |
| `sbom-notices` | Run `packaging/windows/gate.ps1` on a new output directory; independently verify CycloneDX graph, notices and hashes | Complete locked graph and byte-bound notices pass; no unknown/unrelated file. |
| `qt-source-relink` | Same gate plus the Qt 6.8.3 modified-marker relink and headful synthetic smoke | Corresponding source builds and modified Qt binary runs; application objects remain identical. |
| `exact-sha-ci` | Trigger the pinned workflow on the exact event SHA, then `gh run watch <run-id> --exit-status`; download artifact to a new directory | The `GitHub-hosted runner windows-2022` run passes and downloaded hashes match. Hosted evidence is allowed only here and for provenance. |
| `github-provenance` | Use `gh attestation verify` exactly as section 16 for all three downloaded subjects | Machine-readable receipts bind repo, workflow, event SHA/ref and bytes; self-hosted provenance denied. |
| `bilingual-docs-threat-limitations-parity` | `python -m unittest tests.threat.test_required_claims tests.repository.test_policy -v` plus one human RU/EN comparison | Claims, threat boundaries and known limitations are semantically equivalent. |

## 14. Physical mobile commands

Before device work, the candidate TSVALPHA schema-2 core must be exposed through
an exact-source, locked native test harness. The existing TVSPIKE0 adapters are
not that harness; until the new harness is reviewed, these rows remain BLOCKED.
With the approved harness in place, capture the following without device IDs:

```powershell
adb version
adb devices
adb shell getprop ro.build.version.release
adb shell getprop ro.build.fingerprint
adb shell cat /proc/meminfo
adb push crates/tessaveil-core/tests/fixtures/tsvalpha-schema2.hex /data/local/tmp/tsvalpha-schema2.hex
adb shell sha256sum /data/local/tmp/tsvalpha-schema2.hex
adb shell '<approved-harness> --fixture /data/local/tmp/tsvalpha-schema2.hex --runs 10 --json /data/local/tmp/result.json'
adb pull /data/local/tmp/result.json (Join-Path $EvidenceRoot 'android-result.json')
```

Record only a sanitized model class, SoC/RAM class, Android build and thermal
state; redact serial/device identifiers from `adb devices` and fingerprint output.
The approved harness must output each wall time, peak process RSS, OOM/result,
normalized-test status and KDF/rejection status without outputting password bytes.

On the recorded Mac, `xcodebuild -version` and the two `xcrun` commands in section
11 must match the pin. Build the reviewed device target with `xcodebuild` using a
locked project and a generic device destination, then run it on each separately
named physical device class through Xcode's native test plan. Capture Instruments
Allocations/VM Tracker and Energy/thermal exports for ten cold opens. Do not place
device UDIDs, signing tokens or developer-account paths in the receipt.

## 15. Bounded interruption and rollback harness

No step here prepares or formats media. The owner must first name the exact
dedicated empty physical device and separately authorize destructive testing.
The operator records its sanitized class/capacity/controller and verifies the
already prepared filesystem. Any ambiguity stops the run.

For process interruption, start Process Monitor 4.11 before Tessaveil and filter
the exact PID and dedicated vault directory. In a disposable child PowerShell,
terminate only the recorded Tessaveil PID with `Stop-Process -Id <candidate-pid>
-Force` at the boundary sequence `AfterCreate, AfterWrite, AfterFlush, AfterVerify, BeforeReplace, AfterReplace`;
also run `None` as the uninterrupted
control. Repeat each point five times on each filesystem. A 60-second boundary
timeout is BLOCKED. Reconnect/reopen without repair, hash all surviving allowed
files, authenticate them through the exact candidate, and preserve the raw PML.

Hardware power interruption uses the same boundaries and repetitions but only an
owner-approved isolated controller operated by a second person; never power-cycle
the development workstation. Capture controller timestamp, boundary event,
filesystem health and post-restore hashes. This document provides no disk, mount,
partition or formatting command.

For rollback/version comparison, create two clearly labelled synthetic vault
versions A/B and an identical A copy. Confirm old authentic A still opens,
identical copies add no different-table signal, and comparison of decrypted A/B
exposes invariant cells. This observation must remain a documented limitation.

## 16. Exact trace and hosted-provenance commands

On each clean Windows target, use an elevated capture operator only to start the
OS trace; run Tessaveil itself from the standard non-admin account. First record
tool/binary versions and hashes. Start before process creation:

```powershell
pktmon start --capture --comp nics --pkt-size 0 --file-name (Join-Path $EvidenceRoot 'network.etl')
Procmon64.exe /AcceptEula /Quiet /Minimized /BackingFile (Join-Path $EvidenceRoot 'procmon.pml')
```

Run the full workflow, exit Tessaveil, wait 30 seconds, then stop capture:

```powershell
Procmon64.exe /Terminate
pktmon stop
pktmon etl2pcap (Join-Path $EvidenceRoot 'network.etl') --out (Join-Path $EvidenceRoot 'network.pcapng')
Get-FileHash -Algorithm SHA256 (Join-Path $EvidenceRoot 'procmon.pml')
Get-FileHash -Algorithm SHA256 (Join-Path $EvidenceRoot 'network.etl')
```

Preserve a `%TEMP%` recursive name/size/hash inventory immediately before launch
and after the quiet period. Review the unfiltered PML first, then export PID/path
views; a pre-supplied filter that drops events is not acceptable raw evidence.
Disconnected and connected-idle network captures are separate runs. A capture
tool which cannot run on the recorded OS build makes the relevant row BLOCKED.

For hosted evidence, the only accepted environment string is
`GitHub-hosted runner windows-2022`, and it is accepted only for `exact-sha-ci`
and `github-provenance`. It can never substitute for clean Windows, physical
mobile, removable-media, Narrator, audit or signing evidence. After
`gh run watch <run-id> --exit-status`, download to a new directory and run for
each of `runtime.zip`, `compliance.zip` and `release-decision.json`:

```powershell
gh attestation verify "downloaded-artifact/<subject>" --repo rbuzzz/tessaveil --signer-workflow "rbuzzz/tessaveil/.github/workflows/windows-alpha.yml" --source-digest $SourceSha --source-ref '<exact-event-ref>' --deny-self-hosted-runners --format json
```

Store each JSON output and its hash as evidence. The workflow's pinned checkout
must precede the repository `release_decision.py verify` call; an attestation job
without source checkout is FAIL.

## 17. Final decision

Run the strict release-decision validator against the materialized report and exact
runtime/compliance/EXE paths. Integrity may pass while the verdict remains NO-GO.
Run its separate real-data mode only after evidence owners have changed every mandatory
row to `pass`. If even one row is `blocked` or `fail`, the only permitted verdict is
**NO-GO для реальных данных** and packaging must remain conspicuously unsigned,
synthetic-only and non-stable.
