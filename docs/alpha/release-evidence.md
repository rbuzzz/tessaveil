# Windows alpha packaging evidence — fail-closed engineering gate

Unsigned Windows engineering alpha, synthetic data only. Not RC/stable. No
Authenticode, no real funds, no final format/KDF/migration promise. Windows
release/freeze remains NO-GO. No GitHub Release, tag, installer or update channel.

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
for GitHub provenance. No GitHub run or successful attestation has occurred here.

Primary mechanism references: [GitHub artifact attestations](https://docs.github.com/en/actions/how-tos/secure-your-work/use-artifact-attestations/use-artifact-attestations)
and [Qt 6.8 licensing](https://doc.qt.io/qt-6.8/licensing.html).
