#![cfg(windows)]
use std::time::{Duration, Instant};
use tessaveil_windows_controller::*;
fn call(c: &mut Controller, op: u32, a: u32, b: u32, s: [&str; 4]) -> Result<String, String> {
    c.run(op, a, b, s, Instant::now())
}
fn blank(c: &mut Controller, op: u32) -> Result<String, String> {
    call(c, op, 0, 0, [""; 4])
}
fn setup(c: &mut Controller, path: &str) {
    blank(c, ACK).unwrap();
    call(
        c,
        CREATE,
        0,
        0,
        [path, "synthetic-master-password", "synthetic-vault", ""],
    )
    .unwrap();
}

#[test]
fn profile_length_query_preserves_profile_shape_and_add_honors_requested_length() {
    const PROFILE_LENGTHS_OP: u32 = 24;
    let d = tempfile::tempdir().unwrap();
    let p = d.path().join("profile-lengths.tessaveil-alpha");
    let mut c = Controller::default();
    setup(&mut c, p.to_str().unwrap());
    let profile_count = blank(&mut c, PROFILE_COUNT)
        .unwrap()
        .parse::<u32>()
        .unwrap();
    let mut selectable = Vec::new();
    for index in 0..profile_count {
        let fields: Vec<_> = call(&mut c, PROFILE, index, 0, [""; 4])
            .unwrap()
            .split('\t')
            .map(str::to_owned)
            .collect();
        assert_eq!(fields.len(), 5, "PROFILE reply shape changed");
        if fields[0] == "1" {
            selectable.push(index);
        }
    }
    assert_eq!(selectable.len(), 3);
    let unsupported_profile = selectable[0];

    for profile in selectable {
        let lengths = call(&mut c, PROFILE_LENGTHS_OP, profile, 0, [""; 4]).unwrap();
        assert_eq!(lengths, "24");
        for length in lengths.split(',') {
            for columns in [10, 36] {
                call(
                    &mut c,
                    ADD,
                    profile,
                    columns,
                    ["synthetic-sheet", length, "", ""],
                )
                .unwrap();
                assert_eq!(c.state().rows, length.parse::<u32>().unwrap());
                assert_eq!(c.state().columns, columns);
            }
        }
    }
    let before = c.state().sheets;
    assert!(call(
        &mut c,
        ADD,
        unsupported_profile,
        10,
        ["unsupported-length", "12", "", ""]
    )
    .is_err());
    assert_eq!(c.state().sheets, before);
    assert_eq!(c.state().dirty, 1);
}

