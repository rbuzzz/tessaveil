#![cfg(windows)]
use tessaveil_core::{catalog, sheet::SheetSize, CreateOptions, StoragePolicy, VaultService};

fn words() -> Vec<String> {
    (0..80).map(|i| format!("synthetic-{i:03}")).collect()
}

#[test]
fn every_selectable_exact_profile_accepts_each_allowed_length_and_column_mode() {
    let dir = tempfile::tempdir().unwrap();
    let path = dir.path().join("profile-lengths.tessaveil-alpha");
    let mut vault = VaultService::create(
        path,
        "synthetic-master-password",
        CreateOptions {
            storage: StoragePolicy::DevelopmentLocalNtfs,
            ..Default::default()
        },
    )
    .unwrap();
    let mut payload = vault.payload_mut().unwrap();
    let selectable: Vec<_> = catalog::profiles()
        .unwrap()
        .iter()
        .filter(|profile| profile.selectable())
        .collect();
    assert_eq!(selectable.len(), 3);

    for profile in selectable {
        for &rows in profile.supported_lengths() {
            for columns in [10, 36] {
                let index = payload
                    .create_profile_sheet(
                        "synthetic-profile-sheet",
                        profile.id(),
                        profile.mode(),
                        SheetSize { rows, columns },
                    )
                    .unwrap();
                let sheet = payload.sheet(index).unwrap();
                assert_eq!(sheet.profile_id(), profile.id());
                assert_eq!(sheet.mode_id(), profile.mode());
                assert_eq!(sheet.row_count(), rows);
                assert_eq!(sheet.row(0).unwrap().len(), columns);
            }
        }
        let unsupported = [12, 13, 15, 16, 18, 20, 21, 25, 26, 27, 28, 29, 33]
            .into_iter()
            .find(|rows| !profile.supported_lengths().contains(rows))
            .unwrap();
        assert!(payload
            .create_profile_sheet(
                "unsupported",
                profile.id(),
                profile.mode(),
                SheetSize {
                    rows: unsupported,
                    columns: 10,
                },
            )
            .is_err());
    }
}

#[test]
fn custom_dictionary_rejects_case_and_diacritic_comparison_collisions() {
    let dir = tempfile::tempdir().unwrap();
    let path = dir.path().join("comparison-collisions.tessaveil-alpha");
    let mut vault = VaultService::create(
        path,
        "synthetic-master-password",
        CreateOptions {
            storage: StoragePolicy::DevelopmentLocalNtfs,
            ..Default::default()
        },
    )
    .unwrap();
    let mut payload = vault.payload_mut().unwrap();
    for (first, second) in [
        ("synthetic-Case", "synthetic-case"),
        ("synthetic-résumé", "synthetic-resume"),
    ] {
        let mut dictionary = words();
        dictionary[0] = first.into();
        dictionary[1] = second.into();
        assert!(payload
            .create_custom_sheet(
                "collision",
                SheetSize {
                    rows: 12,
                    columns: 10,
                },
                &dictionary,
            )
            .is_err());
        assert_eq!(payload.sheet_count(), 0);
    }
}

