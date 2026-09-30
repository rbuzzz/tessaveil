# Named wallets and network guidance

Reviewed 2026-09-29 UTC. Research only; **Windows release remains NO-GO**.
All 36 new named products have explicit modes, all 22 named networks have
search guidance, and the generic Trezor obligation now points to the eight
already researched model-specific Task12 profiles. This completes terminal
research coverage, not wallet recovery support. New records are documented
and non-selectable. Earlier verified TON profiles are unchanged.

The 163/163 terminal result is current-manifest mechanics only and cannot close Task16.
The generic Cake requirement predates Task15 and only references the existing
`cake-wallet-monero` profile; other earlier Cake profiles likewise are not a
complete current-format inventory. Task16 still requires official research of
every current Cake network/mnemonic mode, new evidence or explicit blockers,
and its independent completeness audit. Task15 does not change that scope.

## Identity and evidence boundaries

Identity is normalized product ID + platform + overlapping version interval
+ concrete mode ID. NFKC, case folding, hyphen/space normalization and collapsed
whitespace apply to identity/alias comparisons. Different simultaneous modes
are allowed. Cross-platform overlaps every concrete platform.
Mobile-app is an app-scoped observation without an exact mobile OS binding;
it overlaps iOS, Android and cross-platform for conflict detection, not web or
desktop. It does not claim tested support for both mobile systems. Closed numeric
intervals compare component-wise (1.0 equals 1.0.0); touching endpoints overlap.
Open or incomparable intervals fail closed. Opaque singleton commits/snapshot
IDs are evidence observations, not chronological release ranges; distinct pins
therefore cannot establish disjoint versions of the same mode. Numeric
strings longer than 128 characters are treated as incomparable, avoiding
unbounded integer conversion. Duplicate normalized aliases fail; no
unstructured prose/evidence string can silently override a conflict. Resolve
ambiguity by explicit product/platform/version/mode records and sourced aliases.

The snapshot markers are deliberately not app-version claims. Source pins
prove the inspected code, not the installed binary. Platform labels scope the
research profile; where a generic app guide is used, exact platform-specific
behavior and version binding remain unresolved in the limitations. A false
generation flag means that this mode does not claim generation, not that the
product can never generate a phrase. Import is never generation evidence.
No runtime phrase input, key derivation, provider submission or wallet creation
was performed. Only public documentation/source was retrieved.

No dictionaries, vectors or third-party implementations were copied. Existing
scheme IDs are reused only where explicitly established or as labeled network
search candidates. A null product scheme is intentional: a word count alone
does not establish BIP39, normalization, passphrase treatment or account paths.
A word dictionary is never duplicated for an EVM network. Native Substrate,
TON, Cardano, Algorand, Monero, Zano, Sia and Chia distinctions are preserved.

## Material product findings

- MetaMask social login still generates an SRP; shards, login credentials and
  password are not a seedless mode. Its passkey unlock is separate again.
- Coinbase's current table gives mnemonic **import**, smart passkey and CDP
  social-login wallets separately. The optional smart recovery phrase adds an
  on-chain signer and has per-chain setup dependencies; it is not EOA recovery.
  The mnemonic and CDP routes are app-scoped; the smart-wallet web route must
  not be transferred to them. Exact mobile OS/version remains unresolved.
- Exodus recommends passkey backup in its Mobile section. Its Web3 exception
  concerns screenshot/screen-recording protection, not passkey availability;
  neither Web3 passkey support nor its absence is established by that sentence.
- OKX stopped new MPC creation on 2025-05-23 and extension service on 2025-04-07.
  Existing app MPC recovery, phrase backup, private-key import and cloud backup
  are distinct. The MPC record is historical rather than a promise of creation.
  A separate social-login mode creates a wallet on Google/Apple/email sign-in
  without manual seed backup; this is not proof that no underlying mnemonic exists.
- Bitget's guide separates 12/24-word creation from email/password MPC and
  cloud backup of that mode. SWIFT is Trust Wallet's passkey smart wallet.
- Tangem's FAQ simultaneously says 12/24-word creation exists and elsewhere
  says 12 words can only be imported. Generation existence is documented,
  exact length/version remains unresolved. Seedless cards and seed import are
  separate. Do not infer a generation length set from the import list.
- Keystone Essential/Pro M-4.5 guide is not Keystone 3. Single-backup and SLIP39
  creation/import remain distinct; no share length is inferred. BitBox02 now
  documents optional 12-word creation, not just default24. MicroSD backups are
  their own material; no removable storage was accessed.
- ELLIPAL evidence is specifically X Card Starter; this record does not claim
  Titan or Joy support. OneKey is specifically Pro hardware, not App software.
- Guarda's normal file+password backup is not automatically BIP39. The mnemonic
  import tutorial establishes import only. Coinomi recovery/password evidence
  also does not establish a new generation flow.
- Rabby, Cosmostation, Temple and Passport are pinned source observations.
  Cosmostation calls bip39 with12/18/24 choices. Temple generates128-bit BIP39
  and has distinct Tezos/EVM derivation plus legacy import branches. Passport's
  encrypted backup explicitly excludes an active mnemonic passphrase.
- Glow's official pages establish Solana and user-held recovery phrases but
  not generation lengths, cloud backup, codec or detailed import routes. Its
  unresolved backup mode remains documented/non-selectable.
- Keplr Google/Web3Auth provides a private key rather than recovery phrase.
  Kukai DirectAuth uses Torus/OAuth shares, not SLIP39 word shares. Solflare
  Quick Login automatically backs up a recovery phrase, so login does not mean
  seedless. Phantom's current creation choices do not alone settle social-mode
  phrase export semantics. These gaps remain explicit.
- Leap's direct guide URL returned404; an indexed official page was reviewed.
  It documents existing phrase import, not current availability or generation.
  The record is historical and non-selectable; no active-service promise.
