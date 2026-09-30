use super::*;
use std::{
    collections::HashMap,
    panic::{catch_unwind, AssertUnwindSafe},
    sync::{Mutex, OnceLock},
};
use zeroize::Zeroize;
#[repr(C)]
pub struct Input {
    pub len: [u32; 4],
    pub data: [[u8; 4096]; 4],
}
impl Default for Input {
    fn default() -> Self {
        Self {
            len: [0; 4],
            data: [[0; 4096]; 4],
        }
    }
}
#[repr(C)]
pub struct Reply {
    pub abi: u32,
    pub state: u32,
    pub dirty: u32,
    pub sheets: u32,
    pub rows: u32,
    pub columns: u32,
    pub protected: u32,
    pub verified: u32,
    pub minutes: u32,
    pub text_len: u32,
    pub text: [u8; 4096],
}
impl Default for Reply {
    fn default() -> Self {
        Self {
            abi: 1,
            state: 0,
            dirty: 0,
            sheets: 0,
            rows: 0,
            columns: 0,
            protected: 0,
            verified: 0,
            minutes: 0,
            text_len: 0,
            text: [0; 4096],
        }
    }
}
#[no_mangle]
pub extern "C" fn tv_new() -> u64 {
    catch_unwind(|| {
        static NEXT: std::sync::atomic::AtomicU64 = std::sync::atomic::AtomicU64::new(1);
        let id = NEXT.fetch_add(1, std::sync::atomic::Ordering::Relaxed);
        if id == 0 {
            return 0;
        }
        match controllers().lock() {
            Ok(mut all) => {
                all.insert(id, Controller::default());
                id
            }
            Err(_) => 0,
        }
    })
    .unwrap_or(0)
}
#[no_mangle]
pub extern "C" fn tv_free(id: u64) {
    let _ = catch_unwind(|| {
        match controllers().lock() {
            Ok(mut all) => {
                all.remove(&id);
            }
            Err(poison) => {
                // A panic makes all sessions under the registry suspect. Drop
                // their Rust owners even though the mutex was poisoned.
                poison.into_inner().clear();
            }
        }
    });
}
fn controllers() -> &'static Mutex<HashMap<u64, Controller>> {
    static ALL: OnceLock<Mutex<HashMap<u64, Controller>>> = OnceLock::new();
    ALL.get_or_init(|| Mutex::new(HashMap::new()))
}
/// # Safety
/// Requires aligned, valid, disjoint input/output objects, exclusively borrowed.
#[no_mangle]
pub unsafe extern "C" fn tv_call(
    id: u64,
    op: u32,
    a: u32,
    b: u32,
    input: *mut Input,
    output: *mut Reply,
) -> i32 {
    if input.is_null() || output.is_null() {
        if !input.is_null() {
            let input = unsafe { &mut *input };
            input.data.zeroize();
            input.len.zeroize();
        }
        if !output.is_null() {
            let output = unsafe { &mut *output };
            output.text.zeroize();
            *output = Reply::default();
        }
        return -1;
    }
    let input = unsafe { &mut *input };
    let output = unsafe { &mut *output };
    *output = Reply::default();
    let result = catch_unwind(AssertUnwindSafe(|| {
        let mut all = controllers().lock().map_err(|_| ())?;
        let c = all.get_mut(&id).ok_or(())?;
        let mut fields = [""; 4];
        for (i, field) in fields.iter_mut().enumerate() {
            let n = input.len[i] as usize;
            if n > 4096 {
                return Err(());
            }
            *field = std::str::from_utf8(&input.data[i][..n]).map_err(|_| ())?;
        }
        let result = c.run(op, a, b, fields, Instant::now());
        let s = c.state();
        output.state = s.state;
        output.dirty = s.dirty;
        output.sheets = s.sheets;
        output.rows = s.rows;
        output.columns = s.columns;
        output.protected = s.protected;
        output.verified = s.verified;
        output.minutes = s.minutes;
        let (code, mut text) = match result {
            Ok(t) => (0, t),
            Err(t) => (1, t),
        };
        if text.len() > output.text.len() {
            text.zeroize();
            return Err(());
        }
        output.text_len = text.len() as u32;
        output.text[..text.len()].copy_from_slice(text.as_bytes());
        text.zeroize();
        Ok(code)
    }));
    input.data.zeroize();
    input.len.zeroize();
    match result {
        Ok(Ok(code)) => code,
        _ => {
            tv_free(id);
            output.text.zeroize();
            *output = Reply::default();
            -1
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn poisoned_boundary_drops_owned_sessions_instead_of_retaining_them() {
        let id = tv_new();
        assert_ne!(id, 0);
        let _ = catch_unwind(|| {
            let _guard = controllers().lock().unwrap();
            panic!("synthetic boundary fault");
        });
        tv_free(id);
        let guard = controllers().lock().unwrap_or_else(|e| e.into_inner());
        assert!(!guard.contains_key(&id));
    }
}
