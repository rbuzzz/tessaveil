# Tessaveil Registry and Threat Model Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the public, machine-verifiable Windows v1 mnemonic catalogue, licensing evidence, threat model, and disposable desktop/mobile/filesystem feasibility evidence required before Figma production work or vault-format freeze.

**Architecture:** Store primary-source-backed catalogue records as small JSON documents connected by stable IDs, execute their JSON Schemas with a pinned development-only CLI, validate cross-record semantics with dependency-free Python tooling, and generate human documentation deterministically from the same records. Keep all architecture, KDF, and filesystem probes under `spikes/`; they produce evidence and ADRs but no production application code.

**Tech Stack:** Git/GitHub Actions, Python 3.12 standard library and `unittest`, `check-jsonschema==0.38.2` as a development-only schema runner, JSON Schema 2020-12, Markdown, PowerShell 7, Rust stable for disposable FFI/KDF probes, and minimal pinned toolchains for Avalonia/NativeAOT, Slint, Qt 6, Android, and iOS.

**Spec:** `docs/superpowers/specs/2026-09-29-tessaveil-registry-threat-model-design.md` and `docs/superpowers/specs/2026-09-29-tessaveil-foundation-windows-v1-design.md`

## Global Constraints

- Execute in an isolated worktree on `feature/tessaveil-research-foundation`; preserve unrelated user files and never let an implementation or review agent modify `main`.
- Target the public repository `rbuzzz/tessaveil`; verify the authenticated GitHub owner, name availability, obvious same-category conflicts, and every publishable local history ref before creation.
- The controller alone pushes after a task review passes. Commits and pushes are separate commands, pushes are sequential, and mandatory GitHub CI must succeed for the exact feature-branch SHA or PR SHA before the next task.
- Integrate to `main` only after the complete branch review; no agent may push, merge, or edit shared manifests/generated documents concurrently.
- This plan produces research data, validators, documentation, and disposable probes only—no production vault implementation, product UI, Figma file, release binary, or mobile application.
- Use current primary sources, pin source revisions or product-version ranges, and record the UTC verification date. Import support alone is not proof that a wallet creates a mnemonic.
- Only `verified` profiles are future-selectable. Every required Windows v1 item must end as `verified`, `documented`, `blocked`, or `no-mnemonic-confirmed`; `historical` is an independent flag.
- A terminal `blocked` item is an acceptable, evidence-backed research result and does not make the research-completeness gate fail. It does keep the separate Windows release-readiness gate at `NO-GO` until the owner explicitly changes that acceptance criterion.
- Every bundled word list needs source-license, repository-redistribution, attribution, and SignPath Foundation compatibility decisions.
- Never commit a real seed phrase, funded key, user vault, token, credential, local user path, or generated example that could represent live funds.
- Existing sheets own immutable dictionary snapshots. A changed custom dictionary creates a new unverified sheet; no table state or “Verified by me” flag migrates.
- Threat documentation must cover comparison of different tables for the same phrase, including manual backups and interrupted-save temporary files; full re-randomization is not described as eliminating that leakage.
- The provisional KDF candidate is Argon2id 64 MiB, 3 iterations, parallelism 4. Absolute encoded bounds are 64–256 MiB, 3–6 iterations, parallelism 1–8, fixed 32-byte output, and 16-byte salt; format freeze waits for physical-device evidence.
- Password normalization is NFC UTF-8 inside the shared Rust boundary. Embedded NUL is rejected; native wrappers must not normalize independently.
- A temporary vault image contains a clear technical header and authenticated ciphertext, never an open payload.
- Do not format or erase a removable device, purchase a certificate/service, or start a paid device farm without explicit owner approval.
- Check availability of clean Windows 10/11 environments, required physical Android/iPhone classes, a Mac/Xcode host, and a pre-provisioned removable test device before risky probes or bulk catalogue research. Missing physical equipment is recorded as a concrete blocker and is never replaced by a simulator or Windows Server CI claim.
- No production deployment exists for this desktop project; GitHub publication is the only remote mutation in this plan.

## Review Focus

- Ambiguous or renamed wallet products must split into versioned profiles instead of inheriting a format by name; Task 15 adds a test that rejects overlapping unresolved identities.
- Unicode normalization can create duplicates or platform disagreement; Tasks 3 and 6 add collision and cross-platform byte-vector tests.
- A redistributable dictionary can still conflict with SignPath's OSS terms; Task 9 adds a gate that prevents `verified` status without both decisions.
- Oversized files, collections, word lists, or KDF fields can cause resource exhaustion before authentication; Tasks 3 and 6 test rejection before expensive allocation.
- Different saved tables for one phrase can reveal invariant words even after complete decoy refresh; Task 17 pins this warning and the no-reshuffle/no-automatic-migration rules.

---

## Planned File Structure

```text
.github/
  workflows/catalog-quality.yml       # Deterministic validation, tests, docs diff, and secret scan.
requirements-dev.txt                  # Pinned development-only JSON Schema runner.
tools/run_tests.py                    # Discovers tests and fails if the suite contains zero tests.
.gitattributes                         # UTF-8/LF and word-list text handling.
.gitignore                             # Build/probe outputs and local tooling only.
LICENSE                                # Apache-2.0 for original project code.
README.md                              # English project scope and security status.
README.ru.md                           # Russian project scope and security status.
CONTRIBUTING.md                        # Evidence and catalogue contribution workflow.
SECURITY.md                            # Private vulnerability reporting and audit status.
PRIVACY.md                             # No-transfer/offline privacy statement.
CODE_SIGNING_POLICY.md                 # SignPath roles, origin verification, and unsigned-RC rule.
THIRD_PARTY_NOTICES                    # Generated/maintained third-party attribution index.
catalog/
  schema/{dictionary,scheme,wallet,evidence,required-set}.schema.json
  required/windows-v1.json             # Exhaustive acceptance manifest.
  dictionaries/*.json                  # One dictionary revision per file.
  schemes/*.json                       # One mnemonic scheme/version per file.
  wallets/*.json                       # One product mode/version per file.
  evidence/*.json                      # One pinned primary-source item per file.
wordlists/<dictionary-id>/<revision>.txt
tools/catalog/
  __init__.py
  model.py                             # Typed immutable record structures.
  loader.py                            # Bounded JSON and UTF-8 loading.
  validator.py                         # Cross-record/domain/license checks.
  generator.py                         # Deterministic Markdown generation.
  cli.py                               # validate and generate entry points.
tests/
  __init__.py
  repository/__init__.py
  catalog/__init__.py
  threat/__init__.py
  repository/test_policy.py
  catalog/{fixtures,test_loader,test_validator,test_generator,test_required_set}.py
  threat/test_required_claims.py
docs/
  catalog.md
  catalog.ru.md
  research/{name-check,licensing,source-policy}.md
  research/batches/*.md
  adr/{0001-desktop-stack,0002-kdf-envelope-bounds,0003-filesystem-replace}.md
spikes/
  windows/{avalonia-nativeaot,slint,qt6,verify.ps1,README.md}
  mobile/{core,android,ios,vectors,README.md}
  filesystems/{ReplaceProbe.ps1,fixtures,README.md}
reports/
  spikes/{equipment-availability,windows,mobile-kdf,filesystem-matrix}.md
```

