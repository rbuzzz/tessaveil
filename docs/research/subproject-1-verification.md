# First research subproject verification — Task 18

Verified UTC: 2026-09-29. Research completeness: COMPLETE with evidenced terminal
blockers. Windows release readiness: NO-GO. Vault-format/KDF freeze: NO-GO.
Production implementation, Figma production work, release and signing are not
authorized by this research result.

## Commit identity and reproducible binding

Audited input/base commit: `f0f70f738ee3cdd6c3a9052358e8e8d10374218c`.
Repository: `rbuzzz/tessaveil`; branch: `feature/tessaveil-research-foundation`.
Task 18 adds the final gates to that input. The candidate commit cannot contain
its own hash. Therefore the exact candidate is supplied by CI as `GITHUB_SHA`,
printed by `python -m tools.research_gate --candidate-sha "$GITHUB_SHA"`, checked
against checkout HEAD and a clean tracked tree, and required to descend from the
audited input. Full checkout history is mandatory for that ancestry check.
A PR merge candidate has its own SHA; it is never mislabeled as the branch SHA.

The controller must record the final exact branch candidate and successful
mandatory GitHub run externally after review/push. This committed document does
not claim that its own future CI run already succeeded. Input evidence hashes
below bind the report to the reviewed reports/ADRs/license source; exact catalogue
CLI exit/output and the complete, untruncated findings are recomputed in CI.
An unrelated exception, stderr output, missing evidence or changed blocker fails
the report check, even if another failure also returns exit code 1.

## Local verification and scope

The final task log records commands and counts. The complete Python run includes
schema/Python parity, positive discovery, threat claims, spike-report contracts,
sensitive-material scanning and the new report/notices regression cases.
Development host: Windows 11 Pro x64 build 26200, PowerShell 7.6.5, Python 3.14.2.
GitHub independently executes Python 3.12; the development host is not clean Windows.

| Command / gate | Observed result and limitation |
| --- | --- |
| `python -m py_compile tools/sensitive_material.py tools/notices.py tools/research_gate.py` | PASS; syntax only |
| `python -m unittest discover -s tests -p "test_*.py" -v` | Initial run exposed the old generator test's link allowlist; extended only for the two new handoff paths and verified both target files exist |
| `TESSAVEIL_RUN_FILESYSTEM_PROBE=1 python tools/run_tests.py` | PASS, 192 cases in 361.728s, one unavailable Windows directory-symlink case; native filesystem cases enabled |
| `python -m tools.catalog.cli validate --root . --require-terminal` | PASS, 0 errors / 0 warnings; terminal blocked accepted as research |
| `python -m tools.catalog.cli generate --root . --check` | PASS; generated EN/RU docs exactly match |
| `python -m tools.notices --check` | PASS; exact generated notices and closed decisions for every bundled dictionary |
| `python -m tools.sensitive_material` | PASS; tracked text plus non-ignored new files; exact reviewed public vector hashes; fresh 5-case scanner rerun also covers the final OpenPGP header extension |
| `python -m tools.research_gate` | PASS as report consistency only; independent Windows release remains NO-GO |
| `python -m tools.catalog.cli validate --root . --require-release-ready` | Expected exit 1; 51 required catalogue blockers, complete findings below |
| `cargo fmt --manifest-path spikes/mobile/core/Cargo.toml --check` | PASS; isolated pinned Rust 1.90.0 |
| `cargo check --manifest-path spikes/mobile/core/Cargo.toml --locked --offline --all-targets` | PASS; Windows GNU host only |
| `cargo test --manifest-path spikes/mobile/core/Cargo.toml --locked --offline` | PASS, 2 unit + 2 independent crypto + 5 vector tests; 0 ignored |
| `pwsh -NoProfile -File spikes/windows/verify.ps1` | PASS discovery; no .NET/Qt/MSVC build prerequisites; Rust exists in its isolated Task 6 installation despite absence from global PATH |
| Task 6 Android/iOS build availability | BLOCKED: Java/Gradle/Android SDK/NDK and Mac/Xcode absent; wrappers remain source contracts, not native builds |
| `TESSAVEIL_RUN_FILESYSTEM_PROBE=1 python -m unittest tests.repository.test_filesystem_report -v` | PASS, 9 tests including the bounded local NTFS interruption harness; no physical-media claim |

Rust reused the isolated Task 6 homes and ASCII build-output workaround, with
process-local variables only. No new SDK, GUI framework, device farm, provider call,
paid generation, remote machine, formatted medium or production payload was used.

## Separate decisions and remaining blockers

