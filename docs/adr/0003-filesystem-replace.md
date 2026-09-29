# ADR 0003 — Scope filesystem save claims to measured targets

Date: 2026-09-29. Status: accepted research policy; production implementation and
removable-media/release guarantees remain unapproved / **NO-GO**.

## Decision

Use adjacent complete encrypted images, flush, reopen and authenticate before
same-directory replacement on a target whose particular filesystem/device/API
combination has passed its required interruption matrix. Never silently fall back
to in-place overwrite or deleting the destination before renaming. Failures must
be surfaced; production handling of all replacement error modes needs further
evidence and cannot inherit a blanket old-file-preservation claim from this probe.

The [local NTFS matrix](../../reports/spikes/filesystem-matrix.md) passed six
named process interruption boundaries plus a normal control on Windows 11 Pro
x64 25H2 build 26200.9457, PowerShell 7.6.5 / .NET 10.0.11. It establishes only
old-or-new authenticated 4140-byte image survival at those boundaries for that
fixed development volume and `File.Replace` path. It does not establish atomicity
inside the system call, power-loss durability or clean-Windows release readiness.

Physical removable NTFS and removable exFAT are independent required rows. Their
exact [Task 4](../../reports/spikes/equipment-availability.md) blocker is:

> Zero USB/SD disks and zero removable volumes were visible. No pre-provisioned empty physical media or separately safe NTFS and exFAT test paths were supplied.

Both remain unapproved / NO-GO. Virtual disks and local NTFS cannot clear them.
The disposable probe currently refuses removable volumes altogether; its target
allowlist may be extended only as a separately reviewed change with explicit
physical media provenance and safe empty test paths. Do not format/mount devices
to make this research gate pass.

FAT32, network shares, cloud-sync folders and untested filesystems have no
atomicity promise and no silent in-place update. Future product behavior is
read-only or explicit Save As to a verified target. These are requirements, not
implemented product features or available production support.

## Security and consequences

The temporary image has only an open technical header plus authenticated
ciphertext. Reopen verification must authenticate, not merely compare an
unkeyed checksum or length. The synthetic AES-GCM research fixture uses a public
test key and is explicitly separate from the provisional product format/KDF.

Incomplete temporary files must never appear as valid empty vaults. Complete
temporary images can preserve another table version, enabling cross-version
comparison after password disclosure; full re-randomization does not remove the
risk. Cleanup is best effort without secure erasure, and no rollback detection
is promised. Directory guards reduce accidental wrong-target writes but cannot
defeat a hostile OS or same-privilege adversary.

Before any product filesystem claim, obtain the required physical matrix and
resolve API error recovery, power-loss/device behavior and release gates. Task 7
may complete as honest research while removable guarantees and Windows release
readiness remain **NO-GO**.
