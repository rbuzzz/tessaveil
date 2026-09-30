# Equipment and clean-environment availability — 2026-09-29

This is a read-only inventory of resources already connected or explicitly configured in the current development environment. `blocked` means access and the required provenance have not been demonstrated; it does not mean such equipment does not exist elsewhere. No safe physical test path or device identifier is approved by this inventory.

| Environment / device class | Owner | Access method | Verified (UTC) | Status | Evidence or exact blocker | Dependent gate |
| --- | --- | --- | --- | --- | --- | --- |
| clean Windows 10 22H2 x64 | Unassigned | No verified clean target access | 2026-09-29 | blocked | No Windows 10 target or clean-image provenance was supplied; local host is Windows 11 development OS. | Task 5 clean Windows 10 launch, runtime, packaging, and release evidence: BLOCKED |
| clean Windows 11 x64 | Unassigned | No verified clean target access | 2026-09-29 | blocked | Local Windows 11 Pro x64 build 26200 is a development host; no clean target provenance or separate access was supplied. Hyper-V VM enumeration was unavailable, so no configured clean VM could be verified. | Task 5 clean Windows 11 launch, runtime, packaging, and release evidence: BLOCKED |
| physical arm64 Android 4 GiB lower-bound | Unassigned | No verified physical-device access | 2026-09-29 | blocked | No present portable-device entry; adb unavailable. No physical device identity, arm64 architecture, or 4 GiB RAM evidence was supplied. | Task 6 lower-bound Android vault-open and Argon2id measurements: BLOCKED |
| current mid-range physical Android | Unassigned | No verified physical-device access | 2026-09-29 | blocked | No present portable-device entry; adb unavailable. No current mid-range physical Android model or access evidence was supplied. | Task 6 current Android vault-open and Argon2id measurements: BLOCKED |
| physical iPhone 11/A13/4 GiB-class lower-bound | Unassigned | No verified physical-device access | 2026-09-29 | blocked | No present portable-device entry and no accessible Mac/Xcode host; physical iPhone class and access were not supplied. | Task 6 lower-bound iPhone vault-open and Argon2id measurements: BLOCKED |
| current physical iPhone | Unassigned | No verified physical-device access | 2026-09-29 | blocked | No present portable-device entry and no accessible Mac/Xcode host; current physical iPhone class and access were not supplied. | Task 6 current iPhone vault-open and Argon2id measurements: BLOCKED |
| Mac/Xcode host | Unassigned | No verified Mac host access | 2026-09-29 | blocked | Current host is Windows; local Xcode command-line tools are absent and no configured Mac/Xcode host access was supplied. | Task 6 iOS build, deployment, and physical measurement evidence: BLOCKED |
| pre-provisioned empty removable device for NTFS and exFAT | Unassigned | No verified removable test-media access | 2026-09-29 | blocked | Zero USB/SD disks and zero removable volumes were visible. No pre-provisioned empty physical media or separately safe NTFS and exFAT test paths were supplied. | Task 7 removable NTFS and removable exFAT interruption/atomicity evidence: BLOCKED |

## Independent gate decisions

- Task 5 — Windows stack selection and release evidence: NO-GO. Neither clean Windows 10 22H2 x64 nor clean Windows 11 x64 access and provenance is verified. Candidate build work may proceed, but stack selection and clean-machine release claims require both target results.
- Task 6 — Vault-format/KDF freeze: NO-GO. The required physical Android and iPhone classes and Mac/Xcode access are unverified. Synthetic vectors and safe build work may proceed, but physical vault-open and Argon2id measurements are required before freezing the format or KDF profile.
- Task 7 — Removable NTFS/exFAT atomicity claims: NO-GO. No pre-provisioned empty physical removable medium or safe separate NTFS and exFAT test paths are verified. Local NTFS work may proceed, but removable-media guarantees require interruption results on each physical filesystem.

## Read-only discovery

- Queried the local operating-system class and version: Windows 11 Pro, x64, build 26200. This establishes only the development host, not a clean Windows target.
- Queried Hyper-V command availability and configured-VM enumeration: the command exists, but enumeration was unavailable. VirtualBox and VMware command tools were absent. Tool presence is not clean-machine evidence.
- Checked for adb and counted present portable-device entries without recording identifiers: adb absent; zero present portable-device entries. This does not prove the absence of equipment outside this host.
- Checked local Xcode command availability: neither `xcodebuild` nor `xcrun` was present. No configured Mac access was provided.
- Counted USB/SD disks and removable volumes without recording identifiers: zero of each, including zero removable NTFS and exFAT volumes.

No device farm, simulator, hosted runner, virtual disk, or development host was substituted for a physical, removable, or clean target. No device was mounted, formatted, or written. Safe source, build, and synthetic-vector work may continue, but Task 5 clean-Windows claims, Task 6 physical-mobile/format-freeze claims, and Task 7 removable-filesystem atomicity claims remain unapproved until the listed access and provenance are supplied and their tests pass.