- Coldcard's current documentation warns about affected firmware and requires
  firmware verification before setup. This research does not approve any
  hardware entropy or historical seed. SeedSigner dice, photo, SeedQR input
  and BIP85 child generation are separate modes.

## Network aliases and candidates

Network guidance profiles use the existing wallet-profile schema with explicit
mode_id network-search-guidance and product_id network-guide-*; they are
navigation records, not actual wallet products. Both generation/import flags
are false. Scheme links and aliases are search guidance only. Existing required
network profile references are preserved alongside the new guide. A network
identity page proves its name/scope, not any candidate recovery algorithm.
Algorand's current documentation also describes xHD24; existing Algo25 does not
cover it. ZIP339's current landing page is Reserved, so it is not substituted
for the earlier pinned implementation evidence.

| Network | Search aliases | Existing candidate scheme IDs | Boundary |
| --- | --- | --- | --- |
| bitcoin | BTC | `bip39`, `electrum-v1`, `electrum-v2`, `slip39-share` | Bitcoin wallets have distinct backup families; multisig also needs policy, cosigner and descriptor metadata. |
| ethereum | ETH, EVM | `bip39` | EOA keys, mnemonic HD wallets and smart-account signers are different recovery modes; EVM address support alone proves no mnemonic scheme. |
| base | Base Mainnet, Base chain | `bip39` | Base is an EVM chain; Coinbase Wallet is a product and Base Account is a smart-account mode, not a Base dictionary. |
| bnb-chain | BNB, BSC, BNB Smart Chain | `bip39` | BNB Smart Chain is the EVM search scope. BNB Beacon Chain and opBNB are not interchangeable network or recovery promises. |
| polygon | POL, MATIC, Polygon PoS | `bip39` | Polygon PoS search guidance; zkEVM and other Polygon products require their own chain/account identity. |
| avalanche | AVAX, Avalanche C-Chain | `bip39` | C-Chain EVM, X-Chain and P-Chain are separate chains with different address and account context; no universal recovery mapping. |
| arbitrum | ARB, Arbitrum One | `bip39` | Arbitrum One network guidance; Nova and testnets are separate chain identities. Network configuration is not mnemonic evidence. |
| solana | SOL | `bip39` | Solana accounts and program-derived addresses do not establish a wallet mnemonic scheme. Original wallet derivation and account selection remain necessary. |
| tron | TRX, TRON | `bip39` | Official accounts documentation separates private-key EOAs and contract accounts; neither creates a dedicated word list. |
| cosmos | ATOM, Cosmos Hub, Interchain | `bip39` | Cosmos names an ecosystem, not a universal coin type, curve, prefix or HD path. Cosmos EVM and chain-specific accounts require separate mapping. |
| tezos | XTZ | `bip39` | Phrase wallets, legacy fundraiser credentials, keystores and Kukai DirectAuth are distinct. Curve, derivation and external credentials remain required. |
| polkadot | DOT | `substrate-bip39` | Substrate key derivation is not ordinary BIP39 sentence-to-seed derivation. Curve, junctions and network address encoding must match. |
| kusama | KSM | `substrate-bip39` | Kusama is a separate network from Polkadot; related code and shared dictionary do not prove cross-network wallet recovery. |
| cardano | ADA | `cardano-byron`, `cardano-icarus`, `cardano-hardware`, `cardano-daedalus-27` | Byron, Icarus, hardware and paper-certificate modes require distinct derivation and external-secret handling. |
| algorand | ALGO | `algorand-25` | Official current overview distinguishes Algo25 from newer xHD 24-word accounts and smart accounts. Existing Algo25 profile is not xHD support; xHD remains unmapped. |
| monero | XMR | `monero-legacy`, `mymonero-13`, `polyseed-16` | Legacy25, MyMonero13 and Polyseed16 have different codecs and dependencies despite sharing a network. |
| zcash | ZEC | `zcash-bip39`, `zcash-non-mnemonic` | The current ZIP339 landing page is Reserved; it does not establish implementation semantics. Use pinned Task14 source profiles for Zallet/zcashd; imported standalone keys remain distinct. |
| chia | XCH | `chia-bip39` | Chia derives BLS keys, not Bitcoin BIP32. BIP39 words alone do not prove another wallet's recovery compatibility. |
| decred | DCR | `decred-pgp33`, `decred-bip39`, `cake-decred-15` | PGP33, current BIP39 and Cake modes are separate profiles; project home establishes network identity only, not codec equivalence. |
| zano | ZANO | `zano-modern`, `zano-legacy-24`, `zano-legacy-25`, `cake-zano-bip39` | Native timestamp/password modes and Cake BIP39-derived mode differ; dictionary license and historical-version blockers remain. |
| sia | SC, Siacoin | `sia-bip39`, `sia-legacy-28`, `sia-legacy-29` | Current walletd English12 and legacy28/29 are different codecs; current UI and legacy backend compatibility are not interchangeable. |
| ton | TON, The Open Network | `ton-native`, `ton-multichain-bip39` | Native TON and multichain BIP39 are separate profiles. Shared English2048 words do not establish equivalent seeds. |

## Product/mode matrix

Each row links to its complete limitations and source backlinks. Platform is
a research scope, not a tested recovery compatibility statement.

