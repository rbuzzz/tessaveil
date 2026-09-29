# Electrum, Substrate and Decred research batch

Reviewed **2026-09-29 UTC** under [source-policy.md](../source-policy.md) and
[licensing.md](../licensing.md). All versions below are singleton source
boundaries. A source package version is not proof that a signed release contains
the inspected code. No wallet was launched, restored, synced or funded; no user
phrase, private key, provider call or removable medium was used.

The batch adds three dictionary metadata records, seven schemes, nine concrete
wallet modes and primary/public evidence. Only the two ISC-licensed PGP halves
are bundled and verified as dictionaries. Schemes and wallet modes remain
documented or blocked, hence non-selectable. Completed research is not release
readiness. The old Electrum dictionary is deliberately absent from `wordlists/`:
its original data-license chain needs further review.

## Exact boundaries and product modes

| Product/source | Revision | Scoped finding |
| --- | --- | --- |
| Electrum 4.8.2 source | `ede66c89887234c83b0def133b3100fe92a160eb` | Qt Windows native English segwit creation; separate legacy v1 and BIP39 import profiles |
| substrate-bip39 0.4.6 | `ceb4fe5a3c7ac91da2e272037797ebecb56aa177` | Entropy-based derivation primitive, not wallet compatibility |
| Polkadot.js extension | `54f44022004f4cefb4a2b929f3a397715a134d6f` | Browser extension default 12-word sr25519 creation, Polkadot/Kusama research target |
| SubWallet extension | `1f9b2a4cb6fea68193e5e012dcca7284a1dd0d80` | General mnemonic handler default 12, sr25519 mode only |
| Talisman 3.10.0 source | `2cee3ef46633cdc3e90bb0fed6855fa25fc87692` | Browser extension Substrate 12/24 mnemonic creation; classic Ethereum/Solana excluded |
| dcrwallet source | `c0fee6b52ad30961cfc3e06017d5e7516952615e` | PGP word arrays, positional codec and double-SHA256 checksum |
| Decrediton 2.1.6 source | `942eed0b34d09316d753942abdbec8dc5320cbed` | Windows native PGP33 creation; no direct BIP39 creation claim |
| Decred documentation source | `30e042a46a97cf78f9766904d3ca4e5ed253266d` | PGP33 versus external BIP39-to-hex conversion |
| Cake Wallet source | `9679f91a8c9f63d00500c2b7cc18daf00949bdef` | Android native15 restore and separate current 12/24 creation; app release version unresolved |
| Cake Android libwallet pin | `ecc4a5fb9594368777848de42d7e072d62406507` | Native format dispatch, no-passphrase native15, NFC deviation in 12/24 |
| dcrdex v1.0.5 resolved commit | `37585833528544f80dddd92dcdff10a78ad01e1f` | Native15 entropy/date/checksum layout |

The upstream repository owners are the official project organizations used by
their published source/documentation; Cake's build script itself identifies
the libwallet repository and full revision, and libwallet's go.mod identifies
dcrdex v1.0.5. The tag was resolved through the GitHub commit API to the full
commit above. No moving branch/tag is used as the evidence revision.

## Electrum generations and licensing boundary

`old_mnemonic.py` contains a fixed 1626-entry tuple. Each 32-bit chunk becomes
three indices: `w1=x%n`, `w2=(x//n+w1)%n`, `w3=(x//n//n+w2)%n`, `n=1626`.
The pinned current legacy recognizer accepts 12 or 24 words and also raw
16/32-byte hex. Its historical lenient recognition is not complete validation.
This batch maps legacy phrase import only; it does not infer which historical
Electrum releases generated every accepted length, nor map raw hex as words.
There is no recovery passphrase for this old mode. The required historical
v1 scheme and dictionary remain blocked.

