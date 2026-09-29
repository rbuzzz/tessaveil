//! Disposable probe only. Never use this deterministic synthetic envelope for funds.
use argon2::{Algorithm, Argon2, Params, Version};
use chacha20poly1305::{aead::{Aead, KeyInit, Payload}, XChaCha20Poly1305, XNonce};
use std::time::Instant;
use unicode_normalization::UnicodeNormalization;
use zeroize::Zeroizing;

const MAX_FILE: usize = 4096;
const MAX_PASSWORD: usize = 1024;
const PREFIX: usize = 96;
const HEADER: usize = 144;
const SYNTHETIC_CBOR: &[u8] = b"\xa1\x69synthetic\xf5";

#[repr(u32)]
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Status {
    Success = 0,
    InvalidEnvelope = 1,
    UnsupportedVersion = 2,
    UnsupportedAlgorithm = 3,
    KdfOutOfBounds = 4,
    UnsupportedProfile = 5,
    InvalidUtf8 = 6,
    EmbeddedNul = 7,
    PasswordTooLong = 8,
    PasswordTooShort = 9,
    AuthenticationFailed = 10,
    UnsupportedPayload = 11,
    InternalError = 12,
    InvalidArgument = 13,
}

/// No password, normalized bytes, keys, or plaintext cross the mobile return boundary.
/// memory_bytes is u64::MAX = unmeasured (not zero and not encoded Argon memory).
#[repr(C)]
#[derive(Clone, Copy)]
pub struct ProbeResult {
    pub status: u32,
    pub reserved: u32,
    pub duration_us: u64,
    pub memory_bytes: u64,
}

impl ProbeResult {
    fn error(status: Status) -> Self {
        Self { status: status as u32, reserved: 0, duration_us: 0, memory_bytes: u64::MAX }
    }
}

pub fn normalize_password_utf8(input: &[u8]) -> Result<Zeroizing<Vec<u8>>, Status> {
    if input.len() > MAX_PASSWORD { return Err(Status::PasswordTooLong); }
    let text = std::str::from_utf8(input).map_err(|_| Status::InvalidUtf8)?;
    if text.contains('\0') { return Err(Status::EmbeddedNul); }
    let normalized = Zeroizing::new(text.nfc().collect::<String>());
    if normalized.len() > MAX_PASSWORD { return Err(Status::PasswordTooLong); }
    Ok(Zeroizing::new(normalized.as_bytes().to_vec()))
}

fn u32_at(bytes: &[u8], offset: usize) -> u32 {
    u32::from_le_bytes(bytes[offset..offset + 4].try_into().unwrap())
}

/// All header validation is borrowed/no-heap; called before password decoding or KDF.
fn validate_header(bytes: &[u8]) -> Result<(), Status> {
    if bytes.len() < HEADER + 16 || bytes.len() > MAX_FILE || &bytes[..8] != b"TVSPIKE0" {
        return Err(Status::InvalidEnvelope);
    }
    if bytes[8..10] != [0, 0] { return Err(Status::UnsupportedVersion); }
    if bytes[10..12] != [1, 1] { return Err(Status::UnsupportedAlgorithm); }
    let m = u32_at(bytes, 12);
    let t = u32_at(bytes, 16);
    let p = u32_at(bytes, 20);
    let output = u16::from_le_bytes(bytes[24..26].try_into().unwrap());
    let salt_len = u16::from_le_bytes(bytes[26..28].try_into().unwrap());
    if !(65536..=262144).contains(&m) || !(3..=6).contains(&t) || !(1..=8).contains(&p)
        || output != 32 || salt_len != 16 {
        return Err(Status::KdfOutOfBounds);
    }
    if (m, t, p) != (65536, 3, 4) { return Err(Status::UnsupportedProfile); }
    let ciphertext_len = u32_at(bytes, 92) as usize;
    if !(16..=MAX_FILE - HEADER).contains(&ciphertext_len) || bytes.len() - HEADER != ciphertext_len {
        return Err(Status::InvalidEnvelope);
    }
    Ok(())
}

#[cfg(test)]
thread_local! { static KDF_CALLS: std::cell::Cell<u32> = const { std::cell::Cell::new(0) }; }

