#![cfg(windows)]
use tessaveil_core::{format::MAX_FILE, CreateOptions, StoragePolicy, VaultError, VaultService};
#[test]
fn every_truncation_and_structural_region_fails_before_password_processing() {
    let dir = tempfile::tempdir().unwrap();
    let source = dir.path().join("source.tessaveil-alpha");
    VaultService::create(
        &source,
        "synthetic-test-password",
        CreateOptions {
            storage: StoragePolicy::DevelopmentLocalNtfs,
            ..Default::default()
        },
    )
    .unwrap();
    let image = std::fs::read(source).unwrap();
    let path = dir.path().join("broken.tessaveil-alpha");
    for n in 0..image.len() {
        std::fs::write(&path, &image[..n]).unwrap();
        assert!(
            matches!(VaultService::open(&path, "\0"), Err(VaultError::Truncated)),
            "boundary {n}"
        );
    }
    for (index, value, expected) in [
        (0, 0, VaultError::InvalidHeader),
        (8, 1, VaultError::UnsupportedVersion),
        (10, 2, VaultError::InvalidHeader),
        (11, 2, VaultError::InvalidHeader),
        (15, 0xff, VaultError::KdfOutOfBounds),
        (16, 4, VaultError::UnsupportedKdf),
        (20, 9, VaultError::KdfOutOfBounds),
        (91, 0xff, VaultError::TooLarge),
    ] {
        let mut bad = image.clone();
        bad[index] = value;
        std::fs::write(&path, bad).unwrap();
        assert!(
            matches!(VaultService::open(&path,"\0"),Err(e) if e==expected),
            "byte {index}"
        );
    }
    std::fs::File::create(&path)
        .unwrap()
        .set_len(MAX_FILE as u64 + 1)
        .unwrap();
    assert!(matches!(
        VaultService::open(&path, "\0"),
        Err(VaultError::TooLarge)
    ));
}
#[test]
fn actual_open_wrong_password_and_damaged_authenticated_regions_share_error() {
    let dir = tempfile::tempdir().unwrap();
    let path = dir.path().join("synthetic.tessaveil-alpha");
    VaultService::create(
        &path,
        "synthetic-test-password",
        CreateOptions {
            storage: StoragePolicy::DevelopmentLocalNtfs,
            ..Default::default()
        },
    )
    .unwrap();
    let original = std::fs::read(&path).unwrap();
    assert!(matches!(
        VaultService::open(&path, "synthetic-wrong-password"),
        Err(VaultError::Authentication)
    ));
    for i in [24, 40, 64, 92, 124, 140, original.len() - 1] {
        let mut bad = original.clone();
        bad[i] ^= 1;
        std::fs::write(&path, bad).unwrap();
        assert!(
            matches!(
                VaultService::open(&path, "synthetic-test-password"),
                Err(VaultError::Authentication)
            ),
            "byte {i}"
        );
    }
}