### Task 1: Repository trust foundation and public remote

**Files:**
- Create: `.gitattributes`
- Create: `.gitignore`
- Create: `LICENSE`
- Create: `README.md`
- Create: `README.ru.md`
- Create: `CONTRIBUTING.md`
- Create: `SECURITY.md`
- Create: `PRIVACY.md`
- Create: `CODE_SIGNING_POLICY.md`
- Create: `THIRD_PARTY_NOTICES`
- Create: `requirements-dev.txt`
- Create: `tools/run_tests.py`
- Create: `docs/research/name-check.md`
- Create: `tests/repository/test_policy.py`
- Create: `tests/__init__.py`
- Create: `tests/repository/__init__.py`
- Create: `.github/workflows/catalog-quality.yml`

**Interfaces:**
- Consumes: approved design documents and GitHub authentication for `rbuzzz`.
- Produces: public `origin`, repository policy files, a non-empty `unittest` CI gate, the pinned JSON Schema runner, and stable documentation paths used by later tasks.

- [ ] **Step 1: Write the repository-policy test**

Create `tests/repository/test_policy.py` with `RepositoryPolicyTests` asserting that every listed policy file exists, `LICENSE` contains `Apache License`, both READMEs contain `Security audit: not yet independently completed`, `PRIVACY.md` says the program transfers no information unless the user explicitly requests it, and `CODE_SIGNING_POLICY.md` states that unsigned RCs are never stable releases.

- [ ] **Step 2: Run the test and verify the empty repository fails**

Run: `python -m unittest tests.repository.test_policy -v`
Expected: FAIL because the required policy files do not exist.

- [ ] **Step 3: Create the repository and signing-policy documents**

Write the listed files with RU/EN scope, Apache-2.0 limited to original code, vulnerability contact instructions without inventing an email address, the SignPath Foundation publisher trade-off, required 2FA/reviewer/approver roles, and the `v0.1.0-rc.1` unsigned-pre-release rule. Add only local build/probe outputs to `.gitignore`; do not ignore catalogue evidence or word lists.

- [ ] **Step 4: Record the name check**

Use GitHub and current web results to record repository-name availability and obvious same-category conflicts in `docs/research/name-check.md`, with date and the statement that this is not legal or trademark clearance.

- [ ] **Step 5: Add the initial CI workflow**

Create `.github/workflows/catalog-quality.yml` for pushes to `main` and `feature/**` plus pull requests to `main`. Pin official actions to full commit SHAs, use Python 3.12, install `requirements-dev.txt`, and run `python tools/run_tests.py`. The runner must construct the discovered suite, fail before execution when `countTestCases() == 0`, print the discovered count, and return nonzero on any failure. Conditionally run `python -m tools.catalog.cli validate --root . --allow-incomplete-required` only when `tools/catalog/cli.py` exists. Generated-doc drift becomes mandatory after Task 8, and Task 18 replaces the temporary flag with separate terminal-research and release-readiness gates.

- [ ] **Step 6: Run the policy test**

Run: `python -m unittest tests.repository.test_policy -v`
Expected: PASS.

- [ ] **Step 7: Commit the foundation**

Run: `git add .gitattributes .gitignore .github LICENSE README.md README.ru.md CONTRIBUTING.md SECURITY.md PRIVACY.md CODE_SIGNING_POLICY.md THIRD_PARTY_NOTICES requirements-dev.txt tools/run_tests.py docs/research/name-check.md tests/__init__.py tests/repository/__init__.py tests/repository/test_policy.py`
Run: `git commit -m "chore: establish Tessaveil repository policies"`

- [ ] **Step 8: Hand repository publication to the controller**

The implementer does not publish. The controller verifies that the active owner is exactly `rbuzzz`, repeats the GitHub/web name check, confirms no remote exists, scans every branch/tag/remote-tracking ref that could be pushed for old product names, credentials, and local absolute user paths, and verifies the pre-cleanup bundle. Only then may the controller create `rbuzzz/tessaveil` and add `origin`.

- [ ] **Step 9: Controller push and exact-SHA CI**

The controller first pushes the cleaned baseline `main`, then separately pushes `feature/tessaveil-research-foundation`, opens a PR, and waits for CI on the exact feature-branch SHA. The implementer and reviewer never push. Expected: CI reports a positive discovered test count and succeeds for the exact local `HEAD`.

### Task 2: Catalogue schemas and exhaustive required-set manifest

**Files:**
- Create: `catalog/schema/dictionary.schema.json`
- Create: `catalog/schema/scheme.schema.json`
- Create: `catalog/schema/wallet.schema.json`
- Create: `catalog/schema/evidence.schema.json`
- Create: `catalog/schema/required-set.schema.json`
- Create: `catalog/required/windows-v1.json`
- Create: `tests/catalog/fixtures/valid-minimal/`
- Create: `tests/catalog/fixtures/invalid-schema/`
- Create: `tests/catalog/test_required_set.py`
- Create: `tests/catalog/test_schema_cli.py`
- Create: `tests/catalog/__init__.py`

**Interfaces:**
- Consumes: status/lifecycle definitions from the specs.
- Produces: JSON Schema 2020-12 field contracts executed by `check-jsonschema==0.38.2` and `windows-v1.json` IDs consumed by `load_catalog(root: Path) -> Catalog` and completeness validation.

- [ ] **Step 1: Write failing manifest-contract tests**

Add tests `test_required_manifest_contains_every_named_product`, `test_historical_is_not_a_support_status`, and `test_required_ids_are_unique`. Assert all names and networks from parent spec sections 8.3–8.4, exact statuses `verified|documented|blocked|no-mnemonic-confirmed`, and a separate Boolean `historical`.

- [ ] **Step 2: Run the targeted tests**

Run: `python -m unittest tests.catalog.test_required_set -v`
Expected: FAIL because schemas and manifest are absent.

- [ ] **Step 3: Define exact record fields**

Create the five schemas. Require `schema_version`, stable lowercase-kebab ID, bilingual display name where user-visible, pinned evidence IDs, ISO date, version interval, and status fields. Dictionary license data must include `spdx_or_name`, `source_url`, `attribution`, `repository_redistribution`, `signpath_compatible`, and `decision_evidence`.

