//! Narrow borrowed sheet operations. Dictionary revisions always create a new
//! custom, unverified sheet and cannot rewrite an existing snapshot.
use crate::{
    catalog,
    model::{PayloadEditor, Sheet},
    spin::{generate_row, OsRandom},
    VaultError,
};
use std::{collections::HashSet, fs::File, io::Read, path::Path};
use subtle::ConstantTimeEq;
use unicode_normalization::{char::is_combining_mark, UnicodeNormalization};
use zeroize::{Zeroize, Zeroizing};

pub const SUPPORTED_ROWS: &[usize] = &[12, 13, 15, 16, 18, 20, 21, 24, 25, 26, 27, 28, 29, 33];
pub const MAX_CUSTOM_DICTIONARY_BYTES: usize = 1_056_771;
#[derive(Clone, Copy)]
pub struct SheetSize {
    pub rows: usize,
    pub columns: usize,
}
impl SheetSize {
    fn validate(self) -> Result<(), VaultError> {
        if !SUPPORTED_ROWS.contains(&self.rows) || ![10, 36].contains(&self.columns) {
            return Err(VaultError::InvalidPayload);
        }
        Ok(())
    }
}
pub struct SheetView<'a> {
    pub(crate) sheet: &'a Sheet,
}
impl SheetView<'_> {
    pub fn name(&self) -> &str {
        &self.sheet.name
    }
    pub fn profile_id(&self) -> &str {
        &self.sheet.profile_id
    }
    pub fn mode_id(&self) -> &str {
        &self.sheet.mode_id
    }
    pub fn dictionary(&self) -> &[String] {
        &self.sheet.dictionary
    }
    pub fn row_count(&self) -> usize {
        self.sheet.rows.len()
    }
    pub fn row(&self, index: usize) -> Option<&[String]> {
        self.sheet.rows.get(index).map(Vec::as_slice)
    }
    pub fn verified_by_me(&self) -> bool {
        self.sheet.verified_by_user
    }
    pub fn has_sheet_password(&self) -> bool {
        self.sheet.protection.is_some()
    }
    pub fn is_protected(&self) -> bool {
        !self.sheet.unlocked
    }
}
pub struct SheetEditor<'a> {
    pub(crate) sheet: &'a mut Sheet,
    // Exact remaining aggregate budget while this exclusive borrow is held.
    pub(crate) remaining: usize,
}
impl SheetEditor<'_> {
    /// Explicit user assertion after independent recovery checking, never inferred.
    pub fn set_verified_by_me(&mut self, verified: bool) {
        self.sheet.verified_by_user = verified;
    }
    pub fn rename(&mut self, name: &str) -> Result<(), VaultError> {
        let before = crate::model::text_len(&self.sheet.name);
        self.sheet.rename(name, self.remaining)?;
        let after = crate::model::text_len(&self.sheet.name);
        if after >= before {
            self.remaining -= after - before;
        } else {
            self.remaining += before - after;
        }
        Ok(())
    }
    pub fn set_protection(&mut self, secret: &str) -> Result<(), VaultError> {
        if secret.is_empty() {
            return Err(VaultError::InvalidPassword);
        }
        // Empty byte string costs 1 byte; a 48-byte verifier string costs 50.
        let growth = if self.sheet.protection.is_none() {
            49
        } else {
            0
        };
        if growth > self.remaining {
            return Err(VaultError::InvalidPayload);
        }
        let mut protection = Zeroizing::new([0; 48]);
        getrandom::getrandom(&mut protection[..16]).map_err(|_| VaultError::Io)?;
        let verifier = crate::crypto::derive(secret, &protection[..16])?;
        protection[16..].copy_from_slice(&*verifier);
        self.sheet.protection.zeroize();
        self.sheet.protection = Some(*protection);
        self.remaining -= growth;
        Ok(())
    }
}

fn normalized_dictionary(
    words: &[String],
    columns: usize,
) -> Result<Zeroizing<Vec<String>>, VaultError> {
    if words.len() < columns || words.len() > 8192 {
        return Err(VaultError::InvalidPayload);
    }
    let mut result = Zeroizing::new(Vec::with_capacity(words.len()));
    for input in words {
        if input.len() > 128 {
            return Err(VaultError::InvalidPayload);
        }
        let mut word = Zeroizing::new(String::with_capacity(128));
        for ch in input.nfkd() {
            if ch.is_whitespace() || ch.is_control() || word.len() + ch.len_utf8() > 128 {
                return Err(VaultError::InvalidPayload);
            }
            word.push(ch);
        }
        if word.is_empty() {
            return Err(VaultError::InvalidPayload);
        }
        result.push(std::mem::take(&mut *word));
    }
    if result.iter().collect::<HashSet<_>>().len() != result.len()
        || result
            .iter()
            .map(|word| comparison_key(word))
            .collect::<HashSet<_>>()
            .len()
            != result.len()
    {
        return Err(VaultError::InvalidPayload);
    }
    Ok(result)
}

