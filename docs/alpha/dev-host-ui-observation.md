# Development-host Windows candidate observation

Date: 2026-09-30. Reviewed source base:
`be2b9c9a1c2162952f319080cde33e267dc6a353`. Scope: Task 5 Windows
candidate workflows, native Qt Widgets and the real `tessaveil-core`.
**This is development-host evidence, not clean-Windows, Narrator, release, or
format/KDF-freeze approval.** All data was synthetic. No executable was
published or signed; the release decision remains NO-GO.

## Architecture and interface boundary

One Rust controller owns each open vault. Decrypted payload, keys, dictionary,
sheets and session state remain in the non-cloneable Rust owner. Qt keeps only
an opaque handle, bounded replies, transient masked entry text and individual
visible table-cell strings. It has no full-payload, phrase, order-key,
target-column, plaintext-serialization or row-history API.

ABI v1 retains its fixed C layouts, opcodes and reply bounds. Existing profile
opcode 29 gained append-only selectors 5 through 8 for platform, status and
minimum/maximum version. They project only already validated generated-catalog
data; generated data, selectability, schema 2, KDF and persistence are
unchanged. Rust and native tests check both layouts and bounded replies.

All input lengths are explicit and bounded. Invalid UTF-8, invalid lengths and
stale handles fail closed. Extern boundaries catch unwinding. Secret input is
cleared before the synchronous call, Rust wipes the bridge buffer on success
and failure, and C++ wipes its temporary buffers again. GUI, IME, framework and
OS copies remain best-effort rather than a forensic-erasure guarantee. No
secret is logged.

## Implemented candidate workflows

The focused Create and Open dialogs use native ciphertext pickers and expose a
read-only selected path. Create confirms a new password; Open accepts the
existing password. The workspace provides profile inspection, 10/36-column
sheets, add/rename/delete, Spin, reversible `Verified by me`, protection and
unlock, save, lock and close. It also provides bounded dialogs for backup,
restore with the old password, password rotation, custom dictionary selection
and replacement-dictionary selection. Backup is checked byte-for-byte. A denied
save preserves the dirty session and permits a later retry. All recovery flows
are covered with synthetic encrypted files. Successful Restore starts a fresh
inactivity window and synchronizes the encrypted locale before localized profile
details and their accessibility text are refreshed. Opening Add custom, Replace
dictionary or Delete first clears pending word/symbol/sheet-password input and
both acknowledgments. Cancellation or controller rejection preserves the vault
session and current sheet while keeping that transient input scrubbed.

The catalogue view provides a keyboard-operable search over all 733 profiles,
including unavailable entries, using product, platform, version interval,
status, mode, identifier and reason. Filtering never changes the exact profile
projection or makes an unavailable profile selectable. The dynamically selected
exact details and localized reason/guidance are also the current accessible name
and description rather than being masked by a static override. Selectable
profiles use controller-projected allowed row lengths rather than UI constants.
Reason codes are converted to bounded plain-language RU/EN guidance that states
why creation in Tessaveil is unavailable, directs verification to the exact mode
and version, and points to the original wallet's own backup/export process.
Unknown codes use a readable fail-safe explanation without displaying the
internal value.

Russian and English strings are centralized. Before a vault is available, the
locale is process-local, so Closed state and focused Create/Open dialogs use the
current choice without QSettings, registry or another persistent side channel.
Create writes a differing choice to the encrypted vault preference after the
vault exists; Open then synchronizes from that encrypted preference. The
system/light/dark theme choice remains process-only. Theme colors and the
stylesheet are semantic and window-local, including owned dialogs.
Dialog buttons, state labels and accessibility names change with the locale.
Authentication and corruption share the same outward message.

The actual Create dialog proactively states the minimum 15-Unicode-character
master-password rule in RU/EN. Restore states that the selected backup requires
the original/old password used when that backup was created; rotation continues
to warn that old backups and old passwords are not revoked. Native regressions
exercise the 4096-byte UTF-8 boundary for every new path, name, confirmation and
password field family. Oversized multilingual values fail closed while preserving
the required session/data state and clearing transient secret widgets.

Ordinary window deactivation clears pending secrets and acknowledgments, then
shows an opaque privacy cover without discarding the open session, dirty state,
table or file identity. Returning Active uncovers the same session and refreshes
the inactivity generation. A real Windows session lock, suspend/sleep or
inactivity timeout instead discards dirty state and locks the controller. Owned
sensitive dialogs are rejected before that transition. Manual close/lock offers
localized Save, Discard and Cancel. Before any foreground process-owned native
picker becomes usable, every pending secret and acknowledgment is scrubbed; the
read-only selected-path field and controller session/data are unchanged when the
picker is cancelled. The picker remains usable while a 50 ms ownership check
continues throughout Inactive.
Alt-Tab from that picker to an external process therefore closes the tracked
owned window, scrubs transient secrets and displays the privacy cover without
requiring a second application-state signal. Every return to Active rechecks
the timeout generation even when no cover was shown. The same bounded foreground
monitor remains active under the cover: if Win32 restores the exact main HWND
before Qt publishes `ApplicationActive`, it uncovers that HWND only and continues
watching so a subsequent external departure immediately re-covers.

