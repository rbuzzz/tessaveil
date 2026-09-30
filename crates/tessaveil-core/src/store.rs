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
        persist_image(&self.path, &image, &u.secrets, false, |_, _| Ok(()))
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
    let mut file = options.open(path).map_err(io_error)?;
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
    let mut temp = tempfile::Builder::new()
        .prefix(".tessaveil-alpha-")
        .suffix(".tmp")
        .make_in(path.parent().ok_or(VaultError::InvalidPath)?, |p| {
            let mut options = OpenOptions::new();
            options.read(true).write(true).create_new(true);
            #[cfg(windows)]
            {
                use std::os::windows::fs::OpenOptionsExt;
                options
                    .custom_flags(windows_sys::Win32::Storage::FileSystem::FILE_FLAG_WRITE_THROUGH);
            }
            options.open(p)
        })
        .map_err(io_error)?;
    let early = (|| {
        hook(Stage::BeforeWrite, temp.path())?;
        temp.write_all(image).map_err(io_error)?;
        hook(Stage::AfterWrite, temp.path())?;
        temp.flush().map_err(io_error)?;
        temp.as_file().sync_all().map_err(io_error)
    })();
    let temp = temp.into_temp_path();
    let temporary_path = temp.to_path_buf();
    let result = early.and_then(|()| {
        hook(Stage::AfterFlush, &temp)?;
        let (reopened, _guard) = read_image(&temp)?;
        crypto::verify(&reopened, secrets)?;
        hook(Stage::AfterVerify, &temp)?;
        hook(Stage::BeforeReplace, &temp)?;
        platform::replace(&temp, path, create)
    });
    if let Err(cause) = result {
        if temp.close().is_err() {
            return Err(VaultError::TemporaryRemains {
                cause: Box::new(cause),
                path: temporary_path,
            });
        }
        return Err(cause);
    }
    // The source name no longer exists after replacement; TempPath drop is harmless.
    Ok(())
}
#[cfg(windows)]
mod platform {
    use super::*;
    use std::{os::windows::ffi::OsStrExt, ptr};
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
    pub(super) fn replace(from: &Path, to: &Path, create: bool) -> Result<(), VaultError> {
        let from = wide(from)?;
        let to = wide(to)?;
        let flags = MOVEFILE_WRITE_THROUGH | if create { 0 } else { MOVEFILE_REPLACE_EXISTING };
        // SAFETY: terminated UTF-16 buffers live through the synchronous OS call.
        if unsafe { MoveFileExW(from.as_ptr(), to.as_ptr(), flags) } == 0 {
            return Err(io_error(std::io::Error::last_os_error()));
        }
        Ok(())
    }
}
#[cfg(not(windows))]
mod platform {
    use super::*;
    pub(super) fn check(_path: &Path) -> Result<(), VaultError> {
        Err(VaultError::UnsupportedFilesystem)
    }
    pub(super) fn replace(_from: &Path, _to: &Path, _create: bool) -> Result<(), VaultError> {
        Err(VaultError::UnsupportedFilesystem)
    }
}
#[cfg(all(test, windows))]
mod tests {
    use super::*;
    use crate::crypto;
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
        assert_eq!(
            persist_image(&path, &new, &s, false, |stage, temp| {
                if stage == Stage::AfterFlush {
                    let mut broken = new.clone();
                    *broken.last_mut().unwrap() ^= 1;
                    std::fs::write(temp, broken).unwrap();
                }
                Ok(())
            }),
            Err(VaultError::Authentication)
        );
        assert_eq!(std::fs::read(&path).unwrap(), old);
        // A denied cleanup identifies only this operation's encrypted temp image.
        use std::os::windows::fs::OpenOptionsExt;
        let mut held = None;
        let failure = persist_image(&path, &new, &s, false, |stage, temp| {
            if stage == Stage::AfterFlush {
                held = Some(
                    OpenOptions::new()
                        .read(true)
                        .share_mode(1)
                        .open(temp)
                        .unwrap(),
                );
                return Err(VaultError::InsufficientSpace);
            }
            Ok(())
        });
        match failure {
            Err(VaultError::TemporaryRemains { cause, path: temp }) => {
                assert_eq!(*cause, VaultError::InsufficientSpace);
                assert_eq!(temp.parent(), path.parent());
                assert_eq!(std::fs::read(temp).unwrap(), new);
            }
            _ => panic!("cleanup failure must identify the encrypted temporary image"),
        }
        assert_eq!(std::fs::read(&path).unwrap(), old);
        drop(held);
    }
}
