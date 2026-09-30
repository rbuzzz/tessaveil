//! Emits a candidate only; a self-generated round trip is not independent validation.
#[allow(dead_code)]
#[path = "../tests/support/mod.rs"]
mod support;

fn main() -> std::io::Result<()> {
    use std::io::Write;
    let path =
        std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("../vectors/synthetic-vault-v0.bin");
    // Never overwrite a fixture that has already been reviewed.
    let mut file = std::fs::OpenOptions::new()
        .write(true)
        .create_new(true)
        .open(path)?;
    file.write_all(&support::fixture())?;
    file.sync_all()
}
