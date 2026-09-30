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
    pub(crate) dictionary: Vec<String>,
    pub(crate) rows: Vec<Vec<String>>,
    pub(crate) verified_by_user: bool,
    pub(crate) protected: bool,
}
impl Payload {
    pub fn name(&self) -> &str {
        &self.name
    }
    pub fn rename(&mut self, name: &str) -> Result<(), VaultError> {
        if name.len() > 256 {
            return Err(VaultError::InvalidPayload);
        }
        self.name.zeroize();
        self.name = name.to_owned();
        Ok(())
    }
    pub(crate) fn encode(&self) -> Result<Zeroizing<Vec<u8>>, VaultError> {
        let mut w = Writer(Zeroizing::new(Vec::with_capacity(
            crate::format::MAX_PAYLOAD,
        )));
        w.number(4, 4)?;
        w.number(0, 1)?;
        w.text(&self.name, 256)?;
        w.text(&self.locale, 16)?;
        w.array(self.sheets.len(), 32)?;
        for s in &self.sheets {
            w.array(6, 6)?;
            w.text(&s.name, 256)?;
            w.text(&s.profile_id, 128)?;
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
            w.push(&[
                if s.verified_by_user { 0xf5 } else { 0xf4 },
                if s.protected { 0xf5 } else { 0xf4 },
            ])?;
        }
        Ok(w.0)
    }
    pub(crate) fn decode(bytes: &[u8]) -> Result<Self, VaultError> {
        if bytes.len() > crate::format::MAX_PAYLOAD {
            return Err(VaultError::InvalidPayload);
        }
        let mut r = Reader { bytes, offset: 0 };
        // Recognize the canonical, bounded envelope of the schema before imposing
        // v1's arity: a future mandatory field changes arity together with version.
        let arity = r.array(65535)?;
        if arity == 0 {
            return Err(VaultError::InvalidPayload);
        }
        if r.number(0)? != 1 {
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
            if r.array(6)? != 6 {
                return Err(VaultError::InvalidPayload);
            }
            let mut s = Sheet::default();
            s.name = r.text(256)?;
            s.profile_id = r.text(128)?;
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
            s.protected = r.boolean()?;
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
}
const ROWS: &[usize] = &[12, 13, 15, 16, 18, 20, 21, 24, 25, 26, 27, 28, 29, 33];
struct Writer(Zeroizing<Vec<u8>>);
impl Writer {
    fn push(&mut self, bytes: &[u8]) -> Result<(), VaultError> {
        if bytes.len() > crate::format::MAX_PAYLOAD - self.0.len() {
            return Err(VaultError::InvalidPayload);
        }
        self.0.extend_from_slice(bytes);
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
    #[test]
    fn payload_and_sheet_zeroization_clear_owned_data() {
        let mut p = Payload::default();
        p.name = "synthetic-label".into();
        p.locale = "en".into();
        p.sheets.push(Sheet {
            name: "synthetic-sheet".into(),
            profile_id: "synthetic-profile".into(),
            dictionary: vec!["synthetic-word".into()],
            rows: vec![vec!["synthetic-cell".into(); 10]; 12],
            verified_by_user: true,
            protected: true,
        });
        p.sheets[0].zeroize();
        assert!(p.sheets[0].name.is_empty());
        assert!(p.sheets[0].dictionary.is_empty());
        assert!(p.sheets[0].rows.is_empty());
        assert!(!p.sheets[0].verified_by_user);
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
        p.sheets[0].name = "x".repeat(257);
        assert!(p.encode().is_err());
        p.sheets[0].name.clear();
        p.sheets[0].profile_id = "x".repeat(129);
        assert!(p.encode().is_err());
        p.sheets[0].profile_id.clear();
        p.sheets[0].dictionary = vec!["synthetic".into(); 8193];
        assert!(p.encode().is_err());
        p.sheets[0].dictionary.truncate(8192);
        for rows in ROWS {
            p.sheets[0].rows = vec![vec!["synthetic-cell".into(); 36]; *rows];
            assert!(Payload::decode(&p.encode().unwrap()).is_ok());
        }
        p.sheets[0].rows = vec![vec!["synthetic-cell".into(); 36]; 34];
        assert!(p.encode().is_err());
        for prefix in [
            vec![0x84, 1, 0x60, 0x60, 0x99, 0xff, 0xff],
            vec![
                0x84, 1, 0x60, 0x60, 0x81, 0x86, 0x60, 0x60, 0x99, 0xff, 0xff,
            ],
        ] {
            assert!(Payload::decode(&prefix).is_err());
        }
    }
    #[test]
    fn canonical_cbor_has_exact_schema_and_rejects_noncanonical_or_unbounded_data() {
        let p = Payload::default();
        assert_eq!(&**p.encode().unwrap(), &[0x84, 1, 0x60, 0x60, 0x80]);
        assert!(Payload::decode(&[0x84, 1, 0x60, 0x60, 0x80]).is_ok());
        for bad in [
            vec![0x84, 0x18, 1, 0x60, 0x60, 0x80],
            vec![0x84, 1, 0x60, 0x60, 0x98, 33],
            vec![0x84, 1, 0x79, 0xff, 0xff],
            vec![0x84, 1, 0x61, 0xff, 0x60, 0x80],
            vec![0x84, 1, 0x60, 0x60, 0x80, 0],
            vec![0x9f, 1, 0x60, 0x60, 0x80, 0xff],
            vec![0x85, 1, 0x60, 0x60, 0x80, 0x60],
        ] {
            assert!(Payload::decode(&bad).is_err());
        }
        for n in 0..5 {
            assert!(Payload::decode(&[0x84, 1, 0x60, 0x60, 0x80][..n]).is_err());
        }
    }
    #[test]
    fn bounded_tables_roundtrip_without_secret_metadata() {
        let mut p = Payload::default();
        p.rename("synthetic table").unwrap();
        p.locale = "ru".into();
        p.sheets.push(Sheet {
            name: "synthetic".into(),
            profile_id: "synthetic-only".into(),
            dictionary: (0..40).map(|i| format!("synthetic-{i}")).collect(),
            rows: vec![vec!["synthetic-cell".into(); 10]; 12],
            verified_by_user: false,
            protected: true,
        });
        let encoded = p.encode().unwrap();
        let round = Payload::decode(&encoded).unwrap();
        assert_eq!(round.name(), "synthetic table");
        assert_eq!(round.sheets[0].rows.len(), 12);
        assert_eq!(round.sheets[0].rows[0][0], "synthetic-cell");
        assert_eq!(round.encode().unwrap(), encoded);
        p.sheets[0].rows[0].push("extra".into());
        assert!(p.encode().is_err());
        p.sheets[0].rows.clear();
        p.sheets[0].dictionary = vec!["x".repeat(129)];
        assert!(p.encode().is_err());
    }
}
