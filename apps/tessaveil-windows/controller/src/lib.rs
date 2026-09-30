use std::{path::Path, time::Instant};
use tessaveil_core::{
    catalog,
    session::Inactivity,
    sheet::SheetSize,
    spin::{OsRandom, SpinRequest},
    CreateOptions, OpenVault, StoragePolicy, VaultError, VaultService,
};
mod ffi;
pub use ffi::*;
pub const ACK: u32 = 1;
pub const CREATE: u32 = 2;
pub const OPEN: u32 = 3;
pub const SAVE: u32 = 4;
pub const CLOSE: u32 = 5;
pub const LOCK: u32 = 6;
pub const UNLOCK: u32 = 7;
pub const ADD: u32 = 8;
pub const SELECT: u32 = 9;
pub const VERIFY: u32 = 10;
pub const SET_SHEET_PASSWORD: u32 = 11;
pub const PROTECT: u32 = 12;
pub const UNLOCK_SHEET: u32 = 13;
pub const UNLOCK_MASTER: u32 = 14;
pub const SPIN: u32 = 15;
pub const TIMEOUT: u32 = 16;
pub const ACTIVITY: u32 = 17;
pub const TICK: u32 = 18;
pub const INFO: u32 = 19;
pub const CELL: u32 = 20;
pub const PROFILE: u32 = 21;
pub const PROFILE_COUNT: u32 = 22;
pub const SHEET_NAME: u32 = 23;
pub const PROFILE_LENGTHS: u32 = 24;
pub const ADD_CUSTOM: u32 = 25;
pub const REPLACE_DICTIONARY: u32 = 26;
pub const RENAME_SHEET: u32 = 27;
pub const DELETE_SHEET: u32 = 28;
pub const PROFILE_FIELD: u32 = 29;
pub const PROFILE_LENGTH_COUNT: u32 = 30;
pub const PROFILE_LENGTH: u32 = 31;
pub const SHEET_FIELD: u32 = 32;
pub const BACKUP: u32 = 33;
pub const RESTORE: u32 = 34;
pub const CHANGE_PASSWORD: u32 = 35;
pub const LOCALE: u32 = 36;
pub const THEME: u32 = 37;

