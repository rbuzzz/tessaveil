use crate::VaultError;
use zeroize::{Zeroize, ZeroizeOnDrop, Zeroizing};

#[derive(Default, Zeroize, ZeroizeOnDrop)]
pub(crate) struct Payload {
    pub(crate) name: String,
    pub(crate) locale: String,
    pub(crate) sheets: Vec<Sheet>,
}
#[derive(Default, Zeroize, ZeroizeOnDrop)]
pub(crate) struct Sheet {
    pub(crate) name: String,
    pub(crate) profile_id: String,
    pub(crate) mode_id: String,
    pub(crate) dictionary: Vec<String>,
    pub(crate) rows: Vec<Vec<String>>,
    pub(crate) verified_by_user: bool,
    pub(crate) protection: Option<[u8; 48]>,
    // Session-only authorization. Never serialized; every open starts protected.
    pub(crate) unlocked: bool,
}
impl Sheet {
    pub(crate) fn rename(&mut self, name: &str, remaining: usize) -> Result<(), VaultError> {
        if name.is_empty() || name.len() > 256 || name.chars().any(char::is_control) {
            return Err(VaultError::InvalidPayload);
        }
        let growth = text_len(name).saturating_sub(text_len(&self.name));
        if growth > remaining {
            return Err(VaultError::InvalidPayload);
        }
        self.name.zeroize();
        self.name = name.to_owned();
        Ok(())
    }
}
impl Payload {
    pub fn name(&self) -> &str {
        &self.name
    }
    pub fn rename(&mut self, name: &str) -> Result<(), VaultError> {
        if name.len() > 256 || name.contains('\0') {
            return Err(VaultError::InvalidPayload);
        }
        let next = self.encoded_len()? - text_len(&self.name) + text_len(name);
        if next > crate::format::MAX_PAYLOAD {
            return Err(VaultError::InvalidPayload);
        }
        self.name.zeroize();
        self.name = name.to_owned();
        Ok(())
    }
    pub(crate) fn encode(&self) -> Result<Zeroizing<Vec<u8>>, VaultError> {
        let mut w = Writer {
            bytes: Some(Zeroizing::new(Vec::with_capacity(
                crate::format::MAX_PAYLOAD,
            ))),
            len: 0,
        };
        self.write(&mut w)?;
        Ok(w.bytes.expect("encoding writer owns output"))
    }
    // The exact same validated codec can count without allocating/copying plaintext.
    pub(crate) fn encoded_len(&self) -> Result<usize, VaultError> {
        let mut w = Writer {
            bytes: None,
            len: 0,
        };
        self.write(&mut w)?;
        Ok(w.len)
    }
    fn write(&self, w: &mut Writer) -> Result<(), VaultError> {
        w.number(4, 4)?;
        w.number(0, 2)?;
        w.text(&self.name, 256)?;
        w.text(&self.locale, 16)?;
        w.array(self.sheets.len(), 32)?;
        for s in &self.sheets {
            s.validate()?;
            w.array(7, 7)?;
            w.text(&s.name, 256)?;
            w.text(&s.profile_id, 128)?;
            w.text(&s.mode_id, 128)?;
            w.array(s.dictionary.len(), 8192)?;
            for word in &s.dictionary {
                w.text(word, 128)?;
            }
            w.array(s.rows.len(), 33)?;
            let columns = s.rows.first().map_or(0, Vec::len);
            if !s.rows.is_empty() && (!ROWS.contains(&s.rows.len()) || ![10, 36].contains(&columns))
            {
                return Err(VaultError::InvalidPayload);
            }
            for row in &s.rows {
                if row.len() != columns {
                    return Err(VaultError::InvalidPayload);
                }
                w.array(row.len(), 36)?;
                for word in row {
                    w.text(word, 128)?;
                }
            }
            w.push(&[if s.verified_by_user { 0xf5 } else { 0xf4 }])?;
            let protection = s.protection.as_ref().map_or(&[][..], |v| &v[..]);
            w.number(2, protection.len())?;
            w.push(protection)?;
        }
        Ok(())
    }
    pub(crate) fn decode(bytes: &[u8]) -> Result<Self, VaultError> {
        if bytes.len() > crate::format::MAX_PAYLOAD {
            return Err(VaultError::InvalidPayload);
        }
        let mut r = Reader { bytes, offset: 0 };
        // Recognize the canonical, bounded envelope of the schema before imposing
        // v2's arity: a future mandatory field changes arity together with version.
        let arity = r.array(65535)?;
        if arity == 0 {
            return Err(VaultError::InvalidPayload);
        }
        if r.number(0)? != 2 {
            return Err(VaultError::UnsupportedVersion);
        }
        if arity != 4 {
            return Err(VaultError::InvalidPayload);
        }
        let mut p = Self::default();
        p.name = r.text(256)?;
        p.locale = r.text(16)?;
        let count = r.array(32)?;
        for _ in 0..count {
            if r.array(7)? != 7 {
                return Err(VaultError::InvalidPayload);
            }
            let mut s = Sheet::default();
            s.name = r.text(256)?;
            s.profile_id = r.text(128)?;
            s.mode_id = r.text(128)?;
            let dictionary_count = r.array(8192)?;
            for _ in 0..dictionary_count {
                s.dictionary.push(r.text(128)?);
            }
            let row_count = r.array(33)?;
            if row_count != 0 && !ROWS.contains(&row_count) {
                return Err(VaultError::InvalidPayload);
            }
            let mut columns = 0;
            for _ in 0..row_count {
                let count = r.array(36)?;
                if ![10, 36].contains(&count) || (columns != 0 && count != columns) {
                    return Err(VaultError::InvalidPayload);
                }
                columns = count;
                let mut row = Zeroizing::new(Vec::with_capacity(count));
                for _ in 0..count {
                    row.push(r.text(128)?);
                }
                s.rows.push(std::mem::take(&mut *row));
            }
            s.verified_by_user = r.boolean()?;
            match r.number(2)? {
                0 => (),
                48 => {
                    s.protection = Some(
                        r.take(48)?
                            .try_into()
                            .map_err(|_| VaultError::InvalidPayload)?,
                    )
                }
                _ => return Err(VaultError::InvalidPayload),
            }
            s.validate()?;
            p.sheets.push(s);
        }
        if r.offset != bytes.len() {
            return Err(VaultError::InvalidPayload);
        }
        Ok(p)
    }
}
/// Domain-only borrowed access; no owned payload, serde or plaintext byte access.
pub struct PayloadEditor<'a> {
    pub(crate) payload: &'a mut Payload,
}
impl PayloadEditor<'_> {
    pub fn name(&self) -> &str {
        self.payload.name()
    }
    pub fn rename(&mut self, name: &str) -> Result<(), VaultError> {
        self.payload.rename(name)
    }
    pub fn locale(&self) -> &str {
        &self.payload.locale
    }
    pub fn set_locale(&mut self, locale: &str) -> Result<bool, VaultError> {
        if !matches!(locale, "en" | "ru") {
            return Err(VaultError::InvalidPayload);
        }
        if self.payload.locale == locale {
            return Ok(false);
        }
        let next = self.payload.encoded_len()? - text_len(&self.payload.locale) + text_len(locale);
        if next > crate::format::MAX_PAYLOAD {
            return Err(VaultError::InvalidPayload);
        }
        self.payload.locale.zeroize();
        self.payload.locale = locale.into();
        Ok(true)
    }
}
const ROWS: &[usize] = crate::sheet::SUPPORTED_ROWS;
pub(crate) fn text_len(text: &str) -> usize {
    text.len()
        + if text.len() < 24 {
            1
        } else if text.len() <= 255 {
            2
        } else {
            3
        }
}
struct Writer {
    bytes: Option<Zeroizing<Vec<u8>>>,
    len: usize,
}
impl Writer {
    fn push(&mut self, bytes: &[u8]) -> Result<(), VaultError> {
        if bytes.len() > crate::format::MAX_PAYLOAD - self.len {
            return Err(VaultError::InvalidPayload);
        }
        if let Some(output) = &mut self.bytes {
            output.extend_from_slice(bytes);
        }
        self.len += bytes.len();
        Ok(())
    }
    fn number(&mut self, major: u8, n: usize) -> Result<(), VaultError> {
        if n < 24 {
            self.push(&[(major << 5) | n as u8])
        } else if n <= 255 {
            self.push(&[(major << 5) | 24, n as u8])
        } else if n <= 65535 {
            self.push(&[(major << 5) | 25, (n >> 8) as u8, n as u8])
        } else {
            Err(VaultError::InvalidPayload)
        }
    }
    fn array(&mut self, n: usize, max: usize) -> Result<(), VaultError> {
        if n > max {
            return Err(VaultError::InvalidPayload);
        }
        self.number(4, n)
    }
    fn text(&mut self, s: &str, max: usize) -> Result<(), VaultError> {
        if s.len() > max || s.contains('\0') {
            return Err(VaultError::InvalidPayload);
        }
        self.number(3, s.len())?;
        self.push(s.as_bytes())
    }
}
struct Reader<'a> {
    bytes: &'a [u8],
    offset: usize,
}
impl<'a> Reader<'a> {
    fn take(&mut self, len: usize) -> Result<&'a [u8], VaultError> {
        let end = self
            .offset
            .checked_add(len)
            .ok_or(VaultError::InvalidPayload)?;
        let out = self
            .bytes
            .get(self.offset..end)
            .ok_or(VaultError::InvalidPayload)?;
        self.offset = end;
        Ok(out)
    }
    fn number(&mut self, major: u8) -> Result<usize, VaultError> {
        let byte = self.take(1)?[0];
        if byte >> 5 != major {
            return Err(VaultError::InvalidPayload);
        }
        let n = match byte & 31 {
            n @ 0..=23 => n as usize,
            24 => {
                let n = self.take(1)?[0] as usize;
                if n < 24 {
                    return Err(VaultError::InvalidPayload);
                }
                n
            }
            25 => {
                let v = self.take(2)?;
                let n = u16::from_be_bytes([v[0], v[1]]) as usize;
                if n <= 255 {
                    return Err(VaultError::InvalidPayload);
                }
                n
            }
            _ => return Err(VaultError::InvalidPayload),
        };
        Ok(n)
    }
    fn array(&mut self, max: usize) -> Result<usize, VaultError> {
        let n = self.number(4)?;
        if n > max || n > self.bytes.len() - self.offset {
            return Err(VaultError::InvalidPayload);
        }
        Ok(n)
    }
    fn text(&mut self, max: usize) -> Result<String, VaultError> {
        let n = self.number(3)?;
        if n > max {
            return Err(VaultError::InvalidPayload);
        }
        let s = std::str::from_utf8(self.take(n)?).map_err(|_| VaultError::InvalidPayload)?;
        if s.contains('\0') {
            return Err(VaultError::InvalidPayload);
        }
        Ok(s.to_owned())
    }
    fn boolean(&mut self) -> Result<bool, VaultError> {
        match self.take(1)?[0] {
            0xf4 => Ok(false),
            0xf5 => Ok(true),
            _ => Err(VaultError::InvalidPayload),
        }
    }
}
#[cfg(test)]
mod tests {
    use super::*;
    fn synthetic_sheet(count: usize, width: usize) -> Sheet {
        let dictionary: Vec<_> = (0..count)
            .map(|i| format!("s{i:04}{}", "x".repeat(width - 5)))
            .collect();
        Sheet {
            name: String::new(),
            profile_id: "custom".into(),
            mode_id: "custom".into(),
            rows: vec![dictionary[..10].to_vec(); 12],
            dictionary,
            unlocked: true,
            verified_by_user: true,
            ..Default::default()
        }
    }
    fn near_limit(remaining: usize) -> Payload {
        let mut p = Payload::default();
        for _ in 0..7 {
            p.sheets.push(synthetic_sheet(8192, 128));
        }
        let current = p.encode().unwrap().len();
        let count = (crate::format::MAX_PAYLOAD - current - 30_000) / 130;
        p.sheets.push(synthetic_sheet(count, 128));
        p.sheets.push(synthetic_sheet(10, 5));
        let target = crate::format::MAX_PAYLOAD - remaining;
        let extra = (target - p.encode().unwrap().len()) / 130 - 1;
        p.sheets[8]
            .dictionary
            .extend((0..extra).map(|i| format!("t{i:04}{}", "x".repeat(123))));
        let base = p.encode().unwrap().len();
        for n in 0..=256 {
            for locale in 0..=16 {
                let growth = n + if n < 24 {
                    0
                } else if n <= 255 {
                    1
                } else {
                    2
                };
                if base + growth + locale == target {
                    p.sheets[0].name = "n".repeat(n);
                    p.locale = "l".repeat(locale);
                    assert_eq!(p.encode().unwrap().len(), target);
                    return p;
                }
            }
        }
        panic!("synthetic boundary fixture could not reach exact length");
    }
    #[test]
    fn protection_and_rename_preserve_exact_aggregate_boundary() {
        let mut p = near_limit(48);
        let before = p.encode().unwrap();
        assert!(PayloadEditor { payload: &mut p }
            .edit_sheet(0)
            .unwrap()
            .set_protection("synthetic-sheet-password")
            .is_err());
        assert!(p.sheets[0].protection.is_none());
        assert!(p.sheets[0].verified_by_user && p.sheets[0].unlocked);
        assert_eq!(p.encode().unwrap(), before);
        // Empty name -> 48 characters costs 49 additional CBOR bytes.
        let longer = "n".repeat(48);
        assert!(p.rename(&longer).is_err());
        assert_eq!(p.encode().unwrap(), before);
        assert!(p.rename("synthetic\0name").is_err());
        assert_eq!(p.encode().unwrap(), before);
        p.rename(&"n".repeat(47)).unwrap();
        assert_eq!(p.encode().unwrap().len(), crate::format::MAX_PAYLOAD);
        let mut p = near_limit(49);
        PayloadEditor { payload: &mut p }
            .edit_sheet(0)
            .unwrap()
            .set_protection("synthetic-sheet-password")
            .unwrap();
        assert_eq!(p.encode().unwrap().len(), crate::format::MAX_PAYLOAD);
        // Replacing a verifier has no size growth, even at exactly MAX_PAYLOAD.
        PayloadEditor { payload: &mut p }
            .edit_sheet(0)
            .unwrap()
            .set_protection("synthetic-next-password")
            .unwrap();
        assert_eq!(p.encode().unwrap().len(), crate::format::MAX_PAYLOAD);
    }
    #[test]
    fn sheet_rename_requires_unlocked_state_and_preserves_exact_aggregate_boundary() {
        let mut p = near_limit(0);
        let before = p.encode().unwrap();
        assert!(PayloadEditor { payload: &mut p }
            .edit_sheet(8)
            .unwrap()
            .rename("x")
            .is_err());
        assert_eq!(p.encode().unwrap(), before);

        let mut p = near_limit(1);
        PayloadEditor { payload: &mut p }
            .edit_sheet(8)
            .unwrap()
            .rename("x")
            .unwrap();
        assert_eq!(p.encode().unwrap().len(), crate::format::MAX_PAYLOAD);
        let before = p.encode().unwrap();
        p.sheets[8].unlocked = false;
        assert!(PayloadEditor { payload: &mut p }
            .edit_sheet(8)
            .and_then(|mut sheet| sheet.rename("locked"))
            .is_err());
        p.sheets[8].unlocked = true;
        for invalid in ["", "synthetic\nname", "synthetic\0name"] {
            assert!(PayloadEditor { payload: &mut p }
                .edit_sheet(8)
                .unwrap()
                .rename(invalid)
                .is_err());
        }
        assert_eq!(p.encode().unwrap(), before);
    }
    #[test]
    fn sheet_editor_tracks_rename_growth_before_a_second_mutation() {
        let mut p = near_limit(49);
        {
            let mut payload = PayloadEditor { payload: &mut p };
            let mut sheet = payload.edit_sheet(8).unwrap();
            sheet.rename("x").unwrap();
            assert!(sheet.set_protection("synthetic-sheet-password").is_err());
        }
        assert!(p.sheets[8].protection.is_none());
        assert!(p.encoded_len().unwrap() <= crate::format::MAX_PAYLOAD);

        let mut p = near_limit(50);
        {
            let mut payload = PayloadEditor { payload: &mut p };
            let mut sheet = payload.edit_sheet(8).unwrap();
            sheet.rename("x").unwrap();
            sheet.set_protection("synthetic-sheet-password").unwrap();
        }
        assert_eq!(p.encoded_len().unwrap(), crate::format::MAX_PAYLOAD);
    }
    #[test]
    fn spin_budget_is_candidate_independent_and_failure_preserves_state() {
        use crate::spin::{RandomSource, SpinError, SpinRequest};
        struct CountRandom(usize);
        impl RandomSource for CountRandom {
            fn fill(&mut self, bytes: &mut [u8]) -> Result<(), SpinError> {
                self.0 += 1;
                bytes.copy_from_slice(&u32::MAX.to_le_bytes());
                Ok(())
            }
        }
        // Ten 128-byte entries cost 1300 CBOR bytes; old ten 5-byte entries cost 60.
        let mut p = near_limit(1239);
        let before = p.encode().unwrap();
        let long = p.sheets[8].dictionary[10].clone();
        for word in [long.as_str(), "s0000", "synthetic-invalid"] {
            let mut rng = CountRandom(0);
            assert!(PayloadEditor { payload: &mut p }
                .edit_sheet(8)
                .unwrap()
                .spin_row(
                    SpinRequest {
                        row: 0,
                        first_symbol: "0",
                        second_symbol: "0",
                        word
                    },
                    &mut rng
                )
                .is_err());
            assert_eq!(rng.0, 0);
            assert_eq!(p.encode().unwrap(), before);
            assert!(p.sheets[8].verified_by_user && p.sheets[8].unlocked);
        }
        let mut p = near_limit(1240);
        let long = p.sheets[8].dictionary[10].clone();
        let mut rng = CountRandom(0);
        PayloadEditor { payload: &mut p }
            .edit_sheet(8)
            .unwrap()
            .spin_row(
                SpinRequest {
                    row: 0,
                    first_symbol: "0",
                    second_symbol: "0",
                    word: &long,
                },
                &mut rng,
            )
            .unwrap();
        assert_eq!(rng.0, 10);
        assert_eq!(p.sheets[8].rows[0][0], long);
        assert!(!p.sheets[8].verified_by_user);
        assert!(p.encode().unwrap().len() <= crate::format::MAX_PAYLOAD);
    }
    #[test]
    fn protection_is_salted_and_spin_persists_only_current_rows() {
        use crate::{
            sheet::SheetSize,
            spin::{RandomSource, SpinError, SpinRequest},
        };
        struct CountRandom(usize);
        impl RandomSource for CountRandom {
            fn fill(&mut self, bytes: &mut [u8]) -> Result<(), SpinError> {
                self.0 += 1;
                bytes.copy_from_slice(&(1_000_000u32 + self.0 as u32).to_le_bytes());
                Ok(())
            }
        }
        let mut p = Payload::default();
        let words: Vec<_> = (0..80).map(|i| format!("synthetic-{i:03}")).collect();
        let mut editor = PayloadEditor { payload: &mut p };
        editor
            .create_custom_sheet(
                "synthetic",
                SheetSize {
                    rows: 12,
                    columns: 10,
                },
                &words,
            )
            .unwrap();
        editor
            .edit_sheet(0)
            .unwrap()
            .set_protection("synthetic-protection-secret-marker")
            .unwrap();
        let first = p.sheets[0].protection.unwrap();
        PayloadEditor { payload: &mut p }
            .edit_sheet(0)
            .unwrap()
            .set_protection("synthetic-protection-secret-marker")
            .unwrap();
        assert_ne!(first[..16], p.sheets[0].protection.unwrap()[..16]);
        assert_ne!(first[16..], p.sheets[0].protection.unwrap()[16..]);
        for (a, b, word) in [
            ("9", "9", "synthetic-001"),
            ("A", "A", "synthetic-invalid-marker"),
            ("9", "8", "synthetic-001"),
        ] {
            let mut rng = CountRandom(0);
            let mut editor = PayloadEditor { payload: &mut p };
            editor.edit_sheet(0).unwrap().set_verified_by_me(true);
            editor
                .edit_sheet(0)
                .unwrap()
                .spin_row(
                    SpinRequest {
                        row: 0,
                        first_symbol: a,
                        second_symbol: b,
                        word,
                    },
                    &mut rng,
                )
                .unwrap();
            assert_eq!(rng.0, 10);
            assert!(!p.sheets[0].verified_by_user);
            if a == b && a == "9" {
                assert_eq!(p.sheets[0].rows[0][9], "synthetic-001");
            }
            let encoded = p.encode().unwrap();
            for forbidden in [
                b"synthetic-protection-secret-marker".as_slice(),
                b"synthetic-invalid-marker",
            ] {
                assert!(!encoded.windows(forbidden.len()).any(|w| w == forbidden));
            }
            let round = Payload::decode(&encoded).unwrap();
            assert!(!round.sheets[0].unlocked);
            assert_eq!(round.encode().unwrap(), encoded);
            // Independent shape walk: 7 sheet fields, never a candidate/target/
            // validity extension. Only current rows and the salted verifier.
            let mut r = Reader {
                bytes: &encoded,
                offset: 0,
            };
            assert_eq!(r.array(4).unwrap(), 4);
            assert_eq!(r.number(0).unwrap(), 2);
            r.text(256).unwrap();
            r.text(16).unwrap();
            assert_eq!(r.array(32).unwrap(), 1);
            assert_eq!(r.array(7).unwrap(), 7);
            r.text(256).unwrap();
            r.text(128).unwrap();
            r.text(128).unwrap();
            for _ in 0..r.array(8192).unwrap() {
                r.text(128).unwrap();
            }
            for _ in 0..r.array(33).unwrap() {
                for _ in 0..r.array(36).unwrap() {
                    r.text(128).unwrap();
                }
            }
            assert!(!r.boolean().unwrap());
            assert_eq!(r.number(2).unwrap(), 48);
            r.take(48).unwrap();
            assert_eq!(r.offset, encoded.len());
        }
    }
    #[test]
    fn mandatory_protection_schema_requires_v2() {
        assert_eq!(
            &**Payload::default().encode().unwrap(),
            &[0x84, 2, 0x60, 0x60, 0x80]
        );
        assert!(matches!(
            Payload::decode(&[0x84, 1, 0x60, 0x60, 0x80]),
            Err(VaultError::UnsupportedVersion)
        ));
    }
    #[test]
    fn payload_and_sheet_zeroization_clear_owned_data() {
        let mut p = Payload::default();
        p.name = "synthetic-label".into();
        p.locale = "en".into();
        p.sheets.push(Sheet {
            name: "synthetic-sheet".into(),
            profile_id: "synthetic-profile".into(),
            mode_id: "synthetic-mode".into(),
            dictionary: vec!["synthetic-word".into()],
            rows: vec![vec!["synthetic-cell".into(); 10]; 12],
            verified_by_user: true,
            protection: Some([42; 48]),
            unlocked: true,
        });
        p.sheets[0].zeroize();
        assert!(p.sheets[0].name.is_empty());
        assert!(p.sheets[0].dictionary.is_empty());
        assert!(p.sheets[0].rows.is_empty());
        assert!(!p.sheets[0].verified_by_user);
        assert!(!p.sheets[0].unlocked);
        assert!(p.sheets[0]
            .protection
            .as_ref()
            .is_none_or(|v| v.iter().all(|b| *b == 0)));
        p.zeroize();
        assert!(p.name.is_empty());
        assert!(p.locale.is_empty());
        assert!(p.sheets.is_empty());
        // These types own zeroizing destructors; never read freed memory to test Drop.
        assert!(std::mem::needs_drop::<Payload>());
        assert!(std::mem::needs_drop::<Sheet>());
    }
    #[test]
    fn every_collection_and_text_bound_is_enforced() {
        let mut p = Payload::default();
        p.name = "x".repeat(257);
        assert!(p.encode().is_err());
        p.name.clear();
        p.locale = "x".repeat(17);
        assert!(p.encode().is_err());
        p.locale.clear();
        p.sheets = (0..33).map(|_| Sheet::default()).collect();
        assert!(p.encode().is_err());
        p.sheets.truncate(1);
        p.sheets[0].profile_id = "custom".into();
        p.sheets[0].mode_id = "custom".into();
        p.sheets[0].dictionary = (0..40).map(|i| format!("synthetic-{i}")).collect();
        p.sheets[0].rows = vec![p.sheets[0].dictionary[..36].to_vec(); 12];
        assert!(p.encode().is_ok());
        p.sheets[0].name = "x".repeat(257);
        assert!(p.encode().is_err());
        p.sheets[0].name.clear();
        p.sheets[0].profile_id = "x".repeat(129);
        assert!(p.encode().is_err());
        p.sheets[0].profile_id = "custom".into();
        p.sheets[0].mode_id = "x".repeat(129);
        assert!(p.encode().is_err());
        p.sheets[0].mode_id = "custom".into();
        p.sheets[0].dictionary = vec!["synthetic".into(); 8193];
        assert!(p.encode().is_err());
        p.sheets[0].profile_id = "custom".into();
        p.sheets[0].mode_id = "custom".into();
        p.sheets[0].dictionary = (0..40).map(|i| format!("synthetic-{i}")).collect();
        for rows in ROWS {
            p.sheets[0].rows = vec![p.sheets[0].dictionary[..36].to_vec(); *rows];
            assert!(Payload::decode(&p.encode().unwrap()).is_ok());
        }
        p.sheets[0].rows = vec![vec!["synthetic-cell".into(); 36]; 34];
        assert!(p.encode().is_err());
        for prefix in [
            vec![0x84, 2, 0x60, 0x60, 0x99, 0xff, 0xff],
            vec![
                0x84, 2, 0x60, 0x60, 0x81, 0x87, 0x60, 0x60, 0x60, 0x99, 0xff, 0xff,
            ],
        ] {
            assert!(Payload::decode(&prefix).is_err());
        }
    }
    #[test]
    fn canonical_cbor_has_exact_schema_and_rejects_noncanonical_or_unbounded_data() {
        let p = Payload::default();
        assert_eq!(&**p.encode().unwrap(), &[0x84, 2, 0x60, 0x60, 0x80]);
        assert!(Payload::decode(&[0x84, 2, 0x60, 0x60, 0x80]).is_ok());
        for bad in [
            vec![0x84, 0x18, 2, 0x60, 0x60, 0x80],
            vec![0x84, 2, 0x60, 0x60, 0x98, 33],
            vec![0x84, 2, 0x79, 0xff, 0xff],
            vec![0x84, 2, 0x61, 0xff, 0x60, 0x80],
            vec![0x84, 2, 0x60, 0x60, 0x80, 0],
            vec![0x9f, 2, 0x60, 0x60, 0x80, 0xff],
            vec![0x85, 2, 0x60, 0x60, 0x80, 0x60],
        ] {
            assert!(Payload::decode(&bad).is_err());
        }
        for n in 0..5 {
            assert!(Payload::decode(&[0x84, 2, 0x60, 0x60, 0x80][..n]).is_err());
        }
    }
    #[test]
    fn schema_two_custom_collision_snapshot_remains_readable_without_migration() {
        let mut words: Vec<_> = (0..10).map(|i| format!("synthetic-{i:02}")).collect();
        words[0] = "synthetic-Case".into();
        words[1] = "synthetic-case".into();
        words[2] = "synthetic-re\u{301}sume\u{301}".into();
        words[3] = "synthetic-resume".into();
        let mut writer = Writer {
            bytes: Some(Zeroizing::new(Vec::new())),
            len: 0,
        };
        writer.array(4, 4).unwrap();
        writer.number(0, 2).unwrap();
        writer.text("synthetic-vault", 256).unwrap();
        writer.text("en", 16).unwrap();
        writer.array(1, 32).unwrap();
        writer.array(7, 7).unwrap();
        writer.text("legacy-custom", 256).unwrap();
        writer.text("custom", 128).unwrap();
        writer.text("custom", 128).unwrap();
        writer.array(words.len(), 8192).unwrap();
        for word in &words {
            writer.text(word, 128).unwrap();
        }
        writer.array(12, 33).unwrap();
        for _ in 0..12 {
            writer.array(words.len(), 36).unwrap();
            for word in &words {
                writer.text(word, 128).unwrap();
            }
        }
        writer.push(&[0xf4]).unwrap();
        writer.number(2, 0).unwrap();
        let encoded = writer.bytes.unwrap();

        let decoded = Payload::decode(&encoded).unwrap();
        assert_eq!(decoded.sheets[0].dictionary, words);
        assert_eq!(&*decoded.encode().unwrap(), &*encoded);
    }
    #[test]
    fn bounded_tables_roundtrip_without_secret_metadata() {
        let mut p = Payload::default();
        p.rename("synthetic table").unwrap();
        p.locale = "ru".into();
        p.sheets.push(Sheet {
            name: "synthetic".into(),
            profile_id: "custom".into(),
            mode_id: "custom".into(),
            dictionary: (0..40).map(|i| format!("synthetic-{i}")).collect(),
            rows: vec![(0..10).map(|i| format!("synthetic-{i}")).collect(); 12],
            verified_by_user: false,
            protection: Some([42; 48]),
            unlocked: true,
        });
        let encoded = p.encode().unwrap();
        let round = Payload::decode(&encoded).unwrap();
        assert_eq!(round.name(), "synthetic table");
        assert_eq!(round.sheets[0].rows.len(), 12);
        assert_eq!(round.sheets[0].rows[0][0], "synthetic-0");
        assert_eq!(round.encode().unwrap(), encoded);
        p.sheets[0].rows[0].push("extra".into());
        assert!(p.encode().is_err());
        p.sheets[0].rows.clear();
        p.sheets[0].dictionary = vec!["x".repeat(129)];
        assert!(p.encode().is_err());
    }

