use tessaveil_windows_controller::*;
#[test]
fn abi_layout_wipes_inputs_bounds_handles_and_error_outputs() {
    assert_eq!(std::mem::size_of::<Input>(), 16400);
    assert_eq!(std::mem::size_of::<Reply>(), 4136);
    assert_eq!(std::mem::offset_of!(Reply, text), 40);
    let id = tv_new();
    assert_ne!(id, 0);
    let mut i = Input::default();
    let mut o = Reply::default();
    i.data[0][0] = b'X';
    i.len[0] = 1;
    assert_eq!(unsafe { tv_call(id, ACK, 0, 0, &mut i, &mut o) }, 0);
    assert_eq!(o.abi, 1);
    assert!(i.data.iter().flatten().all(|b| *b == 0));
    assert_eq!(o.minutes, 5);
    i.len[0] = 4097;
    assert_eq!(unsafe { tv_call(id, ACK, 0, 0, &mut i, &mut o) }, -1);
    assert_eq!(o.state, 0);
    assert_eq!(i.len, [0; 4]);
    assert!(o.text.iter().all(|b| *b == 0));
    tv_free(id);
    assert_eq!(unsafe { tv_call(id, INFO, 0, 0, &mut i, &mut o) }, -1);
    assert_eq!(
        unsafe { tv_call(id, INFO, 0, 0, std::ptr::null_mut(), &mut o) },
        -1
    );
    let id = tv_new();
    i.len[0] = 1;
    i.data[0][0] = 255;
    assert_eq!(unsafe { tv_call(id, ACK, 0, 0, &mut i, &mut o) }, -1);
    assert!(i.data.iter().flatten().all(|b| *b == 0));
    tv_free(id);
}
#[test]
fn null_peer_still_wipes_the_valid_owned_buffer() {
    let mut input = Input::default();
    input.data[0][0] = 42;
    input.len[0] = 1;
    assert_eq!(
        unsafe { tv_call(0, INFO, 0, 0, &mut input, std::ptr::null_mut()) },
        -1
    );
    assert_eq!(input.data[0][0], 0);
    let mut output = Reply {
        state: 2,
        ..Default::default()
    };
    output.text[0] = 42;
    assert_eq!(
        unsafe { tv_call(0, INFO, 0, 0, std::ptr::null_mut(), &mut output) },
        -1
    );
    assert_eq!(output.state, 0);
    assert_eq!(output.text[0], 0);
}
