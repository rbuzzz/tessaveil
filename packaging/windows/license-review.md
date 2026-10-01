# Static Windows candidate: engineering licensing review

Unsigned Windows v1 candidate for synthetic data only; not RC/stable, no
Authenticode, no real funds, no final format/KDF/migration promise. Windows
real-data use/freeze remains NO-GO. This is documented engineering evidence, not legal
assurance. Original Tessaveil code remains Apache-2.0.

## Scope and binding

The exact executable link map is reconciled against the actual application
Ninja link inputs and archive member lists. Ambiguous object basenames retain
every possible input; they are not guessed away. `linked-inputs.json` records
the EXE, link-map and input hashes. The source/notice hashes in
`license-bindings.json` bind the material below. Bootstrap pins compiler and
source archives. Changing dependencies, modules, source or notice bytes requires
re-running the inventory, independent audit and review.

## QtBase 6.8.3

Source is the complete unmodified QtBase archive whose SHA-256 is
`992bf7766e214a341ef793eb3665fb784787d2fd666955f5f507f4c6f1f770dd`.
Core/Gui/Widgets/EntryPoint and Windows, modern-Windows-style, GIF/ICO/JPEG
plugins are linked under LGPL-3.0-only. No Network, SQL, OpenSSL, Vulkan,
QtTest, DBus, QML, QtQuick or commercial-only Qt module is an application input.
The configure summary and generated feature decisions are preserved. Building
other QtBase tools/modules does not make them shipped application components.

The entire upstream source retains every original notice. Convenient verbatim
copies accompany the distribution, including each attribution's referenced
LicenseFile, compound JPEG notices and the inline Wintab notice. Attribution
metadata is a source inventory, not by itself evidence that every entry is
linked. Applicable third-party terms were read from this exact source:

| Material in selected modules | Chosen/applicable terms and handling |
| --- | --- |
| FreeType and gray rasterizer | FTL route, not GPL-2.0; keep full FreeType notices and attribution. BDF/PCF additionally MIT/MIT-open-group; bundled compression Zlib. |
| HarfBuzz, md4c, D3D12 memory allocator/MiniEngine, pixman | MIT; retain copyright/permission notices. |
| libjpeg-turbo and IJG code | IJG AND BSD-3-Clause; retain compound notices and explicit IJG acknowledgement. |
| libpng and zlib | Libpng AND libpng-2.0; Zlib; retain unmodified notices. |
| PCRE2 and SLJIT | Exact PCRE2 BSD-3-Clause variant and BSD-2-Clause; ship full terms without relying on notice exceptions. |
| double-conversion, easing, AGLFN, RFC6234, iaccessible2 | BSD-3-Clause; retain attribution, conditions and disclaimers; no endorsement claim. |
| smooth scaling and X server helper | BSD-2-Clause AND Imlib2; X11 AND HPND; exact compound notices retained. |
| Unicode character/CLDR data | Unicode-3.0 notices retained. |
| MIME data | Apache-2.0 (Tika attribution retained). |
| BLAKE2 | Apache-2.0 route (upstream alternative CC0 also preserved). |
| MD4/MD5/SipHash/Keccak and SHA-1 | CC0/public-domain dedications retained; SHA3 endian helper BSD-2-Clause. |
| tinycbor and portable forkfd source | MIT; notices retained even where platform preprocessing excludes a helper. |
| ICC sRGB profile | Exact ICC terms permit copying/distribution/embedding; profile unmodified, source notice retained. |
| Wintab definitions | Inline LCS/Telegraphics notice expressly permits free use/copy/distribution; retained verbatim. |

GPL-only test/performance code, LGPL/GPL alternatives for unused DBus headers,
Android/wasm/cocoa/XCB and source-only utilities are not labeled as runtime
components. Their source remains intact in the complete corresponding Qt source.
LGPL obligations are not discharged by this table: the source/configuration,
application objects, replacement/reverse-engineering information and actual
modified-library relink/smoke gates remain mandatory for every candidate.

