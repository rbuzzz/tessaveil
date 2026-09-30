use crate::VaultError;
use unicode_normalization::UnicodeNormalization;
use zeroize::Zeroizing;
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct KdfParams {
    pub memory_kib: u32,
    pub iterations: u32,
    pub parallelism: u32,
}
impl Default for KdfParams {
    fn default() -> Self {
        Self {
            memory_kib: 65536,
            iterations: 3,
            parallelism: 4,
        }
    }
}
impl KdfParams {
    pub fn validate(self) -> Result<(), VaultError> {
        if !(65536..=262144).contains(&self.memory_kib)
            || !(3..=6).contains(&self.iterations)
            || !(1..=8).contains(&self.parallelism)
        {
            return Err(VaultError::KdfOutOfBounds);
        }
        if self != Self::default() {
            return Err(VaultError::UnsupportedKdf);
        }
        Ok(())
    }
}
pub fn normalize_password(password: &str) -> Result<Zeroizing<String>, VaultError> {
    if password.len() > 4096 || password.contains('\0') {
        return Err(VaultError::InvalidPassword);
    }
    let mut result = Zeroizing::new(String::new());
    for ch in password.nfc() {
        if result.len() + ch.len_utf8() > 4096 {
            return Err(VaultError::InvalidPassword);
        }
        result.push(ch);
    }
    Ok(result)
}