#[test]
fn custom_dictionary_file_import_is_bounded_normalized_and_recoverable() {
    const ADD_CUSTOM_OP: u32 = 25;
    const MAX_CUSTOM_DICTIONARY_BYTES: usize = 1_056_771;
    let d = tempfile::tempdir().unwrap();
    let vault_path = d.path().join("custom-import.tessaveil-alpha");
    let mut c = Controller::default();
    setup(&mut c, vault_path.to_str().unwrap());

    let write = |name: &str, bytes: &[u8]| {
        let path = d.path().join(name);
        std::fs::write(&path, bytes).unwrap();
        path
    };
    let dictionary = |count: usize, separator: &str| {
        (0..count)
            .map(|index| format!("synthetic-{index:04}"))
            .collect::<Vec<_>>()
            .join(separator)
    };

    let lf = write("valid-lf.txt", dictionary(40, "\n").as_bytes());
    call(
        &mut c,
        ADD_CUSTOM_OP,
        12,
        10,
        ["custom-lf", lf.to_str().unwrap(), "", ""],
    )
    .unwrap();
    assert_eq!(c.state().rows, 12);
    assert_eq!(c.state().columns, 10);

    let mut bom_crlf = b"\xef\xbb\xbf".to_vec();
    bom_crlf.extend_from_slice(dictionary(40, "\r\n").as_bytes());
    bom_crlf.extend_from_slice(b"\r\n");
    let bom_crlf = write("valid-bom-crlf.txt", &bom_crlf);
    call(
        &mut c,
        ADD_CUSTOM_OP,
        13,
        36,
        ["custom-crlf", bom_crlf.to_str().unwrap(), "", ""],
    )
    .unwrap();
    let mut boundary_dictionary: Vec<_> = (0..40)
        .map(|index| format!("boundary-{index:04}"))
        .collect();
    boundary_dictionary[0] = "x".repeat(128);
    let boundary = write(
        "valid-128-byte-word.txt",
        boundary_dictionary.join("\n").as_bytes(),
    );
    call(
        &mut c,
        ADD_CUSTOM_OP,
        12,
        10,
        ["custom-boundary", boundary.to_str().unwrap(), "", ""],
    )
    .unwrap();
    blank(&mut c, SAVE).unwrap();
    assert_eq!(c.state().dirty, 0);
    assert_eq!(blank(&mut c, SHEET_NAME).unwrap(), "custom-lf");
    assert_eq!(
        call(&mut c, SHEET_NAME, 1, 0, [""; 4]).unwrap(),
        "custom-crlf"
    );
    call(&mut c, SELECT, 1, 0, [""; 4]).unwrap();

    let mut invalid_cases: Vec<(&str, Vec<u8>, u32)> = vec![
        ("invalid-utf8.txt", vec![0xff], 10),
        (
            "stray-cr.txt",
            dictionary(40, "\n").replacen('\n', "\r", 1).into_bytes(),
            10,
        ),
        (
            "lone-trailing-cr.txt",
            format!("{}\r", dictionary(40, "\n")).into_bytes(),
            10,
        ),
        (
            "blank-line.txt",
            dictionary(40, "\n").replacen('\n', "\n\n", 1).into_bytes(),
            10,
        ),
        (
            "nul.txt",
            dictionary(40, "\n")
                .replacen("synthetic-0000", "synthetic\0word", 1)
                .into_bytes(),
            10,
        ),
        (
            "whitespace.txt",
            dictionary(40, "\n")
                .replacen("synthetic-0000", "synthetic word", 1)
                .into_bytes(),
            10,
        ),
        ("too-few-10.txt", dictionary(9, "\n").into_bytes(), 10),
        ("too-few-36.txt", dictionary(35, "\n").into_bytes(), 36),
        ("too-many.txt", dictionary(8193, "\n").into_bytes(), 10),
        (
            "raw-word-too-long.txt",
            dictionary(40, "\n")
                .replacen("synthetic-0000", &"x".repeat(129), 1)
                .into_bytes(),
            10,
        ),
        (
            "normalized-word-too-long.txt",
            dictionary(40, "\n")
                .replacen("synthetic-0000", &"é".repeat(43), 1)
                .into_bytes(),
            10,
        ),
        (
            "nfkd-collision.txt",
            dictionary(40, "\n")
                .replacen("synthetic-0000", "synthetic-é", 1)
                .replacen("synthetic-0001", "synthetic-e\u{301}", 1)
                .into_bytes(),
            10,
        ),
        (
            "case-collision.txt",
            dictionary(40, "\n")
                .replacen("synthetic-0000", "synthetic-Case", 1)
                .replacen("synthetic-0001", "synthetic-case", 1)
                .into_bytes(),
            10,
        ),
        (
            "diacritic-collision.txt",
            dictionary(40, "\n")
                .replacen("synthetic-0000", "synthetic-résumé", 1)
                .replacen("synthetic-0001", "synthetic-resume", 1)
                .into_bytes(),
            10,
        ),
        (
            "stray-bom.txt",
            dictionary(40, "\n")
                .replacen("synthetic-0001", "\u{feff}synthetic-0001", 1)
                .into_bytes(),
            10,
        ),
    ];
    invalid_cases.push((
        "over-byte-cap.txt",
        vec![b'x'; MAX_CUSTOM_DICTIONARY_BYTES + 1],
        10,
    ));
    for (name, bytes, columns) in invalid_cases {
        let path = write(name, &bytes);
        let before = c.state();
        assert!(call(
            &mut c,
            ADD_CUSTOM_OP,
            12,
            columns,
            ["invalid", path.to_str().unwrap(), "", ""]
        )
        .is_err());
        let after = c.state();
        assert_eq!(after.sheets, before.sheets, "case {name}");
        assert_eq!(after.rows, before.rows, "case {name}");
        assert_eq!(after.columns, before.columns, "case {name}");
        assert_eq!(after.dirty, before.dirty, "case {name}");
        assert_eq!(
            call(&mut c, SHEET_NAME, 1, 0, [""; 4]).unwrap(),
            "custom-crlf"
        );
    }

    let retry = write("valid-retry.txt", dictionary(40, "\n").as_bytes());
    call(
        &mut c,
        ADD_CUSTOM_OP,
        15,
        10,
        ["custom-retry", retry.to_str().unwrap(), "", ""],
    )
    .unwrap();
    blank(&mut c, SAVE).unwrap();
    assert_eq!(c.state().dirty, 0);
    assert_eq!(c.state().sheets, 4);
}