| Record | Product | Platform | Mode | Generation / import only | Scheme |
| --- | --- | --- | --- | --- | --- |
| [trust-wallet](../../../catalog/wallets/trust-wallet.json) | Trust Wallet | android | classic-mnemonic-generated | true / false | bip39 |
| [trust-wallet-swift](../../../catalog/wallets/trust-wallet-swift.json) | Trust Wallet | android | swift-passkey | false / false | unresolved / not mnemonic |
| [metamask](../../../catalog/wallets/metamask.json) | MetaMask | web | mnemonic-generated | true / false | unresolved / not mnemonic |
| [metamask-social-login](../../../catalog/wallets/metamask-social-login.json) | MetaMask | web | social-login-srp | true / false | unresolved / not mnemonic |
| [metamask-private-key](../../../catalog/wallets/metamask-private-key.json) | MetaMask | web | private-key-imported | false / true | unresolved / not mnemonic |
| [metamask-passkey-unlock](../../../catalog/wallets/metamask-passkey-unlock.json) | MetaMask | web | passkey-local-unlock | false / false | unresolved / not mnemonic |
| [coinbase-wallet](../../../catalog/wallets/coinbase-wallet.json) | Coinbase Wallet | mobile-app | mnemonic-imported | false / true | unresolved / not mnemonic |
| [coinbase-wallet-passkey](../../../catalog/wallets/coinbase-wallet-passkey.json) | Coinbase Wallet | web | smart-wallet-passkey | false / false | unresolved / not mnemonic |
| [coinbase-wallet-social-login](../../../catalog/wallets/coinbase-wallet-social-login.json) | Coinbase Wallet | mobile-app | cdp-social-login | false / false | unresolved / not mnemonic |
| [coinbase-wallet-smart-recovery](../../../catalog/wallets/coinbase-wallet-smart-recovery.json) | Coinbase Wallet | web | smart-recovery-signer | true / false | unresolved / not mnemonic |
| [coinbase-wallet-cloud-backup](../../../catalog/wallets/coinbase-wallet-cloud-backup.json) | Coinbase Wallet | ios | legacy-cloud-backup | false / false | unresolved / not mnemonic |
| [exodus](../../../catalog/wallets/exodus.json) | Exodus | windows | global-mnemonic-generated | true / false | bip39 |
| [exodus-passkey](../../../catalog/wallets/exodus-passkey.json) | Exodus | ios | passkey-backup | false / false | unresolved / not mnemonic |
| [atomic-wallet](../../../catalog/wallets/atomic-wallet.json) | Atomic Wallet | windows | mnemonic-generated | true / false | unresolved / not mnemonic |
| [onekey](../../../catalog/wallets/onekey.json) | OneKey Pro | hardware | pro-mnemonic-generated | true / false | unresolved / not mnemonic |
| [ledger](../../../catalog/wallets/ledger.json) | Ledger | hardware | device-bip39-generated | true / false | bip39 |
| [okx-wallet](../../../catalog/wallets/okx-wallet.json) | OKX Wallet | android | mnemonic-generated | true / false | unresolved / not mnemonic |
| [okx-wallet-social-login](../../../catalog/wallets/okx-wallet-social-login.json) | OKX Wallet | mobile-app | social-login | false / false | unresolved / not mnemonic |
| [okx-wallet-mnemonic-import](../../../catalog/wallets/okx-wallet-mnemonic-import.json) | OKX Wallet | android | mnemonic-imported | false / true | unresolved / not mnemonic |
| [okx-wallet-private-key](../../../catalog/wallets/okx-wallet-private-key.json) | OKX Wallet | android | private-key-imported | false / true | unresolved / not mnemonic |
| [okx-wallet-cloud-backup](../../../catalog/wallets/okx-wallet-cloud-backup.json) | OKX Wallet | android | mnemonic-cloud-backup | false / false | unresolved / not mnemonic |
| [okx-wallet-mpc](../../../catalog/wallets/okx-wallet-mpc.json) | OKX Wallet | android | mpc-existing-wallet | false / false | unresolved / not mnemonic |
| [bitget-wallet](../../../catalog/wallets/bitget-wallet.json) | Bitget Wallet | android | mnemonic-generated | true / false | unresolved / not mnemonic |
| [bitget-wallet-mpc](../../../catalog/wallets/bitget-wallet-mpc.json) | Bitget Wallet | android | mpc-keyless | false / false | unresolved / not mnemonic |
| [bitget-wallet-cloud-backup](../../../catalog/wallets/bitget-wallet-cloud-backup.json) | Bitget Wallet | android | mpc-cloud-backup | false / false | unresolved / not mnemonic |
| [safepal](../../../catalog/wallets/safepal.json) | SafePal | android | software-mnemonic-generated | true / false | unresolved / not mnemonic |
| [tangem-seed](../../../catalog/wallets/tangem-seed.json) | Tangem | hardware | app-generated-seed | true / false | bip39 |
| [tangem-seed-import](../../../catalog/wallets/tangem-seed-import.json) | Tangem | hardware | mnemonic-imported | false / true | bip39 |
| [tangem-seedless](../../../catalog/wallets/tangem-seedless.json) | Tangem | hardware | seedless-card-backup | false / false | unresolved / not mnemonic |
| [keystone](../../../catalog/wallets/keystone.json) | Keystone Essential/Pro | hardware | single-backup-generated | true / false | unresolved / not mnemonic |
| [keystone-mnemonic-import](../../../catalog/wallets/keystone-mnemonic-import.json) | Keystone Essential/Pro | hardware | single-backup-imported | false / true | unresolved / not mnemonic |
| [keystone-shamir](../../../catalog/wallets/keystone-shamir.json) | Keystone Essential/Pro | hardware | slip39-generated | true / false | slip39-share |
| [keystone-shamir-import](../../../catalog/wallets/keystone-shamir-import.json) | Keystone Essential/Pro | hardware | slip39-imported | false / true | slip39-share |
| [bitbox02](../../../catalog/wallets/bitbox02.json) | BitBox02 | hardware | mnemonic-generated | true / false | bip39 |
| [bitbox02-mnemonic-import](../../../catalog/wallets/bitbox02-mnemonic-import.json) | BitBox02 | hardware | mnemonic-imported | false / true | bip39 |
| [bitbox02-microsd](../../../catalog/wallets/bitbox02-microsd.json) | BitBox02 | hardware | microsd-backup | false / false | unresolved / not mnemonic |
| [ellipal](../../../catalog/wallets/ellipal.json) | ELLIPAL X Card | hardware | x-card-mnemonic-generated | true / false | unresolved / not mnemonic |
| [ellipal-import](../../../catalog/wallets/ellipal-import.json) | ELLIPAL X Card | hardware | x-card-mnemonic-imported | false / true | unresolved / not mnemonic |
| [coinomi](../../../catalog/wallets/coinomi.json) | Coinomi | android | mnemonic-imported | false / true | bip39 |
| [guarda](../../../catalog/wallets/guarda.json) | Guarda | web | encrypted-backup-file | false / false | unresolved / not mnemonic |
| [guarda-mnemonic-import](../../../catalog/wallets/guarda-mnemonic-import.json) | Guarda | web | mnemonic-imported | false / true | unresolved / not mnemonic |
| [tokenpocket](../../../catalog/wallets/tokenpocket.json) | TokenPocket | web | mnemonic-generated | true / false | unresolved / not mnemonic |
| [tokenpocket-import](../../../catalog/wallets/tokenpocket-import.json) | TokenPocket | web | mnemonic-imported | false / true | unresolved / not mnemonic |
| [tokenpocket-private-key](../../../catalog/wallets/tokenpocket-private-key.json) | TokenPocket | web | private-key-imported | false / true | unresolved / not mnemonic |
| [imtoken](../../../catalog/wallets/imtoken.json) | imToken | android | mnemonic-generated | true / false | unresolved / not mnemonic |
| [rabby](../../../catalog/wallets/rabby.json) | Rabby | web | mnemonic-generated | true / false | unresolved / not mnemonic |
| [rabby-import](../../../catalog/wallets/rabby-import.json) | Rabby | web | mnemonic-imported | false / true | unresolved / not mnemonic |
| [rainbow](../../../catalog/wallets/rainbow.json) | Rainbow | web | mnemonic-generated | true / false | unresolved / not mnemonic |
| [rainbow-cloud-backup](../../../catalog/wallets/rainbow-cloud-backup.json) | Rainbow | ios | icloud-backup | false / false | unresolved / not mnemonic |
| [zerion](../../../catalog/wallets/zerion.json) | Zerion | web | mnemonic-generated | true / false | unresolved / not mnemonic |
| [zerion-cloud-backup](../../../catalog/wallets/zerion-cloud-backup.json) | Zerion | ios | icloud-backup | false / false | unresolved / not mnemonic |
| [sparrow](../../../catalog/wallets/sparrow.json) | Sparrow | windows | bip39-generated | true / false | bip39 |
| [sparrow-electrum-import](../../../catalog/wallets/sparrow-electrum-import.json) | Sparrow | windows | electrum-imported | false / true | unresolved / not mnemonic |
| [bluewallet](../../../catalog/wallets/bluewallet.json) | BlueWallet | ios | bitcoin-mnemonic-generated | true / false | unresolved / not mnemonic |
| [bluewallet-import](../../../catalog/wallets/bluewallet-import.json) | BlueWallet | ios | mnemonic-imported | false / true | unresolved / not mnemonic |
| [bluewallet-private-key](../../../catalog/wallets/bluewallet-private-key.json) | BlueWallet | ios | private-key-imported | false / true | unresolved / not mnemonic |
| [coldcard](../../../catalog/wallets/coldcard.json) | COLDCARD | hardware | mnemonic-generated | true / false | bip39 |
| [blockstream-jade](../../../catalog/wallets/blockstream-jade.json) | Blockstream Jade | hardware | mnemonic-generated | true / false | unresolved / not mnemonic |
| [passport](../../../catalog/wallets/passport.json) | Passport | hardware | mnemonic-generated | true / false | unresolved / not mnemonic |
| [passport-microsd](../../../catalog/wallets/passport-microsd.json) | Passport | hardware | encrypted-microsd-backup | false / false | unresolved / not mnemonic |
| [seedsigner](../../../catalog/wallets/seedsigner.json) | SeedSigner | hardware | dice-mnemonic-generated | true / false | bip39 |
| [seedsigner-photo](../../../catalog/wallets/seedsigner-photo.json) | SeedSigner | hardware | photo-mnemonic-generated | true / false | bip39 |
| [seedsigner-seedqr](../../../catalog/wallets/seedsigner-seedqr.json) | SeedSigner | hardware | seedqr-imported | false / true | bip39 |
| [seedsigner-bip85](../../../catalog/wallets/seedsigner-bip85.json) | SeedSigner | hardware | bip85-child-generated | true / false | bip39 |
| [phantom](../../../catalog/wallets/phantom.json) | Phantom | web | mnemonic-generated | true / false | unresolved / not mnemonic |
| [phantom-social-login](../../../catalog/wallets/phantom-social-login.json) | Phantom | web | social-login | false / false | unresolved / not mnemonic |
| [solflare](../../../catalog/wallets/solflare.json) | Solflare | web | mnemonic-generated | true / false | unresolved / not mnemonic |
| [solflare-social-login](../../../catalog/wallets/solflare-social-login.json) | Solflare | ios | quick-login-cloud-backup | true / false | unresolved / not mnemonic |
| [backpack](../../../catalog/wallets/backpack.json) | Backpack | web | mnemonic-generated | true / false | unresolved / not mnemonic |
| [backpack-import](../../../catalog/wallets/backpack-import.json) | Backpack | web | mnemonic-imported | false / true | unresolved / not mnemonic |
| [backpack-private-key](../../../catalog/wallets/backpack-private-key.json) | Backpack | web | private-key-imported | false / true | unresolved / not mnemonic |
| [glow](../../../catalog/wallets/glow.json) | Glow | web | mnemonic-backup-unresolved | false / false | unresolved / not mnemonic |
| [keplr](../../../catalog/wallets/keplr.json) | Keplr | android | mnemonic-generated | true / false | unresolved / not mnemonic |
| [keplr-social-login](../../../catalog/wallets/keplr-social-login.json) | Keplr | android | google-web3auth-private-key | false / false | unresolved / not mnemonic |
| [leap](../../../catalog/wallets/leap.json) | Leap | web | mnemonic-imported | false / true | unresolved / not mnemonic |
| [cosmostation](../../../catalog/wallets/cosmostation.json) | Cosmostation | web | mnemonic-generated | true / false | bip39 |
| [temple](../../../catalog/wallets/temple.json) | Temple | web | mnemonic-generated | true / false | bip39 |
| [temple-import](../../../catalog/wallets/temple-import.json) | Temple | web | mnemonic-imported | false / true | unresolved / not mnemonic |
| [temple-cloud-backup](../../../catalog/wallets/temple-cloud-backup.json) | Temple | web | google-drive-backup | false / false | unresolved / not mnemonic |
| [kukai](../../../catalog/wallets/kukai.json) | Kukai | web | mnemonic-generated | true / false | unresolved / not mnemonic |
| [kukai-keystore](../../../catalog/wallets/kukai-keystore.json) | Kukai | web | encrypted-keystore | false / false | unresolved / not mnemonic |
| [kukai-social-login](../../../catalog/wallets/kukai-social-login.json) | Kukai | web | directauth-oauth | false / false | unresolved / not mnemonic |

