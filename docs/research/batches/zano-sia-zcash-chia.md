# Zano, Sia, Zcash/Zallet and Chia research batch

Reviewed **2026-09-29 UTC** under [source-policy.md](../source-policy.md) and
[licensing.md](../licensing.md). This batch is public-source research only.
No wallet was restored, funded, synced or used to derive a private key. No
removable medium, provider call, main-branch change or production access occurred.

There are two dictionary records, ten schemes and thirteen concrete product
modes. Only the Sia legacy English dictionary is verified. Every wallet and
mnemonic scheme remains documented or blocked and non-selectable. A completed
research requirement is not selectable support or a release-readiness claim.

## Immutable boundaries

All min/max intervals are the same full source commit: a singleton inspected
boundary. A version in package metadata does not prove a released binary
contains that source. Historical generation start/end releases that were not
established remain explicit blockers; no open-ended compatibility is invented.

| Upstream | Full revision | Scoped identity |
| --- | --- | --- |
| hyle-team/zano | `e55c8ec47b76ed809162a958cf4600e03256a96a` | Inspected source only |
| SiaFoundation/siad | `66e7fc630585887c30033379d2a0a8bf5c618177` | Inspected source only |
| SiaFoundation/walletd | `aa523f95c5b2a106a3c0d9675205c90305d2d9d9` | Inspected source only |
| SiaFoundation/web | `f4e3ff774c4f6a5b9830abf1767485215a26a349` | walletd UI package0.36.2 |
| SiaFoundation/coreutils | `024db888b8bb80b5e54876baaf868c03c9aa0902` | v0.24.1, both walletd and web SDK go.mod |
| NebulousLabs/Sia-UI | `cd7e221b98fc7a395de25bd8dfaa4f4de2a6e3d2` | Historical Sia-UI package v1.3.3 |
| zcash/zcash | `558f686599586f55def3db86955d74d3be44605e` | Inspected source only |
| zcash/zallet | `f9dcd4d31439feb813c95ac2516814421f5b04df` | Inspected source only |
| Chia-Network/chia-blockchain | `af0d7eab5fb12bbd8af51f47a7123ee700d74c2a` | Inspected source only |
| cake-tech/cake_wallet | `9679f91a8c9f63d00500c2b7cc18daf00949bdef` | Inspected source only |
| koushiro/rust-bips | `1a6cc63a53721781aabd695307cc41b82ca76813` | bip0039 crate0.12.0 vcs revision |
| NebulousLabs/entropy-mnemonics | `7532f67e35008b0f36bbebb20d5a6ee8f14a22f5` | Exact siad pseudo-version dependency, official GitLab |

The official project organizations host these repositories. siad directly names
the NebulousLabs GitLab module and pseudo-version in go.mod; the official GitLab
commit API resolved7532f67e3500 to the full hash above. The old GitHub mirror
HEADbc7e13c5ccd82d4715222a0dc2b4b60e881dd462 was discovery only, not used as the
siad dependency pin. The web SDK pins coreutils0.24.1; GitHub's tag commit API
resolved it. Zallet Cargo.lock pins bip0039 0.12.0 with checksum
`568b6890865156d9043af490d4c4081c385dd68ea10acd6ca15733d511e6b51c`.
The downloaded crates.io archive exactly matched; its .cargo_vcs_info.json
provided the upstream commit above. No dependency was installed into the app.

## Zano: native26, historical25 and rejected24

The source word map has1626 contiguous numeric indices. Parsing the literal map
and sorting by its integer values reproduces exactly the Electrum-old tuple at
the Task13 immutable source pin, including order. It is not the current Monero
English dictionary and not BIP39. Word membership is case-sensitive; the core
codec performs no lowercase or Unicode normalization. The account restore
wrapper trims and compresses whitespace before rebuilding the data words.