- [ ] **Step 4: Create `windows-v1.json`**

List every required dictionary family, scheme, product/mode, and network from the specs. Give each requirement a stable ID and `record_ids` array; use empty arrays only as an explicit failing placeholder during research, never as a completed status.

- [ ] **Step 5: Add valid and invalid fixtures**

The valid fixture connects one synthetic dictionary, scheme, wallet, and evidence record. Invalid fixtures cover `historical` used as status, unknown fields, missing licensing decision, and duplicate required IDs.

Add `tests/catalog/test_schema_cli.py` to invoke the pinned `check-jsonschema` CLI against every valid and invalid fixture and assert the expected exit class. These same fixtures become the sole schema-conformance corpus consumed by the Python parity tests in Task 3; neither validator gets a private duplicate fixture set.

- [ ] **Step 6: Run tests and commit**

Run: `python -m unittest tests.catalog.test_required_set tests.catalog.test_schema_cli -v`
Expected: PASS.
Run: `git add catalog tests/catalog`
Run: `git commit -m "feat: define catalogue schemas and required set"`

### Task 3: Bounded catalogue loader and fail-closed validator

**Files:**
- Create: `tools/catalog/__init__.py`
- Create: `tools/catalog/model.py`
- Create: `tools/catalog/loader.py`
- Create: `tools/catalog/validator.py`
- Create: `tools/catalog/cli.py`
- Create: `tests/catalog/test_loader.py`
- Create: `tests/catalog/test_validator.py`
- Create: `tests/catalog/test_schema_parity.py`
- Create: `tests/catalog/fixtures/normalization-collision/`
- Create: `tests/catalog/fixtures/oversized/`

**Interfaces:**
- Consumes: schema files and required manifest from Task 2.
- Produces: `load_catalog(root: Path, limits: LoadLimits = DEFAULT_LIMITS) -> Catalog`, `validate_catalog(catalog: Catalog, require_terminal: bool = True, require_release_ready: bool = False) -> tuple[Finding, ...]`, and CLI exit code 0 only with no error findings. `--allow-incomplete-required` converts only missing required-record findings to warnings; it never relaxes malformed or dishonest existing records. `--require-terminal` accepts an evidenced terminal `blocked` status; `--require-release-ready` additionally rejects any required blocker.

- [ ] **Step 1: Write loader failure tests**

Test `load_catalog` rejects invalid UTF-8, duplicate JSON keys, files over 1 MiB, more than 10,000 records, strings over 16 KiB, word-list files over 16 MiB, and unknown mandatory schema versions before constructing the full catalogue.

- [ ] **Step 2: Write domain-validation failure tests**

Test broken IDs/references, unsupported statuses, missing pinned evidence, word count/SHA mismatch, normalization collisions, unsupported phrase lengths, unresolved required entries, and a `verified` record whose redistribution or SignPath decision is not `allowed/compatible`.

Add `tests/catalog/test_schema_parity.py`: parameterize over the exact Task 2 fixture corpus, execute `check-jsonschema` and the Python loader/validator for every fixture, and assert both classify each fixture identically. A new schema rule or Python rule is incomplete until the shared fixture makes this parity test pass.

- [ ] **Step 3: Run targeted tests**

Run: `python -m unittest tests.catalog.test_loader tests.catalog.test_validator tests.catalog.test_schema_parity -v`
Expected: FAIL because the interfaces do not exist.

- [ ] **Step 4: Implement immutable models and bounded loading**

Define frozen dataclasses `SourceRef`, `LicenseDecision`, `DictionaryRecord`, `SchemeRecord`, `WalletRecord`, `EvidenceRecord`, `RequiredItem`, `Catalog`, `LoadLimits`, and `Finding`. Parse JSON with duplicate-key detection; read sizes before decoding; never fetch URLs in loader or validator.

- [ ] **Step 5: Implement cross-record validation**

Use `unicodedata.normalize(record.normalization, word)` for collision checks, `hashlib.sha256` over exact word-list bytes, stable sorted findings, and fail-closed checks for every required-set reference and license decision.

- [ ] **Step 6: Implement the CLI**

Expose `python -m tools.catalog.cli validate --root . --require-terminal`, `python -m tools.catalog.cli validate --root . --require-release-ready`, and `python -m tools.catalog.cli generate --root . --check`. Validation first executes the JSON Schemas through the same pinned schema engine, then applies Python cross-record checks; it prints bounded one-line findings without word contents and returns nonzero on any error.

- [ ] **Step 7: Run tests and the validator**

Run: `python -m unittest tests.catalog.test_loader tests.catalog.test_validator tests.catalog.test_schema_parity -v`
Expected: PASS.
Run: `python -m tools.catalog.cli validate --root . --require-terminal`
Expected: FAIL only because mandatory research records are not yet populated; no crash or secret-like output.
Run: `python -m tools.catalog.cli validate --root . --allow-incomplete-required`
Expected: PASS with bounded warnings for missing required IDs.

- [ ] **Step 8: Commit**

Run: `git add tools/catalog tests/catalog`
Run: `git commit -m "feat: add fail-closed catalogue validation"`

### Task 4: Physical equipment and clean-environment availability gate

**Files:**
- Create: `reports/spikes/equipment-availability.md`
- Create: `tests/repository/test_equipment_availability.py`

**Interfaces:**
- Consumes: the exact physical and clean-environment requirements from both specifications.
- Produces: a dated availability matrix whose rows are `available` or evidence-backed `blocked`, plus exact safe paths/devices that Tasks 5–7 may use. A `blocked` row completes this inventory task but keeps its dependent technology, format, filesystem, or Windows release gate at `NO-GO`.

- [ ] **Step 1: Write the report-contract test**

Require separate rows for clean Windows 10 22H2 x64, clean Windows 11 x64, physical arm64 Android 4 GiB lower-bound, current mid-range physical Android, physical iPhone 11/A13/4 GiB-class lower-bound, current physical iPhone, a Mac/Xcode host, and a pre-provisioned empty removable device suitable for separately testing NTFS and exFAT. Require owner, access method, verification date, status, and blocker/evidence fields.

- [ ] **Step 2: Run the test and verify the missing report fails**

Run: `python -m unittest tests.repository.test_equipment_availability -v`
Expected: FAIL because the report is absent.

- [ ] **Step 3: Perform read-only availability discovery**

Inspect only already connected or explicitly configured local resources. Do not format media, install runtimes on a clean target, start a paid device farm, or treat a simulator, macOS runner, Windows Server runner, or the development computer as proof for a required physical/clean class. Record exact missing access rather than a generic “not tested.”

