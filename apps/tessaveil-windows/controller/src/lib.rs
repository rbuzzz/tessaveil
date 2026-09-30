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
            if v.expire(v.timeout_token(), now) {
                self.dirty = false;
            }
        }
    }
    pub fn run(
        &mut self,
        op: u32,
        a: u32,
        b: u32,
        s: [&str; 4],
        now: Instant,
    ) -> Result<String, String> {
        self.execute(op, a, b, s, now).map_err(|e| e.to_string())
    }
    fn execute(
        &mut self,
        op: u32,
        a: u32,
        b: u32,
        s: [&str; 4],
        now: Instant,
    ) -> Result<String, VaultError> {
        self.expire(now);
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
            }
            ACTIVITY => {
                self.v()?.activity(now)?;
            }
            TICK | INFO => {}
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
