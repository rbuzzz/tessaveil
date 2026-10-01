#[derive(Debug, Clone, PartialEq, Eq)]
pub enum VaultError {
    InvalidHeader,
    UnsupportedVersion,
    KdfOutOfBounds,
    UnsupportedKdf,
    Truncated,
    TooLarge,
    Authentication,
    InvalidPassword,
    PasswordPolicy,
    AccessDenied,
    InsufficientSpace,
    Io,
    AlreadyExists,
    InvalidPath,
    UnsupportedFilesystem,
    Locked,
    UnsavedChanges,
    InvalidPayload,
    TemporaryRemains {
        cause: Box<VaultError>,
        path: Option<std::path::PathBuf>,
    },
}
impl std::fmt::Display for VaultError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.write_str(match self {
            Self::InvalidHeader=>"Invalid vault header.",
            Self::UnsupportedVersion=>"Unsupported vault or payload version.",
            Self::KdfOutOfBounds=>"KDF parameters are outside allowed bounds.",
            Self::UnsupportedKdf=>"Unsupported or too resource-intensive KDF profile.",
            Self::Truncated=>"The vault file is truncated.",
            Self::TooLarge=>"The vault exceeds the alpha size limits.",
            Self::Authentication=>"The password is incorrect or the vault is damaged.",
            Self::InvalidPassword=>"Password input contains NUL or exceeds the input limit.",
            Self::PasswordPolicy=>"Use at least 15 normalized characters and avoid common passwords and patterns.",
            Self::AccessDenied=>"Access denied or the file is in use.",
            Self::InsufficientSpace=>"Insufficient space to save the vault.",
            Self::Io=>"The vault could not be read or written.",
            Self::AlreadyExists=>"A vault already exists at this path.",
            Self::InvalidPath=>"Select a regular .tessaveil-alpha file.",
            Self::UnsupportedFilesystem=>"Saving requires an explicitly enabled development local NTFS target.",
            Self::Locked=>"The vault is locked.",
            Self::UnsavedChanges=>"Save or reopen the vault before making a backup.",
            Self::InvalidPayload=>"The requested vault data exceeds the alpha schema limits.",
            Self::TemporaryRemains{..}=>"Save failed; an encrypted temporary image remains. Comparing saved versions after password disclosure may reveal unchanged words.",
        })
    }
}
impl std::error::Error for VaultError {}
#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn errors_have_safe_actionable_categories() {
        assert_eq!(
            VaultError::Authentication.to_string(),
            "The password is incorrect or the vault is damaged."
        );
        let messages = [
            VaultError::InvalidHeader,
            VaultError::UnsupportedVersion,
            VaultError::KdfOutOfBounds,
            VaultError::UnsupportedKdf,
            VaultError::Truncated,
            VaultError::InsufficientSpace,
            VaultError::AccessDenied,
        ]
        .map(|e| e.to_string());
        for (i, m) in messages.iter().enumerate() {
            assert!(!m.is_empty());
            assert!(!messages[..i].contains(m));
        }
    }
}