Focus order is explicit. Password widgets expose password semantics and masked
values. The table is read-only, virtualized, content-sized and visually neutral
with respect to the target column. Guidance lives in a scrollable sidebar so
the table retains usable height at every tested scale.

## Reproduction and exact results

Pinned development toolchain: Rust/Cargo 1.90.0 GNU, Clang 20.1.8 with
LLVM-MinGW 20250709 UCRT x64, static QtBase 6.8.3, CMake 3.31.8, Ninja 1.12.1,
PowerShell 7.6.5 and Windows PowerShell 5.1 for UI Automation. Commands are run
from the repository with an external ASCII-only `$ToolchainRoot`:

```powershell
pwsh -NoProfile -File apps/tessaveil-windows/build.ps1 -ToolchainRoot $ToolchainRoot -Test

. ./spikes/windows/environment.ps1 -ToolchainRoot $ToolchainRoot
$env:CARGO_TARGET_DIR = "$ToolchainRoot/task5-target"
cargo fmt --all --check
cargo clippy --locked --all-targets -- -D warnings
cargo test --locked --all-targets
$env:RUSTDOCFLAGS = '-C link-self-contained=yes'
cargo test --workspace --doc --locked

python tools/run_tests.py
python tools/alpha_catalog.py --check
python -m tools.sensitive_material
python -m tools.history_sensitive_material --root .
```

Results on the development host:

- native candidate build and native workflow suite passed;
- the native suite passed again with `QT_ENABLE_HIGHDPI_SCALING=0` and
  `QT_SCALE_FACTOR` 1, 1.5 and 2;
- Rust formatting and warning-denying clippy passed;
- Rust all-targets tests passed 67/67; ownership doctests passed 2/2;
- Python discovered 249 tests and passed 249 with five documented
  environment-dependent skips in 396.063 seconds;
- catalogue consistency and both sensitive-material scanners passed with no
  findings.

The first doctest invocation omitted the established GNU Rust
`link-self-contained` rustdoc flag and therefore failed at link time on missing
Windows CRT/import libraries. Repeating the same doctests with the pinned flag
passed 2/2. This was an invocation/toolchain-environment error, not counted as a
passing product test or hidden by an unexamined rerun.

The final unstripped development artifact is 26,534,912 bytes. The exact hash
of the final local build is recorded in the ignored Task 5 evidence report;
static-link output is not treated as reproducible. Task 8 will create the
release manifest only after the final source SHA is selected. This artifact is
not a stable or published release.

## Live UI Automation and scaling

`apps/tessaveil-windows/tests/observe.ps1` launches the actual candidate,
binds observation to its process and closes only that PID. It drives the real
native `#32770` Open picker and Qt controls, then checks focused Open, read-only
path selection, successful fixture opening, 10-to-36-column navigation, real
lock, generic wrong-password handling, unlock and close.

Fresh runs at application scale factors 1, 1.5 and 2 all passed against the
same candidate hash. Each observed six distinct password roles, with password
semantics, masked reads and keyboard focus; native picker and full workflow
checks also passed. The observer keyboard-focuses the all-profile search, locates
an unavailable profile and verifies that its exact product/platform/version/
status/mode/reason and original-wallet guidance are dynamically exposed through
UI Automation. The 1280 by 720 logical client retained a table height of at least
150 pixels. These checks do not change Windows display settings and do not prove
cross-monitor behavior.

Fresh Task 5 captures and fixtures were kept outside the repository. The seven
checked-in PNGs under `docs/alpha/screenshots` are historical Task 4 evidence,
not claimed as captures of this Task 5 artifact. No real mnemonic, entered
secret, local user path or unrelated window was added to the repository.

No Figma file/node for Tessaveil was supplied. The unrelated Renderis design
was not accessed. The implementation follows the approved written focused-flow
direction; no pixel-perfect Figma comparison is claimed.

## Remaining gates and limitations

This observation does not establish clean Windows 10/11 launch, Narrator or a
complete assistive-technology audit, movement between physically differently
scaled monitors, transient `%TEMP%`/file-event absence, packet-level network
silence, physical Android/iPhone compatibility, removable-media durability,
independent audit, signing readiness or lawful Qt redistribution packaging.
The host clipboard limitation remains: shortcuts and application events are
covered, but native OS clipboard-content observation is unverified. Existing
host-injected modules noted by the stack spike also remain unresolved.

There is no application network, telemetry, update, provider-submit,
screenshot/export/print/import or clipboard feature. The UIA observer is a
separate development script. Static Qt publication still requires the verified
LGPLv3 corresponding-source/object/relinking/install-information bundle or
another lawful route. Until all explicit physical, packaging and signing gates
are completed or separately dispositioned, the Windows release and vault/KDF
freeze remain **NO-GO**.
