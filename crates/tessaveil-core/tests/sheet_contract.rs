#![cfg(windows)]
use tessaveil_core::{sheet::SheetSize, CreateOptions, StoragePolicy, VaultService};

fn words() -> Vec<String> {
    (0..80).map(|i| format!("synthetic-{i:03}")).collect()
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
