# Tessaveil

Tessaveil is public research toward an offline mnemonic backup table. The repository now contains a working **unsigned Windows engineering alpha for synthetic data only**, alongside specifications, a source-backed wallet and dictionary catalogue, a threat model, and feasibility probes. It is **not production-ready, RC or stable** and must never be used for real secrets or funds. Android and iOS compatibility remains a future requirement, not a current feature.

The exact predecessor branch artifact at `4c3e9de5b0e7936edc030992584ae6cdd59493ed` passed the static-Qt source/notices/relink and artifact gates and official GitHub provenance verification. That evidence does not approve later commits or PR runs, nor clear Windows release/freeze NO-GO. See the [exact-SHA evidence ledger and remaining gates](docs/alpha/release-evidence.md) and [synthetic-only alpha guide](docs/alpha/user-guide.md).

Security audit: not yet independently completed

No code or document here should be used to protect real funds. Do not submit a real recovery phrase, private key, funded wallet, or vault to issues, pull requests, tests, or sample data. A public repository and automated checks are not an independent security audit.

In the proposed design, Tessaveil briefly sees the current word and column, cannot defeat a compromised OS, and does not validate complete phrases. It does not replace a separate cold backup or trusted hardware-wallet process. Identical copies of one unchanged table add no new table-comparison signal; different saved tables can expose invariant real words after decryption. Full row or table re-randomization does not remove cross-version intersection risk. Read the [threat model and backup warnings](THREAT_MODEL.md#english) before evaluating the design. Research completion does not authorize a product release: Windows release remains NO-GO, as do format/KDF freeze and unverified physical-device/removable-media guarantees.

Project policies: [security reporting](SECURITY.md), [privacy](PRIVACY.md), [contributions](CONTRIBUTING.md), [code signing](CODE_SIGNING_POLICY.md), and [third-party notices](THIRD_PARTY_NOTICES). [Русский README](README.ru.md).

Original project code is licensed under Apache-2.0; third-party dictionaries, source material, and other components retain their own licenses and require separate review before inclusion or redistribution.

For the current research gate, install the pinned development requirements with `python -m pip install -r requirements-dev.txt`, then run `python tools/run_tests.py`. Check terminal research coverage with `python -m tools.catalog.cli validate --root . --require-terminal` and generated documentation with `python -m tools.catalog.cli generate --root . --check`. The separate `python -m tools.catalog.cli validate --root . --require-release-ready` gate currently fails on documented required blockers; research success does not clear them.