fn comparison_key(word: &str) -> String {
    word.nfkd()
        .flat_map(char::to_lowercase)
        .filter(|ch| !is_combining_mark(*ch))
        .collect()
}

fn dictionary_from_file(path: &Path, columns: usize) -> Result<Zeroizing<Vec<String>>, VaultError> {
    let file = File::open(path).map_err(|_| VaultError::Io)?;
    let mut bytes = Zeroizing::new(Vec::new());
    file.take((MAX_CUSTOM_DICTIONARY_BYTES + 1) as u64)
        .read_to_end(&mut bytes)
        .map_err(|_| VaultError::Io)?;
    if bytes.len() > MAX_CUSTOM_DICTIONARY_BYTES {
        return Err(VaultError::TooLarge);
    }
    let text = std::str::from_utf8(&bytes).map_err(|_| VaultError::InvalidPayload)?;
    let text = text.strip_prefix('\u{feff}').unwrap_or(text);
    if text.is_empty() || text.contains('\u{feff}') {
        return Err(VaultError::InvalidPayload);
    }
    let mut lines = Zeroizing::new(Vec::new());
    let mut parts = text.split('\n').peekable();
    while let Some(mut line) = parts.next() {
        if line.is_empty() && parts.peek().is_none() && !lines.is_empty() {
            break;
        }
        let followed_by_lf = parts.peek().is_some();
        if let Some(without_cr) = line.strip_suffix('\r') {
            if !followed_by_lf {
                return Err(VaultError::InvalidPayload);
            }
            line = without_cr;
        } else if line.contains('\r') {
            return Err(VaultError::InvalidPayload);
        }
        if line.is_empty() {
            return Err(VaultError::InvalidPayload);
        }
        if lines.len() == 8192 {
            return Err(VaultError::InvalidPayload);
        }
        lines.push(line.to_owned());
    }
    normalized_dictionary(&lines, columns)
}
impl Sheet {
    pub(crate) fn validate(&self) -> Result<(), VaultError> {
        let columns = self.rows.first().map_or(0, Vec::len);
        SheetSize {
            rows: self.rows.len(),
            columns,
        }
        .validate()?;
        if self.profile_id != "custom" || self.mode_id != "custom" {
            let profile = catalog::select(&self.profile_id, &self.mode_id)?;
            if !profile.supported_lengths().contains(&self.rows.len())
                || !profile.matches_dictionary(&self.dictionary)
            {
                return Err(VaultError::InvalidPayload);
            }
        }
        if self.dictionary.len() < columns
            || self.dictionary.len() > 8192
            || self.profile_id.is_empty()
            || self.mode_id.is_empty()
            || self.dictionary.iter().any(|w| {
                w.is_empty()
                    || w.len() > 128
                    || w.chars().any(|ch| ch.is_whitespace() || ch.is_control())
                    || !w.nfkd().eq(w.chars())
            })
        {
            return Err(VaultError::InvalidPayload);
        }
        let dictionary: HashSet<_> = self.dictionary.iter().collect();
        if dictionary.len() != self.dictionary.len()
            || self.rows.iter().any(|row| {
                row.len() != columns
                    || row.iter().any(|w| !dictionary.contains(w))
                    || row.iter().collect::<HashSet<_>>().len() != columns
            })
        {
            return Err(VaultError::InvalidPayload);
        }
        Ok(())
    }
    fn create(
        name: &str,
        profile: &str,
        mode: &str,
        size: SheetSize,
        words: &[String],
    ) -> Result<Self, VaultError> {
        size.validate()?;
        if name.len() > 256 || name.contains('\0') {
            return Err(VaultError::InvalidPayload);
        }
        let mut dictionary = normalized_dictionary(words, size.columns)?;
        let mut sheet = Self {
            name: name.into(),
            profile_id: profile.into(),
            mode_id: mode.into(),
            dictionary: std::mem::take(&mut *dictionary),
            rows: Vec::with_capacity(size.rows),
            unlocked: true,
            ..Default::default()
        };
        for _ in 0..size.rows {
            let mut row = generate_row(&sheet.dictionary, size.columns, &mut OsRandom)
                .map_err(|_| VaultError::Io)?;
            sheet.rows.push(std::mem::take(&mut *row));
        }
        Ok(sheet)
    }
}
impl PayloadEditor<'_> {
    pub fn sheet_count(&self) -> usize {
        self.payload.sheets.len()
    }
    pub fn sheet(&self, index: usize) -> Result<SheetView<'_>, VaultError> {
        Ok(SheetView {
            sheet: self
                .payload
                .sheets
                .get(index)
                .ok_or(VaultError::InvalidPayload)?,
        })
    }
    pub fn edit_sheet(&mut self, index: usize) -> Result<SheetEditor<'_>, VaultError> {
        let remaining = crate::format::MAX_PAYLOAD - self.payload.encoded_len()?;
        let sheet = self
            .payload
            .sheets
            .get_mut(index)
            .ok_or(VaultError::InvalidPayload)?;
        if !sheet.unlocked {
            return Err(VaultError::AccessDenied);
        }
        Ok(SheetEditor { sheet, remaining })
    }
    pub fn protect_sheet(&mut self, index: usize) -> Result<(), VaultError> {
        self.payload
            .sheets
            .get_mut(index)
            .ok_or(VaultError::InvalidPayload)?
            .unlocked = false;
        Ok(())
    }
    pub fn unlock_sheet(&mut self, index: usize, secret: &str) -> Result<(), VaultError> {
        let sheet = self
            .payload
            .sheets
            .get_mut(index)
            .ok_or(VaultError::InvalidPayload)?;
        let protection = sheet.protection.as_ref().ok_or(VaultError::AccessDenied)?;
        let verifier = crate::crypto::derive(secret, &protection[..16])?;
        if !bool::from(verifier.as_slice().ct_eq(&protection[16..])) {
            return Err(VaultError::AccessDenied);
        }
        sheet.unlocked = true;
        Ok(())
    }
    fn insert_sheet(&mut self, sheet: Sheet) -> Result<usize, VaultError> {
        if self.payload.sheets.len() >= 32 {
            return Err(VaultError::InvalidPayload);
        }
        let index = self.payload.sheets.len();
        self.payload.sheets.push(sheet);
        // Aggregate serialized bounds must hold before exposing the new sheet.
        if self.payload.encoded_len().is_err() {
            self.payload.sheets.pop();
            return Err(VaultError::InvalidPayload);
        }
        Ok(index)
    }
    pub fn create_profile_sheet(
        &mut self,
        name: &str,
        id: &str,
        mode: &str,
        size: SheetSize,
    ) -> Result<usize, VaultError> {
        if self.sheet_count() >= 32 {
            return Err(VaultError::InvalidPayload);
        }
        let profile = catalog::select(id, mode)?;
        if !profile.supported_lengths().contains(&size.rows) {
            return Err(VaultError::InvalidPayload);
        }
        let dictionary = Zeroizing::new(profile.dictionary()?);
        self.insert_sheet(Sheet::create(name, id, mode, size, &dictionary)?)
    }
    /// Explicit custom flow: never represents a catalogue compatibility claim.
    pub fn create_custom_sheet(
        &mut self,
        name: &str,
        size: SheetSize,
        words: &[String],
    ) -> Result<usize, VaultError> {
        if self.sheet_count() >= 32 {
            return Err(VaultError::InvalidPayload);
        }
        self.insert_sheet(Sheet::create(name, "custom", "custom", size, words)?)
    }
    pub fn create_custom_sheet_from_file(
        &mut self,
        name: &str,
        size: SheetSize,
        path: &Path,
    ) -> Result<usize, VaultError> {
        size.validate()?;
        let dictionary = dictionary_from_file(path, size.columns)?;
        self.create_custom_sheet(name, size, &dictionary)
    }
    pub fn new_dictionary_sheet(
        &mut self,
        source: usize,
        name: &str,
        words: &[String],
    ) -> Result<usize, VaultError> {
        let sheet = self
            .payload
            .sheets
            .get(source)
            .ok_or(VaultError::InvalidPayload)?;
        if !sheet.unlocked {
            return Err(VaultError::AccessDenied);
        }
        let size = SheetSize {
            rows: sheet.rows.len(),
            columns: sheet.rows[0].len(),
        };
        self.create_custom_sheet(name, size, words)
    }
    pub fn new_dictionary_sheet_from_file(
        &mut self,
        source: usize,
        name: &str,
        path: &Path,
    ) -> Result<usize, VaultError> {
        let sheet = self
            .payload
            .sheets
            .get(source)
            .ok_or(VaultError::InvalidPayload)?;
        if !sheet.unlocked {
            return Err(VaultError::AccessDenied);
        }
        let size = SheetSize {
            rows: sheet.rows.len(),
            columns: sheet.rows[0].len(),
        };
        let dictionary = dictionary_from_file(path, size.columns)?;
        self.create_custom_sheet(name, size, &dictionary)
    }
    pub fn delete_sheet(
        &mut self,
        index: usize,
        exact_name: &str,
        confirmed: bool,
    ) -> Result<(), VaultError> {
        let sheet = self
            .payload
            .sheets
            .get(index)
            .ok_or(VaultError::InvalidPayload)?;
        if !sheet.unlocked || !confirmed || sheet.name.as_bytes() != exact_name.as_bytes() {
            return Err(VaultError::AccessDenied);
        }
        let mut removed = self.payload.sheets.remove(index);
        removed.zeroize();
        Ok(())
    }
}
