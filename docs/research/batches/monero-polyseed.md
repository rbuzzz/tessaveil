# Monero, MyMonero and Polyseed — Task 11

Reviewed UTC: 2026-09-29. Scope: research data only; no production key derivation,
complete user-phrase validation, real wallet, funds, provider submission or Rust
change. Apply [source policy](../source-policy.md) and [licensing](../licensing.md).
The original physical-device, filesystem, format-freeze and signing gates remain
NO-GO. Dictionary verification does not make a wallet profile selectable.

## Results and honest limits

All 23 requested dictionaries are present: 13 Monero lists of 1626 words and 10
Polyseed lists of 2048 words. Five dictionary records are verified by a fixed
public-vector projection: monero-en/de/pt and polyseed-en/es. The other 18 are
documented: exact source order, hashes, counts, normalization and licenses pass,
but an independent deterministic language-specific mnemonic example was not
reproduced. Upstream random all-language roundtrips are not presented as fixed
known-answer evidence. These 18 lists are licensed research payload, not selectable
support. EnglishOld has `historical=true`, independently of its documented status.

The three schemes and eleven concrete wallet modes are documented. Their precise
source-backed rules are retained, but full independent key/address derivation and
exact released application artifact bindings are not verified. No record uses
`no-mnemonic-confirmed`: insufficient evidence and discontinued XMR management do
not prove absence of exportable backup words. `generates_mnemonic=false` in the
Exodus export profile means this record covers export, not new-wallet generation.

Only 31 Task 11 required entries are closed. Existing manifest IDs are preserved:
`scheme-mymonero` points to `mymonero-13`, `scheme-polyseed` to `polyseed-16`,
`wallet-cake-wallet` to `cake-wallet-monero`, and `wallet-exodus-monero` to
`exodus-monero-export`. The generic Cake requirement is resolved only for its
Monero mode; other Cake chains remain separate requirements. Network closure and
all later research batches remain pending (112 warnings, zero errors).

## Scheme distinctions and lifecycle

- `monero-legacy`: 24 data words from eight little-endian 32-bit values, with three
  base-1626 indices per value; CRC32 of language-specific word prefixes chooses a
  repeated 25th checksum word. Checksumless restoration forms are not the standard
  25-word profile. A wallet seed offset may be an additional external secret.
- `mymonero-13`: 12 data words encode 16 bytes, plus a checksum. MyMonero's core
  hashes the short seed with Keccak before scalar reduction; this differs from
  simply restoring the same words with Monero's 32-byte legacy decoder. Current
  pinned MyMonero core new_wallet generates 32-byte/25-word seeds. The 13-word
  format is retained by its legacy decoder; no historical app cutoff was inferred.
- `polyseed-16`: 150 secret bits, five feature bits, ten birthday bits and an
  11-bit GF(2048) checksum. The checksum is the first word, not the last. The
  second coefficient is coin-domain separated. Key derivation uses
  PBKDF2-HMAC-SHA256 with 10000 iterations; optional seed encryption has a separate
  passphrase. Neither algorithm nor the modified word orders are BIP39.

The standard Monero generation language list has twelve languages. EnglishOld is
recognized by the restore language search but excluded from generation; its four
character prefixes deliberately permit duplicates and short words. Keep its
1626-entry order distinct from current English and do not infer a selectable
historical 25-word generator from its presence. The scheme references only the
twelve current generation dictionaries; EnglishOld remains independently visible.

## Source bytes, order and normalization

Sources are upstream C/C++ arrays, not plain text files. The stored word lists are
explicit source projections: isolate `words[NWORDS]` (Monero) or `.words` (Polyseed),
read each anchored quoted UTF-8 literal (optional `u8` prefix), remove only source
indentation, quotes and commas, and append LF to each token, including the last.
All selected literals have no C escape sequence. Do not sort, translate, lowercase,
or normalize the tokens. Thus source-file hashes and extracted-file hashes are
different and are recorded separately below and in the public fixture.

Monero does not perform Unicode NFC/NFKD normalization in its reviewed lookup.
`language_base.h` calls `utf8canonical` with `towlower`; inspected `src/common/utf8.h`
re-encodes transformed codepoints without Unicode decomposition/composition.
Case-insensitive and prefix matching are input conveniences, not permission to
rewrite dictionary bytes. The new `normalization=none` schema value means retain
the source characters; validator still checks exact duplicates and unique counts.
It is covered by behavioral tests and the external JSON Schema parity test.

Polyseed requires stored NFKD words. Its decoder decomposes input, while encoding
can compose NFC for language flags. Latin prefixes, Spanish/French accent-insensitive
comparison and Japanese U+3000 separators are separate rules. Spanish order is
accent-insensitive; Japanese uses ordinal order; Czech fixes BIP39's order. Those
three projected lists differ byte-for-byte from their BIP39 counterparts. The
other seven can share vocabulary bytes, but retain separate source identity and
incompatible scheme semantics. All 23 lists have full-word uniqueness under both
NFC and NFKD; that does not imply unique EnglishOld prefixes.

## Wallet evidence boundaries

Wallet identity is product + platform + exact version interval + specific mode.
All source intervals in this batch are singleton full commits, not claims about
every binary with a similar package version. Multiple modes of Cake, Feather,
Monero CLI and MyMonero coexist without a conflict. The batch test rejects duplicate
identities and non-singleton intervals; generalized mixed interval conflict handling
remains Task 15's scope.