- [ ] **Step 4: Write the matrix and dependent-gate decisions**

For each unavailable row, name the affected Task 5, 6, or 7 acceptance evidence and mark it `BLOCKED`. For available rows, record only a non-secret device/environment identifier and the safe test boundary; never store a local absolute user path. State that safe code/build work may continue while the unavailable physical claim remains unapproved.

- [ ] **Step 5: Verify and commit**

Run: `python -m unittest tests.repository.test_equipment_availability -v`
Expected: PASS when every required row is honestly terminal, including `blocked`.
Commit: `docs: record feasibility equipment availability`.

### Task 5: Comparative Windows packaging spike and ADR

**Files:**
- Create: `spikes/windows/avalonia-nativeaot/`
- Create: `spikes/windows/slint/`
- Create: `spikes/windows/qt6/`
- Create: `spikes/windows/verify.ps1`
- Create: `spikes/windows/README.md`
- Create: `reports/spikes/windows.md`
- Create: `docs/adr/0001-desktop-stack.md`
- Create: `tests/repository/test_windows_spike_report.py`

**Interfaces:**
- Consumes: identical synthetic secure-input/dense-table probe requirements and the clean Windows rows from Task 4.
- Produces: evidence-based desktop-stack decision; only the ADR may promote Rust + Avalonia/NativeAOT from provisional to selected.

- [ ] **Step 1: Write report-contract tests**

Require all three candidates, exact toolchain versions, license notes, clean Windows 10/11 results or the exact Task 4 hardware blocker, single-EXE result, dependency inventory, `%TEMP%` before/after evidence, accessibility observations, binary size, startup measurement, and a scored decision. A blocked physical row is a valid research conclusion but must not select a stack or clear Windows release readiness.

- [ ] **Step 2: Build equivalent minimal probes**

Each probe shows one secure masked input, one virtualized 36-column synthetic table, keyboard focus, light/dark tokens, and one call across its proposed core boundary. No probe contains product cryptography or real seed data.

- [ ] **Step 3: Inspect packaging and dependencies**

For each release artifact record file count, PE imports/modules, native libraries, runtime prerequisites, and files created under `%TEMP%` during launch/use. For Avalonia, verify the Rust library is actually statically linked into the executable or document failure.

- [ ] **Step 4: Test clean Windows 10 and 11**

Run on clean x64 systems without development runtimes or admin rights. If Task 4 found them unavailable, complete only safe local build/inspection work, copy the exact blocker into the report/ADR, leave the stack provisional, and do not substitute Windows Server CI as proof.

- [ ] **Step 5: Write the comparison report and ADR**

Score portability, dependencies, accessibility, table performance, Figma fidelity, license obligations, maintenance, and future Rust/UniFFI reuse. Select a winner only from observed results.

- [ ] **Step 6: Verify and commit**

Run: `python -m unittest tests.repository.test_windows_spike_report -v`
Expected: PASS.
Commit: `docs: record Windows stack feasibility decision`.

### Task 6: Physical-device vault/KDF compatibility prototype

**Files:**
- Create: `spikes/mobile/core/Cargo.toml`
- Create: `spikes/mobile/core/src/lib.rs`
- Create: `spikes/mobile/core/tests/vectors.rs`
- Create: `spikes/mobile/android/`
- Create: `spikes/mobile/ios/`
- Create: `spikes/mobile/vectors/synthetic-vault-v0.bin`
- Create: `spikes/mobile/vectors/password-normalization.json`
- Create: `spikes/mobile/README.md`
- Create: `reports/spikes/mobile-kdf.md`
- Create: `docs/adr/0002-kdf-envelope-bounds.md`
- Create: `tests/repository/test_mobile_spike_report.py`

**Interfaces:**
- Consumes: provisional envelope fields, Argon2id bounds, NFC UTF-8 rules, synthetic-only data, and Task 4's physical Android/iPhone/Mac availability rows.
- Produces: `probe_open_vault(bytes: &[u8], password_utf8: &[u8]) -> ProbeResult`, shared test vectors, benchmark evidence, and a freeze/no-freeze ADR.

- [ ] **Step 1: Write Rust vector and bounds tests**

Test the provisional 64 MiB/3/4 tuple, absolute bounds 64–256 MiB/3–6/1–8, fixed 32-byte output, 16-byte salt, rejection before KDF for out-of-bounds values, distinct unsupported-profile error for non-allowlisted in-bound tuples, and corrupted authentication.

- [ ] **Step 2: Add password byte-equivalence vectors**

Cover composed/decomposed accents, combining marks, Cyrillic, Japanese, a non-BMP character, empty input, and embedded NUL. Assert Rust NFC output bytes are authoritative and embedded NUL is rejected.

- [ ] **Step 3: Build minimal Android and iOS wrappers**

Wrappers pass explicit-length Unicode input to the Rust boundary, open the same fixture, and display only success class, duration, and memory—not secret bytes. They do not normalize natively or persist passwords.

- [ ] **Step 4: Run physical Android measurements**

Measure on an arm64 4 GiB lower-bound device and a current mid-range physical device. Record model class, OS, wall time, peak memory, OOM/failure, and thermal observation for every candidate tuple. If either device is unavailable, record the exact Task 4 blocker and keep format freeze at `NO-GO`; an emulator may build the wrapper but cannot satisfy this step.

- [ ] **Step 5: Run physical iPhone measurements**

Measure on a physical iPhone 11/A13/4 GiB class as the provisional lower bound and on a current physical iPhone class. A simulator or macOS runner may verify compilation but cannot replace physical-device evidence. If a Mac/iPhone is unavailable, copy the exact Task 4 blocker, keep format freeze at `NO-GO`, and complete only the safe build/vector evidence that is actually available.

- [ ] **Step 6: Write report and ADR**

Freeze the profile only if every required class opens the fixture reliably and normalization bytes match. Otherwise record `NO-GO` and the explicit owner/security decision required; do not lower the profile automatically.

- [ ] **Step 7: Verify and commit**

Run Rust tests plus platform build checks and `python -m unittest tests.repository.test_mobile_spike_report -v`.
Commit: `docs: record mobile vault and KDF feasibility`.

### Task 7: Filesystem atomic-replacement probe

**Files:**
- Create: `spikes/filesystems/ReplaceProbe.ps1`
- Create: `spikes/filesystems/fixtures/header-and-ciphertext.bin`
- Create: `spikes/filesystems/README.md`
- Create: `reports/spikes/filesystem-matrix.md`
- Create: `docs/adr/0003-filesystem-replace.md`
- Create: `tests/repository/test_filesystem_report.py`

