# Filesystem interruption matrix — 2026-09-29

Local NTFS passed the seven-row **process-boundary interruption** matrix below.
This is bounded research evidence, not power-loss durability, a removable-media
guarantee, or Windows release readiness. Removable NTFS/exFAT remain **NO-GO**.

| Filesystem / device class | Result and claim scope | Exact blocker / policy |
| --- | --- | --- |
| local NTFS | PASS: complete authenticated old-or-new image at all six injected process boundaries and normal control; only this development environment/API/image size | No power-loss, kernel crash, hardware-unplug, mid-system-call or general atomicity promise; research scope only |
| removable NTFS | unapproved / NO-GO | Zero USB/SD disks and zero removable volumes were visible. No pre-provisioned empty physical media or separately safe NTFS and exFAT test paths were supplied. |
| removable exFAT | unapproved / NO-GO | Zero USB/SD disks and zero removable volumes were visible. No pre-provisioned empty physical media or separately safe NTFS and exFAT test paths were supplied. |
| FAT32 | no atomicity promise | no silent in-place update; read-only or Save As to a separately verified target |
| network shares | no atomicity promise | no silent in-place update; read-only or Save As to a separately verified target |
| cloud-sync folders | no atomicity promise | no silent in-place update; read-only or Save As to a separately verified target |
| untested filesystems | no atomicity promise | no silent in-place update; read-only or Save As to a separately verified target |

Both removable blockers are copied verbatim from
[Task 4 equipment availability](equipment-availability.md). No removable medium
was touched. A virtual disk, emulator or fixed disk is not a substitute for
physical removable NTFS **and** exFAT evidence. Current probe authorization is
deliberately local-only; adding removable targets requires separately reviewed
safety/provenance work and those physical measurements.

## Exact observed environment and API

- UTC evidence: `2026-09-29T13:00:49Z`.
- Windows 11 Pro x64, 25H2, version `10.0.26200`, build `26200.9457`, development
  host. CIM identifies Windows 11; the legacy registry ProductName still says
  Windows 10 Pro and is not used to infer the OS edition.
- PowerShell `7.6.5`, `.NET 10.0.11`; fixed local volume, NTFS, healthy according
  to the read-only volume query. No serial number, username or private path is
  recorded. The target is a newly created unique empty Public test directory.
- `FileStream(CreateNew, Write, FileShare.None)`; temporary stream buffer 8192;
  4140-byte image; `Write`, `Flush(true)`, close and reopen, strict structure and
  AES-256-GCM verification; `System.IO.File.Replace(source, destination, null,
  ignoreMetadataErrors: false)`, the Windows `ReplaceFileW` API path.
- All paths are same-directory; there is no backup argument, in-place write,
  delete-before-rename fallback, mount, format or disk operation.
- The harness launches a hidden child for each row, checks exact exit code,
  reopens the surviving target in the parent and verifies authentication and
  SHA-256 identity against the old/new hashes emitted before interruption.
  `Environment.Exit(86)` does not run stream disposal/finally; the OS stays alive.

## Measured matrix

| Failure phase | Child exit | Surviving target | Target authentication | Temporary file after exit |
| --- | --- | --- | --- | --- |
| AfterCreate | 86 | old, 4140 bytes | PASS | 0 bytes, incomplete, not authenticated |
| AfterWrite | 86 | old, 4140 bytes | PASS | 0 bytes, buffered write not flushed, not authenticated |
| AfterFlush | 86 | old, 4140 bytes | PASS | 4140 bytes, new image authenticated |
| AfterVerify | 86 | old, 4140 bytes | PASS | 4140 bytes, new image authenticated |
| BeforeReplace | 86 | old, 4140 bytes | PASS | 4140 bytes, new image authenticated |
| AfterReplace | 86 | new, 4140 bytes | PASS | absent |
| None | 0 | new, 4140 bytes | PASS | absent |

The exact sanitized hashes and machine-readable rows are in
[`local-ntfs-evidence.json`](../../spikes/filesystems/local-ntfs-evidence.json).
Reproduction: `pwsh -NoProfile -NonInteractive -File
./spikes/filesystems/Test-ReplaceProbe.ps1`. Each run produces fresh new ciphertext
and hashes; the baseline fixture hash stays constant. Successful harness cleanup
removes only synthetic test files/links and their empty dedicated directories,
without recursive deletion or a secure-erasure claim.

The safe-path tests also refused a nonempty directory without changing its
sentinel and refused a real junction without writing through it. Negative image
tests rejected corruption in all envelope regions, truncated images and trailing
bytes. The repository test suite skips live filesystem execution unless explicitly
enabled; a skipped test is not new physical/environment evidence.

## Limits and failure handling

This matrix interrupts **between** operations; it does not interrupt inside
`ReplaceFileW`. `Flush(true)` requests buffer flushing, but does not demonstrate
storage-controller power-loss behavior, post-replace directory durability,
filesystem-filter behavior, concurrent readers/writers, disk-full/access-denied
recovery, other image sizes, Windows versions or hardware. An unexpected API
error fails the probe; no replacement fallback runs. ReplaceFileW error modes
require separate production recovery design, so a blanket promise that every
possible failed save leaves the old name untouched is not established here.

Temporary images contain a clear technical header and authenticated ciphertext,
never an open payload; interruptions may leave an incomplete image that must not
be treated as an empty valid vault. A complete temporary image can represent a
different table version. After master-password disclosure, comparing such
versions can expose invariant true words; full re-randomization does not remove
that risk. Best-effort temporary cleanup is not secure erasure. No rollback
detection is claimed.

The fixture uses public synthetic key material and AES-GCM solely to make
authentication meaningful for this filesystem probe. It neither freezes the
production envelope nor clears Task 6. **Windows release readiness: NO-GO.**

## Primary references

Verified 2026-09-29 for the APIs used: [.NET FileStream.Flush(Boolean)](https://learn.microsoft.com/en-us/dotnet/api/system.io.filestream.flush?view=net-10.0),
[Windows ReplaceFileW](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-replacefilew),
[Cloud Files sync-root query](https://learn.microsoft.com/en-us/windows/win32/api/cfapi/nf-cfapi-cfgetsyncrootinfobypath),
[Microsoft cloud-root error constant](https://microsoft.github.io/windows-docs-rs/doc/windows/Win32/Foundation/constant.ERROR_CLOUD_FILE_NOT_UNDER_SYNC_ROOT.html).
API documentation describes operations and error contracts; only the measured
rows above are experimental evidence.