All 819 required catalogue items have terminal evidence. The exact 51 blocked
requirements are below; documented profiles remain nonselectable, and only verified
profiles are future candidates. Research completion never upgrades a profile.

The [equipment inventory](../../reports/spikes/equipment-availability.md) still
blocks both clean Windows classes, both physical Android classes, both physical
iPhone classes, Mac/Xcode and physical removable NTFS/exFAT. The inventory's exact
reasons are repeated below; the owner supplied no new target access in Task 18.

- [Desktop ADR](../adr/0001-desktop-stack.md): provisional/blocked, no selected
  winner. The three GUI candidates are source contracts; packaging, one-EXE,
  static linkage, dependency/TEMP inventory, accessibility and scores remain
  unmeasured. Safe isolated Rust success does not close GUI build/clean-host gates.
- [KDF ADR](../adr/0002-kdf-envelope-bounds.md): format and KDF freeze remain NO-GO.
  Keep provisional 64 MiB / 3 / 4 and absolute bounds unchanged. Native wrapper
  builds, native NFC parity, repeated physical timings, memory/OOM and thermal
  evidence are still absent for every required class.
- [Filesystem ADR](../adr/0003-filesystem-replace.md): only bounded process-death
  evidence on the observed fixed local NTFS/API is supported. No power-loss,
  hostile-OS, removable NTFS/exFAT, FAT32, network-share or sync-folder atomicity
  promise follows. The harness's exact synthetic files and owned empty directories
  were cleaned by the harness; no user content was removed.
- External security audit, complete future binary SBOM/dependency licensing,
  SignPath Foundation acceptance, signing roles and stable-release approval remain
  unresolved. There is no release binary or deployment for this desktop project.
  Independent test implementations and a heuristic secret scan are not an audit.

## License and sensitive-material closure

`THIRD_PARTY_NOTICES` is generated from the preserved full upstream license texts
in `third-party-notices-source.txt` and the sorted bundled-dictionary catalogue.
Every distributed list has its path, count, hash, source/revision, attribution,
license source, decision evidence and allowed/compatible decisions in that index.
Any pending/nonpositive bundled decision or catalogue error fails generation.
The original license text block is retained, not replaced by SPDX labels.

Electrum v1 and Zano rights remain unclear/pending and are NOT BUNDLED. This is
a terminal exclusion decision, not clearance. Development-only Cargo dependencies
are not vendored or shipped; their future binary distribution review remains
pending exactly as the Task 6 dependency inventory says. No legal or Foundation
acceptance is inferred from local component compatibility.

The scanner always checks private-key headers, GitHub/Figma token forms and
personal absolute paths, without printing matched values. Mnemonic runs (including
Unicode decomposition and JSON arrays) and seed/index JSON fixtures need review.
Only the five existing public projection files at exact reviewed SHA-256 values
bypass vector/mnemonic heuristics; source provenance is in their batch reports.
Exact catalogue-validated dictionary byte files are word lists, not phrase fixtures.
The two binary exceptions are exact-hash synthetic authenticated probes, not wallets.
Arbitrary binary files or changed exceptions fail. This bounded heuristic does not
detect every encoding, encrypted credential or arbitrary secret; human review remains
required. Tests construct fake patterns in memory rather than commit fake tokens.

## CI actions and promotion boundary

Official upstream releases were checked via GitHub release/tag APIs and the pinned
`action.yml` files on the verification date:

