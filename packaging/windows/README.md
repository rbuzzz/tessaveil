# Windows alpha packaging

Unsigned engineering alpha; synthetic data only. Not RC/stable. No Authenticode,
real funds or final format/KDF/migration promise. Windows release/freeze: NO-GO.

Use an external ASCII `$ToolchainRoot`, a clean exact-SHA checkout and a NEW
external `$OutputRoot`. The tool/source identities and SHA-256 hashes are in
`toolchains.json`, `runtime-sources.json`, `requirements.lock` and Cargo.lock.
`bootstrap.ps1 -ToolchainRoot $ToolchainRoot` provisions a fresh root; existing
pinned tools may instead be reused. Never copy toolchains/build caches into Git.

From the repository root with the variables explicitly assigned:

```powershell
& packaging/windows/build.ps1 -ToolchainRoot $ToolchainRoot
$SourceSha = (git rev-parse HEAD).Trim()
& packaging/windows/gate.ps1 -ToolchainRoot $ToolchainRoot -SourceSha $SourceSha -OutputRoot $OutputRoot
& "$ToolchainRoot/python/python.exe" packaging/windows/verify.py --runtime "$OutputRoot/runtime.zip" --compliance "$OutputRoot/compliance.zip" --source-sha $SourceSha --distribution
```

For the complete CI-equivalent checks, `ci.ps1` takes ToolchainRoot and SourceSha
and creates the new `$ToolchainRoot/alpha-output`. It runs root Rust checks,
doctests, all discovered Python tests, generators/scanners, native E2E and the gate.
The gate requires a usable interactive Windows desktop; unavailable headful smoke
is a failure, never a skip. It rebuilds modified Qt from the staged source, relinks
the unchanged objects, checks the marker in the actual EXE and observes that app.

The independent verifier needs Python 3.12 plus the hash-locked requirements and
this repository checked out at the expected SHA. The provisioned Python includes
both repository and packaging module search paths. It unpacks and audits both
archives without executing their contents. Its committed exact compliance member
inventory is deliberately fail-closed; dependency/configuration changes require
reviewing and updating that inventory, notices and source bindings together.

The SBOM is checked for exact content, not just schema validity. Expected identities,
licenses and the complete Cargo graph are reconstructed from Cargo.lock and the
reviewed `sbom-source-inventory.json`; runtime packages use the pinned rust-src lock,
Qt records come from the complete hash-verified source ZIP, dictionary metadata from
the catalogue, and system imports from the actual EXE. The application root binds
the source SHA and EXE hash and connects every source-inventory component (including
explicitly scoped non-linked/dev/build entries). No expectation is read from the SBOM.
The producer compares fresh `cargo metadata --locked --offline` and hash-verified
runtime crate manifests with the source inventory before packaging. To review a
dependency change, `sbom.py --toolchain-root $ToolchainRoot` prints a new inventory;
`--check` verifies the committed one. Inventory updates require source review.

Primary and modified-Qt observations bind source SHA and EXE SHA-256 captured before
and after the UIA run. Both require masking, keyboard focus, open/close/reopen/lock,
authentication, the two password getter/setter observations and a module inventory.
After final audit the gate also runs actual-archive mutation tests with recomputed
manifests: absent/substituted component families, versions/licenses/checksums/graph
and empty/false/stale observations must all be rejected. These tests require actual
Windows artifacts and are explicitly skipped only in the earlier generic Python run.

`prepare.py --analysis-only` is diagnostic: dirty-tree archives remain analysis
only. Only successful finalization writes `GATE-PASS.json` and candidate ZIPs.
Never distribute analysis archives, the runtime alone, or a failed candidate.
Keep the complete source/compliance ZIP alongside the runtime ZIP. ZIP metadata
is deterministic for identical inputs; byte-identical compiler outputs across
hosts are not established. There is no release/tag/installer/update operation.

Local hashes and relink receipts are not provenance. Only the separate pinned
official GitHub attestation job can establish the CI artifact's provenance; its
permission failure is visible and must not be waived into a success claim.