Monero CLI's reviewed development source declares version 0.18.1.0, but the exact
commit is authoritative: it now defaults to Polyseed and offers `--use-legacy-seed`.
`seed` and `legacy_seed` display paths are visible separately. The historical required
ID `monero-gui-cli` scopes only the CLI legacy mode; a separate `monero-gui` record
does not pretend GUI/backend revision equivalence. GUI creates an in-memory wallet
and displays wallet.seed; backend mapping remains unresolved, hence null scheme.

MyMonero app 1.3.2 source displays a generated mnemonic; separately pinned core
source creates 25 and restores 13/25. The app's dependency ranges do not bind that
exact core revision. Its generated mode is therefore unmapped. The 13-word restore
record is only a documented candidate mapping, with the binding gap explicit.

Feather 2.9.1 source creates English Polyseed only. Legacy 25-word restoration is
an import-only profile (the code also accepts checksumless 24). Its 14-word Tevador
restoration format is not Polyseed or MyMonero and is not silently catalogued as one.
Cake's Android source exposes legacy 25, Polyseed 16 default and BIP39-derived 12
choices; all three branches coexist. The generated version template says 0.0.0,
so only the source commit is used as its version bound. The BIP39-derived Monero
mode is deliberately unmapped pending separate derivation research. The seed
backup view and seed getter were inspected separately from restore/create branches;
no iOS/desktop executable equivalence or full FFI recovery was executed.

Exodus's official article, published update 2026-01-20, documents XMR support ending
2025-08-18 while retaining Desktop 25-word export. Its Cake instructions explicitly
select Legacy (25), English. The Windows Desktop export path is scoped here;
Mobile must sync to Desktop. The global 12-word Exodus backup and importing into
Cake are distinct. No 25-word import-into-Exodus or new XMR creation claim is made.
The article names no app version: the interval is explicitly version-unresolved,
not an invented release number. Web retrieval exposed the article; direct HTTP
body requests returned 403. We record its published revision and review date,
not a fictitious byte hash or immutable archive.

## Licensing and SignPath component assessment

The exact dictionary headers were inspected, not just repository badges.
Most Monero arrays are BSD-3-Clause with Monero copyright; Spanish, Portuguese,
Japanese and Chinese Simplified explicitly license the word lists under MIT by
dabura667, while surrounding code is BSD. Contributor attribution includes Shrikez,
sammy007, dnaleor, Engelberg, ProkhorZ, sorpaas and Thomas Voegtlin's EnglishOld
origin. Full per-file leading notices, relevant root LICENSE and disclaimer text
are retained in [THIRD_PARTY_NOTICES](../../../THIRD_PARTY_NOTICES), with only
trailing whitespace removed from displayed comment lines.

Polyseed arrays and test projections use Apache-2.0, with cumulative MIT obligations
for BIP39-derived words. The entire upstream NOTICE and Apache license are retained;
the transformation is prominently described in the dictionary metadata, this note
and notices. No upstream executable or wallet dependency is bundled. MyMonero's
public test projection uses its pinned core repository BSD-3-Clause terms, with
the complete MyMonero copyright and license retained as well.

