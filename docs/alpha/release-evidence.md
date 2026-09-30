# Windows alpha packaging evidence — fail-closed engineering gate

Unsigned Windows engineering alpha, synthetic data only. Not RC/stable. No
Authenticode, no real funds, no final format/KDF/migration promise. Windows
release/freeze remains NO-GO. No GitHub Release, tag, installer or update channel.

## Exact-SHA evidence ledger

The repository contains a working synthetic-only Windows engineering alpha, not
a production-ready application or permission to use real secrets/funds. The
following successful record belongs to a **predecessor branch artifact**, not to
the later documentation-fix commit or an unverified PR event/merge SHA.

| Evidence | Exact scope and result |
| --- | --- |
| Source | `4c3e9de5b0e7936edc030992584ae6cdd59493ed`, `refs/heads/feature/windows-alpha` |
| Hosted Windows run | [36691081137](https://github.com/rbuzzz/tessaveil/actions/runs/36691081137): build/upload and separate provenance jobs PASSED |
| Static-Qt alpha gate | Exact corresponding source, notices/licenses, application relink material, real modified-Qt rebuild/relink/smoke and independent distribution audit PASSED for this artifact |
| Official provenance | Pinned official GitHub attestation succeeded; both ZIPs separately passed strict `gh attestation verify` with repository, signer workflow, exact source digest/ref, standard SLSA predicate and `--deny-self-hosted-runners` enforced |
| Product release/freeze | **NO-GO**; alpha gate/provenance success is not Authenticode, a security audit or RC/stable approval |

The signer workflow was `rbuzzz/tessaveil/.github/workflows/windows-alpha.yml`.
Independently downloaded, hashed and distribution-verified hosted outputs:

| Item | Bytes | SHA-256 |
| --- | ---: | --- |
| runtime.zip | 26,662,567 | `ce0dd44acbb448e9938448f0e1bb158d63398f2af4839e8b5e552bae525ea83e` |
| compliance.zip | 94,570,940 | `e7298b56f9e06759c8df522309ae8d3f558cc90a32984d647c8bd4d0a7580536` |
| Tessaveil.exe inside runtime.zip | 26,347,520 | `1cdca1bb70e822f952d8a01ed8638ea3ee4f28dc6480e9f47e3648279e5dc0c8` |

Attestations cover the ZIP digests; the EXE is bound through the verified runtime
archive/manifest and receipt, not claimed as a separately attested subject.
Local b43e6d1-era outputs are separate local evidence, not these hosted artifacts.

## Current-candidate gate (separate from the ledger)

[PR #2](https://github.com/rbuzzz/tessaveil/pull/2) must be evaluated on its own
exact event/merge SHA. At the documentation check on **2026-09-30 10:34 UTC**,
[PR Windows run 36699910534](https://github.com/rbuzzz/tessaveil/actions/runs/36699910534)
was in progress. That is a timestamped observation, not a permanent pending status
or a claim that the PR run succeeded. Consult the linked run/current PR checks for
later results. This ledger records no successful build, artifact or attestation
for the subsequent documentation-fix commit; a predecessor result never transfers
to a new SHA. No merge/release permission is implied.

Clean Windows 10/11, physical Android/iPhone format/KDF compatibility, removable
NTFS/exFAT interruption and power loss, full process/file/network tracing, Narrator,
independent security audit and SignPath/Authenticode signing remain open. Final
format/KDF freeze and migration guarantees remain unapproved. See
[known limitations](known-limitations.md); all Windows release/freeze gates remain NO-GO.

## Gate mechanics and evidence boundaries

The Windows workflow checks out the exact event SHA (the merge SHA for a PR),
builds pinned QtBase 6.8.3 from its unmodified source archive, and builds the actual
Rust/Qt application. Root Rust formatting/lint/workspace tests/doctests, native
headful synthetic E2E, full discovered Python tests, generation and sensitive/history
checks precede the packaging gate. Generic Linux catalogue/mobile CI remains
research evidence and does not compile the Windows application.

The local gate is `packaging/windows/gate.ps1`, with explicit ToolchainRoot,
SourceSha and OutputRoot parameters. Existing external Qt/Rust tools may be reused;
packaging/windows/build.ps1 rebuilds application material with private-path
remapping. No local machine path is hardcoded in those scripts. The independent
archive verifier is `packaging/windows/verify.py --runtime ... --compliance ...
--source-sha ...`; `--distribution` additionally requires every compliance gate.
Analysis archives cannot be renamed into a distribution candidate.

The compliance exercise extracts the bundled exact Qt source, changes qVersion()
to a harmless diagnostic marker, rebuilds Qt and relinks unchanged application
objects. Marker probe, changed application digest, marker presence in that EXE,
and real synthetic application smoke are required. The primary EXE is built from
unmodified Qt. Corresponding library source is bundled, not just linked externally.

The workflow's mandatory gate refuses upload until every source, licensing,
relink and artifact check passes for its exact SHA. Analysis-only material is
local engineering evidence, not a released/attested candidate. Machine-readable
per-run evidence records the exact source SHA, dirty-tree status, EXE size/hash,
PE imports, runtime observation, SBOM and content-audit findings without secrets.
The actual link inputs are mapped to static archive members; MinGW objects are
bound to individual source files, and Rust std subdependencies to its exact
source lock. License texts are preserved and hashed, not inferred from names.
Known vendor build-prefix spans require exact supplier bytes and hashes; private
user/worktree paths remain forbidden. The shipped EXE is never patched to hide paths.

The independent verifier checks the original bytes, exhaustive manifests,
AMD64 PE imports/no Authenticode, source/configuration/notice/object bindings,
and relink proof. `GATE-PASS.json` exists only after final archives pass the
distribution-mode audit. Local execution cannot establish GitHub provenance or
clean consumer-Windows certification. It does not authorize RC/stable release.

Official GitHub attestations are wired after the successful artifact-producing
job using pinned `actions/attest`, with only contents-read, id-token-write and
attestations-write in that separate job. Unsupported repository/PR permissions
fail visibly. Locally authored manifests are checksums/evidence, never substituted
for GitHub provenance. The successful hosted run and strict verification above
establish provenance only for their exact recorded ZIPs/source SHA; they do not
turn a local receipt or a later unchecked candidate into GitHub-provenance evidence.

Primary mechanism references: [GitHub artifact attestations](https://docs.github.com/en/actions/how-tos/secure-your-work/use-artifact-attestations/use-artifact-attestations)
and [Qt 6.8 licensing](https://doc.qt.io/qt-6.8/licensing.html).
