# Contributing

Tessaveil is in a research phase. Start by opening an issue describing the proposed change and the affected specification, catalogue record, or probe. Keep each pull request focused and include the evidence needed to reproduce its claims.

For wallet formats and dictionaries, cite a primary source, its version or revision, the UTC verification date, and the exact product mode. Distinguish a wallet's ability to **create** a mnemonic from its ability to import one. Record uncertainty and blocked findings explicitly; do not infer a format from a product name. Dictionary contributions require a source license, redistribution decision, attribution, and a separate code-signing compatibility decision.

Every research batch must follow the [four-level source policy](docs/research/source-policy.md) and [licensing decision matrix](docs/research/licensing.md). Supply exact source revision (full commit for official source), byte hashes, reproducible vectors, actual license evidence, copyright/attribution and fulfillment of notice obligations. Link narrowly scoped evidence to the affected records. No circular evidence or self-generated expected outputs may establish verification.

Only `repository_redistribution=allowed` AND `signpath_compatible=compatible` may pass the licensing gate for `verified` or bundling. `forbidden`/`unclear` redistribution and `incompatible`/`pending` signing decisions block both; retain research metadata without unapproved bytes. A local compatibility assessment is not SignPath project acceptance. Update THIRD_PARTY_NOTICES only for actual bundled material, with its original terms preserved.

Follow the [Code signing policy](CODE_SIGNING_POLICY.md): a first unsigned RC needs SHA-256 and exact-commit provenance and remains non-stable. Stable releases require the externally accepted signing path and signed-artifact verification. Remediation, alternative signing arrangements, paid certificates and acceptance-criterion changes require owner action.

Use synthetic test inputs only. Never submit a real seed phrase, funded key, user vault, credential, token, or local user path. Run `python tools/run_tests.py` and describe the result in the pull request. Security issues should follow [SECURITY.md](SECURITY.md), not a public issue.

Contributions to original project code are offered under Apache-2.0. Do not assume that this licenses third-party dictionaries, documents, or trademarks.
