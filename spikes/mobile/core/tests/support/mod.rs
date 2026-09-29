//! Synthetic test construction, not a known-answer or independent crypto oracle.
use argon2::{Algorithm, Argon2, Params, Version};
use chacha20poly1305::{aead::{Aead, KeyInit, Payload}, XChaCha20Poly1305, XNonce};

pub const PASSWORD: &str = "SYNTHETIC-only-café-🧪";

pub fn unhex(value: &str) -> Vec<u8> {
    assert_eq!(value.len() % 2, 0);
    (0..value.len()).step_by(2).map(|i| u8::from_str_radix(&value[i..i + 2], 16).unwrap()).collect()
}

pub fn header_only() -> Vec<u8> {
    let mut image = vec![0; 160];
    image[..8].copy_from_slice(b"TVSPIKE0");
    image[10..12].copy_from_slice(&[1, 1]);
    for (offset, value) in [(12, 65536u32), (16, 3), (20, 4), (92, 16)] {
        image[offset..offset + 4].copy_from_slice(&value.to_le_bytes());
    }
    image[24..28].copy_from_slice(&[32, 0, 16, 0]);
    image
}

pub fn fixture() -> Vec<u8> {
    let plaintext = b"\xa1\x69synthetic\xf5";
    let mut prefix = header_only()[..96].to_vec();
    // PUBLIC deterministic synthetic inputs only. Never a production RNG or key.
    for (i, byte) in prefix[28..92].iter_mut().enumerate() { *byte = i as u8; }
    prefix[92..96].copy_from_slice(&((plaintext.len() + 16) as u32).to_le_bytes());
    let mut kek = [0u8; 32];
    Argon2::new(Algorithm::Argon2id, Version::V0x13, Params::new(65536, 3, 4, Some(32)).unwrap())
        .hash_password_into(PASSWORD.as_bytes(), &prefix[28..44], &mut kek).unwrap();
    let dek = [0xa5u8; 32];
    let wrapped = XChaCha20Poly1305::new_from_slice(&kek).unwrap()
        .encrypt(XNonce::from_slice(&prefix[44..68]), Payload { msg: &dek, aad: &prefix }).unwrap();
    let mut header = prefix;
    header.extend_from_slice(&wrapped);
    let ciphertext = XChaCha20Poly1305::new_from_slice(&dek).unwrap()
        .encrypt(XNonce::from_slice(&header[68..92]), Payload { msg: plaintext, aad: &header }).unwrap();
    header.extend_from_slice(&ciphertext);
    header
}
