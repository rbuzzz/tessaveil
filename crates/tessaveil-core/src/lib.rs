//! Provisional, GUI-independent encrypted alpha vault. No release format promise.
mod crypto;
pub mod error;
pub mod format;
pub mod kdf;
pub mod model;
pub mod session;
mod store;
pub use error::VaultError;
pub use store::{CreateOptions, OpenVault, StoragePolicy, VaultService};