#[derive(Clone, Copy)]
enum Theme {
    System,
    Light,
    Dark,
}
impl Theme {
    fn parse(value: &str) -> Result<Self, VaultError> {
        match value {
            "system" => Ok(Self::System),
            "light" => Ok(Self::Light),
            "dark" => Ok(Self::Dark),
            _ => Err(VaultError::InvalidPayload),
        }
    }
    fn as_str(self) -> &'static str {
        match self {
            Self::System => "system",
            Self::Light => "light",
            Self::Dark => "dark",
        }
    }
}
#[derive(Default)]
pub struct State {
    pub state: u32,
    pub dirty: u32,
    pub sheets: u32,
    pub rows: u32,
    pub columns: u32,
    pub protected: u32,
    pub verified: u32,
    pub minutes: u32,
}
pub struct Controller {
    ack: bool,
    vault: Option<OpenVault>,
    path: Option<String>,
    dirty: bool,
    selected: usize,
    minutes: u8,
    timeout_generation: u32,
    theme: Theme,
}
impl Default for Controller {
    fn default() -> Self {
        Self {
            ack: false,
            vault: None,
            path: None,
            dirty: false,
            selected: 0,
            minutes: 5,
            timeout_generation: 0,
            theme: Theme::System,
        }
    }
}
impl Controller {
    fn v(&mut self) -> Result<&mut OpenVault, VaultError> {
        self.vault
            .as_mut()
            .filter(|v| !v.is_locked())
            .ok_or(VaultError::Locked)
    }
    fn expire(&mut self, now: Instant) {
        if let Some(v) = &mut self.vault {
            if !v.is_locked() && v.expire(v.timeout_token(), now) {
                self.dirty = false;
                self.selected = 0;
                self.bump_timeout_generation();
            }
        }
    }
    fn bump_timeout_generation(&mut self) -> u32 {
        self.timeout_generation = self.timeout_generation.wrapping_add(1);
        if self.timeout_generation == 0 {
            self.timeout_generation = 1;
        }
        self.timeout_generation
    }
    pub fn run(
        &mut self,
        op: u32,
        a: u32,
        b: u32,
        s: [&str; 4],
        now: Instant,
    ) -> Result<String, String> {
        self.execute(op, a, b, s, now)
            .map_err(|error| error_key(&error).into())
    }
    fn execute(
        &mut self,
        op: u32,
        a: u32,
        b: u32,
        s: [&str; 4],
        now: Instant,
    ) -> Result<String, VaultError> {
        if op != TICK {
            self.expire(now);
        }
        match op {
            ACK => self.ack = true,
            CREATE | OPEN | UNLOCK => {
                if !self.ack || self.vault.as_ref().is_some_and(|v| !v.is_locked()) {
                    return Err(VaultError::AccessDenied);
                }
                let (path, password) = if op == UNLOCK {
                    (self.path.as_deref().ok_or(VaultError::Locked)?, s[0])
                } else {
                    (s[0], s[1])
                };
                let mut v = if op == CREATE {
                    VaultService::create(
                        path,
                        password,
                        CreateOptions {
                            name: s[2].into(),
                            storage: StoragePolicy::DevelopmentLocalNtfs,
                            inactivity: Inactivity::from_minutes(self.minutes)?,
                        },
                    )?
                } else {
                    VaultService::open(path, password)?
                };
                v.set_storage_policy(StoragePolicy::DevelopmentLocalNtfs);
                v.set_inactivity(Inactivity::from_minutes(self.minutes)?, Instant::now())?;
                self.path = Some(path.into());
                self.vault = Some(v);
                self.dirty = false;
                self.selected = 0;
                return Ok(self.bump_timeout_generation().to_string());
            }
            SAVE => {
                self.v()?.save()?;
                self.dirty = false;
            }
            CLOSE | LOCK => {
                if self.dirty {
                    match a {
                        1 => {
                            self.v()?.save()?;
                        }
                        2 => {}
                        _ => return Err(VaultError::AccessDenied),
                    }
                }
                if let Some(v) = &mut self.vault {
                    v.lock();
                }
                self.vault = None;
                self.dirty = false;
                self.selected = 0;
                if op == CLOSE {
                    self.path = None;
                }
                self.bump_timeout_generation();
            }
            ADD => {
                let profile = catalog::profiles()?
                    .get(a as usize)
                    .filter(|p| p.selectable())
                    .ok_or(VaultError::InvalidPayload)?;
                let rows = if s[1].is_empty() {
                    match profile.supported_lengths() {
                        [only] => *only,
                        _ => return Err(VaultError::InvalidPayload),
                    }
                } else {
                    s[1].parse::<usize>()
                        .map_err(|_| VaultError::InvalidPayload)?
                };
                self.selected = self.v()?.payload_mut()?.create_profile_sheet(
                    s[0],
                    profile.id(),
                    profile.mode(),
                    SheetSize {
                        rows,
                        columns: b as usize,
                    },
                )?;
                self.dirty = true;
            }
            ADD_CUSTOM => {
                self.selected = self.v()?.payload_mut()?.create_custom_sheet_from_file(
                    s[0],
                    SheetSize {
                        rows: a as usize,
                        columns: b as usize,
                    },
                    Path::new(s[1]),
                )?;
                self.dirty = true;
            }
            REPLACE_DICTIONARY => {
                if a != 1 {
                    return Err(VaultError::AccessDenied);
                }
                let selected = self.selected;
                self.selected = self.v()?.payload_mut()?.new_dictionary_sheet_from_file(
                    selected,
                    s[0],
                    Path::new(s[1]),
                )?;
                self.dirty = true;
            }
            RENAME_SHEET => {
                let selected = self.selected;
                self.v()?
                    .payload_mut()?
                    .edit_sheet(selected)?
                    .rename(s[0])?;
                self.dirty = true;
            }
            DELETE_SHEET => {
                let selected = self.selected;
                let next = {
                    let mut payload = self.v()?.payload_mut()?;
                    payload.delete_sheet(selected, s[0], a == 1)?;
                    if payload.sheet_count() == 0 {
                        0
                    } else {
                        selected.min(payload.sheet_count() - 1)
                    }
                };
                self.selected = next;
                self.dirty = true;
            }
            SELECT => {
                self.v()?.payload_mut()?.sheet(a as usize)?;
                self.selected = a as usize;
            }
            VERIFY => {
                let selected = self.selected;
                self.v()?
                    .payload_mut()?
                    .edit_sheet(selected)?
                    .set_verified_by_me(a == 1);
                self.dirty = true;
            }
            SET_SHEET_PASSWORD => {
                let selected = self.selected;
                self.v()?
                    .payload_mut()?
                    .edit_sheet(selected)?
                    .set_protection(s[0])?;
                self.dirty = true;
            }
            PROTECT => {
                let selected = self.selected;
                self.v()?.payload_mut()?.protect_sheet(selected)?;
            }
            UNLOCK_SHEET => {
                let selected = self.selected;
                self.v()?.payload_mut()?.unlock_sheet(selected, s[0])?;
            }
            UNLOCK_MASTER => {
                let selected = self.selected;
                self.v()?.unlock_sheet_with_master(selected, s[0])?;
            }
            SPIN => {
                let selected = self.selected;
                self.v()?
                    .payload_mut()?
                    .edit_sheet(selected)?
                    .spin_row(
                        SpinRequest {
                            row: a as usize,
                            first_symbol: s[0],
                            second_symbol: s[1],
                            word: s[2],
                        },
                        &mut OsRandom,
                    )
                    .map_err(|_| VaultError::InvalidPayload)?;
                self.dirty = true;
            }
            TIMEOUT => {
                let timeout = Inactivity::from_minutes(
                    u8::try_from(a).map_err(|_| VaultError::InvalidPayload)?,
                )?;
                if let Some(v) = &mut self.vault {
                    if !v.is_locked() {
                        v.set_inactivity(timeout, now)?;
                    }
                }
                self.minutes = a as u8;
                return Ok(self.bump_timeout_generation().to_string());
            }
            ACTIVITY => {
                self.v()?.activity(now)?;
                return Ok(self.bump_timeout_generation().to_string());
            }
            TICK => {
                if a == self.timeout_generation {
                    self.expire(now);
                }
            }
            INFO => {}
            CELL => {
                let selected = self.selected;
                let p = self.v()?.payload_mut()?;
                let view = p.sheet(selected)?;
                return Ok(view
                    .row(a as usize)
                    .and_then(|r| r.get(b as usize))
                    .ok_or(VaultError::InvalidPayload)?
                    .clone());
            }
            SHEET_NAME => return Ok(self.v()?.payload_mut()?.sheet(a as usize)?.name().into()),
            PROFILE_COUNT => return Ok(catalog::profiles()?.len().to_string()),
            PROFILE => {
                let p = catalog::profiles()?
                    .get(a as usize)
                    .ok_or(VaultError::InvalidPayload)?;
                return Ok(format!(
                    "{}\t{}\t{}\t{}\t{}",
                    u8::from(p.selectable()),
                    p.name(),
                    p.id(),
                    p.mode(),
                    p.reason()
                ));
            }
            PROFILE_LENGTHS => {
                let profile = catalog::profiles()?
                    .get(a as usize)
                    .ok_or(VaultError::InvalidPayload)?;
                return Ok(profile
                    .supported_lengths()
                    .iter()
                    .map(usize::to_string)
                    .collect::<Vec<_>>()
                    .join(","));
            }
            PROFILE_FIELD => {
                let profile = catalog::profiles()?
                    .get(a as usize)
                    .ok_or(VaultError::InvalidPayload)?;
                let (value, bound) = match b {
                    0 => (if profile.selectable() { "1" } else { "0" }, 1),
                    1 => (profile.name(), 256),
                    2 => (profile.id(), 128),
                    3 => (profile.mode(), 128),
                    4 => (profile.reason(), 160),
                    5 => (profile.platform(), 64),
                    6 => (profile.status(), 32),
                    7 => (profile.version_min(), 128),
                    8 => (profile.version_max(), 128),
                    _ => return Err(VaultError::InvalidPayload),
                };
                return bounded(value, bound);
            }
            PROFILE_LENGTH_COUNT => {
                let profile = catalog::profiles()?
                    .get(a as usize)
                    .ok_or(VaultError::InvalidPayload)?;
                return Ok(profile.supported_lengths().len().to_string());
            }
            PROFILE_LENGTH => {
                let profile = catalog::profiles()?
                    .get(a as usize)
                    .ok_or(VaultError::InvalidPayload)?;
                return Ok(profile
                    .supported_lengths()
                    .get(b as usize)
                    .ok_or(VaultError::InvalidPayload)?
                    .to_string());
            }
            SHEET_FIELD => {
                let payload = self.v()?.payload_mut()?;
                let sheet = payload.sheet(a as usize)?;
                let value = match b {
                    0 => return bounded(sheet.name(), 256),
                    1 => return bounded(sheet.profile_id(), 128),
                    2 => return bounded(sheet.mode_id(), 128),
                    3 => sheet.row_count().to_string(),
                    4 => sheet.row(0).map_or(0, |row| row.len()).to_string(),
                    5 => u8::from(sheet.is_protected()).to_string(),
                    6 => u8::from(sheet.verified_by_me()).to_string(),
                    7 => u8::from(sheet.has_sheet_password()).to_string(),
                    _ => return Err(VaultError::InvalidPayload),
                };
                return Ok(value);
            }
            BACKUP => {
                self.v()?.backup_to(Path::new(s[0]))?;
            }
            RESTORE => {
                if !self.ack || self.path.is_some() || self.vault.is_some() {
                    return Err(VaultError::AccessDenied);
                }
                let mut vault = VaultService::restore(
                    Path::new(s[0]),
                    Path::new(s[1]),
                    s[2],
                    StoragePolicy::DevelopmentLocalNtfs,
                )?;
                vault.set_storage_policy(StoragePolicy::DevelopmentLocalNtfs);
                vault.set_inactivity(Inactivity::from_minutes(self.minutes)?, now)?;
                self.path = Some(s[1].into());
                self.vault = Some(vault);
                self.dirty = false;
                self.selected = 0;
                return Ok(self.bump_timeout_generation().to_string());
            }
            CHANGE_PASSWORD => {
                self.v()?.change_master_password(s[0], s[1])?;
                self.dirty = false;
            }
            LOCALE => match a {
                0 => {
                    let locale = {
                        let payload = self.v()?.payload_mut()?;
                        if payload.locale().is_empty() {
                            "en".into()
                        } else {
                            payload.locale().into()
                        }
                    };
                    return Ok(locale);
                }
                1 => {
                    let changed = self.v()?.payload_mut()?.set_locale(s[0])?;
                    if changed {
                        self.dirty = true;
                    }
                }
                _ => return Err(VaultError::InvalidPayload),
            },
            THEME => match a {
                0 => return Ok(self.theme.as_str().into()),
                1 => self.theme = Theme::parse(s[0])?,
                _ => return Err(VaultError::InvalidPayload),
            },
            _ => return Err(VaultError::InvalidPayload),
        }
        Ok(String::new())
    }
    pub fn state(&mut self) -> State {
        self.expire(Instant::now());
        let mut state = State {
            state: if self.path.is_some() { 1 } else { 0 },
            minutes: self.minutes.into(),
            ..Default::default()
        };
        let selected = self.selected;
        if let Ok(v) = self.v() {
            if let Ok(p) = v.payload_mut() {
                state.state = 2;
                state.sheets = p.sheet_count() as u32;
                if let Ok(sheet) = p.sheet(selected) {
                    state.rows = sheet.row_count() as u32;
                    state.columns = sheet.row(0).map_or(0, |r| r.len()) as u32;
                    state.protected = sheet.is_protected().into();
                    state.verified = sheet.verified_by_me().into();
                }
            }
        }
        state.dirty = self.dirty.into();
        state
    }
}

