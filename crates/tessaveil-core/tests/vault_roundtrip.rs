#![cfg(windows)]
use std::time::{Duration, Instant};
use tessaveil_core::{CreateOptions, StoragePolicy, VaultError, VaultService};
#[test]
fn create_reopen_save_and_lock_have_no_plaintext_disk_copy() {
    let dir = tempfile::tempdir().unwrap();
    let path = dir.path().join("synthetic.tessaveil-alpha");
    let mut v = VaultService::create(
        &path,
        "synthetic-password-🦀",
        CreateOptions {
            name: "synthetic-original".into(),
            storage: StoragePolicy::DevelopmentLocalNtfs,
            ..Default::default()
        },
    )
    .unwrap();
    let original = std::fs::read(&path).unwrap();
    assert!(!original.windows(18).any(|w| w == b"synthetic-original"));
    assert!(matches!(
        VaultService::create(&path, "synthetic-password-🦀", CreateOptions::default()),
        Err(VaultError::AlreadyExists)
    ));
    v.payload_mut()
        .unwrap()
        .rename("synthetic-revised")
        .unwrap();
    v.save().unwrap();
    assert_ne!(original, std::fs::read(&path).unwrap());
    let mut opened = VaultService::open(&path, "synthetic-password-🦀").unwrap();
    assert_eq!(opened.payload_mut().unwrap().name(), "synthetic-revised");
    assert_eq!(opened.save(), Err(VaultError::UnsupportedFilesystem));
    opened.lock();
    assert!(opened.is_locked());
    assert!(matches!(opened.payload_mut(), Err(VaultError::Locked)));
    assert_eq!(opened.save(), Err(VaultError::Locked));
    let old = v.timeout_token();
    let now = Instant::now();
    let token = v.activity(now).unwrap();
    assert!(!v.expire(old, now + Duration::from_secs(301)));
    assert!(v.expire(token, now + Duration::from_secs(300)));
    assert!(v.is_locked());
    assert_eq!(std::fs::read_dir(dir.path()).unwrap().count(), 1);
}
#[test]
fn extension_and_missing_access_errors_are_distinct() {
    let dir = tempfile::tempdir().unwrap();
    assert!(matches!(
        VaultService::create(
            dir.path().join("release.tessaveil"),
            "synthetic-password",
            CreateOptions::default()
        ),
        Err(VaultError::InvalidPath)
    ));
    assert!(matches!(
        VaultService::open(
            dir.path().join("missing.tessaveil-alpha"),
            "synthetic-password"
        ),
        Err(VaultError::Io)
    ));
}