Its [exact LICENSE.txt](https://raw.githubusercontent.com/mymonero/mymonero-core-cpp/9637c91cbe5f46e67156c66c739932294808109d/LICENSE.txt)
is 1585 bytes, SHA-256
`c7c911457cac352c3d79c43cde1dc26a2c0355234e737060cac7a786647ac87f`.

For these exact research-data projections: repository_redistribution=allowed and
signpath_compatible=compatible. The separate component assessment rests on actual
source terms, OSI BSD/MIT/Apache approval and the reviewed SignPath OSS conditions;
no commercial dual-license requirement was identified for this payload. It does
not establish Foundation acceptance, a certificate, SmartScreen reputation, project
security eligibility or permission to ship a release. Reassess any future binary,
dependency or changed data revision independently.

## Public reproduction and validation

Fixture: `tests/catalog/fixtures/public/monero-polyseed.json`; public, non-funded
test material only. It stores indices and phrase fingerprints, not full sentences.
Expected byte hashes derive from pinned source extraction, not the catalogue hash.

- Monero's public Portuguese and German examples exercise prefix CRC32 checks.
- MyMonero's published 13-word prefix example and published 16-byte input map to
  the same expected address upstream. Our test checks decoded entropy and checksum,
  not Keccak, scalar reduction or address generation.
- Polyseed's fixed English/Spanish inputs, phrases and birthday assertions exercise
  NFKD, dictionary order, GF polynomial checksum and embedded secret/date/features.
  Its upstream test uses a dummy PBKDF2 callback that asserts inputs, so it is not
  a public derived-key known answer. No derived-key output is invented here.

Tests run offline with Python 3.14.2 standard hashlib/zlib/unicodedata and the existing
pinned JSON Schema engine. No upstream wallet or downloaded executable is run.
The test catches missing IDs, altered order/bytes/counts, false status promotion,
lost lifecycle flags, broken required references, source-pin/backlink errors,
BIP39 substitution, mode conflation and generated EN/RU omission. The general
validator now supports source-native `none` without dropping duplicate checks.
Empty optional aliases now render the existing absent-value marker rather than
trailing whitespace; that change was tested RED before implementation.

Commands:

```text
python -m unittest tests.catalog.test_monero_polyseed tests.catalog.test_validator -v
python -m tools.catalog.cli validate --root . --allow-incomplete-required
python -m tools.catalog.cli generate --root .
python -m tools.catalog.cli generate --root . --check
python tools/run_tests.py
git diff --check
```

The SDD report records the observed RED/GREEN runs, complete test totals and commit.
Research completion closes these entries only; future vectors and artifact binding
are needed before promoting the documented profiles.

## Exact dictionary fingerprint ledger

Hashes identify bytes, not authenticity or license approval. Each source link in
its dictionary evidence contains the complete commit SHA. Source paths and source
byte lengths are also recorded in the fixture.

| Dictionary | Count | Stored bytes | Stored SHA-256 | Source-file SHA-256 |
| --- | ---: | ---: | --- | --- |
| monero-de | 1626 | 12349 | `e1e6653cf418e0a392a5cd34160a8cdacb5dfce8edbac0e124fba8d7daff1f69` | `7b910a96bc94d19eb3e4edd8179db383a68b03a7608396bbee0fdc46a7d4e88e` |
| monero-en | 1626 | 11467 | `eaa6bce7dd92f4d6dd74f224264e0ef4ad21095d68ec77616b26ceb599baf4f7` | `9bd756d29e689aae0e6e7f8b1196c4f35df350225c4668d4f6f41842f05fc2ca` |
| monero-en-old | 1626 | 10494 | `c8da327d316f8ee758b790068e618077ac271a89fd77ec1250c59ae40e7b599e` | `20c9090994c5b441f2e550cddbf266d604b64e495d9b172e45a8031e1aa5d578` |
| monero-eo | 1626 | 12086 | `aa53b9b2af6586e8df69bcf04b17af4f06cac9e7ad20420d45b265f9aa18b32d` | `382d9f9bfcf293e4dc9f156042fe5a3f2a151191bae368a494eaf53c77e16043` |
| monero-es | 1626 | 10898 | `05da8a20ae4a5af8fc1bd02d20d1282cf72ce1a6c98b9be60b1eff4c79d424fb` | `994a941260f53e066753204f4b92c20bb1d830b58e76ff89c2caa71c34d546ef` |
| monero-fr | 1626 | 10898 | `b17376bb1341cc32b8a7088d23c0dba3b25743c167f4e4f3d8062946ffd93e87` | `f4e42ab4eb9824a2cd829f132e33dfc46ae31c5788a37c9726d393e7cc809a82` |
| monero-it | 1626 | 12774 | `aea041cbb43e8e3b817b48b64001df3e28949002d99c920a8a46231319bcc121` | `d02956b528db827646a1f6f78c1a19716b9334985cb893eb09409834a04045db` |
| monero-ja | 1626 | 19428 | `0e879f11f3806e6b25738598cfec6f372364af7fb8c59b4874d7a406f6b0fee7` | `3701f067006b60e95e266e7a385b472c5bddeb6f476e737eed6d3b7febefe6d5` |
| monero-jbo | 1626 | 9934 | `19c3f71b26c808bbe9ed7ab944ac1c8b1f11307f96d27d01874c093520c972f9` | `6c84dedd2609060f30368b92b5e377207e28afcda5401b5060d57c633e623a04` |
| monero-nl | 1626 | 12720 | `9b2005b2c4d95360361949c7f5b43ef6a021d3ce31f01f6101a24d93540e790a` | `775d05f737f453d6798876d99961bb3bcfc49d47cb57860d3c0b2a03b9a64822` |
| monero-pt | 1626 | 13139 | `9099aaa5470c568ca91f0040222760af55720ddc3f3a6f9e1736d4c2dd9247da` | `0a6b191930a29f1ae827c1f5f8905548035bac5e5b41386f0978cf39e4adcfa1` |
| monero-ru | 1626 | 20750 | `fd225689dda9d342acae6bd58ecbdba3274ded07d89936ce979a95f6d60c64ea` | `2d3f282d11e917fcdd6248b87002f5b982b6abaa773e9676d21886b6a50a4762` |
| monero-zh-hans | 1626 | 6504 | `d0b846b2036f55182892d98c2410996c399ed3aee5be2d6cbfaf594e599dd522` | `4a38fbe7279616aa78aa11dbcf425d0ba5305fd2089cb4421d544f2c540d50fd` |
| polyseed-cs | 2048 | 14945 | `195136b3ba0f3099a9df625e0963f4efb56625b91c3a76bc5b4a9466a26880f7` | `395c70fb0de3e4c9034da698c679269227c1783d0ae56617bb8bcfd950eb9cd3` |
| polyseed-en | 2048 | 13116 | `2f5eed53a4727b4bf8880d8f3f199efc90e58503646d9ff8eff3a2ed3b24dbda` | `6e32fb9d56d5c8a304d173937deec9dc9d64e52d15a9104f1c63dc45b7911f47` |
| polyseed-es | 2048 | 13996 | `31e589970a7490b1d62534c57b97b65b7d8ec7e7fcdad4830af1e324ed387c52` | `90405262a658434062b1d26cc7799c1d7fbeb11486c93a01153c733315c0cc0d` |
| polyseed-fr | 2048 | 16777 | `ebc3959ab7801a1df6bac4fa7d970652f1df76b683cd2f4003c941c63d517e59` | `0cb937a44ac79218a35e4d10f757d85dcd482cb4ed1482928644d0292ab8f0e2` |
| polyseed-it | 2048 | 16033 | `d392c49fdb700a24cd1fceb237c1f65dcc128f6b34a8aacb58b59384b5c648c2` | `211787e3a762b7b55e7f2f422dc16e843399697ef078b10b2773ba62972a312a` |
| polyseed-ja | 2048 | 26423 | `438b4d19c4af485650822ae0d08855090a6812e2a2ed6fb793583ae90f3e6248` | `c309fd0d6c435de214262dd5c96331b8a48bd9a9a3b3b6659d2817056ecc1887` |
| polyseed-ko | 2048 | 37832 | `9e95f86c167de88f450f0aaf89e87f6624a57f973c67b516e338e8e8b8897f60` | `0b56d27f7c1d3c6d13af9248d981d90a7d515222e3858fe6eca2f1aae7ea6ac9` |
| polyseed-pt | 2048 | 15671 | `2685e9c194c82ae67e10ba59d9ea5345a23dc093e92276fc5361f6667d79cd3f` | `40e9919edf8b768a12cdfc3c3cd2343fa16a628ad0e8d2749b4c026af7c9bf70` |
| polyseed-zh-hans | 2048 | 8192 | `5c5942792bd8340cb8b27cd592f1015edf56a8c5b26276ee18a482428e7c5726` | `cabe21517dcde33e517926ab29d7b58bb5e5f97b7b5a6a631e9137f256a5165b` |
| polyseed-zh-hant | 2048 | 8192 | `417b26b3d8500a4ae3d59717d7011952db6fc2fb84b807f3f94ac734e89c1b5f` | `7ddbd0546736c7e53077b97bef5f6697f752f6a78ea7e4429987b66f14a118ba` |

## Primary-source retrieval ledger

All files below were fetched and inspected at the pinned revisions on 2026-09-29.
Unquoted implementation files are references only, not redistributed code.

| Source | Exact source URL | Byte SHA-256 |
| --- | --- | --- |
| monero/LICENSE | [source](https://raw.githubusercontent.com/monero-project/monero/2f9d1bbb2c553dc75f3335bd1452117dfddd86fa/LICENSE) | `1f99d6b6e1ae17de27147ff2e1e0238fa8c7d5a8accd0f1ac062c89365516abd` |
| monero/cmake/Version.cmake | [source](https://raw.githubusercontent.com/monero-project/monero/2f9d1bbb2c553dc75f3335bd1452117dfddd86fa/cmake/Version.cmake) | `e6275da2065e6d155fe0077b4a919ed1dbc2695e36800b601c91c225a68b307c` |
| monero/src/mnemonics/electrum-words.cpp | [source](https://raw.githubusercontent.com/monero-project/monero/2f9d1bbb2c553dc75f3335bd1452117dfddd86fa/src/mnemonics/electrum-words.cpp) | `f92675503096425c92f6cc8b38946a707db6999cfcd95657f87a58d364051e4f` |
| monero/src/mnemonics/language_base.h | [source](https://raw.githubusercontent.com/monero-project/monero/2f9d1bbb2c553dc75f3335bd1452117dfddd86fa/src/mnemonics/language_base.h) | `2bc256f01c6904af914cb7c6526254267ed463882e216fd0eb1d9bbdf4bf5bb4` |
| monero/tests/unit_tests/mnemonics.cpp | [source](https://raw.githubusercontent.com/monero-project/monero/2f9d1bbb2c553dc75f3335bd1452117dfddd86fa/tests/unit_tests/mnemonics.cpp) | `520fec49e96e4b01d472f627e109b7a343f80e58291eed793f7ca76f2e63a1d1` |
| monero/src/simplewallet/simplewallet.cpp | [source](https://raw.githubusercontent.com/monero-project/monero/2f9d1bbb2c553dc75f3335bd1452117dfddd86fa/src/simplewallet/simplewallet.cpp) | `54534a83e1c17bf4d5176dbdb2c1293399575058ad4db3f58948c958bda3ff15` |
| monero/src/mnemonics/english.h | [source](https://raw.githubusercontent.com/monero-project/monero/2f9d1bbb2c553dc75f3335bd1452117dfddd86fa/src/mnemonics/english.h) | `9bd756d29e689aae0e6e7f8b1196c4f35df350225c4668d4f6f41842f05fc2ca` |
| monero/src/mnemonics/german.h | [source](https://raw.githubusercontent.com/monero-project/monero/2f9d1bbb2c553dc75f3335bd1452117dfddd86fa/src/mnemonics/german.h) | `7b910a96bc94d19eb3e4edd8179db383a68b03a7608396bbee0fdc46a7d4e88e` |
| monero/src/mnemonics/spanish.h | [source](https://raw.githubusercontent.com/monero-project/monero/2f9d1bbb2c553dc75f3335bd1452117dfddd86fa/src/mnemonics/spanish.h) | `994a941260f53e066753204f4b92c20bb1d830b58e76ff89c2caa71c34d546ef` |
| monero/src/mnemonics/french.h | [source](https://raw.githubusercontent.com/monero-project/monero/2f9d1bbb2c553dc75f3335bd1452117dfddd86fa/src/mnemonics/french.h) | `f4e42ab4eb9824a2cd829f132e33dfc46ae31c5788a37c9726d393e7cc809a82` |
| monero/src/mnemonics/italian.h | [source](https://raw.githubusercontent.com/monero-project/monero/2f9d1bbb2c553dc75f3335bd1452117dfddd86fa/src/mnemonics/italian.h) | `d02956b528db827646a1f6f78c1a19716b9334985cb893eb09409834a04045db` |
| monero/src/mnemonics/dutch.h | [source](https://raw.githubusercontent.com/monero-project/monero/2f9d1bbb2c553dc75f3335bd1452117dfddd86fa/src/mnemonics/dutch.h) | `775d05f737f453d6798876d99961bb3bcfc49d47cb57860d3c0b2a03b9a64822` |
| monero/src/mnemonics/portuguese.h | [source](https://raw.githubusercontent.com/monero-project/monero/2f9d1bbb2c553dc75f3335bd1452117dfddd86fa/src/mnemonics/portuguese.h) | `0a6b191930a29f1ae827c1f5f8905548035bac5e5b41386f0978cf39e4adcfa1` |
| monero/src/mnemonics/russian.h | [source](https://raw.githubusercontent.com/monero-project/monero/2f9d1bbb2c553dc75f3335bd1452117dfddd86fa/src/mnemonics/russian.h) | `2d3f282d11e917fcdd6248b87002f5b982b6abaa773e9676d21886b6a50a4762` |
| monero/src/mnemonics/japanese.h | [source](https://raw.githubusercontent.com/monero-project/monero/2f9d1bbb2c553dc75f3335bd1452117dfddd86fa/src/mnemonics/japanese.h) | `3701f067006b60e95e266e7a385b472c5bddeb6f476e737eed6d3b7febefe6d5` |
| monero/src/mnemonics/chinese_simplified.h | [source](https://raw.githubusercontent.com/monero-project/monero/2f9d1bbb2c553dc75f3335bd1452117dfddd86fa/src/mnemonics/chinese_simplified.h) | `4a38fbe7279616aa78aa11dbcf425d0ba5305fd2089cb4421d544f2c540d50fd` |
| monero/src/mnemonics/esperanto.h | [source](https://raw.githubusercontent.com/monero-project/monero/2f9d1bbb2c553dc75f3335bd1452117dfddd86fa/src/mnemonics/esperanto.h) | `382d9f9bfcf293e4dc9f156042fe5a3f2a151191bae368a494eaf53c77e16043` |
| monero/src/mnemonics/lojban.h | [source](https://raw.githubusercontent.com/monero-project/monero/2f9d1bbb2c553dc75f3335bd1452117dfddd86fa/src/mnemonics/lojban.h) | `6c84dedd2609060f30368b92b5e377207e28afcda5401b5060d57c633e623a04` |
| monero/src/mnemonics/english_old.h | [source](https://raw.githubusercontent.com/monero-project/monero/2f9d1bbb2c553dc75f3335bd1452117dfddd86fa/src/mnemonics/english_old.h) | `20c9090994c5b441f2e550cddbf266d604b64e495d9b172e45a8031e1aa5d578` |
| monero/src/common/utf8.h | [source](https://raw.githubusercontent.com/monero-project/monero/2f9d1bbb2c553dc75f3335bd1452117dfddd86fa/src/common/utf8.h) | `584f39c455b3693c6ad5870e5ec4e1ddc065497d86a6ecd18569c388498305e9` |
| monero/src/version.cpp.in | [source](https://raw.githubusercontent.com/monero-project/monero/2f9d1bbb2c553dc75f3335bd1452117dfddd86fa/src/version.cpp.in) | `cddb09cd7a59eefe5486766145baf2849a9161a504545a649d83e034a81ea83a` |
| polyseed/LICENSE | [source](https://raw.githubusercontent.com/tevador/polyseed/56f634647d4f75596de20a6259b0cf1933949fdc/LICENSE) | `cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30` |
| polyseed/NOTICE | [source](https://raw.githubusercontent.com/tevador/polyseed/56f634647d4f75596de20a6259b0cf1933949fdc/NOTICE) | `442cd16cdc8913cd76a9f7bd1047a0aea68ede782d94db3556392e18f39ad64e` |
| polyseed/README.md | [source](https://raw.githubusercontent.com/tevador/polyseed/56f634647d4f75596de20a6259b0cf1933949fdc/README.md) | `51abea48365ac1e4f8fb364be55a69550f81e265d6d96487c418e223789845d8` |
| polyseed/CMakeLists.txt | [source](https://raw.githubusercontent.com/tevador/polyseed/56f634647d4f75596de20a6259b0cf1933949fdc/CMakeLists.txt) | `de907754ca1641c392a5b8fd86a0fd4ac1848a56fed09e6239c0834f27f76ff1` |
| polyseed/src/lang.c | [source](https://raw.githubusercontent.com/tevador/polyseed/56f634647d4f75596de20a6259b0cf1933949fdc/src/lang.c) | `f30f867f5afd3bab323d85a8678868862d94dde09ed7801ab45a74f9b563b447` |
| polyseed/src/lang.h | [source](https://raw.githubusercontent.com/tevador/polyseed/56f634647d4f75596de20a6259b0cf1933949fdc/src/lang.h) | `5b2d7c6e579fcf532d4083a1b2bc0c52642d2231d0068bfdafecd75bc2bb6af6` |
| polyseed/src/polyseed.c | [source](https://raw.githubusercontent.com/tevador/polyseed/56f634647d4f75596de20a6259b0cf1933949fdc/src/polyseed.c) | `b2212792a019b0fa50676397448bf2df3b1e035bbf60f8b94f1c84bdf78b5079` |
| polyseed/tests/tests.c | [source](https://raw.githubusercontent.com/tevador/polyseed/56f634647d4f75596de20a6259b0cf1933949fdc/tests/tests.c) | `3bc51ff2c12c3840e93d5e87a8da47516f806e3d51dc72ea6049f7f439dba4d5` |
| polyseed/src/lang_en.c | [source](https://raw.githubusercontent.com/tevador/polyseed/56f634647d4f75596de20a6259b0cf1933949fdc/src/lang_en.c) | `6e32fb9d56d5c8a304d173937deec9dc9d64e52d15a9104f1c63dc45b7911f47` |
| polyseed/src/lang_jp.c | [source](https://raw.githubusercontent.com/tevador/polyseed/56f634647d4f75596de20a6259b0cf1933949fdc/src/lang_jp.c) | `c309fd0d6c435de214262dd5c96331b8a48bd9a9a3b3b6659d2817056ecc1887` |
| polyseed/src/lang_ko.c | [source](https://raw.githubusercontent.com/tevador/polyseed/56f634647d4f75596de20a6259b0cf1933949fdc/src/lang_ko.c) | `0b56d27f7c1d3c6d13af9248d981d90a7d515222e3858fe6eca2f1aae7ea6ac9` |
| polyseed/src/lang_es.c | [source](https://raw.githubusercontent.com/tevador/polyseed/56f634647d4f75596de20a6259b0cf1933949fdc/src/lang_es.c) | `90405262a658434062b1d26cc7799c1d7fbeb11486c93a01153c733315c0cc0d` |
| polyseed/src/lang_fr.c | [source](https://raw.githubusercontent.com/tevador/polyseed/56f634647d4f75596de20a6259b0cf1933949fdc/src/lang_fr.c) | `0cb937a44ac79218a35e4d10f757d85dcd482cb4ed1482928644d0292ab8f0e2` |
| polyseed/src/lang_it.c | [source](https://raw.githubusercontent.com/tevador/polyseed/56f634647d4f75596de20a6259b0cf1933949fdc/src/lang_it.c) | `211787e3a762b7b55e7f2f422dc16e843399697ef078b10b2773ba62972a312a` |
| polyseed/src/lang_cs.c | [source](https://raw.githubusercontent.com/tevador/polyseed/56f634647d4f75596de20a6259b0cf1933949fdc/src/lang_cs.c) | `395c70fb0de3e4c9034da698c679269227c1783d0ae56617bb8bcfd950eb9cd3` |
| polyseed/src/lang_pt.c | [source](https://raw.githubusercontent.com/tevador/polyseed/56f634647d4f75596de20a6259b0cf1933949fdc/src/lang_pt.c) | `40e9919edf8b768a12cdfc3c3cd2343fa16a628ad0e8d2749b4c026af7c9bf70` |
| polyseed/src/lang_zh_s.c | [source](https://raw.githubusercontent.com/tevador/polyseed/56f634647d4f75596de20a6259b0cf1933949fdc/src/lang_zh_s.c) | `cabe21517dcde33e517926ab29d7b58bb5e5f97b7b5a6a631e9137f256a5165b` |
| polyseed/src/lang_zh_t.c | [source](https://raw.githubusercontent.com/tevador/polyseed/56f634647d4f75596de20a6259b0cf1933949fdc/src/lang_zh_t.c) | `7ddbd0546736c7e53077b97bef5f6697f752f6a78ea7e4429987b66f14a118ba` |
| polyseed/src/gf.c | [source](https://raw.githubusercontent.com/tevador/polyseed/56f634647d4f75596de20a6259b0cf1933949fdc/src/gf.c) | `8a8b3bac87e42de108ce0095f0d4d115ecb0969c693770cef2538224110a7d4c` |
| polyseed/src/storage.c | [source](https://raw.githubusercontent.com/tevador/polyseed/56f634647d4f75596de20a6259b0cf1933949fdc/src/storage.c) | `65114da0060a6986d2f26caed7a16dd26012b40b4b444e4c42e4c792bfe31fa3` |
| polyseed/src/birthday.h | [source](https://raw.githubusercontent.com/tevador/polyseed/56f634647d4f75596de20a6259b0cf1933949fdc/src/birthday.h) | `64ecece95280bae14d0511d75555334f90cdb364bddfd957322d75d0a18d8ed7` |
| mymonero/LICENSE.txt | [source](https://raw.githubusercontent.com/mymonero/mymonero-core-js/ad21d528d2202300349e6f303af9be649c53eb66/LICENSE.txt) | `c7c911457cac352c3d79c43cde1dc26a2c0355234e737060cac7a786647ac87f` |
| mymonero/README.md | [source](https://raw.githubusercontent.com/mymonero/mymonero-core-js/ad21d528d2202300349e6f303af9be649c53eb66/README.md) | `d1f4e5f50183056ed6d6b015a51ed26c11bbe9dbfc0cdb21ee8188f09bb2bb93` |
| mymonero/package.json | [source](https://raw.githubusercontent.com/mymonero/mymonero-core-js/ad21d528d2202300349e6f303af9be649c53eb66/package.json) | `789b17bc971a23102d0fa5250b2f25b54fbdec34774096b3c3e40615ed1ec339` |
| mymonero/test/monero_utils.spec.js | [source](https://raw.githubusercontent.com/mymonero/mymonero-core-js/ad21d528d2202300349e6f303af9be649c53eb66/test/monero_utils.spec.js) | `848876fdea3bba9c346e7914bc5a0754e9682677077eee2bfb2853b8fbca430b` |
| mymonero/monero_utils/MyMoneroCoreBridgeEssentialsClass.js | [source](https://raw.githubusercontent.com/mymonero/mymonero-core-js/ad21d528d2202300349e6f303af9be649c53eb66/monero_utils/MyMoneroCoreBridgeEssentialsClass.js) | `3ec81300ac7c4ce52c47144e99460064c820a36b782a3df683e32df7e39f0a9b` |
| feather/CMakeLists.txt | [source](https://raw.githubusercontent.com/feather-wallet/feather/948773cf13c7486ee230eb67b6bac06b2f94c874/CMakeLists.txt) | `d1eb1b67c42fbeb682a945225097cec2c434040d42d1ce583e640f9f6450e8b7` |
| feather/src/utils/Seed.cpp | [source](https://raw.githubusercontent.com/feather-wallet/feather/948773cf13c7486ee230eb67b6bac06b2f94c874/src/utils/Seed.cpp) | `dc79e1b6aace91076f1f9da96411706661830f55fda93926776d83e22d3ab8e5` |
| feather/src/wizard/PageWalletSeed.cpp | [source](https://raw.githubusercontent.com/feather-wallet/feather/948773cf13c7486ee230eb67b6bac06b2f94c874/src/wizard/PageWalletSeed.cpp) | `53c8e05132d18d59a27df07231bbb4fe7a4aa0d559f5d32c28262810e73bce89` |
| feather/src/wizard/PageWalletRestoreSeed.cpp | [source](https://raw.githubusercontent.com/feather-wallet/feather/948773cf13c7486ee230eb67b6bac06b2f94c874/src/wizard/PageWalletRestoreSeed.cpp) | `c03228a2042ef744ab58d1a290602d735c04bdb6a7d2183d9240232acee8f4e9` |
| feather/src/dialog/SeedDialog.cpp | [source](https://raw.githubusercontent.com/feather-wallet/feather/948773cf13c7486ee230eb67b6bac06b2f94c874/src/dialog/SeedDialog.cpp) | `91747e813d973aef54fbed00a7b9fa10afd6bdc2699898f46751424dc288bf5f` |
| cake/pubspec_base.yaml | [source](https://raw.githubusercontent.com/cake-tech/cake_wallet/9679f91a8c9f63d00500c2b7cc18daf00949bdef/pubspec_base.yaml) | `f253e40af9e340b21652cdaab9ecfa6845885e7a8fdcfb7d9e3e905c4a1dfa53` |
| cake/pubspec_description.yaml | [source](https://raw.githubusercontent.com/cake-tech/cake_wallet/9679f91a8c9f63d00500c2b7cc18daf00949bdef/pubspec_description.yaml) | `bc50a0936bf299070e19fcd721af9d5c76f374da719d720cea8ff029f289a21b` |
| cake/cw_monero/pubspec.yaml | [source](https://raw.githubusercontent.com/cake-tech/cake_wallet/9679f91a8c9f63d00500c2b7cc18daf00949bdef/cw_monero/pubspec.yaml) | `2e1399f1c2f943cc34ff45af8a16434d116cdf146ae6d77ff34b9933e5a21852` |
| cake/cw_monero/lib/api/wallet_manager.dart | [source](https://raw.githubusercontent.com/cake-tech/cake_wallet/9679f91a8c9f63d00500c2b7cc18daf00949bdef/cw_monero/lib/api/wallet_manager.dart) | `ca72aa4f9591b54628fd581316d1e9e8c800c54d79dd5814291eb5d0ff8af8c7` |
| cake/lib/entities/seed_type.dart | [source](https://raw.githubusercontent.com/cake-tech/cake_wallet/9679f91a8c9f63d00500c2b7cc18daf00949bdef/lib/entities/seed_type.dart) | `04848d36e285949e61e16b53c9cd9589d0896eaf3921575ea86fba983ad6d5fe` |
| cake/lib/core/mnemonic_length.dart | [source](https://raw.githubusercontent.com/cake-tech/cake_wallet/9679f91a8c9f63d00500c2b7cc18daf00949bdef/lib/core/mnemonic_length.dart) | `6d5749ff8a5b14c66679378051a5daa58a3f38c4a1d59423095c12749376a840` |
| cake/cw_monero/lib/monero_wallet_service.dart | [source](https://raw.githubusercontent.com/cake-tech/cake_wallet/9679f91a8c9f63d00500c2b7cc18daf00949bdef/cw_monero/lib/monero_wallet_service.dart) | `9e0591a1fa987aa48ad876fecdb5ad41b77accd8cdd9fc2a382a90563148d727` |
| cake/cw_monero/lib/monero_wallet.dart | [source](https://raw.githubusercontent.com/cake-tech/cake_wallet/9679f91a8c9f63d00500c2b7cc18daf00949bdef/cw_monero/lib/monero_wallet.dart) | `a5b4e7ef6cfa274eec62670850358f433c26c0f19cdea5cf1f081592e3712e68` |
| cake/lib/view_model/wallet_seed_view_model.dart | [source](https://raw.githubusercontent.com/cake-tech/cake_wallet/9679f91a8c9f63d00500c2b7cc18daf00949bdef/lib/view_model/wallet_seed_view_model.dart) | `e57829ad9284056ec12b705e5e2c289434a6d952966ad232adfaca0c8616986c` |
| cake/lib/view_model/seed_settings_view_model.dart | [source](https://raw.githubusercontent.com/cake-tech/cake_wallet/9679f91a8c9f63d00500c2b7cc18daf00949bdef/lib/view_model/seed_settings_view_model.dart) | `03a6be242cfe37ccac9f2d83de891b9747e01b43e76c9b295a4c0e64252e49cf` |
| cake/cw_monero/lib/bip39_seed.dart | [source](https://raw.githubusercontent.com/cake-tech/cake_wallet/9679f91a8c9f63d00500c2b7cc18daf00949bdef/cw_monero/lib/bip39_seed.dart) | `18d553ebf4da1994bd39be740c417a8c708c5d54aff82d8c364fa4927cb8fd77` |
| gui/wizard/WizardCreateWallet1.qml | [source](https://raw.githubusercontent.com/monero-project/monero-gui/01d6640aff7fd1c1a87932e14e8439383e1229c5/wizard/WizardCreateWallet1.qml) | `908072363400da03915f754efec3f6660974c34be5410e0b1c44c7be288ef9e1` |
| gui/wizard/WizardCreateWallet2.qml | [source](https://raw.githubusercontent.com/monero-project/monero-gui/01d6640aff7fd1c1a87932e14e8439383e1229c5/wizard/WizardCreateWallet2.qml) | `3d09e531de104f12c2f7651a7a32edfeeabec400e0f1ce61a1f105e37ca707da` |
| gui/CMakeLists.txt | [source](https://raw.githubusercontent.com/monero-project/monero-gui/01d6640aff7fd1c1a87932e14e8439383e1229c5/CMakeLists.txt) | `a4a7accb1ea3b598355486e00d240e19a2112a47df688534c4e604290a7e1672` |
| gui/wizard/WizardController.qml | [source](https://raw.githubusercontent.com/monero-project/monero-gui/01d6640aff7fd1c1a87932e14e8439383e1229c5/wizard/WizardController.qml) | `ce321b1d39e21dfa6e50c36d07206f2d7d37acb8d4cef3d1c9225db473a6b7af` |
| myapp/package.json | [source](https://raw.githubusercontent.com/mymonero/mymonero-app-js/5c7455d30e4e20150962f5f74efd83477962a05e/package.json) | `c00f3699d4f244e57dba1522665910687c0fdf2228edfc576f83a717dfc75457` |
| myapp/local_modules/WalletWizard/Views/CreateWallet_InformOfMnemonic_View.web.js | [source](https://raw.githubusercontent.com/mymonero/mymonero-app-js/5c7455d30e4e20150962f5f74efd83477962a05e/local_modules/WalletWizard/Views/CreateWallet_InformOfMnemonic_View.web.js) | `1772443b59b4c4286aa30054f41d7f6110c35e2d471344b00346ca7774c9c674` |
| mycpp/src/monero_wallet_utils.cpp | [source](https://raw.githubusercontent.com/mymonero/mymonero-core-cpp/9637c91cbe5f46e67156c66c739932294808109d/src/monero_wallet_utils.cpp) | `ea6d34729151cffd2b7cdd1a16c31507ff3122242540646ac9797cc0797bb7b4` |
| mycpp/test/test_all.cpp | [source](https://raw.githubusercontent.com/mymonero/mymonero-core-cpp/9637c91cbe5f46e67156c66c739932294808109d/test/test_all.cpp) | `8292f763a1b2bf70052dc959a2672e73a1b4035d5c379bbccb4e03f6a2de6634` |
| signpath.html | [source](https://signpath.org/terms.html) | `6610cf889bbe0dc7533abaa310bc7a5cc9a61ae6c2ce0798a08109c925b46c51` |
| osi-bsd.html | [source](https://opensource.org/license/bsd-3-clause) | `0dfece33194f06d15b862c323f7ed32ba6ab7f512a7fda11880bb2e1401518f8` |
| osi-apache.html | [source](https://opensource.org/license/apache-2-0) | `1377faaaa81ba356528c4053d80e32fd12d84b794ed2667f09bf94aaca7458eb` |

[OSI MIT](https://opensource.org/license/mit) same-day fingerprint is reused from
Task 10 (`004c79db0a335488afc87600d89f447dce7fb4d24d510af15ed4381a24be848c`).
[Exodus official article](https://www.exodus.com/support/en/articles/10862085-support-for-monero-xmr-has-ended)
is identified by published update 2026-01-20; the direct-body retrieval limitation
is explained above. No hash of an HTTP challenge is used as article evidence.
