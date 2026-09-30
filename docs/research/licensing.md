# Licensing and signing eligibility

Verified UTC: **2026-09-29**. Recheck upstream terms for each new material
revision and before any signing application or release. Apply
[source-policy.md](source-policy.md) in every research batch.

## Two independent decisions

For each dictionary and prospective bundled component, inspect the actual
license files/headers at the exact revision, scope (including generated data),
copyright, attribution, dependencies and intended distribution form. Record
the chosen branch of any license alternative and all cumulative obligations.
Do not infer permission from a download button, public repository, package
metadata, familiar SPDX identifier, or the project's own Apache license.

`repository_redistribution` has exactly these outcomes:

- `allowed`: reviewed terms permit the intended redistribution and every
  applicable obligation has an identified, implementable fulfillment plan.
- `forbidden`: reviewed terms prohibit the intended distribution, or required
  conditions cannot be met in that distribution.
- `unclear`: license scope, provenance, terms or compliance evidence is missing
  or ambiguous; further review is required.

`signpath_compatible` is a separate, local component assessment:

- `compatible`: evidence supports compatibility with the selected SignPath OSS
  arrangement for the intended component use, with obligations recorded.
- `incompatible`: a known component condition conflicts with that arrangement.
- `pending`: compatibility has not been established, including uncertain
  treatment of data licenses, exceptions or mixed licensing.

Only `allowed` AND `compatible` can pass. Any non-positive outcome blocks both
`verified` and bundling, even when redistribution alone is lawful. Keep metadata
and primary evidence as `documented` or `blocked`; keep unapproved bytes out of
the repository and release. These flags are necessary conditions, not complete
license clearance or release authorization. Legacy `denied`/`pending` values for
redistribution are rejected, not silently translated into permission.

## Executable decision matrix

`pass` means this license gate only; other provenance, integrity, vector,
mapping and release gates still apply. Tests execute all nine rows through the
real validator and reject missing, duplicate or altered outcome vocabulary.

| repository_redistribution | signpath_compatible | License gate |
| --- | --- | --- |
| allowed | compatible | pass |
| allowed | incompatible | block |
| allowed | pending | block |
| forbidden | compatible | block |
| forbidden | incompatible | block |
| forbidden | pending | block |
| unclear | compatible | block |
| unclear | incompatible | block |
| unclear | pending | block |

## Official terms and project eligibility

The [Foundation conditions](https://signpath.org/terms.html), currently labeled
draft, require OSI-approved licensing without commercial dual-licensing across
components, no proprietary components (with a system-library exception), active
maintenance, an existing release and documented functionality. Foundation
certificates add ownership, security, privacy, uninstall, role, MFA, metadata,
verifiable-build and manual-approval conditions; restrictions on security tools
and signing upstream binaries also apply. Acceptance is discretionary and may
be revoked. This is not a component-license whitelist.

The [official application page](https://signpath.org/apply.html) is the owner’s
application entrypoint. No application or acceptance is asserted here. Our
`compatible` flag cannot establish project reputation, operational compliance,
Foundation acceptance, a certificate, or SmartScreen reputation. Review actual
application behavior and distribution with the Foundation when needed; do not
assume an offline security-related product is automatically eligible.

## Apache-2.0 and third-party material

The [actual Apache-2.0 text](https://www.apache.org/licenses/LICENSE-2.0.txt)
permits source/object redistribution subject to its conditions. Section 4
requires the license copy, notices of modifications, preservation of relevant
source notices and applicable upstream NOTICE attribution. Sections 3 and 6
address the patent grant/termination and lack of a general trademark grant.
The [OSI license entry](https://opensource.org/license/apache-2-0) confirms
its open-source approval; that alone does not establish SignPath acceptance.

The repository's Apache-2.0 covers original contributions. It does not relicense
word lists, vectors, embedded Unicode data, upstream code or trademarks. Inspect
each artifact's own terms, including static-linking and redistribution duties;
permissive metadata alone cannot establish a positive decision. Preserve required
third-party licenses and attribution rather than replacing them with our LICENSE.

The [Task 6 dependency inventory](../../spikes/mobile/dependency-review.md)
records locked research dependencies and a limited source-license inspection.
It explicitly leaves full file-level/Unicode-data review, notices, SBOM and
SignPath review pending. Its downloads and host-only probe results are not
bundled application components. Do not add invented distribution notices for
them. Before bundling, prepare the real attribution bundle and update
[THIRD_PARTY_NOTICES](../../THIRD_PARTY_NOTICES) for the actual payload.

## Review record and enforcement limits

Store source/version/commit, relevant file paths, byte SHA-256, exact license
URL/revision, attribution and obligations in the research note. Dictionary
`license` fields record the identifier/name, URL, attribution, both decisions
and nonempty `decision_evidence` links. Evidence claims explain each conclusion,
intended use, reviewer and verification date, citing actual primary terms.

The validator enforces the two positive decisions for `verified` dictionaries
and for referenced word-list bytes even under another status (`license-decision`).
It checks evidence links, not legal truth. Reviewers must inspect the complete
repository/release payload, including unreferenced files and non-dictionary
components, before bundling. An absent `wordlist_path` is no permission to copy
an unapproved file elsewhere. No release packager exists in this research stage.
Follow [Code signing policy](../../CODE_SIGNING_POLICY.md) for release gates.

## Primary-source retrieval fingerprints

Fetched and inspected 2026-09-29 UTC. SHA-256 values identify retrieved response
body bytes (after HTTP decoding), not signatures or an archived legal guarantee.
HTML may change between requests; preserve a lawful review snapshot outside the
distributed payload where needed. Never silently reuse these hashes as current.

| Source | SHA-256 |
| --- | --- |
| [Foundation conditions](https://signpath.org/terms.html) | `6610cf889bbe0dc7533abaa310bc7a5cc9a61ae6c2ce0798a08109c925b46c51` |
| [Application](https://signpath.org/apply.html) | `70c969adb059ae7edf23073b0a9e9d8e7b8d0d7eebb00d66d22fd4c6c2315aec` |
| [Apache-2.0 text](https://www.apache.org/licenses/LICENSE-2.0.txt) | `cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30` |
| [OSI Apache-2.0 entry](https://opensource.org/license/apache-2-0) | `8d5c1c76d25d21f1ae3533f16f3e7b5fcba5468acee66e1c229e893efc8b618d` |
