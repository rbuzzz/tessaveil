//! Provisional, GUI-independent encrypted alpha vault. No release format promise.
//! Authenticated backup/restore preserve the existing ciphertext; password rotation
//! commits fresh encryption atomically under the same provisional schema.
pub mod catalog;
mod crypto;
pub mod error;
pub mod format;
pub mod kdf;
pub mod model;
pub mod session;
pub mod sheet;
pub mod spin;
mod store;
pub use error::VaultError;
pub use store::{CreateOptions, OpenVault, StoragePolicy, VaultService};
