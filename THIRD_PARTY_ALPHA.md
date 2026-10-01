# Tessaveil unsigned synthetic Windows v1 candidate — third-party status

Synthetic data only. Not RC/stable; no real funds. No Authenticode. No final
format, KDF or migration promise. Verdict: NO-GO для реальных данных.
Distribution is permitted by this engineering pipeline only after all same-SHA
source, notice, relink, synthetic smoke and independent archive gates pass.
The candidate uses the conspicuous
`Tessaveil-unsigned-synthetic-windows-v1-candidate-<source-sha>` container and
runtime/compliance/decision/manifest files. The external manifest binds exact
names, byte sizes and SHA-256 for both ZIPs, `Tessaveil.exe`, SBOM, notices and
decision; the compliance inventory also binds the bilingual guidance, threat
model and operator protocols. No artifact publication or GitHub attestation is
claimed by this file; it is not legal assurance, signing or real-data approval.

Original Tessaveil code is Apache-2.0 (LICENSE). It does not relicense Qt,
third-party dependencies, word lists or trademarks.

The build uses static QtBase 6.8.3 Core/Gui/Widgets/EntryPoint with Windows,
style and image plugins, under the LGPL-3.0-only route. The separate
compliance bundle must accompany any runtime artifact: complete exact source,
GPLv3/LGPLv3 and component license texts, notices, generated configuration,
relinkable application material and replacement information. Modification of
Qt and reverse-engineering to debug those modifications are permitted.

Qt source SHA-256:
`992bf7766e214a341ef793eb3665fb784787d2fd666955f5f507f4c6f1f770dd`.
Qt bundled FreeType (including its subcomponents), HarfBuzz, libpng, libjpeg,
PCRE2, zlib, double-conversion and other source components have separate terms.
Source qt_attribution.json records and licenses are retained in the compliance
bundle and represented in the CycloneDX inventory with explicit source scope.
The selected modules, individual runtime sources, license choices and preserved
notices are documented in compliance/license-review.md. The same-run link-member
inventory, source/notice bindings and runtime policy must match; changes fail closed.
This software is based in part on the work of the Independent JPEG Group.
Portions of this software are copyright The FreeType Project (www.freetype.org).
All rights reserved. FreeType is used under its FTL option, not its GPL option.

Rust dependencies are pinned by Cargo.lock. The SBOM is derived from exact
locked Cargo metadata with crate archive hashes; missing licenses or graph drift
stop packaging. Crate-root licenses/notices accompany the application archive.
Rust 1.90.0 standard-library subdependencies use the exact rust-src library lock
and checksum-verified crate source licenses. LLVM-MinGW 20250709 runtime notices
are bound to pinned supplier/source material and actual linked MinGW members.
Package SPDX metadata alone is not accepted as license text.

Only BIP39 English dictionary bytes are embedded by the application. Their
SHA-256 is `2f5eed53a4727b4bf8880d8f3f199efc90e58503646d9ff8eff3a2ed3b24dbda`.
MIT license/copyright and language credits are retained in THIRD_PARTY_NOTICES.
The catalogue's explicit allowed/compatible decisions remain prerequisites,
including for this unsigned GitHub-provenance candidate path. No SignPath project
acceptance is claimed. Only the three approved TON native profile identities
are selectable; sharing a word list does not activate other wallet modes.

Windows API/UCRT system components listed in PE-imports.json are provided by the
host and are not redistributed. Static compiler/runtime notices are included in
the compliance bundle, which must always accompany the runtime archive.
No paid/commercial Qt license or signing purchase is selected.
