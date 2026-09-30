use crate::{
    crypto,
    format::{Header, HEADER_LEN, MAX_FILE},
};
use crate::{
    crypto::Secrets,
    model::{Payload, PayloadEditor},
    session::{Inactivity, Session, TimeoutToken},
    VaultError,
};
use std::{
    fs::{File, OpenOptions},
    io::{Read, Write},
};
use std::{
    path::{Path, PathBuf},
    time::Instant,
};
#[derive(Clone, Copy, Default)]
pub enum StoragePolicy {
    #[default]
    ReadOnly,
    DevelopmentLocalNtfs,
}
#[derive(Default)]
pub struct CreateOptions {
    pub name: String,
    pub storage: StoragePolicy,
    pub inactivity: Inactivity,
}
pub struct VaultService;
pub struct OpenVault {
    path: PathBuf,
    storage: StoragePolicy,
    session: Session,
    unlocked: Option<Unlocked>,
}
struct Unlocked {
    payload: Payload,
    secrets: Secrets,
    salt: [u8; 16],
}
impl VaultService {
    pub fn restore(
        source: impl AsRef<Path>,
        destination: impl AsRef<Path>,
        password: &str,
        storage: StoragePolicy,
    ) -> Result<OpenVault, VaultError> {
        let source = resolve(source.as_ref())?;
        let (image, _source_guard) = read_recovery_image(&source)?;
        let (payload, secrets) = crypto::open(&image, password)?;
        let path = recovery_destination(destination.as_ref(), storage)?;
        persist_image(&path, &image, &secrets, true, |_, _| Ok(()))?;
        Ok(OpenVault {
            path,
            storage,
            session: Session::new(Inactivity::default(), Instant::now()),
            unlocked: Some(Unlocked {
                payload,
                secrets,
                salt: image[24..40].try_into().expect("fixed header range"),
            }),
        })
    }
    pub fn create(
        path: impl AsRef<Path>,
        password: &str,
        options: CreateOptions,
    ) -> Result<OpenVault, VaultError> {
        let path = resolve(path.as_ref())?;
        if path.try_exists().map_err(io_error)? {
            return Err(VaultError::AlreadyExists);
        }
        check_storage(&path, options.storage)?;
        let mut payload = Payload::default();
        payload.rename(&options.name)?;
        let (image, secrets) = crypto::create(password, &payload)?;
        persist_image(&path, &image, &secrets, true, |_, _| Ok(()))?;
        let salt = image[24..40].try_into().expect("fixed header range");
        Ok(OpenVault {
            path,
            storage: options.storage,
            session: Session::new(options.inactivity, Instant::now()),
            unlocked: Some(Unlocked {
                payload,
                secrets,
                salt,
            }),
        })
    }
    pub fn open(path: impl AsRef<Path>, password: &str) -> Result<OpenVault, VaultError> {
        let path = resolve(path.as_ref())?;
        let (image, _guard) = read_image(&path)?;
        let (payload, secrets) = crypto::open(&image, password)?;
        let salt = image[24..40].try_into().expect("fixed header range");
        Ok(OpenVault {
            path,
            storage: StoragePolicy::ReadOnly,
            session: Session::new(Inactivity::default(), Instant::now()),
            unlocked: Some(Unlocked {
                payload,
                secrets,
                salt,
            }),
        })
    }
}
impl OpenVault {
    /// Copy the authenticated saved ciphertext; unsaved or stale payloads fail closed.
    pub fn backup_to(&mut self, destination: impl AsRef<Path>) -> Result<(), VaultError> {
        self.expire(self.session.token(), Instant::now());
        let u = self.unlocked.as_ref().ok_or(VaultError::Locked)?;
        let (image, _source_guard) = read_recovery_image(&self.path)?;
        let saved = crypto::authenticated_payload(&image, &u.secrets)?;
        if saved.encode()?.as_slice() != u.payload.encode()?.as_slice() {
            return Err(VaultError::UnsavedChanges);
        }
        let destination = recovery_destination(destination.as_ref(), self.storage)?;
        persist_image(&destination, &image, &u.secrets, true, |_, _| Ok(()))
    }
    /// Atomically save the complete current payload under freshly generated keys.
    pub fn change_master_password(
        &mut self,
        current: &str,
        replacement: &str,
    ) -> Result<(), VaultError> {
        self.rotate(
            current,
            replacement,
            &mut crypto::Random::default(),
            |_, _| Ok(()),
        )
    }
    fn rotate(
        &mut self,
        current: &str,
        replacement: &str,
        random: &mut crypto::Random<'_>,
        hook: impl FnMut(Stage, &Path) -> Result<(), VaultError>,
    ) -> Result<(), VaultError> {
        use subtle::ConstantTimeEq;
        self.expire(self.session.token(), Instant::now());
        let u = self.unlocked.as_ref().ok_or(VaultError::Locked)?;
        let current_key = crypto::derive(current, &u.salt)?;
        if !bool::from(current_key.as_slice().ct_eq(u.secrets.kek.as_slice())) {
            return Err(VaultError::Authentication);
        }
        check_storage(&self.path, self.storage)?;
        let (image, secrets) = crypto::create_with_random(replacement, &u.payload, random)?;
        let salt = image[24..40].try_into().expect("fixed header range");
        persist_image(&self.path, &image, &secrets, false, hook)?;
        // There are no fallible operations after the atomic commit.
        let u = self.unlocked.as_mut().expect("checked session");
        u.secrets = secrets;
        u.salt = salt;
        for sheet in &mut u.payload.sheets {
            sheet.unlocked = false;
        }
        Ok(())
    }
    /// Borrow a narrow editor, without transferring ownership of the payload.
    ///
    /// ```
    /// use tessaveil_core::OpenVault;
    /// fn rename(vault: &mut OpenVault) {
    ///     vault.payload_mut().unwrap().rename("synthetic-label").unwrap();
    /// }
    /// ```
    ///
    /// ```compile_fail
    /// use tessaveil_core::OpenVault;
    /// fn detach(vault: &mut OpenVault) {
    ///     let _retained = std::mem::take(vault.payload_mut().unwrap());
    /// }
    /// ```
    pub fn payload_mut(&mut self) -> Result<PayloadEditor<'_>, VaultError> {
        self.expire(self.session.token(), Instant::now());
        Ok(PayloadEditor {
            payload: &mut self.unlocked.as_mut().ok_or(VaultError::Locked)?.payload,
        })
    }
    pub fn save(&mut self) -> Result<(), VaultError> {
        self.expire(self.session.token(), Instant::now());
        let u = self.unlocked.as_ref().ok_or(VaultError::Locked)?;
        check_storage(&self.path, self.storage)?;
        let image = crypto::seal(&u.payload, &u.secrets, &u.salt)?;
        persist_image(&self.path, &image, &u.secrets, false, |_, _| Ok(()))?;
        for sheet in &mut self
            .unlocked
            .as_mut()
            .expect("checked session")
            .payload
            .sheets
        {
            sheet.unlocked = false;
        }
        Ok(())
    }
    /// Authorize one sheet using the master credential; never expose keys.
    pub fn unlock_sheet_with_master(
        &mut self,
        index: usize,
        password: &str,
    ) -> Result<(), VaultError> {
        use subtle::ConstantTimeEq;
        self.expire(self.session.token(), Instant::now());
        let u = self.unlocked.as_mut().ok_or(VaultError::Locked)?;
        let sheet = u
            .payload
            .sheets
            .get_mut(index)
            .ok_or(VaultError::InvalidPayload)?;
        let key = crypto::derive(password, &u.salt)?;
        if !bool::from(key.as_slice().ct_eq(u.secrets.kek.as_slice())) {
            return Err(VaultError::Authentication);
        }
        sheet.unlocked = true;
        Ok(())
    }
    pub fn lock(&mut self) {
        self.unlocked = None;
    }
    pub fn is_locked(&self) -> bool {
        self.unlocked.is_none()
    }
    pub fn set_storage_policy(&mut self, policy: StoragePolicy) {
        self.storage = policy;
    }
    pub fn activity(&mut self, now: Instant) -> Result<TimeoutToken, VaultError> {
        self.expire(self.session.token(), now);
        if self.is_locked() {
            return Err(VaultError::Locked);
        }
        Ok(self.session.activity(now))
    }
    pub fn timeout_token(&self) -> TimeoutToken {
        self.session.token()
    }
    pub fn set_inactivity(
        &mut self,
        timeout: Inactivity,
        now: Instant,
    ) -> Result<TimeoutToken, VaultError> {
        self.activity(now)?;
        Ok(self.session.set_inactivity(timeout, now))
    }
    pub fn expire(&mut self, token: TimeoutToken, now: Instant) -> bool {
        if self.session.is_expired(token, now) {
            self.lock();
            true
        } else {
            false
        }
    }
}
fn resolve(path: &Path) -> Result<PathBuf, VaultError> {
    // Reject ADS, reserved DOS device names and ambiguous Win32 trailing aliases
    // before canonicalizing the parent (which produces an extended-length path).
    for component in path.components() {
        if let std::path::Component::Normal(name) = component {
            let name = name.to_str().ok_or(VaultError::InvalidPath)?;
            let stem = name
                .split('.')
                .next()
                .unwrap_or("")
                .trim_end_matches(' ')
                .to_ascii_uppercase();
            if name.contains([':', '\0'])
                || name.ends_with([' ', '.'])
                || matches!(
                    stem.as_str(),
                    "CON" | "PRN" | "AUX" | "NUL" | "CONIN$" | "CONOUT$"
                )
                || ["COM", "LPT"].iter().any(|prefix| {
                    stem.strip_prefix(prefix).is_some_and(|suffix| {
                        matches!(
                            suffix,
                            "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" | "¹" | "²" | "³"
                        )
                    })
                })
            {
                return Err(VaultError::InvalidPath);
            }
        }
    }
    if path.extension().and_then(|s| s.to_str()) != Some("tessaveil-alpha") {
        return Err(VaultError::InvalidPath);
    }
    let parent = path
        .parent()
        .filter(|p| !p.as_os_str().is_empty())
        .unwrap_or(Path::new("."));
    let result = parent
        .canonicalize()
        .map_err(io_error)?
        .join(path.file_name().ok_or(VaultError::InvalidPath)?);
    if let Ok(meta) = std::fs::symlink_metadata(&result) {
        if !meta.is_file() || meta.file_type().is_symlink() {
            return Err(VaultError::InvalidPath);
        }
    }
    Ok(result)
}
fn io_error(error: std::io::Error) -> VaultError {
    #[cfg(windows)]
    match error.raw_os_error() {
        Some(5 | 32 | 33) => return VaultError::AccessDenied,
        Some(39 | 112) => return VaultError::InsufficientSpace,
        _ => (),
    }
    match error.kind() {
        std::io::ErrorKind::PermissionDenied => VaultError::AccessDenied,
        std::io::ErrorKind::AlreadyExists => VaultError::AlreadyExists,
        std::io::ErrorKind::UnexpectedEof => VaultError::Truncated,
        std::io::ErrorKind::StorageFull => VaultError::InsufficientSpace,
        _ => VaultError::Io,
    }
}
fn read_image(path: &Path) -> Result<(Vec<u8>, File), VaultError> {
    let mut options = OpenOptions::new();
    options.read(true);
    #[cfg(windows)]
    {
        use std::os::windows::fs::OpenOptionsExt;
        options.share_mode(1 | 4);
    }
    read_image_handle(options.open(path).map_err(io_error)?)
}
fn recovery_destination(path: &Path, storage: StoragePolicy) -> Result<PathBuf, VaultError> {
    let path = resolve(path)?;
    if path.try_exists().map_err(io_error)? {
        return Err(VaultError::AlreadyExists);
    }
    check_storage(&path, storage)?;
    Ok(path)
}
fn read_recovery_image(path: &Path) -> Result<(Vec<u8>, File), VaultError> {
    let mut options = OpenOptions::new();
    options.read(true);
    #[cfg(windows)]
    {
        use std::os::windows::fs::{MetadataExt, OpenOptionsExt};
        use windows_sys::Win32::Storage::FileSystem::{
            FILE_ATTRIBUTE_REPARSE_POINT, FILE_FLAG_OPEN_REPARSE_POINT, FILE_SHARE_READ,
        };
        options
            .share_mode(FILE_SHARE_READ)
            .custom_flags(FILE_FLAG_OPEN_REPARSE_POINT);
        let file = options.open(path).map_err(io_error)?;
        let metadata = file.metadata().map_err(io_error)?;
        if !metadata.is_file() || metadata.file_attributes() & FILE_ATTRIBUTE_REPARSE_POINT != 0 {
            return Err(VaultError::InvalidPath);
        }
        read_image_handle(file)
    }
    #[cfg(not(windows))]
    read_image_handle(options.open(path).map_err(io_error)?)
}
fn read_image_handle(mut file: File) -> Result<(Vec<u8>, File), VaultError> {
    let len = file.metadata().map_err(io_error)?.len();
    if len > MAX_FILE as u64 {
        return Err(VaultError::TooLarge);
    }
    let mut prefix = [0; HEADER_LEN];
    file.read_exact(&mut prefix).map_err(io_error)?;
    let header = Header::parse(&prefix, len)?;
    let mut image = vec![0; HEADER_LEN + header.ciphertext_len()];
    image[..HEADER_LEN].copy_from_slice(&prefix);
    file.read_exact(&mut image[HEADER_LEN..])
        .map_err(io_error)?;
    let mut extra = [0; 1];
    if file.read(&mut extra).map_err(io_error)? != 0 {
        return Err(VaultError::InvalidHeader);
    }
    Ok((image, file))
}
fn check_storage(path: &Path, policy: StoragePolicy) -> Result<(), VaultError> {
    if matches!(policy, StoragePolicy::ReadOnly) {
        return Err(VaultError::UnsupportedFilesystem);
    }
    platform::check(path)
}
#[derive(Clone, Copy, PartialEq, Eq)]
enum Stage {
    BeforeWrite,
    AfterWrite,
    AfterFlush,
    AfterVerify,
    BeforeReplace,
}
fn persist_image(
    path: &Path,
    image: &[u8],
    secrets: &Secrets,
    create: bool,
    mut hook: impl FnMut(Stage, &Path) -> Result<(), VaultError>,
) -> Result<(), VaultError> {
    let mut temp = OwnedTemp::create(path.parent().ok_or(VaultError::InvalidPath)?)?;
    let result = (|| {
        hook(Stage::BeforeWrite, &temp.name)?;
        temp.file.write_all(image).map_err(io_error)?;
        hook(Stage::AfterWrite, &temp.name)?;
        temp.file.flush().map_err(io_error)?;
        temp.file.sync_all().map_err(io_error)?;
        hook(Stage::AfterFlush, &temp.name)?;
        // ReOpenFile binds the read view to the owned object, never its pathname.
        let (reopened, _guard) = read_image_handle(platform::reopen(&temp.file)?)?;
        crypto::verify(&reopened, secrets)?;
        hook(Stage::AfterVerify, &temp.name)?;
        hook(Stage::BeforeReplace, &temp.name)?;
        platform::replace(&temp.file, path, create)
    })();
    if let Err(cause) = result {
        let cleanup = platform::delete(&temp.file);
        // After an explicit cleanup attempt, preserve any survivor for reporting.
        temp.finished = true;
        if cleanup.is_err() {
            return Err(VaultError::TemporaryRemains {
                cause: Box::new(cause),
                path: platform::current_path(&temp.file).ok(),
            });
        }
        return Err(cause);
    }
    temp.finished = true;
    Ok(())
}
// This owner never removes a pathname. Even unwinding cleanup uses the handle.
struct OwnedTemp {
    file: File,
    name: PathBuf,
    finished: bool,
}
impl OwnedTemp {
    fn create(parent: &Path) -> Result<Self, VaultError> {
        for _ in 0..16 {
            let mut random = [0; 16];
            getrandom::getrandom(&mut random).map_err(|_| VaultError::Io)?;
            let name = parent.join(format!(
                ".tessaveil-alpha-{:032x}.tmp",
                u128::from_le_bytes(random)
            ));
            match platform::create(&name) {
                Ok(file) => {
                    return Ok(Self {
                        file,
                        name,
                        finished: false,
                    })
                }
                Err(VaultError::AlreadyExists) => continue,
                Err(e) => return Err(e),
            }
        }
        Err(VaultError::Io)
    }
}
impl Drop for OwnedTemp {
    fn drop(&mut self) {
        if !self.finished {
            let _ = platform::delete(&self.file);
        }
    }
}
#[cfg(windows)]
mod platform {
    use super::*;
    use std::{
        os::windows::{
            ffi::{OsStrExt, OsStringExt},
            fs::OpenOptionsExt,
            io::{AsRawHandle, FromRawHandle},
        },
        ptr,
    };
    use windows_sys::Win32::Foundation::{GENERIC_READ, GENERIC_WRITE, INVALID_HANDLE_VALUE};
    use windows_sys::Win32::Storage::FileSystem::*;
    fn wide(path: &Path) -> Result<Vec<u16>, VaultError> {
        let mut v: Vec<u16> = path.as_os_str().encode_wide().collect();
        if v.contains(&0) {
            return Err(VaultError::InvalidPath);
        }
        v.push(0);
        Ok(v)
    }
    pub(super) fn check(path: &Path) -> Result<(), VaultError> {
        let parent = wide(path.parent().ok_or(VaultError::InvalidPath)?)?;
        let mut volume = [0u16; 32768];
        let mut fs = [0u16; 32];
        // SAFETY: terminated UTF-16 inputs, sized writable buffers, optional outputs null.
        unsafe {
            if GetVolumePathNameW(parent.as_ptr(), volume.as_mut_ptr(), volume.len() as u32) == 0 {
                return Err(io_error(std::io::Error::last_os_error()));
            }
            if GetDriveTypeW(volume.as_ptr()) != 3 {
                return Err(VaultError::UnsupportedFilesystem);
            }
            if GetVolumeInformationW(
                volume.as_ptr(),
                ptr::null_mut(),
                0,
                ptr::null_mut(),
                ptr::null_mut(),
                ptr::null_mut(),
                fs.as_mut_ptr(),
                fs.len() as u32,
            ) == 0
            {
                return Err(io_error(std::io::Error::last_os_error()));
            }
        }
        if fs[..5] != [78, 84, 70, 83, 0] {
            return Err(VaultError::UnsupportedFilesystem);
        }
        Ok(())
    }
    pub(super) fn create(path: &Path) -> Result<File, VaultError> {
        OpenOptions::new()
            .create_new(true)
            .write(true)
            .read(true)
            .access_mode(GENERIC_READ | GENERIC_WRITE | DELETE)
            .share_mode(FILE_SHARE_READ | FILE_SHARE_DELETE)
            .custom_flags(FILE_FLAG_WRITE_THROUGH)
            .open(path)
            .map_err(io_error)
    }
    pub(super) fn reopen(file: &File) -> Result<File, VaultError> {
        // SAFETY: borrowed live handle. ReOpenFile creates a distinct owned handle
        // to the same object; sharing permits the existing owner's write/delete access.
        let handle = unsafe {
            ReOpenFile(
                file.as_raw_handle(),
                GENERIC_READ,
                FILE_SHARE_READ | FILE_SHARE_WRITE | FILE_SHARE_DELETE,
                0,
            )
        };
        if handle == INVALID_HANDLE_VALUE {
            return Err(io_error(std::io::Error::last_os_error()));
        }
        // SAFETY: successful ReOpenFile returns a new handle transferred exactly once.
        Ok(unsafe { File::from_raw_handle(handle) })
    }
    pub(super) fn replace(file: &File, to: &Path, create: bool) -> Result<(), VaultError> {
        let name = wide(to)?;
        if name.len() > 32768 {
            return Err(VaultError::InvalidPath);
        }
        let offset = std::mem::offset_of!(FILE_RENAME_INFO, FileName);
        let bytes = (offset + name.len() * 2).max(std::mem::size_of::<FILE_RENAME_INFO>());
        // u64 storage supplies FILE_RENAME_INFO's alignment on Windows x64.
        let mut buffer = vec![0u64; bytes.div_ceil(8)];
        let info = buffer.as_mut_ptr().cast::<FILE_RENAME_INFO>();
        // SAFETY: aligned, zero-initialized buffer holds the full struct plus UTF-16
        // tail; all pointers remain live through the synchronous handle-based call.
        unsafe {
            (*info).Anonymous.ReplaceIfExists = !create;
            (*info).FileNameLength = ((name.len() - 1) * 2) as u32;
            ptr::copy_nonoverlapping(
                name.as_ptr(),
                buffer.as_mut_ptr().cast::<u8>().add(offset).cast::<u16>(),
                name.len(),
            );
            if SetFileInformationByHandle(
                file.as_raw_handle(),
                FileRenameInfo,
                info.cast(),
                bytes as u32,
            ) == 0
            {
                return Err(io_error(std::io::Error::last_os_error()));
            }
        }
        Ok(())
    }
    pub(super) fn delete(file: &File) -> Result<(), VaultError> {
        let info = FILE_DISPOSITION_INFO { DeleteFile: true };
        // SAFETY: the live owner has DELETE access; only its identity is marked.
        if unsafe {
            SetFileInformationByHandle(
                file.as_raw_handle(),
                FileDispositionInfo,
                ptr::from_ref(&info).cast(),
                std::mem::size_of_val(&info) as u32,
            )
        } == 0
        {
            return Err(io_error(std::io::Error::last_os_error()));
        }
        Ok(())
    }
    pub(super) fn current_path(file: &File) -> Result<PathBuf, VaultError> {
        let mut name = vec![0u16; 32768];
        // SAFETY: live handle and explicitly sized writable UTF-16 buffer.
        let size = unsafe {
            GetFinalPathNameByHandleW(
                file.as_raw_handle(),
                name.as_mut_ptr(),
                name.len() as u32,
                0,
            )
        } as usize;
        if size == 0 || size >= name.len() {
            return Err(VaultError::Io);
        }
        Ok(PathBuf::from(std::ffi::OsString::from_wide(&name[..size])))
    }
}
#[cfg(not(windows))]
mod platform {
    use super::*;
    pub(super) fn check(_path: &Path) -> Result<(), VaultError> {
        Err(VaultError::UnsupportedFilesystem)
    }
    pub(super) fn replace(_from: &File, _to: &Path, _create: bool) -> Result<(), VaultError> {
        Err(VaultError::UnsupportedFilesystem)
    }
    pub(super) fn create(_path: &Path) -> Result<File, VaultError> {
        Err(VaultError::UnsupportedFilesystem)
    }
    pub(super) fn reopen(_file: &File) -> Result<File, VaultError> {
        Err(VaultError::UnsupportedFilesystem)
    }
    pub(super) fn delete(_file: &File) -> Result<(), VaultError> {
        Err(VaultError::UnsupportedFilesystem)
    }
    pub(super) fn current_path(_file: &File) -> Result<PathBuf, VaultError> {
        Err(VaultError::UnsupportedFilesystem)
    }
}
#[cfg(all(test, windows))]
mod tests {
    use super::*;
    use crate::crypto;
    #[test]
    fn rotation_entropy_and_each_persistence_failure_preserve_session_and_image() {
        let dir = tempfile::tempdir().unwrap();
        let path = dir.path().join("rotation.tessaveil-alpha");
        let password = "synthetic-current-password";
        let replacement = "synthetic-replacement-password";
        let mut vault = VaultService::create(
            &path,
            password,
            CreateOptions {
                storage: StoragePolicy::DevelopmentLocalNtfs,
                ..Default::default()
            },
        )
        .unwrap();
        let words: Vec<_> = (0..40).map(|i| format!("synthetic-{i:03}")).collect();
        vault
            .payload_mut()
            .unwrap()
            .create_custom_sheet(
                "synthetic-table",
                crate::sheet::SheetSize {
                    rows: 12,
                    columns: 10,
                },
                &words,
            )
            .unwrap();
        vault
            .payload_mut()
            .unwrap()
            .edit_sheet(0)
            .unwrap()
            .set_verified_by_me(true);
        vault.save().unwrap();
        vault.unlock_sheet_with_master(0, password).unwrap();
        let old_payload = vault.unlocked.as_ref().unwrap().payload.encode().unwrap();
        let old = std::fs::read(&path).unwrap();
        let old_salt = vault.unlocked.as_ref().unwrap().salt;
        let old_dek = zeroize::Zeroizing::new(*vault.unlocked.as_ref().unwrap().secrets.dek);
        let old_kek = zeroize::Zeroizing::new(*vault.unlocked.as_ref().unwrap().secrets.kek);
        // Fail salt, DEK, then nonce entropy. Successful draws remain OS-random.
        for fail_call in 0..3 {
            let mut call = 0;
            let mut fill = |bytes: &mut [u8]| {
                let this = call;
                call += 1;
                if this == fail_call {
                    return Err(VaultError::Io);
                }
                getrandom::getrandom(bytes).map_err(|_| VaultError::Io)
            };
            let mut random = crypto::Random::injected(&mut fill);
            assert_eq!(
                vault.rotate(password, replacement, &mut random, |_, _| Ok(())),
                Err(VaultError::Io)
            );
            let u = vault.unlocked.as_ref().unwrap();
            assert_eq!(u.salt, old_salt);
            assert_eq!(*u.secrets.dek, *old_dek);
            assert_eq!(*u.secrets.kek, *old_kek);
            assert_eq!(*u.payload.encode().unwrap(), *old_payload);
            assert!(u.payload.sheets[0].unlocked);
            assert_eq!(std::fs::read(&path).unwrap(), old);
            assert_eq!(std::fs::read_dir(dir.path()).unwrap().count(), 1);
        }
        for failure in [
            Stage::BeforeWrite,
            Stage::AfterWrite,
            Stage::AfterFlush,
            Stage::AfterVerify,
            Stage::BeforeReplace,
        ] {
            assert_eq!(
                vault.rotate(
                    password,
                    replacement,
                    &mut crypto::Random::default(),
                    |stage, _| {
                        if stage == failure {
                            Err(VaultError::InsufficientSpace)
                        } else {
                            Ok(())
                        }
                    }
                ),
                Err(VaultError::InsufficientSpace)
            );
            let u = vault.unlocked.as_ref().unwrap();
            assert_eq!(u.salt, old_salt);
            assert_eq!(*u.secrets.dek, *old_dek);
            assert_eq!(*u.secrets.kek, *old_kek);
            assert_eq!(*u.payload.encode().unwrap(), *old_payload);
            assert!(u.payload.sheets[0].unlocked);
            assert_eq!(std::fs::read(&path).unwrap(), old);
            assert_eq!(std::fs::read_dir(dir.path()).unwrap().count(), 1);
        }
        vault.change_master_password(password, replacement).unwrap();
        assert_ne!(*vault.unlocked.as_ref().unwrap().secrets.dek, *old_dek);
        assert_eq!(
            *vault.unlocked.as_ref().unwrap().payload.encode().unwrap(),
            *old_payload
        );
        assert!(!vault.unlocked.as_ref().unwrap().payload.sheets[0].unlocked);
        let (reopened, _) = crypto::open(&std::fs::read(&path).unwrap(), replacement).unwrap();
        assert_eq!(*reopened.encode().unwrap(), *old_payload);
    }
    #[test]
    fn source_guard_and_nonreplacing_commit_defeat_recovery_name_races() {
        let dir = tempfile::tempdir().unwrap();
        let source = dir.path().join("source.tessaveil-alpha");
        let destination = dir.path().join("destination.tessaveil-alpha");
        let (image, secrets) =
            crypto::create("synthetic-recovery-password", &Payload::default()).unwrap();
        std::fs::write(&source, &image).unwrap();
        let (_, guard) = read_recovery_image(&source).unwrap();
        assert!(std::fs::rename(&source, dir.path().join("displaced.tessaveil-alpha")).is_err());
        assert!(std::fs::write(&source, b"synthetic-substitute").is_err());
        let result = persist_image(&destination, &image, &secrets, true, |stage, _| {
            if stage == Stage::BeforeReplace {
                std::fs::hard_link(&source, &destination).unwrap();
            }
            Ok(())
        });
        assert!(result.is_err());
        assert_eq!(std::fs::read(&source).unwrap(), image);
        assert_eq!(std::fs::read(&destination).unwrap(), image);
        drop(guard);
        assert_eq!(std::fs::read_dir(dir.path()).unwrap().count(), 2);
    }
    #[test]
    fn replaced_temp_name_never_commits_unverified_bytes() {
        let dir = tempfile::tempdir().unwrap();
        let path = dir.path().join("target.tessaveil-alpha");
        let mut p = Payload::default();
        p.rename("synthetic-old").unwrap();
        let (old, s) = crypto::create("synthetic-fix-password", &p).unwrap();
        std::fs::write(&path, &old).unwrap();
        p.rename("synthetic-new").unwrap();
        let new = crypto::seal(&p, &s, &old[24..40]).unwrap();
        let displaced = dir.path().join("owned-displaced.tmp");
        let mut substitute = new.clone();
        *substitute.last_mut().unwrap() ^= 1;
        let mut original_name = None;
        let result = persist_image(&path, &new, &s, false, |stage, temp| {
            if stage == Stage::AfterVerify {
                std::fs::rename(temp, &displaced).unwrap();
                std::fs::write(temp, &substitute).unwrap();
                original_name = Some(temp.to_path_buf());
            }
            Ok(())
        });
        assert_eq!(result, Ok(()));
        assert_eq!(
            std::fs::read(&path).unwrap(),
            new,
            "only the verified file object may be committed"
        );
        assert_eq!(
            std::fs::read(original_name.unwrap()).unwrap(),
            substitute,
            "foreign replacement name must remain untouched"
        );
        assert!(!displaced.exists());
    }
    #[test]
    fn replaced_temp_name_error_cleanup_deletes_only_owned_identity() {
        let dir = tempfile::tempdir().unwrap();
        let path = dir.path().join("target.tessaveil-alpha");
        let (old, s) = crypto::create("synthetic-fix-password", &Payload::default()).unwrap();
        std::fs::write(&path, &old).unwrap();
        let displaced = dir.path().join("owned-displaced.tmp");
        let mut original_name = None;
        let result = persist_image(&path, &old, &s, false, |stage, temp| {
            if stage == Stage::AfterVerify {
                std::fs::rename(temp, &displaced).unwrap();
                std::fs::write(temp, b"synthetic-foreign-file").unwrap();
                original_name = Some(temp.to_path_buf());
                return Err(VaultError::Io);
            }
            Ok(())
        });
        assert_eq!(std::fs::read(&path).unwrap(), old);
        assert_eq!(
            std::fs::read(original_name.unwrap()).ok().as_deref(),
            Some(b"synthetic-foreign-file".as_slice()),
            "cleanup must not remove the substituted name"
        );
        assert_eq!(result, Err(VaultError::Io));
        assert!(
            !displaced.exists(),
            "owned object must be cleaned or explicitly reported"
        );
    }
    #[test]
    fn overdue_activity_cannot_revive_secrets_and_overdue_access_locks() {
        fn overdue() -> OpenVault {
            OpenVault {
                path: PathBuf::new(),
                storage: StoragePolicy::ReadOnly,
                session: Session::new(
                    Inactivity::OneMinute,
                    Instant::now() - std::time::Duration::from_secs(61),
                ),
                unlocked: Some(Unlocked {
                    payload: Payload::default(),
                    secrets: Secrets {
                        kek: zeroize::Zeroizing::new([7; 32]),
                        dek: zeroize::Zeroizing::new([9; 32]),
                    },
                    salt: [0; 16],
                }),
            }
        }
        let mut v = overdue();
        assert!(matches!(
            v.activity(Instant::now()),
            Err(VaultError::Locked)
        ));
        assert!(v.is_locked());
        let mut v = overdue();
        assert!(matches!(v.payload_mut(), Err(VaultError::Locked)));
        assert!(v.is_locked());
        let mut v = overdue();
        assert_eq!(v.save(), Err(VaultError::Locked));
        assert!(v.is_locked());
    }
    #[test]
    fn failures_before_replacement_keep_old_image_and_cleanup_owned_temp() {
        let dir = tempfile::tempdir().unwrap();
        let path = dir.path().join("fault.tessaveil-alpha");
        let mut p = Payload::default();
        p.rename("synthetic-old").unwrap();
        let (old, s) = crypto::create("synthetic-test-password", &p).unwrap();
        std::fs::write(&path, &old).unwrap();
        p.rename("synthetic-new").unwrap();
        let new = crypto::seal(&p, &s, &old[24..40]).unwrap();
        for failure in [
            Stage::BeforeWrite,
            Stage::AfterWrite,
            Stage::AfterFlush,
            Stage::AfterVerify,
            Stage::BeforeReplace,
        ] {
            let result = persist_image(&path, &new, &s, false, |stage, temp| {
                if stage != Stage::BeforeWrite {
                    let image = std::fs::read(temp).unwrap();
                    assert_eq!(&image[..8], b"TSVALPHA");
                    assert!(!image.windows(13).any(|w| w == b"synthetic-new"));
                }
                if stage == failure {
                    Err(VaultError::InsufficientSpace)
                } else {
                    Ok(())
                }
            });
            assert_eq!(result, Err(VaultError::InsufficientSpace));
            assert_eq!(std::fs::read(&path).unwrap(), old);
            assert_eq!(std::fs::read_dir(dir.path()).unwrap().count(), 1);
        }
        let mut broken = new.clone();
        *broken.last_mut().unwrap() ^= 1;
        assert_eq!(
            persist_image(&path, &broken, &s, false, |_, _| Ok(())),
            Err(VaultError::Authentication)
        );
        assert_eq!(std::fs::read(&path).unwrap(), old);
        // A denied cleanup identifies only this operation's encrypted temp image.
        let displaced = dir.path().join("owned-displaced.tmp");
        let mut foreign_name = None;
        let mut original_permissions = None;
        let failure = persist_image(&path, &new, &s, false, |stage, temp| {
            if stage == Stage::AfterVerify {
                std::fs::rename(temp, &displaced).unwrap();
                std::fs::write(temp, b"synthetic-foreign-file").unwrap();
                foreign_name = Some(temp.to_path_buf());
                let mut permissions = std::fs::metadata(&displaced).unwrap().permissions();
                original_permissions = Some(permissions.clone());
                permissions.set_readonly(true);
                std::fs::set_permissions(&displaced, permissions).unwrap();
                return Err(VaultError::InsufficientSpace);
            }
            Ok(())
        });
        match failure {
            Err(VaultError::TemporaryRemains {
                cause,
                path: Some(temp),
            }) => {
                assert_eq!(*cause, VaultError::InsufficientSpace);
                assert_eq!(temp, displaced.canonicalize().unwrap());
                assert_eq!(std::fs::read(&temp).unwrap(), new);
                std::fs::set_permissions(&temp, original_permissions.take().unwrap()).unwrap();
            }
            _ => panic!("cleanup failure must identify the encrypted temporary image"),
        }
        assert_eq!(std::fs::read(&path).unwrap(), old);
        assert_eq!(
            std::fs::read(foreign_name.unwrap()).unwrap(),
            b"synthetic-foreign-file"
        );
    }
}