**Interfaces:**
- Consumes: adjacent-temp/write/flush/reopen/authenticate/replace sequence and Task 4's removable-device availability row.
- Produces: `Invoke-ReplaceProbe -Root <path> -FailurePhase <phase>` evidence and the supported-filesystem policy.

- [ ] **Step 1: Write report and fixture safety tests**

Assert the fixture exposes only magic/version/KDF/AEAD/length metadata and random ciphertext, report rows exist for local NTFS, removable NTFS, and removable exFAT, and no row claims atomicity without a passed interruption matrix.

- [ ] **Step 2: Implement the phase-controlled probe**

Support failure phases after temporary create, write, flush, reopen verification, and immediately before/after replace. Never target a workspace root or user directory; require a caller-supplied empty test directory and refuse broad paths.

- [ ] **Step 3: Run local NTFS tests**

Verify the old or new complete authenticated image survives every interruption and record exact Windows/API/filesystem details.

- [ ] **Step 4: Run removable NTFS and exFAT tests safely**

Use only a pre-provisioned empty removable test volume recorded by Task 4. Do not format a device as part of the script. If hardware is unavailable, copy the exact blocker into the report and leave removable NTFS/exFAT unapproved; a virtual disk does not replace physical removable-media evidence.

- [ ] **Step 5: Document unsupported locations**

State that FAT32, network shares, cloud-sync folders, and untested filesystems get no atomicity promise and must not receive silent in-place updates.

- [ ] **Step 6: Verify and commit**

Run: `python -m unittest tests.repository.test_filesystem_report -v`
Expected: PASS only for claims supported by the matrix.
Commit: `docs: define verified filesystem save guarantees`.

### Task 8: Deterministic catalogue documentation generator

**Files:**
- Create: `tools/catalog/generator.py`
- Create: `tests/catalog/test_generator.py`
- Create: `docs/catalog.md`
- Create: `docs/catalog.ru.md`
- Modify: `.github/workflows/catalog-quality.yml`

**Interfaces:**
- Consumes: `Catalog` and `Finding` from Task 3.
- Produces: `render_catalog(catalog: Catalog, locale: Literal["en", "ru"]) -> str` and deterministic generated docs.

- [ ] **Step 1: Write failing generator tests**

Test stable ordering, identical output across two runs, visible status/reason/evidence/version/license fields, shared-dictionary deduplication, `no-mnemonic-confirmed` guidance, and no word-list contents or local absolute paths.

- [ ] **Step 2: Run the tests**

Run: `python -m unittest tests.catalog.test_generator -v`
Expected: FAIL because `render_catalog` does not exist.

- [ ] **Step 3: Implement generation**

Generate an index by product/network and details by scheme/dictionary. Use stable ID sorting, LF output, a generated-file warning, and relative repository links. Do not perform network calls.

- [ ] **Step 4: Generate both documents and add CI drift check**

Run: `python -m tools.catalog.cli generate --root .`
Update CI to regenerate and fail on `git diff --exit-code -- docs/catalog.md docs/catalog.ru.md`.

- [ ] **Step 5: Verify and commit**

Run: `python -m unittest tests.catalog.test_generator -v`
Run: `python -m tools.catalog.cli generate --root . --check`
Expected: PASS and no diff.
Commit: `docs: generate catalogue documentation`
The controller pushes after review and waits for exact-SHA CI.

### Task 9: Evidence, licensing, and SignPath eligibility policy

**Files:**
- Create: `docs/research/source-policy.md`
- Create: `docs/research/licensing.md`
- Create: `tests/catalog/test_licensing.py`
- Modify: `CONTRIBUTING.md`
- Modify: `THIRD_PARTY_NOTICES`
- Modify: `CODE_SIGNING_POLICY.md`

**Interfaces:**
- Consumes: `LicenseDecision` and validator findings from Task 3.
- Produces: a four-level evidence policy and a mandatory SignPath-compatibility gate used by every research batch.

- [ ] **Step 1: Write failing policy tests**

Add `test_verified_requires_primary_evidence`, `test_verified_requires_redistribution_permission`, and `test_verified_requires_signpath_compatibility`. Include a dictionary that is redistributable but marked SignPath-incompatible and assert validation fails.

- [ ] **Step 2: Run tests and confirm failure**

Run: `python -m unittest tests.catalog.test_licensing -v`
Expected: FAIL until policy fields and checks are wired.

- [ ] **Step 3: Document research and license decisions**

Define evidence priority: official specification, official documentation, official source at pinned commit, reproducible public vector. Define outcomes `allowed`, `forbidden`, `unclear` for repository redistribution and `compatible`, `incompatible`, `pending` for SignPath. State that either non-positive result blocks `verified` and bundling.

- [ ] **Step 4: Update contribution and signing policy**

Require contributors to supply source revision, license evidence, attribution, hashes, and signing compatibility. State that SignPath rejection leaves the first RC unsigned and non-stable; remediation, paid CA, or changed acceptance requires owner action.

- [ ] **Step 5: Run tests and commit**

Run: `python -m unittest tests.catalog.test_licensing -v`
Expected: PASS.
Commit: `docs: define evidence and signing eligibility policy`
The controller pushes after review and waits for exact-SHA CI.

### Task 10: BIP-39 and TON research batch

**Files:**
- Create: `catalog/dictionaries/bip39-{en,ja,ko,es,zh-hans,zh-hant,fr,it,cs,pt}.json`
- Create: `wordlists/bip39-<language>/<pinned-revision>.txt` for all ten languages
- Create: `catalog/schemes/{bip39,ton-native,ton-multichain-bip39}.json`
- Create: `catalog/wallets/{tonkeeper-classic,tonkeeper-multichain,gram-wallet,mytonwallet,ton-space,tonhub,openmask}.json`
- Create: `catalog/evidence/bip39-*.json`
- Create: `catalog/evidence/ton-*.json`
- Create: `docs/research/batches/bip39-ton.md`
- Create: `tests/catalog/test_bip39_ton.py`
- Modify: `catalog/required/windows-v1.json`
- Modify: `THIRD_PARTY_NOTICES`

**Interfaces:**
- Consumes: schemas, evidence policy, validator, and generator.
- Produces: verified or explicitly terminal BIP-39 and TON records with exact hashes and version-split wallet modes.

- [ ] **Step 1: Write the batch test and add expected IDs to the required manifest**

Create `tests/catalog/test_bip39_ton.py` asserting all ten dictionary IDs, three scheme IDs, seven named wallet IDs, BIP-39 lengths 12/15/18/21/24, and separate TON native/multichain mappings.
Run: `python -m unittest tests.catalog.test_bip39_ton -v`
Expected: FAIL listing missing BIP-39/TON records.

