use crate::VaultError;
use unicode_normalization::UnicodeNormalization;
use zeroize::Zeroizing;
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct KdfParams {
    pub memory_kib: u32,
    pub iterations: u32,
    pub parallelism: u32,
}
impl Default for KdfParams {
    fn default() -> Self {
        Self {
            memory_kib: 65536,
            iterations: 3,
            parallelism: 4,
        }
    }
}
impl KdfParams {
    pub fn validate(self) -> Result<(), VaultError> {
        if !(65536..=262144).contains(&self.memory_kib)
            || !(3..=6).contains(&self.iterations)
            || !(1..=8).contains(&self.parallelism)
        {
            return Err(VaultError::KdfOutOfBounds);
        }
        if self != Self::default() {
            return Err(VaultError::UnsupportedKdf);
        }
        Ok(())
    }
}
pub fn normalize_password(password: &str) -> Result<Zeroizing<String>, VaultError> {
    if password.len() > 4096 || password.contains('\0') {
        return Err(VaultError::InvalidPassword);
    }
    // Reserve the full bounded output before the first secret byte. No push can
    // reallocate and leave an unwiped prefix outside the Zeroizing owner.
    let mut result = Zeroizing::new(String::with_capacity(4096));
    for ch in password.nfc() {
        if result.len() + ch.len_utf8() > 4096 {
            return Err(VaultError::InvalidPassword);
        }
        result.push(ch);
        #[cfg(test)]
        allocation_tests::observe_owner(&result);
    }
    Ok(result)
}
#[cfg(test)]
mod allocation_tests {
    use super::*;
    use std::{
        alloc::{GlobalAlloc, Layout, System},
        sync::atomic::{AtomicBool, AtomicUsize, Ordering},
    };
    static WATCH: AtomicBool = AtomicBool::new(false);
    static PREFIX_REALLOCS: AtomicUsize = AtomicUsize::new(0);
    static PREFIX_FREES: AtomicUsize = AtomicUsize::new(0);
    static FINAL_PTR: AtomicUsize = AtomicUsize::new(0);
    static LIVE_LEN: AtomicUsize = AtomicUsize::new(0);
    static FINAL_WIPED: AtomicBool = AtomicBool::new(false);
    struct ObservedAllocator;
    pub(super) fn observe_owner(value: &str) {
        if WATCH.load(Ordering::SeqCst) && value.starts_with("nfcwatch-") {
            LIVE_LEN.store(value.len(), Ordering::SeqCst);
            FINAL_PTR.store(value.as_ptr() as usize, Ordering::SeqCst);
        }
    }
    // Test-only moving allocator. Every allocation is initialized, and all inspection
    // occurs before its deallocation. No secret bytes are printed or read after free.
    unsafe impl GlobalAlloc for ObservedAllocator {
        unsafe fn alloc(&self, layout: Layout) -> *mut u8 {
            unsafe { System.alloc_zeroed(layout) }
        }
        unsafe fn alloc_zeroed(&self, layout: Layout) -> *mut u8 {
            unsafe { System.alloc_zeroed(layout) }
        }
        unsafe fn dealloc(&self, ptr: *mut u8, layout: Layout) {
            if WATCH.load(Ordering::SeqCst) && FINAL_PTR.load(Ordering::SeqCst) == ptr as usize {
                // Only the initialized bytes of a registered live String are read.
                let live =
                    unsafe { std::slice::from_raw_parts(ptr, LIVE_LEN.load(Ordering::SeqCst)) };
                let wiped = live.iter().all(|b| *b == 0);
                if !wiped {
                    PREFIX_FREES.fetch_add(1, Ordering::SeqCst);
                }
                FINAL_WIPED.store(wiped, Ordering::SeqCst);
                FINAL_PTR.store(0, Ordering::SeqCst);
            }
            unsafe { System.dealloc(ptr, layout) };
        }
        unsafe fn realloc(&self, ptr: *mut u8, layout: Layout, size: usize) -> *mut u8 {
            let next_layout = unsafe { Layout::from_size_align_unchecked(size, layout.align()) };
            let next = unsafe { System.alloc_zeroed(next_layout) };
            if next.is_null() {
                return next;
            }
            unsafe { std::ptr::copy_nonoverlapping(ptr, next, layout.size().min(size)) };
            if WATCH.load(Ordering::SeqCst) && FINAL_PTR.load(Ordering::SeqCst) == ptr as usize {
                PREFIX_REALLOCS.fetch_add(1, Ordering::SeqCst);
                FINAL_PTR.store(next as usize, Ordering::SeqCst);
            }
            unsafe { System.dealloc(ptr, layout) };
            next
        }
    }
    #[global_allocator]
    static ALLOCATOR: ObservedAllocator = ObservedAllocator;
    #[test]
    fn normalized_password_never_reallocates_a_live_secret_prefix() {
        let expanded = format!("nfcwatch-{}", "\u{0344}".repeat(1000));
        let overflow = format!("nfcwatch-{}", "\u{0344}".repeat(1500));
        PREFIX_REALLOCS.store(0, Ordering::SeqCst);
        PREFIX_FREES.store(0, Ordering::SeqCst);
        WATCH.store(true, Ordering::SeqCst);
        for input in [
            "nfcwatch-synthetic-ascii-abcdefghijklmnopqrstuvwxyz",
            expanded.as_str(),
        ] {
            let normalized = normalize_password(input).unwrap();
            FINAL_WIPED.store(false, Ordering::SeqCst);
            drop(normalized);
            assert!(
                FINAL_WIPED.load(Ordering::SeqCst),
                "current owner must be wiped before deallocation"
            );
        }
        FINAL_WIPED.store(false, Ordering::SeqCst);
        assert!(matches!(
            normalize_password(&overflow),
            Err(VaultError::InvalidPassword)
        ));
        assert!(
            FINAL_WIPED.load(Ordering::SeqCst),
            "overflow error must wipe its current owner"
        );
        WATCH.store(false, Ordering::SeqCst);
        assert_eq!(
            PREFIX_REALLOCS.load(Ordering::SeqCst),
            0,
            "normalized password prefixes must not be freed by realloc"
        );
        assert_eq!(
            PREFIX_FREES.load(Ordering::SeqCst),
            0,
            "success and error paths wipe owned password allocations"
        );
    }
}
