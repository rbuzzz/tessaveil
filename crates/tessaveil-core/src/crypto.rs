use crate::{
    format::{Header, HEADER_LEN, MAGIC},
    kdf::{normalize_password, KdfParams},
};
use crate::{model::Payload, VaultError};
use argon2::{Algorithm, Argon2, Params, Version};
use chacha20poly1305::{
    aead::{AeadInPlace, KeyInit},
    Tag, XChaCha20Poly1305, XNonce,
};
use zeroize::Zeroizing;
pub(crate) struct Secrets {
    pub(crate) kek: Zeroizing<[u8; 32]>,
    pub(crate) dek: Zeroizing<[u8; 32]>,
}
fn random(bytes: &mut [u8]) -> Result<(), VaultError> {
    getrandom::getrandom(bytes).map_err(|_| VaultError::Io)
}
pub(crate) fn derive(password: &str, salt: &[u8]) -> Result<Zeroizing<[u8; 32]>, VaultError> {
    let password = normalize_password(password)?;
    let params = Params::new(65536, 3, 4, Some(32)).map_err(|_| VaultError::UnsupportedKdf)?;
    let mut key = Zeroizing::new([0; 32]);
    // Use explicit zeroizing workspace: the convenience hash API does not erase its allocation.
    let mut memory = Zeroizing::new(vec![argon2::Block::default(); 65536]);
    Argon2::new(Algorithm::Argon2id, Version::V0x13, params)
        .hash_password_into_with_memory(password.as_bytes(), salt, &mut *key, &mut *memory)
        .map_err(|_| VaultError::Io)?;
    Ok(key)
}
pub(crate) fn create(password: &str, payload: &Payload) -> Result<(Vec<u8>, Secrets), VaultError> {
    let normalized = normalize_password(password)?;
    let chars = normalized.chars().count();
    let common = [
        "passwordpassword",
        "123456789012345",
        "qwertyuiopasdfgh",
        "letmeinletmeinletmein",
    ];
    if chars < 15
        || normalized.chars().all(|c| normalized.starts_with(c))
        || common
            .iter()
            .any(|candidate| normalized.eq_ignore_ascii_case(candidate))
    {
        return Err(VaultError::PasswordPolicy);
    }
    let mut salt = [0; 16];
    random(&mut salt)?;
    let mut secrets = Secrets {
        kek: derive(&normalized, &salt)?,
        dek: Zeroizing::new([0; 32]),
    };
    random(&mut *secrets.dek)?;
    let image = seal(payload, &secrets, &salt)?;
    Ok((image, secrets))
}
pub(crate) fn open(image: &[u8], password: &str) -> Result<(Payload, Secrets), VaultError> {
    let h = Header::parse(image, image.len() as u64)?;
    let kek = derive(password, &h.bytes[24..40])?;
    decrypt(image, kek)
}
fn decrypt(image: &[u8], kek: Zeroizing<[u8; 32]>) -> Result<(Payload, Secrets), VaultError> {
    let h = Header::parse(image, image.len() as u64)?;
    let mut dek = Zeroizing::new([0; 32]);
    dek.copy_from_slice(&h.bytes[92..124]);
    XChaCha20Poly1305::new((&*kek).into())
        .decrypt_in_place_detached(
            XNonce::from_slice(&h.bytes[40..64]),
            &h.bytes[..92],
            &mut *dek,
            Tag::from_slice(&h.bytes[124..140]),
        )
        .map_err(|_| VaultError::Authentication)?;
    let body = &image[HEADER_LEN..];
    let mut plain = Zeroizing::new(body[..body.len() - 16].to_vec());
    XChaCha20Poly1305::new((&*dek).into())
        .decrypt_in_place_detached(
            XNonce::from_slice(&h.bytes[64..88]),
            &h.bytes,
            &mut plain,
            Tag::from_slice(&body[body.len() - 16..]),
        )
        .map_err(|_| VaultError::Authentication)?;
    let payload = Payload::decode(&plain).map_err(|e| match e {
        VaultError::UnsupportedVersion => e,
        _ => VaultError::Authentication,
    })?;
    Ok((payload, Secrets { kek, dek }))
}
pub(crate) fn verify(image: &[u8], secrets: &Secrets) -> Result<(), VaultError> {
    decrypt(image, Zeroizing::new(*secrets.kek)).map(|_| ())
}
pub(crate) fn seal(
    payload: &Payload,
    secrets: &Secrets,
    salt: &[u8],
) -> Result<Vec<u8>, VaultError> {
    let mut plain = payload.encode()?;
    let mut h = [0; HEADER_LEN];
    h[..8].copy_from_slice(MAGIC);
    h[8..10].copy_from_slice(&2u16.to_le_bytes());
    h[10..12].copy_from_slice(&[1, 1]);
    let p = KdfParams::default();
    for (i, n) in [(12, p.memory_kib), (16, p.iterations), (20, p.parallelism)] {
        h[i..i + 4].copy_from_slice(&n.to_le_bytes());
    }
    h[24..40].copy_from_slice(salt);
    random(&mut h[40..88])?;
    // Fail closed on the astronomically unlikely equal-nonce draw; never reuse it.
    if h[40..64] == h[64..88] {
        return Err(VaultError::Io);
    }
    h[88..92].copy_from_slice(&((plain.len() + 16) as u32).to_le_bytes());
    let mut wrapped = Zeroizing::new(*secrets.dek);
    let tag = XChaCha20Poly1305::new((&*secrets.kek).into())
        .encrypt_in_place_detached(XNonce::from_slice(&h[40..64]), &h[..92], &mut *wrapped)
        .map_err(|_| VaultError::Io)?;
    h[92..124].copy_from_slice(&*wrapped);
    h[124..140].copy_from_slice(&tag);
    let tag = XChaCha20Poly1305::new((&*secrets.dek).into())
        .encrypt_in_place_detached(XNonce::from_slice(&h[64..88]), &h, &mut plain)
        .map_err(|_| VaultError::Io)?;
    let mut image = Vec::with_capacity(HEADER_LEN + plain.len() + 16);
    image.extend_from_slice(&h);
    image.extend_from_slice(&plain);
    image.extend_from_slice(&tag);
    Ok(image)
}
#[cfg(test)]
mod tests {
    use super::*;
    use crate::format::HEADER_LEN;
    const PASSWORD: &str = "synthetic-password-🦀-e\u{301}";
    #[test]
    fn retained_keys_use_zeroizing_owners() {
        use zeroize::Zeroize;
        let mut s = Secrets {
            kek: Zeroizing::new([7; 32]),
            dek: Zeroizing::new([9; 32]),
        };
        s.kek.zeroize();
        s.dek.zeroize();
        assert_eq!(*s.kek, [0; 32]);
        assert_eq!(*s.dek, [0; 32]);
        assert!(std::mem::needs_drop::<Secrets>());
    }
    #[test]
    fn authenticated_bad_payload_is_authentication_but_unknown_schema_is_version_error() {
        let (image, secrets) = create(PASSWORD, &Payload::default()).unwrap();
        for (bytes, expected) in [
            (
                vec![0x85, 3, 0x60, 0x60, 0x80, 0],
                VaultError::UnsupportedVersion,
            ),
            (vec![0x81, 3], VaultError::UnsupportedVersion),
            (
                vec![0x85, 2, 0x60, 0x60, 0x80, 0],
                VaultError::Authentication,
            ),
            (vec![0x80, 2], VaultError::Authentication),
            (
                vec![0x98, 5, 2, 0x60, 0x60, 0x80, 0],
                VaultError::Authentication,
            ),
            (
                vec![0x84, 3, 0x60, 0x60, 0x80],
                VaultError::UnsupportedVersion,
            ),
            (vec![0x84, 2, 0x61, 0xff, 0x80], VaultError::Authentication),
            (vec![0x85, 2, 0x60, 0x60, 0x80], VaultError::Authentication),
        ] {
            let mut h = image[..HEADER_LEN].to_vec();
            h[88..92].copy_from_slice(&((bytes.len() + 16) as u32).to_le_bytes());
            let mut wrapped = *secrets.dek;
            let tag = XChaCha20Poly1305::new((&*secrets.kek).into())
                .encrypt_in_place_detached(XNonce::from_slice(&h[40..64]), &h[..92], &mut wrapped)
                .unwrap();
            h[92..124].copy_from_slice(&wrapped);
            h[124..140].copy_from_slice(&tag);
            let mut encrypted = bytes;
            let tag = XChaCha20Poly1305::new((&*secrets.dek).into())
                .encrypt_in_place_detached(XNonce::from_slice(&h[64..88]), &h, &mut encrypted)
                .unwrap();
            h.extend_from_slice(&encrypted);
            h.extend_from_slice(&tag);
            assert!(matches!(decrypt(&h,Zeroizing::new(*secrets.kek)),Err(e) if e==expected));
        }
    }
    #[test]
    fn envelope_roundtrip_nfc_randomness_and_authentication() {
        let mut p = Payload::default();
        p.rename("synthetic-encrypted-marker").unwrap();
        let (image, secrets) = create(PASSWORD, &p).unwrap();
        assert_eq!(&image[..8], b"TSVALPHA");
        assert_ne!(&image[40..64], &image[64..88]);
        assert!(!image
            .windows(26)
            .any(|w| w == b"synthetic-encrypted-marker"));
        let (opened, _) = open(&image, "synthetic-password-🦀-é").unwrap();
        assert_eq!(opened.name(), p.name());
        assert!(matches!(
            open(&image, "synthetic-wrong-password"),
            Err(VaultError::Authentication)
        ));
        let second = seal(&p, &secrets, &image[24..40]).unwrap();
        assert_ne!(image[40..88], second[40..88]);
        // Every non-structural header byte and every ciphertext byte must authenticate.
        for i in 24..image.len() {
            if (88..92).contains(&i) {
                continue;
            }
            let mut bad = image.clone();
            bad[i] ^= 0x80;
            let result = open_with_secrets_for_test(&bad, &secrets).map(|_| ());
            assert_eq!(result, Err(VaultError::Authentication), "byte {i}");
        }
        assert!(image.len() > HEADER_LEN);
    }
    fn open_with_secrets_for_test(image: &[u8], secrets: &Secrets) -> Result<Payload, VaultError> {
        decrypt(image, Zeroizing::new(*secrets.kek)).map(|(p, _)| p)
    }
    #[test]
    fn password_policy_rejects_short_and_bundled_common_patterns() {
        for pw in [
            "short",
            "passwordpassword",
            "PASSWORDpassword",
            "123456789012345",
            "aaaaaaaaaaaaaaa",
        ] {
            assert!(matches!(
                create(pw, &Payload::default()),
                Err(VaultError::PasswordPolicy)
            ));
        }
    }
}