#[test]
fn replacement_dictionary_requires_unlocked_source_and_inherits_no_mutable_state() {
    let dir = tempfile::tempdir().unwrap();
    let path = dir.path().join("replacement.tessaveil-alpha");
    let mut vault = VaultService::create(
        path,
        "synthetic-master-password",
        CreateOptions {
            storage: StoragePolicy::DevelopmentLocalNtfs,
            ..Default::default()
        },
    )
    .unwrap();
    let mut payload = vault.payload_mut().unwrap();
    let source = payload
        .create_custom_sheet(
            "source",
            SheetSize {
                rows: 12,
                columns: 10,
            },
            &words(),
        )
        .unwrap();
    payload.edit_sheet(source).unwrap().set_verified_by_me(true);
    payload
        .edit_sheet(source)
        .unwrap()
        .set_protection("synthetic-sheet-password")
        .unwrap();
    payload.protect_sheet(source).unwrap();
    let replacement_words: Vec<_> = (0..80)
        .map(|index| format!("replacement-{index:03}"))
        .collect();
    let source_name = payload.sheet(source).unwrap().name().to_owned();
    let source_dictionary = payload.sheet(source).unwrap().dictionary().to_vec();
    let source_rows: Vec<_> = (0..12)
        .map(|row| payload.sheet(source).unwrap().row(row).unwrap().to_vec())
        .collect();
    assert!(payload
        .new_dictionary_sheet(source, "replacement", &replacement_words)
        .is_err());
    assert_eq!(payload.sheet_count(), 1);
    assert_eq!(payload.sheet(source).unwrap().name(), source_name);
    assert_eq!(
        payload.sheet(source).unwrap().dictionary(),
        source_dictionary
    );
    for (row, expected) in source_rows.iter().enumerate() {
        assert_eq!(payload.sheet(source).unwrap().row(row).unwrap(), expected);
    }

    payload
        .unlock_sheet(source, "synthetic-sheet-password")
        .unwrap();
    let replacement = payload
        .new_dictionary_sheet(source, "replacement", &replacement_words)
        .unwrap();
    let original = payload.sheet(source).unwrap();
    assert_eq!(original.name(), source_name);
    assert_eq!(original.dictionary(), source_dictionary);
    assert!(original.verified_by_me());
    assert!(original.has_sheet_password());
    assert!(!original.is_protected());
    for (row, expected) in source_rows.iter().enumerate() {
        assert_eq!(original.row(row).unwrap(), expected);
    }
    let replacement = payload.sheet(replacement).unwrap();
    assert_eq!(replacement.name(), "replacement");
    assert_eq!(replacement.profile_id(), "custom");
    assert_eq!(replacement.mode_id(), "custom");
    assert_eq!(replacement.dictionary(), replacement_words);
    assert!(!replacement.verified_by_me());
    assert!(!replacement.has_sheet_password());
    assert!(!replacement.is_protected());
    assert!(replacement
        .row(0)
        .unwrap()
        .iter()
        .all(|word| word.starts_with("replacement-")));
}