fn bounded(value: &str, bound: usize) -> Result<String, VaultError> {
    if value.len() > bound {
        Err(VaultError::InvalidPayload)
    } else {
        Ok(value.into())
    }
}

fn error_key(error: &VaultError) -> &'static str {
    match error {
        VaultError::InvalidHeader => "invalid-header",
        VaultError::UnsupportedVersion => "unsupported-version",
        VaultError::KdfOutOfBounds => "kdf-out-of-bounds",
        VaultError::UnsupportedKdf => "unsupported-kdf",
        VaultError::Truncated => "truncated",
        VaultError::TooLarge => "too-large",
        VaultError::Authentication => "authentication",
        VaultError::InvalidPassword => "invalid-password",
        VaultError::PasswordPolicy => "password-policy",
        VaultError::AccessDenied => "access-denied",
        VaultError::InsufficientSpace => "insufficient-space",
        VaultError::Io => "io",
        VaultError::AlreadyExists => "already-exists",
        VaultError::InvalidPath => "invalid-path",
        VaultError::UnsupportedFilesystem => "unsupported-filesystem",
        VaultError::Locked => "locked",
        VaultError::UnsavedChanges => "unsaved-changes",
        VaultError::InvalidPayload => "invalid-payload",
        VaultError::TemporaryRemains { .. } => "temporary-remains",
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn every_domain_error_has_a_unique_bounded_localization_key() {
        let errors = vec![
            VaultError::InvalidHeader,
            VaultError::UnsupportedVersion,
            VaultError::KdfOutOfBounds,
            VaultError::UnsupportedKdf,
            VaultError::Truncated,
            VaultError::TooLarge,
            VaultError::Authentication,
            VaultError::InvalidPassword,
            VaultError::PasswordPolicy,
            VaultError::AccessDenied,
            VaultError::InsufficientSpace,
            VaultError::Io,
            VaultError::AlreadyExists,
            VaultError::InvalidPath,
            VaultError::UnsupportedFilesystem,
            VaultError::Locked,
            VaultError::UnsavedChanges,
            VaultError::InvalidPayload,
            VaultError::TemporaryRemains {
                cause: Box::new(VaultError::Io),
                path: Some(std::path::PathBuf::from("x".repeat(5000))),
            },
        ];
        let keys: Vec<_> = errors.iter().map(error_key).collect();
        assert!(keys.iter().all(|key| {
            !key.is_empty()
                && key.len() <= 32
                && key
                    .bytes()
                    .all(|byte| byte.is_ascii_lowercase() || byte == b'-')
        }));
        let unique: std::collections::HashSet<_> = keys.iter().copied().collect();
        assert_eq!(unique.len(), keys.len());
    }
}