fn open(bytes: &[u8], password_utf8: &[u8]) -> Result<(), Status> {
    validate_header(bytes)?;
    let password = normalize_password_utf8(password_utf8)?;
    // Open path uses this spike's provisional password policy; empty NFC is a
    // normalization vector only, never accepted as an unlock password.
    if std::str::from_utf8(&password).map_err(|_| Status::InvalidUtf8)?.chars().count() < 15 {
        return Err(Status::PasswordTooShort);
    }
    let params = Params::new(u32_at(bytes, 12), u32_at(bytes, 16), u32_at(bytes, 20), Some(32))
        .map_err(|_| Status::InternalError)?;
    let mut kek = Zeroizing::new([0u8; 32]);
    #[cfg(test)]
    KDF_CALLS.with(|n| n.set(n.get() + 1));
    Argon2::new(Algorithm::Argon2id, Version::V0x13, params)
        .hash_password_into(&password, &bytes[28..44], &mut *kek)
        .map_err(|_| Status::InternalError)?;
    let wrap = XChaCha20Poly1305::new_from_slice(&*kek).map_err(|_| Status::InternalError)?;
    let dek = Zeroizing::new(wrap.decrypt(XNonce::from_slice(&bytes[44..68]),
        Payload { msg: &bytes[PREFIX..HEADER], aad: &bytes[..PREFIX] })
        .map_err(|_| Status::AuthenticationFailed)?);
    if dek.len() != 32 { return Err(Status::AuthenticationFailed); }
    let payload_cipher = XChaCha20Poly1305::new_from_slice(&dek).map_err(|_| Status::InternalError)?;
    let payload = Zeroizing::new(payload_cipher.decrypt(XNonce::from_slice(&bytes[68..92]),
        Payload { msg: &bytes[HEADER..], aad: &bytes[..HEADER] })
        .map_err(|_| Status::AuthenticationFailed)?);
    // This fixed canonical-CBOR marker is the ONLY supported payload. No wallet,
    // table, mnemonic, user metadata or general-purpose product schema exists here.
    if payload.as_slice() != SYNTHETIC_CBOR { return Err(Status::UnsupportedPayload); }
    Ok(())
}

pub fn probe_open_vault(bytes: &[u8], password_utf8: &[u8]) -> ProbeResult {
    let started = Instant::now();
    let status = open(bytes, password_utf8).err().unwrap_or(Status::Success);
    ProbeResult { duration_us: started.elapsed().as_micros().min(u64::MAX as u128) as u64,
        ..ProbeResult::error(status) }
}

/// # Safety
/// Non-null inputs must point to readable memory for their exact lengths and stay
/// alive/unmodified until return. Null is accepted only with zero length. Caller
/// bounds are checked before slices are made; arbitrary invalid pointers are not safe.
#[no_mangle]
pub unsafe extern "C" fn tv_probe_open_vault(
    vault: *const u8, vault_len: usize, password: *const u8, password_len: usize,
) -> ProbeResult {
    if vault_len > MAX_FILE || password_len > MAX_PASSWORD
        || (vault.is_null() && vault_len != 0) || (password.is_null() && password_len != 0) {
        return ProbeResult::error(Status::InvalidArgument);
    }
    std::panic::catch_unwind(|| {
        let image = if vault_len == 0 { &[] } else { std::slice::from_raw_parts(vault, vault_len) };
        let input = if password_len == 0 { &[] } else { std::slice::from_raw_parts(password, password_len) };
        probe_open_vault(image, input)
    }).unwrap_or_else(|_| ProbeResult::error(Status::InternalError))
}

#[cfg(test)]
mod tests {
    use super::*;

    fn envelope(m: u32, t: u32, p: u32) -> Vec<u8> {
        let mut image = vec![0; 160];
        image[..8].copy_from_slice(b"TVSPIKE0");
        image[10..12].copy_from_slice(&[1, 1]);
        for (offset, value) in [(12, m), (16, t), (20, p), (92, 16)] {
            image[offset..offset + 4].copy_from_slice(&value.to_le_bytes());
        }
        image[24..28].copy_from_slice(&[32, 0, 16, 0]);
        image
    }

    #[test]
    fn rejected_profiles_never_invoke_kdf() {
        KDF_CALLS.with(|n| n.set(0));
        for (m, t, p, status) in [(65535, 3, 4, Status::KdfOutOfBounds),
            (262145, 3, 4, Status::KdfOutOfBounds), (65536, 7, 4, Status::KdfOutOfBounds),
            (65536, 3, 0, Status::KdfOutOfBounds), (262144, 6, 8, Status::UnsupportedProfile)] {
            assert_eq!(probe_open_vault(&envelope(m, t, p), &[0xff]).status, status as u32);
        }
        KDF_CALLS.with(|n| assert_eq!(n.get(), 0));
    }

    #[test]
    fn ffi_checks_null_and_lengths_without_dereferencing() {
        unsafe {
            assert_eq!(tv_probe_open_vault(std::ptr::null(), 1, std::ptr::null(), 0).status, Status::InvalidArgument as u32);
            assert_eq!(tv_probe_open_vault(std::ptr::null(), 0, std::ptr::null(), 0).status, Status::InvalidEnvelope as u32);
        }
    }
}
