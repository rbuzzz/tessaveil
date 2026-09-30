//! Independent fixture oracle: no RustCrypto or shared construction helper imports.
//! SRU rust-argon2 and Orion perform the KDF and AEAD respectively.
use independent_argon2::{hash_raw, Config, ThreadMode, Variant, Version};
use orion::hazardous::aead::xchacha20poly1305::{open, Nonce, SecretKey};

fn configuration(memory_kib: u32) -> Config<'static> {
    Config {
        variant: Variant::Argon2id,
        version: Version::Version13,
        mem_cost: memory_kib,
        time_cost: 3,
        lanes: 4,
        hash_length: 32,
        thread_mode: ThreadMode::Sequential,
        secret: &[],
        ad: &[],
    }
}

#[test]
fn independent_argon2_matches_rfc9106_section_5_3() {
    // Public numeric known-answer vector, RFC 9106 (2021), section 5.3:
    // https://www.rfc-editor.org/rfc/rfc9106#section-5.3
    // 32 KiB belongs to this primitive KAT only, never the vault allowlist.
    let mut config = configuration(32);
    config.secret = &[3; 8];
    config.ad = &[4; 12];
    assert_eq!(
        hash_raw(&[1; 32], &[2; 16], &config).unwrap(),
        [
            0x0d, 0x64, 0x0d, 0xf5, 0x8d, 0x78, 0x76, 0x6c, 0x08, 0xc0, 0x37, 0xa3, 0x4a, 0x8b,
            0x53, 0xc9, 0xd0, 0x1e, 0xf0, 0x45, 0x2d, 0x75, 0xb6, 0x5e, 0xb5, 0x25, 0x20, 0xe9,
            0x6b, 0x01, 0xe6, 0x59
        ]
    );
}

#[test]
fn independently_open_committed_fixture_and_reject_corruption() {
    let path =
        std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("../vectors/synthetic-vault-v0.bin");
    let image = std::fs::read(path).expect("shared synthetic fixture required");
    // Independent literal layout checks, not the core's parser/builder.
    assert_eq!(image.len(), 172);
    assert_eq!(&image[..12], b"TVSPIKE0\0\0\x01\x01");
    assert_eq!(
        &image[12..28],
        &[0, 0, 1, 0, 3, 0, 0, 0, 4, 0, 0, 0, 32, 0, 16, 0]
    );
    assert_eq!(&image[92..96], &[28, 0, 0, 0]);
    let kek = hash_raw(
        "SYNTHETIC-only-café-🧪".as_bytes(),
        &image[28..44],
        &configuration(65536),
    )
    .unwrap();
    let wrapping_key = SecretKey::from_slice(&kek).unwrap();
    let wrap_nonce = Nonce::from_slice(&image[44..68]).unwrap();
    let mut dek = [0u8; 32];
    open(
        &wrapping_key,
        &wrap_nonce,
        &image[96..144],
        Some(&image[..96]),
        &mut dek,
    )
    .unwrap();
    assert_eq!(dek, [0xa5; 32]);
    let payload_key = SecretKey::from_slice(&dek).unwrap();
    let payload_nonce = Nonce::from_slice(&image[68..92]).unwrap();
    let mut plaintext = [0u8; 12];
    open(
        &payload_key,
        &payload_nonce,
        &image[144..],
        Some(&image[..144]),
        &mut plaintext,
    )
    .unwrap();
    assert_eq!(&plaintext, b"\xa1\x69synthetic\xf5");

    let mut damaged_wrap = image[96..144].to_vec();
    damaged_wrap[47] ^= 1;
    assert!(open(
        &wrapping_key,
        &wrap_nonce,
        &damaged_wrap,
        Some(&image[..96]),
        &mut dek
    )
    .is_err());
    let mut damaged_payload = image[144..].to_vec();
    damaged_payload[27] ^= 1;
    assert!(open(
        &payload_key,
        &payload_nonce,
        &damaged_payload,
        Some(&image[..144]),
        &mut plaintext
    )
    .is_err());
}
