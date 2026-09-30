use tessaveil_core::{
    format::{Header, HEADER_LEN, MAX_FILE},
    kdf::{normalize_password, KdfParams},
    VaultError,
};
fn header() -> [u8; HEADER_LEN] {
    let mut h = [0; HEADER_LEN];
    h[..8].copy_from_slice(b"TSVALPHA");
    h[8..10].copy_from_slice(&1u16.to_le_bytes());
    h[10] = 1;
    h[11] = 1;
    h[12..16].copy_from_slice(&65536u32.to_le_bytes());
    h[16..20].copy_from_slice(&3u32.to_le_bytes());
    h[20..24].copy_from_slice(&4u32.to_le_bytes());
    h[64] = 1;
    h[88..92].copy_from_slice(&17u32.to_le_bytes());
    h
}
#[test]
fn header_lengths_magic_version_algorithms_and_nonces_are_checked() {
    let h = header();
    assert!(Header::parse(&h, 157).is_ok());
    for n in 0..HEADER_LEN {
        assert!(matches!(
            Header::parse(&h[..n], n as u64),
            Err(VaultError::Truncated)
        ));
    }
    for (index, value, expected) in [
        (0, 0, VaultError::InvalidHeader),
        (8, 2, VaultError::UnsupportedVersion),
        (10, 2, VaultError::InvalidHeader),
        (11, 2, VaultError::InvalidHeader),
        (64, 0, VaultError::InvalidHeader),
    ] {
        let mut bad = h;
        bad[index] = value;
        assert!(matches!(Header::parse(&bad, 157), Err(e) if e == expected));
    }
    assert!(matches!(Header::parse(&h, 156), Err(VaultError::Truncated)));
    assert!(matches!(
        Header::parse(&h, 158),
        Err(VaultError::InvalidHeader)
    ));
    assert!(matches!(
        Header::parse(&h, MAX_FILE as u64 + 1),
        Err(VaultError::TooLarge)
    ));
}
#[test]
fn kdf_bounds_and_allowlist_reject_without_deriving() {
    assert_eq!(KdfParams::default().validate(), Ok(()));
    for p in [
        KdfParams {
            memory_kib: 65535,
            ..Default::default()
        },
        KdfParams {
            memory_kib: 262145,
            ..Default::default()
        },
        KdfParams {
            iterations: 2,
            ..Default::default()
        },
        KdfParams {
            iterations: 7,
            ..Default::default()
        },
        KdfParams {
            parallelism: 0,
            ..Default::default()
        },
        KdfParams {
            parallelism: 9,
            ..Default::default()
        },
    ] {
        assert_eq!(p.validate(), Err(VaultError::KdfOutOfBounds));
    }
    assert_eq!(
        KdfParams {
            memory_kib: 262144,
            iterations: 6,
            parallelism: 8
        }
        .validate(),
        Err(VaultError::UnsupportedKdf)
    );
}
#[test]
fn passwords_use_nfc_explicit_unicode_without_nul() {
    assert_eq!(
        normalize_password("synthetic-e\u{301}-🦀-password")
            .unwrap()
            .as_bytes(),
        "synthetic-é-🦀-password".as_bytes()
    );
    assert_eq!(
        normalize_password("\u{212b}\u{301}").unwrap().as_bytes(),
        "Ǻ".as_bytes()
    );
    assert!(matches!(
        normalize_password("synthetic\0password"),
        Err(VaultError::InvalidPassword)
    ));
    assert!(matches!(
        normalize_password(&"x".repeat(4097)),
        Err(VaultError::InvalidPassword)
    ));
    assert_eq!(normalize_password(&"x".repeat(64)).unwrap().len(), 64);
}