#[test]
fn dimensions_snapshot_verification_and_protection_survive_roundtrip() {
    let dir = tempfile::tempdir().unwrap();
    let path = dir.path().join("synthetic.tessaveil-alpha");
    let mut vault = VaultService::create(
        &path,
        "synthetic-master-password",
        CreateOptions {
            storage: StoragePolicy::DevelopmentLocalNtfs,
            ..Default::default()
        },
    )
    .unwrap();
    {
        let mut p = vault.payload_mut().unwrap();
        let mut dictionary = words();
        for rows in [12, 13, 15, 16, 18, 20, 21, 24, 25, 26, 27, 28, 29, 33] {
            for columns in [10, 36] {
                let id = p
                    .create_custom_sheet("synthetic", SheetSize { rows, columns }, &dictionary)
                    .unwrap();
                let sheet = p.sheet(id).unwrap();
                assert_eq!(sheet.row_count(), rows);
                assert!(!sheet.verified_by_me());
                for r in 0..rows {
                    let row = sheet.row(r).unwrap();
                    assert_eq!(row.len(), columns);
                    assert_eq!(
                        row.iter().collect::<std::collections::HashSet<_>>().len(),
                        columns
                    );
                    assert!(row.iter().all(|w| dictionary.contains(w)));
                }
            }
        }
        for size in [
            SheetSize {
                rows: 11,
                columns: 10,
            },
            SheetSize {
                rows: 24,
                columns: 11,
            },
        ] {
            assert!(p.create_custom_sheet("invalid", size, &dictionary).is_err());
        }
        p.edit_sheet(0).unwrap().set_verified_by_me(true);
        p.edit_sheet(0)
            .unwrap()
            .set_protection("synthetic-sheet-password")
            .unwrap();
        dictionary[0] = "synthetic-revised".into();
        let new_id = p.new_dictionary_sheet(0, "revised", &dictionary).unwrap();
        assert_eq!(new_id, 28);
        assert!(p.sheet(0).unwrap().verified_by_me());
        assert_eq!(p.sheet(0).unwrap().dictionary()[0], "synthetic-000");
        assert!(!p.sheet(new_id).unwrap().verified_by_me());
        assert!(!p.sheet(new_id).unwrap().has_sheet_password());
        assert_eq!(
            p.sheet(new_id).unwrap().dictionary()[0],
            "synthetic-revised"
        );
        p.protect_sheet(0).unwrap();
        assert!(p.edit_sheet(0).is_err());
        assert!(p.unlock_sheet(0, "synthetic-wrong-password").is_err());
        p.unlock_sheet(0, "synthetic-sheet-password").unwrap();
        assert!(p.edit_sheet(0).is_ok());
        assert!(p
            .create_custom_sheet(
                "invalid",
                SheetSize {
                    rows: 12,
                    columns: 36
                },
                &words()[..35]
            )
            .is_err());
        let mut duplicate = words();
        duplicate[1] = duplicate[0].clone();
        assert!(p
            .create_custom_sheet(
                "invalid",
                SheetSize {
                    rows: 12,
                    columns: 10
                },
                &duplicate
            )
            .is_err());
        let mut collisions = words();
        collisions[0] = "synthetic-é".into();
        collisions[1] = "synthetic-e\u{301}".into();
        assert!(p
            .create_custom_sheet(
                "invalid",
                SheetSize {
                    rows: 12,
                    columns: 10
                },
                &collisions
            )
            .is_err());
        for bad in ["", "synthetic word", "synthetic\0word"] {
            let mut invalid = words();
            invalid[0] = bad.into();
            assert!(p
                .create_custom_sheet(
                    "invalid",
                    SheetSize {
                        rows: 12,
                        columns: 10
                    },
                    &invalid
                )
                .is_err());
        }
        assert!(p
            .create_profile_sheet(
                "invalid",
                "tonhub",
                "wrong-mode",
                SheetSize {
                    rows: 24,
                    columns: 10
                }
            )
            .is_err());
        assert!(p
            .create_profile_sheet(
                "invalid",
                "tonhub",
                "ton-native-generated",
                SheetSize {
                    rows: 12,
                    columns: 10
                }
            )
            .is_err());
        for _ in 0..3 {
            p.create_custom_sheet(
                "synthetic",
                SheetSize {
                    rows: 12,
                    columns: 10,
                },
                &words(),
            )
            .unwrap();
        }
        assert!(p
            .create_custom_sheet(
                "too-many",
                SheetSize {
                    rows: 12,
                    columns: 10
                },
                &words()
            )
            .is_err());
    }
    vault.set_storage_policy(StoragePolicy::ReadOnly);
    assert!(vault.save().is_err());
    assert!(vault.payload_mut().unwrap().edit_sheet(0).is_ok());
    vault.set_storage_policy(StoragePolicy::DevelopmentLocalNtfs);
    vault.save().unwrap();
    assert!(vault.payload_mut().unwrap().edit_sheet(0).is_err());
    vault.lock();
    let mut reopened = VaultService::open(&path, "synthetic-master-password").unwrap();
    assert!(reopened.payload_mut().unwrap().edit_sheet(0).is_err());
    reopened
        .payload_mut()
        .unwrap()
        .unlock_sheet(0, "synthetic-sheet-password")
        .unwrap();
    assert!(reopened
        .payload_mut()
        .unwrap()
        .sheet(0)
        .unwrap()
        .verified_by_me());
    assert!(reopened
        .unlock_sheet_with_master(28, "synthetic-wrong-password")
        .is_err());
    assert!(reopened.payload_mut().unwrap().edit_sheet(28).is_err());
    reopened
        .unlock_sheet_with_master(28, "synthetic-master-password")
        .unwrap();
    assert!(reopened.payload_mut().unwrap().edit_sheet(28).is_ok());
    reopened.lock();
    assert!(reopened.payload_mut().is_err());
}
