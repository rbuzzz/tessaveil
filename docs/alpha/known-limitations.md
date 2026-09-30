# Known limitations — unsigned Windows engineering alpha

Synthetic data only. No real funds, seeds, private keys or wallet backups.
Not RC/stable; no Authenticode; no final format/KDF/migration promise.
Windows release/freeze remains NO-GO. Security audit: not yet independently completed.

Binary publication is blocked unless the same-run static-Qt/full-runtime source,
notice, corresponding-application-object, modified-library relink and artifact
audits all pass. The engineering review is not legal assurance. Local
hashes and locally generated JSON are not GitHub provenance. Unsupported GitHub
attestation permissions must cause a failing job, not an attestation claim.

Evidence from this development host or a Windows Server CI runner does not prove
clean Windows 10/11 behavior, physical mobile KDF compatibility, removable-media
durability, power-loss recovery, Narrator support or an independent security audit.
Final cross-platform format and KDF decisions remain open; schema 2 alpha files
carry no migration promise. Windows 10 trusted-device use requires current ESU
security updates after ordinary support ends.

Automatic privacy/inactivity locks discard unsaved changes. Save before switching
apps. Sheet passwords prevent accidental edits after unlock and are not a second
cryptographic boundary. Spin does not expose validity, ordering or target signals;
timing resistance and protection against a compromised OS are not promised.

Input zeroization is best effort. Host/IME/paging/crash-dump copies and screenshots
remain outside its guarantee. Existing development-host hooks are unresolved.
No complete network/process/file event trace or OS clipboard-content observation
has been established. Empty TEMP snapshots do not exclude transient extraction.
The alpha UI is English/dark; final localization, themes and product flows remain.

There is no GitHub Release/tag, installer or update channel for this work.
The build recipe and archive metadata are pinned; byte-identical executable
reproducibility across separate hosts is not established.