- [ ] **Step 2: Pin official BIP-39 sources and word lists**

Record the Bitcoin BIPs repository commit, exact list files, NFKD requirement, counts, hashes, and official vectors. Preserve source bytes; do not normalize stored files silently.

- [ ] **Step 3: Research TON modes and named products**

Use current official TEPs, product docs, and official source where documentation is insufficient. Split native 24-word and multichain 12/24-word modes. Resolve Gram Wallet by product identity/version rather than name inheritance.

- [ ] **Step 4: Add records, licenses, vectors, and research notes**

Set status only from evidence. A product without confirmed exportable mnemonic receives `no-mnemonic-confirmed` or `documented`, never an inferred BIP-39 mapping.

- [ ] **Step 5: Validate, regenerate, and commit**

Run: `python -m tools.catalog.cli validate --root . --allow-incomplete-required`
Run: `python -m tools.catalog.cli generate --root .`
Run: `python -m unittest tests.catalog.test_bip39_ton -v`
Expected: this batch has no missing/broken records; remaining batches may still be reported as incomplete.
Commit: `data: add verified BIP39 and TON catalogue records`
The controller pushes after review and waits for exact-SHA CI.

### Task 11: Monero, MyMonero, and Polyseed research batch

**Files:**
- Create: `catalog/dictionaries/monero-{en,de,es,fr,it,nl,pt,ru,ja,zh-hans,eo,jbo,en-old}.json`
- Create: `catalog/dictionaries/polyseed-{en,ja,ko,es,fr,it,cs,pt,zh-hans,zh-hant}.json`
- Create: corresponding `wordlists/<id>/<revision>.txt`
- Create: `catalog/schemes/{monero-legacy,mymonero-13,polyseed-16}.json`
- Create: `catalog/wallets/{monero-gui-cli,mymonero,feather,cake-wallet-monero,exodus-monero-export}.json`
- Create: `catalog/evidence/monero-*.json`
- Create: `docs/research/batches/monero-polyseed.md`
- Create: `tests/catalog/test_monero_polyseed.py`
- Modify: `catalog/required/windows-v1.json`
- Modify: `THIRD_PARTY_NOTICES`

**Interfaces:**
- Consumes: Task 9 policy and Task 3 validators.
- Produces: separate Monero legacy, MyMonero, and Polyseed records; no BIP-39 substitution.

- [ ] **Step 1: Make the batch test fail on missing Monero-family IDs**

Create `tests/catalog/test_monero_polyseed.py` asserting every listed language ID, 25/13/16-word separation, and named wallet mappings. Run it and capture only missing record IDs, never words, in output.

- [ ] **Step 2: Pin official sources and exact word-list bytes**

Research getmonero documentation/source, MyMonero behavior, and Polyseed upstream revision. Record 25/13/16-word rules and historical EnglishOld separately.

- [ ] **Step 3: Research wallet/version mappings**

Verify Cake Wallet, Feather, and version-specific Exodus export behavior from current official sources. Do not generalize import support to export support.

- [ ] **Step 4: Add records, vectors, licenses, and notes**

Require exact count/hash tests for every dictionary and distinct scheme IDs.

- [ ] **Step 5: Validate, regenerate, and commit**

Run `python -m unittest tests.catalog.test_monero_polyseed -v`, lenient catalogue validation, and generation checks; commit `data: add Monero and Polyseed catalogue records`. The controller pushes after review and waits for exact-SHA CI.

### Task 12: SLIP-39, Algorand, and Cardano research batch

**Files:**
- Create: `catalog/dictionaries/slip39-en.json`
- Create: corresponding `wordlists/<id>/<revision>.txt`
- Create: `catalog/schemes/{slip39-share,algorand-25,cardano-byron,cardano-icarus,cardano-hardware}.json`
- Create: `catalog/wallets/{trezor-model-t,trezor-safe-3,trezor-safe-5,trezor-safe-7,pera-wallet,defly,yoroi,daedalus,lace,eternl,nami,typhon}.json`
- Create: `catalog/evidence/{slip39,algorand,cardano}-*.json`
- Create: `docs/research/batches/slip39-algorand-cardano.md`
- Create: `tests/catalog/test_slip39_algorand_cardano.py`
- Modify: `catalog/required/windows-v1.json`
- Modify: `THIRD_PARTY_NOTICES`

**Interfaces:**
- Consumes: common BIP-39 dictionary references from Task 10 where evidence permits.
- Produces: versioned 20/33-word SLIP-39 share profiles, Algorand 25-word, and Cardano 12/15/24/27-word modes.

- [ ] **Step 1: Add a failing test for the complete batch**

Create `tests/catalog/test_slip39_algorand_cardano.py`. Assert each Trezor model and each named Cardano/Algorand wallet has a record, even if its terminal status is non-selectable; assert Algorand references `bip39-en` rather than a duplicate dictionary.

- [ ] **Step 2: Research and pin SLIP-39 evidence**

Record the 1024-word list, supported share lengths, group/threshold metadata, and the rule that Tessaveil never combines shares.

- [ ] **Step 3: Research Algorand and Cardano variants**

Separate Byron/Icarus/hardware semantics and the historical 27-word Daedalus paper mode. Map named wallets by version and actual generated backup format.

- [ ] **Step 4: Add data, vectors, licenses, and notes**

Do not duplicate BIP-39 word files for Algorand or Cardano profiles; reference the verified dictionary IDs.

- [ ] **Step 5: Validate, regenerate, and commit**

Run the batch test, lenient catalogue validation, and generation checks. Commit `data: add SLIP39 Algorand and Cardano records`. The controller pushes after review and waits for exact-SHA CI.

### Task 13: Electrum, Substrate, and Decred research batch

**Files:**
- Create: `catalog/dictionaries/{electrum-v1-en,pgp-even,pgp-odd}.json`
- Create: corresponding `wordlists/<id>/<revision>.txt`
- Create: `catalog/schemes/{electrum-v1,electrum-v2,substrate-bip39,decred-pgp33,decred-bip39,cake-decred-15}.json`
- Create: `catalog/wallets/{electrum,polkadot-js,subwallet,talisman,decrediton,cake-wallet-decred}.json`
- Create: `catalog/evidence/{electrum,substrate,decred}-*.json`
- Create: `docs/research/batches/electrum-substrate-decred.md`
- Create: `tests/catalog/test_electrum_substrate_decred.py`
- Modify: `catalog/required/windows-v1.json`
- Modify: `THIRD_PARTY_NOTICES`

**Interfaces:**
- Consumes: BIP-39 dictionary IDs and position-rule schema.
- Produces: separate Electrum generations, Polkadot/Kusama semantics, and three non-interchangeable Decred profiles.