## LLVM-MinGW runtime

The pinned binary archive is LLVM-MinGW 20250709. Its build scripts at
`a1f6413e5c21fd74b64137b56167f4fba500d1d8` select MinGW-w64
`a0e69f7bc83a29b40e68355aac3e0c39b113b20f` and LLVM 20.1.8
(`87f0227cb60147a26a1eeb4fb06e3b505e9c7261`). Source/notice downloads
and hashes are in runtime-sources.json, not floating URLs.

libc++, libc++abi and libunwind use Apache-2.0 WITH LLVM-exception;
their complete upstream texts, including legacy MIT/NCSA terms, are retained.
Compiler-rt's full license is retained conservatively; actual Rust builtins have
their separate source license below. No libwinpthread DLL is distributed.

All observed MinGW runtime members are mapped to exact C/assembly source files
in the pinned source archive. The full files preserve their individual notices.
`COPYING` supplies ZPL-2.1 for otherwise unmarked files (including GUID/startup
definitions); prominently marked public-domain files retain their dedication.
gdtoa retains Lucent/David Gay permission and disclaimer; printf wrappers retain
Keith Marshall's unrestricted grant and gdtoa notice. No runtime source is
modified. Aggregate runtime COPYING and disclaimers accompany the individual
sources; no trademark/endorsement permission is claimed.

The generic MinGW notice contains an unresolved Cephes paragraph. It is not
used to infer permission: observed hypotf is the `_hypot` wrapper, x86 ldexp
and ldexpf are explicitly public domain. Actual linked source mapping rejects
Cephes/Moshier material pending a separate review. This is a member/source
conclusion, not a claim that all MinGW math code is cleared.

## Rust 1.90.0 and application crates

Application dependencies come from Cargo.lock and exact Cargo metadata; source
checksums, versions, expressions, graph and copied license/notice files are
recorded. The standard library uses the pinned rust-src library lock (hash in
runtime-sources.json), not merely the shorter bundled copyright summary.
The actual linked external standard-library objects include addr2line 0.25.0,
gimli 0.32.0, hashbrown 0.15.4, memchr 2.7.5, object 0.37.1 and rustc-demangle
0.1.25. Exact checksum-verified crate archives provide their MIT/Apache terms
(MIT route for memchr's Unlicense OR MIT). Their full notices are included.
The std source graph also lists non-Windows/build-only dependencies; the SBOM
marks observed linked objects separately and does not impute their code to EXE.

Rust std/core/alloc retain MIT OR Apache-2.0 plus Unicode-3.0/BSD notices listed
in COPYRIGHT-library.html. compiler-builtins' exact rust-src LICENSE.txt states
MIT AND Apache-2.0 WITH LLVM-exception; both terms are retained. Original
Tessaveil code is never relabeled as LGPL or MIT.

## Dictionaries and operating system

Only the compiled, hash-checked public BIP39 English dictionary is distributed
as an embedded application asset. Its catalogue decision is MIT, redistribution
allowed, and approved for this unsigned/GitHub-provenance alpha route. Existing
dictionary notices remain intact. Unverified modes remain unavailable; no
additional dictionary is copied just because it exists in the repository.

Windows/UCRT import DLLs are supplied by the operating system, not packaged.
An independent PE parser checks AMD64, imports and absence of Authenticode;
LLVM's import report must agree. Host-injected security/accessibility DLLs in
development-host observation are not application sidecars or shipped files.

## Supplier build prefixes

An exact byte/hash-bound record distinguishes known LLVM vendor CI prefixes
from local user paths. Each reviewed byte string must occur in the specific
immutable supplier archive members pinned in vendor-members.json. The EXE is
never patched or stripped to conceal paths. Only a temporary scan view classifies
those proven supplier spans; all remaining bytes and UTF-16 data are scanned.
Private username/worktree paths still fail. Public, deterministic toolchain
prefixes are not represented as personal user paths.