## Source ledger and reproducibility

The ledger below identifies the exact bytes reviewed on2026-09-29. HTTP bodies
were fetched using CPython requests (response.content, after HTTP decoding);
SHA-256 covers those raw decoded response bytes. BeautifulSoup text extraction
was used only for review, without executing page scripts. Source-code .body
files were reviewed as plain UTF-8; HTML extraction is not the code authority.
Caches remain ignored and are not a licensed distribution payload. Only short
original summaries and metadata are committed; no license/SignPath component
assessment is newly granted by this batch.

Two exceptions are clearly labeled: imToken's direct HTTP challenge was not
hashed as product evidence; the official web-tool extracted page (updated
2026-09-20) was hashed as UTF-8 extraction bytes. Leap's official indexed page
was similarly hashed as extraction bytes because direct HTTP returned404.
These are mutable/indexed observations, not archived original HTML or immutable
source pins. Re-fetching can legitimately yield different bytes. Documentation
availability, dependency provenance and platform/version recovery remain gaps.
Failed or empty pages, source discovery shells and search snippets are not used
as positive algorithm evidence. Temple and Passport unavailable docs were
replaced by inspected upstream source at full commits.

### Immutable source ledger

| Evidence source | Commit | Retrieved source-byte SHA-256 | URL |
| --- | --- | --- | --- |
| rabby-mnemonic | `e2b98a27e9ef979ab121e81e591fcf5ad79d6e19` | `4b2df498bb20442574ead7de614b8e6a7bfdc53a7ae2e0cdf7b1197105e36f2d` | [source](https://raw.githubusercontent.com/RabbyHub/Rabby/e2b98a27e9ef979ab121e81e591fcf5ad79d6e19/src/ui/state/createMnemonics.ts) |
| rabby-import | `e2b98a27e9ef979ab121e81e591fcf5ad79d6e19` | `069afc1dfbc7275cf54c68f4f2948cdf306e43f5106023f6bc1799ead818ebea` | [source](https://raw.githubusercontent.com/RabbyHub/Rabby/e2b98a27e9ef979ab121e81e591fcf5ad79d6e19/src/ui/state/importMnemonics.ts) |
| passport-source | `670c3886e8373cbe9ade5b8d48e7ceae2e4cd0d0` | `f8498559a5fd7289634a77deb4213b1d7261d93f3c00d5c424f85d858839b9b6` | [source](https://raw.githubusercontent.com/Foundation-Devices/passport2/670c3886e8373cbe9ade5b8d48e7ceae2e4cd0d0/ports/stm32/boards/Passport/modules/tasks/new_seed_task.py) |
| passport-flow | `670c3886e8373cbe9ade5b8d48e7ceae2e4cd0d0` | `cfc2b1b19da86be7a263ab95085f5ecda0d45f858757e1f432047cb3c44d95d7` | [source](https://raw.githubusercontent.com/Foundation-Devices/passport2/670c3886e8373cbe9ade5b8d48e7ceae2e4cd0d0/ports/stm32/boards/Passport/modules/flows/new_seed_flow.py) |
| passport-backup | `670c3886e8373cbe9ade5b8d48e7ceae2e4cd0d0` | `d29900a319d4deedc58246b60cb20894219ae61a9b3a5e746330ef92d43e9b65` | [source](https://raw.githubusercontent.com/Foundation-Devices/passport2/670c3886e8373cbe9ade5b8d48e7ceae2e4cd0d0/ports/stm32/boards/Passport/modules/flows/backup_flow.py) |
| cosmostation-source | `278e29ab131cff4dda2ac2700863108d3b25e36a` | `dec3c0ed287753d9f0ecc2f9cfe5159991fbd11698cdd0b4f425494a78a658e4` | [source](https://raw.githubusercontent.com/cosmostation/cosmostation-chrome-extension/278e29ab131cff4dda2ac2700863108d3b25e36a/src/pages/account/create-wallet/mnemonic/-entry.tsx) |
| temple-source | `7770f23fffd85a96c2148335bca7c946c84d9337` | `73c47c3e632d6fd6abdd4eee70b367367b3f742e4ca6d7a1e0e5cf74bd8e6311` | [source](https://raw.githubusercontent.com/madfish-solutions/templewallet-extension/7770f23fffd85a96c2148335bca7c946c84d9337/src/lib/temple/back/vault/index.ts) |
| temple-import | `7770f23fffd85a96c2148335bca7c946c84d9337` | `63d7185040400a8a3d4753d0b842729df935cb766440d0be8b2e79c8c7b6dade` | [source](https://raw.githubusercontent.com/madfish-solutions/templewallet-extension/7770f23fffd85a96c2148335bca7c946c84d9337/src/app/templates/ImportAccountModal/forms/mnemonic.tsx) |
| temple-cloud | `7770f23fffd85a96c2148335bca7c946c84d9337` | `085466d4f8e74694f6438a813a7b9da813326ea399a034d3d160333916fc1a01` | [source](https://raw.githubusercontent.com/madfish-solutions/templewallet-extension/7770f23fffd85a96c2148335bca7c946c84d9337/src/app/layouts/PageLayout/BackupMnemonicOverlay/google-backup-modal-content.tsx) |

### Mutable documentation ledger

| Evidence source | Representation | SHA-256 | URL |
| --- | --- | --- | --- |
| trust-classic | decoded HTTP response body | `0d11be8c0fba06e7a47c991079f933782d80c6ee9a70bbb7898284a3bcd7ff06` | [source](https://trustwallet.com/blog/academy/what-is-a-seed-phrase-and-why-is-it-important) |
| trust-wallet | decoded HTTP response body | `9a714d9eac177eb8b7861d211cdc11eda9c38d3346d63fe437fb790340596314` | [source](https://trustwallet.com/blog/security/what-are-passkeys) |
| trust-wallet-swift | decoded HTTP response body | `47428b82d857cc5335fe1558bf0913ea34ce937de521f3d8dfaa078c1b2b40f3` | [source](https://trustwallet.com/swift) |
| metamask | decoded HTTP response body | `c245a4907a21d310270069c3488f20961f8cbebd12ed288bf54225bc8b903189` | [source](https://support.metamask.io/start/user-guide-secret-recovery-phrase-password-and-private-keys) |
| coinbase-wallet | decoded HTTP response body | `1d65b63ed007b5b405e1aca52d0f939a483144ecd9db2bd37941344aa31148b2` | [source](https://help.coinbase.com/en/wallet/getting-started/smart-wallet) |
| coinbase-recovery | decoded HTTP response body | `12e56c471b07282398e28380ee5128f9ff2e6be7066e2cafed57c3d65d6552c5` | [source](https://help.coinbase.com/en/wallet/getting-started/smart-wallet-recovery) |
| coinbase-cloud | decoded HTTP response body | `4255ad095c105d1b6bb79d9e14f7e7bcb33c676367ee2b5527efe2d9fc1a849b` | [source](https://help.coinbase.com/en/contact-us/support-faq/coinbase-wallet/how-to-recover-access-to-coinbase-wallet) |
| exodus | decoded HTTP response body | `069661f51ab1b253d632fdcc820738b240ff478290963826f90bd1157da207f5` | [source](https://www.exodus.com/support/en/articles/8598627-everything-you-need-to-know-about-your-12-word-secret-recovery-phrase) |
| atomic-wallet | decoded HTTP response body | `cd66b03392fb8c0584673194407955126af7977bfd6b81c0fe022ce568fb2290` | [source](https://support.atomicwallet.io/article/35-what-is-12-word-recovery-phrase) |
| onekey | decoded HTTP response body | `6bf15e920abf565452cba9b9a43b083f81a84a3bc1775b2d828133d7e5fac563` | [source](https://help.onekey.so/en/articles/11461081-get-started-with-onekey-pro) |
| ledger | decoded HTTP response body | `48ed5a86fa4a503232460e9e6cdd693e20536c159aefa61b9dff1679120d8b27` | [source](https://www.ledger.com/academy/basic-basics/2-how-to-own-crypto/whats-a-secret-recovery-phrase) |
| okx-wallet | decoded HTTP response body | `b06df9a2d93a88de2735af96ba233d05687108047c781042d09140d5bc357083` | [source](https://www.okx.com/en-gb/help/how-do-i-manage-my-wallet-app) |
| okx-mpc | decoded HTTP response body | `a31421d257c5bc95c13672d58b41464c9eff0677a784d30e72aebbde9a7e89e3` | [source](https://www.okx.com/en-gb/help/what-is-okx-keyless-wallet) |
| bitget-wallet | decoded HTTP response body | `bc5c1394731b946ba18b4feb4ea6f94ac5910a848f5b8ca28ed64430294552bb` | [source](https://web3.bitget.com/en/academy/how-to-use-an-mpc-wallet-or-a-mnemonic-wallet) |
| safepal | decoded HTTP response body | `8233d300de67d2fb7aac9031d76d6c1868de1d40c354cbfdbb7e84e9de7bcbcd` | [source](https://www.safepal.com/en/blog/tutorial-software-wallet) |
| tangem-seed | decoded HTTP response body | `39be36bfad5ad935f17768dba15a1b81035df02c685890ef4be42b577ba601a8` | [source](https://tangem.com/en/blog/post/seed-phrase-faq/) |
| tangem-seedless | decoded HTTP response body | `0e224d2d4923fe8d107b64f68ef3c2d81ec5ac2d7133f5afca2b91481380692a` | [source](https://tangem.com/en/blog/post/onboarding-tangem-ama/) |
| keystone | decoded HTTP response body | `13706e85e7f067e4f719a2e1c931bda3e6fd736996087b3e4ef93c06615ee56d` | [source](https://support.keyst.one/getting-started/setting-up-keystone-new) |
| keystone-shamir | decoded HTTP response body | `c9e4fc678240b68de31a9a25a7ed12e2d5e5e88860ba9349f556cec8d673be35` | [source](https://support.keyst.one/advanced-features/recovery-phrase/import-or-create-shamir-backup) |
| bitbox02 | decoded HTTP response body | `41e32d676620a8f0b35f8479c573910ac15deab61733f3d7d7c75527e3f0694b` | [source](https://support.bitbox.swiss/en_US/erweiterte-backup-optionen-bitbox02) |
| bitbox02-import | decoded HTTP response body | `a54492f733f61b85ee7a3367a3f390e3c2ee99b90f92358ac0dcf8e5566a57e7` | [source](https://support.bitbox.swiss/en_US/how-to-restore-from-recovery-words) |
| ellipal | decoded HTTP response body | `8298236125062cd1212c5afb275ee508857ba1845a50e22c8a8b16ccf6340abb` | [source](https://www.ellipal.com/en-br/pages/x-card-setup-guide) |
| coinomi | decoded HTTP response body | `6242fd9e4de599577e70d398a4c3cfb4537d84de409a0b72a2b392c1759546aa` | [source](https://coinomi.freshdesk.com/support/solutions/articles/29000019254) |
| guarda | decoded HTTP response body | `174800cedf36b5ec2379deed5ad9f3e57f21bfd3c404c00ebfeb1d2f813ac91c` | [source](https://guarda.com/support/security/what-is-a-backup-file/) |
| guarda-import | decoded HTTP response body | `c6f3e00c73031b9a0822c03c8ca5afebec1dd2c40d501c63b5fe480e08032c3c` | [source](https://guarda.com/academy/tutorials/how-to-restore-your-crypto-wallet-using-a-mnemonic-phrase/) |
| tokenpocket | decoded HTTP response body | `1a19c549dc63e25b929aab162aa2061067cb3aa40f482f2425ddda847d5ee502` | [source](https://help.tokenpocket.pro/en/extension-wallet/faq/basic-intro) |
| imtoken | UTF-8 web-tool extracted page; direct HTTP retrieval blocked or unavailable | `6b49c3bf1b6646a71684093a4bbbc122e987b4bb27a1ffd6a4be4f86a1890e9f` | [source](https://support.token.im/hc/en-us/articles/28921881978265-How-to-create-a-wallet) |
| rainbow | decoded HTTP response body | `be686dc3c5b3c26e4ff1fb8b9ae1e81404cbc89c918ebba9329170374ce741d4` | [source](https://rainbow.me/support/extension/get-started-with-the-rainbow-extension) |
| rainbow-cloud | decoded HTTP response body | `f24b74d203c7b974b47d873775b5a0c04a21d8fde3e7873f3eb651a81a6a9e9d` | [source](https://rainbow.me/support/app/restore-from-a-backup) |
| zerion | decoded HTTP response body | `c37b8caa2a8e75cec5b2a0f38f429c093eb2b629d495934afa01edfe0478487f` | [source](https://help.zerion.io/en/articles/9657118-create-your-first-wallet-in-zerion) |
| sparrow | decoded HTTP response body | `853a96de90aedc07ed80fbd2d003765db03bb568ffd7b1517e6c1adcac7e6f25` | [source](https://www.sparrowwallet.com/docs/quick-start.html) |
| bluewallet | decoded HTTP response body | `47a847355b7d79459cbb21207184a4ca4aff561e3144b8a18df7fdc8d3d85eba` | [source](https://bluewallet.io/docs/intro/) |
| coldcard | decoded HTTP response body | `0a7991f6d468e694098fc762346edf13f35fd10799674c2f8031790a7a86d861` | [source](https://coldcard.com/docs/quick/) |
| blockstream-jade | decoded HTTP response body | `ecc74e713f7e865062baec4783363a1d87ede53c37aa31d88e4ca6b8652daca3` | [source](https://help.blockstream.com/blockstream-jade/faqs/blockstream-jade-quickstart-guide-for-desktop.md) |
| seedsigner | decoded HTTP response body | `106362fa6af27750e9bf76ea1d09dee0f066cf8005253d5c94d16e0c95a1ab82` | [source](https://seedsigner.com/) |
| phantom | decoded HTTP response body | `14c729c88449e342d194a63d059a89a9f3c50a0bb2699e27caf44972d1495ee2` | [source](https://help.phantom.com/articles/how-to-create-a-new-wallet-in-phantom-8071074929043) |
| solflare | decoded HTTP response body | `a4468500040d56fa04d5729504527f337d64590578fdf90e99ecf00f25811317` | [source](https://help.solflare.com/en/articles/6134545-how-to-generate-a-wallet-with-a-recovery-phrase-desktop) |
| solflare-social | decoded HTTP response body | `d55bd3950a0f2a9ef83498ab1bb71ba5a4b016e6fe0bd04a479532a34db1fd9d` | [source](https://help.solflare.com/en/articles/16944009-create-a-new-wallet-with-quick-login) |
| backpack | decoded HTTP response body | `d48b55cce4a72115acfc9c559eebbffe84fef627c888c6acb079e93728f9a081` | [source](https://support.backpack.exchange/wallet/get-started) |
| glow | decoded HTTP response body | `77d6d9331b55f325d74c2194560fdd4fff81437e229773be671f98349c195e20` | [source](https://glow.app/) |
| glow-support | decoded HTTP response body | `98e9c925bdfb2a4bb1f83c55182127261e04f507d6d3ca66c3cc9b2f08e86bc1` | [source](https://glow.app/support) |
| keplr | decoded HTTP response body | `52e4154a556731e3e193d7f08852f497b33389801b66abbc70b3eb6cd3a7dcf4` | [source](https://help.keplr.app/mobile-app/5R3bMyjtr3iKzMhqyCqu56/create-a-new-wallet-with-keplr-mobile/5R3bMyjtr5cEFHpvssu2G4) |
| leap | UTF-8 web-tool extracted page; direct HTTP retrieval blocked or unavailable | `e16436522b5c4a6bce9948720a8b5ea87347d27d8eaf6889fc080bf5445e9828` | [source](https://www.leapwallet.io/support/import-your-existing-keplr-wallet-into-leap) |
| kukai | decoded HTTP response body | `88483abb01630e7421a7d0fb0a67a2cb94f3d6e5a0e4431291a40ace1f674afa` | [source](https://docs.kukai.app/learn-kukai/new-wallet) |
| kukai-social | decoded HTTP response body | `341aa123a53c94f13ae3035847f2409ef9cfd81e87bca3ea3f9b1abbb8718cbc` | [source](https://docs.kukai.app/learn-kukai/direct-auth) |
| network-bitcoin | decoded HTTP response body | `ecf8cd25398eb5590b5ba770420402a928058503b0aa2e13ada734a554ceb70a` | [source](https://bitcoin.org/en/choose-your-wallet) |
| network-ethereum | decoded HTTP response body | `0218e8b8204d59a5abc3c5235e8c6ad35d7781ef294b740ba9683f27f63638a9` | [source](https://ethereum.org/en/wallets/) |
| network-base | decoded HTTP response body | `337f996551fbf9a7cd197210a9140e9ac46b3644ee64e76f22f49cae607f64c3` | [source](https://docs.base.org/base-chain/quickstart/connecting-to-base) |
| network-bnb-chain | decoded HTTP response body | `68b333d42320adfeeba0a2ab1ca9a4a46b84d6ddce4deee64ca43c633bd92996` | [source](https://docs.bnbchain.org/) |
| network-polygon | decoded HTTP response body | `a733bb44ab6e7489a468b12dae9972b972039641b2ece7e7c68d66965b15cdf0` | [source](https://docs.polygon.technology/) |
| network-avalanche | decoded HTTP response body | `07aa1c4f21f565cbc50139515e7fa4e4485d0b33c021b54999530e608594c69f` | [source](https://build.avax.network/docs/quick-start/networks) |
| network-arbitrum | decoded HTTP response body | `ceda32c7434bafd551b361441e520df6902cdf1983fa877e3f9f8c2d256aefbb` | [source](https://docs.arbitrum.io/for-devs/dev-tools-and-resources/chain-info) |
| network-solana | decoded HTTP response body | `8ae6154eb16497da8876c4be9b2ccb91392a3e805b2b57cb8c190ca619815461` | [source](https://solana.com/docs/core/accounts) |
| network-tron | decoded HTTP response body | `3d7368ebff0bd3cec14c74ecb5197c8f47030a8d0b1741e6810fc5d2bbf71b51` | [source](https://developers.tron.network/docs/account) |
| network-cosmos | decoded HTTP response body | `eb58d7c87a4b3ef9ac07188e2f8fc51bf8a6cfb7f3896c2ed45ea6958fa6b490` | [source](https://docs.cosmos.network/) |
| network-tezos | decoded HTTP response body | `f4f01c4b9c99246bfc27f8f4d9cca8fec85f591fa3a3e2763bbff11bf6f3a6a4` | [source](https://docs.tezos.com/) |
| network-polkadot | decoded HTTP response body | `2c97d5dfd5b7adcdc3ce53197fd24edc560a142662589a776dbace7a0d4f133b` | [source](https://docs.polkadot.com/reference/parachains/accounts/) |
| network-kusama | decoded HTTP response body | `25eb213fda835aaa94077ef7115329fc61e68ae60fec7b03dc0e112ca500e2dc` | [source](https://guide.kusama.network/docs/kusama-accounts/) |
| network-cardano | decoded HTTP response body | `4bb87b35c4445fa71e19df942f7c2e99fe7704971bcca634d0b8a519e1393575` | [source](https://docs.cardano.org/) |
| network-algorand | decoded HTTP response body | `58d26cf32c712dbb67764cead8a191620f632e640e80154728d97dc6517af206` | [source](https://dev.algorand.co/concepts/accounts/overview/) |
| network-monero | decoded HTTP response body | `7b12e0abdde1eb836bcab38f1cf8528db3d642272dafe8e29f78a57fbc7c237e` | [source](https://www.getmonero.org/resources/moneropedia/mnemonicseed.html) |
| network-zcash | decoded HTTP response body | `73c5b4702f535e2c087f4b5c833d8c5a6a4a34394b728c377e8fb1e1d621f0fa` | [source](https://zips.z.cash/zip-0339) |
| network-chia | decoded HTTP response body | `5d633c523485ed1c47186f4ea42257e705ae42e489aca65cbd5fcd34b32ca2c4` | [source](https://docs.chia.net/chia-blockchain/keys/keys-and-signatures/) |
| network-decred | decoded HTTP response body | `68a647b0a9ffb13345c551c09e54dc8c25197042958ea1d93ac17bdcfc95c9cb` | [source](https://decred.org/) |
| network-zano | decoded HTTP response body | `2a6b8410f6012d262dd287649401b8db94e6f045a23d60f10e4d1fbc6435fe90` | [source](https://docs.zano.org/) |
| network-sia | decoded HTTP response body | `8b0763a91182eabce60b2b60c0e319a4fb91a1af7ea8d05c40bab96431b15e18` | [source](https://docs.sia.tech/) |
| network-ton | decoded HTTP response body | `8a394dc065dbc8c2e82aefc5b74ee16770d4b8800e2d0af3a77a39f4c1df9fe3` | [source](https://docs.ton.org/) |

## Verification scope

Identity tests include simultaneous modes, import/generation contradiction,
normalized ambiguous aliases, disjoint platforms, cross-platform overlap,
closed and open numeric bounds, opaque snapshots, reversed ranges and oversized
numeric strings. Full offline Python tests and catalogue generation are checked
before commit. Existing Rust1.90 host checks remain host evidence only. No
physical-device, clean-machine, signing, security-audit or Windows release gate
is cleared by terminal catalogue coverage.
