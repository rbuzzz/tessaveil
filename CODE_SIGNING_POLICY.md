# Code-signing and release policy

The first functional candidate, `v0.1.0-rc.1`, may be published as an **unsigned pre-release** because SignPath Foundation requires an already released and documented open-source project. It must carry a SHA-256 checksum, GitHub artifact provenance tied to the exact source commit, an SBOM, successful CI, test and clean-machine verification summaries, and conspicuous unsigned labeling. It is not a stable release.

The preferred later path is an application to SignPath Foundation. The repository owner must enable GitHub two-factor authentication. Separate authorized reviewers assess changes and an authorized approver manually approves release signing; the build must originate from the protected repository workflow and verified source. Signing requests must use SignPath's trusted-build/origin-verification flow. No contributor may sign an unreviewed local binary as a project release.

If accepted, the certificate belongs to SignPath Foundation and Windows will display **SignPath Foundation** as publisher, not Tessaveil. Acceptance and SmartScreen reputation are not guaranteed. After integration, publish a signed subsequent RC, then verify the exact signed artifact on supported clean Windows systems before any stable release.

If SignPath declines or delays the project, unsigned RCs are never stable releases. Stable publication stops pending an explicit owner decision to remedy and reapply, approve a separately funded CA certificate, or revise the release criteria. No certificate purchase or unsigned-stable exception is implicit.
