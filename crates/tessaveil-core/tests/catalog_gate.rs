use tessaveil_core::catalog;

#[test]
fn only_projected_approved_pairs_can_be_selected() {
    let profiles = catalog::profiles().unwrap();
    let selected: Vec<_> = profiles
        .iter()
        .filter(|p| p.selectable())
        .map(|p| (p.id(), p.mode()))
        .collect();
    assert_eq!(
        selected,
        vec![
            ("mytonwallet-native", "ton-native-generated"),
            ("tonhub", "ton-native-generated"),
            ("tonkeeper-classic", "ton-native-generated"),
        ]
    );
    assert!(profiles.len() > 100);
    for p in profiles {
        if !p.selectable() {
            assert!(!p.reason().is_empty());
            assert!(catalog::select(p.id(), p.mode()).is_err());
        }
    }
    assert!(catalog::select("tonhub", "wrong-mode").is_err());
}

#[test]
fn exact_ton_modes_and_supported_lengths_stay_distinct() {
    let profiles = catalog::profiles().unwrap();
    let profile = |id: &str, mode: &str| {
        profiles
            .iter()
            .find(|profile| profile.id() == id && profile.mode() == mode)
            .unwrap_or_else(|| panic!("missing exact profile pair {id}/{mode}"))
    };

    for (id, mode) in [
        ("mytonwallet-native", "ton-native-generated"),
        ("tonhub", "ton-native-generated"),
        ("tonkeeper-classic", "ton-native-generated"),
    ] {
        let selected = profile(id, mode);
        assert!(selected.selectable());
        assert_eq!(selected.supported_lengths(), &[24]);
    }

    for (id, mode) in [
        ("mytonwallet", "bip39-multichain-generated"),
        ("tonkeeper-multichain", "bip39-multichain-generated"),
        ("gram-wallet", "mnemonic-backup-unresolved"),
    ] {
        assert!(!profile(id, mode).selectable());
        assert!(catalog::select(id, mode).is_err());
    }
}