- [ ] **Step 1: Add the failing batch test and even/odd position fixtures**

Create `tests/catalog/test_electrum_substrate_decred.py`. Assert all batch IDs exist and a 33-row Decred scheme alternates only the eligible PGP half for each position.

- [ ] **Step 2: Research official sources and version boundaries**

Pin Electrum v1/v2 sources, Substrate derivation documentation/source, Decred PGP format, and Cake Wallet's actual 15-word list/version.

- [ ] **Step 3: Add records and vectors without inferred compatibility**

Use separate schemes even when a dictionary is shared; mark insufficient Cake evidence non-selectable rather than guessing.

- [ ] **Step 4: Validate, regenerate, and commit**

Run the batch test, lenient catalogue validation, and generation checks. Commit `data: add Electrum Substrate and Decred records`. The controller pushes after review and waits for exact-SHA CI.

### Task 14: Zano, Sia, Zcash/Zallet, and Chia research batch

**Files:**
- Create: `catalog/dictionaries/{zano-en,sia-legacy}.json` plus any additional distinct verified lists discovered
- Create: corresponding `wordlists/<id>/<revision>.txt`
- Create: `catalog/schemes/{zano-modern,zano-legacy,sia-bip39,sia-legacy,zcash-bip39,chia-bip39}.json`
- Create: `catalog/wallets/{zano-wallet,cake-wallet-zano,sia-walletd,sia-ui,siad,zallet,zcash-official,chia-wallet}.json`
- Create: `catalog/evidence/{zano,sia,zcash,chia}-*.json`
- Create: `docs/research/batches/zano-sia-zcash-chia.md`
- Create: `tests/catalog/test_zano_sia_zcash_chia.py`
- Modify: `catalog/required/windows-v1.json`
- Modify: `THIRD_PARTY_NOTICES`

**Interfaces:**
- Consumes: BIP-39 dictionary records where explicitly proven.
- Produces: Zano 26 and historical 24/25, Sia 12 and historical 28/29, and verified Zcash/Chia modes with limitations.

- [ ] **Step 1: Add the failing batch test and historical flags**

Create `tests/catalog/test_zano_sia_zcash_chia.py`. Assert all batch IDs exist, historical records still require support status, and walletd's legacy limitation is visible.

- [ ] **Step 2: Research and pin official specifications/source**

Resolve list revision, extra passphrase behavior, current versus historical product support, and non-mnemonic key material.

- [ ] **Step 3: Add records, vectors, licenses, and limitations**

Never label non-mnemonic Zcash material as a word-table profile.

- [ ] **Step 4: Validate, regenerate, and commit**

Run the batch test, lenient catalogue validation, and generation checks. Commit `data: add Zano Sia Zcash and Chia records`. The controller pushes after review and waits for exact-SHA CI.

### Task 15: Named wallet and network coverage matrix

**Files:**
- Create: `catalog/wallets/{trust-wallet,metamask,coinbase-wallet,exodus,atomic-wallet,onekey,ledger,okx-wallet,bitget-wallet,safepal,tangem-seed,keystone,bitbox02,ellipal,coinomi,guarda,tokenpocket,imtoken,rabby,rainbow,zerion,sparrow,bluewallet,coldcard,blockstream-jade,passport,seedsigner,phantom,solflare,backpack,glow,keplr,leap,cosmostation,temple,kukai}.json`
- Create: `catalog/evidence/wallet-*.json`
- Create: `catalog/evidence/network-*.json`
- Create: `docs/research/batches/named-wallets-networks.md`
- Create: `tests/catalog/test_wallet_identity.py`
- Modify: `catalog/required/windows-v1.json`

**Interfaces:**
- Consumes: all scheme IDs from Tasks 10–14.
- Produces: a complete searchable product/network/mode matrix for Bitcoin, Ethereum/EVM, Base, BNB Chain, Polygon, Avalanche, Arbitrum, Solana, TRON, Cosmos, Tezos, Polkadot/Kusama, and all previously covered ecosystems.

- [ ] **Step 1: Write identity and completeness tests**

Add `test_no_overlapping_product_platform_version_mode`, `test_same_product_can_have_distinct_modes`, `test_import_only_is_not_generation_evidence`, and `test_all_named_products_have_terminal_status`. The conflict key is normalized product ID, platform, overlapping version interval, and concrete `mode_id`. Multiple records with the same wallet/product name are allowed when their `mode_id` values represent distinct simultaneous modes. Fail only when the complete conflict key overlaps or when duplicate aliases make that same mode ambiguous without conflict-resolution evidence.

- [ ] **Step 2: Run tests and confirm missing records fail**

Run: `python -m unittest tests.catalog.test_wallet_identity -v`
Expected: FAIL with missing named-product IDs.

- [ ] **Step 3: Research multichain, hardware, Bitcoin, Solana, Cosmos, and Tezos products**

For every product, assign stable mode IDs for generated mnemonic, imported mnemonic, private key, passkey, MPC, social login, and cloud backup modes. Record platform/version and current official source; never collapse simultaneous modes merely because the product name matches.

- [ ] **Step 4: Add network aliases without duplicating dictionaries**

Map EVM networks and product search terms to scheme/profile IDs; keep network guidance distinct from proof of recovery compatibility.

- [ ] **Step 5: Validate terminal statuses and ambiguity handling**

Run the identity test, required-set test, and validator. Any unresolved product remains explicit `documented` or `blocked`; do not clear the Windows gate by inference.

- [ ] **Step 6: Regenerate and commit**

Commit `data: complete named wallet and network matrix`. The controller pushes after review and waits for exact-SHA CI.

### Task 16: Cake Wallet current-format matrix and catalogue completeness audit

**Files:**
- Create: `catalog/wallets/cake-wallet-<network>-<mode>.json` for every current official Cake Wallet network/mnemonic mode
- Create: `catalog/evidence/cake-wallet-*.json`
- Create: `docs/research/batches/cake-wallet.md`
- Create: `tests/catalog/test_catalogue_complete.py`
- Modify: `catalog/required/windows-v1.json`

**Interfaces:**
- Consumes: all dictionaries, schemes, wallets, evidence, and the required manifest.
- Produces: strict `validate_catalog(catalog, require_terminal=True, require_release_ready=False)` research coverage, zero unresolved manifest references, and a separately evaluated Windows release-readiness result.

- [ ] **Step 1: Write the final completeness test**

Assert every required item has at least one record, every record has an evidenced terminal status, and every selectable record is `verified`. Add a separate release-readiness assertion proving that any required `blocked` item yields `NO-GO` without making the research-completeness assertion fail.

- [ ] **Step 2: Run the test and capture the precise missing-ID list**

