#![cfg(windows)]
use tessaveil_core::{
    sheet::SheetSize,
    spin::{OsRandom, RandomSource, SpinError, SpinRequest},
    CreateOptions, StoragePolicy, VaultService,
};

struct FailingRandom;
struct FixedRandom;
impl RandomSource for FixedRandom {
    fn fill(&mut self, bytes: &mut [u8]) -> Result<(), SpinError> {
        bytes.copy_from_slice(&1_000_000u32.to_le_bytes());
        Ok(())
    }
}
impl RandomSource for FailingRandom {
    fn fill(&mut self, _: &mut [u8]) -> Result<(), SpinError> {
        Err(SpinError)
    }
}

#[test]
fn valid_and_invalid_input_replace_the_full_row_with_same_public_transition() {
    let dir = tempfile::tempdir().unwrap();
    let mut vault = VaultService::create(
        dir.path().join("synthetic.tessaveil-alpha"),
        "synthetic-master-password",
        CreateOptions {
            storage: StoragePolicy::DevelopmentLocalNtfs,
            ..Default::default()
        },
    )
    .unwrap();
    let mut p = vault.payload_mut().unwrap();
    let words: Vec<_> = (0..80).map(|i| format!("synthetic-{i:03}")).collect();
    let id = p
        .create_custom_sheet(
            "synthetic",
            SheetSize {
                rows: 12,
                columns: 36,
            },
            &words,
        )
        .unwrap();
    for (first, second, word, expected) in [
        ("A", "A", "synthetic-001", true),
        ("A", "B", "synthetic-001", false),
        ("A", "A", "synthetic-invalid-input-marker", false),
        ("А", "А", "synthetic-001", false),
        ("", "", "synthetic-001", false),
    ] {
        let before = p.sheet(id).unwrap().row(0).unwrap().to_vec();
        p.edit_sheet(id).unwrap().set_verified_by_me(true);
        {
            let mut editor = p.edit_sheet(id).unwrap();
            let replacement = editor
                .spin_row(
                    SpinRequest {
                        row: 0,
                        first_symbol: first,
                        second_symbol: second,
                        word,
                    },
                    &mut OsRandom,
                )
                .unwrap();
            assert_eq!(replacement.words().len(), 36);
            assert!(replacement.words().iter().all(|w| words.contains(w)));
            assert_eq!(
                replacement
                    .words()
                    .iter()
                    .collect::<std::collections::HashSet<_>>()
                    .len(),
                36
            );
            if expected {
                assert_eq!(replacement.words()[10], "synthetic-001");
            }
        }
        let after = p.sheet(id).unwrap();
        assert_ne!(after.row(0).unwrap(), before);
        assert!(!after.verified_by_me());
        assert!(!after.is_protected());
    }
    let before = p.sheet(id).unwrap().row(0).unwrap().to_vec();
    assert!(p
        .edit_sheet(id)
        .unwrap()
        .spin_row(
            SpinRequest {
                row: 0,
                first_symbol: "A",
                second_symbol: "A",
                word: "synthetic-001"
            },
            &mut FailingRandom
        )
        .is_err());
    assert_eq!(p.sheet(id).unwrap().row(0).unwrap(), before);
    let mut accented = words;
    accented[0] = "synthetic-é".into();
    let custom = p
        .create_custom_sheet(
            "unicode",
            SheetSize {
                rows: 12,
                columns: 10,
            },
            &accented,
        )
        .unwrap();
    let mut editor = p.edit_sheet(custom).unwrap();
    let row = editor
        .spin_row(
            SpinRequest {
                row: 0,
                first_symbol: "1",
                second_symbol: "1",
                word: "synthetic-é",
            },
            &mut FixedRandom,
        )
        .unwrap();
    assert_eq!(row.words()[1], "synthetic-e\u{301}");
}
