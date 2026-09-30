//! One row in, one full replacement row out. Input validity is never returned.
use crate::sheet::SheetEditor;
use unicode_normalization::UnicodeNormalization;
use zeroize::Zeroizing;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct SpinError;
impl std::fmt::Display for SpinError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.write_str("The row could not be replaced.")
    }
}
impl std::error::Error for SpinError {}

/// Callers must supply cryptographic randomness. The UI uses only OsRandom;
/// dependency injection permits deterministic tests and entropy-failure tests.
pub trait RandomSource {
    fn fill(&mut self, bytes: &mut [u8]) -> Result<(), SpinError>;
}
pub struct OsRandom;
impl RandomSource for OsRandom {
    fn fill(&mut self, bytes: &mut [u8]) -> Result<(), SpinError> {
        getrandom::getrandom(bytes).map_err(|_| SpinError)
    }
}
pub struct SpinRequest<'a> {
    pub row: usize,
    pub first_symbol: &'a str,
    pub second_symbol: &'a str,
    pub word: &'a str,
}
/// Borrowed from the current sheet; cannot retain an independent prior row owner.
pub struct ReplacementRow<'a>(&'a [String]);
impl ReplacementRow<'_> {
    pub fn words(&self) -> &[String] {
        self.0
    }
}

fn uniform(upper: usize, rng: &mut impl RandomSource) -> Result<usize, SpinError> {
    let upper = upper as u32;
    let threshold = upper.wrapping_neg() % upper;
    // Bound even a broken/custom RNG. Rejection is independent of user inputs.
    for _ in 0..128 {
        let mut bytes = Zeroizing::new([0; 4]);
        rng.fill(&mut *bytes)?;
        let n = u32::from_le_bytes(*bytes);
        if n >= threshold {
            return Ok((n % upper) as usize);
        }
    }
    Err(SpinError)
}
pub(crate) fn generate_row(
    dictionary: &[String],
    columns: usize,
    rng: &mut impl RandomSource,
) -> Result<Zeroizing<Vec<String>>, SpinError> {
    if dictionary.len() < columns || columns == 0 {
        return Err(SpinError);
    }
    let mut indices: Vec<usize> = (0..dictionary.len()).collect();
    let mut row = Zeroizing::new(Vec::with_capacity(columns));
    for i in 0..columns {
        let j = i + uniform(dictionary.len() - i, rng)?;
        indices.swap(i, j);
        row.push(dictionary[indices[i]].clone());
    }
    Ok(row)
}
fn normalized_word(input: &str) -> Option<Zeroizing<String>> {
    if input.len() > 128 {
        return None;
    }
    let mut word = Zeroizing::new(String::with_capacity(128));
    for ch in input.nfkd() {
        if word.len() + ch.len_utf8() > 128 {
            return None;
        }
        word.push(ch);
    }
    Some(word)
}
impl SheetEditor<'_> {
    pub fn spin_row(
        &mut self,
        request: SpinRequest<'_>,
        rng: &mut impl RandomSource,
    ) -> Result<ReplacementRow<'_>, SpinError> {
        let columns = self.sheet.rows.get(request.row).ok_or(SpinError)?.len();
        // Identical random work and public transition for every candidate.
        let mut row = generate_row(&self.sheet.dictionary, columns, rng)?;
        let alphabet = b"0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ";
        let symbol = request.first_symbol.as_bytes();
        let normalized = normalized_word(request.word);
        if symbol.len() == 1
            && request.first_symbol == request.second_symbol
            && request.word.len() <= 128
        {
            if let (Some(column), Some(word)) = (
                alphabet[..columns].iter().position(|b| *b == symbol[0]),
                self.sheet.dictionary.iter().find(|w| {
                    normalized
                        .as_ref()
                        .is_some_and(|input| w.as_str() == input.as_str())
                }),
            ) {
                // Preserve within-row uniqueness without extra RNG or a side flag.
                if let Some(existing) = row.iter().position(|w| w == word) {
                    row.swap(existing, column);
                } else {
                    use zeroize::Zeroize;
                    row[column].zeroize();
                    row[column] = word.clone();
                }
            }
        }
        use zeroize::Zeroize;
        self.sheet.rows[request.row].zeroize();
        self.sheet.rows[request.row] = std::mem::take(&mut *row);
        self.sheet.verified_by_user = false;
        Ok(ReplacementRow(&self.sheet.rows[request.row]))
    }
}
