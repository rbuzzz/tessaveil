# Tessaveil

Tessaveil is an offline Windows application for creating encrypted decoy tables
for mnemonic backups that already exist. This branch contains a working
**unsigned Windows v1 candidate for synthetic data only**. It is not an RC,
stable release, or permission to use real secrets or funds. The current verdict
is **NO-GO для реальных данных**.

Security audit: not yet independently completed

The application can create/open/save a schema-2 `.tessaveil-alpha` vault,
manage multiple protected sheets, use immutable custom-dictionary snapshots,
perform neutral single-row Spin, record the user's “Verified by me” assertion,
make a byte-identical authenticated backup, restore to a new destination, and
rotate the master password. It supports Russian/English, system/light/dark
themes, keyboard operation, privacy cover, explicit lock, and tested
development-host scaling. It never accepts or returns a complete phrase or an
order key and does not derive wallet keys, addresses, or balances.

Only three exact profiles are selectable, all with 24 rows:

- `mytonwallet-native / ton-native-generated`, web,
  `26.9.8-source-f042bcc06b84f0cec928a29795f1cb8bf60a3e9c`;
- `tonhub / ton-native-generated`, Android,
  `2.5.45-source-a2503f79d14868d65349ad7035d18389c6e2f996`;
- `tonkeeper-classic / ton-native-generated`, web,
  `source-4942adcdcddf55d57e3d3fc3676f019caf87357e`.

Tonkeeper Multichain, Gram Wallet, MyTonWallet multichain, and other mandatory
catalogue entries remain visible but non-selectable at their exact terminal
status. Use the original trusted wallet's own backup/recovery procedure for an
unavailable mode; import support or a shared dictionary is not proof of
generation compatibility. See the [generated catalogue](docs/catalog.md) and
the [bilingual candidate guide](docs/alpha/user-guide.md).

Never submit a recovery phrase, order key, private key, funded-wallet backup, or
user vault to Tessaveil issues, pull requests, tests, CI, agents, or websites.
Tessaveil briefly sees the current word and column, cannot defeat a compromised
OS, and does not validate complete phrases. It does not replace a separate cold
backup or trusted hardware-wallet process. A lost master password is
unrecoverable. Password rotation does not revoke old copies or their old
passwords. Different retained tables for the same phrase can reveal unchanged
words after password disclosure. Full row or table re-randomization does not
remove cross-version intersection risk. Windows release remains NO-GO.
Read the [threat model](THREAT_MODEL.md) and
[known limitations](docs/alpha/known-limitations.md).

An exact candidate is packaged only as
`Tessaveil-unsigned-synthetic-windows-v1-candidate-<source-sha>` with separate
`-runtime.zip`, `-compliance.zip`, `-release-decision.json`, and
`-manifest.json` files. The manifest binds names, sizes, SHA-256 values,
`Tessaveil.exe`, SBOM, notices, and the fail-closed decision. A technical package
PASS is not real-data authorization. Keep the compliance archive and external
manifest with the runtime and verify all hosted bytes and GitHub provenance.

Development checks use the pinned requirements:

```text
python -m pip install -r requirements-dev.txt
python tools/run_tests.py
python -m tools.catalog.cli validate --root . --require-terminal
python -m tools.catalog.cli generate --root . --check
```

`--require-release-ready` intentionally remains blocked while mandatory
physical-device, clean-Windows, removable-media, audit, signing, format/KDF,
typography, trace, and exact hosted-evidence gates are unresolved.

Project policies: [security reporting](SECURITY.md), [privacy](PRIVACY.md),
[contributions](CONTRIBUTING.md), [code signing](CODE_SIGNING_POLICY.md), and
[third-party notices](THIRD_PARTY_NOTICES). [Русский README](README.ru.md).
Original project code is Apache-2.0; third-party material keeps its own terms.
