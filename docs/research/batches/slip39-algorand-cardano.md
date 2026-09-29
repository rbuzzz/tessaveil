# SLIP-39, Algorand and Cardano research batch

Reviewed UTC: **2026-09-29**. Scope: terminal research, not Windows release.
Baseline: `27e82ab9453ddbbe9341beb758714ef2e9960dfe`.
Primary sources only; no wallet installation, real mnemonic, account creation,
provider request, transaction, share combination or remote mutation performed.
Exact source SHAs were resolved via official repositories with an upper commit
date bound of 2026-09-29. A source singleton is not a released-binary attestation.
Official documentation without an app/firmware version is explicitly unresolved,
even when a publication date or response fingerprint exists.

## Decisions and vocabulary

Only the SLIP-39 dictionary is verified in this batch. All nine schemes and
twenty wallet-mode records remain documented or blocked. In particular the
generic Cardano hardware profile, Defly, Eternl and Typhon are blocked. They
remain visible and non-selectable. Research completion does not clear Windows
release readiness or SignPath acceptance.

Exactly 19 existing required items become terminal: one dictionary, six schemes
(including the historical Daedalus27 item omitted from the plan's file list),
and the twelve named wallets. No IDs are removed/added to the required manifest.
Generic wallet-trezor and network requirements belong to later catalogue work
and remain untouched. Three extra length-subset schemes prevent a wallet
creation profile from inheriting lengths proved only for another mode.

## SLIP-39 dictionary and individual shares

The python-shamir-mnemonic list is byte-identical to the normative SLIP list:
1024 unique ASCII words, 7231 UTF-8 bytes, LF with final LF; SHA-256
`bcc4555340332d169718aed8bf31dd9d5248cb7da6e5d355140ef4f1e601eec3`.
No extraction, sorting, case conversion or Unicode transformation was applied.
Indices use source order. The upstream parser lowercases and splits whitespace,
without NFC/NFKD normalization; ASCII means all normalization forms leave the
stored tokens unchanged. No normalization collisions exist.

The standard's format section defines four metadata words: a 15-bit identifier,
one extendable flag, four-bit iteration exponent, then five four-bit values
(group index, group threshold minus one, group count minus one, member index,
member threshold minus one). Group count and thresholds are 1..16; the member
count is not encoded in a share. Value bits are left-padded to ten-bit boundaries.
The final three words are RS1024 checksum. The same 1024-word dictionary applies
to each position, but fields and padding constrain valid complete shares.
128/256-bit secrets give 20/33 words. These are scoped supported lengths, not a
claim that the general standard allows no other length.

Tessaveil never combines or reconstructs shares, stores the recovered master
secret, validates a user's complete share, or derives keys. Optional passphrases
remain external. Public tests inspect individual-share metadata and checksum
only. Their upstream expected recovered secrets are deliberately omitted.

The Trezor official device table names each model explicitly. Separate records
cover Model T, Safe 3, Safe 5 and Safe 7 and separate simultaneous single-share and
multi-share creation modes. Each references the **20-word subset**. Model T's
default remains BIP39; the Safe 3 documentation distinguishes setup before/from
June2024; Safe 5/7 document20-word default. Those dates are not firmware version
numbers. Exact Suite/firmware bounds and Suite host OS are unpublished here:
all eight profiles are documented and non-selectable. No Model One support,
33-word Suite creation, CLI advanced-group support, all-firmware coverage or
Cardano derivation is inferred. The FAQ says two-level advanced groups require
trezorctl; this batch does not create a CLI wallet profile.

## Algorand format and product separation

The Algorand SDK's word_list_raw() literal was compared entry-for-entry with
verified bip39-en: 2048 words in the same order. The literal already includes a
final LF; its unchanged UTF-8 bytes reproduce existing BIP39 file SHA-256
`2f5eed53a4727b4bf8880d8f3f199efc90e58503646d9ff8eff3a2ed3b24dbda`.
Only the existing dictionary is referenced; no Algorand/Cardano copy is added.

Legacy Algo 25 encodes a 32-byte account seed in little-endian11-bit units.
Words1..23 use all 11 bits; word 24 holds three remaining bits and eight zero
padding bits, so its eligible zero-based indices are **0..7**. Word25 is the
first little-endian11 bits of SHA-512/256(seed). It is neither an extra passphrase
nor BIP39's entropy checksum nor Monero's repeated checksum word. The restricted
eight-word position must remain explicit in any later10/36-column design:
repetition/masking behavior for that row requires review; substituting a full
2048-word eligible set would be wrong. This batch implements no table creation.

The SDK export method takes the first32 bytes of a private-key object; that
does not establish a wallet product's fresh-generation path. Pera's current
backup article (updated2026-08-31) discusses24 and 25 words and later viewing.
Its migration article (2026-05-28) explicitly names Universal 24 and Legacy
Algo 25. The required Pera record therefore describes **existing legacy25 export
on iOS**, with generation=false and import_only=false. No fresh legacy25
creation at unspecified current versions is asserted. Universal 24 iOS generation
has its own unmapped documented profile, using the2025-06-04 FAQ; that dated
article calls Android forthcoming, so its claim is not generalized to Android.
Pera HD derivation, passkeys, Quantum, rekeyed, Ledger, web and secure-backup-file
formats are not mapped to Algo 25.

Defly's official manual proves native-account creation and a later backup
reminder that reveals a mnemonic, but its retrieved text gives no count,
dictionary, algorithm, exact app version or platform-specific bound. Android is
the explicit research target; no parity claim is made. The profile is blocked
and unmapped. Third-party25-word guides were not used to fill that gap.

## Cardano schemes and concrete modes

CIP 3 separates deprecated random/Byron, Icarus, Icarus-Trezor and
Ledger/BitBox02 roots. Shared BIP39 vocabulary/entropy encoding never means
shared root derivation. Icarus uses 4096-round PBKDF2-HMAC-SHA512 with entropy salt
and separate mnemonic password; the examined Yoroi and Nami source passes an
empty mnemonic password. Their local spending/encryption password is distinct.
CIP 3 describes the Trezor 24 checksum-byte deviation and the different Ledger
BIP39-seed/HMAC construction. No generic selectable hardware scheme is possible
without exact vendor/model/firmware/mode evidence: its dictionaries and lengths
are deliberately empty.

| Product / platform | Exact research version | Concrete mode / result |
| --- | --- | --- |
| Yoroi extension / web | source 91febfc95a288d3436b891356c87645611ea603a | Explicit160-bit/15-word generation, backup flow, Icarus entropy API; documented |
| Daedalus / Windows | 11.4.0-source 6c57eb94753211f66d3a63f49d031bf746044755 | Regular24 creation; distinct legacy12, Yoroi15 and historical paper 27 import profiles; documented |
| Nami extension / web | 3.9.6-sourcee52e0bdb02eb1ec224db26f48b0192685a30f99e | Explicit256-bit/24-word generation/display and Icarus entropy API; documented, no current-maintenance claim |
| Lace extension / web | app version unresolved; article2026-07-14 |24-word generation/display proved; exact derivation/library binding absent, scheme unmapped; documented |
| Eternl / web | app version unresolved; reviewed2026-09-29 | FAQ identifies24-word recovery; creation/export path and algorithm not proved; blocked/unmapped |
| Typhon / web | app version unresolved; reviewed2026-09-29 | Creation distinct from import/hardware; exact generation length/version/algorithm absent; blocked/unmapped |

The15/24 Icarus umbrella lists only the two researched creation lengths, not all
theoretical inputs. Length-specific schemes avoid showing15-word creation for
Nami/Daedalus or 24-word creation for Yoroi. A12-word Cardano phrase does not
universally mean Byron: only the exact historical Daedalus12 mode is mapped.
Typhon import selectors and testnet pages were not evidence of production
generation. Unproven lengths remain unproven, not invented.

Historical Daedalus paper 27 is **18 scrambled certificate words +9 password
words** that recover an old Byron 12 wallet. The nine-word suffix feeds a
2048-round, 32-byte PBKDF2-HMAC-SHA512 password computation with mnemonic salt;
it is already part of the27, not an additional outside passphrase. It is not a
27-word BIP39 mnemonic, an Icarus seed, or Lace's modern PGP paper backup.
The current source retains helpers while the upstream fixture describes
creation retirement; the record claims historical import only, not current
reachable generation. Full rust-cardano-crypto unscrambling, backend binding
and wallet-level recovery remain unverified.

## Public/synthetic vectors and offline reproduction

Run `python -m unittest tests.catalog.test_slip39_algorand_cardano -v`.
Observed with CPython 3.14.2, standard-library hashlib/json/unittest; no network
or upstream dependency is used by the tests. Test fixture data is exclusively
published tests or explicitly synthetic non-funded inputs.

- SLIP public cases 1, 4, 17, 20, 42, 44: only the first share of each case projected
  to indices, sentence fingerprint, reviewed expected identifier/extendable/
  exponent and group/member fields. The tests reproduce RS1024 and padding for
  both20/33 and original/extendable domains. They never combine shares.
- Algorand public TestMnemonic.test_zero_mnemonic is the fixed zero-seed answer.
  Ascending00..1f and all-FF are explicitly synthetic. Their expected words were
  produced by the four reviewed pure functions from the pinned official SDK
  (`_from_key/_checksum/_to_11_bit/_apply_words`), extracted via Python AST
  after verifying the downloaded byte hash, with standard SHA-512/256 supplied.
  The offline test independently uses integer shifts over the seed and literal
  expected indices, so its expected output does not come from itself.
- Daedalus's explicitly synthetic2026-08-27 certificate is projected to27
  indices, 18+9 partition, sentence hash and published password hash. The test
  reproduces the suffix password only. It does not claim certificate decryption,
  Cardano key derivation or a successful wallet restoration.
- CIP 3 contains published root-key examples, but none is copied or counted as
  reproduced here. The schemes stay documented/blocked.

The tests additionally enforce required IDs, exact length-specific references,
no duplicate BIP39 files, terminal versus release separation, and unique
product+platform+singleton-version+mode identities. The catalogue validator
checks all backlinks/schema/hash rules; it cannot authenticate claims in prose.

## Licensing and distribution

Reviewed by Codex 2026-09-29 for this data/test projection payload only.
SLIP's source list and vector projection are covered by the pinned repository's
MIT license, Copyright 2019 SatoshiLabs. The exact dictionary is unchanged;
vector projections are modified. Algorand's source/test projection is MIT,
Copyright(c)2020 Algorand; no SDK/list copy is bundled. Both complete notices
are retained in THIRD_PARTY_NOTICES.

The Daedalus synthetic fixture has no local license override. The same source
revision's root Apache-2.0 LICENSE and LICENSE NOTICE (Copyright 2019 IOHK)
were inspected. The projection is marked modified, attribution retained, and
the complete Apache text is already in root LICENSE and THIRD_PARTY_NOTICES.
Only trailing whitespace on blank notice lines is removed. No wallet
implementation, rust-cardano-crypto, SDK binary or dependency is bundled.
The source ledger below pins both terms and notice.

Repository redistribution is allowed for these exact MIT/Apache projections
with the recorded obligations fulfilled. SignPath component-license compatibility
is a separate local assessment based on actual OSS-license conditions and OSI
approval; it does not establish Foundation acceptance, project reputation,
certificate issuance, clean-machine evidence or Windows release approval.
CIP 3 CC-BY-4.0 prose/vector bytes are **not bundled**; factual summaries and
citations do not claim its license is an OSI software license.

## Retrieval limits and source ledger

Trezor device table/FAQ, Defly, Eternl, Typhon, IOHK support and OSI MIT direct
body fetches returned403. Official text was reviewed through web retrieval;
no raw-response hash or immutable capture is claimed for those pages. Pera and
Lace body fingerprints below identify retrieved bytes before markup removal.
The Pera source explored at c7a41e2f62e230d4850725fc86e8af334012ae55 has backup
and export call paths, but their exact dependency/release binding is unproven;
it is not substituted for the newer product documentation. No forum/community
claim is used as primary evidence.

Immutable raw GitHub URLs below include full revision SHAs. Bytes/hash refer to
the original HTTP-decoded response before any source-array projection. Only the
SLIP list and explicitly licensed vector projections enter the payload.

| Source | Bytes | SHA-256 |
| --- | ---: | --- |
| [slip:LICENSE](https://raw.githubusercontent.com/trezor/python-shamir-mnemonic/17fcce14736afe498871d3018e4fa9330443471a/LICENSE) | 1051 | `332f92f7f90a1c957b473b902a5daf39ad5eb179d8828e0304b4c40faa0123c0` |
| [slip:shamir_mnemonic/wordlist.txt](https://raw.githubusercontent.com/trezor/python-shamir-mnemonic/17fcce14736afe498871d3018e4fa9330443471a/shamir_mnemonic/wordlist.txt) | 7231 | `bcc4555340332d169718aed8bf31dd9d5248cb7da6e5d355140ef4f1e601eec3` |
| [slip:shamir_mnemonic/share.py](https://raw.githubusercontent.com/trezor/python-shamir-mnemonic/17fcce14736afe498871d3018e4fa9330443471a/shamir_mnemonic/share.py) | 7000 | `3ee6f46415ba34dd8c1bc5f92601b17151854a35425e098d1de857ca714205c5` |
| [slip:shamir_mnemonic/constants.py](https://raw.githubusercontent.com/trezor/python-shamir-mnemonic/17fcce14736afe498871d3018e4fa9330443471a/shamir_mnemonic/constants.py) | 2022 | `434696830041652cc08d6f837b763d7333aec149c1b2fd976aa2bd20350a147b` |
| [algo:algosdk/mnemonic.py](https://raw.githubusercontent.com/algorand/py-algorand-sdk/189855d43cba5d20e66248693d74332052ccb08e/algosdk/mnemonic.py) | 5749 | `6d9387e3ee7213c14a1dec9f53a22f2880ee80b00df8457430f5ecae21f2c74e` |
| [algo:LICENSE](https://raw.githubusercontent.com/algorand/py-algorand-sdk/189855d43cba5d20e66248693d74332052ccb08e/LICENSE) | 1065 | `32b60f70e2a09ff695719af28a8ff60a8188d79de889d03913965f0d4b3d6055` |
| [cip:CIP-0003/README.md](https://raw.githubusercontent.com/cardano-foundation/CIPs/4ca4dcefccc7143672cf07a0b760d9e5abfc7797/CIP-0003/README.md) | 4588 | `84a4abe37702847073aac805452c570ac8bc80a8723d89875826f3d5f1f034e4` |
| [cip:CIP-0003/Icarus.md](https://raw.githubusercontent.com/cardano-foundation/CIPs/4ca4dcefccc7143672cf07a0b760d9e5abfc7797/CIP-0003/Icarus.md) | 2794 | `f83da5fbdc6865a0de83edb7219208908e109b2a50671c8a9682d7c3d1179a85` |
| [cip:CIP-0003/Byron.md](https://raw.githubusercontent.com/cardano-foundation/CIPs/4ca4dcefccc7143672cf07a0b760d9e5abfc7797/CIP-0003/Byron.md) | 1571 | `0d46c673348dccdaf32f1cc3732a744745494478417cb6e2388247ecd12a25d6` |
| [cip:CIP-0003/Ledger_BitBox02.md](https://raw.githubusercontent.com/cardano-foundation/CIPs/4ca4dcefccc7143672cf07a0b760d9e5abfc7797/CIP-0003/Ledger_BitBox02.md) | 3095 | `164975c4556ae04fa00377f431e37be35b6fdd2b84b0fd7843a859093c3fe62f` |
| [slips:slip-0039.md](https://raw.githubusercontent.com/satoshilabs/slips/570ed55b7fde158f1116be34fc2faa35dada5912/slip-0039.md) | 43071 | `7b4269f66f10f03ac685ea7c76f742bfbf56211af1af29339eadef9acba1f856` |
| [slip:vectors.json](https://raw.githubusercontent.com/trezor/python-shamir-mnemonic/17fcce14736afe498871d3018e4fa9330443471a/vectors.json) | 22411 | `13ebecebdd869dd2bc2cdf69e7ce3a158cf106cac76c39d17682b1c6cdabbdc4` |
| [algo:algosdk/wordlist.py](https://raw.githubusercontent.com/algorand/py-algorand-sdk/189855d43cba5d20e66248693d74332052ccb08e/algosdk/wordlist.py) | 13267 | `bacc048829f092449fea722912b268ec9d6f5494776ca4ece50f463bb80e77d7` |
| [daedalus:source/renderer/app/api/utils/mnemonics.ts](https://raw.githubusercontent.com/input-output-hk/daedalus/6c57eb94753211f66d3a63f49d031bf746044755/source/renderer/app/api/utils/mnemonics.ts) | 921 | `df34bb44cb02d001319d19cbf70c4f370fbf5c43a4202e463b4ecc4d0747b1c7` |
| [daedalus:source/renderer/app/config/walletsConfig.ts](https://raw.githubusercontent.com/input-output-hk/daedalus/6c57eb94753211f66d3a63f49d031bf746044755/source/renderer/app/config/walletsConfig.ts) | 1867 | `2535b05897dc65e3dbb3654462c426ca07ad12eb62f957dbbf88f77321b93e85` |
| [yoroi:packages/yoroi-extension/app/stores/ada/MnemonicWalletCreationStore.js](https://raw.githubusercontent.com/Emurgo/yoroi-frontend/91febfc95a288d3436b891356c87645611ea603a/packages/yoroi-extension/app/stores/ada/MnemonicWalletCreationStore.js) | 2537 | `330e545c3035cc251c40ae6dd7895495a48f530cbe58d664159c6e0e87579c16` |
| [nami:src/api/extension/index.js](https://raw.githubusercontent.com/input-output-hk/nami/e52e0bdb02eb1ec224db26f48b0192685a30f99e/src/api/extension/index.js) | 61072 | `8c50628956578649ab228d7cfb6a29dcf8ac104e53f2c0a4fa67731ac913ce57` |
| [algo:tests/unit_tests/test_other.py](https://raw.githubusercontent.com/algorand/py-algorand-sdk/189855d43cba5d20e66248693d74332052ccb08e/tests/unit_tests/test_other.py) | 31265 | `9d1ae77d906174a845979221cf483b01e8756aeadf5e3d66d5f45ca6aca1d79f` |
| [daedalus:source/renderer/app/config/cryptoConfig.ts](https://raw.githubusercontent.com/input-output-hk/daedalus/6c57eb94753211f66d3a63f49d031bf746044755/source/renderer/app/config/cryptoConfig.ts) | 550 | `58d94791c7826fca095e4f56e213ea04cd69a4cd915eab0b7cb3103b8f35a265` |
| [daedalus:source/renderer/app/utils/crypto.ts](https://raw.githubusercontent.com/input-output-hk/daedalus/6c57eb94753211f66d3a63f49d031bf746044755/source/renderer/app/utils/crypto.ts) | 4502 | `02c137b08bf4394f95afeaf6e81a538ff39b15719fe326b8dbf1728c1a04cfd4` |
| [daedalus:package.json](https://raw.githubusercontent.com/input-output-hk/daedalus/6c57eb94753211f66d3a63f49d031bf746044755/package.json) | 13587 | `4af61443fb0bf72a23c1ee4aa5faaf70adc5cced3a3d6e358e91f4cdf2bf73c8` |
| [nami:src/ui/app/tabs/createWallet.jsx](https://raw.githubusercontent.com/input-output-hk/nami/e52e0bdb02eb1ec224db26f48b0192685a30f99e/src/ui/app/tabs/createWallet.jsx) | 19716 | `d79776a12f8f7c4c6a4dc93e159c58110509494e169f84f2c556f139ccaf109c` |
| [nami:package.json](https://raw.githubusercontent.com/input-output-hk/nami/e52e0bdb02eb1ec224db26f48b0192685a30f99e/package.json) | 4706 | `81438dedcb3b9b8223148da27f89c7e5e5cb215ff0cffb6ed01527c0231d6ef4` |
| [https://support.perawallet.app/en/article/backing-up-your-recovery-passphrase-uacy9k/](https://support.perawallet.app/en/article/backing-up-your-recovery-passphrase-uacy9k/) | 20952 | `4fad7c798ef8891ca31f4ee64051c570fd8d4952665f70738635c26eb425c9d6` |
| [https://www.lace.io/blog/moving-your-funds-to-lace-carefully](https://www.lace.io/blog/moving-your-funds-to-lace-carefully) | 170535 | `ce02d32706cf597d8f3861e3040d487d7e8862020069ccdf6e40aa48b7a83f19` |
| [yoroi:packages/yoroi-extension/app/api/ada/index.js](https://raw.githubusercontent.com/Emurgo/yoroi-frontend/91febfc95a288d3436b891356c87645611ea603a/packages/yoroi-extension/app/api/ada/index.js) | 93338 | `8c9dbfbc259cbca65b002c11c690c39fd647d8acdefa46381c0aafee0856657c` |
| [daedalus:source/common/config/crypto/valid-words.en.ts](https://raw.githubusercontent.com/input-output-hk/daedalus/6c57eb94753211f66d3a63f49d031bf746044755/source/common/config/crypto/valid-words.en.ts) | 23376 | `6a445ce64e8068dc7f523546e4f7788c0315365ff1561b389eea524629e18386` |
| [daedalus:source/renderer/app/utils/__fixtures__/paper-wallet-certificate.json](https://raw.githubusercontent.com/input-output-hk/daedalus/6c57eb94753211f66d3a63f49d031bf746044755/source/renderer/app/utils/__fixtures__/paper-wallet-certificate.json) | 1139 | `2c7449afaf97bf85b62537c655323def5bb6f328755dae303ac3f52a6465e13b` |
| [yoroi:packages/yoroi-extension/app/api/ada/lib/cardanoCrypto/cryptoWallet.js](https://raw.githubusercontent.com/Emurgo/yoroi-frontend/91febfc95a288d3436b891356c87645611ea603a/packages/yoroi-extension/app/api/ada/lib/cardanoCrypto/cryptoWallet.js) | 2775 | `cb4e95b9bc4e8a30ecd3f6520424e556560155503ad03456988bf5a3fed4fa21` |
| [https://support.perawallet.app/en/article/universal-wallet-faq-1ssu0sq/](https://support.perawallet.app/en/article/universal-wallet-faq-1ssu0sq/) | 18634 | `d54c39508a76f426bd3958cfbae5600d8f737aa05d4356540be617986a4c0b81` |
| [https://support.perawallet.app/en/article/device-migration-moving-pera-to-a-new-phone-1thj6od/](https://support.perawallet.app/en/article/device-migration-moving-pera-to-a-new-phone-1thj6od/) | 25498 | `30fa382990ea359398ccde9c9a4ccdd2e031b6b83721f9aede4cb46cb57c506b` |
| [daedalus:LICENSE](https://raw.githubusercontent.com/input-output-hk/daedalus/6c57eb94753211f66d3a63f49d031bf746044755/LICENSE) | 11357 | `58d1e17ffe5109a7ae296caafcadfdbe6a7d176f0bc4ab01e12a689b0499d8bd` |
| [slip:shamir_mnemonic/wordlist.py](https://raw.githubusercontent.com/trezor/python-shamir-mnemonic/17fcce14736afe498871d3018e4fa9330443471a/shamir_mnemonic/wordlist.py) | 1113 | `f246d5c397155a377cb7344f6a3986e197210469cd575c83fbbfae2bcfe09975` |
| [https://signpath.org/terms.html](https://signpath.org/terms.html) | 19630 | `6610cf889bbe0dc7533abaa310bc7a5cc9a61ae6c2ce0798a08109c925b46c51` |
| [slips:slip-0039/wordlist.txt](https://raw.githubusercontent.com/satoshilabs/slips/570ed55b7fde158f1116be34fc2faa35dada5912/slip-0039/wordlist.txt) | 7231 | `bcc4555340332d169718aed8bf31dd9d5248cb7da6e5d355140ef4f1e601eec3` |
| [slip:shamir_mnemonic/rs1024.py](https://raw.githubusercontent.com/trezor/python-shamir-mnemonic/17fcce14736afe498871d3018e4fa9330443471a/shamir_mnemonic/rs1024.py) | 965 | `7527b6ab5b0de8ef90697699f24c4bd615dbc77ec988e90590bfcf80146e8391` |
| [daedalus:source/renderer/app/api/api.ts](https://raw.githubusercontent.com/input-output-hk/daedalus/6c57eb94753211f66d3a63f49d031bf746044755/source/renderer/app/api/api.ts) | 110054 | `55fdbd3fd1851cf46fee7444bb90323ff440e46f99dbe30fb67d2cfc36991d7c` |
| [daedalus:LICENSE%20NOTICE](https://raw.githubusercontent.com/input-output-hk/daedalus/6c57eb94753211f66d3a63f49d031bf746044755/LICENSE%20NOTICE) | 548 | `d7fe15fe73be69f2543950c5b87a9c3964bd31ccbaa51a6127e7d88aea877190` |