    #[test]
    fn locale_access_is_en_ru_only_bounded_and_schema_two_roundtrips() {
        let mut p = Payload::default();
        let before = p.encode().unwrap();
        {
            let mut editor = PayloadEditor { payload: &mut p };
            assert_eq!(editor.locale(), "");
            assert!(editor.set_locale("de").is_err());
            assert_eq!(editor.locale(), "");
            assert!(editor.set_locale("en").unwrap());
            assert!(!editor.set_locale("en").unwrap());
            assert_eq!(editor.locale(), "en");
            assert!(editor.set_locale("ru").unwrap());
        }
        assert_ne!(p.encode().unwrap(), before);
        let encoded = p.encode().unwrap();
        let mut round = Payload::decode(&encoded).unwrap();
        let editor = PayloadEditor {
            payload: &mut round,
        };
        assert_eq!(editor.locale(), "ru");
        assert_eq!(round.encode().unwrap(), encoded);

        let mut full = near_limit(0);
        let locale_bytes = full.locale.len();
        assert!((1..24).contains(&locale_bytes));
        full.locale.clear();
        full.sheets[1].name = "n".repeat(locale_bytes);
        assert_eq!(full.encode().unwrap().len(), crate::format::MAX_PAYLOAD);
        assert!(PayloadEditor { payload: &mut full }
            .set_locale("en")
            .is_err());
        assert!(full.locale.is_empty());
        assert_eq!(full.encode().unwrap().len(), crate::format::MAX_PAYLOAD);
    }
}
