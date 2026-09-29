# Contributing

Tessaveil is in a research phase. Start by opening an issue describing the proposed change and the affected specification, catalogue record, or probe. Keep each pull request focused and include the evidence needed to reproduce its claims.

For wallet formats and dictionaries, cite a primary source, its version or revision, the UTC verification date, and the exact product mode. Distinguish a wallet's ability to **create** a mnemonic from its ability to import one. Record uncertainty and blocked findings explicitly; do not infer a format from a product name. Dictionary contributions require a source license, redistribution decision, attribution, and a separate code-signing compatibility decision.

Use synthetic test inputs only. Never submit a real seed phrase, funded key, user vault, credential, token, or local user path. Run `python tools/run_tests.py` and describe the result in the pull request. Security issues should follow [SECURITY.md](SECURITY.md), not a public issue.

Contributions to original project code are offered under Apache-2.0. Do not assume that this licenses third-party dictionaries, documents, or trademarks.
