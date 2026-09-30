//! Offline registry projected from validated source records. Never infer support
//! from a wallet name or a shared dictionary.
use crate::VaultError;
use serde_json::Value;
use sha2::{Digest, Sha256};
use std::sync::OnceLock;

const WORDLIST: &str =
    include_str!("../../../wordlists/bip39-en/3a10b5b5f0a7586df8928d580a3009744ebb2079.txt");

pub struct Profile {
    id: String,
    mode: String,
    name: String,
    reason: String,
    selectable: bool,
    lengths: Vec<usize>,
    dictionary_id: Option<String>,
}
impl Profile {
    pub fn id(&self) -> &str {
        &self.id
    }
    pub fn mode(&self) -> &str {
        &self.mode
    }
    pub fn name(&self) -> &str {
        &self.name
    }
    pub fn reason(&self) -> &str {
        &self.reason
    }
    pub fn selectable(&self) -> bool {
        self.selectable
    }
    pub fn supported_lengths(&self) -> &[usize] {
        &self.lengths
    }
    pub(crate) fn dictionary(&self) -> Result<Vec<String>, VaultError> {
        // This is a pinned data asset, not a second selectability allowlist.
        // Generator validation checks its bytes and provenance before publication.
        if !self.selectable || self.dictionary_id.as_deref() != Some("bip39-en") {
            return Err(VaultError::InvalidPayload);
        }
        Ok(WORDLIST.lines().map(str::to_owned).collect())
    }
    pub(crate) fn matches_dictionary(&self, snapshot: &[String]) -> bool {
        // load() has already bound this profile's dictionary ID and SHA-256 to
        // WORDLIST. Compare exact ordered content without allocating another copy.
        self.selectable
            && self.dictionary_id.as_deref() == Some("bip39-en")
            && snapshot.iter().map(String::as_str).eq(WORDLIST.lines())
    }
}

fn load() -> Result<Vec<Profile>, VaultError> {
    parse(include_str!("../../../generated/alpha/profile-matrix.json"))
}
fn parse(input: &str) -> Result<Vec<Profile>, VaultError> {
    let value: Value = serde_json::from_str(input).map_err(|_| VaultError::InvalidPayload)?;
    if value["schema_version"] != 1 {
        return Err(VaultError::InvalidPayload);
    }
    let mut profiles = Vec::new();
    let asset_hash = format!("{:x}", Sha256::digest(WORDLIST.as_bytes()));
    for v in value["profiles"]
        .as_array()
        .ok_or(VaultError::InvalidPayload)?
    {
        let text = |key: &str| {
            v[key]
                .as_str()
                .map(str::to_owned)
                .ok_or(VaultError::InvalidPayload)
        };
        let selected = v["selectable"]
            .as_bool()
            .ok_or(VaultError::InvalidPayload)?;
        let reason = text("reason")?;
        if selected != reason.is_empty() || reason.len() > 160 {
            return Err(VaultError::InvalidPayload);
        }
        // A regenerated matrix must never silently bind a profile to a stale
        // compiled word-list asset. This check only narrows the generated gate.
        if selected
            && (v["dictionaries"].as_array().is_none_or(|d| d.len() != 1)
                || v["dictionaries"][0]["id"] != "bip39-en"
                || v["dictionaries"][0]["sha256"] != asset_hash)
        {
            return Err(VaultError::InvalidPayload);
        }
        let lengths = v["supported_lengths"]
            .as_array()
            .ok_or(VaultError::InvalidPayload)?
            .iter()
            .map(|n| {
                n.as_u64()
                    .map(|n| n as usize)
                    .ok_or(VaultError::InvalidPayload)
            })
            .collect::<Result<Vec<_>, _>>()?;
        profiles.push(Profile {
            id: text("profile_id")?,
            mode: text("mode_id")?,
            name: v["display_name"]["en"]
                .as_str()
                .ok_or(VaultError::InvalidPayload)?
                .into(),
            reason,
            selectable: selected,
            lengths,
            dictionary_id: v["dictionaries"][0]["id"].as_str().map(str::to_owned),
        });
    }
    Ok(profiles)
}

pub fn profiles() -> Result<&'static [Profile], VaultError> {
    static PROFILES: OnceLock<Result<Vec<Profile>, VaultError>> = OnceLock::new();
    PROFILES
        .get_or_init(load)
        .as_ref()
        .map(Vec::as_slice)
        .map_err(|_| VaultError::InvalidPayload)
}
pub fn select(id: &str, mode: &str) -> Result<&'static Profile, VaultError> {
    profiles()?
        .iter()
        .find(|p| p.id == id && p.mode == mode && p.selectable)
        .ok_or(VaultError::InvalidPayload)
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn selected_dictionary_must_match_the_compiled_asset() {
        let original: Value =
            serde_json::from_str(include_str!("../../../generated/alpha/profile-matrix.json"))
                .unwrap();
        for field in ["id", "sha256"] {
            let mut changed = original.clone();
            let selected = changed["profiles"]
                .as_array_mut()
                .unwrap()
                .iter_mut()
                .find(|p| p["selectable"] == true)
                .unwrap();
            selected["dictionaries"][0][field] = Value::String("synthetic-mismatched-asset".into());
            assert!(parse(&changed.to_string()).is_err());
        }
    }
}