The file has a complete MIT header, Copyright (C) 2011 thomasv@gitorious, and
explicitly credits the Wiktionary Contemporary poetry frequency list. Root
LICENCE grants MIT for Electrum software, but this review did not establish the
original frequency-list revision, original authors/attribution, or whether
additional data terms apply. The linked Wiktionary page was reviewed as a
provenance lead, not as retroactive permission. Therefore
`repository_redistribution=unclear`, `signpath_compatible=pending`, and
`wordlist_path`/committed `sha256` remain null. The source hash is retained below;
metadata count/order/uniqueness were checked by parsing the literal without
executing the module. No legacy wordlist bytes or misleading license notice
are included in the distributed payload. This conservative result makes no
claim of infringement and can be revisited with the missing provenance.

The [Electrum seed-version documentation](https://electrum.readthedocs.io/en/latest/seedphrase.html)
describes the generation change at 2.0. Current source independently confirms
the difference: native generation uses the same English bytes as `bip39-en`,
but seed type comes from an HMAC-SHA512 `Seed version` prefix. Standard `01`,
segwit `100`, 2FA `101`, and 2FA-segwit `102` are distinct. Normalization uses
NFKD, lowercase, combining-mark removal, whitespace collapse and CJK-space
handling. PBKDF2 uses the normalized sentence, 2048 rounds and `electrum` plus
normalized extension as salt, not BIP39's `mnemonic` salt.

The generation scheme is deliberately scoped to English/default 132-bit
standard/segwit behavior: normally 12 words, with possible 13-word nonce
overflow. Upstream tests explicitly allow 12..13; a fixed public 13-word seed
also demonstrates that 12 is not a universal recognition limit. No arbitrary
CLI entropy length, foreign-language dictionary, 2FA or multisig support is
inferred. Qt WCCreateSeed selects native segwit by default, calls the English
generator and displays the result; a configuration flag selects standard.
Only the segwit concrete wallet profile is added. BIP39 and old restoration
use separate profiles with `generates_mnemonic=false`, `import_only=true`.

## Substrate and Polkadot/Kusama

BIP39 English word encoding/checksum yields 16, 20, 24, 28 or 32 entropy bytes.
substrate-bip39 uses those **bytes** as the PBKDF2 password, `mnemonic` plus
the supplied recovery password as salt, 2048 HMAC-SHA512 rounds, and a 64-byte
result. The mini-secret takes its first 32 bytes. Standard BIP39 instead uses
the sentence. Shared vocabulary/length is not interchangeable derivation.

The raw Rust primitive does not normalize the supplied password. Talisman's
inspected consumer normalizes its salt to NFKD and requests 32 output bytes for
Substrate curves. These are the first 32 bytes of the same primitive for equal
inputs, but arbitrary Unicode-password parity is not assumed. Ethereum/Solana
use its separate sentence-based classic branch. Curve, derivation junctions,
external password, network/address encoding, and hardware mode remain essential
backup context. Tessaveil stores or derives none of these secrets.

Polkadot.js UI creates a fresh seed with default12, displays it, then creates
the selected account; DEFAULT_TYPE is sr25519. Its handler accepts five BIP39
validation lengths, which does not prove five UI creation options. SubWallet's
general handler creates sr25519 plus several other coin types; this record is
only sr25519, excluding TON-native, Ethereum and mobile. Talisman's creation
context explicitly generates 12 and 24, default12. The umbrella scheme's five
lengths describe primitive inputs; they must not be rendered as each wallet's
generation choices. Exact dependency-to-release binding and independent
Polkadot/Kusama restoration are still unverified, so all three are documented.

## Decred PGP33: position determines the half

The official dcrwallet source stores 512 alternating words. Source array
indices `2*b` and `2*b+1` project to 256-word even/odd dictionaries. Preserve
capitalized entries and source order. The decoder compares lowercase strings,
but committed bytes preserve the source spelling; neither half nor their
case-folded union has collisions. Projection is UTF-8 with LF and one final LF.

For a 32-byte seed, 32 word indices are byte values. A 33rd byte is the first
byte of `SHA256(SHA256(seed))`. One-based rows 1,3,...,33 use **pgp-even**;
rows 2,4,...,32 use **pgp-odd**. Even/odd refers to the zero-based position,
never the parity of the byte value. The checksum word is even-half. Unioning
the two halves into a 512-word row would admit invalid candidates.

The position-rule schema currently stores prose strings, not an executable
table selector. The batch records all 33 eligible row halves and tests the
source-backed projections and wrong-half exclusion. It does not add a new
table-generation API or claim user-phrase validation. dcrwallet accepts other
seed byte lengths; those are outside this exact PGP33 scheme. A wallet unlock
password encrypts local keys, not a mnemonic-derived extra wallet.

| Dictionary | Count | Bytes | SHA-256 of committed bytes |
| --- | ---: | ---: | --- |
| pgp-even | 256 | 2024 | `37a65f88512467edd12a1ab3eeb5f4328230e86711a8efde6333361ce10f4fcf` |
| pgp-odd | 256 | 2407 | `c2f23c2233d4d7291107e8f796c374d0cb1fb30c1391bcb4f6480243de8ebf5a` |

The generic Decred BIP39 record reflects the official distinction between
PGP33 and standards-compliant BIP39-capable wallets. It references existing
English words only. Decred documentation describes converting BIP39 to a
binary seed and hex externally for native restoration; this is not direct
Decrediton BIP39 phrase import or generation. No universal path, hardware
model, passphrase equivalence or wallet compatibility is inferred.

## Cake's actual native15 and conflicting current behavior

The dated [Cake documentation](https://docs.cakewallet.com/cryptos/decred/)
says 15-word creation/restoration without an app-version interval. Current
pinned service source instead creates 128-bit/12-word or 256-bit/24-word
BIP39-shaped mnemonics. Both statements remain visible; the documentation is
not silently treated as current source behavior. Exact historical 15-word
creation releases remain unresolved.

For Android, the build pins libwallet, whose go.mod pins dcrdex v1.0.5. Its
native15 decoder is reached for **every 15-word input**, even an ordinary
15-word BIP39 sentence. Dart's permissive precheck does not override native
dispatch. The word list in dcrdex matches all 2048 existing BIP39-English
entries in the same order; Cake's Dart suggestion list and libwallet's separate
list were also compared. No copies or Blue Oak implementation/vector bytes are
bundled merely to prove vocabulary identity.

Native15 carries 144 entropy bits, 16 bits of big-endian days since Unix epoch,
and five leading SHA256 bits over those 20 bytes. The first 13 words carry
143 entropy bits; word14 carries one entropy bit and ten date bits; word15
carries six date bits and five checksum bits. Ordinary BIP39-15 treats all
160 data bits as entropy, so a shared word/checksum shape does not establish
equivalent wallets. libwallet rejects a nonempty recovery passphrase for
native15 and transforms the 18-byte entropy using BLAKE256 with the big-endian
32-bit Decred coin value42 appended. The birthday is retained for recovery
scanning. This is neither PGP33 nor standard BIP39.

`cake-wallet-decred` is the source-bound Android native15 **import** profile;
no current15 creation is asserted. `cake-wallet-decred-bip39` separately records
current12/24 generation. Its native ApplyPassphrase uses **NFC**, whereas
BIP39 requires **NFKD**. ASCII examples cannot prove Unicode compatibility.
Consequently its own `cake-decred-bip39-12-24` scheme and wallet are blocked;
they are not mapped to normative `decred-bip39`. Android binary contents,
Unicode edge cases and independent recovery remain unverified. No iOS, macOS
or Windows behavior is inferred from Android's declared source pin.

## Vectors, licenses and reproduction

`python -m unittest tests.catalog.test_electrum_substrate_decred -v` runs six
offline contracts with CPython3.14.2 and standard-library hashlib/json/unittest.
There are 32 public/reference cases in the fixture, not 32 wallet recoveries:

- Four upstream dcrwallet mnemonicTests have literal expected sentences and
  seed bytes. They cover20/31-byte seeds (21/32 words); they are not mislabeled
  as33. Project sentences to half-local indices and SHA256 fingerprints.
- Two clearly synthetic32-byte inputs (all zero, ascending00..1f) use the
  independently maintained official Decrediton `app/helpers/seed.js` as oracle.
  Verify its raw SHA256 `985754500768714bcb8b084acefaa8b51c6dab0f79ee9857d8cbf3ac4afd1aa8`
  and wordlist SHA256 `dfa89d4ddc3ddbea00069c156437c20e2742ecc51f0c75678ecc8b2f2bbad986`.
  With Node24.13.0, remove only the static wordlist import and export markers,
  supply the unchanged pinned wordlist and Node WebCrypto, and await
  encodeMnemonic for both hex inputs. Store indices and sentence fingerprints
  from its outputs. Tests independently use hashlib double-SHA256 and the
  committed separate halves; expected outputs are not generated by that test.
- Two published Electrum English segwit vectors retain their indices, expected
  seed fingerprints and normalized ASCII passphrase (lowercased as source
  specifies). The expected seed bytes are upstream literals. Tests reproduce
  HMAC seed-type and PBKDF2 fingerprints, and demonstrate BIP39 salt differs.
- Twenty-four published substrate-bip39 VECTORS use password `Substrate`.
  Project literal entropy, sentence indices and upstream expected seed
  fingerprints; reproduce word encoding/checksum and primitive fingerprints.
  Standard sentence-based BIP39 must differ. No addresses or keys are derived.

The fixture extraction uses Python AST for Electrum literals, delimited
source literals for Go vectors/lists and Node only for the inspected pure
Decrediton encoder. The committed fixture is the durable offline artifact;
tests need no Node, Go, upstream module or network. No native15 fixed public
vector was established: upstream dcrdex tests are randomized roundtrips.
Native15 therefore stays documented without invented vector evidence.

The PGP source file explicitly grants ISC; its header and pinned root terms
cover these modified even/odd projections. Copyright and complete ISC terms
are retained in THIRD_PARTY_NOTICES, as are Decrediton's ISC terms for the
reference outputs and Electrum's MIT terms for public test projections.
Substrate vectors carry Apache-2.0 and Copyright2019-2020 Parity Technologies
(UK) Ltd.; modification/attribution are retained and the full Apache text is
already present in the notices and root LICENSE. No software libraries or
wallet binaries are distributed. The legacy Electrum list is excluded.

Codex's separate component-license review on2026-09-29 found the exact PGP ISC
payload compatible with the OSS-license requirement in SignPath's current
draft terms, using the OSI ISC entry plus actual upstream grants. Redistribution
is allowed with notices fulfilled. This is not Foundation acceptance, a
certificate, reputation evidence, or release approval. Scope does not extend
to unbundled libwallet/dcrdex implementations or other wallet dependencies.

Full repository verification uses `python tools/run_tests.py`,
`python -m tools.catalog.cli validate --root . --allow-incomplete-required`,
`python -m tools.catalog.cli generate --root .` then `generate --root . --check`.
The pinned host gate uses `cargo +1.90.0 fmt --check`,
`cargo +1.90.0 check --locked --all-targets`, and `cargo +1.90.0 test --locked`
inside `spikes/mobile/core`. These host checks do not resolve wallet or release
blockers. Exact observed counts and commit are recorded in the task report.

## Source retrieval ledger

The following response-body hashes identify downloaded bytes before source
projection, after HTTP decoding. GitHub URLs pin full commits; mutable pages
are dated2026-09-29 snapshots. Hashes are reproducibility fingerprints, not
signatures or proof of ownership. The raw source review cache is excluded
from the commit. Only approved wordlist/projection bytes enter the payload.

| Retrieved source | Bytes | SHA-256 |
| --- | ---: | --- |
| [cake--docs.html](https://docs.cakewallet.com/cryptos/decred/) | 516873 | `60b015b6925b3c3e8af1cde9b06e34f017f4eb5c53ad8ebc76d2f4fe37100854` |
| [electrum--seedphrase.html](https://electrum.readthedocs.io/en/latest/seedphrase.html) | 40177 | `93d7422d74821ecabd6364a8c3912fea3d0521229bd16b9b3d512537545511e7` |
| [legal--wiktionary.html](https://en.wiktionary.org/wiki/Wiktionary:Frequency_lists/Contemporary_poetry) | 156428 | `4e855a3752e536a70c8526021cb40cb416ddf53dc2f46c9ae95b4e3b917d326a` |
| [legal--isc.html](https://opensource.org/license/isc) | 183820 | `fe58f76539728fb410787c66268597afe5a4a35f223fc2664fb9442d573df9a0` |
| [subwallet--packages__extension-base__src__services__keyring-service__context__handlers__Mnemonic.ts](https://raw.githubusercontent.com/Koniverse/SubWallet-Extension/1f9b2a4cb6fea68193e5e012dcca7284a1dd0d80/packages/extension-base/src/services/keyring-service/context/handlers/Mnemonic.ts) | 7693 | `a878cf20030dd1b7debcb55b0be27ba7b72197365d95877c22431a5b87b17be9` |
| [talisman--apps__extension__package.json](https://raw.githubusercontent.com/TalismanSociety/talisman/2cee3ef46633cdc3e90bb0fed6855fa25fc87692/apps/extension/package.json) | 8185 | `7c8e134dbd8d443fc865d3263318fe1d49f55a5333ff42d8db177f03a3f30b01` |
| [talisman--context.ts](https://raw.githubusercontent.com/TalismanSociety/talisman/2cee3ef46633cdc3e90bb0fed6855fa25fc87692/apps/extension/src/ui/apps/dashboard/routes/Settings/Mnemonics/MnemonicCreateModal/context.ts) | 1923 | `0c74584ed5856e3d1e0a745493fdb6e6ef2e01d5baa15df976f4c43c944c5cbc` |
| [talisman--packages__crypto__src__mnemonic__index.ts](https://raw.githubusercontent.com/TalismanSociety/talisman/2cee3ef46633cdc3e90bb0fed6855fa25fc87692/packages/crypto/src/mnemonic/index.ts) | 3780 | `69a8c5186c5357d88a2eec70513b00725422dfa02ccb28470829fb77ca0d8fa0` |
| [cake--cw_decred__lib__mnemonic.dart](https://raw.githubusercontent.com/cake-tech/cake_wallet/9679f91a8c9f63d00500c2b7cc18daf00949bdef/cw_decred/lib/mnemonic.dart) | 23386 | `311655d3b4ff6ec266879e7728e291c194813d8840ddf3e0275ba41a0577055f` |
| [cake--cw_decred__lib__mnemonic_validation.dart](https://raw.githubusercontent.com/cake-tech/cake_wallet/9679f91a8c9f63d00500c2b7cc18daf00949bdef/cw_decred/lib/mnemonic_validation.dart) | 809 | `ed5e249561c0866155ddea8134c3ada6bbf354f582ab86c4b80b6ad215ace590` |
| [cake--cw_decred__lib__wallet_service.dart](https://raw.githubusercontent.com/cake-tech/cake_wallet/9679f91a8c9f63d00500c2b7cc18daf00949bdef/cw_decred/lib/wallet_service.dart) | 11988 | `52ebe2b13257d5dfd3841d938958d29a46ba8d48ac1d89a00945ffc6610a3a9f` |
| [cake--scripts__android__build_decred.sh](https://raw.githubusercontent.com/cake-tech/cake_wallet/9679f91a8c9f63d00500c2b7cc18daf00949bdef/scripts/android/build_decred.sh) | 2661 | `308575d4520b3f5fa008d0936329f73b0072696fe8fa96b686b449ff6a49d864` |
| [dex--LICENSE.md](https://raw.githubusercontent.com/decred/dcrdex/37585833528544f80dddd92dcdff10a78ad01e1f/LICENSE.md) | 1552 | `8a1af140fdfbf5afd3df27f7e662f989c5b963a300020dfafce42033cae9e004` |
| [dex--client__mnemonic__seed.go](https://raw.githubusercontent.com/decred/dcrdex/37585833528544f80dddd92dcdff10a78ad01e1f/client/mnemonic/seed.go) | 4693 | `99f88584f92b54f0c92b9d3e2bd69fc83cdbef7e70060f08bd43dc645bf985fc` |
| [dex--client__mnemonic__seed_test.go](https://raw.githubusercontent.com/decred/dcrdex/37585833528544f80dddd92dcdff10a78ad01e1f/client/mnemonic/seed_test.go) | 929 | `b8d1e664b28035fbb4f944636d187b6dcbacfb741f8ed7b5bbc1c3fcaaa8173d` |
| [dex--client__mnemonic__words.go](https://raw.githubusercontent.com/decred/dcrdex/37585833528544f80dddd92dcdff10a78ad01e1f/client/mnemonic/words.go) | 21616 | `585467487d475e2b11a1dff64d59350e541071acf2879651bcb5f3fecb140ec7` |
| [docs--docs__advanced__mnemonic-seed.md](https://raw.githubusercontent.com/decred/dcrdocs/30e042a46a97cf78f9766904d3ca4e5ed253266d/docs/advanced/mnemonic-seed.md) | 1926 | `9cdbc465c15b5b515be384fe285143417fa79bb870d3cb78499860df9cef8e65` |
| [decred--LICENSE](https://raw.githubusercontent.com/decred/dcrwallet/c0fee6b52ad30961cfc3e06017d5e7516952615e/LICENSE) | 789 | `9990feefbbca609998b307ced438cb78b331f52eca2337038fe0401db6481acd` |
| [decred--pgpwordlist__pgpwordlist.go](https://raw.githubusercontent.com/decred/dcrwallet/c0fee6b52ad30961cfc3e06017d5e7516952615e/pgpwordlist/pgpwordlist.go) | 1860 | `e8cf7924cedebfa0a1a37db2f0eb0cd8e81a025b0186a789ea33b035d45115c4` |
| [decred--pgpwordlist__wordlist.go](https://raw.githubusercontent.com/decred/dcrwallet/c0fee6b52ad30961cfc3e06017d5e7516952615e/pgpwordlist/wordlist.go) | 5497 | `e97bef5c014c34b9b1f3c013759fbd4ed5cdbce93dba7b5b175d572c9ddec61b` |
| [decred--walletseed__seed.go](https://raw.githubusercontent.com/decred/dcrwallet/c0fee6b52ad30961cfc3e06017d5e7516952615e/walletseed/seed.go) | 3177 | `29642a77483addc3eb6a6334cf9934d44d40f717281d62242f550d4a8a210b4a` |
| [decred--walletseed__seed_test.go](https://raw.githubusercontent.com/decred/dcrwallet/c0fee6b52ad30961cfc3e06017d5e7516952615e/walletseed/seed_test.go) | 3165 | `e80e09d2e12aba12190eea8497fdb0b8c9cf2958d32733a64359c4ffec998542` |
| [decrediton--LICENSE](https://raw.githubusercontent.com/decred/decrediton/942eed0b34d09316d753942abdbec8dc5320cbed/LICENSE) | 741 | `1f7582ae3e1946972711ab1dc84b26cec056f591c52857170efc53dc46b0f88d` |
| [decrediton--app__actions__WalletLoaderActions.js](https://raw.githubusercontent.com/decred/decrediton/942eed0b34d09316d753942abdbec8dc5320cbed/app/actions/WalletLoaderActions.js) | 25261 | `0e1ddc92847ddd81e13a38b8e486fe9b67892fea0aeecaacaf78c1eafe9046a8` |
| [decrediton--app__helpers__seed.js](https://raw.githubusercontent.com/decred/decrediton/942eed0b34d09316d753942abdbec8dc5320cbed/app/helpers/seed.js) | 613 | `985754500768714bcb8b084acefaa8b51c6dab0f79ee9857d8cbf3ac4afd1aa8` |
| [decrediton--app__helpers__wordlist.js](https://raw.githubusercontent.com/decred/decrediton/942eed0b34d09316d753942abdbec8dc5320cbed/app/helpers/wordlist.js) | 7054 | `dfa89d4ddc3ddbea00069c156437c20e2742ecc51f0c75678ecc8b2f2bbad986` |
| [decrediton--package.json](https://raw.githubusercontent.com/decred/decrediton/942eed0b34d09316d753942abdbec8dc5320cbed/package.json) | 12506 | `832b85872d6897a840b3180b35be39950e85c1b6d39463b6107f13038822a9ae` |
| [libwallet--LICENSE.md](https://raw.githubusercontent.com/decred/libwallet/ecc4a5fb9594368777848de42d7e072d62406507/LICENSE.md) | 1552 | `8a1af140fdfbf5afd3df27f7e662f989c5b963a300020dfafce42033cae9e004` |
| [libwallet--cgo__walletloader.go](https://raw.githubusercontent.com/decred/libwallet/ecc4a5fb9594368777848de42d7e072d62406507/cgo/walletloader.go) | 7660 | `c71f460e6795805140541d5b0acf7f66ffb3eb03cf4f8e468b76b76a062e2c84` |
| [libwallet--dcr__loader.go](https://raw.githubusercontent.com/decred/libwallet/ecc4a5fb9594368777848de42d7e072d62406507/dcr/loader.go) | 9937 | `1cfc2fef857df3ad859f56676c19b97e0db3f1b81876f2d8bf9a60b1d3bc4c32` |
| [libwallet--go.mod](https://raw.githubusercontent.com/decred/libwallet/ecc4a5fb9594368777848de42d7e072d62406507/go.mod) | 2195 | `9e15bb61e1b443b520ab46d48cf293fbcb094df0cc48c2d624d540ddc425c692` |
| [libwallet--mnemonic__seed.go](https://raw.githubusercontent.com/decred/libwallet/ecc4a5fb9594368777848de42d7e072d62406507/mnemonic/seed.go) | 4271 | `b623cf0d0903a574b7f54fdfc4c9c25f7dc20e32f4ea5df1a33fcfcae5f66b34` |
| [libwallet--mnemonic__words.go](https://raw.githubusercontent.com/decred/libwallet/ecc4a5fb9594368777848de42d7e072d62406507/mnemonic/words.go) | 21388 | `32ecc346a9ab7f26ed7dfc33b8f2a84798c444efe274dc17995428b5c59754ed` |
| [substrate--Cargo.toml](https://raw.githubusercontent.com/paritytech/substrate-bip39/ceb4fe5a3c7ac91da2e272037797ebecb56aa177/Cargo.toml) | 683 | `eeb6c73f5f0d1931d4dc4cc345a3c84cd1b61a86d640639e13b0ce53d25f27e1` |
| [substrate--LICENSE](https://raw.githubusercontent.com/paritytech/substrate-bip39/ceb4fe5a3c7ac91da2e272037797ebecb56aa177/LICENSE) | 10705 | `b079a8b0300467fd8eb24d145fc5984be7a7954d7fc5120670f7d06d9500d7fa` |
| [substrate--src__lib.rs](https://raw.githubusercontent.com/paritytech/substrate-bip39/ceb4fe5a3c7ac91da2e272037797ebecb56aa177/src/lib.rs) | 12262 | `df887f9ddc001032abc040d733d3901fe18fdf8f225f60fefa68775dcd396be0` |
| [polkadot--packages__extension-base__src__background__handlers__Extension.ts](https://raw.githubusercontent.com/polkadot-js/extension/54f44022004f4cefb4a2b929f3a397715a134d6f/packages/extension-base/src/background/handlers/Extension.ts) | 22206 | `dfb74cc17a121fa71b49c8d169aea9914254b4f18948d8b4535055bd08f82314` |
| [polkadot--packages__extension-ui__src__Popup__CreateAccount__index.tsx](https://raw.githubusercontent.com/polkadot-js/extension/54f44022004f4cefb4a2b929f3a397715a134d6f/packages/extension-ui/src/Popup/CreateAccount/index.tsx) | 4004 | `29987a28fd4d021e4d62a0a1581a019c1b0c05a4c9cc65a3c48dfe10ac263102` |
| [polkadot--defaultType.ts](https://raw.githubusercontent.com/polkadot-js/extension/54f44022004f4cefb4a2b929f3a397715a134d6f/packages/extension-ui/src/util/defaultType.ts) | 226 | `3586d9f1207722e93ec3c9da0ad289b55e990fe889473425e2a225881f783625` |
| [electrum--LICENCE](https://raw.githubusercontent.com/spesmilo/electrum/ede66c89887234c83b0def133b3100fe92a160eb/LICENCE) | 1135 | `fae9c8f29c1493f99de4cd7d4407ff6006e919833e9a8c191b355750ec08a349` |
| [electrum--electrum__gui__qt__wizard__wallet.py](https://raw.githubusercontent.com/spesmilo/electrum/ede66c89887234c83b0def133b3100fe92a160eb/electrum/gui/qt/wizard/wallet.py) | 61229 | `4ac4f7289bd96c6d62af7e3d09dcfa2c4afeb18ebcf4402442ae259fdf3bf06a` |
| [electrum--electrum__mnemonic.py](https://raw.githubusercontent.com/spesmilo/electrum/ede66c89887234c83b0def133b3100fe92a160eb/electrum/mnemonic.py) | 11081 | `22113802b5ae09d1a57fbe004c5773175ee8c5a958237a293717f63f27460570` |
| [electrum--electrum__old_mnemonic.py](https://raw.githubusercontent.com/spesmilo/electrum/ede66c89887234c83b0def133b3100fe92a160eb/electrum/old_mnemonic.py) | 18166 | `9cf503acd21f86cf14c782e456bba4bb38a0999314da25fce899e0d930c39e68` |
| [electrum--electrum__version.py](https://raw.githubusercontent.com/spesmilo/electrum/ede66c89887234c83b0def133b3100fe92a160eb/electrum/version.py) | 758 | `ec35c9ff2273834e1d1d037646550462d1a36fdc251fa319c5725c2c155a7311` |
| [electrum--electrum__wizard.py](https://raw.githubusercontent.com/spesmilo/electrum/ede66c89887234c83b0def133b3100fe92a160eb/electrum/wizard.py) | 42867 | `0e6a88e27e42afb677ae2cfec165078499679388a3c207443e1d65e648b630d2` |
| [electrum--electrum__wordlist__english.txt](https://raw.githubusercontent.com/spesmilo/electrum/ede66c89887234c83b0def133b3100fe92a160eb/electrum/wordlist/english.txt) | 13116 | `2f5eed53a4727b4bf8880d8f3f199efc90e58503646d9ff8eff3a2ed3b24dbda` |
| [electrum--tests__test_mnemonic.py](https://raw.githubusercontent.com/spesmilo/electrum/ede66c89887234c83b0def133b3100fe92a160eb/tests/test_mnemonic.py) | 18315 | `b4f6465869b2781607d4cc56ce0291881247d449899696013ff58d9fd9e855c6` |
| [legal--signpath.html](https://signpath.org/terms.html) | 19630 | `6610cf889bbe0dc7533abaa310bc7a5cc9a61ae6c2ce0798a08109c925b46c51` |