#[test]
fn rename_delete_and_replacement_validate_before_mutation_and_keep_handle_usable() {
    const ADD_CUSTOM_OP: u32 = 25;
    const REPLACE_DICTIONARY_OP: u32 = 26;
    const RENAME_SHEET_OP: u32 = 27;
    const DELETE_SHEET_OP: u32 = 28;
    let d = tempfile::tempdir().unwrap();
    let vault_path = d.path().join("sheet-operations.tessaveil-alpha");
    let original_path = d.path().join("original.txt");
    let revised_path = d.path().join("revised.txt");
    let original = (0..40)
        .map(|index| format!("synthetic-{index:03}"))
        .collect::<Vec<_>>()
        .join("\n");
    let revised = (0..40)
        .map(|index| format!("replacement-{index:03}"))
        .collect::<Vec<_>>()
        .join("\n");
    std::fs::write(&original_path, original).unwrap();
    std::fs::write(&revised_path, revised).unwrap();
    let mut c = Controller::default();
    setup(&mut c, vault_path.to_str().unwrap());
    call(
        &mut c,
        ADD_CUSTOM_OP,
        12,
        10,
        ["source", original_path.to_str().unwrap(), "", ""],
    )
    .unwrap();
    call(&mut c, VERIFY, 1, 0, [""; 4]).unwrap();
    call(
        &mut c,
        SET_SHEET_PASSWORD,
        0,
        0,
        ["synthetic-sheet-password", "", "", ""],
    )
    .unwrap();
    let source_cell = call(&mut c, CELL, 0, 0, [""; 4]).unwrap();
    blank(&mut c, SAVE).unwrap();
    assert_eq!(c.state().protected, 1);

    for (op, a, fields) in [
        (RENAME_SHEET_OP, 0, ["renamed", "", "", ""]),
        (
            REPLACE_DICTIONARY_OP,
            1,
            ["replacement", revised_path.to_str().unwrap(), "", ""],
        ),
        (DELETE_SHEET_OP, 1, ["source", "", "", ""]),
    ] {
        assert!(call(&mut c, op, a, 0, fields).is_err());
        assert_eq!(c.state().sheets, 1);
        assert_eq!(c.state().dirty, 0);
        assert_eq!(call(&mut c, SHEET_NAME, 0, 0, [""; 4]).unwrap(), "source");
        assert_eq!(call(&mut c, CELL, 0, 0, [""; 4]).unwrap(), source_cell);
    }
    call(
        &mut c,
        UNLOCK_SHEET,
        0,
        0,
        ["synthetic-sheet-password", "", "", ""],
    )
    .unwrap();

    for invalid in ["", "synthetic\nname", "synthetic\0name"] {
        assert!(call(&mut c, RENAME_SHEET_OP, 0, 0, [invalid, "", "", ""]).is_err());
    }
    let overlong = "x".repeat(257);
    assert!(call(&mut c, RENAME_SHEET_OP, 0, 0, [&overlong, "", "", ""]).is_err());
    assert_eq!(c.state().dirty, 0);
    call(
        &mut c,
        RENAME_SHEET_OP,
        0,
        0,
        ["renamed-source", "", "", ""],
    )
    .unwrap();
    assert_eq!(
        call(&mut c, SHEET_NAME, 0, 0, [""; 4]).unwrap(),
        "renamed-source"
    );
    blank(&mut c, SAVE).unwrap();
    call(
        &mut c,
        UNLOCK_SHEET,
        0,
        0,
        ["synthetic-sheet-password", "", "", ""],
    )
    .unwrap();

    assert!(call(
        &mut c,
        REPLACE_DICTIONARY_OP,
        0,
        0,
        ["replacement", revised_path.to_str().unwrap(), "", ""]
    )
    .is_err());
    call(
        &mut c,
        REPLACE_DICTIONARY_OP,
        1,
        0,
        ["replacement", revised_path.to_str().unwrap(), "", ""],
    )
    .unwrap();
    assert_eq!(c.state().sheets, 2);
    assert_eq!(c.state().verified, 0);
    assert_eq!(c.state().protected, 0);
    call(&mut c, SPIN, 0, 0, ["0", "0", "replacement-000", ""]).unwrap();
    assert_eq!(
        call(&mut c, CELL, 0, 0, [""; 4]).unwrap(),
        "replacement-000"
    );
    assert_eq!(
        call(&mut c, SHEET_NAME, 0, 0, [""; 4]).unwrap(),
        "renamed-source"
    );
    call(&mut c, SELECT, 0, 0, [""; 4]).unwrap();
    assert_eq!(call(&mut c, CELL, 0, 0, [""; 4]).unwrap(), source_cell);

    assert!(call(&mut c, DELETE_SHEET_OP, 1, 0, ["wrong", "", "", ""]).is_err());
    assert!(call(
        &mut c,
        DELETE_SHEET_OP,
        0,
        0,
        ["renamed-source", "", "", ""]
    )
    .is_err());
    assert_eq!(c.state().sheets, 2);
    call(
        &mut c,
        DELETE_SHEET_OP,
        1,
        0,
        ["renamed-source", "", "", ""],
    )
    .unwrap();
    assert_eq!(c.state().sheets, 1);
    call(
        &mut c,
        RENAME_SHEET_OP,
        0,
        0,
        ["selected-after-delete", "", "", ""],
    )
    .unwrap();
    assert_eq!(
        call(&mut c, SHEET_NAME, 0, 0, [""; 4]).unwrap(),
        "selected-after-delete"
    );
    blank(&mut c, SAVE).unwrap();
    assert_eq!(c.state().dirty, 0);
}
#[test]
fn warning_gates_create_and_auth_failure_does_not_open_empty_vault() {
    let d = tempfile::tempdir().unwrap();
    let p = d.path().join("synthetic.tessaveil-alpha");
    let p = p.to_str().unwrap();
    let mut c = Controller::default();
    assert!(call(
        &mut c,
        CREATE,
        0,
        0,
        [p, "synthetic-master-password", "", ""]
    )
    .is_err());
    assert!(!std::path::Path::new(p).exists());
    setup(&mut c, p);
    assert_eq!(c.state().state, 2);
    blank(&mut c, CLOSE).unwrap();
    let bad = call(&mut c, OPEN, 0, 0, [p, "synthetic-wrong-password", "", ""]).unwrap_err();
    assert_eq!(bad, "The password is incorrect or the vault is damaged.");
    assert_eq!(c.state().state, 0);
    let mut bytes = std::fs::read(p).unwrap();
    *bytes.last_mut().unwrap() ^= 1;
    std::fs::write(p, bytes).unwrap();
    assert_eq!(
        call(&mut c, OPEN, 0, 0, [p, "synthetic-master-password", "", ""]).unwrap_err(),
        bad
    );
}
#[test]
fn complete_sheet_spin_protect_save_reopen_lock_workflow() {
    let d = tempfile::tempdir().unwrap();
    let p = d.path().join("synthetic.tessaveil-alpha");
    let p = p.to_str().unwrap();
    let mut c = Controller::default();
    setup(&mut c, p);
    let n: usize = blank(&mut c, PROFILE_COUNT).unwrap().parse().unwrap();
    let mut available = Vec::new();
    for i in 0..n {
        let t = call(&mut c, PROFILE, i as u32, 0, [""; 4]).unwrap();
        if t.starts_with("1\t") {
            available.push(i);
        } else {
            assert!(t.split('\t').next_back().unwrap().len() > 1)
        }
    }
    assert_eq!(available.len(), 3);
    for cols in [10, 36] {
        call(
            &mut c,
            ADD,
            available[0] as u32,
            cols,
            ["synthetic-sheet", "", "", ""],
        )
        .unwrap();
        assert_eq!(c.state().columns, cols);
        assert_eq!(c.state().rows, 24);
    }
    assert!(call(&mut c, ADD, u32::MAX, 10, [""; 4]).is_err());
    assert!(call(&mut c, ADD, available[0] as u32, 11, [""; 4]).is_err());
    call(&mut c, VERIFY, 1, 0, [""; 4]).unwrap();
    assert_eq!(c.state().verified, 1);
    call(
        &mut c,
        SET_SHEET_PASSWORD,
        0,
        0,
        ["synthetic-sheet-password", "", "", ""],
    )
    .unwrap();
    blank(&mut c, PROTECT).unwrap();
    assert_eq!(c.state().protected, 1);
    assert!(call(
        &mut c,
        UNLOCK_SHEET,
        0,
        0,
        ["synthetic-wrong-password", "", "", ""]
    )
    .is_err());
    call(
        &mut c,
        UNLOCK_SHEET,
        0,
        0,
        ["synthetic-sheet-password", "", "", ""],
    )
    .unwrap();
    // Public invalid synthetic token exercises the identical replacement transition.
    assert_eq!(
        call(
            &mut c,
            SPIN,
            0,
            0,
            ["?", "!", "synthetic-not-a-dictionary-word", ""]
        )
        .unwrap(),
        ""
    );
    assert_eq!(c.state().verified, 0);
    assert_eq!(c.state().dirty, 1);
    assert!(blank(&mut c, CLOSE).is_err());
    assert_eq!(c.state().state, 2);
    assert!(blank(&mut c, LOCK).is_err());
    blank(&mut c, SAVE).unwrap();
    assert_eq!(c.state().dirty, 0);
    assert_eq!(c.state().protected, 1);
    blank(&mut c, CLOSE).unwrap();
    call(&mut c, OPEN, 0, 0, [p, "synthetic-master-password", "", ""]).unwrap();
    assert_eq!(c.state().sheets, 2);
    blank(&mut c, LOCK).unwrap();
    assert_eq!(c.state().state, 1);
    assert!(call(&mut c, CELL, 0, 0, [""; 4]).is_err());
    call(
        &mut c,
        UNLOCK,
        0,
        0,
        ["synthetic-master-password", "", "", ""],
    )
    .unwrap();
    assert_eq!(c.state().state, 2);
    call(
        &mut c,
        UNLOCK_MASTER,
        0,
        0,
        ["synthetic-master-password", "", "", ""],
    )
    .unwrap();
    assert_eq!(c.state().protected, 0);
}
#[test]
fn timeout_real_activity_choices_and_forced_dirty_lock() {
    let d = tempfile::tempdir().unwrap();
    let p = d.path().join("synthetic.tessaveil-alpha");
    let mut c = Controller::default();
    setup(&mut c, p.to_str().unwrap());
    assert_eq!(c.state().minutes, 5);
    let now = Instant::now();
    c.run(ACTIVITY, 0, 0, [""; 4], now).unwrap();
    c.run(TICK, 0, 0, [""; 4], now + Duration::from_secs(299))
        .unwrap();
    assert_eq!(c.state().state, 2);
    c.run(TICK, 0, 0, [""; 4], now + Duration::from_secs(300))
        .unwrap();
    assert_eq!(c.state().state, 1);
    assert!(c.run(ACTIVITY, 0, 0, [""; 4], now).is_err());
    for minutes in [1, 5, 15, 30] {
        call(&mut c, TIMEOUT, minutes, 0, [""; 4]).unwrap();
        assert_eq!(c.state().minutes, minutes);
    }
    assert!(call(&mut c, TIMEOUT, 0, 0, [""; 4]).is_err());
    call(
        &mut c,
        UNLOCK,
        0,
        0,
        ["synthetic-master-password", "", "", ""],
    )
    .unwrap();
    call(&mut c, LOCK, 2, 0, [""; 4]).unwrap();
    assert_eq!(c.state().state, 1);
}

