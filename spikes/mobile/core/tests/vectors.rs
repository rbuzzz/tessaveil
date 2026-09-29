use tessaveil_mobile_probe::{normalize_password_utf8, probe_open_vault, Status};

mod support;

#[test]
fn rust_normalization_matches_shared_expected_bytes() {
    let document: serde_json::Value =
        serde_json::from_str(include_str!("../../vectors/password-normalization.json")).unwrap();
    for row in document["cases"].as_array().unwrap() {
        let input = support::unhex(row["input_utf8_hex"].as_str().unwrap());
        let actual = normalize_password_utf8(&input);
        if row.get("error").is_some() {
            assert_eq!(actual.unwrap_err(), Status::EmbeddedNul);
        } else {
            assert_eq!(
                &*actual.unwrap(),
                &support::unhex(row["nfc_utf8_hex"].as_str().unwrap()),
                "{}",
                row["id"]
            );
        }
    }
    assert_eq!(
        normalize_password_utf8(&[0xff]).unwrap_err(),
        Status::InvalidUtf8
    );
    assert_eq!(
        normalize_password_utf8(&vec![b'a'; 1025]).unwrap_err(),
        Status::PasswordTooLong
    );
}

#[test]
fn provisional_profile_authenticates_and_normalized_password_is_equivalent() {
    let image = support::fixture();
    assert_eq!(
        probe_open_vault(&image, support::PASSWORD.as_bytes()).status,
        Status::Success as u32
    );
    assert_eq!(
        probe_open_vault(&image, "SYNTHETIC-only-cafe\u{301}-🧪".as_bytes()).status,
        Status::Success as u32
    );
    assert_eq!(
        probe_open_vault(&image, b"SYNTHETIC-wrong-password").status,
        Status::AuthenticationFailed as u32
    );
    assert_eq!(
        probe_open_vault(&image, b"").status,
        Status::PasswordTooShort as u32
    );
    assert_eq!(
        probe_open_vault(&image, b"synthetic\0long-enough").status,
        Status::EmbeddedNul as u32
    );
}

#[test]
fn bounds_and_unsupported_profiles_precede_password_processing() {
    let base = support::header_only();
    for (offset, values) in [
        (12, vec![0, 65535, 262145, u32::MAX]),
        (16, vec![0, 2, 7, u32::MAX]),
        (20, vec![0, 9, u32::MAX]),
    ] {
        for value in values {
            let mut image = base.clone();
            image[offset..offset + 4].copy_from_slice(&value.to_le_bytes());
            assert_eq!(
                probe_open_vault(&image, &[0xff]).status,
                Status::KdfOutOfBounds as u32
            );
        }
    }
    for (offset, value) in [(24, 31u16), (24, 33), (26, 15), (26, 17)] {
        let mut image = base.clone();
        image[offset..offset + 2].copy_from_slice(&value.to_le_bytes());
        assert_eq!(
            probe_open_vault(&image, &[0xff]).status,
            Status::KdfOutOfBounds as u32
        );
    }
    // Both edges of every encoded range, except the single allowlisted tuple.
    for m in [65536u32, 262144] {
        for t in [3u32, 6] {
            for p in [1u32, 8] {
                let mut image = base.clone();
                for (offset, value) in [(12, m), (16, t), (20, p)] {
                    image[offset..offset + 4].copy_from_slice(&value.to_le_bytes());
                }
                assert_eq!(
                    probe_open_vault(&image, &[0xff]).status,
                    Status::UnsupportedProfile as u32
                );
            }
        }
    }
}

#[test]
fn authenticated_regions_detect_corruption() {
    let base = support::fixture();
    // Salt, each nonce, wrapped key body/tag, payload body/tag.
    for offset in [28, 44, 68, 96, 143, 144, base.len() - 1] {
        let mut image = base.clone();
        image[offset] ^= 1;
        assert_eq!(
            probe_open_vault(&image, support::PASSWORD.as_bytes()).status,
            Status::AuthenticationFailed as u32,
            "offset {offset}"
        );
    }
    let mut oversized = base.clone();
    oversized[92..96].copy_from_slice(&u32::MAX.to_le_bytes());
    assert_eq!(
        probe_open_vault(&oversized, &[0xff]).status,
        Status::InvalidEnvelope as u32
    );
    assert_eq!(
        probe_open_vault(&base[..143], &[0xff]).status,
        Status::InvalidEnvelope as u32
    );
    assert_eq!(
        probe_open_vault(&vec![0; 4097], &[0xff]).status,
        Status::InvalidEnvelope as u32
    );
    for (offset, expected) in [
        (0, Status::InvalidEnvelope),
        (8, Status::UnsupportedVersion),
        (10, Status::UnsupportedAlgorithm),
        (11, Status::UnsupportedAlgorithm),
    ] {
        let mut image = base.clone();
        image[offset] ^= 0x40;
        assert_eq!(probe_open_vault(&image, &[0xff]).status, expected as u32);
    }
}

#[test]
fn shared_binary_must_exist_and_match_before_claiming_interoperability() {
    let path =
        std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("../vectors/synthetic-vault-v0.bin");
    let committed = std::fs::read(path)
        .expect("BLOCKED: create and independently verify the shared synthetic fixture first");
    assert_eq!(committed, support::fixture());
    assert_eq!(
        probe_open_vault(&committed, support::PASSWORD.as_bytes()).status,
        Status::Success as u32
    );
}
