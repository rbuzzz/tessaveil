#![cfg(windows)]
use std::os::windows::fs::OpenOptionsExt;
use tessaveil_core::{CreateOptions, StoragePolicy, VaultError, VaultService};
#[test]
fn actual_windows_sharing_denial_keeps_previous_vault() {
    let dir = tempfile::tempdir().unwrap();
    let path = dir.path().join("locked.tessaveil-alpha");
    let mut vault = VaultService::create(
        &path,
        "synthetic-test-password",
        CreateOptions {
            storage: StoragePolicy::DevelopmentLocalNtfs,
            ..Default::default()
        },
    )
    .unwrap();
    let old = std::fs::read(&path).unwrap();
    let held = std::fs::OpenOptions::new()
        .read(true)
        .share_mode(1)
        .open(&path)
        .unwrap();
    vault
        .payload_mut()
        .unwrap()
        .rename("synthetic-next")
        .unwrap();
    assert_eq!(vault.save(), Err(VaultError::AccessDenied));
    drop(held);
    assert_eq!(std::fs::read(&path).unwrap(), old);
    assert_eq!(std::fs::read_dir(dir.path()).unwrap().count(), 1);
}
