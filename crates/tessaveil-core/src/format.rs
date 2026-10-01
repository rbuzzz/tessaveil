use crate::{kdf::KdfParams, VaultError};
pub const MAGIC: &[u8; 8] = b"TSVALPHA";
pub const HEADER_LEN: usize = 140;
pub const MAX_PAYLOAD: usize = 8 * 1024 * 1024;
pub const MAX_FILE: usize = HEADER_LEN + MAX_PAYLOAD + 16;
pub struct Header {
    pub(crate) bytes: [u8; HEADER_LEN],
}
impl Header {
    pub fn parse(bytes: &[u8], file_len: u64) -> Result<Self, VaultError> {
        if file_len > MAX_FILE as u64 {
            return Err(VaultError::TooLarge);
        }
        let bytes: [u8; HEADER_LEN] = bytes
            .get(..HEADER_LEN)
            .ok_or(VaultError::Truncated)?
            .try_into()
            .map_err(|_| VaultError::Truncated)?;
        if &bytes[..8] != MAGIC {
            return Err(VaultError::InvalidHeader);
        }
        if bytes[8..10] != 2u16.to_le_bytes() {
            return Err(VaultError::UnsupportedVersion);
        }
        if bytes[10..12] != [1, 1] || bytes[40..64] == bytes[64..88] {
            return Err(VaultError::InvalidHeader);
        }
        let h = Self { bytes };
        h.params().validate()?;
        let len = h.ciphertext_len();
        if !(17..=MAX_PAYLOAD + 16).contains(&len) {
            return Err(VaultError::TooLarge);
        }
        let expected = (HEADER_LEN + len) as u64;
        if file_len < expected {
            return Err(VaultError::Truncated);
        }
        if file_len != expected {
            return Err(VaultError::InvalidHeader);
        }
        Ok(h)
    }
    pub(crate) fn params(&self) -> KdfParams {
        let number = |start| {
            u32::from_le_bytes(
                self.bytes[start..start + 4]
                    .try_into()
                    .expect("fixed header range"),
            )
        };
        KdfParams {
            memory_kib: number(12),
            iterations: number(16),
            parallelism: number(20),
        }
    }
    pub(crate) fn ciphertext_len(&self) -> usize {
        u32::from_le_bytes(self.bytes[88..92].try_into().expect("fixed header range")) as usize
    }
}