On the inspected little-endian Windows/Linux target, each32-bit word x becomes
three indices: x%n, (x//n+w1)%n, (x//n//n+w2)%n, n=1626. Eight groups encode32
bytes as24 words. Current generation appends word25 for quantized creation time
and a password-use flag, then word26 for the auditable flag and checksum.
The timestamp uses the source's fixed date offset/quantum and reserves the upper
range for password use. The checksum hashes plaintext seed plus exact password,
overwrites the first64-bit hash segment with rounded timestamp, hashes again,
then applies the modulo/remainder workaround present in source; word26 stores
twice the checksum plus auditable bit. This is not Monero's CRC32 repeated word.

An optional seed password encrypts binary seed via the legacy ChaCha helper:
legacy password-to-key derivation and a cn_fast_hash-derived IV. Creation rejects
characters outside its restricted ASCII regex. There is no BIP39 salt or NFKD
extension. A wallet-file unlock password is a different secret. The research
does not promise arbitrary Unicode, cross-endian or historical password parity.

The restore function accepts25 and26 only. The pinned public wallet_seed_entries
explicitly labels a24-word example invalid and old25 examples valid. Therefore:

- native26 is current generation in inspected core;
- historical25 is separately documented as current-source import, without a
  proven original historical generation release interval;
- historical24 remains blocked: current core rejects it, and the precise old
  generating release/mode/passphrase behavior was not established.

The official dated [seed documentation](https://docs.zano.org/docs/use/seed-phrase)
describes24–26 in broad terms. That broad historical description does not
override the exact current parser. No24-word wallet support is advertised.
Upstream tests were read, not run as wallet recovery; no new funded vectors.

The source carries a Monero BSD-3-Clause header and Zano/Louisdor credits; root
LICENSE has an MIT-like grant. However, exact equality to the Electrum-old
Wiktionary-derived list exposes the same unresolved original data-rights chain
as Task13. The word list is intentionally not bundled: redistribution unclear,
SignPath pending, dictionary blocked, committed hash/path null. The requested
wordlists/zano-en artifact would violate the license gate while unresolved.
This is a provenance blocker, not an assertion of infringement.

## Cake Zano is not a native26 creation profile

Task16 follow-up: official Cake documentation now explicitly dates native26
creation before v6.4.3 and documents current12/24. The locked Dart BIP39 list
was independently compared and normalization reviewed in
[the complete Cake matrix](cake-wallet.md). This closes the source-list
identity gap below, not native dependency, binary or recovery verification;
the earlier blocked scheme remains blocked.

At the shared Cake source pin, create() chooses128 or256-bit BIP39 generation
and restores from a computed derivation. The helper applies BIP39, then BIP32
`m/44'/128'/0'/0/0`, interprets the private bytes as little-endian and reduces
modulo the Ed25519 subgroup order. Restore dispatch first tests BIP39; the other
branch calls native seed restore. The two identities are preserved as:

- cake-wallet-zano: Android-targeted native seed import, not native26 creation;
- cake-wallet-zano-bip39: separate12/24 creation with its own blocked scheme.

The exact Dart dependency bytes, Unicode normalization, native-library pin and
released Android artifact were not bound in this batch. Mapping native26 to
current BIP39 creation would be an unsupported compatibility assertion.
No iOS/desktop parity is inferred. The BIP39 vocabulary reference is provisional
source-level dependency intent in a blocked scheme, not a verified list binding.

## Sia12 versus legacy28/29

The current coreutils wallet code uses exactly the existing2048 BIP39-English
entries in the same order. It supports only128-bit entropy /12 words with4
leading SHA256 checksum bits. It parses words with strings.Fields and exact
case-sensitive lookup. Crucially, SeedFromPhrase computes **BLAKE2b-256 over
the16 entropy bytes**, not BIP39 PBKDF2 over the sentence. There is no recovery
passphrase argument. KeyFromSeed then hashes seed plus a little-endian index
for Ed25519; no keys are derived by Tessaveil or these tests.

The walletd UI0.36.2 source calls SDK.generateSeedPhrase and labels validation
as12-word BIP39. Its pinned SDK routes directly to coreutils0.24.1. The profile
is web/UI/seed creation, not every API client supported by the server.

The dated [V2 hardfork documentation](https://docs.sia.tech/miscellaneous/v2)
warns that walletd's new seed flow does not support legacy28/29. Current
walletd README also explicitly states its server is seed-agnostic and can use
externally derived legacy keys. These are retained as scoped facts: **the
inspected UI seed route rejects legacy phrases; the generic server does not
ban externally supplied legacy addresses/transactions**. The required manifest's
wallet-walletd historical flag is corrected to false; this is a current UI
record, unlike Sia-UI/siad historical modes. No automatic fund migration occurs.

Legacy siad SeedToString appends six checksum bytes to32 seed bytes, using
crypto.HashObject / BLAKE2b-256, and passes the38-byte payload to the pinned
entropy-mnemonics module. This is a bijective base conversion, not Monero's
three-word algorithm. Byte digits are least-significant first, with a length
offset: integer = sum((byte+1)*256**position)-1. Phrase indices use the analogous
base1626 mapping. On encoding, repeatedly emit value%1626 and set
value=(value-1626)//1626 until the last index remains. This naturally gives
28 or29 words for the38-byte payload; the lengths are **not successive format
versions**. Separate required scheme IDs preserve the two research identities.

The vocabulary does **not** make all 1626 indices eligible at every position.
For base b and digit count k, define the bijective length offset
`O(b,k) = sum(b**i for i in 1..k-1) = (b**k-b)/(b-1)`.
Every 38-byte payload represents an integer in the inclusive interval
`L = O(256,38)` through `U = L + 256**38 - 1`.
A k-word sequence represents `O(1626,k) + sum(index[i]*1626**i)`,
with positions counted from zero in that formula. These are mathematical
consequences of the pinned codec, not a separate upstream specification.

For a fixed last index d, the lower k-1 indices span
`[O(1626,k) + d*1626**(k-1), O(1626,k) + (d+1)*1626**(k-1) - 1]`.
Intersecting this interval with [L,U] gives these necessary final-row ranges:

| Encoding | Final position (one-based) | Zero-based final index |
| --- | ---: | --- |
| 28 words | 28 | 253..1625 |
| 29 words | 29 | 0..39 |

For 28 words at d=253, the lower-position value must be at least
`L - O(1626,28) - 253*1626**27`; smaller values decode to 37 bytes.
For 29 words at d=39, that value must be at most
`U - O(1626,29) - 39*1626**28`; larger values decode to 39 bytes.
Index252 at position28 cannot reach 38 bytes even with every lower index1625;
index40 at position29 exceeds 38 bytes even with every lower index0.
Other positions can individually span the full vocabulary within this length
envelope, but lower rows are not independent at the boundary.
These constraints do not establish checksum-valid candidate eligibility:
the separate six-byte BLAKE2b checksum still constrains the complete payload.
Schemes remain documented/non-selectable and Tessaveil validates no user phrase.

The English list has1626 unique entries and unique3-character prefixes. The
dependency normalizes each word to NFC and matches its prefix. siad adds
stricter lowercase, character, exact-space/length and checksum checks; do not
generalize the dependency's permissive prefix behavior to arbitrary UI input.
Its seed encryption password protects storage, not an extra derived wallet.

Historical Sia-UI v1.3.3 source trims the entered seed and custom password
separately and sends them to its restore route. Exact bundled siad artifact
was not verified; both28 and29 import profiles remain documented only.
siad28 and29 source export profiles likewise do not promise current-network
viability. No claim that one is BIP39 or Monero is made.

The Sia dictionary is a UTF-8 LF/final-LF projection of EnglishDictionary at
the exact GitLab dependency. It is 11467 bytes; SHA256
`eaa6bce7dd92f4d6dd74f224264e0ef4ad21095d68ec77616b26ceb599baf4f7`. The file explicitly attributes Monero2014-2015 and includes
BSD-3-Clause. Root MIT Copyright2015 Nebulous is also retained. Both full notices
and modification labels are in THIRD_PARTY_NOTICES. Codex's separate data-only
assessment: redistribution allowed, local SignPath OSS compatibility compatible.
No wallet software or libraries are distributed and no Foundation acceptance
is asserted.

## Zcash: exact mnemonic mode and separate key material

zcashd source supports mnemonic creation from32-byte entropy and a language.
The ZIP339 FFI uses BIP39 and explicitly passes the empty derivation passphrase.
This batch scopes the scheme to English24; other language choices are not
silently mapped. FromLegacySeed can adjust entropy while constructing a NEW
mnemonic seed; that is not proof a mnemonic recreates every previously imported
or legacy standalone key. The inspected zcashd lock dependency version has not
been proven equal to Zallet's bip0039 version.

Zallet generates English24 from32 random bytes and stores it encrypted; keystore
derivation uses mnemonic.to_seed(""). Its pinned bip0039 crate uses NFKD and
PBKDF2-HMAC-SHA512/2048 with mnemonic+passphrase salt, and its English list was
compared entry-for-entry to the existing BIP39 dictionary. A public library
doc-test corroborates empty-passphrase behavior, not Zallet wallet recovery.

An age identity/passphrase protects Zallet storage/export and is not an extra
BIP39 derivation passphrase. The pinned export documentation explicitly says
the encrypted phrase is not self-contained without the age identity and that
standalone z_importkey/migrated key material can lie outside mnemonic coverage.

zcash-non-mnemonic is a no-mnemonic-confirmed material classification with empty
dictionary_ids and supported_lengths. zcash-official-standalone has scheme_id
null and generates_mnemonic=false. No word-table profile is fabricated for
dumpprivkey/z_exportkey, raw HD seed bytes, spending/viewing keys or wallet.dat.
The general zcash-official record is specifically zcashd Linux English mnemonic
mode, not a claim about every official wallet or every Zcash account.

## Chia English24

The pinned reference source generates32 entropy bytes /24 English words.
Its English list is byte-identical to existing BIP39-English. The primitive
also accepts12/15/18/21/24 and reconstructs English words from their first four
characters; these import behaviors are not claimed as GUI creation options.
ASCII inputs use that prefix expansion; mnemonic_to_seed then normalizes NFKD,
uses PBKDF2-HMAC-SHA512/2048 and the fixed salt mnemonic. It exposes no user
BIP39 extension. Keyring master password encrypts local storage separately.
BLS key generation/paths are distinct from BIP32; no BLS key is generated here.

## Public vectors and limits

The offline fixture contains35 public cases: ten Sia primitive codec boundary
vectors,24 Chia English entropy/empty-passphrase seed vectors, and one bip0039
empty-passphrase doc-test. Expectations are projected from upstream literals,
not generated by the Python implementation under test. Chia seed bytes are
represented by SHA256 fingerprints; sentences become existing dictionary
indices. The bip0039 literal expected seed is public and non-funded.

Tests independently reconstruct BIP39 bit packing and PBKDF2 fingerprints and
show the nonempty TREZOR salt changes the result. Chia primitive vectors include
12/18/24, while default generation remains24. Sia codec vectors include
leading-zero and base-boundary cases, but **are not full28/29 recovery vectors**.
Zano upstream format tests remain cited/reviewed evidence only. No fixed
independent full Sia12, Sia28/29, Cake Zano or Zano recovery was established;
those schemes remain non-selectable. Tests never derive addresses/private keys
or accept user phrases. No runtime wallet implementation is added.

Fix round1 adds six original synthetic length-boundary projections separately
under sia_length_boundaries, for 41 total cases. All-zero38 bytes and all-ff38
bytes exercise the exact inclusive endpoints. All-ff37 and all-zero39 exercise
their immediate integer neighbors; final indices remain253 and39 respectively,
proving that the final-index range alone is insufficient. The other two cases
are the maximum lower rows at final252 and minimum lower rows at final40.
These are arbitrary byte payloads, deliberately **not checksum-valid seeds**.
Tests explicitly reject checksum eligibility for the two 38-byte endpoints.

The six fixture expectations were independently constructed with JavaScript
BigInt using the closed-form offsets above: subtract the offset and expand the
remaining integer as ordinary base1626/base256 digits. Python tests instead
reconstruct the bijective integer with Horner recurrence and decode using the
source's iterative subtract-base/divide rule. They also exhaust all1626 final
indices against the interval intersection and compare the ranges rendered by
the actual catalogue metadata. This catches off-by-one range changes, payload
length errors and the original unrestricted-final-row claim without asserting
that the synthetic fixtures came from upstream public wallet vectors.

Chia projections retain Apache-2.0 (Chia Network2026) and existing Trezor/MIT
attribution; Apache license text already resides in notices/root LICENSE.
bip0039 uses the MIT alternative, full Qinxuan Chen2020 notice included.
License decisions cover these small source-data projections only, not wallet
binaries, application dependencies or the complete signing application.

## Reproduction and verification

Use Python3.14.2 standard-library tests:
`python -m unittest tests.catalog.test_zano_sia_zcash_chia -v`.
The original six contracts first failed for missing profiles, then passed after
records. Two regression contracts first failed for missing final-row ranges
and missing 38-byte fixtures, then passed after the narrow fix (eight total).
The full non-empty suite runs via `python tools/run_tests.py`.
Catalogue validation: `python -m tools.catalog.cli validate --root . --allow-incomplete-required`.
Regenerate both documents with `python -m tools.catalog.cli generate --root .`,
then run the same command with `--check`. Pending future batches are warnings;
strict release-readiness remains NO-GO.

Pinned Rust1.90.0 host gates: cargo fmt --check, cargo check --locked --all-targets,
cargo test --locked, with manifest spikes/mobile/core/Cargo.toml and the existing
isolated GNU toolchain. Process-local environment, short sysroot and ASCII target
avoid the known Windows linker path issue. No toolchain installation or global
settings were changed. Actual counts, failures repaired, and commit are in the
Task14 report, not invented here.

## Primary source ledger

Evidence URLs below pin the full upstream revision. Mutable documentation and
SignPath terms are dated2026-09-29 body snapshots. Byte hashes are retrieval
fingerprints, not signatures or legal guarantees. Discovery caches are excluded
from the commit; only approved dictionary/test projections are bundled.

- [zano-codec](https://raw.githubusercontent.com/hyle-team/zano/e55c8ec47b76ed809162a958cf4600e03256a96a/src/common/mnemonic-encoding.cpp) — `e55c8ec47b76ed809162a958cf4600e03256a96a`.
- [zano-modes](https://raw.githubusercontent.com/hyle-team/zano/e55c8ec47b76ed809162a958cf4600e03256a96a/src/currency_core/account.cpp) — `e55c8ec47b76ed809162a958cf4600e03256a96a`.
- [zano-timestamp-password](https://raw.githubusercontent.com/hyle-team/zano/e55c8ec47b76ed809162a958cf4600e03256a96a/src/currency_core/currency_format_utils.cpp) — `e55c8ec47b76ed809162a958cf4600e03256a96a`.
- [zano-history-vector](https://raw.githubusercontent.com/hyle-team/zano/e55c8ec47b76ed809162a958cf4600e03256a96a/tests/unit_tests/wallet_seed_test.cpp) — `e55c8ec47b76ed809162a958cf4600e03256a96a`.
- [zano-license](https://raw.githubusercontent.com/hyle-team/zano/e55c8ec47b76ed809162a958cf4600e03256a96a/LICENSE) — `e55c8ec47b76ed809162a958cf4600e03256a96a`.
- [zano-cake-modes](https://raw.githubusercontent.com/cake-tech/cake_wallet/9679f91a8c9f63d00500c2b7cc18daf00949bdef/cw_zano/lib/zano_wallet.dart) — `9679f91a8c9f63d00500c2b7cc18daf00949bdef`.
- [zano-cake-bip39](https://raw.githubusercontent.com/cake-tech/cake_wallet/9679f91a8c9f63d00500c2b7cc18daf00949bdef/cw_zano/lib/bip39_seed.dart) — `9679f91a8c9f63d00500c2b7cc18daf00949bdef`.
- [sia-list](https://gitlab.com/NebulousLabs/entropy-mnemonics/-/blob/7532f67e35008b0f36bbebb20d5a6ee8f14a22f5/english.go) — `7532f67e35008b0f36bbebb20d5a6ee8f14a22f5`.
- [sia-codec](https://gitlab.com/NebulousLabs/entropy-mnemonics/-/blob/7532f67e35008b0f36bbebb20d5a6ee8f14a22f5/mnemonics.go) — `7532f67e35008b0f36bbebb20d5a6ee8f14a22f5`.
- [sia-codec-vectors](https://gitlab.com/NebulousLabs/entropy-mnemonics/-/blob/7532f67e35008b0f36bbebb20d5a6ee8f14a22f5/mnemonics_test.go) — `7532f67e35008b0f36bbebb20d5a6ee8f14a22f5`.
- [sia-license](https://gitlab.com/NebulousLabs/entropy-mnemonics/-/blob/7532f67e35008b0f36bbebb20d5a6ee8f14a22f5/LICENSE) — `7532f67e35008b0f36bbebb20d5a6ee8f14a22f5`.
- [sia-siad-seed](https://raw.githubusercontent.com/SiaFoundation/siad/66e7fc630585887c30033379d2a0a8bf5c618177/modules/wallet.go) — `66e7fc630585887c30033379d2a0a8bf5c618177`.
- [sia-siad-dependency](https://raw.githubusercontent.com/SiaFoundation/siad/66e7fc630585887c30033379d2a0a8bf5c618177/go.mod) — `66e7fc630585887c30033379d2a0a8bf5c618177`.
- [sia-current-codec](https://raw.githubusercontent.com/SiaFoundation/coreutils/024db888b8bb80b5e54876baaf868c03c9aa0902/wallet/seed.go) — `024db888b8bb80b5e54876baaf868c03c9aa0902`.
- [sia-web-create](https://raw.githubusercontent.com/SiaFoundation/web/f4e3ff774c4f6a5b9830abf1767485215a26a349/apps/walletd/dialogs/WalletAddNewDialog/index.tsx) — `f4e3ff774c4f6a5b9830abf1767485215a26a349`.
- [sia-web-sdk](https://raw.githubusercontent.com/SiaFoundation/web/f4e3ff774c4f6a5b9830abf1767485215a26a349/sdk/wallet.go) — `f4e3ff774c4f6a5b9830abf1767485215a26a349`.
- [sia-server-boundary](https://raw.githubusercontent.com/SiaFoundation/walletd/aa523f95c5b2a106a3c0d9675205c90305d2d9d9/README.md) — `aa523f95c5b2a106a3c0d9675205c90305d2d9d9`.
- [sia-ui-history](https://raw.githubusercontent.com/NebulousLabs/Sia-UI/cd7e221b98fc7a395de25bd8dfaa4f4de2a6e3d2/plugins/Wallet/js/components/initseedform.js) — `cd7e221b98fc7a395de25bd8dfaa4f4de2a6e3d2`.
- [zcash-create](https://raw.githubusercontent.com/zcash/zcash/558f686599586f55def3db86955d74d3be44605e/src/zcash/address/mnemonic.cpp) — `558f686599586f55def3db86955d74d3be44605e`.
- [zcash-ffi](https://raw.githubusercontent.com/zcash/zcash/558f686599586f55def3db86955d74d3be44605e/src/rust/src/zip339_ffi.rs) — `558f686599586f55def3db86955d74d3be44605e`.
- [zcash-standalone](https://raw.githubusercontent.com/zcash/zcash/558f686599586f55def3db86955d74d3be44605e/src/wallet/rpcdump.cpp) — `558f686599586f55def3db86955d74d3be44605e`.
- [zcash-zallet-create](https://raw.githubusercontent.com/zcash/zallet/f9dcd4d31439feb813c95ac2516814421f5b04df/zallet-core/src/commands/generate_mnemonic.rs) — `f9dcd4d31439feb813c95ac2516814421f5b04df`.
- [zcash-zallet-empty](https://raw.githubusercontent.com/zcash/zallet/f9dcd4d31439feb813c95ac2516814421f5b04df/zallet-core/src/components/keystore.rs) — `f9dcd4d31439feb813c95ac2516814421f5b04df`.
- [zcash-zallet-export](https://raw.githubusercontent.com/zcash/zallet/f9dcd4d31439feb813c95ac2516814421f5b04df/book/src/cli/export-mnemonic.md) — `f9dcd4d31439feb813c95ac2516814421f5b04df`.
- [zcash-bip0039](https://raw.githubusercontent.com/koushiro/rust-bips/1a6cc63a53721781aabd695307cc41b82ca76813/bip0039/src/mnemonic.rs) — `1a6cc63a53721781aabd695307cc41b82ca76813`.
- [zcash-bip0039-vector](https://raw.githubusercontent.com/koushiro/rust-bips/1a6cc63a53721781aabd695307cc41b82ca76813/bip0039/src/mnemonic.rs) — `1a6cc63a53721781aabd695307cc41b82ca76813`.
- [zcash-vector-license](https://raw.githubusercontent.com/koushiro/rust-bips/1a6cc63a53721781aabd695307cc41b82ca76813/bip0039/LICENSE-MIT) — `1a6cc63a53721781aabd695307cc41b82ca76813`.
- [chia-source](https://raw.githubusercontent.com/Chia-Network/chia-blockchain/af0d7eab5fb12bbd8af51f47a7123ee700d74c2a/chia/util/keychain.py) — `af0d7eab5fb12bbd8af51f47a7123ee700d74c2a`.
- [chia-vectors](https://raw.githubusercontent.com/Chia-Network/chia-blockchain/af0d7eab5fb12bbd8af51f47a7123ee700d74c2a/chia/_tests/util/bip39_test_vectors.json) — `af0d7eab5fb12bbd8af51f47a7123ee700d74c2a`.
- [chia-license](https://raw.githubusercontent.com/Chia-Network/chia-blockchain/af0d7eab5fb12bbd8af51f47a7123ee700d74c2a/LICENSE) — `af0d7eab5fb12bbd8af51f47a7123ee700d74c2a`.

| Retrieved cache source | Bytes | SHA256 |
| --- | ---: | --- |
| bip0039.crate | 106621 | `568b6890865156d9043af490d4c4081c385dd68ea10acd6ca15733d511e6b51c` |
| cake--bip39_seed.dart | 1888 | `66d9b8ea2bcff2c24e30648c721da20209e049c2fde89cc27461fe96ee27cf17` |
| cake--zano_service.dart | 5693 | `cdf92c7e65a094da6a76a055d7536c61efcb6ee2f597a334934a73ff25977791` |
| cake--zano_wallet.dart | 28225 | `481f9830494a781fe6c533ad9bbb5bde0a5c90f8d1e19bcccadcbd2778d29e37` |
| chia--chia__util__english.txt | 13116 | `2f5eed53a4727b4bf8880d8f3f199efc90e58503646d9ff8eff3a2ed3b24dbda` |
| chia--chia__util__keychain.py | 25431 | `05d3379fc85827a4857d4049240eca54ca2dce2b40e40ce33571acb0c076979e` |
| chia--chia___tests__util__bip39_test_vectors.json | 10283 | `74cbe8870cc8cce5472b3d1e392507ecc2622f90620f0a7e10ff42e3f566379d` |
| chia--keychain-test.py | 24415 | `79c2a3a1178637c5a0621c961eaeb0197918c189239de93b5b1edbeaac16c39a` |
| chia--LICENSE | 11347 | `7db0cf1060026bf2a544ea29cf9a96fba7d3781f93a1d06d6fee18251f1c207a` |
| coreutils--wallet__seed.go | 22514 | `14cc153bae59c48eaaef186f8b4252a9d389b5dd7c1fc2d8e33d91aa822959a1` |
| coreutils-pin--LICENSE | 1085 | `eeee029109f66b6fc8629b57786993390f6903a668d30bf4f9d2fc112043f305` |
| coreutils-pin--wallet__seed.go | 22514 | `14cc153bae59c48eaaef186f8b4252a9d389b5dd7c1fc2d8e33d91aa822959a1` |
| entropy--english.go | 21718 | `08fb5d20e5fbe9c6d23b0a46075c4ad54c6df20318a90c8fa65803b0c3cd9ac7` |
| entropy--LICENSE | 1076 | `a904b29c77a88afe460f6d4f357c75694faafccf4f7b8123c94cbbe0949deed0` |
| entropy--mnemonics.go | 6956 | `4a87b5f62171173390a523b2e6aebf644b59b23c22f22b2a2e32f521ad409f83` |
| entropy--mnemonics_test.go | 10033 | `f79bf4cd99fffd97a257f09a21955feeeb0273509c0411fc1ae4014ed2394f53` |
| entropy-pin--english.go | 21718 | `f9f023d27d902f1778f260dda2adc025fddd104ee6a6ab0b0cf1b62d70eb5bb5` |
| entropy-pin--LICENSE | 1076 | `a904b29c77a88afe460f6d4f357c75694faafccf4f7b8123c94cbbe0949deed0` |
| entropy-pin--mnemonics.go | 6985 | `e6dabeaac37c34a7ce5ee189aa44e7cff7c850a82b008a2b50d5cdeaf7d4dc4f` |
| entropy-pin--mnemonics_test.go | 10033 | `f79bf4cd99fffd97a257f09a21955feeeb0273509c0411fc1ae4014ed2394f53` |
| legal--signpath.html | 19630 | `6610cf889bbe0dc7533abaa310bc7a5cc9a61ae6c2ce0798a08109c925b46c51` |
| sia--go.mod | 1741 | `7c5957f9cac53be465f563ce5cf0d554c5715392d11f7e254c525f45ee97b86d` |
| sia--LICENSE | 1080 | `c5cce4cec9b39b467f3322b10594235fbc37fdc8fce79a8cff6289c6bef8b760` |
| sia--modules__seeds.go | 9591 | `5a2b601f66f68758151b308bbea46624a9abfe78a1ebaeb989918055d08278a2` |
| sia--modules__seeds_test.go | 1078 | `28705e81920090c478b5a5aa1082f295f5e19785660b3a56f6e75735d9521d62` |
| sia--modules__wallet.go | 26434 | `1835fc9093fb730bf6aa0c4994c0286f122becdef32bcd9ad9ca8183204635dc` |
| sia--v2-doc.html | 556864 | `0ed0809acb1fb02a3bee23e25459c4e8349d78b9d3f936692b91bf056d1c5c8d` |
| siaui--package.json | 4450 | `b79a815caf994537c86b7d84624e97d0a06c4a0ab8688d9176af9486454b603f` |
| siaui--plugins__Wallet__js__components__initseedform.js | 1490 | `000708d45db0e8045aa0f0da310e54990f8a052f97907dd951ae57e1f2e45912` |
| walletd--go.mod | 1454 | `034b2a1dd369750ccd5dd3485ebe550657af139f5518a5035dc0ebd1ddaee817` |
| walletd--README.md | 9414 | `8e1f35a4f4b02b38ff8ad42bea24edfda4de27d4c2929f17296a9829c358d0ae` |
| walletd--wallet__seed.go | 4768 | `6e6ee0b042437b3187839d18a3d98c01ba6bd2865d818ca86b65c0583284a2cd` |
| web--apps__walletd__dialogs__FieldMnemonic.tsx | 2322 | `470d9ec9fb4fded305f64707d369057c76f3c0d51ebdf5f55b86055ce43c8018` |
| web--apps__walletd__lib__fieldMnemonic.tsx | 2033 | `0dfc5693d5c77b96fbd8e19254849273b3313f48058d9afa5eb4576b17984010` |
| web--apps__walletd__package.json | 1087 | `7107358a22c5d33be613b87308ae4557861a00290ecf9fee99f95354d1651edf` |
| web--libs__design-system__src__lib__mnemonics.ts | 19626 | `15f86d07c947b8c27f63c60f6e7a0f5b6db2c094523015f9ce1a6a3dd6aa8eae` |
| web--new.tsx | 6308 | `240c150c6ec0806165e11ec56ceb3d3a89105fab2d6112b5ee079daf49bc287c` |
| web--sdk-go.mod | 371 | `72f318769e9a871543daadd893ace69105352bea24fc8a46b3bf4d39c92dc76d` |
| web--sdk-wallet.go | 8706 | `bb1b528935db7a3da3dd1a8edb1fb8e1cd69d8b26ee6a68522f2653f18587a01` |
| zallet--book__src__cli__export-mnemonic.md | 2630 | `fb6e0daba9e9423ab2da4a5cc69d8c8a66834f39bb8216ef3f86251a4feeca4e` |
| zallet--Cargo.lock | 153654 | `8a8c2377429cfdcbe688dd68f2c201ae87c3c80da8c464618088e4e470010e3e` |
| zallet--LICENSE-MIT | 1092 | `d80fdbe401d351ec90483d3c069f0d65e9e3c234e2647cddd36288735df55380` |
| zallet--zallet-core__src__commands__generate_mnemonic.rs | 1732 | `cedc665407b8b48b1cb44879757853512a794bbceeb0a08d1ba425f4f207fe18` |
| zallet--zallet-core__src__commands__import_mnemonic.rs | 1511 | `126194def9cda6f5bfb55b805916196b8e72bc4e192ef505267306e9909e4973` |
| zallet--zallet-core__src__components__keystore.rs | 73070 | `caea8a237179973d4cff680def984debd361dba3449212ea9c97a52fbc5f359d` |
| zano--currency_format_utils.cpp | 254452 | `c9af8db0e7b9d32abee49a0d5a087edc457aa22559f43bbd3b1288353c7a7725` |
| zano--docs.html | 26220 | `f776bddd3bd03f9b58287bd60986b5764c557975dd455dba3310fec57f12be0f` |
| zano--LICENSE | 1263 | `272a94e79145e2dc44fdf3863c80c8e898404ac6fd27802d30f8e2bf573d9855` |
| zano--src__common__mnemonic-encoding.cpp | 57201 | `56b07d67bc786069204816d50fbc7b2763bb3f1730b1274344cdfa1f37631f0c` |
| zano--src__currency_core__account.cpp | 15344 | `5c06f5a469ced8bd4552093b17cae8eef69a9e005eaa7cf70f98a5bad534ef3a` |
| zano--tests__unit_tests__wallet_seed_test.cpp | 10483 | `de3d8d3b5dc9455ad5fe81fbbb422ccebbb7bb7e8b797b00562478de8a26f470` |
| zcash--COPYING | 2168 | `8e30cd61f12d42b612c094376e1cb169a6a235fe70a818d08ed4e527235f2881` |
| zcash--src__wallet__rpcdump.cpp | 40337 | `2173df4638b12c21b6a44f3d399a08bee2fa912ab1eec39ed50884e3827ea62e` |
| zcash--src__wallet__rpcwallet.cpp | 281998 | `969ac1a22d053cffabd148597ddaf00d6a990b6e93e76ffd142779cba6f0f150` |
| zcash--src__zcash__address__mnemonic.cpp | 2700 | `feca12beebc53e931fbb3adfd1e5a9852bec46bc56e4283d1e455f788847a45b` |
| zcash--src__zcash__address__mnemonic.h | 3548 | `ccde4e42aa781aac2129fa8af29f7f4468f83fedd27f3266c795b019120bd8e2` |
| zcash--zip339_ffi.rs | 5916 | `4dbde74efbef3ac7e7e5d78c4c8593527c1e1562d84cfbd59bb567225b330b36` |

Additional dependency-content checks fetched the raw pinned GitHub files and
compared them byte-for-byte to the inspected crate. All three matched:

| Pinned supplementary source | SHA256 |
| --- | --- |
| [bip0039 mnemonic.rs](https://raw.githubusercontent.com/koushiro/rust-bips/1a6cc63a53721781aabd695307cc41b82ca76813/bip0039/src/mnemonic.rs) | `4fd88b5211102c2ff4abbf9fadf77d2bd1061f01f94f794447249ead6df72be3` |
| [bip0039 English](https://raw.githubusercontent.com/koushiro/rust-bips/1a6cc63a53721781aabd695307cc41b82ca76813/bip0039/src/language/english.rs) | `bdb9667233bf0885b4d3947e3f7268113b88fdd6ebbc01be45a8e8cd9c7c855c` |
| [bip0039 MIT](https://raw.githubusercontent.com/koushiro/rust-bips/1a6cc63a53721781aabd695307cc41b82ca76813/bip0039/LICENSE-MIT) | `26cac9a0d229644f0f112fd18cca5919d76d054ca90fb8cdfa119000c0a42383` |
| [siad BLAKE2b hash implementation](https://raw.githubusercontent.com/SiaFoundation/siad/66e7fc630585887c30033379d2a0a8bf5c618177/crypto/hash.go) | `201a83586f8782c21694f50ec866d248c01a0b508a9ff0214e2aaf3a3fbee930` |

Cache source names map to the evidence URLs above; `--` separates repository
label from file path and `__` denotes a slash. `*-pin` is dependency-resolved;
unpinned mirror/HEAD discoveries are not substituted. The complete retrieved
legal terms were inspected; SignPath draft conditions are assessed locally
only. Residual blockers remain visible in every affected record.
