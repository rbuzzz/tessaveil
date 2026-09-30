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