#[test]
fn failed_save_preserves_dirty_session_and_last_file_then_timeout_discards_edits() {
    use std::os::windows::fs::OpenOptionsExt;
    let d = tempfile::tempdir().unwrap();
    let p = d.path().join("synthetic.tessaveil-alpha");
    let mut c = Controller::default();
    setup(&mut c, p.to_str().unwrap());
    let profile = (0..blank(&mut c, PROFILE_COUNT)
        .unwrap()
        .parse::<u32>()
        .unwrap())
        .find(|i| {
            call(&mut c, PROFILE, *i, 0, [""; 4])
                .unwrap()
                .starts_with("1\t")
        })
        .unwrap();
    call(&mut c, ADD, profile, 10, ["synthetic-sheet", "", "", ""]).unwrap();
    let old = std::fs::read(&p).unwrap();
    let guard = std::fs::OpenOptions::new()
        .read(true)
        .share_mode(1)
        .open(&p)
        .unwrap();
    assert!(blank(&mut c, SAVE).is_err());
    assert!(call(&mut c, CLOSE, 1, 0, [""; 4]).is_err());
    assert_eq!(c.state().state, 2);
    assert_eq!(c.state().dirty, 1);
    assert_eq!(std::fs::read(&p).unwrap(), old);
    drop(guard);
    blank(&mut c, SAVE).unwrap();
    call(&mut c, ADD, profile, 36, ["synthetic-unsaved", "", "", ""]).unwrap();
    let now = Instant::now();
    c.run(ACTIVITY, 0, 0, [""; 4], now).unwrap();
    c.run(TICK, 0, 0, [""; 4], now + Duration::from_secs(300))
        .unwrap();
    assert_eq!(c.state().state, 1);
    assert_eq!(c.state().dirty, 0);
    call(
        &mut c,
        UNLOCK,
        0,
        0,
        ["synthetic-master-password", "", "", ""],
    )
    .unwrap();
    assert_eq!(c.state().sheets, 1);
}

