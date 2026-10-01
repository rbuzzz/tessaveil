#![cfg(windows)]

use sha2::{Digest, Sha256};
use std::path::Path;
use tessaveil_core::{StoragePolicy, VaultError, VaultService};

const PASSWORD_DECOMPOSED: &str = "TSVALPHA public e\u{301} 🦀 password";
const PASSWORD_COMPOSED: &str = "TSVALPHA public é 🦀 password";
const FIXTURE_HEX: &str = include_str!("fixtures/tsvalpha-schema2.hex");
const FIXTURE_SHA256: &str = "0298259eccd7ecb9d4ca47383f93d0982a00c1e0ae1b9bd850ca8b89935edf25";

fn decode_fixture() -> Vec<u8> {
    let compact: String = FIXTURE_HEX
        .chars()
        .filter(|ch| !ch.is_whitespace())
        .collect();
    assert_eq!(compact.len() % 2, 0);
    compact
        .as_bytes()
        .chunks_exact(2)
        .map(|pair| u8::from_str_radix(std::str::from_utf8(pair).unwrap(), 16).unwrap())
        .collect()
}

fn write(path: &Path, bytes: &[u8]) {
    std::fs::write(path, bytes).unwrap();
}

#[test]
fn independent_schema_two_fixture_has_fixed_identity_and_unicode_password_contract() {
    let image = decode_fixture();
    assert_eq!(format!("{:x}", Sha256::digest(&image)), FIXTURE_SHA256);
    assert_eq!(&image[..8], b"TSVALPHA");
    assert_eq!(&image[8..10], &2u16.to_le_bytes());

    let dir = tempfile::tempdir().unwrap();
    let path = dir.path().join("public-fixture.tessaveil-alpha");
    write(&path, &image);
    for password in [PASSWORD_DECOMPOSED, PASSWORD_COMPOSED] {
        let mut vault = VaultService::open(&path, password).unwrap();
        vault.set_storage_policy(StoragePolicy::DevelopmentLocalNtfs);
        let editor = vault.payload_mut().unwrap();
        assert_eq!(editor.name(), "public-tsvalpha-fixture");
        assert_eq!(editor.locale(), "en");
    }
    assert!(matches!(
        VaultService::open(&path, "TSVALPHA public e\0 🦀 password"),
        Err(VaultError::InvalidPassword)
    ));
    assert!(matches!(
        VaultService::open(&path, "synthetic-wrong-password"),
        Err(VaultError::Authentication)
    ));
}

#[test]
fn every_schema_two_envelope_region_truncation_and_trailing_byte_fail_closed() {
    let original = decode_fixture();
    let dir = tempfile::tempdir().unwrap();
    let path = dir.path().join("mutated.tessaveil-alpha");

    for length in 0..original.len() {
        write(&path, &original[..length]);
        assert!(
            matches!(
                VaultService::open(&path, PASSWORD_COMPOSED),
                Err(VaultError::Truncated)
            ),
            "truncation {length}"
        );
    }
    let mut trailing = original.clone();
    trailing.push(0);
    write(&path, &trailing);
    assert!(matches!(
        VaultService::open(&path, PASSWORD_COMPOSED),
        Err(VaultError::InvalidHeader)
    ));

    let mut mutations = vec![
        ("magic", 0usize, None, VaultError::InvalidHeader),
        ("version", 8, None, VaultError::UnsupportedVersion),
        ("kdf-id", 10, None, VaultError::InvalidHeader),
        ("aead-id", 11, None, VaultError::InvalidHeader),
        ("kdf-memory", 12, None, VaultError::UnsupportedKdf),
        ("salt", 24, None, VaultError::Authentication),
        ("wrap-nonce", 40, None, VaultError::Authentication),
        ("payload-nonce", 64, None, VaultError::Authentication),
        ("wrapped-dek", 92, None, VaultError::Authentication),
        ("wrap-tag", 124, None, VaultError::Authentication),
        ("body", 140, None, VaultError::Authentication),
        (
            "payload-tag",
            original.len() - 1,
            None,
            VaultError::Authentication,
        ),
    ];
    let payload_length = u32::from_le_bytes(original[88..92].try_into().unwrap());
    mutations.push((
        "ciphertext-length",
        88,
        Some((payload_length + 1).to_le_bytes()),
        VaultError::Truncated,
    ));
    for (label, index, replacement, expected) in mutations {
        let mut mutated = original.clone();
        if let Some(bytes) = replacement {
            mutated[index..index + 4].copy_from_slice(&bytes);
        } else {
            mutated[index] ^= 1;
        }
        write(&path, &mutated);
        assert!(
            matches!(VaultService::open(&path, PASSWORD_COMPOSED), Err(error) if error == expected),
            "region {label}"
        );
    }

    write(&path, &original);
    let mut opened = VaultService::open(&path, PASSWORD_COMPOSED).unwrap();
    assert_eq!(
        opened.payload_mut().unwrap().name(),
        "public-tsvalpha-fixture"
    );
}

#[test]
fn actual_open_rejects_every_kdf_boundary_before_invalid_password_processing() {
    let original = decode_fixture();
    let dir = tempfile::tempdir().unwrap();
    let path = dir.path().join("kdf-matrix.tessaveil-alpha");
    let cases = [
        (12usize, 65535u32, VaultError::KdfOutOfBounds),
        (12, 65536, VaultError::InvalidPassword),
        (12, 262144, VaultError::UnsupportedKdf),
        (12, 262145, VaultError::KdfOutOfBounds),
        (16, 2, VaultError::KdfOutOfBounds),
        (16, 3, VaultError::InvalidPassword),
        (16, 6, VaultError::UnsupportedKdf),
        (16, 7, VaultError::KdfOutOfBounds),
        (20, 0, VaultError::KdfOutOfBounds),
        (20, 1, VaultError::UnsupportedKdf),
        (20, 8, VaultError::UnsupportedKdf),
        (20, 9, VaultError::KdfOutOfBounds),
    ];
    for (offset, value, expected) in cases {
        let mut image = original.clone();
        image[offset..offset + 4].copy_from_slice(&value.to_le_bytes());
        write(&path, &image);
        assert!(
            matches!(VaultService::open(&path, "invalid\0password"), Err(error) if error == expected),
            "offset {offset} value {value}"
        );
    }
}
