#![cfg(windows)]
use std::{fs, os::windows::fs::OpenOptionsExt, path::Path};
use tessaveil_core::{CreateOptions, OpenVault, StoragePolicy, VaultError, VaultService};

const PASSWORD: &str = "synthetic-recovery-password";
const REPLACEMENT: &str = "synthetic-replacement-password";
const STORAGE: StoragePolicy = StoragePolicy::DevelopmentLocalNtfs;
fn create(path: &Path) -> OpenVault {
    VaultService::create(
        path,
        PASSWORD,
        CreateOptions {
            name: "synthetic-saved".into(),
            storage: STORAGE,
            ..Default::default()
        },
    )
    .unwrap()
}

#[test]
fn backup_is_exact_authenticated_ciphertext_and_requires_semantic_cleanliness() {
    let dir = tempfile::tempdir().unwrap();
    let source = dir.path().join("source.tessaveil-alpha");
    let backup = dir.path().join("backup.tessaveil-alpha");
    let mut vault = create(&source);
    let original = fs::read(&source).unwrap();
    // Merely borrowing the editor is not a change.
    assert_eq!(vault.payload_mut().unwrap().name(), "synthetic-saved");
    vault.backup_to(&backup).unwrap();
    assert_eq!(fs::read(&backup).unwrap(), original);
    let unsaved = dir.path().join("unsaved.tessaveil-alpha");
    vault
        .payload_mut()
        .unwrap()
        .rename("synthetic-unsaved")
        .unwrap();
    assert_eq!(vault.backup_to(&unsaved), Err(VaultError::UnsavedChanges));
    assert!(!unsaved.exists());
    vault
        .payload_mut()
        .unwrap()
        .rename("synthetic-saved")
        .unwrap();
    vault.backup_to(&unsaved).unwrap();
    let mut other = VaultService::open(&source, PASSWORD).unwrap();
    other.set_storage_policy(STORAGE);
    other
        .payload_mut()
        .unwrap()
        .rename("synthetic-other-session")
        .unwrap();
    other.save().unwrap();
    let stale = dir.path().join("stale.tessaveil-alpha");
    assert_eq!(vault.backup_to(&stale), Err(VaultError::UnsavedChanges));
    assert!(!stale.exists());
}

#[test]
fn recovery_refuses_self_alias_existing_unsafe_and_readonly_destinations() {
    let dir = tempfile::tempdir().unwrap();
    let source = dir.path().join("source.tessaveil-alpha");
    let mut vault = create(&source);
    let original = fs::read(&source).unwrap();
    let alias = dir.path().join("hardlink.tessaveil-alpha");
    fs::hard_link(&source, &alias).unwrap();
    let existing = dir.path().join("existing.tessaveil-alpha");
    fs::write(&existing, b"synthetic-existing").unwrap();
    for path in [&source, &alias, &existing] {
        assert_eq!(vault.backup_to(path), Err(VaultError::AlreadyExists));
        assert!(matches!(
            VaultService::restore(&source, path, PASSWORD, STORAGE),
            Err(VaultError::AlreadyExists)
        ));
    }
    for name in [
        "source.tessaveil-alpha:stream.tessaveil-alpha",
        "bad.txt",
        "NUL.tessaveil-alpha",
        "NUL .tessaveil-alpha",
    ] {
        assert_eq!(
            vault.backup_to(dir.path().join(name)),
            Err(VaultError::InvalidPath)
        );
    }
    vault.set_storage_policy(StoragePolicy::ReadOnly);
    let denied = dir.path().join("denied.tessaveil-alpha");
    assert_eq!(
        vault.backup_to(&denied),
        Err(VaultError::UnsupportedFilesystem)
    );
    assert!(matches!(
        VaultService::restore(&source, &denied, PASSWORD, StoragePolicy::ReadOnly),
        Err(VaultError::UnsupportedFilesystem)
    ));
    assert!(!denied.exists());
    assert_eq!(fs::read(&source).unwrap(), original);
    assert_eq!(fs::read(&existing).unwrap(), b"synthetic-existing");
}