#[test]
fn structural_version_and_creation_errors_remain_safe_and_closed() {
    let d = tempfile::tempdir().unwrap();
    let p = d.path().join("synthetic.tessaveil-alpha");
    let mut c = Controller::default();
    blank(&mut c, ACK).unwrap();
    assert!(
        call(&mut c, CREATE, 0, 0, [p.to_str().unwrap(), "short", "", ""])
            .unwrap_err()
            .starts_with("Use at least 15")
    );
    assert_eq!(c.state().state, 0);
    assert!(!p.exists());
    setup(&mut c, p.to_str().unwrap());
    blank(&mut c, CLOSE).unwrap();
    let mut bytes = std::fs::read(&p).unwrap();
    bytes[8] = 127;
    std::fs::write(&p, &bytes).unwrap();
    assert_eq!(
        call(
            &mut c,
            OPEN,
            0,
            0,
            [p.to_str().unwrap(), "synthetic-master-password", "", ""]
        )
        .unwrap_err(),
        "Unsupported vault or payload version."
    );
    assert_eq!(c.state().state, 0);
    bytes[0] = 0;
    std::fs::write(&p, &bytes).unwrap();
    assert_eq!(
        call(
            &mut c,
            OPEN,
            0,
            0,
            [p.to_str().unwrap(), "synthetic-master-password", "", ""]
        )
        .unwrap_err(),
        "Invalid vault header."
    );
}
