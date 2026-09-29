# Tessaveil

Tessaveil is public research toward an offline mnemonic backup table. The current repository contains specifications and will add a source-backed wallet and dictionary catalogue, threat model, and disposable feasibility probes. It does **not** contain a usable vault application or a release binary. Windows is the first proposed product; Android and iOS compatibility is a future requirement, not a current feature.

Security audit: not yet independently completed

No code or document here should be used to protect real funds. Do not submit a real recovery phrase, private key, funded wallet, or vault to issues, pull requests, tests, or sample data. A public repository and automated checks are not an independent security audit.

Project policies: [security reporting](SECURITY.md), [privacy](PRIVACY.md), [contributions](CONTRIBUTING.md), [code signing](CODE_SIGNING_POLICY.md), and [third-party notices](THIRD_PARTY_NOTICES). [Русский README](README.ru.md).

Original project code is licensed under Apache-2.0; third-party dictionaries, source material, and other components retain their own licenses and require separate review before inclusion or redistribution.

For the current research gate, install the pinned development requirements with `python -m pip install -r requirements-dev.txt`, then run `python tools/run_tests.py`. Catalogue validation is added when its CLI exists.