- [actions/checkout v7.0.1](https://github.com/actions/checkout/releases/tag/v7.0.1):
  `3d3c42e5aac5ba805825da76410c181273ba90b1`, `runs.using: node24`.
- [actions/setup-python v7.0.0](https://github.com/actions/setup-python/releases/tag/v7.0.0):
  `5fda3b95a4ea91299a34e894583c3862153e4b97`, `runs.using: node24`.

Full SHA pinning is retained; checkout credentials are not persisted.
Mandatory jobs: `validate`, `sensitive-material`, `release-readiness-report`,
`rust-host-evidence`. The release report job intentionally accepts an exactly
recorded NO-GO; it grants no release permission. A future promotion workflow MUST
invoke `python -m tools.catalog.cli validate --root . --require-release-ready`
directly and require exit 0, plus independently satisfy physical/clean-machine,
format, filesystem, audit and signing gates. Changing acceptance criteria requires
an explicit owner decision; this task changes none.

## Machine-readable evidence contract

This is the sole JSON block consumed by the report verifier. Catalogue stdout
retains its bounded CLI presentation; `release_findings` contains all findings.

```json
{
  "audited_input_sha": "f0f70f738ee3cdd6c3a9052358e8e8d10374218c",
  "research_completeness": "COMPLETE",
  "windows_release": "NO-GO",
  "catalogue_release": {
    "exit_code": 1,
    "output": "error required-blocked dictionary-electrum-v1-en: required item remains blocked\nerror required-blocked dictionary-zano-en: required item remains blocked\nerror required-blocked scheme-cake-bip39-create: required item remains blocked\nerror required-blocked scheme-cake-bip39-import: required item remains blocked\nerror required-blocked scheme-cake-decred-bip39-12-24: required item remains blocked\nerror required-blocked scheme-cake-electrum-24: required item remains blocked\nerror required-blocked scheme-cake-electrum-import: required item remains blocked\nerror required-blocked scheme-cake-electrum-mweb-import: required item remains blocked\nerror required-blocked scheme-cake-monero-bip39-create: required item remains blocked\nerror required-blocked scheme-cake-monero-bip39-import: required item remains blocked\nerror required-blocked scheme-cake-monero-polyseed-offset-cs: required item remains blocked\nerror required-blocked scheme-cake-monero-polyseed-offset-en: required item remains blocked\nerror required-blocked scheme-cake-monero-polyseed-offset-es: required item remains blocked\nerror required-blocked scheme-cake-monero-polyseed-offset-fr: required item remains blocked\nerror required-blocked scheme-cake-monero-polyseed-offset-it: required item remains blocked\nerror required-blocked scheme-cake-monero-polyseed-offset-ja: required item remains blocked\nerror required-blocked scheme-cake-monero-polyseed-offset-ko: required item remains blocked\nerror required-blocked scheme-cake-monero-polyseed-offset-pt: required item remains blocked\nerror required-blocked scheme-cake-monero-polyseed-offset-zh-hans: required item remains blocked\nerror required-blocked scheme-cake-monero-polyseed-offset-zh-hant: required item remains blocked\nerror required-blocked scheme-cake-wownero-14-unresolved: required item remains blocked\nerror required-blocked scheme-cake-zano-bip39: required item remains blocked\nerror required-blocked scheme-cake-zcash-create: required item remains blocked\nerror required-blocked scheme-cake-zcash-import: required item remains blocked\nerror required-blocked scheme-cardano-hardware: required item remains blocked\n... 26 further findings omitted\nvalidation: 51 errors, 0 warnings\n",
    "status": "NO-GO"
  },
  "release_findings": [
    {
      "severity": "error",
      "code": "required-blocked",
      "location": "dictionary-electrum-v1-en",
      "message": "required item remains blocked"
    },
    {
      "severity": "error",
      "code": "required-blocked",
      "location": "dictionary-zano-en",
      "message": "required item remains blocked"
    },
    {
      "severity": "error",
      "code": "required-blocked",
      "location": "scheme-cake-bip39-create",
      "message": "required item remains blocked"
    },
    {
      "severity": "error",
      "code": "required-blocked",
      "location": "scheme-cake-bip39-import",
      "message": "required item remains blocked"
    },
    {
      "severity": "error",
      "code": "required-blocked",
      "location": "scheme-cake-decred-bip39-12-24",
      "message": "required item remains blocked"
    },
    {
      "severity": "error",
      "code": "required-blocked",
      "location": "scheme-cake-electrum-24",
      "message": "required item remains blocked"
    },
    {
      "severity": "error",
      "code": "required-blocked",
      "location": "scheme-cake-electrum-import",
      "message": "required item remains blocked"
    },
    {
      "severity": "error",
      "code": "required-blocked",
      "location": "scheme-cake-electrum-mweb-import",
      "message": "required item remains blocked"
    },
    {
      "severity": "error",
      "code": "required-blocked",
      "location": "scheme-cake-monero-bip39-create",
      "message": "required item remains blocked"
    },
    {
      "severity": "error",
      "code": "required-blocked",
      "location": "scheme-cake-monero-bip39-import",
      "message": "required item remains blocked"
    },
    {
      "severity": "error",
      "code": "required-blocked",
      "location": "scheme-cake-monero-polyseed-offset-cs",
      "message": "required item remains blocked"
    },
    {
      "severity": "error",
      "code": "required-blocked",
      "location": "scheme-cake-monero-polyseed-offset-en",
      "message": "required item remains blocked"
    },
    {
      "severity": "error",
      "code": "required-blocked",
      "location": "scheme-cake-monero-polyseed-offset-es",
      "message": "required item remains blocked"
    },
    {
      "severity": "error",
      "code": "required-blocked",
      "location": "scheme-cake-monero-polyseed-offset-fr",
      "message": "required item remains blocked"
    },
    {
      "severity": "error",
      "code": "required-blocked",
      "location": "scheme-cake-monero-polyseed-offset-it",
      "message": "required item remains blocked"
    },
    {
      "severity": "error",
      "code": "required-blocked",
      "location": "scheme-cake-monero-polyseed-offset-ja",
      "message": "required item remains blocked"
    },
    {
      "severity": "error",
      "code": "required-blocked",
      "location": "scheme-cake-monero-polyseed-offset-ko",
      "message": "required item remains blocked"
    },
    {
      "severity": "error",
      "code": "required-blocked",
      "location": "scheme-cake-monero-polyseed-offset-pt",
      "message": "required item remains blocked"
    },
    {
      "severity": "error",
      "code": "required-blocked",
      "location": "scheme-cake-monero-polyseed-offset-zh-hans",
      "message": "required item remains blocked"
    },
    {
      "severity": "error",
      "code": "required-blocked",
      "location": "scheme-cake-monero-polyseed-offset-zh-hant",
      "message": "required item remains blocked"
    },
    {
      "severity": "error",
      "code": "required-blocked",
      "location": "scheme-cake-wownero-14-unresolved",
      "message": "required item remains blocked"
    },
    {
      "severity": "error",
      "code": "required-blocked",
      "location": "scheme-cake-zano-bip39",
      "message": "required item remains blocked"
    },
    {
      "severity": "error",
      "code": "required-blocked",
      "location": "scheme-cake-zcash-create",
      "message": "required item remains blocked"
    },
    {
      "severity": "error",
      "code": "required-blocked",
      "location": "scheme-cake-zcash-import",
      "message": "required item remains blocked"
    },
    {
      "severity": "error",
      "code": "required-blocked",
      "location": "scheme-cardano-hardware",
      "message": "required item remains blocked"
    },
    {
      "severity": "error",
      "code": "required-blocked",
      "location": "scheme-electrum-v1",
      "message": "required item remains blocked"
    },
    {
      "severity": "error",
      "code": "required-blocked",
      "location": "scheme-tevador-14-unresolved",
      "message": "required item remains blocked"
    },
    {
      "severity": "error",
      "code": "required-blocked",
      "location": "scheme-zano-legacy-24",
      "message": "required item remains blocked"
    },
    {
      "severity": "error",
      "code": "required-blocked",
      "location": "scheme-zano-legacy-25",
      "message": "required item remains blocked"
    },
    {
      "severity": "error",
      "code": "required-blocked",
      "location": "scheme-zano-modern",
      "message": "required item remains blocked"
    },
    {
      "severity": "error",
      "code": "required-blocked",
      "location": "wallet-cake-wallet-decred-bip39",
      "message": "required item remains blocked"
    },
    {
      "severity": "error",
      "code": "required-blocked",
      "location": "wallet-cake-wallet-decred-bip39-create-ios",
      "message": "required item remains blocked"
    },
    {
      "severity": "error",
      "code": "required-blocked",
      "location": "wallet-cake-wallet-decred-bip39-group-android",
      "message": "required item remains blocked"
    },
    {
      "severity": "error",
      "code": "required-blocked",
      "location": "wallet-cake-wallet-decred-bip39-group-ios",
      "message": "required item remains blocked"
    },
    {
      "severity": "error",
      "code": "required-blocked",
      "location": "wallet-cake-wallet-decred-bip39-import-android",
      "message": "required item remains blocked"
    },
    {
      "severity": "error",
      "code": "required-blocked",
      "location": "wallet-cake-wallet-decred-bip39-import-ios",
      "message": "required item remains blocked"
    },
    {
      "severity": "error",
      "code": "required-blocked",
      "location": "wallet-cake-wallet-wownero-legacy14-export-android",
      "message": "required item remains blocked"
    },
    {
      "severity": "error",
      "code": "required-blocked",
      "location": "wallet-cake-wallet-wownero-legacy14-export-ios",
      "message": "required item remains blocked"
    },
    {
      "severity": "error",
      "code": "required-blocked",
      "location": "wallet-cake-wallet-wownero-legacy14-export-linux",
      "message": "required item remains blocked"
    },
    {
      "severity": "error",
      "code": "required-blocked",
      "location": "wallet-cake-wallet-wownero-legacy14-export-macos",
      "message": "required item remains blocked"
    },
    {
      "severity": "error",
      "code": "required-blocked",
      "location": "wallet-cake-wallet-zano-bip39",
      "message": "required item remains blocked"
    },
    {
      "severity": "error",
      "code": "required-blocked",
      "location": "wallet-cake-wallet-zano-bip39-create-ios",
      "message": "required item remains blocked"
    },
    {
      "severity": "error",
      "code": "required-blocked",
      "location": "wallet-cake-wallet-zano-bip39-group-android",
      "message": "required item remains blocked"
    },
    {
      "severity": "error",
      "code": "required-blocked",
      "location": "wallet-cake-wallet-zano-bip39-group-ios",
      "message": "required item remains blocked"
    },
    {
      "severity": "error",
      "code": "required-blocked",
      "location": "wallet-cake-wallet-zano-bip39-import-android",
      "message": "required item remains blocked"
    },
    {
      "severity": "error",
      "code": "required-blocked",
      "location": "wallet-cake-wallet-zano-bip39-import-ios",
      "message": "required item remains blocked"
    },
    {
      "severity": "error",
      "code": "required-blocked",
      "location": "wallet-defly",
      "message": "required item remains blocked"
    },
    {
      "severity": "error",
      "code": "required-blocked",
      "location": "wallet-electrum-v1-import",
      "message": "required item remains blocked"
    },
    {
      "severity": "error",
      "code": "required-blocked",
      "location": "wallet-eternl",
      "message": "required item remains blocked"
    },
    {
      "severity": "error",
      "code": "required-blocked",
      "location": "wallet-feather-tevador-import",
      "message": "required item remains blocked"
    },
    {
      "severity": "error",
      "code": "required-blocked",
      "location": "wallet-typhon",
      "message": "required item remains blocked"
    }
  ],
  "external_blockers": [
    {
      "environment": "clean Windows 10 22H2 x64",
      "reason": "No Windows 10 target or clean-image provenance was supplied; local host is Windows 11 development OS."
    },
    {
      "environment": "clean Windows 11 x64",
      "reason": "Local Windows 11 Pro x64 build 26200 is a development host; no clean target provenance or separate access was supplied. Hyper-V VM enumeration was unavailable, so no configured clean VM could be verified."
    },
    {
      "environment": "physical arm64 Android 4 GiB lower-bound",
      "reason": "No present portable-device entry; adb unavailable. No physical device identity, arm64 architecture, or 4 GiB RAM evidence was supplied."
    },
    {
      "environment": "current mid-range physical Android",
      "reason": "No present portable-device entry; adb unavailable. No current mid-range physical Android model or access evidence was supplied."
    },
    {
      "environment": "physical iPhone 11/A13/4 GiB-class lower-bound",
      "reason": "No present portable-device entry and no accessible Mac/Xcode host; physical iPhone class and access were not supplied."
    },
    {
      "environment": "current physical iPhone",
      "reason": "No present portable-device entry and no accessible Mac/Xcode host; current physical iPhone class and access were not supplied."
    },
    {
      "environment": "Mac/Xcode host",
      "reason": "Current host is Windows; local Xcode command-line tools are absent and no configured Mac/Xcode host access was supplied."
    },
    {
      "environment": "pre-provisioned empty removable device for NTFS and exFAT",
      "reason": "Zero USB/SD disks and zero removable volumes were visible. No pre-provisioned empty physical media or separately safe NTFS and exFAT test paths were supplied."
    }
  ],
  "evidence_sha256": {
    "docs/adr/0001-desktop-stack.md": "665407350b5d0898b4ef1f1c1393b4c1da2931b37d48131cea191cdddd54aed8",
    "docs/adr/0002-kdf-envelope-bounds.md": "57ead16d3d99229c4755e23b13bf2577ce4fdde32eea2ad6c1ee606856fadfd1",
    "docs/adr/0003-filesystem-replace.md": "5c488514db4fd63690b03dff5c80d9aa3cc8a1871097d5957f0b3402af734d09",
    "docs/research/third-party-notices-source.txt": "5751042ae297b653754b2621fd1bbf941cc7e3af75152ea15bfc9d372aa95045",
    "reports/spikes/equipment-availability.md": "9b7c1f4298ad347a282428cbf625d98a5c1da50e44fe022274c83839d97dc8e4",
    "reports/spikes/filesystem-matrix.md": "357659eed9466b34153874a069440d287a74e23d34fb64b4c60cf1727400e661",
    "reports/spikes/mobile-kdf.md": "23c3aabc2231a887419713b7fdac384a2e965444e8254ea81a3af21bd3460a1a",
    "reports/spikes/windows.md": "763f236b687fc4906f58047e38448085126d7f89e7f116d2400eb91bf22936cc"
  }
}
```
