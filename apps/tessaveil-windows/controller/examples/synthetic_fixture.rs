//! Development observation fixture. Never linked into Tessaveil.exe.
use tessaveil_core::{sheet::SheetSize, CreateOptions, StoragePolicy, VaultService};
fn main() {
    let path = std::env::args()
        .nth(1)
        .expect("provide a new task-owned .tessaveil-alpha path");
    let mut vault = VaultService::create(
        path,
        "synthetic-master-password",
        CreateOptions {
            name: "Synthetic observation".into(),
            storage: StoragePolicy::DevelopmentLocalNtfs,
            ..Default::default()
        },
    )
    .expect("create synthetic fixture");
    let words: Vec<String> = (0..80).map(|i| format!("synthetic-{i:03}")).collect();
    for columns in [10, 36] {
        vault
            .payload_mut()
            .unwrap()
            .create_custom_sheet(
                &format!("Synthetic {columns} columns"),
                SheetSize { rows: 24, columns },
                &words,
            )
            .unwrap();
    }
    vault.save().unwrap();
    vault.lock();
}
