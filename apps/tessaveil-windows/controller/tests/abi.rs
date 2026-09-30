use tessaveil_windows_controller::*;

#[test]
fn numeric_operations_are_frozen_and_append_only() {
    assert_eq!(
        [
            ACK,
            CREATE,
            OPEN,
            SAVE,
            CLOSE,
            LOCK,
            UNLOCK,
            ADD,
            SELECT,
            VERIFY,
            SET_SHEET_PASSWORD,
            PROTECT,
            UNLOCK_SHEET,
            UNLOCK_MASTER,
            SPIN,
            TIMEOUT,
            ACTIVITY,
            TICK,
            INFO,
            CELL,
            PROFILE,
            PROFILE_COUNT,
            SHEET_NAME,
            PROFILE_LENGTHS,
            ADD_CUSTOM,
            REPLACE_DICTIONARY,
            RENAME_SHEET,
            DELETE_SHEET,
            PROFILE_FIELD,
            PROFILE_LENGTH_COUNT,
            PROFILE_LENGTH,
            SHEET_FIELD,
            BACKUP,
            RESTORE,
            CHANGE_PASSWORD,
            LOCALE,
            THEME,
        ],
        std::array::from_fn::<_, 37, _>(|index| index as u32 + 1)
    );
}

#[test]
fn abi_layout_wipes_inputs_bounds_handles_and_error_outputs() {
    assert_eq!(std::mem::size_of::<Input>(), 16400);
    assert_eq!(std::mem::size_of::<Reply>(), 4136);
    assert_eq!(std::mem::offset_of!(Reply, text), 40);
    let id = tv_new();
    assert_ne!(id, 0);
    let mut i = Input::default();
    let mut o = Reply::default();
    for (index, slot) in i.data.iter_mut().enumerate() {
        slot[0] = b'W' + index as u8;
        i.len[index] = 1;
    }
    assert_eq!(unsafe { tv_call(id, ACK, 0, 0, &mut i, &mut o) }, 0);
    assert_eq!(o.abi, 1);
    assert!(i.data.iter().flatten().all(|b| *b == 0));
    assert_eq!(o.minutes, 5);
    assert!(o.text[o.text_len as usize..].iter().all(|byte| *byte == 0));
    for (index, slot) in i.data.iter_mut().enumerate() {
        slot[0] = b'S' + index as u8;
        i.len[index] = 1;
    }
    i.len[0] = 4097;
    assert_eq!(unsafe { tv_call(id, ACK, 0, 0, &mut i, &mut o) }, -1);
    assert_eq!(o.state, 0);
    assert_eq!(i.len, [0; 4]);
    assert!(o.text.iter().all(|b| *b == 0));
    assert_eq!(unsafe { tv_call(id, INFO, 0, 0, &mut i, &mut o) }, -1);
    tv_free(id);
    assert_eq!(
        unsafe { tv_call(id, INFO, 0, 0, std::ptr::null_mut(), &mut o) },
        -1
    );
    let id = tv_new();
    i.len[0] = 1;
    i.data[0][0] = 255;
    assert_eq!(unsafe { tv_call(id, ACK, 0, 0, &mut i, &mut o) }, -1);
    assert!(i.data.iter().flatten().all(|b| *b == 0));
    assert_eq!(unsafe { tv_call(id, INFO, 0, 0, &mut i, &mut o) }, -1);
    tv_free(id);

    let id = tv_new();
    for (index, slot) in i.data.iter_mut().enumerate() {
        slot[0] = b'a' + index as u8;
        i.len[index] = 1;
    }
    assert_eq!(unsafe { tv_call(id, u32::MAX, 0, 0, &mut i, &mut o) }, 1);
    assert_eq!(
        std::str::from_utf8(&o.text[..o.text_len as usize]).unwrap(),
        "invalid-payload"
    );
    assert!(i.data.iter().flatten().all(|byte| *byte == 0));
    assert_eq!(i.len, [0; 4]);
    assert!(o.text[o.text_len as usize..].iter().all(|byte| *byte == 0));
    assert_eq!(unsafe { tv_call(id, INFO, 0, 0, &mut i, &mut o) }, 0);
    tv_free(id);
}
#[test]
fn null_peer_wipes_the_valid_owned_buffer_and_destroys_the_handle() {
    let id = tv_new();
    let mut input = Input::default();
    input.data[0][0] = 42;
    input.len[0] = 1;
    assert_eq!(
        unsafe { tv_call(id, INFO, 0, 0, &mut input, std::ptr::null_mut()) },
        -1
    );
    assert_eq!(input.data[0][0], 0);
    let mut output = Reply::default();
    assert_eq!(
        unsafe { tv_call(id, INFO, 0, 0, &mut input, &mut output) },
        -1
    );

    let id = tv_new();
    let mut output = Reply {
        state: 2,
        ..Default::default()
    };
    output.text[0] = 42;
    assert_eq!(
        unsafe { tv_call(id, INFO, 0, 0, std::ptr::null_mut(), &mut output) },
        -1
    );
    assert_eq!(output.state, 0);
    assert_eq!(output.text[0], 0);
    assert_eq!(
        unsafe { tv_call(id, INFO, 0, 0, &mut input, &mut output) },
        -1
    );
}