Run: `python -m unittest tests.catalog.test_catalogue_complete -v`
Expected: FAIL until Cake Wallet and any omissions from Tasks 10–15 are resolved.

- [ ] **Step 3: Research all current Cake Wallet networks and modes**

Use Cake Wallet's official per-cryptocurrency documentation and official source at pinned revisions where needed. Split modes by actual list, length, network, and version; reuse dictionary IDs only with evidence.

- [ ] **Step 4: Resolve every manifest gap**

Add evidence-backed records or explicit blockers. Produce a concise blocker section in `docs/catalog*.md`; do not change mandatory scope during this task.

- [ ] **Step 5: Run the complete data gate**

Run: `python -m tools.catalog.cli validate --root . --require-terminal`
Run: `python -m tools.catalog.cli generate --root . --check`
Run: `python -m unittest tests.catalog.test_catalogue_complete -v`
Expected: PASS when every mandatory item has an evidenced terminal status, including `blocked`. Then run `python -m tools.catalog.cli validate --root . --require-release-ready`; it may return nonzero with a precise blocker list. That nonzero result is recorded as the honest Windows release `NO-GO` and requires a separate owner decision, but it does not invalidate completion of this research task.

- [ ] **Step 6: Commit the honest research result**

Commit `data: complete Tessaveil research catalogue status`. A commit may document blockers once the terminal-research gate is green; it must never describe Windows release readiness as green while `--require-release-ready` is red.

### Task 17: Threat model and cross-version warning contract

**Files:**
- Create: `THREAT_MODEL.md`
- Create: `tests/threat/test_required_claims.py`
- Create: `tests/threat/__init__.py`
- Modify: `README.md`
- Modify: `README.ru.md`

**Interfaces:**
- Consumes: threat scenarios and precise file/edit semantics from both specs.
- Produces: public claims and warnings later copied into Figma/product copy; no absolute security promise.

- [ ] **Step 1: Write failing required-claims tests**

Assert the threat model covers EXE theft, ciphertext theft, offline guessing, master disclosure, weak order key, hostile OS/IME/memory/swap/dumps, repeated Spin, different saved tables, temporary files, mobile group leakage, password loss, source-wallet compromise, physical loss, rollback, and filesystem-specific atomicity.

- [ ] **Step 2: Pin the comparison-risk requirements**

Test for explicit statements that full row/table re-randomization does not remove cross-version intersection risk, no cosmetic reshuffle exists, custom-list changes create a new unverified sheet, and “Verified by me” never transfers.

- [ ] **Step 3: Run tests and confirm failure**

Run: `python -m unittest tests.threat.test_required_claims -v`
Expected: FAIL because `THREAT_MODEL.md` is absent.

- [ ] **Step 4: Write the scenario matrix**

For each threat, record assets, attacker capability, protection, limitation, mitigation, residual risk, and user guidance. Distinguish identical redundant copies from changed table versions. Describe temporary files as clear technical headers plus ciphertext, not plaintext payload.

- [ ] **Step 5: Add concise README warnings**

State that Tessaveil briefly sees the current word/column, cannot defeat a compromised OS, does not validate complete phrases, and does not replace a cold backup/hardware-wallet process.

- [ ] **Step 6: Verify and commit**

Run: `python -m unittest tests.threat.test_required_claims -v`
Expected: PASS.
Commit: `docs: add Tessaveil threat model`. The controller pushes after review and waits for exact-SHA CI.

### Task 18: Final first-subproject gate and handoff

**Files:**
- Create: `docs/research/subproject-1-verification.md`
- Create: `tests/repository/test_no_sensitive_material.py`
- Modify: `.github/workflows/catalog-quality.yml`
- Modify: `docs/catalog.md`
- Modify: `docs/catalog.ru.md`
- Modify: `THIRD_PARTY_NOTICES`

**Interfaces:**
- Consumes: every earlier task's records, reports, ADRs, tests, and exact commit SHA.
- Produces: one evidence document with two independent conclusions: first-subproject research completeness and Windows release readiness.

- [ ] **Step 1: Add repository secret and synthetic-data tests**

Scan tracked text for private-key headers, GitHub/Figma token patterns, local absolute user paths, and mnemonic-like fixture violations. Allow only reviewed public standard vectors by exact path/hash.

- [ ] **Step 2: Run the complete local gate**

Run: `python -m unittest discover -s tests -p "test_*.py" -v`
Run: `python -m tools.catalog.cli validate --root . --require-terminal`
Run: `python -m tools.catalog.cli generate --root . --check`
Run the Rust probe tests and platform build checks documented by Tasks 5–7.
Expected: all safe/applicable checks pass and every unavailable physical check has an evidenced terminal blocker. Missing physical-device/filesystem evidence remains an explicit Windows release `NO-GO`, not a skipped green check and not a failure of honest research completion.

- [ ] **Step 3: Switch CI from incremental to strict catalogue validation**

Replace `--allow-incomplete-required` with mandatory `python -m tools.catalog.cli validate --root . --require-terminal` and make generated-document drift, threat claims, spike-report contracts, schema/Python parity, positive test discovery, and sensitive-material scanning mandatory jobs. Add a separate release-readiness reporting job that runs `--require-release-ready`, captures its exit code and blocker output, and verifies they exactly match the committed `GO`/`NO-GO` report. On the research branch that job succeeds when an honest `NO-GO` is recorded; a future release/promotion workflow must invoke `--require-release-ready` directly and require exit code 0.

- [ ] **Step 4: Review licences and generated notices**

Confirm every distributed list has source revision, hash/count, attribution, repository permission, and SignPath compatibility. Regenerate `THIRD_PARTY_NOTICES` deterministically and fail on pending decisions.

- [ ] **Step 5: Write the verification report**

Record exact commit, command results, catalogue research completeness, the independent Windows release-readiness result, blockers, architecture decision status, mobile/KDF freeze status, filesystem claim scope, and remaining external risks. An evidence-backed `blocked` result may close this research subproject while release remains prohibited until a separate owner decision.

- [ ] **Step 6: Commit**

Run: `git add .github docs tests THIRD_PARTY_NOTICES`
Run: `git commit -m "docs: complete Tessaveil research foundation"`
Do not push from the task agent. The controller pushes `feature/tessaveil-research-foundation` after review.

- [ ] **Step 7: Wait for exact-SHA GitHub CI and stop**

Run: `gh run list --commit "$(git rev-parse HEAD)" --limit 5` and watch the mandatory run to completion.
Expected: mandatory research CI is green for the exact SHA and the report records the independent release-readiness result. Report blockers honestly and do not merge, release, or start production implementation while a required release blocker remains unresolved.