#[test]
fn restore_authenticates_before_destination_mutation_and_never_falls_back() {
    let dir = tempfile::tempdir().unwrap();
    let source = dir.path().join("source.tessaveil-alpha");
    let mut vault = create(&source);
    let original = fs::read(&source).unwrap();
    let restored = dir.path().join("restored.tessaveil-alpha");
    assert!(matches!(
        VaultService::restore(&source, &restored, "synthetic-wrong-password", STORAGE),
        Err(VaultError::Authentication)
    ));
    assert!(!restored.exists());
    let mut opened = VaultService::restore(&source, &restored, PASSWORD, STORAGE).unwrap();
    assert_eq!(opened.payload_mut().unwrap().name(), "synthetic-saved");
    assert_eq!(fs::read(&restored).unwrap(), original);
    for truncated in [false, true] {
        let mut damaged = original.clone();
        if truncated {
            damaged.truncate(50);
        } else {
            *damaged.last_mut().unwrap() ^= 1;
        }
        fs::write(&source, &damaged).unwrap();
        let target = dir.path().join("damage.tessaveil-alpha");
        assert!(VaultService::restore(&source, &target, PASSWORD, STORAGE).is_err());
        assert!(vault.backup_to(&target).is_err());
        assert!(!target.exists());
        assert_eq!(fs::read(&source).unwrap(), damaged);
        assert_eq!(fs::read(&restored).unwrap(), original);
    }
    assert_eq!(fs::read_dir(dir.path()).unwrap().count(), 2);
}

#[test]
fn source_sharing_denial_and_locked_session_cannot_create_backup() {
    let dir = tempfile::tempdir().unwrap();
    let source = dir.path().join("source.tessaveil-alpha");
    let destination = dir.path().join("copy.tessaveil-alpha");
    let mut vault = create(&source);
    let held = fs::OpenOptions::new()
        .read(true)
        .share_mode(0)
        .open(&source)
        .unwrap();
    assert_eq!(vault.backup_to(&destination), Err(VaultError::AccessDenied));
    assert!(matches!(
        VaultService::restore(&source, &destination, PASSWORD, STORAGE),
        Err(VaultError::AccessDenied)
    ));
    drop(held);
    vault.lock();
    assert_eq!(vault.backup_to(&destination), Err(VaultError::Locked));
    assert_eq!(
        vault.change_master_password(PASSWORD, REPLACEMENT),
        Err(VaultError::Locked)
    );
    assert!(!destination.exists());
}

#[test]
fn password_rotation_authenticates_current_and_preserves_unsaved_payload() {
    let dir = tempfile::tempdir().unwrap();
    let source = dir.path().join("source.tessaveil-alpha");
    let mut vault = create(&source);
    let original = fs::read(&source).unwrap();
    vault
        .payload_mut()
        .unwrap()
        .rename("synthetic-unsaved")
        .unwrap();
    assert_eq!(
        vault.change_master_password("synthetic-wrong-password", REPLACEMENT),
        Err(VaultError::Authentication)
    );
    assert_eq!(
        vault.change_master_password(PASSWORD, "short"),
        Err(VaultError::PasswordPolicy)
    );
    assert_eq!(fs::read(&source).unwrap(), original);
    vault.change_master_password(PASSWORD, REPLACEMENT).unwrap();
    let rotated = fs::read(&source).unwrap();
    for range in [24..40, 40..64, 64..88, 92..124] {
        assert_ne!(original[range.clone()], rotated[range]);
    }
    assert!(matches!(
        VaultService::open(&source, PASSWORD),
        Err(VaultError::Authentication)
    ));
    let mut reopened = VaultService::open(&source, REPLACEMENT).unwrap();
    assert_eq!(reopened.payload_mut().unwrap().name(), "synthetic-unsaved");
    vault.save().unwrap();
    VaultService::open(&source, REPLACEMENT).unwrap();
}

#[test]
fn failed_password_persistence_preserves_file_and_current_session() {
    let dir = tempfile::tempdir().unwrap();
    let source = dir.path().join("source.tessaveil-alpha");
    let mut vault = create(&source);
    let original = fs::read(&source).unwrap();
    let held = fs::OpenOptions::new()
        .read(true)
        .share_mode(1)
        .open(&source)
        .unwrap();
    assert_eq!(
        vault.change_master_password(PASSWORD, REPLACEMENT),
        Err(VaultError::AccessDenied)
    );
    drop(held);
    assert_eq!(fs::read(&source).unwrap(), original);
    vault.save().unwrap();
    VaultService::open(&source, PASSWORD).unwrap();
    assert_eq!(fs::read_dir(dir.path()).unwrap().count(), 1);
}
